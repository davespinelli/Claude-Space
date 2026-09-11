# Idea 557 — re-read idea 300's WF-C KILL as a panel fact

**cloud lane, 2026-09-11.** Script `2026-09-11_re-read-idea-300s-WF-C-KILL-as-a-panel-fact_cloud.py`.
Two tuned parameters: **panel (3) × window split (5)**; every grid point reported (45 WF-C cells,
486 books, 90 walk-forward picks). Everything else inherited from ideas 300/305: theta ladder (9),
cadence {W,M,Q}, families {MA-THRESH, QUANTILE-M, QUANTILE-F}, gross 0.75, 10 bps, next-day.

## ANSWER — the kill is NEITHER a clean panel fact NOR a general one. It is a **SPLIT-AND-PANEL** fact, and the record's exposure is **5 statements, all idea 300's**.

**At the record's 2016-12-31 split the constant-residual discount walks forward on all three
panels** — including SMALL439, where idea 300 called it a kill:

| panel | OOS MAE, ZERO | OOS MAE, IS-mean constant | gain | verdict |
|---|---|---|---|---|
| U56 | 0.3389 | **0.2360** | +30.4% | constant walks |
| B136 | 0.5352 | **0.3562** | +33.4% | constant walks |
| SMALL439 | 0.5975 | **0.5789** | **+3.1%** | constant walks, *barely* |

Idea 300's own published numbers reproduce exactly (0.5975 → 0.5789), so **its headline "WF-C KILLS
the constant-residual discount" was never supported by its own MAE comparison** — the constant beat
zero there too, by 3.1%. What idea 300 actually measured was the **IS→OOS drift**: −0.0201 IS vs
−0.5918 OOS, a 29× move. That drift is real and is worst on SMALL439, but drift is not the test
WF-C runs.

## The split ladder (B2) — the kill is where the split lands, not which panel

Cell value = % of OOS MAE the IS-mean constant saves over zero on the **MA-THRESH** family (the one
idea 298's discount is about). Negative = the kill.

| panel | 2012-12-31 | 2014-12-31 | **2016-12-31** | 2018-12-31 | 2020-12-31 |
|---|---|---|---|---|---|
| U56 | +35.4 | +43.0 | **+30.4** | +31.8 | **−52.0** |
| B136 | +36.3 | +33.2 | **+33.4** | +25.4 | **−64.2** |
| SMALL439 | **−181.1** | +34.1 | **+3.1** | +0.9 | **−14.3** |

* **11 of 15** MA-THRESH panel × split cells walk forward; **4 are kills**.
* **Every panel is killed at the 2020-12-31 split** — a 2021–2026 OOS window turns the sign of the
  IS mean positive or near-zero on U56 (+0.0542 OOS vs −0.4770 IS), so a negative constant is worse
  than saying nothing. That is a **regime statement about the post-2020 window**, not about a panel.
* SMALL439 is genuinely the *weakest* panel (mean gain −31.4% vs +17.7% U56 / +12.8% B136) and is
  the only one killed at an early split, but it is **not uniformly killed**: it walks forward at 3 of 5.
* The QUANTILE arms (idea 298's ZERO claim) behave as claimed in magnitude — |OOS mean resid0| never
  exceeds **0.0531 pp/yr** over 30 cells — but zero wins only **11 of 30**, i.e. even a ~0.03 pp/yr
  constant is usually a better predictor than exactly zero.

## The audit (B3) — 5 committed kill-statements, all from idea 300; 3 quote it with no panel named

Census of `research/*.md`, `research/backtests/*.md` and `*.py`: **768 deduped mentions in 62 files**.
A row counts as STRICT only if its ±160-character neighbourhood carries a **discount phrase** AND the
**residual object** AND a **kill word** — a deliberately narrow filter, because LEADERBOARD rows carry
a literal `KILL` verdict column and later ideas reuse the "WF-C" label for entirely different tests.
That leaves **13 STRICT rows (12 prose)**, each then hand-adjudicated in a table published in the
script source and in `.census.csv`:

| file:line | scope | genuine kill-claim? | note |
|---|---|---|---|
| CHANGELOG.md:214 | panel-qualified | **YES** | idea 300's entry; says "on this panel" |
| LEADERBOARD.md:2901 | **GENERAL** | **YES** | idea 300's WF-C row — "KILL of the MA-gate constant-residual discount out of sample" |
| QUEUE.md:563 | **GENERAL** | **YES** | idea 300's Done entry — "WF-C KILLS idea 298's MA constant-residual discount out of sample" |
| 2026-09-06_…small-panel_C.result.md:87 | GENERAL* | **YES** | *line-wrap artefact: SMALL439 is named on the next wrapped line |
| 2026-09-06_…small-panel_C.result.md:88 | panel-qualified | **YES** | idea 300's result.md |
| CHANGELOG.md:216 | — | no | idea 298 — says the discount **walks forward** |
| LEADERBOARD.md:2890 | — | no | idea 298 — the kill is of the share-vs-c_bar **curve** |
| LEADERBOARD.md:4274 | — | no | **idea 305's correction** ("WF-C REVERSES idea 300's OOS KILL") |
| QUEUE.md:303 | — | no | idea 305's Done entry — carries the reversal |
| 2026-09-09_…replicate-off-SMALL439_B.result.md:89 | — | no | idea 305's correction |
| 2026-09-09_…residual-a-constant…_B.result.md:8 | — | no | idea 551 — frames it as untested OOS |

**So the queue's question answers: 3 of 5, and one of those three is a line-wrap artefact — the real
exposure is 2 uncorrected artefacts (`LEADERBOARD.md:2901` and `QUEUE.md:563`), both idea 300's own,
both stating the kill with no panel named in the reader's neighbourhood.** No *later* idea ever
propagated the claim as a general one; idea 305 already published the reversal in three places. The
record's problem is not mis-citation — it is that **idea 300's two artefacts were never restated**.

## Gates — 3 PASS, 2 FAIL, both failures diagnosed and neither a method error

| gate | result |
|---|---|
| **G0 ENGINE** | fast backtester vs `engine.backtest` (returns, turnover, gross) **6.939e-18** — PASS |
| **G1 IDENTITY** | max&#124;r_dg⁰ − c_t·r_rs⁰&#124; over 162 cells **6.939e-17** — PASS (idea 300 published 5.55e-17) |
| **G2 REPRODUCTION** | **1.150e-03 — FAIL**, and the whole residue is U56: per panel **U56 1.150e-03, B136 5.138e-15, SMALL439 6.543e-15** |
| **G3 MATCHING** | **0.01396 — FAIL** on QUANTILE-M; QUANTILE-F (the fractional fix) max **0.00225** |
| **G4 PURE-EXPOSURE** | max mean QUANTILE resid0 **0.0329 pp/yr** (U56 −0.0248, B136 −0.0310, SMALL439 −0.0329) — PASS |

**G2 is a two-trading-day data-vintage gap, not a disagreement.** `data/prices.csv` is 2026-09-10
today; idea 305 ran on 2026-09-09. B136 and SMALL439 read `prices_broad`/`prices_small`, unchanged
since 2026-09-04, and reproduce to 1e-15. Re-cutting U56 k trading days short:

| k | panel ends | IS mean | OOS mean | MAE zero | MAE const | max&#124;Δ&#124; vs idea 305 |
|---|---|---|---|---|---|---|
| 0 | 2026-09-10 | −0.3162 | −0.3383 | 0.3389 | 0.2360 | 1.150e-03 |
| 1 | 2026-09-09 | −0.3162 | −0.3382 | 0.3385 | 0.2348 | 4.801e-04 |
| **2** | **2026-09-08** | −0.3162 | −0.3377 | 0.3382 | 0.2348 | **9.839e-07 ← reproduces** |
| 3 | 2026-09-04 | −0.3162 | −0.3365 | 0.3372 | 0.2350 | 1.228e-03 |

**G3 is a reproduction of a defect idea 305 itself documented**: `ceil(x·n_t)` hands the constant-depth
arm up to 1/n_t of extra exposure, and 1/55 = 0.01818 on U56 — the worst cell is U56 QUANTILE-M at
theta +0.30 (+0.01396). The fractional arm QUANTILE-F fixes it (0.00225) and **its WF-C verdict
matches QUANTILE-M in 14 of 15 cells**, so the defect does not drive this run's answer.

## Rule 8, book leg (B4) — mandatory, and it finds nothing new

(theta, cadence) picked on the IS window alone by IS Sharpe, per panel × family × construction ×
split; OOS read once. At the record's split:

| panel | best pick | OOS CAGR | OOS Sharpe | OOS MaxDD | vs SPY | vs RULES v2 |
|---|---|---|---|---|---|---|
| U56 | QUANTILE-M/RESPREAD th+0.30 W | 29.86% | 1.0947 | −32.21% | +0.2226 | −0.1800 |
| B136 | MA-THRESH/DEGROSS th−0.25 Q | 13.58% | 1.1384 | −24.16% | +0.2564 | −0.1467 |
| SMALL439 | MA-THRESH/RESPREAD th+0.30 M | 24.02% | 1.1042 | −30.78% | +0.2221 | −0.1809 |

Comparands OOS: SPY **15.24% / 0.8721 / −33.72%** (U56 frame), **15.45% / 0.8820 / −33.72%**
(B136, SMALL439 frames); RULES v2 **9.45% / 1.2747 / −12.05%** and **9.53% / 1.2851 / −12.05%**.

**4a 2/486 on the grid and 0/90 at the walk-forward picks — no arm's IS pick beats RULES v2 OOS on
any panel or any split. 4b 20/486 and 2/90.** Binding legs over the grid: DD 328 · CAGR 243 ·
OOS 183 · H2 176 · H1 168. Every one of the 20 4b passers is a U56/B136 gate book inside the
**MA-DISTANCE TOP-HALF family already memoed** as `2026-09-11_4b-candidate-U56-MA-DISTANCE-TOP-HALF-monthly_memo.md`
(idea 536R), which that memo itself declines. **NO NEW KEEP-CANDIDATE, NO MEMO.**

## Appendix — the 4b passers under an equal-weight bar (idea 742, same run, same day)

Idea 742 established today that a 4b pass against cap-weighted SPY on a large-cap panel is largely a
comparand fact. Re-scoring all 20 passers against an equal-weight basket of their own panel
(U56 17.94% / 1.1357 / −28.87%; B136 19.22% / 1.1361 / −32.52%; SMALL439 14.35% / 0.7249 / −45.61%):

**0 of 20 survive.** The binding leg is the **DD cap** on 18 of 20 (the equal-weight bar's own
drawdown is deep enough that 60% of it is a tighter cap than 60% of SPY's −33.72%), plus CAGR on 15.
This is an independent confirmation of idea 742 on a disjoint book population.

## Caveats

1. **Survivorship.** All three panels are current constituents / a current screen; SMALL439 drops the
   44 names with `max_1d_move >= 1.0`. Every absolute number is inflated. The panel *contrast* is
   less exposed, but "SMALL439 behaves differently" could be a property of that screen rather than of
   small caps.
2. **The 2020-12-31 split has only ~5.7 years of OOS** and covers one regime; its unanimous kill
   should be read as "the constant's sign is not stable into 2021–2026", not as a fourth panel fact.
3. **27 cells per WF-C reading** (9 theta × 3 cadences) are not independent — they share a panel and
   overlapping gates — so the MAE gains are descriptive, not significance-tested.
4. G2/G3 both fail as recorded above; the run is reported with those failures standing, diagnosed,
   and not re-barred.

## PROPOSED (not applied — PROTOCOL rule 6)

Restate the two uncorrected idea-300 artefacts (`LEADERBOARD.md:2901`, `QUEUE.md:563`) to name the
panel and the split, e.g. *"on SMALL439 at the 2016-12-31 split the IS-mean constant beats zero by
only 3.1% of MAE after a 29× IS→OOS drift"* — which is what idea 300's own numbers say. RULES.md,
PROTOCOL.md, scan.py, bot.py and baseline.py are untouched by this run.
