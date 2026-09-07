# Idea 374 — does the SECOND-worst drawdown episode bound every overlay in the record?

**cloud, 2026-09-07.** Script `2026-09-07_does-the-SECOND-worst-drawdown-episode-bound-every-overlay_cloud.py`.
Grid `..._cloud.grid.csv` (1242 rows = 54 stamped books x 23 menu points), `.classmax.csv`,
`.walkforward.csv`, `.rule8books.csv`, `.numeraire.csv`, console `..._cloud.console.txt`.

## Verdict: **ANSWERED — the premise is FALSE. Do NOT put H in PROTOCOL.**

The statistic: `H = |D1| - |D2|` in pp, the gap between the base book's worst and second-worst
under-water episode (episodes are disjoint by construction: each opens at an all-time high).
H is what an overlay can buy if it erases the worst episode entirely and touches nothing else.

**Books:** idea 350's six canonical forms (EWALL, TOP3, TOP10, TOP20, MAEW, RULESV2) x 3 panels
(U56, B136, SMALL439) x 3 rungs (0/10/25 bps) = 54. **Overlays:** 22 pre-registered points in
three classes — GLOBAL (GROSS g in {0.40..0.90}, VOLTGT t in {0.08..0.15}), SELECTIVE (BREADTH B
in {0.30,0.40,0.50} x cut {0.50,1.00}; DDCTRL T in {0.05..0.20}; HIVOL80), CADENCE (M, Q).
**0 tuned parameters** — every dial is a reported axis and all 1188 overlay points are committed.

### 1. It is not a bound

| class | points | bound violated | median dDD/H | class-MAX per book violated |
|---|---|---|---|---|
| GLOBAL | 486 | **247 (50.8%)** | 1.016 | **54/54** (median ratio 2.161, max 18.1) |
| SELECTIVE | 594 | 73 (12.3%) | 0.142 | **38/54** (median ratio 1.183, max 8.9) |
| CADENCE | 108 | 6 (5.6%) | -1.239 | 3/54 (cadence *deepens* DD: median dDD -5.66 pp) |

The queue's object is the class maximum ("the maximum achievable dMaxDD of ANY overlay"), and it
exceeds H in **92 of 108** GLOBAL+SELECTIVE books. The reason is structural and was predictable:
an overlay that scales the book on *ordinary* days moves the runner-up episode too, so the floor H
assumes away is not a floor. Violation share is stable across rungs (GLOBAL 0.506/0.512/0.506).

### 2. It does not predict — and loses to a statistic that needs no episode decomposition

Spearman(predictor, class-max dDD) across the 18 books:

| class | rung | **rho(H)** | rho(D1 = the book's own MaxDD) |
|---|---|---|---|
| GLOBAL | 0/10/25 | 0.135 / 0.077 / 0.641 | **0.992 / 0.992 / 0.990** |
| SELECTIVE | 0/10/25 | 0.451 / 0.422 / **0.932** | 0.771 / 0.723 / 0.707 |
| CADENCE | 0/10/25 | 0.307 / 0.434 / 0.771 | -0.018 / -0.018 / 0.408 |

H beats the trivial rival in exactly one of nine cells (SELECTIVE @25 bps). "How much drawdown can
an overlay buy" is answered by *how much drawdown the book has*, not by the runner-up gap.

### 3. Where saturation IS real: the breadth family, i.e. exactly where idea 350 found it

Headroom utilisation `dDD/H` by family @10 bps (median / p90):

| family | n | med dDD/H | med dDD_pp | med dCAGR_pp | med dSharpe |
|---|---|---|---|---|---|
| BREADTH | 108 | **0.000** | **0.000** | -0.773 | -0.018 |
| DDCTRL | 72 | 0.021 | 0.056 | -0.645 | -0.012 |
| HIVOL80 | 18 | 0.797 | 3.413 | -2.002 | -0.083 |
| GROSS | 90 | 0.797 | 3.865 | -1.436 | 0.000 |
| VOLTGT | 72 | 1.177 | 5.122 | -1.900 | -0.028 |

The median breadth-gated book buys **literally zero** pp of drawdown while paying 0.77 pp of CAGR.
Idea 41's depth invariance reproduces to 4.4e-16 in weight space and to 1e-6 against idea 41's own
committed grid in its return-space convention (GATE 2). So idea 350's saturation is a **property of
late, rarely-armed gates**, not a law about overlays — restating it as a record-wide bound is what
this file kills.

### 4. Rule 8 — H as the ex-ante number PROTOCOL would quote

H computed on the IS window (<= 2016-12-31) only, scored against the OOS window (2017- , equity
restarted). It holds as an ex-ante bound in **0/54 GLOBAL**, 13/54 SELECTIVE, 45/54 CADENCE, and as
a predictor of OOS class-max dDD it loses to IS |MaxDD| in **8 of 9** class x rung cells
(rho(H_IS) 0.15-0.51 vs rho(D1_IS) 0.58-0.94). Even the in-window H_OOS holds in only 16/54
SELECTIVE. **A PROTOCOL clause quoting H before an overlay is run would mislead in half the cases
and add nothing to a column the leaderboard already has.**

### 5. KEEP paths, all 1242 points

**4a 55/1242** (19/18/18 at 0/10/25 bps). **4b 122/1242** (71/37/14 at 0/10/25 bps).
By panel: U56 87, B136 35, **SMALL439 0** (idea 326 reproduced). First failing 4b bar across all
points: H1 589, CAGR 317, H2 113, DD 100, OOS 1.

SPY over the evaluation window: 15.2% / 0.889 / -33.7%, halves 0.957 / 0.834, OOS 0.882.

### 6. By-product: a 4b KEEP-candidate that survives the numeraire and rule 8

`EWALL + 12% vol target` (equal-weight all priced names at 75% gross, weekly, scaled by
`min(1, 0.12 / vol20_{t-1})`) clears 4b on **both** large-cap panels at **0, 10 and 25 bps**:

| | CAGR | Sharpe | MaxDD | H1 / H2 | OOS | turnover | gross |
|---|---|---|---|---|---|---|---|
| U56 @10 bps | 11.68% | 1.202 | -15.82% | 1.287 / 1.126 | 1.212 | 1.39x | 0.700 |
| B136 @10 bps | 11.95% | 1.205 | -14.76% | 1.344 / 1.073 | 1.183 | 1.46x | 0.692 |

Smallest 4b margin anywhere in the 6 cells: CAGR +0.79 pp (U56 @25 bps). **4a FAILS** (DD, and H2
on U56) — RULES v2 is a lower-drawdown, lower-return book, which is the case PROTOCOL 4b exists for.

It is **not** a gross-ladder point: against the static-gross ladder solved to its own realised mean
gross (match residual <= 6.6e-06) it wins Sharpe in 18/27, OOS Sharpe 18/27, MaxDD **27/27**, and
the matched ladder point clears 4b in **0/27** against the overlay's 16/27. Rule 8 selects it: the
IS<=2016 Sharpe chooser picks `VOLTGT_t0.12` in 6/6 U56+B136 EWALL cells (t=0.15 at B136 @25 bps,
also a 4b pass), beating its own base book OOS 6/6 and RULES v2 OOS 4/6, regret 0.036-0.070.
**Single-family, large-cap only:** on SMALL439 it fails 4b at every rung and loses to its own
matched-gross ladder point (dSharpe -0.083 to -0.173). Memo filed.

Chooser over the whole 23-point menu, all 54 cells: takes an overlay 54/54, beats its own base book
OOS 41/54 (median +0.0366), beats live RULES v2 OOS 17/54, mean regret 0.0631; most-picked
`CADENCE_M` 31, `VOLTGT_t0.12` 8.

## Reproduction gates
- GATE 0 cost identity `net = gross - turnover*bps/1e4` vs `engine.backtest(cost_bps=k)`: **0.00e+00**.
- GATE 1 idea 40/41 published U56 books @10 bps: TOP3 21.9%/1.04/-25.8% **PASS**, TOP5 16.5%/0.95/-21.6% **PASS**.
- GATE 1b live RULES v2 U56 @10 bps 8.66%/1.2056/-12.05% **PASS**.
- GATE 2 idea 41's committed gated cells (U56 n=3, B=0.30, return-space convention): MaxDD -0.205534 at every depth, **matches the committed grid to 1e-6** (the 0.75 multiplier is not in idea 41's grid; it prints the same number).
- GATE 3 deepest episode == MaxDD on all 18 books: **0.00e+00**.

## Caveats
Current-constituent panels (survivorship flatters every level; SMALL439 most). D1/D2 are window
statistics — which is why the IS/OOS split is run, and it is the split that kills the claim.
SMALL439 starts 2010, so its windows are shorter.
