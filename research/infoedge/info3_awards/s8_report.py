#!/usr/bin/env python3
"""Stage 8: write RESULTS.md from results.json and the data files."""
from __future__ import annotations

import datetime as dt
import json

import numpy as np
import pandas as pd

from common import DATA, HERE


def pct(x, k=2):
    return "n/a" if x is None or not np.isfinite(x) else f"{100 * x:+.{k}f}%"


def num(x, k=2):
    return "n/a" if x is None or not np.isfinite(x) else f"{x:.{k}f}"


def main():
    R = json.loads((HERE / "results.json").read_text(), parse_constant=lambda c: None)
    S = R["samples"]
    C = R["counts"]
    spot = json.loads((DATA / "spotcheck_summary.json").read_text()) if (DATA / "spotcheck_summary.json").exists() else {}
    dates = json.loads((DATA / "dating_summary.json").read_text()) if (DATA / "dating_summary.json").exists() else {}

    def f(x):
        return float(x) if x is not None else np.nan

    def row(label, key):
        s = S[key]
        h1, h2 = s.get("h1", {}), s.get("h2", {})
        return (f"| {label} | {s.get('verdict', '')} | {s['n']:,} ({s.get('companies', 0)} cos.) | "
                f"{pct(f(s.get('mean_car_net')))} | {num(f(s.get('t_net')))} | "
                f"{pct(f(h1.get('mean_car_net')))} (n={h1.get('n', 0)}) | {pct(f(h2.get('mean_car_net')))} (n={h2.get('n', 0)}) |")

    P = S["primary"]
    L = []
    L.append("# Do federal contract awards that nobody announced move small-cap stocks? (INFO-3)")
    L.append("")
    L.append(f"*Generated {dt.date.today()} by `research/infoedge/info3_awards/s8_report.py` from `results.json`. "
             "Pre-registration and every deviation: `PREREG.md` in this folder.*")
    L.append("")
    L.append("## The short answer")
    L.append("")
    verdict = P.get("verdict", "No")
    pl = P.get("placebo") or {}
    lead = (f"**{verdict} by the pre-registered rule, but not a usable edge.** " if verdict == "Yes" else f"**{verdict}.** ")
    L.append(lead + (
        "Awards worth at least 2% of a small listed company's market value, with no 8-K from the company around the "
        f"award, were followed by an average abnormal return of {pct(f(P.get('mean_car_net')))} over the 20 trading days "
        f"after the award became public (after 0.2% cost), t = {num(f(P.get('t_net')))} (clustered by month); "
        f"the bar was t >= 2.5 with a positive sign in both halves.") + (
        f" The required placebo check fails: the same stocks on random non-event days in the same years earned "
        f"{pct(f(pl.get('mean_placebo_car_net')))}, so the award windows beat them by only "
        f"{pct(f(pl.get('mean_event_minus_placebo')))} (t = {num(f(pl.get('t_event_minus_placebo')))}), "
        f"{pct(f(pl.get('h1_diff')))} in the first half. Buy-and-hold returns give "
        f"{pct(f(P['bhar'].get('mean_car_net')))} (t = {num(f(P['bhar'].get('t_net')))}), companies worth $50M or more show "
        f"{pct(f(S['info_mcap_ge_50m'].get('mean_car_net')))} (t = {num(f(S['info_mcap_ge_50m'].get('t_net')))}), and the "
        f"pessimistic survivorship bound flips the sign. The average comes from nano-cap stocks and a general small-stock drift, "
        f"not from the awards." if pl else ""))
    L.append("")
    L.append("| Test | Answer | Events | Mean abnormal return, days +1..+20, after 0.2% cost | t (clustered by month) | First half | Second half |")
    L.append("|---|---|---|---|---|---|---|")
    L.append(row("Primary: award >= 2% of market cap, no 8-K within 5 trading days", "primary"))
    L.append(row("Secondary: award >= 5% of market cap", "sec_5pct"))
    L.append(row("Secondary: civilian agencies only", "sec_civilian"))
    L.append("")
    L.append("Abnormal return = stock total return minus IWM total return, summed over trading days +1 to +20 after the public date. "
             f"Halves split at the median public date ({P.get('split_date')}).")
    L.append("")
    L.append("## Events")
    L.append("")
    L.append("| | Civilian | DoD | Total |")
    L.append("|---|---|---|---|")
    L.append(f"| No 8-K within 5 trading days (\"unannounced\") | {C['civ_unannounced']:,} | {C['dod_unannounced']:,} | {C['unannounced']:,} |")
    L.append(f"| 8-K within 5 trading days (\"announced\") | {C['civ_announced']:,} | {C['dod_announced']:,} | {C['announced']:,} |")
    L.append(f"| All | {C['civilian']:,} | {C['dod']:,} | {C['events_complete_window']:,} |")
    L.append("")
    L.append(f"These are priced events with a complete 20-day window, {C['companies']} companies, before the same-company "
             "overlap rule (an event within 20 trading days of the same company's previous event is dropped inside each test). "
             f"Companies with no usable Yahoo price add {C['missing_events']:,} more events at {C['missing_companies']} companies "
             "(screened on public float); they enter only the survivorship bounds below.")
    L.append("")
    if dates:
        L.append("## Read this first: how the awards are dated")
        L.append("")
        for line in dates.get("lines", []):
            L.append(f"- {line}")
        L.append("")
    if spot:
        L.append("## Mapping precision")
        L.append("")
        for line in spot.get("lines", []):
            L.append(f"- {line}")
        L.append("")
    L.append("## How much to trust it")
    L.append("")
    for key, lab in (("primary", "Primary"), ("sec_5pct", ">= 5%"), ("sec_civilian", "Civilian only")):
        s = S[key]
        L.append(f"**{lab}.** Gross mean {pct(f(s.get('mean_car')))} (t = {num(f(s.get('t_gross')))}), "
                 f"median {pct(f(s.get('median_car')))}, {100 * f(s.get('share_positive')):.0f}% of events positive; "
                 f"buy-and-hold version {pct(f(s['bhar'].get('mean_car_net')))} (t = {num(f(s['bhar'].get('t_net')))}). "
                 f"Survivorship bounds (every missing-company event, {s.get('missing_events', 0)} of them, and every "
                 f"window cut short by a delisting ({s.get('truncated_windows', 0)}), set to -30% / +15%): "
                 f"{pct(f(s['bound_minus30'].get('mean_car_net')))} (t = {num(f(s['bound_minus30'].get('t_net')))}) / "
                 f"{pct(f(s['bound_plus15'].get('mean_car_net')))} (t = {num(f(s['bound_plus15'].get('t_net')))}).")
        L.append("")
    L.append("For information only (not part of the verdict):")
    L.append("")
    L.append("| Sample | Events | Mean after cost | t |")
    L.append("|---|---|---|---|")
    for key, lab in (("info_dod", "DoD only, unannounced"), ("info_announced", "Announced (8-K within 5 trading days)"),
                     ("info_all_events", "All events regardless of 8-K"), ("info_mcap_ge_50m", "Unannounced, market cap >= $50M"),
                     ("info_10pct", "Unannounced, award >= 10% of market cap")):
        s = S[key]
        L.append(f"| {lab} | {s['n']:,} | {pct(f(s.get('mean_car_net')))} | {num(f(s.get('t_net')))} |")
    L.append("")
    extra = (HERE / "RESULTS_notes.md")
    if extra.exists():
        L.append(extra.read_text().strip())
        L.append("")
    (HERE / "RESULTS.md").write_text("\n".join(L) + "\n")
    print("\n".join(L[:20]))


if __name__ == "__main__":
    main()
