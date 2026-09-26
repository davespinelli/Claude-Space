#!/usr/bin/env python3
"""INFO-5 step 1: extract every Form 4/5 gift line (TRANS_CODE 'G') from the SEC Form 3/4/5
quarterly data sets, with the filing, the reporting owners and the donor's holdings.

Sources (read-only):
  data/sec_cache/form345/{2012q1..2026q1}_form345.zip       shared cache (earlier projects)
  research/infoedge/info5_gifts/cache/form345/{2006q1..2011q4, 2026q2}_form345.zip  (fetch_form345.py)

Parsing follows research/backtests/2026-09-04_insider-cluster-smallcap.py (_read_tsv, dates in
DD-MON-YYYY, ISSUERCIK zero-padded), extended to code G and to the holdings columns.

Writes (cache/, gitignored):
  gift_lines.parquet    every non-derivative G line on Forms 4, 4/A, 5, 5/A
  owners.parquet        REPORTINGOWNER rows for those accessions
  acct_balances.parquet last reported post-transaction balance per ownership account per
                        accession (NONDERIV_TRANS + NONDERIV_HOLDING), for the holdings test
  os_prices.parquet     daily median open-market (P/S) Form 4 price per issuer, used only to
                        validate the Yahoo ticker mapping and as a price proxy for unpriced issuers
  symbols.parquet       ISSUERTRADINGSYMBOL counts per issuer CIK and year
"""
from __future__ import annotations

import io
import sys
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
DIRS = [REPO / "data" / "sec_cache" / "form345", HERE / "cache" / "form345"]
OUT = HERE / "cache"
FORMS = {"4", "4/A", "5", "5/A"}


def zips():
    seen = {}
    for d in DIRS:
        for p in sorted(d.glob("*_form345.zip")):
            seen.setdefault(p.name, p)
    return [seen[k] for k in sorted(seen)]


def read(zf, name, usecols=None):
    with zf.open(name) as fh:
        df = pd.read_csv(io.BytesIO(fh.read()), sep="\t", dtype=str, low_memory=False,
                         quoting=3, on_bad_lines="warn")
    if usecols:
        df = df[[c for c in usecols if c in df.columns]]
    return df


def dt(s):
    return pd.to_datetime(s, format="%d-%b-%Y", errors="coerce")


def num(s):
    return pd.to_numeric(s, errors="coerce")


def main():
    G, O, A, P, S = [], [], [], [], []
    for path in zips():
        tag = path.name[:6]
        with zipfile.ZipFile(path) as zf:
            sub = read(zf, "SUBMISSION.tsv", ["ACCESSION_NUMBER", "FILING_DATE", "PERIOD_OF_REPORT",
                                              "DOCUMENT_TYPE", "ISSUERCIK", "ISSUERNAME",
                                              "ISSUERTRADINGSYMBOL"])
            sub = sub[sub.DOCUMENT_TYPE.isin(FORMS)]
            tr = read(zf, "NONDERIV_TRANS.tsv")
            tr = tr[tr.ACCESSION_NUMBER.isin(set(sub.ACCESSION_NUMBER))]
            # --- open-market prices (Form 4 only), for ticker validation --------------------
            om = tr[tr.TRANS_CODE.isin(["P", "S"])][["ACCESSION_NUMBER", "TRANS_DATE",
                                                       "TRANS_PRICEPERSHARE"]].copy()
            om["price"] = num(om.TRANS_PRICEPERSHARE)
            om = om[om.price > 0].merge(sub[["ACCESSION_NUMBER", "ISSUERCIK"]], on="ACCESSION_NUMBER")
            om["date"] = dt(om.TRANS_DATE)
            P.append(om.groupby(["ISSUERCIK", "date"]).price.agg(["median", "size"]).reset_index())
            # --- symbols ------------------------------------------------------------------------
            ss = sub.assign(year=dt(sub.FILING_DATE).dt.year)
            S.append(ss.groupby(["ISSUERCIK", "year", "ISSUERTRADINGSYMBOL"]).size()
                     .rename("n").reset_index())
            # --- gift lines -------------------------------------------------------------------
            g = tr[tr.TRANS_CODE == "G"]
            accs = set(g.ACCESSION_NUMBER)
            keep = ["ACCESSION_NUMBER", "NONDERIV_TRANS_SK", "SECURITY_TITLE", "TRANS_DATE",
                    "DEEMED_EXECUTION_DATE", "TRANS_FORM_TYPE", "TRANS_CODE", "TRANS_TIMELINESS",
                    "TRANS_SHARES", "TRANS_PRICEPERSHARE", "TRANS_ACQUIRED_DISP_CD",
                    "SHRS_OWND_FOLWNG_TRANS", "DIRECT_INDIRECT_OWNERSHIP", "NATURE_OF_OWNERSHIP"]
            g = g[[c for c in keep if c in g.columns]].merge(sub, on="ACCESSION_NUMBER")
            g["quarter"] = tag
            G.append(g)
            own = read(zf, "REPORTINGOWNER.tsv", ["ACCESSION_NUMBER", "RPTOWNERCIK", "RPTOWNERNAME",
                                                   "RPTOWNER_RELATIONSHIP", "RPTOWNER_TITLE",
                                                   "RPTOWNER_TXT"])
            O.append(own[own.ACCESSION_NUMBER.isin(accs)])
            # --- account balances for G accessions (holdings after the filing's transactions) --
            t2 = tr[tr.ACCESSION_NUMBER.isin(accs)][["ACCESSION_NUMBER", "NONDERIV_TRANS_SK",
                                                     "SECURITY_TITLE", "TRANS_DATE",
                                                     "SHRS_OWND_FOLWNG_TRANS",
                                                     "DIRECT_INDIRECT_OWNERSHIP",
                                                     "NATURE_OF_OWNERSHIP"]].copy()
            t2["src"] = "T"
            h = read(zf, "NONDERIV_HOLDING.tsv")
            h = h[h.ACCESSION_NUMBER.isin(accs)]
            h = h[[c for c in ["ACCESSION_NUMBER", "NONDERIV_HOLDING_SK", "SECURITY_TITLE",
                               "SHRS_OWND_FOLWNG_TRANS", "DIRECT_INDIRECT_OWNERSHIP",
                               "NATURE_OF_OWNERSHIP"] if c in h.columns]].copy()
            h = h.rename(columns={"NONDERIV_HOLDING_SK": "NONDERIV_TRANS_SK"})
            h["src"] = "H"
            A.append(pd.concat([t2, h], ignore_index=True))
        print(f"{tag}: {len(sub):7d} F4/5 filings, {len(g):6d} G lines, {len(accs):6d} G filings",
              flush=True)

    g = pd.concat(G, ignore_index=True)
    for c in ["FILING_DATE", "PERIOD_OF_REPORT", "TRANS_DATE", "DEEMED_EXECUTION_DATE"]:
        g[c] = dt(g[c])
    for c in ["TRANS_SHARES", "TRANS_PRICEPERSHARE", "SHRS_OWND_FOLWNG_TRANS", "NONDERIV_TRANS_SK"]:
        g[c] = num(g[c])
    g.to_parquet(OUT / "gift_lines.parquet", index=False)

    pd.concat(O, ignore_index=True).drop_duplicates().to_parquet(OUT / "owners.parquet", index=False)

    a = pd.concat(A, ignore_index=True)
    a["TRANS_DATE"] = dt(a["TRANS_DATE"])
    a["SHRS_OWND_FOLWNG_TRANS"] = num(a["SHRS_OWND_FOLWNG_TRANS"])
    a["NONDERIV_TRANS_SK"] = num(a["NONDERIV_TRANS_SK"])
    a["acct"] = (a.SECURITY_TITLE.fillna("").str.upper().str.strip() + "|"
                 + a.DIRECT_INDIRECT_OWNERSHIP.fillna("") + "|"
                 + a.NATURE_OF_OWNERSHIP.fillna("").str.upper().str.strip())
    # last balance per account: transaction lines ordered by date then SK; holding lines last
    a["order"] = np.where(a.src == "H", 1, 0)
    a = a.sort_values(["ACCESSION_NUMBER", "acct", "order", "TRANS_DATE", "NONDERIV_TRANS_SK"])
    last = a.groupby(["ACCESSION_NUMBER", "acct"]).SHRS_OWND_FOLWNG_TRANS.last().reset_index()
    last.to_parquet(OUT / "acct_balances.parquet", index=False)

    p = pd.concat(P, ignore_index=True)
    # the same issuer-day can appear in two quarterly files (filed in a later quarter)
    p["w"] = p["median"] * p["size"]
    p = p.groupby(["ISSUERCIK", "date"])[["w", "size"]].sum().reset_index()
    p["price"] = p.w / p["size"]
    p = p.rename(columns={"size": "n"})[["ISSUERCIK", "date", "price", "n"]]
    p.to_parquet(OUT / "os_prices.parquet", index=False)
    s = pd.concat(S, ignore_index=True).groupby(["ISSUERCIK", "year", "ISSUERTRADINGSYMBOL"]).n.sum()
    s.reset_index().to_parquet(OUT / "symbols.parquet", index=False)
    print(f"total G lines {len(g):,}; filings {g.ACCESSION_NUMBER.nunique():,}", flush=True)


if __name__ == "__main__":
    sys.exit(main())
