# Idea 1187 (lane cloud, 2026-09-17) — does a SUB-TAPE RATIO need a STATISTIC CLASS before a CLAUSE can be written?

**ANSWERED = A CLASS IS NOT ENOUGH; THERE IS NO CLAUSE TO WRITE AT ANY CLASS — AND 1158's
STATED MECHANISM IS WRONG.** Scored in the pre-declared order the outcome is **(D) NO CLAUSE
ON RATIO**, but the true reading is stronger than the declared ladder allows: **no repair
serves ANY of the three classes.** Verdict **KILL** as a capital finding (4a 0 of 81 rung
books, 0 of 12 rule-8 picks pass 4b) and **KILL** as a schema finding (no clause reaches a
majority anywhere).

No RULES change, no book promoted, no PROTOCOL edit (rule 6). `RULES.md`, `PROTOCOL.md`,
`engine.py`, `scan.py`, `bot.py` and `baseline.py` untouched.

SELECTION: this lane takes the FIRST eligible open idea; 1187 stood first under `## Open`
and is not EDGAR / Form 4 / 8-K / options / spin-off / live-data.

## The two dials and no more (rule 4)
`STATISTIC CLASS` {LEVEL, SPREAD, RATIO} × `REPAIR` {R_ASIS, R_FROZEN, R_COUNT, R_BOTH}
= **12 cells, every one published** at every (panel, construction, partition) and every
fraction ladder — 1,440 rows in `.grid.csv`. R_BOTH is promoted from 1158's off-grid product
to a dial *value*, because the queue's clause is exactly "which repair goes in the wording"
and a product that is never a candidate cannot be one. That is the only dial-set departure
from 1158 and it is declared.

NOT dials: PANEL {U56, B136, SMALL}; the four dial ladders that are the ratio's groups
(CADENCE, GROSS, H, N = 27 rung books per panel, 81 total, 1148's grid); FRACTION LADDERS
{L2, L3, L4, L6, L8}; PARTITIONS {ALIGNED, OFFSET}; CONSTRUCTIONS {C_POOLED, C_BOOK};
WITHIN terms {R_SPREAD, R_SD, R_MATCHED} (headline R_MATCHED); the leave-one-ladder-out
jackknife; the four rule-8 choosers. Tape PINNED at 2026-09-15.

## The classes, declared before any number
`LEVEL = CAGR + MAXDD` (a location of the equity path, in return units) ·
`SPREAD = VOL + ULCER` (a dispersion magnitude, non-negative by construction) ·
`RATIO = SHARPE + CALMAR` (a quotient of a LEVEL by a SPREAD). The split is 2/2/2 and is a
property of the statistic's **algebra**, not of any number this run produced; it was not
re-drawn after the fact.

## (1) THE QUEUE'S PREMISE IS HALF RIGHT AND ITS MECHANISM IS WRONG

1158 wrote: "on RATIO-valued statistics the between term **passes near zero**". Pooled over
all four repairs, 480 cells per class:

| class | DEGENERATE (\|B\|/scale < 0.05) | SIGNFLIP | BLOWUP (ratio > 10) | median \|ratio\| |
|---|---|---|---|---|
| LEVEL  | 58/480 = **0.121** | **0/480** | 17/480 | 1.5565 |
| SPREAD | 88/480 = **0.183** | **0/480** |  6/480 | 2.7737 |
| RATIO  | 124/480 = **0.258** | **0/480** | 34/480 | 2.0803 |

**The direction holds: RATIO degenerates 2.13× as often as LEVEL and blows up 5.7× as
often.** The mechanism does not. **SIGNFLIP is 0 of 1,440 — at every class, every repair,
every panel, every ladder.** Not one cell's fraction-ladder medians straddle zero. The
between term never *passes through* zero; it goes small because the statistic stops moving
with sub-tape length. A clause written against sign cancellation would be a clause against
something that has never once happened in this record.

Worst single cell remains 1158's own: U56 / SHARPE / R_FROZEN reads **49.1204** (reproduced
bit for bit, gate G6), and R_BOTH at the same cell reads **73.6807** against a resolved
5.8130 — a relative gap of **11.68**.

## (2) THE CLASS THAT MOST OFTEN HAS NO TARGET IS *SPREAD*, NOT RATIO

RESOLVABLE := the resolved target (R_COUNT @ L8, 1158's committed target, reproduced not
re-chosen) is itself not DEGENERATE **and** its leave-one-ladder-out jackknife SE is no
larger than the ratio itself. Over 24 (panel × stat × construction × partition) cells:

| class | RESOLVABLE | rate | median SE/\|r\| | median zrel |
|---|---|---|---|---|
| LEVEL  | 24/24 | **1.000** | 0.6157 | 0.1419 |
| SPREAD | 14/24 | **0.583** | 0.6563 | 0.0729 |
| RATIO  | 20/24 | **0.833** | **0.2057** | 0.1181 |

This inverts the queue's framing directly. RATIO is the **best-resolved** class by SE
(0.2057 against 0.62–0.66) and second-best by publishable-target rate; **SPREAD** is the
class where 10 of 24 cells have no publishable target at all. RATIO's problem is not that
its ratio cannot be measured — it is that the measurement is large and moves a lot.

## (3) NO REPAIR SERVES ANY CLASS — the answer to the queue's question

A repair SERVES a class iff it is **COMPARABLE** (max/min over the 5 fraction ladders
≤ 1.25) **and LANDS** (within 25% of the resolved target) at a **majority** of that class's
resolvable cells. Comparability alone is vacuous — 1158's G8, re-proved here as G9, shows
R_FROZEN is ladder-invariant *by construction* — so the landing leg is not optional.

| class | R_ASIS | R_FROZEN | R_COUNT | R_BOTH |
|---|---|---|---|---|
| LEVEL  (24 cells) | 0/24 = 0.000 | 10/24 = **0.417** | 3/24 = 0.125 | 9/24 = 0.375 |
| SPREAD (14 cells) | 0/14 = 0.000 | 5/14 = 0.357 | 0/14 = 0.000 | 6/14 = **0.429** |
| RATIO  (20 cells) | 0/20 = 0.000 | 9/20 = **0.450** | 0/20 = 0.000 | 5/20 = 0.250 |

**Every cell of the 12 is below the 0.5 majority bar.** The best reading in the whole grid
is 0.450. The declared outcome ladder stops at (D) "no clause on RATIO"; the honest reading
is that (D) is true of LEVEL and SPREAD as well, and a statistic class therefore **does not
rescue the clause** — it only re-sorts which repair comes closest (R_FROZEN on LEVEL and
RATIO, R_BOTH on SPREAD), and even that re-sorting is inside the noise.

A TAUTOLOGY, DECLARED NOT HIDDEN: R_COUNT read at L8 *is* the resolved target, so its
landing column is 24/24, 14/14, 20/20 by construction and is never evidence; R_COUNT earns
or loses a class on comparability alone, where it reads 3/24, 0/14, 0/20. The structure of
the whole table is the trade 1158 found: the ladder-FOLLOWING repairs land but never stay
put (comparable 0 of 58 resolvable cells); the ladder-FROZEN ones stay put by construction
and land at 9–10 of 20–24.

## (4) RULE 8 AND BOTH KEEP PATHS — 81 rung books, 12 picks, all published

Parameters chosen on 2009-2016 only; 2017-2026 read once. 10 bps, next-day execution.

Benchmarks (pinned tape, post-warm-up): **SPY** U56 15.10% / 0.8829 / −33.72% (halves
0.9588/0.8207), OOS 15.21% / 0.8711 / −33.72%. **LIVE RULES v2** U56 8.62% / 1.2008 /
−12.05%, OOS 9.46% / 1.2763; B136 7.98% / 1.0993 / −12.24%; SMALL 4.30% / 0.6637 / −13.89%.

**4a: 0 of 81 rung books and 0 of 12 picks.** 4b full 16 of 81, 4b OOS 17, BOTH 15
(U56 10/27, B136 6/27, **SMALL 0/27 on every path**).

**No new candidate, and the reason is arithmetic, not judgement.** The 16 full-4b passers
are **5 distinct selections**: 10 of the 16 are one book read at a different gross rung.
U56's `CADENCE=W`, `GROSS=0.75`, `H=126` and `N=20` rows are the *same* anchor book
(0.155793 / 1.139742 / −0.191276 to six decimals), and U56 `GROSS` 0.55→0.75 moves Sharpe
only 1.139051→1.139742 — a spread of **6.9e-04 over a 1.36× change in gross** —
independently reproducing idea 1177/1189's de-grossing degeneracy. On B136 the effect is
load-bearing in the wrong direction: the anchor **fails** 4b at gross 0.75 (MaxDD −20.74%
against the 0.60×SPY cap of −20.23%) and **passes** at 0.50–0.70 purely because de-grossing
shrinks the drawdown at ~zero Sharpe cost. Anything that counts those five rows as five
independent 4b passes is counting a scalar.

**The statistic class moves the pick at 3 of 3 panels and never into a passing one.**
CH_ISSHARPE / CH_LEVEL / CH_SPREAD / CH_RATIO pick N=40 / N=10 / H=252 / N=5 on U56, N=8 /
N=5 / N=8 / H=63 on B136, H=252 / H=63 / CADENCE=M / N=15 on SMALL. Seven of the twelve
picks beat SPY's OOS Sharpe; **none passes 4b on any path and none passes 4a.** The class
is a real fork in a live capital decision and it is worth nothing at the end of it.

## Gates — 10 of 10 PASS
G1 fast runner ≡ `engine.backtest` (1.39e-17). G2 committed U56 W/H126/N=20 triple
(4.12e-05). G3 committed SPY OOS triple (1.70e-04). G4 live RULES v2 MaxDD ≡ −12.05%
(4.95e-05). G5 1157/1158's committed full-tape MaxDD levels on all three panels (7.17e-06).
**G6 1158's committed FROZEN readings at four (panel, stat) cells including its U56/SHARPE
blow-up 49.1204 — dev 0.000e+00.** **G7 1158's comparability counts R_ASIS 0/18, R_FROZEN
18/18, R_COUNT 2/18 — exact.** **G8 1158's R_BOTH landing count 4 of 18 — exact.** G9
R_FROZEN ladder-invariance 0.000e+00. G10 the 8,262-row sub-tape table is deterministic.

THE VINTAGE, PUBLISHED NOT ABSORBED: G2/G3 on the UNPINNED file read 1.62e-03 and 2.89e-03.

**G8 caught a real defect in the first cut of this script.** It initially defined the
resolved target as `R_ASIS @ L8` — a defensible choice, and the wrong one, because 1158's
committed target is `R_COUNT @ L8`. The gate failed at 5 of 18 against the committed 4 of
18, and the definition was corrected to 1158's rather than the gate relaxed. Every number
above is from the corrected run.

## Survivorship
The SMALL panel is current constituents of a sub-$2B screen (`data/SMALL_PANEL_README.md`);
`data/small_meta.csv` lists 715 tickers, **52 dropped** for `max_1d_move >= 1.0`, **663
names + SPY served** over 4,198 bars (2010-01-04 .. 2026-09-11).
Its levels are **optimistic** and every 4a/4b count on it is an **UPPER bound** — which
makes SMALL's 0/27 on every path the one count in this run that needs no discount.
