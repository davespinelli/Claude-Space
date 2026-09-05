# Idea 145 — weak-dominance-bands-as-the-calibration-output (lane C, 2026-09-05)

**Verdict: ANSWERED — the band exists, it is the right thing to publish, and deriving it kills
the premise it was derived from.** Idea 131's `gamma in [0.57, 0.61]` band came from **swapping
the statistic** (CAGR → mean gross), not from re-calibrating a coefficient: in its own units the
published CAGR floor has **no strictly dominating value at all**, and its indifference band is
**0.0054 wide**. What the exercise does turn up is three things nobody had measured:

1. **The drawdown cap, not the CAGR floor, is 4b's largest sole cause of KILL** — 47 rows vs 27,
   **61.8% vs 48.2%** of arms clearing the bar's own other four. Idea 129's famous "48%" is the
   *second* biggest.
2. **4b's OOS Sharpe bar is redundant on this corpus.** 0 sole victims, and its indifference band
   is **unbounded below**: setting sigma_OOS to anything at or below 1.0520 — including deleting
   the bar outright — changes **neither the admitted set nor the ladder leakage**.
3. **The five bands differ in width by three orders of magnitude** (0.0033 to unbounded), so
   there is no single "quote +/- x" convention; the memo proposes quoting each band as measured.

And the band is **out-of-sample inert for selection**: every coefficient anywhere inside its own
IS-derived band moves **0 of 18 rule-8 picks** and leaves OOS Sharpe at 1.022 to three decimals.

## Harness and reproduction

Idea 94's script is **imported, not re-implemented**; ideas 129/131's corpus is reproduced
**exactly** before any new number is read. Corpus = 3 panels (u56, broad, small) x 3 books
(V1u, TOP20, EWall) x 17 arms x 2 cost rungs = **306 arm-rows**, plus the 19-point static-gross
ladder per cell (**342 rows**) as the pure de-grossing leakage control. Weekly, t+1, 75% target
gross, IS <= 2016-12-31, OOS >= 2017-01-01.

| check | result |
|---|---|
| (a) `H.run` vs `engine.backtest`, ungated EWall u56 | max abs diff **0.00e+00** — PASS |
| (b) idea 94's published `EWall+vol60-dg` u56 @10bps (11.6% / 1.133 / −16.9%) | **11.587% / 1.133 / −16.884%** — PASS |
| (c) idea 129/131 census: 306 rows / 82 Pareto / 29 pass 4b / 27 floor-only / 11 of 23 on the frontier / 342 ladder / 97 ladder floor-only at m ≤ 0.80 / **ladder0 = 10** | **all ten exact** — PASS |
| (d) idea 129's IS-screen groups A / B / C | **45 / 9 / 252** — PASS |

An early version of this run inverted the drawdown comparison and produced 47 passes instead of
29; check (c) caught it before any band was read. That is what the checks are for, and it is
recorded rather than quietly fixed.

**Tuned parameters — never more than two at once.** Q2 sweeps **one** coefficient at a time with
the other four pinned at their published values. Q3 is the single two-parameter map (phi x delta),
the pair idea 129 already published. Every grid point is printed. Band **endpoints are computed
analytically**: each bar is monotone in its own coefficient, so the admitted set can only change
at the finitely many per-row crossing values, which makes the bands exact rather than a function
of grid resolution — and makes "unbounded" a *proof*, not an artefact of where the scan stopped.

## Q1 — what each bar is actually doing at the published point (1.00, 1.00, 1.00, 0.60, 0.70)

29 of 306 rows pass 4b; 97 pass 4a; 6 pass both; **10 of 342 ladder points** pass (the leakage).

| bar | coef | sole victims | of which Pareto-best | also pass 4a | ladder points it alone excludes | share of arms clearing the other four |
|---|---|---|---|---|---|---|
| H1 | 1.00 | 1 | 0 | 0 | 0 | 3.3% |
| H2 | 1.00 | 2 | 1 | 2 | 0 | 6.5% |
| **OOS** | 1.00 | **0** | 0 | 0 | **0** | **0.0%** |
| **DD** | 0.60 | **47** | 4 | 7 | **26** | **61.8%** |
| CAGR | 0.70 | 27 | 11 | 19 | 97 | 48.2% |

Two corrections to the project's picture fall straight out of this table.

**The DD cap is the bigger exclusion.** Idea 129 established the CAGR floor as the sole cause of
KILL for 48% of otherwise-qualifying arms and built two follow-up ideas on it. The drawdown cap
does the same to **61.8%** — more rows (47 vs 27) — and has never been named as such. It is also
doing more of the leakage work per unit of exclusion than that framing suggests: it alone
excludes 26 ladder points.

**The OOS Sharpe bar excludes nothing.** Not one row in 306 fails 4b on the OOS bar alone, and
not one ladder point does either. Every row it would reject is already rejected by H1, H2, DD or
CAGR. On this corpus it is a **free bar** — which is not the same as saying it should be dropped
(see the caveat on what a corpus census can and cannot support).

## Q2 — the bands, one coefficient at a time (all grid points in `.bands.csv`)

Definitions, generalising idea 131's three criteria to any bar: (1) lose none of the published
29 admissions; (2) save sole victims, especially Pareto-best ones; (3) admit no more ladder
points than the published 10. **INDIFFERENCE** = admitted set *and* leakage identical.
**WEAK** = (1) and (3). **STRICT** = weak, plus a strict gain on (2) or (3).

| bar | published | indifference band | width | weak band | strictly dominated? |
|---|---|---|---|---|---|
| H1 | 1.00 | [0.9974, 1.0453] | 0.0479 | (−inf, 1.0453] | **no** |
| H2 | 1.00 | [0.9829, 1.0213] | 0.0383 | (−inf, 1.0905] | yes, **in both directions** |
| OOS | 1.00 | **(−inf, 1.0520]** | **unbounded** | (−inf, 1.1447] | yes, tighter: [1.0522, 1.1447] |
| DD | 0.60 | [0.5979, 0.6012] | **0.0033** | [0.5969, 0.6012] | yes, tighter: [0.5969, 0.5978] |
| CAGR | 0.70 | [0.6965, 0.7020] | 0.0054 | [0.6965, 0.7020] | **no** |

**The published point is inside its own band in 5 of 5 cases.** No bar is mis-set in the sense
that would have been a finding against PROTOCOL.

**The CAGR floor has no dominating value in its own units — this kills idea 145's premise as
stated.** Idea 131 found a dominance band for `gamma` because gross and CAGR order the corpus
differently; the band was a property of the *swap*, not of calibration. Sweeping phi itself, the
three criteria are strictly opposed (every step down admits victims *and* ladder points: at
phi = 0.65, +4 victims and +8 ladder; at 0.60, +6 and +17; at 0.50, +22 and +33), so nothing
dominates 0.70 and the honest output is the 0.0054-wide indifference interval. "Publish the band,
not the point" survives; "the band will usually be a dominance band" does not.

**Where dominance does appear, it is worth one ladder point and nothing else.** OOS at 1.0522
and DD at 0.5978 each drop exactly one ladder point while losing zero admissions. A 0.15%
relative move in delta is not a calibration recommendation; it is one ladder row sitting on the
boundary, and is reported as such.

**H2 is dominated in both directions and is therefore undetermined, not mis-set.** Loosening to
sigma2 ≤ 0.9727 admits 1 extra Pareto-best row at no leakage cost; tightening to ≥ 1.0215 drops
a ladder point at no admission cost. Both are "strict improvements" under criteria that here
point opposite ways. This is a limitation of the inherited dominance test, stated against the
run's own framing: **it only orders a bar when its criteria are co-monotone**, which holds for
the CAGR floor (idea 131's case) and fails for the Sharpe bars, where the ladder control has
almost no purchase (0 sole ladder exclusions between them).

## Q3 — separability (the two-parameter map; all 108 points in `.pairmap.csv`)

phi's indifference band re-derived at every delta, and delta's at every phi:

| delta | phi band | width | | phi | delta band | width |
|---|---|---|---|---|---|---|
| 0.30 | [0.4028, 3.0189] | 2.616 | | 0.00–0.70 | [0.5979, 0.6012] | 0.0033 |
| 0.40 | [0.5687, 3.0189] | 2.450 | | 0.80 | [0.5979, 0.6012] | 0.0033 |
| 0.50 | [0.6845, 0.7084] | 0.0239 | | 0.90 | [0.5979, 0.6076] | 0.0097 |
| **0.60–1.10** | **[0.6965, 0.7020]** | **0.0054** | | 1.00–1.10 | (−2.475, 0.659]+ | unbounded |

**The bands are separable in a neighbourhood of the published point and nowhere else.** For every
delta ≥ 0.60 phi's band is *identical*, and for every phi ≤ 0.80 delta's band is *identical*.
Outside that region both bands blow up — because the joint screen has emptied (at delta ≤ 0.40,
or phi ≥ 1.00, almost nothing is admitted and a bar that binds on nothing has an infinite band).
A wide band is therefore **not** evidence of robustness; it can equally mean the bar is inert.
That is the same trap idea 128 hit measuring plateau width on dials, arriving from the other side.

## Rule 8 walk-forward (bands re-derived on 2009–2016 alone; OOS read once)

Stated before any number: **4b has five bars but only four are prospectively checkable.** The OOS
Sharpe bar cannot be screened on an IS window by construction, so its band is retrospective only.
The IS screen is idea 131's four-bar version (H1, H2, DD, CAGR on the IS window).

| bar | published | IS band | IS width | full-sample band | contains published | overlaps full |
|---|---|---|---|---|---|---|
| H1 | 1.00 | [0.9864, 1.0136] | 0.0272 | [0.9974, 1.0453] | yes | yes |
| H2 | 1.00 | (−inf, 1.0171] | unbounded | [0.9829, 1.0213] | yes | yes |
| DD | 0.60 | [0.5979, 0.6012] | 0.0033 | [0.5979, 0.6012] | yes | yes |
| CAGR | 0.70 | [0.6960, 0.7016] | 0.0056 | [0.6965, 0.7020] | yes | yes |

**4 of 4 IS bands contain the published point and overlap the full-sample band**, and for the two
bars that bind (DD, CAGR) the IS and full-sample bands are the same to three decimals. The band
is a stable object across the split, which is the one thing that has to be true before PROTOCOL
can publish it.

Selector = argmax IS Sharpe among arms clearing the IS screen. 14 coefficient sets x 18 cells:

| selector | cells picking | mean admitted | OOS CAGR | OOS Sharpe | OOS MaxDD | beat SPY | beat v1 | picks moved |
|---|---|---|---|---|---|---|---|---|
| PUB (published point) | 7 | 2.5 | 12.7% | 1.022 | −21.1% | 5/7 | 7/7 | — |
| **all 12 band-edge/midpoint sets** | 7 | 2.5 | **12.7%** | **1.022** | **−21.1%** | 5/7 | 7/7 | **0** |
| NOBARS (screen deleted) | 18 | 17.0 | 9.1% | 0.695 | −23.1% | 6/18 | 12/18 | 11 |

Reference OOS on those cells: **SPY 15.45% / 0.882 / −33.72%**; **RULES v1 4.77% / 0.480 /
−19.67%**; ungated control Sharpe 1.051.

Two readings, both against my own framing:

- **The band is OOS-irrelevant for selection.** Not one of the 12 in-band coefficient sets moves
  a single pick in any of the 18 cells. That is an argument *for* publishing the band: quoting
  0.60 and 0.70 as points implies a precision the out-of-sample record does not contain.
- **Paired on the 7 cells the published screen enters, NOBARS is identical (1.022 / 12.7% /
  −21.1%).** The screen's entire OOS value is again *declining to enter* 11 cells, not picking
  better inside the 7 — reproducing ideas 131 and 132 on a fifth pass. And the picks beat SPY
  only 5/7 and the **ungated control only 2/7**, so the 1.022 is not evidence the screen adds
  value; it is evidence it avoids the panels where nothing works.

## Both KEEP paths, all 306 rows

4a: **97 of 306** (unaffected by 4b's coefficients). 4b at the published point: **29**; both: **6**.
At **every** finite band edge of every bar, 4b passes stay at **29** and both-paths at **6**; the
only column that moves is ladder leakage (10 → 9 at three tighter edges). **No book is promoted
and none could be** — this run re-scores an existing corpus under alternative bar coefficients,
which is the thing being adjudicated. Nothing here is a KEEP candidate for capital.

## What this proposes (exact wording in `.memo.md`)

PROTOCOL rule 4b quotes each bar as a band with its measured width, plus the two facts a width
alone cannot carry: how many rows the bar excludes *alone*, and whether the band is bounded.
No coefficient changes. Sunday review decides.

## Caveats, stated not buried

- **The dominance test only orders a bar when its criteria are co-monotone.** It does for the
  CAGR floor and the DD cap; it does not for the three Sharpe bars, where the ladder control
  excludes nothing. The H2 "dominated in both directions" result is a diagnosis of the test,
  not of the bar.
- **"Redundant" is a statement about this corpus, not about the bar.** The OOS Sharpe bar
  excludes 0 of 306 rows *here*, on 17 arm families over 3 panels — all of which already face
  H1, H2, DD and CAGR on overlapping windows. It is not evidence that a walk-forward bar is
  unnecessary in general, and the run does not recommend deleting it.
- **Band width is not robustness.** Q3 shows a bar that binds on nothing has an infinite band.
  Width must always be read next to the sole-victim count.
- **n is small where it matters**: 11 Pareto-best CAGR-floor victims and 4 DD-cap ones, in four
  cells, all EWall, with overlapping return series. Every band is a census of *this* corpus.
- **Survivorship** (idea 54): all three panels are current-constituent lists. Absent delistings
  inflate CAGR most for ungated high-gross books, which flatters the CAGR floor.
- **Idea 128**: the IS window's SPY MaxDD (−22.1% u56/broad, −18.6% small) is shallower than the
  OOS window's (−33.7%), so every IS-derived drawdown band admits too much. This biases the Q4
  screen in one known direction and cannot explain a 0-of-18 difference in moved picks.
- **Idea 38** (u56/broad calendar-day index) and **idea 126** (t+1 only, no lag band) carry over.
- The Q2 band endpoints are exact given the corpus; adding one arm family could move any of them.

Script: `research/backtests/2026-09-05_weak-dominance-bands-as-the-calibration-output_C.py`
Console: `.console.txt` · Corpus: `.grid.csv` · Ladder: `.ladder.csv` ·
Bands (all grid points): `.bands.csv` · Summary: `.bandsummary.csv` ·
phi x delta map: `.pairmap.csv` · Separability: `.separability.csv` ·
IS bands: `.isbands.csv` · Walk-forward: `.walkforward.csv` · Memo: `.memo.md`
