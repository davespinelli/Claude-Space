# Idea 101 — fixed-gross-S4-blend (cloud, 2026-09-05), with idea 104 folded in as its second arm

**Verdict: KEEP on both PROTOCOL paths (4a + 4b) for the S3 arm; 4b-only for the S4 arm.**
One pre-registered robustness bar (idea 65's cadence-insensitivity) is FAILED, and the failure is
traced to the equity book rather than to the sleeve.

## What was fixed ex ante, before any number was computed

`g = 1.00` (fully invested, no leverage), book = idea 2's `top20`, `f* = 0.50`, two sleeve arms
(S4 = TLT,GLD,DBC,UUP from idea 100; S3 = TLT,GLD,UUP from idea 104), sleeve construction =
idea 18 variant B verbatim. Tuned parameters: **f** (5 points) and **cost** (5 rungs) — two, per
PROTOCOL rule 4. Universe, cadence and gross convention are reported controls and were never
selected on. 600 grid points, all written to `.grid.csv`, all printed in `.console.txt`.

## Headline, 10 bps, weekly, g = 1.00

| | CAGR | Sharpe | MaxDD | H1 / H2 | OOS CAGR / Sharpe / MaxDD | 4a | 4b |
|---|---|---|---|---|---|---|---|
| **S3, u56** | 11.5% | 1.167 | −13.3% | 1.169 / 1.167 | 12.3% / 1.215 / −13.3% | ✅ | ✅ |
| **S3, broad** | 12.0% | 1.073 | −14.6% | 1.245 / 0.917 | 11.1% / 0.985 / −14.6% | ✅ | ✅ |
| S4, u56 | 11.8% | 1.149 | −14.2% | 1.099 / 1.197 | 12.9% / 1.236 / −14.2% | ❌ | ✅ |
| S4, broad | 12.2% | 1.063 | −15.6% | 1.173 / 0.961 | 11.8% / 1.020 / −15.6% | ✅ | ✅ |
| RULES v1, u56 | 6.5% | 0.664 | −13.8% | 0.641 / 0.688 | 7.7% / 0.747 / −13.8% | — | — |
| RULES v1, broad | 6.4% | 0.635 | −21.2% | 0.756 / 0.532 | 5.9% / 0.576 / −21.2% | — | — |
| SPY | 15.2% | 0.889 | −33.7% | 0.957 / 0.834 | 15.5% / 0.882 / −33.7% | — | — |

4b bars over this sample: Sharpe > 0.957 (H1) / 0.834 (H2) / 0.882 (OOS); MaxDD ≥ −20.2%;
CAGR ≥ 10.66%.

## The finding idea 101 was written to get

Idea 100 parked because rule 8's IS-Sharpe selector chose `f = 0.50` while only `f = 0.25` passed
4b — the selector and the KEEP bar disagreed. **That disagreement was an artefact of letting gross
float.** With g fixed at 1.00 ex ante, rule 8 picks `f = 0.50` in **44 of 60 cells** and in **4/4**
of the (universe × arm) cells at weekly / 10 bps, **at zero regret** — the same arm that passes 4b.
Fixing the exposure dial ex ante is what reconciles them; it was not a third dial being tuned.

`f = 0.50` is an interior maximum of the f-grid in 4/4 cells (u56/S3: 1.064, 1.127, **1.167**,
1.056, 0.392 for f = 0, .25, .50, .75, 1.00), so it is not a boundary artefact.

Rule 8 OOS (2017–2026) across all 60 cells: the pick beats its own `f = 0` anchor in 51/60, SPY in
44/60, RULES v1 in 60/60; OOS CAGR clears 70% of SPY's OOS CAGR in 39/60.

## Cost ladder (5 / 10 / 15 / 20 / 25 bps)

Cross-universe 4b holds to **15 bps for both arms** and dies at 20. The binding bar at 20 bps is
the **CAGR floor** (u56/S4 −0.30pp, u56/S3 −0.49pp; broad loses H2, OOS and CAGR together).
MaxDD keeps 4.5–6.9pp of headroom against the 4b cap at every rung, so this book is
cost-constrained, never risk-constrained. **4a** is more forgiving: S3 passes 4a on both universes
at every rung including 25 bps; S4 fails 4a on u56 at every rung, because its MaxDD (−14.2%) is
worse than RULES v1's (−13.8%). Idea 104's drop-DBC arm is therefore strictly the better one, which
independently confirms idea 102's deletion result.

## Idea 65's cadence bar: FAILED, and the failure belongs to the book

|ΔSharpe| across D/W/M at f = 0.50, 10 bps, g = 1.00: **0.290 / 0.329 (u56 S4/S3)** and
**0.405 / 0.438 (broad)** — 0/2 universes pass a 0.05 bar. But the `f = 0` anchor, which *is* idea
2's standing KEEP, fails identically (0.260 u56, 0.363 broad). The sleeve's own contribution
(blend minus anchor) is +0.041…+0.155, **positive in 12/12 cadence cells**, with a spread of
0.068 (u56 S3) and 0.075 (broad S3). Idea 65's bar as worded is a property of the equity book, not
a discriminator between overlays.

The sharper fact: **4b fails outright at daily cadence in 4/4 cells** (Sharpe 0.83–1.00 vs
1.06–1.17 weekly) and passes 4/4 at both weekly and monthly. Monthly dominates weekly on CAGR,
Sharpe and MaxDD in every cell. Cadence is therefore load-bearing and must be written into RULES,
not left to implementation; weekly is retained only because it is the incumbent cadence.

## Caveats

- **Survivorship.** Both equity panels are current constituents of their lists, so absolute levels
  are biased up. The bias hits the arm, its `f = 0` anchor, and RULES v1 identically, so the
  f-contrast is clean; the absolute 4b pass is not.
- **Calendar-day index (queue idea 38).** `data/prices*.csv` are calendar-indexed after 2014-09-17
  because BTC-USD is in the download. It hits every arm, the baseline and SPY identically, but it
  interacts with the cadence test specifically: the `D` cadence rebalances on weekend zero-return
  rows. The D-vs-W gap should be re-measured once idea 38 lands.
- **Gold concentration.** Idea 102 attributed 53% of the sleeve's return to GLD. Queue idea 105 is
  the open question of whether this is a gold claim or a real-asset claim; until it is answered the
  RULES wording should name the three tickers, not a category.

## Follow-ups added to the queue

- 107 — cadence-as-a-pre-registered-rule-parameter (monthly dominates weekly here; is that the
  idea-3 monthly-drawdown effect, and does it survive idea 38's index fix?)
- 108 — cost-breakeven for the S3 arm at 0.5 bp resolution, with the walk-forward spread on the
  breakeven (idea 82's protocol).

Script: `research/backtests/2026-09-05_fixed-gross-S4-blend_cloud.py`
Console: `.console.txt` · Grid: `.grid.csv` · Ladder: `.costladder.csv` · Cadence: `.cadence.csv`
· Walk-forward: `.walkforward.csv` · OOS: `.oos.csv` · Memo: `.memo.md`
