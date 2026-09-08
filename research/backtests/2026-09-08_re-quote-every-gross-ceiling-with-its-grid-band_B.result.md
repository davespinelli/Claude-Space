# Idea 236 — re-quote-every-gross-ceiling-with-its-grid-band (lane B, 2026-09-08)

**VERDICT: KILL of the `+/-0.03` band as worded — but the CORRECTION it was reaching for
stands and is sharpened.** A published gross ceiling is not a point estimate with a symmetric
error bar. It is a **one-sided lower bound**, and the bound's width is **free, exact and
per-book**, so the queue's universal constant is neither necessary nor sufficient. No RULES
change, no KEEP candidate. `RULES.md`, `scan.py`, `bot.py`, `baseline.py` and `PROTOCOL.md`
untouched.

Script `research/backtests/2026-09-08_re-quote-every-gross-ceiling-with-its-grid-band_B.py`;
console `..._B.console.txt`; data `..._B.{census,band,flips,grid,keep,walkforward}.csv` and the
10,890-row ladder `..._B.fine.csv.gz`.

---

## Corpus and parameters

The record's gross ceilings are the 4b admissible-interval **upper shoulders** of idea 90/144's
306-book gross family. **72 of 306** books carry a non-empty interval at the record's published
bars (phi = 0.70, delta = 0.60) and therefore a published ceiling; **all 72 were read off idea
90's 25-point m-grid of step 0.05**. This run re-reads every one of them on idea 154's 0.01
ladder — **3.4x idea 154's 21 cells** — by rebuilding the 45 distinct (panel, book, arm) cells
behind them on the full 121-point ladder at both rungs (10,890 runs).

Exactly two tuned parameters, **15 grid points, all reported**: grid `step` in
{0.05 (published), 0.02, 0.01} and band half-width `b` in {0.01, 0.02, **0.03 (the queue's)**,
0.04, 0.05}. The bar coefficients are pinned at the record's published (phi, delta) so that the
displacement measured is the **grid's**, not a bar change.

## Gates — all four pass before any new number is read

| gate | result |
|---|---|
| G1 `H.run` (every instrument off) vs `engine.backtest`, u56 + broad | **0.000e+00** both |
| G2 cost-rung identity `r(25) == r(10) - TO*15/1e4` on `gate` arms | **3.469e-18** |
| G3a rebuilt 0.05 rows vs idea 90 `family.csv.gz`, 2,250 rows x 15 cols | **6.788e-04** (see below) |
| G3b rebuilt **readings** vs idea 90 `intervals.csv` | grid positions (m_lo, m_hi) **0.000e+00**, nonempty verdict **90/90**, quoted gross 3.601e-05 |
| G4 idea 154's published fine ceilings, 6 cells | max \|d\| **8.32e-10** (0.817668, 0.810173, 0.862655, 0.855162, 0.781129, 0.870830 all reproduced) |

**G3a's residual is diagnosed, not waved through.** `broad` reproduces the committed file to
**6.661e-16**; `u56` carries **6.788e-04** that is **zero in H1** and non-zero in H2 / OOS /
full sample. That is the signature of one late-sample daily return changing — an adjusted-close
revision to `data/prices.csv` after idea 90 ran (`data/prices_broad.csv` is a separate weekly
cache and was not refreshed). This sandbox's clone is **shallow**, so the pre-revision file
cannot be checked out and the residual cannot be removed. It is 1e-5-scale against a measurand
quantised at ~0.007-0.03 of realised gross. **G3b is the decisive gate and it is exact: every
published shoulder lands on the same grid point**, so the readings this run re-quotes are the
record's own.

## Q1 — the census

* 306 books in the family; **72 carry a published gross ceiling**; **72 of 72 read off a 0.05
  grid** (100%); admissible set contiguous **72 of 72**.
* The bar that sets the ceiling: **DD 62**, `grid` 9, `H2+DD` 1.
* **9 of 72 are RIGHT-CENSORED** at PROTOCOL rule 2's no-leverage cap (m = 1.30). **A censored
  ceiling has no band** — it is a rule, not a measurement, and attaching +/-0.03 to it would
  quote leverage the protocol forbids. **63 are bandable.**

## Q2 — the displacement is ONE-SIDED, and the queue's `+/-` is the wrong shape

The coarse grid is a **subset** of the fine one, so every coarse-admissible point stays
admissible and `m_hi` can only **rise**. Where m is a pure exposure rescale (idea 90's
`PURE_KINDS` = ctl/gate/stop) realised gross is monotone in m, so the quoted ceiling can only
rise too. Pre-registered prediction: `d_hi >= 0` on every MONO book.

| 0.05 -> 0.01 | n | d >= 0 | mean | mean \|d\| | max | min | moved |
|---|---|---|---|---|---|---|---|
| all | 72 | 71/72 | +0.0122 | 0.0124 | +0.0300 | -0.0060 | 51 |
| **MONO (ctl/gate/stop)** | 55 | **55/55** | +0.0127 | — | +0.0300 | **0.0000** | — |
| NON-MONO (dd/bud) | 17 | 16/17 | +0.0107 | — | +0.0297 | -0.0060 | — |

**Prediction holds exactly on MONO.** The single downward mover is
`u56|TOP20|10.0|ddctl-8/.5/high` (m_hi 1.20 -> 1.23, g_hi 0.6557 -> **0.6497**): on a
drawdown-control arm m moves the instrument as well as the exposure, so realised gross is
**non-monotone in m** and the finer grid finds a *higher* admissible m at a *lower* realised
gross. There, "a band around the ceiling" is not even the right object.

**Idea 154's headline reproduces and extends:** on 72 cells instead of 21, mean \|move\| =
**0.0124** (idea 154: 0.0113), max = **0.0300** (idea 154: 0.0300), median 0.0127.

## Q3 — `+/-0.03` is not a bound; the bound is free

The displacement is bounded above, per book, **with no extra backtest**:

    d_hi  <  DELTA_STEP(book)  =  gross(m_hi + 0.05) - gross(m_hi)

the realised-gross width of one coarse step at that book's own shoulder.

| group | n | mean | median | min | max | > 0.03 | bound holds |
|---|---|---|---|---|---|---|---|
| all bandable | 63 | 0.0353 | 0.0370 | -0.0096 | 0.0375 | **61** | 62/63 |
| MONO only | 50 | 0.0367 | 0.0370 | 0.0340 | 0.0375 | **50** | **50/50** |
| NON-MONO | 13 | 0.0301 | 0.0370 | -0.0096 | 0.0375 | 11 | 12/13 |

**On 61 of 63 bandable ceilings one coarse step is WIDER than +/-0.03.** The queue's constant
is not a bound; it is a guess that happens to cover this corpus. Coverage at (step 0.05,
b = 0.03) is 1.000 with mean waste 0.0160 — the band is more than twice the typical
displacement — and at b = 0.01 coverage collapses to **0.4127**.

## Flips — what actually changes

Targets g in {0.75 (the live book's gross), 0.85 (idea 84's contested target)}, step 0.05:

| target | published admits | admits at 0.01 | **real flips** | flagged by +/-0.03 | caught | false alarms |
|---|---|---|---|---|---|---|
| 0.75 | 20 | 23 | **3** | 8 | 3 | 5 |
| 0.85 | 7 | 8 | **1** | 2 | 1 | 1 |

**Every flip runs INADMISSIBLE -> ADMISSIBLE; none runs the other way** — the one-sided result
again, now in verdict space. The four:

* `u56|TOP20|10.0|g200-rw` 0.7226 -> **0.7514**
* `broad|EWall|10.0|ddctl-8/.5/recover` 0.7447 -> **0.7584**
* `broad|EWall|25.0|ddctl-8/.5/recover` 0.7409 -> **0.7533**
* `u56|EWall|25.0|band3-rw` 0.8252 -> **0.8552** (the g = 0.85 flip)

The +/-0.03 band has **recall 1.000 and precision 0.400** on this corpus: it flags 10 books
across the two targets and only 4 flip.

**A third flip class the queue does not name.** Two cells published with **no admissible gross
at all** acquire one at 0.01 resolution — a 4b verdict flip at the *book* level, not the
ceiling level: `u56|TOP20|25.0|abs12-dg` (m [0.88, 0.89], g [0.6074, 0.6143], 2 of 121 points)
and `u56|EWall|25.0|abs12-rw` (m 0.98, g 0.7353, **1** of 121 points). Both are knife-edges and
neither is a candidate. **Coverage limit, stated:** only the 45 cells behind a published
ceiling were refined, so 2 is a **lower bound** on this class; the other 234 empty books were
not re-run.

## Both KEEP paths — every grid point

| step | books | 4a vs RULES v2 (live) | 4a vs RULES v1 | 4b |
|---|---|---|---|---|
| 0.05 | 72 | **0** | 19 | 72 |
| 0.02 | 71 | **0** | 19 | 71 |
| 0.01 | 72 | **0** | 19 | 72 |

4b at a book's own ceiling is **true by construction** (the ceiling is the largest admissible
point), so the informative column is 4a — and it is **0/72 against the live book at every
resolution**. A grid refinement creates no KEEP candidate on either path; idea 136's 4a
pathology again.

## Rule 8 — walk-forward (ceiling re-derived on 2009-2016, 2017-2026 read once)

43 of 90 cells have an IS ceiling; **40 have one on both grids**. Mean OOS 2017-2026, each book
run at **its own IS ceiling**:

| arm | n | realised gross | OOS CAGR | OOS Sharpe | OOS MaxDD |
|---|---|---|---|---|---|
| IS ceiling, step 0.05 | 40 | 0.7933 | 14.59% | 1.0912 | -22.23% |
| IS ceiling, step 0.02 | 40 | 0.7989 | 14.68% | 1.0905 | -22.37% |
| IS ceiling, step 0.01 | 40 | 0.8030 | **14.76%** | **1.0905** | **-22.48%** |
| RULES v2 (live baseline) | 72 | — | 9.03% | **1.2292** | -12.12% |
| RULES v1 (previous) | 72 | — | 5.75% | 0.5699 | -16.09% |
| SPY | 72 | — | 15.45% | 0.8820 | -33.72% |

Paired on the 40: refining the grid licenses **+0.0097 of realised gross** (moved in 29/40, max
+0.0300) and buys **+0.17 pp of OOS CAGR** (better in 28/40) for **-0.0007 of OOS Sharpe**
(better in only **14/40**) and **+0.25 pp of deeper OOS drawdown** (deeper in 29/40). Both
grids beat SPY's OOS Sharpe **40/40** and both lose to the live book **36/40**. By panel and
rung the picture is flat: broad@10 0.9958 -> 0.9958, broad@25 1.1149 -> 1.1058, u56@10 1.1487
-> 1.1487, u56@25 1.1388 -> 1.1388.

**The extra exposure a finer ceiling licenses is risk-neutral at best**: it is paid for exactly
in drawdown, which is the bar that set 62 of the 72 ceilings in the first place.

## What should be published instead of the queue's band

A gross ceiling read off a grid of step `s` must be quoted as the **one-sided interval**

    [ g_hi ,  g_hi + DELTA_STEP )   where DELTA_STEP = gross(m_hi + s) - gross(m_hi)

with three flags: **(i)** whether the shoulder is **right-censored** by rule 2 (9 of 72 here —
those have no band at all), **(ii)** whether m is a **pure exposure rescale** on that arm (if
not, gross need not be monotone in m and the interval is not even one-sided — 1 of 72 here),
and **(iii)** the grid step it was read on. `DELTA_STEP` costs nothing: the ladder point above
the shoulder was already run.

## Caveats carried

Survivorship (idea 54, u56/broad are current-constituent lists); idea 128 (the IS window's SPY
MaxDD is shallower than the OOS window's, biasing both walk-forward arms the same way); idea
144 Q1 (`ebud`/`ddctl` arms are not pure rescales — reported separately, never pooled); idea 38
and idea 126 carry over; the G3a price-revision residual above; and the flip census covers the
72 books that HAVE a published ceiling, which is the question asked, not all 306.
