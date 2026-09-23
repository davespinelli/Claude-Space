#!/usr/bin/env python3
"""Write RESULTS.md from results.json, the nowcast panel, the test samples and data/live_nowcast.csv.
Run after run_tests.py and live_nowcast.py."""
import json
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
NAMES = {"PENN": "Penn", "BYD": "Boyd", "ERI_CZR": "Eldorado/Caesars (CZR)", "CHDN": "Churchill Downs",
         "CNTY": "Century", "FLL": "Full House", "BALY": "Bally's", "MGM": "MGM", "MCRI": "Monarch",
         "RRR": "Red Rock", "WYNN": "Wynn", "NYNY": "Empire Resorts", "TPCA": "Tropicana Ent.",
         "DDE": "Dover Downs", "ISLE": "Isle of Capri", "PNK_OLD": "Pinnacle (to 2016)", "PNK": "Pinnacle (2016-18)",
         "GDEN": "Golden/Lakes", "CZR_OLD": "Caesars Ent. Corp (old)", "MNTG": "MTR Gaming", "AFFI": "Affinity"}


def f2(x, d=2, sign=True):
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return "n/a"
    return f"{x:+.{d}f}" if sign else f"{x:.{d}f}"


def pct(x, d=1):
    return "n/a" if x is None or (isinstance(x, float) and np.isnan(x)) else f"{100 * x:.{d}f}%"


def reg_line(r):
    if "slope" not in r:
        return f"n = {r.get('n')} (too few)"
    return f"{f2(r['slope'])} points per SD, t = {r['t']:.2f}, n = {r['n']}"


def main():
    R = json.loads((ROOT / "results.json").read_text())
    P, G = R["samples"]["prop"], R["samples"]["region"]
    pr, gr = P["primary"], G["primary"]
    live = pd.read_csv(DATA / "live_nowcast.csv")
    Tp = pd.read_csv(DATA / "test_sample_prop.csv.gz")
    Tg = pd.read_csv(DATA / "test_sample_region.csv.gz")
    panel = pd.read_csv(DATA / "nowcast_panel.csv.gz", parse_dates=["qend", "ann_date"])
    Q = panel[panel["qualifies"]]
    L = []
    w = L.append
    w("# Do monthly state casino data get ahead of casino earnings? Pre-registered pilot\n")
    w(f"*Generated {R['generated']} by `research/nowcast/gaming/scripts/write_results.py` from `results.json`. "
      "Design in `PREREG.md` (locked), with the Deviations section written before any return was computed. "
      "State revenue data 2012-01 to 2026-08, earnings announcements April 2013 to August 2026.*\n")
    w("## The short answer\n")
    w(f"**No.** Monthly state casino revenue tells you a casino company's same-store revenue before it reports, and pushing it "
      f"through the company's operating leverage gives a better EBITDA forecast than \"same as last quarter\". But the stock "
      f"does not move with it. Companies whose state data pointed to an earnings acceleration did only {f2(pr['slope'])} "
      f"percentage points better around the release per standard deviation of the signal (t = {pr['t']:.2f}, bar 2.0). "
      f"The slope was positive in both halves ({f2(pr['halves'][0]['slope'])} and {f2(pr['halves'][1]['slope'])}), "
      "but too small and noisy to count. Nothing happened before the release either, and the signal "
      "did not predict whether EPS beat consensus. The likeliest reading: analysts and investors already track these public "
      "state numbers, so they are in the price and the consensus by report day.\n")
    w("| Test | Property-level states (verdict) | With Mississippi / Colorado / Nevada proxies (no verdict) |")
    w("|---|---|---|")
    w(f"| **Primary: announcement return on EBITDA-acceleration nowcast** | **No.** {reg_line(pr)}; halves {f2(pr['halves'][0]['slope'])} / {f2(pr['halves'][1]['slope'])} | {reg_line(gr)}; halves {f2(gr['halves'][0]['slope'])} / {f2(gr['halves'][1]['slope'])} |")
    w(f"| Pre-announcement drift (last state report to release) | {reg_line(P['drift'])} | {reg_line(G['drift'])} |")
    w(f"| Revenue-only nowcast (no operating-leverage step) | {reg_line(P['revenue_only'])} | {reg_line(G['revenue_only'])} |")
    a, b = P["analyst"], G["analyst"]
    w(f"| Sign of EPS surprise vs consensus (Yahoo) | hit rate {pct(a['hit_rate'])} of {a['n']}, p = {a['binom_p']:.2f} | {pct(b['hit_rate'])} of {b['n']}, p = {b['binom_p']:.2f} |")
    w(f"| Small caps (< $2B at announcement) | {reg_line(P['small_caps'])} | {reg_line(G['small_caps'])} |")
    w(f"| Larger companies | {reg_line(P['larger'])} | {reg_line(G['larger'])} |")
    w("")
    w("Slopes are the abnormal return (stock minus SPY, close before the 8-K filing day to close after it) in percentage "
      "points for a one-standard-deviation higher signal, after winsorising the signal at the 5th/95th percentiles; "
      "t-statistics are clustered by calendar quarter. \"Halves\" split the sample at its median announcement date.\n")
    w(f"In one line: **Primary No** (slope {f2(pr['slope'])} points per SD, clustered t = {pr['t']:.2f}, positive in both halves: "
      f"{f2(pr['halves'][0]['slope'])} in {pr['halves'][0]['from'][:4]}-{pr['halves'][0]['to'][:4]}, {f2(pr['halves'][1]['slope'])} in {pr['halves'][1]['from'][:4]}-{pr['halves'][1]['to'][:4]}).\n")

    # ------------------------------------------------------------------ sample sizes
    w("## Sample sizes\n")
    cnt = lambda T: ", ".join(f"{NAMES.get(c, c)} {n}" for c, n in T["company"].value_counts().items())
    w(f"- **Return tests, property sample (verdict):** {P['n']} company-quarters, {len(P['companies'])} companies ({cnt(Tp)}), "
      f"{P['quarters']} calendar quarters, announcements {pr['first_ann']} to {pr['last_ann']}; state data from {len(P['states'])} states "
      f"({', '.join(P['states'])}).")
    w(f"- **Return tests, region sample:** {G['n']} company-quarters, {len(G['companies'])} companies ({cnt(Tg)}), {len(G['states'])} states.")
    ap, ag = P["accuracy_all_qualifying"]["all"], G["accuracy_all_qualifying"]["all"]
    w(f"- **Accuracy checks** use every qualifying company-quarter whether or not the stock has prices: {ap['n']} company-quarters of "
      f"{ap['companies']} companies (property sample), {ag['n']} of {ag['companies']} (region sample).")
    w("- **State data:** 21 states, monthly, mostly 2012-01 to 2026-07/08 (table at the end). Every state's property rows "
      "add up to the regulator's own statewide total (largest gap 0.02%, except Kansas 0.8% against a later year's comparison column).")
    w("- **Ownership timeline:** 523 ownership spells, 294 casinos, 34 companies, 511 of them checked against 10-K property lists and 8-K closing notices.")
    w("- A company-quarter qualifies when its covered casinos' GGR a year earlier was at least 60% of its reported gaming revenue "
      "then (the casino line of the revenue breakdown; total revenue only where no gaming line exists), and the state reports for "
      "at least two-thirds of that were public before the release.\n")

    # ------------------------------------------------------------------ accuracy
    w("## How accurate the nowcasts were (the machine works)\n")
    A, NB = P["accuracy_all_qualifying"], P["accuracy_all_qualifying"]["naive_benchmark"]
    w("Property sample, all qualifying company-quarters. \"No portfolio change\" drops quarters where the company bought or sold a "
      "casino in the past year (reported growth then includes the deal; the nowcast is same-store by design). "
      "Pearson correlations are dominated by the 2020-21 closures and reopenings, so rank correlations and median errors are the "
      "better guide. Growth is in fractions (0.05 = 5%).\n")
    w("| Quarters | n | Revenue: correlation / rank corr. / median miss | Naive (last quarter's growth) | EBITDA: correlation / rank corr. / median miss | Naive |")
    w("|---|---|---|---|---|---|")
    for lab, k in [("All", "all"), ("No portfolio change", "no_portfolio_change"), ("No portfolio change, ex-COVID", "no_portfolio_change_ex_covid")]:
        r, e = A[k]["rev"], A[k]["ebitda"]
        nr, ne = NB[k]["rev"], NB[k]["ebitda"]
        w(f"| {lab} | {r['n']} | {r['pearson']:.2f} / {r['spearman']:.2f} / {r['median_ae']:.3f} | {nr['pearson']:.2f} / {nr['spearman']:.2f} / {nr['median_ae']:.3f} | "
          f"{e['pearson']:.2f} / {e['spearman']:.2f} / {e['median_ae']:.2f} | {ne['pearson']:.2f} / {ne['spearman']:.2f} / {ne['median_ae']:.2f} |")
    r, e = A["all"]["rev"], A["all"]["ebitda"]
    w(f"\nPre-registered figures (all qualifying quarters): revenue-growth correlation {r['pearson']:.2f}, mean absolute error {r['mae']:.3f}; "
      f"EBITDA-growth correlation {e['pearson']:.2f}, mean absolute error {e['mae']:.2f}. Same-store, the state data nail revenue "
      f"(median miss {A['no_portfolio_change']['rev']['median_ae'] * 100:.1f} points of growth vs {NB['no_portfolio_change']['rev']['median_ae'] * 100:.1f} for the naive forecast). "
      f"EBITDA is much harder (median miss {A['no_portfolio_change']['ebitda']['median_ae'] * 100:.0f} points) because operating income carries "
      "impairments, pre-opening costs, online losses and rent changes that no revenue data can see, but it still beats \"same as last quarter\".\n")
    w("By company (property sample, all qualifying quarters; rank correlations):\n")
    ntest = Tp["company"].value_counts()
    w("| Company | Quarters | Period | Median coverage | Revenue rank corr. | Revenue median miss | EBITDA rank corr. | In return tests |")
    w("|---|---|---|---|---|---|---|---|")
    for c, v in sorted(A["by_company"].items(), key=lambda kv: -kv[1]["n"]):
        rv, eb = v["rev"], v["ebitda"]
        w(f"| {NAMES.get(c, c)} | {v['n']} | {v['first'][:7]} to {v['last'][:7]} | {v['coverage_median']:.2f} | "
          f"{f2(rv.get('spearman', np.nan), 2, False)} | {f2(rv.get('median_ae', np.nan), 3, False)} | {f2(eb.get('spearman', np.nan), 2, False)} | {int(ntest.get(c, 0))} |")
    w("")

    # ------------------------------------------------------------------ primary
    w("## Primary test\n")
    w(f"Signal: nowcast EBITDA growth for the quarter (state GGR growth x revenue a year ago x the company's flow-through rate, "
      f"added to EBITDA a year ago) minus the company's reported EBITDA growth the quarter before. Flow-through (dollars of EBITDA "
      f"per dollar of revenue change, estimated only on quarters reported before each release, shrunk halfway to the industry "
      f"median) had a median of about 0.4 in the sample.\n")
    w(f"- Result: slope {f2(pr['slope'])} points per SD (standard error {pr['se']:.2f}), clustered t = {pr['t']:.2f}, "
      f"{pr['n']} company-quarters, {pr['clusters']} calendar-quarter clusters, R-squared {pr['r2']:.3f}.")
    for i, h in enumerate(pr["halves"]):
        w(f"- {'First' if i == 0 else 'Second'} half ({h['from']} to {h['to']}): {f2(h['slope'])} points (t = {h['t']:.2f}, n = {h['n']}).")
    s3, ec = P["all3_months_spec_literal"], P["ex_covid"]
    w(f"- Using all three months of state data even when a report came out after the release (the literal PREREG signal): {f2(s3['slope'])}, t = {s3['t']:.2f}.")
    w(f"- Excluding fiscal quarters from 2020 Q1 to 2021 Q2 (closures): {f2(ec['slope'])}, t = {ec['t']:.2f}, n = {ec['n']}.")
    w(f"- **Verdict: {R['verdict']}.** Positive in both halves, but t = {pr['t']:.2f} is well short of 2.0.\n")

    # ------------------------------------------------------------------ secondary
    w("## Secondary tests (no verdict)\n")
    d = P["drift"]
    w(f"**Does the market price the state data before the report?** Return from the day the last state report used was published "
      f"to the day before the release (median {int(np.nanmedian(Tp['drift_days']))} calendar days): {reg_line(d)}; halves "
      f"{f2(d['halves'][0]['slope'])} / {f2(d['halves'][1]['slope'])}. Region sample: {reg_line(G['drift'])}. No drift in the direction of the "
      "nowcast. Most state reports are out one to four weeks before the release; the market does not trend toward the nowcast in that "
      "window and does not react to it on the day, which together say the information is already in prices (or is not news).\n")
    ro = P["revenue_only"]
    w(f"**Revenue-only version:** {reg_line(ro)} (region {reg_line(G['revenue_only'])}). The operating-leverage step turns a "
      f"slightly negative revenue signal into a slightly positive EBITDA one; neither is distinguishable from zero.\n")
    w(f"**Versus analyst estimates:** Alpha Vantage was not available locally, but Yahoo's earnings calendar (via yfinance) gives a free "
      f"consensus-EPS history. The nowcast signal's sign matched the sign of the EPS surprise in {a['hits']} of {a['n']} releases "
      f"({pct(a['hit_rate'])}, binomial p = {a['binom_p']:.2f}); small caps {pct(a['small']['hit_rate'])} of {a['small']['n']}, larger "
      f"{pct(a['larger']['hit_rate'])} of {a['larger']['n']}. Region sample {pct(b['hit_rate'])} of {b['n']} (p = {b['binom_p']:.2f}). "
      "Yahoo's consensus is today's record, not a point-in-time snapshot, and uses adjusted EPS.\n")
    w("**Small caps versus larger** (market cap at the announcement below $2B; signals standardised on the whole sample):\n")
    w("| | Property sample | Region sample |")
    w("|---|---|---|")
    for lab, k in [("Small caps, announcement", "small_caps"), ("Larger, announcement", "larger"),
                   ("Small caps, drift", "small_caps_drift"), ("Larger, drift", "larger_drift"),
                   ("Small caps, revenue-only", "small_caps_revenue_only"), ("Larger, revenue-only", "larger_revenue_only")]:
        w(f"| {lab} | {reg_line(P[k])} | {reg_line(G[k])} |")
    sm = Tp[Tp["small"]]["company"].value_counts()
    w(f"\nThe property-sample small caps are {', '.join(f'{NAMES.get(c, c)} {n}' for c, n in sm.items())} (Penn, Boyd and Eldorado were "
      "under $2B in parts of 2013-2016). The thinner analyst coverage of small caps does not show up as a larger reaction to the "
      "state data; if anything the slope is smaller.\n")

    # ------------------------------------------------------------------ region
    w("## The region sample (Mississippi, Colorado, Nevada)\n")
    w(f"These states publish revenue only by region, town or reporting area, so each casino's revenue is imputed from its share of "
      f"the area's slot machines and tables (10-K property tables for Nevada and Colorado, the Gaming Commission's per-casino counts "
      f"for Mississippi). That brings in Monarch, Red Rock, the Las Vegas side of Boyd and Caesars, and most of Century and Full House. "
      f"Result: {reg_line(gr)}, positive in both halves ({f2(gr['halves'][0]['slope'])}, t = {gr['halves'][0]['t']:.2f}; "
      f"{f2(gr['halves'][1]['slope'])}, t = {gr['halves'][1]['t']:.2f}). Closer to the bar than the verdict sample but still short, "
      "and it has no verdict under the pre-registration.\n")

    # ------------------------------------------------------------------ exclusions
    w("## Names and dates excluded, and why\n")
    un = Q[~Q["priced"]].groupby(["company", "sample"]).size().unstack(1).fillna(0).astype(int)
    w("**No daily prices on Yahoo** (kept in the accuracy checks, left out of the return tests). Qualifying company-quarters lost, property / region sample:\n")
    reasons = {"NYNY": "taken private Nov 2019 (Yahoo's NYNY today is an unrelated company)", "TPCA": "acquired by Eldorado Oct 2018",
               "BALY": "Yahoo's history starts 2024-12-06; Twin River/Bally's 2019-2024 missing", "DDE": "merged into Twin River Mar 2019",
               "ISLE": "acquired by Eldorado May 2017", "PNK_OLD": "Pinnacle before the 2016 GLPI deal", "PNK": "acquired by Penn Oct 2018",
               "GDEN": "taken private April 2026; Yahoo dropped the symbol", "CZR_OLD": "Yahoo's CZR history is Eldorado's",
               "MNTG": "merged into Eldorado Sept 2014", "AFFI": "never exchange-listed"}
    for c, row in un.iterrows():
        w(f"- {NAMES.get(c, c)}: {row.get('prop', 0)} / {row.get('region', 0)} ({reasons.get(c, '')})")
    w("- Caesars Acquisition Co, Nevada Gold, Lakes (LACO) and ERI/TRWH under their old tickers: no Yahoo history. Stooq blocks "
      "scripted access with a browser check, which was not bypassed.\n")
    w("**Never qualified in the property sample** (coverage below 60%): Monarch and Red Rock (all Nevada/Colorado), Wynn (Macau, Las Vegas), "
      "MGM in all but 3 quarters (Strip, Macau); Caesars after 2020 mostly (Strip). Churchill Downs does qualify, because the "
      "pre-registered rule measures coverage against casino revenue, although most of its revenue is racing, historical racing machines and online.\n")
    w("**States not collected:** Kentucky (Churchill's historical racing machines), New Mexico (Penn's Zia Park), Virginia (Caesars Virginia, 2024 on), "
      "Nebraska, Washington card rooms, tribal casinos (no public property data). Their properties count as uncovered.\n")
    w("**Data gaps:** West Virginia racetracks before July 2018 (no archive found); New York after September 2025 (the regulator blocks "
      "scripted access; Internet Archive copies end there); Iowa from July 2026 (AGR redefined, about -13% mechanically; excluded from "
      "year-over-year comparisons); Maine November-December 2017; Illinois April-June 2020 set to zero (closed, no reports); Nevada 2020-04/05 "
      "and 2025-06/07 rebuilt from later reports' three-month columns; Mississippi 2012-2015 Central/Northern split imputed.\n")
    w("**Point-in-time drops:** company-quarters whose state reports covering two-thirds of the year-ago GGR were not public before the "
      "release were dropped: 7 in the property sample (1 priced), 33 in the region sample (26 priced; Nevada publishes about four weeks after month-end).\n")

    # ------------------------------------------------------------------ caveats
    w("## Caveats\n")
    w(f"- **Small cross-section.** Only 8 companies (property sample) have usable prices; Penn, Boyd and Eldorado/Caesars supply "
      f"{int(Tp['company'].isin(['PENN', 'BYD', 'ERI_CZR']).sum())} of {len(Tp)} observations. The companies bought out in 2017-2019 "
      "(Isle, Pinnacle, Tropicana, Dover Downs, Empire) are exactly the ones with the cleanest single-state coverage, and they have no prices.")
    w("- **EBITDA as defined here is noisy.** Operating income + D&A carries impairments and one-offs, and growth on small or negative bases "
      "explodes; the signal subtracts last quarter's reported EBITDA growth, which is dominated by those swings (winsorisation caps it "
      "but the signal is mostly baseline noise). A cleaner adjusted-EBITDA series would need the press releases.")
    w("- **The coverage rule is literal.** Coverage is against casino revenue, so Churchill Downs qualifies although state data cover a minority "
      "of its business; Rhode Island and New York report total net terminal income, of which the operator books only its share, so "
      "Bally's and Empire Resorts look better covered than they are.")
    w("- **Publication dates are partly assumed.** Where a report's date could not be found (Illinois from 2020, most of Ohio, Iowa, "
      f"Colorado, Delaware, Florida), month-end + 30 days was used; {Tp['any_pub_assumed'].mean():.0%} of property-sample test quarters use at least one assumed date. "
      "Some state archives hold revised rather than first-published figures (Iowa, Florida, Missouri).")
    w("- **Region imputation** assumes each casino earns its machine share of the area's win; big Strip resorts and local casinos differ.")
    w("- **Fixed after the first run:** Red Rock has no cover-page share count in the SEC data, so the first run left it out of the size split; "
      "the reported numbers use its Class A weighted share count (listed shares only). Only the region-sample size split changed "
      "(first run: small caps +0.18, t = 0.24, n = 163; larger +0.89, t = 1.71, n = 195); nothing else was affected.")
    w("- Research only; no trading.\n")

    w("## For picking stocks\n")
    w(f"Do not trade casino earnings off the monthly state revenue reports: they forecast same-store revenue well, but the market "
      f"already has them. No reliable announcement-day edge (t = {pr['t']:.2f}), no drift after the reports (t = {P['drift']['t']:.2f}), "
      f"and a coin-flip on beating consensus ({pct(a['hit_rate'], 0)}), in small caps as in large. They remain useful for knowing "
      "what a quarter will look like, not for beating the market to it.\n")

    # ------------------------------------------------------------------ live
    w("## Live nowcast, Q3 2026 (July-September; `data/live_nowcast.csv`)\n")
    w("State reports published by 2026-09-23: July and August for most states, July only for Nevada and Colorado. September is not "
      "out yet, so these are two-month (or one-month) reads. Given the results above, treat them as a preview of the quarter, "
      "not a trading signal.\n")
    w("| Company | Sample | Months | Coverage | Same-store GGR growth | Nowcast EBITDA growth | Last quarter's EBITDA growth | Signal (SD) | Reports |")
    w("|---|---|---|---|---|---|---|---|---|")
    for _, r in live.sort_values(["sample", "company"]).iterrows():
        w(f"| {NAMES.get(r['company'], r['company'])} | {r['sample']} | {r['months_covered']} | {r['coverage']:.2f} | {pct(r['ggr_growth_yoy'])} | "
          f"{pct(r['nowcast_ebitda_growth'])} | {pct(r['reported_ebitda_growth_prev_q'])} | {r['signal_z']:+.2f} | {r['next_report']} |")
    w("\nNotes: Penn's and MGM's year-ago quarters carry large impairments, so their EBITDA growth rates are not meaningful; "
      "Bally's coverage is overstated (see caveats); Iowa's July-August 2026 figures are left out (AGR redefined).\n")

    # ------------------------------------------------------------------ data table
    w("## State data used\n")
    w("| State | Source | Measure | Months | Units | Publication date |")
    w("|---|---|---|---|---|---|")
    rows = [
        ("PA", "Gaming Control Board revenue workbooks", "slot + table GGR", "2011-07 to 2026-08", "18 casinos (incl. Category 4)", "press releases, ~16 days"),
        ("NJ", "Division of Gaming Enforcement releases", "casino win (slots + tables)", "2012-01 to 2026-08", "14 casinos", "release date, ~14 days"),
        ("DE", "Delaware Lottery", "video lottery + table win (periods pro-rated)", "2012-01 to 2026-08", "3", "assumed"),
        ("MD", "Lottery & Gaming Control Agency releases", "GGR", "2012-01 to 2026-08", "6", "release date, ~5 days"),
        ("MA", "Gaming Commission", "GGR", "2015-06 to 2026-08", "3", "upload date, ~15 days"),
        ("NY", "Gaming Commission (Internet Archive copies)", "VGM net win / casino GGR", "2012-01 to 2025-09", "15", "partly, ~8 days"),
        ("RI", "RI Lottery", "net terminal income + tables", "2012-01 to 2026-07", "3", "partly, ~27 days"),
        ("ME", "Gambling Control Unit", "GGR", "2012-01 to 2026-08", "2", "~6 days"),
        ("OH", "Casino Control Commission + Ohio Lottery", "casino AGR; racino VLT net win", "2012-05 to 2026-08", "4 casinos + 7 racinos", "partly"),
        ("MI", "Gaming Control Board", "AGR (Detroit)", "2012-01 to 2026-08", "3", "from 2021, ~11 days"),
        ("WV", "WV Lottery weekly (pro-rated to months)", "VLT + table revenue", "2018-07 to 2026-08", "5", "partly"),
        ("KS", "Racing and Gaming Commission", "gaming facility revenue", "2012-01 to 2026-08", "4", "PDF date, ~16 days"),
        ("IN", "Gaming Commission", "win before deductions", "2012-01 to 2026-08", "15", "PDF date, ~9 days"),
        ("IL", "Gaming Board", "AGR", "2012-01 to 2026-08", "17", "to 2020-03, ~4 days"),
        ("IA", "Racing & Gaming Commission", "AGR", "2012-01 to 2026-08", "20", "2026 only"),
        ("MO", "Gaming Commission", "AGR", "2012-01 to 2026-08", "13", "file date, ~9 days"),
        ("LA", "State Police Gaming Division", "AGR (riverboats, racinos), GGR (land-based)", "2012-01 to 2026-08", "22", "file date, ~16 days"),
        ("FL", "Division of Pari-Mutuel Wagering", "net slot revenue", "2012-01 to 2026-08", "8", "mostly assumed"),
        ("MS", "Gaming Commission", "AGR by region (no casino detail)", "2012-01 to 2026-08", "3 regions", "~17 days"),
        ("CO", "Division of Gaming", "AGP by town (no casino detail)", "2012-01 to 2026-07", "3 towns", "mostly assumed"),
        ("NV", "Gaming Control Board", "win ex race/sports by area (no casino detail)", "2012-01 to 2026-07", "21 areas", "press release, ~29 days"),
    ]
    for r in rows:
        w("| " + " | ".join(r) + " |")
    w("\nScripts: `scripts/state_<st>.py` (download and parse, sources and spot checks in each docstring), `ownership.py`, "
      "`property_map.py`, `property_devices.py`, `sec_fetch.py`, `gaming_revenue.py`, `prices.py`, `eps_estimates.py`, "
      "`build_nowcast.py` (no returns), `run_tests.py`, `live_nowcast.py`, `write_results.py`.")
    (ROOT / "RESULTS.md").write_text("\n".join(L) + "\n")


if __name__ == "__main__":
    main()
