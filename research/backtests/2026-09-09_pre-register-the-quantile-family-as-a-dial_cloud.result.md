# Idea 299 — pre-register-the-quantile-family-as-a-dial (cloud, 2026-09-09)

**A3 reproduction PASS** (max |d| 2.220e-16 vs idea 301's committed weekly cells).

**A1 FAIL** — 3 of 27 (family, x) cells clear 4b on both U56 and B136; 0 also clear the DD cap by > 1.0 pp. Cells: none.
**A2 FAIL** — walk-forward (x chosen on IS Sharpe only) cells clearing both panels: none.

**VERDICT: PARK**

## Idea 298's PARK candidate at the weekly default (U56, QUANTILE, x=0.50)

```
    CAGR  Sharpe   MaxDD     H1     H2  oCAGR  oSharpe  dd_margin_pp f4b f4b_25
6 0.1452  1.1942 -0.2093 1.2879 1.1238 0.1519   1.1862       -0.7000  DD     DD
```

## A1 table (every (family, x) cell on the two required panels)

```
                 U56_Sharpe  U56_MaxDD  U56_ddmargin    U56_f4b  B136_Sharpe  B136_MaxDD  B136_ddmargin      B136_f4b  both_4b  both_margin     A1
family    level                                                                                                                                   
MA-THRESH -0.40      1.1223    -0.2211       -1.8760         DD       1.1223     -0.2508        -4.8520            DD    False        False  False
          -0.25      1.1318    -0.2166       -1.4249         DD       1.1123     -0.2481        -4.5789            DD    False        False  False
          -0.12      1.1368    -0.2010        0.1306          -       1.0683     -0.2293        -2.6976            DD    False        False  False
          -0.06      1.1341    -0.1881        1.4166          -       1.0575     -0.2156        -1.3330            DD    False        False  False
           0.00      1.0948    -0.1862        1.6073          -       1.0585     -0.2012         0.1129             -     True        False  False
           0.06      1.0547    -0.2212       -1.8916         DD       1.0133     -0.2163        -1.4018            DD    False        False  False
           0.12      1.0812    -0.2421       -3.9764         DD       0.9732     -0.2320        -2.9710            DD    False        False  False
           0.20      0.8861    -0.4853      -28.3028  H2,OOS,DD       0.8501     -0.3494       -14.7132  H1,H2,OOS,DD    False        False  False
           0.30      0.9836    -0.6143      -41.1967  H2,OOS,DD       0.9739     -0.5134       -31.1058            DD    False        False  False
QUANTILE   0.20      1.0943    -0.2093       -0.6989         DD       1.0468     -0.2143        -1.2034            DD    False        False  False
           0.30      1.1089    -0.2088       -0.6485         DD       1.0260     -0.2232        -2.0864            DD    False        False  False
           0.40      1.1481    -0.2118       -0.9527         DD       1.0463     -0.2306        -2.8314            DD    False        False  False
           0.50      1.1942    -0.2093       -0.7000         DD       1.0492     -0.2359        -3.3652            DD    False        False  False
           0.60      1.2069    -0.2027       -0.0367         DD       1.0787     -0.2359        -3.3573            DD    False        False  False
           0.70      1.1472    -0.2041       -0.1762         DD       1.0806     -0.2394        -3.7110            DD    False        False  False
           0.80      1.1360    -0.2136       -1.1257         DD       1.0785     -0.2439        -4.1563            DD    False        False  False
           0.90      1.1525    -0.2120       -0.9731         DD       1.1135     -0.2437        -4.1400            DD    False        False  False
           0.95      1.1472    -0.2221       -1.9834         DD       1.1279     -0.2474        -4.5139            DD    False        False  False
QUANTxMA   0.20      1.0962    -0.2093       -0.6989         DD       1.0603     -0.2143        -1.1955            DD    False        False  False
           0.30      1.0952    -0.2083       -0.6012         DD       1.0303     -0.2137        -1.1441            DD    False        False  False
           0.40      1.1095    -0.2097       -0.7368         DD       1.0360     -0.2104        -0.8065            DD    False        False  False
           0.50      1.1140    -0.2041       -0.1842         DD       1.0296     -0.2091        -0.6824            DD    False        False  False
           0.60      1.1104    -0.1989        0.3447          -       1.0429     -0.2087        -0.6453            DD    False        False  False
           0.70      1.0766    -0.1957        0.6579          -       1.0443     -0.2072        -0.4915            DD    False        False  False
           0.80      1.0805    -0.1925        0.9814          -       1.0454     -0.2048        -0.2459            DD    False        False  False
           0.90      1.0931    -0.1862        1.6073          -       1.0585     -0.2012         0.1129             -     True        False  False
           0.95      1.0949    -0.1862        1.6073          -       1.0583     -0.2012         0.1129             -     True        False  False
```

## A2 rule-8 walk-forward

```
                               level  oCAGR  oSharpe  oMaxDD  spy_oSharpe  live_oSharpe  beats_SPY_oos  beats_LIVE_oos  dd_margin_pp    p4b
pick      family    panel                                                                                                                  
POOLED-IS QUANTILE  U56       0.9500 0.1358   1.1358 -0.2221       0.8786        1.2817           True           False       -1.9834  False
                    B136      0.9500 0.1383   1.1108 -0.2474       0.8820        1.2851           True           False       -4.5139  False
                    SMALL439  0.9500 0.0942   0.6032 -0.3700       0.8820        1.2851          False           False      -16.7672  False
          MA-THRESH U56      -0.1200 0.1223   1.1096 -0.2010       0.8786        1.2817           True           False        0.1306   True
                    B136     -0.1200 0.1192   1.0304 -0.2293       0.8820        1.2851           True           False       -2.6976  False
                    SMALL439 -0.1200 0.0754   0.5467 -0.3527       0.8820        1.2851          False           False      -15.0384  False
          QUANTxMA  U56       0.2000 0.1802   1.0877 -0.2093       0.8786        1.2817           True           False       -0.6989  False
                    B136      0.2000 0.1515   1.0462 -0.2143       0.8820        1.2851           True           False       -1.1955  False
                    SMALL439  0.2000 0.0937   0.6028 -0.3747       0.8820        1.2851          False           False      -17.2391  False
PANEL-IS  MA-THRESH B136     -0.4000 0.1378   1.0986 -0.2508       0.8820        1.2851           True           False       -4.8520  False
          QUANTILE  B136      0.9500 0.1383   1.1108 -0.2474       0.8820        1.2851           True           False       -4.5139  False
          QUANTxMA  B136      0.2000 0.1515   1.0462 -0.2143       0.8820        1.2851           True           False       -1.1955  False
          MA-THRESH SMALL439 -0.4000 0.0813   0.5507 -0.3556       0.8820        1.2851          False           False      -15.3337  False
          QUANTILE  SMALL439  0.9500 0.0942   0.6032 -0.3700       0.8820        1.2851          False           False      -16.7672  False
          QUANTxMA  SMALL439  0.2000 0.0937   0.6028 -0.3747       0.8820        1.2851          False           False      -17.2391  False
          MA-THRESH U56      -0.1200 0.1223   1.1096 -0.2010       0.8786        1.2817           True           False        0.1306   True
          QUANTILE  U56       0.5000 0.1519   1.1862 -0.2093       0.8786        1.2817           True           False       -0.7000  False
          QUANTxMA  U56       0.2000 0.1802   1.0877 -0.2093       0.8786        1.2817           True           False       -0.6989  False
```

4a 0/162 books, 4b 14/162, 4b at 25 bps 5/162.

SURVIVORSHIP: U56/B136/SMALL439 are current constituents only (no delistings), so every CAGR level and both KEEP columns are inflated. SMALL439 drops every ticker with max_1d_move >= 1.0 in data/small_meta.csv.
