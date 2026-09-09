# Idea 543 — is-the-BAND-a-TURNOVER-dial-with-a-free-SHARPE (cloud, 2026-09-09)

**ANSWERED / KILL for the "free Sharpe" reading — the band's turnover saving is real and large,
but no band is distinguishable from the live 0.03 on net Sharpe at the PROTOCOL rung, and the
argmax band is panel-, construction- and cost-dependent. RULES v2 unchanged.**

## Design
Two dials only: **band** (11 values 0.00…0.15) × **cost rung** (0/10/25/50 bps). Everything else
held at the live setting — cadence W, gross 0.75, next-day execution, 200d MA band with
hysteresis (`baseline.band_state`), IS ≤ 2016-12-31 / OOS ≥ 2017-01-01 (PROTOCOL 8).
DEGROSS is the live construction and the only one a KEEP may be claimed on; RESPREAD is a
reported control. Panels U56 and B136 required, SMALL439 reported. 264 book-rungs, all reported
in `.grid.csv` / `.console.txt`.

Gates: **G1** vectorised runner vs `engine.backtest` 1.7e-17; **G2** band 0.03/gross 0.75/DEGROSS
bit-identical to `baseline.rules_v2_weights` (0.000e+00); **G3** reproduces idea 542's committed
head-to-head dSharpe on all three panels to 6.9e-17.

## What the numbers say

**B1 — the argmax.** At 10 bps under the live DEGROSS form the live 0.03 **is** the net-Sharpe
argmax on U56 (1.2108) but **not** on B136 (0.10 wins, 1.1283 vs 1.1078) and not on SMALL439
(0.15 wins, 0.6721 vs 0.5710). Across all 24 (panel, construction, rung) cells the live band is
the argmax in **3 / 24**. At 50 bps it stops being the argmax even on U56 (0.10 wins by 0.0229).

**B2 — the ridge is narrow, not flat.** Mean bands within 0.02 Sharpe of the argmax: **2.00 of
11**; mean Sharpe span across the band axis **0.1686**. The band axis moves net Sharpe by real
amounts — the premise "an arbitrary point on a flat ridge" is wrong — but the live band sits
inside that tolerance ridge in only 4 / 24 cells.

**B3 — but the winner is not distinguishable from the incumbent.** Paired circular-block
bootstrap (2000 draws, 21d blocks, seed 0), 10 bps, DEGROSS: B136 argmax 0.10 beats 0.03 by
dSharpe **+0.0205 [−0.0808, +0.1332]** (P(better) 0.69); SMALL439 argmax 0.15 by **+0.1011
[−0.0041, +0.2078]** (0.97); U56's argmax *is* 0.03. Every required-panel CI straddles zero.

**B4 — the turnover leg is deterministic and monotone.** Turnover x/yr, DEGROSS: U56 3.15 (band
0.00) → 1.79 (live 0.03) → 0.84 (0.15); B136 3.33 → 2.02 → 0.93. The band therefore cuts
turnover by 73% end-to-end and 53% from the live point. The implied **breakeven cost rung** at
which a wider band overtakes 0.03 is **30.1 bps** (U56, band 0.10) and **25.9–33.7 bps** for the
B136 bands that overtake at all — i.e. above the PROTOCOL 10 bps rung and above the 25 bps
sensitivity rung on U56. Below 0.03, every narrower band is worse at *both* 0 and 50 bps: the
band's first three percentage points are paid for by gross return, not by costs.

**B5 — rule 8 (walk-forward).** Band chosen on IS Sharpe only, per rung, per panel and pooled
over the two required panels; OOS read once. The IS surface peaks at **0.10** on both required
panels at every rung — the IS-chosen band equals the live 0.03 in **0 / 40** cells. The pooled
DEGROSS pick (0.10) OOS at 10 bps: U56 CAGR **9.24% / Sharpe 1.2164 / MaxDD −12.19%**, B136
**8.44% / 1.1110 / −14.53%**, against SPY OOS 15.38% / 0.8786 / −33.72% and RULES v2 OOS
9.51% / 1.2817 / −12.05%. So the walk-forward pick beats SPY on OOS Sharpe on both required
panels and **loses to the live book** on both (32/40 beat SPY, 2/40 beat RULES v2, 8/40 clear
full-sample 4b — the 8 are all RESPREAD/U56).

**B6 — both KEEP paths.** 4a 5 / 264, 4b 53 / 264, both 0 / 264. Every 4a "pass" is the incumbent
band (0.00–0.03) on U56 DEGROSS at 0–10 bps, clearing the baseline only because the baseline is
computed on the SPY-*including* 56-name panel while the book runs on the 55-name panel — a
constituent artefact, not an improvement. 18 / 88 (band, construction, rung) cells clear 4b on
**both** required panels and **all 18 are RESPREAD**, the control form; the live DEGROSS form
clears 4b on zero cells on B136 at 10 bps and fails on **CAGR** in 91 of the 211 failing cells.
SMALL439 clears 4b nowhere (0 / 88).

## Verdict
**KILL** for a rule change and for the queue's "free Sharpe" premise. The band is a genuine
turnover dial (−53% from the live point to 0.10, −73% end to end), but the Sharpe it buys is not
free in either direction: narrower bands lose gross return, and wider bands only overtake the
live 0.03 above ~30 bps of cost. At the PROTOCOL 10 bps rung the live 0.03 is the U56 argmax and
is inside every required-panel bootstrap CI, so the record cannot distinguish it from its
alternatives; rule 8 prefers 0.10 in-sample and that pick loses to the live book out-of-sample.
0.03 is defensible as a live setting and is **not** demonstrably optimal — which is the honest
reading, not a promotion.

## Caveats
SURVIVORSHIP: U56, B136 and SMALL439 are current constituents only (no delistings), so every
CAGR level here is inflated and both KEEP columns inherit that whole. SMALL439 drops the 44
tickers with `max_1d_move >= 1.0` in `data/small_meta.csv`. The RULES v2 comparand is computed on
U56-with-SPY and reindexed onto each panel (idea 299/542 convention), which is what makes the
five 4a passes above artefactual.
