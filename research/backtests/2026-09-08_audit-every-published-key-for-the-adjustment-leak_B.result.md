# Idea 197 — audit-every-published-key-for-the-adjustment-leak (lane B, 2026-09-08)

**ANSWERED, and the queue's own instrument is the first casualty. The queue asked to "apply that
one-line test" — idea 193's `Spearman(key, future total return)` — to every published key. That
test CANNOT classify a key: it flags two keys that are provably clean (VOLSH −0.417, VOL +0.279 at
h = T, both larger in magnitude than the leaking PRICE's −0.333) and misses one that is provably
dirty (DVOLT, −0.096). KILL of the statistic; it is replaced with an exact arithmetic operator
that has no sampling error. Under that operator: 5 of 14 catalogued keys are contaminated, the
LIVE BOOK IS CLEAN to machine zero, and the census finds 7 of 361 scripts and 35 of 3,382
LEADERBOARD rows affected — of which 3 scripts and 14 rows were NEVER FLAGGED BEFORE, all of them
`px * vol` dollar-volume constructions, one of which prints the words "Point-in-time." No RULES
change, no new book, no KEEP-candidate: 4a is 0 of 219 at every rung and every 4b pass is either a
level key (disqualified) or a re-measurement of the known u56 composite book.**

Script `research/backtests/2026-09-08_audit-every-published-key-for-the-adjustment-leak_B.py`
— 219 arm-rows x 3 cost rungs + 108 rescale-draw backtests + 3 x 14 keys x 2 sigmas x 3 draws of
invariance testing + a 361-file census, 253 s, deterministic, no network.
Outputs: `.reproduction.csv`, `.readjust.csv`, `.channels.csv`, `.keys.csv`, `.live.csv`,
`.horizon.csv`, `.census.csv`, `.arms.csv`, `.spread.csv`, `.walkforward.csv`, `.console.txt`.

**Tuned parameters: exactly two** — tilt strength `m ∈ {0.20, 0.50, 1.00}` and direction
`{POS, NEG}`, both inherited verbatim from ideas 181/193. KEY, PANEL, COST RUNG, horizon `h`,
dispersion `sigma` and seed are reported axes, never selected on. All grid points are in `.arms.csv`.

---

## Reproduction — and the one that failed, which is the run's best finding

| check | result |
|---|---|
| R1 adjusted-price identity `px[T]/px[t] == TR(t→T)` | **9.10e-12** (u56), 3.18e-12 (broad), 4.26e-13 (small) |
| R2 `fast_backtest == engine.backtest` | **1.04e-17** |
| R3 cost identity `r_c == r_0 − turnover·c/1e4` | **1.04e-17** |
| R0 RULES v1 u56 @10 bps vs the published anchor | **6.45851% / 0.66471 / −13.82781%** vs published **6.45305% / 0.66418 / −13.82780%** — **DOES NOT REPRODUCE** |

R0's failure is not a bug. Chasing it produced section E.

## (E) The operator is not a model — it is what this project's cache does every week

`data/prices.csv` was refreshed between commit `0e586d7` (2026-09-07) and `f138ee9` (2026-09-08).
Comparing the two committed snapshots over the 4,699 shared bars x 56 names:

* **exactly one name — GOOGL — had its ENTIRE history multiplied by one constant, 0.999358**;
  every other column is byte-identical.
* **max deviation from a per-name constant: 2.13e-04**, and that is the CSV's own 4-dp storage
  (NVDA's worst bar is priced at 0.4705, where 1e-4 absolute *is* 2e-4 relative).
* the ratio is 1.000000 on the final bar and 0.999358 on all 4,698 before it — i.e. the ex-dividend
  bar is the step.

That is precisely the theorem this run is built on:

> An auto-adjusted close is `adj[s] = raw[s]·F(s)`, `F(s) = ∏` of every adjustment factor over
> `(s, T]`. A panel truncated at `t` is adjusted to `t`: `adj_t[s] = raw[s]·F(s)/F(t) = adj[s]/F(t)`.
> **Truncating the panel at t rescales each column by one positive per-name constant.**
> So a key is point-in-time honest **iff its cross-sectional ranks are invariant under
> `px → px·diag(c)`, `c > 0`.**

Running the same code on both snapshots (u56, 10 bps):

| book | CAGR old → new | Sharpe old → new | dSharpe |
|---|---|---|---|
| RULES v1 (scale-invariant) | 6.453% → 6.459% | **0.66418 → 0.66471** | +0.00053 |
| RULES v2 (scale-invariant) | 8.660% → 8.660% | 1.20562 → 1.20563 | +0.00001 |
| PRICE/NEG m=1.00 (LEVEL key) | 13.149% → 13.149% | 1.17291 → 1.17291 | 0.00000 |

**The published anchor reproduces EXACTLY on the old snapshot** (6.45305% / 0.66418 / −13.82780%)
and is unreachable on the new one. Read the table correctly: one 0.064% dividend on 1 of 56 names
is far too small to reorder any cross-section, so the level book does not move here either. What E
establishes is the **mechanism, observed**: a routine refresh rescaled a 4,698-bar history by a
constant. A level key does not read one refresh — it reads `F(t)`, the *product* of every such
factor from `t` to the last bar. Calibrating from the observed event (0.064%/quarter = 0.26%/yr):
that name's `F` reaches ~1.049 over the sample's 18.7 years; a 4%-yield name reaches ~2.08 (log
0.73). The cross-name dispersion of `log F` a level key reads is therefore roughly 0 to 0.73, which
`sigma ∈ {0.10, 0.25}` brackets conservatively.

## (1) THE ANSWER — the queue's proposed test does not work, and here is one that does

**T1, the operator (exact, sigma = 0.25, pooled over u56/broad/small, 3 draws each):**

| key | class | frac of cells whose rank MOVES | mean \|Δ rankpct\| |
|---|---|---|---|
| PXTERM | LEVEL | **0.8299** | 0.0551 |
| PRICE | LEVEL | **0.8157** | 0.0588 |
| FROZEN | LEVEL | **0.7847** | 0.0592 |
| DVOLT | LEVEL | **0.7357** | 0.0388 |
| DVOL | LEVEL | **0.7277** | 0.0315 |
| COMP, R3, DDTR, R6, MOM, REBASED, FWDRET, VOL, VOLSH | RATIO/FWD | **0.0000 – 0.00031** | 0.000000 |

Three orders of magnitude, no overlap, no sampling error. **P2 is reported a MISS and not
repaired**: it demanded `max|Δ| < 1e-12` for a ratio key, and float64 multiply-then-divide is not
bit-exact, so a handful of *numerically tied* names swap rank and move `rankpct` by one rank step
(0.0096 on broad = 1/104). The measure was restated as `frac_cells_moved`; the strict pre-registered
bar of 1e-4 leaves COMP/R3/DDTR/R6 at 1.1e-4 – 3.1e-4 and so "fails", which is a bar-calibration
artefact against a 0.73–0.83 effect. Any threshold in [1e-3, 0.5] gives the identical partition.

**T2, the queue's own statistic, back-filled with a horizon ladder** (mean cross-sectional Spearman
with forward return, pooled over panels):

| class | key | h=21 | h=63 | h=126 | h=252 | **h=T** |
|---|---|---|---|---|---|---|
| LEVEL | DVOL | −0.0364 | −0.0845 | −0.1275 | −0.1721 | **−0.5959** |
| LEVEL | PRICE | −0.0425 | −0.0716 | −0.0970 | −0.1357 | **−0.3327** |
| LEVEL | FROZEN | −0.0685 | −0.0978 | −0.1337 | −0.1744 | **−0.3239** |
| LEVEL | **DVOLT** | +0.0263 | +0.0071 | −0.0009 | +0.0011 | **−0.0963** |
| RATIO | **VOLSH** | −0.0108 | −0.0408 | −0.0642 | −0.0803 | **−0.4166** |
| RATIO | **VOL** | +0.0394 | +0.0580 | +0.0786 | +0.1037 | **+0.2786** |
| RATIO | MOM / R3 / R6 / COMP / REBASED / DDTR | ~0 | ~0 | +0.04..+0.06 | +0.04..+0.09 | +0.04..+0.12 |
| FWD | FWDRET | +0.1617 | +0.2324 | +0.3086 | +0.4060 | +1.0000 |

**This is the KILL.** `VOLSH` (share volume, no price term at all) and `VOL` (realised volatility)
are *exactly* invariant under T1 — `frac_moved` 0.0000 and 0.000001 — yet reach |rho| 0.417 and
0.279 at h = T, larger than the leaking PRICE key's 0.333. Low-volatility and low-volume names
genuinely outperform over the sample; the statistic cannot tell that from a leak. In the other
direction DVOLT is contaminated (73.6% of cells move) with |rho_T| of only 0.096. **False positives
and false negatives, both, in the same table.** P5 was written before the first run and its second
clause ("ratio keys are roughly flat and small at every h") is falsified; that failure is the point.

**FWDRET fixes T1's scope, and is why it is carried.** `term/px − 1` is a *ratio*, so T1 says
invariant — and it is pure look-ahead. T1 certifies a key against **the adjustment leak**, not
against look-ahead in general. Both tests are needed; neither is sufficient alone.

## (2) THE RESULT THAT MATTERS FOR CAPITAL — the live book is clean

| object | u56 | broad | small | cells moved |
|---|---|---|---|---|
| **RULES v1 weight matrix** | **0.00e+00** | **0.00e+00** | **0.00e+00** | **0 / 0 / 0** |
| **RULES v2 weight matrix** | **0.00e+00** | **0.00e+00** | **0.00e+00** | **0 / 0 / 0** |
| v2 `band_state` | 0.00e+00 | 0.00e+00 | 0.00e+00 | 0 / 0 / 0 |
| v1 `vol20` | 1.4e-14 | 3.6e-14 | 3.3e-08 | 0 / 0 / 7.8e-05 |
| v1 `above 200d MA` | 0.00e+00 | 1.0e+00 | 1.0e+00 | 0 / 3.1e-06 / 1.1e-06 |
| v1 composite score | 2.0e-13 | 0.387 | 0.387 | 0 / 1.8e-04 / 7.8e-04 |

**P3 HIT.** The objects that hold capital are bit-identical under the operator. The two
intermediates that move do so on a *single* MA-crossing bar where `px > rolling mean` is a
floating-point tie (3 cells in a million), and it does not reach the weights. **RULES v1 and RULES
v2 carry no adjustment leak.**

## (3) THE CENSUS — which published claims are affected

Gated on the **construction**, never the column name (idea 334), with **every string literal blanked
first**. That step is not cosmetic: without it the record appears to contain 34 absolute price
thresholds in 27 files, and **all 34 are the prose `px > 200d MA` inside docstrings**. The true
count of absolute price thresholds in code is **0**, as is `np.log(px)`.

* **361 scripts scanned. 7 (1.9%) carry a LEVEL construction.** 184 carry a RATIO construction.
* **35 of 3,382 LEADERBOARD rows (1.0%)** sit on one of those 7 scripts.

| script | construction | LB rows | status |
|---|---|---|---|
| `2026-09-05_does-a-null-column-change-any-published-verdict_cloud.py` (181) | `rankpct(px)` | 5 | already killed (193) |
| `2026-09-05_does-a-harmful-instrument-clear-more-often-than-a-helpful-one_B.py` (192) | `rankpct(px)` | 4 | already killed (193) |
| `2026-09-05_is-PRICE-NEG-...-large-and-helpful_B.py` (193) | `rankpct(px)`, `rankpct(entry)`, `rankpct(term)`, `px*vol` | 8 | the killing file itself |
| `2026-09-06_is-the-low-price-tilt-...-survivorship-one_cloud.py` (199) | same four | 4 | already killed |
| **`2026-09-06_band-gate-on-small-panel_B.py`** | `dv = (px*vol).rolling(20).median()`, then **`dv >= floor`** as an eligibility screen | **9** | **NEWLY FLAGGED** |
| **`2026-09-06_trend-filter-by-market-cap_cloud.py`** | `advrank = (px*vol).rolling(ADV_WIN).median().rank(axis=1, pct=True)` | **5** | **NEWLY FLAGGED** |
| **`2026-09-06_trend-filter-by-market-cap_B.py`** | `rk = (px*vol).rolling(60).median().rank(axis=1, pct=True)` | **0** | **NEWLY FLAGGED** |

**The three new files are all the same construction — dollar volume, `price × shares` — used as a
size or liquidity proxy.** `trend-filter-by-market-cap_cloud.py:391` prints the claim
`"... coverage ... of panel cells.  Point-in-time."` beside the very rank that is not.
`band-gate-on-small-panel_B.py` is worse in kind, not in size: the contaminated quantity there is an
**absolute floor on an eligibility mask**, so the leak enters the *panel*, not merely a tilt.

This also answers queue idea 313 ("why do capQ and advQ disagree in SIGN") without running it:
**advQ has a price LEVEL inside it and capQ does not.** Idea 313 should be re-scoped accordingly.

## (4) HOW BIG IS THE ARBITRARINESS — section A

Full-sample Sharpe @10 bps, `m = 1.00`, re-running each arm with the KEY computed on `px·diag(c)`
for 6 draws at sigma = 0.25 (returns untouched — only the key moves):

| panel | key | dir | published Sharpe | min | max | **range** |
|---|---|---|---|---|---|---|
| small | PXTERM | POS | 0.7503 | 0.6314 | 0.9176 | **0.2862** |
| small | PRICE | NEG | 1.0672 | 0.9394 | 1.1348 | **0.1955** |
| small | FROZEN | POS | 0.1517 | −0.0150 | 0.1746 | **0.1896** |
| u56 | PRICE | NEG | 1.1729 | 1.1491 | 1.2419 | **0.0927** |
| … 22 level rows total … | | | | | | 0.042 – 0.286 |
| **every RATIO row (20 of 20)** | | | | | | **exactly 0.0000** |

**P6 HIT.** A level-key headline is one draw from a distribution 0.04–0.29 of Sharpe wide, and
which draw you get is decided by the date the cache was last refreshed.

## (5) BOTH KEEP PATHS, rule 8, and what is promoted (nothing)

Comparands @10 bps — SPY **15.23% / 0.8890 / −33.72%** (OOS 15.45% / 0.8820 / −33.72%);
RULES v2 u56 **8.66% / 1.2056 / −12.05%**, halves 1.2259 / 1.1909 (OOS 9.53% / 1.2851 / −12.05%).

| rung | 4a passes | 4b passes | BOTH |
|---|---|---|---|
| 0 bps | **0 / 219** | 81 / 219 | **0** |
| 10 bps | **0 / 219** | 56 / 219 | **0** |
| 25 bps | **0 / 219** | 16 / 219 | **0** |

By class @10 bps: LEVEL 0 / 9 (4a / 4b of 48), RATIO 0 / 37 (of 132), oracle 0 / 9 (of 36),
control 0 / 1 (of 3). **All 9 level-key and 9 oracle 4b passes live on u56, and every one is
disqualified by T1 regardless of its numbers.** The largest is the one that matters as a warning:

* **u56 PRICE/NEG m=1.00 @10 bps — 13.15% / 1.1729 / −17.65%, halves 1.1494 / 1.1957,
  OOS 14.03% / 1.2540 / −17.65%. It clears 4b outright.** It beats SPY on Sharpe in both halves and
  OOS, on 86% of SPY's CAGR and 52% of its drawdown. **It is not implementable at any cost, on any
  panel, at any gross**, and its own admissible-rescaling range is 0.093 of Sharpe.

The best *implementable* arm is u56 REBASED/POS m=1.00 (13.29% / 1.1288 / −18.44%, OOS 15.58% /
1.1945 / −18.44%) against an untilted control of 12.66% / 1.0921 / −18.31% (OOS 14.36% / 1.1680) —
a +0.037 Sharpe tilt on a book the record already has. **4a is 0 of 219 at every rung: nothing here
beats RULES v2 in both halves without a worse drawdown.**

**Rule 8** (`(m, dir)` chosen by IS Sharpe on ≤ 2016-12-31 within each (panel, key, rung) cell, 2017–2026
read once, `.walkforward.csv`): the IS chooser's OOS gain over the untilted control is monotone in
how contaminated the key is — on the small panel **DVOL +1.079, PRICE +0.703, VOLSH +0.589,
FWDRET +1.667** against **MOM +0.220, R3 +0.224, R6 +0.080, DDTR −0.021**. The selector is buying
the leak, out of sample, exactly as it buys it in sample — because the contamination is present in
both windows. **A walk-forward split does not detect this failure and never could**; only T1 does.

## Predictions

| | prediction | result |
|---|---|---|
| P1 | R1 identity < 1e-9 | **HIT** |
| P2 | ratio invariant, level not | **MISS** (float64 tie-breaking; ratio 7.6e-04 vs level 0.728 — partition unaffected) |
| P3 | LIVE book exactly invariant | **HIT** (0.00e+00, 0 cells) |
| P4 | FROZEN — idea 193's own substitute for PRICE — is itself NOT invariant | **HIT** (78.5% of cells move) |
| P5 | level \|rho\| peaks at h = T; ratio flat | **HIT / MISS** — level 0.057 → 0.381 and ratio 0.161 at h = T, so the aggregate holds, but VOL and VOLSH falsify the clause and that is the run's KILL |
| P6 | rescale spread 0 for ratio, > 0.10 for a level arm | **HIT** (0.0000 vs 0.2862) |
| P7 | no level-key arm promoted | **18 arms pass 4b @10 bps; all disqualified** |

## Recommendation (no RULES change; PROTOCOL not modified by this run)

1. **PROTOCOL should require the T1 line beside any new key.** One assertion, no sampling error:
   `assert key(px).equals(key(px * diag(c)))` up to rank ties. It is cheaper than the Spearman it
   replaces and it is decisive where the Spearman is not.
2. **Re-scope idea 313**: advQ's sign disagreement with capQ is the price level inside advQ.
3. **`band-gate-on-small-panel_B`'s 9 rows carry the leak in the ELIGIBILITY MASK**, not a tilt —
   re-run its liquidity floor on `VOLSH` (share volume, T1-clean) before any of it is cited again.
4. `trend-filter-by-market-cap_cloud.py`'s "Point-in-time" line should be struck or corrected.

## Caveats

* **SURVIVORSHIP.** All three panels are current constituents (idea 54, PROTOCOL rule 9); the small
  panel additionally drops the 44 tickers with `max_1d_move >= 1.0` (idea 186's screen).
* The operator models the dividend+split channel that runs **through price**. Share volume in these
  caches is split-adjusted too, so `VOLSH` is invariant under *this* operator while still carrying a
  weaker future-split channel of its own. Stated, not measured: no split calendar is cached.
* `sigma` is a reported sensitivity axis, calibrated in section E from the one real re-adjustment
  the repository contains — not fitted. T1's verdict does not depend on it; only section A's size does.
* Section E rests on **one** observed refresh (56 names, 3 days). It establishes the mechanism
  exactly and bounds one event; it does not estimate a distribution of events.
* MCAP remains **PARKED** (idea 195): needs local/Actions data.
