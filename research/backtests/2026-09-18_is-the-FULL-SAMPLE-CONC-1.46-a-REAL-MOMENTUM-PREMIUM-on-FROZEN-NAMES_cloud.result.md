# Idea 1068 (lane cloud, 2026-09-18) — is the FULL-SAMPLE CONC 1.46 a REAL MOMENTUM PREMIUM on FROZEN NAMES?

**VERDICT: KILL (capital), NO NEW BOOK / ANSWERED: NEITHER OF THE TWO PRE-DECLARED READINGS.**
75 cells (5 MINHOLD x 5 MAXHOLD x 3 panels), 6 age buckets, 3 shuffle seeds, 21 of 21 gates PASS,
14s, offline, deterministic.

## The answer
The excess is **not** a rebalance-timing artefact and it **does not decay with holding age**, so
neither pre-declared reading survives as written. On U56 the per-unit-weight excess over the
same-day eligible pool runs, by age bucket 1-21 / 22-63 / 64-126 / 127-252 / 253-504 / 505+,
**+1.01 / +8.12 / +5.57 / +7.11 / +7.78 / +11.63 pp** annualised (CONC **1.0583 / 1.5724 / 1.3775
/ 1.4743 / 1.5499 / 1.9214**). The youngest bucket — the one outcome (ART) said carries it — is
the **weakest** at 11.1% of weight, and the profile is flat-to-RISING out to 505+ days rather than
decaying past a 12-1 horizon, which is what (CONT) required. B135 reads the same shape
(-1.90 / +5.75 / +9.59 / +9.17 / +6.53 / +11.10 pp) with an outright NEGATIVE young bucket.

**But almost none of it is an AGE fact.** Against SHUFFLEAGE — the same name-days with their age
labels permuted *within each calendar day*, which keeps the day mix and destroys the age axis —
the U56 profile's excess-minus-null is **-0.16 / -0.72 / -2.39 / +1.95 / +2.14 / +9.61 pp**: four
of six buckets sit inside +-2.4pp of a null that knows nothing about age. The one bucket that
separates, 505+, is **3.2% of book weight** and is **in-sample only (XS_IS +22.71 vs XS_OOS
+1.26)**. B135's 505+ bucket is 0.5% of weight and does not separate at all (-0.60). The 1.46 is
a statement about WHICH DAYS the book is invested, not about how long it has held.

**And it is exactly the reading survivorship manufactures.** U56/B135 are current-constituent
lists, so a survivor's whole path is in the panel and the LONGEST holdings are the most flattered.
The one age-specific signal in the run points in precisely that direction, in the in-sample window,
on 3.2% of weight. It is recorded as bias-consistent, not as an edge.

## The grid (all 75 cells in the .grid.csv)
**4a 0 of 75** — live v2's -12.05% MaxDD is not beatable by a growth book, as at every other dial.
**4b 14 of 75: U56 13 of 25, B135 1 of 25, SMALL663 0 of 25.** Of the 61 failures the **DD leg
fails at 56**, joined by H2 31, OOS 30, H1 22, CAGR 22 — the sixth dial running to say the
committed 4b pass is a statement about drawdown and nothing else. The MAXHOLD dial buys nothing:
on U56 the anchor (H=126, A=NONE) posts 15.78% / 1.1522 / -19.13%, and putting a forced exit on
it gives 15.67% / 1.1335 / -18.57% at A=252 and 14.93% / 1.0949 / -19.34% at A=504 — 0.56pp of
drawdown for 0.11pp of CAGR and 0.019 of Sharpe at A=252, and strictly worse at A=504.

## Rule 8 (walk-forward, IS Sharpe on warm-up..2016, OOS read once)
| panel | pick (H, A) | OOS Sharpe | anchor OOS | chooser - do-nothing | 4b | rank corr |
|---|---|---|---|---|---|---|
| U56 | (21, 126) | 1.0998 | 1.1832 | **-0.0834** | FAIL (DD) | -0.2047 |
| B135 | (63, 126) | 1.0238 | 1.0240 | **-0.0002** | FAIL (DD) | +0.2443 |
| SMALL663 | (252, 252) | 0.6677 | 0.4534 | **+0.2143** | FAIL (H2, OOS, DD) | -0.0378 |

The chooser's pick **fails 4b on all three panels**, and on the anchor panel it is 0.0834 of OOS
Sharpe BEHIND doing nothing. SMALL's +0.2143 buys a book whose OOS Sharpe 0.6677 is still below
SPY's 0.8769 on three legs. IS/OOS rank correlation is -0.2047 / +0.2443 / -0.0378 over 25 cells:
this grid is not choosable. The best OOS cell on every panel is (H=252, A=504) — **recorded, not
promoted**, and reached by no honest chooser in the run.

## Benchmarks on this tape
U56 SPY 15.13% / 0.8849 / -33.72%, OOS 0.8747; LIVE v2 8.62% / 1.2018 / -12.05%, OOS 1.2781.
B135 SPY 15.16% / 0.8862, OOS 0.8769. SMALL663 SPY 14.06% / 0.8582, OOS 0.8769.
G1 replays the committed anchor triple 15.7147% / 1.1480 / -19.1276% to **5.965e-05**
(vintage-pinned to 2026-09-16; the live tape runs 1 trading day longer, published not toleranced).

## Two gates that failed first and are published rather than re-specified
1. **The pool comparand was look-ahead.** It was first written as "eligible at today's close",
   which conditions on today's own return; r_pool came out at 35-58% annualised and made every
   bucket's excess catastrophically negative. The book reads eligibility at t-1 (rule 2), so its
   comparand must too. Fixed, and the wrong version is named in the code.
2. **G4 "mean hold is monotone in both dials" was the wrong bar.** It failed on U56 at
   (H=21, A=504) 74.3288d vs (H=21, A=NONE) 74.2483d. First diagnosis — censoring of still-open
   holdings at the tape end — was real and fixed, and the inversion survived. The true cause is
   that a forced exit frees a slot and the two books DIVERGE from that rebalance on, so mean
   realised hold is a path statistic across two different books. The gate is now what the dial
   actually guarantees (a HARD CAP: no holding exceeds A plus one rebalance gap, 0 violations on
   all three panels), and the mean-hold ladder is published beside it with its 1-of-20 exception
   named.

## Capital
No new book. The min hold's CAGR gain is not a holding-age premium that a MAXHOLD dial can
harvest, trim or time; it is where the book is invested on which days, and the only age-specific
residual is small, in-sample, and pointing the way a current-constituent panel biases it.
