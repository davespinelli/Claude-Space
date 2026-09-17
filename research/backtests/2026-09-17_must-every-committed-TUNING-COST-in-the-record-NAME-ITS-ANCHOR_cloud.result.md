# Idea 1238 (lane cloud, 2026-09-17) — must every committed TUNING COST in the record NAME ITS ANCHOR?

**VERDICT: KILL (capital) — the schema clause is EARNED, the policy it implies is NOT TRADABLE.**
Pre-declared outcome **(A) THE ANCHOR MUST BE NAMED**, read off, not chosen. 10 of 10 gates pass.

## The question

1237 showed the same 620 committed pick-cells price anywhere from -0.3292 to +0.1105 of OOS
Sharpe depending only on which of the record's 19 distinct rung books stands in as the anchor.
So every committed "tuning costs X" figure was measured against ONE counterfactual. This run
asks whether the sentence carrying the figure ever says which.

## ARM 1 — the census (33,957 committed units; LEADERBOARD.md + CHANGELOG.md + 1,162 `*.md`)

5,013 units carry a signed figure of the record's own `[+-]d.dddd` form.

| claim set | n | A_FULL (names all 4 rungs) | A_PARTIAL | A_NONE |
|---|---|---|---|---|
| C_STRICT (substitution + price + "Sharpe") | 140 | **1 (0.007)** | 48 (0.343) | **91 (0.650)** |
| C_LOOSE (substitution or price language) | 1,980 | 2 (0.001) | 281 (0.142) | 1,697 (0.857) |
| C_ALL (any signed figure) | 5,013 | 2 (0.000) | 424 (0.085) | 4,587 (0.915) |

**ONE committed tuning-cost figure in 140 states the comparand book it was measured against.**

## ARM 2 — the re-price (33 checkable C_STRICT claims, each on its own panels x rungs x 10 OOS folds)

`DELTA_c(A) = mean over c's cells [OOS Sharpe(A) - OOS Sharpe(the book c names)]`, SE clustered
on fold. All nine (claim set x candidate set) cells published in `.grid.csv`:

| claim set | cand set | claims | median share keeping SIGN | ALL keep | NONE keep | median spread |
|---|---|---|---|---|---|---|
| C_STRICT | A19 | 33 | **0.2632** | 0.0303 | 0.0000 | 0.4760 |
| C_STRICT | A_REAL9 | 33 | 0.5000 | 0.0303 | 0.0000 | 0.4760 |
| C_STRICT | A_RULE8 | 33 | 0.5000 | 0.0303 | 0.0000 | 0.4760 |
| C_LOOSE | A19 / A_REAL9 / A_RULE8 | 140 | 0.2632 / 0.5000 / 0.5000 | 0.0071 | 0.0000 | 0.4760 |
| C_ALL | A19 / A_REAL9 / A_RULE8 | 202 | 0.2632 / 0.5000 / 0.5000 | 0.0050 | 0.0099 | 0.4760 |

**The median checkable committed figure keeps its SIGN at 5 of the record's 19 anchors (0.2632),
and 1 claim in 33 keeps it at every one.** The per-claim candidate spread runs -0.4455 to
+0.1470 with a median width of 0.4760 of OOS Sharpe, against a typical committed figure of
0.1095 — the unnamed dial is **4.35x the number it was reported to** (gate G7).

Mechanically (1237 G9, replayed): `DELTA_c(A) = meanOOS(A) - meanOOS(c's book)`, so the whole
spread is the ANCHOR column's and carries no information about the claim. Naming the anchor is
therefore not book-keeping: it is the larger half of the measurement.

## ARM 3 — rule 8 walk-forward and both KEEP paths (the tradable arm)

Benchmarks (10 bps, t+1, post warm-up): U56 SPY 15.06% / 0.8815 / -33.72% (halves
0.9600/0.8171), OOS 15.15% / 0.8686; U56 live RULES v2 8.60% / 1.1982 / -12.05%.

66 candidate books: **4a 0; 4b full 17; 4b OOS 16; BOTH 15** — all 15 on U56, all the standing
2026-09-04 candidate's neighbourhood (best U56 N=15: 17.07% / 1.1675 / -20.14%, halves
1.2596/1.1091, OOS 18.87% / 1.1894 / -20.14%). Nothing new is promoted.

The policy the census implies, made rule-8 legal — **S_SIGN**: at each fold, on the IS window
only, hold the anchor iff a strict majority of the candidate set agrees the substitution is
positive; else hold the ladder's IS argmax. 36 stitched OOS curves per policy:

| policy | mean stitched OOS Sharpe | mean CAGR | mean MaxDD | 4b OOS passes |
|---|---|---|---|---|
| S_NONE (tune) | 0.8407 | 12.66% | -26.85% | 3/36 |
| S_ALL (always anchor) | **0.8845** | 13.51% | -25.23% | 12/36 |
| S_SIGN (require sign agreement) | 0.8392 | 12.66% | -26.85% | 3/36 |

**S_SIGN is S_NONE.** It fires at 0.042 of folds on A19 and 0.017 on A_RULE8 (0.200 on
A_REAL9), because the sign-majority condition almost never holds in sample — which is the ARM 2
finding restated as a trade: a committed figure whose sign does not survive its own candidate
set cannot be acted on. S_SIGN - S_NONE is -0.0015 and S_SIGN - S_ALL is -0.0452.

## What this run does and does not license

- **Licensed:** a schema clause. *Every committed price of a substitution must state the
  comparand book (all four rungs) beside the figure.* 139 of 140 existing C_STRICT figures do
  not, and the median one changes sign under 14 of the 19 anchors the record itself supplies.
- **Not licensed:** any capital change. No 4a pass anywhere; the only 4b passes are the
  standing candidate's own neighbourhood, unchanged; the new policy arm is a no-op.

## Caveats

Rule 9 survivorship: B136 and SMALL are CURRENT constituents (SMALL: 663 investable of 715
after dropping 52 names with `max_1d_move >= 1.0` from `data/small_meta.csv`), so their levels
are biased high. The headline is a within-panel SIGN comparison, which the bias does not move.
The census is reflexive (1230): committing this file changes the denominators a re-run reads.
Claim classification is regex-based and errs toward calling a unit A_PARTIAL rather than
A_FULL; the A_FULL count is a lower bound.

Files: `.py`, `.console.txt`, `.census.csv.gz`, `.census_summary.csv`, `.reprice.csv.gz`,
`.cells.csv.gz`, `.grid.csv`, `.books.csv`, `.walkforward.csv`, `.stitched.csv`, `.gates.csv`.
