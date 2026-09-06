# Idea 278 — does v2's 2017-2026-only Sharpe edge have a regime name?

**Lane C, 2026-09-06.** Script `2026-09-06_does-v2s-2017-2026-only-Sharpe-edge-have-a-regime-name_C.py`,
console `…_C.console.txt`, grids `…_C_{grid,conditional,decomposition,reweight,channel,walkforward}.csv`.

**Verdict: ANSWERED — KILL of the regime hypothesis.** None of the three regime labels the
queue named (200d state, vol tercile, drawdown depth) accounts for the IS→OOS swing. One
by-product PARKs (see §6). No RULES change: 4a 0 of 108 rows, 4b 7 of 108 and none of them
is the rule-8 pick.

## 1. The gap being explained (reproduces the parent exactly)

u56 @10 bps, weekly, next-day execution, matched control = the CG rung whose *realised*
mean gross matches v2's 0.5328, i.e. g\*=0.55 (realised 0.5503); g\*_IS is also 0.55.

| | Sharpe IS 2009-16 | Sharpe OOS 2017-26 | full | CAGR | MaxDD |
|---|---|---|---|---|---|
| RULES v2 (live) | 1.1043 | 1.2851 | 1.2056 | 8.66% | -12.05% |
| CG g\*=0.55 | 1.1085 | 1.1359 | 1.1235 | 9.70% | -16.90% |
| **dSharpe (V2−CG)** | **−0.0043** | **+0.1492** | +0.0821 | | |

Swing **+0.1535**. (The parent's "+0.18" was quoted against CG g=1.00, the IS-argmax rung;
against the gross-matched rung the OOS edge is +0.1492. Same sign, same story.) On broad
B136 the same comparison is IS −0.0528 → OOS +0.0153, swing +0.0680. Every ladder rung
0.20–1.00 at 0 and 10 bps is in `…_grid.csv`; the un-gated ladder's Sharpe is flat to
0.0024 across the whole gross range, as idea 274 found.

## 2. The gate's *mechanics* are identical in both windows

v2's realised gross conditional on regime barely moves between windows (u56):
above200 0.5824 → 0.5922, below200 0.2745 → 0.2564, volHI 0.3952 → 0.3947,
volLO 0.6117 → 0.6188, dd0-5 0.5751 → 0.6085. The gate puts on the same exposure in the
same regimes in 2017-2026 as in 2009-2016. What changed is the *payoff* to doing so.

## 3. Shift-share of the mean-return gap: 92–97% is NOT composition

The OOS-minus-IS gap in mean d = r(V2) − r(CG g\*) is **+0.95 pp/yr** on u56
(+0.18 pp/yr on broad). Decomposed into MIX (window crash content) / BEHAVIOUR
(within-bucket conditional means) / INTERACTION:

| axis (u56) | gap pp/yr | MIX | BEHAVIOUR | INTERACTION |
|---|---|---|---|---|
| state200 | +0.954 | +0.074 (7.7%) | +0.961 (100.7%) | −0.080 |
| voltercile (IS cuts) | +0.954 | +0.069 (7.3%) | +0.827 (86.7%) | +0.057 |
| voltercile (FULL cuts) | +0.954 | +0.019 (2.0%) | +0.872 (91.4%) | +0.063 |
| ddbucket | +0.954 | +0.214 (22.4%) | +3.394 | −2.654 |

The ddbucket row is not usable: SPY's ≥20% bucket is 15.0% of IS days and 2.3% of OOS
days, so MIX and INTERACTION are large and offsetting — a shift-share instability, not a
finding. On the two stable axes the window's crash content buys 2–8% of the gap.

## 4. The Sharpe gap itself, reweighted (the direct test)

Reweighting OOS days so their bucket shares equal the IS shares — "OOS at IS crash
content" — does **not** shrink the edge:

| axis (u56) | IS dSharpe | OOS dSharpe | OOS at IS content | ESS kept |
|---|---|---|---|---|
| state200 | −0.0043 | +0.1492 | **+0.1603** | 99.9% |
| voltercile IS | −0.0043 | +0.1492 | **+0.1294** (13% of gap) | 99.2% |
| voltercile FULL | −0.0043 | +0.1492 | +0.1296 (13%) | 99.2% |
| ddbucket | −0.0043 | +0.1492 | +0.4622 | **57.9%** — discount it |

So regime composition explains **0% (state200) to 13% (vol terciles)** of the swing. Broad
agrees in direction (32% on vol terciles, −1% on state200). If the queue's hypothesis were
right this column would land near the IS value of −0.004; it does not.

## 5. What the edge actually is: a mean-return channel, and only on u56

Sharpe = mean/vol, so the swing has two possible sources. Counterfactuals:

| u56 | mean pp/yr V2 | mean pp/yr CG | d mean | vol V2 | vol CG | vol ratio | dSharpe |
|---|---|---|---|---|---|---|---|
| IS | 7.57 | 9.16 | −1.59 | 0.0686 | 0.0827 | 0.8294 | −0.0043 |
| OOS | 9.38 | 10.01 | −0.64 | 0.0730 | 0.0882 | 0.8275 | +0.1492 |

**v2 loses to the gross-matched control on mean return in both windows.** Its Sharpe comes
entirely from running at ~83% of the control's vol, and that ratio is unchanged
(0.8294 → 0.8275, −0.19 pp). Swapping OOS means onto IS vols reproduces **104.4%** of the
swing; swapping OOS vols onto IS means reproduces **1.7%**. On u56 the edge is a shrinking
mean-return *penalty*, not a better risk cut.

On broad the same decomposition runs the other way — MEAN 24.4%, VOL 76.9%, vol ratio
0.8089 → 0.7719 — and on broad the conditional drag is statistically significant in the
regime that dominates the sample (above200, 83% of days: −1.48 pp/yr IS at t −2.00,
−1.55 pp/yr OOS at t −2.09). **The channel does not replicate across panels**, which is what an unexplained
window statistic looks like. Idea 111 stands; the three regime labels do not resolve it.

## 6. Rule 8 and the KEEP paths — the regime-conditional arms lose the selection

Nine arms ("apply the gate only inside bucket b, hold constant gross 0.75 elsewhere"), all
reported at both rungs on both panels in `…_{panel}_{bps}bps_arms.csv`.

Walk-forward (IS 2009-2016 chooses, OOS read once), u56 @10 bps:

| selector | pick | IS Sharpe | OOS Sharpe |
|---|---|---|---|
| do-nothing V2 | RULES v2 | 1.1043 | **1.2851** |
| chooser over ALL arms + ladder | gate only in above200 | 1.1296 | 1.0301 |
| ARM IS-argmax ddbucket | gate only in dd0-5 | 1.1049 | 1.0536 |
| CG IS-argmax | CG g=1.00 | 1.1116 | 1.1353 |

The honest chooser gives up **−0.2550 of OOS Sharpe** against doing nothing (broad: −0.0179,
picking CG g=1.00 over v2's 1.1185). Selection-loses again.

**PARK (by-product):** `gate only in dd10-20` clears 4b on u56 at both rungs — 12.14% CAGR /
1.1605 Sharpe / −19.75% MaxDD, halves 1.1690/1.1528, OOS 1.2304, turnover 1.92x/yr, +0.0366
Sharpe and +0.0946 OOS over its own gross-matched rung (CG 0.70). It is PARK, not KEEP, for
three reasons: its IS Sharpe (1.0778) ranks it *below* both CG and the IS-argmax arm, so
rule 8 never picks it; its MaxDD clears the 4b bar by 0.5 pp (−19.75% vs the −20.23%
allowed); and on broad the same arm fails 4b on drawdown while a *different* bucket (dd20+,
armed on 15.0% of IS days but only 2.3% of OOS days — idea 247's coverage problem) is the
one that passes. Two panels, two different buckets, neither IS-selected.

**Census:** 4a 0 of 108 non-benchmark rows (v2 is hard to beat on drawdown by construction);
4b 7 of 108 — 3 un-gated CG rungs already PARKed by idea 274, plus the 4 arm rows above.
