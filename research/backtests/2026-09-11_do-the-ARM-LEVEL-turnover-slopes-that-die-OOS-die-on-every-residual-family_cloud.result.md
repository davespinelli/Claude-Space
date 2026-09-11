# Idea 735 — do the ARM-LEVEL turnover slopes that die OOS die on EVERY residual family?

**ANSWERED / KILL of the turnover-specific reading. The IS-significant / OOS-dead pattern is
the NORM, not a property of turnover. No KEEP, no memo, no RULES / PROTOCOL / scan / bot /
baseline edit.** Plus one convention discrepancy found in idea 538's own 4a column, reported
and not resolved.

Script `2026-09-11_do-the-ARM-LEVEL-turnover-slopes-that-die-OOS-die-on-every-residual-family_cloud.py`;
tables `.ladder.csv` (46 rows), `.cells.csv` (324), `.grid.csv` (324), `.walkforward.csv` (12),
`.wfc.csv` (46), console `.console.txt`.

## G1 reproduction gate (printed before any new fit was read)
Idea 538's exact 162 cells / 324 books rebuilt from source:

| quantity | max abs deviation vs 538's committed table |
|---|---|
| `c_sd_is` / `c_bar_is` | 9.975e-17 / 1.110e-16 |
| `resid_is` / `resid_oos` | 4.449e-14 / 6.665e-14 |
| `to_is` / `tors_is` | 8.882e-16 / 3.553e-15 |
| book-level `CAGR` / `Sharpe` / `MaxDD` / `oSharpe` / `turn_yr` | 5.274e-16 / 6.661e-16 / 8.327e-16 / 6.661e-16 / 3.553e-15 |
| 4a column under **538's own comparand convention** | agrees 324/324 (0 vs 0) |
| 4b column | agrees 324/324 (16 vs 16) |

The rebuild is exact to float rounding — well inside idea 301's stated 1e-2 pp allowance for
the `prices.csv` daily vintage, which was not needed.

## The answer — three parts

### (1) "IS-significant, OOS-dead" is the norm. Turnover is the median case, not an outlier.
20 non-constant single-term predictors, each fitted on IS cell values only and scored ONCE on
the OOS truth. **Identical at both splits:**

| | OOS-dead | OOS-live |
|---|---|---|
| **IS-significant** (\|t\| ≥ 2) | **13** | 2 |
| IS-dead | 5 | 0 |

**13 of 15 IS-significant forms (87%) are OOS-dead, at BOTH splits.** Idea 538's two turnover
slopes (TORS t −4.11 R² 0.0953 ratio 1.2530; DTO t +4.38 R² 0.1070 ratio 1.2413) sit in the
middle of that group, not at its edge. By predictor group, median OOS MAE ratio vs the FAMILY
constant (both splits pooled):

| group | forms | IS-significant | OOS-live | IS-sig & OOS-dead | median ratio |
|---|---|---|---|---|---|
| BOOK (arm's own IS quality) | 6 | 4 | **0** | 4 | 1.2178 |
| DESIGN (cell coordinates) | 6 | 3 | **0** | 3 | 1.2080 |
| TURNOVER | 10 | 6 | **0** | 6 | **1.1820** |
| EXPOSURE (c_t path) | 10 | 9 | 2 | 7 | 1.1435 |
| DECOMP (IS gap/pred/resid) | 6 | 6 | **0** | 6 | 1.1302 |
| INCUMBENT (c_sd) | 2 | 2 | **2** | 0 | 0.9411 |

Four of the five non-c_sd groups have **zero** OOS-live forms. "Turnover dies out of sample"
is not a fact about turnover; it is what fitting 162 cells does.

### (2) What survives is not c_sd — it is the DISPERSION of the c_t path, and it has a twin.
The only two forms in the whole 20-form ladder that beat the FAMILY constant out of sample are
**CSD** and **CT_RANGE** (max(c_t) − min(c_t) on the IS window), and they are the same
quantity read two ways:

| split | form | IS t | IS R² | OOS MAE | ratio vs FAMILY |
|---|---|---|---|---|---|
| S2016 | FAMILY (incumbent constant) | — | — | 0.1937 | 1.0000 |
| S2016 | **CSD** | −6.32 | 0.1996 | 0.1773 | 0.9153 |
| S2016 | **CT_RANGE** | −6.16 | 0.1918 | **0.1769** | **0.9133** |
| S2018 | FAMILY | — | — | 0.2609 | 1.0000 |
| S2018 | **CSD** | −5.46 | 0.1570 | **0.2523** | **0.9669** |
| S2018 | **CT_RANGE** | −5.09 | 0.1393 | 0.2529 | 0.9693 |

CT_RANGE is new to the record and lands within 0.5% of the incumbent at both splits — ahead at
S2016, behind at S2018. That ordering is a coin-flip and is reported as one; the result that
matters is that **idea 535's finding generalises from `c_sd` to the c_t path's dispersion**,
and that no reading of the c_t path other than its dispersion survives (CBAR, ABSCBAR, CT_AC1,
GSHARE are all IS-significant and all OOS-dead).

### (3) IS R² does NOT predict OOS survival — which is the actual lesson.
- **DSH** (IS Sharpe DEGROSS − RESPREAD) has the **highest IS R² in the ladder, 0.4212, t =
  10.79** — and is **29% WORSE than the constant** out of sample (ratio 1.2902). At S2018 it is
  R² 0.5398, t 13.70, ratio 1.1560.
- **RESID_IS** (each cell's own IS residual) has R² = 1.0 by construction and still fails:
  ratio 1.0776 (S2016) / 1.0226 (S2018). The residual **does not persist cell by cell**.
- Spearman(IS R², OOS MAE ratio) over the 19 non-degenerate forms is **−0.1483** (S2016) and
  **−0.3088** (S2018). Weak, and explicitly **not** an inverse law — the separation is binary
  (two dispersion forms walk, seventeen do not) rather than graded in R².

So the record's habit of quoting a slope's t and R² as evidence that a predictor is real is
what fails here, in both directions: the strongest IS fit in the ladder is among the worst OOS,
and the two survivors are mid-R².

## A convention discrepancy in idea 538's 4a column (reported, NOT resolved)
Idea 538 computes its 4a comparand **once on the U56 panel** (`px_u = load_universe()`, its
line 376) and reindexes that single series onto all three panels. PROTOCOL rule 3 and
`baseline.compare()` instead run RULES v2 on the idea's **own** panel. The two readings differ
materially on the non-U56 panels:

| panel | same-panel RULES v2 | idea 538's U56-reindexed comparand |
|---|---|---|
| SMALL439 | Sharpe **0.5725** / MaxDD −14.68% | Sharpe **1.1689** / MaxDD −12.05% |
| B136 | Sharpe 1.1058 / MaxDD −12.24% | Sharpe 1.2056 / MaxDD −12.05% |

and therefore so does the verdict column: **4a is 9/324 under the same-panel comparand and
0/324 under 538's**, with all nine passes on SMALL439 DEGROSS. Both are published here; neither
is adopted as the record's convention, which is a rule-6 Sunday-review matter. (This is the
same mechanism idea 731 measured on a separate corpus today: 4a's pass rate is a function of the
comparand, and a weak comparand is what makes the bar reachable. None of the nine comes near
4b — their CAGRs are 1.9%–3.8% against SPY's 14.13%.)

## Rule 8 walk-forward
**WF-A** — each of 12 (panel, family, construction) arms picks its (level, cadence) on IS Sharpe
ALONE (2009/2011–2016) and 2017+ is read ONCE:

**beats RULES v2 OOS Sharpe 7/12; beats SPY OOS Sharpe 8/12; 4a 0/12; 4b 1/12.**

| panel | family | con | pick | OOS CAGR | OOS Sharpe | OOS MaxDD | v2 OOS Sharpe | SPY OOS Sharpe |
|---|---|---|---|---|---|---|---|---|
| SMALL439 | QUANTILE | RESPREAD | x=0.8 Q | 9.19% | 0.6169 | −35.07% | 0.5680 | 0.8820 |
| SMALL439 | QUANTILE | DEGROSS | x=0.8 Q | 7.59% | 0.6225 | −28.16% | 0.5680 | 0.8820 |
| SMALL439 | MA-THRESH | RESPREAD | θ=0.30 M | 24.02% | 1.1042 | −30.78% | 0.5680 | 0.8820 |
| SMALL439 | MA-THRESH | DEGROSS | θ=−0.40 Q | 7.98% | 0.5874 | −32.47% | 0.5680 | 0.8820 |
| U56 | QUANTILE | RESPREAD | **x=0.5 M** | **15.95%** | **1.2164** | **−19.80%** | 1.2747 | 0.8721 |
| U56 | QUANTILE | DEGROSS | x=0.5 M | 7.98% | 1.2168 | −10.32% | 1.2747 | 0.8721 |
| U56 | MA-THRESH | RESPREAD | θ=0.20 Q | 21.20% | 0.9326 | −32.51% | 1.2747 | 0.8721 |
| U56 | MA-THRESH | DEGROSS | θ=0.30 Q | 1.04% | 0.5655 | −3.38% | 1.2747 | 0.8721 |
| B136 | QUANTILE | RESPREAD | x=0.9 Q | 13.85% | 1.1262 | −24.65% | 1.1185 | 0.8820 |
| B136 | QUANTILE | DEGROSS | x=0.9 Q | 12.50% | 1.1284 | −22.33% | 1.1185 | 0.8820 |
| B136 | MA-THRESH | RESPREAD | θ=0.20 Q | 21.11% | 1.0665 | −29.53% | 1.1185 | 0.8820 |
| B136 | MA-THRESH | DEGROSS | θ=−0.25 Q | 13.58% | 1.1384 | −24.16% | 1.1185 | 0.8820 |

SPY OOS 15.24% / 0.8721 / −33.72% (U56 calendar), 15.45% / 0.8820 / −33.72% (B136, SMALL439).

**The single 4b pass is not a new result.** `U56 / QUANTILE x=0.50 / M / RESPREAD` (full sample
CAGR 15.47%, Sharpe 1.2359, MaxDD −19.80%, halves 1.3518 / 1.1454, OOS Sharpe 1.2164) is one of
the **16 books of these 324 that idea 538 already published as 4b passers**, and this run
reproduces all 16 exactly. Its DD leg clears by 0.4 pp (−19.80% against the −20.23% cap = 60% of
SPY's −33.72%), and it loses to RULES v2 on OOS Sharpe (1.2164 vs 1.2747). Promoting an
already-published book is a rule-6 Sunday-review decision, not a finding of this run; **no KEEP
is claimed here and no memo is written.**

**WF-C** — every IS-fitted predictor is used to CHOOSE the construction per cell:
always-RESPREAD 0.9350 / always-DEGROSS 0.9036 / oracle 0.9410 (S2016); 0.9793 / 0.9380 / 0.9839
(S2018). **All 46 (form × split) combinations pick RESPREAD for all 162 cells — zero decisions
changed, at every form including CSD and CT_RANGE.** 46/46 beat always-DEGROSS and 0/46 beat
always-RESPREAD, by construction. Every predictor in this ladder, the two survivors included,
is a **reporting rule, not a book.**

## Both KEEP paths, all 324 books
- **4a:** 9/324 (same-panel comparand) / 0/324 (idea 538's convention); 0/12 on the rule-8 leg.
- **4b:** 16/324, all reproductions of idea 538's committed passers; 1/12 on the rule-8 leg.
- **No KEEP.**

## Caveats
- **Survivorship (idea 54):** three current-constituent panels, no delistings, so every CAGR
  LEVEL is inflated and the 4a/4b columns inherit that in full. The headline object is an
  arm-minus-arm contrast on the same names, days and gross (both constructions share one gate
  mask), so the bias very largely cancels out of gap0 / pred0 / resid0; it does **not** cancel
  out of the KEEP columns. SMALL439 drops the 44 tickers with `max_1d_move >= 1.0` first.
- Two splits is two splits. The 87% figure is identical at both, but both share the same 162
  cells, so they are not independent evidence.
- `|t| >= 2` and `MAE <= FAMILY` are conventional cut-points; the full ratio is published for
  every form at both splits so any other cut can be read off `.ladder.csv`.

## Filed to the queue
- Is **CT_RANGE** a better-behaved reading of c_t dispersion than `c_sd` at other grosses and
  cadences, or is the S2016/S2018 order flip the whole story?
- Should PROTOCOL rule 3 state explicitly that the 4a comparand is run on the **idea's own
  panel**? Census how many committed rows used a reindexed U56 comparand instead.
- The record quotes IS t and R² beside residual-family predictors. Census how many committed
  "predictor is real" claims rest on an IS fit that was never scored against the constant out
  of sample.
