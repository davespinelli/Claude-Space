# Idea 2231 — does a NO-TRADE BAND on the IDLE-NAV SLEEVE make the accounting fix 4a-ADOPTABLE?
lane B, 2026-09-22. Script `2026-09-22_lazy-idle-nav-sleeve_B.py`; every grid point in `.grid.csv`
(220 published rows = 2 panels x 22 books x 5 cost rungs x 3 windows), gates in `.gates.csv`,
walk-forward in `.walkforward.csv`, full console in `.log.txt`.

**ANSWER: YES ON THE PANEL THE BOOK LIVES ON, AND THE LAZINESS IS FREE — IT RETAINS ~103% OF THE
GAIN FOR ~64% OF THE TURNOVER LIFT.** Idea 2213(B) ruled the idle-NAV accounting fix (idle NAV ->
SHY, phi = 0) non-adoptable for exactly one reason: it lifts turnover 1.77x -> 2.80x/yr and so
fails 4a at 50 bps, while RULES v2's acceptance record holds at 5/10/25/50. Putting a no-trade
tolerance `h` on the sleeve leg alone repairs that on U56 and only that: **4a holds at 0 / 5 / 10 /
25 / 50 bps for every h >= 0.05 on U56** (h = 0.00/0.01/0.02 still fail at 50, exactly as 2213
found), and **on B136 only h = 0.50 reaches the 50 bps rung**. At the protocol's own 10 bps rung
4a passes on BOTH panels at all seven h.

## A. The laziness is not a trade-off — it DOMINATES the eager sweep on both panels
10 bps, FULL, phi = 0.00, against the live RULES v2 book (U56 8.62% / 1.2010 / -12.05%, 1.77x/yr;
B136 7.96% / 1.0972 / -12.24%, 2.01x/yr):

| h | U56 dCAGR | U56 dSharpe | U56 turn | B136 dCAGR | B136 dSharpe | B136 turn | gain retained (U56/B136) | lift retained |
|---|---|---|---|---|---|---|---|---|
| 0.00 (eager, = 2213) | +0.50 pp | +0.0663 | 2.80x | +0.52 pp | +0.0697 | 3.04x | 100% / 100% | 100% / 100% |
| 0.05 | +0.51 pp | +0.0681 | 2.56x | +0.53 pp | +0.0719 | 2.81x | 102.6% / 103.1% | 76.4% / 78.0% |
| **0.10** | **+0.52 pp** | **+0.0682** | **2.43x** | **+0.54 pp** | **+0.0732** | **2.68x** | **102.8% / 105.0%** | **63.7% / 65.3%** |
| 0.20 | +0.49 pp | +0.0652 | 2.24x | +0.53 pp | +0.0714 | 2.49x | 98.3% / 102.4% | 45.7% / 46.3% |
| 0.50 | +0.47 pp | +0.0617 | 2.14x | +0.44 pp | +0.0595 | 2.33x | 93.0% / 85.3% | 35.3% / 31.6% |

At h = 0.10 the sleeve is still funded at 44.6% / 44.5% of NAV against the eager 46.7% / 46.8%:
95% of the allocation is kept, a third of the churn is not. The gain-retained column exceeding
100% is not noise-free precision, it is the mechanical fact that the trades the tolerance skips
were cost with no tracking benefit.

## B. The 4a leg that binds, and where it stops binding (50 bps, FULL, phi = 0.00)
The eager sweep's 50 bps failure is an **H1 Sharpe** failure, and h fixes it by giving back cost:
U56 dSharpe H1 runs **-0.0126 -> -0.0095 -> -0.0049 -> +0.0027 -> +0.0122 -> +0.0240 -> +0.0228**
across h = 0.00..0.50, crossing zero between h = 0.02 and h = 0.05. On B136 the H1 leg crosses at
the same place (+0.0045 at h = 0.05) but the **MaxDD leg** then binds instead — dMaxDD stays
NEGATIVE (-0.71 / -0.52 / -0.38 / -0.09 pp) until h = 0.50 turns it +0.40 pp. So the repair is
real on both panels and complete on one. 4a over all 21 sleeve cells: **7 of 21 per panel at 0, 5,
10 and 25 bps** (all seven are phi = 0.00), **4 of 21 on U56 and 1 of 21 on B136 at 50 bps**.

## C. RULE 8 WALK-FORWARD, 2017-2026 READ ONCE — the two legal IS-only choosers AGREE ACROSS PANELS
Dials fit on warm-up..2016-12-31 only. At 10 bps, **C_SHARPE (argmax IS Sharpe) and C_4aIS (argmax
IS Sharpe among IS-4a passers) both pick phi = 0.00 / h = 0.10 on U56 AND on B136** — the same cell
on two panels, from two different objectives:

| | OOS CAGR | OOS Sharpe | OOS MaxDD | turn | 4a OOS | 4b OOS |
|---|---|---|---|---|---|---|
| U56 pick (phi 0, h 0.10) | **10.15%** | **1.3577** | **-11.53%** | 2.41x | **TRUE** | FALSE |
| U56 live RULES v2 | 9.46% | 1.2767 | -12.05% | 1.79x | — | FALSE |
| B136 pick (phi 0, h 0.10) | **8.61%** | **1.1955** | **-11.68%** | 2.76x | **TRUE** | FALSE |
| B136 live RULES v2 | 7.85% | 1.1017 | -12.24% | 2.10x | — | FALSE |
| SPY OOS | 15.29% / 15.26% | 0.8751 / 0.8737 | -33.72% | — | — | — |

The pick beats the live book on **all three** of CAGR, Sharpe and MaxDD out of sample on both
panels, and does so on the untouched window. C_ANCHOR (change nothing) is the live book itself.
At 50 bps the choosers scatter (U56 C_SHARPE moves to phi = 0.25 / h = 0.10, B136 to phi = 0.25 /
h = 0.20) and **0 of 4 picks pass 4a**, so the adoptable region is a 10-25 bps region, not a
50 bps one, even on U56.

## D. 4b: KILL at phi = 0, on the CAGR floor alone — the record's umpteenth 4a/4b disjunction
phi = 0.00 is **0 of 35 on 4b in every window at every rung**, and the leg is always CAGR:
U56 OOS 10.15% against a 10.70% floor (**-0.55 pp**), B136 OOS 8.61% against 10.68% (-2.07 pp),
while the DD cap is cleared by 8.7 pp and both Sharpe halves beat SPY by 0.28-0.67. The 4b passers
in this run are all phi >= 0.25 (34 cells at phi = 0.25, 11 at phi = 0.50), i.e. books that buy the
CAGR with SPY beta — and **not one of them passes 4a**. One honest oddity, reported not
recommended: at the **50 bps** rung on U56 the C_SHARPE chooser picks phi = 0.25 / h = 0.10 and it
clears 4b OOS (10.84% / 1.1660 / -15.73%) while failing 4b in FULL and IS — one panel, one rung,
one window, so it is a coincidence until a second panel says otherwise.

## E. Gates — 12 of 12, printed before any hypothesis was read
G1 the eager (h = 0) runner reproduces `engine.backtest` on the explicit augmented weights to
**1.4e-17 (returns) / 1.1e-15 (turnover)** on U56 and 2.1e-17 / 1.8e-15 on B136; G2 max total
weight **1.000000** at every (phi, h) — never levered, never short; G4 the derived 25 bps rung
equals a fresh 25 bps engine run to **1.4e-17** (the cost axis is an exact identity, not an
interpolation); G5 the NOSLEEVE control equals `baseline.rules_v2_weights` at **0.000e+00** — the
ladder literally contains the live book; G6 17.65 years of sample per panel.

## F. What this run cannot do, stated not repaired
One cadence (weekly), one band (the live 0.03), one gross (the live 0.75), one weekday offset
(d = 0 — the 5-offset spread that ideas 914/2111 make binding was NOT measured here), one sleeve
composition family. SPY and SHY are also gated universe names, so the sleeve ADDS to any core
holding of them and its legs are charged as separate lines: turnover here is an **upper bound**,
never flattering. **SHY is a real allocation with real duration risk** — FULL CAGR 1.31%, MaxDD
-5.71%, **2022 -3.88%**, and its contribution is regime-bound (IS CAGR 0.81% vs OOS 1.72%), so a
forward-looking version of this book is not the object this backtest prices. **SURVIVORSHIP
(rule 9):** U56 and B136 are current-constituent lists; every absolute level is optimistic and the
lazy-vs-eager contrast is within-tape, which does not repair the level.
