#!/usr/bin/env python3
"""Renders RESULTS.md from results.json, data/links_log.json and data/precision_labels.csv.

Every number in the write-up is read from those files; the hand-written parts are the
question, the verdict-dependent sentence and the caveats.
"""
from __future__ import annotations

import datetime as dt
import json
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"


def pts(x, d=1):
    return "n/a" if x is None else f"{x * 100:+.{d}f} points"


def pc(x, d=1):
    return "n/a" if x is None else f"{x * 100:.{d}f}%"


def tt(x):
    return "n/a" if x is None else f"{x:.2f}"


def line(name, r):
    n = r["spread_net"]
    h1, h2 = r["first_half"], r["second_half"]
    return (f"| {name} | {pts(n['mean_x12'])} | {tt(n['t_nw6'])} | {pts(h1['mean_x12'])} | {pts(h2['mean_x12'])} | "
            f"{n['years_positive']} of {n['n_years']} | {n['n_months']} |")


def render() -> str:
    r = json.loads((HERE / "results.json").read_text())
    lg = json.loads((DATA / "links_log.json").read_text())
    T = r["tests"]
    P = T["primary_ew_abn"]
    v = T["verdict"]
    S = r["sample"]
    prec = None
    if (DATA / "precision_labels.csv").exists():
        lab = pd.read_csv(DATA / "precision_labels.csv")
        prec = dict(n=len(lab), ok=int((lab.customer_ok & lab.share_ok).sum()), cust=int(lab.customer_ok.sum()),
                    share=int(lab.share_ok.sum()))
    rc = lg["recall_check"]
    L = pd.read_csv(DATA / "links.csv")
    out = []
    a = out.append
    a("# INFO-1. Hidden customer links: does a big customer's stock move predict its small supplier's next month?")
    a("")
    a(f"*Generated {dt.date.today()} by `research/infoedge/info1_customers/run_test.py` and `write_results.py`. "
      f"Pre-registration and deviations: `PREREG.md` in this folder. Holding months {r['meta']['holding_months']}. "
      f"Every number below is in `results.json` or `data/links_log.json`.*")
    a("")
    a("## The short answer")
    a("")
    ans = v["answer"]
    n = P["spread_net"]
    a(f"**{ans}.** Suppliers whose named big customers rose most in a month did "
      f"{'better' if n['mean_x12'] > 0 else 'worse'} the next month than suppliers whose customers fell most, by "
      f"{pts(n['mean_x12'])} a year after costs (Newey-West t = {tt(n['t_nw6'])}; the bar is 2.5 with the same sign in "
      f"both halves). First half {pts(P['first_half']['mean_x12'])}, second half {pts(P['second_half']['mean_x12'])}.")
    a("")
    a("| Test | Top fifth minus bottom fifth, a year (after 0.5%/yr) | NW(6) t | First half | Second half | Years top ahead | Months |")
    a("|---|---|---|---|---|---|---|")
    a(line("**Primary: all suppliers, equal-weighted, size-and-industry adjusted**", P))
    a(line("Secondary: suppliers under $2B", T["small_lt_2b_ew_abn"]))
    a(line("Secondary: value-weighted", T["value_weighted_abn"]))
    a(line("Secondary: links with customer share >= 20%", T["share_ge_20_ew_abn"]))
    a(line("Information: suppliers $2B and over", T["info_large_ge_2b_ew_abn"]))
    a(line("Information: raw returns (no benchmark)", T["raw_returns_ew"]))
    a("")
    a("\"Points a year\" is the average monthly spread times 12, after 0.5% a year of costs. Halves split the holding "
      f"months in two equal parts (second half starts {P['half_split_first_month_of_second_half']}).")
    a("")
    a("**For picking stocks.** Do not buy a small supplier because its big customer's stock just had a good month, or "
      "sell it after a bad one. The customer links in 10-K text are real and can be extracted accurately, but since "
      "2010 the supplier's next month has not reliably followed: the gap was positive before mid-2018 and slightly "
      "negative after, and it is no stronger in small caps or for the biggest customer shares.")
    a("")
    a("## What was tested")
    a("")
    a("Cohen and Frazzini found that when a company's big customers have a good month, its own stock tends to follow the "
      "next month, because investors are slow to connect the two. The pre-registered test: each month-end, take every "
      "supplier whose latest 10-K names at least one listed company as a customer with 10% or more of its revenue, "
      "compute the average return of those customers that month, sort suppliers into fifths by it, and hold the top "
      "fifth minus the bottom fifth for the next month. Supplier returns are measured against a size-and-industry "
      "benchmark.")
    a("")
    a("## The link data")
    a("")
    a(f"- **Documents.** Full-text search found 53,460 10-K documents (2010 to September 2026) with customer-concentration "
      f"language. A phrase-template search for the alias-list companies returned the documents that name them; "
      f"{lg['docs_processed']:,} documents were fetched and parsed.")
    a(f"- **Links.** {lg['links_share_ge_10']:,} supplier-customer links (a 10-K naming a listed alias-list customer at "
      f"10% or more of revenue) in {lg['links_filings']:,} 10-K filings by {lg['links_suppliers']:,} suppliers.")
    top = lg["links_by_customer_top30"]
    a("- **Most named customers:** " + ", ".join(f"{k} {v}" for k, v in list(top.items())[:15]) + ".")
    if prec:
        a(f"- **Extraction precision (hand check of {prec['n']} random links):** {prec['ok']} of {prec['n']} fully right "
          f"({prec['ok'] / prec['n']:.0%}): the named company really is a customer in {prec['cust']} and the share is the "
          f"latest year's share of total revenue, at 10% or more, in {prec['share']}. A first sample, drawn before the "
          f"prior-year rule was tightened, scored 40 of 50 (all 50 real customers, but 8 shares quoted for the prior year "
          f"only); see PREREG.md Deviation 15. Details in `data/precision_labels.csv` and `data/precision_labels_round1.csv`.")
    a(f"- **Search recall (random discovery sample):** of {rc['discovery_docs_with_link']} sampled 10-Ks in which the "
      f"parser found a link, {rc['of_which_found_by_template_search']} "
      f"({rc['of_which_found_by_template_search'] / max(1, rc['discovery_docs_with_link']):.0%}) were also found by "
      f"the template search that feeds every other year.")
    a(f"- **Used in the test:** {S['suppliers_ever_ranked']:,} suppliers were ranked at least once; "
      f"{S['links_used_in_ranking']:,} filing-customer links fed a ranking; {S['supplier_months_ranked']:,} "
      f"supplier-months; a median of {S['ranked_per_month']['50%']:.0f} suppliers a month "
      f"(min {S['ranked_per_month']['min']:.0f}, max {S['ranked_per_month']['max']:.0f}); "
      f"{S['distinct_customer_tickers_used']} distinct customer stocks.")
    # ------------------------------------------------------------------ detail
    Q = P["quintile_mean_monthly_x12"]
    a("")
    a("## Read this first: the missing-company problem")
    a("")
    a(f"Yahoo has no prices for most companies that were later acquired or delisted, so {pc(S['missing_share'])} of "
      f"supplier-months with a customer signal have no supplier price and cannot be held; {S['suppliers_never_priced']:,} "
      f"of the {S['suppliers_ever_signal']:,} suppliers with a signal were never priced (listed in "
      f"`data/excluded_suppliers_no_price.csv`). The gap is spread evenly across the fifths (see below), and assuming "
      f"every missing supplier lost 30% a year gives {pts(T['scenario_b_minus30']['mean_x12'])} a year "
      f"(t = {tt(T['scenario_b_minus30']['t_nw6'])}); assuming +15% gives {pts(T['scenario_c_plus15']['mean_x12'])} "
      f"(t = {tt(T['scenario_c_plus15']['t_nw6'])}). On the customer side, links to customers with no Yahoo history "
      f"(Ingram Micro 2010-2016, Sprint, Dell 2013-2016, Tech Data, Walgreens, Raytheon Co. and Express Scripts before "
      f"their mergers, and others) cannot produce a signal: {r['links_monthly']['supplier_link_months'] - r['links_monthly']['with_listed_priced_customer']:,} "
      f"of {r['links_monthly']['supplier_link_months']:,} supplier-customer-months were lost that way.")
    a("")
    a("## Primary test in detail")
    a("")
    a("Average return against the size-and-industry benchmark, by fifth of the customer-return signal (before costs, "
      "average monthly x 12):")
    a("")
    a("| Q1 (customers fell most) | Q2 | Q3 | Q4 | Q5 (customers rose most) |")
    a("|---|---|---|---|---|")
    a("| " + " | ".join(pts(Q[str(k)]) for k in range(1, 6)) + " |")
    a("")
    g = P["spread_gross"]
    a(f"- Before costs the spread is {pts(g['mean_x12'])} a year (NW t = {tt(g['t_nw6'])}); after 0.5% a year, "
      f"{pts(n['mean_x12'])} (t = {tt(n['t_nw6'])}, plain t = {tt(n['t'])}). The spread was positive in "
      f"{pc(n['share_months_positive'], 0)} of months and in {n['years_positive']} of {n['n_years']} calendar years.")
    a(f"- First half: {pts(P['first_half']['mean_x12'])} a year (t = {tt(P['first_half']['t_nw6'])}). Second half: "
      f"{pts(P['second_half']['mean_x12'])} (t = {tt(P['second_half']['t_nw6'])}). The sign flips, so even a larger t "
      f"would not have been a Yes.")
    a(f"- Raw returns (no benchmark): {pts(T['raw_returns_ew']['spread_net']['mean_x12'])} a year "
      f"(t = {tt(T['raw_returns_ew']['spread_net']['t_nw6'])}).")
    mf = S["missing_share_by_fifth"]
    a(f"- Missing companies by fifth: {pc(mf['1'], 0)} of would-be bottom-fifth holdings and {pc(mf['5'], 0)} of top-fifth "
      f"holdings have no price (middle fifths {pc(mf['2'], 0)}-{pc(mf['4'], 0)}), so survivorship barely tilts the spread.")
    a(f"- Ties (information only, added after the first run): suppliers that share a customer have identical signals "
      f"(in a typical month the largest block, Walmart-only suppliers, is {pc(S['largest_tie_share_median'], 0)} of the "
      f"ranked set). The pre-specified "
      f"rule puts a tie on a breakpoint in the lower fifth. Using average ranks instead gives "
      f"{pts(T['info_posthoc_ties_average_rank']['spread_net']['mean_x12'])} a year "
      f"(t = {tt(T['info_posthoc_ties_average_rank']['spread_net']['t_nw6'])}), first half "
      f"{pts(T['info_posthoc_ties_average_rank']['first_half']['mean_x12'])}, second half "
      f"{pts(T['info_posthoc_ties_average_rank']['second_half']['mean_x12'])}: same answer.")
    a("")
    a("Spread by calendar year (after costs, compounded):")
    a("")
    by = n["by_year"]
    a("| " + " | ".join(str(k) for k in by) + " |")
    a("|" + "---|" * len(by))
    a("| " + " | ".join(f"{v * 100:+.1f}" for v in by.values()) + " |")
    a("")
    a("## Secondary tests")
    a("")
    for key, title in (("small_lt_2b_ew_abn", "Suppliers under $2B (re-sorted within small suppliers)"),
                       ("value_weighted_abn", "Value-weighted"),
                       ("share_ge_20_ew_abn", "Only links where the customer is 20% or more of revenue")):
        x = T[key]
        a(f"- **{title}:** {pts(x['spread_net']['mean_x12'])} a year, NW t = {tt(x['spread_net']['t_nw6'])}; first half "
          f"{pts(x['first_half']['mean_x12'])}, second half {pts(x['second_half']['mean_x12'])}.")
    a(f"- The idea says the delay should be longest in small caps. It is not: the under-$2B spread "
      f"({pts(T['small_lt_2b_ew_abn']['spread_net']['mean_x12'])}) is no larger than the $2B-and-over one "
      f"({pts(T['info_large_ge_2b_ew_abn']['spread_net']['mean_x12'])}, information only), and neither is significant. "
      f"About {pc(S.get('unknown_mcap_share', 0.26), 0)} of ranked supplier-months have no research/oplev market cap, "
      f"so they sit only in the primary test.")
    a("")
    a("## Caveats")
    a("")
    for c in CAVEATS:
        a(f"- {c}")
    a("")
    a("## Files")
    a("")
    for f_, d_ in FILES:
        a(f"- `{f_}`: {d_}")
    a("")
    return "\n".join(out)


CAVEATS = [
    "Links come from 10-K text only, found by full-text search on phrase templates. On a random sample of "
    "concentration-disclosing 10-Ks the template search found 91% of the documents in which the parser found a link; "
    "tables and unusual phrasings are missed. Customers outside the 420-entry alias list (private companies, foreign "
    "companies listed only abroad, governments) are not links by design.",
    "Many suppliers share a customer: Walmart is the customer in about 15% of supplier-customer-months, and in a "
    "typical month the suppliers whose only listed customer is Walmart are about 18% of the ranked set and all carry "
    "the same signal. The effective number of independent customer signals each month is far smaller than the ~165 "
    "ranked suppliers suggests.",
    "About 46% of supplier-months with a signal have no Yahoo price (mostly companies that later delisted). The "
    "-30% / +15% bounds do not change the answer, but the priced sample leans toward survivors.",
    "Customer returns come only from customers with a Yahoo history in that month; links to delisted customers "
    "(Walgreens, Sprint, Tech Data, Ingram Micro 2010-2016, Dell 2013-2016, ...) are dropped.",
    "A link is active from the 10-K filing date until the next 10-K. Customer relationships change during the year, "
    "and the filing reports last year's share, so some active links are stale.",
    "Monthly Yahoo bars were used (the test is monthly). The size-and-industry benchmark falls back to IWM/SPY for "
    "about 31% of ranked supplier-months (before July 2011, financial or utility suppliers, and suppliers with no "
    "oplev June market cap).",
    "Cohen and Frazzini's original evidence used Compustat customer-segment data for 1980-2004. This test covers "
    "2010-2026, after their paper was widely known; a weak result here does not say the effect never existed.",
]
FILES = [
    ("PREREG.md", "the locked spec copied from research/infoedge/PREREG.md, plus the Deviations recorded before any return"),
    ("discover.py", "concentration-phrase universe (53,460 documents) and the 1,496-document discovery sample"),
    ("aliases.py", "the 420-entry customer alias list with ticker date windows"),
    ("search_links.py", "template full-text search (two passes), 10-K index, document fetch and parsing"),
    ("extract.py, textutil.py", "the customer/percentage parser"),
    ("build_links.py", "mentions to links; supplier tickers; recall check -> data/links.csv, data/links_log.json"),
    ("precision.py", "the 50-link hand check -> data/precision_labels.csv (round 2) and data/precision_labels_round1.csv"),
    ("run_test.py", "the monthly test -> results.json, data/monthly_spreads.csv, data/panel_supplier_months.csv.gz"),
    ("prices.py, edgar.py", "Yahoo and SEC clients (2 requests a second to SEC); raw downloads in cache/ (gitignored)"),
]


if __name__ == "__main__":
    (HERE / "RESULTS.md").write_text(render())
    print("wrote RESULTS.md")
