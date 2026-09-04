#!/usr/bin/env python3
"""
Deep-value fundamentals screener for US small/mid-cap stocks.

Free sources only:
  * SEC company_tickers.json          -> CIK <-> ticker map
  * SEC XBRL "frames" API             -> one request per concept for ALL filers
  * SEC submissions API               -> SIC code (only for the post-liquidity set)
  * yfinance                          -> prices / volume (filtered set only)

Outputs:
  research/deepvalue/candidates.csv
  research/deepvalue/CANDIDATES.md

Run: .venv/bin/python research/deepvalue/screen.py
Research output only -- not investment advice.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
import threading
import time
import datetime as dt
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np
import pandas as pd
import requests
import yfinance as yf

# --------------------------------------------------------------------------- #
# Config
# --------------------------------------------------------------------------- #
HERE = Path(__file__).resolve().parent
DATA = HERE / "data"
FRAMES = DATA / "frames"
SUBS = DATA / "submissions"
for d in (DATA, FRAMES, SUBS):
    d.mkdir(parents=True, exist_ok=True)

UA = "ClaudeSpace research dspinjr@gmail.com"
HEADERS = {"User-Agent": UA, "Accept-Encoding": "gzip, deflate"}
CACHE_DAYS = 7
MIN_REQ_INTERVAL = 1.0 / 7.0  # <= ~7 req/s, SEC asks for <=10

MKTCAP_MIN, MKTCAP_MAX = 100e6, 5_000e6
ADV_MIN = 1e6
REV_MIN = 20e6
TOP_N = 40
# Wider band written by --universe-out: every operating company a cloud agent
# might research. Deliberately overlaps but does not equal the candidate band.
UNIVERSE_MIN, UNIVERSE_MAX = 50e6, 2_000e6

# Latest completed fiscal year available in the frames API, newest first.
ANNUAL_PERIODS = ["CY2025", "CY2024"]
PRIOR_OF = {"CY2025": "CY2024", "CY2024": "CY2023"}
# Instant periods, newest first (first hit per CIK wins).
INSTANT_PERIODS = ["CY2026Q2I", "CY2026Q1I", "CY2025Q4I"]
# Same instant one year earlier, for share-count change.
INSTANT_PERIODS_PY = ["CY2025Q2I", "CY2025Q1I", "CY2024Q4I"]
# Share-count tags, in fallback order. dei:EntityCommonStockSharesOutstanding is
# the cover-page count and is the primary source, but it is missing or tagged as
# zero for a meaningful minority of filers (e.g. DEC reported 0 for CY2024Q4I and
# filed nothing at all for CY2025Q1I/Q2I), which silently blanked share_chg while
# rev_growth showed +141% from an acquisition. Two fallbacks close that hole.
SHARES_ALT_TAG = "CommonStockSharesOutstanding"                     # instant, us-gaap
WANSO_TAG = "WeightedAverageNumberOfSharesOutstandingBasic"         # duration, us-gaap
# Share-count growth above this is flagged next to revenue growth: revenue that
# grew alongside a much larger share count is bought growth, not organic growth.
SHARE_GROWTH_FLAG = 0.15

# Quarters summed for a TTM fallback when no annual frame exists (non-Dec FY ends).
TTM_QUARTERS = ["CY2025Q3", "CY2025Q4", "CY2026Q1", "CY2026Q2"]

REV_TAGS = [
    "Revenues",
    "RevenueFromContractWithCustomerExcludingAssessedTax",
    "SalesRevenueNet",
]
DUR_TAGS = {
    "revenue": REV_TAGS,
    "net_income": ["NetIncomeLoss"],
    "op_income": ["OperatingIncomeLoss"],
    "cfo": ["NetCashProvidedByUsedInOperatingActivities"],
    "capex": ["PaymentsToAcquirePropertyPlantAndEquipment",
              "PaymentsToAcquireProductiveAssets",
              "PaymentsToAcquirePropertyPlantAndEquipmentExcludingCapitalizedInterest"],
}
INST_TAGS = {
    "equity": ["StockholdersEquity"],
    "assets": ["Assets"],
    # Long-term debt is tagged inconsistently; LongTermDebtNoncurrent alone covers
    # only ~1/3 of filers, which silently understates EV. Wide fallback chain:
    "ltd": ["LongTermDebtNoncurrent", "LongTermDebt",
            "LongTermDebtAndCapitalLeaseObligations",
            "DebtLongtermAndShorttermCombinedAmount",
            "LongTermNotesPayable", "LongTermLineOfCredit",
            "ConvertibleLongTermNotesPayable", "SecuredLongTermDebt"],
    # last fallback is the cash-flow-statement total (includes restricted cash);
    # used only when the plain cash tag is absent, which beats assuming zero
    "cash": ["CashAndCashEquivalentsAtCarryingValue",
             "CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents"],
}

# SIC exclusions: 6000-6799 = banks, credit, brokers, insurers, real estate, REITs,
# blank-check/holding companies. Screened metrics (EV/EBIT, FCF, ROIC) are
# meaningless for these.
SIC_EXCLUDE_RANGES = [(6000, 6799)]
# Drug/biotech SIC codes -- kept only if they have real revenue (REV_MIN applies
# to everyone, so pre-revenue biotech is already excluded; these are dropped when
# revenue is below 3x the general floor, i.e. still essentially clinical-stage).
SIC_BIOTECH = {2833, 2834, 2836, 8731}
BIOTECH_REV_MIN = 60e6

# yfinance can't price these; SEC tickers use a '-' class/warrant separator.
BAD_SUFFIXES = {"W", "WS", "WT", "U", "UN", "R", "RT", "RTS", "P", "PR"}

_last_req = [0.0]
_req_lock = threading.Lock()


def log(msg: str) -> None:
    print(f"[{dt.datetime.now():%H:%M:%S}] {msg}", flush=True)


def _throttle() -> None:
    with _req_lock:
        delta = time.time() - _last_req[0]
        if delta < MIN_REQ_INTERVAL:
            time.sleep(MIN_REQ_INTERVAL - delta)
        _last_req[0] = time.time()


def get_json(url: str, cache: Path, tries: int = 3):
    """Fetch JSON with an on-disk cache (reused if < CACHE_DAYS old)."""
    if cache.exists():
        age = time.time() - cache.stat().st_mtime
        if age < CACHE_DAYS * 86400:
            try:
                return json.loads(cache.read_text())
            except Exception:
                pass
    for attempt in range(tries):
        try:
            _throttle()
            r = requests.get(url, headers=HEADERS, timeout=60)
            if r.status_code == 404:
                cache.write_text("null")
                return None
            r.raise_for_status()
            cache.write_text(r.text)
            return r.json()
        except Exception as exc:  # noqa: BLE001
            if attempt == tries - 1:
                log(f"  ! failed {url}: {exc}")
                return None
            time.sleep(1.5 * (attempt + 1))
    return None


# --------------------------------------------------------------------------- #
# 1. Ticker universe
# --------------------------------------------------------------------------- #
def clean_ticker(t: str) -> str | None:
    t = (t or "").strip().upper()
    if not t or "." in t or " " in t:
        return None
    if "-" in t:
        base, _, suf = t.partition("-")
        if suf in BAD_SUFFIXES or len(suf) > 2:
            return None  # warrants / units / rights / preferreds
    if len(t) > 6:
        return None
    return t


def load_universe() -> pd.DataFrame:
    """cik -> primary ticker + name. First occurrence in SEC's (cap-ordered) file wins."""
    js = get_json(
        "https://www.sec.gov/files/company_tickers.json", DATA / "company_tickers.json"
    )
    rows = []
    for i, rec in enumerate(js.values()):
        rows.append(
            dict(cik=int(rec["cik_str"]), ticker=str(rec["ticker"]), name=rec["title"], order=i)
        )
    df = pd.DataFrame(rows)
    df["yf"] = df.ticker.map(clean_ticker)
    n_all = len(df)
    df = df.dropna(subset=["yf"])
    # one row per CIK: prefer a ticker with no class suffix, then file order
    df["has_dash"] = df.yf.str.contains("-").astype(int)
    df = df.sort_values(["cik", "has_dash", "order"]).drop_duplicates("cik", keep="first")
    log(f"SEC company_tickers: {n_all} ticker rows -> {len(df)} unique CIKs after cleaning")
    return df.set_index("cik")[["ticker", "yf", "name"]]


# --------------------------------------------------------------------------- #
# 2. XBRL frames
# --------------------------------------------------------------------------- #
def frame(taxonomy: str, tag: str, unit: str, period: str) -> pd.Series:
    """cik -> value for one concept/period. Empty series if unavailable."""
    url = f"https://data.sec.gov/api/xbrl/frames/{taxonomy}/{tag}/{unit}/{period}.json"
    js = get_json(url, FRAMES / f"{taxonomy}_{tag}_{unit}_{period}.json")
    if not js or "data" not in js:
        return pd.Series(dtype="float64")
    d = js["data"]
    s = pd.Series({int(r["cik"]): float(r["val"]) for r in d if r.get("val") is not None})
    if unit == "shares":
        s = s[s > 0]
    s.index.name = "cik"
    return s


def frame_ends(taxonomy: str, tag: str, unit: str, period: str) -> pd.Series:
    url = f"https://data.sec.gov/api/xbrl/frames/{taxonomy}/{tag}/{unit}/{period}.json"
    js = get_json(url, FRAMES / f"{taxonomy}_{tag}_{unit}_{period}.json")
    if not js or "data" not in js:
        return pd.Series(dtype="object")
    return pd.Series({int(r["cik"]): r.get("end") for r in js["data"]})


def coalesce(series_list: list[pd.Series]) -> pd.Series:
    """First non-null value per CIK, in list order."""
    out = pd.Series(dtype="float64")
    for s in series_list:
        if s.empty:
            continue
        out = out.combine_first(s) if not out.empty else s.copy()
    return out


def prefetch_all() -> None:
    """Warm the frame cache (sequential, throttled). Prints progress."""
    jobs = []
    for tags in DUR_TAGS.values():
        for tag in tags:
            for p in ANNUAL_PERIODS + ["CY2023"]:
                jobs.append(("us-gaap", tag, "USD", p))
            for q in TTM_QUARTERS:
                jobs.append(("us-gaap", tag, "USD", q))
    for tags in INST_TAGS.values():
        for tag in tags:
            for p in INSTANT_PERIODS:
                jobs.append(("us-gaap", tag, "USD", p))
    for p in INSTANT_PERIODS + INSTANT_PERIODS_PY:
        jobs.append(("dei", "EntityCommonStockSharesOutstanding", "shares", p))
        jobs.append(("us-gaap", SHARES_ALT_TAG, "shares", p))
    for p in ANNUAL_PERIODS + ["CY2023"]:
        jobs.append(("us-gaap", WANSO_TAG, "shares", p))
    jobs = list(dict.fromkeys(jobs))
    log(f"fetching {len(jobs)} XBRL frames (cache: {FRAMES})")
    for i, (tax, tag, unit, per) in enumerate(jobs, 1):
        cache = FRAMES / f"{tax}_{tag}_{unit}_{per}.json"
        fresh = cache.exists() and time.time() - cache.stat().st_mtime < CACHE_DAYS * 86400
        get_json(
            f"https://data.sec.gov/api/xbrl/frames/{tax}/{tag}/{unit}/{per}.json", cache
        )
        if i % 10 == 0 or i == len(jobs):
            log(f"  frames {i}/{len(jobs)} (last: {tag} {per}{' cached' if fresh else ''})")


def annual_concept(name: str) -> tuple[pd.Series, pd.Series, pd.Series]:
    """
    Latest fiscal-year value per CIK, the period label used, and the prior-year value.
    Preference: CY2025 annual -> CY2024 annual -> TTM (sum of 4 quarterly frames).
    """
    tags = DUR_TAGS[name]
    by_period = {p: coalesce([frame("us-gaap", t, "USD", p) for t in tags])
                 for p in ANNUAL_PERIODS + ["CY2023"]}
    latest = pd.Series(dtype="float64")
    period = pd.Series(dtype="object")
    prior = pd.Series(dtype="float64")
    for p in ANNUAL_PERIODS:
        s = by_period[p]
        new = s[~s.index.isin(latest.index)] if not latest.empty else s
        if new.empty:
            continue
        latest = pd.concat([latest, new])
        period = pd.concat([period, pd.Series(p, index=new.index)])
        pp = by_period.get(PRIOR_OF[p], pd.Series(dtype="float64"))
        prior = pd.concat([prior, pp.reindex(new.index)])
    # TTM fallback for filers whose fiscal year does not align with a calendar frame
    qs = [coalesce([frame("us-gaap", t, "USD", q) for t in tags]) for q in TTM_QUARTERS]
    qdf = pd.concat(qs, axis=1) if any(not q.empty for q in qs) else pd.DataFrame()
    if not qdf.empty:
        ttm = qdf.dropna(how="any").sum(axis=1)
        add = ttm[~ttm.index.isin(latest.index)]
        if not add.empty:
            latest = pd.concat([latest, add])
            period = pd.concat([period, pd.Series("TTM(4Q)", index=add.index)])
            prior = pd.concat([prior, pd.Series(np.nan, index=add.index)])
    return latest, period, prior


def instant_concept(name: str, periods: list[str]) -> tuple[pd.Series, pd.Series, pd.Series]:
    """Latest available instant value per CIK, plus the period and the tag used."""
    tags = INST_TAGS[name]
    val = pd.Series(dtype="float64")
    per = pd.Series(dtype="object")
    src = pd.Series(dtype="object")
    for p in periods:
        merged = pd.Series(dtype="float64")
        tagof = pd.Series(dtype="object")
        for t in tags:
            fr = frame("us-gaap", t, "USD", p)
            if fr.empty:
                continue
            new_t = fr[~fr.index.isin(merged.index)] if not merged.empty else fr
            if new_t.empty:
                continue
            merged = pd.concat([merged, new_t])
            tagof = pd.concat([tagof, pd.Series(t, index=new_t.index)])
        if merged.empty:
            continue
        new = merged[~merged.index.isin(val.index)] if not val.empty else merged
        if new.empty:
            continue
        val = pd.concat([val, new])
        per = pd.concat([per, pd.Series(p, index=new.index)])
        src = pd.concat([src, tagof.reindex(new.index)])
    return val, per, src


def shares_concept(periods: list[str]) -> tuple[pd.Series, pd.Series]:
    val = pd.Series(dtype="float64")
    per = pd.Series(dtype="object")
    for p in periods:
        s = frame("dei", "EntityCommonStockSharesOutstanding", "shares", p)
        if s.empty:
            continue
        new = s[~s.index.isin(val.index)] if not val.empty else s
        if new.empty:
            continue
        val = pd.concat([val, new])
        per = pd.concat([per, pd.Series(p, index=new.index)])
    return val, per


def alt_shares_concept(periods: list[str]) -> tuple[pd.Series, pd.Series]:
    """us-gaap:CommonStockSharesOutstanding over the same instant windows.

    Used only where the dei cover-page count is absent, and always compared
    against itself (current vs prior instant) so the two sides of share_chg come
    from the same tag - a dei count covers every class, this one sometimes only
    one, so the two must never be mixed inside a single ratio.
    """
    val = pd.Series(dtype="float64")
    per = pd.Series(dtype="object")
    for p in periods:
        s = frame("us-gaap", SHARES_ALT_TAG, "shares", p)
        if s.empty:
            continue
        new = s[~s.index.isin(val.index)] if not val.empty else s
        if new.empty:
            continue
        val = pd.concat([val, new])
        per = pd.concat([per, pd.Series(p, index=new.index)])
    return val, per


def wanso_yoy() -> tuple[pd.Series, pd.Series]:
    """Year-over-year change in weighted-average basic shares, and the label.

    Last-resort fallback: an income-statement concept, so it exists whenever EPS
    does, and both sides come from the same annual frame pair.
    """
    by = {p: frame("us-gaap", WANSO_TAG, "shares", p)
          for p in ANNUAL_PERIODS + ["CY2023"]}
    chg = pd.Series(dtype="float64")
    lab = pd.Series(dtype="object")
    for p in ANNUAL_PERIODS:
        cur, pri = by.get(p), by.get(PRIOR_OF[p])
        if cur is None or cur.empty or pri is None or pri.empty:
            continue
        common = cur.index.intersection(pri.index).difference(chg.index)
        if len(common) == 0:
            continue
        ratio = cur.reindex(common) / pri.reindex(common) - 1.0
        ratio = ratio[np.isfinite(ratio)]
        chg = pd.concat([chg, ratio])
        lab = pd.concat([lab, pd.Series(f"{p} vs {PRIOR_OF[p]}", index=ratio.index)])
    return chg, lab


# --------------------------------------------------------------------------- #
# 3. SIC codes (only for the already-narrowed set)
# --------------------------------------------------------------------------- #
def fetch_sic(ciks: list[int]) -> pd.DataFrame:
    log(f"fetching SIC codes for {len(ciks)} companies (submissions endpoint)")
    out = {}

    def one(cik: int):
        cache = SUBS / f"CIK{cik:010d}.json"
        if cache.exists() and time.time() - cache.stat().st_mtime < CACHE_DAYS * 86400:
            try:
                js = json.loads(cache.read_text())
            except Exception:
                js = None
        else:
            js = None
        if js is None:
            js = get_json(f"https://data.sec.gov/submissions/CIK{cik:010d}.json", cache)
        if not js:
            return cik, None
        return cik, dict(
            sic=int(js.get("sic") or 0) if str(js.get("sic") or "").isdigit() else 0,
            sic_desc=js.get("sicDescription") or "",
            exchange=",".join([e for e in (js.get("exchanges") or []) if e]),
            entity_type=js.get("entityType") or "",
            fy_end=js.get("fiscalYearEnd") or "",
        )

    with ThreadPoolExecutor(max_workers=5) as ex:
        for i, (cik, rec) in enumerate(ex.map(one, ciks), 1):
            if rec:
                out[cik] = rec
            if i % 100 == 0:
                log(f"  submissions {i}/{len(ciks)}")
    df = pd.DataFrame.from_dict(out, orient="index")
    df.index.name = "cik"
    return df


# --------------------------------------------------------------------------- #
# 4. Prices
# --------------------------------------------------------------------------- #
def fetch_prices(tickers: list[str]) -> pd.DataFrame:
    log(f"yfinance: downloading 400d of prices for {len(tickers)} tickers")
    closes, adjs, vols = [], [], []
    chunk = 300
    for i in range(0, len(tickers), chunk):
        part = tickers[i : i + chunk]
        try:
            df = yf.download(
                part, period="400d", auto_adjust=False, progress=False,
                threads=True, group_by="column", actions=False,
            )
        except Exception as exc:  # noqa: BLE001
            log(f"  ! chunk {i} failed: {exc}")
            continue
        if df is None or df.empty:
            continue
        if not isinstance(df.columns, pd.MultiIndex):
            df.columns = pd.MultiIndex.from_product([df.columns, part])
        lvl0 = set(df.columns.get_level_values(0))
        closes.append(df["Close"])
        adjs.append(df["Adj Close"] if "Adj Close" in lvl0 else df["Close"])
        vols.append(df["Volume"])
        log(f"  prices {min(i+chunk, len(tickers))}/{len(tickers)}")
    if not closes:
        raise SystemExit("no price data")
    close = pd.concat(closes, axis=1)
    adj = pd.concat(adjs, axis=1)
    vol = pd.concat(vols, axis=1)
    close = close.loc[:, ~close.columns.duplicated()].sort_index()
    adj = adj.loc[:, ~adj.columns.duplicated()].sort_index()
    vol = vol.loc[:, ~vol.columns.duplicated()].sort_index()
    close = close.dropna(how="all")
    adj = adj.reindex(close.index)
    vol = vol.reindex(close.index)

    rows = []
    for t in close.columns:
        c = close[t].dropna()
        a = adj[t].dropna()
        v = vol[t].reindex(c.index)
        if len(c) < 130 or len(a) < 130:
            continue
        px = float(c.iloc[-1])
        if not np.isfinite(px) or px <= 0:
            continue
        dollar = (c * v).dropna()
        adv20 = float(dollar.iloc[-20:].mean()) if len(dollar) >= 20 else np.nan
        r6m = float(a.iloc[-1] / a.iloc[-127] - 1) if len(a) >= 127 else np.nan
        mom = float(a.iloc[-22] / a.iloc[-253] - 1) if len(a) >= 253 else np.nan
        hi52 = float(a.iloc[-252:].max())
        rows.append(
            dict(yf=t, price=px, adv20=adv20, r6m=r6m, mom_12_1=mom,
                 off_52w_high=float(a.iloc[-1] / hi52 - 1) if hi52 > 0 else np.nan,
                 n_days=len(c))
        )
    out = pd.DataFrame(rows).set_index("yf")
    log(f"  usable price histories: {len(out)}/{len(tickers)}")
    return out


# --------------------------------------------------------------------------- #
# 5. Main
# --------------------------------------------------------------------------- #
def pct(x, dec=1):
    return "n/a" if x is None or (isinstance(x, float) and not np.isfinite(x)) else f"{x*100:.{dec}f}%"


def num(x, dec=1):
    return "n/a" if x is None or (isinstance(x, float) and not np.isfinite(x)) else f"{x:,.{dec}f}"


def money(x):
    if x is None or not np.isfinite(x):
        return "n/a"
    if abs(x) >= 1e9:
        return f"${x/1e9:.2f}B"
    return f"${x/1e6:.0f}M"


def apply_sic_filters(f: pd.DataFrame, sic: pd.DataFrame) -> tuple[pd.DataFrame, int, int]:
    """Join SIC codes and drop financials/real-estate and clinical-stage biotech."""
    f = f.join(sic, how="left")
    f["sic"] = f.sic.fillna(0).astype(int)
    bad = pd.Series(False, index=f.index)
    for lo, hi in SIC_EXCLUDE_RANGES:
        bad |= f.sic.between(lo, hi)
    n0 = len(f)
    f = f[~bad]
    n_fin = n0 - len(f)
    n0 = len(f)
    f = f[~(f.sic.isin(SIC_BIOTECH) & (f.revenue < BIOTECH_REV_MIN))]
    return f, n_fin, n0 - len(f)


def compute_metrics(f: pd.DataFrame) -> pd.DataFrame:
    """Valuation/quality/growth metrics + the composite score, sorted best first.

    Percentile ranks are cross-sectional, so the score depends on the population
    passed in. The candidate list and the wider universe are therefore scored
    separately and each row is ranked against its own peer set.
    """
    f = f.copy()
    f["ltd_missing"] = f.ltd.isna()
    f["ltd_tag"] = f.ltd_tag.fillna("none")
    f["ltd"] = f.ltd.fillna(0.0)
    f["cash"] = f.cash.fillna(0.0)
    f["net_debt"] = f.ltd - f.cash
    f["ev"] = f.mktcap + f.net_debt
    f["ev_ebit"] = np.where((f.ebit > 0) & (f.ev > 0), f.ev / f.ebit, np.nan)
    f["capex_missing"] = f.capex.isna()
    f["fcf"] = f.cfo - f.capex.fillna(0.0)
    f["fcf_yield"] = f.fcf / f.mktcap
    invcap = f.equity + f.net_debt
    f["roic"] = np.where(invcap > 0, f.ebit * 0.79 / invcap, np.nan)
    f["rev_growth"] = np.where(f.revenue_prior > 0, f.revenue / f.revenue_prior - 1, np.nan)
    f["net_debt_ebit"] = np.where(f.ebit > 0, f.net_debt / f.ebit, np.nan)
    for col in ("alt_shares", "alt_shares_py", "wanso_chg"):
        if col not in f:
            f[col] = np.nan
    for col in ("alt_shares_period", "alt_shares_py_period", "wanso_label"):
        if col not in f:
            f[col] = np.nan
    f["share_chg"] = np.where(f.shares_py > 0, f.shares / f.shares_py - 1, np.nan)
    f["share_chg_src"] = np.where(f.share_chg.notna(),
                                  "dei:EntityCommonStockSharesOutstanding", "")

    # Fallback 1: us-gaap:CommonStockSharesOutstanding, both sides from that tag.
    need = f.share_chg.isna() & (f.alt_shares > 0) & (f.alt_shares_py > 0)
    if need.any():
        f.loc[need, "share_chg"] = f.loc[need, "alt_shares"] / f.loc[need, "alt_shares_py"] - 1
        f.loc[need, "share_chg_src"] = "us-gaap:" + SHARES_ALT_TAG
        # surface the counts that actually produced the number
        f.loc[need, "shares_py"] = f.loc[need, "alt_shares_py"]
        f.loc[need, "shares_py_period"] = (f.loc[need, "alt_shares_py_period"].astype(str)
                                           + f" ({SHARES_ALT_TAG})")

    # Fallback 2: weighted-average basic shares, year over year.
    need = f.share_chg.isna() & f.wanso_chg.notna()
    if need.any():
        f.loc[need, "share_chg"] = f.loc[need, "wanso_chg"]
        f.loc[need, "share_chg_src"] = ("us-gaap:" + WANSO_TAG + " "
                                        + f.loc[need, "wanso_label"].astype(str))

    # share counts here are cover-page / annual counts; ignore absurd jumps
    # (reverse splits, unit changes) rather than ranking on them
    f.loc[f.share_chg.abs() > 3, "share_chg"] = np.nan
    f.loc[f.share_chg.isna(), "share_chg_src"] = ""

    # Revenue that grew alongside a much bigger share count is bought growth.
    f["rev_growth_note"] = ""
    dilutive = f.share_chg.notna() & (f.share_chg > SHARE_GROWTH_FLAG)
    f.loc[dilutive, "rev_growth_note"] = (
        "share count +" + (f.loc[dilutive, "share_chg"] * 100).round(1).astype(str)
        + "% yoy — growth may be acquisition/issuance-driven, not organic")

    def rank_hi(s):  # higher is better
        return s.rank(pct=True)

    r_fcf = rank_hi(f.fcf_yield)
    r_ev = 1.0 - f.ev_ebit.rank(pct=True)          # cheaper (lower EV/EBIT) = better
    r_ev = r_ev.where(f.ev_ebit.notna(), 0.0)      # no positive EBIT / negative EV -> worst
    r_roic = rank_hi(f.roic)
    r_growth = rank_hi(f.rev_growth)
    r_buyback = 1.0 - f.share_chg.rank(pct=True)   # shrinking share count = better
    comps = pd.concat([r_fcf, r_ev, r_roic, r_growth, r_buyback], axis=1)
    comps.columns = ["r_fcf_yield", "r_ev_ebit", "r_roic", "r_rev_growth", "r_buyback"]
    # r_ev_ebit already encodes "no positive EBIT" as 0.0 (a real signal). The other
    # four are NaN only when the underlying concept was not tagged, which is an
    # absence of information, not bad news -> score them neutrally at 0.5 so every
    # company is scored on the same five factors.
    comps = comps.fillna(0.5)
    base = comps.mean(axis=1)
    penalty = np.where(f.r6m < -0.40, 0.10, 0.0)
    bonus = np.where(f.mom_12_1 > 0, 0.05, 0.0)
    f = f.join(comps)
    f["score"] = (base - penalty + bonus).clip(0, 1.2)
    f["falling_knife"] = f.r6m < -0.40
    return f.sort_values("score", ascending=False)


def make_why(f: pd.DataFrame):
    """Return a row -> plain-English 'why it screens' function for this population."""
    q3 = {c: f[c].quantile(0.75) for c in ["fcf_yield", "roic", "rev_growth"]}
    q1_ev = f.ev_ebit.quantile(0.25)
    q1_sh = f.share_chg.quantile(0.25)

    def why(r) -> str:
        bits = []
        if np.isfinite(r.fcf_yield) and r.fcf_yield >= q3["fcf_yield"]:
            bits.append(f"top-quartile FCF yield {pct(r.fcf_yield)}")
        if np.isfinite(r.ev_ebit) and r.ev_ebit <= q1_ev:
            bits.append(f"cheap at {r.ev_ebit:.1f}x EV/EBIT")
        if np.isfinite(r.roic) and r.roic >= q3["roic"]:
            bits.append(f"high ROIC {pct(r.roic)}")
        if np.isfinite(r.rev_growth) and r.rev_growth >= q3["rev_growth"]:
            note = str(getattr(r, "rev_growth_note", "") or "")
            bits.append(f"revenue +{pct(r.rev_growth)}"
                        + (f" BUT {note}" if note else ""))
        elif str(getattr(r, "rev_growth_note", "") or ""):
            bits.append(str(r.rev_growth_note))
        if np.isfinite(r.share_chg) and r.share_chg <= q1_sh and r.share_chg < 0:
            bits.append(f"buying back stock {pct(r.share_chg)}")
        if np.isfinite(r.net_debt_ebit) and r.net_debt_ebit < 0:
            bits.append("net cash")
        if np.isfinite(r.mom_12_1) and r.mom_12_1 > 0:
            bits.append(f"12-1 momentum {pct(r.mom_12_1)}")
        if r.falling_knife:
            bits.append("WARNING 6m return below -40%")
        return "; ".join(bits) if bits else "balanced across factors, no single standout"

    return why


OUT_COLS = ["ticker", "name", "sic", "sic_desc", "exchange", "price", "mktcap", "ev",
            "ev_ebit", "fcf", "fcf_yield", "roic", "rev_growth", "net_debt", "net_debt_ebit",
            "share_chg", "share_chg_src", "rev_growth_note",
            "mom_12_1", "r6m", "off_52w_high", "adv20", "revenue",
            "revenue_prior", "ebit", "net_income", "cfo", "capex", "equity", "ltd", "cash",
            "shares", "shares_py", "capex_missing", "ltd_missing", "ltd_tag",
            "revenue_period", "ebit_period", "equity_period",
            "shares_period", "shares_py_period", "r_fcf_yield", "r_ev_ebit", "r_roic",
            "r_rev_growth", "r_buyback", "score", "why"]


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--universe-out", metavar="CSV",
                    help=f"also write every company passing the base filters with market cap "
                         f"${UNIVERSE_MIN/1e6:.0f}M-${UNIVERSE_MAX/1e9:.0f}B, scored and ranked")
    args = ap.parse_args(argv)
    universe_out = Path(args.universe_out).resolve() if args.universe_out else None

    t_start = time.time()
    stages: list[tuple[str, int]] = []

    uni = load_universe()
    stages.append(("SEC tickers -> unique CIKs with a usable ticker", len(uni)))

    prefetch_all()

    log("assembling fundamentals from frames")
    rev, rev_per, rev_prior = annual_concept("revenue")
    ni, _, _ = annual_concept("net_income")
    ebit, ebit_per, _ = annual_concept("op_income")
    cfo, _, _ = annual_concept("cfo")
    capex, _, _ = annual_concept("capex")
    equity, equity_per, _ = instant_concept("equity", INSTANT_PERIODS)
    assets, _, _ = instant_concept("assets", INSTANT_PERIODS)
    ltd, ltd_per, ltd_tag = instant_concept("ltd", INSTANT_PERIODS)
    cash, _, _ = instant_concept("cash", INSTANT_PERIODS)
    sh, sh_per = shares_concept(INSTANT_PERIODS)
    sh_py, sh_py_per = shares_concept(INSTANT_PERIODS_PY)
    alt_sh, alt_sh_per = alt_shares_concept(INSTANT_PERIODS)
    alt_sh_py, alt_sh_py_per = alt_shares_concept(INSTANT_PERIODS_PY)
    wanso_chg, wanso_lab = wanso_yoy()

    f = pd.DataFrame(
        dict(revenue=rev, revenue_prior=rev_prior, revenue_period=rev_per,
             net_income=ni, ebit=ebit, ebit_period=ebit_per, cfo=cfo, capex=capex,
             equity=equity, equity_period=equity_per, assets=assets,
             ltd=ltd, ltd_period=ltd_per, ltd_tag=ltd_tag, cash=cash,
             shares=sh, shares_period=sh_per, shares_py=sh_py, shares_py_period=sh_py_per,
             alt_shares=alt_sh, alt_shares_period=alt_sh_per,
             alt_shares_py=alt_sh_py, alt_shares_py_period=alt_sh_py_per,
             wanso_chg=wanso_chg, wanso_label=wanso_lab)
    )
    f.index.name = "cik"
    f = f.join(uni, how="inner")
    stages.append(("CIKs with any USD XBRL frame data + a ticker", len(f)))

    f = f[f.shares.notna() & (f.shares > 0) & f.revenue.notna() & f.ebit.notna()]
    stages.append(("have shares outstanding + revenue + operating income", len(f)))

    f = f[f.revenue > REV_MIN]
    stages.append((f"revenue > ${REV_MIN/1e6:.0f}M", len(f)))

    f = f[f.ebit > -0.25 * f.revenue]
    stages.append(("operating income > -25% of revenue (not deeply loss-making)", len(f)))

    # Pre-price sanity: a $5B cap needs price = 5e9/shares; drop absurd share counts
    f = f[f.shares < 5e9]
    stages.append(("shares outstanding < 5B (drops mega-caps / odd units)", len(f)))

    f = f[f.cfo.notna()]
    stages.append(("operating cash flow reported (FCF computable)", len(f)))

    prices = fetch_prices(sorted(f.yf.unique().tolist()))
    f = f.join(prices, on="yf", how="inner")
    stages.append(("priced by yfinance (>=130 trading days)", len(f)))

    f["mktcap"] = f.price * f.shares
    priced = f                                   # everything priced, before any cap band

    f = priced[(priced.mktcap >= MKTCAP_MIN) & (priced.mktcap <= MKTCAP_MAX)]
    stages.append((f"market cap ${MKTCAP_MIN/1e6:.0f}M - ${MKTCAP_MAX/1e9:.0f}B", len(f)))

    f = f[f.adv20 > ADV_MIN]
    stages.append((f"20d avg dollar volume > ${ADV_MIN/1e6:.0f}M", len(f)))

    # Wider band for --universe-out. Same base filters, different cap window, so it
    # is not a subset of the candidate set (it adds $50-100M, drops $2-5B).
    uni = pd.DataFrame()
    if universe_out is not None:
        uni = priced[(priced.mktcap >= UNIVERSE_MIN) & (priced.mktcap <= UNIVERSE_MAX)
                     & (priced.adv20 > ADV_MIN)].copy()
        log(f"universe band ${UNIVERSE_MIN/1e6:.0f}M-${UNIVERSE_MAX/1e9:.0f}B "
            f"before SIC exclusions: {len(uni)}")

    # One submissions fetch covering both populations (cached, so no double cost).
    sic = fetch_sic(sorted(set(f.index.unique()) | set(uni.index.unique())))

    n_before = len(f)
    f, n_fin, n_bio = apply_sic_filters(f, sic)
    stages.append((f"exclude SIC 6000-6799 (banks/insurers/REITs/holdcos): -{n_fin}",
                   n_before - n_fin))
    stages.append((f"exclude drug/biotech SIC with revenue < ${BIOTECH_REV_MIN/1e6:.0f}M: -{n_bio}",
                   len(f)))

    # ---------------- metrics + composite score ----------------
    log("computing metrics")
    f = compute_metrics(f)
    stages.append(("scored universe", len(f)))

    # ---------------- "why it screens" ----------------
    why = make_why(f)
    top = f.head(TOP_N).copy()
    top["why"] = [why(r) for _, r in top.iterrows()]

    cols = OUT_COLS
    out = top[cols]
    out.to_csv(HERE / "candidates.csv", index=True)
    log(f"wrote {HERE/'candidates.csv'}")

    # ---------------- full sub-$2B universe ----------------
    n_universe = 0
    if universe_out is not None:
        u, u_fin, u_bio = apply_sic_filters(uni, sic)
        log(f"universe after SIC exclusions: {len(u)} "
            f"(-{u_fin} financials/REITs, -{u_bio} clinical-stage biotech)")
        u = compute_metrics(u)
        u_why = make_why(u)
        u["why"] = [u_why(r) for _, r in u.iterrows()]
        u.insert(0, "rank", range(1, len(u) + 1))
        universe_out.parent.mkdir(parents=True, exist_ok=True)
        u[["rank"] + cols].to_csv(universe_out, index=True)
        n_universe = len(u)
        log(f"wrote {universe_out}")

    # ---------------- markdown ----------------
    asof = dt.date.today().isoformat()
    L = []
    L.append(f"# Deep-Value Screen -- US Small/Mid Cap -- {asof}")
    L.append("")
    L.append("Free data only: SEC XBRL `frames` API for fundamentals (one request per concept "
             "for every filer), SEC `submissions` for SIC codes, yfinance for prices. "
             "Generated by `research/deepvalue/screen.py`. **Research output only -- not investment advice.**")
    L.append("")
    L.append("## Filter stages")
    L.append("")
    L.append("| # | Stage | Companies remaining |")
    L.append("|---|---|---|")
    for i, (label, n) in enumerate(stages, 1):
        L.append(f"| {i} | {label} | {n:,} |")
    L.append("")
    L.append("## Score formula")
    L.append("")
    L.append("```")
    L.append("score = mean of five cross-sectional percentile ranks")
    L.append("          r_fcf_yield   pct-rank of FCF/mktcap            (higher better)")
    L.append("          r_ev_ebit     1 - pct-rank of EV/EBIT           (lower better; NaN or")
    L.append("                                                          non-positive EBIT -> 0.0)")
    L.append("          r_roic        pct-rank of EBIT*0.79/(equity+net debt)  (higher better)")
    L.append("          r_rev_growth  pct-rank of YoY revenue growth    (higher better)")
    L.append("          r_buyback     1 - pct-rank of share-count change (shrinking better)")
    L.append("")
    L.append("        a factor whose XBRL concept was simply not tagged scores a neutral 0.5,")
    L.append("        so every company is ranked on the same five factors")
    L.append("")
    L.append("        - 0.10 if 6-month return < -40%   (falling-knife penalty)")
    L.append("        + 0.05 if 12-1 momentum > 0       (trend confirmation bonus)")
    L.append("")
    L.append("EV        = market cap + long-term debt - cash")
    L.append("FCF       = cash flow from operations - capex")
    L.append("ROIC      = operating income x 0.79 (21% tax) / (equity + LTD - cash)")
    L.append("mktcap    = last close x dei:EntityCommonStockSharesOutstanding")
    L.append("```")
    L.append("")
    L.append(f"## Top {TOP_N}")
    L.append("")
    L.append("| # | Ticker | Name | Mkt cap | EV/EBIT | FCF yld | ROIC | Rev gr | NetDebt/EBIT | Share chg | 12-1 mom | ADV $ | Score |")
    L.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for i, (cik, r) in enumerate(top.iterrows(), 1):
        L.append(
            f"| {i} | {r.ticker} | {str(r['name'])[:34]} | {money(r.mktcap)} | "
            f"{num(r.ev_ebit)} | {pct(r.fcf_yield)} | {pct(r.roic)} | {pct(r.rev_growth)} | "
            f"{num(r.net_debt_ebit)} | {pct(r.share_chg)} | {pct(r.mom_12_1)} | "
            f"{money(r.adv20)} | {r.score:.3f} |"
        )
    L.append("")
    L.append("## Why each name screens")
    L.append("")
    for i, (cik, r) in enumerate(top.iterrows(), 1):
        L.append(f"{i}. **{r.ticker}** -- {r['name']} ({r.sic_desc or 'SIC ' + str(r.sic)}). {r.why}")
    L.append("")
    L.append("## Data notes")
    L.append("")
    L.append(f"- Fiscal periods used per company are in `candidates.csv` "
             f"(`revenue_period`, `ebit_period`, `equity_period`, `shares_period`). "
             f"Annual preference {' -> '.join(ANNUAL_PERIODS)} -> TTM(4Q) sum of "
             f"{', '.join(TTM_QUARTERS)} for off-calendar fiscal years.")
    L.append(f"- Balance-sheet instants: first available of {', '.join(INSTANT_PERIODS)}; "
             f"prior-year share count from {', '.join(INSTANT_PERIODS_PY)}.")
    L.append(f"- `share_chg` prefers the dei cover-page count on both sides. That tag is missing "
             f"(or filed as zero) for a slice of filers, so it falls back first to "
             f"`us-gaap:{SHARES_ALT_TAG}` for both instants and then to "
             f"`us-gaap:{WANSO_TAG}` year over year. `share_chg_src` in the CSV names the tag "
             f"that produced each number; both sides of a ratio always come from the same tag.")
    L.append(f"- `rev_growth_note` flags companies whose share count grew more than "
             f"{SHARE_GROWTH_FLAG:.0%} year over year: revenue growth alongside that much "
             f"issuance is usually bought, not organic, and the note is repeated in the "
             f"'why each name screens' line below.")
    L.append("- `ltd_missing` / `ltd_tag` in the CSV show whether any long-term-debt concept was found "
             "and which one. When nothing is tagged, long-term debt is treated as zero, so EV is "
             "understated and ROIC overstated for those names. Short-term borrowings, floorplan "
             "notes and lease liabilities are never included in EV.")
    L.append("- Cash is `CashAndCashEquivalentsAtCarryingValue`, falling back to the cash-flow-statement "
             "total (which includes restricted cash) when the plain tag is absent. Short-term "
             "investments and marketable securities are never netted, so EV is conservative for "
             "companies that park cash in securities.")
    L.append("- `capex_missing` in the CSV flags companies with no capex concept tagged; for those "
             "FCF equals operating cash flow and is therefore overstated.")
    L.append("- Market cap uses the dei cover-page share count, which for dual-class companies "
             "sometimes covers only one class and then understates the true market cap.")
    L.append("- Only USD-denominated frames are requested, so foreign-currency filers drop out automatically.")
    L.append("- Sector exclusions use the SIC code from the SEC submissions endpoint, fetched only for "
             "companies that already passed the market-cap and liquidity filters.")
    L.append(f"- No sector-neutrality is applied: the composite is a pure cross-sectional rank, so "
             f"whichever industry is cheapest on EV/EBIT at the moment can dominate the list "
             f"(currently: {', '.join(f'{k} x{v}' for k, v in top.sic_desc.fillna('unknown').value_counts().head(3).items())}).")
    L.append("- One row per CIK: where a CIK maps to several tickers, the class without a `-` suffix "
             "(else SEC's file order, which is roughly cap-descending) is kept. Warrants, units, "
             "rights and preferreds are dropped by ticker suffix.")
    L.append("")
    (HERE / "CANDIDATES.md").write_text("\n".join(L) + "\n")
    log(f"wrote {HERE/'CANDIDATES.md'}")

    # ---------------- spot checks ----------------
    print("\n=== SPOT CHECK: raw inputs for top 3 ===")
    for cik, r in top.head(3).iterrows():
        print(f"\n{r.ticker} ({r['name']}) CIK {cik}  SIC {r.sic} {r.sic_desc}")
        print(f"  price={r.price:.2f} x shares={r.shares:,.0f} ({r.shares_period}) -> mktcap={money(r.mktcap)}")
        print(f"  revenue={money(r.revenue)} ({r.revenue_period})  prior={money(r.revenue_prior)}  growth={pct(r.rev_growth)}")
        print(f"  ebit={money(r.ebit)} ({r.ebit_period})  net_income={money(r.net_income)}")
        print(f"  cfo={money(r.cfo)}  capex={money(r.capex)}  fcf={money(r.fcf)}  fcf_yield={pct(r.fcf_yield)}")
        print(f"  equity={money(r.equity)} ({r.equity_period})  ltd={money(r.ltd)}  cash={money(r.cash)}  net_debt={money(r.net_debt)}")
        print(f"  EV={money(r.ev)}  EV/EBIT={num(r.ev_ebit)}  ROIC={pct(r.roic)}")
        print(f"  shares_py={r.shares_py:,.0f} ({r.shares_py_period})  "
              f"share_chg={pct(r.share_chg)} [{r.share_chg_src or 'unavailable'}]")
        print(f"  adv20={money(r.adv20)}  mom_12_1={pct(r.mom_12_1)}  r6m={pct(r.r6m)}  off52wh={pct(r.off_52w_high)}")

    print("\n=== FILTER STAGES ===")
    for i, (label, n) in enumerate(stages, 1):
        print(f"{i:>2}. {label:<70} {n:>7,}")
    print("\n=== TOP 10 ===")
    for i, (cik, r) in enumerate(f.head(10).iterrows(), 1):
        print(f"{i:>2}. {r.ticker:<6} {str(r['name'])[:36]:<38} score={r.score:.3f}")
    if universe_out is not None:
        print(f"\nUNIVERSE under ${UNIVERSE_MAX/1e9:.0f}B: {n_universe:,} companies "
              f"(market cap ${UNIVERSE_MIN/1e6:.0f}M-${UNIVERSE_MAX/1e9:.0f}B, "
              f"revenue > ${REV_MIN/1e6:.0f}M, ADV > ${ADV_MIN/1e6:.0f}M, non-financial) "
              f"-> {universe_out}")
    print(f"\nruntime: {time.time()-t_start:.1f}s")


if __name__ == "__main__":
    main()
