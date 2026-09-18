# Idea 1139 (lane B, 2026-09-18) — should a committed FLOOR-KEYED CLAIM be required to quote its RUNG LIST rather than its RUNG COUNT?

**ANSWER: YES — but the clause binds only where the bar is not SATURATED, and on this record that
is the drawdown leg and the 4b verdict leg, not the Sharpe legs. CAPITAL: KILL.**

## The clause, priced (ARM A — 2 dials, all 4 cells published)

Own detector, own denominator (idea 894 stamp: tree `e929781b226c`). A *floor-keyed sentence*
asserts something about the worst / minimum / every member of a ladder.

| CLAIM_SET | REQUIRED | claims | checkable today | COUNT only | NEITHER | clause would newly require |
|---|---|---|---|---|---|---|
| CORE | R_LIST | 1,810 | 91 (5.0%) | 274 (15.1%) | 1,445 (79.8%) | 1,719 (95.0%) |
| CORE | R_LIST_PLUS | 1,810 | 2 (0.1%) | 274 (15.1%) | 1,445 (79.8%) | 1,808 (99.9%) |
| WIDE | R_LIST | 5,006 | 160 (3.2%) | 557 (11.1%) | 4,289 (85.7%) | 4,846 (96.8%) |
| WIDE | R_LIST_PLUS | 5,006 | 4 (0.1%) | 557 (11.1%) | 4,289 (85.7%) | 5,002 (99.9%) |

CORE = LEADERBOARD.md + CHANGELOG.md; WIDE = those plus every committed `research/*.md` and
`research/backtests/*.md` (1,216 files). `R_LIST` = the rung values; `R_LIST_PLUS` = rung list +
ladder axis + the statistic the floor is over.

**The wide denominator is an UPPER bound and is published as one.** The bare word *floor* also
names bars that are not ladder claims at all (4b's "CAGR floor", 877's "seed floor"). On the
STRICT denominator — the sentence names a ladder/rung at all — WIDE falls to **1,241 claims, 7.7%
checkable today, 18.9% count-only**; CORE to **564 / 10.8% / 20.7%**. Either way `H_UNCHECKABLE`
FIRES: a large majority of the record's floor-keyed prose states neither a list nor a count.

## Is the COUNT ever enough? (ARM B — real books, three panels)

INF_FLOOR over the record's committed 9-rung H ladder {5,10,21,42,63,90,126,189,252}, each of six
floor statistics carrying PROTOCOL 4b's *own* bar for that leg, every C(9,k) subset scored.

- **The Sharpe legs are SATURATED.** On U56, S_IS / S_OOS / S_FULL / S_CAGR fire at **100.0% of
  subsets at every k = 1..9** (floors 0.9976–1.2466 against bars 0.8747–0.8989). Nothing can fail,
  so the rung count trivially determines the verdict and the clause buys nothing there.
- **The drawdown leg is where the rung list decides.** U56 `S_DD` fires at **44.4% / 16.7% / 4.8%
  / 0.8% / 0.0%** at k = 1..5 (bar -0.2023, floor range [-0.2553, -0.1846]); `S_4B` is identical;
  B135 `S_DD` 11.1% at k=1 then 0. SMALL663 is silent on all six legs at every k.
- Across all cells the count fails to determine the verdict at **21 of 162 (panel, statistic, k)**
  — **13.0%**, and every one of the 21 is a DD or 4b-verdict cell. `H_COUNT_INSUFF` FIRES.

`H_NONMONOTONE` **does NOT fire here.** Adding 1131's H=210 moves the floor (B135 `S_DD` -0.2869 →
-0.2872) but flips the verdict at **0 of 18 (panel, statistic) cells**. Reported as a
NON-REPRODUCTION on a different construction, not a refutation of 1131.

## Capital (ARM C — PROTOCOL rule 8, OOS 2017-2026 read ONCE). KILL.

The trigger run as a real gate: floor of an IS-only statistic over rung subset R clears its 4b bar
→ allocate to the IS-Sharpe-argmax H in R; else DO NOTHING (hold live RULES v2). 511 subsets × 2
gate keys × 3 panels = **3,066 decisions**, every pick made on warm-up..2016-12-31.

| panel | do-nothing OOS S | gate key | GO | gate−do-nothing OOS Sharpe (mean [min,max]) | positive | 4a | 4b |
|---|---|---|---|---|---|---|---|
| U56 | 1.2781 | G_SHARPE | 511/511 | -0.1924 [-0.2250, -0.0812] | 0/511 | 0 | 29 |
| U56 | 1.2781 | G_DD | 127/511 | -0.0502 [-0.2250, +0.0000] | 0/511 | 0 | 13 |
| B135 | 1.1061 | G_SHARPE | 511/511 | -0.1373 [-0.2697, -0.0583] | 0/511 | 0 | 0 |
| B135 | 1.1061 | G_DD | 1/511 | -0.0004 [-0.2181, +0.0000] | 0/511 | 0 | 0 |
| SMALL663 | 0.6518 | G_SHARPE | 3/511 | -0.0004 [-0.2591, +0.0160] | 2/511 | 0 | 0 |
| SMALL663 | 0.6518 | G_DD | 0/511 | +0.0000 | 0/511 | 0 | 0 |

**The gate never pays.** 4a passes 0 of 3,066. It beats doing nothing at 2 of 3,066 decisions,
both on SMALL663, by at most +0.0160 of Sharpe — and at 0 of 1,022 on the two large-cap panels.
The 42 nominal 4b passes are not new books: all 4 of 30 grid rungs that clear 4b outright are U56
H = 5 / 10 / 21 / 126, every one an already-published rung of the incumbent's own ladder, and the
best reachable cell (U56 H=126, OOS 17.28% / 1.1832 / -19.13%) IS the standing 2026-09-04 book.
Under G_SHARPE the full-ladder pick is H=189 on U56 — OOS 1.0530, failing 4b on DD.

## Schema line offered to the record (not adopted here; rule 6 reserves that for a Sunday review)

*A committed floor-keyed claim should state its rung LIST and the BAR its floor is measured
against. The count is sufficient only when the bar is SATURATED — when no rung of the ladder can
fail — and a claim that does not publish its bar cannot be read for saturation. On this record
13.0% of (panel, statistic, k) cells are decided by which rungs were chosen rather than how many,
and every one of them is on the drawdown or verdict leg.*

## Gates — 17 of 17 passing

G1 fast runner == `engine.backtest` on the anchor **2.08e-17**. G2 anchor cell deterministic on
rebuild + rerun, bit for bit, on all three panels (scope: one cell per panel, stated not
overclaimed). G3 IS/OOS disjoint, OOS starts 2017-01-03. G4 the IS chooser reads no OOS row,
**0.00e+00** on all three panels. G5 BASE ⊂ EXT with the anchor on both. G6 every census share in
[0,1], denominators > 0. G7 the floor is monotone in the rung set, all 511 subsets × 6 statistics
× 3 panels. G8 census denominator stamped with (file count, tree sha).

## Survivorship (PROTOCOL rule 9)

U56 and B135 are CURRENT-constituent lists; SMALL663 is a current sub-$2B screen with the house
`max_1d_move >= 1.0` filter applied first. Every absolute level in ARM B/C is optimistic and every
4b pass is an UPPER bound. The ARM B headline is a contrast between rung SUBSETS of one ladder on
one tape, so a level bias common to the panel moves every subset together and the rung-choice
finding is first-order immune; the 4b counts are not. ARM A re-reads committed prose and changes
no number in it.
