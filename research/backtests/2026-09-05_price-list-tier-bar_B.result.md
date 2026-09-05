# Idea 97 — price-list-tier-bar (lane B, 2026-09-05)

**Verdict: KILL of the tier statement as worded. One clause of the four survives every
panel and every window and is proposed to PROTOCOL; the other two are large-cap-only and
crisis-window-only, and idea 94's "stops are not insurance" phrasing is refuted outright on
the small-cap panel.**

Script `research/backtests/2026-09-05_price-list-tier-bar_B.py`, console `…_B.console.txt`,
data `…_B.grid.csv` (816 arm-points), `…_B.pricelist.csv` (765 priced arm-cells),
`…_B.tiers.csv` (54 tier rows), `…_B.walkforward.csv` (18 cells).

## What was run

Idea 94's simulator was **imported, not re-implemented** — this script executes that module's
`targets`/`run`/`price`/`ladder_slope`/`arm_specs` so every number here comes from the
identical harness. Verification before anything else runs: engine-equivalence of the control
vs `engine.backtest` is `max|diff| = 0.000e+00`, and two published rows reproduce exactly
(`EWall+vol60-dg` u56 @10bps 11.6% / 1.133 / −16.9%; `EWall+band3-rw` 12.2% / 1.161 / −17.7%).
The walk-forward also reproduces idea 94's 12 u56/broad picks arm-for-arm.

New: a **third panel** and a **tier layer**.

- Panels: `u56` (universe.json, 56), `broad` (universe_broad.json, 136), **`small`**
  (data/prices_small.csv.gz, 439 names after holding SPY out as benchmark and dropping the 44
  names with `max_1d_move ≥ 1.0` — the convention of every other small-panel run here).
  The small panel is trading-day indexed and starts 2010-01-04, so its IS window is 2010–2016.
- Books (idea 94's, ungated, 75% gross): `V1u`, `TOP20`, `EWall`. Costs 10 and 25 bps.
  3 × 3 × 2 = **18 cells**, 17 arms + a 19-point static-gross ladder each.
- Tiers (fixed before any number was read): **T1** per-name gate (g200/band3/abs12/vol60/v1gate
  × dg/rw), **T2** the static gross lever (the ladder slope — the reference), **T3** book-level
  DD control, **T4** per-name trailing stop. `ebud` is reported but excluded from the statement.
  Tier price = median of the finite arm rates in the tier; a tier with no priceable arm ranks
  last by pre-registration.
- Tuned parameters: **one** (instrument family / tier, in the walk-forward selector).

The candidate sentence, split into three falsifiable inequalities:

    C1  per-name gate      <  static gross lever
    C2  static gross lever <  book-level DD rule
    C3  book-level DD rule <  per-name trailing stop

## Result: the sentence does not hold as a sentence

Cells in which each clause is true (6 per panel per window; 18 per window):

| window | C1 u56 / broad / small | C2 u56 / broad / small | C3 u56 / broad / small | exact 4-tier order |
|---|---|---|---|---|
| full | **6/6 · 6/6 · 2/6** | 5/6 · 6/6 · 2/6 | 6/6 · 6/6 · 6/6 | 11/18 |
| IS (2009/10–2016) | **0/6 · 3/6 · 2/6** | 6/6 · 6/6 · 4/6 | 5/6 · 4/6 · 6/6 | 2/18 |
| OOS (2017–2026) | 6/6 · 6/6 · 2/6 | 3/6 · 3/6 · 3/6 | 6/6 · 6/6 · 5/6 | 7/18 |
| **all 54 rows** | **33/54** | 38/54 | **50/54** | 20/54 |

Two independent failures, both fatal to the sentence as idea 94 wrote it:

**1. Panel. The ordering does not merely weaken on small caps — it reverses.** Median
full-sample tier prices:

| panel | T1 gate | T2 lever | T3 DD rule | T4 stop | median order |
|---|---|---|---|---|---|
| u56 | **0.468** | 0.592 | 0.659 | unpriceable | T1 < T2 < T3 < T4 ✓ |
| broad | **0.294** | 0.519 | 0.579 | unpriceable | T1 < T2 < T3 < T4 ✓ |
| small | 0.350 | 0.279 | **0.219** | 0.746 | **T3 < T2 < T1 < T4** |

On the small panel the book-level drawdown control — the instrument idea 22 and idea 94 both
priced as dear — is the **cheapest** real instrument (0.164–0.565 across the six cells, buying
10.7–13.0 pp of MaxDD at 1.4–21x/yr turnover), and the per-name gate tier is the dearest of
the three. The mechanism is not the one ideas 38/49/51 predicted: the 200d gate does not price
negatively on `EWall/small` — it buys a large 21.9 pp of drawdown for 6.6 pp of CAGR
(rate 0.302) — but the ungated small-cap book drawdowns so deeply (control −30.8%) that the
crude book-level rule finds far more drawdown to cut per pp of CAGR than a per-name signal
does. Where the queue's inversion *does* appear literally is `V1u/small`, where every gate
prices **negative** (−0.34 to −1.41: the gate adds CAGR *and* cuts drawdown, +0.02 to +0.10
Sharpe), which is a different result again — free insurance, not dear insurance.

**2. Window. C1 is true only in a window that contains crises.** On u56 the gate tier prices
at **4.108 in-sample against a 1.002 lever** and C1 is true in **0 of 6** IS cells, then at
0.404 against 0.616 out-of-sample with C1 true in 6/6. SPY's MaxDD is −22.1% in the IS window
and −33.7% in the OOS window; the deepest IS year is 2009 (−22.1%) against OOS's 2020 (−33.7%),
2022 (−24.5%), 2018/2023 (−19.3%). An instrument that pays in crashes looks dear in a window
without one — the same crisis-density signature ideas 99/111 measured on overlays, now
reproduced on the drawdown-price axis. **A price quoted without its window's drawdown depth is
not interpretable**, which is the specific reason PROTOCOL must not quote the number.

**3. "Stops are not insurance" is refuted on the small panel.** Idea 94's phrasing came from
u56/broad, where the stop buys **negative** drawdown (median ΔMaxDD −0.69 pp / −1.03 pp at
10 bps, priced 0/6 in both). On the small panel it buys **positive** drawdown in 9 of 12 cells
(median **+1.07 pp**, 1.8–4.0 pp on `TOP20`/`EWall`). The stop *is* insurance on small caps —
it is simply the **dearest** tier there (0.351–2.652, T4 last in 6/6 full-sample cells).
C3 is the one clause that is true on all three panels: **50 of 54 rows**.

## Are tiers more stable than instruments? Split answer (P1 half-confirmed)

| axis | instrument-level Spearman | tier-level Spearman |
|---|---|---|
| IS → OOS, median over 18 cells | **+0.418** | +0.400 |
| IS → OOS, mean | +0.249 | +0.334 |
| cross-panel (full sample, matched book × cost), median over 18 pairs | +0.386 | **+0.800** |

Tiers are **not** more stable through time — the median is a dead heat, and idea 94's published
+0.442 instrument figure reproduces at +0.418 on the enlarged cell set. Tiers *are* markedly
more portable **across panels** (+0.800 vs +0.386), and the instrument ordering is
catastrophically unstable on the pair that matters: `u56 vs small, EWall` gives instrument
Spearman **−0.717 / −0.833** against tier +0.200. So the tier is the right object to compare
*panels* with and buys nothing against *time*.

## Rule 8 walk-forward — the tier selector is WORSE (P4 refuted)

Family chosen on IS only, evaluated untouched on 2017–2026. `S1` = argmin IS instrument rate
(idea 94's selector). `Stier` = argmin IS tier price over {T1,T3,T4}, then the **median**-IS-rate
arm inside that tier. Regret = OOS rate of the pick − OOS rate of the cell's OOS-cheapest arm.

| panel | S1 mean regret | Stier mean regret | S1 rank-1 | Stier rank-1 | ΔOOS Sharpe (Stier−S1) |
|---|---|---|---|---|---|
| u56 | +0.579 | +0.709 | 2/6 | 0/6 | +0.039 |
| broad | +0.250 | +0.263 | 3/6 | 2/6 | −0.025 |
| small | +0.169 | +0.418 | 3/6 | 2/6 | +0.006 |
| **all 18** | **+0.337** | +0.489 | **8/18** | 4/18 | +0.007 |

Choosing the cheapest *tier* and then a deliberately non-extremal member of it is worse on OOS
price in every panel and halves the rank-1 hit rate, while OOS **Sharpe** is a wash (+0.007).
The tier abstraction does not buy a better selector; it buys portability and nothing else.

**The flag that matters more than either selector:** in **12 of 18 cells the cheapest rule tier
is dearer in-sample than the static gross lever** — i.e. an investor sizing a drawdown budget
on IS evidence alone should have used no rule at all. The 6 exceptions are `broad/EWall` (both
costs), `broad/V1u` (both) and `small/V1u` (both).

## PROTOCOL rule 4 — both KEEP paths, every arm, all three panels

4b passes at 10 bps: **u56 14**, **broad 4**, **small 0**; at 25 bps: 9 / 2 / 0.
Passing 4b on **both large panels at 10 bps**: `EWall+g200-rw`, `EWall+band3-rw`,
`EWall+v1gate-rw`, `EWall+vol60-dg` — the last two of which are idea 94's published pair, here
independently reproduced, plus `g200-rw` and `v1gate-rw` which idea 94 did not flag at 10 bps.
**No arm passes 4b on all three panels**, and no arm passes it on the small panel at all: every
small-panel arm fails on H1, H2, OOS *and* the drawdown cap simultaneously — the ungated small
book itself runs 14.7% CAGR / 0.767 Sharpe / −30.8% MaxDD against SPY's 14.1% / 0.862 / −33.7%
on that window. 4a passes at 10 bps: u56 3 arms, broad 11, small 12 (including the *control*),
which is idea 22/40/94's known 4a pathology — cutting exposure clears 4a only because live
RULES v1 is weak, and on the small panel v1 is weakest of all (0.603 Sharpe, −32.8% MaxDD).
**P5 confirmed: this run produces no new KEEP.**

## Prediction scorecard

- **P1 half-confirmed.** Tier > instrument cross-panel (+0.800 vs +0.386); a dead heat
  IS→OOS (+0.400 vs +0.418).
- **P2 confirmed on C1, confirmed on C3.** C1 inverts on small (2/6 vs 6/6 and 6/6);
  C3 holds on all three panels (6/6 each full-sample). Not predicted: **C2 also inverts on
  small** (2/6), and the driver is the DD control becoming cheap, not the gate becoming dear.
- **P3 REFUTED.** The stop buys ≤ 0 drawdown in only 3 of 12 small-panel cells (median
  +1.07 pp). "Not insurance" is a large-cap statement; "dearest tier" is the invariant one.
- **P4 REFUTED.** Stier mean OOS regret +0.489 vs S1's +0.337.
- **P5 confirmed.** No arm passes 4b on all three panels.

## What PROTOCOL should quote (the deliverable)

Only C3, and only with its two qualifiers. Exact wording is in
`2026-09-05_price-list-tier-bar_B.memo.md`. The clauses that must **not** be quoted are C1 and
C2 — not because they are false on this project's primary universes (they are true 6/6 and 5–6/6
there) but because they are false on a third panel of the same asset class and false in-sample
on the panel they were derived from, which is exactly the pattern PROTOCOL rule 7 exists to
catch.

## Caveats, stated plainly

- **SURVIVORSHIP.** All three panels are current-constituent lists; the small panel's bias is
  the worst and falls hardest on beaten-down names (idea 54) — precisely the cohort a gate
  excludes — so the small-panel gate price here is **flattered**, and the C1 inversion is if
  anything understated.
- The small panel's evaluation window starts 2011-01-13 (260-day warm-up from 2010) against
  2009-01-13 for the other two, so its IS window is 2010–2016 and it misses the 2009 rebound.
  Cross-panel comparisons of *levels* inherit that; the within-cell deltas that are the result
  do not.
- Calendar-day index (open idea 38) is unfixed for u56/broad and affects every arm on those two
  panels equally; the small panel is trading-day indexed.
- The 3% band, the 0.60 vol threshold, the 8%/0.5 DD control and the 15/25% stop depths are all
  inherited from earlier runs on overlapping data. This run tunes only the family, so the IS/OOS
  split is a validity check on the **ordering**, not a clean OOS test of those constants — the
  same caveat idea 94 carried.
- 18 cells is not many. C3's 50/54 is the only count with real margin; C1's 33/54 and C2's
  38/54 are close enough to coin-flips that no wording should rest on them.

## Recommended follow-ups (queued)

117. `crisis-depth-as-the-price-denominator` — every drawdown price in this project is quoted
     without stating the window's own MaxDD, and C1 flips sign between a −22.1% window and a
     −33.7% one. Test pricing per pp of MaxDD **at matched crisis depth** (episode-level, using
     idea 62's >10% drawdown episode classification) instead of whole-window MaxDD.
118. `why-the-DD-control-is-cheap-on-small-caps` — T3 prices at 0.16–0.57 on the 439-name panel
     against 0.58–0.86 on u56/broad, reversing idea 22's headline. Is it the deeper control
     drawdown (−30.8% vs −17%), the higher single-name vol, or idea 93's absorbing-state
     behaviour firing more often? Bears on ideas 22, 74, 93.
119. `V1u-small-negative-price` — on `V1u/small` every gate prices negative (−0.34 to −1.41):
     more CAGR *and* less drawdown, +0.02..+0.10 Sharpe, in 6/6 arms. A free lunch this large
     on a 439-name panel is more likely a panel artefact (survivorship, the 32x/yr turnover, the
     top-5 concentration) than an edge — audit it before anyone cites it.
