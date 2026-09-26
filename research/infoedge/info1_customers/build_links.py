#!/usr/bin/env python3
"""
INFO-1 step 3: mentions -> links -> supplier/customer identities.

Reads data/mentions.csv.gz, data/docs_processed.csv.gz, data/tenk_index.csv.gz and writes
  data/links.csv          one row per (10-K filing, listed customer): pct, snippet, dates
  data/filings.csv        every original 10-K of every supplier CIK (for "until the next 10-K")
  data/suppliers.csv      supplier CIK -> Yahoo ticker (+ source), SIC, name
  data/links_log.json     counts at each filter

Rules (fixed before any return was computed):
  * one link per (filing, customer id); its share = the most frequent share among that
    filing's mentions about its latest fiscal year (mentions without a year count as
    current), ties broken by document order (extract.py never emits a combined share
    such as "A and B together accounted for 35%");
  * share >= 10% (the spec's threshold); share > 100 dropped as a parse error;
  * self-links (supplier CIK = customer CIK) dropped;
  * only original 10-K / 10-KT filings (no 10-K/A); main document or EX-13.
Supplier tickers: SEC company_tickers.json (current holder of the symbol), else the
oplev ticker maps (current or historical XBRL-prefix symbol) when the symbol is not
currently assigned to another CIK.
"""
from __future__ import annotations

import gzip
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
DATA = HERE / "data"
OPLEV = HERE.parents[1] / "oplev" / "cache"
from aliases import C as CUSTOMERS  # noqa: E402

BAD_SUFFIXES = {"W", "WS", "WT", "U", "UN", "R", "RT", "RTS", "P", "PR"}


def clean_ticker(t):
    t = (t or "").strip().upper()
    if not t or " " in t:
        return None
    t = t.replace(".", "-")
    if "-" in t:
        _, _, suf = t.partition("-")
        if suf in BAD_SUFFIXES or len(suf) > 2:
            return None
    return t if len(t) <= 7 else None


def company_tickers() -> pd.DataFrame:
    with gzip.open(OPLEV / "company_tickers.json.gz", "rt") as fh:
        js = json.loads(fh.read())
    rows = [dict(cik=int(r["cik_str"]), ticker=clean_ticker(str(r["ticker"])), title=r["title"], order=i)
            for i, r in enumerate(js.values())]
    ct = pd.DataFrame(rows).dropna(subset=["ticker"])
    ct["dash"] = ct.ticker.str.contains("-").astype(int)
    return ct.sort_values(["cik", "dash", "order"])


def main():
    log = {}
    m = pd.read_csv(DATA / "mentions.csv.gz")
    d = pd.read_csv(DATA / "docs_processed.csv.gz")
    log["docs_processed"] = int(len(d))
    log["docs_status"] = d.status.value_counts().to_dict()
    log["mentions_raw"] = int(len(m))
    m = m[(m.pct > 0) & (m.pct <= 100)].copy()
    log["mentions_pct_in_0_100"] = int(len(m))
    ct = company_tickers()
    tk2cik = ct.drop_duplicates("ticker").set_index("ticker").cik.to_dict()
    cid_tick = {c["id"]: c["tickers"][0][0] for c in CUSTOMERS if c["tickers"]}
    m["cust_ticker"] = m.cid.map(cid_tick)
    m["cust_cik"] = m.cust_ticker.map(tk2cik)
    self_ = m.cust_cik.notna() & (m.cust_cik == m.cik)
    log["mentions_self_dropped"] = int(self_.sum())
    m = m[~self_]
    # one link per filing x customer id: among the mentions about the latest fiscal year in the
    # filing (sentence's latest year, capped at the period year + 1; mentions without a year
    # count as current), the most frequent share; ties -> first in document order
    py = pd.to_datetime(m.period_ending, errors="coerce").dt.year.fillna(pd.to_datetime(m.file_date).dt.year)
    def maxyear(ys, cap):
        v = [int(y) for y in str(ys).split(";") if y.isdigit() and int(y) <= cap]
        return max(v) if v else np.nan
    m["max_year"] = [maxyear(y, c + 1) for y, c in zip(m.years.fillna(""), py)]
    m["ord"] = np.where(m.offset < 0, 10**12, m.offset)
    picks = []
    for (adsh, cid), g in m.groupby(["adsh", "cid"], sort=False):
        top = g.max_year.max()
        cur = g[(g.max_year == top) | g.max_year.isna()] if np.isfinite(top) else g
        vc = cur.pct.round(1).value_counts()
        best = vc[vc == vc.max()].index
        row = cur[cur.pct.round(1).isin(best)].sort_values("ord").iloc[0].copy()
        row["max_year"] = top
        row["n_mentions"] = len(g)
        row["max_pct_any"] = g.pct.max()
        row["any_combined"] = bool(g.combined.max())
        picks.append(row)
    L = pd.DataFrame(picks).reset_index(drop=True)
    log["filing_customer_pairs_any_share"] = int(len(L))
    # a filing whose latest mention of the customer is about an earlier fiscal year than its own
    # ("For 2020, Google accounted for 10%" in the FY2021 10-K) is not a current link: the customer
    # has usually dropped below 10%. Fiscal years ending January-March may carry the prior
    # calendar year's name ("fiscal 2015" ending January 2016), so one year of slack there.
    # (Tightened from "two or more years" after the first 50-link precision check, before any return.)
    pe = pd.to_datetime(L.period_ending, errors="coerce")
    pe = pe.fillna(pd.to_datetime(L.file_date) - pd.Timedelta(days=90))
    need = pe.dt.year - (pe.dt.month <= 3).astype(int)
    stale = L.max_year.notna() & (L.max_year < need)
    log["links_dropped_stale_year"] = int(stale.sum())
    L = L[~stale]
    L = L[L.pct >= 10].copy()
    log["links_share_ge_10"] = int(len(L))
    L["file_date"] = pd.to_datetime(L.file_date)
    L = L.rename(columns={"cik": "supplier_cik"})
    # customer ticker windows
    win = {c["id"]: c["tickers"] for c in CUSTOMERS}
    L["cust_windows"] = L.cid.map(lambda c: json.dumps(win.get(c, [])))
    L = L[["supplier_cik", "display_name", "sic", "adsh", "file_name", "file_date", "period_ending", "cid",
           "cust_ticker", "cust_windows", "alias", "pct", "pcts", "role", "combined", "any_combined",
           "n_mentions", "max_pct_any", "years", "snippet"]].sort_values(["file_date", "supplier_cik", "cid"])
    L.to_csv(DATA / "links.csv", index=False)
    # recall of the template search, measured on the random discovery sample
    dd = d[d.in_discovery].set_index(["adsh", "file_name"])
    Lk = L.set_index(["adsh", "file_name"])
    disc = Lk[Lk.index.isin(dd.index)]
    found = dd.loc[disc.index.unique(), "in_alias_search"]
    log["recall_check"] = {
        "discovery_docs": int(len(dd)),
        "discovery_docs_with_link": int(disc.index.nunique()),
        "of_which_found_by_template_search": int(found.sum()),
        "discovery_links": int(len(disc)),
        "discovery_links_found_by_template_search": int(dd.loc[disc.index, "in_alias_search"].sum()),
    }
    log["links_filings"] = int(L.adsh.nunique())
    log["links_suppliers"] = int(L.supplier_cik.nunique())
    log["links_by_customer_top30"] = L.cid.value_counts().head(30).to_dict()
    log["links_by_file_year"] = L.file_date.dt.year.value_counts().sort_index().to_dict()

    # every original 10-K of the supplier CIKs
    ti = pd.read_csv(DATA / "tenk_index.csv.gz")
    ti = ti[ti.form.isin(["10-K", "10-K405", "10-KT"]) & ti.cik.isin(L.supplier_cik.unique())].copy()
    ti["date"] = pd.to_datetime(ti.date)
    ti = ti.sort_values(["cik", "date"]).drop_duplicates(["cik", "adsh"])
    ti.to_csv(DATA / "filings.csv", index=False)
    miss = set(L.adsh) - set(ti.adsh)
    log["link_filings_not_in_full_index"] = len(miss)

    # supplier tickers
    sup = (L.sort_values("file_date").groupby("supplier_cik")
           .agg(name=("display_name", "last"), sic=("sic", "last"), first_link=("file_date", "min"),
                last_link=("file_date", "max")).reset_index())
    cur = ct.drop_duplicates("cik").set_index("cik").ticker
    sup["ticker"] = sup.supplier_cik.map(cur)
    sup["ticker_src"] = np.where(sup.ticker.notna(), "company_tickers", None)
    holder = ct.drop_duplicates("ticker").set_index("ticker").cik.to_dict()
    op_t = pd.read_parquet(OPLEV / "tickers.parquet")
    op_h = pd.read_parquet(OPLEV / "hist_tickers.parquet").dropna(subset=["hist_ticker"])
    for i, r in sup[sup.ticker.isna()].iterrows():
        c = int(r.supplier_cik)
        cand, src = None, None
        if c in op_t.index:
            cand, src = op_t.at[c, "ticker"], "oplev_submissions"
        elif c in op_h.index:
            cand, src = op_h.at[c, "hist_ticker"], "oplev_hist_xbrl_prefix"
        if cand and holder.get(cand, c) == c:
            sup.at[i, "ticker"] = cand
            sup.at[i, "ticker_src"] = src
    sup.to_csv(DATA / "suppliers.csv", index=False)
    log["suppliers"] = int(len(sup))
    log["suppliers_ticker_src"] = sup.ticker_src.fillna("none").value_counts().to_dict()
    (DATA / "links_log.json").write_text(json.dumps(log, indent=1, default=str))
    print(json.dumps(log, indent=1, default=str))


if __name__ == "__main__":
    main()
