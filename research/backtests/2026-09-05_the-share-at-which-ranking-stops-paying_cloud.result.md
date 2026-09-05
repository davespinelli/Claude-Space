# Idea 159 — the-share-at-which-ranking-stops-paying (cloud, 2026-09-05)

> INDEPENDENT CONCURRENT RUN. Lane B ran idea 159 in parallel on a disjoint implementation
> (`..._B.py`) and pushed first. The two agree on every headline — no usable crossing, the cost
> bar cannot bind, do-nothing beats the gate out of sample, the live INV tilt is the worst key.
> Lane B adds the value/cost parallelism and the sign analysis; this run adds the random-key
> control. Read them together.

**ANSWERED — KILL of the proposed PROTOCOL clause.** The number idea 159 asked for exists, is
**q\* ≈ 0.85 [0.80, 0.96]**, and is **useless**: idea 159's cost bar is an order of magnitude too
cheap to bind anywhere a real book trades. The bar that *does* bind is a **random key**, and by
that bar a real cross-sectional key is already noise at **q ≈ 0.10 on u56** — below idea 2's
standing 4b KEEP, which ranks at q = 0.53.

Script: `2026-09-05_the-share-at-which-ranking-stops-paying_cloud.py`
Artifacts: `.console.txt`, `.grid.csv` (294 books), `.curve.csv` (42), `.qstar.csv` (18),
`.bootstrap.csv` (18), `.walkforward.csv` (17). 10 bps, weekly, t+1, gross normalised to 0.75
across names held (idea 153's `norm`). Runtime ~570 s.

## Reproduction

**[a] EXACT.** All 63 overlapping cells of idea 153's committed `.grid.csv` (`norm`, 10 bps,
its 7 shares × INV/NONE/POS) reproduce to machine precision — max|diff| CAGR 9.7e-17, Sharpe
2.2e-16, MaxDD 8.3e-17, H1/H2 2.2e-16. This is literally idea 153's curve, on a 2× finer share
grid (14 points) and 6 keys instead of 2.

**[b] Idea 153's slope CONFIRMED and widened.** Spearman(share, |dCAGR|) = **−0.986** (u56),
**−0.987** (broad), **−0.947** (small). Not strictly monotone (P2 fails on the letter — every
panel has 1–3 local reversals) but overwhelmingly decreasing. The *random* key's magnitude falls
in share too (−0.862 / −0.763 / −0.697), which is the first sign that the decline is arithmetic
rather than informational.

## R1, the literal bar: the number exists and does not bind

`cost_tilt(q) = [Turnover(tilt) − Turnover(NONE)] × 10 bps`, against `mean_k |dCAGR_net|(q)`.

The trouble is the scale. `cost_tilt` runs **1–30 bps of CAGR** across the whole share range
while `|dCAGR|` runs **26–480 bps**. The curves only meet near the mechanical endpoint:

| panel | q\*(R1) LIN | LOG | POW | n at q\* | bootstrap p05–p95 (LIN) | frac. of draws defined |
|---|---|---|---|---|---|---|
| u56 | 0.893 | — | — | 33 of 37 | 0.817 – 0.959 | LIN 98.8%, LOG 19.8%, POW 0% |
| broad | 0.839 | 0.950 | — | 77 of 91 | 0.798 – 0.911 | LIN 99.8%, LOG 61.8%, POW 0% |
| small | 0.877 | 0.910 | — | 124 of 141 | 0.795 – 0.957 | LIN 95.8%, LOG 68.3%, POW 0% |

(400 circular block-bootstrap draws, block 21d, seed 159001, paired within panel; turnover held
at its realised value and not resampled. R2, the breakeven reading, differs by ≤0.06 everywhere
— the two readings are the same answer.)

**P5 confirmed, emphatically.** The POW family never crosses at all (0 of 400 draws on every
panel) and LOG crosses in 20–68%. A crossing that one of three pre-registered families cannot
locate and a second finds in a fifth of resamples is not a number PROTOCOL should write down.
**Recommendation: do not adopt idea 159's clause.** Below q = 0.80 a cross-sectional key always
moves the book by more than its own trading bill — that test simply cannot fail where books live.

## The bar that binds: a random key

`RND` = the composite times a **fixed per-name random draw** (seed 159000), pre-registered, held
constant in time so it costs almost no incremental turnover. Whatever it moves is the arithmetic
noise floor a real key must beat.

| panel | real/RND \|dCAGR\| at q=0.05 | at q=0.53 | crossing q (LIN / LOG / POW) |
|---|---|---|---|
| u56 | 1.48× | **0.53×** | 0.096 / 0.118 / 0.135 |
| broad | 1.66× | **0.87×** | 0.745 / 0.686 / — |
| small | 3.06× | **0.71×** | 0.03 — already at the floor at the smallest share tested |

**On all three panels a real key moves the book LESS than a random one by q = 0.53.** That is
the share of the project's standing 4b KEEP (idea 2's top-20 of 37.5 mean-eligible names on
u56 = 0.53), and 4–5× above u56's crossing at q ≈ 0.10.

But the crossing is **panel-specific by a factor of 7** (0.10 vs 0.68) and undefined on small.
So P4's hoped-for portable number does not exist either. The honest output is a sentence, not a
constant: *on the panel the live book trades, a cross-sectional key stops beating a random one
above roughly 10% of the eligible set — about 4 names of 37.*

## The random key is the best book in the run

Across all 294 books, by key:

| key | 4a passes | 4b passes | 4b on the OOS window |
|---|---|---|---|
| **RND** (random) | **12** | **20** | 16 |
| R6 | 10 | 18 | 18 |
| POS | 8 | 14 | 14 |
| NONE (no key) | 9 | 13 | 14 |
| MOM | 9 | 13 | 8 |
| R3 | 11 | 11 | 18 |
| **INV** (the LIVE tilt) | 11 | **1** | 4 |

**The random scramble tops both KEEP paths and the live `/sqrt(vol20)` tilt is last on 4b by a
factor of 20.** That is the fifth independent confirmation of the delete-the-vol-tilt finding
(ideas 81, 153, 160, 162) and a direct restatement of idea 82: on these panels the ranking is
not adding information, so a key that adds none scores like the rest.

Full census by panel: 4a 70/294 (broad 69, u56 1, small 0); 4b 90/294 (broad 49, u56 41,
small 0); 4b on the OOS window 92/294. Nothing is proposed — these are known books.

## Rule 8 walk-forward (everything fitted on ≤2016-12-31, read once on 2017→)

| arm | mean OOS CAGR | OOS Sharpe | OOS MaxDD |
|---|---|---|---|
| A_BELOW (best IS-Sharpe at share ≤ q\*_IS) | 12.13% | 0.7245 | −25.99% |
| A_ABOVE (best IS-Sharpe at share > q\*_IS) | 6.98% | 0.6596 | −28.96% |
| A_NONE (no ranking, same share as A_BELOW) | **13.39%** | **0.7695** | −26.11% |

SPY OOS 15.45% / 0.882 / −33.72%. RULES v1 OOS: u56 7.73% / 0.747; broad 5.94% / 0.576;
small 7.92% / 0.581.

**Ranking loses to not ranking on the side of q\* where it is supposed to pay**: A_BELOW −
A_NONE = **−0.045** OOS Sharpe, −1.26pp CAGR, wins 1 of 3 panels. On the other side A_ABOVE −
A_NONE = −0.004 Sharpe, −3.09pp CAGR, wins 1 of 2. Against the random bar the arms come out
mildly positive (N_BELOW +0.045, N_ABOVE +0.091) but both are measured against a near-degenerate
q = 0.03 control (n = 2–4 names) and neither survives as evidence for ranking.

The transfer is poor: q\*_IS vs q\*_OOS is 0.98 vs 0.95 on broad, 0.77 vs 0.99 on small, and
undefined on u56; the random-bar crossing goes 0.03 → 0.29 (u56), 0.03 → 0.68 (broad),
0.03 → 0.03 (small). **The threshold is not stable across a single split**, which is the
strongest argument against writing it into PROTOCOL.

One detail worth stating plainly rather than burying: on broad, the IS-Sharpe selector's
A_ABOVE pick was **RND at q = 1.00**, which then delivered the best OOS Sharpe of any arm
(1.0121) and a clean full-sample 4b pass. At q = 1.00 every key holds essentially the whole
eligible set (idea 153's confound (i)), so that book *is* the equal-weight-all-eligible book
wearing a random key. Given the entire grid to choose from, the selector picked the book with
no effective ranking in it.

## Verdict

**KILL** of idea 159's proposed clause. The cost-based q\* is ≈0.85, unbinding, family-dependent
and unstable across the walk-forward split; the random-key q\* is meaningful but panel-specific
by 7× and undefined on one panel. **No number belongs in PROTOCOL.** The finding that does
survive is the sentence: *on u56, above ~10% of the eligible set no cross-sectional key beats a
random one, and the live book ranks at 53%.* **No KEEP** — nothing here proposes a book.

## Caveats

Survivorship on all three panels (current constituents, idea 54); worst on `small`
(`data/SMALL_PANEL_README.md`), where every delisted or acquired sub-$2B name is absent — the
names a bad ranking would have bought are the missing ones, so measured key payoff there is an
upper bound. Ideas 49/39: the eligibility gate is inverted on `small`, so its share axis is
nominal. q\* is a crossing of two shallow fitted curves and inherits the fit family — all three
families are reported and their disagreement is part of the result. `cost_tilt` is modelled
turnover × 10 bps with no slippage or impact, so it is a lower bound and q\*(R1) is biased high.
Idea 153's confound (i) holds: at q → 1.00 tilted and control books converge mechanically, so
every fit is reported with and without that endpoint (dropping it moves q\*(R1) down by
0.06–0.09 and changes nothing). Ideas 38 (calendar-day index) and 126 (t+1) carry over.
