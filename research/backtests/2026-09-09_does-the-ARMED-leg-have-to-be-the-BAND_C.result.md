# Idea 465 — does the ARMED leg have to be the BAND?  (lane C, 2026-09-09)

**VERDICT: ANSWERED — NO, and the answer is a CAUTION on idea 247's KEEP-candidate.
At the candidate's own operating point (U56, q = 0.80, 10 bps) the band supplies 8.5% of the
edge idea 247 published; 91.5% is DE-GROSSING IN HIGH VOL, and a book with no
cross-sectional gate at all reproduces it. No new book is promoted; RULES.md, scan.py,
bot.py and baseline.py untouched.**

Script: `research/backtests/2026-09-09_does-the-ARMED-leg-have-to-be-the-BAND_C.py`
Artefacts: `.grid.csv` (150 points), `.decomp.csv`, `.boot.csv`, `.walkforward.csv`,
`.console.txt`.

## What was priced

Idea 247's conditional book, with the ARMED leg — and only the armed leg — varied. Arming is
unchanged (ISFIX: θ = q-th quantile of SPY vol20 on 2009–2016 only, then frozen; θ = 0.2125
at q = 0.80 on U56, arming 15.55% of IS days and 16.44% of OOS days), so **every leg is armed
on exactly the same days.** Disarmed leg is EW_ALL at 0.75 for all arms.

| leg | definition |
|---|---|
| `BAND3DG` | RULES v2's 200d MA ±3% band with hysteresis — idea 247's incumbent (asserted identical to `baseline.rules_v2_weights`, gate G2) |
| `BAND6DG` | the same object at ±6% |
| `MA200DG` | plain 200d MA gate, no hysteresis (asserted equal to `px > ma` after warm-up, G6) |
| `ABSDG` | 12-month absolute momentum, `px_t > px_{t-252}` (the queue did not define "ABS-dg"; this is the definition used) |
| `GROSSCUT` | **no cross-sectional gate at all** — EW_ALL at the reduced nominal gross that matches BAND3DG's mean realised gross at the same q |

2 tuned parameters (leg, q ∈ {0.60, 0.70, 0.80, 0.90}). 3 panels × 2 rungs reported at every
level, never chosen. 25 arms × 3 panels × 2 rungs = **150 grid points, all reported**.
Gates G1–G6 all pass exactly (fast twin vs `engine.backtest` max|Δ| 1.7e-17; G5: the
GROSSCUT arm IS its own timed control, max|Δ returns| 4.1e-15).

## The decomposition (the point of the run)

Idea 247's +0.0975 is measured against a **static** control — one that differs from the arm
in two ways at once (it never times exposure AND never selects names). Splitting it with a
third book, `CTRL_TIMED` = EW_ALL de-grossed on the same armed days to the same mean realised
gross:

    total edge = timing edge + composition edge      (identity holds to 0.000e+00 on all 120 cells)

**Headline cell, U56, q = 0.80, 10 bps** (idea 247's candidate and its four rivals; matched
gross to 9.7e-11):

| arm | CAGR | Sharpe | MaxDD | H1/H2 | gross | armed gross | static ctrl | timed ctrl | total | timing | composition |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `BAND3DG@0.80` (incumbent) | 11.05% | 1.2201 | −15.49% | 1.348/1.110 | 0.6803 | 0.3422 | 1.1226 | 1.2118 | **+0.0975** | **+0.0891 (91.5%)** | **+0.0083 (8.5%)** |
| `BAND6DG@0.80` | 10.89% | 1.1917 | −15.89% | 1.334/1.071 | 0.6787 | 0.3344 | 1.1226 | 1.2116 | +0.0691 | +0.0890 | −0.0199 |
| `MA200DG@0.80` | 10.92% | 1.2133 | −16.06% | 1.340/1.104 | 0.6804 | 0.3407 | 1.1226 | 1.2118 | +0.0907 | +0.0891 | +0.0015 |
| `ABSDG@0.80` | 10.78% | 1.1256 | −16.34% | 1.206/1.057 | 0.6945 | 0.4259 | 1.1227 | 1.2071 | +0.0029 | +0.0844 | −0.0815 |
| `GROSSCUT@0.80` (no gate) | **11.18%** | 1.2118 | **−15.04%** | 1.383/1.061 | 0.6803 | 0.3522 | 1.1226 | 1.2118 | +0.0891 | +0.0891 | −0.0000 |

The gateless book earns **91.5% of the published edge, with 0.13 pp more CAGR and 0.45 pp
less drawdown**, and clears 4b at both rungs. The band buys +0.0083 of Sharpe over it.

**Pooled over 24 cells per leg (3 panels × 4 q × 2 rungs):**

| leg | total | timing | composition | composition > 0 |
|---|---|---|---|---|
| BAND3DG | +0.0150 | +0.0039 | +0.0111 | 14/24 |
| BAND6DG | +0.0096 | +0.0035 | +0.0061 | 12/24 |
| MA200DG | +0.0079 | +0.0048 | +0.0031 | 9/24 |
| ABSDG | −0.0498 | +0.0089 | **−0.0587** | **0/24** |
| GROSSCUT | +0.0039 | +0.0039 | −0.0000 | 2/24 (identity) |

Timing share of the total edge, on the 55 gate-leg cells with a positive total: **median
104.5%, ≥50% in 42/55, ≥90% in 35/55.** (No pooled ratio is quoted — the denominator changes
sign across panels.)

**The strongest single number in the run:** of the 39 grid points that clear 4b, **38 beat
their STATIC control and only 5 beat their TIMED control** — and 2 of those 5 are the
GROSSCUT identity at machine zero, so **3 of 39 survive**, all on U56, two of them idea 247's
own `BAND3DG@0.80` (+0.0083 at 10 bps, +0.0077 at 25). "Beats its matched-gross control" is
almost entirely a statement about the STATIC comparand.

**The band is not always decorative — it is decorative AT q = 0.80.** At q = 0.60 and 0.70 on
U56 the composition edge is +0.1023 and +0.0454 and TIMING is near zero or negative
(−0.0076, +0.0711); those arms fail 4b on the CAGR floor. The candidate's own operating point
is the one where the band contributes least.

## Uncertainty

Block bootstrap (2000 draws, 21-day blocks, seed 465) of the annualised Sharpe of the daily
return DIFFERENCE, U56 q = 0.80 @ 10 bps: `BAND3DG − timed ctrl` point −0.0589, 90% CI
[−0.396, +0.282], P(>0) 0.385; `BAND3DG − static ctrl` point −0.1787, CI [−0.484, +0.121],
P(>0) 0.160. **No contrast in the headline cell is distinguishable from zero**, and both
point estimates are negative because the arm gives up return: its Sharpe advantage is a
risk-reduction effect, not an excess-return one.

## Rule 8 (leg and q chosen on IS ≤ 2016-12-31; 2017– read once; OOS controls IS-matched)

| panel | bps | IS pick | IS margin over 2nd | OOS CAGR | OOS Sharpe | OOS MaxDD | OOS 4b |
|---|---|---|---|---|---|---|---|
| U56 | 10 | `GROSSCUT@0.80` | +0.0413 over BAND3DG@0.80 | 10.83% | 1.1594 | −15.04% | **PASS** |
| U56 | 25 | `GROSSCUT@0.80` | +0.0450 | 10.50% | 1.1267 | −15.48% | fail (CAGR floor by 0.27 pp) |
| B136 | 10 | `GROSSCUT@0.80` | +0.0387 | 10.67% | 1.1370 | −15.67% | fail |
| B136 | 25 | `GROSSCUT@0.80` | +0.0420 | 10.33% | 1.1037 | −15.74% | fail |
| SMALL439 | 10 | `GROSSCUT@0.90` | +0.0066 | 6.97% | 0.5510 | −26.71% | fail |
| SMALL439 | 25 | `GROSSCUT@0.90` | +0.0078 | 6.46% | 0.5170 | −27.38% | fail |

**The chooser picks the gateless book in 6 of 6 cells** and never a gate leg. It is wrong to
do so out of sample on U56: the incumbent `BAND3DG@0.80` reads **11.19% / 1.2077 / −15.49%**
OOS at 10 bps against the pick's 1.1594, an IS→OOS flip on an IS margin of 0.041. Read once
in every cell, the incumbent's OOS composition edge (against its IS-matched timed control) is
**+0.0534 / +0.0568 on U56**, +0.0262 / +0.0294 on B136 and **−0.013 / −0.015 on SMALL439**;
its OOS timing edge is +0.021 / −0.003 (U56) and −0.149 / −0.173 (SMALL439). SPY OOS 15.38% /
0.8786 / −33.72%. **4a: 0 of 150** — no arm beats the live RULES v2 book on both halves.

## What this changes

Idea 247's memo point 6 says the candidate "beats its own matched-realised-gross control by
+0.0975 Sharpe … This is not idea 244's gross channel." That is true of the STATIC gross
channel and **false of the timed one**: against a control that de-grosses on the same days to
the same exposure, the margin is **+0.0083 full sample** (+0.0534 OOS at 10 bps). A Sunday
review that adopts the candidate is adopting **vol-timed de-grossing**, which the band merely
implements; the same exposure path with no band clears 4b full sample on U56 at both rungs
and misses the OOS CAGR floor at 25 bps by 0.27 pp. The candidate's 4b pass and its published
levels are unchanged by this run — only the mechanism attribution is.

SURVIVORSHIP: B136 and SMALL439 are current-constituent lists, so their levels are biased
upward; U56 is the fixed ETF/mega-cap list and the least biased. Only within-panel
arm-minus-control contrasts are load-bearing here.
