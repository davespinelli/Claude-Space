# Idea 1635 (lane cloud, 2026-09-19) — does the 2026-09-04 KEEP-4b TOP-20 BOOK survive a 1-DAY-DELAYED EXECUTION at 25 and 50 bps?

**ANSWERED = YES, BUT THE MARGIN THE PASS RUNS ON IS NOT THE ONE THE RECORD QUOTES.**
The candidate survives on U56 at every cost rung up to 50 bps and at execution lags out to L = 3
trading days. It does so, at the gross idea 1635's own text names (0.75), on a 4b drawdown margin
of **+1.10 pp that ONE further day of lag cuts to +0.16 pp** — a step of **−0.95 pp**, against
idea 1511's measured paired circular-block SE for a MaxDD contrast of **2.93 pp**. At the gross the
record actually certified (**0.65**, idea 1293) the same book carries **+3.50 pp** of margin and
clears 4b at **16 of 16** (L, c) cells including L = 5 at 50 bps. **KEEP-4b CONFIRMED at g = 0.65;
the g = 0.75 statement is DOWNGRADED to PARK.** Nothing is enacted; RULES.md is not modified.

**GATE: PASS.** (U56, N = 20, g = 0.65, L = 1, c = 10) reproduces idea 1293's certified candidate
to max |dev| **2.52e-03** (FULL 13.68% / 1.1540 / −16.73% vs 13.66% / 1.1526 / −16.73%; OOS 14.99% /
1.1858 vs 14.95% / 1.1833). Everything below is conditional on this.

## Design
Two adversarial axes and no more (rule 4): **L ∈ {1, 2, 3, 5}** trading days from the Friday
decision row to the application row (L = 1 is the engine's t+1 convention and the published
anchor) × **c ∈ {0, 10, 25, 50}** bps. **Neither is a dial a manager owns** — nobody chooses
their own fill lag or their own spread — so **no chooser is run over either**; the pre-registered
reading is the frontier. Panel {U56, B136, SMALL} is a replication axis; gross {0.75, 0.65} are
both frozen comparands, neither chosen by anything. **96 cells, every one published**
(`.grid.csv`). Frozen: N = 20, H = 126-row min hold, weekly Fri decision, above-200d & vol20 < 0.60,
3-leg composite, no vol scaler, equal weights, 260-row warm-up, cash at 0%.

## (1) The lag is ~5× more expensive than the cost, and it is paid ENTIRELY in drawdown
On U56 at g = 0.75 the 4b drawdown margin moves **−0.367 pp per day of lag** but only **−0.08 pp
per 25 bps of cost**. CAGR is nearly flat in L (L = 2 at 10 bps is **+0.11 pp/yr** vs the anchor;
L = 5 is −0.32 pp) and Sharpe barely moves (+0.0024 at L = 2). The entire price of a later fill
shows up on the leg that was already binding:

| U56, g 0.75, 10 bps | L=1 | L=2 | L=3 | L=5 |
|---|---|---|---|---|
| CAGR | 15.82% | 15.92% | 15.80% | 15.50% |
| Sharpe | 1.1543 | 1.1567 | 1.1497 | 1.1263 |
| MaxDD | −19.13% | −20.07% | −20.07% | −20.60% |
| 4b DD margin | **+1.10** | **+0.16** | **+0.16** | **−0.37** |
| 4b | pass | pass | pass | **FAIL (b_dd)** |

## (2) The cost question idea 1635 actually asked: answered YES
At L = 1 the book clears 4b at **0, 10, 25 AND 50 bps** on U56 at both grosses (DD margin +1.15 /
+1.10 / +1.02 / +0.90 at g = 0.75). Cost alone does not break it. The 50 bps rung costs
−1.27 pp/yr of CAGR and −0.082 of Sharpe, and the CAGR floor still clears by +3.96 pp.

## (3) The frontier (largest L at which every 4b leg still passes)
| panel | gross | 0 bps | 10 bps | 25 bps | 50 bps | binding leg at L=1 |
|---|---|---|---|---|---|---|
| U56 | 0.75 | 3 | 3 | 3 | 3 | — |
| U56 | **0.65** | **5** | **5** | **5** | **5** | — |
| B136 | 0.75 | — | — | — | — | b_dd (already −0.51 at L=1) |
| B136 | 0.65 | 3 | 3 | 3 | — (b_h2) | — |
| SMALL | 0.75 / 0.65 | — | — | — | — | all five legs |

The OOS-only 4b reading (scored against SPY's **own** OOS bars) gives the identical frontier in
every one of the 24 (panel, gross, cost) rows.

## (4) g = 0.65 is not a smaller book — it is a materially more lag-robust one
| U56, g 0.65 | CAGR | Sharpe | MaxDD | H1 / H2 (SPY 0.957 / 0.825) | OOS CAGR | OOS Sharpe | DD margin |
|---|---|---|---|---|---|---|---|
| L = 1, 10 bps | 13.68% | 1.1540 | −16.73% | 1.207 / 1.121 | 14.99% | 1.1858 | **+3.50** |
| L = 5, 50 bps | 12.33% | 1.0442 | −18.17% | 1.099 / 1.010 | 13.66% | 1.0811 | **+2.06** |

The worst cell in the entire 16-cell (L, c) box at g = 0.65 still clears every 4b leg, and its DD
margin (+2.06 pp) is larger than the g = 0.75 book's **best** cell (+1.15 pp). Giving up 2.1 pp/yr
of CAGR buys 2.4 pp of margin on the leg that decides the verdict.

## (5) 4a passes 0 of 96, as expected, and that is not news
Live RULES v2 draws down −12.05% on U56. No cell of a 15%-CAGR growth book comes near that. Path
4a cannot adjudicate this family; 4b is the path that matters here (PROTOCOL rule 4b's own text).

## (6) The IS-only chooser over L, reported and LABELLED ILLEGITIMATE
It picks **L = 2 in 24 of 24** (panel, gross, cost) cells and its OOS Sharpe is **worse than the
honest L = 1 reading in 24 of 24** (mean −0.0147). Published so the record cannot later quote it.

## Caveats
- **The g = 0.75 pass is inside its own measurement error.** +1.10 pp of DD margin against idea
  1511's 2.93 pp paired SE is ~0.38 SE. This run does not bootstrap; it reports the point margin
  and the published SE side by side and declines to call that pass robust.
- **Survivorship (rule 9).** U56 / B136 / SMALL are current-constituent lists (SMALL: 665
  investable after dropping 54 tickers with `max_1d_move ≥ 1.0` from `data/small_meta.csv`). Every
  number here is an upper bound; the SMALL panel's above all. Its 0 of 32 is therefore the strong
  reading.
- **L models fill TIMING, not fill PRICE.** A late fill here trades at that day's close, with no
  extra slippage beyond the c rung. Real late fills are also worse fills, so the frontier is, if
  anything, optimistic.

Artifacts: `.grid.csv` (96 cells), `.frontier.csv` (24 rows), `.decay.csv` (32 rows),
`.walkforward.csv` (24 rows), `.console.txt`, `.memo.md`.
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified.
