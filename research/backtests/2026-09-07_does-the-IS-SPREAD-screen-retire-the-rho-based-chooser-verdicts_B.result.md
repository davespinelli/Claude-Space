# Idea 373 — does-the-IS-SPREAD-screen-retire-the-record's-rho-based-chooser-verdicts (lane B, 2026-09-07)

**Verdict: KILL of the screen as a retirement rule; the queue's two counts are ANSWERED.**
*(Independent lane-B run; lane C answered the same idea concurrently and reached the same verdict on
a different corpus — see the collision note below. Filed as 373b, a replication, not a duplicate.)*
The IS-spread screen flags a real population, but it flags the verdicts whose Sharpe stakes are
already ~nil and **misses every verdict that actually flips** in the arm where the pools are exact.
What the screen mostly detects is a *dial* property known a priori (the gross numeraire, idea 351),
not a per-verdict warning.

## The queue's two questions, answered

| question | archaeology (all) | archaeology (validated) | live exact-pool corpus |
|---|---|---|---|
| chooser cells priced | 12,724 (169 files) | 651 | 72 |
| **rest on IS spread < 0.01** | **1,502 (11.8%)** | **66 (10.1%)** | **6 (8.3%)** |
| **of those, FLIP when judged by OOS MaxDD** | **601 (40.0%)** | **32 (48.5%)** | **0 (0.0%)** |
| flip rate of cells with spread ≥ 0.01 | 31.1% | 32.6% | 13.6% (9/66) |
| Δflip (below − above) | **+8.9 pp** | **+15.8 pp** | **−13.6 pp** |

Per-file (not per-cell) the low-spread population is thin: **median 1.1% of a file's cells**
(IQR 0.0–17.4%), median per-file flip rate 33.3%. The pooled 11.8% is carried by a handful of
flat-surface grids.

## Why the screen cannot retire anything

1. **No consistent sign.** Δflip is +8.9 pp pooled, +15.8 pp validated, and **−13.6 pp** on the arm
   whose pools are exact by construction. A screen whose discriminating statistic changes sign
   between arms retires nothing.
2. **It misses the flips.** In the live corpus all **9/9 flips sit at IS spread 0.056–0.593**, every
   one above the proposed threshold, while all **6 cells below it (the G1 gross dial, spread
   0.001–0.005) agree in both judgements**.
3. **What it flags is immaterial on the Sharpe axis.** Mean OOS-Sharpe regret below τ = 0.01 is
   **−0.003** (validated) / **−0.002** (live) against **−0.048 / −0.022** above it — a 10–15×
   difference, reproduced in both arms. When five points are indistinguishable in-sample they are
   near-indistinguishable out-of-sample too: there is no verdict left to retire.
4. **It is a dial property, not a verdict property.** The low-spread population is concentrated on
   gross-type axes: of cells whose dial axis is `g` **81.5%** fall below τ, `gross_mode` **85.7%**,
   `selector` **100%**, against 9.7% for `n` and 8.9% for `arm`. Idea 351 already established that
   the gross dial costs 0.000 Sharpe by construction; a near-zero IS spread there is mechanical and
   knowable before any backtest.

## What does survive — and it is not the spread

The **judgement axis**, not the spread, is where the record loses information:

| statistic | archaeology (all) | validated | live |
|---|---|---|---|
| FLIP rate, unconditional | **32.2%** | **34.3%** | 12.5% |
| ρ(rank by OOS Sharpe, rank by OOS MaxDD) | +0.322 | **+0.098** | +0.476 |
| pick sits in the better half by Sharpe (GOOD_S) | 77.1% | 79.3% | 80.6% |
| … but in the better half by drawdown (GOOD_D) | 64.5% | 68.0% | 68.1% |
| "Sharpe says fine, drawdown says harmed" | 22.0% | 22.7% | 12.5% |
| mean OOS-drawdown regret of the pick | **+3.31 pp** | **+3.65 pp** | **+2.45 pp** |

About one chooser verdict in three reverses when the same pick is judged by OOS MaxDD, at **every**
spread level. Idea 371's 4.8× drawdown was not a low-spread pathology; it is the record-wide
condition of a Sharpe-only rule 8.

ρ(IS spread, ·) across cells: rank_S **+0.235 / +0.319 / +0.676**, **|regret_S| +0.082 / +0.075 /
−0.445**, regret_DD +0.118 / **+0.490** / **−0.550**, FLIP −0.127 / −0.176 / +0.155 (all / validated /
live). Note the two Sharpe-axis statistics point opposite ways and both are fatal for the screen: a
wider spread makes the pick *rank* better (+0.235) yet carries a *larger* absolute regret (+0.082) —
the sign the screen needs is negative. Cells inside one file are not independent, so no p-value is
quoted on the 12,724; the per-file medians and the 72 exact cells are the load-bearing numbers.

Relation to idea 114: it tested the *margin* (best − runner-up) against OOS regret and found
ρ +0.119, p 0.705 (FAIL). The *spread* (max − min) reproduces that wrong sign at ρ **+0.082** on a
289× larger cell corpus.

## Collision note — lane C answered the same idea concurrently

Lane C's `..._cloud.py` landed on origin/main while this run was executing; neither saw the other.
The two runs use different corpora (lane C: 6,307 stratified menus from 225 live grids; here: 12,724
one-dial slices reconstructed from 169 committed CSVs, plus 72 exact live cells) and **agree on the
verdict and on every mechanism**: the screen is killed, the flip is universal rather than a
small-spread effect, the low-spread population is *exposure* dials (lane C's phrasing) = gross-type
axes (measured here on axis names: `selector` 100%, `gross_mode` 85.7%, `g` 81.5%), and the right
disposition is a **reporting** requirement, not a selection rule. The independent reproductions worth
recording: ρ(spread, |OOS regret|) **+0.082 here vs +0.155 there vs +0.119 (idea 114)** — three
corpora, one wrong sign; and unconditional verdict-flip **32.2% here vs 31.1% there**. The one number
that differs is the *count*: 11.8% of one-dial slices here (per-file median 1.1%) against 35.3% of
stratified menus there. That is a pooling convention, not a disagreement — the share below τ depends
entirely on how a "menu" is cut, which is itself an argument against writing τ into PROTOCOL.

## What was run

- **[A] Leaderboard census (exact).** 2,876 rows; **439 (15.3%)** claim a rule-8 / chooser / regret
  result; **8 (1.8% of those)** quote an IS spread or margin, six of them idea 114's own rows. The
  record's chooser verdicts are published without the statistic the queue proposes to screen by.
- **[B] Record archaeology.** All 1,078 committed CSVs; 169 carry IS Sharpe + OOS Sharpe + OOS MaxDD
  per point. Chooser cells reconstructed as "same context, one varying dial, ≥ n_min points";
  651 cells **validated** by matching the reconstructed pick's IS Sharpe to a pick published in the
  file's own `*.walkforward.csv`.
- **[C] Live control corpus.** Idea 371's nine dials + three it did not run (cadence W3, vol target
  V1, breadth gate B1) × 2 panels × 3 cost rungs = **72 exact chooser cells, 354 grid points**.
  **GATE: reproduces idea 371's committed `ordering.csv` on 54/54 cells, max |ΔIS_spread| 9.7e-17,
  max |Δρ| 1.1e-16.**
- Both reported parameters (τ ∈ {0.0025, 0.005, 0.01, 0.02, 0.05, 0.10}, n_min ∈ {3,4,5}) are swept;
  every one of the 54 grid points is in `.screengrid.csv` and the console. Nothing was tuned.

## Rule-8 walk-forward and both KEEP paths (live corpus, all 354 points reported)

At the PROTOCOL rung (10 bps, 24 cells): median chooser pick **OOS CAGR 10.15%, Sharpe 1.118,
MaxDD −14.90%** vs RULES v2 OOS **8.76% / 1.202 / −12.15%** and SPY OOS **15.45% / 0.882 / −33.72%**.
Picks beat SPY on OOS Sharpe **23/24** (69/72 across rungs) and beat the live book **3/24** (10/72).

**4a 27/354** (B1 8, C5 7, W2 6, W3 6 — all de-grossing or cadence variants of the live book).
**4b 18/354**: V1 11, G1 5, W1 2. **None is filed as a KEEP-candidate, and no memo is written:**

- the 11 **V1** passes are **leverage-touched and therefore not protocol-clean** — the 1.5× cap binds
  on 90.2% of days at t=0.15 (74.3% at t=0.12), realised gross mean 0.786, **max 1.106, above 1.0 on
  10.0% of days**. PROTOCOL 2 forbids leverage unless the idea says so; this dial exists to study
  choosers, not to propose a book. It is **not** idea 374's candidate, which caps at `k_t ≤ 1` on the
  un-gated EWALL parent and never levers.
- the 5 **G1** passes are `gross = 1.00`, the grid edge of the numeraire dial (ideas 311/351), and the
  2 **W1** passes are wide-n RULES v1 at **0 bps only**.

## Caveats

Arm [B] reconstructs pools by a column-role heuristic: an admitted slice is a pool rule 8 *could*
have chosen over, which is why the validated subset is reported separately and every headline is
given on both. Both panels are current-constituent (survivorship bites hardest in the OOS window);
the within-pool *ranks* used throughout are far less exposed than levels. Files dated before
2026-09-07 inherit the pre-idea-38 calendar-day tape — a level effect shared by every point inside a
pool, so it cancels in within-pool ranks (idea 39: the error was conservative, never generous).
Five points per dial gives ρ ≈ 1.5 effective degrees of freedom; nothing rests on one cell's ρ.

## What the record should do instead (for Sunday, not adopted here)

Do not screen by IS spread. **Report OOS MaxDD beside every rule-8 chooser verdict** — the pick's
drawdown rank costs nothing to compute, disagrees with the Sharpe rank in ~1/3 of the record's
chooser cells at every spread level, and is the axis on which idea 371's damage was invisible.
