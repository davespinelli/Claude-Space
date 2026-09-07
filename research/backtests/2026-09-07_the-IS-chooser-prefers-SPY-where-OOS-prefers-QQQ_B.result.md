# Idea 371 — the-IS-chooser-prefers-SPY-where-OOS-prefers-QQQ (lane B, 2026-09-07)

**Verdict: KILL of the generalisation.** The rule-8 IS→OOS ordering inversion is **not** a
composition-dial property. Composition dials are the class rule 8 handles **best** in this
record; the inversions live on the CONTROL dials the queue named as the safe comparison
(gross, band width). Idea 30's own dial (C1) is confirmed, reproduced and fold-stable — and
is the **only** composition dial in the census that inverts.

Script `research/backtests/2026-09-07_the-IS-chooser-prefers-SPY-where-OOS-prefers-QQQ_B.py`,
console `..._B.console.txt`, grids `..._B.grid.csv` (270 points), `..._B.ordering.csv` (54),
`..._B.walkforward.csv` (156), `..._B.folds.csv` (162). Deterministic, offline caches only.

## Design

Nine one-parameter dials, 5 points each, **classified before any number was read** (the
classification is in the script docstring):

| | dial | class | what q moves |
|---|---|---|---|
| C1 | core-QQQ-vs-SPY | composition | idea 30's dial: c=0.60 gated core + 0.40 macro sleeve |
| C2 | core-QQQ-vs-IWM | composition | size composition of the same core |
| C3 | core-SPY-vs-EFA | composition | geography composition of the same core |
| C4 | sleeve-equity-membership | composition | idea-18 sleeve's 5 equity legs scaled, gross held at the q=1 level |
| C5 | book-blend v1-vs-v2 | composition | q of NAV run by RULES v1, 1−q by RULES v2, both gross 0.75 |
| C6 | sector-tilt XLK | composition | XLK's share of a 0.75-gross 11-sector book |
| W1 | width n | control-width | RULES v1 at n ∈ {3,5,8,12,20}, w = 0.75/n (gross fixed) |
| W2 | width band | control-width | RULES v2 band ∈ {0.00,0.03,0.06,0.12,0.20} |
| G1 | gross | control-gross | RULES v2 band 0.03, gross ∈ {0.20…1.00} |

**Exactly one tuned parameter per dial.** Panel (U56, B136), cost rung (0/10/25 bps) and dial
identity are reported axes: all 270 points are printed, both KEEP paths evaluated at every one.

**Gate.** C1 is idea 30's `c=0.60, GATE=ON` column. Against its committed grid CSV, 20 shared
cells (2 panels × 2 rungs × 5 q) reproduce at **max |diff| ≤ 2.2e-16** on CAGR, Sharpe, MaxDD,
H1, H2, IS Sharpe, OOS Sharpe and OOS CAGR. Idea 30's headline is exact: U56 @10 bps, OOS Sharpe
**1.024 → 1.094 → 1.134 → 1.151 → 1.153** monotone in q, IS chooser picks q=0.50, **−0.019**
below the q=1.00 anchor.

## The answer

**Rule 8 orders composition dials correctly and control dials badly** — the opposite of the
queue's premise. Spearman ρ(IS Sharpe, OOS Sharpe) across each dial's 5 points, 54 cells:

| class | cells | median ρ | ρ<0 | median regret | worst regret | IS pick = OOS best |
|---|---|---|---|---|---|---|
| composition | 36 | **+1.00** | **2** | **+0.000** | −0.065 (C2) | 19/36 |
| control (width+gross) | 18 | −0.20 | **11** | −0.003 | **−0.120** (W2) | 4/18 |

Excluding near-ties (IS Sharpe spread < 0.01, which removes all 6 G1 cells and nothing else):
composition unchanged; control 12 cells, ρ<0 in 5, median ρ +0.50, **median regret −0.052**.

**C1 is the outlier, not the representative.** Per-dial median ρ: C1 **+0.10**, C2 +0.70,
C3 +1.00, C4 +0.90, C5 +1.00, C6 +1.00. Drop C1 and the composition class is **30 cells,
0 inversions, median ρ +1.00, median regret 0.000**. Both composition inversions in the whole
census are C1's.

**C1's inversion is nevertheless real and fold-stable.** On the F1 fold (train ≤2013 → test
2014-16) C1's ρ is **−1.00 in 6/6 panel×rung cells**; F2 +0.10, F3 −0.30. So idea 30 found a
genuine, reproducible chooser error — on one dial, which does not transfer to its class.

**The sign the queue saw is a composition-dial signature, but a cheap one.** Where the pick
and the OOS best differ, the composition pick sits on the **lower-vol** side in **12 of 17**
disagreements (C1 dq −0.50, C2 −0.25: IS prefers SPY/IWM where OOS prefers QQQ); on control
dials that count is **0 of 14** — those errs run the other way (G1 picks max gross 6/6, W2
picks the wider band 6/6). The direction is right; the price is not: the composition class's
median regret is 0.000 and its worst is −0.065, against −0.120 on the width dials.

**The expensive chooser failure is the GROSS dial, and Sharpe hides it.** G1's ρ is **−1.00 in
6/6** cells — but its IS Sharpe spread is **0.001–0.005**, so the ordering it inverts is a
numerical tie, and the Sharpe regret is a trivial −0.001…−0.004. The consequence is in
drawdown: the IS pick (gross 1.00) runs **OOS MaxDD −15.9% / −16.2%** where the OOS-Sharpe-best
point (gross 0.20) runs **−3.3%**. Same finding as idea 372's ungated c-dial (chooser picks
c=1.00) and idea 351's Sharpe-neutral gross, on a third dial family: **ρ on a Sharpe-flat dial
is not a chooser diagnostic; the exposure it picks is.**

Three-fold check (162 cells): composition ρ<0 in **22/108** (median ρ +1.000, median regret
0.000), control ρ<0 in **23/54** (median ρ +0.250, median regret −0.007). Fold F1 is the
noisiest for both classes (composition 11 inversions of 36) — a 3-year test window, not a
class property.

## KEEP paths (both evaluated at all 270 points)

- **4a: 13/270 — but 12 of them are the live book tying with itself.** C5 q=0 and W2 band=0.03
  *are* `rules_v2(band=0.03, gross=0.75)`; their max |difference| over Sharpe/CAGR/MaxDD across
  all 6 panel×rung cells is **0.00e+00** (a useful identity gate, not a result), and 4a's
  no-worse-than test passes on a tie. **Non-degenerate 4a: 1/258** — B136 C5 q=0.25 at 0 bps
  (1.137 Sharpe, −11.4% DD), which dies at 10 bps.
- **4b: 7/270, every one on a CONTROL dial, none on a composition dial.** Five are G1 gross=1.00
  (U56 at 0/10/25 bps, B136 at 0/10; B136 @25 bps fails on CAGR). Two are W1 n=12 and n=20 on
  U56 **at 0 bps only** — both gone at 10 bps.
- Rule 8 selects the 4b passer in 6/7 cases and its pick clears 4b in 7/7 — but on G1 that
  "selection" rests on the 0.002 IS Sharpe spread above, i.e. it is not a selection.
- The G1 gross=1.00 cell is **not a new book**: it is the RULES-v2 (no vol filter) sibling of
  idea 66's already-recorded 4b KEEP `universe.json ew-band3 g=1.00` (2026-09-04, 15.1%/1.14/
  −19.9%, turnover 6.4x/yr; this one is 11.6%/1.205/−15.9% at 2.35x/yr on the corrected tape,
  weekly, without idea 66's `vol20 < 0.60` filter). Memo written for the Sunday review as a
  **one-parameter gross placement on the live book**, with the near-tie caveat stated:
  `..._B.memo.md`.

## What the record should take from this

1. **Retire the premise.** "Composition dials break rule 8" is false on 6 dials × 2 panels ×
   3 rungs × 4 windows. Do not open further ideas on it.
2. **Keep idea 30's finding as a single-dial fact.** C1's QQQ-vs-SPY inversion is real,
   fold-stable and worth −0.019 to −0.030; it is not evidence about any other dial.
3. **Pre-screen with the IS spread.** A ρ computed on a dial whose IS Sharpes span <0.01 (all
   6 G1 cells here) says nothing about the chooser. Report IS spread beside every ρ.
4. **Judge Sharpe-flat dials by exposure, not ρ.** G1 inverts perfectly and costs 0.002 Sharpe
   while multiplying OOS drawdown by 4.8x.

## Caveats

- Current-constituent panels: survivorship flatters levels, and most in the OOS window; the
  IS-vs-OOS *ordering* statistics are far less exposed, but not immune.
- 5 points per dial ⇒ ρ takes discrete values at 0.1 steps with ~1.5 effective d.f. Nothing
  here rests on a single ρ, only on the census across 9 dials × 2 panels × 3 rungs × 4 windows.
- C1–C4 and C6 hold only ETFs present in both panels: their panel axis is price-file rounding
  (max |U56−B136| ≤ 1.3e-03 on every metric, measured not assumed), so it is **not** an
  independent confirmation. C5, W1, W2, G1 are panel-sensitive.
- The dial classification was fixed in the docstring before results were read; the dial *set*
  is this run's choice and is not exhaustive (the queue's "S3/S4 arms" are not reproduced here).
