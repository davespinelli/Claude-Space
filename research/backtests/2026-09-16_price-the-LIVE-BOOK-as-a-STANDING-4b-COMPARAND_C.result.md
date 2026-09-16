# Idea 997 (lane C, 2026-09-16) — price the LIVE BOOK as a standing 4b comparand

**Verdict: KEEP-candidate (4b) on U56, CONDITIONAL. KEEP path 4a refused 0 of 78. Gates 10 of 10. Hypotheses 9 of 12.**

The live book's only 4b failure is `L5_CAGR`. Walking the same book on gross 0.25→1.50 locates both crossings and the window between them.

```
(A) GATES -- printed before any hypothesis number
====================================================================================================
  G0  offset_mask vs engine.rebalance_mask       : 0 disagreeing rows
  G1  Ctx vs engine.backtest, D             : max|d ret| 4.337e-19  max|d turn| 6.245e-17
  G1  Ctx vs engine.backtest, W             : max|d ret| 6.939e-18  max|d turn| 1.665e-16
  G2  live_book@0.75 vs rules_v2_weights        : max|d| 0.000e+00   (the subject IS the live book)
  G6  gross identity W(g) == (g/0.75)*W(0.75)   : max|d| 3.469e-18

====================================================================================================
(B) THE LADDER -- (panel x gross x cadence x phase x cost), the live book at every size
====================================================================================================
  G4  78 target matrices built once, reused across every cadence and phase
  U56    done  (2,080 rows so far, 24s)
  B136   done  (4,160 rows so far, 31s)
  SMALL  done  (6,240 rows so far, 57s)
  wrote 2026-09-16_price-the-LIVE-BOOK-as-a-STANDING-4b-COMPARAND_C.ladder.csv  (6,240 rows, 67 cols)
  G5  determinism (U56 @ 1.00 rebuilt)          : max|d| 0.000e+00
  G8  financing charge: max at g<=1.00 0.000e+00 bps | min at g>1.00 0.0120 bps | identity max|d| 7.105e-15
  G7  IS-purity C_ISSHARPE : real pick 1.5  permuted-OOS pick 1.5  OK
  G7  IS-purity C_ISCAGR   : real pick 1.5  permuted-OOS pick 1.5  OK
  G7  IS-purity C_IS4B     : real pick 1.05  permuted-OOS pick 1.05  OK
  G3  CROSS-RUN idea 993 fallbacks.csv FB_LIVE : 45 cells, max|d| 4.441e-16
  G3b CROSS-RUN idea 993 ladder.csv BAND03/W    : 30 rows x 19 cols = 570 cells, max|d| 2.220e-16
  wrote 2026-09-16_price-the-LIVE-BOOK-as-a-STANDING-4b-COMPARAND_C.gates.csv  (10 rows, 5 cols)
  GATES: 10 of 10 pass

====================================================================================================
```

```
(C) THE GROSS LADDER, HEADLINE CELL (cadence W, phase 0, 10 bps, zero-borrow convention)
    every rung reported; nothing is selected on this table
====================================================================================================

  --- U56 --- SPY: CAGR  15.10% (full) /  15.21% (OOS), MaxDD -33.72%, OOS Sharpe 0.8713
      4b size bars: OOS CAGR >=  10.57%   |OOS MaxDD| <=  20.23%
      gross | OOS CAGR | OOS Shrp | OOS MaxDD |  turn/yr | CAGRleg DDleg | 4b   4a  | fail legs
       0.25 |    3.12% |   1.2775 |    -4.10% |    0.607 |  False True  | False False| L5_CAGR
       0.30 |    3.74% |   1.2774 |    -4.91% |    0.726 |  False True  | False False| L5_CAGR
       0.35 |    4.37% |   1.2773 |    -5.72% |    0.844 |  False True  | False False| L5_CAGR
       0.40 |    5.00% |   1.2772 |    -6.52% |    0.962 |  False True  | False False| L5_CAGR
       0.45 |    5.64% |   1.2771 |    -7.32% |    1.079 |  False True  | False False| L5_CAGR
       0.50 |    6.27% |   1.2770 |    -8.12% |    1.196 |  False True  | False False| L5_CAGR
       0.55 |    6.90% |   1.2769 |    -8.91% |    1.312 |  False True  | False False| L5_CAGR
       0.60 |    7.54% |   1.2768 |    -9.70% |    1.428 |  False True  | False False| L5_CAGR
       0.65 |    8.18% |   1.2767 |   -10.49% |    1.544 |  False True  | False False| L5_CAGR
       0.70 |    8.82% |   1.2766 |   -11.27% |    1.659 |  False True  | False False| L5_CAGR
       0.75 |    9.45% |   1.2765 |   -12.05% |    1.775 |  False True  | False False| L5_CAGR <== INCUMBENT
       0.80 |   10.10% |   1.2764 |   -12.83% |    1.890 |  False True  | False False| L5_CAGR
       0.85 |   10.74% |   1.2762 |   -13.61% |    2.006 |  True  True  | True  False| -
       0.90 |   11.38% |   1.2761 |   -14.38% |    2.121 |  True  True  | True  False| -
       0.95 |   12.02% |   1.2759 |   -15.15% |    2.237 |  True  True  | True  False| -
       1.00 |   12.67% |   1.2758 |   -15.91% |    2.354 |  True  True  | True  False| -
       1.05 |   13.31% |   1.2756 |   -16.67% |    2.470 |  True  True  | True  False| -
       1.10 |   13.96% |   1.2755 |   -17.43% |    2.587 |  True  True  | True  False| -
       1.15 |   14.61% |   1.2753 |   -18.19% |    2.705 |  True  True  | True  False| -
       1.20 |   15.26% |   1.2751 |   -18.94% |    2.824 |  True  True  | True  False| -
       1.25 |   15.91% |   1.2749 |   -19.69% |    2.944 |  True  True  | True  False| -
       1.30 |   16.56% |   1.2747 |   -20.43% |    3.064 |  True  False | False False| L4_DD
       1.35 |   17.21% |   1.2745 |   -21.17% |    3.186 |  True  False | False False| L4_DD
       1.40 |   17.86% |   1.2743 |   -21.91% |    3.309 |  True  False | False False| L4_DD
       1.45 |   18.51% |   1.2741 |   -22.65% |    3.433 |  True  False | False False| L4_DD
       1.50 |   19.16% |   1.2739 |   -23.38% |    3.558 |  True  False | False False| L4_DD

  --- B136 --- SPY: CAGR  15.16% (full) /  15.33% (OOS), MaxDD -33.72%, OOS Sharpe 0.8769
      4b size bars: OOS CAGR >=  10.61%   |OOS MaxDD| <=  20.23%
      gross | OOS CAGR | OOS Shrp | OOS MaxDD |  turn/yr | CAGRleg DDleg | 4b   4a  | fail legs
       0.25 |    2.62% |   1.1079 |    -4.16% |    0.687 |  False True  | False False| L5_CAGR
       0.30 |    3.14% |   1.1077 |    -4.98% |    0.821 |  False True  | False False| L5_CAGR
       0.35 |    3.67% |   1.1076 |    -5.80% |    0.956 |  False True  | False False| L5_CAGR
       0.40 |    4.20% |   1.1074 |    -6.62% |    1.089 |  False True  | False False| L5_CAGR
       0.45 |    4.72% |   1.1072 |    -7.43% |    1.222 |  False True  | False False| L5_CAGR
       0.50 |    5.25% |   1.1071 |    -8.24% |    1.354 |  False True  | False False| L5_CAGR
       0.55 |    5.78% |   1.1069 |    -9.05% |    1.486 |  False True  | False False| L5_CAGR
       0.60 |    6.30% |   1.1067 |    -9.85% |    1.618 |  False True  | False False| L5_CAGR
       0.65 |    6.83% |   1.1065 |   -10.65% |    1.749 |  False True  | False False| L5_CAGR
       0.70 |    7.36% |   1.1063 |   -11.45% |    1.880 |  False True  | False False| L5_CAGR
       0.75 |    7.88% |   1.1061 |   -12.24% |    2.011 |  False True  | False False| L5_CAGR <== INCUMBENT
       0.80 |    8.41% |   1.1059 |   -13.03% |    2.142 |  False True  | False False| L5_CAGR
       0.85 |    8.94% |   1.1057 |   -13.82% |    2.273 |  False True  | False False| L5_CAGR
       0.90 |    9.47% |   1.1055 |   -14.60% |    2.403 |  False True  | False False| L5_CAGR
       0.95 |   10.00% |   1.1053 |   -15.38% |    2.535 |  False True  | False False| L5_CAGR
       1.00 |   10.52% |   1.1050 |   -16.16% |    2.666 |  False True  | False False| L5_CAGR
       1.05 |   11.05% |   1.1048 |   -16.93% |    2.798 |  True  True  | True  False| -
       1.10 |   11.58% |   1.1046 |   -17.70% |    2.930 |  True  True  | True  False| -
       1.15 |   12.11% |   1.1043 |   -18.47% |    3.063 |  True  True  | True  False| -
       1.20 |   12.63% |   1.1040 |   -19.23% |    3.197 |  True  True  | True  False| -
       1.25 |   13.16% |   1.1038 |   -19.99% |    3.331 |  True  True  | True  False| -
       1.30 |   13.69% |   1.1035 |   -20.75% |    3.466 |  True  False | False False| L4_DD
       1.35 |   14.22% |   1.1032 |   -21.50% |    3.602 |  True  False | False False| L4_DD
       1.40 |   14.74% |   1.1030 |   -22.26% |    3.739 |  True  False | False False| L4_DD
       1.45 |   15.27% |   1.1027 |   -23.00% |    3.878 |  True  False | False False| L4_DD
       1.50 |   15.79% |   1.1024 |   -23.75% |    4.017 |  True  False | False False| L4_DD

  --- SMALL --- SPY: CAGR  14.06% (full) /  15.33% (OOS), MaxDD -33.72%, OOS Sharpe 0.8769
      4b size bars: OOS CAGR >=   9.84%   |OOS MaxDD| <=  20.23%
      gross | OOS CAGR | OOS Shrp | OOS MaxDD |  turn/yr | CAGRleg DDleg | 4b   4a  | fail legs
       0.25 |    1.29% |   0.5605 |    -4.80% |    0.870 |  False True  | False False| L1_H1,L2_H2,L3_OOS,L5_CAGR
       0.30 |    1.54% |   0.5605 |    -5.74% |    1.043 |  False True  | False False| L1_H1,L2_H2,L3_OOS,L5_CAGR
       0.35 |    1.80% |   0.5605 |    -6.67% |    1.215 |  False True  | False False| L1_H1,L2_H2,L3_OOS,L5_CAGR
       0.40 |    2.05% |   0.5604 |    -7.60% |    1.387 |  False True  | False False| L1_H1,L2_H2,L3_OOS,L5_CAGR
       0.45 |    2.30% |   0.5604 |    -8.52% |    1.558 |  False True  | False False| L1_H1,L2_H2,L3_OOS,L5_CAGR
       0.50 |    2.54% |   0.5604 |    -9.43% |    1.729 |  False True  | False False| L1_H1,L2_H2,L3_OOS,L5_CAGR
       0.55 |    2.79% |   0.5603 |   -10.33% |    1.900 |  False True  | False False| L1_H1,L2_H2,L3_OOS,L5_CAGR
       0.60 |    3.03% |   0.5603 |   -11.23% |    2.071 |  False True  | False False| L1_H1,L2_H2,L3_OOS,L5_CAGR
       0.65 |    3.27% |   0.5602 |   -12.13% |    2.242 |  False True  | False False| L1_H1,L2_H2,L3_OOS,L5_CAGR
       0.70 |    3.51% |   0.5602 |   -13.01% |    2.412 |  False True  | False False| L1_H1,L2_H2,L3_OOS,L5_CAGR
       0.75 |    3.75% |   0.5601 |   -13.89% |    2.582 |  False True  | False False| L1_H1,L2_H2,L3_OOS,L5_CAGR <== INCUMBENT
       0.80 |    3.99% |   0.5601 |   -14.76% |    2.752 |  False True  | False False| L1_H1,L2_H2,L3_OOS,L5_CAGR
       0.85 |    4.22% |   0.5600 |   -15.63% |    2.923 |  False True  | False False| L1_H1,L2_H2,L3_OOS,L5_CAGR
       0.90 |    4.46% |   0.5600 |   -16.49% |    3.093 |  False True  | False False| L1_H1,L2_H2,L3_OOS,L5_CAGR
       0.95 |    4.69% |   0.5599 |   -17.34% |    3.263 |  False True  | False False| L1_H1,L2_H2,L3_OOS,L5_CAGR
       1.00 |    4.92% |   0.5599 |   -18.19% |    3.433 |  False True  | False False| L1_H1,L2_H2,L3_OOS,L5_CAGR
       1.05 |    5.15% |   0.5598 |   -19.03% |    3.603 |  False True  | False False| L1_H1,L2_H2,L3_OOS,L5_CAGR
       1.10 |    5.37% |   0.5598 |   -19.87% |    3.774 |  False True  | False False| L1_H1,L2_H2,L3_OOS,L5_CAGR
       1.15 |    5.59% |   0.5597 |   -20.69% |    3.945 |  False False | False False| L1_H1,L2_H2,L3_OOS,L4_DD,L5_CAGR
       1.20 |    5.82% |   0.5596 |   -21.51% |    4.115 |  False False | False False| L1_H1,L2_H2,L3_OOS,L4_DD,L5_CAGR
       1.25 |    6.04% |   0.5595 |   -22.33% |    4.286 |  False False | False False| L1_H1,L2_H2,L3_OOS,L4_DD,L5_CAGR
       1.30 |    6.25% |   0.5595 |   -23.14% |    4.458 |  False False | False False| L1_H1,L2_H2,L3_OOS,L4_DD,L5_CAGR
       1.35 |    6.47% |   0.5594 |   -23.94% |    4.630 |  False False | False False| L1_H1,L2_H2,L3_OOS,L4_DD,L5_CAGR
       1.40 |    6.68% |   0.5593 |   -24.74% |    4.802 |  False False | False False| L1_H1,L2_H2,L3_OOS,L4_DD,L5_CAGR
       1.45 |    6.90% |   0.5592 |   -25.53% |    4.974 |  False False | False False| L1_H1,L2_H2,L3_OOS,L4_DD,L5_CAGR
       1.50 |    7.11% |   0.5592 |   -26.31% |    5.147 |  False False | False False| L1_H1,L2_H2,L3_OOS,L4_DD,L5_CAGR

====================================================================================================
(D) THE WINDOW -- g_CAGR (smallest rung clearing the floor) vs g_DD (largest clearing the cap)
====================================================================================================
  U56    g_CAGR  0.85   g_DD  1.25   window NON-EMPTY  width  0.40   4b passes  9 of 26 rungs  [0.85 .. 1.25]   4a passes  0
         ALL-OOS leg reading: g_CAGR  0.85  g_DD  1.25  NON-EMPTY
  B136   g_CAGR  1.05   g_DD  1.25   window NON-EMPTY  width  0.20   4b passes  5 of 26 rungs  [1.05 .. 1.25]   4a passes  0
         ALL-OOS leg reading: g_CAGR  1.05  g_DD  1.25  NON-EMPTY
  SMALL  g_CAGR   nan   g_DD  1.10   window EMPTY      width   nan   4b passes  0 of 26 rungs   4a passes  0
         ALL-OOS leg reading: g_CAGR   nan  g_DD  1.10  EMPTY
  wrote 2026-09-16_price-the-LIVE-BOOK-as-a-STANDING-4b-COMPARAND_C.window.csv  (3 rows, 14 cols)

====================================================================================================
(E) RULE 8 WALK-FORWARD -- the gross rung chosen on 2009-2016 ALONE, scored on 2017-2026
    3 panels x 3 pre-declared IS choosers = 9 slots.  A chooser that picks nothing is
    NOT dropped (idea 993's lesson): it is scored holding the INCUMBENT 0.75.
====================================================================================================
  U56    C_ISSHARPE  pick 1.50         OOS CAGR  19.16%  Sharpe 1.2739  MaxDD -23.38%  4b False 4a False | L4_DD
  U56    C_ISCAGR    pick 1.50         OOS CAGR  19.16%  Sharpe 1.2739  MaxDD -23.38%  4b False 4a False | L4_DD
  U56    C_IS4B      pick 1.05         OOS CAGR  13.31%  Sharpe 1.2756  MaxDD -16.67%  4b True  4a False | -
  B136   C_ISSHARPE  pick 1.50         OOS CAGR  15.79%  Sharpe 1.1024  MaxDD -23.75%  4b False 4a False | L4_DD
  B136   C_ISCAGR    pick 1.50         OOS CAGR  15.79%  Sharpe 1.1024  MaxDD -23.75%  4b False 4a False | L4_DD
  B136   C_IS4B      pick 1.00         OOS CAGR  10.52%  Sharpe 1.1050  MaxDD -16.16%  4b False 4a False | L5_CAGR
  SMALL  C_ISSHARPE  pick 1.50         OOS CAGR   7.11%  Sharpe 0.5592  MaxDD -26.31%  4b False 4a False | L1_H1,L2_H2,L3_OOS,L4_DD,L5_CAGR
  SMALL  C_ISCAGR    pick 1.50         OOS CAGR   7.11%  Sharpe 0.5592  MaxDD -26.31%  4b False 4a False | L1_H1,L2_H2,L3_OOS,L4_DD,L5_CAGR
  SMALL  C_IS4B      pick NONE(->0.75) OOS CAGR   3.75%  Sharpe 0.5601  MaxDD -13.89%  4b False 4a False | L1_H1,L2_H2,L3_OOS,L5_CAGR
  wrote 2026-09-16_price-the-LIVE-BOOK-as-a-STANDING-4b-COMPARAND_C.rule8.csv  (9 rows, 17 cols)
  RULE 8 TOTALS: OOS 4b 1 of 9 slots   OOS 4a 0 of 9   (incumbent-0.75 reference: 4b 0 of 3)
  OOS comparands, per panel (incumbent live book at 0.75 / SPY):
    U56    live@0.75 CAGR   9.45% Sharpe 1.2765 MaxDD -12.05%  |  SPY CAGR  15.21% Sharpe 0.8713 MaxDD -33.72%
    B136   live@0.75 CAGR   7.88% Sharpe 1.1061 MaxDD -12.24%  |  SPY CAGR  15.33% Sharpe 0.8769 MaxDD -33.72%
    SMALL  live@0.75 CAGR   3.75% Sharpe 0.5601 MaxDD -13.89%  |  SPY CAGR  15.33% Sharpe 0.8769 MaxDD -33.72%

====================================================================================================
(F) ROBUSTNESS COLUMNS -- reported, selected on by nothing
====================================================================================================

  (F1) FINANCING: the same headline cell with 200 bps/yr charged on the levered fraction
    U56    g_CAGR  0.85  g_DD  1.25  NON-EMPTY  4b  9 rungs [0.85..1.25]  max financing drag 32.3 bps/yr
    B136   g_CAGR  1.05  g_DD  1.25  NON-EMPTY  4b  5 rungs [1.05..1.25]  max financing drag 31.3 bps/yr
    SMALL  g_CAGR   nan  g_DD  1.10  EMPTY  4b  0 rungs  max financing drag 7.0 bps/yr
  wrote 2026-09-16_price-the-LIVE-BOOK-as-a-STANDING-4b-COMPARAND_C.financing.csv  (3 rows, 8 cols)

  (F2) PHASE: all 5 weekly phases at 10 bps, zero-borrow.  The record's L4_DD leg is a
       known phase coin-flip, so the window is reported per phase and as a phase median.
    U56    g_CAGR ['0.85', '0.90', '0.85', '0.85', '0.85']  g_DD ['1.25', '1.20', '1.45', '1.40', '1.35']  non-empty 5 of 5 phases   4b rungs [9, 7, 13, 12, 11]
    B136   g_CAGR ['1.05', '1.05', '1.00', '1.00', '1.05']  g_DD ['1.25', '1.20', '1.40', '1.35', '1.35']  non-empty 5 of 5 phases   4b rungs [5, 4, 9, 8, 7]
    SMALL  g_CAGR ['nan', 'nan', 'nan', 'nan', 'nan']  g_DD ['1.10', '1.10', '1.15', '1.15', '1.10']  non-empty 0 of 5 phases   4b rungs [0, 0, 0, 0, 0]
  wrote 2026-09-16_price-the-LIVE-BOOK-as-a-STANDING-4b-COMPARAND_C.phase.csv  (15 rows, 6 cols)

  (F3) CADENCE (phase 0, 10 bps, zero-borrow) -- D / W / M / Q, published beside the
       headline and selected on by nothing
    U56    D:[0.90,1.40] 4b 11  W:[0.85,1.25] 4b  9  M:[0.85,1.05] 4b  5  Q:[0.95,0.75] 4b  0
    B136   D:[1.05,1.40] 4b  8  W:[1.05,1.25] 4b  5  M:[1.00,0.95] 4b  0  Q:[1.05,0.65] 4b  0
    SMALL  D:[nan,1.20] 4b  0  W:[nan,1.10] 4b  0  M:[nan,0.90] 4b  0  Q:[nan,0.60] 4b  0
  wrote 2026-09-16_price-the-LIVE-BOOK-as-a-STANDING-4b-COMPARAND_C.cadence.csv  (12 rows, 6 cols)

  (F4) COST RUNGS (W, phase 0, zero-borrow) -- 4b-passing rung count at each rung
    U56    0bps:[0.85,1.25] 4b  9  5bps:[0.85,1.25] 4b  9  10bps:[0.85,1.25] 4b  9  25bps:[0.90,1.25] 4b  8  50bps:[0.95,1.25] 4b  7
    B136   0bps:[1.00,1.25] 4b  6  5bps:[1.00,1.25] 4b  6  10bps:[1.05,1.25] 4b  5  25bps:[1.10,1.25] 4b  4  50bps:[1.15,1.25] 4b  3
    SMALL  0bps:[nan,1.15] 4b  0  5bps:[nan,1.10] 4b  0  10bps:[nan,1.10] 4b  0  25bps:[nan,1.05] 4b  0  50bps:[nan,1.00] 4b  0
  wrote 2026-09-16_price-the-LIVE-BOOK-as-a-STANDING-4b-COMPARAND_C.cost.csv  (15 rows, 5 cols)

====================================================================================================
(G) PRE-REGISTERED HYPOTHESES
====================================================================================================
  H_WINDOW       PASS   non-empty on 2 of 3 panels (U56, B136)
  H_PANEL        FAIL   non-empty on 2 of 3
  H_INCUMBENT    PASS   incumbent 0.75 below the window on 2 of 2 non-empty panels; inside it on 0
  H_4B           PASS   14 of 78 (panel,gross) points pass full OOS 4b
  H_4A           FAIL   0 of 78 points clear 4a against RULES v2 (pre-declared expected FAIL)
  H_R8           PASS   1 of 9 rule-8 slots pass OOS 4b
  H_R8_ALL       FAIL   1 of 6 slots on the non-empty panels
  H_SHARPE_FLAT  PASS   max |OOS Sharpe(g) - OOS Sharpe(0.75)| over the ladder = 0.0037 (idea 948's cancellation band 0.005)
  H_MONO         PASS   OOS CAGR and |OOS MaxDD| monotone in gross
  H_BORROW       PASS   window non-empty on 2 of 3 panels once financing is charged (zero-borrow: 2)
  H_PHASE        PASS   10 of 15 (panel,phase) cells non-empty; on the non-empty panels all phases agree
  H_LEGDEF       PASS   record and ALL-OOS leg readings agree on all 3 panels
  wrote 2026-09-16_price-the-LIVE-BOOK-as-a-STANDING-4b-COMPARAND_C.hypotheses.csv  (12 rows, 5 cols)

====================================================================================================
(H) VERDICT
====================================================================================================
  KEEP path 4a : REFUSED -- 0 of 78 rungs
  KEEP path 4b : 14 of 78 rungs pass full sample OOS; 1 of 9 rule-8 slots pass
  GATES        : 10 of 10
  VERDICT      : KEEP-candidate (4b)
  elapsed 59s
```

Memo with the proposed RULES wording: `2026-09-16_price-the-LIVE-BOOK-as-a-STANDING-4b-COMPARAND_C.memo.md`.

_Research, not investment advice. Survivorship: U56/B136/SMALL are current-constituent lists; this run measures LEVELS, so both crossings are optimistic and any window here is an UPPER bound on the true one._
