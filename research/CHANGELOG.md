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

