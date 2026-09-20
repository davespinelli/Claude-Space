# Idea 736 (lane cloud, 2026-09-20) — IS CT_RANGE A BETTER-BEHAVED READING OF c_t DISPERSION THAN c_sd?

**ANSWERED — NO, AND NEITHER IS c_sd. The two are INTERCHANGEABLE and the object should be named
"c_t DISPERSION" with the estimator stated beside every number. But the interchangeability is NOT a
property of dispersion: it is a property of the TAIL-SENSITIVE estimators — the one form that
discards the tails (CT_IQR) is measurably worse at 8 of 8 cells. NO NEW KEEP. NO RULES CHANGE.**

Script: `research/backtests/2026-09-20_ct-dispersion-estimator-on-a-gross-ladder_cloud.py`
(`.cells.csv` 1,296 rows, `.books.csv` 1,296 books, `.ladder.csv` 80 fits, `.compare.csv`,
`.family.csv`, `.walkforward.csv` 60 picks, `.gates.csv`, `.log.txt`). **GATES 23 of 23.**
Deterministic, offline. RULES.md / PROTOCOL.md / scan.py / bot.py / baseline.py untouched (rule 6).

## The construction

Idea 538's corpus: a gate mask run two ways on the SAME names, days and cadence — `RESPREAD`
(`w = g·e_in/n_in`) and `DEGROSS` (`w = g·e_in/n_live`, the live clause) — with
`c_t = gross(DEGROSS)/gross(RESPREAD)` and the timing residual
`resid0 = 100·[CAGR(DG) − CAGR(RS)] − 100·[CAGR(c̄·RS) − CAGR(RS)]` as the target.

TUNED (2, exactly the pair the idea's own text names): **ESTIMATOR** {CSD, CT_RANGE, CT_IQR,
CT_MAD, CT_SD_RANGE, CBAR, TORS + the constants ZERO/GLOBAL/FAMILY} and **GROSS** {0.25, 0.50,
0.75, 1.00} — 735/538 fixed 0.75. Published, not tuned: panel {U56, B136, SMALL665}, family
{QUANTILE ×9 levels, MA-THRESH ×9 thetas}, cadence {W, M, Q}, split {S2016, S2018}, 10 bps,
next-day execution. **648 cells, 1,296 books, 80 fits — every grid point reported.** Both
constructions share one unit direction, so the whole gross ladder is EXACT off one per-cell state;
**G1 re-asserts it against `engine.backtest` at 3.5e-18 … 2.1e-17 on all nine panel × cadence pairs.**

## V1 NOT TRIGGERED / V2 TRIGGERED — neither estimator dominates

| gross | split | MAE CSD | MAE CT_RANGE | FAMILY | winner | Δ | SE | t | 95% CI |
|---|---|---|---|---|---|---|---|---|---|
| 0.25 | S2016 | 0.060529 | 0.060982 | 0.065126 | CSD | −0.000453 | 0.000737 | −0.61 | [−0.0019, +0.0010] |
| 0.25 | S2018 | 0.088079 | 0.088419 | 0.090030 | CSD | −0.000340 | 0.000499 | −0.68 | [−0.0013, +0.0006] |
| 0.50 | S2016 | 0.121369 | 0.122307 | 0.132647 | CSD | −0.000938 | 0.001397 | −0.67 | [−0.0037, +0.0017] |
| 0.50 | S2018 | 0.179490 | 0.180416 | 0.184634 | CSD | −0.000926 | 0.001001 | −0.93 | [−0.0029, +0.0010] |
| 0.75 | S2016 | 0.183950 | 0.185346 | 0.203220 | CSD | −0.001396 | 0.002243 | −0.62 | [−0.0057, +0.0029] |
| 0.75 | S2018 | 0.275787 | 0.277512 | 0.285210 | CSD | −0.001725 | 0.001533 | −1.13 | [−0.0047, +0.0012] |
| 1.00 | S2016 | 0.249730 | 0.251841 | 0.277892 | CSD | −0.002112 | 0.003058 | −0.69 | [−0.0082, +0.0039] |
| 1.00 | S2018 | 0.378666 | 0.381484 | 0.393336 | CSD | −0.002818 | 0.002066 | −1.36 | [−0.0069, +0.0012] |

**Idea 735's order flip does not reappear: CSD is the point-estimate winner at 8 of 8 cells.** But
the difference is **not resolvable anywhere** — the paired-cell bootstrap (2,000 draws, the same 162
cell indices resampled for both estimators) gives max |t| **1.36**, and the 95% CI covers zero at
**8 of 8**. V1's dominance test therefore FAILS on its resolvability leg and **V2 triggers**: the
surviving object is **"c_t dispersion"**, and the record must state which estimator any published
number used — the same defect idea 564 found for unnamed correlation statistics, on the scale axis.

## V3 — THE INTERCHANGEABILITY IS A TAIL FACT, NOT A DISPERSION FACT

| estimator vs CSD | CI covers zero | t range |
|---|---|---|
| CT_RANGE | **8 of 8** | −1.32 … −0.61 |
| CT_MAD | **8 of 8** | −1.08 … −0.55 |
| **CT_IQR** | **0 of 8** | **−3.83 … −2.25** |

Order is **stable at 8 of 8 cells**: `CSD < {CT_RANGE, CT_MAD} < CT_IQR`, with only the middle pair
swapping. CT_IQR is also the single reason "all four beat the FAMILY constant" reads 7 of 8 rather
than 8 of 8 — at gross 0.25 / S2018 it posts **0.090373 against FAMILY's 0.090030** and loses to a
constant outright. So what `c_sd` measures is **the TAIL of the c_t path**, not dispersion
generically: every estimator that keeps the tails (SD, RANGE, MAD) is statistically
indistinguishable from every other, and the one that throws them away (the interquartile range)
falls measurably behind. That is a falsifiable statement the record did not have.

**And the two-term form buys nothing.** `CT_SD_RANGE` ties CSD to five decimals (0.184741 vs
0.183950 at gross 0.75 / S2016) while the IS |t| collapses from **6.87** (CSD alone) to **2.24** —
collinearity, not information.

## The gross ladder — the rung was NOT load-bearing for the estimator question

OOS MAE as a share of the FAMILY constant's (the estimator's whole purchase):

| gross | CSD / FAMILY, S2016 | CSD / FAMILY, S2018 |
|---|---|---|
| 0.25 | 0.9294 | 0.9783 |
| 0.50 | 0.9150 | 0.9721 |
| 0.75 | 0.9052 | 0.9670 |
| 1.00 | 0.8987 | 0.9627 |

The absolute MAE scales with gross (so does `resid0`), but the estimator's advantage is a slowly
GROWING fraction — 735's 0.75-only reading understates it at gross 1.00 and overstates it at 0.25.
**The ORDER of the forms never changes across the ladder**, so the gross rung did not carry 735's
result, and the ladder does not rescue CT_RANGE at any rung.

## G2c — A DATA-VINTAGE FINDING THE RECORD NEEDS

G2b reproduces idea 735's committed cells **on U56** (the stable `prices.csv` cache) to
**2.61e-07** (c_sd), **3.67e-06** (ct_range), **1.44e-07** (c̄), **1.38e-05** (turnover) and
**6.25e-04** (resid_is). **B136 and SMALL do not reproduce, and the cause is the DATA, not the
construction** — G1 proves the runner is engine-exact to 1e-17 on all nine panel × cadence pairs.

`gshare` (= n_gated_in / n_live, a pure panel-composition number with no book in it) already
differs by **9.58e-06 (U56) / 5.12e-05 (B136) / 6.42e-02 (SMALL)** before any book is run. Idea 735
ran on a SMALL panel of **439 names** (44 dropped for `max_1d_move >= 1.0`); today's cache holds
**665** after the same rule (54 dropped) — **a different universe**. `prices_broad.csv` was likewise
re-fetched with restated adjusted closes: B136's IS-window RESPREAD turnover moves **0.184
turns/yr** and SMALL's **1.500**, against U56's 1.4e-05 — and since the IS window ENDS 2016-12-31 in
both runs, a longer tape cannot explain it. The historical prices moved.

**Consequence: every committed number on the SMALL panel from before the 2026-09-20 re-cache is on a
different universe and is not reproducible today.** A PANEL VINTAGE stamp (name count + cache sha)
belongs beside every published panel number — the price-side twin of idea 894's tree stamp.

## V4 — CAPITAL ARM (1,296 books, 10 bps, next-day execution)

| gross | 4a | 4b | mean Sharpe | mean MaxDD | mean turn |
|---|---|---|---|---|---|
| 0.25 | 69/324 | **0/324** | 0.9419 | −7.81% | 1.01/yr |
| 0.50 | 10/324 | 13/324 | 0.9417 | −15.21% | 2.00/yr |
| 0.75 | 3/324 | 16/324 | 0.9411 | −22.21% | 2.97/yr |
| 1.00 | 3/324 | 10/324 | 0.9401 | −28.84% | 3.94/yr |

By panel: **U56 4a 0/432, 4b 28/432**; B136 4a 49/432, 4b 10/432; SMALL665 4a 36/432, 4b 1/432.
**PATH 4a: KILL.** Every 4a pass is on a panel where the live RULES v2 book is RESTATED (B136 or
SMALL) — on U56, the panel the live book actually runs on, 4a is **0 of 432 books and 0 of 20 legal
picks**. Same panel-restatement artefact ideas 763 / 1793 recorded; 4a is computed here under
PROTOCOL rule 3's same-panel comparand, which is the generous reading.

**RULE 8** (level and cadence on 2009-2016 IS Sharpe only; 2017-2026 read ONCE; gross published as a
separate arm, plus a joint (gross, level, cadence) chooser): **4b 2 of 60 legal picks, 4a 9 of 60
and all nine at gross 0.25 on the restated panels.** The joint chooser clears 4b **0 of 12**.
The two 4b-reachable picks:

* **U56 QUANTILE top-50% monthly RESPREAD, gross 0.75** — FULL 15.48% / 1.2371 / −19.80%
  (H1 1.344 / H2 1.155), **OOS 15.96% / 1.2185 / −19.80%** at 3.10 turns/yr, against SPY
  15.12% / 0.8844 / −33.72% (OOS 15.26% / 0.8738) and live RULES v2 8.62% / 1.2011 / −12.05%
  (OOS 9.46% / 1.2769). Its OOS drawdown-cap margin is **0.43 pp** (−19.80% against −20.23%) —
  the same knife-edge as the parked VOLTGT memo's 0.37 pp, so it is NOT filed as a KEEP-candidate
  here: it is one of 1,296 grid points in a run pre-registered for an ESTIMATOR question, and it
  would need its own pre-registered pass before any wording leans on it.
* SMALL665 MA-THRESH θ=0.30 monthly RESPREAD, gross 0.50 — OOS 15.85% / 1.1308 / −20.18%.

The best 4b-clearing book in the whole grid (U56 MA-THRESH θ=0.00 monthly DEGROSS, gross 1.00:
FULL 11.94% / 1.2144 / −15.54%, OOS 12.68% / 1.2754 / −15.54%) is **not reachable by any legal
IS-only chooser**.

## Caveats, stated

**SURVIVORSHIP:** all three panels are CURRENT constituent lists — no delistings — so every CAGR
LEVEL is inflated and the 4a/4b columns inherit that in full. The headline object is an
arm-minus-arm contrast on the SAME names, days and gross (both constructions share one gate mask),
so the bias very largely cancels out of gap0/pred0/resid0; it does NOT cancel out of the KEEP
columns. SMALL drops 54 tickers with `max_1d_move >= 1.0` first. The paired-cell bootstrap resamples
CELLS, which are not independent (the same panel and family recur), so its SE is if anything
optimistic — and it still cannot separate CSD from CT_RANGE.
