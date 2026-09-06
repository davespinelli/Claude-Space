# Idea 188 — can a PANEL PROPERTY choose the cadence? (cloud, 2026-09-06)

> **Collision notice, stated first.** A sibling cloud lane answered idea 188 on 2026-09-05 and
> committed it as `2026-09-05_why-the-small-panel-wants-M-and-the-large-caps-6W_cloud.*` while
> this run was in flight; the queue read as open when this lane claimed it (the claim was pushed
> at 00:00 UTC on 09-06, after their run had started and before their push landed). This file is
> **not** a replacement. It measures the same two properties independently — and agrees with
> them on both — then takes the step the queue's final clause asks for and the sibling did not:
> it turns each property into an actual **selector** and prices it under rule 8 against the
> constants. Section (5) reconciles the two line by line, including one methodological
> correction that changes how the sibling's central table should be read.

**ANSWERED, and it is a KILL of the clause idea 77 asked for. Both proposed mechanisms fail:
signal decay fails because on the large-cap panels the composite's information does not decay at
all — it RISES monotonically with horizon — and on the small panel there is no cross-sectional
information to decay. Holding-episode length orders the three families correctly but recovers
under half the family label's explanatory power, and every property-chosen cadence loses
out-of-sample to simply writing a constant down. No book proposed; RULES.md, PROTOCOL.md,
scan.py, bot.py and baseline.py untouched.**

A family label is not a clause: "small caps want M" cannot go into RULES because a future panel
carries no label. A clause needs a measurable panel property, computable in-sample, that
(a) explains the split and (b) chooses the cadence at least as well as a constant. Neither
candidate does either.

## Corpus and reproduction

Idea 175's corpus, book construction, cadence mask, backtest and KEEP evaluators imported
verbatim: **115 books** (SMALL439, U56, ETF36 plus 112 sub-panels drawn with idea 175's own
seeds) × the 7-point ladder D/2D/W/2W/M/6W/Q, 10 bps, t+1. 92 s.

| check | result |
|---|---|
| [a] `cad_mask` vs `engine.rebalance_mask` at D/W/M/Q | identical at all four — PASS |
| [b] `fast_backtest` vs `engine.backtest` | max\|dret\| 1.7e-18–8.3e-17 — PASS |
| [c] CAND-20 weights vs idea 78/171 `weights_cand` | **0.000e+00** — PASS |
| [d] idea 175's published `ladder.csv`, **805 of 805 rows** | Sharpe/IS/OOS 2.2e-16, CAGR 9.9e-17, MaxDD 9.7e-17, turnover 7.1e-15 — PASS |
| [e] idea 175's `constants.csv`, 28 cells re-derived | max\|d mean_d\| **8.3e-17** — PASS |

The split to be explained reproduces exactly (mean OOS Sharpe minus the W incumbent):

| family | M | 6W | Q |
|---|---|---|---|
| SMALL | **+0.0978** | +0.0163 | +0.0313 |
| U56 | +0.0469 | **+0.1640** | −0.2472 |
| ETF | +0.0730 | **+0.1600** | −0.2914 |

## (1) Signal decay — the mechanism is not merely absent, it points the other way

Cross-sectional rank IC of the composite against forward return, eligible names only, sampled
every 21 trading days so overlapping windows cannot inflate the t (stride 63 gives the same
shape and is in `.ic.csv`):

| family | h=5 | h=10 | h=21 | h=30 | h=42 | h=63 | h=90 | h=126 |
|---|---|---|---|---|---|---|---|---|
| U56 IC | +0.0605 | +0.0657 | +0.0639 | +0.0763 | +0.0772 | +0.0984 | +0.1215 | **+0.1481** |
| U56 t | 2.57 | 2.72 | 2.76 | 3.30 | 3.49 | 4.41 | 5.61 | **6.59** |
| ETF IC | +0.0706 | +0.0680 | +0.0470 | +0.0570 | +0.0609 | +0.0862 | +0.1053 | **+0.1291** |
| SMALL IC | +0.0180 | +0.0079 | **+0.0045** | +0.0002 | −0.0114 | −0.0071 | −0.0076 | −0.0064 |
| SMALL t | 0.73 | 0.34 | 0.24 | −0.02 | −0.40 | −0.17 | −0.28 | −0.23 |

**On U56 and ETF the composite is a SLOW signal whose IC roughly doubles from 21 to 126 days —
it does not decay over any horizon on the grid.** On SMALL the IC is statistically
indistinguishable from zero at every horizon and turns mildly negative past 30 days (|t| ≤ 0.8
throughout). So the queue's implied story — "small caps want a faster cadence because their
signal decays faster" — is false in both halves: the large caps' signal does not decay, and the
small panel's does not exist to decay. The IR-optimal horizon `argmax IC(h)/sqrt(h)` lands at
h = 5d for all three families' fixed panels, i.e. the statistic that should select the cadence
selects the ladder's fastest point everywhere and therefore cannot produce the observed split.

## (2) Holding-episode length — right ordering, wrong size

Idea 76's measure, made cadence-free: mean length in trading days of a maximal run of
consecutive days on which a name sits in the daily top-20 among eligible names.

| family | mean episode (days) | fixed panel |
|---|---|---|
| SMALL | **18.8** | SMALL439 **9.0** |
| U56 | 31.3 | U56 17.2 |
| ETF | 38.8 | ETF36 22.9 |

The ordering is the one the mechanism wants — the panel whose selection turns over fastest is
the one that prefers the faster of the two cadences — and it is on idea 76's own scale (16d for
v1, 39d for top20). But it is not enough to be a clause:

| OLS of gap = OOS Sharpe(M) − OOS Sharpe(6W), 115 books | k | R² |
|---|---|---|
| family dummies only | 2 | **0.4453** |
| log episode_days | 1 | 0.1726 |
| log h* (IR, stride 21) | 1 | 0.0559 |
| log turnover at W | 1 | 0.0153 |
| log h* + log episode | 2 | **0.2036** |
| log h* + log episode + family dummies | 4 | **0.4518** |

The two properties together recover **46% of the label's R²**, and adding the family dummy on
top of them still lifts R² from 0.204 to 0.452 — **the label carries information the properties
do not**. Spearman(gap, episode_days) = −0.386 pooled but +0.072 / +0.141 / −0.008 within ETF /
SMALL / U56: the correlation is entirely between-family, which is the signature of a re-labelling
rather than a mechanism. Turnover confirms idea 175's own aside — it explains 1.5%.

## (3) Rule 8 — the constant beats every property, 115 books, OOS 2017–2026

Every property recomputed on IS ≤ 2016-12-31 only; the cadence it implies is mapped to the
nearest ladder point in log spacing; 2017–2026 read once.

| arm | mean OOS Sharpe | OOS CAGR | OOS MaxDD | Δ vs W (t) | Δ vs M (t) | beats M |
|---|---|---|---|---|---|---|
| ORACLE (OOS argmax) | 0.8427 | 7.14% | −18.24% | +0.1629 (17.6) | +0.0868 (14.8) | 87.8% |
| **A2 constant 6W** | **0.7797** | 6.49% | −20.26% | +0.0999 (8.5) | +0.0238 (1.9) | 73.0% |
| **A1 constant M** | 0.7559 | 6.02% | −17.32% | +0.0761 (6.7) | — | — |
| A5 EPISODE (IS) | 0.7384 | 6.12% | −19.22% | +0.0586 (3.6) | −0.0175 (−1.3) | 38.3% |
| A3 SEL-SHARPE (IS argmax) | 0.7186 | 5.75% | −17.98% | +0.0388 (3.3) | −0.0373 (−3.8) | 5.2% |
| A4 DECAY IR/s21 | 0.6966 | 5.53% | −18.25% | +0.0168 (2.3) | −0.0593 (−5.5) | 20.0% |
| A0 constant W (incumbent) | 0.6798 | 5.26% | −17.05% | — | −0.0761 (−6.7) | 18.3% |
| A4 DECAY IC/s21 | 0.6325 | 5.40% | −20.59% | −0.0473 (−3.2) | −0.1234 (−8.3) | 18.3% |
| A4 DECAY HALF/s63 | 0.5688 | 5.12% | −22.87% | −0.1109 (−7.2) | −0.1870 (−11.6) | 14.8% |

References over the same window: **SPY Sharpe 0.8820**; RULES v1 @10 bps 7.73% / 0.7471 /
−13.83% (U56) and 6.35% / 0.4923 / −36.12% (SMALL).

**All six DECAY settings and the EPISODE rule lose to the constant M, and all seven lose to the
constant 6W.** The best property arm (EPISODE) is −0.0175 against M at t −1.32 and wins in 38%
of books; the worst is −0.187. This is idea 175's own "the constant beats the fit that mostly
picks it" extended from a fitted selector to a fitted panel property, and the third such reading
after ideas 175 and 189. The DECAY arms fail for a legible reason: the IC curve's shape sends
them to the ladder's ends (HALF picks Q in 53–58% of books, IR picks W in 52–56%), and the
observed optimum is interior.

## (4) The finding that survives, and the honest form of the answer to idea 77

By family, at the two constants:

| family | constant M | constant 6W |
|---|---|---|
| SMALL | **0.3030** / 2.58% / −24.67% | 0.2215 / 1.91% / −29.36% |
| U56 | 1.2699 / 12.10% / −14.13% | **1.3870** / 13.99% / −16.16% |
| ETF | 0.9143 / 5.06% / −9.59% | **1.0013** / 5.78% / −10.84% |

Idea 175's split is real, reproduces to 1e-16, and **no measurable panel property tested here
recovers it**. So the clause idea 77 wants cannot be written on this evidence, and a single
global constant must trade the families off: 6W is the better pooled choice (+0.0238 over M,
73% of books) but is the worse choice on the family where M was significant. **The defensible
output is idea 175's, unchanged — write M down as the pre-registered constant and state the
large-cap preference for 6W as an unexplained observation, not as a rule.**

## KEEP paths (PROTOCOL 4)

Carried unchanged from idea 175's own 4a/4b columns across all 805 points: **4a 195/805,
4b 59/805**. Every one of the 59 4b passes is on **U56** (D 5, 2D 12, W 10, 2W 4, **M 18**,
6W 10, Q 0); ETF 0/231 and SMALL 0/343 — idea 136's small-panel wall again. Q passes 4b nowhere
and 4a nowhere. This idea proposes no book and claims neither path.

## (5) Reconciliation with the sibling 2026-09-05 run

**Agreements, reached independently:**

| quantity | this run | sibling run |
|---|---|---|
| SMALL439 rank IC at h=21 | **+0.0064** | **+0.0070** |
| shape of the SMALL curve | crosses zero at h≈30, negative beyond | "peaks at h=10, dead by h=30" |
| shape of the U56/ETF curves | rising to h=126 (+0.1505 / +0.1115) | "still RISING at h=84 (1.081 / 1.061)" |
| episode-length ordering | SMALL 9.0d < U56 17.2d < ETF 22.9d | SMALL 1.90 < U56 4.18 < ETF 5.71 rebalances at M |
| rule 8 headline | the constant beats every fitted rule | "the pre-registered constant beats both fitted selectors on all three families at every rung" |
| 4b passes | 59/805, **all on U56**, ETF 0, SMALL 0 | "every fixed-panel pass being U56, SMALL439/ETF36 0/7 at all rungs" |

The two episode measures use different units (cadence-free trading days here, rebalances at M
there) and land on the same ratio: 9.0/17.2 = 0.52 against 1.90/4.18 = 0.45.

**One methodological correction, and it changes the reading of the sibling's decay table.** Its
IC t-statistics are computed on **fully overlapping** h-day windows sampled every bar
(`n_bars` 3891 at h=21 on a 3907-bar sample), which inflates t by approximately √h. Its
SMALL439 row reads t = 5.22 / 5.76 / 3.58 at h = 5 / 10 / 21 — apparently a significant signal
that then dies. Sampling every 21 bars so the windows do not overlap, the same IC point estimate
(+0.0064 vs its +0.0070) carries **t = 0.75**, and 3.58/√21 = 0.78 — the overlap factor accounts
for essentially the whole difference. **On overlap-corrected standard errors the small panel's
composite is not distinguishable from zero at any horizon on the grid (|t| ≤ 1.55 throughout),
so "peaks at h=10 and is dead by h=30" over-reads it: it was never alive.** The large-cap
panels' significance survives the same correction (U56 t = 2.76 at h=21 rising to 6.59 at
h=126), so the *contrast* both runs report is real; only the small panel's peak is an artefact
of overlapping windows.

**What this run adds.** The sibling establishes that the split is a signal-horizon phenomenon
rather than a cost one. It does not test whether either property can be *written down as a
rule*, which is what idea 77 asked for and what determines whether a PROTOCOL clause exists.
Section (3) does: seven property-based selectors, each computed on the IS window alone, and all
seven lose out-of-sample to the constant M and to the constant 6W. That is the finding that
makes the answer a KILL rather than a mechanism paper.

## Pre-registered predictions: 2 of 5 hit

- **MISS** P1 — SMALL's IR-optimal horizon is not the shortest (12.9d vs ETF 5.3d, U56 5.2d); the
  statistic degenerates to the ladder's fast end on the large-cap panels.
- **HIT** P2 — SMALL's episodes are shorter than U56's (18.8d vs 31.3d, ETF 38.8d).
- **MISS** P3 — the properties recover 0.204 of the family dummies' 0.445 R², not ≥50%.
- **HIT** P4 — no property-chosen cadence beats the constant M (best −0.0175).
- **MISS** P5 — IC does not decay: it rises with horizon on U56 and ETF. This is the run's
  central result and the prediction was wrong in the most useful direction.

## Caveats

**Survivorship is doing visible work in section (1) and must be read as such.** All three panels
are current constituents; on such a panel the long-horizon cross-sectional IC of a momentum
composite is biased upward precisely because the surviving names' multi-year returns are positive
and correlated with their past momentum. The monotone rise of IC to h = 126d on U56/ETF is
therefore the shape survivorship manufactures, and the levels (+0.13 to +0.15) are not tradable
estimates. SMALL439's near-zero IC carries the same bias and is still zero, which is the more
robust half of the reading. SMALL439 is the 483-name sub-$2B panel less the 44
`max_1d_move ≥ 1.0` tickers per `data/small_meta.csv`; its bias is one-directional and falls
hardest on beaten-down names.

Implementation note: the holding-episode measure must be run-length-encoded **per name**. A
2-D difference plus a flat `nonzero` splices runs across name boundaries and inflates the mean
by two orders of magnitude (3974d instead of 9.0d on SMALL439); this run's first pass had that
defect and the committed version flattens column-major with a False pad on each column. Anyone
implementing idea 76's measure elsewhere should check the same thing.
