# Idea 1624 (lane C, 2026-09-20) — is the FILTER-vs-DEGROSS DRAWDOWN GAP bigger than its OWN PAIRED SE?

**Verdict: PARK the finding, KILL the book.** The drawdown gap is NOT uniformly inside its noise
— but it is not 30 of 33 either. It is **one effect at two adjacent rungs of one family**, and it
buys no adoptable book on either KEEP path.

## The question and the pre-registration

Idea 1617 ran every eligibility filter the record owns (MAXVOL / BAND / RANKCUT, 11 rungs x 3
panels) against a constant de-gross of the UNFILTERED book matched on **realised** mean gross, and
found the filter shallower at **30 of 33 cells, mean dMaxDD +3.67 pp**. That drawdown gap is the
only axis on which the filter family beat the de-gross. Idea 1511 measured a paired circular-block
SE of a MaxDD contrast at **2.93 pp**, so the queue read +3.67 pp as ~1.25 SE. This run bootstraps
the FILTER-minus-TWIN dMaxDD **directly at each of the 33 pairs** (identical block starts on both
legs, so the common tape cancels) instead of borrowing one number from another cell.

Pre-registered before the run: *if NO cell reaches |t| > 2 the axis is inside its own noise and the
family can be retired; if some do, the retirement is partial and the run must say which.*

## Answer

**8 of 33 cells reach |t| > 2 at the idea's own rung (LB = 65, 10 bps), 8 of 33 OOS, and the same
8 cells both times. All 8 are positive; 0 of 33 reach |t| > 2 in the negative direction.**

| window | cost | LB | \|t\|>2 | mean dMaxDD | mean SE | mean t | max \|t\| |
|---|---|---|---|---|---|---|---|
| FULL | 0 | 65 | 8 of 33 | +3.79% | 2.29% | +1.43 | 2.53 |
| FULL | 10 | 21 | 7 of 33 | +3.67% | 2.48% | +1.28 | 2.34 |
| FULL | 10 | **65** | **8 of 33** | +3.67% | 2.33% | +1.36 | 2.51 |
| FULL | 10 | 126 | 12 of 33 | +3.67% | 2.21% | +1.50 | 2.57 |
| FULL | 25 | 65 | 5 of 33 | +3.48% | 2.42% | +1.26 | 2.48 |
| FULL | 50 | 65 | 5 of 33 | +3.20% | 2.62% | +1.12 | 2.44 |
| OOS | 0 | 65 | 8 of 33 | +4.20% | 2.39% | +1.48 | 2.56 |
| OOS | 10 | 21 | 7 of 33 | +4.09% | 2.58% | +1.34 | 2.19 |
| OOS | 10 | **65** | **8 of 33** | +4.09% | 2.41% | +1.42 | 2.55 |
| OOS | 10 | 126 | 12 of 33 | +4.09% | 2.29% | +1.54 | 2.72 |
| OOS | 25 | 65 | 8 of 33 | +3.90% | 2.47% | +1.32 | 2.53 |
| OOS | 50 | 65 | 5 of 33 | +3.62% | 2.61% | +1.19 | 2.49 |

Every grid point is in `...boot.csv` (396 rows). Note the block-length dial is not neutral: LB 126
reads 12 of 33 where LB 21 reads 7, so **any published count of this kind must name its LB**.

## Four things the record should take from this

**1. The borrowed 2.93 pp SE was wrong in both directions.** The per-cell paired SE measured here
runs **0.65% .. 4.35%** — a factor of 6.7. The mean gap is **1.57 SE** against this run's own mean
SE (2.33%), not the 1.25 the queue computed. But the mean is the wrong statistic anyway: the cells
with the big gaps also have the big SEs, and the cells with tiny SEs (RANKCUT, 0.65-1.50%) have
essentially no gap.

**2. The 30-of-33 sign count is worth ~2 observations, not 33.** Naive binomial p = 1.4e-06. But
the mean pairwise correlation of the 11 within-panel cells' bootstrap dMaxDD draws is **+0.513 /
+0.564 / +0.544** (U56 / B136 / SMALL), giving **n_eff ~ 1.80 of 33**. The 11 rungs of a panel are
nested filters on one tape, and U56 ∩ B136 = 55 of 56 names. 30 of 33 is one sign, seen repeatedly.

**3. The effect that survives is the TIGHT VOL CEILING, and only that.** By family, at LB 65 /
10 bps / FULL:

| family | positive | mean dMaxDD | max \|t\| |
|---|---|---|---|
| MAXVOL | 12 of 12 | +4.95% | 2.51 |
| BAND | 12 of 12 | +5.00% | 2.18 |
| RANKCUT | 6 of 9 | **+0.19%** | 1.49 |

The cells significant at **every** block length AND **every** cost rung are the same core:
**U56 MAXVOL 0.45 / 0.60 and B136 MAXVOL 0.45 / 0.60** (B136 BAND 0.03 clears the cost ladder but
not the LB ladder; SMALL MAXVOL 0.60 clears the LB ladder but not the cost ladder). The loose
rungs die monotonically — U56 MAXVOL 0.80 t = +1.60, MAXVOL 1.00 t = +1.59 — which is the right
shape for a real effect, not for noise. **RANKCUT is retired outright**: mean gap +0.19 pp, 0 of 9
cells anywhere near the bar, at any dial point.

**4. Of the four cells that clear 4b FULL, three own a significant gap and one does not.**

| cell | MaxDD | 4b DD cap | margin | twin MaxDD | dMaxDD | SE | t | |
|---|---|---|---|---|---|---|---|---|
| U56 MAXVOL 0.60 | −16.88% | −20.23% | +3.35% | −21.69% | +4.81% | 2.21% | **+2.17** | significant |
| U56 MAXVOL 0.80 | −18.87% | −20.23% | +1.36% | −22.22% | +3.35% | 2.10% | +1.60 | **inside its own noise** |
| B136 MAXVOL 0.45 | −15.51% | −20.23% | +4.72% | −23.34% | +7.83% | 3.12% | **+2.51** | significant |
| B136 MAXVOL 0.60 | −18.70% | −20.23% | +1.53% | −24.55% | +5.85% | 2.64% | **+2.22** | significant |

**A correction to the queue's own premise.** Idea 1624 says "3 cells clear 4b where 0 twins do".
Idea 1617's committed `grid.csv` has **4** cells clearing 4b FULL at 10 bps (the fourth is U56
MAXVOL 0.80); **3** is the count that clears 4b FULL *and* OOS. The twin count is 0 either way.
This run reproduces 1617's dMaxDD, odMaxDD and dSharpe at all 144 rows to **< 1e-12** (G2/G2b/G2c),
so the contrast being tested is byte-identical to the one 1617 published.

## The capital arm: the filter family is still not adoptable (rule 8)

Parameters chosen on 2009-2016 **only**, 2017-2026 read once:

| panel | chooser | pick | OOS CAGR / Sharpe / MaxDD | SPY OOS | RULES v2 OOS | 4b | 4a |
|---|---|---|---|---|---|---|---|
| U56 | C_SHARPE (max IS Sharpe) | RANKCUT 0.75 | 10.43% / 1.1418 / −16.26% | 15.26% / 0.8738 / −33.72% | 9.46% / 1.2769 / −12.05% | fail | fail |
| U56 | C_DDT (max IS dMaxDD t) | MAXVOL 1.00 | 12.91% / 1.1148 / −20.93% | " | " | fail | fail |
| U56 | C_BASE (no filter) | BASE | 13.67% / 1.1268 / −22.53% | " | " | fail | fail |
| B136 | C_SHARPE | MAXVOL 0.45 | 10.64% / 1.1401 / −15.51% | 15.26% / 0.8739 / −33.72% | 7.85% / 1.1019 / −12.24% | fail | fail |
| B136 | C_DDT | MAXVOL 1.00 | 12.78% / 1.0751 / −23.68% | " | " | fail | fail |
| B136 | C_BASE | BASE | 13.70% / 1.0872 / −25.37% | " | " | fail | fail |
| SMALL | C_SHARPE | MAXVOL 0.45 | 1.96% / 0.2783 / −16.75% | 15.26% / 0.8738 / −33.72% | 4.41% / 0.6473 / −12.48% | fail | fail |
| SMALL | C_DDT | MAXVOL 0.45 | 1.96% / 0.2783 / −16.75% | " | " | fail | fail |
| SMALL | C_BASE | BASE | 9.02% / 0.5953 / −35.01% | " | " | fail | fail |

**0 of 9 picks clear 4b OOS; 0 of 9 clear 4a OOS.** Pooled OOS Sharpe: C_SHARPE **0.8534**, C_DDT
**0.8227**, no filter at all **0.9365** — choosing a filter on IS rows costs **−0.083 / −0.114** of
pooled OOS Sharpe, reproducing 1617's −0.0831. The idea's own chooser (pick the cell whose IS
dMaxDD carries the largest t) is the *worse* of the two, and on U56/B136 it lands on **MAXVOL 1.00**
— the loosest rung, i.e. the IS t-stat does not even select the cells whose gap is significant on
the full sample. Both KEEP paths over the whole grid at 10 bps: **4a — FILTER 0 of 33, TWIN 0 of 33;
4b FULL — FILTER 4 of 33, TWIN 0 of 33; 4b OOS — FILTER 4 of 33, TWIN 0 of 33.**

## Honest limits

1. **A block bootstrap of MaxDD is a crude yardstick.** MaxDD is the most path-dependent statistic
   the record uses and a resampled block path is not the tape's path. This run deliberately does not
   invent a better estimator — it uses the one idea 1511 committed to, so the answer is commensurable
   with the record. The LB ladder (7 / 8 / 12 of 33 at LB 21 / 65 / 126) is the honest width of that
   choice, and it is wider than the effect.
2. **|t| > 2 on a bootstrap SE is not a p-value**, and 33 cells with n_eff ~1.8 admit no multiplicity
   correction worth writing down. Read "8 of 33" as "the tight-MAXVOL corner and nothing else".
3. **Survivorship (rule 9).** U56 / B136 are current-constituent lists and SMALL a current sub-$2B
   screen carried back to 2010. The headline is a within-panel, same-names, same-days, same-realised-
   exposure contrast, so it is first-order immune; the 4b pass counts and every CAGR level are not.
4. All 17 gates pass (G0-G8), including exact reproduction of idea 1617's committed contrast.

## Files

`2026-09-20_filter-vs-degross-dd-paired-se_C.py` (34 s, deterministic, offline),
`.boot.csv` (396 bootstrap rows — every grid point), `.grid.csv` (144 book rows),
`.walkforward.csv` (9 rule-8 picks), `.gates.csv` (17), `.log.txt`.
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are unmodified.
