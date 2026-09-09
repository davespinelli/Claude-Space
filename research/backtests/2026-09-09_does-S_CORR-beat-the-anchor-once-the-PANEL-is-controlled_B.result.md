# Idea 309 — does S_CORR beat the anchor once the PANEL is controlled? (2026-09-09, lane B)

**VERDICT: KILL. S_CORR's edge is a PANEL edge, not a RANKING edge, and no selector survives
the control. No KEEP candidate, no memo, no RULES change.** RULES.md, scan.py, bot.py and
baseline.py untouched.

Script: `research/backtests/2026-09-09_does-S_CORR-beat-the-anchor-once-the-PANEL-is-controlled_B.py`
Two tuned parameters only: **statistic** (RAW = book OOS Sharpe, idea 293's score; RESID =
book OOS Sharpe − that panel's EWall OOS Sharpe) × **block** (A = seeds 0–59, idea 293's
committed panels; B = seeds 100–159, idea 310's disjoint fresh block). Everything else — 9
strata (k∈{20,40,80} × q∈{0.25,0.50,0.75}), 60 seeds each, 2 ranked books, 7 selectors and
their pre-registered directions — is inherited verbatim. **All 540 selector-cell rows and all
3,240 panel-books are reported** (`.walkforward.csv`, `.survivors.csv`, `.permutation.csv`,
`.residual_level.csv`, `.keeppaths.csv`).

## Gates (run before any new number was read)
- **G-SEED** blocks A and B are disjoint in seed — PASS.
- **G0** SPY, the 4b comparand, recomputed from prices on the **small-panel calendar** (the
  calendar every constructed panel lives on): max |committed − recomputed| over 6 columns
  **4.305e-05** — PASS. The large-cap calendar gives 0.8871/OOS 0.8786 instead of
  0.8615/0.8820; the calendar alone is worth 0.0256 Sharpe, so the bar here is the
  small-calendar SPY and **not** the large-cap SPY quoted elsewhere in the record.
- **G1** idea 293's published S_CORR raw edge reproduced: CAND10 **+0.1456** (published
  +0.1456), CAND20 **+0.1430** (+0.1430), wins **15/18** (15/18); max |d| 3.937e-05 — PASS.
- **G2** against idea 293's own committed `.walkforward.csv`, 18 cells: max |d| **2.776e-16**
  — PASS.

## 1. There is almost nothing in the residual to select on
D = book OOS Sharpe − EWall OOS Sharpe on the same panel. Pooled over 36 (block × stratum ×
book) cells **mean D = −0.0210**; D_mean > 0 in only **9/36** cells; only **41.3%** of the
2,160 individual panel-books beat their own equal-weight panel OOS. **11 cells are
significantly negative (t ≤ −2), 3 significantly positive.** The damage is monotone in width:
CAND10 mean D −0.0378 (positive in 4/18), CAND20 −0.0041 (5/18), and the worst cells are the
widest, lowest-small-cap-share ones (k=80, q=0.25: −0.165 A / −0.153 B, t −12.7 / −11.5).
**On these panels the ranking is a cost, not an edge, before any selector is applied.**

## 2. S_CORR's 15/18 is the panel, and it does not replicate
| statistic | block A mean edge | A wins | A perm z | block B mean edge | B wins | B perm z |
|---|---|---|---|---|---|---|
| RAW (idea 293's score) | **+0.1443** | 15/18 | **+3.57** | +0.0774 | 12/18 | +2.14 |
| RESID (panel controlled) | **−0.0235** | 4/18 | **−2.35** | +0.0296 | 12/18 | +1.78 |

Controlling for the panel **erases the whole edge and flips its sign in block A**, where the
residual is significantly *worse* than a random draw. The two blocks disagree on the residual's
sign. Reverse-direction sign checks lose their meaning too (A_rev −0.0081 vs forward −0.0235:
the reverse is *better*).

## 3. No selector survives — on either statistic
Pre-registered bars, fixed before the residual was read: **B1** mean edge > 0 in both blocks;
**B2** edge > 0 in ≥14/18 cells in both blocks (14/18 is the weakest count that beats a fair
coin at p<0.05 one-sided); **B3** the reverse direction is worse in both blocks.

**RESID survivors: 0 of 7.** Best is S_RESID — the residual's own native selector, "pick the
panel where the ranking beat EWall in-sample" — which clears B3 only (A +0.0321 13/18 z+2.20,
B −0.0030 10/18 z+0.30): **the ranking's in-sample advantage does not carry to the next
seed block.** S_CORR fails B1 and B2; S_DISP fails both (A −0.0528, 4/18, z −3.25).

**RAW survivors: 0 of 7 as well.** Idea 293's own headline does not clear the replication bar
either: S_CORR is 15/18 in block A but **12/18** in the fresh block. S_EVOL is the mirror
image — significantly *worse* than random on RAW in both blocks (z −3.39 / −2.25).

## 4. The 4b footprint is the panel's, exactly as the queue suspected
Over all **3,240 panel-books** (1,080 panels × {CAND10, CAND20, EWall}, no selection):
**4a 2/3240 (0.06%), 4b 85/3240 (2.62%), BOTH 0/3240.** Binding bars: DD 3014 / H2 2917 /
OOS 2772 / CAGR 1974 / H1 1799.

- Of the **43** ranked-book 4b passes, **40 (93.0%) sit on a panel whose un-ranked EWall book
  also clears 4b.** Only 3 are candidates for a pass the ranking earned; 2 of those have a
  positive residual.
- **Ranking makes 4b passage less likely, not more:** EWall 42/1080 (3.89%) vs CAND20
  31/1080 (2.87%) vs CAND10 12/1080 (1.11%).
- Of the **504 selector picks, 9 clear 4b and all 9 (100%) sit on a panel where EWall clears
  it too.** Idea 293's PARK candidate (block A, k20/q0.25, seed 48) is one of them and its
  residual is **−0.1230** — the ranked book is 0.12 Sharpe *worse* than simply holding that
  panel equal-weighted.

## 5. Rule 8 headline (selection is IS ≤2016 only, OOS ≥2017 read once)
Comparands: SPY OOS Sharpe **0.8820** (OOS CAGR 15.45%, MaxDD −33.72%), RULES v2 restricted to
these panels OOS Sharpe **0.8332** (OOS CAGR 6.48%), do-nothing anchor OOS Sharpe **0.6602**
(CAGR 9.06%, MaxDD −28.78%), EWall OOS Sharpe 0.6812.

| selector | OOS CAGR | OOS Sharpe | OOS MaxDD | mean resid | beats SPY | beats v2 |
|---|---|---|---|---|---|---|
| S_CORR | 11.09% | 0.7711 | −28.23% | −0.0179 | 13/36 | 2/36 |
| S_DISP | 10.77% | 0.7378 | −30.15% | −0.0468 | 11/36 | 8/36 |
| S_RESID | 9.49% | 0.6910 | −27.68% | −0.0064 | 5/36 | 6/36 |
| S_ISS | 9.11% | 0.6621 | −28.73% | −0.0238 | 6/36 | 4/36 |
| S_EWALL | 8.55% | 0.6247 | −30.06% | −0.0255 | 5/36 | 2/36 |
| S_BREADTH | 8.15% | 0.6240 | −28.02% | −0.0235 | 5/36 | 6/36 |
| S_EVOL | 6.78% | 0.5382 | −29.47% | −0.0253 | 2/36 | 2/36 |

**Every selector's mean residual is negative.** Only 88 of 504 picks beat SPY OOS at all, and
every selector's OOS Sharpe sits below both SPY and the live RULES v2.

**SURVIVORSHIP:** constructed panels are drawn from *current* constituents of the small-cap
screen (`data/SMALL_PANEL_README.md`) and the large-cap universe, so every level here is
optimistic. The object under test is a selector over panels, not a book.
