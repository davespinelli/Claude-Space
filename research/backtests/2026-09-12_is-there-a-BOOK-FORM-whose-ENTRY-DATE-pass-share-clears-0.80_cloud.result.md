# Idea 828 — is-there-a-BOOK-FORM-whose-ENTRY-DATE-pass-share-clears-0.80-at-a-3-YEAR-HORIZON (cloud, 2026-09-12)

**ANSWERED = NO, AND THE QUEUE'S MECHANISM IS BACKWARDS. 0 of 21 (form × gross) cells clear 0.80;
the best book at a 3-year horizon is the one the record already holds, at 0.3977. CAGR
co-movement buys the CAGR leg and loses the DD leg at almost exactly the same rate, because both
4b legs are ratios to SPY driven by ONE dial — gross — in opposite directions.**
Script: `2026-09-12_is-there-a-BOOK-FORM-whose-ENTRY-DATE-pass-share-clears-0.80_cloud.py`.
**KILL for capital. No KEEP claimed, no book promoted, no memo, no RULES/PROTOCOL change.**

## Gates (printed before any new number was read)

| gate | what | result |
|---|---|---|
| G1 | `fast_backtest` == `engine.backtest`, returns AND turnover, 3 books × 3 rungs | 4.996e-16 **PASS** |
| G2 | fast CAGR/Sharpe/MaxDD == `engine.metrics`, 200 real series | 2.220e-16 **PASS** |
| G3 | **idea 829's committed entry-date headline** (CAND g=1.00, U56, H=756, s=21, 10 bps) | this run **0.3977** vs committed 0.3977, \|diff\| **0.0000** **PASS** |
| G4 | the committed candidate memo's fixed-window triple | full 11.54%/1.2017/−15.91% (pub 11.52/1.1996/−15.91); OOS 12.70%/1.2775/−15.91% (pub 12.66/1.2740/−15.91); SPY 15.16%/0.8861/−33.72% **PASS** |
| G5 | idea 84's EWALL U56 g=0.85 @10bps | 11.75% / 1.046 / −17.89% **PASS** |
| G6 | panel vintage stamp | 664 cols − 52 (`max_1d_move ≥ 1.0`) → **SMALL663** |

Because G3 lands exactly, the 0.3977 this run is trying to beat is this run's own number, not a
quoted one.

## The sweep — joint window-local 4b pass share, U56, H = 756d, s = 21d, 10 bps, 176 entry windows

| form \ gross | 0.50 | 0.75 | 1.00 |
|---|---|---|---|
| EW (no gate) | 0.0682 | 0.0057 | 0.0000 |
| EWALL-RS | 0.0284 | 0.1193 | 0.0000 |
| EWALL-DG | 0.0057 | 0.1023 | 0.1875 |
| **MA-DG** (RULES v2 form) | 0.0227 | 0.1875 | **0.3977** |
| MA-RS | 0.1761 | 0.3182 | 0.0057 |
| TOP20 | 0.1364 | 0.1534 | 0.0000 |
| LOWVOL20 | 0.0000 | 0.0057 | 0.0909 |

*(comparands at the same cell: RULES v2 live 0.1875, RULES v1 0.0114)*

**H_828 FAILS: 0 of 21.** The sweep's best cell **is the standing candidate itself**. Nothing in
the record's committed book forms does better at a 3-year horizon, on any panel, spacing or rung:
the best H=756 reading anywhere in the run is MA-DG g1.00 on U56 at 0.3977 (B136 tops out at
0.2557, SMALL663 at 0.2105).

## Why — the two legs are one dial pulling in opposite directions

The queue's hypothesis was that a form whose **CAGR co-moves** with the benchmark would clear the
floor. Measured as the slope of each cell's window CAGR on SPY's window CAGR across the 176 entry
windows, that half is emphatically true — and useless:

| statistic | Spearman over the 21 cells | hypothesis |
|---|---|---|
| slope vs **leg_cagr** | **+0.8759** | co-movement does buy the CAGR floor |
| slope vs **leg_dd** | **−0.8806** | and gives back the DD cap at the same rate |
| slope vs **joint pass_4b** | **−0.1975** | **H_SLOPE FAILS** |

**H_COST PASSES** at −0.8806; **H_JOINT PASSES** — 0 of 21 cells clear both legs at 0.80.

The mechanism is not subtle. Across **7 of 7 forms**, `leg_cagr` is **monotone increasing** in
gross and `leg_dd` is **monotone decreasing** in gross:

| form | leg_cagr @ 0.50 / 0.75 / 1.00 | leg_dd @ 0.50 / 0.75 / 1.00 |
|---|---|---|
| EW | 0.0682 / 0.8864 / 1.0000 | 1.0000 / 0.0057 / 0.0000 |
| MA-DG | 0.0227 / 0.2443 / 0.7273 | 1.0000 / 0.9545 / **0.8636** |
| MA-RS | 0.1932 / 0.7500 / 0.9886 | 1.0000 / 0.6023 / 0.0057 |
| TOP20 | 0.2443 / 0.7784 / 0.9432 | 0.9773 / 0.3636 / 0.0000 |

The limiting case settles it: **EW g=1.00 — the panel itself — has slope 0.8962, passes the CAGR
leg in 176 of 176 windows, and passes the DD leg in 0 of 176. Joint share 0.0000.** Only 1 of 21
cells reaches slope ≥ 0.70 (the level 4b's ratio floor actually needs) and that cell passes zero
windows. A book that tracks the benchmark's return inherits the benchmark's drawdown, and 4b caps
drawdown at 60% of it.

**MA-DG g=1.00 wins the sweep for one structural reason:** de-grossing to *cash* is the only one of
the seven forms that raises CAGR without proportionally raising drawdown — its `leg_dd` is still
0.8636 at gross 1.00 where every re-spreading form has collapsed to ≤0.0057. That is the whole of
its 0.3977, and it is still less than half the bar.

## Horizon, spacing, cost, panel (all reported, none tuned)

* **Horizon is the binding axis, not form.** MA-DG g1.00 runs 0.3977 (H=756) → **0.6513** (H=1260,
  s=21) → **0.6863** (H=1260, s=63). The 0.80 bar is not reached at 5 years either.
* **Cost bites**: 10 → 25 bps takes the headline 0.3977 → 0.3409 and MA-RS g0.75 0.3182 → 0.2159.
* **Panels**: B136 max 0.2557 (MA-DG g1.00); **SMALL663 max 0.2105** and 0.0000 for 18 of 21 cells
  at the headline. Nothing survives the small panel.

## PROTOCOL rule 8 — **FAILS**

Choosing on IS entry dates (entry ≤ 2016-12-31, n=96) and reading OOS entry dates (n=80) untouched:

| cell | IS pass share | OOS pass share |
|---|---|---|
| **MA-DG g1.00** (the IS pick) | 0.2812 | 0.5375 |
| **MA-RS g0.75** (the OOS best) | **0.0000** | **0.7000** |
| TOP20 g0.75 | 0.0000 | 0.3375 |

Gap 0.1625 > 0.15 → **H_R8 FAILS**, and the detail is worse than the headline: the OOS-best cell
passes **zero** of 96 in-sample entry windows, and the IS pick's own share drifts **+0.2562**. The
entry-date pass share is not a stable property of a book form — it is a property of the window,
which is the same second-window character ideas 605/609/825/829 keep finding.

## Fixed window (PROTOCOL 3 & 4, every cell, never selected on)

At 10 bps: **4a 0 of 24 on every panel**; 4b 3 of 24 on U56 (MA-DG g1.00, MA-RS g0.75,
TOP20 g0.75), 3 of 24 on B136, **0 of 24 on SMALL663**. The gap the queue is about, laid out:

| panel | book | CAGR | Sharpe | MaxDD | fixed 4b | **entry-date share (H=756)** |
|---|---|---|---|---|---|---|
| U56 | MA-DG g1.00 | 11.54% | 1.2017 | −15.91% | PASS | **0.3977** |
| U56 | MA-RS g0.75 | 12.21% | 1.1575 | −17.71% | PASS | 0.3182 |
| B136 | MA-DG g1.00 | 10.65% | 1.0992 | −16.16% | PASS | 0.2557 |
| U56 | TOP20 g0.75 | 12.65% | 1.0918 | −18.31% | PASS | 0.1534 |
| B136 | EWALL-RS g0.75 | 10.66% | 1.0211 | −17.69% | PASS | 0.0227 |

Every book that passes 4b on the record's one fixed window fails it for **at least 60%** of the
entry dates an actual investor could have started on.

## Verdict

**KILL.** The answer to the queue's question is no, and the reason generalises past this idea:
PROTOCOL 4b's CAGR floor and DD cap are both ratios to SPY, and in every committed book form they
are moved in opposite directions by the single dial (gross) that the record tunes. There is
therefore no book form on this corpus whose 3-year entry-window pass share can clear 0.80 by
co-moving harder — the joint share peaks at an interior gross for every form and never at an end.
Anything that clears the bar would have to break the leg-vs-leg opposition (a book whose drawdown
is structurally shallower than its return would imply — i.e. the de-grossing-to-cash channel that
already gives MA-DG its 0.3977), not track the benchmark more closely. Two follow-ups are filed.

*Survivorship: all three panels are current constituents only (U56/B136 from `universe.json` /
`universe_broad.json`, SMALL663 from a sub-$2B screen that is re-stated nightly — see
`data/SMALL_PANEL_README.md`). Every pass share above is biased upward. Research, not investment
advice.*
