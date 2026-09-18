# Idea 904 (lane B, 2026-09-18) — which committed PLACEBO numbers are below their own SEED FLOOR?

```
================================================================================================================
IDEA 904 (lane B, 2026-09-18) — which committed PLACEBO numbers are BELOW their own SEED FLOOR?
CAPITAL ARM: is a PLACEBO-DIFFERENCED chooser, gated on its own seed floor, worth
             anything OUT OF SAMPLE against the RAW IS-Sharpe chooser?
DIALS: S [5, 10, 20, 50] x k [0.0, 0.5, 1.0, 2.0].  Book family frozen: N [5, 10, 15, 20, 25, 30] x H [21, 63, 126, 252], gross 0.75, W, 10 bps, t+1.
================================================================================================================
  SMALL filter (protocol-mandated): data/small_meta.csv drops 52 tickers with max_1d_move >= 1.0 -> 663 investables.
    U56: 2008-01-02 .. 2026-09-17  4707 rows (18.7y), 977 weekly rebalances, 55 investables
    B136: 2008-01-02 .. 2026-09-11  4703 rows (18.7y), 976 weekly rebalances, 135 investables
    SMALL: 2010-01-04 .. 2026-09-11  4198 rows (16.7y), 871 weekly rebalances, 663 investables
  GATE PASS  G0 min sample >= 10 years (rule 1): 16.7y  (target >= 10.0y)

  [U56] SPY full 15.13%/0.8849/-33.72%  -> 4b caps DD -20.23%, CAGR 10.59%;  RULES v2 live 8.62%/1.2018/-12.05%
  [U56] OOS SPY 15.28%/0.8747/-33.72%;  OOS RULES v2 9.47%/1.2781/-12.05%
  [U56] 24 real arms built in 4s
  [U56] 1200 null books done at 34s

  [B136] SPY full 15.16%/0.8862/-33.72%  -> 4b caps DD -20.23%, CAGR 10.61%;  RULES v2 live 7.98%/1.0994/-12.24%
  [B136] OOS SPY 15.33%/0.8769/-33.72%;  OOS RULES v2 7.88%/1.1061/-12.24%
  [B136] 24 real arms built in 36s
  [B136] 1200 null books done at 74s

  [SMALL] SPY full 14.06%/0.8582/-33.72%  -> 4b caps DD -20.23%, CAGR 9.84%;  RULES v2 live 4.64%/0.7130/-12.18%
  [SMALL] OOS SPY 15.33%/0.8769/-33.72%;  OOS RULES v2 4.47%/0.6518/-12.18%
  [SMALL] 24 real arms built in 80s
  [SMALL] 1200 null books done at 141s
  GATE PASS  G1 the null is GROSS-MATCHED (same N, H, gate, gross, days — only the ORDERING differs): build(rand=...) shares every argument with the real arm  (target by construction)
  GATE PASS  G2 the chooser reads NO row at or after 2017-01-01 (rule 8): null frames built with stop=i_oos; X uses r[WARMUP:i_oos] only  (target 0 OOS rows read)
  GATE PASS  G3 measured per-arm null dispersion sigma_hat vs 885's quoted 0.067: 0.1307  (target reported, not assumed)
  GATE PASS  G4 every dial cell published: 48 cells  (target 48 = 48)
  GATE PASS  G5 exactly 2 tuned parameters (rule 4): S, k  (target <= 2)

================================================================================================================
THE MEASUREMENT — is the placebo excess resolvable at all at the record's seed budgets?
================================================================================================================
  measured per-arm null-Sharpe dispersion sigma_hat = 0.1307 (885 assumed 0.067); per-arm floor = 1.2533*sigma/sqrt(S)
    S=  5: typical per-arm floor 0.0733 of Sharpe; arms whose |excess| < floor: U56 5/24, B136 6/24, SMALL 8/24
    S= 10: typical per-arm floor 0.0518 of Sharpe; arms whose |excess| < floor: U56 4/24, B136 4/24, SMALL 8/24
    S= 20: typical per-arm floor 0.0366 of Sharpe; arms whose |excess| < floor: U56 4/24, B136 4/24, SMALL 7/24
    S= 50: typical per-arm floor 0.0232 of Sharpe; arms whose |excess| < floor: U56 3/24, B136 3/24, SMALL 6/24

  per-panel mean placebo excess (real IS Sharpe - null median, 50 seeds):
    U56    mean +0.0849  min -0.0510  max +0.2997  mean null sd 0.1077
    B136   mean +0.1559  min -0.0697  max +0.4893  mean null sd 0.1086
    SMALL  mean -0.0419  min -0.2966  max +0.2800  mean null sd 0.1759

================================================================================================================
THE CAPITAL ANSWER — 48 dial cells + 3 comparands per panel, ALL published
================================================================================================================

  [U56] comparands
    RAW-IS-Sharpe-chooser    pick (5, 63)      full  19.01%/1.0116/-26.26%  OOS  17.95%/0.8996/-26.26%  4a 0 4b 0 | OOS 4b 0
    FROZEN-anchor-N20H126    pick (20, 126)    full  15.78%/1.1522/-19.13%  OOS  17.28%/1.1832/-19.13%  4a 0 4b 1 | OOS 4b 1
    GRIDAVG-no-choice        pick all24        full  15.93%/1.1618/-20.53%  OOS  17.13%/1.1676/-20.53%  4a 0 4b 0 | OOS 4b 0
  [U56] placebo-chooser cells (S x k)
    S=  5 k=0.0  lic 18/24          pick (5, 63)    full  19.01%/1.0116/-26.26%  OOS  17.95%/0.8996/-26.26%  4a 0 4b 0 | OOS 4b 0
    S=  5 k=0.5  lic 18/24          pick (5, 63)    full  19.01%/1.0116/-26.26%  OOS  17.95%/0.8996/-26.26%  4a 0 4b 0 | OOS 4b 0
    S=  5 k=1.0  lic 16/24          pick (5, 63)    full  19.01%/1.0116/-26.26%  OOS  17.95%/0.8996/-26.26%  4a 0 4b 0 | OOS 4b 0
    S=  5 k=2.0  lic  9/24          pick (5, 63)    full  19.01%/1.0116/-26.26%  OOS  17.95%/0.8996/-26.26%  4a 0 4b 0 | OOS 4b 0
    S= 10 k=0.0  lic 20/24          pick (5, 63)    full  19.01%/1.0116/-26.26%  OOS  17.95%/0.8996/-26.26%  4a 0 4b 0 | OOS 4b 0
    S= 10 k=0.5  lic 18/24          pick (5, 63)    full  19.01%/1.0116/-26.26%  OOS  17.95%/0.8996/-26.26%  4a 0 4b 0 | OOS 4b 0
    S= 10 k=1.0  lic 17/24          pick (5, 63)    full  19.01%/1.0116/-26.26%  OOS  17.95%/0.8996/-26.26%  4a 0 4b 0 | OOS 4b 0
    S= 10 k=2.0  lic 12/24          pick (5, 63)    full  19.01%/1.0116/-26.26%  OOS  17.95%/0.8996/-26.26%  4a 0 4b 0 | OOS 4b 0
    S= 20 k=0.0  lic 20/24          pick (5, 63)    full  19.01%/1.0116/-26.26%  OOS  17.95%/0.8996/-26.26%  4a 0 4b 0 | OOS 4b 0
    S= 20 k=0.5  lic 19/24          pick (5, 63)    full  19.01%/1.0116/-26.26%  OOS  17.95%/0.8996/-26.26%  4a 0 4b 0 | OOS 4b 0
    S= 20 k=1.0  lic 18/24          pick (5, 63)    full  19.01%/1.0116/-26.26%  OOS  17.95%/0.8996/-26.26%  4a 0 4b 0 | OOS 4b 0
    S= 20 k=2.0  lic 17/24          pick (5, 63)    full  19.01%/1.0116/-26.26%  OOS  17.95%/0.8996/-26.26%  4a 0 4b 0 | OOS 4b 0
    S= 50 k=0.0  lic 21/24          pick (5, 21)    full  16.84%/0.9263/-25.45%  OOS  15.61%/0.8186/-25.45%  4a 0 4b 0 | OOS 4b 0
    S= 50 k=0.5  lic 19/24          pick (5, 21)    full  16.84%/0.9263/-25.45%  OOS  15.61%/0.8186/-25.45%  4a 0 4b 0 | OOS 4b 0
    S= 50 k=1.0  lic 19/24          pick (5, 21)    full  16.84%/0.9263/-25.45%  OOS  15.61%/0.8186/-25.45%  4a 0 4b 0 | OOS 4b 0
    S= 50 k=2.0  lic 16/24          pick (5, 21)    full  16.84%/0.9263/-25.45%  OOS  15.61%/0.8186/-25.45%  4a 0 4b 0 | OOS 4b 0
  [U56] distinct picks across the 16 cells: ['(5, 21)', '(5, 63)']  (2 of 24 arms ever chosen)

  [B136] comparands
    RAW-IS-Sharpe-chooser    pick (5, 63)      full  23.99%/1.1212/-28.62%  OOS  20.43%/0.9144/-28.62%  4a 0 4b 0 | OOS 4b 0
    FROZEN-anchor-N20H126    pick (20, 126)    full  16.18%/1.0715/-20.74%  OOS  16.29%/1.0240/-20.74%  4a 0 4b 0 | OOS 4b 0
    GRIDAVG-no-choice        pick all24        full  17.39%/1.1297/-24.71%  OOS  17.25%/1.0628/-24.71%  4a 0 4b 0 | OOS 4b 0
  [B136] placebo-chooser cells (S x k)
    S=  5 k=0.0  lic 22/24          pick (10, 21)   full  17.23%/0.9981/-25.61%  OOS  15.18%/0.8435/-25.61%  4a 0 4b 0 | OOS 4b 0
    S=  5 k=0.5  lic 20/24          pick (10, 21)   full  17.23%/0.9981/-25.61%  OOS  15.18%/0.8435/-25.61%  4a 0 4b 0 | OOS 4b 0
    S=  5 k=1.0  lic 17/24          pick (10, 21)   full  17.23%/0.9981/-25.61%  OOS  15.18%/0.8435/-25.61%  4a 0 4b 0 | OOS 4b 0
    S=  5 k=2.0  lic 14/24          pick (10, 21)   full  17.23%/0.9981/-25.61%  OOS  15.18%/0.8435/-25.61%  4a 0 4b 0 | OOS 4b 0
    S= 10 k=0.0  lic 22/24          pick (5, 63)    full  23.99%/1.1212/-28.62%  OOS  20.43%/0.9144/-28.62%  4a 0 4b 0 | OOS 4b 0
    S= 10 k=0.5  lic 20/24          pick (5, 63)    full  23.99%/1.1212/-28.62%  OOS  20.43%/0.9144/-28.62%  4a 0 4b 0 | OOS 4b 0
    S= 10 k=1.0  lic 19/24          pick (5, 63)    full  23.99%/1.1212/-28.62%  OOS  20.43%/0.9144/-28.62%  4a 0 4b 0 | OOS 4b 0
    S= 10 k=2.0  lic 16/24          pick (5, 63)    full  23.99%/1.1212/-28.62%  OOS  20.43%/0.9144/-28.62%  4a 0 4b 0 | OOS 4b 0
    S= 20 k=0.0  lic 22/24          pick (5, 63)    full  23.99%/1.1212/-28.62%  OOS  20.43%/0.9144/-28.62%  4a 0 4b 0 | OOS 4b 0
    S= 20 k=0.5  lic 21/24          pick (5, 63)    full  23.99%/1.1212/-28.62%  OOS  20.43%/0.9144/-28.62%  4a 0 4b 0 | OOS 4b 0
    S= 20 k=1.0  lic 19/24          pick (5, 63)    full  23.99%/1.1212/-28.62%  OOS  20.43%/0.9144/-28.62%  4a 0 4b 0 | OOS 4b 0
    S= 20 k=2.0  lic 17/24          pick (5, 63)    full  23.99%/1.1212/-28.62%  OOS  20.43%/0.9144/-28.62%  4a 0 4b 0 | OOS 4b 0
    S= 50 k=0.0  lic 21/24          pick (5, 63)    full  23.99%/1.1212/-28.62%  OOS  20.43%/0.9144/-28.62%  4a 0 4b 0 | OOS 4b 0
    S= 50 k=0.5  lic 20/24          pick (5, 63)    full  23.99%/1.1212/-28.62%  OOS  20.43%/0.9144/-28.62%  4a 0 4b 0 | OOS 4b 0
    S= 50 k=1.0  lic 20/24          pick (5, 63)    full  23.99%/1.1212/-28.62%  OOS  20.43%/0.9144/-28.62%  4a 0 4b 0 | OOS 4b 0
    S= 50 k=2.0  lic 20/24          pick (5, 63)    full  23.99%/1.1212/-28.62%  OOS  20.43%/0.9144/-28.62%  4a 0 4b 0 | OOS 4b 0
  [B136] distinct picks across the 16 cells: ['(10, 21)', '(5, 63)']  (2 of 24 arms ever chosen)

  [SMALL] comparands
    RAW-IS-Sharpe-chooser    pick (15, 252)    full  14.91%/0.8333/-40.06%  OOS  13.13%/0.7304/-40.06%  4a 0 4b 0 | OOS 4b 0
    FROZEN-anchor-N20H126    pick (20, 126)    full   7.87%/0.5073/-35.81%  OOS   7.09%/0.4534/-35.81%  4a 0 4b 0 | OOS 4b 0
    GRIDAVG-no-choice        pick all24        full  10.12%/0.6377/-37.04%  OOS   8.66%/0.5465/-37.04%  4a 0 4b 0 | OOS 4b 0
  [SMALL] placebo-chooser cells (S x k)
    S=  5 k=0.0  lic  7/24          pick (5, 252)   full  24.72%/1.0143/-45.91%  OOS  26.44%/1.0501/-45.91%  4a 0 4b 0 | OOS 4b 0
    S=  5 k=0.5  lic  7/24          pick (5, 252)   full  24.72%/1.0143/-45.91%  OOS  26.44%/1.0501/-45.91%  4a 0 4b 0 | OOS 4b 0
    S=  5 k=1.0  lic  5/24          pick (5, 252)   full  24.72%/1.0143/-45.91%  OOS  26.44%/1.0501/-45.91%  4a 0 4b 0 | OOS 4b 0
    S=  5 k=2.0  lic  2/24          pick (5, 252)   full  24.72%/1.0143/-45.91%  OOS  26.44%/1.0501/-45.91%  4a 0 4b 0 | OOS 4b 0
    S= 10 k=0.0  lic  9/24          pick (10, 252)  full  17.99%/0.9128/-42.63%  OOS  17.35%/0.8590/-42.63%  4a 0 4b 0 | OOS 4b 0
    S= 10 k=0.5  lic  7/24          pick (10, 252)  full  17.99%/0.9128/-42.63%  OOS  17.35%/0.8590/-42.63%  4a 0 4b 0 | OOS 4b 0
    S= 10 k=1.0  lic  4/24          pick (10, 252)  full  17.99%/0.9128/-42.63%  OOS  17.35%/0.8590/-42.63%  4a 0 4b 0 | OOS 4b 0
    S= 10 k=2.0  lic  2/24          pick (10, 252)  full  17.99%/0.9128/-42.63%  OOS  17.35%/0.8590/-42.63%  4a 0 4b 0 | OOS 4b 0
    S= 20 k=0.0  lic  8/24          pick (10, 252)  full  17.99%/0.9128/-42.63%  OOS  17.35%/0.8590/-42.63%  4a 0 4b 0 | OOS 4b 0
    S= 20 k=0.5  lic  5/24          pick (10, 252)  full  17.99%/0.9128/-42.63%  OOS  17.35%/0.8590/-42.63%  4a 0 4b 0 | OOS 4b 0
    S= 20 k=1.0  lic  4/24          pick (10, 252)  full  17.99%/0.9128/-42.63%  OOS  17.35%/0.8590/-42.63%  4a 0 4b 0 | OOS 4b 0
    S= 20 k=2.0  lic  4/24          pick (10, 252)  full  17.99%/0.9128/-42.63%  OOS  17.35%/0.8590/-42.63%  4a 0 4b 0 | OOS 4b 0
    S= 50 k=0.0  lic  9/24          pick (5, 252)   full  24.72%/1.0143/-45.91%  OOS  26.44%/1.0501/-45.91%  4a 0 4b 0 | OOS 4b 0
    S= 50 k=0.5  lic  8/24          pick (5, 252)   full  24.72%/1.0143/-45.91%  OOS  26.44%/1.0501/-45.91%  4a 0 4b 0 | OOS 4b 0
    S= 50 k=1.0  lic  6/24          pick (5, 252)   full  24.72%/1.0143/-45.91%  OOS  26.44%/1.0501/-45.91%  4a 0 4b 0 | OOS 4b 0
    S= 50 k=2.0  lic  4/24          pick (5, 252)   full  24.72%/1.0143/-45.91%  OOS  26.44%/1.0501/-45.91%  4a 0 4b 0 | OOS 4b 0
  [SMALL] distinct picks across the 16 cells: ['(10, 252)', '(5, 252)']  (2 of 24 arms ever chosen)

  RULE 8 (strict): (S, k) chosen on IS by argmax IS Sharpe of the selected book; 2017-2026 read ONCE.
    [U56] S=5 k=0.0 -> (5, 63)  OOS  17.95%/0.8996/-26.26%  4a 0 4b 0  || RAW chooser OOS Sharpe 0.8996, anchor 1.1832, gridavg 1.1676, SPY 0.8747, RULES v2 1.2781
    [B136] S=10 k=0.0 -> (5, 63)  OOS  20.43%/0.9144/-28.62%  4a 0 4b 0  || RAW chooser OOS Sharpe 0.9144, anchor 1.0240, gridavg 1.0628, SPY 0.8769, RULES v2 1.1061
    [SMALL] S=10 k=0.0 -> (10, 252)  OOS  17.35%/0.8590/-42.63%  4a 0 4b 0  || RAW chooser OOS Sharpe 0.7304, anchor 0.4534, gridavg 0.5465, SPY 0.8769, RULES v2 0.6518

================================================================================================================
THE CENSUS LEG (904's literal ask) — committed placebo numbers vs their own seed floor
================================================================================================================
  FUNNEL (the funnel IS most of the answer):
    NARROW  cued sentences  306 -> carrying a >=4dp decimal  19 -> DIFFERENCES (|x|<0.1)  13 in 10 files -> STAMPED with both a seed count and an arm count   1
    WIDE    cued sentences  386 -> carrying a >=4dp decimal  22 -> DIFFERENCES (|x|<0.1)  17 in 13 files -> STAMPED with both a seed count and an arm count   2
    NARROW  all       n=1, median own-floor 0.00108, median |value| 0.00020
        k=0.5: 1 of 1 (100.0%) INSIDE k x their own floor
        k=1.0: 1 of 1 (100.0%) INSIDE k x their own floor
        k=2.0: 1 of 1 (100.0%) INSIDE k x their own floor
    NARROW  signed   : 0 stamped numbers -> NOTHING in this claim set can be scored against its own floor
    WIDE    all       n=2, median own-floor 0.00071, median |value| 0.00020
        k=0.5: 1 of 2 (50.0%) INSIDE k x their own floor
        k=1.0: 2 of 2 (100.0%) INSIDE k x their own floor
        k=2.0: 2 of 2 (100.0%) INSIDE k x their own floor
    WIDE    signed    n=1, median own-floor 0.00034, median |value| 0.00020
        k=0.5: 0 of 1 (0.0%) INSIDE k x their own floor
        k=1.0: 1 of 1 (100.0%) INSIDE k x their own floor
        k=2.0: 1 of 1 (100.0%) INSIDE k x their own floor

================================================================================================================
VERDICT
================================================================================================================
  [U56] placebo-chooser cells beating the RAW IS-Sharpe chooser OOS: 0/16  (mean OOS Sharpe 0.8793 vs raw 0.8996); 4a 0/16, 4b 0/16, OOS 4b 0/16
  [B136] placebo-chooser cells beating the RAW IS-Sharpe chooser OOS: 0/16  (mean OOS Sharpe 0.8967 vs raw 0.9144); 4a 0/16, 4b 0/16, OOS 4b 0/16
  [SMALL] placebo-chooser cells beating the RAW IS-Sharpe chooser OOS: 16/16  (mean OOS Sharpe 0.9545 vs raw 0.7304); 4a 0/16, 4b 0/16, OOS 4b 0/16
  TOTAL: 16/48 cells beat the raw chooser out of sample; 4a 0/48, 4b 0/48.
```
