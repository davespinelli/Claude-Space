====================================================================================================
IDEA 586 - does the IS-side EPISODE MISMATCH move any published rule-8 pick?
           (cloud, 2026-09-09)
====================================================================================================
load_prices: network unavailable (ModuleNotFoundError); using prices.csv
panel U56        4700 days x   55 names + SPY  2008-01-02 .. 2026-09-08
load_prices: network unavailable (ModuleNotFoundError); using prices.csv
panel B136       4699 days x  135 names + SPY  2008-01-02 .. 2026-09-04
  SMALL panel: dropped 44 tickers with max_1d_move >= 1.0 (data errors, per data/SMALL_PANEL_README.md)
panel SMALL439   4194 days x  439 names + SPY  2010-01-04 .. 2026-09-04

--- G1  fast_backtest vs engine.backtest (4 real books) ---
  v2 band 0.03 g0.75 W     max|diff| = 1.041e-17
  band 0.00 g1.00 W        max|diff| = 2.082e-17
  band 0.10 g0.50 M        max|diff| = 6.939e-18
  band 0.20 g0.25 M        max|diff| = 3.469e-18
  G1 PASS (bar 1e-12, worst 2.082e-17)

--- G2  band_book(0.03, 0.75) nests baseline.rules_v2_weights ---
  max|diff| = 0.000e+00   G2 PASS (bar exactly 0.0)

--- building the book grid (7 bands x 4 gross x 2 cadences x 3 panels) ---
  U56: 56 books
  B136: 56 books
  SMALL439: 56 books

--- G3  episode identity: max over disjoint episodes == MaxDD (exactly) ---
  max|episode-max - MaxDD| = 0.000e+00   G3 PASS

--- G4  structural relation between the conventions ---
  G4a SPY arm nests at theta->0 : max|CE bar - RAW bar| = 2.776e-16  PASS (bar 1e-12)
  G4a2 CE bar only tightens : max(CE bar - RAW bar) = 1.388e-16  PASS (must be <= 0)
  G4b book arm is a subwindow reading: max(book_CE - book_RAW) = 1.110e-15  PASS (must be <= 0)
      equality (book's worst DD sits inside a SPY span) on 120/308 = 39.0% of book x theta cells
      => CE tightens BOTH sides of the inequality; the direction of any verdict
         change is therefore NOT fixed by construction (see Part 2).

====================================================================================================
PART 1  REPRODUCE THE DEFECT - whose episode sets each side of the IS DD bar?
====================================================================================================
  336 grid points written to 2026-09-09_does-the-IS-side-EPISODE-MISMATCH-move-any-published-rule-8-pick_cloud.grid.csv

  IS worst-episode year, book vs SPY (PROTO cost rung, both cadences):
    U56       book modal IS worst year 2011 on 56/56 (100%)  {2011: np.int64(56)}   |  SPY's own IS worst year 2009   MISMATCH on 100%
    B136      book modal IS worst year 2011 on 43/56 (77%)  {2011: np.int64(43), 2010: np.int64(13)}   |  SPY's own IS worst year 2009   MISMATCH on 100%
    SMALL439  book modal IS worst year 2012 on 40/56 (71%)  {2012: np.int64(40), 2011: np.int64(16)}   |  SPY's own IS worst year 2011   MISMATCH on 71%

  H_MISMATCH (FAILS): min panel mismatch share 71% vs an 80% bar

  The IS DD bar itself, RAW vs CE (pp of drawdown allowed), PROTO rung:
    U56       RAW bar  13.24 pp   CE0.08  13.24   CE0.1  13.24   CE0.15  13.24   CE0.2  13.24   | book IS DD median  7.31 pp
    B136      RAW bar  13.24 pp   CE0.08  13.24   CE0.1  13.24   CE0.15  13.24   CE0.2  13.24   | book IS DD median  7.49 pp
    SMALL439  RAW bar  11.16 pp   CE0.08  11.16   CE0.1  11.16   CE0.15  11.16   CE0.2    nan   | book IS DD median  8.00 pp

  WHY CE moves nothing - the live-start filter excludes no episode:
    U56       book live-start: 2009-01-13 .. 2009-01-13   IS episodes at theta=0.1: 4 total, 0 excluded by live-start
    B136      book live-start: 2009-01-13 .. 2009-01-13   IS episodes at theta=0.1: 4 total, 0 excluded by live-start
    SMALL439  book live-start: 2011-01-13 .. 2011-01-13   IS episodes at theta=0.1: 2 total, 0 excluded by live-start
    => the two arms already read the SAME episode set; what differs is only WHICH
       episode each arm takes its maximum on.  That is what EM removes.

  EM (episode-matched) worst ratio  |book DD in e| / (0.60*|SPY DD in e|), PROTO rung:
    U56       median  0.67  IQR [0.44, 0.95]  max  1.26   binding-episode year {2010: np.int64(29), 2011: np.int64(19), 2016: np.int64(8)}  binding SPY depth median 15.7 pp
    B136      median  0.74  IQR [0.50, 1.00]  max  1.28   binding-episode year {2010: np.int64(56)}  binding SPY depth median 15.7 pp
    SMALL439  median  0.71  IQR [0.46, 0.99]  max  1.33   binding-episode year {2011: np.int64(40), 2016: np.int64(16)}  binding SPY depth median 18.6 pp

  IS THE EM BITE A SHALLOW-EPISODE ARTEFACT?  binding episode depth by theta:
    theta=0.08  EM fails  67/168   binding SPY depth on the FAILURES: median   9.7 pp  min   9.7 pp   binding years {2012: np.int64(54), 2011: np.int64(6), 2010: np.int64(5)}
    theta=0.10  EM fails  39/168   binding SPY depth on the FAILURES: median  15.7 pp  min  13.0 pp   binding years {2010: np.int64(19), 2011: np.int64(14), 2016: np.int64(6)}
    theta=0.15  EM fails  37/168   binding SPY depth on the FAILURES: median  15.7 pp  min  15.7 pp   binding years {2010: np.int64(19), 2011: np.int64(18)}
    theta=0.20  EM fails   0/112   binding SPY depth on the FAILURES: median   nan pp  min   nan pp   binding years {}
    A ratio test on a SHALLOW episode is mechanically harsh (0.60 x 8 pp = 4.8 pp of
    allowance), so the theta ladder is reported in full and theta=0.15 - where the
    binding episodes are SPY's real 2010/2011 selloffs - is the honest reading.

  H_BAR (FAILS): median bar falls 0.00 pp at theta=0.1 vs a 5 pp bar

====================================================================================================
PART 2  DOES THE RE-BASING CHANGE THE IS DD-GATE VERDICT?  (all grid points)
====================================================================================================
 theta   cost   n  undefined  RAW_pass  CE_pass  CE_flips  CE_flip_rate  EM_n  EM_pass  EM_flips  EM_flip_rate  raw_pass_EM_fail  raw_fail_EM_pass
 0.080 10.000 168          0       143      147         4         0.024   168      101        42         0.250                42                 0
 0.080 25.000 168          0       139      147         8         0.048   168      101        38         0.226                38                 0
 0.100 10.000 168          0       143      147         4         0.024   168      129        20         0.119                17                 3
 0.100 25.000 168          0       139      147         8         0.048   168      128        19         0.113                15                 4
 0.150 10.000 168          0       143      147         4         0.024   168      131        18         0.107                15                 3
 0.150 25.000 168          0       139      147         8         0.048   168      131        22         0.131                15                 7
 0.200 10.000 112         56       102      112        10         0.089   112      112        10         0.089                 0                10
 0.200 25.000 112         56       102      112        10         0.089   112      112        10         0.089                 0                10

  H_VERDICT (HOLDS): EM flip rate 11.9% (CE 2.4%) at theta=0.1, 10 bps, vs a 10% bar

====================================================================================================
PART 3  RULE 8 - does any pick MOVE?  chooser sees IS only; OOS read once
====================================================================================================
  U56       10bps RAW      pick b=0.10 g=1.00 (of  3 IS-eligible)  OOS 12.37%/1.216/-16.10%  | v2  9.54%/1.290 | SPY 15.38%/0.879  4a False 4b True (-)
  U56       10bps CE0.08   pick b=0.10 g=1.00 (of  3 IS-eligible)  OOS 12.37%/1.216/-16.10%  | v2  9.54%/1.290 | SPY 15.38%/0.879  4a False 4b True (-)
  U56       10bps CE0.1    pick b=0.10 g=1.00 (of  3 IS-eligible)  OOS 12.37%/1.216/-16.10%  | v2  9.54%/1.290 | SPY 15.38%/0.879  4a False 4b True (-)
  U56       10bps CE0.15   pick b=0.10 g=1.00 (of  3 IS-eligible)  OOS 12.37%/1.216/-16.10%  | v2  9.54%/1.290 | SPY 15.38%/0.879  4a False 4b True (-)
  U56       10bps CE0.2    pick b=0.10 g=1.00 (of  4 IS-eligible)  OOS 12.37%/1.216/-16.10%  | v2  9.54%/1.290 | SPY 15.38%/0.879  4a False 4b True (-)
  U56       10bps EM0.08   no (b,g) clears the IS 4b legs
  U56       10bps EM0.1    no (b,g) clears the IS 4b legs
  U56       10bps EM0.15   no (b,g) clears the IS 4b legs
  U56       10bps EM0.2    pick b=0.10 g=1.00 (of  4 IS-eligible)  OOS 12.37%/1.216/-16.10%  | v2  9.54%/1.290 | SPY 15.38%/0.879  4a False 4b True (-)
  U56       25bps RAW      pick b=0.10 g=1.00 (of  2 IS-eligible)  OOS 12.13%/1.195/-16.11%  | v2  9.24%/1.253 | SPY 15.38%/0.879  4a False 4b True (-)
  U56       25bps CE0.08   pick b=0.10 g=1.00 (of  2 IS-eligible)  OOS 12.13%/1.195/-16.11%  | v2  9.24%/1.253 | SPY 15.38%/0.879  4a False 4b True (-)
  U56       25bps CE0.1    pick b=0.10 g=1.00 (of  2 IS-eligible)  OOS 12.13%/1.195/-16.11%  | v2  9.24%/1.253 | SPY 15.38%/0.879  4a False 4b True (-)
  U56       25bps CE0.15   pick b=0.10 g=1.00 (of  2 IS-eligible)  OOS 12.13%/1.195/-16.11%  | v2  9.24%/1.253 | SPY 15.38%/0.879  4a False 4b True (-)
  U56       25bps CE0.2    pick b=0.10 g=1.00 (of  3 IS-eligible)  OOS 12.13%/1.195/-16.11%  | v2  9.24%/1.253 | SPY 15.38%/0.879  4a False 4b True (-)
  U56       25bps EM0.08   no (b,g) clears the IS 4b legs
  U56       25bps EM0.1    no (b,g) clears the IS 4b legs
  U56       25bps EM0.15   no (b,g) clears the IS 4b legs
  U56       25bps EM0.2    pick b=0.10 g=1.00 (of  3 IS-eligible)  OOS 12.13%/1.195/-16.11%  | v2  9.24%/1.253 | SPY 15.38%/0.879  4a False 4b True (-)
  B136      10bps RAW      pick b=0.10 g=1.00 (of  4 IS-eligible)  OOS 11.27%/1.110/-19.14%  | v2  7.98%/1.121 | SPY 15.45%/0.882  4a False 4b True (-)
  B136      10bps CE0.08   pick b=0.10 g=1.00 (of  4 IS-eligible)  OOS 11.27%/1.110/-19.14%  | v2  7.98%/1.121 | SPY 15.45%/0.882  4a False 4b True (-)
  B136      10bps CE0.1    pick b=0.10 g=1.00 (of  4 IS-eligible)  OOS 11.27%/1.110/-19.14%  | v2  7.98%/1.121 | SPY 15.45%/0.882  4a False 4b True (-)
  B136      10bps CE0.15   pick b=0.10 g=1.00 (of  4 IS-eligible)  OOS 11.27%/1.110/-19.14%  | v2  7.98%/1.121 | SPY 15.45%/0.882  4a False 4b True (-)
  B136      10bps CE0.2    pick b=0.10 g=1.00 (of  6 IS-eligible)  OOS 11.27%/1.110/-19.14%  | v2  7.98%/1.121 | SPY 15.45%/0.882  4a False 4b True (-)
  B136      10bps EM0.08   no (b,g) clears the IS 4b legs
  B136      10bps EM0.1    no (b,g) clears the IS 4b legs
  B136      10bps EM0.15   no (b,g) clears the IS 4b legs
  B136      10bps EM0.2    pick b=0.10 g=1.00 (of  6 IS-eligible)  OOS 11.27%/1.110/-19.14%  | v2  7.98%/1.121 | SPY 15.45%/0.882  4a False 4b True (-)
  B136      25bps RAW      pick b=0.10 g=1.00 (of  3 IS-eligible)  OOS 11.01%/1.086/-19.16%  | v2  7.64%/1.076 | SPY 15.45%/0.882  4a False 4b True (-)
  B136      25bps CE0.08   pick b=0.10 g=1.00 (of  3 IS-eligible)  OOS 11.01%/1.086/-19.16%  | v2  7.64%/1.076 | SPY 15.45%/0.882  4a False 4b True (-)
  B136      25bps CE0.1    pick b=0.10 g=1.00 (of  3 IS-eligible)  OOS 11.01%/1.086/-19.16%  | v2  7.64%/1.076 | SPY 15.45%/0.882  4a False 4b True (-)
  B136      25bps CE0.15   pick b=0.10 g=1.00 (of  3 IS-eligible)  OOS 11.01%/1.086/-19.16%  | v2  7.64%/1.076 | SPY 15.45%/0.882  4a False 4b True (-)
  B136      25bps CE0.2    pick b=0.10 g=1.00 (of  5 IS-eligible)  OOS 11.01%/1.086/-19.16%  | v2  7.64%/1.076 | SPY 15.45%/0.882  4a False 4b True (-)
  B136      25bps EM0.08   no (b,g) clears the IS 4b legs
  B136      25bps EM0.1    no (b,g) clears the IS 4b legs
  B136      25bps EM0.15   no (b,g) clears the IS 4b legs
  B136      25bps EM0.2    pick b=0.10 g=1.00 (of  5 IS-eligible)  OOS 11.01%/1.086/-19.16%  | v2  7.64%/1.076 | SPY 15.45%/0.882  4a False 4b True (-)
  SMALL439  10bps RAW      no (b,g) clears the IS 4b legs
  SMALL439  10bps CE0.08   no (b,g) clears the IS 4b legs
  SMALL439  10bps CE0.1    no (b,g) clears the IS 4b legs
  SMALL439  10bps CE0.15   no (b,g) clears the IS 4b legs
  SMALL439  10bps CE0.2    no (b,g) clears the IS 4b legs
  SMALL439  10bps EM0.08   no (b,g) clears the IS 4b legs
  SMALL439  10bps EM0.1    no (b,g) clears the IS 4b legs
  SMALL439  10bps EM0.15   no (b,g) clears the IS 4b legs
  SMALL439  10bps EM0.2    no (b,g) clears the IS 4b legs
  SMALL439  25bps RAW      no (b,g) clears the IS 4b legs
  SMALL439  25bps CE0.08   no (b,g) clears the IS 4b legs
  SMALL439  25bps CE0.1    no (b,g) clears the IS 4b legs
  SMALL439  25bps CE0.15   no (b,g) clears the IS 4b legs
  SMALL439  25bps CE0.2    no (b,g) clears the IS 4b legs
  SMALL439  25bps EM0.08   no (b,g) clears the IS 4b legs
  SMALL439  25bps EM0.1    no (b,g) clears the IS 4b legs
  SMALL439  25bps EM0.15   no (b,g) clears the IS 4b legs
  SMALL439  25bps EM0.2    no (b,g) clears the IS 4b legs

  DID ANY PICK MOVE?  (RAW pick vs each CE pick, same panel and rung)
    U56       10bps  RAW b0.10/g1.00  vs CE0.08  b0.10/g1.00   SAME
    U56       10bps  RAW b0.10/g1.00  vs CE0.1   b0.10/g1.00   SAME
    U56       10bps  RAW b0.10/g1.00  vs CE0.15  b0.10/g1.00   SAME
    U56       10bps  RAW b0.10/g1.00  vs CE0.2   b0.10/g1.00   SAME
    U56       10bps  RAW b0.10/g1.00  vs EM0.08  NONE ELIGIBLE IS  *** MOVED ***
    U56       10bps  RAW b0.10/g1.00  vs EM0.1   NONE ELIGIBLE IS  *** MOVED ***
    U56       10bps  RAW b0.10/g1.00  vs EM0.15  NONE ELIGIBLE IS  *** MOVED ***
    U56       10bps  RAW b0.10/g1.00  vs EM0.2   b0.10/g1.00   SAME
    U56       25bps  RAW b0.10/g1.00  vs CE0.08  b0.10/g1.00   SAME
    U56       25bps  RAW b0.10/g1.00  vs CE0.1   b0.10/g1.00   SAME
    U56       25bps  RAW b0.10/g1.00  vs CE0.15  b0.10/g1.00   SAME
    U56       25bps  RAW b0.10/g1.00  vs CE0.2   b0.10/g1.00   SAME
    U56       25bps  RAW b0.10/g1.00  vs EM0.08  NONE ELIGIBLE IS  *** MOVED ***
    U56       25bps  RAW b0.10/g1.00  vs EM0.1   NONE ELIGIBLE IS  *** MOVED ***
    U56       25bps  RAW b0.10/g1.00  vs EM0.15  NONE ELIGIBLE IS  *** MOVED ***
    U56       25bps  RAW b0.10/g1.00  vs EM0.2   b0.10/g1.00   SAME
    B136      10bps  RAW b0.10/g1.00  vs CE0.08  b0.10/g1.00   SAME
    B136      10bps  RAW b0.10/g1.00  vs CE0.1   b0.10/g1.00   SAME
    B136      10bps  RAW b0.10/g1.00  vs CE0.15  b0.10/g1.00   SAME
    B136      10bps  RAW b0.10/g1.00  vs CE0.2   b0.10/g1.00   SAME
    B136      10bps  RAW b0.10/g1.00  vs EM0.08  NONE ELIGIBLE IS  *** MOVED ***
    B136      10bps  RAW b0.10/g1.00  vs EM0.1   NONE ELIGIBLE IS  *** MOVED ***
    B136      10bps  RAW b0.10/g1.00  vs EM0.15  NONE ELIGIBLE IS  *** MOVED ***
    B136      10bps  RAW b0.10/g1.00  vs EM0.2   b0.10/g1.00   SAME
    B136      25bps  RAW b0.10/g1.00  vs CE0.08  b0.10/g1.00   SAME
    B136      25bps  RAW b0.10/g1.00  vs CE0.1   b0.10/g1.00   SAME
    B136      25bps  RAW b0.10/g1.00  vs CE0.15  b0.10/g1.00   SAME
    B136      25bps  RAW b0.10/g1.00  vs CE0.2   b0.10/g1.00   SAME
    B136      25bps  RAW b0.10/g1.00  vs EM0.08  NONE ELIGIBLE IS  *** MOVED ***
    B136      25bps  RAW b0.10/g1.00  vs EM0.1   NONE ELIGIBLE IS  *** MOVED ***
    B136      25bps  RAW b0.10/g1.00  vs EM0.15  NONE ELIGIBLE IS  *** MOVED ***
    B136      25bps  RAW b0.10/g1.00  vs EM0.2   b0.10/g1.00   SAME
    SMALL439  10bps  RAW NONE ELIGIBLE IS vs CE0.08  NONE ELIGIBLE IS  SAME
    SMALL439  10bps  RAW NONE ELIGIBLE IS vs CE0.1   NONE ELIGIBLE IS  SAME
    SMALL439  10bps  RAW NONE ELIGIBLE IS vs CE0.15  NONE ELIGIBLE IS  SAME
    SMALL439  10bps  RAW NONE ELIGIBLE IS vs CE0.2   NONE ELIGIBLE IS  SAME
    SMALL439  10bps  RAW NONE ELIGIBLE IS vs EM0.08  NONE ELIGIBLE IS  SAME
    SMALL439  10bps  RAW NONE ELIGIBLE IS vs EM0.1   NONE ELIGIBLE IS  SAME
    SMALL439  10bps  RAW NONE ELIGIBLE IS vs EM0.15  NONE ELIGIBLE IS  SAME
    SMALL439  10bps  RAW NONE ELIGIBLE IS vs EM0.2   NONE ELIGIBLE IS  SAME
    SMALL439  25bps  RAW NONE ELIGIBLE IS vs CE0.08  NONE ELIGIBLE IS  SAME
    SMALL439  25bps  RAW NONE ELIGIBLE IS vs CE0.1   NONE ELIGIBLE IS  SAME
    SMALL439  25bps  RAW NONE ELIGIBLE IS vs CE0.15  NONE ELIGIBLE IS  SAME
    SMALL439  25bps  RAW NONE ELIGIBLE IS vs CE0.2   NONE ELIGIBLE IS  SAME
    SMALL439  25bps  RAW NONE ELIGIBLE IS vs EM0.08  NONE ELIGIBLE IS  SAME
    SMALL439  25bps  RAW NONE ELIGIBLE IS vs EM0.1   NONE ELIGIBLE IS  SAME
    SMALL439  25bps  RAW NONE ELIGIBLE IS vs EM0.15  NONE ELIGIBLE IS  SAME
    SMALL439  25bps  RAW NONE ELIGIBLE IS vs EM0.2   NONE ELIGIBLE IS  SAME

  H_PICK (HOLDS): 12 of 48 (panel x rung x convention) picks move under the re-based bar

  Baselines on the same windows (weekly, next-day, PROTO rung):
    U56       RULES v2 full  8.67%/1.211/-11.90%  H1 1.236 H2 1.192  OOS  9.54%/1.290
              SPY      full 15.19%/0.887/-33.72%  H1 0.959 H2 0.829  OOS 15.38%/0.879
    B136      RULES v2 full  8.03%/1.108/-12.18%  H1 1.231 H2 0.986  OOS  7.98%/1.121
              SPY      full 15.23%/0.889/-33.72%  H1 0.957 H2 0.834  OOS 15.45%/0.882
    SMALL439  RULES v2 full  3.80%/0.571/-14.70%  H1 0.568 H2 0.576  OOS  3.84%/0.566
              SPY      full 14.13%/0.862/-33.72%  H1 0.891 H2 0.858  OOS 15.45%/0.882

====================================================================================================
PART 4  CENSUS - how much of the record's rule-8 output can be re-read FROM DISK?
====================================================================================================
  435 committed *.walkforward.csv files in research/backtests/
    carry an IS-side book MaxDD column      : 18 (4.1%)
    carry an IS-side SPY  MaxDD column      : 0 (0.0%)
    carry BOTH, i.e. their IS DD gate can be re-read from disk without re-running the script: 0
  HONEST LIMIT: the record publishes the PICK and its OOS metrics, not the IS-side
  bar it was chosen under, so 'every committed rule-8 pick' cannot be re-read from
  the committed CSVs.  The rebuild above is the answer that IS available: the same
  chooser, the same book family, the same two dials, run under both conventions.

====================================================================================================
PRE-REGISTERED HYPOTHESES
====================================================================================================
  G1 PASS   G2 PASS   G3 PASS   G4 PASS
  H_MISMATCH  FAILS   (min panel mismatch 71% vs 80%)
  H_BAR       FAILS   (median bar falls 0.00 pp vs 5 pp)
  H_VERDICT   HOLDS   (flip rate 11.9% vs 10%)
  H_PICK      HOLDS   (12/48 picks move)
