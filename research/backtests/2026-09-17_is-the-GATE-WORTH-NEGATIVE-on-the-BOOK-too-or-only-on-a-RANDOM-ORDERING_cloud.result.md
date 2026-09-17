# 1096 (lane cloud, 2026-09-17) — is the gate worth negative on the BOOK too, or only on a random ordering?

**ANSWER: THE GATE IS NOT WORTH NEGATIVE ON THE LARGE-CAP BOOK — IT IS WORTH ALMOST EXACTLY
NOTHING (-0.23 pp/yr of CAGR for +0.94 pp of drawdown at the committed rung, Sharpe -0.0051) —
AND IT *IS* WORTH NEGATIVE ON THE SMALL-CAP PANEL AT EVERY RUNG (-2.80 to -4.11 pp/yr of CAGR
while making drawdown WORSE at 7 of 8 rungs).** Pre-declared outcome (A) lands on U56,
(C) lands on SMALL663, (B) lands on B136's drawdown only. Idea 1085's "0.54-1.89 pp/yr risk
filter" is a property of the RANDOM ORDERING, not of the real book: on the momentum book the
ranking has already done the gate's work.

## What was run
Frozen 2026-09-04 candidate (composite 21/252 + 0/126 + 0/63 RAW, no vol scaler, H = 126,
GROSS = 0.75, weekly, 10 bps, t+1) with two dials and no more: **n ∈ {5,10,12,15,20,25,30,40}
× GATE ∈ {BOTH, MA, VOL, NONE} = 32 cells per panel, 96 in all, every one published**
(`.grid.csv`), plus two control arms per rung (`.control.csv`). Anchor (20, BOTH) replays the
committed U56 triple to 4.65e-05.

## A DEFECT IN THE RECORD, PUBLISHED RATHER THAN QUIETLY FIXED (rule 7)
Every memo describes the book as "gated-out weight to CASH, de-gross, never re-spread".
**IT DOES NOT.** Every committed script sets each holding to 1/len(selected), so the book is
**always fully invested at GROSS = 0.75** — mean net exposure is 0.750 at all 96 grid points,
published in the `exposure` column. A screen admitting 9 names holds those 9 at 8.33% each.
**THE COMMITTED GATE IS A PURE SELECTION FILTER AND CANNOT TIME EXPOSURE AT ALL.** The main
grid is left as the record built it; the missing behaviour is measured as controls:
- **CASH\*** — gate BOTH, 1/N weights, unfilled slots in cash (the book the memos describe).
  It de-grosses only slightly: mean exposure 0.722–0.750 on U56, 0.744–0.750 on B136, and
  **0.750 at every rung on SMALL663 (with 663 names the screen never runs out of candidates,
  so the de-gross clause is unreachable there)**.
- **MTCH\*** — ungated, at a CONSTANT gross equal to CASH\*'s own mean exposure: the same
  average money at risk, bought by permanently holding less instead of by timing.

## The committed rung (n = 20), per panel: gate BOTH vs gate NONE, same gross
| panel | CAGR B/N | MaxDD B/N | Sharpe B/N | OOS Sharpe B/N | 4b B/N |
|---|---|---|---|---|---|
| U56 | 15.71% / 15.94% | -19.13% / -20.06% | 1.1480 / 1.1531 | 1.1759 / 1.1463 | PASS / PASS |
| B136 | 16.18% / 16.82% | -20.74% / -24.33% | 1.0715 / 1.0667 | 1.0240 / 1.0563 | FAIL / FAIL |
| SMALL663 | 7.87% / 11.79% | -35.81% / -33.14% | 0.5073 / 0.6412 | 0.4534 / 0.6567 | FAIL / FAIL |
SPY (U56 window): 15.06% / 0.8815 / -33.72%, halves 0.9600/0.8171, OOS 15.15% / 0.8686.
LIVE RULES v2: 8.60% / 1.1982 / -12.05%, OOS 9.42% / 1.2717.

## Headline
- **THE GATE BINDS ON ALMOST NOTHING THE RANKING WANTED.** Mean gate-on share of panel-days is
  0.684 (MA), 0.926 (VOL), 0.667 (BOTH) — but the top-20 momentum names are already above
  their own 200d MA, so at n = 20 removing the whole screen moves CAGR by 0.23 pp and Sharpe
  by 0.0051 on U56 and does not change the 4b verdict.
- **THE SIGN IS n-DEPENDENT AND COIN-FLIP.** Over the 8 rungs the gate improves MaxDD at 4 of 8
  (U56), 6 of 8 (B136) and **1 of 8 (SMALL663)**; it improves CAGR at 3 / 3 / **0** and Sharpe
  at 3 / 4 / **0**. At n = 5 it costs **5.05 pp/yr** of CAGR on U56 (17.79% vs 22.84%) to buy
  1.21 pp of drawdown — 4.19 pp of CAGR per pp of drawdown, the worst price on the grid.
- **THE VOL LEG IS THE PART THAT DOES THE RISK WORK; THE MA LEG BUYS RETURN WITH DRAWDOWN.**
  On U56, 4b passes by gate: **VOL 5 of 8, BOTH 3, NONE 3, MA 2**. The MA leg alone posts the
  grid's best Sharpe (n=10: 1.2349 full, 1.2337 OOS, CAGR 20.19%) and fails 4b on drawdown
  (-22.36%) at that rung. The two legs are not one screen and the record treats them as one.
- **IS TIMING CHEAPER THAN HOLDING LESS? ONLY ON B136.** CASH\* beats MTCH\* on MaxDD at 4 of 8
  rungs on U56 (mean dCAGR -0.83 pp, mean dMaxDD -0.48 pp — i.e. on average it is worse on
  both), at **7 of 8 on B136** (mean dCAGR -1.31 pp for mean dMaxDD **+3.26 pp**, a real if
  expensive trade), and at **1 of 8 on SMALL663** (mean dCAGR -3.48 pp, mean dMaxDD -2.58 pp —
  strictly dominated by simply holding less).

## Rule 8 (walk-forward)
(n, GATE) chosen on warm-up..2016-12-31 by IS Sharpe alone; 2017-2026 read ONCE.
| panel | IS argmax | IS Sharpe | OOS Sharpe | grid-mean | anchor | IS/OOS rank corr | pick 4b |
|---|---|---|---|---|---|---|---|
| U56 | n=5, NONE | 1.2781 | 1.0187 | 1.1063 | **1.1759** | -0.0546 | FAIL |
| B136 | n=10, NONE | 1.3281 | 0.9677 | 1.0044 | 1.0240 | -0.7615 | FAIL |
| SMALL663 | n=25, BOTH | 0.7424 | 0.4088 | 0.5242 | 0.4534 | -0.2304 | FAIL |
Pooled: IS-chosen OOS Sharpe 0.7984 vs grid-mean 0.8783 (**-0.0799**) vs do-nothing anchor
0.8845 (**-0.0861**). **IN SAMPLE THE CHOOSER TURNS THE GATE OFF ON BOTH LARGE-CAP PANELS AND
IS WORSE OUT OF SAMPLE FOR IT ON ALL THREE, WITH THE IS/OOS RANK CORRELATION NEGATIVE ON ALL
THREE PANELS (-0.0546 / -0.7615 / -0.2304)**, and every IS-chosen cell fails 4b while the
anchor passes on U56. Turning the gate off is not an improvement either — it is the same
nothing, with the tail risk left in.

## Both KEEP paths
- **4a: 0 of 96.** Every cell's MaxDD is worse than live RULES v2's -12.05%.
- **4b: 13 of 32 (U56), 2 of 32 (B136), 0 of 32 (SMALL663).** The anchor passes on U56 only.
- **NO NEW BOOK, NO MEMO, NO RULES CHANGE.** Nothing here beats the incumbent.

## Survivorship (rule 9)
U56 and B136 are CURRENT-constituent lists; SMALL663 is a current sub-$2B screen (52 of 715
dropped for max_1d_move ≥ 1.0 before anything was computed). Levels are optimistic and every
4b pass is an upper bound. A current-constituent panel is **kind to GATE = NONE** — a name that
fell below its 200d MA and never recovered is disproportionately a name the screen dropped from
the panel — so the ungated arm's numbers are the more optimistic of the two and its wins here
are upper bounds on its wins.

## What the record should take, in one sentence
**THE 200d/vol SCREEN EARNS ITS PLACE IN THE RULES AS A TAIL CLAUSE ON THE SMALL-n END AND AS
NOTHING AT ALL AT THE COMMITTED n = 20, AND THE MEMOS' "de-gross to CASH" LANGUAGE DESCRIBES
BEHAVIOUR THE COMMITTED CODE DOES NOT HAVE** — the wording fix is proposed for the Sunday
review (rule 6) as a PROTOCOL/memo correction, not a rules change; rule 8 shows choosing on
this dial is negative-value.

Script: `research/backtests/2026-09-17_is-the-GATE-WORTH-NEGATIVE-on-the-BOOK-too-or-only-on-a-RANDOM-ORDERING_cloud.py`
Console: `..._cloud.console.txt` · Grid: `..._cloud.grid.csv` · Controls: `..._cloud.control.csv` · Walk-forward: `..._cloud.walkforward.csv`
