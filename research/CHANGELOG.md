## 2026-09-20 — idea 2038 (lane C): DOES THE VOL-TARGET FAMILY'S 4b MARGIN DECOMPOSE INTO A STACK OF DRAWDOWN EPISODES? **ANSWERED — NO. IT IS ONE 23-DAY WINDOW AT 11.5x-40.3x CONCENTRATION, PARTLY CANCELLED BY THE OTHER FOUR; THE STANDING KEEP-4b CANDIDATE IS THE LEAST EPISODE-CONCENTRATED CELL OF THE FOUR PRICED. PLUS A KILL ON READING THE EXCISED VERDICT AS A BOOK FAILURE.**

  **THE QUESTION.** Idea 2022 found ONE 24-day window carrying 89% of the drift-vs-calendar edge.
  Idea 2038 asks the same of the 4b margin AGAINST SPY: excise each OOS SPY peak-to-trough episode
  in turn and cumulatively, and report how much of the standing candidate's OOS Sharpe and CAGR
  margin each one owns.

  **THE CONSTRUCTION.** Four committed vol-target cells, none chosen by this run — `C_KEEP`
  (t=0.10, T=M, R=M, the standing KEEP-4b candidate), `C_MEMO` (t=0.16, T=W, R=W, PARK), `C_GXDD`
  (t=0.08, idea 1793's chooser pick) and `C_ORCL` (t=0.12, R=D, 1793's OOS oracle) — on U56 and
  B136 at 10 bps, t+1, sigma (L=20, d=0). The record's excision convention: days are dropped from
  the STATISTIC for book, SPY and live RULES v2 alike, never from the tape. TUNED (2, every grid
  point published): DEPTH BAR {0.05, 0.10, 0.15, 0.20} x PADDING {0, 5, 10, 20} trading days.
  1,664 scored rows, gates **11/11**; committed memo rows reproduced to max |d| **4.54e-05** and
  the IS half invariant to every excision at exactly **0.000e+00**.

  **H_STACK FALSIFIED (0 of 8 panel x cell pairs).** No single episode owns >= 0.50 of any cell's
  OOS Sharpe margin; the max is **+38.0%** (B136 `C_ORCL`, 2020Q1) and `C_KEEP` reads **+10.8%**
  (U56) / **+13.3%** (B136). But 2020Q1 is 23 days = **0.94%** of the 2,441-day OOS tape, so its
  CONCENTRATION RATIO (margin share / day share) is **11.5x-40.3x**, while every other episode runs
  NEGATIVE on `C_KEEP` and `C_MEMO` — excising 2018Q4, 2025Q1 or 2018-02 RAISES the margin. The
  whole 5-episode stack at b=10% (326d = 13.4% of days) owns only **+19.1% / +24.0%** of `C_KEEP`'s
  +0.4085 / +0.3263 Sharpe margin: **concentration 1.43x / 1.80x, the LOWEST of the four cells**
  (`C_MEMO` 1.17x/1.03x, `C_GXDD` 2.13x/3.69x, `C_ORCL` 3.33x/3.60x). The margin is one window plus
  a drag, not a stack and not an even spread.

  **KILL — "excise the crashes and the book dies" is a BAR SHIFT, not a book failure.** 4b OOS
  flips PASS -> FAIL in **127 of 128** (panel x cell x bar x pad) cells, but the BOOK's OOS Sharpe
  rises **+1.196** (1.2822 -> 2.4778) while SPY's rises **+1.274** (0.8737 -> 2.1472): both legs
  co-move and the margin loses only 0.078 of 0.408. On the other two legs the bar moves ~14 pp each
  — the DD cap `0.60 x SPY` tightens **-20.23% -> -5.98%** and the CAGR floor `0.70 x SPY` rises
  **10.68% -> 25.38%**. This is idea 2034's axis, measured on the 4b legs.

  **H_CAGR CONFIRMED (6 of 8).** The CAGR floor dies first: the stack owns **+80.9%** of `C_KEEP`'s
  U56 OOS CAGR margin (B136 **+110.0%**, it crosses zero) against +19.1% / +24.0% of the Sharpe
  margin. Both `C_MEMO` arms are the exceptions. Resolution caveat stated: B136 `C_GXDD`'s base OOS
  CAGR margin is **+0.47 pp**, so its four-digit CAGR shares are a thin denominator, not a
  measurement; Sharpe denominators run 0.3080-0.4748 and carry no such degeneracy.

  **H_DIAL FALSIFIED, AND BOTH TUNED DIALS ARE LIVE — ONE OF THEM INVERTS.** The four cells' order
  on OOS Sharpe margin is not episode-invariant: **11 / 10 distinct orderings** over 208 (bar x pad
  x mode) cells per panel, modal share only **24.0% / 30.3%**. At b=5% (13 episodes, 476d) the
  all-excision Sharpe share for `C_KEEP` is **NEGATIVE** (-35.9% U56, -43.1% B136); padding raises
  it monotonically at b >= 10% (+19.1% -> +35.8% U56, +24.0% -> +61.8% B136, p=0 to p=20), i.e. the
  edge sits in the RECOVERY leg as much as in the decline.

  **RULE 8 (2017-2026 read ONCE).** Two legal IS-only choosers x two trade cadences x two panels x
  32 (bar x pad): **16 of 128 picks clear 4b OOS un-excised, 0 of 128 with every episode excised,
  0 of 128 clear 4a OOS either way.** Only `C_ISLEGS` on B136 T=M reaches the standing cell (OOS
  13.05% / 1.2000 / -19.87% against SPY 15.26% / 0.8737 / -33.72% and live RULES v2 7.85% / 1.1017
  / -12.24%). The CELL clears, the CHOOSER does not — ideas 1771 / 1803 reconfirmed.

  **WHAT IT CHANGES.** No status move: the standing KEEP-4b candidate stays a KEEP-candidate
  awaiting Sunday review, with an addendum filed on its memo. A companion statistic is now required
  of any future excision claim — publish the CONCENTRATION RATIO and the BOOK-vs-BENCHMARK split of
  the move, because a raw "share of the margin" is a small difference of two large co-moving legs.
  Survivorship: U56 / B136 are CURRENT constituents, so every LEVEL is optimistic; SMALL665 not
  re-run (the family clears 4b 0 of N there, confirmed four times). RULES.md, PROTOCOL.md, scan.py,
  bot.py and baseline.py are untouched. Evidence:
  `research/backtests/2026-09-20_voltgt-4b-margin-episode-stack_C.py` / `.result.md` /
  `.grid.csv` (1,664) / `.decomp.csv` (1,536) / `.walkforward.csv` (256) / `.episodes.csv` /
  `.ladder.csv` / `.gates.csv` / `.log.txt`.

## 2026-09-20 — idea 2022 (lane cloud): IS THE DRIFT TRIGGER'S MATCHED-TURNOVER WIN A DRAWDOWN-TIMING FACT OR A COST FACT? **ANSWERED — A DRAWDOWN-TIMING FACT 24 TRADING DAYS WIDE, AND NOT A COST FACT. IDEA 1799'S "263 OF 263" MUST BE RESTATED AS ONE EPISODE COUNTED 263 TIMES. NO NEW BOOK, NO RULES CHANGE.**

  **THE DEFECT THIS CLOSES.** Idea 1799 (same day, lane C) reported that a DRIFT-THRESHOLD refresh
  beats its own arm's TURNOVER-MATCHED point on the CALENDAR ladder at **263 of 263** cells at 10
  bps, mean OOS Sharpe **+0.0596**. Two of its own tables said that might be one quarter: the win
  decomposed as +4.07 pp of OOS MaxDD against only +0.31 pp of OOS CAGR, and its MECHANISM table
  showed the whole gross gap opening between 2020-02-19 and 2020-03-23. And 1799 published no
  standard error at all — 263 point estimates cannot distinguish 263 independent wins from one win
  counted 263 times.

  **THE CONSTRUCTION.** 1799's corpus is rebuilt verbatim (same runners, same panels, same 420-cell
  grid, same interpolation estimator) and then two readings 1799 did not take: (A) every book's
  daily net return series has the crash window removed and the matched comparison recomputed END TO
  END on the excised tape, so turnover AND Sharpe are both excised and the pairs stay matched on the
  tape they are scored on; (B) a PAIRED moving-block bootstrap in which the whole 13-cell arm is
  resampled on the SAME day blocks, with 1799's estimator held exact (each calendar rung's Sharpe
  re-read on the resampled days, interpolated at the drift book's realised turnover, turnover held
  fixed as a design quantity). B = 1000, seed 20260922. **NOTHING NEW IS TUNED** — `t` and `h` are
  1799's two inherited dials; crash window {24d peak-to-trough, 51d wide}, block {21, 63}, trade
  cadence {W, M}, panel {U56, B136, SMALL665} and cost {0, 10, 25, 50} bps are REPORTED. **420 cells
  x 3 tapes x 4 costs published; gates 10/10**, including G5, an exact replication of 1799's V2
  headline (263 of 263, mean +0.0596) before anything is excised.

  **THE WIN IS 24 DAYS WIDE.** Removing 2020-02-19 -> 03-23 — **24 of ~2,440 OOS trading days,
  1.0% of the sample** — takes the mean from +0.0596 to **+0.0066** and the win share from 263/263
  to 188/263. The 51-day window gives +0.0126 and 210/263. **89.0% of the published edge lives in
  one quarter**, and all six arms (panel x trade cadence) move the same way; U56/M, the arm carrying
  1799's own KEEP cell, is the weakest survivor at 28/44, mean +0.0005.

  **IT IS NOT A COST FACT.** Same 263 keys on the FULL tape: 0 bps **+0.0603** (263/263), 10 bps
  +0.0596, 25 bps +0.0586, 50 bps +0.0569 (261/263). The edge is fully present BEFORE costs and
  SHRINKS as they rise, so saved turnover is not the mechanism — the gross path through the crash is.

  **THE CREDIT IS DRAWDOWN, AND ONLY DRAWDOWN.** Outside the crash the OOS MaxDD gap keeps its sign
  at 88.6% of pairs but loses 84% of its size (+4.07 -> **+0.66 pp**), while the OOS CAGR gap turns
  **negative** (+0.31 -> **-0.26 pp**). Outside 2020 the drift trigger is a small drawdown shaver
  that costs a little return.

  **AND THE SWEEP WAS NEVER RESOLVABLE.** On the FULL tape only **61 of 263** cells have a 95%
  bootstrap CI excluding zero (mean |t| **1.49**, max 3.07); crash-excised it is 26 of 261. Block 63
  agrees (59/263 and 40/261). This is the general lesson for the record: a clean N-of-N sweep across
  a grid whose cells share one tape is not N pieces of evidence, and any such count published
  without a paired SE should be read as a single point estimate.

  **CAPITAL ARM (rule 8, 2017-2026 read exactly once).** DRIFT never reaches more arms than CALENDAR
  on any tape — FULL 3/6 vs 3/6, crash-excised 2/6 vs 2/6 and 2/6 vs 4/6 — reconfirming 1799's own
  V1 reachability KILL. **Path 4a: KILL on every tape** (40 of 420 cells on FULL, 0 of 420 on both
  excised). 1799's standing KEEP-4b cell (U56, T=M, `t=0.16, h=0.12`, C_ISSHARPE) posts FULL 15.62%
  / 1.2451 / -18.16% (H1/H2 1.29/1.20) and OOS **16.36% / 1.2810 / -18.16%** against SPY 15.12% /
  0.8843 / -33.72% (OOS 15.26% / 0.8737 / -33.72%) and live RULES v2 8.62% / 1.2010 / -12.05% (OOS
  9.46% / 1.2766 / -12.05%) — **it still clears 4b FULL+OOS on the real tape, and crashes are part
  of the real tape**, so the candidate is NOT withdrawn. But its own matched edge over the calendar
  ladder is +0.0735 (t +1.16) full and **-0.0123 (t -0.30)** crash-excised, so the dominance claim
  attached to it is withdrawn. **DISCLOSED, because it changes how the excised census reads:** the
  4b collapse 187 -> 80 and the 4a collapse 40 -> 0 are largely a BAR SHIFT — SPY's own MaxDD moves
  from -33.72% to -24.50%, tightening the 4b cap from -20.23% to -14.70% — while the book's MaxDD is
  unchanged at -18.16% on all three tapes. The matched DRIFT-vs-CALENDAR contrast is book-against-
  book on one tape and is immune to that shift; the pass COUNTS are not.

  **SURVIVORSHIP.** U56 / B136 are current-constituent lists and SMALL665 a current sub-$2B screen
  (54 tickers with `max_1d_move >= 1.0` dropped first). Levels are optimistic and both 4b bars are
  easier here than on a point-in-time panel; the contrast is first-order immune, the pass counts are
  not. SMALL numbers are not comparable with pre-2026-09-20 SMALL results (cache grew 439 -> 665).

  Scripts: `research/backtests/2026-09-20_drift-win-episode-or-dial_cloud.py`; caveat memo
  `research/backtests/2026-09-20_drift-trigger_CAVEAT_MEMO.md`. RULES.md unchanged.

## 2026-09-20 — idea 736 (lane cloud): IS CT_RANGE A BETTER-BEHAVED READING OF c_t DISPERSION THAN c_sd? **ANSWERED — NO, AND NEITHER IS c_sd: THE TWO ARE INTERCHANGEABLE AND THE OBJECT IS "c_t DISPERSION". BUT THE INTERCHANGEABILITY IS A *TAIL* FACT, NOT A DISPERSION FACT — THE ONE ESTIMATOR THAT DISCARDS THE TAILS IS MEASURABLY WORSE AT 8 OF 8 CELLS. NO NEW BOOK, NO RULES CHANGE.**

  **THE DEFECT THIS CLOSES.** Idea 735 fitted 23 predictor forms to the de-grossing TIMING RESIDUAL
  on idea 538's 162 cells and found CT_RANGE is the ONLY non-c_sd form of 20 that walks forward,
  landing within 0.5% of the incumbent at both splits with the ORDER FLIPPING between them — a coin
  toss. Both readings were taken at ONE gross (0.75), the rung idea 538 happened to fix, and the
  record has gone on quoting "c_sd" as if it were the QUANTITY rather than one ESTIMATOR of it.

  **THE CONSTRUCTION.** Two dials, exactly the pair the idea's own text names: ESTIMATOR {CSD,
  CT_RANGE, CT_IQR, CT_MAD, CT_SD_RANGE, CBAR, TORS + the constants ZERO/GLOBAL/FAMILY} x GROSS
  {0.25, 0.50, 0.75, 1.00}. Published, not tuned: panel {U56, B136, SMALL665}, family {QUANTILE x9,
  MA-THRESH x9}, cadence {W, M, Q}, split {S2016, S2018}, 10 bps, next-day execution. **648 cells,
  1,296 books, 80 fits, every grid point published.** Both constructions share one unit direction,
  so the whole gross ladder is EXACT off one per-cell state; **G1 re-asserts it against
  `engine.backtest` at 3.5e-18 … 2.1e-17 on all nine panel x cadence pairs.** The CSD-minus-CT_RANGE
  OOS MAE difference is given a PAIRED CELL BOOTSTRAP (2,000 draws, fixed md5 seed, the same 162
  cell indices resampled for both estimators) so the "order flip" is called resolved or not, instead
  of being read off two point estimates.

  **V1 NOT TRIGGERED, V2 TRIGGERED.** CSD is the point-estimate winner at **8 of 8** cells — 735's
  order flip does NOT reappear on the current cache — but the difference is not resolvable anywhere:
  max |t| **1.36**, and the 95% CI covers zero at **8 of 8** (t = -0.61 / -0.68 / -0.67 / -0.93 /
  -0.62 / -1.13 / -0.69 / -1.36). So the surviving object is **"c_t DISPERSION"** and the record must
  state which estimator any published number used — idea 564's unnamed-statistic defect, on the
  scale axis. The two-term `CT_SD_RANGE` buys nothing: OOS MAE ties CSD to five decimals while the
  second term's IS |t| collapses from **6.87 to 2.24**.

  **V3 IS THE SHARP RESULT: THE INTERCHANGEABILITY IS A TAIL FACT.** CT_RANGE (t -1.32 … -0.61) and
  CT_MAD (t -1.08 … -0.55) sit inside CSD's CI at **8 of 8** cells; **CT_IQR is EXCLUDED at 8 of 8
  (t -3.83 … -2.25)** and is the one form that loses to the FAMILY constant outright (0.090373
  against 0.090030 at gross 0.25 / S2018, the single reason "all four beat FAMILY" reads 7 of 8).
  Order is stable at 8 of 8: `CSD < {CT_RANGE, CT_MAD} < CT_IQR`, only the middle pair swapping.
  **What `c_sd` measures is the TAIL of the c_t path, not dispersion generically** — every estimator
  that keeps the tails is statistically indistinguishable from every other, and the interquartile
  range, which throws them away, falls measurably behind. That statement is new and falsifiable.

  **THE GROSS RUNG WAS NOT LOAD-BEARING.** CSD's OOS MAE as a share of the FAMILY constant's runs
  **0.9294 / 0.9150 / 0.9052 / 0.8987** (S2016) and 0.9783 / 0.9721 / 0.9670 / 0.9627 (S2018) across
  gross 0.25 -> 1.00: the ladder moves the SIZE of the estimator's purchase and never the ORDER, so
  735's 0.75-only reading did not carry its result, and no rung rescues CT_RANGE.

  **G2c — A DATA-VINTAGE FINDING THE RECORD NEEDS.** G2b reproduces idea 735's committed cells **on
  U56** (the stable `prices.csv` cache) to **2.61e-07** (c_sd), **3.67e-06** (ct_range), **1.44e-07**
  (c-bar) and **1.38e-05** (turnover). **B136 and SMALL do NOT reproduce, and the cause is the DATA,
  not the construction.** `gshare` (n_gated_in / n_live, a pure panel-composition number with no book
  in it) already differs by **9.58e-06 / 5.12e-05 / 6.42e-02** before any book is run; idea 735 ran
  on a SMALL panel of **439 names** and today's cache holds **665** after the same `max_1d_move >= 1.0`
  rule — a DIFFERENT UNIVERSE — and `prices_broad.csv` was re-fetched with restated adjusted closes
  (B136's IS-window RESPREAD turnover moves **0.184 turns/yr**, SMALL's **1.500**, U56's 1.4e-05,
  with the IS window ending 2016-12-31 in both runs so a longer tape cannot explain it).
  **Every committed number on the SMALL panel from before the 2026-09-20 re-cache is on a different
  universe and is not reproducible today.** A PANEL VINTAGE stamp (name count + cache sha) belongs
  beside every published panel number — the price-side twin of idea 894's tree stamp.

  **V4, THE CAPITAL ARM.** 1,296 books at 10 bps: 4b **39**, 4a **85**. By gross, 4b is 0 / 13 / 16 /
  10 of 324 at 0.25 / 0.50 / 0.75 / 1.00. **PATH 4a: KILL** — on U56, the panel the live book actually
  runs on, 4a is **0 of 432 books and 0 of 20 legal picks**; all 85 passes are on a RESTATED panel
  (B136 49, SMALL665 36), the artefact ideas 763 / 1793 recorded, and that is already the generous
  reading under PROTOCOL rule 3's same-panel comparand. **RULE 8 (2017-2026 read ONCE): 4b 2 of 60
  legal picks, 4a 9 of 60 and all nine at gross 0.25 on the restated panels; the joint (gross, level,
  cadence) chooser clears 4b 0 of 12.** The best reachable book — U56 QUANTILE top-50% monthly
  RESPREAD at gross 0.75, FULL 15.48% / 1.2371 / -19.80% (halves 1.344 / 1.155), **OOS 15.96% /
  1.2185 / -19.80%** at 3.10 turns/yr against SPY 15.12% / 0.8844 / -33.72% (OOS 15.26% / 0.8738) and
  live RULES v2 8.62% / 1.2011 / -12.05% — clears on a **0.43 pp** OOS drawdown-cap margin, the same
  knife-edge as the parked VOLTGT memo's 0.37 pp, and is **NOT filed as a KEEP-candidate**: it is one
  of 1,296 grid points in a run pre-registered for an ESTIMATOR question and needs its own
  pre-registered pass first. The grid's best 4b book (U56 MA-THRESH theta=0.00 monthly DEGROSS at
  gross 1.00, OOS 12.68% / 1.2754 / -15.54%) is unreachable by any legal IS-only chooser.

  **SURVIVORSHIP:** all three panels are CURRENT constituent lists — no delistings — so every CAGR
  LEVEL is inflated and the 4a/4b columns inherit that in full; the headline residual is an
  arm-minus-arm contrast on the SAME names, days and gross, so the bias very largely cancels out of
  it. SMALL drops 54 tickers with `max_1d_move >= 1.0` first. The paired-cell bootstrap resamples
  CELLS, which are not independent, so its SE is if anything optimistic — and it still cannot
  separate CSD from CT_RANGE. GATES 23 of 23. RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py
  are untouched by idea 736.
  Evidence: `research/backtests/2026-09-20_ct-dispersion-estimator-on-a-gross-ladder_cloud.py` /
  `.result.md` / `.cells.csv` / `.books.csv` / `.ladder.csv` / `.compare.csv` / `.family.csv` /
  `.walkforward.csv` / `.gates.csv`.

## 2026-09-20 — idea 1785 (lane cloud): DOES THE VOLTGT DIAL'S MATCHED-TWIN WIN SURVIVE A PAIRED CIRCULAR-BLOCK BOOTSTRAP? **ANSWERED — SPLIT. KILL THE SHARPE HALF OF IDEA 1771's HEADLINE (it is not distinguishable from zero, and neither is its opposite on SMALL665); THE DRAWDOWN HALF SURVIVES AT ~2 SIGMA AND NO FURTHER. NO NEW BOOK, NO RULES CHANGE.**

  **THE DEFECT THIS PRICES.** Every addendum since 2026-09-20 has demoted the standing VOLTGT memo —
  its rung (1771), its convention (1771), its cadence clause (1767), its panel-sourcing (1763) — and
  what is left carrying the object is ONE sentence: "the vol target is the record's FIRST device to
  beat its own realised-mean-gross-matched constant-gross twin, OOS +0.0587 Sharpe / +6.16 pp MaxDD
  on U56, win share 0.810". That sentence was published as a POINT ESTIMATE with no standard error,
  and its "n" was quoted as 100 cells that are 20 conventions x 5 targets on ONE 2,400-day tape.
  Idea 1537's paired circular-block bootstrap of exactly this dMaxDD had been open and unrun since
  2026-09-10.

  **THE CONSTRUCTION.** Two dials, the protocol maximum: BLOCK LENGTH `B` {5, 10, 21, 63} and the
  twin's GROSS-MATCHING WINDOW `M` {IS, FULL, OOS}. Published, not tuned: target `t` {0.08, 0.10,
  0.12, 0.16, 0.20}, PANEL {U56, B136, SMALL665}, COST {0, 10, 25, 50} bps, the memo's own sigma cell
  `(L=20, d=0)`, weekly, next-day, gross capped at 1.00. **540 book rows and 540 bootstrap cells at
  2,000 paired draws each, every grid point published.** Book and twin are resampled with the SAME
  block offsets, so the difference keeps its pairing; the seed stream is md5-derived and fixed.

  **REPLICATION FIRST.** G1 the fast runner == `engine.backtest` at **1.4e-17 / 2.1e-17 / 3.5e-17**
  (three panels, 10 and 25 bps); G2 reproduces the memo's sections 2-4 at **2.76e-04**; **G3
  reproduces idea 1771's pooled headline EXACTLY — U56 +0.0587 / +0.0616 / 0.810 and B136 +0.0503 /
  +0.0944 / 0.790**; G4 twins bisected to **2.2e-16**. Gates 12 of 12.

  **V1 TRIGGERED AT 4 OF 4 BLOCK LENGTHS. The Sharpe leg is below this tape's resolution.** At the
  memo's own rung the observed U56 OOS dSharpe is **+0.0930**, and its bootstrap t reads
  **+0.80 / +0.78 / +0.87 / +1.04** at B = 5 / 10 / 21 / 63 (SE 0.1156 / 0.1198 / 0.1072 / 0.0899,
  two-sided p **0.398 / 0.450 / 0.400 / 0.307**), with BOTH the percentile and the pivotal 95% CI
  covering zero. Across all 180 OOS cells only **0.033** reach |t| >= 2 on dSharpe, and on U56 and
  B136 the CI covers zero at **1.000** under both conventions. The same instrument kills the
  OPPOSITE claim too: SMALL665's −0.1929 mean twin LOSS reaches |t| >= 2 in only **0.100** of cells.
  Neither "the dial beats its twin on Sharpe" nor "the twin beats the dial on small caps" is
  supported.

  **V2: THE TWO LEGS DISAGREE, AND ONLY THE DRAWDOWN LEG CARRIES SIGNAL.** OOS, 10 bps: dSharpe mean
  +0.0207 with share obs>0 **0.667**; dMaxDD mean +0.0928 with share obs>0 **1.000** and share
  t >= 2 **0.522** (U56 0.567, B136 **1.000**, SMALL665 0.000), share t <= −2 **0.000**. The book's
  drawdown beats its matched twin's at **180 of 180** cells. The two legs must never be averaged into
  one "twin win".

  **V3: THE INSTRUMENT WORKS FOR DRAWDOWN, BUT THE TWO STANDARD CI CONVENTIONS DISAGREE AND THAT IS
  THE REAL LIMIT.** The dMaxDD SE moves only **1.27x** across the whole block ladder (0.0356 at B=5
  to 0.0389 at B=63) — V3 PASS. But the **percentile CI covers zero at 1.000 of 180 cells while the
  pivotal CI excludes it at 1.000 of U56/B136 cells**, because circular block resampling biases the
  drawdown draw distribution DOWN (boot mean +0.033…+0.047 against an observed +0.076) by shredding
  the long declines that make a drawdown. The honest statement is the range: **~1.7-2.1 sigma**, and
  any future wording that leans on this leg must name which CI it used.

  **V4, RULE 8 (2017-2026 read ONCE): THE BOOTSTRAP-t IS A NO-OP ON ONE LEG AND FRAGILE ON THE
  OTHER.** 33 legal IS-only picks: 4b OOS **17 of 33**, 4a OOS **3 of 33**. `C_BOOTT_S` makes the
  IDENTICAL pick to plain `C_ISSHARPE` at 4 of 4 block lengths on all three panels — dividing an
  unresolvable difference by its own SE adds nothing, the same shape of no-op idea 1793 proved for
  `C_GXS`. `C_BOOTT_D` clears 4b OOS **7 of 12** but **4b FULL 0 of 12**: its U56 pick `t = 0.08`
  posts OOS **11.38% / 1.2999 / −12.28%** (PASS, against SPY 15.26% / 0.8738 / −33.72% and live
  RULES v2 9.46% / 1.2769 / −12.05%) yet fails 4b FULL on the CAGR floor (10.22% against
  0.70 x SPY = 10.58%) — and on B136 the TUNED DIAL moves the verdict (B=5 → `t=0.20`, 4b OOS FAIL;
  B >= 10 → `t=0.08`, PASS).

  **CAPITAL ARM.** 15 M=IS books x 4 cost rungs: 4b FULL **8 / 6 / 6 / 5** and 4b OOS **8 / 8 / 7 /
  5** of 15 at 0 / 10 / 25 / 50 bps; 4a FULL 1 / 1 / 0 / 0 and 4a OOS 1 / 1 / 1 / 0. Binding 4b leg
  OOS at 10 bps is `L4_DD` (7 of 15), the other three 5 each. **PATH 4a: KILL** — its 3 passing picks
  are all B136 at `t = 0.08` and only against the live book RESTATED on B136 (1.1019) rather than the
  real live U56 comparand (1.2769), the same panel-restatement artefact ideas 1763 and 1793 recorded.
  **SMALL665 clears 4b 0 of 45 rows at every cost rung — memo addendum A2's FOURTH confirmation.**

  **WHAT IT CHANGES.** Idea 1771's headline loses its Sharpe half; the 0.810 win share is not
  independent evidence and must not be quoted as if it were. The standing VOLTGT memo stays **PARK**
  (ideas 1771 / 1767 / 1793) and nothing here restores it; idea 1793's `C_GXDD` KEEP-4b candidate is
  untouched, with the one note that its U56 pick is the same `t = 0.08` cell this run finds failing
  4b FULL on the CAGR floor. **SURVIVORSHIP:** U56 / B136 / SMALL665 are CURRENT constituents; SMALL
  drops 54 tickers with `max_1d_move >= 1.0` first. RULES.md, PROTOCOL.md, scan.py, bot.py and
  baseline.py are untouched by idea 1785.
  Evidence: `research/backtests/2026-09-20_voltgt-twin-win-block-bootstrap_cloud.py` / `.result.md`
  / `.books.csv` / `.bootstrap.csv` / `.walkforward.csv` / `.surface.csv` / `.gates.csv`.

## 2026-09-20 — idea 1793 (lane B): CAN AN EXPOSURE-NEUTRAL IS-ONLY CHOOSER REACH THE 4b CELLS THAT PLAIN IS SHARPE MISSES? **ANSWERED — YES ON THE DRAWDOWN LEG (4 of 4 large-panel arms against 2 of 4 and 0 of 4), NO ON THE SHARPE LEG, WHERE THE SAME CORRECTION IS A PROVABLE NO-OP. KEEP-CANDIDATE (path 4b) FOR THE CHOOSER; KILL THE RECORD'S STANDING "IS SHARPE REWARDS THE HIGHER-GROSS BOOK" EXPLANATION. NO RULES CHANGE.**

  **THE DEFECT THIS PRICES.** Three runs on 2026-09-20 found the SAME failure and none tried to fix
  it. Idea 1771: IS Sharpe peaks at `t = 0.16` and the surface argmax is the STALER convention,
  which fails 4b OOS on the drawdown cap. Idea 1767: **23 of 24** legal IS-only picks land
  off-diagonal on a STALE scalar "because IS Sharpe rewards the lazier, higher-gross book", and on
  U56 all eight go to `(T=Q, R=M)` and fail. Idea 1763: a chooser handed the sigma source free buys
  SPY 14 of 18 times because SPY's sigma runs hot and pushes the target argmax one rung UP. All
  three blamed EXPOSURE. Idea 1771 also built the machinery to test that — the realised-mean-gross-
  matched constant-gross twin — and that difference is computable ENTIRELY IN SAMPLE, so it is a
  legal rule-8 chooser that had never been run.

  **THE CONSTRUCTION.** Two dials, the protocol maximum, both spent by the chooser: TARGET
  `t` {0.08, 0.10, 0.12, 0.16, 0.20} x REFRESH cadence `R` {D, W, M, Q} = 20 cells per arm.
  Published, not tuned: TRADE cadence `T` {W, M} (each `(panel, T)` is a SEPARATE arm and no chooser
  ever selects across `T`), PANEL {U56, B136, SMALL665}, COST {0, 10, 25, 50} bps. The sigma
  convention is FIXED at the standing memo's `(L = 20, d = 0)`. **480 rows, every grid point
  published.** Each book carries its OWN constant-gross twin bisected to the book's realised mean
  gross (G8 **2.9e-11**) — one matched on the IS window (what the chooser may see) and one on the
  full window (reporting only). Verdict rules V1-V4 were fixed in the script header before the run.

  **REPLICATION FIRST.** G3 reproduces the standing KEEP-4b memo's points 2-4 at max |d|
  **4.605e-05** and G4 reproduces idea 1767's `(T=M, R=W)` U56 OOS row at **5.027e-05**.

  **V1 TRIGGERED. `C_GXDD` — rank by `IS MaxDD(book) - IS MaxDD(its own IS-gross-matched twin)` —
  clears 4b FULL *and* OOS at 4 of 4 large-panel arms**, against `C_ISDD` **2 of 4**, `C_ISLEGS`
  1 of 4 and `C_ISSHARPE` / `C_ISCALMAR` **0 of 4**. U56 pick `t=0.08, R=M`: FULL 11.26% / 1.2285 /
  -16.13% (halves 1.3198 / 1.1442), **OOS 11.87% / 1.2780 / -16.13%** at 2.19 turns/yr against SPY
  15.12% / 0.8843 / -33.72% (OOS 15.26% / 0.8737) and live RULES v2 8.62% / 1.2010 / -12.05%.
  B136 pick `t=0.10, R=W`: FULL 12.17% / 1.1817 / -13.46%, OOS 12.69% / 1.2417 / -13.46%, clearing
  4b FULL+OOS at **0 / 10 / 25 / 50 bps** where the parked memo's own cell fails at 50. DD-cap
  margins **4.10 pp** (U56) and **6.77 pp** (B136) against the parked memo's 0.37 pp. V2 and V3 also
  triggered (mean OOS Sharpe 0.9186 vs 0.9167, mean OOS MaxDD -26.36% vs -27.64%; in-band share
  0.500 vs 0.292).

  **AND THE SHARPE HALF IS A NO-OP, WHICH IS THE KILL THAT MATTERS.** `C_GXS` makes the IDENTICAL
  pick to plain `C_ISSHARPE` in **6 of 6** arms. Across a twin gross range `k = 0.6218 -> 0.9812`
  the twin's IS Sharpe spans **0.0007-0.0057** against the book's **0.2283-0.3347** — **0.2% to
  2.4%** of it — with spearman(is_Sharpe, gx_Sharpe) **0.9985-1.0000** and identical argmax 6 of 6.
  A long-only constant-gross book's Sharpe is invariant in its gross, so **"IS Sharpe rewards the
  lazier, HIGHER-GROSS book" is arithmetically impossible**: exposure carries ~1% of the IS Sharpe
  variation on this dial. What IS Sharpe actually buys is **LESS TIMING** — a higher target is a
  book closer to always-on, and 2009-2016 did not pay for timing. On the DRAWDOWN leg the twin
  carries **55-75%** of the book's IS variation (twin spread 0.047-0.080 against the book's
  0.085-0.092), which is exactly why the same correction is decisive there and vacuous on Sharpe.

  **THE SQUEEZE IS MOVED, NOT ESCAPED.** U56's pick swaps a 0.37 pp DD-cap margin for a **0.68 pp
  CAGR-floor margin** and FAILS at 50 bps on that floor; only B136's `t = 0.10` sits in the middle.
  And **half the dial is still unreachable**: `R = D` clears 4b FULL+OOS at 4 of 4 arms for every
  `t >= 0.10` and **no legal IS-only chooser ever picks it** — the OOS oracle does (`t=0.12, R=D`,
  U56 OOS 15.28% / 1.3485 / -15.79%). Grid totals: 4b FULL+OOS **41 / 35 / 32 / 21** of 120 at
  0 / 10 / 25 / 50 bps, 21 of 120 clearing at ALL FOUR rungs. **SMALL665: 0 of 40 at every rung**,
  confirming the memo's addendum A2 a third time. Binding legs at 10 bps: `L4_DD` 75, `L2_H2` 46,
  `L5_CAGR` 44, `L3_OOS` 42, `L1_H1` 21 of 120.

  **PATH 4a: KILL.** 0 of 36 legal picks; 6 of 120 grid cells at 10 bps, all B136 at
  `t in {0.08, 0.10}` with `R in {D, W}` — and only against the live book RESTATED on B136
  (Sharpe 1.0972) rather than the real live U56 comparand (1.2010), the same panel-restatement
  artefact idea 1763 recorded.

  **GATES 11 of 11.** G0 >= 10y; G1 the two-schedule runner == `engine.backtest` on returns AND
  turnover **0.000e+00**; G2 the cost identity == fresh engine runs at 10 and 25 bps **0.000e+00**;
  G3 / G4 as above; G5 a refresh row moves every held name by ONE common factor (8.9e-16 over
  133,070 refresh rows); G6 exactly two tuned dials; G7 all 480 cells published; G8 twin gross match
  2.9e-11; G9 max realised gross 1.0000 (never levered); **G10 all 36 chooser picks are unchanged
  when every chooser input is rebuilt on a panel PHYSICALLY TRUNCATED at 2016-12-31 — rule 8 tested,
  not asserted.**

  **RESIDUE (rule 6; RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py untouched):** (1) a
  KEEP-candidate memo with fully implementable RULES wording — target, lookback, staleness, refresh
  cadence and trade cadence all named — is written, and an addendum is appended to the parked VOLTGT
  memo; (2) **any claim that a chooser is bought by EXPOSURE must be scored against a gross-matched
  twin before it is published**: on the Sharpe leg that correction is provably empty, so the claim
  can only ever be a TIMING claim; (3) the refresh half of the dial remains PARK — a real, repeatable
  gain (`R = D`) that no legal in-sample statistic reaches.

  **SURVIVORSHIP.** U56 / B136 are CURRENT-constituent lists and SMALL665 a CURRENT sub-$2B screen
  (54 tickers with `max_1d_move >= 1.0` dropped). Every CAGR and drawdown LEVEL above is optimistic
  and both 4b bars are easier here than on a point-in-time panel. The CHOOSER contrast is same-tape,
  same-names, same-grid with only the ranking statistic moved and is first-order immune; the pass
  COUNTS are not.
  `research/backtests/2026-09-20_exposure-neutral-is-chooser_B.py` / `.result.md` / `.grid.csv` /
  `.choosers.csv` / `.twins.csv` / `.truncated.csv` / `.gates.csv`
## 2026-09-20 — idea 1789 (lane C): IS THE STALE-REFRESH PREFERENCE AN IS-WINDOW FACT OR A REGIME FACT? **ANSWERED — AN IS-WINDOW FACT, AND THE CARRIER IS CRASH-PRESENCE. KILL OF 1767's CHOOSER-BLINDNESS READING; NO NEW BOOK, NO RULES CHANGE.**

  **THE DEFECT THIS CLOSES.** Idea 1767 found that on rule 8's fixed window all four legal IS-only
  choosers picked a STALE gross scalar (R = M or Q) on 2009-2016 and then failed the 4b drawdown cap
  out of sample (U56 t=0.16: all four pick T=Q,R=M, OOS MaxDD **-23.96%** vs the memo's weekly
  **-19.86%**), and the record read that as a chooser defect. A stale exposure scalar only costs money
  **when vol spikes**, and 2009-2016 contains no drawdown deeper than the 2015-16 correction.

  **THE ANSWER.** Same book, same two-schedule runner, same panels, same targets, same costs as 1767 —
  only the chooser's visible window moves (**G3 cross-run reproduces 1767's published picks with 0
  mismatches, max |d| 4.5e-05**). With IS LENGTH HELD FIXED AT 8 YEARS the STALE share of legal IS-only
  picks runs **79.2% (W0 2009-2016, rule 8's own) / 75.0 / 62.5 / 41.7 / 0.0 / 0.0 (W5 2014-2021)**, and
  the collapse lands exactly where the 2020 crash enters the window. The idea's own two named windows
  agree (N1 2010-2018 **62.5%**, N2 2012-2020 **4.2%**). Rank corr(SPY IS MaxDD, stale share) **+0.638**
  JOINT / **+0.600** T-conditional, quoted DESCRIPTIVELY — the windows overlap heavily, so no p-value is
  computable and none is claimed.

  **CRASH-PRESENCE, NOT RECENCY.** The slid family confounds the two (sliding forward both acquires 2020
  and drops 2009-2012), so a control 2x2 separates them: **main effect of crash-presence -50.0 pp**
  (stale 2.1% with a crash in IS vs 52.1% without) against **main effect of recency -4.2 pp** (25.0%
  late vs 29.2% early). X1 2009-2019 -> X2 2009-2020 adds **one year** to an eleven-year window and takes
  the stale share **54.2% -> 4.2%**.

  **THE MECHANISM, PRICED.** FRESH minus STALE is **-0.0003 Sharpe / +0.23 pp MaxDD inside W0** — an
  argmax over indistinguishable cells falls to the stale one on noise and saved turnover — and
  **+0.1967 Sharpe / +12.23 pp MaxDD inside W4**, where every chooser finds it instantly. Reported
  against our own reading: on the crash-free post-2021 OOS spans d(post Sharpe) turns **-0.1011**, so the
  preference tracks crash-presence in whichever sample it is measured on, in both directions.

  **THE CAPITAL ARM IS UNCHANGED AND SHARPER.** Over 384 book cells: 4b **119**, **4a 0** (the live
  book's -12.05% MaxDD is unreachable for a 0.12/0.16-target vol-scaled book). At 10 bps the STALE
  scalar clears 4b at **0 of 48** cells and the FRESH scalar at **32 of 48** (mean OOS MaxDD -32.37% vs
  -20.78%); binding leg is `L4_DD` throughout with `L5_CAGR` binding 0 times, and SMALL clears nothing.
  Rule 8 (2009-2016 chooses, 2017-2026 read once): **4 of 24 picks clear 4b OOS and all four are FRESH**;
  all 8 U56 picks are stale and clear nothing.

  **WHAT CHANGES.** Nothing in the book. RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are
  untouched (rule 6). One item is left for the Sunday review as a finding, not a change: any claim of
  the form "no legal IS-only chooser can reach X" that rests on rule 8's fixed 2009-2016 window is
  untested against the possibility that the window does not contain the event that prices X, and the
  cheap test is to slide the IS window at fixed length and read whether the argmax moves.

  GATES **10 of 10 PASS**. Survivorship: U56/B136 current-constituent, SMALL a current sub-$2B screen
  (54 tickers dropped); the window-to-window contrasts are same-tape and first-order immune, the pass
  COUNTS are not. Script `research/backtests/2026-09-20_stale-refresh-is-window-or-regime_C.py`.

## 2026-09-20 — idea 1613 (lane C): IS EVERY CADENCE CLAIM IN THE RECORD A c* CLAIM QUOTED AT ONE RUNG? **ANSWERED, BOTH WAYS — YES FOR THE ORDERING, NO FOR THE KEEP VERDICT. KILL: NO RULES CHANGE, NO NEW BOOK.**

  **THE DEFECT THIS PRICES.** PROTOCOL rule 2 binds every backtest to ONE cost rung, so every cadence
  verdict this repository has ever committed is a point reading of a function of cost. Idea 1586 found
  the frozen anchor's weekly cadence beating its quarterly twin by only **c\* = 12.4 bps**. This run asks
  how much of the committed cadence record sits on a slope that steep.

  **THE CENSUS.** Mechanical extraction over LEADERBOARD.md and CHANGELOG.md under a rule fixed before the
  run: **86 BROAD cadence-comparison sentences, 30 STRICT** (explicit ordered pair). **76 of 86 (88.4%)
  and 25 of 30 (83.3%) are quoted at a SINGLE cost rung**; 8 BROAD quote a ladder, 2 quote a c\*, and
  exactly **1 of 86 quotes a ladder spanning the whole 5-50 bps band**. Every extracted sentence is
  published to `.census.csv` so the classification is auditable, and the STRICT denominator is carried
  because the BROAD rule cannot tell a rebalance cadence from rule 9's weekly cache refresh.

  **THE RE-PRICING.** 24 books (FRAME {LIVE, INC} x PANEL {U56, B136, SMALL} x CADENCE {D, W, M, Q}),
  the whole cost axis exact: `r(c) = r_gross - turnover*c/1e4` reproduces fresh `engine.backtest` runs at
  10, 25 and 50 bps to **0.000e+00**, and a closed-form `Sharpe(c)` matches the direct reduction to
  6.7e-16. Over 180 pairwise verdicts (6 cadence pairs x 5 windows x 6 frame-panels), **43 (23.9%) FLIP
  SIGN inside 5-50 bps** and **0 of 180 cross more than once** — the comparison is MONOTONE in cost, so
  a single c\* describes it completely. Median c\* among in-band crossers **27.5 bps** (IQR 17.3-33.7).
  By frame **LIVE 34.4% vs INC 13.3%**; by window OOS 27.8%, IS 19.4%; by pair DvM 33.3% down to
  **MvQ 3.3%**. G9: idea 1586's committed headline is re-derived at **c\* = 12.42** against 12.4.

  **AND THE FLIP IS PREDICTABLE FROM THE MARGIN THE RECORD ALREADY PUBLISHES.** Readings with
  `|dSharpe@10| < 0.05` flip **50.7%** of the time (n = 69); readings at `>= 0.05` flip **7.2%**
  (n = 111). Median |d@10| is 0.0221 among flippers against 0.0843 among non-flippers.

  **WHY IT IS A KILL ANYWAY.** Scanning c in [0, 50] at 0.25 bps for all 24 books, with the live RULES v2
  comparator re-priced at the same rung, the **4b verdict (FULL and OOS) is EMPTY over the whole band for
  22 of 24 books, holds over the ENTIRE band for 2, and is RUNG-CONDITIONAL for 0**. The 4b legs are
  dominated by the DD cap and the CAGR floor, which a 40 bps cost swing moves far less than it moves the
  Sharpe ranking of two adjacent cadences. The rung reorders cadences often and changes a KEEP decision
  never. The two passers are U56/INC: the frozen anchor **W** (15.80% / 1.1537 / -19.13%; OOS 17.32% /
  1.1857; 2.87x/yr) and its quarterly twin **Q** (15.49% / 1.1515 / -19.89%; OOS 17.43% / 1.1885;
  **1.64x/yr**), each passing on [0,50]. 4a: 2 of 24 at any rung.

  **RULE 8 (2017-2026 READ ONCE), WITH THE RUNG ITSELF AS DIAL 2.** **4 of 12 (panel x frame x chooser)
  groups change their IS pick with the rung they quote** — U56/INC/C_SHARPE picks W at 5 and 10 bps and Q
  at 25 and 50, i.e. the 12.42 bps crossing surfacing as a tuning artefact — so the rung is a real free
  parameter of a cadence search. Spending it is negative-value: pooled over 24 cells, C_SHARPE mean OOS
  Sharpe **0.8815** (dS vs anchor **-0.0464**), C_MEMO 0.9198 (-0.0080), **C_ANCHOR 0.9278** for choosing
  nothing; **0 of 24 beat the live RULES v2 book** on either chooser and 16 of 24 beat SPY.

  **THE CONSTRUCTIVE HALF (memo written, NOT adopted).** A blanket interval requirement in rule 2 buys
  nothing, because the verdicts this protocol commits to are rung-invariant. The cheap fix is a margin
  trigger, since c\* costs no extra backtest: *"A claim that one rebalance cadence beats another must
  publish the break-even cost `c*` at which the comparison reverses whenever the quoted Sharpe margin at
  10 bps is below 0.05; above that margin the point quote stands."* It fires on 38.3% of readings and
  catches the half that actually flips. Pre-stated adoption trigger: the flip base rate must survive on a
  second corpus not built from these two frames.

  **GATES 19 of 19.** G0 >= 10y; G1/G1b fast runner == `engine.backtest` on returns AND turnover
  (0.000e+00); G2 derived 25 and 50 bps rungs == fresh engine runs (0.000e+00); G3 LIVE/W == the committed
  RULES v2 baseline row; G4 INC/W == the committed 2026-09-04 anchor (3.7e-05); G5 exactly two dials;
  G6 no chooser reads a row on or after 2017-01-01 (truncated re-fit, tested not asserted); G7 all 120
  grid cells published; G8 max realised gross 0.7500; G9 the c\* solver re-derives 1586's 12.4;
  G11 closed-form Sharpe(c) == the direct reduction (6.7e-16); G10 turnover per cadence published.

  **SURVIVORSHIP.** U56 / B136 are CURRENT-constituent lists and SMALL a CURRENT sub-$2B screen, so every
  CAGR and drawdown LEVEL is optimistic. The cadence contrasts are same-tape, same-names, same-frame, and
  the SHAPE of each contrast in cost is arithmetic on one tape. **RULES.md, PROTOCOL.md, scan.py, bot.py
  and baseline.py are untouched by this run.**

## 2026-09-20 — idea 1767 (lane cloud): IS THE VOLTGT016 CANDIDATE'S MONTHLY BLOWOUT A REBALANCE-COUNT FACT OR A SIGNAL-STALENESS FACT? **ANSWERED — STALENESS, 100% OF IT. KILL THE STANDING MEMO'S "THE WEEKLY REBALANCE IS LOAD-BEARING". A CHEAPER BOOK DOMINATES IT AND RULE 8 CANNOT REACH THAT EITHER.**

  **THE DEFECT THIS CLOSES.** Idea 956 found the standing KEEP-4b candidate's OOS MaxDD goes −19.9% →
  −24.2% on U56 and −18.8% → −26.1% on B136 when the cadence moves weekly → monthly, and its memo
  addendum concluded "the weekly rebalance is load-bearing and must stay in any RULES wording". But a
  monthly cadence changes TWO things at once — how often the NAMES are re-spread, and how stale the
  gross scalar `g = clip(t / sigma20, 0, 1)` is when applied — and in the standard construction `g` can
  only move ON a trade day, so the two are perfectly confounded. The memo's clause was never a claim
  about the rebalance.

  **THE CONSTRUCTION.** Two nested schedules on one book, and the separation is the whole run: the book
  carries a scalar `g_eff` READ OFF `g_t` ONLY ON A REFRESH DAY (schedule **R**), so R alone controls
  staleness; on a TRADE day (schedule **T**) the names are re-spread to `g_eff * ew_t`; on a refresh day
  that is not a trade day the book keeps its names and is scaled by ONE common factor to `g_eff`, a pure
  exposure trade costing |g_eff − held|. The diagonal `T == R` is the committed book exactly. Two tuned
  dials, T and R, each over {D, W, M, Q}; PANEL {U56, B136, SMALL665}, TARGET {0.12, 0.16} and COST
  {0, 10, 25, 50} bps are reported axes. **384 scored books, every cell published** to `_grid.csv`.

  **THE ANSWER.** Of the weekly-minus-monthly OOS drawdown gap, refreshing the SCALAR weekly while
  trading the names MONTHLY recovers **+4.57 pp of +4.38 on U56 (104%), +7.36 of +7.35 on B136 (100%)
  and +7.62 of +7.58 on SMALL665 (101%)**; doing the opposite — weekly names on a MONTHLY scalar —
  recovers **−0.28 / −0.45 / −1.16 pp (−6% / −6% / −15%)**. The interaction is +0.09 / +0.43 / +1.11 pp.
  **The 4b verdict is a function of R alone**: pooled over panels and targets at 10 bps, `R ∈ {D, W}`
  clears full 4b in 4 of 6 cells at EVERY trade cadence including quarterly, and `R ∈ {M, Q}` clears
  **0 of 6 at every trade cadence including daily**. T is inert on the verdict.

  **THE CONSTRUCTIVE HALF WORKS.** `(T=M, R=W)` dominates the candidate on both panels at strictly lower
  cost: U56 FULL 15.71% / 1.2129 / −19.68% (halves 1.2864 / 1.1468), **OOS 16.11% / 1.2343 / −19.68% at
  1.51 turns/yr** against the memo's 15.94% / 1.2193 / −19.86% at 1.83 — **+0.015 of OOS Sharpe,
  +0.18 pp of drawdown, −17.5% of turnover**; B136 OOS 15.38% / 1.1886 / −18.74% at 1.61 against
  15.36% / 1.1837 / −18.76% at 1.93. It clears 4b FULL and OOS at 0 / 10 / 25 bps and fails only at 50,
  on the CAGR floor.

  **AND RULE 8 CANNOT REACH IT (2017-2026 read ONCE).** With T and R chosen jointly on 2009-2016 only,
  **4 of 24 legal IS-only picks clear 4b OOS and 0 of 24 clear 4a OOS**; **23 of 24 land off-diagonal on
  the WRONG side**, taking a STALE scalar (`R = M` or `Q`) because IS Sharpe rewards the lazier,
  higher-gross book. On U56 all eight IS picks go to `(T=Q, R=M)` — OOS −20.83% / −23.96%, 4b OOS FAIL
  at both targets — while the no-choice control `(T=W, R=W)` passes at both. The OOS oracle is
  `(T=Q, R=D)`: U56 16.89% / 1.2892 / −19.18%. So the finding is a WORDING fix, not a tuned pick, and
  the candidate stays **PARK** (idea 1771); this run does not restore it.

  **WHAT SECTION 9 OF THE MEMO SHOULD SAY INSTEAD.** "`g` is re-read and the book's total exposure reset
  to it **at least weekly**; the equal-weight re-spread of the names may run on any cadence from daily
  to monthly." Shipping "weekly rebalance" as written pays a cost the book does not need and does not
  protect the drawdown it claims to.

  **BINDING LEGS AND THE NEGATIVE HALF.** Over 384 cells: 4b FULL 119, 4b OOS 119, full 4b 119, **4a 0,
  4a OOS 0**. On U56/B136 the ONLY binding leg is the DD CAP (32-41 of 64 per panel × target; every
  other leg binds 0-2 times). On SMALL665 every one of 128 cells fails 4-5 legs.

  **GATES 9 of 9.** G0 `sigma20(t)` is a trailing window closing at t, 1.277e-15; G1 the two-schedule
  runner == `engine.backtest` on returns AND turnover on the diagonal, 0.000e+00; G2 the cost identity
  `r(c) = r0 − turnover·c/1e4` == the engine at 10 and 25 bps, 0.000e+00; **G3 the standing memo's
  committed U56 and B136 cells (points 2-4) reproduce at max |Δ| 4.605e-05**; G4 each of 85,914 refresh
  rows moves every held name by ONE common factor (spread 8.882e-16); G5 SMALL drops 54 tickers at
  `max_1d_move >= 1.0`; G6 exactly two dials; G7 no chooser statistic reads a row on or after
  2017-01-01; G8 all 384 cells published; G9 no RNG.

  **SURVIVORSHIP.** U56 / B136 are CURRENT-constituent lists and SMALL a CURRENT sub-$2B screen, so every
  CAGR and drawdown LEVEL is optimistic. The T × R contrasts are same-tape, same-names, same-scalar
  comparisons with only the two schedules moved and are first-order immune; the pass COUNTS are not.

  **STATUS.** ANSWERED. No new KEEP, **no rule change** (PROTOCOL rule 6); the standing candidate stays
  PARK and its memo carries a new addendum with the corrected wording. RULES.md, PROTOCOL.md, scan.py,
  bot.py and baseline.py are untouched. Evidence:
  `research/backtests/2026-09-20_voltgt-trade-vs-refresh-cadence_cloud.py` / `_grid.csv` /
  `_choosers.csv` / `_gates.csv` / `.txt`.

## 2026-09-20 — idea 1753 (lane cloud): IS THE STANDING U56 / GROSS-1.00 / WEEKLY 4b PASS A TRADE-CADENCE ARTEFACT? **ANSWERED — NO. IT IS A CONTIGUOUS CADENCE WINDOW D..M THAT DIES ONLY AT Q, AND THE RULE-8 CHOOSER LANDS INSIDE IT. KEEP-CANDIDATE (path 4b) RE-CERTIFIED ON U56 ONLY.**

  **THE DEFECT THIS CLOSES.** Idea 1741 priced the band's drawdown credit at three TRADE cadences and
  found the sign reversing outright at Q (positive in 89.4% of weekly books, 81.8% of monthly, 3.0% of
  quarterly). The record's standing band 4b passer — U56, the live RULES v2 clause-2 equal-weight band
  book (c = 0.03, gated weight to CASH) at gross 1.00, WEEKLY — had never been scored as a 4b VERDICT
  against that ladder: idea 1694 walked the weekly PHASE, not the CADENCE, and idea 1761's CAL arm
  published D / W / M / Q without the 2W rung, without per-leg margins, and without a chooser.

  **THE CONSTRUCTION.** Two tuned dials: CADENCE LADDER {D, W, 2W, M, Q} at the committed
  last-trading-day anchor (2W = every second weekly anchor; BOTH its phases published) x PANEL AXIS
  {U56, B136, SMALL665}. Reported, not tuned: GROSS {0.75, 1.00}, COST {0, 10, 25, 50} bps
  reconstructed exactly off the cost-0 leg. **144 scored books, every cell published** to `_grid.csv`,
  with all five 4b legs, their margins in their own units, and the failing-leg set at each.

  **THE ANSWER — A WINDOW, NOT A RUNG.** On U56 at gross 1.00 / 10 bps, **4 of 5 rungs clear all five
  4b legs**: D 11.20%/1.1899/−14.77% (OOS 12.45%/1.2873), W 11.53%/1.2008/−15.91% (OOS
  12.67%/1.2759), 2W-a 11.81%/1.2141/−15.99% (OOS **13.10%/1.3096**), M 11.90%/1.1734/−18.81% (OOS
  12.82%/1.2251), against SPY 15.12%/0.8843/−33.72% (OOS 15.26%/0.8737/−33.72%). **Q alone fails**, on
  the DD cap by itself (−26.07% against the −20.23% cap, L4_DD −5.84 pp) while still clearing the CAGR
  floor by +0.07 pp. 1741's Q reversal is a DRAWDOWN reversal and it does not reach a tradable rung.
  Over the cost ladder 19 of 24 U56 g=1.00 cells pass; 2W and M survive all four rungs, D and W die
  only at 50 bps and only on the CAGR floor.

  **RULE 8 (cadence chosen on 2009-2016 only, 2017-2026 read ONCE): the pass is REACHABLE.** All three
  legal IS-only choosers — IS Sharpe, IS Calmar, IS 4b-leg count — land on **M** on U56 at gross 1.00,
  inside the passing set, and all three clear 4b OOS: **12.82% / 1.2251 / −18.81%** against live RULES
  v2 9.46% / 1.2766 / −12.05% and SPY 15.26% / 0.8737 / −33.72%. The cost of choosing against the OOS
  oracle (2W-a at 1.3096) is **−0.085 of OOS Sharpe**. This is the first cadence dial in the record
  whose IS argmax reaches a 4b passer; the VOLTGT016 candidate reached 0 of 3 on U56 (idea 1771).

  **WHAT DOES NOT SURVIVE, and it is half the finding.** The window is a **gross-1.00 AND U56** object.
  At gross 0.75 — the live book's own rung — **0 of 24** cells pass on any panel at any cadence, the
  CAGR floor binding at every one (idea 1757's realised-gross reading, reproduced here). On B136 only
  2W-a clears all five legs and the IS choosers pick W/M, which fail OOS: **0 of 6** legal picks. On
  SMALL665, **0 of 24**, failing 4–5 legs at every rung. **0 of 144 cells clear path 4a** anywhere —
  the book's H2 sits 0.0007 below the live book's and its drawdown 3.9 pp deeper. Pooled over panels
  and gross, legal picks clear 4b OOS 3 of 18 and 4a OOS 0 of 18. Binding-leg census over 144 cells:
  **L5_CAGR 115 / L2_H2 60 / L3_OOS 52 / L1_H1 40 / L4_DD 35**; Q is the only rung where the DD cap is
  the majority binder (20 of 24).

  **GATES 9 of 9.** G0 the book IS `baseline.rules_v2_weights(px, 0.03, g)` at 0.000e+00; G1 the fast
  runner == `engine.backtest` on returns AND turnover at 0.000e+00; G2 the cost identity
  `r(c) = r0 − turnover·c/1e4` == the engine at 10 and 25 bps, 0.000e+00; **G3 CROSS-RUN: idea 1761's
  12 committed CAL cells (D/W/M/Q x 3 panels, gross 1.00, 10 bps) reproduce at max |Δ| 8.882e-16**;
  G4 the 2W mask partitions W (977 = 489 + 488, disjoint); G5 SMALL drops 54 tickers at
  `max_1d_move >= 1.0`, 665 kept; G6 exactly two dials; G7 no chooser statistic reads a row on or
  after 2017-01-01; G8 all 144 cells published; G9 no RNG anywhere.

  **SURVIVORSHIP.** U56 / B136 are CURRENT-constituent lists and SMALL a CURRENT sub-$2B screen, so
  every CAGR and drawdown LEVEL above is optimistic and both 4b bars are easier here than on a
  point-in-time panel. The cadence contrasts are same-tape, same-names, same-rule comparisons with
  only the trade dates moved and are first-order immune; the pass COUNTS are not.

  **STATUS.** KEEP-candidate (path 4b) for the band book at gross 1.00 on U56 at any cadence in D..M,
  memo `research/backtests/2026-09-20_band-g100-cadence_KEEP4b_MEMO.md` with exact RULES wording,
  awaiting Sunday review. **No rule change this run** (PROTOCOL rule 6); RULES.md, PROTOCOL.md,
  scan.py, bot.py and baseline.py are untouched. Evidence:
  `research/backtests/2026-09-20_band-g100-cadence-artefact_cloud.py` / `_grid.csv` / `_choosers.csv`
  / `_gates.csv` / `.txt`.

## 2026-09-20 — idea 1757 (lane C): IS THE 4b CAGR FLOOR JUST A GROSS BAR IN DISGUISE? **ANSWERED — YES ON THE LEG, NO ON THE VERDICT. KILL THE PER-UNIT RESTATEMENT AND THE NOMINAL-GROSS READING. NO NEW BOOK.**

  **THE DEFECT THIS CLOSES.** Idea 1741 found the 4b CAGR floor is the binding leg almost everywhere
  (H1 417 / H2 606 / DD 370 / **CAGR 1,049** of 1,188 cells) and idea 1761 found "ALL 52 4b passes sit at
  gross 1.00, 0 of 168 at gross 0.75". If the floor is satisfied by EXPOSURE alone, PROTOCOL rule 4b is
  selecting books for holding more beta than for any device, and every 4b count in the record is a gross
  census quoted as a verdict.

  **THE CONSTRUCTION.** Two tuned dials: GROSS LADDER (0.05..1.00 in 20 rungs — the record's prior grids
  carried three) x PANEL AXIS {U56, B136, SMALL}. Published, not tuned: DEVICE {BAND = the live RULES v2
  clause-2 device at c = 0.03 with gated weight to CASH, NOBAND = the same equal-weight book ungated},
  CADENCE {D, W, M, Q}, COST {0, 10, 25, 50} bps. **1,920 rows, every point published** to
  `_grid.csv`; both KEEP paths at every one. The second device arm is what lets the question be asked at
  MATCHED REALISED GROSS rather than at matched labels.

  **THE ANSWER, PART 1 — THE LEG IS A GROSS BAR.** CAGR is a straight line in realised gross: pooled
  `CAGR = -0.0048 + 0.1667*gross` at **R² +0.9241**, and within every panel x device **R² +0.9785 to
  +0.9999**. The floor's own pass indicator regressed on realised gross alone gives **R² +0.5689 (FULL) /
  +0.4586 (OOS)**; adding the DEVICE label buys +0.029 and adding PANEL AND CADENCE +0.033. The floor
  therefore reduces to one number per cell — the realised gross at which it is crossed: **0.600**
  (U56/NOBAND) to **0.930** (SMALL/BAND), and SMALL/BAND never crosses it at any cadence.

  **THE ANSWER, PART 2 — THE VERDICT IS NOT A GROSS CENSUS.** Realised gross explains only **R² +0.0233**
  of the 4b FULL pass indicator and **+0.0279** of the OOS one, because the DD CAP runs the OTHER WAY in
  gross (its own leg R² +0.5354, opposite sign). 4b is a two-sided EXPOSURE WINDOW: at 10 bps **all 14 of
  14** 4b FULL passers lie in realised gross **[0.606, 0.711] (width 0.104)**, **0 of the 430 cells
  outside it pass**, and only 14 of the 50 cells inside it do (sufficiency 0.280). Binding legs over 480
  cells: H1 40 / H2 180 / DD 134 / **CAGR 377**, and **217 of the 231** cells clearing every other FULL
  leg die on the floor alone.

  **THE NOMINAL-GROSS READING IS AN ARTEFACT OF A 3-RUNG LADDER.** On 20 rungs the FULL passers span
  NOMINAL gross 0.60..1.00 (5 rungs; only **28.6%** at 1.00) and collapse onto ONE realised window. The
  live band device at nominal 1.00 realises **0.710** — exactly where the ungated book at nominal 0.65
  sits. At matched realised gross (34 panel x 0.025-bin cells carrying both devices) the 4b FULL pass
  rate is BAND **0.039** vs NOBAND **0.044**, differing in **5 of 34** bins: the device label is nearly
  inert once exposure is held.

  **THE CONSTRUCTIVE HALF FAILS.** Stating the floor PER UNIT OF REALISED GROSS does remove the exposure
  content (R² on gross +0.5689 -> **+0.0004**) but removes the LEG with it: CAGR-leg failures fall
  **377 -> 6 of 480**, 4b FULL passes rise **14 -> 231** (48% of the grid), 4b OOS 20 -> 244, and **not
  one cell fails the per-unit floor alone**. A bar nothing fails is not a bar. The defensible residue is
  a REPORTING form, not a protocol change: publish a book's realised mean gross BESIDE its 4b verdict,
  never divide by it.

  **RULE 8 (2017-2026 READ ONCE).** Four IS-only choosers (IS Sharpe / IS Calmar / IS floor slack / IS
  per-unit slack) x 3 panels: **0 of 12 clear 4a OOS, 0 of 12 clear 4b OOS, 0 of 12 clear the per-unit
  4b OOS**. Eleven of 12 picks sit at nominal gross 1.00 and every one dies on the DD CAP, never on the
  floor — best pick U56 C_SHARPE -> NOBAND Q **OOS 18.84% / 1.1633 / -28.56%** (SH pass, CAGR pass, DD
  fail at a -20.23% cap) against the live book at 9.46% / 1.2766 / -12.05% and SPY at 15.26% / 0.8737 /
  -33.72%. This replicates idea 1590's "argmax IS Sharpe lands on gross 0.95-1.00 while the 4b passes sit
  lower" on a ladder six times denser.

  **CAPITAL ARM.** 13 cells clear 4b FULL *and* OOS — 12 of them the STANDING U56 band family (prior art
  from 1694/1741) and one a plain de-gross; **none clears 4a on any panel**. Cost ladder 4b FULL 19 / 14 /
  10 / 8 at 0 / 10 / 25 / 50 bps. **NO NEW BOOK; RULES.md and PROTOCOL.md untouched per rule 6.**

  **GATES 7/7.** G1 bt_np vs `engine.backtest` **1.388e-17**; G2 the BAND arm IS `baseline.rules_v2_weights`
  at **0.000e+00**; G3 exact cost reconstruction at 25 bps 1.388e-17; G4 1,920 rows; G5 NOBAND realised vs
  nominal gross 6.6e-03 (drift, diagnostic); G6 the 1694/1741 anchor replicates at **2.723e-05** (FULL
  11.53% / 1.2008 / -15.91%, OOS 12.67% / 1.2759 / -15.91%); G7 the g=0.75 BAND rung IS the live book at
  **0.000e+00**. Survivorship: U56/B136 are current constituents, SMALL a current sub-$2B screen (house
  filter, 666 columns); the leg-vs-verdict statements are within-panel and first-order immune, the pass
  COUNTS are not.
  `research/backtests/2026-09-20_4b-cagr-floor-a-gross-bar_C.py`

## 2026-09-20 — idea 1771 (lane B): IS THE STANDING VOLTGT016 4b OOS PASS DECIDABLE ACROSS THE SIGMA-CONVENTION SURFACE? **ANSWERED — NO. IT IS A KNIFE-EDGE, AND THE KNIFE IS THE TARGET RUNG. DOWNGRADE THE RECORD'S ONE STANDING KEEP-4b CANDIDATE TO PARK; KILL THE t = 0.16 CERTIFICATION. THE DIAL SURVIVES — VOL-TARGETING IS THE FIRST DEVICE IN THIS RECORD TO BEAT ITS OWN MATCHED TWIN AT SCALE. NO NEW BOOK, NO RULES CHANGE.**

  **THE DEFECT THIS CLOSES.** The record has exactly ONE standing KEEP-4b candidate heading for a
  Sunday review (`2026-09-20_voltgt-panel_KEEP4b_MEMO.md`, idea 1730). Its U56 4b OOS pass clears
  the drawdown cap by **0.37 pp**, and addendum A1 (idea 1715) already flipped it to FAIL by reading
  `sigma` one day staler — ONE alternative convention, tested ONCE. `sigma_t` is not a primitive: it
  is a convention with a LOOKBACK `L` and a STALENESS `d`, and the memo's proposed RULES wording
  (its section 9) names NEITHER. The surface those two choices span had never been mapped.

  **THE CONSTRUCTION.** Two dials, the protocol maximum: `L` {5, 10, 20, 40, 60} x `d` {0, 1, 2, 5}
  = **20 convention cells**, every grid point reported. Published, not tuned: target
  `t` {0.08, 0.10, 0.12, 0.16, 0.20}, PANEL {U56, B136, SMALL665}, COST {0, 10, 25, 50} bps. Every
  VOLTGT book is paired with its OWN constant-gross twin carrying the SAME REALISED MEAN GROSS on
  the SAME window (bisection, matched to < 1e-10). **300 VOLTGT books + 600 matched twins x 4 cost
  rungs = 2,400 scored rows, all published.** Verdict rules V1-V4 were fixed in the script header
  before the run.

  **REPLICATION FIRST.** Idea 1730's 12 published numbers reproduce at max |d| **2.8e-04** (U56 FULL
  15.61% / 1.2028 / -19.86%, OOS 15.94% / 1.2196 / -19.86%; B136 FULL 15.94% / 1.2050 / -18.76%,
  OOS 15.36% / 1.1839 / -18.76%), and A1 reproduces exactly: `d = 1` gives U56 OOS MaxDD
  **-20.7709%** against the published -20.77%, 4b OOS FAIL.

  **THE ANSWER — V1 TRIGGERED. CONVENTION PASS-SHARE 0.250.** At the candidate's own `t = 0.16`,
  only **5 of 20 convention cells clear 4b OOS on U56** and **8 of 20 on B136**. The memo's cell
  `(L = 20, d = 0)` is one of the five. A 4b pass holding at a quarter of the conventions its own
  rule wording leaves open is a property of the CELL, not of the BOOK.

  **THE CARRIER IS THE RUNG, AND 4b HERE IS A TWO-SIDED SQUEEZE.** The OOS DD-cap fail-share is
  monotone in the target — U56 **0.00 / 0.10 / 0.20 / 0.75 / 0.95** and B136 **0.00 / 0.10 / 0.25 /
  0.60 / 0.80** at t = 0.08 / 0.10 / 0.12 / 0.16 / 0.20 — while the CAGR floor binds only BELOW
  t ~ 0.10 (U56 0.45, B136 0.85 at t = 0.08). The convention-robust band is **t in {0.10, 0.12} on
  BOTH panels** (pass-share 0.90 / 0.80 on U56, 0.85 / 0.75 on B136) and the memo's rung sits on the
  wrong side of it. This is also a counter-example to the record's standing 'the CAGR floor is the
  binding leg almost every time': here `L4_DD` fails **0.40** of the whole U56 surface against
  `L5_CAGR`'s **0.09**.

  **AND IS SHARPE WALKS THE CHOOSER STRAIGHT INTO THE FRAGILE RUNG.** IS Sharpe peaks at t = 0.16 on
  both panels (U56 1.1822 at L20/d0 against 1.1339 at t = 0.12; B136 1.2301 against 1.1572), and the
  IS argmax over the whole surface is `t0.16 L20 **d1**` — the STALER convention, which is the cell
  A1 showed fails.

  **RULE 8 (2017-2026 read ONCE) — AT THE CANDIDATE'S OWN RUNG, 0 OF 3 LEGAL IS-ONLY CHOOSERS REACH
  A 4b-OOS-PASSING CELL ON U56.** `C_ISSHARPE` and `C_ISLEGS` both pick `L20 d1` -> OOS 15.76% /
  1.2012 / **-20.77% FAIL**; `C_ISDD` picks `L40 d1` -> **-20.83% FAIL**. Only the no-choice control
  `C_MEMO` passes, and `C_MEMO` is hindsight. B136 survives all three, so the pass is **panel- AND
  chooser-dependent**. With `t` free, `C_ISLEGS` lands on **t = 0.12 on BOTH panels** and clears 4b
  OOS on both (U56 `t0.12 L40 d0` 14.48% / 1.2392 / -18.06%; B136 `t0.12 L20 d0` 13.86% / 1.2220 /
  -16.01%) — a legal IS-only route to a passing cell that does not go through t = 0.16. Totals:
  **4b OOS 7 of 18 legal picks, 4a OOS 0 of 24**; SMALL665 0 of 8, every pick below SPY.

  **THE CONTROL — V4 NOT TRIGGERED, AND THIS IS THE RUN'S ONE POSITIVE RESULT.** At IDENTICAL
  realised mean gross, pooled over 100 cells per panel at 10 bps, the vol target buys OOS
  **+0.0587 of Sharpe and +6.16 pp of MaxDD on U56** (win share 0.810) and **+0.0503 / +9.44 pp on
  B136** (0.790); the matched twins clear 4b OOS **4** and **0** times against the VOLTGT books' 51
  and 47. At the memo's own cell the twin (constant gross k = 0.9338) posts OOS 17.06% / **1.1266** /
  **-27.46%** against 15.94% / 1.2196 / -19.86%. **This is the first device in this record to survive
  its own realised-gross-matched twin at scale** — BAND, MAXVOL, SPYFILT, STOP, MADIST and the eight
  sleeves all lost. It does NOT survive on SMALL665, where the plain twin wins 100 of 100
  (dSharpe -0.2516), the same panel-dependence idea 1632 found for the band.

  **COST LADDER AND SMALL CAPS.** 4b OOS passes per 100 cells: U56 58 / 51 / 38 / 29 and B136
  57 / 47 / 40 / 31 at 0 / 10 / 25 / 50 bps. **SMALL665: 0 of 100 at every cost rung and every
  convention**, confirming addendum A2 on a 5x wider surface.

  **RESIDUE, not a rules change (rule 6; RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py
  untouched):** (1) the standing KEEP-4b candidate should be read as **PARK** — an addendum saying so
  is appended to its memo; (2) **publish the CONVENTION PASS-SHARE beside any 4b verdict whose signal
  has a lookback**, the way idea 956 proposed the phase pass-share for the rebalance date — it is
  free and it separates a 0.90 book from a 0.25 book that read identically at their canonical cell;
  (3) any RULES wording naming a volatility must also name its lookback and its staleness, or it is
  not implementable without a second, uncertified choice. This run does NOT certify t = 0.12 in
  t = 0.16's place: the pass-share table is OOS-visible and cannot select a rung. It also does not
  close idea 1537, whose block bootstrap of the VOLTGT-vs-twin dMaxDD is not run here. Gates 10/10
  (fast path == `engine.backtest` at <= 3.5e-17 on all three panels at two cost rungs; twin gross
  match < 1e-10). Survivorship: U56/B136 are current constituents, SMALL665 a current sub-$2B screen
  (665 of 719 names, `max_1d_move >= 1.0` dropped) — every pass count is the OPTIMISTIC read.
  `research/backtests/2026-09-20_voltgt-sigma-convention-surface_B.py`

## 2026-09-20 — idea 1632 (lane C): IS THE BAND'S U56-ONLY SURVIVAL A PANEL EFFECT OR A NAME-COUNT EFFECT? **ANSWERED — PANEL. KILL THE NAME-COUNT HYPOTHESIS; CONFIRM IDEA 1617. NO NEW BOOK.**

  **THE DEFECT THIS CLOSES.** Idea 1617's one convincing survivor — the live band c = 0.03 beating its
  realised-gross-matched de-gross twin, on U56 alone — is the live book's ONLY matched-exposure win in
  the record, and it was confounded. U56 is both a different PANEL and the SMALLEST panel by NAME COUNT,
  and under the live convention (gross / N_priced per eligible name, gated-out weight to cash) the band
  is a BREADTH device: one gated name moves realised gross by 1/56 on U56 and 1/665 on SMALL. A contrast
  shrinking like 1/N reproduces 1617's whole cross-panel ordering with no panel content at all.

  **THE CONSTRUCTION.** Two dials: N_NAMES (uniform seeded draws without replacement from each panel's
  own traded columns; ladder 20/36/56/100/136/300 truncated at panel size, plus each panel's FULL set as
  the ALL rung) x BAND c {0.00, 0.03, 0.06, 0.10}. Published, not tuned: PANEL {U56, B136, SMALL},
  DRAW (24 per rung, **291 draws**), COST {0, 10, 25, 50} bps. Every band book is paired with its OWN
  twin — the same names ungated, scaled by a constant k solved so the twin carries the SAME REALISED mean
  gross to machine precision (closed form: inside a segment the scaled book's gross path is
  `kGP / (kGP + 1 - kGF0)` with P, F0 independent of k; gated at G11). **1,164 band books + 1,164 twins
  x 4 cost rungs = 4,656 rows, all published.**

  **REPLICATION FIRST.** The ALL rungs reproduce 1617 to the published digit: U56 dSharpe **+0.0827 FULL
  / +0.1499 OOS**, B136 **-0.0161 / +0.0136**, SMALL **-0.0461 / -0.0520**.

  **THE ANSWER — THE DIRECTION IS THE OPPOSITE OF THE HYPOTHESIS.** H0 required mean dSharpe to DECREASE
  in N; it decreases at **9 of 48 ladder steps — 0 of 8 on U56**, 1 of 16 on B136, 8 of 24 on SMALL. At
  the matched rung **N = 56, 0 of 48 subsamples reach U56**: B136 draws land at FULL -0.0371 (sd 0.0412)
  and SMALL at -0.0851 (sd 0.0654) against U56's +0.0827 (z **+2.91 / +2.57**), and OOS 0.000 / 0.000
  (z **+3.79 / +3.27**); same at the plain 200d gate c = 0.00. Subsampling **U56 DOWN SHRINKS** the
  contrast: +0.0827 (N=56) -> +0.0610 (36) -> +0.0515 (20). SPY is not the mechanism — U56 draws WITHOUT
  SPY score +0.0592 against +0.0542 with it.

  **WHICH LEG: THE PANEL DEPENDENCE IS ENTIRELY IN THE RETURN LEG.** The band's DRAWDOWN credit is near
  panel-invariant and flat in N above 56 (c = 0.03: U56 **+4.34 pp**, B136 +5.93, SMALL +6.45 — U56 gets
  the SMALLEST credit). Its CAGR cost is flat in N inside a panel and a ~**3x effect ACROSS** them
  (U56 **-0.72 pp/yr**, SMALL -1.46, B136 **-1.99**). The band does the same thing to drawdown everywhere
  and only costs U56's names less return.

  **CAPITAL ARM — THE WIN IS REAL AND STILL NOT CAPITAL-WORTHY, AND THE TWIN IS THE BETTER 4b BOOK.** Of
  1,164 band books at 10 bps: 19 clear 4a FULL, 5 clear 4b FULL, **3 clear 4b FULL *and* OOS** (all U56,
  N=20, draws 3/18) and none of those clears 4a. Their own matched TWINS clear 4b FULL **19 (U56) / 53
  (B136)** against the band books' 4 / 1. The 4b CAGR floor fails on **0.996** of band books (DD cap
  0.069). Cost ladder 4b FULL: 6 / 5 / 4 / 0 at 0 / 10 / 25 / 50 bps.

  **RULE 8 (2017-2026 read ONCE).** Three IS-only choosers x 3 panels: **0 of 9 picks clear 4a OOS and
  0 of 9 clear 4b OOS**, every one on the CAGR floor (8 of 9 pass the DD cap). The live inheritance is
  the best OOS contrast in the run (U56 +0.1499) and still delivers OOS 9.46% / 1.2769 / -12.05% against
  SPY 15.26% / 0.8738 / -33.72% and a 10.68% floor. The 3 passing books are random 20-name subsets no
  chooser reaches: hindsight, recorded as such.

  **RESIDUE, not a rules change (rule 6; PROTOCOL.md and RULES.md untouched):** the band's drawdown
  credit is a CONSTANT OF THE CONSTRUCTION and should stop being re-priced panel by panel; its RETURN
  cost is the only panel-dependent leg, so "the band works on panel X" is a claim about what the gate
  costs X's names in return and should be written that way. Gates 19/19 (G1/G2/G3/G11 vs
  engine.backtest 0.000e+00-6.2e-15; G4 gross match 0.000e+00; G6 clean). Survivorship: U56/B136 are
  current constituents, SMALL a current sub-$2B screen (54 names dropped at max_1d_move >= 1.0, 665
  remain); the headline is a within-draw contrast and first-order immune, the 4b counts are not.
  `research/backtests/2026-09-20_band-u56-panel-or-namecount_C.py`

## 2026-09-20 — idea 1627 (lane cloud): IS EVERY SLEEVE AND HEDGE IN THE RECORD A CARRY CLAIM WEARING AN INSTRUMENT? **ANSWERED — YES. KILL THE SLEEVE FAMILY; KEEP ONE ACCRUAL LINE. NO NEW BOOK.**

  **THE DEFECT THIS CLOSES.** Idea 1602 took ONE instrument, SHY, and found its whole contribution
  to the live band book is reproduced by a zero-duration accrual at the same realised rate. But the
  record has routed weight into SEVEN OTHERS — IEF, TLT, GLD, TIP, HYG, LQD, UUP — and every one of
  those routings is written as a claim about the INSTRUMENT rather than about the rate it earns.

  **THE CONSTRUCTION.** Live RULES v2 band book (gross 0.75, weekly, 10 bps, t+1); fraction F of the
  gated-out NAV routed to a sleeve. ETF arm = the instrument marked to market. MATCH arm = a
  constant daily accrual compounding to THAT INSTRUMENT'S OWN realised CAGR on the same tape, same
  names, same days, same turnover charge — so `ETF - MATCH` is the instrument's price path and
  nothing else. MATCH_IS sets the rate from 2009-2016 only and is the arm rule 8 uses. Dials: F
  {0, 0.25, 0.50, 0.75, 1.00} and the instrument (8). 3 panels x 8 x 5 x 3 = **360 priced cells**,
  all published.

  **THE ANSWER.** **0 of 24 panel x instrument cells survive at F = 1.00**; 12 of 96 over all F,
  every one at F <= 0.50 where the sleeve is too small to matter. Mean dSharpe / dMaxDD: SHY
  **+0.0012 / +0.38 pp** — the only positive, and an independent replication of 1602's +0.0009 on a
  wider set — then IEF -0.0101/-3.99, UUP -0.0430/-0.11, TIP -0.0529/-3.39, LQD -0.1278/-7.81, TLT
  -0.1422/-13.21, HYG -0.2482/-8.75, GLD -0.2731/-3.94. The deficit is MONOTONE in F for 7 of 8.
  TLT at F = 1.00 costs -20.3 pp of MaxDD on U56 and -28.3 pp on SMALL against an accrual paying
  TLT's own 1.08 %/yr.

  **THE ONE 4b-CLEARING INSTRUMENT IS ALSO THE WORST SUBSTITUTION FAILURE.** Every ETF-arm 4b pass
  in the run is GLD (U56 and B136 at F = 0.50/0.75/1.00 clear 4b FULL *and* OOS; U56 F = 0.75 OOS
  15.12 % / 1.4002 / -14.98 % against SPY 15.26 % / 0.8738 / -33.72 %). An accrual at gold's own
  9.51 %/yr beats it by +0.63 of Sharpe at F = 1.00 with 7.1 pp less drawdown: the pass is CARRY
  wearing a hedge's name.

  **RULE 8 (2017-2026 read ONCE).** Two IS-only choosers x 3 panels: **the ETF arm's 6 picks clear
  4a OOS 0 times and 4b OOS 0 times.** U56 and B136 both pick LQD F = 1.00 -> OOS 1.0729 / -24.31 %
  and 0.9309 / -25.25 % against a live book at 1.2769 / -12.05 % and 1.1019 / -12.24 %; every pick
  roughly DOUBLES the live drawdown. The 4b-clearing GLD cells sit at IS-Sharpe rank **#35/#39/#40
  of 40** (U56), **#26/#37/#40** (B136), **#38/#39/#40** (SMALL) — dead last, so no chooser reaches
  them. MATCH_IS's OOS 4a/4b passes run on a RISKLESS accrual of 8.78 %/yr (HYG IS CAGR) and
  7.57 %/yr (TLT IS CAGR) and are labelled fiction, not candidates.

  **RESIDUE, not a rules change (rule 6; PROTOCOL.md and RULES.md untouched):** a sleeve should be
  written as an ACCRUAL RATE, and any instrument proposed above that accrual must clear the
  `ETF - MATCH` contrast before its name enters the clause. Gates 19/19. Survivorship: B136/SMALL
  are current constituents; SMALL drops 54 names with `max_1d_move >= 1.0` (665 remain).
  `research/backtests/2026-09-20_every-sleeve-a-carry-claim_cloud.py`

## 2026-09-20 — idea 956 (lane cloud): DOES A PHASE-AVERAGED 4b VERDICT CHANGE WHICH BOOKS PASS? **ANSWERED — BARELY, AND ONLY IN ONE DIRECTION. KILL THE PROTOCOL CHANGE; PARK ONE FREE REPORTING LINE. NO NEW BOOK.**

  **THE CORPUS.** Six books the record has certified or is standing on — TOP20 (the 2026-09-04
  first KEEP-4b shape), BAND03_G075 (live RULES v2), BAND10_G100 (1719/896's U56 passer), EWELIG,
  MAXVOL060 (1617's PARK) and VOLTGT016 (the standing KEEP-4b candidate found by idea 1730 THIS
  DAY) — x 3 panels x 26 phases (DOM21 + DOW5) x 4 cost rungs = **1,872 scored books**, all
  published. Dials: phase grid and averaging rule. **MEAN / MEDIAN / MIN / SHARE50 are ESTIMATORS
  and can never BE a KEEP** — no allocation of capital produces a median-of-Sharpes; TRANCHE (1/P
  of NAV per phase-book, re-levelled daily) is the only tradable arm.

  **THE ANSWER.** Over 144 (panel x grid x book x cost) cells CANON certifies 30 on 4b FULL.
  **MEDIAN passes 25, keeps 25 of 30 and newly certifies 0** (disagreement 0.035 FULL / 0.049 OOS);
  MEAN passes 33, keeps 25 and **newly certifies 8**; MIN 16; SHARE50 25; TRANCHE 38, keeping
  30 of 30. **The averaging rule is not a neutral estimator choice — MEDIAN only de-certifies and
  MEAN only loosens** — which is itself the reason not to adopt one silently. At the 10 bps primary
  rung MEDIAN and CANON disagree on **1 of 36** cells.

  **AND THAT ONE CELL IS THE RECORD'S OWN FIRST KEEP-4b BOOK.** U56/DOM21/**TOP20** passes 4b at the
  canonical month-end and **fails at 16 of its 21 DOM phases** (phase pass-share **0.238**),
  de-certifying at all four cost rungs; the only other loss is the same book at B136/DOW5/0 bps.
  **Every de-certified cell in the run is TOP20.** Every other certified cell in the corpus has a
  phase pass-share of **0.800-1.000**.

  **CONSTRUCTIVE RESIDUE (Sunday review only; PROTOCOL.md untouched):** publish the **PHASE
  PASS-SHARE** beside every 4b verdict. It is free — it falls out of the same 21 runs a phase check
  already makes — it is a statement about the book rather than about an estimator, and on this
  corpus it is the one number that separates the record's single fragile 4b certification from
  every robust one.

  **THE STANDING KEEP-4b CANDIDATE SURVIVES, WITH A LIMIT NAMED.** VOLTGT016 clears 4b FULL and OOS
  at **5 of 5 weekly phases on B136 and 4 of 5 on U56** and holds under CANON, MEAN, MEDIAN,
  SHARE50 and TRANCHE alike. Its DOM21 failure is NOT a phase result: on a monthly cadence its OOS
  MaxDD blows out to **-24.2 % (U56) / -26.1 % (B136)** against **-19.9 % / -18.8 %** weekly, so the
  weekly rebalance is load-bearing and must stay in any RULES wording. Addendum appended to its memo.

  **RULE 8 (2017-2026 read ONCE): the phase is a KILL as a dial.** Choosing the rebalance date in
  sample is worth **-0.0215** of OOS Sharpe on DOM21 (3 of 18 wins) and **-0.0058** on DOW5 (7 of
  18); the tradable TRANCHE buys -0.0400 (DOM21) and +0.0021 (DOW5) against CANON — i.e. nothing.
  Both KEEP paths per-phase @10 bps: DOM21 4a FULL 0/378, 4a OOS 7/378, 4b FULL 31/378, 4b OOS
  31/378; DOW5 1/90, 11/90, 32/90, 32/90. Binding legs among the 405 4b failures: **L4_DD 0.654**,
  L5_CAGR 0.637, L2_H2 0.462, L3_OOS 0.412, L1_H1 0.240 — idea 944's ranking reproduced on an
  independent corpus. Gates 28/28, including a cross-run replay of idea 1730's committed VOLTGT
  memo at max|d| 0.0000 on both panels.
  `research/backtests/2026-09-20_phase-averaged-4b-verdict_cloud.py`

## 2026-09-20 — idea 1738 (lane C): IS THE WINDOW-MATCHED 4a TEST TESTABLE ON A SOMETIMES-OFF CORPUS? **ANSWERED — YES, AND THE TWO WINDOW CONVENTIONS ARE NOT THE SAME TEST. KILL the ACTIVE-DIFF restatement; the ACTIVE-GROSS one is a NO-OP. NO NEW BOOK.**

  **THE DEFECT THIS CLOSES.** Idea 1631 priced three restatements of PROTOCOL rule 4a and could not
  adjudicate the first — the WINDOW-MATCHED one — because its corpus had no variance on the only
  axis that matters: every committed book is deployed on ~100% of days (act-share 1.000 at 50 of 52
  cells) and differs from the incumbent's book at diff-share 1.000 at 44 of 52. A window-matched
  test can only differ from a full-window test when the window is genuinely SHORTER, so 1631's
  verdict on (i) was a statement about its corpus, not about the restatement.

  **THE CORPUS 1631 LACKED.** Four SWITCH families — SPYFILT / STOP / BREADTH / VOLTGT, the four the
  idea names — each a causal market-state statistic thresholded at the IS-window quantile that puts
  its ON-share on a **0.30-0.90 ladder**; two ARMS turn a switch into a book: **CASH** (hold the
  incumbent when ON, sit flat when OFF -> act-share = s) and **OVER(f)** (BE the incumbent when OFF,
  hold f x the incumbent when ON -> diff-share = s). 7 shares x 2 arms (f = 0.25/0.50/0.75) x 3
  panels = **423 books, 336 real + 84 NULL** (seeded uniform switches at the same shares, no
  information). Realised **act-share 0.170-1.000, diff-share 0.000-0.914**; 420 of 423 cells sit
  strictly inside (0.05, 0.95) on the diff axis. Weekly, 10 bps, t+1, long-only, max gross 0.7373.

  **THE ANSWER, AND IT SPLITS.** **R1a (the device's DEPLOYED window) moves 1 of 336 verdicts** at
  every MINN rung {250, 500, 750, 1000, 1500} — one SMALL SPYFILT|CASH|s=0.90 cell missing by
  dSharpe **-0.0044** — so matching the window to realised gross is a distinction without a
  difference even across 0.17-1.00 of coverage. **R1b (the days the book actually DIFFERS from the
  incumbent) flips ALL 38 R0 passes to FAIL and passes 0 of 336 at every rung**, with the lowest
  divergence at diff-share 0.1-0.2. The two conventions 1631 treated as one restatement are two
  different tests, and only one of them is a restatement of 4a at all.

  **WHY — AND IT IS MECHANICAL, NOT TAPE.** On the diff window the DD leg still holds **38 of 38**
  (the deviation is +5.30 pp SHALLOWER) and **both Sharpe legs fail 38 of 38**, because a de-gross
  deviation leaves Sharpe near-invariant on the very days it is applied: median |dSharpe| runs
  **0.0830 / 0.0279 / 0.0091 at f = 0.25 / 0.50 / 0.75**, shrinking with (1-f), and what is left is
  the cash drag, i.e. negative. This is NOT a power failure — the paired circular-block t (63d, 400
  draws, seed 20260920, inherited conventions) of mean excess on the diff window reaches **|t| > 2
  at 258 of 336**, and **332 of 336 are NEGATIVE with 0 of 336 positive at |t| > 2**. The window can
  tell the books apart; its uniform answer is that no deviation in the corpus pays for itself on its
  own days. NULL leakage is 0 of 84 under every test at every rung.

  **RULE 8 (2017-2026 read ONCE).** R0 and R1a pick the IDENTICAL book on all three panels — U56
  BREADTH|OVER f=0.25|s=0.40 OOS **5.79% / 1.1318 / -7.69%**; B136 STOP|OVER f=0.50|s=0.60 **5.67% /
  0.9876 / -8.60%**; SMALL VOLTGT|OVER f=0.25|s=0.60 **4.13% / 0.6689 / -10.83%**, the run's only OOS
  4a pass — while **R1b selects NOTHING on IS on any panel at any (MINN, f)**, so it cannot serve as
  a chooser; f* had to fall back to the current rule's IS argmax, which is itself the finding.
  Both KEEP paths over the corpus: 4a FULL **38/336**, 4a OOS 39/336, **4b FULL 0/336, 4b OOS 0/336**.
  Bars: SPY FULL 15.12% / 0.8843 / -33.72%, OOS 15.26% / 0.8737 / -33.72%; RULES v2 OOS 9.46% /
  1.2766 / -12.05% (U56), 7.85% / 1.1017 / -12.24% (B136), 3.64% / 0.5458 / -14.16% (SMALL).
  GATES **24/24** (cost axis exact 0.00e+00 x3; baseline == live `rules_v2_weights` 0.00e+00 x3;
  the OVER f=1.00 control reproduces the incumbent 0.00e+00 x3; hard-truncated IS replay identical
  x3; no leverage). Survivorship (rule 9): current-constituent panels, absolute levels are upper
  bounds, every claim is a within-tape contrast.

  **CONSTRUCTIVE RESIDUE (proposed for Sunday review only; PROTOCOL.md, RULES.md, scan.py, bot.py
  and baseline.py NOT modified).** Leave rule 4a as written — this confirms 1631's KILL on a corpus
  that could have refuted it. But the run turned up the one deviation statistic in the record that
  ADJUDICATES at this sample length: the diff-window MEAN-EXCESS t, decisive at 258 of 336 cells,
  against idea 1511's 0 of 240 for a MaxDD contrast and idea 1709's 12 of 27 for an IS-Sharpe
  margin. A device's deviation should be quoted as that t, on the days it is actually a deviation,
  rather than as a full-window Sharpe delta — and on that ruler 332 of 336 devices in this corpus
  are negative.

## 2026-09-20 — idea 1709 (lane C): IS THE RULE-8 PICK INSTABILITY A PLATEAU ARTEFACT OR A REAL PREFERENCE? **ANSWERED — A PLATEAU ARTEFACT, AT EVERY SINGLE MOVE EVENT. BUT THE PLATEAU IS A HAZARD, NOT A COMFORT. KILL (capital), NO NEW BOOK.**

  **THE DEFECT THIS CLOSES.** Idea 720 (earlier today) convicted rule 8's chooser: a year-deleted
  IS window moves the pick at 8 of 12 chooser x panel pairs. But that was measured as a COUNT OF
  MOVES, and a count cannot distinguish a FLAT surface (ties reshuffling, a statement about the
  grid) from a REAL preference overturned by one year of tape (a statement about the tape, and a
  much more serious one). 1709 computes the statistic 720 never did: the MARGIN between the
  argmax and its rival, against that same margin's own leave-one-IS-year-out spread.

  **CONSTRUCTION.** Two dials and no more: **band c {NOGATE, 0.00, 0.01, 0.02, 0.03, 0.05, 0.075,
  0.10, 0.15, 0.20}** x **gross G {0.05, 0.10, ..., 1.00}** = 200 books per panel on **U56 /
  B136 / SMALL** = **600 REAL BOOKS**, every one in `grid.csv` with FULL / H1 / H2 / IS / OOS
  metrics and both KEEP-path verdicts. Weekly, 10 bps, next-day execution, no leverage (max
  realised gross 1.0000 over all 600). Deletion convention identical to idea 720: the book is
  NEVER re-run, the calendar year is removed from the SCORED RETURN STREAM. Gates 21 of 21, incl.
  a bit-for-bit replay of `baseline.rules_v2_weights` (max|d| < 1e-12) and a cross-run match on
  all three committed U56 cells (LIVE 8.62%/1.2011/-12.05%, PICK 11.72%/1.1726/-16.30%, PARK
  11.42%/1.1188/-19.75%).

  **THE METHOD POINT, AND IT MATTERS.** The naive comparator — the LOYO SD of the winner's OWN IS
  Sharpe — is the WRONG scale by three orders of magnitude (0.1681 against a paired 0.0001): the
  winner and its rival move together when a year is deleted, and only their DIFFERENCE decides the
  pick. Every t here is on the PAIRED SD, with a 400-draw random-contiguous-252-day null published
  beside it. The second trap: the rank-2 rival is the SAME BAND one gross rung down — a
  near-duplicate, mean margin **0.0002** of IS Sharpe — so the rank ladder measures GRID
  RESOLUTION, not preference. The ladder that adjudicates is the best cell in each OTHER band.

  **THE ANSWER.** **0 of 10 leave-one-IS-year-out pick moves goes to a rival the undeleted IS
  window could resolve** at |t| > 2 (median |t| at a move event **0.292**, max **1.123**); 10 of
  22 single-year refits move the argmax — 720's instability, reproduced on a 200-cell grid — and
  **10 of 10 moves cross to a different BAND**, never to the adjacent gross rung. On the
  cross-band ladder only **12 of 27** rivals are resolved (median |t| 1.65, mean margin 0.0715
  against a mean paired SD of 0.0378), and only **3 of 9** of the record's committed (panel, cell)
  pairs are distinguishable from their own panel's IS argmax — B136's committed 2026-09-19 PICK
  sits 0.0011 of IS Sharpe below that panel's argmax against a paired SD of 0.0493, t **+0.02**.

  **BUT FLATNESS IS NOT COMFORT — THE CAPITAL HALF.** The IS window cannot separate its argmax
  from **100 of 200 cells on average (50.2% of the grid)**, and those IS-indistinguishable cells
  do NOT behave alike out of sample: OOS CAGR runs **0.28% to 18.27%**, OOS MaxDD **-0.84% to
  -44.38%**, and only **10 of 301** plateau cells clear 4b OOS. Three LEGAL IS-only tie-breaks of
  the SAME tie (C_PLAT_LO / MID / HI) spread OOS CAGR by **8.97%** on average. The chooser is not
  choosing; the tie-break is.

  **RULE 8 (2017-2026 read ONCE per chooser).** 4 of 21 chooser x panel picks clear 4b OOS, **2 of
  21 clear 4a OOS**; mean OOS Sharpe 0.9472 against SPY's 0.8738. U56 C_SHARPE reaches
  `c0.10/g1.00` (OOS 12.14% / 1.1940 / -16.30%, 4b OOS PASS) — the record's ALREADY-COMMITTED
  pick, not a new book. Both KEEP paths over all 600 cells: 4a FULL 59 (all SMALL), 4a OOS 69,
  4b FULL 26, 4b OOS 31, BOTH 20. OOS bars: SPY 15.26% / 0.8738 / -33.72%; RULES v2 U56 9.46% /
  1.2769 / -12.05%, B136 7.85% / 1.1019 / -12.24%, SMALL 3.64% / 0.5459 / -14.16%.
  **NO NEW KEEP CANDIDATE IS PROPOSED** — every 4b-clean cell sits in the known high-gross region
  the record already holds, and this run's own measurement says no legal IS-only chooser can be
  trusted to land on it.

  **CONSTRUCTIVE RESIDUE (proposed for Sunday review only; PROTOCOL.md, RULES.md, scan.py, bot.py
  and baseline.py NOT modified).** Rule 8 should say WHICH argmax and publish its margin: quote
  every walk-forward pick with the paired leave-one-IS-year-out t against its best CROSS-BAND
  rival. Below |t| = 2 the pick is a tie-break and should not be quoted as a preference. This
  agrees with lane B's independent idea 1713 the same day from the other direction — robustness
  on the IS window buys nothing OOS precisely BECAUSE the IS objective cannot see the dial it is
  picking.

  **SURVIVORSHIP (rule 9).** U56 / B136 are current-constituent lists; SMALL is a current-screen
  sub-$2B panel with every name whose max 1-day move >= 1.0 dropped (54 dropped, 666 columns
  remain). Absolute levels are UPPER BOUNDS; the object measured is the SEPARATION of two cells
  on one fixed tape. Script
  `research/backtests/2026-09-20_rule8-pick-margin-vs-deletion-noise_C.py`.

## 2026-09-20 — idea 1713 (lane B, run 2): DOES A DELETION-ROBUST RULE-8 CHOOSER BEAT PLAIN IS-ARGMAX OUT OF SAMPLE? **ANSWERED — NO. ROBUSTNESS MOVES THE CELL AT 1 OF 9 PANEL x CHOOSER PAIRS AND THAT ONE MOVE IS A LOSS THAT DESTROYS THE ONLY 4b OOS PASS. KILL; NO NEW BOOK. THE REASON IS THAT THE IS OBJECTIVE CANNOT SEE THE DIAL IT IS PICKING.**

  **THE DEFECT THIS CLOSES.** Idea 720 (earlier today) acquitted the 4a/4b verdicts under a
  single-calendar-year deletion (2 of 260 and 0 of 260 move) but convicted the CHOOSER: a
  year-deleted IS window moves the rule-8 pick at 8 of 12 chooser x panel pairs and the OOS 4b
  verdict at 5 of 12, while 44 of 100 perturbed picks clear 4b OOS and 0 of 100 clear 4a. That
  left an open constructive question — the perturbation ensemble CONTAINS passing books the
  argmax walks past, so does choosing a DELETION-ROBUST cell on the same IS window buy anything?

  **CONSTRUCTION.** Two dials and no more: **band c {NOGATE, 0.00, 0.03, 0.10}** x **gross G
  {0.30,0.40,...,1.00}** on **U56 / B136 / SMALL** = **96 real books**, every one in `grid.csv`.
  Weekly, 10 bps, next-day execution. Four choosers, all seeing 2009-2016 ONLY — **A_SHARPE**
  (argmax IS Sharpe, what the record uses), **R_MEAN**, **R_MIN** (worst case) and **R_MODAL**
  over the 8 leave-one-IS-year-out deletions — plus an **ORACLE_OOS** published as the upper
  bound, never a pick. 2017-2026 read ONCE per chooser. Deletion convention identical to idea
  720: the book is never re-run, the year is removed from the SCORED RETURN STREAM. Gates:
  RULES v2 reproduces the record's committed U56 / B136 / SMALL cells (8.62%/1.2010/-12.05%,
  7.96%/1.0972/-12.24%, 4.66%/0.7184/-12.48%) and the U56 A_SHARPE pick reproduces the
  2026-09-19 rule-8 PICK at 11.72%/1.1724/-16.30% against 720's committed 11.72%/1.1726/-16.30%.

  **(1) THE LITERAL ANSWER IS NO.** Robustness moves the chosen cell at **1 of 9** (panel x robust
  chooser) pairs. The one move is a LOSS: U56 R_MIN goes (0.10, G 1.00) -> (NOGATE, G 1.00),
  **dOOS Sharpe -0.0676**, and turns the run's only 4b OOS pass into a fail. 4b OOS: A_SHARPE
  **1/3**, R_MEAN 1/3, R_MODAL 1/3, R_MIN **0/3**. 4a OOS **0/3** for all four.

  **(2) THREE OF THE FOUR CHOOSERS ARE THE SAME FUNCTION.** Over all 96 cells the leave-one-year-out
  MEAN Sharpe equals the plain IS Sharpe to **max |diff| 0.0032** (mean 0.0010). Deleting one of
  eight years cannot move an eight-year Sharpe enough to re-rank anything, so R_MEAN and R_MODAL
  are arithmetically A_SHARPE. Only R_MIN differs — and what worst-case robustness selects for is
  **less gating** (NOGATE), not better out-of-sample behaviour.

  **(3) WHY — AND THIS IS THE FINDING.** The IS objective is **near-invariant to the dial it is
  choosing**. IS Sharpe moves **0.0015-0.0106** across the ENTIRE gross ladder (G 0.30 -> 1.00)
  against a leave-one-year-out SD of **0.090-0.248**: a ratio of **0.010-0.075**. The same ladder
  moves **OOS MaxDD by 10.9-29.2 pp** and **OOS CAGR by 3.9-12.9 pp**. The argmax-vs-runner-up
  margin is **0.0002-0.0013** of Sharpe — **0.09% to 1.4% of the deletion SD**. So IS-argmax pins
  to **G = 1.00 on 3 of 3 panels** while the OOS-Sharpe oracle sits at **G = 0.30 on 3 of 3**, and
  idea 720's "the pick moves under a deleted year" is on this grid a **PLATEAU** fact: 7 / 4 / 7 of
  8 LOYO years reproduce the undeleted argmax, and the years that differ separate cells by ~1% of
  a deletion SD. No re-weighting of a Sharpe objective can fix this, because the flatness is
  arithmetic (scaling weights barely moves Sharpe), not statistical.

  **(4) THE BAND MARGIN, BY CONTRAST, IS REAL AT TWO PANELS.** argmax-vs-best-OTHER-band is
  **0.30 deletion-SDs on U56** (c 0.10 over NOGATE) and **0.87 on SMALL** (NOGATE over c 0.10),
  against 0.012 on B136. The chooser can resolve WHICH BAND; it cannot resolve WHICH GROSS.

  **WHAT THE RECORD SHOULD DO.** Stop trying to stabilise rule 8's chooser by robustifying its
  objective — the instability is a flat surface, and the one robust variant that does move loses.
  **Proposed (NOT adopted here; PROTOCOL.md, RULES.md, scan.py, bot.py and baseline.py are all
  unmodified): rule 8 should pick the BAND by Sharpe and pick GROSS by 4b's own legs** — the
  feasible interval idea 1695 measured at mean width 1.11 of 20 rungs — rather than by the same
  argmax. That is idea **1705**, filed this run. Grid-wide this run: FULL 4a **0/96**, FULL 4b
  5/96, OOS 4a 5/96, OOS 4b 8/96. **SURVIVORSHIP:** U56, B136 and SMALL are all current
  constituents; every number above inherits that bias.

## 2026-09-20 — idea 720 (lane cloud): DOES ANY PUBLISHED IS-vs-OOS DRIFT SURVIVE A SINGLE-YEAR DELETION? **ANSWERED — NO, 12 OF 15 REVERSE SIGN, BUT THAT IS A KILL OF THE STATISTIC, NOT A FINDING ABOUT ANY YEAR: THE DRIFT IS INSIDE ITS OWN DELETION NOISE AT 11 OF 15 PAIRS AND THOSE ARE EXACTLY THE 11 THAT REVERSE. THE 4a/4b VERDICTS ARE ACQUITTED (2 OF 260 MOVE); RULE 8'S PICK IS NOT (8 OF 12 PAIRS MOVE). NO RULES CHANGE.**

  **THE DEFECT THIS CLOSES.** Idea 536 found that deleting calendar 2020 alone reverses idea 301's
  MA-residual drift on B136 (-0.2423 -> +0.1245) and U56 (-0.0222 -> +0.3213). Nobody had asked
  whether that is a fact about 2020 or a fact about the resolution of a drift statistic at this
  sample length. This lane's idea 1695, pushed earlier today, sharpened the stake: 4b is a
  two-leg gross interval whose mean feasible width is 1.11 of 20 rungs, so every standing verdict
  in this repository is a knife edge and one year of tape is a large perturbation.

  **CONSTRUCTION.** Two dials: **YEAR {NONE, 2008..2026}** x **BOOK {LIVE (band 0.03 @ G 0.75, as
  traded), PICK (band 0.10 @ 1.00, the 2026-09-19 rule-8 pick), PARK (no gate @ 0.65, idea 1695's
  one-rung 4b passer), EW100, EW050}**, on U56 / B136 / SMALL = **275 re-scorings**, every one in
  `grid.csv`. Deletion convention, stated once and never varied: **the book is never re-run** — it
  is run once on the full tape and the calendar year is removed from the SCORED RETURN STREAM,
  which isolates "is this verdict carried by one year?" from "would the signal have differed?".
  SPY's bars and the live book's 4a bar are re-scored under the SAME deletion, so no cell compares
  two different tapes. Gates 19 of 19, including an exact reproduction of today's committed U56
  LIVE / PICK / PARK cells (8.62%/1.2011/-12.05%, 11.72%/1.1726/-16.30%, 11.42%/1.1188/-19.75%),
  a partition assert at every cell, and a checked (not assumed) IS/OOS attribution: 0 of 260
  deletions straddle the 2016/2017 boundary and IS-side deletions leave the OOS number bit-identical.

  **(1) THE LITERAL ANSWER IS NO.** **12 of 15** (panel, book) drifts (OOS Sharpe minus IS Sharpe)
  reverse sign under at least one single-year deletion, with a mean span of **0.5477** of Sharpe
  over the 19 deletions. U56's no-gate books reverse at 9 or 10 of 19 years; B136's LIVE book at 10.

  **(2) AND THAT IS A FACT ABOUT THE STATISTIC, NOT ABOUT ANY YEAR.** Deleting a RANDOM contiguous
  252-day block (500 draws, seed 20260920) moves the same drift with SD **0.1191** of Sharpe.
  Against that SD the UNDELETED drift reaches |t| > 2 at only **4 of 15** pairs (median |t| 0.57,
  max 2.75), and only **21 of 260** single-year deletions exceed 2 block-SDs — **8.1% against a
  nominal 5%**, i.e. barely above chance. The years that do reach it are **2013, 2022 and 2011** —
  not the 2020 idea 536 headlined.

  **(3) THE CONSTRUCTIVE HALF: REVERSAL IS PREDICTED EXACTLY BY RESOLUTION.** Of the 11 pairs whose
  drift does NOT clear 2 block-SDs, **11 of 11 reverse** (mean 6.00 reversals of 19 deletions). Of
  the 4 that do clear it — all SMALL, the genuine IS->OOS collapse at t -2.40 to -2.75 — **1 of 4**
  reverses (mean 0.25). A statistic that does not differ from zero at its own deletion resolution
  has no sign to reverse. **Proposed reporting rule (NOT adopted here; PROTOCOL.md is unmodified):
  publish |drift| / block-deletion SD beside every IS-vs-OOS drift claim, and stop quoting the sign
  below |t| = 2.**

  **(4) THE VERDICTS ARE ACQUITTED — DO NOT CONFLATE THE TWO.** Only **2 of 260** single-year
  deletions move a 4b FULL verdict (0.8%, against the random-block null's own 1.0%), 6 move a 4b
  OOS verdict, and **0 of 260** move a 4a verdict. Both 4b movers are the deletion of **2020**
  acting on idea 1695's PARK book — U56 pass -> fail, B136 fail -> pass — which is precisely the
  one-rung knife edge this morning's PARK memo flagged. Everything else holds: the live book fails
  4b on the CAGR floor at every deletion on U56 and B136, and SMALL fails at 5 of 5 books always.

  **(5) RULE 8 IS WHERE THE FRAGILITY ACTUALLY LIVES.** Re-fitting the chooser on a year-deleted IS
  window and reading 2017-2026 once per deletion: the PICK changes at **8 of 12** chooser x panel
  pairs (21 of 88 deletions) and the OOS 4b verdict changes at **5 of 12**. Over all 100 picks the
  mean OOS Sharpe is 0.9838, 44 of 100 clear 4b OOS and **0 of 100 clear 4a**. On U56, C_MEMO's
  undeleted pick is the PARK book (OOS 11.83% / 1.1269 / -19.75%) and two IS-year deletions move it
  to LIVE; C_CAGR's pick moves between PICK and PARK at 4 of 8 years.

  **WHAT THE RECORD SHOULD DO.** Retire the IS-vs-OOS drift as a quotable stability statistic — at
  this sample length it is unresolvable at 11 of 15 of the places the record quotes it, and its
  sign is a coin toss there. Keep quoting the 4a/4b verdicts, which survive a one-year deletion at
  258 of 260 and 260 of 260 respectively. And read any rule-8 pick knowing that one year of IS tape
  moves it two-thirds of the time: the procedure that would promote a book to RULES is less stable
  than the test it is feeding. No RULES change is proposed and none of RULES.md, PROTOCOL.md,
  scan.py, bot.py or baseline.py was modified.

## 2026-09-20 — idea 1695 (lane cloud): IS THE 4b CAGR FLOOR THE ONLY LEG THAT EVER BINDS ON A FULL GROSS LADDER? **ANSWERED — KILL OF THE 'SINGLE-LEG' PREMISE, AND SOMETHING STRONGER IN ITS PLACE: 4b IS NOT A FOUR-LEG TEST AT ALL. DELETING THE H1 AND H2 SHARPE LEGS MOVES 0 OF 900 CELL-WINDOW VERDICTS, AND 4b RESTATED AS {DD, CAGR} ALONE REPRODUCES ALL 900 EXACTLY. NO RULES CHANGE; ONE PARK MEMO.**

  **THE DEFECT THIS CLOSES.** Idea 1454 found the live book fails 4b on the CAGR floor alone; the
  2026-09-19 CHANGELOG found all 11 of 180 FULL-and-OOS passes sitting at G = 1.00; idea 1699
  (pushed this morning) found an always-invested ladder squeezed between a CAGR floor at G <= 0.50
  and a DD cap at G >= 0.75 and said in terms that the leg census "belongs beside open idea 1695".
  Nobody had resolved all four legs at every rung of a FULL gross ladder.

  **CONSTRUCTION.** Two dials and no more: **G 0.05..1.00 step 0.05 (20 rungs)** x **FORM
  {NOGATE, BAND003 (live), BAND010 (the 2026-09-19 rule-8 pick)}**. Published, not tuned: PANEL
  {U56, B136, SMALL} x WINDOW {FULL, H1, H2, IS, OOS}. 180 books, 900 cell-windows, every one in
  `grid.csv`. Weekly, t+1, 10 bps, no leverage (max realised gross 1.0000). Gates 19 of 19,
  including a bit-for-bit replay of `baseline.rules_v2_weights` through `engine.backtest`
  (max|d| 1.7e-17 over the scored window) and an EXACT cross-run reproduction of idea 1703's
  committed U56 (c=0.10, G=1.00) cell at 11.72% / 1.1726 / -16.30%.

  **(1) THE TWO SHARPE LEGS NEVER BIND.** 50 of 900 cell-windows clear 4b. 606 fail exactly one
  leg, and the binder is **CAGR 514 (84.8%), DD 92 (15.2%), H1 0, H2 0**. The leg-deletion
  counterfactual is the same fact stated as a test-design claim: deleting H1 moves **0** of 900
  verdicts, deleting H2 moves **0**, deleting DD moves 92, deleting CAGR moves 514. Keeping only
  {DD, CAGR} reproduces **all 900** verdicts with zero disagreement. On this grid the H1 and H2
  legs of PROTOCOL 4b are decorative.

  **(2) AND THE REASON IS ARITHMETIC, NOT EMPIRICAL.** Over a 20x range of target gross the window
  Sharpe moves by at most **0.0169** (mean 0.0031) while MaxDD moves **41.7 pp** and CAGR **19.2
  pp**. Scaling a book cannot move its Sharpe, so a Sharpe leg cannot adjudicate gross: at every
  one of 45 (panel, form, window) triples the H1 and H2 pass-sets are ALL-or-NOTHING. The CAGR leg
  passes on an UPPER set of G at 31 of 31 non-trivial cases and never a lower one; the DD leg on a
  LOWER set at 17 of 17 and never an upper one; 0 of 180 pass-sets are non-contiguous.
  **Operationally, 4b = (a G-invariant Sharpe screen) x (G in [g_CAGR, g_DD]).** Mean feasible
  width **1.11 of 20 rungs**; **22 of 45** triples are EMPTY.

  **(3) 'EVERY PASS AT G = 1.00' IS A BAND-BOOK ARTEFACT.** The FORM decides which end of the
  interval binds. NOGATE feasible windows sit at G 0.55-0.75; BAND forms at G 0.85-1.00 — because
  the band's realised gross is 0.53 of a 0.75 target, so a band book must ask for more gross to
  clear the same CAGR floor, and its de-gross keeps the DD leg passing at every rung (DD is 'ALL'
  at every BAND cell on U56 and B136). The record's edge-of-grid gross claim is a statement about
  the band's de-gross, not about the gross ladder.

  **(4) IDEA 1699'S 'NO RUNG IN BETWEEN' WAS A GRID-RESOLUTION ARTEFACT.** At 0.05 resolution the
  always-invested U56 ladder does have a rung in between: **G = 0.65 clears 4b in ALL FIVE
  windows** — no moving average, no band, no ranking, FULL 11.42% / 1.1188 / -19.75%, OOS
  11.83% / 1.1269 / -19.75%, turnover 0.73x/yr. G=0.60 fails the CAGR floor and G=0.70 fails the
  DD cap, so the window is **one rung wide**, it is **U56-only** (B136 and SMALL no-gate windows
  are empty), and U56 is the panel idea 1703 showed is carried by its 20 survivorship-selected
  mega-caps. **PARK, not KEEP** — memo at `research/backtests/2026-09-20_nogate-G065-U56_PARK_MEMO.md`
  with the exact RULES wording it would take. The squeeze is real; its emptiness was not.

  **(5) RULE 8 (picks fit on warm-up..2016-12-31, 2017-2026 read EXACTLY ONCE).** Four choosers x
  three panels: **3 of 12 picks clear 4b OOS, 0 of 12 clear 4a**, mean OOS Sharpe 0.9465; 5 of 12
  land on G = 1.00 and 5 of 12 on NOGATE. On U56, C_MEMO reaches the G=0.65 no-gate cell from the
  IS window alone and it holds OOS. SMALL fails every leg at every chooser.

  **WHAT THE RECORD SHOULD DO.** Stop quoting 4b as four facts. It is a Sharpe screen that does not
  depend on gross, times an interval on gross whose endpoints are the CAGR floor below and the DD
  cap above — and on this grid the Sharpe screen has never once been the binding constraint. A
  Sunday review may wish to restate PROTOCOL rule 4b in those terms (this run did NOT modify
  PROTOCOL.md, RULES.md, scan.py, bot.py or baseline.py). Two consequences for reading the record:
  any "4b pass" is, to the resolution of this grid, a claim about realised exposure; and any 4b
  verdict quoted without its feasible-width is quoting a number that is empty at 22 of 45 triples
  and one rung wide at the median of the rest.

## 2026-09-20 — idea 1699 (lane C): DOES THE BAND BOOK NEED THE BAND AT ALL ONCE GROSS IS FREE? **ANSWERED — THE BAND IS FREE ON RETURN (28 OF 60 MATCHED PAIRS, MEAN dSHARPE -0.0009, 0 OF 12 BOOTSTRAP CONTRASTS AT |t| > 2), LOAD-BEARING ON THE 4b VERDICT (AN ALWAYS-INVESTED LADDER PASSES AT 0 OF 12 RUNGS), AND ITS ONE REAL EDGE — DEPTH — IS TWO-THIRDS DE-GROSS WITH THE RESIDUAL INSIDE ITS OWN NOISE. KILL OF THE PREMISE; NO NEW BOOK, NO RULES CHANGE.**

  **THE DEFECT THIS CLOSES.** The 2026-09-19 rule-8 pick wanders across c = 0.00-0.10 from
  chooser to chooser while G pins to 1.00 at every passing cell, and idea 1703 re-read the same
  thing today (all 5 U56 4b passes at G = 1.00). That pattern says the band rung is free and the
  gross rung is everything. Every prior run priced the no-gate twin as an OUTSIDE control beside
  the grid; none had put it INSIDE, as a cell a chooser can legally pick and a 4b verdict can
  legally land on.

  **CONSTRUCTION.** Two dials and no more: **c {NOGATE, 0.00, 0.03, 0.05, 0.10, 0.15}** x
  **G {0.25, 0.50, 0.75, 1.00}**, where NOGATE removes the 200d band entirely (always invested,
  equal weight over the priced names at the same target gross). Published, not tuned: PANEL
  {U56, B136, SMALL} x WINDOW {FULL, H1, H2, IS, OOS}. 72 books, every cell in `grid.csv`.
  Weekly, t+1, 10 bps. TWO matchings, both reported: **TARGET** gross (the idea's wording — the
  investor who has fixed G and asks whether to run the gate) and **REALISED** gross (this
  record's nine-run convention — the twin's target G' solved by bisection so its realised mean
  gross equals the band cell's, converged to 9.6e-06). Gates 11 of 11, including a bit-for-bit
  replay of `baseline.rules_v2_weights` through `engine.backtest` (max|d| 1.7e-17) and a
  CROSS-RUN reproduction of idea 1703's committed U56 (c=0.10, G=1.00) cell at max|d| 4.7e-05.

  **(1) ON RETURN THE BAND IS FREE, AND THE MATCHING DOES NOT MATTER.** Over 60 matched pairs the
  band beats its own no-gate twin on FULL Sharpe at **28 of 60** (mean **-0.0009**, median
  -0.0018), OOS Sharpe 32 of 60 (+0.0180), and on FULL CAGR at **0 of 60** (mean -4.46%/yr).
  Matching on REALISED gross instead reproduces it to four decimals (28 of 60, mean -0.0009).
  Per panel the sign is not even stable: U56 +0.0419, B136 **-0.0264**, SMALL -0.0182. The
  paired circular block bootstrap (21-day blocks, 2,000 draws, seed 20260920) of dSharpe at the
  two headline cells on three panels under both matchings reaches |t| > 2 at **0 of 12** — max
  |t| **0.68**, min p **0.497**. The live cell's own +0.0821 carries SE 0.1209.

  **(2) DEPTH IS THE ONE LEG IT WINS, AND TWO-THIRDS OF IT IS DE-GROSS.** Target-matched, the
  band is shallower at **60 of 60** pairs, mean **+11.80 pp**, and there the bootstrap is
  emphatic: 6 of 6 headline cells at |t| >= 2.69 (p <= 0.011). Match the twin's REALISED exposure
  and the edge falls to **+4.11 pp** (U56 +3.03, B136 +4.14, SMALL +5.15) and **0 of 6 clear
  |t| > 2** — max +1.92 (B136 live, p 0.049), U56 live +4.34 pp at t +1.52, p 0.112. That is the
  same order as idea 1511's committed paired dMaxDD SE of 2.93 pp. So the band's measurable
  contribution is that it holds less; the part that is timing is unresolvable at this sample.

  **(3) AND YET REMOVING IT DELETES EVERY PASS — BECAUSE 4b CANNOT BE CLEARED BY A CONSTANT-GROSS
  BOOK.** No-gate cells clear 4b FULL-and-OOS at **0 of 12**; band cells at 7 of 60. The leg
  census says exactly why: the always-invested ladder is **squeezed** — on U56 and B136 it fails
  the CAGR floor at G <= 0.50 (U56 G=0.50: 8.76% against 10.59%) and the DD cap at G >= 0.75
  (U56 G=0.75: -22.53% against -20.23%), **with no rung in between**, while its Sharpe is flat
  across the whole gross ladder (1.1174-1.1195 on U56) because scaling a constant book cannot
  move Sharpe. SMALL additionally fails H2 at 4 of 4. The band escapes the squeeze arithmetically,
  not cleverly: it holds ~0.69 realised gross and draws down like a ~0.50 book. **The operational
  reading is that 4b, as written, is passable only by a book whose REALISED GROSS MOVES** — which
  is a statement about the test, not about trend following, and it belongs beside open idea 1695.

  **(4) RULE 8 (picks fit on warm-up..2016-12-31, 2017-2026 read EXACTLY ONCE).** Four choosers
  (C_SHARPE / C_MEMO / C_CAGR / C_ANCHOR) x three ARENAS: FULL 24-cell grid, BAND-only 20 cells,
  NOGATE-only 4. Mean OOS Sharpe: **BAND 0.9613 > FULL 0.9499 > NOGATE 0.9372**. So handing the
  chooser the no-gate rung does not help — it **hurts**: on U56, C_MEMO and C_CAGR both defect to
  NOGATE G=0.75 and give up the 4b pass (OOS 1.1268 / -22.53% against the band pick's 1.1940 /
  -16.30%). The FULL arena lands on NOGATE at 3 of 12 picks and on G = 1.00 at 6 of 12 — the
  edge-of-grid gross claim again. **4a is 0 of 72 across the whole run.**

  **WHAT THE RECORD SHOULD DO.** Stop quoting c as if it earned Sharpe: it does not, on any panel,
  under either matching, at any resolvable significance. Quote it as what the numbers support — a
  STATE-DEPENDENT DE-GROSS whose entire measurable value is that realised exposure falls in bad
  tape, ~0.69 of target on U56. And read every 4b pass in this repository knowing that the test
  cannot be cleared by any constant-gross book at any rung: the pass is a statement about moving
  gross first and about names second. **No RULES change proposed** (4a 0 of 72; the 4b passers are
  the already-committed band family that idea 1703 showed this morning to be survivorship-
  conditional). Caveats: current-constituent survivorship on all three panels (rule 9), so every
  absolute level is an UPPER BOUND — this run reads CONTRASTS on a common tape, which is what
  survives that; SMALL is 667 columns after the idea-1074 max_1d_move >= 1.0 drop; the SPY column
  enters each panel's book as one name exactly as `baseline.rules_v2_weights` does.

## 2026-09-19 — idea 772 (lane cloud): IS THE SMALL 4a BAR CARRIED ENTIRELY BY ITS OOS SECOND HALF? **ANSWERED — THE COLLAPSE IS REAL IN MAGNITUDE (OOS HALVES 0.9496 / 0.1292) AND UNRESOLVABLE IN NOISE (SE 0.6375, t +1.29, p 0.195). THE BAR'S OWN CALENDAR-YEAR SPREAD IS 4.73 OF SHARPE. AND THERE IS NOTHING LEFT TO RE-SCORE: 0 OF 17 PRE-REGISTERED DEVICES CLEAR 4a ON SMALL UNDER THE COMMITTED READING, FULL OR OOS. THE LENIENT 'MIN' BAR IS VACUOUS — THE BAR PASSES ITS OWN TEST. KILL (no book); A PROTOCOL NOTE IS PROPOSED.**

  **THE DEFECT THIS CLOSES.** Idea 767 read the live book on the small panel at OOS Sharpe
  0.5665 with OOS halves 0.9166 / 0.1704. Path 4a asks a device to beat THAT book in both
  halves, so a comparand that collapses inside one sub-window would make every SMALL 4a
  verdict a verdict about a degenerate object. No run had asked whether the collapse is
  resolvable, or what survives a split-aware bar.

  **CONSTRUCTION.** Two dials: **SPLIT {H2, T3, Y}** x **BAR {POOLED, MIN, ALL}** — POOLED is
  the committed practice (both halves of the window), MIN the lenient reading (device pooled
  Sharpe > the bar's WORST block), ALL the strict one (device beats the bar in EVERY block);
  the MaxDD leg is unchanged in all three. Published, not tuned: **PANEL {SMALL, U56, B136} x
  WINDOW {FULL, IS, OOS} x 17 PRE-REGISTERED DEVICES** rebuilt from `baseline.py` and tuned by
  no one here (BAND {0.00, 0.03, 0.08} x G {0.75, 1.00}; MAXVOL {0.60, 0.80} x G; TOP-N {10,
  20, 40} x G, the 2026-09-04 KEEP-4b construction; RULES v1). Weekly, t+1, 10 bps. Gate: the
  local replay equals `engine.backtest` at **max|d| 1.0e-17 (SMALL), 6.9e-18 (U56, B136)**.
  Bar reproduction: **OOS 0.5458, halves 0.9496 / 0.1292** against 767's committed
  0.5665 / 0.9166 / 0.1704 — same sign and shape, the gap being the pool rebuild (idea 1074:
  `SMALL439` now denotes a 665-name pool after dropping the 54 names with max_1d_move >= 1.0).

  **(1) THE COLLAPSE IS INSIDE ITS OWN NOISE.** Circular block bootstrap of the bar's OOS
  half-Sharpe difference (21-day blocks, 2,000 draws, seed 20260919): observed **+0.8204**,
  **SE 0.6375, t +1.29, 95% CI [-1.2954, +1.2312], p 0.195**. The same statistic reads
  **+0.3266 (p 0.604) on U56** and **+0.4127 (p 0.517) on B136**. A half-Sharpe gap of 0.8 is
  what a stationary stream of this length produces routinely; "carried entirely by its second
  half" is not a property the record can measure at this sample size.

  **(2) BUT THE BAR IS NOT A STABLE COMPARAND ON ANY PANEL.** Bar Sharpe by calendar-year block:
  **SMALL spread 4.7273 (-1.5374 to +3.1899), U56 3.8453, B136 4.7940**; by thirds of OOS,
  SMALL **-0.3181 / 1.1384 / 0.5281 (spread 1.4565)**. The object a 4a verdict is measured
  against moves year to year by more than any device margin the record has ever published.

  **(3) THERE IS NOTHING LEFT TO RE-SCORE ON SMALL.** Under the COMMITTED (POOLED) reading the
  device corpus clears 4a at **0 of 17 FULL, 1 of 17 IS, 0 of 17 OOS** on SMALL, and **0 of 17
  at every window on U56 and B136**. Under the strict block-dominance readings (ALL x H2/T3/Y)
  it is **0 of 17 everywhere** except the same lone SMALL IS cell. The SMALL 4a line is empty on
  the rebuilt pool whichever bar is used, so no committed SMALL 4a pass survives — and none
  fails — for want of any pass at all. 4b OOS for reference: **SMALL 0 of 17, U56 8, B136 3**.

  **(4) THE LENIENT BAR IS VACUOUS.** Under BAR = MIN the passers are 1-2 of 17 at every
  panel-window and they include **the bar itself** (`BAND0.03_G0.75` on SMALL and B136,
  BAND0.00/0.03 on U56): a comparand that clears its own test cannot adjudicate anything.
  MIN should never be written into a bar rule.

  **(5) RULE 8.** Devices chosen on IS only, 2017-2026 read once. SMALL: both legal choosers
  pick **RULES v1** — OOS **7.82% / 0.7073 / -31.50%** against the bar's 3.64% / 0.5458 /
  -14.16% and SPY's 15.26% / 0.8737 / -33.72%. It beats the bar's POOLED OOS Sharpe and still
  **fails 4a in both halves and in every block, and fails 4b on the drawdown cap (-31.50% vs
  the -20.23% allowance)**. U56 picks BAND0.08_G1.00 / BAND0.03_G1.00 and B136 BAND0.08_G1.00
  (4b True, **4a False**). The third chooser, "best IS device that clears 4a under ALL/Y", has
  **no legal pick on any panel**.

  **WHAT THE RECORD SHOULD DO.** Quote the bar's BLOCK PROFILE (year spread 3.85-4.79 of
  Sharpe) beside every 4a verdict, never a MIN-style bar, and treat a sub-window Sharpe gap
  below ~1.3 (the 95% band of this bootstrap) as unreadable. **No RULES change proposed.**
  Caveats: current-constituent survivorship on all three panels; SMALL is 665 names after the
  max_1d_move >= 1.0 drop; the SPY column enters the panel books as one name exactly as
  `baseline.rules_v2_weights` does.

## 2026-09-19 — idea 1686 (lane cloud): DOES THE KEEP-4b BOOK SURVIVE A PER-NAME AND PER-GROUP CONCENTRATION CAP AT MATCHED REALISED GROSS? **ANSWERED — THE COMMITTED BOOK IS ALREADY CAP-COMPLIANT (A PER-NAME CAP BINDS AT 0 OF 72 CELLS), A 45% GROUP CAP IS FREE, A 30% GROUP CAP COSTS 0.009 OF SHARPE AND A 20% GROUP CAP COSTS THE 4b PASS. WHERE CAPS DO BIND THEY BUY NOTHING AT MATCHED GROSS (39 OF 77 ON SHARPE) AND THEIR ONLY POSITIVE DIRECTION IS THE DE-GROSS RECIPE THE RECORD ALREADY SHIPS. KILL AS A DEVICE; NO RULES CHANGE.**

  **THE DEFECT THIS CLOSES.** Real capital is held under a mandate: x% per name, y% per group.
  No run had ever asked whether the standing 4b band book can be held under one, and the
  record's nine-run lesson (every device is beaten at matched exposure by a plain de-gross)
  says a cap must be priced against a REALISED-GROSS-MATCHED twin, not against the uncapped book.

  **CONSTRUCTION.** Two dials: **c_N {0.02, 0.04, 0.06, 0.10, 0.20, inf} x c_G {0.20, 0.30,
  0.45, inf}** (fractions of NAV; groups are `research/universe.json`'s four, so c_G is a U56
  object — B136 and SMALL carry no committed groups). Published, not tuned: **BOOK {DEGROSS =
  the committed recipe gross/N_priced with gated-out weight to CASH, INBAND = gross/N_inband,
  the full-exposure book a cap is actually for} x PANEL {U56, B136, SMALL} x GROSS {0.75, 1.00}**.
  Spill convention fixed and stated: capped weight re-spreads to names with BOTH name and group
  headroom, the remainder to cash. **144 cells, every one published** (`.grid.csv`), each against
  its OWN twin: the same uncapped book scaled to the capped book's realised mean gross. Weekly,
  t+1, 10 bps. Gates: the local replay equals `engine.backtest` at **max|d| 6.9e-18** (U56, B136)
  and **1.0e-17** (SMALL); and **INBAND capped at c_N = gross/N reproduces
  `baseline.rules_v2_weights` at max|dw| 0.000e+00** on every fully-priced rebalance day of all
  three panels — the tight limit of the cap ladder IS the shipped book.

  **(1) A PER-NAME CAP CANNOT BIND ON THE COMMITTED BOOK — 0 OF 72 CELLS.** The recipe divides
  by names PRICED, not names in band, so the largest position it can ever hold is gross/N:
  **1.79% of NAV on U56 at G = 1.00, 0.74% on B136, 0.15% on SMALL.** Any mandate stating a
  per-name limit of 2% or looser is satisfied by construction, at zero cost, at every rung.

  **(2) THE GROUP CAP IS THE ONLY BINDING ONE, AND IT HAS A PRICE.** U56, G = 1.00 (the standing
  4b cell): **c_G = 0.45 binds on 0% of rebalance days** (the largest group, MEGACAP 20 of 56,
  reaches 35.7%) and is free — 11.53% / 1.2008 / -15.91% unchanged. **c_G = 0.30 binds on 33.2%**
  of days and costs **-0.0091 Sharpe FULL and -0.0103 OOS** against its matched-gross twin
  (11.37% / 1.1918 / -15.85%; OOS 12.46% / 1.2656 / -15.85%) — **4b survives**. **c_G = 0.20
  binds on 78.3% and breaks the 4b pass on the CAGR floor**: FULL 9.82% against a 10.58% floor,
  OOS 10.65% against 10.68% — three basis points — for **-0.0588 / -0.0706** of Sharpe.

  **(3) AT MATCHED REALISED GROSS THE CAP IS A COIN FLIP ON SHARPE AND SUB-SE ON DRAWDOWN.**
  Over the 77 cells whose cap actually binds: **39 of 77 beat their own twin on FULL Sharpe**
  (mean **-0.0023**, median +0.0002) and **33 of 77 on OOS Sharpe** (mean **-0.0040**). The one
  systematic effect is depth — **61 of 77 shallower, mean +0.88 pp** — which is **0.30 of the
  record's own 2.93 pp paired block-bootstrap DD SE** (idea 1511) and therefore unresolvable.
  **4a: 0 of 144.** 4b FULL 59, OOS 58, FULL-and-OOS 53 — every passer is a book the record
  already owns.

  **(4) THE CAP'S ONLY POSITIVE DIRECTION IS THE RECIPE ALREADY SHIPPED.** On the construction
  where caps bite (INBAND, U56, G = 0.75, c_G = inf) the twin gain is monotone in tightness and
  argmax sits at the grid EDGE: **+0.0734 (c_N 0.02) -> +0.0318 -> +0.0076 -> -0.0063 -> 0.0000**.
  Tightening further does not open a new book: by gate (2) the limit c_N -> gross/N IS
  `rules_v2_weights`. The gain is the exposure channel — constant per-name weight with a varying
  gross — not a concentration channel.

  **(5) RULE 8 — THE IS-FITTED CAP RUNS TO THE EDGE, AGAIN.** 28 picks (3 legal IS-only choosers
  x 12 (panel, book, gross) cells; 4 cells have no IS 4b pass), 2017-2026 read once. **24 of 28
  land on the tightest rung offered, 0 interior, 0 on the uncapped corner**; mean OOS dSharpe vs
  uncapped **+0.0103**; **9 of 28 clear 4b OOS, 0 of 28 clear 4a**. Same end-seeking already
  found on N (1639), gross (1590), cadence (1586) and phase (1694).

  **WHAT THE RECORD SHOULD DO.** Quote the mandate the book can be held under, not a cap study:
  **per name >= 2% of NAV is free, per group >= 45% is free, 30% costs ~0.01 of Sharpe and keeps
  4b, 20% costs the 4b pass.** Do NOT add a cap as a device. **No RULES change proposed.**
  Caveats: current-constituent survivorship on all three panels; SMALL is 665 names after
  dropping the 54 with `max_1d_move >= 1.0`; the SPY column enters the panel books as one name
  exactly as `baseline.rules_v2_weights` does.

## 2026-09-19 — idea 1690 (lane C): DOES THE 4b PASS SURVIVE DELETING ITS BEST CALENDAR YEAR OR ITS BEST k DAYS? **ANSWERED / KILL (capital) — THE PASS IS A ONE-DAY RESULT, AND THE DAY IS SPY's, NOT THE BOOK's. EVERY FLIP ON EVERY UNIT IS THE DD LEG. THE RETURN SIDE IS INDESTRUCTIBLE. NO NEW BOOK, NO RULES CHANGE.**

  **THE DEFECT THIS CLOSES.** Idea 1590 found the standing 2026-09-04 candidate cost-robust to
  120 bps yet dead to ONE day of execution LATENCY, so its 4b margins are thin in ways the cost
  axis cannot see. Idea 1511 measured its entire 4b drawdown margin at **1.10 pp against a paired
  bootstrap SE of 2.93 pp**. Nobody had asked how much TAPE it takes to spend that margin.

  **CONSTRUCTION.** The book is NOT rebuilt — positions are history. What is deleted is the
  SCORING WINDOW: a set of days is removed from the daily return stream of the BOOK, of SPY and of
  LIVE RULES v2 **identically**, so the 4b bar moves with the tape. Two dials: **UNIT {YEAR,
  DAY_BOOK, DAY_SPY, DAY_ADV} x k** (0..6 / 0..20 / 0..20 / 0..10). YEAR and DAY_ADV are
  ADVERSARIAL GREEDY on a scale-free objective (margin / |anchor margin|), so they answer the
  idea literally. Published, not dials: PANEL {U56, B136, SMALL665}, CONVENTION {SPLICE+DD_SEG,
  ZERO}, BAR {MOVES, FROZEN}, arena {FULL, IS, OOS}. **979 grid points, every one published.**
  Conventions: 1254's DD_SEG is right for a YEAR (one long cut) and WRONG for scattered days (the
  book's best days sit inside its deepest drawdowns, so a splice cuts the drawdown path exactly
  where it flatters), so DAY_* is headlined under ZERO — the day's return set to 0 in all three
  streams, calendar and drawdown path intact. Both are computed at every cell.

  **(1) THE SMALLEST DELETION THAT FLIPS THE VERDICT IS ONE TRADING DAY, AND IT IS NOT THE BOOK's.**
  Zeroing **2020-03-16** — SPY's worst session of the sample, **-10.94%**, on which the book lost
  only 6.66% — moves **SPY's MaxDD -33.72% -> -26.67%**, tightening the 60% cap from **-20.23% to
  -16.00%**, while **the book's own MaxDD moves -19.13% -> -19.10%**. DD margin **+0.0110 ->
  -0.0310**. One scale up, deleting the calendar year **2020** alone takes the cap to -14.70%;
  exhaustively, **17 of 18 single-year deletions KEEP the pass and only 2020 kills it**. This is
  idea 1254's OOS-arena finding (the drawdown side is carried by 2020, and not because 2020 was
  good for the book but because it was bad for SPY) confirmed on the FULL arena and localised to a
  **single session**.

  **(2) THE RETURN SIDE IS INDESTRUCTIBLE — AND THE BEST-DAY CUT MAKES IT BETTER.** Deleting the
  book's **20 best days** walks CAGR 15.80% -> **11.42%** and Sharpe 1.1537 -> **0.8994** and flips
  **no return leg**: H1 +0.2494 -> +0.2406, H2 +0.2952 -> **+0.3642**, OOS +0.3118 -> **+0.3792**,
  CAGR margin +0.0522 -> +0.0505. H2 and OOS WIDEN, because the same deletion costs SPY more than
  it costs the book. The cut cannot discriminate: **13 of the book's top-20 days are also SPY's
  top-20** (10 of 20 on the worst side) and both share one best session (2025-04-09, book +7.55% /
  SPY +10.50%). The ranked cuts flip only at **k = 9 (DAY_BOOK)** and **k = 7 (DAY_SPY)**, always
  on DD. **Of 979 grid points, every U56 4b failure names DD and 0 pass 4a.**

  **(3) THE FRAGILITY IS IN THE BAR, NOT THE BOOK — PUBLISHED IN BOTH DIRECTIONS.** With SPY's
  k=0 bar held FROZEN, DAY_SPY/SPLICE **never flips in 20** and DAY_BOOK/SPLICE flips only at 18
  (H2); but DAY_BOOK/ZERO flips at **3 instead of 9**, because a frozen cap no longer loosens as
  SPY's own drawdown deepens. Both directions say the same thing: **a 4b DD verdict is a statement
  about the benchmark's worst week as much as about the book.**

  **(4) THE OTHER TWO PANELS HAVE NO PASS TO LOSE.** B136 fails 4b at k=0 on DD alone (MaxDD
  **-20.74%** against a **-20.23%** cap, margin -0.0051) with every return leg positive;
  SMALL665 fails all five legs. Marked `NO_PASS_AT_K0`, never reported as fragility.

  **(5) RULE 8 — THE FRAGILITY MEASURE IS UNADJUDICABLE IN SAMPLE.** The book **fails 4b at k = 0
  in the 2009-2016 IS window on all three panels, on the DD leg** (U56 margin **-0.0072**, B136
  -0.0140), because that window holds no deep SPY drawdown (SPY IS MaxDD -22.06% -> cap -13.24%
  against a book at -13.95%) — the defect `2026-09-04_is-window-has-no-crash_C` already named. So
  every IS flip-depth is 0, the IS-only chooser is a **pure tie**, and the IS/OOS flip-depth rank
  correlation over the 12 (panel, unit) pairs is **undefined (nan)**. It degenerates to the
  do-nothing anchor U56, whose OOS flip depths are 1 / 1 / 6 / 5 against a 3-panel mean of
  0.33 / 0.33 / 2.00 / 1.67 and a worst panel (B136) of 0. OOS triples read once (2017-2026):
  BOOK **17.32% / 1.1857 / -19.13%**, LIVE v2 9.46% / 1.2769 / -12.05%, SPY 15.26% / 0.8738 /
  -33.72%.

  **GATES 4 of 5, AND THE FAILURE IS PUBLISHED RATHER THAN PATCHED.** G1b: on 1254's own tape
  (ending **2026-09-16**, 4,446 days) this book replays the committed U56 triple **0.1571 /
  1.1480 / -0.1913 exactly**. G4 is a cross-run gate reproducing 1254's **9-of-10** OOS-year
  count. G1, the same replay on THIS run's window, FAILS at 5e-3 (0.1580 / 1.1537 / -0.1913)
  for one reason: **the committed cache has grown by two trading sessions**, and SPY (0.8844 vs
  0.8815) and LIVE v2 (1.2011 vs 1.1982) drift the same +0.003 in the same direction. The
  tolerance was not loosened. **Any committed Sharpe quoted to 3 decimals is a statement about a
  tape vintage**, which is idea 1350's finding arriving by a second route.

  **WHAT THE RECORD SHOULD DO.** Quote a 4b DD verdict **with its deletion depth** — "DD passes,
  flip depth 1" is a different claim from "DD passes" — and quote the return legs separately from
  the DD leg, since on this book they are not remotely the same kind of evidence. Do NOT retune
  the 60% cap. **No RULES change proposed; the 2026-09-04 candidate is not promoted.**

## 2026-09-19 — idea 1694 (lane cloud): IS THE KEEP-4b PASS A REBALANCE-CALENDAR-PHASE ARTEFACT? **ANSWERED — THE PHASE IS THE LARGEST UNPRICED DIAL THE RECORD OWNS. THE STANDING U56 WEEKLY PASS SURVIVES ALL 5 WEEKDAYS; B136's SURVIVES ONLY 2 OF 5 AND NEITHER COMMITTED ANCHOR. 4a 0 OF 66. NO RULES CHANGE; A PROTOCOL NOTE IS PROPOSED.**

  **THE DEFECT THIS CLOSES.** Every book in this record rebalances on the LAST TRADING DAY of
  the period because that is what `engine.rebalance_mask` does. Nobody chose that anchor and no
  run had priced it. Idea 1590 found ONE day of execution LATENCY kills the standing 4b pass;
  this run holds latency fixed at t+1 and moves the day you LOOK.

  **CONSTRUCTION.** Two dials: CADENCE {W, M} x PHASE (W: weekday anchor MON..FRI, FRI being
  exactly `rebalance_mask(idx,'W')`; M: k-th trading day k in {1,5,10,15,20,L}, L being exactly
  `rebalance_mask(idx,'M')`). Not dials, published at every cell: PANEL {U56, B136, SMALL} and
  GROSS {0.75, 1.00} — both gross values PRE-REGISTERED from the committed record (0.75 live,
  1.00 the only gross at which the band book clears 4b FULL-and-OOS, ideas 1498/1649), neither
  chosen by this run. **66 cells, every one published.** Gates first: the FRI and L masks equal
  `engine.rebalance_mask` exactly, and the local backtester replays `engine.backtest` at W and M
  **bit-for-bit (max |d| 0.000e+00)**.

  **(1) THE PHASE MOVES THE BOOK BY MORE THAN ANY DEVICE THE RECORD HAS EVER CERTIFIED.** Within
  one (panel, gross, cadence) group — identical book, only the anchor moves — mean Sharpe spread
  **0.0737 (max 0.1639)**, mean MaxDD spread **4.33 pp (max 10.03 pp)**, mean OOS Sharpe spread
  **0.1005**. Weekly is the calm cadence (0.0416 Sharpe / 1.69 pp), monthly the violent one
  (0.1060 / 6.97 pp). The standing 4b candidate's Sharpe edge over its matched twin is **0.0089**
  (idea 1617) and its entire 4b drawdown margin is **1.10 pp** (idea 1511, paired SE 2.93 pp).
  **M/D15 is the worst phase at 6 of 6 monthly groups** — mid-month rebalancing of a 200d-band
  book is materially worse than month-end, which no run had said.

  **(2) THE 4b VERDICT IS PHASE-DEPENDENT AT 3 OF 12 GROUPS.** U56 G=1.00 weekly **5 of 5**
  (the reassuring half, checked for the first time); U56 G=1.00 monthly **5 of 6** (D15 fails);
  **B136 G=1.00 weekly 2 of 5 (TUE, WED) and monthly 2 of 6 (D1, D5) — and it fails at BOTH
  anchors the record actually quotes.** Any B136 4b claim that does not name its phase is
  unadjudicable. Corpus: **4a 0 of 66, 4b FULL 16, 4b FULL-and-OOS 14** — every passer is the
  already-committed G = 1.00 band book, not a new one.

  **(3) THE COMMITTED ANCHOR IS NOT A NEUTRAL DRAW.** Ranked by Sharpe inside its own phase set,
  the last-trading-day anchor has **mean rank 2.00 of a mean 5.5 phases against a uniform 3.25**,
  and rank 1 or 2 in **8 of 12 groups**. Every Sharpe the record has published is quoted at a
  mildly favourable point of a dial nobody declared. Small, but free to state.

  **(4) RULE 8 — THE IS-FITTED PHASE IS ACTIVELY HARMFUL.** 18 picks, three legal IS-only
  choosers, 2017-2026 read once. **0 of 18 land back on W/FRI**; mean OOS Sharpe of the picks
  **0.9188 vs the anchor's 0.9744 (-0.0555)**; **C_SHARPE picks M/D15 at all four U56 and B136
  cells**, the worst OOS phase (U56 G=1.00 **-0.1639**). 3 of 18 clear 4b OOS, 0 of 18 clear 4a.
  The same end-seeking failure already found on N (1639), gross (1590) and cadence (1586).

  **WHAT THE RECORD SHOULD DO.** Quote the PHASE beside every committed cadence or device
  verdict; use the cross-phase spread (0.0416 weekly, 0.1060 monthly) as the noise floor a
  cadence contrast must clear; do NOT re-tune the phase. **No RULES change proposed.**

## 2026-09-19 — idea 1664 (lane cloud): IS THE 27-of-27 MIXTURE CONVEXITY A DIVERSIFICATION FACT OR A SHARPE-ALGEBRA FACT? **ANSWERED — THE SIGN IS ALGEBRA (99.9% UNDER A NULL THAT CROSSES NOTHING), THE MAGNITUDE IS A rho FACT AND NOT A PANEL FACT. THE CONVEXITY COUNT SHOULD BE RETIRED. KILL STANDS FOR THE BLEND.**

  **THE DEFECT THIS CLOSES.** Idea 1649 reported blend Sharpe above the NAV-weighted average of
  its two corner Sharpes in **27 of 27 cells (mean +0.0535)** and read it as "real
  diversification". Sharpe is not linear in NAV weights, so some of that is arithmetic that holds
  for ANY two imperfectly correlated books — including two random halves of ONE panel.

  **CONSTRUCTION.** Two dials: **w {0.25, 0.50, 0.75} x G {0.50, 0.75, 1.00}**. Published, not
  dials: PAIR {U56xSMALL, U56xB136, B136xSMALL} x SLICE {FULL, IS, OOS} = **81 cross-panel
  cells**. Null: 40 random disjoint half-splits per panel, same book, same w, same G, seed
  20260919 = **3,240 null cells**. Book everywhere: live RULES v2 band 0.03, weekly, t+1, 10 bps.
  Gate: the (U56, G=0.75) corner replays `baseline.rules_v2_weights` bit-for-bit.

  **(0) THE ALGEBRA, ASSERTED NUMERICALLY.** C decomposes EXACTLY as `C = MIX + DIV`, where
  `MIX = (S_A - S_B) * w(1-w)(sd_A - sd_B) / (w*sd_A + (1-w)*sd_B)` is vol-mismatch re-weighting
  and `DIV = (w*mu_A + (1-w)*mu_B) * (1/sd_blend - 1/sd_lin)` is variance sub-additivity, **>= 0
  for ANY rho < 1 whenever the blend's mean is positive**. Identity holds to **5.1e-16** at all
  81 + 3,240 cells. Of 1649's number, replicated here at **+0.0536**, **93.1% is DIV** and only
  6.9% is MIX.

  **(1) THE SIGN CARRIES NO INFORMATION.** Random halves of ONE panel — same names, same gate,
  same regime, no panel crossed — give **C > 0 in 99.9% of 3,240 cells and 120 of 120 draw-means
  (100.0%)**. "k of k cells" is an algebraic near-certainty and must never again be published as
  evidence of diversification.

  **(2) THE MAGNITUDE SEPARATES — ON rho.** Shape-matched null (each draw's own mean over its 27
  cells): **0 of 120 draws reach +0.0536**; within-U56 reaches 65.6% of it, within-B136 24.0%,
  within-SMALL 12.4%. But **corr(C, 1 - rho) = +0.9528** over 1,107 even-split cells, and the
  ordering is decisive: **a random split of U56 (rho 0.865) yields C +0.0352 while the CROSS-PANEL
  U56xB136 pair (rho 0.964) yields only +0.0088**. Panel-crossing is not the operative property —
  U56 and B136 share 55 of 56 names (idea 536), so they are barely two books.

  **(3) THE CAPITAL ARM CONFIRMS 1649.** 15 cells published: **4a 0 of 15, 4b FULL 1, 4b OOS 2,
  4b FULL-and-OOS 1** — and that one is **w = 1.00**, the pure U56 corner at G = 1.00, i.e. no
  blend. **Of the 9 BLEND cells: 4a 0, 4b FULL 0, 4b OOS 1.** Rule 8, 2017-2026 read once: all
  three IS-only choosers leave the corner and every one is negative-value OOS (argmax IS Sharpe
  and IS Calmar **-0.1072**; **argmax IS CONVEXITY ITSELF is worst at -0.2752**). C is not a
  selection criterion.

  **WHAT THE RECORD SHOULD DO.** Retire the convexity COUNT; quote rho beside any convexity
  magnitude and price it against a within-panel split at the same rho. **No RULES change.**

## 2026-09-19 — idea 908 (lane B): WHY IS THE k/n 4b LEG-OVERLAP EMPTY ON EVERY SMALL BLOCK? **ANSWERED — THE QUESTION'S OWN PREMISE IS WRONG (THERE IS NO ONE LEG: THE LEG IS A PROPERTY OF THE CONSTRUCTION, NOT THE PANEL), THE GAP IS A PANEL FACT AND NOT A NAME-COUNT FACT, AND THE EMPTY OVERLAP ITSELF IS A GRID ARTEFACT OF 887's TWO CONSTRUCTIONS. KILL FOR CAPITAL (the one 4b cell dies at 25 bps and is reached by 0 of 108 legal IS-only picks). NO NEW BOOK, NO RULES CHANGE.**

  **THE DOUBT THIS CLOSES.** Idea 887 found the two LEVEL legs of path 4b — `L_CAGR` (CAGR >= 0.70
  x SPY) and `L_DD` (MaxDD >= 0.60 x SPY) — overlapping in 7 of 12 blocks but **0 of 4 on SMALL**,
  where 174 of 192 cells cleared NEITHER. It never said WHICH leg SMALL fails, nor whether the
  failure belongs to SMALL-CAP NAMES or merely to HOW MANY names a panel carries (U56 holds 55
  investable, SMALL 665). This run decomposes it leg by leg against SIZE-MATCHED RANDOM DRAWS
  from all three panels.

  **CONSTRUCTION.** 887's five families (MOM / MADIST / VOLLO / VOLHI / RAND) and its k/n dial
  (k_t = max(1, round(q x n_elig,t))), on random sub-panels of size m drawn from each panel's
  investable columns (SPY is the benchmark only, never held — 887 left it investable, and a
  size-matched draw must not sometimes contain the yardstick). **Tuned parameters: exactly 2
  (m, FAMILY), the queue's own.** Reported axes, every point published: panel x q {0.05 .. 1.00}
  x construction x cost rung {10, 25} bps x 8 seed draws. Weekly, t+1, gross 0.75 frozen at 887's
  headline. **29,880 cells, all committed.** One calendar for everything: the SMALL cache starts
  2010, so every book, every baseline and SPY are scored from **2011-01-13** (15.65 y) — without
  this a "SMALL misses the CAGR floor" reading could be nothing but U56 carrying 2008-09 and
  SMALL not. All three panels' SPY rows come out identical (n = 3,943; CAGR 14.01%, Sharpe
  0.8561, MaxDD -33.72%), so the cross-panel contrast is exact. 4a is judged against **RULES v2
  re-run on the same sub-panel** (a matched-universe baseline).

  **(1) THERE IS NO "THE LEG". THE FAILING LEG IS A PROPERTY OF THE CONSTRUCTION.** On SMALL,
  RESPREAD (always at full gross) clears `L_DD` in **0 of 1,230 cells** — every size, every seed,
  every family, every q — while clearing `L_CAGR` at 0.1537. DEGROSS (gross x k/n_e) inverts it
  exactly: `L_DD` 0.4423, `L_CAGR` **11 of 1,230**. The question asked which leg the small panel
  is failing; the honest answer is that it fails whichever leg its exposure is not paying for,
  and 887's two constructions sit at opposite ends of the exposure axis (realised mean gross
  median **0.2181 under DEGROSS against 0.7500 under RESPREAD**).

  **(2) THE GAP IS A PANEL FACT, NOT A NAME-COUNT FACT (pre-registered read, m = 55).** At the
  matched size the BOTH-rate is **SMALL 0.0000 against U56 0.1667 and B136 0.1313** — H_PANEL on
  both contrasts, the pre-registered bar being 0.10. Both legs are worse, not one: `L_CAGR` 0.0917
  vs 0.4167 / 0.3917, `L_DD` 0.2500 vs 0.6667 / 0.6542. The dilution-proof LEVEL statistic says the
  same thing and says it larger: **median Calmar at m = 55 is SMALL 0.1123 against U56 0.5251 and
  B136 0.4696, a factor 4.7.** Size is real but secondary and runs the same way on every panel
  (U56's BOTH-rate falls 0.1667 -> 0.0292 -> 0.0250 as m goes 55 -> 28 -> 14).

  **(3) A METHOD DEFECT, PUBLISHED BECAUSE IT WOULD HAVE FLIPPED THIS RUN'S OWN HEADLINE.** A
  pass RATE is a fraction over a construction set, so adding constructions that rarely pass
  anywhere shrinks every rate AND every difference between rates. Read over 887's two
  constructions, P2's m = 55 gap is **0.1667 / 0.1313 -> H_PANEL**; read over the six this run
  ends up with, the SAME cells give **0.1000 / 0.0708 -> H_SIZE**. Same data, opposite verdict,
  purely from the denominator. Both readings are published side by side and the pre-registered one
  decides. **Any "matched-control" verdict in this record that is a difference of pass rates is a
  function of its own construction set; the level statistic (here median Calmar) is not.**

  **(4) THE PRE-REGISTERED MECHANISM IS REFUTED, AND ITS NECESSITY HALF IS A TAUTOLOGY.** Clearing
  both level legs implies `Calmar >= (0.70 x SPY CAGR)/(0.60 x |SPY MaxDD|) = 1.1667 x SPY Calmar`
  **by algebra**, so its recall is 1.0000 by construction (FN 0 of 29,880) and publishing that as a
  finding would be publishing a tautology — this run says so before reading the number. The
  empirical half fails: precision is **0.1381** at 10 bps, and **SMALL's max Calmar is 0.6899,
  ABOVE the 0.4849 bar**, so the panel does reach over the ceiling and still never clears both
  legs. What the Calmar-clearing SMALL cells actually are: RESPREAD books at gross 0.75 with CAGR
  13-27% and MaxDD **-27% to -54%**, or DEGROSS books at a realised mean gross of **0.0375-0.15**
  with MaxDD -1.8% to -9.3% and CAGR 1.1-5.1%. Efficient at either end, never at a scale that
  clears the floor and a depth that clears the cap at once.

  **(5) AND THAT IS BECAUSE THE RUNG THAT WOULD IS NOT IN THE GRID (post-hoc arm, declared as
  post-hoc, not back-dated).** The k/n family offers only those two exposure regimes with nothing
  between, so the book that would clear both bars was never a cell 887 could have found. Adding it
  — the same selections held at a CONSTANT gross c {0.15, 0.25, 0.375, 0.50}, 887's own gross axis
  widened downward, every rung published — puts **4 of 7,380 SMALL cells over both level legs, all
  of them at c = 0.375 or c = 0.50**. The empty overlap is a **GRID ARTEFACT of 887's two
  constructions**, not a property of the small-cap panel.

  **(6) IT IS STILL A KILL FOR CAPITAL.** Exactly **1 of 7,380** SMALL cells clears the WHOLE of 4b
  at 10 bps — the full 665-name panel, MOM, c = 0.375, q = 0.05: 10.56% / 0.8930 / **-17.30%**,
  halves 1.0204 / 0.8529, OOS 11.73% / 0.8893 / -17.30%, against a SMALL RULES v2 baseline of
  4.26% / 0.6588 / -14.16% and SPY's 14.01% / 0.8561 / -33.72%. Every binding margin is inside the
  record's own measured noise: **CAGR +0.75 pp over the floor, H2 +0.0138, OOS Sharpe +0.0156**
  (idea 1639's paired bootstrap SE on Sharpe is 0.0666; idea 1511's on the DD leg is 2.93 pp). It
  **fails 4b outright at 25 bps** (CAGR 8.88% against the 9.81% floor) and it **fails 4a** on its
  own panel's baseline, on MaxDD. **RULE 8 closes it: 0 of 108 legal IS-only picks on SMALL clear
  4b, 0 of 108 beat SPY's OOS Sharpe (mean OOS Sharpe of the picks 0.4272 against SPY's 0.8737),
  and the 4b cell is reached by 0 of the 3 choosers that could name it.** No memo, no book, no
  RULES change.

  **BOTH KEEP PATHS OVER ALL 14,940 HEADLINE CELLS.** 4b: **216** (U56 68, B136 147, **SMALL 1**),
  falling to 57 at 25 bps. 4a: **129** (SMALL 89, B136 40, **U56 0**) — the one axis where the small
  panel leads, and 4a is blind to the CAGR it spends, which is the record's standing diagnosis
  restated on a third construction.

  **GATES 7/7 PASS.** G0/G1 this run's vectorised clone replays `engine.backtest` in returns and
  turnover to **3.82e-16 / 4.44e-16**; G2 it replays the LIVE RULES v2 book to **4.15e-16**; G3 at
  q = 1.00 RESPREAD is bit-identical to DEGROSS (k = n_elig, 0.0); G4 RESPREAD's realised gross is
  exact to 8.88e-16; G5 no leverage anywhere; G6 15.65 y (rule 1 min 10). Offline, deterministic,
  331 s. **SURVIVORSHIP (rule 9):** U56 / B136 are current-constituent lists and SMALL a current
  sub-$2B screen, so every LEVEL here is an upper bound — including SMALL's, which makes the
  panel's 4.7x Calmar deficit a floor on the true gap, not a ceiling.

  Script: `research/backtests/2026-09-19_why-is-the-k-over-n-4b-overlap-empty-on-every-SMALL-block_B.py`


## 2026-09-19 — idea 1639 (lane C): IS THE KEEP-4b TOP-20 BOOK'S N AN ARGMAX, A PLATEAU MEMBER, OR A POINT ON A MONOTONE RAY? **ANSWERED — (B) PLATEAU MEMBER, EVERYWHERE. N = 20 IS NOT AN INTERIOR ARGMAX ON ANY PANEL-GROSS CELL, 0 OF 36 NEIGHBOUR CONTRASTS REACH |t| > 2, AND 0 OF 12 LEGAL IS-ONLY CHOOSERS REACH IT. KILL AS A RE-TUNE AXIS; NO RULES CHANGE PROPOSED.**

  **THE DEFECT THIS CLOSES.** The standing 2026-09-04 KEEP-4b candidate (three-leg composite,
  N = 20, H = 126, MAXVOL 0.60, 200d gate, weekly, G = 0.75) has had its U56 cell replayed as a
  gate by dozens of runs, but no run had ever read N against its own neighbours at matched gross.
  A number nobody has laddered is an INHERITANCE, not a chosen parameter.

  **CONSTRUCTION.** Two dials and no more: N {10, 14, 20, 28, 40} x GROSS {0.50, 0.75, 1.00} on
  U56 / B136 / SMALL663 = **45 cells, every one published** at 10 bps, t+1, everything else frozen.
  A REFINED ladder N {8, 10, 12, 14, 17, 20, 24, 28, 34, 40} at G = 0.75 (30 further cells, all
  published) is a denser sampling of the SAME dial, not a third parameter — idea 1476 found coarse
  interior argmaxes relocate on refinement. The plateau SE is not asserted: it is a PAIRED
  circular-block bootstrap on the two books' own daily returns (block 65 rows, 1000 draws, seed
  20260919), so one resampled calendar prices both rungs.

  **(1) N = 20 IS A PLATEAU MEMBER AT 9 OF 9 PANEL-GROSS CELLS AND AN ARGMAX AT ONLY 3 (ALL U56).**
  U56 Sharpe N10/N14/N20/N28/N40 = 1.1081 / 1.1528 / **1.1537** / 1.0845 / 1.1349; B136 argmax is
  N = 28 (1.1077 vs 20's 1.0654); SMALL argmax is N = 14 (0.5739 vs 0.5092). **0 of 36 neighbour
  contrasts against N = 20 reach |t| > 2** — max |t| **1.28**, mean |dSharpe| 0.0306 against a mean
  paired SE of 0.0666. The ladder cannot tell 20 from the best rung on any panel, in either
  direction. **0 of 9 ladders are monotone in N**, so answer (C) is excluded outright.

  **(2) REFINEMENT RELOCATES THE ARGMAX ON 2 OF 3 PANELS — idea 1476 CONFIRMED.** U56 moves 20 ->
  **12** (1.1537 -> 1.1713, 17.68% / -20.17%, and it clears 4b FULL and OOS), B136 moves 28 -> 34,
  SMALL stays at 14. The fine ladder's Sharpe SPREAD (0.1154 U56 / 0.0989 B136 / 0.2129 SMALL) is
  wider than any neighbour gap the bootstrap can resolve, which is the whole finding: the dial has
  visible structure and none of it is significant.

  **(3) RULE 8 — REACHING FOR A DIFFERENT N ON IS ROWS IS NEGATIVE-VALUE OOS.** Four legal IS-only
  choosers (argmax IS Sharpe joint; argmax IS Sharpe over N at G = 0.75; argmax IS Calmar; argmax
  IS 4b-leg count) on 2009-2016 rows alone, 2017-2026 read ONCE. **0 of 12 (chooser, panel) picks
  reach N = 20.** Mean OOS Sharpe of the picks **0.8431 vs the N = 20 anchor's 0.8812 on the same
  panels (-0.0381)**; **1 of 12 picks clears 4b OOS, 0 of 12 clear 4a OOS**, while the anchor cell
  clears 4b FULL *and* OOS. The IS argmax runs to the ladder's ENDS (N = 40 on U56, N = 10 on B136,
  N = 28 on SMALL) — the same end-seeking failure the gross dial shows.

  **(4) BOTH KEEP PATHS OVER THE 45 COARSE CELLS: 4a 0, 4b FULL 8, 4b OOS 6, 4b FULL-AND-OOS 5.**
  The five: U56 N20 G0.75 (the anchor), U56 N14 G0.50, U56 N10 G0.50, B136 N20 G0.50, B136 N28
  G0.50. **SMALL passes 0 of 15.** Nothing here is a new book — every passer is the incumbent shape
  at a rung the bootstrap cannot distinguish from it.

  **WHAT THE RECORD SHOULD DO.** Stop quoting N = 20 as a chosen parameter; it is an UNRESOLVABLE
  dial at this sample length, and that is a defensible reason to leave it alone rather than a
  reason to move it. **No RULES change is proposed.** A re-tune to the ex-post argmax (N = 12 on
  U56) is exactly the reach rule 8 just priced at -0.0381 of OOS Sharpe.

  **GATES 8/8 PASS.** G0 16.7y min sample; **G1 the committed 2026-09-04 U56 anchor replayed to
  |dSharpe| 3.72e-05** (15.80% / 1.1537 / -19.13% full, 17.32% / 1.1857 OOS); G2 no leverage (max
  realised gross 1.000000, max drift above rung +0.0449); G3 exactly two dials; G4 every IS slice
  ends 2016-12-30; G5 60 of 60 cells published; G6 realised holding count non-decreasing in N
  (U56 10.0/13.9/19.8/27.6/38.5); G7 the three gross rungs are ONE exposure family (min corr of the
  G = 0.50 and G = 1.00 paths 0.9998 — which is why Sharpe barely moves with G and the 4b verdict
  moves only through the DD cap and the CAGR floor). Offline, deterministic, 12s.
  Survivorship (rule 9): U56 / B136 current-constituent, SMALL a current sub-$2B screen — every
  LEVEL is an upper bound; what survives is the SHAPE of Sharpe in N, since every rung inherits the
  identical bias.

  Script: `research/backtests/2026-09-19_top20-n-argmax-or-plateau_C.py`

## 2026-09-19 — idea 1666 (lane B): DOES THE BAND'S TIMING SURVIVE AN IN-BAND-SHARE-MATCHED PLACEBO GATE? **ANSWERED — THE *WHEN* IS A DRAWDOWN FACT AND ONLY A DRAWDOWN FACT. KILL FOR THE RETURN CLAIM (0 of 3 panels FULL, 1 of 3 OOS), CONFIRMED FOR THE DRAWDOWN CLAIM (3 of 3, against a null 1670's twin did not impose), AND A METHOD DEFECT THAT WOULD HAVE MANUFACTURED THE OPPOSITE ANSWER.**

  **THE DOUBT THIS CLOSES.** 1674 raced the live band against a static equity/SHY mix and 1670
  found the Sharpe half of that a U56 fact and the drawdown half 60 of 60. Both comparands are out
  of the market a DIFFERENT amount of the time than the band is, so neither can separate WHEN the
  band is out from HOW OFTEN — and the CHANGELOG's standing diagnosis is that every device family
  in the record is beaten at matched exposure by a plain constant de-gross, which is a HOW-OFTEN
  device. This run holds how often fixed to the day and destroys only the timing.

  **CONSTRUCTION.** CELL = live RULES v2 verbatim (200d +/-3% band with hysteresis, gross 0.75,
  weekly, gated weight to CASH), weights bit-identical to `baseline.rules_v2_weights` on U56
  (max |d| 0.000e+00). Three share-matched nulls, ordered by how much gate structure they keep:
  **ROT-COM** (primary) applies ONE common circular shift, each name permuted within its own
  priced rows, so per-name in-band share, run-length structure and cross-name synchrony survive
  exactly; **ROT-IND** shifts each name independently (synchrony destroyed); **IID** draws
  Bernoulli(p_i) per priced day, rejection-sampled to |share - p_i| <= tol (runs destroyed).
  Two tuned parameters and only two: seed count S {10, 25, 50} and tolerance tol {0.005, 0.02,
  0.05}; band pinned at the live 0.03 and gross at 0.75. **900 grid points, every one published**
  (3 panels x 5 null configurations x 3 S x 4 cost rungs x 5 windows), costs 0/10/25/50 bps off
  the exact two-rung reconstruction (gated at 0.000e+00 against the engine).

  **(1) THE DRAWDOWN CREDIT IS REAL AND IS NOT AN EXPOSURE ARTEFACT.** At 10 bps, S = 50, ROT-COM:
  cell MaxDD **-12.05% / -12.24% / -14.16%** (U56 / B136 / SMALL) against null means **-17.38% /
  -19.34% / -22.23%** — **+5.33 / +7.10 / +8.07 pp**, shallower than **49 / 49 / 48 of 50** draws
  (p 0.02 / 0.02 / 0.04) on FULL *and* OOS. ROT-IND and IID agree at p 0.00. This is the stronger
  form of 1670's 60-of-60: that twin was exposure-matched only in the mean of a fitted constant,
  this null is matched name-by-name and day-count-by-day-count.

  **(2) THE RETURN CREDIT IS NOT.** p(Sharpe) FULL **0.08 / 0.34 / 0.40**, OOS **0.04 / 0.22 /
  0.30**; dSharpe FULL **+0.1144 / -0.0254 / -0.0008**. On two of three panels a random gate of
  the same frequency earns MORE than the live band. The pre-registered bar (in the script header
  before any number was read) required FULL-Sharpe p <= 0.05 on >= 2 of 3, the same OOS, and
  MaxDD p <= 0.05 on >= 2 of 3: **0/3, 1/3, 3/3**. Two legs fail -> **KILL** for the timing claim
  on return.

  **(3) AND THE TRADE IS NOT CAPITAL-POSITIVE ON THE RECORD'S OWN BAR.** The cell fails path 4b
  **12 of 12** (3 panels x 4 rungs) — the DD cap is clear with room on every panel, the Sharpe legs
  pass on two, and the **CAGR floor (10.68% OOS) binds every time** (cell OOS CAGR 9.46% / 7.85% /
  3.63%). Meanwhile **10-14% of the ROT-COM draws on B136 and 6-8% on U56 CLEAR 4b** (S = 50; 10-20% on B136 across S), because
  scrambling the band's timing RAISES OOS CAGR (B136 9.96% null vs 7.85% cell) and the slack DD cap
  absorbs the deeper drawdowns. Path 4a against the panel's own RULES v2 baseline is a TIE by
  construction (the cell IS that baseline); the nulls clear 4a against the cell at 2-6% (ROT-COM)
  and at **0.00 at every IID cell**.

  **(4) THE NULL'S STRENGTH DECIDES THE ANSWER, AND THE WEAK NULL LIES IN THE BAND'S FAVOUR.**
  dSharpe FULL at 10 bps: ROT-COM +0.1144 / -0.0254 / -0.0008, ROT-IND +0.0671 / -0.0066 /
  **-0.0643** (SMALL beaten by 50 of 50, p 1.00), IID **+0.2338 / +0.1379 / +0.1389** with
  p = 0.00 at every FULL and OOS cell. An IID gate is out as often as the band but never in RUNS,
  so it pays the band's whole cost of being wrong without any of the persistence — a record that
  had priced the band against it alone would have published a decisive Sharpe win on the two
  panels where the honest null says the band LOSES. **Any future placebo gate in this record must
  match run-length structure, not just frequency.**

  **(5) RULE 8 (2017-2026 read ONCE).** The IS-only chooser is the (S, tol) cell maximising the
  NULL's mean IS Sharpe — the calibration most adverse to the cell — on rows <= 2016-12-31 only:
  it picks (50, 0.05) on B136, (10, 0.02) on SMALL, (10, 0.005) on U56. OOS at 10 bps, ROT-COM:
  U56 **1.2766** vs 1.0115 (p 0.00), B136 **1.1017** vs 1.0829 (p 0.22), SMALL **0.5447** vs 0.5202
  (p 0.30); OOS MaxDD -12.05 / -12.24 / -14.16% vs -18.25 / -19.34 / -21.47% (p 0.00 / 0.02 / 0.10).
  SPY OOS 15.26% / 0.8737 / -33.72%. The split is the same out of sample as in it.

  **(6) A METHOD DEFECT WORTH KEEPING, BECAUSE IT POINTED THE OTHER WAY.** The first draft failed
  its own exposure gate by **2.6 pp of mean gross** (null 0.5065 vs cell 0.5327 on U56): `band_state`
  is structurally OUT for a name's first 200 closes, those rows sit in the warm-up the cell is never
  scored over, and permuting across the whole history drags them INTO the scored window — docking
  the null ~5% of capital and handing the cell a Sharpe edge that read p = 0.00 everywhere.
  Restricting the share match and the permutation to priced rows INSIDE the scored window closes it
  to **0.00000 at 15 of 15 (panel x null) gates**; the residual constant rescale never exceeds
  1.0257 (max per-day gross 0.769, no leverage). **A share-matched permutation is not
  exposure-matched unless the warm-up is excluded**, and the un-excluded version produced exactly
  the answer the band's advocates would have wanted.

  **WHAT IS AND IS NOT PROPOSED.** Nothing is enacted; no KEEP candidate arises (4a is a tie, 4b
  fails 12 of 12) so no memo is filed. What the record gains is a sharper statement of the live
  clause 2: **it is a drawdown device, and its return content off U56 is indistinguishable from a
  coin-flip gate of the same frequency.** Survivorship (rule 9): U56 / B136 current-constituent
  lists, SMALL a current sub-$2B screen (665 kept of 719 priced; the mandated max_1d_move >= 1.0
  filter drops 54) carried back to 2010 — every absolute level is an UPPER BOUND; cell and null are
  the same names on the same days at the same mean gross, which the bias cannot manufacture. Script
  `research/backtests/2026-09-19_in-band-share-matched-placebo-gate_B.py`, full console
  `research/backtests/out/2026-09-19_in-band-share-matched-placebo-gate_B_log.txt`, grids
  `..._grid.csv` (900 rows), `..._cell.csv`, `..._keeppaths.csv`, `..._rule8.csv`, `..._gates.csv`.


## 2026-09-19 — idea 909 (lane B): IS THE 4b DD CAP A BETA CAP ON A PANEL THAT IS NOT U56? **ANSWERED — THE IDENTITY REPLICATES ON ALL THREE PANELS, ITS CONSTANT DOES NOT, AND THE EX-ANTE CAP IT LICENSES IS A KILL (4b 0 of 72, beaten by a plain de-gross on 56 of 72). NO NEW BOOK, NO RULES CHANGE.**

  **THE CLAIM UNDER TEST.** Idea 867 read agreement between PROTOCOL 4b's drawdown leg
  (MaxDD <= 60% of SPY's) and a single BETA THRESHOLD at **1.0000 on U56** (82 books, zero
  misclassifications, b\* = 0.596) but only **0.9146-0.9268 on SMALL**, and the record has since
  treated the DD leg as a beta leg. If that identity is real it is not a curiosity: it says the
  cap can be cleared EX ANTE by capping beta, which no committed book has tried.

  **(1) THE IDENTITY IS NOT A U56 ARTEFACT.** On a shelf this run BUILDS rather than recovers from
  prose — 14 frozen shapes (BAND x3, TOPN x4, MAXVOL x3, EQW, V1, VOLTGT x2) x 4 gross rungs =
  **56 books per panel, 168 in all, every one published** — the best single beta threshold
  reproduces the DD-cap label at **1.0000 / 1.0000 / 1.0000** on U56 / B136 / SMALL on the NARROW
  (BAND+TOPN, 28-book) shelf and **0.9821 / 0.9286 / 0.9464** on the WIDE (56-book) shelf, against
  majority-class base rates of **0.786 / 0.714 / 0.500** published beside every one. 867's SMALL
  number is reproduced in magnitude on an independent construction.

  **(2) BUT THE CONSTANT IS PANEL-SPECIFIC, AND THAT IS THE WHOLE VALUE OF THE IDENTITY.** b\* is
  **0.540 (U56) / 0.515 (B136) / 0.355 (SMALL)** and does not transfer: U56's b\* scores **0.7857**
  on SMALL, SMALL's scores **0.6964** on U56 and on B136. **867's OWN COMMITTED b\* = 0.596, applied
  verbatim, reads 0.9821 / 0.9286 / 0.7500** — on SMALL, 0.196 below SMALL's own refit and 0.250
  above a coin. The errors are a named family, not near-ties: U56 1 of 56 (VOLTGT @ gross 1.00,
  0.94 pp from the bar), B136 4 of 56 (V1 x2, MAXVOL, VOLTGT; 3.21 pp), **SMALL 3 of 56 at 7.46 pp**.
  Outcome (b) of the four pre-registered outcomes fires: real in FORM, useless as a CONSTANT.

  **(3) THE CAPITAL ARM — AN EX-ANTE BETA CAP — IS A KILL ON EVERY LEG THAT MATTERS.** The live
  RULES v2 band book (gross 0.75, weekly, 10 bps) de-grossed at each decision close by
  b / (weights x trailing-L-day name betas). Two dials and no more: **b {0.20..0.90} x L {63, 126,
  252}**, 24 cells x 3 panels, **all 72 published**. The cap buys drawdown (+6.26 / +6.83 / +3.50 pp
  at its best cell) by cutting mean gross from 0.533 to 0.23, and pays **-5.06 / -4.77 / -2.55 pp of
  CAGR** for it. **That purchase is worthless: the live book ALREADY clears the DD leg on all three
  panels** (-12.05% / -12.24% / -12.48% against a -20.23% bar). **4b passes 0 of 72 FULL and 0 of 72
  OOS, with the CAGR floor failing at 72 of 72.** Path 4a passes 13 of 72 (U56 7, B136 6, SMALL 0),
  every one with LOWER CAGR than the book it beats.

  **(4) RULE 8: NO IS-ONLY CHOOSER BEATS DOING NOTHING, ON 3 OF 3 PANELS.** Picks on
  warm-up..2016-12-31, 2017-2026 read once. C_SHARPE takes b=0.40/L=63 on U56 -> OOS **7.41% /
  1.275 / -10.23%** against the do-nothing anchor's **9.46% / 1.2769 / -12.05%**; B136 b=0.50/L=63 ->
  7.12% / 1.088 against **7.85% / 1.102**; SMALL b=0.50/L=252 -> 3.63% / 0.584 against **4.41% /
  0.647**. C_CAGR|DD selects an unbinding or near-unbinding cap on 3 of 3, i.e. it chooses the
  anchor. 0 of 6 chooser rows clears 4b OOS. SPY OOS on the same window: 15.26% / 0.8737 / -33.72%.

  **(5) AND THE DEVICE IS A WORSE DE-GROSS THAN A DE-GROSS.** Each cell raced against the same band
  book at a CONSTANT gross solved to reproduce that cell's own realised mean gross (31-rung ladder
  per panel, published; match error **1.08e-07**; no parameter added). **dSharpe > 0 in 16 of 72,
  mean -0.0209; OOS dSharpe > 0 in 5 of 72, mean -0.0308; MaxDD shallower than the twin in only 5 of
  72, mean -0.47 pp.** The cap's drawdown is typically DEEPER than a constant de-gross at the same
  exposure — the one thing a beta cap is supposed to be for. Its only win is **path 4a, 13 of 72
  against the twin's 0 of 72**, on a path blind to the CAGR it spends. This is the tenth consecutive
  2026-09-19 run in which a device is beaten at matched exposure by plain de-grossing.

  **GATES 11 of 11 PASS.** G0 samples 17.7y / 17.7y / 15.7y. G1 this script's simulator replays
  `baseline.compare`'s RULES v2 row to **2.220e-16** — published beside it, the ddof0-vs-ddof1 Sharpe
  convention gap on the same series is **1.350e-04**, larger than several credits the record calls
  findings. G2 the unbinding cap (b = 9.99) is **bit-identical** to the live book on 3 of 3 panels
  (0.000e+00). G3 max mean gross 0.5328, no leverage. G4 exactly two tuned parameters. G5 no chooser
  reads a row on or after 2017-01-01. Deterministic, offline, ~2 min.

  **CAVEATS (rule 9).** All three panels are current-constituent lists: every level is an upper
  bound. Arm 1's beta is a full-sample ex-post statistic — which is precisely why arm 2 exists, and
  arm 2 is the arm that fails. **NO RULES CHANGE, NO NEW BOOK, NOTHING ENACTED.**
## 2026-09-19 — idea 1602 (lane B): DOES THE SHY RESIDUAL CLAUSE SURVIVE A ZERO-DURATION CASH LEG? **ANSWERED — YES ON RISK, NO ON THE LICENSING. KEEP-4a CONFIRMATION FOR THE ACCRUAL RESTATEMENT (zero tuned parameters), KILL FOR THE ERA-HONEST FORM ON PATH 4a (0 of 492), AND A PROVED DEFECT IN PATH 4a AND RULE 8 THEMSELVES. NO NEW BOOK ENACTED, NO RULES CHANGE.**

  **THE DOUBT THIS CLOSES.** Ideas 1358 / 1498 / 1555 / 1547 credit the band's idle NAV with SHY
  and publish the result as a property of the RULE. SHY is not cash: it is a 1-3y Treasury ETF
  marked to market, own MaxDD **-5.71%**, **-3.88% in calendar 2022**, and idea 1555's own preamble
  flagged the gap in one line while idea 1547 found the 4a pass fails inside ERA_HIKE monotonically
  in F — i.e. exactly where duration was paid. The committed pass is a SUM of CARRY (idle NAV
  earning something instead of 0.00%/yr) and DURATION (a bond's own vol, drawdown and 2022 loss),
  never separated. A real book's idle NAV earns the first with none of the second.

  **CONSTRUCTION.** The sleeve asset is replaced by a SYNTHETIC ZERO-DURATION ACCRUAL: a daily
  return of exactly (1+a)^(1/252)-1, constant, never marked to market. Dials: **F {0.00, 0.25,
  0.50, 0.75, 1.00}** x **A {0, 1, 2, 3, 4, 5} %/yr**, and no more; gross FROZEN at G = 0.75 (the
  live value and the 2026-09-04 anchor value — 1498 already swept it). Reported, not tuned: SHAPE
  {FLAT, STEP}, where STEP pays 0 before **2022-03-16** (the FOMC's first hike of the 2022-23 cycle,
  a calendar fact fixed before any return was read, and idea 1547's own break) and a after;
  FRAME {LIVE, INC}; PANEL {U56, B136, SMALL}. Derived comparands with no free parameter: **SHY**
  (the committed sleeve), **MATCH1** (flat accrual at SHY's OWN realised CAGR), **MATCH2**
  (two-piece accrual at SHY's OWN era CAGRs). **450 cells, every one published**, plus a 492-cell
  break-even scan. **A pre-registered caveat: A IS NOT A DIAL A MANAGER OWNS** — a sweep rate is set
  by the money market — so the PRIMARY rule-8 chooser runs over F alone at each A and the joint
  (F, A) chooser is reported and labelled illegitimate.

  **(1) DURATION CONTRIBUTES NOTHING. THE CREDIT IS PURE CARRY.** SHY minus its carry-matched
  zero-duration twin at F = 1.00, over 6 panel-frames: **dCAGR -0.0024 pp, dSharpe +0.0009, dMaxDD
  +0.033 pp** (MATCH1); **dSharpe -0.0003** and **0 of 6 on the HIKE era** (MATCH2, mean -0.0316).
  The twins clear 4a on **3 of 6** panel-frames against SHY's **2 of 6** — SHY's duration COSTS the
  SMALL/LIVE pass outright, MaxDD **-13.78%** against the twin's **-11.46%**. Outcome (a) of the
  four pre-registered outcomes fires: the bond is along for the ride and clause 6 should be written
  as an accrual.

  **(2) THE RESTATED CLAUSE CLEARS 4a FULL *AND* OOS ON 3 OF 3 LIVE PANELS WITH ZERO TUNED
  PARAMETERS.** Break-even accrual a\*, solved on a 41-rung 0-10% ladder with every rung published:
  **U56 0.75%, B136 1.00%, SMALL 0.25%** (0.25% on all three if the sweep pays no transaction cost).
  At a flat 1.00%: U56/LIVE FULL **9.01% / 1.2522 / -12.04%** (H1/H2 1.282/1.229 against the live
  book's 1.228/1.181), OOS **9.85% / 1.3264 / -12.04%** against the live book's 9.46% / 1.2769.
  **F is NOT a free parameter**: OOS Sharpe is monotone non-decreasing in F on **78 of 78** (arm,
  panel, frame) cells, and a book has no reason to leave idle cash uncredited, so F = 1.00 is
  forced and the restated clause ships with **no tuned dial at all** — the rate is observed.
  **4b is UNMOVED at 5 of 30**: the CAGR floor still binds (9.01% against a 10.59% bar).

  **(3) BUT THE FLAT RATE IS A COUNTERFACTUAL, AND THE ERA-HONEST FORM IS KILLED: 0 OF 492.** A
  sweep paid ~0 through ZIRP; SHY's 0.9129%/yr there was ROLL and duration return, not a cash rate.
  Under the STEP shape, 4a passes **0 of 492** — 41 rungs to 10%/yr x 6 panel-frames x both cost
  conventions.

  **(4) AND THE REASON IS STRUCTURAL, PROVED RATHER THAN SCANNED (G10).** 4a's first leg is a
  STRICT inequality against the live book's FIRST-HALF Sharpe. This tape's halves split at ~2017,
  so the WHOLE first half sits in ZIRP; an honest sweep earns nothing there and the book is
  **BIT-IDENTICAL** to the live one — max |daily diff| **1.388e-17 / 2.082e-17 / 3.816e-17** on the
  three panels, H1 **1.2279 vs 1.2279**, **1.2298 vs 1.2298**, **0.8353 vs 0.8353**. *Equal is not
  greater.* **PATH 4a HAS NO WINDOW IN WHICH TO SEE A CASH-LEG RULE AT ALL**, and every 4a verdict
  the record has published about the cash leg — including idea 1498's headline pass — is a verdict
  about what the sleeve INSTRUMENT earned in 2009-2016, not about the rule.

  **(5) RULE 8 IS BLIND FOR THE SAME REASON.** The IS window (warm-up..2016-12-31) is entirely
  ZIRP, so the IS-Sharpe chooser over F picks **F = 0.00 on 18 of 18 era-honest cells**, at every
  rate to 5%/yr. Yet that same book at a 5% post-2022 sweep returns OOS **10.57% / 1.4167 /
  -12.07%** on U56/LIVE against the live book's **9.46% / 1.2769** — **+0.140 of Sharpe, +1.11 pp
  of CAGR** — and 1.2510 vs 1.1019 on B136, 0.8421 vs 0.6473 on SMALL. Over all legitimate choosers
  (78 picks): mean d_oSharpe **+0.0520**, beats the null 36/78, beats the live book OOS 25/78, picks
  F = 0.00 in 42/78. The illegitimate joint (F, A) chooser: mean **+0.0945** but beats the null only
  **9 of 24**. **Both licensing devices the record owns look only where the answer cannot appear.**

  **WHAT IS AND IS NOT PROPOSED.** The exact RULES wording for the accrual restatement, and the
  companion PROTOCOL clause this run earns ("a rule whose effect is confined to one monetary regime
  may not be adjudicated by path 4a's half-sample legs or by rule 8's 2009-2016 IS window"), are
  lines 8 and 9 of the memo. **Nothing is enacted**; PROTOCOL rule 6 gives the Sunday review that
  call. **GATES 10/10**, including G3's cross-script replay of ideas 1498/1555's committed U56 SHY
  cells to the decimal (LIVE 9.12% / 1.2675 / -11.48%, INC 16.16% / 1.1787 / -18.88%). Survivorship
  (rule 9): U56 / B136 current-constituent lists, SMALL a current sub-$2B screen (665 kept of 719
  priced; the mandated max_1d_move >= 1.0 filter drops 54) carried back to 2010 — every absolute
  level is an UPPER BOUND; the SHY-vs-twin contrast is same-names, same-days, same-frame and both
  arms carry the identical bias. Script
  `research/backtests/2026-09-19_zero-duration-cash-leg_B.py`, memo
  `research/backtests/2026-09-19_zero-duration-cash-leg_B.memo.md`.

## 2026-09-19 — idea 725 (lane cloud): DOES THE DAILY INVERSION OF IDEA 535's RETIREMENT GENERALISE? **ANSWERED: IT IS A CADENCE FACT, NOT A LOW-SIGNAL-REGIME FACT — AND THE IDEA'S OWN MECHANISM IS REFUTED IN ITS OWN DIRECTION. INCIDENTAL KEEP-CANDIDATE (4b) ON 2 OF 3 PANELS VIA THE DD-AWARE CHOOSER. NO RULES CHANGE (rule 6: Sunday review only).**

  **THE QUESTION.** Idea 535 retired idea 301's gate-FAMILY constant for the de-grossing timing
  residual in favour of a continuous predictor (CSD.is). Idea 539 found the retirement bar holds at
  every gross on {W,M,Q} and on {D,W,M,Q} but **INVERTS on the DAILY-only cells**, where CSD.is is
  23-27% WORSE than the label it retired — "the continuous predictor loses exactly where the residual
  is smallest". This run prices the retirement against the RESIDUAL'S OWN SCALE instead of cadence.
  **1,296 real books** (SMALL439 / U56 / B136 x {QUANTILE, MA-THRESH} x 9 levels x {D,W,M,Q} x gross
  {0.50,0.75,1.00} x {RESPREAD, DEGROSS}), **648 decomposition cells** on FULL/IS/OOS, both KEEP paths
  on every book, **gates 9/9**. The premise replicates: D-only OOS MAE ratio **1.3099 / 1.3187 / 1.3372**
  against 539's committed 1.2297 / 1.2492 / 1.2710.

  **(1) THE ANSWER.** Pre-registered **H_SCALE FALSE, H_CADENCE TRUE**. In the pooled bivariate fit of
  `d_err = |e_CSD| - |e_FAM|` on log IS residual scale and a D-cadence dummy (gross dummies included),
  the D dummy holds **+0.0231 (t +3.11)**; on the pool-stable panels alone (G8) **+0.0283 (t +2.92)**.
  Scale does not absorb it — corr(log IS scale, D dummy) is only **-0.1601**. Total explanatory power is
  small either way: pooled R² **0.0322** against a gross-dummy baseline of 0.0041.

  **(2) HOLD CADENCE FIXED AND THE IDEA'S CLAIM REVERSES.** Inside the **D-only** cells CSD.is is
  *better* than the family constant in the LOW-|resid| tercile (ratio **0.7569 / 0.6081 / 0.5412** at
  gross 0.50 / 0.75 / 1.00) and *worse* in MID (1.2835 / 1.2865 / 1.3884) and HIGH (1.0976 / 1.0956 /
  1.0888). Pooled, mean d_err across terciles runs -0.0020 / +0.0066 / -0.0218 (g 0.50), -0.0087 /
  +0.0082 / -0.0342 (0.75), -0.0163 / +0.0060 / -0.0454 (1.00) — **non-monotone**, negative at both ends
  and positive in the middle, so **no scale restatement of the retirement is available**. The confound
  was measured, not assumed: D cells are **37-40%** of the LOW tercile against 25% under a cadence-blind
  split, which is exactly why the marginal tables cannot settle it and the controlled fit can.

  **(3) THREE GATES FAILED AS FIRST DRAFTED, AND THE DIAGNOSIS IS A RECORD CORRECTION.** The first draft
  asserted a three-panel IS replay of 539, a reproduction of 535's published fit (-1.5722, t -6.32) and
  c_t gross-invariance to 1e-12. All three failed. **`SMALL439` IS NOT THE SAME PANEL: 439 names in 539,
  665 here** (ideas 706 / 1074), so one third of the cells are a different universe. On the
  **POOL-MATCHED** subset (U56 + B136) the replay is exact — 535's fit gives **-2.3811 (t -9.01)** here
  against **-2.3783 (t -9.02)** recomputed from 539's own committed decomposition, |d slope| **0.0028** —
  so the whole of the -1.5722 -> -1.6976 move in the all-panel level is the pool rebuild and none of it
  is method. And **539's own console already published "G4 FAIL — c_sd moves with gross"** (4.042e-3 /
  9.861e-3): asserting invariance inherited a claim the parent run had refuted, so the gate now
  REPRODUCES the documented failure (4.032e-3 / 9.112e-3). Per-panel drift is published with its cause:
  U56 IS 3.63e-3 pp (8 further trading days, inside the inherited allowance), B136 4.50e-2 pp
  (`prices_broad.csv` is re-cached weekly and restates adjusted closes), SMALL439 5.70e-1 pp (the pool).

  **(4) RULE 8 (2017-2026 read once).** Two IS-only choosers over each panel's 432 books.
  **ISSHARPE lands 0 of 3 panels on a KEEP path** — every pick fails the DD leg (B136 -37.77%,
  SMALL439 -39.18%, U56 -40.65%). **PREREG** (the 2026-09-03 memo's DD-aware IS rule) lands **2 of 3**:
  B136 `MA-THRESH / L=0.2 / M / g=0.50 / RESPREAD`, FULL 14.25%/1.1102/-18.98% (H1 1.305, H2 0.926), OOS
  **12.85%/1.0152/-18.98%**; U56 `QUANTILE / L=0.2 / Q / g=0.50 / RESPREAD`, FULL 12.01%/1.0683/-18.73%
  (H1 1.288, H2 0.921), OOS **11.73%/0.9627/-18.73%**. SPY OOS 15.26%/0.8737/-33.72% (DD cap -20.23%,
  CAGR floor 10.59%). **SMALL439's admitted set is EMPTY (0 of 432).**

  **(5) THE KEEP IS THIN AND THE RUN SAYS SO.** Both picks **fail 4a** (RULES v2 OOS 1.2766 on U56 and
  1.1017 on B136, at a third of the drawdown), both sit at the **lowest gross rung on the ladder**, and
  the corpus-wide rate is **4b 47 of 1,296 and 4a 16 of 1,296**. It is a replication, on an unrelated
  corpus, of the finding committed the same day under idea 1600.

  **(6) SURVIVORSHIP (rule 9).** All three panels are current-constituent lists with no delistings, so
  every CAGR level and every 4a/4b count is an upper bound. The headline `d_err` is an arm-minus-arm
  contrast on the same names and days (DEGROSS and RESPREAD share one gate mask), which the bias cannot
  manufacture; the KEEP columns inherit it whole.

  **GATES 9/9.** G0 >= 10y. G1 U56 IS replay of 539 (3.63e-3 pp). G2 pool-matched reproduction of 535's
  fit (|d slope| 0.0028). G3 exactly two tuned parameters (cadence set; residual-scale tercile) — panels,
  families, levels, gross, construction and lambda are inherited axes, every rung reported. G4 reproduces
  539's published G4 failure. G5 no scale bin, tercile edge, family mean or coefficient reads a row on or
  after 2017-01-01. G6 all 648 cells and 1,296 books published. G7 premise check (D-only ratio > 1 at all
  three grosses). G8 the headline survives dropping the changed panel. Script
  `research/backtests/2026-09-19_daily-inversion-of-the-retirement-as-a-residual-scale-fact_cloud.py`;
  memo `...cloud.memo.md`; grid / decomp / premise / bins / cadence_matched / fits / cells / walkforward
  / gates CSVs beside it.

## 2026-09-19 — idea 1592 (lane cloud): IS THE 4b DD CAP READABLE AT ALL AT ONE ARBITRARY LATENCY POINT? **ANSWERED: NO. 45% OF THE RECORD'S FULL-WINDOW 4b PASSES ARE POINT ARTEFACTS. KEEP-CANDIDATE (4b) ON ONE PANEL OF THREE. NO RULES CHANGE (rule 6: Sunday review only); a PROTOCOL 4b restatement is drafted for that review.**

  **THE QUESTION.** Idea 1590 found one trading day of execution timing moves MaxDD by 1.3-3.6 pp in
  EITHER direction and 1596 confirmed it at 144 books (sd 1.52 pp, range -3.28..+6.28 pp). That move is
  larger than the 1.10 pp DD margin every 4b verdict in this record is decided on — and EVERY published
  4b verdict is quoted at delay +0, one arbitrary point on the latency axis. This run re-reads the same
  bar on a LATENCY-AVERAGED statistic instead of a point. **96 real books** (U56 / B136 / SMALL x H
  {21,63,126,252} x cadence {W,M} x gross {0.50,0.60,0.75,1.00}) on the frozen incumbent frame, each at
  execution delay {+0,+1,+2} at 10 bps: **288 published cells, both KEEP paths under three readings
  (POINT / MEAN / WORST) at every one, gates 9/9.** G1 replays the committed 2026-09-04 U56 anchor to
  3.7e-5; G8 reproduces 1590/1596's -2.44 pp dMaxDD(+1) on it to **-2.4391 pp**.

  **(1) THE ANSWER, AND THE SIZE OF IT.** Of the 20 books clearing 4b on the FULL window at POINT,
  **only 11 survive the WORST-over-{0,1,2} reading**; OOS 17 -> 11; on FULL *and* OOS together
  **13 -> 7**. The MEAN reading is nearly harmless (80% of FULL and 88% of OOS POINT passes survive) —
  **it is the worst case that bites**, which is exactly why averaging is not a substitute for it.

  **(2) THE DD LEG IS THE LEG THAT BREAKS.** Among the 20 FULL POINT passers the DD leg flips
  POINT -> WORST in **6**, H2 Sharpe in 3, the CAGR floor in 3, H1 Sharpe in **0**. The mechanism is
  arithmetic, not a regime story: over D = {0,1,2} a book's MaxDD moves by mean **1.83 pp** (median 1.69,
  max 6.80) while the surviving DD-leg margin has median **1.29 pp** (min -1.94), and **64.6% of the 96
  books have a latency spread wider than the 1.10 pp margin the record decides DD verdicts on.**

  **(3) IT FLIPS A CAPITAL DECISION, NOT JUST CENSUS ROWS.** B136's PREREG pick (the 2026-09-03 memo's
  own DD-aware IS-only rule), M/H=21/g=0.50, reads 4b **TRUE** on FULL at POINT **and** at MEAN and
  **FALSE** at WORST: 11.00%/1.0910/-18.72% -> 10.44%/1.0432/-18.86% against the -20.23% cap.

  **(4) RULE 8 (2017-2026 read once).** Three IS-only choosers, admitted sets on warm-up..2016-12-31
  only. **LATWORST** — the memo's DD rule with the admission computed on the WORST-over-D IS statistics,
  i.e. the chooser held to the bar the idea proposes — picks U56 **W / H=126 / gross 0.60**, the
  incumbent's own cadence and brake de-grossed one rung, and it clears 4b FULL and OOS under **all three**
  readings: FULL 12.19%/1.1044/-17.54% (H1 1.1885, H2 1.0313), OOS **13.06%/1.1014/-17.54%** at WORST
  against SPY OOS 15.26%/0.8738/-33.72% (floor 10.68%, cap -20.23%) and live RULES v2 OOS
  9.46%/1.2769/-12.05%. Turnover 2.32x/yr.

  **(5) THE KEEP IS BOUNDED AND THE RUN SAYS SO.** It is **4b only and 4a fails everywhere** (the live
  book is higher-Sharpe and shallower on every panel), and it is **one panel of three**: 6 of 32 U56
  books survive WORST on both windows, **1 of 32 on B136, 0 of 32 on SMALL**, where the DD-aware admitted
  set is **EMPTY at both statistics**. Survivorship (rule 9): U56/B136 are current-constituent lists and
  SMALL a current sub-$2B screen carried back to 2010, so every pass count is an upper bound; the
  headline is a within-book contrast between three timings of the same names on the same days, which the
  bias cannot manufacture.

  **(6) THE PROPOSED PROTOCOL RESTATEMENT (Sunday review only; nothing changes today).** Add to rule 4b,
  verbatim: *"Every 4b leg is evaluated on the WORST value of its statistic over execution delays
  {+0, +1, +2} trading days beyond rule 2's decide-at-t / apply-at-t convention. A 4b pass quoted at a
  single delay is provisional and must be labelled POINT-READ."* It costs 45% of the record's FULL-window
  passes, and the books it removes are precisely those whose DD margin is inside their own latency spread.

  **GATES 9/9.** G0 >= 10y (16.7y min). G1 anchor replay 3.7e-5. G2 exactly two tuned parameters (the
  latency set; the statistic) — H / cadence / gross are a published ladder, every rung reported. G3 delay
  +0 is bit-for-bit PROTOCOL rule 2 against an independently rebuilt lag-1 frame (dev 0). G4 gross <= 1.0.
  G5 no chooser reads a row on or after 2017-01-01. G6 all 288 cells published. G7 reading nesting
  (WORST-pass => POINT-pass and MEAN-pass) 0 violations of 576. G8 cross-run replay of 1590/1596.
  Script `research/backtests/2026-09-19_is-the-4b-dd-cap-readable-at-one-latency-point_cloud.py`; memo
  `...cloud.memo.md`; grid / census / walk-forward / gates CSVs beside it.

## 2026-09-19 — idea 1596 (lane C): IS LATENCY FRAGILITY PREDICTABLE EX ANTE FROM TURNOVER OR HOLDING AGE? **ANSWERED: NO. PARK AS PRE-REGISTERED, KILL ON THE DEFLATED READING. THE SHORTCUT IS CLOSED; THE LATENCY AXIS MUST BE READ PER BOOK. NO RULES CHANGE (rule 6: Sunday review only).**

  **THE QUESTION.** Idea 1590 killed the standing 4b book because ONE trading day of execution delay
  moved MaxDD by 1.3-3.6 pp in EITHER direction — larger than the 1.10 pp DD margin every 4b verdict
  in this record is decided on — and idea 1600 then rescued a book at the (25 bps, +1 day) cell with a
  DD-aware IS-only chooser. Both readings LOOK at the latency axis. This run asks whether capital
  could have SKIPPED that look: if dSharpe(+1) and dMaxDD(+1) were a function of a book's OWN realised
  turnover path or its OWN realised mean holding age — both observable at delay +0, in-sample — a
  latency-robust book would be pickable ex ante. **144 real books** (3 panels x H {21,42,63,126,252,504}
  x cadence {W,M} x gross {0.50,0.60,0.75,1.00}), each at delay +0 and +1 at 10 bps: **288 published
  cells, both KEEP paths at every one, gates 48/48.** G1 replays the committed 2026-09-04 U56 anchor to
  2e-16 and reproduces 1590's -2.44 pp on that book exactly.

  **(1) THE ALARM IS CONFIRMED AT FOUR TIMES THE BOOK COUNT.** dSharpe(+1) sd 0.0419 (range
  -0.1276..+0.0912); dMaxDD(+1) sd **1.52 pp, range -3.28..+6.28 pp**, worse in 79 books and better in
  65. One day of timing **flips the 4b verdict in 7 of 144 books FULL and 11 of 144 OOS.**

  **(2) THE TWO REGRESSORS ARE ONE COLLINEAR AXIS.** corr(turnover/yr, mean holding age) = **-0.681**
  pooled (-0.766 per unit gross): a faster brake mechanically raises turnover AND lowers age. A
  coefficient **flips sign between its univariate and its bivariate fit in 7 of 48 (sample, Y,
  regressor) triples.** Both reach |t| > 2 on dMaxDD(+1) in the pre-registered reading (t[turn] -2.19,
  t[age] -2.69) — two collinear regressors splitting one axis, not two mechanisms.

  **(3) THE R² THAT CLEARS THE PRE-REGISTERED BAR IS MOSTLY PANEL DUMMIES.** Pooled R² = 0.431 on
  dMaxDD(+1), but **the dummies alone explain 0.297 on the same 36 rows, so the regressors buy
  dR² = 0.134**; on dSharpe(+1) they buy nothing (R² 0.093, no regressor at |t| > 2). The bar was
  written as a pooled R² BEFORE the run and is reported as written — hence the PARK — but the honest
  answer to "how much of the fragility either explains" is **13.4%**, and the run says so in its own
  verdict block rather than letting the PARK stand as a half-win.

  **(4) THE DECISIVE FACT, INDEPENDENT OF THE REGRESSION.** For the ex-ante claim to work, IS fragility
  must survive into the OOS window. It does not: **rho(IS dSharpe(+1), OOS dSharpe(+1)) = -0.18 pooled
  and NEGATIVE on all three panels** (-0.36 U56, -0.21 B136, -0.07 SMALL); rho(IS dMaxDD, OOS dMaxDD) =
  **-0.07**. In-sample latency fragility ANTI-PREDICTS out-of-sample latency fragility. No regressor and
  no model fit on IS rows can repair a transfer with the wrong sign.

  **(5) RULE 8.** PREDROBUST — the idea's own proposal, minimising the IS-fitted predicted |dMaxDD(+1)|
  inside the 2026-09-03 memo's admitted set — picks U56 M/H=42/g=0.60 (FULL 12.16%/1.1082/-20.88%, OOS
  13.41%/1.1230/-20.88%, **4b FALSE both windows at both delays**) and B136 W/H=21/g=0.75 (**OOS
  dMaxDD(+1) = -1.65 pp, the worst of the four choosers**): 4b FULL+OOS at delay +1 on **0 panels**, beats
  both rivals on **1 of 3** (bar 2). H_USABLE does not fire. REALROBUST (smallest REALISED IS |dMaxDD|,
  no model) does deliver B136 W/H=126/g=0.50 — FULL 10.69%/1.0632/-14.17% (H1/H2 1.279/0.894), **OOS
  10.80%/1.0155/-14.17%, 4b TRUE both windows at BOTH delays**, latency HELPING it (+0.95 pp) — against
  SPY FULL 15.12%/0.8845/-33.72% (DD cap -20.23%, CAGR floor 10.59%), SPY OOS 15.26%/0.8739/-33.72% and
  RULES v2 OOS 1.1019; but at rho = -0.07 one panel of three is a coin flip. **Path 4a fires 0 of 288.**

  **(6) A GATE THAT FAILED, RECORDED RATHER THAN DROPPED.** G7's first draft asserted the realised
  contiguous holding spell was <= H + one cadence gap and FAILED on all 144 books. The brake was not
  violated: it drops a name at age H, the screen may re-take it the same day, and **30.7% of fresh picks
  are such immediate re-entries**, so a spell runs **1.75x H on average (1.02-4.82x)** with no trade. G7
  now asserts the brake's true invariant (max age-since-entry among held names < H, holds on all 72
  frames) and the age regressor is documented as the ECONOMIC holding age.

  **WHAT IT CHANGES.** Nothing in RULES.md. It closes 1596's shortcut: a book's own turnover and its own
  holding age do not tell capital whether that book is latency-robust. **Idea 1592's route — restating
  PROTOCOL 4b on a latency-averaged or worst-case DD statistic read directly per book — is the surviving
  one, and this run supplies the reason it has to be:** 11 of 144 books change their OOS 4b verdict on
  one day of timing and no summary statistic sorts them. SURVIVORSHIP (rule 9): current-constituent
  panels, so levels are upper bounds; the headline is a DIFFERENCE between two timings over the same
  names on the same days, which the bias cannot manufacture.

## 2026-09-19 — idea 1600 (lane B): DOES A DD-AWARE IS-ONLY CHOOSER REACH THE 4b-PASSING GROSS RUNGS THAT ARGMAX IS SHARPE WALKS PAST? **ANSWERED: YES — 8 OF 12 CELLS AGAINST 0 OF 12, INCLUDING THE (25 bps, +1 DAY) CELL THAT KILLED THE INCUMBENT. KEEP-CANDIDATE UNDER PATH 4b. NO RULES CHANGE ENACTED (rule 6: Sunday review only).**

  **THE QUESTION.** Idea 1590 closed the same day with "0 of 48 legal IS-only choosers reach a
  4b-passing rung": argmax IS Sharpe took gross 0.95-1.00 at every one of its 48 cells and blew the
  DD cap, while every 4b pass in its grid sat at 0.50-0.75. That is a statement about the CHOOSER'S
  OBJECTIVE, not about rule 8, and the record already owns an untested alternative — the
  2026-09-03 RECOMMENDATION memo pre-registered, in writing, "smallest G whose MaxDD <= 60% of
  SPY's and CAGR >= 70% of SPY's". This run races five IS-only choosers over the same frozen book
  (N = 20, H = 126, MAXVOL 0.60, 200d gate, weekly), the same 13-rung gross ladder 0.40..1.00, on
  three panels x cost {10, 25} bps x execution delay {+0, +1}: **156 published books, 60 published
  picks, both KEEP paths at every one.**

  **(1) THE RETURN CHOOSERS DISCRIMINATE ON 0.0010 OF SHARPE AND PAY 10.9 pp OF DRAWDOWN.** Across
  the 13 rungs the IS Sharpe span is **0.0010 (U56), 0.0041 (B136), 0.0033 (SMALL)** while the IS
  MaxDD span is **10.86 / 11.41 / 18.77 pp**. Gross is a pure scale dial, so IS Sharpe is
  flat-to-increasing in it. Over the 12 cells: **ISSHARPE mean pick g 0.992, 4b 0/12; ISCALMAR
  0.983, 0/12; PREREG 0.617, 8/12; SHARPEDD (argmax IS Sharpe inside the memo's admitted set)
  0.700, 6/12; FROZEN 0.75, 4/12.** The failing OOS leg is **DD in 12 of 12 cells for both return
  choosers** and 4 of 12 for PREREG.

  **(2) THE HEADLINE BOOK.** U56, (10 bps, +0), PREREG picks **g = 0.60**: FULL **12.61% / 1.1532 /
  -15.51%** (H1 1.206, H2 1.120), **OOS 13.81% / 1.1851 / -15.51%**, 4b TRUE on BOTH windows,
  against SPY FULL 15.12% / 0.8844 / -33.72% (bars: DD cap -20.23%, CAGR floor 10.59%), SPY OOS
  15.26% / 0.8738 / -33.72% and RULES v2 OOS 9.46% / 1.2769 / -12.05%. B136 PREREG g = 0.50: FULL
  10.69% / 1.0632 / -14.17%, OOS 10.80% / 1.0155 / -14.17%, 4b TRUE both.

  **(3) IT SURVIVES THE CELL THAT KILLED THE INCUMBENT.** 1590's kill was one trading day of
  latency driving U56's g = 0.75 book from -19.13% to -21.57% through the -20.23% cap. The DD-aware
  pick is not exposed: at **(25 bps, +1 day)** U56 PREREG g = 0.60 reads FULL **11.80% / 1.0723 /
  -17.60%**, **OOS 12.66% / 1.0710 / -17.60%**, 4b TRUE both windows; B136 PREREG g = 0.50 FULL
  11.47% / 1.1214 / -13.33%, OOS 11.56% / 1.0679 / -13.33%, 4b TRUE both — while **FROZEN 0.75 and
  SHARPEDD 0.70 both FAIL there on U56, on the DD leg.** Three (panel, chooser) pairs hold 4b on
  both windows at the headline AND the realistic cell: **U56/PREREG, B136/PREREG, B136/SHARPEDD.**
  H_REACHABLE, pre-registered before the run, therefore FIRES.

  **(4) THE HONEST DEFLATION, STATED IN THE MEMO.** **rho(IS MaxDD, OOS MaxDD) = 1.0000 at all 12
  cells** (Sharpe 0.9835-1.0000). Every rung is the SAME holdings frame scaled by g, so a drawdown
  bar read in-sample pins the same ordering out-of-sample BY CONSTRUCTION. This is a
  **leverage-selection** result, not a forecasting one — which is exactly why it survives rule 8,
  and exactly why it is worth less than a signal discovery. **Path 4a fires 2 of 156 FULL and 0 of
  156 OOS: a 4b claim only.** SMALL passes nothing at any of its 4 cells (shelf size 0).

  **(5) GATES 10/10.** G0 16.7y; **G1 the committed 2026-09-04 U56 frozen anchor replayed at
  3.72e-05**; G2 exactly two tuned parameters (chooser objective, gross rung — cost and delay are
  published stress axes, every cell reported); G3 the cost ladder an exact identity on one turnover
  path (0.00e+00); G4 max realised gross 1.000000; **G5 every IS statistic recomputed on a
  hard-truncated array, 0.00e+00 — no chooser can see a 2017+ row even by accident**; G6 all 156
  ladder cells and all 60 picks published; G7 delay +0 == the protocol convention (0.00e+00); G8
  every PREREG / SHARPEDD pick re-derived from the published IS columns alone agrees with the pick
  taken in the loop. Deterministic, offline, 11.2s. **SURVIVORSHIP (rule 9):** U56 55 names, B136
  135, SMALL 665 investable after the `small_meta` max_1d_move filter; all current-constituent
  lists, so every absolute level is an UPPER BOUND and the headline is a CONTRAST BETWEEN CHOOSERS
  over the SAME books on the SAME days. **PROPOSED, NOT ENACTED** — memo at
  `research/backtests/2026-09-19_dd-aware-is-only-chooser_B.memo.md` carries the exact RULES
  clause-3 wording for the Sunday review.

## 2026-09-19 — idea 1590 (lane cloud, idea 2 of 2): DOES THE STANDING 4b BOOK SURVIVE 25 AND 50 bps AND EXTRA DAYS OF EXECUTION DELAY? **ANSWERED: IT SURVIVES COST TO 120 bps AND DIES TO ONE DAY OF LATENCY AT EVERY COST RUNG, 0 bps INCLUDED. KILL FOR CAPITAL. NO RULES CHANGE ENACTED.**

  **THE QUESTION.** Every 4b pass in this record is priced at exactly 10 bps with the decision
  taken at close t-1 and applied at t. Real capital pays neither. 624 cells: 3 panels x 13 gross
  rungs (0.40..1.00 step 0.05) x cost {0, 10, 25, 50} bps x execution delay {+0, +1, +2, +3}
  trading days ON TOP of rule 2's t-1 -> t, with delay +0 being the protocol convention itself
  (G7 verified bit-for-bit against an independently rebuilt lag-1 frame, 0.00e+00). The book is
  frozen throughout: N = 20, H = 126, MAXVOL 0.60, 200d MA gate, weekly.

  **(1) COST IS NOT WHAT KILLS IT.** U56, g = 0.75, delay +0, holds 4b FULL *and* OOS at ALL FOUR
  cost rungs: 0 bps **16.14% / 1.1750 / -19.08%**, 10 bps **15.80% / 1.1537 / -19.13%** (OOS
  17.32% / 1.1857), 25 bps **15.31% / 1.1217 / -19.20%** (OOS 16.81% / 1.1546), 50 bps **14.48% /
  1.0682 / -19.35%** (OOS 15.95% / 1.1028). Bisected on its own turnover path (2.87x/yr) its 4b
  verdict does not flip until **c* = 120.3 bps** (OOS median c* on U56 139.0). Pooled over the 11
  books that pass 4b FULL at 0 bps and delay +0, **median c* = 43.8 bps** (q25 42.9, q75 103.8;
  U56 103.8, B136 43.1, SMALL none) — the pre-registered 25 bps bar is cleared on the cost axis.

  **(2) ONE DAY OF EXECUTION LATENCY DOES, AT EVERY RUNG.** U56, g = 0.75, 10 bps, vs delay +0:
  **+1 day dSharpe -0.0487, dCAGR -0.54 pp, dMaxDD -2.44 pp (-19.13% -> -21.57%, straight through
  the 4b DD cap of -20.23%), dOOS Sharpe -0.0835, 4b True -> False FULL AND OOS**; +2 days -0.0334
  / -1.37 pp; +3 days -0.0418 / -2.79 pp. At delay +1 the g = 0.75 rung fails 4b even at 0 bps.
  **The binding 4b leg is a LATENCY object, not a cost object, and no cost convention in the
  record has ever tested it.**

  **(3) AND THE LATENCY AXIS IS NOT MONOTONE — IT IS A COIN FLIP THE SIZE OF THE MARGIN.** B136's
  frozen book goes the OTHER way: **+1 day turns a 4b FAIL into a 4b PASS** (dSharpe **+0.0907**,
  dCAGR +1.81 pp, dMaxDD **+1.32 pp**, OOS 16.19%/1.0180 -> 17.98%/1.1024), then loses it at +2
  (+0.0709, -0.88 pp) and +3 (-0.0013, **-3.61 pp**). SMALL moves +0.0480 / +0.0050 / +0.0131 and
  passes nothing anywhere. Grid-wide 4b BOTH-window counts by delay: **11 / 11 / 9 / 6 at 0 bps,
  10 / 10 / 4 / 3 at 10 bps** out of 39 books per cell. **One trading day of execution timing moves
  MaxDD by 1.3-3.6 pp in EITHER direction — larger than the DD margin every 4b verdict in this
  record is decided on, and every one is quoted at one arbitrary point on that axis.**

  **(4) THE CAPITAL ARM: NO IS-ONLY CHOOSER REACHES A PASSING RUNG, ANYWHERE.** Gross chosen by
  argmax IS Sharpe on warm-up..2016-12-31 only, separately at each (cost, delay) cell so the
  chooser pays the same cost and latency the book does; 2017-2026 read once. **0 of 48 picks clear
  4b on either window and 0 of 48 clear 4a.** The chooser lands on **g = 0.95-1.00 at every one of
  the 48 cells** (IS Sharpe is flat-to-increasing in gross) and those rungs blow the DD cap. At the
  realistic **(25 bps, +1 day)** cell: U56 pick g 0.95 OOS **20.07% / 1.0731 / -26.81%**; B136 pick
  g 1.00 OOS **23.16% / 1.0719 / -25.52%**; SMALL pick g 1.00 OOS **9.16% / 0.4742 / -45.48%** —
  all 4b False on both windows against SPY OOS 15.26% / 0.8738 / -33.72% and RULES v2 OOS
  9.46% / 1.2769 (U56). Over the whole grid **4a fires 5 times FULL and 0 times OOS**. The 4b
  passes that exist sit at gross 0.50-0.75 and every legal IS-only chooser walks past them.
  **NOT PROPOSED FOR ENACTMENT.**

  **(5) GATES 12/12, AND AN HONEST LIMIT.** G1 the frozen 2026-09-04 U56 anchor replayed at the
  (10 bps, +0) cell to **3.72e-05**; G2 exactly two tuned parameters (cost rung, execution delay);
  G3 cost ladder an exact identity on one turnover path (0.00e+00); G4 max realised gross
  1.000000; G5 no chooser reads a row on or after 2017-01-01; G6 all 624 cells published;
  G7 delay +0 == the protocol convention (0.00e+00); G8 all 38 interior c* bracketed (PASS at
  c*-0.02 bp, FAIL at c*+0.02 bp). Deterministic, offline, 23.0s. **THE LIMIT, stated in the
  memo:** delay is implemented by reading the signal at close t-1-d and trading at t, which ages
  the signal and holds the rebalance calendar fixed; a real latency would also move the intraday
  fill price, so the MaxDD move is a LOWER bound on what an execution study would find, not an
  upper one. **SURVIVORSHIP (rule 9):** U56 55 names, B136 135, SMALL 665 investable after
  dropping the 54 `max_1d_move >= 1.0` tickers in `data/small_meta.csv` — the cached small pool has
  grown well past the 439 / 483 figures older memos quote, so the LABEL is stale, not the run.
  All are current-constituent lists: every absolute level and every 4a/4b pass count is an UPPER
  BOUND; the headline is a DEGRADATION over the SAME names on the SAME days.

## 2026-09-19 — idea 1570 (lane cloud, idea 1 of 2): HOW LONG A TAPE WOULD RESOLVE THE RECORD'S TYPICAL DEVICE MARGIN, AND DOES POOLING RESOLVE IT? **ANSWERED: ~147 MORE YEARS FOR THE MEDIAN CONTRAST, 24.6% OF ROWS REACHABLE BEFORE 2050, AND POOLING RESOLVES NOTHING — 0 OF 6 COMBINATIONS. KILL FOR CAPITAL. NO RULES CHANGE ENACTED.**

  **THE QUESTION.** Eight-plus runs on 2026-09-19 ended "the margin is inside its own SE" (1562:
  0 of 36 contrasts reach |t| > 2; 1511: a 2.93 pp DD SE against a 1.10 pp margin). This run
  inverts it: how much tape *would* it take, and is any of it reachable?

  **(1) ARM A — THE CENSUS. THE MEDIAN UNRESOLVED CONTRAST NEEDS 10.98x ITS OWN WINDOW.** 287
  committed 2026-09-19 CSVs scanned. A `(d, se, t)` trio is admitted only if `se` is NAMED like a
  standard error, `t` like a t statistic, `d/se` reproduces `t` to 1e-6 on >= 98% of finite rows,
  and `t` takes >= 3 distinct values (G9 — constant/boolean columns cannot match by accident):
  **50 internally validated triples, 4,371 contrast rows.** |t| min 0.000 / q25 0.299 / **median
  0.712** / q75 1.237 / q90 2.110 / q95 2.885 / max 7.648. **Resolved today: 481 of 4,371 =
  11.00%.** Required multiple of its own window on the 3,890 unresolved rows: q25 3.82x / **median
  10.98x** / q75 57.22x / q90 624.81x — extra tape q25 43.8y / **median 147.1y** / q75 919.2y /
  q90 9,984.9y. **Reachable with tape available before 2050: 24.57% of all rows, 15.24% of
  unresolved rows.** FULL 12.22% resolved vs **OOS 2.41%**; U56 13.10% / B136 11.54% / SMALL 8.16%.

  **(2) ARM B — POOLING BUYS NOTHING, AND THE NAIVE ARITHMETIC WOULD HAVE MANUFACTURED THE
  OPPOSITE.** Idea 1562's two-state-gross family, 12 cells x 2 large-cap panels = the 24
  large-cap cells, each against the constant gross whose FULL-sample CAGR it matches (worst match
  0.01 bp). ONE circular-block index set per replicate applied to all 24 cells AND their 24 twins.
  Per-cell **0 of 24 reach |t| > 2 at every L** (max 1.2817 / 1.5224 / 1.7379 at L = 21 / 63 /
  126). Pooled EQ |t| 0.5937 / 0.7137 / 0.7944; pooled inverse-variance |t| 0.9103 / 1.0794 /
  1.2138, on a margin of +0.0191 (EQ) / +0.0125-0.0128 (PREC) of Sharpe. **0 of 6 (L, scheme)
  combinations resolve. THE METHOD FINDING: the PAIRED pooled SE is 3.52x-3.78x the
  independence-assuming one; under the naive arithmetic 5 of the 6 would have read |t| = 2.24 /
  2.61 / 2.83 / 3.36 / 3.89 / 4.28 — "RESOLVED". The cells share one tape and one holdings frame.
  Every future pooled claim in this record must publish the ratio of its paired pooled SE to its
  independence-assuming SE.**

  **(3) ARM C — THE CAPITAL ARM. TWO 4b PASSES, BOTH INDISTINGUISHABLE FROM A CONSTANT DE-GROSS.**
  Rule 8, cell chosen on warm-up..2016-12-31 only, 2017-2026 read once. **U56 (MA 100, g_low
  0.5625): FULL 14.65% / 1.1817 / -16.54% (H1/H2 1.2289/1.1508), OOS 16.15% / 1.2247 / -16.54%,
  4b TRUE full AND OOS on all four legs**; vs its own CAGR-matched twin OOS +0.0393, SE 0.0418,
  **|t| 0.94**. **B136 (MA 200, g_low 0.3750): FULL 14.23% / 1.0799 / -16.69%, OOS 14.29% /
  1.0254 / -16.69%, 4b TRUE full AND OOS**; vs twin +0.0082, **|t| 0.12**. **SMALL (MA 200, g_low
  0.3750): 4a and 4b FALSE on all legs and it LOSES to its twin (-0.0336).** 4a fires 0 of 3.
  Comparands: SPY 15.12% / 0.8844 / -33.72% (OOS 15.26% / 0.8738); live RULES v2 U56 8.62% /
  1.2011 / -12.05% (OOS 9.46% / 1.2769). **NOT PROPOSED FOR ENACTMENT:** the twin is one constant
  (g* = 0.6958 on U56, 0.6649 on B136) against a device with an MA length, a threshold and a
  second gross, and the tape cannot say the device is better — so the simpler book wins by default.

  **(4) GATES 13/13, AND TWO CROSS-SCRIPT REPLAYS.** G1 the frozen 2026-09-04 U56 anchor replayed
  to **3.72e-05** (15.80%/1.1537/-19.13%, OOS 1.1857); G2 idea 1562's own headline cell to
  **3.27e-04** (14.92%/1.1788/-18.05%, OOS 1.2250). G3 exactly two tuned parameters (block length,
  pooling scheme); G4 twin CAGR match 0.01 bp; G5 no chooser reads a row on or after 2017-01-01;
  G6 max realised gross 0.7769; G7 cost ladder an exact identity (0.00e+00); G8 all 144 cells
  published (3 panels x 4 MA x 3 g_low x 4 cost rungs). Deterministic, offline, 44.9s.
  **SURVIVORSHIP (rule 9):** U56/B136 current-constituent, SMALL a current sub-$2B screen back to
  2010 with `max_1d_move >= 1.0` dropped first — absolute levels are UPPER BOUNDS; ARM A is
  bias-free and ARM B is a same-names, same-days contrast.
## 2026-09-19 — idea 1574 (lane C): IS EVERY COMMITTED MACRO AND TIMING GAIN IN THE RECORD A ONE-OR-TWO-DAY OBJECT? **ANSWERED — YES, AND THE GENERALISATION IS WORSE THAN THE QUESTION ASSUMED. KILL (H_MICRO). NO NEW BOOK, NO RULES CHANGE.**

  **THE QUESTION.** Idea 1562 found its two-state SPY-trend gross gate worth +0.0238 of pooled Sharpe
  at 1 day of signal lag, +0.0275 at 2 and +0.0001 at 5 — a margin that evaporates over four trading
  days, which is not how a state variable behaves. Every macro gate, breadth gate, trailing stop and
  vol target the record owns is read at exactly one lag and none had ever been swept. Two tuned
  parameters only — **(device FAMILY, signal LAG)** — over LAG {1, 2, 3, 5, 10, 21} x 8 families x 3
  panels = **144 published cells**, every one scored against its OWN CAGR-matched constant-gross twin
  on the same weight frame (|CAGR gap| gated < 20 bp), the comparand idea 1574 specifies.

  **(1) THE PREMISE REPRODUCES EXACTLY, ON THE FRAME IT WAS MEASURED ON, AND THE HALF-LIFE IS 2.7
  TRADING DAYS.** The main grid rides idea 1534's base book, not idea 1562's, so a separate replay arm
  rebuilt the 2026-09-04 KEEP-4b incumbent frame (3-leg composite, min-hold H = 126, N = 20) and
  reproduced the committed anchor to **0.0002 of Sharpe** (15.80% / 1.1535 / −19.13% against the
  committed 15.80% / 1.1537 / −19.13%; G1b). On that frame the two-state gate's margin over its
  CAGR-matched twin reads **+0.0254 / +0.0231 / +0.0088 / +0.0000 / +0.0006 / −0.0229** at
  L = 1 / 2 / 3 / 5 / 10 / 21. Interpolated half-life **2.7 trading days**, and by lag 21 the gate is
  worth *less than doing nothing*. The queue's own numbers are confirmed, not overturned.

  **(2) BUT ACROSS THE CLASS THERE IS MOSTLY NO GAIN FOR A HALF-LIFE TO BE A PROPERTY OF.** On idea
  1534's frame, **13 of 15 timing (family, panel) cells have a NEGATIVE lag-1 margin**. On **U56, the
  panel the live book lives on, ALL FIVE timing families are negative at lag 1**: MACRO2 −0.0019,
  BREADTH −0.0014, VOLTGT −0.0241, SPYFILT −0.0786, STOP −0.1768. The only two positive cells are
  SMALL/MACRO2 **+0.0203** and SMALL/SPYFILT **+0.0511**, and both halve in **2.5 d** and **2.3 d**.
  H_MICRO fires; H_STATE does not fire anywhere. The three eligibility-side families carried as a
  control (BAND, MAXVOL, MADIST, made to read a stale tape) behave no better, so the short half-life
  is not a property of gross-path devices specifically.

  **(3) THE LEG THAT SHOULD CHANGE HOW THE RECORD QUOTES THESE NUMBERS: NO POSITIVE TIMING MARGIN
  ANYWHERE IS RESOLVABLE, AND EVERY RESOLVED ONE IS A COST.** Paired circular-block bootstrap, 500 reps
  x 65-day blocks, seed 20260919, identical block starts across both legs and across pairs. Only **2 of
  14** timing lag-1 margins reach |t| > 2 and **both are negative** (U56 STOP t = −2.00, B136 STOP
  t = −3.00). The two positive cells read t = **+0.80** and **+0.45**. The *decay* is equally
  unresolvable — m(1)−m(5) **1 of 24**, m(1)−m(21) **0 of 24** — and the mean SE of a margin, **0.0555**,
  is twelve times the pooled lag-1-to-lag-21 spread of −0.0046. So the half-life this run measures at
  2.7 days is a real feature of the point estimates and simultaneously a quantity the tape cannot
  resolve: **the honest reading is that these margins should not be quoted as findings at all.**

  **(4) RULE 8 AND BOTH KEEP PATHS.** 4a fires **0 of 144** cells; 4b **44 of 144** (U56 31, B136 13,
  SMALL 0). Both choosers read warm-up..2016-12-31 only; 2017-01-01..end read once. Picks and their
  untouched OOS: U56 **BAND L=2** 13.73% / 1.1109 / −18.32% against the frozen BASE's 13.43% /
  **1.1133** / −17.99%; B136 **STOP L=3** 7.63% / 0.6236 / −21.46% against 13.41% / **0.9498**; SMALL
  **MAXVOL L=21** 1.73% / 0.1877 / −38.10% against 6.90% / **0.4669**. **The chooser beats doing
  nothing in 0 of 6 cells**, mean OOS Sharpe **0.6407** against the anchor's **0.8433** — the same
  shape idea 1578 reported. SPY full 15.12% / 0.8843 / −33.72%, OOS 15.26% / 0.8737; live RULES v2 on
  U56 8.62% / 1.2010 / −12.05%. The best 4b passer (U56 MADIST L=5, 12.40% / 1.1337 / −15.80%, OOS
  15.22% / 1.2952 / −15.80%) is an *eligibility control* cell picked post hoc out of 144 and chosen by
  neither chooser — **not proposed for enactment**.

  **(5) METHOD FINDING — A DEVICE CAN FALL OFF THE BOTTOM OF ITS OWN COMPARAND FAMILY.** 8 of 144 cells
  (the SMALL trailing stop at every lag, plus SMALL/MAXVOL L=3 and SMALL/MADIST L=21) land BELOW the
  CAGR of the most de-grossed book in the constant-gross family (g = 0.20..1.00), so **no CAGR-matched
  twin exists**: the device destroyed more than *all* of the gross it was supposed to be timing. They
  are published with `matched = False` and a NaN margin, and excluded from every pooled statistic and
  from the bootstrap — never silently dropped. **G4 therefore FAILS by design (13/14 gates pass)**; the
  failure is the finding, not a solver defect.

  **DISCLOSURE (rule 7).** The pre-registration originally carried three verdict branches
  (H_STATE / H_MICRO / H_UNMEASURABLE). A 3-lag smoke test on U56 alone showed they were not
  exhaustive — every timing family's lag-1 margin came out negative, which none of the three covers —
  so a fourth branch, H_NOMARGIN, was added *before* the full run. Nothing measured, no parameter, no
  rung, no ladder and no ruler changed; only the verdict taxonomy was completed. In the event
  H_NOMARGIN did not fire (2 of 15 cells are positive) and the verdict is H_MICRO.

  **GATES.** 13/14. G1 replays idea 1534's BASE and its SPYFILT L=200 / STOP d=0.100 / VOLTGT v=0.12
  cells at 0.00e+00 / 1.11e-16 / 0.00e+00 / 2.22e-16. G1b replays the committed 2026-09-04 anchor to
  0.0002. G7 confirms lag 1 IS the record's convention (bit-identical books). G3 two tuned parameters.
  G5 no chooser row on or after 2017-01-01. G6 every multiplier in [0, 1]. G8 all 144 cells published.
  G4 fails as described in (5). **SURVIVORSHIP (rule 9):** U56 and B136 are current-constituent lists
  and SMALL a current sub-$2B screen carried back to 2011, so every absolute level is an UPPER BOUND;
  the headline is a contrast between two books over the same names on the same days differing only in
  *when* a multiplier is read, which survivorship cannot manufacture.

## 2026-09-19 — idea 718 (lane B): IS "WORSE THAN RANDOM" THE GENERAL SHAPE OF A disp SELECTOR ON THIS LADDER? **ANSWERED — AND THE ANSWER SPLITS BY OUTCOME. ON THE SHARPE PERCENTILE IT IS THE TWO CELLS; ON THE KEEP PATHS IT IS THE RULE. THE PREMISE IS ALSO MISATTRIBUTED (`evol`, NOT disp) AND HALF OF IDEA 714's READING IS A BASE ARTEFACT. NO RULES CHANGE ENACTED.**

  **THE QUESTION.** Idea 714's drawdown-directed selectors landed at the 1.8th percentile of 2,000
  random picks (return-directed at 55.1%), the same direction as idea 540's SEL-DISP|v below its own
  anchor in 2 of 3 arms. The queue asked whether sub-random is THE RULE or THE TWO CELLS. Two tuned
  dials only — SELECTOR (4 characteristics x 4 transforms x 2 directions x 3 arms = 96) and
  PERCENTILE BASE (EXACT / RESAMP2000 / STRAT / PERMSEL) — x 2 outcomes (Sharpe, MaxDD) x 2 ladders
  = **1,536 published percentile cells**, every one in `.grid.csv`.

  **(1) T1 — SUB-RANDOM IS *NOT* THE RULE ON THE SHARPE PERCENTILE.** Pre-registered bars (>= 18 of
  24 = RULE, <= 15 = TWO CELLS): **14 of 24** disp cells sit below the 50th percentile on the
  INHERITED ladder and **15 of 24** on an independently re-drawn LIVE one. Mean disp percentile
  0.3993 / 0.3480. Both readings land in the coin-flip band. The queue's own antecedent — 715's
  45-of-96 at mean 0.383 — is reproduced exactly (G3) and is what it looks like: mildly negative on
  the mean, a coin flip on the count.

  **(2) BUT ON THE KEEP PATHS IT *IS* THE RULE, AND THAT IS THE LEG THAT MATTERS.** 504 books built
  as real weights functions and priced here at 10 bps, next-day, weekly, gross 0.75. **Path 4a fires
  0 of 96 picks and 0 of 504 books, full sample and OOS.** Path 4b: picks FULL 4 / OOS 3 / **BOTH 2
  (2.1%)** against the population's FULL 44 / OOS 38 / **BOTH 30 (6.0%)**. **SELECTOR LIFT −3.9 pp.**
  Mean pick OOS Sharpe **0.5194** against the pool's **0.6727**. The selectors *rank* no better than
  chance and *choose* worse than it. The two arithmetic 4b passers (top10 SEL-evol−|ratio 13.82% /
  1.0150 / −18.99% full, 14.43% / 1.0305 / −18.99% OOS; top20 SEL-disp−|ratio 10.35% / 0.9544 /
  −18.15%, OOS 11.20% / 0.9982 / −18.15%) are beaten OOS by the pool's own best book (1.1848, which
  no selector found) and dominated on all three legs by the frozen 2026-09-04 incumbent. **Not
  proposed for enactment**; the memo states the four reasons.

  **(3) THE PREMISE IS MISATTRIBUTED — `evol`, NOT disp, AND THE TRANSFORM BEATS THE CHARACTERISTIC.**
  T3 gap disp vs non-disp **+0.0216 / −0.0290** against a 0.10 bar: not disp-specific. Sub-random
  counts out of 24, both ladders: **evol 17 / 17** (mean pct 0.2629 / 0.2944), disp 14 / 15, breadth
  11 / 14, corr 13 / 8. By transform: **residx 17, dm 16** (INHERITED) and **dm 19**, residx 14
  (LIVE) against none 11 / 9 and ratio 11 / 12. On the live ladder **`dm` is worse than `residx`**,
  so idea 540's "the CONTROL inverts the ranking" is really **"the WITHIN-STRATUM DE-MEANING inverts
  it"** — the vol leg of the control adds nothing.

  **(4) HALF OF 714's READING IS A BASE ARTEFACT — THE DRAWDOWN HALF.** 714's 2,000-draw base is NOT
  a sampling artefact: EXACT vs RESAMP2000 agree to mean |diff| **0.0048 / 0.0063** (max 0.0125 /
  0.0215). But the **STRATUM-MATCHED** base — the pick's own q rung — moves the **DRAWDOWN**
  percentile from 0.3684 → **0.5052** (INHERITED) and 0.4057 → **0.5065** (LIVE), to dead random,
  disp-only 0.3852 → **0.5833** and 0.4301 → **0.5938** (ABOVE random), while the **SHARPE**
  percentile barely moves (0.3831 → 0.3984, 0.3697 → 0.4349). **Sub-random drawdown is a statement
  about WHERE argmax lands (715's extreme-q capture), not about what it ranks on. Sub-random Sharpe
  is not.** Within-cell spread across the 4 bases: mean **0.3463 / 0.3047**, max 0.8310; the
  sub-random verdict is non-unanimous across bases on **50/96 (52.1%)** and **41/96 (42.7%)** of
  cells. **The base is a bigger dial than the selector.**

  **(5) METHOD FINDING — THE COMMITTED top-n CONSTRUCTION BREACHES ITS OWN NOMINAL GROSS ON RANK
  TIES.** `(rank <= n) * gross/n` with pandas' average-rank puts more than n names in the book
  whenever the score ties at the n-th rank: **332 of 504 books breach gross 0.75 on at least one
  day, max realised 0.9750 (1.30x nominal)**, touching 24.0 of 4,203 days per breaching book
  (**0.376%** of all book-days). EWall never breaches. **PROTOCOL rule 2 is NOT violated** (max
  weight sum 0.975 <= 1.0, G5 PASS) — but nominal gross is an unstated dial in every top-n number
  this ladder has published, and it is reported rather than clipped.

  **(6) REPRODUCIBILITY BOUND — THE LADDER IS NOT REBUILDABLE.** Idea 715's gate replayed idea 533's
  panels at machine precision off a **439**-name small pool; today's cache carries **665** (+226,
  1.51x), so `rng(seed=20260909).choice` lands on different tickers. Run both ways, the sub-random
  verdict agrees on **71 of 96 cells (74.0%)**, pearson **+0.4798**, spearman **+0.4545**. The
  aggregate answer replicates; **individual cells do not, and no single-cell reading on this ladder
  — 714's included — should be quoted without its draw.**

  **SURVIVORSHIP (rule 9):** both ladder ends are current-constituent lists carried back to 2010, so
  every LEVEL is an UPPER BOUND; what is read here is a within-ladder CONTRAST over the same panels
  on the same days. **Gates 6/6 PASS** (G1 540's 12 rows at 0.0e+00, G2 4a 0/504 + 4b 41/504, G3
  715's 45 beat-anchor and 0.3831 mean percentile, G4 vintage, G5 no leverage, G6 SPY one series at
  sd 1.1e-16 while RULES v2 varies per panel). **KILL for capital. RULES.md, PROTOCOL.md, scan.py,
  bot.py and baseline.py untouched.** Script
  `research/backtests/2026-09-19_is-WORSE-THAN-RANDOM-the-general-shape-of-a-disp-selector_B.py`.
## 2026-09-19 — idea 1566 (lane C): IS MIN-HOLD RETENTION SILENTLY DISARMING EVERY ELIGIBILITY DEVICE? **ANSWERED — YES IN SUBSTANCE, NO ON THE IDEA'S OWN CONJUNCTION: T1 AND T4 PASS, T2 FAILS ON 3 OF 12 LADDERS. ONE LIVE CLAUSE MEASURES AT EXACTLY ZERO ON ONE PANEL. NO NEW BOOK, NO RULES CHANGE.**

  **THE DEFECT PRICED.** Idea 1538 could not empty the book at ANY MAXVOL rung down to m = 0.06 and
  blamed the min-hold clause: H = 126 RETAINS a held name regardless of its eligibility. This run
  measured that claim directly for the first time, on 5 configs x 5 H rungs {0, 21, 63, 126, 252}
  x 3 panels = **75 books, every one published**, and 4 devices x 5 H x 3 panels = **60 contrasts**,
  each an ON book against an OFF twin differing in ONE eligibility clause with the SCORE KEY held
  bit-identical, so the contrast is eligibility and never ranking. Two dials only (device, H).

  **(1) THE CENSUS — T1 PASSES.** `OVRC_W` = mean share of BOOK WEIGHT in names THAT DEVICE'S OWN
  CLAUSE calls ineligible and H keeps anyway. At the live H = 126, U56 / B136 / SMALL:
  **MAXVOL 0.60 0.0428 / 0.0439 / 0.1750; MAXVOL 0.35 0.1474 / 0.1958 / 0.3600; the 200d MA gate
  0.1227 / 0.1191 / 0.1803; the +/-3% band 0.1122 / 0.1074 / 0.1747.** On a DAY basis the incumbent
  U56 book carries at least one overridden name on **47.4%** of days (MAXVOL 0.60), **69.7%** (MA
  gate) and **72.5%** (band); SMALL at MAXVOL 0.35 reads **95.8%**. G8 confirms the instrument:
  both override readings are EXACTLY 0.00e+00 at H = 0, where there is no retention to override.

  **(2) T2 FAILS AND THE FAILURE IS INFORMATIVE.** OVRC_W is non-decreasing in H on only **9 of 12**
  device x panel ladders. All three violations are the TOP rung (B136/MAXVOL060 -0.0035,
  SMALL/MAXVOL060 -0.0211, SMALL/MAXVOL035 -0.0109 from H 126 to 252): a year-long hold changes the
  book's COMPOSITION enough that fewer of its names are high-vol to begin with. **"More retention
  means more disarmament" is false at the long end**, and the record should stop assuming it.

  **(3) THE STRONGEST FORM IS TRUE AND EXACT, ON ONE PANEL.** On SMALL at H >= 63 the per-name 200d
  MA gate and the +/-3% band produce **BIT-IDENTICAL books to switching them off entirely**
  (ident_share **1.000**, dSharpe **0.0000**, dMaxDD **0.00%**) while their own clause is overridden
  on **7.6-27.6%** of book weight. The mechanism is plain: the score key carries the `0.5+0.5*above`
  MA tilt, so above-MA names already win every entry contest on a 665-name panel, and retention then
  holds them through the crossings the gate was meant to catch. **An eligibility clause that never
  binds at entry and is overridden afterwards is a live rule doing nothing** — here, exactly nothing.

  **(4) THE PRICE — T4 PASSES, T3 FAILS BY ONE PANEL.** |dSharpe| against the device's own OFF twin,
  H = 0 vs H = 126: **MAXVOL060 shrinks on 3/3 panels (0.0496->0.0176, 0.0556->0.0175,
  0.2134->0.1075), MAXVOL035 3/3 (0.0790->0.0381, 0.1084->0.0523, 0.3806->0.1487), MA200 2/3,
  BAND03 2/3** — retention roughly halves every device's measured effect (T4 PASS). T3 asked whether
  the LIVE MAXVOL 0.60 inheritance is INERT at H = 126 (|dSharpe| inside one paired-bootstrap SE on
  all three panels): U56 **+0.0176 (SE 0.0472, t 0.37) INSIDE**, B136 **-0.0175 (SE 0.0581, t 0.30)
  INSIDE**, SMALL **-0.1075 (SE 0.1071, t 1.00) OUTSIDE** and costing **-3.34 pp of CAGR**. So on the
  two large-cap panels the live ceiling moves Sharpe by less than a third of its own SE; on SMALL it
  is a drag, not a protection. **T3 FAIL** — and the honest reading is "near-inert where it is free,
  expensive where it is not", not "inert".

  **(5) CAPITAL — 4a 0/75, 4b 12/75 BOTH, AND NOTHING ENACTABLE.** Path 4a fires on **0 of 75** cells
  full and OOS. Path 4b: **12/75 full = OOS = BOTH, all twelve on U56, 0/25 on B136 and 0/25 on
  SMALL**; the binding leg is DD on U56 (12/25) while H1/H2/CAGR pass 25/25. Of the twelve, one IS
  the frozen incumbent, three are argmax-IS REACHABLE and **all three are strictly worse than it**
  (C_VOL035|H126 1.0980/1.0638, D_NOMA|H126 1.1306/1.1316, E_BAND03|H126 1.1288/1.1337 full/OOS
  Sharpe vs 1.1537/1.1857). The one cell beating the incumbent on both Sharpes — **U56 D_NOMA|H252,
  full 14.71%/1.1843/-18.87%, OOS 16.14%/1.2825/-18.87%** — has IS Sharpe 1.0641 against 1.1324 for
  H126 in its own ladder, so **no legal IS-only chooser reaches it. Recorded as HINDSIGHT; no memo.**

  **(6) RULE 8.** Chooser = argmax IS Sharpe on warm-up..2016-12-31 only, 2017-2026 read ONCE. U56 ->
  B_NOVOL|H21 OOS 16.76%/1.1450/-22.63%; B136 -> B_NOVOL|H63 16.38%/0.9491/-27.38%; SMALL ->
  A_INCUMBENT|H252 9.37%/0.5935/-35.37%. **Mean OOS Sharpe 0.8959 vs 0.8812 for doing nothing (T5
  PASS) — but the whole +0.0147 is SMALL's +0.1537; on BOTH large-cap panels the chooser LOSES to
  doing nothing.** Benchmarks: SPY 15.12%/0.8844/-33.72% full and 15.26%/0.8738/-33.72% OOS; RULES v2
  on U56 8.62%/1.2011/-12.05% full and 9.46%/1.2769/-12.05% OOS.

  **WHAT THE RECORD SHOULD CARRY FORWARD.** Every eligibility result in the record was measured at
  one H without naming H as the thing doing the work: at H = 126 between 4% and 36% of book weight
  sits in names the device itself rejects, and the device's Sharpe contrast is about half what the
  same device shows at H = 0. **9/9 construction gates PASS** (G1 replays the committed 2026-09-04
  U56 anchor to 3.7e-05; G5 no leverage; G6 determinism 0.0; G7 non-anticipation 0.0; G8 census 0.0).
  RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py untouched; **no RULES change enacted.**

## 2026-09-19 — idea 1538 (lane C): IS EXPOSURE-STATE DISAGREEMENT THE THIRD LADDER AXIS, AND IS TWO NUMBERS ENOUGH? **ANSWERED — NO. `flat_one` IS A REAL, LADDER-INDEPENDENT AXIS, BUT IT IS NOT ONE NUMBER: THE RULE FAILS TO TRANSFER TO A HELD-OUT FLAT LADDER BY A FACTOR OF THIRTY. ONE INCIDENTAL KEEP-4b CANDIDATE FALLS OUT. NO RULES CHANGE ENACTED.**

  **THE DEFECT REPAIRED.** Idea 1530 refuted the SCALE/COMPOSITION dichotomy and found, post-hoc,
  that adding `flat_one` (the share of days two adjacent rungs disagree about being INVESTED AT ALL)
  took the blend-gap fit from R² 0.0154 to 0.6094 while collapsing ladder identity's contribution
  from +0.3104 to +0.0053. That was measured on 78 pairs of which **exactly ONE ladder carried any
  `flat_one`** (the trailing stop, mean 0.3190; cadence 0.0015; the other six EXACTLY 0.0000). A
  regressor fitted on one ladder's variation describes that ladder. This run BUILT the axis into
  **three independent mechanisms** and re-fitted: **L_S own-equity drawdown stop (mean flat_one
  0.3055-0.3306 across panels), L_M SPY price vs its own MA {None,200,150,100} (0.0823-0.0916),
  L_R cross-sectional breadth {None,0.35,0.50,0.65} (0.0875-0.2370)**. Gate **G11 PASSES**, so the
  re-fit is a genuine three-mechanism fit. 9 ladders x 4 rungs = 36 rungs and 27 adjacent pairs per
  panel x 3 blend weights; **351 cells, every one published.** Two tuned parameters only.

  **(1) T1 FAILS, AND IN THE DIRECTION THAT MATTERS.** Pooled over 81 pairs at lambda = 0.50 the
  two-number fit reads **R² 0.5460 (OV_HOLD) / 0.5435 (OV_CAP)** against the pre-registered 0.80
  bar — and **BELOW 1530's committed 0.6094**. Measured on three mechanisms instead of one, the
  result gets WORSE. 1530's figure was flattered by being fitted on the single ladder it described.

  **(2) T4 — THE TEST 1530 COULD NOT RUN — IS WHAT KILLS THE RULE.** Fit the two numbers on the
  OTHER EIGHT ladders and predict the held-out one: **L_M +0.7652, L_S +0.1075, L_R -32.2242**
  (OV_CAP: +0.7631 / +0.1358 / -30.8471). A rule that never saw the breadth gate misprices it by a
  factor of thirty while pricing the SPY macro gate well. **The REASON two books are flat apart is
  load-bearing: breadth-driven disagreement and stop-driven disagreement do not open the same gap.**
  A third regressor is needed. (The large negatives on the non-flat ladders — L_G -3.9e4 at
  mean |D| 0.0001 — are division by a near-zero variance, and say only that those gaps are too
  small to predict by anything.)

  **(3) WHAT SURVIVES, AND IT IS NOT NOTHING.** **T2 PASSES**: adding ladder identity (9 dummies)
  raises R² by only **+0.0238 / +0.0259** (bar 0.05) with nine ladders and three flat mechanisms to
  explain — so `flat_one` is a real axis, not a description of the stop, which is a STRONGER reading
  of 1530's +0.0053 than 1530 could support. **T3 PASSES** (worst ladder mean residual |t| 1.25).
  **T5 (rule 8 on the rule itself)** fits coefficients on warm-up..2016-12-31 gaps ONLY and reads
  2017-2026 ONCE: **OOS R² +0.7317 for two numbers against -0.0398 for one** (OV_CAP +0.7284 vs
  +0.1461). FAIL at the 0.80 bar, but the TEMPORAL generalisation is real where the CROSS-LADDER one
  is not, and that asymmetry is the finding. Fitted slope: 10 pp of `flat_one` buys ~0.040 of Sharpe
  gap against ~0.007 for 10 pp of overlap — **a 5.6x axis.**

  **(4) THE THIRD ROUTE THE IDEA ITSELF PROPOSED DOES NOT BUILD.** 1538 named "a MAXVOL rung coarse
  enough to empty the book". Carried anyway at m {0.60, 0.12, 0.08, 0.06}: mean `flat_one`
  **0.0017-0.0101**. The **min-hold H = 126 RETAINS a held name regardless of its eligibility**, so
  tightening the ceiling SHRINKS the book without EMPTYING it — on U56 the eligible SET is empty on
  1.0% of days at m = 0.12 and 2.5% at 0.10 while the BOOK is flat on **0.00%** at every m down to
  0.10 and 1.39% at 0.08 and 0.06. **MAXVOL is an eligibility dial, not an exposure-state dial**,
  and the record should stop treating the two as interchangeable.

  **(5) CAPITAL — 4a 0/351, 4b 67/351 BOTH, AND THE UNRESTRICTED CHOOSER LOSES TO DOING NOTHING.**
  Path 4a fires on **0 of 351 cells** full and OOS, matching 1530's 0/336 and 710's 0/495. Path 4b:
  71/351 full, 74/351 OOS, **67/351 BOTH**, by ladder **L_M 19, L_R 15**, then L_G 8, L_S 7, L_N 6,
  L_B 5, L_H 3, L_X 2, L_C 2; per panel U56 53/117, B136 14/117, **SMALL 0/117**. **Mean OOS Sharpe:
  ARGMAX-IS chooser 0.7588 vs DO NOTHING 0.8812 — doing nothing wins**, because on two of three
  panels the chooser is captured by L_X's unbuildable extreme rungs, which post the run's highest IS
  Sharpe (U56 1.3176, SMALL 2.0234) and collapse OOS (0.6503, 0.4760). Putting a dead ladder on the
  grid has a measurable cost and it is reported, not hidden.

  **(6) RULE 8 — ONE INCIDENTAL KEEP-4b CANDIDATE, WITH ITS LIMITS STATED AS LOUDLY AS THE PASS.**
  The chooser restricted to the three flat ladders lands on **U56 `L_M blend None|200 @ lambda 0.75`**,
  which is algebraically a **TWO-STATE GROSS** because both sleeves share one selection frame: gross
  0.75 when SPY is above its 200d MA, **0.5625** when below. Gate **G12** re-runs it as a single book
  and gets max |dSharpe| **0.0002** against the blend over all 3 lambdas x 3 panels, so the enactable
  wording IS the measured book. IS 1.1207 (incumbent 1.1158) -> **FULL 14.92% / 1.1788 / -18.05%
  (4b PASS, halves 1.2196/1.1532)** -> **OOS 16.48% / 1.2250 / -18.05% (4b PASS)**, against the frozen
  2026-09-04 incumbent's 15.80%/1.1537/-19.13% and OOS 17.32%/1.1857/-19.13%, SPY OOS
  15.26%/0.8738/-33.72% and RULES v2 OOS 9.46%/1.2769/-12.05%. Turnover 3.24x/yr, charged. On B136 at
  lambda 0.50 the same cell passes 4b full AND OOS **where the anchor fails both**.
  **THE HONEST LIMITS.** It is **1 of 3 choosers**, and the one that reaches it restricts the pool to
  the three flat ladders — no OOS row is read, but a pool restriction is a choice. The OOS Sharpe
  contrast against the anchor is **+0.0393, t = +1.06** (U56) and +0.0127, t = +0.38 (B136), paired
  circular-block bootstrap L = 65, 400 reps — **not significant**, the regime idea 1511 measured.
  **Path 4a is FALSE**, and on SMALL the cell fails 4b on both windows. **NOT proposed for
  enactment**; PROTOCOL rule 6 gives the Sunday review that call, and the exact RULES wording is
  line 10 of the memo.

  **NO LEVERAGE (rule 2):** every device on every flat ladder DE-GROSSES to cash; max realised weight
  sum 1.000000 over all 351 cells (G6). **Survivorship (rule 9):** U56 / B136 / SMALL are
  current-constituent lists carried back to 2008/2010 — every LEVEL is an UPPER BOUND; what the fit
  reads is a CONTRAST between a blend and its own two rungs over the same names on the same days.
  **Gates 14/14 PASS**, including G1 (cross-script replay of the committed 2026-09-04 U56 anchor,
  max |dev| 3.72e-05), G9 (all three exposure-state devices non-anticipating on a truncated tape)
  and G11/G12 above. Script
  `research/backtests/2026-09-19_exposure-state-disagreement-third-ladder-axis_C.py`.

## 2026-09-19 — idea 710 (lane cloud, run 7): IS THE 4b GROSS WINDOW ON BSTK100 THE SAME WINDOW IDEA 677 MEASURED? **ANSWERED — THE WINDOW IS AN (n, g) RAY, 702's 0.75 IS A GRID ARTEFACT, 677's NEGATIVE MEDIAN WIDTH IS A CORPUS PROPERTY NOT AN AXIS PROPERTY, AND ONE RULE-8-CLEAN KEEP-4b CANDIDATE FALLS OUT. NO RULES CHANGE ENACTED.**

  **WHAT WAS WRONG WITH THE COMMITTED READING.** Idea 702 ran CAND-n on BSTK100 over a THREE-RUNG
  gross ladder {0.50, 0.75, 1.00} and reported its 4b passes as a GROSS window — five of six at
  exactly g = 0.75. A three-rung ladder cannot locate an edge: "the window is 0.75" was a statement
  about the ladder. This run re-cut the axis at **0.05 resolution** (15 rungs, 0.30..1.00) x idea
  702's own 11 n rungs on three panels: **495 cells, every one published.**

  **(1) THE EDGES, AS NUMBERS.** BSTK100 / FULL, 677's interpolated leg convention (g_min = the
  CAGR floor's crossing, g_max = the DD cap's, W = g_max - g_min): **g_min runs 0.4664 (n = 5) ->
  0.7716 (n = 75) and is UNREACHABLE at n = 100; g_max runs 0.6818 -> 0.9998**, right-censored at
  1.00 for n = 100. Both edges slide RIGHT, monotonically, with n, on **3 of 3 panels**, and
  **0 of 99** (panel, window, n) rows has a non-contiguous 4b pass set, so the interpolation is
  legitimate everywhere it was used. **The window is not a gross. It is an (n, g) ray.**

  **(2) 702's "FIVE OF SIX AT EXACTLY 0.75" IS A GRID ARTEFACT.** At 0.05 the modal passing rung
  on BSTK100 is **0.70** (6 of 11 n rungs), not 0.75 (4 of 11), and the pass mass spans
  **0.55..0.95**. 0.70 was simply not on 702's ladder.

  **(3) THE REPLAY IS EXACT WHERE IT CAN BE, AND ONE COMMITTED CLAIM BREAKS.** Re-read at 702's own
  three rungs this tape gives **0/11 at 0.50, 4/11 at 0.75, 0/11 at 1.00 = 4/33** — precisely 702's
  committed NATIVE-CALENDAR count (its 6/33 headline was on idea 694's 2010-start calendar; this is
  the 2008 native tape). The headline cell replays to **max|d| = 1.3e-03**. But 702's CAGR-floor
  claim — "every g = 0.50 cell tops out at 9.51%" — is **CALENDAR-SPECIFIC and fails here**: the
  best g = 0.50 cell reaches **11.34%** and 1 of 11 clears the floor. It is recorded as **gate G2a
  FAIL**, which is the finding, not a defect. 702's DD-cap claim replicates exactly (**9/9** g = 1.00
  cells at n <= 60 fail the DD leg).

  **(4) AGAINST IDEA 677 — A SCOPE CORRECTION, NOT A CONTRADICTION.** 677 committed a gate-book
  median **W = -0.0523** with `W >= 0` in 76/180 = **0.422**, i.e. the typical book has an EMPTY 4b
  window. On CAND-n this run reads **median W = +0.1709** (BSTK100 FULL), **+0.1564** pooled over
  three panels, `W >= 0` in **28/33 = 0.848** (OOS +0.1400, 29/33). These are DIFFERENT BOOK
  CORPORA, so 677's reading is a property of its 192 gate books, not of the gross axis, and should
  be quoted with its corpus from now on. The window's LOCATION is panel-dependent (median W:
  BSTK100 +0.1709, B136 +0.1210, U56 +0.2187); its SHAPE — the monotone right-slide in n — is not.

  **(5) PATH 4a IS 0 OF 165 ON BSTK100 AND 0 OF 495 OVERALL**, confirming 702's 0/33. CAND-n never
  beats the live RULES v2 book on both halves at any gross. This family is a 4b story or nothing.

  **(6) RULE 8 — ONE KEEP-4b CANDIDATE, AND CHOOSING THE WINDOW BEATS CHOOSING THE CELL.** Dials fit
  on warm-up..2016-12-31 only, 2017-2026 read ONCE, four choosers. **C_MIDWIN** — the MIDPOINT of the
  IS leg-window at the IS-best n — lands on **BSTK100 CAND-75 @ g = 0.85**: IS 11.97% / 1.1311 /
  -11.28% (4b PASS) -> FULL 11.67% / **1.1123** / -17.35% (4b PASS, halves 1.2834/0.9485) -> **OOS
  11.42% / 1.0966 / -17.35% (4b PASS, halves 1.3050/0.8489)**, against SPY OOS 15.26% / 0.8739 /
  -33.72% and RULES v2 OOS 8.73% / 1.1215 / -12.96%. Turnover 5.47x/yr, charged; realised gross
  0.7229 (n = 75 on 100 names de-grosses the book by 0.13 on its own).

  **THE HONEST LIMIT, STATED AS LOUDLY AS THE PASS.** It is **1 of 3 choosers**: C_SHARPE and C_4b
  both take **(n = 75, g = 1.00)**, which **FAILS 4b OOS** on the DD leg. And **0 of 3 choosers on
  any panel beat RULES v2's OOS Sharpe**. The candidate clears the capital bar while staying worse
  than the live book on Sharpe — which is what path 4b was added on 2026-09-04 to allow, and exactly
  why it must not be read as a 4a result. **NOT proposed for enactment**; PROTOCOL rule 6 gives the
  Sunday review that call, and the exact RULES wording is line 10 of the memo.

  **NO LEVERAGE (rule 2):** the ladder stops at g = 1.00 where 677 swept to 1.50; a g_max not reached
  by 1.00 is reported RIGHT-CENSORED, never extrapolated. **Survivorship (rule 9):** BSTK100 / B136 /
  U56 are current-constituent lists carried back to 2008 — every level is an UPPER BOUND; what
  survives is the edges' LOCATION on the gross axis and the cross-panel comparison. **Gates 12/13**,
  the one FAIL being G2a above. Script
  `research/backtests/2026-09-19_is-the-4b-GROSS-WINDOW-on-BSTK100-the-same-window-idea-677-measured_cloud.py`.

## 2026-09-19 — idea 1547 (lane cloud, run 7): DOES THE SHY SLEEVE'S 4a PASS SURVIVE A RATE-REGIME SPLIT? **ANSWERED — THE CREDIT IS NOT A ZIRP ARTEFACT, IT IS 2.5x LARGER AFTER THE FIRST HIKE. KEEP-4a CONFIRMATION (era-robust), RESTATEMENT OF THE COMMITTED "+0.50 pp", NO NEW BOOK, NO RULES CHANGE ENACTED.**

  **THE DOUBT THIS CLOSES.** Ideas 1358 / 1498 / 1555 all credit the band's idle NAV at SHY's
  realised TOTAL return and publish the result as a property of the RULE. But SHY is not a rate:
  it is a 1-3y Treasury ETF marked to market over a tape with two monetary regimes glued together
  — ~0 carry to 2022-03-15, 0.25% -> 5.33% after, with a capital loss on the way. A credit
  measured over both at once is an average of a free lunch and a loss.

  **THE SPLIT.** ERA_ZIRP = start..2022-03-15, ERA_HIKE = 2022-03-16..end. 2022-03-16 is the
  FOMC's first hike of the 2022-23 cycle — a CALENDAR fact chosen before any return was read, and
  NOT one of the run's two tuned dials. Dials: F {0.00, 0.25, 0.50, 0.75, 1.00} (fraction of idle
  NAV in SHY) x G {0.50, 0.60, 0.75, 0.90, 1.00} (gross). Frames (reported, not tuned): LIVE
  (`baseline.rules_v2_weights`) and INC (the frozen 2026-09-04 incumbent, N = 20, H = 126). Three
  panels. **150 cells, every one published.** Because the rule-8 OOS window STRADDLES the break,
  OOS is also read split at the same date.

  **(1) OUTCOME (b), NOT (a) — THE CREDIT IS BIGGER AT TODAY'S RATES.** Anchor cell (U56/LIVE,
  G = 0.75, F = 1.00) against its own 0%-cash twin: **dCAGR +0.36 pp/yr in ERA_ZIRP, +0.91 pp/yr
  in ERA_HIKE**, full-sample +0.50 pp. Over all 120 SHY cells: **+0.196 pp -> +0.553 pp**. SHY's
  own CAGR is **0.91% ZIRP / 2.48% HIKE**; realised mean idle share 0.372 / 0.400. The credit
  identity `F x mean_idle x r_SHY` reconciles: predicted +0.212 / +0.620 against realised
  +0.196 / +0.553, mean residual **-0.017 / -0.068 pp** (max |resid| 0.486 pp).

  **(2) OUTCOME (d) FIRES — "+0.50 pp/yr" IS NOW A RETIRED FORM.** It is the length-weighted
  average of two numbers 2.5x apart, and the shorter, higher era is the one that describes the
  rate environment the book would actually run in. Every future quotation of the sleeve credit
  states its era or states both.

  **(3) 4a SURVIVES ERA_ZIRP OUTRIGHT AND IS NOT UNIFORM INSIDE ERA_HIKE.** LIVE-frame SHY cells
  clear 4a **38/60 in ERA_ZIRP and 30/60 in ERA_HIKE** (INC frame 0/60 in both, unchanged from the
  record). The anchor passes ERA_ZIRP (halves **1.2210 / 1.2124** vs live 1.1701 / 1.1482) and
  **fails ERA_HIKE on the FIRST half alone** (**1.3346** vs live 1.3518) while its second half is
  the **largest win on the whole tape** (**1.5116** vs 1.3372). The failure is **monotone in F** —
  4a in ERA_HIKE is True at F = 0.25 / 0.50 and False at F = 0.75 / 1.00 — and it is exactly the
  duration risk the record already flagged: SHY's own 2022 mark-to-market loss, paid in full and
  then recovered. ERA_HIKE is 4.5y, so its halves are ~2.2y: **a WEAK test, stated as such, and
  not a KILL.**

  **(4) RULE 8 — WITH GROSS FROZEN, THE CHOOSER FINDS THE SLEEVE FOR THE FIRST TIME IN THE
  RECORD.** Restricting the same grid to the live G = 0.75 makes F the only dial: the IS-Sharpe
  chooser picks **F = 1.00 on 6 of 6 panel-frames** and **beats doing nothing OOS 6 of 6** — mean
  dOOS Sharpe **+0.0637**, mean dOOS CAGR **+0.643 pp**, and positive in **both** OOS eras
  (+0.0500 ZIRP, +0.0810 HIKE). Ideas 1358 and 1555 both concluded the axis was a KILL as a dial;
  this run shows those failures were their grids' **IEF / TLT decoys**, not an unlearnable F.
  **On the full two-dial grid the confounding returns**: C_SHARPE picks (G = 0.50, F = 1.00) 6/6
  for +0.1385 of Sharpe and **-2.37 pp of CAGR** — the de-gross ray, found for the ninth time;
  C_CAGR picks F = 1.00 at 5/6 for +0.0407 / +0.575 pp. **GROSS remains the dial that must not be
  tuned; F is the dial that may be.**

  **(5) 4b UNMOVED.** The anchor still fails the CAGR floor in both eras (9.12% full vs SPY's
  10.59% bar; OOS 10.14% vs 10.68%). 36/150 cells clear 4b full, all already-known high-gross
  books. This run moves no 4b verdict and proposes no rule change — PROTOCOL rule 6 gives the
  Sunday review that call. The exact RULES wording, if it is ever enacted, is line 10 of the memo.

  **GATES 15/15**, including G1 F = 0 invariance at **0.000e+00**, G2 replay of
  `baseline.compare`'s RULES v2 row at **1.7e-17**, and G3 replay of ideas 1498/1555's committed
  anchor (9.12% / 1.2675 / -11.48%) at **max|d| = 2.69e-05**. Survivorship (rule 9): U56 / B136
  current-constituent lists, SMALL a current sub-$2B screen (665 names kept of 719 priced; the
  mandated `max_1d_move >= 1.0` filter drops 54) carried back to 2010 — every absolute level is an
  UPPER BOUND; the SHY-vs-cash and era contrasts share one construction and survive it.
  Script `research/backtests/2026-09-19_does-the-SHY-SLEEVE-s-4a-PASS-SURVIVE-a-RATE-REGIME-SPLIT_cloud.py`.

## 2026-09-19 — idea 1555 (lane B): WHERE SHOULD GATED-OUT WEIGHT GO? **ANSWERED — INTO SHY, AND THE COMPETING FIX IS KILLED. KEEP-4a CONFIRMATION (U56 + B136 / LIVE, rule-8 clean as REALISM), KILL FOR THE DIAL, KILL FOR IDEA 1454's ABOLITION. NO NEW BOOK, NO RULES CHANGE ENACTED.**

  **THE DEFECT THIS CLOSES.** RULES v2 clause 2 sends band-gated weight to CASH at 0.00%/yr and
  "never re-spreads" it. That destination was never chosen — it is what the first implementation
  happened to do — and TWO INCOMPATIBLE FIXES for it stood in the record, filed four hours apart
  and never raced: idea **1454** (the live book fails 4b on the CAGR FLOOR ALONE, so ABOLISH the
  cash leg, G = 1.00) and ideas **1358 / 1498** (CREDIT the cash leg with SHY, the first device in
  twelve runs to clear path 4a at all). They cannot both be right. This run puts both — and five
  other destinations — on the same tape at IDENTICAL selection and IDENTICAL 100% of NAV.

  **CONSTRUCTION.** DEST {CASH, SHY, IEF, TLT, GLD, SPY, RESPREAD} x F {0.00, 0.25, 0.50, 0.75,
  1.00}, the two and only tuned dials. **GROSS IS FROZEN at G = 0.75** (the live value and the
  2026-09-04 anchor value) — 1498 already swept it and sweeping it again would be a third
  parameter. Frames (reported, not dials): **LIVE** = `baseline.rules_v2_weights`; **INC** = the
  frozen 2026-09-04 incumbent (N = 20, H = 126). Three panels. **210 cells, every one published.**
  RESPREAD is not an asset: the gated-out weight is re-spread pro rata over the names still inside
  the band, which at F = 1.00 IS idea 1454's abolition made conditional; an empty band leaves the
  book in 0% cash, stated not glossed. Every sleeve's returns come from the SAME reference tape on
  every panel, so the destination contrast is not confounded by which panel prices the sleeve.

  **(1) THE FRAMING CONTROL — 1498's READING SURVIVES.** 1358's ladder (SHY / IEF / TLT) was all
  bonds, so it could not distinguish "cash earns something" from "the band under-deploys". Adding
  an EQUITY sleeve does. **SPY clears path 4a at 0 of 30 cells.** On U56/LIVE it buys **+8.27 pp/yr
  of CAGR (8.51% -> 16.78%)** and pays **0.1516 of Sharpe and 18.24 pp of drawdown** for it,
  monotone in F at 4 of 4 rungs (Sharpe 1.2011 / 1.1788 / 1.1263 / 1.0764 / 1.0350). The band's
  de-gross is buying REAL risk reduction, and only a LOW-VOL residual keeps it. 1498's headline is
  therefore NOT a disguised under-deployment result.

  **(2) IDEA 1454's FIX IS KILLED OUTRIGHT BY IDEA 1498's.** RESPREAD at F = 1.00 against SHY at
  F = 1.00, same names, same days: **loses on Sharpe at 6 of 6 panel-frames (mean -0.0630 full,
  -0.0725 OOS)**, **loses on MaxDD at 6 of 6 (mean -12.20 pp DEEPER)**, and wins only on CAGR
  (6 of 6, +5.39 pp). U56/LIVE turnover goes **1.77 -> 5.68x/yr**. It is the de-gross ray the
  record has re-found eight times, paid for at full price. **1454's proposed G = 1.00 should not
  be enacted.**

  **(3) PATH 4a — 10 of 210 FULL, 8 FULL *AND* OOS, AND EVERY ONE OF THE 8 IS SHY ON THE LIVE
  FRAME.** All four F rungs on U56 **and** all four on B136, so the pass is a WHOLE LADDER, not a
  corner: U56/LIVE Sharpe 1.2190 / 1.2361 / 1.2523 / 1.2675 and MaxDD -11.91% / -11.77% / -11.63%
  / -11.48%, monotone in F on Sharpe, CAGR **and** drawdown at once. Best cell **U56/LIVE SHY
  F = 1.00: full 9.12% / 1.2675 / -11.48%, halves 1.278 / 1.264** against live 1.228 / 1.181, **OOS
  10.14% / 1.3560 / -11.48%** against live OOS 1.2769; turnover 1.77 -> 2.80x/yr, charged. **This
  is idea 1498's standing candidate, not a new one** — it is replayed here to the committed decimal
  (G3). **4a at F = 0.00 is 0 of 42**, all seven destinations bit-identical there (G1 = 0.000e+00).
  Mean dSharpe vs the cash twin by destination: **GLD +0.0715, IEF +0.0504, SHY +0.0327, SPY
  -0.0001, RESPREAD -0.0028, TLT -0.0242.**

  **(4) AS A TUNED DIAL THE AXIS IS A KILL, REPRODUCING 1358 ON AN INDEPENDENT GRID.** Dials fit on
  warm-up..2016-12-31 only, 2017-2026 read ONCE. **C_SHARPE picks IEF x3 and TLT x3 and NEVER finds
  SHY** — mean OOS dSharpe **-0.0274** against doing nothing, beats it **1 of 6**. **C_CAGR**
  picks TLT x3 / RESPREAD x2 / CASH x1 — **-0.0699, 0 of 6**. 1358 reached the same conclusion from
  a (SLEEVE, GROSS) grid; this run reaches it from a (DESTINATION, FRACTION) grid at frozen gross,
  so the failure is the chooser's, not the parameterisation's. The **ex-post best 4b cell of all
  210** — U56/LIVE **GLD F = 0.50**, full 11.51% / 1.2634 / -13.70%, OOS 13.26% / **1.4204** /
  -13.70% — is reached by NO chooser and clears 4a at 0 of 30. **H_HINDSIGHT fires again.**

  **(5) PATH 4b.** 40 of 210 full and 40 full AND OOS, **none of them a new book**: U56/INC SHY
  inherits the 2026-09-04 candidate's 5 passes, and the GLD / IEF / TLT passes are the hindsight
  cells of (4). The LIVE-frame book still fails 4b on the CAGR floor at every destination that does
  not buy it with beta — exactly what 1454 and 1498 found, now confirmed against five more
  destinations.

  **(6) WHAT THE BOOK ACTUALLY IS.** RULES v2's realised mean gross, published not asserted (G8c):
  **U56 0.5328 / B136 0.5322 / SMALL 0.4051**. The live rules leave nearly HALF of NAV idle, which
  is the only reason the destination matters at all. At F = 1.00 the 4a candidate holds a mean
  **46.7% of NAV in short Treasuries** — a half-bond book whose 4a win is **DIVERSIFICATION, NOT
  ALPHA** (CAGR +0.50 pp; vol falls).

  **THE HONEST LIMITS.** (a) There is **no zero-duration instrument in the committed cache** (no
  BIL, no SHV): SHY is the cheapest proxy available and is marked to market — own profile FULL
  1.31% / 0.958 / **-5.71%**, IS 0.81% / -1.08%, OOS 1.72% / -5.71%. Every "credit the cash" number
  in this record is optimistic for the ZIRP years and carries genuine duration risk afterwards.
  (b) The 4a pass is **LIVE frame and large-cap only**: 0 of 30 on SMALL, 0 of 30 on INC. (c) GLD
  beats SHY on Sharpe at F = 0.25 (1.2770 vs 1.2675) and still fails 4a on drawdown.

  **GATES 8/8**: G0 samples 18.7y / 18.7y / 16.7y (rule 1); **G1 destination invariance at F = 0,
  0.000e+00** over 6 dests x 6 panel-frames; **G2 LIVE/(CASH, 0.00) reproduces
  `baseline.rules_v2_weights` to 1.249e-16** on all three panels; **G3 U56 SHY F = 1.00 reproduces
  idea 1498's two committed cells exactly** (LIVE 9.12% / 1.2675 / -11.48%, INC 16.16% / 1.1787 /
  -18.88%); G4 no leverage (max deployed 1.000000000000); G5 exactly two tuned parameters; G6 no
  chooser input reads a row on or after 2017-01-01, tested by refit not asserted; G7 all 210 cells
  published. G8 publishes every sleeve's standalone profile and RESPREAD's realised mean gross
  (1.0000 at F = 1.00 on all six panel-frames).

  **SURVIVORSHIP (rule 9).** U56 / B136 are CURRENT-constituent lists and SMALL a CURRENT sub-$2B
  screen carried back to 2010; every absolute level is an UPPER BOUND. The headlines are CONTRASTS
  between destinations over the SAME names on the SAME days, so they are first-order immune; the
  4a / 4b pass counts are not.

  **VERDICT. KEEP-4a CONFIRMATION of idea 1498's candidate (U56 + B136 / LIVE, SHY), now carrying
  the equity control it lacked; KILL for idea 1454's abolition; KILL for the destination as a tuned
  dial (rule 8). Enact the residual instrument as REALISM with SHY FIXED, never as a knob.**
  Memo `research/backtests/2026-09-19_where-should-gated-out-weight-go_B.memo.md`. **No RULES
  change:** RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py untouched (rule 6 reserves
  enactment for the Sunday review).

## 2026-09-19 — idea 1511 (lane cloud): does a DOWNSIDE-ONLY VOLATILITY GATE beat the incumbent's TWO-SIDED vol20? **ANSWERED — NO, ON EVERY ARM, AND THE PREMISE IS FALSE BEFORE THE GATE STATISTIC IS EVEN CHANGED. KILL. ONE METHOD FINDING THAT INVALIDATES A WHOLE CLASS OF DRAWDOWN CLAIMS. NO RULES CHANGE PROPOSED.**

  **THE FRAME.**  Four gate statistics on the frozen 2026-09-04 incumbent: **VOL** (its own
  two-sided std, the control), **SEMI0** (downside semi-deviation about zero), **SEMIM** (about the
  window mean) and **UPM** (ABOVE the window mean — **the placebo**).  SEMIM and UPM are an EXACT
  decomposition of the control: gate **G10 asserts SEMIM^2 + UPM^2 = VOL^2 * (w-1)/w pointwise to
  2.8e-14** (the factor is pandas' ddof=1 in the INCUMBENT'S own rolling std, which VOL must keep —
  it is why G2 is bit-identical).  Two dials: window w {10, 20, 40, 60} and target pass rate
  q {0.70, 0.80, 0.90, p*, 1.00}, every threshold the q-quantile of ITS OWN statistic over
  IN-SAMPLE priced cells only, applied unchanged to 2017-2026.  **80 cells per panel, 240 in all,
  every one published.**  All **11 gates pass**: G1 replays the committed U56 anchor to
  **3.7e-05**, G2 recovers threshold **exactly 0.600000** and is **bit-identical (0.000e+00)**,
  G8 matches every pass rate to **3e-05**.

  **(0) THE PREMISE IS FALSE.**  The incumbent's own pass rate p* — the IS share of priced
  name-days with vol20 < 0.60 — is **96.68% (U56), 96.84% (B136), 88.13% (SMALL)**.  The screen
  this idea set out to improve excludes **3.3% / 3.2% / 11.9%** of name-days.  Removing it
  **entirely** costs U56 **0.0176 of Sharpe at t -0.37** while ADDING 0.08 pp/yr of CAGR, and on
  SMALL it **IMPROVES** Sharpe by **+0.1075** and drawdown by **+4.51 pp**.  A dial that barely
  turns cannot be improved by relabelling it.

  **(1) THE DRAWDOWN LEG DOES NOT WIDEN — B1 FAIL.**  Mean SEMI0 dMaxDD against the matched VOL
  control: **U56 +0.61 pp, B136 +0.74 pp** against a pre-registered +1.0 pp bar.  SEMIM is WORSE
  than the control on both (**-0.39 / -0.13 pp**).  SMALL's +3.00 pp is bought with -0.0099 of
  Sharpe and -0.38 pp/yr of CAGR on the panel where nothing passes 4b at all.

  **(2) THE PLACEBO KILLS THE STORY.**  Screening on UPSIDE dispersion does what screening on
  DOWNSIDE dispersion does.  Mean dMaxDD vs control: U56 **downside +0.11 pp vs upside +0.25 pp
  (the PLACEBO WINS)**, B136 +0.31 vs +0.12, SMALL +1.64 vs +0.61.  Mean dSharpe: U56 **+0.0015 vs
  +0.0020 (placebo wins again)**, B136 -0.0020 vs -0.0132, SMALL **-0.0099 vs +0.0023 (placebo
  wins)**.  What little these gates do, they do by being a dispersion screen at a given pass rate —
  not by which tail they read.

  **(3) THE METHOD FINDING — THE BINDING 4b DRAWDOWN LEG IS NOT MEASURABLE AT THIS SAMPLE LENGTH.**
  **0 of 240 cells reach |t| > 2 on dMaxDD** (max |t| anywhere **1.72**), and the paired
  circular-block bootstrap SE of the drawdown contrast averages **2.93 pp — 2.7x the anchor's
  ENTIRE 1.10 pp 4b margin** (-19.13% against a -20.23% cap).  Realised MaxDD spans **4.66 pp
  (U56) / 8.63 pp (B136) / 8.94 pp (SMALL)** across each panel's 80 cells.  **Any committed claim
  that a device MOVED the binding 4b drawdown leg by less than ~3 pp is inside its own SE and is
  not a finding.**  Ideas 1409 and 1515 each found a CONVENTION that swamps this leg; this run
  finds the leg is **unresolvable in principle** at 16.7 years, whatever the dial.  Filed as idea
  1542, with the constructive half attached (is there a drawdown-path statistic whose contrast SE
  can adjudicate a 1 pp move?).

  **(4) 5 OF THE 6 RESOLVED CELLS RUN THE WRONG WAY.**  Of 240 cells, six reach |t| > 2 on dSharpe
  and five are NEGATIVE (U56 VOL/w10 -0.0852, VOL/w40 -0.1091, **SEMIM/w20 -0.0775 at t -2.84**,
  UPM/w40 -0.1132 and -0.0899); the single positive (B136 SEMIM/w10/q0.90, +0.0959, t +2.26) does
  not survive rule 8.

  **(5) BOTH KEEP PATHS.**  **4a 0 of 240 full and 0 of 240 OOS** — another consecutive 4a zero.
  **4b 59 full / 58 OOS / 58 BOTH**: U56 43 of 80 (**UPM the PLACEBO produces the most, 13 of 20**,
  vs VOL 10 / SEMI0 11 / SEMIM 9), B136 16 of 80, **SMALL 0 of 80**.  DD is the binding leg on both
  surviving panels (U56 43/80, B136 17/80) while H1, H2 and the CAGR floor pass 80/80 on U56.
  **Sorted by OOS Sharpe the best 4b-BOTH cell in all 240 IS the frozen incumbent (1.1857); the
  best challenger is UPM/w60/q0.80 at 1.1832 — the placebo.**

  **(6) RULE 8 — B3 FAILS ON 3 OF 3 PANELS.**  Both dials AND every threshold fitted on
  warm-up..2016-12-31.  The downside-only chooser picks U56 SEMIM/w10/q0.80 -> OOS
  **14.88% / 1.0937 / -21.51%** vs the anchor's **17.32% / 1.1857 / -19.13%**; B136 SEMIM/w20/q0.80
  -> **13.19% / 0.8859 / -22.63%** vs **16.19% / 1.0180 / -20.74%**; SMALL SEMI0/w10/q0.70 ->
  **5.24% / 0.3790 / -33.14%** vs **6.70% / 0.4398 / -36.51%**.  **It loses OOS Sharpe 3 of 3 and
  OOS CAGR 3 of 3, by 2.44 / 3.00 / 1.46 pp/yr.**  Doing nothing wins.

  Script `research/backtests/2026-09-19_downside-only-volatility-gate_cloud.py`; `.grid.csv`
  (240 cells), `.matched.csv`, `.walkforward.csv`, `.gates.csv`, `.log.txt`, `.result.md`.
  SURVIVORSHIP (rule 9): U56/B136 current-constituent lists, SMALL a current sub-$2B screen carried
  back to 2010 (the protocol's max_1d_move >= 1.0 filter applied), so every absolute level is an
  UPPER BOUND — and the bias runs AGAINST a downside screen, since a survivor's drawdown was by
  selection one it recovered from.

## 2026-09-19 — idea 1530 (lane cloud): is SCALE vs COMPOSITION the RIGHT TAXONOMY for every LADDER the record owns? **ANSWERED — NO, AND THE REFUTATION IS DOUBLE-SIDED. KILL FOR CAPITAL. ONE CONSTRUCTIVE RESIDUE AND ONE METHOD FINDING. NO RULES CHANGE PROPOSED.**

  **WHY THIS IDEA.**  Idea 1509 found that a two-rung capital blend can differ from a single rung
  only when the two rungs HOLD DIFFERENT THINGS, and verified it on exactly TWO ladders: gross
  (SCALE) and min-hold (COMPOSITION).  Two ladders is not a taxonomy.  If holdings overlap really
  were a sufficient statistic, no ladder in the record would ever need re-cutting twice.

  **THE FRAME.**  8 ladders off the frozen 2026-09-04 incumbent, each moving ONE dial and nothing
  else: L_G gross, L_T vol target, L_S trailing-equity stop (**pre-registered SCALE**); L_N, L_H
  min-hold, L_C cadence, L_V MAXVOL, L_B MA band (**pre-registered COMPOSITION**).  34 rungs, 26
  adjacent pairs, 3 blend weights -> **112 cells per panel, 336 in all on U56 / B136 / SMALL, every
  one published**.  Two dials: blend weight lambda {0.25, 0.50, 0.75} and overlap statistic
  {OV_HOLD composition-only, OV_CAP capital-inclusive}.  All **10 gates pass**; G1 replays the
  committed anchor to **3.7e-05** and G2 shows it **bit-identical (0.000e+00)** on all 8 ladders.

  **(1) 1509'S MECHANISM REPLAYS EXACTLY.**  G7: the lambda-blend of gross 0.50 and 1.00 equals the
  single gross rung at the blended exposure to **|dSharpe| 0.000e+00**.  L_G max |D| **0.0002**,
  L_T max |D| **0.0031**.  Two SCALE ladders, confirmed.

  **(2) AND THEN THE COMPOSITION SIDE TURNS OUT TO BE EMPTY.**  D = Sharpe(blend) - the
  lambda-weighted rung Sharpes never becomes material on any pre-registered COMPOSITION ladder:
  max |D| **0.0074** (L_B), **0.0165** (L_N, L_V), **0.0249** (L_C), **0.0255** (L_H).  **93% of
  the 69 non-stop pairs sit below 0.02.**  The pre-registered label agrees on **26 of 78 pairs
  (33.3%)**, and all 26 are SCALE labels.

  **(3) THE ONE LADDER THAT DOES OPEN A GAP WAS PRE-REGISTERED AS SCALE.**  L_S (trailing stop) has
  OV_HOLD **1.0000** — whenever both rungs are invested they hold IDENTICAL portfolios — yet mean D
  **+0.1247**, max **+0.5421** (B136 0.15 -> 0.10: Sharpe -0.3802 and 0.8374 blend to 0.7707).
  **Overlap does not even ORDER the gaps**: the lowest-overlap pair in the run (SMALL L_C M -> Q,
  OV_HOLD **0.2915**) opens a gap 33x SMALLER than an overlap-1.0000 stop pair.

  **(4) ALL THREE PRE-REGISTERED SUFFICIENCY BARS FAIL, TWICE OVER.**  D ~ (1 - OV_HOLD): R^2
  **0.0154**, ladder identity adds **+0.3104**, L_S residual **t +4.30**.  D ~ (1 - OV_CAP): R^2
  **0.1117**, **+0.3326**, **t +4.65**.  S1 (R^2 >= 0.80), S2 (dR^2 < 0.05) and S3 (no ladder
  |t| > 2) all FAIL on both statistics.

  **(5) RULE 8 ON THE TAXONOMY: THE BINARY CUT IS WORSE THAN ASSUMING EVERY LADDER IS SCALE.**
  theta chosen on warm-up..2016 gaps only.  OV_HOLD: IS 93.6% (baseline 91.0%) -> **OOS 87.2%
  against an 89.7% majority-class baseline**; OV_CAP: IS 96.2% -> **OOS 82.1%**.  Used as a
  classifier the taxonomy DESTROYS information.

  **(6) THE CONSTRUCTIVE RESIDUE (POST-HOC, LABELLED AS SUCH): THE MISSING AXIS IS EXPOSURE STATE.**
  OV_HOLD is blind by construction to days when exactly one rung is flat, and L_S is the only
  ladder that has any (flat_one **0.3190** vs **0.0000-0.0015** everywhere else).  Adding flat_one:
  **R^2 0.0154 -> 0.6094**, ladder identity **+0.3104 -> +0.0053**, worst ladder **t +4.30 -> -0.49**.
  **Two numbers make ladder identity redundant; one does not.**  R^2 0.61 is still short of the
  0.80 bar and the second regressor is fitted on ONE ladder's variation, so this is a hypothesis,
  filed as idea 1538, not a finding.

  **(7) METHOD FINDING — THE RECORD'S NAIVE BLEND CHARGE UNDER-COSTS A REAL BLEND.**  The gate
  premise "netted <= naive" is **FALSE** (222 of 234 blends violate it) because the naive
  lambda-weighted charge omits the cost of RESTORING the capital split.  The correct bound,
  netted <= naive + split-restoration, passes **0 of 234**.  A daily constant-mix blend spends
  **0.57 bp/yr** on restoration and costs **+0.21 bp/yr MORE** than the naive ruler says:
  cross-sleeve netting saves LESS than restoration costs.  Small, and of the opposite sign to the
  one a blend ruler is usually assumed to have.

  **(8) BOTH KEEP PATHS.**  **4a 0 of 336 full and 0 of 336 OOS** — another consecutive 4a zero.
  **4b 76 full / 73 OOS / 70 BOTH of 336**: U56 53 of 112 (all INHERITED from the anchor, which
  passes both windows), B136 17 of 112 (all CREATED by de-gross devices, 10 on L_T alone, the B136
  anchor itself failing at -20.74% against a -20.23% cap), SMALL 0 of 112.  **DD is the binding leg
  everywhere.**  The one literal candidate, U56 L_T = 0.15 (a 15% vol target on the incumbent),
  is full **15.01% / 1.1806 / -16.61%** and OOS **15.99% / 1.2048 / -16.61%** — it beats the anchor
  on Sharpe and cuts 2.52 pp of drawdown, but by **+0.0192 of Sharpe at t +0.39** (UNRESOLVED) while
  giving up **1.33 pp/yr of OOS CAGR**.  Rejected: another de-gross-shaped near-miss.

  **(9) RULE 8 CAPITAL ARM.**  U56 picks L_V = 0.30 and **LOSES** (OOS 1.0163 vs anchor 1.1857,
  t -1.91); B136 picks L_B = 0.10 and wins (1.1502 vs 1.0180, t +1.31); SMALL picks L_H = 252 and
  wins (0.5935 vs 0.4398, t +0.95).  Mean 0.9200 vs 0.8812 for doing nothing — but the one panel it
  loses on is the ONLY panel where the anchor is a 4b passer, and no panel resolves at |t| > 2.
  **Doing nothing remains unbeaten where it matters.**

  Script `research/backtests/2026-09-19_scale-vs-composition-ladder-taxonomy_cloud.py`;
  `.grid.csv` (336 cells), `.pairs.csv` (78 pairs x 3 lambdas), `.fit.csv`, `.posthoc_fit.csv`,
  `.class.csv`, `.rule8_taxonomy.csv`, `.walkforward.csv`, `.gates.csv`, `.log.txt`,
  `.result.md`.  SURVIVORSHIP (rule 9): U56/B136 current-constituent lists, SMALL a current
  sub-$2B screen carried back to 2010 (the protocol's max_1d_move >= 1.0 filter applied), so every
  absolute level is an UPPER BOUND; the run reads CONTRASTS between books over the same names on
  the same days, which the bias cannot manufacture.

## 2026-09-19 — idea 1515 (lane B): does WINSORISING the MOMENTUM LEGS against SINGLE-DAY JUMPS change which names the incumbent holds? **ANSWERED — YES ON THE HOLDINGS, NO ON THE MONEY. KILL FOR CAPITAL. ONE METHOD FINDING: A SECOND UNDECLARED CONVENTION SWAMPS THE ONLY BINDING 4b LEG. NO RULES CHANGE PROPOSED.**

  **WHY THIS IDEA.**  The standing 2026-09-04 KEEP-4b incumbent ranks on three RAW CUMULATIVE
  RETURN legs — (skip 21, look 252), (0, 126), (0, 63).  A cumulative return is a product of daily
  returns, so ONE gap day enters every leg spanning it at full weight and can carry a name into the
  top 20 on a single print.  Nothing in this record had asked whether the incumbent's holdings are
  being SET by such days.

  **THE FRAME.**  Two dials and no more: CLIP c {1.5, 2.0, 2.5, 3.0, 4.0, inf} x SIGMA WINDOW w
  {20, 60, 126, 252}, where c = inf IS the frozen incumbent at every window.  **24 cells per panel,
  72 in all, every one published** in the .grid.csv.  ONLY the three ranking legs see the clipped
  tape; the 200d MA gate, the vol20 screen and all REALISED P&L are the real tape — a book that
  traded a clipped tape would be marking itself to a price that does not exist.  sigma_t is a
  rolling std through t-1, so the clip on day t reads only days strictly before it (G7 replays a
  truncated tape bit-identically).  All 10 gates pass; G1 replays the committed 2026-09-04 U56
  anchor (15.80% / 1.1537 / -19.13% full; 17.32% / 1.1857 / -19.13% OOS) to **3.7e-05**.

  **(1) THE PREMISE IS CONFIRMED, AND LARGER THAN EXPECTED.**  Clipping only **0.53%-14.54% of
  days** changes the held set at **86.1%-100.0% of rebalances**; Jaccard against the incumbent
  falls to **0.465**; up to **54.3% of name-days** change.  The incumbent's top-20 genuinely is
  jump-set.

  **(2) IT DOES NOT PAY, AND NOT ONE CELL RESOLVES.**  25 of 60 clipped books beat the frozen
  incumbent on full-sample Sharpe and 42 of 60 OOS, but **0 of 120 contrasts reach |t| > 2 in
  either direction** (max |t| anywhere **1.62**; paired circular-block bootstrap, 400 reps x 63-row
  blocks, seed 20260919, identical block starts).  Mean dSharpe **-0.0104**, mean dCAGR **-0.22
  pp/yr**.  As a capital device the clip is unresolved and therefore dead.

  **(3) THE DOSE-RESPONSE RUNS THE WRONG WAY, ON 3 OF 3 PANELS.**  The HIGH-reorder tercile has a
  LOWER mean dSharpe than the LOW-reorder tercile on U56 (**+0.0147 -> -0.0206**), B136 (**-0.0019
  -> -0.0165**) and SMALL (**-0.0067 -> -0.0638**) alike, and |dSharpe| rises with name-days
  changed at rho **+0.40 / +0.53 / +0.69**.  Pooled over 60 cells this is a real gradient even
  though no single cell carries it.  **The jump content of the three legs is NOT noise the ranking
  would be better off without** — removing it makes the book worse, monotonically in dose.  This is
  a finding against the idea's own hypothesis and is recorded as one.

  **(4) BOTH KEEP PATHS.**  **4a 0 of 72 — another consecutive 4a zero.  NO ORDINAL IS CLAIMED: lane cloud's idea 1523 landed its own 4a zero concurrently today and numbered it thirteenth, so the count is not well defined across lanes**, for the standing
  reason: a re-selection of the same eligible pool at the same gross cannot out-Sharpe the low-vol
  RULES v2 book in both halves while matching its -12.05% MaxDD.  **4b 14 full / 14 OOS / 14 BOTH
  of 72**: U56 8 of 24 (the frozen anchor passes; 4 of 20 clipped cells inherit it), **B136 6 of 24
  — all six CREATED by the clip, since the B136 anchor itself FAILS at -20.74% against a -20.23%
  cap** — SMALL 0 of 24.

  **(5) THE ONE LITERAL CANDIDATE, AND WHY IT IS REJECTED.**  B136, c = 3.0, w = 252, **rule-8
  selected**: full 15.90% / 1.0663 / -19.50% (halves 1.2906 / 0.8912), OOS 15.61% / 0.9959 /
  -19.50%; it passes 4b on BOTH windows where the anchor fails.  It is nonetheless **strictly worse
  than the anchor it perturbs** on OOS Sharpe (**-0.0220, t -0.62**) and OOS CAGR (**-0.58 pp/yr**).
  It passes on DRAWDOWN ALONE.

  **(6) AND THAT DRAWDOWN PASS IS A LOTTERY — THE METHOD FINDING.**  MaxDD across the 24 B136 cells
  spans **2.30 pp** (-21.80% .. -19.50%) around a cap at -20.23%; on U56 it spans **5.48 pp**
  (-24.46% .. -18.98%) against the anchor's ENTIRE **+1.10 pp** 4b margin; on SMALL **7.87 pp**.
  Every 4b verdict that moves in this run moves on the DD leg alone — the halves and the CAGR floor
  are decided identically at every clip on U56 and B136.  **This reproduces idea 1409's finding (the
  binding 4b leg is a LOOKBACK convention, 5.3173 pp span) on a SECOND, UNRELATED, NEVER-DECLARED
  convention: how much of a single day's return a leg is allowed to read.**  Two independent
  conventions now each swamp the only leg on which the standing incumbent's 4b pass rests.

  **(7) RULE 8** (dials fit on warm-up..2016-12-31, 2017-2026 read ONCE).  U56 picks c = 3.0,
  w = 60 -> OOS **18.15% / 1.2224 / -21.21%**, +0.0367 of Sharpe over the anchor at **t +0.68**, and
  **fails 4b_OOS on drawdown**.  B136 picks c = 3.0, w = 252 (item 5).  SMALL's unconstrained
  chooser **picks c = inf — no clip at all**.  Forced to clip, the chooser beats the anchor on OOS
  Sharpe at 2 of 3 panels and at |t| > 2 at **0 of 3**.  Comparands at every cell: RULES v2 live
  (U56 8.62% / 1.2011 / -12.05%) and SPY (15.12% / 0.8844 / -33.72%).

  SURVIVORSHIP (rule 9): U56 / B136 are current-constituent lists and SMALL a current sub-$2B
  screen carried back to 2010, so every absolute level is an upper bound.  Note the bias runs
  AGAINST the clip: a survivor's gap day is more likely to have been a real re-rating, which is one
  reading of (3).  Memo: `research/backtests/2026-09-19_winsorised-momentum-legs_B.MEMO.md`.

## 2026-09-19 — idea 1509 (lane C): should the record's DEVICE-vs-ANCHOR contrasts ALL be re-cut against a TWO-RUNG CAPITAL BLEND? **ANSWERED — NO, NOT AS A RECORD-WIDE RE-CUT. KILL. ONE CARVE-OUT PARKED: THE BLEND IS FREE ON RANK CLAIMS AND NOT ON LEVEL CLAIMS. NO RULES CHANGE PROPOSED.**

  **WHY THIS IDEA.**  1484 compared a turnover-capped book to the min-hold ladder AT MATCHED
  TURNOVER by blending the two BRACKETING RUNGS of the comparand's own dial — a capital split
  between two ladders, an IMPLEMENTABLE book and therefore a fairer anchor than any single rung.
  Every OTHER matched-X contrast in this record was cut against a SINGLE RUNG or an INTERPOLATED
  STATISTIC.  If the blend is the right ruler, ten runs of de-gross twins need re-reading.

  **THE CENSUS (mechanical, gate G13: every classification is a published regex over committed
  bytes).**  Across LEADERBOARD.md, CHANGELOG.md, every committed memo/result and every committed
  script docstring: **1,215 matched-X sentences.  8 (0.7%) name a BLEND.  1,207 (99.3%) name a
  single rung, an interpolated statistic, or nothing.**  Read as a LOWER BOUND on prevalence and
  nothing more — it counts sentences, not distinct claims, and an unstated anchor is counted
  UNSTATED, not miscut.

  **THE RE-CUT.**  45 device books per panel (STOP trailing-equity stop, MAGATE SPY-200d gate,
  VOLTGT vol target; DIAL 1 STRENGTH x DIAL 2 THRESHOLD) on U56 / B136 / SMALL — **135 books, every
  cell published** — each differenced against FOUR rulers (R_NEAR nearest rung, R_STAT interpolated
  statistic, R_BLEND two-rung capital blend, R_BLENDC the blend charged its OWN cross-sleeve
  turnover at 10 bps) on TWO anchor ladders (L_G gross, L_H min-hold) and THREE matching statistics
  (exposure, CAGR, turnover).  **432 contrasts, 337 bracketed, 95 unbracketed and published.**
  All 11 gates pass; G1 replays the committed 2026-09-04 U56 anchor to 3.7e-05.

  **(1) THE PRE-REGISTERED BAR WAS NOT MET.**  Written before any number was read: material only if
  >= 10% of biting contrasts on U56 AND B136 flip the SIGN of dSharpe or change their |t| > 2
  decision between R_NEAR and R_BLEND.  **Observed: 5.9% sign flips, 0.4% decision changes on 238
  bracketed contrasts.**

  **(2) THE MECHANISM, MEASURED RATHER THAN ASSERTED (gate G9).**  A blend differs from a rung ONLY
  IF THE TWO RUNGS HOLD DIFFERENT THINGS.  The gross ladder is a **SCALE** ladder — every rung holds
  the same names at the same relative weights — and on 27 real blends a two-rung gross blend and the
  single gross rung at the SAME realised exposure differ by at most **|dSharpe| 2.8e-05 and |dCAGR|
  6.1e-06**: **0 of 198 sign flips, 0 decision changes** on both L_G combos.  The min-hold ladder is
  a **COMPOSITION** ladder — which is exactly why 1484's blend mattered — and there the blend does
  move things: **11.1%** flips on X_TURN and **17.5%** on X_CAGR, but only **1 and 0** |t| > 2
  decision changes, and 14 of those 18 flips sit on contrasts whose dSharpe is ~0 under BOTH rulers,
  where a sign is not a finding.

  **(3) THE CARVE-OUT WORTH ADOPTING, AND THE ONLY THING HERE THAT CHANGES PRACTICE.**  Sharpe is
  scale-invariant, so rounding a matched-X anchor to the nearest rung is free on RANK claims (max
  |R_NEAR - R_BLEND| dSharpe **0.0004** on L_G).  **CAGR is not.**  The same rounding moves the
  LEVEL by up to **1.06 pp/yr on L_G and 2.01 pp/yr on L_H** — larger than the 4b CAGR-floor margins
  this record publishes (1498's razor-thin U56/INC G = 0.50 cell at **+0.07 pp**; the standing
  candidate at **+1.35 pp**).  **PARKED AS A REPORTING RULE: a committed CAGR- or MaxDD-LEVEL claim
  cut against a NEAREST RUNG should be re-cut against the blend or an exact continuous rung; rank
  claims need not be.**  Filed as idea 1526 to be censused and priced rather than adopted by
  assertion.

  **(4) NO RULER RESCUES ANY DEVICE.**  Of 337 bracketed contrasts, **0 are significantly POSITIVE
  (|t| > 2, dSharpe > 0) under the blend and 25 are significantly NEGATIVE.**  Ten previous runs
  found every drawdown-buying device beaten at matched exposure by a plain de-gross; a fairer,
  implementable anchor does not change that on a single cell.  The best cell any chooser reaches
  (U56 VOLTGT target 0.20, FRAC 0.50; full 14.94% / 1.1956 / -16.05%, OOS 15.76% / 1.2103 /
  -16.05%) sits at **dSharpe +0.042, t = +1.20** against its own matched-exposure blend —
  UNRESOLVED, not a win — and gives up **1.57 pp of OOS CAGR** to the frozen anchor whose Sharpe it
  beats.

  **(5) BOTH KEEP PATHS AND RULE 8.**  **4a 0 of 135** — the eleventh consecutive zero, for the
  reason 1498 made explicit: a de-gross is a near-pure ray and cannot beat the book it scales.
  **4b 50 full / 59 OOS / 50 BOTH**, all on U56 (35) and B136 (15), none on SMALL, and every one
  inherited from the frozen incumbent's standing pass rather than created by a device.  Dials fit on
  warm-up..2016-12-31 ONLY, 2017-2026 read ONCE: `C_RAW`, `C_NEAR`, `C_BLEND` and `C_STAT` pick the
  **IDENTICAL cell on all 3 panels**, so the ruler is **rule-8 unreachable** — the capital arm's
  pre-registered bar (C_BLEND beats both C_NEAR and the do-nothing anchor on OOS Sharpe at every
  panel) fails by construction, and the pick beats the do-nothing frozen anchor on OOS Sharpe at
  1 of 3 panels (U56 1.2103 vs 1.1857; B136 1.0167 vs 1.0180; SMALL 0.3129 vs 0.4398).

  SURVIVORSHIP (rule 9): U56 / B136 are current-constituent lists and SMALL a current sub-$2B screen
  carried back to 2010; every absolute level above is an upper bound.  What this run reads is a
  contrast between two RULERS on the same books on the same days, which the bias cannot manufacture.

  Script: `research/backtests/2026-09-19_two-rung-capital-blend-as-the-matched-X-anchor_C.py`
  (+ `.log.txt`, `.census.csv`, `.census_pivot.csv`, `.grid.csv`, `.recut.csv`, `.algebra.csv`,
  `.walkforward.csv`, `.gates.csv`, `.result.md`).

## 2026-09-19 — idea 1498 (lane B): does the record's 0%-CASH CONVENTION hide a 4b pass? **ANSWERED — IT IS WORTH 0.0–1.1 pp/yr, IT DOES NOT RESCUE THE LIVE BOOK'S CAGR FLOOR, AND IT IS THE ONLY DEVICE ON THIS GRID THAT CLEARS PATH 4a. KEEP-4a CANDIDATE (U56/LIVE, rule-8 clean) AND A STRICT 4b IMPROVEMENT TO THE STANDING CANDIDATE. NO RULES CHANGE ENACTED HERE.**

  **WHY THIS IDEA.**  Every de-gross in this record parks un-invested NAV at EXACTLY 0.00%/yr.  The
  convention was never declared, never tuned and never priced — and today it sits directly on two
  decisions.  Idea 1454 found the live RULES v2 book fails 4b on the **CAGR FLOOR ALONE** (-1.97 pp
  full, -1.22 pp OOS, all four other legs passing) and concluded the fix is G = 1.00, i.e. ABOLISH
  the cash leg because the cash leg earns nothing.  Eight runs (1405, 1413, 1429, 1433, 1436, 1461,
  1468, 1488) each found a drawdown-buying DEVICE beaten at matched exposure by a plain DE-GROSS — a
  contest in which the de-gross carries a 0%-yielding bucket.  Crediting that bucket is not a
  bookkeeping audit: it is an IMPLEMENTABLE RULE CHANGE.

  **THE GRID.**  Un-invested NAV placed in a real **SHY** sleeve that drifts with the book and pays
  10 bps on its OWN turnover.  Two dials: gross **G** {0.25, 0.375, 0.50, 0.625, 0.75, 0.875, 1.00} x
  sleeve fraction **F** {0.00, 0.25, 0.50, 0.75, 1.00}; **F = 0.00 IS the standing convention** and is
  a cell of the grid.  Two frames, reported not tuned: **LIVE** (`rules_v2_weights` band shape) and
  **INC** (the frozen 2026-09-04 incumbent, N = 20, H = 126).  Three panels.  **210 cells, every one
  published.**  All **25 gates pass**, including two cross-script replays: LIVE/U56 (0.75, 0.00)
  reproduces `baseline.compare`'s RULES v2 row to **2.2e-16** and INC/U56 (0.75, 0.00) the committed
  2026-09-04 anchor to **3.7e-05**.  SHY's own profile is published BEFORE anything is credited:
  FULL **1.31%/yr, Sharpe 0.958, MaxDD -5.71%**; IS 0.81%, OOS 1.72%.

  **(1) THE CREDIT IS SMALL, MONOTONE, AND NOT FREE ON DRAWDOWN.**  F = 1.00 minus F = 0.00 is
  **+0.000 .. +1.123 pp/yr of CAGR** (median +0.657), monotone non-decreasing in F at **42 of 42**
  (panel, frame, G) twins, largest at low G where the bucket is largest.  MaxDD is **WORSE** at
  F = 1.00 on **14 of 42** twins, worst **-3.56 pp** on SMALL/LIVE.  SHY is a 1-3y Treasury sleeve,
  not a sweep rate: it is marked to market and it lost 5.71% in 2022.  That is stated, not glossed.

  **(2) IT CANNOT RESCUE THE LIVE BOOK'S 4b CAGR FLOOR, SO 1454's READING STANDS.**  U56/LIVE at the
  live G = 0.75 moves from **-1.97 pp to -1.47 pp** full-sample and **-1.23 pp to -0.54 pp** OOS
  against the floor.  The OOS gap narrows by three quarters and still does not close.  **The
  convention is IMMATERIAL to that decision** — which is itself worth committing, because it retires
  a standing objection to every de-gross contest in the record.

  **(3) PATH 4a — THE FINDING.  68 of 210 CELLS CLEAR 4a FULL, 59 CLEAR 4a FULL *AND* OOS, AND EVERY
  ONE OF THEM CARRIES F > 0: 0 of 42 AT F = 0.00.**  The mechanism is visible in the grid, not
  asserted: at F = 0.00 the LIVE frame's Sharpe is **invariant in G to 4 decimal places**
  (1.20096 .. 1.20116 across all seven rungs) — a de-gross is a pure ray and cannot beat the book it
  scales, which is exactly why 1405 / 1413 / 1436 / 1446 / 1454 / 1461 / 1468 / 1488 returned 4a
  counts of 0/216, 0/90, 0/48, 0/42, 0/42, 0/225, 0/78 and 0/46.  **The cash sleeve is the first
  device in that run to lift Sharpe at all.**  The best cell is the LIVE BOOK WITH NOTHING ELSE
  CHANGED, its idle 25% in SHY: full **9.12% / 1.2675 / -11.48%**, halves **1.278 / 1.264** against
  the live book's **1.228 / 1.181**, MaxDD better than live's -12.05%; OOS **10.14% / 1.3560 /
  -11.48%** against live OOS **9.46% / 1.2769 / -12.05%**; turnover 1.77 -> 2.80x/yr, charged.
  **HONEST LABEL: this is DIVERSIFICATION, not alpha** — CAGR rises only +0.50 pp and vol falls.  It
  beats the live rules because the live rules leave a quarter of NAV in a hole.  It fails 4b on the
  CAGR floor (-1.47 pp), as the live book always has.

  **(4) PATH 4b — A STRICT IMPROVEMENT TO THE STANDING CANDIDATE, PLUS SIX FLIPS.**  INC/U56 at its
  OWN G = 0.75 goes **15.80% -> 16.16%** CAGR, **1.1537 -> 1.1787** Sharpe, **-19.13% -> -18.88%**
  MaxDD — the sole binding 4b leg's margin **+1.1028 -> +1.3544 pp** — and OOS **17.32% -> 17.80% /
  1.1857 -> 1.2148 / -19.13% -> -18.88%**: better on EVERY 4b leg, full and out of sample, for
  +0.18x/yr of turnover.  Separately **6 (panel, frame, G, F) cells flip 4b FULL *and* OOS** where
  their F = 0.00 twin fails: U56/INC G = 0.50 at all four F > 0 (full 10.66% / 1.172 / -12.93%, OOS
  11.70% / 1.207 / -12.93%, but the full-sample CAGR margin is only **+0.07 pp** — razor-thin, stated
  not glossed) and B136/LIVE G = 1.00 at F >= 0.75.  Totals: 4b FULL 34/210, OOS 37/210, BOTH 31/210.

  **(5) RULE 8 — F = 1.00 IS A CORNER, NOT A FITTED VALUE.**  Dials fit on warm-up..2016-12-31 only,
  2017-2026 read ONCE.  `C_SHARPE` picks **F = 1.00 at 6 of 6** panel-frames and `C_CAGR` at **6 of
  6**; **no chooser picks an interior F**.  `C_MEMO` reads F = 0.00 at 6 of 6, but that is a
  **TIE-BREAK ARTEFACT OF THIS RUN'S OWN EXTENSION**: the 2026-09-03 memo's rule names only G, every
  F rung at its chosen G clears its bars identically, so the memo is **SILENT on F** and the 0.00 is
  this script's, not the data's.  7 of 24 chooser picks clear 4b FULL and OOS.

  **(6) THE HONEST LIMIT — REPLICATION.**  B136/INC at (0.75, 1.00) closes **83%** of its DD deficit
  (**-0.5106 -> -0.0880 pp**) and still fails 4b; SMALL clears **0 of 70** 4b cells on either frame,
  and SMALL/LIVE is where the sleeve's drawdown damage is worst.  The 4a result is carried by U56 and
  B136 LIVE (20 + 20 of the 59) and SMALL/LIVE (16).

  **SURVIVORSHIP (rule 9).**  U56 / B136 are current-constituent lists and SMALL a current sub-$2B
  screen carried back to 2010; every absolute level is an upper bound.  What survives is the F-to-F
  CONTRAST on the same names and the same days.  SHY is itself a CONSTITUENT of U56 and B136, so the
  INC frame may already select it on momentum; that is left unchanged and the sleeve is additive.

  **VERDICT.  KEEP-4a CANDIDATE (U56/LIVE, G = 0.75, F = 1.00), rule-8 clean, labelled
  diversification not alpha; KEEP-4b CANDIDATE (U56/INC, G = 0.75, F = 1.00) as a strict improvement
  to the standing 2026-09-04 candidate.  No cell clears both paths (0 of 210).  Nothing enacted:
  PROTOCOL rule 6 reserves enactment for the Sunday review.**  Filed 1490 (charge SPY the candidate's
  own turnover before reading its bars) and 1494 (is realised mean gross a sufficient statistic for
  every device-vs-de-gross loss in the record).
  `research/backtests/2026-09-19_zero-percent-cash-convention_B.py`, memo `.memo.md`, 210 cells in
  `.grid.csv`, choosers in `.walkforward.csv`, gates in `.gates.csv`, transcript in `.log.txt`.

## 2026-09-19 — idea 1461 (lane C): is H = 126 the DD-per-CAGR OPTIMUM, or a GRID ARTEFACT? **ANSWERED — GRID ARTEFACT, BOTH WAYS. KILL (the claim). NO RULES CHANGE. One incidental KEEP-4b candidate PARKED, not recommended.**

  **WHY THIS IDEA.**  1444's finding #2 said the beta band's exchange rate (pp of MaxDD bought per pp
  of CAGR given up, against each rung's own c = 0 anchor) PEAKS at H = 126 on U56 (-0.901) and B136
  (-1.047) — the frozen incumbent's own min-hold — and concluded "the incumbent is already standing on
  the best rung".  That peak was read off a SIX-rung ladder {21, 63, 126, 189, 252, 378} whose nearest
  neighbours to 126 are a factor of 2 and 1.5 away, from a point estimate with NO standard error.

  **THE GRID.**  The same rule, same frozen incumbent (N = 20, gross 0.75, weekly, 10 bps, t+1), with
  the ladder REFINED to H {100, 112, 126, 142, 160} (126 interior, ~+/-12% and ~+/-27%) and c FROZEN at
  0.50; the second dial is the bootstrap block length L {21, 63, 126}, all three reported.  225 cells on
  U56 / B136 / SMALL, every one published.  Gate **G2 is a cross-script replay of the statistic under
  test**: re-forming 1444's coarse ladder here reproduces its six published U56 slopes and B136's H =
  126 slope to **4.2e-4**.  All 20 gates pass.

  **(1) THE PEAK MOVED — 126 IS THE ARGMIN ON NO PANEL.**  U56 reads -0.702 / -0.472 / **-0.901** /
  **-1.391** / -1.128 at H = 100 / 112 / 126 / 142 / 160, so the argmin is **142** and it is 54% steeper
  than 126; B136 reads +0.221 / -0.280 / -1.047 / -0.066 / **-1.050**, argmin **160**; SMALL's argmin is
  **160**.  The coarse ladder did not find an optimum, it found the best of six far-apart rungs.

  **(2) AND IT DISSOLVED — THE SLOPE CANNOT SEPARATE ANY RUNG FROM ANY OTHER.**  Under a paired
  circular-block bootstrap (400 reps; ONE shared block-start matrix per panel x L, so every rung-to-rung
  gap is paired), the slope's own SE is **0.61 .. 8.96** against a total five-rung spread of **0.92**
  (U56) and **1.27** (B136).  The 126-vs-best-rival gap reads **|t| 0.14..0.20** on U56 and **|t|
  0.01..0.09** on B136 at EVERY block length; P(argmin = 126) is **0.038..0.080** (U56) and
  **0.330..0.338** (B136); the NEW argmin is no better resolved (P(argmin = 142) 0.55..0.75 on U56,
  P(argmin = 160) 0.50..0.52 on B136).  All three pre-registered legs fail on both large-cap panels at
  all three block lengths.  **The exchange rate is a ratio of two sub-2-pp differences and carries no
  resolving power at this sample length.**

  **(3) THE LOOKBACK CONTROL.**  H = 126 also equals the beta lookback B and the composite's middle
  momentum leg, so the refined ladder was re-run with B decoupled to 252 (published, never selected on).
  U56's argmin STAYS at 142; B136's moves BACK to 126; SMALL's moves to 112.  A location that relocates
  when a frozen, non-selected lookback changes is noise, not a property of the min-hold.

  **CAPITAL AND RULE 8.**  4a **0 of 225**; 4b FULL and OOS **44 of 225** (U56 36, B136 8, SMALL 0).  H
  chosen on warm-up..2016-12-31 at c = 0.50 and 2017-2026 read ONCE under two pre-registered choosers
  (argmax IS Sharpe; steepest IS slope): neither picks H = 126 on any panel (**0 of 6**).  Both pick
  **H = 142** on U56 — full 15.47% / 1.2103 / -19.47%, halves 1.302 / 1.158, OOS **17.25% / 1.2350 /
  -19.47%** against the -20.23% cap (+0.76 pp) and the 10.68% floor (+6.57 pp), turnover 3.42x/yr.  It
  clears path **4b full sample AND out of sample** and is rule-8 clean, and it is still **PARKED, not
  recommended**: against the frozen incumbent (OOS 17.32% / 1.1857 / -19.13%) it buys **+0.049 of OOS
  Sharpe at t = +0.55** and **-0.07 pp of OOS CAGR** while NARROWING the binding 4b DD margin from +1.10
  to +0.76 pp and raising turnover from 2.87x/yr; its own c = 0 anchor FAILS 4b (-1.15 pp), so the pass
  is bought by exactly the band device 1436/1444 closed.  B136's picks fail 4b on drawdown (-26.6% and
  -27.0% against a -20.2% cap); SMALL fails every leg.  SPY OOS 15.26% / 0.8738 / -33.72%; live RULES v2
  OOS 9.46% / 1.2769 / -12.05%.

  **SURVIVORSHIP (rule 9).**  U56 / B136 are current-constituent lists and SMALL a current sub-$2B
  screen carried back to 2010; every absolute level is an upper bound and every 4b pass an optimistic
  one.  What this run reads is a CONTRAST between books over the same names on the same days.

  **CONSEQUENCE FOR THE RECORD.**  A "best rung" read off a ladder whose neighbours are a factor of 2
  apart, with no SE on the statistic, is not evidence — including 1444's own.  Filed 1468 (does the
  slope resolve on ANY device family), 1472 (de-gross twin for U56 H = 142) and 1476 (census and
  re-pricing of every committed best-rung claim).  `research/backtests/2026-09-19_is-H126-the-DD-per-CAGR-optimum_C.py`, memo `.memo.md`, 225 cells in `.grid.csv`, the bootstrap in `.bootstrap.csv` / `.peak.csv`.

## 2026-09-19 — idea 1454 (lane B): does the 2026-09-03 RECOMMENDATION memo's OWN G-CHOOSING RULE survive PROTOCOL rule 8? **ANSWERED — IT FIRES ITS OWN FALLBACK AND THAT IS WHY THE LIVE BOOK FAILS 4b. KEEP-4b CANDIDATE (U56, rule-8 clean), 4a FAIL 0 of 42, NO RULES CHANGE ENACTED HERE.**

  **WHY THIS IDEA.**  Five consecutive runs today (1405 trailing equity stop 216 of 216 cells, 1413
  breadth throttle 90 of 90, 1433 intra-book inverse-vol on CAGR, 1429 beta-keyed floor-and-cap, 1436
  its beta-matched twin 48 of 48) each found a DRAWDOWN-BUYING DEVICE beaten, at matched exposure, by a
  plain DE-GROSS of the same anchor.  The record's repeated WINNER is therefore the gross scalar itself
  — and it had never been scored as a candidate, nor had the rule that SET the live G = 0.75 ever been
  read out of sample.  That rule is written down, pre-registered, in the recommendation memo:
  *"gross G chosen ONLY from idea 28's three reported values by the pre-stated rule 'smallest G whose
  MaxDD <= 60% of SPY's and CAGR >= 70% of SPY's'; if none, keep 75%"*.

  **THE GRID.**  The LIVE RULES v2 shape unchanged (`baseline.rules_v2_weights`: 200d +/-3% hysteresis
  band, hold every IN name, de-gross to cash, never re-spread) with its ONE sizing number walked over
  G {0.25, 0.375, 0.50, 0.625, 0.75, 0.875, 1.00} x cadence {W, M}: 14 cells per panel on U56 / B136 /
  SMALL485, **42 cells, every one published**.  Two tuned parameters exactly.  No leverage — the ladder
  stops at G = 1.00 (PROTOCOL rule 2).  G = 0.75 & W IS the live book and reproduces
  `baseline.compare`'s baseline row to **1e-9** on Sharpe and MaxDD (gate G3).

  **(1) THE LIVE BOOK IS UNDER-GROSSED, AND ON ONE LEG ONLY.**  At the live weekly cadence on U56,
  **G = 1.00 clears all five 4b legs FULL-SAMPLE AND OUT-OF-SAMPLE**: CAGR **11.53%** against the
  10.59% floor (**+0.94 pp**), Sharpe **1.201**, MaxDD **-15.91%** against the -20.23% cap (**+4.32
  pp**), halves 1.228 / 1.180 against SPY's 0.957 / 0.825; OOS **12.67% / 1.276 / -15.91%** against
  SPY OOS 15.26% / 0.874 / -33.72%.  Turnover 2.35x/yr.  The live G = 0.75 fails 4b on the **CAGR floor
  alone** — the single bar RULES.md itself names — by **-1.97 pp full-sample and -1.22 pp OOS**, with
  all four other legs already passing.  The CAGR floor binds at every rung G <= 0.75 on both cadences;
  the DD cap binds NOWHERE on U56 up to G = 1.00.

  **(2) RULE 8 IS CLEAN AND THE MEMO GOT ITS OWN RULE BACKWARDS.**  Fit on 2009-2016 alone and read
  once on 2017-2026, **both** IS-only choosers pick G = 1.00 on U56; the licensable G set is
  **{0.875, 1.00}** at the 2017 split, **{0.875, 1.00}** at 2015 and **{1.00}** at 2019.  The memo's
  literal rule, applied to IS at weekly, finds that NO rung clears the IS CAGR floor (best 10.16% at
  G = 1.00 vs 10.47%), so **its own fallback fires and keeps 0.75** — that is how the live book came to
  sit below its own bar.  On the full sample the same rule picks **1.00**.  Honest label: C_BUDGET is
  **DEGENERATE** — the IS DD cap binds at **0 of 7 rungs on all three panels**, so "spend the risk
  budget" reduces to "take the ladder's ceiling", and the ceiling is 1.00 only because PROTOCOL forbids
  leverage.  The recommendation keeps the live cadence W; the joint chooser's M pick (11.90% / 1.173 /
  -18.81%, a DD margin of only +1.42 pp) is reported and NOT recommended.

  **(3) IT IS A RISK-BUDGET FINDING, NOT AN ALPHA ONE.**  Sharpe is **1.201 at all seven weekly rungs**
  on U56, invariant to 3 dp, and turnover per unit of gross is constant to cv <= 1.1e-2 (gate G2) with
  MaxDD monotone in G at 6 of 6 panel-cadences (gate G1).  G buys nothing risk-adjusted; it moves the
  book along its own ray.  **4a fails at 0 of 42 cells** — more gross is strictly deeper MaxDD at an
  unchanged Sharpe, so this book never beats the book.  4b-only candidate.

  **(4) COST-ROBUST TO 25 bps; THE 0.75 MISS IS NOT FRICTION.**  4b holds FULL and OOS at 0, 5, 10 and
  25 bps and fails FULL at 50 bps by 0.10 pp (10.49% vs 10.59%) while OOS still passes.  The live 0.75
  fails the CAGR leg at **every** rung **including 0 bps** (8.81% vs 10.59%), so its failure is
  exposure, not cost.  Caveat retained (idea 1063): the ladder is one-sided — SPY pays no turnover, so
  the floor and cap it sets never move.

  **(5) REPLICATION FAILS OFF THE PROTOCOL PANEL — the honest limit.**  **0 of 14** cells clear the two
  level legs on B136 and **0 of 14** on SMALL485, at all three splits.  B136's G = 1.00 W passes 4b
  full-sample but misses the OOS CAGR floor by **0.21 pp** (10.47% vs 10.68%); B136 at G = 1.00 M
  **BREACHES** the OOS DD cap (-20.50% vs -20.23%), as does SMALL485 at G = 1.00 M (-21.66%).  U56 is a
  current-constituent list (idea 54) and a full-gross long book is the most exposed to that bias.

  **(6) THE CAP ITSELF MOVED, AND THE LUCK RAN THE RIGHT WAY.**  SPY's MaxDD is -22.06% on IS and
  -33.72% on OOS, so the 4b DD cap loosened **-13.24% -> -20.23% (+6.99 pp)** between the window the G
  was chosen in and the window it was judged in.  Budgeting against the IS cap was conservative by
  luck here; a shallower SPY decline would tighten it.  This is filed as idea 1450 for a proper pricing.

  **VERDICT.  KEEP-4b CANDIDATE on U56, rule-8 clean, with the §5 replication limit and the §2
  degeneracy stated.  4a FAIL.  Nothing enacted: PROTOCOL rule 6 reserves enactment for the Sunday
  review, and RULES.md / bot.py / scan.py / baseline.py are untouched by this run.**  Exact one-number
  RULES wording (clause 4 `0.75 / N` -> `1.00 / N`, clause 5's reset line likewise, everything else
  unchanged) is in `research/backtests/2026-09-19_memo-G-chooser-under-rule-8_B.memo.md`, together with
  the G = 0.875 fallback if the review declines the survivorship exposure.
## 2026-09-19 — idea 1436 (lane cloud): is the BETA BAND's 4b DD GAIN anything more than a BETA-MATCHED EXPOSURE DIAL? **ANSWERED NO — KILL (capital), NO NEW BOOK, NO RULES CHANGE.**

  Idea 1429's PARK memo named the repair and did not run it ("a BETA-MATCHED twin").  This run
  is that twin, with 1429's committed script IMPORTED rather than re-typed: G1a replays the
  committed U56 anchor to 3.7e-05 of Sharpe, G1b replays its +1.1028 pp DD margin exactly.
  Each of 1429's 60 cells gets two controls holding the IDENTICAL names on the IDENTICAL rows,
  solved SEGMENT BY SEGMENT to the cell's OWN realised NAV beta b* = sum_i w_i beta_i:
  **TWIN-G** (beta-matched DE-GROSS: equal weights, gross scaled to g = b*/mean(beta); ZERO bits
  of the ranking, no leverage) and **TWIN-B** (beta-matched BARBELL: two-point weights at FIXED
  gross 0.75 hitting the same b*; ONE bit of the ranking).  At c = 0 both are bit-identical to
  the incumbent to 4.5e-17 by algebra (G3); beta match exact to 8.9e-16 (G2); TWIN-B's gross
  pinned to 3.3e-16 (G7a) and clips 0 of 56,520 segments, TWIN-G clips 2,895 (5.12%).

  **(1) THE PURE EXPOSURE DIAL WINS THE DRAWDOWN LEG 48 OF 48.**  Given the cell's own beta and
  nothing else, a plain de-gross of the anchor draws down LESS at EVERY biting cell on all three
  panels.  U56: cell DD margin **+1.8329 .. +4.4039 pp** vs TWIN-G's **+2.0664 .. +7.0996 pp** —
  the band recovers at most 62% of what its own beta reduction is worth, while deploying MORE
  capital (mean gross 0.7500 vs 0.4538–0.6981) and trading MORE (3.02–9.89 vs 2.24–3.61
  turnover/yr).  The band is the trailing stop (1405), the breadth throttle (1413) and the
  convention blend (1423) again — an exposure dial in costume — only more expensive: it pins
  DOLLAR gross and spends the cut in BETA, which the 4b DD cap cannot tell apart.

  **(2) ONE BIT OF BETA REPRODUCES ALL n BITS.**  TWIN-B beats the CELL on Sharpe at 16 of 16
  U56 cells (1.0784–1.1666 vs 1.0585–1.1568) and on OOS Sharpe at 16 of 16 (1.1690–1.2303 vs
  1.1222–1.2040), matches it on drawdown (cell ahead 10 of 16), and **|t| on MaxDD is 0 of 16 on
  U56 and 0 of 16 on B136**.  The fine n-way ranking is worth nothing over a median split.

  **(3) THE BAR AND RULE 8.**  Pre-registered before any number was read: (i) cell's DD margin
  beats BOTH twins at a majority of the 16 biting cells — **0 of 16**; (ii) |t| > 2 on MaxDD vs
  TWIN-B at >= 1 cell — **0 of 16**; (iii) 4b full and OOS there — 16/16.  Rule 8 (argmax IS
  Sharpe, 2017–2026 read ONCE, the same chooser over all three arms) picks **c = 0, the frozen
  anchor, for CELL, TWIN-G and TWIN-B alike on U56 AND B136** (OOS 17.32% / 1.1857 / -19.13% vs
  SPY 15.26% / 0.8738 / -33.72%).  **4a 0 of 180.**

  **(4) WHAT SURVIVES, AND WHERE IT CANNOT BE SPENT.**  The band's only non-beta content is on
  SMALL, on RETURN not drawdown: at matched beta the cell beats TWIN-G on Sharpe by +0.0517 ..
  +0.2340 with |t| > 2 at 12 of 16 — on the one panel whose 4b DD leg fails by 16.28 pp.  Beta
  information resolves only where it cannot carry capital, exactly as 1433's vol information did.
  **The beta family is closed on the drawdown leg.**  Result:
  `research/backtests/2026-09-19_beta-matched-twin-for-the-beta-band_cloud.result.md`.
  Survivorship (rule 9): U56/B136 current-constituent lists, SMALL a current sub-$2B screen back
  to 2010; every level an upper bound, though a contrast between three weightings of the SAME
  names on the SAME days at the SAME beta is not something the bias can manufacture.

## 2026-09-19 — idea 704 (lane cloud): price the CAP CHANNEL against a MATCHED-VOL control. **ANSWERED — ALL OF IT SURVIVES AND THE CONFOUND RUNS THE WRONG WAY. KILL (capital), NO NEW BOOK.**

  Idea 694 published CAP = rho(q, OOS Sharpe) = -0.7709 at matched width and matched selection
  ratio and the queue asked whether it is a name-vol story in disguise.  Three arms at k = 90,
  r in {0.05, 0.10, 0.25, 0.50}, every definition imported from ideas 276/286/525.  **ARM CAP**
  reproduces the channel on this run's own seed: **CAP -0.8009**, mean OOS Sharpe 0.8973 ->
  0.4150, **span -0.4823**.  **ARM VOLTWIN** draws each panel's twin from the POOLED universe
  with ORIGIN IGNORED, hill-climbed to the same mean IS name vol within TOL in {0.02, 0.05}
  (0 of 640 twins outside TOL).  **ARM VOLRUNG** pins the cap mix exactly and splits each pool
  into its LOW and HIGH IS-vol half.  Every matching vol is measured on warm-up..2016-12-31 only
  (G6), which narrows the pools to SMALL 478 / BSTK 97 and the width to k = 90 — stated, and it
  removes the post-2016 listings, making SMALL older and working AGAINST a small-cap penalty.

  **(1) THE MATCHED-VOL CONTROL CARRIES NONE OF IT.**  Over the same realised vol range (twins
  0.276–0.434 vs the cap arm's 0.259–0.430), the twin ladder's OOS Sharpe spans +0.0220 /
  +0.0672 / +0.0098 / -0.0377 (TOL 0.02) and -0.0393 / +0.1302 / +0.1419 / +0.0816 (TOL 0.05)
  against the cap arm's -0.4542 / -0.2919 / -0.4714 / -0.7116.  **SURVIVAL = -0.1278.**  The
  twins' realised cap share is 0.644–0.900 (mean 0.785) because the admissible pool is 83% small
  — published, because it is why this arm moves cap and vol together and lands flat.

  **(2) AT PINNED CAP MIX, HIGH VOL WINS 12 OF 12.**  q=0.50: 0.2884 -> 0.7875; q=0.75: 0.2159 ->
  0.7142; q=1.00: 0.0356 -> 0.5387; every (q, r) span positive, +0.3233 .. +0.6783.  (The rho
  column reads +0.8729 at all 12 cells because a two-level Spearman with 4+4 draws and perfect
  separation saturates there; the SPAN is the statistic.)

  **(3) THE POOLED DECOMPOSITION.**  On ARM CAP alone q and name vol are +0.9694 collinear —
  stated in the script header, not discovered after.  Pooling the three arms drops it to +0.5715
  and the standardised rank OLS reads **beta_q -0.4603 / -0.5304 / -0.7604 / -0.8839 against
  beta_vol +0.3973 / +0.5142 / +0.5024 / +0.4477** (pooled partial rho q -0.5446, vol +0.4274).
  **Cap is a PENALTY, vol is a PREMIUM, they are positively correlated and partly CANCEL — so
  694's raw ladder UNDERSTATES the pure cap penalty.**  The pre-registered bar calls MIXED and
  the run prints both numbers rather than rounding to a verdict.

  **(4) CAPITAL.**  4a **0 of 576**, 4b 20 of 576 (16 on ARM CAP all at q <= 0.25, 4 on VOLRUNG,
  **0 of 320 on VOLTWIN**).  Rule 8: CAP picks q=0.00 r=0.10 -> OOS 12.24% / 0.7697 / -21.68%;
  VOLTWIN picks q=0.00 r=0.50 -> 4.10% / 0.4591 / -16.95%; VOLTWIN@0.05 -> 3.45% / 0.3888 /
  -18.81%.  **0 of 3 arms beat SPY OOS (15.26% / 0.8737 / -33.72%), so nothing here is a book.**
  NAMED FOLLOW-UP, not filed: the +0.50 OOS-Sharpe HIGH-minus-LOW name-vol premium at PINNED cap
  mix is a channel the record has priced only as a confound and never as a book.  Result:
  `research/backtests/2026-09-19_cap-channel-vs-matched-vol-control_cloud.result.md`.

## 2026-09-19 — idea 1429 (lane C): does a BETA-KEYED FLOOR-AND-CAP REDISTRIBUTION buy the BINDING 4b DD LEG at IDENTICAL NAMES and IDENTICAL GROSS? **ANSWERED YES ON THE LEG AND MORE CHEAPLY THAN 1433 — BUT PARK (capital), NO NEW BOOK, NO RULES CHANGE.**

  The queue's premise (1429) is exact: the 2026-09-04 incumbent is EQUAL WEIGHT, so a max-weight
  CAP alone is inert — a cap can only bite if something is redistributed INTO a floor.  This run
  prices that mirror.  Rank the n held names by their own trailing beta to SPY (ascending) and
  set `z = 1 - 2(rank - 0.5)/n` (sum EXACTLY 0), `w = (G/n)(1 + c*z)`, G = 0.75: LOWEST beta
  takes the cap `(G/n)(1 + c(1-1/n))`, HIGHEST takes the floor.  c = 0 IS the frozen incumbent.

  **THE GRID.** C {0, 0.25, 0.50, 0.75, 1.00} x B {20, 63, 126, 252} beta lookback.  20 cells per
  panel, 60 in all, every one published.  Selection is built ONCE per panel before any dial, so
  every cell holds the IDENTICAL names on the IDENTICAL rows (G8); every cell's realised mean
  gross matches the anchor's to **< 1e-12** and every rebalance sums to 0.75 exactly (G7/G7b);
  the realised max/min weight equals the analytic cap/floor at every rebalance (G11).  Because
  the multiset is a function of (n, c) alone, every cell at the same c has an IDENTICAL
  effective-N and Herfindahl path — the ONLY thing any dial moves is WHICH NAME GETS WHICH SLOT.

  **(1) IT BUYS THE BINDING LEG, AND IT KEEPS THE CAGR FLOOR 1433 BROKE.**  U56's 4b DD margin
  widens from the anchor's **+1.1028 pp to +1.8329 .. +4.4039 pp at 16 of 16 biting cells**
  (MaxDD -19.13% -> **-15.83%**), at identical gross, identical names and identical name count.
  Unlike 1433's inverse-vol mirror, whose four widest cells LOST 4b full-sample on the CAGR
  floor, **4b here passes FULL AND OOS at 16 of 16** with the floor intact (CAGR margin +1.4276
  .. +4.3802 pp).  **B136 crosses the leg outright: the anchor FAILS at -0.5106 pp, the band
  passes at 15 of 16 full and 14 of 16 OOS (+0.3821 .. +2.2726 pp).**  Across all panels: 4b full
  35 of 60, 4b OOS 34, both 34.

  **(2) THE ORDERING IS REAL IN SIGN, UNRESOLVED IN SIZE WHERE THE MONEY IS.**  Two exact
  controls.  The **ANTI-BETA MIRROR** runs the same band at -c (highest beta takes the cap):
  identical multiset, identical gross, identical names, identical effective-N path, EXACTLY
  reversed ordering — the sharpest available null.  The beta ordering draws down LESS than its
  mirror at **48 of 48 cells** (+1.633 .. +12.951 pp of MaxDD).  The **RANK-PERMUTATION TWIN**
  (K = 12 seeded shuffles of the cell's own multiset) is beaten on Sharpe at 47 of 48 and on
  MaxDD at 44 of 48; median percentile 1.000 on both.  But a paired 63-day circular-block
  bootstrap (400 reps, seed 20260919, identical block starts) puts **|t| > 2 on MaxDD at 0 of 48
  against the mirror and 1 of 48 against the shuffle**.  On Sharpe it resolves at 2 of 16 on U56
  (t +1.27 .. +2.25), 7 of 16 on B136 and **16 of 16 on SMALL** (t +2.44 .. +3.98) — and SMALL
  fails 4b at every cell (DD margin -15.41 .. -9.92 pp).  Beta information resolves only on the
  panel that cannot carry capital, exactly as 1433's vol information did.

  **(3) THE PRE-REGISTERED BAR FAILS ON LEG (iii) AND RULE 8 LEAVES THE ANCHOR.**  Bar stated in
  the script header before any number was read: capital only if U56 (i) DD margin > +1.1028 pp
  AND (ii) 4b passes FULL and OOS AND (iii) |t| vs its own twin > 2.  **(i) 16/16, (ii) 16/16,
  (iii) 2 of 16 — ALL THREE 2 of 16**, and neither cell was named in advance.  Rule 8 (argmax IS
  Sharpe on warm-up..2016-12-31, 2017-2026 read ONCE) picks **c = 0, the frozen anchor, on U56
  AND on B136**; on SMALL it picks (1.00, 126) — OOS Sharpe 0.6385 vs the anchor's 0.4398
  (+0.1987, t +2.25), OOS MaxDD -31.38% vs -36.51% — on a book that fails every 4b leg.
  **4a 0 of 60.**

  **(4) THE CAVEAT THAT KEEPS IT OUT OF THE BOOK.**  The rule shuts the DOLLAR exposure channel
  to machine precision and OPENS the BETA one.  Realised book beta falls **1.0162 -> 0.6516 ..
  0.9330**, CAGR falls MONOTONICALLY in c (-0.84 .. -3.79 pp vs the anchor) and turnover rises
  2.87 -> 3.02 .. 9.89 (drag 30.2 .. 98.9 bp/yr).  A plain rotation down the security market line
  predicts every headline above; the 48/48 mirror sign says the direction is not free, but
  nothing here resolves that it is more than a beta dial.  The repair is named, not run: a
  BETA-MATCHED twin, and a rule-8 chooser keyed on the 4b DD margin rather than on Sharpe.

  **VERDICT: PARK (capital).**  No new book, no RULES change, RULES.md / scan.py / bot.py /
  baseline.py untouched.  Memo:
  `research/backtests/2026-09-19_beta-keyed-floor-and-cap_C.memo.md`.
  Survivorship (rule 9): U56/B136 are current-constituent lists, SMALL a current sub-$2B screen
  carried back to 2010; every level is an upper bound and every 4b pass an optimistic one — what
  the run reads is a CONTRAST between two orderings of the SAME weights over the SAME names on
  the SAME days, which the bias cannot manufacture.

## 2026-09-19 — idea 1433 (lane B): does INTRA-BOOK INVERSE-VOL SIZING buy the BINDING 4b DD LEG at IDENTICAL NAMES and IDENTICAL GROSS? **ANSWERED YES ON THE LEG AND NO ON THE MONEY. KILL (capital), NO NEW BOOK, NO RULES CHANGE — with the month's first non-exposure DD finding logged as a caveat.**

  The standing 2026-09-04 KEEP-4b incumbent (U56, N = 20, H = 126, gross 0.75, weekly Fri-decide /
  Mon-trade, 10 bps, t+1) passes 4b on ONE leg by +1.1028 pp of MaxDD. Every attack on that leg
  this month — a trailing equity stop (1405), a breadth throttle (1413), a convention ensemble
  (1423) — died the SAME death: each shallowed drawdown by HOLDING LESS STOCK or HOLDING MORE
  NAMES, and each failed against its own exposure-matched twin. This run closes that channel BY
  CONSTRUCTION and asks whether anything is left.

  **THE GRID.** P {0, 0.5, 1.0, 1.5, 2.0} x L {20, 63, 126, 252}: size the SAME held names by
  `(1/vol_L)^p` at the SAME gross. P = 0 IS the frozen incumbent, present at every L. 20 cells
  per panel, 60 in all, every one published. Selection is built ONCE per panel before any dial,
  so all 60 cells hold the IDENTICAL names on the IDENTICAL rows (G8), and every cell's realised
  mean gross matches the anchor's to **1.11e-16** (G7). The vol floor is not a third dial: it is
  inherited from the live `baseline.score` clip at 0.08 annualised.

  **(1) THE BINDING LEG MOVES, AND IT IS NOT AN EXPOSURE DIAL.** U56's 4b DD margin widens from
  the anchor's **+1.1028 pp to +2.2897 .. +5.6306 pp at 16 of 16 biting cells** — MaxDD -19.13%
  -> **-14.60%** at p = 2.0 / L = 20, +4.53 pp of headroom — at identical gross, identical names
  and identical name count. B136's margin crosses from **-0.5106 pp (FAIL) to +1.3995 .. +2.4541
  pp (PASS) at 16 of 16**. This is the first result this month to move that leg without touching
  exposure.

  **(2) IT IS AN EXCHANGE, NOT A FREE LUNCH.** Every U56 biting cell is WORSE than the anchor on
  full-sample Sharpe (**-0.1944 .. -0.0225**) and on CAGR (**-6.41 .. -1.80 pp**; 15.80% ->
  9.39-14.00%). Turnover runs 2.91-9.07 against 2.87 (drag 29.1-90.7 vs 28.7 bp/yr) and effective
  N falls 18.69 -> 10.30-17.78. At **p = 2.0 the 4b CAGR FLOOR BREAKS** (margin -0.46 .. -1.19 pp),
  so the four cells with the WIDEST DD margins in the whole run LOSE 4b full-sample. 4b full 12 /
  12 / 0 of 16 and 4b OOS 16 / 14 / 0 on U56 / B136 / SMALL. **4a 0 of 60.**

  **(3) THE ORDERING IS REAL IN SIGN, UNRESOLVED IN SIZE WHERE THE MONEY IS.** Every cell is
  scored against its OWN **WEIGHT-PERMUTATION TWIN**: the cell's own weight multiset re-assigned
  to the same held names in seeded random order (K = 12), matching gross, names, name count AND
  the entire weight distribution — identical effective-N path to 2.8e-14 (G9) — so the ONLY
  difference is WHICH name gets WHICH weight. The real ordering wins at **48 of 48 cells
  full-sample and 48 of 48 OOS**, a systematic sign. But paired 63-day circular-block bootstrap
  (400 reps, seed 20260919, identical block starts) puts **|t| > 2 at 0 of 16 on U56** (t +0.57 ..
  +1.97), **0 of 16 on B136** (+0.47 .. +1.18) and **12 of 16 on SMALL** (+1.48 .. +2.85). Vol
  information resolves only where cross-sectional vol dispersion is large — and that panel fails
  4b at every cell (DD margin -9.94 .. -15.47 pp, OOS MaxDD -30.17% .. -35.70%).

  **(4) THE PRE-REGISTERED BAR, AND RULE 8.** The bar was stated in the script header before any
  number was read: capital only if U56 (i) DD margin > the anchor's +1.1028 pp AND (ii) |t| vs its
  own permutation twin > 2. **(i) 16 of 16. (ii) 0 of 16. BOTH: 0 of 16.** Rule 8 — (p, L) by
  argmax IS Sharpe on warm-up..2016-12-31, 2017-2026 read ONCE — **picks p = 0.0, the frozen
  incumbent itself, on BOTH U56 and B136**, so the OOS book is bit-identical to the anchor
  (17.32% / 1.1857 / -19.13%, dSharpe +0.0000) against SPY OOS 15.26% / 0.8738 / -33.72%. SMALL
  picks p = 2.0 / L = 20 for +0.1182 of OOS Sharpe (t +1.40, unresolved) on a book that fails all
  four OOS 4b legs at MaxDD -32.61%. **A Sharpe chooser declines this trade, so no deployable rule
  reaches it.**

  **WHAT THE RECORD SHOULD CARRY FORWARD.** The 4b DD cap is NOT un-buyable at fixed exposure —
  1405/1413/1423 established only that it is un-buyable with exposure. It is buyable with CAGR, at
  roughly **0.4-0.8 pp of CAGR per pp of DD headroom** on U56, and the exchange is Sharpe-negative
  in sample at every rung tested. That is a caveat for any future run tempted to read the
  incumbent's +1.1028 pp as a structural floor.

  **GATES** all PASS: G0 >= 10y (16.68); G1 cross-script replay of the committed U56 anchor
  (|dSharpe| 3.7e-05); G2 P=0 bit-identical across all four L (0.0); G3 P=0 permutation twin
  bit-identical to the P=0 cell (0.0); G4 60 of 60 cells published; G5 exactly two tuned
  parameters; G6 no chooser row on or after 2017-01-01; G7 mean gross equals the anchor's to
  1.11e-16 and G7b no leverage (max weight sum 0.750000); G8 selection untouched; G9 twin
  effective-N match 2.8e-14; G10 bit-identical recompute (0.0). Survivorship stated (rule 9):
  U56 / B136 are current-constituent lists and SMALL a current sub-$2B screen, so every absolute
  level is an upper bound; what this run reads is a CONTRAST between two sizings of the SAME names
  on the SAME days. RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py NOT modified.
  Script: `research/backtests/2026-09-19_intra-book-inverse-vol-sizing_B.py`.

## 2026-09-19 — idea 1182 (lane C): how many committed LADDER claims name a RUNG the record has measured FEWER THAN TEN TIMES? **ANSWERED: 204 of 4,614 (0.0442) — AND THE RESTRICTION BUYS NOTHING. KILL (capital), no new book.**

  Idea 1174 built the measurement histogram for the hold axis H and found the record's "finer"
  hold evidence is two runs wearing seven rung labels. This run does the same for the four axes
  that actually price a book — N, GROSS, COST, CADENCE — and then turns the answer into a
  capital decision instead of leaving it as bookkeeping.

  **THE CENSUS.** 35,216 committed text units (LEADERBOARD.md + CHANGELOG.md + 1,204
  `*.result.md` / `*.memo.md`, 15,178,975 bytes off HEAD). A MEASUREMENT is a DISTINCT RUN naming
  a rung through that axis's own token; a CLAIM is a unit with the token, >= 1 named rung AND a
  shape verb. At the queue's single-digit bar T = 10: **N 42 of 776 (0.0541), GROSS 23 of 966
  (0.0238), COST 139 of 2,078 (0.0669), CADENCE 0 of 794 (0.0000)** — 204 of 4,614 overall. Every
  bar published, none tuned: T = 3 / 5 / 10 / 20 / 50 gives 107 / 149 / 204 / 337 / 484.
  **The H axis's alarm does not generalise.**

  **WHY NOT — AND THE DEFECT THAT IS REALLY THERE.** The thin tail is small because the mass sits
  on ONE rung per axis: **N = 20 holds 0.4568 of all run-mass** (51 rungs, HHI 0.2384, 10 rungs
  cover 90%); **GROSS = 0.75 holds 0.4467**, top two 0.7016; **COST = 10 bps holds 0.4236**, top
  two 0.6406; **CADENCE = W holds 0.5473**, top two 0.7903. A committed ladder claim is rarely
  standing on a rung nobody measured — it is usually standing on the rung everybody measured, and
  no thinness bar can detect that. **The record's axis defect is CONCENTRATION, not thinness.**

  **THE CAPITAL LEG.** 126 real books — N {5,10,15,20,25,30,40} x GROSS {0.35,0.45,0.55,0.65,
  0.75,1.00} on the frozen 2026-09-04 incumbent frame (H = 126, MAXVOL 0.60, MA gate ON, weekly,
  10 bps, t+1), three panels, every cell published with both KEEP paths. **4a 0 of 126. 4b 28 of
  126 full-sample, 20 OOS, 19 both.** The U56 anchor replays to |dSharpe| 3.7e-05.

  **RULE 8 KILLS THE PREMISE.** (N, GROSS) by argmax IS Sharpe on warm-up..2016-12-31, 2017-2026
  read ONCE, in two variants: C_ALL over all 42 cells, C_THICK restricted to cells both of whose
  rungs the census measures >= T times, at every T. **14 of 15 (panel x bar) arms pick the
  IDENTICAL cell**; mean OOS dSharpe **+0.0052**. The one differing arm (SMALL, T = 50, menu 12 of
  42) gains +0.0782 OOS Sharpe on a book with OOS MaxDD **-49.88%** that fails every 4b leg, and
  against 40 SIZE-MATCHED RANDOM menus sits at the 0.9625 mid-rank percentile — 1 of 9 arms above
  the 95th at a draw resolution of 0.025; median arm 0.425, mean tied share 0.575 (a random menu
  of the same size usually picks the SAME cell). **"The record has barely measured this rung"
  carries no out-of-sample information about the cell.**

  **DOCUMENTED CAVEAT (not a KEEP).** U56 **N15 g0.75** passes 4b full-sample AND OOS and beats
  the frozen incumbent on every headline (CAGR 17.14% vs 15.80%, Sharpe 1.1722 vs 1.1537, OOS
  1.1971 vs 1.1857) — but its 4b DD margin is **+0.0858 pp against the anchor's +1.1028 pp**,
  12.8x thinner, and its edge is **+0.0185 Sharpe, t +0.34** (paired 63-day circular-block
  bootstrap, 400 reps). **0 of 27 4b-passing non-anchor cells resolve |t| > 2 on full-sample
  Sharpe and 0 on OOS Sharpe.** Rule 8's chooser never reaches it: the argmax-IS-Sharpe chooser
  goes to the **gross corner g = 1.00 on all three panels** and lands OOS-4b-FAIL on all three,
  while 19 of 126 cells pass 4b both full and OOS. PARK-not-KEEP, per rule 8.

  **GATES** all PASS: G0 >= 10y (16.68); G1 cross-script replay of the committed anchor; G2 126 of
  126 cells; G3 corpus stamp; G4 no chooser row >= 2017-01-01; G5 no leverage (1.000000); G6 every
  BOOK rung appears in the census histogram; G7 bit-identical recompute. Two tuned parameters per
  leg and no more (census: axis set, thinness bar — the bar reported at every value; book: N,
  GROSS). Survivorship stated (rule 9). RULES.md, scan.py, bot.py, baseline.py NOT modified.
  Script: `research/backtests/2026-09-19_rung-thinness-census-and-well-measured-rung-chooser_C.py`.

## 2026-09-19 — idea 1423 (lane B): does a CONVENTION-ENSEMBLE beat the SINGLE COMMITTED CELL on the BINDING 4b DD LEG? **ANSWERED NO — THE BLEND IS A CONCENTRATION DIAL IN A COSTUME. KILL (capital), NO NEW BOOK, NO RULES CHANGE — WITH ONE CAVEAT LOGGED.**

  Idea 1409 (this morning) proved the standing 2026-09-04 KEEP-4b incumbent (U56, N = 20, H = 126,
  gross 0.75, weekly Fri-decide / Mon-trade, 10 bps, t+1) is **ONE DRAW from a 5.3173 pp DD-margin
  band** across its 12-1 leg's (skip, long) convention. The textbook antidote to a convention
  artefact is to stop choosing and AVERAGE the member books — zero tuned lookback parameters, the
  band's centre instead of its lucky tail. This run prices that antidote, and the trap in it.

  **THE GRID.** BLEND {WAVG (mean of the member weight frames), VOTE (top N = 20 of that blended
  frame, same H = 126 rule)} x SPAN {SKIP5 = skip {0,5,10,21,42} at long 252; LONG2 = long
  {189,252} at skip 21; BOTH10 = the full 5 x 2 grid}. Members are the idea-1409 books exactly;
  only their COMBINATION is new. Three panels, **all 18 cells published**.

  **THE CONTROL IS THE WHOLE POINT.** A blended book shallows drawdown by HOLDING MORE NAMES
  (WAVG runs **23.5 .. 43.8** names against the anchor's 19.8) — the same plain exposure dial that
  killed idea 1405 (trailing equity stop) and idea 1413 (breadth throttle). Every cell is therefore
  paired against its **OWN CONCENTRATION-MATCHED CONTROL**: the frozen anchor convention re-run at
  that cell's realised name count, DERIVED from the cell and not chosen (worst match 0.450 names,
  G7). Gaps scored by a PAIRED circular-block bootstrap (400 reps x 63-row blocks, seed 20260919,
  identical block starts).

  **THE BAR WAS PRE-REGISTERED AND IT FAILS ON BOTH LEGS.** Stated in the script header before the
  numbers: worth capital only if on U56 (i) the DD margin exceeds the anchor's own **+1.1028 pp**
  AND (ii) the Sharpe edge over its own control resolves **t > +2**. **(i) 0 of 6 cells** (range
  -1.5448 .. **+0.2120** pp). **(ii) 0 of 6** (t range -1.12 .. +0.48). **BOTH: 0 of 6.**

  **AND NOTHING RESOLVES ANYWHERE.** Against the concentration-matched twin, **0 of 18 cells
  resolve |t| > 2 on Sharpe and 0 favour the ensemble**; median dSharpe **-0.0143**, median |t|
  0.48. On the BINDING leg — MaxDD, bootstrapped on the same blocks as a REPORTED DIAGNOSTIC added
  after the first pass, which moves no bar — **0 of 18 resolve and 0 are SHALLOWER**; median gap
  **-0.54 pp**, U56 median **-1.00 pp**. Against the frozen anchor, 1 of 18 resolves and **0 BEAT
  it**; median dSharpe -0.0185, median dMaxDD -1.45 pp. **4a 0 of 18.**

  **THE CAVEAT, LOGGED HONESTLY.** U56 **WAVG SKIP5** is the grid's only 4b pass (U56 1 of 6, B136
  0 of 6, SMALL 0 of 6): 15.71% / **1.1477** / **-20.02%**, halves 1.166 / 1.144, DD margin
  **+0.2120 pp** — a pass **5.2x THINNER** than the anchor's own. Rule 8 lands on exactly this cell
  on U56, and it is **the record's first DD-leg attack to come out OOS-POSITIVE against the frozen
  anchor**: OOS 17.76% / **1.2061** / -20.02% against 17.32% / 1.1857 / -19.13%, **dSharpe +0.0204**,
  **OOS 4b PASSES**. It is still a KILL, because against its own N = 24 twin that edge is
  **+0.0164 of Sharpe (t +0.48)** and **+1.00 pp of MaxDD (t +0.88)** — unresolved on both, i.e.
  buyable by turning one exposure dial and nothing more.

  **RULE 8 (IS = warm-up..2016-12-31, 2017-2026 read ONCE).** Picks WAVG SKIP5 on U56 (+0.0204 of
  OOS Sharpe vs the anchor, -0.89 pp of MaxDD, OOS 4b PASS) and WAVG BOTH10 on B136 (+0.0442,
  -1.36 pp, 4b FAIL) and SMALL (-0.0692, -3.32 pp, 4b FAIL). Mean OOS Sharpe minus the frozen
  anchor **-0.0015**, 2 of 3 positive; **minus its OWN control -0.0297, 1 of 3 positive**. OOS 4b
  1 of 3, 4a 0 of 3. **Convention-averaging buys nothing the concentration dial does not already
  sell — so it is not a route to the binding leg.**

  GATES all pass: G0 min sample 16.68y; G1 cross-script replay of the committed U56 anchor
  **|dSharpe| 3.72e-05** (15.80% / 1.1537 / -19.13% full, 1.1857 OOS); G2 18 of 18 published; G3
  two tuned parameters; G4 max realised weight sum **0.750000** (no leverage, no shorting); G5 the
  chooser reads no row on or after 2017-01-01; G6 the ensembles genuinely differ from the anchor
  book — max |W_ens - W_anchor| **7.27e-02**, published rather than asserted, so a null reading
  could not have been a silent no-op; G7 the concentration match is real, worst |gap| **0.450
  names**. Survivorship (rule 9): U56/B136 are current-constituent lists and SMALL a current
  sub-$2B screen (54 tickers with max_1d_move >= 1.0 dropped, 665 kept), so every level is an upper
  bound; what is read here is a GAP between a book and its own twin on identical names and days.

  **NO RULES CHANGE.** Script `research/backtests/2026-09-19_convention-ensemble-vs-concentration-matched_B.py`.

## 2026-09-19 — idea 1409 (lane cloud): is the incumbent's 4b DD MARGIN a LOOKBACK-SKIP ARTEFACT? **ANSWERED YES — THE COMMITTED PASS IS A LOOKBACK CONVENTION. KILL (capital), NO NEW BOOK, NO RULES CHANGE — AND A CONFIRMED CAVEAT ON THE STANDING 2026-09-04 INCUMBENT.**

  Idea 1257 priced the composite's leg SUBSETS but froze each leg's own (skip, length). The 12-1
  leg's **21-day skip** decides whether the book buys what has just fallen or what has just risen —
  whether it runs INTO or AWAY FROM a crash — which is exactly where a −19.13% is made. It had
  never been walked.

  **THE GRID.** SKIP {0, 5, 10, 21, 42} x LONG {189, 252} on the composite's FIRST leg only; the
  other two legs (0, 126) and (0, 63), N = 20, H = 126, gross 0.75, MAXVOL 0.60, the 200d MA gate,
  the weekly cadence, 10 bps and t+1 all frozen. Three panels, **all 30 cells published**.

  **THE BAR WAS PRE-REGISTERED AND IT IS EXCEEDED BY 4.8x.** Stated in the script header before the
  numbers: if the U56 DD margin's spread across the 10 cells exceeds the incumbent's own
  **+1.1028 pp**, the committed pass is a convention. **The spread is 5.3173 pp** (−4.2145 at
  (21, 189) to +1.1028 at (21, 252)). Holding LONG at the incumbent's own 252 and moving the SKIP
  ALONE, the spread is still **1.5635 pp** — larger than the whole margin.

  **THE INCUMBENT'S CELL IS THE ONLY ONE OF THE TEN THAT PASSES 4b.** U56 **1 of 10**, B136 0 of 10,
  SMALL 0 of 10; **4a 0 of 30**. On U56 the CAGR, H1 and H2 legs pass at 10 of 10 and the DD leg at
  1 of 10 — the same one-leg story the record has told eight times, now localised to a lookback
  convention.

  **AND THE PERFORMANCE EVIDENCE DOES NOT SELECT IT.** At LONG = 252 the five skips run Sharpe
  **1.1322 .. 1.1556** at **89-91% name overlap** with the anchor book, and the full-sample argmax
  is **skip 10, not 21**. The four non-anchor skips fail the DD cap by 0.18-0.46 pp. **Two of them
  BEAT the anchor out of sample and still fail on drawdown**: skip 10 (OOS 18.17% / **1.2261** /
  −20.67%) and skip 42 (OOS 18.40% / **1.2329** / −20.41%) against the anchor's 17.32% / 1.1857 /
  −19.13%.

  **WHAT RESOLVES AND WHAT DOES NOT.** Under a PAIRED circular-block bootstrap (400 reps x 63-row
  blocks, seed 20260919, identical block starts), **4 of 27 non-anchor cells resolve |t| > 2 against
  the anchor and 0 of the 4 beat it**; median |t| 0.62. All four are LONG = 189 cells — dropping the
  long leg to 189 costs U56 a mean **−3.18 pp** of DD margin. **The SKIP dial at LONG = 252 is
  UNRESOLVED (all |t| <= 0.60)** and is reported as such: the record has no evidence that 21 is
  better than 0, 5, 10 or 42, only that it is the one that happens to clear the cap.

  **RULE 8 (IS = warm-up..2016-12-31, 2017-2026 read ONCE).** The IS-Sharpe chooser lands on the
  anchor **(21, 252)** on U56 and loses on the other two panels — **(0, 252)** on B136 (−0.0326 of
  OOS Sharpe, −0.62 pp of MaxDD) and **(10, 189)** on SMALL (−0.1788, −7.37 pp). Mean OOS Sharpe
  minus the frozen anchor **−0.0705**, **0 of 3 panels positive**; OOS 4b 1 of 3, 4a 0 of 3.
  **Touching the lookback convention buys nothing out of sample — so freeze it — but the committed
  +1.10 pp should be read as ONE DRAW FROM A 5.32 pp BAND, not as a property of the strategy.**

  GATES all pass: G1 cross-script replay of the committed anchor **|dSharpe| 3.7e−05** (15.80% /
  1.1537 / −19.13% full, 1.1857 OOS); G2 skip < long at all 30 cells; G3 30 of 30 published; G4 two
  tuned parameters; G5 the chooser reads no row on or after 2017-01-01; G6 max realised weight sum
  **0.750000** (no leverage, no shorting); G7 the legs genuinely differ — max |score − anchor score|
  **3.31e−01**, published rather than asserted, so a null reading could not have been a silent
  no-op. Survivorship (rule 9): U56/B136 are current-constituent lists and SMALL a current sub-$2B
  screen (54 tickers with max_1d_move >= 1.0 dropped, 665 kept), so every level is an upper bound;
  what is read here is a SPREAD across one dial on identical names and identical days.

  **NO RULES CHANGE.** Script `research/backtests/2026-09-19_lookback-skip-artefact_cloud.py`.

## 2026-09-19 — idea 1405 (lane cloud): does a TRAILING EQUITY STOP on the incumbent's OWN BOOK buy the BINDING 4b DD LEG? **ANSWERED NO — THE BRAKE IS REAL, IT SHALLOWS THE BINDING LEG, AND AT MATCHED EXPOSURE IT IS WORTH NOTHING ON 216 OF 216 CELLS. KILL (capital), NO NEW BOOK, NO RULES CHANGE.**

  The standing 2026-09-04 KEEP-4b incumbent (U56, N = 20, H = 126, gross 0.75, weekly Fri-decide /
  Mon-trade, 10 bps, t+1) passes on one leg's margin: MaxDD −19.13% against a −20.23% cap, **+1.10
  pp**, with only 0.046 of gross of headroom (idea 1194). Every prior attack went at the SIGNAL.
  An equity-curve brake goes at the leg itself: it predicts nothing, it reacts to the book's own
  realised loss.

  **THE GRID.** DEPTH {0.05, 0.075, 0.10, 0.125, 0.15, 0.20} x FRAC {0, 0.25, 0.50, 0.75, 1.00} at
  the frozen incumbent, on three panels. RESTORE {SAME, HALF, PEAK} is a REPORTED axis, not a third
  dial — rule 8 runs separately inside each convention, so no arm has more than two free parameters.
  **All 270 cells published** in `.grid.csv`. The brake decides at rebalance row t from the book's
  own NET equity through row t−1 only, on an already-lagged grid; it touches EXPOSURE, never
  selection, so the frame is built once and scaled.

  **THE BRAKE WORKS — AND THAT IS NOT THE QUESTION.** U56's 4b DD margin runs **+1.10 pp frozen to
  +13.62 pp** at (SAME, 0.05, 1.00). 4b passes **59 of 90** U56 cells, 6 of 90 B136, **0 of 90**
  SMALL. **4a: 0 of 270.**

  **THE CONTROL DECIDES IT.** A brake that shallows drawdown by holding less stock is a gross dial
  in a costume, so every one of the 216 biting cells is scored against its OWN **exposure-matched
  FLAT gross cut** (fine ladder 0.20..0.75 by 0.01, controls not dials), gap scored by a PAIRED
  circular-block bootstrap (400 reps x 63-row blocks, seed 20260919, identical block starts).
  Against that twin the brake's **median MaxDD edge is −0.01 pp** (U56 −0.002, B136 −0.165, SMALL
  +0.105) and its **median Sharpe edge −0.1009**. **90 of 216 biting cells resolve |t| > 2 and
  0 of the 90 favour the brake**; OOS, 31 resolve and 0 favour it. Only **7 of 216** cells show any
  positive Sharpe gap at all. Of U56's 41 biting 4b passes, median Sharpe gap vs twin **−0.0274**,
  best MaxDD gap **+3.01 pp**, and the 7 that resolve all resolve AGAINST the brake.

  **THE ONE HONEST CELL, REPORTED AS UNRESOLVED.** U56 / SAME / depth 0.05 / frac 0.25: CAGR 14.02%,
  Sharpe 1.1522, MaxDD **−16.54%** (DD margin **+3.69 pp** against the frozen +1.10 pp), OOS Sharpe
  **1.2024** against the anchor's 1.1857. It buys **+1.15 pp** of MaxDD over its g = 0.69 twin for
  **−0.0013** of Sharpe at **t = −0.04**. Inside its own SE. Not an edge. At depth 0.20 the brake
  **never fires on U56** at all — the book's own weekly-grid peak-to-trough never reaches −20%.

  **RULE 8 (IS = warm-up..2016-12-31, 2017-2026 read ONCE).** The IS chooser picks **FRAC = 0 — the
  frozen incumbent — on 7 of 9 (panel, restore) arms**, including all three U56 and all three B136
  arms. Mean OOS Sharpe minus the frozen anchor **−0.0020**; the two SMALL arms that do brake land
  −0.0189 and +0.0012. U56 OOS anchor **17.32% / 1.1857 / −19.13%** against SPY 15.26% / 0.8738 /
  −33.72% and live RULES v2 9.46% / 1.2769 / −12.05%. OOS 4b among the 9 arms: 3 of 9, all the
  untouched anchor; 4a 0 of 9.

  GATES all pass: G1 cross-script replay of the committed 2026-09-04 U56 anchor **|dSharpe| 3.7e−05**
  (15.80% / 1.1537 / −19.13% full, 1.1857 OOS); G2 the FRAC = 0 cell is bit-identical to the frozen
  book at all 18 (depth, restore) cells, max |dret| **0.000e+00**; G3 270 of 270 published; G4 two
  tuned parameters per arm; G5 the chooser reads no row on or after 2017-01-01; G6 max realised
  weight sum **0.750000** (no leverage, no shorting); G7 feed-lag sensitivity published.
  Survivorship (rule 9): U56/B136 are current-constituent lists and SMALL a current sub-$2B screen
  (54 tickers with max_1d_move >= 1.0 dropped, 665 kept), so every absolute level is an upper bound;
  what is read here is a CONTRAST between a braked book and its own twin on identical names and days.

  **NO RULES CHANGE.** Script `research/backtests/2026-09-19_trailing-equity-stop-on-the-incumbent_cloud.py`.

## 2026-09-19 — idea 1194 (lane C): how many committed 4b PASSES COLLAPSE under a GROSS-FREE KEY? **ANSWERED NO — THE RE-KEY IS NOT A DE-DUPLICATION, IT ERASES THE DIAL THAT DECIDES THE VERDICT. KILL (re-key), KILL (dial), NO NEW BOOK, NO RULES CHANGE — AND ONE CONFIRMED CAVEAT ON THE STANDING INCUMBENT.**

  Idea 1189 recommended keying a 4b pass on `(panel, N, cadence, H)` with GROSS as an ATTRIBUTE,
  and that re-key collapsed its own 14 passes to 8 (0.43 duplicated). The re-key is sound only if
  a 4b PASS is INVARIANT to gross within a book. **It is not, and the reason is mechanical.**

  **SHARPE IS FLAT IN GROSS AND THE TWO 4b LEVEL LEGS ARE NOT.** On 270 real books — 3 panels x
  6 N {10,15,20,25,30,40} x **15 gross rungs 0.30..1.00**, every other byte the frozen 2026-09-04
  incumbent (H = 126, weekly Fri-decide/Mon-trade, 10 bps, t+1, 260-row warm-up), **all 270
  published** — U56 N=20 moves **Sharpe 1.1520 -> 1.1542 across the WHOLE ladder (swing 0.0022;
  OOS swing 0.0029)** while CAGR runs 6.26% -> 21.14% and MaxDD −7.99% -> −24.93%. The 4b CAGR
  floor therefore binds from BELOW and the 4b DD cap from ABOVE, and a pass is a contiguous
  **INTERVAL IN GROSS** — contiguous at **18 of 18 families** (G7 tested, not asserted).

  **SO THE KEY CANNOT DROP GROSS.** 4b passes at **49 of 270** cells; median interval width is
  **2.5 of 15 rungs** (large-cap families 4.5, widest 7); and **only 26 of 49 passing cells (53.1%)
  still pass at BOTH g−0.05 and g+0.05**. Two cells sharing `(panel, N, cadence, H)` and differing
  only in gross hold the SAME NAMES ON THE SAME DAYS and return opposite 4b verdicts. Collapsing
  them does not remove a duplicate; it removes the only field that distinguishes a pass from a fail.
  **4a: 0 of 270.**

  **AND THE RE-KEY IS UNAPPLICABLE TO 99.3% OF THE RECORD ANYWAY.** Mechanical census of
  LEADERBOARD.md (7,805 table rows; regexes and recall limits published in the script, counts a
  LOWER bound): **1,295** rows assert a 4b PASS. Of those, **322 (24.9%) state their gross** and
  only **9 (0.7%) state the full `(panel, N, cadence, H)` key**. The record cannot be re-keyed
  mechanically because it was never stamped.

  **THE CAPITAL FINDING — THE FROZEN INCUMBENT IS THE LAST PASSING RUNG OF ITS OWN LADDER.** U56
  N=20: 4b DD margin **+1.1028 pp at g = 0.75** and **−0.0797 pp at g = 0.80**. The slope is
  **−24.19 pp per unit gross**, so the headroom is **0.0456 of gross — 0.91 of ONE 0.05 rung.**
  Symmetrically the CAGR floor is 0.96 pp away at g = 0.55 and fails at 0.50. In **ALL FOUR**
  large-cap families whose passing interval contains 0.75, **0.75 is the TOP EDGE**; no large-cap
  family in this grid passes 4b above it. Eight prior runs localised the binding DD leg; this one
  prices its remaining travel in the one dial that moves it.

  **RULE 8 (IS = warm-up..2016-12-31, 2017-2026 read ONCE).** Letting a chooser touch gross buys
  nothing: OOS Sharpe(C_FULL, N and g free) − OOS Sharpe(C_NFREE, g frozen at 0.75) =
  **−0.0003 / +0.0041 / −0.0001** on U56 / B136 / SMALL. Because Sharpe is flat in gross the
  IS-Sharpe chooser picks **g = 1.00 on all three panels** and then **fails 4b on DD everywhere**.
  The frozen anchor (N=20, g=0.75) beats both choosers OOS on U56 — **17.32% / 1.1857 / −19.13%**
  against C_FULL 18.93% / 1.1213 / −29.09% and C_NFREE 14.17% / 1.1216 / −22.46% (SPY OOS
  15.26% / 0.8738 / −33.72%, live RULES v2 OOS 9.46% / 1.2769 / −12.05%) — and is the only U56 arm
  of the three that passes 4b. **Freeze both dials.**

  SMALL663 is **0 of 90** and fails H1, H2 and OOS at every rung.

  GATES all pass: G1 incumbent replay 15.80% / **1.1537** / −19.13% against the committed
  15.80% / 1.1537 / −19.13% (|dSharpe| **3.7e-05**, floor 5e-3); G2 max |gross deviation| 3.3e-16;
  G3 270 of 270 cells published; G4 exactly two tuned parameters (N, gross); G5 the chooser reads
  no row on or after 2017-01-01; G6 bit-identical recompute; G7 contiguity tested; G8 census
  regexes and recall published. Survivorship (rule 9): U56/B136 are current-constituent lists and
  SMALL a current sub-$2B screen, so every absolute level is an upper bound and every 4b pass an
  optimistic one; the headline is a WIDTH read over one panel on one set of days.

  **NO RULES CHANGE.** Script `research/backtests/2026-09-19_gross-free-key_C.py`.

## 2026-09-19 — idea 1413 (lane B): does a PANEL-BREADTH THROTTLE on GROSS buy the BINDING 4b DD LEG, against its OWN EXPOSURE-MATCHED FLAT CUT? **ANSWERED NO — THE SIGNAL IS REAL, THE REPAIR IS REAL, AND AT MATCHED EXPOSURE IT IS WORTH NOTHING ON 90 OF 90 CELLS. KILL (capital), NO NEW BOOK, NO RULES CHANGE.**

  The standing 2026-09-04 KEEP-4b incumbent (U56, N = 20, H = 126, gross 0.75, weekly, 10 bps,
  next-row) passes on one leg's margin: MaxDD −19.13% against a −20.23% cap, **+1.10 pp**. Eight
  consecutive runs found the DD leg is the only one that ever binds, and idea 1399 localised it to
  **34 short-fill rebalance rows**. Short fill is a breadth signal read at its last possible moment —
  the pool must fall below TWENTY names before the book holds a cent of cash. This run asks whether
  reading breadth EARLIER buys the leg.

  **THE PREMISE IS FACTUALLY TRUE.** On U56's 923 post-warm-up decision rows, panel breadth (the
  share of priced, investable names above their 200d with vol20 < 0.60) is below 0.50 at **162** rows
  and below 0.30 at **73**, against **98** short-fill rows, and the low-breadth rows sit exactly where
  the drawdown is made (2009: 14, 2022: 28, 2020: 5). A throttle at b0 = 0.70 bites on **41.0%** of
  rows against short fill's 3.7%.

  **AND THE REPAIR WORKS, ON ITS FACE.** Scaling gross by `min(1, (b_s/b0)**p)`, read at the decision
  row and applied the next row: **all 25 biting U56 cells have a SHALLOWER MaxDD than the incumbent**
  (−19.13% → **−13.55%** at p = 3.0 / b0 = 0.70), the 4b DD margin goes +1.10 pp → **+6.68 pp**, and
  **4b passes at 30 of 30 U56 cells**. Two dials and no more (p, b0); 30 cells per panel, **90 in
  all, every one published**.

  **THEN THE CONTROL EATS IT, AND THE CONTROL IS THE WHOLE EXPERIMENT.** Idea 1189 established that
  Sharpe is flat in gross, so any de-grossing slides one book along a fixed-Sharpe CAGR-vs-drawdown
  line. So every throttled cell here is judged against a **FLAT-GROSS book at that cell's OWN realised
  mean target gross**, same weight frame, same tape, same cost. **Paired circular-block bootstrap
  (400 × 63 rows, seed 20260919, identical blocks): of the 75 biting cells across three panels,
  dSharpe is inside 2 SE at 75 and dMaxDD is inside 2 SE at 75. The largest |t| ANYWHERE in the grid
  is 1.59 on Sharpe and 1.93 on MaxDD.** U56 means: dSharpe **−0.0003**, dMaxDD **+1.08 pp**, dCAGR
  **−0.57 pp**. The matched flat cut reaches −15.33% on U56 with no signal at all and also passes 4b
  at 30 of 30.

  **THE TIMING IS NOT FREE — IT IS STRICTLY DEARER.** U56 annualised turnover runs **2.77 → 4.27
  turns/yr** across the throttle grid while the matched flat control runs **2.77 → 2.20**. At the most
  aggressive cell the throttle trades **94% more than its own control** to reach a drawdown 1.78 pp
  shallower — a gap inside 0.50 SE — and gives up 0.79 pp of CAGR and 0.024 of Sharpe doing it.

  **B136 IS THE CLEANEST STATEMENT: THE CONTROL WINS OUTRIGHT.** The throttle passes 4b at **6 of 30**
  B136 cells; its own exposure-matched flat cut passes at **24 of 30**. On the second large-cap panel,
  de-grossing on a breadth signal is strictly worse than de-grossing on nothing. SMALL663 is **0 of 30
  both ways** and fails all five 4b legs. **4a 0 of 180 books.**

  **RULE 8: THE AXIS IS NULL TO AN OPERATOR TOO.** (p, b0) chosen on warm-up..2016-12-31 ONLY by IS
  net Sharpe, ties to the lowest p (do nothing), with a declared IS-Calmar control; 2017-2026 read
  ONCE. **Both choosers pick p = 0 — the incumbent — on U56, OOS delta +0.000000.** On B136 the
  IS-Sharpe chooser moves and loses **−0.0335** of OOS Sharpe; on SMALL both move and lose **−0.3195**
  and **−0.2471**. The ex-post best OOS U56 cell (p = 3.0 / b0 = 0.60, OOS 14.54% / **1.2538** /
  −13.48% against the incumbent's 17.34% / 1.1862 / −19.13%) is **reported, not claimed**: no declared
  chooser reaches it and its full-sample gap over its own matched flat is 0.09 SE.

  **GATES 6/6.** G1 p = 0 is b0-invariant, worst spread **0.000e+00**. G2 the p = 0 cell replays the
  committed incumbent to **2.51e-03** — inside the tape-vintage floor, OUTSIDE 5e-4, published rather
  than smoothed (`data/prices.csv` is restated daily, idea 1272). G3 at p = 0 the matched flat control
  IS the throttled book, **0.000e+00**. G4 the chooser reads no row ≥ 2017-01-01, asserted in code.
  G5 mean target gross non-increasing in p at **15 of 15** ladders. G6 exactly two tuned parameters.
  Deterministic, offline, 28s.

  **SURVIVORSHIP (rule 9).** U56/B136 are current constituents; SMALL is the current sub-$2B screen
  less 54 tickers with `max_1d_move >= 1.0`. Delisted, acquired and bankrupt names are absent from
  every panel, which flatters the books **and the breadth series itself** — a name that collapsed is
  not in breadth's denominator — so the throttle is measured on an OPTIMISTIC signal and this null is
  if anything generous. Every 4b pass count is an upper bound.

  **WHAT THIS ADDS.** A ninth consecutive mechanism that cannot move the incumbent's sole binding leg
  on its own account. The new content is the **control**: this is the first run to price an
  exposure-TIMING mechanism against an exposure-MATCHED flat cut rather than against the incumbent.
  **ONE RECOMMENDATION IS LOGGED FOR THE SUNDAY REVIEW, NOT APPLIED (rule 6): a 4b pass bought by
  de-grossing — timed or untimed — should be published beside its own exposure-matched flat control,
  because at matched exposure the timing was worth nothing on 90 of 90 cells here.**

## 2026-09-19 — idea 1198 (lane C): how many committed RUNNER-EQUIVALENCE GATES were read through a SKIPNA MAX, and did the skip cover any cell OUTSIDE the warm-up? **ANSWERED — THE MAJORITY BASIS IS GENUINELY BLIND, AND IT COVERED NOTHING PUBLISHED. KILL as a dial, CONFIRM the infrastructure.**

  Idea 1191's G1b found `engine.backtest` emits NaN in `returns`, because `engine.py`'s
  `weights.reindex(...).fillna(0.0).shift(1)` never fills the row the shift vacates: the engine
  rebalances unconditionally at i = 0, reads an all-NaN target, carries `cur = NaN` to the first
  scheduled rebalance, and NaNs the turnover at both rows. 1191 observed that both rows sit inside
  the 260-row warm-up, but also that **no gate has ever checked it**, because `pandas.Series.max()`
  SKIPS NaN while `ndarray.max()` PROPAGATES it. This run settles both halves.

  **THE CENSUS IS REAL. 279 of 459 engine-equivalence gate lines (60.8%), across 341 of 1,209
  committed scripts, are on the SKIPNA_PANDAS basis; 127 (27.7%) are STRICT_NUMPY and 53 (11.5%)
  NaN-aware. 219 of 341 scripts (64.2%) carry NO NaN-propagating gate at all.** C2 runs the
  blindness rather than asserting it: a CLEAN difference reads 2.776e-17 on both bases; inject ONE
  NaN at post-warm-up row 3000 and the skipna basis still reads **2.776e-17, unchanged**, while the
  strict basis reads **nan**. And the record's OWN gate vector (FAST runner minus engine.backtest)
  **already carries 2 NaN cells** — every skipna gate in the record has been reading past NaN all
  along and reporting a clean 1e-17.

  **BUT THE SKIP COVERED NOTHING PUBLISHED, AND THAT IS NOW MEASURED RATHER THAN ASSUMED.** The
  canonical gate re-run on ndarray at 3 panels x 4 cadences x 2 pairs gives **0 of 24 readings with
  a post-warm-up NaN**, and post-warm-up max |FAST − ENGINE| of **8.327e-17** over the whole grid.
  The C1 census puts every NaN at row 0 and the first rebalance-application row at **24 of 24**
  (panel, cadence, book) cells — max index **61**, the Q cadence, against a 260-row warm-up — and
  the NaN'd turnover charge is **0.00 bps at all 24**, because no book holds a position that early
  in its own tape. The only way a NaN can reach a published window is a window starting at row 0 of
  its own `backtest()` call: **1 of 2,511 committed call sites** passes a pre-sliced frame
  (`2026-09-11_is-n_elig-...-mislabelling_cloud.py`) and it reads from row 260 of that slice.

  **SECONDARY FINDING, AND IT IS NEW: the defect's REACH is wider than 1191 read it.** G3 as
  pre-declared ("ENGINE == REPAIRED bit-for-bit after the last NaN row") **FAILS at 4.857e-17**, and
  the failure is published rather than swapped out. The cause is not the book: pandas'
  `DataFrame.sum(axis=1)` switches accumulation kernel when the frame carries a NaN **anywhere**, so
  the engine's NaN weight rows (56 to 43,920 cells per run) perturb **every other row too**. G3b
  demonstrates the kernel switch on a synthetic frame. The magnitude is 15 orders of magnitude below
  any published digit — G3a, the exact restatement (≤ 1e-15), PASSES on all 24 cells.

  **CAPITAL. The frozen 2026-09-04 incumbent (N = 20, H = 126, gross 0.75, weekly, 10 bps, t+1)
  priced through all three runners — engine.backtest as committed, a NaN-REPAIRED local copy, and
  the record's segment FAST runner — is ONE BOOK on all three panels**: worst within-panel
  full-sample Sharpe spread **2.220e-16**, identical 4a and 4b verdicts at 9 of 9 cells. U56
  **15.80% / 1.1537 / −19.13%**, OOS 17.32% / 1.1857 / −19.13%, **4b PASS**; B136 16.06% / 1.0654 /
  −20.74%, **4b FAIL:DD**; SMALL 7.81% / 0.5092 / −36.51%, 4b FAIL on all five legs. **4a 0 of 9.**
  G1 replays idea 1350's committed head-vintage U56 anchor at dev **+0.0000 / −0.0000 / +0.0000**.
  So the standing U56 4b pass is **runner-independent**: it is not an artefact of which runner
  produced it, and the record's fast runners are certified against the engine to 1e-16.

  **RULE 8: KILL AS A TUNED DIAL — the axis is exactly null.** The IS chooser (RUNNER by argmax IS
  net Sharpe on warm-up..2016-12-31, ties to ENGINE = do nothing, 2017-2026 read ONCE) picks ENGINE
  on 3 of 3 panels and the OOS delta is **+0.000000** on every one. A dial that cannot move a book
  is not a dial. (SMALL's ex-post best OOS reads FAST, at a 1e-16 tie — reported, not claimed.)

  **GATES 19/20**, the one failure being G3 in its pre-declared form, published with two exact
  restatements that pass. G2 REPAIRED carries 0 NaN at all 24 cells; G7 determinism 0.000e+00; G6
  the chooser reads no row ≥ 2017-01-01; G5 exactly two tuned parameters (RUNNER, BASIS), with
  PANEL / CADENCE / GROSS / COST reported at every value and never chosen on.

  **NO NEW BOOK AND NO RULES CHANGE.** `engine.py` is NOT modified — the repair exists only as a
  local copy so the defect could be priced; on this evidence installing it would change no published
  figure and would reset every committed replay anchor, so it should ride a RULES change rather than
  lead one. **ONE RECOMMENDATION IS LOGGED HERE FOR THE SUNDAY REVIEW, NOT APPLIED** (PROTOCOL.md
  untouched): a runner-equivalence gate should state its comparison basis and read the difference on
  `.values`, i.e. `float(np.abs((a - b).values).max())` with an explicit NaN count, so that a future
  fast runner that diverges by NaN cannot pass. Offline, deterministic, ~210s. Survivorship (rule 9):
  U56 / B136 are current-constituent lists and SMALL a current sub-$2B screen, so the absolute levels
  quoted are upper bounds — the bias is orthogonal to this run's question, which is a property of the
  arithmetic and not of the names.

## 2026-09-19 — idea 1403 (lane B): does the 2026-09-04 KEEP-4b BOOK SURVIVE the LIVE BOOK's OWN NO-RE-SPREAD SIZING CONVENTION? **YES ON U56 — AND ON B136 THE RE-SPREAD WAS BREAKING THE DD LEG ALL ALONG. KILL as a tuned dial.**

  RULES v2 clause 4 is explicit — "Do NOT re-spread the gross over the IN names: a re-grossed book
  is a different, unpriced book (idea 81)". The standing 2026-09-04 KEEP-4b candidate (N=20 slots,
  H=126, gross 0.75, weekly, 10 bps, t+1), on which every capital run of the last fortnight is
  built (1350, 1358, 1366, 1369, 1373, 1377), does the OPPOSITE: its slot is `gross / n`, not
  `gross / N`. **G9's census puts a number on it — 34 of 922 U56 rebalance rows (3.69%) fill fewer
  than 20 slots, min n = 8, and they are 2009:14 / 2020:5 / 2022:15**, i.e. exactly the three
  episodes that make the drawdown the record calls this book's SOLE binding 4b leg. At the worst
  row the candidate puts 9.38% of NAV on each of eight names. No run had priced that.

  One dial interpolates the two conventions: `w_i = gross*(f/n + (1-f)/N)`, f=1 the committed
  candidate, f=0 the live book's fixed slot with the shortfall in CASH at 0%/yr. 5 rungs x 3 panels
  x gross {0.60, 0.75} = 30 cells, all published. **G1 replays idea 1350's committed head-vintage
  U56 anchor 15.80% / 1.1537 / -19.13% at dev +0.0000 / -0.0000 / +0.0000.**

  **H_PASS CONFIRMED — the pass is not an artefact of re-grossing.** U56 gross 0.75 at f=0 reads
  **15.49% / 1.1482 / -19.10%**, OOS **16.82% / 1.1731 / -19.10%**, clearing every 4b leg FULL and
  OOS (DD room +1.13 pp, CAGR room +4.91 pp, OOS Sharpe against SPY's 0.8738). Obeying the live
  rule costs **-0.31 pp of CAGR and -0.0055 of Sharpe** and buys 0.02 pp of drawdown.

  **THE SECONDARY FINDING IS THE BIGGER ONE. On B136 at gross 0.75 the committed 4b FAIL is a
  CONVENTION ARTEFACT:** f=1 draws down **-20.74%** against the -20.23% cap (FAIL:DD by 0.51 pp),
  f=0 draws down **-18.78%** and PASSES with +1.45 pp of room. Over all 30 cells the fixed slot
  passes 4b at **4 of 6** against the re-spread's **3 of 6** — it weakly dominates everywhere and
  is beaten nowhere. SMALL is the null control: **0 short-fill rows of 818**, so all five rungs are
  bit-identical (d = 0.0000).

  **H_DD REFUTED on U56** (predicted >= 0.5 pp shallower, actual +0.02 pp) **and confirmed on B136**
  (+1.96 pp). **H_CAGR half-refuted**: f=0 does cost CAGR, but the 4b CAGR floor never binds
  (+4.91 / +5.35 pp of room at f=0). **H_RES CONFIRMED** — paired 63-row block bootstrap, 400 reps,
  seed 20260919: U56 t **-1.79** FULL / **-1.69** OOS, B136 **-0.85 / -0.83**, SMALL exactly 0:
  unresolved on 3 of 3 panels, so obeying the live rule is FREE within the tape's resolution.
  **H_PICK CONFIRMED — rule-8 KILL as a dial**: the IS chooser picks f=0.00 on U56 and B136 and
  loses **-0.0126** and **-0.0050** of OOS Sharpe, and the ex-post best OOS rung is f=1.00 on both.
  `f` is a convention the rule book fixes, never a parameter to fit. **4a KILL at 30 of 30.**

  **GATES 18/20, with both failures PUBLISHED rather than swapped.** G3 as pre-declared ("all five
  rungs bit-identical on every full-fill row") FAILS on U56 (1.03e-04) and B136 (3.69e-04) by a
  known mechanism: the turnover charge on the FIRST day of a full-fill segment FOLLOWING a short
  one depends on the drifted weights carried out of that short segment. The exact restatements both
  pass on all three panels — **G3a** slot weight identical on every full-fill rebalance row
  (6.9e-18, double rounding on gross/N), **G3b** returns bit-identical on every full-fill day after
  the segment-start row (0.000e+00) — bounding the leak at 4 of 4448 days on U56 and 2 of 4448 on
  B136. G2 deployed-gross identity worst |dev| 2.2e-16; G4 30 of 30 cells; G5 exactly two tuned
  parameters (f, panel — GROSS reported at both 0.60 and 0.75); G6 chooser reads no row >=
  2017-01-01; G7 determinism exact; G8 mean deployed gross monotone in f on all three panels.

  Memo `research/backtests/2026-09-19_no-re-spread-sizing-convention_MEMO.md` carries the exact
  RULES wording. **NO RULES CHANGE THIS RUN**: the clause changes no selection and no exposure
  target, so it rides the next RULES change (the posture 1358 took). RULES.md, PROTOCOL.md,
  scan.py, bot.py and baseline.py untouched. Offline, deterministic, ~10s. Survivorship (rule 9):
  U56/B136 are current-constituent lists and the bias runs AGAINST the re-spread column — the eight
  names still eligible in Jan 2009 are eight names that survived to be listed today — so f=1 is an
  upper bound and the -0.31 pp cost of f=0 is itself an upper bound. Cash is priced at 0%/yr
  deliberately: idea 1358's SHY correction would flatter f=0, which carries the most cash.

## 2026-09-19 — idea 1377 (lane cloud): RANK-HYSTERESIS BUFFER in place of the 126-day MINIMUM HOLD. **ANSWERED NO — THE BUFFER KEEPS THE FAILURES OUT AND CANNOT BUY THE TURNOVER. KILL.**

  Idea 1366 put a number on the incumbent's calendar immunity: 14.48% / 15.57% / 30.61% of all held
  name-weeks on U56 / B136 / SMALL sit on names FAILING the book's own eligibility test at H=126. The
  queue's proposed repair was SIGNAL immunity — keep a name while it still passes the screen and its
  composite rank is inside b*N, evict it otherwise — on the argument that it should cut the same
  turnover without carrying failures. It does the first thing and not the second.

  Everything but the hold rule is byte-identical to the frozen 2026-09-04 book (same raw 3-leg
  composite, same above-200d and vol20 < 0.60 entry test, N=20, equal weight gross/n at 0.75, weekly,
  10 bps, t+1, 260-row warm-up). H=126 and H=0 are carried as control rows on every panel. G1 replays
  idea 1350's head-vintage anchor 15.80% / 1.1537 / -19.13% at max|dev| 3.7e-05; G3 shows b=1.0 under
  E+R is bit-identical to the H=0 control on all three panels; **G8 independently reproduces idea
  1366's failing-share triple (0.1514 / 0.1520 / 0.3009 against its 0.1448 / 0.1557 / 0.3061).**

  **H_FAIL CONFIRMED, H_TURN REFUTED — and that is the answer.** Under E+R (retain only while ELIGIBLE
  and inside b*N) the failing share is **0.00% at all 18 cells**. But turnover never returns to the
  incumbent's **2.75/yr**: the cheapest clean U56 rung is **4.44/yr (+61%)**, with b=1.0/1.5/2.0 at
  10.13 / 5.49 / 4.67. The mechanism is mechanical, not tuning — losing eligibility ALONE evicts 0.73
  names per rebalance, and the rank test evicts on top of that. The permissive mode R does reach
  1.96/yr at b=2.0, but only by letting failures back in (13.08% of held name-weeks). **Calendar
  immunity is buying a turnover reduction that signal immunity cannot replicate at any b.**

  **WHAT IT DOES BUY, AND THE PRICE.** This is the first mechanism in the record to shallow the U56
  MaxDD at scale: **+1.63 / +1.90 / +3.87 pp** at b = 1.5 / 2.0 / 3.0 (E+R), widening the 4b DD margin
  **+1.10 -> +2.73 / +3.01 / +4.97 pp**. It is still not worth buying: the exchange rate is **0.58 /
  0.58 / 0.97 pp of drawdown per pp of CAGR** on a leg U56 ALREADY PASSES, CAGR falls **15.80% ->
  12.99 / 12.54 / 11.80%**, the CAGR-floor margin falls **5.22 -> 2.40 / 1.95 / 1.21 pp**, and
  **Calmar FALLS at every rung (0.826 -> 0.742 / 0.728 / 0.773)**. PARK for U56 E+R as a drawdown
  instrument; not a KEEP.

  **THE DIAL SATURATES, AND THE PRETTIEST CELL IS AN ARTEFACT.** U56 has 55 investables, so b*N = 60
  exceeds the whole pool and the rank test CANNOT BIND at b >= 2.75: b = 3.0 / 4.0 / 6.0 are
  bit-identical at both modes. Under mode R that cell evicts **0.00 names per rebalance** — a literal
  BUY-AND-NEVER-SELL book, not a hysteresis buffer. It posts the run's best headline (Sharpe **1.3216**,
  MaxDD -16.91%, turnover 0.91/yr, 4b PASS) and it is published as an artefact: the paired circular-block
  bootstrap (400 reps x 63-row blocks, seed 20260919, identical blocks both sides) makes its return
  difference **NEGATIVE and resolvable — FULL t -2.34, OOS t -2.20** — so the +0.168 of Sharpe is pure
  denominator. Saturation thresholds, now on the record: **U56 2.75, B136 6.75, SMALL 33.25.**

  **BOTH KEEP PATHS.** 4a **0 of 42**. 4b **11 of 42 and all 11 on U56** (2 of them the H=126 and H=0
  controls). **B136 0 of 14** — under mode R the buffer makes its drawdown WORSE (-22.7% to -27.8%
  against -20.7%). **SMALL 0 of 14.** Binding legs across the 31 failures: DD 23, H2 14, OOS 13.

  **RULE 8 (b chosen on warm-up..2016-12-31, ties to the LARGEST b, 2017-2026 read ONCE).** The
  saturation makes the chooser pick b=6.0 on 5 of 6 (panel, mode) cells. **U56 E+R loses -0.0314 of OOS
  Sharpe** and never finds the ex-post best rung (b=2.0); **B136 E+R loses -0.1204**. The two positive
  deltas are both unusable: U56 mode R's +0.0562 IS the never-sell artefact, and SMALL's +0.1077 /
  +0.1038 sit on a panel that fails 4b at 0 of 14. **Fifth dial in a row to fail rule 8 on the live
  panel** (1358 sleeve, 1362 N, 1366 H, 1369 cluster cap, 1373 inverse-vol).

  Gates **7/7**, offline, deterministic, 11 s, 42 rows + 42 bootstrap rows + 6 rule-8 rows all
  published. **No memo and no RULES change** (KILL).

## 2026-09-19 — idea 1369 (lane cloud): CLUSTER CAP on the incumbent's top 20. **THE DIVERSIFICATION DEFECT IS REAL AND THE OBVIOUS REPAIR IS A KILL — CAPPING A CLUSTER MAKES THE DRAWDOWN DEEPER.**

  Selection inputs, eligibility, slot count (N=20), min-hold (H=126), gross (0.75), cadence and costs
  held byte-identical to the frozen 2026-09-04 book; gate G1 replays idea 1350's committed head-vintage
  anchor 15.80% / 1.1537 / -19.13% at max|dev| 3.7e-05, and G3 shows cap=20 is bit-identical across both
  RHO controls on all three panels. Convention FILL: a candidate whose cluster is full is SKIPPED and the
  slot goes to the next name down the SAME ranking, so the cap changes WHICH names are held and nothing
  else — not N, not gross, not the eligibility test, not the equal weighting. Clustering is causal and
  deterministic (leader algorithm at correlation >= RHO on the trailing 252 rows ending at the decision
  row, refreshed the first rebalance of each calendar year, labels frozen between refreshes; RHO
  published at 0.50 and 0.65 as a control, never chosen on).

  **H_BIND CONFIRMED — the incumbent really is a one-theme book.** The mean largest cluster among its 20
  slots is **9.20 names at RHO 0.65 and 13.63 at RHO 0.50** on U56 (7.77 / 12.93 on B136), and the book
  spends **78.4% / 98.2%** of held days with some cluster over 5 slots. On SMALL the statistic is inert
  (1.55 / 3.37 of 20) — small caps do not co-move enough for the cap to bite, and cap=6 is bit-identical
  to uncapped there.

  **H_DD FAILS AT EVERY RUNG. U56 KILL.** Against the uncapped -19.13%, MaxDD is **DEEPER** at cap
  2/3/4/5/6 by **-1.62 / -0.28 / -2.53 / -1.43 / -3.40 pp** (RHO 0.65), taking the 4b DD margin from
  **+1.10 pp to negative at 9 of the 10 capped cells**, while CAGR falls **15.80% -> 12.68-14.25%** and
  Sharpe **1.1537 -> 1.0456-1.1531**. The mechanism is not subtle: the cap forces the book down its own
  ranking into weaker names without removing the market beta that actually produces the drawdown. The
  paired circular-block bootstrap (400 reps x 63-row blocks, seed 20260919, identical blocks both sides)
  puts the return difference **NEGATIVE at 10 of 10 U56 cells and resolvable at 7** (FULL t -1.59..-2.88,
  OOS t -1.95..-3.25; cap=4 OOS **t -3.25**). B136 and SMALL are unresolved at 20 of 20 (|t| <= 1.49).

  **BOTH KEEP PATHS.** 4a **0 of 36** (live RULES v2's -12.05% MaxDD stays out of reach for a growth
  book). 4b **5 of 36** — and **2 of the 5 are the uncapped incumbent itself**. The only capped survivors
  are U56 cap=4/RHO 0.50 (DD margin +0.10 pp) and cap=3/RHO 0.65 (+0.83) — both strictly worse than the
  incumbent's +1.10 — plus B136 cap=6/RHO 0.65 at +0.02 pp. The binding leg is the DD cap at **27 of 31**
  failures. SMALL fails all five legs at every cap.

  **RULE 8 (cap chosen on warm-up..2016-12-31, ties to the LOOSEST cap, 2017-2026 read ONCE).** U56 picks
  **cap=6 (RHO 0.50) and cap=5 (RHO 0.65) and LOSES -0.1156 / -0.1211 of OOS Sharpe**; the ex-post best
  OOS cap is **20, i.e. no cap, at both RHOs**. The dial is anti-selected on the live panel. B136 picks
  cap=2 for +0.0880 at RHO 0.50, but that cell fails 4b on the DD cap by **0.046 pp** and RHO is a
  control, not a third dial. SMALL's +0.02 is on a panel that fails 4b at 0 of 12.

  **WHAT THE RECORD SHOULD CARRY:** the incumbent's concentration is now a measured number rather than a
  worry, and the standard fix is priced and rejected. Gates **8/8**, offline, deterministic, 12 s, 36
  cells + 30 bootstrap rows + 6 rule-8 rows all published. **No memo and no RULES change** (KILL).

## 2026-09-19 — idea 1373 (lane C): INVERSE-VOL SLOT WEIGHTING on the incumbent's 20 slots. **A DRAWDOWN INSTRUMENT, NOT A SHARPE ONE — AND ON THE LIVE PANEL THE DRAWDOWN IS NOT FOR SALE AT A PRICE WORTH PAYING.**

  Selection, eligibility and slot count held byte-identical to the frozen 2026-09-04 book (gate G3:
  p=0 reproduces it exactly, and G1 replays idea 1350's committed head-vintage anchor 15.80% /
  1.1537 / -19.13% at max|dev| 3.7e-05); gross stays 0.75; only the 20 slot weights move, w
  proportional to vol^-p. This is NOT the SCORE vol scaler the 2026-09-04 KEEP killed.

  **U56 KILL.** p=1 shallows MaxDD **+2.64 pp** (-19.13% -> -16.49%), widening the 4b DD margin
  **+1.10 -> +3.74 pp** — a leg U56 already PASSES — and pays for it at **0.78 pp of drawdown per pp
  of CAGR**: CAGR 15.80% -> 12.40%, the CAGR-floor margin 5.22 -> **1.81 pp** (0.52 pp at p=1.5),
  Calmar monotonically **0.826 -> 0.752 -> 0.718**, turnover 2.75 -> 5.56/yr. The paired circular-block
  bootstrap (400 reps x 63-row blocks, seed 20260919, identical blocks both sides) puts the return
  difference **NEGATIVE and resolvable at 20 of 30 cells** (U56 p=1 FULL **t -4.49**, OOS **t -2.51**);
  the +0.021 OOS Sharpe is pure denominator. The dial swaps a 5 pp margin for a 1 pp one.

  **B136 is the one place the leg binds, and rule 8 cannot reach it.** At equal weight B136 fails 4b
  on the **DD cap alone** (margin **-0.51 pp**); every rung p = 0.25..1.00 flips it to a full 4b PASS
  **full AND OOS**, the drawdown bought **cheaper than 1:1** (1.69 / 1.65 pp per pp of CAGR) with
  Calmar RISING (0.7743 -> 0.7942 full, 0.7805 -> 0.8101 OOS). But the IS chooser picks **p=0** there.
  **PARK**, not KEEP: a non-live panel, and not IS-choosable.

  **The split the record should carry: the DRAWDOWN gain is vol INFORMATION, the SHARPE is DISPERSION.**
  Against a dispersion-matched SHUFFLE null (200 seeds, the identical weight vector dealt to the held
  names in permuted order), MaxDD percentile reads **1.000 at 4 of 6 (panel, p) cells** (0.875 / 0.955
  on SMALL), but Sharpe reads **only 0.890-0.910 on B136** against 0.995-1.000 on U56 and SMALL.

  **RULE 8 (p chosen on warm-up..2016-12-31, 2017-2026 read once).** U56 picks p=0 (**+0.0000**), B136
  picks p=0 (**+0.0000**, leaving its DD fail standing), SMALL picks p=1.5 (+0.0942 but 4b **0 of 12**).
  H_HINDSIGHT does not even get a chance: the dial is **un-choosable on both 4b-passing panels**.
  4b: U56 **12/12**, B136 **9/12**, SMALL **0/12**. 4a **0 of 36** (live RULES v2's -12.05% MaxDD stays
  out of reach for a growth book). Gates **8/8**, offline, deterministic, 63 s, 36 cells + 30 bootstrap
  rows + 6 nulls all published. **No memo and no RULES change** (PARK, not KEEP).

## 2026-09-19 — ideas 1358 + 1366 (lane cloud): two attacks on the incumbent's SOLE binding 4b leg (the MaxDD cap). **ONE WORKS AND IS NOT ALPHA; ONE BUYS THE DRAWDOWN AND CANNOT AFFORD IT.**

  **1358 — PAY THE RESIDUAL A COUPON, NOT ZERO. 4b KEEP-CANDIDATE for the SUBSTITUTION, rule-8
  KILL for the DIAL.** Every de-grossed book in the record (1296, 1346, 794, 1297) parks its
  uninvested gross in CASH at 0%/yr. Routing it to **SHY** instead moves U56 at the frozen gross
  0.60 from **13.67% / 1.1717 / −16.38%** to **14.24% / 1.2182 / −16.00%**, OOS **15.15% / 1.1965**
  to **15.91% / 1.2500** — strictly dominating the incumbent on Sharpe, CAGR and MaxDD at once and
  passing every 4b leg full AND OOS. It is the ONLY resolvable effect on the axis: against
  vol-matched CASH twins drawn from a 14-rung 0.35–1.00 control ladder, a paired 63-row block
  bootstrap (400 reps, seed 20260919) puts SHY beyond 2 SE at **9 of 9** cells FULL and **9 of 9**
  OOS; IEF **0 of 9 / 0 of 9**; TLT **0 of 9** and OOS-NEGATIVE at **9 of 9**. But it is a
  MEASUREMENT CORRECTION, not an edge: SHY is what idle cash earns, the gain scales with
  (1 − gross) (+0.069 / +0.047 / +0.023 of Sharpe at g 0.50 / 0.60 / 0.75) and vanishes at gross
  1.00. **As a tuned dial the axis is a rule-8 KILL**: the IS chooser picks IEF / IEF / TLT and
  loses **0.0082** of mean OOS Sharpe against doing nothing, never finding SHY — which is the
  ex-post best OOS cell on **3 of 3** panels. Duration is a 2009–2016 mirage: TLT costs the U56
  book **−14.9% in 2022** against cash's −1.6%, and its own standalone OOS Sharpe is **0.0005**.
  4a KILL (H2 1.177 vs the live book's 1.1808). SMALL fails 4b at 0 of 12 with or without a
  sleeve. Memo `research/backtests/2026-09-19_bond-sleeve-residual_MEMO.md` with exact RULES
  wording; **not recommended for enactment on its own** (it changes no selection and no exposure,
  so it can ride the next RULES change), but the record needs the note that every published
  de-grossed book understates itself by (1 − gross) x the T-bill return.

  **1366 — RELEASE THE H=126 HOLD ON LOSS OF ELIGIBILITY. KILL on U56, PARK for MA on B136.**
  The incumbent makes a name immune from replacement for 126 trading days whatever it does, and
  that exposure is now a number: **HOLD carries 14.48% / 15.57% / 30.61% of ALL held name-weeks on
  names that FAIL the book's own eligibility test** on U56 / B136 / SMALL at H=126, rising to
  19.61% / 20.40% / 36.47% at H=189 (gate G2 confirms ELIG carries 0). Removing it works exactly
  as advertised on drawdown — **mean +5.59 pp SHALLOWER MaxDD** against turnover-matched HOLD
  twins on an 11-rung H 21–252 control ladder, U56's room to the 4b DD cap going +3.85% → +7.02% —
  **and that is the problem**: it pays in CAGR, and the CAGR floor is the leg that then binds
  (U56 ELIG@H126 **10.17%** against the 10.59% floor). As a Sharpe effect it is **UNRESOLVED**:
  |t| > 2 at **3 of 18** cells full and **1 of 18** OOS, and that one sits on SMALL, which fails 4b
  at 0 of 9 regardless. Rule 8 picks HOLD@H189 / MA@H126 / ELIG@H189 for **+0.0537** mean OOS
  Sharpe but **−0.0394 on U56**, where the ex-post best OOS cell IS the incumbent. 4a 0 of 27.
  **The one robust secondary finding: an MA-ONLY release dominates a full-eligibility release
  everywhere (4b full+OOS 6 of 9 vs 2 of 9) — the vol20 < 0.60 gate ejects names in high-vol
  RALLIES and belongs to ENTRY, not to EXIT.** No memo (not a KEEP), no RULES change.

  **BOTH RUNS:** offline, deterministic, ~10s each; 36 + 27 cells, 42 + 33 controls, 27 + 18
  bootstrap rows, all published. Gates 7/7 each, including a cross-script replay of ideas
  1296/1346's committed (gross 0.60, W) anchors to **4.4e-16 / 1.1e-16 / 8.3e-17** on U56 / B136 /
  SMALL. RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py untouched. Survivorship (rule 9):
  U56 / B136 / SMALL are current-constituent lists; for 1366 that bias runs AGAINST the clause
  (names delisted after breaking down are absent), so the value of exiting is understated, not
  overstated.

## 2026-09-19 — idea 1196 (lane C): should a committed MC FIGURE state its PAIR FORM before its SEED? **YES — AND THE MIGRATION IS FREE.**

  **VERDICT: ANSWERED (schema) + KILL as a capital finding.** The record holds **470 committed pair
  statistics**, of which **76 (0.1617) are recoverable today**. The binding leg is the KERNEL, not the
  seed and not the artefact: every LINEAR pair statistic is recoverable from pooled means by
  construction (1191 G2, re-confirmed here at 5.55e-17) although only 0.108 of them ever stated a
  seed, while only **11 of 145 NONLINEAR ones (0.076)** still own the per-draw CSV they would need.
  **0.553 of pair units cannot be classified from their own text at all.** No RULES change, no
  PROTOCOL edit (rule 6); RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py untouched. Offline,
  deterministic, 327 s.

  **THE INSTRUMENT.** Two dials (rule 4, both named by the queue): **CLAIM SET {C_STRICT, C_PROX,
  C_ALL} x KERNEL CLASS {LINEAR, NONLINEAR, UNCLASSIFIED}**, all 9 cells published. Corpus 35,100
  committed text units; 6,950 CSVs, 479 with a per-draw column. Capital arm: 24 real books
  (3 panels x N {10,12,20,30} x cadence {W,M}, gross 0.75, 10 bps, next-day execution) each against
  a 200-draw gross-matched null pool read IS-only — 4,800 null backtests.

  **1. DIAL 1 MOVES THE DENOMINATOR AND THEN STOPS MOVING THE NUMERATOR.** MC-derived units run
  3,215 / 6,695 / 27,046 across the three claim sets, but **C_PROX and C_ALL hold the SAME 470 pair
  units**, because the pair test itself requires a generator or null token. The same shape as 1191's
  "39 at every claim set", reached from the other side.

  **2. THE CAPITAL ANSWER: RETIRING THE UNRECOVERABLE FORM CHANGES NO PURCHASE.** Four choosers
  fitted on warm-up..2016-12-31, 2017-2026 read ONCE. **CH_DIFF (linear, recoverable) and CH_PCT
  (the record's percentile, not recoverable) pick the same book at 14 of 15 (panel, K) cells and
  read the same mean modal OOS Sharpe to four decimals — 0.8481 both**; the single disagreement is
  SMALL at K=200 and is worth **0.0003** of OOS Sharpe. Class means read LINEAR 0.8984 vs NONLINEAR
  0.8511, but that gap is carried **entirely by CH_Z** (0.9488 against 0.8481 / 0.8481 / 0.8541), the
  only chooser that divides by the pool's own SD. **Published as a standardisation fact, not as a
  kernel-class fact.**

  **3. THE RECORD'S PERCENTILE FORM CANNOT RANK.** CH_PCT is tied at its maximum on **5.76 of 8**
  anchors (U56) and **6.93 of 8** (B136) — 1191's saturation — so its "pick" is the deterministic
  first-wins tie-break; the linear forms tie at 1.00 of 8 everywhere. Tied counts published; a random
  tie-break would have manufactured the instability being measured.

  **4. WHAT RE-PUBLICATION COSTS.** Pooled/linear form 10.4 us, exact-pair form 101.4 us (9.8x), the
  200-draw pool **28.4 s = 2.8e5x the pairing**. The 39 C_STRICT linear units cost **nothing** (already
  exact); the 11 recoverable nonlinear ones **0.0011 s**; the 79 lost ones need their pools rebuilt at
  **0.62 compute-hours**. **The record's irreproducibility was never bought with compute; it was bought
  with a missing sentence.**

  **5. A GATE THAT FAILED, PUBLISHED NOT ABSORBED.** G3 — two mirrored pools with identical mean and
  sd whose percentile against the same book differs — was pre-declared at the incumbent cell
  U56/N=20/W and reads exactly **0** there: that book beats all 200 draws, so both pools read
  percentile 1.000. The gate failed on **saturation**, not on the mathematics, which is the same
  defect section 3 prices. The proposition was then tested where it is testable (G3b, interior cell
  chosen mechanically as argmin|pct-0.5|; G3c, a synthetic pair needing no tape: identical mean 0.000
  and sd 1.154701, percentiles 0.50 vs 0.75) and both hold.

  **6. BOOKS.** 3 of 24 clear 4b full+OOS, 0 of 24 clear 4a: U56 N=20/W (the standing 2026-09-04
  incumbent, 14.23%/1.1448/-19.39%, halves 1.217/1.100, OOS 15.65%/1.1660/-19.39%), U56 N=30/W (OOS
  14.02%/1.2276/-18.31%) and U56 N=30/M (OOS 14.43%/1.2180/-18.13%). The only rule-8-reachable pass
  is the incumbent, reached by CH_Z — **confirmatory, not generative**, and no chooser's pick beats
  the live book's OOS Sharpe (1.2769 on U56). SURVIVORSHIP (rule 9): U56/B136 are current-constituent
  lists and SMALL is a current screen output, so every LEVEL is optimistic and every 4a/4b count an
  UPPER bound.

  **RECOMMENDATION (not enacted — rule 6).** A committed MC figure should state its **kernel class**
  before its seed, and a LINEAR one should be published as its pooled means: *"Any figure computed
  from paired draws states its kernel. A kernel whose pair-mean is a function of the pooled means is
  published AS those pooled means (no seed, no draw order). Any other kernel publishes its per-draw
  artefact."* Priced here at 0.62 compute-hours and 0.0003 of OOS Sharpe.

## 2026-09-19 — idea 1298 (lane C): how STALE can the incumbent's SIGNAL be before its 4b PASS dies? **THREE DAYS — AND IT DIES ON DRAWDOWN, NOT ON RETURN.**

  **VERDICT: ANSWERED, with a standing CAVEAT on the 2026-09-04 book and a KILL of the lag as a
  dial.** The frozen incumbent (U56, N=20, H=126, gross 0.75, weekly, 10 bps) clears 4b when traded
  1, 2 or 3 rows late and FAILS at 5, 10 and 21 — with the MaxDD cap the SOLE binding leg at every
  failing rung. Its drawdown room runs **+1.101 / +0.156 / +0.160 / -0.365 / -0.839 / -0.870 pp**
  at d = 1 / 2 / 3 / 5 / 10 / 21 while the CAGR leg never binds (+4.9 to +5.3 pp) and the Sharpe
  legs never bind on U56. **The whole 4b pass rests on 1.10 pp of drawdown room, and one week of
  trading late costs 1.47 pp of drawdown.** Staleness does not stop this book earning; it makes it
  take a deeper drawdown, and 4b's cap is where that lands. No RULES change, no PROTOCOL edit
  (rule 6); RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py untouched. Offline,
  deterministic, 11s.

  **THE INSTRUMENT.** Two dials (rule 4): **LAG {1, 2, 3, 5, 10, 21} x PANEL {U56, B136, SMALL}**,
  18 cells per construction, **all 36 published** in `.grid.csv`, everything else frozen at the
  incumbent. d = 1 IS PROTOCOL rule 2.

  **1. THE DECAY IS NOT RESOLVABLE, SO THE PASS/FAIL FLIPS ARE NOT FINDINGS.** A paired
  circular-block bootstrap (400 reps x 63-row blocks, seed 20260919, both books resampled on
  IDENTICAL blocks) puts **0 of 36 rungs beyond 2 SE** of d = 1 in Sharpe. Worst |t| on the anchor
  ladder is -1.25 (U56/LATE, d = 5); worst anywhere +1.92. The U56 ladder IS ordered — rho
  **-0.886**, OLS **-0.00156** Sharpe per day of staleness — but its entire spread (0.0333) is
  **1.49x** the median rung SE. Pre-declared outcome **(C) UNRESOLVED**. The honest reading is NOT
  "the book survives three days": the tape cannot resolve what staleness costs in Sharpe, while
  what it costs in drawdown is monotone (-0.95 / -0.94 / -1.47 / -1.94 / -1.97 pp) and is enough to
  break 4b by d = 5. Every 4b flip along this axis — **idea 1287's included** — is a coin flip.

  **2. A RECORD DEFECT, FOUND BY TRYING TO REPLAY 1287.** The record now contains TWO incompatible
  definitions of "execution lag": **LATE** (decide on the weekly close, TRADE d rows later — this
  idea's own wording) and **SNAP** (trade on the fixed next row with a d-row-old snapshot — idea
  1287's `build1`). They are identical at d = 1 and different books at d >= 2, by **up to 0.1051
  of Sharpe (B136, d = 21)** against a median rung SE of 0.0498 — **2.1x the measurement noise and
  larger than either ladder's own spread**. U56's 4b verdicts disagree rung for rung: LATE passes
  at d = 1, 2, 3; SNAP passes at d = 1 and 5 only. SNAP replays 1287's committed rows to **3.4e-2**
  (most cells ~1e-3) against LATE's **1.0e-1**, a factor 3.0, which settles the attribution: 1287's
  non-monotone ladder was its CONSTRUCTION plus unresolved noise, not the tape. **A committed lag
  claim that does not name its construction is uninterpretable** — filed as a schema finding, both
  arms published whole, nothing selected on the convention (it is a replication control, not a
  third dial).

  **3. RULE 8 — THE LAG IS A KILL AS A DIAL.** Chosen on warm-up..2016-12-31 by IS Sharpe (ties to
  the lower lag), 2017-2026 read ONCE, against PROTOCOL's frozen d = 1: IS picks d = 21 / 2 / 10
  (LATE) and 10 / 3 / 10 (SNAP) on U56 / B136 / SMALL. **Chooser-minus-do-nothing: mean -0.0114 OOS
  Sharpe over the six arms, worst -0.0618, positive on 3 of 6**, and the IS pick is the ex-post best
  OOS lag on **0 of 6**. Every selecting IS margin (+0.0066 .. +0.1164) is inside its own rung SE.
  PROTOCOL rule 2's frozen d = 1 stands, and not because it is safe — because nothing else is
  choosable.

  **4. THE ANCHOR GATE, REPORTED NOT EXPLAINED AWAY.** (U56, d=1) reads 15.82% / 1.1543 / -19.13%,
  OOS 17.34% / 1.1862 against the committed 15.79% / 1.1529 / -19.13%, OOS 17.30% / 1.1837 — worst
  |diff| **2.5e-3**, which MISSES a 5e-4 exact replay and sits INSIDE the tape-vintage floor (idea
  1335 measured ~7e-3 of half-sample movement from one daily rewrite; commit 4e19a80 rewrote
  `data/prices*.csv` on 2026-09-18). Every cell here is on ONE tape, so the within-run comparisons
  are unaffected; only cross-run comparisons carry the floor and are labelled where they appear.
  4a fails at 36 of 36 cells; 4b passes 3 of 18 under each construction.

  **WHAT THIS DOES TO THE STANDING BOOK.** It does not refute the 2026-09-04 candidate at d = 1; it
  prices how thin that pass is. 1.10 pp of drawdown room is less than the drawdown one week of late
  trading adds, and is itself the same order as what a single tape rewrite has been shown to move.
  Survivorship (rule 9) makes it worse, not better: U56 is a current-constituent list, so the
  drawdown is flattered and 1.10 pp is an upper bound on the room a real account would have.

## 2026-09-18 — idea 1354 (lane cloud): is WEEKLY still the CADENCE ARGMAX at EVERY N? **ONLY AT 15 — and the run turned up a KEEP-4b CANDIDATE.**

  **VERDICT: ANSWERED — the cadence argmax MOVES WITH N on 3 of 3 panels and W holds it in only
  4 of 12 (panel, N) cells, so idea 1335's "weekly wins" is an N=15 FACT, NOT a cadence fact.
  PLUS a KEEP-4b candidate: U56 (N=30, QUARTERLY) at gross 0.60 passes 4b on every full-sample
  AND every OOS leg, replicates on B136, and is the rule-8 IS argmax on U56 — but the IS margin
  that selects it is +0.00031, so it is MEMO'd and PARKED, not swapped.** SELECTION: every
  numbered item still standing at the bottom of '## Open' (903 / 896 / 895 / 894 / 877 / 876,
  and above them 353, 429 and the 687..532 block) is a census of committed TEXT or NUMBERS with
  no book to price, or needs live / local data this sandbox has no network for, so none can carry
  the mandatory rule-8 walk-forward or either KEEP path; each of the bottom eight is annotated
  SKIP in place. This run therefore filed 3 new price-only ideas stress-testing the KEEP-4b
  candidate — **1346** (gross x cadence, to buy back B136's monthly DD leg), **1350** (is the
  standing pass TAPE-VINTAGE robust), **1354** (N x cadence) — and claimed the LAST of them.
  No RULES change, no PROTOCOL edit (rule 6); RULES.md, PROTOCOL.md, scan.py, bot.py and
  baseline.py untouched. Offline, deterministic, 17s. (The run crossed into 2026-09-19 UTC while
  writing up; every file is stamped 2026-09-18, the date of the claim and of the tape's last row.)

  **THE INSTRUMENT.** Two dials (rule 4): **N {10, 15, 20, 30} x CADENCE {D, W, 2W, M, Q}** = 20
  cells per panel, **all 60 published** in `.grid.csv`, at the frozen incumbent (3-leg composite,
  above-200d AND vol20 < 0.60, equal weight, H=126 min hold, gross 0.60, t+1) with COST frozen at
  PROTOCOL's 10 bps — 1335 had already shown the cadence ranking is invariant to the cost rung on
  all three panels, so re-sweeping it would add a third dial and no information. Gate **G1: the
  (N=15, W) cell replays 1335's committed U56 W/10bps row to < 5e-6 on all eight statistics
  including turnover; 9 of 9 asserted gates pass**, plus 3 published tape stamps.

  **1. THE ANSWER.** Full-sample Sharpe argmax over the 5 cadences, at N = 10 / 15 / 20 / 30:
  **U56 M, W, W, Q** (1.1210 / 1.1717 / 1.1532 / 1.2097); **B136 M, M, M, W**; **SMALL M, W, 2W,
  2W**. Moves on **3 of 3 panels**; W holds it in **4 of 12** (panel, N) cells and, out of sample,
  ranks 1 of 5 in only **2 of 12**. Against 1335's finding that the SAME argmax is perfectly
  stable across the whole 0-50 bps cost ladder on all three panels, the reading is sharp: **the
  cadence coordinate is robust to what the tape charges and fragile to how wide the book is.**
  U56 N=20 is the one near-tie (W 1.153200 vs Q 1.151634, +0.00157, and it REVERSES out of
  sample: Q 1.188840 vs W 1.185065) — below resolution, so read as indistinguishable.

  **2. WHICH DIAL BINDS.** Mean within-panel Sharpe spread, CADENCE vs N: **U56 0.1490 / 0.0974
  (1.53x), B136 0.1062 / 0.0661 (1.61x), SMALL 0.2112 / 0.1465 (1.44x)**; OOS 1.43x / 1.45x /
  2.11x. Cadence commands 1.4-1.6x the spread N does on every panel and in both windows — and yet
  WHICH cadence wins is decided by N. **The two dials interact; neither is a nuisance parameter
  for the other**, which is exactly how the record keeps producing coordinates nobody chose.

  **3. THE KEEP-4b CANDIDATE — U56 (N=30, QUARTERLY), gross 0.60, 10 bps.** Three cells beat the
  frozen (15, W) incumbent on full-sample Sharpe AND pass 4b full+OOS: U56 (30, Q) +0.0380,
  B136 (30, W) +0.0264, B136 (20, W) +0.0011. Only the first also wins out of sample, and it is
  the rule-8 IS argmax on U56. **U56 (30, Q): 12.23% / 1.2097 / -18.21%, halves 1.2543 / 1.1945;
  OOS 13.93% / 1.2610 / -18.21%.** All four 4b legs pass full sample with **2.02 pp of drawdown
  room** (-18.21% vs the -20.23% cap) and **1.64 pp of CAGR room** (12.23% vs the 10.59% floor)
  against SPY's 15.12% / 0.8844 / -33.72%, and all four hold out of sample. **+0.0645 of OOS
  Sharpe over the frozen incumbent for -1.22 pp of OOS CAGR.** It **replicates on B136** (11.50% /
  1.0332 / -18.81%, OOS 12.49% / 1.0461 / -18.81%, 4b all four legs full and OOS) and carries the
  **lowest turnover in the entire grid, 1.05/yr** against the incumbent's 2.46 — by 1335's cost
  ladder, the cell least exposed to the cost rung. It is **not an isolated cell**: the U56 Q
  ladder rises monotonically in N in both windows (Sharpe 0.9528 -> 1.0292 -> 1.1516 -> 1.2097;
  OOS 0.9611 -> 1.0110 -> 1.1888 -> 1.2610). **H_HINDSIGHT does NOT fire on U56** — the IS pick IS
  the ex-post best OOS cell, which is rare in this record.

  **WHY IT IS PARKED AND NOT SWAPPED, stated plainly.** (i) **The selection is not decidable**:
  its IS Sharpe is 1.148502 against the incumbent's 1.148194, a margin of **+0.00031**, roughly
  1/23rd of the ~7e-3 half-sample resolution floor idea 1335 measured TODAY from a single daily
  tape rewrite — rule 8's argmax here is a coin flip, and the N-gradient along Q is the only real
  evidence. (ii) It **fails outright on SMALL** (0 of 4 legs, -30.41% MaxDD), so this is a
  large-cap fact. (iii) It is **1 cell of 60** with no multiplicity correction. (iv) It **buys
  Sharpe with 1.44 pp of full-sample CAGR** (12.23% vs 13.67%). (v) **Quarterly means 75
  rebalance decisions in 18.7 years and the PHASE inside the quarter is unpriced** — a larger dial
  at Q than at W, which is what idea 1253 is currently asking of the weekly book. The memo's
  recommendation is therefore: price the quarterly phase dial and re-confirm on a second tape
  vintage BEFORE any Sunday swap; if both hold, this is the strongest 4b candidate the record has,
  because it buys Sharpe with LESS trading rather than more risk.

  **4. RULE 8 (the (N, CADENCE) PAIR chosen on warm-up..2016-12-31 by argmax IS Sharpe; 2017-2026
  read ONCE).** U56 picks **(30, Q)** -> OOS 13.93% / 1.2610 / -18.21% (4b OOS PASS, +0.0645 vs
  the frozen incumbent); B136 picks (10, W) -> 13.48% / 0.9186 / -16.41% (4b OOS PASS but
  **-0.1201** vs the incumbent); SMALL picks (30, M) -> 3.89% / 0.3317 / -29.55% (4b FAIL on
  Sharpe, DD and CAGR, -0.1411). The IS chooser lands on the frozen incumbent on **0 of 3**
  panels; choosing the pair is worth a mean **-0.0656 of OOS Sharpe** and -1.42 pp of OOS CAGR and
  beats the incumbent on **1 of 3**. 4b on every OOS leg after rule 8: **2 of 3**.

  **5. KEEP-PATH CENSUS.** **4a 0 of 60.** **4b 22 of 60 full-sample and 22 of 60 full AND OOS**
  (U56 16/20, B136 6/20, SMALL 0/20). By cadence: D 2/12, W 8/12, 2W 2/12, M 4/12, Q 6/12 — **W
  still passes 4b most often even where it is not the argmax**, because the cells that out-Sharpe
  it mostly do so by taking drawdown.

  **SURVIVORSHIP (rule 9).** U56 / B136 / SMALL are CURRENT-constituent lists; SMALL is a sub-$2B
  screen carried back to 2010 with the mandated 52 `max_1d_move >= 1.0` tickers dropped (663 of
  715 kept) and fails 4b on all 20 of its cells. A current-constituent large-cap list flatters a
  WIDE momentum book, so the (30, Q) candidate's CAGR is the number the bias inflates most; its
  drawdown margin, which the memo leans on, is the less affected leg.

  **TAPE STAMP (published, not asserted).** U56 4708 rows and B136 4708 rows,
  2008-01-02..2026-09-18; SMALL 4203 rows, 2010-01-04..2026-09-18. Every number above is on this
  vintage of `data/prices*.csv` and on no other.

## 2026-09-18 — idea 1335 (lane cloud): is WEEKLY the CADENCE ARGMAX for the INCUMBENT, or just PROTOCOL's DEFAULT? **IT IS THE ARGMAX. KILL as a dial.**

  **VERDICT: ANSWERED, and the queue's own rationale FALSIFIED — the cadence argmax does NOT
  move with the cost rung on ANY of the three panels, so the committed numbers in this family
  are NOT a 10-bps artifact.** SELECTION: 1335 was the FIRST numbered item standing in '## Open';
  price-only, eligible, claimed and pushed before any compute. No RULES change, no PROTOCOL edit
  (rule 6); RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py untouched. Offline,
  deterministic, 35s.

  **THE INSTRUMENT.** Two dials (rule 4): CADENCE {D, W, 2W, M, Q} x COST {0, 10, 25, 50} bps =
  20 cells per panel, **all 60 published** in `.grid.csv`, at the record's frozen incumbent
  (3-leg composite, above-200d AND vol20 < 0.60, N=15 equal weight, H=126 min hold, gross 0.60,
  t+1). Gross returns and turnover are cadence properties, so each (panel, cadence) is run ONCE
  and every rung is read off the same pair — the grid is exact, not interpolated. 2W is the
  engine's own W array subsampled every second entry, never a phase shift.

  **1. THE ARGMAX IS STABLE ACROSS THE WHOLE COST LADDER.** Full-sample Sharpe argmax at
  0 / 10 / 25 / 50 bps: **U56 W, W, W, W** (1.1931 / 1.1717 / 1.1394 / 1.0855); **B136 M, M, M,
  M**; **SMALL W, W, W, W**. Moves on **0 of 3 panels**; W is the argmax in **8 of 12** (panel,
  rung) cells. The rung moves every LEVEL and no RANKING. What it does move is the size of
  B136's M-over-W gap, monotonically in M's favour: **+0.0261 / +0.0320 / +0.0408 / +0.0554** —
  the rebate reading, priced, and still not enough to flip an argmax anywhere.

  **2. WEEKLY IS EARNED ON THE PANEL THAT MATTERS.** OOS Sharpe order at 10 bps: U56 **W 1.1965**
  > 2W 1.1251 > M 1.0902 > D 1.0769 > Q 1.0110 (**W ranks 1 of 5**); B136 M 1.1196 > W 1.0387
  (2 of 5); SMALL 2W 0.5750 > W 0.4728 (2 of 5). PROTOCOL's inherited default is simultaneously
  the full-sample argmax at every rung and the OOS argmax on U56 — the only panel this family
  has ever cleared 4b on. Idea 1305's W->M sign reproduces on all three panels (-0.1061 /
  +0.0320 / -0.1427 against its -0.1053 / +0.0283 / -0.0796, gate G2); turnover is monotone
  D >= W >= 2W >= M >= Q on all three (G3), U56 3.39 / 2.46 / 2.12 / 1.86 / 1.41 per year, with
  the W->M refund +6.0 bp/yr at 10 bps and +30.2 at 50.

  **3. B136's BETTER CADENCE IS UNBUYABLE.** M beats W on B136 at every rung full-sample and by
  +0.0809 out of sample, and is the ex-post best OOS cadence there — but it **fails 4b on the
  drawdown leg at every rung, MaxDD -22.76% against the -20.23% cap (0.60 x SPY's -33.72%), a
  2.53 pp miss**, while W on B136 passes all four legs at -15.97%. D and 2W fail the same leg.
  **4a 0 of 60. 4b 23 of 60 full-sample and 23 of 60 full AND OOS** (U56 19/20, B136 4/20,
  SMALL 0/20), and every U56 pass is the incumbent or a slower version no cell dominates.

  **4. RULE 8 (cadence chosen on warm-up..2016-12-31 by argmax IS Sharpe AT EACH RUNG,
  2017-2026 read ONCE).** The IS chooser picks PROTOCOL's W in only **4 of 12** cells. Choosing
  costs a mean **-0.0746 of OOS Sharpe** (min -0.2268, max +0.0010) and -0.75 pp of OOS CAGR,
  and beats W in **1 of 12** (B136 @50 bps, +0.0010). At 10 bps: U56 picks W -> 15.15% / 1.1965 /
  -16.38% (4b OOS PASS); B136 picks 2W -> 15.17% / 1.0230 / -21.85% (4b FAIL, DD); SMALL picks
  M -> 2.85% / 0.2525 / -32.36% (4b FAIL on Sharpe, DD and CAGR) against W's 6.38% / 0.4728.
  **4b on every OOS leg after rule 8: 4 of 12 — all four are the U56 rungs where the pick IS W**,
  so every surviving pass comes from NOT choosing. H_HINDSIGHT fires in **8 of 12**: the ex-post
  best OOS cadence is not the IS pick.

  **5. A RECORD-WIDE TAPE-VINTAGE CAVEAT, MEASURED BECAUSE A GATE FAILED.** The U56 W@10bps cell
  IS idea 1305's committed flat control and idea 1339's PROTOCOL_DEFAULT cell. This run replays
  its **MaxDD to 1e-8 and its IS-window Sharpe to 6.6e-7** (G1a — the construction is identical),
  but the tape-sensitive statistics land off the committed values: dCAGR +0.000129, dSharpe
  +0.001096, **dH1 -0.006378, dH2 +0.006984**, dOOS Sharpe +0.001826. Cause: commit **4e19a80
  "Daily close 2026-09-18" rewrote data/prices.csv, prices_broad.csv and prices_small.csv.gz
  wholesale (9410 lines replaced, +6 net rows) AFTER 1305 was committed** — 1305 ran on a tape
  ending 2026-09-17 / 09-11 / 09-11 (4707 / 4703 / 4198 rows), this run on 2026-09-18
  (4708 / 4708 / 4203) with the whole history re-adjusted (G1c). The declared 3e-3 replay
  tolerance **FAILS at 6.98e-3 and is published as a failure rather than widened**:
  cross-run replay of a HALF-SAMPLE Sharpe in this repo is resolution-limited to ~7e-3 by daily
  re-adjustment of `data/prices*.csv`, and **no committed number in this family carries a tape
  stamp.** The committed cell's verdict is unaffected (G1d: 4b PASS on all four legs, Sharpe
  1.1717 vs SPY 0.8844, MaxDD -16.38% inside the cap). Gates 11 of 12, the twelfth diagnosed.

  **SURVIVORSHIP (rule 9).** U56 / B136 / SMALL are CURRENT-constituent lists; SMALL is a
  sub-$2B screen carried back to 2010 with the mandated 52 `max_1d_move >= 1.0` tickers dropped
  (663 of 715 kept), so its LEVELS are an upper bound and only its cadence CONTRASTS are read —
  its best cell (2W, OOS Sharpe 0.5750) still fails all four 4b legs.

  **NOTHING PROMOTED, NOTHING RETRACTED.** Weekly stays because it wins, not because nobody
  looked.

- 2026-09-18 (lane cloud, idea 1327 is-the-CHOOSER-STATISTIC-or-the-RE-PICK-CADENCE-the-binding-dial)
  — **VERDICT: KILL for real-time (N, H) re-selection, and the queue's premise FALSIFIED — the
  binding dial is the CHOOSER STATISTIC, not the cadence, and the switch-turnover bill is ~0.1
  pp/yr and often NEGATIVE.** SELECTION: 1327 is the LAST numbered item standing in '## Open';
  price-only, no eligibility descent taken. It is filed as conditional on 1323, which is still
  Open and unrun, so this run BUILDS 1323's real-time book itself (cell SHARPE x 1y) rather
  than assuming its result. No RULES change, no PROTOCOL edit (rule 6); RULES.md, PROTOCOL.md,
  scan.py, bot.py and baseline.py untouched. Offline, deterministic, 28.7s.

  **THE INSTRUMENT.** Two dials, STATISTIC {SHARPE, CAGR, MAXDD, MARGIN4B} x CADENCE
  {1y, 2y, 3y, 5y, NEVER} = 20 stitched books per panel, **all 60 published**, chosen over the
  record's own 24-cell N {5,10,15,20,30,40} x H {21,63,126,252} grid at the incumbent's frozen
  gross 0.60, weekly, 10 bps, t+1. The chooser reads an EXPANDING window of already-realised
  returns ending at the re-pick date; NEVER reproduces 1321's once-and-for-all pick. Switches
  are costed INSIDE the runner (drifted weights traded into the new cell's targets). MARGIN4B
  maximises min(Sharpe - SPY Sharpe, MaxDD - 0.60*SPY MaxDD, CAGR - 0.70*SPY CAGR) — a chooser
  aimed at what PROTOCOL actually grades. Comparands: frozen anchor N=15/H=126, GRIDAVG (the
  parked no-choice book), the unattainable full-sample ORACLE, RULES v2, SPY. Gates G0-G3 PASS
  (the grid contains its anchor bit-for-bit; 1321's N=5/H=63 replays as 15.22% / 1.0091 /
  -21.46%, 4b FAIL).

  **1. THE STATISTIC BINDS.** Mean OOS-Sharpe spread across STATISTICS vs across CADENCES:
  **U56 0.3665 vs 0.1675 (2.19x), B136 0.1214 vs 0.0505 (2.40x), SMALL663 0.6428 vs 0.4304
  (1.49x)**; sum-of-squares share stat **81.8 / 81.2 / 68.6%** against cadence 5.9 / 7.4 /
  11.2%. What the chooser maximises decides the book; how often it revisits is second order on
  every panel. On B136 the SHARPE and CAGR choosers pick the SAME cell at every cadence.

  **2. THE BILL IS NOT THE STORY.** Switch bill (cost drag minus the same statistic's drag at
  NEVER): **-0.096 / +0.012 / -0.082 pp/yr** (U56 / B136 / SMALL663), every cell inside
  ±0.27 pp/yr, **negative on two of three panels** — re-picking often lands on a LOWER-turnover
  cell, refunding cost rather than charging it. 1.7-3.4 switches per book over 7.2 picks.

  **3. THE BOOKS DO NOT EARN THEIR KEEP.** 4a **0 of 60**. 4b **10 of 60 full sample and 10 of
  60 OOS, all ten on U56**, and all ten under a grading-aligned statistic (MAXDD 4/5, MARGIN4B
  4/5, SHARPE 2/5, CAGR 0/5); B136 and SMALL are 0 of 20 each. **Exactly one of the 60 beats the
  frozen anchor's OOS Sharpe** — U56 MAXDD/3y, 14.43% / 1.1979 / -16.90% vs anchor 15.12% /
  1.1947 / -16.38%, a +0.0032 edge for -0.69 pp of CAGR — and rule 8 does not pick it.

  **4. RULE 8 (2017-2026 READ ONCE).** (STATISTIC, CADENCE) by argmax IS Sharpe on
  warm-up..2016-12-31. U56 picks MARGIN4B/1y -> OOS 13.70% / 1.0455 / -16.90% (4b PASS but
  **-0.1492 of OOS Sharpe against doing nothing**); B136 picks SHARPE/3y -> 16.43% / 0.9095 /
  -23.42%, **4b FAIL** on the DD cap, -0.1360 vs anchor; SMALL picks CAGR/1y -> 21.30% / 1.0517
  / **-38.27%**, buying +14.90 pp of OOS CAGR by missing the -20.23% cap by 18 pp. GRIDAVG stays
  the least-bad no-choice book (U56 OOS 13.48% / 1.1732 / -16.62%, still -0.0215 behind frozen).

  **5. IT ALSO ANSWERS 1323, IN THE NEGATIVE,** on 1323's own arm (SHARPE/1y): U56 OOS 12.48% /
  1.0017 / -16.63%, **-0.1929 of OOS Sharpe against the frozen cell it replaces**. 1323 stays
  Open for its own lane to claim; this is evidence filed against it, not a claim on it.

  **SURVIVORSHIP (rule 9).** U56 / B136 / SMALL663 are current-constituent lists; SMALL663 is a
  sub-$2B screen carried back to 2010 — its 21.30% OOS CAGR under a CAGR chooser concentrating
  into N=5 is precisely the number that bias inflates most, a further reason not to read that
  cell as an opportunity.


## 2026-09-18 — idea 1323 (lane B): does the 4b PASS survive ANNUAL REAL-TIME RE-SELECTION of (N,H)? **NO. KILL.**

  **The question, answered directly.** 1323 asked for the book an implementer could actually
  have run: re-pick (N,H) from the committed 24-cell grid (N {5,10,15,20,25,30} x H
  {21,63,126,252}, MAXVOL 0.60, GROSS 0.75, weekly, 10 bps, t+1) on an EXPANDING window every
  January, stitch the real equity curve with switch turnover costed, and score both KEEP paths
  and rule-8 OOS against the frozen anchor, RULES v2 and SPY. The literal book (ANNUAL /
  EXPANDING / argmax) fails 4b at every chooser statistic on every panel: U56 FAIL(H1,DD) at
  SHARPE, FAIL(DD) at CALMAR, FAIL(H2,OOS,DD) at CAGR; B135 and SMALL663 fail at all three.

  **Rule 8 (two dials, K and WINDOW, picked on 2011-2016 IS only; STAT held at SHARPE).**
  U56 picks k=24/EXPANDING (IS Sharpe 1.0992, top of the full 18-point ladder): OOS 17.18% /
  1.1703 / -20.56%, 4b FAIL on the DD leg alone, missing the -20.23% cap (0.60 x SPY's -33.72%)
  by 0.33 pp, against the frozen anchor's 17.28% / 1.1832 / -19.13% and SPY's 15.28% / 0.8747 /
  -33.72%. B135 picks k=1/EXPANDING: OOS 20.43% / 0.9144 / -28.62%, 4b FAIL(H2,DD). SMALL663
  picks k=16/EXPANDING: OOS 10.16% / 0.6308 / -37.31%, 4b FAIL(H1,H2,OOS,DD) — worse than SPY
  OOS on Sharpe and CAGR both.

  **THE NEW RESULT — churn is not the cause; selection variance is.** The run's content beyond
  1327 and 1331 is the K-LADDER that bridges their two extremes: k=1 is 1323's argmax, k=24 is
  1331's no-choice GRIDAVG (reproduced bit-identically, gate G7). Across all 54 rungs (9 K x 2
  WINDOW x 3 STAT) on every panel the switch-turnover bill never exceeds 0.089 pp/yr and is
  0.000 at k=24 — the real-time book is not being eaten by trading costs. What it is being
  eaten by is the variance of the pick itself: at STAT=SHARPE on U56, OOS Sharpe rises
  monotonically in k, 0.9583 (k=1) -> 1.0876 -> 1.1021 -> 1.1132 -> 1.1238 -> 1.1420 -> 1.1703
  (k=24), i.e. every unit of real-time choosing subtracts return. The monotone shape is
  CHOOSER-CONDITIONAL, not universal: it holds at 1 of 6 (WINDOW, STAT) pairs strictly and
  collapses under CALMAR/CAGR on SMALL663, where k=1 is the best rung. This is the same
  direction 1327 found (the STAT is the binding dial) measured on a different axis.

  **H_HINDSIGHT fires.** The frozen N=20/H=126 anchor beats ALL 54 real-time books on U56 OOS
  Sharpe (1.1832). Taken with 1321 and 1331, the record's position is now: every committed
  KEEP-4b is reachable only by freezing a cell nobody could have named in 2011, and the best
  implementable approximation (hold the whole grid, choose nothing) lands 0.33 pp of drawdown
  short of the 4b cap.

  **Four rungs do pass 4b on U56** — k=3/EXPANDING/CALMAR, k=4/EXPANDING/CAGR, k=1 and
  k=2/ROLL1260/SHARPE — and NONE of them is the rule-8 pick. Each passes the DD leg by at most
  0.33 pp of margin (-19.90% to -19.97% against the -20.23% cap) and they sit at scattered,
  non-adjacent (K, WINDOW, STAT) coordinates with no shared structure. They are reported, not
  banked: a 4-of-54 pass rate at sub-0.4 pp margins on a razor-edge leg is what selection noise
  looks like, and PROTOCOL rule 8 exists precisely so that such rungs are not promoted.
  B135 and SMALL663 pass 0 of 54.

  **GATES 11/11.** Including G1 (anchor replays the committed 15.7147% / 1.14804 / -19.1276%
  U56 triple to 6.0e-5 when vintage-pinned to 2026-09-16), G3 (chooser scores unchanged under
  IS-truncation), G6 (no row at or after a re-pick date is read), G7 (k=24 == GRIDAVG to 0.0),
  G8 (k=1 == plain argmax) and G10 (the switch cost is actually charged: the k=1 book's
  turnover/yr, 4.289, strictly exceeds the mean of its own held cells', 3.936).

  **SURVIVORSHIP (rule 9).** U56 / B135 / SMALL663 are current-constituent lists. Every absolute
  level is optimistic and every 4b pass is an upper bound. The headline is a DIFFERENCE between
  books built from the SAME names on the SAME days, so the k-ladder shape is first-order immune;
  the 4-of-54 pass count is not.

  **No RULES change.** RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py untouched.


## 2026-09-18 — idea 904 (lane B): which committed PLACEBO numbers are below their own SEED FLOOR? **ANSWERED (almost none can be scored at all) / CAPITAL ARM KILL.**

  **Why this run has a price leg.** Four lanes had skipped 904 as "a census, no book". Lane B's
  own idea 1265 overturned that premise, so this run gave 904 a real capital arm: a placebo-
  differenced statistic IS a selector, and the floor IS a licensing gate on it. 24 committed
  (N,H) books per panel (N {5,10,15,20,25,30} x H {21,63,126,252}, MAXVOL 0.60, GROSS 0.75,
  weekly, 10 bps, t+1) were scored against a gross-matched RAND null — the same machine with
  only the ORDERING randomised — at S = 5/10/20/50 seeds, and the pick was gated on k x the
  arm's own floor, k in {0, 0.5, 1, 2}. 48 cells, every one published.

  **THE FLOOR CONSTANT IS WRONG BY A FACTOR OF 1.95.** Idea 885's arithmetic assumed
  sigma ~ 0.067 of Sharpe. Measured here on 3,600 null books (24 arms x 50 seeds x 3 panels),
  the per-arm null-Sharpe dispersion is **sigma_hat = 0.1307** (panel means 0.1077 U56 / 0.1086
  B136 / 0.1759 SMALL). Every floor the record computed from 0.067 is understated about
  two-fold, so every "this number is resolvable" claim built on it is optimistic by the same
  factor. The typical per-arm floor is 0.0733 / 0.0518 / 0.0366 / 0.0232 of Sharpe at
  S = 5/10/20/50, and 3 to 8 of each panel's 24 arms have a placebo excess smaller than their
  own floor even at 50 seeds.

  **THE CENSUS ANSWER — the record cannot ask 904 of itself.** Over research/backtests/*.md and
  CHANGELOG.md (LEADERBOARD.md and QUEUE.md excluded by declaration: their 4-dp numbers are
  Sharpe LEVELS): 306 placebo-cued sentences under the NARROW cue, of which 19 carry a >=4 dp
  decimal, 13 are DIFFERENCES (|x| < 0.1), and **1** carries both a seed count and an arm count.
  Under the WIDE cue: 386 -> 22 -> 17 -> **2**. So 7.7% (NARROW) / 11.8% (WIDE) of the record's
  committed placebo-differenced numbers are scoreable against their own floor AT ALL; the rest
  are unstamped, and imputing counts for them would be inventing the answer. Of those that can
  be scored, 1 of 1 and 2 of 2 sit INSIDE k = 1 x their own floor. The funnel IS the finding:
  the defect is not that the record's placebo numbers are below the floor, it is that they do
  not carry the two integers needed to find out.

  **THE CAPITAL ANSWER — KILL, on both the statistic and the gate.** Rule 8 (S, k picked on
  warm-up..2016 by argmax IS Sharpe of the selected book; 2017-2026 read ONCE):
  U56 S=5/k=0.0 -> (5,63), OOS 17.95% / 0.8996 / -26.26%; B136 S=10/k=0.0 -> (5,63), OOS
  20.43% / 0.9144 / -28.62%; SMALL S=10/k=0.0 -> (10,252), OOS 17.35% / 0.8590 / -42.63%.
  4a 0 of 48, 4b 0 of 48, OOS 4b 0 of 48 — the DD leg fails everywhere. Against the RAW
  IS-Sharpe chooser the placebo chooser wins 16 of 48 cells OOS, and all 16 are SMALL
  (0 of 16 on U56, 0 of 16 on B136).

  **THE FLOOR GATE IS AN INERT DIAL.** k changes the pick in **0 of 12** (panel, S) groups and
  0 of 48 cells ever fell back to the raw chooser, although the licensed set shrinks from 18-22
  arms at k=0 to 9-20 at k=2 (SMALL 7-9 down to 2-4). Only S moves the pick, and it moves it
  between exactly two arms per panel. Gating a chooser on its own resolution buys nothing
  because the arms the gate removes are never the argmax.

  **THE MECHANISM — placebo-differencing is a CONCENTRATION BIAS, not a neutral correction.**
  Mean placebo excess falls monotonically in N (U56 +0.1913 at N=5 -> +0.0289 at N=30; B136
  +0.2919 -> +0.0627) while mean OOS Sharpe RISES monotonically in N (U56 0.9456 -> 1.1237;
  B136 0.9301 -> 1.0254). A random 5-name portfolio is a terrible null, so subtracting it
  rewards exactly the arms that lose out of sample. Spearman(IS placebo excess, OOS Sharpe)
  over the 24 arms is **-0.765** on B136 and **-0.274** on U56 (raw IS Sharpe: -0.724 and
  +0.192); only on SMALL, where the composite's mean excess is NEGATIVE (-0.0419, i.e. the
  live score loses to coin-flipping on that panel), does the statistic help (+0.582) — and
  even there it is beaten by the raw IS Sharpe (+0.803). The record's standing habit of
  reporting a gross-matched null difference as the "clean" number is therefore not clean: on
  a grid that contains a size dial it imports a size preference of its own.

  **H_HINDSIGHT fires again.** The frozen N=20/H=126 anchor on U56 — 15.78% / 1.1522 / -19.13%
  full, OOS 17.28% / 1.1832 / -19.13%, 4b PASS on all four legs — beats all 16 placebo-chooser
  cells, the raw chooser (0.8996) and the no-choice GRIDAVG (1.1676) out of sample. Consistent
  with 1321 / 1323 / 1331: every chooser the record builds loses to the cell nobody had to
  choose. Reported, not claimed.

  **GATES 5/5**: G0 sample >= 10y; G1 the null shares every argument with its real arm except
  the ordering; G2 the chooser reads no row at or after 2017-01-01 (null frames built with
  stop=i_oos); G3 sigma measured, not assumed; G4 all 48 cells published; G5 exactly two tuned
  parameters (S, k).

  **SURVIVORSHIP (rule 9).** U56 / B136 / SMALL are current-constituent lists, so every absolute
  level is an upper bound. The headline is a DIFFERENCE between choosers built from the SAME
  names on the SAME days and the N-monotonicity is a within-panel shape, so both are
  first-order immune; the 4b pass count is not.

  **No RULES change.** RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py untouched.


## 2026-09-19 — idea 1350 (lane B): is the 2026-09-04 KEEP-4b pass TAPE-VINTAGE ROBUST? **ANSWERED — YES within the post-fix era / KEEP-4b CONFIRMATION (U56), no new book.**

  **The defect this closes.** Idea 1335's gate G1b replayed a committed cell to 1e-8 on the full
  sample but FAILED by 6.98e-3 on its HALVES, because commit 4e19a80 rewrote data/prices*.csv
  wholesale after idea 1305 had committed the same cell. No committed number in this family
  carries a TAPE STAMP, and the standing candidate sits only 1.10 pp inside a hard DD cap.
  14 vintages of data/prices.csv are recoverable from this repo's own history (14 DISTINCT
  blobs, 2026-09-03..2026-09-18, read offline with `git show`, with prices_broad.csv /
  prices_small.csv.gz taken as of the same commit). 3 panels x 2 readings x N {10,16,20,25} x
  H {63,126,252} = **912 books**, every one published.

  **THE VERDICT SURVIVES THE TAPE.** The frozen 2026-09-04 book (N=20, H=126, gross 0.75,
  weekly, 10 bps, t+1) clears 4b on **12 of 12** post-fix vintages on both readings. Head
  vintage (4e19a80d): 15.80% / 1.1537 / -19.13%, halves 1.2067 / 1.1203, OOS 17.32% / 1.1857 /
  -19.13%; SPY 15.12% / 0.8844 / -33.72%, OOS 0.8738. Across the 12 the anchor spans
  15.71..15.82% CAGR and 1.1480..1.1544 Sharpe at a MaxDD of -19.13% (spread 8.2e-7).

  **THE MARGINS BARELY MOVE, AND THE BINDER MOVES LEAST.** Restatement-only (V_TRUNC, every
  vintage cut to the common end date, so only rewrites of overlapping rows can act): every 4b
  margin spreads by <= **1.05e-4** and full Sharpe by **5.2e-6**. The drawdown-cap margin — the
  leg the record calls the modal binder — is **+1.1028 pp against a 1.05e-4 pp spread**, a
  margin-to-spread ratio of **10,521**. The 2020/2022 drawdown sits deep inside every tape.

  **IDEA 1335's RESIDUAL IS THE TAPE'S NEW ROWS, NOT ITS REWRITES.** Letting each vintage keep
  its own sample (V_RAW, up to 11 extra sessions) spreads full Sharpe by **6.4e-3**, the H2
  margin by 1.2e-2, the OOS margin by 1.2e-2 and the CAGR margin by 0.09 pp — the size of the
  6.98e-3 G1b residual, and ~1,000x the V_TRUNC spread. **Cross-run replay in this repo is
  resolution-limited to ~6e-3 of Sharpe unless both runs name the same tape blob**, and that
  limit comes from the extra week of data, not from the restatement.

  **THE VERDICT DOES FLIP — ON 2 OF 14, BOTH A FIXED BUG.** The two vintages below commit
  c006b439 ("Fix calendar-day index bug: align crypto to equity") carry ~6,060 calendar rows
  against ~4,700 trading rows and give 11.85/11.87% CAGR, 1.0028/1.0044 Sharpe, -20.89% MaxDD,
  DD margin **-0.66 pp** -> 4b FAIL. Published, but counted as a data bug, not as tape noise.

  **THE MECHANISM — PRICE CHURN IS AN UPPER BOUND ON WHAT A BOOK FEELS.** 9.2% of overlapping
  U56 price cells restate per daily step (auto_adjust back-adjusts the whole history on every
  ex-dividend), but the median |delta daily return| is **1.1e-6** (CSV formatting), only
  **0..699** return cells per step move by more than 1 bp, and the largest single move (5.1 pp)
  is in the two CRYPTO columns universe.json excludes. Reporting a restated-cell share without
  converting it to return space overstates the exposure by three orders of magnitude.

  **RULE 8 — THE CHOOSER IS VINTAGE-STABLE AND STILL LOSES.** Dials chosen on warm-up..2016-12-31
  only, 2017-2026 read ONCE, the chooser re-run SEPARATELY ON EACH VINTAGE: argmax IS Sharpe
  picks (16, 63) on **12 of 12** post-fix U56 vintages and loses to the do-nothing anchor by
  **-0.0400** of mean OOS Sharpe (pick 1.1388..1.1462 vs anchor 1.1759..1.1870); the pick clears
  4b **0 of 12**, the anchor **12 of 12**. H_HINDSIGHT fires again — the cell nobody had to
  choose is the one that passes. On SMALL the pick DOES move ((20,63) -> (10,252), 0.43 of OOS
  Sharpe) but only at the commit where the cached panel went from **445 to 665 names**: that is a
  universe rebuild, so on SMALL the vintage dial is confounded and is reported as such.

  **KEEP-path census.** 4a **0 of 912** at every cell (live RULES v2: full Sharpe 1.2011,
  MaxDD -12.05%). 4b 65 of 912 — U56 28/336, BROAD 37/312, **SMALL 0 of 264**.

  **GATES 8/8**: G0 every vintage >= 10y; G1 the 2026-09-16 vintage replays the committed U56
  anchor 15.7147% / 1.14798 / -19.1276% against 1.14804 (deviation **6e-5** of Sharpe) — the
  committed anchor IS reproducible once the tape is named; G2 determinism 0.0; G3 14 distinct
  blobs; G4 all 912 cells published; G5 exactly two tuned parameters (vintage, panel); G6 OOS
  starts on or after 2017-01-01 everywhere; G7 one V_TRUNC end date per panel.

  **SURVIVORSHIP (rule 9).** U56 / BROAD are current-constituent lists and SMALL a current
  sub-$2B screen, so every absolute level is an upper bound. The headline is a SPREAD of the
  SAME book over the SAME names across tapes, so it is first-order immune; the 4b pass count
  is not.

  **No RULES change.** RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py untouched. The
  memo (`2026-09-19_tape-vintage-certified-incumbent_B.memo.md`) carries the exact RULES wording
  and adds one reporting clause: publish the price tape's git blob beside every committed number.

## 2026-09-19 — idea 903 (lane B): is the per-arm 20-seed MEDIAN a biased estimator of every null-minus-BLOCK headline? **ANSWERED (yes, and it explains nothing) / CAPITAL ARM KILL / SCHEMA FIX PROPOSED.**

  **Why this run has a price leg.** Three lanes had skipped 903 as "a census / a null contrast,
  no book". Lane B's own 1265 and its 904 run (2026-09-18) overturned that premise, and 903's
  own second clause — "re-price the record's committed 20-seed placebo numbers against it" — is
  a question about money. 7,200 null books were built and every per-seed Sharpe STORED (the
  thing 885 could not do, and the reason 903 exists): 3 panels x 6 arms (N {5,10,15,20,25,30} at
  the frozen H=126, MAXVOL 0.60, GROSS 0.75, weekly, 10 bps, t+1) x 2 gross-matched null kinds
  (RAND, and a BLOCK circular bootstrap of the real key at LB=13 rebalance rows) x 200 seeds.
  Dials: S {5,10,20,50,100,200} x estimator {median, mean, trimmed10} — 18 cells per panel, all
  published.

  **THE DECLARED TEST, AND 885 IS RIGHT.** The sample mean is unbiased at every S by
  construction, so if the 20->200 drift vanishes under the MEAN, the drift IS the median's
  small-sample bias. It vanishes. Bias at S=20 (mean over 2,000 random size-S subsets minus the
  all-200 read, averaged over the 6 arms, RAND null): **median +0.002693 / -0.002938 / -0.003307
  (U56/B136/SMALL) against mean +0.000019 / -0.000184 / -0.000267.** Scored per (panel, kind)
  row against that row's own Monte-Carlo floor, the median clears at **4 of 6** and the mean at
  **0 of 6**. Mean |bias| at S=20: median **0.001779**, trimmed10 **0.000315**, mean **0.000168**.

  **AND IT EXPLAINS NOTHING. The per-arm SD of ONE 20-seed read is 0.027829 of Sharpe, so
  bias/noise = 0.0639** — the systematic error is **15.7x smaller** than the random error on the
  very number it biases. 885 measured a real effect and drew the wrong lesson from its size.

  **885's TWO SUPPORTING CLAIMS BOTH FAIL.** (1) "9 of 9 shift the same way": over this run's 36
  (panel, kind, arm) cells the sign is **15 positive / 21 negative**, consistent WITHIN a panel
  on RAND (U56 +, B136 -, SMALL -) and different ACROSS them — the unanimity is a property of
  885's one corpus, not of the median. (2) "cancels between same-construction nulls": true only
  in the trivial BLOCK-vs-BLOCK direction. The form the record actually publishes is
  **null-minus-BLOCK**, and there the contrast's median bias at S=20 is **+0.002049 / -0.002728
  / -0.002471 — 76% to 102% of the RAND arm's own bias** — because BLOCK's own median bias is
  3.6x to 8.3x smaller. A cross-construction contrast inherits the biased side nearly in full.

  **THE FIX IS FREE AND THE MEDIAN IS STRICTLY DOMINATED.** median -> mean removes the bias AND
  cuts the per-arm 1-read SD by **-20.3% (U56) / -24.1% (B136) / -21.4% (SMALL)**: the
  null-Sharpe distribution is near-symmetric, so the median's robustness buys nothing while it
  pays the usual efficiency penalty. Measured per-arm sigma = **0.0707 / 0.0759 / 0.1021**,
  between 885's assumed 0.067 and 904's 0.1307 (904's grid included H=21, which disperses more).
  **RECOMMENDED SCHEMA CHANGE, NOT ENACTED:** a committed placebo statistic should aggregate
  seeds with the arithmetic MEAN and quote its seed count and its per-arm 1-read SD. PROTOCOL
  rule 6 confines rules changes to the Sunday review; this run modifies no rule file.

  **THE CAPITAL ANSWER — KILL, NO NEW BOOK.** 108 chooser cells (S x estimator x null kind x
  panel), every one published: among the 6 arms pick argmax of Sharpe_IS - E_{s<=S}[null], read
  on IS rows only. **4a 0 of 108; 4b full 0 of 108; 4b full+OOS 0 of 108**, binding legs L_DD
  108 > L_H2 72 > L_H1 36 = L_CAGR 36. **THE DIAL IS ALL BUT INERT:** distinct picks over the 18
  RAND cells are **U56 1, B136 1, SMALL 2** — every seed budget and every estimator picks N=5 on
  two of three panels. Rule 8 (S, estimator picked on warm-up..2016 by argmax IS Sharpe of the
  selected book; 2017-2026 read ONCE): U56 (S=5, median) -> N=5, OOS 17.32% / 0.9118 / -25.85%;
  B136 (S=5, median) -> N=5, OOS 14.67% / 0.7513 / -28.12%; SMALL (S=20, median) -> N=25, OOS
  8.84% / 0.5236 / -36.87%. Mean d(OOS Sharpe) **-0.1536** vs doing nothing, beats it 1 of 3;
  **-0.0951** vs the raw IS-Sharpe chooser, beats it 0 of 3.

  **THE MECHANISM, INDEPENDENTLY REPRODUCING 904.** Placebo-differencing is a CONCENTRATION
  BIAS: a random 5-name portfolio is a terrible null, so subtracting it rewards exactly the arms
  that lose out of sample. U56's pick N=5 reads OOS 0.9118 against ARM-N15's 1.1971 and the
  frozen ANCHOR-N20's 1.1857. 904 found this at 50 seeds on a 24-book N x H grid; it is
  unchanged at H=126 with a 200-seed budget, so it is not a seed-budget artefact.

  **H_HINDSIGHT fires again.** Six comparand books clear 4b full AND OOS and **none is reachable
  by any chooser in this run** — U56 ARM-N15 (17.14% / 1.1722 / -20.14% full, OOS 19.01% /
  1.1971 / -20.14%), U56 ANCHOR-N20 (15.80% / 1.1537 / -19.13%, OOS 17.32% / 1.1857), B136
  ARM-N15 (OOS 1.0405), B136 ARM-N10 (OOS 0.9212). Consistent with 1321 / 1323 / 1331 / 904.

  **THE RE-PRICING (903's second clause) — THE PROBLEM IS SEEDS, NOT ESTIMATORS.** Mechanical
  harvest over research/backtests/*.md + CHANGELOG.md (LEADERBOARD.md and QUEUE.md excluded by
  declaration, 904's rule): **1,262 files -> 410 placebo-cued sentences -> 24 carrying a >=4-dp
  decimal -> 18 DIFFERENCES (|x| < 0.1) -> 4 stamped with a seed count -> 1 stamped S=20
  exactly.** 12 of 18 sit inside the per-arm 1-read 20-seed SD and only 3 of 18 inside the bias.
  The record's committed placebo numbers are not wrong because the median is biased; they are
  UNRESOLVED, and the fix for that is seeds.

  **A GATE THIS SCRIPT FAILED FIRST, KEPT IN THE RECORD.** G3 as originally written
  ("|bias_mean| <= 1e-12") FAILED at **1.824e-03**. The mean IS unbiased in expectation, but the
  measurement of it is a Monte-Carlo average with SE = sd/sqrt(R), ~3e-3 at S=5 and R=400 — the
  gate was measuring its own noise. Fixed by publishing the MC SE beside every bias, raising R
  400 -> 2000, and reading the three estimators on COMMON RANDOM NUMBERS so the median's bias is
  readable net of the mean arm's residual (bias_net 0.001648). No dial, book or verdict changed.
  Final gates **10/10**, including G2 (the IS slice of a full-sample build is bit-identical,
  0.000e+00, to a build stopped at IS_END, which licenses the build-once-slice-twice
  construction) and G8 (the frozen U56 anchor replays at 15.8028% / 1.1537 / -19.1276%,
  consistent with idea 1350's committed head anchor).

  **SURVIVORSHIP (rule 9).** U56 / B136 / SMALL are current-constituent lists. Every absolute
  level is optimistic. The bias headline is a difference between estimators computed on the SAME
  books and the SAME seeds, so it is first-order immune; the 0-of-108 pass count is not.

  **No RULES change.** RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py untouched.

## 2026-09-19 — idea 1534 (lane C): does ANY ruler ever rescue a DEVICE, or is the device side of the record simply EMPTY? **ANSWERED — THE SIDE IS EMPTY AND THE NUMBER IS -0.0727 ± 0.0291 OF SHARPE / KILL for capital, no new book.**

  **The defect this closes.** Eleven runs had returned 4a = 0 and the record's standing claim
  "no device beats a de-gross" was a COUNT OF FAILURES, not an effect size. A count cannot be
  compared to anything, cannot be pooled, and cannot say how big the loss is. This run states
  the number.

  **CONSTRUCTION.** BASE = the committed 2026-09-04 anchor shape: top-N by H-day momentum among
  names above their 200d MA with vol20 < 0.60, equal weight at gross 0.75, weekly, 10 bps, t+1.
  Exactly two tuned parameters, (N, H) = (20, 126), FROZEN at the committed anchor and not
  searched. DEVICE = any overlay that withdraws exposure: six families x five rungs x three
  panels = **90 device books**, every rung published. ANCHOR = the SAME base book de-grossed by a
  CONSTANT chosen so its realised mean gross equals the device's, to **1.92e-07** over all 90
  pairs (G1). Families: BAND (200d hysteresis band), STOP (trailing equity stop, re-entry
  fraction 0.50 frozen from idea 1468), VOLTGT (gross scaled to a vol target, no leverage),
  MAXVOL (name-level vol ceiling), MADIST (distance above the 200d MA), SPYFILT (index MA gate).

  **THE HEADLINE.** Pooled over all 90 pairs the device costs **-0.0727 of Sharpe, SE 0.0291,
  t -2.50, 95% CI [-0.1298, -0.0157]**; pooled dCAGR **-0.69 pp/yr**; pooled dMaxDD **-1.55 pp**,
  i.e. the device is **DEEPER** than the plain de-gross twin, not shallower. SEs come from a
  circular block bootstrap, LB = 65 trading days (~ the record's LB = 13 rebalance rows), B = 500,
  with the SAME blocks drawn for every book and every panel in a replicate, so cross-book and
  cross-panel dependence is carried rather than assumed away.

  **NO RULER EVER RESCUES A DEVICE.** Scored book by book against its OWN bootstrap SE:
  **0 of 90 significantly POSITIVE, 17 significantly NEGATIVE, 73 indeterminate.** This
  reproduces 1509's 337-contrast reading (0 positive / 25 negative) on an independent
  construction — paired matched-exposure twins rather than bracketed contrasts.

  **AND THE POOLED SIGNIFICANCE IS ONE FAMILY.** STOP carries it: **-0.2522, SE 0.0718, t -3.51,
  0 of 15 wins, dMaxDD -7.23 pp**. Ex-STOP the pooled effect over the remaining 75 books is
  **-0.0368, SE 0.0244, t -1.51 — indistinguishable from zero.** By family: BAND -0.0013
  (t -0.12), VOLTGT -0.0249 (t -0.62), MAXVOL -0.0508 (t -1.18), MADIST -0.0568 (t -2.42),
  SPYFILT -0.0504 (t -0.71). By panel: U56 -0.0684 (t -2.41), B136 -0.0800 (t -2.91), SMALL
  -0.0698 (t -1.49). **The record's sentence should be "STOPS LOSE, THE REST ARE FREE AND
  POINTLESS", not "devices lose".**

  **THE ONE FAMILY THAT BUYS ANY DRAWDOWN.** VOLTGT is alone in a POSITIVE pooled dMaxDD at
  matched exposure (**+0.97 pp**, against BAND -0.56, MADIST -0.54, MAXVOL -0.53, SPYFILT -1.40,
  STOP -7.23) and pays -0.56 pp/yr of CAGR for it. Filed as idea 1537.

  **BOTH KEEP PATHS.** **4a 0 of 93** — the twelfth consecutive 4a zero (live RULES v2 on U56:
  8.62% / 1.2010 / -12.05%, halves 1.228 / 1.181). **4b 31 of 93**, but **6 of the 31 are the
  frozen BASE itself** at degenerate rungs (MAXVOL m=0.60 and MADIST k=0.00 ARE the BASE;
  G2 |dSharpe| = 0.00e+00) and the remainder are inherited from it — no device CREATES a 4b pass
  its own de-gross twin does not already have.

  **RULE 8.** Device and rung chosen by argmax Sharpe on warm-up..2016-12-31 only, 2017-2026 read
  ONCE. The chooser picks the **LOOSEST** rung (MAXVOL m=0.80, i.e. the least device) on BOTH U56
  and B136, and MAXVOL m=0.25 on SMALL. Against its own matched-exposure anchor it runs
  **-0.0021 / +0.0626 / -0.1953**, mean **-0.0449** of OOS Sharpe, beating it **1 of 3**; against
  the do-nothing frozen BASE, mean -0.0450, **1 of 3**. H_HINDSIGHT fires again. The one book that
  beats both (B136 MAXVOL m=0.80, OOS 15.07% / 1.0124 / -19.37%) wins by REMOVING device, which is
  the thesis, not a counterexample — filed as idea 1541.

  **GATES 7/7**: G1 exposure match 1.92e-07 over all 90 pairs; G2 the two degenerate rungs replay
  the BASE at 0.00e+00; G3 samples 17.7y / 17.7y / 15.6y (rule 1); G4 all 93 books published in
  the script's output and in `2026-09-19_pooled-device-vs-degross_C.csv`; G5 exactly two tuned
  parameters, both frozen; G6 OOS starts 2017-01-01 on every panel and the chooser reads no row
  at or after it; G7 10 bps per unit turnover, t -> t+1, no shorting, gross <= 0.75.

  **SURVIVORSHIP (rule 9).** U56 / B136 / SMALL are CURRENT-constituent lists, so every absolute
  level is an upper bound. The headline is a DIFFERENCE between two books over the SAME names on
  the SAME days, so it is first-order immune; the 4a / 4b pass counts are not.

  **No RULES change.** RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py untouched. No memo:
  this run produces no KEEP candidate.

## 2026-09-19 — idea 708 (lane B): is the per-r COST DRAG INVERSION a record-wide fact or a CAND-n GROSS/n CONVENTION? **ANSWERED — IT IS A CONVENTION, AND THE RAW CLAIM IS NOT EVEN SIGN-STABLE. KILL (capital), NO NEW BOOK, NO RULES CHANGE — with a METHOD FINDING and a self-logged statistic correction.**

  **The claim under test.** Idea 703 (lane C, 2026-09-11) measured cost drag on OOS Sharpe
  monotone DECREASING in the selection ratio at every width (k = 400: −0.1219 / −0.1168 /
  −0.0981 / −0.0805 at r = .05/.10/.25/.50) and committed the sentence *"holding more names is
  CHEAPER, not dearer"*, which inverts the record's recurring cost-of-breadth reasoning and has
  been quoted since. Every book in that ladder sizes at GROSS/n, so one replacement costs 2G/n
  of NAV: turnover per unit NAV is a replacement FRACTION, and a fraction falls as its
  denominator grows even when the book churns the same number of slots.

  **CONSTRUCTION.** DIAL 1 FAMILY {CAND, MADIST, BAND, ADAPT, EWALL}; DIAL 2 COST RUNG {0, 5,
  10, 25, 50} bps, 10 binding. Exactly two tuned parameters. NOT dials, published at every
  value: breadth n {5, 10, 20, 40, 80, ALL} (the axis the question is about) and PANEL {U56,
  B136, SMALL}. Gross frozen at the live 0.75, weekly, t+1, no shorting, no leverage. **25 books
  per panel, 75 in all, × 5 rungs = 375 cells, every one published.** Costs are RECONSTRUCTED
  from the turnover identity, not re-fitted (G1 proves the reconstruction exact at 0.000e+00).

  **THE PRE-REGISTERED DISCRIMINATOR, AND IT IS UNANIMOUS.** Drag re-cut in three currencies:
  T_nav (per unit NAV, the record's), T_gross (per unit deployed capital), T_slot (NAME SLOTS
  replaced per year = T_nav · nbar / gbar). Meaned over three panels: **rho(n, T_nav) −0.9952
  (CAND) / −0.9952 (MADIST) / −0.9952 (BAND) / −0.9804 (ADAPT) against rho(n, T_slot) +0.9952 /
  +0.9952 / +0.8216 / +0.9804.** H_CONVENTION legs 4 of 4 and 4 of 4; **H_GENERAL 0 of 4.** Per
  unit NAV a wide book looks far cheaper (U56 CAND 23.67 → 8.20 ×/yr, n = 5 → ALL); in slots it
  churns **more than twice as much** (157.7 → 408.7 on U56, 196 → 1006 on B136, 223 → 4152 on
  SMALL). Nothing got stabler — GROSS/n shrank the slot.

  **THE DRAG IS T_nav/vol AND NOTHING ELSE.** Over the 75 books, **drag(10 bps) = +0.000167 +
  0.999786 × (10/1e4)·T_nav/vol_0, R² 0.999983, max |residual| 0.000735 against a mean |drag| of
  0.106382, Spearman 0.999516.** Slope 1.000, intercept 0.0002. Any ordering of books by drag is
  an ordering by T_nav, so the inversion restates without residue as "T_nav falls with n" — the
  convention written down.

  **AND 703's RAW CLAIM DOES NOT REPLICATE WITH A STABLE SIGN. 3 of 12 arms run the other way.**
  rho(n, drag) is −0.81 / −0.75 / −0.81 / −0.94 on U56 and −1.00 / −0.83 / −0.60 / −1.00 on B136
  (CAND / MADIST / BAND / ADAPT), but **+0.26 (CAND) / +0.43 (BAND) / +0.60 (ADAPT) on SMALL**,
  where drag RISES from n = 5 to n = 40 (CAND +0.0810 → +0.1860) before falling. "Monotone
  decreasing at every width" is a property of 703's one panel.

  **METHOD FINDING (G8): THE RECORD HAS TWO CURRENCIES, NOT THREE.** Every count family
  re-spreads the full gross over the names it holds, so gbar is constant and T_gross is a fixed
  multiple of T_nav: their rank correlations against n agree on **12 of 12 arms at max |Δrho|
  0.000e+00**. "Per unit deployed capital" is not an independent reading of anything on any
  GROSS/n ladder in this record.

  **BOTH KEEP PATHS.** **4a 0 of 75** — another consecutive 4a zero (live RULES v2 on U56 8.62% /
  1.2010 / −12.05%, halves 1.2276 / 1.1805). **4b 13 of 75** (U56 3 / B136 10 / SMALL 0), binding
  legs CAGR 34 < H2 38 < DD 39 < OOS 40 < H1 46. **Not one of the 13 is a new book:** they are the
  wide/ALL ends — idea 1454's re-spread book (U56 BAND-ALL 12.19% / 1.1567 / −17.71% full, OOS
  1.1950) and its neighbours, already killed as a dial by idea 1555 (RESPREAD loses to the SHY
  sleeve on Sharpe 6 of 6 and MaxDD 6 of 6). **H_HINDSIGHT fires again:** all 13 clear 4b full AND
  OOS and none is reachable by any chooser in this run.

  **RULE 8** (params on warm-up..2016-12-31 only, 2017–2026 read ONCE). **C_DRAG — "pick the
  cheapest book", this idea's own dial made into a real selector — picks EWALL-ALL on 3 of 3
  panels and loses to doing nothing on 2 of 3, mean dOOS Sharpe −0.0430.** C_SHARPE picks BAND-5
  on U56 and B136 and EWALL-ALL on SMALL. Both choosers pooled: mean **−0.0556** vs LIVE (beats it
  2 of 6) and **+0.0793** vs SPY (4 of 6). The cheapest book in the grid is the one with no
  selection in it at all.

  **A CORRECTION THIS RUN MADE TO ITSELF, LOGGED RATHER THAN HIDDEN.** The per-slot currency was
  first written `T_nav / nbar`, which divides by breadth TWICE (a GROSS/n book already carries one
  factor of 1/n inside T_nav) and forces rho(n, ·) = −1 by construction. The first pass printed
  rho(n, T_nav) == rho(n, T_gross) == rho(n, T_name) to four decimals on 12 of 12 arms — the
  signature of exactly that degeneracy — and read **H_GENERAL** off it. Corrected to
  `T_nav · nbar / gbar`, the verdict **REVERSED to H_CONVENTION, 4 of 4 against 0 of 4.** Both the
  erroneous reading and the fix stand in the script docstring and the result memo.

  **GATES 91/91**, including G1 cost identity 0.000e+00 over 9 spot cells; G2 this script's own
  band machinery replays `baseline.rules_v2_weights` at exactly 0.0 on all three panels; G3
  ADAPT-ALL == CAND-ALL at 0.000e+00 (degeneracy checked, not assumed); G5 no chooser reads a row
  on or after 2017-01-01; G6 gross in [0, 1] on all 75 books; G7 all 375 cells published.

  **SURVIVORSHIP (rule 9).** U56 / B136 / SMALL are CURRENT-constituent lists, so every absolute
  level is an upper bound. The headline is a set of within-book turnover decompositions and a
  difference between two cost rungs on the SAME book over the SAME days, so it is first-order
  immune; the 4a / 4b pass counts are not.

  **WHAT THE RECORD SHOULD SAY INSTEAD.** *The cost drag of a GROSS/n book falls with n because
  the convention shrinks each slot to G/n, not because wide books churn less: in name-slots per
  year, breadth RAISES turnover monotonically on 4 of 4 families and 3 of 3 panels. Drag is
  T_nav/vol to R² 0.99998 and carries no information of its own. The sign of drag-vs-breadth is
  panel-dependent, so "holding more names is cheaper" should not be quoted unqualified.*

  **No RULES change.** RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py untouched. No memo:
  this run produces no KEEP candidate.

## 2026-09-19 — idea 766 (lane B): is the DAILY-CADENCE WIN of the MOMENTUM SLICE an EDGE the IS SELECTOR is MISSING? **ANSWERED — NO. IT IS REAL INFORMATION PRICED AT 2.62 bps ON A 10 bps TAPE. KILL for capital, no new book, no RULES change.**

  **THE CLAIM UNDER TEST.** Idea 563 (cloud, 2026-09-11) committed two sentences side by side:
  MOM-D (the daily-depth-matched 12-1 momentum slice) beats the MA slice on Sharpe in **66.7%**
  of pairs at cadence D and **13.0%** at Q, *and* the IS-Sharpe selector picks cadence D in **0
  of 54** MA-THRESH cells and 4 of 54 MOM-D cells. Read together those say the record's own
  selector systematically refuses the one cell where the momentum slice wins. Either it is an
  edge left on the table, or it is churn the selector is right to avoid. Nobody had priced it.

  **BOTH CLAUSES OF THE PREMISE REPRODUCE.** On this run's independent grid (5 theta x 3 gross,
  3 panels) MOM-D beats MA-THRESH on Sharpe in **0.6667** of pairs at D (mean **+0.1063**),
  0.6778 at W, 0.4000 at M and **0.2000** at Q (mean −0.0275) — 563's 66.7% is hit to four
  decimals and its 13.0% at Q lands at 20.0% on the wider gross axis. The selector picks D in
  **0 of 90** MA-THRESH cells and **3 of 90** MOM-D cells. The premise is not the problem.

  **CONSTRUCTION.** Idea 563's, verbatim, so the premise is tested rather than re-invented.
  MA-THRESH = `px > MA200*(1+theta)`; MOM-D = top k_t by 12-1 momentum with k_t = |MA-THRESH_t|
  pinned EVERY DAY, so the two arms hold the same NUMBER of names each day and only the NAMES
  differ. DIAL 1 CADENCE {D, W, M, Q}; DIAL 2 SELECTOR {S_SHARPE, S_CAGR, S_FORCE_D}. Exactly
  two tuned parameters. NOT dials, published at every value: PANEL {U56, B136, SMALL439} x THETA
  {0.12, 0.06, 0.00, −0.06, −0.12} x ARM x CONSTRUCTION {RESPREAD, DEGROSS} x GROSS {0.50, 0.75,
  1.00}. **720 books, every one in `.grid.csv`.** S_ORACLE (argmax OOS Sharpe) is printed as an
  UNREACHABLE upper bound, never as a verdict.

  **LEG 2 — THE TURNOVER-MATCHED CONTROL, AND IT IS THE WHOLE ANSWER.** Because the engine's
  cost is exactly `turnover x c / 1e4` in return space, the rung at which the daily book's
  advantage over the same cell at a slower cadence crosses zero is computable EXACTLY off one
  held path. Bisected over 540 daily-vs-slower pairs: **at 0 bps the daily cell genuinely wins
  for the momentum arm** — MOM-D takes 0.80 (vs M) / 0.86 (vs Q) / 0.69 (vs W) of pairs on
  Sharpe and **1.0000 of them on SMALL439** — and **at 10 bps that collapses to 0.12 / 0.41 /
  0.03.** Median break-even **c\* = 2.62 bps for MOM-D** (IQR 0.52–7.89, p90 16.90) and **0.00
  bps for MA-THRESH**, whose daily book is behind before a single basis point is charged. Only
  **0.1278 of 540 pairs** have c\* above the protocol's binding 10. Median daily turnover
  8.99x/yr against the weekly twin's 3.76x.

  **LEG 1 — RULE 8, AND IT AGREES.** Cadence chosen on IS Sharpe (start..2016-12-31) ONLY,
  2017–2026 read ONCE, over 180 (panel, theta, arm, construction, gross) cells. **S_FORCE_D beats
  S_SHARPE on OOS Sharpe in 0.1111 of 180 cells, mean −0.1033** (MA-THRESH 0.0556 / −0.1422;
  MOM-D 0.1667 / −0.0645). Mean OOS Sharpe: S_FORCE_D **0.8242**, S_CAGR 0.9054, S_SHARPE
  **0.9275**, unreachable S_ORACLE 0.9538 — **the selector the record already uses banks 97.2%
  of the oracle, and forcing the daily cell throws away a tenth of a Sharpe.** It beats RULES v2
  OOS in 0.15 of cells against the selector's 0.38, and SPY OOS in 0.55 against 0.67.

  **THE CLEANEST FORM OF THE FINDING.** Pooled over the 180 cells, the WEEKLY twin beats the
  DAILY twin of the SAME cell on full Sharpe in **0.9833** and on OOS Sharpe in **0.9944** —
  while at ZERO cost that falls to 0.5889 overall and **0.3111 on the MOM-D arm**. The daily
  book picks better names and hands the difference back at the tape. Nothing is left on the table.

  **BOTH KEEP PATHS.** **4a 15 of 720, 4b 31 of 720, and the two sets are DISJOINT (0 books pass
  both)** — the twenty-somethingth consecutive 4a/4b disjunction in this record. All 15 4a passes
  are DEGROSS books that fail 4b on the CAGR floor. **Only 3 of the 31 4b passes sit at cadence
  D, and all 3 are dominated by their OWN weekly twin on full Sharpe, OOS Sharpe AND turnover
  (3 of 3)**: the best, U56 theta −0.06 MA-THRESH DEGROSS g1.00, runs 12.29% / 1.1271 / −18.83%
  (OOS 1.1926) at 6.61x/yr against its weekly twin's 12.97% / 1.1664 / −18.29% (OOS 1.2090) at
  2.97x. Live RULES v2 @10bps for reference: U56 8.62% / 1.2010 / −12.05% (halves 1.2276/1.1805,
  OOS 1.2766); B136 1.0972 (1.2296/0.9669); SMALL439 0.6596 (0.8057/0.5480). SPY 15.12% / 0.8843
  / −33.72% (0.9570/0.8249), OOS 0.8737.

  **GATES 8/8**: G0 fast_run vs `engine.backtest` (returns AND turnover) 0.000e+00 on every panel
  at D and W; G1 derived 25 bps rung vs a fresh engine run at 25 bps 0.000e+00; G2 daily depth
  match exact on 0.9694..1.0000 of days, mean |dk| <= 0.031, max |dk| = 1 — REPORTED, not assumed
  away, since 12-1 momentum needs 252 closes where the 200d MA needs 200; G3 the live baseline row
  is produced by the committed `baseline.rules_v2_weights` through `engine.backtest`, unmodified;
  G4 target-gross identity between the two arms 0.000e+00 on exact-match days; G5 no selector reads
  a row on or after 2017-01-01; G6 720 of 720 books published; G7 10 bps per unit turnover,
  t -> t+1, no shorting, max realised gross 1.0000.

  **SURVIVORSHIP (rule 9).** U56 / B136 / SMALL439 are CURRENT-constituent lists, so every absolute
  level is an upper bound. The headline is a cadence-minus-cadence and arm-minus-arm difference
  INSIDE one panel over the SAME names on the SAME days at identical daily depth, so it is
  first-order immune; the 4a / 4b pass counts are not.

  **WHAT THE RECORD SHOULD SAY INSTEAD.** *The daily cadence win of the momentum slice is real
  and it is not alpha the selector is missing. At zero cost the daily book holds better names
  (MOM-D wins 0.69–0.86 of daily-vs-slower pairs, 1.0000 on SMALL439); the advantage breaks even
  at a median 2.62 bps and the protocol charges 10. Forcing it costs 0.1033 of OOS Sharpe against
  the IS selector, which already banks 97.2% of the unreachable oracle. Idea 563's two sentences
  are both true and their juxtaposition is not evidence of a missed edge.*

  **No RULES change.** RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py untouched. No memo:
  this run produces no KEEP candidate.

## 2026-09-19 — Research C (idea 1586): the weekly cadence and the MAXVOL 0.60 gate, priced together at 10 and 25 bps

  **No RULES change.** RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py untouched. One memo
  written (`2026-09-19_weekly-cadence-x-maxvol-gate-at-25bps_C.memo.md`) for an INCIDENTAL 4b
  passer that is explicitly NOT adopted.

  **WHAT WAS RUN.** 192 real books: 3 panels (U56 55 / B136 135 / SMALL 665) x 2 frames (LIVE =
  the live RULES v2 band shape at gross 0.75; INC = the frozen 2026-09-04 anchor, N = 20, H = 126)
  x cadence {D, W, M, Q} x MAXVOL {0.45, 0.60, 0.80, none} x cost {10, 25} bps, every one
  published. Two dials only. Cost is NOT a dial: weights are cost-independent, so
  `r(c) = r_gross - turnover * c / 1e4` is EXACT, and **G2 checks the derived 25 bps rung against
  a fresh 25 bps engine run at 0.000e+00**. That exactness is what makes the headline possible.

  **LEG 1 — THE GATE IS A DE-GROSS IN DISGUISE, AND IT IS SEPARABLE FROM THE CADENCE.** The 2x2
  interaction `[S(W,0.60) - S(W,none)] - [S(c,0.60) - S(c,none)]` has mean |I| **0.0482** over 36
  readings and **0.0121 on the LIVE frame**, against the record's own W->M step of 0.1053: the two
  inheritances are separable and "jointly" is the wrong word for them. The gate's own sign is
  one-directional — re-adding MAXVOL 0.60 to the live book costs **-0.0505 / -0.0352 / -0.1253**
  of Sharpe on U56 / B136 / SMALL at 10 bps (-0.0564 / -0.0391 / -0.1449 at 25) and
  **-0.85 / -0.54 / -1.41 pp/yr** of CAGR. It DOES buy 0.55-1.74 pp of drawdown, and **G10 shows
  how: mean realised gross falls 0.5317 -> 0.5192 (U56), 0.5306 -> 0.5214 (B136), 0.4124 -> 0.3670
  (SMALL).** It is a de-gross wearing an eligibility filter's clothes — the family eight
  2026-09-19 runs already found beaten at matched exposure. **RULES v2 clause 2's decision to drop
  the volatility filter is vindicated on all three panels.**

  **LEG 2 — THE COST INVERSION IS REAL AND ONE-DIRECTIONAL.** Over the 24 (panel, frame, MAXVOL)
  groups the full-sample cadence argmax moves between 10 and 25 bps in **5 of 24** and the OOS
  argmax in **4 of 24** — and **9 of 9 of those moves go SLOWER, not one goes faster.** Argmax
  distribution FULL: 10 bps {M 11, W 10, D 3} -> 25 bps {M 15, W 7, Q 1, D 1}. Idea 1009's
  0-vs-10 inversion is therefore not a zero-cost artefact; the ordering is still sliding at rungs
  a real book pays.

  **LEG 3 — THE SHARPEST NUMBER: c\* = 12.4 bps.** Because the cost axis is exact, the break-even
  rung at which a slower rival overtakes W is readable by bisection for all 72 (panel, frame,
  MAXVOL, rival) pairs with no extra backtest. **For the frozen anchor's own cell (U56, INC,
  MAXVOL 0.60), W vs Q: c\* = 12.4 bps.** At 25 bps the quarterly twin already wins on full Sharpe
  (1.1329 vs 1.1217) AND OOS (1.1706 vs 1.1546), at 1.64x/yr against 2.87x/yr of turnover, passing
  4b FULL and OOS at both rungs. Across all 72 pairs: 58 finite c\*, 14 never overtake W; of the
  58, **25 are already ahead at 10 bps, 7 cross between 10 and 25, 26 cross above 25**; median c\*
  **19.2 bps**. **The live weekly cadence is optimal by 2.4 bps of cost, not by a margin.**

  **BOTH KEEP PATHS.** At the binding 10 bps: **4a 0 of 96** (3 of 96 on OOS alone), **4b 7 of 96
  FULL, the same 7 OOS, 7 BOTH**, and **4a n 4b = 0** — the umpteenth consecutive disjunction. All
  7 sit on the INC frame; the LIVE frame passes 4b **0 of 48**, still failing on the CAGR floor.
  **The best of the seven is the frozen 2026-09-04 anchor itself** (15.80% / 1.1537 / -19.13%,
  OOS 17.32% / 1.1857): it is its own grid's argmax. The same 7 pass at 25 bps.

  **RULE 8.** Three IS-only choosers x 3 panels x 2 frames x 2 rungs = 36 walk-forwards, 2017-2026
  read once. Pooled mean OOS Sharpe **C_ANCHOR (change nothing) 0.9081 > C_MEMO 0.9001 > C_SHARPE
  0.8466**; C_SHARPE beats the anchor in **2 of 12** and costs **-0.0615** of OOS Sharpe (-0.0625
  at 10 bps, -0.0605 at 25). Tuning these two dials is negative-value out of sample at both rungs.
  Live RULES v2 OOS for reference: U56 1.2769 / B136 1.1019 / SMALL 0.6473; SPY OOS 0.8738.

  **GATES 20/20.** G1 fast_run vs `engine.backtest` (returns AND turnover) 0.000e+00 over 12
  panel x cadence runs; G2 as above; G3 LIVE (W, none) replays `baseline.compare`'s RULES v2 row
  to **2.220e-16** (the `none` rung reduces the frame exactly); G4 INC (W, 0.60) replays the
  committed 2026-09-04 anchor to **3.718e-05**; G5 two dials; G6 no chooser reads a row on or
  after 2017-01-01, TESTED on truncated IS input; G7 192 of 192 published; G8 max realised target
  gross 0.7500, no shorting; G9/G10 turnover, realised gross and names held published per cell.

  **SURVIVORSHIP (rule 9).** U56 / B136 are current-constituent lists and SMALL a current sub-$2B
  screen carried back to 2010, so every absolute level is an UPPER BOUND. The headline is a
  cadence-minus-cadence and rung-minus-rung contrast inside one panel over the same names on the
  same days, so it is first-order immune; the 4b pass counts are not.

  **WHAT THE RECORD SHOULD SAY.** *Neither inheritance is jointly anything: the two dials are
  separable, and the MAXVOL gate is a de-gross that costs Sharpe and CAGR on every panel at every
  rung. The weekly cadence survives, but only just — its margin over a quarterly twin on the
  frozen anchor's own cell is 12.4 basis points of trading cost. Quote cadence verdicts as a
  break-even rung, not as a delta at one rung.*

## 2026-09-19 — idea 1617 (lane C): is EVERY eligibility filter a de-gross in disguise?

  **THE QUESTION, AND WHY IT IS NOT THE USUAL ONE.** Eight 2026-09-19 runs found every
  POSITION-SIZING device (trailing stops, breadth throttles, vol targeting, MA-distance gates,
  SPY filters, the drawdown-budget ladder) beaten at matched exposure by a plain constant
  de-gross. Idea 1586's G10 showed the inherited MAXVOL 0.60 gate has the same signature: it
  lowers REALISED mean gross and buys drawdown for CAGR. This run asks whether the whole
  ELIGIBILITY-FILTER family — a SELECTION claim, not an exposure claim — falls the same way.

  **DESIGN.** Two dials and no more: FAMILY {MAXVOL, BAND, RANKCUT} x RUNG, 12 cells including
  the common BASE anchor (hold every priced name at 0.75/N_priced, weekly, t+1, gate-out to
  cash). Each non-BASE cell is paired with a constant de-gross of the SAME unfiltered book,
  scaled by a k solved by 60-step bisection so the twin carries the same **REALISED** mean gross
  — not the same target gross, which is the distinction the idea turns on (the live band runs at
  a realised 0.533 against a target 0.750). 3 panels x 4 cost rungs, **144 of 144 rows published**.

  **THE ANSWER IS SPLIT, AND THE SPLIT IS THE FINDING.** On the SHARPE axis the null holds:
  dSharpe > 0 in **13 of 33** at 10 bps, mean **-0.0273**, decaying monotonically with cost
  (17/33 at 0, **5/33 at 25, 2/33 at 50**), mean dCAGR **-1.12 pp/yr**. On the DRAWDOWN axis the
  null is **REJECTED**: **30 of 33** filters are SHALLOWER than their matched twin, mean
  **+3.67 pp**, holding at every cost rung (30/30/30/29) and out of sample (30 of 33, +4.09 pp).
  This is the opposite sign from every position-sizing device the record has priced.

  **BY FAMILY (10 bps).** BAND dMaxDD **+5.00 pp** (dSharpe > 0 in 6 of 12, mean -0.0006);
  MAXVOL **+4.95 pp** (4 of 12, -0.0389); **RANKCUT +0.19 pp** (3 of 9, -0.0474) — and on SMALL
  all three RANKCUT rungs are DEEPER than their twin, the only 3 negative dMaxDD cells in the
  run, at 2.7-3.8x/yr turnover against the twin's 0.2-1.1x. **The momentum screen's own rank cut
  IS a pure de-gross in disguise; the price-vs-MA and volatility gates are not.**

  **CAPITAL.** 4a **0 of 36** at 10, 25 and 50 bps (4 of 36 at 0 bps only, cost-matched
  comparand). 4b FULL 4 of 36, FULL+OOS **3 of 36**, twins **0 of 36** on every reading: all
  three passers' twins miss the DD cap (-21.69% / -22.22% / -24.55% against -20.23%), so the
  passes are bought ENTIRELY with drawdown the twin cannot buy. Leg failures over 36 cells:
  **CAGR 26**, H2 12, DD 10, H1 9 — the CAGR floor binds the whole family, as it binds the live
  book. Incidental **PARK** (memo written, NOT adopted): vol20 < 0.60, no band, no ranking —
  U56 11.52% / 1.1279 / -16.88%, **OOS 12.04% / 1.1765 / -16.88%**, B136 12.24% / 1.1291 /
  -18.70% (OOS 11.80% / 1.1058), clearing 4b FULL and OOS at 0/10/25/50 bps.

  **RULE 8.** Four legal IS-only choosers x 3 panels, 2017-2026 read once. Pooled mean OOS
  Sharpe **C_LIVE 0.9745 > C_BASE 0.9365 > C_MEMO 0.9324 > C_SHARPE 0.8534**; **0 of 12 picks
  pass 4b OOS**; **0 of 12 reach the PARK cell**; C_SHARPE minus C_BASE = **-0.0831**. Choosing
  an eligibility filter on in-sample rows is negative-value out of sample. Live RULES v2 OOS for
  reference: U56 1.2769 / B136 1.1019 / SMALL 0.6473; SPY OOS 0.8738.

  **GATES 15/15.** G1/G1b fast_run vs `engine.backtest` (returns AND turnover) **0.000e+00**;
  G2 the derived 25 bps rung vs a fresh 25 bps engine run **0.000e+00**; G3 BAND 0.03 on U56
  replays `baseline.compare`'s RULES v2 row to **2.220e-16**; **G4 the realised-gross match, max
  |gap| 1.443e-15 over 66 twins x 2 windows**; G5 two dials; G6 no chooser reads a row on or
  after 2017-01-01, TESTED on truncated IS input; G7 144 of 144 published; G8 max realised target
  gross 0.7500; G9/G10 turnover, realised gross and names held published per cell, filter AND twin.

  **SURVIVORSHIP (rule 9).** U56 / B136 are current-constituent lists and SMALL a current sub-$2B
  screen carried back to 2010, so every absolute level is an UPPER BOUND. The headline is a
  filter-minus-twin contrast inside one panel, same names, same days, same realised exposure, so
  it is first-order immune; the 4b pass counts and the PARK's CAGR leg are not.

  **WHAT THE RECORD SHOULD SAY.** *Eligibility filters are not de-gross in costume — but only on
  the drawdown axis, and only the price-and-volatility gates. Their Sharpe and CAGR are fully
  explained by the exposure they remove, and the effect gets worse with cost. The momentum
  screen's own rank cut is explained by exposure on BOTH axes and should be priced as a gross
  dial from now on. And since the +3.67 pp drawdown gap sits at ~1.25 of idea 1511's paired
  DD-contrast SE, the one surviving axis is not yet significant — idea 1624 is filed to settle it.*

## 2026-09-19 — idea 1653 (lane B): does a CONSTANT-GROSS U56 x SMALL NAV SPLIT clear 4b against its OWN CORNERS and a MATCHED-DE-GROSS TWIN? **NO — THE REALLOCATION DIRECTION IS THE TENTH DE-GROSS IN COSTUME, AND THE FIRST FAMILY BEATEN ON THE DRAWDOWN AXIS TOO. KILL (capital), NO NEW BOOK FROM THE DEVICE — but the appendix turns up a 4b KEEP-CANDIDATE THE RECORD ALREADY OWNED AND NEVER PRINTED.**

  **THE QUESTION, AND WHY IT IS NOT THE USUAL ONE.** Nine consecutive 2026-09-19 runs found every
  device family — trailing stops, breadth throttles, vol targeting, MA-distance gates, SPY filters,
  the drawdown-budget ladder, correlation-cluster caps, the momentum rank cut, the MAXVOL gate —
  beaten at matched exposure by a plain constant de-gross. Every one of those devices **REMOVES**
  exposure. A cross-panel NAV split only **MOVES** it, at constant total gross: it is the one
  direction the record has never priced, and the only lever that can lift CAGR, the 4b leg that
  binds 26 of 36 cells in idea 1617 and kills the live book on its own.

  **DESIGN.** Two dials and no more: `w` (NAV share to the live U56 band book) x `G` (total target
  gross), 11 x 3 = 33 cells, each at 10 / 25 / 50 bps, **99 of 99 rows published**. The other
  sleeve is the identical band book (200d +/-3% hysteresis, no ranking, no vol filter, gate-out to
  cash, weekly, t+1) run on the 665-name SMALL panel. `w = 1` is the live book exactly (G3 replays
  `baseline.rules_v2_weights` to 0.000e+00); `w = 0` is the SMALL book alone. Window
  2011-01-13..2026-09-18 (15.6y, the SMALL panel's intersection). Each cell is paired with a
  constant de-gross of the **U56 book alone**, bisected to carry the blend's OWN **realised** mean
  gross — idea 1617's method, pointed for the first time at the additive direction.

  **THE ANSWER IS NO, AND IT IS THE CLEANEST OF THE TEN.** **dSharpe > 0 in 0 of 30** paired cells
  at 10 bps (mean **-0.2316**), 0 of 30 at 25 and 50 (**-0.2445 / -0.2661**), mean dCAGR
  **-1.08 pp/yr**, and **OOS dSharpe > 0 in 0 of 30** (mean **-0.3448**). CAGR, Sharpe and OOS
  Sharpe are **monotone increasing in `w` at all three G**: every dollar moved out of the incumbent
  costs money on every axis, at every rung, in both windows.

  **AND IT IS THE FIRST FAMILY BEATEN ON THE DRAWDOWN AXIS AS WELL.** Mean **dMaxDD -1.05 pp**
  (18 of 30 shallower, the mean negative), widening to **-1.28 / -1.70 pp** at 25 / 50 bps. That is
  the **opposite sign** from idea 1617's eligibility filters (+3.67 pp), the one family a matched
  de-gross did not dominate. The reallocation direction buys nothing a scalar could not buy cheaper.

  **WHY.** corr(U56 book, SMALL book) daily = **0.7375** (IS 0.8597, OOS 0.6808), and the SMALL
  corner reads **4.26% / 0.6588 / -14.16%** against the incumbent's **8.14% / 1.1636 / -12.05%**.
  A 0.74-correlated sleeve with half the Sharpe and 1.18x the drawdown cannot lift a blend.

  **BOTH KEEP PATHS.** **4a 0 of 33 at 10, 25 and 50 bps.** 4b FULL **3 / 2 / 1 of 33** and 4b OOS
  **3 / 2 / 2** — and **every passer sits at w >= 0.8 with G = 1.00**, maximised at **w = 1.00**,
  i.e. at no split at all. **4a n 4b = 0**, the umpteenth consecutive disjunction. The pass belongs
  to the inherited gross dial and survives DESPITE the device, never because of it.

  **RULE 8.** Four IS-only choosers fitted on 2011..2016-12-31, 2017-2026 read once. C_LIVE
  (w 1.00, G 0.75) OOS **1.2766**; C_PREREG (1.00, 0.75) **1.2766**; C_CALMAR (1.00, 1.00)
  **1.2759**; C_SHARPE (0.80, 1.00) **1.1952**. **C_SHARPE minus C_LIVE = -0.0814**, and **0 of 4
  choosers picks any w below 0.8**. The two that clear 4b OOS get there by raising G, not by
  splitting. Live RULES v2 OOS on this window 9.46% / 1.2766 / -12.05%; SPY OOS 0.8737.

  **THE APPENDIX, AND IT IS THE RUN'S REAL FINDING.** Because every passer sat at G = 1.00 on a
  window whose SPY CAGR bar is 9.81%, the inherited dial was re-read on the LIVE frame's OWN 17.7y
  history (bars MaxDD >= -20.23%, CAGR >= 10.59% FULL / 10.68% OOS). **The live RULES v2 book with
  gross 0.75 -> 1.00 and nothing else changed clears 4b on BOTH windows at 10 AND 25 bps:** FULL
  **11.53% / 1.2008 / -15.91%**, halves **1.2282 / 1.1798** against SPY's 0.9570 / 0.8249; **OOS
  12.67% / 1.2759 / -15.91%**. At the live G = 0.75 the same book reads **8.62% / 1.2010 / -12.05%**
  and fails on the **CAGR floor ALONE** — exactly idea 1454's reading, which is a statement about
  **0.75**, not about the book.

  **PUBLICATION GAP, NOT A DISCOVERY.** Idea 1498's committed grid ALREADY carries
  `keep4b=True, keep4b_oos=True` for (U56, LIVE, G=1.00, F=0.00); its memo §4 and this CHANGELOG say
  the floor "does not close". Both are true — it does not close at 0.75 and it does close two rows
  down the same table. **G11 replicates that committed cell from an independently built frame to
  2.614e-04.** The record computed this on 2026-09-19 and printed the opposite sentence.

  **HONEST LABEL ON THE CANDIDATE: A DE-GROSS REVERSAL, NOT ALPHA.** Sharpe is invariant in G to
  3 dp (**1.2010 / 1.2010 / 1.2009 / 1.2008** across 0.50 / 0.75 / 0.85 / 1.00) because the book is
  never levered and un-invested NAV earns 0.00%/yr; raising G only stops throwing return away. Idea
  1600's deflation applies in full — rho(IS MaxDD, OOS MaxDD) is 1 **by construction** on a pure
  scale dial, so this survives rule 8 as **leverage selection, not forecasting**, and is worth less
  than a signal discovery. Max realised gross **0.7165**; no shorting, no leverage.

  **GATES 12/12.** G0 15.65y; G1 fast_run vs `engine.backtest` (returns AND turnover) **0.000e+00**
  with identical NaN masks; G2 the derived 25 bps rung vs a fresh 25 bps engine run **0.000e+00**
  (cost axis exact); **G3 the w=1, G=0.75 corner replays `baseline.rules_v2_weights` to 0.000e+00 —
  the corner IS the live book**; G4 target gross an exact convex combination of the two corners'
  (2.720e-14) and never above G (0.000e+00); G5 two dials, cost/window/panel published axes; **G6 no
  chooser reads a 2017+ row, TESTED on a hard-truncated array (0.000e+00)**; G7 99 of 99 published;
  G8 max realised gross 0.7165, no shorting; **G9 realised-gross match 3.331e-16 over 90 twins**;
  G10 turnover and realised gross published per cell AND per twin; **G11 independent replication of
  idea 1498's committed G=1.00 cell, 2.614e-04**. Deterministic, offline, 232s.

  **SURVIVORSHIP (rule 9).** U56 is a current-constituent list and SMALL a current sub-$2B screen
  carried back to 2010, so every ABSOLUTE level — including the appendix's 11.53% and its 4b pass —
  is an **UPPER BOUND**. The kill is a blend-minus-twin contrast inside one frame over the same
  names on the same days at the same realised exposure and is first-order immune; the appendix's
  pass is **NOT**.

  **WHAT THE RECORD SHOULD SAY.** *The reallocation direction is not an escape from the de-gross
  result — it is the tenth member of the same family, and the first one a matched de-gross beats on
  the drawdown axis too. The only thing on this grid that clears 4b is the gross dial, and the
  record has owned that number in a committed CSV since this morning while printing the opposite
  sentence. Before any new device is priced, the live book should be re-read at the exposure it was
  never actually run at.* **PROPOSED, NOT ENACTED** (rule 6: Sunday review only) — memo at
  `research/backtests/2026-09-19_cross-panel-nav-split_B.memo.md` carries the exact clause-2 wording.

## 2026-09-19 — idea 1660 (lane C): the matched-exposure twin is a CLOSED FORM, and the record can stop solving for it

**KEEP (method), with a boundary stated in the same breath.** Idea 1649 reported two panels at
in-band shares 0.7051 / 0.5482 and realised gross 0.5293 / 0.4113 at the same target 0.75 — ratios
0.7507 and 0.7503. This run asked whether that is a law, and priced the answer as real books rather
than as gross numbers. Two dials (band c {0.00, 0.01, 0.03, 0.05, 0.10} x target gross G {0.25,
0.50, 0.75, 1.00}); PANEL {U56, B136, SMALL}, CADENCE {W, M, Q}, SLICE {FULL, IS, OOS} and COST
{0, 10, 25, 50} bps published at every value. **8640 rows published.**

**THE FORM HOLDS.** `R / (G * mean in-band share)` over 540 points: U56 mean **0.998846**
(0.975495-1.015020), B136 0.997280, SMALL 1.005391. Realised gross IS target gross times the gate-out
complement, to within 0.12% on the live weekly cadence.

**AND IT IS A WEEKLY FACT, NOT A LAW.** The residual is monotone in the rebalance interval and grows
**16x**: mean absolute error 0.0253 pp weekly, 0.1504 monthly, 0.4137 quarterly (max 0.1253 / 0.8869
/ **1.7249** pp). A held-target-path refinement, also free, halves the tail to 0.6437 pp but is
biased +0.1638 pp rather than centred. The whole cadence term is the stale-weight effect.

**PRICED, THE SUBSTITUTION IS INVISIBLE.** Against pre-registered bars — |dSharpe| < 0.0089 (idea
1617's smallest committed device margin) and |dMaxDD| < 2.93 pp (idea 1511's measured paired
circular-block SE), both fixed before the run — replacing the 44-step bisection with `k = G * mean s`
moves the control by max |dSharpe| **0.000496** and max |dMaxDD| **0.5632 pp** over 180 cells x
FULL/OOS at 10 bps, 18x and 5x inside the bars, and does not drift at 0 / 25 / 50 bps. Using the
cell's own measured realised gross instead (`k = R_cell`, also bisection-free) is tighter still:
0.000169 and 0.2295 pp. **Same-slice KEEP-verdict flips: 0 of 540 on 4a and 0 of 540 on 4b.**

**THE BOUNDARY, PUBLISHED NOT BURIED.** Rule 8 fits the twin on IS rows and reads it OOS, and there
the 1.5 pp of gross the formula adds tips a knife-edge: on U56 quarterly, band 0.00 / G 1.00 — picked
by BOTH C_SHARPE and C_MEMO — TWIN_BISECT (k 0.689525) posts OOS MaxDD **-20.118%** and PASSES the
-20.230% cap, while TWIN_R (0.693907, -20.240%) and TWIN_A (0.704109, -20.523%) FAIL. **2 of 27
chooser rows flip.** The passing margin is 0.11 pp — **1/27th of the 2.93 pp SE the record itself
measured for a MaxDD contrast**. That is not a formula failure; it is a verdict that was never
adjudicable. The memo's proposed rule-4 wording says so: a twin whose gross is fitted on one slice
and read on another, or whose verdict turns on a sub-2.93 pp drawdown margin, MUST still be bisected.

**CAPITAL ARM.** 4b at 10 bps: 13 of 180 CELL books pass FULL, 11 pass OOS, **11 pass both — and all
11 sit at G = 1.00, the top gross rung**, while the band rung wanders freely across 0.00-0.10 among
them. On this grid the 4b pass is an EDGE-OF-GRID GROSS claim, the same sentence the rest of the
2026-09-19 record has written all day. The rule-8 legitimate pick on U56 weekly (C_SHARPE and C_MEMO
agree, IS rows only, 2017-2026 read exactly once) is **band 0.10 / G 1.00**: FULL 11.72% / 1.1726 /
-16.30% (halves 1.247 / 1.107), **OOS 12.14% / 1.1940 / -16.30%**, against SPY FULL 15.12% / 0.8844 /
-33.72% and OOS 15.26% / 0.8738 / -33.72%. It clears **4b on FULL and OOS at 0 / 10 / 25 / 50 bps**,
and its own realised-gross-matched twin FAILS 4b on both slices — at 1.7x the turnover. 4a fails
(live RULES v2 draws -12.05%; path 4a cannot adjudicate a growth book).

**THE HONEST HALF.** Pooled over all 180 cells at 10 bps, the band CELL beats its realised-gross-
matched twin on Sharpe in only **76 of 180 FULL** (mean dSharpe **-0.0407**) and **64 of 180 OOS**
(mean **-0.0469**), while running shallower in 104 of 180 (mean +0.62 pp). The de-gross result
survives a fourth family; the headline cell is one of the 76, not the rule.

**GATES 12/12.** G0 18.68y / 18.68y / 16.68y; G1 fast_run vs `engine.backtest`, returns
**2.776e-17** and turnover 1.943e-16; G2 the derived 25 bps rung vs a fresh 25 bps engine run
**1.735e-17** (cost axis exact); **G3 the (U56, W, c=0.03, G=0.75) cell replays
`baseline.rules_v2_weights` to 1.735e-17 — that cell IS the live book**; G4 bisection quality
**2.900e-14** over every twin; G5 two dials; **G6 no chooser reads a 2017+ row, TESTED on a
hard-truncated array (0.000e+00, argmax identical)**; G7 8640 of 8640 published; G8 max realised
gross 0.982143, no shorting, no leverage, **0 twins infeasible**; G9/G10 turnover, realised gross
and in-band share published per cell and per twin. Deterministic, offline, 695s.

**SURVIVORSHIP (rule 9).** U56 and B136 are current-constituent lists and SMALL a current sub-$2B
screen carried back to 2010, so every ABSOLUTE level — including the 4b pass — is an **UPPER BOUND**.
The twin-minus-twin contrast that carries the method result is inside one frame over the same names
on the same days at the same realised exposure and is first-order immune; the 4b pass counts are NOT.

**WHAT THE RECORD SHOULD SAY.** *The control the record has been paying 44 runs a cell for is one
multiplication, and has been since the convention was written: gated-out weight goes to cash, so
realised gross is target gross times the in-band share. Retire the bisection for same-slice
contrasts. Keep it for the two cases that actually bite — a gross fitted on one window and read on
another, and any verdict whose margin is under the record's own 2.93 pp drawdown SE — and note that
the second case is really an argument for not quoting such a verdict at all.* **PROPOSED, NOT
ENACTED** (rule 6: Sunday review only) — exact wording in
`research/backtests/2026-09-19_band-gate-out-rate-predicts-realised-gross_C.memo.md`.

## 2026-09-20 — idea 1628 (lane cloud): DOES THE MAXVOL 0.60 PARK SURVIVE A BAND CROSS AND A CAGR-FLOOR-CHARGED SPY? **ANSWERED — KILL THE CROSS. PARK CONFIRMED AND STRENGTHENED, BUT RULE 8 DENIES KEEP. NO NEW BOOK.**

  **THE CONSTRUCTION.** Equal weight over the priced constituents passing (vol20 < m) AND the 200d
  MA band of width c, gross 0.75, weekly, 10 bps, t+1, de-gross to CASH. Dials: m in {0.45, 0.60,
  0.80, 1.00, 1.50, inf} x c in {NOBAND, 0.00, 0.03, 0.10} — exactly TWO tuned parameters — on
  U56 / B136 / SMALL. **72 books, every rung published.** The cost axis is not a third dial: 1586's
  identity r(c) = r_gross − turnover*c/1e4 is EXACT (gate G3 = 0.000e+00 against the engine at
  c = 25), so 0/10/25/50 bps are restatements, not refits.

  **Q1 — SUBSTITUTES, NOT ADDITIVE.** The MAXVOL ceiling's Sharpe gain over its OWN no-ceiling twin
  is **+0.0176 with no band and −0.0422 / −0.0420 / −0.0403 once the band is on** (c = 0.00 / 0.03 /
  0.10). INTERACTION = [gain with band] − [gain without] is **negative in 37 of 45 band-on cells,
  mean −0.0590**, and on U56 and B136 the gain flips sign outright (U56 m = 0.45: +0.1141 → −0.0464;
  B136 m = 0.45: +0.1501 → −0.0347). The retired v1 vol gate buys nothing live clause 2 has not
  already bought. Same sign at 25 bps.

  **AND THE CROSS IS WORSE THAN EITHER ALONE.** **0 of 54 band-on cells clear 4b on any panel, FULL
  or OOS**, against 4 of 18 NOBAND cells on FULL. The mechanism is that the two devices fix
  DIFFERENT 4b legs and cannot be held at once: the band de-grosses to ~0.52 mean gross and fails
  the CAGR floor (band OOS CAGR 6.7–9.5% against SPY's 15.26%, floor 10.68%), while the ceiling
  alone holds 0.72 gross and clears it but pays drawdown. Binding legs over all 72 cells: SH 48,
  DD 60, CAGR 12.

  **THE PARK CELL REPLICATES — AND BREAKS AN EIGHT-RUN STREAK.** MAXVOL m = 0.60, no band, U56:
  full **11.52% / 1.1277 / −16.88%**, OOS **12.04% / 1.1762 / −16.88%**; 4b clears FULL *and* OOS at
  0/10/25/50 bps (Sharpe 0.9920 / 0.9774 / 0.9554 / 0.9188). B136 the same. Against the record's
  standing killer — a plain de-gross twin (no ceiling, band unchanged, gross re-scaled so realised
  mean gross MATCHES to 1e-4) — this is the **first device family in the record to survive**:
  **device 4b passes 4 of 60 cells, the matched de-gross twin 0 of 60**, and on the NOBAND cells the
  device is +0.0963 (U56) / +0.0983 (B136) of Sharpe and **+4.81 pp / +5.85 pp SHALLOWER**.

  **BUT THE SURVIVAL IS A CORNER, NOT A LAW.** With the band on the device loses to its matched twin
  in **44 of 45** cells; on SMALL it loses in **15 of 15** (NOBAND −0.1043, mean −0.0855). Pooled over
  all 60 cells the device wins on Sharpe only **11 of 60**, mean dSharpe **−0.0267**. The de-gross
  dominance finding stands everywhere except the un-banded large-cap corner.

  **Q2 — IDEA 1490'S WORRY IS A NO-OP HERE.** Charging SPY the candidate's OWN realised turnover
  moves **0 of 72** 4b verdicts on FULL (4 → 4) and gains exactly **1** on OOS (4 → 5, U56 m = 0.45
  NOBAND). Binding-leg counts are IDENTICAL under both conventions. At 10 bps the 4b bar is not a
  costless-SPY artefact; the re-read is worth publishing but is not a blocker.

  **RULE 8 (2017-2026 read ONCE).** Two IS-only choosers x 3 panels over the joint (m, c) grid:
  **0 of 6 reach the PARK cell** (IS rank #12 / #9 of 24 on U56, #2 / #2 on B136, #11 / #17 on
  SMALL), and the 6 picks clear **4a OOS 0 of 6** and **4b OOS 0 of 6** costless (1 of 6 charged).
  U56's Sharpe chooser takes m = inf, c = 0.10 → OOS 9.08% / 1.1944 / −12.35% against the live book
  at 9.46% / 1.2766 / −12.05% and SPY at 15.26% / 0.8737 / −33.72%. The exposure dial is
  unresolvable in sample, exactly as 1713 found, so PROTOCOL rule 8 forbids KEEP.

  **RESIDUE, not a rules change (rule 6; RULES.md and PROTOCOL.md untouched):** the ceiling and the
  band should never be written into the same clause — they are one device measured twice — and the
  matched-exposure de-gross twin should be a REQUIRED control beside any device claim, since it is
  the only ruler that separates this PARK from the eight families it killed. Gates 3/3.
  Survivorship: U56 / B136 / SMALL are CURRENT constituents; SMALL worst (delisted sub-$2B names
  absent), so every absolute level is optimistic.

## 2026-09-20 — idea 907 (lane cloud): IS THE DELAY-1 DRAWDOWN MOVE A GROSS FACT OR A WIDTH FACT? **ANSWERED — NEITHER OF 887'S TWO READINGS. IT IS A WIDTH FACT, AND ON DRAWDOWN IT IS NOT RELIABLY A COST AT ALL. KILL THE GROSS READING. NO NEW BOOK.**

  **THE DEFECT THIS CLOSES.** Idea 887's reached 4b cell lost 4.51 pp of MaxDD to one further day of
  execution delay at g = 1.00 and 3.50 pp at g = 0.75 on the same width, and the record has been
  reading that pair as evidence that the delay cost SCALES WITH EXPOSURE — i.e. that de-grossing
  buys execution risk back. It is one cell, and it does not replicate.

  **THE CONSTRUCTION.** Names inside the live 200d +/-3% band, ranked by `baseline.score`'s
  composite, top N held equal-weighted at gross g, shortfall to CASH; weekly, 10 bps. Axes:
  **d in {0, 1, 2, 3} EXTRA days beyond the engine's own t+1** x g in {0.50, 0.75, 1.00} x
  N in {5, 10, 20, 40, 80}, on U56 / B136 / SMALL = **180 books, every rung published**. Delay is
  an execution-realism axis and is NEVER tuned: only (g, N) are ever chosen, and only on IS rows,
  which is stricter than the idea's own "max 2 params (delay, gross)" allowance. Gate G2 proves
  `delay=d` is identical to pre-shifting weights AND the rebalance mask by d (0.000e+00).

  **(A) GROSS CARRIES NOTHING.** Regressing dMaxDD(d=1) on nominal gross gives **R² = +0.0012**
  pooled over 45 cells, and **+0.0005 / +0.0062 / +0.0016** within U56 / B136 / SMALL — with the
  slope the WRONG SIGN (−0.40 pp per unit of gross: more exposure, *less* drawdown cost). Realised
  mean gross is no better (+0.0014). Turnover carries +0.1351 pooled and is unstable across panels
  (+0.8063 on U56, +0.0408 on B136), so it is collinearity with width, not a carrier.

  **(B) WIDTH CARRIES IT — AND REVERSES SIGN.** N alone gives **R² = +0.4665**. Mean dMaxDD(d=1) by
  width: N=5 **−0.08 pp**, N=10 **+2.20**, N=20 **+0.83**, N=40 **−2.03**, N=80 **−3.10**. Narrow
  books lose drawdown to a stale trade; wide books GAIN it. A delay cost quoted without its width
  is unreadable.

  **(C) AND ON DRAWDOWN IT IS A COIN FLIP.** Mean dMaxDD(d=1) = **−0.437 pp** (one extra day makes
  drawdown SHALLOWER on average) against an SD of **2.427 pp**; only **21 of 45** cells get worse,
  and 32 of 45 move less than one SD. Same at d=2 (−0.54 pp, 21/45) and d=3 (−0.79 pp, 17/45).
  **887's pair does not replicate: g=1.00 loses more than g=0.75 at matched width in 8 of 15
  pairs.**

  **THE ONE LEG THAT DOES HAVE A SIGN IS SHARPE.** dSharpe(d=1) is negative in **37 of 45** cells,
  mean **−0.0357** (SD 0.0456); dCAGR −0.285 pp. Delay is a real RETURN cost and a non-cost on
  drawdown, so the two must never be collapsed into one "execution realism" number.

  **DELAY DOES NOT BREAK 4b — IT ADDS PASSES.** 4b FULL passes run **3 / 2 / 4 / 4** across
  d = 0/1/2/3 and 4b OOS **4 / 3 / 4 / 4**, with a NEW pass appearing at d=2 and d=3. Of the 3 cells
  clearing 4b FULL at d=0, 2 survive d=1 and 3 survive d=2 and d=3.

  **RULE 8 (2017-2026 read ONCE, at every delay).** Two IS-only choosers x 3 panels, (g, N) fixed on
  2009-2016 at d=0: the 6 picks clear **4a OOS 0 of 6 at every delay**, and 4b OOS runs
  **1/6 → 0/6 → 1/6 → 1/6** as d goes 0 → 3. U56's Calmar pick (g = 1.00, N = 10) clears 4b OOS at
  d=0 (12.59% / 0.8888 / −18.78%), LOSES it at d=1, and regains it at d=2 and d=3 against a live
  book at 9.46% / 1.2766 / −12.05% and SPY at 15.26% / 0.8737 / −33.72%. A 4b pass that blinks with
  one day of execution delay is noise, not robustness. Mean OOS Sharpe move at d=1: −0.1357.

  **RESIDUE, not a rules change (rule 6; RULES.md and PROTOCOL.md untouched):** any published delay
  or execution-realism cost must carry its WIDTH and its dispersion, and must quote the Sharpe and
  the MaxDD legs separately — the first has a sign, the second does not. Gates 3/3. Survivorship:
  U56 / B136 / SMALL are CURRENT constituents; SMALL worst (delisted sub-$2B names absent), so
  every absolute level is optimistic.

## 2026-09-20 — idea 775 (lane B): IS THE U56 FLOOR ADVANTAGE A DRAW-OVERLAP ARTEFACT? **ANSWERED / SPLIT — KILL THE U56 READING. THE SIGN OF THE ADVANTAGE IS SET BY THE MATCHING CONVENTION. NO NEW BOOK.**

  **THE DEFECT THIS CLOSES.** Idea 567's per-parent draw floor (U56 0.050224, B136 0.099511,
  SMALL439 0.094077, max/min 1.9813) has been used as a BAR: a cross-panel margin counts as
  evidence only if it clears its parent's floor, and 558 of the 607 census claims name U56, whose
  floor is the narrowest. But U56's floor is measured by drawing k = 36 of M = 55 names, so two
  draws share 65% of their constituents by construction against B136's 27% and SMALL's 5%.

  **THE CONSTRUCTION.** Idea 567's module is IMPORTED, not copied: its crc32 draw seeds, its
  EWall / MA-RS books at gross {0.50, 0.75, 1.00} x cadence {W, M}, 10 bps, t+1, warm-up 260, and
  its floor estimator (mean over the six cells of the sd across draws). Only the DRAW SCHEME moves:
  **K RULE {FIXED_K, RATIO_K (k = phi*M, overlap matched), DISJOINT (partitioned draws, overlap
  EXACTLY 0)} x LEVEL (k {12,24,36} / phi {0.0541, 0.2667, 0.6545})** = 8 cells x 3 parents x 24
  draws, every rung published.

  **(A) THE PAIRWISE ANSWER — ARTEFACT.** The **U56/B136 floor ratio runs 0.6517 .. 1.5874** across
  the eight schemes. At 567's own rung (k = 36 fixed) U56 is **0.652** of B136 with P(U56 narrower)
  **0.994**; at MATCHED expected overlap (phi 0.2667 and 0.6545) U56 is **1.504x and 1.587x WIDER**
  with P **0.025 / 0.005**. Its bootstrap interval covers 1.0 in **5 of 8** cells; U56 is the
  narrowest-floor parent in **4 of 8** and the **WIDEST in 2**.

  **(B) THE THREE-PARENT SPREAD SURVIVES — BUT IT IS SMALL, NOT U56.** Mean max/min over the
  matched- and zero-overlap arms is **1.5924** against 567's 1.9813, so the pre-registered
  H_OVERLAP (< 1.25) is FALSIFIED and H_PANEL (>= 1.50) HOLDS as written. The noise null the
  statistic needs: three sd estimates of ONE true floor at dof 23 give max/min **1.2680 median,
  1.6601 at the 95th**, and only **4 of 8** cells' bootstrap intervals (2,000 resamples of the
  draws, of the partitions on DISJOINT) exclude even that median.

  **(C) WHY — THE FINITE-POPULATION LAW.** implied `sigma_p = floor / sqrt((M-k)/(k(M-1)))` reads
  **U56 0.4417, B136 0.4618, SMALL665 0.7046**: U56/B136 = **0.9565**, 4.4% apart. Pooled
  log(floor) on log(scale) has slope **+0.6545** (the iid law predicts +1 — names inside a parent
  are correlated) at **R2 0.7549**; parent dummies add **dR2 +0.1278**, carried by SMALL665
  **+0.3887** against B136 +0.0509. The one genuine panel fact is that sub-$2B names are ~57% more
  dispersed than large caps.

  **(D) CAPITAL — KILL.** 6,912 books at 10 bps, t+1: **4a 11, 4b FULL 340, 4b OOS 362, BOTH 1**;
  **SMALL665 passes 0 of 2,304** on every path; the binding 4b leg is DD (1,958 rows) then CAGR
  (983). Rule 8 (fitted <= 2016-12-31, 2017-2026 read ONCE): **4a OOS 0/15, 4b OOS 4/15**, and the
  floor is ANTI-informative as a selector — **C_FLOORMIN mean OOS Sharpe 0.8987 against its mirror
  C_FLOORMAX 0.9624** (d -0.0637, narrower floor wins 1 of 3 parents), both below do-nothing
  **C_LIVE 0.9747**. U56's C_FLOORMIN book clears 4b FULL and OOS (11.86% / 1.1212 / -17.76%,
  H1/H2 1.207/1.059; OOS 12.65% / 1.1340 / -17.76%) against SPY 15.12% / 0.8843 / -33.72% and live
  RULES v2 8.62% / 1.2010 / -12.05% — but so does C_FLOORMAX, so nothing was chosen, and the book
  underneath is the record's existing MA-RS gate at gross 0.75, prior art idea 774 already declined
  to claim. No candidate, no memo.

  **PUBLISHED, NOT REPAIRED (gates 22 of 24; the two failures ARE the finding).** 567's committed
  floors do not reproduce even on **567's own tape end dates** (G2b max |dev| **4.770e-04**; G2 on
  today's tape **2.147e-03**) although the RATIO does (1.9855 vs 1.9813) — so the construction is
  verbatim and the drift is DATA: cache restatement plus 5-10 extra trading days. The SMALL parent's
  2026-09-11 rebuild (439 -> 665 names) moved its floor **0.094077 -> 0.063317, -32.7%**.

  **RESIDUE, not a rules change (rule 6; RULES.md and PROTOCOL.md untouched):** a per-parent draw
  floor must carry its **k/M** or be quoted in overlap-free units, and a max/min over parents must
  be quoted against its own chi/bootstrap null. Survivorship: U56 / B136 are CURRENT constituents
  and SMALL665 a CURRENT sub-$2B screen, so every absolute level is optimistic; the headline is a
  within-parent dispersion and is first-order immune, the 4b counts are not.
