# Idea 90 — `gross-interval-as-a-pre-registered-KEEP-bar` (lane B, 2026-09-05)

> **INDEPENDENT CONCURRENT REPLICATION.** A second lane-B run
> (`2026-09-05_gross-interval-as-a-pre-registered-KEEP-bar_B.py`) claimed and answered this same
> idea in parallel and pushed first. The two implementations were written independently and
> **agree on every shared number**: 72 non-empty books, contiguity 72/72 at the published bars,
> idea 144's corpus reproduced to its own 6dp precision, Spearman(IS width, OOS Sharpe) +0.542
> here vs +0.540 there against the binary's +0.546 and IS Sharpe's +0.902, the same widest book
> (`u56|TOP20|10|vol60-dg`, m in [0.85, 1.20]), the same 4 of 51 operational pairs (all EWall:
> `vol60-dg`, `vol60-rw`, `band3-rw`, `ddctl-recover`), 0 on the small panel, and the same verdict.
> Two numbers differ because the constructions differ, not the data: the within-passing Spearman
> (+0.126 here on the 67 IS-admitted books, +0.055 there on its own passing set) and the width
> selector's OOS Sharpe (1.0488/1.0495 here for argmax-width at m = midpoint / pinned, 1.0397
> there for a w* threshold selector). Widths here are in **realised mean gross**; there, in m.
> Four measurements below are **new**: the shoulder census, the censoring census, 4a's set as a
> one-sided cap, and the 42-point contiguity sweep. So is the Q4b re-check of idea 84's by-product.

**Verdict: ANSWERED — KILL of the proposal as worded ("quote the width INSTEAD of a pass/fail"),
KEEP of the interval as a reported descriptor with two companion statistics.**
No book proposed, no KEEP candidate, RULES untouched. One replacement clause for the Sunday review
in `...memo.md`. One correction to idea 84's own by-product (below), one new discrepancy queued.

Script `2026-09-05_gross-interval-as-a-keep-bar_B.py`. 306 books x a 25-point gross family =
**7,650 runs**, rebuilt from scratch here rather than read from a csv. Two tuned parameters
(phi, delta), all **42** grid points reported. Both KEEP paths evaluated. Rule 8 run.

---

## Reproduction (all four pass before any new number is read)

| check | result |
|---|---|
| (a) `H.run` (every instrument off) vs `engine.backtest`, 3 books x 3 panels | max\|diff\| = **0.000e+00** on all three panels |
| (b) idea 94's published `EWall + vol60-dg` u56@10bps row | **11.58715% / 1.1333 / -16.88395%**, diff vs published **0.000e+00** |
| (c) idea 144's committed 7,650-row family file | index identical; max\|diff\| **5.0e-07** over 17 shared numeric columns — that file is written at 6dp, so this is its own precision floor; 0 `pass4a` disagreements |
| (d) idea 144/131 census + the rebuilt m=1.00 slice | 306 rows / 82 Pareto / 29 pass-4b / 27 floor-only / 97 pass-4a, all exact; slice diff **2.22e-16** |

## Q1 — is the admissible gross set an interval?  **Mostly, and not everywhere.**

Across all 42 (phi, delta) points there are 2,707 non-empty book-verdicts, of which **52 (1.92%)
are GAPPED** — the admissible m-set is not contiguous. Every gap sits at **phi <= 0.50**, i.e. where
the CAGR floor is weak or switched off; at the published (0.70, 0.60) **0 of 72** are gapped.

So "interval" is exact at the published bars and is an approximation in general. The clause must
say *admissible set*, with the interval as its hull, or it silently asserts something false one
time in fifty.

## Q2 — the interval for all 306 books at (phi=0.70, delta=0.60)

**72 of 306** books have a non-empty set (idea 144's family-4b count; the point-4b count is 29).
Width, in **realised mean gross**:

| p0 | p25 | p50 | p75 | p90 | p100 | mean |
|---|---|---|---|---|---|---|
| 0.0000 | 0.0256 | **0.0750** | 0.1124 | 0.1788 | 0.2490 | 0.0789 |

Median admissible points **3 of 25**; **17 books** are a single grid point (width 0.000 — admissible,
but with no headroom the grid can see). Two structural facts:

* **Right-censoring: 9 of 72 (12.5%)** intervals end at m = 1.30, the no-leverage ceiling — their
  upper end is set by PROTOCOL rule 2, not by the DD cap. Left-censoring is 0 of 72. This is idea
  145's warning ("width alone is not robustness — a bar that binds on nothing has an infinite
  band") reappearing on the gross axis, and it is why the censoring flag has to travel with the
  width. It is also idea 148's question, from the other side.
* **Nothing on the small panel and nothing in the V1u book has a non-empty interval** — all 72 are
  u56/broad, EWall or TOP20.

## Q3 — which bar sets each end?  **Idea 84's mechanism holds exactly.**

| shoulder | census over the 72 |
|---|---|
| lower (fails one grid point below g_lo) | **CAGR 72 / 72** |
| upper (fails one grid point above g_hi) | **DD 62**, grid/no-leverage ceiling **9**, `H2+DD` **1** |

The single Sharpe-bar shoulder is on a `ddctl` arm, where m is *not* a pure exposure rescale
(idea 144 Q1). Restricted to the **55 pure-rescale books** (`ctl`/`gate`/`stop`): **0 Sharpe bars at
either shoulder**. Family Sharpe spread confirms why — mean max-min over the 25 m points is 0.0034
(`gate`), 0.0039 (`ctl`), 0.0038 (`stop`) against 0.1928 (`dd`) and 0.0487 (`bud`).

## Q3b — the other KEEP path.  4a's set is one-sided, and 4b is a strict subset of it.

4a (Sharpe > live RULES v1 in both halves, MaxDD no worse) is non-empty for **184 of 306** books,
and **183 of those (99.5%) run right down to the grid floor**: with no CAGR floor, 4a is a *cap*,
not an interval — the mechanism predicts this and it is confirmed. Median 4a width 0.5716, 7.6x
the 4b median. Cross-tab: **both 72, 4b-only 0, 4a-only 112, neither 122** — on this corpus every
4b pass is a 4a pass, so 4b is the binding path, as PROTOCOL rule 4b intends.

## Q4 — the clause as worded ("non-empty on both universes at 10 AND 25 bps")

Of **51** (book, arm) pairs on the large-cap pair, **4** have all four cells non-empty and **4** have
a non-empty joint interval — the intersection **collapses nothing** (0 cases of 4/4 individually
but empty jointly), so on this corpus the conjunction is exactly "4 of 4", and the joint widths are
thin: 0.0199 to 0.0756 of gross. Adding the small panel: **0 of 51** survive 6/6.

| book + arm | joint interval | joint width | thinnest cell |
|---|---|---|---|
| EWall + `vol60-dg` | [0.6839, 0.7594] | 0.0756 | 0.1084 |
| EWall + `band3-rw` | [0.7502, 0.7877] | 0.0375 | 0.0375 |
| EWall + `vol60-rw` | [0.6753, 0.7127] | 0.0375 | 0.0750 |
| EWall + `ddctl-8/.5/recover` | [0.7210, 0.7409] | 0.0199 | 0.0505 |

### Q4b — a correction to idea 84's own by-product

* **The incumbent book (`EWall + vol60-dg`) at the published g = 0.75 is INTERIOR in 4 of 4 cells.**
  Its joint ceiling is 0.7594, set by broad's DD cap — so the published gross is right, and raising
  it toward 0.85 breaks it on broad (2 of 4 cells at g = 0.85).
* **Idea 84's proposed by-product, idea 57's `ew-band3` at g = 0.85, is inside its own interval in
  only 1 of the 4 cells** (u56@10bps). It is out on u56@25 and out on broad at both cost rungs, the
  broad ceiling being 0.7877 — **three grid steps away, which is not a resolution artifact**. By
  contrast g = 0.75 misses that same cell's floor by 0.0002 (one step, and that *is* an artifact).
  Caveat carried honestly: idea 84 swept a 312-point fine ladder and also read a 5 bps rung, and
  the `dg`/`rw` convention is a real fork (`band3-dg` is empty on broad at both rungs). This is a
  documented disagreement to resolve, not a settled overturn — **queued as idea 154**.

## Q5 — rule 8.  Interval read on 2009-2016 only, 2017-2026 untouched.

IS intervals: 67 of 306 non-empty (1 gapped), median IS width 0.1119. OOS truth: 82 of 306 books
have some m clearing OOS-4b; 35 clear it at the published m = 1.00.

**(a) Does the width carry information the binary pass does not?  No.**

| predictor | AUC vs OOS-4b (family) | AUC vs OOS-4b (m=1.00) | Spearman vs OOS Sharpe |
|---|---|---|---|
| binary IS pass (incumbent) | +0.700 | **+0.634** | +0.546 |
| **IS interval width** | +0.714 | +0.632 | +0.542 |
| plain IS Sharpe at m=1.00 | **+0.915** | **+0.820** | **+0.902** |

Width beats the binary by +0.014 AUC on one target and loses by 0.003 on the other, and **both are
beaten by a wide margin by the statistic the project already has**. Inside the 67 books the binary
screen already admits — the only place a width could add anything — Spearman(width, OOS Sharpe) =
**+0.126** and AUC(width -> OOS pass at m=1.00) = **+0.467**, i.e. *below* a coin flip. The one real
signal is Spearman(width, **OOS CAGR**) = **+0.579**, which is close to a tautology: a wide interval
is by construction a book with CAGR headroom over the floor, and it predicts CAGR, not quality.

**(b) As a live selector** (one arm+m per (panel, book, cost) cell, IS information only; the width
selectors take no parameter of their own — argmax, not threshold):

paired on the **7 of 18** cells every selector enters:

| selector | OOS CAGR | OOS Sharpe | OOS MaxDD |
|---|---|---|---|
| S0 do nothing (control arm, m = 1.00) | **14.18%** | **1.0513** | -24.31% |
| S1 incumbent: IS-point-4b screen + argmax IS Sharpe | 12.70% | 1.0219 | -21.14% |
| S2 widest IS interval, m = midpoint | 13.10% | 1.0488 | **-20.52%** |
| S3 widest IS interval, m pinned at 1.00 | 13.20% | 1.0495 | -20.70% |
| S4 argmax IS Sharpe, no screen at all | 12.70% | 1.0219 | -21.14% |
| SPY (same window) | 15.45% | 0.8820 | -33.72% |
| RULES v1 (same cells) | 4.77% | 0.4795 | -19.67% |

Across all 18 cells (selectors that decline a cell are excluded from their own mean and the count
is shown): S0 10.65% / 0.762 / -27.39% on 18; S1 12.70% / 1.022 / -21.14% on 7; **S2 13.10% / 1.049
/ -20.52% on 7**; S3 13.20% / 1.050 / -20.70% on 7; S4 9.06% / 0.695 / -23.12% on 18.
Full-sample of the same IS-chosen picks: S2 12.86% / 1.0693 / -20.52% (halves 1.196/0.970),
S1 12.78% / 1.0624 / -21.14% (1.215/0.942), S0 10.19% / 0.7683 / -27.39% (0.861/0.701).

Two readings, both of which have to be stated:

1. The width selector **does** edge the incumbent — +0.027 OOS Sharpe, +0.40pp CAGR, 0.6pp less
   drawdown, on all three at once. That is the best case for the idea and it is small.
2. **S1 and S4 are identical to the last digit on all 7 cells**, i.e. the incumbent IS-4b screen
   changes 0 picks — an independent reproduction of idea 132 — and **the paired control S0 has the
   highest Sharpe and CAGR of the five**. Every screen here, width included, is paying return for
   drawdown by *declining 11 of 18 cells*, not by choosing better inside a cell. Abstention again.

Against the mandated references, the width selector's OOS numbers beat SPY on Sharpe (1.049 vs
0.882) and drawdown (avg -20.52% vs -33.72%) at 84.8% of SPY's CAGR, and beat RULES v1 on Sharpe
and CAGR while giving up drawdown (-20.52% vs -19.67%). These are equal-weighted averages of 7
book statistics, **not** the statistics of one combined portfolio, and are reported as such.

## Answer to idea 90, in one line

**Publish the interval, keep the pass/fail.** The interval is a true and useful description of a
book — its shoulders are exactly the two bars idea 84 named, and the incumbent book's published
gross is interior on all four large-cap cells — but its *width* has no out-of-sample content beyond
the binary verdict it summarises, and is dominated by plain IS Sharpe on every target tested. A
width quoted without its censoring flag and its shoulder bars would be actively misleading, since
1 in 8 of them is set by the no-leverage clause rather than by any 4b bar.

## Caveats carried

Survivorship on all three panels (idea 54). The IS window's SPY MaxDD is shallower than the OOS
window's (idea 128), biasing every Q5 selector the same way. The m grid is 0.05 wide, so widths
quantise to ~0.035 of gross and a one-step disagreement is noise. `ebud` and `ddctl` arms are not
pure exposure rescales; they are kept, flagged, and reported separately wherever it matters.
Idea 38 (calendar-day index) and idea 126 (t+1 only) carry over.

## Artefacts

`.console.txt` (full log), `.intervals.csv` (306 books x interval, shoulders, censoring),
`.grid.csv` (the 42-point phi x delta sweep), `.joint.csv` (Q4), `.intervals4a.csv` (Q3b),
`.walkforward.csv` (Q5a, per book), `.selectors.csv` (Q5b, per cell), `.family.csv.gz`
(the rebuilt 7,650-run corpus), `.memo.md` (proposed clause).
