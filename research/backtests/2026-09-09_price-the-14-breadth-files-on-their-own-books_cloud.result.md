# Idea 286 — price the 14 `breadth` files on their own books (cloud, 2026-09-09)

**ANSWERED. Two things, and the second is the one that matters.**

**(1) The census's 14 is really 7.** A semantic read of each headline block finds that 7 of
idea 276's 14 `breadth` files carry no cross-cap comparison explained by a panel property at
all — one of them (`does-every-regime-conditional-dial-lose-its-own-regime_C`) uses the word
`breadth` to name an *instrument* (`breadth20`, a breadth gate), which is a straight false
positive of a keyword census, and two of the "files" are `LEADERBOARD.md` and `CHANGELOG.md`,
which have no headline sentence to restate. **Of the 7 that are restatable, 2 survive the
restatement and 5 do not.**

**(2) `breadth` carries NOTHING once the cap mix q is beside it.** On 40 mixed panels
(k = 40 names, share q drawn from the sub-$2B panel) breadth interpolates smoothly from 0.681
at q=0 to 0.322 at q=1, Spearman(q, breadth) = **−0.980**, and every headline statistic moves
monotonically with q. But the *within-q* regression of each statistic on breadth — the only
question left once the collinearity is admitted — is **null on all three families**: pooled
correlation with breadth +0.54 / −0.51 / +0.53 collapses to within-q t = **+0.97 / −1.60 /
+0.11** (R² 0.012 / 0.033 / 0.000; N=80, p=5, dof 74, reported per idea 512's clause). **Every
`breadth` explanation in the record is a cap-mix explanation with a different name.**

No RULES change, no KEEP-candidate, no memo. `RULES.md`, `PROTOCOL.md`, `scan.py`, `bot.py`
and `baseline.py` untouched.

Script `2026-09-09_price-the-14-breadth-files-on-their-own-books_cloud.py`; console
`.console.txt`; CSVs `.audit.csv` (the hand-read of all 14), `.panels.csv` (43 panels with
breadth beside q), `.arms.csv` (602 arms), `.families.csv`, `.withinq.csv`, `.verdicts.csv`,
`.walkforward.csv`. Runtime 485 s, deterministic, no network.

---

## A. The audit — what the 14 files actually claim in their headline

| family | files | `breadth` in the headline |
|---|---|---|
| SIZE (a book-size effect across the cap line) | 2 | 1 |
| SHARE (a share-of-eligible book vs a fixed-n book) | 2 | 2 |
| SEL (where selectivity pays) | 1 | 1 |
| REV (Sharpe-vs-CAGR ordering reversal) | 2 | 2 |
| **NONE (no cross-cap panel-property headline)** | **7** | 4 |

The 7 with no restatable headline, and why: `insider-cluster-smallcap` (a Form 4 instrument,
and its headline attributes the result to signal quality and book size, not to a panel
property); `required-gross-as-a-leaderboard-column` (a column's rehabilitation rate over 378
books); `the-on-share-column` (on-share is a *book* property — share of days armed — and the
headline compares claims, not panels); `do-the-18-majority-reversing-files-have-reversing-
HEADLINES` (a claim about the record's sentences); `does-every-regime-conditional-dial-lose-
its-own-regime` (**`breadth20` names an instrument, not a panel** — a keyword false positive);
and `LEADERBOARD.md` / `CHANGELOG.md`, which idea 276's file-level census counted as files.

## B. The ladder — breadth beside q, the column idea 286 asks the record to publish

idea 276's MIX construction, rebuilt: k = 40 names, share q from the 439-name sub-$2B panel
and 1−q from the 100-name large-cap stock pool, 8 draws per rung, all panels run on one common
window so the rungs are comparable.

| q | breadth mean | min | max |
|---|---|---|---|
| 0.00 | 0.6807 | 0.6496 | 0.7005 |
| 0.25 | 0.6105 | 0.5755 | 0.6419 |
| 0.50 | 0.4944 | 0.4504 | 0.5300 |
| 0.75 | 0.4110 | 0.3645 | 0.4429 |
| 1.00 | 0.3220 | 0.3025 | 0.3428 |

named anchors: U56 0.6571, B136 0.6619, SMALL439 0.3224 — inside idea 276's published bands.
**Spearman(q, breadth) = −0.980.**

Family statistics, mean over the 8 draws per rung (both gross rungs; `.families.csv` has all
86 panel-by-gross points):

| q | breadth | D_size = S(top30)−S(top10) | share of draws > 0 | D_share = S(share m=0.5)−S(top20) | share < 0 | reversal |
|---|---|---|---|---|---|---|
| 0.00 | 0.681 | **+0.133** | 1.00 | −0.129 | 1.00 | 0.688 |
| 0.25 | 0.611 | +0.077 | 0.69 | −0.098 | 0.88 | 0.552 |
| 0.50 | 0.494 | +0.044 | 0.63 | −0.132 | 0.88 | 0.375 |
| 0.75 | 0.411 | +0.015 | 0.50 | −0.073 | 0.88 | 0.375 |
| 1.00 | 0.322 | **−0.010** | 0.50 | **+0.057** | 0.25 | 0.250 |

Selectivity argmax (gross 0.75, the rung idea 155 used): mean 0.988 at q=0 falling to 0.662 at
q=1. The named anchors reproduce idea 155's published reading closely — **U56 0.90 (published
0.90), B136 0.90 (published 0.95)**, small panel 0.50 — which is the reproduction check for
this family.

### Does breadth carry anything once q is controlled?

| statistic | pooled corr with breadth | N | p | dof naive | dof correct | slope | R² | t naive | t correct |
|---|---|---|---|---|---|---|---|---|---|
| D_size | +0.537 | 80 | 5 | 78 | 74 | +0.371 | 0.012 | +0.97 | +0.94 |
| D_share | −0.512 | 80 | 5 | 78 | 74 | −0.696 | 0.033 | −1.64 | −1.60 |
| reversal | +0.534 | 80 | 5 | 78 | 74 | +0.123 | 0.000 | +0.11 | +0.10 |

**Nothing survives.** A pooled correlation of ±0.5 with breadth is entirely the cap line; at
fixed cap mix, the draw-to-draw variation in breadth (a range of 0.05 within each rung)
predicts none of the three statistics.

## C. Headline survival — 2 of 7

| file | claim as its headline states it | on the ladder | verdict |
|---|---|---|---|
| `is-the-book-size-floor-a-corpus-wide-clause_C` (209) | size effect positive on large caps, non-positive on small | D_size +0.132 at q=0, −0.010 at q=1 | **SURVIVES** |
| `where-selectivity-and-cost-cross_B` (155) | the Sharpe-premium argmax is 0.90–1.00 on large caps, lower on small | 0.988 at q=0, 0.662 at q=1 | **SURVIVES** |
| `the-screen-is-a-book-size-rule_cloud` (199) | the size floor fires on **both** sides of the cap line | D_size −0.010 at q=1, positive in only 4 of 8 draws | FAILS |
| `time-varying-share-vs-fixed-n_B` (157) | fixed n beats the time-varying share count at every rung | reverses at q=1: D_share **+0.057**, negative in only 2 of 8 draws | FAILS |
| `does-book-share-price-a-tilt_C` (153) | a share book is a faithful restatement of a fixed-n book | \|D_share\| reaches 0.132 Sharpe | FAILS |
| `is-the-sharpe-cagr-reversal-a-PANEL-property_C` (271) | small-cap panels never reverse, large-cap panels usually do | 0.688 at q=0 but **0.250, not 0**, at q=1 | FAILS |
| `is-the-reversal-share-a-function-of-n-over-n_elig_C` (269C) | reversal share is NOT a monotone function of the eligible-share ratio | it is monotone in q: 0.688, 0.552, 0.375, 0.375, 0.250 | FAILS |

**Two things the failures do and do not mean.** They are restatements on a *matched-k = 40*
cap-mix ladder with this run's own arm set, not re-runs of the source files' books, so a FAILS
row says the headline's direction does not generalise off its own panel pair — not that the
published number was wrong. And two of the five failures are informative in the same way:
idea 271's "never reverse" holds exactly (**0.000**) on the named 439-name SMALL panel and
fails at 0.250 on an all-small 40-name panel, so that headline is a statement about panel
SIZE as much as about capitalisation; idea 269C's non-monotonicity was measured at matched
ratio across five heterogeneous panels, and on a ladder where only the cap mix moves the
reversal share is cleanly monotone.

## D. PROTOCOL — rule 8 and both KEEP paths

Arm chosen on the first half by IS Sharpe, second half read once, on all 43 panels:

| panels | OOS Sharpe (median) | OOS CAGR | OOS MaxDD | mean arm | RULES v2 | SPY |
|---|---|---|---|---|---|---|
| 40 mixed | 0.7152 | 9.80% | −28.22% | 0.6948 | 0.7981 | 0.8577 |
| 3 named | 0.9202 | 10.12% | −18.36% | 0.8390 | 0.9861 | 0.8340 |

The IS-chosen arm beats its own panel's mean arm OOS on 27 of 43 panels, the live RULES v2 on
**5 of 43**, and SPY on 14 of 43 — the record's standing "selection loses" reading, again.

**Both KEEP paths over all 602 arms: 4a 0/602, 4b 36/602.** Every 4b pass sits at q ≤ 0.25
(mixed panels: 16 at q=0, 14 at q=0.25, **0** at q ≥ 0.50; plus 6 on the named large-cap
anchors and 0 on SMALL439) — a by-product bearing directly on open idea 285: the
4b footprint is monotone in cap mix and disappears once a book is half small-cap. The best
passer (MIX q=0 d4, top30, gross 0.75: 11.54% / 1.1590 / −16.10%) is a 40-name random
sub-panel of the large-cap pool and sits inside the random-draw 4b base rate idea 486 priced,
so it is **not** a candidate. **No KEEP.**

## Caveats

* The audit is a hand-read of each headline block, committed verbatim in `.audit.csv` with the
  quoted sentence and the reason, so the classification can be checked rather than believed.
* The restated statistics are this run's own arm set on k=40 panels, not the source files'
  books; see the note under section C.
* SURVIVORSHIP: the sub-$2B panel and B136 are CURRENT constituents of their screens, and every
  mixed panel inherits that bias on its small-cap side, so no LEVEL comparison across q is a
  tradable statement. The object under test is the ORDERING of a dial's effect along q, which
  survivorship moves only through the level of the eligible share. The small panel drops 44
  tickers with `max_1d_move >= 1.0` per `data/small_meta.csv`.
* Two tuned parameters only: book size n and gross g. The per-family dials (m = 0.50, the
  selectivity grid) are fixed at the values the source files published and were not searched.
