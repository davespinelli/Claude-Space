"""Step 1h: keep sponsor companies that were plausibly under $5B at some point since 2015, and
list their trials for the history download.

A company passes if its smallest month-end market value 2015-2026 (XBRL shares x Yahoo close,
ADS ratio for foreign issuers; see run_event_study.mcap_panel) was under $5B, or its smallest
reported public float since mid-2014 was under $5B, or neither figure exists (size is then
decided event by event). The exact per-event screen is applied later in run_event_study.py.
Writes data/sponsor_companies_priced.csv (adds min_mcap, size_pass) and data/trials_universe.csv.
"""
from pathlib import Path
import numpy as np, pandas as pd
import run_event_study as es

HERE = Path(__file__).resolve().parent


def main():
    comp = pd.read_csv(HERE / "data/sponsor_companies_priced.csv")
    T, R, close, after = es.load_prices()
    MV = es.mcap_panel(T, close, after, comp, es.share_series())
    mv = MV.loc["2015-01-01":].resample("ME").last()
    comp["min_mcap"] = comp.cik.map(mv.min())
    comp["max_mcap"] = comp.cik.map(mv.max())
    comp["size_pass"] = ((comp.min_mcap < 5e9) | (comp.min_float < 5e9)
                         | (comp.min_mcap.isna() & comp.min_float.isna()))
    comp.to_csv(HERE / "data/sponsor_companies_priced.csv", index=False)
    kept = set(comp.loc[comp.size_pass, "cik"])
    mp = pd.read_csv(HERE / "data/sponsor_map_kept.csv")
    names = set(mp.loc[mp.cik.isin(kept), "lead_sponsor"])
    tr = pd.read_csv(HERE / "data/trials_current.csv", dtype=str)
    tr = tr[tr.lead_sponsor.isin(names)]
    # download order: trials of companies with Yahoo prices first, then the rest; random
    # (seeded) within each group, so a partial download of either group is a random sample
    priced_names = set(mp.loc[mp.cik.isin(set(comp.loc[comp.size_pass & comp.ticker.notna(), "cik"])), "lead_sponsor"])
    tr = tr[["nct", "lead_sponsor", "phases", "last_update_post"]].sort_values("nct").sample(frac=1, random_state=4)
    tr["priced_sponsor"] = tr.lead_sponsor.isin(priced_names)
    tr = pd.concat([tr[tr.priced_sponsor], tr[~tr.priced_sponsor]])
    tr.to_csv(HERE / "data/trials_universe.csv", index=False)
    print(len(comp), "companies;", len(kept), "pass the size screen;", len(tr), "trials to download")
    print("no size data at all:", int((comp.min_mcap.isna() & comp.min_float.isna()).sum()))


if __name__ == "__main__":
    main()
