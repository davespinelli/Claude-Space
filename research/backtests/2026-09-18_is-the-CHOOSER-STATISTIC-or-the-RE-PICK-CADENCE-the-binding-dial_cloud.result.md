# Idea 1327 — is the CHOOSER STATISTIC or the RE-PICK CADENCE the binding dial?
*(2026-09-18, lane cloud, idea 2 of 2. Script: `2026-09-18_is-the-CHOOSER-STATISTIC-or-the-RE-PICK-CADENCE-the-binding-dial_cloud.py`, offline, deterministic, 28.7s.)*

**VERDICT: KILL for real-time (N, H) re-selection — and the queue's own premise is FALSIFIED.
The binding dial is the CHOOSER STATISTIC, not the cadence; the switch-turnover bill the queue
asked to be priced is ~0.1 pp/yr and frequently NEGATIVE.**

## What was run
1327 is filed as conditional on idea 1323, which is still Open and unrun, so this run **builds
1323's real-time book itself** (the cell STATISTIC=SHARPE x CADENCE=1y) rather than assuming
its result. Two dials only: **STATISTIC {SHARPE, CAGR, MAXDD, MARGIN4B}** x **CADENCE
{1y, 2y, 3y, 5y, NEVER}** — 20 stitched books per panel, all published, chosen over the
record's own 24-cell grid N {5,10,15,20,30,40} x H {21,63,126,252} at the incumbent's frozen
gross 0.60, weekly, 10 bps, t+1. The chooser reads an **expanding window of already-realised
returns ending at the re-pick date**; NEVER reproduces 1321's once-and-for-all pick.
**Switches are costed inside the runner** (drifted weights traded into the new cell's targets),
so the bill is paid by the equity curve. Comparands (not dials): the frozen anchor N=15/H=126,
GRIDAVG (the parked 24-cell equal-weight book), the unattainable full-sample ORACLE, RULES v2,
SPY. Gates G0-G3 PASS, including the grid containing its own anchor bit-for-bit and 1321's
N=5/H=63 pick failing 4b on U56 (15.22% / 1.0091 / -21.46%).

## 1. The binding dial is the STATISTIC, on all three panels
Two-way spread of OOS Sharpe over the 4x5 grid:

| panel | mean spread across STATISTICS | across CADENCES | ratio | SS share: stat / cadence / interaction | binding |
|---|---|---|---|---|---|
| U56 | **0.3665** | 0.1675 | 2.19x | 81.8% / 5.9% / 12.3% | **STATISTIC** |
| B136 | **0.1214** | 0.0505 | 2.40x | 81.2% / 7.4% / 11.4% | **STATISTIC** |
| SMALL663 | **0.6428** | 0.4304 | 1.49x | 68.6% / 11.2% / 20.1% | **STATISTIC** |

What you maximise decides the book; how often you revisit it is a second-order dial on every
panel tested. On B136 the SHARPE and CAGR choosers pick the *same* cell at every cadence, so
four of the five cadences are literally the same book.

## 2. The switch-turnover bill is not the story
Bill = cost drag (CAGR at 0 bps minus CAGR at 10 bps) minus the same statistic's drag at NEVER:

| panel | mean bill | range | mean dCAGR vs NEVER | switches / picks |
|---|---|---|---|---|
| U56 | **-0.096 pp/yr** | -0.268 .. +0.160 | -0.15 pp | 3.4 / 7.2 |
| B136 | **+0.012 pp/yr** | -0.015 .. +0.049 | +0.09 pp | 1.7 / 7.2 |
| SMALL663 | **-0.082 pp/yr** | -0.184 .. +0.110 | +3.80 pp | 2.8 / 7.2 |

Every bill is inside ±0.27 pp/yr and the average is **negative on two of three panels** —
re-picking often lands on a *lower*-turnover cell, so churn refunds cost rather than charging
it. "A cadence that churns" is not what breaks these books.

## 3. Real-time re-selection does not earn its keep
4a: **0 of 60**. 4b: **10 of 60 full sample and 10 of 60 OOS — all ten on U56**, and all ten
under a statistic aligned with how PROTOCOL grades (MAXDD 4/5, MARGIN4B 4/5, SHARPE 2/5,
CAGR 0/5). B136 and SMALL are 0 of 20 each. **Exactly one of the 60 beats the frozen anchor's
OOS Sharpe** (U56 MAXDD/3y, 14.43% / 1.1979 / -16.90% vs anchor 15.12% / 1.1947 / -16.38%, a
+0.0032 edge for -0.69 pp of CAGR) — and rule 8 does not pick it.

## 4. Rule 8 (pair chosen on warm-up..2016-12-31, 2017-2026 read ONCE)
| panel | rule-8 pick | OOS pick | OOS frozen anchor | OOS SPY | OOS RULES v2 | 4b OOS |
|---|---|---|---|---|---|---|
| U56 | MARGIN4B / 1y | 13.70% / 1.0455 / -16.90% | 15.12% / 1.1947 / -16.38% | 15.28% / 0.8747 / -33.72% | 9.47% / 1.2781 / -12.05% | PASS (-0.1492 Sharpe vs anchor) |
| B136 | SHARPE / 3y | 16.43% / 0.9095 / -23.42% | 14.11% / 1.0454 / -15.97% | 15.33% / 0.8769 / -33.72% | 7.88% / 1.1061 / -12.24% | **FAIL** (DD) |
| SMALL663 | CAGR / 1y | 21.30% / 1.0517 / **-38.27%** | 6.40% / 0.4653 / -33.35% | 15.33% / 0.8769 / -33.72% | 4.47% / 0.6518 / -12.18% | **FAIL** (DD) |

The chooser an implementer would actually have selected is **worse out of sample than doing
nothing** on every panel: -0.1492 (U56) and -0.1360 (B136) of OOS Sharpe against the frozen
anchor, and on SMALL it buys +14.90 pp of OOS CAGR by taking the drawdown to -38.27%, missing
the -20.23% cap by 18 pp. GRIDAVG (parked) remains the least-bad no-choice book: OOS
13.48% / 1.1732 / -16.62% on U56, still -0.0215 behind the frozen anchor.

**This also answers idea 1323's question in the negative**, on its own arm (SHARPE/1y): U56
12.48% / 1.0017 / -16.63% OOS, -0.1929 of OOS Sharpe against the frozen cell it replaces.

## What this is NOT
Not a RULES change (rule 6). Not a claim that the frozen anchor is *attainable* — it is the
incumbent because the record froze it; the honest reading is that **no real-time chooser tested
here recovers what freezing bought**, and the loss is in the objective, not the cadence.

**SURVIVORSHIP (rule 9).** U56 / B136 / SMALL663 are current-constituent lists; SMALL663 is a
sub-$2B screen carried back to 2010 — its 21.30% OOS CAGR under a CAGR chooser concentrating
into N=5 is exactly the number the bias inflates most, which is a further reason not to read
that cell as an opportunity.
