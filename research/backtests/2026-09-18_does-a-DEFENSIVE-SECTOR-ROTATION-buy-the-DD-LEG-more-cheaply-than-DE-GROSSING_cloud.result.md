# Idea 1267 (lane cloud, 2026-09-18) — does a DEFENSIVE ROTATION buy the DD LEG more cheaply than DE-GROSSING?

**VERDICT: KILL (capital), NO NEW BOOK. ANSWERED: NO — TWICE OVER.** 516 cells, 17 of 18 gates
PASS, the one FAIL deliberate and published (it is the answer to the first half of the question).

## 1. On the committed book the mechanism has almost no DOSE — and the reason is idea 1066's
The 2026-09-04 book frees a slot only when the 200d gate has emptied the eligible pool, and the
H=126 minimum hold has already filled those slots with stale names. Rotation therefore touches
**3.7% of rebalances and 0.205 of a slot per week on U56, 0.9% and 0.03 on B135, and NOTHING AT
ALL on SMALL663** (gate G3 FAILs there, published not repaired: a 663-name panel's eligible pool
never empties). Across all 43 U56 cells MaxDD spans **-19.54% .. -19.10%** against the
do-nothing -19.13%: the binding 4b leg does not move. Pre-declared outcome (A). This is idea
1066 seen from the other side — the min hold IS frozen weight, so there is nothing left to free.

## 2. Where the dose exists, rotation is WORSE than cash — outcome (D)
On the H=0 books (slots freed at 10.8% of rebalances, minimum 3 names held) and on B135/SMALL,
filling freed slots with equities instead of cash costs drawdown on every panel: at ROT=1.00 vs
its own de-grossing control, LOWBETA runs **MaxDD -1.13pp (B135) / -5.46pp (SMALL663) / -0.25pp
(U56 H=126)** and CAGR **-0.15 / -0.41 / -0.09pp**, OOS Sharpe -0.031 / -0.039 / -0.005. Low-beta
names in a crash are still equities; de-grossing was the cheaper purchase all along.

## 3. The beta axis is decorative, and its sign is backwards — outcome (C)
LOWBETA minus its RANDOM control at matched ROT (exposure differenced out) is **|d_MaxDD| <=
0.60pp, d_Sharpe within +-0.0096 and negative at 8 of 12 (panel, minhold, fill) groups, d_OOS
-0.0090 .. +0.0050** — the beta input buys nothing a coin does not. Worse for the premise,
HIGHBETA beats LOWBETA where it matters: on U56 H=0 at ROT=1.00, HIGHBETA earns **+1.44pp of
CAGR over cash with MaxDD unchanged** while LOWBETA earns +0.32pp. The weeks the gate empties
the book are not the weeks the drawdown is made.

## 4. Capital
**4a 0 of 516.** 4b 212 of 516, dominated by cells whose own do-nothing already passes. Rule 8
(IS Sharpe on warm-up..2016, OOS read once, 36 choosers): chooser-minus-do-nothing **mean
+0.0042, positive at 9 of 36, best +0.0072 on the committed book's own grid** — noise. Only 9
of 516 cells convert a 4b FAIL to a PASS, all of them B135 / H=126 / RESPREAD, and **three are
RANDOM and three are HIGHBETA**: a ±0.5pp jiggle of a DD leg sitting 0.51pp from its cap, not a
mechanism. Nothing proposed for capital, nothing enacted (rule 6).

## 5. BYCATCH, PARKED, NOT PROPOSED — the de-grossing control is the thing that works
The FILL axis, run only as a control, is the one thing here that converts a committed verdict:
on **B135, H=126, ROT=0**, not re-spreading onto the survivors (freed slots to CASH, fixed
GROSS/N slots) reads **16.06% / 1.0702 / -18.78%, halves 1.2924 / 0.8926, OOS 1.0190, 4b PASS**
against the committed re-spread rule's 16.18% / 1.0715 / **-20.74%, 4b FAIL(DD)** — 1.96pp of
drawdown bought for 0.12pp of CAGR. It is NOT proposed: on the incumbent's own panel it is
strictly dominated (U56 15.47% / 1.1467 / -19.10%, OOS 1.1706 against 15.78% / 1.1522 / -19.13%,
OOS 1.1832) and on SMALL663 it is bit-identical to doing nothing. PARKED for the record.

## Survivorship (rule 9)
U56/B135 current-constituent lists; SMALL663 a current sub-$2B screen (52 of 715 dropped for
max_1d_move >= 1.0). Levels are optimistic, every 4b pass an UPPER bound. The headline is a
DIFFERENCE between what is done with the SAME freed slots under the SAME core selection, so it
is first-order immune. Not neutral, and stated: the rotation pool is drawn from names that
FAILED the trend gate — exactly the population a current panel has cleaned of its casualties —
so the defensive sleeve's return here is FLATTERED and the negative result is, if anything,
understated; the cash control carries no such flattery.

Script: `2026-09-18_does-a-DEFENSIVE-SECTOR-ROTATION-buy-the-DD-LEG-more-cheaply-than-DE-GROSSING_cloud.py`
