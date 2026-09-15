# Idea 887 — does the MEDIAN-vs-MEAN SIGN INSTABILITY track a SKEW statistic the record could publish instead?

**Lane C, 2026-09-15. ANSWERED = NO. THE GAP IS A SKEW FACT; THE INSTABILITY IS NOT.**
The standardised median−mean gap is almost entirely a skew fact (**R² 0.82**, slope **0.224** against
Pearson's 1/3, and 0.75–0.89 at every one of the six claim sets) — but the *instability* is a
**LOCATION** fact, and location is exactly what a scale- and location-free shape statistic cannot
carry. Shape statistics alone classify which claims are unstable at a leave-one-file-out balanced
accuracy of **0.6667** at their best grid point (bar 0.80), and the practical form of the proposal —
recover the MEAN's sign from (median, sd, skew) — works **81.5% overall but 53.8% on the unstable
subset**, i.e. a coin toss precisely where the record needs it. **H_GAP, H_UNRES and H_WF CONFIRMED;
H_SHAPE and H_SIGN REFUTED on their own bars.**
The rival one number is not a shape statistic at all: **100.0% of the 26 unstable cuts sit below the
signed estimator's own resolvability bar** (max |z| **1.2374** against a bar of 2.0), and the
instability rate among RESOLVABLE cuts is **0.0000 at all six claim sets**. So PROTOCOL does get its
one number — it is the sign-test |z| the signed estimator already produces for free — but it buys
well-definedness by **stripping the sign from 59.6% of the record's re-priceable placebo cuts
(78.3% of the headline set)**, which is the honest price and is stated as such.
**KILL for capital — nothing here is a book.** No PROTOCOL change is applied (rule 6); one is
PROPOSED. RULES.md, PROTOCOL.md, scan.py, bot.py, baseline.py untouched.

Script: `2026-09-15_does-the-MEDIAN-vs-MEAN-SIGN-INSTABILITY-track-a-SKEW-statistic_C.py`
Outputs: `.cuts.csv` (151 + shape stats) `.grid.csv` (54 classifier points) `.regress.csv`
`.walkforward.csv` `.books.csv` `.keep.csv` `.console.txt`

## The algebra, stated before any regression was run

With `s = ex_null − ex_BLOCK` the per-arm gap vector, standardise by its own cross-arm sd:

    M   = median(s)/sd(s)              standardised LOCATION
    LAM = (mean(s) − median(s))/sd(s)  standardised MEDIAN-MEAN GAP,   mean(s)/sd(s) = M + LAM

    unstable  ⟺  median·mean < 0  ⟺  M·(M+LAM) < 0  ⟺  sign(M) ≠ sign(LAM)  AND  |M| < |LAM|

Instability is therefore a function of the **pair** (location, gap), decided by the ratio
ρ = M/LAM (unstable ⟺ −1 < ρ < 0). A shape statistic is scale-free and location-free by
construction, so it can deliver LAM and **cannot** deliver M. That is an identity, not a finding, so
it was asserted as **gate G2** up front rather than discovered at the end — and it is what makes the
queue's hypothesis a genuinely empirical question only in the form "is LAM big enough, often enough,
to dominate M?". It is not.

## Gates — 4 of 4 PASS

| gate | test | result |
|---|---|---|
| G0 | the 151 cuts recomputed from the raw per-arm CSVs reproduce idea 880's committed `claims.csv` | 151 vs 151, max abs diff over MED/MEAN/z/n = **7.1e-15** |
| G1 | the de-duplication reproduces 880's 23-claim headline set | **23 of 31, identical sets** |
| G2 | the identity above | **151 of 151** |
| G3 | the unstable flags reproduce 880's committed `sign_unstable` column | **151 of 151** |

Two tuned parameters, the queue's own: **shape statistic** (SKEW / EXKURT / NEAR / SKEW+EXKURT /
SKEW+EXKURT+NEAR / LAMBDA, plus three declared NON-shape contrasts) × **claim set** (ALL 151 /
HEADLINE 23 / HEADLINE_RAW 31 / COST 89 / WINDOW 62 / NEARABLE 72). All 54 grid points printed.

**Coverage the queue's third regressor does not have:** NEAR (share of arms within one seed-SE of
zero) is computable on **72 of 151 cuts** — only 3 of the 5 files committed seed dispersion, and
**no** IS/OOS cut commits it anywhere. Out of sample the queue's tail-mass leg does not exist.
Five cuts (idea 882's `OP_REAL`, which is BLOCK by construction) have cross-arm sd = 0 and carry no
shape statistic at all; they are dropped from every regression (n reads 146, not 151) and read
stable in the counts.

## 1. Q1 — the GAP is a skew fact. **H_GAP CONFIRMED**

`LAM ~ a + b·stat`, every claim set:

| claim set | SKEW R² / slope | EXKURT R² / slope | NEAR R² / slope |
|---|---|---|---|
| ALL (146) | **0.8236 / 0.2242** | 0.1578 / −0.0391 | 0.7878 / −0.3833 |
| HEADLINE (22) | **0.8079 / 0.2284** | 0.2642 / −0.0448 | 0.8681 / −0.4061 |
| HEADLINE_RAW (30) | **0.8906 / 0.2453** | 0.3013 / −0.0646 | 0.8530 / −0.3976 |
| COST (86) | 0.8204 / 0.2308 | 0.2685 / −0.0494 | 0.7878 / −0.3833 |
| WINDOW (60) | 0.8331 / 0.2207 | 0.0818 / −0.0290 | — (not computable) |
| NEARABLE (69) | 0.7489 / 0.2128 | 0.4725 / −0.0695 | 0.7878 / −0.3833 |

Skew explains three quarters to nine tenths of the standardised gap at every claim set, and the
slope is stable at **0.21–0.25** — inside the pre-registered [0.20, 0.47] bracket but consistently
**below Pearson's 1/3**, i.e. these gap distributions are less skew-driven than the textbook
relation assumes. Excess kurtosis is nearly useless on its own (R² 0.08–0.47). NEAR is a good
proxy *where it exists* (R² 0.79–0.87, negative slope: more mass within a seed-SE of zero ⇒ smaller
standardised gap) — but it exists on under half the cuts and on none of the out-of-sample ones.

## 2. Q2 — shape alone cannot say WHICH claims are unstable. **H_SHAPE REFUTED**

Leave-one-**FILE**-out (the only honest fold: cuts inside one file share arms). `bal_acc` is the
pre-registered bar at a fixed 0.5 cut-off; `bal_acc_trthr` uses a cut-off chosen on the *training*
fold only and is reported because the classes are 17–30% positive — it is an extra column, not a
moved bar. Best point per feature set (by `bal_acc`, ties broken by `bal_acc_trthr`; several shape
sets tie at 0.5000, which is the all-negative rule):

| feature set | kind | best claim set | bal_acc | bal_acc_trthr | AUC |
|---|---|---|---|---|---|
| SKEW | shape | WINDOW | 0.5000 | 0.7222 | 0.6512 |
| EXKURT | shape | COST | 0.5273 | 0.6962 | 0.4939 |
| NEAR | shape | ALL/COST/NEARABLE | 0.5000 | 0.6111 | 0.4059 |
| SKEW+EXKURT | shape | HEADLINE_RAW | 0.5170 | 0.6989 | 0.6534 |
| **SKEW+EXKURT+NEAR** | shape | **HEADLINE** | **0.6667** | **0.7917** | 0.7222 |
| LAMBDA | shape | HEADLINE_RAW (best trthr) | 0.4773 | 0.5284 | 0.4716 |
| \|M_LOC\| | **location — not a shape statistic** | HEADLINE_RAW | 0.7670 | 0.8693 | **0.9318** |
| SKEW+\|M_LOC\| | mixed — not a shape statistic | HEADLINE_RAW | 0.6818 | 0.6591 | 0.8580 |
| **\|z\|** | **the estimator's own bar — not a shape statistic** | **HEADLINE_RAW** | **0.8920** | 0.8693 | **0.9631** |

The best shape-only point misses the 0.80 bar on the pre-registered column (0.6667) **and** on the
fairer train-threshold column (0.7917), so the refutation does not turn on the cut-off choice. It is
also the point with the smallest sample in the whole grid (n=18, 6 positive) and the only one whose
AUC clears 0.70 — every shape set at n ≥ 69 sits at AUC 0.38–0.59, i.e. **at or below chance**.
Meanwhile the location contrast reaches AUC 0.83–0.93 and |z| reaches 0.86–0.96. This is the
identity in §0 showing up as an out-of-fold measurement, exactly as it should.

## 3. The practical form of the proposal — recover the MEAN's sign from median + skew. **H_SIGN REFUTED**

`mean_hat = median + sd·skew/3` (parameter-free Pearson) and a fitted variant:

| claim set | form | sign recovery, all | on the UNSTABLE subset | on the stable subset |
|---|---|---|---|---|
| ALL | PEARSON 1/3 | **81.5%** | **53.8%** (14 of 26) | 87.5% |
| ALL | FITTED | 83.6% | 46.2% | 91.7% |
| HEADLINE | PEARSON 1/3 | 81.8% | 57.1% (4 of 7) | 93.3% |
| HEADLINE_RAW | PEARSON 1/3 | 86.7% | 62.5% | 95.5% |
| COST | PEARSON 1/3 | 81.4% | 55.0% | 89.4% |
| WINDOW | PEARSON 1/3 | 81.7% | 50.0% | 85.2% |
| NEARABLE | PEARSON 1/3 | 82.6% | 61.1% | 90.2% |

This is the decisive number for the queue's proposal. A run that publishes its median, its sd and
its skew has published a *mean-sign* that is right 82% of the time overall — and **46–62%, a coin
toss, on exactly the claims whose sign was in dispute.** Fitting the coefficient makes the unstable
subset *worse* (46.2%), because the fit is driven by the many stable cuts. Publishing a shape
statistic does not replace the declared convention; it replaces it with a wrong answer half the
time, silently.

## 4. Q3 — the rival one number, and what it costs. **H_UNRES CONFIRMED**

| claim set | n | unstable | max \|z\| among unstable | share below \|z\|=2 | unstable rate among UNRESOLVABLE | among RESOLVABLE |
|---|---|---|---|---|---|---|
| ALL | 151 | 26 | **1.2374** | **100.0%** | 28.9% | **0.0000** |
| HEADLINE | 23 | 7 | 0.9428 | 100.0% | 38.9% | **0.0000** |
| HEADLINE_RAW | 31 | 8 | 0.9428 | 100.0% | 36.4% | **0.0000** |
| COST | 89 | 20 | 1.2374 | 100.0% | 33.3% | **0.0000** |
| WINDOW | 62 | 6 | 1.2374 | 100.0% | 20.0% | **0.0000** |
| NEARABLE | 72 | 18 | 1.2374 | 100.0% | 33.3% | **0.0000** |

Idea 880 observed this on its 7 headline claims (|z| ≤ 0.94); it holds at **26 of 26** across all
151 cuts, with a clean margin (1.2374 against 2.0). **No resolvable claim in the re-priceable
corpus is sign-unstable, at any claim set.** So the pooling convention is undecidable only where
the claim itself is undecidable, and the fix costs no new number.

**The price, stated rather than buried** — a declared "quote no sign below |z| = 2" strips the sign
from every *unresolvable* cut, not only the unstable ones:

| claim set | n | unresolvable | share stripped | unstable claims left carrying a sign |
|---|---|---|---|---|
| ALL | 151 | 90 | **59.6%** | **0** |
| HEADLINE | 23 | 18 | **78.3%** | **0** |
| COST | 89 | 60 | 67.4% | 0 |
| WINDOW | 62 | 30 | 48.4% | 0 |

## 5. Rule 8 (a) — the shape→gap law walks forward. **H_WF CONFIRMED**

Fitted on the IS-window cuts only (`LAM = −0.0059 + 0.2099·SKEW`, R² 0.7028, n=30), read once on
the OOS-window cuts (n=30):

| window | R² on own cuts | own slope | sign recovery under the **IS-fitted** law | unstable | recovery on unstable |
|---|---|---|---|---|---|
| IS (fit) | 0.7028 | 0.2099 | 83.3% | 2 | 0.0% (0 of 2) |
| OOS (read once) | 0.9363 | 0.2403 | **90.0%** | 4 | 75.0% (3 of 4) |

The law itself is portable — slope 0.2099 → 0.2403, and sign recovery moves **6.7 pp**, inside the
10 pp tolerance. **What walks forward is the finding that the gap is a skew fact; what does not
walk forward is any ability to use it**, since the unstable subsets are 2 and 4 claims and the
IS-window one is recovered 0 of 2. H_WF is confirmed on its stated bar and is the weakest leg here
by sample size.

## 6. Rule 8 (b) — the books, both KEEP paths (10 bps, next-day, weekly)

A census has no book of its own, so idea 880's declared grid and IS-only selector (highest
2009–2016 Sharpe over 384 arms per panel) are carried verbatim; OOS read once.

| panel | IS pick | CAGR | Sharpe | MaxDD | H1/H2 | OOS CAGR | OOS Sh | OOS DD | 4a | 4b |
|---|---|---|---|---|---|---|---|---|---|---|
| U56 | CORR-HI q0.07 w1008 d1.00 W g1.00 | 12.73% | 1.034 | −22.93% | 1.160/0.915 | 12.41% | 1.016 | −22.93% | ✗ | ✗ |
| B136 | CORR-HI q0.12 w252 d1.00 W g1.00 | 13.91% | 1.166 | −16.63% | 1.289/1.037 | 12.97% | 1.154 | −16.63% | ✗ | **✓** |
| SMALL | VOL20-LO q0.17 w252 d1.00 D g1.00 | 5.04% | 0.404 | −48.52% | 0.736/0.201 | 2.00% | 0.203 | −48.52% | ✗ | ✗ |
| — | RULES v2 live (U56 / B136 / SMALL) | 8.64 / 7.98 / 4.30% | 1.208 / 1.101 / 0.663 | −11.90 / −12.18 / −13.89% | 1.237/1.186 · 1.237/0.968 · 0.806/0.554 | 9.49 / 7.88 / 3.75% | 1.286 / 1.108 / 0.559 | — | — | — |
| — | SPY (same windows) | 15.13 / 15.16 / 14.06% | 0.885 / 0.886 / 0.858 | −33.72% | 0.959/0.824 · 0.960/0.826 · 0.914/0.834 | 15.27 / 15.33 / 15.33% | 0.874 / 0.877 / 0.877 | — | — | — |

Unselected base rates: **4a 0.0% on all three panels**; 4b U56 15.9%, B136 11.5%, SMALL **0.0%**.
The single 4b pass is the same B136 CORR-family by-product that 875, 881, 882 and 880 each memo'd
and declined — **declined a fifth time, not promoted, no KEEP memo written.** Its IS pick is
selected on Sharpe, not on 4b, and it loses to SPY on CAGR (13.91% vs 15.16%) while the record has
now four times failed to make this family survive its own follow-up.

## PROPOSED PROTOCOL amendment (rule 6: PROPOSED, NOT APPLIED; PROTOCOL.md untouched)

> A run reporting a placebo difference must publish the **sign-test |z|** beside the number, and
> **must not attach a sign to a reading with |z| < 2**. This supersedes the "declare your pooling
> rule" clause idea 880 proposed for the median/mean ambiguity — not because that clause is wrong,
> but because it is unnecessary: across all 151 re-priceable cuts, **no resolvable claim is
> sign-unstable**, and every unstable one sits at |z| ≤ 1.24. A shape statistic cannot do this job:
> skew predicts the median−mean *gap* well (R² 0.82) but predicts the *mean's sign* on the disputed
> claims at 46–62%, no better than a coin. The cost of the rule is explicit and should be quoted
> with it: **59.6% of the corpus's cuts (78.3% of the headline set) would carry no sign at all.**

## Honest limits

1. **The denominator is idea 880's, and it is tiny.** Five files, 151 cuts, 23 independent headline
   claims, 26 unstable. Every percentage here is a small-sample reading, and the best shape grid
   point (0.6667 / AUC 0.7222) rests on n=18 with 6 positives.
2. Leave-one-file-out gives only 5 folds and the files are not equal-sized (15–55 cuts), so a single
   file drives any fold's result. Where a training fold had no positive class the fold's prediction
   falls back to the training base rate, which is scored as no information rather than dropped.
3. NEAR is computable on 72 of 151 cuts and on **zero** IS/OOS cuts, so the queue's tail-mass leg
   is untested out of sample. Its `NSEED = 20` inherits 880's assumption for the three
   dispersion-bearing files.
4. H_UNRES's 100.0% is a statement about *this* corpus. It is consistent with the algebra (both
   |M| small and |LAM| > |M| are needed, and |z| is a monotone reading of location) but it is not
   guaranteed: a heavily skewed claim with a large resolvable median could in principle be unstable,
   and none is present here.
5. The moment skew `g1` is itself noisy at n = 1,152–3,456 arms that are not independent (they
   share names and days across the grid), so the R² of 0.82 is an association across cuts, not a
   distributional test.
6. SURVIVORSHIP: the book leg's U56 and B136 are current-constituent lists; SMALL is the sub-$2B
   panel with every `max_1d_move` ≥ 1.0 ticker dropped (716 → 664) and holds current constituents
   only, so its levels are the most optimistic here and its 0-of-384 4b rate is an upper bound that
   still reads zero. The census legs inherit whatever bias their source runs carried.
7. Deterministic; the census legs read committed CSVs read-only.

**Verdict: ANSWERED = NO. The median−mean GAP is a skew fact (R² 0.82, slope 0.224 vs Pearson
0.333, stable across all six claim sets and walking forward at 0.2099 → 0.2403), but the SIGN
INSTABILITY is a LOCATION fact that no shape statistic can carry: shape alone classifies it at
LOFO balanced accuracy 0.6667 (bar 0.80) and recovers the disputed mean's sign 53.8% of the time.
The one number PROTOCOL can require instead is the sign-test |z| the signed estimator already
produces — 100.0% of the 26 unstable cuts sit below |z| = 2 (max 1.2374) and 0.0% of resolvable
cuts are unstable, at the price of stripping the sign from 59.6% of the corpus. H_GAP, H_UNRES and
H_WF CONFIRMED / H_SHAPE and H_SIGN REFUTED / KILL for capital.**
