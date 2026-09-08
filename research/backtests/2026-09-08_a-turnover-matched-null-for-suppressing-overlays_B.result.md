# idea 203 — a-turnover-matched-null-for-suppressing-overlays (lane B, 2026-09-08)

**Verdict: ANSWERED / SPLIT. Idea 203's proposed null is KILLED (it makes the problem *worse*).
An approximately turnover-matched null (RS16) is built and validated; an *exactly* matched one
cannot exist for this indicator. The clause-as-a-gate is KILLED again, under all six nulls.
No RULES change, no PROTOCOL edit, no KEEP, no memo.**

> **READ THE CONCORDANCE AT THE END OF THIS FILE BEFORE QUOTING §1–§2.** The concurrent cloud run
> (`13b6106`) showed that idea 186's fidelity ratio divides by the *overlaid* book's turnover, which
> a suppressing overlay drives toward zero — so **the 2036.8% / 4759.3% headline figures below
> carry a denominator artefact**, as does idea 191's 1782.7%. On the corrected, overlay-independent
> denominator (recomputed from this run's own grid) rotation is within **6.88%** and RS16 within
> **0.30%**. The *ordering* of the nulls and every KEEP / rule-8 count below are unaffected.

Script `2026-09-08_a-turnover-matched-null-for-suppressing-overlays_B.py` · 7,260 grid rows
(60 real) + 1,260 size-control rows · 208 s · deterministic.

---

## What was asked and what came back

Idea 186's clause-11 null for an overlay `(s, A)` is the same action `A` on a **circular rotation**
of the ON indicator. It preserves on-share and episode structure exactly, and realised turnover to
1.25% (DDCTL) / 0.82% (SLEEVE) — but **not** for BUDGET-**skip**, the action that suppresses a
rebalance. Idea 203 proposed replacing rotation with a **resample of the skip decisions at matched
count**. That proposal is tested here against the one-parameter family that contains it:

> **RS-B** — stratify the J rebalance dates into B equal-count strata by the **ex-ante
> target-to-target turnover** `tt_j = |w_j − w_{j−1}|₁` of the untreated base book (known at
> decision time, identical for the real overlay and every draw, so it peeks at nothing), then draw
> — independently in each stratum — exactly as many skip dates as the real overlay has there.
> **B = 1 is idea 203's literal proposal** (count-matched, turnover-blind); **B → J** matches the
> ex-ante turnover profile of the skipped set exactly.

Two tuned parameters, all points reported: `tau ∈ {0.05, 0.10, 0.20, 0.30, 0.50}` (idea 191's
widened ladder) × `B ∈ {1, 2, 4, 8, 16}`. Corpus axes: 3 panels × 2 actions (skip / half) × 2 cost
rungs. Nulls: ROT (idea 186's rotation, at idea 186's own offsets) + RS1/RS2/RS4/RS8/RS16, 20 draws
each. Base book: idea 2's top-20 EW composite, no vol scaler, gross 0.75, weekly, t+1.

---

## 1. Idea 203's null makes it WORSE — the count is not the binding statistic

Realised turnover gap, mean `|null − real| / real`, pooled over panels / tau / rungs:

| kind | BUDGET-**skip** | BUDGET-half (control) | skip, median | skip, excl. the on-share>0.9 corner |
|---|---|---|---|---|
| ROT (incumbent) | 2036.8% | 4.4% | 24.8% | 20.7% |
| **RS1 (idea 203's ask)** | **4759.3%** | 4.8% | 29.9% | 30.9% |
| RS2 | 4277.4% | 2.2% | 8.7% | 17.2% |
| RS4 | 3475.8% | 1.0% | 1.5% | 7.5% |
| RS8 | 2425.9% | 0.4% | 0.5% | 1.3% |
| **RS16** | **1.6%** | **0.1%** | **0.5%** | **1.4%** |

**RS1 is worse than rotation in 26 of 30 skip cells (sign test p = 5.9e-05) and 24 of 30 half cells
(p = 1.4e-03).** Matching the *count* is what rotation already does; what breaks fidelity is *which*
dates are suppressed, and rotation at least preserves the episode structure that correlates weakly
with turnover. **Idea 203's proposal as written is a KILL.**

**P2 recorded as a MISS in the letter and a HIT in the spirit:** the pre-registration said RS1 would
not repair the gap and would land within a factor of two of ROT; it does not repair it and lands at
**2.34×** — outside the stated band, in the wrong direction.

## 2. The blow-up is one corner, and RS16 removes it

Gap by on-share bin, BUDGET-skip:

| on-share | ROT | RS1 | RS2 | RS4 | RS8 | RS16 |
|---|---|---|---|---|---|---|
| (0.0, 0.1] | 1.8% | 1.8% | 1.1% | 0.7% | 0.3% | 0.2% |
| (0.1, 0.3] | 8.3% | 8.5% | 3.7% | 1.0% | 0.2% | 0.3% |
| (0.3, 0.5] | 16.5% | 18.0% | 4.5% | 0.6% | 0.5% | 0.2% |
| (0.5, 0.7] | 22.6% | 26.7% | 5.5% | 1.2% | 0.7% | 0.7% |
| (0.7, 0.9] | 41.2% | 69.3% | 44.9% | 20.8% | 3.0% | 3.5% |
| **(0.9, 1.0]** | **10101%** | **23673%** | **21318%** | **17349%** | **12124%** | **2.6%** |

Idea 191's "degrades without bound in on-share" is **confirmed and localised**: at `tau = 0.05` the
overlay skips ~99% of rebalances, so the real book barely trades and any null that trades at all
divides by ~0. The gap is **not monotone in B** — it is a cliff (4759 → 4277 → 3476 → 2426 → **1.6**%),
because B = 16 is the first stratification fine enough to force the null's skips onto the same
high-turnover dates. **P3 MISS** on the monotonicity claim; the shape is the finding.

**RS16 is better than rotation in 30 of 30 cells on BOTH actions (p = 1.9e-09)** and its 1.6% mean /
0.5% median beats rotation's own 4.4% on the *non-suppressing* action — the fidelity target idea 186
set. So an *approximately* turnover-matched null for a suppressing overlay exists — it is not
"matched count", it is **matched ex-ante turnover profile**. (An *exactly* matched one does not:
see the concordance. RS16 reaches its fidelity by overlapping the real skip set 87.5% of the time.)

## 3. What the fidelity costs, measured

| kind | ex-ante gap | overlap with the real skip set | null band (mean max\|dSharpe\|) | signed clear rate |
|---|---|---|---|---|
| ROT | 0.2952 | 0.5408 | 0.1664 | 36.7% |
| RS1 | 0.2938 | 0.5407 | 0.1481 | 53.3% |
| RS2 | 0.1637 | 0.6488 | 0.1581 | 33.3% |
| RS4 | 0.1014 | 0.7458 | 0.1453 | 16.7% |
| RS8 | 0.0653 | 0.8048 | 0.1380 | 6.7% |
| RS16 | 0.0407 | **0.8748** | 0.1322 | 13.3% |

Because the BUDGET indicator **is** a threshold on the stratifying variable, exactly **one** stratum
ever straddles the threshold — `free_strata ≡ 1` at every B — so as B grows the randomisation is
squeezed into a shrinking window and **87.5% of RS16's "random" skip dates are the real ones**. In
**1 of 15 (panel, tau) cells** (SMALL439 / tau = 0.05) RS16 has **zero** free strata: the null is
*bit-identical to the instrument* (6.7% of its skip draws have overlap 1.0). That is the wall, and
it is a wall in the mechanism — but **P4 is a MISS as stated**: the clause does not lose all power at
the fidelity target. It loses about two thirds of it (36.7% → 13.3%), which is a price, not a veto.

## 4. Size control — under-powered, and it does not carry the kill

A zero-information overlay (random ON, on-share matched, U56, 20 cells per kind) against a nominal
1/21 = 4.76%: ROT 0/20, RS1 2/20, RS2 0/20, RS4 3/20, RS8 2/20, RS16 0/20. **P5 MISS**, but at n = 20
P(≥2) = 0.246 and P(≥3) = 0.067 — **not significant**, and stated as such. The intermediate nulls
*lean* anti-conservative; the KILL of RS1 rests on fidelity (26/30, p = 5.9e-05), not on this.

## 5. Rule 8 — the clause is still not a gate, under any null

12 cells = 3 panels × 2 actions × 2 rungs; tau chosen on ≤ 2016-12-31, 2017-2026 read once.

| arm | OOS CAGR | OOS Sharpe | OOS MaxDD | dOOS vs do-nothing | t | wins | beats SPY |
|---|---|---|---|---|---|---|---|
| ORACLE-OOS (hindsight) | 11.38% | 0.8102 | −25.42% | +0.0336 | +1.75 | 9/12 | 7/12 |
| **S0 do-nothing** | **10.22%** | **0.7766** | **−23.53%** | — | — | — | 4/12 |
| S2 RS1 | 10.06% | 0.7524 | −24.58% | −0.0242 | −1.66 | 2/12 | 4/12 |
| S2 RS2 | 10.16% | 0.7475 | −24.98% | −0.0291 | −2.70 | 1/12 | 5/12 |
| S2 RS4 | 9.97% | 0.7435 | −25.00% | −0.0331 | −2.16 | 0/12 | 4/12 |
| S2 RS16 | 9.92% | 0.7375 | −25.96% | −0.0391 | −2.31 | 4/12 | 4/12 |
| S2 ROT | 9.78% | 0.7234 | −25.05% | −0.0532 | −2.48 | 1/12 | 3/12 |
| S1 IS-argmax | 9.50% | 0.7177 | −27.51% | −0.0589 | −1.87 | 4/12 | 5/12 |
| S2 RS8 | 9.53% | 0.7018 | −25.01% | −0.0748 | −2.43 | 0/12 | 2/12 |

SPY OOS 15.45% / 0.8820 / −33.72%. **P6 HIT: 6 of 6 clause-gated arms lose to doing nothing**, the
twelfth consecutive instance (110/132/151/166/171/174/175/181/186/191/204). Note **ORACLE-OOS buys
only +0.034 of OOS Sharpe** — perfect hindsight over the whole tau ladder is worth almost nothing,
so the BUDGET family has no headroom for any selector to find.

## 6. Both KEEP paths — nothing

| kind | rows | 4a vs RULES v2 | 4a vs RULES v1 | 4b vs SPY | BOTH |
|---|---|---|---|---|---|
| real | 60 | **0** | 8 | 9 | **0** |
| ROT | 1200 | 0 | 204 | 314 | 0 |
| RS1 | 1200 | 0 | 224 | 323 | 0 |
| RS2 / RS4 / RS8 / RS16 | 4800 | 0 | 666 | 1056 | 0 |

Real rows by panel: U56 4b 9/20, BROAD136 0/20, SMALL439 0/20 (**P7 HIT**). All nine 4b passes are
U56 **'half'** rows; **no skip overlay passes 4b anywhere.** Best: U56 / tau 0.05 / half / 10 bps —
CAGR 13.25%, Sharpe 1.1207, MaxDD −18.17%, H1/H2 1.1149/1.1325, OOS 1.2057, vs SPY 15.23% / 0.889 /
−33.72%. It is **not a candidate**: the effectively-untreated book (tau 0.50, on-share 0.41%) already
scores 1.0913 / OOS 1.1464 / −18.18%, so the overlay adds +0.029 full-sample Sharpe inside a null band
of ~0.13, and the ROT clause clears 'half' at 3.3%. **4b here is a property of idea 2's base book, not
of the instrument** — idea 186's P7, reproduced.

---

## Reproduction gates

| gate | result |
|---|---|
| [a] `fast_backtest`/`_core` vs `engine.backtest` | max\|dret\| 2.776e-17, max\|dturn\| 4.441e-16 — **PASS** |
| [b] cost identity, 10 bps derived from the 0 bps run | 2.776e-17 — **PASS** |
| [c] base CAND-20 weights vs idea 78/171 `weights_cand` | 0.000e+00 — **PASS** |
| [d] `mstats` (numpy) vs `engine.metrics` | 0.000e+00 — **PASS** |
| [e] ROT arm vs idea 186's committed grid | 756/756 rows matched; **672 with an identical ON set at max\|dSharpe\| 2.942e-04** — **PASS (bounded)** |
| [f] null validity | skip-count mismatches **0/7200**; per-stratum count mismatches **0/9300** — **PASS** |

**Gate [e]'s residual is a data revision, not a code difference.** `data/prices.csv` was re-committed
by the daily Actions job on 2026-09-07, after idea 186 ran. 84 rows (tau = 0.10) have an ON set that
moved by **1 of 975** rebalance dates — the revision flipped one date's composite across the 0.10
threshold — and their drift is bounded at max\|dSharpe\| **0.0719**, max\|dMaxDD\| **0.0632**. Reported,
not absorbed. Idea 424 carries the same caveat for its own source.

**Not reproducible, and said so:** idea 191's published **1782.7%**. Idea 208 established that idea 191
salted its rotation offsets with Python's per-process `hash()`, so that figure is not a fixed
quantity. Re-measured here at a fixed seed on the same ladder: **2036.8%** (sd across the 30 cells
7568.6%, se 1381.8%) — same order, same conclusion, and the statistic's dispersion is now on the
record. On idea 186's narrow 3-point ladder this run reads 45.2% mean / **213.8%** max against idea
186's published 25.4% / 213.8% (which pooled both actions).

## Recommendation for PROTOCOL clause 11 (proposed only — **PROTOCOL.md, RULES.md, scan.py, bot.py and baseline.py untouched**)

1. **Do not adopt a count-matched skip resample.** It is measurably worse than the rotation it would
   replace (26/30, p = 5.9e-05).
2. For a **schedule-suppressing** overlay, the matched null is the **ex-ante-turnover-stratified
   resample at B = 16** (RS16): fidelity 1.6% mean / 0.5% median, better than rotation's own fidelity
   on a non-suppressing action, size 0/20 on a known null.
3. It must be published **with its overlap and its free-stratum count**. An RS-B null whose overlap
   is 0.87 is a weak test, and one with zero free strata **is the instrument** — that case occurred
   in 1 of 15 cells here and must be reported as inert, never as a clean pass.
4. **Report-only, in every form.** Under all six nulls the clause loses to doing nothing out of
   sample (−0.024 to −0.075 of Sharpe, 6/6). It is a description of an instrument, not an admission
   rule.

## Caveats

Survivorship: all three panels are current-constituent lists (idea 54); SMALL439 contains no
delistings — real and null draws inherit the bias identically so the *comparison* is unaffected, the
*level* of every number is not. 20 draws give a nominal one-sided size of 4.76% that is approximate
(idea 214). Idea 211's signed reading is primary; the two-sided is reported for comparability with
idea 186. Idea 38 (calendar-day index) and idea 126 (t+1 only) carry. Idea 144: an overlaid book is
the same book with an instrument on it, not a new book.


---

# CONCORDANCE with the concurrent cloud run (filed 2026-09-08 by lane B, after the fact)

The cloud lane ran idea 203 independently and landed at `13b6106`, after this run. Both runs are on
the record; this section reconciles them and **corrects this run's headline where the cloud run is
right**.

## Where the two runs agree (independent constructions, same conclusion)

| claim | lane B (this run) | cloud |
|---|---|---|
| idea 203's matched-count null is a **strict downgrade** on rotation | worse in **26/30** skip cells, p=5.9e-05; 2.34x the mean gap | MC fid/base **10.3%** vs ROT **6.8%**; switch match 8.0% vs 100% |
| the pathology is specific to **suppression** | 'half' ROT gap **4.43%** | 'half' ROT **4.4%** |
| clause verdicts / rule 8 | 6 of 6 clause-gated arms lose to do-nothing | better-matched null changes no verdict, 0/60 vs 0/60 |
| KEEP | 4a **0/60**, 4b **9/60** real | 4a **0/60**, 4b **9/60** |
| the 4b passes belong to the **base book**, not the overlay | untreated book already 1.0913 / OOS 1.1464 | same conclusion, PARKed as partial rebalancing |

## Where the cloud run is right and this run's headline was wrong

**Idea 186's fidelity ratio divides by the *overlaid* book's own turnover, which a suppressing
overlay drives toward zero.** This run *observed* that mechanism (it is why the on-share>0.9 bin
reads 10101%) and reported the corner separately — median 24.8%, excl-corner mean 20.7% — but still
led with **2036.8%**, which therefore carries the artefact. The cloud run's fix is the right one:
divide by an **overlay-independent** denominator, the untreated base book's turnover.

Recomputed here from this run's own committed `.grid.csv` (base turnover/yr: U56 9.456, BROAD136
13.655, SMALL439 20.215), 30 skip cells per null:

| null | fid ÷ real (this run's published form) | **fid ÷ base** | fid ÷ base, max |
|---|---|---|---|
| ROT (incumbent) | 2036.77% | **6.88%** | 12.90% |
| RS1 = the cloud run's MC | 4759.34% | **10.33%** | 18.50% |
| RS2 | 4277.40% | 6.02% | 16.50% |
| RS4 | 3475.77% | 3.49% | 13.72% |
| RS8 | 2425.89% | 1.81% | 9.75% |
| **RS16** | 1.64% | **0.30%** | **1.39%** |

**This reproduces the cloud run to the tenth of a percent on every overlapping quantity** — ROT
6.88% vs its 6.8% (max 12.90% vs 13.6%), MC/RS1 10.33% vs its 10.3%, 'half' ROT 3.32% vs its 3.3%.
Two independent implementations, same numbers. **So: rotation was never as broken as idea 191's
1782.7% says, and this run's 2036.8% restates that artefact rather than correcting it.** The cloud
lane's correction stands and is adopted here.

## Where this run adds something the cloud run's frontier does not show

The cloud run concludes the requested null **cannot exist**, because BUDGET's ON set *is* the top-K
dates by `tt`, so the only *exactly* turnover-matched matched-count draw is the overlay itself. That
is correct, and it is this run's `free_strata == 1` result stated more sharply. **This run's RS16 is
not a counterexample to it** — it buys fidelity with overlap (0.875) exactly as that argument
predicts, and the claim in §2 above that RS16 is "the replacement that does work" is **too strong
and is withdrawn in that form**.

But the *approximate* frontier is much better than the cloud run's `STRAT(f)` dial suggests. On the
cloud run's own honest denominator, `STRAT(0.75)` reads **7.5%** — worse than the ROT it would
replace — whereas **RS16 reads 0.30% mean / 1.39% max and beats ROT in 30 of 30 skip cells.** The
two constructions differ: `STRAT(f)` draws K dates from the top-M by `tt` (matching the *identity*
of high-turnover dates loosely); RS-B stratifies **all** J dates and matches the per-stratum count
across the whole `tt` distribution. On this evidence the per-stratum-count construction dominates
the top-M construction by more than an order of magnitude on the corrected metric.

## Net reading of idea 203 after both runs

1. **The queue's proposal is killed twice, independently** — that part needs no revision.
2. **Idea 191's 1782.7%, and this run's 2036.8%, are both denominator artefacts.** Any future
   fidelity claim must divide by the untreated base book's turnover. On that metric rotation is
   within 6.9% and was never the problem the queue assumed.
3. **An exactly turnover-matched null cannot exist** for an indicator that is a threshold on
   turnover (cloud), but the approximate frontier has a usable corner at RS16 (0.30% ÷ base at 0.875
   overlap) that neither `STRAT(f)` nor rotation reaches — a genuinely open follow-up, since RS16's
   power cost (clear rate 36.7% -> 13.3%) has not been priced on the corrected denominator.
4. Untested here and claimed by the cloud run as the one improvement available: **RUN**, the
   run-length permutation (fid/base 6.8%, max 12.6%, switch match 100%). RS16 beats it on fidelity;
   RUN beats RS16 on overlap. Neither run has compared them directly.
