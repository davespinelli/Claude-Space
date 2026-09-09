# Idea 306 — is-the-MA-threshold-edge-a-CONSTANT-GROSS-effect (cloud, 2026-09-09)

**ANSWER: NO — and the question's premise is the wrong dial twice over. KILL of the MA-threshold
selection edge as a general property.**

1. **It is not a gross effect.** The pair's dSharpe is *invariant* in gross: span **≤ 0.0019** over
   g ∈ {0.50, 0.75, 1.00} in all six panel×construction cells (slope on g between −0.0037 and
   +0.0037). What scales with gross is the pp/yr headline (dCAGR slope **+0.86 pp per unit g** on
   SMALL439, **−2.17** on U56), so quoting the edge in pp/yr makes a gross-invariant statistic look
   gross-dependent. There is no gross at which the answer changes.
2. **It is a panel effect that reverses off the panel it was measured on.** RESPREAD mean dSharpe
   (MA − matched QM), identical at every gross: **SMALL439 +0.027 (t +2.2)**, **U56 −0.079 (t −5.4)**,
   **B136 −0.063 (t −4.3)**. Positive in 27/45 cells on SMALL439 but only 8/45 (U56) and 7/45 (B136).
3. **Even on SMALL439 it is a corner, not a form.** By cadence: −0.015 D, +0.015 W, **+0.061 M,
   +0.067 Q**, +0.005 A. By θ: negative at every θ ≤ 0.00 on all three panels, positive only at
   θ ≥ +0.06 where the MA book holds 10–38% of names. Dropping the three θ where the U56 matching
   gate fails, the SMALL439 edge collapses to **+0.0086 (t +0.98), +0.04 pp/yr** — while the U56 and
   B136 negatives survive (−0.052 t −3.70; −0.039 t −3.27).

**Idea 300's published number reproduces exactly and still fails to generalise.** Restricted to its
own W/M/Q cadences at gross 0.75 on SMALL439, this run gives **dCAGR +1.086 pp/yr, dSharpe +0.0476**
against the published **+1.09 / +0.048**. The failure is one of domain (cadence, θ, panel), not
arithmetic.

## Gates
| Gate | What | Result |
|---|---|---|
| G0.1 | local cadence-extended runner == `engine.backtest` at D/W/M/Q, 3 panels | **PASS**, worst \|dr\| **0.000e+00** |
| G0.2 | matching \|mask frac(QM) − mask frac(MA)\| < 0.01 at all 9 θ, all panels | **FAIL on U56 only** — worst **0.01396** at θ=+0.30 (55 names ⇒ 1.8 pp of `ceil` granularity). SMALL439 worst 0.00166, B136 0.00440 both pass. Robustness above: the U56 sign survives dropping every θ with \|Δ\| > 0.01. |
| G0.3 | idea 300's committed `.decomp.csv` RESPREAD 0-bps CAGR reproduces on SMALL439 at gross 0.75, 54/54 cells | **PASS**, worst \|d CAGR\| **9.7e-17** at 1e-9 |

## Headline — MA-THRESH minus matched QUANTILE-M (mean over 9 θ × 5 cadences = 45 cells)
| panel | con | gross | dCAGR pp/yr (t) | dSharpe (t) | OOS dSharpe | Δturnover/yr | 10-bps as share of 0-bps |
|---|---|---|---|---|---|---|---|
| SMALL439 | RESPREAD | 0.50 / 0.75 / 1.00 | +0.425 / +0.638 / +0.854 (t ≈ +2.15) | **+0.0271 / +0.0265 / +0.0261** (t ≈ +2.2) | +0.046 / +0.045 / +0.044 | +1.55 / +2.26 / +2.91 | 0.716 |
| U56 | RESPREAD | 0.50 / 0.75 / 1.00 | −0.727 / −1.223 / −1.809 (t −3.4…−3.9) | **−0.0781 / −0.0787 / −0.0791** (t ≈ −5.4) | −0.083 / −0.084 / −0.084 | +1.64 / +2.44 / +3.20 | 1.29 |
| B136 | RESPREAD | 0.50 / 0.75 / 1.00 | −0.614 / −1.025 / −1.505 (t −3.9…−4.3) | **−0.0619 / −0.0629 / −0.0637** (t ≈ −4.3) | −0.056 / −0.057 / −0.058 | +2.02 / +3.00 / +3.93 | 1.48 |
| SMALL439 | DEGROSS | all | −0.122 / −0.178 / −0.229 | −0.011 / −0.010 / −0.010 | −0.010…−0.007 | ≈ −0.04 | 0.97 |
| U56 | DEGROSS | all | −0.596 / −0.902 / −1.211 | −0.120 (t −5.6) | −0.089 | ≈ −0.09 | 0.99 |
| B136 | DEGROSS | all | −0.574 / −0.868 / −1.166 | −0.117 (t −5.5) | −0.089 | ≈ −0.01 | 1.00 |

The DEGROSS column confirms idea 300's second half — the MA form loses under de-grossing on every
panel — but that loss is now the *only* part that replicates.

**Costs are not the story.** Under RESPREAD the MA arm trades 1.5–3.9× more per year, so 10 bps
takes ~28% of SMALL439's 0-bps edge (0.89 → 0.64 pp/yr, clause 4 **PASS**), but the pair's median
breakeven is **negative** (−5.6 bps SMALL439, −77 to −105 bps U56/B136) — the sign is set by returns,
not by the cost dial.

## Pre-registered verdict (RESPREAD, 10 bps)
| clause | result |
|---|---|
| (1) dSharpe > 0 at all 3 gross, same sign on all panels | **FAIL** — +0.027 SMALL439 vs −0.079 U56, −0.063 B136 |
| (2) mean dCAGR ≥ +0.50 pp/yr at all 3 gross (SMALL439) | **FAIL** — +0.425 at g=0.50 |
| (3) sign survives rule-8 OOS at all 3 gross (SMALL439) | PASS — +0.046 / +0.045 / +0.044 |
| (4) 10-bps dCAGR ≥ 50% of 0-bps dCAGR | PASS — 0.716 at every gross |

**H_EDGE_IS_REAL FAILS. H_EDGE_IS_A_DIAL_PLACEMENT HOLDS.**

## Rule-8 walk-forward (IS 2010–2016 picks (θ, cadence) by the MA arm's IS Sharpe; OOS read once)
The OOS **pair** difference is positive in **6/18** picks, mean **+0.0004** — the edge is not
selectable. The one large OOS win, SMALL439 RESPREAD (θ=+0.30, M): OOS Sharpe 1.106, OOS CAGR 24.0%
at g=0.75, OOS pair +0.32 — is the deep-θ corner on the survivorship-biased panel and still lands
**below RULES v2 OOS (1.285)**. WF-C: the IS pair difference beats a hard zero at predicting the OOS
pair difference in 9/18 cells cellwise and 12/18 as an IS constant — a coin flip on the statistic
that would have to be stable for the edge to be tradeable.

## Both KEEP paths (all 1,620 books)
**4a 2/1620, 4b 46/1620, BOTH 0/1620.** Both 4a passes are QUANTILE-M/DEGROSS books, i.e. the
*constant-depth twin*, not the MA form. 4b by arm: MA RESPREAD 13, MA DEGROSS 9, QM RESPREAD 14, QM
DEGROSS 10 — the matched twin passes at least as often as the form the edge was claimed for. Failing
clauses: CAGR 962, DD 924, OOS 654, H2 644, H1 630. No memo: nothing here clears both paths and no
book beats the live RULES v2 book OOS.

**SURVIVORSHIP:** SMALL439 and B136 are current constituents of their screens only (no delistings);
CAGR levels are inflated and the 4a/4b columns inherit that whole. The headline is a pair difference
on the same names, same ranking variable and same days, which the bias very largely leaves alone.

Outputs: `.grid.csv` (1,620 books) `.pairs.csv` (810 pairs) `.walkforward.csv` `.leaderboard.txt`
`.console.txt`.
