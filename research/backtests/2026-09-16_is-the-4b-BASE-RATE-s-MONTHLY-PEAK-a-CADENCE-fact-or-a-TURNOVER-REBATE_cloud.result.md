# Idea 1009 — is the 4b BASE RATE's MONTHLY PEAK a CADENCE fact or a TURNOVER REBATE?

**cloud lane, 2026-09-16, idea 1 of 2.**
Script: `2026-09-16_is-the-4b-BASE-RATE-s-MONTHLY-PEAK-a-CADENCE-fact-or-a-TURNOVER-REBATE_cloud.py`

## ANSWERED = A TURNOVER REBATE. KILL the monthly peak as a cadence fact.

At **0 bps the peak is not at M at all** — it is at **D**, and the gross base rate falls
monotonically with holding period. Charging costs deletes D and W, and M is simply what is
left standing. Equalising the cost drag across cadences at 10 bps removes **97.7%** of M's
advantage over D and W.

## THE TWO PROFILES (mean `base4b` over the 10 (panel, book) cells, 200 draws each)

| rung | D | W | M | Q | argmax |
|---|---|---|---|---|---|
| **0 bps** | **0.4585** | 0.4490 | 0.3080 | 0.0395 | **D** |
| 10 bps | 0.0000 | 0.0015 | **0.2210** | 0.0310 | M |
| 25 bps | 0.0000 | 0.0000 | **0.0460** | 0.0150 | M |
| 50 bps | 0.0000 | 0.0000 | 0.0000 | **0.0020** | Q |

**H_1007 PASS.** 1007's published 10 bps profile `0.000 / 0.003 / 0.212 / 0.030` reproduces
here at `0.000 / 0.002 / 0.221 / 0.031`, worst |d| **0.0090** against a ±0.05 bar, at 200
draws against its 100/60. The claim being tested is real; its *reading* is what dies.
(A test of a PUBLISHED claim at a different draw count, not a bit-level cross-run.)

**H_PEAK0 FAIL** — the question, answered. At 0 bps M's margin over the best other cadence is
**−0.1505**, not positive. **H_REBATE PASS** (ratio −0.79 against a ≤ 0.25 bar).

## THE MECHANISM — two opposite gradients crossing at M

| cadence | annual turnover | cost drag @10 bps | `p_L4_DD` @0 bps | `p_L1_H1` @10 bps |
|---|---|---|---|---|
| D | 164.7 | **16.47 pp/yr** | 0.802 | **0.000** |
| W | 35.3 | 3.53 pp/yr | 0.786 | 0.406 |
| M | 8.7 | 0.87 pp/yr | 0.540 | 0.887 |
| Q | 3.1 | 0.31 pp/yr | **0.136** | 0.975 |

1. **Before cost the gradient runs the OTHER WAY.** `base4b` is 0.459 / 0.449 / 0.308 / 0.040
   at D/W/M/Q. The leg that carries it is **`L4_DD`** (0.802 / 0.786 / 0.540 / 0.136): a book
   that rebalances rarely drifts, and drift widens drawdowns. Slowing down *costs* a coin
   flip 4b passability. That part **is** a genuine cadence fact, and it is negative for M.
2. **Cost is an almost pure function of cadence.** D turns over **19.0×** M and W **4.1×** M
   (943's ratio range 16–33× reproduces). At 10 bps that is 16.5 vs 0.9 pp/yr of drag.
3. **The rebate decides the argmax.** At 10 bps every Sharpe leg on D collapses to 0.000 and
   W's halve, while M loses almost nothing. **M does not win; D and W are removed.**

**H_EQDRAG PASS, and it is the cleanest single number here.** Charging every cadence the same
daily drag (the cell's mean over the four cadences) while keeping its own schedule collapses
the M-over-mean(D,W) gap from **+0.2203 to +0.0050 — 97.7% removed.**

**H_REAL FAIL, in the same direction.** The real books show the identical inversion: 4b passes
by cadence run **D 6 / W 7 / M 3 / Q 0 at 0 bps**, **0 / 4 / 3 / 0 at 10 bps**, and M only
takes the lead at 25 bps (0/1/**3**/0) and 50 bps (0/0/**3**/0). The null's story is the book's.

**H_MONO PASS**, 0 of 120 rung steps increase. **H_TURN FAIL as pre-registered**: ρ(turnover,
base4b drop) is **+0.619 / +0.524 / +0.467** at 10/25/50 bps — right sign, right ordering, but
it *decays* with the rung and misses the ≥ 0.50-at-50-bps bar, because by 50 bps the drop has
saturated at the cell's whole rung-0 base rate and the rank information is gone. 943's
predictor works where there is room for it to work, which is the low rungs.

## THE CAVEAT THAT OUTRANKS THE QUESTION

**At 0 bps a gross-matched coin flip clears the whole of 4b 45.9% of the time on daily
cadence.** 4b at zero cost is not a bar. Every zero-cost 4b claim in the record is being read
against a null that passes about half the time, and the run that quotes one without its base
rate is quoting a coin.

## RULE 8 (PROTOCOL rule 8) — OOS 4b **0 of 24**, OOS 4a **0 of 24**

(book, cadence) chosen on 2009–2016 **alone** by three IS-only choosers × 2 panels × 4 rungs;
2017–2026 read once. Best pick `U56 C_ISSHARPE → TOP10/M @0 bps`: OOS **18.05% / 1.1410 /
−23.17%**. Comparands, same window: SPY **15.21% / 0.8713 / −33.72%** (U56) and 15.33% /
0.8769 / −33.72% (B136); RULES v2 @10 bps **9.45% / 1.2765 / −12.05%** (U56), 7.88% / 1.1061 /
−12.24% (B136). **23 of 24 picks bind `L4_DD`** — the drift leg, again. No KEEP candidate on
either path, so no memo, no promotion.

Seven real cells do pass 4b at 10 bps (U56 EWELIG/W, EWELIG/M, TOP20/W, TOP20/M, TOP40/W,
TOP40/M; B136 TOP40/W) — the record's existing objects — but **no legal IS-only chooser picks
any of them**, which is rule 8 doing its job.

## GATES — 8 of 8 PASS

G0 `offset_mask` ≡ `engine.rebalance_mask` (0 rows) · G1 fast runner ≡ `engine.backtest`
(2.08e-17 / 4.44e-16) · G2 `band_book` ≡ `baseline.rules_v2_weights` (0.0) · **G3 cost
linearity: one (gross, turnover) pair prices every rung, 2.08e-17 against `engine` run
independently at 0/10/50 bps — this is what makes the 0 bps column the same draw with the
rebate switched off** · **G4 CROSS-RUN: SPY OOS reads 15.21% / 0.8713 / −33.72%, the record's
committed triple, to 0.0000 on all three, hence the DD cap −20.23% and CAGR floor 10.65%** ·
G5 null count and gross ≡ the book's (0 / 1.11e-16) · G6 determinism 0.0 · G7 rung-0 ≡ gross
stream 0.0.

## RESOLUTION AND SURVIVORSHIP

200 draws ⇒ a 0-of-200 rate is only distinguishable from a true rate below the rule-of-three
bound **0.0149**. Every `0.0000` above means "below 1.5%", not "impossible".

U56 and B136 are **current-constituent** lists (PROTOCOL rule 9), so every level here is
optimistic. The measured object is a *difference between cadences on the same panel and the
same draws*, where the bias largely cancels; where it does not, it works **against** this run's
own conclusion — survivorship lifts realised CAGR most where turnover is highest, which
flattens rather than creates the monthly peak.

## WHAT 1007 MAY STILL SAY / MAY NO LONGER SAY

**May still say:** the 10 bps profile `0.000 / 0.003 / 0.212 / 0.030` is right, and M is the
only cadence where `L5_CAGR` and `L4_DD` are jointly clearable *at 10 bps*.
**May no longer say:** that this is a fact about cadence. It is a fact about **10 bps**. The
"collapse at both ends" is one end (D, W) removed by cost and the other end (Q) removed by
drift, and only the second survives a zero-cost reading.

## PROPOSED (not applied — PROTOCOL rule 6 reserves rule changes to Sunday review)

> *"A base rate quoted for a cadence states its cost rung, because the cadence ranking of
> `base4b` INVERTS between 0 bps and 10 bps: at 0 bps it falls monotonically with holding
> period (0.459 / 0.449 / 0.308 / 0.040 at D/W/M/Q) and at 10 bps it peaks at M. A cadence
> claim read at one rung is a claim about that rung."*

**No RULES change, no book promoted, no KEEP claimed, no memo.** RULES.md, PROTOCOL.md,
scan.py, bot.py and baseline.py untouched.
