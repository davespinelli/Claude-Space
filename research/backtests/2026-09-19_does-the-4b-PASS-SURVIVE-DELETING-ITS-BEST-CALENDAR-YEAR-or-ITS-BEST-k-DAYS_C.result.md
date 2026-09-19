# Idea 1690 (lane C, 2026-09-19) — does the 4b PASS survive deleting its best calendar year or its best k days?

**VERDICT: ANSWERED / KILL (capital) — no new book, and the standing candidate is not promoted.
The 4b pass of the 2026-09-04 KEEP-4b candidate is a ONE-DAY result. The smallest deletion that
flips it is k = 1: one trading day, 2020-03-16 — and it is not one of the BOOK's days, it is
SPY's worst day. Every flip on every unit is the same leg, DD, and the mechanism is always the
BAR moving, never the book breaking. The RETURN side is indestructible: after deleting the 20
best days the four return legs are all still positive and two of them are WIDER than at k = 0.**

## What was run
The frozen 2026-09-04 candidate (U56 / composite 21-252, 0-126, 0-63 RAW / **no vol scaler** /
above own 200d MA and vol20 < 0.60 / top **N = 20** equal weight / min hold **H = 126** /
**gross 0.75** of NAV, gated-out weight to CASH / weekly), 10 bps, decide-at-t / apply-at-t+1,
260-row warm-up. The book is **not rebuilt** — positions are history. What is deleted is the
**scoring window**: a set of days is removed from the daily return stream of the BOOK, of SPY and
of LIVE RULES v2 **identically**, so the 4b bar moves with the tape, and all five 4b legs plus
the three 4a legs are recomputed on the surviving days.

Dials: **UNIT {YEAR, DAY_BOOK, DAY_SPY, DAY_ADV}** x **k** (0..6 YEAR, 0..20 DAY_BOOK/DAY_SPY,
0..10 DAY_ADV). YEAR and DAY_ADV are **adversarial greedy** — at each step take the deletion that
most erodes the weakest surviving 4b margin (scale-free objective: margin / |anchor margin|), so
they answer the idea's question literally ("the SMALLEST deletion that flips"). DAY_BOOK / DAY_SPY
are the classic ranked best-day cuts. Published and **not** dials: PANEL {U56, B136, SMALL665},
CONVENTION {SPLICE, ZERO}, BAR {MOVES, FROZEN}, arena {FULL, IS, OOS}.
**979 grid points, every one published** in `.grid.csv`; 63 flip-depth rows in `.depth.csv`;
52 exhaustive single-year rows in `.years.csv`; 16 rule-8 rows in `.walkforward.csv`;
3 rows in `.overlap.csv`; 5 gates in `.gates.csv`. 149s, offline, deterministic.

**TWO CONVENTIONS, BOTH PUBLISHED, NEITHER A DIAL.** Idea 1254 published the method fix worth
inheriting — splicing a cut can manufacture a drawdown that never happened — and answered it with
**DD_SEG** (worst drawdown *within* a contiguous surviving segment, never spanning a cut). DD_SEG
is right for YEAR, which makes one long cut. It is **wrong for scattered single days**: the book's
best days sit inside its deepest drawdowns, so a splice cuts the drawdown path exactly where it
hurts and DD_SEG then flatters the book by construction. So `SPLICE` (drop the day, MaxDD = DD_SEG)
is the headline for YEAR and `ZERO` (set that day's return to 0 in all three streams; calendar,
compounding and drawdown paths stay contiguous) is the headline for DAY_*. Every cell is computed
under both.

**GATES: 4 of 5 pass, and the one that fails is published rather than patched.** G1b: on 1254's
own tape (2009-01-13..**2026-09-16**, 4,446 days) this book replays the committed U56 triple
**0.1571 / 1.1480 / -0.1913 exactly**. G1, the same check on *this* run's window, FAILS at a 5e-3
tolerance (0.1580 / 1.1537 / -0.1913) for one reason: the committed cache has grown by **two
trading sessions**, and SPY (0.8844 vs 0.8815) and LIVE v2 (1.2011 vs 1.1982) drift by the same
+0.003 in the same direction. The tolerance was not loosened. G2/G3 replay 1254's SPY and LIVE v2
triples; **G4 is a cross-run gate — k = 1 over the ten OOS years on U56 gives 9 of 10 passing,
exactly 1254's committed count.**

## The anchor (U56, 4,448 days, 2009-01-13..2026-09-18)
| | CAGR | Sharpe | MaxDD | OOS CAGR | OOS Sharpe | OOS MaxDD |
|---|---|---|---|---|---|---|
| **BOOK (candidate)** | 15.80% | 1.1537 | -19.13% | 17.32% | 1.1857 | -19.13% |
| LIVE RULES v2 (baseline) | 8.62% | 1.2011 | -12.05% | 9.46% | 1.2769 | -12.05% |
| SPY | 15.12% | 0.8844 | -33.72% | 15.26% | 0.8738 | -33.72% |

4b PASSES at k = 0 with margins **H1 +0.2494, H2 +0.2952, OOS +0.3118, CAGR +0.0522, DD +0.0110**.
4a fails, as the record already holds. The DD margin is 1.10 pp against idea 1511's paired
bootstrap SE of 2.93 pp — the pass has always been inside its own noise on that leg, and this run
says how little tape it takes to spend it.

## (1) The smallest deletion that flips the verdict is ONE DAY — and it is SPY's day
| unit | conv | flip at k | leg | what was deleted |
|---|---|---|---|---|
| **DAY_ADV (adversarial)** | ZERO | **1** | DD | **2020-03-16** |
| **YEAR (adversarial)** | SPLICE | **1** | DD | **2020** |
| DAY_SPY (SPY's best days) | ZERO | 7 | DD | 2025-04-09, 2020-03-24, 2020-03-13, ... |
| DAY_BOOK (book's best days) | ZERO | **9** | DD | 2025-04-09, 2020-03-24, 2020-03-13, ... |

2020-03-16 is **SPY's worst day of the sample (-10.94%; the book lost 6.66%)**. Zeroing it in both
streams moves **SPY's MaxDD from -33.72% to -26.67%**, which tightens the 60% cap from -20.23% to
**-16.00%**, while **the book's own MaxDD barely moves (-19.13% -> -19.10%)**. Margin +0.0110 ->
**-0.0310**. The same thing happens one scale up: deleting the calendar year 2020 alone takes the
cap to -14.70% against a book at -19.10%. This is 1254's OOS-arena finding — *the drawdown side is
carried by 2020, and not because 2020 was good for the book but because 2020 was bad for SPY* —
now confirmed on the FULL arena and localised to **a single session**.

## (2) The return side is indestructible, and the best-day cut makes it BETTER
Deleting the book's 20 best days (ZERO, BAR=MOVES) walks CAGR 15.80% -> 11.42% and Sharpe
1.1537 -> 0.8994, and **not one return leg flips**: H1 +0.2494 -> **+0.2406**, H2 +0.2952 ->
**+0.3642**, OOS +0.3118 -> **+0.3792**, CAGR margin +0.0522 -> **+0.0505**. H2 and OOS *widen*,
because the same deletion costs SPY more than it costs the book. **The best-day fragility the idea
suspected does not exist on this book's return legs.** Of 979 grid points, **every single 4b
failure on U56 names DD**, and **0 of 979 pass 4a**.
Why the cut cannot discriminate: **13 of the book's 20 best days are also SPY's 20 best days**
(10 of 20 on the worst side); the book's best day and SPY's best day are the same session
(2025-04-09, book +7.55% / SPY +10.50%).

## (3) The fragility is in the BAR, not in the book — published in both directions
| unit | conv | BAR=MOVES | BAR=FROZEN (SPY's k=0 bar held fixed) |
|---|---|---|---|
| DAY_SPY | SPLICE | flips at 3 | **never (> 20)** |
| DAY_BOOK | SPLICE | flips at 3 | flips at 18 (H2) |
| DAY_BOOK | ZERO | flips at 9 | **flips at 3** |
| YEAR | SPLICE | flips at 1 | flips at 2 (H1) |

Under SPLICE a frozen bar makes the book look untouchable; under ZERO a frozen bar makes it look
*more* fragile, because the cap no longer loosens as SPY's own drawdown deepens. Both directions
are the same fact: **what decides this verdict is what the deletion does to SPY.** A 4b DD verdict
is a statement about the benchmark's worst week as much as about the book's.

## (4) The other two panels have no pass to lose
**B136** fails 4b at k = 0 on DD alone (MaxDD **-20.74%** against a cap of **-20.23%**, margin
-0.0051) with every return leg comfortably positive (H1 +0.3242, H2 +0.0717, OOS +0.1441, CAGR
+0.0547). **SMALL665** fails all five legs at k = 0 (CAGR 7.81%, Sharpe 0.5092, MaxDD -36.51%).
Neither is a fragility result and neither is reported as one — `.depth.csv` marks them
`NO_PASS_AT_K0`.

## (5) RULE 8 — the fragility measure is unadjudicable in-sample
Parameters chosen on warm-up..2016-12-31 only; 2017-2026 read once. **The book fails 4b at k = 0
in the IS window on all three panels, on the DD leg** (U56 margin **-0.0072**, B136 -0.0140),
because 2009-2016 contains no deep SPY drawdown (SPY IS MaxDD -22.06% -> cap -13.24%, book
-13.95%) — the defect the committed `2026-09-04_is-window-has-no-crash_C` already named. So every
IS flip-depth is 0, the IS-only chooser is a **pure tie**, and the IS/OOS flip-depth rank
correlation over the 12 (panel, unit) pairs is **undefined (nan)**. The chooser degenerates to the
do-nothing anchor U56: OOS flip depth 1 (YEAR), 1 (DAY_ADV), 6 (DAY_BOOK), 5 (DAY_SPY) — identical
to the anchor's, against a 3-panel mean of 0.33 / 2.00 / 1.67 / 0.33 and a worst panel (B136) of 0.
**OOS triples read once (2017-2026):** BOOK 17.32% / 1.1857 / -19.13%; LIVE v2 9.46% / 1.2769 /
-12.05%; SPY 15.26% / 0.8738 / -33.72%. On the OOS arena alone the pass is again **1-day fragile**.

## What the record should do
1. **Do not promote the 2026-09-04 candidate on the strength of its 4b DD leg.** That leg is one
   session of SPY's tape wide. Its four return legs, by contrast, are the most robust thing this
   run measured and should be quoted separately from the DD leg rather than as one verdict.
2. **Quote a DD-leg verdict with its deletion depth**, the way idea 1694 asked for the rebalance
   phase to be quoted: "4b DD passes, flip depth 1" is a different claim from "4b DD passes".
3. **PROTOCOL rule 4b's DD cap is a relative bar and inherits the benchmark's tail.** In a sample
   whose benchmark has one -10.94% day, the cap is set by that day. This is not a reason to retune
   the cap — it is a reason to report the depth. No RULES change is proposed and none is warranted.
4. Overlap with the record, declared before any number was read: **the calendar-year half is idea
   1254's** (ten OOS years, exhaustive to k = 5) and the name half is 1255's. The year arm here is
   a cross-run gate (G4 reproduces 1254's 9-of-10) plus the adversarial-depth framing 1254 did not
   report; **the DAY axis and the BAR arm are this run's own**.

## Caveats
Survivorship (rule 9): U56 and B136 are current-constituent lists and SMALL665 is a current
sub-$2B screen (54 tickers with max_1d_move >= 1.0 dropped first). Every absolute level is
optimistic, and a current-constituent panel is **kind to the best-day cut** in particular — the
names a momentum screen piles into are disproportionately survivors, so their biggest up-days are
over-represented and the DAY_BOOK robustness reported here is an **upper** bound. The adversarial
searches are greedy, not exhaustive, so every flip depth they report is an **upper** bound on the
true smallest deletion; the exhaustive single-year arm (17 of 18 on U56) is not greedy.
