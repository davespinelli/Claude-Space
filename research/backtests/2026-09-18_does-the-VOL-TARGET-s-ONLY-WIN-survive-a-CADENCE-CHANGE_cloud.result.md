# Idea 1305 (lane cloud, 2026-09-18) — does the VOL-TARGET's ONLY WIN survive a CADENCE CHANGE?

**VERDICT: KILL, and the queue's own premise is FALSIFIED.** Idea 1297's single OOS winner
(U56, TARGET=8%, WINDOW=21d, +0.0166 of OOS Sharpe for −1.54 pp of OOS CAGR) is **neither an
edge nor the rebate** — it is a **WEEKLY-ONLY artifact**. Moved to monthly, the same cell reads
**−0.0219** against its own-cadence control. And the premise that "a W→M change is a turnover
rebate every book collects" is **false on 2 of 3 panels**: the un-scaled flat book's W→M OOS
Sharpe change is **U56 −0.1048, SMALL −0.1658, B136 +0.0750**. Monthly does refund cost
(−6.0 / −6.5 / −8.3 bp/yr of drag) — the refund is simply swamped by what the slower cadence
costs in drawdown. 30 B_CONST cells + 30 B_SELF + 6 flat controls, **every one published**.
76 gates pass, 0 fail. Offline, deterministic, 11.2 s. No RULES/PROTOCOL change (rule 6).

## The instrument
Two dials and no more (rule 4): **CADENCE {W, M} × TARGET {6, 8, 10, 12, 14}%**, WINDOW frozen
at 21 d (the queue fixes it). Scaler is 1297's, unchanged: at each application row
`k_t = min(0.60, TARGET / v_t)`, `v_t` = annualised sd of the basis book's daily returns over
the 21 rows **ending at t−1** (rule 2). Cap = the incumbent's own gross 0.60, so **no cell is
levered**. Basis B_CONST (the constant-gross book at the same cadence, non-circular) is the
headline; B_SELF is published beside it. Book = the certified incumbent N=15 / H=126 / g=0.60.

**The control that decides it.** The un-scaled flat g=0.60 book is built at **both** cadences,
and the run reports the difference-in-differences
`DiD = [S(scaled@M) − S(flat@M)] − [S(scaled@W) − S(flat@W)]`. A positive DiD is evidence the
scaler is timing volatility; a DiD ≤ 0 says the cadence, not the scaler, moved the number.

## 1. The premised rebate is a B136 fact, not a tape fact
| panel | flat W Sharpe | flat M Sharpe | full ΔS | OOS ΔS | Δ turnover | Δ drag |
|---|---|---|---|---|---|---|
| U56 | 1.1706 | 1.0653 | **−0.1053** | **−0.1048** | −0.60 /yr | −6.0 bp/yr |
| B136 | 1.0670 | 1.0953 | **+0.0283** | **+0.0750** | −0.65 /yr | −6.5 bp/yr |
| SMALL | 0.5202 | 0.4405 | **−0.0796** | **−0.1658** | −0.83 /yr | −8.3 bp/yr |

The cost rebate is real and uniform (~6–8 bp/yr) and **an order of magnitude smaller** than the
Sharpe swing it is offered to explain. On U56 the slower cadence also deepens MaxDD −16.38% →
−19.25%; on B136 −15.97% → −22.76%, which is how B136's +0.0750 of OOS Sharpe is bought.

## 2. The +0.0166 is WEEKLY-only
U56 / B_CONST / TARGET=8%: OOS edge over own-cadence flat **+0.0166 at W, −0.0219 at M**,
**OOS DiD −0.0386**. Across all 30 (panel × basis × target) cells: **OOS DiD > 0 in 9 of 30**,
mean **+0.0016**, median **−0.0137**; the scaler still beats its own-cadence control at M in
**9 of 30**, and all 9 sit at the two lowest targets (6–8%) on U56/B136 — the settings where
`k` is off the cap on 45–58% of rows, i.e. where the "scaler" is mostly a de-grosser.

## 3. Rule 8 (2017–2026 read once), (CADENCE, TARGET) by argmax IS Sharpe
| panel/basis | pick | OOS scaled | OOS flat @W | OOS flat @M | 4b all legs |
|---|---|---|---|---|---|
| U56/B_CONST | **W 8%** | 13.58% / 1.2113 / −14.41% | 15.12% / 1.1947 / −16.38% | 13.72% / 1.0899 / −19.25% | **1** |
| U56/B_SELF | W 8% | 14.03% / 1.2140 / −15.01% | " | " | 1 |
| B136/B_CONST | W 6% | 9.91% / 1.0056 / −11.33% | 14.11% / 1.0454 / −15.97% | 16.30% / 1.1204 / −22.76% | 0 |
| B136/B_SELF | W 6% | 11.04% / 1.0075 / −12.86% | " | " | 1 |
| SMALL/B_CONST | M 6% | 0.96% / 0.1412 / −22.33% | 6.40% / 0.4653 / −33.35% | 3.63% / 0.2995 / −28.68% | 0 |
| SMALL/B_SELF | M 6% | 1.50% / 0.1784 / −25.41% | " | " | 0 |

SPY OOS 15.28% / 0.8747 / −33.72% (U56 calendar); live RULES v2 OOS 9.47% / 1.2781 / −12.05%.
**The IS chooser never picks monthly where the scaler helps** — it picks W on U56 and B136 and
picks M only on SMALL, where the scaler then loses 0.1583 of OOS Sharpe. Full sample: **4a 0 of
66**; 4b full-sample legs 17/30 B_CONST, 18/30 B_SELF, 3/6 flat; **4b all legs after rule 8:
3 of 6** — and all three are books the flat control already clears without any scaler.

## 4. Why this is a KILL rather than a KEEP
The U56/W/8% cell does pass 4b on every leg. So does the **flat book it is built on**, which
needs no second dial, and the scaler's whole contribution is +0.0166 of OOS Sharpe bought for
−1.54 pp of OOS CAGR — a trade that reverses sign the moment the rebalance calendar moves by
one step. A capital rule whose only win is conditional on the operator rebalancing weekly and
never monthly is not a rule; it is a coordinate. **KILL.**

## Gates (76/76)
G0 sample ≥ 10 y · G1 U56 weekly flat control replays idea 1215's committed 13.66% / 1.1706 /
−16.38% · G2 degenerate TARGET=1000% reproduces the flat control **bit-exactly** at both
cadences on all three panels · G3 live RULES v2 U56 MaxDD = the committed −12.05% · G4 monthly
is cheaper than weekly at every panel × basis × target · G5/G6 IS and OOS windows disjoint,
OOS starts 2017-01-03 · G7 `k` never exceeds the incumbent gross (no leverage) anywhere ·
**G8a** the weekly column replays idea 1297's committed WINDOW=21 cells on U56 and B136 to
< 5e-4 · **G8b** the SMALL replay differs by ≤ 4.19e-3, and the reason is stated rather than
tolerated: 1297/1309 screened the small panel with an **in-panel** `max |1d move| < 1.0` test
(664 names), while this run applies the **protocol-mandated `data/small_meta.csv`
`max_1d_move >= 1.0` drop**, which additionally removes **OBT** (663 names).

## Survivorship (rule 9)
U56 / B136 / SMALL663 are **current-constituent** lists; SMALL663 is a sub-$2B screen carried
back to 2010, so its *levels* are an upper bound. Only its *contrasts* (W vs M, scaled vs flat)
are read here, and every one of them points the same way as U56's.

Data: `.grid.csv` (30 B_CONST cells) · `.robust.csv` (30 B_SELF) · `.flat.csv` (6 controls) ·
`.did.csv` (30 difference-in-differences rows) · `.walkforward.csv` · `.gates.csv` ·
`.console.txt`.
