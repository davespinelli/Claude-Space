# Idea 614 — is the IS 4b WINDOW a SUPERSET on every published dial? (cloud, 2026-09-10)

**Verdict: KILL of the queue's generalisation. Containment carries; the LOWER EDGE does not, and
the proposed one-step inward margin does not repair anything.**

## Gates (all PASS, printed before any new number)
| Gate | Result |
|---|---|
| G1 idea 403's premise off its own committed `.windows.csv` | both-non-empty **346** (published 346), containment **215** (215), lower-edge **344** (344) — EXACT |
| G2 `H.run` vs `engine.backtest`, EWall @10bps, u56 | max\|d\| **0.000e+00** |
| G3 (EWall, n) degeneracy — the n dial does not exist on EWall | max sd over the 5 values ≤ **3.1e-17** in all 6 cells; those cells excluded from every rate |
| G4 IS/OOS disjoint and exhaustive | IS 2009-01-13..2016-12-30 (2007d) / OOS 2017-01-03..2026-09-09 (2434d), overlap 0, union = 4441 = full |

## Corpus
5 dials (band, n, gross, vol, K — idea 401's `weights_for`/`DIALS`/`ADOPTED`/`CONTROL` imported
verbatim) × 2 books (EWall, TOP20) × 3 panels (u56, broad136, SMALL439) × 2 rungs (10, 25 bps)
= **564 arm rows** (504 ordered + 60 abstain controls), **60 cells**, 54 non-degenerate.
Two tuned parameters and only two: the **dial** (5) and the **margin** (3) — all 15 grid points
published in `.census.csv`; panels, books, rungs and both KEEP paths are reported axes.

## A1 — the nesting census
| statistic | this run (5 dials) | idea 403 (f dial) |
|---|---|---|
| CONTAINMENT (IS hull ⊇ full hull) | **7/12 = 58.3%** | 215/346 = 62.1% |
| LOWER EDGE (IS_lo ≤ full_lo) | **7/12 = 58.3%** | 344/346 = **99.4%** |
| IS set wider | 10/12 = 83.3% | — |
| SET containment (the strict form the hull overstates) | 6/12 = 50.0% | — |

Exact binomial on the lower edge: **P(X ≤ 7 | n = 12, p = 0.9942) = 4.9e-09**. Idea 403's
near-universal lower-edge result is an **f-dial fact, not a screen fact**. Containment, the weaker
statistic, is the one that generalises — the reverse of prediction P1.

The break is **dial-shaped, and it changes sign**: on the fine exposure dials the IS screen is wider
and lower-edged (gross 3/4, vol 4/6 on both statistics); on the coarse gate dials it collapses to a
single point that is *above* the full window's lower edge (band 0/1 — full admits 0|2|3|5|8, IS admits
**8 alone**; K 0/1 — full admits 100|150|200|250, IS admits **150 alone**). On those dials the IS
screen is over-**restrictive**, the opposite defect.

Denominator honesty: only 12 of 54 cells can carry a nesting relation because the **full 4b window is
empty in 38 of 54 cells** and the IS window in 35 — on these five dials the book mostly fails 4b at
every value. 43 of 54 cells have a non-contiguous pass set, so the hull overstates every window here;
the SET form is reported above and every set is in `.windows.csv`.

## A2 — over-admission and the margin (all 15 grid points in `.census.csv`)
| margin | admitted | false admits | false-admit rate | coverage of full passers | cells emptied |
|---|---|---|---|---|---|
| 0 | 67 | 45 | **0.672** | **0.500** | 35/54 |
| 1 | 32 | 20 | 0.625 | 0.273 | 40/54 |
| 2 | 7 | 3 | 0.429 | 0.091 | 49/54 |

The margin buys **4.7 pp of precision for 22.7 pp of recall** at one step, and 24.3 pp for 40.9 pp at
two. It is a bad trade on every dial including `gross`, the only fine grid and the one prediction P3
said would work (fa 0.731 → 0.786 → 0.500 while coverage 0.700 → 0.300 → 0.200). **P3 refuted.**

**The mechanism is not the missing bar.** `fa_only_OOS_bar = 0` at every dial and every margin: not one
of the 45 false admits fails full-4b on the OOS Sharpe bar alone. Over-admission is entirely noise in
the four bars the IS screen *does* see, measured on 8 years instead of 17. P2's conclusion holds for a
reason P2 got wrong — and it is the more useful reason, because it says no re-specification of the
screen's *bars* can fix this either.

## A3 — rule 8 (dial chosen on 2009-2016 alone, max IS-window Sharpe inside the margin-shrunk IS hull; abstain to the dial's control when empty; 2017-2026 read ONCE)
| margin | picks | abstained | mean OOS Sharpe | mean OOS CAGR | mean OOS MaxDD | beat SPY | beat RULES v2 | 4a | 4b |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 54 | 35 | **0.9324** | 13.38% | −26.66% | 32 | 24 | 0 | 3 |
| 1 | 54 | 40 | 0.9332 | 13.30% | −26.58% | 32 | 24 | 0 | 3 |
| 2 | 54 | 49 | 0.9331 | 13.49% | −26.98% | 32 | 24 | 0 | 3 |

Comparands: SPY OOS Sharpe **0.8799**, RULES v2 (cost-matched) **0.9642**, RULES v1 0.4476.
The margin moves the OOS pick by **+0.0008 Sharpe** — indistinguishable from nothing — because what
it mostly does is convert picks into abstains (35 → 49 of 54). Per panel: u56 1.1177/1.1196/1.1197
(SPY 0.8758, v2 1.2604), broad136 0.9957/0.9961/0.9959 (SPY 0.8820, v2 1.0963), SMALL439
0.6838/0.6838/0.6838 (SPY 0.8820, v2 0.5360) — the small panel's picks are identical at every margin.
Per dial the largest margin effect is n (0.9414 → 0.9505), a dial that exists on one book only.

## KEEP paths
4a **37/564** arms, 4b **44/564**, **no arm passes both**. On the 162 rule-8 picks: 4a **0**, 4b 9.
Every 4b passer is u56 or broad136 (SMALL439: zero); the best is u56/EWall/vol=0.50 @10bps
(full 10.75%/1.135/−16.13%, OOS 11.38%/1.199/−16.13% vs SPY OOS 15.32%/0.876/−33.72%), which fails 4a
on the DD leg and is *not* its cell's rule-8 pick. **No KEEP-candidate, no RULES change.**

## What downstream should change
Any file citing idea 403's "IS window contains the full window, lower edge at or below in 344/346"
must now say **on the sleeve fraction f**. On the record's other five dials the lower-edge rate is
58.3% (p = 4.9e-09 against 403's), and on the two gate dials the IS screen errs the *other* way.
The transferable statement is weaker and dial-conditional: *an IS-screened dial is wider than the
full-sample one (10/12) but not reliably shifted downward, and no inward margin repairs it.*

## Caveats
SURVIVORSHIP (idea 54): all three panels are current-constituent lists; SMALL439 is a screen run today
and back-filled with idea 118's `max_1d_move ≥ 1.0` filter applied first (idea 627: that filter is
itself terminal-dated). The record's **gross dial is a multiplier on a book already built at 0.75
gross**, so dial value g realises 0.75g — carried verbatim from idea 401 so the numbers compare, but
the label is not the exposure. The IS screen sees four bars, not five (idea 401's `margins_win`).
MaxDD is one number off one path (idea 321). Idea 126: t+1, no lag band. Idea 38: u56/broad carry the
calendar-day index. n = 12 is a thin denominator and is thin for a reportable reason, stated above.
