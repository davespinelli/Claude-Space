# Idea 852 (lane B, 2026-09-14) — does an EQUITY-DRAWDOWN THROTTLE on the band book spend the unused 4b drawdown budget?

**VERDICT: KILL.** The budget is not spendable this way. Across 48 arms (2 panels x 6 triggers
x 4 throttled-gross levels, ALL reported), **every arm that actually fires is strictly worse
than its own un-throttled parent on both CAGR and Sharpe**, and **every 4b pass on the grid
belongs to an arm where the throttle never fires** — i.e. the passes are the parent wearing a
dial. No RULES change, no book promoted, no KEEP claimed, no memo; RULES.md, PROTOCOL.md,
scan.py, bot.py and baseline.py untouched (rule 6).

Script: `2026-09-14_equity-drawdown-throttle-on-the-band-book_B.py` ·
tables: `.grid.csv` (56 rows), `.walkforward.csv` (70 rows) · console: `.console.txt`

## What was tested and why

Grounded in the CHANGELOG diagnosis: ideas 786/787/795 put the binding 4b leg on the **CAGR
floor** while the live band book's MaxDD (-12.05%) sits far inside the 4b cap (60% of SPY's
-33.72% = -20.23%) — roughly 8 pp of drawdown budget never spent. Idea 794 killed the realised-
**vol** scaler as the way to spend it. Idea 403 noted that **no instrument in this record reads
its own equity**, so the drawdown-state sibling had never been priced. This run prices it.

**Book.** Base = RULES v2's frozen band clause (`band_state`, band=0.03 — frozen, not a dial) at
gross 1.00, equal weight inside the band, gated-out weight to cash. **Throttle:** at each weekly
rebalance the book reads its own realised equity through the decision date, computes
`dd = eq/cummax(eq) - 1`, and targets gross `g_low` while `dd <= -d`, gross 1.00 otherwise.
**Two tuned parameters only:** `d` in {0.04, 0.06, 0.08, 0.10, 0.12, 0.15} and `g_low` in
{0.00, 0.25, 0.50, 0.75} — 24 points per panel, all published. 10 bps, weekly, t+1, no leverage.
Panels U56 (live) and B136 (broad). **Survivorship:** both universe files are current
constituents, which flatters every long book here, the parent included.

## Gates (printed before any new number)

| gate | result |
|---|---|
| G1 throttle OFF == `engine.backtest` on the identical static book, 4,701 finite rows (the engine's 2 NaN warm-up rows excluded, both before the 260-day skip) | max\|dr\| **0.000e+00**, max\|dturnover\| **0.000e+00** — PASS |
| G2 `d=0.99` (trigger unreachable) == parent | **0.000e+00** — PASS |
| G3 `g_low=1.00` == parent at all 6 triggers | **0.000e+00** — PASS |
| G4 cost-rung identity `r(c) = r(0) - turnover*c/1e4` on a live throttled arm | **2.396e-02** — REPORTED, not a pass. This is the honest consequence of a path-dependent book: costs move equity, equity moves the trigger, so the record's cost-rung identity (0.000e+00 on every static book it has published) **does not hold here**. Every cost rung in this run was therefore run live, never interpolated. |

## The decisive reading — no firing arm beats its own parent

| panel | leg | parent (no throttle) | inert arms | best firing arm | firing arms beating parent, Sharpe / CAGR |
|---|---|---|---|---|---|
| U56 | FULL | Sharpe 1.2017, CAGR 11.54%, MaxDD -15.91% | 4/24 bit-identical | Sharpe 1.1991, CAGR 11.50% | **0/20 / 0/20** |
| U56 | OOS 2017-2026 | Sharpe 1.2775, CAGR 12.70% | 4/24 | — | **0/20 / 0/20** |
| B136 | FULL | Sharpe 1.0992, CAGR 10.65%, MaxDD -16.16% | 4/24 bit-identical | Sharpe 1.0946, CAGR 10.58% | **0/20 / 0/20** |
| B136 | OOS 2017-2026 | Sharpe 1.1048, CAGR 10.52% | 4/24 | — | 2/20 / **0/20** (both still fail 4b on the CAGR floor) |

4b tally over the 24 throttled arms per panel — **full sample:** U56 11, B136 4; **OOS:** U56 14,
B136 0. Every one of those passes is an arm at `d=0.15` (never fires on either panel) or, on U56,
`d=0.12` with `g_low >= 0.25` whose only firing episode is March 2020. 4a passes: **0 of 48**, on
every leg. Of the 48 throttled arms, **33 fail 4b and every one of the 33 fails on the CAGR floor**
(U56 13 of 24, B136 20 of 24; the remaining 15 are the passes above), exactly as
786/787/795 predicted — the throttle moves the book **down** that leg, never up.

## The `g_low = 0.00` absorbing trap

De-grossing to full cash on a **self-referential** trigger is an absorbing state: at zero gross
the equity curve is flat, so the drawdown never recovers and the rule never re-arms. Measured, not
asserted — first trap date and cash-held span, both panels:

| d | U56 | B136 |
|---|---|---|
| 0.04 | 2009-07-13, **17.2 yrs in 100% cash** | 2009-07-13, 17.2 yrs |
| 0.06 | 2010-02-08, 16.6 yrs | 2010-02-08, 16.6 yrs |
| 0.08 | 2010-07-06, 16.2 yrs | 2010-05-24, 16.3 yrs |
| 0.10 | 2011-11-28, 14.8 yrs | 2010-07-06, 16.2 yrs |
| 0.12 | 2020-03-16, 6.5 yrs | 2020-03-16, 6.5 yrs |
| 0.15 | never fires | never fires |

This is a property of the rule as specified, not a bug in the runner: G2/G3 show the wiring is
inert when the trigger is unreached, and the trap arms trade normally until the trigger day.

## Rule 8 walk-forward — and a tie that decides it

Parameters chosen on **2009-2016 IS Sharpe only**, read once on 2017-2026. **The IS-best Sharpe is
an 8-way tie on both panels** (U56 1.1047, B136 1.0927) because the throttle **never fires in
sample** at `d >= 0.12`. The record's own tie convention (first in grid order) therefore hands the
pick to `g_low = 0.00` — the absorbing arm — on the strength of a number that contains no
information about the throttle at all. What that pick does out of sample:

| panel | arm | OOS CAGR | OOS Sharpe | OOS MaxDD | 4b |
|---|---|---|---|---|---|
| U56 | **rule-8 pick** d=0.12 g_low=0.00 | **2.37%** | **0.4463** | -15.91% | FAIL (H1+H2+CAGRFLOOR) |
| U56 | IS-tied d=0.12 g_low=0.75 | 12.61% | 1.2732 | -15.91% | PASS |
| U56 | IS-tied d=0.15 (all g_low) | 12.70% | 1.2775 | -15.91% | PASS (= parent exactly) |
| U56 | BAND g=1.00 parent | 12.70% | 1.2775 | -15.91% | PASS |
| U56 | RULES v2 (live) | 9.47% | 1.2782 | -12.05% | FAIL (CAGRFLOOR) |
| U56 | SPY | 15.33% | 0.8767 | -33.72% | — |
| B136 | **rule-8 pick** d=0.12 g_low=0.00 | **2.50%** | **0.4480** | -16.16% | FAIL (H1+H2+CAGRFLOOR) |
| B136 | IS-tied d=0.15 (all g_low) | 10.52% | 1.1048 | -16.16% | FAIL (CAGRFLOOR) |
| B136 | BAND g=1.00 parent | 10.52% | 1.1048 | -16.16% | FAIL (CAGRFLOOR) |
| B136 | RULES v2 (live) | 7.88% | 1.1059 | -12.24% | FAIL (CAGRFLOOR) |

This is idea 846's tie-convention finding reproduced **on a live book** rather than on a census of
committed columns: an 8-way IS tie, broken by grid order, costs 10.3 pp of OOS CAGR on U56 and
8.0 pp on B136. The pre-registered pick is reported as the pick; all 8 tied arms are published
beside it so the convention's cost is visible rather than hidden.

## Two by-products, neither claimed as a KEEP

1. **The standing 4b candidate reproduces on U56 and FAILS on B136 out of sample.** The
   un-throttled BAND book at gross 1.00 (ideas 733/795) passes 4b on U56 full (CAGR 11.54%,
   Sharpe 1.2017 vs SPY 0.8861, MaxDD -15.91% vs a -20.23% cap) and OOS (12.70% / 1.2775). On
   B136 OOS it misses the CAGR floor by **0.21 pp** (10.52% against 70% of SPY's 15.33% = 10.73%).
   The shelf's surviving candidate is a **panel-conditional** pass, which the memo for it does not
   currently say.
2. **The cost-rung identity is not available to equity-reading books** (G4, 2.396e-02). Any future
   instrument that reads its own equity must run every cost rung live; the record's interpolation
   shortcut is valid only for the static books it was measured on.

## Caveats

Current-constituent survivorship in both universe files. 2009-2026 is one regime, and 2020 and
2022 are the only real stress episodes — idea 835 has already shown that 89% of this record's 4b
passes are 2020-dependent, which applies to the parent's passes here too. The throttle was frozen
at base gross 1.00 and band 0.03; a different base could in principle interact with it, but the
mechanism that kills it (de-grossing after a drawdown sells the recovery) is base-independent.
