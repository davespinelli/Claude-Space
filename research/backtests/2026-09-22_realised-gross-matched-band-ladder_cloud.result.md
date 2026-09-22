# Idea 2203 — does the 4b VERDICT on the BAND LADDER survive a REALISED-GROSS-MATCHED comparand?

**Lane cloud, run 8, 2026-09-22.** Script:
`research/backtests/2026-09-22_realised-gross-matched-band-ladder_cloud.py`
(deterministic, offline, 7 of 7 gates PASS). Panels U56 (56) / B136 (136) / SMALL (665 names
after dropping 54 with `max_1d_move >= 1.0`), weekly, costs 0/10/25/50 bps, IS ..2016-12-31,
OOS 2017-01-01.. read once.

## Verdict: ANSWERED — and the premise is largely RETIRED. No KEEP, no new candidate.

**The filed premise was that nominal and realised gross "come apart", so the same `g` label
denotes different exposures. On the band family it does not come apart in the way that
matters: realised gross is EXACTLY PROPORTIONAL to nominal gross.**

1. **V1 — the gap is real but it is a PANEL constant, not a band effect and not a 41% number.**
   Realised mean gross sits **−29.0%** below nominal on U56 (bands 0.00–0.03), −31.4% / −32.3%
   at bands 0.05 / 0.08; **−29.1% to −29.8%** on B136; **−44.1% to −45.2%** on SMALL. The
   *panel* moves the shortfall by 16 pp; the *band* moves it by at most 3.3 pp (U56) and
   0.8 pp (B136). 2125's "41%" is between the large-cap and small-cap values and is a
   panel statement misread as a band statement.

2. **V7 — the re-parameterisation is an AFFINE RELABEL, not a new experiment.** At fixed
   (panel, band) the shortfall spread across the whole nominal ladder is **0.0301 pp (median),
   0.0376 pp (max)** — i.e. `R(b,g) = k(panel,band)·g` to four decimals. The realised axis
   therefore re-scales the nominal axis per band and **re-orders nothing**. Every cell keeps
   its rank; the mapping is a change of units.

3. **V2/V3 — the 4b COUNT nevertheless collapses, and the reason is TRUNCATION, not refutation.**
   At 10 bps, 4b (FULL and OOS) reads **6 passes on the nominal axis and 1 on the realised
   axis**; median band-set Jaccard **0.1000**. All **9** nominal 4b-FULL passes sit at
   **g = 1.00**, carrying realised gross **0.6773–0.7103**. The filed realised ladder's top
   rung **R\* = 0.75 is INFEASIBLE on 15 of 15 (panel, band) rows** at g ≤ 1.00 (no leverage),
   so its top *feasible* rung is 0.65 — **below every pass**. The realised ladder does not
   contradict the nominal passes; it does not reach them.

4. **V7 — the mechanism, stated plainly.** Across the whole gross ladder at fixed
   (panel, band, cost) the FULL-sample **Sharpe spread is 0.0006 (median) / 0.0021 (max)**
   while CAGR moves 5.14 pp and MaxDD 8.46 pp. Gross is Sharpe-neutral and moves return and
   drawdown together, so 4b on this ladder is decided by the **CAGR floor** (binds **66 of 75**
   nominal FAIL rows at 10 bps) with the **DD cap binding 0 of 75**. Any re-parameterisation of
   the exposure axis is therefore a statement about *where the axis stops*, nothing else.

5. **V5 — rule 8, OOS read once.** Both legal IS-only choosers pick band 0.08 at the top
   feasible rung on **both** axes and on all three panels. Paired over 24 (panel, cost, chooser)
   instances, re-parameterising costs **−0.0018 OOS Sharpe / −0.46 pp OOS CAGR** — inside the
   record's seed-noise floor. At 10 bps on U56: NOMINAL `b0.08_g1.00` → OOS 12.00% / 1.163 /
   −19.05%; REALISED `b0.08_R0.65` (g\* = 0.960) → OOS 11.51% / 1.163 / −18.32%; SPY OOS
   15.29% / 0.875 / −33.72%; live book OOS Sharpe 1.277. **4b-OOS Y on both, 4a-OOS N on both**
   (both lose to the live book's Sharpe). OOS rank of the pick is **25/25** (nominal) and
   **20/20** (realised): the chooser walks to the exposure ceiling, which is the worst OOS
   Sharpe cell, and only clears 4b because the CAGR floor rewards exposure.

6. **KEEP paths.** 4a FULL: **4 of 75** nominal, **2 of 52** realised. 4a OOS: 17 / 13.
   4b (FULL and OOS) at 10 bps: U56 5 → 1, B136 1 → 0, **SMALL 0 → 0 at every cost rung**.
   **No cell clears both paths. Nothing here is capital-worthy.**

7. **Cost ladder.** 4b (FULL and OOS): nominal 9 / 6 / 5 / 1 and realised 4 / 1 / 1 / 0 at
   0 / 10 / 25 / 50 bps; median Jaccard 0.500 / 0.100 / 0.125 / 0.000.

## What the record should take from this
The committed band × gross verdicts are **not** quoted in a dial the book does not carry — they
are quoted in a dial that is a *fixed multiple* of the one it carries, and the multiple is a
property of the panel. The honest correction is smaller than 2203 supposed: **every published
band × gross cell should state `k(panel, band)` beside `g`**, so `g = 1.00` on U56 reads as
realised 0.71 and on SMALL as realised 0.55. Cross-panel comparisons at matched *nominal* gross
are the ones that are wrong, by 16 pp of exposure; within-panel ladders are sound.

## Survivorship (PROTOCOL rule 9)
All three panels are current-constituent lists. SMALL is a screen of names sub-$2B **and still
listed today**, so every sub-$2B company delisted, acquired or taken to zero between 2010 and
2026 is absent; its CAGR is severely optimistic and its drawdown severely understated. SMALL is
used here only for a within-tape contrast of two parameterisations of the same book.
