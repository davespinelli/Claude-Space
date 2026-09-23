#!/usr/bin/env python3
"""
Operating-leverage study: data build.

Builds a point-in-time firm-year panel from SEC filings as they exist in the
XBRL frames API (every filer that ever reported, including companies that later
delisted or were acquired), attaches SIC codes and current tickers from the SEC
submissions API, downloads monthly Yahoo prices for whatever tickers exist, and
writes:

    research/oplev/panel.parquet          firm-year panel (formation years 2011-2025)
    research/oplev/cache/returns.parquet  monthly total returns, date x ticker
    research/oplev/cache/build_log.json   coverage / data-problem counts

Everything downloaded is cached under research/oplev/cache/ and reused, so a
rerun makes no network requests once the cache is warm.

Run:  .venv/bin/python research/oplev/build_panel.py [--stage frames|subs|prices|panel|all]

Fixed definitions (see run_tests.py docstring for the pre-registered tests):
  * Portfolios are formed at the end of June of year t from frames CY(t-1).
  * No-look-ahead guard: the frames API files a fiscal year under the calendar
    year it overlaps most, so CY(t-1) contains fiscal years that end as late as
    June of year t (not yet filed at the end of June). A firm-year is used only
    if its CY(t-1) fiscal year ended on or before the last day of February of
    year t (10-K deadline <= 90 days, + 15-day NT extension, still before June 30).
  * Universe: SIC not 6000-6999 and not 4900-4999 (current SIC from submissions),
    revenue > $10M, total assets > 0, market cap at formation >= $50M, where
    market cap = shares (CY(t-1)Q4I) x June-end close of year t, both put on the
    same split basis using Yahoo's split history.
"""
from __future__ import annotations

import argparse
import datetime as dt
import gzip
import json
import math
import re
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np
import pandas as pd
import requests

HERE = Path(__file__).resolve().parent
CACHE = HERE / "cache"
FRAMES = CACHE / "frames"
SUBS = CACHE / "submissions"
PRICES = CACHE / "prices"
for d in (CACHE, FRAMES, SUBS, PRICES):
    d.mkdir(parents=True, exist_ok=True)

UA = "ClaudeSpace research dspinjr@gmail.com"
HEADERS = {"User-Agent": UA, "Accept-Encoding": "gzip, deflate"}
MIN_REQ_INTERVAL = 1.0 / 7.5          # <= 7.5 requests/second to SEC (limit asked: 8)

YEARS = list(range(2009, 2026))       # frames CY2009 .. CY2025
FORMATIONS = list(range(2011, 2026))  # June 2011 .. June 2025

# Revenue fallback chain: the three tags used by research/deepvalue/screen.py
# first (same order), then further total-revenue tags; the goods/services split
# tags are summed and used only when no total tag exists for that firm-year.
REV_TAGS = [
    "Revenues",
    "RevenueFromContractWithCustomerExcludingAssessedTax",
    "SalesRevenueNet",
    "RevenueFromContractWithCustomerIncludingAssessedTax",
]
REV_PART_TAGS = ["SalesRevenueGoodsNet", "SalesRevenueServicesNet"]
OPINC_TAG = "OperatingIncomeLoss"
ASSETS_TAG = "Assets"
SHARES_DEI = ("dei", "EntityCommonStockSharesOutstanding")
SHARES_GAAP = ("us-gaap", "CommonStockSharesOutstanding")
FLOAT_DEI = ("dei", "EntityPublicFloat")
# Share-count fallbacks beyond the two named in the brief (dei Q4I, then
# us-gaap CommonStockSharesOutstanding Q4I), used only when both are absent:
#   3. dei cover-page count from the next CY Q1I instant (the 10-K cover date of
#      a December filer, Feb-Apr of year t, still before the June formation date)
#   4. us-gaap WeightedAverageNumberOfSharesOutstandingBasic for fiscal CY(t-1).
WANSO_TAG = "WeightedAverageNumberOfSharesOutstandingBasic"
SHARE_SOURCES = {            # priority order
    "dei": ("dei", "EntityCommonStockSharesOutstanding", "CY{y}Q4I"),
    "gaap": ("us-gaap", "CommonStockSharesOutstanding", "CY{y}Q4I"),
    "deiQ1": ("dei", "EntityCommonStockSharesOutstanding", "CY{y1}Q1I"),
    "wanso": ("us-gaap", WANSO_TAG, "CY{y}"),
}
# Share-count checks (data integrity, fixed): cover-page share counts are
# sometimes tagged 1,000x too large or small (e.g. Alaska Air CY2010 dei = 35.8
# billion shares). Each available source is put on today's split basis. A source
# is used only if (1) it is within 3x of at least one other source, when any two
# sources agree, and (2) its implied market cap / max(revenue, total assets) lies
# in [0.002, 100]. The first source in priority order passing both is used; if
# none does, the share count is treated as unknown and the firm is not held.
MCAP_RATIO_BAND = (0.002, 100.0)
# Yahoo split records are used as given. They include Yahoo's spin-off price
# adjustments (e.g. eBay/PayPal 2015 recorded as a 2.376 "split"), which Yahoo
# also applies to its historical closes, so they are needed to recover the raw
# price. (An attempt to validate records against SEC cover-page share counts was
# dropped: cover counts are often dated at the fiscal period end although they
# are measured at the later cover date, so genuine splits looked contradicted.)
# A symbol recovered from an old filing (see recover_hist_tickers) is only used
# when the implied market cap is consistent with the company's own last reported
# public float: 0.2 <= float / market cap <= 5. Guards against a recycled symbol.
HIST_FLOAT_BAND = (0.2, 5.0)

REV_MIN = 10e6
MCAP_MIN = 50e6
PRICE_START = "2010-01-01"
BENCH = ["IWM", "SPY"]

_last_req = [0.0]
_lock = threading.Lock()
_session = requests.Session()


def log(msg: str) -> None:
    print(f"[{dt.datetime.now():%H:%M:%S}] {msg}", flush=True)


def _throttle() -> None:
    with _lock:
        wait = MIN_REQ_INTERVAL - (time.time() - _last_req[0])
        if wait > 0:
            time.sleep(wait)
        _last_req[0] = time.time()


def get_json(url: str, cache: Path, tries: int = 6):
    """Fetch JSON with a permanent gzip cache. 404 is cached as null."""
    if cache.exists():
        with gzip.open(cache, "rt") as fh:
            txt = fh.read()
        return json.loads(txt)
    for attempt in range(tries):
        try:
            _throttle()
            r = _session.get(url, headers=HEADERS, timeout=90)
            if r.status_code == 404:
                with gzip.open(cache, "wt") as fh:
                    fh.write("null")
                return None
            if r.status_code in (403, 429, 500, 502, 503, 504):
                raise RuntimeError(f"HTTP {r.status_code}")
            r.raise_for_status()
            js = r.json()
            with gzip.open(cache, "wt") as fh:
                fh.write(r.text)
            return js
        except Exception as exc:  # noqa: BLE001
            if attempt == tries - 1:
                log(f"  ! giving up on {url}: {exc}")
                return "FAILED"
            time.sleep(2.0 * (attempt + 1) ** 2)
    return "FAILED"


# --------------------------------------------------------------------------- #
# 1. Frames
# --------------------------------------------------------------------------- #
def frame_jobs() -> list[tuple[str, str, str, str]]:
    jobs = []
    for y in YEARS:
        for tag in REV_TAGS + REV_PART_TAGS + [OPINC_TAG]:
            jobs.append(("us-gaap", tag, "USD", f"CY{y}"))
        jobs.append(("us-gaap", ASSETS_TAG, "USD", f"CY{y}Q4I"))
        jobs.append((SHARES_DEI[0], SHARES_DEI[1], "shares", f"CY{y}Q4I"))
        jobs.append((SHARES_GAAP[0], SHARES_GAAP[1], "shares", f"CY{y}Q4I"))
        jobs.append((SHARES_DEI[0], SHARES_DEI[1], "shares", f"CY{y}Q1I"))
        jobs.append(("us-gaap", WANSO_TAG, "shares", f"CY{y}"))
        for q in (1, 2, 3, 4):
            jobs.append((FLOAT_DEI[0], FLOAT_DEI[1], "USD", f"CY{y}Q{q}I"))
    return jobs


def frame_path(tax, tag, unit, per) -> Path:
    return FRAMES / f"{tax}_{tag}_{unit}_{per}.json.gz"


def fetch_frames() -> dict:
    jobs = frame_jobs()
    log(f"frames: {len(jobs)} requests (cached ones are free)")
    failed = []
    for i, (tax, tag, unit, per) in enumerate(jobs, 1):
        url = f"https://data.sec.gov/api/xbrl/frames/{tax}/{tag}/{unit}/{per}.json"
        js = get_json(url, frame_path(tax, tag, unit, per))
        if js == "FAILED":
            failed.append(url)
        if i % 25 == 0:
            log(f"  frames {i}/{len(jobs)}")
    if failed:
        log(f"  ! {len(failed)} frames failed: {failed[:5]}")
    return {"n_frames": len(jobs), "failed": failed}


def load_frame(tax, tag, unit, per) -> pd.DataFrame:
    p = frame_path(tax, tag, unit, per)
    cols = ["cik", "val", "end", "start", "accn"]
    if not p.exists():
        return pd.DataFrame(columns=cols)
    with gzip.open(p, "rt") as fh:
        js = json.loads(fh.read())
    if not js or "data" not in js:
        return pd.DataFrame(columns=cols)
    df = pd.DataFrame(js["data"])
    for c in cols:
        if c not in df.columns:
            df[c] = None
    df = df[cols].copy()
    df["cik"] = df["cik"].astype("int64")
    df["val"] = pd.to_numeric(df["val"], errors="coerce")
    df["end"] = pd.to_datetime(df["end"])
    df["start"] = pd.to_datetime(df["start"])
    df["accn"] = df["accn"].astype(str)
    return df.drop_duplicates("cik", keep="last")


def fundamentals_long() -> pd.DataFrame:
    """One row per (cik, fy) with revenue, op income, assets, shares, float."""
    rows = []
    for y in YEARS:
        # revenue: first total tag present wins; else sum of goods + services
        rev = None
        for tag in REV_TAGS:
            f = load_frame("us-gaap", tag, "USD", f"CY{y}")
            f = f.dropna(subset=["val"])
            f = f.assign(rev_tag=tag)
            rev = f if rev is None else pd.concat([rev, f[~f.cik.isin(rev.cik)]])
        parts = [load_frame("us-gaap", t, "USD", f"CY{y}").dropna(subset=["val"]) for t in REV_PART_TAGS]
        parts = pd.concat(parts)
        parts = parts[~parts.cik.isin(rev.cik)]
        if len(parts):
            agg = parts.groupby("cik").agg(val=("val", "sum"), end=("end", "max"),
                                           start=("start", "min"), accn=("accn", "first")).reset_index()
            agg["rev_tag"] = "Goods+Services"
            rev = pd.concat([rev, agg])
        rev = rev.rename(columns={"val": "revenue", "end": "rev_end", "start": "rev_start",
                                  "accn": "rev_accn"})
        oi = load_frame("us-gaap", OPINC_TAG, "USD", f"CY{y}").rename(
            columns={"val": "opinc", "end": "oi_end", "start": "oi_start", "accn": "oi_accn"})
        at = load_frame("us-gaap", ASSETS_TAG, "USD", f"CY{y}Q4I")[["cik", "val", "end"]].rename(
            columns={"val": "assets", "end": "assets_end"})
        # all four share-count sources kept side by side; the panel step picks one
        srcs = {}
        for key, (tax, tag, per) in SHARE_SOURCES.items():
            per = per.format(y=y, y1=y + 1)
            f = load_frame(tax, tag, "shares", per)[["cik", "val", "end", "accn"]]
            f = f[f.val > 0].rename(columns={"val": f"sh_{key}", "end": f"sh_{key}_end",
                                             "accn": f"sh_{key}_accn"})
            srcs[key] = f
        sh = None
        for f in srcs.values():
            sh = f if sh is None else sh.merge(f, on="cik", how="outer")
        fl = []
        for q in (1, 2, 3, 4):
            ff = load_frame(*FLOAT_DEI, "USD", f"CY{y}Q{q}I")[["cik", "val", "end"]]
            fl.append(ff)
        fl = pd.concat(fl).dropna(subset=["val"]).sort_values("end")
        fl = fl.drop_duplicates("cik", keep="last").rename(columns={"val": "pfloat", "end": "pfloat_end"})
        allc = pd.Index(sorted(set(rev.cik) | set(oi.cik)), name="cik")
        df = pd.DataFrame(index=allc).reset_index()
        for part in (rev, oi[["cik", "opinc", "oi_end", "oi_start", "oi_accn"]], at, sh, fl):
            df = df.merge(part, on="cik", how="left")
        df["fy"] = y
        rows.append(df)
        log(f"  CY{y}: revenue {rev.cik.nunique()}, opinc {oi.cik.nunique()}, assets {at.cik.nunique()}, "
            f"shares {sh.cik.nunique()} (dei {len(srcs['dei'])}), float {fl.cik.nunique()}")
    out = pd.concat(rows, ignore_index=True)
    for c in ["rev_end", "rev_start", "oi_end", "oi_start", "assets_end", "pfloat_end"] + \
            [f"sh_{k}_end" for k in SHARE_SOURCES]:
        out[c] = pd.to_datetime(out[c])
    for c in ["revenue", "opinc", "assets", "pfloat"] + [f"sh_{k}" for k in SHARE_SOURCES]:
        out[c] = pd.to_numeric(out[c], errors="coerce").astype("float64")
    # op income must describe the same fiscal period as revenue
    bad = out.opinc.notna() & out.revenue.notna() & ((out.oi_end - out.rev_end).abs().dt.days > 31)
    out["oi_period_mismatch"] = bad
    out.loc[bad, "opinc"] = np.nan
    return out


# --------------------------------------------------------------------------- #
# 2. Submissions (SIC, tickers)
# --------------------------------------------------------------------------- #
def fetch_submissions(ciks: list[int]) -> pd.DataFrame:
    log(f"submissions: {len(ciks)} CIKs")
    out = {}

    def one(cik):
        js = get_json(f"https://data.sec.gov/submissions/CIK{cik:010d}.json",
                      SUBS / f"CIK{cik:010d}.json.gz")
        if not js or js == "FAILED":
            return cik, None, js == "FAILED"
        sic = str(js.get("sic") or "").strip()
        return cik, dict(
            sic=int(sic) if sic.isdigit() else np.nan,
            sic_desc=js.get("sicDescription") or "",
            name=js.get("name") or "",
            sub_tickers="|".join([t for t in (js.get("tickers") or []) if t]),
            exchanges="|".join([e for e in (js.get("exchanges") or []) if e]),
            entity_type=js.get("entityType") or "",
            fye=js.get("fiscalYearEnd") or "",
            n_10k=sum(f in ("10-K", "10-K405", "10-KT") for f in js.get("filings", {}).get("recent", {}).get("form", [])),
            n_20f=sum(f in ("20-F", "40-F") for f in js.get("filings", {}).get("recent", {}).get("form", [])),
        ), False

    failed = []
    with ThreadPoolExecutor(max_workers=6) as ex:
        for i, (cik, rec, f) in enumerate(ex.map(one, ciks), 1):
            if rec:
                out[cik] = rec
            if f:
                failed.append(cik)
            if i % 500 == 0:
                log(f"  submissions {i}/{len(ciks)}")
    df = pd.DataFrame.from_dict(out, orient="index")
    df.index.name = "cik"
    if failed:
        log(f"  ! submissions failed for {len(failed)} CIKs")
    return df, failed


BAD_SUFFIXES = {"W", "WS", "WT", "U", "UN", "R", "RT", "RTS", "P", "PR"}


def clean_ticker(t: str) -> str | None:
    t = (t or "").strip().upper()
    if not t or " " in t:
        return None
    t = t.replace(".", "-")
    if "-" in t:
        _, _, suf = t.partition("-")
        if suf in BAD_SUFFIXES or len(suf) > 2:
            return None
    if len(t) > 7:
        return None
    return t


def ticker_map(subs: pd.DataFrame) -> pd.DataFrame:
    """cik -> primary Yahoo ticker. company_tickers.json first, submissions tickers second."""
    js = get_json("https://www.sec.gov/files/company_tickers.json", CACHE / "company_tickers.json.gz")
    rows = [dict(cik=int(r["cik_str"]), ticker=str(r["ticker"]), order=i) for i, r in enumerate(js.values())]
    ct = pd.DataFrame(rows)
    ct["yf"] = ct.ticker.map(clean_ticker)
    ct = ct.dropna(subset=["yf"])
    ct["dash"] = ct.yf.str.contains("-").astype(int)
    ct = ct.sort_values(["cik", "dash", "order"]).drop_duplicates("cik")
    m = ct.set_index("cik")["yf"].rename("ticker").to_frame()
    m["ticker_src"] = "company_tickers"
    extra = []
    for cik, s in subs["sub_tickers"].items():
        if cik in m.index or not s:
            continue
        cands = [clean_ticker(x) for x in s.split("|")]
        cands = [c for c in cands if c]
        if cands:
            cands.sort(key=lambda c: ("-" in c))
            extra.append((cik, cands[0]))
    if extra:
        e = pd.DataFrame(extra, columns=["cik", "ticker"]).set_index("cik")
        e["ticker_src"] = "submissions"
        m = pd.concat([m, e])
    return m


IDX = CACHE / "filing_index"
IDX.mkdir(exist_ok=True)
_XSD = re.compile(r"^([a-z][a-z0-9]{0,9})-(\d{8})\.xsd$")


def recover_hist_tickers(F: pd.DataFrame, subs: pd.DataFrame, tmap: pd.DataFrame) -> pd.DataFrame:
    """Historical ticker for CIKs with no current ticker.

    EDGAR XBRL file names follow "{prefix}-{yyyymmdd}.xsd" where the prefix is
    conventionally the trading symbol. For every CIK without a current ticker we
    read the file list of its most recent annual filing in the frames data and
    take that prefix. This recovers companies that still trade under a new CIK
    after a holding-company reorganisation (e.g. Google Inc -> Alphabet, Exxon
    Mobil Corp -> ExxonMobil Holdings in 2026). Delisted companies' old symbols
    are recovered too but Yahoo generally has no data for them. A recovered
    symbol is only used where it passes the same checks as any other ticker plus
    the per-year duplicate rule in build_panel().
    """
    ok = subs[subs.sic.notna() & ~subs.sic.between(6000, 6999) & ~subs.sic.between(4900, 4999)].index
    need = sorted(set(ok) - set(tmap.index))
    last = (F[F.cik.isin(need)].dropna(subset=["rev_accn"]).sort_values("fy")
            .drop_duplicates("cik", keep="last").set_index("cik").rev_accn)
    log(f"historical tickers: {len(last)} CIKs without a current ticker")

    def one(item):
        cik, accn = item
        a = str(accn).replace("-", "")
        js = get_json(f"https://www.sec.gov/Archives/edgar/data/{cik}/{a}/index.json",
                      IDX / f"{cik}_{a}.json.gz")
        if not js or js == "FAILED":
            return cik, accn, None
        names = [i.get("name", "") for i in js.get("directory", {}).get("item", [])]
        for n in names:
            m = _XSD.match(n)
            if m:
                return cik, accn, m.group(1)
        return cik, accn, None

    rows = []
    with ThreadPoolExecutor(max_workers=6) as ex:
        for i, r in enumerate(ex.map(one, list(last.items())), 1):
            rows.append(r)
            if i % 500 == 0:
                log(f"  filing index {i}/{len(last)}")
    h = pd.DataFrame(rows, columns=["cik", "accn", "prefix"])
    h["hist_ticker"] = h.prefix.map(lambda x: clean_ticker(x.upper()) if isinstance(x, str) else None)
    return h.set_index("cik")


# --------------------------------------------------------------------------- #
# 3. Prices
# --------------------------------------------------------------------------- #
PX_LONG = PRICES / "monthly_long.parquet"
PX_STATUS = PRICES / "status.csv"


SENTINEL = "SPY"


def _download_chunk(tickers: list[str]):
    """One yf.download call. A sentinel symbol that always has data (SPY) is
    added to every request: if it comes back empty the whole call was rate
    limited or failed, and the caller retries instead of recording 'no data'."""
    import yfinance as yf
    req = list(dict.fromkeys(tickers + [SENTINEL]))
    try:
        df = yf.download(req, interval="1mo", start=PRICE_START, auto_adjust=False,
                         actions=True, progress=False, threads=True, group_by="column",
                         multi_level_index=True)
    except Exception as exc:  # noqa: BLE001
        return None, False
    ok = (df is not None and not df.empty and ("Adj Close", SENTINEL) in df.columns
          and df[("Adj Close", SENTINEL)].notna().sum() > 100)
    return df, ok


def fetch_prices(tickers: list[str], chunk: int = 100) -> dict:
    """Monthly OHLC + actions for every ticker, cached as a long parquet.

    Stored per (date, ticker): close (split-adjusted, not dividend-adjusted),
    adj (split + dividend adjusted = the auto_adjust=True close), split ratio.
    """
    have = pd.read_parquet(PX_LONG) if PX_LONG.exists() else pd.DataFrame(
        columns=["date", "ticker", "close", "adj", "split"])
    status = pd.read_csv(PX_STATUS) if PX_STATUS.exists() else pd.DataFrame(columns=["ticker", "status"])
    status = status.drop_duplicates("ticker", keep="last")
    done = set(status.loc[status.status.isin(["ok", "nodata"]), "ticker"])
    status = status[status.ticker.isin(done)]
    todo = [t for t in dict.fromkeys(tickers) if t not in done]
    log(f"prices: {len(tickers)} tickers requested, {len(todo)} not yet cached")
    new_frames, new_status = [], []
    rate_limited_total = 0
    for i in range(0, len(todo), chunk):
        part = todo[i:i + chunk]
        pending = list(part)
        for attempt in range(8):
            df, healthy = _download_chunk(pending)
            if not healthy:
                rate_limited_total += 1
                log(f"  chunk {i}: sentinel missing (rate limited?), backing off (attempt {attempt+1})")
                time.sleep(60 * (attempt + 1))
                continue
            got = []
            if df is not None and not df.empty:
                lvl0 = set(df.columns.get_level_values(0))
                for t in pending:
                    if ("Adj Close", t) not in df.columns:
                        continue
                    sub = pd.DataFrame({
                        "close": df[("Close", t)] if ("Close", t) in df.columns else np.nan,
                        "adj": df[("Adj Close", t)],
                        "split": df[("Stock Splits", t)] if ("Stock Splits", t) in df.columns else 0.0,
                    })
                    sub = sub.dropna(subset=["adj"])
                    if len(sub):
                        sub = sub.reset_index().rename(columns={"Date": "date"})
                        sub["ticker"] = t
                        new_frames.append(sub[["date", "ticker", "close", "adj", "split"]])
                        got.append(t)
            for t in got:
                new_status.append((t, "ok"))
            for t in pending:
                if t not in got:
                    new_status.append((t, "nodata"))
            break
        else:
            for t in pending:
                new_status.append((t, "failed"))
        log(f"  prices {min(i+chunk, len(todo))}/{len(todo)}")
        time.sleep(1.0)
        # checkpoint every 10 chunks
        if (i // chunk) % 10 == 9 or i + chunk >= len(todo):
            if new_frames:
                have = pd.concat([have] + new_frames, ignore_index=True)
                new_frames = []
            status = pd.concat([status, pd.DataFrame(new_status, columns=["ticker", "status"])],
                               ignore_index=True)
            new_status = []
            have["date"] = pd.to_datetime(have["date"])
            have.to_parquet(PX_LONG, index=False)
            status.to_csv(PX_STATUS, index=False)
    return {"n_requested": len(tickers), "status_counts": status.status.value_counts().to_dict(),
            "rate_limited_retries": rate_limited_total}


# --------------------------------------------------------------------------- #
# 4. Panel
# --------------------------------------------------------------------------- #
def fcs_for(group: pd.DataFrame) -> float:
    g = group.dropna(subset=["revenue", "cost"]).drop_duplicates("rev_end")
    if len(g) < 4:
        return np.nan
    x = g.revenue.to_numpy(float)
    yv = g.cost.to_numpy(float)
    if np.var(x) <= 0:
        return np.nan
    b = np.cov(x, yv, bias=True)[0, 1] / np.var(x)
    a = yv.mean() - b * x.mean()
    mc = yv.mean()
    if not np.isfinite(mc) or mc == 0:
        return np.nan
    return float(np.clip(a / mc, -1.0, 1.0))


def consecutive(end_a: pd.Series, end_b: pd.Series) -> pd.Series:
    """True where end_a is one fiscal year after end_b (300-430 days)."""
    d = (end_a - end_b).dt.days
    return d.between(300, 430)


def split_records(split: pd.DataFrame) -> dict:
    """ticker -> list of (month, ratio) Yahoo split records."""
    out = {}
    nz = split.stack()
    nz = nz[(nz > 0) & (nz != 1.0)]
    for (m, t), k in nz.items():
        out.setdefault(t, []).append((m, float(k)))
    return out


def refresh_subs_fields(subs: pd.DataFrame) -> pd.DataFrame:
    """Add 10-K / 20-F filing counts from the cached submissions files (no network)."""
    n10, n20 = {}, {}
    for cik in subs.index:
        p = SUBS / f"CIK{int(cik):010d}.json.gz"
        forms = []
        if p.exists():
            with gzip.open(p, "rt") as fh:
                js = json.loads(fh.read())
            if js:
                forms = js.get("filings", {}).get("recent", {}).get("form", [])
        n10[cik] = sum(f in ("10-K", "10-K405", "10-KT") for f in forms)
        n20[cik] = sum(f in ("20-F", "40-F") for f in forms)
    subs = subs.copy()
    subs["n_10k"] = pd.Series(n10)
    subs["n_20f"] = pd.Series(n20)
    subs.to_parquet(CACHE / "subs.parquet")
    return subs


def filing_date(cik: int, accn: str):
    """Filing date of an accession (from the EDGAR filing index, cached)."""
    a = str(accn).replace("-", "")
    js = get_json(f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{a}/index.json",
                  IDX / f"{int(cik)}_{a}.json.gz")
    if not js or js == "FAILED":
        return None
    ds = [i.get("last-modified") for i in js.get("directory", {}).get("item", []) if i.get("last-modified")]
    return pd.Timestamp(min(ds)[:10]) if ds else None


# us-gaap share counts (balance-sheet CommonStockSharesOutstanding, weighted
# average shares) are restated for splits in later filings, and the frames API
# returns the latest filing's number. Their split basis is therefore the filing
# date of the accession that supplied the value, looked up when a Yahoo split
# record falls within 27 months after the period end. dei cover-page counts are
# never restated; their basis is their own date.
RESTATABLE = ("gaap", "wanso")


def build_panel() -> tuple[pd.DataFrame, dict]:
    info = {}
    F = fundamentals_long()
    info["oi_period_mismatch_rows"] = int(F.oi_period_mismatch.sum())
    F["cost"] = F.revenue - F.opinc
    F["margin"] = F.opinc / F.revenue.where(F.revenue > 0)

    subs = pd.read_parquet(CACHE / "subs.parquet")
    if "n_20f" not in subs.columns:
        subs = refresh_subs_fields(subs)
    subs["foreign_filer"] = (subs.n_20f > 0) & (subs.n_10k == 0)
    info["foreign_filers"] = int(subs.foreign_filer.sum())
    tmap = pd.read_parquet(CACHE / "tickers.parquet")
    # a submissions-file ticker that company_tickers.json assigns to another CIK is dropped
    ct_tk = set(tmap.loc[tmap.ticker_src == "company_tickers", "ticker"])
    dup_sub = (tmap.ticker_src == "submissions") & tmap.ticker.isin(ct_tk)
    tmap = tmap[~dup_sub]
    info["submissions_tickers_dropped_as_dup"] = int(dup_sub.sum())
    # historical tickers (XBRL file prefix) for CIKs with no current ticker
    hp = CACHE / "hist_tickers.parquet"
    if hp.exists():
        h = pd.read_parquet(hp).dropna(subset=["hist_ticker"])
        h = h[~h.index.isin(tmap.index)]
        h = h.rename(columns={"hist_ticker": "ticker"})[["ticker"]].assign(ticker_src="hist")
        tmap = pd.concat([tmap, h])
    # current holder of every symbol (all SEC tickers, any industry)
    js = get_json("https://www.sec.gov/files/company_tickers.json", CACHE / "company_tickers.json.gz")
    holder = {}
    for r in js.values():
        c = clean_ticker(str(r["ticker"]))
        if c and c not in holder:
            holder[c] = int(r["cik_str"])
    filers_by_fy = {y: set(F.loc[F.fy == y, "cik"]) for y in YEARS}

    px = pd.read_parquet(PX_LONG)
    px["date"] = pd.to_datetime(px["date"]).dt.to_period("M").dt.to_timestamp()
    px = px.drop_duplicates(["date", "ticker"], keep="last")
    close = px.pivot(index="date", columns="ticker", values="close").sort_index()
    adj = px.pivot(index="date", columns="ticker", values="adj").sort_index()
    info["nonpositive_adj_prices_set_missing"] = int((adj <= 0).sum().sum())
    adj = adj.where(adj > 0)
    close = close.where(close > 0)
    split = px.pivot(index="date", columns="ticker", values="split").sort_index().fillna(0.0)
    recs_split = split_records(split)
    # monthly total return, only between two consecutive valid month-ends
    ret = adj / adj.shift(1) - 1
    last_valid = adj.apply(lambda s: s.last_valid_index())
    first_valid = adj.apply(lambda s: s.first_valid_index())
    data_end = adj.index.max()
    def split_factor(cik, tick, after):
        """Product of Yahoo split factors after the share-count month."""
        am = after.to_period("M").to_timestamp()
        f = 1.0
        for m, k in recs_split.get(tick, []):
            if m > am:
                f *= k
        return f

    recs = []
    keys = list(SHARE_SOURCES)
    n_fd_lookups = [0]
    for t in FORMATIONS:
        y1 = t - 1
        base = F[F.fy == y1].set_index("cik")
        lag = {k: F[F.fy == y1 - k].set_index("cik") for k in (1, 2)}
        lead = F[F.fy == t].set_index("cik")
        cols = ["revenue", "rev_tag", "rev_end", "rev_start", "rev_accn", "opinc", "cost", "margin",
                "assets", "assets_end", "pfloat", "pfloat_end"] + \
            [f"sh_{k}" for k in keys] + [f"sh_{k}_end" for k in keys] + [f"sh_{k}_accn" for k in keys]
        df = base[cols].copy()
        df["year"] = t
        n_raw = len(df)
        # --- look-ahead guard
        cutoff = pd.Timestamp(t, 3, 1) - pd.Timedelta(days=1)
        df["late_fye"] = df.rev_end > cutoff
        # --- lags
        r1 = lag[1].reindex(df.index)
        r2 = lag[2].reindex(df.index)
        ok1 = consecutive(df.rev_end, r1.rev_end) & (r1.revenue > 0)
        ok2 = consecutive(r1.rev_end, r2.rev_end) & (r2.revenue > 0) & ok1
        df["rev_growth"] = np.where(ok1, df.revenue / r1.revenue - 1, np.nan)
        df["rev_growth_prev"] = np.where(ok2, r1.revenue / r2.revenue - 1, np.nan)
        df["accel"] = df.rev_growth - df.rev_growth_prev
        df["margin_prev"] = np.where(ok1, r1.margin, np.nan)
        df["margin_chg_pp"] = 100 * (df.margin - df.margin_prev)
        df["OL"] = np.where(df.assets > 0, df.cost / df.assets, np.nan)
        # --- FCS over fiscal years t-5..t-1 (>= 4 of 5)
        hist = F[(F.fy >= t - 5) & (F.fy <= t - 1) & F.cik.isin(df.index)][["cik", "revenue", "cost", "rev_end"]]
        fcs = hist.groupby("cik").apply(fcs_for, include_groups=False)
        df["FCS"] = fcs.reindex(df.index)
        # --- forward fundamentals (CY t vs CY t-1)
        ld = lead.reindex(df.index)
        okf = consecutive(ld.rev_end, df.rev_end) & (df.revenue > 0)
        df["fwd_margin_chg_pp"] = np.where(okf, 100 * (ld.margin - df.margin), np.nan)
        df["fwd_rev_growth"] = np.where(okf, ld.revenue / df.revenue - 1, np.nan)
        df["fwd_growth_chg"] = df.fwd_rev_growth - df.rev_growth
        # --- SIC + ticker
        df = df.join(subs[["sic", "name", "entity_type", "foreign_filer"]], how="left")
        df = df.join(tmap, how="left")
        df["sic2"] = (df.sic // 100)
        fin = df.sic.between(6000, 6999)
        util = df.sic.between(4900, 4999)
        df["sic_ok"] = df.sic.notna() & ~fin & ~util
        # foreign private issuers (20-F/40-F annual reports, no 10-K): their SEC share
        # counts are ordinary shares while Yahoo prices the ADS, so market cap and
        # the size filter cannot be computed; excluded from the study (counted).
        df["foreign_filer"] = df.foreign_filer.fillna(False).astype(bool)
        df["fund_ok"] = (~df.late_fye) & df.sic_ok & ~df.foreign_filer & (df.revenue > REV_MIN) & (df.assets > 0)
        # historical symbol is not used in a year when its current holder (another CIK) was itself filing
        ish = df.ticker_src == "hist"
        clash = ish & df.apply(lambda r: r.ticker in holder and holder[r.ticker] != r.name
                               and holder[r.ticker] in filers_by_fy.get(y1, set()), axis=1)
        df.loc[clash, ["ticker", "ticker_src"]] = [None, None]
        # per-year duplicate symbols among fundamentals-eligible rows: current mapping wins
        cand = df[df.fund_ok & df.ticker.notna()]
        dd = cand[cand.ticker.duplicated(keep=False)]
        drop = dd[dd.ticker_src == "hist"].index.tolist()
        rest = dd.drop(index=drop)
        drop += rest[rest.ticker.duplicated(keep=False)].index.tolist()
        df.loc[drop, ["ticker", "ticker_src"]] = [None, None]
        df["hist_ticker_clash"] = clash
        # --- price at formation (June of year t)
        fdate = pd.Timestamp(t, 6, 1)
        tk = df.ticker
        has_series = tk.isin(adj.columns)
        c_f = pd.Series(np.nan, index=df.index)
        a_f = pd.Series(np.nan, index=df.index)
        if fdate in adj.index:
            idx = df.index[has_series]
            c_f.loc[idx] = close.loc[fdate, tk[idx]].to_numpy()
            a_f.loc[idx] = adj.loc[fdate, tk[idx]].to_numpy()
        df["price_june"] = c_f
        df["priced"] = a_f.notna() & c_f.notna() & (c_f > 0)
        # --- shares: first source (priority order) passing the sanity band
        df["shares"] = np.nan
        df["shares_end"] = pd.NaT
        df["shares_src"] = None
        df["split_factor"] = np.nan
        df["shares_rejected_sources"] = 0
        size_base = np.maximum(df.revenue.fillna(0), df.assets.fillna(0))
        for cik in df.index[df.priced & df.fund_ok]:
            tick = tk[cik]
            cands = []   # (source, value, date, split factor, shares on today's split basis)
            for k in keys:
                v = df.at[cik, f"sh_{k}"]
                e = df.at[cik, f"sh_{k}_end"]
                if not (np.isfinite(v) and v > 0) or pd.isna(e):
                    continue
                basis = e
                if k in RESTATABLE:
                    em = e.to_period("M").to_timestamp()
                    if any(em < m <= em + pd.DateOffset(months=27) for m, _ in recs_split.get(tick, [])):
                        fd = filing_date(cik, df.at[cik, f"sh_{k}_accn"])
                        n_fd_lookups[0] += 1
                        if fd is not None:
                            basis = max(e, fd)
                f = split_factor(cik, tick, basis)
                cands.append((k, v, e, f, v * f))
            # consistency: a source within 3x of at least one other source
            cons = [any(j != i and abs(math.log(c[4] / d[4])) <= math.log(3.0)
                        for j, d in enumerate(cands)) for i, c in enumerate(cands)]
            any_cons = any(cons)
            nrej = 0
            for i, (k, v, e, f, sb) in enumerate(cands):
                mc = sb * df.at[cik, "price_june"]
                ratio = mc / size_base[cik] if size_base[cik] > 0 else np.nan
                if MCAP_RATIO_BAND[0] <= ratio <= MCAP_RATIO_BAND[1] and (cons[i] or not any_cons):
                    df.at[cik, "shares"] = v
                    df.at[cik, "shares_end"] = e
                    df.at[cik, "shares_src"] = k
                    df.at[cik, "split_factor"] = f
                    break
                nrej += 1
            df.at[cik, "shares_rejected_sources"] = nrej
        df["mcap"] = df.shares * df.split_factor * df.price_june
        # recovered historical symbols must agree with the company's own public float
        fr_ = df.pfloat / df.mcap
        bad_hist = (df.ticker_src == "hist") & df.priced & ~fr_.between(*HIST_FLOAT_BAND)
        df["hist_ticker_rejected"] = bad_hist
        df.loc[bad_hist, "priced"] = False
        df.loc[bad_hist, ["mcap", "shares", "split_factor"]] = np.nan
        df["size"] = np.where(df.mcap >= 2e9, "large", np.where(df.mcap.notna(), "small", None))
        df["in_univ"] = df.fund_ok & df.priced & (df.mcap >= MCAP_MIN)
        # a Yahoo series that only starts after the formation date = not yet listed
        # (e.g. an SEC registrant that IPO'd later): not a survivorship casualty,
        # counted separately and kept out of the missing set.
        fv = pd.to_datetime(first_valid.reindex(tk.fillna("")).to_numpy())
        df["not_yet_listed"] = df.fund_ok & ~df.priced & has_series & (pd.Series(fv, index=df.index) > fdate)
        df["missing"] = df.fund_ok & ~df.priced & ~df.not_yet_listed
        df["missing_reason"] = np.where(
            ~df.missing, "",
            np.where(df.ticker.isna(), "no_ticker",
                     np.where(df.hist_ticker_rejected, "hist_ticker_failed_float_check",
                              np.where(~has_series, "ticker_no_yahoo_data", "no_price_at_formation"))))
        df["priced_no_shares"] = df.fund_ok & df.priced & df.shares.isna()
        # --- forward returns, July t .. June t+1
        months = pd.date_range(pd.Timestamp(t, 7, 1), pd.Timestamp(t + 1, 6, 1), freq="MS")
        months = [m for m in months if m in ret.index]
        fr = pd.Series(np.nan, index=df.index)
        nm = pd.Series(0, index=df.index)
        ended = pd.Series(False, index=df.index)
        idx = df.index[df.priced]
        if months and len(idx):
            R = ret.loc[months, tk[idx]]
            R.columns = idx
            nm.loc[idx] = R.notna().sum().to_numpy()
            gross = (1 + R).prod(min_count=1)
            fr.loc[idx] = (gross - 1).to_numpy()
            lv = last_valid.reindex(tk[idx]).to_numpy()
            ended.loc[idx] = pd.to_datetime(lv) < min(pd.Timestamp(t + 1, 6, 1), data_end)
        df["fwd_ret_12m"] = fr
        df["n_fwd_months"] = nm
        df["series_ended_in_hold"] = ended
        df["n_frame_rows"] = n_raw
        recs.append(df.reset_index())
        log(f"  formation {t}: CY{y1} rows {n_raw}, fund_ok {int(df.fund_ok.sum())}, "
            f"priced {int((df.fund_ok & df.priced).sum())}, universe {int(df.in_univ.sum())} "
            f"(hist-ticker {int((df.in_univ & (df.ticker_src == 'hist')).sum())}), "
            f"missing {int(df.missing.sum())}, no reliable shares {int(df.priced_no_shares.sum())}, "
            f"late FYE dropped {int((df.late_fye & df.sic_ok).sum())}")
    P = pd.concat(recs, ignore_index=True)
    info["split_records_used"] = int(sum(len(v) for v in recs_split.values()))
    info["filing_date_lookups_for_restated_share_counts"] = n_fd_lookups[0]
    # monthly returns matrix for the tests (only tickers that are ever held) + benchmarks
    held = set(P.loc[P.fund_ok & P.priced, "ticker"].dropna()) | set(BENCH)
    R = ret[[c for c in ret.columns if c in held]]
    R.to_parquet(CACHE / "returns.parquet")
    return P, info

def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", default="all", choices=["frames", "subs", "hist", "prices", "panel", "all"])
    a = ap.parse_args(argv)
    logp = CACHE / "build_log.json"
    blog = json.loads(logp.read_text()) if logp.exists() else {}

    if a.stage in ("frames", "all"):
        blog["frames"] = fetch_frames()
        logp.write_text(json.dumps(blog, indent=1, default=str))

    if a.stage in ("subs", "all"):
        F = fundamentals_long()
        keep = F[(F.fy.between(2010, 2024)) & (F.revenue > REV_MIN) & (F.assets > 0)]
        ciks = sorted(keep.cik.unique().tolist())
        subs, failed = fetch_submissions(ciks)
        subs.to_parquet(CACHE / "subs.parquet")
        tm = ticker_map(subs)
        tm = tm[tm.index.isin(ciks)]
        tm.to_parquet(CACHE / "tickers.parquet")
        blog["subs"] = {"n_ciks": len(ciks), "n_with_subs": len(subs), "failed": failed,
                        "n_with_ticker": int(len(tm)),
                        "ticker_src": tm.ticker_src.value_counts().to_dict()}
        logp.write_text(json.dumps(blog, indent=1, default=str))

    if a.stage in ("hist", "all"):
        F = fundamentals_long()
        subs = pd.read_parquet(CACHE / "subs.parquet")
        tm = pd.read_parquet(CACHE / "tickers.parquet")
        h = recover_hist_tickers(F, subs, tm)
        h.to_parquet(CACHE / "hist_tickers.parquet")
        blog["hist"] = {"n_ciks": int(len(h)), "n_prefix": int(h.prefix.notna().sum()),
                        "n_ticker": int(h.hist_ticker.notna().sum())}
        logp.write_text(json.dumps(blog, indent=1, default=str))

    if a.stage in ("prices", "all"):
        subs = pd.read_parquet(CACHE / "subs.parquet")
        tm = pd.read_parquet(CACHE / "tickers.parquet")
        ok = subs[subs.sic.notna() & ~subs.sic.between(6000, 6999) & ~subs.sic.between(4900, 4999)]
        tickers = BENCH + sorted(tm[tm.index.isin(ok.index)].ticker.unique().tolist())
        hp = CACHE / "hist_tickers.parquet"
        if hp.exists():
            h = pd.read_parquet(hp)
            tickers += sorted(set(h.hist_ticker.dropna()) - set(tickers))
        blog["prices"] = fetch_prices(tickers)
        logp.write_text(json.dumps(blog, indent=1, default=str))

    if a.stage in ("panel", "all"):
        P, info = build_panel()
        blog["panel"] = info
        out = P[["cik", "ticker", "ticker_src", "name", "sic", "sic2", "year", "rev_end", "rev_tag",
                 "rev_accn", "revenue", "opinc", "cost", "margin", "assets", "shares", "shares_src",
                 "shares_end", "shares_rejected_sources", "split_factor", "price_june", "mcap", "pfloat",
                 "size", "OL", "FCS",
                 "rev_growth", "rev_growth_prev", "accel", "margin_prev", "margin_chg_pp",
                 "fwd_margin_chg_pp", "fwd_rev_growth", "fwd_growth_chg", "fwd_ret_12m",
                 "n_fwd_months", "series_ended_in_hold", "late_fye", "sic_ok", "fund_ok", "priced",
                 "priced_no_shares", "in_univ", "missing", "missing_reason", "not_yet_listed",
                 "hist_ticker_clash", "hist_ticker_rejected", "foreign_filer"]]
        out.to_parquet(HERE / "panel.parquet", index=False)
        logp.write_text(json.dumps(blog, indent=1, default=str))
        log(f"wrote {HERE/'panel.parquet'} ({len(out)} rows)")


if __name__ == "__main__":
    main()
