# Idea 314 — is the vol cap the real universe clause, and does a panel-scaled cap fix it?

**Lane B, 2026-09-09. Verdict: KILL of the volatility universe clause, in both the absolute and
the panel-scaled form. No KEEP candidate, no memo, no RULES change proposed.**

Script `2026-09-09_is-the-vol-cap-the-real-universe-clause-not-the-trend-leg_B.py`.
60 books = 3 panels (U56 / B136 / SMALL439) x 2 constructions (RESPREAD, DEGROSS) x 10 clause
settings. Trend leg (`px > MA200`) held fixed in every book; gross 0.75, weekly, 10 bps, lb 200.
Two tuned parameters only: **family** (ABS = `vol20 < c`; QTL = `vol20 <=` the day's
cross-sectional q-quantile over live names) and **level** (ABS c in 0.40/0.60/0.80/1.00/off;
QTL q in 0.40/0.60/0.80/1.00, plus q = the per-panel mean admission rate that ABS 0.60 realises).

## Gates — all three pass

* **G1** `fast_backtest` vs `engine.backtest`, 4 real books: max |diff| **1.39e-17**.
* **G2** 51R reproduces to **0.004 pp**: MA-only **-1.444** pp/yr / dSharpe **-0.0735**, VOL-only
  **-3.926** / **-0.2043** against published -1.44/-0.074 and -3.93/-0.204.
  **By-product worth recording:** that published pair is not a cell. It is the **mean over three
  cadences (W/M/Q) of a 0-bps CAGR column paired with a 10-bps Sharpe column**. The sign and the
  ordering hold at every cadence, but the headline **2.73x** ratio reads **1.54x** at the weekly
  cell this idea sweeps and **4.69x** at monthly. Cell-level: W -2.81 vs -4.32, M -0.66 vs -3.12,
  Q -0.86 vs -4.34.
* **G3** ABS(inf) == QTL(1.00) == the cap-OFF book to **0.000e+00**; the QTL clause fires at its
  nominal rate on every panel (max |realised - q| **0.0040**, bar 0.02).

## The four pre-registered hypotheses: **all four fail**

**H_LEVEL FAILS (5/6 arms monotone).** The one non-monotone arm is SMALL439/RESPREAD — 51R's own
cell — where **tightening** the cap from 0.60 to 0.40 *reduces* the damage (-2.52 -> -1.79 pp/yr at
0 bps; -2.81 -> -2.56 at 10 bps). The "level" reading is not self-consistent on the panel the claim
is about.

**H_SCALE FAILS on both legs.** At matched admission the panel-scaled clause recovers about a
third of the damage, not the damage: SMALL439 **-2.52 -> -1.63 pp/yr** (RESPREAD, gain +0.89 vs a
+1.0 bar; residual 1.63 vs a 1.0 bar) and **-1.88 -> -1.40** (DEGROSS). On U56 the panel-scaled
clause is *worse* than the absolute one (-1.10 -> -1.31).

**H_ORDER FAILS.** The cross-panel spread of the damage falls only from **1.64 to 1.20 pp**
(ratio 0.73, bar 0.50). The small-cap ordering is compressed by panel-scaling, not removed, so it
is not mainly a units artefact.

**H_CLAUSE FAILS, and this is the decisive result.** Over the 48 genuinely capped books
(ABS(inf) and QTL(1.00) are the control itself, by G3):

| | capped books beating their own cap-OFF control |
|---|---|
| Sharpe | **1 / 48** (best **+0.0032**, median -0.0849, worst -0.3241) |
| CAGR | **0 / 48** (best -0.08 pp, median -1.55 pp) |
| MaxDD (shallower) | 41 / 48 (median +2.08 pp, best +8.53 pp) |

So a volatility clause buys drawdown and pays for it in return, at an exchange rate that loses
Sharpe 47 times out of 48. **On SMALL439/RESPREAD — the cell the claim comes from — it does not
even buy that:** the cap *deepens* the drawdown in **5 of 8** settings (median dMaxDD **-0.86 pp**,
worst -2.73) while costing a median **-1.78 pp/yr** and **-0.088** of Sharpe. There the clause is
a pure loss on all three axes at once.

## Decomposition (the queue's actual mechanism question)

The matched-rate QTL clause is the ABS clause with its time variation removed, so
`ABS damage = SELECTION (matched-QTL) + TIMING (the rest)`, 0 bps, pp/yr:

| panel / con | TOTAL | SELECTION | TIMING |
|---|---|---|---|
| U56 RESPREAD | -1.10 | -1.31 | **+0.22** |
| U56 DEGROSS | -0.87 | -1.25 | **+0.38** |
| B136 RESPREAD | -0.89 | -0.43 | -0.46 |
| B136 DEGROSS | -0.56 | -0.57 | +0.01 |
| SMALL439 RESPREAD | **-2.52** | **-1.63** | **-0.89** |
| SMALL439 DEGROSS | -1.88 | -1.40 | -0.48 |

**Majority of the small-cap damage is plain cross-sectional selection (65% / 74%): the panel's
own highest-vol names earn their volatility.** The timing leg is the minority, and it changes sign
by panel — the absolute cap's crisis-firing mildly *helps* U56 and hurts SMALL439.

That timing leg is real and it is what the absolute number hides. ABS 0.60's admission rate is a
market-state variable, not a universe property: mean 0.959 / 0.964 / 0.781 on U56 / B136 /
SMALL439, but **0.863 / 0.850 / 0.547 in 2020** and 0.919 / 0.947 / **0.673 in 2022**, against
0.975 / 0.986 / 0.898 in 2013. The live RULES v1 clause was a **market-wide de-risking switch
wearing a universe clause's clothes** — idea 400's frequency-vs-level artefact, inside the traded
rules. A cross-sectional quantile is flat at q by construction (G3) and has no such leg.

## KEEP paths and rule 8

**4a 0/60. 4b 10/60. BOTH 0/60.** Binding 4b bars: CAGR 50, H2 27, OOS 26, H1 21, DD 11.
All 10 4b passes are RESPREAD books on U56/B136, and **in every arm where a capped book passes,
that arm's cap-OFF control passes too** — 4b never separates the clause from no clause.

**Rule 8 walk-forward** ((family, level) chosen on 2009-2016 IS Sharpe, 2017-2026 read once):
the IS pick beats its own cap-OFF control OOS in **0/6 arms**; mean OOS regret **+0.1439**. The
IS pick *is* the cap-OFF book in 3/6 arms and the OOS-best clause is the cap-OFF book in 4/6.
Where selection does choose a cap it is punished: SMALL439 picks ABS 0.400 and reads OOS Sharpe
**0.2418** (RESPREAD) and **0.0001** (DEGROSS) against the control's 0.5355 / 0.5507 — regret
0.294 and 0.551.

**WF-B (highest IS Sharpe over all 60 books): U56 / RESPREAD / cap OFF.**
Full 11.59% / **1.0948** (H1 1.1778 / H2 1.0347) / -18.62%; OOS 12.45% / **1.1138** / -18.62%.
SPY on that window 15.19% / 0.8871 / -33.72%, OOS 0.8786. RULES v2 (live) 8.64% / 1.2037 /
-12.05%, OOS 1.2817. **4a False; 4b PASS — and it is the CONTROL, not a treatment.**

## Why the 4b passes are not promoted (idea 311's standing proposal, applied)

Every book here is a gross scalar, so all 10 4b passers were re-run on a 17-point gross ladder
(0.20-1.00, step 0.05), everything else fixed. **Admissible bands: min 1, median 3, max 5 of 17
grid points** (all contiguous) — e.g. WF-B's own band is [0.70, 0.80], three points. Each pass is
a knife-edge placement of an un-tuned convention, exactly the pattern idea 311's census found in
98.1% of the record. Under that proposal these are PARK, never KEEP. No book is promoted.

## What this closes

RULES v2 (live since 2026-09-06) already dropped the `vol20 < 0.60` clause. This run says the
door stays shut and should not be reopened in panel-scaled form: **no volatility universe clause,
at any of eight levels in either family, on any of three panels, under either construction, beats
simply holding the trend leg alone.** The honest RULES form of a universe clause phrased in
volatility is: none.

**Survivorship:** SMALL439 and B136 are current constituents only (PROTOCOL 9). The bias is common
to each capped book and its own cap-OFF control, so it largely cancels out of the dCAGR/dSharpe
columns that carry the argument; it does not cancel out of the 4a/4b level columns, and a KILL of
the clause is strengthened by it.

Outputs: `.console.txt`, `.grid.csv` (60 books), `.g2.csv`, `.admission.csv`, `.byyear.csv`,
`.scale.csv`, `.decomp.csv`, `.ordering.csv`, `.keeppaths.csv`, `.walkforward.csv`,
`.gband.csv` (170 gross-ladder points).

Follow-ups proposed: 577, 578, 579 (see QUEUE.md).
