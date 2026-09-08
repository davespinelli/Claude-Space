# Idea 235 — is-selection-beats-do-nothing-just-a-rung-artefact (cloud, 2026-09-08)

**Verdict: SPLIT — the queue's hypothesis is CONFIRMED on the rung and the published sentence is
KILLED at PROTOCOL's own 10 bps. "Selection beats do-nothing" is a quantity that is NEGATIVE at
zero cost, crosses zero between 5 and 15 bps, is bought by turnover to within 0.0012 of Sharpe,
and at 10 bps is a coin flip live (6/12, sign p 1.000) whose archive SIGN FLIPS with the
weighting convention. What survives is the weaker true sentence: selection beats a RANDOM arm of
the same grid — it does not beat the grid's middle arm.**

Script: `2026-09-08_is-selection-beats-do-nothing-just-a-rung-artefact_cloud.py`
Console: `..._cloud.console.txt` · Data: `.census.csv` `.rungcurve.csv` `.decomp.csv`
`.grid.csv` `.walkforward.csv` `.keep.csv`

Two tuned parameters, both fully reported: **p1 = COMPARAND** (what "not choosing" means:
MEDIAN arm of the swept grid, or RANDOM = mean over arms), **p2 = RUNG** the claim is read at
(every rung the record quotes: 0, 5, 10, 15, 20, 25, 30, 50 bps). The oracle is reported as a
ceiling, never as a comparand choice.

Corpus: **1,844 CSVs scanned, 58 usable, 5,202 cells, 12,455 rung-readings, 28 dial columns**;
turnover committed on 90.2% of readings. A claim is re-read exactly as the record makes it —
pick = argmax `IS_Sharpe` at that rung, `OOS_Sharpe` read once.

## 1. The premium is monotone in the rung, and negative at zero cost

| rung | cells | files | cell-wtd vs MEDIAN | win | sign p | **file-wtd vs MEDIAN** | win | sign p | file-wtd vs RANDOM | win | sign p |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 771 | 24 | **−0.0074** | 0.41 | 0.0000 | **−0.0032** | 0.38 | 0.221 | +0.0172 | 0.67 | 0.103 |
| 5 | 338 | 14 | −0.0008 | 0.48 | 0.518 | −0.0020 | 0.54 | 0.782 | +0.0425 | 0.86 | 0.008 |
| **10** | 5,202 | 58 | **−0.0153** | 0.42 | **0.0000** | **+0.0044** | 0.65 | **0.024** | +0.0340 | 0.71 | 0.002 |
| 15 | 336 | 13 | +0.0199 | 0.58 | 0.010 | +0.0123 | 0.92 | 0.004 | +0.0616 | 0.92 | 0.002 |
| 20 | 256 | 11 | +0.0340 | 0.59 | 0.010 | +0.0189 | 0.90 | 0.011 | +0.0769 | 0.91 | 0.007 |
| 25 | 5,194 | 57 | −0.0043 | 0.54 | 0.0000 | +0.0179 | 0.62 | 0.061 | +0.0554 | 0.75 | 0.0001 |
| 30 | 212 | 8 | +0.0619 | 0.66 | 0.0000 | +0.0403 | 0.88 | 0.034 | +0.0798 | 0.88 | 0.034 |
| 50 | 110 | 5 | +0.1317 | 0.78 | 0.0000 | +0.1891 | 0.80 | 0.180 | +0.3267 | 0.80 | 0.180 |

Slope of the mean premium in the rung: **+0.003571 Sharpe/bp file-weighted (R² 0.790)**,
+0.002765 cell-weighted (R² 0.797), **+0.002951 live (R² 0.079 cell-by-cell)** — three
independent readings of the same tilt, ≈ +0.09 to +0.11 of Sharpe across a 0→30 bps span.

**The 10 bps row is the whole finding.** At PROTOCOL's own mandated rung the archive premium is
−0.0153 cell-weighted (p < 1e-4) and **+0.0044 file-weighted (p 0.024) — the sign flips with the
weighting convention**, because one file (`is-the-conditional-sleeve-anything-at-all_B.null.csv`,
a permutation corpus) commits 2,648 of the 5,202 cells. Both readings are reported; neither is
preferred. A premium whose sign depends on whether you weight by cell or by file, and whose
file-weighted magnitude is +0.004 of Sharpe, is not a result.

## 2. Live, PROTOCOL rule 8 — 12 (panel × dial) cells, IS 2009–2016, OOS 2017–2026 read once

| rung | pick | do-nothing | median arm | random arm | oracle | prem vs DN | random's own prem | selection-only | wins | sign p |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 0.9224 | 0.9503 | 0.9304 | 0.9072 | 1.0074 | **−0.0279** | −0.0431 | +0.0152 | 2/12 | **0.021** |
| 5 | 0.9042 | 0.9002 | 0.8871 | 0.8610 | 0.9634 | +0.0040 | −0.0392 | +0.0432 | 4/12 | 0.248 |
| **10** | 0.8656 | 0.8500 | 0.8438 | 0.8148 | 0.9238 | **+0.0156** | −0.0352 | +0.0509 | **6/12** | **1.000** |
| 15 | 0.8271 | 0.7998 | 0.8004 | 0.7685 | 0.8851 | +0.0273 | −0.0313 | +0.0586 | 8/12 | 0.248 |
| 20 | 0.7810 | 0.7496 | 0.7570 | 0.7222 | 0.8463 | +0.0314 | −0.0273 | +0.0587 | 10/12 | 0.021 |
| 25 | 0.7427 | 0.6993 | 0.7135 | 0.6760 | 0.8076 | +0.0434 | −0.0234 | +0.0667 | 10/12 | 0.021 |
| 30 | 0.7273 | 0.6491 | 0.6701 | 0.6297 | 0.7691 | **+0.0783** | −0.0194 | +0.0976 | 11/12 | 0.004 |

Idea 230's headline is reproduced in shape: the premium runs from **significantly negative at
0 bps to significantly positive at 30 bps and is an exact coin flip at 10 bps (6 of 12, p 1.000)**.

## 3. The mechanism: it is bought with turnover, and the mean is exact

The artefact's own prediction, with no free parameter — a premium earned purely by holding a
lower-turnover arm is `dSharpe(c) = (turn_DN − turn_pick)·c/1e4 / vol`:

* Over all 84 live cells: **predicted +0.0257 vs actual +0.0246, mean residual −0.0012 of
  Sharpe.** At 10 bps predicted +0.0143 vs actual +0.0156 (residual +0.0013); at 30 bps
  predicted +0.0700 vs actual +0.0783 (residual +0.0082, sign p 0.248). The turnover channel
  accounts for the entire mean premium; cell by cell it explains the level, not the cross-section
  (slope +0.643, R² 0.125).
* The chooser picks a **17.27/yr-turnover book where do-nothing runs 20.16/yr** (random arm
  18.51/yr). It is selecting cheapness, not names.
* The archive shows the same signature in the claim's own metadata: mean `dturn` (do-nothing
  minus pick) rises monotonically with the rung the claim was quoted at — **−1.30/yr at 0 bps,
  +0.00 at 10, +1.57 at 20, +2.20 at 30, +3.79 at 50** — and `premium ~ dturn·c` fits with
  R² 0.494 / 0.541 / 0.535 / 0.902 at 15 / 20 / 30 / 50 bps against R² 0.069 at 10 bps.

## 4. What survives — the falsifier partly holds

The queue's hypothesis required the random-arm null to carry the same rung tilt. **It does not.**
The archive's random arm has its own premium over the median arm of −0.0224 at 10 bps with slope
**−0.000943/bp — the opposite sign**; live it carries +0.000791/bp against the chooser's
+0.002951 (27%). So net of a random arm the chooser is positive at **every rung under both
weightings**: archive file-weighted +0.0340 at 10 bps (win 0.71, p 0.0016), live +0.0509.

**Choosing beats choosing at random. It does not beat the grid's middle arm at PROTOCOL's rung.**
That is the sentence the record should carry.

## 5. Rule 8 headline, benchmarks, and both KEEP paths

At 10 bps over the 12 cells: IS chooser **OOS Sharpe 0.8656, CAGR 17.58%, MaxDD −32.50%**;
do-nothing 0.8500 / 14.92% / −28.85%; random arm 0.8148 / 14.63%. Benchmarks OOS: **SPY 0.8820
(CAGR 15.45%, MaxDD −33.72%)** — the chooser does *not* clear SPY on OOS Sharpe; RULES v1 0.7471
(U56) / 0.5763 (B136) / 0.4923 (SMALL439); RULES v2 1.2851 / 1.1185 / 0.5680.

**4a 80 / 665** (U56 0/217, B136 44/224, SMALL439 36/224) · **4b 12 / 665, all on U56**; bars
DD 639, H2 404, OOS 378, H1 312, CAGR 198. These reproduce idea 453's Part B of the same
construction, run independently earlier today, exactly — an internal reproduction gate. The 12
are the already-PARKed `U56 N=40` / `V=0.30` arms. **No KEEP is claimed by this idea.** Best
full-sample Sharpe at 10 bps: U56 `V=5.0` 1.147 (4a DD, 4b DD), B136 `K=4` 1.057 (DD/DD),
SMALL439 `V=5.0` 0.749 (DD / H1,H2,OOS,DD).

SURVIVORSHIP: SMALL439 is current constituents of a sub-$2B screen with the 44 `max_1d_move ≥ 1.0`
tickers dropped from 483; its numbers are upper bounds and no verdict here rests on them.

## 6. What to do with it

Offered to Sunday review as a **reporting clause, not a rules change**: *every "selection beats
do-nothing" claim must be quoted with (a) the cost rung it was read at, (b) the same premium at
0 bps, and (c) the turnover difference between the picked and the comparand arm. At 10 bps the
premium is indistinguishable from zero and weighting-dependent; the defensible claim is against a
random arm, not against the incumbent.* Ideas 233 (does-turnover-level-predict-chooser-power) and
234 (re-read-single-rung-argmaxes-on-V1C-shaped-books) should be read under this clause; idea
233's regression is now half-answered — the chooser's value is a function of `dturn·c`, with the
turnover *difference*, not the turnover *level*, as the carrier.
