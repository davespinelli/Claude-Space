# Idea 910 (lane C, 2026-09-15) — is there an EX-ANTE proxy for the DDWIN beta that is not CIRCULAR?

**ANSWERED = YES on agreement, NO on usefulness. Two ex-ante proxies reach DDWIN's agreement
exactly (U56/ROLL 0.9844, B136/SPYDD 1.0000, both with 0 disagreeing matched pairs) — and the one
that wins by a mile does so because on the large-cap panels 89–93% of books' own peak-to-trough
windows are *contained inside SPY's*, so it is reading DDWIN's own days. Measured in sample and
read once out of sample, every proxy misses the 0.95 bar (best 0.9375). KILL: the circularity is
relocated to the market, not removed.**

No RULES change, no PROTOCOL edit applied (rule 6). `RULES.md`, `PROTOCOL.md`, `scan.py`,
`bot.py` and `baseline.py` untouched.

**SELECTION.** Second Open idea in QUEUE.md (lane C's claim rule); 909 is lane A's. No EDGAR /
Form 4 / 8-K / options / live-data content, so eligible for the cloud sandbox.

## What was asked

Idea 867 killed "the 4b DD cap is a beta cap" for the three estimators you can compute ex ante
(FULL / DOWN / ROLL, agreement 0.679–0.983) but found one that *does* reach the bar — **DDWIN**,
beta measured inside the book's own peak-to-trough max-drawdown window: B136 agreement 0.983,
best-case 1.000, 0 of 109 matched pairs disagreeing — and dismissed it as circular. This run
searches for a forward-computable statistic that reaches the same agreement.

**EX ANTE is defined before any number is read:** a statistic qualifies iff its conditioning set
is a function of SPY's path and of the book's returns, but **never of the book's own equity-curve
extremum**. That is exactly the dependence 867 flagged. DDWIN is carried as the **ceiling**, never
as a candidate.

## Scale, dials, gates

336 real books + 48 controls on 3 panels × 4 families × 3 modes × 3 thetas × 4 gross rungs, each
scored on 3 windows with 11 beta readings on 2 populations = 1,152 book-windows and 198 agreement
cells, 10 bps, t+1, weekly. **TUNED 1** proxy {FULL, DOWN, ROLL, MAXROLL, EWMA, SEMI, TAIL10,
HIVOL, SPYDD, SPYDD10} + DDWIN as ceiling; **TUNED 2** panel {U56, B136, SMALL}. Every one of the
30 ex-ante grid points is reported below and in `.agree.csv` / `.barA.csv` / `.wfproxy.csv`.

**GATES 6 of 6 PASS.** G1 TREND/ROW at g=0.75 ≡ `baseline.rules_v2_weights`, max|dw| **0.000e+00**.
G2 fast `Book.at` ≡ `engine.backtest`, max|dr| **1.041e-17**, max|dturn| **2.429e-16**. G3 U56
committed triples — SPY 15.13%/0.8845/−33.72%, RULES v2 8.62%/1.2013/−12.05%. **G4 is the strong
one: idea 867's committed `.agree.csv` reproduces on all 12 rows, worst |Δagree| 1.11e-16, worst
|Δbest_agree| 1.11e-16, 0 n-mismatches** (β\* differs by up to 2.7e-02 because the maximising
threshold is an interval, not a point — the agreement it buys is identical, so β\* is excluded
from the gate by declaration). G5 determinism 0.000e+00. G6 the analytic ray: on `g × SPY` all
11 proxies read g, max|β−g| **1.6e-02** over 4 × 11 — this gates every implementation at once.

## H0 — the population control FAILS, in DDWIN's favour

867's DDWIN is read on n = 64 / 60 / 112 books against n = 112 for the others: DDWIN is undefined
whenever a book's peak-to-trough is under 20 days. So the run's first move was to re-read every
estimator on **DDSUB**, DDWIN's own population. The suspicion — that 0.983 is a selection effect —
is **wrong, and the honest decomposition runs the other way**:

| panel | DDWIN(DDSUB) − FULL(ALL) | = POPULATION | + ESTIMATOR |
|---|---|---|---|
| U56 | +0.0513 | **−0.0424** | **+0.0938** |
| B136 | +0.1262 | **−0.0571** | **+0.1833** |
| SMALL | +0.0536 | 0.0000 | +0.0536 |

FULL gets *worse* on DDSUB (0.9018→0.8594, 0.8571→0.8000), so DDWIN's edge over it is larger than
867 published, not smaller. There is a real estimator effect to proxy.

## H1 / H2 / H3 — BAR-A: 2 of 30 ex-ante cells QUALIFY

Pre-registered BAR-A (FULL window, DDSUB population, per panel): agree ≥ DDWIN's **and**
best_agree ≥ DDWIN's **and** 0 disagreeing matched pairs (|Δβ| ≤ 0.02).

| panel | DDWIN | best ex-ante | agree | best | pairs disagreeing | BAR-A |
|---|---|---|---|---|---|---|
| U56 (n=64) | 0.9531 / 0.9844 / 21 of 211 | **ROLL** | **0.9844** | **1.0000** | **0 of 146** | **QUALIFIES** |
| B136 (n=60) | 0.9833 / 1.0000 / 0 of 109 | **SPYDD** | **1.0000** | **1.0000** | **0 of 130** | **QUALIFIES** |
| SMALL (n=112) | 0.7321 / 0.8571 / 80 of 413 | MAXROLL | 0.8393 | 0.8482 | 57 of 400 | no |

And on the population a real rule would face (**ALL 112 books**, nothing dropped): U56 ROLL
**0.9286** vs FULL 0.9018; B136 **SPYDD 0.9732** vs FULL 0.8571; SMALL MAXROLL 0.8393 vs FULL
0.6786. SPYDD is defined on all 112 books, so unlike DDWIN it is a rule you could actually write.

**But no proxy wins twice.** ROLL is 0.9844 on U56 and 0.8667 on B136; SPYDD is 1.0000 on B136,
0.9844 on U56 and **0.6696 on SMALL — the worst of all ten**. There is no single ex-ante estimator
the record could adopt.

## The mechanism, and it is why the answer is really NO

The run measured, for every book, the **Jaccard overlap between its own peak-to-trough day-set and
SPY's** (`.overlap.csv`, 1,008 rows, reported, never tuned):

| panel | window | median Jaccard | share of books entirely INSIDE SPY's DD | SPY DD length |
|---|---|---|---|---|
| U56 | FULL | **0.854** | **0.929** | 24d |
| B136 | FULL | **0.708** | **0.893** | 24d |
| SMALL | FULL | 0.054 | **0.000** | 24d |
| U56 / B136 | IS | **0.000** | 0.286 / 0.357 | 28d |

On the large-cap panels 89–93% of books have their whole max-drawdown **contained inside SPY's own
24-day window**. SPYDD and DDWIN are therefore reading the *same days* for nine books in ten —
which is precisely why SPYDD reaches 1.000, and precisely why it collapses to 0.6696 on SMALL,
where that containment is **0 of 112**. The circularity is not removed. It is relocated from the
book's drawdown to the market's, and it survives only where the two coincide.

## H4 / RULE 8 (a) — every proxy FAILS out of sample, and the winner fails hardest

Beta measured on **2009–2016 only**, cap fitted on IS only, the OOS DD leg read **once**:

| panel | DDWIN_IS→OOS | FULL_IS→OOS | best ex-ante | bar 0.95 |
|---|---|---|---|---|
| U56 | 0.9000 (n=100) | 0.8482 | MAXROLL **0.9375** | MISSES |
| B136 | 0.8704 (n=108) | 0.8304 | ROLL **0.8750** | MISSES |
| SMALL | 0.8304 | 0.8839 | HIVOL **0.8929** | MISSES |

**0 of 30 ex-ante cells clear 0.95, and neither does DDWIN itself.** The IS→OOS persistence of the
beta reading names the culprit: every other proxy reads ρ(β_IS, β_OOS) between **+0.757 and
+0.993**, while **SPYDD reads +0.216 on U56 and +0.292 on B136** — the two lowest numbers in the
table, from the proxy that won BAR-A outright. Its IS window is the 2011 decline, its OOS window is
2020; it is not a book property at all, it is a date. That is the same defect as DDWIN, arriving by
a different road.

## Does the substitution reach 4b?

Books whose **whole 4b verdict** flips under `beta ≤ 0.60` (the DD leg differs *and* the other three
legs all pass), FULL window, against the actual pass count:

| panel | actual 4b | FULL | ROLL | SPYDD | MAXROLL | DDWIN |
|---|---|---|---|---|---|---|
| U56 | 9 of 112 | 9 | 7 | 8 | 9 | 2 of 64 |
| B136 | 10 of 112 | 6 | 8 | **3** | 10 | 0 of 60 |
| SMALL | 0 of 112 | 0 | 0 | 0 | 0 | 0 |

SPYDD's high agreement does cut B136's flips from 6 to 3, but 3 flips against 10 actual passes is
still a third of the shelf rewritten. Full 33 rows in `.flips.csv`.

## RULE 8 (b) — THE BOOKS, both KEEP paths, OOS read once

IS-only choosers on 2009–2016, OOS 2017–2026 read once, 10 bps, t+1, weekly.

| panel | chooser | book | OOS CAGR | Sharpe | MaxDD | H1/H2 | 4a | 4b |
|---|---|---|---|---|---|---|---|---|
| U56 | IS_SHARPE | TREND/AGG/th=0.2/g=1.00 | 16.41% | 1.075 | −29.18% | 1.184/0.955 | n | n |
| U56 | IS_DDCAP | TREND/AGG/th=0.2/g=0.75 | 12.30% | 1.076 | −22.53% | 1.186/0.953 | n | n |
| U56 | IS_PROXYCAP[ROLL@0.60] | TREND/AGG/th=0.2/g=0.50 | 8.18% | 1.076 | −15.46% | 1.189/0.951 | n | n |
| U56 | IS_PROXYCAP[ROLL@IScap] | TREND/AGG/th=0.2/g=0.75 | 12.30% | 1.076 | −22.53% | 1.186/0.953 | n | n |
| U56 | IS_DDWINCAP[circular] | TREND/AGG/th=0.2/g=0.50 | 8.18% | 1.076 | −15.46% | 1.189/0.951 | n | n |
| B136 | IS_SHARPE | TREND/AGG/th=0.2/g=1.00 | 15.85% | 1.058 | −25.59% | 1.231/0.873 | n | n |
| B136 | **IS_DDCAP** | **TREND/AGG/th=0.2/g=0.75** | **11.89%** | **1.060** | **−19.53%** | **1.235/0.873** | n | **y** |
| B136 | IS_PROXYCAP[ROLL@0.60] | TREND/AGG/th=0.2/g=0.50 | 7.91% | 1.061 | −13.25% | 1.239/0.872 | n | n |
| B136 | **IS_PROXYCAP[ROLL@IScap]** | **TREND/AGG/th=0.2/g=0.75** | **11.89%** | **1.060** | **−19.53%** | **1.235/0.873** | n | **y** |
| B136 | IS_DDWINCAP[circular] | TREND/AGG/th=0.2/g=0.50 | 7.91% | 1.061 | −13.25% | 1.239/0.872 | n | n |
| SMALL | IS_SHARPE | VOL/AGG/th=0.2/g=1.00 | 12.52% | 0.673 | −37.13% | 0.932/0.447 | n | n |
| SMALL | IS_DDCAP | VOL/AGG/th=0.2/g=0.25 | 3.43% | 0.679 | −10.45% | 0.954/0.441 | n | n |
| SMALL | IS_PROXYCAP[DOWN@0.60] | VOL/AGG/th=0.2/g=0.50 | 6.67% | 0.678 | −20.10% | 0.947/0.443 | n | n |
| SMALL | IS_PROXYCAP[DOWN@IScap] | VOL/AGG/th=0.2/g=0.25 | 3.43% | 0.679 | −10.45% | 0.954/0.441 | n | n |
| SMALL | IS_DDWINCAP[circular] | VOL/AGG/th=0.2/g=0.75 | 9.71% | 0.676 | −28.97% | 0.940/0.445 | n | n |

Comparands, same OOS window: **SPY 15.27%–15.33% / 0.874–0.877 / −33.72%** (halves 0.980/0.759–0.765);
**RULES v2 (live)** U56 9.46% / 1.277 / −12.05%, B136 7.88% / 1.106 / −12.24%, SMALL 4.47% / 0.652 /
−12.18%. **RULE 8 SUMMARY: 4a 0 of 15, 4b 2 of 15.**

**The two 4b passes are the same book reached twice, and it is not new.** B136 TREND/AGG/th=0.2/
g=0.75 clears 4b on FULL, IS *and* OOS (12.66% / 1.124 / −19.53% full sample) — but it is already
row 2 of idea 867's committed `.books.csv` at identical numbers. What is new is only that an
**IS-only chooser reaches it**, which 867 did not test. Its **DD margin is 0.70 pp** (−19.53%
against the −20.23% bar; 0.62 pp in sample), and idea 806's standing finding is that a margin that
thin is a date, not a book. A short memo is filed at
`2026-09-15_b136-trend-agg-th020-g075_4b_C_MEMO.md`; **it is NOT proposed** for the Sunday review.

## Verdict — KILL for the premise

An ex-ante proxy that *matches* DDWIN's agreement exists (two of them), so the queue's literal
question answers YES. It answers NO where it matters: neither proxy wins on more than one panel,
neither clears the 0.95 walk-forward bar, and the one that reaches 1.000 does it by reading the
market's drawdown window, which on U56/B136 contains 89–93% of the books' own — the same in-window
dependence 867 rejected, wearing the market's clothes instead of the book's. Its
ρ(β_IS, β_OOS) of **+0.216** is the proof: a statistic that does not survive a change of window
cannot be an ex-ante substitute for anything. **The DD leg still has no forward-computable beta
stand-in.**

## Survivorship

U56 / B136 / SMALL are current-constituent lists (SMALL additionally drops the 52 tickers with
`max_1d_move` ≥ 1.0 per `data/small_meta.csv`), so every CAGR and drawdown **level** above is
optimistic — the books' and the comparands' alike. The agreement rates, the Jaccard overlaps and
the IS→OOS persistences are same-tape comparisons between books on one panel and are unaffected.

## Follow-ups filed

912 (is the record's whole DD-leg literature a 2020-CONTAINMENT fact — re-run 867/910 on a panel
whose books' drawdowns do *not* sit inside SPY's), 913 (does a SPYDD-style market-episode beta
computed on a FIXED pre-registered episode set, rather than the window's own argmin, restore the
IS→OOS persistence SPYDD lacks), 914 (price the 0.70 pp DD margin of B136 TREND/AGG/th=0.2/g=0.75
against its own rebalance-offset spread, per idea 806's test).

Artifacts: `.console.txt` `.books.csv` (1,152 rows) `.agree.csv` (198) `.barA.csv` (30)
`.flips.csv` (33) `.overlap.csv` (1,008) `.wfproxy.csv` (33) `.walkforward.csv` (15)
`.gate867.csv` (12).
