# Idea 129 — absolute-bars-disqualify-the-best-insurance (lane B, 2026-09-05)

**Verdict: ANSWERED — KILL of the claim that 4b's CAGR floor is a risk bar.** The floor at
0.70 × SPY is the *sole* cause of KILL for **48% of every arm that clears 4b's other four
bars** (27 of 56 on the reconstructed corpus; 11 of 23 on the Pareto frontier), and the arms
it excludes are **out-of-sample better on Sharpe (+0.104, t +3.22) and 8.1 pp shallower on
drawdown (t +8.97)** than the arms it admits. The only axis on which its victims are worse is
CAGR — the axis it screens on. It is a return-adequacy preference, not risk control.

Idea 95 was not an accident, and it is not rare.

## Harness and reproduction

Idea 94's script is **imported, not re-implemented**, so every number sits on the simulator
that produced the rows being audited. Corpus = 3 panels (u56, broad, small — idea 97/118's
construction verbatim) × 3 books (V1u, TOP20, EWall) × 17 arms (control, 5 gates × {dg, rw},
2 stops, 2 DD controls, 2 entry budgets) × 2 cost rungs = **306 arm-rows**, plus a 19-point
static-gross ladder per cell (342 rows) carried separately as the pure-de-grossing control.
Weekly, t+1, 75% gross, IS ≤ 2016-12-31, OOS ≥ 2017-01-01.

| check | result |
|---|---|
| (a) `run()` vs `engine.backtest`, ungated EWall u56 | max abs diff **0.00e+00** — PASS |
| (b) idea 94's published `EWall+vol60-dg` u56 @10bps (11.6% / 1.133 / −16.9%) | got **11.587% / 1.133 / −16.884%** — PASS |
| (c) re-parameterised bars at (φ=0.70, δ=0.60) vs `H.margins` on all 306 rows | **0 mismatches** — PASS |

Two tuned parameters, both bars of 4b itself: φ (CAGR floor coefficient) ∈ {0.00, 0.50, 0.60,
0.70, 0.80, 0.90, 1.00}, δ (MaxDD cap) ∈ {0.50, 0.60, 0.70}. **All 21 grid points reported.**

## Q1 — the census

| | Pareto-best rows | whole corpus |
|---|---|---|
| rows | 82 of 306 (26.8%) | 306 |
| pass 4b | 12 | 29 (9.5%) |
| **fail on the CAGR floor ALONE** | **11** | **27 (8.8%)** |
| fail on ≥1 other bar | 59 | 250 |
| **floor's share of arms clearing all four other bars** | **11 / 23 = 48%** | **27 / 56 = 48%** |

**All 11 Pareto-best floor-only victims pass KEEP path 4a.** Corpus-wide 4a passes 97/306;
both paths 6; 4a-not-4b 91; 4b-not-4a 23.

The eleven arms 4b throws away are a coherent family, not a scatter: every one is an **EWall
book with a slow trend gate de-grossed to cash** (`band3-dg`, `g200-dg`, `v1gate-dg`, plus one
`ddctl`), sitting at ~53% mean gross. Exemplar — u56 / EWall / 10 bps / `band3-dg`:
**8.7% CAGR, Sharpe 1.206, MaxDD −12.1%**, halves 1.226 / 1.191, OOS Sharpe 1.285, OOS MaxDD
−12.1%, missing the floor by 2.0 pp of CAGR. Against SPY (15.2% / 0.889 / −33.7%) and RULES v1
(6.5% / 0.66 / −13.8%) it is the best risk-adjusted book in its cell — and a KILL.

**The floor is not broken.** On the static-gross ladder — pure de-risking, zero Sharpe content
(idea 66) — the floor is the sole cause of KILL in 97 of 342 rows, and bites only at gross
multipliers ≤ 0.80. That is exactly the job it was written to do. What it cannot do is tell a
de-grossed lever from a differently-shaped book: the victims sit at 0.57 gross yet carry
*higher* OOS Sharpe than the admitted set at 0.74.

**Published-leaderboard census (INDICATIVE ONLY).** 1289 parseable numeric rows: 288 (22.3%)
meet the drawdown cap and fail the CAGR floor; 5 of the 6 Pareto-best published rows are
floor-only KILLs. Rows span different samples, universes, costs and conventions and carry no
OOS column, so this is a magnitude check on the reconstructed corpus, never a verdict. (Both
SPY reference sets in the console are identical — the two large-cap panels share one SPY
series — so the printed "range" is a single number, not a range.)

## Q2 — is the floor doing risk work?

Pre-registered: screen on the **IS window alone**, then read OOS **once**.
A = IS-admitted at (0.70, 0.60). B = rejected by the IS CAGR floor **alone**. C = rejected by
some other IS bar.

| group | n | OOS Sharpe | OOS MaxDD | OOS CAGR | mean gross |
|---|---|---|---|---|---|
| A admitted | 45 | 1.056 | −21.5% | 13.4% | 0.736 |
| **B floor's exclusive victims** | **9** | **1.160** | **−13.4%** | 9.1% | 0.569 |
| C rejected by another bar | 252 | 0.638 | −24.2% | 7.8% | 0.671 |

B − A: OOS Sharpe **+0.104** (Welch t +3.22), OOS MaxDD **+8.1 pp shallower** (t +8.97), OOS
CAGR −4.4 pp (t −7.12). Paired by cell: B beats A on OOS Sharpe in **3 of 4** cells holding
both, and is shallower on OOS MaxDD in **4 of 4** (mean +6.8 pp).

**Calibration grid — all 21 points** (n_pass out of 306; `adm_*` = mean OOS outcome of what the
bars admit). At δ=0.60, raising φ from 0 to 0.70 removes 27 of 56 admissions (−48%) and buys
**+0.002 of mean admitted OOS Sharpe while making mean admitted OOS drawdown 1.9 pp deeper**:

| φ \ δ | 0.50 | 0.60 | 0.70 |
|---|---|---|---|
| 0.00 | 25 | 56 · Sh 1.112 · DD −16.6% | 85 |
| 0.50 | 20 | 51 · 1.112 · −17.0% | 80 |
| 0.60 | 6 | 35 · 1.110 · −18.3% | 64 |
| **0.70** | 3 | **29 · 1.114 · −18.5%** | 57 |
| 0.80 | 1 | 14 · 1.143 · −19.0% | 36 |
| 0.90 | 0 | 5 · 1.175 · −19.4% | 15 |
| 1.00 | 0 | 0 | 2 |

The floor and the drawdown cap **pull against each other**: every step up in φ admits a
higher-CAGR, deeper-drawdown set. δ is by far the stronger dial (at φ=0.70: 3 / 29 / 57).

## Rule 8 walk-forward (PROTOCOL rule 8; three selectors fixed before any OOS read)

S0 = argmax IS Sharpe, no screen. S1 = argmax IS Sharpe among arms meeting the IS halves bars,
the IS DD cap at δ=0.60 and the IS CAGR floor at φ=0.70. S2 = identical with the floor deleted
(φ=0.00). 18 cells.

| selector | cells picking | mean admitted | OOS CAGR | OOS Sharpe | OOS MaxDD | beat SPY | beat v1 | beat own control |
|---|---|---|---|---|---|---|---|---|
| S0 (all 18) | 18 | 17.0 | 9.1% | 0.695 | −23.1% | 6/18 | 12/18 | 3/18 |
| S1 (floor on) | 7 | 2.5 | 12.7% | 1.022 | −21.1% | 5/7 | 7/7 | 2/7 |
| S2 (floor off) | 7 | 3.0 | 12.7% | 1.022 | −21.1% | 5/7 | 7/7 | 2/7 |

Reference OOS: SPY 0.882 / −33.7%, ungated control 0.762, RULES v1 0.451.

**The floor is inert as a selector: S1 and S2 pick the identical arm in all 7 cells where both
pick, and empty the same 11 of 18 cells.** Stronger, and stated against my own framing: **S0
restricted to those same 7 cells returns 12.7% / 1.022 / −21.1% — identical to S1 and S2.** The
whole IS 4b screen changes **0 of 18 picks**; its apparent OOS improvement over S0 is entirely
the cells where it declines to pick, not better picking. This reproduces idea 109's result
(the floor moved the pick in 8/44 cells and never for the better) on a disjoint arm family,
and sharpens it: here it moves the pick in 0 of 18.

So the floor is *non-binding where selection happens* (the IS argmax is never the arm it
excludes) and *maximally binding where adoption happens* (48% of otherwise-qualifying arms).
That asymmetry is the finding.

## What this does and does not say

- It does **not** propose a new book, and no standing candidate changes. `EWall + vol60-dg`
  passes 4b under both conventions and is untouched.
- It does **not** recommend lowering the floor to make things pass. Rule 7 stands: the grid
  above is diagnosis, not a search for a number that works.
- It **does** say that PROTOCOL's word "KILL" is wrong for this class of arm, and proposes the
  reporting clause in the memo.

## Caveats, stated not buried

- **n = 9.** Group B is nine arm-rows in four cells, and they are *not* independent — same
  panels, same book (EWall), overlapping return series. The Welch t's describe this corpus,
  not a population; the paired-by-cell counts (3/4 and 4/4) are the honest version and they
  are small. The effect is large and consistently signed, and that is all that is claimed.
- **Survivorship** (idea 54): all three panels are current-constituent lists. Absent
  delistings inflate every arm's CAGR and inflate the *ungated* books most, so the floor's
  real-world exclusion of defensive arms is if anything understated here.
- **Idea 128**: the IS window's SPY MaxDD is 65% (u56/broad) and 55% (small) of the full
  sample's, so the IS drawdown cap is measured on a window that cannot express deep
  drawdowns. This biases the S1/S2 screen toward admitting too much.
- **Idea 38**: u56 and broad still carry the calendar-day index.
- **Idea 126**: every number is quoted at t+1 execution only; no lag band is claimed.
- One console line under Q2b ("B beats A's cell-mean OOS Sharpe in 1 of 1 pooled comparison")
  is vacuous formatting, superseded by the paired-by-cell lines beneath it.

Script: `research/backtests/2026-09-05_cagr-floor-calibration_B.py`
Console: `.console.txt` · Corpus: `.grid.csv` · Ladder: `.ladder.csv` ·
Calibration: `.calibration.csv` · Risk-work: `.riskwork.csv` · Walk-forward: `.walkforward.csv`
Memo: `.memo.md`
