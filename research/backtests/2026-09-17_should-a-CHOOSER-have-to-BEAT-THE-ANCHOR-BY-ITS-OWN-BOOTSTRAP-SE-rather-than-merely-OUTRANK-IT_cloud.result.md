# Idea 1210 (cloud lane, 2026-09-17) — should a CHOOSER have to BEAT THE ANCHOR BY ITS OWN BOOTSTRAP SE rather than merely OUTRANK IT?

**VERDICT: KILL (capital) / ANSWERED = NO — the SE bar is CONSERVATISM, not information, and so
is the rank bar it was proposed to replace.**

## What was tested

1154 published three publishing rules over 72 pick decisions (3 panels × 2 anchors × 4 ladders ×
3 honest choosers) and committed, at C_ALL × L63: `R_RAW` (publish the IS argmax) mean OOS Sharpe
0.7996 with 6 of 72 4b books; `R_BAR` (publish only if P_pick ≥ 0.90) 0.7887 / 19; `R_ANCHOR`
(never move) 0.7901 / 24 — "the publish-the-argmax habit loses three quarters of its capital-worthy
books to doing nothing". It also found P_boot and the IS margin near-orthogonal (Spearman 0.1551).

The queue proposed a third rule that prices the pick directly:

> `R_SE(k, basis)` — move only when the IS argmax beats the **anchor** by k bootstrap SE of the
> **difference** stat(pick) − stat(anchor).

Two dials, every cell reported: **k** ∈ {0, 0.25, 0.5, 1, 1.5, 2, 3} and **basis** ∈ {`SE_JOINT`
(SD of the difference across 1000 joint moving-block redraws), `SE_MARGINAL` (√(var+var), the
correlation-blind estimate), `SE_IID` (block length 1)}. Block length frozen at 1154's L = 63; the
other three reported and never adjudicated on. Everything else is 1154's, inherited whole,
including its seed base — so the reproductions below are **bit-level**:

| | mean OOS Sharpe | 4b full | 4b OOS | 4a | moved |
|---|---|---|---|---|---|
| R_RAW | 0.7996 (dev 0.0) | 6 | 7 | 0 | 59 |
| R_BAR | 0.7887 (dev 0.0) | 19 | 19 | 0 | 13 |
| R_ANCHOR | 0.7901 (dev 0.0) | 24 | 24 | 0 | 0 |

Spearman(margin, P_pick) reproduces 1154's 0.1551 to **2.06e-05**; its resolved count reproduces
**17 of 72** exactly.

## The trap, declared before any number, and why it decides the run

`R_SE(k)` is monotone in k (G9) and at large k **is** `R_ANCHOR`. So "R_SE recovers the 18
capital-worthy books R_RAW loses" is true by construction and means nothing — `R_ANCHOR` recovers
all 18, costs nothing, needs no bootstrap and is already in the record. The run was therefore built
around one test: **at a matched move count**, does R_SE beat `R_BAR` and a **count-matched random
bar** (500 seeded uniform draws of the same number of moves from R_RAW's 59)?

## The answer

**No cell carries information.** Across the 18 R_SE cells with k > 0:

* **0 of 18** book more 4b passers than the 90th percentile of their own count-matched null.
* **0 of 18** beat it on mean OOS Sharpe. The best cell (k = 1.0, `SE_JOINT`, 28 moves, 17 books)
  sits at the **0.815** percentile; several sit far below (k = 0.5 `SE_JOINT` is at the **0.006**
  percentile on mean OOS Sharpe).

**And the rank bar is worse than random too.** `R_BAR` moves 13 times and books 19; a random bar
moving 13 times books a median of **20** (p10 18, p90 22). `R_BAR` sits at the **0.263** percentile
on 4b and **0.248** on mean OOS Sharpe. 1154's "the bar buys 19 books against R_RAW's 6" is bought
entirely by moving 13 times instead of 59 — and bought slightly worse than a coin would.

**The law.** If no bar carries information, a rule's 4b count is a function of its move count alone.
The straight line through the record's own two endpoints — `R_ANCHOR` 24 at 0 moves, `R_RAW` 6 at
59 — is `4b(m) = 24.0 − 0.3051·m`, fitted to **no data**. Against the count-matched null medians it
is exact:

| m | 0 | 6 | 13 | 19 | 28 | 41 | 47 | 59 |
|---|---|---|---|---|---|---|---|---|
| null median 4b | 24.0 | 22.0 | 20.0 | 18.0 | 15.0 | 12.0 | 9.0 | 6.0 |
| predicted | 24.00 | 22.17 | 20.03 | 18.20 | 15.46 | 11.49 | 9.66 | 6.00 |

Worst deviation **0.66 of a book** over the whole range m = 0…59, and across all 20 published rules
(R_RAW, R_BAR and the 18 R_SE cells) move count alone explains **R² = 0.9798** of the 4b count.
Meanwhile mean OOS Sharpe over those same 20 rules spans only **0.7828–0.7996** — a range of 0.0168
— while the 4b count swings 6 to 24. **The 4b count in this family is a threshold census of how
often a rule declined to move, not a return.**

**Rule 8, second stage.** The picks already use 2009-2016 only (1154's split). This run's own two
dials were then chosen on 2017-2021 and 2022-2026 read **once**: the IS-chosen cell is
k = 1.5 `SE_JOINT` (19 moves), IS Sharpe 1.0100 → **OOS-B 0.5580 / 7.17% / −17.23%**, against
`R_BAR` 0.5517 / 7.00% / −17.02%, `R_ANCHOR` 0.5543 / 7.26% / −17.35% and `R_RAW` **0.6042** /
7.74% / −18.50%. The chosen SE cell lands between the do-nothing control and the rank bar, and the
rule that moved all 59 times is the best of the four out of sample — the opposite of what the
resolution-bar programme predicts, and one more reading with no information in it. SPY over
2022-2026: 0.7298-0.7475 / 11.82-12.18% / −24.50%; live RULES v2: U56 1.1548, B136 0.8965, SMALL
0.1824.

## Two methodological findings worth carrying

**1. A correlation-blind error bar overstates a ladder difference by ~3.2×.** The pick's and the
anchor's bootstrap statistics co-move at median correlation **0.9247** (min 0.6777), so the SD of
their difference is far smaller than the two legs added in quadrature: median
`SE_MARGINAL / SE_JOINT` = **3.1580** (G10 confirms the inequality holds wherever the rungs
co-move positively). Any reader who prices a "rung A beats rung B" claim from two published error
bars will move roughly a third as often as the joint arithmetic warrants — `SE_MARGINAL` moves 6
times at k = 1 where `SE_JOINT` moves 28.

**2. The bootstrap SEED is an unstated dial in every P_boot claim in the record.** P_pick is a mean
of B = 1000 Bernoulli draws with MC standard error up to 0.0158, so a decision within that of the
0.90 bar is called by the seed. The same 72 decisions at L = 63 under four seed bases, nothing else
changed: **resolved 16-17 of 72, Spearman 0.1551-0.1749, R_BAR move count 12-13.** 1154 stated its
seed base; no other P_boot claim in the record does.

The SE bar is also **not** simply the margin bar re-scaled — Spearman(delta, delta/SE) is +0.5560 at
`SE_JOINT` over the 59 movers (G8), so the SE does vary across decisions (max/min 158.6). It varies;
it just does not vary in a way that predicts which moves keep a 4b book.

## Both KEEP paths (PROTOCOL rule 4)

144 distinct rung books: **4a 0 of 144**; 4b full 20; 4b OOS 24; both 19 — U56 14/48, B136 6/48,
**SMALL 0/48**. These are 1154's own rung books; this run re-reads them and adds none.
**NOT PROMOTED, NO MEMO, NO RULES CHANGE.** Benchmarks: SPY 14.06-15.16% / 0.8581-0.8861 /
−33.72% (OOS 15.15-15.33% / 0.8684-0.8767); live RULES v2 U56 1.1980 (OOS 1.2714), B136 1.0993
(OOS 1.1059), SMALL 0.6637 (OOS 0.5600).

## Survivorship (rule 9)

B136 and SMALL are CURRENT constituents. SMALL is the sub-$2B screen with 52 of 715 tickers dropped
for `max_1d_move >= 1.0`, leaving 663 names plus SPY as a benchmark column only; SPY is excluded
from SMALL's eligible set. SMALL books 0 of 48 on either KEEP path here.

## Gates: 12 of 12 pass

G1 live RULES v2 U56 MaxDD ≡ −12.05% · G2 population is 72 · G3 1154's Spearman reproduces
(2.06e-05) · G4 1154's resolved count 17 of 72 reproduces exactly · G5 R_RAW move count 59
reproduces · G6 R_SE(k=0) is **exactly** R_RAW · G7 1154's three committed mean OOS Sharpes
reproduce (0.0) · G8 the SE bar is not the identity on the margin bar · G9 R_SE's move count is
monotone in k · G10 SE_MARGINAL ≥ SE_JOINT wherever the rungs co-move · G11 every R_SE move set is
a subset of R_RAW's · G12 the null draws only from R_RAW's move set.

Runtime 105s, offline, deterministic.
