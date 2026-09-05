# Idea 159 — the-share-at-which-ranking-stops-paying (lane B, 2026-09-05)

**ANSWERED, and the answer is a KILL of the question: there is no share at which ranking stops
paying, because the VALUE of a tilt and the COST of running it are the same function of book
share.** The ratio g/c is flat in m, so it never falls through 1, so the threshold PROTOCOL
wanted does not exist at any share on any panel. No RULES change, no new KEEP-candidate.

Script `2026-09-05_the-share-at-which-ranking-stops-paying_B.py`; console, grid, curve,
crossing, ratio, dslope, bootstrap and walk-forward CSVs alongside.

## Reproduction, asserted before any new number was read — 8 of 8 MATCH

| check | published | this run | |
|---|---|---|---|
| [a] u56 n=20 INV-vs-NONE name overlap (ideas 81/153) | 69.4% | **69.4%** | MATCH |
| [a] broad n=20 INV-vs-NONE name overlap | 42.5% | **42.5%** | MATCH |
| [b] u56 dCAGR(POS−NONE) at m=0.20 @10bps (idea 153) | +2.83%/yr | **+2.83%/yr** | MATCH |
| [b] broad dCAGR(POS−NONE) at m=0.20 @10bps | +2.75%/yr | **+2.75%/yr** | MATCH |
| [c] mean weekly eligible counts u56 / broad / small | 37.5 / 91.5 / 141.2 | **37.5 / 91.5 / 141.2** | MATCH |
| [d] cost-derivation identity `r_c = r_0 − turnover·c/1e4` vs a fresh 10 bps engine run | — | max abs diff **0.00e+00** | MATCH |

[d] matters: every gross/net split below is the *same book*, not two runs, so g and c are
measured on one path.

## The corpus

2 tuned parameters, all grid points reported: book share m ∈ {0.05, 0.10, 0.15, 0.20, 0.30,
0.40, 0.53, 0.70, 0.85, 1.00} (n = max(2, round(m·Ē)), idea 153's map, so m = 0.53 lands on
u56 n = 20, the incumbent) × tilt ∈ {INV = /√vol20 (the live tilt), NONE (control), POS = ×√vol20}.
3 panels × 10 shares × 3 tilts × 2 constructions = **180 books**, each run once at 0 bps with the
10/25 bps rungs derived exactly. Weekly, t+1, no shorting, no leverage.

## The measurement, fixed before any number was read

* **g(m)** = |CAGR(tilt @ 0 bps) − CAGR(NONE @ 0 bps)| — the tilt's *gross* realised magnitude.
* **c(m)**, three bars, all reported: **INC** = the exact incremental cost of choosing the tilted
  book over its control (primary; may be ≤ 0); **OVL** = 10 bps × annualised Σ|w_tilt − w_NONE|
  over rebalances (the cost of *expressing* the tilt, an upper bound); **FLAT** = 0.10 pp/yr.
* **m\*** = smallest share with g ≤ c thereafter, by linear interpolation of the grid
  (empirical) and by crossing the log-linear fits of g and c (fitted).

## The result: the crossing is not locatable

**10 of 36 (panel, construction, tilt, bar) cells produce a finite empirical m\* at all, and 6 of
those 10 sit at the grid's lower endpoint m = 0.05** (i.e. "already noise at the smallest share
tested", not a threshold). The fitted estimator returns −16.72, +86.90, +15.82 and similar — the
signature of two near-parallel lines whose intersection is numerically meaningless.

The bootstrap says why. Circular block bootstrap, block = 21 d, 2000 replicates, seed 159, tilt
and control resampled with the same block index:

| panel | tilt | m\* point (BAR-OVL) | boot median | 5–95 | censored |
|---|---|---|---|---|---|
| u56 | INV | none | 0.050 | [0.050, 0.934] | **83.2%** |
| u56 | POS | 0.050 | 0.050 | [0.050, 0.756] | 27.5% |
| broad | INV | none | 0.050 | [0.050, 0.991] | **68.8%** |
| broad | POS | none | 0.285 | [0.050, 0.977] | **56.0%** |
| small | INV | 0.050 | 0.050 | [0.050, 0.916] | 4.6% |
| small | POS | 0.669 | 0.642 | [0.050, 0.926] | 11.5% |

Every interval that is not censored spans essentially the whole share axis. **P4 held for the
wrong reason**: the interval is wide because the parameter does not exist, not because it is
imprecisely estimated.

## Why — the ratio diagnostic (POST-HOC, added after P3 failed, labelled as such)

A crossing exists only if g decays *faster* in m than c does, i.e. only if
d = slope(log g) − slope(log c) < 0. Bootstrapped, BAR-OVL, literal book:

| panel | tilt | d | boot 5–95 | P(d < 0) |
|---|---|---|---|---|
| u56 | INV | **+0.032** | [−1.186, +1.097] | 47.4% |
| u56 | POS | +0.478 | [−2.128, +1.390] | 60.1% |
| broad | INV | +0.173 | [−0.781, +1.274] | 38.5% |
| broad | POS | −0.590 | [−2.116, +0.688] | 80.0% |
| small | INV | +1.876 | [−1.385, +2.296] | 29.8% |
| small | POS | +0.662 | [−2.145, +1.874] | 50.8% |

**6 of 6 intervals straddle zero.** The two curves are parallel in logs to within noise. The
mechanism is arithmetic and should have been obvious: both the value and the cost of a tilt are
proportional to how many names it moves, and how many names it moves is exactly what book share
governs (idea 153). Share scales the numerator and the denominator equally.

The ratio itself, u56 literal, BAR-OVL: **1.95 at m = 0.05, 1.83 at m = 0.53, 2.20 at m = 1.00**
(Spearman(m, ratio) = **−0.224**); broad: 1.50 / 1.47 / 1.58 (Spearman **+0.358**). On the
primary bar (BAR-INC, the tilt's *true* incremental cost) the ratio is **16–4254 on u56 and
9–193 on broad** — the tilt's gross magnitude exceeds what it actually costs by one to three
orders of magnitude at **every** share, endpoint included.

## What the number should have been, and what replaces it

At the incumbent's own share m = 0.53 on u56, the live INV tilt has g = **2.68 pp/yr** of gross
magnitude available, against c_INC = **0.083 pp/yr** and c_OVL = **1.46 pp/yr**. It is affordable
by a factor of 32 on the honest bar. Its **signed** dCAGR is **−2.68 pp/yr**, and INV's signed
dCAGR is negative at **all 10 shares on u56 (−13.49 to −0.61 pp/yr) and all 10 on broad (−9.57 to
−0.36)**. **The live tilt is never too expensive; it is wrong-signed everywhere.** That is a
fifth independent derivation of "delete the vol scaler" (after ideas 72, 82, 141, 160, 162), and
the first one that separates the two possible reasons — cost and direction — and finds the cost
reason absent.

## Both KEEP paths, all 180 books

| cost | construction | 4a | 4b | 4b on the OOS window |
|---|---|---|---|---|
| 10 bps | literal | 22/90 | **17/90** | 24/90 |
| 10 bps | gross-normalised | 22/90 | **24/90** | 25/90 |
| 25 bps | literal | 36/90 | **0/90** | 11/90 |
| 25 bps | gross-normalised | 29/90 | **0/90** | 11/90 |

**No new book.** The 4b passes are idea 153's already-published set re-measured on a finer share
grid: u56 and broad, m ∈ [0.30, 1.00], tilt NONE or POS, 10 bps only (u56 m=0.53/NONE/n=20 is the
incumbent: 12.66%/1.092/−18.31%, halves 1.088/1.102, OOS 1.168). Cross-universe 4b @10 bps = 19
(m, tilt, construction) arms, all inside idea 153's interval. **INV — the live tilt — passes 4b 2
of 60 times**, both at m ≥ 0.85 where all three tilts hold nearly the same names. **Everything
fails at 25 bps** (idea 137's wall, confirmed again). Nothing here is proposed to the Sunday
review.

## Rule 8 walk-forward (2009–2016 → 2017–2026; small panel 2011–2016), 12 cells

m\* re-estimated on the IS window only; the gate is the tighter of the two treatments' IS
crossings; picks read once on 2017-01-01→.

| selector | mean OOS Sharpe | mean OOS CAGR | mean OOS MaxDD |
|---|---|---|---|
| S_NONE (do nothing: NONE at m = 0.53) | **0.8044** | 9.67% | −23.21% |
| S_MSTAR (tilt free below m\*, forced NONE above) | 0.7212 | 13.08% | −28.53% |
| S_IS (plain IS Sharpe over the whole grid) | 0.7005 | 12.77% | −28.28% |
| S_LIVE (RULES v1) | 0.4514 | 4.86% | −25.30% |
| SPY | **0.882** | 15.45% | −33.72% |

S_MSTAR − S_IS = **+0.021**, wins 4 of 12. S_MSTAR − S_NONE = **−0.083**, wins **1 of 12**. The
gate beats the naive IS chooser by a hair and loses clearly to doing nothing, and **all four
selectors lose to SPY**. The IS gate is also unstable: it lands at 1.01 (no gate) in the 10 bps
cells and collapses to 0.05 (gate everything) at 25 bps, which is the non-existence of m\*
showing up in the selector rather than in the diagnostic.

## Predictions — 3 of 6 held

* **P1 HELD** — all 8 reproduction checks.
* **P2 FAILED** — g is monotone in m for INV (Spearman −0.988 u56, −1.000 broad) but not for POS
  (−0.515 u56); on small, neither (−0.273 / −0.418).
* **P3 FAILED, and this is the result** — no crossing strictly inside [0.15, 0.85] on either
  large-cap panel against BAR-OVL.
* **P4 HELD** but for the wrong reason (see above).
* **P5 HELD** — 0.53 is below m\* on u56 (vacuously: there is no m\*) and the signed INV dCAGR
  there is −2.68 pp/yr.
* **P6 FAILED** — S_MSTAR beats S_IS by +0.021 (it loses to S_NONE, as predicted). The
  prediction was that it beats neither; half of it held.

## Bearing on the ideas that queued this one

* **Idea 82 ("ranking subtracts value")**: supported, but its mechanism is now pinned. Ranking is
  not subtracting value by costing too much — on the exact incremental bar it costs 0.08 pp/yr at
  the incumbent's share. It subtracts value by pointing the wrong way.
* **Idea 124 (book-size floor)**: no cost-based floor is derivable from this axis. If a floor
  exists it must come from a different argument than "the tilt stops covering its cost".

## Caveats carried, not buried

Survivorship on all three current-constituent panels (idea 54); the eligibility gate is inverted
on the small panel (ideas 39/49), so its numbers describe a gate that does not work there; idea
38 (calendar-day index) and idea 126 (t+1 only) carry over; idea 128 (the IS window's SPY
drawdown is shallower than the OOS window's). The m → 1.00 endpoint forces all three tilts onto
the same eligible set, so g → 0 mechanically; the fitted estimator is therefore also reported on
m ≤ 0.70 and the empirical estimator treats a crossing at 1.00 as "no crossing". A block
bootstrap on one realised path measures sampling error around *this* path, not uncertainty across
worlds. m is a sample-average share; idea 157 (open) tests the time-varying n_t = round(m·E_t).
