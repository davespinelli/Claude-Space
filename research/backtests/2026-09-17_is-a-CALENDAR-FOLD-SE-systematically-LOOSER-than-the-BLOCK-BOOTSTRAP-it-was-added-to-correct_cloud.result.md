# Idea 1212 — is a CALENDAR-FOLD SE systematically LOOSER than the BLOCK BOOTSTRAP it was added to correct?

**VERDICT: KILL, and the queue's question is mis-posed.** Against a difference whose true
value is **zero by construction**, the fold-clustered SE is **not systematically looser and not
systematically inflating t's**: at the record's own L = 252 the three bases reject at **S_IID
0.0389, S_FOLD 0.0611, S_BLOCK 0.0722** against a nominal 0.0500 over 180 null pairs. What the
fold SE *is* is **almost entirely a function of the fold length nobody states** — its honest
critical value runs **1.64 at L = 21 to 2.53 at L = 504, a factor of 1.54** — and, as a chooser,
it is the **least stable of the three and loses to doing nothing**.

Script: `2026-09-17_is-a-CALENDAR-FOLD-SE-systematically-LOOSER-than-the-BLOCK-BOOTSTRAP-it-was-added-to-correct_cloud.py`
Artefacts: `.pairs.csv` (183), `.dialgrid.csv` (2,745), `.calibration.csv` (180), `.census.csv`
(210), `.picks.csv` (48), `.gates.csv`, `.hypotheses.csv`, `.log.txt`. **Gates 6 of 6 PASS**,
including the fast runner against `engine.backtest` at 1.4e-17, `S_BLOCK at L = 1 == S_IID` to
0.46% relative, `S_FOLD` returning NaN rather than a number when fewer than two folds are usable,
and **P_SPLIT's two halves sharing no name at any rebalance (overlap exactly 0)**.

**LANE NOTE.** The queue's literal last open idea at claim time was 1218, which this run's own
idea-1205 arm filed minutes earlier. Taking it would have been this lane marking its own homework
on the same machinery, so this is 1212 — the last open idea not authored by this run.

## THE TWO DIALS AND NO MORE (rule 4, and the queue names both)
`SE BASIS` {S_IID, S_BLOCK, S_FOLD} × `FOLD LENGTH` L {21, 63, 126, 252, 504} = **15 cells, every
one published**. L is carried into **both** clustered bases — S_FOLD's fold length *and* S_BLOCK's
block length — so the two are read at matched clustering scale and a gap between them cannot be a
gap between two window sizes. NOT dials: PANEL {U56, B136, SMALL}; PAIR KIND {P_NULL, P_SPLIT} plus
the non-null power control P_SPY; 30 disjoint pairs per (panel, kind); levels {0.10, 0.05, 0.01};
the 4a/4b legs; the rule-8 arm. Book frozen at the 2026-09-04 KEEP-4b candidate's construction,
10 bps, next-day execution, warm-up 260, IS ends 2016-12-31, anchor N 20 / H 126 / g 0.75 / weekly.

## (A) WHY A KNOWN-NULL DIFFERENCE IS THE ONLY THING THAT SETTLES IT
"Which SE is bigger" cannot decide which SE is *right*: on a difference that is genuinely there, a
small SE is correct and a large one is waste. An SE is right or wrong only where the truth is zero.
Two exchangeable constructions give that, and **both are verified exchangeable before anything is
read off them** (H_EXCH: mean ΔSharpe **P_NULL +0.0052, P_SPLIT −0.0189** over 90 pairs each):

- **P_NULL** — two gross-matched random books, N names drawn uniformly from those eligible at each
  rebalance. Mean pair correlation 0.9033.
- **P_SPLIT** — the eligible pool split at random into two halves at each rebalance, the *real*
  composite's top-N taken from each. Mean pair correlation 0.8234, halves provably disjoint (G4).

**A declared expectation of this run failed and is reported as a finding, not repaired:** P_SPLIT
was expected to be the *more* correlated pair and is the **less** (0.823 vs 0.903), because two
uniform draws from a small eligible set both approximate its average while two top-of-composite
books from disjoint halves diverge. What matters for a fold SE is not contemporaneous correlation
but **year-to-year persistence of the difference**, and there P_SPLIT is the harder case as
intended (mean |lag-1 autocorrelation of the yearly ΔSharpe| **0.2159 vs 0.2004**).

## (B) THE CALIBRATION — THE FINDING
False-positive rate at |t| > 1.96, pooled over 3 panels × 2 null kinds (n = 180 pairs per cell).
**Nominal is 0.0500.**

| basis | L=21 | L=63 | L=126 | **L=252** | L=504 |
|---|---|---|---|---|---|
| S_IID | 0.0500 | 0.0500 | 0.0500 | **0.0389** | 0.0500 |
| S_BLOCK | 0.0500 | 0.0611 | 0.0500 | **0.0722** | 0.0944 |
| S_FOLD | 0.0111 | 0.0333 | 0.0389 | **0.0611** | 0.0833 |

Empirical 95th percentile of |t| — the honest critical value against the 1.96 the record quotes:

| basis | L=21 | L=63 | L=126 | **L=252** | L=504 |
|---|---|---|---|---|---|
| S_IID | 1.9496 | 1.8901 | 1.9224 | **1.8346** | 1.9076 |
| S_BLOCK | 1.9379 | 1.9874 | 1.9438 | **2.0507** | 2.4004 |
| S_FOLD | 1.6417 | 1.6897 | 1.7996 | **2.0748** | 2.5341 |

**Three things follow.** (i) **H_LOOSE is SUPPORTED but trivially so** — S_FOLD rejects less than
S_BLOCK at L = 252 (0.0611 vs 0.0722), so the fold SE is not the offender the queue's framing
expects; both sit within a factor of 1.5 of nominal and **H_CAL is SUPPORTED at all three bases**.
(ii) **The real dial is L, not the basis.** S_FOLD's critical value moves **1.64 → 2.53 (×1.54)**
and S_BLOCK's **1.94 → 2.40 (×1.24)** across the L ladder, on the same 180 pairs with nothing else
changed. At L = 21 a fold SE is *over-conservative* (rejects 0.0111, a fifth of nominal); at L = 504
it *over-rejects* at 0.0833. **This is 1208's "block length is the record's largest unstated dial"
arriving from the calibration side, and it applies to the fold length identically.** (iii) The
harder null is harder for everyone: at L = 252, P_SPLIT rejects at 0.0556 / 0.0889 / 0.0778
(IID / BLOCK / FOLD) against P_NULL's 0.0222 / 0.0556 / 0.0444.

**1210's ordering leg reproduces; 1210's magnitude leg does not.** SE_IID ≤ SE_BLOCK at
**0.2722–0.3667** of 180 null pairs at every L (1210 measured 0.3750 of 59). But 1210's "SE_FOLD's
median is the SMALLEST" **does not hold on a known-null difference at matched scale**: median SE
runs S_FOLD 0.1423 / 0.1330 / 0.1328 / 0.1247 / 0.1108 against S_BLOCK 0.1274 / 0.1210 / 0.1197 /
0.1116 / 0.1054, i.e. **S_FOLD is the LARGEST of the three at L ≤ 252** and only dips below S_IID at
L = 504. 1210's smallest-median was a property of the *real, persistent* differences it measured,
not of the fold basis.

## (C) WHICH COMMITTED t's ARE INFLATED — CENSUS
Recovery rule, published and applied verbatim: scan `research/LEADERBOARD.md` and
`research/CHANGELOG.md` for `t = X`, `t of X`, `t's to X`, `(t X)`, `mean/SE +X`; classify a hit
FOLD-CLUSTERED if "fold", "cluster" or "year" occurs within 200 characters. **210 committed
t-values recovered; 10 classify as fold-clustered: 0.06, 1.09, 1.15, 1.17, 1.63, 1.94, 3.07, 3.07,
3.07, 3.56.** Against the honest L = 252 fold critical value of **2.07** rather than 1.96:
**4 clear 1.96 and the same 4 clear 2.07 — 0 are inflated** (H_CENSUS SUPPORTED). The one that
comes close is the 1.94, which fails both bars.

**The recovery rule's limit, stated rather than hidden:** it classifies only 10 of 210 hits as
fold-clustered because most committed t's in the record do not name their SE basis within 200
characters. The census answers *"of the fold-clustered t's the record's own text makes
identifiable, none is inflated"* — it does **not** license "no committed t in the record is
inflated", and the 200 unclassified ones are exactly the gap idea 1208 is about.

## (D) RULE 8 AND BOTH KEEP PATHS — EVERY CHOOSER LOSES TO DOING NOTHING
Benchmarks (10 bps, post warm-up): **U56 SPY 15.06% / 0.8814 / −33.72% (halves 0.9598/0.8170), OOS
15.15% / 0.8684; U56 RULES v2 (live) 8.60% / 1.1980 / −12.05%, OOS 9.42% / 1.2714; B136 SPY 15.16%
/ 0.8861 / −33.72%, OOS 15.33% / 0.8767; B136 LIVE 7.98% / 1.0993 / −12.24%, OOS 7.88% / 1.1059;
SMALL SPY 14.06% / 0.8581 / −33.72%, OOS 15.33% / 0.8767; SMALL LIVE 4.30% / 0.6637 / −13.89%, OOS
3.75% / 0.5600.** Each (basis, L) is a chooser: from the 9-rung N ladder take the book whose **IS**
Sharpe difference vs the anchor has the largest signed t under that basis. Chosen on warm-up →
2016-12-31 ONLY; 2017-2026 read ONCE.

**Mean OOS Sharpe: S_IID 0.8202, S_BLOCK 0.8174, S_FOLD 0.8103 — against the anchor book, which
does nothing, at 0.8750.** All three lose; the naive IS-Sharpe control loses most (0.7910).
**H_WF REFUTED.** The fold SE is also the **least stable chooser**: over 15 (panel, L) cells it
lands on **6 distinct N** (5, 10, 12, 15, 25, 40) against S_BLOCK's 4 and C_ISSHARPE's 3 — which is
what an SE whose critical value moves ×1.54 with an unstated dial does to a decision.

**4b full 14 of 48, 4b OOS 26, BOTH 14, 4a 0 of 48** — and **all 14 are ONE book**, U56 / N = 12
(17.65% / 1.1658 / −20.17%, halves 1.274/1.083, OOS 18.78% / 1.1701 / −20.17%), already committed
by 1183. **CONFIRMATORY, NOT GENERATIVE. NO NEW CANDIDATE, NO MEMO, NOTHING ENACTED.**

## WHAT THIS IS WORTH
The capital content is a reporting rule, not a book: **a committed t built on a fold-clustered or
block SE is uninterpretable without its L, because L alone moves the honest critical value from
1.64 to 2.53.** Quoting the L is free; the alternative is a bar that is a fifth of nominal at one
end of the ladder and 1.7× nominal at the other. Beyond that, nothing here supports choosing
between books on an SE-based t at all: all three bases picked worse books than the anchor out of
sample, on the one comparison where the answer was checked rather than argued.

## SURVIVORSHIP (rule 9)
U56 and B136 are CURRENT-CONSTITUENT lists; SMALL is the current output of a sub-$2B screen
(`data/SMALL_PANEL_README.md`) less the documented `max_1d_move >= 1.0` exclusion — 52 of 715
dropped, 663 investable names plus SPY as benchmark only. A false-positive RATE is one construction
measured against itself on one tape and the bias very largely cancels out of (B); the census in (C)
is a scan of committed text and carries no market bias at all. The bias does **not** cancel out of
the rule-8 OOS levels or the 4b legs in (D), so the 14 passes are an upper bound.

## FOLLOW-UPS FILED
1219 (should every committed t carry its SE basis and its L — the census could classify only 10 of
210), 1220 (the fold SE is the least stable chooser at 6 distinct picks over 15 cells — is chooser
instability a readable function of an SE's own L-sensitivity), 1221 (all three SE choosers lose to
the anchor: is there ANY chooser on this record that beats doing nothing out of sample).
