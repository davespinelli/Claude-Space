# Idea 1730 — is path 4a's drawdown clause just a gross test?

Corpus 33 books (26 real, 7 null) x 2 panels = 66 books. Weekly, 10 bps, next-day execution, no leverage. Panels U56 / B136 are CURRENT CONSTITUENTS — survivorship bias applies to every level below; the regression is a WITHIN-panel contrast and is far less exposed to it than a level claim.

**U56**  SPY FULL 15.12% / 0.8843 / -33.72% (H1 0.9570 / H2 0.8249), OOS 15.26% / 0.8737 / -33.72%  |  RULES v2 FULL 8.62% / 1.2010 / -12.05% (H1 1.2276 / H2 1.1805), OOS 9.46% / 1.2766 / -12.05%, mean realised gross 0.5328
**B136**  SPY FULL 15.12% / 0.8844 / -33.72% (H1 0.9571 / H2 0.8249), OOS 15.26% / 0.8737 / -33.72%  |  RULES v2 FULL 7.96% / 1.0972 / -12.24% (H1 1.2296 / H2 0.9669), OOS 7.85% / 1.1017 / -12.24%, mean realised gross 0.5322

## (A) dMaxDD (pp, vs the LIVE book) regressed on REALISED-GROSS RATIO to the live book

| set | n | slope (pp per 1.0 of ratio) | intercept | R^2 | resid SD (pp) | resid min..max (pp) | rho(Spearman) |
|---|---|---|---|---|---|---|---|
| POOLED (all books, both panels) | 66 | -12.67 | +8.45 | 0.3686 | 6.91 | -27.74 .. +9.01 | -0.7223 |
| POOLED real only | 52 | -15.02 | +12.55 | 0.5312 | 5.10 | -18.26 .. +7.89 | -0.8058 |
| POOLED null only | 14 | -17.00 | +7.08 | 0.3870 | 10.24 | -23.33 .. +8.41 | -0.7495 |
| U56 all | 33 | -11.47 | +7.53 | 0.2980 | 6.98 | -27.66 .. +7.04 | -0.7152 |
| U56 real only | 26 | -14.18 | +12.16 | 0.5546 | 4.70 | -14.94 .. +6.36 | -0.8010 |
| B136 all | 33 | -13.67 | +9.12 | 0.4338 | 6.99 | -25.63 .. +9.61 | -0.7316 |
| B136 real only | 26 | -15.87 | +12.95 | 0.5229 | 5.58 | -17.48 .. +8.56 | -0.8092 |

### The same regression per device FAMILY (real books only, pooled panels)

| family | n | slope | R^2 | resid SD (pp) | mean gross ratio | mean dMaxDD (pp) |
|---|---|---|---|---|---|---|
| BAND | 8 | +8.66 | 0.0284 | 0.95 | 0.990 | -0.73 |
| DEGROSS | 8 | -15.95 | 0.9799 | 1.38 | 1.174 | -7.82 |
| LIVE | 2 | (n<3) | — | — | 1.408 | -5.37 |
| MADIST | 4 | -16.78 | 0.9796 | 0.72 | 0.486 | +4.22 |
| MAXVOL | 8 | -51.34 | 0.8059 | 1.37 | 1.356 | -6.64 |
| SPYFILT | 4 | +17.58 | 0.6878 | 0.37 | 1.142 | -2.89 |
| STOP | 4 | -18.74 | 0.9984 | 0.19 | 1.076 | -0.40 |
| TOPN | 8 | +583.28 | 0.5062 | 4.19 | 1.397 | -16.53 |
| VOLTGT | 6 | -16.30 | 0.9678 | 0.71 | 1.543 | -3.55 |

### 1631's headline, reproduced on this corpus

- U56: 24 of 33 books trip the MaxDD leg against the live book (mean dMaxDD -5.36 pp, 9 shallower); mean min-half Sharpe margin -0.2531.
- B136: 25 of 33 books trip the MaxDD leg against the live book (mean dMaxDD -5.87 pp, 8 shallower); mean min-half Sharpe margin -0.1956.
- BOTH PANELS: 49 of 66 trip, mean dMaxDD -5.62 pp, mean min-half margin -0.2243.

## (B) restated 4a against a GROSS-MATCHED incumbent — EVERY grid point

Pass counts over the pooled corpus (52 real, 14 null book-panel cells). `R0` is the CURRENT rule (live book, tau=0) and is the same at every row by construction.

| basis | tau (pp) | real PASS (FULL) | null PASS (FULL) | real PASS (IS) | null PASS (IS) | real PASS (OOS) | null PASS (OOS) | moves vs R0 (FULL) |
|---|---|---|---|---|---|---|---|---|
| MEAN | 0 | 3 of 52 | 0 of 14 | 2 of 52 | 0 of 14 | 6 of 52 | 0 of 14 | 2 of 66 |
| MEAN | 1 | 3 of 52 | 0 of 14 | 4 of 52 | 0 of 14 | 7 of 52 | 0 of 14 | 2 of 66 |
| MEAN | 2 | 4 of 52 | 0 of 14 | 16 of 52 | 0 of 14 | 8 of 52 | 0 of 14 | 3 of 66 |
| MEAN | 3 | 5 of 52 | 0 of 14 | 18 of 52 | 0 of 14 | 9 of 52 | 0 of 14 | 4 of 66 |
| MEAN | 5 | 7 of 52 | 0 of 14 | 23 of 52 | 0 of 14 | 9 of 52 | 0 of 14 | 6 of 66 |
| DAILY | 0 | 0 of 52 | 0 of 14 | 0 of 52 | 0 of 14 | 2 of 52 | 0 of 14 | 1 of 66 |
| DAILY | 1 | 5 of 52 | 0 of 14 | 8 of 52 | 0 of 14 | 9 of 52 | 0 of 14 | 4 of 66 |
| DAILY | 2 | 9 of 52 | 0 of 14 | 19 of 52 | 0 of 14 | 14 of 52 | 0 of 14 | 8 of 66 |
| DAILY | 3 | 13 of 52 | 0 of 14 | 25 of 52 | 1 of 14 | 17 of 52 | 0 of 14 | 12 of 66 |
| DAILY | 5 | 15 of 52 | 0 of 14 | 29 of 52 | 1 of 14 | 19 of 52 | 0 of 14 | 14 of 66 |

R0 (current rule 4a, live book as incumbent): real PASS 1 of 52, null PASS 0 of 14.

### Per-book detail at the two tau=0 rungs (the restatement the idea proposes)

| panel | book | gross ratio | dMaxDD vs LIVE (pp) | dMaxDD vs MEAN twin (pp) | dMaxDD vs DAILY twin (pp) | 4a now | 4a MEAN | 4a DAILY | 4b FULL | 4b OOS |
|---|---|---|---|---|---|---|---|---|---|---|
| B136 | BAND c=0.00 | 1.000 | -0.38 | -0.38 | -0.27 | . | . | . | . | . |
| B136 | BAND c=0.03 | 1.000 | +0.00 | +0.00 | +0.00 | . | . | . | . | . |
| B136 | BAND c=0.06 | 0.988 | -1.45 | -1.59 | -0.74 | . | . | . | . | . |
| B136 | BAND c=0.10 | 1.005 | -2.34 | -2.28 | -1.04 | . | . | . | . | . |
| B136 | DEGROSS G=0.25 | 0.470 | +3.21 | -3.19 | -2.60 | . | . | . | . | . |
| B136 | DEGROSS G=0.50 | 0.940 | -5.24 | -5.96 | -4.87 | . | . | . | . | . |
| B136 | DEGROSS G=0.75 | 1.410 | -13.13 | -8.43 | -6.84 | . | . | . | . | . |
| B136 | DEGROSS G=1.00 | 1.879 | -20.48 | -15.78 | -8.53 | . | . | . | . | . |
| B136 | RULES v1 (previous) | 1.409 | -8.96 | -4.25 | -2.67 | . | . | . | . | . |
| B136 | MADIST q=0.20 | 0.278 | +7.92 | -0.84 | -0.54 | . | . | . | . | . |
| B136 | MADIST q=0.50 | 0.699 | -0.05 | -3.65 | -2.79 | . | . | . | . | . |
| B136 | MAXVOL m=0.45 | 1.286 | -3.27 | +0.09 | -0.59 | . | Y | . | Y | . |
| B136 | MAXVOL m=0.60 | 1.359 | -6.46 | -2.24 | -2.23 | . | . | . | Y | Y |
| B136 | MAXVOL m=0.80 | 1.391 | -8.31 | -3.73 | -3.67 | . | . | . | . | . |
| B136 | MAXVOL m=1.00 | 1.401 | -11.44 | -6.73 | -5.76 | . | . | . | . | . |
| B136 | NULL_COINFLIP s=0 | 0.916 | -5.83 | -6.83 | -5.14 | . | . | . | . | . |
| B136 | NULL_PARITY | 0.705 | -26.15 | -29.68 | -8.04 | . | . | . | . | . |
| B136 | NULL_RAND s=0 | 0.215 | +7.62 | -1.93 | -1.71 | . | . | . | . | . |
| B136 | NULL_RAND s=1 | 0.215 | +7.72 | -1.83 | -1.61 | . | . | . | . | . |
| B136 | NULL_RAND s=2 | 0.215 | +7.84 | -1.71 | -1.49 | . | . | . | . | . |
| B136 | NULL_SHUFFLE s=0 | 1.404 | -11.03 | -6.33 | -4.74 | . | . | . | . | . |
| B136 | NULL_SHUFFLE s=1 | 1.404 | -16.85 | -12.14 | -10.56 | . | . | . | . | . |
| B136 | SPYFILT L=100 | 1.121 | -3.28 | -1.86 | -0.58 | . | . | . | . | . |
| B136 | SPYFILT L=200 | 1.164 | -2.85 | -0.91 | -2.96 | . | . | . | . | . |
| B136 | STOP s=0.10 | 0.876 | +3.24 | +1.76 | -0.01 | . | . | . | . | . |
| B136 | STOP s=0.20 | 1.251 | -3.83 | -0.87 | -1.01 | . | . | . | . | . |
| B136 | TOPN n=10 | 1.405 | -13.78 | -9.07 | -7.49 | . | . | . | . | . |
| B136 | TOPN n=20 | 1.405 | -13.73 | -9.03 | -7.44 | . | . | . | . | . |
| B136 | TOPN n=3 | 1.393 | -26.63 | -22.02 | -20.34 | . | . | . | . | . |
| B136 | TOPN n=5 | 1.397 | -17.07 | -12.41 | -10.78 | . | . | . | . | . |
| B136 | VOLTGT t=0.08 | 1.269 | +1.38 | +4.55 | -0.13 | Y | Y | . | . | Y |
| B136 | VOLTGT t=0.12 | 1.593 | -3.77 | +0.93 | -1.01 | . | Y | . | Y | Y |
| B136 | VOLTGT t=0.16 | 1.737 | -6.51 | -1.81 | -0.59 | . | . | . | Y | Y |
| U56 | BAND c=0.00 | 0.999 | +0.04 | +0.03 | -0.32 | . | . | . | . | . |
| U56 | BAND c=0.03 | 1.000 | +0.00 | +0.00 | +0.00 | . | . | . | . | . |
| U56 | BAND c=0.06 | 0.956 | -1.42 | -1.93 | -1.07 | . | . | . | . | . |
| U56 | BAND c=0.10 | 0.971 | -0.29 | -0.63 | -0.63 | . | . | . | . | . |
| U56 | DEGROSS G=0.25 | 0.470 | +4.10 | -2.20 | -1.81 | . | . | . | . | . |
| U56 | DEGROSS G=0.50 | 0.939 | -3.40 | -4.12 | -3.41 | . | . | . | . | . |
| U56 | DEGROSS G=0.75 | 1.408 | -10.47 | -6.34 | -4.81 | . | . | . | . | . |
| U56 | DEGROSS G=1.00 | 1.877 | -17.12 | -12.99 | -6.04 | . | . | . | . | . |
| U56 | RULES v1 (previous) | 1.407 | -1.77 | +2.36 | +3.89 | . | . | . | . | . |
| U56 | MADIST q=0.20 | 0.272 | +7.61 | -1.10 | -0.73 | . | . | . | . | . |
| U56 | MADIST q=0.50 | 0.696 | +1.39 | -2.20 | -1.70 | . | . | . | . | . |
| U56 | MAXVOL m=0.45 | 1.275 | -3.14 | +0.05 | -1.62 | . | . | . | . | Y |
| U56 | MAXVOL m=0.60 | 1.351 | -4.83 | -0.77 | -1.91 | . | . | . | Y | Y |
| U56 | MAXVOL m=0.80 | 1.387 | -6.82 | -2.69 | -2.72 | . | . | . | Y | Y |
| U56 | MAXVOL m=1.00 | 1.400 | -8.87 | -4.74 | -3.80 | . | . | . | . | . |
| U56 | NULL_COINFLIP s=0 | 0.913 | -4.20 | -5.22 | -3.89 | . | . | . | . | . |
| U56 | NULL_PARITY | 0.704 | -28.21 | -31.70 | -10.85 | . | . | . | . | . |
| U56 | NULL_RAND s=0 | 0.521 | +3.00 | -2.68 | -2.36 | . | . | . | . | . |
| U56 | NULL_RAND s=1 | 0.521 | +2.52 | -3.16 | -2.85 | . | . | . | . | . |
| U56 | NULL_RAND s=2 | 0.521 | +3.24 | -2.44 | -2.12 | . | . | . | . | . |
| U56 | NULL_SHUFFLE s=0 | 1.398 | -8.27 | -4.14 | -2.61 | . | . | . | . | . |
| U56 | NULL_SHUFFLE s=1 | 1.398 | -20.10 | -15.97 | -14.44 | . | . | . | . | . |
| U56 | SPYFILT L=100 | 1.119 | -3.27 | -1.88 | -1.49 | . | . | . | . | . |
| U56 | SPYFILT L=200 | 1.163 | -2.14 | -0.25 | -2.58 | . | . | . | . | . |
| U56 | STOP s=0.10 | 0.925 | +2.56 | +1.68 | -1.02 | . | . | . | . | . |
| U56 | STOP s=0.20 | 1.252 | -3.56 | -0.64 | -1.37 | . | . | . | . | . |
| U56 | TOPN n=10 | 1.399 | -12.04 | -7.90 | -6.38 | . | . | . | . | . |
| U56 | TOPN n=20 | 1.402 | -10.16 | -6.02 | -4.81 | . | . | . | . | . |
| U56 | TOPN n=3 | 1.387 | -22.44 | -18.31 | -16.78 | . | . | . | . | . |
| U56 | TOPN n=5 | 1.391 | -16.40 | -12.27 | -10.74 | . | . | . | . | . |
| U56 | VOLTGT t=0.08 | 1.290 | -0.22 | +3.13 | -1.91 | . | . | . | . | Y |
| U56 | VOLTGT t=0.12 | 1.616 | -4.38 | -0.25 | -2.37 | . | . | . | Y | Y |
| U56 | VOLTGT t=0.16 | 1.754 | -7.81 | -3.67 | -4.33 | . | . | . | Y | Y |

## (C) rule 8 — (basis, tau) and the book both fitted on 2009-2016 ONLY; 2017-2026 read once

Pre-registered chooser: at each (basis, tau) take the REAL books that pass the restated 4a on IS rows only, pick the highest IS Sharpe among them (ties -> corpus order), then read that book's OOS once.  `C_NOW` is the same chooser under the CURRENT rule (live incumbent, tau=0).  A rung whose IS-pass set admits a NULL is flagged.

| panel | chooser | IS pass set (real) | IS nulls admitted | pick | OOS CAGR | OOS Sharpe | OOS MaxDD | 4a OOS | 4b OOS |
|---|---|---|---|---|---|---|---|---|---|
| U56 | C_NOW (live incumbent, tau=0) | 2 | 0 | MADIST q=0.50 | 7.42% | 1.1757 | -10.67% | . | . |
| U56 | C_MEAN_tau0 | 2 | 0 | MADIST q=0.50 | 7.42% | 1.1757 | -10.67% | . | . |
| U56 | C_MEAN_tau1 | 3 | 0 | MADIST q=0.50 | 7.42% | 1.1757 | -10.67% | . | . |
| U56 | C_MEAN_tau2 | 9 | 0 | TOPN n=20 | 16.54% | 1.1629 | -22.21% | . | . |
| U56 | C_MEAN_tau3 | 9 | 0 | TOPN n=20 | 16.54% | 1.1629 | -22.21% | . | . |
| U56 | C_MEAN_tau5 | 11 | 0 | TOPN n=20 | 16.54% | 1.1629 | -22.21% | . | . |
| U56 | C_DAILY_tau0 | 0 | 0 | (none) | — | — | — | — | — |
| U56 | C_DAILY_tau1 | 4 | 0 | MADIST q=0.50 | 7.42% | 1.1757 | -10.67% | . | . |
| U56 | C_DAILY_tau2 | 8 | 0 | MADIST q=0.50 | 7.42% | 1.1757 | -10.67% | . | . |
| U56 | C_DAILY_tau3 | 11 | 1 | TOPN n=20 | 16.54% | 1.1629 | -22.21% | . | . |
| U56 | C_DAILY_tau5 | 12 | 1 | TOPN n=20 | 16.54% | 1.1629 | -22.21% | . | . |
| U56 | *SPY (bar)* | — | — | SPY | 15.26% | 0.8737 | -33.72% | — | — |
| U56 | *RULES v2 (bar)* | — | — | live | 9.46% | 1.2766 | -12.05% | — | — |
| B136 | C_NOW (live incumbent, tau=0) | 1 | 0 | DEGROSS G=0.25 | 4.55% | 1.0891 | -9.03% | . | . |
| B136 | C_MEAN_tau0 | 0 | 0 | (none) | — | — | — | — | — |
| B136 | C_MEAN_tau1 | 1 | 0 | STOP s=0.20 | 9.40% | 1.0660 | -16.07% | . | . |
| B136 | C_MEAN_tau2 | 7 | 0 | STOP s=0.20 | 9.40% | 1.0660 | -16.07% | . | . |
| B136 | C_MEAN_tau3 | 9 | 0 | STOP s=0.20 | 9.40% | 1.0660 | -16.07% | . | . |
| B136 | C_MEAN_tau5 | 12 | 0 | VOLTGT t=0.16 | 15.36% | 1.1837 | -18.76% | . | Y |
| B136 | C_DAILY_tau0 | 0 | 0 | (none) | — | — | — | — | — |
| B136 | C_DAILY_tau1 | 4 | 0 | STOP s=0.20 | 9.40% | 1.0660 | -16.07% | . | . |
| B136 | C_DAILY_tau2 | 11 | 0 | STOP s=0.20 | 9.40% | 1.0660 | -16.07% | . | . |
| B136 | C_DAILY_tau3 | 14 | 0 | VOLTGT t=0.16 | 15.36% | 1.1837 | -18.76% | . | Y |
| B136 | C_DAILY_tau5 | 17 | 0 | VOLTGT t=0.16 | 15.36% | 1.1837 | -18.76% | . | Y |
| B136 | *SPY (bar)* | — | — | SPY | 15.26% | 0.8737 | -33.72% | — | — |
| B136 | *RULES v2 (bar)* | — | — | live | 7.85% | 1.1017 | -12.24% | — | — |

## Both KEEP paths over the whole corpus (rule 4)

| panel | 4a FULL | 4b FULL | 4a OOS | 4b OOS | BOTH 4b |
|---|---|---|---|---|---|
| U56 | 0 of 33 | 4 of 33 | 0 of 33 | 6 of 33 | 4 of 33 |
| B136 | 1 of 33 | 4 of 33 | 2 of 33 | 4 of 33 | 3 of 33 |

## Gates

**74 of 74 pass.**

| gate | value | ok |
|---|---|---|
| G1 U56 fast_run vs engine.backtest (returns / turnover, FULL) | 0.000e+00 / 0.000e+00 | OK |
| G2 U56 live RULES v2 FULL cell | 8.62% / 1.2010 / -12.05% | OK |
| G4 U56 no leverage (max target gross over corpus) | 1.000000 | OK |
| G1 B136 fast_run vs engine.backtest (returns / turnover, FULL) | 0.000e+00 / 0.000e+00 | OK |
| G2 B136 live RULES v2 FULL cell | 7.96% / 1.0972 / -12.24% | OK |
| G4 B136 no leverage (max target gross over corpus) | 1.000000 | OK |
| G5 two tuned dials only | basis (MEAN/DAILY), tau (0-5 pp) | OK |
| G6 grid points reported | 2x5 = 10 x 33 books x 2 panels = 660 rows | OK |
| G3 DAILY twin target-gross match, all 66 (book, panel) cells | max 4.441e-16 | OK |
