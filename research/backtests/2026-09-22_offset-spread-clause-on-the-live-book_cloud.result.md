# Idea 2111 — does the OFFSET-SPREAD CLAUSE kill the LIVE RULES v2 book itself?

**Lane cloud, run 4, 2026-09-22.** Script `2026-09-22_offset-spread-clause-on-the-live-book_cloud.py`.
Artifacts: `.grid.csv` (189 rows), `.clause.csv` (144 leg-cells), `.verdicts.csv` (36), `.walkforward.csv` (6), `.gates.csv`, `.console.txt`.

**ANSWER: NO — and it does not rescue it either. KILL of the hypothesis; no new book.**

Idea 914 earned a rule-4b clause (*a margin inside the book's own rebalance-offset spread is
not a pass*) on a candidate; 2119 generalised it over a 25-cell ladder; 2115 showed the spread
is a PATH artefact, not a cost artefact. None of them turned it on the book that is actually
live. This run does, on **both sides** of the clause, because it is symmetric and the record
has only ever read the PASS side: *an unresolved FAIL is not a fail either.*

## The book, the dials, the gates
LIVE RULES v2 unmodified (`baseline.rules_v2_weights`, band 0.03, gross 0.75, weekly, t+1,
long only). Exactly two tuned dials as the idea line specifies — **OFFSET** d ∈ {0,1,2,3,4}
and **COST** c ∈ {0,10,25,50} bps — 20 cells per panel, every grid point published. The
reported book is **always d = 0**, the published convention; d > 0 exists only to build the
spread. Panels U56 / B136 / SMALL, windows FULL / IS (..2016-12-31) / OOS (2017-01-01..).
**5 of 6 gates PASS**: G1 local `run()+net()` ≡ `engine.backtest(W,10bps)` **0.000e+00**;
G2 `offset_mask(·,0)` ≡ `rebalance_mask(·,'W')` **0 differing rows**; G3 the weights priced
≡ `baseline.rules_v2_weights` **max|d| = 0**; G4a every offset trades **52.3/yr**;
G6 SMALL drops **54 of 719** names with `max_1d_move ≥ 1.0`. **G4b FAILS structurally**
(d=3 clips 2 weeks, d=4 clips 175) — published, not patched, and every leg is re-read on the
clip-free offsets {0,1,2} as a second column rather than widening the bar quietly.

## (A) The live book at the published convention (d=0, 10 bps)

| panel | win | CAGR | Sharpe | MaxDD | H1 / H2 | SPY | 4b |
|---|---|---|---|---|---|---|---|
| U56 | FULL | 8.62% | 1.2010 | −12.05% | 1.228 / 1.181 | 15.14% / 0.8851 / −33.72% | FAIL on CAGR |
| U56 | IS | 7.61% | 1.1043 | −7.89% | 0.917 / 1.348 | 14.96% / 0.8986 / −22.06% | FAIL on CAGR |
| U56 | OOS | 9.46% | 1.2767 | −12.05% | 1.432 / 1.106 | 15.29% / 0.8751 / −33.72% | FAIL on CAGR |
| B136 | FULL | 7.96% | 1.0972 | −12.24% | 1.230 / 0.967 | 15.12% / 0.8844 / −33.72% | FAIL on CAGR |
| B136 | IS | 8.10% | 1.0922 | −7.90% | 0.931 / 1.297 | 14.96% / 0.8987 / −22.06% | FAIL on CAGR |
| B136 | OOS | 7.85% | 1.1017 | −12.24% | 1.291 / 0.878 | 15.26% / 0.8737 / −33.72% | FAIL on CAGR |
| SMALL | FULL | 4.26% | 0.6596 | −14.16% | 0.806 / 0.548 | 14.03% / 0.8570 / −33.72% | FAIL on H1,H2,CAGR |
| SMALL | IS | 5.29% | 0.8752 | −8.41% | 1.043 / 0.675 | 12.02% / 0.8316 / −18.61% | FAIL on H2,CAGR |
| SMALL | OOS | 3.64% | 0.5458 | −14.16% | 0.950 / 0.129 | 15.29% / 0.8751 / −33.72% | FAIL on H1,H2,CAGR |

**4b is 0 of 9.** The binding leg is the CAGR floor on every panel in every window.

## (B) THE HEADLINE — the live book's margins are 4–6× OUTSIDE their own weekday noise

**130 of 144** leg-cells (panel × cost × window × leg) are RESOLVED, i.e. |margin| > that
leg's own 5-offset spread — **0.9028**; **138 of 144 (0.9583)** on the clip-free {0,1,2}
variant. On U56 + B136 at PROTOCOL's own 10 bps it is **23 of 24 (0.9583)**.

The leg that decides the verdict is the one furthest outside the noise. **CAGR margin /
CAGR spread at 10 bps:**

| panel | FULL | IS | OOS |
|---|---|---|---|
| U56 | −1.978 pp / 0.381 pp = **5.19×** | −2.862 / 0.634 = **4.51×** | −1.245 / 0.406 = **3.07×** |
| B136 | −2.627 / 0.455 = **5.77×** | −2.377 / 0.606 = **3.92×** | −2.833 / 0.488 = **5.81×** |
| SMALL | −5.559 / 0.211 = **26.4×** | −3.124 / 0.405 = **7.72×** | −7.065 / 0.161 = **43.8×** |

Over all four cost rungs the CAGR leg's worst ratio anywhere is **2.563×** (median 5.865×).
The DD leg — the one 914's clause was written for — runs **1.96× to 7.10×** at 10 bps
(median 4.55×), reproducing lane B's +8.18 pp vs 1.80 pp reading on U56 and extending it to
all three panels and all four rungs.

**So the clause does not kill the live book, and — read on the side nobody has read — it
does not rescue it either. RULES v2's 4b failure is a rule, not a weekday.**

## (B2) Where the clause DOES bite: the Sharpe legs, never the level legs
All **14** unresolved leg-cells are **H1 or H2** (0 of 36 DD, 0 of 36 CAGR). Ratio range by
leg at 10 bps: CAGR 3.07–43.8, DD 1.96–7.10, **H1 0.589–5.57, H2 0.599–23.9**. This is the
constructive half of 2119's residue — that run predicted the clause "should bite the CAGR leg
first"; on the live book it bites **neither level leg at any rung**, only the halves.

## (C) Verdict stability: 4b is immovable, 4a is not
The **4b verdict is identical at 5 of 5 offsets in 36 of 36 cells** (and is FAIL in all 36).
The **4a verdict moves in 11 of 36**: at 0 bps the live book beats itself-at-10-bps on 4a at
d=0 on all three panels, but only at **2–3 of 5** offsets on U56/B136. Path 4a over all 180
grid points: **35 pass (0.194)**. The clause's real target on the incumbent is 4a.

## (D) The bite does not move with cost — 2115 confirmed on the live book
spread(50 bps)/spread(0 bps), median over the 9 panel×window cells: H1 **1.0122**,
H2 **1.0071**, DD **1.0379**, CAGR **1.0003**. A 5× change in the cost rung moves the
weekday spread by ≤ 4% on the level legs. Independent confirmation, on a different book, of
2115's "path not cost" finding.

## (E) Rule 8 — 2017–2026 read ONCE, both arms

| panel | arm | IS pick | OOS book | OOS RULES v2 (d=0,10bps) | OOS SPY | 4b | 4a |
|---|---|---|---|---|---|---|---|
| U56 | both dials | d=1, 0 bps | 9.37% / 1.2710 / −12.54% | 9.46% / 1.2767 / −12.05% | 15.29% / 0.8751 / −33.72% | FAIL (CAGR) | FAIL |
| U56 | offset only @10bps | d=1 | 9.18% / 1.2465 / −12.58% | 9.46% / 1.2767 / −12.05% | same | FAIL (CAGR) | FAIL |
| B136 | both dials | d=1, 0 bps | 7.96% / 1.1194 / −12.57% | 7.85% / 1.1017 / −12.24% | 15.26% / 0.8737 / −33.72% | FAIL (CAGR) | FAIL |
| B136 | offset only @10bps | d=1 | 7.73% / 1.0899 / −12.63% | 7.85% / 1.1017 / −12.24% | same | FAIL (CAGR) | FAIL |
| SMALL | both dials | d=1, 0 bps | 3.88% / 0.5772 / −14.10% | 3.64% / 0.5458 / −14.16% | 15.29% / 0.8751 / −33.72% | FAIL (H1,H2,CAGR) | PASS |
| SMALL | offset only @10bps | d=1 | 3.60% / 0.5394 / −14.46% | 3.64% / 0.5458 / −14.16% | same | FAIL (H1,H2,CAGR) | FAIL |

**0 of 6 arms pass 4b. NO KEEP CANDIDATE, no memo, RULES untouched (rule 6).** Two things
the walk-forward buys beyond the verdict:

1. **The IS chooser prefers a weekday nobody is allowed to pick.** On all three panels and
   both arms, IS Sharpe argmax lands on **d = 1**, not the published d = 0 — and d = 1 is
   WORSE out of sample on 5 of 6 arms. Selecting the offset is a coin flip that costs.
2. **The cost rung is a degenerate rule-8 dial.** Argmax Sharpe picks **0 bps every time**,
   because cost is a fact of the world and not a choice. The "offset only @10bps" arm exists
   precisely so the walk-forward is read at PROTOCOL's own rung; it changes no verdict.
3. **Selection width on the offset dial** (OOS Sharpe max−min): **0.0520 / 0.0519 / 0.0221**
   on U56 / B136 / SMALL — the unreported width any single-offset verdict carries.

## What this run cannot do (stated, not repaired)
One book (the live one), one cadence (weekly), one offset family (the 5 weekday phases of a
weekly rebalance). Monthly and quarterly books carry their own spreads and are not priced
here. The 4b bars are set by a **costless** SPY at every rung (idea 1063's one-sided
handicap stands, unrepaired). **SURVIVORSHIP (rule 9):** U56, B136 and SMALL are
current-constituent lists, so every absolute CAGR and drawdown level is optimistic; the SMALL
panel is the sub-$2B screen's survivors since 2010 and its levels are the most optimistic of
the three. The offset contrast is within-tape — same names, same dates, only the weekday
moves — and does not repair the level.

## Residue (not a rules change; RULES.md, PROTOCOL.md, scan.py, bot.py, baseline.py untouched)
1. Idea 914's clause is **safe to adopt**: turned on the incumbent it changes **0 of 36** 4b
   verdicts, so a Sunday review can adopt it without re-scoring the live book.
2. The clause should be written **symmetrically** — a FAIL margin inside its own spread is
   an UNRESOLVED FAIL, not a FAIL. On the live book no level leg is ever unresolved, so the
   symmetry costs nothing here, but it is free to state and it is the honest form.
3. The clause's real exposure is **path 4a and the two Sharpe halves**, not the level legs:
   11 of 36 4a verdicts move across the weekday, and 14 of 14 unresolved leg-cells are H1/H2.
