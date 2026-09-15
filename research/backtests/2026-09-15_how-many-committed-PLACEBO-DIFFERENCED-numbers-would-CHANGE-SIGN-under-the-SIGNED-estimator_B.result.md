# Idea 880 — how many committed PLACEBO-DIFFERENCED numbers would CHANGE SIGN under the SIGNED estimator?
**lane B, 2026-09-15.** Script `2026-09-15_how-many-committed-PLACEBO-DIFFERENCED-numbers-would-CHANGE-SIGN-under-the-SIGNED-estimator_B.py`.
1,152 real gate arms (U56 / B136 / SMALL-664, 384 each) × 6 nulls × 40 md5 seeds × 3 cost rungs
= **829,440 placebo cells**, re-read under **4 estimators × 4 seed budgets**. Deterministic; two
independent re-runs agree to the printed digit on every number below.

## ANSWER — **ALL OF THEM, AND THE FLIP IS NOT A SIGN, IT IS A DIFFERENT QUANTITY. KILL for capital.**

The queue's question presumes the two estimators measure the same thing up to a sign. They do not.
On the **13 (rung × budget × null) cells where BOTH estimators resolve at |z| ≥ 2, the two disagree
on the sign in 13 — 100.0%**; across all 48 cells the sign disagrees in **40 (83.3%)**.

Two distinct failure modes, and both are in the record:

1. **Large effects: E1 has no sign to report.** `RAND` reads **+0.2626** under E1 (the record's
   `median_a |g_a|`) and **−0.3150** under E3 (the signed pooled gap). E1 is non-negative by
   construction, so it can never carry the direction of an effect it does resolve. Definitional,
   and it costs the record every directional placebo claim it published in the absolute form.
2. **Small effects: E1 points the WRONG WAY.** `SM_DOM` — the one null with a real, walk-forward
   effect — reads E1 **0.02092** against the true-zero calibrator BLOCK2's **0.02317**, i.e. a
   difference of **−0.00225 (z −2.22, RESOLVED)**, while E3 reads **+0.00447 (z +2.43, RESOLVED)**.
   The record's estimator resolves SM_DOM as *quieter than a null with no effect at all*. It does
   so at 12 of 12 (rung × budget) cells, sign-stably.

## THE MECHANISM, MEASURED NOT ASSUMED — E1 is a DISPERSION read, not an EFFECT read

`E1² = noise²/S + effect²`, fitted on the four-point budget ladder at 10 bps:

| null | E1 @S=5 | @S=10 | @S=20 | @S=40 | log-log slope (pure noise = −0.500) | E1 asymptote (S→∞) | \|E3\| |
|---|---|---|---|---|---|---|---|
| RAND | 0.27543 | 0.27201 | 0.27485 | 0.27377 | **−0.001** | **0.27340** | 0.31531 |
| BLOCK2 (true zero) | 0.03307 | 0.02317 | 0.01676 | 0.01120 | **−0.515** | **0.00000** | 0.00035 |
| SM_UNIF | 0.03312 | 0.02327 | 0.01490 | 0.01105 | **−0.539** | **0.00000** | 0.00021 |
| SM_DOM | 0.02839 | 0.02092 | 0.01490 | 0.01064 | **−0.474** | **0.00499** | 0.00403 |
| SM_SPLIT2 | 0.02990 | 0.02263 | 0.01630 | 0.01130 | **−0.469** | **0.00663** | 0.00238 |

At the record's own 10-seed budget E1 reads **0.0209** for SM_DOM, of which the fitted effect
content is **0.0050 (24%)** and the remaining **76% is the seed noise E1 was supposed to be net
of** — which reproduces idea 875's "87–95% seed noise" and sharpens it into a law: **E1's magnitude
falls as 1/√S at slope −0.47 to −0.54, so it is dominated by the very quantity a placebo difference
exists to remove.** E3's whole bootstrap standard error at S=40 is **0.00056**, i.e. **E1's
zero-effect floor (0.0112) is 20× the signed estimator's entire standard error.**

**H_ORDER FAILS as pre-registered, and informatively.** It predicted E1 would be blind at every
budget. E1 is not blind — it resolves SM_DOM at S = 5, 10 and 20 (|z| 2.68 / 2.22 / 2.74) — it is
**inverted**. "The estimator hides the effect" is the wrong diagnosis; the estimator *misreports*
it.

**H_BUDGET FAILS, and in the opposite direction to the rival it encodes.** E1's |z| on SM_DOM is
**not monotone increasing in S** — it runs 2.68 → 2.22 → 2.74 → **1.25** at 10 bps. More seeds make
the record's estimator *less* resolving, because more seeds shrink the per-arm noise that is
E1's actual content. No seed budget fixes E1; a larger one makes it worse.

## GATES — 5 PASS, 2 FAIL, both causes named

| gate | result |
|---|---|
| G1 never-firing multiplier ≡ ungated book | **PASS** max\|d\| 0.000e+00 (bar 1e-12) |
| G2 rate match, every null vs its real arm | **PASS** 0.000e+00 (bar 1e-12) |
| G2b switch-matched nulls preserve *k* and *m* | **PASS** 0 violations in 900 draws |
| G3 fast Sharpe ≡ `engine.metrics()['Sharpe']` | **PASS** 0.000e+00 (bar 1e-10) |
| G4 determinism from md5 seed | **PASS** max\|d\| 0.000e+00 (bar 0) |
| G5 BLOCK2 calibration (E3, S=40, 10bps) | **PASS** +0.00035, z +0.54 |
| G6 half-normal identity E1/sd = 0.6745 | **FAIL** 0.01120/0.02160 = **0.5183**, \|d\| 0.156 (bar 0.12) |
| G7 reproduction of 881's SM_DOM −0.00348 | **FAIL as printed** +0.00397, \|d\| 0.00745 (bar 0.0020) |

**G6's cause (diagnostic, bar not moved):** the per-arm gap is **not Gaussian — excess kurtosis
+1.75** — so median\|g\|/sd is 0.518, not the Gaussian 0.674. The conclusion the gate was protecting
is unaffected: the floor is **0.0112 > 0 whatever the shape, and it does not shrink with the number
of arms.**

**G7's cause, and it is this run's subject.** Ideas 875 and 881 difference `EXCESS = real − placebo`,
so their published statistic is `(BLOCK − null)` — the **negative** of this run's `(null − BLOCK)`.
Under 881's own convention this run reads **−0.00397 vs 881's −0.00348, |d| 0.00049, inside the
0.0020 bar (G7b PASS)**. *Neither committed script's prose names that convention.* A run that
compared the two published numbers as printed would have concluded the effect had reversed.

## CENSUS (param 1: claim set) — the record's placebo numbers mostly name NO estimator at all

876 committed placebo-bearing number-carrying lines across 132 files:

| form | ALL (876) | NAMED subset (304 lines naming a null kind) |
|---|---|---|
| ABS (abs-before-pool) | 39 (4.5%) | 14 (4.6%) |
| SIGNED | 61 (7.0%) | 29 (9.5%) |
| BOTH | 2 (0.2%) | 2 (0.7%) |
| **UNSTATED** | **774 (88.4%)** | **259 (85.2%)** |

**H_CENSUS FAILS (4.5% vs its ≥50% bar)** — but not because the record prefers the signed form.
**88.4% of committed placebo-differenced numbers state no estimator form at all**, so they cannot
be re-priced from prose; only 102 lines state a form, and 39 of those 102 (38.2%) are absolute.
This is the same unadjudicable mass idea 876 found for null *kind* (67.1%), now measured for
estimator *form*, and it is worse: 88.4%. Combined with G7's unnamed sign convention, **a committed
placebo-differenced number in this record typically names neither its null kind, nor its estimator,
nor its sign convention.**

## H_CONSERV — REFUTED. Re-pricing can RETRACT, not only add

Over 48 (rung × S × null) cells: E1-unresolved → E3-**RESOLVED** in 9 (18.8%); E3 **retracts** an E1
resolution in **8**; agree in 31. Per null, cells resolved of 12: RAND E1 9 / E3 10; SM_UNIF E1 **3**
/ E3 **0**; SM_DOM E1 8 / E3 9; SM_SPLIT2 E1 1 / E3 3. `SM_UNIF` is the clean control with no
effect, and **E1 resolves it in 3 of 12 cells while E3 resolves it in 0** — E1 manufactures
resolutions on a null that has nothing to find.

## H_SIGN — FAILS (2 of 4 nulls). Portability is effect-size-dependent

E3's sign agrees **9/9** panel × rung cells for SM_DOM (+0.0056…+0.0009) and **9/9** for SM_SPLIT2,
but only **6/9** for RAND (whose gap changes sign between 0 bps and 10/25 bps — a cost story, as
expected for the one null with unmatched switch counts) and **6/9** for SM_UNIF (whose true gap is
zero, so its sign is noise). The bar as written required all four; the informative reading is that
**the signed estimator is sign-portable exactly where there is an effect to be portable about.**

## RULE 8 (a) THE ESTIMATOR — IS ≤2016 fitted, OOS 2017+ read once

| null | pooled IS | pooled OOS | ρ(IS,OOS) over arms | family sign agreement |
|---|---|---|---|---|
| RAND | −0.34042 | −0.30518 | +0.940 | 8/8 |
| SM_UNIF | −0.00344 | +0.00012 | −0.002 | 3/8 |
| **SM_DOM** | **+0.01559** | **+0.02015** | +0.141 | **8/8** |
| SM_SPLIT2 | +0.00682 | +0.01276 | +0.043 | 8/8 |

**H_WF PASSES 8/8** — SM_DOM's signed defect walks forward on every family, and SM_UNIF's
non-effect does not (3/8, i.e. a coin). The defect the signed estimator resolves is a real,
out-of-sample property of the construction, not a window artefact.

## RULE 8 (b) THE BOOKS — IS-only selector (highest 2009–2016 Sharpe per panel), OOS read once

| panel | pick | FULL CAGR / Sharpe / MaxDD | halves | OOS CAGR / Sharpe / MaxDD | 4a | 4b full | 4b OOS |
|---|---|---|---|---|---|---|---|
| U56 | CORR-HI q0.07 w1008 d1.00 W g1.00 | 12.73% / 1.034 / −22.93% | 1.160/0.915 | 12.41% / 1.016 / −22.93% | FAIL | FAIL | FAIL |
| B136 | CORR-HI q0.12 w252 d1.00 W g1.00 | 13.91% / 1.166 / −16.63% | 1.289/1.037 | **12.97% / 1.154 / −16.63%** | FAIL | PASS | **PASS** |
| SMALL | VOL20-LO q0.17 w252 d1.00 D g1.00 | 5.04% / 0.404 / −48.52% | 0.736/0.201 | 2.00% / 0.203 / −48.52% | FAIL | FAIL | FAIL |

Comparands: SPY full 15.13% / 0.885 / −33.72%, OOS 15.27% / 0.874 / −33.72% (U56 calendar);
RULES v2 (live) full 8.64% / 1.208 / −11.90%, OOS 9.49% / 1.286 / −11.90%.
Unselected base rates over 384 arms per panel: **4a 0 / 0 / 0**; 4b full 61 / 44 / 0; 4b OOS
131 / 54 / 0. **4a is 0 of 1,152 everywhere in this run.**

**The one 4b OOS pass is not new and is DECLINED for the fourth time.** B136 CORR-HI q0.12 w252
d1.00 W g1.00 is idea 875's by-product, re-selected identically by 881, 882 and this run because
all four use the same declared IS-only selector on the same arm grid. It is not this idea's object,
it is the best of a large unselected 4b population (54 of 384 on this panel alone), and 4a is 0.
See `2026-09-15_CORR-HI-U56-BYPRODUCT_MEMO.md` for the standing by-product memo on the sibling U56
book. **No memo written, no book promoted, no KEEP claimed.**

## VERDICT

**ANSWERED = EVERY RESOLVED NUMBER CHANGES SIGN, BECAUSE E1 AND E3 ARE NOT THE SAME QUANTITY.
KILL for capital.** H_ORDER, H_BUDGET, H_CONSERV, H_CENSUS and H_SIGN all print FAIL on their own
pre-registered bars; H_WF passes 8/8. No RULES change, no PROTOCOL edit, no book promoted, no KEEP
claimed; `RULES.md`, `PROTOCOL.md`, `scan.py`, `bot.py` and `baseline.py` untouched (rule 6).

## PROTOCOL CLAUSE — **PROPOSED, NOT APPLIED (rule 6)**

> *Every committed placebo-differenced number must name three things beside it: the null KIND, the
> ESTIMATOR (whether the absolute value is taken before or after pooling over arms), and the SIGN
> CONVENTION of the difference. A number stated as `median_a |null − BLOCK|` may not be read as an
> effect size or compared to a floor: it is a dispersion statistic whose magnitude falls as 1/√S in
> the seed budget, whose sign is uninformative, and which can resolve a true-zero null (3 of 12
> cells here) and invert the sign of a real one (12 of 12 here). Directional placebo claims must be
> stated in the signed pooled form with a standard error.*

Scope note: this run prices the clause on its own 1,152-arm grid. It does **not** re-price the
record's 774 unstated-form numbers, because 88.4% of them do not state enough to be re-priced —
which is the clause's own justification.

**SURVIVORSHIP:** U56 and B136 are current-constituent lists; SMALL-664 is current constituents of
a sub-$2B screen with 52 tickers dropped for `max_1d_move ≥ 1.0`, so its CAGRs are upper bounds.
The headline quantity is a DIFFERENCE BETWEEN TWO NULLS ON THE SAME ARM and is far less exposed to
that bias than any level.

## CROSS-LANE NOTE (added at merge time, 2026-09-15)

The cloud lane ran idea 880 independently on the same day (`2026-09-15_...*_cloud`, its idea 2). Neither run saw the other. They **agree on the load-bearing point and answer different units**:

- **Denominator.** Cloud: only **5 of idea 871's 70 placebo-bearing files (7.1%)** can be re-priced at all. Lane B (this run): **774 of 876 committed placebo-differenced numbers (88.4%) state no estimator form at all**. Both say the adjudicable mass is tiny; they measure it on different units (files vs number-carrying lines).
- **The moved verdicts.** Cloud counts **CLAIMS**: 17.4% of re-priceable headline claims move verdict (39.1% over all 151 cuts). Lane B prices the **ESTIMATORS** on the cell grid: of the 13 (rung x budget x null) cells where both estimators resolve, **13 disagree on the sign**. These are complementary, not competing, readings.
- **Both conclude KILL for capital and both propose a PROTOCOL clause, neither applied (rule 6).**
