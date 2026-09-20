# Idea 1799 (lane C, 2026-09-20) — does a DRIFT-THRESHOLD refresh dominate a CALENDAR refresh?

**Script:** `research/backtests/2026-09-20_drift-threshold-refresh_C.py` (gates **8/8**), outputs
`.grid.csv` (420 scored cells, every grid point), `.matched.csv`, `.choosers.csv`, `.crash.csv`,
`.gates.csv`, `.log.txt`.

**Construction.** The standing VOLTGT book (equal-weight panel scaled by
`g_t = clip(t / sigma20_panel, 0, 1)`, next-day execution, gross capped at 1.00), with the scalar
re-read on one of two triggers, same tape / same names / same trade cadence:
* **CALENDAR** — `R in {D, W, M, Q}`, the record's own axis (idea 1767's two-schedule runner);
* **DRIFT** — re-read `g` iff `|g_t - gross_held_t| > h`, `h in {0.01 ... 0.25}`, cadence-free.

`h = 0` reproduces `R = D` **exactly** (G4, 0.000e+00 at all 30 cells); the calendar diagonal
`T = R` reproduces `engine.backtest` at 0.000e+00 (G1); the standing memo's points 2–4 reproduce
at **4.605e-05** (G3) and idea 1793's OOS oracle cell at **4.875e-05** (G5). Two tuned dials and no
more, never across families: DRIFT spends `(t, h)`, CALENDAR spends `(t, R)`.

## THE HEADLINE — the trigger dominates the calendar ladder at MATCHED TURNOVER, everywhere

At its own realised turnover, interpolated onto its own arm's calendar ladder, the drift book wins
**263 of 263 cells at 10 bps** (mean **+0.0596** OOS Sharpe, **+4.07 pp** OOS MaxDD, +0.31 pp CAGR)
— and the win is not a cost-rung artefact: **1.000 / 1.000 / 0.996 / 0.992** at 0 / 10 / 25 / 50 bps.
It holds on every panel including the one where the book itself fails (U56 +0.0628, B136 +0.0647,
SMALL665 +0.0516; worst cell of 263 is **+0.0015**, i.e. the calendar ladder is never ahead).
Whole-grid 4b FULL *and* OOS at 10 bps on the large panels: **DRIFT 136 of 180 (75.6%) vs CALENDAR
35 of 80 (43.8%)**; SMALL665 is **0 of 150** for both (fourth confirmation of the VOLTGT memo's A2).

**The mechanism is the 2020 crash, and it is visible directly** (`.crash.csv`, U56 / T=M / t=0.16,
gross on 2020-02-19 -> trough): `h=0.12` goes **1.00 -> 0.254** on 9 refreshes/yr and 2.07 turns/yr;
`R=M`, at a comparable **1.87 turns/yr**, only reaches **0.687**; `R=Q` never moves (1.000).
`R=D` reaches 0.224 but pays **3.57 turns/yr**. A threshold buys the crash response at a
monthly-calendar price, which is exactly the idea's "freshness only where freshness is worth paying
for".

## BUT IT DOES NOT FIX REACHABILITY — V1 FAILS, and the ladder length is why

| pre-stated rule | result |
|---|---|
| **V1 REACHABILITY** (drift reaches 4b FULL+OOS on strictly more arms) | **FAIL** — 3 of 6 arms vs calendar's 3 of 6 |
| **V2 TURNOVER EFFICIENCY** | **PASS** — win share **1.000**, mean **+0.0596** |
| **V3 FRESHNESS REACH** | **FAIL** — drift picks weekly-fresh on **0** arms vs calendar's 2 |
| **V4 CAPITAL** | **PASS** — 10 legal picks clear 4b FULL+OOS (**7 DRIFT / 3 CAL**) |

**The stale preference is FAMILY-INVARIANT, which is the sharp negative result.** Idea 1789 found
the IS chooser takes a stale scalar on 2009–2016 because that window holds no crash; making the
trigger cadence-free does not remove the preference, it *renames* it. The calendar chooser lands on
`R = M` in **22 of 24** legal picks; the drift chooser lands on the two laziest rungs of its own
ladder (`h = 0.16` or `0.25`) in **18 of 24**. `C_ISDD` is the only chooser that buys freshness in
either family.

**And the reach is LADDER-LENGTH FRAGILE — disclosed, because it changed this run's verdict.** On
the 6-rung ladder `h in {0.01 ... 0.12}` first run, V1 **passed** (DRIFT 4 arms vs CAL 3, 13 of 24
picks clearing 4b). Extending the ladder to 10 rungs (`... 0.25`) — the honest fix for an argmax
sitting on the top rung, the defect idea 1771 named on the `t` dial — walks the chooser onto the
new top rungs and drops it to a **3–3 tie with 7 of 24**. Both readings are published; **the
verdict taken is the longer ladder's**, i.e. no reachability gain. The rung is not choosable in
either family; the TRIGGER is what survives.

## Capital arm (PROTOCOL rule 4, both paths, every cell)

* 10 bps, 420 cells: 4b FULL 187, 4b OOS 225, **4b FULL+OOS 187**; **4a 40, 4a OOS 54** — and on
  **U56, the panel the live book runs on, 4a is 0 at every reached pick**: the book's drawdown
  (−18.2%) is deeper than live RULES v2's (−12.05%), which is the failure mode PROTOCOL 4b exists
  for. **Path 4a: KILL.**
* **Rule 8 (2017–2026 read exactly once).** Best reached cell on U56: `C_ISSHARPE`, T=M,
  **`t = 0.16, h = 0.12`** — OOS **16.36% / 1.2810 / −18.16%** at **1.13 turns/yr** against SPY
  15.26% / 0.8737 / −33.72% and live RULES v2 9.46% / 1.2766 / −12.05%; FULL 15.62% / 1.2451 /
  −18.16% (halves 1.2944 / 1.2036). It clears 4b FULL *and* OOS at **0 / 10 / 25 / 50 bps**, where
  the standing memo's own cell fails at 50 and its calendar twin `R=M t=0.16` fails 4b outright
  (OOS MaxDD −24.24%). B136's `h = 0.25, t = 0.16` likewise clears all four rungs (OOS 14.08% /
  1.1888 / −17.93% at 1.19 turns/yr). Memo: `2026-09-20_drift-threshold-refresh_KEEP4b_MEMO.md`.
* The **OOS oracle** (reported, never a pick) is a drift cell on 4 of 4 large-panel arms:
  U56 `h=0.12, t=0.08` OOS **1.3989 / −10.37%** against the calendar oracle's 1.3485 / −15.79%.

## Caveats, stated

Survivorship: U56 / B136 are current-constituent lists, SMALL665 a current sub-$2B screen (54
tickers with `max_1d_move >= 1.0` dropped); every level is optimistic and both 4b bars are easier
here than on a point-in-time panel. The DRIFT-vs-CALENDAR contrast is same-tape / same-names /
same-grid with only the trigger moved, so it is first-order immune; the pass COUNTS are not. The
sigma convention is fixed at `(L=20, d=0)` — idea 1771 showed the standing memo's rung loses 3 of 4
defensible conventions, and this run does **not** re-price that surface. `h` is a genuine free
parameter and this run shows the IS window cannot set it.

**Verdict: ANSWERED.** DOMINANCE on the book axis (V2, 263/263), **KILL** on the chooser axis
(V1/V3), **KEEP-candidate (path 4b)** for the reached U56 cell, path 4a KILL. RULES.md,
PROTOCOL.md, scan.py, bot.py and baseline.py are untouched by this run.
