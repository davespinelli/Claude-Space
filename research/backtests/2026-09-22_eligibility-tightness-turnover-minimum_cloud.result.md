# Idea 949 (lane cloud, 2026-09-22) — why does TIGHTENING ELIGIBILITY RAISE TURNOVER on all three panels?

**ANSWERED, AND THE QUESTION'S OWN PREMISE IS HALF WRONG. There is NO interior minimum to find:
turnover is STRICTLY DECREASING in `max_vol` across the whole ladder on 6 of 6 equal-weight
instances, so the eligibility screen is turnover-ADDING at EVERY threshold and the minimum is
"no screen at all". The mechanism is the per-member REPLACEMENT RATE, not the count of names
crossing the screen. And on the record's own live top-5 book the dial is INERT.**

## What was priced
`max_vol` ladder 0.20..1.00 in 0.05 steps (17 rungs) x 3 panels x 4 books x 2 cadences x 4 cost
rungs = **408 books / 1,632 grid points**, all published (`*.grid.csv`).  Books: **EWELIG**
(equal weight over gated names at gross 0.75 — the 1/N channel live), **FIXEDW** (fixed weight
gross/Nbar(m) — partial control, Nbar still moves between rungs), **FIXEDW0** (the strict control:
one weight gross/Nbar(m=1.00) at EVERY rung, so an admission moves identical NAV), **V1TOP5**
(`baseline.rules_v1_weights(n=5, w=0.15, max_vol=m)` — the record's own book).  Gate G_COST: cost
reconstruction error vs a direct 25 bps engine run = **0.000e+00**.

Tuned dials (2): THRESHOLD LADDER, PANEL.  Reported, not tuned: book kind, cadence, cost rung.

## Headline
| gate | result |
|---|---|
| **V1 INTERIOR MINIMUM** | **FAIL — and that is the finding.** Turnover is **strictly decreasing in m on 6 of 6** EWELIG instances; argmin sits at the loose EDGE m=1.00 on **12 of 12** EWELIG+FIXEDW instances. Ranges: U56/W 13.56x -> 7.72x, B136/W 16.72 -> 7.90, SMALL/W 26.21 -> 10.36 |
| **V2 945 REPLICATION** | **PASS** — turnover(0.35)/turnover(0.60) = **1.204 / 1.208 / 1.395** on U56 / B136 / SMALL (945 implied 1.15 / 1.16 / 1.25; same sign, larger) |
| **V3 MECHANISM (renormalisation)** | **FAIL as stated** — the strict FIXEDW0 control shrinks the rise to **1.087 / 1.112 / 0.967** but only reverses it on SMALL. In log space the 1/N renormalisation carries **55.1% / 43.8% / 110.1%** of the rise; the rest is a genuine churn-count rise on the two large-cap panels |
| **V3b RATE LAW** | **PASS, decisively** — rho(churn/N, turnover) = **+0.9999 / +0.9997 / +0.9999** against rho(churn, turnover) = +0.8847 / +0.9031 / **−0.7150**. On SMALL the raw count of names crossing the screen **FALLS** as the screen tightens while turnover RISES |
| **V4 CAPITAL** | **PASS** — 105 of 408 rungs clear 4b FULL+OOS at 10 bps (U56 and B136 only; SMALL 0 of 136). **4a = 0 of 408** |
| **V5 RULE 8** | **FAIL** — the IS-chosen m beats its own ladder's median OOS Sharpe on **0 of 3** panels (EWELIG/W) and **12 of 24** instances overall; **mean OOS rank 10.00 of 17**, i.e. worse than the middle of the ladder |

## The mechanism, stated plainly
An equal-weight book's turnover is set by **churn / N** — the share of the held set replaced per
rebalance — not by churn.  Tightening a trailing-vol screen shrinks N far faster than it removes
crossings, so the replacement RATE rises monotonically: on U56/W, N falls 38.3 -> 23.5 while
churn/rebalance barely moves (3.79 -> 4.57), and churn/N climbs 0.0990 -> 0.1948 in lockstep with
turnover (rho +0.9999).  SMALL is the clean proof: churn/rebalance **falls** 44.0 -> 27.4 as the
screen tightens — fewer names cross it — yet turnover nearly triples, because N collapses 279 -> 57.

## The premise's blind spot: the effect does not exist on the record's own book
On **V1TOP5** — `rules_v1_weights` with `max_vol` as its only moving part, the book the record
actually runs — the whole ladder moves turnover by **under 5% of level** (U56/W 22.54x-23.66x,
B136/W 29.44-29.87x, SMALL/W 32.56-33.71x) and the 0.35-vs-0.60 ratio is **0.998-1.002 on all
three panels**, i.e. dead flat.  A top-N book fixes the position count by construction, so the
churn/N channel has nothing to act on.  **945's finding is an equal-weight-book fact, not a
statement about eligibility screens in general**, and any CHANGELOG sentence reading it as the
latter over-generalises.

## Which committed eligibility claims sit on the wrong side of the minimum
A keyword census of `research/*.md` finds **21 committed `max_vol = x` sites** (values 0.046, 0.105,
0.20 x2, 0.30 x4, 0.35, 0.40, **0.60 x10**, 0.75).  Because the turnover minimum is at m = 1.00 on
every panel, **21 of 21 (100%)** quote a threshold on the turnover-RAISING side.  That is a true but
weak statement: the honest reading is that **no vol threshold anywhere on the ladder reduces an
equal-weight book's turnover**, so the record's habit of describing `max_vol` as a calming clause is
wrong at every value it has ever used — while being harmless for the top-5 books it is used on.

## Rule 8 — 2017-2026 read ONCE
m chosen on 2009-2016 IS Sharpe at 10 bps.  Mean OOS rank **10.00 of 17** over 24 instances; on
EWELIG/W the IS pick lands at m = 0.20 on B136 and SMALL and ranks **17 of 17** (dead last) on both.
Fitting the eligibility threshold in-sample is worse than not fitting it.

## Capital — one 4b KEEP-candidate, and it is a TWO-PANEL one (recorded, not recommended)
The IS-only chooser picks m = 1.00 (no screen) on U56 and B136 monthly, and that cell clears 4b in
FULL and OOS on **both** panels: U56 FULL 12.57% / 1.2168 / -15.84% (H1 1.2418 / H2 1.1982),
OOS 13.81% / 1.2916 / -15.84%, turnover 2.13x/yr; B136 FULL 11.82% / 1.1318 / -17.03%
(H1 1.2494 / H2 1.0189), OOS 11.90% / 1.1475 / -17.03%, turnover 2.26x/yr.  Memo filed.  It fails
4a on both (0 of 408 run-wide) and **fails on SMALL** (Sharpe 0.6171 vs SPY 0.8570).

## Survivorship (rule 9)
U56, B136 and SMALL are all CURRENT-CONSTITUENT panels; SMALL = 719 cached names less the **54 with
max_1d_move >= 1.0** (data/small_meta.csv), leaving 665 investable names, SPY a benchmark column
only.  CAGR and MaxDD LEVELS are optimistic and both 4b bars are easier than on a point-in-time
panel.  The primary object — a turnover curve against a threshold on one tape — is first-order
immune; the 4b counts are not.

## Verdict
**ANSWERED / KILL of "tightening eligibility has a turnover optimum" and KILL of the
churn-count reading; PARK of the fixed-weight book that fell out.**

Files: `*.grid.csv` (1,632 rows) · `*.curve.csv` (24) · `*.walkforward.csv` (24) ·
`*.claims.csv` (21) · `*.gates.csv` · `*.log.txt`
