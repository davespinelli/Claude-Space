# Idea 1222 (lane C, 2026-09-18) — is the WIDEST-DIAL HABIT RESOLVABLE on ANY ATTAINABLE FOLD COUNT?

**VERDICT: KILL (capital). ANSWERED = YES ON THE RECORD'S OWN FOUR-LADDER SET, AND THE ENTIRE
YES IS THE DEGENERATE GROSS LADDER.** On disjoint folds the habit resolves at **52 of 108**
(panel, pair, fold-length) cells — but **36 of those 52 are the 36 GROSS pairs, which resolve at
36 of 36 with a minimum |t| of 6.11**, while the non-GROSS pairs resolve at **8 of 36** and at
the headline fold length at **0 of 9**. 10 of 10 gates pass. Runtime 14.1s, offline,
deterministic.

Script: `2026-09-18_is-the-WIDEST-DIAL-HABIT-RESOLVABLE-on-ANY-ATTAINABLE-FOLD-COUNT_C.py`
Dials (2, PROTOCOL rule 4): **FOLD LENGTH L** {63, 126, 252, 504} x **LADDER PAIR SET**
{ALL4, NG}. 8 cells, every one published in `.cells.csv`; the 108 underlying (panel, pair, L)
rows are in `.foldcount.csv`. alpha is not a third dial — 0.05 is the queue's and 0.10 is
reported beside it at every cell. Nothing is selected on.

---

## 1. What this run changes about 1214's construction, declared not buried

1214's fourteen folds are **NESTED expanding windows** (warm-up..2012, warm-up..2013, ...), so
its fourteen readings of a pair are fourteen readings of mostly the same data and **cannot be
averaged to buy precision**. A required-precision calculation needs independent folds, so this
run tiles the tape with **DISJOINT consecutive folds of length L** and makes L a dial. 1214's
252-pair table is therefore NOT reproduced by this script and is not claimed to be.

The statistic is a difference of logs, so fold readings ADD:
`D = log(R_a/d2(k_a)) - log(R_b/d2(k_b))`, and the band on the mean of F folds shrinks as
`1/sqrt(F)` — gated to 0.0100 at F = 1/4/16/64 (G1). **E[D] under H0 is not 0** (the log of an
unbiased estimator is biased low): mu0 runs **-0.0699 to +0.3731** over the six pairs and is
measured by Monte Carlo, not assumed (`.nullmoments.csv`). Orientation is fixed ONCE on the full
sample and held across every fold and cell, so no conditioning correction is smuggled in; the
per-fold agreement rate with that fixed direction runs at a median 0.9143.

## 2. The answer, and the one fact that empties it

At the headline cell (**ALL4, L = 252, alpha = 0.05**) **9 of 18 (panel, pair) cells resolve** at
the F_max = 17 folds the tape supplies — exactly the 0.50 the pre-declared outcome (A) required.
Across all 8 cells:

| set | L | cells | F_max | resolved (.05) | resolved (.10) | median F* | median YEARS* |
|---|---|---|---|---|---|---|---|
| ALL4 | 63 | 18 | 70 | 13 | 13 | 14 | 3.4 |
| ALL4 | 126 | 18 | 35 | 11 | 12 | 12 | 6.0 |
| ALL4 | 252 | 18 | 17 | 9 | 11 | 10 | 9.5 |
| ALL4 | 504 | 18 | 8 | 11 | 12 | 2 | 5.0 |
| NG | 63 | 9 | 70 | 4 | 4 | 110 | 27.5 |
| NG | 126 | 9 | 35 | 2 | 3 | 116 | 58.0 |
| NG | 252 | 9 | 17 | **0** | 2 | 72 | 72.0 |
| NG | 504 | 9 | 8 | 2 | 3 | 18 | 36.0 |

**The GROSS pairs resolve at 36 of 36, at every panel and every fold length, with |t| from 6.11
to 41.34.** That is not a measurement of anything: IS Sharpe is flat in gross (1189, reproduced
here), so the GROSS ladder's spread is near zero at every fold and the log ratio against it is
huge and stable. Strip it (NG) and the habit resolves at **8 of 36**, at the headline fold length
at **0 of 9**, and the median non-GROSS pair needs **27.5 to 72 years** of tape. **1223's open
complaint is now priced: the record's four-ladder comparison set manufactures its own
resolvability.**

## 3. Two things the required-precision calculation says that are new

- **SHORTER FOLDS WIN.** 13 cells resolve at L = 63 against 9 at L = 252. More folds beats
  noisier per-fold readings on this tape, i.e. the `sqrt(F)` gain dominates the dispersion the
  short window adds. Anyone reading a dial off yearly folds is leaving resolution on the table.
- **THE IID BAND IS TOO NARROW, BY A MEASURED AMOUNT.** The empirical per-fold sd runs at a
  median **1.3879x** the iid-normal null's (range 0.4784-4.0366), so a band assumed rather than
  measured understates the required fold count by roughly the square of that — about **1.9x**.
  Every F* here is quoted on the tape's own dispersion, not the null's; both are in the CSV.

## 4. Best case, against the tape actually in hand

Taking each (panel, pair)'s best fold length, **14 of 18** cells need no more tape than the
15.6-17.6 years available — but **only 5 of 9** once GROSS is dropped, and those five need 6.5 to
13.2 of the years in hand, i.e. they are resolvable and barely. The four that are not resolvable
at any attainable count need **18 to 296 years** (B136 N/H needs 296).

## 5. The capital arm — rule 8, both KEEP paths, nothing new

66 rung books on three panels: **4a 0; 4b full 17; 4b OOS 16; BOTH 15.** 96 rule-8 decisions
(dials chosen on warm-up..2016 ONLY, 2017-2026 read ONCE): **4a 0; 4b BOTH 16, and all 16 are one
distinct book — the U56 anchor N=20 / H=126 / g=0.75 / W**, 15.78% / 1.1522 / -19.13%, halves
1.2127/1.1128, OOS 17.28% / 1.1832 / -19.13%. That is the standing 2026-09-04 incumbent
(1214's same book reads 15.71% / 1.1480 / OOS 17.16% — the gap is a refreshed price cache, not a
construction difference). **CONFIRMATORY, NOT GENERATIVE. NO NEW CANDIDATE, NO MEMO, NOTHING
ENACTED.**

Made deployable, the resolution test is the only chooser that does not lose: mean OOS Sharpe
**CH_RES 0.9226 > CH_ANCHOR 0.8869 > CH_RAW = CH_POINT 0.8479**, and CH_RES vs the anchor is
+0.0357 with 4 wins / 0 losses / 20 ties. **Under 1211's decision-row correction that collapses
to ONE distinct move** — SMALL, H = 252, +0.2143 of OOS Sharpe — counted four times across the
(ladder set x L) cells, inflation factor 4. In the rolling walk the same deltas run t = +0.40 to
+0.84, inside one SE at every cell. **A single decision on the worst panel is not evidence.**

**THE LADDER-SET DIAL IS INERT ON PRICE.** ALL4 and NG give bit-identical picks at all 48 rule-8
rows and all 672 rolling pick-cells, because the point-widest ladder and its runner-up are never
GROSS (its spread/d2 is the smallest of the four everywhere). The dial moves ARM A's census and
not one capital decision.

## 6. Caveats

Survivorship: `universe.json` / `universe_broad.json` are CURRENT constituents; the small panel
is the current output of a sub-$2B screen — 715 rows at this commit, 51 drop for
`max_1d_move >= 1.0`, 664 tradable remain (the label SMALL439 does not denote this pool, 1074
still open). F* is a point estimate built on an observed effect that is itself measured with
error, so a cell reading F* = 18 against F_max = 17 is not meaningfully different from resolvable
— the honest content is the ORDER of magnitude, and for the non-GROSS pairs that order is
decades. The disjoint-fold tiling drops the tape's remainder (up to L-1 rows) and treats folds as
independent, which the 1.39x sd ratio shows they are not exactly. Benchmarks read 0.07pp above
1214's committed figures throughout because the price caches were refreshed between the two runs.
