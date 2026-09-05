# idea 115 — `sleeve-G-is-2013` (cloud, 2026-09-05) — **KILL as posed**

**Question.** Idea 112 showed the sleeve grid's whole rule-8 gap (pooled `G = -0.169`) flips to
`+0.035` when 2013 is deleted from the in-sample window, while every other overlay grid moves
≤0.013. Decompose 2013 for the sleeve: which of TLT/GLD/DBC/UUP loses, and is the gap simply
"gold had one terrible year inside the IS window"?

**Answer: no, on both halves of the question.** Gold is not the biggest 2013 loser inside the leg,
and deleting gold does not remove the 2013 dependence. The 2013 effect is a property of the
*window* (a +32% equity year that punishes any diversifier), not of any sleeve asset.

## Harness

Idea 112's module imported construction-for-construction (`book`, `sleeve_weights`, `_regross`,
`full_row`, `keep_4a/4b`, the `f` grid). 2 universes (u56 = `universe.json` incl. BTC/ETH,
broad = `universe_broad.json`) × 2 base books (`top20`, `ewall`, both 0.75 gross) × 2 cost rungs
(10, 25 bps) = **8 cells**, weekly, next-day execution. Sleeve fraction `f ∈ {0, .25, .50, .75, 1.00}`.
**Two tuned parameters (PROTOCOL rule 4): `f` and the sleeve COMPOSITION.** All 280 grid points
reported. IS = ..2016-12-31, OOS = 2017-01-01.. and is never used to choose anything.

Sleeve variants, all reported: `S4` (TLT+GLD+DBC+UUP, the incumbent), `exTLT`/`exGLD`/`exDBC`/`exUUP`
(leave-one-asset-out), `GLDonly`, and **`FLAT4`** — the four legs held at S4's own weights but
earning **zero return**: the dilution control that isolates "any non-equity leg" from "these assets".

**Reproduction (S0): EXACT.** All 32 of idea 112's committed sleeve points re-derived, max |diff|
`1.1e-16` across `d_IS`, `d_OOS`, `G_full` and all eight `G_ex{year}`. Published
`G_full −0.1694 → G_ex2013 +0.0350` reproduces to four decimals.

## (1) Which asset loses in 2013 — all four of them, and gold least of the ones that matter

Exact attribution inside the leg (realised t+1 weights × returns, u56; broad agrees to 1e-3):

| asset | mean sleeve weight | 2013 total return | 2013 contribution |
|---|---|---|---|
| TLT | 4.96% | −12.2% | **−1.16 pp** |
| DBC | 5.26% | −8.0% | −0.80 pp |
| GLD | 1.92% | **−28.8%** | −0.71 pp |
| UUP | 16.52% | −1.4% | −0.69 pp |
| leg total | | | **−3.36 pp** |

The queue's premise ("gold −28%") is true about gold and false about the sleeve: the inverse-vol
weighting gives gold the **smallest** weight of the four precisely because it is the most volatile,
so the biggest price move produces the third-largest loss. **All four assets lost in 2013** — it is
the only year in the sample in which they all do.

## (2) The gap is a window property, not a composition property

Pooled `G` (8 cells × 4 non-null `f` = 32 points per variant):

| variant | `G_full` | `G_ex2013` | move on deleting 2013 | largest other-year move |
|---|---|---|---|---|
| S4 | −0.1694 | +0.0350 | **+0.204** | 0.225 (2011) |
| exTLT | −0.2850 | −0.0968 | +0.188 | 0.162 |
| exGLD | −0.0737 | +0.1127 | **+0.186** | 0.221 |
| exDBC | **+0.0209** | +0.2237 | +0.203 | 0.252 |
| exUUP | −0.1463 | +0.0400 | +0.186 | 0.188 |
| GLDonly | −0.3102 | −0.1629 | +0.147 | 0.163 |
| FLAT4 | +0.1732 | +0.1444 | −0.029 | 0.066 |

Deleting gold halves the *level* of `G` (−0.169 → −0.074, so condition (ii) of the pre-registered
test passes) but leaves the *2013 dependence* completely intact (+0.186 against S4's +0.204), so
condition (iii) fails and condition (i) fails outright. **Pre-registered decision: FALSE.**

Two further readings the table forces:

- **On the composition axis it is DBC, not GLD, that carries the sign.** `exDBC` is the only variant
  whose pooled `G` is positive; `exTLT` roughly doubles the gap. Direct support for queue idea 106.
- **2011 moves `G` further than 2013 does** (0.225 vs 0.204) — in the opposite direction. Idea 112's
  "2013 flips the sign" is about the sign, not the magnitude; idea 116 already found 2011 is the
  year rule 8 leans on hardest, and this run agrees on the sleeve grid specifically.

## (3) What 2013 actually is: 27.5% dilution, ~11% gold, the rest the assets' own returns

`FLAT4` — the sleeve's exact weight footprint earning nothing — reproduces **116%** of S4's raw 2013
`d(Sharpe)`. That number is misleading on its own, because `FLAT4` dilutes in every year (its `d`
never rises above −1.13). The statistic that has to be explained is 2013's **excess** over the
variant's own other years:

| variant | mean `d` (other years) | `d` 2013 | excess | z | share of S4's excess |
|---|---|---|---|---|---|
| S4 | −0.044 | −1.959 | **−1.915** | −3.38 | 1.000 |
| FLAT4 | −1.753 | −2.280 | −0.527 | −1.63 | **0.275** |
| exGLD | −0.146 | −1.853 | −1.707 | −2.44 | 0.891 |

So **27.5%** of 2013's excess damage is what *any* zero-return leg would have done to a +32% equity
year, **10.9%** is gold, and the remaining ~62% is the other three assets losing money at the same
time. 2013 is S4's worst year of 18 (z = −3.4); 2011 is its best (+1.09).

## (4) Walk-forward (PROTOCOL rule 8) — the standing candidate is untouched

`f` chosen on the IS window only (argmax IS Sharpe, tie-break smallest `f`); OOS 2017-2026 untouched.
56 picks; 20 pass 4b, 22 pass 4b-OOS, 32 pass 4a. References on the same days: RULES v1
**7.2% / 0.699 / −13.8%**, SPY **15.5% / 0.882 / −33.7%**.

- **Incumbent `S4 / top20 / 10 bps`** picks `f = 0.50`: full **12.4% / 1.180 / −14.3%** (halves
  1.161 / 1.200), **OOS 13.6% / 1.261 / −14.3%** on u56, and passes 4b on broad in the same cell
  (12.1% / 1.057 / −15.6%, OOS 11.6% / 1.006). Unchanged by this run.
- **`exDBC / top20 / 10 bps`** picks the same `f = 0.50` and **dominates it full-sample on both
  universes**: u56 **12.1% / 1.200 / −13.4%** (halves 1.237 / 1.170), OOS 12.9% / 1.240 / −13.4%,
  passing **both 4a and 4b**; broad 11.9% / 1.068 / −14.6%, OOS 11.0% / 0.974, also both paths.
  It beats S4 on full-sample Sharpe in **8 of 8** cells (mean +0.027) at a shallower drawdown
  (mean +0.021 pp) — and loses to it marginally out of sample (mean OOS Sharpe −0.015). Composition
  was a *tuned* axis here, so this is a candidate for the Sunday review, not a selection this run is
  entitled to make; memo: `2026-09-05_sleeve-G-is-2013_cloud.memo.md`.
- `GLDonly` passes 4b at **0 of 40** grid points and its walk-forward rule picks `f = 0` (no sleeve)
  in **6 of 8** cells. The strong form of the queue's gold hypothesis is dead on its own numbers.

## Caveats

**Survivorship:** both lists are current-constituent, so absolute CAGR/Sharpe are optimistic. Every
statistic above is a difference between books holding the same equity names on the same days plus
four ETFs with no survivorship exposure, so the bias largely cancels; the levels should not be quoted.
**Contamination of the FLAT4 control:** the base books themselves hold TLT/GLD/DBC/UUP for 1.9–7.4%
of gross, and those holdings are flattened too, so `FLAT4`'s 27.5% is a slight over-estimate of pure
dilution. **Spliced Sharpe:** deleting a year leaves mean/std defined (idea 89's convention); MaxDD
is never taken on a spliced series. 2009 is a partial IS year.

## For the Sunday review

1. **Do not write a gold clause into RULES on the strength of the sleeve's `G`.** Gold is ~11% of
   the 2013 effect and removing it leaves the 2013 dependence intact. Ideas 105/106's gold question
   is worth answering on its own merits (idea 105 asks about *return contribution*, where GLD is
   large) but it does not explain rule 8's blind spot.
2. **The honest statement of the blind spot is about the window:** rule 8's IS window contains a
   +32% equity year in which every diversifier lost money simultaneously, and roughly a quarter of
   the resulting penalty would apply to *any* zero-return leg. That is idea 111's caveat, restated
   with a number.
3. **Idea 106 is now the load-bearing open question for the sleeve**, not idea 105: DBC is the asset
   whose removal flips the sleeve's `G` sign and improves the candidate on both universes.
