# Idea 797 — should every published PANEL-ORDERING quote its ADJACENT GAP over FLOOR instead of its SPAN?

**cloud lane, 2026-09-11.** Script `2026-09-11_should-every-published-PANEL-ORDERING-quote-its-ADJACENT-GAP-over-FLOOR_cloud.py`, console `…console.txt`, artefacts `.grid.csv` (900) `.floors.csv` (60) `.spans.csv` (90) `.cells.csv` (48) `.census.csv` (32) `.retire.csv` (32) `.windows.csv` (6) `.walkforward.csv` (20) `.keeppaths.csv` (900) `.sites_COMMITTED.csv.gz` (2,334) `.sites_ALL.csv.gz` (4,884). 113 s, deterministic, no network.

## ANSWER — YES, and the whole effect is the NUMERATOR, not the floor

**The swap retires every re-scorable committed panel-ordering claim that passed the record's own bar: 574 of 574 (100%), 0 reinstated.** But read the resolution caveat below before quoting the 574.

**KILL for capital.** The bar swap is a reporting rule, not a book. No RULES change, no book promoted, no KEEP claimed, no PROTOCOL edit applied (rule 6, Sunday review); RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py untouched.

## GATES — five, pre-registered, printed before any new number was read. ALL PASS

| gate | result | bar |
|---|---|---|
| G0 draw determinism | **0 of 72** draws differ on rebuild | 0 |
| G1 `fast_backtest` vs `engine.backtest` | **0.000e+00** | 1e-12 |
| G2 **cross-lane** — idea 773's committed `.floors.csv`, all **60 rows × 7 cols**, rebuilt from prices here | **8.882e-16** | 1e-12 |
| G3 **cross-lane** — idea 773's committed `.spans.csv`, all **90 rows × 29 numeric cols**, plus `order`/`top`/`span_pair`/`margin_pair` labels identical | **8.882e-16**, labels `True` | 1e-12 |
| G4 live RULES v2 on U56 vs committed 0.0861 / 1.1998 / −0.1205 | **4.945e-05** | 1e-4 |
| G5 claim harvest rebuilt twice | identical | 0 |

G2/G3 make this a genuine reproduction of lane C's same-day numbers from prices, not a re-quote. Idea 773's headline replicates exactly: at D=6 **SPAN/POOLED clears its floor in 66 of 90 cells** (FULL 24/30, IS 23/30, OOS 19/30) and **GAP/RSS in 2 of 90** (FULL 2, IS 0, OOS 2).

## THE TWO BARS — all 90 cells, D=6 (every D in `.cells.csv`)

| bar form | FULL | IS | OOS | median ratio (FULL/IS/OOS) |
|---|---|---|---|---|
| SPAN_POOLED *(the record's bar)* | 24/30 | 23/30 | 19/30 | 2.44 / 2.22 / 2.16 |
| SPAN_RSS | 22/30 | 20/30 | 17/30 | 1.70 / 1.42 / 1.21 |
| GAP_POOLED | 2/30 | 0/30 | 2/30 | 0.37 / 0.18 / 0.34 |
| GAP_RSS *(proposed)* | 2/30 | 0/30 | 2/30 | 0.30 / 0.15 / 0.37 |

**H_NUMERATOR PASS, and it is not close: 574 retirements vs 19.** Swapping only the floor (POOLED → RSS over the gap's own pair) retires **19 of 574 (3.3%)**. Swapping only the numerator (span → smallest adjacent gap) retires **574 of 574 (100%)**. The RSS floor is cosmetic; the record's defect is quoting the span. Recommended wording therefore fixes the numerator and may keep either floor.

## THE CENSUS — 2 claim sets × 4 bar forms × 4 draw counts, all 32 points in `.retire.csv`

| claimset | files | lines naming ≥2 panels | ORDERING sites | re-scorable | pass SPAN_POOLED | retired by GAP_RSS |
|---|---|---|---|---|---|---|
| COMMITTED | 789 | 2,334 | 922 | **693** (75.2%) | **574** | **574 (100.0% of passers, 82.8% of all)** |
| ALL | 2,207 | 4,884 | 1,421 | 897 | 774 | 774 (100.0% / 86.3%) |

229 of the 922 committed ordering sites are dropped for carrying no recoverable statistic. Stable across D: retirement 574/574 at D=3/6/12 and 597/597 at D=24.

**RESOLUTION CAVEAT, stated plainly:** the bar is evaluated at **(statistic, window)** granularity, because the claim text almost never quotes its own margin or floor — those are rebuilt from prices. So the 693 claims carry only **15 distinct verdicts**, and the honest statement of the result is the statistic-level one: **of the 5 statistics, 3 pass SPAN_POOLED at each window and all 3 are retired by GAP_RSS — 3/3 at FULL, 3/3 at IS, 3/3 at OOS.** The 574 is that 3-of-3 weighted by how often the record repeats each claim. Both readings are committed (`.retire.csv` and `.windows.csv`); neither is an independent-claim count.

## MECHANISM — the binding gap is the NESTED PAIR in 75 of 90 cells (83.3%)

`U56 ⊂ B136 on 55 of 55 names` (verified here, U56-only set empty). The smallest adjacent gap sits on the **U56|B136** pair in **75 of 90 cells** — 63 as `U56|B136`, 12 as `B136|U56`. Idea 773 measured 21 of 30 OOS cells; it generalises to 83.3% over the full 90. So the statistic that decides almost every three-panel ordering in this record is a gap between a panel and a strict superset of itself, i.e. not an independent-panel comparison at all. That is the reason the gap sits inside the floor: a nested pair shares most of its composition luck, so its spread is small while the pooled floor is built from draws that do not.

## RULE 8 — WF-A on the answer, WF-B on a book, OOS read ONCE

**WF-A.** Census re-run separately on FULL / IS / OOS. Retirement share of old passers: **100.0% (18/18) FULL, 100.0% (105/105) IS, 100.0% (451/451) OOS**. Statistic-level: 3/3 at every window. **H_WINDOW PASS** (OOS ≥ IS), **H_WF PASS** (|OOS − IS| = 0 pp ≤ 10). The bar chosen in-sample keeps its verdict out of sample.

**WF-B.** The ordering taken at face value as a trading instruction: hold the panel the IS ordering puts first, but only where that bar clears its floor in ≥4 of 6 IS cells; where it does not the bar issues **no instruction** and the book stays the incumbent (live RULES v2 on U56). (gross, cadence) then chosen by IS Sharpe alone.

| selector statistic | SPAN_POOLED holds | OOS CAGR / Sharpe / MaxDD | GAP_RSS holds | OOS CAGR / Sharpe / MaxDD |
|---|---|---|---|---|
| PREM_SHARPE | no instruction (3/6) | 9.45% / 1.2747 / −12.05% | no instruction (0/6) | 9.45% / 1.2747 / −12.05% |
| PREM_CAGR | no instruction (3/6) | 9.45% / 1.2747 / −12.05% | no instruction (0/6) | 9.45% / 1.2747 / −12.05% |
| SHARPE | **U56 MA-RS g1.00 M** (6/6) | **18.26% / 1.1936 / −23.73%** | no instruction (0/6) | 9.45% / 1.2747 / −12.05% |
| CAGR | **B136 MA-RS g1.00 M** (5/6) | **17.25% / 1.1016 / −28.35%** | no instruction (0/6) | 7.98% / 1.1185 / −12.24% |
| MAXDD | **U56 MA-RS g1.00 M** (6/6) | **18.26% / 1.1936 / −23.73%** | no instruction (0/6) | 9.45% / 1.2747 / −12.05% |

Comparands on the selected panel, OOS: **RULES v2 9.45% / 1.2747 / −12.05%; SPY 15.24% / 0.8721 / −33.72%.**
**H_BOOK PASS.** Under the old bar the record's orderings tell you to leave the incumbent for a gross-1.00 monthly MA-RS book in 3 of 5 currencies; under the new bar **every one of the 5 falls silent** and you stay in the incumbent. Across all 20 (statistic × bar form) WF-B books: **beat RULES v2 on OOS Sharpe 0/20; beat SPY on OOS Sharpe 20/20.**

The capital reading is two-sided and is not a recommendation: the swap **protects OOS Sharpe** (1.2747 vs 1.1936/1.1016) and **MaxDD** (−12.05% vs −23.73%/−28.35%) and **costs 8.8 pp of OOS CAGR** (9.45% vs 18.26%). A silent bar is the right answer to an unsupported claim, but it is not evidence that the incumbent is the better book — that question is idea 677/675's gross-window business, untouched here.

## KEEP PATHS — every one of the 900 books

4a **1** (a DRAW panel, not a tradable rule), 4b **52**, BOTH **0**. On the **REAL parents: 4a 0 of 36, 4b 3 of 36** — `U56 MA-RS g0.75 W` (11.55% / 1.0914 / −18.62%, H1/H2 1.181/1.026, OOS Sharpe 1.1078), `U56 MA-RS g0.75 M` (12.60% / 1.1594 / −18.21%, 1.221/1.115, OOS 1.1930), `B136 MA-RS g0.75 W` (11.66% / 1.0585 / −20.12%, 1.160/0.971, OOS 1.0660). **NOT a new candidate:** identical to idea 773's same-day rows and to lane B's, and a single-rung gross pass. Binding 4b legs across all 900: DD 637, CAGR 425, H1 322, H2 315, OOS 306.

## SURVIVORSHIP

`universe_broad.json` and the small panel are **current constituents** of their screens; SMALL439 drops every ticker with `max_1d_move ≥ 1.0` in `data/small_meta.csv` (439 of 483 kept). On a premium the bias largely cancels; on the LEVEL statistics it does not, so every level span and gap here is an upper bound and every floor a lower bound — which biases the OLD bar toward passing and therefore biases this run **toward** finding retirements. The nested-pair mechanism is not survivorship-driven: `U56 ⊂ B136` is a construction fact of the two universe files.

## PROPOSED WORDING (not applied — PROTOCOL edits are Sunday-review business, rule 6)

> A claim that orders three or more panels must quote the **smallest adjacent gap** in the ordering, not the span, and must quote it against a noise floor built on the same window. Where two panels in the ordering are nested, the claim must say so and name the binding pair.

## HYPOTHESES

H_REPRO **PASS** · H_RETIRE **PASS** · H_NUMERATOR **PASS** · H_WINDOW **PASS** · H_WF **PASS** · H_BOOK **PASS**.
