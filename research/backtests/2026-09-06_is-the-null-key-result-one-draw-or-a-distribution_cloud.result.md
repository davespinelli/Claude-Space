# idea 180 — is-the-null-key-result-one-draw-or-a-distribution (cloud, 2026-09-06)

**VERDICT: idea 158's null-key result SURVIVES as a band, and gets stronger. Every one of its four
headline null-key claims is a typical draw, not a lucky one — but its S3 rule-8 number was the
*good* tail, and the 0.7240 the record quotes should be replaced by 0.7059 ± 0.0801. Nothing here
is a KEEP; no book is proposed and no rule changes. The deliverable is the band PROTOCOL should
quote in place of the point.**

## Controls (asserted before any new number was read)

* **[a]** mean weekly eligible counts reproduce idea 153/158's published 37.50 / 91.46 / 141.23 on
  all three panels.
* **[A]** the vectorised simulator == `engine.backtest` to **1.0e-17 / 1.4e-17** on returns and
  **2.2e-16 / 2.8e-16** on turnover, on all three panels at weekly cadence.
* **[D]** the cost identity `r_c = r_0 − turnover·c/1e4` against a fresh 10 bps engine run: max
  **1.4e-17** on every panel.
* **[C] the decisive one.** All **462** NONE + real-key rows reproduce idea 158's committed
  `.grid.csv` to **7.1e-15**, and **draw 0 (seed 158) reproduces its published RAND rows exactly**
  — so this is idea 158's grid, its instrument, and its key, with 99 more keys added.

## R1 — the |dSharpe| band (the first distribution the idea asks for)

Mean |Sharpe(tilt) − Sharpe(NONE)| at matched (panel, m, cost), over 100 null keys:

| panel | null band (full grid) | mean of the 5 real keys | where the real mean sits | draw 0 |
|---|---|---|---|---|
| u56 | **0.0945** ± 0.0178 [0.050, 0.150] | 0.1207 | **92nd** pct of the null band | 0.0921 (50th) |
| broad | **0.0514** ± 0.0136 [0.027, 0.081] | 0.0856 | **100th** pct | 0.0608 (74th) |
| small | **0.1049** ± 0.0197 [0.060, 0.156] | 0.1056 | **51st** pct | 0.0699 (4th) |

On `m ≤ 0.53` the same picture one level up (u56 null 0.1243 ± 0.0252 vs real mean 0.1566, 90th
pct; broad 0.0668 vs 0.1125, 100th; small 0.1371 vs 0.1341, 44th).

**Idea 158's headline reading holds and is now quantified.** A key with zero information moves
Sharpe by 0.05–0.14 depending only on the panel, and on the small panel the five real keys are
*indistinguishable* from noise (51st percentile of the null band, full grid). On the large-cap
panels the real keys are at the top of the null band but still inside it — the separation is a
percentile statement, not a categorical one. `R6` on u56 (0.0565) is *below* the null mean.

## R4 — "beats the live `/sqrt(vol20)` scaler in k of 28 large-cap cells"

| tilt | null band, cells won of 28 | idea 158's published draw |
|---|---|---|
| NEG | **27.06** ± 1.41 [22, 28], median 28 | 27 → **23rd** percentile |
| POS | **26.56** ± 1.63 [20, 28], median 27 | 23 → **2nd** percentile |

**100 of 100 draws beat the live scaler in at least half the cells, and 0 of 100 draws are worse
than it on mean signed dSharpe** (null NEG −0.0682 ± 0.0311, POS −0.0461 ± 0.0278, against the
live scaler's **−0.1931**). The eighth delete-the-scaler finding is not a property of seed 158 —
it is the property of *any* random key. Idea 158's published counts were, if anything, an
**understatement**: its draw sat at the 23rd and 2nd percentiles of what a null key typically does.

## R2 — the 4b pass-count band (the second distribution)

Each draw contributes 84 RAND cells (3 panels × 7 shares × 2 dirs × 2 costs).

| statistic | band over 100 draws | idea 158's draw |
|---|---|---|
| 4b passes | **9.82** ± 1.51 [6, 13] | 11 → 68th pct |
| 4a passes | 26.04 ± 1.73 [22, 31] | — |
| 4b on the OOS window | 17.24 ± 2.12 [11, 23] | — |
| share of the grid's total 4b passes | **18.5%** [12.2%, 23.2%] | 20.4% |

**Zero draws out of 100 scored zero 4b passes.** By panel: u56 5.33 ± 0.93, broad 4.49 ± 1.08,
small **0.00 ± 0.00 in every one of 100 draws** — the eighth reproduction of idea 136's "the small
panel has no 4b passer", now against a null family rather than a book.

## R5 — cross-universe 4b

Null-key combinations passing 4b on more than one panel: **3.19 ± 1.03 [1, 5]**, and **100 of 100
draws produce at least one**. The fixed part of the grid (NONE + 5 real keys) yields 16.
Idea 158's "4 of 19" was a typical draw. A cross-universe 4b pass is not evidence that a key is
real — it is what a random key does roughly three times per grid.

## R3 — PROTOCOL rule 8, the third distribution (and where idea 158 was lucky)

Mean OOS Sharpe over the 6 (panel, cost) cells, parameters chosen on ≤2016-12-31 only:

| selector | band over 100 draws | vs the do-nothing control |
|---|---|---|
| S1 (IS argmax over all 91+14 arms) | 0.7244 ± 0.0474 [0.499, 0.825] | beats S2 in **1/100** draws |
| **S3 (IS argmax, null key only)** | **0.7059 ± 0.0801** [0.480, 0.980] | beats S2 in **2/100** |
| S4 (IS argmax, NONE arms only) | 0.7808 (fixed) | 0/100 |
| **S2 do-nothing (m = 0.53)** | **0.8149** (fixed) | — |
| RULES v1 | 0.4514 (OOS CAGR 4.86%) | — |
| SPY | 0.8820 (OOS CAGR 15.45%) | — |

**This is the one place the published number needs correcting.** Idea 158 quotes S3 = 0.7240 and
reads it as "0.001 ahead of S1" — but 0.7240 is that draw's value and it sits at the **56th
percentile**; the null selector's actual mean is **0.7059** with an sd of **0.0801**, four times
S1's spread. The honest statement is not "the null selector ties the real one" but **"the null
selector is a coin flip whose expected value is 0.019 BELOW the real one and 0.109 below doing
nothing"**. S1 beats the do-nothing control in 1 of 100 draws and SPY in 0; S3 beats do-nothing in
2 and SPY in 1. **The seventh consecutive instance of "selection loses to doing nothing" is now
measured with an error bar rather than asserted from one path.**

Idea 158's "rule 8's own selector picks the RAND key on broad@10bps" is likewise a draw-level
fact: S1 picks a null-key arm in **26 of 100** draws on broad@10bps, and in **41 of 100** draws
somewhere among the 6 cells (0.74 ± 1.08 cells per draw). It happens often, but it is not the norm.

## What this changes

1. Idea 158's four headline null-key claims are all **typical**, two of them conservatively so.
   The record does not need to retract anything it said about the null key's *magnitude*.
2. **Its S3 number should be re-quoted as a band.** 0.7240 is a point on a distribution with an sd
   of 0.0801; any future sentence comparing a selector to "the null selector's 0.7240" is
   comparing to a coin flip's single toss.
3. Offered to PROTOCOL and **not adopted here**: a null-key control quoted as a point estimate
   should carry the draw count and the sd of its own family, exactly as a KEEP carries its halves.

## Caveats

* **SURVIVORSHIP:** all three panels are current-constituent lists (idea 54); the small panel
  additionally drops every ticker with `max_1d_move ≥ 1.0` per the standing rule (439 of 483 names
  remain). No level here is an attainable return.
* Ideas 39/49: the eligibility gate is **inverted** on the small panel, so its numbers describe a
  gate that does not work there. Reported, never traded.
* Idea 126: t+1 execution only, no spread or impact model.
* **100 draws bound the SEED, not the model.** Every null key here is a geometric random walk with
  R6's functional form at the panel's own median daily vol. A different null *family* — a shuffled
  real key, a persistent AR(1), a sector-correlated walk — is a different question and is not
  answered here.
