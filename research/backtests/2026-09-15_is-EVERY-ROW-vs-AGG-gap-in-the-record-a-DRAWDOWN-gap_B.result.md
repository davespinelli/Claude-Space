# Idea 662 — is EVERY ROW-vs-AGG gap in the record a DRAWDOWN gap?

**lane B, 2026-09-15 · script `2026-09-15_is-EVERY-ROW-vs-AGG-gap-in-the-record-a-DRAWDOWN-gap_B.py`**

**ANSWERED = NO as literally asked, YES as a mechanism. KILL for capital.** No RULES change, no book
promoted, no KEEP claimed, no PROTOCOL edit; RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py
untouched (rule 6).

## What was run

Idea 655 priced row-level vs aggregate-only resolution on ONE gate (the RULES v2 200d ±3% band) and
found AGG buys OOS CAGR and pays MaxDD. This run repeats the identical three-mode construction on
**four committed gate families** × **three panels** × **10 breadth triggers** × **3 gross rungs** =
**756 grid points, all published** in `.grid.csv`.

* **ROW** knows WHICH names pass: each passing name at `gross`/N of NAV, rest in CASH.
* **AGG** knows only HOW MANY (breadth `b_t`): the WHOLE priced panel equal-weighted at `gross`
  when `b_t ≥ θ`, else all cash.
* **HYB** knows both: the ROW book, switched off on days when `b_t < θ`.

Families (every per-name threshold is a committed constant or a dial-free cross-sectional statistic;
only **θ and gross** are tuned — PROTOCOL 4's maximum of two): **TREND** 200d ±3% band ·
**VOL** 20d ann. vol < 0.60 (`rules_v1`'s `max_vol`) · **MOM** 12-1 momentum > 0 (`score`'s `mom`) ·
**DISP** 60d idiosyncratic vol below the panel's own cross-sectional mean that day.
10 bps, weekly, t+1, no shorting/leverage. Panels U56 / B136 / SMALL663.

**Gates, six, all PASS, printed before any result number was read:** G1 TREND/ROW at gross 0.75 **IS**
`baseline.rules_v2_weights` (max|dW| 0.000e+00, max|dR| 0.000e+00); G2 `fast_run` == `engine.backtest`
over 4,702 finite rows (returns **8.674e-18**, turnover **1.978e-16**); G3 AGG at θ=0 is the same
buy-and-hold panel in all four families (0.000e+00); G4 HYB at θ=0 == ROW in every family
(0.000e+00); G5 an always-TRUE gate reduces ROW to AGG(θ=0) (0.000e+00); G6 U56 SPY
15.13%/0.8845/−33.72% and RULES v2 8.62%/1.2013/−12.05% against their committed triples.

## The answer

**Matched-gross census (the clean test — same family, same panel, same gross, AGG vs ROW):**

| leg | cells | AGG buys CAGR over ROW | of those, pays drawdown | **FREE** |
|---|---|---|---|---|
| full sample | 360 | 261 | **261** | **0** |
| OOS (2017–) | 360 | 246 | **244** | **2** |

So the queue's dichotomy is **not a property of the band gate** — it reproduces in all four families
and all three panels, **0 free cells in 11 of 12 family × panel blocks** and 261 of 261 full-sample.
The two OOS exceptions are both U56 TREND at θ=0.70 and are **economically null**: +0.0089 pp and
+0.0041 pp of CAGR, i.e. ties to inside a basis point, on an arm that sits in cash 31% of days.
**H3 is REFUTED on the letter and confirmed on the substance.** Pooled median cost of aggregation
per family × panel runs **−0.83 pp to −12.57 pp of MaxDD** for **−1.33 pp to +5.10 pp of CAGR**.

**Rule 8 (θ, gross fitted on 2009–2016 by IS Sharpe, 2017–2026 read once, 36 picks):**
H1 (AGG pick buys OOS CAGR) **10/12**, H2 (AGG pick pays OOS drawdown) **11/12** — and **all three
exceptions are gross artefacts, not resolution facts**: the picks are not matched-gross (SMALL663
VOL's AGG pick is g=0.50 against ROW's g=1.00), and the matched-gross census above shows 0 free
cells in each of those same three blocks. Across the 36 picks the mode medians are **AGG OOS CAGR
16.13% / MaxDD −29.18%** against **ROW 9.46% / −23.34%**: +6.7 pp of return for +5.8 pp of drawdown.

**H4 as stated is REFUTED but its mechanism is confirmed.** The modal 4b blocker record-wide is the
**CAGR floor** (544 of 705 failures) not the DD cap (300) — but the cap is what specifically punishes
aggregation: DDCAP blocks **186 of 340 AGG** cells, **102 of 333 HYB**, **12 of 32 ROW**.
**H5 holds: 4a passes 3 of 756 grid points and 0 of 36 rule-8 picks at 10 bps.**

## Capital verdict — KILL

4b passes **51 of 756** grid points, but **40 of 51 sit at gross 0.75**, so they are idea 657's
exposure fact again, not a resolution fact. Rule-8 picks clearing 4b at **all** cost rungs (0/10/25):
**2 of 36**, both U56 TREND — `ROW θ=0.00 g=1.00`, which **is the standing band candidate**
(11.54%/1.2011/−15.91% full, halves 1.2327/1.1762, OOS 12.68%/1.2765/−15.91%), and its HYB twin at
θ=0.30, which adds **+0.03 pp of CAGR and +0.010 of Sharpe on an identical MaxDD** — inside noise and
not worth a second dial. Nothing new is promoted. Reference rows: RULES v2 U56 8.62%/1.2013/−12.05%
(OOS 9.46%/1.2772), SPY 15.13%/0.8845/−33.72% (OOS 15.27%/0.8740).

## Caveats

**SURVIVORSHIP (rule 9):** all three panels are current-constituent lists — U56/B136 from the
committed universe files, SMALL663 the sub-$2B panel after dropping 52 tickers with
`max_1d_move ≥ 1.0` per `data/small_meta.csv`. Levels are optimistic everywhere, SMALL663 worst.
**Idea 835's finding applies:** every panel's binding drawdown is 2020, so "aggregation pays in
drawdown" rests heavily on one episode; this run did not re-run the episode-deletion leg.
**Tie convention:** 10 of 36 rule-8 picks sit in an IS-Sharpe tie (up to 7-way; all are AGG/HYB cells
in families whose breadth rarely crosses the low triggers, so several θ are the same book); the
grid-order convention decides them, per idea 846.
