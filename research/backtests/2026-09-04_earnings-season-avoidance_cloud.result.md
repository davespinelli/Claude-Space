# Idea 23 — earnings-season-avoidance (cloud, 2026-09-04) — **KILL**

**Script:** `research/backtests/2026-09-04_earnings-season-avoidance_cloud.py`
**Artefacts:** `.console.txt`, `.premise.csv`, `.grid.csv`, `.effect.csv`, `.walkforward.csv`

## What was run

372 grid points, all reported: 2 universes (`universe.json` 56 names / 20 single stocks;
`universe_broad.json` 136 names / 100 single stocks) × 3 books (live `v1` top-5; idea 2's
standing 4b KEEP `top20`; idea 10's `ewall`) × 2 exclusion conventions (`replace` = promote the
next-ranked eligible name, gross held; `cash` = sit the blacked-out holding out, gross falls) ×
31 windows (1 no-blackout anchor + 15 season windows + 15 placebo windows).

Tuned parameters: exactly 2 — `start` ∈ {7,14,21,28,35} days after calendar quarter end and
`length` ∈ {14,21,28} days. Everything else held at the incumbent books' own settings (200d ∧
vol20<0.60 gate, 75% gross, weekly, 10 bps, next-day execution). ETFs are never blacked out.
The anchor reproduces `rules_v1_weights` **exactly** (max weight difference 0.0).

Controls: (a) a **placebo season** shifted +45 days into mid-quarter, run at the same 15
(start,length) points and never selectable by rule 8; (b) the no-blackout anchor in every cell.

## Results

**(1) The premise does not hold in the data.** Per-name SPY-excess daily return in-season vs
out, single stocks only, across all 15 windows: u56 mean difference **+0.81 bps/day**, positive
in 10/15, max |t| 2.39; broad **+0.05 bps/day**, positive in 8/15, max |t| 1.42. The placebo's
own max |t| is *larger* on both panels (3.10 and 2.16), so nothing here is distinguishable from
window-shopping noise. The one real in-season effect is **volatility**: on u56, in-season daily
vol runs 0.36–0.39 vs 0.30 out-of-season for windows starting 14–28 days after quarter end.
More risk, no more return — and avoidance still loses, because the excluded exposure is to an
asset with positive unconditional drift.

**(2) The rule loses in 179 of 180 season cells.** dSharpe against the same book with no
blackout: **mean −0.129, positive in 1/180**, dCAGR **−2.19%/yr**, dMaxDD **+0.50pp**. Even the
**best** of the 15 windows, cherry-picked per cell, loses to its own anchor in **11 of 12 cells**
(range −0.075 to −0.009); the single exception is +0.004 on `broad/v1/cash`, the weakest book in
the run. There is no window at which this idea is not a cost.

**(3) Priced as drawdown insurance it is off the bottom of idea 94's menu.** MaxDD does improve
in 99/180 season cells, at a median **2.88 pp of CAGR per pp of MaxDD** (aggregate 4.34) —
against idea 94's measured menu where the *dearest* priceable instrument was 0.91 and the static
gross lever 0.57. Anyone wanting this drawdown can buy it ~5× cheaper by holding less.

**(4) Half the damage is generic, half is specifically the season.** The placebo loses too
(dSharpe mean −0.061, positive in 34/180) — sitting out ~30% of stock-days costs money whenever
you do it. But the season window costs **twice** as much as the placebo window at the same
duty cycle, i.e. the post-quarter-end weeks are where the *return* is, which is the sign
Frazzini-Lamont predicts and the opposite of the idea's premise. Turnover also rises (15.5x →
17.9x/yr on average), so the cost is not even a trading-cost story in reverse.

**(5) Rule 8 is a clean demonstration of in-sample selection.** In-sample (2009–2016) Sharpe is
*higher* for a blackout arm than for the anchor in **10 of 12 cells** (mean IS gain +0.100), so
the walk-forward picks a season window in 10 of 12 — and OOS Sharpe then falls versus the anchor
by **−0.106 to −0.420 (mean −0.188)**, with regret ≤ 0 in all 12 cells. The grid is selectable
and selection makes it worse everywhere.

**(6) The 7 season rows that pass 4b are inherited, not caused.** All 7 sit on `u56/top20`,
whose *anchor* already passes 4b at 12.7%/1.092/−18.3% (idea 2's standing KEEP). Every one of
the 7 has a **lower** Sharpe than that anchor (0.973–1.045). No cell is converted from fail to
pass by the blackout.

**(7) The 4a pathology again:** 4a passes rise from 4/12 anchors to 47/180 season rows while 4b
passes fall relative to the anchor rate — cutting exposure clears 4a only because RULES v1 is
weak. Consistent with ideas 22, 40 and 94.

## Verdict

**KILL**, not PARK. The queue expected PARK on the grounds that the idea "needs earnings dates".
That defence is weaker than it looks: the calendar approximation covers most of the reporting
mass of most names in both panels, and the measured effect is not small-and-noisy but
**large, negative and monotone across 180 cells and two independent panels**, with a placebo
that isolates roughly half the damage as duty-cycle cost and the other half as specifically
giving up the announcement weeks. Exact dates would sharpen the window; they would not change
its sign. If someone wants to resurrect this with real dates, the pre-registered bar should be
that the *premise* test (A) clears |t| > 3 on the broad panel first — it currently reads +0.05
bps/day at t = 1.42.

Recommended RULES wording: **none**. Rules unchanged.

## Caveats

- SURVIVORSHIP: both panels are current constituents; every level above is biased upward. This
  runs *against* the idea being resurrected (survivors had fewer catastrophic announcements).
- Queue idea 38 (calendar-day index) applies: post-2014 weekends are zero-return rows. It hits
  every arm, baseline and SPY identically, so the cross-arm comparisons here are apples-to-apples;
  absolute Sharpe levels are not trustworthy until 38 lands. Applying the window on calendar days
  is what a quarterly-calendar approximation wants in any case.
- The placebo windows with `start` ∈ {28,35} are truncated at the 92-day quarter boundary, so
  their duty cycle is 13–21% rather than 15–31%; the three affected rows are identical to each
  other by construction and are reported as such.
- Off-cycle filers (fiscal years ending in Jan/Jun/Sep — e.g. AAPL Q4 in late Oct, COST, ORCL,
  NVDA) are mis-timed by this calendar. That is the approximation's known error and the reason
  the premise test is reported separately from the rule.
