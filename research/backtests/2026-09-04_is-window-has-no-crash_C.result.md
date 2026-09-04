# idea 89 — is-window-has-no-crash (lane C, 2026-09-04) — **KILL the amendment; premise REFUTED**

Script `research/backtests/2026-09-04_is-window-has-no-crash_C.py`, console
`…_C.console.txt`, grids `…_C.grid.csv` (66 points), selections `…_C.selections.csv` (36).
Two parameters: the grid parameter and the SPLIT DATE. **All 66 grid points and all 36
selections are reported.** Universes: universe.json (56) and universe_broad.json (136);
SURVIVORSHIP — current constituents, absolute CAGRs optimistic, but the bias hits every
arm and every split alike. Weekly, t+1 execution, 10 bps.

Splits: **S13** IS 2009-2013 / OOS 2014-2026 · **S16** IS 2009-2016 / OOS 2017-2026
(incumbent rule 8) · **S21** IS 2009-2021 / OOS 2022-2026. Grids re-run verbatim from
idea 87's harness: GROSS/top20, GROSS/EWall, BAND/ew-all, N/ranked, CRYPTO/CAND20,
CRYPTO/EWall.

## (b) The premise is wrong in both of its halves

| split | SPY IS MaxDD | SPY OOS MaxDD | IS 4b DD bar | arms clearing IS DD bar (u56 / broad) | arms clearing IS CAGR floor |
|---|---|---|---|---|---|
| S13 | -22.1% | -33.7% | -13.2% | 27/33 · 19/33 | 4/33 · 20/33 |
| S16 | -22.1% | -33.7% | -13.2% | 27/33 · 19/33 | 17/33 · 29/33 |
| S21 | **-33.7%** | -24.5% | **-20.2%** | **30/33 · 24/33** | 23/33 · 28/33 |

1. **S13 and S16 have the identical IS MaxDD (-22.1%)** — 2011 is the in-sample maximum in
   both — so the DD bar, the feasible set and the crash content are literally unchanged
   between them, yet 8/12 selections still move. Pick instability is therefore **not**
   caused by the IS window's crash content.
2. **Putting COVID in-sample makes 4b's DD cap LOOSER, not tighter** (bar -13.2% → -20.2%;
   arms clearing it 27→30 on u56, 19→24 on broad). The cap is *relative to SPY on the same
   window*, and a trend-gated book draws down less than SPY in a crash, so a crash inside
   the window widens the book's margin. The DD cap cannot be made binding by moving the
   split. **The binding in-sample constraint is the CAGR floor** (u56: 4/33 → 17/33 → 23/33
   across splits), which is the opposite of idea 87's stated diagnosis.

## (a) Selections do move — but mostly where rule 8 has nothing to select on

| universe | grid | S13 | **S16** | S21 |
|---|---|---|---|---|
| u56 | BAND/ew-all | 0.02 | **0.08** | 0.08 |
| u56 | CRYPTO/CAND20 | 0.00 | **0.15** | 0.15 |
| u56 | CRYPTO/EWall | 0.00 | **0.15** | 0.15 |
| u56 | GROSS/EWall | 1.00 | **1.00** | 0.50 |
| u56 | GROSS/top20 | 0.50 | **0.80** | 0.70 |
| u56 | N/ranked | 40 | **20** | 40 |
| broad | BAND/ew-all | 0.08 | **0.08** | 0.08 |
| broad | CRYPTO/CAND20 | 0.00 | **0.15** | 0.15 |
| broad | CRYPTO/EWall | 0.00 | **0.15** | 0.15 |
| broad | GROSS/EWall | 1.00 | **1.00** | 0.50 |
| broad | GROSS/top20 | 1.00 | **1.00** | 1.00 |
| broad | N/ranked | 20 | **30** | 40 |

**S13 changes 8/12, S21 changes 5/12; only 2/12 cells are stable across all three.** But
applying idea 87's proposed 8a selectability pre-test (IS Sharpe spread ≥ 0.01 across the
grid): only **3 of 8** (S13) and **2 of 5** (S21) changed cells sit on a selectable grid.
The rest are the GROSS grids (IS Sharpe spread 0.0001–0.0007 across a 2× change in gross —
a fourth confirmation of idea 66) and the CRYPTO grids under S13, whose IS window **ends
before BTC history begins**, making every arm's IS Sharpe identical to 4 decimal places
(Spearman undefined) and the pick a tie-break artefact. That degeneracy accounts for the
only four large consequences in the whole run (+0.06…+0.16 2022+ Sharpe) and is a
data-coverage bug in the selection, not evidence about crash content.

**Consequence on the common window (2022+, out-of-sample for all three splits):** every
changed cell on a selectable grid moves realised Sharpe by **≤ 0.034**, and the two N/ranked
flips that touch a standing candidate move it by **0.000** (u56 n=20 → n=40: 1.100 → 1.099).
Mean 2022+ Sharpe of the 12 picks: **S13 0.954 · S16 0.924 · S21 0.924** (CAGR 10.8/11.8/10.3%,
MaxDD -15.8/-18.8/-16.5%). The split date is worth ~0.03 Sharpe.

## (c) The incumbent split selects best of the three

| split | mean regret vs grid OOS-best | mean OOS rank | picks grid-best | beats default arm | mean ρ(IS Sh, OOS Sh) | picks passing OOS-4b |
|---|---|---|---|---|---|---|
| S13 | -0.059 | 3.42 / 5.5 | 4/12 | 5/12 | +0.205 | 8/12 |
| **S16** | **-0.028** | **3.08** | 2/12 | **9/12** | **+0.361** | 4/12 |
| S21 | -0.046 | 3.67 | 3/12 | 4/12 | **-0.228** | 3/12 |

S21 — the split whose IS window contains the crash — has a **negative** IS→OOS Sharpe rank
correlation: the longest in-sample window selects worst. Caveat, stated plainly: the three
OOS windows have different lengths (12.7 / 9.7 / 4.7 yr) and S16 is the incumbent under
which this repo's history was produced, so "S16 wins" is not a clean out-of-sample claim
for S16 — it is sufficient to say **no alternative split is better**.

## Both KEEP paths

Evaluated per arm on the full sample: **4b passes 29/66 arms, 4a passes 26/66** (printed
per grid point in the console). This idea proposes no book, so neither path is claimed.
The one live consequence: **idea 2's n=20 on u56 is picked by rule 8 only under S16**;
S13 and S21 both pick n=40, which fails full-sample 4b on the CAGR floor. The candidate's
*justification* is split-dependent even though its realised 2022+ performance is not
(1.100 vs 1.099). Flag for Sunday review as a scoping caveat, not a reversal.

## Verdict

**KILL** — no change to rule 8's split. Moving it changes many picks but no conclusions
worth the name, and the mechanism idea 87 hypothesised runs backwards: 4b's drawdown cap is
self-scaling and gets looser, not tighter, when a crash enters the in-sample window.

Two by-products worth carrying:
- **4b's DD cap essentially never binds in-sample; the CAGR floor is the binding
  constraint.** Any future work on 4b's calibration should aim there.
- **Rule 8 selection is degenerate on any grid whose parameter has no data in the IS
  window** (crypto caps under S13). If PROTOCOL adopts idea 87's 8a pre-test, "the grid
  parameter must have live data across the IS window" belongs in it.
