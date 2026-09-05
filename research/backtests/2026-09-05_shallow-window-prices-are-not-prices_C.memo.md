# Memo — idea 128: the depth clause PROTOCOL should NOT adopt (2026-09-05, lane C)

1. Not a KEEP candidate: 192 arm-points, 4a 54 / 4b 29, all pre-existing. No RULES change.
2. Idea 122's `40 IS vs 0 OOS` is a filter tautology: 103/104 book troughs sit in 2017-2026, so
   `dMaxDD_full == dMaxDD_OOS` in 132 of 138 published rows (corr 0.998). Do not cite it again.
3. Unconditional truth: dMaxDD > 0 in 58/96 IS rows and 71/96 OOS rows — 60% vs 74%, not 0%.
4. No depth makes a drawdown denominator reliable: max frac over 1,640 rolling windows is 0.833;
   the fitted L=4 / 90% crossing is 77.5 pp of SPY drawdown, deeper than 2008.
5. The depth-frac slope is +0.0051/pp (t +7.07 overlapping, **t +0.04 disjoint**) — not inference.
6. As a rule-8 selector the clause changes 13 of 30 picks and loses OOS: S2 0.885 vs S1 0.885 vs
   the do-nothing control S0 **0.937** (SPY 0.882, RULES v1 0.747).
7. Inside rule 8's IS half a deeper ruler cannot be bought: the deepest sub-window is 22.062 pp
   at every L from 2 to 6 years.

**Proposed PROTOCOL rule 4 clause (report-only, negative):** *"A drawdown ratio's denominator is
not made measurable by the depth of its evaluation window: on 1,640 rolling windows the share of
sign-positive denominators never exceeds 83% at any observable depth. Do not qualify a published
price by window depth, and never quote an IS-window drawdown price as if the OOS-window price
were the same measurement — where the full-sample trough lies in one half, the two are the same
number. Report `(dCAGR, dMaxDD)` with its half-sample pair, per idea 123's relative floor."*

**Rule 8 note:** the 2009-2016 IS window's 22.1 pp depth is a hard ceiling, not a choice — idea
111's re-derived split date cannot fix it, so any rule-8 statement about drawdown instruments
should say the IS half prices them at 60% sign reliability rather than pretend to a threshold.
