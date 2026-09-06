# Idea 287 — does the MA200-only book pass 4b on a THIRD large-cap panel? — **ANSWERED / KILL**

2026-09-06, cloud lane. Script `2026-09-06_MA200-only-book-on-a-third-large-cap-panel_cloud.py`;
outputs `.grid.csv` (36 fixed-panel cells), `.draws.csv` (500 random panels), `.walkforward.csv`,
`.console.txt`.

## Setup

Book held fixed at idea 56's by-product: composite score (no vol scaler), eligibility `px > 200d MA`
only, top-n equal weight at `gross/n` each (de-gross to cash), weekly, 10 bps, decided at close t and
applied at t+1, first 260 rows dropped. Tuned parameters (≤2): `n ∈ {10,20,30}`, `gross ∈ {0.50,0.75,1.00}`;
all 9 points reported on every fixed panel. Anchor `(n=20, gross=0.75)` pre-registered.

Panels — U56 (55 names, where the pass was found), B136 (135, where it failed), **B100** (the 100
longest-history names of B136; a history-length stand-in for "BSTK100", *not* a capitalisation
ranking — this repo has no cap column for B136), **BXU80** (B136 \ U56, the 80 names U56 does not
contain), plus **300 random 55-name and 200 random 100-name draws** from B136's 135 names (seed 287,
anchor book only, no per-draw selection). U56 ⊂ B136 is verified in-script, the trading-day index is
identical on every panel, and SPY is the same never-tradable series everywhere — so the two 4b LEVEL
bars are constants: **MaxDD ≥ −20.23%, CAGR ≥ 10.66%** (SPY 15.23% / 0.8890 / −33.72%, OOS 0.8820).

## 1. Reproduction and the two new fixed panels

| panel | CAGR | Sharpe | MaxDD | H1 / H2 | OOS Sharpe | 4b | first-failing bar |
|---|---|---|---|---|---|---|---|
| U56 | 14.40% | 1.1578 | −19.09% | 1.222 / 1.118 | 1.1810 | **PASS** | – |
| B136 | 14.74% | 0.9946 | −24.00% | 1.195 / 0.841 | 0.9208 | fail | DD |
| B100 | 13.72% | 0.9950 | −21.58% | 1.198 / 0.829 | 0.9029 | fail | **H2** |
| BXU80 | 11.43% | 0.8776 | −21.10% | 1.098 / 0.679 | 0.8021 | fail | **H2** |

The queue's published numbers reproduce exactly (U56 14.4%/1.158/−19.1%, OOS 1.181; B136 −24.00% vs
the −20.23% bar). The third and fourth panels **do not pass**, and they refute the queue's own framing:
B100 and BXU80 fail on **H2 Sharpe**, not on the drawdown cap, i.e. off U56 this book loses to SPY in
the second half before the DD cap ever gets a say. `4a 0/36` — the live RULES v2 book is unbeaten
again (v2 Sharpe 1.2127 / 1.1078 / 1.1152 / 0.9959 by panel, MaxDD ≈ −12% on all four).

Gross is confirmed Sharpe-neutral (max |ΔSharpe| across gross at fixed n: 0.0030 U56, 0.0080 B136,
0.0068 B100, 0.0079 BXU80) while moving MaxDD at n=20 from −13.0% to −24.9% on U56 — so the two 4b
level bars are the only thing that dial touches, and a pass bought by de-grossing is idea 288's
de-gross null, not a book result. Stated before the grid was run, not after.

## 2. The null: U56's pass is a 61% coin, and the DD cap is a function of PANEL SIZE

Anchor book, random draws from the same 135-name pool:

| | median MaxDD | median Sharpe | median OOS Sharpe | **4b pass rate** | DD cap fails |
|---|---|---|---|---|---|
| k=55 (300 draws) | −19.30% | 1.0076 | 1.0139 | **61.3%** (184/300) | 21.7% |
| k=100 (200 draws) | −21.85% | 1.0115 | 0.9630 | **5.5%** (11/200) | 92.0% |
| k=135 (B136 itself) | −24.00% | 0.9946 | 0.9208 | fail | yes |

Two things follow, and they are the result:

1. **The U56 pass carries almost no information.** A random 55-name large-cap panel passes 4b with
   this book **61.3%** of the time. U56's MaxDD (−19.09%) sits at the **58th percentile** of its own
   null — 41.7% of random 55-name panels have a *shallower* drawdown. Finding one panel that passes
   and one that fails was never evidence about the book.
2. **Where the DD cap binds is set by the pool size k, not by which names are in it.** At the fixed
   anchor the median MaxDD is monotone in k (−19.30% → −21.85% → −24.00% for k=55/100/135) and the
   DD-cap failure rate goes 21.7% → 92.0% → 100%. With n held at 20, a larger pool means a more
   selective book (top-20 of 55 = 36% of the pool, top-20 of 135 = 15%), and the more selective book
   is the deeper-drawdown book. `corr(number of U56 names in a draw, MaxDD)` is **+0.037** (k=55) and
   **+0.013** (k=100) — panel *identity* explains essentially none of the drawdown, panel *size* explains
   the ordering.

Where U56 *is* special is the return axis, not the risk axis: Sharpe 1.1578 is the **97th** percentile
and OOS Sharpe 1.1810 the **98th** percentile of the k=55 null (CAGR 93rd). That is a statement about
the curated 55-name list — which is a hand-picked, current-constituent list — not about the MA200 book.

## 3. Rule 8 walk-forward (choose on ≤2016 by IS Sharpe inside each panel, 2017–2026 read once)

| panel | IS pick | IS Sharpe | OOS CAGR | OOS Sharpe | OOS MaxDD | vs SPY OOS 0.8820 | vs RULES v2 OOS | regret |
|---|---|---|---|---|---|---|---|---|
| U56 | n=20, g=0.75 (= anchor) | 1.1347 | 15.85% | **1.1810** | −19.09% | beats | 1.2937 — loses | −0.061 |
| B136 | n=10, g=1.00 | 1.1952 | 20.66% | 0.8401 | −33.52% | loses | 1.1206 — loses | −0.114 |
| B100 | n=10, g=1.00 | 1.1780 | 18.19% | 0.8040 | −32.00% | loses | 1.1015 — loses | −0.198 |
| BXU80 | n=10, g=1.00 | 0.9995 | 15.44% | 0.7514 | −32.67% | loses | 0.9443 — loses | −0.168 |

On all three broad panels the in-sample chooser picks the most concentrated, most levered cell
(n=10, gross=1.00) and lands on the **worst** OOS Sharpe available — regret −0.11 to −0.20, and OOS
MaxDD around −33%, i.e. SPY-like. Only U56's chooser lands on the anchor, and even there the book
loses to the live RULES v2 book out-of-sample (1.181 vs 1.294). Nothing here walks forward.

## Verdict — **KILL** (as a 4b KEEP candidate; the measurement is the keeper)

4a 0/36, 4b 4/36 across fixed panels (U56 3/9, B100 1/9 at n=30 only, B136 0/9, BXU80 0/9). The
MA200-only top-20 book does **not** pass 4b on a third or fourth large-cap panel, its one pass is a
61%-base-rate event on its own panel-size null, and its rule-8 chooser is actively harmful off U56.

Reportable by-product, worth more than the verdict: **on this book the 4b drawdown cap is a monotone
readout of pool size at fixed n**, so "panel A passes, panel B fails" comparisons across panels of
different size are confounded unless n/k is held fixed. That is a direct constraint on how ideas
276/284/285 (the cap-mix and panel-property line) should be read, and it is a cheap thing to check
before any future cross-panel 4b claim.

**Survivorship caveat:** `universe_broad.json` is a list of *current* large-cap constituents, and
`universe.json` is a hand-curated current list; every panel and every draw here inherits that bias.
Absolute CAGR/Sharpe levels are optimistic. The panel-to-panel contrasts are measured on one common
pool, which controls composition but not the pool's own survivorship.
