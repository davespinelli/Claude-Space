# Idea 392 — price-the-VOLCAP-target-as-a-standalone-4b-arm-on-the-standing-parent (lane C, 2026-09-07)

**SPLIT: the queue's "g=1.00 corner" reading is KILLED — the corner is real but sits at the
OTHER end of the dial — and the VOLCAP target survives as a 4b KEEP-candidate at g=0.75 on
both panels under rule 8. No RULES change, no book promoted; RULES.md, scan.py, bot.py,
baseline.py and PROTOCOL.md untouched.**

## Gates (all PASS, printed before any new number is read)

| gate | reading |
|---|---|
| G1 `fast_bt` == `engine.backtest` (returns AND turnover, 0 and 25 bps) | **0.000e+00** |
| G2 book-level overlay at OFF (m == 1) == parent | **0.000e+00** |
| G3 matched-gross control at a = 1 == parent | **0.000e+00** |
| G4 SHARPE INVARIANCE of the gross dial (a in 0.25..1.00 x c in 0/10/25) | max \|dSharpe\| **2.2e-16** |
| G5 standing 2026-09-04 KEEP-4b row (published 12.7% / 1.09 / -18.3%, halves 1.09/1.10) | **12.66% / 1.092 / -18.31% (1.09/1.10)** |
| G6 **idea 335's two decisive cells rebuilt from source** | U56 g=1.00 VOLCAP 0.15 c* = **17.67** (published 17.67), its control **0.00** (published 0.00); DDCTL 0.10 c* = **11.67** (published 11.67) |
| G7 bisection determinism | \|dc*\| **0.000e+00** |

Panel integrity is asserted, not assumed: `baseline.load_universe(broad=True)` reaches
`data/prices_broad.csv` only through an exception path, so the script asserts the wide panel
really has >= 120 columns before reading a number off it.

## Design

Parent = idea 335's standing NF20 book (eligible = above 200d MA and vol20 < 0.60; rank the
eligible names by the v1 composite **without** the /sqrt(vol20) term; hold top k = min(20, E_t)
equal-weight at g/k; weekly, t+1). Two tuned parameters only: **gross g in {0.75, 0.85, 1.00}**
and the **VOLCAP target in {0.08, 0.10, 0.12, 0.15, 0.18, 0.20, 0.25, 0.30}** (+ OFF).
Panel (U56 / B136) and cost rung (0 / 10 / 25 bps) are census axes — **all 54 grid points
reported** in `.grid.csv`, all 54 binding-bar rows in `.bars.csv`, all 18 walk-forward rows in
`.walkforward.csv`. VOLCAP uses idea 41/335's convention verbatim (`r = m*r0`,
`turn = m*turn0 + |dm|*gross0`). The matched control is the plain gross dial held at the
overlay's own realised mean exposure, closed form.

**INFORMATIVE cell** = the matched control's own c* > 0, i.e. the comparand is admissible at
zero cost. Where it is not, any positive c* "widens" by construction and the number prices the
CONTROL, not the overlay (this is idea 393's fix, applied to one family).

## Findings

**(1) The queue's premise is INVERTED.** The widening is not a g=1.00 corner. At **g=1.00** it is
entirely degenerate — U56 informative 3/8, widened **0/3**; B136 2/8, widened **0/2**. The only
rung carrying an informative widening is the **lowest**, g=0.75 on B136 (**5/7** full-sample,
**6/7** OOS, median **+2.37 / +8.86 bps**). The queue's own decisive cell (U56 g=1.00 VOLCAP
0.15, c* 17.67 against a control at 0.00) reproduces to the digit and is **degenerate**: its
comparand already fails a 4b bar at zero cost.

**(2) Over the cells that can speak, the identity direction mostly holds.** Census over 48 tuned
cells x 3 windows = 144 readings: **81/144 (56.2%) are DEGENERATE**; of the 63 informative
readings the overlay widens c* in **19 (30.2%, binomial sd 0.058)**, so
`c*(overlay) <= c*(matched gross)` survives in **44/63 (69.8%)**. It is a tendency, not an
identity — idea 335's KILL of the identity stands — but the headline "widening" rate falls from
37.5% (all cells) to 30.2% once the degenerate comparands are dropped. **Direct support for
idea 393.**

**(3) As a standalone 4b arm the target is real but rung- and panel-bounded.** 4b passes:
**36/54 at 0 bps, 21/54 at 10 bps, 0/54 at 25 bps.** 4a against live RULES v2: **0/54 at every
rung.** Binding-bar census at 10 bps: **DD 20, H2 20, CAGR 14** — the cap trades CAGR for DD, so
tight targets die on the CAGR floor and loose ones die on the DD cap.

**(4) Rule-8 walk-forward (targets chosen on 2008-2016 only, 2017-2026 read once).** The
IS-Sharpe chooser picks **0.18 on U56 and 0.20 on B136 at g=0.75**, and both clear 4b
full-sample AND out of sample:

| book (10 bps) | CAGR | Sharpe | MaxDD | H1 / H2 | OOS Sharpe |
|---|---|---|---|---|---|
| **U56 g=0.75 VOLCAP 0.18** (IS pick) | 12.7% | 1.084 | -15.3% | 1.091 / 1.083 | **1.150** |
| U56 g=0.75 un-capped parent | 12.8% | 1.070 | -18.3% | 1.076 / 1.072 | 1.137 |
| **B136 g=0.75 VOLCAP 0.20** (IS pick) | 13.1% | 0.982 | -18.1% | 1.126 / 0.853 | **0.934** |
| B136 g=0.75 un-capped parent | 13.0% | 0.943 | -20.1% | 1.105 / 0.802 | 0.883 |
| SPY | 15.2% | 0.889 | -33.7% | 0.957 / 0.834 | 0.882 |
| live RULES v2 (U56) | 9.5% (OOS) | — | -12.1% (OOS) | — | 1.285 |

OOS window: SPY CAGR 15.5%, Sharpe 0.882, MaxDD -33.7%; the 4b bars are CAGR >= 10.85% and
MaxDD <= -20.23%. The chooser buys **3.0 pp of drawdown on U56 and 2.0 pp on B136 for
essentially no CAGR** (-0.1 pp / +0.1 pp) and **+0.014 / +0.051 of OOS Sharpe**.

**(5) The chooser matters more than the dial.** Selecting the target on **IS Sharpe@10** walks
forward: OOS Sharpe beats the un-capped parent in **6/6** cells (mean **+0.0307**), beats SPY in
**6/6** (mean +0.1592), regret against the OOS oracle only **-0.0069**. Selecting it on
**IS c*_4b** — the statistic idea 335's question is about — does **not**: **3/6** (mean
**-0.0250**), regret **-0.0626**. c* is not a usable in-sample selector on this dial.

## Verdict

**KILL** of the queue's "the widening is a g=1.00 corner" reading, and a **restatement**: the
corner is real but inverted — g=1.00 is where the comparand is inadmissible and the widening is
purely bookkeeping, while g=0.75 is where an informative widening actually survives (B136 only).
**4b KEEP-candidate filed** for the g=0.75 walk-forward pick, with the honest caveat that it
improves the standing parent by +0.014 OOS Sharpe on U56 and buys its DD with a second dial;
it is **not** offered as a replacement for the standing 2026-09-04 candidate. Memo:
`2026-09-07_volcap-g075-4b_C_MEMO.md`.

## Caveats

(1) `universe.json` (56) and `universe_broad.json` (136) are **current-constituent** lists —
survivorship; absolute CAGRs are optimistic on both, and B136 **contains** U56, so two panels
are not two independent samples. (2) Gross is capped at 1.00 (PROTOCOL rule 2); a c* that only
leverage could move is reported as unmoved. (3) c* is a breakeven, not a return — the 10-bps
levels are reported beside every budget in `.grid.csv`. (4) The 4a comparand moves with the rung
too, so 0/54 on 4a is partly a statement about RULES v2's own cost path. (5) The whole family
fails 4b at 25 bps; the record's cost wall (idea 58) is unclosed here as everywhere.
