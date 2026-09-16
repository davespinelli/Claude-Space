# Idea 969 (lane B, 2026-09-16) — re-score EVERY committed 4b PASS against its OWN CELL's PER-LEG NULL, under BOTH kinds

**ANSWERED = ESSENTIALLY ALL OF THEM SURVIVE, AND THAT IS THE PROBLEM.** 17 of 18 STRICT
resolvable committed 4b passes (0.944), 86 of 88 WIDE (0.977) and 8 of 10 structural passes
(0.800) clear idea 942's clause (ii). On the **72 non-degenerate ladder cells the clause fires
0 times**. KILL ×3, CONFIRM ×2, KEEP a re-worded PROTOCOL clause (proposed, not applied — rule 6).
`RULES.md`, `PROTOCOL.md`, `scan.py`, `bot.py`, `baseline.py` untouched.

## The grid
90 cells = 2 panels (U56, B136) × 5 books (TOP5, TOP10, TOP20, EWELIG, BAND03) × 3 gross
(0.50, 0.75, 1.00) × 3 cadences (W, M, Q), at **10 bps binding**, next-day execution.
**36,000 gross-matched coin flips**: 200 draws × 3 kinds × 30 (panel, book, cadence) families,
gross a free rescale of the same picks. Two tuned dials only — CLAIM SET {STRICT, WIDE, STRUCT}
and NULL KIND {RANDROT, RANDFIX} (+ `RANDROT_FREE` reported as a control) — every level printed,
none used to choose anything.

## The answer
| claim set | claim-cells | distinct cells | survive (≥1 certifying leg, BOTH kinds) | RANDROT | RANDFIX | mean certifying legs of 5 | non-degenerate subset | 4b PASS on this tree |
|---|---|---|---|---|---|---|---|---|
| STRICT | 96 | 18 | **17/18 = 0.944** | 0.944 | 0.944 | 2.11 | 14/14 = **1.000** | 0.278 |
| WIDE | 1,058 | 88 | **86/88 = 0.977** | 0.977 | 0.977 | 2.61 | 70/70 = **1.000** | 0.114 |
| STRUCT (control, from prices) | 10 | 10 | **8/10 = 0.800** | 0.800 | 0.800 | **1.40** | 8/8 = **1.000** | 1.000 |

**The only two cells the clause strips anywhere in the 90-cell grid are `EWELIG` U56@0.75/M and
`EWELIG` B136@0.75/W** — exactly the cells whose null is DEGENERATE (1 distinct draw of 200,
idea 998's found defect: a holding-count-matched draw from the eligible pool *is* the book when
the book already holds that pool). The disjunction detects a broken null, not a weak book.

## Why it is vacuous — one leg carries every survival
Of the **32** ladder cells with exactly one certifying leg, the sole certifier is `L_CAGR` in
**20** and `L_DD` in **12**, and **never** `L_H1`, `L_H2` or `L_OOS`. A coin flip essentially
never clears 70% of SPY's CAGR (median RANDROT base rate **0.000**), so `L_CAGR` alone keeps
almost every pass adjudicable under a ≥1 bar.

## 942's per-leg deadness reproduces on the record's OWN claimed cells
Share of STRICT cells where the leg is NON-certifying (base rate > 0.90) under BOTH kinds, with
median base rates ROT / FIX / FREE:

| leg | non-certifying (BOTH) | ROT | FIX | median base rate ROT / FIX / FREE |
|---|---|---|---|---|
| `L_H1` | 0.667 | 0.556 | 0.667 | 0.970 / 0.988 / 0.415 |
| `L_H2` | 0.667 | 0.500 | 0.667 | 0.922 / 0.980 / 0.492 |
| `L_OOS` | **0.722** | 0.500 | 0.722 | 0.950 / 0.995 / 0.507 |
| `L_DD` | 0.556 | 0.500 | 0.556 | 0.895 / 0.975 / 0.043 |
| `L_CAGR` | 0.278 | 0.222 | 0.278 | 0.000 / 0.483 / 0.142 |

The **kind does not move the verdict but it does move the leg**: survival is identical under
RANDROT and RANDFIX, yet the two disagree on **12.2%** of (cell, leg) pairs and RANDFIX is
uniformly the harsher null. Quoting one kind understates leg deadness — which is the part of
942's clause that earns its keep.

## The count bar has the teeth the disjunction lacks
Certifying-leg count over the **72 non-degenerate** cells: ≥1 **72**, ≥2 **56**, ≥3 **45**,
≥4 **33**. Over the **10 structural 4b passes**: ≥1 **8**, ≥2 **4**, ≥3 **1**.

## Rule 8 — walk-forward (picks on 2009–2016 ALONE, 2017–2026 read ONCE)
Three IS-only choosers × 2 panels × 3 cadences = 18 picks. G6 proves IS-only by permuting the
OOS return rows. **OOS 4b 5 of 18. OOS 4a 0 of 18.**

| chooser | OOS 4b | OOS 4a | mean OOS Sharpe |
|---|---|---|---|
| `C_ISSHARPE` | 2/6 | 0/6 | 0.943 |
| `C_IS4B` | 3/6 | 0/6 | **0.984** |
| `C_ISCERT` (this idea's statistic as a selector) | **0/6** | 0/6 | **0.857** |

`H_RULE8` **FAIL** — the certifying-leg count is a reporting statistic, not a selector.

Best pick, U56 / `BAND03`@1.00 / W: full **11.53% / 1.201 / −15.91%** (H1 1.233, H2 1.175),
OOS **12.67% / 1.276 / −15.91%**, against the RULES v2 live baseline full 8.62% / 1.201 / −12.05%
(H1 1.232, H2 1.176), OOS 9.45% / 1.276 / −12.05%, and SPY full 15.10% / 0.883 / −33.72%
(H1 0.959, H2 0.821), OOS 15.21% / 0.871 / −33.72%.

## Hypotheses — 6 of 8 PASS, both failures measured
| | bar | read | |
|---|---|---|---|
| `H_SURVIVE` | STRICT survival ≥ 0.50 | 0.944 | PASS |
| `H_KIND` | \|ROT − FIX\| ≤ 0.10 | 0.000 | PASS |
| `H_LEGAGREE` | leg-label agreement ≥ 0.80 | 0.878 (90 pairs) | PASS |
| `H_CLAIM` | \|STRICT − WIDE\| ≤ 0.10 | 0.033 | PASS |
| `H_STRUCT` | \|STRICT − STRUCT\| ≤ 0.10 | **0.144** | **FAIL** |
| `H_DEGEN` | \|all − non-degenerate\| ≤ 0.10 | 0.056 | PASS |
| `H_ALLCERT` | `L_OOS` non-certifying in ≥ 0.50 | 0.722 | PASS |
| `H_RULE8` | `C_ISCERT` OOS 4b ≥ `C_ISSHARPE`'s | 0 vs 2 | **FAIL** |

`H_STRUCT` fails because text-harvested passes are an EASIER population than price-harvested
ones: only **27.8%** of STRICT text-claimed cells pass 4b structurally on this tree at all — an
independent reproduction of idea 998's published `H_REPRO` of **0.294** on the same corpus,
measured by a different route.

## Gates — 8 of 8 PASS, printed before any result number
`G0` rebalance masks == `engine.rebalance_mask`, 0 rows. `G1` `Ctx` == `engine.backtest` on
returns AND turnover, **0.000e+00 / 0.000e+00**. `G2` `BAND03`@0.75 == `baseline.rules_v2_weights`,
**0.000e+00**. `G3` CROSS-RUN SPY OOS triple **15.2102% / 0.8711 / −33.7173%**, max\|d\| 2.98e-05
against the record's committed value. `G4` GROSS MATCH: row sum 2.998e-15, holding count **0** on
every decision row. `G5` determinism, redrawn null identical. `G6` choosers IS-only. `G7`
CROSS-RUN of idea 942's headline — U56 / `TOP20`@0.75 / M `L_OOS` base rate **1.000 under RANDROT
and 1.000 under RANDFIX**, matching 942's published 250-of-250 on both kinds. Separately, that
same cell's OOS triple reads **17.53% / 1.306 / −19.51%** against 942's published
17.53% / 1.305 / −19.51%.

## Limits, stated
This run prices **2** panels; committed claims naming `SMALL663` (5 of 104 STRICT units) are
dropped and counted as unresolvable, so the STRICT distinct-cell count is 18, not 20-odd. The
null is GROSS-matched, not turnover-matched (926's convention): it randomises WHICH names, not
WHEN to be invested, so it tests security selection and not the gate — `RANDROT_FREE` is printed
beside it for exactly that reason. 200 draws resolve a base rate to about ±0.07 at 2 SE, so a
leg reading 0.90–0.95 is on the bar's edge and a `cert_BOTH` label there is not certain. The
harvest is a regex over committed text and inherits every ambiguity idea 998 documented;
its STRICT rule cannot see a claim that names its cell only by prose.

## Survivorship (rule 9)
U56 and B136 are CURRENT-constituent lists. Every CAGR and drawdown LEVEL is optimistic and
every 4b count an UPPER bound. A coin flip drawn from a survivor panel is a BETTER book than one
drawn in real time, so **every null base rate here is also an upper bound** — which cuts AGAINST
this run's own headline: legs measured live could certify more often than printed, making the
≥1 disjunction even more vacuous, not less.

## Proposed, not applied (rule 6)
`2026-09-16_4b-leg-certification-count-clause_B.memo.md` — replace 942's clause (ii) final
sentence with a CERTIFYING-LEG COUNT (≥2 of 5) plus a DEGENERATE-null declaration.
