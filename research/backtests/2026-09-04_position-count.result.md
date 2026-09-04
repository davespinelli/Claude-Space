# Idea 2 — position-count (lane A, 2026-09-04)

Script: `2026-09-04_position-count.py` · console: `2026-09-04_position-count.console.txt`
Data: `data/prices.csv`, corrected trading-day index (verified in-script: 252/251/252 rows in
2013/2018/2024). Sample 2009-01-13 → 2026-09-03. 10 bps, next-day execution, weekly.

## Verdict

**KEEP-candidate under PROTOCOL path 4b: `OFF / EQW / n=20`** — top-20 eligible names by the v1
composite *without* `/sqrt(vol20)`, equal-weight at a constant 75% gross.
Full sample **12.7% / Sharpe 1.093 / MaxDD -18.3%**, halves **1.088 / 1.103**, and it is the
rule-8 walk-forward pick of the 4b-aware selection rule with **OOS 14.4% / 1.170 / -18.3%**
against SPY's 15.5% / 0.884 / -33.7% and RULES v1's 7.8% / 0.751 / -13.8%. It passes all five
4b tests with margin on four of them. Three qualifiers below matter and are not decorative.

5 of 30 grid points pass 4b; 2 of 30 pass 4a. All 30 are in the leaderboard.

## Design (why this is not the trivial version of the question)

RULES v1 holds the top 5 at a **fixed 15% each**, so its position count and its gross exposure
are the same dial: n=3 is a 45%-invested book, n=8 a 120% (levered) one. Ideas 1 and 40 varied n
this way and therefore varied two things at once. This script separates them:

| arm | construction | n grid |
|---|---|---|
| FIXEDW | v1's own: w = 15% each, gross = 0.15n | 2–6 (n=7 would be 105% gross → leverage, rule 2) |
| EQW | w = 0.75/n, gross constant at 75% | 2,3,4,5,6,8,10,12,15,20 |

Both run on the live v1 composite (**ON**) and with the `/sqrt(vol20)` term removed (**OFF**).
Tuned parameters: **n only**. The two arms and two scorers are structural and all four
combinations are reported in full; nothing is selected on the strength of its own result.
Sanity check that the harness is right: `ON/EQW n=5` ≡ `ON/FIXEDW n=5` ≡ RULES v1 baseline to
three decimals (0.75/5 = 0.15), and `OFF/*/n=5` reproduces idea 1's row exactly.

## What n actually does

**With gross held constant (EQW), raising n de-risks and mildly improves risk-adjusted return.**
OFF/EQW vol falls monotonically 24.3% (n=2) → 11.5% (n=20) while CAGR falls 19.5% → 12.7% and
Sharpe rises 0.857 → 1.093. MaxDD improves -26.5% → -18.3%.

**With v1's fixed 15% (FIXEDW), n is mostly a leverage dial.** Vol rises 4.6% → 12.1% (ON) and
9.7% → 20.0% (OFF) as n goes 2 → 6, and drawdown deepens in step. The Sharpe profile is nearly
identical to the EQW arm at the same n — the books are the same, scaled.

**This is the finding that governs the other 4b passes.** `OFF/FIXEDW n=3` and `n=4` also pass 4b
(13.2%/1.033/-16.2% and 16.0%/1.052/-19.5%), but their Sharpes are the same as `OFF/EQW n=3`/`n=4`
(1.037, 1.053) — they clear 4b's drawdown cap purely because 45% and 60% gross scale the -25.8%
and -23.8% drawdowns under it. That is idea 20's "gross is a pure lever" result, not a
position-count edge, and the Sunday review should not read those two rows as evidence for n=3–4.
The n=20 pass is different in kind: it is the only one obtained **at v1's own 75% gross**.

**Matched-vol diagnostic** (every EQW book scaled ex post by a constant to 12% vol — a
diagnostic, not a tradable rule): if n were only a de-risking lever these would be flat.

- ON/EQW: 5.6% (n=2) → 11.9% (n=20), monotone. Diversification substantially repairs the scaler.
- OFF/EQW: 10.0, 12.4, 12.7, 11.3, 11.1, 11.0, 11.0, 11.4, 12.5, **13.2%** for n = 2…20.
- SPY at 12% vol: 10.5%.

So position count is worth something at matched risk, but **only ~1.9pp/yr over v1's n=5, and the
OFF curve is U-shaped rather than monotone** — n=4 (12.7%) is nearly as good as n=20 (13.2%) and
the n=5–12 middle is a flat ~11%. Most of what n=20 buys under 4b is vol reduction that happens to
fit under the drawdown cap, not a large risk-adjusted improvement.

Daily-return correlations confirm n is a real change of book, not a re-labelling: OFF/EQW n=5 vs
n=20 correlates 0.869, n=2 vs n=20 0.731.

## Binding constraints across the grid (`fail4b` column)

A clean split, and it explains four earlier near-misses:

- n = 2–5 (OFF): fail on **MaxDD** — too concentrated, -21.6% to -26.5% against a -20.2% cap.
- n = 6–10 (OFF): fail on **H1 Sharpe** alone (0.892–0.918 vs SPY's 0.957). This is idea 1's
  nearest miss (`OFF n=8`) and idea 40's whole BREADTH arm.
- n = 12–20 (OFF): pass everything. **Position count is what resolves the H1 constraint that
  ideas 24, 25, 28 and 40 all failed on** — the answer to queue idea 43 is at least partly "not a
  regime failure, a concentration failure".
- The entire **ON** (scaler) arm fails 4b's CAGR floor at every n, best case 9.9% vs a 10.7%
  floor. The scaler caps the book's return no matter how it is sized. `ON/EQW n=10` is one of the
  two 4a passes (8.9%/0.905/-12.9%) and is a weak book by 4b's standard.

## Walk-forward (rule 8), parameters chosen on 2009–2016 only

Both selection rules were fixed before any OOS number was read. Ties break to smaller n.

| arm / rule | pick | IS Sharpe | IS MaxDD | OOS CAGR | OOS Sharpe | OOS MaxDD | 4b |
|---|---|---|---|---|---|---|---|
| ON/FIXEDW S1 & S2 | n=6 | 0.734 | -12.3% | 8.6% | 0.717 | -17.4% | fail H1,H2,OOS,CAGR |
| ON/EQW S1 & S2 | n=12 | 1.006 | -8.9% | 9.5% | 0.919 | -13.9% | fail CAGR |
| OFF/FIXEDW S1 & S2 | n=4 | 1.100 | -11.7% | 16.5% | 1.023 | -19.5% | **pass** |
| OFF/EQW S1 (Sharpe) | n=4 | 1.101 | -14.5% | 20.6% | 1.025 | -23.8% | fail DD |
| OFF/EQW S2 (4b-aware) | **n=20** | 0.993 | -11.7% | **14.4%** | **1.170** | **-18.3%** | **pass** |

References over the same OOS window: SPY 15.5% / 0.884 / -33.7%; RULES v1 7.8% / 0.751 / -13.8%.

The plain-Sharpe rule (S1) picks n=4 and fails on drawdown out of sample, exactly as it does in
sample. The 4b-aware rule picks n=20 in sample and it holds up untouched. Note that n=20 is *not*
the in-sample Sharpe maximum (0.993 vs n=4's 1.101) — it is chosen for its in-sample drawdown and
it improves out of sample, which is the opposite of the overfitting signature.

## Qualifiers on the KEEP

1. **The margin does not replicate on the broad universe.** Same OFF/EQW sweep on the 136-name
   `universe_broad.json` (rule 9): the *direction* replicates cleanly — Sharpe 0.698 (n=2) → 0.958
   (n=20) → 1.004 (n=40), MaxDD -40.6% → -20.1% → -19.1%. But at n=20 the broad book's H2 Sharpe
   is **0.814 against SPY's 0.837**, so the same rule would **fail 4b's H2 test** there by 0.02.
   Only n=40 (H2 0.887) passes on the broad list, and picking n=40 because it works would be
   tuning. Read this as: the n-effect is real, the specific 4b clearance at n=20 is marginal.
2. **Survivorship bias bites hardest exactly here.** `universe.json` is a current-constituent list
   of 56 names; mean 37.5 are eligible on a given day, so an n=20 book holds **over half of a
   hand-picked winner list**. The absolute 12.7%/14.4% figures are optimistic by an unknown
   amount. The ranking across n is far more trustworthy than the levels.
3. **The gain at matched risk is small** (~1.9pp/yr over n=5, non-monotone in n), and n=20's
   turnover is 9.6x/yr — the lowest in the grid, which helps, but 4b clearance rests on a
   -18.3% drawdown against a -20.2% cap, a 1.9pp margin.

## Practical notes

Turnover falls monotonically with n: 32.1x/yr at ON/EQW n=2 down to 9.6x/yr at OFF/EQW n=20, so
the diversified book is also the cheapest to run and the least cost-sensitive. 2022: OFF/EQW n=20
-9.0% vs SPY -18.2%; 2020 +15.4%; 2008-09 is outside the sample. The book is never fewer than its
target names except on the 2% of days with under 8 eligible.

## Answers to other queue items

- **Idea 43 (H1-Sharpe diagnosis)** is partly answered: H1 Sharpe below SPY's 0.957 is a
  *concentration* artefact, not a 2009–2017 regime failure. At n ≥ 12 the same book, same window,
  same signal clears it (1.088 at n=20). Idea 43 should still run the by-year decomposition, but
  it is no longer true that "4b may be unreachable on this universe".
- **Idea 28 (equal-weight ALL eligible)** now has its bracket: selecting the top 20 of ~37
  eligible beats holding all of them (which missed 4b's CAGR floor by 0.23pp on 2026-09-03). The
  momentum ranking does add return once the vol scaler is not cancelling it.
