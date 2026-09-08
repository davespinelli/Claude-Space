# Idea 468 — is phi a standalone de-grossing instrument? (cloud, 2026-09-08)

**Verdict: ANSWERED. phi is a real, cheap and by far the most REACHABLE de-grossing
instrument on idea 74's menu — and idea 244's headline size does NOT transfer to it.
One PARK by-product, no KEEP, no RULES change.**

Script: `research/backtests/2026-09-08_is-phi-a-standalone-de-grossing-instrument_cloud.py`
(660 arm-rows = 3 panels x 2 books x 9 families x 6 levels x 2 cost rungs, plus 12 controls;
every grid point in `.grid.csv`, the menu in `.menu.csv`, the attribution in `.matched.csv`,
rule 8 in `.walkforward.csv`, both KEEP paths in `.keep.csv`).

## Construction (the thing that was never priced)
For a base book `w` and a gate mask `M`, `phi_t = sum(w*M)/sum(w)` — the share of the book's
own weight clearing the gate, the un-ranked analogue of idea 244's `n_held/n`. Three objects
share that gate: **GATE** (re-spread, SELECTION only), **PHI** (the ungated book scaled by
`phi_t`, TIMING only) and **DGG** (gated weight to cash, BOTH), with the exact identity
`DGG = GATE * phi_t * (sum_w/GROSS)` — max |dw| **6.9e-18** over 36 cells, and the last factor
is exactly 1 on the queue's own un-ranked EWALL0 book (0 rows after warm-up where it is not).
PHI and DGG carry an **identical target gross every day** (max |d| 1.1e-14), so the pairing is
matched-gross by construction, not by fitting.

## 1. The menu (pp of CAGR surrendered per pp of MaxDD bought; lower = cheaper)
* **phi beats the de-gross reference lever in 40 of 40 reachable cells (100%)** — u56 0.519-0.599
  vs dg 0.612-0.642; broad136 0.430-0.517 vs 0.581-0.616; SMALL439 0.230-0.240 vs 0.283-0.300.
* **phi beats the cheapest GATE in only 6 of 17 cells (35.3%)** where a gate reaches at all —
  the 3% and 12% bands remain the cheapest shallow insurance on the large-cap panels
  (u56 EWALL0 band(0.12) **-0.255** at T=2pp, i.e. free).
* **REACHABILITY is where phi wins**: over the 60 (panel, book, cost, budget) menu cells, phi
  and phib reach **40**, dgg 50, dg 60, ddctl 47 — but 200d only **13**, abs **11**, band **10**,
  stop **11**. Max MaxDD a family's whole ladder can buy, averaged: phi **12.8 pp** / phib
  **13.0 pp** (max 32.1) against 200d 2.67, abs 2.64, band 1.93, stop 2.64 pp. **No gate reaches
  8 pp anywhere; phi does on 5 of 6 panel x book cells.**
* phi is cheaper than the cheapest instrument on idea 74's WHOLE menu in 26 of 40 cells (65%);
  it never wins on u56/CAND20 (ddctl owns the shallow budgets there) and always wins on
  SMALL439/EWALL0 (10/10).

## 2. Matched-gross attribution — the gate's SELECTION is worth negative
Same gate (MA200), same realised gross path, 12 (panel, book, cost) cells:

| | mean dCAGR | mean dSharpe | cells + | mean dMaxDD | mean OOS dSharpe | cells + |
|---|---|---|---|---|---|---|
| TIMING alone (PHI − control) | −3.04 pp | **+0.0044** | 4/12 | +8.46 pp | **+0.0199** | 6/12 |
| SELECTION at matched gross (DGG − PHI) | −0.41 pp | **−0.0458** | 2/12 | +0.24 pp | **−0.0295** | 1/12 |

So the de-grossed MA gate is, to a good approximation, **the phi overlay plus a selection
overlay that loses money**: dropping the below-MA names rather than holding everyone at the
same exposure costs 0.046 of Sharpe and 0.030 of OOS Sharpe on average.

**But idea 244's magnitude does not transfer.** Its LEVEL-vs-TIMING split put the overlay at
+0.0480 full-sample and +0.0587 OOS Sharpe on 37 and 36 of 42 ranked (panel, n) cells. Priced
standalone on the un-ranked book the same object is worth **+0.0044 / +0.0199 on 4 and 6 of 12
cells** — an order of magnitude smaller and no longer a majority effect. Idea 244's number is a
property of phi *inside a ranked count sweep*, not of phi.

## 3. Rule 8 (instrument AND level chosen on 2009-2016, 2017-2026 read once)
47 live (panel, book, cost, budget) cells. IS-cheapest is a phi arm in **15 of 47**; the OOS
oracle is a phi arm in **17 of 47** — so phi is picked about as often as it deserves. But the
menu itself does not walk forward: the IS-cheapest instrument stays OOS-cheapest in **1 of 47**
cells and the mean OOS xrate is **0.258 CHEAPER** than its IS quote (insurance was systematically
over-priced in sample). The IS pick still reaches its budget OOS in 46 of 47. phi picks deliver
mean OOS Sharpe 0.761 / CAGR 5.8% / MaxDD −16.0% against non-phi picks' 0.967 / 8.2% / −14.9%
(phi is picked mostly on SMALL439, where every arm is weak).

## 4. KEEP paths (both rungs, 660 arm-rows, 4a vs LIVE RULES v2, 4b vs SPY)
**4a 13/660** (dg 3, phi 3, phib 7 — every 4a passer is an exposure instrument, no gate);
**4b 77/660**; **0 rows pass both.**

PARK by-product (not a KEEP): **u56 / CAND20 / phib(k=1)** — @10 bps 14.88% / **1.1904** /
−19.80%, halves 1.2755 / 1.1349, OOS **1.1967**; @25 bps 13.36% / 1.0821 / −19.95%, halves
1.1516 / 1.0379, OOS 1.0988. It clears 4b at BOTH rungs and beats its own un-overlaid control
(1.1816 / −21.92% / OOS 1.1746) by +0.0088 full and +0.0221 OOS Sharpe. PARK, not KEEP, because
(a) the control already clears every 4b bar except **DD**, so the pass is bought on the drawdown
cap with 0.43 pp of margin (idea 461's pattern); (b) it clears in 1 of 6 panel x book cells and
fails 4a (H2|DD); (c) rule 8's own chooser keeps its instrument only 1 time in 47.

## Caveats
`dg` is priced with idea 66's LEVER convention (scale realised return and turnover by g), the
parent's own convention. Reproduction of idea 74's committed grid on 144 shared arm-rows:
max |dCAGR| 2.9e-05, max |dMaxDD| 4.1e-07 — not bit-exact because `data/prices.csv` was
rewritten on 2026-09-08 (commit 26d0089) after idea 74 ran.
SURVIVORSHIP: all three panels are current constituents (PROTOCOL 9); SMALL439 is the sub-$2B
screen's survivors since 2010 with the 44 `max_1d_move >= 1.0` tickers dropped. Levels are
upward-biased and crashes are shallower than they were, so every instrument here is priced in a
world with less drawdown to buy; the exchange rate is a within-cell ratio against the same
control on the same days, which cancels most but not all of that bias.
