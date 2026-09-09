# Idea 286 — price-the-14-breadth-files-on-their-own-books (lane B, 2026-09-09)

**VERDICT: ANSWERED / KILL. 0 of the 14 headlines survive the restatement — and the reason is
worse for the census than for the files.** Of idea 276's "tight lower bound of 14", **2 are the
record's own ledgers** (LEADERBOARD.md, CHANGELOG.md — no headline to restate, and they carry
218 of the 246 `breadth` occurrences by themselves), and of the remaining 12 headline files
**exactly 1 puts `breadth` in its own headline block at all**; the other 11 use the word only in
the body, or in the INSTRUMENT sense (a market-breadth timing series, not a panel property).
Re-run on the cap-mix ladder, **all 5 headline statistics the 7 re-runnable files rest on are
RESTATED as cap-mix (q) claims** — every one reproduces the record's published panel ordering
and every one loses its breadth association once q is held. No KEEP candidate, no memo, no
RULES change. `RULES.md`, `PROTOCOL.md`, `scan.py`, `bot.py`, `baseline.py` untouched.

Script: `2026-09-09_price-the-14-breadth-files-on-their-own-books_B.py` (639 backtests, 426
book cells, seed 2026). Outputs `.console.txt`, `.panels.csv`, `.books.csv`, `.audit.csv`,
`.files.csv`, `.stats.csv`, `.walkforward.csv`.
Two tuned parameters: **q** (11 levels) and **n** (6 book sizes) — all 66 × 6 = 396 mix cells
and 30 named cells reported. Weekly, t+1, 10 bps, 75% gross, RULES v1 gate — the record's
conventions, not selected on.

---

## 0. Gates, asserted before any new number was read

Idea 276's script is **imported, never re-typed**: its panels, its breadth definition, its
census regexes and its book construction all execute their own committed code.

| gate | what | result |
|---|---|---|
| **G0** | committed `.panels.csv` breadth rebuilt from source, all 71 panels | **70/71 at 0.000e+00**; `breadth_IS` exact (5.551e-17) on **71/71** |
| G0 mover | the one panel that moves | **U56 only, 1.666e-05** (`breadth_OOS` 2.192e-05) |
| **G1** | idea 276's own `census()` re-run: the frozen 14 | **14/14 re-flagged**, **0 flag flips** on the 292 files common to both censuses |
| **G2a** | committed `.books.csv`, the **132 MIX cells** | **2.220e-16** over CAGR/Sharpe/MaxDD/H1/H2/OOS/IS/v2/SPY |
| **G2b** | the 10 NAMED cells | max 6.037e-03 (H2), **all of it on U56**; **4a flips 0/142, 4b flips 0/142** |

**The U56 residual is idea 513's finding reproduced independently and by accident.** `data/prices.csv`
is the one price file the daily close job restates; U56 is the one panel served by it. Every
panel drawn from `prices_small.csv` / `prices_broad.csv` reproduces at machine precision at
*every* window, and the IS window (≤2016) is exact everywhere including U56. The residual is
**larger than idea 515's proposed 1e-3 Sharpe tolerance** (6.0e-03 on a half-Sharpe) and is
reported as such rather than absorbed — while moving **0 of 142 verdicts**.

## 1. LEG A — the census counts the WORD, not the CLAIM

Pre-registered, mechanical: a file's HEADLINE BLOCK is the text before its first `## `. Every
`breadth` occurrence is classified from a ±70-char window as INSTRUMENT (`breadth20`, "breadth
gate/signal/overlay" — a market-wide timing series), PANEL-PROPERTY, or OTHER.

**LEDGERS.** `LEADERBOARD.md` and `CHANGELOG.md` have no `## ` structure and make no headline
claim of their own. They are 2 of the 14 and carry **218 of the 246** occurrences.

| role × location, the 12 HEADLINE files (28 occurrences) | HEADLINE | body |
|---|---|---|
| PANEL-PROPERTY | **1** | 18 |
| INSTRUMENT | 1 | 3 |
| OTHER | 0 | 5 |

**1 of 12 files is a HEADLINE-BREADTH file** (`2026-09-06_where-selectivity-and-cost-cross_B`).
Ten have zero headline hits; one (`does-every-regime-conditional-dial-lose-its-own-regime_C`)
has a headline hit that is `breadth20`, **a timing instrument, not a panel property** — the
census's own PROP regex matches `\bbreadth\b` and cannot tell the two apart.

So idea 276's "tight lower bound" is not tight in the direction it claimed: **as a count of
published headline claims attributing a result to breadth-the-panel-property, 14 overstates by
14×.** The upper bound of 26 is unaffected — it was always an upper bound.

## 2. LEG B — the queue's literal ask: q beside breadth

| panel | k | **q** | breadth | breadth IS | breadth OOS |
|---|---|---|---|---|---|
| U56 | 55 | **0.00** | 0.6571 | 0.6583 | 0.6838 |
| B136 | 135 | **0.00** | 0.6619 | 0.6811 | 0.6783 |
| BSTK100 | 100 | **0.00** | 0.6617 | 0.6878 | 0.6754 |
| ETF36 | 35 | **0.00** | 0.6624 | 0.6619 | 0.6864 |
| SMALL439 | 439 | **1.00** | 0.3224 | 0.2727 | 0.3328 |

**Every named panel in the record sits at q ∈ {0, 1}.** There is no interior point anywhere in
the published corpus, so **no published breadth comparison has any within-stratum content at
all**: 13 of the 14 files straddle the whole cap line (Δq = 1.00) and the fourteenth
(`insider-cluster-smallcap`) names one panel and makes no cross-panel comparison.

## 3. LEG C — the re-run: each headline statistic with q held

Idea 276's ladder rebuilt name-for-name (k = 40, share q from SMALL439 and 1−q from BSTK100,
q ∈ {0.0…1.0}, 6 seeded draws = 66 panels). `Spearman(q, breadth) = −0.9759`; **total sd(breadth)
0.1198 against a mean within-q sd of 0.0226 — 3.6% of breadth's variance is free of the cap
mix, and that 3.6% is the entire room a breadth statement has.**

**The ladder reproduces the record's own published orderings, on the named panels, before any
control is applied** — so this is not a re-run that fails to find the effect:

- idea 209 "ρ(n, OOS Sharpe) positive on LARGE, negative on SMALL": U56 **+1.000**, B136
  **+1.000**, BSTK100 +0.943, ETF36 +0.829, SMALL439 **−0.086** — **sign split reproduced.**
- idea 153 "INV-vs-NONE overlap at matched n=20: u56 > broad > small" (published
  0.694/0.425/0.269, spread 0.425): here 0.798/0.576/0.401, spread **0.397** — **ordering reproduced.**
- idea 271 "small-cap panels never reverse, large-cap panels usually do": SMALL439 **0.133** vs
  large 0.867–1.000 — **split reproduced.**

| statistic (file) | ρ(breadth,S) | ρ(q,S) | partial (breadth\|q) | **within-q mean** | sign in | verdict |
|---|---|---|---|---|---|---|
| S1 ρ(n,OOS Sharpe) — 209, 199 | +0.629 | −0.623 | +0.124 | **−0.087** | 5/11 | **RESTATED** |
| S2 INV-vs-NONE overlap — 153 | −0.957 | +0.929 | −0.623 | **−0.470** | 2/11 | **RESTATED (sign reversal)** |
| S3 reversal share — 271, 269C | +0.614 | −0.640 | −0.059 | **−0.113** | 6/11 | **RESTATED** |
| S4 argmax-n premium — 155 | +0.607 | −0.609 | +0.078 | **−0.083** | 4/11 | **RESTATED** |
| S5 fixed-n − adaptive — 157 | +0.285 | −0.278 | +0.069 | **+0.133** | 6/11 | **RESTATED** |

Bar, pre-registered before any statistic was read: survive iff the within-q mean Spearman
carries the published sign with |mean| ≥ 0.30 **and** that sign holds in ≥ 8 of 11 q levels.
**0 of 5 survive. Four collapse to |within-q| ≤ 0.13. One (S2) clears the magnitude bar and
carries the OPPOSITE sign — a reversal, not a null.**

**Why S2 reverses, and the limit it marks.** breadth ≡ mean(n_elig)/k, so on a ladder that
fixes k = 40 breadth and panel width are the same number (`Spearman(breadth, Ebar) = +0.99999`,
max |40·breadth − Ebar| = 0.34) — a fixed-k ladder **cannot** separate breadth from width, only
both of them from the cap mix, which is what the queue asked. But the record's panels vary k by
8× and their width runs the **opposite** way: on the ladder Ebar falls 27.3 → 12.3 as q goes
0 → 1, while in the record it *rises* 36.1 (U56) → 141.5 (SMALL439). Idea 153's overlap
statistic is a function of n/n_elig, so its published cross-panel ordering is a **panel-SIZE**
result, and it reverses the moment size is held. Idea 209's sign flip is likewise **continuous
in q — first crossing zero at q = 0.4**, not at a sub-$2B boundary.

## 4. KEEP paths — 426 book cells, all reported

**4a 1/426. 4b 36/426.** Every mix-cell 4b pass sits at **q ≤ 0.5**, reproducing idea 276's
result at 3× the book-size resolution: 4b eligibility is itself a monotone function of the cap
mix. Named passes: U56 n=15/20/30 (n=20: 12.7%/1.097/−18.1%, OOS 1.167), B136 n=40, BSTK100
n=30/40. SPY on the common calendar 14.1%/0.862/−33.7%. Nothing beats the live book: the single
4a pass is one CAND-40 mix cell.

## 5. Rule 8 walk-forward — panel chosen on 2010–2016, 2017–2026 read once

| selector | OOS CAGR | OOS Sharpe | OOS MaxDD | anchor | edge | regret | SPY OOS | RULES v2 OOS |
|---|---|---|---|---|---|---|---|---|
| BREADTH-MAX (IS breadth) | 11.00% | **0.9845** | −19.13% | 0.6553 | +0.329 | −0.161 | 0.8820 | 1.0988 |
| Q-MIN (cap mix) | 10.07% | 0.8740 | −19.77% | 0.6553 | +0.219 | −0.272 | 0.8820 | 1.0115 |
| IS-SHARPE-MAX | 9.31% | 0.8425 | −19.11% | 0.6553 | +0.187 | −0.303 | 0.8820 | 0.9649 |

BREADTH-MAX beats Q-MIN on OOS Sharpe **6/6** book sizes and SPY **5/6** — and **this run
corrects that reading itself.** Both selectors land on q = 0.0; BREADTH-MAX is a draw-level
tie-break *inside* one stratum. Run over all 11 strata × 6 draws instead of one argmax, the
within-q Spearman(IS breadth, OOS Sharpe) is **−0.197, negative in 6 of 6 book sizes**: inside a
cap stratum, higher IS breadth goes with **lower** OOS Sharpe. The 6/6 argmax win is one lucky
draw. Nothing here is promotable, and BREADTH-MAX loses to RULES v2 on the same panel **0/6**.

## 6. Survivorship

SMALL439 and BSTK100 are **current constituents** of their screens; every small-cap level is
biased upward by an unknown amount. The bias reaches the ladder's *ordering* only through the
level of the eligible share, and the within-q test compares panels drawn from the **same two
source pools**, so the confound is common to both sides of it. The direction of the bias
(small-cap levels flattered) runs *against* the cap-mix reading, making the restatement the
conservative call.

## 7. What to do with it (Sunday review, not adopted here)

1. **The census's `breadth` column is a keyword count and should not be quoted as a claim
   count.** A one-line fix: the PROP regex must exclude `breadth\d+` and "breadth gate/signal",
   which are timing instruments, and should be scored on the headline block, not the whole file.
2. **The record has no interior cap mix.** Any future cross-panel claim should publish its
   panels' q beside the property it names; a claim comparing q = 0 with q = 1 panels is a
   cap-mix claim until shown otherwise.
3. **breadth ≡ n_elig/k.** On panels of different k it is not separable from panel width, and
   the record's two ends differ in width by 8× in the direction opposite the ladder's — which
   is enough to reverse a published ordering's sign, as S2 shows.

## 8. Collision with the cloud lane — an unplanned independent replication

Idea 286 was claimed and run **concurrently** by the cloud lane
(`..._cloud.py`, pushed first) and by this one (`..._B.py`, pushed second). Neither run saw the
other. Both are kept, because the pair is more informative than either.

**Where they agree — everything mechanical.** The 14 is really 12 headline files plus 2
ledgers; `does-every-regime-conditional-dial-lose-its-own-regime_C`'s headline `breadth` is
`breadth20`, a timing instrument and a straight false positive of the keyword census; breadth
interpolates smoothly in q (cloud 0.681 → 0.322, this run 0.6753 → 0.3045) with
`Spearman(q, breadth) = −0.980` / **−0.9759**; and the **within-q association is null** —
cloud reports t = +0.97 / −1.60 / +0.11 with R² ≤ 0.033 on three families, this run reports
within-q Spearman −0.087 / −0.470 / −0.113 / −0.083 / +0.133 on five statistics, 0 of 5 clearing
a pre-registered bar. Both find `4b = 36` passes and no KEEP.

**Where they differ — only in what "survive" is asked to mean.** The cloud lane asks whether
each file's literal claim still *reads true* on the ladder (2 of 7 survive: idea 209's size
effect is still positive at q=0 and non-positive at q=1; idea 155's argmax still sits higher on
the large-cap end). This run asks whether the claim still tracks **breadth** once q is held
(0 of 7 survive). Those two answers are the same fact stated twice: **the claims that "survive"
survive as functions of the cap mix.** Idea 209's flip is real and this run measures it
continuously — S1 runs +0.76 at q=0 to −0.62 at q=1, crossing zero at q = 0.4. Read the pair
as: *2 of 7 published claims remain true, 0 of 7 remain breadth claims.*

This run additionally holds the ladder's k fixed and reports the k-identity above, which the
cloud run does not, and which is what makes idea 153's overlap ordering reverse rather than
merely weaken.

By-product for the queue: idea 276's census machinery is now known to over-count by an order of
magnitude on its tightest column. The same regex family produced the 26-file upper bound and
the 136-file cross-cap count; both deserve the headline-block restatement before being cited.
