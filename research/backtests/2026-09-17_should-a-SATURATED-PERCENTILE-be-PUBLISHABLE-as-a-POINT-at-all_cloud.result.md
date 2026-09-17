# Idea 1199 (cloud, 2026-09-17) — should a SATURATED PERCENTILE be PUBLISHABLE as a POINT at all?

**ANSWERED = NO, AND THE COST IS NOT RHETORICAL: THE POINT FORM'S ARGMAX IS ITS TIE-BREAK.**

## The arithmetic, printed before any data was touched

A percentile read as `mean(null < obs)` over K draws lives on the lattice {0, 1/K, …, 1}. A
reading of 1.000 means only *"obs exceeded all K draws"*. The four conventions print four
different sentences for that one event:

| K | B_POINT | B_ONE `> 1−1/(K+1)` | B_CP `0.05**(1/K)` (one-sided 95% Clopper–Pearson) |
|---|---|---|---|
| 10 | 1.000 | 0.909091 | **0.741134** |
| 100 | 1.000 | 0.990099 | 0.970487 |
| 400 | 1.000 | 0.997506 | 0.992539 |

At K=10 the honest 95% statement is **0.741**, not 1.000 — the point form overstates the
evidence by **0.259 in the statistic's own units**, and 1197 found 0.963–1.000 of U56/B136
cells sitting exactly there. B_CP is strictly the most conservative rung at every K (gate G0).

## Arm A — census (32,887 committed text units; 1197's harvester verbatim, gate G6b)

| claim set | n | ceiling-quoted | floor-quoted | states K | adjudicated | **adjudicated AT the ceiling** |
|---|---|---|---|---|---|---|
| C_STRICT | 104 | 26 | 10 | 40 | 86 | **23** |
| C_PROX | 264 | 26 | 10 | 82 | 196 | 23 |
| C_ALL | 1,742 | 36 | 12 | 400 | 1,117 | 29 |

**The reader's first and largest loss is one the POINT form hides rather than avoids.** A
bound form is a *function of K*. Of the 31 saturated C_STRICT units, only **21 are
re-expressible at all**; **0.3226 state no draw count and so cannot carry any bound**
(C_ALL: 0.4884). Those units are not *made* uncheckable by the convention — they already
were; the point form simply never said so. Median move on re-expression: **0.0015** (B_ONE),
**0.0044** (B_CP). **Ten C_STRICT units quote the FLOOR**, which B_ONE leaves unrepaired and
only B_TWO covers.

## Arm B — price: 36 books × 3 panels, 14,400 gross-matched null backtests, K ladder nested (G8)

Distinct values the statistic takes over a panel's 12 books (mean of 20 seeds):

| panel | K=10 | K=50 | K=400 | CH_Z at every K |
|---|---|---|---|---|
| U56 | 1.75 (sat 0.912) | 3.40 (0.729) | 5.00 (0.500) | **12.00** |
| B136 | 1.40 (0.967) | 2.40 (0.842) | 5.00 (0.583) | **12.00** |
| SMALL | 6.35 (0.367) | 9.25 (0.171) | 12.00 (0.000) | 12.00 |

On the large-cap panels the point form separates 12 books into **1.4–1.75 values at K=10**,
with **10.95 (U56) / 11.60 (B136) of 12 books tied at its maximum**. CH_Z ties at its maximum
**1.00 of 12 at every one of 360 cells** (gate G5). SMALL de-saturates completely at K=400 —
**saturation is a property of the statistic meeting an easy panel, not of the machinery.**

## Arm C/D — rule 8 walk-forward: the convention IS the chooser

IS window 2009-2016 only; 2017-2026 read once. B_POINT breaks ties FIRST-WINS (the record's
habit). B_ONE/B_TWO/B_CP declare the ceiling a TIE and break it on CH_Z — the statement a
bound form *forces* an author to make. Mean OOS Sharpe of the pick over 20 seeds, pooled over
18 (panel, K) cells:

| chooser | mean OOS Sharpe | vs B_POINT | picks clearing 4b |
|---|---|---|---|
| **B_POINT** | **0.8897** | — | **0 of 18** |
| B_ONE = B_TWO = B_CP | **0.9568** | **+0.0671** | **7 of 18** |
| CH_Z | 0.9524 | +0.0627 | 7 of 18 |
| CH_ISSHARPE | 0.8581 | −0.0316 | 0 of 18 |

**THE THREE BOUND FORMS ARE DECISION-IDENTICAL TO SIX DECIMAL PLACES AT ALL 54 CELLS.** They
differ only in the sentence they print. Every basis point of the +0.0671 comes from *declaring
the tie*, none from *how the bound is written* — which is the actual finding, and it says the
queue's choice of bound form is a publishing question, not a measurement one.

**THE MECHANISM, VISIBLE IN THE PICKS.** B_POINT lands on **N=5/M at 6 of 6 U56 K rungs and 5
of 6 B136 rungs** — the FIRST cell in the sort order — because 0.91/0.97 of cells are tied at
1.000 and the "argmax" is therefore the sort order itself. Its OOS Sharpe 0.9121 sits **below
SPY's own 0.8686 + its DD** (OOS MaxDD −28.7% against the bound form's −19.7%). A saturated
point percentile does not choose; the alphabet does, silently.

B_ONE reaches **U56 N=15/W at all six K rungs** (OOS CAGR 17.58% / Sharpe 1.1795 / MaxDD
−19.69%), against SPY OOS 15.15% / 0.8686 / −33.72% and live RULES v2 OOS 9.42% / 1.2717.

## KEEP paths (PROTOCOL rule 4), all 36 books

**4a 0 of 36. 4b full 6 of 36, 4b OOS 7, BOTH 6** (U56 5/12, B136 1/12, **SMALL 0/12 on every
path**). Passers: U56 N=15/W, N=20/W, N=30/W, N=30/M, N=40/M; B136 N=40/W.

**NO NEW CANDIDATE, AND THE REASON IS THE RECORD'S OWN.** U56 N=20/W **is** the standing
2026-09-04 incumbent. The five U56 passers span Sharpe 1.1520 → 1.2111 over an N ladder from
15 to 40 — a spread of 0.059 across a 2.7× change in holding count, and N=15/W beats the
incumbent by **0.0130 of full Sharpe and 0.0090 of OOS Sharpe**. That is idea 1189's
degenerate-ladder reading arriving from a fourth direction, a cross-run confirmation and not a
discovery. Preferring N=15/W over N=20/W would be selecting inside a ladder this record has
already measured flat. **Recorded, not promoted. No memo.**

## PROTOCOL clause PROPOSED NOT ENACTED (rule 6)

> *"no saturated percentile as a point"* — any committed sentence quoting a null percentile at
> an attainable extreme (`>= 1 − 1/(K+1)` or `<= 1/(K+1)`) SHALL publish it as a **bound**
> carrying its own draw count, and SHALL name the statistic used to break the resulting tie. A
> ceiling percentile quoted as a point, or quoted without K, is not an adjudication and may not
> be cited as one.

Pricing: 26 C_STRICT units re-read, 23 of them adjudicating; 21 re-expressible; **10 of 31
saturated units state no K and are thereby revealed uncheckable** — the clause's cost is
admitting that, not creating it.

## Survivorship (rule 9)

U56 and B136 are CURRENT-CONSTITUENT lists. SMALL is the current output of a sub-$2B screen
less the documented `max_1d_move >= 1.0` exclusion (52 of 715 dropped → 663 names, SPY joined
as benchmark only). Every LEVEL above is optimistic and every 4a/4b count is an UPPER bound.
The Arm C **comparison** between conventions runs two choosers over the *same* book population
and is far less exposed, but the levels are published beside it.

## Gates — 11 of 11 pass

G0 bound ordering; G1 fast runner == `engine.backtest` at 2.08e-17; G1b reproduces 1191's two
NaN rows in `engine.backtest` `returns` and confirms both sit inside the 260-row warm-up;
G2 determinism at 0; G3 live RULES v2 U56 MaxDD −12.0549% == committed −12.05%; G4 CH_PCT
distinct ≤ K+1 at every rung; G5 CH_Z never ties; G6 claim sets nest; G6b census reproduces
1197 (104/26/23/22 against its committed 103/26/23/22 — the corpus grew by one unit);
G7 null gross == 0.75 at every rebalance row; G8 the K ladder is nested and costs no draws.

**KILL as a capital finding. Verdict on the question: a saturated percentile should NOT be
publishable as a point — it costs 0.0671 of OOS Sharpe and 7 of 18 4b-clearing picks, and the
loss is entirely an undeclared tie-break.**

Artefacts: `…_cloud.py`, `.console.txt`, `.census.csv`, `.claims.csv`, `.reread.csv`,
`.bounds.csv`, `.books.csv`, `.grid.csv`, `.discrimination.csv`, `.walkforward.csv`,
`.gates.csv`. Follow-ups filed 1202–1204.
