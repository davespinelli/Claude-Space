# idea 458 — why-is-the-ungated-control-the-IS-argmax-on-broad136-and-SMALL439-but-not-u56 (lane C, 2026-09-08/09)

**Verdict: ANSWERED / SPLIT. The queue's degeneracy is REAL and reproduced exactly, one of its
three candidate properties survives (the 200d gate's hit rate, and the sharper statistic behind
it), one is FALSIFIED as a cause (breadth — it is the property that reverses when the price
source changes), and one is the worst of nine (cross-sectional dispersion). The larger result is
that the degeneracy is a property of the IS WINDOW, not of the panels: the arm that sweeps 400 of
400 sub-menus in-sample ranks 22nd of 31 out of sample on broad136, 7th of 31 on SMALL439 and
31st of 31 on u56 — every one of the three panels reverses.**
One 4b passer falls out as a by-product (u56, rule-8 selected); PARK-recommended, not adopted —
memo block below. No RULES change; `RULES.md`, `scan.py`, `bot.py`, `baseline.py` untouched.

Script `2026-09-08_why-is-the-ungated-control-the-IS-argmax-on-broad136-and-SMALL439-but-not-u56_C.py`
(stages `--census`, `--fit`, `--halves` are re-runnable slices of the same file). 10 bps, t+1,
weekly/monthly per arm. 2 tuned dials: `k` = how many of the 12 non-equity names are in the panel
(-> phi = k/N) x `N` = breadth. 69 probe cells, ALL reported in `.grid.csv`; the 31-arm menu on
the 3 real panels x 2 cost rungs in `.arms.csv`.

## G0 — the number, reproduced before it is explained
Idea 241's lane-B harness imported by path (not re-implemented); its `fresh_grid` / `submenus`
(seed 20260908) / `live_cells` rebuilt: **1,200 live cells**, control is the IS-Sharpe argmax in
**400/400 broad136, 400/400 SMALL439, 92/400 = 23.00% u56**. Published numbers reproduced. **PASS.**

Underneath the sub-menus it is one panel-level fact (10 bps): the control beats **all 30** gated
arms on broad136 (D = +0.0325) and on SMALL439 (+0.0160), and is **6th of 31** on u56 (−0.0243).
A 400/400 sweep therefore rests on a Sharpe margin of **0.016–0.033** — the same order as the
0.013 margin idea 241 showed is the record's 46th percentile. Gated-arm Sharpe is gross-invariant
to max−min **0.0061** across gross 0.50/0.75/1.00, which is why the probe menu fixes gross at 1.00.

## R2/R3 — which panel property carries the sign
broad136 is a strict SUPERSET of u56, so breadth and composition were varied on one price source.
Best single-threshold accuracy for `ctl_wins_is` over the 69 cells:

| property | AUC | acc | threshold |
|---|---|---|---|
| `r_out` (annualised drift of the name-days the gate puts in cash) | +0.853 | **0.870** | ≥ +5.63%/yr |
| `rho` (mean pairwise correlation) | +0.856 | 0.855 | ≥ 0.327 |
| `inband` (**the 200d gate's hit rate**) | +0.837 | 0.855 | ≥ 0.711 |
| `negdrift` (share of names with negative IS drift) | +0.182 | 0.855 | < 0.036 |
| `N` (**breadth**) | +0.780 | 0.754 | ≥ 56 |
| `phi` (non-equity share) | +0.273 | 0.739 | < 0.167 |
| `disp` (**cross-sectional dispersion**) | +0.402 | 0.696 | < 0.222 |

Within the broad136 source, composition is everything and breadth is not significant:
`D_is ~ logN + phi` gives logN +0.0150 (t +1.34), phi **−0.4227 (t −7.54)**, R² 0.658.
**Leave-source-out (fit on the 56 broad-source cells, read once on the 13 small-source cells) is
the discriminating test:** `r_out` 0.893 → **0.769**, `inband` 0.875 → **0.769**, `N` 0.875 →
**0.231**, `phi` 0.857 → **0.231**. Breadth and non-equity share are broad136 artefacts whose
thresholds invert on a different price source; the gate's own hit rate and the drift of what it
cuts are the transferable statement. It is not exact: the real SMALL439 panel (`r_out` −14.5%/yr,
`inband` 0.543) is one of the three held-out misses — it is a control win the rule predicts wrong.

## R4 — rule 8, and the finding that matters
Property and threshold fitted on IS labels, read once on 2017–2026: **every** property scores
0.26–0.42 against a **0.84** majority-class baseline, because the base rate itself flips — the
control wins IS in **39 of 69** cells and OOS in **11 of 69**, with **36 of 39 IS wins flipping**
and corr(D_is, D_oos) = **−0.05**. On the three real panels the control's OOS Sharpe rank among
the 31 arms is **31/31 (u56), 22/31 (broad136), 7/31 (SMALL439)**. So the sub-menu experiments on
broad136 and SMALL439 are not merely constant — they are constant on the arm the out-of-sample
window ranks below the median. **CAUTION for every multi-panel chooser result that used this menu.**

## R5 — both KEEP paths (full sample and OOS window), 10 bps
`4a` 0 of 9 books (the live RULES v2 book's −12.1% MaxDD is not beaten by anything here).
`4b` 3 of 9 rows full and the same 3 on the OOS window — **two distinct books**: `b0-g1.00-M` on
u56 (counted twice, because there the IS-argmax over the whole menu and the IS-argmax over the
gated arms are the same arm, so the pick is rule-8-clean) and `b0-g1.00-M` on broad136 (which is
the gated argmax only — the whole-menu IS-argmax there is the control, and it fails). The three
ungated controls fail 4b on drawdown (u56 −29.2%, broad136 −32.7%, SMALL439 −46.0% vs SPY's
−33.7% x 0.60 = −20.2% bar).

## KEEP-candidate memo (PARK-recommended, NOT adopted — Sunday review decides)
1. Book: `u56 / EW-all-priced / 200d MA gate, band 0.0 / gross 1.00 / monthly` (`b0-g1.00-M`).
2. Selected rule-8-cleanly: highest IS Sharpe (2009–2016) of the 31-arm menu on u56, read once OOS.
3. Full sample: CAGR **11.96%**, Sharpe **1.213**, MaxDD **−15.5%**, H1 **1.249** / H2 **1.179**.
4. OOS 2017–2026: CAGR **12.72%**, Sharpe **1.275**, MaxDD **−15.5%**.
5. SPY: 15.23% / 0.889 / −33.7%, H1 0.957 / H2 0.834; OOS 15.45% / 0.882 / −33.7%.
6. 4b: Sharpe > SPY in both halves and OOS; MaxDD −15.5% ≤ 0.60 x −33.7%; CAGR 11.96% ≥ 0.70 x 15.23%. **PASS, full and OOS.**
7. 4a vs live RULES v2 (0.087 CAGR / 1.206 Sharpe / −12.1% MaxDD): **FAIL on drawdown.**
8. Exact RULES wording if ever adopted: *"Hold every instrument in the universe whose close is
   above its 200-day moving average at 100%/N of NAV, N = instruments priced that day; gated-out
   weight goes to CASH and is never re-spread. Rebalance on the last trading day of each month."*
9. **Why PARK, not KEEP:** the pick comes off a THREE-dial menu (band x gross x cadence), over
   PROTOCOL rule 4's two-parameter cap, and it is a parameter variant of the live book, not a new
   instrument; ideas 407/274/128 already show these dials are plateau-flat.
10. It is also the arm this script shows beats the ungated control OOS on all three panels — i.e.
    it is on the right side of the reversal, which is a reason to look again, not to adopt now.

## R6 — census: is the record degenerate the same way?
Every committed CSV carrying a panel column, an arm/book column and an IS Sharpe column, cell keys
found mechanically by idea 417's rule: **566 (file, panel) menus over 194 files**. Degenerate (one
arm is the IS argmax in EVERY cell of that panel, ≥2 arms, ≥2 cells): **121 of 566 = 21.4%**, in
**57 of 194 files**; median modal-argmax share 0.571. Only **15** of the 121 are won by an
explicitly labelled control arm — the other 106 are constant on a named parameter arm, which is
the same defect wearing a different label. By panel label the rate is highest exactly where idea
241 found it: `small439` 9/11 (81.8%), `broad136` 7/14 (50.0%), `SMALL439` 12/33 (36.4%),
`BSTK100` 4/9, versus `u56` 21/133 (15.8%). Full list in `.census.csv`.

## Survivorship / scope
SMALL439 is current constituents of the sub-$2B screen only (`data/SMALL_PANEL_README.md`); its
levels are not tradeable history and only the CONTRASTS are read here. SPY is a benchmark column
in every probe cell and is never investable. The non-equity sleeve spliced into the small panel is
priced from `data/prices.csv` reindexed onto the small panel's trading days.
