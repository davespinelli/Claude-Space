#!/usr/bin/env python3
"""Idea 50 - insider CLUSTER buying on the SMALL-CAP panel (rerun of idea 32).

Idea 32 ran the Cohen-Malloy-Pomorski (2012) cluster-buying signal on 136 mega caps and came
back PARK (12m) / KILL (6m): the edge was there (OOS Sharpe 1.36 vs SPY 0.94) but the book
held only 4-8 names at 100% gross and drew down -39.7%, about 2x 4b's cap.  Its memo named
two things to change, and this script changes exactly those two and nothing else:

  1. THE UNIVERSE.  CMP's effect is an information-asymmetry effect, so it should be strongest
     in small caps.  483 sub-$2B names (data/prices_small.csv.gz) instead of 136 mega caps.
     A 439-name tradable panel should also give a 20-60 name book rather than 4-8, which is
     the concentration problem idea 32 died of.
  2. THE ROUTINE/OPPORTUNISTIC SPLIT.  CMP's actual result is that only *opportunistic*
     insiders predict returns.  Idea 32 used every code-P buyer and said so.

Plus one sizing arm the idea brief asks for (5% per-name cap, remainder in cash) to show the
concentration effect directly rather than argue about it.

Signal (identical to idea 32, not re-tuned)
-------------------------------------------
Qualifying purchase = Form 4, non-derivative table, transaction code P (open-market buy),
                      acquired (A), shares x price >= $10,000.
Cluster             = >= 2 DISTINCT reporting owners with qualifying purchases whose
                      TRANSACTION dates fall inside a 30 calendar-day window.
Signal date         = min over partners of max(filing_date of the pair), i.e. the first moment
                      the pair is public.  Form 4 is due within 2 business days, so 0-4 days.
Entry               = weekly rebalance; hold every ticker whose most recent cluster signal is
                      <= 30 calendar days old, then hold it HOLD months from the signal.

Arms
----
  hold     : 6 or 12 months                       <- the ONE tuned parameter (rule 8 chooses it)
  filter   : ALL buyers  vs  OPPORTUNISTIC only   <- CMP's own test, pre-specified, not tuned
  sizing   : EW at 100% gross  vs  5%/name cap    <- concentration diagnostic, pre-specified

ROUTINE (dropped by the OPPORTUNISTIC arm): a purchase by insider I at firm F in calendar
month M of year Y is routine if the SAME (firm, insider) also made a qualifying purchase in
calendar month M of Y-1 AND Y-2 AND Y-3.  Deviation from CMP, stated rather than hidden: CMP
classify on the insider's whole trade record (buys and sells); the SEC extract used here keeps
only code-P purchases, so this is the purchase-only version the idea brief specifies.  It also
means nothing can be classified routine before 2015 (three prior years of history are needed
and the sample starts in 2012).

Data
----
Prices : baseline.load_universe(small=True, with_spy=True), 2010-01-04 -> 2026-09-03, a true
         trading-day index (checked in-script).  The 44 names with small_meta.csv
         max_1d_move >= 1.0 (corrupted / relisted) are dropped -> 439 tradable + SPY benchmark.
         SURVIVORSHIP: current constituents of a sub-$2B screen, so the panel is biased upward
         and, for a signal that concentrates in distressed names, biased in the WORST direction.
Insiders: the SEC's own quarterly Form 345 structured data sets, already cached in
         data/sec_cache/form345/ (57 zips, 2012q1 .. 2026q1, ALL filers), read through the
         same loader as research/backtests/2026-09-04_insider-cluster-buying.py.  2026Q2+ is
         not published as a data set; --crawl-q2 fills it from data.sec.gov/submissions JSON
         for the small-cap tickers only.  Without that flag the window is a stated GAP.

Verdicts (PROTOCOL rule 4): 4a = Sharpe > RULES v1 in BOTH halves and MaxDD no worse.
4b = Sharpe > SPY in BOTH halves AND out-of-sample, MaxDD <= 60% of SPY's, CAGR >= 70% of SPY's.
Rule 8 walk-forward: hold chosen on 2012-2018 only, evaluated untouched on 2019-2026 (the
protocol's 2009-2016 split is shifted because Form 4 structured coverage starts in 2012).

Usage
-----
    python 2026-09-04_insider-cluster-smallcap.py                # uses the cache
    python 2026-09-04_insider-cluster-smallcap.py --build        # rebuild from cached zips
    python 2026-09-04_insider-cluster-smallcap.py --build --crawl-q2   # + 2026Q2+ crawl

Deterministic and standalone.
"""
from __future__ import annotations

import argparse
import io
import json
import sys
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))
sys.path.insert(0, str(REPO / "research" / "deepvalue"))

CACHE_DIR = REPO / "data" / "sec_cache"
Z_DIR = CACHE_DIR / "form345"
SUBS_DIR = CACHE_DIR / "submissions"
XML_DIR = CACHE_DIR / "form4xml"
PURCHASES = REPO / "data" / "form4_purchases_small.csv"
META = REPO / "data" / "small_meta.csv"

START = "2012-01-01"
BULK_LAST_Q = (2026, 1)
XML_FROM = "2026-04-01"
MIN_VALUE = 10_000.0
CLUSTER_DAYS = 30
SIGNAL_DAYS = 30
NAME_CAP = 0.05
COST_BPS = 10
FREQ = "W"
IS_END = "2018-12-31"
OOS_START = "2019-01-01"
BAD_MOVE = 1.0
SCRIPT = Path(__file__).name


# =========================================================================
# 0. universe
# =========================================================================
def small_universe(px: pd.DataFrame):
    """Tradable small-cap tickers: panel columns minus SPY minus the corrupted names."""
    meta = pd.read_csv(META)
    bad = set(meta.loc[meta["max_1d_move"] >= BAD_MOVE, "ticker"])
    keep = [c for c in px.columns if c != "SPY" and c not in bad]
    return keep, sorted(bad & set(px.columns))


# =========================================================================
# 1. data build  (loader reused from 2026-09-04_insider-cluster-buying.py)
# =========================================================================
def norm_symbol(s) -> str:
    if not isinstance(s, str):
        return ""
    s = s.strip().upper()
    if ":" in s:
        s = s.split(":")[-1]
    return s.replace(".", "-").replace(" ", "-")


def universe_cik_map(tickers) -> dict[str, str]:
    """{zero-padded issuer CIK -> ticker}; fallback for blank ISSUERTRADINGSYMBOL."""
    raw = (CACHE_DIR / "company_tickers.json").read_bytes()
    uni = set(tickers)
    m = {}
    for v in json.loads(raw).values():
        t = norm_symbol(v["ticker"])
        if t in uni:
            m[f"{int(v['cik_str']):010d}"] = t
    return m


def quarters(start_year=2012):
    y, q = start_year, 1
    while (y, q) <= BULK_LAST_Q:
        yield y, q
        q += 1
        if q == 5:
            y, q = y + 1, 1


def _read_tsv(zf, name, usecols):
    with zf.open(name) as fh:
        return pd.read_csv(io.BytesIO(fh.read()), sep="\t", dtype=str,
                           usecols=usecols, low_memory=False)


def build_from_bulk(universe: set[str], verbose=True) -> pd.DataFrame:
    """Cached SEC quarterly Form 345 data sets -> qualifying code-P purchases.

    The zips in data/sec_cache/form345/ cover ALL filers for 2012q1..2026q1, so no network is
    needed; fetch() is only reached if a quarter is missing from the cache."""
    from fetch_filings import fetch
    Z_DIR.mkdir(parents=True, exist_ok=True)
    cikmap = universe_cik_map(universe)
    frames = []
    for y, q in quarters():
        tag = f"{y}q{q}"
        path = Z_DIR / f"{tag}_form345.zip"
        if path.exists() and path.stat().st_size > 0:
            raw = path.read_bytes()
        else:
            raw = fetch(f"https://www.sec.gov/files/structureddata/data/"
                        f"insider-transactions-data-sets/{tag}_form345.zip",
                        Z_DIR, f"{tag}_form345.zip", binary=True)
        if raw is None:
            print(f"  ! {tag}: not available", file=sys.stderr)
            continue
        with zipfile.ZipFile(io.BytesIO(raw)) as zf:
            sub = _read_tsv(zf, "SUBMISSION.tsv",
                            ["ACCESSION_NUMBER", "FILING_DATE", "DOCUMENT_TYPE",
                             "ISSUERCIK", "ISSUERTRADINGSYMBOL"])
            sub = sub[sub["DOCUMENT_TYPE"].isin(["4", "4/A"])].copy()
            sub["ticker"] = sub["ISSUERTRADINGSYMBOL"].map(norm_symbol)
            blank = ~sub["ticker"].isin(universe)
            sub.loc[blank, "ticker"] = sub.loc[blank, "ISSUERCIK"].map(cikmap).fillna("")
            sub = sub[sub["ticker"].isin(universe)]
            if sub.empty:
                if verbose:
                    print(f"  {tag}: 0 universe filings", flush=True)
                continue
            accs = set(sub["ACCESSION_NUMBER"])
            tr = _read_tsv(zf, "NONDERIV_TRANS.tsv",
                           ["ACCESSION_NUMBER", "TRANS_DATE", "TRANS_CODE", "TRANS_SHARES",
                            "TRANS_PRICEPERSHARE", "TRANS_ACQUIRED_DISP_CD"])
            tr = tr[tr["ACCESSION_NUMBER"].isin(accs) & (tr["TRANS_CODE"] == "P")
                    & (tr["TRANS_ACQUIRED_DISP_CD"] == "A")]
            if tr.empty:
                if verbose:
                    print(f"  {tag}: {len(sub):5d} filings ->     0 purchases", flush=True)
                continue
            own = _read_tsv(zf, "REPORTINGOWNER.tsv",
                            ["ACCESSION_NUMBER", "RPTOWNERCIK", "RPTOWNERNAME",
                             "RPTOWNER_RELATIONSHIP"])
            own = own[own["ACCESSION_NUMBER"].isin(set(tr["ACCESSION_NUMBER"]))]
            own = (own.sort_values(["ACCESSION_NUMBER", "RPTOWNERCIK"])
                      .groupby("ACCESSION_NUMBER")
                      .agg(owner_cik=("RPTOWNERCIK", lambda s: "+".join(sorted(set(s)))),
                           owner_name=("RPTOWNERNAME",
                                      lambda s: " / ".join(dict.fromkeys(s.fillna("")))),
                           relationship=("RPTOWNER_RELATIONSHIP",
                                         lambda s: " / ".join(dict.fromkeys(s.fillna("")))))
                      .reset_index())
        df = tr.merge(sub[["ACCESSION_NUMBER", "ticker", "FILING_DATE"]],
                      on="ACCESSION_NUMBER").merge(own, on="ACCESSION_NUMBER", how="left")
        df["shares"] = pd.to_numeric(df["TRANS_SHARES"], errors="coerce")
        df["price"] = pd.to_numeric(df["TRANS_PRICEPERSHARE"], errors="coerce")
        df["filing_date"] = pd.to_datetime(df["FILING_DATE"], format="%d-%b-%Y", errors="coerce")
        df["trans_date"] = pd.to_datetime(df["TRANS_DATE"], format="%d-%b-%Y", errors="coerce")
        df = df.rename(columns={"ACCESSION_NUMBER": "accession"})
        df["source"] = "sec_dataset"
        frames.append(df[["ticker", "filing_date", "trans_date", "owner_cik", "owner_name",
                          "relationship", "shares", "price", "accession", "source"]])
        if verbose:
            print(f"  {tag}: {len(sub):5d} filings -> {len(df):5d} purchase rows", flush=True)
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()


def build_from_xml(universe_tickers, xml_cap=6000, verbose=True) -> pd.DataFrame:
    """2026Q2+ only: submissions JSON + Form 4 XML, for the small-cap tickers."""
    from fetch_filings import (fetch, ticker_to_cik, get_submissions, parse_form4,
                               filing_dir_url, filing_documents)
    SUBS_DIR.mkdir(parents=True, exist_ok=True)
    XML_DIR.mkdir(parents=True, exist_ok=True)
    todo, skipped_ciks = [], []
    for t in universe_tickers:
        try:
            cik, _ = ticker_to_cik(t, CACHE_DIR)
            sub = get_submissions(cik, SUBS_DIR)
        except Exception as exc:
            skipped_ciks.append((t, str(exc)[:50]))
            continue

        def take(rec, t=t, cik=cik):
            n = len(rec["form"])
            for i in range(n):
                if rec["form"][i] in ("4", "4/A") and rec["filingDate"][i] >= XML_FROM:
                    todo.append((t, cik, rec["filingDate"][i], rec["accessionNumber"][i],
                                 (rec.get("primaryDocument") or [""] * n)[i]))
        take(sub["filings"]["recent"])
        for f in sub["filings"].get("files", []):
            if f.get("filingTo", "") < XML_FROM:
                continue
            raw = fetch(f"https://data.sec.gov/submissions/{f['name']}", SUBS_DIR, f["name"])
            if raw:
                take(json.loads(raw))
    todo = sorted(set(todo))
    n_all = len(todo)
    # clusters need >= 2 filings in the window, so ticker-months with a single filing cannot
    # produce one; dropping them is lossless for this signal, not a sample
    cnt = pd.Series([f"{t}|{d[:7]}" for t, _, d, _, _ in todo]).value_counts()
    keep_keys = set(cnt[cnt >= 2].index)
    todo = [r for r in todo if f"{r[0]}|{r[2][:7]}" in keep_keys]
    n_pref = len(todo)
    skipped_cap = max(0, n_pref - xml_cap)
    todo = todo[:xml_cap]
    if verbose:
        print(f"  XML window {XML_FROM}+: {n_all} filings, {n_pref} after the >=2/month "
              f"pre-filter, downloading {len(todo)} (cap {xml_cap}, skipped {skipped_cap})",
              flush=True)
    rows = []
    for i, (t, cik, fdate, acc, primary) in enumerate(todo):
        name = (primary or "form4.xml").split("/")[-1]
        raw = fetch(f"{filing_dir_url(cik, acc)}/{name}", XML_DIR, f"{acc}_{name}")
        if raw is None or b"<ownershipDocument" not in raw[:4000]:
            for d in filing_documents(cik, acc, XML_DIR):
                if d["document"].lower().endswith(".xml"):
                    raw = fetch(f"{filing_dir_url(cik, acc)}/{d['document']}", XML_DIR,
                                f"{acc}_{d['document']}")
                    break
        if raw is None:
            continue
        for r in parse_form4(raw, fdate, acc):
            if (r["table"] != "non-derivative" or r["code"] != "P"
                    or r["acquired_disposed"] != "A"):
                continue
            rows.append(dict(ticker=t, filing_date=fdate, trans_date=r["transaction_date"],
                             owner_cik=r["owner"], owner_name=r["owner"],
                             relationship=r["relationship"], shares=r["shares"],
                             price=r["price"], accession=acc, source="form4_xml"))
        if verbose and (i + 1) % 250 == 0:
            print(f"    {i+1}/{len(todo)} XML parsed, {len(rows)} purchase rows", flush=True)
    df = pd.DataFrame(rows)
    if not df.empty:
        for c in ("shares", "price"):
            df[c] = pd.to_numeric(df[c].astype(str).str.replace(",", ""), errors="coerce")
        df["filing_date"] = pd.to_datetime(df["filing_date"])
        df["trans_date"] = pd.to_datetime(df["trans_date"], errors="coerce")
    df.attrs["skipped"] = dict(total=n_all, after_prefilter=n_pref, capped_out=skipped_cap,
                               no_cik=skipped_ciks)
    return df


def build_cache(tickers, crawl_q2=False, xml_cap=6000):
    print(f"building {PURCHASES.name} for {len(tickers)} small-cap tickers, {START} -> "
          + ("today" if crawl_q2 else f"{BULK_LAST_Q[0]}Q{BULK_LAST_Q[1]}"))
    parts = [build_from_bulk(set(tickers))]
    print(f"  bulk rows: {len(parts[0])}")
    if crawl_q2:
        xml = build_from_xml(tickers, xml_cap=xml_cap)
        print(f"  xml  rows: {len(xml)}")
        if len(xml):
            parts.append(xml)
        if xml.attrs.get("skipped"):
            print("  skipped:", xml.attrs["skipped"])
    df = pd.concat(parts, ignore_index=True)
    df = df[(df["filing_date"] >= START) & df["shares"].notna() & df["price"].notna()]
    df["value"] = df["shares"] * df["price"]
    df = df[df["value"] >= MIN_VALUE]
    df["trans_date"] = df["trans_date"].fillna(df["filing_date"])
    df = (df.sort_values(["ticker", "trans_date", "owner_cik", "accession"])
            .drop_duplicates(["ticker", "owner_cik", "trans_date", "shares", "price"]))
    df.to_csv(PURCHASES, index=False)
    print(f"  wrote {PURCHASES} ({len(df)} qualifying purchases, "
          f"{df['ticker'].nunique()} tickers)")
    return df


# =========================================================================
# 2. routine / opportunistic (CMP)
# =========================================================================
def tag_routine(df: pd.DataFrame) -> pd.Series:
    """True where the (firm, insider) also bought in the SAME calendar month in each of the
    three prior years.  Purchase-only version of CMP's routine/opportunistic split."""
    key = df["ticker"].astype(str) + "|" + df["owner_cik"].astype(str)
    ym = set(zip(key, df["trans_date"].dt.year, df["trans_date"].dt.month))
    return pd.Series(
        [all((k, y - b, m) in ym for b in (1, 2, 3))
         for k, y, m in zip(key, df["trans_date"].dt.year, df["trans_date"].dt.month)],
        index=df.index)


# =========================================================================
# 3. signal
# =========================================================================
def cluster_signal_dates(df: pd.DataFrame) -> pd.DataFrame:
    """-> DataFrame[ticker, signal_date, n_insiders]: dates on which a >=2-insider,
    30-calendar-day cluster becomes public.  signal_date = max filing_date of the pair."""
    out = []
    for t, g in df.groupby("ticker", sort=True):
        g = g.sort_values("trans_date")
        td = g["trans_date"].values
        fd = g["filing_date"].values
        ow = g["owner_cik"].astype(str).values
        for i in range(len(g)):
            lo = td[i] - np.timedelta64(CLUSTER_DAYS, "D")
            partners = [j for j in range(i) if td[j] >= lo and ow[j] != ow[i]]
            if not partners:
                continue
            sig = min(max(fd[i], fd[j]) for j in partners)
            n_ins = len({ow[i]} | {ow[j] for j in partners})
            out.append((t, pd.Timestamp(sig), n_ins))
    s = pd.DataFrame(out, columns=["ticker", "signal_date", "n_insiders"])
    if s.empty:
        return s
    return (s.groupby(["ticker", "signal_date"], as_index=False)["n_insiders"].max()
             .sort_values(["signal_date", "ticker"]))


def active_matrix(signals: pd.DataFrame, px: pd.DataFrame, hold_months: int) -> pd.DataFrame:
    hold_days = int(round(hold_months * 30.4375))
    active = pd.DataFrame(False, index=px.index, columns=px.columns)
    idx = px.index
    for t, g in signals.groupby("ticker"):
        if t not in active.columns:
            continue
        col = np.zeros(len(idx), dtype=bool)
        for sd in g["signal_date"]:
            lo = idx.searchsorted(sd)
            hi = idx.searchsorted(sd + pd.Timedelta(days=hold_days))
            if lo < len(idx):
                col[lo:hi] = True
        active[t] = col
    return active


def weights_from_active(active: pd.DataFrame, cap: float | None) -> pd.DataFrame:
    """Equal weight at 100% gross; with cap, min(1/n, cap) per name and the rest in cash."""
    n = active.sum(axis=1)
    per = 1.0 / n.where(n > 0, np.nan)
    if cap is not None:
        per = per.clip(upper=cap)
    return active.astype(float).mul(per, axis=0).fillna(0.0)


# =========================================================================
# 4. evaluation
# =========================================================================
def half_sharpes(r, metrics):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def row(name, r, metrics):
    m = metrics(r)
    h1, h2 = half_sharpes(r, metrics)
    return dict(name=name, CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2)


def verdict(idea, base, spy, oos_sharpe=None, oos_spy=None):
    """PROTOCOL 4a / 4b, plus the PARK case rule 4 allows (signal present, risk caps missed)."""
    a = (idea["H1"] > base["H1"] and idea["H2"] > base["H2"]
         and idea["MaxDD"] >= base["MaxDD"])
    sharpe_ok = idea["H1"] > spy["H1"] and idea["H2"] > spy["H2"]
    if oos_sharpe is not None and oos_spy is not None:
        sharpe_ok = sharpe_ok and oos_sharpe > oos_spy
    risk_ok = (idea["MaxDD"] >= 0.60 * spy["MaxDD"] and idea["CAGR"] >= 0.70 * spy["CAGR"])
    b = sharpe_ok and risk_ok
    if a and b:
        return "KEEP (4a+4b)"
    if a:
        return "KEEP (4a)"
    if b:
        return "KEEP (4b)"
    if sharpe_ok:
        return "PARK (4b: Sharpe yes, risk caps no)"
    return "KILL"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--build", action="store_true")
    ap.add_argument("--crawl-q2", action="store_true",
                    help="fill 2026Q2+ from data.sec.gov (else it is a stated gap)")
    ap.add_argument("--xml-cap", type=int, default=6000)
    args = ap.parse_args()

    from baseline import load_universe, rules_v1_weights
    from engine import backtest, metrics

    # ---------------- universe ----------------
    px_all = load_universe(small=True, with_spy=True, start="2010-01-01")
    tickers, dropped = small_universe(px_all)
    px = px_all[tickers]                      # tradable small caps only
    spy_px = px_all["SPY"]
    print(f"small panel: {px_all.shape[1]} columns -> {len(tickers)} tradable "
          f"({len(dropped)} dropped for max_1d_move >= {BAD_MOVE}: "
          f"{', '.join(dropped[:8])}{' ...' if len(dropped) > 8 else ''})")
    print(f"  {px.index[0].date()} -> {px.index[-1].date()}, {len(px)} rows, "
          f"weekend rows {(px.index.dayofweek >= 5).sum()} (trading-day index)")
    print("  rows per year: " + " ".join(
        f"{y}:{n}" for y, n in px.index.to_series().groupby(px.index.year).count().items()))

    # ---------------- insider data ----------------
    if args.build or not PURCHASES.exists():
        build_cache(tickers, crawl_q2=args.crawl_q2, xml_cap=args.xml_cap)
    buys = pd.read_csv(PURCHASES, parse_dates=["filing_date", "trans_date"])
    buys = buys[buys["ticker"].isin(tickers)].copy()
    # hygiene, not tuning: a Form 4 cannot be filed BEFORE the transaction it reports.
    lag = (buys["filing_date"] - buys["trans_date"]).dt.days
    n_bad = int((lag < 0).sum())
    buys = buys[lag >= 0].copy()
    lag = lag[lag >= 0]
    print(f"\npurchases: {len(buys)} rows, {buys['ticker'].nunique()} tickers, "
          f"{buys['filing_date'].min().date()} -> {buys['filing_date'].max().date()}, "
          f"{buys['owner_cik'].nunique()} distinct owners, median ${buys['value'].median():,.0f}")
    print(f"  filing lag (days): median {lag.median():.0f}, p90 {lag.quantile(0.9):.0f}, "
          f"{(lag > 60).sum()} over 60d, {n_bad} rows dropped for filing_date < trans_date")
    tv = buys["ticker"].value_counts()
    print(f"  purchase concentration: top name {tv.index[0]} {tv.iloc[0]} rows "
          f"({tv.iloc[0] / len(buys):.1%} of all purchases); top-5 "
          f"{tv.head(5).sum() / len(buys):.1%}")
    if buys["filing_date"].max() < pd.Timestamp("2026-06-01"):
        print(f"  DATA GAP: no insider data after {buys['filing_date'].max().date()} "
              f"(2026Q2+ not published as a data set; rerun with --crawl-q2 to fill).")

    buys["routine"] = tag_routine(buys)
    print(f"  routine purchases (same calendar month 3 prior years): "
          f"{buys['routine'].sum()} of {len(buys)} ({buys['routine'].mean():.1%})")

    sets = {"ALL": buys, "OPP": buys[~buys["routine"]]}
    sigs = {}
    for k, d in sets.items():
        s = cluster_signal_dates(d)
        sigs[k] = s
        print(f"\n[{k}] cluster signal-days {len(s)}, distinct tickers {s['ticker'].nunique()}")
    cy = pd.DataFrame({
        "purchases": buys.groupby(buys["filing_date"].dt.year).size(),
        "clusters_ALL": sigs["ALL"].groupby(sigs["ALL"]["signal_date"].dt.year).size(),
        "tickers_ALL": sigs["ALL"].groupby(sigs["ALL"]["signal_date"].dt.year)["ticker"].nunique(),
        "clusters_OPP": sigs["OPP"].groupby(sigs["OPP"]["signal_date"].dt.year).size(),
        "tickers_OPP": sigs["OPP"].groupby(sigs["OPP"]["signal_date"].dt.year)["ticker"].nunique(),
    }).fillna(0).astype(int)
    print("\nPer year:")
    print(cy.to_string())
    ns = sigs["ALL"]["n_insiders"]
    print(f"\ncluster size (ALL): 2 insiders {(ns == 2).sum()}, 3 {(ns == 3).sum()}, "
          f"4 {(ns == 4).sum()}, >=5 {(ns >= 5).sum()}, max {ns.max()}")
    top = sigs["ALL"]["ticker"].value_counts().head(8)
    print("most-clustered names: " + ", ".join(f"{t} {v}" for t, v in top.items()))
    print(f"  top name = {top.index[0]} at {top.iloc[0] / len(sigs['ALL']):.1%} of all "
          f"cluster signal-days; top-5 {top.head(5).sum() / len(sigs['ALL']):.1%}")
    hot = top.index[0]

    # ---------------- backtests ----------------
    start = pd.Timestamp(START)
    spy_r = spy_px.pct_change().fillna(0.0).loc[start:]
    base_r = backtest(px, rules_v1_weights(px), cost_bps=COST_BPS,
                      freq=FREQ)["returns"].loc[start:]
    # CONTROL, not a variant: equal weight EVERY tradable small cap that has a price, weekly.
    # This is the question idea 32 could not ask with a 4-8 name book - does picking the
    # cluster names beat owning the whole (survivorship-flattered) panel?
    alive = px.notna() & (px.shift(1).notna())
    ew_all = alive.astype(float).div(alive.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    ewp_r = backtest(px, ew_all, cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:]

    grid = [(f, h, c) for f in ("ALL", "OPP") for h in (6, 12) for c in (None, NAME_CAP)]
    res, rows = {}, []
    for f, h, c in grid:
        act = active_matrix(sigs[f], px, h)
        w = weights_from_active(act, c)
        r = backtest(px, w, cost_bps=COST_BPS, freq=FREQ)
        key = (f, h, c)
        res[key] = (r["returns"].loc[start:], r)
        rows.append(row(label(f, h, c), res[key][0], metrics))
    base_row = row("RULES v1 (small panel)", base_r, metrics)
    spy_row = row("SPY buy & hold", spy_r, metrics)
    ewp_row = row("EW all 439 small caps (control)", ewp_r, metrics)
    tbl = pd.DataFrame(rows + [base_row, spy_row, ewp_row]).set_index("name")
    print(f"\n=== Full sample {start.date()} -> {px.index[-1].date()}")
    print(tbl.to_string(float_format=lambda x: f"{x:.3f}"))

    print("\nVol / Sortino / Calmar:")
    for k in grid:
        m = metrics(res[k][0])
        print(f"  {label(*k):26s} vol {m['Vol']:.1%}  Sortino {m['Sortino']:.2f}  "
              f"Calmar {m['Calmar']:.2f}")
    for nm, rr in (("RULES v1", base_r), ("SPY", spy_r), ("EW all small caps", ewp_r)):
        m = metrics(rr)
        print(f"  {nm:26s} vol {m['Vol']:.1%}  Sortino {m['Sortino']:.2f}  "
              f"Calmar {m['Calmar']:.2f}")

    # ---------------- book size / concentration ----------------
    print("\nBook size and exposure (the thing idea 32 died on):")
    print(f"  {'arm':26s} {'gross':>7s} {'avg n':>7s} {'med n':>6s} {'max n':>6s} "
          f"{'<=5 names':>10s} {'cash':>6s} {'turn/yr':>8s}")
    booksz = {}
    for k in grid:
        w = res[k][1]["weights"].loc[start:]
        nn = (w > 1e-9).sum(axis=1)
        booksz[k] = nn
        yrs = metrics(res[k][0])["Years"]
        print(f"  {label(*k):26s} {w.sum(axis=1).mean():6.1%} {nn.mean():7.1f} "
              f"{nn.median():6.0f} {nn.max():6.0f} {(nn <= 5).mean():9.1%} "
              f"{(nn == 0).mean():5.1%} "
              f"{res[k][1]['turnover'].loc[start:].sum() / yrs:7.1f}x")

    # ---------------- drop-the-winner ----------------
    print("\nDrop-the-largest-contributor robustness (diagnostic, not a variant):")
    rets = px.pct_change().fillna(0.0)
    for k in grid:
        f, h, c = k
        w = res[k][1]["weights"].loc[start:]
        contrib = (w * rets.loc[start:]).sum(axis=0).sort_values(ascending=False)
        worst = contrib.index[0]
        s2 = sigs[f][sigs[f]["ticker"] != worst]
        r2 = backtest(px, weights_from_active(active_matrix(s2, px, h), c),
                      cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:]
        m2 = metrics(r2)
        hh = len(r2) // 2
        print(f"  {label(*k):26s} ex-{worst:<6s} CAGR {m2['CAGR']:6.1%}  "
              f"Sharpe {m2['Sharpe']:.2f}  MaxDD {m2['MaxDD']:6.1%}  halves "
              f"{metrics(r2.iloc[:hh])['Sharpe']:.2f} / {metrics(r2.iloc[hh:])['Sharpe']:.2f}"
              f"   (top-3: " + ", ".join(f"{t} {v:+.2f}" for t, v in contrib.head(3).items())
              + ")")

    # ---------------- ex the name that dominates the SIGNAL ----------------
    print(f"\nEx-{hot} (the name generating the most cluster signal-days) - diagnostic:")
    for k in grid:
        f, h, c = k
        s3 = sigs[f][sigs[f]["ticker"] != hot]
        r3 = backtest(px, weights_from_active(active_matrix(s3, px, h), c),
                      cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:]
        m3 = metrics(r3)
        hh = len(r3) // 2
        print(f"  {label(*k):26s} CAGR {m3['CAGR']:6.1%}  Sharpe {m3['Sharpe']:.2f}  "
              f"MaxDD {m3['MaxDD']:6.1%}  halves {metrics(r3.iloc[:hh])['Sharpe']:.2f} / "
              f"{metrics(r3.iloc[hh:])['Sharpe']:.2f}")

    # ---------------- vs the EW-panel control ----------------
    print("\nvs the EW-all-small-caps control (same panel, same costs, no insider signal):")
    ewm = metrics(ewp_r)
    for k in grid:
        m = metrics(res[k][0])
        d = res[k][0] - ewp_r
        t = d.mean() / d.std() * np.sqrt(len(d)) if d.std() else np.nan
        print(f"  {label(*k):26s} dCAGR {m['CAGR'] - ewm['CAGR']:+6.2%}  "
              f"dSharpe {m['Sharpe'] - ewm['Sharpe']:+.3f}  "
              f"daily excess t {t:+.2f}  corr {res[k][0].corr(ewp_r):.3f}")

    # ---------------- calendar years ----------------
    print("\nCalendar-year returns:")
    yr = pd.DataFrame({label(*k): res[k][0] for k in grid}
                      | {"RULESv1": base_r, "SPY": spy_r, "EWsmall": ewp_r})
    print(yr.groupby(yr.index.year).apply(lambda x: (1 + x).prod() - 1)
            .to_string(float_format=lambda v: f"{v:+.1%}"))

    # ---------------- walk-forward (rule 8) ----------------
    print(f"\n=== Walk-forward: hold chosen on {START}..{IS_END}, evaluated on {OOS_START}..")
    wf = []
    for k in grid:
        r = res[k][0]
        ins, oos = r.loc[:IS_END], r.loc[OOS_START:]
        wf.append(dict(name=label(*k), IS_Sharpe=metrics(ins)["Sharpe"],
                       IS_CAGR=metrics(ins)["CAGR"], OOS_Sharpe=metrics(oos)["Sharpe"],
                       OOS_CAGR=metrics(oos)["CAGR"], OOS_MaxDD=metrics(oos)["MaxDD"]))
    for nm, rr in (("RULES v1 (small panel)", base_r), ("SPY", spy_r),
                   ("EW all small caps (control)", ewp_r)):
        ins, oos = rr.loc[:IS_END], rr.loc[OOS_START:]
        wf.append(dict(name=nm, IS_Sharpe=metrics(ins)["Sharpe"], IS_CAGR=metrics(ins)["CAGR"],
                       OOS_Sharpe=metrics(oos)["Sharpe"], OOS_CAGR=metrics(oos)["CAGR"],
                       OOS_MaxDD=metrics(oos)["MaxDD"]))
    print(pd.DataFrame(wf).set_index("name").to_string(float_format=lambda x: f"{x:.3f}"))
    # selection rule, fixed before looking at OOS: highest IS Sharpe within each (filter,cap)
    # family, ties -> shorter hold.  hold is the only tuned parameter.
    print("IS picks (highest IS Sharpe over hold, tie -> 6m):")
    picks = {}
    for f in ("ALL", "OPP"):
        for c in (None, NAME_CAP):
            best = max((6, 12), key=lambda h: (metrics(res[(f, h, c)][0].loc[:IS_END])["Sharpe"],
                                               -h))
            picks[(f, c)] = best
            print(f"  {f} cap={'5%' if c else 'none':4s} -> hold={best}m  "
                  f"OOS Sharpe {metrics(res[(f, best, c)][0].loc[OOS_START:])['Sharpe']:.3f}")

    # ---------------- verdicts / leaderboard ----------------
    oos_spy = metrics(spy_r.loc[OOS_START:])["Sharpe"]
    print(f"\nSPY OOS Sharpe {oos_spy:.3f} | 4b caps: MaxDD >= {0.60 * spy_row['MaxDD']:.1%}, "
          f"CAGR >= {0.70 * spy_row['CAGR']:.1%}")
    print("\n=== LEADERBOARD rows")
    lines = []
    for i, k in enumerate(grid):
        d = rows[i]
        oos_s = metrics(res[k][0].loc[OOS_START:])["Sharpe"]
        v = verdict(d, base_row, spy_row, oos_s, oos_spy)
        line = (f"| 2026-09-04 | 50 {d['name']} | {d['CAGR']:.1%} | {d['Sharpe']:.2f} "
                f"| {d['MaxDD']:.1%} | {d['H1']:.2f} / {d['H2']:.2f} "
                f"| {base_row['Sharpe']:.2f} ({base_row['H1']:.2f}/{base_row['H2']:.2f}) "
                f"| {v} | research/backtests/{SCRIPT} |")
        lines.append(line)
        print(line)
    for nm, d in ((f"RULES v1 on the small panel, {START[:4]}+ - reference", base_row),
                  (f"SPY buy & hold, {START[:4]}+ - reference", spy_row),
                  (f"EW all 439 small caps, {START[:4]}+ - CONTROL", ewp_row)):
        line = (f"| 2026-09-04 | 50 {nm} | {d['CAGR']:.1%} | {d['Sharpe']:.2f} "
                f"| {d['MaxDD']:.1%} | {d['H1']:.2f} / {d['H2']:.2f} "
                f"| {base_row['Sharpe']:.2f} ({base_row['H1']:.2f}/{base_row['H2']:.2f}) "
                f"| - | research/backtests/{SCRIPT} |")
        lines.append(line)
        print(line)
    return tbl, cy, lines


def label(f, h, c):
    return f"insider-cluster {f} hold={h}m {'cap5%' if c else 'EW100%'}"


if __name__ == "__main__":
    main()
