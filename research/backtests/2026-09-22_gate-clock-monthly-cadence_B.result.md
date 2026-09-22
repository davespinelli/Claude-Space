# Idea 2276 — does the GATE CLOCK matter at the MONTHLY cadence too?
**Lane B, 2026-09-22. ANSWERED = NO. KILL of the gate-clock family on a SECOND, independent book.
One 4b-clearing, drawdown-improving cell is RECORDED AND NOT RECOMMENDED (rule-8 unreachable).
4a 0 of 480. NO RULES CHANGE.**

Script `2026-09-22_gate-clock-monthly-cadence_B.py`; outputs `.grid.csv` (480 rows),
`.walkforward.csv` (80 chooser rows), `.pairs.csv` (400 matched pairs), `.ddcells.csv`,
`.gates.csv`, `.console.txt`. Deterministic, offline, 22s.

## What was priced
Idea 182's R6 top-20 monthly book — the record's standing monthly 4b candidate — with **only the
MA gate's SAMPLING CLOCK moved**. Its eligibility clause is `px > px.rolling(200).mean()`,
recomputed every session, while clause 5 trades MONTHLY: the gate is sampled **21x finer than it
is ever executed**. Idea 2284 priced this mismatch at the WEEKLY cadence on the RULES v2 band book
and killed it; idea 2280 then showed the contrast is not a turnover rebate. 2276 asks the question
neither answered — both moved the clock at the FAST trading clock, and the premise is that a
coarser gate should be worth **MORE** at the slow one, where the stale-state window is 4x longer.

**Two tuned dials and no more: L (MA length in MONTHLY bars) ∈ {5,7,10,13,16} and the band
half-width c ∈ {0.00, 0.02, 0.03, 0.05, 0.08}.** L = 10 months (~210 sessions) is the monthly twin
of the live 200 days; c = 0.00 is idea 182's literal clause (a bare above/below test). Reported,
never selected on: panel {U56, B136}, **trading cadence {M (live), W}** — the contrast that answers
the premise same-tape — cost rung {0,10,25,50} bps, and the frozen body of the hypothesis (R6/126d,
1/vol20^0.5 scaler, vol20 < 0.60 ceiling, n = 20 EW, **gross fixed at 0.75 and never a parameter**).
480 published rows = 2 panels x 2 cadences x 30 cells x 4 cost rungs, plus a 5-cell DAILY-200d
control ladder inside each (panel, cadence, cost).

## Gates — 16 of 16 exact
- **G0** the numpy simulator IS `engine.backtest`: max|dreturns| and max|dturnover| **0.000e+00** at
  both cadences on both panels (4 of 4).
- **G1** the DAILY c = 0.00 control IS idea 182's literal clause: on 182's own tape (cut at its last
  session, 2026-09-04) it replays **13.6102% / 1.1557 / -18.8134% | OOS 14.5564% / 1.1695** against
  the committed **13.61% / 1.1557 / -18.81% | 14.56% / 1.1695**.
- **G1b** the same book on the CURRENT tape (9 sessions longer) reads 13.5930% / 1.1551 / -18.8134%,
  i.e. **dCAGR -0.0172 pp, dSharpe -0.0006** — the drift is published, not hidden in a tolerance.
- **G2** monthly bar ends == `engine.rebalance_mask(idx,'M')`, symmetric difference **0** on both panels.
- **G3a** no look-ahead: the monthly state at a month-end equals the state recomputed from a tape
  TRUNCATED at that date, **0.0** at 4 probe dates per panel. **G3b** the state changes on month-end
  rows only, **0** mid-month changes.
- **G5** analytic cost reconstruction == `engine.backtest(25bps)` at **0.000e+00**.
- **G6** IS 1887 + OOS 2441 = 4328 sessions, an exact partition.

## PART 1 — the premise is FALSE, and its sign is PANEL-determined, not cadence-determined
d = (monthly gate clock) − (daily 200d control) at the same band, averaged over the 5 bands, 10 bps:

| | mean dSharpe_FULL | mean dSharpe_OOS |
|---|---|---|
| cadence **M** (slow, live) | **−0.0099** | **−0.0091** |
| cadence **W** (fast) | **−0.0170** | **−0.0164** |
| M − W | +0.0070 | +0.0073 |

The pooled M−W is positive but it is a **coin flip: M beats W at 5 of 10 (panel, L) rungs, OOS at 5
of 10** — and the split is not noise, it is the panel: **all 5 U56 rungs are NEGATIVE** (M−W −0.0129
/ −0.0064 / −0.0154 / −0.0167 / −0.0058) and **all 5 B136 rungs are POSITIVE** (+0.0352 / +0.0222 /
+0.0180 / +0.0316 / +0.0206). On the panel the standing candidate actually lives on, the coarser
gate is worth **LESS** at the slow trading clock, which is the opposite of what 2276 predicted.
And in absolute terms the clock is negative on both sides: **dSharpe_FULL > 0 at only 2 of 10 rungs
at cadence M and 1 of 10 at cadence W.**

**The turnover premise fails too, as it did in 2280.** At the MONTHLY cadence the coarser gate does
not trade less: dTurn runs **+0.02 / +0.00 / −0.02 / −0.03 / −0.05 x/yr** across L on U56 — a flat
ladder, so there is no rebate to mistake for signal here at all. (At cadence W it cuts 0.43–0.85x.)

## PART 2 — matched-pair 4b: the clock DESTROYS 4x more passes than it creates
Each of the 400 MONTHLY cells paired with the DAILY control at the same (panel, cadence, cost, band):

| | monthly 4b FULL+OOS | its paired control | creates | destroys | mean dSharpe_FULL | dSharpe_OOS |
|---|---|---|---|---|---|---|
| cadence M | 18/200 | **35/200** | 5 | **22** | −0.0099 | −0.0092 |
| cadence W | 88/200 | **105/200** | 5 | **22** | −0.0126 | −0.0124 |
| pooled | 106/400 | **140/400** | **10** | **44** | **−0.0113** | **−0.0108** |

The grid's 134 4b FULL+OOS passes are **inherited from idea 182's book, not bought by the clock**:
the shipped daily gate passes more often than its own coarsened twin at every cadence.

## PART 3 — both KEEP paths
**4a: 0 of 480**, at every clock, cadence, band and cost rung — the nineteenth consecutive run to
report it. Live RULES v2's −12.05% MaxDD (U56) is unreachable by this book, whose shallowest cell
is −13.46%. **4b FULL+OOS: 134 of 480** (DAILY M 7, DAILY W 21, MONTHLY M 18, MONTHLY W 88);
**BOTH(4a & 4b) 0 of 480.** Binding leg over the 346 4b-FULL failures: **DD-only 225**, joint 79,
Sharpe-only 13, CAGR-only 4 — on this book the DRAWDOWN CAP binds, not the CAGR floor that binds
every gross-ladder run in the record. Benchmarks at 10 bps, U56: SPY 15.29% / 0.9204 / −33.72%
(H1 1.0703 / H2 0.8166; OOS 15.29% / 0.8751 / −33.72%), live RULES v2 8.97% / 1.2399 / −12.05%
(OOS 9.46% / 1.2767 / −12.05%), 4b floor 10.70% and cap −20.23%.

## PART 4 — rule 8: at the live cell, every legal chooser LOSES to the gate it replaces
Dials chosen on IS rows (≤ 2016-12-31) ONLY, 2017–2026 read ONCE; 16 (panel, cadence, cost) families.

| chooser | defined | mean OOS Sharpe | mean OOS CAGR | mean OOS MaxDD | picks MONTHLY | beats shipped gate OOS | 4b OOS |
|---|---|---|---|---|---|---|---|
| C_SHARPE argmax IS Sharpe (monthly clock) | 16/16 | 0.9736 | 12.95% | −20.88% | 16/16 | 8/16 | 5/16 |
| C_4B argmax IS Sharpe among IS-4b passers | **7/16** | 1.0761 | 13.35% | −18.53% | 7/7 | **1/7** | 4/7 |
| C_DAILY argmax IS Sharpe, daily ladder (band only) | 16/16 | 0.9700 | 12.78% | −20.80% | 0/16 | 5/16 | 5/16 |
| **C_LIVE the shipped gate, ZERO parameters** | 16/16 | **0.9801** | 12.68% | −19.96% | 0/16 | — | **8/16** |
| C_ORACLE argmax OOS Sharpe (illegal upper bound) | 16/16 | 1.0187 | 13.43% | −20.14% | 12/16 | 16/16 | 7/16 |

**The zero-parameter shipped gate has the highest mean OOS Sharpe of any LEGAL chooser and the most
4b-OOS passes, while tuning nothing.** C_4B's 1.0761 is an abstention artefact: it is undefined in 9
of 16 families (no monthly-clock cell clears 4b in sample) and beats the shipped gate in **1 of the
7 where it is defined**. **On U56 at the MONTHLY cadence — idea 182's own live cell — no legal
chooser beats the shipped gate OOS at any cost rung, 0 of 16.** At 10 bps C_SHARPE picks L=13 c=0.05
(OOS 14.70% / **1.1237** / −21.69%), C_4B picks L=7 c=0.05 (14.58% / 1.1228 / −21.42%) and C_DAILY
picks c=0.05 (14.34% / 1.1063 / −21.69%), against the shipped gate's **14.52% / 1.1683 / −18.81%** —
every pick is worse on Sharpe AND ~3 pp deeper. The oracle beats it 16/16, so the information exists;
no legal rule reaches it.

## PART 5 — the one thing the clock does buy, and why it is not adopted
**48 of 400** monthly-clock cells are shallower than the shipped gate at no full-sample Sharpe cost.
The best of them, and the only one that is a real capital candidate, is **U56 / L = 5 months /
c = 0.00 / cadence M @ 10 bps**: FULL **13.16% / 1.1850 / −14.61%** (H1 1.3312, H2 1.0616), OOS
**13.15% / 1.1434 / −14.61%**, turnover 5.38x/yr, against the shipped gate's 14.03% / 1.1828 /
−18.81% — **+4.20 pp of drawdown and +0.0022 of Sharpe for −0.87 pp of CAGR**. It clears 4b FULL and
OOS with margins CAGR **+2.46 pp** over the 10.70% floor and DD **+5.62 pp** under the −20.23% cap
(OOS +2.45 / +5.62), Sharpe over SPY +0.2646 full and +0.2683 OOS. **KEEP-4b candidate, RECORDED AND
NOT RECOMMENDED**, memo `2026-09-22_gate-clock-monthly-L5_4b_PARK_MEMO.md`. Three reasons: (i) it is
reached by **0 of 4 legal IS-only choosers at every cost rung on U56/M** — rule 8 cannot get to it,
which makes it PARK, not KEEP; (ii) its **OOS Sharpe is WORSE than the shipped gate's**, −0.0249, so
the gain is a full-sample drawdown fact that does not repeat out of sample; (iii) L = 5 months is the
FASTEST rung of its own ladder and the far end from the live gate's 200-day analogue, and its
neighbours L = 7/10/13/16 buy nothing — the cell is a ladder edge, not a plateau.

## Verdict
**ANSWERED = NO.** The gate clock is not worth more at the monthly cadence: the M−W premise is a
coin flip whose sign is set by the panel and is NEGATIVE on U56, the clock destroys 4x more 4b
passes than it creates, 4a is empty, and the zero-parameter shipped gate beats every legal chooser
built on the dial. **KILL of the gate-clock family, now confirmed on a second book (2284's band
book, this R6 top-20 book) and a second trading cadence.** No RULES change; `RULES.md`, `scan.py`,
`bot.py`, `baseline.py` and `PROTOCOL.md` untouched.

**Survivorship (PROTOCOL rule 9), stated not repaired:** U56 and B136 are CURRENT-CONSTITUENT lists
held from 2008, so every absolute CAGR level is optimistic and both 4b bars are easier than on a
point-in-time panel. The monthly-vs-daily CLOCK CONTRAST is same-tape, same-names and first-order
immune to that; the pass COUNTS are not.
