# Idea 865 — do 4b's H1/H2 LEGS inherit the SAME SINGLE-EPISODE COMPARAND DEFECT as its DD CAP?

**Lane C, 2026-09-15.  ANSWERED: NO as a VERDICT, YES as a MECHANISM — and the mechanism is
LARGER than the DD cap's.  KILL for capital; nothing promoted; RULES.md, PROTOCOL.md, scan.py,
bot.py and baseline.py untouched.  A PROTOCOL line is proposed under rule 6, not applied.**

Script `2026-09-15_do-4b-H1-H2-LEGS-inherit-the-SINGLE-EPISODE-COMPARAND-DEFECT_C.py`
(deterministic, seed 865, no network).  Two tuned dials, exactly the two the queue names: PASS
SET {SHELF, GRID} × EPISODE SET {QUEUE2, REAL5, PLACEBO3}.  All 4 × 3 grid points reported; the
half convention {COUNT, DATE} is a reported control at every cell, not a third dial.

## Gates (all PASS, printed before any new number)

| | |
|---|---|
| G1 | empty splice == unspliced, `max\|d\| 0.000e+00` |
| G2 | **8 of 8** committed 4b memos rebuild from their own RULES wording inside tolerance (max dSharpe 0.0202, max dMaxDD 1.09 pp).  `b136-corr-hi-q017-w252-d050-D-g100` still does not rebuild at all — named and excluded, as in 851/861 |
| G3 | SPY full **15.1631% / 0.8861 / −33.7173%** vs the record's committed comparand, `max\|d\| 4.50e-05`.  Its half Sharpes, the object of this run: **H1 0.9595 / H2 0.8259** |
| G4 | **861 cross-run replication**: SPY MaxDD ex-COVID_TIGHT **−24.4964%** vs 861's −24.50%, re-priced cap **−14.6978%** vs −14.70% (both `\|d\| 0.0000`) — this census is comparable with 861's DD census row for row |
| G5 | halves disjoint + exhaustive at all 18 (strip, convention) cells; COUNT == `baseline._row`'s own `len(r)//2` at `0.000e+00`; COUNT == DATE on the unstripped leg at `0.000e+00` |
| G6 | the clause is a conjunction (HALFMIN ≤ every (strip, half) margin) on **528 of 528** rows |

Calendar note: the broad cache is refreshed weekly (PROTOCOL rule 9) and today runs one session
behind the U56 cache, so both panels are truncated to their common 4,703 days ending 2026-09-11
(1 U56 day dropped).  861 ran on a day when the two already agreed; G4 shows the truncation
costs nothing.

## Part A — the half-margin census (new: the record publishes both half Sharpes, never the margin)

1,584 rows (44 books × 9 strips × 2 rungs × 2 conventions) in `.margins.csv`.
At the headline cell (10 bps, COUNT), **SHELF 8 of 8** and **GRID 19 of 36** pass 4b unstripped.

* SHELF half margins (book half Sharpe − SPY's, the weaker half = HALFMIN): median **+0.2045**,
  min **+0.1299** (`b136-r620-gross065-W`), max +0.3218.  **0 of 8 clear by under 0.10.**
* GRID: median +0.1565, min **+0.0205**, **3 of 19 clear by under 0.10**.
* 861's companion number on the identical rows, the DD leg: median **+1.75 pp**.

## Part B — the clause, and the answer

**4b-HALF-STRIP**: both half legs must clear at every single-episode strip, SPY's halves re-read
on each stripped leg.  Against 861's **4b-DD-STRIP** on the same books, same strips, same run:

| cell | HALF clause kills | DD clause kills (861's, re-derived here) |
|---|---|---|
| SHELF @ 10 bps, QUEUE2 | **0 of 8** | **3 of 8** |
| GRID @ 10 bps, QUEUE2 | **2 of 19** | **13 of 19** |
| SHELF @ 25 bps, QUEUE2 | 2 of 7 | 3 of 7 |
| GRID @ 25 bps, QUEUE2 | 2 of 14 | 11 of 14 |
| every PLACEBO3 cell | 0 | 0 |

**H_INHERIT FAILS (0 of 8).**  As a verdict the half legs do **not** inherit the DD cap's defect:
at the headline cell the clause that retires three of the record's committed 4b passes through
the drawdown leg retires **none** of them through the half legs.

**And the binding episode is the other one.**  On the SHELF at 10 bps, HALFMIN is set by
**BEAR2022 in 5 of 8 books** and COVID_TIGHT in 3 — against 861's DD leg, where **COVID_TIGHT
bound 16 of 16 kills and BEAR2022 bound nothing**.  The two legs are sensitive to different
episodes, which is the sharpest single reason to call them different defects rather than one.
(H_BEAR as pre-registered — "BEAR2022's own half-kill count ≥ 1" — **FAILS at 0**, because
nothing at all dies at 10 bps; the binding-strip count above is the measurement that survives.)

## Part B1 — which side moves: the queue's premise is CONFIRMED, and it is large

`d margin = dBOOK − dCOMP`, exactly (residual `0.000e+00` over 2,816 decompositions).

SPY's own H2 Sharpe under a single-episode strip:

| strip | SPY H1 | SPY H2 | SPY MaxDD |
|---|---|---|---|
| NONE | 0.9595 | 0.8259 | −33.72% |
| COVID_TIGHT | 0.9521 (−0.0074) | **1.1044 (+0.2785)** | −24.50% |
| BEAR2022 | 0.9410 (−0.0186) | **1.1195 (+0.2936)** | −33.72% |

Deleting 2022 raises the H2 bar by **+0.2936 Sharpe units, 36% of SPY's own unstripped H2** —
relatively a *bigger* comparand move than the DD cap's (−33.72% → −24.50%, 27%).  Idea 863's
reading of its own failure was right about the mechanism.

**Why it does not reach the verdict — the hedge.**  Offset = mean dBOOK / mean dCOMP:

| strip | half | mean dCOMP | mean dBOOK | offset | mean d margin |
|---|---|---|---|---|---|
| COVID_TIGHT | H2 | +0.2785 | +0.2167 | **0.78** | −0.0618 |
| BEAR2022 | H2 | +0.2936 | +0.2304 | **0.78** | −0.0631 |
| COVID_TIGHT | H1 | −0.0074 | −0.0150 | 2.02 | −0.0076 |
| BEAR2022 | H1 | −0.0186 | −0.0440 | 2.37 | −0.0254 |

The book is long the same episode as the comparand, so **78% of the comparand's H2 shift is
absorbed by the book's own H2** and only −0.063 reaches the margin.  The DD cap has no such
hedge: a book's own binding drawdown need not lie inside the stripped episode, which is exactly
why 861's clause bit and this one does not.  On H2 the comparand carries the majority of the
movement (mean comparand share **0.55–0.57**); on H1 the book does (0.31).

**The erosion is real even where the verdict does not move** (the number the record never
publishes):

| cell | median HALFMIN, unstripped → stripped | margin eaten |
|---|---|---|
| SHELF @ 10 bps | +0.2045 → **+0.1555** | 23.9% |
| GRID @ 10 bps | +0.1565 → +0.1291 | 17.5% |
| SHELF @ 25 bps | +0.0870 → **+0.0372** | **57.2%** |
| GRID @ 25 bps | +0.0590 → +0.0193 | **67.4%** |

At 10 bps the SHELF's minimum margin falls +0.1299 → **+0.0629** and one row lands under +0.10;
on GRID the minimum goes **+0.0205 → −0.0147**, i.e. negative.  The cost rung, not the episode
set, is what decides whether the erosion reaches a verdict.

## Part B2 / B3 — controls

* **Boundary channel** (the leg the DD cap does not have: `h = len(r)//2` moves the midpoint when
  days are deleted — up to **98 trading days** across the boundary for BEAR2022, from 2017-11-07
  to 2017-06-19).  Freezing the midpoint by DATE never kills *more*, and kills fewer in 2 of the
  cells where anything dies (GRID QUEUE2 2 → 1; SHELF 25 bps 2 → 1).  H_BOUNDARY as
  pre-registered **FAILS** only because its declared cell (SHELF/QUEUE2) has 0 kills under both
  conventions; the one-directional pattern is the readable result.
* **PLACEBO3** kills 0 at every 10-bps cell (and 1 of 7 at SHELF 25 bps, where QUEUE2 kills 2 —
  so the 25-bps kills are **not** cleanly separable from the convention, and nothing is claimed
  from them).
* **Shuffle null**, 20 random 35-day strips, seed 865: **0 kills on every draw**, SPY's spliced
  halves ranging H1 0.9468–0.9925 / H2 0.7511–0.8645.  Unlike 861's DD null this one is not
  inert by construction — both halves move on every draw — and it still cannot flip a leg.  The
  committed shelf's half margins are simply wider than a single episode is worth.

## Part C — rule 8 (required)

Dials chosen on 2009-2016 alone; 2017-2026 read once per (panel, episode set, chooser).
The half clause as an in-sample screen cuts the pool (U56 18 → 7 eligible, B136 18 → 14) and
**changes the pick at 0 of 6 cells**: SCREENED − UNSCREENED OOS Sharpe = **+0.0000 at all six**.
**H_R8 PASS** — it is a reporting requirement, not an alpha filter.

| panel | pick | OOS CAGR / Sharpe / MaxDD | RULES v2 OOS | SPY OOS | 4b / 4a |
|---|---|---|---|---|---|
| U56 | `band0.08-g1.00` | **12.04% / 1.1654 / −19.05%** (H1 1.246 / H2 1.079) | 9.47% / 1.2782 / −12.05% | 15.33% / 0.8767 / −33.72% | PASS / FAIL |
| B136 | `band0.08-g1.00` | **11.05% / 1.0974 / −19.50%** (H1 1.218 / H2 0.963) | 7.88% / 1.1059 / −12.24% | 15.33% / 0.8767 / −33.72% | PASS / FAIL |

Both picks and both OOS triples are **identical to 861's**, which is the intended cross-run
check and not a new candidate: these books are already on the record, nothing here promotes
them, and both still fail 4a.  Their OOS half-clause margins are +0.1273 (U56) and **+0.0318**
(B136) — the B136 pick clears the half legs out of sample by three basis points of Sharpe.

## The PROTOCOL line proposed (rule 6, NOT applied)

> **4b half-leg reporting.**  A 4b pass must publish, beside each half Sharpe, (i) the
> comparand's half Sharpe on the same leg and (ii) the **half margin**.  A margin below
> **0.10** must additionally be quoted against the comparand's own single-episode range
> (SPY's H2 moves +0.28 to +0.29 under a 2020 or 2022 strip), because a margin inside that
> range is not distinguishable from the episode composition of the comparand.
> 861's conjunctive **4b-DD-STRIP** clause is **not** extended to the half legs: its kill set
> here is empty on the committed shelf at 10 bps, and its 25-bps kills are not separable from
> the placebo.

On the record as it stands this retires **0 of 8** SHELF passes and flags **3 of 19** GRID
passes for the extra quotation.

## Survivorship and scope

U56 and B136 are current-constituent lists, so every CAGR and drawdown **level** is optimistic;
the strip-to-strip **difference** is the durable part.  No capital claim, no KEEP, no promotion.
