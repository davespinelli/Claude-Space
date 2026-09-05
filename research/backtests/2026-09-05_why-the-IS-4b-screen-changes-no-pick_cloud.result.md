# idea 132 — why-the-IS-4b-screen-changes-no-pick (cloud, 2026-09-05)

**Verdict: ANSWERED — explanation (A). KILL of the IS 4b screen as a *selector*; it survives only
as an *abstention* rule.**
The screen changes no pick because the **IS-Sharpe argmax is already admissible in 100% of the
cells where anything is** — and the same is true of the IS-Calmar argmax. Break the selector and
the screen does start moving picks (12 moved picks, **all 12 from non-Sharpe selectors**), which is
the direct evidence for (A) over (B). Its entire apparent OOS advantage is abstention: idea 129's
reading gives S1 − S0 = **+0.327** of mean OOS Sharpe; the same 216 picks read **paired** give
**+0.000**.

Script: `2026-09-05_why-the-IS-4b-screen-changes-no-pick_cloud.py` ·
console `…console.txt` · grid `…grid.csv` (306 rows) · picks/walk-forward `…picks.csv`,
`…walkforward.csv` (216 picks) · memo `…memo.md`

## Harness checks, run before any new number was read
* **(a0) engine-equivalence** on the 3 ungated books, all 3 panels: `max|diff| = 0.000e+00` (EXACT).
* **(a) reproduction of idea 129's corpus:** **306 of 306 rows matched**, `max|diff| <= 2.2e-16`
  across CAGR, Sharpe, MaxDD, IS Sharpe/CAGR/MaxDD, OOS CAGR/Sharpe/MaxDD and mean gross — EXACT.
  The screen under test is literally the code that produced the result under test.
* **P1 reproduction of the finding itself:** K_Sharpe / S1 picks in **7 of 18** cells, declines in
  **11**, and among the 7 the arm **differs from the unscreened S0 pick in 0** — idea 129's
  "changes 0 of 18", re-derived. HELD.

## The discriminator (A) vs (B), measured not inferred

| selector | screen | picks in | moved where it picks | unscreened argmax already admissible | mean admitted / 17 |
|---|---|---|---|---|---|
| K_Sharpe | S1 / S2 | 7 | **0 / 0** | **100% / 100%** | 2.5 / 3.0 |
| K_Calmar | S1 / S2 | 7 | **0 / 0** | **100% / 100%** | 2.5 / 3.0 |
| K_CAGR | S1 / S2 | 7 | 3 / 3 | 57% / 57% | 2.5 / 3.0 |
| K_MaxDD | S1 / S2 | 7 | **5 / 1** | 29% / 86% | 2.5 / 3.0 |

**12 moved picks in total, 12 of them from non-Sharpe selectors → (A).** The refinement the queue
did not anticipate: the immunity is not Sharpe's alone. **K_Calmar is equally immune**, and it is
the two *risk-adjusted-return* selectors that are immune while the two single-axis ones
(K_CAGR, K_MaxDD) are moved. The screen is a conjunction of a Sharpe-like condition (two halves
bars, an OOS bar) with a drawdown cap and a return floor; an argmax of a statistic that already
trades return against risk lands inside it by construction, an argmax of return alone or of
drawdown alone does not.

## Why the admissible set cannot move a pick: it is a cell filter, not an arm filter

| cell | admitted S1 / S2 (of 17) | cell | admitted S1 / S2 |
|---|---|---|---|
| broad / EWall / 10 | 5 / 9 | u56 / EWall / 10 | 10 / 12 |
| broad / EWall / 25 | 1 / 2 | u56 / EWall / 25 | 8 / 10 |
| broad / TOP20 / 10 | 12 / 12 | u56 / TOP20 / 10 | 8 / 8 |
| broad / TOP20 / 25 | 1 / 1 | u56 / TOP20 / 25 | **0 / 0** |
| broad / V1u / 10, 25 | **0 / 0** | u56 / V1u / 10, 25 | **0 / 0** |
| small / all 3 books, both costs (6 cells) | **0 / 0** | | |

Median admitted per cell is **0 of 17**; the set is non-empty in **7 of 18** cells. What the screen
actually removes is **the whole small panel (6 of 6 cells), the whole V1u book (4 of 4), and
u56/TOP20 at 25 bps** — a book-and-panel judgement, not a choice among overlays. Inside the 7 cells
it does admit, it admits 1–12 arms and always the one the selector wanted.

## The apparent OOS gain, read three ways (mean OOS Sharpe, S1 − S0)

| selector | idea 129's reading (cells where it picks) | FALLBACK (all 18, decline → hold the control) | PAIRED (the 7 cells where every screen picks) |
|---|---|---|---|
| K_Sharpe | **+0.327** | +0.055 | **+0.000** |
| K_Calmar | +0.311 | +0.028 | **+0.000** |
| K_MaxDD | +0.412 | +0.129 | −0.012 |
| K_CAGR | +0.274 | −0.012 | −0.001 |

**P4 HELD for all four selectors.** The exactly-zero PAIRED column for K_Sharpe and K_Calmar is
not a rounding artefact — it is the same arm, so it is the same return series. The gain is entirely
in *which cells the screen declines to enter*, and it survives as +0.055 under FALLBACK only
because declining to enter the small panel and V1u is itself a good decision.

Absolute levels for context (FALLBACK, 18 cells): K_Sharpe S0 0.695 → S1 0.750; SPY OOS Sharpe
0.882 in every cell; RULES v1 OOS Sharpe 0.576 (broad @10) down to 0.146 (broad V1u @25); the
ungated control ranges 0.146–1.168. Picks beat SPY in 6 of 18 cells and RULES v1 in 12 of 18.

## S1 vs S2 — the CAGR floor
S1 and S2 pick the **identical arm in every cell for K_Sharpe, K_Calmar and K_CAGR**; only
K_MaxDD's pick moves (5 moves under S1 vs 1 under S2, and its PAIRED reading flips from −0.012 to
+0.014). Deleting the floor changes the admitted count from a median of 0 to a median of 0
(2.5 → 3.0 arms on the mean). On this corpus the floor is inert for any selector that is not the
drawdown argmax — which is the same conclusion idea 129 reached, now shown to be robust to
breaking the selector.

## KEEP paths on every pick (rule 8: chosen on 2009–2016, read once on 2017–2026)
53 distinct picked arms. **18 pass 4a; 7 pass 4b on the full sample; the same 7 pass 4b again on
the OOS window alone** — `broad/EWall {vol60-dg @10, band3-rw @10, vol60-dg @25}`,
`u56/EWall {abs12-rw @10, band3-rw @10, vol60-dg @25}`, `u56/TOP20 vol60-dg @10`. Every one is a
pre-existing leaderboard book; **this run promotes nothing and does not try to**. Example:
`u56/EWall/band3-rw @10` 12.2% / 1.161 / −17.7% (halves 1.210/1.129), OOS 13.4% / 1.203 / −17.7%,
against SPY 15.5% / 0.882 / −33.7% OOS and RULES v1 7.7% / 0.747 / −13.8% OOS.

## Pre-registered predictions, scored
* **P1** reproduce idea 129 (0 moves, declines in 11 of 18) — **HELD**.
* **P2** a non-Sharpe selector's pick is moved by the screen — **HELD**, 12 moves, all non-Sharpe → (A).
* **P3** minority admissible (median 0 < 9) and contains the K_Sharpe argmax in ≥90% of non-empty
  cells (100%) — **HELD**.
* **P4** FALLBACK halves S1's apparent gain for every selector — **HELD**, 4 of 4.
* **P5** K_Sharpe is the best selector on PAIRED cells — **FAILED**, and it is the **worst**:
  K_MaxDD 1.052, K_CAGR 1.047, K_Calmar 1.040, K_Sharpe 1.022. On 7 cells this is noise, and it is
  reported rather than acted on; it does say the incumbent selector has no measured OOS advantage
  over the alternatives it was compared against.

## Proposal to PROTOCOL (reporting clause, not a selector change)
Rule 8's IS 4b screen should be described and reported as an **abstention rule**: it decides
whether a (panel, book, cost) cell is worth entering at all, and it has been shown here to change
**0 of 18 picks** under the incumbent selector. Two consequences, both reportable numbers rather
than judgements:
1. Any walk-forward that quotes a screen's OOS advantage must quote it **paired or with an
   explicit fallback**, never averaged over the cells the screen chose to enter — for the
   incumbent selector those readings are +0.327, +0.055 and +0.000 for the same 216 picks.
2. Every screened walk-forward should report **admitted / total arms per cell** and **whether the
   unscreened argmax was already admissible**; when the second is always true the screen has done
   no selecting and should not be credited with any.

## Caveats carried, not buried
* Survivorship (idea 54): all three panels are current constituents; the small panel drops the 44
  tickers with `max_1d_move >= 1.0` (439 names) and its SPY is a joined benchmark, never
  selectable. Absent delistings inflate every CAGR, so every floor margin here is optimistic.
* Idea 128: the IS window's SPY drawdown is shallower than the OOS window's, so the IS drawdown cap
  is measured on a window that cannot express a deep drawdown. This biases the screen toward
  admitting **too much**, i.e. against P3 — and P3 held anyway.
* Idea 126: t+1 execution only. Idea 127: mean realised gross reported per row; dg/rw never collapsed.
* n = 18 cells and 7 paired cells. P5's ordering, and the K_MaxDD +0.014, are within noise at that
  size and are reported as such.

## Follow-ups proposed
1. `abstention-is-the-whole-screen` — if the screen's value is declining to enter the small panel
   and V1u, test the abstention directly: a rule that trades only cells whose IS window clears the
   4b bars, against always-trade and against never-trade, on returns rather than on picks.
2. `is-Calmar-immunity-general` — K_Calmar was immune too. Test whether every risk-adjusted-return
   argmax is immune to a screen built from Sharpe-like bars, on random bar values (bears on idea 110).
3. `selector-comparison-needs-more-cells` — 7 paired cells cannot order four selectors. Re-run the
   same comparison on idea 133's 816-row widened corpus, where the cells are 4× as many.
