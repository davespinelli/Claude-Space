# Idea 539 — does-the-c_sd-RESIDUAL-LAW-hold-on-a-CADENCE-and-GROSS-grid (lane B, 2026-09-11)

**G1 reproduction PASS** — the (gross 0.75, cad W/M/Q) subgrid reproduces idea 301's committed decomposition and idea 535's CSD.is fit (const -0.0209, slope -1.5722, t -6.32, n 162).

## The headline: the slope at every gross (cadences W/M/Q, idea 535's exact population)

```
         n   const   slope     se       t     R2  slope_over_gross    lo95    hi95
gross                                                                             
0.50   162 -0.0081 -1.0264 0.1624 -6.3223 0.1999           -2.0529 -1.3446 -0.7082
0.75   162 -0.0209 -1.5722 0.2489 -6.3168 0.1996           -2.0963 -2.0601 -1.0844
1.00   162 -0.0405 -2.1435 0.3399 -6.3059 0.1991           -2.1435 -2.8098 -1.4773
```

- **B1 SLOPE INVARIANCE IN GROSS: FAIL** — beta(0.75) = -1.5722 [-2.0601, -1.0844]; beta(0.50) = -1.0264 OUTSIDE; beta(1.00) = -2.1435 OUTSIDE.
- **B2 PURE SCALE: PASS** — beta(0.50)/beta(0.75) = 0.6528 vs g/0.75 = 0.6667; beta(1.00)/beta(0.75) = 1.3634 vs g/0.75 = 1.3333.
- **B3 CADENCE (daily): FAIL**.
- **B4 idea 535's RETIREMENT: FAIL** at 6 of 9 (gross, cadence-set) points.

## G2 — the queue's premise ('c_sd is the one input that gross scales directly')

```
       expected_if_SCALES    n  med_ratio_IS   min_IS   max_IS  med_ratio_OOS  max_abs_dev_from_1
gross                                                                                            
0.50             0.666667  216      0.999389 0.664632 1.007419       0.999698            0.335368
0.75             1.000000  216      1.000000 1.000000 1.000000       1.000000            0.000000
1.00             1.333333  216      1.000826 0.993282 1.340220       1.000499            0.340220
```

G2-SCALES FAIL / G2-INVARIANT FAIL.

## All 12 (gross, cadence) slopes

```
                             n   const   slope     se       t     R2  slope_over_gross    lo95    hi95
gross cadset                                                                                          
0.50  WMQ(535 population)  162 -0.0081 -1.0264 0.1624 -6.3223 0.1999           -2.0529 -1.3446 -0.7082
      WMQD(all)            216 -0.0033 -1.1828 0.1437 -8.2293 0.2404           -2.3657 -1.4646 -0.9011
      W                     54  0.0099 -1.7167 0.3214 -5.3410 0.3542           -3.4335 -2.3467 -1.0867
      M                     54 -0.0303 -0.1177 0.2750 -0.4279 0.0035           -0.2353 -0.6566  0.4213
      Q                     54 -0.0060 -1.2044 0.1927 -6.2497 0.4289           -2.4088 -1.5821 -0.8267
      D                     54  0.0115 -1.6732 0.3000 -5.5767 0.3742           -3.3465 -2.2613 -1.0852
0.75  WMQ(535 population)  162 -0.0209 -1.5722 0.2489 -6.3168 0.1996           -2.0963 -2.0601 -1.0844
      WMQD(all)            216 -0.0110 -1.8039 0.2200 -8.1982 0.2390           -2.4052 -2.2352 -1.3726
      W                     54  0.0128 -2.5970 0.4944 -5.2524 0.3466           -3.4627 -3.5661 -1.6279
      M                     54 -0.0612 -0.1766 0.4209 -0.4194 0.0034           -0.2354 -1.0016  0.6485
      Q                     54 -0.0183 -1.8714 0.2979 -6.2819 0.4315           -2.4952 -2.4553 -1.2875
      D                     54  0.0183 -2.5197 0.4603 -5.4743 0.3656           -3.3596 -3.4219 -1.6176
1.00  WMQ(535 population)  162 -0.0405 -2.1435 0.3399 -6.3059 0.1991           -2.1435 -2.8098 -1.4773
      WMQD(all)            216 -0.0233 -2.4479 0.3000 -8.1594 0.2373           -2.4479 -3.0359 -1.8599
      W                     54  0.0143 -3.4911 0.6763 -5.1621 0.3388           -3.4911 -4.8166 -2.1656
      M                     54 -0.1043 -0.2385 0.5746 -0.4152 0.0033           -0.2385 -1.3648  0.8877
      Q                     54 -0.0380 -2.5878 0.4110 -6.2972 0.4327           -2.5878 -3.3933 -1.7824
      D                     54  0.0260 -3.3707 0.6276 -5.3711 0.3568           -3.3707 -4.6007 -2.1407
```

## B4 — estimator ladder (fitted IS, scored once OOS)

```
              MAE_CSD_ALL  MAE_FAM_ALL  ratio  MAE_CSD_MA  MAE_FAM_MA    B1a    B1b  RETIRES
gross cadset                                                                                
0.50  D            0.0927       0.0754 1.2297      0.1788      0.1486  False  False    False
      WMQ          0.1162       0.1260 0.9219      0.2184      0.2367   True   True     True
      WMQD         0.1051       0.1117 0.9409      0.1986      0.2096   True   True     True
0.75  D            0.1411       0.1129 1.2492      0.2711      0.2223  False  False    False
      WMQ          0.1773       0.1937 0.9153      0.3226      0.3521   True   True     True
      WMQD         0.1611       0.1726 0.9335      0.2952      0.3132   True   True     True
1.00  D            0.1906       0.1500 1.2710      0.3651      0.2951  False  False    False
      WMQ          0.2414       0.2661 0.9074      0.4243      0.4672   True   True     True
      WMQD         0.2204       0.2381 0.9260      0.3912      0.4172   True   True     True
```

## WF-A (rule 8): (level, cadence, gross) chosen on IS Sharpe, OOS read once

```
                             pick_level pick_cad  pick_gross  is_Sharpe  oCAGR  oSharpe  oMaxDD  spy_oCAGR  spy_oSharpe  spy_oMaxDD  live_oSharpe  live_oCAGR  beats_SPY_oos  beats_LIVE_oos    p4a    p4b                f4b
panel    family    con                                                                                                                                                                                                       
B136     MA-THRESH DEGROSS      -0.2500        Q      0.7500     1.2156 0.1358   1.1384 -0.2416     0.1545       0.8820     -0.3372        1.2851      0.0953           True           False  False  False                 DD
                   RESPREAD      0.2000        Q      1.0000     1.4596 0.2799   1.0693 -0.3776     0.1545       0.8820     -0.3372        1.2851      0.0953           True           False  False  False                 DD
         QUANTILE  DEGROSS       0.9000        M      1.0000     1.1725 0.1638   1.1065 -0.2866     0.1545       0.8820     -0.3372        1.2851      0.0953           True           False  False  False                 DD
                   RESPREAD      0.9000        M      1.0000     1.1729 0.1818   1.1051 -0.3146     0.1545       0.8820     -0.3372        1.2851      0.0953           True           False  False  False                 DD
SMALL439 MA-THRESH DEGROSS      -0.4000        Q      0.5000     0.7417 0.0557   0.5957 -0.2172     0.1545       0.8820     -0.3372        1.2851      0.0953          False           False  False  False  H1,H2,OOS,DD,CAGR
                   RESPREAD      0.3000        M      1.0000     0.8934 0.3190   1.1019 -0.4044     0.1545       0.8820     -0.3372        1.2851      0.0953           True           False  False  False                 DD
         QUANTILE  DEGROSS       0.8000        Q      0.5000     0.7305 0.0524   0.6279 -0.1884     0.1545       0.8820     -0.3372        1.2851      0.0953          False           False  False  False     H1,H2,OOS,CAGR
                   RESPREAD      0.9500        Q      0.5000     0.7288 0.0700   0.6480 -0.2259     0.1545       0.8820     -0.3372        1.2851      0.0953          False           False  False  False  H1,H2,OOS,DD,CAGR
U56      MA-THRESH DEGROSS       0.3000        Q      1.0000     1.2403 0.0139   0.5678 -0.0447     0.1524       0.8721     -0.3372        1.2747      0.0945          False           False  False  False        H2,OOS,CAGR
                   RESPREAD      0.2000        Q      1.0000     1.4098 0.2780   0.9421 -0.4065     0.1524       0.8721     -0.3372        1.2747      0.0945           True           False  False  False                 DD
         QUANTILE  DEGROSS       0.5000        M      1.0000     1.2624 0.1069   1.2178 -0.1357     0.1524       0.8721     -0.3372        1.2747      0.0945           True           False  False  False               CAGR
                   RESPREAD      0.5000        M      1.0000     1.2699 0.2144   1.2180 -0.2569     0.1524       0.8721     -0.3372        1.2747      0.0945           True           False  False  False                 DD
```

WF-A picks beat SPY OOS 8/12, RULES v2 0/12.  4a 0/1296 books, 4b 46/1296 books.

## WF-C — is the law actionable?

```
                n  share_DEGROSS  hit_rate   PICK  ALWAYS_RS  ALWAYS_DG  ORACLE  PICK_minus_best_fixed  share_of_oracle_gap
gross cadset                                                                                                               
0.50  WMQ     162         0.0000    1.0000 0.9372     0.9372     0.9048  0.9428                 0.0000               0.0000
      WMQD    216         0.0000    1.0000 0.9086     0.9086     0.8915  0.9225                 0.0000               0.0000
0.75  WMQ     162         0.0000    1.0000 0.9350     0.9350     0.9036  0.9410                 0.0000               0.0000
      WMQD    216         0.0000    1.0000 0.9072     0.9072     0.8907  0.9213                 0.0000               0.0000
1.00  WMQ     162         0.0000    1.0000 0.9322     0.9322     0.9020  0.9387                 0.0000               0.0000
      WMQD    216         0.0000    1.0000 0.9052     0.9052     0.8896  0.9197                 0.0000               0.0000
```

SURVIVORSHIP: SMALL439/U56/B136 are current constituents only (no delistings); CAGR levels and the 4a/4b columns are inflated.  The residual is an arm-minus-arm contrast on the same names, days and gross, so the bias very largely cancels out of it.

## ADDENDUM — descriptive splits (NOT pre-registered bars)

Re-derivable from the committed `.decomp.csv` / `.slope.csv` by
`2026-09-11_does-the-c_sd-RESIDUAL-LAW-hold-on-a-CADENCE-and-GROSS-grid_B_addendum.py`.

```
========================================================================================================================
Idea 539 ADDENDUM - descriptive splits (NOT pre-registered bars)
========================================================================================================================

A. G2 BY FAMILY: r_g = c_sd(gross=g) / c_sd(gross=0.75), per cell
                   n  c_sd_at_075  med_ratio  max_abs_dev_from_1  expected_if_SCALES  INVARIANT_at_0p05  SCALES_at_0p10
family    gross                                                                                                        
MA-THRESH 0.50   108     0.121338   1.000000            0.010382            0.666667               True           False
          0.75   108     0.121338   1.000000            0.000000            1.000000               True            True
          1.00   108     0.121338   1.000000            0.011394            1.333333               True           False
QUANTILE  0.50   108     0.004736   0.861593            0.335368            0.666667              False           False
          0.75   108     0.004736   1.000000            0.000000            1.000000               True            True
          1.00   108     0.004736   1.169756            0.340220            1.333333              False           False

  READING: the MA-THRESH family -- the one that carries the whole residual (mean c_sd
  0.1213) -- is INVARIANT in gross to 1.1e-02 at both off-grosses, exactly as the
  construction c_t = k_t/n_t says.  The QUANTILE family -- whose c_t is near-constant by
  construction (mean c_sd 0.0047) and whose resid0 is ~0 by identity -- moves toward the
  queue's g/0.75 without reaching it (median 0.862 vs 0.667, 1.170 vs 1.333).  The main
  run's joint G2 failure is therefore entirely a QUANTILE artefact: the queue's premise
  is FALSE where the residual lives and only PARTLY true where c_sd is negligible.

========================================================================================================================
B. beta/gross WITHIN each cadence (from the main run's .slope.csv)
gross                   0.5    0.75     1.0   span  rel_span
cadset                                                      
D                   -3.3465 -3.3596 -3.3707 0.0242    0.0072
M                   -0.2353 -0.2354 -0.2385 0.0032    0.0137
Q                   -2.4088 -2.4952 -2.5878 0.1791    0.0717
W                   -3.4335 -3.4627 -3.4911 0.0576    0.0166
WMQ(535 population) -2.0529 -2.0963 -2.1435 0.0907    0.0432

  READING: gross-normalisation holds INSIDE every cadence (relative span 0.7%-7.2%),
  but the cadences themselves are 15x apart: MONTHLY has essentially NO c_sd slope
  (beta/gross -0.235, t -0.42, R2 0.003) while W/D sit at -3.43/-3.35 and Q at -2.50.
  The pooled -1.5722 is an average over a population that is not homogeneous in the
  dial the queue asked about.

========================================================================================================================
C. WHY WF-C CHANGED NO DECISION
  OOS cells with a POSITIVE 0-bps gap (DEGROSS CAGR > RESPREAD CAGR): 0 of 648
  max gap0_pp over all OOS cells: -0.0739 pp/yr   median -4.3954   min -33.4037
  The sign the predictor is asked for is CONSTANT over the whole population, so any
  estimator with a negative fitted mean picks RESPREAD everywhere and scores exactly
  ALWAYS_RESPREAD.  WF-C's hit rate of 1.0000 is that identity, not skill.
```

## One-paragraph answer

**The -1.5722 slope is NOT invariant — it is a SCALE number, and the gross-normalised slope
beta/gross is the invariant the record should publish.** B1 fails at both off-grosses
(beta 0.50 = -1.0264, beta 1.00 = -2.1435, both outside beta(0.75)'s 95% CI [-2.0601, -1.0844]),
but B2 passes cleanly: the ratios 0.6528 and 1.3634 sit within 0.014 and 0.030 of g/0.75, so
beta/gross = -2.0529 / -2.0963 / -2.1435 (a 4.3% span). **The queue's stated reason is wrong:**
c_sd is NOT scaled by gross — inside MA-THRESH, which carries the entire residual, c_sd is
gross-invariant to 1.1e-02, exactly as c_t = k_t/n_t predicts. The gross-dependence is
entirely on the OUTCOME side. **Cadence is the bigger domain limit:** the pooled WMQ law
averages a 15x spread (beta/gross W -3.43, D -3.35, Q -2.50, M -0.235 with t -0.42 and
R2 0.003 — MONTHLY carries no c_sd slope at all), and the daily slope sits outside the WMQ CI
at all three grosses. Idea 535's retirement of the family label survives at every gross on
{W,M,Q} and {W,M,Q,D} (6 of 9 points) but **inverts on the daily-only cells**, where CSD.is is
23-27% WORSE than the FAMILY constant. And the law changes no decision: the OOS 0-bps gap is
negative in **648 of 648** cells, so the predictor picks RESPREAD everywhere and scores
exactly ALWAYS_RESPREAD. **No KEEP** — 4a 0/1296, 4b 46/1296 books, and the 12 WF-A picks
carry 4a 0/12, 4b 0/12, beat RULES v2 OOS 0/12, beat SPY OOS 8/12.
