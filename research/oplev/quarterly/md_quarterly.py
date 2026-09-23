"""Renders RESULTS_QUARTERLY.md from results_quarterly.json (called by run_quarterly.py).

Every number is read from the results dictionary. The hand-written parts are the
questions, the "For picking stocks" sentences (written after the results were
in; each falls back to a neutral sentence if the verdict differs from the one
seen) and the caveats.
"""
from __future__ import annotations

import datetime as dt


def p(x, d=1):
    return "n/a" if x is None else f"{x*100:.{d}f}%"


def pts(x, d=1):
    return "n/a" if x is None else f"{x*100:+.{d}f} points"


def tt(x):
    return "n/a" if x is None else f"{x:.2f}"


def n0(x):
    return f"{int(x):,}"


def mon(s):
    return dt.date.fromisoformat(s).strftime("%b %Y")


def eff(x, won="signal ahead"):
    return (f"{pts(x['ann_diff'])} a year (NW t = {tt(x['t_nw6'])}, t = {tt(x['t'])}; {won} in "
            f"{x['years_positive']} of {x['n_years']} years)")


TESTS = {
    "H5": dict(
        title="H5. The quarterly report, acted on the next month",
        q=("When a company whose costs are mostly fixed reports a quarter in which year-over-year sales growth "
           "sped up (top 30% of that month's filers, and faster than the quarter before), does buying at the "
           "first month-end after the filing and holding three months beat the other companies that filed that "
           "month?"),
        sig="the signal portfolio (high fixed costs, accelerating sales)",
        ctl="the other companies that filed that month"),
    "H6": dict(
        title="H6. Backlog running ahead of sales",
        q=("When a high-fixed-cost company's remaining performance obligations (contracted revenue not yet "
           "recognised, reported since ASC 606) grow faster than its sales, does the stock beat other companies "
           "reporting RPO that month?"),
        sig="the signal portfolio (RPO growth well ahead of sales growth, high fixed costs)",
        ctl="the other RPO reporters that filed that month"),
}


def _pick_h5(x):
    if x["verdict"] != "No":
        return "See the verdict above; this line was written for a 'No' result."
    f = x["fundamental_check"]
    m = x["matched_size_sic2"]
    return (f"Acting fast on the quarterly report does not help. Operating leverage does kick in at quarterly speed: "
            f"the signal companies' operating margins rose a median {f['table']['signal']['fwd_margin_chg_pp_median']:+.2f} "
            f"points year over year in the next quarter, against {f['table']['control']['fwd_margin_chg_pp_median']:+.2f} "
            f"for the other filers. But the stocks did no better than the other filers held the same way "
            f"({pts(x['ew']['ann_diff'])} a year), and against companies of the same size in the same industry they "
            f"did worse ({pts(m['ann_diff'])}). By the first month-end after the 10-Q, the price already reflects "
            f"the acceleration. Do not buy a fixed-cost company because its latest quarter showed sales speeding up.")


def _pick_h6(x):
    if x["verdict"] != "No":
        return "See the verdict above; this line was written for a 'No' result."
    f = x["fundamental_check"]
    return (f"Backlog growing faster than sales is not a usable signal on this evidence. The gap "
            f"({pts(x['ew']['ann_diff'])} a year) is statistically weak, comes from small caps "
            f"({pts(x['small_ew']['ann_diff'])}) rather than large ones ({pts(x['large_ew']['ann_diff'])}), and "
            f"disappears against same-size companies in the same industry ({pts(x['matched_size_sic2']['ann_diff'])}). "
            f"The accounts do not back it either: the signal companies' next-quarter margins moved "
            f"{f['table']['signal']['fwd_margin_chg_pp_median']:+.2f} points against "
            f"{f['table']['control']['fwd_margin_chg_pp_median']:+.2f} for other RPO reporters. With a median of "
            f"{int(x['counts']['signal_held_median'])} stocks held and under eight years of data, a real effect of a "
            f"few points a year could not be told apart from luck; treat a growing backlog as a question to ask, "
            f"not a reason to buy. The signal portfolio's {p(x['ew']['ann_top'])} a year against IWM's "
            f"{p(x['top_vs']['iwm']['ann_bench'])} mostly reflects which companies report RPO (the other RPO reporters "
            f"returned {p(x['ew']['ann_bottom'])}) and the missing-company bias, not the signal.")


PICK = {"H5": _pick_h5, "H6": _pick_h6}


def test_section(r, k):
    x, T = r[k], TESTS[k]
    e = x["ew"]
    L = [f"## {T['title']}", "", f"**Question.** {T['q']}", ""]
    L.append(f"**Answer: {x['verdict']}.** {T['sig'][0].upper() + T['sig'][1:]} did not reliably beat "
             f"{T['ctl']} (Newey-West t = {tt(e['t_nw6'])}, below the pre-registered bar of 2.0)."
             if x["verdict"] == "No" else
             f"**Answer: {x['verdict']}.** Newey-West t = {tt(e['t_nw6'])} (bar 2.0).")
    if k == "H6":
        c = x["counts"]
        if c["months_with_fewer_than_30_signal_held"] > c["n_months"] / 2:
            L[-1] += (f" **Fewer than 30 signal companies were held in most months** ({c['months_with_fewer_than_30_signal_held']} "
                      f"of {c['n_months']}; median {int(c['signal_held_median'])}), as the pre-registration asked to flag.")
    L.append("")
    nm = e["n_months"]
    v_top = 10000 * (1 + e["ann_top"]) ** (nm / 12)
    v_bot = 10000 * (1 + e["ann_bottom"]) ** (nm / 12)
    L.append(f"**Size of the effect (equal-weighted, the pre-registered headline).** {T['sig'][0].upper() + T['sig'][1:]} "
             f"returned {p(e['ann_top'])} a year against {p(e['ann_bottom'])} for {T['ctl']}, a gap of "
             f"{pts(e['ann_diff'])} a year ({mon(e['first_month'])} to {mon(e['last_month'])}, {nm} months). Monthly "
             f"spread: Newey-West t {tt(e['t_nw6'])}, plain t {tt(e['t'])}. The signal was ahead in {e['years_positive']} "
             f"of {e['n_years']} calendar years. $10,000 would have become ${v_top:,.0f} in the signal portfolio and "
             f"${v_bot:,.0f} in the control, before costs.")
    L += ["", "**How much to trust it.**", ""]
    h1, h2 = x["first_half"], x["second_half"]
    L.append(f"- First half ({mon(h1['first_month'])} to {mon(h1['last_month'])}): {eff(h1)}. "
             f"Second half ({mon(h2['first_month'])} to {mon(h2['last_month'])}): {eff(h2)}.")
    L.append(f"- Small caps (< $2B): {eff(x['small_ew'])}. Large caps (>= $2B): {eff(x['large_ew'])}.")
    m = x["matched_size_sic2"]
    L.append(f"- Matched within size tercile x 2-digit SIC (each signal stock against the control stocks of the same "
             f"size tercile and industry that month): {eff(m)}; {n0(m['n_signal_filings_matched'])} of "
             f"{n0(x['n_signal_filings'])} signal filings had a match.")
    L.append(f"- Value-weighted: {eff(x['vw'])}.")
    L.append(f"- Holding 1 month instead of 3: {eff(x['hold_1m_ew'])}. Holding 6 months: {eff(x['hold_6m_ew'])}.")
    s = x["survivorship"]
    sc = s["scenarios_ew"]
    b, b50, c, c50 = (sc["b_minus30_all_missing"], sc["b_minus30_float50_missing"], sc["c_plus15_all_missing"],
                      sc["c_plus15_float50_missing"])
    signs = {v["mean_monthly_x12"] > 0 for v in sc.values()}
    L.append(f"- Missing companies: {p(s['missing_share_signal'])} of the would-be signal filings and "
             f"{p(s['missing_share_control'])} of the would-be control filings have no price "
             f"({p(s['missing_share_signal_float50'])} and {p(s['missing_share_control_float50'])} counting only public "
             f"float >= $50M), so the two sides lose companies at about the same rate. If every missing company lost "
             f"30% a year: {pts(b['ann_diff'])}, NW t = {tt(b['t_nw6'])} (float >= $50M only: {pts(b50['ann_diff'])}, "
             f"NW t = {tt(b50['t_nw6'])}); if every missing company gained 15%: {pts(c['ann_diff'])}, NW t = "
             f"{tt(c['t_nw6'])} ({pts(c50['ann_diff'])}, NW t = {tt(c50['t_nw6'])}). "
             + ("The sign does not change across these assumptions" if len(signs) == 1 else
                "**The sign changes across these assumptions**")
             + (", and none lifts the t-statistic to 2." if max(v["t_nw6"] for v in sc.values()) < 2 else
                "; at least one assumption lifts the t-statistic above 2."))
    L.append(f"- Raw Yahoo returns, no bad-print rule: {eff(x['raw_returns_ew'])}. Most or all of the difference "
             f"from the cleaned result is Chord Energy's November 2020 splice (+30,991%, in the control group; see Caveats).")
    L.append(f"- Extra, not pre-registered: control limited to companies where the signal could be computed at all: "
             f"{eff(x['extra_control_evaluable_only'])}.")
    tv = x["top_vs"]
    L.append(f"- The signal portfolio after 0.5% a year of trading costs: {p(tv['univ_ew']['ann_top_net'])} a year vs "
             f"{p(tv['univ_ew']['ann_bench'])} for the equal-weighted universe of filers ({pts(tv['univ_ew']['ann_excess'])}, "
             f"t = {tt(tv['univ_ew']['t'])}), {p(tv['iwm']['ann_bench'])} for IWM ({pts(tv['iwm']['ann_excess'])}, "
             f"t = {tt(tv['iwm']['t'])}) and {p(tv['spy']['ann_bench'])} for SPY ({pts(tv['spy']['ann_excess'])}, "
             f"t = {tt(tv['spy']['t'])}).")
    cn = x["counts"]
    few = [k2 for k2, v in cn["signal_held_per_month"].items() if v < 30]
    few_txt = (f"; {len(few)} of {cn['n_months']} months held fewer than 30 (first {mon(few[0])}, last {mon(few[-1])})"
               if few else "; no month held fewer than 30")
    L.append(f"- Signal counts: median {int(cn['signal_held_median'])} companies held in a month (min "
             f"{cn['signal_held_min']}, max {cn['signal_held_max']}){few_txt}; {n0(cn['signal_distinct_companies'])} "
             f"distinct companies over the period; the control held a median {n0(cn['control_held_median'])}. "
             f"Monthly counts are in `results_quarterly.json`.")
    L.append("")
    f = x["fundamental_check"]
    tag = "" if k == "H5" else " Reported for information; the pre-registration set this check for H5 only."
    L.append(f"**Fundamental check (next reported quarter vs the same quarter a year earlier, first-reported numbers).**{tag}")
    L += ["", "| Group | Next quarter: change in operating margin (median, pts) | Next quarter: revenue growth (median) "
              "| Signal quarter: revenue growth (median) | Change in growth, next vs signal quarter (median, pts) "
              "| Filings (with a next quarter) |", "|---|---|---|---|---|---|"]
    for g in ("signal", "control"):
        t = f["table"][g]
        L.append(f"| {g.capitalize()} | {t['fwd_margin_chg_pp_median']:+.2f} | {p(t['fwd_rev_growth_median'])} | "
                 f"{p(t['cur_rev_growth_median'])} | {t['fwd_growth_chg_median']*100:+.1f} | {n0(t['n'])} "
                 f"({n0(t['n_with_fwd'])}) |")
    L.append("")
    verdict_txt = ("positive, so the mechanism is present at quarterly speed" if f["mechanism_present"]
                   else "not positive, so the mechanism does not show up at quarterly speed")
    L.append(f"Signal minus control: {f['signal_minus_control_median_pp']:+.2f} points of operating margin; the signal "
             f"group was ahead in {f['years_signal_above']} of {f['n_years']} calendar years (mean yearly gap "
             f"{f['by_year_mean']:+.2f} points, t = {tt(f['by_year_t'])}). The difference is {verdict_txt}.")
    L.append("")
    L.append(f"**For picking stocks.** {PICK[k](x)}")
    L.append("")
    return L


def render(r: dict) -> str:
    h5, h6 = r["H5"], r["H6"]
    L = ["# Can we spot operating leverage kicking in before the market? Quarterly tests H5 and H6", ""]
    L.append(f"*Generated {dt.date.today().isoformat()} by `research/oplev/quarterly/run_quarterly.py`. Signals are formed "
             f"at each month-end from 10-Q and 10-K filings, using every number as the SEC filing first reported it. "
             f"H5 returns run {mon(h5['ew']['first_month'])} to {mon(h5['ew']['last_month'])} ({h5['ew']['n_months']} "
             f"months); H6 {mon(h6['ew']['first_month'])} to {mon(h6['ew']['last_month'])} ({h6['ew']['n_months']} months). "
             f"Every number below is in `results_quarterly.json`. Pre-registration: `../H5_H6_PREREG.md`; its "
             f"Deviations section was written before any H5 or H6 return was computed.*")
    L += ["", "## The short answer", "",
          "| Test | Answer | Signal minus control, per year (equal-weighted) | Newey-West t | Plain t | Years signal won |",
          "|---|---|---|---|---|---|"]
    for k, lab in (("H5", "H5. Fixed costs + sales acceleration, bought the month after each 10-Q/10-K"),
                   ("H6", "H6. Backlog (RPO) growing faster than sales, fixed costs")):
        e = r[k]["ew"]
        L.append(f"| {lab} | {r[k]['verdict']} | {pts(e['ann_diff'])} | {tt(e['t_nw6'])} | {tt(e['t'])} | "
                 f"{e['years_positive']} of {e['n_years']} |")
    tv = h5["top_vs"]
    L += ["", "\"Signal minus control\" is the difference between the two portfolios' compound annual returns. Each "
              "month holds three overlapping monthly cohorts, so the verdict uses the Newey-West t-statistic (6 lags) on "
              "the monthly return differences; 2.0 is the pre-registered bar. Years are calendar years; the first and "
              f"last are partial. Benchmarks over H5's months: equal-weighted universe of filers "
              f"{p(tv['univ_ew']['ann_bench'])} a year, IWM {p(tv['iwm']['ann_bench'])}, SPY {p(tv['spy']['ann_bench'])}.",
          ""]
    L.append(f"In one line each: **H5** {h5['verdict']} ({pts(h5['ew']['ann_diff'])} a year, NW t = "
             f"{tt(h5['ew']['t_nw6'])}, {h5['ew']['years_positive']} of {h5['ew']['n_years']} years); the margins do jump "
             f"the next quarter ({h5['fundamental_check']['signal_minus_control_median_pp']:+.2f} points vs the control), "
             f"but the price has already moved. **H6** {h6['verdict']} ({pts(h6['ew']['ann_diff'])} a year, NW t = "
             f"{tt(h6['ew']['t_nw6'])}, {h6['ew']['years_positive']} of {h6['ew']['n_years']} years), on a thin portfolio "
             f"(median {int(h6['counts']['signal_held_median'])} stocks).")
    L += ["", "## Read this first", "",
          "H2b (see `../RESULTS.md`) found that operating leverage is real in the accounts but not in returns when acted "
          "on with annual data four to six months old. These tests act on each 10-Q and 10-K at the first month-end "
          "after it is filed, using only numbers as first reported (never later restatements), so they ask whether "
          "the lag was the problem.", "",
          "The missing-company problem of H1-H3 applies unchanged. The universe comes from every company that filed "
          "with the SEC at the time; companies later acquired or delisted usually have no Yahoo price and cannot be "
          "held. They are counted, placed in the signal or control group with their own filings, and re-run under the "
          "-30% and +15% assumptions in each test. Filings per calendar year (a company files about four times a year):",
          "", "| Year | Universe filings (priced, >= $50M) | Missing: passes filters, no price | Missing share | "
              "Missing with float >= $50M | Not yet listed (excluded) |", "|---|---|---|---|---|---|"]
    for y, c in r["coverage_by_calendar_year"].items():
        if int(y) < 2011:
            continue
        L.append(f"| {y} | {n0(c['universe'])} | {n0(c['missing'])} | {p(c['missing_share'], 0)} | "
                 f"{n0(c['missing_float50'])} | {n0(c['not_yet_listed'])} |")
    L += ["", "2026 covers filings through July (held into August). In both tests the signal and control groups lose "
              "about the same share of companies (see each test), so the comparison between them is less exposed than "
              "the absolute returns.", ""]
    L += test_section(r, "H5")
    L += test_section(r, "H6")
    # RPO reporters table
    L += ["**How many companies report RPO.** Distinct companies whose 10-Q or 10-K reported a total remaining "
          "performance obligation at the quarter end, by calendar year of the formation month:", "",
          "| Year | In the universe (priced, >= $50M) | All that pass the filters (incl. unpriced) | H6 signal filings |",
          "|---|---|---|---|"]
    for y, c in r["coverage_by_calendar_year"].items():
        if int(y) < 2018:
            continue
        L.append(f"| {y} | {n0(c['universe_rpo_distinct_companies'])} | {n0(c['all_rpo_distinct_companies'])} | "
                 f"{n0(c['signal_H6'])} |")
    L += ["", "Year-over-year RPO needs a year of reporting after ASC 606 took effect (2018), so H6 starts in spring 2019.", ""]
    b = r.get("build", {})
    k10 = b.get("q0_src_counts", {})
    L += ["## Caveats", ""]
    L.append(f"- **First-reported numbers.** Every quarterly value is taken from the first filing that reported that "
             f"period, available from its filing date. Q4 is rarely reported on its own: {n0(b.get('quarters_q4_derived', 0))} "
             f"of {n0(b.get('quarters_total', 0))} company-quarters are a derived Q4 (the 10-K's full year minus the "
             f"first-reported nine months), and for {n0(k10.get('derived_fy_minus_9m', 0))} of the 10-K triggers the "
             f"just-reported quarter is such a derived Q4. Revenue follows the annual study's tag order within each "
             f"filing; when a company switched revenue tags between the quarter and the year-ago quarter the growth "
             f"rate compares two tags.")
    L.append("- **What counts as acceleration.** Year-over-year growth includes acquisitions, so some H5 signals are "
             "deals rather than organic demand (for example Shentel after buying nTelos in 2016). H6's gap is "
             "\"RPO growth minus sales growth\", so a shrinking company whose backlog falls less than its sales, or a "
             "tiny RPO balance that multiplies, also qualifies (examples in the data: LSB Industries 2023, Sturm Ruger "
             "2025). Both definitions were fixed in advance and are not changed here.")
    mi = r["meta"]["price_error_rule"]
    L.append(f"- **Price errors.** The H1-H3 bad-print rule removed {mi['v_reversals_removed']} one-month 10x round trips "
             f"and {mi['returns_above_1000pct_removed']} monthly returns above +1,000% across all symbols. Only three "
             f"fell in stocks these tests held, all in the control groups: Chord Energy's November 2020 +30,991% (a "
             f"bankruptcy splice that never happened to a holder), GameStop's +1,625% in January 2021 and Urban One's "
             f"+1,446% in June 2020. The raw-return lines above differ from the cleaned ones mainly because of Chord. "
             f"The return matrix was rebuilt from the annual study's price cache and matches `../cache/returns.parquet` "
             f"in {p(mi['check_vs_annual_returns_parquet']['share_cells_identical'], 1)} of cells.")
    few5 = [k2 for k2, v in h5["counts"]["signal_held_per_month"].items() if v < 30]
    L.append("- **Early years.** Fixed-cost share needs four fiscal years of XBRL data, so until 2013 mostly large, "
             "long-listed companies have one and the H5 signal portfolio is small"
             + (f" (every month with fewer than 30 holdings falls between {mon(few5[0])} and {mon(few5[-1])})."
                if few5 else "."))
    L.append(f"- **H6 is thin.** {n0(h6['counts']['signal_distinct_companies'])} distinct companies ever enter the H6 "
             f"signal, over {h6['ew']['n_months']} months; a real effect of a few points a year could not reach t = 2 "
             f"in a sample this size.")
    L.append(f"- **Several looks.** Two hypotheses, each cut about a dozen ways. The closest cut to the bar is H5 held six "
             f"months ({pts(h5['hold_6m_ew']['ann_diff'])} a year, NW t = {tt(h5['hold_6m_ew']['t_nw6'])}); with this "
             f"many cuts one near 2 is expected by chance, and the matched and half-period results do not support it.")
    L.append("- **Other data limits.** Industry codes are each company's current SIC code. Market caps use the most "
             "recent SEC share count before the month-end on Yahoo's split basis (only the $50M filter, the $2B split, "
             "size terciles and value weights depend on them). The company list is the annual study's (revenue above "
             "$10M in some fiscal year 2010-2024). Only the signal-versus-universe comparison deducts costs (0.5% a "
             "year); a portfolio that turns over every three months would cost more in practice.")
    L += ["", "## Files", "",
          "- `research/oplev/quarterly/fetch_facts.py` downloads SEC companyfacts (cached in `quarterly/cache/`)",
          "- `research/oplev/quarterly/build_quarterly.py` builds first-reported quarterly fundamentals, fixed-cost "
          "shares and RPO per filing",
          "- `research/oplev/quarterly/run_quarterly.py` the pre-registered tests; `md_quarterly.py` renders this file",
          "- `research/oplev/quarterly/results_quarterly.json` every number; `monthly_returns_quarterly.csv` monthly "
          "signal, control and universe returns",
          "- `research/oplev/H5_H6_PREREG.md` the pre-registration and its Deviations section", ""]
    return "\n".join(L)
