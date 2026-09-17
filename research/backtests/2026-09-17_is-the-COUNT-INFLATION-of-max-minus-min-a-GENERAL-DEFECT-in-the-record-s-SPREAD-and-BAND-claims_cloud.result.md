# Idea 1155 (cloud, 2026-09-17) — is the COUNT INFLATION of max-minus-min a GENERAL DEFECT in the record's SPREAD and BAND claims?

**ANSWERED = YES, IT IS GENERAL AND IT IS DETERMINISTIC: the count-matched spread is strictly
smaller at 54 of 54 cells where the counts differ, and exactly equal at 18 of 18 where they do
not. There is no cell in between.**

## Arm 0 — the arithmetic, printed before any data was touched

A range is not an estimator of dispersion. For k iid N(0,1) draws E[max−min] = d2(k):

| k | 2 | 3 | 4 | 6 | 10 |
|---|---|---|---|---|---|
| d2(k) | 1.128379 | 1.692569 | 2.058751 | 2.534413 | 3.077505 |
| ladder | CADENCE | — | H | N | GROSS |
| vs k=2 | 1.0000 | **1.5000** | 1.8245 | 2.2461 | **2.7274** |

Monte Carlo at 4e5 draws reproduces every constant to 2.13e-3 (gate G0). **The record's own
four ladders are 2, 4, 6 and 10 rungs long, so a GROSS ladder's max−min is 2.7274× a CADENCE
ladder's ON PURE NOISE and 1.4948× an H ladder's, before any effect exists at all.**

**1140's committed "1.7× – 61× band" pools a k=2 range with a k=3 one, and d2(3)/d2(2) =
1.5000 exactly. Its FLOOR is therefore 1.7/1.5 = 1.133× the count difference alone — the
bottom of that committed band is indistinguishable from zero effect** (gate G0b).

## Arm A — census (32,930 committed text units)

| claim set | n | states a point count | **compares DIFFERENT counts** | x-to-x band | **adjudicates with NO count** |
|---|---|---|---|---|---|
| C_STRICT | 313 | 191 (0.6102) | **90 (0.2875)** | 13 | **122 (0.3898)** |
| C_PROX | 496 | 277 (0.5585) | 123 (0.2480) | 21 | 122 (0.2460) |
| C_ALL | 4,442 | 1,842 (0.4147) | 695 (0.1565) | 21 | 1,302 (0.2931) |

**Re-expressing the 90 checkable C_STRICT units** (those stating both a multiple and two
different point counts), against the d2(k_max)/d2(k_min) their own counts buy:

- the **SMALLEST quoted multiple survives its own count inflation at only 54 of 90 (0.6000)** —
  **two in five committed spread multiples are smaller than what the rung-count difference
  alone produces, i.e. they are not effects, they are the two counts**;
- the largest quoted multiple survives at 73 of 90 (0.8111);
- median inflation carried: **1.8999**.

## Arm B — re-walking the record's four ladders (3 panels × 4 ladders × 6 statistics = 72 cells)

| ladder | k | measured M_NONE/M_SUBSAMPLE | **predicted d2(k)/d2(2)** | M_NONE/M_D2 | M_PAIRWISE/M_NONE |
|---|---|---|---|---|---|
| CADENCE | 2 | 1.0000 | 1.0000 | 1.1284 | 1.0000 |
| H | 4 | 1.8524 | 1.8245 | 2.0588 | 0.5398 |
| **N** | 6 | **2.2467** | **2.2461** | 2.5344 | 0.4453 |
| GROSS | 10 | 2.4545 | 2.7274 | 3.0775 | 0.4074 |

**On the N ladder the realised count inflation matches the pure-noise prediction to 6e-4.**
The H ladder matches to 0.028. **On these two dials the published "spread" is, to measurement
precision, ENTIRELY the rung count.** GROSS comes in **below** its prediction (2.4545 against
2.7274) — and that shortfall is not a failure of the arithmetic but a measurement of idea
1189's degenerate gross ladder: d2 assumes independent rungs, and a ladder whose rungs are
near-identical realises **less** range than noise would. **The d2 prediction is an upper bound
for a monotone ladder, and the gap from it is a degeneracy statistic.**

**1148's headline, re-measured on 12 (panel, ladder) families:** count-matched < max−min at
**54 of 72** cells, median ratio **1.9680** (1148 committed 5 of 6, median 1.137×). The 18
cells that do not shrink are **every CADENCE cell and only those** — k=2 is already k_min, so
matching is a no-op. **The relation is exact, not statistical: 54 of 54 strictly smaller where
k>2, 18 of 18 equal where k=2** (gates G4, G5). 1148's 1.137× understates the defect **1.73×**
because 1148 matched to a larger k_min than the record's shortest ladder.

### The limit of the repair, stated as a gate

**M_D2's t-statistic equals M_NONE's at every cell to 3.6e-15 (gate G7)** — d2 is a constant
divisor at fixed k, so it cannot change a WITHIN-ladder verdict. Decisiveness at a 2-block-
bootstrap-SE bar (L=63, 400 draws) is **0.3472 under M_NONE and M_D2, 0.3333 under
M_SUBSAMPLE and M_PAIRWISE**. **Count matching makes ACROSS-ladder comparison legal and does
essentially nothing for whether any spread is measurable at all. Two thirds of the record's
ladder spreads do not clear 2 SE under ANY convention.**

## Arm C — rule 8 walk-forward: the matching rule as the chooser

The record's habit is *"this dial moves the statistic most, so tune it"*. Here the chooser
reads each ladder's IS-window (2009-2016 **only**) Sharpe spread under one matching rule, takes
the widest ladder, then takes that ladder's IS argmax. 2017-2026 read **once**. C_ANCHOR
(never move off N=20/H=126/g=0.75/W) is the do-nothing control.

| rule | widest ladder chosen | mean OOS Sharpe | mean OOS CAGR | mean OOS MaxDD | 4b picks |
|---|---|---|---|---|---|
| M_NONE | H, N | 0.8672 | 14.94% | −28.52% | 0 of 3 |
| M_SUBSAMPLE | CADENCE, N | 0.8198 | 13.71% | −25.87% | 0 of 3 |
| M_PAIRWISE | CADENCE, N | 0.8198 | 13.71% | −25.87% | 0 of 3 |
| M_D2 | CADENCE, H, N | 0.8865 | 14.94% | −26.11% | 0 of 3 |
| **C_ANCHOR (do nothing)** | — | **0.8934** | 13.71% | **−25.46%** | **1 of 3** |

**THE CAPITAL FINDING IS NOT THE REPAIR, IT IS THAT THE HABIT LOSES TO DOING NOTHING.** Every
matching rule, the status quo included, is beaten out of sample by never moving off the anchor,
and the anchor is the only one of the five that reaches a 4b book at all (U56
N=20/H=126/g=0.75/W, OOS 16.13% / 1.1042 / −19.47% against SPY OOS 15.15% / 0.8686 / −33.72%).
On U56 M_NONE's widest-dial pick is N=5, OOS Sharpe 0.9512 at MaxDD −22.87% — **the chooser
walks off a 4b book and onto a worse one**. Count matching changes the dial chosen at 2 of 3
panels and does **not** repair this: M_SUBSAMPLE and M_PAIRWISE are the two **worst** rules
here. M_D2 recovers most of the gap but still trails the control.

## KEEP paths (PROTOCOL rule 4), all 66 books

**4a 0 of 66. 4b full 16, 4b OOS 17, BOTH 16** (U56 10/22, B136 6/22, **SMALL 0/22 on every
path**).

**NO NEW CANDIDATE, AND THE PASSER LIST IS A CROSS-RUN CONFIRMATION OF 1189.** Ten of the 16
passers are **one book read at a different GROSS rung** (U56 g=0.55…0.75 at Sharpe 1.102047 →
1.102906, a spread of **8.6e-04 over a 1.36× change in gross**; B136 g=0.50…0.70 at 1.105489 →
1.107079, spread 1.6e-03 over 1.40×). The remainder are the anchor itself and its N=15 / H=21
neighbours. **This run did not go looking for 1189's degenerate gross ladder — it fell out of a
census of range statistics, which is the strongest form the confirmation can take. Recorded,
not promoted. No memo.**

## PROTOCOL clause PROPOSED NOT ENACTED (rule 6)

> *"no range without its count"* — any committed sentence quoting a spread, band or range SHALL
> state the number of points it was taken over. A sentence comparing two such quantities over
> DIFFERENT counts SHALL either count-match them or divide each by d2(k); a raw max-minus-min
> ratio across unequal counts is not a comparison and may not be cited as one. **A published
> multiple below d2(k_max)/d2(k_min) SHALL be reported as no effect.**

Pricing: 313 C_STRICT units re-read, 90 checkable, **36 of them (0.4000) quoting a smallest
multiple at or below their own count inflation**, and 122 (0.3898) adjudicating with no count
stated at all and thereby revealed uncheckable.

## The gate that failed first, and why it is printed rather than patched over

**G1 failed on the first cut at 1.977e-02.** `build` writes its targets on the ALREADY-SHIFTED
rebalance rows (t+1, the application row), because that is where `nrun` starts each segment;
`engine.backtest` shifts **both** the weights frame and the mask, so an application-time frame
is lagged a second time. The comparand must be the decision-time frame Wdec[t] = W[t+1]. No
arithmetic changed — the first cut compared two books one trading day apart. **G1 now reads
2.78e-17.** Every other gate passed silently through that defect, which is the reason the gate
exists.

## Survivorship (rule 9)

U56 and B136 are CURRENT-CONSTITUENT lists. SMALL is the current output of a sub-$2B screen
less the documented `max_1d_move >= 1.0` exclusion (52 of 715 dropped → 663 names, SPY joined
as benchmark only). Every LEVEL above is optimistic and every 4a/4b count is an UPPER bound.
Arm B's quantity is a **ratio of two spreads of the same statistic on the same panel** and is
far less exposed; but MaxDD is one of the six statistics and a survivorship-flattered panel has
a shallower drawdown path, so the levels are published beside every ratio.

## Gates — 9 of 9 pass

G0 Monte-Carlo d2(k) == Hartley's constants (2.13e-3); G0b 1140's band floor against its own
count inflation; G1 fast runner == `engine.backtest` at **2.78e-17** (after the failure above);
G1b `engine.backtest`'s two NaN rows all sit inside the 260-row warm-up; G3 live RULES v2 U56
MaxDD −12.0549% == committed −12.05%; G4 M_SUBSAMPLE ≤ M_NONE at every cell; G5 M_PAIRWISE ≤
M_NONE at every cell; G6 claim sets nest; G7 M_D2 t == M_NONE t at 3.6e-15.

**KILL as a capital finding. ANSWERED = YES: count inflation is general, exact, and the largest
single term in the record's ladder-spread claims — but repairing it does not make the record's
"tune the widest dial" habit profitable, because that habit loses to doing nothing under every
convention including the repaired ones.**

Artefacts: `…_cloud.py`, `.console.txt`, `.d2.csv`, `.census.csv`, `.claims.csv`,
`.reread.csv`, `.books.csv`, `.ladders.csv`, `.walkforward.csv`, `.gates.csv`. Follow-ups filed
1205–1207.
