# Idea 542 — does MA-THRESH θ=0 beat RULES v2's 3% band on its own terms? (lane C, 2026-09-09)

**VERDICT: ANSWERED / KILL for θ=0. The band earns its two numbers. At matched gross,
cadence and construction, θ=0 loses to the live 3% band in 24 of 24 paired cells — worse
Sharpe, worse CAGR, worse MaxDD, and 1.73x/yr MORE turnover. Idea 299's "only 4b cell" was
an artefact of its FAMILY axis, not a property of θ=0: at idea 299's own operating point 5
of my 6 bands clear 4b on both required panels, and the live 0.03 dominates 0.00 on all
three headline numbers there. RULES v2 unchanged; RULES.md, scan.py, bot.py, baseline.py
untouched. No new KEEP.**

Script: `research/backtests/2026-09-09_does-MA-THRESH-theta-0-beat-RULES-v2-s-3-percent-BAND-on-its-own-terms_C.py`
Artefacts: `.grid.csv` (144 books), `.paired.csv` (24 matched cells), `.boot.csv`,
`.walkforward.csv`, `.console.txt`.

## What was priced

The band is not a rival family — it is the same 200d-MA gate with one dial, and θ=0 **is**
band = 0.00 (gate G3). Two pre-registered dials, every point reported, none selected on:

| dial | values |
|---|---|
| BAND | 0.00 (θ=0, challenger), 0.01, 0.02, **0.03 (live)**, 0.05, 0.08 |
| GROSS | 0.25, 0.50, **0.75 (live)**, 1.00 |

Fixed: weekly cadence (live), 10 bps, next-day execution, IS ≤ 2016-12-31 / OOS ≥ 2017-01-01.
CONSTRUCTION is a reported control, not a dial: **DEGROSS** (gated-out weight → cash) is the
live form and the only one a KEEP could come from; **RESPREAD** (equal weight over held names)
is idea 299's book form. 6 × 4 × 2 × 3 panels = 144 books.

### Gates (all passed before any verdict was read)

- **G1** vectorised runner vs `engine.backtest` on the live U56 v2 book: max abs diff **1.735e-17**.
- **G2** `book(0.03, 0.75, DEGROSS)` vs `baseline.rules_v2_weights`: max abs diff **0.000e+00**.
- **G3** θ=0 identity: band 0.00 differs from `px > ma200` on **0/258,500** U56 cells,
  **3/634,365** B136, **63/1,841,166** SMALL439 — and every single disagreement is an exact
  tie `px == ma` (TLT 2012-10-18, BSX 2018-02-27, IBM 2022-04-08 on B136), where the
  hysteresis holds the prior state and the strict inequality says OUT. The identity holds.
- **G4 (unplanned, post-hoc)** the grid reproduces idea 299's committed cell to every quoted
  digit: U56 band 0.00 / 0.75 / RESPREAD = **11.5938% / 1.094826 / -18.6230%** (quoted
  11.59% / 1.0948 / -18.62%), B136 = **11.6593% / 1.058499 / -20.1167%** (quoted 11.66% /
  1.0585 / -20.12%). The challenger under test is the same object idea 299 published.

## B1 — the head-to-head: θ=0 loses everywhere

**0 of 24** matched (panel × gross × construction) cells have θ=0 with higher Sharpe and no
worse MaxDD. On the two required panels: **0 of 16**. Means over the 24 cells (0.00 − 0.03):
**ΔSharpe −0.0363, ΔCAGR −0.363 pp, ΔMaxDD −0.495 pp (deeper), Δturnover +1.734 x/yr.**
The sign is the same in every cell for Sharpe, CAGR and turnover.

At the LIVE operating point (gross 0.75, DEGROSS, weekly):

| panel | book | CAGR | Sharpe | MaxDD | OOS Sharpe | turnover/yr |
|---|---|---|---|---|---|---|
| U56 | θ=0 (band 0.00) | 8.20% | 1.1745 | -12.06% | 1.2630 | 3.15x |
| U56 | **live band 0.03** | **8.67%** | **1.2108** | **-11.90%** | **1.2904** | **1.79x** |
| B136 | θ=0 (band 0.00) | 7.78% | 1.0952 | -12.64% | 1.1260 | 3.33x |
| B136 | **live band 0.03** | **8.03%** | **1.1078** | **-12.18%** | **1.1206** | **2.02x** |

At idea 299's own operating point (gross 0.75, RESPREAD) the live band also wins on all
three headline numbers: U56 12.30% / 1.1664 / -17.64% vs θ=0's 11.59% / 1.0948 / -18.62%;
B136 11.76% / 1.0712 / -18.49% vs 11.66% / 1.0585 / -20.12%.

**Idea 299's uniqueness claim does not survive the band axis.** Within my grid, **9 of 48**
(band, gross, construction) cells clear 4b on BOTH required panels, and at idea 299's exact
cell shape (gross 0.75, RESPREAD) that is bands **0.00, 0.01, 0.02, 0.03 and 0.05** — five of
six. θ=0 was "the only cell" only because idea 299's axis was FAMILY at a fixed band.

## B2 — but the band's Sharpe edge is inside the noise

Paired circular-block bootstrap (2000 draws, 21d blocks, seed 0) at the live operating point,
positive = θ=0 better:

| panel | ΔSharpe | 95% CI | ΔCAGR | 95% CI (pp) | t(daily diff) | P(θ=0 better) |
|---|---|---|---|---|---|---|
| U56 | -0.0363 | [-0.0897, +0.0130] | -0.46 pp | [-0.85, -0.09] | -2.16 | 6.6% |
| B136 | -0.0126 | [-0.0551, +0.0273] | -0.25 pp | [-0.58, +0.06] | -1.36 | 26.6% |
| SMALL439 | -0.0323 | [-0.0641, -0.0019] | -0.25 pp | [-0.47, -0.03] | -1.96 | 1.9% |

Honest reading: on the two REQUIRED panels the Sharpe difference **straddles zero**, so the
band does not buy a statistically distinguishable Sharpe. What it does buy is (i) a sign that
never flips — 24/24 cells — (ii) a CAGR gap that excludes zero on U56, and (iii) a **43% cut
in turnover** (1.79x vs 3.15x/yr at the live point), which is not a statistical claim at all:
it is a deterministic property of the hysteresis and it is what the two extra numbers are for.
The band is retained because it is never worse and it trades half as much, not because it
wins a significance test.

## B3/B4 — rule 8 walk-forward

IS Sharpe is monotone in the band on every panel and both constructions (U56 DEGROSS:
1.0620 → 1.1093 → 1.1270 for 0.00 / 0.03 / 0.08). **IS never picks θ=0, anywhere.** The
one-dial pick at live gross is band 0.08 on all panels and both constructions; OOS it beats
SPY on both required panels (U56 OOS Sharpe 1.1821, B136 1.1139 vs SPY 0.8786/0.8820) but
fails 4b full-sample on the CAGR floor at gross 0.75.

The two-dial pick (IS Sharpe subject to the IS drawdown cap; the cap never bound) lands on
**(band 0.08, gross 1.00, DEGROSS)** on both required panels and clears 4b there — U56
11.47% / 1.1570 / -18.91% (OOS Sharpe 1.1810), B136 11.48% / 1.1271 / -19.44% (OOS 1.1125).

**This is PARKed, not promoted, and the grid says why.** On DEGROSS, Sharpe is invariant in
gross to 3 decimals (U56 band 0.03: 1.2108 at 0.75, 1.2106 at 1.00) and the ONLY failing 4b
bar at gross 0.75 is CAGR, on every band and both required panels. So the 4b pass is bought
entirely by the gross dial, exactly as idea 404 published — the band choice is irrelevant to
it. The live band at gross 1.00 (U56 11.60% / 1.2106 / -15.71%, B136 10.73% / 1.1077 /
-16.08%) dominates the walk-forward pick, and is simply RULES v2 with one dial moved. It
buys 2.9 pp of CAGR for 3.7 pp of drawdown; that is a gross decision for the Sunday review,
not a research finding, and no memo is written for it.

One sharp corollary in the live form: at gross 1.00 on B136, **θ=0 FAILS 4b on the CAGR
floor (10.39% vs 10.66% required) exactly where the live 0.03 band clears it (10.73%).**

## Both KEEP paths, all 144 books

**4a 3/144** — all three are U56, band 0.03, DEGROSS, at gross 0.25/0.50/0.75: the live book
with SPY removed from the *investable* set. (The baseline is `rules_v2_weights` on the full
`load_universe()` panel, which holds SPY as a constituent; the graded panels drop it, per idea
299's convention. Dropping it moves H1 1.2309 → 1.2360 and H2 1.1828 → 1.1916, which is the
entire 4a "win". It is a bookkeeping difference, not an edge.) **4b 21/144** (U56
12, B136 9, SMALL439 **0 of 48**). **BOTH: 0/144.** With 144 books reported the 4b rate is
14.6%; nothing here is selected on and no cell is claimed as a new rule.

## Caveats

SURVIVORSHIP: U56, B136 and SMALL439 are CURRENT constituents — no delistings — so every CAGR
level above is inflated and both KEEP columns inherit that whole. SMALL439 additionally drops
the 44 tickers with `max_1d_move >= 1.0`. Costs are 10 bps flat; no cost-rung robustness leg
was run here (the head-to-head is not cost-fragile in direction — θ=0 trades MORE, so a
higher cost rung widens the band's win). The bootstrap is a paired block bootstrap on daily
net returns and inherits the usual dependence caveats.
