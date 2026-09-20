# Idea 1709 (lane C, 2026-09-20) — the rule-8 pick instability is a PLATEAU ARTEFACT

**Script:** `research/backtests/2026-09-20_rule8-pick-margin-vs-deletion-noise_C.py`
**Artifacts:** `2026-09-20_rule8-pick-margin-vs-deletion-noise_C/` (grid.csv 600 cells, margins.csv,
band_ladder.csv, committed_cells.csv, move_events.csv, plateau.csv, walkforward.csv, loyo_*.csv,
gates.csv 21/21 pass, log.txt).  Dials: BAND c (10 rungs incl. NOGATE) x GROSS G (20 rungs);
panels U56 / B136 / SMALL published, not a dial.  Weekly, 10 bps, t+1, no leverage.

## The question
Idea 720 found rule 8's pick moves at 8 of 12 chooser x panel pairs under a one-year IS deletion.
A count of moves cannot say whether the surface is FLAT (ties reshuffling) or the preference is
REAL but unstable.  1709 measures the margin and compares it to that same margin's own noise.

## The answer: FLAT, at every single move event
- **0 of 10 LOYO move events go to a rival the undeleted IS window could resolve** (|t| > 2 on the
  paired leave-one-year-out SD).  Median |t| at a move event **0.292**, max **1.123**.  10 of 10
  moves cross to a different BAND, none to the adjacent gross rung.
- The rank-2 rival is a near-duplicate — same band, one gross rung down, mean margin **0.0002** of
  IS Sharpe — so the rank ladder measures grid resolution, not preference.  On the ladder that
  matters (best cell in each OTHER band) only **12 of 27** cross-band rivals are resolved, median
  |t| **1.65**, mean margin 0.0715 against a mean paired deletion SD of 0.0378.
- Of the record's three committed cells, only **3 of 9** (panel, book) pairs are distinguishable
  from their own panel's IS argmax.  B136's committed PICK sits 0.0011 of IS Sharpe below that
  panel's argmax against a paired SD of 0.0493 — t = +0.02.

## But flatness is a HAZARD, not a comfort (the capital half)
- The IS window cannot separate its argmax from **100 of 200 cells on average (50.2% of the grid)**.
- Across those IS-indistinguishable cells the OOS outcomes are NOT alike: OOS CAGR runs **0.28% to
  18.27%**, OOS MaxDD **-0.84% to -44.38%**, OOS Sharpe spread 0.0683, and only **10 of 301**
  plateau cells clear 4b OOS.
- Three LEGAL IS-only tie-breaks of the SAME tie (C_PLAT_LO / MID / HI) spread OOS CAGR by
  **8.97%** on average.  The chooser is not choosing; the tie-break is.

## Rule 8 (2017-2026 read ONCE per chooser)
4 of 21 chooser x panel picks clear 4b OOS, **2 of 21 clear 4a OOS**; mean OOS Sharpe 0.9472
against SPY's 0.8738.  U56 C_SHARPE reaches `c0.10/g1.00` (OOS 12.14% / 1.1940 / -16.30%, 4b OOS
PASS) — but that is the record's ALREADY-COMMITTED 2026-09-19 pick, not a new book.
OOS bars: SPY 15.26% / 0.8738 / -33.72%; RULES v2 U56 9.46% / 1.2769 / -12.05%, B136 7.85% /
1.1019 / -12.24%, SMALL 3.64% / 0.5459 / -14.16%.
Both KEEP paths over all 600 cells: 4a FULL 59 (all SMALL), 4a OOS 69, 4b FULL 26, 4b OOS 31,
BOTH 20.  **No new KEEP candidate is proposed** — every 4b-clean cell is in the known high-gross
region the record already holds, and this run's own measurement says no legal IS-only chooser can
be trusted to land on it.

## Proposed (for Sunday review only; PROTOCOL.md NOT modified)
Rule 8 should say WHICH argmax and publish its margin: quote every walk-forward pick with the
paired leave-one-IS-year-out t against its best cross-band rival.  Below |t| = 2 the pick is a
tie-break, and a pick that is a tie-break should not be quoted as a preference.

## Survivorship (rule 9)
U56 / B136 are current-constituent lists; SMALL is a current-screen sub-$2B panel with every name
whose max 1-day move >= 1.0 dropped (54 dropped, 666 columns remain).  Absolute levels are UPPER
BOUNDS; the object measured here is the SEPARATION of two cells on one fixed tape.
