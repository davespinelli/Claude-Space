# IDEA 208 — audit-every-committed-null-for-a-salted-seed (lane C, 2026-09-05)

**ANSWERED, and the answer is worse than the question.** The salted seed is real, rare and
cheap to fix — 2 committed scripts, 4 sites, 612 published draw-derived cells (5.8% of the
corpus) and 540 clause verdicts (11.7%). But re-drawing one of them EXACTLY — the complete
974-rotation population for all 60 published U56 clause cells, 29,250 genuine backtests —
shows the seed is a symptom. **Under the exact 20-draw law, 50 of 60 published verdicts
(83.3%) are UNDETERMINED, and not one of the 60 clears with probability 1.** A reproducible
seed buys reproducibility; it does not buy a verdict.

5 of 5 pre-registered predictions hit.

---

## Q1 CENSUS — the AST audit

166 committed `.py`, **165 parsed** (`research/build_site.py` fails only on this
interpreter's pre-3.12 f-string rule; it is a site builder, not a backtest). **5 `hash()`
call sites in the whole repository, 4 of them seeds, 2 scripts affected:**

| file | line | expression | seed? | salted |
|---|---|---|---|---|
| `..._the-margin-column-instead-of-two_cloud.py` | 221 | `hash(('U56','DDCTL',0.03))` | no (a printed demonstration) | — |
| `..._the-on-share-column_cloud.py` (idea 191) | 435 | `rotations(J, N_NULL, SEED + hash((pan.name, fam, thr)) % 10_000)` | yes | **YES** |
| `..._the-on-share-column_cloud.py` (idea 191) | 580 | `default_rng(... + 7*abs(hash(pan.name)) % 1000)` | yes | **YES** |
| `..._the-share-at-which-ranking-stops-paying_B.py` | 536 | `default_rng(SEED + 7000 + hash((pk, t)) % 10_000)` | yes | **YES** |
| `..._the-share-at-which-ranking-stops-paying_B.py` | 581 | `default_rng(SEED + hash((pk, t, bar)) % 10_000)` | yes | **YES** |

The detector that matters is the fourth route: idea 191's seed reaches an RNG through a
*locally defined helper's* `seed` parameter, so a rule that only looks for `default_rng(...)`
misses the corpus's single largest exposure. **Empirically confirmed in two child processes:**
the str-bearing hash differs across processes, `hash(3)` and `hash((1,2,3))` do not — so a
hash of ints is a legitimate seed and a hash of a str never is.

**By-product:** 34 committed scripts draw randomness; **0** of them draw unseeded. The salted
seed is the only reproducibility hole of this kind in the corpus.

## Q2 EXPOSURE — what was published on an unreproducible draw

36 committed CSVs publish a draw-derived quantity (null band, permutation p-value, bootstrap
interval): **10,472 cells, 4,628 clause verdicts.** Of those, **3 CSVs / 612 cells (5.8%) /
540 verdicts (11.7%)** came from a salted seed — idea 191's `clause.csv` (540 cells, 540
verdicts) and idea B's `bootstrap.csv` + `dslope.csv` (72 interval cells, no verdicts).

## Q3 BOUND — the exact re-draw

Idea 191 draws 20 offsets uniformly without replacement from the J−1 = 974 circular
rotations, and `clears ⇔ |dSharpe| > max|dSharpe| over the 20`. Enumerating the **whole**
population makes the draw law closed-form:
`P(band ≤ x₍ₖ₎) = C(k,20)/C(974,20)`, `P(clears) = C(K,20)/C(974,20)`, `K = #{|d_off| < |d_real|}`.

**Reproduction first.** All 60 of idea 191's U56 real rows reproduce at **max |Δ| 1.4e-15**
(dSharpe 2.9e-16, dSharpe_IS 3.7e-16, dMaxDD 1.4e-15, on-share 8.3e-17) through the parent's
own code. Its bands do not reproduce at all, as predicted — and could not, in any process.

| exact result (60 published U56 cells) | Sharpe bar | MaxDD bar | IS-Sharpe bar |
|---|---|---|---|
| clear with probability **1** | **0/60** | 0/60 | 0/60 |
| clear with probability 0 | 10/60 | 12/60 | 8/60 |
| **UNDETERMINED (0 < P < 1)** | **50/60 = 83.3%** | 48/60 = 80.0% | 52/60 = 86.7% |
| band 5–95% draw range ÷ median band | **98.5% (median)**, 127.0% mean | 67.9% (median) | 81.4% (median) |
| E[# cells clearing] | **12.04 ± 1.61** (published: 10) | 6.23 ± 1.53 | 7.71 ± 1.56 |

* **Expected verdict flips vs idea 191's published U56 verdicts: 6.00 of 60 = 10.0%.**
  Worst single cell **P(flip) = 0.864** (BUDGET τ=0.30/half @10bps: published `clears=False`,
  true P(clears) = 0.864). 2 published `True`s sit below P = 0.5; 3 published `False`s sit
  above it.
* The probability that **two** independent 20-draw seeds disagree, averaged over cells, is
  **8.7%** (10.0% over the 52 non-inert cells) — the exact counterpart of idea 201's sampled
  17.8% across all three panels, and it supersedes it on U56.
* The undetermined zone spans `[band_min, band_max]` = **0.3070 wide on a mean |dSharpe| of
  0.0862 — 356% of the effect being tested.**
* Only **10 of 60** cells have P outside [0.1, 0.9]. A published `clears` on this grid is
  closer to a coin flip than to a finding.
* 8 cells are inert (`on_share = 0`, overlay never fires; DDCTL θ ≥ 0.15 on U56): |dSharpe| =
  band = 0, P(clears) = 0 correctly, and all 8 "pass 4b" only because they ARE the control
  book — idea 200's inert-cell defect, reproduced here from an independent direction.

## RULE 8 — what the seed costs in dollars

Pick on ≤ 2016-12-31 only (largest IS margin among points clearing their IS band, else
do-nothing), read 2017→ once, under 200 independent 20-draw seed regimes.

| 10 bps, OOS 2017-01-01 → | CAGR | Sharpe | MaxDD |
|---|---|---|---|
| seed-dependent clause selector (mean of 200 seeds) | 13.3% | 1.104 | −18.4% |
| — its best seed | 14.7% | 1.177 | −13.5% |
| — its **worst** seed | **7.2%** | **0.826** | −21.8% |
| do-nothing control (CAND-20, no overlay) | 14.5% | **1.177** | −18.2% |
| RULES v1 baseline | 3.8% | 0.399 | −14.2% |
| SPY buy-and-hold | 15.5% | 0.882 | −33.7% |

Full sample: RULES v1 2.8%/0.32/−15.6% · SPY 15.2%/0.89/−33.7% · control 12.9%/1.11/−18.2%.

* **0 of 6 cells beat do-nothing** (best cell mean dOOS **−0.0026**; pooled mean −0.0738;
  best single seed +0.0000, i.e. it never beats it, only ties by abstaining). **The twelfth
  consecutive do-nothing win.**
* **23.7% of (cell, seed) draws pick a different overlay** from their own cell's modal pick;
  11 distinct picks arise across the 1,200 draws. Within-cell OOS Sharpe spread: mean sd
  0.0784, max range **0.3832** (DDCTL @25bps).
* So the seed is not a cosmetic defect: it moves a real decision by up to 0.38 OOS Sharpe and
  7.3pp of OOS CAGR — while the decision itself is worth less than nothing.

## Both KEEP paths (all 60 real rows)

4a passes **7/60**; 4b passes **27/60**. Of the 27 4b passes, **0 clear their own null with
probability 1**, 18 are undetermined and 9 have P(clears) = 0 — and 8 of the 27 are the inert
control book. **No 4b pass on this grid is defensible as an overlay effect.** This run
proposes no new book and claims neither KEEP path; its product is a protocol clause.

## Recommended clauses (proposals — PROTOCOL.md and RULES.md untouched, per rule 6)

> **PROTOCOL 5 (addendum).** Every random draw must be seeded from a value identical across
> processes: an int literal, `zlib.crc32(key.encode())`, or a `SeedSequence` built from ints.
> **`hash()` of a `str`, or of any tuple containing one, is forbidden as a seed** — CPython
> salts it per process, so the published draw cannot be reproduced by anyone, including its
> author. A script that draws randomness must print its seeds.

> **PROTOCOL 11b (replacement).** A 20-draw band is not a verdict. Publish `clears` only
> beside `P(clears)`, or mark the cell UNDETERMINED. **Where the null population is
> enumerable — circular rotations are, at J−1 points — enumerate it and publish the exact
> `P(clears)` instead of a band.** On idea 191's U56 grid the exact computation costs 975
> backtests per configuration and removes the draw noise entirely.

## Caveats

Survivorship (idea 54): U56 is current constituents; every LEVEL above is biased upward and
is not a tradable estimate, while the clause reading is unaffected because real and rotated
draws inherit the bias identically. Neighbouring rotations are correlated, so the clause's
nominal 4.8% size is approximate — the enumeration is exact for the draw law, not for the
clause's power. BROAD136 and SMALL439 were not re-drawn (cost); the Q1/Q2 census covers all
three panels, the Q3 bound covers U56's 60 cells only. The MaxDD row's *mean* range ratio is
a divide-by-zero artefact of the 8 inert cells — the median (67.9%) is the usable figure.
Idea 38 (calendar-day index after 2014-09-17), idea 126 (t+1 only), idea 203 (BUDGET-skip
turnover mismatch) inherited and stated, not fixed.

**Files:** `2026-09-05_audit-every-committed-null-for-a-salted-seed_C.py` ·
`.console.txt` · `.audit.csv` (5 hash sites) · `.exact.csv` / `.keep.csv` (60 cells × exact
law) · `.walkforward.csv` (1,200 seed-regime picks).
