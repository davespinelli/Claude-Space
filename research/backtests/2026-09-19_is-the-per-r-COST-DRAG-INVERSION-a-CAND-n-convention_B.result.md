# Idea 708 — is-the-per-r-COST-DRAG-INVERSION-a-record-wide-fact-or-a-CAND-n-convention
**lane B, 2026-09-19.** Script `2026-09-19_is-the-per-r-COST-DRAG-INVERSION-a-CAND-n-convention_B.py`;
artefacts `.console.txt .grid.csv .drag.csv .walkforward.csv .keeppaths.csv`. Runtime 210 s,
75 books, 375 published cells, gates **91/91**.

## Verdict — **IT IS A CONVENTION, AND IT IS NOT EVEN RECORD-WIDE AS A RAW FACT. KILL for capital, no new book, no RULES change.**

Idea 703's committed sentence — *"a CAND-20 book on a 400-name panel turns its whole NAV over far
more often than a CAND-200 one, so **holding more names is CHEAPER, not dearer**"* — survives as
arithmetic about a normaliser and dies as a statement about breadth. Both legs of the
pre-registered discriminator land on the same side, and a third, unplanned reading says the raw
claim does not even replicate with a stable sign.

## 1. The discriminator (pre-registered, bar stated before the run)

Every book's drag re-cut in three turnover currencies, Spearman against breadth n, meaned over
the three panels:

| family | rho(n, T_nav) | rho(n, T_slot) |
|---|---|---|
| CAND | **−0.9952** | **+0.9952** |
| MADIST | **−0.9952** | **+0.9952** |
| BAND | **−0.9952** | **+0.8216** |
| ADAPT | **−0.9804** | **+0.9804** |

**H_CONVENTION legs: rho(n, T_nav) < 0 in 4 of 4 and rho(n, T_slot) ≥ 0 in 4 of 4. H_GENERAL: 0 of 4.**
The reading is **H_CONVENTION** and it is unanimous. Per unit NAV a wide book looks far cheaper
(U56 CAND 23.67 → 8.20 ×/yr from n = 5 to ALL); measured in the currency the convention hides —
**NAME SLOTS replaced per year** — the same wide book churns **more than twice as much**
(157.7 → 408.7 on U56, 196 → 1006 on B136, 223 → 4152 on SMALL). Nothing about the book got
stabler; each replacement simply became a smaller share of NAV because GROSS/n shrank the slot.

**G8, and it matters for how the record reads its own tables.** T_nav and T_gross are
rank-identical on **12 of 12** count arms (max |Δrho| 0.000e+00): every count family re-spreads
the full gross over the names it holds, so `gbar` is a constant and "per unit deployed capital"
is not a second reading of anything. The record has two currencies, not three.

## 2. The arithmetic leg — the drag carries no information beyond turnover

Costs are exact in this engine (G1: reconstructed `r_c = r_0 − turnover·c/1e4` equals a fresh
`backtest(cost_bps=c)` at **0.000e+00** over 9 spot cells spanning three panels and three rungs),
so Sharpe drag has a closed form. Regressing the 75 measured drags on `(c/1e4)·T_nav/vol_0`:

    drag(10 bps) = +0.000167 + 0.999786 × (10/1e4)·T_nav/vol_0
    R² 0.999983    max |residual| 0.000735    mean |drag| 0.106382    Spearman 0.999516

**Slope 1.000, intercept 0.0002, R² 0.99998.** The "per-r cost drag" is `T_nav/vol` in different
units. It has no residual content, so any ordering of books by drag is an ordering by T_nav, and
the inversion restates — without residue — as *"T_nav falls with n"*, which is the GROSS/n
convention written down.

## 3. An unplanned finding: 703's raw claim is not sign-stable across panels

Drag vs breadth at 10 bps, rho(n, drag) by arm: U56 −0.81 / −0.75 / −0.81 / −0.94 and B136
−1.00 / −0.83 / −0.60 / −1.00 (CAND / MADIST / BAND / ADAPT) — but **SMALL runs +0.26 (CAND),
+0.43 (BAND), +0.60 (ADAPT)**. On the small-cap panel the drag *rises* from n = 5 to n = 40
(CAND +0.0810 → +0.1860) before falling. **3 of 12 arms carry the opposite sign.** 703 measured
its ladder on one panel; "monotone decreasing at every width" is a property of that panel, and
the record should stop quoting it unqualified. (703's own file already carries one correction of
this shape — its §1(a) deletes "monotonically" from a different ladder.)

## 4. Both KEEP paths at the binding 10 bps rung, all 75 books

**4a: 0 of 75** — another consecutive 4a zero (live RULES v2 on U56 8.62% / 1.2010 / −12.05%,
halves 1.2276 / 1.1805). **4b: 13 of 75** (U56 3, B136 10, SMALL 0); binding legs CAGR 34 < H2 38
< DD 39 < OOS 40 < H1 46. **Not one of the 13 is a new book:** they are the wide/ALL ends of BAND,
MADIST, CAND and ADAPT, i.e. idea 1454's "re-spread the gated-out weight" book (U56 BAND-ALL
12.19% / 1.1567 / −17.71%, OOS 1.1950) and its neighbours, already priced and already killed as a
dial by idea 1555 (RESPREAD loses to the SHY sleeve on Sharpe at 6 of 6 panel-frames and on MaxDD
at 6 of 6). **H_HINDSIGHT fires again:** all 13 clear 4b full *and* OOS and **none is reachable by
any chooser in this run**.

## 5. Rule 8 walk-forward (params on warm-up..2016 only; 2017–2026 read exactly once)

| panel | selector | pick | OOS CAGR | OOS Sharpe | OOS MaxDD | Δ vs LIVE | Δ vs SPY |
|---|---|---|---|---|---|---|---|
| U56 | C_SHARPE | BAND-5 | 23.56% | 1.0598 | −28.01% | −0.2168 | +0.1861 |
| U56 | C_DRAG | EWALL-ALL | 13.67% | 1.1266 | −22.53% | −0.1500 | +0.2529 |
| U56 | C_ANCHOR | LIVE | 9.46% | **1.2766** | −12.05% | 0.0000 | +0.4030 |
| B136 | C_SHARPE | BAND-5 | 25.76% | 1.0786 | −26.67% | −0.0231 | +0.2049 |
| B136 | C_DRAG | EWALL-ALL | 13.70% | 1.0870 | −25.37% | −0.0147 | +0.2133 |
| B136 | C_ANCHOR | LIVE | 7.85% | **1.1017** | −12.24% | 0.0000 | +0.2280 |
| SMALL | C_SHARPE | EWALL-ALL | 10.71% | 0.6828 | −35.11% | +0.0356 | −0.1908 |
| SMALL | C_DRAG | EWALL-ALL | 10.71% | 0.6828 | −35.11% | +0.0356 | −0.1908 |
| SMALL | C_ANCHOR | LIVE | 4.41% | 0.6472 | −12.48% | 0.0000 | −0.2265 |

**Mean Δ(OOS Sharpe) vs LIVE −0.0556, beating it 2 of 6; vs SPY +0.0793, beating it 4 of 6.**
**C_DRAG — "pick the cheapest book", the dial this idea is about, made into a real selector —
picks EWALL-ALL on 3 of 3 panels and loses to doing nothing on 2 of 3 (mean −0.0430).** Cheapness
is a real axis and it is not worth choosing on: the cheapest book in the grid is the one with no
selection in it at all.

## 6. A correction this run made to itself, logged rather than hidden

The per-slot currency was first written `T_nav / nbar`. That is wrong and wrong in the direction
that flatters H_GENERAL: a GROSS/n book already carries one factor of 1/n inside T_nav, so
dividing by nbar again divides by breadth twice and forces rho(n, ·) = −1 by construction. The
first pass printed rho(n, T_nav) == rho(n, T_gross) == rho(n, T_name) to four decimals on 12 of
12 arms — the signature of exactly that degeneracy — and read **H_GENERAL** off it. The corrected
quantity multiplies by the slot count (`T_nav · nbar / gbar`, name-slots replaced per year) and
the verdict **reversed to H_CONVENTION, 4 of 4 to 0 of 4**. Both the erroneous reading and the fix
are in the script docstring. A currency that moves a headline this far deserves a name in the
record, not a silent patch.

## 7. Gates (91/91)

G0 samples 17.7y / 17.7y / 15.6y (rule 1). G1 cost identity **0.000e+00** over 9 spot cells.
G2 this script's own band machinery replays `baseline.rules_v2_weights` at **0.0** on all three
panels. G3 ADAPT-ALL == CAND-ALL at **0.000e+00** (degenerate by construction, checked not
assumed). G4 exactly two tuned parameters (FAMILY, COST RUNG). G5 no chooser reads a row on or
after 2017-01-01. G6 gross in [0, 1] on all 75 books. G7 all 375 cells published. G8 T_nav /
T_gross rank-identical, max |Δrho| 0.000e+00.

## Survivorship (rule 9)

U56 / B136 / SMALL are CURRENT-constituent lists, so every absolute level is an upper bound. The
headline is a set of within-book turnover decompositions and a difference between two cost rungs
on the SAME book over the SAME days, so it is first-order immune; the 4a / 4b pass counts are not.

## What the record should say instead

> The cost drag of a GROSS/n book falls with n because the convention shrinks each slot to G/n,
> not because wide books churn less: measured in name-slots per year, breadth *raises* turnover
> monotonically on 4 of 4 families and 3 of 3 panels. Drag is `T_nav/vol` to R² 0.99998 and
> carries no information of its own. The sign of drag-vs-breadth is panel-dependent (3 of 12 arms
> run the other way on SMALL), so "holding more names is cheaper" should not be quoted unqualified.

**No RULES change.** RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py untouched.
No memo: this run produces no KEEP candidate.
