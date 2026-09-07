# Idea 366 — is DDCTRL (the equity stop) retirable as a family? — **KILL of the family** (2026-09-07, lane C)

Script: `2026-09-07_is-DDCTRL-retirable-as-a-family_C.py` · grid `…_C.grid.csv` (522 rows) ·
walk-forward `…_C.walkforward.csv` · console `…_C.console.txt`

## Question
Idea 351 priced the equity stop at a median **-1.58** pp of drawdown bought per pp of CAGR given up
with a **negative** median dDD, using ONE re-entry rule (immediate). Does **any** re-entry rule flip
the sign, at the same trigger levels, on the same two books?

## Design (2 tuned params, all points reported)
- trigger X ∈ {0.10, 0.15, 0.20, 0.25} — idea 351's dial, unchanged
- re-entry lag k ∈ {0, 1, 3, 5, 10, 21, 63} trading days of confirmation (k=0 ≡ idea 351)
- reported axes: n ∈ {3, 20}, panel ∈ {U56, B136, SMALL439}, rung ∈ {0, 10, 25} bps
- 4·7·2·3·3 = **504 overlay points + 18 controls, every one written to the grid CSV**

Reproduction gates, asserted before any new number: rung identity vs `engine.backtest` **0.000e+00**;
U56 NONE n=3 @10 bps 21.85%/1.036/-25.81% (1.014/1.061) and n=5 16.52%/0.950/-21.58% vs published;
**all 24 k=0 cells reproduce idea 351's committed DDCTRL grid to 4.4e-16.**

## Answer: NO. No re-entry rule flips the sign.
Pooled median ratio @10 bps by lag (k=0 → 63): **-1.582 / -1.582 / -0.915 / -1.083 / -1.073 / -1.103 /
-0.484**. Every lag is negative at every rung (0 bps best -0.433, 25 bps best -0.760). Median **dDD_pp
is negative at all seven lags** (-1.622 … -1.893): the median stop still *deepens* the drawdown it was
bought to fix, however long it waits to re-enter.

The single decisive number: **dSharpe > 0 in 0 of 168 points @10 bps**. Not one (panel, n, X, k)
combination improves risk-adjusted return over its own un-stopped control. dDD_pp > 0 in 30/168,
ratio > 0 in 30/131 priceable.

## Where the lag does help, and why it is not a rescue
Taking the max over 7 lags per cell, 12 of 24 (panel, n, X) cells have *some* lag with ratio > 0, and
9 of those were negative at k=0 — but that is a selection over 7 draws, and rule 8 prices it:

- **Rule 8** (menu = control + 28 arms, chosen on 2008–2016 @10 bps): the ruler chooser beats
  do-nothing on **0/6** books (mean -0.173, mean regret -0.202); the IS-Sharpe chooser **0/6**
  (mean -0.055, regret -0.084) and it picks the control in 5/6. Worst pick SMALL439 n=20
  X0.10_k10: OOS Sharpe **-0.143** vs the control's +0.487.
- **OOS-only** exchange rate is negative at every lag (median -0.965 / -0.965 / -0.453 / -0.365 /
  -0.354 / -0.603 / -0.480; positive in 5–8 of ~19 cells).
- **Numeraire bar** (idea 351): only **4 of 168** points @10 bps beat their own book's |MaxDD|/CAGR,
  and **0 of those 4 cost ≤0.01 of Sharpe** — the free gross dial dominates all of them.

## KEEP paths
**4a 0/168 at every rung.** 4b 40/168 @0 bps, **23/168 @10 bps**, 0/168 @25 bps — but all 23 are
U56 n=20, **14 of them never fire at all** (days_out = 0, i.e. they are the control, which itself
passes 4b on that book), and only 3 have a positive exchange rate. No 4b pass is attributable to the
stop.

## Mechanism
The lag does what it says — mean firing episodes 29.3 → 5.7 and switches 58.5 → 11.1 from k=0 to
k=63, days-out 16.1% → 28.4% — so it buys fewer, longer exits. It just does not pay: rank
corr(lag, dSharpe) = **-0.031**, corr(lag, dDD_pp) = +0.101. Waiting longer to re-enter trades one
sell-the-bottom episode for a longer absence from the recovery.

## Proposed PROTOCOL clause (for Sunday review; PROTOCOL.md NOT edited by this run)
> *No equity stop.* An overlay that cuts exposure on the book's own drawdown is not admissible as a
> drawdown instrument: across 504 points (4 triggers × 7 re-entry rules × 2 books × 3 panels × 3
> rungs) it improves Sharpe at **zero** points, its median exchange rate is negative at every
> re-entry rule and every cost rung, and rule 8 rejects it on 6 of 6 books. Use the gross dial.

## Caveats
Current-constituent panels (survivorship) — drawdown *levels* are optimistic; the ruler reads
differences against a same-panel control. SMALL439 starts 2010-01-04, so its halves differ in
calendar from U56/B136. A longer k is strictly a later re-entry and cannot help a V-shaped recovery;
that asymmetry is the hypothesis priced here, and it is what the numbers reject.
