# Idea 485 — does-sd-still-survive-the-PARTIAL-t-test-once-the-control-has-DATA (lane B, 2026-09-10)

> **RECONCILIATION — this is an INDEPENDENT SAME-DAY REPLICATION.** The cloud lane claimed and ran
> idea 485 concurrently (`..._cloud.py`, `..._cloud.result.md`); neither run saw the other's code.
> **They agree on the headline to four decimals:** B136, pooled, n=20 CAND Sharpe, λ=2 — `kill`
> **0.6751 → 0.1713** and `t` **+6.19 → +9.62** across D=50 → 500 — and both membership gates
> reproduce idea 484's 3,000 committed rows at **7.105e-15**. Three things below are lane B's and
> are not in the cloud row: **(i)** the per-k cells, where the control is not diluted by pooling
> (D=500 oofR² 0.9736/0.9281/0.8969, kill 0.0217/0.0202/0.0108); **(ii)** `t50`, the same partial
> correlation restated at idea 252's own N, published beside every `t` — which turns the cloud
> run's "the two legs move in opposite directions in N" into a decided verdict (both legs clear in
> 88 of 96 cells at D=500 against 0 of 96 at D=50); **(iii)** the reason SMALL484's bar fires —
> R²(sd) is 0.003–0.012 there, so it is a NULL panel, not a killed effect. The KEEP-path counts
> differ only because the objects differ: lane B re-scored idea 484's **3,000 committed** books,
> the cloud run scored its own **120 fresh** ones. Neither run claims a KEEP, and the two
> recommendations coincide.

**ANSWERED. The queue's suspicion is CONFIRMED: idea 252's headline is a POWER statement, not a
statement about dispersion. On B136 the kill ratio collapses `0.675 → 0.171` (pooled) and
`1.011 → 0.022` (k=20) as the control's own out-of-fold R² rises `+0.21 → +0.97`, crossing idea
252's own 1/3 bar at a median D\* of 200 draws per k cell in 94 of 96 book-Sharpe cells. The bar
is not fully met at D=500 only because its second leg, `|t| < 2`, is mechanically unreachable at
N=1500 — restated at idea 252's own N=50 the same partial correlations clear BOTH legs in 88 of
96 cells against 0 of 96 at D=50. On SMALL484 there was never anything to kill: R²(sd) is
0.003–0.012 there, so its kill ratios are noise. No RULES change, no KEEP-candidate, no memo;
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py untouched.**

Script `2026-09-10_does-sd-still-survive-the-PARTIAL-t-test-once-the-control-has-DATA_B.py`;
console `.console.txt`; CSVs `.partial.csv` (4,032 grid points), `.census.csv` (14),
`.walkforward.csv` (924), `.keeppaths.csv` (16). Elapsed 380s. **No book is re-run** — every book
metric is read from idea 484's committed `.grid.csv.gz` and the membership matrix behind it is
rebuilt from the seeds and gated against that file first.

---

## What was asked

Idea 252 ran idea 83's partial test with a 136-column name-level control fitted out of fold:

| | R²(sd) | pR²(sd \| F_oof) | t | kill |
|---|---|---|---|---|
| idea 252 headline (B136, pooled 150 draws, n=20 CAND Sharpe, λ\*=2) | 0.3062 (t +8.08) | 0.2067 | **+6.19** | **0.675** |

Pre-registered bar (idea 83's, reused verbatim by 252): `sd` is KILLED iff **kill < 1/3 AND
|t| < 2**, read out of fold. Both legs were missed at every penalty, so idea 252 concluded `sd`
survives. Idea 484 then measured what that control actually knew — oofR² **+0.20** at D=50,
**+0.88** at D=500 — and filed the consequence rather than asserting it:

> *"Whether the partial test still leaves `sd` alive once the control reaches oofR² 0.88 is a
> genuinely open question and is filed to the queue rather than asserted."*

## Reproduction gates (run before any new number was read)

| gate | result |
|---|---|
| **[a] harness — INFORMATIONAL, and it FAILS** | U56/CAND20 12.6576% / 1.09219 / −18.3083% on a window that now ends **2026-09-09**. Truncated to idea 484's own last date (2026-09-04) it is 12.6597% / **1.09214** vs idea 484's published **1.09172**, and RULES v1 6.4585% / **0.66470** vs **0.66110**. `data/prices.csv` has been **RESTATED since 2026-09-09, not merely extended** (+0.00042 and +0.00360 of Sharpe on idea 484's own window). The u56 panel plays no part in this run. |
| **[b] MEMBERSHIP — BINDING** | all **3,000** draws re-drawn from `SEED_B + k` on both panels and idea 484's four membership-derived columns recomputed from the reconstructed name sets: `n_elig` **7.105e-15**, `sd` **2.220e-16**, `n_elig_IS` **3.553e-15**, `sd_IS` **8.327e-17**. **PASS** — the name sets *and* both price panels are exactly idea 484's. |
| **[c] IDEA 252's HEADLINE — BINDING** | the full 12-row published table reproduced through this run's estimator: R²(sd) **0.3062** (t **+8.08**); OOF λ=2 kill **0.6751** at t **+6.1897**; IS λ=0.5 kill **0.0002** at t **−0.1012**; idea 83's scalar kill_W **0.6200**. 7 of 7 checks PASS. |
| **[d] unplanned cross-checks** | idea 252's rule-8 cell (B136, k=20, n=20, D=50) re-derives its picks and metrics exactly — S1 draw 19 (8.37% / 1.1045 / −10.54%), S2 draw 39 (9.03% / **1.1841** / −9.43%), S5 draw 16 (5.99% / 0.9559 / −12.67%), and **S7 picks draw 39 at all six penalties**, as published. Idea 484's KEEP-path counts also reproduce exactly (B136 CAND-20 4a-v1 **1462** / 4a-v2 **12** / 4b **394** / BOTH **1**; CAND-5 285/0/30/0; SMALL484 CAND-20 11/1/0/0; CAND-5 27/0/0/0). |

## Two tuned parameters (the queue's own): draws and panel

D ∈ {50, 100, 150, 200, 300, 400, 500} per k cell × panel ∈ {B136, SMALL484}, on idea 484's
**nested** ladder (draw *d* is the same name set at every D). Everything else is idea
78/83/252/484's, imported unchanged: k ∈ {20,40,80}, n ∈ {5,20}, gate, gross 0.75, weekly,
10 bps, next-day execution, the 2009-2016 / 2017-2026 split, seeds `SEED_B + k`, 10 folds by
draw index. **The penalty is not a third tuned parameter:** the whole ladder λ ∈ {0.5, 2, 8, 32,
128, 512} is reported at every point, both schemes (IS and OOF), all four scopes (pooled, k=20,
k=40, k=80), both book sizes and all three y-columns — **4,032 grid points, all in `.partial.csv`**.

## (1) THE HEADLINE CELL — B136, pooled, n=20 CAND Sharpe, out of fold

| D | N | control oofR²(F) | **kill_F** | t(sd\|F) | **t50** (same partial r at N=50) | oofR²(sd ~ M) |
|---|---|---|---|---|---|---|
| 50 | 150 | +0.2100 | **0.6751** | +6.19 | **+3.50** | +0.268 |
| 100 | 300 | +0.5139 | 0.3749 | +6.35 | +2.53 | +0.644 |
| 150 | 450 | +0.6040 | 0.3204 | +7.04 | +2.28 | +0.734 |
| 200 | 600 | +0.6611 | 0.2553 | +7.36 | +2.07 | +0.755 |
| 300 | 900 | +0.7021 | 0.1989 | +8.04 | +1.84 | +0.784 |
| 400 | 1200 | +0.7184 | 0.1844 | +9.11 | +1.81 | +0.794 |
| **500** | **1500** | **+0.7213** | **0.1713** | **+9.62** | **+1.71** | **+0.796** |

Per k cell at D=500 (λ\*=2), where the control is not diluted by pooling: oofR²(F)
**0.9736 / 0.9281 / 0.8969** and kill **0.0217 / 0.0202 / 0.0108** for k=20/40/80 — against
1.0114 / 0.8544 / 0.8154 at D=50. The k=20 cell goes from `sd` explaining **everything the
control could not** to explaining **2% of its own univariate R²**.

`sd`'s univariate R² does not move: 0.3062 → 0.3401 on B136 across the 10× in draws. Nothing
about dispersion changed. The control learned.

## (2) THE CENSUS — 96 out-of-fold book-Sharpe points per panel per D

| panel | D | median kill | leg 1 `kill < 1/3` | leg 2 `|t| < 2` | **BOTH (idea 252's bar)** | **BOTH at N=50-equivalent** | control oofR² (med) |
|---|---|---|---|---|---|---|---|
| B136 | 50 | 0.8514 | **0 / 96** | 4 / 96 | **0 / 96** | **0 / 96** | +0.166 |
| B136 | 150 | 0.3898 | 41 / 96 | 0 / 96 | 0 / 96 | 16 / 96 | +0.490 |
| B136 | 300 | 0.1669 | 87 / 96 | 7 / 96 | 7 / 96 | 75 / 96 | +0.704 |
| **B136** | **500** | **0.0924** | **94 / 96** | 18 / 96 | **18 / 96** | **88 / 96** | **+0.758** |
| SMALL484 | 50 | 1.0005 | 10 / 96 | 94 / 96 | 10 / 96 | 10 / 96 | −0.015 |
| **SMALL484** | **500** | **0.2910** | 52 / 96 | 92 / 96 | **52 / 96** | 52 / 96 | +0.433 |

Crossover, cell by cell: the smallest D at which `kill < 1/3` is reached in **94 of 96** B136
cells and **85 of 96** SMALL484 cells, at a **median D\* of 200** on both — i.e. **4× idea 252's
own N**, and the same D\* neighbourhood at which idea 484 found the prediction ordering flip.

## (3) THE TWO LEGS ARE NOT THE SAME KIND OF NUMBER — and this is the reportable defect

`kill` is a ratio of R²s and is scale-free. A partial `t` is `r · sqrt(N − p − 2)`: it rises with
N whether or not anything about the panel changed, and N rises 10× up this ladder. So idea
83/252's bar gets **harder to clear exactly as the control gets better**, which is the opposite
of what it intends. Median over the same 96 points:

| panel | median kill (D=50 → 500) | median t (D=50 → 500) | **median t50** (D=50 → 500) |
|---|---|---|---|
| B136 | 0.8514 → **0.0924** | +4.61 → **+3.62** | +4.10 → **+1.11** |
| SMALL484 | 1.0005 → **0.2910** | +1.20 → +0.09 | +1.07 → +0.03 |

Read on the leg that can be read across D, **dispersion is dead on B136 by D=300**. Read on the
raw-t leg it "survives" at every D — and the same partial correlations, restated at idea 252's
own N, clear the bar in 88 of 96 cells. Both readings are published above; the record should stop
quoting a `|t|` bar without its N.

## (4) THE SCALAR CONTROL IS THE CONTROL GROUP, AND IT DOES NOT MOVE

Idea 83's one-scalar control `W` on the same rows, median kill over the same book-Sharpe points:

| panel | D=50 | D=100 | D=200 | D=300 | D=400 | D=500 |
|---|---|---|---|---|---|---|
| B136 kill_W | 0.6194 | 0.6553 | 0.6101 | 0.5926 | 0.5856 | **0.5960** |
| B136 kill_F (name-level) | 0.7798 | 0.4770 | 0.1601 | 0.0679 | 0.0416 | **0.0295** |

A scalar cannot learn from more draws and does not: 0.62 → 0.60 across a 10× in N (and 0.6200 at
D=50 is idea 83's published 0.620, exactly). The name-level control falls by a factor of **26**.
That contrast is the cleanest statement of what idea 252 actually measured: **not that dispersion
is structural, but that 50 draws are not enough to fit 136 name effects.** The IN-SAMPLE scheme,
idea 252's own known artefact, is unchanged by D (median kill 0.056 → 0.024) — as it must be.

## (5) RULE 8 WALK-FORWARD — selectors on 2009-2016 only, 2017-2026 read once

Mean over 7 ladder points × 3 k cells × 2 book sizes (S7 also × 6 penalties).

| panel | arm | OOS CAGR | OOS Sharpe | OOS MaxDD | beats SPY | beats live v2 |
|---|---|---|---|---|---|---|
| B136 | S0 do-nothing | 14.27% | 0.8529 | −21.71% | 21/42 | **0/42** |
| B136 | S1 IS-Sharpe argmax | 13.04% | 0.9866 | −19.41% | 31/42 | 5/42 |
| B136 | S2 max IS `sd` | 13.58% | **0.9890** | −20.37% | 28/42 | 13/42 |
| B136 | S5 `sd` \| W_IS (scalar) | 12.40% | 0.9532 | −21.18% | 25/42 | 7/42 |
| B136 | **S7 `sd` \| F_oof (name-level)** | 12.95% | **0.9584** | −20.38% | 155/252 | 69/252 |
| B136 | S6 random | 10.86% | 0.8567 | −19.90% | 21/42 | 0/42 |
| B136 | SPY / **live RULES v2** | 15.45% / 7.98% | 0.8820 / **1.1185** | −33.72% / −12.24% | | |
| SMALL484 | S1 / S2 / S5 / **S7** / S6 / S0 | 4.47 / 2.21 / 2.48 / **2.15** / 4.17 / 6.89% | 0.269 / 0.192 / 0.206 / **0.192** / 0.322 / 0.432 | ≈ −0.35 | **1/42 total** | ≤5/42 |
| SMALL484 | SPY / live RULES v2 | 15.45% / 4.55% | 0.8820 / **0.6629** | −33.72% / −12.09% | | |

**No arm on either panel beats the live book on average, and on SMALL484 exactly one row of 462
beats SPY.** Nothing is promotable — the same verdict ideas 83/252/484 reached on these rows.

**The decision-form answer to this idea's question.** At N=50 idea 252 found the name-level
residualisation changed nothing: S7 picked S2's draw at all six penalties (reproduced above,
gate [d]). Once the control has data it **does** change the pick, and changes it for the worse:

| B136, S7 vs S2 | λ=0.5 | λ=2 | λ=8 | λ=32 | λ=128 | λ=512 |
|---|---|---|---|---|---|---|
| same pick (of 42) | 17 | **20** | 24 | 23 | 24 | 19 |
| mean ΔOOS Sharpe | −0.0270 | **−0.0208** | −0.0299 | −0.0287 | −0.0336 | +0.0468 |

At the single cell idea 252 published (k=20, n=20) the ladder is explicit: **D=50** S7 = S2 =
draw 39 (OOS 1.1841); **D=500** S2 picks draw 366 (1.1386) and S7 picks draw **335 (1.0708)** at
all six penalties. Better out-of-fold *fit* still does not buy a better *choice* — idea 484's
finding, now shown on the residualisation arm as well as the prediction arm.

## (6) BOTH KEEP PATHS (PROTOCOL rule 4)

No new book form is introduced; idea 484's 3,000 committed books are re-scored and reproduce it:

| panel | book | N | 4a vs v1 (superseded) | 4a vs **live v2** | 4b vs SPY | BOTH |
|---|---|---|---|---|---|---|
| B136 | CAND-20 | 1500 | 1462 | **12** | 394 | **1** |
| B136 | CAND-5 | 1500 | 285 | 0 | 30 | 0 |
| SMALL484 | CAND-20 | 1500 | 11 | 1 | 0 | 0 |
| SMALL484 | CAND-5 | 1500 | 27 | 0 | 0 | 0 |

**13 of 3,000 clear 4a against the live book, 424 clear 4b, one clears both** — idea 484's own
single random 20-name list, already declined there. **No KEEP-candidate and no memo.**

## What the record should say now

1. **Idea 252's headline needs its D, exactly as its leg (3) needed its N.** Write it as: *"at
   50 draws per k cell — where a 136-column control explains oofR² +0.20 of the target — `sd`
   survives the name-level partial test at kill 0.675; at 300 draws it does not (kill 0.199,
   87 of 96 cells under the bar), and at 500 the k-cell kills are 0.01–0.02."* The sentence
   "the stronger control leaves *more* of dispersion, not less" is true only against a control
   that had 50 rows for 136 parameters.
2. **Idea 252's conclusion that idea 83's 62% is "structural" does not follow from these rows.**
   What is structural is that a *scalar* control cannot learn (kill_W 0.62 → 0.60 across 10× the
   draws). Idea 78's test C is not retracted by this run — no book or diagnostic changes — but
   its support on this axis is now a D=50 result with a published D=500 counter-reading.
3. **PROTOCOL/idea 83's `|t| < 2` bar is N-dependent and should not be quoted across sample
   sizes.** Either fix N when comparing, or state the bar on the scale-free leg alone. This run
   publishes `t50` beside every `t` so both readings are available.
4. **`data/prices.csv` was restated after 2026-09-09** (gate [a]): the u56 CAND-20 and RULES v1
   rows that ideas 2/73/77/83/252/484 all quote have moved by +0.0004 and +0.0036 of Sharpe on
   their own window. `prices_broad.csv` and `prices_small.csv` have **not** (gate [b] at 1e-15).

## Caveats

* **Survivorship (rule 9):** both panels are current constituents. Here that cuts *against* the
  name-additive control — name dummies fitted on names already known to have survived are the
  most favourable possible sample for a fixed-effect design. The control wins anyway, so the
  bias does not manufacture this result; it does mean the D\* is, if anything, optimistic.
* **SMALL484 has no denominator.** R²(sd) there is **0.0032–0.0122**, so `kill` is a ratio of two
  near-zero numbers and its cell values range to **83.9**. Its `|t| < 2` leg passes in 92–96 of
  96 points at *every* D, D=50 included. The honest reading of that panel is **NULL — there was
  never any dispersion effect to kill**, not that data killed one. Only B136 carries the finding.
* The comparison is of idea 252's estimator on idea 252's folds (by draw index, so training size
  is 0.9·D throughout); the ladder is a clean power curve, not a change of estimator. The
  multi-target Gram sharing is gated at [c] against the published single-target numbers.
* Pooled scopes add two unpenalised k dummies (idea 252's own choice) and are therefore a weaker
  control than the k-scoped cells; both are reported and the k cells are the sharper reading.
* Ideas 39/49's inverted gate and idea 128's shallow IS drawdown window bias every rule-8
  selector here identically, as in ideas 83/252/484.
