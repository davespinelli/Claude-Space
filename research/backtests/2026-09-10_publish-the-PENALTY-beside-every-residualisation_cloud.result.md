# Idea 496 — publish the PENALTY beside every residualisation (cloud, 2026-09-10)

**CROSS-LANE NOTE.** Lane B ran the same queue idea the same day and independently
(`2026-09-10_publish-the-PENALTY-beside-every-residualisation_B.py`), counting *fitting files*:
6 of 109 penalise at all, 7 of 74 residualisation CSVs carry a penalty column, and stability is
**100% at or below the record's own widest p/n (0.0370) and 0% at p/n > 0.5**. This run counts
*artefacts carrying a partial statistic* instead, and reaches the same verdict by a different
route — so the two censuses disagree on population and agree on the answer. Where this run adds
something is the **mechanism** behind lane B's p/n split (§B) and the **price** of the dial (§C).
The two runs share only idea 483's construction; neither read the other's numbers before running.

**PREMISE CONFIRMED, and priced. No KEEP, no book promoted, no RULES change; RULES.md,
PROTOCOL.md, scan.py, bot.py and baseline.py untouched.** Two tuned parameters and no more
(PENALTY ∈ {1e-3, 1e-2, 1e-1, 1, 10, 100}, PANEL ∈ {U56, B136, SMALL439}); fold count K,
control width, target, cost rung and sample half are reported axes, never chosen. Every grid
point written to disk.

## Gates

* **G1** `fast_backtest` vs `engine.backtest` on the read window: returns **0.000e+00**,
  turnover **0.000e+00**.
* **G2** exact cost re-rung `r(c) = r(10bps) + turnover·(10−c)/1e4` against a live re-run at
  0/10/25 bps: **6.939e-18**.
* **G3** idea 483's committed grid re-derived, 144/144 rows joined on (panel, width, lam, K)
  over 9 published columns. **Reported split per panel**, following the record's own
  G2a/G2b precedent, because two of the three price files are frozen and one is live:
  **B136 4.441e-16** and **SMALL439 2.220e-16** — the machinery is idea 483's exactly — and
  **U56 5.457e-02**, which is `data/prices.csv` having gained trading days since idea 483 ran.
  Reported, not waived; it moves no conclusion below, all of which are B136/U56 contrasts read
  off identical books within this run.
* **G4** the queue's own headline reproduces: B136 WIDE `survive_insample` runs
  **0.0199 → 0.9587** across lam 1e-3..100, spread **0.9388** (the queue quotes 0.020 → 0.959).

## A. The census — the dial is unpublished, and mostly unrecoverable

3,111 committed CSV artefacts scanned. A **residualisation** is defined as an artefact carrying
a partial statistic (a `pR2…` / `…_given_…` column) — a number produced by fitting a control and
reading what is left. A bare `kill`/`survive` flag is a survival claim, not a residualisation,
and is censused separately rather than scored.

| population | count |
|---|---|
| residualisation artefacts | **8** |
| … that publish a penalty column | **3** |
| … that publish **no** penalty (dial unrecoverable from the artefact) | **5** |
| kill/survive artefacts with no partial statistic (censused, **not** scored) | 23 |
| prose residualisation claims across 658 committed prose files | **76 lines** |
| … that name a penalty at all | **24 (31.6%)** |

**Roughly two of every three residualisation sentences in the record do not say what penalty
produced them**, and 5 of 8 artefacts do not carry the column either.

## B. The re-read — what moves, and what does not

**B1, committed rows, no re-fit.** 880 conclusions from the 3 penalty-publishing artefacts,
read at LOW = min(lam), MID = 1.0, HIGH = max(lam). Verdicts: `survive ≥ 0.5`, `kill < 0.5`,
sign for a partial R², and (significance, sign) for a t-stat.

* Overall penalty-stable: **733 / 880 = 83.3%**; median value spread 0.1539.
* By artefact: `name-level-fixed-effects_B` 296/336 (88.1%), `…IN-SAMPLE-fits_C` 373/432
  (86.3%), `…IN-SAMPLE-fits_cloud` **64/112 (57.1%)**.
* **By statistic is where the answer is.** The partial R² itself is essentially penalty-proof —
  `pR2_insample` **24/24**, `pR2_oof` **24/24**, `pR2_sd_given_F` **192/192**,
  `pR2_sd_given_W` 48/48 — while the record's *headline* residualisation statistic is not:
  `survive_insample` **4/16**, `survive_oof` **4/16**, `kill_insample` **4/16**,
  `kill_oof` **4/16**, i.e. **25% stable, spreads up to 0.9388**.

So the instability is not in the fit. It is in the **normalisation**: dividing the partial R² by
the raw R² and comparing to 0.5 turns a number that barely moves into a verdict that flips
three times in four.

**B2, fresh re-run** (idea 483's construction rebuilt: 200 equal-weight 20-name draw books per
panel, seeds 0..199, weekly, 10 bps, t+1; 144 grid points). 32 fresh conclusions,
**8 penalty-stable (25.0%)**, median spread 0.6357, max 0.9388. Width decides it: **WIDE**
controls are stable 0–1 of 4 per cell, **NARROW10** 2–4 of 4.

**The mechanism, published beside the verdict.** On B136 WIDE the control's own reproduction of
the signal, `R2_control_reproduces_sd_insample`, runs **0.9882 at lam ≤ 0.1 → 0.4543 at
lam 100**. At a small penalty the wide control *is* the signal, so it "kills" it by construction;
at a large penalty it cannot fit the signal, so the signal "survives". Both readings are
arithmetic about the penalty, not evidence about the characteristic.

**B3, the unrecoverable five** (residualisation artefacts publishing no penalty):
`2026-09-05_extend-the-three-degenerate-ladders-past-their-endpoints_C.picks.csv`,
`2026-09-06_dispersion-as-a-survivorship-detector_B.regressions.csv`,
`2026-09-06_is-within-stratum-CORR-a-SECTOR-concentration-proxy_C.fits.csv`,
`2026-09-07_is-the-SLEEVE-S-OWN-SHARPE-the-real-design-variable_cloud.bivariate.csv`,
`2026-09-08_is-cost-blind-choosing-worse-than-not-choosing-generally_C.rungcurve.csv`.

## C. Does the dial change what you would trade? Yes — by more than the method is worth

Control fitted on **2009–2016 only**, book Sharpe residualised, top-residual book held, OOS
2017–2026 read once (PROTOCOL rule 8).

* The penalty **changes the pick**: U56 **3 distinct books** across the 6 penalties (OOS Sharpe
  1.0666..1.1659, spread **0.0993**), B136 **3** (spread **0.0467**), SMALL439 **2**
  (0.4192..0.5823, spread **0.1631**).
* Residualising is worth almost nothing against simply taking the best in-sample book:
  mean OOS Sharpe **RESID +0.9028** vs **RAW_IS_SHARPE +0.8797** (**+0.0231**) vs
  **SD +0.7380**; RESID and RAW both beat RULES v2 OOS on 12 of 18 cells and SPY on 12 of 18.
* **The unpublished dial moves the answer by up to 0.163 OOS Sharpe; the entire residualisation
  method buys 0.023 over not residualising at all.** The dial is ~7× the method.

**Both KEEP paths.** Picks: **4a 0/54, 4b 0/54**. All 600 draw books at 0, 10 and 25 bps:
**4a 0/600, 4b 0/600, BOTH 0/600** — unfiltered random 20-name books carry no gate and no
sleeve, so this is the expected floor and is reported as such. Reference levels at 10 bps:
RULES v2 U56 8.63%/1.2021/−12.05%, B136 8.03%/1.1058/−12.24%, SMALL439 3.81%/0.5725/−14.68%;
SPY 15.15%/0.8855/−33.72%.

## Proposal filed for the Sunday review, NOT adopted here

A file that publishes a `survive`/`kill` residualisation must publish (a) the **penalty**, and
(b) the control's own **reproduction R²** of the signal it is controlling for. Without (b) the
reader cannot tell a killed signal from a control that simply memorised it. Where one number is
wanted, publish the **partial R²**, which is penalty-stable at **336/336** committed conclusions
here, rather than its ratio to the raw R², which is stable at only 238/368 overall and 16/64 on
the four `survive`/`kill` statistics the record actually quotes.

## Caveats

Survivorship (PROTOCOL 9): U56 and B136 are current-constituent lists; SMALL439 is the sub-$2B
screen with `data/small_meta.csv max_1d_move ≥ 1.0` dropped (idea 118, 44 tickers), also current
constituents and back-filled only to 2010. Every level above is optimistic and none is a
tradable estimate; what is meant to survive is the within-panel penalty contrast — same books,
same rows, same target, different lam — which a common level shift cannot move, and the census
arithmetic, which is a property of committed files. The census also picks up idea 658's
artefacts, written earlier in the same sprint; they land in the not-scored survival-claim bucket
and move no scored number. Ideas 38, 54 and 126 also apply.

Script `research/backtests/2026-09-10_publish-the-PENALTY-beside-every-residualisation_cloud.py`;
artefacts `.census.csv`, `.prose.csv`, `.reread.csv`, `.grid.csv`, `.keeppaths.csv`,
`.walkforward.csv`, `.console.txt`.
