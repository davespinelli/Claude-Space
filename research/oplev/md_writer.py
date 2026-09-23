"""Renders RESULTS.md from results.json (called by run_tests.py).

Every number in the write-up is read from the results dictionary; the only
hand-written parts are the questions, the verdict-dependent sentences below
(TAKEAWAY) and the caveats.
"""
from __future__ import annotations

import datetime as dt

TESTS = [
    ("H1_OL", "H1. Operating-leverage level",
     "Do companies with high operating costs per dollar of assets (Novy-Marx's measure of operating "
     "leverage) earn higher stock returns?",
     "the highest-operating-leverage fifth", "the lowest fifth"),
    ("H2a_FCS", "H2a. Fixed-cost share",
     "Do companies whose costs are mostly fixed (they barely move when sales move) earn higher returns?",
     "the most-fixed-cost fifth", "the most-variable-cost fifth"),
    ("H2b_FCSxAccel", "H2b. Fixed costs plus accelerating sales (operating leverage \"kicking in\")",
     "When sales growth speeds up at a company whose costs are mostly fixed, do profits jump and does "
     "the stock outperform?",
     "the high-fixed-cost, accelerating-sales group", "the average of the other eight groups"),
    ("H3_margin_chg", "H3. Margin expansion on growing sales",
     "Among companies with growing sales, do the ones whose operating margin widened the most keep "
     "outperforming (the market under-reacts), or is it already in the price?",
     "the biggest-margin-expansion fifth", "the biggest-margin-contraction fifth"),
]

# Plain-English consequence for stock picking. Written after the results were
# in; each function only phrases numbers taken from the results dictionary and
# falls back to a neutral sentence if the verdict differs from the one seen.


def _t_h1(r):
    x = r["H1_OL"]
    if x["verdict"]["verdict"] != "No":
        return "See the verdict above; this line was written for a 'No' result."
    i = x["ind_neutral_ew_spread"]
    b = x["survivorship"]["scenarios_ew_spread"]["b_minus30_all_missing"]
    flip = (f", and it turns negative ({pts(b['ann_diff'])}) if every missing company is assumed to have "
            f"lost 30%" if b["mean_monthly_x12"] < 0 else "")
    return (f"Do not buy a stock because it runs a lot of operating cost through a small asset base. "
            f"High-OL stocks did a little better in most cuts, but the headline gap did not clear the bar"
            f"{flip}. The version closest to Novy-Marx's original (sorting within industries) is borderline at "
            f"{pts(i['ann_diff'])} a year, t = {tt(i['t'])}: at most a weak tilt, not a selection rule.")


def _t_h2a(r):
    x = r["H2a_FCS"]
    if x["verdict"]["verdict"] != "No":
        return "See the verdict above; this line was written for a 'No' result."
    e = x["ew_ann"]
    return (f"The closest call of the four. Equal-weighted returns rise step by step from the most-variable-cost "
            f"fifth ({p(e['1'])}) to the most-fixed-cost fifth ({p(e['5'])}) and the gap stays positive under every "
            f"delisting assumption, but it misses the pre-registered bar, is weak in the first half, and is "
            f"small in value-weighted terms ({pts(x['vw_spread']['ann_diff'])}). Whatever premium exists lives "
            f"in small caps, where trading costs are highest. Treat a high fixed-cost share as a risk trait to "
            f"know about, not an edge to buy.")


def _t_h2b(r):
    x = r["H2b_FCSxAccel"]
    if x["verdict"]["verdict"] != "No":
        return "See the verdict above; this line was written for a 'No' result."
    fc = x["fundamental_check"]
    return (f"Operating leverage does kick in inside the accounts: these companies' margins widened by a median "
            f"{fc['HH_median_fwd_margin_chg_pp']:+.2f} points the next year against {fc['others_median_fwd_margin_chg_pp']:+.2f} "
            f"for everyone else. But most of that comes from the sales acceleration itself (the extra from high "
            f"fixed costs, the difference-in-differences, is only {fc['DiD_fwd_margin_chg_pp']:+.2f} points), and "
            f"the stocks earned no reliable premium. Spotting the setup in last year's filings is not an edge; "
            f"you would have to anticipate the acceleration before it is reported.")


def _t_h3(r):
    x = r["H3_margin_chg"]
    if x["verdict"]["verdict"] != "No":
        return "See the verdict above; this line was written for a 'No' result."
    f = x["fundamentals_median_by_group"]
    return (f"Last year's margin expansion is already in the price. The biggest expanders did keep improving "
            f"(median margin change next year {f['5']['fwd_margin_chg_pp']:+.2f} points vs "
            f"{f['1']['fwd_margin_chg_pp']:+.2f} for the biggest contractors), yet their stocks did no better. "
            f"Do not buy a company just because its profits grew faster than its sales last year.")


def _one(key):
    def f(x):
        h = head(x, key)
        v = x["verdict"]["verdict"]
        return f"{v} ({pts(h['ann_diff'])} a year, t = {tt(h['t'])}, {h['years_positive']} of {h['n_years']} years)."
    return f


ONE_LINE = {k: _one(k) for k in ("H1_OL", "H2a_FCS", "H2b_FCSxAccel", "H3_margin_chg")}

TAKEAWAY = {"H1_OL": _t_h1, "H2a_FCS": _t_h2a, "H2b_FCSxAccel": _t_h2b, "H3_margin_chg": _t_h3}


SCEN_NAMES = {"a_excluded": "exclusion", "b_minus30_all_missing": "-30% for all missing firms",
              "b_minus30_float50_missing": "-30% for float >= $50M missing firms",
              "c_plus15_all_missing": "+15% for all missing firms",
              "c_plus15_float50_missing": "+15% for float >= $50M missing firms"}


def p(x, d=1, sign=False):
    if x is None:
        return "n/a"
    return f"{x * 100:+.{d}f}%" if sign else f"{x * 100:.{d}f}%"


def pts(x, d=1):
    if x is None:
        return "n/a"
    return f"{x * 100:+.{d}f} points"


def tt(x):
    return "n/a" if x is None else f"{x:.2f}"


def money(ann, months, start=10_000):
    if ann is None:
        return "n/a"
    return f"${start * (1 + ann) ** (months / 12):,.0f}"


def head(r, key):
    if key == "H2b_FCSxAccel":
        return r["ew_HH_minus_rest"]
    return r["ew_spread"]


def pieces(r, key):
    if key == "H2b_FCSxAccel":
        return dict(
            head=r["ew_HH_minus_rest"], vw=r["vw_HH_minus_rest"], ind=r["ind_neutral_ew_HH_minus_rest"],
            small=r["small_ew_HH_minus_rest"], large=r["large_ew_HH_minus_rest"],
            h1=r["first_half_ew_HH_minus_rest"], h2=r["second_half_ew_HH_minus_rest"],
            raw=r["raw_returns_ew_HH_minus_rest"], raw1=r["raw_returns_minus_largest_month_ew_HH_minus_rest"])
    return dict(head=r["ew_spread"], vw=r["vw_spread"], ind=r["ind_neutral_ew_spread"],
                small=r["small_ew_spread"], large=r["large_ew_spread"], h1=r["first_half_ew_spread"],
                h2=r["second_half_ew_spread"], raw=r["raw_returns_ew_spread"],
                raw1=r["raw_returns_minus_largest_month_ew_spread"])


def line_spread(s):
    return (f"{pts(s['ann_diff'])} a year (t = {tt(s['t'])}; top ahead in "
            f"{s['years_positive']} of {s['n_years']} years)")


def section(r, key, title, q, top_name, bot_name, takeaway):
    x = pieces(r, key)
    h = x["head"]
    v = r["verdict"]
    L = [f"## {title}", ""]
    L.append(f"**Question.** {q}")
    L.append("")
    L.append(f"**Answer: {v['verdict']}.** " + answer_sentence(key, v, h, top_name, bot_name))
    L.append("")
    months = h["n_months"]
    L.append(f"**Size of the effect (equal-weighted, the pre-registered headline).** {top_name[0].upper()+top_name[1:]} "
             f"returned {p(h['ann_top'])} a year against {p(h['ann_bottom'])} for {bot_name}, a gap of "
             f"{pts(h['ann_diff'])} a year; the top group was ahead in {h['years_positive']} of "
             f"{h['n_years']} holding years. $10,000 held for the {months} months "
             f"would have become {money(h['ann_top'], months)} in the top group and "
             f"{money(h['ann_bottom'], months)} in the bottom one, before costs. "
             f"Monthly spread t-statistic {tt(h['t'])} (Newey-West {tt(h['t_nw6'])}).")
    L.append("")
    L.append("**How much to trust it.**")
    L.append("")
    sv = r["survivorship"]
    sc = sv["scenarios_ew_spread"]
    signs = {k: (s["mean_monthly_x12"] > 0) for k, s in sc.items()}
    L.append(f"- First half (formations 2011-2017): {line_spread(x['h1'])}. "
             f"Second half (2018-2025): {line_spread(x['h2'])}.")
    L.append(f"- Within industries (2-digit SIC): {line_spread(x['ind'])}.")
    L.append(f"- Small caps (< $2B): {line_spread(x['small'])}. Large caps (>= $2B): {line_spread(x['large'])}.")
    L.append(f"- Value-weighted (secondary): {line_spread(x['vw'])}.")
    botlab = "the other eight groups (average)" if key == "H2b_FCSxAccel" else "the would-be bottom group"

    def sct(k):
        return f"{pts(sc[k]['ann_diff'])}, t = {tt(sc[k]['t'])}"
    sig = [k for k, v in sc.items() if v["t"] is not None and v["t"] >= 2.0]
    if sig:
        concl = ("Under " + " and ".join(SCEN_NAMES[k] for k in sig) + " the t-statistic reaches 2, but not under "
                 "the others, so no assumption turns the answer into a robust yes.")
    else:
        concl = "No assumption lifts the t-statistic to 2, so the answer does not flip."
    L.append(f"- Missing companies: {p(sv['missing_share_top'])} of the would-be top group and "
             f"{p(sv['missing_share_bottom'])} of {botlab} have no price. "
             f"Spread with missing firms excluded {sct('a_excluded')}; if every missing firm lost 30%: "
             f"{sct('b_minus30_all_missing')} (only those with public float >= $50M: {sct('b_minus30_float50_missing')}); "
             f"if every missing firm gained 15%: {sct('c_plus15_all_missing')} ({sct('c_plus15_float50_missing')}). "
             + ("The sign does not change across these assumptions. " if len(set(signs.values())) == 1
                else "**The sign changes across these assumptions.** ") + concl)
    L.append(f"- Raw Yahoo returns, no bad-print rule: {line_spread(x['raw'])}; raw returns with only the single "
             f"largest held monthly return removed: {line_spread(x['raw1'])}.")
    tv = r["top_vs"]
    L.append(f"- The top group after 0.5% a year of trading costs: {p(tv['univ_ew']['ann_top_net'])} a year vs "
             f"{p(tv['univ_ew']['ann_bench'])} for the equal-weighted universe ({pts(tv['univ_ew']['ann_excess'])}, "
             f"t = {tt(tv['univ_ew']['t'])}) and {p(tv['iwm']['ann_bench'])} for IWM "
             f"({pts(tv['iwm']['ann_excess'])}, t = {tt(tv['iwm']['t'])}).")
    L.append("")
    L.append(fund_para(r, key))
    L.append("")
    L.append(f"**For picking stocks.** {takeaway}")
    L.append("")
    return "\n".join(L)


def answer_sentence(key, v, h, top_name, bot_name):
    t = h["t"]
    if v["verdict"].startswith("No (reversed)"):
        return (f"The opposite of the hypothesis: {top_name} did worse than {bot_name}, reliably (t = {tt(t)}).")
    if v["verdict"] == "No":
        return (f"{top_name[0].upper()+top_name[1:]} did not reliably beat {bot_name} "
                f"(t = {tt(t)}, below the pre-registered bar of 2.0).")
    failed = [k for k, ok in v["checks"].items() if not ok and k != "t_ge_2"]
    if v["verdict"] == "Yes":
        return (f"{top_name[0].upper()+top_name[1:]} beat {bot_name} (t = {tt(t)}) and passed every "
                f"pre-registered robustness check.")
    names = {"both_halves_positive": "it did not hold in both halves",
             "industry_neutral_positive": "it disappeared within industries",
             "all_survivorship_scenarios_positive": "it flipped under a delisting assumption",
             "fundamental_HH_largest_margin_expansion": "the profit mechanism did not show up in the fundamentals"}
    return (f"{top_name[0].upper()+top_name[1:]} beat {bot_name} (t = {tt(t)}), but "
            + "; ".join(names.get(f, f) for f in failed) + ".")


def fund_para(r, key):
    if key == "H2b_FCSxAccel":
        fc = r["fundamental_check"]
        ft = r["fundamentals_median_by_cell"]
        cells = " | ".join(f"{k}: {v['fwd_margin_chg_pp']:+.2f}" for k, v in sorted(ft.items()))
        lh, did = r["ew_HH_minus_LH"], r["ew_DiD"]
        extra = (f"**Other pre-registered cuts of the returns.** High vs low fixed costs among accelerating firms: "
                 f"{pts(lh['ann_diff'])} a year (t = {tt(lh['t'])}). The pure interaction, (high-FCS accelerating "
                 f"minus high-FCS slowing) minus (low-FCS accelerating minus low-FCS slowing): "
                 f"{pts(did['mean_monthly_x12'])} a year on average (t = {tt(did['t'])}).\n\n")
        return extra + (f"**Does the mechanism show up in the fundamentals?** Median change in operating margin over "
                f"the next fiscal year: {fc['HH_median_fwd_margin_chg_pp']:+.2f} percentage points for the "
                f"high-fixed-cost, accelerating group vs {fc['others_median_fwd_margin_chg_pp']:+.2f} for all "
                f"other groups; the group ranked {fc['HH_rank_among_9_cells']} of 9 and was ahead of the rest in "
                f"{fc['years_HH_above_others']} of {fc['n_years']} years (t = {tt(fc['HH_minus_others_by_year_t'])}). "
                f"Difference-in-differences in margin change: {fc['DiD_fwd_margin_chg_pp']:+.2f} points. "
                f"All cells (FCS tercile then acceleration tercile, 1 = low): {cells}.")
    ft = r["fundamentals_median_by_group"]
    rows = ["| Group | Next-year change in operating margin (median, pts) | Next-year revenue growth (median) | Change in revenue growth (median, pts) |",
            "|---|---|---|---|"]
    for k, v in sorted(ft.items(), key=lambda kv: int(kv[0])):
        rows.append(f"| Q{k} | {v['fwd_margin_chg_pp']:+.2f} | {p(v['fwd_rev_growth'])} | "
                    f"{v['fwd_growth_chg'] * 100:+.1f} |")
    return "**Fundamental sanity check (next fiscal year, CY t vs CY t-1).**\n\n" + "\n".join(rows)


def quintile_table(r, key):
    if key == "H2b_FCSxAccel":
        e = r["ew_ann"]
        rows = ["| FCS tercile \\ acceleration tercile | 1 (slowing) | 2 | 3 (accelerating) |", "|---|---|---|---|"]
        for f in (1, 2, 3):
            rows.append(f"| {f} {'(variable costs)' if f == 1 else '(fixed costs)' if f == 3 else '(middle)'} | "
                        + " | ".join(p(e.get(str(f * 10 + a))) for a in (1, 2, 3)) + " |")
        return "Annualised equal-weighted return by cell:\n\n" + "\n".join(rows)
    e, w = r["ew_ann"], r["vw_ann"]
    ks = sorted(e, key=int)
    rows = ["| | " + " | ".join(f"Q{k}" for k in ks) + " |", "|---" * (len(ks) + 1) + "|",
            "| Equal-weighted | " + " | ".join(p(e[k]) for k in ks) + " |",
            "| Value-weighted | " + " | ".join(p(w[k]) for k in ks) + " |",
            "| Industry-neutral EW | " + " | ".join(p(r["ind_neutral_ew_ann"].get(k)) for k in ks) + " |"]
    return "Annualised return by quintile (Q1 = lowest signal, Q5 = highest):\n\n" + "\n".join(rows)


def render(r: dict) -> str:
    u = r["universe"]
    b = r["benchmarks"]
    L = ["# Does operating leverage predict stock returns? Pre-registered study", ""]
    L.append(f"*Generated {dt.date.today():%Y-%m-%d} by `research/oplev/run_tests.py`. Portfolios formed each June "
             f"2011-2025 from SEC filings, held July to June; returns {b['first_month']} to {b['last_month']} "
             f"({b['n_months']} months). Every number below is in `results.json`.*")
    L.append("")
    L.append("## The short answer")
    L.append("")
    L.append("| Test | Answer | Top minus bottom, per year (equal-weighted) | t-stat | Years top won |")
    L.append("|---|---|---|---|---|")
    for key, title, *_ in TESTS:
        h = head(r[key], key)
        L.append(f"| {title} | {r[key]['verdict']['verdict']} | {pts(h['ann_diff'])} | {tt(h['t'])} | "
                 f"{h['years_positive']} of {h['n_years']} |")
    L.append("")
    L.append(f"\"Top minus bottom\" is the difference between the two groups' compound annual returns; the t-statistic "
             f"is computed on the monthly return differences (2.0 is the pre-registered bar). The two can differ in "
             f"sign when the gap is near zero. H2 needs four years of history, so it covers the 13 formations "
             f"from June 2013. Benchmarks over the same months: equal-weighted study universe "
             f"{p(b['UNIV_EW_ann'])} a year, IWM {p(b['IWM_ann'])}, SPY {p(b['SPY_ann'])}.")
    L.append("")
    L.append("In one line each: " + " ".join(
        f"**{title.split('.')[0]}** {ONE_LINE[key](r[key])}" for key, title, *_ in TESTS))
    L.append("")
    L.append(SURV_INTRO(r))
    L.append("")
    for key, title, q, top, bot in TESTS:
        L.append(section(r[key], key, title, q, top, bot, TAKEAWAY[key](r)))
        L.append(quintile_table(r[key], key))
        L.append("")
    L.append(CAVEATS(r))
    return "\n".join(L) + "\n"


def SURV_INTRO(r):
    u = r["universe"]
    py = u["per_year"]
    ys = sorted(py, key=int)
    rows = ["| Formation (June) | Universe (priced, >= $50M) | Missing: passes filters, no price | Missing share | Missing with float >= $50M | Not yet listed (Yahoo history starts later; excluded) |",
            "|---|---|---|---|---|---|"]
    for y in ys:
        d = py[y]
        rows.append(f"| {y} | {d['universe']:,} | {d['missing']:,} | {p(d['missing_share'], 0)} | "
                    f"{d['missing_float_ge_50m']:,} ({p(d['missing_share_float50'], 0)}) | {d['not_yet_listed_excluded']:,} |")
    return ("## Read this first: the missing-company problem\n\n"
            f"The universe is built from every company that filed with the SEC at the time, including ones that "
            f"later disappeared. Yahoo only has prices for symbols that still trade, so companies that were "
            f"later acquired or delisted usually have no price and cannot be held. Across all years, "
            f"{u['firm_years_missing']:,} firm-years pass the fundamental filters but have no price, against "
            f"{u['firm_years_universe']:,} that can be held: {p(u['missing_share_overall'])} of the would-be "
            f"universe is missing ({p(u['missing_share_overall_float50'])} counting only companies whose last "
            f"reported public float was at least $50M, a stand-in for the size filter we cannot apply without a "
            f"price). The problem is worst in the early years, when the most companies have since vanished:\n\n"
            + "\n".join(rows) +
            "\n\n" + (
            f"One symptom: the priced universe itself returned {p(r['benchmarks']['UNIV_EW_ann'])} a year "
            f"equal-weighted against {p(r['benchmarks']['IWM_ann'])} for IWM, which holds the losers too. If "
            f"every missing company is assumed to have lost 30% in its year, the universe return drops to "
            f"{p(r['benchmarks']['UNIV_EW_ann_b_minus30_all_missing'])} "
            f"({p(r['benchmarks']['UNIV_EW_ann_b_minus30_float50_missing'])} counting only float >= $50M); at +15% "
            f"it is {p(r['benchmarks']['UNIV_EW_ann_c_plus15_all_missing'])}. So absolute returns in this study "
            f"flatter reality; the tests below compare groups against each other, which is what can survive "
            f"this, provided the missing companies are spread evenly across groups. They are not quite: in every "
            f"quintile sort the two extreme fifths lose more companies than the middle ones, because unusual "
            f"companies are the ones that get acquired or fail. ") +
            "Each test below reports the missing share at the top and the bottom of the sort, and re-runs the "
            "headline spread assuming every missing company lost 30% in its year (a typical delisting for poor "
            "performance) or gained 15% (a typical takeover premium).")


def CAVEATS(r):
    u = r["universe"]
    rc = r.get("restatement_check")
    b = r.get("build", {})
    lag = u["months_fye_to_formation"]
    L = ["## Caveats", ""]
    L.append(f"- **Coverage.** The universe holds {u['n_min']:,} to {u['n_max']:,} companies a year "
             f"(median {u['n_median']:,.0f}); {u['distinct_firms_universe']:,} distinct companies in all. "
             f"{p(u['universe_opinc_coverage'])} of universe firm-years report an operating-income line "
             f"(us-gaap OperatingIncomeLoss); the rest cannot be sorted and sit only in the universe benchmark. "
             f"XBRL tagging only became mandatory for smaller companies in mid-2011, so the June 2011 formation "
             f"(fiscal 2010 data) under-represents small companies, and fixed-cost share needs four years of "
             f"history, so H2 starts with the June 2013 formation.")
    L.append(f"- **Missing companies.** See the table at the top. Missing firms are placed into quintiles using "
             f"their own fundamentals and the breakpoints of the priced firms. Value-weighted results exclude them "
             f"in every scenario (no market cap).")
    L.append(f"- **Frames alignment and look-ahead.** The SEC frames API files each fiscal year under the calendar "
             f"year it overlaps most, so \"CY2015\" includes fiscal years ending as late as June 2016. Firm-years "
             f"whose fiscal year ended after the last day of February of the formation year are dropped (a "
             f"10-K may not be filed by the end of June otherwise). For the firms used, the gap from fiscal "
             f"year-end to formation is at least {lag['min']:.0f} months (median {lag['median']:.0f}): about six "
             f"months for December year-ends, which are most firms, but only four to five for January and "
             f"February year-ends (mostly retailers), so \"at least six months\" is not true of every firm.")
    rs = (f" A spot check of {rc['n_rev_compared']} random firm-years against each company's first-filed 10-K "
          f"found revenue differing by more than 1% in {p(rc['rev_share_differs_gt_1pct'])} of cases (median "
          f"difference {p(rc['rev_median_abs_diff'], 2)}) and operating income differing by more than 1% of "
          f"revenue in {p(rc['oi_share_differs_gt_1pct_of_rev'])}. In the same sample "
          f"{p(rc['share_first_10k_filed_before_formation'])} of the revenue figures had been filed in a 10-K "
          f"before the formation date; the rest first appear in a later 10-K (late filers, or a company's first "
          f"tagged 10-K after a listing).") if rc else ""
    L.append(f"- **Restated numbers.** Frames returns the value from the most recent filing that reported a "
             f"period, so {p(u['share_rev_value_from_filing_after_formation_year'])} of the revenue figures used "
             f"come from a filing made after the formation year (usually the comparative column of a later "
             f"10-K). Where a later filing restated or reclassified the number, the study uses information that "
             f"was not available on the formation date." + rs)
    L.append("- **Industry codes** are each company's current SIC code, not the code at the time.")
    L.append(f"- **Market caps** use SEC share counts times Yahoo's June close, put on the same split basis with "
             f"Yahoo's split history ({b.get('split_records_used', 0):,} split records, including Yahoo's spin-off "
             f"adjustments); us-gaap share counts, which later filings restate for splits, are put on the basis of "
             f"the filing that supplied them ({b.get('filing_date_lookups_for_restated_share_counts', 0):,} filing "
             f"dates looked up). A share count is used only if it agrees within 3x with another source (when two "
             f"agree) and implies a market cap between 0.2% and 100x the larger of revenue and assets, which catches "
             f"1,000x tagging errors. Residual errors remain for a few dozen firm-years (for example BeOne Medicines, "
             f"whose SEC count is ordinary shares while Yahoo prices the ADS, and a few post-bankruptcy share "
             f"cancellations); {p(u['float_to_mcap_ratio']['share_lt_0_1'])} of universe firm-years have a reported "
             f"public float below 10% of the computed market cap, some because the float is mis-tagged. These errors "
             f"only touch the $50M filter, the $2B size split and value weights, not equal-weighted returns. "
             f"Foreign private issuers (20-F/40-F filers, {b.get('foreign_filers', 'n/a')} registrants) are excluded "
             f"because their share counts and ADS prices are on different bases.")
    pe = r["meta"]["price_error_rule"]
    L.append(f"- **Price errors.** Yahoo monthly data for small stocks contain bad prints. "
             f"{pe['v_reversals_removed']} one-month 10x round trips and {pe['returns_above_1000pct_removed']} "
             f"monthly returns above +1,000% were set to missing across all symbols, fixed before any portfolio "
             f"was computed. Only {len(r['meta']['held_stock_months_changed_by_rule'])} of these stock-months fell "
             f"in stocks the study actually held: Chord Energy's November 2020 +30,991% (a bankruptcy splice: "
             f"Oasis Petroleum's old shares were cancelled, so the jump never happened to a holder), Phunware's "
             f"January-February 2019 round trip, Healthier Choices' 2023 round trip, and two genuine spikes that "
             f"the rule also drops, GameStop's +1,625% in January 2021 and Urban One's +1,446% in June 2020. Each "
             f"test reports the spread on raw returns too. Where the raw number has the opposite sign (H1, H2b), "
             f"the Chord Energy month is the cause: it sits in the comparison group, and with only that month "
             f"removed the raw spreads have the same sign as the cleaned ones.")
    L.append("- **Costs.** Only the top-group comparison deducts costs (0.5% a year). Small-cap spreads would "
             "shrink further after real bid-ask costs.")
    L.append("- **Several tests at once.** Four pre-registered hypotheses, each cut several ways. With that many "
             "looks, one t-statistic near 2 is weak evidence on its own; the verdict rule asks for consistency "
             "across halves, industries and delisting assumptions for that reason.")
    L.append("")
    L.append("## Files")
    L.append("")
    L.append("- `research/oplev/build_panel.py` data build (SEC frames, submissions, filing indexes, Yahoo), cached in `research/oplev/cache/`")
    L.append("- `research/oplev/run_tests.py` the pre-registered tests; `md_writer.py` renders this file")
    L.append("- `research/oplev/check_restatements.py` restatement spot check")
    L.append("- `research/oplev/panel.parquet` firm-year panel")
    L.append("- `research/oplev/results.json` every number; `research/oplev/quintile_returns.csv` monthly returns per quintile and cell, plus IWM and SPY")
    return "\n".join(L)
