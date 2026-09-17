# Idea 1261 — is ALWAYS-ACT the DEFAULT the record never declared and cannot afford?  **KILL**

Run 2026-09-17, lane cloud, idea 2 of 2. Script:
`research/backtests/2026-09-17_is-ALWAYS-ACT-the-DEFAULT-the-record-never-declared-and-cannot-afford_cloud.py`
Grid: 4 ladders (N, GROSS, CADENCE, MOM around the frozen 2026-09-04 book) x 3 panels (U56, B136,
SMALL431) = 12 cells, 4 selectors each, costed and switch-free = 96 rows, all in `.cells.csv`.
2 tuned params only (ladder, panel). Decisions at 14 year-end folds on a strictly trailing
expanding window; ANCHOR_R8 pinned on warm-up..2016-12-30 with 2017-2026 read once.
Every selector is realised as one stitched daily return stream an account could hold; a switch is
charged |w_new - w_old| x 10 bps on the switch date from the two books' actual drifted weights.

## The headline: 1252's two facts are different books averaging. Neither reproduces at book level.

| over the 12 cells, costed | ALWAYS_ACT | ANCHOR | INCUMBENT |
|---|---|---|---|
| mean full-sample Sharpe | **0.9862** | 0.9987 | 0.9958 |
| mean OOS Sharpe (2017-2026) | **0.9384** | 0.9391 | 0.9355 |
| AA minus comparand, OOS | — | **-0.0006** (wins 2/12) | **+0.0030** (wins 6/12) |
| 4b passes | 2/12 | 1/12 | 3/12 |
| 4a passes | 0/12 | 0/12 | 0/12 |

1252 reported ALWAYS-ACT at +0.0089 OOS Sharpe over do-nothing and a 4b collapse of 24 -> 6. Held
as a book, the gain shrinks to **+0.0030 against the incumbent and turns negative (-0.0006) against
the anchor**, and the collapse does not happen at all: ALWAYS_ACT carries 2 of 12 4b passes against
the anchor's 1 and the incumbent's 3. The pooled decision average and the realised book are not
measuring the same object — the pooled figure averages over decisions, most of which are no-ops.

## Why: on 7 of 12 cells ALWAYS-ACT never acts, and where it acts it loses 4 times in 5

Switch counts: U56/GROSS 11, U56/N 4, B136/N 4, SMALL/N 2, SMALL/GROSS 2, and **0 on all seven
remaining cells** — the IS argmax never moves on any CADENCE or MOM ladder, on any panel. On those
cells ALWAYS_ACT is bit-identical to ANCHOR. Of the five cells where it does act, it beats the
anchor's full-sample Sharpe in one (B136/N, +0.0515) and loses in four, worst U56/N at -0.1170 and
U56/GROSS at -0.1112.

U56/GROSS is the clean indictment. The picks run G0.40, G0.70, G1.00, G1.00, G0.70, G1.00, G0.80,
G0.90, G0.40, G0.40, G0.60, G0.70, G0.50, G0.70 — 11 switches on a ladder idea 1193 measured the
same day as Sharpe-degenerate (rung spread 0.0009 = **0.08% of its own mean** at cash 0). The
selector is resolving noise of order 1e-3 and paying for it in the dimension the ladder actually
moves: full-sample Sharpe 1.1399 against the anchor's 1.2511, and **MaxDD -23.00% against -10.68%**.

## The switch charge is real but is NOT the mechanism

Sharpe cost of charging switches: -0.0021 (U56/N, 4 switches), -0.0015 (U56/GROSS, 11), -0.0018
(B136/N, 4), -0.0003 (SMALL/N, 2), -0.0006 (SMALL/GROSS, 2); OOS -0.0004 to -0.0016. At an annual
decision cadence the trade itself is cheap. ALWAYS-ACT loses because of *which* rung it picks, not
because of what the switch costs — so 1236's turnover-rebate concern does not explain this result
and cannot rescue it either.

## The one cell that passes 4b, stated with its margin

B136 / N ladder, ALWAYS_ACT: CAGR 14.53%, Sharpe 1.0514, MaxDD **-19.87%**, halves 1.091 / 1.011,
OOS CAGR 12.82% / Sharpe 0.9358 / MaxDD -19.87% (SPY OOS 15.33% / 0.877 / -33.72%; RULES v2 OOS
7.88% / 1.106 / -12.24%). All five 4b legs pass. The anchor and the incumbent on the same cell fail
on the DD leg alone (-24.00%). The 4b DD cap is -20.23%, so **the entire pass is 0.36pp of
drawdown margin** — the same boundary idea 1257 found decided at 3.6e-05 and idea 1193 found
pinching the incumbent's own gross between rungs 0.70 and 0.80. It is 1 of 12 cells, selected by
both tuned params, on the panel with the strongest survivorship caveat. **PARK, not KEEP** — it
does not change any rule, and nothing here justifies replacing the live book.

## Answer to the question as posed
The Sharpe gain and the 4b loss cannot both be true of one book, because at book level neither is
true. ALWAYS-ACT is not a default the record cannot afford; on this tape it is a default that is
mostly inert (7/12 cells), mildly harmful when it fires (4 losses in 5), and not chargeable to its
own trading costs. Declaring it would change almost nothing and would cost -0.012 mean Sharpe where
it changed anything.

## Caveats
Survivorship: U56, B136 and SMALL431 are all current constituents; SMALL431 = the 483-name sub-$2B
panel with the 52 tickers whose max 1-day move >= 100% dropped per `data/small_meta.csv`, and its
own SPY column is a benchmark, not a constituent. Folds are calendar year-ends (14 decisions); a
different fold cadence is a third dial and was not walked. IS argmax ties break to ladder order.
