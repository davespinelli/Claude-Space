load_prices: network unavailable (ModuleNotFoundError); using prices.csv
load_prices: network unavailable (ModuleNotFoundError); using prices.csv
========================================================================================================================================================================================================
Idea 266 the-hindsight-overlap-test-as-a-pre-registration-check | 2026-09-06_the-hindsight-overlap-test-as-a-pre-registration-check_cloud.py
sets: STK20=20, BROAD8=8, SECT16=16, BFC12=12, ETF36=36, BSTK100=100, SMALL439=439, SMALL483=483, ALLSTK=583
  frame U56   2008-01-02 -> 2026-09-04, 56 columns
  frame B136  2008-01-02 -> 2026-09-04, 136 columns
  frame SMALL 2010-01-04 -> 2026-09-04, 484 columns
  frame POOL  2010-01-04 -> 2026-09-04, 583 columns
windows per frame: FULL = the frame's own span | IS ..2016-12-31 | OOS 2017-01-01.. | metrics ['TOTRET', 'SHARPE'] | conventions PUB (idea 71's) and COV (unrankable names dropped)
small panel: 44 tickers dropped by the max_1d_move>=1.0 screen
========================================================================================================================================================================================================

--- PART A: hindsight-overlap census, panel x convention x metric x window (exact hypergeometric) -------------------------
                                      superset_n    k  unrankable  obs    exp  excess         p  p_lt_05                           note
panel             conv metric window                                                                                                   
STK20             PUB  TOTRET FULL           100   20          11   10      4       6 0.0006475     True                               
                              IS             100   20          11    7      4       3   0.06367    False                               
                              OOS            100   20           3    8      4       4   0.01809     True                               
                       SHARPE FULL           100   20          11   10      4       6 0.0006475     True                               
                              IS             100   20          11    7      4       3   0.06367    False                               
                              OOS            100   20           3    9      4       5  0.003931     True                               
                  COV  TOTRET FULL            89   16          11    8  2.876   5.124  0.001094     True                               
                              IS              89   16          11    6  2.876   3.124   0.03558     True                               
                              OOS             97   19           3    8  3.722   4.278   0.01035     True                               
                       SHARPE FULL            89   16          11    9  2.876   6.124 0.0001137     True                               
                              IS              89   16          11    5  2.876   2.124    0.1236    False                               
                              OOS             97   19           3    9  3.722   5.278  0.001933     True                               
STK20 vs ALLSTK   PUB  TOTRET FULL           583   20         225   11 0.6861   10.31 4.105e-13     True                size-confounded
                              IS             583   20         225    2 0.6861   1.314    0.1469    False                size-confounded
                              OOS            583   20         148    6 0.6861   5.314 2.102e-05     True                size-confounded
                       SHARPE FULL           583   20         225   10 0.6861   9.314 2.512e-11     True                size-confounded
                              IS             583   20         225    3 0.6861   2.314   0.02712     True                size-confounded
                              OOS            583   20         148    8 0.6861   7.314 4.012e-08     True                size-confounded
                  COV  TOTRET FULL           358   18         225    9  0.905   8.095  7.94e-09     True                size-confounded
                              IS             358   18         225    2  0.905   1.095    0.2269    False                size-confounded
                              OOS            435   19         148    5 0.8299    4.17 0.0007232     True                size-confounded
                       SHARPE FULL           358   18         225    9  0.905   8.095  7.94e-09     True                size-confounded
                              IS             358   18         225    3  0.905   2.095   0.05418    False                size-confounded
                              OOS            435   19         148    8 0.8299    7.17 1.482e-07     True                size-confounded
BROAD8            PUB  TOTRET FULL            36    8           2    4  1.778   2.222   0.05378    False                               
                              IS              36    8           2    3  1.778   1.222    0.2357    False                               
                              OOS             36    8           1    3  1.778   1.222    0.2357    False                               
                       SHARPE FULL            36    8           2    4  1.778   2.222   0.05378    False                               
                              IS              36    8           2    3  1.778   1.222    0.2357    False                               
                              OOS             36    8           1    4  1.778   2.222   0.05378    False                               
                  COV  TOTRET FULL            34    8           2    4  1.882   2.118   0.06617    False                               
                              IS              34    8           2    3  1.882   1.118    0.2691    False                               
                              OOS             35    8           1    3  1.829   1.171    0.2517    False                               
                       SHARPE FULL            34    8           2    4  1.882   2.118   0.06617    False                               
                              IS              34    8           2    3  1.882   1.118    0.2691    False                               
                              OOS             35    8           1    4  1.829   2.171   0.05958    False                               
SECT16            PUB  TOTRET FULL            36   16           2   10  7.111   2.889   0.05304    False                               
                              IS              36   16           2   10  7.111   2.889   0.05304    False                               
                              OOS             36   16           1    9  7.111   1.889    0.1744    False                               
                       SHARPE FULL            36   16           2    7  7.111 -0.1111    0.6592    False                               
                              IS              36   16           2    7  7.111 -0.1111    0.6592    False                               
                              OOS             36   16           1    7  7.111 -0.1111    0.6592    False                               
                  COV  TOTRET FULL            34   14           2    8  5.765   2.235    0.1097    False                               
                              IS              34   14           2    8  5.765   2.235    0.1097    False                               
                              OOS             35   15           1    8  6.429   1.571    0.2299    False                               
                       SHARPE FULL            34   14           2    7  5.765   1.235    0.3008    False                               
                              IS              34   14           2    6  5.765  0.2353    0.5726    False                               
                              OOS             35   15           1    7  6.429  0.5714    0.4794    False                               
BFC12             PUB  TOTRET FULL            36   12           2    0      4      -4         1    False                               
                              IS              36   12           2    0      4      -4         1    False                               
                              OOS             36   12           1    2      4      -2    0.9739    False                               
                       SHARPE FULL            36   12           2    1      4      -3    0.9978    False                               
                              IS              36   12           2    2      4      -2    0.9739    False                               
                              OOS             36   12           1    2      4      -2    0.9739    False                               
                  COV  TOTRET FULL            34   12           2    0  4.235  -4.235         1    False                               
                              IS              34   12           2    0  4.235  -4.235         1    False                               
                              OOS             35   12           1    2  4.114  -2.114    0.9789    False                               
                       SHARPE FULL            34   12           2    1  4.235  -3.235    0.9988    False                               
                              IS              34   12           2    2  4.235  -2.235    0.9834    False                               
                              OOS             35   12           1    2  4.114  -2.114    0.9789    False                               
BSTK100 vs ALLSTK PUB  TOTRET FULL           583  100         225   70  17.15   52.85 3.133e-42     True                size-confounded
                              IS             583  100         225   40  17.15   22.85 1.031e-09     True                size-confounded
                              OOS            583  100         148   53  17.15   35.85  1.04e-20     True                size-confounded
                       SHARPE FULL           583  100         225   74  17.15   56.85  1.13e-48     True                size-confounded
                              IS             583  100         225   54  17.15   36.85 9.678e-22     True                size-confounded
                              OOS            583  100         148   62  17.15   44.85 5.237e-31     True                size-confounded
                  COV  TOTRET FULL           358   91         225   64  23.13   40.87  1.19e-27     True                size-confounded
                              IS             358   91         225   36  23.13   12.87 0.0003886     True                size-confounded
                              OOS            435   97         148   50  21.63   28.37 1.703e-13     True                size-confounded
                       SHARPE FULL           358   91         225   70  23.13   46.87 2.688e-36     True                size-confounded
                              IS             358   91         225   50  23.13   26.87 8.374e-13     True                size-confounded
                              OOS            435   97         148   61  21.63   39.37 2.851e-24     True                size-confounded
SMALL439 screen   PUB  TOTRET FULL           483  439         216  247    399    -152         1    False  the max_1d_move screen itself
                              IS             483  439         216  247    399    -152         1    False  the max_1d_move screen itself
                              OOS            483  439         145  308    399  -91.01         1    False  the max_1d_move screen itself
                       SHARPE FULL           483  439         216  247    399    -152         1    False  the max_1d_move screen itself
                              IS             483  439         216  247    399    -152         1    False  the max_1d_move screen itself
                              OOS            483  439         145  308    399  -91.01         1    False  the max_1d_move screen itself
                  COV  TOTRET FULL           267  247         216  233  228.5   4.502  0.001618     True  the max_1d_move screen itself
                              IS             267  247         216  233  228.5   4.502  0.001618     True  the max_1d_move screen itself
                              OOS            338  308         145  290  280.7   9.337 7.498e-07     True  the max_1d_move screen itself
                       SHARPE FULL           267  247         216  231  228.5   2.502   0.05078    False  the max_1d_move screen itself
                              IS             267  247         216  229  228.5  0.5019    0.4538    False  the max_1d_move screen itself
                              OOS            338  308         145  281  280.7  0.3373    0.5118    False  the max_1d_move screen itself

significant at 0.05, by panel x convention (of 6 metric x window cells each):
                        cells  sig     min_p  mean_excess
panel             conv                                   
BFC12             COV       6    0    0.9789       -3.028
                  PUB       6    0    0.9739       -2.833
BROAD8            COV       6    0   0.05958        1.636
                  PUB       6    0   0.05378        1.722
BSTK100 vs ALLSTK COV       6    6 2.688e-36        32.54
                  PUB       6    6  1.13e-48        41.68
SECT16            COV       6    0    0.1097        1.347
                  PUB       6    0   0.05304        1.222
SMALL439 screen   COV       6    3 7.498e-07        3.614
                  PUB       6    0         1       -131.7
STK20             COV       6    5 0.0001137        4.342
                  PUB       6    4 0.0006475          4.5
STK20 vs ALLSTK   COV       6    4  7.94e-09         5.12
                  PUB       6    5 4.105e-13        5.981

what the convention costs: the same cell under PUB and COV
                                excess           k     obs             p           superset_n    
conv                               COV     PUB COV PUB COV PUB       COV       PUB        COV PUB
panel             metric window                                                                  
BFC12             SHARPE FULL   -3.235      -3  12  12   1   1    0.9988    0.9978         34  36
                         IS     -2.235      -2  12  12   2   2    0.9834    0.9739         34  36
                         OOS    -2.114      -2  12  12   2   2    0.9789    0.9739         35  36
                  TOTRET FULL   -4.235      -4  12  12   0   0         1         1         34  36
                         IS     -4.235      -4  12  12   0   0         1         1         34  36
                         OOS    -2.114      -2  12  12   2   2    0.9789    0.9739         35  36
BROAD8            SHARPE FULL    2.118   2.222   8   8   4   4   0.06617   0.05378         34  36
                         IS      1.118   1.222   8   8   3   3    0.2691    0.2357         34  36
                         OOS     2.171   2.222   8   8   4   4   0.05958   0.05378         35  36
                  TOTRET FULL    2.118   2.222   8   8   4   4   0.06617   0.05378         34  36
                         IS      1.118   1.222   8   8   3   3    0.2691    0.2357         34  36
                         OOS     1.171   1.222   8   8   3   3    0.2517    0.2357         35  36
BSTK100 vs ALLSTK SHARPE FULL    46.87   56.85  91 100  70  74 2.688e-36  1.13e-48        358 583
                         IS      26.87   36.85  91 100  50  54 8.374e-13 9.678e-22        358 583
                         OOS     39.37   44.85  97 100  61  62 2.851e-24 5.237e-31        435 583
                  TOTRET FULL    40.87   52.85  91 100  64  70  1.19e-27 3.133e-42        358 583
                         IS      12.87   22.85  91 100  36  40 0.0003886 1.031e-09        358 583
                         OOS     28.37   35.85  97 100  50  53 1.703e-13  1.04e-20        435 583
SECT16            SHARPE FULL    1.235 -0.1111  14  16   7   7    0.3008    0.6592         34  36
                         IS     0.2353 -0.1111  14  16   6   7    0.5726    0.6592         34  36
                         OOS    0.5714 -0.1111  15  16   7   7    0.4794    0.6592         35  36
                  TOTRET FULL    2.235   2.889  14  16   8  10    0.1097   0.05304         34  36
                         IS      2.235   2.889  14  16   8  10    0.1097   0.05304         34  36
                         OOS     1.571   1.889  15  16   8   9    0.2299    0.1744         35  36
SMALL439 screen   SHARPE FULL    2.502    -152 247 439 231 247   0.05078         1        267 483
                         IS     0.5019    -152 247 439 229 247    0.4538         1        267 483
                         OOS    0.3373  -91.01 308 439 281 308    0.5118         1        338 483
                  TOTRET FULL    4.502    -152 247 439 233 247  0.001618         1        267 483
                         IS      4.502    -152 247 439 233 247  0.001618         1        267 483
                         OOS     9.337  -91.01 308 439 290 308 7.498e-07         1        338 483
STK20             SHARPE FULL    6.124       6  16  20   9  10 0.0001137 0.0006475         89 100
                         IS      2.124       3  16  20   5   7    0.1236   0.06367         89 100
                         OOS     5.278       5  19  20   9   9  0.001933  0.003931         97 100
                  TOTRET FULL    5.124       6  16  20   8  10  0.001094 0.0006475         89 100
                         IS      3.124       3  16  20   6   7   0.03558   0.06367         89 100
                         OOS     4.278       4  19  20   8   8   0.01035   0.01809         97 100
STK20 vs ALLSTK   SHARPE FULL    8.095   9.314  18  20   9  10  7.94e-09 2.512e-11        358 583
                         IS      2.095   2.314  18  20   3   3   0.05418   0.02712        358 583
                         OOS      7.17   7.314  19  20   8   8 1.482e-07 4.012e-08        435 583
                  TOTRET FULL    8.095   10.31  18  20   9  11  7.94e-09 4.105e-13        358 583
                         IS      1.095   1.314  18  20   2   2    0.2269    0.1469        358 583
                         OOS      4.17   5.314  19  20   5   6 0.0007232 2.102e-05        435 583

ETF36: NO offline superset exists (it IS the whole cached ETF list) - UNTESTABLE here, reported as such rather than scored.

reproduction of idea 71's published cell (STK20 vs BSTK100, TOTRET, FULL, PUB):
  overlap 10 of 20 against 4.0 expected, N=100, p = 0.000648   (idea 71 published 10/20 vs 4.0, p 6.5e-4)
  empirical null (200 seeded uniform 20-of-100 draws): mean overlap 3.99 (hypergeometric expectation 4.00), P(overlap >= 10) = 0 vs exact 0.000648; 11 of 100 superset names were not listed at the window start and therefore CANNOT enter the top-20 under PUB

--- PART B: the one pre-registered book on every panel (composite/n10/g0.75/NORM/W) -----------------------------------
  HIND20_IS  (top 20 of BSTK100 by 2009-2016 total return) = NFLX,BKNG,REGN,NVDA,AMZN,SBUX,AAPL,CRM,CI,TJX,HD,CMG,MA,UNH,MU,MO,V,DHR,ISRG,TXN
  HIND20_OOS (top 20 by 2017-2026 total return, LOOK-AHEAD) = NVDA,MU,AMD,LRCX,ANET,KLAC,AVGO,TSLA,LLY,AMAT,PANW,AAPL,CAT,NOW,MSFT,GOOGL,PGR,DE,ETN,VRTX
  STK20 n HIND20_IS = 7/20   STK20 n HIND20_OOS = 8/20
  harness identity |derived - live @10bps| max = 0.000e+00
                 members  CAGR  Sharpe  MaxDD    H1    H2  IS_Sharpe  OOS_CAGR  OOS_Sharpe  OOS_MaxDD  decay     TO    p4a                f4b    p4b
panel      cost                                                                                                                                     
U56        0          55 0.109   1.069 -0.130 1.164 0.995      1.101     0.113       1.049     -0.130  0.052 16.480   True                  -   True
           10         55 0.091   0.908 -0.136 0.993 0.840      0.934     0.094       0.890     -0.136  0.044 16.480   True               CAGR  False
           25         55 0.065   0.665 -0.145 0.736 0.608      0.684     0.066       0.652     -0.145  0.031 16.480  False     H1,H2,OOS,CAGR  False
ETF36      0          36 0.063   0.720 -0.208 0.883 0.590      0.763     0.063       0.692     -0.208  0.071 13.476  False  H1,H2,OOS,DD,CAGR  False
           10         36 0.048   0.570 -0.222 0.725 0.445      0.606     0.048       0.546     -0.222  0.060 13.476  False  H1,H2,OOS,DD,CAGR  False
           25         36 0.027   0.345 -0.244 0.488 0.227      0.370     0.027       0.327     -0.244  0.043 13.476  False  H1,H2,OOS,DD,CAGR  False
STK20      0          20 0.209   1.277 -0.306 1.135 1.415      1.063     0.241       1.458     -0.186 -0.395 11.130  False                 DD  False
           10         20 0.196   1.207 -0.308 1.065 1.344      0.995     0.227       1.386     -0.189 -0.391 11.130  False                 DD  False
           25         20 0.176   1.101 -0.312 0.961 1.237      0.893     0.206       1.278     -0.194 -0.385 11.130  False                 DD  False
B136       0         135 0.093   0.914 -0.176 1.119 0.738      1.065     0.083       0.801     -0.176  0.264 23.827   True        H2,OOS,CAGR  False
           10        135 0.067   0.682 -0.180 0.878 0.513      0.831     0.057       0.570     -0.180  0.261 23.827  False     H1,H2,OOS,CAGR  False
           25        135 0.029   0.333 -0.211 0.515 0.176      0.479     0.018       0.223     -0.211  0.256 23.827  False  H1,H2,OOS,DD,CAGR  False
BSTK100    0         100 0.118   0.912 -0.262 1.113 0.728      1.077     0.099       0.778     -0.262  0.299 21.938  False          H2,OOS,DD  False
           10        100 0.093   0.745 -0.265 0.942 0.564      0.914     0.074       0.607     -0.265  0.307 21.938  False  H1,H2,OOS,DD,CAGR  False
           25        100 0.058   0.493 -0.269 0.686 0.317      0.670     0.039       0.351     -0.269  0.318 21.938  False  H1,H2,OOS,DD,CAGR  False
SMALL439   0         439 0.088   0.705 -0.316 0.895 0.550      0.844     0.080       0.629     -0.316  0.215 28.606   True     H2,OOS,DD,CAGR  False
           10        439 0.057   0.487 -0.346 0.658 0.347      0.623     0.048       0.413     -0.346  0.210 28.606  False  H1,H2,OOS,DD,CAGR  False
           25        439 0.013   0.161 -0.388 0.303 0.042      0.290     0.003       0.089     -0.388  0.201 28.606  False  H1,H2,OOS,DD,CAGR  False
SMALL483   0         483 0.111   0.619 -0.307 0.730 0.618      0.637     0.134       0.642     -0.307 -0.005 28.770   True       H1,H2,OOS,DD  False
           10        483 0.080   0.474 -0.318 0.499 0.503      0.420     0.101       0.514     -0.318 -0.094 28.770  False  H1,H2,OOS,DD,CAGR  False
           25        483 0.034   0.256 -0.401 0.151 0.330      0.096     0.053       0.323     -0.401 -0.227 28.770  False  H1,H2,OOS,DD,CAGR  False
HIND20_IS  0          20 0.209   1.331 -0.290 1.642 0.990      1.546     0.159       1.130     -0.196  0.416 10.583  False                 DD  False
           10         20 0.196   1.261 -0.291 1.578 0.913      1.484     0.146       1.052     -0.202  0.433 10.583  False                 DD  False
           25         20 0.178   1.156 -0.293 1.481 0.799      1.392     0.128       0.934     -0.212  0.458 10.583  False              H2,DD  False
HIND20_OOS 0          20 0.222   1.242 -0.206 1.207 1.278      1.069     0.261       1.375     -0.206 -0.306 11.424   True                 DD  False
           10         20 0.209   1.176 -0.207 1.140 1.213      1.003     0.247       1.309     -0.207 -0.306 11.424  False                 DD  False
           25         20 0.188   1.078 -0.207 1.039 1.116      0.904     0.225       1.211     -0.207 -0.307 11.424  False                 DD  False

controls (RULES v1 weekly @10 bps and SPY, on each parent price panel):
                     CAGR  Sharpe  MaxDD    H1    H2  OOS_CAGR  OOS_Sharpe  OOS_MaxDD
panel      arm                                                                       
U56        RULES v1 0.065   0.664 -0.138 0.641 0.688     0.077       0.747     -0.138
           SPY      0.152   0.889 -0.337 0.957 0.834     0.155       0.882     -0.337
ETF36      RULES v1 0.038   0.465 -0.179 0.619 0.339     0.038       0.443     -0.179
           SPY      0.152   0.889 -0.337 0.957 0.834     0.155       0.882     -0.337
STK20      RULES v1 0.167   1.072 -0.193 1.057 1.091     0.182       1.109     -0.193
           SPY      0.152   0.889 -0.337 0.957 0.834     0.155       0.882     -0.337
B136       RULES v1 0.064   0.635 -0.212 0.756 0.532     0.059       0.576     -0.212
           SPY      0.152   0.889 -0.337 0.957 0.834     0.155       0.882     -0.337
BSTK100    RULES v1 0.085   0.693 -0.211 0.899 0.510     0.065       0.544     -0.211
           SPY      0.152   0.889 -0.337 0.957 0.834     0.155       0.882     -0.337
SMALL439   RULES v1 0.074   0.565 -0.361 0.743 0.404     0.064       0.492     -0.361
           SPY      0.141   0.862 -0.337 0.891 0.858     0.155       0.882     -0.337
SMALL483   RULES v1 0.136   0.523 -0.448 0.539 0.591     0.172       0.554     -0.448
           SPY      0.141   0.862 -0.337 0.891 0.858     0.155       0.882     -0.337
HIND20_IS  RULES v1 0.176   1.156 -0.228 1.544 0.758     0.120       0.858     -0.228
           SPY      0.152   0.889 -0.337 0.957 0.834     0.155       0.882     -0.337
HIND20_OOS RULES v1 0.181   1.043 -0.222 1.157 0.959     0.193       1.035     -0.222
           SPY      0.152   0.889 -0.337 0.957 0.834     0.155       0.882     -0.337

KEEP paths by rung:
      p4a  p4b  n
cost             
0       5    1  9
10      1    0  9
25      0    0  9

every 4b pass:
            CAGR  Sharpe  MaxDD    H1    H2  OOS_Sharpe  OOS_MaxDD     TO
panel cost                                                               
U56   0    0.109   1.069 -0.130 1.164 0.995       1.049     -0.130 16.480

failing 4b bars at the published rung:
f4b
H1,H2,OOS,DD,CAGR    4
DD                   3
CAGR                 1
H1,H2,OOS,CAGR       1

--- does the overlap statistic predict the book? (excess overlap vs performance) ---------------------------------------------
                 exc_FULL    p_FULL  exc_IS      p_IS  exc_OOS     p_OOS  Sharpe  OOS_Sharpe  decay                f4b
panel    metric                                                                                                       
STK20    TOTRET     5.124  0.001094   3.124   0.03558    4.278   0.01035   1.207       1.386 -0.391                 DD
         SHARPE     6.124 0.0001137   2.124    0.1236    5.278  0.001933   1.207       1.386 -0.391                 DD
BSTK100  TOTRET     40.87  1.19e-27   12.87 0.0003886    28.37 1.703e-13  0.7446      0.6074  0.307  H1,H2,OOS,DD,CAGR
         SHARPE     46.87 2.688e-36   26.87 8.374e-13    39.37 2.851e-24  0.7446      0.6074  0.307  H1,H2,OOS,DD,CAGR
SMALL439 TOTRET     4.502  0.001618   4.502  0.001618    9.337 7.498e-07  0.4871      0.4128 0.2097  H1,H2,OOS,DD,CAGR
         SHARPE     2.502   0.05078  0.5019    0.4538   0.3373    0.5118  0.4871      0.4128 0.2097  H1,H2,OOS,DD,CAGR
  [TOTRET] Spearman(excess_OOS, OOS_Sharpe) = -0.500; Spearman(excess_IS, OOS_Sharpe) = -0.500; n = 3 panels (too few to order; reported as a table, not a fit)
  [SHARPE] Spearman(excess_OOS, OOS_Sharpe) = 0.500; Spearman(excess_IS, OOS_Sharpe) = 0.500; n = 3 panels (too few to order; reported as a table, not a fit)

--- PART C: PROTOCOL rule 8 (IS <= 2016-12-31 chooses, OOS >= 2017 read once) ---------------------------------------------
  IS book Sharpe @10 bps: U56 0.934, ETF36 0.606, STK20 0.995, B136 0.831, BSTK100 0.914, SMALL439 0.623, HIND20_IS 1.484
  IS-window overlap p (TOTRET, COV): STK20 0.03558, BSTK100 0.0003886, SMALL439 0.001618   [only the 3 panels with an offline superset are eligible for the overlap selectors]
                                                           picked  CAGR  Sharpe  MaxDD  OOS_CAGR  OOS_Sharpe  OOS_MaxDD    p4a                f4b
selector                                                                                                                                         
ANCHOR (U56, do nothing)                                      U56 0.091   0.908 -0.136     0.094       0.890     -0.136   True               CAGR
IS_SHARPE_PICK                                          HIND20_IS 0.196   1.261 -0.291     0.146       1.052     -0.202  False                 DD
CLEAN_PICK (weakest IS overlap evidence, highest p)         STK20 0.196   1.207 -0.308     0.227       1.386     -0.189  False                 DD
LOADED_PICK (strongest IS overlap evidence, lowest p)     BSTK100 0.093   0.745 -0.265     0.074       0.607     -0.265  False  H1,H2,OOS,DD,CAGR
HIND20_IS (a real ex-ante rule on the same superset)    HIND20_IS 0.196   1.261 -0.291     0.146       1.052     -0.202  False                 DD
HIND20_OOS (look-ahead ceiling, NOT a rule)            HIND20_OOS 0.209   1.176 -0.207     0.247       1.309     -0.207  False                 DD
RULES v1 (U56)                                                  - 0.065   0.664 -0.138     0.077       0.747     -0.138    NaN                  -
SPY                                                             - 0.152   0.889 -0.337     0.155       0.882     -0.337    NaN                  -

--- the number the queue actually asked for: the publishable column --------------------------------------------------------------------------------
                        superset_n    k  unrankable  obs    exp  excess         p                           note
panel             conv                                                                                          
STK20             PUB          100   20          11   10      4       6 0.0006475                               
                  COV           89   16          11    8  2.876   5.124  0.001094                               
STK20 vs ALLSTK   PUB          583   20         225   11 0.6861   10.31 4.105e-13                size-confounded
                  COV          358   18         225    9  0.905   8.095  7.94e-09                size-confounded
BROAD8            PUB           36    8           2    4  1.778   2.222   0.05378                               
                  COV           34    8           2    4  1.882   2.118   0.06617                               
SECT16            PUB           36   16           2   10  7.111   2.889   0.05304                               
                  COV           34   14           2    8  5.765   2.235    0.1097                               
BFC12             PUB           36   12           2    0      4      -4         1                               
                  COV           34   12           2    0  4.235  -4.235         1                               
BSTK100 vs ALLSTK PUB          583  100         225   70  17.15   52.85 3.133e-42                size-confounded
                  COV          358   91         225   64  23.13   40.87  1.19e-27                size-confounded
SMALL439 screen   PUB          483  439         216  247    399    -152         1  the max_1d_move screen itself
                  COV          267  247         216  233  228.5   4.502  0.001618  the max_1d_move screen itself
(ETF36: no offline superset - the column cannot be computed and must be printed as such.)

========================================================================================================================================================================================================
CAVEATS: (i) every superset is itself made of CURRENT constituents, so delisted names are absent from both panel and superset and the overlap counts are LOWER bounds on the true selection; (ii) the two ALLSTK rows pool large caps with sub-$2B names and therefore mix a SIZE effect into the hindsight reading - flagged, not clean; (iii) the hypergeometric null is a uniform k-of-N draw, which no curator performs, so a small p means 'not uniform' and it is the EX-POST ordering of the superset that makes it a hindsight finding; (iv) the small panel is today's sub-$2B screen carried back to 2010 and its own max_1d_move screen is one of the objects under test; (v) 3 panels have an offline superset, so the link between overlap and performance is reported as a table, not fitted.
========================================================================================================================================================================================================
