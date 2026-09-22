# Idea 935 (lane B, 2026-09-22) — is the RSP-minus-SPY EQUAL-WEIGHT PREMIUM a REGIME OBJECT, or a CONSTANT?

**ANSWERED = IT IS A CONSTANT, AND THE CONSTANT IS ZERO. KILL of the regime-object reading,
of all three ex-ante conditioning variables, and of the RSP/SPY switch as a book. No new
KEEP, no rules change.**

Script `2026-09-22_ew-premium-regime-object-or-constant_B.py`, log `…_B.log.txt`,
96 rows in `out/2026-09-22_ew-premium-regime_B.csv`.

## What was asked
Idea 924 measured the only **survivorship-free** leg of U56's +0.2006 of Sharpe — RSP vs SPY,
two traded ETFs, no name selection — at **+0.0750 (2009–2013), −0.0863 (FULL), −0.1797 (OOS)**.
It changes sign on the window the record quotes it in, and every committed citation quotes one
number. Two readings fit: the premium is a **constant** near zero, or it is a **regime object**
whose sign an ex-ante observable can call. If the second is right, a conditioning book is worth
capital and the record's constant is a mis-statement.

## Construction (nothing re-tuned; 2 tuned parameters, all 68 capital cells published)
Tuned: `v ∈ {BREADTH, DISP, RATE} × q ∈ {0.00, 0.20, 0.40, 0.50, 0.60, 0.80, 1.01}`, where
q=0.00 is **always-RSP** and q=1.01 is **always-SPY** — the two CONSTANT controls, kept in the
grid so conditioning is scored against "do not condition at all".
Published-not-tuned: panel {U56, B136}, gross {1.00, 0.75}, cost {0,10,25,50} bps (headline 10),
windows {FULL, IS 2009-12-30..2016-12-31, OOS 2017-01-01..2026-09-18}.
Regime variables, all price-only and known at the close of t: **BREADTH** = share of the panel's
names above their own 200d MA; **DISP** = cross-sectional stdev of trailing 63d returns; **RATE**
= 63d change in IEF. RSP and SPY are excluded from the cross-section so the signal cannot read
its own legs. Each is converted to an **expanding percentile rank** (min 504 sessions) — causal
by construction, no full-sample quantile anywhere.
**Direction fixed a priori**: rank ≥ q buys RSP, rank < q buys SPY, on all three variables,
declared before any number was read. A premium running the other way is a KILL, not a re-fit.
Execution: weekly, t+1 (engine), 10 bps, long-only, no leverage.
**GATE G1**: the two-column runner ≡ the full-panel runner, max|d| = **0.000e+00** on both panels.

## (A) The premium is not a regime object — 0 of 18 tercile contrasts reach |t| = 2
Annualised RSP−SPY premium by ex-ante tercile, 3 variables × 3 windows × 2 panels:
**max |t(hi−lo)| = 1.398** (B136/BREADTH/IS); **0 of 18** contrasts reach |t| ≥ 2. The tercile
*levels* are no better: **max |t| = 1.969** over all 54 tercile readings, i.e. **not one tercile
of any variable in any window carries a premium distinguishable from zero.**
The one contrast that looks like something in sample reverses out of it: BREADTH hi−lo runs
**+4.88 pp/yr IS → −1.75 pp/yr OOS** on U56 and **+6.71 → +2.67** on B136 — the same instability
idea 924 found in the level, reproduced one level down in the conditioning.

## (B) The capital grid: 0 of 68 cells clear either KEEP path, on FULL or OOS
4a: **0 of 68**. 4b: **0 of 68** on FULL and **0 of 68** on OOS. **0 of 60** conditioned cells
beat SPY's OOS Sharpe (0.8751); the best conditioned cell anywhere is B136/BREADTH/q=0.80/gross
1.00 at OOS **13.45% / 0.785 / −34.15%**. The 4b DD leg fails structurally for every
always-invested cell (cap −20.23%, shallowest cell −26.20%), which re-confirms idea 1699's
"an always-invested ladder passes at 0 of 12 rungs" on a family it had not been tested on.

## (C) Rule 8, 2017–2026 read once — the IS chooser refuses to condition at all
At **4 of 4** (panel × gross) the IS-Sharpe chooser picks the CONSTANT control **always-SPY**
(IS Sharpe 0.845/0.842) over every conditioning cell. Forcing the chooser to condition
(CONSTANT cells removed) picks **BREADTH q=0.20** on both panels:

| panel | book OOS CAGR / Sharpe / MaxDD | RULES v2 OOS | SPY OOS |
|---|---|---|---|
| U56  | 11.14% / **0.663** / −36.25% | 9.46% / 1.277 / −12.05% | 15.29% / 0.875 / −33.72% |
| B136 | 10.80% / **0.651** / −36.25% | 7.85% / 1.102 / −12.24% | 15.26% / 0.874 / −33.72% |

4a FAIL and 4b FAIL at both, at gross 1.00 and 0.75. OOS Sharpe decays monotonically with cost
(0/10/25/50 bps: 0.691/0.663/0.621/0.550 on U56) — no rung rescues it.

## (D) And the regime is beaten by a coin flip at its own switching rate
200 circular block-21 draws that preserve the pick's on-fraction exactly (0.911 U56, 0.916 B136):
the **real** breadth regime lands at OOS-Sharpe percentile **0.320** (U56) and **0.235** (B136),
below the null medians (0.678 / 0.679). Conditioning on real breadth is worse than switching at
random at the same rate.

## What this cannot do (stated, not repaired)
Three variables, one direction, one threshold family. A different observable could still carry
the premium; this run bounds three standard ones and finds nothing at |t| = 2. Both panels are
current-constituent lists, so the breadth/dispersion **signal** is survivorship-bearing (all
absolute levels optimistic) — but the RSP-vs-SPY **contrast** is survivorship-free by
construction, which is exactly why idea 924 singled it out.

## Residue (rule 6; RULES.md, PROTOCOL.md, scan.py, bot.py, baseline.py untouched)
1. The record's committed quotations of the equal-weight premium as a single number are
   **acquitted** — but they should carry the interval: on this tape the premium is
   **indistinguishable from zero in every tercile of every variable in every window**, so
   "+0.0750" and "−0.1797" are the same measurement, not a sign change.
2. Idea 924's mega-cap sleeve result does **not** get a regime repair from this direction.
