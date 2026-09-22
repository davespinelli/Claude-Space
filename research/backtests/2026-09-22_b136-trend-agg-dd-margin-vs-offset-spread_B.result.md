# Idea 914 (lane B, 2026-09-22) — price the 0.70 pp DD MARGIN of B136 TREND/AGG th=0.20 g=0.75 against its OWN OFFSET SPREAD

**VERDICT: KILL of the idea-910 KEEP-candidate. The 4b pass is a WEEKDAY, and the weekday is
March 2020.** The margin is 0.70 pp; its own rebalance-offset spread is **4.18 pp — 6.0x the
margin**. The book clears 4b at **1 of 5** weekly offsets on FULL and **1 of 5** on OOS, at every
one of 4 cost rungs, and the one that passes is the published convention. Rule 8 makes it worse,
not better: the IS-only chooser picks the **worst** OOS offset.

Script: `research/backtests/2026-09-22_b136-trend-agg-dd-margin-vs-offset-spread_B.py`
Artefacts: `.console.txt`, `.grid.csv` (144 rows, every point), `.walkforward.csv`,
`.ddwindows.csv`, `.offsets.csv`, `.verdicts.json`

## The book (idea 910's memo, nothing re-tuned)
B136 (`research/universe_broad.json`), weekly, t+1, 10 bps. `band = baseline.band_state(px, 0.03)`;
`breadth(t) = #band / #priced`; if `breadth >= 0.20` hold every priced name at `0.75/#priced`,
else 100% cash. Reproduced within tape drift (G3): FULL **12.62% / 1.121 / −19.53%** against the
memo's 12.66% / 1.124 / −19.53%; OOS 11.81% / 1.054 / −19.53% against 11.89% / 1.060 / −19.53%.
The tape has grown 3 sessions since 2026-09-15, so exact equality was not the bar.

## Tuned parameters — exactly two, both named by the idea; all 144 grid points published
`offset d ∈ {0,1,2,3,4}` (rebalance d trading days before the week's last session; d=0 **is** the
published convention, gate G2 = 0 differing rows) × `cost ∈ {0,10,25,50}` bps.
Published-not-tuned: band 0.03, th 0.20, gross 0.75, W; panel {B136 primary, U56 replication};
construction {AGG the book, ENS the parameter-free 5-offset ensemble}.

## (A) B136 / AGG / 10 bps — the committed book at each of its five weekdays

| window | d | CAGR | Sharpe | MaxDD | H1 | H2 | DD margin | CAGR margin | 4b | 4a |
|---|---|---|---|---|---|---|---|---|---|---|
| FULL | **0** | 12.62% | 1.121 | **−19.53%** | 1.300 | 0.957 | **+0.70** | +2.03 | **PASS** | FAIL |
| FULL | 1 | 12.08% | 1.088 | −20.65% | 1.302 | 0.888 | −0.42 | +1.49 | FAIL | FAIL |
| FULL | 2 | 12.15% | 1.064 | −23.71% | 1.313 | 0.846 | −3.48 | +1.56 | FAIL | FAIL |
| FULL | 3 | 12.20% | 1.075 | −22.13% | 1.326 | 0.855 | −1.90 | +1.61 | FAIL | FAIL |
| FULL | 4 | 12.33% | 1.085 | −23.03% | 1.349 | 0.853 | −2.80 | +1.74 | FAIL | FAIL |
| OOS | **0** | 11.81% | 1.054 | **−19.53%** | 1.247 | 0.848 | **+0.70** | +1.13 | **PASS** | FAIL |
| OOS | 1 | 10.83% | 0.992 | −20.65% | 1.189 | 0.788 | −0.42 | +0.15 | FAIL | FAIL |
| OOS | 2 | 10.82% | 0.944 | −23.71% | 1.016 | 0.866 | −3.48 | +0.14 | FAIL | FAIL |
| OOS | 3 | 10.86% | 0.954 | −22.13% | 1.030 | 0.872 | −1.90 | +0.18 | FAIL | FAIL |
| OOS | 4 | 10.82% | 0.953 | −23.03% | 1.024 | 0.877 | −2.80 | +0.14 | FAIL | FAIL |

Comparands (same tape, 10 bps): RULES v2 B136 FULL 7.96% / 1.097 / −12.24% (OOS Sharpe 1.102);
SPY FULL 15.12% / 0.884 / −33.72% (OOS 15.33% / 0.874 / −33.72%). 4b DD bar = 0.60 × −33.72% =
−20.23%; 4b CAGR floor = 0.70 × 15.12% = 10.59%.

## (B) The pre-registered bars — five of six FAIL

- **B1 (THE QUESTION) FAIL.** MaxDD over the 5 offsets runs −23.71% .. −19.53% → **S_DD = 4.18 pp**
  against a margin of **0.70 pp**. `M > S_DD` is false by a factor of 6.0. Idea 806's standing
  criterion therefore convicts: *a date, not a book.* Same read OOS (4.18 vs 0.70, fails); IS is
  the one window where it survives (0.40 vs 0.62) — i.e. the defect is invisible in sample.
- **B1c (clip-free subset).** Restricting to the offsets with zero clipped weeks, {0,1,2}, the
  spread is **unchanged at 4.18 pp**. The verdict does not depend on the clipped offsets.
- **B2 FAIL.** The 4b DD leg alone holds at **1 of 5** offsets (FULL, 10 bps).
- **B3 FAIL.** All four 4b legs: **1 of 5** on FULL, **1 of 5** on OOS.
- **B4 FAIL.** At 0 / 10 / 25 / 50 bps the FULL count is 1 / 1 / 1 / 1 and the OOS count is
  1 / 1 / 1 / 1. Worst-offset FULL MaxDD runs −23.59% / −23.71% / −23.89% / −24.19% (all d=2).
  In sample the count is 5 / 5 / 5 / 5 at every rung — **the failure is entirely out of sample.**
- **B5 (RULE 8) FAIL, and this is the sharpest leg.** IS Sharpe by offset is **monotonically
  increasing in d** (1.2015 / 1.2033 / 1.2157 / 1.2276 / **1.2521**), so an IS-only chooser
  lands on **d = 4 — the worst OOS drawdown offset — at all 4 cost rungs and on both panels.**
  The walk-forward pick's OOS: B136 **10.82% / 0.953 / −23.03%** (DD margin −2.80 pp) vs RULES v2
  OOS Sharpe 1.102 and SPY OOS 15.33% / 0.874 / −33.72% → **4b FAIL, 4a FAIL**. U56 pick d=4:
  11.87% / 1.037 / −22.53% → 4b FAIL, 4a FAIL. **0 of 8 walk-forward cells clear either path.**
- **B6 PASS (the memo's own claim).** 4a fails at **0 of 60** B136/AGG grid points.

## (D0) Which date — the claim is literal, so the date is named
Every offset's full-sample MaxDD is the **same** 2020 episode, peak **2020-02-19** in all five:

| d | MaxDD | peak | trough | sessions |
|---|---|---|---|---|
| **0** | **−19.53%** | 2020-02-19 | **2020-03-12** | **16** |
| 1 | −20.65% | 2020-02-19 | 2020-04-21 | 43 |
| 2 | −23.71% | 2020-02-19 | 2020-04-21 | 43 |
| 3 | −22.13% | 2020-02-19 | 2020-03-16 | 18 |
| 4 | −23.03% | 2020-02-19 | 2020-04-21 | 43 |

Only the published weekday de-grosses early enough to end its decline on 2020-03-12; the other
four are carried into the April leg. The 0.70 pp margin is the width of that one scheduling
accident, and nothing else.

## (D) The candidate repair fails too
The parameter-free 5-offset equal-weight **ENSEMBLE** (hold 1/5 of NAV in each offset book — the
standard de-dating device, no free parameter) does **not** rescue the pass: B136 FULL
12.29% / 1.096 / **−21.02%** (DD margin −0.79 pp) → 4b FAIL; OOS 11.05% / 0.994 / −21.02% → 4b
FAIL. It passes 4b in sample at all four cost rungs and fails FULL and OOS at all four. U56 ENS:
FULL 12.09% / 1.095 / −22.47%, OOS 12.03% / 1.053 / −22.47% → 4b FAIL at every rung.

## (E) U56 replication (published, not tuned)
The same construction on U56 never had the pass to lose: FULL MaxDD −22.30% .. −23.14% across the
5 offsets, margin **−2.30 pp**, 4b FAIL at 0 of 5 offsets on FULL and OOS. Offset spread there is
only 0.84 pp — i.e. the 4.18 pp spread is a **B136** fact, which is the panel the candidate was
filed on.

## Gates — 4 of 5 PASS, and the failure is published rather than relaxed
G1 local runner ≡ `engine.backtest(freq='W')` max|d| **0.000e+00** over 4,706 rows, NaN masks
identical; G2 `offset_mask(idx,0)` ≡ `engine.rebalance_mask(idx,'W')`, **0** differing rows;
G3 memo reproduction within tape drift (ΔCAGR 0.045 / 0.084 pp, ΔSharpe 0.0034 / 0.0059, MaxDD
identical to 2 dp); G4a rebalance count 5 of 5 offsets at 52.24–52.29/yr; **G4b FAIL** — d=3 clips
2 weeks and d=4 clips 175 (a 4-session holiday week has no session 4 before its last; the mask
falls back to that week's first session). That clause fails **by construction**, is reported
rather than widened, and section B1c re-reads the headline without those offsets to the same
verdict. G5 comparands match `baseline`'s own rows (SPY MaxDD −33.72%).

## What this test cannot do (stated, not repaired)
B136 and U56 are **current-constituent** lists, so every absolute CAGR and drawdown level here is
survivorship-optimistic; the contrast is within-tape (same names, same dates, only the weekday
moves), which is the comparison the idea asks for, and it does not repair the level. The offset
family is the 5 weekly ones the idea names — monthly/phase families are not priced here. A 4.18 pp
spread bounds the size of the scheduling channel on this book; it does not certify that every
other committed 4b DD margin is as fragile (that census is not this run).

## Residue for the Sunday review (rule 6 — RULES.md, PROTOCOL.md, scan.py, bot.py, baseline.py untouched)
1. **Idea 910's B136 TREND/AGG candidate should be struck from the standing candidate list.** Its
   sole distinguishing leg (the DD pass) is 6.0x smaller than its own scheduling noise, its repair
   fails, and its IS-only chooser is OOS-anticorrelated.
2. **A concrete PROTOCOL rule-4b clause this run earns:** *a 4b DD or CAGR margin must exceed the
   book's own rebalance-offset spread over the offsets of its cadence, and that spread must be
   published beside the margin.* This run shows a margin surviving in sample (0.62 vs 0.40 pp) and
   dying out of sample (0.70 vs 4.18 pp), so the clause must be evaluated on the OOS window, not IS.
