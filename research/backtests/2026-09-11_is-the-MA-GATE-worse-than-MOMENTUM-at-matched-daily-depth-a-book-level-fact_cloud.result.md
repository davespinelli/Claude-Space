# Idea 563 — is "the MA gate is worse than momentum at matched daily depth" a BOOK-LEVEL fact?

**Cloud lane, 2026-09-11.** Script `2026-09-11_is-the-MA-GATE-worse-than-MOMENTUM-at-matched-daily-depth-a-book-level-fact_cloud.py`.
10 bps / unit turnover (0 and 25 derived exactly off the same held path and reported), next-day
execution. IS = start..2016-12-31, OOS = 2017-01-01..end read once. 2 tuned params: **cadence
{D, W, M, Q} × gross {0.50, 0.75, 1.00}**. Panel (3) × theta (9) × arm (2) × construction (2) are
reported axes, never selected over. **1,296 books, every one in `.grid.csv`.**

## Verdict: **ANSWERED / NO — it is a ZERO-COST CAGR fact and a DAILY-CADENCE fact, and it does not become a book-level Sharpe fact. No KEEP.**

Idea 559's SELECTION leg (MOM-D ahead by 0.36 / 1.15 / 1.24 pp/yr of zero-cost CAGR, negative in
22 of 27 cells) **reproduces exactly** — and survives as a *CAGR* statement at book level: the
momentum slice earns more in **59.1%** of the 648 matched cell × dial pairs, mean **+0.384 pp/yr**.
But on the bar that decides both KEEP paths it flips: **MOM-D beats MA-THRESH on full-sample Sharpe
in only 261 of 648 pairs (40.3%)**, median dSharpe **−0.0059**, and **47.8%** out of sample. It buys
return with volatility, not with drawdown (mean dMaxDD **+0.23 pp**, i.e. marginally *shallower*).

## The contrast is a cadence fact, and it is exactly gross-invariant

| cadence (pooled) | MOM-D win share | mean dSharpe | mean dCAGR | mean dTurnover |
|---|---|---|---|---|
| D | **66.7%** | +0.0584 | +1.42 pp | +1.13 ×/yr |
| W (the live cadence) | 51.9% | +0.0070 | +0.53 pp | +0.08 ×/yr |
| M | 29.6% | −0.0233 | −0.06 pp | −0.10 ×/yr |
| Q | **13.0%** | −0.0355 | −0.36 pp | −0.10 ×/yr |

The second tuned dial does **nothing**: the win share is **0.402778 at gross 0.50, 0.75 and 1.00** —
identical to six decimals, because both arms hold the same number of names every day and gross is a
pure scale on both. And cost is not the mechanism either: the win share moves 40.1% → 40.3% → 41.8%
over 0 → 10 → 25 bps (the arms' turnover differs by only +0.255 ×/yr), so the head-to-head is
**+0.0020 of Sharpe** across the whole rung range.

By panel, MOM-D wins **52.8%** on SMALL439, **45.8%** on B136 and **22.2%** on U56 (mean dSharpe
−0.0185) — idea 559's zero-cost panel ordering (U56 least negative) **inverts** once the arms are
priced as books.

## Rule 8 (cadence and gross chosen on IS Sharpe alone, OOS read once)

108 picks. **MOM-D beats MA-THRESH out of sample in 22 of 54 cells (40.7%)**, mean dOOS Sharpe
**−0.0123**, median −0.0155. Picks beating RULES v2 OOS **35/108**; beating SPY OOS **65/108**.
The IS selector sends both arms to slow cadences (MA-THRESH picks D in **0 of 54**, Q in 31; MOM-D
picks D in 4) and to gross 1.00 (47 of 54 for MOM-D) — i.e. it walks away from the only cadence
where the momentum slice wins.

## KEEP paths

**4a 33/1,296 · 4b 36/1,296 · BOTH 0.** Split by arm: 4a MA-THRESH 13 / **MOM-D 20** (all DEGROSS —
the one column where the momentum slice is genuinely ahead), 4b **MA-THRESH 21** / MOM-D 15.
**SMALL439 passes nothing, 0 of 432.** Binding 4b bars: CAGR 762, DD 722, H2 613, OOS 610, H1 552.
Only **5 of the 108 rule-8 picks** are 4b passers.

**No new KEEP-candidate, no memo.** The best book in the run — U56 / θ=0 / MA-THRESH / DEGROSS /
monthly / gross 1.00: CAGR **11.93%**, Sharpe **1.2133**, MaxDD **−15.54%**, halves 1.2610 / 1.1699,
OOS Sharpe **1.2737** — is the record's **already-memo'd and already-PARKed** book
(`2026-09-11_u56-v2band-gross100_4b_cloud_MEMO.md`: 11.55% / 1.2067 / −15.70%, OOS 1.2827) reached
from a different dial setting: the same U56 above-the-200d-MA de-grossing book at gross 1.00, without
the ±3% hysteresis band and at monthly instead of weekly. Idea 742's objection applies to it
unchanged — the equal-weight U56 basket runs 17.94% CAGR, so the 4b floor is 12.56% and **this book
misses it by 0.63 pp/yr**. It fails 4a on H2 (1.1699 against RULES v2's 1.1806).

## Gates (pre-registered)

| gate | result |
|---|---|
| G0 `fast_run` vs `engine.backtest`, every panel at D and W | **0.000e+00** PASS (bar 1e-12) |
| G1 derived cost rung vs a fresh run at 25 bps | **0.000e+00** PASS (bar 1e-15) |
| G2 daily depth match, reproducing idea 559's committed `dk_md` | **3.225e-05 — FAIL at the flat bar, fully localised: B136 9.194e-17, SMALL439 5.378e-17, U56 3.225e-05.** The match is exact on **98.31%** of (cell, day) pairs; the clip is a history-length fact (12-1 momentum needs 252 closes, the 200d MA needs 200, so a name aged 200–251 days is gateable but not rankable) and it bites only at the loosest thresholds — idea 559's own `.match.csv` carries the same column. |
| G3 reproduction of idea 559's MOM-D/W/FULL SELECTION, 27 cells | **2.880e-01 — FAIL at the flat bar, same localisation: B136 2.220e-14, SMALL439 2.220e-14, U56 2.880e-01.** Panel means reproduce at B136 −1.1499 / −1.1499 and SMALL439 −1.2430 / −1.2430 **exactly**, U56 −0.3642 vs −0.3167, and the headline count **22/27 negative reproduces exactly**. The residue scales inversely with book breadth (θ +0.30, 2.3 names: 2.88e-01 → θ −0.40, 52.6 names: 1.21e-04), the signature of a **price restatement** in `data/prices.csv`, which is re-downloaded daily while `prices_broad`/`prices_small` are static — idea 560's G2b finding, same cause. No number in this run depends on idea 559's file. |
| G4 target-gross identity on the exactly-matched days | **0.000e+00** PASS (bar 1e-12) |

## Survivorship

B136 and SMALL439 are **current constituents only** (44 SMALL names with `max_1d_move >= 1.0`
dropped first). CAGR levels are inflated and neither KEEP column is immune. The head-to-head is an
arm-minus-arm difference inside one panel at identical daily depth, where the bias very largely
cancels; the KEEP columns and the rule-8 levels are not protected.

## Follow-ups proposed

* The **daily** cell is where MOM-D wins (66.7%, +0.058 Sharpe) and where the IS selector never
  goes — is that a real edge the selector is missing, or the turnover the selector is right to avoid?
* MOM-D takes **20 of the 33 4a passes**, all DEGROSS. The 4a path is where the momentum slice is
  ahead; the record has spent its attention on 4b. Worth one run at the 4a column directly.
