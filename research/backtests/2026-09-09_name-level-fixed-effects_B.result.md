# Idea 252 — name-level-fixed-effects-instead-of-a-draw-scalar (lane B, 2026-09-09)

**ANSWERED. The queue's hypothesis is REFUTED: dispersion survives the stronger control, and
survives it leaving MORE of its univariate R² than idea 83's scalar left. Idea 83's 62% is
STRUCTURAL, not a power result about the scalar. No RULES change, no KEEP-candidate, no memo;
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py untouched.**

Script `2026-09-09_name-level-fixed-effects_B.py`; console `.console.txt`; CSVs
`.regressions.csv` (288 grid points), `.power.csv`, `.nested.csv`, `.walkforward.csv`,
`.s7_ladder.csv`. Elapsed 10s.

---

## What was asked

Idea 83 controlled a draw's winner content with ONE SCALAR (`W` = mean full-sample annualised
log return of the draw's own names, plus `W_max`) and found dispersion survived:
pooled n=20 CAND-20, R²(sd) 0.3062 (t +8.08) → partial R²(sd | W) **0.1899 (t +5.87)**,
`kill` **0.620**. Idea 83 itself listed the weakness: *"W is one scalar per draw (a
name-by-name fixed-effect design would be stronger and is not run)"*. The queue asked for that
design: regress draw Sharpe on the full **136-column membership indicator matrix** by ridge and
ask what `sd` adds to the **fitted** composition effect rather than to a summary of it.

## Reproduction gate (run before any new number was read)

| gate | result |
|---|---|
| [a] U56/CAND20 from `engine.backtest` | 12.6530% / 1.09172 / −18.3083% (published 12.7% / 1.092–1.093 / −18.3%) |
| [a] U56/RULES v1 | 6.4194% / 0.66110 / −13.8278% (published 6.5% / 0.664–0.666 / −13.8%) |
| **[b] MEMBERSHIP** — 150 sub-panels re-drawn from `SEED_B + k`, then six independent membership-derived columns of idea 83's committed `draws.csv` recomputed from the reconstructed name sets | W 8.3e-17, W_IS 8.3e-17, W_sd 9.7e-17, W_max 5.6e-17, W_cw 4.4e-16, W_cov 0.0 over 300 rows → **M is provably idea 83's own membership matrix** |
| [c] idea 83 `draws.csv` vs idea 78 `gridB.csv` | 300 rows × 17 numeric columns, max abs diff **0.000e+00**; f4b strings identical 300/300 |

The 450 books are **not** re-run: they are idea 83's committed output, gated at [c], and this run
changes no book. Every book metric below is read from that file.

## The design, and the hazard it had to defuse

`sd` is a deterministic function of membership. A 136-parameter model fitted on 50 draws can
absorb `sd` by overfitting the same y it is being tested against — and would report `sd` dead
for a reason with nothing to do with composition. So:

* **IN-SAMPLE fitted composition** is reported but is **not** a valid control.
* **THE TEST** uses **out-of-fold** fitted values (10 deterministic folds by draw index): F_oof(i)
  is draw *i*'s composition fit from a ridge estimated on the other nine folds.

Two tuned parameters, both reported at every point: ridge penalty λ ∈ {0.5, 2, 8, 32, 128, 512}
and scheme ∈ {IS, OOF}. Everything else — panel, seeds, draws, k ∈ {20,40,80}, n ∈ {5,20}, gate,
gross 0.75, weekly, 10 bps, IS/OOS split — is idea 78/83's, imported unchanged.

Effective df of the fit, trace(H), N = 50 rows against 136 name columns:

| k | λ=0.5 | λ=2 | λ=8 | λ=32 | λ=128 | λ=512 |
|---|---|---|---|---|---|---|
| 20 | 47.86 | 42.79 | 31.37 | 16.58 | 6.51 | 2.55 |
| 40 | 48.69 | 45.32 | 36.41 | 21.94 | 9.40 | 3.51 |
| 80 | 48.90 | 45.99 | 37.86 | 23.67 | 10.46 | 3.89 |

## (1) THE POWER AUDIT — the leg the scalar design could not run

A control that *spans* `sd` leaves no coefficient to test. One scalar cannot span a dispersion;
136 columns can.

| k | R²(sd ~ M) in-sample, λ=0.5 | out-of-fold |
|---|---|---|
| 20 | **0.9981** | −0.040 |
| 40 | **0.9996** | +0.409 |
| 80 | **0.9996** | +0.150 |

The in-sample name-level fit reproduces `sd` itself at R² 0.998–0.9996. **An in-sample 136-column
control cannot leave a coefficient on sd to test, at any penalty below λ≈128.** Out of fold the
same model genuinely carries only −0.04 to +0.41 of `sd`.

## (2) THE TEST — headline cell (n=20, CAND Sharpe, pooled over 150 draws)

Idea 83's scalar on these same rows: R²(sd) 0.3062 (t +8.08) → pR²(sd|W) 0.1899 (t +5.87), kill 0.620.

| scheme | λ | R²(F) | pR²(sd \| F) | t(sd \| F) | t(F \| sd) | kill |
|---|---|---|---|---|---|---|
| IS | 0.5 | 0.9701 | 0.0001 | **−0.10** | +58.17 | **0.000** |
| IS | 2 | 0.9408 | 0.0016 | +0.48 | +41.77 | 0.005 |
| IS | 8 | 0.8735 | 0.0134 | +1.41 | +29.66 | 0.044 |
| IS | 32 | 0.7151 | 0.0426 | +2.56 | +22.35 | 0.139 |
| IS | 128 | 0.4180 | 0.1067 | +4.19 | +17.76 | 0.348 |
| IS | 512 | 0.1588 | 0.2446 | +6.90 | +12.66 | 0.799 |
| **OOF** | 0.5 | −0.1884 | 0.2332 | **+6.69** | +5.74 | **0.762** |
| **OOF** | **2 (λ\*)** | 0.2100 | **0.2067** | **+6.19** | +6.86 | **0.675** |
| **OOF** | 8 | 0.3945 | 0.1836 | +5.75 | +7.78 | 0.599 |
| **OOF** | 32 | 0.3575 | 0.1880 | +5.83 | +8.01 | 0.614 |
| **OOF** | 128 | 0.1794 | 0.2467 | +6.94 | +7.20 | 0.805 |
| **OOF** | 512 | 0.0419 | 0.3349 | +8.60 | +4.40 | 1.094 |

**Pre-registered bar (idea 83's, reused verbatim): sd is KILLED iff kill < 1/3 AND |t| < 2 on the
out-of-fold scheme. Both legs are MISSED at every penalty.** At the IS-cross-validated λ\*=2 the
name-level control leaves kill **0.675** at t **+6.19**, against the scalar's 0.620 at +5.87 —
i.e. the stronger control leaves *more* of dispersion, not less.

Across all 96 book-Sharpe grid points (CAND Sharpe + EWall Sharpe, both n, 4 scopes, 6 penalties):

* **OOF: sd survives |t| > 2 in 92 of 96** (kill median 0.851, range 0.563–1.094).
* IS: 17 of 96 (kill median 0.056) — the artefact, exactly as the power audit predicts.
* Reference: idea 83's scalar survives in 15 of the same 16 cells (kill median 0.619).

The four OOF failures are one cell — n=5, k=40, CAND Sharpe — where the **univariate** t is
already only +2.18 and idea 83's scalar also fails to leave it significant (t +1.51). The
name-level control is not what kills it. On the RANKING PREMIUM, which idea 83 already showed
was near-nil, sd survives in only 5 of 48 OOF points; nothing there was contaminated because
nothing was there.

## (3) NESTED OUT-OF-FOLD PREDICTION — immune to overfit in both directions

Does adding `sd` to the name-level model improve what it predicts on draws it did not fit?

**Yes, in 72 of 72 book-Sharpe grid points** (median OOF R² gain **+0.2391**, range +0.0305 to
+0.5391). The name-level model alone predicts out of fold at R² −0.197…+0.424 (median +0.151);
`sd` **alone** predicts at R² +0.026…+0.375 (median +0.289) — a single dispersion number
out-predicts the whole 136-name additive model on this panel.

## (4) Rule 8 — the new selector is a NULL

Selectors fitted on 2009–2016 only; 2017–2026 read once. **S7 FE-RESID-DISP** = max IS `sd`
after the out-of-fold name-level fit of IS Sharpe is regressed out, penalty chosen by IS
cross-validation (λ\*=2; the whole ladder is reported).

SPY OOS 15.45% / 0.882 / −33.72%; RULES v1 on B136 OOS 5.94% / 0.576; RULES v2 on B136 8.03% /
1.106 / −12.24% (OOS 1.119); do-nothing (full B136 CAND-20) OOS 12.49% / **0.892** / −20.05%.

| selector | pick | OOS CAGR | OOS Sharpe | OOS MaxDD | regret | z in cell | 4b |
|---|---|---|---|---|---|---|---|
| S0 do-nothing | — | 12.49% | 0.8919 | −20.05% | 0 | — | H2 |
| S1 IS-Sharpe argmax | k20 d19 | 8.37% | 1.1045 | −10.54% | +0.2125 | +0.97 | CAGR |
| S2 DISPERSION | k20 d39 | 9.03% | 1.1841 | −9.43% | +0.2922 | +1.66 | CAGR |
| S3 COUNT | k80 d26 | 12.00% | 0.9526 | −19.64% | +0.0607 | +0.22 | **—** |
| S5 RESID-DISP (scalar) | k20 d16 | 5.99% | 0.9559 | −12.67% | +0.0639 | −0.31 | H2,CAGR |
| S6 WINNERNESS | k20 d12 | 6.06% | 0.7752 | −12.03% | −0.1167 | −1.86 | H2,OOS,CAGR |
| S4 random | k40 d35 | 10.30% | 0.9837 | −17.61% | +0.0918 | −0.11 | CAGR |
| **S7 FE-RESID-DISP (new)** | **k20 d39** | 9.03% | 1.1841 | −9.43% | +0.2922 | +1.66 | CAGR |

**S7 selects the SAME draw as raw dispersion S2 at all six penalties** (0.5 → 512, identical
pick, identical +0.2922). The name-level residualisation adds **no selector content**. Note the
contrast with idea 83's scalar residualisation, which *did* move the pick — and moved it to a
worse one (S5, +0.0639).

Selector-input skill (Spearman with OOS Sharpe over 150 CAND-20 draws): IS Sharpe +0.2166, IS sd
+0.1944, **IS sd|W_IS +0.2315**, **IS sd|F_oof +0.2053**, IS W_IS +0.0737, IS n_elig −0.2617.

## (5) Both KEEP paths

No new book is introduced. Restated from the committed grid (reproduces idea 83 exactly):

| book | N | 4a (vs RULES v1) | 4b |
|---|---|---|---|
| CAND20 | 150 | 146 | 40 |
| CAND5 | 150 | 32 | 2 |
| EWall | 150 | 98 | 45 |
| **all** | **450** | **276** | **87** |

**New, and it matters for how the record reads idea 78/83's 4a counts:** those counts are against
**RULES v1**, which was superseded on 2026-09-06. Restated against the **live RULES v2** (which on
B136 reads 8.03% / 1.106 / −12.24%, halves 1.229/0.984), the 300 CAND books collapse from
**4a 178/300 to 4a 3/300** (failing-bar census H2 277, H1 268, DD 263). Every published 4a count
taken before 2026-09-06 is against a much weaker book than the one now live. (EWall halves were
never written to the committed grid, so the v2 restatement covers the 300 CAND books only.)

Over the 8 rule-8 selector arms: 4a-v1 8/8, **4a-v2 2/8** (S2 and S7 — the same draw), **4b 1/8**
(S3 only, which idea 78/253 already identified as this cell's random-sub-panel base rate: 23–39%
on B136). **Nothing is promotable.**

## Answer to the queue, stated in its own words

> *"If sd still survives, the 62% is structural and idea 78's diagnostics are safe outright; if it
> dies, idea 83's answer is a power result about the scalar, not about dispersion."*

**sd survives.** The 62% is structural; idea 78's test C is safe outright on this axis. The
scalar was not the weak link.

The run adds one methodological finding the queue did not anticipate: **the design the queue
proposed is only valid fitted out of fold.** Run the obvious way — ridge the membership matrix
in-sample and residualise — it reports kill 0.000 at t −0.10 and would have retracted idea 78's
test C for a pure overfitting reason. The power audit is what separates the two readings, and it
is a leg no scalar-control design can run.

## Caveats

* **Survivorship (rule 9):** `universe_broad.json` is current constituents. As in idea 83 this is
  the premise under test, not a caveat to it — the control is built from returns of names already
  known to have survived, which under-states true winner content and makes the control
  conservative. That cuts **against** a surviving sd, not for it.
* 150 draws on one panel; k ∈ {20,40,80} against 136 names; N=50 per cell against 136 columns is
  a hard regime and the honest OOF R²(F) is sometimes negative (λ=0.5 pooled, −0.188).
* The name-level model is **additive in names**. `sd` is not, so "sd adds to the fitted
  composition effect" is precisely a statement that dispersion carries something a name-additive
  composition model does not — which is the claim under test, and is the strongest form of it
  available on 150 draws.
* Ideas 39/49's inverted gate and idea 128's shallow IS drawdown window bias every rule-8 selector
  here identically, as in idea 83.
* The λ ladder and the fold count are fixed a priori; folds are deterministic (draw index mod 10),
  so there is no fold-seed to tune.
