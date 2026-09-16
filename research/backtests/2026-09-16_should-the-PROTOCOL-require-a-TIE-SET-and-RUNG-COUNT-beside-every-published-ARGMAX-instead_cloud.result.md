# Idea 1133 (cloud lane, idea 2 of 2, 2026-09-16) — should the PROTOCOL require a TIE SET and RUNG COUNT beside every published ARGMAX instead?

**ANSWERED = YES, BUT ONLY IN TWO OF ITS THREE FORMS — and the middle form inherits the exact
rung-dependence that killed 1117's ban.** The clause is drafted below and priced against the
record's 32 committed argmaxes at both rung sets. No RULES change, no book promoted, **no
PROTOCOL edit (rule 6): the clause is STATED for the Sunday review and not enacted.** RULES.md,
PROTOCOL.md, engine.py, scan.py, bot.py and baseline.py untouched.

## The clause, drafted (stated, NOT enacted)

> **PROPOSED PROTOCOL 4c — EVERY PUBLISHED ARGMAX CARRIES ITS OWN RESOLUTION.**
> A result that names the best rung of a ladder shall quote, beside it and in the same sentence:
> (i) the **GAP** from the peak to the runner-up, in the statistic's own units; (ii) the
> ladder's **RESOLUTION FLOOR** at the declared confidence q; (iii) the ladder's **RUNG COUNT**
> and its end rungs; and (iv) the **TIE SET** at that q — every rung the bootstrap cannot
> separate from the peak. Where the tie set holds more than one rung, the result is published
> AS THE TIE SET and not as a rung. Where the tie set is the whole ladder, no argmax is
> published at all.

Three bars were priced, as dial 2: **B_QUOTE** (quote all four, delete nothing), **B_TIESET**
(as B_QUOTE, plus republish a multi-rung tie set as the tie set, and delete only a claim whose
tie set spans the whole ladder), **B_DECIDE** (only a decided argmax may be published as a rung).

## What was run
Two dials and no more: `CLAIM SET` {CS_ALL32, CS_DECIDED, CS_HCAD} x `BAR` {B_QUOTE, B_TIESET,
B_DECIDE} = 9 points, **all published, each at BOTH rung sets**. RUNG SET {CORE, EXT} is **not**
a dial and nothing is selected on it — 1117 died on rung dependence, so both levels are reported
everywhere and the movement between them IS the result. PANEL, LADDER and STATISTIC are not
dials (all 2 x 4 x 4 = 32 cells reported everywhere). q = 0.90 throughout. 74 books; CORE and
EXT rung sets are 1110/1116's and 1118's verbatim (N 9->9, H 4->9, GROSS 10->10, CADENCE 4->9).

**GATES 11 of 11 PASS**, printed before any result number: G1 fast runner == `engine.backtest`
1.39e-17; G2 committed U56 W/H126/N=20 triple 3.18e-07; G3 SPY OOS 1.70e-04; G4/G4b committed
U56 n=12 / B136 n=15 triples 4.98e-05 / 2.13e-05; G5 live RULES v2 MaxDD 4.95e-05; G6
determinism 0.00e+00; **G7 `cadence_mask` == `engine.rebalance_mask` on D/W/M/Q, 0 differing
bars**; G7b every extended cadence rung is a k-th-bar subset of an engine schedule, 0; **G8 EXT
NESTS CORE on every ladder, 0 rungs lost**; G9 the ladders are live.

## The clause priced — restates vs deletes, all 9 points, both rung sets

| claim set | bar | set | n | as-is | +numbers | as tie set | **DELETED** | restate share |
|---|---|---|---|---|---|---|---|---|
| CS_ALL32 | B_QUOTE | CORE | 32 | 6 | 26 | 0 | **0** | 1.0000 |
| CS_ALL32 | B_QUOTE | EXT | 32 | 6 | 26 | 0 | **0** | 1.0000 |
| CS_ALL32 | B_TIESET | CORE | 32 | 6 | 0 | 8 | **18** | 0.4375 |
| CS_ALL32 | B_TIESET | EXT | 32 | 6 | 0 | 17 | **9** | 0.7188 |
| CS_ALL32 | B_DECIDE | CORE | 32 | 6 | 0 | 0 | **26** | 0.1875 |
| CS_ALL32 | B_DECIDE | EXT | 32 | 6 | 0 | 0 | **26** | 0.1875 |
| CS_DECIDED | any | both | 6 | 6 | 0 | 0 | **0** | 1.0000 |
| CS_HCAD | B_QUOTE | both | 16 | 0 | 16 | 0 | **0** | 1.0000 |
| CS_HCAD | B_TIESET | CORE | 16 | 0 | 0 | 1 | **15** | 0.0625 |
| CS_HCAD | B_TIESET | EXT | 16 | 0 | 0 | 10 | **6** | 0.6250 |
| CS_HCAD | B_DECIDE | both | 16 | 0 | 0 | 0 | **16** | 0.0000 |

**The literal answer to the idea's question:** at **B_QUOTE the clause restates 32 of 32 and
deletes 0**, at both rung sets; at **B_DECIDE it restates 6 and deletes 26**, at both rung sets.
It is not a gentler instrument than 1117's ban — in its strict form it is **strictly harsher**
(26 deleted against the ban's 12 at CORE, and 26 against the ban's **0** at EXT).

## Hypotheses: 3 of 5 supported
- **(a) H_RESTATES REFUTED (12 of 18 rows).** The clause restates more than it deletes at
  B_QUOTE everywhere and at B_TIESET/EXT, but **not** at B_DECIDE (26 > 6 at both sets), nor at
  B_TIESET/CORE (18 > 14), nor on CS_HCAD at B_TIESET/CORE (15 > 1).
- **(b) H_STABLE REFUTED, and this is the finding that matters.** The DELETE count swing
  CORE -> EXT is **0 at B_QUOTE and 0 at B_DECIDE on every claim set — perfectly rung-stable —
  but 9 of 32 at B_TIESET** (CS_ALL32 18 -> 9; CS_HCAD 15 -> 6), against the 12-of-32 swing
  (12 -> 0) that killed 1117's ban. **The direction is the same one that killed the ban: adding
  rungs makes the clause delete FEWER claims.** 1117 proposed this clause on the ground that
  "nothing in it depends on a whole-ladder flag" — but B_TIESET's delete trigger, *tie set spans
  the whole ladder*, **is** a whole-ladder flag, and it moves almost as much as the ban's did.
- **(c) H_NO_ZERO SUPPORTED.** Unlike the ban, the clause is never vacuous: CS_ALL32 deletes
  18 / 9 at B_TIESET and 26 / 26 at B_DECIDE, at CORE / EXT.
- **(d) H_WIDENS SUPPORTED, and it is the mechanism for (b).** Median tie-set size CORE -> EXT:
  N 8.0 -> 8.0, **H 4.0 -> 8.0**, GROSS 1.0 -> 1.0, **CADENCE 4.0 -> 7.0**. Adding rungs widens
  tie sets in absolute rungs but shrinks them as a *share* of the ladder, so the "whole ladder"
  trigger fires less often — exactly 1118's mechanism, seen from the clause's side.
- **(e) H_DECIDED_SURVIVE SUPPORTED, 6 of 6.** This run independently reproduces 1102/1109's
  committed census: **the record DECIDES 6 of 32 at CORE, all 6 on the GROSS dial** (U56 CAGR
  and DD; B136 all four), and all 6 stay decided at EXT — near-trivially, since GROSS's rung
  count does not change. Under every bar and every rung set, all 6 survive as rung claims.

## Rule 8 and both KEEP paths — nothing proposed, and an independent reproduction of 1117's arm
Rung chosen per ladder on IS 2009-2016 alone, three choosers, OOS 2017-2026 read once.
**48 IS picks: 4b full 6, 4b OOS 6, 4a 0, median OOS Sharpe 1.0244, median regret +0.0515.**
Whole grid, 74 books: **4b full 17, 4b OOS 18, 4a 0.** Those figures reproduce 1117's committed
walk-forward arm (48 picks, 4b full 6, 4b OOS 6, 4a 0, median OOS Sharpe 1.0244; 74 rungs, 4b
full 17, 4b OOS 18, 4a 0) from an independently written script — a cross-run confirmation, not a
new result. **Of the 74 books, exactly one outside 1110's CORE clears 4b: U56 CADENCE 2Q**
(full 13.26% / 1.0019 / -17.90%, OOS 15.47% / 1.0660 / -17.90%) — **below the incumbent
W/H126/N=20 book's own OOS Sharpe of 1.1643, so it buys nothing.** Benchmarks: U56 SPY 15.10% /
0.8829 / -33.72% full and 15.21% / 0.8711 / -33.72% OOS; B136 SPY 15.16% / 0.8861 / -33.72% and
15.33% / 0.8767 / -33.72%; live RULES v2 U56 8.62% / 1.2007 / -12.05% and 9.45% / 1.2762 /
-12.05%, B136 7.98% / 1.0993 / -12.24% and 7.88% / 1.1059 / -12.24%. **NOTHING PROPOSED AS
CAPITAL.**

## The recommendation to the Sunday review (rule 6 — stated, not enacted)
**Adopt the clause at B_QUOTE, and at B_DECIDE for the WORD "best" only. Do not adopt
B_TIESET.** B_QUOTE and B_DECIDE are the two forms whose trigger reads only the peak's own tie
set and never a whole-ladder property, and both are **exactly rung-stable (swing 0 of 32)** on
every claim set. B_TIESET's extra clause — "where the tie set is the whole ladder, publish no
argmax" — is the one line that reintroduces a whole-ladder trigger, and it costs 9 of 32 claims
of rung-dependence to keep. **The general statement, strengthened from 1117's:** a clause is
rung-stable iff every quantity in its TRIGGER is a property of the peak and its own pair, not of
the ladder. Quoting a whole-ladder quantity (the floor, the rung count) is free; **triggering**
on one is not.

## Survivorship (PROTOCOL rule 9)
U56 and B136 are CURRENT-CONSTITUENT panels, so every 4b figure above is an upper bound. Gaps,
floors and tie sets are within-panel contrasts between two books over the same inflated tape and
the bias very largely cancels out of them — which is why this run's headline is a
clause-pricing claim and not a capital claim.
