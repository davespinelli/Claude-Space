# Idea 1789 (lane C, 2026-09-20) — is the STALE-REFRESH PREFERENCE an IS-WINDOW fact or a REGIME fact?

**ANSWERED — IT IS AN IS-WINDOW FACT, AND THE CARRIER IS CRASH-PRESENCE, NOT RECENCY.
KILL of idea 1767's reading that legal IS-only choosers "cannot find the fresh scalar".
No new book, no rules change (PROTOCOL rule 6); the capital-relevant part of 1767's memo is
unaffected and, if anything, strengthened.**

Script: `research/backtests/2026-09-20_stale-refresh-is-window-or-regime_C.py`
Outputs: `.grid.csv` (384 book cells), `.choosers.csv` (288 joint + 1152 T-conditional + 288
truth rows), `.windows.csv`, `.truth.csv`, `.walkforward.csv`, `.gates.csv`, `.log.txt`.
**GATES 10 of 10 PASS**, including **G3 cross-run: window W0 reproduces idea 1767's published
chooser picks with 0 mismatches and max |Δ| 4.5e-05 on its OOS statistics** — the book, the
runner, the panels and the costs are 1767's, unchanged; only the chooser's visible window moves.

## The defect this closes
Idea 1767 found that on rule 8's fixed window every one of four legal IS-only choosers picked a
STALE gross scalar (R = M or Q) on 2009-2016 and then failed the 4b drawdown cap out of sample
(U56 t=0.16: all four pick T=Q,R=M, OOS MaxDD **−23.96%** against the memo's weekly **−19.86%**).
The record read that as a chooser defect. There is a cheaper explanation: a stale exposure scalar
only costs money **when vol spikes**, and 2009-2016 contains no drawdown deeper than the 2015-16
correction (SPY IS MaxDD −22.06%). If so the chooser is not blind — rule 8's window simply never
shows it the event that prices staleness.

## The headline (10 bps; JOINT = argmax over all 16 (T,R) cells; T-COND = argmax over R holding T)

| window | IS span | SPY IS MaxDD | JOINT stale | T-COND stale |
|---|---|---|---|---|
| W0 [SLID] | 2009-01..2016-12 (rule 8's own) | −22.06% | **19/24 = 79.2%** | 76/96 = 79.2% |
| W1 [SLID] | 2010-01..2017-12 | −18.61% | 18/24 = 75.0% | 72/96 = 75.0% |
| W2 [SLID] | 2011-01..2018-12 | −19.35% | 15/24 = 62.5% | 60/96 = 62.5% |
| W3 [SLID] | 2012-01..2019-12 | −19.35% | 10/24 = 41.7% | 44/96 = 45.8% |
| W4 [SLID] | 2013-01..2020-12 | **−33.72%** | **0/24 = 0.0%** | 2/96 = 2.1% |
| W5 [SLID] | 2014-01..2021-12 | **−33.72%** | **0/24 = 0.0%** | 0/96 = 0.0% |
| N1 [NAMED, the idea's own] | 2010-01..2018-12 | −19.35% | 15/24 = 62.5% | 60/96 = 62.5% |
| N2 [NAMED, the idea's own] | 2012-01..2020-12 | **−33.72%** | 1/24 = 4.2% | 3/96 = 3.1% |

IS length is held fixed at 8 years across the whole SLID family, so window LENGTH cannot carry
this. The stale share falls **monotonically** as the window slides, 79.2 → 75.0 → 62.5 → 41.7 →
0.0 → 0.0, and the collapse happens exactly where the 2020 crash enters the window. The two
windows the idea named behave the same way (N1 62.5%, N2 4.2%). Rank correlation of SPY IS MaxDD
with the stale share over the SLID family is **+0.638** (JOINT) / **+0.600** (T-COND) — quoted
descriptively only: the six windows overlap heavily, so no p-value is computable and none is
claimed.

## The control 2×2 — crash-presence, not recency
The slid family moves two things at once: as it slides forward it acquires the 2020 crash *and*
drops 2009-2012. Four control windows break the confound (lengths differ by construction and are
never pooled with SLID — read the 2×2, not the levels):

| | NO CRASH in IS | CRASH in IS |
|---|---|---|
| **EARLY** | X1 2009-2019 (11y), IS_DD −22.1%, stale **54.2%** | X2 2009-2020 (12y), IS_DD −33.7%, stale **4.2%** |
| **LATE** | X3 2013-2019 (7y), IS_DD −19.3%, stale **50.0%** | X4 2017-2020 (4y), IS_DD −33.7%, stale **0.0%** |

**Main effect of CRASH-PRESENCE −50.0 pp** (2.1% vs 52.1%); **main effect of RECENCY −4.2 pp**
(25.0% vs 29.2%). X1 → X2 adds **one year** to an eleven-year window and takes the stale share
from 54.2% to 4.2%; that one year is 2020. The carrier is the crash.

## Why the chooser behaves this way (the truth it is trying to see)
FRESH minus STALE, measured inside each window and after it (mean over panel × target × T):

| window | d(IS Sharpe) | d(IS MaxDD) | d(post Sharpe) | d(post MaxDD) |
|---|---|---|---|---|
| W0 | **−0.0003** | +0.23% | +0.0961 | +11.59% |
| W3 | +0.0036 | +2.24% | +0.1012 | +10.60% |
| W4 | **+0.1967** | **+12.23%** | −0.1011 | −2.07% |
| X4 | **+0.3267** | **+12.23%** | −0.1011 | −2.07% |

Inside a crash-free window the fresh scalar is worth **0.000 to 0.03 of Sharpe and 0.2-2.2 pp of
drawdown** — genuinely indistinguishable, so an argmax falls to the stale cell on noise and on the
turnover it saves. Inside a crash-containing window the same contrast is **+0.20 Sharpe and
+12.2 pp of drawdown**, and every chooser finds it immediately. The chooser was never blind; on
2009-2016 there was nothing to see. Symmetrically, and reported against our own reading: on the
*post*-2021 OOS spans (which contain no crash either) d(post Sharpe) turns **−0.10** — freshness
correctly stops paying there too. The preference tracks crash-presence in whichever sample it is
measured on, in **both** directions.

## Both KEEP paths (384 book cells, full sample + rule-8 OOS)
4b FULL **119/384**, 4b OOS **119/384**, 4b all five legs **119/384**, **4a 0/384** (4a is never
reached — the live book's −12.05% MaxDD is unreachable for a 0.12/0.16-target vol-scaled book).
Split by refresh class at 10 bps, pooled over panels, targets and T:

| R class | 4b | 4b OOS | 4a | mean OOS MaxDD |
|---|---|---|---|---|
| **FRESH (D/W)** | **32/48** | **32/48** | 0/48 | **−20.78%** |
| **STALE (M/Q)** | **0/48** | **0/48** | 0/48 | −32.37% |

The stale scalar clears 4b at **zero** cells. The binding leg is `L4_DD` everywhere on U56/B136
(32 and 41 of 64 failures) with `L5_CAGR` binding 0 times; SMALL clears nothing on any leg. So for
real capital the conclusion is unchanged and sharper than 1767 put it: **freshness is not a
preference, it is the whole 4b pass** — but the reason the rule-8 chooser misses it is the
window, not the statistic.

## Rule 8 walk-forward (PROTOCOL's own window: chosen on 2009-2016, 2017-2026 read once)
U56, live RULES v2 OOS 9.46% / 1.2766 / −12.05%; SPY OOS 15.26% / 0.8737 / −33.72%:
all 8 picks (4 choosers × 2 targets) land on T=Q,R=M [STALE], OOS **15.66% / 1.2979 / −20.83%**
(t=0.12) and **16.81% / 1.2184 / −23.96%** (t=0.16) — **0 of 8 clear 4b OOS, 0 clear 4a OOS**.
B136: 4 of 8 picks are FRESH and **all 4 clear 4b OOS** (best 15.63% / 1.2020 / −18.62%); the 4
stale picks clear nothing. SMALL: 7 of 8 stale, **0 of 8 clear anything** (OOS MaxDD to −40.18%).
Across all three panels **4 of 24** rule-8 picks clear 4b OOS, and every one of the four is a
FRESH pick. Under a window that contains a crash the same choosers pick FRESH essentially always
(W4/W5: 0/24 stale) — but their OOS spans are then 5.7y and 4.7y and contain no crash, which is
why their 4b pass counts (4/24 and 8/24) are **not** comparable to W0's and are not compared.

## Verdict
**ANSWERED / KILL** of 1767's chooser-blindness wording. No new book is proposed and **no rules
change** is made (PROTOCOL rule 6 — RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are
untouched). One item for the Sunday review, stated as a finding and not as a change: any claim of
the form "no legal IS-only chooser can reach X" that rests on rule 8's fixed 2009-2016 window is
untested against the possibility that the window simply does not contain the event that prices X,
and this run gives a cheap test for it — slide the IS window at fixed length and read whether the
argmax moves.

## Survivorship (PROTOCOL rule 9)
U56 / B136 are CURRENT-constituent lists and SMALL is a CURRENT sub-$2B screen (54 tickers with
`max_1d_move >= 1.0` dropped). Every CAGR and drawdown LEVEL is optimistic and both 4b bars are
easier here than on a point-in-time panel. The window-to-window contrasts that carry this finding
are same-tape, same-names, same-book comparisons with only the chooser's visible window moved and
are first-order immune; the pass COUNTS are not.
