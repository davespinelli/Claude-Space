# Idea 535 — is-the-FAMILY-constant-really-a-c_sd-constant (cloud, 2026-09-09)

**B3 reproduction PASS** (max |d resid0| 2.220e-16 pp, max |d c_sd| 9.931e-17 vs idea 301's committed .decomp.csv).

**B1 RETIREMENT PASS** — honest (.is) c_sd forms clearing both legs: ['CSD.is', 'CSD0.is', 'LOGCSD.is', 'CSD+CBAR.is', 'FAM+CSD.is']; clearing the pooled leg only: none.
**B2 WITHIN-FAMILY PASS** — CSD.is OOS MAE 0.3222 vs the MA-THRESH IS constant 0.3517 on the same 81 OOS cells.

Incumbent FAMILY (lam=1): OOS MAE **0.1936** (ALL 162) / **0.3517** (MA-THRESH 81). ZERO 0.2641/0.4903. GLOBAL 0.2458 (ALL).
PEEK ceiling (contemporaneous c_sd, unavailable ex ante): 0.1793 ALL / 0.3264 MA-THRESH.

## corr(c_sd, |resid0|), pooled vs within family

```
                    n  corr_abs  corr_signed  c_sd_mean  c_sd_sd  resid_mean  resid_sd
window subset                                                                         
IS     ALL        162    0.6795      -0.4468     0.0637   0.0734     -0.1211    0.2583
       MA-THRESH   81    0.4606      -0.3143     0.1219   0.0630     -0.2076    0.3441
       QUANTILE    81    0.5164      -0.5073     0.0055   0.0027     -0.0346    0.0273
OOS    ALL        162    0.7690      -0.7664     0.0586   0.0673     -0.2566    0.3539
       MA-THRESH   81    0.5480      -0.5471     0.1112   0.0591     -0.4861    0.3790
       QUANTILE    81    0.6465      -0.1793     0.0060   0.0036     -0.0270    0.0424
```

## Every honest c_sd form at its own best lambda (ALL cut)

```
             lam_star  MAE_ALL  MAE_MA  MAE_QU  ratio_vs_FAMILY_ALL  ratio_vs_FAMILY_MA    B1a    B1b
form                                                                                                 
CSD.is         1.0000   0.1771  0.3222  0.0320               0.9151              0.9161   True   True
CSD0.is        1.0000   0.1780  0.3234  0.0326               0.9197              0.9196   True   True
LOGCSD.is      1.0000   0.1813  0.3309  0.0317               0.9365              0.9407   True   True
CSDxVOL.is     1.0000   0.1968  0.3623  0.0312               1.0166              1.0301  False  False
CSD+CBAR.is    1.0000   0.1823  0.3306  0.0341               0.9420              0.9399   True   True
FAM+CSD.is     1.0000   0.1787  0.3242  0.0331               0.9230              0.9217   True   True
```

## WF-A (rule 8): (level, cadence) chosen on IS Sharpe, OOS read once

```
                             pick_level pick_cad  oCAGR  oSharpe  oMaxDD  spy_oSharpe  live_oSharpe  beats_SPY_oos  beats_LIVE_oos    p4a    p4b
panel    family    con                                                                                                                          
B136     MA-THRESH DEGROSS      -0.2500        Q 0.1358   1.1384 -0.2416       0.8820        1.2851           True           False  False  False
                   RESPREAD      0.2000        Q 0.2111   1.0665 -0.2953       0.8820        1.2851           True           False  False  False
         QUANTILE  DEGROSS       0.9000        Q 0.1250   1.1284 -0.2233       0.8820        1.2851           True           False  False  False
                   RESPREAD      0.9000        Q 0.1385   1.1262 -0.2465       0.8820        1.2851           True           False  False  False
SMALL439 MA-THRESH DEGROSS      -0.4000        Q 0.0798   0.5874 -0.3247       0.8820        1.2851          False           False  False  False
                   RESPREAD      0.3000        M 0.2402   1.1042 -0.3078       0.8820        1.2851           True           False  False  False
         QUANTILE  DEGROSS       0.8000        Q 0.0759   0.6225 -0.2816       0.8820        1.2851          False           False  False  False
                   RESPREAD      0.8000        Q 0.0919   0.6169 -0.3507       0.8820        1.2851          False           False  False  False
U56      MA-THRESH DEGROSS       0.3000        Q 0.0105   0.5677 -0.0338       0.8786        1.2817          False           False  False  False
                   RESPREAD      0.2000        Q 0.2138   0.9389 -0.3251       0.8786        1.2817           True           False  False  False
         QUANTILE  DEGROSS       0.5000        M 0.0802   1.2214 -0.1032       0.8786        1.2817           True           False  False  False
                   RESPREAD      0.5000        M 0.1602   1.2210 -0.1980       0.8786        1.2817           True           False  False   True
```

WF-A picks beat SPY OOS 8/12, RULES v2 0/12. 4a 0/324 books, 4b 16/324 books.

SURVIVORSHIP: SMALL439/U56/B136 are current constituents only (no delistings); CAGR levels and the 4a/4b columns are inflated. The residual is an arm-minus-arm contrast on the same names and days, so the bias very largely cancels out of it.
