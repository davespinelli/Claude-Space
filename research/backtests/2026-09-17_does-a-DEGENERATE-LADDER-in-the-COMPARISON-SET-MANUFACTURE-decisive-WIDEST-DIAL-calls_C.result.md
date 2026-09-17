# Idea 1223 (lane C, 2026-09-17) — does a DEGENERATE LADDER in the COMPARISON SET MANUFACTURE decisive WIDEST-DIAL calls?

**VERDICT: KILL (capital). ANSWERED = YES, AND IT IS THE COMPARISON SET, NOT THE BAR, THAT
DECIDES.** One perfectly degenerate rung admitted to a degenerate-free set moves the pairwise
decisive rate from **0.0397 to 0.5198** and CREATES **37 of 42** H_ANY headline calls and **40 of
42** H_NARROWEST ones, destroying 0 and hijacking 0. 21 of 21 gates pass. Runtime 35s, offline,
deterministic, no new book.

Script: `2026-09-17_does-a-DEGENERATE-LADDER-in-the-COMPARISON-SET-MANUFACTURE-decisive-WIDEST-DIAL-calls_C.py`
Dials (2, PROTOCOL rule 4): **DEGENERACY LEVEL** δ ∈ {0.00, 0.01, 0.03, 0.10, 0.30, 1.00} ×
**COMPARISON SET** {NG, NG_D, ALL4, ALL4_D}. 24 cells, every one published in `.grid.csv`.
Nothing selected on.

---

## 1. The instrument

`DEG(δ)`, 6 rungs, k = 6 — the same rung count as the N ladder, so the count-matching inflation
`d2(k_w)/d2(k_n)` against N is exactly 1.000000 and the spread effect is isolated from the count
effect. Rung j is the anchor weight frame blended with the N = n_j frame,

    W_j(δ) = (1-δ)·W_anchor + δ·W_{N=n_j},   n_j ∈ {5,10,15,20,30,40}

a convex combination of two real weight frames, so every rung is a real tradable book at the
frozen gross 0.75 through the same 10 bps / t+1 runner. **δ = 0 makes all six rungs identical
(spread exactly 0); δ = 1 IS the N ladder bit for bit (G2 = 0.0).** Gross is preserved at every
row and every δ (G3 = 4.4e-16). The ALL4 pairs replay 1214's committed 252-row table (G9 =
4.5e-13).

## 2. Arm 0 — settled before any price was read

A ladder with identical rungs has Sharpe spread **exactly 0**, so every ordered pair against it is
written with it as the narrower leg, `M = R_w/0 = +inf`, `V = +inf`. **Every bar the record has
ever used returns a decisive W** — B_RAW, B_POINT, B_MED, B_IID95, and B_BOOT95, the block
bootstrap 1214 built precisely because it carries the real cross-ladder dependence (the resampled
spread is 0 in every rep, so z = +inf). The calls are not *wrong* — N really is more dispersed
than a thing that is not a dial — they are **vacuous, and indistinguishable in a census from calls
about real dials.**

The denominator arithmetic is just as blunt: adding a ladder to a set of m adds m pairs and changes
**no** existing one (G8 = 0), so the decisive rate moves `d/P → (d+m)/(P+m)`. A set of 3 honest
ladders with **zero** decisive pairs reads **0.5000** the moment one degenerate rung is admitted —
and 1214's headline 126 of 252 at ALL4 is exactly 0.5000.

## 3. The 24-cell grid (ALL GRID POINTS)

| set | δ | pairs | decisive | rate | D-pairs | D decisive | rate | med sp(D)/sp(N) |
|---|---|---|---|---|---|---|---|---|
| NG | any (inert, G10) | 126 | 5 | **0.0397** | 0 | — | — | — |
| NG_D | 0.00 | 252 | 131 | **0.5198** | 126 | 126 | **1.0000** | 0.0000 |
| NG_D | 0.01 | 252 | 130 | 0.5159 | 126 | 125 | 0.9921 | 0.0101 |
| NG_D | 0.03 | 252 | 123 | 0.4881 | 126 | 118 | 0.9365 | 0.0304 |
| NG_D | 0.10 | 252 | 90 | 0.3571 | 126 | 85 | 0.6746 | 0.1005 |
| NG_D | 0.30 | 252 | 38 | 0.1508 | 126 | 33 | 0.2619 | 0.3061 |
| NG_D | 1.00 | 252 | 50 | 0.1984 | 126 | 45 | 0.3571 | 1.0000 |
| ALL4 | any (inert) | 252 | 131 | **0.5198** | 0 | — | — | — |
| ALL4_D | 0.00 | 420 | 299 | 0.7119 | 168 | 168 | 1.0000 | 0.0000 |
| ALL4_D | 0.01 | 420 | 265 | 0.6310 | 168 | 134 | 0.7976 | 0.0101 |
| ALL4_D | 0.03 | 420 | 282 | 0.6714 | 168 | 151 | 0.8988 | 0.0304 |
| ALL4_D | 0.10 | 420 | 258 | 0.6143 | 168 | 127 | 0.7560 | 0.1005 |
| ALL4_D | 0.30 | 420 | 206 | 0.4905 | 168 | 75 | 0.4464 | 0.3061 |
| ALL4_D | 1.00 | 420 | 218 | 0.5190 | 168 | 87 | 0.5179 | 1.0000 |

Read through the five bar forms at the headline cell NG_D @ δ=0.00: **B_RAW 1.0000, B_POINT
1.0000, B_MED 1.0000, B_IID95 0.5198, B_BOOT95 0.5119** — the calibrated band and the bootstrap
band are manufactured at essentially the same rate as each other. **Calibrating the bar does not
protect a comparison set that contains a non-dial.**

## 4. Headline calls: created, destroyed, hijacked (NG → NG_D, 42 (panel, fold) cells each)

| δ | H_RUNNERUP | H_NARROWEST | H_ANY |
|---|---|---|---|
| 0.00 | 2→2, **created 0** | 2→42, **created 40** | 5→42, **created 37** |
| 0.01 | 2→2, created 0 | 2→42, created 40 | 5→42, created 37 |
| 0.03 | 2→2, created 0 | 2→42, created 40 | 5→42, created 37 |
| 0.10 | 2→2, created 0 | 2→34, created 32 | 5→40, created 35 |
| 0.30 | 2→2, created 0 | 2→15, created 14 (destroyed 1) | 5→25, created 20 |
| 1.00 | 2→25, created 23 | 2→2, created 0 | 5→42, created 37 |

**DESTROYED 1 in 18 cells; HIJACKED 0 everywhere.** A degenerate rung cannot take a call away or
rename one — it only adds. **H_RUNNERUP is immune at every δ ≤ 0.30**, because a degenerate rung
is never top-2; that is the one reading of "the widest dial" a degenerate comparison set cannot
touch, and it is the strictest one. The δ=1.00 row is the mirror: the rung stops being a foil and
becomes a *duplicate of N*, which is what creates 23 runner-up calls.

## 5. Where GROSS sits, and saturation

Median IS spread ratio to the N ladder over the 42 cells: **GROSS 0.0103**; DEG@0.00 0.0000,
**DEG@0.01 0.0101**, DEG@0.03 0.0304, DEG@0.10 0.1005, DEG@0.30 0.3061, DEG@1.00 1.0000.
**GROSS's degeneracy is δ ≈ 0.01 on this scale**, and the synthetic rung at that δ reproduces its
effect: decisive rate **ALL4 0.5198 vs NG_D@0.01 0.5159, |Δ| = 0.0040** (G12).

**SATURATION (G12b = 0):** ALL4 already contains a degenerate rung, so admitting a second one
changes **0 headline calls at every δ ≤ 0.30** — created 0, destroyed 0, hijacked 0 over 126
(panel, fold, form) cells per δ. *One degenerate rung is enough, and the record already has one.*

## 6. Price leg — rule 8, both KEEP paths, nothing promoted

Each (set, δ, headline form) made deployable: read the IS window, apply B_IID95 in that form, tune
the named ladder's IS-argmax rung, else hold the anchor. 5,040 pick-cells = 42 (panel, fold) × 4
sets × 6 δ × 5 choosers. Mean OOS Sharpe over 42 picks, paired delta vs CH_ANCHOR, SE clustered on
the 14 folds:

| chooser | set | move rate | mean OOS Sharpe | Δ vs ANCHOR | SE | t |
|---|---|---|---|---|---|---|
| CH_ANCHOR | — | 0.000 | **1.0362** | — | — | — |
| H_NARROWEST | NG | 0.024 | 1.0368 | +0.0006 | 0.0006 | +1.00 |
| H_NARROWEST | NG_D @ 0.00/0.01/0.03 | **0.881** | 0.9875 | **−0.0487** | 0.0502 | −0.97 |
| H_NARROWEST | NG_D @ 0.10 | 0.714 | 0.9974 | −0.0388 | 0.0592 | −0.66 |
| H_NARROWEST | NG_D @ 0.30 | 0.310 | 1.0231 | −0.0131 | 0.0351 | −0.37 |
| H_ANY | NG | 0.095 | 1.0394 | +0.0032 | 0.0226 | +0.14 |
| H_ANY | NG_D @ 0.00–0.03 | 0.881 | 0.9875 | −0.0487 | 0.0502 | −0.97 |
| H_RUNNERUP | NG / NG_D @ δ≤0.30 | 0.048 | 1.0179 | −0.0183 | 0.0158 | −1.16 |
| CH_RAW | any | 1.000 | 0.9677 | −0.0685 | 0.0514 | −1.33 |

**The manufactured calls are what makes the chooser move, and moving is what costs.** Admitting a
degenerate rung takes H_NARROWEST's move rate from 0.024 to 0.881 and its OOS Sharpe from
+0.0006 to −0.0487 of the do-nothing anchor; the cost shrinks monotonically as the rung stops
being degenerate (−0.0487 → −0.0388 → −0.0131). ALL4 already reads the manufactured numbers
(0.881, −0.0487) at every δ — again, GROSS is already doing this. None of these deltas is
resolved on 14 folds (|t| ≤ 1.33), and all of them point the same way: **toward the anchor.**

**RULE 8** (dials on warm-up..2016-12-31, 2017-2026 read once), 360 rows = 3 panels × 24 cells ×
5 choosers:

Only **eight distinct outcomes** exist across all 360 rows (every chooser lands on one of them):

| panel | pick (rows) | full CAGR / Sharpe / MaxDD | halves | OOS CAGR / Sharpe / MaxDD | 4a | 4b | 4b OOS |
|---|---|---|---|---|---|---|---|
| U56 | anchor CADENCE=W (55) | 15.71% / 1.1480 / −19.13% | 1.2127/1.1050 | **17.16% / 1.1759 / −19.13%** | F | **T** | **T** |
| U56 | N=40 (63) | 13.40% / 1.1311 / −22.46% | 1.2663/1.0361 | 14.08% / 1.1150 / −22.46% | F | F | F |
| U56 | DEG@1.00 rung 40 (2) | 13.40% / 1.1311 / −22.46% | 1.2663/1.0361 | 14.08% / 1.1150 / −22.46% | F | F | F |
| B136 | anchor CADENCE=W (61) | 16.18% / 1.0715 / −20.74% | 1.2902/0.8995 | 16.29% / 1.0240 / −20.74% | F | F | F |
| B136 | N=5 (57) | 18.73% / 0.9690 / −28.12% | 1.3074/0.7109 | 14.71% / 0.7546 / −28.12% | F | F | F |
| B136 | DEG@1.00 rung 5 (2) | 18.73% / 0.9690 / −28.12% | 1.3074/0.7109 | 14.71% / 0.7546 / −28.12% | F | F | F |
| SMALL | anchor CADENCE=W (61) | 7.84% / 0.5055 / −35.81% | 0.6594/0.3942 | 7.09% / 0.4534 / −35.81% | F | F | F |
| SMALL | H=252 (59) | 13.36% / 0.7845 / −37.41% | 0.9555/0.6419 | 11.16% / 0.6677 / −37.41% | F | F | F |

The two DEG@1.00 rows are the δ=1 identity: the synthetic ladder *is* the N ladder there, so the
pick and the book are the same as N's, to the last decimal (G2).

Benchmarks: U56 SPY 15.06% / 0.8815 / −33.72% (halves 0.9600/0.8171), OOS 15.15% / 0.8686;
U56 LIVE (RULES v2) 8.60% / 1.1982 / −12.05%, OOS 9.42% / 1.2717. B136 SPY 15.16% / 0.8862, OOS
0.8769; B136 LIVE 7.98% / 1.0994, OOS 1.1061. SMALL SPY 14.06% / 0.8582, OOS 0.8769; SMALL LIVE
4.64% / 0.7130, OOS 0.6518.

**BOTH KEEP PATHS.** 174 rung books (108 synthetic): **4a 0 of 174**, 4b full 53, 4b OOS 49, BOTH
48 — which collapse to **33 distinct books** (DEG@0.00's six U56 rungs are *literally the anchor*,
0.1571/1.1480/−0.1913, six times over). 360 stitched chooser curves: 4a 0, 4b 73, 4b OOS 49, BOTH
49. 360 rule-8 picks: **4a 0, 4b 55, 4b OOS 55, BOTH 55 — and all 55 are ONE book**, the U56
anchor the record confirmed on 2026-09-15 and 1206/1207/1214 all declined to promote. Under 1194's
gross-free key that is one book, not 55.

**NOT PROMOTED, NO MEMO, NO RULES CHANGE. This run produces no new book.** The synthetic ladder is
a measuring instrument, not a candidate: no RULES wording can name a blend weight, and the passing
DEG books are near-anchor mixtures by construction. The book *listing* does show U56 N=15
(17.07% / 1.1675 / −20.14%, OOS 18.87% / 1.1894) above the anchor, but that is a rung of the
record's own N ladder, not a decision, and no chooser in this run picks it out of sample.

## 7. Survivorship (rule 9)

B136 and SMALL are CURRENT constituents. SMALL is the sub-$2B screen, 664 investable of 715 after
dropping every ticker with `max_1d_move >= 1.0`, and starts 2010. U56 is the committed cache.

## 8. Gates (21 of 21) and what is reported rather than repaired

G0 MC d2(k) == Hartley 9.66e-04 · G1 R_k/d2(k) unbiased 8.56e-04 · G_A0 every bar form calls W
against a zero-spread ladder · G2 DEG(1.00) == the N ladder 0.0 · G3 the blend preserves gross
4.44e-16 · G4 fast runner == engine.backtest 2.78e-17 · G5 live U56 MaxDD −12.0549% == committed
−12.05% · G6 block-sum bootstrap == direct Sharpe 7.77e-15 · G7 folds tile all three panels ·
**G8 admitting a ladder never moves an EXISTING pair's call (0 mismatches over 5 bar forms)** ·
G9 the ALL4 pairs replay 1214's 252 rows 4.55e-13 · **G10 the degenerate-free control sets are
inert in δ (0)** · G11 the walk is monotone over δ ≤ 0.30 (0 exceptions) · G12 a δ-matched rung
reproduces GROSS's decisive rate 0.0040 · **G12b saturation: a second degenerate rung changes
nothing (0)** · G13 CH_ANCHOR move rate 0 · G14 stitched lengths == sums of folds · G15 null bands
deterministic (0.0).

**REPORTED, NOT REPAIRED (G11b = 2):** the synthetic ladder's IS spread rises with δ at 208 of 210
transitions. Both exceptions are the top step on U56 (2016: 1.1943 → 1.0000; 2019: 1.0696 →
1.0000), where a 30% blend is *wider* than the N ladder itself. There is no monotonicity theorem
for the Sharpe spread of a blended ladder, so the pre-declared pointwise claim was an over-claim
on my part; the gate now covers the degenerate region where every finding in this run lives, and
the two exceptions are named above rather than smoothed away.

## 9. What this leaves for the queue

1214 asked whether the bar was the object worth repairing and answered no. This run says the
**comparison set** is: a decisive widest-dial call is a joint property of the bar *and* the set,
and the record's set contains a member that is not a dial. Three follow-ups are filed, all
price-only: (a) census the record's committed widest-dial claims for whether their comparison set
contained a degenerate member; (b) test an eligibility bar on comparison-set membership (a ladder
must clear a minimum spread against its own null to be admitted) and price it; (c) price
H_RUNNERUP as the record's standing headline form, since it is the only one a degenerate member
cannot manufacture.
