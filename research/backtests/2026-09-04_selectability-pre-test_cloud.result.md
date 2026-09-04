# Idea 88 — selectability-pre-test-across-the-leaderboard (cloud, 2026-09-04)

**Verdict: KILL for PROTOCOL 8a *as idea 87 worded it*; a narrower replacement clause is
recommended below.** Two questions, both answered, and they point opposite ways.

Script `2026-09-04_selectability-pre-test_cloud.py` · console
`…_cloud.console.txt` · 122 arms `…_cloud.grid.csv` · 22 cells `…_cloud.cells.csv`.
11 one-parameter grids × 2 universes, **all 122 points printed**; 2 tuned parameters (the
grid parameter, and the selection rule R0/R2). Weekly, t+1, 10 bps except in the cost grids.
Harness sanity before any new number was read: idea 2's KEEP row **12.7%/1.093/−18.3%,
halves 1.088/1.103** and idea 10's `B136/EWall` **10.7%/1.027/−17.7%, halves 1.146/0.917**
reproduce exactly, and the cost-free simulator matches `engine.backtest` to **0.00e+00**.

## (1) The retrospective: nothing new is flagged

8a fires on **4 of 22 cells — the two gross grids on both universes** — which is precisely
the family idea 87 proposed it from. Every published *n*, *fraction*, *band*, *lookback*,
*cost*, *cadence* and *hysteresis* sweep passes the pre-test with IS Sharpe spreads of
0.040–0.502 against the 0.02 floor. **No walk-forward conclusion on the leaderboard outside
idea 66's gross sweeps rested on a grid with no selectable content.** The nearest to the
line is `HYST/top20` on u56 at 0.0398, and there the pick (k=2.00) is also the grid's
OOS-best. Threshold sensitivity is reported (0.005 → 0.20); the classification is unchanged
anywhere between 0.005 and 0.02, so the retrospective does not hang on idea 87's number.

## (2) The validation: the pre-test's stated rationale is refuted

8a is worded as a safeguard on *selection*. It has no power there, and the sign is wrong.

| group | n | mean SKILL (pick − grid mean) | mean REGRET (pick − grid best) | mean ρ(IS,OOS) |
|---|---|---|---|---|
| 8a PASS | 18 | **+0.039** (t +1.49) | **−0.061** | +0.492 |
| 8a FAIL | 4 | +0.000 (t +0.37) | **−0.001** | +0.196 |

Spearman(IS Sharpe spread, REGRET) over the 22 cells = **+0.256** — 8a predicts a *negative*
correlation. **The four worst selections in the run all PASS 8a:** broad `F/fraction`
−0.310, u56 `F/fraction` −0.232, u56 `CADENCE/EWall` −0.182, broad `CADENCE/EWall` −0.105.
The u56 fraction cell is the textbook case and it reproduces idea 46 exactly: rule 8 picks
**f=0.15**, OOS **16.8%/0.941/−27.8%**, while the grid's OOS-best f=0.45 reads 1.173 and the
4b-aware rule R2 is *infeasible* there. On a flagged grid, by contrast, regret is
**−0.001**: a gross grid's arms differ in OOS Sharpe by 0.001–0.004, so a noise-determined
pick costs nothing *on the objective*. **The pre-test cannot protect Sharpe, because the
grids it flags are the grids where Sharpe does not depend on the choice.**

## (3) What the flag does track: risk, not return

| group | mean OOS Sharpe spread | mean OOS MaxDD spread |
|---|---|---|
| 8a PASS | 0.241 | 4.8% |
| 8a FAIL | **0.002** | **11.3%** |

u56 `GROSS/top20`: IS Sharpe spread **0.0002** (identical to 3 dp at every g) while OOS MaxDD
runs −12.4% → −24.0%. The pick is decided in the fourth decimal and moves realised drawdown
by 11.6pp; it lands on g=0.80 on u56 and g=1.00 on broad. **That is a real defect and it is
worth a clause — but it is a risk-disclosure defect, not a selection-quality one.**

## (4) Recommended replacement wording (for the Sunday review)

> **8a. Risk-consequence disclosure.** Report every walk-forward grid's in-sample spread in
> the selection objective *and* its out-of-sample spread in MaxDD. Where the IS objective
> spread is under 0.02 Sharpe while the parameter moves MaxDD by more than 5pp, the
> parameter is a **policy dial**: record that rule 8's pick is not an estimate, and set it
> from a stated drawdown budget (idea 69). This is a disclosure, not a filter — passing it
> is **not** evidence that rule 8 selected well, and the grids that pass it are where rule
> 8's worst out-of-sample picks have occurred (idea 88).

Do **not** adopt the "only parameters that pass the pre-test are walk-forward selected"
half of idea 87's draft: on this evidence it would license exactly the selections that go
wrong and forbid only the ones that cost nothing.

## (5) By-products, all reproductions of the published record

* `N/ranked` u56: both rules pick **n=20**, OOS 14.4%/1.170/−18.3% (idea 2, confirmed);
  broad picks n=30, 4b fail on DD (ideas 44/53's universe-specificity, again).
* `CADENCE/top20`: rule 8 picks **monthly** on both lists with SKILL +0.135/+0.174 and zero
  regret, and monthly **fails 4b on drawdown on broad** (−26.1%) — idea 64's trade-off, with
  the selection rule walking straight into it.
* `HYST/top20` u56: k=2.00 picked by both rules, 12.7%/1.145/−17.2% at **3.9×/yr** turnover,
  4b PASS full-sample and OOS (idea 86, confirmed).
* Both KEEP paths on all 122 arms: **4b full-sample passes 32/61 (u56), 16/61 (broad)**;
  4b on the OOS window 43/61 and 19/61. **4a passes 3/61 on u56 — and all three are
  g=0.50/0.60 arms** that clear v1's −13.8% drawdown only by de-grossing (idea 20/66's
  lever, not an edge) and then fail 4b's CAGR floor; 46/61 pass 4a on broad, where v1 itself
  draws down −21.2% and 4a is not a bar. No new candidate is produced by this run.

**Survivorship:** both lists are current constituents, so absolute CAGRs are optimistic;
this run compares *selection rules on common grids*, so the bias falls on every arm alike.
**Rules unchanged.** PROTOCOL rule 8 unchanged; 8a recommended in the amended form above.
