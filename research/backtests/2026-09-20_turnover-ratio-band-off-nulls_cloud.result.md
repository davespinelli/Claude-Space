# Idea 267 (lane cloud, 2026-09-20) — is the 1.2x-1.4x turnover-ratio band the rung-sensitivity boundary?

**VERDICT: ANSWERED / KILL — the band is a NULL-ARM ARTEFACT.** Pre-registered exactly as the
queue states it (R < 1.2 => breakeven `c*` > 25 bps; R > 1.4 => `c*` <= 25 bps), scored on 105
NON-NULL arm pairs where the two books differ in a real design dial, and re-scored on idea 262's
own committed null table. 6 of 6 gates pass, including idea 262's law
`c* = dS(0)*1e4/(T_x/v_x - T_y/v_y)` reproducing this run's breakevens at **rho = 1.0000, median
error 0.028 bps** over 32 flipping pairs — the arithmetic is intact; it is the BAND that is not.

## The four numbers
1. **V1 NOT TRIGGERED — off the nulls the high edge is a coin flip.** Of 105 within-family pairs
   (cadence D/W/M/Q on RULES v2 and v1, gross 0.25-1.00, 200d band 0.00-0.08, n = 3-15, vol scaler
   on/off; U56 / B136 / SMALL665), **56 are cost-relevant** (the faster arm wins at 0 bps; in the
   other 49 the SLOWER arm is already ahead at zero cost, so no positive-cost breakeven exists and
   the verdict is cost-invariant). On those 56: **R > 1.4 gives `c*` <= 25 bps on 18 of 37
   (0.486)** against the band's predicted 1.000, and R < 1.2 gives `c*` > 25 on 7 of 8 (0.875, on
   8 pairs only). Bar was 0.80 on both.
2. **V2 — the band does not even hold on the arms it was induced from.** On idea 262's committed
   `breakeven.csv` (1,176 null pairs, read from disk, not re-run), restricted to cost-relevant
   pairs: **R > 1.4 -> 183 of 183 (1.000)**, but **R < 1.2 -> 174 of 259 (0.672)**. The HIGH edge
   is exact on nulls and a coin flip off them; the LOW edge was never right anywhere.
3. **V3 NOT TRIGGERED — the DIRECTION survives, the SEPARATION does not.** `c*` still falls with
   R off the nulls (Spearman **-0.395**), but R classifies rung-sensitivity at **AUC 0.680** there
   against **0.940** on the nulls, and the best single threshold moves from **R >= 1.186**
   (balanced accuracy 0.870, nulls) to **R >= 1.988** (0.641, non-nulls). The ratio profile is
   monotone on nulls (P(sensitive) = 0.41 / 0.59 / 0.93 / 1.00 / 1.00 / 1.00 across
   [1,1.1) [1.1,1.2) [1.2,1.4) [1.4,2) [2,4) [4,inf)) and NON-monotone off them
   (0.00 / 0.25 / 0.46 / 0.33 / 0.44 / 0.86).
4. **V4 NOT TRIGGERED (rule 8) — and the deeper reason is that `c*` is not stable in time.** A
   threshold fitted on 2009-2016 pairs alone lands on R >= 2.257 (IS balanced accuracy 0.689) and
   classifies the 2017-2026 pairs at **0.694** (bar 0.70). The same pair's own rung-sensitivity
   agrees between the two windows on only **0.554 of 56 pairs** — barely better than a coin flip,
   which caps what ANY ratio rule can deliver.

## Why the two populations differ (mechanism, not speculation)
A null arm and its comparand hold the same names with the same gross and differ only in churn, so
`dS(0)` is near zero and the cost term dominates: `c*` is then almost a pure function of the
turnover gap, which is what idea 262 measured. A real design dial moves gross, name count or
eligibility at the same time as it moves turnover, so `dS(0)` is large and of either sign, and the
same R spans breakevens from 1 bp to never. The band is a measurement of the null construction,
not of the cost axis.

## Capital (V5, both KEEP paths, every arm x cost rung)
69 arms x 4 cost rungs. **1 of 69 arms clears 4b FULL+OOS at 10 bps** — U56 `v2 gross 1.00`
(band 0.03, weekly): 11.53% / 1.2008 / -15.91%, halves 1.2282 / 1.1798, OOS 12.67% / 1.2759 /
-15.91%, 2.35 turns/yr — against live RULES v2 U56 8.62% / 1.2010 / -12.05% (OOS 9.46% / 1.2766)
and SPY 15.12% / 0.8843 / -33.72% (OOS 15.26% / 0.8737). **0 of 69 clear 4a at any cost rung.**
Counts by cost: 4b FULL+OOS 4 / 1 / 1 / 0 of 69 at 0 / 10 / 25 / 50 bps. **NO NEW KEEP IS FILED:**
that cell is the live book's own GROSS dial, and the record already commits the gross ladder's
4b behaviour (the 2026-09-20 changelog's `band 0.08 / gross 1.00` IS-pick entry); this run
re-scores it, it does not discover it. Binding leg at 10 bps failures is L5_CAGR: of the 67 arms failing 4b FULL at 10 bps, 64 fail on it and 22 fail on it alone.

## What this cannot do (stated, not repaired)
Only 8 non-null cost-relevant pairs sit below R = 1.2, so the LOW edge's 0.875 off-nulls is an
8-pair estimate and no standard error is attached to it here (idea 2067's paired block bootstrap
is the machinery for that, and this run does not spend it). The six dial families are the ones the
queue names; they are not a random sample of the record's dials. Both tuned dials were laddered:
the ceiling {60, 200} bps changes nothing (identical shares), the statistic changes the verdict's
SIZE but not its direction (CAGR-basis shares 0.700 / 0.286 vs Sharpe's 0.875 / 0.486), so the
KILL is not a ceiling or statistic artefact. SURVIVORSHIP: U56 / B136 are current-constituent
lists and SMALL665 a current sub-$2B screen (54 tickers with `max_1d_move >= 1.0` dropped first);
every CAGR and drawdown LEVEL is optimistic and both 4b bars are easier here than on a
point-in-time panel. The band test itself is a within-panel comparison of two books on the same
names and tape, so it is first-order immune; the 4b pass counts are not.
