# Idea 158 — does-share-price-any-key-or-only-vol (lane B, 2026-09-05)

**VERDICT: SPLIT — the SIGN of idea 153's mechanism is arithmetic and universal, its STRENGTH is
not. KILL of the R² reading; the "book share prices a tilt" wording must be narrowed. No RULES
change, no new book, no KEEP-candidate. The run's sharpest by-product is a negative control the
project did not have: a key with ZERO information passes cross-universe 4b, is picked by rule 8's
own selector, and beats the LIVE `/sqrt(vol20)` scaler in 27 of 28 large-cap cells.**

Script: `2026-09-05_does-share-price-any-key-or-only-vol_B.py`
Outputs: `.console.txt`, `.grid.csv`, `.overlap.csv`, `.delta.csv`, `.regression.csv`, `.ic.csv`,
`.walkforward.csv`

---

## Corpus and parameters

546 backtests: 3 panels (u56 / broad / small) × 7 book shares × 13 books per cell (1 no-tilt
control + 6 keys × 2 tilt directions), literal `GROSS/n` on the whole share grid plus a
gross-normalised control on `m ≤ 0.53`. Each book run **once at 0 bps**, the 10 and 25 bps rungs
derived from the engine's own identity `r_c = r_0 − turnover·c/1e4` (verified below at exactly
zero), so gross and net legs of every comparison are the *same* book. Weekly, t+1, 75% gross, no
shorting, no leverage.

**Exactly two tuned parameters, both swept exhaustively, every grid point printed:** the book
share `m ∈ {0.05, 0.10, 0.20, 0.35, 0.53, 0.75, 1.00}` (idea 153's own share→n map, so `m = 0.53`
is `n = 20` on u56 — the incumbent — exactly) and the tilt direction `∈ {NEG, NONE, POS}`. The
KEY is a **reported axis, never selected on**, the way idea 153 reported panels; panels, cost
rungs, the construction axis and the OOS window likewise.

The six keys, applied as `score = comp / g`, `comp`, `comp × g`:

| key | multiplier `g` | note |
|---|---|---|
| VOL | `clip(vol20, 0.08) ** 0.5` | idea 153 VERBATIM; `VOL/NEG` **is** RULES v1's live scaler |
| VOLR | `clip(rank_pct(vol20), 0.05, 1) ** 0.5` | same key on the common footing |
| MOM | `clip(rank_pct(12−1 momentum), 0.05, 1) ** 0.5` | the composite's own leg |
| R6 | `clip(rank_pct(6m return), 0.05, 1) ** 0.5` | the composite's own leg |
| R3 | `clip(rank_pct(3m return), 0.05, 1) ** 0.5` | the composite's own leg |
| **RAND** | `clip(rank_pct(RW6), 0.05, 1) ** 0.5` | **the decisive control.** `RW6` is the 126-day change of a synthetic geometric random walk per name (seed 158, daily vol = the panel's own median), built with R6's exact functional form so it matches the real keys' persistence and turnover, and carrying zero information by construction |

## Reproduction — 8 of 8 exact, asserted before any new number was read

| check | published | this run |
|---|---|---|
| [a] mean weekly eligible, u56 / broad / small | 37.50 / 91.46 / 141.23 | 37.50 / 91.46 / 141.23 |
| [b] INV-vs-NONE held-set overlap at n=20, u56 / broad | 69.4% / 42.5% | 69.4% / 42.5% |
| [c] `NONE / n=20 / u56 @10bps` | 12.65974% / 1.09214 / −18.30835%, halves 1.08828 / 1.10155 | identical to every printed digit |
| [d] cost identity vs a fresh 10 bps engine run | — | **max\|diff\| 0.00e+00** |
| [e] RULES v1 u56 @10bps | 6.45305% / 0.66418 / −13.82780% | identical |

So the control arm here is literally idea 81/153/159/168's control arm, and the anchors idea 153
built its claim on are reproduced before the claim is tested.

---

## (1) THE ANSWER — the direction is arithmetic, the strength is not

**P3 (the decisive, pre-registered test) HELD.** Within every key, with `m` the only thing that
moves, `Spearman(overlap, |dSharpe|)` is **negative in 36 of 36 (panel, key, cost) cells** on the
full grid and **negative in 24 of 24** large-cap cells on the `m ≤ 0.53` subgrid — including for
RAND (−0.636, −0.673, −0.055, −0.455). A book that holds more of its panel expresses less of
*any* key, a real one or a synthetic one. That half of idea 153 is a genuine mechanism.

**P4 FAILED, and it is the informative failure.** Idea 153 reported R² 0.43–0.60 for overlap
against the key's own slope-t at 0.01–0.11, and read that as *share, not key strength, prices a
tilt*. Re-run key by key on `m ≤ 0.53`, literal book:

| key | slope of \|dSharpe\| on overlap | t | R² |
|---|---|---|---|
| VOL | −0.4279 | −6.60 | 0.429 |
| VOLR | −0.7276 | −7.16 | 0.469 |
| MOM | −0.2984 | −8.43 | 0.551 |
| R6 | −0.3859 | −8.91 | 0.578 |
| R3 | −0.1903 | −6.95 | 0.454 |
| **RAND** | **−0.1341** | **−2.09** | **0.070** |
| (pooled, idea 153's own reading) | −0.3354 | −13.55 | 0.339 |

RAND's slope is negative with |t| > 2 — the sign half of P4 held — but its R² is **0.070 against
the five real keys' mean 0.496, i.e. 14% of it**, far under the pre-registered "at least half"
bar. On |dCAGR| the same split: RAND 0.228 vs a real-key mean of 0.596.

**So idea 153's R² is a JOINT product of arithmetic and the key being real, not a measurement of
share alone.** Overlap tells you the direction in which a tilt's magnitude decays for any key
whatever; it explains that magnitude tightly only when the key has something to express. The
project may keep "a book holding half its panel cannot express a ranking"; it may **not** keep
"book share prices a tilt better than key strength does" on the strength of one key's R².

**P5 HELD but weakly, and is reported as such.** Across the six keys, `Spearman(|rank IC|,
mean |dSharpe|)` is **+0.488** on average over the 6 (panel, cost) cells (range +0.290 to +0.638)
against `Spearman(overlap, mean|dSharpe|)` at **−0.362**. Neither dominates. With six keys a
Spearman is nearly uninformative, and the honest reading is that key strength and book share BOTH
carry some of it — which is exactly what P4's split says.

**P2 FAILED, narrowly and harmlessly:** overlap is monotone increasing in `m` in **34 of 36**
(panel, key, direction) cells; the two exceptions are `u56/MOM/POS` and `u56/R6/POS`, which dip by
under 0.01 at small `m` where the book holds 2–4 names.

## (2) A ZERO-INFORMATION KEY MOVES SHARPE AS MUCH AS A REAL ONE

Mean |dSharpe| pooled over the share grid, u56 @ 10 bps: **RAND 0.0794** against MOM 0.0723,
R3 0.0745, R6 0.0409, VOL 0.1077, VOLR 0.1847. On broad @ 10 bps: RAND 0.0545 against MOM 0.0265,
R3 0.0414, R6 0.0515, VOL 0.0882.

The keys' own information is real and correctly measured — weekly rank IC vs the forward 21d
return inside the gate: VOL +0.0912 (t +8.74) on u56, MOM +0.0613 (t +5.68), R6 +0.0539, R3
+0.0461, **RAND −0.0233 (t −3.87)**, i.e. the synthetic key is, if anything, mildly *adverse* on
this path. It still moves the book's Sharpe by as much as the informative keys do.

**The consequence for the record: the SIZE of a tilt's effect on Sharpe is not evidence that the
key is real.** Any past reading of the form "the tilt moved Sharpe by X, so the key does
something" is unsupported unless a null key was run alongside it. This run is the first time the
project has had that control.

## (3) EIGHTH DELETE-THE-SCALER FINDING, AND THE STARKEST FRAMING YET

Mean **signed** dSharpe over all 28 large-cap (panel, share, cost) cells:

| arm | mean dSharpe | cells > 0 |
|---|---|---|
| **VOLR / NEG** | **−0.3306** | 0 of 28 |
| **VOL / NEG — the LIVE scaler** | **−0.1931** | **0 of 28** |
| R3 / NEG | −0.1059 | 0 of 28 |
| MOM / NEG | −0.0978 | 4 of 28 |
| R6 / NEG | −0.0906 | 2 of 28 |
| RAND / POS | −0.0531 | 7 of 28 |
| **RAND / NEG** | **−0.0321** | 8 of 28 |
| R3 / POS | −0.0336 | 5 of 28 |
| MOM / POS | +0.0066 | 14 of 28 |
| R6 / POS | +0.0102 | 12 of 28 |
| VOLR / POS | +0.0136 | 15 of 28 |
| VOL / POS | +0.0293 | 20 of 28 |

**A random key beats the live `/sqrt(vol20)` scaler in 27 of 28 large-cap cells tilted NEG and 23
of 28 tilted POS.** The live tilt is the second-worst of twelve arms and never once positive. At
the incumbent's own point (u56, `m = 0.53`, `n = 20`, 10 bps) all twelve tilts are negative and
the live one is the largest loser but two: `VOL/NEG` −0.0963 dSharpe / −2.76 pp CAGR against
`RAND/NEG` −0.0222 / −0.81 pp.

This is the eighth independent delete-the-scaler result (after ideas 1, 2, 72, 82, 141, 159, 160,
168) and the first stated against a null control rather than against the unscaled composite. It
adds nothing to the *direction* of the recommendation and a great deal to its force.

## (4) BOTH KEEP PATHS, all 546 books — and the control passes them

4a **164 of 546**; 4b full-sample **54 of 546**; 4b on the OOS window alone **98 of 546**. Every
4b pass is 10 bps and large-cap; **0 of 182 small-panel books passes anything** (seventh
reproduction of idea 136).

**P6 FAILED, and the failure is the point.** 19 `(m, key, dir)` combinations pass 4b on two
panels — and **four of them are the RANDOM key**: `m=0.35/RAND/NEG`, `m=0.53/RAND/NEG`,
`m=0.53/RAND/POS` and (single-panel) `m=0.05/RAND/POS` at 17.6% / 1.059 / −17.1%, halves
1.147 / 0.979, OOS Sharpe 1.007. `RAND` books account for **11 of the 54** full-sample 4b passes
— more than VOL's 5 and VOLR's 5, and more than any single real key's.

Nothing here is proposed and nothing is a KEEP-candidate. Every passing book is idea 153's
already-published family (the untilted composite at `m` ≈ 0.53–0.75) perturbed by a tilt that,
on the evidence of the RAND column, is indistinguishable from noise. That a zero-information book
clears PROTOCOL's cross-universe 4b at the same rate as the real ones is a fact about **the bar**,
not about the book, and it is recorded here as such.

## (5) Rule 8 walk-forward — the selector cannot tell a real key from a synthetic one

`(m, key, dir)` chosen on 2009–2016 only, read ONCE on 2017-01-01 → 2026, 6 (panel, cost) cells:

| selector | mean OOS Sharpe | OOS CAGR | OOS MaxDD | OOS-4b passes |
|---|---|---|---|---|
| S1 IS-Sharpe argmax over all 91 arms | **0.7230** | 10.57% | −22.81% | 0 of 6 |
| S2 do nothing (untilted, `m = 0.53`) | **0.8149** | 9.61% | −21.50% | **3 of 6** |
| **S3 IS-Sharpe argmax over the RANDOM key only** | **0.7240** | 9.17% | −22.67% | 0 of 6 |
| S4 IS-Sharpe argmax over the untilted arms | 0.7808 | 11.10% | −22.48% | 0 of 6 |
| RULES v1 | 0.4514 | 4.86% | −25.30% | — |
| SPY | 0.8820 | 15.45% | −33.72% | — |

Large-cap only (4 cells): S1 0.9434, **S2 1.0430**, S3 0.9523, S4 1.0027.

**A selector allowed to fit only a synthetic key (S3, 0.7240) is indistinguishable from — in fact
0.001 ahead of — the selector allowed to fit all 91 arms (S1, 0.7230).** Both lose to doing
nothing by ~0.09 of OOS Sharpe, and S1 beats S2 in only 2 of 6 cells. On `broad @ 10 bps` the
IS-Sharpe argmax over every arm **is** a random-key book (`RAND/POS, m = 0.20`), so S1 and S3 are
byte-identical there; it reads OOS 11.44% / 0.876 / −17.2% against the do-nothing control's
12.00% / 1.038 / −18.9%. Keys picked by S1 across the 6 cells: NONE 2, VOLR 2, RAND 1, MOM 1.

This is the sixth instance (after ideas 110, 151, 132, 166, 168, 170) that an IS-fitted selector
does not beat the constant it was meant to improve on, and the first in which the selector is
shown to be picking *noise* rather than merely picking badly.

## Predictions — outcome

| | prediction | outcome |
|---|---|---|
| P1 | reproduction [a]–[e] holds | **HELD, 8 of 8 exact** |
| P2 | overlap monotone in share in every cell | FAILED (34 of 36; both misses < 0.01 at n ≤ 4) |
| P3 | within every key incl. RAND, \|dSharpe\| falls with overlap | **HELD (36/36, and 24/24 large-cap on m ≤ 0.53)** |
| P4 | RAND's slope negative, \|t\| > 2, R² ≥ half the real keys' | **FAILED on the R² half** (slope −0.134, t −2.09, R² 0.070 vs 0.496) |
| P5 | key strength does NOT order the tilt | HELD, weakly (+0.488 vs overlap's −0.362; six keys) |
| P6 | no cross-universe 4b pass | **FAILED — 19 combinations, 4 of them the RANDOM key** |

## What PROTOCOL should take from this (offered, not adopted)

A reporting clause in the spirit of idea 159's: **any claim that a ranking key does something must
be accompanied by a null-key control run on the same grid.** This run's `RAND` column shows that
|dSharpe|, the count of 4b passes and the rule-8 selector's own pick are all reachable by a key
with zero information, so none of the three is by itself evidence about a key. The clause costs
one extra column and would have caught the inference in several prior entries.

## Caveats, carried not buried

* Survivorship: all three panels are current-constituent lists (idea 54).
* Ideas 39/49: the eligibility gate is **inverted** on the small panel, so its numbers describe a
  gate that does not work there; reported, never traded. Its 4b count is 0 of 182 regardless.
* Idea 38 (calendar-day price index) and idea 126 (t+1 only, no spread or impact model) carry.
* Idea 128: the IS window's SPY drawdown is shallower than the OOS window's, which biases every
  rule-8 selector here identically.
* `m` is a sample-average share, not point-in-time; idea 157 (open) owns the time-varying variant.
* MOM/R6/R3 are legs of the composite itself, so their books overlap the control more at every
  share than an unrelated key's would. This was declared before the result and is why the decisive
  statistic is the WITHIN-key one, where `m` is the only mover; the pooled fit is reported for
  comparability with idea 153 and read second.
* **RAND is ONE draw of a random key**, on one realised path, measured once. The 27-of-28 and
  4-of-19 counts above are properties of that draw. A repeated-draw version of this control is
  the obvious follow-up and is queued.
