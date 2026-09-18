# Idea 1259 (lane C) — run log

```
# Idea 1259 (lane C, 2026-09-18) — is a 4b LEG decided inside its own ROUNDING?
# seed 1259, B 400, block 63 (robustness [42, 63, 126]), cost 10 bps

PANELS: U56 55 names (2008-01-02..2026-09-17); B136 135 (2008-01-02..2026-09-11); SMALL663 664 of 715 kept (2010-01-04..2026-09-11)
  GATE G1 fast runner == engine.backtest (anchor, U56): PASS  value=2.082e-17  target=< 1e-10

=== U56 ===
  books 34 distinct keys; windows FULL 2009-01-13..2026-09-17, IS ..2016-12-30, OOS 2017-01-03..

=== B136 ===
  books 34 distinct keys; windows FULL 2009-01-13..2026-09-11, IS ..2016-12-30, OOS 2017-01-03..

=== SMALL663 ===
  books 34 distinct keys; windows FULL 2011-01-13..2026-09-11, IS ..2016-12-30, OOS 2017-01-03..
  GATE G2 SD stable across rng streams (U56 FULL, median rel. move): PASS  value=0.0512  target=< 0.15
  GATE G3 no degenerate (zero-SD) leg: PASS  value=0  target=== 0

==============================================================================
ARM 1 — HOW MANY 4b VERDICTS ARE DECIDED INSIDE THEIR OWN RESOLUTION?
==============================================================================
  V_LAD bar 1 SD — inside-share by leg: L_H1 0.561, L_H2 0.333, L_CAGR 0.288, L_DD 0.414  | ALL 0.399  (n=792)
  V_LAD bar 2 SD — inside-share by leg: L_H1 0.955, L_H2 0.783, L_CAGR 0.662, L_DD 0.662  | ALL 0.765  (n=792)
  V_GRID bar 1 SD — inside-share by leg: L_H1 0.593, L_H2 0.426, L_CAGR 0.269, L_DD 0.352  | ALL 0.410  (n=432)
  V_GRID bar 2 SD — inside-share by leg: L_H1 0.889, L_H2 0.806, L_CAGR 0.620, L_DD 0.630  | ALL 0.736  (n=432)

  window FULL bar 1 SD inside-share: L_H1 0.186, L_H2 0.382, L_CAGR 0.225, L_DD 0.373  | median |M|/SD: L_H1 1.64, L_H2 1.77, L_CAGR 2.19, L_DD 1.66
  window IS   bar 1 SD inside-share: L_H1 0.843, L_H2 0.402, L_CAGR 0.402, L_DD 0.480  | median |M|/SD: L_H1 0.42, L_H2 1.08, L_CAGR 1.25, L_DD 1.10
  window OOS  bar 1 SD inside-share: L_H1 0.686, L_H2 0.314, L_CAGR 0.216, L_DD 0.324  | median |M|/SD: L_H1 0.62, L_H2 1.76, L_CAGR 1.56, L_DD 1.69

  panel U56       bar 1 SD inside-share 0.355, bar 2 SD 0.831, median |M|/SD 1.30
  panel B136      bar 1 SD inside-share 0.463, bar 2 SD 0.789, median |M|/SD 1.09
  panel SMALL663  bar 1 SD inside-share 0.390, bar 2 SD 0.645, median |M|/SD 1.37

  THE RESOLUTION ITSELF (median SD of the margin, L=63, over all books/panels/windows):
    L_H1    median SD 0.2502 Sharpe; L=42 0.2637, L=126 0.2204; the record PRINTS this leg to +/-0.005 (50x coarser than it measures)
    L_H2    median SD 0.2456 Sharpe; L=42 0.2642, L=126 0.2236; the record PRINTS this leg to +/-0.005 (49x coarser than it measures)
    L_CAGR  median SD 0.0255 fraction; L=42 0.0270, L=126 0.0245; the record PRINTS this leg to +/-0.0005 (51x coarser than it measures)
    L_DD    median SD 0.0379 fraction; L=42 0.0405, L=126 0.0351; the record PRINTS this leg to +/-0.0005 (76x coarser than it measures)

  TEXT-ROUNDING reference: only 0.0090 of verdicts are inside the record's PRINTED precision, against 0.4028 inside 1 SD — the published digits are ~40x finer than the tape resolves.

  THE RECORD'S OWN PUBLISHING HABIT (committed text, reported not gated):
    LEADERBOARD.md  5.21 MB, 3760 units mention 4b; 235 state a MARGIN (0.0625), 48 state an SE/SD (0.0128)
    CHANGELOG.md    0.85 MB, 419 units mention 4b; 14 state a MARGIN (0.0334), 11 state an SE/SD (0.0263)

==============================================================================
ARM 2 — CAPITAL ARM (PROTOCOL rule 8, OOS 2017-2026 READ ONCE): DOES DECISIVENESS PAY?
==============================================================================
   panel verdict_set    bar  n_candidates  n_IS_pass  n_IS_decisive   pick_ANY  pick_DEC  same_pick  d_OOS_Sharpe  d_OOS_CAGR  d_OOS_MaxDD
     U56       V_LAD 1.0000            22          6              0       N=40      N=40       True        0.0000      0.0000       0.0000
     U56       V_LAD 2.0000            22          6              0       N=40      N=40       True        0.0000      0.0000       0.0000
     U56      V_GRID 1.0000            12          5              0 N=40,H=126  N=5,H=63      False       -0.2217      0.0378      -0.0381
     U56      V_GRID 2.0000            12          5              0 N=40,H=126  N=5,H=63      False       -0.2217      0.0378      -0.0381
    B136       V_LAD 1.0000            22          5              0       N=30       N=5      False       -0.3116     -0.0185      -0.0377
    B136       V_LAD 2.0000            22          5              0       N=30       N=5      False       -0.3116     -0.0185      -0.0377
    B136      V_GRID 1.0000            12          2              0  N=40,H=63  N=5,H=63      False       -0.0629      0.0633      -0.0034
    B136      V_GRID 2.0000            12          2              0  N=40,H=63  N=5,H=63      False       -0.0629      0.0633      -0.0034
SMALL663       V_LAD 1.0000            22          0              0      H=252     H=252       True        0.0000      0.0000       0.0000
SMALL663       V_LAD 2.0000            22          0              0      H=252     H=252       True        0.0000      0.0000       0.0000
SMALL663      V_GRID 1.0000            12          0              0  N=40,H=63 N=40,H=63       True        0.0000      0.0000       0.0000
SMALL663      V_GRID 2.0000            12          0              0  N=40,H=63 N=40,H=63       True        0.0000      0.0000       0.0000

  d(OOS Sharpe) DEC-ANY: mean -0.0994, SE 0.0371, t -2.68, n=12; picks differ in 6 of 12 cells
  d(OOS CAGR)   mean +0.0138; d(OOS MaxDD) mean -0.0132 (negative = deeper drawdown; negative in 6 of 12)

  EVERY OOS CHOOSER ROW, BOTH KEEP PATHS:
   panel verdict_set    bar chooser       pick  OOS_CAGR  OOS_Sharpe  OOS_MaxDD  SPY_OOS_Sharpe  V2_OOS_Sharpe  L_H1  L_H2  L_CAGR  L_DD  KEEP_4b  KEEP_4a
     U56       V_LAD 1.0000     ANY       N=40    0.1416      1.1212    -0.2246          0.8747         1.2781  True  True    True False    False    False
     U56       V_LAD 1.0000     DEC       N=40    0.1416      1.1212    -0.2246          0.8747         1.2781  True  True    True False    False    False
     U56       V_LAD 2.0000     ANY       N=40    0.1416      1.1212    -0.2246          0.8747         1.2781  True  True    True False    False    False
     U56       V_LAD 2.0000     DEC       N=40    0.1416      1.1212    -0.2246          0.8747         1.2781  True  True    True False    False    False
     U56      V_GRID 1.0000     ANY N=40,H=126    0.1416      1.1212    -0.2246          0.8747         1.2781  True  True    True False    False    False
     U56      V_GRID 1.0000     DEC   N=5,H=63    0.1795      0.8996    -0.2626          0.8747         1.2781 False  True    True False    False    False
     U56      V_GRID 2.0000     ANY N=40,H=126    0.1416      1.1212    -0.2246          0.8747         1.2781  True  True    True False    False    False
     U56      V_GRID 2.0000     DEC   N=5,H=63    0.1795      0.8996    -0.2626          0.8747         1.2781 False  True    True False    False    False
    B136       V_LAD 1.0000     ANY       N=30    0.1656      1.0663    -0.2435          0.8769         1.1061  True  True    True False    False    False
    B136       V_LAD 1.0000     DEC        N=5    0.1471      0.7546    -0.2812          0.8769         1.1061 False  True    True False    False    False
    B136       V_LAD 2.0000     ANY       N=30    0.1656      1.0663    -0.2435          0.8769         1.1061  True  True    True False    False    False
    B136       V_LAD 2.0000     DEC        N=5    0.1471      0.7546    -0.2812          0.8769         1.1061 False  True    True False    False    False
    B136      V_GRID 1.0000     ANY  N=40,H=63    0.1410      0.9773    -0.2828          0.8769         1.1061  True  True    True False    False    False
    B136      V_GRID 1.0000     DEC   N=5,H=63    0.2043      0.9144    -0.2862          0.8769         1.1061  True  True    True False    False    False
    B136      V_GRID 2.0000     ANY  N=40,H=63    0.1410      0.9773    -0.2828          0.8769         1.1061  True  True    True False    False    False
    B136      V_GRID 2.0000     DEC   N=5,H=63    0.2043      0.9144    -0.2862          0.8769         1.1061  True  True    True False    False    False
SMALL663       V_LAD 1.0000     ANY      H=252    0.1116      0.6677    -0.3741          0.8769         0.6518  True False    True False    False    False
SMALL663       V_LAD 1.0000     DEC      H=252    0.1116      0.6677    -0.3741          0.8769         0.6518  True False    True False    False    False
SMALL663       V_LAD 2.0000     ANY      H=252    0.1116      0.6677    -0.3741          0.8769         0.6518  True False    True False    False    False
SMALL663       V_LAD 2.0000     DEC      H=252    0.1116      0.6677    -0.3741          0.8769         0.6518  True False    True False    False    False
SMALL663      V_GRID 1.0000     ANY  N=40,H=63    0.0758      0.5084    -0.3591          0.8769         0.6518 False False   False False    False    False
SMALL663      V_GRID 1.0000     DEC  N=40,H=63    0.0758      0.5084    -0.3591          0.8769         0.6518 False False   False False    False    False
SMALL663      V_GRID 2.0000     ANY  N=40,H=63    0.0758      0.5084    -0.3591          0.8769         0.6518 False False   False False    False    False
SMALL663      V_GRID 2.0000     DEC  N=40,H=63    0.0758      0.5084    -0.3591          0.8769         0.6518 False False   False False    False    False

  KEEP paths over 24 OOS chooser rows: 4b 0, 4a 0.  Binding leg counts (failures): L_H1 8, L_H2 8, L_CAGR 4, L_DD 24
  SPY OOS 15.28% / 0.8747 / -33.72% (U56 rows); RULES v2 OOS 9.47% / 1.2781 / -12.05%; RULES v1 OOS Sharpe 0.7291

  PRE-DECLARED OUTCOME, read mechanically: (B) THE BINARY IS UNSAFE (worst leg L_H1 at 0.572 inside 1 SD; best leg L_CAGR at 0.281)

wrote 2026-09-18_should-a-4b-LEG-DECIDED-INSIDE-ITS-OWN-ROUNDING-be-PUBLISHABLE-as-a-BINARY_C.[census|dialcells|capital|books|textcensus|gates].csv  (66s)
```
