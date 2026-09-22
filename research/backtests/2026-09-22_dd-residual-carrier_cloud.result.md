# Idea 909 — what is IN the DD-residual?

**Lane cloud, 2026-09-22.  Script:** `research/backtests/2026-09-22_dd-residual-carrier_cloud.py`

## ANSWER: mostly CONCENTRATION (breadth, read directly or as return skewness) plus a real fat-tail term on U56.  GATE TIMING — the idea's own second hypothesis — is DEAD.  No single carrier is sufficient, so the pre-stated naming bar is NOT met.

867/911's residual reproduces exactly on all three panels before anything is decomposed:
rho(res_IS, res_OOS) = **+0.8373 / +0.3426 / +0.3652** (U56 / B136 / SMALL), residual spread
1.30 / 2.24 / 3.95 pp IS and 2.06 / 2.69 / 6.49 pp OOS.

### V1 — does the residual have a NAME?  NOT TRIGGERED (0 of 3 panels at R² ≥ 0.50)

Best single carrier is **daily return skewness on all three panels**, and it misses the bar:
R²_IS **0.4893** (B136), **0.4302** (U56), **0.2206** (SMALL).  Next is breadth —
`n_held` R²_IS 0.3144 / 0.4221 / 0.1602 — and on U56 kurtosis adds a genuinely separate
0.2751.  The idea's own **gate-timing** carrier is worthless: R²_IS **0.0182 / 0.0064 / 0.0005**.

| carrier | U56 R²_IS (rho) | B136 R²_IS (rho) | SMALL R²_IS (rho) |
|---|---|---|---|
| skew | 0.4302 (−0.656) | **0.4893 (−0.700)** | 0.2206 (−0.470) |
| n_held / eff_breadth | 0.4221 (+0.650) | 0.3144 (+0.561) | 0.1602 (+0.400) |
| kurt | 0.2751 (−0.525) | 0.0343 (−0.185) | 0.0091 (+0.095) |
| mean_gross | 0.1148 (−0.339) | 0.0124 (−0.111) | 0.0021 (−0.046) |
| w5 (worst 5-day) | 0.0339 (+0.184) | 0.0270 (+0.164) | 0.0057 (+0.075) |
| gate_share | 0.0182 (−0.135) | 0.0064 (+0.080) | 0.0005 (+0.021) |

As **sets**, the tail triple carries most of it: TAIL R²_IS **0.7558 / 0.6398 / 0.4741**, against
BREADTH 0.4660 / 0.3144 / 0.1845 and TIMING 0.1836 / 0.0159 / 0.0022.  ALL seven reaches
0.7715 / 0.6877 / 0.6074 — i.e. adding breadth and timing to TAIL buys 1.6 / 4.8 / 13.3 pp of R².

**Read the sign before quoting it.**  rho(res, skew) is NEGATIVE, and that is *not* "negative
skew means a worse drawdown".  Residual > 0 means a SHALLOWER drawdown at matched beta, and
every U56/B136 shelf book is already left-skewed (skew ∈ [−0.44, −0.01] and [−0.47, +0.05]).
What the sign says is that the MORE negatively skewed books draw down LESS.  The mechanism is
breadth: corr(skew, n_held) = **−0.745 / −0.436 / −0.270**.  A 40-name book diversifies away
idiosyncratic up-spikes and is left-skewed like an index; a 5-name book has big idiosyncratic
up-moves (less negative, on SMALL positively skewed) and a deeper drawdown.  Skew and breadth
are two readings of one object, which is why their R² are near-identical on U56 (0.430 vs 0.422).
Kurtosis is the part that is NOT breadth (corr(kurt, n_held) = −0.167 / −0.248 / −0.029) and it
enters with the naive sign on U56/B136: fatter tails, deeper drawdown at matched beta.

### V2 — is the carrier what PERSISTS?  NOT TRIGGERED as pre-stated; TRIGGERED on the TAIL set alone

The pre-stated rule strips the set with the highest R²_IS, which is ALL on every panel.  ALL
strips only 43.3% / 35.3% / 31.1% of the persistence — **0 of 3** panels halved.

But ALL is a diluted instrument: `n_held` and `eff_breadth` are collinear to **corr = +1.000000**
on all three panels (standardised coefficients of ±409, ±839 with |t| ≈ 0.2–3.9 — the fit is
splitting one variable into two cancelling halves), and TIMING adds nothing.  The **TAIL** set,
equally pre-registered, is the informative one:

| panel | rho_raw | after stripping TAIL | share lost | in the shuffle null? |
|---|---|---|---|---|
| U56 | +0.8373 | +0.3494 | **+0.583** | OUT (still real) |
| B136 | +0.3426 | +0.1415 | **+0.587** | **IN** [−0.212, +0.225] |
| SMALL | +0.3652 | **−0.0001** | **+1.000** | **IN** [−0.222, +0.238] |

Stripping left-tail shape **halves the persistence on 3 of 3 panels and annihilates it on SMALL**,
leaving B136's inside the noise band.  Only U56 keeps a residual-of-the-residual that is still
outside the null.  This is a secondary reading of a pre-registered set, reported as such — the
pre-stated V2 rule keyed on R²_IS and is NOT triggered.  The record should carry both.

### ARM 3 — gate timing is the one carrier that does not persist

rho(carrier_IS, carrier_OOS): `mean_gross`, `n_held`, `eff_breadth` **+0.9994 to +1.0000**
(construction constants, as expected), `w5` +0.961 / +0.920 / +0.870, `skew` +0.744 / +0.723 /
+0.565, `kurt` +0.128 / +0.035 / +0.312, and **`gate_share` −0.237 / −0.222 / +0.414**.
The share of a book's decline taken while already de-grossed is the only carrier whose IS value
tells you nothing about its OOS value — on two of three panels it flips sign.  Idea 909's
"gate timing" hypothesis is **KILLED** on both legs: it explains nothing in-sample and it does
not persist.

### V3 — CAPITAL (rule 8, 2017–2026 read ONCE): NOT TRIGGERED.  0 of 18 picks clear 4b, 0 of 18 clear 4a

Six legal IS-only choosers × 3 panels; all 18 picks in `.walkforward.csv`.  Every IS_CARRIER
chooser reaches **0 of 3** arms on 4b FULL+OOS, matching IS_RESID (0 of 3) and IS_SHARPE (0 of 3).

The informative part is **which leg each reading fails**.  The carrier choosers argmax onto the
shallowest books on the shelf — U56 `MADIST|ALL|0.25` at 3.88% / 1.136 / **−5.93%** (OOS 4.27% /
1.217 / −5.93%) — which clear the 4b drawdown cap with room to spare and then die on the CAGR
floor (3.88% against a 10.60% bar).  911's IS_RESID chooser goes the other way, onto
`MADIST|ALL|1.00` at 15.82% / 1.141 / **−22.18%**, clearing the CAGR floor and dying on the DD
cap.  **The two readings of the same residual fail 4b on opposite legs**, and nothing on the
shelf sits between them.  Reference books on the same tape: RULES v2 (live) U56 8.62% / 1.201 /
−12.05% (OOS 9.46% / 1.277); B136 7.96% / 1.097 (OOS 7.85% / 1.102); SMALL 4.26% / 0.659 (OOS
3.63% / 0.545).  SPY 15.14% / 0.885 / −33.72%, halves 0.96 / 0.83, OOS 15.29% / 0.875 / −33.72%.

## BY-PRODUCT KILL for the record's conventions

`n_held` and `eff_breadth` correlate at **+1.000000** across all 240 shelf books on all three
panels.  Any published decomposition that carries both as separate carriers is reporting one
variable twice and will produce ±400-sized cancelling coefficients.  Future runs should carry
`n_held` alone.

## GATES

All pass.  G0 sample ≥ 10y (U56/B136 18.7y, SMALL 16.7y).  G2 a 100%-SPY book reads beta 1.0000
(max |β−1| = 0.0000).  G3 no leverage (max shelf gross 1.0000).  G4 `gate_share` defined on
100.0% of book-windows.  G5 every grid point published (12 set rows, 21 single-carrier rows).

## DIALS AND HONESTY

Exactly two tuned dials, every value reported: **CARRIER SET** {TAIL, TIMING, BREADTH, ALL} ×
**PANEL** {U56, B136, SMALL}.  The beta estimator (OLSD, 867/911's own), the shelf and the
reference choosers are reported, not tuned.  All 21 single-carrier readings are in `.single.csv`,
all 12 set fits in `.sets.csv`, all 12 stripping tests in `.persistence.csv`, all 21 carrier
persistences in `.carrierpersistence.csv`, all 240 book-window rows in `.shelf.csv`, all 18
capital picks in `.walkforward.csv`.  Shuffle null: 2000 draws, seed 20260922.

**SURVIVORSHIP.**  U56 and B136 are current-constituent lists; SMALL is a current sub-$2B screen
(54 of 720 tickers with `max_1d_move >= 1.0` dropped first, 666 kept).  Every CAGR, Sharpe and
MaxDD **level** is survivorship-optimistic, and the capital arm's levels inherit that in full.
The decomposition arms are same-shelf, same-tape contrasts and are first-order immune.
