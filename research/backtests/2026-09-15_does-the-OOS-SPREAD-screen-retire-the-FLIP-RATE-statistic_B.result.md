# IDEA 669 — does-the-OOS-SPREAD-screen-retire-the-FLIP-RATE-statistic

**lane B · 2026-09-15 · script `2026-09-15_does-the-OOS-SPREAD-screen-retire-the-FLIP-RATE-statistic_B.py`**

**ANSWER: YES for the HEADLINE, NO for the SCREEN. KILL for capital — nothing promoted.**
The OOS rung-to-rung spread dominates the flip rate as a predictor of what a misread costs
(incremental R² of flip rate over spread **+0.0040** on CORE5, **+0.0550** on EXT9), so as a
*published* statistic the spread retires it. But the spread is a **look-ahead field**: its
in-sample twin orders it at only **Spearman +0.54..+0.56** and agrees on the decision/coin-flip
classification at **60–67 %** at the natural bar, and traded as a real screen it **costs CAGR in
39 of 42 arms** (median −0.35 pp) and destroys 4b OOS passes rather than creating them: PLAIN
passes 2 of 6, the screen 4 of 42, and it kills the U56/CORE5 pass at **every** bar and the
U56/EXT9 pass at every bar ≥ 0.20. Rule 8 can require the spread as a **reporting** field; it
cannot use it as a filter.

---

## Corpus

27 pick sites = 3 panels × 9 dials. Panels U56 (56 cols), B136 (136), SMALL483 (716 incl. SPY).
Dials: **CORE5** = idea 668's committed set (BAND, N, GROSS, VOLCAP, CADENCE); **EXT9** adds
MAWIN, QUANT, VOLEXP, LAG. Chooser = argmax IS Sharpe on 2009..2016, ties to smallest rung index
(668's convention). Misread channels ROUND / WINDOW / BOOK copied verbatim from 668; the
look-ahead `FULL` window level is flagged and excluded from every cost number. 10 bps, next-day
execution, weekly cadence except on the CADENCE dial. 174 (panel × dial × rung) cells published.

**Tuned parameters (2):** PICK SET ∈ {CORE5, EXT9}; SPREAD BAR ∈ {0.01, 0.02, 0.05, 0.10, 0.20,
0.30, 0.50}. All 14 (pickset × bar) census points and all 54 walk-forward arms are reported.

**SURVIVORSHIP (PROTOCOL 9):** B136 and SMALL483 are today's constituents, so every *level* on
those panels is biased upward. Every claim below is a within-site **rank** statistic.

## Gates

| gate | result |
|---|---|
| G1 `fast_backtest` == `engine.backtest` @10 bps | 8.674e-18 **PASS** |
| G2 `band_book(0.03,0.75)` == `baseline.rules_v2_weights` | 0.000e+00 **PASS** |
| G3 `band_state_w(·,0.03,200)` == `baseline.band_state` | 0 cells differ **PASS** |
| G4 `score_e(·,0.5)` == `baseline.score(vol_scale=True)` | 0.000e+00 **PASS** |
| G5a CORE5 IS ladder **levels** vs 668's committed `curvature.csv`, bar 5e-4 | **4 of 10, FAIL** |
| G5b CORE5 **picks** vs 668's committed `grid.csv` control rows, exact | **10 of 10 PASS** |
| G6 every ladder contains its live constant | **PASS** |

**G5a is a vintage finding, reported not hidden.** The sweep over truncated tapes
(today / 2026-09-11 / 09-10 / 09-09) puts the best residual at **"today" for all 10 sites**, so
the drift is *not* appended rows — it is re-adjusted historical adjusted closes, which move an
IS-window statistic that ends in 2016. The damage is concentrated in the **ranked-book** dials:
U56 BAND/GROSS/VOLCAP/CADENCE reproduce at 1.5e-5…4.0e-5 while U56 **N** is 4.2e-3 and B136
**VOLCAP** 1.6e-2 and **N** 1.3e-2 — cross-sectional ranking amplifies a tape revision by ~3
orders of magnitude over a band gate. Every B136 site exceeds the bar (the broad cache is
re-written weekly). G5b, which is what this run's rank statistics actually stand on, is exact:
all 10 committed picks reproduce, max |ΔOOS Sharpe| on them 1.262e-02.

## Q1 — does the OOS spread retire the flip rate? **YES as a headline.**

Target = **worst cost** = max over honest-but-different reads of
`OOS Sharpe(honest pick) − OOS Sharpe(misread pick)`.

| pickset | n | ρ(cost, **OOS spread**) | ρ(cost, **flip rate**) | ρ(cost, IS spread) | ρ(cost, IS margin) | partial flip \| spread | R² spread / flip / both |
|---|---|---|---|---|---|---|---|
| CORE5 | 15 | **+0.8547** | +0.3862 | +0.4510 | +0.0764 | +0.2613 | 0.8669 / 0.0641 / 0.8709 |
| EXT9 | 27 | **+0.7636** | +0.2972 | +0.4703 | +0.0765 | +0.3954 | 0.7779 / 0.0523 / 0.8329 |

Statistic named per open idea 564: **Spearman**, n as shown; partial = rank-residual correlation.

668's +0.83 replicates on a 27-site corpus with a third panel (+0.85 CORE5, +0.76 EXT9). The
flip rate adds **+0.0040 / +0.0550** of R² once the spread is in. The **IS margin** — the
quantity a chooser is nominally deciding on — is worth **+0.08**, i.e. nothing.

The clean demonstration: **U56 / LAG has the corpus's highest flip rate (0.909) at a worst cost
of exactly 0.0000**, and 6 of 27 sites carry flip rate ≥ 0.50 at zero cost (U56 GROSS, U56 LAG,
B136 GROSS, B136 VOLCAP, SMALL483 GROSS, SMALL483 QUANT). **11 of 27 sites have zero cost**: the
honest pick was never beaten by any misread.

**Cost ladder (0/5/10/25/50 bps), CORE5 | EXT9:** ρ(cost, spread) 0.880|0.872, 0.880|0.895,
0.855|0.764, 0.885|0.737, 0.757|0.633 — the spread leads the flip rate (0.434|0.284 … 0.111|−0.041)
at **every rung on both pick sets**. The answer is not a cost artefact.

## Q2 — how many committed picks were decisions? **Most, at bars where nothing is at stake.**

| bar | CORE5 decisions (OOS spread) | EXT9 | mean cost, decisions | mean cost, coin flips |
|---|---|---|---|---|
| 0.01 | 12/15 (80 %) | 24/27 (89 %) | 0.158 / 0.126 | **0.000 / 0.000** |
| 0.05 | 11/15 (73 %) | 21/27 (78 %) | 0.172 / 0.144 | 0.001 / 0.001 |
| **0.10** | **11/15 (73 %)** | **18/27 (67 %)** | 0.172 / 0.164 | 0.001 / 0.007 |
| 0.20 | 5/15 (33 %) | 11/27 (41 %) | 0.319 / 0.233 | 0.031 / 0.028 |
| 0.30 | 4/15 (27 %) | 6/27 (22 %) | 0.344 / 0.339 | 0.048 / 0.047 |
| 0.50 | 1/15 (7 %) | 2/27 (7 %) | 0.346 / 0.406 | 0.111 / 0.088 |

The classification separates cost cleanly — coin-flip sites average **0.000–0.007** of Sharpe at
risk against **0.13–0.41** for decisions — which is exactly why the field is worth publishing.
But the decision count is a pure function of where the bar sits, and the record has never
stated a bar. Two further facts the census exposes: the chooser's pick **beats the ladder's own
OOS median at only 10 of 27 sites**, and mean regret against the best OOS rung is **0.0568**
Sharpe (max 0.1878). The rule-8 pick is, on this corpus, worse than picking the middle rung
more often than not.

## Q3 — is the screen implementable? **No. It is a reporting field only.**

The OOS spread cannot be known when the pick is made. Its IS twin:

| pickset | n | ρ(OOS spread, IS spread) | ρ(·, IS margin) | ρ(·, IS sd) | mean IS / OOS spread |
|---|---|---|---|---|---|
| CORE5 | 15 | **+0.5571** | +0.2750 | +0.5821 | 0.2012 / 0.1851 |
| EXT9 | 27 | **+0.5391** | +0.3114 | +0.5543 | 0.2130 / 0.2006 |

Classification agreement (IS vs OOS spread, same bar): 100 % at 0.01, **60 % (CORE5) / 67 %
(EXT9) at 0.10**, 53 % / 56 % at 0.20, rising again to 80 % / 85 % at 0.50 only because almost
everything lands on one side. At the one bar where the split is informative, the tradeable
version of the screen misclassifies a third to 40 % of sites.

## Rule 8 walk-forward (PROTOCOL 8) — the price leg

Parameters fitted on 2009..2016; 2017..2026 read once. Arms: **PLAIN** (equal-weight blend of
each dial's rule-8 pick), **SCREEN@bar** (a dial whose **IS** spread < bar is replaced by its
live constant — the only decidable-at-pick-time form of the queue's proposal), **LIVE** (every
dial at its live constant). 54 arms published.

| panel | arm | OOS CAGR | OOS Sharpe | OOS MaxDD | RULES v2 OOS | SPY OOS |
|---|---|---|---|---|---|---|
| U56 | PLAIN (CORE5) | 10.89 % | 1.1734 | −15.30 % | 9.46 % / 1.2772 / −12.05 % | 15.27 % / 0.8740 / −33.72 % |
| U56 | PLAIN (EXT9) | 11.08 % | 1.1763 | −15.16 % | ″ | ″ |
| U56 | LIVE (EXT9) | 10.01 % | 1.1557 | −14.35 % | ″ | ″ |
| B136 | PLAIN (EXT9) | 8.67 % | 0.9856 | −15.09 % | 7.88 % / 1.1059 / −12.24 % | 15.33 % / 0.8767 / −33.72 % |
| SMALL483 | PLAIN (EXT9) | 8.56 % | 0.7764 | −17.25 % | 4.47 % / 0.6516 / −12.18 % | 15.33 % / 0.8767 / −33.72 % |

**KEEP paths: 4a 0 of 54 (full) and 0 of 54 (OOS); 4b on the FULL sample 0 of 54. 4b OOS: PLAIN
2 of 6, LIVE 0 of 6, SCREEN 4 of 42** — and every one of those 4 is U56/EXT9 at bars 0.01–0.10. At bars ≥ 0.20 the screen
**destroys** the pass: U56 CORE5 PLAIN clears 4b OOS, every SCREEN arm on it fails, on the CAGR
floor alone (PLAIN 10.89 % vs a 10.69 % floor; SCREEN@0.10 10.55 %). On the full-sample grid,
4a passes **0 of 174** cells and 4b **9 of 174**, 8 of them on U56 and 6 of those on the GROSS or
N dial — the record's standing exposure fact, not a spread fact.

**SCREENED − PLAIN, OOS:** median **−0.0040** Sharpe (mean −0.0020), positive in only **11 of
42** arms; CAGR **negative in 39 of 42**, median **−0.35 pp**; MaxDD shallower in 40 of 42,
median +0.58 pp. The screen is a de-grossing trade — it buys a little drawdown with CAGR, which
is the leg PROTOCOL 4b's cap is least able to price (ideas 657, 814, 861).

## What this means for PROTOCOL

Proposed for the Sunday review (**rule 8, not applied here; RULES.md untouched**):

> Every rule-8 pick must publish, beside the pick, the ladder's **OOS rung-to-rung Sharpe
> spread** and the number of rungs. A pick whose OOS spread is below 0.10 is reported as
> UNDECIDED: the ladder contained no decision and the pick carries no evidence either way.
> The spread is a reporting field only — it is not in the chooser's information set and must
> never gate a pick.

The flip rate should be dropped from published pick tables: it is dominated by the spread at
every cost rung and contributes ≤ 0.055 of R² once the spread is present, while inviting the
exact misreading that U56/LAG exhibits (0.909 flip rate, zero cost).

## Verdict

**KILL for capital.** Nothing promoted, RULES.md / scan.py / bot.py / baseline.py untouched.
The run answers the queue's question, produces a PROTOCOL proposal, and confirms that the
statistic it was asked to price is a reporting field whose tradeable form loses money.

Files: `.cells.csv` (174), `.sites.csv` (27), `.flips.csv` (324), `.correlations.csv` (6),
`.census.csv` (14), `.proxy.csv` (2), `.walkforward.csv` (54), `.screen_delta.csv` (42),
`.costladder.csv` (10), `.gates.csv` (10), `.console.txt`.
