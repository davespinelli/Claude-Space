# Idea 2266 — does the DD-budgeted IS-only chooser generalise to a dial that is NOT gross?

**Lane B, 2026-09-22. ANSWERED = NO. KILL of the device as a METHOD (it survives only on the one
dial where it has no free content). No RULES change.**

Script `2026-09-22_dd-budget-chooser-off-the-gross-dial_B.py`; data `.grid.csv` (610 book cells),
`.choosers.csv` (1,260 chooser cells), console `.console.txt`. 114 zero-cost simulations; every
cost rung derived exactly (gate G2, 0.0 at 1e-15).

## What was asked
Idea 2264 fixed the record's "not rule-8 reachable" verdict on its only reliable 4b passer by
matching the chooser to the binding leg: take the largest GROSS whose IS (2009–2016) MaxDD stays
inside `kappa x IS SPY MaxDD`. It reached the 4b cell at 9 of 10 panel × cost cells. But on gross
that rule has no free content — IS MaxDD is monotone in g, so under PROTOCOL rule 2's no-leverage
cap it degenerates to "take the largest legal gross". 2266 asks what the device does on a dial
where the budget must actually choose.

## The three dials (all walked on the LIVE RULES v2 band book, weekly, t+1, 10 bps headline)
| dial | ladder | incumbent | IS MaxDD monotone? |
|---|---|---|---|
| GROSS (control, 2264's own) | 0.250 … 1.500 step 0.125 | 0.75 | **YES** (gate G6, both panels) |
| BAND width `b` | 0.00 0.01 0.02 0.03 0.05 0.08 0.12 0.16 0.20 0.30 0.40 | 0.03 | **NO** |
| TOPN `N` by composite rank inside the band, gross/N, idle NAV to cash | 5 10 15 20 30 40 ALL | ALL | **NO** |

TOPN is published twice: arm **P** (plain, gross/N — deploys more gross than ALL) and arm **M**
(each finite-N rung rescaled to the ALL book's IS-window mean deployed gross, an IS-only constant,
de-grossing only), because at finite N the plain rung is partly a gross dial and that is the very
confound 2264 saturated.

Choosers, all IS-only on 2009–2016: `C_DDB_CAGR(kappa)` (feasible set = IS MaxDD inside
`kappa x IS SPY MaxDD`, argmax IS CAGR — **gate G4: on the gross dial this reproduces 2264's
largest-gross rule at 70 of 70 cells**), `C_DDB_SHARPE(kappa)` (same set, argmax IS Sharpe — idea
960's reading), `C_SHARPE`, `C_CALMAR`, `C_LIVE` (the shipped rung, a no-information control) and
an illegal `ORACLE_OOS` published only as the regret yardstick. kappa ∈ {0.40…1.00}.
Two tuned dials and no more: **kappa and the dial value**. Panel, gross rung, cost rung, cadence
and the 3% live band are reported axes, never selected on.

## 1. The premise holds: the budget saturates GROSS and does not saturate the other two
`C_DDB_CAGR`'s pick sits at the ladder end at **48.6%** of gross cells, **3.6%** of band cells and
**19.0%** of top-n cells; the budget moves the pick off its own budget-free argmax (i.e. actually
binds) at **51.4% / 21.4% / 78.3%**. Gate G6 measures the mechanism directly: IS MaxDD is monotone
in gross on both panels (max Δ −0.0125) and is non-monotone on every band and top-n ladder
(max Δ up to +0.0993).

## 2. Off gross, the device's content collapses into its TIE-BREAK — an undeclared third parameter
The two equally defensible readings of "the same rule" agree on **100% of gross picks at
kappa ≤ 0.70** (80% above) and on only **5–40% of band picks** and **40–95% of top-n picks**. They
do not merely differ in detail; they reverse the verdict: on BAND, `C_DDB_CAGR0.60` reaches 4b-OOS
at 9 of 20 cells while `C_DDB_SHARPE0.60` reaches 4 — and pooled over all kappa, 54 of 140 vs 20 of
140 against the incumbent's 42. A rule whose answer depends on a dial nobody declared is not a
method.

## 3. Against DOING NOTHING, the device buys nothing off gross (rule 8, 2017–2026 read once)
Pooled over every panel × gross-rung × cost cell and every kappa, versus `C_LIVE`:

| dial | tie-break | n | OOS Sharpe win rate | ΔOOS Sharpe (med) | ΔOOS MaxDD | ΔOOS CAGR | 4b-OOS reach vs live |
|---|---|---|---|---|---|---|---|
| GROSS | CAGR | 70 | 1.4% | −0.0026 | −9.70 pp | **+6.84 pp** | **15 vs 0** |
| GROSS | Sharpe | 70 | 1.4% | −0.0020 | −9.50 pp | +6.54 pp | **18 vs 0** |
| BAND | CAGR | 140 | 12.1% | −0.0399 | −0.15 pp | −0.17 pp | 54 vs 42 |
| BAND | Sharpe | 140 | 24.3% | −0.0210 | +4.78 pp | −2.39 pp | **20 vs 42** |
| TOPN | CAGR | 258 | **0.4%** | **−0.2141** | −8.80 pp | +4.90 pp | **36 vs 70** |
| TOPN | Sharpe | 258 | 0.8% | −0.0473 | −3.12 pp | +3.61 pp | 66 vs 70 |

On gross the trade is coherent and is exactly 2264's: spend 9.7 pp of OOS drawdown inside the
budget, collect 6.8 pp of OOS CAGR, clear the CAGR floor that idea 2270 identified as the binding
leg, and pay ~0.003 of OOS Sharpe. **Off gross the same trade stops paying**: on the top-n dial the
device buys 8.8 pp more drawdown for 4.9 pp of CAGR and gives up 0.21 of OOS Sharpe, losing to the
no-information incumbent at 99.6% of cells and destroying 34 of the incumbent's 70 4b-OOS passes.
Median regret against the OOS oracle: `C_LIVE` −0.0156 (BAND) / **0.0000** (TOPN) against
`C_DDB_CAGR0.60`'s −0.0699 / −0.1890. On the top-n dial **the incumbent IS the OOS-optimal rung.**

The cleanest single cell (u56, arm M, gross 1.00): `C_LIVE` picks ALL and clears 4b-OOS at all five
cost rungs; `C_DDB_CAGR` picks N = 5 or 10 at kappa ≥ 0.80 and clears at none.

## 4. kappa does not transfer either
Best kappa by 4b-OOS reach: GROSS **0.60** (9 of 10), BAND 0.60–1.00 (9 of 20), TOPN **0.50** (21 of
40) — at TOPN the value 2264 shipped (0.60, PROTOCOL 4b's own delta) delivers 8 and kappa = 0.40
abstains at 20 of 40 cells. The device therefore carries two free parameters off gross (kappa and
the tie-break) where it carried none on gross.

## 5. KEEP paths — nothing recommended
Book census over all 610 published cells: **4a 12** (all BAND, all at the ladder-end b = 0.40, a
grid-edge flag; mean deployed gross 0.131–0.234, i.e. the record's known "every 4a pass is a
de-gross" law again — they miss 4b's CAGR floor by 3.38–5.77 pp), 4b FULL 162, 4b OOS 174, **4b
FULL+OOS 142** across 22 distinct books.
**Recorded, NOT recommended (KEEP-4b candidate, by-product):** the gross-matched top-n book
(u56, arm M, gross rung 1.00 = mean deployed gross 0.7042, N = 40, weekly) @10 bps FULL
**12.16% / 1.1997 / −16.90%**, halves 1.2413 / 1.1722, OOS **13.58% / 1.2650 / −16.90%**, turnover
3.83x/yr — against the standing candidate's 11.53% / 1.2009 / −15.91%, OOS 12.67% / 1.2760 /
−15.91% at 2.35x/yr. It buys +0.91 pp of OOS CAGR for 0.99 pp of drawdown, 1.63x the turnover and
0.011 of OOS Sharpe, and it is **NOT rule-8 reachable**: no legal chooser on the grid picks N = 40
at 10 bps (they pick 5, 10, 15 or ALL). 4a is 0 of 280 on the top-n dial.

## Caveats carried
Survivorship (PROTOCOL rule 9): u56/b136 are current constituents held from 2008, so every CAGR
level is optimistic and both 4b level legs are easier than on a point-in-time panel. Flat costs, no
spread/impact/borrow. One cadence (W), one delay (t+1). The IS window is flattered by tape order
(IS SPY MaxDD −22.06% is shallower than OOS SPY's −33.72%), so an IS drawdown budget is
automatically conservative out of sample — 2264 flagged this and it applies here unchanged; it
makes the device look BETTER than it is, which strengthens the KILL.
