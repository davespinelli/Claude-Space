# Idea 2101 (lane cloud, 2026-09-22) — is ANY legal IS-only chooser PORTABLE ACROSS PANELS?

**ANSWER: NO.  A legal IS-only chooser is not neutral machinery — it is a panel-specific
device, and "reached by a legal IS-only chooser" is a claim about the PANEL as much as
about the book.**  Idea 2087's one-family finding generalises to three families and a third
panel.

Script: `2026-09-22_chooser-portability-across-panels_cloud.py` (offline, deterministic).
Tuned dials, exactly two: CHOOSER (7 rules) x PANEL (3).  Reported, not tuned: three families
the record owns — BAND (band {0.00,0.03,0.06,0.10} x gross {0.50,0.75,1.00}, weekly), TOPN
(n {5,10,20,40} x gross, monthly), VOLTGT (target {0.08,0.12,0.16,0.20} x gross, monthly,
band 0.03) — 12 cells each, 108 books per cost rung, costs 0/10/25/50 bps, execution t+1,
warm-up 260 rows, IS <= 2016-12-31, OOS >= 2017-01-01 read once.  **All 432 cell-cost rows are
in `.grid.csv` and all 252 picks in `.choosers.csv`; nothing below is selected.**

## Panel bars (10 bps)

| panel | SPY FULL | SPY OOS | RULES v2 FULL | RULES v2 OOS |
|---|---|---|---|---|
| U56 (55 names) | 15.14% / 0.885 / −33.72% | 15.29% / 0.875 / −33.72% | 8.64% / 1.208 / −11.90% | 9.49% / 1.285 / −11.90% |
| B136 (135) | 15.12% / 0.884 / −33.72% | 15.26% / 0.874 / −33.72% | 7.96% / 1.099 / −12.18% | 7.85% / 1.104 / −12.18% |
| SMALL (665) | 14.03% / 0.857 / −33.72% | 15.29% / 0.875 / −33.72% | 4.26% / 0.659 / −14.16% | 3.63% / 0.545 / −14.16% |

## (1) THE CHOOSER IS NOT NEUTRAL — spread up to 0.917 of the shelf

OOS-Sharpe percentile of the picked cell inside its own 12-cell shelf (0.500 = a uniform draw).
Worst shelf: B136/TOPN, where IS_CAGRSLACK lands at **0.958** and IS_LEGS at **0.042** — the same
grid, the same rule-8 wording, opposite ends of the shelf.  Every one of the 9 shelves spreads
by **at least 0.417**; median spread **0.667**.  GATE G2 PASS.

## (2) AND IT DOES NOT TRANSPORT — median cross-panel rho +0.3638, with outright INVERSIONS

Spearman rho of the seven choosers' ranks, panel vs panel, at 10 bps:

| family | U56–B136 | U56–SMALL | B136–SMALL |
|---|---|---|---|
| BAND | **+1.0000** | +0.3757 | +0.3757 |
| TOPN | +0.3234 | +0.2887 | **−0.5601** |
| VOLTGT | +0.7594 | **−0.7779** | **−0.6321** |
| pooled (3 families) | +0.7092 | +0.4001 | +0.3519 |

Median over the 12 readings **+0.3638**, against a pre-stated portability bar of +0.50 —
**GATE G3 FAIL**.  Three of twelve readings are NEGATIVE: on VOLTGT the chooser ranking
U56 -> SMALL is not merely unstable, it is *reversed*.  The two large-cap panels (55 of 56 names
shared) agree far better than either agrees with SMALL, i.e. what looks like portability in the
record is mostly U56 and B136 being the same panel twice (idea 719's point, priced).

## (3) ONE RULE OF SIX IS STABLE IN SIGN — and the no-information control beats five of six somewhere

Pooled mean OOS percentile per panel: IS_CAGRSLACK **0.653 / 0.597 / 0.764** is the only rule
above the uniform-draw 0.5 on all three panels (GATE G4 PASS, 1 of 6).  IS_SHARPE — the
record's most-used chooser — runs **0.736 / 0.347 / 0.597**, i.e. *below a coin flip on B136*.
CELL_ALPHA, the no-information alphabetical control, scores **0.792** on SMALL/TOPN, beating
every informed rule on that shelf.  The cost ladder does not rescue this: stable rules run
1 / 1 / 1 / 2 of 6 at 0 / 10 / 25 / 50 bps and pooled rho +0.206 / +0.400 / +0.621 / +0.397.

## (4) BOTH KEEP PATHS — one chooser-reached 4b candidate, U56-only

At 10 bps, over 108 cells: **4a 4**, **4b FULL+OOS 18**, and **0 of 36 on SMALL**.  Over the 63
chooser picks: 4a 2, 4b FULL+OOS 11.  Every 4b passer runs gross 0.50–0.75 — the DD cap
(0.60 x SPY = −20.23%) is doing the selecting, which is the record's standing de-grossing result.

The best chooser-reached book is **U56 / BAND / band 0.10 / gross 0.75**, picked by IS_LEGS and
IS_MINMARG (2 of 7):

| | CAGR | Sharpe | MaxDD | H1 / H2 |
|---|---|---|---|---|
| FULL | 13.55% | 1.226 | −18.19% | 1.270 / 1.199 |
| OOS (2017–2026, read once) | **14.68%** | **1.260** | **−18.19%** | — |
| SPY OOS | 15.29% | 0.875 | −33.72% | — |
| RULES v2 OOS | 9.49% | 1.285 | −11.90% | — |

4b FULL and OOS at **0, 10, 25 and 50 bps** (turnover 2.19 turns/yr).  4a FAILS at every rung
(MaxDD −18.2% vs the live book's −11.9%).  **It does NOT replicate:** the identical cell on B136
clears 4b at 0 bps and fails from 10 bps on, by **0.05 pp** of drawdown (−20.28% against the
−20.23% cap), and SMALL has no 4b cell at all.  That failure is this run's own thesis, not an
aside: the candidate exists because the chooser met U56.

## WHAT THIS TEST CANNOT DO (stated, not repaired)

Three families, 12 cells each, one split point, one cadence per family.  A wider grid could move
any single rho.  All three panels are current-constituent lists and SMALL is the worst of them
(names sub-$2B *today* that have priced since 2010 — every delisting, acquisition and wipeout is
absent, and the 54 tickers with `max_1d_move >= 1.0` were dropped first), so every LEVEL above is
optimistic; the portability statistic is a panel-to-panel CONTRAST and is less exposed, but a
chooser could be stable across three biased panels and unstable across three honest ones.

## RESIDUE (not a rules change; rule 6)

(1) Every committed "reached by a legal IS-only chooser" verdict should name its chooser AND its
panel; on this evidence the phrase alone carries a selection width of up to 0.92 of a shelf.
(2) IS_CAGRSLACK is the only rule that survives all three panels here — a candidate convention,
not yet a finding (1 of 6 at n=3 panels is not distinguishable from luck).
(3) U56 and B136 are not two independent replications of a chooser claim.
