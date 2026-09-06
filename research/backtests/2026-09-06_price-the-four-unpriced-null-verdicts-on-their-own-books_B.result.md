# Idea 268 — price-the-four-unpriced-null-verdicts-on-their-own-books (lane B, 2026-09-06)

**ANSWERED / SPLIT 2–2, and the premise is half wrong.** All four flagged scripts already ran their
books at 10 **and** 25 bps, so no published sentence here was ever computed gross — "unpriced" can
only mean *never told you where its breakeven sits*. Measured on each script's own panel, own `n`
and own cadence: **two of the four verdicts are rung-robust and two are bought by the cost rung.**
The sharp one is idea 180's: **at 0 bps the five real keys sit at the 55th / 50th / 45th percentile
of their own 100-draw null band on u56 / broad / small — inside it on all three panels, and *below*
the null mean on all three.** The published 92nd / 100th / 51st is entirely a cost artefact, because
a random-walk key tilts the book **less** than any real key (turnover ratio to the no-tilt control
1.05–1.10 vs 1.12–1.29), so a positive rung inflates the real keys' `|dSharpe|` and nothing else.
**A matched-null `|dSharpe|` band read at a non-zero rung is a turnover test, not an information
test.** Rule 8 pick `S1/broad/R6/n=3` → OOS 17.8% / **0.820** / −30.2% vs SPY OOS 0.882 / 15.45% /
−33.72% = **KILL 4b (OOS, DD)**. No KEEP-candidate, no new book, no RULES change.

Script `2026-09-06_price-the-four-unpriced-null-verdicts-on-their-own-books_B.py` (380 s) ·
`…console.txt` · `…{site1,site2,site3,site4,breakeven,verdicts,walkforward}.csv` ·
`…site3_draws.csv.gz`

---

## Design

Every construction is **imported from its parent with `importlib`, not retyped** — `I158.parts` /
`I158.weights`, `I180.null_key` / `I180.ranks_of` / `I180.Sim`, `I209.keys_for` /
`I209.topn_weights`, `I181.build_keys` / `I181.composite` — so a reproduction miss would be a bug in
this script, never a difference of construction. Each parent is also run on **its own panel**: the
three do not share a small-cap universe (idea 129/158/180 hold SPY out of 439 names, idea 181/192
leave it in, idea 209 uses the unfiltered 483).

Every book is run **once at 0 bps** and every rung derived from the engine's own identity
`r_c = r_0 − turnover·c/1e4`. Sharpe on the fine ladder is **closed form**, not re-simulated:
`Sharpe(c) = (mu0 − mut·k)·√252 / √(V0 − 2k·Cov + k²·Vt)`, `k = c/1e4`, from five sufficient
statistics per window — exact, and asserted against `metrics()` before use.

**Tuned parameters: 2** — the panel and the book size (`n`, or the share `m` that maps to it). Both
are inherited from the parents unchanged and swept exhaustively. Site, key, tilt direction, draw and
**cost rung** are reported axes, never selected on. **4,464 grid rows written; 5,118 books built**
(192 S1 + 273 S2 + 4,200 S3 + 453 S4).

Scoring, pre-registered: **SURVIVES** = true at 10 bps and no breakeven in (0, 25]; **FRAGILE** =
true at 10 bps but a breakeven inside the record's own rung range; **FLIPS** = false at 10 bps.

### Gates — 10 of 10, asserted before any result below was read

| gate | result |
|---|---|
| `Sim.run == engine.backtest`, 3 panels | max abs 1.4e-17 returns / 3.1e-16 turnover |
| cost identity vs a live 10 bps engine run | max abs 1.4e-17 |
| closed-form `Sharpe(c)` vs `metrics()`, 11 rungs × 3 windows | max abs 4.4e-16 |
| **R1** idea 209 `.corpus.csv` | **384 / 384 rows, max abs 2.2e-15** (turnover 1.4e-14) |
| **R2** idea 158 `.grid.csv` (lit) | **546 / 546 rows, max abs 7.1e-15** |
| **R3** idea 180 draw 0 == idea 158's published RAND rows | max abs 5.3e-16 |
| **R4** idea 181 `.grid.csv` (corpus T rebuilt) | **900 rows, max abs 6.7e-16 / 8.5e-16** |
| **R4p** idea 192's published pooling, rebuilt end-to-end | **1/51 clears, 75/237 = 31.6%, Fisher p 9.23e-07** vs published 1/51, 31.6%, 9.2e-07 — **EXACT** |
| mean weekly eligible names | 37.50 / 91.46 / 141.23, == idea 153/158 |

The parents' own headline constants fall out of the re-run: idea 209's `u56 +0.866 / broad +0.880 /
small +0.197` are the means of this run's 10 and 25 bps rungs (+0.869/+0.863, +0.877/+0.883,
+0.395/−0.002); idea 180's null-band means `0.0945 / 0.0514 / 0.1049` are the means of its
(0.0818, 0.1072) / (0.0437, 0.0592) / (0.0964, 0.1134).

---

## S1 — `is-the-book-size-floor-a-corpus-wide-clause_C` (idea 209): **SPLITS**

Null = `RND`, `rng.random(px.shape)` — a fresh uniform for every name **every day**, so the book is
re-drawn at every weekly rebalance. Its turnover is 8.8–76.8×/yr against the composite's 4.9–36.3×.

ρ_Spearman(`n`, OOS Sharpe) within each (panel, arm) cell, by rung:

| | 0 | 1 | 2 | 5 | **10** | 15 | 20 | **25** | breakeven in (0,25] |
|---|---|---|---|---|---|---|---|---|---|
| **LARGE arm-cells positive** | 24/24 | 24/24 | 24/24 | 24/24 | **24/24** | 24/24 | 24/24 | **24/24** | **none** |
| mean ρ u56 | +0.846 | +0.855 | +0.857 | +0.871 | **+0.869** | +0.861 | +0.861 | **+0.863** | — |
| mean ρ broad | +0.824 | +0.842 | +0.841 | +0.864 | **+0.877** | +0.886 | +0.888 | **+0.883** | — |
| **SMALL arm-cells positive** | 12/12 | 12/12 | 12/12 | 10/12 | **10/12** | 8/12 | 4/12 | **4/12** | — |
| small keys with ρ < 0 | **0/6** | 0/6 | 0/6 | 1/6 | **1/6** | 2/6 | 4/6 | **4/6** | — |
| mean ρ small | **+0.600** | +0.589 | +0.553 | +0.514 | **+0.395** | +0.261 | +0.145 | **−0.002** | COMP 14.23, R6 4.11, INVVOL 15.10, **RND 18.12** |

* **S1a (large half) — SURVIVES.** 24 of 24 positive at *every* rung 0–25, zero breakevens. Idea
  209's large-panel claim is rung-invariant.
* **S1b (small half) — FRAGILE, and it is the half the verdict rests on.** Idea 209's headline is
  *"the sign reverses at exactly one boundary — the sub-$2B panel"*. In its fresh corpus that
  reversal **does not exist below ~14 bps**: 12 of 12 arm-cells positive and 0 of 6 keys negative at
  0 bps, still 5 of 6 positive at PROTOCOL's own 10 bps rung. Four of six small arm-cells — the
  `RND` null among them, at **18.12 bps** — flip inside (0, 25]. The published "NEGATIVE in 4 of 6
  ranking keys" is true **only** at 25 bps, exactly as its sentence says, and the pooled `+0.197`
  averages a positive 10 bps rung with a ~zero 25 bps one.

The archive census half of idea 209 (LARGE ρ +0.674 / SMALL −0.361 over 17 scripts) is a different
corpus and is **not** touched by this run.

## S2 — `does-share-price-any-key-or-only-vol_B` (idea 158): **FRAGILE, direction intact**

Null = `RAND`, `rk(126d change of a geometric random walk)`, seed 158 — idea 262's `RWK` shape.

| rung | NEG: RAND > VOL | POS: RAND > VOL | mean dS RAND/NEG | mean dS VOL/NEG | gap |
|---|---|---|---|---|---|
| 0 | 13/14 | 1/14 | +0.0160 | −0.0720 | +0.0880 |
| 5 | 13/14 | 1/14 | +0.0023 | −0.1066 | +0.1088 |
| **10** | **13/14** | 1/14 | −0.0114 | −0.1412 | **+0.1297** |
| 15 | 14/14 | 0/14 | −0.0252 | −0.1758 | +0.1506 |
| **25** | **14/14** | 0/14 | −0.0527 | −0.2450 | **+0.1924** |

Pooled over the parent's two rungs this is **27 of 28 — the published number, exactly.** Only one of
the 14 cells (`broad, m=0.05`) has a breakeven inside (0, 25], at **13.99 bps**, and the gap widens
**monotonically** with cost. So the eighth delete-the-scaler result is **not manufactured by the
rung** — it is true at 0 bps too and cost only amplifies it. What is rung-specific is the *count*:
"27 of 28" is a statement about {10, 25} bps and would be "26 of 28" at {0, 10}.

**The rung-bound sentence at this site is the other one.** Idea 158's memo says a zero-information
book *"clears PROTOCOL's cross-universe 4b at the same rate as the real ones"*, and that fact has a
short life:

| rung | 4a | 4b | 4b RAND | 4b real keys | 4b NONE | cross-universe 4b | of them RAND |
|---|---|---|---|---|---|---|---|
| 0 | 35 | 89 | 19 | 62 | 8 | 37 | 7 |
| 5 | 51 | 74 | 17 | 51 | 6 | 31 | 6 |
| **10** | 65 | **54** | **11** | 38 | 5 | **19** | **3** |
| 15 | 74 | 29 | 5 | 20 | 4 | 7 | 1 |
| 20 | 86 | 8 | 0 | 6 | 2 | 1 | 0 |
| 25 | 99 | **0** | 0 | 0 | 0 | 0 | 0 |

`11 of 54` and `4 of 19` reproduce the published counts at 10 bps. But **every 4b pass in this grid,
random or real, is gone by 25 bps**, and the random ones are gone by 20. The noise-admission finding
is a statement about the 10 bps rung specifically, not about the 4b bar in general.

## S3 — `is-the-null-key-result-one-draw-or-a-distribution_cloud` (idea 180): **FRAGILE — the finding is the rung**

Mean `|Sharpe(tilt) − Sharpe(NONE)|` at matched (panel, m), 100 null draws vs the 5 real keys:

| panel | | 0 bps | 5 | **10** | 15 | 20 | **25** |
|---|---|---|---|---|---|---|---|
| u56 | null band | 0.0698 ± 0.0183 | 0.0752 | **0.0818** | 0.0895 | 0.0980 | **0.1072** |
| | real mean | **0.0687** | 0.0817 | 0.0960 | 0.1122 | 0.1287 | 0.1454 |
| | **percentile** | **55th** | 71st | **82nd** | 91st | 94th | **98th** |
| broad | null band | 0.0416 ± 0.0123 | 0.0418 | **0.0437** | 0.0473 | 0.0525 | **0.0592** |
| | real mean | **0.0400** | 0.0503 | 0.0621 | 0.0771 | 0.0929 | 0.1091 |
| | **percentile** | **50th** | 75th | **90th** | 98th | 100th | **100th** |
| small | null band | 0.0862 ± 0.0189 | 0.0912 | **0.0964** | 0.1019 | 0.1075 | **0.1134** |
| | real mean | **0.0832** | 0.0882 | 0.0945 | 0.1009 | 0.1076 | 0.1167 |
| | **percentile** | **45th** | 45th | **45th** | 49th | 51st | **60th** |

**At 0 bps the real keys are inside their own null band on all three panels — and the real mean is
BELOW the null mean on all three.** Five hand-built ranking tilts move the book *less* than the
average random walk does. The published 92nd / 100th / 51st (the pooled 10+25 bps reading, which
this run reproduces to the digit) is **manufactured by the rung**: broad's "exits the band" starts
only at **16.14 bps**, u56 clears the null 95th only from **20.20 bps**, and small never exits at
all up to 40 bps.

**The mechanism, measured.** Mean turnover ratio to the no-tilt control at 10 bps:

| panel | NONE | **RAND** | MOM | R6 | R3 | VOL | VOLR |
|---|---|---|---|---|---|---|---|
| u56 | 1.000 | **1.101** | 1.164 | 1.232 | 1.235 | 1.162 | 1.160 |
| broad | 1.000 | **1.095** | 1.159 | 1.229 | 1.247 | 1.190 | 1.256 |
| small | 1.000 | **1.053** | 1.118 | 1.136 | 1.153 | 1.191 | 1.286 |

The null key is the **least** disruptive tilt on every panel. Cost therefore adds more drag to every
real arm's distance from the control than to the null's, and `|dSharpe|` separates for that reason
alone. **A matched-null `|dSharpe|` band quoted at a non-zero rung measures the turnover difference,
not the key's information.** Such a band should be read at 0 bps, or with turnover matched, or with
both numbers published side by side.

This does **not** overturn idea 180's own deliverable — its point was that idea 158's single draw
should be replaced by a band, and that stands (draw 0 sits at the 50th / 74th / 4th percentile of
its own band). It overturns the *reading* that the real keys are distinguishable from noise on this
instrument.

## S4 — `does-a-harmful-instrument-…-helpful-one_B` (idea 192): **SURVIVES**

Null band = 20 random-walk keys, corpus T rebuilt from idea 181's construction and re-priced (the
108 corpus-O rows are idea 186's rotations and are held at their committed rungs; both are reported).

| rung | clears / 90 | 4b pass | clears \| 4b pass | clears \| 4b fail | Fisher p |
|---|---|---|---|---|---|
| 0 | 27 | 36 | 6/36 (16.7%) | 21/54 (38.9%) | 3.41e-02 |
| 2 | 27 | 34 | 4/34 (11.8%) | 23/56 (41.1%) | 4.06e-03 |
| 5 | 29 | 32 | 3/32 (9.4%) | 26/58 (44.8%) | 7.61e-04 |
| **10** | 29 | 29 | **1/29 (3.4%)** | **28/61 (45.9%)** | **2.35e-05** |
| 15 | 32 | 23 | 0/23 (0.0%) | 32/67 (47.8%) | 7.05e-06 |
| 25 | 30 | 4 | 0/4 (0.0%) | 30/86 (34.9%) | 2.97e-01 |

**The direction never reverses on 0–25 bps** — no breakeven — and the effect *strengthens* with
cost, so idea 192's KILL of the matched-null clause as a KEEP gate is rung-robust. (The 25 bps
p-value is weak only because 4b survivors collapse to four arms; the point estimate is still 0%.)
Pooled the way idea 192 pooled it, the published table comes back **exactly**: 1 of 51, 31.6% of
237, Fisher p 9.23e-07.

**One qualification S3 forces on it.** If "clears the band" at 10 bps partly encodes *the arm trades
more than the null*, then the clause's measured association with 4b failure carries a turnover
component. The 0-bps row is the clean read, and it has the same sign at p 3.4e-02.

---

## PROTOCOL 8 walk-forward — parameters chosen on 2009–2016, 2017–2026 read once

Pool = all 465 books this run built at sites 1 and 2; IS-Sharpe argmax; OOS read once.

| sel rung | IS-argmax book | IS Sh | OOS CAGR | OOS Sharpe | OOS MaxDD | v1 OOS Sh | SPY OOS Sh | 4b OOS |
|---|---|---|---|---|---|---|---|---|
| 0 | `S1/broad/R6/n=3` | 1.381 | 20.81% | 0.927 | −29.60% | 0.857 | 0.882 | FAIL |
| 5 | `S1/broad/R6/n=3` | 1.330 | 19.31% | 0.873 | −29.90% | 0.717 | 0.882 | FAIL |
| **10** | **`S1/broad/R6/n=3`** | **1.279** | **17.83%** | **0.820** | **−30.21%** | 0.576 | **0.882** | **FAIL** |
| 15 | `S1/broad/MOM/n=8` | 1.233 | 16.43% | 0.871 | −23.36% | 0.436 | 0.882 | FAIL |
| 25 | `S1/broad/MOM/n=8` | 1.143 | 14.64% | 0.793 | −24.03% | 0.155 | 0.882 | FAIL |

SPY OOS 0.882 / 15.45% / −33.72%. RULES v1 OOS @10 bps: u56 0.747/7.73%, broad 0.576/5.94%, small
0.581/7.92%. The 10 bps pick's full sample is 23.0% / 1.021 / −30.2%, halves 1.231 / 0.827.

**KILL on 4b: OOS Sharpe 0.820 < SPY 0.882, and OOS MaxDD −30.2% is worse than 0.60 × SPY's
−33.72% = −20.2%.** It fails at every rung. This is another idea-229 selection-loses instance —
an IS argmax over 465 books lands on a 3-name concentrated book and gives back 0.107 of Sharpe out
of sample. **The selection rung also changes the book**: 2 distinct picks across the 8 rungs, an OOS
Sharpe spread of 0.134 — so the rung is a hidden selector, not only a scorer.

**KEEP paths.** 4a 65 of 273 and 4b 54 of 273 at 10 bps on site 2 (idea 153/158's already-published
family — nothing new), 0 of 273 at 25 bps. Nothing in this run is proposed and there is **no
KEEP-candidate**.

---

## What the record should carry

1. **Idea 209's small-panel sign reversal is a 14–18 bps phenomenon, not a sub-$2B one** — its
   fresh corpus is 12/12 positive at 0 bps and 5/6 positive at PROTOCOL's own rung. The large-panel
   half is rung-invariant and stands.
2. **A matched-null `|dSharpe|` band is not an information test at a non-zero rung.** Idea 180's
   percentiles collapse to 55th / 50th / 45th at 0 bps because the null key tilts the book *least*.
   Any future null-band clause should publish the 0-bps reading, or match turnover.
3. **Idea 158's "a zero-information book clears 4b" is a 10-bps statement**: 19 RAND passes at 0
   bps, 11 at 10, **0 at 20**, and 0 of anything at 25.
4. **Idea 192's clause KILL is rung-robust** and its published table reproduces exactly.
5. Idea 262's class prices did **not** transfer to these books. Its `RWK` class median breakeven was
   11.36 bps and its `REDRAWN_KEY` class ~0.99 bps; on their own panels the actual sentences break
   at 4.1 / 13.99 / 14.2 / 15.1 / 15.1 / 16.1 / 18.1 / 20.2 bps — the class number is the right
   order of magnitude and the wrong number for any individual verdict. **Price the sentence, not the
   class.**

`RULES.md`, `scan.py`, `bot.py` and `baseline.py` untouched. No rules change proposed.
