# Idea 1065 (lane C, 2026-09-16) — does the MIN-HOLD DRAWDOWN TAX fall on the NAMES the SCORE WANTED TO DROP?

**ANSWERED = NO, NOT AS A CONCENTRATION CLAIM. The tax is an EXPOSURE fact, not a selection fact.
936's arithmetic survives; its sentence does not.** KILL of the concentration reading; CONFIRM,
restated, of the exposure reading. One 4b KEEP-candidate falls out of the rule-8 leg and is
REPORTED, NOT PROPOSED (rule 6, Sunday review). RULES.md, PROTOCOL.md, scan.py, bot.py and
baseline.py untouched.

## What was asked
936 found min hold raises a book's MaxDD by up to 7 pp while leaving the gross-matched null's
median MaxDD flat, and read the asymmetry as *"a selecting book's retained name is the one its own
score wanted to drop"*. This run attributes each book's drawdown to RETAINED-BY-CONSTRAINT names
against freely-held ones and asks whether the tax is concentrated in names whose rank had already
fallen out of the top N. Max 2 params (attribution rule, min hold).

## Two dials, all 12 points reported
`ATTRIBUTION RULE` in {`R_GATE` (fails the book's own 200d-MA / vol<0.60 gate), `R_TOP2N` (outside
today's free top-2N), `R_TOPN` (outside today's free top-N)} x `MIN HOLD H` in {5, 21, 63, 126}.
Nested by construction and gated (G6). Gross 0.75, 10 bps, N=20, three top-N mechanisms, four
rebalance grids and two panels are REPORTED axes, never selected. 408 book arms, 256 null arms.

## Gates: 7 of 8 pass
G1 runner == `engine.backtest` 2.08e-17. **G2 CROSS-RUN: idea 936's committed `.grid.csv` BOOK
rows, including its own W/H=63 tax cell, rebuilt here to 4.90e-07**; G3 its committed turnover to
4.27e-07 turns/yr. G4 the attribution is an IDENTITY — retained + free bucket contributions equal
the book's own gross return every day, max|resid| 1.39e-17. G6 the three rules are nested, 0
violations. G7 H=0 yields ZERO retained name-days, so the whole object is a min-hold object.
G8 SPY OOS 1.70e-04. **G5 FAILS at the 5e-4 tolerance this run declared**: live RULES v2 on U56
reads 0.0862/1.2007/-0.1205 against the committed 0.0861/1.1998/-0.1205, |d| 9.32e-04. The
committed triple is quoted to 4 dp and the panel has gained trading days since; 936's own cross-run
gate on this triple uses 5e-3, at which this passes. The tolerance was NOT widened after the fact —
the failure is published as declared.

## THE ANSWER (A2, A2b, A4)
Inside each book's own max-drawdown episode the retained bucket takes **its weight's share of the
loss and no more**. Median CONC (= loss share / weight share) over the 12 dial cells runs
**0.9071 .. 1.1358**, above 1 in **6 of 12** cells, and the share of individual books with CONC > 1
is 0.333 .. 0.636 — a coin flip. The gross-matched null's own CONC runs **0.9655 .. 1.1582**, and
the median (book − null) gap is **−0.0312**. Against the null's across-seed sd (0.137 .. 0.449) the
median book z is **−0.31**; 47.4% of books sit outside ±2 sd **in both directions**, i.e. the books
scatter wider than the null but are centred on it. There is no directional selection signal.

**What the tax IS, measured on the same 24-book cells:** `rho(tax_pp, retained WEIGHT share)` =
**+0.7519 / +0.5142 / +0.2658** (R_GATE / R_TOP2N / R_TOPN) against `rho(tax_pp, CONC)` +0.2128 /
+0.5350 / +0.3201. The retained bucket is **29.7% to 53.7% of invested weight during the episode**.
A book with a third to a half of its NAV frozen draws down more because it cannot de-risk, not
because the frozen names are individually worse than the ones it kept freely.

**Construction fact, stated not hidden:** the null has no eligibility gate, so `R_GATE` is inert
there and its null CONC is undefined (printed `nan`, not imputed). The null control therefore
exists for 8 of the 12 dial cells; the R_GATE column is a book-only reading.

## The causal / price leg (B) — releasing the flagged names
A SOFT min hold (keep a young name only while the score still wants it) **recovers essentially the
whole tax**: median recovery 0.998 .. 1.082 at every H >= 21, under all three rules. This confirms
the tax is the frozen bucket's — through exposure. What separates the rules is the rebate:

| rule | tax recovered (H=63) | rebate kept | turnover H0 -> hard -> soft | CAGR H0 -> hard -> soft | MaxDD H0 -> hard -> soft |
|---|---|---|---|---|---|
| R_GATE | 1.082 | **0.691** | 8.34 -> 3.72 -> 5.31 | 13.84% -> 15.58% -> 14.16% | −21.66% -> −26.65% -> −21.68% |
| R_TOP2N | 1.039 | 0.562 | 8.34 -> 3.72 -> 5.68 | 13.84% -> 15.58% -> 14.17% | −21.66% -> −26.65% -> −21.39% |
| R_TOPN | 1.000 | **0.000** | 8.34 -> 3.72 -> 8.34 | 13.84% -> 15.58% -> 13.85% | −21.66% -> −26.65% -> −21.66% |

**The narrowest rule is the one that pays.** `R_TOPN` — release anything today's ranking would not
pick — recovers the tax by becoming the H=0 book: it keeps 0.000 of the turnover rebate and buys
nothing. `R_GATE` — release only what fails the eligibility gate, 10.9% of held name-days — keeps
**69–77%** of the rebate and still gives the drawdown back. The price of that is the CAGR the hard
constraint was earning: −0.0197 of CAGR and −0.0283 of Sharpe at H=63, medians over 24 books.

## Both KEEP paths and rule 8 (C)
4a: **0 of 408 arms** clear the live RULES v2 book (H_4A PASS). 4b: BOOK_H0 8/24, BOOK_HARD 17/96
(0.177), **BOOK_SOFT 107/288 (0.372)** — against the null's unselected 4b base rate of **14/256 =
0.055**. Binding legs, counting failures: L_DD 261, L_H2 103, L_OOS 48, L_H1 10, L_CAGR 5.

RULE 8, arm chosen on IS (<= 2016-12-31) Sharpe ALONE per (panel, mech) from 68 candidates, OOS
read ONCE:

| panel | mech | pick | full CAGR/Sharpe/MaxDD | halves | OOS | 4b |
|---|---|---|---|---|---|---|
| U56 | CAND20 | **SOFT M/H126/R_TOP2N** | 14.36% / 1.1667 / −19.59% | 1.2631 / 1.0943 | 15.50% / 1.1863 / −19.59% | **True** |
| U56 | R3_84 | HARD W/H63 | 15.47% / 1.1251 / −25.81% | 1.3321 / 0.9842 | 15.73% / 1.0581 / −25.81% | False |
| U56 | MOMONLY | HARD W/H126 | 16.74% / 1.1911 / −20.58% | 1.3465 / 1.0795 | 17.37% / 1.1575 / −20.58% | False |
| B136 | CAND20 | HARD M/H21 | 16.78% / 1.1026 / −27.14% | 1.3662 / 0.8941 | 15.92% / 0.9998 / −27.14% | False |
| B136 | R3_84 | SOFT M/H21/R_TOP2N | 16.56% / 1.0996 / −26.83% | 1.3407 / 0.9106 | 15.81% / 1.0005 / −26.83% | False |
| B136 | MOMONLY | HARD D/H21 | 16.63% / 1.0769 / −25.91% | 1.3083 / 0.9013 | 15.95% / 0.9782 / −25.91% | False |

Benchmarks: SPY U56 full 15.10%/0.8829/−33.72% (halves 0.9588/0.8207), OOS 15.21%/0.8711/−33.72%;
RULES v2 full 8.62%/1.2007/−12.05%, OOS 9.45%/1.2762/−12.05%. **Picks beating RULES v2 on OOS
Sharpe: 0 of 6. Beating SPY: 6 of 6.** Five of the six 4b failures are on L_DD.

## Pre-registered hypotheses: 6 of 10 PASS
FAIL `H_CONC` (6 of 12 cells), `H_NULLFLAT` (the null's own CONC is not flat to ±0.05 — max|CONC−1|
0.1582, which is itself the resolution finding), `H_GAP` (−0.0312), `H_RESOLVE` (median z −0.31).
PASS `H_SOFT`, `H_REBATE`, `H_BOTH` (56 of 288 arms recover >=50% of the tax AND keep >=70% of the
rebate), `H_KEEP`, `H_WF`, `H_4A`.

`H_WF` / WF-A: the attribution verdict is the same in both windows — full-sample CONC 1.4588 (IS)
vs 1.4254 (OOS). Note the full-sample CONC is well above 1 while the drawdown-episode CONC is not:
over the whole tape the retained names earn MORE per unit of weight than the freely-held ones. That
is the same fact as 936's CAGR gain (13.84% -> 15.58% at W/H=63) and it cuts AGAINST the tax being
a bad-name story: the frozen names are, on average, the book's better holdings; they simply cannot
be sold when the tape turns.

## Limits, stated
- Current-constituent panels (U56, B136). Every LEVEL is optimistic. The headline statistics are
  within-book (a bucket against its own book) and book-against-its-own-null contrasts.
- The null's CONC resolution is ±0.14 to ±0.45 at 8 seeds; a true book effect smaller than that
  would not be visible here. The claim banked is one-sided: **no concentration is detectable at
  this resolution**, not that the concentration is exactly zero.
- The daily null's H=0 arm turns over ~240x/yr and pays ~24%/yr in costs, which is why the null's
  D-row "tax" reads −63 to −72 pp: raising H rescues a book the cost rung had destroyed. That row
  is a cost artefact and is not read as evidence either way (1059's finding, reproduced in passing).
- The 4b pass in the rule-8 table clears L_DD by 0.64 pp (−19.59% against the 0.60 x SPY cap of
  −20.23%). On the record's own SE work (1012/1042) a leg margin that size is not decidable on this
  tape half. It is reported as a candidate, not banked.

Script: `research/backtests/2026-09-16_does-the-MIN-HOLD-DRAWDOWN-TAX-fall-on-the-NAMES-the-SCORE-WANTED-TO-DROP_C.py`;
9 CSVs (`gates`, `arms`, `nullarms`, `attribution`, `nullattribution`, `dial`, `resolution`, `soft`,
`walkforward`, `hypotheses`) and a console log.
