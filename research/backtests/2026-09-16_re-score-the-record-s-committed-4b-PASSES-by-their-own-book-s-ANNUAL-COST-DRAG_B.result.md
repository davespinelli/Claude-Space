# Idea 930 (lane B, 2026-09-16) — re-score the record's committed 4b PASSES by their own book's ANNUAL COST DRAG

**ANSWERED = THE LINE DOES NOT EXIST. KILL 926's "drag, not the rung" headline; KILL the drag
line as a re-scoring instrument; KEEP the direct reading, which answers the queue's question
anyway: 5 of 18 (0.278) STRICT committed-pass cells sit in a cell where a gross-matched coin flip
clears all five 4b legs at least 5% of the time at the binding 10 bps.** Gates 9 of 9, hypotheses
1 of 10. Nothing promoted; `RULES.md`, `PROTOCOL.md`, `scan.py`, `bot.py`, `baseline.py` untouched.

## What was measured

90 cells (PANEL {U56, B136} × BOOK {TOP5, TOP10, TOP20, EWELIG, BAND03} × GROSS {0.50, 0.75, 1.00}
× CADENCE {W, M, Q}) × 5 cost rungs {0, 5, 10, 25, 50} bps = **450 (cell, rung) points**, each with
its own 200-draw gross-matched RANDROT null. `drag (bp/yr) = realised annual turnover × rung`,
measured from the same turnover series `engine.backtest` charges (G1, G8). Dials, both fully
reported and neither used to choose anything: **CLAIM SET** {STRICT, WIDE, STRUCT} and
**DRAG LINE** bar {0.05, 0.10, 0.25}.

## The premise fails — and the pooled correlation that looked like support is a rung-0 artefact

| subset | n | ρ(drag, null 4b base) | ρ(rung, base) | ρ(turnover, base) |
|---|---|---|---|---|
| ALL 450 points | 450 | **−0.2659** | −0.3384 | +0.1814 |
| non-degenerate nulls | 360 | −0.3033 | −0.3706 | +0.1600 |
| rung > 0 (drag axis non-trivial) | 360 | −0.1460 | −0.2751 | +0.0788 |
| rung > 0 AND non-degenerate | 288 | −0.1671 | −0.2881 | +0.0467 |
| **the BINDING rung only (10 bps)** | 90 | **+0.0784** | n/a | +0.0784 |

**H_MONO FAIL** (−0.2659 against a −0.50 bar) and **H_NOTRUNG FAIL**: |ρ(drag)| 0.2659 is
*weaker* than |ρ(rung)| 0.3384 on the same points — the exact reverse of 926's "a function of
cost × realised turnover, not of the cost rung". The mechanism is arithmetic: **at rung 0 the drag
of every cell is identically 0**, so pooling that column stacks 90 cells at a single x value and
manufactures most of the apparent slope. Delete it and ρ(drag) collapses by 45% (−0.2659 →
−0.1460) while ρ(rung) barely moves. At PROTOCOL's own binding rung, where drag and turnover are
the same variable up to a constant, the sign is **positive**: higher-turnover books are if anything
*easier* for a coin flip, not harder. **H_WITHIN FAIL** too — ρ inside each cadence reads
W −0.461 / M −0.258 / **Q −0.016**, so even the weak pooled ordering is carried by the weekly
column alone.

## D* is one cell, not a threshold

D*(bar) = the largest book drag at which any point still has base rate ≥ bar. **H_100 PASSES —
D*(0.05) = 91.0 bp/yr, inside 926's [50, 200] band** — and it is the run's only passing hypothesis,
which is exactly why it should not be believed. D* reads **91.0 at all three bars (0.05, 0.10 and
0.25 alike)**: a threshold that does not move when the bar quadruples is not a threshold. It is a
MAX over points, and the point setting it is **U56 / EWELIG @0.75 / M at 25 bps, base4b 1.000,
`degenerate=True`** — idea 998's null-construction defect (a holding-count-matched draw from the
eligible pool *is* the book when the book already holds that pool), 18 of 90 families here. On
non-degenerate nulls only, D* falls to 84.7 / 67.6 / 63.2 and does order by bar.

## The queue's actual question, answered by the direct reading

| claim set | claim-cells → cells | median book drag | 4b here | BELOW (direct, 0.05) | BELOW (drag-line, 0.05) | agreement |
|---|---|---|---|---|---|---|
| STRICT | 100 → 18 | 80.1 bp/yr | 0.278 | **0.278** | 0.611 | 0.667 |
| WIDE | 1,114 → 88 | 48.1 bp/yr | 0.114 | 0.125 | 0.739 | 0.386 |
| STRUCT (control) | 10 → 10 | 43.0 bp/yr | 1.000 | 0.400 | 0.900 | 0.400 |

7,414 claim units scanned, 2,171 assert a 4b pass, 256 name ≥1 panel and ≥1 book; **234 name
SMALL663 and are counted unresolvable** (not priced here). **H_BELOW FAIL** — the record's
committed passes do *not* mostly sit below the line: 0.278 against a 0.50 bar. **H_PREDICT FAIL**
(0.667 against 0.80): the drag line and the direct reading disagree on a third of STRICT cells and
on **two thirds** of WIDE ones, and it errs in one direction — the drag line flags 0.611 of STRICT
cells against the direct reading's 0.278, so used as a re-scoring instrument it would condemn more
than twice as many committed passes as deserve it. **H_CLAIM FAIL** (0.153) and **H_STRUCT FAIL**
(0.122) — the share moves with the claim set, so no single number here is the record's "share of
passes that are not evidence".

**The 11 of 90 cells where a coin flip clears all five legs ≥5% of the time at 10 bps** are listed
in the console; **9 are non-degenerate**, all sit at gross 0.75 or 1.00, and **8 of 11 are M or Q**
— the cadence axis, not the drag axis, is where they concentrate. The worst is U56 / TOP20 @0.75 /
M at **base4b 0.770** on only 48.1 bp/yr of drag, and the *lowest*-drag cell in the list
(BAND03 @1.00 / M, 16.4 bp/yr) is the second-least affected. Drag does not order them.

## Rule 8 and both KEEP paths

18 picks = 3 IS-only choosers × 2 panels × 3 cadences, (book, gross) chosen on 2009–2016 **alone**,
2017–2026 read ONCE, 10 bps binding. G6 proves IS-only by permuting the OOS rows.
**OOS 4b 5 of 18, OOS 4a 0 of 18**; full-sample ladder **4b 10 of 90, 4a 0 of 90**.

| chooser | OOS 4b | OOS 4a | mean OOS Sharpe | mean drag |
|---|---|---|---|---|
| C_ISSHARPE | 2/6 | 0/6 | 0.943 | 62 bp/yr |
| C_IS4B | 3/6 | 0/6 | 0.984 | 35 bp/yr |
| **C_ISDRAG** | **0/6** | 0/6 | 0.868 | 147 bp/yr |

**H_RULE8 FAIL (0 vs 2).** Preferring high-drag books is strictly worse out of sample, so drag is
a REPORTING statistic at best and never a selector — the same verdict idea 969 reached for the
certifying-leg count. Best pick U56 `BAND03`@1.00/W: OOS **12.67% / 1.276 / −15.91%**, against
**RULES v2 (live) OOS 9.45% / 1.276 / −12.05%** (full 8.62% / 1.2007 / −12.05%, halves 1.232 /
1.176) and **SPY OOS 15.21% / 0.8711 / −33.72%** (full 15.10% / 0.8829 / −33.72%, halves 0.959 /
0.821). On B136: baseline OOS 7.88% / 1.106 / −12.24%, SPY OOS 15.33% / 0.8767 / −33.72%.
No KEEP candidate on either path, so no memo and no RULES change.

## 926's cadence arithmetic — reconciled, but it FAILS as published

**H_CADENCE FAIL.** Median book drag at 10 bps reads **W 109.6 / M 48.9 / Q 26.4 bp/yr** against
926's committed 161 / 73. The gap is a **gross-ladder** artefact, not a disagreement about the
tape: gross scales turnover linearly, and the median over {0.50, 0.75, 1.00} is not the same object
as a single book. Split by gross, W reads 84.6 / 126.5 / **168.5** and M reads 37.3 / 55.7 /
**74.0** — 926's 161 / 73 are the **@1.00** column to within 5%. The numbers reproduce; the
*label* on them does not, and a drag figure published without its gross is unreadable.

## Gates 9 of 9 PASS, printed before any result number

G0 rebalance masks == `engine.rebalance_mask`, 0 rows · G1 `Ctx` == `engine.backtest` on returns
AND turnover at **10 and 25 bps**, 0.000e+00 / 0.000e+00 · G2 `BAND03`@0.75 ==
`baseline.rules_v2_weights`, 0.000e+00 · G3 CROSS-RUN SPY OOS triple **15.2102% / 0.8711 /
−33.7173%**, max|d| 2.98e-05 · G4 GROSS MATCH row sum 2.998e-15, holding count **0** on every
decision row · G5 determinism, redrawn null bit-for-bit identical · G6 choosers IS-ONLY under
permuted OOS rows · **G7 CROSS-RUN of idea 969's committed ladder: 10 of 90 structural 4b passes
at 10 bps, 10 vs 10** · **G8 COST LINEARITY `net(c) == gross − turnover·c/1e4`, 3.469e-18** — the
gate that makes "drag" the quantity the backtester actually charges rather than an assumption.

## Limits, stated

One null KIND (RANDROT, 926's own convention); RANDFIX is not priced here, and idea 969 measured
the two to disagree leg-by-leg on 12.2% of (cell, leg) pairs, so a per-leg reading of these cells
could move. 200 draws resolve a base rate to about ±0.07 at 2 SE, so a cell reading 0.050 sits on
the 0.05 bar's edge and its label is not certain. The null is GROSS-matched, not turnover-matched —
it randomises WHICH names, not WHEN to be invested, and it churns more than the book it matches
(median 7.34x/yr against 4.67x/yr), which is the honest reason ρ(NULL's own drag, base) = −0.2634
is not the same statistic as ρ(book drag, base). D* is a MAX over 450 points and therefore has no
sampling interval at all; it is reported as the single cell it is. The harvest is a regex over
committed text and inherits every ambiguity ideas 969 and 998 documented; 234 SMALL663 units are
dropped and counted, not imputed. Two panels only.

## Survivorship (PROTOCOL rule 9)

U56 and B136 are CURRENT-constituent lists, so every CAGR and drawdown LEVEL is optimistic and
every 4b count is an UPPER bound. A coin flip drawn from a survivor panel is a BETTER book than one
drawn in real time, so **every null base rate here is also an upper bound** — which cuts AGAINST
this run's own headline: measured live, the coin flip would clear 4b LESS often, so **fewer** than
5 of 18 committed passes would sit below the line, not more. SPY is a real index series and is not
inflated.
