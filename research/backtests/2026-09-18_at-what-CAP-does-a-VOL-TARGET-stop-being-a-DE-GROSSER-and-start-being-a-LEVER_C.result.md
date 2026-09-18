# Idea 1309 (lane C, 2026-09-18) — at what CAP does a VOL-TARGET stop being a DE-GROSSER and start being a LEVER?

**VERDICT: KILL (capital) for the levered cap — no RULES change, and no request to the Sunday
review to authorise leverage.** 194 of 194 gates pass; offline, deterministic, 22.4s.
RULES.md, PROTOCOL.md, scan.py, bot.py, baseline.py untouched.

**LEVERAGE IS DECLARED (PROTOCOL rule 2, which forbids it "unless the idea says so").** Queue
idea 1309 says so and this memo says so: every CAP above 0.60 is leverage relative to the
certified book, and above 1.00 the book borrows outright. Nothing here is a rules proposal.

**THE INSTRUMENT.** Idea 1297's scaler with its cap lifted: k_t = min(CAP, TARGET / v_t),
v_t = annualised sd of the BASIS book's daily returns over the 21 rows ending at t-1 (rule 2),
applied weekly to the certified incumbent (N=15 / H=126 / GROSS=0.60 / W, 10 bps). Two dials,
**CAP {0.60, 0.75, 1.00, 1.25, 1.50} x TARGET {8, 10, 12}%**, WINDOW frozen at 21 by the queue.
15 cells x 3 panels x 2 financing rungs, **all 90 published** (`.grid.csv`), plus the B_SELF
basis (`.robust.csv`, 90 more) and 12 rule-8 rows (`.walkforward.csv`). Cross-run replay gate
G8: the CAP=0.60 column reproduces idea 1297's committed WINDOW=21 cells (9 cells x 3 stats)
to < 5e-4. **TARGET is a nominal dial, not an achieved vol** — v is measured on the g=0.60
book, so every cell also publishes `vol_real`; read that column.

**FINANCING (the honesty arm, not a dial — both rungs published).** The record's runner charges
nothing for borrowed notional. FIN = 0 bps/yr is the headline (1297's convention); FIN = 200
bps/yr on max(0, exposure - 1) of NAV is reported at every cell. On the CAP >= 1.25 cells it
costs 0.03..0.67 pp of CAGR (mean 0.26) and 0.002..0.026 of Sharpe. **It changes no verdict**,
which is itself the finding: the levered rungs fail on drawdown, not on funding.

---

**1. THE CAP, NOT THE TARGET, WAS ALWAYS THE INSTRUMENT.** At CAP=0.60 the multiplier sits AT
the cap on 81-96% of U56 rows (75-94% B136, 55-90% SMALL); by CAP=1.50 that falls to 6-35%
(9-30%, 1-10%). The vol-target de-grosses only because its cap binds. Once lifted, it grosses:
U56 mean exposure runs 0.58 -> 0.90-1.21 across the CAP ladder.

**2. LIFTING THE CAP IS A PURE GROSS LEVER AND BUYS NO SHARPE.** Across all 15 U56 cells —
a 2.5x range of cap — CAGR runs **12.78% -> 25.71%** and MaxDD **-14.41% -> -24.49%**, while
Sharpe moves inside **1.1681..1.2077, a spread of 0.0397** (B136 0.0249, SMALL 0.0434). rho(mean
k, CAGR) = +0.996 / +0.981 / +0.963 on U56 / B136 / SMALL; rho(mean k, Sharpe) = +0.62 / **-0.20**
/ +0.07, i.e. not even consistent in sign. Return and drawdown scale together with gross; the
scaler adds nothing a flat gross rung would not. Turnover, however, is not free: U56 annual
turnover runs 2.57 -> 7.92 from CAP 0.60 to 1.50 (3.1x) for that flat Sharpe.

**3. THE 4b DRAWDOWN LEG DIES EXACTLY WHERE THE LEVER STARTS — the queue's question, answered.**
Against the 4b cap of -20.23% (0.60 x SPY's -33.72%), the DD leg passes **3/3 cells at CAP=0.60
and 3/3 at CAP=0.75, then 2/3 at 1.00, 1/3 at 1.25 and 1/3 at 1.50** on U56 and identically on
B136. **The first breach is CAP=1.00 / TARGET=12% on both panels** (U56 -21.57% at mean exposure
0.944; B136 -20.66% at 0.917) — i.e. the leg breaks as mean exposure approaches 1, BEFORE the
book borrows a dollar. On SMALL, where idea 1215's binder really binds, the leg passes **0 of 15
at every cap and both financing rungs** and gets monotonically worse: -26.80% at CAP 0.60 to
**-43.29%** at CAP 1.50, against a -20.23% cap. 4a passes **0 of 45** everywhere (the live RULES
v2 book's -12.05% MaxDD is tighter than every cell).

**4. RULE 8 (2017-2026 READ ONCE), (CAP, TARGET) by argmax IS Sharpe on warm-up..2016-12-31.**
The headline B_CONST chooser picks **U56 CAP=1.00/12%, B136 CAP=0.75/8%, SMALL CAP=0.75/8%**,
identical at both financing rungs. It clears every 4b leg incl. the OOS Sharpe leg on **1 of 3
panels**; mean OOS Sharpe vs the incumbent **-0.0385** for +1.19 pp of OOS CAGR. U56's pick is
the single richest cell the IS window offers and it **fails 4b's DD leg in and out of sample**
(OOS 22.07% / 1.2174 / **-21.57%** vs incumbent 15.12% / 1.1947 / -16.38% and SPY 15.28% /
0.8747 / -33.72%): the chooser walks straight into the breach. B136's surviving pick is
**worse than the flat incumbent out of sample** (12.81% / 1.0047 / -14.61% vs 14.11% / 1.0454 /
-15.97%). SMALL's fails every leg (4.20% / 0.3643 / -28.53%).

**5. THE ROBUSTNESS BASIS ANSWERS THE TITLE QUESTION DIFFERENTLY, AND THAT IS THE RESULT.** On
B_SELF (v from the scaled book's own returns) the loop is self-limiting: raising CAP from 1.00
to 1.50 moves U56 mean k only 0.7175 -> 0.7242 (TARGET 8%) and leaves MaxDD pinned at -15.91%,
so **the cap never becomes a lever at all** — B_SELF passes 4b 3/3 at every cap on U56 and B136
(30 of 45 overall) and 0/15 on SMALL. But it buys nothing either: U56 Sharpe falls monotonically
in the cap at every target (12%: 1.1738 -> 1.1401), paying turnover for gross the feedback then
refuses to take. **"At what CAP does it become a lever" has no basis-free answer**: on B_CONST
the answer is CAP >= 1.00; on B_SELF, never.

**6. WHAT A READER SHOULD TAKE.** The one un-levered rung that looks attractive — CAP=0.75,
which passes 4b 3/3 on U56 and B136 at +1.18..+2.81 pp of CAGR over the incumbent at equal
Sharpe — is **not claimed as a KEEP here**: the headline chooser does not pick it on U56, where
it is picked it is worse than the incumbent OOS, and a flat gross bump from 0.60 to 0.75 is the
record's existing GROSS axis, not this run's instrument. This run's own instrument, the levered
cap, is KILLED: it converts drawdown into return one-for-one, breaks the modal 4b binder at
mean exposure ~0.94, and its Sharpe is flat to 0.04 over a 2.5x range of gross.

**PANELS / SURVIVORSHIP (rule 9).** U56 55 names (2008-01-02..2026-09-17, 18.7y), B136 135
(18.7y), SMALL 664 of 715 priced (2010-01-04..2026-09-11, 16.7y). B136 and SMALL are CURRENT
constituents only; their levels are biased upward and their drawdowns downward.

**GATES (194/194).** G0 sample >= 10y. G1 U56 incumbent replays idea 1215's committed
13.66%/1.1706/-16.38%. G2 degenerate TARGET=1000% at CAP=0.60 reproduces the incumbent
bit-exactly on all three panels. G3 live RULES v2 U56 MaxDD == the committed -12.05%. G4
causality: k_t unmoved by perturbing the tape at/after the probe row. G5/G6 IS and OOS disjoint,
OOS starts 2017-01-01. G7 (x180) k never exceeds its CAP. **G8 the CAP=0.60 column replays idea
1297's committed cells to < 5e-4.** G9 FIN=200 never raises a cell's CAGR. G10 no cell borrows
at CAP <= 1.00.
