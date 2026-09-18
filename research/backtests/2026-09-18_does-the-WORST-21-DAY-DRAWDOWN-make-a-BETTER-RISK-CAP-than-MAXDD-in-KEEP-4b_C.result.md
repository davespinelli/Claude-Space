# Idea 1282 (lane C) — run log

```
# Idea 1282 (lane C, 2026-09-18) — does the WORST 21-DAY DRAWDOWN make a BETTER RISK CAP
# than MAXDD in KEEP 4b?   seed 1282, B 400, block 63 (robustness [42, 63, 126]), cost 10 bps
# DIAL 1 k = ['K21', 'K63', 'K126', 'K252', 'KFULL']   DIAL 2 cap multiple = [0.5, 0.6, 0.75, 1.0]   (incumbent cell = KFULL @ 0.60)

PANELS: U56 55 names (2008-01-02..2026-09-17); B136 135 (2008-01-02..2026-09-11); SMALL663 664 of 715 kept (2010-01-04..2026-09-11)
  GATE G1 fast runner == engine.backtest (anchor, U56): PASS  value=2.082e-17  target=< 1e-10
  GATE G2 K_FULL == MaxDD exactly (anchor, U56): PASS  value=0.000e+00  target=== 0
  GATE G3 vectorised rolling max == deque reference: PASS  value=0.000e+00  target=== 0
  GATE G4 |K_k| non-decreasing in k (anchor, U56): PASS  value=0  target=== 0

=== U56 ===
  books 22 keys; windows FULL 2009-01-13..2026-09-17, IS ..2016-12-30, OOS 2017-01-03..

=== B136 ===
  books 22 keys; windows FULL 2009-01-13..2026-09-11, IS ..2016-12-30, OOS 2017-01-03..

=== SMALL663 ===
  books 22 keys; windows FULL 2011-01-13..2026-09-11, IS ..2016-12-30, OOS 2017-01-03..
  GATE G5 incumbent cell == PROTOCOL 4b's L_DD: PASS  value=0.000e+00  target=< 1e-12
  GATE G6 SD stable across rng streams (U56 FULL, median rel. move): PASS  value=0.0288  target=< 0.15
  GATE G7 every chooser decided on IS rows only (structural): PASS  value=True  target=True

==============================================================================
ARM 1 — DOES THE RE-KEY MOVE ANYTHING?  (flip = this cell's DD verdict != KFULL@0.60)
==============================================================================
  DD-leg flip share, every one of the 20 dial cells (all panels, all windows, all books):
mult    0.50   0.60   0.75   1.00
k                                
K21   0.1717 0.2121 0.2626 0.4394
K63   0.1616 0.0202 0.2576 0.3889
K126  0.1717 0.0000 0.2374 0.3687
K252  0.1717 0.0000 0.2374 0.3687
KFULL 0.1717 0.0000 0.2374 0.3687

  WHOLE-4b flip share (the other three legs held at their own values):
mult    0.50   0.60   0.75   1.00
k                                
K21   0.1465 0.1818 0.2071 0.2677
K63   0.1414 0.0101 0.2020 0.2626
K126  0.1465 0.0000 0.1970 0.2576
K252  0.1465 0.0000 0.1970 0.2576
KFULL 0.1465 0.0000 0.1970 0.2576

  AT THE PROTOCOL MULTIPLE 0.60, by k and panel (DD-leg flip share):
panel   B136  SMALL663    U56
k                            
K21   0.1970    0.0455 0.3939
K63   0.0152    0.0303 0.0152
K126  0.0000    0.0000 0.0000
K252  0.0000    0.0000 0.0000
KFULL 0.0000    0.0000 0.0000

  PASS RATES at the protocol multiple (share of books whose DD leg passes):
window   FULL     IS    OOS
k                          
K21    0.3485 0.6364 0.3485
K63    0.4242 0.3939 0.4242
K126   0.4242 0.3333 0.4242
K252   0.4242 0.3333 0.4242
KFULL  0.4242 0.3333 0.4242

  DEGENERACY (share of cells whose margin is bit-identical to the incumbent's), 1146's reading reproduced at the cap:
    K126 0.9394, K21 0.0000, K252 0.9545, K63 0.6566

==============================================================================
ARM 2 — IS THE RE-KEYED CAP BETTER RESOLVED?  (paired block bootstrap, L=63)
==============================================================================
  share of DD verdicts decided INSIDE 1 SD of their own margin:
mult    0.50   0.60   0.75   1.00
k                                
K21   0.2121 0.3030 0.1162 0.0808
K63   0.2071 0.3232 0.1970 0.1515
K126  0.2576 0.3384 0.2323 0.1869
K252  0.3030 0.3687 0.2626 0.1970
KFULL 0.3535 0.3990 0.3030 0.2222

  median |margin| / SD, and the median SD itself (the cap's own resolution):
    K21    median |M|/SD 2.308; median SD 0.0225 (L=42 0.0212, L=126 0.0226); inside 1 SD 0.3030, inside 2 SD 0.4495
    K63    median |M|/SD 1.965; median SD 0.0263 (L=42 0.0263, L=126 0.0254); inside 1 SD 0.3232, inside 2 SD 0.5101
    K126   median |M|/SD 1.888; median SD 0.0299 (L=42 0.0295, L=126 0.0282); inside 1 SD 0.3384, inside 2 SD 0.5202
    K252   median |M|/SD 1.648; median SD 0.0329 (L=42 0.0327, L=126 0.0312); inside 1 SD 0.3687, inside 2 SD 0.5556
    KFULL  median |M|/SD 1.375; median SD 0.0358 (L=42 0.0369, L=126 0.0343); inside 1 SD 0.3990, inside 2 SD 0.6364

==============================================================================
ARM 3 — DOES THE IN-SAMPLE READING FORECAST THE OUT-OF-SAMPLE DRAWDOWN?
==============================================================================
  Spearman rho across the record's own ladder books, IS statistic -> OOS outcome:
   panel     k  n_books  rho_IS_to_OOS_MaxDD  rho_IS_to_OOS_K21
     U56   K21       22               0.7751             0.5786
     U56   K63       22               0.7819             0.5866
     U56  K126       22               0.7706             0.5741
     U56  K252       22               0.7706             0.5741
     U56 KFULL       22               0.7706             0.5741
    B136   K21       22               0.7172             0.7535
    B136   K63       22               0.7161             0.7467
    B136  K126       22               0.7013             0.7331
    B136  K252       22               0.7013             0.7331
    B136 KFULL       22               0.7013             0.7331
SMALL663   K21       22               0.8365             0.8455
SMALL663   K63       22               0.9364             0.9512
SMALL663  K126       22               0.7831             0.6752
SMALL663  K252       22               0.7910             0.6684
SMALL663 KFULL       22               0.7922             0.6616

  panel-mean rho:
       rho_IS_to_OOS_MaxDD  rho_IS_to_OOS_K21
k                                            
K21                 0.7763             0.7259
K63                 0.8115             0.7615
K126                0.7517             0.6608
K252                0.7543             0.6585
KFULL               0.7547             0.6563

==============================================================================
ARM 4 — CAPITAL ARM (PROTOCOL rule 8, OOS 2017-2026 READ ONCE)
==============================================================================
  d = (K-keyed chooser) - (MAXDD-keyed chooser at the SAME cap multiple), OOS:
   panel     k   mult   pick pick_incumbent_key  same_pick  n_IS_pass  n_IS_pass_incumbent  d_OOS_Sharpe  d_OOS_CAGR  d_OOS_MaxDD
     U56   K21 0.5000   N=40               N=40       True          5                    0        0.0000      0.0000       0.0000
     U56   K21 0.6000   N=40               N=40       True         14                    6        0.0000      0.0000       0.0000
     U56   K21 0.7500   N=40               N=40       True         15                   14        0.0000      0.0000       0.0000
     U56   K21 1.0000   N=40               N=40       True         16                   15        0.0000      0.0000       0.0000
     U56   K63 0.5000 G=0.60               N=40      False          1                    0        0.0614     -0.0039       0.0694
     U56   K63 0.6000   N=40               N=40       True          7                    6        0.0000      0.0000       0.0000
     U56   K63 0.7500   N=40               N=40       True         15                   14        0.0000      0.0000       0.0000
     U56   K63 1.0000   N=40               N=40       True         16                   15        0.0000      0.0000       0.0000
     U56  K126 0.5000   N=40               N=40       True          0                    0        0.0000      0.0000       0.0000
     U56  K126 0.6000   N=40               N=40       True          6                    6        0.0000      0.0000       0.0000
     U56  K126 0.7500   N=40               N=40       True         14                   14        0.0000      0.0000       0.0000
     U56  K126 1.0000   N=40               N=40       True         15                   15        0.0000      0.0000       0.0000
     U56  K252 0.5000   N=40               N=40       True          0                    0        0.0000      0.0000       0.0000
     U56  K252 0.6000   N=40               N=40       True          6                    6        0.0000      0.0000       0.0000
     U56  K252 0.7500   N=40               N=40       True         14                   14        0.0000      0.0000       0.0000
     U56  K252 1.0000   N=40               N=40       True         15                   15        0.0000      0.0000       0.0000
     U56 KFULL 0.5000   N=40               N=40       True          0                    0        0.0000      0.0000       0.0000
     U56 KFULL 0.6000   N=40               N=40       True          6                    6        0.0000      0.0000       0.0000
     U56 KFULL 0.7500   N=40               N=40       True         14                   14        0.0000      0.0000       0.0000
     U56 KFULL 1.0000   N=40               N=40       True         15                   15        0.0000      0.0000       0.0000
    B136   K21 0.5000   H=21             G=0.55      False          5                    2       -0.0616      0.0303      -0.1086
    B136   K21 0.6000   H=63               N=30      False         14                    5       -0.0640      0.0005      -0.0434
    B136   K21 0.7500   N=10               H=63      False         17                   15       -0.0788      0.0018       0.0849
    B136   K21 1.0000    N=5               N=10      False         18                   17       -0.1688     -0.0208      -0.0792
    B136   K63 0.5000 G=0.55             G=0.55       True          2                    2        0.0000      0.0000       0.0000
    B136   K63 0.6000   N=30               N=30       True          6                    5        0.0000      0.0000       0.0000
    B136   K63 0.7500   H=63               H=63       True         15                   15        0.0000      0.0000       0.0000
    B136   K63 1.0000   N=10               N=10       True         17                   17        0.0000      0.0000       0.0000
    B136  K126 0.5000 G=0.55             G=0.55       True          2                    2        0.0000      0.0000       0.0000
    B136  K126 0.6000   N=30               N=30       True          5                    5        0.0000      0.0000       0.0000
    B136  K126 0.7500   H=63               H=63       True         15                   15        0.0000      0.0000       0.0000
    B136  K126 1.0000   N=10               N=10       True         17                   17        0.0000      0.0000       0.0000
    B136  K252 0.5000 G=0.55             G=0.55       True          2                    2        0.0000      0.0000       0.0000
    B136  K252 0.6000   N=30               N=30       True          5                    5        0.0000      0.0000       0.0000
    B136  K252 0.7500   H=63               H=63       True         15                   15        0.0000      0.0000       0.0000
    B136  K252 1.0000   N=10               N=10       True         17                   17        0.0000      0.0000       0.0000
    B136 KFULL 0.5000 G=0.55             G=0.55       True          2                    2        0.0000      0.0000       0.0000
    B136 KFULL 0.6000   N=30               N=30       True          5                    5        0.0000      0.0000       0.0000
    B136 KFULL 0.7500   H=63               H=63       True         15                   15        0.0000      0.0000       0.0000
    B136 KFULL 1.0000   N=10               N=10       True         17                   17        0.0000      0.0000       0.0000
SMALL663   K21 0.5000  H=252              H=252       True          0                    0        0.0000      0.0000       0.0000
SMALL663   K21 0.6000  H=252              H=252       True          0                    0        0.0000      0.0000       0.0000
SMALL663   K21 0.7500  H=252              H=252       True          0                    0        0.0000      0.0000       0.0000
SMALL663   K21 1.0000  H=252              H=252       True          0                    0        0.0000      0.0000       0.0000
SMALL663   K63 0.5000  H=252              H=252       True          0                    0        0.0000      0.0000       0.0000
SMALL663   K63 0.6000  H=252              H=252       True          0                    0        0.0000      0.0000       0.0000
SMALL663   K63 0.7500  H=252              H=252       True          0                    0        0.0000      0.0000       0.0000
SMALL663   K63 1.0000  H=252              H=252       True          0                    0        0.0000      0.0000       0.0000
SMALL663  K126 0.5000  H=252              H=252       True          0                    0        0.0000      0.0000       0.0000
SMALL663  K126 0.6000  H=252              H=252       True          0                    0        0.0000      0.0000       0.0000
SMALL663  K126 0.7500  H=252              H=252       True          0                    0        0.0000      0.0000       0.0000
SMALL663  K126 1.0000  H=252              H=252       True          0                    0        0.0000      0.0000       0.0000
SMALL663  K252 0.5000  H=252              H=252       True          0                    0        0.0000      0.0000       0.0000
SMALL663  K252 0.6000  H=252              H=252       True          0                    0        0.0000      0.0000       0.0000
SMALL663  K252 0.7500  H=252              H=252       True          0                    0        0.0000      0.0000       0.0000
SMALL663  K252 1.0000  H=252              H=252       True          0                    0        0.0000      0.0000       0.0000
SMALL663 KFULL 0.5000  H=252              H=252       True          0                    0        0.0000      0.0000       0.0000
SMALL663 KFULL 0.6000  H=252              H=252       True          0                    0        0.0000      0.0000       0.0000
SMALL663 KFULL 0.7500  H=252              H=252       True          0                    0        0.0000      0.0000       0.0000
SMALL663 KFULL 1.0000  H=252              H=252       True          0                    0        0.0000      0.0000       0.0000

  over 48 re-keyed cells: mean d(OOS Sharpe) -0.0065, SE 0.0044, t -1.47; picks differ in 5 of 48 cells
  K21 ALONE (12 cells): mean d(OOS Sharpe) -0.0311, SE 0.0153; mean d(OOS MaxDD) -0.0122 (negative = deeper); picks differ in 4 of 12

  EVERY OOS CHOOSER ROW, BOTH KEEP PATHS (4b's DD leg shown on the INCUMBENT key, which is the one the record publishes, and on the cell's OWN key):
   panel     k   mult   pick  n_IS_pass  OOS_CAGR  OOS_Sharpe  OOS_MaxDD  OOS_H1  OOS_H2  SPY_OOS_Sharpe  V2_OOS_Sharpe  KEEP_4b  KEEP_4b_ownkey  KEEP_4a
     U56   K21 0.5000   N=40          5    0.1416      1.1212    -0.2246  1.2694  0.9590          0.8747         1.2781    False           False    False
     U56   K21 0.6000   N=40         14    0.1416      1.1212    -0.2246  1.2694  0.9590          0.8747         1.2781    False           False    False
     U56   K21 0.7500   N=40         15    0.1416      1.1212    -0.2246  1.2694  0.9590          0.8747         1.2781    False            True    False
     U56   K21 1.0000   N=40         16    0.1416      1.1212    -0.2246  1.2694  0.9590          0.8747         1.2781    False            True    False
     U56   K63 0.5000 G=0.60          1    0.1378      1.1826    -0.1551  1.2642  1.1016          0.8747         1.2781     True            True    False
     U56   K63 0.6000   N=40          7    0.1416      1.1212    -0.2246  1.2694  0.9590          0.8747         1.2781    False           False    False
     U56   K63 0.7500   N=40         15    0.1416      1.1212    -0.2246  1.2694  0.9590          0.8747         1.2781    False            True    False
     U56   K63 1.0000   N=40         16    0.1416      1.1212    -0.2246  1.2694  0.9590          0.8747         1.2781    False            True    False
     U56  K126 0.5000   N=40          0    0.1416      1.1212    -0.2246  1.2694  0.9590          0.8747         1.2781    False           False    False
     U56  K126 0.6000   N=40          6    0.1416      1.1212    -0.2246  1.2694  0.9590          0.8747         1.2781    False           False    False
     U56  K126 0.7500   N=40         14    0.1416      1.1212    -0.2246  1.2694  0.9590          0.8747         1.2781    False            True    False
     U56  K126 1.0000   N=40         15    0.1416      1.1212    -0.2246  1.2694  0.9590          0.8747         1.2781    False            True    False
     U56  K252 0.5000   N=40          0    0.1416      1.1212    -0.2246  1.2694  0.9590          0.8747         1.2781    False           False    False
     U56  K252 0.6000   N=40          6    0.1416      1.1212    -0.2246  1.2694  0.9590          0.8747         1.2781    False           False    False
     U56  K252 0.7500   N=40         14    0.1416      1.1212    -0.2246  1.2694  0.9590          0.8747         1.2781    False            True    False
     U56  K252 1.0000   N=40         15    0.1416      1.1212    -0.2246  1.2694  0.9590          0.8747         1.2781    False            True    False
     U56 KFULL 0.5000   N=40          0    0.1416      1.1212    -0.2246  1.2694  0.9590          0.8747         1.2781    False           False    False
     U56 KFULL 0.6000   N=40          6    0.1416      1.1212    -0.2246  1.2694  0.9590          0.8747         1.2781    False           False    False
     U56 KFULL 0.7500   N=40         14    0.1416      1.1212    -0.2246  1.2694  0.9590          0.8747         1.2781    False            True    False
     U56 KFULL 1.0000   N=40         15    0.1416      1.1212    -0.2246  1.2694  0.9590          0.8747         1.2781    False            True    False
    B136   K21 0.5000   H=21          5    0.1498      0.9605    -0.2637  0.9666  0.9567          0.8769         1.1061    False           False    False
    B136   K21 0.6000   H=63         14    0.1661      1.0023    -0.2869  0.9427  1.0832          0.8769         1.1061    False           False    False
    B136   K21 0.7500   N=10         17    0.1679      0.9235    -0.2020  0.7629  1.0605          0.8769         1.1061    False           False    False
    B136   K21 1.0000    N=5         18    0.1471      0.7546    -0.2812  0.6004  0.8832          0.8769         1.1061    False           False    False
    B136   K63 0.5000 G=0.55          2    0.1195      1.0221    -0.1551  1.0534  0.9989          0.8769         1.1061     True            True    False
    B136   K63 0.6000   N=30          6    0.1656      1.0663    -0.2435  1.1718  0.9562          0.8769         1.1061    False           False    False
    B136   K63 0.7500   H=63         15    0.1661      1.0023    -0.2869  0.9427  1.0832          0.8769         1.1061    False           False    False
    B136   K63 1.0000   N=10         17    0.1679      0.9235    -0.2020  0.7629  1.0605          0.8769         1.1061    False           False    False
    B136  K126 0.5000 G=0.55          2    0.1195      1.0221    -0.1551  1.0534  0.9989          0.8769         1.1061     True            True    False
    B136  K126 0.6000   N=30          5    0.1656      1.0663    -0.2435  1.1718  0.9562          0.8769         1.1061    False           False    False
    B136  K126 0.7500   H=63         15    0.1661      1.0023    -0.2869  0.9427  1.0832          0.8769         1.1061    False           False    False
    B136  K126 1.0000   N=10         17    0.1679      0.9235    -0.2020  0.7629  1.0605          0.8769         1.1061    False           False    False
    B136  K252 0.5000 G=0.55          2    0.1195      1.0221    -0.1551  1.0534  0.9989          0.8769         1.1061     True            True    False
    B136  K252 0.6000   N=30          5    0.1656      1.0663    -0.2435  1.1718  0.9562          0.8769         1.1061    False           False    False
    B136  K252 0.7500   H=63         15    0.1661      1.0023    -0.2869  0.9427  1.0832          0.8769         1.1061    False           False    False
    B136  K252 1.0000   N=10         17    0.1679      0.9235    -0.2020  0.7629  1.0605          0.8769         1.1061    False           False    False
    B136 KFULL 0.5000 G=0.55          2    0.1195      1.0221    -0.1551  1.0534  0.9989          0.8769         1.1061     True            True    False
    B136 KFULL 0.6000   N=30          5    0.1656      1.0663    -0.2435  1.1718  0.9562          0.8769         1.1061    False           False    False
    B136 KFULL 0.7500   H=63         15    0.1661      1.0023    -0.2869  0.9427  1.0832          0.8769         1.1061    False           False    False
    B136 KFULL 1.0000   N=10         17    0.1679      0.9235    -0.2020  0.7629  1.0605          0.8769         1.1061    False           False    False
SMALL663   K21 0.5000  H=252          0    0.1116      0.6677    -0.3741  1.2072  0.0769          0.8769         0.6518    False           False    False
SMALL663   K21 0.6000  H=252          0    0.1116      0.6677    -0.3741  1.2072  0.0769          0.8769         0.6518    False           False    False
SMALL663   K21 0.7500  H=252          0    0.1116      0.6677    -0.3741  1.2072  0.0769          0.8769         0.6518    False           False    False
SMALL663   K21 1.0000  H=252          0    0.1116      0.6677    -0.3741  1.2072  0.0769          0.8769         0.6518    False           False    False
SMALL663   K63 0.5000  H=252          0    0.1116      0.6677    -0.3741  1.2072  0.0769          0.8769         0.6518    False           False    False
SMALL663   K63 0.6000  H=252          0    0.1116      0.6677    -0.3741  1.2072  0.0769          0.8769         0.6518    False           False    False
SMALL663   K63 0.7500  H=252          0    0.1116      0.6677    -0.3741  1.2072  0.0769          0.8769         0.6518    False           False    False
SMALL663   K63 1.0000  H=252          0    0.1116      0.6677    -0.3741  1.2072  0.0769          0.8769         0.6518    False           False    False
SMALL663  K126 0.5000  H=252          0    0.1116      0.6677    -0.3741  1.2072  0.0769          0.8769         0.6518    False           False    False
SMALL663  K126 0.6000  H=252          0    0.1116      0.6677    -0.3741  1.2072  0.0769          0.8769         0.6518    False           False    False
SMALL663  K126 0.7500  H=252          0    0.1116      0.6677    -0.3741  1.2072  0.0769          0.8769         0.6518    False           False    False
SMALL663  K126 1.0000  H=252          0    0.1116      0.6677    -0.3741  1.2072  0.0769          0.8769         0.6518    False           False    False
SMALL663  K252 0.5000  H=252          0    0.1116      0.6677    -0.3741  1.2072  0.0769          0.8769         0.6518    False           False    False
SMALL663  K252 0.6000  H=252          0    0.1116      0.6677    -0.3741  1.2072  0.0769          0.8769         0.6518    False           False    False
SMALL663  K252 0.7500  H=252          0    0.1116      0.6677    -0.3741  1.2072  0.0769          0.8769         0.6518    False           False    False
SMALL663  K252 1.0000  H=252          0    0.1116      0.6677    -0.3741  1.2072  0.0769          0.8769         0.6518    False           False    False
SMALL663 KFULL 0.5000  H=252          0    0.1116      0.6677    -0.3741  1.2072  0.0769          0.8769         0.6518    False           False    False
SMALL663 KFULL 0.6000  H=252          0    0.1116      0.6677    -0.3741  1.2072  0.0769          0.8769         0.6518    False           False    False
SMALL663 KFULL 0.7500  H=252          0    0.1116      0.6677    -0.3741  1.2072  0.0769          0.8769         0.6518    False           False    False
SMALL663 KFULL 1.0000  H=252          0    0.1116      0.6677    -0.3741  1.2072  0.0769          0.8769         0.6518    False           False    False

  KEEP over 60 OOS chooser rows: 4b (incumbent key) 5, 4b (own key) 15, 4a 0
  U56 comparands, OOS: SPY 15.28% / 0.8747 / -33.72% (K21 -30.99%); RULES v2 9.47% / 1.2781 / -12.05%; RULES v1 Sharpe 0.7291

  EVERY DISTINCT PICK ON THE FULL SAMPLE (rule 4's halves; no 4b verdict is quoted from the OOS window alone):
   panel   pick  FULL_CAGR  FULL_Sharpe  FULL_MaxDD  FULL_H1  FULL_H2  SPY_FULL_Sharpe  V2_FULL_Sharpe  FULL_m_DD_incumbent  FULL_m_DD_K21  FULL_4b_incumbent  FULL_4b_K21  FULL_4a
     U56 G=0.60     0.1259       1.1517     -0.1551   1.2123   1.1121           0.8849          1.2018               0.0472         0.0308               True         True    False
     U56   N=40     0.1344       1.1347     -0.2246   1.2663   1.0427           0.8849          1.2018              -0.0223        -0.0265              False        False    False
    B136 G=0.55     0.1185       1.0699     -0.1551   1.2885   0.8976           0.8862          1.0994               0.0472         0.0423               True         True    False
    B136   H=21     0.1604       1.0690     -0.2637   1.3230   0.8647           0.8862          1.0994              -0.0614        -0.0516              False        False    False
    B136   H=63     0.1714       1.0923     -0.2869   1.3529   0.8941           0.8862          1.0994              -0.0847        -0.0875              False        False    False
    B136   N=10     0.1853       1.0666     -0.2020   1.3780   0.8362           0.8862          1.0994               0.0003        -0.0082               True        False    False
    B136   N=30     0.1599       1.0962     -0.2435   1.2738   0.9656           0.8862          1.0994              -0.0412        -0.0542              False        False    False
    B136    N=5     0.1873       0.9690     -0.2812   1.3074   0.7109           0.8862          1.0994              -0.0789        -0.0953              False        False    False
SMALL663  H=252     0.1336       0.7845     -0.3741   0.9555   0.6419           0.8582          0.7130              -0.1718        -0.1882              False        False    False
  FULL-sample 4b over 9 distinct picks: incumbent key 3, K21 key 2; 4a 0

  ANCHOR (U56 N=20/H=126/G=0.75/W) FULL 15.78% / 1.1522 / -19.13% (K21 -19.13%); OOS 17.28% / 1.1832 / -19.13%

==============================================================================
  PRE-DECLARED OUTCOME, read mechanically: (B) DIFFERENT, NOT BETTER
    flip share at the protocol multiple 0.2121 (bar 0.05); inside-1-SD K21 0.1780 vs KFULL 0.3194 (better); forecast rho K21 +0.7763 vs KFULL +0.7547 (better); capital d -0.0311 vs SE 0.0153 (does not pay)
==============================================================================

wrote 2026-09-18_does-the-WORST-21-DAY-DRAWDOWN-make-a-BETTER-RISK-CAP-than-MAXDD-in-KEEP-4b_C.[rescore.csv.gz|cells|capital|books|forecast|picks_full|gates].csv  (98s); gates 7 of 7 passing
```
