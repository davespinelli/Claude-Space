# Idea 898 run log (cloud, 2026-09-15) — stdout of research/backtests/2026-09-15_does-the-TOP20-4b-pass-hold-on-every-rolling-10-year-window_cloud.py

```
load_prices: network unavailable (ModuleNotFoundError); using prices.csv
========================================================================================================
GATES (printed before any hypothesis is read)
========================================================================================================
G1 committed triple  got 12.69% / 1.201 / -17.11%   vs memo 12.69% / 1.201 / -17.11%   -> PASS
G2 full-sample three-leg 4b  h1 True h2 True dd True cagr True -> 4b True   (4a False)   -> PASS
G3 window counts (step 1M) by L {5: 153, 7: 129, 10: 93, 12: 69}  non-increasing True; first window starts 2009-01-13 (sample starts 2009-01-13) -> PASS

========================================================================================================
FULL GRID — three-leg in-window 4b and 4a pass rates over rolling windows
(every (L, step, gross, cost) cell reported; nothing selected)
========================================================================================================
 gross  cost  L  step  n_win  pass4b  pass4a  fail_h1  fail_h2  fail_dd  fail_cagr  degen  pass4b_nd
 0.650    10  5     1    153   0.693   0.000       15       14       28         18      0      0.693
 0.650    10  5     3     51   0.686   0.000        4        5        9          7      0      0.686
 0.650    10  7     1    129   0.930   0.000        8        0        4          3      0      0.930
 0.650    10  7     3     43   0.930   0.000        3        0        1          1      0      0.930
 0.650    10 10     1     93   0.978   0.000        1        0        0          1      0      0.978
 0.650    10 10     3     31   0.968   0.000        1        0        0          0      0      0.968
 0.650    10 12     1     69   0.971   0.000        2        0        0          0      0      0.971
 0.650    10 12     3     23   0.957   0.000        1        0        0          0      0      0.957
 0.650    25  5     1    153   0.627   0.000       24       21       28         27      0      0.627
 0.650    25  5     3     51   0.627   0.000        9        8        9          9      0      0.627
 0.650    25  7     1    129   0.845   0.000       17        0        4          9      0      0.845
 0.650    25  7     3     43   0.814   0.000        7        0        1          3      0      0.814
 0.650    25 10     1     93   0.925   0.000        7        0        0          2      0      0.925
 0.650    25 10     3     31   0.903   0.000        3        0        0          1      0      0.903
 0.650    25 12     1     69   0.971   0.000        2        0        0          0      0      0.971
 0.650    25 12     3     23   0.957   0.000        1        0        0          0      0      0.957
 0.750    10  5     1    153   0.608   0.000       15       14       58          2      0      0.608
 0.750    10  5     3     51   0.608   0.000        4        5       19          1      0      0.608
 0.750    10  7     1    129   0.729   0.000        8        0       34          1      0      0.729
 0.750    10  7     3     43   0.744   0.000        3        0       11          0      0      0.744
 0.750    10 10     1     93   0.860   0.000        1        0       13          0      0      0.860
 0.750    10 10     3     31   0.871   0.000        1        0        4          0      0      0.871
 0.750    10 12     1     69   0.971   0.000        2        0        0          0      0      0.971
 0.750    10 12     3     23   0.957   0.000        1        0        0          0      0      0.957
 0.750    25  5     1    153   0.549   0.000       23       21       58          5      0      0.549
 0.750    25  5     3     51   0.529   0.000        9        8       19          2      0      0.529
 0.750    25  7     1    129   0.698   0.000       17        0       34          2      0      0.698
 0.750    25  7     3     43   0.698   0.000        7        0       11          1      0      0.698
 0.750    25 10     1     93   0.849   0.000        7        0       13          0      0      0.849
 0.750    25 10     3     31   0.839   0.000        3        0        4          0      0      0.839
 0.750    25 12     1     69   0.971   0.000        2        0        0          0      0      0.971
 0.750    25 12     3     23   0.957   0.000        1        0        0          0      0      0.957

========================================================================================================
HEADLINE CELL  L = 10y, step = 1M, gross = 0.65, cost = 10 bps
========================================================================================================
windows 93   three-leg 4b pass 97.8%   4a pass 0.0%
leg failure counts (of 93):  H1 1  H2 0  DD 0  CAGR 1
windows failing EXACTLY one leg, by leg: {'h1': 1, 'h2': 0, 'dd': 0, 'cagr': 1}
     start        end  CAGR  Sharpe  MaxDD    H1    H2  spyCAGR  spySharpe  spyMaxDD  b_h1  b_h2  b_dd  b_cagr    4b    4a
2009-01-13 2018-12-31 0.113   1.139 -0.108 1.168 1.109    0.135      0.854    -0.221  True  True  True    True  True False
2009-02-01 2019-02-01 0.113   1.142 -0.108 1.150 1.134    0.149      0.938    -0.218  True  True  True    True  True False
2009-03-01 2019-03-01 0.115   1.160 -0.108 1.240 1.076    0.166      1.046    -0.193  True  True  True   False False False
2009-04-01 2019-04-01 0.117   1.177 -0.108 1.175 1.180    0.160      1.043    -0.193 False  True  True    True False False
2009-05-01 2019-05-01 0.119   1.197 -0.108 1.148 1.255    0.151      1.008    -0.193  True  True  True    True  True False
2009-06-01 2019-05-31 0.112   1.127 -0.108 1.141 1.113    0.138      0.938    -0.193  True  True  True    True  True False
2009-07-01 2019-07-01 0.116   1.175 -0.108 1.194 1.156    0.147      0.994    -0.193  True  True  True    True  True False
2009-08-01 2019-08-01 0.112   1.148 -0.108 1.085 1.214    0.138      0.949    -0.193  True  True  True    True  True False
2009-09-01 2019-08-30 0.112   1.143 -0.108 1.141 1.146    0.133      0.915    -0.193  True  True  True    True  True False
2009-10-01 2019-10-01 0.109   1.120 -0.108 1.073 1.169    0.130      0.898    -0.193  True  True  True    True  True False
2009-11-01 2019-11-01 0.113   1.168 -0.108 1.123 1.215    0.137      0.945    -0.193  True  True  True    True  True False
2009-12-01 2019-11-29 0.109   1.136 -0.108 1.086 1.188    0.133      0.925    -0.193  True  True  True    True  True False
2010-01-01 2019-12-31 0.110   1.148 -0.108 1.034 1.267    0.135      0.933    -0.193  True  True  True    True  True False
2010-02-01 2020-01-31 0.117   1.219 -0.108 1.128 1.313    0.139      0.959    -0.193  True  True  True    True  True False
2010-03-01 2020-02-28 0.110   1.138 -0.108 1.168 1.109    0.126      0.877    -0.193  True  True  True    True  True False
2010-04-01 2020-04-01 0.101   1.007 -0.171 1.060 0.960    0.099      0.644    -0.337  True  True  True    True  True False
2010-05-01 2020-05-01 0.098   0.981 -0.171 1.031 0.939    0.113      0.707    -0.337  True  True  True    True  True False
2010-06-01 2020-06-01 0.107   1.087 -0.171 1.246 0.955    0.131      0.806    -0.337  True  True  True    True  True False
2010-07-01 2020-07-01 0.114   1.145 -0.171 1.303 1.020    0.139      0.847    -0.337  True  True  True    True  True False
2010-08-01 2020-07-31 0.122   1.203 -0.171 1.345 1.093    0.137      0.840    -0.337  True  True  True    True  True False
2010-09-01 2020-09-01 0.130   1.272 -0.171 1.208 1.333    0.152      0.915    -0.337  True  True  True    True  True False
2010-10-01 2020-10-01 0.123   1.195 -0.171 1.148 1.242    0.137      0.837    -0.337  True  True  True    True  True False
2010-11-01 2020-10-30 0.118   1.134 -0.171 1.156 1.123    0.129      0.794    -0.337  True  True  True    True  True False
2010-12-01 2020-12-01 0.124   1.189 -0.171 1.179 1.206    0.142      0.859    -0.337  True  True  True    True  True False
2011-01-01 2020-12-31 0.122   1.170 -0.171 1.076 1.256    0.138      0.837    -0.337  True  True  True    True  True False
2011-02-01 2021-02-01 0.121   1.158 -0.171 0.904 1.386    0.136      0.826    -0.337  True  True  True    True  True False
2011-03-01 2021-03-01 0.120   1.146 -0.171 0.830 1.425    0.136      0.825    -0.337  True  True  True    True  True False
2011-04-01 2021-04-01 0.119   1.138 -0.171 0.911 1.338    0.139      0.844    -0.337  True  True  True    True  True False
2011-05-01 2021-04-30 0.117   1.121 -0.171 0.848 1.360    0.141      0.850    -0.337  True  True  True    True  True False
2011-06-01 2021-06-01 0.121   1.157 -0.171 0.890 1.387    0.143      0.860    -0.337  True  True  True    True  True False
2011-07-01 2021-07-01 0.124   1.179 -0.171 0.973 1.360    0.148      0.888    -0.337  True  True  True    True  True False
2011-08-01 2021-07-30 0.125   1.192 -0.171 1.032 1.333    0.152      0.912    -0.337  True  True  True    True  True False
2011-09-01 2021-09-01 0.130   1.255 -0.171 1.102 1.391    0.162      0.987    -0.337  True  True  True    True  True False
2011-10-01 2021-10-01 0.131   1.261 -0.171 1.162 1.354    0.167      1.017    -0.337  True  True  True    True  True False
2011-11-01 2021-11-01 0.138   1.321 -0.171 1.115 1.500    0.161      0.999    -0.337  True  True  True    True  True False
2011-12-01 2021-12-01 0.135   1.298 -0.171 1.191 1.399    0.159      0.998    -0.337  True  True  True    True  True False
2012-01-01 2021-12-31 0.138   1.309 -0.171 1.207 1.406    0.165      1.027    -0.337  True  True  True    True  True False
2012-02-01 2022-02-01 0.132   1.255 -0.171 1.243 1.283    0.154      0.966    -0.337  True  True  True    True  True False
2012-03-01 2022-03-01 0.130   1.228 -0.171 1.254 1.225    0.143      0.903    -0.337  True  True  True    True  True False
2012-04-01 2022-04-01 0.131   1.237 -0.171 1.196 1.287    0.146      0.912    -0.337  True  True  True    True  True False
2012-05-01 2022-04-29 0.129   1.227 -0.171 1.281 1.208    0.136      0.854    -0.337  True  True  True    True  True False
2012-06-01 2022-06-01 0.135   1.276 -0.171 1.429 1.183    0.142      0.880    -0.337  True  True  True    True  True False
2012-07-01 2022-07-01 0.130   1.232 -0.171 1.352 1.163    0.130      0.811    -0.337  True  True  True    True  True False
2012-08-01 2022-08-01 0.130   1.231 -0.171 1.406 1.118    0.137      0.847    -0.337  True  True  True    True  True False
2012-09-01 2022-09-01 0.127   1.208 -0.171 1.394 1.085    0.130      0.808    -0.337  True  True  True    True  True False
2012-10-01 2022-09-30 0.122   1.167 -0.171 1.356 1.041    0.116      0.730    -0.337  True  True  True    True  True False
2012-11-01 2022-11-01 0.126   1.202 -0.171 1.488 1.000    0.126      0.778    -0.337  True  True  True    True  True False
2012-12-01 2022-12-01 0.127   1.209 -0.171 1.519 0.992    0.132      0.804    -0.337  True  True  True    True  True False
2013-01-01 2022-12-30 0.124   1.181 -0.171 1.501 0.958    0.125      0.763    -0.337  True  True  True    True  True False
2013-02-01 2023-02-01 0.124   1.179 -0.171 1.555 0.913    0.127      0.774    -0.337  True  True  True    True  True False
2013-03-01 2023-03-01 0.120   1.147 -0.171 1.481 0.895    0.121      0.743    -0.337  True  True  True    True  True False
2013-04-01 2023-03-31 0.119   1.134 -0.171 1.367 0.953    0.121      0.743    -0.337  True  True  True    True  True False
2013-05-01 2023-05-01 0.118   1.131 -0.171 1.348 0.959    0.121      0.741    -0.337  True  True  True    True  True False
2013-06-01 2023-06-01 0.120   1.144 -0.171 1.332 0.999    0.120      0.736    -0.337  True  True  True    True  True False
2013-07-01 2023-06-30 0.124   1.179 -0.171 1.387 1.019    0.128      0.775    -0.337  True  True  True    True  True False
2013-08-01 2023-08-01 0.123   1.172 -0.171 1.336 1.049    0.125      0.763    -0.337  True  True  True    True  True False
2013-09-01 2023-09-01 0.124   1.175 -0.171 1.455 0.963    0.127      0.774    -0.337  True  True  True    True  True False
2013-10-01 2023-09-29 0.115   1.096 -0.171 1.401 0.864    0.118      0.727    -0.337  True  True  True    True  True False
2013-11-01 2023-11-01 0.113   1.075 -0.171 1.191 0.985    0.112      0.694    -0.337  True  True  True    True  True False
2013-12-01 2023-12-01 0.116   1.103 -0.171 1.232 1.002    0.118      0.724    -0.337  True  True  True    True  True False
2014-01-01 2023-12-29 0.118   1.117 -0.171 1.091 1.145    0.119      0.732    -0.337  True  True  True    True  True False
2014-02-01 2024-02-01 0.123   1.163 -0.171 1.139 1.189    0.127      0.769    -0.337  True  True  True    True  True False
2014-03-01 2024-03-01 0.126   1.184 -0.171 1.076 1.283    0.127      0.770    -0.337  True  True  True    True  True False
2014-04-01 2024-04-01 0.130   1.212 -0.171 1.167 1.259    0.128      0.778    -0.337  True  True  True    True  True False
2014-05-01 2024-05-01 0.126   1.180 -0.171 1.255 1.132    0.123      0.749    -0.337  True  True  True    True  True False
2014-06-01 2024-05-31 0.128   1.194 -0.171 1.113 1.271    0.126      0.766    -0.337  True  True  True    True  True False
2014-07-01 2024-07-01 0.128   1.199 -0.171 1.148 1.252    0.128      0.775    -0.337  True  True  True    True  True False
2014-08-01 2024-08-01 0.128   1.187 -0.171 1.213 1.178    0.129      0.779    -0.337  True  True  True    True  True False
2014-09-01 2024-08-30 0.127   1.176 -0.171 1.147 1.211    0.129      0.776    -0.337  True  True  True    True  True False
2014-10-01 2024-10-01 0.130   1.204 -0.171 1.173 1.241    0.132      0.790    -0.337  True  True  True    True  True False
2014-11-01 2024-11-01 0.130   1.206 -0.171 1.205 1.220    0.130      0.781    -0.337  True  True  True    True  True False
2014-12-01 2024-11-29 0.133   1.228 -0.171 1.192 1.271    0.133      0.795    -0.337  True  True  True    True  True False
2015-01-01 2024-12-31 0.132   1.218 -0.171 1.267 1.195    0.130      0.783    -0.337  True  True  True    True  True False
2015-02-01 2025-01-31 0.136   1.248 -0.171 1.347 1.189    0.137      0.816    -0.337  True  True  True    True  True False
2015-03-01 2025-02-28 0.129   1.189 -0.171 1.115 1.260    0.129      0.777    -0.337  True  True  True    True  True False
2015-04-01 2025-04-01 0.125   1.154 -0.171 0.965 1.338    0.125      0.754    -0.337  True  True  True    True  True False
2015-05-01 2025-05-01 0.124   1.129 -0.171 0.976 1.273    0.123      0.727    -0.337  True  True  True    True  True False
2015-06-01 2025-05-30 0.123   1.119 -0.171 0.940 1.287    0.128      0.748    -0.337  True  True  True    True  True False
2015-07-01 2025-07-01 0.125   1.140 -0.171 0.981 1.293    0.136      0.787    -0.337  True  True  True    True  True False
2015-08-01 2025-08-01 0.124   1.134 -0.171 1.075 1.191    0.134      0.779    -0.337  True  True  True    True  True False
2015-09-01 2025-08-29 0.130   1.189 -0.171 1.273 1.106    0.145      0.839    -0.337  True  True  True    True  True False
2015-10-01 2025-10-01 0.137   1.250 -0.171 1.221 1.280    0.153      0.878    -0.337  True  True  True    True  True False
2015-11-01 2025-10-31 0.138   1.249 -0.171 1.134 1.370    0.146      0.844    -0.337  True  True  True    True  True False
2015-12-01 2025-12-01 0.136   1.222 -0.171 1.208 1.237    0.145      0.839    -0.337  True  True  True    True  True False
2016-01-01 2025-12-31 0.137   1.237 -0.171 1.253 1.220    0.148      0.855    -0.337  True  True  True    True  True False
2016-02-01 2026-01-30 0.144   1.304 -0.171 1.371 1.236    0.155      0.895    -0.337  True  True  True    True  True False
2016-03-01 2026-02-27 0.146   1.313 -0.171 1.400 1.221    0.154      0.892    -0.337  True  True  True    True  True False
2016-04-01 2026-04-01 0.141   1.275 -0.171 1.323 1.224    0.142      0.830    -0.337  True  True  True    True  True False
2016-05-01 2026-05-01 0.147   1.319 -0.171 1.366 1.269    0.152      0.880    -0.337  True  True  True    True  True False
2016-06-01 2026-06-01 0.149   1.336 -0.171 1.376 1.294    0.156      0.900    -0.337  True  True  True    True  True False
2016-07-01 2026-07-01 0.143   1.280 -0.171 1.355 1.202    0.154      0.890    -0.337  True  True  True    True  True False
2016-08-01 2026-07-31 0.141   1.268 -0.171 1.333 1.199    0.150      0.870    -0.337  True  True  True    True  True False
2016-09-01 2026-09-01 0.144   1.289 -0.171 1.388 1.184    0.152      0.880    -0.337  True  True  True    True  True False

H_START: 2 failing windows in 1 contiguous block(s) of start months; first failing start 2009-03-01, last 2009-04-01

========================================================================================================
PROTOCOL rule 8 walk-forward (selector declared before the run, OOS read once)
========================================================================================================
IS  L=5y  windows ending <= 2016-12-31: n=37  4b pass 37.8%
IS  L=7y  windows ending <= 2016-12-31: n=13  4b pass 76.9%
IS-PICK -> L = 7y (highest IS 4b pass rate, ties to the larger L)
OOS windows starting >= 2017-01-01 at L=7y: n=33  three-leg 4b pass 100.0%  4a pass 0.0%
  leg failures: H1 0  H2 0  DD 0  CAGR 0

OOS window 2017-01-01..2026-09-14 — the book's own triple, read once:
           BOOK B* (top20, g=0.65, M)  RULES v2 (live, W)     SPY
CAGR                           0.1438              0.0946  0.1527
Sharpe                         1.2814              1.2772  0.8740
MaxDD                         -0.1711             -0.1205 -0.3372
H1 Sharpe                      1.4469              1.4098  0.9802
H2 Sharpe                      1.1039              1.1318  0.7593
OOS three-leg 4b True  (h1 True h2 True dd True cagr True);  OOS 4a False

========================================================================================================
FULL SAMPLE — the one window every committed verdict on this book is read on
========================================================================================================
           BOOK B*  RULES v2 (live)     SPY
CAGR        0.1269           0.0862  0.1513
Sharpe      1.2012           1.2013  0.8845
MaxDD      -0.1711          -0.1205 -0.3372
H1 Sharpe   1.2146           1.2322  0.9588
H2 Sharpe   1.1972           1.1770  0.8236

========================================================================================================
HYPOTHESES
========================================================================================================
H_ROBUST (>= 80% of 10y windows clear three-leg 4b): 97.8% -> SUPPORTED
H_LEG (one leg carries the failures): exactly-one-leg failures {'h1': 1, 'h2': 0, 'dd': 0, 'cagr': 1} -> see counts
H_START (failures form ONE contiguous block of starts): 1 block(s) -> SUPPORTED

turnover / yr at the headline cell: 3.76x

SURVIVORSHIP: universe.json is the current constituent list; every level above is optimistic and the rolling pass rate is an UPPER bound.
```
