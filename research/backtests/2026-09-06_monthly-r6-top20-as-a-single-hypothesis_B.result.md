# Idea 182 — monthly R6 top-20 as a single pre-registered hypothesis (KEEP-candidate (4b), scoped to u56 — with the stale-signal caveat)

Frozen: R6 / vol20^0.5 scaler, above-200dma & vol20<0.60 gates, top n=20 EW, gross 0.75, MONTHLY. Nothing tuned; 0 free parameters.

```
small panel: dropped 44 tickers with max_1d_move >= 1.0; 439 names + SPY remain
panel u56  :  56 cols, sample 2009-01-13..2026-09-04, IS rows 2007, OOS rows 2432
panel broad: 136 cols, sample 2009-01-13..2026-09-04, IS rows 2007, OOS rows 2432
panel small: 440 cols, sample 2011-01-13..2026-09-04, IS rows 1502, OOS rows 2432

=== reference books (CAGR_F / Sharpe F,H1,H2,OOS / MaxDD_F) ===
  u56   SPY             15.23% | 0.8890 0.9566 0.8340 0.8820 | -33.72%
  u56   RULES v1@ 5bps   7.72% | 0.7797 0.7593 0.8015 0.8627 | -13.71%
  u56   RULES v1@10bps   6.45% | 0.6642 0.6409 0.6878 0.7471 | -13.83%
  u56   RULES v1@25bps   2.75% | 0.3169 0.2849 0.3460 0.3992 | -15.63%
  broad SPY             15.23% | 0.8890 0.9566 0.8340 0.8820 | -33.72%
  broad RULES v1@ 5bps   7.96% | 0.7735 0.8964 0.6696 0.7167 | -19.40%
  broad RULES v1@10bps   6.39% | 0.6350 0.7562 0.5320 0.5763 | -21.19%
  broad RULES v1@25bps   1.79% | 0.2195 0.3350 0.1198 0.1554 | -26.72%
  small SPY             14.13% | 0.8615 0.8907 0.8577 0.8820 | -33.72%
  small RULES v1@ 5bps   9.17% | 0.6762 0.8641 0.5079 0.6007 | -32.69%
  small RULES v1@10bps   7.41% | 0.5647 0.7434 0.4044 0.4923 | -36.12%
  small RULES v1@25bps   2.32% | 0.2302 0.3813 0.0940 0.1673 | -45.43%

=== [F] control: sim(lag=1) must equal engine.backtest exactly ===
  u56   max|dreturns| 1.388e-17   max|dturnover| 0.000e+00
  broad max|dreturns| 1.388e-17   max|dturnover| 0.000e+00
  small max|dreturns| 1.388e-17   max|dturnover| 0.000e+00
  control PASSES on all three panels.

grid: 15 engine runs -> 45 cells (19s)

=== [A] the frozen hypothesis on 3 panels x 3 costs x 5 lag readings (ALL 45 cells) ===
panel   cost      lag   CAGR_F    Sh_F  MaxDD_F      H1      H2   CAGR_O  Sh_OOS   DD_OOS  trn/y  4a 4b 4bO  fails
u56        5   fill-1   13.88%  1.1763  -18.78%  1.2501  1.1211   14.83%  1.1892  -18.78%   4.82  n  Y  Y   -
u56       10   fill-1   13.61%  1.1557  -18.81%  1.2279  1.1017   14.56%  1.1695  -18.81%   4.82  n  Y  Y   -
u56       25   fill-1   12.79%  1.0937  -18.90%  1.1611  1.0435   13.72%  1.1102  -18.90%   4.82  n  Y  Y   -
u56        5   fill-5   13.19%  1.1025  -17.58%  1.1670  1.0568   14.22%  1.1189  -17.58%   4.80  n  Y  Y   -
u56       10   fill-5   12.92%  1.0822  -17.61%  1.1450  1.0378   13.95%  1.0997  -17.61%   4.80  n  Y  Y   -
u56       25   fill-5   12.11%  1.0212  -17.71%  1.0785  0.9807   13.12%  1.0420  -17.71%   4.80  n  Y  Y   -
u56        5   fill-7   13.13%  1.0870  -19.98%  1.1242  1.0643   14.50%  1.1265  -19.98%   4.82  n  Y  Y   -
u56       10   fill-7   12.86%  1.0670  -20.01%  1.1024  1.0455   14.22%  1.1075  -20.01%   4.82  n  Y  Y   -
u56       25   fill-7   12.05%  1.0068  -20.10%  1.0369  0.9892   13.40%  1.0504  -20.10%   4.82  n  Y  Y   -
u56        5  stale-5   13.82%  1.1209  -22.51%  1.2352  1.0464   15.03%  1.1224  -22.51%   4.78  n  n  n   DD
u56       10  stale-5   13.55%  1.1014  -22.52%  1.2131  1.0287   14.76%  1.1045  -22.52%   4.78  n  n  n   DD
u56       25  stale-5   12.74%  1.0428  -22.56%  1.1466  0.9756   13.94%  1.0504  -22.56%   4.78  n  n  n   DD
u56        5  stale-7   14.37%  1.1461  -24.40%  1.2286  1.0987   16.00%  1.1682  -24.40%   4.73  n  n  n   DD
u56       10  stale-7   14.10%  1.1271  -24.41%  1.2069  1.0816   15.73%  1.1507  -24.41%   4.73  n  n  n   DD
u56       25  stale-7   13.30%  1.0699  -24.44%  1.1414  1.0300   14.91%  1.0982  -24.44%   4.73  n  n  n   DD
broad      5   fill-1   16.37%  1.1557  -24.48%  1.2917  1.0566   16.95%  1.1226  -24.48%   7.26  n  n  n   DD
broad     10   fill-1   15.95%  1.1298  -24.51%  1.2636  1.0322   16.51%  1.0976  -24.51%   7.26  n  n  n   DD
broad     25   fill-1   14.70%  1.0517  -24.60%  1.1788  0.9587   15.21%  1.0224  -24.60%   7.26  Y  n  n   DD
broad      5   fill-5   14.62%  1.0322  -23.38%  1.2748  0.8486   13.96%  0.9331  -23.38%   7.23  n  n  n   DD
broad     10   fill-5   14.21%  1.0067  -23.41%  1.2471  0.8245   13.53%  0.9087  -23.41%   7.23  n  n  n   H2,DD
broad     25   fill-5   12.97%  0.9299  -23.51%  1.1635  0.7523   12.27%  0.8354  -23.51%   7.23  Y  n  n   H2,OOS,DD
broad      5   fill-7   14.85%  1.0379  -23.39%  1.2291  0.8970   14.93%  0.9792  -23.39%   7.24  n  n  n   DD
broad     10   fill-7   14.44%  1.0126  -23.42%  1.2016  0.8732   14.50%  0.9550  -23.42%   7.24  n  n  n   DD
broad     25   fill-7   13.20%  0.9363  -23.51%  1.1186  0.8013   13.22%  0.8819  -23.51%   7.24  Y  n  n   H2,OOS,DD
broad      5  stale-5   15.84%  1.1129  -25.48%  1.2603  1.0081   16.70%  1.0926  -25.48%   7.25  n  n  n   DD
broad     10  stale-5   15.42%  1.0874  -25.51%  1.2321  0.9843   16.27%  1.0683  -25.51%   7.25  n  n  n   DD
broad     25  stale-5   14.18%  1.0103  -25.59%  1.1472  0.9126   14.98%  0.9948  -25.59%   7.25  Y  n  n   DD
broad      5  stale-7   15.78%  1.0961  -27.09%  1.3049  0.9451   16.06%  1.0401  -27.09%   7.33  n  n  n   DD
broad     10  stale-7   15.36%  1.0705  -27.12%  1.2765  0.9214   15.63%  1.0161  -27.12%   7.33  n  n  n   DD
broad     25  stale-7   14.09%  0.9934  -27.20%  1.1909  0.8500   14.34%  0.9436  -27.20%   7.33  n  n  n   DD
small      5   fill-1    7.74%  0.5240  -37.75%  0.5781  0.4840    7.64%  0.5027  -37.75%  10.41  n  n  n   H1,H2,OOS,DD,CAGR
small     10   fill-1    7.18%  0.4934  -38.23%  0.5463  0.4542    7.05%  0.4720  -38.23%  10.41  n  n  n   H1,H2,OOS,DD,CAGR
small     25   fill-1    5.52%  0.4014  -39.65%  0.4505  0.3645    5.31%  0.3797  -39.65%  10.41  Y  n  n   H1,H2,OOS,DD,CAGR
small      5   fill-5    7.64%  0.5132  -41.43%  0.7220  0.3476    5.68%  0.3956  -41.43%  10.39  n  n  n   H1,H2,OOS,DD,CAGR
small     10   fill-5    7.08%  0.4830  -41.91%  0.6905  0.3182    5.11%  0.3655  -41.91%  10.39  n  n  n   H1,H2,OOS,DD,CAGR
small     25   fill-5    5.42%  0.3923  -43.31%  0.5957  0.2297    3.40%  0.2751  -43.31%  10.39  Y  n  n   H1,H2,OOS,DD,CAGR
small      5   fill-7    8.72%  0.5703  -40.10%  0.7745  0.4079    6.94%  0.4605  -40.10%  10.43  n  n  n   H1,H2,OOS,DD,CAGR
small     10   fill-7    8.15%  0.5402  -40.59%  0.7434  0.3783    6.36%  0.4304  -40.59%  10.43  n  n  n   H1,H2,OOS,DD,CAGR
small     25   fill-7    6.47%  0.4495  -42.02%  0.6497  0.2894    4.62%  0.3398  -42.02%  10.43  Y  n  n   H1,H2,OOS,DD,CAGR
small      5  stale-5    6.38%  0.4434  -49.13%  0.5511  0.3607    5.05%  0.3619  -49.13%  10.58  n  n  n   H1,H2,OOS,DD,CAGR
small     10  stale-5    5.82%  0.4130  -49.52%  0.5196  0.3309    4.47%  0.3316  -49.52%  10.58  n  n  n   H1,H2,OOS,DD,CAGR
small     25  stale-5    4.16%  0.3217  -50.67%  0.4247  0.2416    2.75%  0.2403  -50.67%  10.58  n  n  n   H1,H2,OOS,DD,CAGR
small      5  stale-7    6.66%  0.4575  -45.44%  0.6055  0.3441    5.77%  0.3975  -45.44%  10.49  n  n  n   H1,H2,OOS,DD,CAGR
small     10  stale-7    6.10%  0.4274  -45.89%  0.5742  0.3147    5.19%  0.3674  -45.89%  10.49  n  n  n   H1,H2,OOS,DD,CAGR
small     25  stale-7    4.45%  0.3370  -47.23%  0.4802  0.2262    3.45%  0.2769  -47.23%  10.49  n  n  n   H1,H2,OOS,DD,CAGR

=== [B] reproduction of idea 173's published u56 @10bps / 1-day cell ===
  CAGR_F     published    0.1361   here    0.1361   diff +2.39e-06
  Sharpe_F   published    1.1557   here    1.1557   diff +2.40e-06
  MaxDD_F    published   -0.1881   here   -0.1881   diff -3.40e-05
  CAGR_OOS   published    0.1456   here    0.1456   diff -3.59e-05
  Sharpe_OOS published    1.1695   here    1.1695   diff +1.92e-05
  reproduced (all |diff| < 0.01): True

=== [C] rule 8 walk-forward — nothing is fitted, so this is the frozen rule on 2017-01-01..2026-09-04 untouched ===
panel   cost      lag |  IS_CAGR   IS_Sh |  OOS_CAGR  OOS_Sh   OOS_DD |  base_Sh  spy_Sh  d_base   d_spy 4bOOS
u56        5   fill-1 |   12.74%  1.1637 |    14.83%  1.1892  -18.78% |   0.8627  0.8820 +0.3265 +0.3072   Y
u56        5   fill-5 |   11.96%  1.0857 |    14.22%  1.1189  -17.58% |   0.8627  0.8820 +0.2562 +0.2369   Y
u56        5   fill-7 |   11.49%  1.0381 |    14.50%  1.1265  -19.98% |   0.8627  0.8820 +0.2638 +0.2445   Y
u56        5  stale-5 |   12.38%  1.1322 |    15.03%  1.1224  -22.51% |   0.8627  0.8820 +0.2597 +0.2404   n
u56        5  stale-7 |   12.42%  1.1284 |    16.00%  1.1682  -24.40% |   0.8627  0.8820 +0.3055 +0.2862   n
u56       10   fill-1 |   12.47%  1.1418 |    14.56%  1.1695  -18.81% |   0.7471  0.8820 +0.4225 +0.2875   Y
u56       10   fill-5 |   11.69%  1.0637 |    13.95%  1.0997  -17.61% |   0.7471  0.8820 +0.3527 +0.2177   Y
u56       10   fill-7 |   11.22%  1.0165 |    14.22%  1.1075  -20.01% |   0.7471  0.8820 +0.3604 +0.2255   Y
u56       10  stale-5 |   12.11%  1.1103 |    14.76%  1.1045  -22.52% |   0.7471  0.8820 +0.3574 +0.2225   n
u56       10  stale-7 |   12.16%  1.1068 |    15.73%  1.1507  -24.41% |   0.7471  0.8820 +0.4037 +0.2687   n
u56       25   fill-1 |   11.67%  1.0759 |    13.72%  1.1102  -18.90% |   0.3992  0.8820 +0.7110 +0.2282   Y
u56       25   fill-5 |   10.89%  0.9976 |    13.12%  1.0420  -17.71% |   0.3992  0.8820 +0.6428 +0.1600   Y
u56       25   fill-7 |   10.43%  0.9516 |    13.40%  1.0504  -20.10% |   0.3992  0.8820 +0.6512 +0.1684   Y
u56       25  stale-5 |   11.31%  1.0443 |    13.94%  1.0504  -22.56% |   0.3992  0.8820 +0.6512 +0.1684   n
u56       25  stale-7 |   11.37%  1.0420 |    14.91%  1.0982  -24.44% |   0.3992  0.8820 +0.6990 +0.2161   n
broad      5   fill-1 |   15.68%  1.2118 |    16.95%  1.1226  -24.48% |   0.7167  0.8820 +0.4059 +0.2406   n
broad      5   fill-5 |   15.43%  1.1841 |    13.96%  0.9331  -23.38% |   0.7167  0.8820 +0.2164 +0.0511   n
broad      5   fill-7 |   14.76%  1.1326 |    14.93%  0.9792  -23.39% |   0.7167  0.8820 +0.2626 +0.0972   n
broad      5  stale-5 |   14.81%  1.1529 |    16.70%  1.0926  -25.48% |   0.7167  0.8820 +0.3760 +0.2106   n
broad      5  stale-7 |   15.44%  1.1904 |    16.06%  1.0401  -27.09% |   0.7167  0.8820 +0.3235 +0.1581   n
broad     10   fill-1 |   15.28%  1.1844 |    16.51%  1.0976  -24.51% |   0.5763  0.8820 +0.5214 +0.2156   n
broad     10   fill-5 |   15.03%  1.1567 |    13.53%  0.9087  -23.41% |   0.5763  0.8820 +0.3325 +0.0267   n
broad     10   fill-7 |   14.36%  1.1055 |    14.50%  0.9550  -23.42% |   0.5763  0.8820 +0.3787 +0.0730   n
broad     10  stale-5 |   14.41%  1.1254 |    16.27%  1.0683  -25.51% |   0.5763  0.8820 +0.4920 +0.1862   n
broad     10  stale-7 |   15.03%  1.1623 |    15.63%  1.0161  -27.12% |   0.5763  0.8820 +0.4398 +0.1341   n
broad     25   fill-1 |   14.08%  1.1016 |    15.21%  1.0224  -24.60% |   0.1554  0.8820 +0.8670 +0.1403   n
broad     25   fill-5 |   13.83%  1.0742 |    12.27%  0.8354  -23.51% |   0.1554  0.8820 +0.6800 -0.0467   n
broad     25   fill-7 |   13.17%  1.0239 |    13.22%  0.8819  -23.51% |   0.1554  0.8820 +0.7265 -0.0001   n
broad     25  stale-5 |   13.22%  1.0423 |    14.98%  0.9948  -25.59% |   0.1554  0.8820 +0.8394 +0.1128   n
broad     25  stale-7 |   13.80%  1.0775 |    14.34%  0.9436  -27.20% |   0.1554  0.8820 +0.7882 +0.0616   n
small      5   fill-1 |    7.90%  0.5665 |     7.64%  0.5027  -37.75% |   0.6007  0.8820 -0.0980 -0.3793   n
small      5   fill-5 |   10.89%  0.7365 |     5.68%  0.3956  -41.43% |   0.6007  0.8820 -0.2051 -0.4864   n
small      5   fill-7 |   11.65%  0.7793 |     6.94%  0.4605  -40.10% |   0.6007  0.8820 -0.1402 -0.4215   n
small      5  stale-5 |    8.57%  0.5976 |     5.05%  0.3619  -49.13% |   0.6007  0.8820 -0.2388 -0.5201   n
small      5  stale-7 |    8.11%  0.5747 |     5.77%  0.3975  -45.44% |   0.6007  0.8820 -0.2032 -0.4845   n
small     10   fill-1 |    7.39%  0.5358 |     7.05%  0.4720  -38.23% |   0.4923  0.8820 -0.0203 -0.4100   n
small     10   fill-5 |   10.36%  0.7059 |     5.11%  0.3655  -41.91% |   0.4923  0.8820 -0.1268 -0.5165   n
small     10   fill-7 |   11.12%  0.7490 |     6.36%  0.4304  -40.59% |   0.4923  0.8820 -0.0619 -0.4516   n
small     10  stale-5 |    8.05%  0.5670 |     4.47%  0.3316  -49.52% |   0.4923  0.8820 -0.1607 -0.5505   n
small     10  stale-7 |    7.60%  0.5444 |     5.19%  0.3674  -45.89% |   0.4923  0.8820 -0.1249 -0.5146   n
small     25   fill-1 |    5.87%  0.4438 |     5.31%  0.3797  -39.65% |   0.1673  0.8820 +0.2123 -0.5024   n
small     25   fill-5 |    8.79%  0.6137 |     3.40%  0.2751  -43.31% |   0.1673  0.8820 +0.1078 -0.6069   n
small     25   fill-7 |    9.53%  0.6576 |     4.62%  0.3398  -42.02% |   0.1673  0.8820 +0.1725 -0.5422   n
small     25  stale-5 |    6.48%  0.4749 |     2.75%  0.2403  -50.67% |   0.1673  0.8820 +0.0730 -0.6417   n
small     25  stale-7 |    6.07%  0.4534 |     3.45%  0.2769  -47.23% |   0.1673  0.8820 +0.1096 -0.6051   n

=== [D] availability diagnostic: IS-window (..2016-12-31) ladders around the frozen point. ALL grid points reported; none is used to select anything. ===
  u56   CADENCE IS Sharpe [D:0.889  W:1.027  M:1.142  Q:1.076]  IS argmax=M  OOS argmax=M  anchor=M (IS rank 1/4)
  u56   COUNT   IS Sharpe [5:1.194  10:1.012  20:1.142  40:1.074  80:1.055]  IS argmax=5  OOS argmax=40  anchor=20 (IS rank 2/5)
  broad CADENCE IS Sharpe [D:0.988  W:1.160  M:1.184  Q:1.144]  IS argmax=M  OOS argmax=M  anchor=M (IS rank 1/4)
  broad COUNT   IS Sharpe [5:1.336  10:1.269  20:1.184  40:1.101  80:1.083]  IS argmax=5  OOS argmax=5  anchor=20 (IS rank 3/5)
  small CADENCE IS Sharpe [D:0.007  W:0.158  M:0.536  Q:0.504]  IS argmax=M  OOS argmax=M  anchor=M (IS rank 1/4)
  small COUNT   IS Sharpe [5:0.357  10:0.466  20:0.536  40:0.540  80:0.667]  IS argmax=80  OOS argmax=20  anchor=20 (IS rank 3/5)

=== [E] idea 53 composition draws: u56 @10bps / 1-day lag, drop 5 and drop 10 names at random, 200 draws each (seed 182) ===
drop    n     4a     4b  4bOOS | Sharpe_F p05/p50/p95 | CAGR_F p50 | MaxDD_F p50/p05 | Sharpe_OOS p05/p50/p95
   5  200   0.0% 100.0% 100.0% | 1.0828/1.1446/1.1806 |  13.19% | -18.26%/-19.28% | 1.0926/1.1774/1.2190
  10  200   0.0%  99.5% 100.0% | 1.0657/1.1391/1.2041 |  12.85% | -17.27%/-18.98% | 1.1043/1.1898/1.2610
 all  400   0.0%  99.8% 100.0%
  4b failure modes among draws: CAGR:1
  published-book Sharpe_F 1.1557 sits at draw percentile 70.5%

=== PRE-REGISTERED VERDICT ===
  [1] published cell reproduces          : True
  [2] u56 4b + 4b-OOS at 5/10/25 bps     : True
  [3a] same under a 1-week delayed FILL  : True
  [3b] same under a 1-week STALE SIGNAL  : False
  [4] >=80% of 400 composition draws 4b  : True  (actual 99.8%)
  Condition [3] was pre-registered as 'the 1-week execution lag' before it was clear the phrase has two readings. Both are reported; [3a] is the literal one (the same decision, filled later) and is what decides the verdict. [3b] is a DIFFERENT risk (signal/compute latency) and is reported as a caveat, not as the bar.
  VERDICT: KEEP-candidate (4b), scoped to u56 — with the stale-signal caveat
  portability (not part of the rule): broad 4b 0%, small 4b 0%

=== the 4b drawdown margin on u56, per lag reading (cap = 0.60 x SPY MaxDD) ===
  cap -20.23%
  fill-1   (t+1, PROTOCOL rule 2            ) MaxDD -18.81%  margin +1.42% (+0.070 of the cap)  Sharpe 1.1557
  fill-5   (1 trading week, delayed fill    ) MaxDD -17.61%  margin +2.62% (+0.129 of the cap)  Sharpe 1.0822
  fill-7   (1 calendar week, delayed fill   ) MaxDD -20.01%  margin +0.22% (+0.011 of the cap)  Sharpe 1.0670
  stale-5  (1 trading week, stale signal    ) MaxDD -22.52%  margin -2.29% (-0.113 of the cap)  Sharpe 1.1014
  stale-7  (1 calendar week, stale signal   ) MaxDD -24.41%  margin -4.18% (-0.206 of the cap)  Sharpe 1.1271

=== [G] the two lag readings differ only in WHERE THE TRADE LANDS, not in how old the information is. Holding the decision-to-fill gap FIXED at 1 bar, slide the whole monthly schedule by 0..7 bars (u56 @10bps). ===
  [G1] identity control: stale(5) == sim(lag=5, phase=-4)  max|dret| 1.388e-17  max|dtrn| 0.000e+00
  phase   CAGR_F  Sharpe_F  MaxDD_F   margin Sharpe_OOS  4b  fails
      0   13.61%    1.1557  -18.81%   +1.42%     1.1695  Y   -
      1   12.64%    1.0631  -20.39%   -0.16%     1.0601  n   DD
      2   12.68%    1.0825  -19.79%   +0.44%     1.0858  Y   -
      3   12.81%    1.0819  -19.59%   +0.64%     1.0923  Y   -
      4   13.24%    1.1214  -19.66%   +0.57%     1.1567  Y   -
      5   12.70%    1.0831  -19.95%   +0.28%     1.0992  Y   -
      6   13.00%    1.1275  -17.88%   +2.35%     1.1910  Y   -
      7   13.80%    1.1628  -19.21%   +1.02%     1.2298  Y   -
  MaxDD across 8 phases of the SAME rule: -20.39% .. -17.88% (range 2.51%); 4b passes 7 of 8. The t+1 margin is +1.42%.
```

## Reading (written after the run; every number above is produced by the script)

1. **This is an independent replication of the cloud lane's KEEP-candidate, and it agrees.**
   Idea 173's published cell reproduces to 3.6e-05 on all five statistics. An independently
   written simulator reproduces `engine.backtest` at t+1 to 1.4e-17 on returns and 0.0 on
   turnover, on all three panels (control [F]). The frozen book (0 free parameters) clears
   4b full-sample and 4b-OOS on u56 at 5, 10 and 25 bps and at t+1 / t+5 / t+7 delayed fill —
   9 of 9 cells, the same 9 the cloud lane published — and in 399 of 400 independent
   composition draws (different seed from theirs). Cost, fill delay and universe composition
   are all priced and none of them is the fragility.

2. **The new result: the two lanes' "1-week lag" arms are the same gap at different calendar
   phases, and the phase is what moves the drawdown.** Control [G1] proves the algebra —
   a 5-bar stale signal traded on the month-end bar IS a 5-bar delayed fill with the whole
   schedule slid back 4 bars (1.4e-17). Holding the decision-to-fill gap fixed at one bar and
   sliding only the trade date, u56 @10 bps gives MaxDD **-17.88% to -20.39% across 8 phases
   of the identical rule** (range 2.51pp), and **4b passes 7 of 8** — phase 1 fails the
   drawdown cap at -20.39%. Across all ten (gap, phase) combinations measured here MaxDD spans
   -17.61% to -24.41%, and 4b's -20.23% cap sits inside that span.

3. **So the margin is smaller than the noise it is measured against.** The published t+1 cell
   clears the drawdown cap by 1.42pp; simply moving the trade to the next trading day costs
   1.58pp and flips the verdict. The KEEP is real under PROTOCOL's own execution convention,
   but it is a 7-of-8 statement about which day of the month you trade, not a margin.

4. **This falsifies clause 7 of the cloud lane's memo as written.** "MONTHLY is a k=1 calendar
   block, so it has exactly one phase" conflates block alignment with schedule anchoring: a
   monthly rule still has ~21 possible trade-date anchors, ideas 187/221 apply to that choice,
   and only one anchor was priced. See the amendment memo (`..._B.memo.md`).

5. **Everything else in the cloud memo stands.** Scope (0/9 broad, 0/9 small), 4a failing
   everywhere, survivorship, and "do not tune it" are all reproduced here. Availability
   diagnostic: MONTHLY is the IS argmax cadence on 3 of 3 panels, but n=20 is the IS argmax
   count on 0 of 3 (u56 would have picked n=5) — the cadence leg of the pick was free, the
   count leg was not.
