# Idea 296 — re-quote-every-de-gross-claim-with-its-constant-leverage-replay (cloud, 2026-09-06)

**Verdict: ANSWERED / SPLIT. The published de-gross DRAWDOWN claims are 93% exposure and the CAGR
claims 73–89%, so they are exposure claims, not gate claims. The Sharpe verdicts do not move at
all (1 flip in 162) — because a constant-leverage replay is Sharpe-neutral, the record's Sharpe
comparand was never contaminated, and the de-gross books lose to it in 85% of cells anyway. The
one construction that DOES survive its replay is the live RULES v2 book. Rules unchanged; no KEEP
(4a 1/162, 4b 15/162, all of them ranked TOP20 books whose edge is the ranking).**

Script `2026-09-06_re-quote-every-de-gross-claim-with-its-replay_cloud.py`, 162 cells × 4 books
(DEGROSS, its RESPREAD twin, REPLAY-EW, REPLAY-RS) + 9 controls + the live book and its two
replays, at 10 and 0 bps. 102s, deterministic.

## The instrument
Two zero-parameter replays; each constant is **read off the cell**, never fitted:
* **REPLAY-EW** = `c₂ · EWall`, `c₂ = mean gross(DG) / mean gross(EWall)` — no gate at all, held at
  the de-grossed book's own average exposure. Removes selection *and* timing.
* **REPLAY-RS** = `c₁ · RESPREAD twin` — same names, same relative weights, constant leverage.
  Removes timing only.
Both traded at the cell's cadence and charged the same 10 bps.

## Validity, asserted before any new number was read
| | bar | result |
|---|---|---|
| D0(i) vectorised backtester vs `engine.backtest`, 9 books | < 1e-12 | **8.9e-16** — HOLDS |
| D0(ii) replay realised mean gross matched to DG's | < 0.005 | worst **0.0033** (EW) / **0.0032** (RS); **0 of 162 cells excluded** |
| D0(iii) identity `r_dg,t ≡ c_t·r_rs,t` at 0 bps, 162 pairs | < 1e-12 | **3.5e-17** — HOLDS |

## Part A — the record itself (declared regexes; a mapping, not a semantic reading)
| source | rows/entries | mentioning de-gross | with a comparative claim | touching a KEEP path |
|---|---|---|---|---|
| LEADERBOARD.md | 2651 | **141** | 66 | 67 |
| CHANGELOG.md | 150 | **44** | 42 | 44 |

Those rows name three panels (U56 75, B136 57, SMALL 37 leaderboard hits), the MA/MAVOL gate
forms (23/14) and the ranked n=20 channel (16), which is exactly the 162-cell corpus re-run
below. Rows quoting constructions outside it (sleeves, stops, ddctl, blends) are **not** re-run
and are reported as the un-mapped remainder, not counted as survivors.

## The five readings
| | bar | result | reading |
|---|---|---|---|
| **D1** Sharpe claims survive the replay | rate > 0.50 | DG beats REPLAY-EW in **24/162 (0.148)** vs the full-gross control **25/162 (0.154)** | exposure claims — but see below |
| **D2** drawdown claim survives | shallower than replay in ≥ 2/3 | **97/162 (0.599)**, mean −19.59% vs −20.12% | **does NOT survive** |
| **D3** exposure share replicates idea 290 | median in [0.80, 1.00] | corpus median **0.7331**; MA/MAVOL only **0.7779**, TOP20 **0.0621** | replicates for pure gates, meaningless for ranked ones |
| **D4** replay passes 4b at least as often | replay ≥ DG | DG **15** vs replay **0** | gate adds cells — all 15 are TOP20 |
| **D6** IS-chosen DG beats IS-chosen replay OOS | ≥ 5/9 arms | **3/9**; mean OOS Sharpe 0.8867 vs 0.9816 | **does NOT survive OOS** |

## What the numbers actually say
1. **The replay is Sharpe-neutral, and that is the finding.** Scaling a book's weights by a
   constant scales its returns, so REPLAY-EW's Sharpe differs from the full-gross control's by a
   mean of **0.0014** (max 0.0103). Exactly **1 of 162** Sharpe verdicts flips
   (SMALL439/MA/M/b=0.02, 0.6608 vs 0.6596 → 0.6623). So the record's Sharpe comparisons were
   never carrying the exposure rider; the rider lives entirely in **drawdown and CAGR**, and that
   is where re-quoting changes the answer.
2. **The drawdown claim is 93% exposure.** Against the full-gross control the de-grossed books are
   **+7.74 pp** shallower on average; their exposure-matched replays are **+7.22 pp** shallower
   with no gate at all — a **93.3%** share (MA **96.8%**, MAVOL **97.9%**, TOP20 30.8%). What the
   gate's timing actually buys is the remaining **0.52 pp** of drawdown, and it buys it in only
   60% of cells.
3. **The CAGR price is real and is mostly exposure too.** Mean dCAGR(DG − REPLAY-EW) is
   **−1.89 pp/yr**, negative in **157 of 162** cells: the de-grossed book is *worse* than simply
   holding less. Idea 290's 91.4% exposure share replicates in shape on the pure-gate families
   (median 0.778, U56/MA 0.894, SMALL439/MA 0.835) but is **meaningless against a control that
   also differs in selection** — TOP20's median share is 0.062 because most of its gap is the
   ranking, not the exposure.
4. **Against its own selection at constant leverage, de-grossing is a coin flip.** DG beats
   REPLAY-RS in **75/162 (0.463)**, mean dSharpe **−0.0248** (MA −0.043, MAVOL −0.035, TOP20
   +0.004) — the same "timing buys nothing" reading ideas 297/300 reached by another route.
5. **The KEEP-path cells belong to the ranking, not the de-gross clause.** 4b passes: DG 15/162,
   replay 0/162 — but **all 15 are TOP20** (U56 11, B136 4), no MA or MAVOL cell passes anywhere,
   and the replays fail almost entirely on the CAGR bar (72 of 162) precisely because they hold
   the same reduced exposure. "The gate adds cells" here means "the ranking adds cells".
6. **The exception that matters: the live book survives its replay.** RULES v2 at realised mean
   gross **0.5215**: 8.52%/**1.2128**/−11.69% (OOS 1.2938). Its selection-matched constant-leverage
   replay: 8.53%/1.1680/−12.48% (OOS 1.2108). The no-gate replay at the same exposure:
   9.22%/1.1289/−16.02% (OOS 1.1405). So the live de-gross clause buys **+0.045 Sharpe and 0.79 pp
   of drawdown at identical CAGR** against its own names held flat, and **+0.084 Sharpe and
   4.34 pp of drawdown for 0.71 pp/yr of CAGR** against no gate at all — and the ordering holds
   out of sample. It also turns over 1.76×/yr against the twin's 4.32×. This is one of the few
   de-gross claims in the record that is not an exposure claim.
7. **Out of sample the choosable de-gross arm loses to the choosable replay.** Under rule 8 with
   both sides given the same freedom, the IS-chosen de-gross arm wins **3 of 9** panel × family
   arms; mean OOS Sharpe 0.8867 vs **0.9816**, mean OOS CAGR 7.83% vs 9.66%. It beats SPY in 6/9
   and the live book in **0/9**.

## Caveats
Costs 10 bps, next-day execution, 75% gross, no shorting or leverage. The replay is a comparand,
not a proposal: holding a fixed 52% of NAV in an equal-weight book is itself a capital decision
this run does not endorse. SURVIVORSHIP: all three panels are current constituents (439 sub-$2B
names with the 44 `max_1d_move >= 1.0` dropped; universe(_broad).json are today's large caps and
ETFs); the DG-minus-replay columns are arm-minus-arm contrasts on identical names and days so the
bias very largely cancels there, but it does NOT cancel from the 4a/4b level columns. Part A's
counts are regex mappings of the record's text, not a semantic audit; the un-mapped remainder is
stated rather than assumed to behave the same way.
