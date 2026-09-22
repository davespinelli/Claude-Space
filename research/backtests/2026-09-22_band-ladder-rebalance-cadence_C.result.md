# Idea 2207 (lane C, 2026-09-22) — is the KEEP-4b candidate a REBALANCE-FREQUENCY object?

**ANSWERED — PARTIALLY YES, AND THE PART THAT MOVES IS THE MARGINAL BANDS, NOT THE CORE.**
The 4b pass *set* on the band x gross ladder is **not** cadence-stable (median Jaccard vs weekly
**0.550**, range 0.000–1.000 over 12 panel x cost x cadence comparisons), but the ladder's core
cell survives every cadence: **only `b0.03_g1.00` (the live band at full gross) passes 4b at all
four cadences at BOTH cost rungs**, and it does so on U56 in every one of its 8 cadence x cost
cells. Every 4b pass anywhere on the 600-row grid sits at **gross 1.00**, reproducing 2119's
finding at D / W / 2W / M rather than only at W.

Script `research/backtests/2026-09-22_band-ladder-rebalance-cadence_C.py`, log `..._C.log.txt`.
**5 of 5 gates PASS** (G1 max|d| 0.000e+00 against `engine.backtest` at D/W/M; G3 ladder centre
cell == `baseline.rules_v2_weights`, max|d| 0.000e+00; G2 0 differing mask rows, |2W| 489 ==
ceil(977/2)). Anchors reproduce the record exactly: SPY U56 **15.14% / 0.8851 / −33.72%**
(H 0.9570/0.8264), OOS 15.29% / 0.8751 / −33.72%; live RULES v2 (W) @10 bps **8.62% / 1.2010 /
−12.05%**, OOS **9.46% / 1.2767 / −12.05%**. 4b bars: DD cap −20.23%, CAGR floor 10.60% FULL /
10.70% OOS.

## The grid
5 bands x 5 grosses x 4 cadences x 2 panels = **200 books**, each at 0 / 10 / 25 bps = **600
published rows** (`..._C.grid.csv`). Tuned dials: exactly two — **CADENCE** and **GROSS**. The
band is reported at all five rungs, never tuned (the rule-8 primary scope is cadence x gross at
the live band 0.03; the joint band x gross x cadence pick is reported beside it, labelled as a
three-dial control). Cost 0 bps is the B5 mechanism read only and carries no verdict.

## B1 — the pass count is a cadence object (4b FULL, of 25 cells)
| panel @ cost | D | W | 2W | M |
|---|---|---|---|---|
| U56 @10 bps | 4 | 5 | **5** | 3 |
| U56 @25 bps | 2 | 4 | **5** | 3 |
| B136 @10 bps | 1 | 4 | 4 | 2 |
| B136 @25 bps | 1 | 1 | 0 | 2 |

4b **OOS** passes: U56 @10 bps D5 / W6 / **2W8** / M6; B136 @10 bps D1 / W1 / **2W3** / M2.
**The weekly convention is not the argmax.** 2W has the highest FULL Sharpe on every panel x cost
(U56 @10 bps 1.2252 vs W 1.2011) and weakly dominates W on pass count — so weekly is not a dial
tuned to flatter the record, it is a *conservative* choice that leaves a little on the table.

## B2 — the pass SET, not its size
Cells passing 4b at **all four** cadences: U56 @10 bps **2** (`b0.02_g1.00`, `b0.03_g1.00`),
U56 @25 bps **1** (`b0.03_g1.00`), B136 **0 at either rung**. Jaccard vs weekly: D 0.800 / 2W
1.000 / M 0.600 (U56 @10 bps); D 0.250 / 2W 0.600 / M 0.200 (B136 @10 bps); B136 @25 bps 2W
**0.000** and M **0.000**. Two B136 @25 bps passes exist at exactly one cadence
(`b0.00_g1.00`, `b0.02_g1.00`, both M-only) — those are cadence artefacts.

## B3 — the binding leg differs at the two ends of the cadence axis
The CAGR floor binds everywhere (fail rate 0.80–0.96, sole binder on 18–24 of 25 cells at every
cadence). What cadence changes is the **DD** leg: fail rate **0.000 at D / W / 2W** and
**0.120 (U56) / 0.200 (B136) at M** — monthly buys CAGR by spending drawdown. Of the **14**
weekly 4b passers, **26 of 42** cadence re-reads still pass (61.9%); the margin swings are large
where the band is wide: U56 `b0.08_g1.00` min margin **+0.241 (W) → −3.996 (M)**, B136
`b0.05_g1.00` **+0.023 (W) → −2.869 (M)**. B136 `b0.03_g1.00` @10 bps runs D **−0.179** /
W **+0.041** / 2W **+0.173** / M **−0.272** — a committed weekly pass whose whole margin is
0.04 pp and which is cadence-dependent in both directions.

## B4 — rule 8 (IS ..2016-12-31 only, OOS 2017–2026 read once)
| panel @ cost | chooser | pick | OOS CAGR / Sharpe / MaxDD | 4b OOS | 4a OOS | OOS rank |
|---|---|---|---|---|---|---|
| U56 @10 | IS_SHARPE = IS_CALMAR = IS_MINMARG | `b0.03_g1.00_M` | **12.82% / 1.2252 / −18.81%** | **True** | False | 16/20 |
| U56 @10 | MAXGROSS_W (0 dials) | `b0.03_g1.00_W` | **12.67% / 1.2760 / −15.91%** | **True** | False | 15/20 |
| U56 @25 | all three fitted | `b0.03_g1.00_M` | 12.54% / 1.2011 / −18.84% | **True** | False | 16/20 |
| B136 @10 | IS_SHARPE | `b0.03_g1.00_W` | 10.47% / 1.1006 / −16.16% | False | False | 15/20 |
| B136 @10 | IS_CALMAR / IS_MINMARG | `b0.03_g1.00_M` | 10.97% / 1.0802 / −20.50% | False | False | 16/20 |
| B136 @25 | all three fitted | `b0.03_g1.00_M` | 10.65% / 1.0517 / −20.54% | False | False | 16/20 |

Fitted picks: **16 of 24** clear 4b OOS, **19 of 24** clear 4b FULL, **0 of 24** clear 4a (either
window) — no cadence produces a book that beats the live book on path 4a. The zero-parameter
**MAXGROSS_W** clears 4b OOS 4 of 8 and its mean OOS Sharpe is **1.1681 vs the fitted 1.1606**:
the **fitting premium for choosing cadence in-sample is −0.0075 OOS Sharpe**, i.e. nothing, which
extends 2211's finding from the gross dial to the cadence dial. Every fitted chooser also picks
**M** on the panel where M fails the DD cap — the IS view prefers the cadence that spends
drawdown. RANDCELL (the uniform draw) reads 9.40% / 1.2743 / −12.27% on U56 @10 bps, better
ranked (10/20) than any fitted pick.

## B5 — mechanism (post-hoc, no cell selected on it)
Mean turnover/yr D 3.17x / W 1.89x / 2W 1.51x / M 1.17x (U56). At **0 bps** the pass count is
D5 / W5 / 2W5 / M3 (U56) and D5 / W5 / 2W4 / M2 (B136): **the daily collapse is pure trading
cost** (U56 5 → 4 → 2 at 0 → 10 → 25 bps; B136 5 → 1 → 1) while **the monthly collapse is
timing, already present at zero cost** (U56 3, B136 2 at 0 bps). Cadence therefore has two
distinct failure modes, and 2W sits between them.

## Verdict
**ANSWERED / PARTIAL — a KILL of the cadence dial as a source of anything new, and a
cadence-invariance certificate for one already-standing cell.** No cadence yields a 4a pass (0 of
24), no cadence yields a 4b pass outside gross 1.00, and fitting cadence in-sample is worth
−0.0075 OOS Sharpe. What the run does establish is that the record's **B136** band x gross
verdicts are cadence-dependent (0 cells survive all four cadences; margins of ±0.5 pp) while the
U56 `b0.03_g1.00` cell is cadence-invariant at 8 of 8 cadence x cost cells — see
`..._C.memo.md`. **Recorded, not adopted**: RULES.md, PROTOCOL.md, scan.py, bot.py and
baseline.py are untouched (rule 6 — rules change only at a Sunday review).

**Survivorship (rule 9).** U56 and B136 are current-constituent lists; every absolute CAGR and
drawdown here is optimistic. This is a within-tape contrast across cadence on identical cells and
does not repair the level. **Units note:** the `min_margin` column mixes Sharpe units (H1/H2
legs) with pp (DD/CAGR legs); it is used only as a pass/fail-distance indicator, never as a
scalar to optimise.
