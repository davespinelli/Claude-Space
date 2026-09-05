# Idea 100 — sleeve-with-a-real-diversifier — **mechanism CONFIRMED, queue wording REFUTED on the CAGR half; PARK a strictly-dominant successor to idea 26's by-product**

**Independent second run.** The cloud lane ran the same idea the same day; both reach PARK and every shared number agrees to the printed precision (correlation, +0.265 vs +0.052 convexity, 0.090 vs 0.031 exchange rate, S4 standalone 2.6%/0.616/-8.7%). What this run adds is the **gross-matched** convention — where the arm is a cross-universe 4b pass at the protocol's own 10 bps with no third dial — its cost ladder, and the paired S4-vs-S9 census. See `2026-09-05_sleeve-with-a-real-diversifier_cloud.result.md` for the cloud run's re-grossing diagnostic.

Lane B, 2026-09-05. Script `research/backtests/2026-09-05_sleeve-with-a-real-diversifier_B.py` · console `…_B.console.txt` · grids `…_B.grid.csv` / `.correlations.csv` / `.diversification.csv` / `.paired.csv` / `.walkforward.csv` / `.costladder.csv` / `.ex2022.csv`.

**120 grid points, all reported** = 5 sleeve fractions f ∈ {0.00, 0.25, 0.50, 0.75, 1.00} × 2 sleeves × 3 equity books × 2 universes × 2 gross conventions. Two tuned parameters (f, sleeve). Book, universe and convention are reported dimensions, not selected over. 10 bps, weekly, t+1, long-only, no leverage. Eval window 2009-01-13 → 2026-09-04 after the 260-day warm-up.

**Harness check:** reproduces idea 2's published 4b KEEP row on u56 (12.66% / 1.092 / -18.31%, halves 1.088 / 1.102) and its known broad-universe H2 failure (0.811 vs SPY 0.834), and idea 26's `top20 + 25% S9` by-product to 3 decimals.

Sleeves, identical construction (idea 18 variant B — {12-1, 6m, 3m} momentum-sign votes × inverse-60d-vol risk parity, gross 1.0 inside the sleeve):
- **S9** = SPY QQQ IWM EFA EEM TLT GLD DBC UUP — idea 26's sleeve verbatim. CONTROL.
- **S4** = TLT GLD DBC UUP — the idea's sleeve.

## Claim (A) — is S4 genuinely the less correlated sleeve? **YES, decisively**

Daily-return correlation to the books it is meant to diversify:

| | v1 | top20 | ewall | SPY |
|---|---|---|---|---|
| S9 (u56 / broad) | 0.726 / 0.626 | 0.820 / 0.743 | 0.800 / 0.750 | 0.635 |
| **S4** (u56 / broad) | 0.212 / 0.130 | **0.120 / 0.035** | 0.107 / -0.011 | **-0.142** |

Lower in 8/8 cells, mean gap **-0.678**. Dropping the five equity ETFs turns a 0.63–0.82-correlated overlay into a 0.04–0.21-correlated one that is *negatively* correlated with SPY.

## Claim (B) — does that buy the same convexity? **It buys 5.1× as much — but NOT "at less CAGR"**

`dSharpe(f) = Sharpe(blend) − [(1−f)·Sharpe(f=0) + f·Sharpe(f=1)]`, positive = real diversification.

| sleeve | n | mean dSharpe | median | range | positive | mean dCAGR (pp) | median Sharpe per pp of CAGR |
|---|---|---|---|---|---|---|---|
| S9 | 36 | +0.052 | +0.050 | [+0.008, +0.085] | 36/36 | -2.15 | 0.031 |
| **S4** | 36 | **+0.265** | +0.216 | [+0.070, +0.479] | 36/36 | **-3.19** | **0.090** |

Paired cell by cell (same universe/book/convention/f): **S4 buys more convexity in 36/36 cells** (mean +0.212), and buys more Sharpe *per pp of CAGR surrendered* in 32/36 — but its absolute CAGR toll is **larger in 36/36** (mean 1.04 pp more). The queue line asked whether lower correlation buys the same convexity "at less CAGR": convexity yes and then some, CAGR **no** — S4 costs strictly more.

The reason is visible in the standalone rows: S4 is the *worse* sleeve on its own (2.6% CAGR / 0.616 Sharpe / -8.7% MaxDD vs S9's 5.0% / 0.868 / -10.1%). The convexity is bought by ρ, not by the sleeve's own quality — `d(Sharpe_blend)/df|₀ ∝ (Sharpe_S − ρ·Sharpe_E)·σ_S/σ_E`, and S4's ρ ≈ 0.03–0.12 against top20 more than pays for its 0.25 lower standalone Sharpe. **A sleeve does not have to be good to diversify; it has to be uncorrelated.** That is the transferable finding.

## The arm: `top20 + 25% S4, gross-matched`

| Arm | CAGR | Sharpe | MaxDD | H1 / H2 | OOS CAGR / Sharpe / MaxDD | Turn/yr | 4a | 4b |
|---|---|---|---|---|---|---|---|---|
| u56 · top20 · f=0.00 (incumbent, idea 2) | 12.66% | 1.092 | -18.31% | 1.088 / 1.102 | 14.36% / 1.168 / -18.3% | 9.6× | — | PASS |
| u56 · top20 · +25% S9 matched (idea 26) | 11.09% | 1.089 | -16.26% | 1.082 / 1.098 | 12.43% / 1.171 / -16.3% | 8.8× | FAIL | PASS |
| **u56 · top20 · +25% S4 matched** | **10.83%** | **1.142** | **-14.61%** | **1.127 / 1.159** | 12.08% / **1.217** / -14.6% | 9.2× | FAIL | **PASS** |
| broad · top20 · f=0.00 (incumbent) | 13.09% | 0.957 | -20.05% | 1.125 / **0.811** | 12.49% / 0.892 / -20.1% | 13.8× | PASS | FAIL (H2, OOS) |
| broad · top20 · +25% S9 matched | 11.50% | 0.974 | -17.67% | 1.124 / 0.839 | 11.06% / 0.924 / -17.7% | 12.1× | PASS | PASS |
| **broad · top20 · +25% S4 matched** | **11.26%** | **1.011** | **-16.05%** | **1.174 / 0.865** | 10.66% / **0.941** / -16.1% | 12.5× | PASS | **PASS** |
| RULES v1 baseline (u56 / broad) | 6.5% / 6.4% | 0.664 / 0.635 | -13.8% / -21.2% | 0.641/0.688 · 0.756/0.532 | 0.747 / 0.576 | — | — | — |
| SPY | 15.2% | 0.889 | -33.7% | 0.957 / 0.834 | 15.5% / 0.882 / -33.7% | — | — | — |

4b bars on this window: H1 > 0.957, H2 > 0.834, OOS Sharpe > 0.882, MaxDD ≥ -20.2%, CAGR ≥ 10.66%.

**S4 dominates its S9 twin on every risk axis at 0.24–0.26 pp less CAGR** — higher Sharpe (+0.053 / +0.037), shallower MaxDD (+1.65 / +1.62 pp), higher H1, H2 and OOS Sharpe — and it is a cross-universe 4b pass under the matched convention, as S9's is. Against the incumbent it costs 1.83 pp of CAGR on both universes and returns +0.050 / +0.054 Sharpe with a 3.7 / 4.0 pp shallower drawdown, repairing idea 2's broad-universe H2 shortfall (0.811 → 0.865 vs SPY's 0.834). Census: **120 points, 4a passes 78, 4b passes 14**; interior points only (f ∈ {0.25, 0.50, 0.75}) 72 points, 4a 61, 4b 6 (S9 4, S4 2). Cross-universe 4b passes: `top20/S4/matched/f=0.25`, `top20/S9/matched/f=0.25`, `top20/S9/natural/f=0.25`.

## The three things that killed idea 26's by-product, re-tested

1. **Rule-8 selectability — HALF FIXED.** Idea 26's S9 sleeve had IS Sharpe *monotone decreasing* in f, so the 2009-2016 selector picked f = 0.00 in all four top20 cells. With S4 the IS curve is **hump-shaped**: the selector picks **f\* = 0.50** in all four top20 cells and all four ewall cells (IS Sharpe 1.041/1.071 vs f=0's 0.993 on u56). f\*=0.00 now appears in only 8 of 24 cells (all of them S9). So the objection "rule 8 cannot see this overlay" no longer holds — but the selector **overshoots**: at f=0.50 OOS Sharpe is excellent (1.266 u56 / 1.001 broad vs SPY 0.882, beats the baseline in 24/24 cells and SPY in 21/24) while OOS CAGR falls to 9.6% / 8.6%, below the 10.66% floor. **The arm that passes 4b (f=0.25) is not the arm rule 8 selects (f=0.50).** Under PROTOCOL rule 8 as written that is PARK, not KEEP — the same disqualifier idea 26 applied, in a new shape.
2. **One-year dependence — FIXED.** Idea 26 was killed partly because S9's contribution was negative in 17/18 years, with 2022 carrying everything. Deleting 2022 entirely: S4's Sharpe edge over the pure book survives (u56 +0.050 → **+0.038**; broad +0.054 → **+0.046**), while S9's does not (u56 -0.004 → -0.007; broad +0.017 → +0.016). S4's *return* contribution is still negative in 16/18 years (positive only 2011 and 2022) — the edge is vol reduction, not return — but it is no longer a single-year artefact.
3. **Cost — NOT FIXED.** The cross-universe 4b pass survives 5 and 10 bps and dies at 15, identically for S4 and S9 (u56 CAGR 10.3% vs the 10.66% floor; broad H2 0.811). PROTOCOL's 10 bps sits on the edge of the window, exactly as it did for idea 26.

## Verdict

**PARK.** The mechanism the queue proposed is confirmed and is stronger than expected — a genuinely uncorrelated four-asset sleeve buys 5.1× the Sharpe convexity of idea 26's nine-asset one, in 36/36 cells, despite being the worse sleeve standalone. The queue's specific wording ("at less CAGR") is **refuted**: S4's CAGR toll is larger in 36/36 cells, though its Sharpe-per-pp exchange rate is better in 32/36. `top20 + 25% S4 matched` is a strictly better version of idea 26's PARK — cross-universe 4b, dominant on every risk axis, and it now survives both the rule-8 *visibility* problem and the one-year test — but it is still not a KEEP: rule 8 selects f=0.50, which fails 4b's CAGR floor, and the f=0.25 pass dies by 15 bps. No memo, no RULES wording proposed.

_Research, not investment advice. Both universes are current constituents — survivorship bias is upward and unquantified, and it favours the equity book over the sleeve, so the sleeve's measured contribution is if anything understated. Data caveat (queue idea 38): `data/prices*.csv` are calendar-day indexed after 2014-09-17, so post-2014 weekends are zero-return rows; this deflates daily vol identically for every arm including the baseline and SPY, so cross-arm comparisons hold but absolute Sharpe levels do not._
