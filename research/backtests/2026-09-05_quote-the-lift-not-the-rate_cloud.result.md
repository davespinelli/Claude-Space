# Idea 149 — quote-the-lift-not-the-rate (cloud, 2026-09-05)

**ANSWERED. The CONDITIONING ARTIFACT generalises and is worse than idea 141 found; the
PRESCRIPTION does not. "Quote the lift" is the wrong fix for these two statistics — the right
fix is to quote the CELL SET. No RULES change, no new book, no KEEP candidate.**

Script `2026-09-05_quote-the-lift-not-the-rate_cloud.py`; outputs `.console.txt`, `.grid.csv`,
`.anchor.csv`, `.published.csv`, `.sweep.csv`, `.walkforward.csv`; proposed clause in `.memo.md`.

## Reproduction, before any new number was read (P0 HELD, all four checks exact)

| check | target | this run |
|---|---|---|
| [a] `H.run` vs `engine.backtest`, 3 ungated books x 3 panels | 0 | **0.000e+00** |
| [b] idea 141's 306-row grid, 15 columns | < 1e-9 | **306/306, max 2.22e-16, 0 adm_S1 disagreements** |
| [c] idea 129's POINT census at m=1.00 | 306 / 29 / 27 | **306 / 29 / 27** |
| [d] idea 90's family (7,650 rows) — this run's 306 rows vs its m=1.00 slice, and its census | 72 / 58 / 29 | **306 matched at 2.22e-16; 72 / 58 / 29** |

Section C reads idea 90's committed `.family.csv.gz` rather than re-deriving the 7,650-point
gross sweep; check [d] is what licenses that, and it is stated rather than buried.

## Corpus and grid

3 panels (u56 / broad / small) x 3 books (V1u, TOP20, EWall) x 2 cost rungs (10, 25 bps) = 18
cells x 17 arms = **306 backtests**, weekly, t+1, no leverage. Exactly two tuned parameters:
screen tightness `qmax` in {0.25, 0.50, 0.75, 1.00} and the conditioning convention in
{COND, UNCOND} = **8 grid points per statistic, all printed**, at 4,000 bar draws per (cell,
qmax) and 20,000 size-matched null draws per published-bar statistic.

## (1) The anchor re-derives (P0)

Idea 141's immunity statistic, with this run's own independent draws, agrees to a maximum of
**0.0039** over 20 (selector, qmax) points — Monte-Carlo agreement, not identity, and reported
as such. Its signature is reproduced: K_Sharpe raw **0.787 -> 0.674 -> 0.634 -> 0.651**
(non-monotone) against lift **0.215 -> 0.332 -> 0.418 -> 0.489** (monotone).

## (2) THE ARTIFACT GENERALISES, and it is total rather than partial (P1 HELD, harder than predicted)

The prediction was that idea 90's headline would be inflated by a factor >= 2. It is inflated
by **everything it has**:

| statistic | as the project quotes it | with the dropped cells restored |
|---|---|---|
| idea 90's operational KEEP, m <= 1.30 (non-empty 4b gross interval in every cell) | **4 of 51 (book, arm) pairs** | **0 of 51** |
| the same at m <= 1.00 | 3 of 51 | **0 of 51** |
| idea 129's POINT census read the same way (pass 4b in every cell) | 2 of 51 | **0 of 51** |

Per-cell counts are the whole story: interval non-empty in u56@10 **31**, u56@25 **23**,
broad@10 **14**, broad@25 **4**, **small@10 0, small@25 0**; 4b point passes 14 / 9 / 4 / 2 /
**0 / 0**. Because a joint "passes in every cell" requirement is multiplicative, one empty cell
zeroes it — so dropping the two small-panel cells is not a rounding convention, it is the
difference between a statistic and nothing.

The sweep confirms the same channel under randomised bars: at the tightest screen the COND
convention (drop empty cells, then require all the rest) reads **0.319** pairs against UNCOND's
**0.016**, a **20.2x** inflation; at qmax = 0.25 and 0.50 no cell is ever empty and the two
conventions are identical to the digit. The artifact is a function of how much mass the
convention conditions away, not of which statistic is being quoted.

## (3) BUT BOTH STATISTICS SURVIVE THEIR OWN SIZE-MATCHED NULL, decisively (P3 HELD)

Within the conditioned set, these are not chance findings:

| statistic | observed | size-matched null | lift | ratio | p (MC) |
|---|---|---|---|---|---|
| C — idea 90's cell count, m <= 1.30, 4 large-cap cells | **4** | 0.301 | +3.70 | **13.3x** | < 0.0001 |
| C — same, m <= 1.00 | 3 | 0.127 | +2.87 | **23.6x** | 0.0001 |
| B1 — idea 129's POINT census, pass 4b in all 4 cells | 2 | 0.0076 | +1.99 | **263x** | < 0.0001 |
| B2 — "floor-only KILL" share, 27 of 277 | 27 | 19.48 | +7.52 | **1.39x** | 0.0010 |

B2's null preserves each bar's per-cell failure count and randomises **which** arms fail, so the
1.39x is the part of idea 129's floor-only concentration that is not explained by the CAGR floor
simply failing often. It is real but small — the smallest lift of the four, and the honest
reading of "27 of 277" is "about 7 more than chance", not "27".

The RANDOM control lands on the null to **0.0020** at every qmax (P4 HELD), so the nulls are
trustworthy.

## (4) THE PRESCRIPTION FAILS: the lift is not automatically the better statistic (P2 FAILED, 0 of 8)

Idea 141's signature — raw non-monotone in tightness, lift monotone — appears in **0 of 8**
reported readings, and in one family it is **reversed**:

| statistic | RAW across qmax | LIFT across qmax |
|---|---|---|
| B1 best cross-cell pass rate (COND, large4) | 1.000 -> 1.000 -> 0.802 -> 0.649 (**monotone**) | 0.444 -> 0.678 -> 0.651 -> 0.573 (**non-monotone**) |
| C cell count (COND, large4) | 14.12 -> 3.70 -> 0.42 -> 0.32 (monotone) | 9.26 -> 3.15 -> 0.38 -> 0.15 (monotone) |

The mechanism is measurable and is the transferable part: idea 141's artifact needs the
conditioned-away mass to be large, and its cells hold **17** arms, so P(non-empty) falls to
**0.424** at qmax = 1.00. The statistics this run re-reads are defined over **51** (book, arm)
pairs per cell, where P(non-empty) never falls below **0.997**. Same convention, ~0 mass
conditioned away, no distortion of the raw rate. **"Quote the lift, not the rate" is a property
of idea 141's cell size, not a general prescription** — and where the raw rate is already
well-behaved, substituting the lift makes the reported quantity *worse*.

## (5) Rule 8 walk-forward — debiasing changes no pick, and every screen loses to doing nothing

Selectors read the IS window (<= 2016-12-31) only; picks read ONCE on 2017-01-01..2026, 18 cells,
equal-weighted.

| selector | OOS CAGR | OOS Sharpe | OOS MaxDD | vs S0 (paired) |
|---|---|---|---|---|
| S0 CONTROL (do nothing) | **10.65%** | **0.762** | -27.4% | — |
| S1 SHARPE (rule 8's incumbent) | 9.06% | 0.695 | -23.1% | -0.067, better in 3 of 18 |
| S2 RAW (cross-cell pass count) | 7.62% | 0.649 | -21.2% | -0.113, better in 6 of 18 |
| S3 LIFT (same, minus its size-matched expectation) | 7.62% | 0.649 | -21.2% | -0.113, better in 6 of 18 |
| S4 RANDOM (control) | 10.14% | 0.755 | -26.1% | -0.007, better in 2 of 18 |
| **SPY** | **15.45%** | **0.882** | **-33.7%** | — |
| RULES v1 (live book), by cell | 1.11%-7.92% | 0.155-0.747 | -13.8% to -43.0% | — |

**S3_LIFT picks the identical arm to S2_RAW in 18 of 18 cells** — debiasing a cross-cell pass
count by its size-matched null is a null operation on the decision, because the correction is
almost constant across arms within a cell. And every informed selector loses to the do-nothing
control, with a RANDOM admissible arm (-0.007) closer to S0 than any of them; P5 FAILED on that
clause. This is idea 141's "choosing among these selectors is worth nothing out of sample",
reproduced on a sixth and seventh statistic and with the sign now clearly negative.

**Both KEEP paths, on every distinct arm any selector picked**: 42 distinct (cell, arm) picks —
**13 pass 4a**, **6 pass 4b full-sample**, **5 pass 4b on the OOS window alone**. Every one is a
pre-existing leaderboard book (control, vol60-dg, ebud-0.10/0.20, band3-rw, abs12-rw, stop15,
v1gate-rw, ddctl-8/.5/recover). **No KEEP, nothing promoted.**

## Verdict

**ANSWERED. The artifact generalises (P1), the statistics survive their nulls anyway (P3), and
the prescription does not generalise (P2 FAILED).** The reporting fix this run recommends is not
idea 149's own — it is to quote the **cell set and the per-cell counts** alongside any joint
pass count, and to state the un-conditioned reading, because for a multiplicative statistic one
empty cell is the whole answer. Proposed clause in `.memo.md` for the Sunday review.

## Caveats carried

* **Survivorship**: all three panels are current-constituent lists (idea 54); the small panel
  drops the 44 tickers with `max_1d_move >= 1.0` and its SPY is a held-out benchmark, not a
  constituent. Every CAGR here is optimistic and no level in this file is an achievable return.
  It runs *against* this file's main finding, which is that the small panel admits nothing.
* **Idea 128**: the IS window's SPY drawdown is shallower than the OOS window's, so the IS
  drawdown bar is measured on a window that cannot express a deep drawdown; this biases every
  selector in section 5 identically.
* **Idea 38** (calendar-day price index) and **idea 126** (t+1 execution only) carry over.
* Section C inherits idea 90's family file; check [d] is what licenses that and nothing else.
* The randomised bars are drawn from each cell's own cross-arm distribution, so the sweep
  measures the screen's SHAPE, not 4b's economic content.
* This run selects among existing arms; it cannot promote a book and does not try to.
