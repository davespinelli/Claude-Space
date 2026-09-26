#!/usr/bin/env python3
"""Stage 1: candidate SEC companies and their names (aliases).

Candidates (fixed before any award data was looked at):
  * currently listed: every CIK in SEC company_tickers_exchange.json on Nasdaq,
    NYSE or CBOE (OTC excluded: not "US-listed");
  * no longer listed: every operating company in research/oplev's XBRL universe
    (all filers 2009-2025 with revenue) that has no current ticker but has a
    historical trading symbol (oplev hist_tickers: XBRL file prefix).
  * SIC 6000-6999 (finance, insurance, real estate, SPACs/blank checks) excluded.

Names: current SEC name + every former name in the SEC submissions file.
Submissions JSON comes from caches already on disk (oplev, deepvalue) or is
fetched (<= 2 requests a second).

Writes data/universe.csv (one row per CIK) and data/aliases.csv (cik, name, core).
"""
from __future__ import annotations

import gzip
import json
from concurrent.futures import ThreadPoolExecutor

import pandas as pd

from common import CACHE, DATA, ROOT, core, log, sec_json

SUBS_DIRS = [ROOT / "research/oplev/cache/submissions", ROOT / "research/deepvalue/data/submissions"]
MY_SUBS = CACHE / "sec" / "submissions"


def load_subs(cik: int):
    name = f"CIK{cik:010d}.json"
    for d in SUBS_DIRS:
        for p in (d / (name + ".gz"), d / name):
            if p.exists():
                try:
                    if p.suffix == ".gz":
                        with gzip.open(p, "rt") as fh:
                            return json.loads(fh.read())
                    return json.loads(p.read_text())
                except Exception:  # noqa: BLE001
                    pass
    js = sec_json(f"https://data.sec.gov/submissions/{name}", MY_SUBS / (name + ".gz"))
    return js if isinstance(js, dict) else None


def main():
    ex = sec_json("https://www.sec.gov/files/company_tickers_exchange.json",
                  CACHE / "sec" / "company_tickers_exchange.json.gz")
    cte = pd.DataFrame(ex["data"], columns=ex["fields"])
    listed = cte[cte.exchange.isin(["Nasdaq", "NYSE", "CBOE"])].copy()
    # one primary ticker per CIK: first listed, prefer symbols without '-'
    listed["dash"] = listed.ticker.str.contains(r"[-.]").astype(int)
    listed["order"] = range(len(listed))
    prim = listed.sort_values(["cik", "dash", "order"]).drop_duplicates("cik")
    cur = prim.set_index("cik")[["ticker", "exchange", "name"]]
    cur["listing"] = "current"

    osubs = pd.read_parquet(ROOT / "research/oplev/cache/subs.parquet")
    hist = pd.read_parquet(ROOT / "research/oplev/cache/hist_tickers.parquet").dropna(subset=["hist_ticker"])
    old = osubs[~osubs.index.isin(cte.cik) & osubs.index.isin(hist.index)]
    oldf = pd.DataFrame({"ticker": hist.loc[old.index, "hist_ticker"], "exchange": None,
                         "name": old.name, "listing": "former"})
    U = pd.concat([cur, oldf])
    U.index.name = "cik"
    log(f"candidates: {len(cur)} currently listed CIKs, {len(oldf)} formerly listed")

    ciks = [int(c) for c in U.index]
    with ThreadPoolExecutor(max_workers=3) as exr:
        subs = dict(zip(ciks, exr.map(load_subs, ciks)))
    rows, alias = [], []
    for cik in ciks:
        js = subs.get(cik) or {}
        sic = str(js.get("sic") or "").strip()
        rows.append(dict(cik=cik, sic=int(sic) if sic.isdigit() else None,
                         sic_desc=js.get("sicDescription") or "",
                         entity_type=js.get("entityType") or "",
                         state_inc=js.get("stateOfIncorporation") or "",
                         sub_name=js.get("name") or ""))
        names = [U.at[cik, "name"], js.get("name") or ""]
        for fn in js.get("formerNames") or []:
            names.append(fn.get("name") or "")
            alias.append(dict(cik=cik, name=fn.get("name") or "", src="former",
                              name_from=fn.get("from"), name_to=fn.get("to")))
        for n in names[:2]:
            alias.append(dict(cik=cik, name=n, src="current", name_from=None, name_to=None))
    S = pd.DataFrame(rows).set_index("cik")
    U = U.join(S)
    U["financial"] = U.sic.between(6000, 6999)
    U["no_sic"] = U.sic.isna()
    A = pd.DataFrame(alias)
    A = A[A.name.str.strip() != ""]
    A["core"] = A.name.map(core)
    A = A[A.core != ""].drop_duplicates(["cik", "core", "src"])
    keep = U[~U.financial].index
    U.to_csv(DATA / "universe_all.csv")
    U.loc[keep].to_csv(DATA / "universe.csv")
    A[A.cik.isin(keep)].to_csv(DATA / "aliases.csv", index=False)
    log(f"universe: {len(U)} CIKs, financial excluded {int(U.financial.sum())}, "
        f"no SIC {int(U.no_sic.sum())}, kept {len(keep)}; aliases {int(A.cik.isin(keep).sum())}")


if __name__ == "__main__":
    main()
