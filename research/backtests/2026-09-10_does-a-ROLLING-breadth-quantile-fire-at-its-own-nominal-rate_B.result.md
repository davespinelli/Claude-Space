# Idea 399 — does a ROLLING breadth quantile fire at its own nominal rate? (lane B, 2026-09-10)

Script `2026-09-10_does-a-ROLLING-breadth-quantile-fire-at-its-own-nominal-rate_B.py`;
console/grid/fidelity/walkforward CSVs beside it. 10 bps, weekly book, t+1 execution,
committed caches only. Panels U56 / B136 / SMALL484 (idea 336's own three, truncated to the
common last date 2026-09-04). Tuned: **w** ∈ {252, 504, 756, 1260} and **depth** ∈ {0.25, 0.50,
1.00} — 12 points, all reported. **q is pre-registered at 0.12** (the middle of idea 336's own
set); q = 0.07 / 0.17 are a reported, never-selected-on robustness axis.

## Verdict: the ESTIMATOR diagnosis is CONFIRMED; idea 336's Q3 KILL SURVIVES it. No promotion.

### Gates (all pass, printed before any new number)
G1 derived cost rungs == live engine, 0.000e+00. G4 idea 84's EWALL U56 g0.85 @10bps
11.79% / 1.049 / −17.89% (published 11.8% / 1.05 / −17.9%). **G2 idea 336's committed EXP
fidelity triple reproduces to max |Δratio| 0.0043** across all nine (panel, q) cells. G3 the
firing-rate arithmetic agrees between two independent computations to 0.000e+00. Idea 336's Q3
headline also reproduces independently here: EXP vs its ungated parent, mean ΔSharpe over q at
10 bps = **+0.021 / +0.009 / −0.0004** (U56 / B136 / SMALL484) against its published
+0.020 / +0.008 / −0.001.

### Q1 — a rolling window DOES restore rate fidelity, and keeps cross-panel equality
Realised firing rate / nominal q, over armed days: **EXP median 0.207** (min 0.000, max 0.306)
→ **ROLL median 1.090** (min 0.759, max 1.765; mean 1.167). At the pre-registered q = 0.12 the
ratio is 1.34 / 1.47 / 1.38 at w=252, and **1.06 / 1.07 / 1.02 at w=756** and 1.00 / 1.00 / 0.85
at w=1260 (U56 / B136 / SMALL484) — a 2–3y window is unbiased to ~5%. The property idea 336
bought the quantile form for survives: cross-panel spread of the realised rate is **0.002–0.034**
for ROLL, against the ABSOLUTE form's published 0.193 / 0.413 / 0.686. The chooser's inert-arm
pathology is gone: the EXP chooser picks an arm firing on < 1% of days in **15 of 18** cells;
the ROLL chooser in **0 of 54**.

### Q2 — a live instrument, and it still earns nothing on the panel the idea was raised for
ROLL vs its ungated parent (do nothing), mean over the 12 (w, depth) points, 10 bps, g=0.75,
pre-registered q = 0.12: **U56 +0.068 Sharpe / +0.118 OOS**, **B136 +0.044 / +0.110**,
**SMALL484 −0.007 / −0.005** — and at q = 0.17 SMALL484 goes to **−0.007 / −0.024**. Fixing the
estimator roughly doubles the gate's value on the two large-cap panels (EXP's own numbers at the
same rung are +0.035 / +0.021 / +0.007), and moves SMALL484 from "exactly nothing" to "exactly
nothing, or slightly negative". **Idea 336's Q3 KILL was not an estimator artefact.**

### Q3 — rule 8 (w, depth on IS Sharpe ≤ 2016-12-31, 2017–2026 read once)
The chooser beats do-nothing **39 of 54** ROLL cells against EXP's **3 of 18** (mean vs_nogate
+0.054 at 10 bps vs −0.001), so the fixed estimator is genuinely more selectable. But on
SMALL484 at the pre-registered q the ROLL pick **loses to do-nothing in all 6 cells**
(−0.053 to −0.146); it wins there only at q = 0.07, an axis nothing is allowed to select.
Mean regret against the best OOS cell is 0.13–0.15 for ROLL against 0.08 for EXP — the fixed
instrument is more selectable *and* more dispersed.

### KEEP paths (PROTOCOL rule 4, every grid point reported)
**4a: 0 of 2430 gated points at 10 and 25 bps.** The only 4 passes are all at **0 bps**, all
B136, all at the never-selected q = 0.17. **4b at 10 bps: ROLL 208 of 648, of which 121 are
INHERITED** (the ungated parent passes too) and 87 earned — all on the two survivorship-inflated
large-cap panels, **0 on SMALL484**. Crucially, **none of the 87 earned passes is ever selected
by the walk-forward chooser**: the three rule-8 picks that pass 4b at 10 bps are all B136 g=0.75,
where the parent passes anyway. The best of them (B136 ROLL w756 q0.12 d0.50 W: 10.7% / 1.120 /
−13.1%, H 1.171/1.068, OOS 10.8% / **1.183** / −13.1%) clears the 4b **CAGR floor by 0.0005 pp** —
a tie, not a margin. Not a candidate; nothing is proposed and RULES is untouched.

### Cross-check against the cloud lane's independent same-day run of idea 399
Both lanes claimed this idea and wrote separate estimators. On the **18 shared (panel, family, w,
q) cells** (it used SMALL439 and w ∈ {252, 504, 1008, 2016}, so only U56/B136 at w ∈ {252, 504}
plus the EXP comparand overlap) the realised armed-day firing rates agree to **max |diff|
7.86e-04**. Both lanes reach the same verdict independently: the premise confirmed, idea 336's Q3
KILL surviving anyway, 4a passes only at zero cost (mine 4 of 2430, theirs 3 of 1296), and **no
uninherited 4b pass among any rule-8 pick at the protocol rung** in either run.

### Methodological byproduct, filed for the record
The **matched-mean-gross twin is not an independent second bar on the Sharpe leg.** Two
constructions were run at every one of 2430 points: SCALE (multiply the parent's return series by
mean(mult)) and REGROSS (idea 336's and the cloud lane's own — re-run `engine.backtest` with EW
weights at gross g·mean(mult)). SCALE is *exactly* Sharpe-degenerate because Sharpe is
scale-invariant, and **REGROSS differs from SCALE by at most 0.0012 Sharpe / 0.0025 OOS Sharpe /
0.0031 MaxDD** over all 2430 matched pairs — so "beats its matched-gross twin" and "beats do
nothing" are the same test to within 0.0012 Sharpe, and the two sign counts differ by at most 1 of
216 in every panel × rung cell. That is why idea 336's two Q3 rows (+0.020/+0.008/−0.001 vs parent,
+0.021/+0.009/+0.0001 vs twin) differ only in the fourth decimal, and it means the cloud lane's
"QROLL beats its twin 208/216" is a count of signs of differences whose *median magnitude* is
+0.0348 to +0.0569 on the large-cap panels but **+0.0043 on SMALL484** (124/216). Where the twin
IS a real second bar is the drawdown leg: ROLL beats it on MaxDD in 145/216 (B136), **210/216
(SMALL484)**, 138/216 (U56) at 10 bps, median ΔMaxDD +0.0155 / +0.0474 / +0.0066 — the gate is a
drawdown instrument, and on SMALL484 that is the only thing it is.

### Honesty flags
All three panels are current-constituent lists: CAGR and drawdown **levels** are optimistic and
the gated-vs-parent **contrasts** are the durable part. SMALL484 is idea 336's unfiltered small
cache, not the record's later SMALL439, so its levels are not comparable to post-2026-09-08 rows.
SMALL484 starts 2010-01-04, so its halves are not the same calendar halves as U56/B136's.
Nothing here is a KEEP; no memo with RULES wording is written because no path 4a or 4b candidate
survived rule 8.
