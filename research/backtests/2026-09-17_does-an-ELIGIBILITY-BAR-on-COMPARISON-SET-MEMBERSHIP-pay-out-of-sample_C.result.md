# Idea 1226 (lane C, 2026-09-17) — does an ELIGIBILITY BAR on COMPARISON-SET MEMBERSHIP pay out of sample?

**VERDICT: KILL (capital) / ANSWERED.** The repair 1223 proposed does not repair anything. It
either changes nothing (the cheap bar), or it empties the comparison set entirely (the honest
bar), and every penny it appears to buy is the do-nothing dial being turned by another name.

## The question

1223 found that admitting one perfectly degenerate rung makes the widest-dial chooser move at
0.881 of cells instead of 0.024, and that this costs **-0.0487** of mean OOS fold Sharpe. The
queue named the obvious repair: admit a ladder to the comparison set only if its own Sharpe
spread clears its own null band. This run builds that bar, walks its strictness, and re-prices
every chooser.

Two dials, 24 cells, all published: **ADMISSION BAR** {A_NONE, A_POS, A_MED, A_90, A_95, A_99}
x **COMPARISON SET** {NG, NG_D, ALL4, ALL4_D}. The null for each ladder is its own block
bootstrap (B = 63 rows, 800 reps, block starts shared across books so the market factor
survives) **recentred** so every rung has the same true Sharpe; the observed spread is read
against quantiles of that recentred range. 17 of 17 gates pass. Runtime 19s, offline,
deterministic.

## 1. NO LADDER THE RECORD OWNS CLEARS ITS OWN NULL BAND

Median observed IS spread against the median 95th percentile of its own recentred null, over
42 (panel, fold) cells:

| ladder | k | med R_obs | med q95 | **med R/q95** | A_POS | A_MED | A_90 | A_95 | A_99 |
|---|---|---|---|---|---|---|---|---|---|
| N | 6 | 0.1604 | 0.4133 | **0.3800** | 1.000 | 0.405 | 0.095 | 0.000 | 0.000 |
| H | 4 | 0.0944 | 0.3343 | **0.3285** | 1.000 | 0.262 | 0.000 | 0.000 | 0.000 |
| GROSS | 10 | 0.0018 | 0.0042 | **0.4347** | 1.000 | 0.714 | 0.143 | 0.071 | 0.024 |
| CADENCE | 2 | 0.0428 | 0.2372 | **0.1734** | 1.000 | 0.167 | 0.024 | 0.000 | 0.000 |
| DEG@0.00 | 6 | 0.0000 | 0.0000 | n/a | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |

**Every one of the record's four live ladders realises between 0.17 and 0.43 of its own 95th
percentile.** Mean admitted set size at A_95 is **0.000 (NG, NG_D) and 0.071 (ALL4, ALL4_D)**;
at A_99, 0.000 and 0.024. A bar strong enough to be worth calling a null test admits NOTHING on
this tape, so the chooser holds the anchor at 42 of 42 cells and the clause is a do-nothing rule
with extra machinery.

**AND THE BAR BACKFIRES ON THE CASE IT WAS BUILT FOR.** GROSS — the degenerate ladder whose
spread 1214 measured at 0.0011-0.0034 — has the **HIGHEST** R/q95 of the four (0.4347) and the
highest admission rate at every live bar (0.714 at A_MED, 0.143 at A_90, the only ladder still
admitted at A_95 and A_99). Its null band shrinks with its spread, so a ratio test cannot see
its degeneracy. The only thing the bar cleanly excludes is the PERFECTLY degenerate rung, whose
spread is exactly 0 (G3) — and **A_POS, the free bar `R_obs > 0`, already excludes that.**

## 2. WHAT THE BAR DOES TO THE HEADLINE CALL

Pairwise decisive rate at B_IID95, and the H_ANY headline rate:

| set | A_NONE | A_POS | A_MED | A_90 | A_95 | A_99 |
|---|---|---|---|---|---|---|
| NG decisive / H_ANY | 0.0397 / 0.119 | 0.0397 / 0.119 | 0.0625 / 0.024 | — / 0.000 | — / 0.000 | — / 0.000 |
| NG_D decisive / H_ANY | 0.5198 / **1.000** | 0.0397 / 0.119 | 0.0625 / 0.024 | — / 0.000 | — / 0.000 | — / 0.000 |
| ALL4 decisive / H_ANY | 0.5198 / **1.000** | 0.5198 / **1.000** | 0.5455 / 0.357 | — / 0.000 | — / 0.000 | — / 0.000 |
| ALL4_D decisive / H_ANY | 0.7119 / **1.000** | 0.5198 / **1.000** | 0.5455 / 0.357 | — / 0.000 | — / 0.000 | — / 0.000 |

A_POS collapses NG_D onto NG exactly (0.5198 -> 0.0397 decisive, H_ANY 1.000 -> 0.119) and
ALL4_D onto ALL4, which is 1223's damage undone in full at zero cost. It leaves ALL4 untouched,
because GROSS passes `R > 0`. Above A_POS the sets empty out and every rate goes to zero for the
uninteresting reason.

## 3. THE BAR DOES NOT PAY FOR ANY REASON EXCEPT MOVING LESS

Mean OOS fold Sharpe over 42 cells x 4 sets x 3 headline forms:

| bar | mean OOS Sharpe | d vs A_NONE | move rate (VALUE) | rule-8 mean | d vs A_NONE |
|---|---|---|---|---|---|
| A_NONE | 1.0061 | +0.0000 | 0.466 | 0.8634 | +0.0000 |
| A_POS | 1.0145 | +0.0084 | 0.329 | 0.8682 | +0.0048 |
| A_MED | 1.0322 | +0.0261 | 0.119 | 0.9202 | +0.0567 |
| A_90 / A_95 / A_99 | 1.0362 | +0.0301 | **0.000** | 0.8845 | +0.0210 |
| **DO NOTHING** | **1.0362** | | 0.000 | **0.8845** | |

The best bar's +0.0301 is **exactly** the anchor's number, because at A_90 and above the bar IS
the anchor. Monotone in strictness and terminating at doing nothing: the 1206/1221/1226/1227/1230
finding arriving a sixth time.

**THE COUNT-MATCHED NULL (1227's NL_PERM), which is the test that decides it.** Each moving
chooser's own destination multiset and own move count, re-dealt to randomly chosen folds, 4,000
reps. Over the 46 (set, bar, chooser) cells that move at all: the observed mean sits **ABOVE**
its own null at **6 of 46**, mean gap **-0.0388**, **0 cells at p < 0.05 against 2.3 expected by
chance**. Per bar: A_NONE -0.0529, A_POS -0.0426, A_MED -0.0201, A_90 -0.0132. The bar narrows
the loss monotonically and never reverses it — **the admission test does not select better moves,
it only makes fewer, and the moves it keeps are still on the wrong side of their own null.**

The one apparent exception, stated so it cannot be mistaken for a result: A_MED's rule-8 mean
(0.9202) beats doing nothing (0.8845), and **the entire gap is ONE pick** — SMALL / CH_RAW /
H=252, OOS Sharpe 0.6678 against SMALL's anchor 0.4534 — on the panel with the worst anchor, in
60 rows. Its own rolling-fold null puts it at p = 0.78.

## 4. RULE 8 AND BOTH KEEP PATHS

Every dial and every chooser chosen on the pre-2017 window only; 2017-2026 read once.
360 rule-8 rows, 360 stitched curves, 84 rung books (57 distinct on 1194's gross-free key).
1230's correction applied throughout: a move onto a book that IS the anchor bit for bit is a
no-op, and the KEY move rate overstates the VALUE rate by **0.0103** of pick-cells.

- **4a: 0 of 360 rule-8 rows, 0 of 360 stitched curves, 0 of 84 books.** The live RULES v2 book
  is low-return and shallow (U56 OOS 9.42% / 1.2717 / -12.05%); nothing here clears it.
- **4b: 99 of 360 rule-8 rows pass full AND OOS — and they collapse to ONE distinct book**, the
  frozen U56 anchor CADENCE=W: full 15.71% / 1.1480 / -19.13%, **OOS 17.16% / 1.1759 / -19.13%**
  against U56 SPY OOS 15.15% / 0.8686 / -33.72%. Stitched curves 104 full / 96 OOS / 96 both.
  On the 57 DISTINCT books: 4a 0, 4b full 14, 4b OOS 13, BOTH 12.
- **CONFIRMATORY, NOT GENERATIVE.** Every 4b pass is a book the record already committed,
  re-selected by a rule that declines to move. No new book, no memo owed, RULES.md untouched.

## 5. SURVIVORSHIP (rule 9)

B136 and SMALL are CURRENT constituents; SMALL is the sub-$2B screen with 51 of 715 tickers
dropped for max_1d_move >= 1.0 (664 names), SPY excluded from its eligible set. The bias does not
cancel out of the OOS levels or the 4b legs, so any pass there is an upper bound.

## 6. WHAT THE RECORD SHOULD TAKE FROM THIS

Not a PROTOCOL clause requiring a null-band admission test — it admits nothing, and where it does
admit it admits the degenerate ladder first. The defensible version is the free one: **a ladder
whose rungs are the same book is not a ladder**, which `R_obs > 0` settles at no cost and which
undoes 1223's entire manufactured-call effect (H_ANY 1.000 -> 0.119 on NG_D). Proposed for the
Sunday review (rule 6) as a schema check on comparison-set construction, never as a chooser.
The larger reading stands where the record has put it five times before: the comparison set is
not where the loss is, and no amount of cleaning it turns a chooser into a positive-expectancy
rule on this tape.
