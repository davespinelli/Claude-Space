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
