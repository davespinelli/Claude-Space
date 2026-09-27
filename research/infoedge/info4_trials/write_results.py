"""Write RESULTS.md from results.json and the data files (plain-English answer first)."""
import json
from datetime import date
from pathlib import Path
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent


def pct(x, d=2):
    return "n/a" if x is None or (isinstance(x, float) and np.isnan(x)) else f"{100 * x:+.{d}f}%"


def tt(x):
    return "n/a" if x is None or (isinstance(x, float) and np.isnan(x)) else f"{x:.2f}"


def row(label, s):
    if not s or s.get("n", 0) == 0:
        return f"| {label} | no events | | | | |"
    return (f"| {label} | {pct(s['mean'])} | {tt(s['t_clustered'])} | {pct(s['half1']['mean'])} | "
            f"{pct(s['half2']['mean'])} | {s['n']:,} |")


def main():
    r = json.load(open(HERE / "results.json"))
    feas = json.load(open(HERE / "data/feasibility.json"))
    E = pd.read_csv(HERE / "data/event_returns.csv")
    C = pd.read_csv(HERE / "data/changes_mapped.csv")
    Ct = pd.read_csv(HERE / "data/trial_changes.csv")
    lag = pd.read_csv(HERE / "data/post_lag.csv")
    lag = lag[lag.last_update_post >= "2015-01-01"]
    spot = pd.read_csv(HERE / "data/mapping_spotcheck.csv")
    comp = pd.read_csv(HERE / "data/sponsor_companies_priced.csv")
    excl_hist = pd.read_csv(HERE / "data/history_exclusions.csv") if (HERE / "data/history_exclusions.csv").exists() else pd.DataFrame()
    U = pd.read_csv(HERE / "data/trials_universe.csv")
    done = {p.name[:-8] for p in (HERE / "cache/hist_list").glob("*.json.gz")}
    U["done"] = U.nct.isin(done)

    # the download screen was applied before the ticker fix re-wrote sponsor_companies_priced.csv
    n_pass = int(comp.size_pass.sum()) if "size_pass" in comp else int(pd.read_csv(HERE / "cache/spc_before.csv").size_pass.sum())
    p = r["primary"]; pl = r["placebo"]; mi = r["missing"]
    d_pl = pl["event_minus_placebo_ar"]; d_etf = pl["event_minus_placebo_ar_iwmspy"]
    etf = r["robust_iwm_spy_benchmark"]; xbi = r["robust_xbi_benchmark"]
    s23 = r["secondary_phase23"]; s1b = r["secondary_under_1b"]
    P = E[(~E.k8) & (E.status == "priced") & (E.mcap < 5e9)]

    def verdict_of(s):
        return "Yes" if (s.get("n", 0) and s["t_clustered"] <= -2.5 and s["half1"]["mean"] < 0 and s["half2"]["mean"] < 0) else "No"

    L = []
    L.append("# INFO-4. Quiet clinical-trial registry changes: results\n")
    L.append(f"*Generated {date.today().isoformat()} by `research/infoedge/info4_trials/write_results.py`. "
             "Pre-registration, feasibility notes and every deviation: `PREREG.md` in this folder (see the process note at the end about a pilot run). "
             "Every number below is in `results.json`.*\n")

    L.append("## The short answer\n")
    L.append("**Feasible: yes.** ClinicalTrials.gov keeps a dated copy of every version of every record, and it can be downloaded "
             f"without an account. {U.done.sum():,} trial histories were pulled (all but {int((~U.done & U.priced_sponsor).sum())} of the "
             f"{int(U.priced_sponsor.sum()):,} trials whose sponsor has stock prices).\n")
    L.append(f"**Primary test: {p['verdict']}.** "
             + (f"After a quiet registry change (completion date pushed back 6+ months, enrollment target cut 25%+, or trial suspended/terminated/withdrawn, "
                f"with no 8-K), the sponsor's stock did {pct(p['mean'])} versus similar-size health-care peers over the next 20 trading days "
                f"(t = {tt(p['t_clustered'])}; first half {pct(p['half1']['mean'])}, second half {pct(p['half2']['mean'])}; {p['n']:,} events). ")
             + ("That clears the bar (t <= -2.5, negative in both halves). " if p["verdict"] == "Yes" else "That does not clear the bar (t <= -2.5 and negative in both halves). ")
             + f"The same companies on random dates in the same year did {pct(pl['placebo_mean_ar']['mean'])} against the same benchmark, "
             f"so the event-minus-placebo difference is {pct(d_pl['mean'])} (t = {tt(d_pl['t_clustered'])}). "
             f"Against IWM/SPY alone the events did {pct(etf['mean'])} (t = {tt(etf['t_clustered'])}).\n")

    kills = []
    if p["verdict"] == "Yes":
        if not (d_pl.get("n", 0) and d_pl["t_clustered"] <= -2.5): kills.append("the placebo comparison")
        if not (etf.get("n", 0) and etf["t_clustered"] <= -2.5): kills.append("the IWM/SPY-only benchmark")
        if kills:
            L.append(f"**Warning: the headline passes but does not survive {' and '.join(kills)}.** Treat it as No for trading.\n")

    L.append("| Line (days +1 to +20 after the posting date) | Mean | Clustered t | First half | Second half | Events |")
    L.append("|---|---|---|---|---|---|")
    L.append(row("**Primary**: quiet changes, sponsor under $5B, vs size-and-industry peers", p))
    L.append(row("Event minus placebo (same stocks, random dates, same benchmark)", d_pl))
    L.append(row("Placebo alone (same stocks, random dates)", pl["placebo_mean_ar"]))
    L.append(row("vs IWM (under $2B) / SPY only", etf))
    L.append(row("Event minus placebo, both vs IWM/SPY", d_etf))
    L.append(row("vs XBI only", xbi))
    L.append(row("Secondary: Phase 2/3 trials only", s23))
    L.append(row("Secondary: sponsor under $1B", s1b))
    L.append("")
    L.append(f"Missing companies (listed at the time, no Yahoo price today): about {mi['n_missing_events_scaled']:.0f} quiet events "
             f"({100 * mi['share_of_would_be_sample']:.0f}% of the would-be sample). If every one of them lost 30%: "
             f"{pct(mi['minus30']['mean'])} (t = {tt(mi['minus30']['t_clustered'])}); if every one gained 15%: "
             f"{pct(mi['plus15']['mean'])} (t = {tt(mi['plus15']['t_clustered'])}).\n")
    L.append(f"Costs: shorting after each event would earn {pct(p['mean_after_cost_short'])} per event after 0.2% costs "
             "(before borrow fees, which for small biotechs are often far larger).\n")

    # ---------------------------------------------------------------- feasibility
    L.append("## Feasibility: can the registry history be pulled?\n")
    L.append("- The public ClinicalTrials.gov API (v2) serves only the current version of each record; it has no history endpoint.")
    L.append("- The website's \"History of Changes\" tab reads two internal endpoints: one lists every version of a trial (number, date, overall status, which sections changed); the other returns the whole record as it stood at any version, including the date that version was **posted**. robots.txt explicitly allows crawlers on these endpoints.")
    L.append(f"- A request with no cookies gets \"403 Forbidden\" ({feas['ok_counts']['int_history_list_no_cookie']} of {feas['trials_probed']} succeeded in the logged check). "
             "Any public ClinicalTrials.gov response (for example the v2 API) sets the site's ordinary `ncbi_sid` session cookie, and with it the endpoints answer normally "
             f"({feas['ok_counts']['int_history_list']} of {feas['trials_probed']}). The scripts keep cookies like any HTTP client, send the project User-Agent, and never impersonate a browser or solve a challenge.")
    L.append("- AACT (the Duke/FDA copy) needs an account for both database access and downloads, and holds snapshots rather than version histories. No account was created.")
    L.append("- Cost: about 11 requests per trial at up to 2.9 a second, roughly 12 hours for the whole set, with two network outages along the way.\n")

    # ---------------------------------------------------------------- data
    L.append("## What was measured\n")
    L.append("1. Every industry-sponsored interventional trial updated since 2015: 91,130 current records (v2 API).")
    L.append(f"2. Lead-sponsor names mapped to SEC registrants (current and since-delisted names from EDGAR indices): {len(comp):,} companies kept; "
             f"{n_pass:,} passed the loose under-$5B download screen; {int(comp.ticker.notna().sum()):,} have Yahoo prices.")
    L.append(f"3. Histories for {len(U):,} trials of those companies: all {int(U.priced_sponsor.sum()):,} trials of priced sponsors were attempted "
             f"({int((U.priced_sponsor & U.done).sum()):,} downloaded, {len(excl_hist.nct.unique()) if len(excl_hist) else 0} still failing after one retry and excluded; list in `data/history_exclusions.csv`), "
             f"and a random {100 * mi['unpriced_trials_fraction_downloaded']:.0f}% of the {int((~U.priced_sponsor).sum()):,} trials of sponsors with no price today (used only for the missing-company bounds, scaled up).")
    L.append("4. Changes between consecutive versions; public date = the version's posting date; one event per company per posting date; "
             "an event is quiet if no 8-K (6-K for foreign issuers) was filed from 5 trading days before the version date through the posting date.")
    L.append("5. Abnormal return = buy-and-hold return over trading days +1 to +20 minus the average buy-and-hold return of other sponsor companies in the same industry group and size band.\n")

    # counts
    L.append("### Event counts\n")
    tc = Ct.type.value_counts()
    cm = C.type.value_counts()
    L.append("| | Delay 6+ months | Enrollment cut 25%+ | Suspended / terminated / withdrawn | Total |")
    L.append("|---|---|---|---|---|")
    L.append(f"| Trial-level changes posted 2015 to Aug 2026 | {tc.get('delay', 0):,} | {tc.get('cut', 0):,} | {tc.get('status', 0):,} | {len(Ct):,} |")
    L.append(f"| ... attributed to a listed sponsor at the time | {cm.get('delay', 0):,} | {cm.get('cut', 0):,} | {cm.get('status', 0):,} | {len(C):,} |")
    def evc(df):
        return [int(df.types.str.contains(t).sum()) for t in ("delay", "cut", "status")] + [len(df)]
    a = evc(E); b = evc(E[E.k8]); q = evc(E[(~E.k8) & (E.status == "priced")]); pp = evc(P)
    L.append(f"| Company-date events | {a[0]:,} | {a[1]:,} | {a[2]:,} | {a[3]:,} |")
    L.append(f"| ... with an 8-K/6-K in the window (dropped) | {b[0]:,} | {b[1]:,} | {b[2]:,} | {b[3]:,} |")
    L.append(f"| ... quiet and priced | {q[0]:,} | {q[1]:,} | {q[2]:,} | {q[3]:,} |")
    L.append(f"| ... quiet, priced, under $5B (**primary sample**) | {pp[0]:,} | {pp[1]:,} | {pp[2]:,} | {pp[3]:,} |")
    L.append("\nAn event can carry more than one type, so the type columns can add up to more than the total.\n")
    st = r["counts"]["status"]
    L.append(f"Company-date events by price status: priced {st.get('priced', 0):,}; missing (listed, no Yahoo price) {st.get('missing', 0):,}; "
             f"not listed at the time {st.get('not_listed', 0):,}; too recent {st.get('too_recent', 0):,}.\n")
    L.append("By type (primary sample):\n")
    L.append("| Type | Mean | Clustered t | First half | Second half | Events |")
    L.append("|---|---|---|---|---|---|")
    for k, lab in (("delay", "Completion date pushed back 6+ months"), ("cut", "Enrollment target cut 25%+"),
                   ("status", "Suspended / terminated / withdrawn"), ("status_terminated_etc_only", "Status change only (no other change that day)")):
        L.append(row(lab, r["by_type"][k]))
    L.append("")

    # posting lag
    L.append("### Posting lag\n")
    L.append(f"The date shown in the history is the submission/QC date; the version is posted later: median {lag.lag_days.median():.0f} days, "
             f"90th percentile {lag.lag_days.quantile(.9):.0f}, 95th {lag.lag_days.quantile(.95):.0f} ({len(lag):,} versions posted since 2015). "
             "All events are dated at the posting date, so a model that dated them at the history date would be using information before it was public.\n")

    # mapping precision
    L.append("## Mapping precision\n")
    L.append(f"- 50 randomly drawn sponsor-to-SEC matches were checked by hand (`data/mapping_spotcheck.csv`): {int((spot.correct == 'yes').sum())} of 50 correct "
             "(same company or its subsidiary, including renamed registrants). Matching rules: exact normalised name; looser \"core\" name and single-dictionary-word names only with a health-care SIC code.")
    if (HERE / "data/event_spotcheck.csv").exists():
        es_ = pd.read_csv(HERE / "data/event_spotcheck.csv")
        if "correct" in es_:
            L.append(f"- 50 randomly drawn primary events were also checked (registry sponsor name on that version vs the stock used): "
                     f"{int((es_.correct == 'yes').sum())} of {len(es_)} correct (`data/event_spotcheck.csv`).")
    L.append("- Point in time: the sponsor is the one named in the version itself, and a change is only attributed to a stock if the registrant had used that name by 120 days after the posting date (so a private company that later reverse-merged into a listed shell is not attributed to the shell).\n")

    # robustness
    L.append("## How much to trust it\n")
    rb = [("Literal 8-K window (5 days before the version date only)", r["robust_literal_8k_window"]),
          ("Daily-rebalanced peer benchmark", r["robust_daily_rebalanced_benchmark"]),
          ("Raw return, no benchmark", r["robust_raw_return"]),
          ("Excluding foreign issuers", r["robust_ex_foreign_issuers"]),
          ("Including events with an 8-K in the window", r["robust_including_8k_events"]),
          ("Only events with an 8-K in the window", r["robust_8k_events_only"]),
          ("Event minus placebo, XBI benchmark", pl["event_minus_placebo_ar_xbi"])]
    L.append("| Robustness line | Mean | Clustered t | First half | Second half | Events |")
    L.append("|---|---|---|---|---|---|")
    for lab, s in rb: L.append(row(lab, s))
    L.append("")
    L.append("By year (primary):\n")
    L.append("| Year | Events | Mean abnormal return |")
    L.append("|---|---|---|")
    for y, v in r["by_year"].items(): L.append(f"| {y} | {v['n']} | {pct(v['mean'])} |")
    L.append("")

    # caveats
    L.append("## Caveats\n")
    L.append(f"- **Survivor-built prices and peers.** Yahoo only has symbols that still trade. About {100 * mi['share_of_would_be_sample']:.0f}% of the would-be sample belongs to companies that have since been acquired or delisted; the -30%/+15% bounds show how much that could move the answer. The peer benchmark is built from the same survivors, which is why the placebo line matters: it measures how the same stocks do on ordinary dates against that benchmark.")
    L.append(f"- **Partial download for price-less sponsors.** Only a random {100 * mi['unpriced_trials_fraction_downloaded']:.0f}% of their trials were pulled, so their count in the missing-company bounds is an estimate.")
    L.append("- **Universe chosen by today's sponsor name.** A trial whose current sponsor is a large company (for example after an acquisition) was not downloaded, even if a small listed company sponsored it earlier.")
    L.append("- **8-K screen is coarse.** Any 8-K counts as disclosure, whatever it says; a trial change announced in a press release without an 8-K, or in a 10-Q, still counts as quiet.")
    L.append("- **Short-side frictions.** The expected trade is a short in small biotechs; borrow costs and availability are not modelled beyond the 0.2% per event.")
    L.append("- **Size figures** combine XBRL share counts with Yahoo prices and a hand-checked ADS rule for foreign issuers; errors mostly affect which size band an event falls in, not the return.\n")

    L.append("## Process note (read before relying on the pre-registration)\n")
    L.append("- On 2026-09-26 at 07:45 a pipeline test ran the full event study on the partial download that existed then "
             "(155 primary events). It wrote returns to results.json, but the agent sent the output to /dev/null and read only the "
             "event and peer counts. At 07:57 PREREG deviation 10 (download order: priced sponsors first) was edited. That edit changes "
             "which trials were downloaded first, not how any event or return is defined.")
    L.append("- At 19:18, after the full download, prepare_companies.py was corrected to price each company on its main US listing "
             "rather than an OTC line where both exist (for example ResMed RMD rather than RSMDF, Abivax ABVX rather than AAVXF). "
             "ADS ratios for those 15 companies were recomputed. This is a data correction and is not in PREREG.md.")
    L.append("- Before this final run, the coordinator looked at the 07:45 pilot summary (primary +2.1%, t = 1.11, No). "
             "Nothing in PREREG.md or the return code was changed after that.")
    L.append("- The final run below uses every history downloaded, including one retry pass for failed downloads. "
             "Trials that still failed are listed in data/history_exclusions.csv.\n")
    L.append("## Files\n")
    L.append("- `PREREG.md` spec, feasibility and deviations; `results.json` every number; `data/event_returns.csv` event-level returns; `data/placebo.csv`; "
             "`data/trial_changes.csv`, `data/changes_mapped.csv`; `data/sponsor_map*.csv`, `data/mapping_spotcheck.csv`; `data/excluded_no_price.csv` (companies with no Yahoo price); "
             "`data/history_exclusions.csv` (trials whose history could not be downloaded).")
    L.append("- Pipeline: `pull_universe.py` -> `build_sec_names.py` -> `map_sponsors.py` -> `i4_subs.py`, `i4_facts.py`, `i4_px.py` -> `build_universe.py` -> `prepare_companies.py` -> `i4_ads.py` -> `size_screen.py` -> `i4_hist.py` (resumable, sharded) and `i4_retry.py` -> `detect_changes.py` -> `build_events.py` -> `run_event_study.py` -> `write_results.py`.")
    (HERE / "RESULTS.md").write_text("\n".join(L) + "\n")
    print("wrote RESULTS.md")


if __name__ == "__main__":
    main()
