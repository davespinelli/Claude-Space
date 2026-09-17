# Idea 1208 (cloud lane, 2026-09-17) — is the SMALL-PANEL REVERSAL of the DO-NOTHING ADVANTAGE a PANEL FACT or a TURNOVER FACT?

**VERDICT: KILL (capital) / ANSWERED = NEITHER — it is a REACH fact, and it is UNRESOLVED.**

The queue's hypothesis is falsified as a cost story, and the effect it was trying to explain does
not clear its own error bar.

## What was tested

1206 walked 1155's five choosers 472 picks deep and found the headline unresolvable (+0.0017,
clustered SE 0.0526, t 0.03) but committed a large panel split as "the largest real effect in the
run": the do-nothing control C_ANCHOR is top on U56 (1.2165) and B136 (1.1708) and **behind on
SMALL** (0.5298 against 0.6718-0.6783). The queue's hypothesis: the reversal is a cost rebate the
count-matched rules collect because the anchor book turns over more on the small-cap panel — 1206
also found those rules call CADENCE (a `{W, M}` ladder whose far rung is a turnover cut) widest at
0.307-0.314 of picks against M_NONE's 0.0551.

Two dials, both reported at every grid point, nothing else tuned:

* **COST** `{0, 10, 25, 50}` bps — an accounting assumption, reported at all four rungs and never
  chosen on performance.
* **MATCH** `{T_NONE, T_BAND, T_CHARGE}` — `T_NONE` is 1206's run unchanged; `T_BAND` lets the
  chooser reach only rungs whose IS-window turnover (measured at the anchor's gross) is within
  ±25% of the anchor's; `T_CHARGE` makes every book pay the anchor's selection turnover read at
  the book's own gross rung.

Everything else — four ladders, four matching rules, three controls, four anchors, three IS
windows, the calendar-year fold grid, the 3-leg composite, 200d eligibility, `max_vol` 0.60, t+1
execution, 260-row warm-up — is 1206's, inherited whole. 39,648 pick-cells, 472 picks per rule per
grid point. 1206's 21 committed BY PANEL cells reproduce to **4.69e-05** (G4).

## The answer

**The cost channel is dead.** The SMALL reversal is essentially invariant to the price of trading:

| | 0 bps | 10 bps | 25 bps | 50 bps |
|---|---|---|---|---|
| SMALL reversal, `T_NONE` | **+0.1455** | **+0.1463** | +0.1451 | +0.1744 |
| `T_CHARGE` − `T_NONE` (charge channel) | +0.0000 | **−0.0046** | −0.0013 | −0.0277 |
| `T_BAND` − `T_NONE` (reach channel) | **−0.2103** | **−0.2175** | −0.2298 | −0.2591 |

At **zero cost**, where no move can be cheap or dear, the reversal reads 0.99x of its 10 bps size.
Charging every book the anchor's own selection turnover moves it by 3.1% of its level, in the
*wrong* direction for the hypothesis. The reach channel — which books the chooser may reach at all
— is the whole of the effect, and it reads the SAME at 0 bps as at 10 bps, so it carries no cost
content whatsoever.

**The exact arithmetic closes it.** On SMALL the count-matched picks turn over **4.85/yr** against
the anchor's **5.32/yr** — a rebate of 0.47/yr of one-way turnover. At 16.32% realised vol that is
worth **+0.0029 of Sharpe at 10 bps = 1.96% of the +0.1463 reversal**, and only 9.80% of it even at
50 bps. The turnover story cannot pay for the effect by a factor of fifty.

**The mechanism 1206 pointed at is not there either.** The count-matched rules land on CADENCE=M at
**0.2014** of SMALL picks — *less often* than the anchor set's own 0.2500. They call CADENCE widest
at 0.3542 of picks, but the rung they then take is not the turnover cut.

**And the effect itself is unresolved.** Paired on (anchor, window, fold) with SE clustered by the
14 non-overlapping calendar folds, the reference cell reads **+0.1463, SE 0.0985, t +1.48** —
**0 of 12 grid points clear 2 SE on SMALL, 0 of 12 on U56, 0 of 12 on B136.** SE falls as
1/sqrt(folds), so resolving it needs **25 folds against the 14 this tape supplies** — about eleven
more years of small-cap history. 1206 called it the largest *real* effect in the run; it is the
largest *unresolved* one.

**Rule 8 (required).** The reversal computed separately on the IS folds (2013-2016) and the OOS
folds (2017-2026), each grid point read once: `T_NONE`/10 bps gives SMALL **+0.3103 IS / +0.1135
OOS**, U56 −0.0303 / −0.0505, B136 +0.0054 / −0.0618. The panel split keeps its sign out of sample
on SMALL and on U56 and loses two thirds of its magnitude; `T_CHARGE` tracks `T_NONE` in both
windows (+0.3205 / +0.1059) while `T_BAND` flips sign out of sample (+0.0436 / −0.0942). The
literal chooser walk (dials chosen IS, OOS read once) puts C_ANCHOR at OOS mean fold Sharpe 1.0562
/ 13.51% / −12.84% against the matching rules' 0.7376-0.8325 — but at their own cells, which are
different books; at the matched cell (3y, A_REC, 10 bps) the seven rules collapse to
0.8693-1.0131 under `T_BAND` and 0.9618-1.0294 under `T_NONE`.

**`T_BAND` is not a clean instrument and is reported as such.** Its SMALL reading is not monotone
in its own band: −0.0451 / −0.0712 / +0.0191 at bands 0.10 / 0.25 / 0.50. The band was
pre-declared at 0.25 and the sensitivity is reported, never adjudicated on.

## A defect the gates caught, for the record

Both matches were first written on the natural reading of `W = g * selection_frame`: that turnover
is **linear in gross**, `turn(g) = g*turn(1)`. **G2 rejected it at 0.0173 of one-way turnover on
the record's own anchor before any result was read.** Drifted weights are renormalised by a
portfolio value carrying a `1-g` cash sleeve, so the trade needed to restore a position depends on
the gross rung. Every construction in the final script uses **built** turnover paths only. Any
claim in the record that re-prices a gross ladder by scaling turnover is wrong by up to this much.

## Both KEEP paths (PROTOCOL rule 4)

912 book-readings (228 books × 4 cost rungs) and 3,024 stitched chooser curves.

| cost | 4a | 4b full | 4b OOS | both |
|---|---|---|---|---|
| 0 bps | 0/228 | 53/228 | 59/228 | 51/228 |
| 10 bps | 1/228 | 45/228 | 50/228 | **43/228** |
| 25 bps | 1/228 | 37/228 | 42/228 | 36/228 |
| 50 bps | 1/228 | 25/228 | 33/228 | 25/228 |

Stitched curves: **4a is 0 of 252 at every one of the 12 grid points**; 4b full+OOS 276 of 3,024,
of which **U56 240, B136 36, SMALL 0**. The 43 book-level full+OOS passers at 10 bps are the SAME
43 1206 recorded and declined to promote — this run re-reads 1206's book grid and adds no book.
**NOT PROMOTED, NO MEMO, NO RULES CHANGE.** SPY over the stitched span: 14.88-15.01% / 0.9116-0.9180
/ −33.72% (OOS 15.15-15.33% / 0.8686-0.8769). Live RULES v2 @10 bps: U56 1.2986 (OOS 1.2717), B136
1.1725 (OOS 1.1061), SMALL 0.8141 (OOS 0.6518).

## Survivorship (rule 9)

B136 and SMALL are CURRENT constituents of their screens. SMALL is the sub-$2B panel with every
ticker whose max 1-day move reaches 100% dropped before use (663 names). The reversal under test is
itself a statement about names that survived to the screen date, and the small-cap tape starts in
2010; no conclusion here should be read as a live small-cap edge.

## Gates: 11 of 11 pass

G1 fast runner net@10bps ≡ `engine.backtest` (2.78e-17) · G2 `T_CHARGE` is the identity on the
anchor and its whole GROSS ladder (0, after the linearity shortcut failed at 0.0173) · G3 live
RULES v2 U56 MaxDD ≡ committed −12.05% · G4 1206's 21 BY PANEL cells reproduce (4.69e-05) · G5
`T_NONE` ≡ `T_CHARGE` at 0 bps (exactly 0) · G6 folds tile the span · G7 C_ANCHOR move rate exactly
0 · G8 paired design balanced · G9 `net(c) == gross - turn*c/1e4` re-derived at 25 bps (0) · G10
`T_BAND` always keeps the anchor · G11 2-rung ladder identity.

Runtime 57s, offline, deterministic.
