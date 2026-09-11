# Idea 538 - is c_sd the right SCALE, or is it a TURNOVER proxy?  (lane B, 2026-09-11)

Population: idea 535's exact 162 cells (3 panels x 2 families x 9 levels x 3 cadences ['W', 'M', 'Q'], gross 0.75), 324 books, 10 bps, next-day execution.
Tuned: PREDICTOR FORM (13) x SHRINKAGE [0.0, 0.25, 0.5, 0.75, 1.0] = 65 estimator cells, all reported on all 3 subsets.

## Gates
- **G1 REPRODUCTION FAIL** - max|d resid0_pp| 6.864e-03 pp, max|d c_sd| 8.510e-05 vs idea 301; max|d turn_yr| 9.144e-03 vs idea 535; ladder reproduces MAE(CSD.is) 0.177296 (published 0.177128) and MAE(FAMILY) 0.193700 (published 0.193564).
- **G2 DISTINCT** - rho(c_sd_is, turn_yr_DG_is) over n=162: PEARSON +0.0444, SPEARMAN -0.1291; CSD+TO design condition number 26.63.

## Bars
- **B1 FAIL** - best honest turnover form DTO.is (lam 0.75): OOS MAE ALL 0.2391 vs bar 0.1840 (fail); MA-THRESH 0.3991 vs 0.3521 (fail).
- **B2 FAIL** - DTO.is 0.2391 vs CSD.is 0.1773 on the ALL cut (+0.0618 pp/yr).
- **B3 FAIL** - CSD+TO.is 0.1787 vs bar 0.1684 (increment over c_sd alone +0.0014 pp/yr).
- **B4 PASS** - c_sd orthogonalised on turnover: slope -1.5690, t -6.29 vs raw t -6.32; mirror (turnover net of c_sd) t -0.27 of raw -0.52.

## Rule 8
- WF-A: 12 arms, (level, cadence) picked on IS Sharpe alone. Beat RULES v2 OOS 0/12, SPY 8/12, no-gate EWall control 5/12.
- WF-B: every ladder rung is an IS fit scored once on the OOS-window residual.
- WF-C: always-RESPREAD 0.9350 / always-DEGROSS 0.9036 / oracle 0.9410 mean OOS Sharpe; every honest form's share of the oracle gap is in `.walkforward` prose above.

## KEEP paths
- 4a 0/324 books; 4b 16/324 books.

SURVIVORSHIP: all three panels are current constituents; CAGR levels are inflated and the 4a/4b columns inherit that. The headline object is an arm-minus-arm contrast on the same names, days and gross, so the bias very largely cancels out of gap0/pred0/resid0.
