# Idea 441 — publish-the-HALF-WINDOW-beside-every-published-crossing (lane C, 2026-09-08)

**ANSWERED. The back-fill is complete over all 10 of idea 439's admitted items (the queue's
2 interior crossings + 6 edge/argmax readings, plus the 2 non-locations), and the proposed
columns are worth adopting — but NOT for the reason the queue gives, and not in the form it
proposes. The queue's premise is wrong twice: only 1 of the 10 readings was produced by a
smoothing window at all, and that one run DOES publish its half-window (±0.075) in its own
result.md. What is missing is one level up: of the 15 committed LEADERBOARD rows that publish
a location for these runs, 0 carry the half-window, 4 a grid step and 3 an interiority word.
And the sensitivity that costs money is not the crossing — it is the ARGMAX, which is what 6
of the 8 back-filled readings actually are: on live prices the same IS curve yields 1 adopted
band under a crossing read and 8 distinct bands under an argmax read, worth 0.084 of OOS
Sharpe and 4.5 pp of OOS drawdown.** No RULES change, no KEEP claimed; `RULES.md`, `scan.py`,
`bot.py` and `baseline.py` untouched.

Script: `research/backtests/2026-09-08_publish-the-HALF-WINDOW-beside-every-published-crossing_C.py`
Artefacts: `.console.txt`, `.provenance.csv`, `.backfill.csv` (180 re-reads), `.splithalf.csv`,
`.bookgrid.csv` (252 books), `.walkforward.csv`, `.keeppaths.csv`.

Idea 439's committed frame (`ITEMS`, `local_curve`, `crossing_of`, `argmax_of`, `make_grid`,
`fast_backtest`, min-cells-in-window 5, the interiority convention) is **imported from its
script, not re-implemented**, so the census scope is the record's own.

## Reproduction gate — before any new number was read

| check | published | this run | |
|---|---|---|---|
| idea 219's cells | 560 | 560 | MATCH |
| its crossing at its own half-window (0.075) | 0.425 | 0.425 | MATCH |
| its last non-positive centre | 0.400 | 0.400 | MATCH |
| `fast_backtest` vs `engine.backtest`, RULES v2 / U56 @10 bps | — | max abs diff **0.000e+00** | MATCH |

## (1) THE BACK-FILL — the three proposed columns, filled in

Mechanical: a run "smoothed" iff its committed script contains one of the record's own
smoothing constructs (`local_curve`, `HALF_W`, `half_w`, `local-window`); it "states" the
window iff its result.md/console.txt carries one of the prose forms. Every hit is printed
with its file and line in `.console.txt`, so each call is checkable by hand.

| item | census class | published location | **half-window** | **grid step** | **interior?** |
|---|---|---|---|---|---|
| 219 | interior crossing | **0.425** | **0.075 (3 steps)** | 0.025 | **INTERIOR** |
| 168c | interior crossing | kind only (live k = −0.5 loses to k = 0, 32/32) | none (unsmoothed) | 0.25 | n/a — no numeric location |
| 167 | edge/argmax/no-crossing | kind only (no crossing, 12/12) | none (unsmoothed) | 0.1 | n/a — no numeric location |
| 159B | edge/argmax/no-crossing | kind only (no crossing in [0.05, 0.70]) | none (unsmoothed) | 0.1 | n/a — no numeric location |
| 168B | edge/argmax/no-crossing | kind only (argmax at the grid EDGE) | none (unsmoothed) | 0.25 | n/a — no numeric location |
| 103 | edge/argmax/no-crossing | kind only (positive throughout) | none (unsmoothed) | 0.0346 | n/a — no numeric location |
| 277 | edge/argmax/no-crossing | kind only (non-monotone, no turn located) | none (unsmoothed) | 0.125 | n/a — no numeric location |
| bandgate | edge/argmax/no-crossing | kind only (gap rises in band) | none (unsmoothed) | 0.025 | n/a — no numeric location |
| 159c | not a pooled-curve location | 0.85 (FITTED log-linear) | none (unsmoothed) | 0.08 | n/a — not on this curve |
| 61 | not a pooled-curve location | ~0.5 flips/tkr/yr (per-pool sign) | none (unsmoothed) | 0.3476 | n/a — not on this curve |

**"none (unsmoothed)" is a value, not a gap:** 9 of the 10 runs read their curve as per-x cell
means with no window at all, so a half-window column would be empty by construction. Counts:
numeric location published **3 of 10** (only **1** of them a location on its own committed
curve); smoothed **1 of 10**; half-window recoverable from the script **1 of 10**; stated in
the run's own result.md **1 of 10** (`local-window (±0.075)`, at line 130 of item 219's
result.md); grid step recoverable from the committed cells **10 of 10**.

**Where the gap really is — the LEADERBOARD row.** Across the 67 committed rows belonging to
these 10 runs, **15 publish a location**; of those, **0 carry the half-window**, 4 a grid step
and 3 an interiority word. Item 219's own row (LEADERBOARD:2390) publishes
`crossing 0.425, block-bootstrap 90% CI [0.200, 0.450]` with no window, no step and no
interiority flag, though its result.md has all three. **The queue's complaint is true of the
LEADERBOARD and false of the result.md**, which is exactly the level the proposal targets.

## (2) HOW FAR THE READING MOVES — 6 half-windows × 3 grid steps, all 180 points published

P1 `hmult ∈ {0.5, 1, 2, 3, 4, 5}` (0.5 = non-overlapping bins). P2 `smult ∈ {1, 2, 4}`
(coarsen the item's own committed grid; a finer grid than the committed ladder does not exist
for the 9 unsmoothed items). Span in the item's finest grid steps:

| item | distinct readings | span (both) | span from half-window alone | span from grid step alone | split-half noise floor |
|---|---|---|---|---|---|
| **219** | 9 | **12** | 3 | 9 | **3.40** |
| **168c** | 5 | **5** | 5 | 2 | 0.30 |
| bandgate | 2 | 1 | 1 | 0 | 0.00 |
| 167 / 159B / 159c / 103 / 277 | 1 | 0 | 0 | 0 | 0.00 / 0.00 / 0.00 / 0.40 / 2.29 |
| 168B / 61 | 0 (never uniformly positive) | — | — | — | — |

**Only the 2 interior crossings move at all** (plus 1 step on bandgate): 3 of 8 items with a
defined reading, mean span 2.25 steps. **On the seed item the half-window's own span (3 steps)
is smaller than the split-half sampling noise (3.40 steps)** — so the queue's "up to 4 grid
steps" is real but is not distinguishable from re-drawing the cells; it is the *joint*
(window × grid) span of 12 steps that exceeds the noise floor. The grid step moves item 219
three times as far as the half-window does.

## (3) RULE 8 (ii), LIVE PRICES — what the missing columns cost

252 fresh books: 3 panels (U56 56, B136 136, SMALL439 484 names) × gross {0.75, 1.00} ×
cadence {W, M} × 21 band widths (0.00–0.20 step 0.01), 10 bps, t+1. x = band width, y = IS
(≤ 2016-12-31) Sharpe minus the same cell's bare-200d IS Sharpe. The threshold is read off the
IS curve at all 18 (half-window, grid step) points; 2017-2026 is read once.

| reading | adopted band(s) | OOS CAGR | OOS Sharpe | OOS MaxDD |
|---|---|---|---|---|
| **CROSSING read**, all 18 points | 0.01 (invariant) | 8.67% | **1.0301** | −14.94% |
| **ARGMAX read**, 18 points | **0.01–0.19, 8 distinct** | 8.67–8.90% | **0.9458–1.0301 (range 0.0843)** | **−14.94% to −19.41% (range 4.47 pp)** |
| bare 200d (band 0) | 0.00 | 8.52% | 1.0195 | −14.78% |
| live RULES v2 band | 0.03 | 8.74% | 1.0136 | −15.87% |
| ORACLE (best OOS band per cell) | — | 8.97% | 1.0496 | −16.00% |

**The whole edge of the best reading over the bare gate is +0.0106 of OOS Sharpe; the argmax's
window-and-grid ambiguity is +0.0843, eight times larger.** A published argmax without its
(half-window, grid step) is therefore not reproducible to within its own effect size, while a
published crossing on this curve is. That is the empirical case for the columns, and it lands
on the reading kind the record actually publishes most: 6 of the 8 back-filled readings.

Benchmarks, same OOS window: SPY 15.45% / 0.8822 / −33.72%. RULES v2 (live) @10 bps: U56
9.53% / 1.2853 / −12.05%, B136 7.98% / 1.1187 / −12.24%, SMALL439 4.55% / 0.6630 / −12.09%.
RULES v1 @10 bps: U56 7.73% / 0.7472 / −13.83%, B136 5.94% / 0.5764 / −21.19%, SMALL439
17.15% / 0.5542 / −44.83%.

## (4) Both KEEP paths on all 252 books

| panel | books | 4a pass | 4b pass |
|---|---|---|---|
| U56 | 84 | 0 | 34 |
| B136 | 84 | 0 | 20 |
| SMALL439 | 84 | 1 | 0 |
| **total** | **252** | **1** | **54** |

**All 54 4b passes are gross 1.00** — the live book's cash carve-out removed, at every band
from 0.00 to 0.20, i.e. idea 439's finding reproduced on a finer grid and still a dial
placement, not a book (idea 144: a re-dialled book is the same book). The single 4a pass is
SMALL439 gross 0.75 / W / band 0.04 (Sharpe 0.624 vs live v2's 0.615, halves 0.556/0.686 vs
0.542/0.680, MaxDD −12.06% vs −12.09%) — the live book with its band moved one step, inside
the noise of the dial it moves. **No KEEP is claimed**; the grid also runs three dials, above
a KEEP's two-parameter budget, because it is the instrument of the census and not a book search.

## Verdict

**ANSWERED — the proposal is worth adopting, in a narrower form than the queue writes it, and
the queue's stated motivation is corrected.** Offered as wording only; PROTOCOL/LEADERBOARD
changes are a Sunday-review decision.

**Proposed wording.** *Any LEADERBOARD row that publishes a LOCATION on a curve — a crossing,
a threshold, a floor, an argmax, or an explicit "no location exists" — must carry, in its own
cell, three items in this order:*
`x-grid <min>..<max> step <s>; half-window <h> (= <h/s> steps), or "unsmoothed"; INTERIOR | EDGE | NO LOCATION`.
*An ARGMAX may not be published without them at all: on the record's own dial curves the
argmax moves 8 distinct grid points, and 0.084 of OOS Sharpe, on the smoothing pair alone.
A crossing published without them is a PARK, not a result.*
