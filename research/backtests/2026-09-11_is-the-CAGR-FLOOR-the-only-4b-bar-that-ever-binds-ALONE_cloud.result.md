# Idea 691 — is the CAGR FLOOR the only 4b bar that ever binds ALONE?

**2026-09-11, cloud lane. Verdict: ANSWERED — premise HALF-CONFIRMED, strong form KILLED, and one
NEW PROTOCOL DEFECT found (4b's OOS leg is redundant with its own H2 leg).**
No RULES change, no book promoted, no PROTOCOL edit. RULES.md, PROTOCOL.md, scan.py, bot.py and
baseline.py untouched.

Script `2026-09-11_is-the-CAGR-FLOOR-the-only-4b-bar-that-ever-binds-ALONE_cloud.py`.
Artefacts: `.grid.csv` (450 rows), `.uniquecut.csv`, `.barsets.csv`, `.rungsens.csv`,
`.walkforward.csv`, `.console.txt`.

## Gates (all printed before any result was read)
| gate | got | bar | |
|---|---|---|---|
| G1 `fast_backtest` == `engine.backtest` (U56 BAND03 @10bps) | 6.94e-18 | 1e-12 | PASS |
| G1b engine NaN rows all inside the discarded 260-row warm-up | row 3 | < 260 | PASS |
| G2 `band_book(0.03,0.75)` == `baseline.rules_v2_weights` | 0 | 0 exact | PASS |
| G3 SMALL panel = 483 − 44 (`max_1d_move>=1.0`) = 439 names | 439 | 439 | PASS |
| G4 cost rung 0 reproduces the gross return | 0 | 1e-15 | PASS |
| G5 SPYBH(g=1.00) tracks SPY buy-and-hold Sharpe | 0 | 0.01 | PASS |
| G6 unique-cut count == sole-blocker count, every (bar, rung) | equal | 0 exact | PASS |

Two gates failed on the first execution and were corrected before any number was read: G1 compared
against `engine.backtest`'s NaN warm-up rows (now masked, with G1b added to prove the NaNs cannot
reach a reported row), and G3 was written against a mis-stated panel size (the small panel is 483
names, not 484, so the filtered panel is 439 — the gate bar was wrong, the data was not).

## Corpus (nothing here was chosen by looking at an outcome)
3 panels (U56, B136, SMALL439) × 10 committed book families × 3 committed gross rungs
{0.50, 0.75, 1.00} = **90 arms**, each run at **5 cost rungs** {0, 10, 25, 50, 100} bps = 450 rows.
Families are idea 670's ten, restated verbatim. Two tuned parameters and no more: **BARSET**
(5 values) and **RUNG** (5 values); all 25 points reported.

## Result 1 — the floor is the biggest single cut, but 4b is NOT a one-bar rule
At PROTOCOL's 10 bps: 90 arms, **7 pass 4b**, 83 fail.

| bar | unique-cut (of 83 failing) | own fail rate | drop-1 recovery | rung flips (4 steps, n=90 each) |
|---|---|---|---|---|
| L1 H1 Sharpe > SPY | 2 (2.4%) | 46.7% | +2 | 42 |
| L2 H2 Sharpe > SPY | 1 (1.2%) | 53.3% | +1 | 40 |
| L3 OOS Sharpe > SPY | **0 (0.0%)** | 51.1% | **+0** | 45 |
| L4 MaxDD ≤ 0.60·SPY | 9 (10.8%) | 47.8% | +9 | **17** |
| L5 CAGR ≥ 0.70·SPY | **20 (24.1%)** | 58.9% | **+20** | 40 |

- The floor is the **single most-binding bar by a factor of 2.2** over the next (L4), and dropping
  it alone takes the pass count from 7/90 to 27/90.
- But **only 32 of 83 failing arms (38.6%) fail on exactly one bar**; the mean failing arm fails
  **2.80** of the five. The modal fail set is not `{L5}` (20 arms) but the **total wipeout**
  `L1+L2+L3+L4+L5` (17 arms). So idea 523's "the floor is the sole failing bar" generalises as a
  *plurality*, not a majority: **4b is a two-bar rule (L5 + L4 = 34.9% of failing arms alone), not
  a one-bar rule.** The strong form of the premise is KILLED.
- L5 is the unique cut at **every** rung (25.0% / 24.1% / 16.3% / 16.1% / 10.0% at 0/10/25/50/100),
  so the finding is not a cost artefact.

## Result 2 — NEW: 4b's OOS leg is redundant with its own H2 leg (the load-bearing finding)
`FIVE` and `NO_OOS` have **identical pass counts at all five rungs** (14/14, 7/7, 4/4, 3/3, 0/0).
L3 is the unique cut **0 times at every rung**, and drop-L3 recovery is **+0**.

The mechanism is arithmetic, not luck: PROTOCOL 8's OOS window (2017-01-03 →) and 4b's own H2
window (2017-11-07 →) are nearly the same period. On U56, **100.0% of H2's 2,221 rows lie inside
OOS**, and H2 covers **91.2%** of OOS; B136 is 100.0% / 91.3%. L2 and L3 agree on **95.1%** of all
450 arm-rows. Folding rule 8 into 4b on 2026-09-04 added a bar that re-tests what L2 already tests,
minus 214 trading days. **"Sharpe > SPY in both halves AND out-of-sample" is, on this corpus,
"Sharpe > SPY in both halves."** This bears directly on 530/531 and is the cheapest available
tightening of 4b: either move the rule-8 split away from the half-sample midpoint, or drop L3 and
say so, but do not keep quoting it as a third independent Sharpe test.

## Result 3 — the DD cap is the one bar cost cannot reach
Rung flips over the four cost steps: L3 45, L1 42, L2 40, L5 40, **L4 17** — and 0 of those 17 occur
below 25 bps (0→10 and 10→25 both move L4 exactly 0 arms). Drawdown is a path statistic and
10 bps of turnover does not reshape a path; Sharpe and CAGR are level statistics and cost walks
straight through them. A "4b pass at 10 bps" therefore carries a **cost-fragile** Sharpe/CAGR
component and a **cost-proof** DD component, and those should not be quoted with the same confidence.

## Result 4 — PROTOCOL 8 walk-forward (chosen on 2008–2016 ONLY, evaluated on 2017–2026 untouched)
Both pre-registered choosers (IS-Sharpe argmax; IS-4b-filter then IS-Sharpe) pick the same arm.

| panel | pick | OOS CAGR | OOS Sharpe | OOS MaxDD | OOS 4b | OOS 4a |
|---|---|---|---|---|---|---|
| U56 | BAND08 @ g1.00 | **12.00%** | **1.162** | −19.05% | **PASS** | FAIL |
| U56 — RULES v2 baseline | | 9.45% | 1.275 | −12.05% | | |
| U56 — SPY | | 15.24% | 0.872 | −33.72% | | |
| B136 | BAND08 @ g1.00 | **11.17%** | **1.108** | −19.50% | **PASS** | FAIL |
| B136 — RULES v2 baseline | | 7.98% | 1.119 | −12.24% | | |
| B136 — SPY | | 15.45% | 0.882 | −33.72% | | |
| SMALL439 | CAND20_VS @ g1.00 | 4.47% | 0.333 | −43.73% | FAIL (all 5) | FAIL |
| SMALL439 — RULES v2 baseline | | 3.85% | 0.568 | −14.68% | | |

The large-cap OOS 4b passes are real but **bought entirely with exposure**: the same book at the
live gross 0.75 fails, and fails on the CAGR floor alone, at every rung on both panels. Its DD-cap
margin is 1.2 pp (−19.05% vs the −20.23% cap) and its CAGR-floor margin 0.8 pp. This is a
restatement of idea 668's gross footprint, not a new book, and **nothing is promoted on it.**
The zero-signal control SPYBH fails L1+L2+L3 at every gross on every panel, as it must.

## Survivorship (PROTOCOL 9) — stated, not waved at
All three panels are **current constituents**. U56 and B136 are today's membership; SMALL439 is a
screen run today over sub-$2B names and contains no company that delisted, was acquired, or went to
zero before today. Every **level** above is biased upward, the small panel worst. The claims this
run makes are about **which bar cuts inside a panel** — a within-panel ordering that survivorship
biases far less than it biases a level — but no level here is a tradeable estimate.

## What this changes
1. Stop describing 4b as a five-way test. It is a two-bar test (CAGR floor, then DD cap) with a
   redundant third Sharpe leg and two Sharpe legs that cost moves freely.
2. Ideas 530/531 should be read against **+0 drop-recovery for L3** and **34.9% joint L5+L4 sole
   cutting**, not against a one-bar story.
3. The cheapest honest fix is to stop quoting L3 as independent evidence, or to re-cut rule 8's
   split so OOS is not 91% of H2.
