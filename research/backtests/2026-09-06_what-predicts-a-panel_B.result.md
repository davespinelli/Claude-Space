# Idea 77 — what-predicts-a-panel (lane B, 2026-09-06)

**Verdict: KILL for a universe clause. The +0.710 is (a) entirely a BETWEEN-panel effect and
(b) carries no ranking information — the panel's own UN-RANKED book predicts it as well or
better. Of the three candidates the queue named, LEVEL wins, CORRELATION is nil, PERSISTENCE is
ambiguous; but LEVEL is exactly what survivorship manufactures, so the clause is not writable.**

Script: `research/backtests/2026-09-06_what-predicts-a-panel_B.py`
Console: `…_B.console.txt` · CSVs: `.properties` `.race` `.partial` `.walkforward` `.grid` `.points`

## Reproduction gate (read before anything new)

Idea 73's construction, panels, window and books were imported unchanged, so the decomposition
sits on the table it decomposes.

| check | this run | idea 73 published |
|---|---|---|
| Spearman(IS Sharpe, OOS Sharpe), 21 CAND points | **+0.710** | +0.710 |
| Spearman(IS dispersion, OOS Sharpe), 21 points | **+0.134** | +0.134 |
| harness U56/CAND20 (universe.json window) | 12.7% / 1.092 / -18.3%, halves 1.088/1.102 | 12.7% / 1.093 / -18.3%, halves 1.088/1.103 |
| harness U56/v1 | 6.5% / 0.664 / -13.8% | 6.5% / 0.666 / -13.8% |

Both Spearmans reproduce **exactly**; the two last-digit Sharpe gaps are the ones idea 81 already
logged. Common window 2011-01-13 → 2026-09-04 (3,934 days), identical days for all seven panels.
SPY on it: 14.1% / 0.862 / -33.7%, halves 0.891/0.858, IS 0.832, OOS 0.882.

## 1. Panel properties, measured on 2009-2016 only

| panel | level_S | level_C | corr | xs_mom | ts_mom | disp | n_elig | EWall_S | IS_S(n20) | OOS_S(n20) |
|---|---|---|---|---|---|---|---|---|---|---|
| STK20 | **1.284** | 24.6% | 0.333 | 0.032 | **-0.059** | 0.357 | 13.4 | **1.163** | 1.039 | **1.446** |
| BSTK100 | 1.179 | 19.0% | 0.383 | 0.027 | -0.068 | 0.259 | 69.8 | 1.076 | **1.052** | 0.938 |
| B136 | 1.077 | 15.6% | 0.357 | 0.040 | -0.069 | 0.241 | 93.4 | 0.987 | 1.025 | 0.892 |
| U56 | 0.969 | 12.8% | 0.309 | **0.056** | -0.067 | 0.266 | 37.0 | 0.862 | 0.956 | 1.168 |
| SMALL484 | 0.959 | 27.7% | **0.173** | 0.020 | -0.063 | **0.482** | 138.7 | 0.419 | 0.471 | 0.510 |
| ETF24 | 0.727 | 10.9% | 0.692 | 0.051 | -0.115 | 0.107 | 18.3 | 0.612 | 0.530 | 0.889 |
| ETF36 | 0.605 | 6.4% | 0.307 | **0.064** | -0.071 | 0.127 | 23.9 | 0.433 | 0.577 | 0.942 |

`ts_mom` is **negative on all seven panels**: per-name 12-1 momentum is a reversal signal against a
name's own next 4 weeks everywhere in this data. "Highest persistence" therefore means *least*
reversal, and the selector is reported on that reading.

## 2. The horse race (7 panels; exact permutation p over all 5,040 orderings)

| predictor | ρ (21 pts, descriptive) | ρ (7 panels, n=20) | ρ (7 panels, mean over n) | perm p (mean-n) |
|---|---|---|---|---|
| **EWall_S** (gated level, no ranking) | **+0.712** | +0.607 | **+0.857** | **0.024** |
| IS Sharpe of the ranked book | +0.617 | +0.607 | +0.821 | 0.034 |
| **level_S** (raw EW buy-and-hold) | +0.566 | +0.429 | +0.750 | 0.066 |
| ts_mom (persistence) | +0.342 | +0.357 | +0.464 | 0.302 |
| disp (idea 73) | +0.134 | +0.143 | +0.250 | 0.595 |
| **corr** | +0.173 | **-0.071** | +0.179 | 0.713 |
| xs_mom (persistence) | +0.252 | +0.393 | +0.107 | 0.840 |
| level_C (raw CAGR) | -0.031 | -0.143 | +0.107 | 0.840 |
| n_elig (panel size) | -0.523 | **-0.607** | -0.429 | 0.354 |

**Only two predictors clear a permutation test at N=7, and neither of them reads the ranking.**
`EWall_S` — the Sharpe of the panel's own equal-weight-**all-eligible** book, which does no ranking
at all — predicts the ranked book's OOS Sharpe *better* than the ranked book's own IS Sharpe does
(+0.857 vs +0.821, p 0.024 vs 0.034; +0.712 vs +0.710 on the 21 points). Idea 73's headline number
is a statement about panels, not about selection.

Partial rank correlations (n=20 column) put the same thing structurally: `level_S` controlled for
the ranked book's IS Sharpe collapses to **-0.155** (and to -0.317 controlled for `EWall_S`), while
`EWall_S` and `ISsh_n20` are mutually near-collinear (each +0.147 controlling for the other).
`corr` is negative or nil under every control (-0.591 … +0.114): **the correlation story is dead**.
`xs_mom` and `ts_mom` rise under some controls (+0.62 … +0.82) and fall under others (+0.12);
with 7 points a partial has ~4 effective degrees of freedom and none of that is interpretable.

## 3. Is +0.710 the panel or the n dial? — it is the panel

- **Between panels (N=7):** Spearman(mean IS Sharpe, mean OOS Sharpe) = **+0.857**, exact perm p = **0.0238**.
- **Within panels (3 n each):** pooled panel-demeaned Spearman = +0.494, but the IS argmax n equals
  the OOS argmax n in only **2 of 7** panels — and OOS prefers **n=20 in 7 of 7**, which in-sample
  never sees (IS picks n=5 once, n=10 four times, n=20 twice). Per-panel ρ is -0.500 in two panels.

So the predictable object is the panel. The n dial inside a panel is not predictable from its own
in-sample Sharpe; it is predictable from a constant ("take the widest n on offer"), which is idea
82's finding restated.

## 4. Rule 8 walk-forward — selectors and directions fixed before any OOS number was read

Panel selectors read at n=20 (idea 73's S3 convention); IS = 2009-2016, OOS = 2017-2026 read once.

| rule | pre-registered as | pick | OOS CAGR | OOS Sharpe | OOS MaxDD | vs SPY | vs v1 | OOS 4b | vs coin flip |
|---|---|---|---|---|---|---|---|---|---|
| S_LVL | highest IS level Sharpe | STK20/CAND20 | 13.9% | **1.446** | -12.1% | +0.564 | +0.699 | **PASS** | **+0.477** |
| S_TSMOM | highest IS ts persistence | STK20/CAND20 | 13.9% | **1.446** | -12.1% | +0.564 | +0.699 | **PASS** | **+0.477** |
| S1 | highest IS Sharpe, all 21 (idea 73) | STK20/CAND10 | 21.1% | 1.364 | -17.3% | +0.482 | +0.616 | **PASS** | +0.394 |
| **NOTHING** | incumbent universe, no selection | **U56/CAND20** | **14.4%** | **1.168** | -18.3% | +0.286 | +0.421 | **PASS** | **+0.199** |
| S_XSMOM | highest IS xs momentum efficacy | ETF36/CAND20 | 8.1% | 0.942 | -15.2% | +0.060 | +0.195 | FAIL (CAGR) | -0.027 |
| S_ISS | highest IS Sharpe at n=20 | BSTK100/CAND20 | 13.2% | 0.938 | -20.4% | +0.056 | +0.191 | FAIL | -0.031 |
| S_CORR | LOWEST IS mean pairwise corr | SMALL484/CAND20 | 7.7% | 0.510 | -26.3% | -0.372 | -0.237 | FAIL | -0.459 |
| S_DISP | highest IS dispersion (idea 73 S3) | SMALL484/CAND20 | 7.7% | 0.510 | -26.3% | -0.372 | -0.237 | FAIL | -0.459 |

RANDOM control (mean of the 7 panels at n=20): OOS Sharpe **0.969** (sd 0.286), CAGR 11.1%, MaxDD -18.2%.
SPY OOS 15.5% / 0.882 / -33.7% (4b OOS bars: DD ≤ 20.2%, CAGR ≥ 10.82%). RULES v1 OOS 7.7% / 0.747 / -13.8%.

Three readings, all uncomfortable:

1. **The two selectors that beat a coin flip picked the same panel for opposite stated reasons**
   (highest level, least reversal) — STK20, the 20 current mega-caps. One pick is not evidence for
   two mechanisms; it is one lucky panel with two labels.
2. **S_CORR and S_DISP land on the same wrong panel** (SMALL484, -0.459). Idea 73's dispersion KILL
   and this run's correlation KILL are, out of sample, the *same* error.
3. **The IS-Sharpe chooser read at n=20 loses to doing nothing by -0.230 of OOS Sharpe**
   (BSTK100 0.938 vs U56 1.168) on an IS margin of **0.013** (1.0520 vs 1.0392). Idea 73's S1 wins
   only because reading the same selector over all 21 points happened to reach STK20/n=10. This is
   an **11th instance for the idea-229 pool** of an IS chooser losing to the do-nothing control.

Sign checks (opposite extreme of each selector, labelled not selected): S_LVL^rev → ETF36 0.942,
S_XSMOM^rev → SMALL484 0.510, S_CORR^rev / S_TSMOM^rev / S_DISP^rev → ETF24 0.889, S_ISS^rev →
SMALL484 0.510. Only the `xs_mom` and `disp` axes are ordinally right at both extremes.

## 5. KEEP paths (all 35 points in `.grid.csv`; the 21 CAND rows are on the leaderboard)

4b passes on the common window: **U56/CAND10, U56/CAND20, STK20/CAND5, STK20/CAND10, STK20/CAND20**
(the last two also 4a-pass). Best row STK20/CAND20 11.8% / 1.30 / -12.1%, halves 1.18/1.41, OOS 1.446.
**Nothing is promoted.** STK20 is 20 hand-listed current mega-caps — the single most survivorship-
contaminated panel in the record — and idea 73 already parked it for that reason. This run's own
finding is why: the winning predictor is *level*, and level on a current-constituent list is
exactly what survivorship fabricates. A universe clause of the form "run the book where the names
went up in-sample" cannot be falsified on this data, so it must not be written into RULES.

## 6. Answer to the queue's question, and limits

The queue asked whether +0.710 is trend persistence, mean pairwise correlation, or unconditional
level. **It is level — specifically the panel's level after the eligibility gate (`EWall_S`), which
subsumes the ranked book's own IS Sharpe.** Correlation contributes nothing (ρ -0.071 at n=20,
negative under every control). Persistence is weak, ambiguous in sign, and its one apparent win is
the same STK20 pick as level's.

Limits, stated: 7 panels is 7 draws, and the smallest attainable exact p is 2/5040 — nothing here
is strongly evidenced, and only two of nine predictors clear p<0.05 at all. The 21-point Spearmans
are descriptive because panel properties are constant within a panel. `n_elig` (-0.607 at n=20,
surviving every control at -0.52…-0.70) is at least as strong as anything the queue named and is
perfectly confounded with both survivorship exposure and idea 78's selectivity artefact. All three
lists are current constituents, one-directional.

**RULES wording recommended: none.** Recommended to PROTOCOL instead (not a rules change, a
reporting habit): when a panel-choice claim is published, report the panel's un-ranked `EWall`
Sharpe beside it, because that number carries the whole predictable part and any excess the ranked
book shows over it is the claim's actual content. Ideas 239-241 queued.
