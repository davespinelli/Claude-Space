#!/usr/bin/env python3
"""Idea 32 - "insider cluster buying" (Cohen, Malloy & Pomorski 2012, *Decoding Inside
Information*, JF 67(3)).

CMP split insider trades into "routine" (an insider who trades the same calendar month
every year) and "opportunistic".  Only opportunistic trades predict returns, and the
strongest version of the effect in the earlier literature (Lakonishok-Lee 2001; Jeng-Metrick-
Zeckhauser 2003) is CLUSTER buying: several *different* insiders at the same firm buying on
the open market inside a short window.  This script tests the cluster leg directly on the
broad universe.

Signal
------
Qualifying purchase  = Form 4, non-derivative table, transaction code P (open-market buy),
                       acquired (A), shares x price >= $10,000.
Cluster              = >= 2 DISTINCT reporting owners with qualifying purchases whose
                       TRANSACTION dates fall inside a 30 calendar-day window.
Signal date          = max(filing_date) of the two filings that complete the cluster, so the
                       signal is only ever used once both Form 4s are public (Form 4 is due
                       within 2 business days of the trade, so this is a 0-4 day lag).
Strategy             = weekly rebalance; hold every ticker whose most recent cluster signal
                       date is within the last 30 calendar days, equal weight, gross 100%
                       (cash when there is no cluster anywhere), for HOLD months.
                       HOLD in {6, 12}.  10 bps per unit turnover, next-day execution.

Nothing else is tuned.  The two parameters are HOLD (6 vs 12 months) and the cluster
lookback (fixed at 30 days by the idea's own definition, not searched).

Data
----
Prices: baseline.load_universe(broad=True) -> research/universe_broad.json (136 names).
SURVIVORSHIP: universe_broad.json is TODAY's constituent list, so the price panel is
survivorship-biased upward; every number below inherits that bias.

Insider data: data/form4_purchases.csv, built once and cached.  Two sources, because a
pure per-filing crawl is not feasible:

  * The 108 non-ETF names in the universe filed 128,930 Form 4s between 2012-01-01 and
    today.  Restricting to ticker-months with >= 2 filings (the pre-filter the brief asked
    for) removes almost nothing - 126,987 remain - because large caps file 4s continuously
    for grants, vesting and 10b5-1 sales.  At the SEC's <= 8 req/s that crawl is ~4.4 hours,
    and the 6,000-download cap the brief set would have sampled 4.7% of filings, which
    cannot detect a "2 insiders in 30 days" event at all: with a 4.7% sample the chance of
    catching BOTH legs of a genuine cluster is ~0.2%.  A 6,000-filing crawl would have
    produced a near-empty signal and a meaningless backtest.
  * So 2012-01-01 -> 2026-03-31 comes from the SEC's own structured Form 345 data sets
    (https://www.sec.gov/files/structureddata/data/insider-transactions-data-sets/
    <YYYY>q<N>_form345.zip) - 57 quarterly files, 57 requests.  These are the SEC's parse of
    exactly the same Form 4 XML, with TRANS_CODE / TRANS_SHARES / TRANS_PRICEPERSHARE per
    non-derivative transaction and RPTOWNERCIK per filing.  Latest published quarter is
    2026Q1.
  * 2026-04-01 -> today is not published as a data set yet, so it IS crawled per filing via
    https://data.sec.gov/submissions/CIK##########.json (+ the older filings.files shards)
    and parsed with research/deepvalue/fetch_filings.parse_form4 - 3,016 filings found, 2,911
    after the briefed >=2-per-ticker-month pre-filter, all 2,911 downloaded, inside the 6,000
    cap (--xml-cap bounds it).  48 of the 2,600 final rows; the data sets supply the 2,552.

  SKIPPED / NOT DOWNLOADED: the ~126k individual Form 4 XML documents dated before
  2026-04-01.  They are covered by the SEC data sets instead.  --parse-check validates that
  substitution OFFLINE (the two sources do not overlap in time, and re-crawling a sample of
  the pre-2026Q2 filings draws HTTP 503s after a build this size): it runs parse_form4 over
  the 1,092 Form 4 XML already cached by the deep-value pipeline and compares them with the
  same accessions in the cached quarterly data sets.  525 accessions are in both; all 525
  agree on total code-P purchase value to within 1%, 0 disagree.

Verdicts (PROTOCOL rule 4)
-------------------------
4a  Sharpe > RULES v1 in BOTH halves and MaxDD no worse than RULES v1.
4b  Sharpe > SPY in BOTH halves AND out-of-sample, MaxDD <= 60% of SPY's, CAGR >= 70% of
    SPY's.
Rule 8 walk-forward: parameters chosen on 2012-2018 only, evaluated untouched on 2019-2026
(the sample starts in 2012 because Form 4 XML coverage before then is patchy, so the
2009-2016 / 2017-2026 split in the protocol is shifted to fit the data - stated here rather
than silently).

Usage
-----
    python 2026-09-04_insider-cluster-buying.py              # uses the cache
    python 2026-09-04_insider-cluster-buying.py --build      # (re)build data/form4_purchases.csv
    python 2026-09-04_insider-cluster-buying.py --parse-check # cross-check bulk vs XML parse

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
SUBS_DIR = CACHE_DIR / "submissions"
XML_DIR = CACHE_DIR / "form4xml"
PURCHASES = REPO / "data" / "form4_purchases.csv"

START = "2012-01-01"
BULK_LAST_Q = (2026, 1)          # last published quarterly data set
XML_FROM = "2026-04-01"          # crawl per-filing from here on
MIN_VALUE = 10_000.0             # $ threshold for a qualifying purchase
CLUSTER_DAYS = 30                # >= 2 distinct insiders inside this window
SIGNAL_DAYS = 30                 # "cluster in the last 30 days" entry rule
COST_BPS = 10
FREQ = "W"
IS_END = "2018-12-31"            # rule-8 walk-forward split
OOS_START = "2019-01-01"
SCRIPT = Path(__file__).name


# =========================================================================
# 1. data build
# =========================================================================
def norm_symbol(s) -> str:
    """'NYSE:BRK.B' -> 'BRK-B'.  Blank / NaN symbols (a few thousand filings) -> ''."""
    if not isinstance(s, str):
        return ""
    s = s.strip().upper()
    if ":" in s:
        s = s.split(":")[-1]
    return s.replace(".", "-").replace(" ", "-")


def universe_cik_map(tickers) -> dict[str, str]:
    """{zero-padded issuer CIK -> ticker} for the names SEC's ticker file knows about.
    Used only as a fallback when ISSUERTRADINGSYMBOL is blank; symbol matching is primary
    because it survives CIK changes (e.g. XOM's 2025 holdco reorganisation, under which the
    current ticker file points XOM at a CIK with no pre-2025 filings)."""
    from fetch_filings import fetch, TICKERS_URL
    raw = fetch(TICKERS_URL, CACHE_DIR, "company_tickers.json")
    m = {}
    for v in json.loads(raw).values():
        t = norm_symbol(v["ticker"])
        if t in set(tickers):
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
    """Pull the SEC quarterly Form 345 data sets and keep qualifying code-P purchases."""
    from fetch_filings import fetch          # reuse the throttled/cached session
    zdir = CACHE_DIR / "form345"
    zdir.mkdir(parents=True, exist_ok=True)
    cikmap = universe_cik_map(universe)
    frames = []
    for y, q in quarters():
        tag = f"{y}q{q}"
        url = (f"https://www.sec.gov/files/structureddata/data/"
               f"insider-transactions-data-sets/{tag}_form345.zip")
        raw = fetch(url, zdir, f"{tag}_form345.zip", binary=True)
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
                    print(f"  {tag}: 0 universe filings")
                continue
            accs = set(sub["ACCESSION_NUMBER"])
            tr = _read_tsv(zf, "NONDERIV_TRANS.tsv",
                           ["ACCESSION_NUMBER", "TRANS_DATE", "TRANS_CODE", "TRANS_SHARES",
                            "TRANS_PRICEPERSHARE", "TRANS_ACQUIRED_DISP_CD"])
            tr = tr[tr["ACCESSION_NUMBER"].isin(accs) & (tr["TRANS_CODE"] == "P")
                    & (tr["TRANS_ACQUIRED_DISP_CD"] == "A")]
            if tr.empty:
                if verbose:
                    print(f"  {tag}: {len(sub):5d} filings ->     0 purchases")
                continue
            own = _read_tsv(zf, "REPORTINGOWNER.tsv",
                            ["ACCESSION_NUMBER", "RPTOWNERCIK", "RPTOWNERNAME",
                             "RPTOWNER_RELATIONSHIP"])
            own = own[own["ACCESSION_NUMBER"].isin(set(tr["ACCESSION_NUMBER"]))]
            # a joint Form 4 (rare) is one acting entity: join its owner CIKs
            own = (own.sort_values(["ACCESSION_NUMBER", "RPTOWNERCIK"])
                      .groupby("ACCESSION_NUMBER")
                      .agg(owner_cik=("RPTOWNERCIK", lambda s: "+".join(sorted(set(s)))),
                           owner_name=("RPTOWNERNAME", lambda s: " / ".join(dict.fromkeys(s))),
                           relationship=("RPTOWNER_RELATIONSHIP",
                                         lambda s: " / ".join(dict.fromkeys(s.fillna("")))))
                      .reset_index())
        df = tr.merge(sub[["ACCESSION_NUMBER", "ticker", "FILING_DATE"]],
                      on="ACCESSION_NUMBER").merge(own, on="ACCESSION_NUMBER", how="left")
        df["shares"] = pd.to_numeric(df["TRANS_SHARES"], errors="coerce")
        df["price"] = pd.to_numeric(df["TRANS_PRICEPERSHARE"], errors="coerce")
        df["filing_date"] = pd.to_datetime(df["FILING_DATE"], format="%d-%b-%Y",
                                           errors="coerce")
        df["trans_date"] = pd.to_datetime(df["TRANS_DATE"], format="%d-%b-%Y",
                                          errors="coerce")
        df = df.rename(columns={"ACCESSION_NUMBER": "accession"})
        df["source"] = "sec_dataset"
        frames.append(df[["ticker", "filing_date", "trans_date", "owner_cik", "owner_name",
                          "relationship", "shares", "price", "accession", "source"]])
        if verbose:
            print(f"  {tag}: {len(sub):5d} filings -> {len(df):5d} purchase rows", flush=True)
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()


def build_from_xml(universe_tickers, xml_cap=6000, verbose=True) -> pd.DataFrame:
    """Crawl submissions JSON + Form 4 XML for the period the data sets do not cover yet."""
    from fetch_filings import (fetch, ticker_to_cik, get_submissions, parse_form4,
                               filing_dir_url, filing_documents)
    SUBS_DIR.mkdir(parents=True, exist_ok=True)
    XML_DIR.mkdir(parents=True, exist_ok=True)
    # ---- enumerate every Form 4 filed on/after XML_FROM
    todo, skipped_ciks = [], []
    for t in universe_tickers:
        try:
            cik, _ = ticker_to_cik(t, CACHE_DIR)
            sub = get_submissions(cik, SUBS_DIR)
        except Exception as exc:
            skipped_ciks.append((t, str(exc)[:50]))
            continue
        def take(rec):
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
    # the brief's pre-filter: clusters need >= 2 filings, so drop ticker-months with only 1
    cnt = pd.Series([f"{t}|{d[:7]}" for t, _, d, _, _ in todo]).value_counts()
    keep_keys = set(cnt[cnt >= 2].index)
    todo = [r for r in todo if f"{r[0]}|{r[2][:7]}" in keep_keys]
    n_pref = len(todo)
    skipped_cap = max(0, n_pref - xml_cap)
    todo = todo[:xml_cap]
    if verbose:
        print(f"  XML window {XML_FROM}+: {n_all} filings, {n_pref} after the >=2/month "
              f"pre-filter, downloading {len(todo)} (cap {xml_cap}, skipped {skipped_cap})")
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
            if r["table"] != "non-derivative" or r["code"] != "P" or r["acquired_disposed"] != "A":
                continue
            rows.append(dict(ticker=t, filing_date=fdate, trans_date=r["transaction_date"],
                             owner_cik=r["owner"], owner_name=r["owner"],
                             relationship=r["relationship"],
                             shares=r["shares"], price=r["price"], accession=acc,
                             source="form4_xml"))
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


def build_cache(xml_cap=6000):
    tickers = json.loads((REPO / "research" / "universe_broad.json").read_text())
    uni = set(tickers)
    print(f"building {PURCHASES.name} for {len(tickers)} tickers, {START} -> today")
    bulk = build_from_bulk(uni)
    print(f"  bulk rows: {len(bulk)}")
    xml = build_from_xml(tickers, xml_cap=xml_cap)
    print(f"  xml  rows: {len(xml)}")
    df = pd.concat([bulk, xml], ignore_index=True)
    df = df[(df["filing_date"] >= START) & df["shares"].notna() & df["price"].notna()]
    df["value"] = df["shares"] * df["price"]
    df = df[df["value"] >= MIN_VALUE]
    df["trans_date"] = df["trans_date"].fillna(df["filing_date"])
    # amendments / duplicate reports of the same trade
    df = (df.sort_values(["ticker", "trans_date", "owner_cik", "accession"])
            .drop_duplicates(["ticker", "owner_cik", "trans_date", "shares", "price"]))
    df.to_csv(PURCHASES, index=False)
    print(f"  wrote {PURCHASES} ({len(df)} qualifying purchases, "
          f"{df['ticker'].nunique()} tickers)")
    if xml.attrs.get("skipped"):
        print("  skipped:", xml.attrs["skipped"])
    return df


def parse_check(verbose=True):
    """Cross-check the SEC data sets against research/deepvalue/fetch_filings.parse_form4 on
    the SAME accessions, entirely offline.

    The two sources in data/form4_purchases.csv do not overlap in time, so they cannot be
    compared against each other directly, and re-crawling a sample of the 126k pre-2026Q2
    filings runs into SEC rate limiting (503s) after a build this size.  Instead this uses the
    Form 4 XML already cached by the deep-value pipeline under
    research/deepvalue/filings/<T>/raw/ - a different (small-cap) universe, but the same
    document format and the same quarters, so it tests exactly the thing the substitution rests
    on: does the SEC's structured extract of code-P non-derivative purchases agree with
    parse_form4's extract of the same filing?  No network requests.
    """
    import glob
    from fetch_filings import parse_form4
    zdir = CACHE_DIR / "form345"
    xmls = sorted(glob.glob(str(REPO / "research/deepvalue/filings/*/raw/*.xml")))
    parsed = {}
    for path in xmls:
        raw = Path(path).read_bytes()
        if b"<ownershipDocument" not in raw[:4000]:
            continue
        acc = Path(path).name.split("_")[0]
        rows = [r for r in parse_form4(raw, "", acc)
                if r["table"] == "non-derivative" and r["code"] == "P"
                and r["acquired_disposed"] == "A"]
        val = sum(_num(r["shares"]) * _num(r["price"]) for r in rows)
        parsed[acc] = val
    if verbose:
        print(f"PARSE_CHECK: {len(parsed)} Form 4 XML documents available offline")
    # pull the same accessions out of every cached quarterly data set
    bulk = {}
    for z in sorted(zdir.glob("*_form345.zip")):
        try:
            with zipfile.ZipFile(z) as zf:
                sub = _read_tsv(zf, "SUBMISSION.tsv", ["ACCESSION_NUMBER", "DOCUMENT_TYPE"])
                accs = set(sub["ACCESSION_NUMBER"]) & set(parsed)
                if not accs:
                    continue
                tr = _read_tsv(zf, "NONDERIV_TRANS.tsv",
                               ["ACCESSION_NUMBER", "TRANS_CODE", "TRANS_SHARES",
                                "TRANS_PRICEPERSHARE", "TRANS_ACQUIRED_DISP_CD"])
                tr = tr[tr["ACCESSION_NUMBER"].isin(accs) & (tr["TRANS_CODE"] == "P")
                        & (tr["TRANS_ACQUIRED_DISP_CD"] == "A")]
                tr["v"] = (pd.to_numeric(tr["TRANS_SHARES"], errors="coerce")
                           * pd.to_numeric(tr["TRANS_PRICEPERSHARE"], errors="coerce"))
                for a in accs:
                    bulk[a] = float(tr.loc[tr["ACCESSION_NUMBER"] == a, "v"].sum())
        except zipfile.BadZipFile:
            continue
    shared = sorted(bulk)
    ok = sum(1 for a in shared
             if abs(bulk[a] - parsed[a]) <= max(1.0, 0.01 * max(bulk[a], parsed[a])))
    bad = [a for a in shared if abs(bulk[a] - parsed[a]) > max(1.0, 0.01 * max(bulk[a], parsed[a]))]
    nz = sum(1 for a in shared if parsed[a] > 0)
    print(f"PARSE_CHECK: {len(shared)} accessions present in BOTH the cached SEC data sets and "
          f"the cached Form 4 XML ({nz} of them contain a code-P purchase); "
          f"{ok} agree on total purchase value to within 1%, {len(bad)} disagree.")
    for a in bad[:10]:
        print(f"    disagree {a}: dataset {bulk[a]:.2f} vs parse_form4 {parsed[a]:.2f}")
    return ok, len(bad), len(shared)


def _num(x):
    try:
        return float(str(x).replace(",", "").replace("$", ""))
    except Exception:
        return 0.0


# =========================================================================
# 2. signal
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
            # first moment the pair is public: the earliest partner minimises the wait
            sig = min(max(fd[i], fd[j]) for j in partners)
            n_ins = len({ow[i]} | {ow[j] for j in partners})
            out.append((t, pd.Timestamp(sig), n_ins))
    s = pd.DataFrame(out, columns=["ticker", "signal_date", "n_insiders"])
    if s.empty:
        return s
    return (s.groupby(["ticker", "signal_date"], as_index=False)["n_insiders"].max()
             .sort_values(["signal_date", "ticker"]))


def make_weights(signals: pd.DataFrame, hold_months: int):
    """Hold every ticker with a cluster signal in the last SIGNAL_DAYS, for hold_months."""
    hold_days = int(round(hold_months * 30.4375))

    def fn(px: pd.DataFrame) -> pd.DataFrame:
        active = pd.DataFrame(False, index=px.index, columns=px.columns)
        idx = px.index
        for t, g in signals.groupby("ticker"):
            if t not in active.columns:
                continue
            col = np.zeros(len(idx), dtype=bool)
            for sd in g["signal_date"]:
                # entry rule: the cluster must be <= SIGNAL_DAYS old when it is picked up,
                # then the position is held hold_days from the signal
                lo = idx.searchsorted(sd)
                hi = idx.searchsorted(sd + pd.Timedelta(days=hold_days))
                if lo < len(idx):
                    col[lo:hi] = True
            active[t] = col
        n = active.sum(axis=1)
        w = active.astype(float).div(n.where(n > 0, np.nan), axis=0).fillna(0.0)
        return w
    return fn


# =========================================================================
# 3. evaluation
# =========================================================================
def trading_days(px):
    """Defensive: drop weekends / no-move forward-filled rows (see idea 38's data note)."""
    r = px.pct_change().fillna(0.0)
    keep = (px.index.dayofweek < 5) & (((r != 0).sum(axis=1) > 0) | (np.arange(len(px)) == 0))
    return px[keep]


def half_sharpes(r, metrics):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def row(name, r, metrics):
    m = metrics(r)
    h1, h2 = half_sharpes(r, metrics)
    return dict(name=name, CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=h1, H2=h2)


def verdict(idea, base, spy, oos_sharpe=None, oos_spy=None):
    """PROTOCOL 4a / 4b, plus the PARK case rule 4 allows.

    PARK (rather than KILL) is returned when the idea beats SPY on Sharpe in BOTH halves and
    out-of-sample - i.e. the signal itself is there - but fails 4b only on the risk caps
    (MaxDD <= 60% of SPY's / CAGR >= 70% of SPY's).  That is "interesting, needs more work",
    not "no edge".  It is a report, not a licence to tune: the fix (sizing) is named in the
    memo and deliberately NOT run here."""
    a = (idea["H1"] > base["H1"] and idea["H2"] > base["H2"]
         and idea["MaxDD"] >= base["MaxDD"])
    sharpe_ok = idea["H1"] > spy["H1"] and idea["H2"] > spy["H2"]
    if oos_sharpe is not None and oos_spy is not None:
        sharpe_ok = sharpe_ok and oos_sharpe > oos_spy
    risk_ok = (idea["MaxDD"] >= 0.60 * spy["MaxDD"]        # MaxDD are negative
               and idea["CAGR"] >= 0.70 * spy["CAGR"])
    b = sharpe_ok and risk_ok
    if a and b:
        return "KEEP (4a+4b)"
    if a:
        return "KEEP (4a)"
    if b:
        return "KEEP (4b)"
    if sharpe_ok:
        return "PARK (4b: Sharpe yes, MaxDD no)"
    return "KILL"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--build", action="store_true", help="(re)build data/form4_purchases.csv")
    ap.add_argument("--xml-cap", type=int, default=6000)
    ap.add_argument("--parse-check", action="store_true")
    args = ap.parse_args()

    if args.build or not PURCHASES.exists():
        build_cache(xml_cap=args.xml_cap)
    if args.parse_check:
        parse_check()
        return

    from baseline import load_universe, rules_v1_weights
    from engine import backtest, metrics

    buys = pd.read_csv(PURCHASES, parse_dates=["filing_date", "trans_date"])
    print(f"purchases: {len(buys)} rows, {buys['ticker'].nunique()} tickers, "
          f"{buys['filing_date'].min().date()} -> {buys['filing_date'].max().date()}")
    print("\nQualifying purchases (code P, >= $10k) per year:")
    print(buys.groupby(buys["filing_date"].dt.year).size().to_string())

    sig = cluster_signal_dates(buys)
    print(f"\nCluster signal days: {len(sig)}  "
          f"(distinct tickers {sig['ticker'].nunique() if len(sig) else 0})")
    print("\nClusters per year (distinct ticker-signal-days):")
    cy = sig.groupby(sig["signal_date"].dt.year).agg(clusters=("ticker", "size"),
                                                     tickers=("ticker", "nunique"))
    print(cy.to_string())

    px = trading_days(load_universe(broad=True, start="2010-01-01"))
    dropped = [c for c in px.columns if px[c].notna().sum() == 0]
    px = px.loc[:, px.notna().sum() > 0]
    print(f"\nprices: {px.shape[0]} rows x {px.shape[1]} tickers, "
          f"{px.index[0].date()} -> {px.index[-1].date()}"
          + (f"  (no price history, dropped: {dropped})" if dropped else ""))
    print("  rows per year: "
          + " ".join(f"{y}:{n}" for y, n in
                     px.index.to_series().groupby(px.index.year).count().items()))
    miss = sorted(set(sig["ticker"]) - set(px.columns)) if len(sig) else []
    if miss:
        print(f"  clusters on tickers with no price column (ignored): {miss}")

    start = pd.Timestamp(START)
    spy_r = px["SPY"].pct_change().fillna(0.0).loc[start:]
    base_r = backtest(px, rules_v1_weights(px), cost_bps=COST_BPS,
                      freq=FREQ)["returns"].loc[start:]

    results, rows = {}, []
    for hold in (6, 12):
        res = backtest(px, make_weights(sig, hold)(px), cost_bps=COST_BPS, freq=FREQ)
        r = res["returns"].loc[start:]
        results[hold] = (r, res)
        rows.append(row(f"insider-cluster hold={hold}m", r, metrics))
    rows.append(row("RULES v1 baseline", base_r, metrics))
    rows.append(row("SPY buy & hold", spy_r, metrics))
    tbl = pd.DataFrame(rows).set_index("name")
    print("\n=== Full sample " + str(start.date()) + " -> " + str(px.index[-1].date()))
    print(tbl.to_string(float_format=lambda x: f"{x:.3f}"))
    print("\nVol / Sortino / Calmar:")
    for nm, rr in (("hold=6m", results[6][0]), ("hold=12m", results[12][0]),
                   ("RULES v1", base_r), ("SPY", spy_r)):
        m = metrics(rr)
        print(f"  {nm:9s} vol {m['Vol']:.1%}  Sortino {m['Sortino']:.2f}  "
              f"Calmar {m['Calmar']:.2f}")

    # ---------------- concentration diagnostics ----------------
    # This is the crux of the verdict: how many names is the book actually holding, and how
    # much of the result is one ticker?  A 100%-gross equal-weight book over a handful of
    # names is a concentrated bet, not a factor.
    print("\nExposure / concentration:")
    rets = px.pct_change().fillna(0.0)
    contrib = {}
    for hold in (6, 12):
        w = results[hold][1]["weights"].loc[start:]
        nn = (w > 0).sum(axis=1)
        print(f"  hold={hold:2d}m  gross {w.sum(axis=1).mean():.1%}  avg names {nn.mean():.1f}"
              f"  median {nn.median():.0f}  days with <=2 names {(nn <= 2).mean():.1%}"
              f"  days in cash {(nn == 0).mean():.1%}"
              f"  turnover/yr {results[hold][1]['turnover'].loc[start:].sum() / metrics(results[hold][0])['Years']:.1f}x")
        c = (w * rets.loc[start:]).sum(axis=0).sort_values(ascending=False)
        contrib[hold] = c
        top = c.head(5)
        print(f"      top-5 gross return contribution: "
              + ", ".join(f"{t} {v:+.2f}" for t, v in top.items())
              + f"  (sum of all {c.sum():+.2f})")

    # drop-the-winner robustness: re-run with the single largest contributor removed
    print("\nDrop-the-largest-contributor robustness (diagnostic, not a variant):")
    for hold in (6, 12):
        worst = contrib[hold].index[0]
        s2 = sig[sig["ticker"] != worst]
        r2 = backtest(px, make_weights(s2, hold)(px), cost_bps=COST_BPS,
                      freq=FREQ)["returns"].loc[start:]
        m2 = metrics(r2)
        h = len(r2) // 2
        print(f"  hold={hold:2d}m  ex-{worst}: CAGR {m2['CAGR']:.1%}  Sharpe {m2['Sharpe']:.2f}"
              f"  MaxDD {m2['MaxDD']:.1%}  halves "
              f"{metrics(r2.iloc[:h])['Sharpe']:.2f} / {metrics(r2.iloc[h:])['Sharpe']:.2f}")

    # Vol-matched diagnostic: scale each book by ONE full-sample constant so its vol equals
    # SPY's.  Uses full-sample information, so it is a diagnostic and NOT tradable - it only
    # answers "is the excess return compensation for taking more risk, or something else?"
    print("\nVol-matched to SPY (full-sample constant scalar - diagnostic, not tradable):")
    tv = metrics(spy_r)["Vol"]
    for nm, rr in (("hold=6m", results[6][0]), ("hold=12m", results[12][0]),
                   ("RULES v1", base_r), ("SPY", spy_r)):
        c = tv / metrics(rr)["Vol"]
        m = metrics(rr * c)
        print(f"  {nm:9s} x{c:.2f} -> CAGR {m['CAGR']:.1%}  Sharpe {m['Sharpe']:.2f}  "
              f"MaxDD {m['MaxDD']:.1%}")

    print("\nCalendar-year returns:")
    yr = pd.DataFrame({"hold=6m": results[6][0], "hold=12m": results[12][0],
                       "RULESv1": base_r, "SPY": spy_r})
    print(yr.groupby(yr.index.year).apply(lambda x: (1 + x).prod() - 1)
            .to_string(float_format=lambda v: f"{v:+.1%}"))

    # ---------------- walk-forward (rule 8) ----------------
    print(f"\n=== Walk-forward: parameters chosen on {START}..{IS_END}, "
          f"evaluated on {OOS_START}..")
    wf = []
    for hold in (6, 12):
        r = results[hold][0]
        ins, oos = r.loc[:IS_END], r.loc[OOS_START:]
        wf.append(dict(name=f"hold={hold}m",
                       IS_Sharpe=metrics(ins)["Sharpe"], IS_CAGR=metrics(ins)["CAGR"],
                       OOS_Sharpe=metrics(oos)["Sharpe"], OOS_CAGR=metrics(oos)["CAGR"],
                       OOS_MaxDD=metrics(oos)["MaxDD"]))
    for nm, rr in (("RULES v1", base_r), ("SPY", spy_r)):
        ins, oos = rr.loc[:IS_END], rr.loc[OOS_START:]
        wf.append(dict(name=nm, IS_Sharpe=metrics(ins)["Sharpe"], IS_CAGR=metrics(ins)["CAGR"],
                       OOS_Sharpe=metrics(oos)["Sharpe"], OOS_CAGR=metrics(oos)["CAGR"],
                       OOS_MaxDD=metrics(oos)["MaxDD"]))
    wtbl = pd.DataFrame(wf).set_index("name")
    print(wtbl.to_string(float_format=lambda x: f"{x:.3f}"))
    pick = max((6, 12), key=lambda h: metrics(results[h][0].loc[:IS_END])["Sharpe"])
    print(f"IS selection rule (highest IS Sharpe, tie -> smaller hold): hold={pick}m")

    # ---------------- verdicts ----------------
    base_row, spy_row = rows[-2], rows[-1]
    oos_spy = metrics(spy_r.loc[OOS_START:])["Sharpe"]
    print("\n=== LEADERBOARD rows")
    lines = []
    for i, hold in enumerate((6, 12)):
        d = rows[i]
        oos_s = metrics(results[hold][0].loc[OOS_START:])["Sharpe"]
        v = verdict(d, base_row, spy_row, oos_s, oos_spy)
        line = (f"| {pd.Timestamp('2026-09-04').date()} | insider-cluster-buying hold={hold}m "
                f"| {d['CAGR']:.1%} | {d['Sharpe']:.2f} | {d['MaxDD']:.1%} "
                f"| {d['H1']:.2f} / {d['H2']:.2f} "
                f"| {base_row['Sharpe']:.2f} ({base_row['H1']:.2f}/{base_row['H2']:.2f}) "
                f"| {v} | research/backtests/{SCRIPT} |")
        lines.append(line)
        print(line)
    for nm, d in (("RULES v1 baseline (2012+ sample) - reference", base_row),
                  ("SPY buy & hold (2012+ sample) - reference", spy_row)):
        line = (f"| 2026-09-04 | {nm} | {d['CAGR']:.1%} | {d['Sharpe']:.2f} | {d['MaxDD']:.1%} "
                f"| {d['H1']:.2f} / {d['H2']:.2f} "
                f"| {base_row['Sharpe']:.2f} ({base_row['H1']:.2f}/{base_row['H2']:.2f}) "
                f"| - | research/backtests/{SCRIPT} |")
        lines.append(line)
        print(line)
    return tbl, wtbl, cy, lines


if __name__ == "__main__":
    main()
