#!/usr/bin/env python3
"""Idea 36 — spin-off calendar from EDGAR.

A US spin-off registers the new company's shares on **Form 10-12B** (Securities
Exchange Act Section 12(b), i.e. a listed security), amended as 10-12B/A. This
script enumerates every 10-12B / 10-12B/A filed from 2015 to today via EDGAR
full-text search, collapses them to one row per registrant, then enriches each
registrant from its EDGAR submissions feed to find a ticker and an estimated
distribution / first-listing date.

EDGAR full-text search
----------------------
    https://efts.sec.gov/LATEST/search-index?q=&forms=10-12B&startdt=..&enddt=..&from=..

An **empty** `q` with a `forms` filter is the exhaustive form-type listing: for
2024Q1 it returns exactly the 11 filings that appear in the quarterly full index
(`.../full-index/2024/QTR1/form.idx`), one hit per filing rather than one per
attached document. A non-empty `q` (e.g. "Form 10") is *narrower* — it only
matches documents containing the phrase — and returns one hit per document, so
it needs accession-level dedupe and still misses filings. We therefore query
quarter by quarter with an empty `q`, splitting to months if a quarter should
ever exceed the 100-hit page size.

Distribution date
-----------------
Form 10 registration is effective 60 days after filing, which is a poor proxy for
the actual distribution. Better markers, in the order we prefer them:

  1. **CERT** — the exchange's certification approving the listing. Filed days
     before the shares start trading (GE Vernova: CERT 2024-03-07, spun 2024-04-02).
  2. **8-A12B** — the registrant's own listing registration.
  3. The first **8-K** filed after the registration, with its item numbers kept so
     a reader can see whether it is item 2.01 (completion of disposition), 5.02
     (officers) etc.
  4. **25-NSE** is recorded when present but is a *delisting* notice, so it marks
     the end of a listing, not the start; it is carried for completeness only.

The honest event date for a backtest is the security's first traded day, which the
companion script `research/backtests/2026-09-04_spinoff-calendar.py` takes from
price data rather than from filings.

Caveat that governs everything downstream: **Form 10-12B is not a synonym for
"spin-off".** A large share of these registrants are shell / blank-check vehicles
distributing stock of a company with no operations. The output carries
`n_filings`, `entity_type` and SIC so the study can screen them out; it does not
try to judge them here.

Run: .venv/bin/python research/spinoffs.py
Writes data/spinoffs.csv and prints the count per year.
"""
import json, sys, time, threading, datetime as dt
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import urlencode

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / "research" / ".cache" / "sec"
OUT = ROOT / "data" / "spinoffs.csv"
UA = "ClaudeSpace research dspinjr@gmail.com"
START_YEAR = 2015
FTS = "https://efts.sec.gov/LATEST/search-index"
PAGE = 100
MAX_RPS = 6.0                      # SEC asks for <= 10/s; brief caps us at 8
WORKERS = 5

_lock = threading.Lock()
_next = [0.0]
SESSION = requests.Session()
SESSION.headers.update({"User-Agent": UA, "Accept-Encoding": "gzip, deflate"})


def get(url, params=None, tries=4):
    """Rate-limited GET with retry. Returns a requests.Response or None."""
    for i in range(tries):
        with _lock:                                  # global token bucket
            wait = _next[0] - time.monotonic()
            if wait > 0:
                time.sleep(wait)
            _next[0] = time.monotonic() + 1.0 / MAX_RPS
        try:
            r = SESSION.get(url, params=params, timeout=30)
            if r.status_code == 200:
                return r
            if r.status_code == 404:
                return None
            if r.status_code in (403, 429, 500, 502, 503):
                time.sleep(1.5 * (i + 1))
                continue
            return None
        except requests.RequestException:
            time.sleep(1.5 * (i + 1))
    return None


# ---------------------------------------------------------------- 1. FTS listing
def fts_window(start, end):
    """All 10-12B[/A] filings in [start, end]. Returns list of source dicts."""
    hits, frm = [], 0
    while True:
        r = get(FTS, {"q": "", "forms": "10-12B", "startdt": str(start),
                      "enddt": str(end), "from": frm})
        if r is None:
            print(f"  ! FTS failed {start}..{end}", file=sys.stderr)
            break
        try:
            h = r.json()["hits"]
        except (ValueError, KeyError):
            break
        total = h["total"]["value"]
        got = h["hits"]
        hits.extend(s["_source"] | {"_id": s["_id"]} for s in got)
        frm += PAGE
        if frm >= total or not got:
            break
    return hits, (hits and total or 0)


def quarters(start_year, today):
    for y in range(start_year, today.year + 1):
        for q, (a, b) in enumerate([("01-01", "03-31"), ("04-01", "06-30"),
                                    ("07-01", "09-30"), ("10-01", "12-31")]):
            s, e = dt.date.fromisoformat(f"{y}-{a}"), dt.date.fromisoformat(f"{y}-{b}")
            if s > today:
                return
            yield s, min(e, today)


def collect_filings(today):
    rows = []
    for s, e in quarters(START_YEAR, today):
        hits, total = fts_window(s, e)
        if len(hits) < total:                       # page size exhausted -> go monthly
            hits = []
            m = s
            while m <= e:
                nxt = (m.replace(day=28) + dt.timedelta(days=5)).replace(day=1)
                sub, _ = fts_window(m, min(nxt - dt.timedelta(days=1), e))
                hits.extend(sub)
                m = nxt
        for h in hits:
            ciks = h.get("ciks") or [""]
            rows.append(dict(
                cik=int(ciks[0]) if str(ciks[0]).strip().isdigit() else None,
                display_name=(h.get("display_names") or [""])[0],
                form=h.get("form", ""), root_form=(h.get("root_forms") or [""])[0],
                filing_date=h.get("file_date", ""), accession=h.get("adsh", ""),
                sic=(h.get("sics") or [""])[0],
                inc_state=(h.get("inc_states") or [""])[0],
                biz_state=(h.get("biz_states") or [""])[0]))
        print(f"  {s} .. {e}: {len(hits)} filings")
    df = pd.DataFrame(rows).dropna(subset=["cik"])
    df["cik"] = df["cik"].astype(int)
    return df.drop_duplicates(subset=["accession", "cik"])


# ---------------------------------------------------------------- 2. enrichment
def submissions(cik):
    p = CACHE / f"CIK{cik:010d}.json"
    if p.exists():
        try:
            return json.loads(p.read_text())
        except ValueError:
            pass
    r = get(f"https://data.sec.gov/submissions/CIK{cik:010d}.json")
    if r is None:
        return None
    try:
        j = r.json()
    except ValueError:
        return None
    CACHE.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(j))
    return j


def enrich(cik, reg_date):
    """Ticker/exchange + the filings that mark the actual listing."""
    out = dict(cik=cik, sec_name="", ticker="", exchange="", sic_desc="",
               entity_type="", cert_date="", form8a_date="", first_8k_date="",
               first_8k_items="", form25_date="", n_filings=0, last_filing="")
    j = submissions(cik)
    if not j:
        return out
    out["sec_name"] = j.get("name", "")
    tk = j.get("tickers") or []
    ex = j.get("exchanges") or []
    out["ticker"] = (tk[0] or "").strip().upper() if tk else ""
    out["exchange"] = (ex[0] or "").strip() if ex else ""
    out["sic_desc"] = j.get("sicDescription", "")
    out["entity_type"] = j.get("entityType", "")

    rec = j.get("filings", {}).get("recent", {})
    forms, dates = rec.get("form", []), rec.get("filingDate", [])
    items = rec.get("items", [""] * len(forms))
    # older filings spill into paged files; pull them so pre-2020 spin-offs resolve
    for f in j.get("filings", {}).get("files", []):
        r = get(f"https://data.sec.gov/submissions/{f['name']}")
        if r is None:
            continue
        try:
            e = r.json()
        except ValueError:
            continue
        forms = forms + e.get("form", [])
        dates = dates + e.get("filingDate", [])
        items = items + e.get("items", [""] * len(e.get("form", [])))
    if not forms:
        return out
    items = list(items) + [""] * (len(forms) - len(items))
    tbl = sorted(zip(dates, forms, items))
    out["n_filings"] = len(tbl)
    out["last_filing"] = tbl[-1][0]

    def first(pred):
        for d, f, it in tbl:
            if d >= reg_date and pred(f):
                return d, it
        return "", ""
    out["cert_date"], _ = first(lambda f: f == "CERT")
    out["form8a_date"], _ = first(lambda f: f.startswith("8-A12B"))
    out["first_8k_date"], out["first_8k_items"] = first(lambda f: f == "8-K")
    out["form25_date"], _ = first(lambda f: f.startswith("25"))
    return out


def ticker_map():
    p = CACHE / "company_tickers.json"
    if not p.exists():
        r = get("https://www.sec.gov/files/company_tickers.json")
        if r is None:
            return {}
        CACHE.mkdir(parents=True, exist_ok=True)
        p.write_text(r.text)
    try:
        j = json.loads(p.read_text())
    except ValueError:
        return {}
    return {int(v["cik_str"]): str(v["ticker"]).strip().upper() for v in j.values()}


# ---------------------------------------------------------------- 3. main
def main():
    t0 = time.time()
    today = dt.date.today()
    print(f"spinoffs: EDGAR full-text search, 10-12B[/A], {START_YEAR}-01-01 .. {today}")
    f = collect_filings(today)
    print(f"  {len(f)} filings across {f['cik'].nunique()} registrants")

    orig = f[f["form"] == "10-12B"]
    amend = f[f["form"] != "10-12B"]
    reg = (orig.groupby("cik")
               .agg(filing_date=("filing_date", "min"), display_name=("display_name", "first"),
                    accession=("accession", "first"), sic=("sic", "first"),
                    inc_state=("inc_state", "first"))
               .reset_index())
    # registrants seen only via an amendment (original predates the window)
    only_a = amend[~amend["cik"].isin(reg["cik"])]
    if len(only_a):
        extra = (only_a.groupby("cik")
                 .agg(filing_date=("filing_date", "min"), display_name=("display_name", "first"),
                      accession=("accession", "first"), sic=("sic", "first"),
                      inc_state=("inc_state", "first")).reset_index())
        extra["amend_only"] = True
        reg = pd.concat([reg.assign(amend_only=False), extra], ignore_index=True)
    else:
        reg["amend_only"] = False
    am = amend.groupby("cik").agg(n_amendments=("accession", "count"),
                                  last_amendment=("filing_date", "max"))
    reg = reg.merge(am, on="cik", how="left")
    reg["n_amendments"] = reg["n_amendments"].fillna(0).astype(int)
    reg["last_amendment"] = reg["last_amendment"].fillna("")
    print(f"  {len(reg)} registrants ({int(reg['amend_only'].sum())} seen only via an amendment)")

    print(f"  enriching {len(reg)} registrants from data.sec.gov/submissions ...")
    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        enr = pd.DataFrame(list(ex.map(lambda a: enrich(*a),
                                       zip(reg["cik"], reg["filing_date"]))))
    df = reg.merge(enr, on="cik", how="left")

    cmap = ticker_map()
    df["ticker_ct"] = df["cik"].map(cmap).fillna("")
    # ticker in the FTS display name: "Solventum Corp  (SOLV)  (CIK 0001964738)"
    df["ticker_fts"] = (df["display_name"].str.extract(r"\(([A-Z][A-Z0-9.\-]{0,5})\)\s+\(CIK")[0]
                        .fillna(""))
    df["ticker"] = (df["ticker"].replace("", pd.NA)
                    .fillna(df["ticker_ct"].replace("", pd.NA))
                    .fillna(df["ticker_fts"].replace("", pd.NA)).fillna(""))
    df["ticker_src"] = ["submissions" if a else "company_tickers" if b else "fts_name" if c else ""
                        for a, b, c in zip(enr["ticker"].fillna(""), df["ticker_ct"], df["ticker_fts"])]

    # estimated distribution / first-listing date, best marker available
    def est(r):
        for c in ("cert_date", "form8a_date", "first_8k_date"):
            if r[c]:
                return r[c], c.replace("_date", "")
        return "", ""
    df[["est_dist_date", "est_dist_src"]] = df.apply(lambda r: pd.Series(est(r)), axis=1)

    df["year"] = pd.to_datetime(df["filing_date"], errors="coerce").dt.year
    df["name"] = df["sec_name"].replace("", pd.NA).fillna(
        df["display_name"].str.replace(r"\s*\(CIK.*$", "", regex=True).str.strip())

    cols = ["cik", "name", "ticker", "ticker_src", "exchange", "filing_date", "year",
            "n_amendments", "last_amendment", "amend_only", "cert_date", "form8a_date",
            "first_8k_date", "first_8k_items", "form25_date", "est_dist_date", "est_dist_src",
            "sic", "sic_desc", "inc_state", "entity_type", "n_filings", "last_filing",
            "accession", "display_name"]
    df = df[cols].sort_values(["filing_date", "name"]).reset_index(drop=True)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT, index=False)

    print(f"\n10-12B registrants by year of first registration filing:")
    print(f"  {'year':>6} {'regs':>6} {'w/ticker':>9} {'w/dist':>7} {'still filing':>13}")
    for y, g in df.groupby("year"):
        alive = (pd.to_datetime(g["last_filing"], errors="coerce")
                 > pd.Timestamp(today) - pd.Timedelta(days=400)).sum()
        print(f"  {int(y):>6} {len(g):>6} {(g['ticker'] != '').sum():>9} "
              f"{(g['est_dist_date'] != '').sum():>7} {alive:>13}")
    print(f"  {'TOTAL':>6} {len(df):>6} {(df['ticker'] != '').sum():>9} "
          f"{(df['est_dist_date'] != '').sum():>7}")
    print(f"\nest_dist_src: {df['est_dist_src'].replace('', 'none').value_counts().to_dict()}")
    print(f"ticker_src:   {df['ticker_src'].replace('', 'none').value_counts().to_dict()}")
    print(f"wrote {OUT.relative_to(ROOT)} ({len(df)} rows) in {time.time()-t0:.0f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
