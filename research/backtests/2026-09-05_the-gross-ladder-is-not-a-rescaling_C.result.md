# Idea 176 — the-gross-ladder-is-not-a-rescaling (lane C, 2026-09-05)

**VERDICT: ANSWERED — KILL of the exposure the idea was written to find. The committed record is
clean: across 124 scripts and 1,370 published ladder groups, ZERO gross ladders were priced by
rescaling a return series. Post-adjudication exposure = 0 committed LEADERBOARD rows.**
Two by-products outrank the null result and both are PROTOCOL-relevant: (i) idea 165's "fine for
ranking, wrong for verdicts near a bar" is **confirmed at bar level** (up to 46.7% of points
within 0.005 of the H2 bar flip) and **near-harmless at whole-4b level** (1 of 530); (ii) the
convention's Sharpe error is the **size of the entire measurable Sharpe content of the gross
dial**, so a gross argmax is not a measurable quantity at this precision. No RULES change, no
new KEEP.

## Design
Two swept parameters, and they are the idea: **m**, the gross ladder point (10 points
0.20–1.00, idea 78/166's ladder) × **m0**, the rescaling ANCHOR — the convention under audit —
(2 values, 0.75 and 1.00). Both reported everywhere; nothing is selected on either.
Corpus (idea 171/174's, reused verbatim): 53 books (U56, B136, BSTK100, ETF36, SMALL484 + 48
sub-panels, k∈{20,40,80}×16 draws, seed 171500+k) × 10 gross = **530 GENUINE backtests**, 10 bps,
t+1, weekly, sleeve 0, book = idea 2's top-20 composite candidate. No number in this file was
produced by rescaling.

**The algebra the audit rests on.** A ladder rescaled from m0 asserts `r_m = (m/m0)·r_{m0}`, and
`Sharpe(c·r) = c·mean/(c·std) = Sharpe(r)` **exactly** (turnover is linear in gross, so costs
scale too). A rescaled ladder therefore has a **perfectly constant Sharpe column to machine
precision**. Under `engine.backtest` it never is, because held weights drift and are renormalised
against a constant-value cash sleeve `(1 − gross)`. That fingerprint survives in the committed
CSVs even where the code is unreadable — which is what makes the audit possible on the *published
numbers*, not only on the code.

## Reproduction, asserted before any new number was read
| check | result |
|---|---|
| [a] `fast_backtest` ≡ `products/backtester/engine.backtest` | max\|dret\| **1.388e-17**, max\|dturn\| 3.053e-16 — PASS |
| [b] idea 174's committed sleeve=0 GROSS rows | **530 of 530 matched**, max\|diff\| **2.220e-16** on CAGR/Sharpe/MaxDD/H1/H2 — PASS |
| [c] idea 165's committed `[c] exact lever` rows, re-read from disk | n=12, max\|dMaxDD\| **0.2755pp**, max\|dCAGR\| 0.0238pp, max\|daily diff\| 4.902e-03 — matches the QUEUE text |
| [c′] idea 165's CAGR-monotonicity claim, re-counted from its own `greq.csv` | **92 of 213** — reproduced exactly, and decomposed: **0 of 165** non-failing books, **92 of 213** CAGR-floor failures |

## A1–A4 — the audit (three independent instruments)
| instrument | what it tests | result |
|---|---|---|
| **A1 static** | AST scan of all 124 committed scripts: does a ladder value reach a simulation, or a return series? | **0 RESCALED, 1 MIXED, 55 GENUINE, 9 LADDER-UNCLASSIFIED, 59 NO-LADDER** |
| **A2 numbers** | exactly-constant Sharpe along a committed ladder = the rescaling fingerprint | **0 of 1,370 groups** across 22 committed ladder files (min observed range 1.29e-03) |
| **A3 numbers** | CAGR monotone along a committed ladder at a rate the true engine cannot produce | 58 of 1,370 groups (4.2%) non-monotone — consistent with genuine re-runs, no file anomalous |
| **A4 adjudication** | each A1 flag against a mechanical rule + its own published numbers | **exposure 0 rows** |

The single MIXED file is **idea 165's own script**, and its single RESCALED line is
`ann_vol(r * (g / GROSS))` at L435 — the `ach_lever` arm of that script's *own* lever control,
sitting one line above its genuine counterpart `ach_true` at L436. The adjudication rule is
mechanical and applied identically to every flag ("a RESCALED line is a lever CONTROL if a
GENUINE line sits within ±2 source lines"), not a judgement call about that file.

**Coverage, stated not buried.** A1 reaches 2,007 of LEADERBOARD's 3,315 rows (60.5%); the other
1,308 name a Script cell that is not a committed `.py` in `research/backtests` (free text, a
helper, a deleted file) and are out of A1's reach. A2 audits their *numbers* wherever a ladder
CSV was committed. Nine scripts (314 rows) carry a ladder A1 could not classify; A2 covers those
whose ladders were committed as CSVs. The honest statement is therefore: **no evidence of any
rescaled gross ladder anywhere in the record, on three independent instruments**, not a proof.

## B — what the convention costs, measured (the counterfactual the idea asks for)
| anchor m0 | max\|dCAGR\| | max\|dSharpe\| | max\|dMaxDD\| | max\|dH2\| |
|---|---|---|---|---|
| 0.75 | 0.0677pp | 0.0052 | **0.2236pp** | 0.0049 |
| 1.00 | 0.0661pp | 0.0072 | **0.2439pp** | 0.0068 |

At `m == m0` the two conventions coincide to 0.000e+00 (asserted). The Sharpe error grows
monotonically in `|m − m0|` (mean 1.1e-04 → 1.9e-03 across the span); the CAGR and MaxDD errors
peak mid-ladder. Magnitudes agree with idea 165's independent measurement on a different corpus.

**B2 — the noise floor (the run's own hypothesis, and the finding that outranks the null).**
The genuine ladder's *whole* Sharpe range over 10 gross points has median **0.0014**. The
convention's max\|dSharpe\| has median **0.0012** (anchor 0.75) and **0.0014** (anchor 1.00), and
is **≥ the entire range in 30 of 53 books (56.6%) at anchor 1.00, median ratio exactly 1.000**.
The mechanism is exact, not coincidental: a rescaled ladder is a flat Sharpe line through the
anchor, so when the anchor sits at an extreme of the genuine curve the error *equals* the range —
i.e. **the entire measurable Sharpe content of the GROSS dial is the cash-sleeve drift term, the
one term a rescaling drops.** Idea 173 records that GROSS carries **46 of the project's 104
argmax claims** and measured its OOS range at 0.003. Those claims are argmaxes of a drift term at
the precision of the pricing convention.

## C — verdict exposure: is "wrong for verdicts near a bar" true?
Per bar, points within 0.5pp (Sharpe bars: 0.005) of the bar, and how many the convention flips:

| bar | near, anchor 0.75 | flipped | near, anchor 1.00 | flipped |
|---|---|---|---|---|
| CAGR floor | 38 | 0 (0.0%) | 38 | 0 (0.0%) |
| DD cap | 22 | 0 (0.0%) | 22 | **1 (4.5%)** |
| H1 Sharpe | 14 | 0 (0.0%) | 14 | 0 (0.0%) |
| **H2 Sharpe** | 30 | **6 (20.0%)** | 30 | **14 (46.7%)** |
| OOS Sharpe | 0 | — | 0 | — |
| **full 4b** | — | **0 of 530** | — | **1 of 530 (0.19%)** |

So idea 165's warning is **half right and the half matters**: at the level of an individual bar
the convention flips up to 46.7% of near-miss points, and every one of them is a **Sharpe** bar
(H2), not the CAGR/DD bars idea 165 named. At the level of a whole 4b verdict it costs **one row
in 530** (`B136k40d11 @ m=0.90`, flipped on the DD cap: margin +0.0139 genuine vs +0.0132
rescaled). The project's near-miss literature is written in *bar margins*, so the exposure is
real where the project actually reads the numbers.

## A3 — idea 165's non-monotone CAGR does NOT reproduce here, and its own file says why
**0 of 53 books** are non-monotone on 0.20–2.00 under idea 165's own test (`any diff < −1e-12`),
including 0 of the 31 books here that fail the CAGR floor at m=0.75. Idea 165's 92-of-213 is
reproduced exactly from its `greq.csv` and decomposes as **92 of 213 CAGR-floor failures vs 0 of
165 non-failures** on *its* arm construction (tilted/share books). Scope, not contradiction — but
"CAGR is not monotone in gross" is a statement about that arm family, not about the engine, and
should not be quoted as a general property.

## Rule 8 walk-forward — gross chosen ≤2016-12-31, read ONCE on 2017-01-01→
| arm | mean OOS CAGR | mean OOS Sharpe | mean OOS MaxDD | beats SPY | OOS-window 4b | mean pick |
|---|---|---|---|---|---|---|
| CONTROL m=0.75 (do nothing) | 9.96% | **0.9638** | −17.18% | 45/53 | **14** | 0.75 |
| GENUINE ladder, IS-Sharpe argmax | 13.00% | 0.9633 | −22.25% | 45/53 | 5 | 0.987 |
| RESCALED ladder, tie-break low | 2.67% | 0.9645 | −4.75% | 45/53 | 0 | 0.20 |
| RESCALED ladder, tie-break high | 13.22% | 0.9632 | −22.54% | 45/53 | 4 | 1.00 |
| SPY | 15.45% | 0.8820 | −33.72% | — | — | — |
| RULES v1 (U56 / B136 / SMALL) | 7.73% / 5.94% / 19.31% | 0.7471 / 0.5763 / 0.6046 | −13.83% / −21.19% / −35.01% | — | — | — |

Paired vs the do-nothing control: GENUINE **−0.0006 (t −4.24), wins 14–39**. Selection loses to
doing nothing again — the seventh instance after ideas 110/132/151/166/171/174.

**The pre-registered degeneracy is confirmed and is the sharpest thing here:** the rescaled
ladder's IS-Sharpe column is flat to **6.661e-16** across all 53 books × 2 anchors, so an
IS-Sharpe selector has **no argmax at all** on it. Both tie-breaks bracket OOS Sharpe within
±0.0006 — but they bracket **OOS CAGR from 2.67% to 13.22%, OOS MaxDD from −4.75% to −22.54%, and
OOS-window 4b passes from 0 to 4.** A rescaled ladder would not have changed the project's
rankings; it would have removed the project's ability to choose a gross at all, and left the
choice to whichever end of the loop ran first.

## Both KEEP paths (PROTOCOL rule 4), all 530 genuine points in `.keep.csv`
4a passes **426**, 4b passes **28**, both **25** (B136 25, U56 3, SMALL 0). Every 4b pass is one of
idea 171/174's already-committed passes; **no new candidate is proposed** and no book is claimed
here. Best by full-sample Sharpe: `B136k20d00 @ m=1.00` 12.98% / 1.1617 / −17.91%, `U56 @ m=0.80`
13.72% / 1.1076 / −19.35%.

## Predictions, scored honestly
P1 ✓ ([a],[b],[c] all pass) · P2 ✓ (0 rescaled scripts) · P3 ✓ (0 of 1,370 groups) · P4 ✓
(magnitudes as idea 165 reports, error grows in |m−m0|) · P5 ✓ at bar level, **✗ at whole-4b
level** (1 of 530, not "materially above zero") · P6 **✗** (0 of 53, not ~43% — reconciled above)
· P7 ✓ at anchor 1.00 (56.6% of books), **✗ at anchor 0.75** (0 of 53) · P8 ✓ · P9 ✓ (no new KEEP).
Two of nine missed, both reported rather than re-framed.

## Recommendation to PROTOCOL (one line, for the Sunday review to accept or reject)
Add to rule 2: *"Every point on a gross ladder is a separate backtest. A ladder may never be
produced by scaling one run's return series: under `engine.backtest` that changes MaxDD by up to
0.24pp and flips up to 47% of the points sitting within 0.005 of a Sharpe bar, and it makes the
ladder's Sharpe column exactly constant, which silently destroys any gross selection."*
The audit says the project already obeys this; the rule makes it checkable (A2 is a one-line test
on any committed ladder CSV).

## Caveats carried
Survivorship (idea 54) on U56/B136/SMALL484 — but the audit's conclusions are about the
*difference* between two pricing conventions on the same data, from which the bias largely
cancels; the 4b pass counts inherit it in full. A1 is a static analyser, not a proof, which is
why A2/A3 run alongside it and why every classification prints its evidence line. A2's blind spot
is a *partial* rescaling (returns scaled, costs left at the anchor's turnover), which would not
have an exactly-constant Sharpe; A3 is the weak net for that case. Idea 144 (a re-grossed book is
the same book): 530 points are 53 books at 10 exposures. Ideas 38 and 126 carry over.

Outputs: `.console.txt`, `.audit_static.csv`, `.audit_numbers.csv`, `.audit_adjudication.csv`,
`.points.csv`, `.error.csv`, `.keep.csv`, `.walkforward.csv`.
