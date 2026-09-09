# Idea 587 — is 4b a SINGLE GROSS DIAL wearing five bars? (lane C, 2026-09-09)

**VERDICT: KILL of the headline — 4b does NOT collapse to one gross dial. But it collapses
to TWO bars, not five: on 1,020 grid points the three Sharpe-vs-SPY bars were the sole
failing bar ZERO times, and dropping all three changes 0 of 1,020 verdicts.**

Script `2026-09-09_is-4b-a-SINGLE-GROSS-DIAL-wearing-five-bars_C.py`; console
`.console.txt`; every grid point in `.grid.csv`. No RULES change, no PROTOCOL edit, no new
KEEP claimed. `RULES.md`, `scan.py`, `bot.py`, `baseline.py`, `PROTOCOL.md` untouched.

## Setup
1,020 books = 3 panels (U56 / B136 / SMALL484) × 3 families (BAND 4 bands, MOM 3 n,
VOLQ 3 q) × a 17-point gross ladder 0.20…1.00 × 2 cadences (W, M). Costs 10 bps,
weights at close *t* applied *t+1*, no shorting, gross ≤ 1.00 (PROTOCOL 2). Two tuned
params only: the family dial and gross. PROTOCOL 4b written out as five bars, each
against that panel's own SPY on the same window: **B1** Sharpe > SPY H1, **B2** Sharpe >
SPY H2, **B3** Sharpe > SPY OOS, **B4** |MaxDD| ≤ 0.60·|SPY MaxDD|, **B5** CAGR ≥
0.70·SPY CAGR. **SURVIVORSHIP (PROTOCOL 9): B136 and SMALL484 are current constituents.**

## Gates
- **G1 PASS** — `fast_backtest` vs `engine.backtest` on 4 real books, worst **1.39e-17**
  (bar 1e-12).
- **G2 FAILS ITS OWN LITERAL BAR** — `max|w(0.35)·0.90 − w(0.90)·0.35| = 3.47e-18` against
  a pre-registered bar of *exactly* 0.0. Reported as it fell: the bar was mis-set, since
  3.5e-18 is IEEE-754 rounding in a scalar multiply, ~1e-16 of a typical weight. The
  substantive claim holds at any tolerance ≥ 1e-15, and the ladder itself is built by
  multiplying one base weight matrix by *g*, so the dial is exact by construction inside
  PART 1.
- **G3 PASS** — the committed U56 / RULES v1 anchor rebuilds at **6.4194% / 0.66110 /
  −13.8278%**, max |d| **1.19e-06**.

## The five pre-registered hypotheses
| | hypothesis | result | value |
|---|---|---|---|
| **H_ONE** | gross alone explains ≥ 0.80 of 4b pass variance | **FAIL** | R² = **0.0983** |
| **H_INTERVAL** | pass set contiguous in *g* on ≥ 90% of ladders | **PASS** | **100.0%** (60/60) |
| **H_CAGR** | B5 binding on ≥ 75% of failing points | **PASS** | **91.8%** |
| **H_DROP** | B5 alone changes < 10% of verdicts | **PASS** | **7.8%** |
| **H_FLAT** | no Sharpe bar flips along any gross ladder | **FAIL** | **1** flip, at margin 5.2e-05 |

## What the run found

**1. The single-dial reading fails, and the reason is that the dial cannot reach most
books.** Pooled over 1,020 points, R²(pass ~ gross, 17 levels) = **0.0983** against
R²(pass ~ book identity, 60 levels) = **0.1539**; the saturated book×gross model is 1.0 as
it must be. **43 of 60 books never pass 4b at any gross.** Restricted to the 289 points on
the 17 books that pass somewhere, the ordering reverses hard — R²(gross) **0.3881** vs
R²(book) **0.0537** — so *conditional on a book that the dial can reach*, gross is ~7×
the story, but still explains under 40%. **7 of the 17 gross rungs are non-unanimous**:
at the same *g*, some books pass and some fail. Gross is the dominant dial, not the only
one. (The `r2_shape_within` column in `.within_gross.csv` is 1.0 on every non-unanimous
rung **by construction** — one observation per (book, gross) cell — and carries no
information; the informative line is the count of non-unanimous rungs.)

**2. Along one book's own ladder, the single-dial reading is exactly right, and the
CAGR floor is the whole of it.** The 4b pass set is a contiguous interval in *g* on
**60/60** ladders. On all **17/17** ladders that pass anywhere, the lower edge is set by
**B5, the CAGR floor, without exception**. The upper edge is open at g = 1.00 on 12 of
them and set by **B4, the DD cap, on 5**. No Sharpe bar sets an edge anywhere. Median
admissible band **[0.90, 1.00]**, min lower edge 0.70, median width 0.05 — narrow, and
pressed against the no-leverage ceiling. Passers carry realised mean gross **0.619–1.000
(median 0.709)** against a failer median of 0.460.

**3. The three Sharpe bars are never marginal — this is the run's real finding.** Over
979 failing points: B5 fails on 899 (91.8%) and is the *sole* failing bar 368 times
(37.6%); B4 fails on 267 (27.3%), sole 50 times (5.1%); **B1 fails on 408, B2 on 544,
B3 on 538 — and each is the sole failing bar exactly 0 times.** Consequently **DROP B1,
DROP B2 and DROP B3 each agree with full 4b on 100.00% of the 1,020 points**; DROP B4
agrees on 95.10%, DROP B5 on 63.92%. The Sharpe bars are not slack — they fail often —
but on this grid they never once fail *alone*, so they never set a verdict. **B5 alone
reproduces full 4b on 92.16% of points.** Per-bar slope in gross: B1 +0.0061, B2 +0.0035,
B3 +0.0035 per unit gross (corr ≤ +0.006), against B4 **−0.2563** (corr −0.516) and B5
**+0.1049** (corr **+0.831**) — idea 321's "Sharpe is flat in gross" reproduces on 3
families and 3 panels, not just its one ladder. The single H_FLAT violation
(B136|VOLQ|0.25|M) is a tie, not a dial effect: B3's margin runs +0.0027 → −0.0050 across
the whole dial and crosses zero at g = 0.50; that book passes 4b at 0 of 17 rungs.

**4. Rule 8 (PROTOCOL 8).** (family dial, gross) chosen on IS ≤ 2016-12-31 by IS Sharpe,
2017– read once; cadence fixed at W, not tuned. Two conventions — unconstrained, and
subject to the IS-side 4b gate — over 9 (panel, family) cells; **the IS 4b gate moves the
pick on 5 of 9 cells**; on SMALL484 nothing clears the IS gate in any family, so only 6 of
the 9 cells yield an IS-gated pick at all. **2 of those pass 4b out of sample, 0 pass 4a.** Both are the BAND family at band 0.10, g = 1.00:

| pick | full CAGR / Sharpe / MaxDD | H1 / H2 | OOS CAGR / Sharpe / MaxDD | 4a | 4b |
|---|---|---|---|---|---|
| U56 BAND 0.10 g1.00 W | 11.84% / **1.187** / −16.10% | 1.258 / 1.126 | 12.37% / **1.216** / −16.10% | ✗ | ✓ |
| B136 BAND 0.10 g1.00 W | 11.67% / 1.128 / −19.14% | 1.277 / 0.983 | 11.27% / 1.110 / −19.14% | ✗ | ✓ |
| RULES v2 (live), U56 | 8.64% / 1.204 / −12.05% | — | 9.51% / **1.282** / −12.05% | — | — |
| SPY, U56 | 15.19% / 0.887 / −33.72% | — | 15.38% / 0.879 / −33.72% | — | — |

**The U56 pick reproduces idea 321's committed rule-8 pick to every published digit**
(11.84% / 1.187 / −16.10%, OOS 12.37% / 1.216) from an independently written grid — an
unplanned cross-run reproduction. **It is not a new book and no new KEEP is claimed
here**; both picks fail 4a on drawdown against RULES v2 (−16.10% and −19.14% vs −12.05%),
and both OOS Sharpes sit *below* the live book's OOS 1.282. The 4b pass is bought with
gross: both sit at the g = 1.00 ceiling, which is precisely the reading this run is
testing.

## Cross-run consistency with idea 544 (cloud, same day)
Idea 544 priced 4b passage on the **live DEGROSS family alone** at fine resolution and found
the DD bar never binds there (0 of 1,728 points), so passage is a one-sided bound `[g*, 1.00]`.
This run reproduces that where the two overlap and shows its boundary: of my 17 live ladders,
**12 run open to g = 1.00** (all BAND/DEGROSS books at weekly cadence, exactly 544's regime),
and the **5 that the DD cap does close are 3 MOM books and 2 monthly-cadence BAND books**
(B136 BAND 0.03 M, U56 BAND 0.10 M, U56/B136 MOM n20). So "the DD cap never binds" is a
statement about the live de-grossing family, not about 4b; concentrate the book or slow the
cadence and B4 starts closing the band from above. Neither run claims a new KEEP.

## What this changes
Nothing in the live book. One **proposal**, not an edit (PROTOCOL rule 6 — Sunday review):
PROTOCOL 4b currently reads as five bars, and on 1,020 grid points across 3 families and
3 panels **three of them never once set a verdict**. Either state 4b as the two bars it
actually is (CAGR floor, DD cap) and quote the Sharpe legs as descriptive, or replace the
Sharpe-vs-SPY bars with a leg that is not near-invariant to the one dial that moves the
other two. Until then, "passes all five bars of 4b" should be read as "passes the CAGR
floor at a gross the DD cap still allows" — and, per PART 3, that is a band of median
width 0.05 pressed against the no-leverage ceiling.
