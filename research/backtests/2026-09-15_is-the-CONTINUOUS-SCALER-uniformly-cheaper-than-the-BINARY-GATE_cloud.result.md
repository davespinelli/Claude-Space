# Idea 902 run log (cloud, 2026-09-15) — stdout of research/backtests/2026-09-15_is-the-CONTINUOUS-SCALER-uniformly-cheaper-than-the-BINARY-GATE_cloud.py

```
load_prices: network unavailable (ModuleNotFoundError); using prices.csv
================================================================================================================
GATES (printed before any hypothesis is read)
================================================================================================================
G2 never-firing multiplier == ungated base   max|dr| = 0.000e+00   [PASS]
G5 fast Sharpe == engine.metrics Sharpe      |d|     = 0.000e+00   [PASS]
G1 idea 870 VTCONT-HI arm (U56 q.17 w252 d.50 W g1.00, UNMATCHED): 13.66% / 1.098 / -18.79%  gate turnover 0.71/yr  vs memo 13.66% / 1.098 / -18.79% @ 0.71   [PASS]
   CORR-HI binary, same cell: gate turnover 2.15/yr vs memo 2.16   [PASS]   (12.91% / 1.098 / -16.55%)
G3 matched mean multiplier exact           max|d| = 6.661e-16   [PASS]
G4 BINARY and RAMP share their firing set  cells with a mismatch: 0 of 432   [PASS]
   cells built 432; matched 132; unmatchable 300; matched arms 1584; unmatched (as-published) rows 1296

================================================================================================================
WHY 300-ODD CELLS CANNOT BE MATCHED — the sample the matched contrast is read on
================================================================================================================
reason                             form 
rescale drives multiplier below 0  RAMP     268
                                   RATIO     32

unmatchable cells by depth and side (a binary gate at depth d removes d of the gross on its firing days; a continuous scaler that de-grosses much less needs alpha >> 1 to match it, which drives its deepest day below zero):
state       CORR  NAMEVOL  PORTVOL
depth side                        
0.25  HI       0        6        6
0.50  HI      24       24       24
      LO      24       24       24
1.00  HI      24       24       24
      LO      24       24       24
alpha required on the 'below 0' cells: median 2.60, max 8.04

The matched contrast below is therefore read on the SHALLOW end of the depth axis only. That is a real restriction on the answer and is stated, not hidden: at depths where a continuous scaler CAN be made to hold the same average gross as the binary gate, it does not do so more cheaply.  At the deeper end it cannot be matched at all.

================================================================================================================
AS-PUBLISHED (UNMATCHED) READING — what idea 870's 0.71-vs-2.16 comparison actually is
(same cell, no rescale; this is the reading the queue's premise rests on)
================================================================================================================
                     n  gt_cheaper  med_d_gt  med_d_gbar
form  state   side                                      
RAMP  CORR    HI    72      1.0000   -0.8422      0.0287
              LO    72      1.0000   -1.9069      0.0488
      NAMEVOL HI    72      1.0000   -0.6883      0.0325
              LO    72      1.0000   -1.1550      0.0532
      PORTVOL HI    72      1.0000   -0.6639      0.0283
              LO    72      1.0000   -1.4127      0.0494
RATIO CORR    HI    72      1.0000   -1.1969      0.0378
              LO    72      1.0000   -1.5212      0.0444
      NAMEVOL HI    72      1.0000   -0.9644      0.0406
              LO    72      1.0000   -2.0761      0.0728
      PORTVOL HI    72      1.0000   -0.6898      0.0315
              LO    72      1.0000   -1.8630      0.0586

d_gbar > 0 means the continuous form HOLDS MORE GROSS than the binary gate it is being compared with — i.e. it de-grosses less.  An overlay that barely moves is trivially low-turnover; that is the whole of the unmatched turnover gap.

================================================================================================================
MATCHED-GROSS CONTRAST — CONT minus BINARY, paired within every cell
(pairing keys: base, state, side, q, w, depth, cadence, gross; nothing selected)
================================================================================================================
max |mean-multiplier gap| across every pair: 6.661e-16 (must be ~0)

--- base EWALL ---
                     n  gt_cheaper  med_d_gt  med_d_decay  med_dS0  med_dS10  med_dS25  win25
form  state   side                                                                           
RAMP  CORR    HI    48      0.1667    0.1095       0.0026   0.0062    0.0060    0.0040 0.6250
              LO    48      0.0000    0.4455       0.0086  -0.0065   -0.0100   -0.0148 0.0417
      NAMEVOL HI    36      0.1667    0.1473       0.0032   0.0119    0.0115    0.0110 0.6111
              LO    48      0.0833    0.4621       0.0089   0.0010   -0.0015   -0.0051 0.3333
      PORTVOL HI    36      0.2778    0.1153       0.0024   0.0059    0.0047    0.0023 0.6111
              LO    48      0.0000    0.4837       0.0092  -0.0107   -0.0140   -0.0177 0.0000
RATIO CORR    HI    48      0.4167    0.0200       0.0005   0.0001    0.0014    0.0034 0.5000
              LO    48      0.0000    0.2120       0.0041   0.0022    0.0008   -0.0031 0.3750
      NAMEVOL HI    36      0.3889    0.0404       0.0009  -0.0032   -0.0032   -0.0033 0.4444
              LO    48      0.0833    0.3758       0.0071  -0.0022   -0.0040   -0.0067 0.2917
      PORTVOL HI    36      0.5000   -0.0039       0.0000   0.0033    0.0046    0.0065 0.6667
              LO    48      0.0000    0.3404       0.0065  -0.0072   -0.0097   -0.0129 0.1250

--- base TOP20 ---
                     n  gt_cheaper  med_d_gt  med_d_decay  med_dS0  med_dS10  med_dS25  win25
form  state   side                                                                           
RAMP  CORR    HI    48      0.1667    0.1095       0.0021   0.0055    0.0052    0.0049 0.5833
              LO    48      0.0000    0.4455       0.0072  -0.0037   -0.0065   -0.0101 0.0417
      NAMEVOL HI    36      0.1667    0.1473       0.0026   0.0073    0.0069    0.0064 0.5556
              LO    48      0.0833    0.4621       0.0074  -0.0030   -0.0050   -0.0080 0.2917
      PORTVOL HI    36      0.2778    0.1153       0.0020   0.0039    0.0022    0.0011 0.5556
              LO    48      0.0000    0.4837       0.0076  -0.0105   -0.0118   -0.0146 0.0833
RATIO CORR    HI    48      0.4167    0.0200       0.0004   0.0027    0.0028    0.0030 0.5417
              LO    48      0.0000    0.2120       0.0034   0.0003   -0.0009   -0.0031 0.3333
      NAMEVOL HI    36      0.3889    0.0404       0.0008  -0.0003   -0.0004   -0.0006 0.4444
              LO    48      0.0833    0.3758       0.0059  -0.0034   -0.0053   -0.0062 0.2083
      PORTVOL HI    36      0.5000   -0.0039       0.0000   0.0040    0.0041    0.0051 0.7222
              LO    48      0.0000    0.3404       0.0054  -0.0064   -0.0088   -0.0136 0.1250

================================================================================================================
HYPOTHESES (EWALL base = idea 870's own; TOP20 reported beside it)
================================================================================================================

[EWALL]
  RAMP   H_CHEAP FALSIFIED (min family share below BINARY turnover 0.000; worst family ('CORR', 'LO'))
         H_COST  FALSIFIED (median dSharpe@25 range -0.0177..+0.0110; families with dS25>dS0 0 of 6)
         H_FREE  SUPPORTED (|median dSharpe@0| max 0.0119, range -0.0107..+0.0119)
  RATIO  H_CHEAP FALSIFIED (min family share below BINARY turnover 0.000; worst family ('CORR', 'LO'))
         H_COST  FALSIFIED (median dSharpe@25 range -0.0129..+0.0065; families with dS25>dS0 2 of 6)
         H_FREE  SUPPORTED (|median dSharpe@0| max 0.0072, range -0.0072..+0.0033)

[TOP20]
  RAMP   H_CHEAP FALSIFIED (min family share below BINARY turnover 0.000; worst family ('CORR', 'LO'))
         H_COST  FALSIFIED (median dSharpe@25 range -0.0146..+0.0064; families with dS25>dS0 0 of 6)
         H_FREE  SUPPORTED (|median dSharpe@0| max 0.0105, range -0.0105..+0.0073)
  RATIO  H_CHEAP FALSIFIED (min family share below BINARY turnover 0.000; worst family ('CORR', 'LO'))
         H_COST  FALSIFIED (median dSharpe@25 range -0.0136..+0.0051; families with dS25>dS0 2 of 6)
         H_FREE  SUPPORTED (|median dSharpe@0| max 0.0064, range -0.0064..+0.0040)

================================================================================================================
COST DECAY by form (the queue's own statistic), all arms, both bases
================================================================================================================
                n  med_decay  med_gt  med_S10  keep4b  keep4a  oos4b
base  form                                                          
EWALL BINARY  264     0.0238  1.2050   1.0440      58       0    164
      RAMP    264     0.0294  1.4558   1.0361      52       0    160
      RATIO   264     0.0271  1.3374   1.0409      50       0    160
TOP20 BINARY  264     0.0196  1.2050   1.2107     138       0    138
      RAMP    264     0.0242  1.4558   1.2046     182       0    182
      RATIO   264     0.0223  1.3374   1.2085     171       0    171

================================================================================================================
PROTOCOL rule 8 walk-forward — IS-only pick per FORM, OOS read once
================================================================================================================
  form     family      q   w  depth cad  gross   IS_S  OOS_CAGR  OOS_S  OOS_MaxDD  OOS_H1  OOS_H2  oos4a  oos4b  full_CAGR  full_S  full_MaxDD     gt  decay
BINARY    CORR-HI 0.1700 504 0.2500   D 1.0000 1.0128    0.1531 1.2129    -0.1816  1.4032  1.0241  False   True     0.1397  1.1230     -0.1816 1.6445 0.0338
  RAMP    CORR-HI 0.0700 252 0.2500   D 1.0000 1.0057    0.1528 1.1850    -0.1918  1.4210  0.9509  False   True     0.1404  1.1045     -0.1918 1.2531 0.0249
 RATIO PORTVOL-HI 0.1700 252 0.2500   W 1.0000 1.0084    0.1494 1.2050    -0.1819  1.4381  0.9765  False   True     0.1377  1.1158     -0.1819 0.8271 0.0173

benchmarks — SPY full 15.13% / 0.885 / -33.72%  (H1 0.959 H2 0.824);  OOS 15.27% / 0.874 / -33.72%
             RULES v2 (live) full 8.64% / 1.208 / -11.90%;  OOS 9.49% / 1.286 / -11.90%
             TOP20 shelf book g0.65 full 14.80% / 1.213 (printed at g=0.75, the grid's rung, not the shelf's 0.65)

================================================================================================================
4b / 4a FOOTPRINT by form (matched-gross arms only)
================================================================================================================
              keep4a  keep4b  oos4a  oos4b
base  form                                
EWALL BINARY  0.0000  0.2197 0.0000 0.6212
      RAMP    0.0000  0.1970 0.0000 0.6061
      RATIO   0.0000  0.1894 0.0000 0.6061
TOP20 BINARY  0.0000  0.5227 0.0000 0.5227
      RAMP    0.0000  0.6894 0.0000 0.6894
      RATIO   0.0000  0.6477 0.0000 0.6477

SURVIVORSHIP: universe.json is the current constituent list; levels optimistic, the CONT-minus-BINARY differencing at matched gross is the durable part.
```
