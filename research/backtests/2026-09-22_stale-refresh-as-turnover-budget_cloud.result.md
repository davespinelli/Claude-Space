# Idea 1795 — is the STALE-REFRESH PREFERENCE a TURNOVER-BUDGET fact in disguise?

**Lane cloud, 2026-09-22.**  ANSWERED / **NO to the premise (V1 killed)** + an incidental
**KEEP-4b candidate** the budget device reaches.  Script:
`2026-09-22_stale-refresh-as-turnover-budget_cloud.py`.  Every grid point in `.grid.csv`
(1320 rows), decomposition in `.decomp.csv`, walk-forward in `.walkforward.csv`,
turnover-matched lift in `.matched.csv`, execution-lag stress in `.stress_delay.csv`,
dial-neighbour robustness in `.neighbours.csv`.

Panels U56 (56) / B136 (136) / SMALL665 (dropped 54 with max_1d_move ≥ 1.0), 18.7y / 18.7y /
16.7y.  Gates G0–G5 all PASS (G1/G2/G4 exact to 0; G3 reproduces the standing VOLTGT memo to
9.6e-05; G5 gross ≤ 1.00).

## The question and the answer
The record's exposure scalar `g = clip(t/σ20,0,1)` is re-read on a CALENDAR schedule; 23 of 24
legal IS-only picks land on a STALE cadence, and a stale cadence trades ~1.3–1.6 turns/yr against
a daily one's 1.9–5.5.  The idea asked whether the IS statistic prefers stale because it is
buying **saved cost**.  **It is not.**  Decomposing every `R`-gap (stale rung minus R=D) on the
IS window at 10 bps: of the 65 of 90 cells where the stale rung beats R=D on IS Sharpe, the
turnover term exceeds half the net-return gap in only **9 (13.8%)**, and the stale rung ALSO wins
on **gross return in 65 of 65 (100%)**.  Turnover share of the gap: median **0.148**, mean 0.229.
Mean cost saving 18.6 bp/yr against mean gross gain 100.0 bp/yr.  The stale preference is a
**gross-return fact**, not a cost fact (V1 **NOT TRIGGERED**).  It only becomes cost-dominated at
50 bps (45 of 80 cells turnover-driven) — i.e. a budget is the right fix only at costs the
protocol does not headline.

## What the budget device did anyway (V2–V5 all triggered)
The turnover-budgeted refresh (R=D trigger, executed only while trailing-252d turnover + the
refresh's own cost stays under `B` turns/yr; `B=∞` == R=D, gate G4 exact) turns out to REACH more
capital than the calendar cadences even though the premise failed:
- **V2 reachability:** legal IS-only picks clear 4b FULL+OOS on **3 of 6** arms for BUDGET vs
  **1 of 6** for CALENDAR.
- **V3 efficiency:** budget books beat the turnover-matched point on their own calendar ladder in
  **86 of 110 (78.2%)** in-range cells, mean lift **+0.053** OOS Sharpe.
- **V4 capital:** 102 of 330 cells clear 4b FULL+OOS at 10 bps (67 BUDGET, 35 CAL); a legal
  IS-only chooser reaches **7** of them.
- **V5 robustness:** of the reached cells, several are NOT knife edges.

## KEEP-4b candidate (path 4b; 4a fails on the DD clause)
**U56, MONTHLY trade, BUDGET B = 5.0 turns/yr, target t = 0.12, gross cap 1.00, 10 bps**, reached
by the legal IS-only **IS_LEGS** chooser (IS legs = 4, the joint maximiser on U56/monthly).

| window | CAGR | Sharpe | MaxDD | H1/H2 |
|---|---|---|---|---|
| FULL | 14.07% | 1.251 | −15.90% | 1.246 / 1.256 |
| IS 2009–2016 | 12.48% | 1.122 | −13.10% | — |
| OOS 2017–2026 | **15.40%** | **1.357** | **−15.90%** | — |
| SPY OOS | 15.29% | 0.875 | −33.72% | — |
| RULES v2 OOS | 9.46% | 1.277 | −12.05% | — |

4b FULL+OOS holds at **every** cost rung 0/10/25/50 bps (OOS Sharpe 1.387→1.239).  Survives ONE
EXTRA DAY of execution lag (t+2: OOS 15.05% / 1.326 / −16.24%, still 4b).  Clears 4b at **both**
neighbouring budget rungs (B=3.0 and B=∞) and **both** neighbouring targets (t=0.10, t=0.16).
Realised 3.31 turns/yr, 155 scalar refreshes/yr — i.e. it runs the FRESH scalar the record's
calendar cadences could not afford to pick, at a monthly trade cadence.  **4a fails**: it beats
live RULES v2 in both half Sharpes but its −15.9% MaxDD is worse than the live book's −12.05%.

Also reached and 4b-clean: U56 T=M B=5.0 t=0.16 (IS_SHARPE, OOS 16.63%/1.273/−19.77%),
B136 T=M/W B=5.0 t=0.20 (IS_SHARPE), B136 T=W B=∞ t=0.10 (IS_LEGS).

## Caveat (rule 9)
U56/B136/SMALL are CURRENT-constituent lists; the SMALL panel is a current sub-$2B screen.  Every
CAGR/DD LEVEL is survivorship-optimistic and both 4b bars are easier here than point-in-time.  The
budget-vs-calendar contrast is same-tape/same-names/same-grid with only the refresh TRIGGER moved,
so it is first-order immune; the PASS COUNTS and the candidate's LEVELS are not.  The candidate is
the same U56 VOLTGT/fresh-scalar object ideas 1789/1793 already isolated (the daily-refresh scalar
is the one that clears 4b OOS); this run's contribution is that a TURNOVER BUDGET reaches it with
a legal IS-only chooser at a monthly trade cadence, and that the stale preference it was built to
fix is a gross-return artefact, not a cost artefact.
