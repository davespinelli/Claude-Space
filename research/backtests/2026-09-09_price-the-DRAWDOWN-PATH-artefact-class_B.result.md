====================================================================================================
IDEA 321 - price the DRAWDOWN-PATH artefact class (lane B, 2026-09-09)
====================================================================================================
load_prices: network unavailable (ModuleNotFoundError); using prices.csv
panel U56        4700 days x   56 names  2008-01-02 .. 2026-09-08
load_prices: network unavailable (ModuleNotFoundError); using prices.csv
panel B136       4699 days x  136 names  2008-01-02 .. 2026-09-04
panel SMALL484   4194 days x  484 names  2010-01-04 .. 2026-09-04

--- G1  fast_backtest vs engine.backtest (4 real books) ---
  v2 band 0.03 W         max|diff| = 8.674e-18
  band 0.00 g1.00 W      max|diff| = 2.082e-17
  mom n5 g0.75 M         max|diff| = 6.939e-18
  band 0.10 g0.50 M      max|diff| = 6.939e-18
  G1 PASS (bar 1e-12, worst 2.082e-17)

--- building the 126-book grid ---
  126 books built

--- G2  episode identity  /  G3  disjoint 2nd-worst ---
  G2 max|episode-max - MaxDD| = 0.000e+00  PASS (bar exactly 0.0)
  G3 worst and 2nd-worst episodes disjoint on every book: PASS

====================================================================================================
PART 1  REBUILD - every grid point (full table committed to .grid.csv)
====================================================================================================
  126 books x 5 windows written to 2026-09-09_price-the-DRAWDOWN-PATH-artefact-class_B.grid.csv

  worst-episode CONTRIBUTION c = |MaxDD| - |DD2|, in pp, by panel (full sample):
    U56       books: median   3.61  IQR [ 2.01,  5.39]  max  10.79   |  SPY c =   9.22 pp (MaxDD -33.72% in 2020, DD2 -24.50%)
    B136      books: median   5.07  IQR [ 3.66,  7.07]  max  12.93   |  SPY c =   9.22 pp (MaxDD -33.72% in 2020, DD2 -24.50%)
    SMALL484  books: median   5.92  IQR [ 1.14, 12.20]  max  46.40   |  SPY c =   9.22 pp (MaxDD -33.72% in 2020, DD2 -24.50%)

  POOLED median contribution c = 4.95 pp  <- the scale everything is read against

  4b DD margin |0.60*SPY_MaxDD| - |MaxDD| (pp, full sample), by panel:
    U56       median    6.22  pass 38/42  |margin| < c on 16/42
    B136      median    4.17  pass 31/42  |margin| < c on 19/42
    SMALL484  median   -0.71  pass 20/42  |margin| < c on 14/42

====================================================================================================
H_FLIP  - does the 4b DD verdict change when BOTH arms are read on their 2nd-worst episode?
====================================================================================================
  full   DD-pass  89/126   2nd-worst-episode pass  93/126   VERDICT FLIPS  18/126 = 14.3%   |margin| < c on 38.9%
  H1     DD-pass  90/126   2nd-worst-episode pass  84/126   VERDICT FLIPS  10/126 = 7.9%   |margin| < c on 26.2%
  H2     DD-pass  92/126   2nd-worst-episode pass 101/126   VERDICT FLIPS  17/126 = 13.5%   |margin| < c on 41.3%
  IS     DD-pass  90/126   2nd-worst-episode pass  84/126   VERDICT FLIPS  10/126 = 7.9%   |margin| < c on 26.2%
  OOS    DD-pass  89/126   2nd-worst-episode pass  96/126   VERDICT FLIPS  21/126 = 16.7%   |margin| < c on 43.7%

  H_FLIP (FAILS): full-sample flip rate 14.3% vs a 25% bar

====================================================================================================
H_SAME  - is one calendar episode setting every book's MaxDD?
====================================================================================================
  U56       full  modal worst-episode year 2020  on 100% of books ({2020: np.int64(42)})   SPY's own: 2020
  U56       IS    modal worst-episode year 2011  on 57% of books ({2011: np.int64(24), 2010: np.int64(10), 2016: np.int64(5)})   SPY's own: 2009
  U56       OOS   modal worst-episode year 2020  on 100% of books ({2020: np.int64(42)})   SPY's own: 2020
  B136      full  modal worst-episode year 2020  on 86% of books ({2020: np.int64(36), 2023: np.int64(6)})   SPY's own: 2020
  B136      IS    modal worst-episode year 2011  on 50% of books ({2011: np.int64(21), 2010: np.int64(15), 2014: np.int64(3)})   SPY's own: 2009
  B136      OOS   modal worst-episode year 2020  on 86% of books ({2020: np.int64(36), 2023: np.int64(6)})   SPY's own: 2020
  SMALL484  full  modal worst-episode year 2020  on 79% of books ({2020: np.int64(33), 2025: np.int64(9)})   SPY's own: 2020
  SMALL484  IS    modal worst-episode year 2012  on 57% of books ({2012: np.int64(24), 2011: np.int64(15), 2016: np.int64(3)})   SPY's own: 2011
  SMALL484  OOS   modal worst-episode year 2020  on 79% of books ({2020: np.int64(33), 2025: np.int64(9)})   SPY's own: 2020

  H_SAME (FAILS): min panel concentration 79% vs an 80% bar

====================================================================================================
PART 3  - IS->OOS stability of each drawdown statistic, and the swap test
====================================================================================================
  Spearman rank correlation across books, IS(<=2016) vs OOS(2017-):
    MaxDD    U56 +0.906   B136 +0.915   SMALL484 +0.881   mean +0.901
    DD2      U56 +0.943   B136 +0.805   SMALL484 +0.843   mean +0.864
    Ulcer    U56 +0.914   B136 +0.822   SMALL484 +0.835   mean +0.857
    TUW      U56 +0.156   B136 +0.167   SMALL484 +0.174   mean +0.166
    Sharpe   U56 +0.667   B136 +0.633   SMALL484 +0.294   mean +0.531
    CAGR     U56 +0.928   B136 +0.925   SMALL484 +0.735   mean +0.863

  H_STAB (FAILS): MaxDD mean +0.901 vs Ulcer +0.857 / TUW +0.166

  SWAP: same 0.60 cap, different statistic (full sample):
    MaxDD -> ulcpass   pass  54/126  verdict changes  35/126 = 27.8%
    MaxDD -> tuwpass   pass   0/126  verdict changes  89/126 = 70.6%
    MaxDD -> ddpass2   pass  93/126  verdict changes  18/126 = 14.3%
  H_SWAP (HOLDS): Ulcer swap changes 27.8% vs a 20% bar

  Which 4b leg BINDS (full sample, each book vs its panel's SPY):
    U56       n= 42  fail H1   3  H2   6  OOS   6  DD   4  CAGR  26  -> 4b PASS  11
    B136      n= 42  fail H1   9  H2  15  OOS  15  DD  11  CAGR  30  -> 4b PASS   5
    SMALL484  n= 42  fail H1  42  H2  42  OOS  42  DD  22  CAGR  38  -> 4b PASS   0
    full 4b verdict with the Ulcer cap instead: changes 12/126 = 9.5%

====================================================================================================
PART 2  CENSUS - the record's own published 4b DD margins
====================================================================================================
  112,266 paired (book MaxDD, SPY MaxDD) rows in 259 committed CSVs (259 distinct files)
  published 4b DD-cap verdicts: PASS 43,653 (38.9%)  FAIL 68,613
  |margin| distribution (pp): median 6.56  p25 2.79  p75 10.75  max 76.4
    |margin| <  4.95 pp (rebuilt MEDIAN contribution ):  39.2% of rows, touching 245 files
    |margin| <  1.00 pp (1.00 pp                     ):   8.7% of rows, touching 207 files
    |margin| <  2.00 pp (2.00 pp                     ):  18.4% of rows, touching 224 files
    |margin| <  5.00 pp (5.00 pp                     ):  39.5% of rows, touching 245 files
  FILE-CLUSTERED (one median |margin| per file, n=259): share below the rebuilt median contribution 39.8%, below 1 pp 0.0%, median 5.81 pp
  H_REC (FAILS): file-clustered share below c 39.8% vs a 50% bar

====================================================================================================
PART 4  rule-8 walk-forward (2 tuned params: band b, gross g) + both KEEP paths
====================================================================================================
  U56       MaxDD cap   -> band 0.10 gross 1.00  OOS CAGR  12.37% Sharpe  1.216 MaxDD -16.10%  | SPY OOS 15.38%/0.879/-33.72%
  U56       Ulcer cap   -> band 0.10 gross 0.50  OOS CAGR   6.13% Sharpe  1.217 MaxDD  -8.21%  | SPY OOS 15.38%/0.879/-33.72%
  U56       no DD gate  -> band 0.10 gross 1.00  OOS CAGR  12.37% Sharpe  1.216 MaxDD -16.10%  | SPY OOS 15.38%/0.879/-33.72%
  B136      MaxDD cap   -> band 0.10 gross 1.00  OOS CAGR  11.27% Sharpe  1.110 MaxDD -19.14%  | SPY OOS 15.45%/0.882/-33.72%
  B136      Ulcer cap   -> band 0.10 gross 0.75  OOS CAGR   8.44% Sharpe  1.111 MaxDD -14.53%  | SPY OOS 15.45%/0.882/-33.72%
  B136      no DD gate  -> band 0.10 gross 1.00  OOS CAGR  11.27% Sharpe  1.110 MaxDD -19.14%  | SPY OOS 15.45%/0.882/-33.72%
  SMALL484  MaxDD cap   -> band 0.10 gross 0.75  OOS CAGR   4.90% Sharpe  0.693 MaxDD -15.14%  | SPY OOS 15.45%/0.882/-33.72%
  SMALL484  Ulcer cap    no eligible book IS
  SMALL484  no DD gate  -> band 0.10 gross 1.00  OOS CAGR   6.46% Sharpe  0.692 MaxDD -19.78%  | SPY OOS 15.45%/0.882/-33.72%

  RULES v2 (live baseline) on the same windows:
    U56       full  8.64%/1.204/-12.05%  H1 1.231 H2 1.183  OOS  9.51%/1.282/-12.05%
    SPY       full 15.19%/0.887/-33.72%  H1 0.959 H2 0.829  OOS 15.38%/0.879/-33.72%
    B136      full  8.03%/1.106/-12.24%  H1 1.229 H2 0.984  OOS  7.98%/1.119/-12.24%
    SPY       full 15.23%/0.889/-33.72%  H1 0.957 H2 0.834  OOS 15.45%/0.882/-33.72%
    SMALL484  full  4.07%/0.615/-12.09%  H1 0.542 H2 0.680  OOS  4.55%/0.663/-12.09%
    SPY       full 14.13%/0.862/-33.72%  H1 0.891 H2 0.858  OOS 15.45%/0.882/-33.72%

  BOTH KEEP PATHS on all 126 books:
    U56       4a   2/42   4b  11/42   BOTH   0/42
    B136      4a   4/42   4b   5/42   BOTH   0/42
    SMALL484  4a   4/42   4b   0/42   BOTH   0/42
    TOTAL     4a 10/126   4b 16/126   BOTH 0/126

  The rule-8 picks judged on both KEEP paths (OOS read once):
    U56       MaxDD cap   band 0.10/g 1.00  4a False  4b True  (OOS Sharpe 1.216 vs v2 1.282 vs SPY 0.879; DD margin +4.13 pp, own contribution 3.15 pp)
    U56       Ulcer cap   band 0.10/g 0.50  4a False  4b False  (OOS Sharpe 1.217 vs v2 1.282 vs SPY 0.879; DD margin +12.02 pp, own contribution 1.57 pp)
    U56       no DD gate  band 0.10/g 1.00  4a False  4b True  (OOS Sharpe 1.216 vs v2 1.282 vs SPY 0.879; DD margin +4.13 pp, own contribution 3.15 pp)
    B136      MaxDD cap   band 0.10/g 1.00  4a False  4b True  (OOS Sharpe 1.110 vs v2 1.119 vs SPY 0.882; DD margin +1.09 pp, own contribution 6.57 pp)
    B136      Ulcer cap   band 0.10/g 0.75  4a False  4b False  (OOS Sharpe 1.111 vs v2 1.119 vs SPY 0.882; DD margin +5.70 pp, own contribution 5.02 pp)
    B136      no DD gate  band 0.10/g 1.00  4a False  4b True  (OOS Sharpe 1.110 vs v2 1.119 vs SPY 0.882; DD margin +1.09 pp, own contribution 6.57 pp)
    SMALL484  MaxDD cap   band 0.10/g 0.75  4a False  4b False  (OOS Sharpe 0.693 vs v2 0.663 vs SPY 0.882; DD margin +5.09 pp, own contribution 4.05 pp)
    SMALL484  no DD gate  band 0.10/g 1.00  4a False  4b False  (OOS Sharpe 0.692 vs v2 0.663 vs SPY 0.882; DD margin +0.45 pp, own contribution 5.10 pp)

====================================================================================================
PART 5  idea 311's standing proposal - 17-point gross ladder on every 4b passer the
        rule-8 chooser lands on, plus the DD margin along the ladder
====================================================================================================
  U56 band 0.10 weekly, gross 0.20 -> 1.00 in 17 steps:
    g=0.200  CAGR  2.34% Sh 1.188 DD  -3.32%  OOS  2.44%/1.217  DDmargin +16.91 pp (own c  0.63)  4b fail:CAGR      4a False
    g=0.250  CAGR  2.93% Sh 1.188 DD  -4.15%  OOS  3.05%/1.217  DDmargin +16.08 pp (own c  0.78)  4b fail:CAGR      4a False
    g=0.300  CAGR  3.51% Sh 1.188 DD  -4.97%  OOS  3.66%/1.217  DDmargin +15.26 pp (own c  0.94)  4b fail:CAGR      4a False
    g=0.350  CAGR  4.10% Sh 1.188 DD  -5.78%  OOS  4.28%/1.217  DDmargin +14.45 pp (own c  1.10)  4b fail:CAGR      4a False
    g=0.400  CAGR  4.69% Sh 1.188 DD  -6.60%  OOS  4.90%/1.217  DDmargin +13.64 pp (own c  1.26)  4b fail:CAGR      4a False
    g=0.450  CAGR  5.29% Sh 1.188 DD  -7.40%  OOS  5.51%/1.217  DDmargin +12.83 pp (own c  1.41)  4b fail:CAGR      4a False
    g=0.500  CAGR  5.88% Sh 1.188 DD  -8.21%  OOS  6.13%/1.217  DDmargin +12.02 pp (own c  1.57)  4b fail:CAGR      4a False
    g=0.550  CAGR  6.47% Sh 1.188 DD  -9.01%  OOS  6.75%/1.217  DDmargin +11.22 pp (own c  1.73)  4b fail:CAGR      4a False
    g=0.600  CAGR  7.07% Sh 1.188 DD  -9.81%  OOS  7.37%/1.217  DDmargin +10.42 pp (own c  1.89)  4b fail:CAGR      4a False
    g=0.650  CAGR  7.66% Sh 1.188 DD -10.61%  OOS  7.99%/1.217  DDmargin  +9.62 pp (own c  2.05)  4b fail:CAGR      4a False
    g=0.700  CAGR  8.26% Sh 1.188 DD -11.40%  OOS  8.62%/1.217  DDmargin  +8.83 pp (own c  2.20)  4b fail:CAGR      4a False
    g=0.750  CAGR  8.85% Sh 1.188 DD -12.19%  OOS  9.24%/1.216  DDmargin  +8.04 pp (own c  2.36)  4b fail:CAGR      4a False
    g=0.800  CAGR  9.45% Sh 1.188 DD -12.98%  OOS  9.86%/1.216  DDmargin  +7.25 pp (own c  2.52)  4b fail:CAGR      4a False
    g=0.850  CAGR 10.05% Sh 1.188 DD -13.77%  OOS 10.49%/1.216  DDmargin  +6.47 pp (own c  2.68)  4b fail:CAGR      4a False
    g=0.900  CAGR 10.65% Sh 1.188 DD -14.55%  OOS 11.11%/1.216  DDmargin  +5.69 pp (own c  2.83)  4b PASS           4a False
    g=0.950  CAGR 11.24% Sh 1.187 DD -15.32%  OOS 11.74%/1.216  DDmargin  +4.91 pp (own c  2.99)  4b PASS           4a False
    g=1.000  CAGR 11.84% Sh 1.187 DD -16.10%  OOS 12.37%/1.216  DDmargin  +4.13 pp (own c  3.15)  4b PASS           4a False
    -> 4b admissible band: 3/17 points [0.900, 1.000] contiguous=True
  B136 band 0.10 weekly, gross 0.20 -> 1.00 in 17 steps:
    g=0.200  CAGR  2.31% Sh 1.128 DD  -3.98%  OOS  2.24%/1.114  DDmargin +16.25 pp (own c  1.40)  4b fail:CAGR      4a True
    g=0.250  CAGR  2.89% Sh 1.128 DD  -4.96%  OOS  2.80%/1.113  DDmargin +15.27 pp (own c  1.74)  4b fail:CAGR      4a True
    g=0.300  CAGR  3.47% Sh 1.128 DD  -5.94%  OOS  3.36%/1.113  DDmargin +14.29 pp (own c  2.08)  4b fail:CAGR      4a True
    g=0.350  CAGR  4.05% Sh 1.128 DD  -6.92%  OOS  3.92%/1.113  DDmargin +13.31 pp (own c  2.41)  4b fail:CAGR      4a True
    g=0.400  CAGR  4.64% Sh 1.128 DD  -7.88%  OOS  4.49%/1.113  DDmargin +12.34 pp (own c  2.75)  4b fail:CAGR      4a True
    g=0.450  CAGR  5.22% Sh 1.128 DD  -8.85%  OOS  5.05%/1.112  DDmargin +11.38 pp (own c  3.08)  4b fail:CAGR      4a True
    g=0.500  CAGR  5.80% Sh 1.128 DD  -9.81%  OOS  5.61%/1.112  DDmargin +10.42 pp (own c  3.41)  4b fail:CAGR      4a True
    g=0.550  CAGR  6.39% Sh 1.128 DD -10.76%  OOS  6.18%/1.112  DDmargin  +9.47 pp (own c  3.74)  4b fail:CAGR      4a True
    g=0.600  CAGR  6.97% Sh 1.128 DD -11.71%  OOS  6.74%/1.112  DDmargin  +8.52 pp (own c  4.06)  4b fail:CAGR      4a True
    g=0.650  CAGR  7.56% Sh 1.128 DD -12.66%  OOS  7.31%/1.111  DDmargin  +7.57 pp (own c  4.39)  4b fail:CAGR      4a False
    g=0.700  CAGR  8.14% Sh 1.128 DD -13.60%  OOS  7.87%/1.111  DDmargin  +6.63 pp (own c  4.70)  4b fail:CAGR      4a False
    g=0.750  CAGR  8.73% Sh 1.128 DD -14.53%  OOS  8.44%/1.111  DDmargin  +5.70 pp (own c  5.02)  4b fail:CAGR      4a False
    g=0.800  CAGR  9.32% Sh 1.128 DD -15.46%  OOS  9.00%/1.111  DDmargin  +4.77 pp (own c  5.34)  4b fail:CAGR      4a False
    g=0.850  CAGR  9.91% Sh 1.128 DD -16.39%  OOS  9.57%/1.110  DDmargin  +3.84 pp (own c  5.65)  4b fail:CAGR      4a False
    g=0.900  CAGR 10.50% Sh 1.128 DD -17.31%  OOS 10.14%/1.110  DDmargin  +2.92 pp (own c  5.96)  4b fail:CAGR      4a False
    g=0.950  CAGR 11.08% Sh 1.128 DD -18.23%  OOS 10.70%/1.110  DDmargin  +2.00 pp (own c  6.26)  4b PASS           4a False
    g=1.000  CAGR 11.67% Sh 1.128 DD -19.14%  OOS 11.27%/1.110  DDmargin  +1.09 pp (own c  6.57)  4b PASS           4a False
    -> 4b admissible band: 2/17 points [0.950, 1.000] contiguous=True
  SMALL484 band 0.10 weekly, gross 0.20 -> 1.00 in 17 steps:
    g=0.200  CAGR  1.25% Sh 0.669 DD  -4.22%  OOS  1.34%/0.695  DDmargin +16.01 pp (own c  1.22)  4b fail:H1,H2,OOS,CAGR 4a True
    g=0.250  CAGR  1.56% Sh 0.668 DD  -5.25%  OOS  1.67%/0.694  DDmargin +14.98 pp (own c  1.51)  4b fail:H1,H2,OOS,CAGR 4a True
    g=0.300  CAGR  1.87% Sh 0.668 DD  -6.28%  OOS  2.00%/0.694  DDmargin +13.95 pp (own c  1.79)  4b fail:H1,H2,OOS,CAGR 4a True
    g=0.350  CAGR  2.18% Sh 0.668 DD  -7.29%  OOS  2.33%/0.694  DDmargin +12.94 pp (own c  2.07)  4b fail:H1,H2,OOS,CAGR 4a True
    g=0.400  CAGR  2.49% Sh 0.668 DD  -8.30%  OOS  2.66%/0.694  DDmargin +11.93 pp (own c  2.34)  4b fail:H1,H2,OOS,CAGR 4a True
    g=0.450  CAGR  2.79% Sh 0.668 DD  -9.30%  OOS  2.98%/0.694  DDmargin +10.93 pp (own c  2.60)  4b fail:H1,H2,OOS,CAGR 4a True
    g=0.500  CAGR  3.09% Sh 0.668 DD -10.30%  OOS  3.31%/0.694  DDmargin  +9.93 pp (own c  2.85)  4b fail:H1,H2,OOS,CAGR 4a True
    g=0.550  CAGR  3.39% Sh 0.668 DD -11.28%  OOS  3.63%/0.693  DDmargin  +8.95 pp (own c  3.11)  4b fail:H1,H2,OOS,CAGR 4a True
    g=0.600  CAGR  3.70% Sh 0.668 DD -12.26%  OOS  3.95%/0.693  DDmargin  +7.97 pp (own c  3.35)  4b fail:H1,H2,OOS,CAGR 4a False
    g=0.650  CAGR  3.99% Sh 0.668 DD -13.22%  OOS  4.27%/0.693  DDmargin  +7.01 pp (own c  3.59)  4b fail:H1,H2,OOS,CAGR 4a False
    g=0.700  CAGR  4.29% Sh 0.668 DD -14.19%  OOS  4.59%/0.693  DDmargin  +6.05 pp (own c  3.82)  4b fail:H1,H2,OOS,CAGR 4a False
    g=0.750  CAGR  4.59% Sh 0.668 DD -15.14%  OOS  4.90%/0.693  DDmargin  +5.09 pp (own c  4.05)  4b fail:H1,H2,OOS,CAGR 4a False
    g=0.800  CAGR  4.88% Sh 0.668 DD -16.08%  OOS  5.22%/0.693  DDmargin  +4.15 pp (own c  4.27)  4b fail:H1,H2,OOS,CAGR 4a False
    g=0.850  CAGR  5.17% Sh 0.668 DD -17.02%  OOS  5.53%/0.692  DDmargin  +3.21 pp (own c  4.48)  4b fail:H1,H2,OOS,CAGR 4a False
    g=0.900  CAGR  5.46% Sh 0.668 DD -17.95%  OOS  5.84%/0.692  DDmargin  +2.28 pp (own c  4.69)  4b fail:H1,H2,OOS,CAGR 4a False
    g=0.950  CAGR  5.75% Sh 0.668 DD -18.87%  OOS  6.15%/0.692  DDmargin  +1.36 pp (own c  4.90)  4b fail:H1,H2,OOS,CAGR 4a False
    g=1.000  CAGR  6.04% Sh 0.668 DD -19.78%  OOS  6.46%/0.692  DDmargin  +0.45 pp (own c  5.10)  4b fail:H1,H2,OOS,CAGR 4a False
    -> 4b admissible band: 0/17 points (none)

====================================================================================================
PRE-REGISTERED HYPOTHESES
====================================================================================================
  G1 PASS   G2 PASS   G3 PASS
  H_FLIP  FAILS   (14.3% vs 25%)
  H_SAME  FAILS   (79% vs 80%)
  H_STAB  FAILS
  H_SWAP  HOLDS
