# Idea 389 — does the MAB DD-damage SCALE survive a fourth panel? (cloud, 2026-09-07)

**Verdict: KILL of the premise. Idea 387's `corr(MaxDD, dMaxDD) = +0.781` for the MA
band is (a) partly a MECHANICAL identity, not a measurement, and (b) once specified
correctly, a THREE-POINT LINE that does not survive seven more panels. No 4a anywhere
(0/90 at every rung). No new 4b object — every 4b passer is a filed U56 cell plus one
random-sub-panel replicate.**

Script `2026-09-07_does-the-MAB-DD-damage-SCALE-survive-a-fourth-panel_cloud.py`.
Idea 387's leg-C matched grid run VERBATIM on 10 panels instead of 3: U56, B136,
SMALL439 (the incumbents), ETF36, and k=36 MIX draws at 0% and 50% ETF share, seeds
0/1/2 (idea 277's `build_pool()` seeding, so s=1.000 lands on ETF36 exactly). Two tuned
parameters: the dial (`m ∈ {0,5,10,20,40}` for NT, `b ∈ {0,.03,.06,.12}` for MAB) and
the panel. 90 grid rows (10 panels × 9 cells × 3 rungs), all reported in `.grid.csv`.

Gates: G1/G2 0.000e+00; G3a 0 disagreements; G3b 0/244,532 cells; G4 max |d| 0.000e+00
vs idea 333/384/387's committed B136 row; G5 MIX s=1.000 == ETF36 exactly; **G6 the 21
incumbent cells reproduce idea 387's committed `matched.csv` to max |d| 2.8e-14** — this
run is a strict superset of idea 387's leg C, not a re-derivation.

## 1. The statistic is mechanically +1.000 inside every panel

Within a panel the anchor (NT m=0) is a **constant**, so `dMaxDD = MaxDD − anchor` is an
exact affine function of `MaxDD`. The per-panel correlation is therefore `+1.0000` for
**all 10 panels and both arms** — printed in `[4b]`, and confirmed by the decomposition
in `[4c]` (within-panel-demeaned corr = 1.0000 for NT and MAB alike). Idea 387's number
is not a depth-scaling measurement of an instrument: it is a between-panel statistic
carrying a mechanical within-panel identity, and its pooled value moves with how the
panels' anchors happen to be spread.

## 2. Correctly specified, the scaling is zero

The claim "the damage scales with the book's own depth" is properly a statement about the
**panel's** depth, so the specified statistic is `corr(anchor_MaxDD, dMaxDD)` — the anchor
varies across panels and is fixed within one, so it carries no mechanical term.

| scope | arm | n panels | corr over panel means | corr over cells |
|---|---|---|---|---|
| idea 387's 3 (replication) | MAB | 3 | **+0.9914** | +0.7029 |
| idea 387's 3 (replication) | NT | 3 | +0.0124 | +0.0087 |
| **ALL 10 panels** | **MAB** | 10 | **+0.0302** | +0.0228 |
| **ALL 10 panels** | **NT** | 10 | −0.0044 | −0.0034 |
| EX-SMALL439 | MAB | 9 | **−0.6156** | −0.4405 |
| EX-SMALL439 | NT | 9 | +0.3054 | +0.2475 |

`+0.9914` on three points is a line through three points. On ten it is **+0.0302**, and
excluding the one deep panel it flips to **−0.6156** — the opposite sign to the published
claim. The MAB-minus-NT gap is **+0.0346** on the correctly-specified statistic.

## 3. Even on idea 387's own statistic the SPLIT does not survive

Pooled over 10 panels: MAB **+0.5828** [95% Fisher −0.28..0.78], NT **+0.1646**, gap
+0.4182 (idea 387: +0.781 / +0.160, gap +0.6210). The pre-registered HOLDS bar is met on
the MAB *level* — but the *split it was quoted for* collapses: dropping SMALL439 leaves
MAB **+0.5057** against NT **+0.4486**, gap **+0.0571**, because NT's corr nearly TREBLES
(+0.160 → +0.449) while MAB's falls. The H_scale/H_const contrast is a SMALL439 effect.

Idea 384's monotone `a(m)` fares no better: MAB spearman-in-dial is −1.000 on **1 of 10**
panels (U56, the same one panel idea 387 found), and is **positive** on 3 of 10.

The instrument split idea 387 established on *other* axes is untouched and still holds
here: NT removes 3.72x/yr of turnover to MAB's 2.04x and moves holdings by exactly
+0.0000 names (MAB −0.0212). It is only the *drawdown-scaling* half that dies.

## 4. KEEP paths and rule 8

**4a: 0/90 at 0, 10 and 25 bps** — nothing beats RULES v2 on any panel. 4b: 22/90 @0,
**10/90 @10**, 6/90 @25. Nine of the ten @10-bps passers are U56 cells already filed by
ideas 359/384/387 (the best still `U56 MAB b=0.12`: 13.88% / 1.1297 / −18.72%, H1/H2
1.0773/1.1800, OOS 1.2384). The tenth, `MIX00~1 MAB b=0.12` (15.55% / 1.1702 / −19.33%,
OOS 1.0837), is a **random k=36 sub-panel of B136** and sits inside idea 78/83's 46%
random-sub-panel base rate — not an object. First-failing 4b bars @10 bps: DD 65, H2 52,
CAGR 47, OOS 41, H1 33.

Rule 8 (dial on IS 2008-2016 Sharpe @10 bps, 2017-2026 read once): **12/20 picks above
SPY OOS 0.8820, 2/20 above RULES v2 OOS, 14/20 above the shared anchor, mean regret
+0.0223**; 3/20 picks also clear 4b. Every panel's MAB pick is **b=0.12, the grid edge**
(10/10) — idea 240/256's flag, and idea 390 is the open queue item for it. **Nothing
proposed for RULES.**

## 5. What the record should carry

Two amendments, both INFRASTRUCTURE (no RULES.md change, not a Sunday item):

1. **Retire `corr(MaxDD, dMaxDD)` as a scaling statistic.** Any delta measured against a
   within-group constant is affine in its own level; the statistic is only readable
   between groups. Where the record wants "does this instrument's damage scale with
   depth", the column is `corr(anchor_MaxDD, dMaxDD)` over panel means, with the panel
   count printed beside it.
2. **Idea 387's leg-C headline needs the amendment above appended.** Its lexicon audit,
   its 0-of-46 confound finding and its instrument split on turnover/holdings all stand;
   only the H_scale/H_const drawdown reading is withdrawn.

## Caveats

(1) Every panel is a **current-constituent** list — SURVIVORSHIP; 4b's CAGR floor is
tested in each book's favour throughout. (2) ETF36 and the six MIX panels are k=36
subsets of B136 and share history and names with it, so the ten depth points are **not**
independent draws — which makes the collapse to +0.03 a conservative reading, since
correlated points would if anything inflate a real slope. (3) Ten panels is ten points;
the Fisher bands above are wide and are printed in `.corr.csv` / `.depth.csv`.

Artefacts: `.grid.csv` (90 rows), `.matched.csv` (70 cells), `.corr.csv`, `.depth.csv`,
`.perpanel.csv`, `.decomp.csv`, `.walkforward.csv`, `.console.txt`.
