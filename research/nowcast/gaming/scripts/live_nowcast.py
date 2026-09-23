#!/usr/bin/env python3
"""Live nowcast for the quarter now under way (Q3 2026: July-September), using the state reports
published up to 2026-09-23.  Reads data/nowcast_live_raw.csv.gz (scripts/build_nowcast.py) and the
signal scaling of the historical test samples in results.json; writes data/live_nowcast.csv.

One row per qualifying company and sample ('prop' = property-level states only, the verdict
design; 'region' = adds Mississippi/Colorado/Nevada proxies).  A company qualifies when its covered
properties' GGR a year earlier is at least 60% of its gaming (or total) revenue then.

Columns
  months_covered      months of state data used (reports published by 2026-09-23)
  ggr_growth_yoy      same-store GGR growth over those months vs a year earlier
  nowcast_rev_growth  = ggr_growth_yoy (applied to revenue a year ago)
  flow_through        dollars of EBITDA per dollar of revenue change (own history shrunk 50% to industry)
  nowcast_ebitda_growth, reported_ebitda_growth_prev_q (Q2 2026 vs Q2 2025)
  signal_ebitda_accel = nowcast EBITDA growth minus last quarter's reported EBITDA growth (primary signal)
  signal_z            the signal in standard deviations of the historical test sample (after the same
                      winsorisation); positive = the state data point to an earnings acceleration
  next_report         Yahoo's expected earnings date
"""
import json
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


def main():
    raw = pd.read_csv(DATA / "nowcast_live_raw.csv.gz")
    R = json.loads((ROOT / "results.json").read_text())
    eps = pd.read_csv(DATA / "eps_surprise.csv.gz", parse_dates=["earn_date"])
    rows = []
    for _, r in raw[raw["qualifies"]].iterrows():
        w = R["samples"][r["sample"]].get("winsor", {}).get("sig_ebitda")
        z = np.nan
        if w and pd.notna(r["sig_ebitda"]):
            z = (min(max(r["sig_ebitda"], w["p5"]), w["p95"])) / w["sd"]
        nxt = eps[(eps["ticker"] == r["ticker"]) & (eps["earn_date"] > "2026-09-23")]["earn_date"].min() if isinstance(r["ticker"], str) else pd.NaT
        notes = []
        if r["company"] == "BALY":
            notes.append("coverage overstated: Rhode Island reports total net terminal income but Bally's books only its share, and its UK online business is not covered")
        if isinstance(r.get("states"), str) and "IA" in r["states"]:
            notes.append("Iowa excluded for Jul-Aug 2026 (AGR definition changed)")
        if r["ebitda_4"] < 0 or abs(r["ebitda_4"]) < 0.05 * r["rev_4"]:
            notes.append("year-ago EBITDA is negative or tiny (impairments sit in operating income), so EBITDA growth rates are not meaningful; read ggr_growth_yoy and nowcast_ebitda_musd instead")
        if isinstance(r.get("months_used"), str) and r["months_used"].count(",") == 0:
            notes.append("only one month of state data so far (Nevada/Colorado publish about 4 weeks after month-end)")
        if r["sample"] == "region":
            notes.append(f"region proxies (MS/CO/NV) carry {r['region_share']:.0%} of covered GGR")
        rows.append(dict(company=r["company"], ticker=r["ticker"], sample=r["sample"], quarter="2026Q3",
                         months_covered=r["months_used"], states=r["states"], properties=int(r["props"]),
                         coverage=round(r["coverage"], 3), ggr_growth_yoy=round(r["g"], 4),
                         rev_year_ago_musd=round(r["rev_4"] / 1e6, 1), nowcast_rev_musd=round(r["nc_rev"] / 1e6, 1),
                         flow_through=round(r["beta"], 3), flow_through_source=r["beta_src"],
                         ebitda_year_ago_musd=round(r["ebitda_4"] / 1e6, 1), nowcast_ebitda_musd=round(r["nc_ebitda"] / 1e6, 1),
                         nowcast_ebitda_growth=round(r["nc_ebitda_growth"], 4),
                         reported_ebitda_growth_prev_q=round(r["ebitda_growth_prev"], 4),
                         signal_ebitda_accel=round(r["sig_ebitda"], 4), signal_z=round(z, 2) if pd.notna(z) else np.nan,
                         reported_rev_growth_prev_q=round(r["rev_growth_prev"], 4),
                         signal_rev_accel=round(r["sig_rev"], 4),
                         last_state_report_used=str(pd.Timestamp(r["last_pub"]).date()) if pd.notna(r["last_pub"]) else "",
                         next_report=str(nxt.date()) if pd.notna(nxt) else "",
                         notes="; ".join(notes)))
    out = pd.DataFrame(rows).sort_values(["sample", "signal_z"], ascending=[True, False])
    out.to_csv(DATA / "live_nowcast.csv", index=False)
    return out


if __name__ == "__main__":
    print(main().to_string())
