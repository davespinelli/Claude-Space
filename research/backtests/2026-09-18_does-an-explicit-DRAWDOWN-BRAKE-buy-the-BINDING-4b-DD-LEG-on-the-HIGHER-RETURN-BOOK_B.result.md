# 1262 (lane B, 2026-09-18) — does an explicit DRAWDOWN BRAKE buy the BINDING 4b DD LEG on the HIGHER-RETURN BOOK?

**VERDICT: KILL (capital).** No RULES change, no book promoted, no PROTOCOL edit, no memo, nothing PARKED.
**11 of 11 gates, 144 cells all published, 24s, offline, deterministic.**

## The one-sentence answer
**THE BRAKE CANNOT REACH THE DRAWDOWN THAT DISQUALIFIES THE BOOK — the -20.58% trough that fails 4b is ONE DAY of 4,447 and ZERO of 922 rebalance decision dates, so a brake armed at that depth NEVER FIRES — and every brake shallow enough to fire is, pooled against its own gross-matched control, a -1.36pp/yr CAGR drag that improves drawdown at only 52 of 120 cells: WORSE THAN A COIN FLIP AT THE ONE THING IT EXISTS TO DO.**

## What was run
The frozen 2026-09-04 candidate with **only its gross schedule replaced**. Everything else held: eligibility (above own 200d MA AND vol20 < 0.60), N = 20, H = 126, base GROSS = 0.75, weekly Fri-decide / Mon-trade, equal 1/len(held) slots (1264's answer), 10 bps, t+1, 260-row warm-up, RAW-composite ranking.

    dd(t-1) = equity(t-1) / running_max(equity)(t-1) - 1        on the FROZEN book's own path
    gross(t) = 0.75 * (1 - DEGROSS)  if dd(t-1) <= -TRIGGER  else  0.75

**THE TWO DIALS AND NO MORE (rule 4):** `TRIGGER` {OFF, 0.05, 0.10, 0.15, 0.20, 0.25} (**OFF IS EXACTLY THE COMMITTED CONSTANT-GROSS ANCHOR**) × `DEGROSS` {0.25, 0.50, 0.75, 1.00} = 24 cells per arm. NOT dials, reported at every value: PANEL {U56, B135, SMALL663} × SIGNAL {COMPOSITE3 = the committed three legs, M12_1 = 1257's single 21/252 leg} = 6 arms, **144 cells, EVERY ONE in `.grid.csv`**.

**Frozen constants, declared so they are not mistaken for dials:** no hysteresis band and no minimum brake duration (either would be a third parameter; the chatter this permits is *measured* as turnover, not tuned away); gross never exceeds the anchor's 0.75, so there is no leverage anywhere; `dd` is read on the FROZEN constant-gross book's own equity path, never the braked book's, which avoids a fixed point and is exactly what an implementer observes in real time. **SELECTION IS IDENTICAL AT EVERY CELL BY CONSTRUCTION** — the dials touch only how much of NAV the same names are held at.

**THE CONTROL ARM THAT MAKES THE HEADLINE READABLE.** A brake does not only re-time exposure, it *lowers average exposure*, and this record has established twice (the 2026-09-17 gross-dial run; 1263's finding that 7 of 14 vol-target conversions survive no control) that gross alone is a pure CAGR-for-drawdown slide. So **every braked cell is also run against a constant-gross control held at that cell's OWN realised mean gross**, and the mechanism's effect is the braked cell MINUS that control. The raw comparison against the 0.75 anchor is published too.

## Gates (11 of 11)
**G1/G2** vintage-pinned replay, U56 truncated at the 2026-09-16 cache vintage the committed triples were produced on: COMPOSITE3 OFF replays the committed 15.7147% / 1.1480 / -19.1276% to **5.97e-05**, M12_1 OFF replays 1257's 16.7116% / 1.1893 / -20.5813% to **2.26e-05**. **G10** publishes the one-extra-day drift rather than tolerancing it (+0.0668% / +0.0042 Sharpe on COMPOSITE3; +0.0789% / +0.0048 on M12_1). **G3** OFF bit-identical across all four DEGROSS values (0.000e+00). **G4** realised gross inside [0.0000, 0.7500] at every rebalance of every cell — no leverage, never above the anchor. **G5 NO LOOK-AHEAD**, and the first version of this gate FAILED and was found to be the defective object: it shocked 200 rebalance rows at once, so an earlier shock contaminated a later row's legitimate t-1 decision date. Rewritten to shock **one row at a time**, a -50% return on a rebalance row moves that row's own brake state by **0.000e+00**, and the gate is checked non-vacuous — the same shock moves a *later* rebalance's gross in **185 of the 185** shocked rows (every one of the 185 rebalance rows sampled at a stride of 5 past the warm-up). **G6** brake share monotone non-increasing in trigger depth (0.256 ≥ 0.060 ≥ 0.007 ≥ 0.000 ≥ 0.000). **G7** DEGROSS 1.00 reaches exactly flat (0.000e+00). **G8** the OFF cell's gross-matched control IS the OFF cell (0.000e+00). **G9** determinism, whole U56 COMPOSITE3 grid re-run (0.000e+00).

## Benchmarks on this tape (all recomputed, never carried forward)
| panel | SPY full | SPY halves | SPY OOS | LIVE v2 full | LIVE v2 OOS | 4b DD cap | 4b CAGR floor |
|---|---|---|---|---|---|---|---|
| U56 | 15.13% / 0.8849 / -33.72% | 0.9600 / 0.8236 | 0.8747 | 8.62% / 1.2018 / -12.05% | 1.2781 | -20.23% | 10.59% |
| B135 | 15.16% / 0.8862 / -33.72% | 0.9598 / 0.8261 | 0.8769 | 7.98% / 1.0994 / -12.24% | 1.1061 | -20.23% | 10.61% |
| SMALL663 | 14.06% / 0.8582 / -33.72% | 0.9140 / 0.8346 | 0.8769 | 4.64% / 0.7130 / -12.18% | 0.6518 | -20.23% | 9.84% |

## (1) THE FINDING THAT DECIDES THE IDEA: 4b's DD LEG IS A *MOMENT*, A BRAKE CAN ONLY ACT ON A *STATE*
The disqualifying drawdown is not a condition the book sits in — it is a point it touches. Published per arm as day counts AND rebalance-decision-date counts:

| arm | anchor MaxDD (date) | days ≤ -15% | decision dates ≤ -15% | days ≤ -20% | **decision dates ≤ -20%** |
|---|---|---|---|---|---|
| U56 / COMPOSITE3 | -19.13% (2020-03-16) | 24 of 4447 | 6 of 922 | 0 | **0** |
| **U56 / M12_1** (1257's better book) | **-20.58% (2018-12-24)** | 26 of 4447 | 6 of 922 | **1 of 4447** | **0 of 922** |
| B135 / COMPOSITE3 | -20.74% | 23 | 5 | 0 | **0** |
| B135 / M12_1 | -21.73% | 44 | 9 | 3 | 2 |

**On U56/M12_1 — the exact book 1257 showed is disqualified by 1.45pp of drawdown and nothing else — the book is at or below -20% on ONE trading day in seventeen years and on NO rebalance decision date at all.** A brake armed at 0.20 or 0.25 therefore has `brake_share` **0.0000** and is **bit-identical to do-nothing** at 8 of 8 U56 cells (G6 confirms; the grid shows the identical 16.79% / 1.1941 / -20.58%). The only brakes that ever fire (0.05, 0.10, 0.15) fire during drawdowns that **never set the maximum** — they pay CAGR for 22-26% of weeks in order to be flat for the one that counts.

## (2) AGAINST ITS OWN GROSS-MATCHED CONTROL THE BRAKE IS A DRAG, AND A COIN FLIP ON DRAWDOWN
Pooled over the 120 braked cells, braked MINUS constant gross at the same mean exposure:

| | d_CAGR | d_Sharpe | d_MaxDD | d_OOS_Sharpe | turnover |
|---|---|---|---|---|---|
| pooled, 120 cells | **-1.36pp** | **-0.0833 (positive at 2 of 120)** | **-0.35pp (positive at only 52 of 120)** | **-0.0967 (positive at 3 of 120)** | +0.49 to +1.11/yr |

**A mechanism whose whole purpose is drawdown beats a flat gross cut on drawdown at 52 of 120 cells — less often than chance.** Compare 1263's vol targeting, which at least posted d_MaxDD +1.18pp positive at 60 of 108. Plain constant-gross controls clear 4b at **41 of 144 against the braked cells' 38**: **de-grossing flat passes 4b MORE OFTEN than braking does.**

Pre-declared outcome **(D) fires and it is the DEGROSS dial that carries it**: d_MaxDD runs **+0.88 / +1.41 / -0.16 / -3.52pp** at DEGROSS 0.25 / 0.50 / 0.75 / 1.00. **Going fully flat while braked makes the realised drawdown 3.52pp WORSE than simply holding less stock all the time** — the brake sells the bottom and buys the recovery back higher. Pre-declared **(A)** fires at the deep triggers (section 1), **(C)** at the shallow ones: 16 of 144 cells convert a committed 4b FAIL to a PASS, but **6 of the 16 are reproduced by their own flat gross-matched control** — no timing involved, just less exposure.

## (3) RULE 8 REFUSES IT, AND THE REFUSAL IS EXACTLY WHERE THE MECHANISM'S ONLY WINS LIVE
(TRIGGER, DEGROSS) chosen on warm-up..2016-12-31 by IS Sharpe alone; 2017-2026 read ONCE.

| panel / signal | IS-argmax pick | pick OOS Sharpe | do-nothing OOS | **delta** | 4b pick / OFF |
|---|---|---|---|---|---|
| U56 / COMPOSITE3 | **TRIGGER OFF** | 1.1832 | 1.1832 | **+0.0000** | PASS / PASS |
| U56 / M12_1 | **TRIGGER OFF** | 1.1626 | 1.1626 | **+0.0000** | FAIL / FAIL |
| B135 / COMPOSITE3 | **TRIGGER OFF** | 1.0240 | 1.0240 | **+0.0000** | FAIL / FAIL |
| B135 / M12_1 | 0.05 / 0.50 | 0.9603 | 1.0004 | **-0.0401** | PASS / FAIL |
| SMALL663 / COMPOSITE3 | **TRIGGER OFF** | 0.4534 | 0.4534 | **+0.0000** | FAIL / FAIL |
| SMALL663 / M12_1 | **TRIGGER OFF** | 0.4875 | 0.4875 | **+0.0000** | FAIL / FAIL |

**The in-sample chooser asks for NO BRAKE AT ALL at 5 of 6 arms, and the one arm that asks for a brake loses 0.0401 of OOS Sharpe and buys its 4b pass by giving up return** (0.9603 against the anchor's 1.0004 — 1265's question again, measured live). Mean delta **-0.0067, beats do-nothing at 0 of 6**. Every realised OOS Sharpe in the grid is below live RULES v2's 1.2781 / 1.1061 / 0.6518. **4a is 0 of 144** and fails on the DD leg at **144 of 144** (100 cells also fail both halves): live v2's -12.05% is not reachable from a 0.75-gross momentum book.

## (4) THE ONE NEAR-MISS, AND WHY IT IS NOT PARKED
Three cells beat their gross-matched control on **both** DD and OOS Sharpe — all three are U56/COMPOSITE3/TRIGGER 0.05. The best, **0.05 / 0.25: 14.31% / 1.1636 / -16.54%, halves 1.2026/1.1366, OOS 1.2183, turnover 3.17/yr** — against the anchor's 15.78% / 1.1522 / -19.13% / OOS 1.1832 that is **+2.59pp of drawdown, +0.0114 of full Sharpe and +0.0351 of OOS Sharpe for -1.47pp of CAGR**, and its control-relative d_MaxDD +1.44pp / d_OOS +0.0353 says it is genuinely the timing.

It is **KILLED, not PARKED**, for a reason that is the point of rule 8: **its IS Sharpe is 1.0935 against do-nothing's 1.1158, and the same is true of all three (1.0935 / 1.0421 / 0.9538 vs 1.1158).** The mechanism's only wins on this tape are wins that **no in-sample chooser can select** — an out-of-sample-only edge at 3 cells out of 120, in a pooled distribution whose OOS delta is positive at 3 of 120, is what chance produces. 1263 parked a cell that dominated the incumbent on three legs of four; this one improves full Sharpe by 0.0114 and loses in sample. Parking it would dress 3 lucky cells as a finding.

## WHAT THE RECORD SHOULD TAKE, IN ONE SENTENCE
**ALL THREE MECHANISMS FOR BUYING THE BINDING 4b DD LEG ARE NOW PRICED AND ALL THREE FAIL — inverse-vol slot sizing (1264, rule 8 picks equal weight), portfolio vol targeting (1263, half the conversions are flat de-grossing) and now the explicit drawdown brake (1262, blind to the only drawdown that matters) — so the standing diagnosis should change from "the DD cap refuses available return" to "the DD cap refuses available return AND EVERY RISK CLAUSE THAT WOULD SATISFY IT COSTS MORE RETURN THAN IT SAVES, at 10 bps, on this tape."** The next idea in this family should stop trying to buy the leg and start asking whether a -20.23% cap read off a single-day trough is the right bar (1259's margin question, and 1265's), because the mechanism side is now exhausted.

## SURVIVORSHIP (rule 9)
U56 and B135 are **current-constituent** lists; SMALL663 is a current sub-$2B screen (52 of 715 dropped for `max_1d_move >= 1.0`). Every level is optimistic and every 4b pass an upper bound. The headline is a **difference between gross schedules applied to the SAME holdings on the SAME panel** — selection is identical at every cell by construction — which is first-order immune to a level bias that moves all cells together. One direction is **not** neutral and is stated: a current-constituent panel **understates** the deep drawdowns a momentum book took in names later delisted, so the anchor's drawdown is **flattered**, the day-count table in section 1 would show more days below -20% on a live panel, and the brake's DD improvement here is a **lower** bound — while the CAGR it gives up is measured against a flattered comparand.

- Script: `research/backtests/2026-09-18_does-an-explicit-DRAWDOWN-BRAKE-buy-the-BINDING-4b-DD-LEG-on-the-HIGHER-RETURN-BOOK_B.py`
- Grid (all 144 cells): `..._B.grid.csv` · walk-forward: `..._B.walkforward.csv` · gates: `..._B.gates.csv` · console: `..._B.console.txt`
