# PARK memo — ALWAYS-INVESTED EQUAL WEIGHT AT GROSS 0.65 (U56), idea 1695, lane cloud, 2026-09-20

**What it is.** No 200d moving average, no band, no ranking, no vol filter, no cash rule: hold every
instrument priced that day at 0.65/N of NAV, rebalance weekly, t+1, 10 bps. One dial (G), chosen by
the memo rule below. Script `research/backtests/2026-09-20_is-the-4b-CAGR-floor-the-only-leg-that-ever-binds_cloud.py`.

**Why it is here.** It clears PROTOCOL path 4b in **all five windows** — FULL, H1, H2, IS and OOS —
on U56: FULL CAGR 11.42% / Sharpe 1.1188 / MaxDD -19.75% (SPY 15.12% / 0.8844 / -33.72%; bars
CAGR >= 10.59%, MaxDD >= -20.23%, H1 > 0.9573, H2 > 0.8251). OOS 2017-2026, read once after a
chooser fit on <=2016-12-31: CAGR 11.83% / Sharpe 1.1269 / MaxDD -19.75%, against the live RULES v2
book's 9.46% / 1.2769 / -12.05% and SPY's 15.26% / 0.8738 / -33.72%. Turnover 0.73x/yr — a fifth of
the live book's 1.77x. Rule 8's C_MEMO chooser reaches it from the IS window alone.

**Exact RULES wording it would take.** *"Hold every instrument priced at the close at G/N of NAV,
N = instruments priced that day, G = 0.65. Rebalance weekly at the last close of each week, executed
at the next close. No eligibility test, no moving average, no ranking, no hard exit."*

**Why it is PARK and NOT KEEP.** (1) The feasible gross window is **exactly one rung wide at 0.05
resolution**: G=0.60 fails the CAGR floor on FULL, G=0.70 fails the DD cap. A book whose only
passing setting is a knife edge is a fitted number, not a rule. (2) It passes on **U56 alone** —
B136's no-gate feasible window is EMPTY at FULL and OOS, SMALL's is empty in all five windows.
(3) U56 is a current-constituent list and idea 1703 showed this week that its 4b pass is carried by
its 20 survivorship-selected mega-caps. (4) It fails path 4a at every window (Sharpe 1.1188 against
the live book's 1.2011, MaxDD -19.75% against -12.05%).

**What it is evidence FOR.** Idea 1699 (yesterday) concluded that an always-invested constant-gross
ladder clears 4b at 0 of 12 rungs because it is squeezed "with no rung in between". At 0.05
resolution there IS a rung in between on U56, and this is it. The squeeze is real; its emptiness
was a grid-resolution artefact. **No RULES change is proposed.**
