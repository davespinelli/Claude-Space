# Idea 837 — does ANY cheap-to-compute BOOK STATISTIC order OOS SHARPE out of window at n ≥ 30?

**Lane C, 2026-09-12.** Script `2026-09-12_does-ANY-cheap-to-compute-BOOK-STATISTIC-order-OOS-SHARPE-out-of-window-at-n-GE-30_C.py`.
Runtime 545 s. 10 bps, next-day fill, each family's committed cadence. **No new constructors** —
every arm is a rung of a weights function already committed in idea 833's script (which copied
them from 831 / 641 / 574 / 804), so idea 833's MEMO12 is a strict subset (gate G1).

## ANSWER: **NO — and the queue's remedy does not work the way it was meant to.**

At the honest reading (b) IS→OOS, **not one of ten cheap statistics orders OOS Sharpe at the
record's +0.70 bar** on the 39-arm corpus. Best is **NEGTURN +0.4587** (iid p 0.0040 — the only
iid-significant one), and its **cluster-bootstrap 95% CI is [−0.0109, +0.7735]: it covers zero.**
**0 of 10 cluster CIs exclude zero.** The published Sharpe itself reads **−0.0320** (iid p 0.8463,
CI [−0.5005, +0.4276]).

And the premise: **going n = 12 → 39 narrows the iid band from 0.5804 to 0.3172 (H_NARROW PASS) —
but only if the 39 arms are 39 independent draws. They are 14 families of 2.8 near-duplicate arms.**
Collapsed to family means the iid band is **0.5341, barely better than n = 12**, and the cluster
bootstrap widens every ARMS39 interval to a mean width of **0.7494** under (b). The corpus the
record can build out of its own committed constructors has an effective n of about 14, not 39.

## What DOES survive at n = 39 under (b), cluster-corrected — 9 of 60 cells, all mechanical

| predictor (IS) | target (OOS) | Spearman | iid p | cluster 95% CI |
|---|---|---|---|---|
| CAGR | OOS_CAGR | +0.6174 | 0.0002 | [+0.2353, +0.8671] |
| CAGR | OOS_MaxDD | −0.7267 | 0.0000 | [−0.9017, −0.3964] |
| CAGR | gross_band | +0.3976 | 0.0132 | [+0.0881, +0.6831] |
| MAXDD | OOS_CAGR | −0.5039 | 0.0010 | [−0.7830, −0.1457] |
| NEGVOL | OOS_CAGR | −0.7864 | 0.0000 | [−0.9035, −0.5646] |
| NEGVOL | OOS_MaxDD | +0.6536 | 0.0000 | [+0.3703, +0.8992] |
| NEGVOL | gross_band | −0.6056 | 0.0001 | [−0.7642, −0.3657] |
| NEGTURN | OOS_CAGR | −0.3571 | 0.0262 | [−0.6498, −0.0084] |
| NEGTURN | cost_surv | +0.4637 | 0.0027 | [+0.0270, +0.7571] |

Every survivor is an arithmetic coupling of the book's own risk/cost budget — vol buys return and
buys drawdown, turnover buys cost survival, return level persists in level. **None of them is
`OOS_Sharpe`.** The one thing the record actually ranks books by is the one thing nothing predicts.

## The contaminated reading, for contrast

Under (a) FULL→OOS — the record's actual practice — **22 of 240 cells clear +0.70** against **1 of
240** under (b), and mean |ρ| is **0.4031 against 0.2471**. At the headline corpus the same five
CORE5 statistics read **SHARPE +0.7200, CAGR +0.1358, MAXDD +0.2940, CALMAR +0.4508, H2 +0.9749**.
That H2 = +0.9749 is idea 833's identity again, at 3× the corpus: **H_IDENT PASS at 0.9487** — 37 of
39 arms have full-sample MaxDD *equal* to their OOS MaxDD to 1e-9, so a "full-sample" headline is
largely a restatement of the window it claims to be validated on.

**Rule 8 on the claim: FAILS by the widest margin the record has recorded.** The pair chosen under
(a) by highest ρ vs OOS_Sharpe is **(H2, ARMS39) at +0.9749**; read once under (b) it is **−0.0401**,
**gap 1.0150** against the pre-registered 0.30 bar.

## Replication of idea 833

**H_REPLIC PASS: 6 of 6 target signs agree** with 833's committed MEMO12 (b) reading, at a third the
noise. ARMS39: OOS_Sharpe −0.0320, OOS_CAGR −0.0075, OOS_MaxDD −0.3132, share_3y −0.0628,
cost_surv +0.0085, gross_band −0.1441. 833 MEMO12: −0.2797, −0.0699, −0.4825, −0.1399, +0.0582,
−0.0381. Magnitudes attenuate toward zero as n grows — the shape of a null, not of a weak signal.

**But the corpus choice moves the headline more than the headline moves anything (H_SETFREE FAIL).**
Spearman(SHARPE, OOS_Sharpe) under (b) reads ARMS39 −0.0320, MEMO12 −0.2797, U56ARMS **+0.2488**,
FAMMEAN14 −0.0549 — **spread 0.5285** against a 0.30 bar. Choosing the panel flips the sign.

## The reader's actual use

Split the 39 arms at the median IS (..2016) Sharpe — the ranking a reader had in 2016. Out of
sample the **top half loses on 5 of 6 targets** (OOS Sharpe 1.1553 vs 1.1736, OOS CAGR 13.22% vs
13.26%, OOS MaxDD −18.43% vs −16.76%, share_3y 0.2974 vs 0.3118, gross_band 0.2039 vs 0.2368) and
wins only on cost_surv (38.1 vs 31.7 bps). A coin wins 3.

## Gates and hypotheses

**G1–G4 all PASS.** G1: the twelve MEMO arms reproduce idea 833's committed `.books.csv` to
**2.220e-16** across full CAGR/Sharpe/MaxDD, OOS CAGR/Sharpe and share_3y, and its headline cell
rebuilds at **+0.6084** against a committed +0.6084. G2 free cost ladder at 10 bps = the 10-bps
backtest, max|d| **0.000e+00**. G3 gross rung f = 1.000 re-run (not aliased) = the base book,
**0.000e+00**. G4 max realised gross **1.0000** at every book and every rung — PROTOCOL rule 2's
no-leverage clause is never bent to widen a band.

**7 of 14 pre-registered hypotheses PASS.** PASS: H_REPRO, H_N30 (n = 39, 14 families), H_NARROW
(0.3172 ≤ 0.35), H_SIG (NEGTURN p 0.0040), H_REPLIC, H_IDENT (0.9487), and H_ANY_A (the
contaminated reading clears the bar — which is the point). FAIL: **H_ANY** (best +0.4587 vs +0.70),
**H_SHARPE** (−0.0320), **H_CLUSTER** (0 of 10 CIs exclude 0), **H_SIGN** (6 of 10 negative),
**H_SETFREE** (spread 0.5285), **H_STATBEST** (best is NEGTURN, not SHARPE), **H_R8CLAIM** (gap
1.0150).

## PROTOCOL rule 8 on the books (mandatory)

39 arms, full window and OOS 2017-01-01.. . Arms: full CAGR 6.22–17.74% (median 11.92%), Sharpe
0.932–1.226 (median 1.117), MaxDD −24.32% to −11.13%; **OOS CAGR 6.38–19.03% (median 13.18%),
OOS Sharpe 0.993–1.394 (median 1.170), OOS MaxDD −24.32% to −11.13%.** Comparands on the same
windows: **RULES v2 LIVE** full 8.63%/1.2018/−12.05%, **OOS 9.47%/1.2782/−12.05%**; RULES v1 full
6.41%/0.6602/−13.83%, OOS 7.60%/0.7361/−13.83%; **SPY** full 15.16%/0.8861/−33.72%, **OOS
15.33%/0.8767/−33.72%**.

**KEEP paths: fixed-window 4b PASS 26 of 39; OOS-local 4b PASS 27 of 39; 4a PASS 0 of 39; BOTH 0 of
39.** All 39 arms beat SPY's OOS Sharpe; only **5 of 39** reach SPY's OOS CAGR. 15 of the 26 4b
passers are not among idea 833's twelve (`TOPN-n30, TOPN-n40, BUF-m10, BUF-m50, TOPND-m20,
BANDW-b0.00, BANDW-b0.06, BANDW-b0.12, BANDM-b0.03, BANDRS-b0.03, BRD-q0.25, R6-n30, BANDWB-b0.03,
BANDWB-b0.08, MARSB-g0.75`). **None is promoted**: these arms were enumerated to answer a census
question, not searched for as candidates, so per the record's own standard (idea 814) they are
filed as a follow-up, not as a KEEP. That 26 of 39 arbitrarily-enumerated arms clear 4b is itself a
reading on how much the 4b bar discriminates on this panel.

## Verdict

**KILL for the ordering claim at n ≥ 30. No KEEP claimed, no book promoted, no memo.**
Idea 833's null replicates at 3× the corpus with all six signs intact and magnitudes shrinking
toward zero. The queue's remedy — more books — narrows the *iid* band as intended but does not buy
independence: the record's committed constructors yield families, not draws, and the cluster
bootstrap puts every OOS-Sharpe interval across zero. **The honest statement the record can make
today is that it cannot order books by out-of-window Sharpe with any statistic it publishes, and
that no corpus it can build from its own arm tables will settle the question** — that needs
independent book *forms*, not more rungs of the same dials.

SURVIVORSHIP: U56 and B136 are current-constituent lists; every level above is optimistic. This run
reads orderings across books on one panel, which survivorship moves far less than a level, but no
CAGR or Sharpe printed here is a capital claim.

Files: `.console.txt` (full log), `.books.csv` (39 arms + 2 comparands + 2 SPY rows, all predictors
and targets), `.grid.csv` (480 cells), `.cluster.csv` (120 cluster CIs), `.census.csv` (entry-date
census), `.ladders.csv` (cost and gross ladders), `.walkforward.csv` (rule 8 on the books).
RULES.md, PROTOCOL.md, research/scan.py, products/bot/bot.py and research/baseline.py untouched.
