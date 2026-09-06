```
====================================================================================================
IDEA 71  point-in-time-megacap-panel  (lane B, 2026-09-06)   PANEL-SELECTION BOUND
====================================================================================================
sample 2008-01-02 .. 2026-09-04   B136 cols 136   single stocks BSTK100 100   megacap STK20 20
  PIT market cap: data/ has no shares-outstanding series and prices_broad.csv holds
  CURRENT constituents only -> fallen-out names are ABSENT, not mis-weighted.
  Infrastructure half of idea 71 -> PARK (needs local/Actions data).  This run bounds
  hand-picking WITHIN the survivor set, which is the claim idea 10 actually made.

REPRODUCTION CONTROLS
  check_a  fast_backtest vs engine.backtest : returns 2.08e-17  turnover 6.11e-16
  check_b  panel_score vs baseline.score (all-member) : 0.00e+00
  windows  FULL 4439d  H1 2219d  H2 2220d  IS 2007d (..2016-12-30)  OOS 2432d (2017-01-03..)

REFERENCES (10 bps for the book, SPY is buy-and-hold so cost-free)
  RULESv1  FULL CAGR   6.39% Sharpe 0.6350 MaxDD -21.19% | H1 0.7562 H2 0.5320 | OOS CAGR   5.94% Sharpe 0.5763 MaxDD -21.19%
  SPY      FULL CAGR  15.23% Sharpe 0.8890 MaxDD -33.72% | H1 0.9566 H2 0.8340 | OOS CAGR  15.45% Sharpe 0.8820 MaxDD -33.72%
  4b bars: |MaxDD| <= 0.60x|SPY| -> FULL 20.23%, OOS 20.23%;  CAGR >= 0.70x SPY -> FULL 10.66%, OOS 10.82%

  HIND20 (full-sample top-20 by total return) = NVDA,MU,AMD,NFLX,LRCX,KLAC,AAPL,AMZN,BKNG,AMAT,LLY,REGN,GOOGL,MA,CRM,CMG,MSFT,TJX,ISRG,V
  STK20 n HIND20 = 10 names: AAPL,AMD,AMZN,CRM,GOOGL,LLY,MSFT,NFLX,NVDA,V
  overlap 10/20 against 4.0 expected for a random 20-of-100 draw; hypergeometric P(overlap >= 10) = 6.475e-04
  -> the hand-picked panel is DEMONSTRABLY hindsight-loaded at the membership level,
     independently of anything the backtest says.
  PITGROW20 final-year panel = AAPL,AMD,AMZN,ANET,AVGO,BKNG,INTU,KLAC,LLY,LRCX,MA,MU,NFLX,NOW,NVDA,REGN,SHW,TJX,TSLA,V
  PITGROW20 final n STK20 = 9/20
  check_c  const-panel path vs full-width path on STK20 (all 16 stats x 28 rows) : 3.55e-15

  running 200 RAND20 draws x 14 grid points x 2 rungs ...

----------------------------------------------------------------------------------------------------
1. EVERY GRID POINT, EVERY ARM (10 bps; the 0-bps twin is the last column, idea 261)
----------------------------------------------------------------------------------------------------
arm           n     g conv   turn/yr     CAGR  Sharpe    MaxDD      H1      H2  OOSshp  4a  4b   Shp@0
STK20         5  0.75 NORM     16.36   19.63%  1.1313  -31.16%  1.0136  1.2423  1.2538   .   .  1.2264
STK20         5  0.75 FIXED    15.49   18.59%  1.1531  -19.36%  1.1644  1.1509  1.1696   Y   Y  1.2503
STK20         5  1.00 NORM     21.79   26.14%  1.1290  -40.25%  1.0079  1.2434  1.2549   .   .  1.2239
STK20         5  1.00 FIXED    20.64   24.86%  1.1541  -25.29%  1.1647  1.1526  1.1712   .   .  1.2513
STK20        10  0.75 NORM     11.19   19.51%  1.2054  -31.16%  1.0752  1.3322  1.3736   .   .  1.2759
STK20        10  0.75 FIXED     9.04   17.58%  1.2651  -17.96%  1.2812  1.2573  1.3113   Y   Y  1.3317
STK20        10  1.00 NORM     14.88   26.09%  1.2027  -40.25%  1.0688  1.3334  1.3748   .   .  1.2729
STK20        10  1.00 FIXED    12.05   23.63%  1.2663  -23.50%  1.2819  1.2589  1.3129   .   .  1.3328
STK20        20  0.75 NORM      9.18   19.59%  1.2519  -31.16%  1.1383  1.3673  1.4357   .   .  1.3121
STK20        20  0.75 FIXED     3.50   12.08%  1.3403  -12.11%  1.3485  1.3417  1.4460   Y   Y  1.3800
STK20        20  1.00 NORM     12.15   26.25%  1.2487  -40.25%  1.1313  1.3683  1.4366   .   .  1.3084
STK20        20  1.00 FIXED     4.65   16.23%  1.3407  -15.95%  1.3490  1.3422  1.4465   Y   Y  1.3803
STK20       ALL  0.75 NORM      9.18   19.59%  1.2519  -31.16%  1.1383  1.3673  1.4357   .   .  1.3121
STK20       ALL  1.00 NORM     12.15   26.25%  1.2487  -40.25%  1.1313  1.3683  1.4366   .   .  1.3084
HIND20        5  0.75 NORM     16.88   24.82%  1.3299  -20.96%  1.6199  1.0545  1.1632   Y   .  1.4242
HIND20        5  0.75 FIXED    15.98   21.66%  1.2454  -23.02%  1.5757  0.9404  1.0626   .   .  1.3397
HIND20        5  1.00 NORM     22.47   33.51%  1.3312  -27.36%  1.6215  1.0558  1.1645   .   .  1.4253
HIND20        5  1.00 FIXED    21.29   29.12%  1.2468  -29.89%  1.5770  0.9424  1.0644   .   .  1.3409
HIND20       10  0.75 NORM     11.36   26.10%  1.4569  -22.91%  1.7437  1.1906  1.3096   .   .  1.5240
HIND20       10  0.75 FIXED     9.26   21.32%  1.3528  -20.29%  1.6403  1.0951  1.2345   Y   .  1.4135
HIND20       10  1.00 NORM     15.09   35.44%  1.4583  -29.69%  1.7452  1.1923  1.3111   .   .  1.5251
HIND20       10  1.00 FIXED    12.34   28.79%  1.3542  -26.50%  1.6413  1.0976  1.2366   .   .  1.4148
HIND20       20  0.75 NORM      8.84   26.46%  1.5289  -22.08%  1.7479  1.3215  1.4156   .   .  1.5834
HIND20       20  0.75 FIXED     3.50   15.28%  1.3676  -17.06%  1.5775  1.1878  1.3200   Y   Y  1.3997
HIND20       20  1.00 NORM     11.66   36.01%  1.5299  -28.60%  1.7492  1.3223  1.4162   .   .  1.5838
HIND20       20  1.00 FIXED     4.65   20.57%  1.3677  -22.35%  1.5776  1.1882  1.3202   .   .  1.3996
HIND20      ALL  0.75 NORM      8.84   26.46%  1.5289  -22.08%  1.7479  1.3215  1.4156   .   .  1.5834
HIND20      ALL  1.00 NORM     11.66   36.01%  1.5299  -28.60%  1.7492  1.3223  1.4162   .   .  1.5838
PITGROW20     5  0.75 NORM     17.91   16.13%  0.9703  -39.47%  1.1542  0.8200  0.8670   .   .  1.0761
PITGROW20     5  0.75 FIXED    16.66   15.96%  1.0029  -32.93%  1.2039  0.8398  0.8891   .   .  1.1064
PITGROW20     5  1.00 NORM     23.86   21.35%  0.9719  -49.21%  1.1552  0.8223  0.8693   .   .  1.0776
PITGROW20     5  1.00 FIXED    22.20   21.20%  1.0049  -41.56%  1.2055  0.8424  0.8916   .   .  1.1082
PITGROW20    10  0.75 NORM     12.07   16.37%  1.0438  -40.61%  1.2655  0.8550  0.9472   .   .  1.1206
PITGROW20    10  0.75 FIXED     9.58   15.38%  1.0856  -25.57%  1.2679  0.9305  1.0301   .   .  1.1536
PITGROW20    10  1.00 NORM     16.06   21.78%  1.0448  -50.51%  1.2654  0.8573  0.9491   .   .  1.1214
PITGROW20    10  1.00 FIXED    12.77   20.52%  1.0867  -32.81%  1.2682  0.9326  1.0317   .   .  1.1546
PITGROW20    20  0.75 NORM      9.75   15.37%  1.0315  -39.96%  1.2823  0.8166  0.9124   .   .  1.0966
PITGROW20    20  0.75 FIXED     3.82   10.46%  1.0584  -16.03%  1.2849  0.8661  0.9846   Y   .  1.0970
PITGROW20    20  1.00 NORM     12.91   20.44%  1.0325  -49.76%  1.2818  0.8192  0.9146   .   .  1.0971
PITGROW20    20  1.00 FIXED     5.08   13.96%  1.0590  -20.91%  1.2851  0.8674  0.9856   Y   .  1.0975
PITGROW20   ALL  0.75 NORM      9.75   15.37%  1.0315  -39.96%  1.2823  0.8166  0.9124   .   .  1.0966
PITGROW20   ALL  1.00 NORM     12.91   20.44%  1.0325  -49.76%  1.2818  0.8192  0.9146   .   .  1.0971
BSTK100       5  0.75 NORM     28.39    8.41%  0.6598  -27.51%  0.9122  0.4323  0.4642   .   .  0.8682
BSTK100       5  0.75 FIXED    28.08    8.22%  0.6727  -21.13%  0.9205  0.4524  0.4849   .   .  0.8888
BSTK100       5  1.00 NORM     37.86   10.91%  0.6593  -35.49%  0.9123  0.4317  0.4637   .   .  0.8674
BSTK100       5  1.00 FIXED    37.45   10.72%  0.6733  -27.45%  0.9201  0.4543  0.4867   .   .  0.8891
BSTK100      10  0.75 NORM     21.96    9.44%  0.7522  -26.49%  0.9452  0.5754  0.6183   .   .  0.9197
BSTK100      10  0.75 FIXED    21.50    9.54%  0.8064  -19.42%  1.0162  0.6239  0.6670   Y   .  0.9822
BSTK100      10  1.00 NORM     29.28   12.35%  0.7515  -34.27%  0.9455  0.5742  0.6172   .   .  0.9188
BSTK100      10  1.00 FIXED    28.66   12.57%  0.8072  -25.51%  1.0170  0.6254  0.6684   .   .  0.9827
BSTK100      20  0.75 NORM     16.28   11.12%  0.8770  -27.57%  1.1338  0.6345  0.7126   .   .  1.0029
BSTK100      20  0.75 FIXED    15.57   11.09%  0.9447  -20.33%  1.2412  0.6788  0.7609   Y   .  1.0757
BSTK100      20  1.00 NORM     21.69   14.67%  0.8762  -35.55%  1.1345  0.6326  0.7107   .   .  1.0018
BSTK100      20  1.00 FIXED    20.75   14.73%  0.9454  -26.59%  1.2426  0.6795  0.7613   .   .  1.0760
BSTK100     ALL  0.75 NORM      8.64   12.72%  1.0216  -26.09%  1.1390  0.9049  1.0100   .   .  1.0915
BSTK100     ALL  1.00 NORM     11.40   16.90%  1.0204  -33.78%  1.1401  0.9016  1.0066   .   .  1.0895

KEEP-path census (28 points per named arm = 14 grid x 2 rungs; RAND20 = 200 draws x 28)
  STK20      4a   7/  28   4b   8/  28
  HIND20     4a   4/  28   4b   4/  28
  PITGROW20  4a   3/  28   4b   1/  28
  BSTK100    4a   2/  28   4b   0/  28
  RAND20     4a 1359/5600 (24.3%)   4b 734/5600 (13.1%)   <- NOISE FLOOR
  RAND20 @10bps: 4b base rate 10.1%; draws with >=1 of 14 points passing 4b: 58.0%

----------------------------------------------------------------------------------------------------
2. WHERE STK20 SITS IN THE RAND20 NULL, AND HOW MUCH OF THE HINDSIGHT CEILING IT TAKES
----------------------------------------------------------------------------------------------------
   selection share = (STK20 - RAND20 median) / (HIND20 - RAND20 median)
   1.00 = STK20 is as good as knowing the answer; 0.00 = STK20 is a random 20 of 100
   n     g conv  win     STK20  RANDmed  RANDp90   HIND20   PITGRW  pctile   share
   5  0.75 NORM  FULL   1.1313   0.8261   0.9847   1.3299   0.9703   99.0%    0.61
   5  0.75 NORM  OOS    1.2538   0.7157   0.9359   1.1632   0.8670   99.5%    1.20
   5  0.75 FIXED FULL   1.1531   0.8389   0.9997   1.2454   1.0029  100.0%    0.77
   5  0.75 FIXED OOS    1.1696   0.7404   0.9414   1.0626   0.8891   98.5%    1.33
   5  1.00 NORM  FULL   1.1290   0.8267   0.9846   1.3312   0.9719   99.0%    0.60
   5  1.00 NORM  OOS    1.2549   0.7156   0.9344   1.1645   0.8693   99.5%    1.20
   5  1.00 FIXED FULL   1.1541   0.8403   1.0003   1.2468   1.0049  100.0%    0.77
   5  1.00 FIXED OOS    1.1712   0.7416   0.9405   1.0644   0.8916   98.5%    1.33
  10  0.75 NORM  FULL   1.2054   0.9439   1.0919   1.4569   1.0438   99.0%    0.51
  10  0.75 NORM  OOS    1.3736   0.9254   1.0941   1.3096   0.9472  100.0%    1.17
  10  0.75 FIXED FULL   1.2651   0.9661   1.1135   1.3528   1.0856   99.5%    0.77
  10  0.75 FIXED OOS    1.3113   0.9550   1.1224   1.2345   1.0301  100.0%    1.27
  10  1.00 NORM  FULL   1.2027   0.9445   1.0921   1.4583   1.0448   99.0%    0.50
  10  1.00 NORM  OOS    1.3748   0.9245   1.0934   1.3111   0.9491  100.0%    1.16
  10  1.00 FIXED FULL   1.2663   0.9654   1.1136   1.3542   1.0867   99.5%    0.77
  10  1.00 FIXED OOS    1.3129   0.9545   1.1216   1.2366   1.0317  100.0%    1.27
  20  0.75 NORM  FULL   1.2519   0.9992   1.1453   1.5289   1.0315   98.5%    0.48
  20  0.75 NORM  OOS    1.4357   0.9780   1.1545   1.4156   0.9124  100.0%    1.05
  20  0.75 FIXED FULL   1.3403   1.0246   1.1554   1.3676   1.0584  100.0%    0.92
  20  0.75 FIXED OOS    1.4460   1.0179   1.1712   1.3200   0.9846  100.0%    1.42
  20  1.00 NORM  FULL   1.2487   0.9995   1.1463   1.5299   1.0325   98.5%    0.47
  20  1.00 NORM  OOS    1.4366   0.9773   1.1543   1.4162   0.9146  100.0%    1.05
  20  1.00 FIXED FULL   1.3407   1.0242   1.1556   1.3677   1.0590  100.0%    0.92
  20  1.00 FIXED OOS    1.4465   1.0167   1.1710   1.3202   0.9856  100.0%    1.42
 ALL  0.75 NORM  FULL   1.2519   0.9992   1.1453   1.5289   1.0315   98.5%    0.48
 ALL  0.75 NORM  OOS    1.4357   0.9780   1.1545   1.4156   0.9124  100.0%    1.05
 ALL  1.00 NORM  FULL   1.2487   0.9995   1.1463   1.5299   1.0325   98.5%    0.47
 ALL  1.00 NORM  OOS    1.4366   0.9773   1.1543   1.4162   0.9146  100.0%    1.05
  MEDIAN over the 14 grid points -- FULL: percentile 99.0%, selection share 0.60   OOS: percentile 100.0%, share 1.20
  STK20 beats the RAND20 MEDIAN in 14/14 FULL and 14/14 OOS points;
  clears the RAND20 90th pctile in 14/14 FULL and 14/14 OOS.

----------------------------------------------------------------------------------------------------
3. RULE 8 WALK-FORWARD.  (n, g, conv) chosen on IS <= 2016-12-31 Sharpe @10bps only;
   2017-01-01.. read ONCE.  RAND20's chooser is run per draw and pooled.
----------------------------------------------------------------------------------------------------
arm             pick (n,g,conv)  IS shp |  OOS CAGR  OOS shp  OOS MaxDD  turn/yr  vs SPY  vs base
STK20             10,1.00,FIXED  1.2073 |    25.86%   1.3129    -23.50%    12.05 +0.4308  +0.7366
HIND20             20,1.00,NORM  1.6662 |    32.57%   1.4162    -28.60%    11.66 +0.5342  +0.8400
PITGROW20          20,0.75,NORM  1.1857 |    13.68%   0.9124    -39.96%     9.75 +0.0304  +0.3362
BSTK100           20,1.00,FIXED  1.1790 |    11.64%   0.7613    -26.59%    20.75 -0.1207  +0.1851
RAND20               (per draw)  1.1067 |    13.12%   0.9291    -24.47%    11.45 +0.0471  +0.3528
  RAND20 rule-8 OOS Sharpe distribution: p10 0.6838  med 0.9468  p90 1.1455  max 1.3214
  STK20's rule-8 OOS Sharpe 1.3129 sits at the 99.5% percentile of the 200 random panels.
  4b on the rule-8 pick: STK20 FAIL, HIND20 FAIL, PITGROW20 FAIL, BSTK100 FAIL, RAND20 11.5% of draws.

----------------------------------------------------------------------------------------------------
4. IDEA 10's OWN CONTROL, RE-READ:  STK20 vs BSTK100 at matched (n, g, conv)
----------------------------------------------------------------------------------------------------
  @ 0bps FULL STK20-BSTK100 dSharpe: mean +0.3223 median +0.3498 range +0.2189..+0.3622  wins 14/14
  @ 0bps OOS  STK20-BSTK100 dSharpe: mean +0.5828 median +0.5899 range +0.4124..+0.6726  wins 14/14
  @10bps FULL STK20-BSTK100 dSharpe: mean +0.4087 median +0.4521 range +0.2283..+0.4809  wins 14/14
  @10bps OOS  STK20-BSTK100 dSharpe: mean +0.6733 median +0.6852 range +0.4257..+0.7913  wins 14/14
  @10bps FULL STK20-PITGROW20 dSharpe: mean +0.1952 range +0.1493..+0.2819  wins 14/14
  @10bps OOS  STK20-PITGROW20 dSharpe: mean +0.4114 range +0.2796..+0.5233  wins 14/14
```
