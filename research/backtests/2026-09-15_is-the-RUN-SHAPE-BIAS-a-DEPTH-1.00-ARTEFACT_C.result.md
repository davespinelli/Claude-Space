# Idea 883 (lane C, 2026-09-15) — is the RUN-SHAPE BIAS a DEPTH-1.00 ARTEFACT across the whole placebo record?

**ANSWERED — NO. It is a DEEP-DE-GROSSING effect that turns on between depth 0.50 and 0.75, and it
is SUPER-LINEAR in depth, not proportional. KILL for capital (no book, nothing to promote); the
queue's premise is refuted and the record's headline is re-stated as a depth-conditional number.**

Script `2026-09-15_is-the-RUN-SHAPE-BIAS-a-DEPTH-1.00-ARTEFACT_C.py`, 150 s, deterministic,
committed caches only. 3 panels × 768 arms = **2,304 arms** × 5 nulls × 20 seeds × 3 cost rungs =
**691,200 priced placebo cells**, every grid point written to `.excess.csv` / `.gap.csv`.
2 tuned parameters, both named by the queue: **claim set** (NARROW / BROAD) and **depth grid**
{0.25, 0.50, 0.75, 1.00}.

## Gates (printed before any hypothesis was read)
| gate | reading | bar | verdict |
|---|---|---|---|
| G1 never-firing multiplier ≡ ungated book | 0.000e+00 | 1e-12 | PASS |
| G6 fast Sharpe ≡ `engine.metrics()['Sharpe']` | 0.000e+00 | 1e-10 | PASS |
| G2 rate match, every null's mean multiplier ≡ the real arm's | 0.000e+00 | 1e-12 | PASS |
| G4 determinism (every placebo recomputed from its md5 seed) | 0.000e+00 | 0 | PASS |
| G5 k and m preserved by both switch-matched nulls | 0 violations in 92,160 real cells | 0 | PASS |
| G7 BLOCK2 calibration (its true gap is ZERO by construction) | −0.00015, sign z +0.25 | ≤0.0010, \|z\|<2 | PASS |
| **G3 cross-run reproduction of idea 881** | depth 1.00 **−0.00590 (z +3.67)**, depth 0.50 **−0.00184 (z +1.75)**, dispersion **5.87×** | within 0.0020 of 881's published −0.00590 / −0.00184 / 5.87× | **PASS at 0.00000 — identical seed stream, so this is an identity, not an agreement** |
| G8 all 8 memo-backed shelf books reproduce their committed triple | 8 of 8 | 1.00 pp / 0.10 / 2.00 pp | PASS |

The G7 band is itself **depth-free** (BLOCK2 at d = 0.25 / 0.50 / 0.75 / 1.00 reads +0.00009 /
+0.00027 / −0.00084 / −0.00046, every \|z\| ≤ 0.58), which is what makes the law below readable.

## (A) The census — TUNED PARAMETER 1
| claim set | n files | POOLED over depth incl. 1.00 | FULL_ONLY | PARTIAL_ONLY | NO_DEPTH | carries d=1.00 |
|---|---|---|---|---|---|---|
| NARROW (files that BUILD a null) | 14 | 13 (92.9%) | 0 | 0 | 1 | **13 of 14 (92.9%)** |
| BROAD (+ null vocabulary and a depth axis) | 57 | 16 (28.1%) | 0 | 0 | 41 | 16 of 57 (28.1%) |

**H_CENSUS CONFIRMED.** Not one committed placebo-differenced number in the record was priced at
partial depth alone; every file that prices depth at all carries the 1.00 rung inside a pooled
headline. So the record's published run-shape numbers are depth-1.00-inclusive averages by
construction — which is precisely why the queue's question needed asking, and why the answer below
matters even though it refutes the premise.

## (B) The depth law — H_LAW **REFUTED**, H_ART **REFUTED**
SM_DOM minus BLOCK, signed pooled median, all rungs reported:

| depth | 0 bps | 10 bps | 25 bps | z@10 | gap/d | vs the BLOCK2 band |
|---|---|---|---|---|---|---|
| 0.25 | −0.00081 | **−0.00073** | −0.00052 | +1.33 | −0.00291 | **INSIDE (unresolvable)** |
| 0.50 | −0.00170 | **−0.00184** | −0.00062 | +1.75 | −0.00368 | magnitude outside, sign-test **not** significant |
| 0.75 | −0.00536 | **−0.00519** | −0.00484 | **+3.83** | −0.00693 | OUTSIDE (resolved) |
| 1.00 | −0.00679 | **−0.00590** | −0.00678 | +3.67 | −0.00590 | OUTSIDE (resolved) |

* **H_LAW REFUTED.** gap/d spans −0.00291 → −0.00693, a **42.7%** deviation from its mean against a
  25% bar, and the through-origin fit `gap(d) = −0.00581·d` explains **R² 0.876** against a 0.90
  bar. The bias is **super-linear**: essentially absent at a quarter de-gross, ~88% of its full size
  already at three quarters. A (1−d) multiplier scaling returns on firing days would give a
  proportional law; this is not that, so the mechanism is not a simple return-scaling effect.
* **H_ART REFUTED — the queue's title is answered NO.** Depth 0.75 carries −0.00519 at a **larger**
  sign-test statistic than depth 1.00 (z +3.83 vs +3.67). The defect is not an artefact of the
  1.00 rung; it is an artefact of the **deep** rungs, and it is only unresolvable at d ≤ 0.25.
* **H_COSTINV CONFIRMED** (worst range over 0/10/25 bps = 0.00122 < 0.005; switch ratio 1.00× at
  every depth). Contrast RAND, whose switches are unmatched at 13.2×: −0.00210 / +0.23284 / +0.59096.
* Honest miss to report: SM_UNIF, 875's clean control, reads **+0.00111 (z −2.33)** at d = 0.25 —
  marginally outside the band in the *opposite* direction, one cell of 16 (4 nulls × 4 depths).
  Read as multiple-comparison noise, but published rather than absorbed.
* Placebo annualised vol falls 0.1227 → 0.1172 across the depth ladder, as any de-grossing book's
  must; 881's "flat vol ⇒ mean-return effect" reading holds *across nulls at a depth*, not across
  depths, and this run does not extend it.

## The exposure re-read at each book's own depth — H_BOOK **REFUTED as declared**
`depth_own` is measured from each book's own exposure path (1 − mean gross on its de-grossed days ÷
its 95th-percentile gross), not assumed:

| book | depth_own | days de-grossed | measured gap at its own rung | fit-predicted (pre-registered) |
|---|---|---|---|---|
| u56-marsrespread-gross075 | 0.000 | 0.0% | **0 (never de-grosses)** | −0.00000 |
| u56-quantile50-respread-M | 0.000 | 0.0% | **0** | −0.00000 |
| b136-r620-gross065-W | 0.000 | 0.0% | **0** | −0.00000 |
| u56-top20-band-m20 | 0.243 | 18.8% | **−0.00073 (INSIDE band)** | −0.00141 |
| u56-v2band-gross100 | 0.245 | 89.1% | **−0.00073 (INSIDE band)** | −0.00143 |
| u56-band008-gross100 | 0.257 | 90.1% | **−0.00073 (INSIDE band)** | −0.00150 |
| b136-qroll-q012-w1008-d050-g100 | 0.500 | 9.5% | −0.00184 (z +1.75) | −0.00291 |
| u56-k8-qroll-q017-w1008-d100-g100 | 1.000 | 12.2% | **−0.00590 (resolved)** | −0.00581 |

**H_BOOK is REFUTED on its pre-registered form** (3 of 8 below resolution, majority needed) — and
the pre-registered form used the through-origin fit, which H_LAW just refuted. Read on the
**measured** rung instead, **6 of 8 shelf books sit at or inside the record's own resolution** and
only **1 of 8 — `u56-k8-qroll…d100-g100` — de-grosses at the depth the whole placebo record priced
its run-shape number at.** Both readings are published; the fit overstates the bias at shallow depth
by ~2×, which is the super-linearity above seen from the other side.

## Rule 8 (a) — the statistic: **H_WF REFUTED**
ρ(IS signed gap, OOS signed gap) ≥ +0.30 in **0 of 8 families for SM_DOM at every one of the four
depths**, while RAND — an effect 40× larger — walks forward **8 of 8 at every depth**. So the
per-arm ranking of the run-shape gap is noise-dominated at 20 seeds even where its pooled sign is
resolved. The pooled level does persist in sign and order of magnitude (d = 1.00: IS median
−0.02493 → OOS −0.02902; d = 0.25: −0.00074 → −0.00369), so the defect is real and non-stationary
in size, not a window artefact — but nothing about it is estimable arm-by-arm ex ante.

## Rule 8 (b) — the books: IS-only selector (max 2009–2016 Sharpe per panel), OOS read once
| panel | IS-pick | FULL CAGR / Sharpe / MaxDD | halves | OOS CAGR / Sharpe / MaxDD | 4a | 4b |
|---|---|---|---|---|---|---|
| B136 | CORR-HI q0.12 w252 **d1.0** W g1.0 | 13.91% / 1.166 / −16.63% | 1.289 / 1.037 | **12.97% / 1.154 / −16.63%** | fail | **PASS** |
| U56 | CORR-HI q0.07 w1008 **d1.0** W g1.0 | 12.73% / 1.034 / −22.93% | 1.160 / 0.915 | 12.41% / 1.016 / −22.93% | fail | fail (DD −22.93% vs −20.23% cap) |
| SMALL | VOL20-LO q0.17 w252 d1.0 D g1.0 | 5.04% / 0.404 / −48.52% | 0.736 / 0.201 | 2.00% / 0.203 / −48.52% | fail | fail |

Comparands: **SPY** U56 15.13% / 0.885 / −33.72% (OOS 15.27% / 0.874), B136 15.16% / 0.886 (OOS
15.33% / 0.877); **RULES v2 (live)** U56 8.64% / 1.208 / −11.90% (OOS 9.49% / 1.286), B136 7.98% /
1.101 / −12.18% (OOS 7.88% / 1.108). Unselected base rates over 2,304 arms: **4a 0 (0.0%)**;
4b U56 137 (17.8%), B136 93 (12.1%), SMALL 0 (0.0%).

**No memo, nothing proposed for promotion.** All three picks and all three of their metrics
reproduce the books committed earlier today by ideas 882/885 to the printed digit (B136
12.97% / 1.154 / −16.63%, U56 12.41% / 1.016 / −22.93%, SMALL 2.00% / 0.203 / −48.52%), so the B136
4b pass is an **already-committed book seen again inside a wider depth grid**, not a new candidate —
and at a 12.1% unselected base rate on that panel it would not be one anyway.

## What this changes in the record
1. The queue's premise is wrong in the direction that matters: the run-shape defect is **not** a
   depth-1.00 artefact. Any PROTOCOL clause naming the longest run is needed at **d ≥ 0.75**, not
   only at full de-grossing.
2. The published −0.0046 headline (875) and −0.0059 / −0.0018 pair (881) are correct where they were
   measured and **are not transportable to a book at a different depth**: the law between them is
   super-linear, so interpolation understates and extrapolation from a linear fit overstates.
3. For the 8 memo-backed shelf books, the exposure is **zero for 3 (no de-grossing at all) and
   inside this record's own seed-noise band for 3 more**. One book — the d=1.00 QROLL live-leg —
   carries the full −0.0059, and it is the only one that does.

**SURVIVORSHIP:** U56 / B136 are current-constituent lists; SMALL is the sub-$2B panel with the 52
`max_1d_move ≥ 1.0` tickers dropped and is current constituents only, so every CAGR **level** above
is optimistic. The run's headline is a **difference between two nulls on the same arm**, which is
far less exposed to that bias than any level.

**PROTOCOL:** 10 bps per unit turnover (0 and 25 also reported), next-day fills, no shorting, no
leverage. Modifies nothing outside its own outputs; proposes no RULES change and applies none.
