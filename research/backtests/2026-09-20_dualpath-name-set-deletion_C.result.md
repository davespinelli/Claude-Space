# Idea 2050 (lane C, 2026-09-20) — IS THE DUAL-PATH CELL A B136 NAME-SET ACCIDENT?

**Object.** Idea 2034's cell `B136, VOLTGT t = 0.10, DRIFT refresh h = 0.08, trade weekly, 10 bps,
t+1` — the standing KEEP-candidate, on path **4b only** since idea 2054's addendum. Every one of
2054's 36 stress points was read on the SAME 136 columns, and idea 1749 showed the name set is a
REACHABLE axis worth ~43 pp of 4b pass rate. This run deletes names at random and re-scores.

**Construction.** 2,403 rebuilt books at the candidate cell (3 panels x {0, 5, 10, 20, 40} deleted
names x 200 seeded draws, k = 0 being the undeleted reference), plus 9,150 books for the rule-8
arm (the first 15 draws of every (panel, k), the two inherited dials re-chosen on 2009-2016 only
over `t` x `h` = 5 x 10, 2017-2026 read exactly once). Deleting a name rebuilds everything that
depends on the panel: the equal-weight basket, the realised panel volatility that drives the gross
scalar, the drift trigger and the turnover. Gates 8/8; the undeleted B136 reference reproduces
idea 2034's published candidate to max abs d = **4.441e-16**.

---

## V1 — THE 4b PASS IS **NOT** A NAME-SET ACCIDENT: 800 of 800, 100.0%

| panel | k | deleted | n | **4b** | 4a (fixed bar) | 4a (matched bar) | mean Sharpe | mean CAGR | mean MaxDD |
|---|---|---|---|---|---|---|---|---|---|
| B136 | 0 | 0.0% | 1 | PASS | PASS | PASS | 1.2286 | 12.51% | -11.81% |
| B136 | 5 | 3.7% | 200 | **1.000** | 0.760 | 0.765 | 1.2210 | 12.43% | -12.05% |
| B136 | 10 | 7.4% | 200 | **1.000** | 0.630 | 0.605 | 1.2191 | 12.41% | -12.17% |
| B136 | 20 | 14.7% | 200 | **1.000** | 0.405 | 0.420 | 1.2154 | 12.39% | -12.36% |
| B136 | 40 | 29.4% | 200 | **1.000** | 0.280 | 0.330 | 1.2078 | 12.31% | -12.46% |

Over all 800 deleted B136 draws the WORST reading of every 4b leg margin is still positive:
H1 **+0.2254**, H2 **+0.2064**, OOS **+0.2997**, MaxDD vs `0.60 x SPY` **+6.40 pp**, CAGR vs
`0.70 x SPY` **+0.63 pp**. Worst single book: 11.22% / 1.1099 / -13.83% full, 11.73% / 1.1734 /
-13.83% OOS, against SPY 15.12% / 0.8843 / -33.72% (OOS 15.26% / 0.8737 / -33.72%) and live
RULES v2 on B136 7.96% / 1.0972 / -12.24% (OOS 7.85% / 1.1017 / -12.24%). Mean Sharpe falls
0.0208 across the whole ladder and the dispersion stays small (sd 0.0113 at k = 5, 0.0313 at
k = 40). **Pre-stated V1 band: >= 0.80 at every rung -> ROBUST. Measured 1.000 at every rung.**

## V2 — THE 4a PASS FAILS A **SECOND, INDEPENDENT** AXIS, AND THROUGH THE SAME LEG

4a decays monotonically in k — **0.760 -> 0.630 -> 0.405 -> 0.280** — and the MATCHED bar (live
RULES v2 rebuilt on the same deleted names) tracks it within 0.05 at every rung, so this is a
**book** effect, not a comparand effect. Of the 385 failures, **381 fail on DRAWDOWN** and 371 on
drawdown ALONE; both Sharpe halves clear in 786 of 800. That is the identical mechanism idea 2054
found on the latency axis. The reason is the margin: the candidate's -11.81% sits 0.43 pp inside
the live book's -12.24%, and the mean deleted book already reads **-12.26%** — through the bar.
Deleting FIVE names of 136 is enough to break 4a in 24% of draws. **Pre-stated V2 band:
<= 0.40 on both bars -> ARTEFACT. Measured 0.280 / 0.330.**

## V3 — THE COMPANION PANELS, AND WHICH LEG MOVES

* **U56** carries the same cell: 4b at **1.000 / 1.000 / 0.965 / 0.710** for k = 5 / 10 / 20 / 40
  — but k = 40 is **71.4%** of that panel. Of its 65 failing draws the **CAGR floor is implicated
  in 54**, drawdown in 2. 4a never passes on U56 at any rung (0.000-0.015), which is a property of
  the cell on that panel, not of the deletion.
* **SMALL665: 0 of 800** at every rung and **0 of 60** rule-8 picks — a FURTHER independent confirmation
  that this family does not clear 4b on small caps. All five legs fail at all 800 draws.
* **The ladder is absolute, not fraction-matched**: k = 40 is 71.4% of U56, 29.4% of B136 and 6.0%
  of SMALL665, so the per-panel shares above are NOT directly comparable. Stated, not repaired.
* **SPY is itself a held name on U56 and B136.** Deleting it costs U56 13 pp of 4b share (0.834
  with SPY gone vs 0.965 with it kept, 283 draws) and costs B136 **nothing** (1.000 either way,
  111 draws).

## V4 — RULE 8 ON THE DELETED PANELS (IS 2009-2016 chooses `t` and `h`; 2017-2026 read ONCE)

| panel | k | n | reached book clears 4b | OOS CAGR | OOS Sharpe | OOS MaxDD |
|---|---|---|---|---|---|---|
| B136 | 5 / 10 / 20 / 40 | 60 | **59 of 60** (1.000 / 1.000 / 1.000 / 0.933) | mean 13.10% (12.05-15.43%) | mean **1.2752** (1.1663-1.3716) | worst -21.06% |
| U56 | 5 / 10 / 20 / 40 | 60 | 53 of 60 | mean 14.42% | mean 1.2557 | worst -23.71% |
| SMALL665 | 5 / 10 / 20 / 40 | 60 | **0 of 60** | mean 6.05% | mean 0.4564 | worst -33.61% |

Comparands, OOS: live RULES v2 **7.85% / 1.1017 / -12.24%** on B136 (9.46% / 1.2766 / -12.05% on
U56), SPY **15.26% / 0.8737 / -33.72%**. The reached book clears 4a (fixed bar) at only 0.267-0.333
of B136 picks — V2 again. On average **38.5 of the 50 ladder cells** clear 4b on a deleted B136
panel, so the chooser is picking out of a wide passing region rather than hitting a knife edge.

**Where the chooser lands.** On deleted B136 it keeps `t = 0.10` at **57 of 60** draws but lands on
the candidate's own `h = 0.08` at only **17 of 60** (h = 0.16 at 19, h = 0.12 at 10, h = 0.20 at
10). The TARGET is the stable dial; the drift THRESHOLD is not — the same lazy-rung wander idea
1799 measured. It does not change the verdict here, because 59 of the 60 rungs it wanders onto
clear 4b anyway.

---

## VERDICT

**ANSWERED, and it cuts both ways.**

1. **4b: ROBUST — the standing KEEP-candidate is NOT a B136 name-set accident** (800 of 800, every
   leg margin positive at the worst draw, 59 of 60 legal rule-8 reaches). This is the axis idea
   1749 said should be worth ~43 pp of pass rate, and on this cell it is worth zero.
2. **4a: a KILL of the unqualified claim on a SECOND axis.** Idea 2054 killed it on cost x delay x
   phase (8 of 36); this kills it on the name set (0.280 at k = 40, 0.760 at k = 5), through the
   same drawdown leg, against both a fixed and a matched bar. The 4a claim must not be quoted
   without its settings AND its name set.

**No new KEEP is filed.** This run prices an existing candidate; the finding is recorded as an
addendum to `2026-09-20_voltgt-drift-b136_KEEP4b_MEMO.md`, whose status is unchanged:
**KEEP-candidate on path 4b only, awaiting Sunday review.** RULES.md, PROTOCOL.md, scan.py, bot.py
and baseline.py are untouched.

**SURVIVORSHIP (rule 9).** U56/B136 are CURRENT-constituent lists and SMALL665 a CURRENT screen.
Random deletion removes survivors at random where history removes losers, so it bounds the
verdict's SENSITIVITY to the name set and does NOT de-bias the levels, which stay optimistic on
every panel here.

**Evidence.** `2026-09-20_dualpath-name-set-deletion_C.py` / `.log.txt` / `.draws.csv.gz` (2,403
rows) / `.summary.csv` / `.walkforward.csv` (183 picks) / `.wf_summary.csv` / `.gates.csv` (8/8).
