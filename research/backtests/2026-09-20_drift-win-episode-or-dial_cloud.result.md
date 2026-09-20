# Idea 2022 (lane cloud, 2026-09-20) — is the DRIFT trigger's matched-turnover win a DRAWDOWN-TIMING fact or a COST fact?

**Verdict: ANSWERED / the 263-of-263 is a DRAWDOWN-TIMING fact concentrated in 24 trading days, and it is NOT a cost fact. Idea 1799's V2 dominance must be restated. No new book; the standing 4b candidate survives on the FULL tape but loses its matched-turnover edge outside 2020.**

Script `2026-09-20_drift-win-episode-or-dial_cloud.py`; gates **10/10**. Replication gate **G5 reproduces 1799's V2 headline exactly: 263 of 263, mean +0.0596.**

## 1. The win is 24 days wide

The same 263 pairs (keyed on panel x target x T_trade x h, so a tape cannot silently change the population), 10 bps, OOS 2017-2026:

| tape | days removed | wins | mean d OOS Sharpe | mean d OOS MaxDD | mean d OOS CAGR |
|---|---|---|---|---|---|
| FULL | 0 | **263/263 (100.0%)** | **+0.0596** | +4.07 pp | +0.31 pp |
| CRASH_PT (2020-02-19 -> 03-23) | 24 | 188/263 (71.5%) | **+0.0066** | +0.66 pp | **-0.26 pp** |
| CRASH_WIDE (2020-02-19 -> 04-30) | 51 | 210/263 (79.8%) | +0.0126 | +0.65 pp | -0.06 pp |

Removing **24 of ~2,440 OOS trading days (1.0%)** removes **89.0%** of the mean edge; the wider window removes 78.4%. Every arm moves the same way (U56/M is the weakest survivor at 28/44, mean +0.0005). V1 verdict **PARTIAL** by the pre-stated bands (71.5% and 79.8% fall between the 50% EPISODE bar and the 90% NOT-AN-EPISODE bar) — but the *magnitude* is unambiguous: what is left outside the crash is a tenth of what was published.

## 2. It is not a cost fact

Flat across the whole cost ladder on the FULL tape, same 263 keys:

| cost | wins | mean d OOS Sharpe |
|---|---|---|
| 0 bps | 263/263 | +0.0603 |
| 10 bps | 263/263 | +0.0596 |
| 25 bps | 262/263 | +0.0586 |
| 50 bps | 261/263 | +0.0569 |

The edge is already fully present at **zero cost** and *shrinks* as costs rise. Saved turnover is not the mechanism; the mechanism is the gross path.

## 3. Which leg carries it — drawdown, and only drawdown

| tape | d OOS MaxDD | d OOS CAGR | d OOS Sharpe win |
|---|---|---|---|
| FULL | +4.07 pp (win 98.5%) | +0.31 pp (win 87.5%) | 100.0% |
| CRASH_PT | +0.66 pp (win 88.6%) | **-0.26 pp** (win 54.0%) | 71.5% |
| CRASH_WIDE | +0.65 pp (win 88.2%) | -0.06 pp (win 59.3%) | 79.8% |

The drawdown credit survives in **sign** (88% of pairs) but loses 84% of its **size**; the CAGR credit goes *negative*. Outside 2020 the drift trigger is a small, mostly-unpaid drawdown shaver that costs a little return.

## 4. The published sweep was never resolvable

Paired moving-block bootstrap, B = 1000, seed 20260922, all 13 cells of an arm resampled on the **same** day blocks so the difference is genuinely paired; 1799's estimator reproduced exactly (each calendar rung's Sharpe re-read on the resampled days, then linearly interpolated at the drift book's realised turnover, turnover held fixed as a design quantity).

| tape | block | mean SE | mean \|t\| | max \|t\| | 95% CI excludes 0 |
|---|---|---|---|---|---|
| FULL | 21 | 0.0436 | 1.49 | 3.07 | **61/263 (23.2%)** |
| FULL | 63 | 0.0445 | 1.51 | 3.22 | 59/263 (22.4%) |
| CRASH_PT | 21 | 0.0311 | 0.94 | 2.77 | 26/261 (10.0%) |
| CRASH_PT | 63 | 0.0295 | 1.02 | 3.19 | 40/261 (15.3%) |
| CRASH_WIDE | 21 | 0.0283 | 0.90 | 2.59 | 26/262 (9.9%) |
| CRASH_WIDE | 63 | 0.0276 | 0.96 | 3.11 | 36/262 (13.7%) |

Even on the FULL tape **77% of the 263 cells cannot reject zero**. "263 of 263" is 263 point estimates of one shared event, not 263 independent wins. Both block lengths agree.

## 5. Capital arm — both KEEP paths at every cell, rule 8 on every tape

All 420 cells x 3 tapes x 4 costs published in `.grid.csv.gz`.

| tape | 4b FULL+OOS @10bps | of which DRIFT | 4a | legal IS picks clearing 4b | arms reached (CAL / DRIFT) |
|---|---|---|---|---|---|
| FULL | 187/420 | 152 | 40 | 10/48 | 3/6 / 3/6 |
| CRASH_PT | 80/420 | 62 | **0** | 7/48 | 2/6 / 2/6 |
| CRASH_WIDE | 89/420 | 67 | **0** | 9/48 | 4/6 / 2/6 |

Rule 8 (IS 2009-2016 chooses `(t,h)` or `(t,R)`; 2017-2026 read exactly once). **DRIFT never reaches more arms than CALENDAR on any tape** — 3/6 vs 3/6, 2/6 vs 2/6, 2/6 vs 4/6 — reconfirming 1799's own V1 KILL on reachability.

**1799's standing KEEP-4b cell (U56, T=M, `t=0.16, h=0.12`, C_ISSHARPE):**

| tape | full CAGR / Sharpe / MaxDD | H1 / H2 | OOS CAGR / Sharpe / MaxDD | 4b | matched d OOS Sharpe (bootstrap t, 95% CI) |
|---|---|---|---|---|---|
| FULL | 15.62% / 1.2451 / -18.16% | 1.29 / 1.20 | 16.36% / 1.2810 / -18.16% | **PASS** | +0.0735 (t +1.16, CI -0.054 .. +0.187) |
| CRASH_PT | 16.94% / 1.3582 / -18.16% | 1.29 / 1.42 | 18.80% / 1.4892 / -18.16% | FAIL (L4_DD) | **-0.0123** (t -0.30, CI -0.099 .. +0.066) |
| CRASH_WIDE | 16.63% / 1.3362 / -18.16% | 1.28 / 1.39 | 18.26% / 1.4502 / -18.16% | FAIL (L4_DD) | -0.0013 (t -0.03) |

vs SPY FULL 15.12% / 0.8843 / -33.72% (OOS 15.26% / 0.8737 / -33.72%) and live RULES v2 8.62% / 1.2010 / -12.05% (OOS 9.46% / 1.2766 / -12.05%).

**Stated honestly: the 4b FAIL on the excised tapes is a BAR SHIFT, not a book failure.** The book's own MaxDD is unchanged at -18.16% on all three tapes; what moves is SPY's, from -33.72% to -24.50%, which tightens the 4b cap from -20.23% to -14.70%. The same shift is what zeroes 4a on both excised tapes. So the excised 4b/4a *census* is not a clean read on the book. The **matched DRIFT-vs-CALENDAR contrast (sections 1-4) is immune to it** — it is book-against-book on the same tape with only the refresh trigger moved — and that contrast is where the 263-of-263 lives.

## 6. What this means for the record

1799's V2 should be read as: *at 10 bps a drift trigger bought a better 2020 than a turnover-matched calendar, and outside that quarter the two are indistinguishable (mean +0.007, 77-90% of cells unresolvable).* 1799's own V1/V3 KILLs on reachability stand and are reinforced. The standing 4b candidate is not withdrawn — it clears 4b FULL+OOS on the real tape, and crashes are part of the real tape — but its **claimed advantage over a cheaper calendar refresh is a single-episode, unresolvable one**, and it should not be quoted as a 263-of-263 dominance.

## Survivorship

U56 / B136 are CURRENT-constituent lists; SMALL665 is a CURRENT sub-$2B screen with 54 tickers (`max_1d_move >= 1.0`) dropped first. Every CAGR and drawdown LEVEL above is optimistic and both 4b bars are easier here than on a point-in-time panel. The DRIFT-vs-CALENDAR contrast is same-tape / same-names / same-grid, so it is first-order immune; the PASS COUNTS are not. SMALL-panel numbers are not comparable with pre-2026-09-20 SMALL results (cache grew 439 -> 665 names).

## Dials

Nothing new tuned. `t` and `h` are 1799's two inherited dials. REPORTED, not tuned: crash window {PT, WIDE}, block length {21, 63}, trade cadence {W, M}, panel {U56, B136, SMALL665}, cost {0, 10, 25, 50} bps. Every grid point published.
