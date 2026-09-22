# Idea 2077 (lane C, 2026-09-22) — LEVER THE BAND BOOK: THE FINANCING FRONTIER
**ANSWERED. Financing is NOT what kills levered band books — the 4b DRAWDOWN CAP is, at every
financing rung including 0%/yr. KILL of the financing hypothesis. NO NEW KEEP.**

Script `2026-09-22_lever-the-band-book-financing-frontier_C.py`; 72 cells published
(`.grid.csv`), plus `.breakeven.csv`, `.clause.csv`, `.walkforward.csv`, `.convention.csv`,
`.log.txt`. Two tuned dials and no more: FIN MODEL {0,2,4,6,8 %/yr flat, TV_SHY} x GROSS
{0.75,1.00,1.25,1.50,1.75,2.00}. Band 0.03, weekly cadence, 10 bps — all fixed at the live
book's values. Panels U56 / B136, price-only on the committed caches. Survivorship: current
constituents on both panels.

## Gates (printed before any hypothesis was read)
* **G1** local `run()+net()` == `engine.backtest(band .03, gross .75, 10 bps)`, max|diff| **0.000e+00** on both panels.
* **G2** borrowed NAV is identically 0 at gross <= 1.00 (max held gross **0.9822**), so the financing charge cannot touch the unlevered comparands.
* **G3** TV_SHY well-formed: mean **3.24%/yr**, min 1.50%, max 8.46%, 0 NaN, lagged one day.
* **G4** SPY is unlevered buy-and-hold and financing-invariant by construction.

## The mechanism, and why the answer is what it is
**The nominal gross dial is a CAP, not a level.** At nominal gross 1.25 the band book's mean
HELD gross is **0.888** (U56) / **0.887** (B136): it borrows on only **43.1%** / **40.1%** of
days and, when it does, only **7.6%** / **8.7%** of NAV. Mean borrowed over the whole sample is
**0.033 / 0.035**. The 200d band is out often enough that a "1.25x book" is levered a minority
of the time, so the financing bill at 8%/yr on that rung is **26 bps/yr** (U56 CAGR 14.46% ->
14.16%) and at the TV proxy **12 bps/yr**.

## Q1 — BREAK-EVEN FINANCING RATE r* (model-free; `.breakeven.csv`)
Flat rate at which the levered cell's CAGR falls back to the gross-1.00 book's, FULL sample:

| gross | U56 r*_unlev | B136 r*_unlev | U56 r*_4b floor | B136 r*_4b floor |
|---|---|---|---|---|
| 1.25 | **78.94%** | **68.66%** | never (CAGR floor never reached) | 69.73% |
| 1.50 | 31.70% | 30.13% | 36.91% | 30.37% |
| 1.75 | 23.96% | 22.50% | 26.62% | 22.62% |
| 2.00 | 20.92% | 19.44% | 22.68% | 19.52% |

OOS (2017–2026) reads the same or higher (1.25: 85.98% / 80.19%). Against TV_SHY's own mean of
3.24%/yr, the gross-1.25 rung has **24x** headroom and even gross 2.00 has **6x**. No plausible
funding path is within an order of magnitude of the break-even.

## Q2 — BREAK-EVEN GROSS g* (B3)
**There is none on this ladder.** At every financing rung from 0% to 8%/yr and under TV_SHY,
on BOTH panels, every levered rung {1.25, 1.50, 1.75, 2.00} still out-CAGRs gross 1.00.
Financing never reverses the ladder; it only flattens it (U56 gross 2.00: 23.27% at 0%,
18.64% at 8%, still above 11.53%).

## Q3 — DOES ANY LEVERED CELL SURVIVE A REALISTIC BORROW COST ON THE 4b MARGIN?
**On the grid, yes — and that is exactly why financing is not the story.** 4b FULL passes
**12 of 36 on each panel**, and the passing set is *identical at all six financing models*:
gross 1.00 and gross 1.25, never anything above. **10 of 40** levered cells carrying a non-zero
financing charge pass 4b FULL (all of them gross 1.25); 10 of 40 pass 4b OOS. Every rung >= 1.50
fails the 4b DD cap **at 0%/yr too** (U56 gross 1.50 MaxDD −23.38% against a −20.23% cap).
**The binding constraint is drawdown, not the borrow desk.** 4a: **0 of 72** — no levered cell
beats the live book's drawdown, as expected of a book that scales it linearly.

## Rule 8 — walk-forward (params on 2009–2016 only, 2017–2026 read once)
| panel | chooser | IS pick | OOS CAGR/Sharpe/MaxDD | OOS 4b | OOS 4a |
|---|---|---|---|---|---|
| U56 | gross only, fin fixed TV_SHY (headline) | gross **1.25** (1/6 IS-legal) | **15.74% / 1.263 / −19.70%** (halves 1.418/1.093) | **True** | False |
| U56 | gross only, fin fixed FLAT4 | gross 1.25 | 15.76% / 1.264 / −19.70% | True | False |
| U56 | both dials free | FLAT0, gross 1.25 | 15.91% / 1.275 / −19.69% | True | False |
| B136 | gross only, fin fixed TV_SHY (headline) | gross **1.00** (2/6 IS-legal) | **10.47% / 1.101 / −16.16%** | **False** (CAGR 10.47% vs floor 10.68%) | False |
| B136 | gross only, fin fixed FLAT4 | gross 1.00 | 10.47% / 1.101 / −16.16% | False | False |
| B136 | both dials free | FLAT0, gross 1.25 | 13.10% / 1.099 / −19.99% | True | False |

OOS comparands: U56 RULES v2 9.46%/1.277/−12.05%, SPY 15.29%/0.875/−33.72%; B136 RULES v2
7.85%/1.102/−12.24%, same SPY. **4 of 6 arms clear 4b OOS, 0 of 6 clear 4a.**

## THE ONE THING FINANCING ACTUALLY DOES — and it is procedural, not economic
On B136 the IS-Sharpe chooser prefers gross **1.25** at 0%/yr by **0.00089** of IS Sharpe
(1.094095 vs 1.093209) and flips to gross **1.00** at *every* non-zero financing model,
TV_SHY included. That 0.0009 reordering is the whole difference between an OOS 4b **PASS**
(13.10% CAGR) and an OOS 4b **FAIL** (10.47% against a 10.68% floor — a miss by 21 bps).
So a cost that needs **69%/yr** to matter economically changes the capital pick at **2%/yr**,
purely through the chooser. This is the chooser-fragility idea 2087/2101 measured, reached
from a completely different direction.

## IDEA 914's CLAUSE KILLS THE LEVERED CANDIDATE (`.clause.csv`)
Every 4b pass re-read across the book's own five weekly rebalance offsets (the book is always
reported at d=0):
* **gross 1.25** (the rule-8 pick): DD margin **+0.54 pp** (U56) / **+0.24 pp** (B136) against
  its own 5-offset DD spread of **3.00 pp** / **2.86 pp** — unresolved by **5.5x / 12x** — and
  the 4b verdict holds at only **4 of 5 offsets** on both panels, at every financing model.
* **gross 1.00** (U56 only): CAGR margin +0.93 pp (FULL) / +1.97 pp (OOS) vs a 0.54 / 0.58 pp
  spread, DD margin **+4.32 pp** vs a 2.40 pp spread, **5 of 5 offsets** — the only cells in
  this whole run that are weekday-robust. Overall **12 of 42** clause rows resolved, and the
  resolved twelve are all the U56 gross-1.00 cells.

## Why there is still no KEEP
The only weekday-robust 4b passer (U56, gross 1.00, band 0.03 — i.e. the live book with the
de-gross removed) is **not reachable by rule 8**: its IS CAGR is **10.16%** against the IS 4b
floor of **10.47%**, so a 2016 chooser could not legally have picked it (it misses by 31 bps).
The cell rule 8 does reach (gross 1.25) fails idea 914's standing clause. **PARK, not KEEP** —
memo filed.

## Convention sensitivity (B7, `.convention.csv`) — reported, never picked on
Under the record's 0%-on-idle-NAV convention the de-grossed live book earns nothing on its
25% cash. Letting idle NAV earn (fin − 150 bps) lifts U56 gross 0.75 from 8.62% to 11.97% at
8%/yr and makes it a **4b FULL passer at FLAT6 and FLAT8** (and B136's at FLAT8). The record's
cash convention is therefore load-bearing for the live book's own 4b standing in a high-rate
world, in the opposite direction from the one this idea was chasing. Left as a stated
sensitivity; no verdict is read off it.
