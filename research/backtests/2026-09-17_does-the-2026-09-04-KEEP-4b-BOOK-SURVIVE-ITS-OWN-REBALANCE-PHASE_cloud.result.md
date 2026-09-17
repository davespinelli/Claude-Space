# Idea 1253 (lane cloud, 2026-09-17) — does the 2026-09-04 KEEP 4b book survive its own REBALANCE PHASE?

**VERDICT: KILL (capital) — no new book. But the standing 4b pass is PHASE-CONTINGENT, and the
phase is a dial the record never stated.**

## What was run
The frozen 2026-09-04 candidate (U56 / 3-leg composite 21-252, 0-126, 0-63 / **no vol scaler** /
above-own-200d and vol20 < 0.60 / top **N=20** equal weight / min hold **H=126** / **gross 0.75**
of NAV, gated-out weight to CASH), 10 bps, decide-at-t / apply-at-t+1, 260-row warm-up, rebuilt at
**every rebalance phase** on three panels: a fixed 5-trading-day stride (5 phases), a fixed
21-trading-day stride (21 phases), and the **WEEKDAY family** — one rebalance per calendar week on
the trading day whose weekday is Mon..Fri (or that week's last trading day on or before it), which
is the literal question an implementer asks. **99 grid points, all published** in `.grid.csv`;
9 rule-8 rows in `.walkforward.csv`. Dials: CYCLE {P5, P21, WD} x PHASE. 11 of 11 gates pass, 11s,
offline, deterministic.

**G9: the WEEKDAY-MONDAY book reproduces the committed calendar-weekly anchor to 0.000e+00.** The
record's "weekly" book is the **Monday-execution** book (decide Friday close, trade Monday), and
this run therefore prices the committed number itself, not a near relative.

## The numbers (U56, the panel the candidate lives on)
Benchmarks on the identical window (2009-01-13..2026-09-16): **SPY 15.06% / 0.8815 / -33.72%,
halves 0.9600/0.8171, OOS 15.15% / 0.8686 / -33.72%. LIVE RULES v2 8.60% / 1.1982 / -12.05%,
OOS 9.42% / 1.2717.** 4b's drawdown cap is therefore **0.60 x -33.72% = -20.23%**.

| U56 book | full CAGR / Sharpe / MaxDD | halves | OOS CAGR / Sharpe / MaxDD | 4b |
|---|---|---|---|---|
| WD **Mon** (= the committed anchor) | 15.71% / 1.1480 / **-19.13%** | 1.2127 / 1.1050 | 17.16% / 1.1759 / -19.13% | **PASS** |
| WD Tue | 15.12% / 1.0986 / -21.31% | 1.1856 / 1.0403 | 16.57% / 1.1212 / -21.31% | fail (DD) |
| WD Wed | 15.48% / 1.1236 / -20.30% | 1.1858 / 1.0865 | 17.47% / 1.1732 / -20.30% | fail (DD) |
| WD **Thu** | 15.48% / 1.1351 / **-19.45%** | 1.2168 / 1.0764 | 16.58% / 1.1463 / -19.45% | **PASS** |
| WD Fri | 15.25% / 1.1042 / -21.00% | 1.2382 / 1.0101 | 16.09% / 1.0868 / -21.00% | fail (DD) |
| P5 strides (5 phases) | Sharpe 1.0568..1.1609 | — | OOS Sharpe 1.0201..1.1687 | **0 of 5** |
| P21 strides (21 phases) | Sharpe 1.0144..1.1644 | — | OOS Sharpe 1.0127..1.2196 | **0 of 21** |

**4b passes: WD 2 of 5, P5 0 of 5, P21 0 of 21 on U56; 0 of 31 on B136; 0 of 31 on SMALL663.**
4a passes **0 of 99** everywhere — live v2's -12.05% MaxDD is not beatable by a growth book, which
is rule 4b's own stated reason for existing.

## The finding, in one line
**The book's RETURN is phase-robust and its VERDICT is not.** On U56 the H1, H2, OOS-Sharpe and
CAGR legs of 4b pass at **31 of 31** phase books — every phase beats SPY in both halves and out of
sample (OOS Sharpe 1.0127..1.2196 against SPY's 0.8686). **The only leg that ever fails is the
drawdown cap, and it fails at 29 of 31.** The committed -19.13% clears the -20.23% bar by 1.10 pp;
moving execution one weekday costs up to **2.18 pp of MaxDD**, i.e. the unstated phase dial is
**twice the margin the pass was won by**. B136 fails the DD leg at 31 of 31 and SMALL663 fails
every leg at 31 of 31.

## Rule 8 (phase chosen on warm-up..2016-12-31 only, 2017-2026 read once)
Choosing the phase in sample is **worth negative money**: pooled over 3 panels the IS-argmax phase
returns mean OOS Sharpe **0.8122 vs 0.8197 for the phase mean (-0.0075) at P5** and **0.8822 vs
0.8975 (-0.0153) at P21**. On U56's weekday family the IS argmax is **Friday**, whose OOS Sharpe
1.0868 is the **worst of the five** against the anchor's 1.1759, with IS/OOS rank correlation
**-0.50**. Rank correlations across the nine rule-8 rows run -0.80 to +0.60 with no sign. **The
phase carries no selection information; its spread is pure risk an implementer must eat.**

## What this does and does not say
It does **not** produce a new book, and it does not refute the candidate's edge: its Sharpe and
CAGR advantage over SPY survives every phase tested on U56. It does say the committed **4b verdict
was won on the one leg that the dial moves**, so "the 2026-09-04 book passes 4b" is more precisely
"the Monday-execution book passes 4b, the Tuesday, Wednesday and Friday ones miss the drawdown cap
by 0.07-1.08 pp." **PROPOSED for the Sunday review (rule 6) as wording only, never as a chooser:
a published 4b pass whose binding leg is MaxDD should state its execution phase and the pass count
over that phase's own family.** RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py untouched.

## Survivorship (rule 9)
U56 and B136 are current-constituent lists; SMALL663 is a current sub-$2B screen (52 of 715 names
dropped for `max_1d_move >= 1.0` before anything was computed). Every level printed is optimistic
and every 4b pass is an upper bound. The headline is a spread across phases of the same book on the
same panel, which is first-order immune to a common level bias; the levels are not.
