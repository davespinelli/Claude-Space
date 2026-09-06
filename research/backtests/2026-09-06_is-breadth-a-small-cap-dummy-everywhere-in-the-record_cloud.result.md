# Idea 276 — is-breadth-a-small-cap-dummy-everywhere-in-the-record (2026-09-06, cloud)

**Verdict: ANSWERED / KILL of `breadth` as an independent panel property.** No KEEP candidate.

Idea 271 reported `breadth` (share of a panel RULES v1's gate admits, averaged over weekly
rebalance days) as perfectly BIMODAL over 53 panels — SMALL439-derived 0.307–0.329, every
large-cap panel 0.619–0.745, no overlap — and noted `breadth<0.5` was arithmetically identical
to `source==SMALL439` there. This run tests whether that bimodality is a property of breadth or
of the record's sampling, and censuses how much of the corpus is exposed.

## Q1 — the bimodality is a SAMPLING artefact. Breadth is continuous in capitalisation mix.

Mixed panels, k=40 names, share q drawn from SMALL439 and (1−q) from BSTK100 (stock-vs-stock,
so the axis is capitalisation, not asset class), q ∈ {0.0,…,1.0}, 6 seeded draws each = 66 panels,
all reported.

| q | 0.0 | 0.1 | 0.2 | 0.3 | 0.4 | 0.5 | 0.6 | 0.7 | 0.8 | 0.9 | 1.0 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| breadth (mean) | 0.6753 | 0.6221 | 0.6331 | 0.5689 | 0.5188 | 0.4985 | 0.4451 | 0.4076 | 0.3894 | 0.3574 | 0.3045 |
| min–max | .652–.698 | .601–.638 | .615–.650 | .539–.596 | .482–.548 | .467–.567 | .414–.477 | .373–.435 | .336–.427 | .340–.381 | .286–.325 |

- Spearman(q, breadth) **−0.9759**, Pearson −0.9770, **R² linear in q = 0.9546**.
- **45 of 66** mixed panels land INSIDE idea 271's "empty gap" (0.329, 0.619). The gap is filled;
  the sweep spans 0.286–0.698 continuously. Nothing about breadth is two-clustered — the record
  only ever sampled q≈0 and q≈1.
- Monotone in q at every step except 0.1→0.2 (+0.011, inside the draw spread), i.e. one noisy rung
  in a strictly decreasing curve.
- `breadth<0.5` is crossed at **q ≥ 0.5**: idea 271's threshold is the 50/50 cap-mix line.
- Named panels reproduce 271: U56 0.6571, B136 0.6619, BSTK100 0.6617, ETF36 0.6624, SMALL439 0.3224.

**Breadth carries nothing beyond the cap mix.** Over the 132 mix book cells, Spearman with OOS
Sharpe is q −0.7827 / breadth +0.7475 (n=10) and q −0.8737 / breadth +0.8340 (n=20), while
Spearman(q, breadth) = −0.9759. Breadth is a strictly *noisier* proxy for the same one thing.

Breadth is stable out of sample (IS/OOS rank agreement over the 66 panels Spearman **+0.9841**) —
it is a reliable measurement, just of capitalisation, not of anything a book can exploit.

## Books — CAND-n (RULES v1 gate, top-n EW @75% gross, weekly, 10 bps, next-day), 142 cells, all reported

Mean of 6 draws per q; SPY on the common calendar 14.1% / 0.862 / −33.7%.

| n=20 | q=0.0 | 0.2 | 0.4 | 0.6 | 0.8 | 1.0 |
|---|---|---|---|---|---|---|
| CAGR | 11.2% | 10.4% | 9.5% | 6.7% | 4.1% | 1.9% |
| Sharpe | 0.995 | 0.949 | 0.895 | 0.693 | 0.469 | 0.239 |
| MaxDD | −19.0% | −18.1% | −16.7% | −17.1% | −21.0% | −26.1% |
| OOS Sharpe | 0.998 | 0.941 | 0.857 | 0.673 | 0.380 | 0.139 |

Named panels (n=20): U56 12.7%/1.098/−18.1% (H1 1.097 / H2 1.104, OOS 1.168) — **4b PASS**, the only
one, reproducing idea 2's candidate; B136 13.1%/0.959/−20.1%; BSTK100 13.9%/1.003/−20.4%;
ETF36 6.6%/0.805/−15.2%; SMALL439 6.7%/0.472/−27.4%.

**KEEP paths.** 4a **0/66** at n=10 and **0/66** at n=20 (RULES v2 is not beaten anywhere).
4b **3/66** (n=10) and **16/66** (n=20), and every pass sits at q ≤ 0.5 — 4b eligibility is itself
a monotone function of the cap mix, so no new rule is produced here, only the known large-cap result.

## Rule 8 walk-forward (choose q on 2010–2016, evaluate 2017–2026 untouched)

| n | IS argmax q | IS Sharpe | OOS Sharpe | do-nothing anchor (mean over q) | edge | best OOS q | regret | SPY OOS | RULES v2 OOS |
|---|---|---|---|---|---|---|---|---|---|
| 10 | 0.0 | 1.007 | 0.899 | 0.653 | **+0.246** | 0.0 (0.899) | **0.000** | 0.882 | 0.833 |
| 20 | 0.0 | 0.990 | 0.998 | 0.688 | **+0.310** | 0.1 (1.000) | **−0.002** | 0.882 | 0.833 |

The cap-mix dial does walk forward (regret ≈ 0, beats the anchor and SPY at both n) — but the answer
it transfers is "hold the large-cap panel", which is not new and is not a breadth statement.

## Q2 — census of the published record

292 markdown files (backtest results/memos + LEADERBOARD + CHANGELOG):

- name a small-cap panel **140**; name a large-cap panel/universe **266**
- **CROSS-CAP (both sides named): 136 = 46.6% of the corpus**
- of those, comparison language: **126**
- of those, attributing to a panel PROPERTY (breadth / dispersion / correlation / eligible-set vol):
  **26** — the files exposed to this collinearity
- of those, naming `breadth` explicitly: **14**

LEADERBOARD row level: 2,543 rows, **92 cross-cap (3.6%)**, 6 of those carrying a panel-property word.

So the exposure is bounded: **26 files upper bound, 14 tight lower bound** — not the ~136 files that
merely mention both tiers. Nearly half the corpus compares across the capitalisation line, but only
a tenth of that half explains a result with a panel statistic that is collinear with the line.

**Census caveat:** keyword census, not semantic. It counts files naming panels on both sides of the
cap line AND using a panel-property word; it does not verify each file's headline claim is the
collinear one. Read 26 as an upper bound and the 14 `breadth` files as the tight lower bound.

## Survivorship caveat

SMALL439 and B136/BSTK100 are CURRENT constituents of their screens. Every small-cap number here is
biased upward by an unknown amount; no cross-panel level comparison in this file is a tradable edge.
The object under test — the collinearity of a panel statistic with capitalisation — is affected by
survivorship only through the level of the eligible share, not through its ordering, and the
ordering is what the Spearmans use.

## What to do with it

Proposed reporting clause (Sunday review, not adopted here): **any claim that regresses or compares
across panels of different capitalisation must report the cap mix q alongside any panel property, and
may not attribute a result to `breadth` without showing the property still separates at fixed q.**
Follow-ups queued as ideas 284, 285, 286.

Script: `research/backtests/2026-09-06_is-breadth-a-small-cap-dummy-everywhere-in-the-record_cloud.py`
Artifacts: `.panels.csv` (77 panels), `.books.csv` (142 cells), `.walkforward.csv`, `.census.csv`, `.console.txt`
