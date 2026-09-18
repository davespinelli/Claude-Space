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
