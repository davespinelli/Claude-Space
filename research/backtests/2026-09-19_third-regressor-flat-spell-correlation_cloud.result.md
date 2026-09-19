# Idea 1558 (lane cloud, 2026-09-19) — is the THIRD REGRESSOR the CORRELATION of the FLAT SPELLS and not their COUNT?

**VERDICT: KILL the three-number hypothesis. T1, T4 and T5 all FAIL — and the run kills 1558's own
PREMISE as well: the SPY macro gate and the breadth gate do NOT differ measurably in the TIMING of
their flat spells under any of the three measures the idea named. One incidental KEEP-4b candidate
falls out, and it is a lambda-0.50 sibling of idea 1538's, not independent evidence.**

Script `research/backtests/2026-09-19_third-regressor-flat-spell-correlation_cloud.py` (imports
idea 1538's committed builders, so the 81 pairs are literally 1538's 81 pairs).
189 cells (3 panels x [36 rungs + 27 adjacent pairs at lambda 0.50]), every one published.
Two tuned parameters: third regressor {R3_CORR_ANCH, R3_CORR_OWN, R3_LEN} and bootstrap block
length {32, 63, 126}; the overlap statistic is reported BOTH ways as 1538 reported it, not chosen.
All 6 build/replay gates PASS (G1 replays the committed 2026-09-04 U56 anchor to 3.7e-05).
78s, offline, deterministic.

---

## 0. WHAT THE THIRD REGRESSOR IS

1538's T4 mis-priced the BREADTH ladder at R² -32.22 while pricing the SPY MACRO ladder at +0.7652
on nearly identical `flat_one` (0.0875 vs 0.0916 on U56). 1558's hypothesis: the two ladders differ
not in HOW OFTEN the rungs are flat apart but in WHEN. Three readings of "when", all built:

| dial-1 setting | definition |
|---|---|
| `R3_CORR_ANCH` | corr(flat_one indicator_t, the FROZEN INCUMBENT's own net return_t). The incumbent is the selection frame every rung shares, so this carries no mechanical zero-return artefact. |
| `R3_CORR_OWN` | corr(flat_one indicator_t, the pair's own mean GROSS return_t). The literal reading of the queue text; it DOES carry the artefact (a flat rung returns exactly 0), which is why both are built. |
| `R3_LEN` | mean length in trading days of a maximal run of consecutive flat_one days. |

## 1. THE PREMISE IS FALSE — the timing regressors separate L_M from L_R LESS than `flat_one` does

Mean over the 27 flat-ladder pairs, with the separation expressed in the regressor's own pooled sd:

| regressor | L_S (stop) | L_M (SPY MA) | L_R (breadth) | \|L_M − L_R\| | in sd |
|---|---|---|---|---|---|
| `flat_one` (1538's) | +0.3190 | +0.0885 | +0.1380 | 0.0495 | **0.28** |
| `R3_CORR_ANCH` | -0.0027 | +0.0069 | +0.0038 | 0.0032 | **0.26** |
| `R3_CORR_OWN` | -0.0007 | -0.0024 | -0.0040 | 0.0016 | **0.08** |
| `R3_LEN` | +1364.89 | +13.86 | +15.52 | 1.66 | **0.00** |

**Not one of the three timing measures separates the two ladders better than the COUNT already
does, and two of them separate them worse.** The correlations themselves are ~0.003-0.012 in
absolute value on every ladder: the flat-state indicator is essentially UNCORRELATED with the
book's contemporaneous return on all three mechanisms. `R3_LEN` does separate the STOP (mean spell
1,365 days — the equity stop is an ABSORBING state once the book stops compounding) from the two
market gates (~14-16 days), but that is a distinction 1538's `flat_one` already made; it says
nothing about L_M vs L_R, which is the pair the rule fails on.

## 2. T1 — a third number raises R² but nowhere near the 0.80 bar

Pooled OLS over all 81 pairs, y = `D_sharpe`, x1 = 1 − OV, x2 = `flat_one`, x3 = the third number:

| OV stat | third regressor | R²(1) | R²(2) | **R²(3)** | ΔR² 3−2 | +identity | ΔR² id | β_R3 | t_R3 | T1 |
|---|---|---|---|---|---|---|---|---|---|---|
| OV_HOLD | R3_CORR_ANCH | 0.0011 | 0.5460 | **0.5460** | +0.0000 | 0.5707 | +0.0246 | +0.0294 | +0.04 | FAIL |
| OV_HOLD | R3_CORR_OWN | 0.0011 | 0.5460 | **0.6430** | +0.0970 | 0.6810 | +0.0380 | +1.8004 | +4.57 | FAIL |
| OV_HOLD | R3_LEN | 0.0011 | 0.5460 | **0.5966** | +0.0506 | 0.6244 | +0.0279 | +0.0001 | +3.11 | FAIL |
| OV_CAP | R3_CORR_ANCH | 0.0891 | 0.5435 | **0.5436** | +0.0001 | 0.5703 | +0.0267 | +0.0718 | +0.10 | FAIL |
| OV_CAP | R3_CORR_OWN | 0.0891 | 0.5435 | **0.6347** | +0.0912 | 0.6807 | +0.0460 | +1.7640 | +4.38 | FAIL |
| OV_CAP | R3_LEN | 0.0891 | 0.5435 | **0.5888** | +0.0453 | 0.6241 | +0.0352 | +0.0001 | +2.91 | FAIL |

- **T1 FAIL at all 6 published cells.** Best 0.6430 against the 0.80 bar — the three-number fit
  closes **0.038 of the 0.254 of R² the two-number fit was short**, i.e. 15% of the gap.
- `R3_CORR_ANCH`, the reading WITHOUT the mechanical artefact, adds **exactly nothing** (+0.0000 /
  +0.0001, t +0.04 / +0.10). The +0.0970 that `R3_CORR_OWN` does add is therefore best read as the
  artefact it was built to expose: a flat rung returns 0 by construction, so the own-return
  correlation is partly a re-statement of the flat count itself.
- **T2 PASS at every cell** (max ΔR² from ladder identity +0.0460 < 0.05), and **T3 PASS at every
  cell** (worst per-ladder mean residual |t| 1.53, on L_X; 1538's convention, pooled residual sd).
  These two are 1538's surviving positives and they survive again.

## 3. T4 — LEAVE-ONE-LADDER-OUT, the test that killed 1538, is not repaired; it is made worse

| OV stat | third regressor | L_S | L_M | L_R | T4 |
|---|---|---|---|---|---|
| OV_HOLD | R3_CORR_ANCH | +0.0821 | +0.7339 | **-35.4650** | FAIL |
| OV_HOLD | R3_CORR_OWN | -0.0990 | +0.2176 | **-22.3373** | FAIL |
| OV_HOLD | R3_LEN | -0.1663 | -0.0855 | **-3.0645** | FAIL |
| OV_CAP | R3_CORR_ANCH | +0.1153 | +0.7519 | **-34.1245** | FAIL |
| OV_CAP | R3_CORR_OWN | -0.0923 | +0.2567 | **-22.1564** | FAIL |
| OV_CAP | R3_LEN | -2.5267 | -0.1744 | **-4.2358** | FAIL |

*(1538 committed: L_R -32.22, L_M +0.7652, L_S +0.1075 on OV_HOLD.)*

**T4 FAIL at all 6 cells, and the breadth ladder's misprice gets WORSE, not better, under the
regressor built to fix it** (-35.47 against 1538's -32.22). The two regressors that raise the
pooled R² (`R3_CORR_OWN`, `R3_LEN`) buy that R² by **destroying** the one ladder 1538 could already
price: L_M falls from +0.7339 to +0.2176 / -0.0855, and L_S from +0.0821 to -0.0990 / -0.1663. This
is the signature of an in-sample regressor, not of a mechanism: **the third number is fitted, not
explanatory.**

## 4. T5 — the rule still transfers across TIME, and adding a third number does not help

Coefficients fit on warm-up..2016-12-31 pair statistics ONLY; 2017-2026 read ONCE. 77 of 81 pairs
finite on both windows (4 dropped: a rung that is flat across a whole window has no Sharpe).

| OV stat | third regressor | OOS R² two | **OOS R² three** | ΔR² | T5 |
|---|---|---|---|---|---|
| OV_HOLD | R3_CORR_ANCH | 0.7317 | **0.7333** | +0.0017 | FAIL |
| OV_HOLD | R3_CORR_OWN | 0.7317 | **0.7316** | -0.0001 | FAIL |
| OV_HOLD | R3_LEN | 0.7317 | **-7.2215** | -7.9532 | FAIL |
| OV_CAP | R3_CORR_ANCH | 0.7284 | **0.7308** | +0.0024 | FAIL |
| OV_CAP | R3_CORR_OWN | 0.7284 | **0.7278** | -0.0006 | FAIL |
| OV_CAP | R3_LEN | 0.7284 | **-2.2121** | -2.9405 | FAIL |

**T5 FAIL at all 6 cells** (best 0.7333 vs the 0.80 bar), reproducing 1538's 0.7317 almost exactly.
The best third regressor buys **+0.0017 of OOS R²**; `R3_LEN`, which looked like the second-best
regressor in-sample (+0.0506), goes to **-7.22 out of sample**. Note the IS R² of every fit is only
0.16-0.21: the pair gaps of 2009-2016 are themselves much harder to fit than the full sample's.

## 5. CAPITAL ARM (protocol step 3) — both KEEP paths at all 189 cells, rule-8 walk-forward

- **Path 4a: 0/189 full and 0/189 OOS.** No cell on any of the nine ladders beats live RULES v2 on
  both halves with no worse drawdown — a ninth consecutive run with the same answer.
- **Path 4b: 37/189 full, 39/189 OOS, 34/189 BOTH** (U56 29, B136 5, **SMALL 0**).
- **Rule-8 choosers** (fitted on warm-up..2016-12-31 only, 2017-2026 read once), mean OOS Sharpe:
  **chooser 0.7599 vs DO NOTHING 0.8812 — doing nothing wins again.** The unrestricted ARGMAX-IS is
  captured on U56 and SMALL by L_X's extreme MAXVOL rungs (IS Sharpe 1.3062 / 2.0041 collapsing to
  OOS 0.6146 / 0.5091), exactly as 1538 found.

Benchmarks on the common sample: SPY 15.12%/0.8844/-33.72% full and 15.26%/0.8738/-33.72% OOS;
RULES v2 live U56 8.62%/1.2011/-12.05% full and 9.46%/1.2769/-12.05% OOS; frozen 2026-09-04
incumbent U56 15.80%/1.1537/-19.13% full and 17.32%/1.1857/-19.13% OOS.

## 6. INCIDENTAL KEEP-4b CANDIDATE — and why it is not new evidence

`L_M blend None|200 @ lambda 0.50` = a two-state gross of **0.75 above SPY's 200d MA and 0.375
below** (the same Clause M idea 1538 memo'd, one lambda deeper).

| panel | FULL CAGR/Sharpe/MaxDD | halves | OOS CAGR/Sharpe/MaxDD | 4b full | 4b OOS | reached by a legal IS-only chooser? |
|---|---|---|---|---|---|---|
| U56 | 13.99% / **1.1828** / **-17.01%** | 1.2114 / 1.1654 | 15.58% / **1.2438** / -17.01% | PASS | PASS | **NO** — IS Sharpe 1.1042 < the anchor's 1.1158 |
| B136 | 14.23% / **1.0798** / **-16.73%** | 1.3276 / 0.8824 | 14.29% / **1.0250** / -16.73% | PASS | PASS | **YES** — IS 1.1651 > anchor 1.1391; anchor FAILS 4b on both windows |
| SMALL | 6.87% / 0.5105 / -31.29% | 0.7239 / 0.3364 | 5.33% / 0.4058 / -31.29% | FAIL | FAIL | no |

Turnover 3.66x/yr (U56) and 4.00x/yr (B136), charged at 10 bps. **HONEST LIMITS:** (i) the U56 cell
is HINDSIGHT — no IS-only chooser in this run reaches it; (ii) the OOS Sharpe contrast against the
frozen anchor is **+0.0581, t = +0.74** (U56) and **+0.0071, t = +0.10** (B136) on the paired
circular-block bootstrap at L = 63 — not significant, the regime idea 1511 measured; (iii) **path
4a is FALSE** at every cell; (iv) it is the SAME macro de-gross device as 1538's committed
candidate, so it is a second reading of one book, not a second book.

## 7. SURVIVORSHIP (rule 9)

U56 and B136 are CURRENT-constituent lists and SMALL a CURRENT sub-$2B screen (665 names after the
protocol-mandated `max_1d_move >= 1.0` drop of 54 tickers) carried back to 2008/2010. Every
ABSOLUTE level above is an UPPER BOUND. What this run reads is a CONTRAST between books over the
same names on the same days, which the bias cannot manufacture.

## 8. WHAT THE RECORD GAINS

1. **1558's premise is refuted on its own terms.** The flat spells of a macro gate and of a breadth
   gate are not distinguishable by correlation with return or by spell length. The reason a
   breadth gate's flat days price differently from a macro gate's is **not** their timing against
   the book's own return, so a third scalar of that shape cannot exist.
2. **A negative on scalar summaries generally.** Three independent one-number summaries of "when
   the flat spells happen" were tried; the only one that raises pooled R² materially is the one
   contaminated by the flat count itself, and it makes T4 worse. The next attempt should either
   abandon the pooled scalar model or carry the flat-spell **distribution** (not a moment of it).
3. **1538's positives replicate exactly** under a different script and a fourth regressor: T2 PASS,
   T3 PASS, OOS R² 0.7317 reproduced to four decimals.
