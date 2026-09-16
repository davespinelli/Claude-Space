# Idea 999 (lane C, 2026-09-16) — is-the-TRANCHE-LIFT-a-FUNCTION-of-PHASE-BOOK-CORRELATION-and-can-it-be-PREDICTED-EX-ANTE

**ANSWERED = THE SIGN IS REAL, THE PREDICTION IS NOT. The lift's regression on phase-book
correlation is negative on the pooled grid and at every one of W, M and Q — but it explains
0.2356 of the variance (bar 0.25), an IS-only correlation reading ranks the OOS lift at
Spearman −0.3653 (bar −0.50), the IS lift itself ranks it BACKWARDS at −0.2504, and book
width adds nothing (adjusted R² −0.0180). KILL ×3.** The killer is a panel, not a coefficient:
**6 of 15 U56 cells carry a positive lift and 0 of 15 B136 cells do**, although B136 holds
three of the five *least* correlated phase families in the grid. **Nothing promoted.** No RULES
change, no PROTOCOL edit applied (rule 6); `RULES.md`, `PROTOCOL.md`, `scan.py`, `bot.py`,
`baseline.py` untouched.

**Gates 9 of 9. Hypotheses 5 of 10.** 990 s.

## The grid

2 panels {U56 56, B136 136} × 5 books {TOP10, TOP20, TOP40, EWELIG, BAND03} × gross 0.75
× 4 cadences {D 1 phase, W 5, M 21, Q 63} × 3 cost rungs {0, 10, 25} × ROTP gross-matched
rotating nulls {U56 100 draws, B136 60, nested at 25/50} = **40 cells, 240 REAL rows,
19,200 NULL rows**, 8,900 null phase-books per panel. Two tuned axes only — PREDICTOR (5 points)
and CADENCE (4 points) — **all 20 fits reported, none selected.**

`LIFT(cell) = (null OOS-4b base rate under FPORT) − (same under CANON)`, CANON = the phase-0
book PROTOCOL rule 4 reads today, FPORT = 964's tranche (mean of the P phase-books' net
streams). The null holds the book's own name COUNT at the book's own per-name weight, drawn at
random from the book's own pool: gross, width, schedule, cadence and phase family are fixed and
only *which names* changes (G5, dcount 0 / dgross 1.11e-16).

## 1. The lift table (10 bps; the full 120-row × 3-rung table is in `.lift.csv`)

| panel | book | cad | P | k | CORR_IS | CORR_FULL | base CANON | base FPORT | **LIFT** |
|---|---|---|---|---|---|---|---|---|---|
| U56 | TOP40 | Q | 63 | 34.2 | 0.9511 | 0.9398 | 0.010 | **1.000** | **+0.990** |
| U56 | TOP20 | Q | 63 | 19.2 | 0.9461 | 0.9385 | 0.070 | 0.670 | **+0.600** |
| U56 | TOP10 | Q | 63 | 9.9 | 0.9201 | 0.9116 | 0.140 | 0.700 | **+0.560** |
| U56 | TOP10 | M | 21 | 9.9 | 0.9489 | 0.9432 | 0.230 | 0.660 | **+0.430** |
| U56 | TOP20 | M | 21 | 19.2 | 0.9673 | 0.9597 | 0.800 | 1.000 | +0.200 |
| U56 | TOP40 | M | 21 | 34.2 | 0.9706 | 0.9579 | 0.990 | 1.000 | +0.010 |
| **B136** | **TOP10** | **Q** | 63 | 9.9 | **0.9245** | **0.9081** | 0.050 | 0.000 | **−0.050** |
| B136 | TOP20 | M | 21 | 19.7 | 0.9766 | 0.9621 | 0.050 | 0.000 | −0.050 |
| B136 | TOP20 | Q | 63 | 19.7 | 0.9576 | 0.9402 | 0.033 | 0.000 | −0.033 |
| … the other 21 W/M/Q cells | | | | | | | | | **0.000** |
| all 10 **D** cells | | 1 | | | n/a | n/a | 0.000 | 0.000 | **0.000** |

975-B's two published points reproduce exactly: U56/TOP20/Q lift **+0.570** there against
**+0.600** here (its 200 draws, this run's 100 — the same 100 seeds, see §5), U56/EWELIG/Q
**+0.000** both times, and the two correlations it quoted, **0.9385** and **0.9507**, land at
1.11e-16 (G3).

**H_D PASS** — at D the family has one phase, FPORT ≡ CANON, and the lift is exactly 0.000 on
all 10 cells. The boundary the question's ladder demands is reproduced, not asserted.

## 2. The fit — the sign survives, the prediction does not

| cadset | predictor | n | β₁ | R² | adj R² | Spearman | LOO RMSE | LOO mean-only |
|---|---|---|---|---|---|---|---|---|
| **POOLED W/M/Q** | CORR_IS | 30 | **−6.5606** | 0.282 | 0.256 | **−0.3653** | **0.2230** | 0.2434 |
| POOLED W/M/Q | K_IS (log) | 30 | −0.0758 | 0.057 | 0.023 | −0.1869 | 0.2417 | 0.2434 |
| POOLED W/M/Q | CORR_IS + K_IS | 30 | −7.4159 | 0.291 | **0.238** | −0.3653 | 0.2272 | 0.2434 |
| POOLED W/M/Q | CORR_FULL | 30 | **−5.4181** | **0.236** | 0.208 | −0.2987 | 0.2316 | 0.2434 |
| POOLED W/M/Q | LIFT_IS | 30 | −0.0768 | 0.007 | −0.029 | **−0.2504** | 0.2508 | 0.2434 |
| W | CORR_FULL | 10 | −0.1911 | 0.066 | −0.051 | −0.2768 | 0.0065 | 0.0062 |
| M | CORR_FULL | 10 | −7.0038 | 0.317 | 0.232 | −0.4590 | 0.1744 | 0.1560 |
| Q | CORR_FULL | 10 | −6.0870 | 0.107 | −0.005 | −0.1099 | 0.4302 | 0.3897 |
| D | any | 10 | n/a (lift ≡ 0, zero variance) | | | | | 0.0000 |

- **H_SIGN PASS.** β(CORR_FULL) = **−5.4181** pooled. The lift does point the way the question
  said: it lives where the phase-books differ.
- **H_CAD PASS.** That sign is **−1 at W, M and Q alike** — a construction fact, not a cadence
  fact.
- **H_FIT FAIL at 0.2356**, bar 0.25, and this is the *full-sample* correlation, the reading no
  practitioner is entitled to. Under a quarter of the cross-cell variance, missed by 14 bp of R².
- **H_EXANTE FAIL at −0.3653**, bar −0.50. An in-sample correlation reading ranks the OOS lift
  no better than a coin flip would rank a third of the pairs.
- **H_K FAIL at −0.0180.** Width is not a second channel: adding log k to CORR_IS raises raw R²
  by 0.009 and *lowers* adjusted R². On this grid k spans 9.9 → 91.7 and buys nothing.
- **H_DIRECT FAIL at −0.2504, and it runs BACKWARDS.** Measuring the lift itself in sample and
  projecting it forward is *worse than the grand mean* (LOO RMSE 0.2508 vs 0.2434) and at Q the
  rank correlation is **−0.5563**. W's +1.0000 is a degenerate agreement on ten lifts that are
  all within 0.017 of zero.
- **H_LOO PASS**, and it is the one honest positive: the CORR_IS fit's leave-one-out RMSE
  **0.2230** beats intercept-only **0.2434**, an **8.4%** reduction. The correlation carries
  *some* signal. It does not carry enough to choose with.

**Cost rungs (all 3 reported).** β stays negative at 0 / 10 / 25 bps (**−5.4148 / −6.5606 /
−5.7950**) and R² runs 0.175 / 0.282 / 0.199 — but the rank correlation **flips sign at 25 bps**
(−0.1681 / −0.3653 / **+0.0447**) while the mean lift decays +0.1069 / +0.0867 / +0.0526. The
one rung where the story looks best is the rung the headline is read at.

**Resolution, stated against the claim.** Nested draw ladder: max |lift(d) − lift(full)| is
**0.200 at 25 draws and 0.100 at 50**. At 100 draws a single cell's lift is worth roughly ±0.1,
so every 0.000 and every ±0.05 in §1 is a *zero to within resolution*, and only the five lifts
above +0.19 are resolved.

## 3. The counterexample that kills the correlation story

**B136/TOP10/Q holds the lowest phase-book correlation in the entire grid — 0.9081 full,
0.9245 in sample — and its lift is −0.050. U56/TOP40/Q sits 3.2 correlation points HIGHER at
0.9398 and lifts +0.990.** Same construction, same cadence, same gross, same null, same tape.

Panel-wise: **U56 6 of 15 positive lifts (max +0.990); B136 0 of 15 (max +0.000, min −0.050).**
Three of the five least-correlated cells in the grid are B136's, and all three lift zero or
negative. Whatever the lift is a function of, it is not a function of how much the phase-books
differ.

## 4. What it IS a function of — and why that is still not predictable

The tranche does exactly what 975 said it does, everywhere: it **compresses drawdown by
+0.84 pp on average (+0.91 median, positive in 23 of 30 cells)** and raises the null's median
OOS Sharpe by **+0.0494**. That compression is stable across panels. What is not stable is
whether it carries the cell **across a cap fixed outside the cell** — 0.60 × |SPY −33.72%| =
**−20.23%**:

| cell | null median OOS MaxDD, CANON → FPORT | crosses −20.23%? | DD leg | CAGR leg | lift |
|---|---|---|---|---|---|
| U56/TOP40/Q | −21.96% → **−19.75%** | **yes** | 0.050 → **1.000** | 0.010 → **1.000** | +0.990 |
| U56/TOP20/Q | −22.40% → **−20.14%** | **yes** | 0.140 → 0.670 | 0.320 → 1.000 | +0.600 |
| B136/TOP20/Q | −24.40% → −23.15% | no, 2.9 pp short | 0.067 → 0.000 | 0.300 → **1.000** | −0.033 |
| B136/TOP10/Q | −24.82% → −23.18% | no, 3.0 pp short | 0.100 → 0.000 | 0.483 → **1.000** | −0.050 |
| U56/TOP20/W | −16.09% → −13.99% | already inside | 1.000 → 1.000 | **0.000 → 0.000** | +0.000 |
| U56/BAND03/Q | −19.92% → −19.03% | already inside | 0.740 → 1.000 | **0.000 → 0.000** | +0.000 |

The lift is a **double crossing**: the tranche's ~1–3 pp of compression must land the cell on the
right side of the DD cap *while* the CAGR floor is simultaneously clearable. B136/Q starts 3 pp
too far out, so the tranche takes its CAGR leg 0.18 → 1.00 and collects **nothing**. U56/W is
already inside the cap, so the compression is wasted and the CAGR floor is pinned at 0.000.
Only U56 at M and Q sits in the band where both legs move together — which is why 6 of the 6
positive lifts are U56/M and U56/Q.

**And the distance does not rescue the prediction either (POST-HOC, not pre-registered, not
used to choose anything; it widens the PREDICTOR axis to 6 points and is reported as such).**
`GAP_IS` — the CANON null's median *in-sample* |MaxDD| minus 0.60 × |SPY's in-sample MaxDD| —
is a legal ex-ante reading, and it **does locate the cell**: Spearman(GAP_IS, GAP_OOS) =
**+0.7117**. It still does not predict the lift: **Spearman −0.2866, R² 0.0023**, and
CORR_IS + GAP_IS together reach only **R² 0.3041**. A window indicator (GAP_IS inside
−1 pp…+4 pp) splits the big lifts **3 of 18 in-window against 2 of 12 out** — no discrimination
at all. The in-sample tape tells you where the cell sits; it does not tell you that 2020 and
2022 will move it across a cap that 2008–09 set.

## 5. The REAL books — where the coin flip gains most, the rule gains nothing

**H_REAL FAIL.** At 10 bps the tranche takes the REAL books from **7 of 40 to 9 of 40** 4b
passes, flipping two cells and losing none:

- **U56/EWELIG/Q** CANON 11.52% / 1.0328 / −22.21% (binds `L4_DD`) → FPORT **12.29% / 1.1201 /
  −20.14%** (binds nothing). This is 964's published subject, reproduced to the digit.
- **B136/EWELIG/W** CANON 10.49% / 1.0107 / −17.69% (binds `L5_CAGR`) → FPORT **10.79% /
  1.0365 / −17.27%**.

Neither is a top-5-lift cell. **U56/TOP40/Q, where the tranche takes 1 of 100 coin flips to 100
of 100, leaves the REAL book failing 4b under both estimators** — CANON 10.33% / 0.9408 /
−26.26%, FPORT 11.74% / 1.1132 / **−22.16%**, still 1.93 pp outside the cap. The lift is a
property of the **random basket**, not of the rule that shares its width and schedule.

**OOS 4a: 3 of 80 rows**, all of them `BAND03` at gross 0.75 — the live book compared with
itself on a second panel. No book on this grid beats the live rules.

## 6. PROTOCOL rule 8 — the ex-ante predictor picks, and loses

(book, cadence) chosen inside each panel on **2009–2016 alone**, OOS read once, 10 bps:

| chooser | panel | pick | OOS CAGR | OOS Sharpe | OOS MaxDD | 4b | 4a | binds |
|---|---|---|---|---|---|---|---|---|
| **C_CORR_IS** (the ex-ante predictor) | U56 | TOP10 / Q | 17.76% | 1.0869 | −24.01% | — | — | `L4_DD` |
| **C_CORR_IS** | B136 | TOP10 / Q | 16.62% | 0.9215 | −26.70% | — | — | `L4_DD` |
| C_LIFT_IS | U56 | EWELIG / M | 12.35% | **1.1707** | −17.63% | **PASS** | — | — |
| C_LIFT_IS | B136 | TOP10 / Q | 16.62% | 0.9215 | −26.70% | — | — | `L4_DD` |
| C_K_IS | U56 | TOP10 / M | 17.15% | 1.1015 | −21.44% | — | — | `L4_DD` |
| C_K_IS | B136 | TOP10 / Q | 16.62% | 0.9215 | −26.70% | — | — | `L4_DD` |
| C_IS4B | U56 | EWELIG / Q | 12.29% | **1.1201** | −20.14% | **PASS** | — | — |
| C_IS4B | B136 | TOP20 / M | 13.81% | 0.9318 | −23.85% | — | — | `L4_DD` |
| **SPY OOS** | | | **15.21%** | **0.8713** | **−33.72%** | | | |
| **RULES v2 (live), U56 OOS** | | | **9.45%** | **1.2765** | **−12.05%** | | | 1.77 turns/yr |

**H_RULE8 PASS on a technicality worth stating plainly: 2 of 8, OOS 4a 0 of 8 — and the
ex-ante correlation chooser is 0 of 2.** Both passes are `EWELIG` on U56, i.e. **964's already
published tranche**, reached from two directions (M via the IS lift, Q via the IS-4b bar). The
predictor this idea was asked to build picks `TOP10/Q` on both panels and busts the drawdown cap
by 3.8 and 6.5 pp. Nothing new was found; the one thing the ladder can reach was already in the
record.

## 7. Gates — 9 of 9

| gate | what | got | bar |
|---|---|---|---|
| G0 | `offset_mask(·,per,0)` == `engine.rebalance_mask` on W/M/Q | 0 rows | 0 |
| G1 | fast `Ctx` == `engine.backtest`, returns and turnover | 2.08e-17 / 4.44e-16 | 1e-12 / 1e-10 |
| G2 | `band_book(0.03, 0.75)` == `baseline.rules_v2_weights` | 0.00e+00 | 0.0 |
| **G3** | **CROSS-RUN: 975-B's committed `phasecorr.csv` REAL column** | **12 of 12 cells, 1.11e-16** | 1e-10 |
| **G4** | **CROSS-RUN: 975-B's committed `nulls.csv.gz`, draw by draw** | **5,760 shared rows, 2.22e-16** | 1e-10 |
| G5 | GROSS MATCH: null count and gross == book's, row by row | dcount 0, dgross 1.11e-16 | 0 / 1e-12 |
| G6 | NESTING: 25/50-draw rates are the first seeds of the grid | nested by construction | 0.0 |
| G7 | TRANCHE IDENTITY: FPORT over a 1-phase family == CANON | 0.00e+00 | 1e-12 |
| G8 | determinism: a rebuilt cell reproduces its own stream | 0.00e+00 | 0.0 |

G4 is the strong one: **5,760 of 975-B's committed per-draw ROTP null rows replay at 2.22e-16**
across six metrics, on the same seeds, the same books and the same two cadences. This run nests
the record exactly; where it differs from 975-B it differs because the grid is wider, not
because the construction moved.

## 8. Verdict

**KILL ×3.** KILL for *"mean pairwise phase-book correlation predicts the tranche lift"* (R²
0.2356 full-sample, below its own 0.25 bar, and falsified outright by B136 carrying the grid's
lowest correlation at zero lift). KILL for *"an IS-only correlation reading predicts the OOS
lift"* (Spearman −0.3653 against a −0.50 bar; the chooser built on it is 0 of 2 on rule 8).
KILL for *"book width is the second channel"* (adjusted R² −0.0180 over k = 9.9 → 91.7).
**PARK** the direction: the sign is negative, pooled and at W, M and Q separately, and the fit
does beat the grand mean out of sample by 8.4% of RMSE — enough to report, not enough to size.

**KEEP as a PROTOCOL rule 4 reporting clause (proposed, NOT applied — rule 6):** see
`2026-09-16_tranche-lift-clause_C.memo.md`.

## Survivorship (PROTOCOL rule 9)

U56 and B136 are **current-constituent** lists, so every CAGR and drawdown LEVEL above is
optimistic, and a coin flip drawn from a survivor panel is a better book than one drawn in real
time — every NULL base rate here is an **UPPER bound** on the real-time one. The measured object,
the LIFT, is a DIFFERENCE between two estimators of the *same draw* on the *same tape*, so the
level bias largely cancels. What does not cancel is that a survivor panel compresses cross-name
dispersion, which **raises** phase-book correlation and pushes every cell toward the no-lift end
of the predictor — i.e. the bias works **against** H_EXANTE's chance of passing, not for it. The
rule-8 levels are read against SPY, which is not survivorship-inflated.
