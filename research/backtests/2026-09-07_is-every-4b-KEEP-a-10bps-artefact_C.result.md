# Idea 323 — is-every-4b-KEEP-in-the-record-a-10bps-ARTEFACT (lane C, 2026-09-07)

**ANSWERED — premise CONFIRMED with exactly one exception, and one premise correction.
At 25 bps, 1 of the record's 10 standing weekly 4b cells survives: `U56 / BAND12`
(idea 291's band `b=0.12` book, 1.93x turnover/yr), which clears 4b at every rung out to
50 bps. The other nine die between 6.8 and 24.7 bps. Separately: RULES v2, the LIVE book,
has never been a 4b pass at all — it fails the CAGR floor at ZERO cost on both panels.**

Script: `research/backtests/2026-09-07_is-every-4b-KEEP-a-10bps-artefact_C.py`
Console: `…_C.console.txt` · Grid: `…_C.grid.csv` (378 rows) · `…_C.breakeven.csv` · `…_C.walkforward.csv`

## The question and the design

Idea 47 swept cost × lag on four books of ONE family and found 0/180 cells passing 4b at 25 or
50 bps. The queue asks whether that is a fact about that family or about PROTOCOL rule 4b: re-run
the record's OTHER standing 4b passes on a cost ladder and count the survivors.

Books, all fixed in advance, each taken from the record verbatim — `N20` (idea 2's KEEP),
`F085` (idea 46), `BAND12` (idea 291's PARKed cell: 200d band b=0.12, RESPREAD, 75% gross),
`BRCASH` (idea 48's breadth cash gate at the causal q=0.20 quintile), `RULESv2` (the live book),
plus `NF20` and `EWALL` as controls. Panels U56 and B136 (SMALL439 not re-run: idea 47 already
reported 0/60 there at every cost and lag).

**Two tuned parameters, all points reported:** `cost_bps ∈ {0,5,10,15,20,25,30,40,50}` ×
`cadence ∈ {W,M,Q}` = 27 cells per book per panel, **378 cells total**. Cadence is the second
axis because the queue's own second clause is a *turnover budget*, and cadence is the record's
cheapest turnover instrument.

Costs are analytic (`r_c = r_0 − turnover·c/1e4`) from one zero-cost run per cell, **gated against
`engine.backtest` at 10 bps on all 42 (book, cadence, panel) cells: max|diff| = 0.000e+00**.

**Reproduction check (before anything else was read).** U56 @10 bps weekly:
`N20` 12.66% / 1.092 / −18.31% (1.088/1.102) = idea 2's published KEEP to 3 dp;
`F085` 11.32% / 1.071 / −16.67% = idea 46's 11.3% / 1.072 / −16.7%;
`BRCASH` 12.20% / 1.131 / −12.68%, OOS 1.240 = idea 315's quote exactly;
`RULESv2` 8.66% / 1.206 / −12.05% = idea 48's table.
`BAND12` 14.02% / 1.226 / −19.42% against idea 291's published 14.09% / 1.233 / −19.4% — the one
cell that does not reproduce to 3 dp (−0.007 Sharpe, a warm-up/start-date difference, not a
construction one).

## 1. The census

4b bars on this sample (SPY 15.23% / 0.889 (0.957/0.834) / −33.72%, OOS 0.882):
H1 > 0.957, H2 > 0.834, OOS > 0.882, MaxDD < 20.23%, CAGR > 10.66%.

Pooled over both panels, all 7 books, all 3 cadences (42 cells per rung):

| bps | 0 | 5 | 10 | 15 | 20 | 25 | 30 | 40 | 50 |
|---|---|---|---|---|---|---|---|---|---|
| 4b passes | 14 | 14 | 12 | 10 | 9 | 6 | **5** | 5 | 5 |

The record's five *standing* passes at their own weekly cadence (5 books × 2 panels = 10 cells):

| bps | 0 | 5 | 10 | 15 | 20 | 25 | 30 | 40 | 50 |
|---|---|---|---|---|---|---|---|---|---|
| 4b passes | 7 | 7 | 6 | 4 | 3 | **1** | 1 | 1 | 1 |

**4a: 0/378** — nothing beats RULES v2 in both halves at any rung, as the record keeps finding.

## 2. The premise correction: RULES v2 is not a 4b pass and never was

The queue lists "RULES v2 itself" among the standing 4b passes. It is not one. Its CAGR is
8.66% (U56) / 8.03% (B136) against a floor of 10.66%, so it fails the CAGR bar **at zero cost,
on both panels, at all three cadences** — 6/6 cells, first failing bar `CAGR` every time. The
live book is a Sharpe/drawdown book that 4b's growth floor rejects; that is a fact about the
book, not about costs, and it means only **four** of the queue's five items were ever eligible
for this census.

At the 10 bps anchor the four eligible ones pass 6 of 8 cells: U56 all four; B136 `F085` and
`BRCASH` only (`N20` fails H2 by −0.023 — lane B's independent B136 result today, `BAND12` fails
the DD cap at −21.74%).

## 3. The one survivor, and why it is the one

| panel/book/cadence | turnover/yr | 25 bps: CAGR / Sharpe / MaxDD | H1 / H2 | OOS Sharpe | 4b breakeven |
|---|---|---|---|---|---|
| **U56 / BAND12 / W** | **1.93** | **13.69% / 1.200 / −19.53%** | 1.236 / 1.177 | **1.239** | **> 50 bps** |
| U56 / N20 / W | 9.62 | fails (H1) | — | — | 24.7 |
| U56 / BRCASH / W | 9.72 | fails (H1) | — | — | 23.3 |
| U56 / NF20 / W | 10.77 | fails (H1) | — | — | 22.6 |
| U56 / F085 / W | 9.58 | fails (CAGR) | — | — | 16.2 |
| B136 / F085 / W | 9.51 | fails (CAGR) | — | — | 14.8 |
| B136 / BRCASH / W | 13.41 | fails (H2) | — | — | 11.5 |
| B136 / N20 / W | 13.75 | fails (H2) | — | — | 7.7 |
| B136 / NF20 / W | 14.09 | fails (H2) | — | — | 6.9 |
| B136 / BAND12 / W, both RULESv2 | 2.06 / 1.8–2.0 | fails at 0 bps (DD / CAGR) | — | — | 0 |

`BAND12` on U56 is not marginal at 25 bps: its slack over the five bars is
H1 +0.279, H2 +0.343, OOS +0.357, DD +0.70 pp, CAGR +3.03 pp. Across the whole ladder its
Sharpe falls only 1.244 → 1.156 (0 → 50 bps) because it turns over 1.93x/yr, five to seven
times less than the ranked books. Its binding bar out past 50 bps is the DD cap, whose margin
decays +0.88 pp → +0.53 pp over the ladder (linear extrapolation ≈ 125 bps).

## 4. The turnover budget, in closed form

Cost enters as `−T·c`, so `Sharpe(c) = (μ − T·c)/σ` and the breakeven for any Sharpe bar is
`c*_bps = 1e4 · margin · σ / T` (for the CAGR floor, `1e4 · margin / T`). Tested against the
interpolated crossings on the 9 cells that have one: **mean error +0.9 bps, MAE 1.2 bps.**
The empirical drag fits `dSharpe/10bps = −0.00785·T − 0.0022` (corr **−0.983**, n=42), i.e.
σ ≈ 0.124 as the identity requires.

> **Usable form:** a book clears 4b at `c` bps only if its annual turnover
> `T ≤ 1e4 · (its smallest 4b margin, in σ units) / c`.
> At 25 bps on these panels that bites at **T ≲ 6.2x NAV/yr**; every 9.5–14x book dies short of it.

## 5. Does slowing the cadence buy the rung back? On one panel only

Monthly rescues the whole ranked family **on U56** — `N20/M`, `F085/M`, `NF20/M`, `BRCASH/M` all
clear 4b at every rung to 50 bps (predicted breakevens 71–81 bps) because monthly halves turnover
(9.6 → 4.3x) *and* raises Sharpe (1.176 → 1.239 at 0 bps). On **B136 it fails at zero cost**: the
same slowdown deepens MaxDD past the cap (`N20/W` −19.98% → `N20/M` −26.07% vs a −20.23% cap), so
5 of the 7 B136 monthly cells fail on `DD` before any cost is charged (`BRCASH/M` is the one that
survives, out to 29.5 bps; `RULESv2/M` fails on CAGR as always). **Quarterly is 0/126** — every
cell, both panels, every rung, on `DD`. Cadence is a cost instrument with a drawdown bill, and
whether you can afford it is a panel fact.

## 6. Rule 8 (walk-forward, required)

Book × cadence chosen on 2009–2016 only at each (panel, cost) cell, 2017–2026 read once.
S1 = best IS Sharpe; S2 = best IS Sharpe among cells clearing the IS 4b bars. 18 cells each.

| chooser | beats N20/W anchor | beats RULES v2 | beats SPY | mean OOS Sharpe | vs anchor | mean regret |
|---|---|---|---|---|---|---|
| S1 | **18/18** | 4/18 | 18/18 | 1.1383 | 0.9260 (**+0.2123**) | 0.0856 |
| S2 | **18/18** | 4/18 | 18/18 | 1.1365 | 0.9260 (**+0.2105**) | 0.0874 |

This is the record's rare *positive* chooser result, and it is a cost artefact of the opposite
sign: the anchor `N20/W` is the high-turnover book, so its OOS Sharpe decays 1.247 → 0.852 (U56)
and 0.991 → 0.496 (B136) across the ladder while the chooser walks to the cheap book. S2 picks
`BAND12/W` 11/18, `N20/M` 6/18, `EWALL/Q` 1/18. It still loses to the live RULES v2 in 14/18.
The honest reading: an IS chooser cannot pick an *edge*, but it can pick a *cost*.

## Verdict — **CONFIRMED (with one exception), no new KEEP**

- The queue's "≈0 survive" prediction is right in 9 of 10 standing weekly cells and right for
  the entire ranked family. **PROTOCOL rule 4b owes a cost rung**; on this evidence the honest
  one is 25 bps, which is where the record's 10-bps footprint collapses from 6/10 to 1/10.
- **PROTOCOL rule 4b owes a turnover budget too**, and §4 gives it in closed form rather than as
  a number to be re-fitted per idea.
- `U56/BAND12/W` **stays PARK, not KEEP**, for the three reasons idea 291 already gave (b=0.12 is
  the grid edge in 4/4 arms; the same cell fails 4b on B136, here at *every* cost including zero,
  on the DD cap; rule 8 inside its own band arm picks (0.02, Q) → OOS 1.084). What this run adds
  is that it is the only 4b passer in the record that is not a 10-bps artefact — it is the
  strongest standing candidate for a Sunday review, and the first thing that should be re-run if
  the b-grid is ever extended past 0.12.
- RULES v2, the live book, is not and has never been a 4b pass. Any future claim that the live
  rules are "capital-worthy" under 4b needs to be withdrawn.

**SURVIVORSHIP:** U56 and B136 are current-constituent lists, so all absolute CAGRs are
optimistic. This run holds names, days, filter, gross and fill fixed and moves only the cost rung
and the cadence, so the cost ordering — the durable part — is far less exposed than the levels.
