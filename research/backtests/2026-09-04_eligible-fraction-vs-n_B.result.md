# Idea 46 — eligible-fraction-vs-n (lane B, 2026-09-04)

**Script:** `research/backtests/2026-09-04_eligible-fraction-vs-n_B.py`
**Console:** `2026-09-04_eligible-fraction-vs-n_B.console.txt`
**Verdict:** **KILL** the fixed-fraction rule as an improvement on fixed-n — **plus one KEEP-candidate
(4b) that fixed-n does not produce: `f = 0.85` is the only setting in the study that passes 4b on
BOTH universes.** Memo: `2026-09-04_eligible-fraction-vs-n_B.memo.md`.

## The question

Lane A's KEEP-candidate (idea 2) holds the top **20** eligible names at 3.75% each. The universe
averages 37.5 eligible names a day but the count swings from 3 to 55, so a fixed n=20 does two
different things depending on regime: in a broad market it selects the top ~40%, and in a narrow
market (E_t < 20, **11.0% of days**; E_t < 10, 3.5%) it holds *everything* eligible and quietly
de-grosses to as little as 45% invested. Should the rule pin the count or the fraction?

## Design

Scorer fixed at the candidate's own (v1 composite **without** `/sqrt(vol20)`); eligibility, 75%
gross, weekly, 10 bps, next-day execution all RULES v1's own and held fixed. Three arms, one tuned
parameter each, all 24 points reported:

| arm | rule | gross |
|---|---|---|
| **N** | top `n` eligible at `0.75/n` each — the memo's construction; cash when `E_t < n` | drifts to 69–74% |
| **NF** | top `min(n, E_t)` at `0.75/min(n, E_t)` — same count cap, gross renormalised | 75% always |
| **F** | top `ceil(f · E_t)` at `0.75/ceil(f · E_t)` — count adapts to breadth | 75% always |

`NF` exists only to split `N` into its two effects (count cap vs. cash sleeve) so the N-vs-F
comparison is not confounded. Grid: n ∈ {5,8,10,12,15,20,25,30}, f ∈ {0.15…1.00}.

**Harness sanity:** `N n=20` reproduces lane A's KEEP row exactly (12.7% / 1.093 / −18.3%, halves
1.088 / 1.103, OOS 14.4% / 1.170) and `N n=5` reproduces idea 1's `OFF EQW n=5` row (16.5% / 0.95 /
−21.6%).

## Result 1 — at matched book size, the fraction rule is not better (the idea's actual test)

Each F point paired with the fixed-count point of nearest average position count:

| comparison | F wins on Sharpe | mean ΔSharpe | F wins on OOS Sharpe | mean ΔOOS | mean ΔCAGR |
|---|---|---|---|---|---|
| F vs **N** | 2 / 8 | **−0.025** | 3 / 8 | −0.039 | +0.41% |
| F vs **NF** (gross-matched) | 3 / 8 | **−0.002** | 3 / 8 | −0.002 | +0.15% |

Against the gross-matched arm the difference is a rounding error in both directions: adapting the
count to breadth buys nothing on this universe. It costs a parameter, so on the primary universe the
answer to "top n or top X%?" is **top n** — KILL for the fraction rule as an improvement.

## Result 2 — the walk-forward agrees, and it is not close

Rule 8, parameter chosen on 2009–2016 alone, 2017–2026 untouched. Two selection rules fixed in
advance (S1 = best in-sample Sharpe; S2 = same but restricted to in-sample MaxDD ≤ 60% of SPY's
in-sample MaxDD, i.e. −13.2%):

| arm / rule | pick | OOS CAGR | OOS Sharpe | OOS MaxDD | 4b |
|---|---|---|---|---|---|
| N / S1 and S2 | **n=20** | 14.4% | **1.170** | −18.3% | pass |
| NF / S1 and S2 | n=20 | 14.5% | 1.138 | −18.3% | pass |
| F / S1 | f=0.15 | 16.7% | 0.941 | −27.8% | **fail (DD)** |
| F / S2 | **f=0.85** | 12.4% | 1.132 | −16.7% | pass |
| SPY | — | 15.5% | 0.884 | −33.7% | — |
| RULES v1 | — | 7.8% | 0.751 | −13.8% | — |

Fixed-n's pick beats fixed-fraction's on both OOS CAGR (14.4% vs 12.4%) and OOS Sharpe (1.170 vs
1.132). The plain-Sharpe rule picks f=0.15 in the F arm and blows the drawdown cap out of sample —
the fraction arm is the one that needs the 4b-aware guard rail to be safe.

## Result 3 — the cash sleeve in the memo's wording is a small positive, not a bug

`N` minus `NF` isolates de-grossing when fewer than n names are eligible. It is worth **+0.022
Sharpe at n=20 and +0.046 at n=30** (1.093 vs 1.071; 1.099 vs 1.053) for −0.9pp and −0.5pp of CAGR,
and n=30's MaxDD improves −17.5% → −16.6%. Small, one-directional at every n ≥ 8. The memo's clause
*"if fewer than 20 names are eligible, hold all eligible at 3.75% each and leave the remainder in
cash"* should be kept as a deliberate feature, not treated as an artefact of the arithmetic.

## Result 4 — the one thing the fraction rule does win: portability across universes

Lane A's honest caveat was that n=20 fails 4b's H2 on the 136-name broad universe by 0.02 (0.814 vs
SPY's 0.837) and only n=40 passes there. Re-running both arms on that list (rule 9):

| | universe.json (56) | | universe_broad.json (136) | |
|---|---|---|---|---|
| | Sharpe / MaxDD (H1/H2) | 4b | Sharpe / MaxDD (H1/H2) | 4b |
| N n=20 | 1.093 / −18.3% (1.088/1.103) | **pass** | 0.958 / −20.1% (1.125/**0.814**) | fail H2 |
| N n=40 | — (out of grid) | — | 1.004 / −19.1% (1.133/0.887) | pass |
| F f=0.85 | 1.072 / −16.7% (1.092/1.058) | **pass** | 1.024 / −18.6% (1.128/0.928) | **pass** |
| F f=1.00 | 1.051 / −15.9% (1.069/1.038) | fail CAGR (10.4% vs 10.7%) | 1.026 / −17.7% (1.143/0.918) | pass |

A count is a different rule on a 56-name list than on a 136-name one; a fraction is the same rule.
`f = 0.85` — the F arm's own pre-registered walk-forward pick, not a point chosen after the fact —
is the only parameter value in the whole study that clears all five 4b tests on both universes.
That is a robustness result, not a return result: it gives up 1.4pp of CAGR and 0.04 of OOS Sharpe
to n=20, and its CAGR margin over the 4b floor is thin (11.3% vs 10.7% primary, 11.2% vs 10.7%
broad). Note also that **idea 28's "equal-weight all eligible" (f=1.00), which missed 4b's CAGR
floor by 0.23pp on universe.json, passes 4b outright on the broad list.**

## Other numbers

* 14 of 24 points pass 4b; **0 of 24 pass 4a** (every growth book fails v1's −13.8% drawdown, as
  always).
* Matched to 12% vol: N tops out at 13.3%/yr (n=30), F at 12.9% (f=0.85), SPY 10.5%. The two arms
  are on the same curve.
* Turnover is nearly identical at matched size — n=20: 9.63x/yr, f=0.85: 9.60x/yr.
* 2022: F f=0.35 −0.8% and f=0.45 −1.5% vs N n=20's −9.0% and SPY's −18.2%. The adaptive count is a
  genuine bear-market defence (E_t averaged **16** in 2022 vs 37.5 overall) — it just does not show
  up in full-sample Sharpe because it costs return in every other year.

## Caveats

* **Survivorship.** Both universes are current-constituent lists; an f=0.85 book holds 32 of 56
  hand-picked names. Absolute CAGRs are optimistic. The N-vs-F *comparison* is far less exposed —
  both arms hold the same names.
* Costs are 10 bps flat and execution is next-day; ideas 45 (cost/lag sensitivity) is unrun for the
  fraction rule.
* The f=0.85 4b pass has ~0.6pp of CAGR margin on both universes. That is thinner than n=20's 2.0pp
  on the primary list.
