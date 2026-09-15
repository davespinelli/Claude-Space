# Idea 676 (cloud lane, 2026-09-15) — does the 4b CAGR FLOOR survive a NON-ZERO CASH LEG on the arms that need it least?

**ANSWERED: NO — the CAGR floor is the one 4b leg a cash rate can buy. Over 0–5%/yr flat cash the
4b pass count on idea 670's own 160-point grid goes 17 → 51 (CONV-A) / 17 → 38 (CONV-B), the floor's
pass share goes 0.425 → 0.613, and 34 of 160 committed 4b verdicts change. Every one of those 34
changes is FALSE → TRUE: a cash credit never destroys a committed pass, it manufactures new ones.
VERDICT: KILL for capital (no book promoted); the deliverable is the invariance census below.**
RULES.md, PROTOCOL.md, scan.py, bot.py, baseline.py untouched.

Script `research/backtests/2026-09-15_does-the-4b-CAGR-FLOOR-survive-a-NON-ZERO-CASH-LEG_cloud.py`;
console `..._cloud.console.txt`; data `..._cloud.{grid,invariance,walkforward,zerosignal,window,l5_by_gross,4b_by_gross,vintage,hypotheses}.csv`.
Grid: idea 670's ten arms × 8 gross rungs × 2 panels = **160 points** × 7 credit levels =
**1,120 rows, every one published** (weekly, BAND03_M monthly, 10 bps, next-day execution).
Two tuned parameters, the queue's own: **credit level** {0,1,2,3,4,5,6}%/yr × **panel** {U56, B136}.

## Gates
| gate | result |
|---|---|
| G1 `fast_backtest` == `engine.backtest` (U56/CAND20 g=0.75) | **1.39e-17** PASS |
| G2 H_REPRO vs idea 670's committed grid | **FAIL as pre-registered** — max \|d\| CAGR 2.75e-3, Sharpe 1.24e-2, H2 3.38e-2 against a 5e-4 bar; 4b verdicts 159/160 |
| G2b vintage diagnostic (the honest reading of that failure) | rolled back to any earlier tape the **4b verdicts match 160/160** (09-08, 09-04, 09-03) and levels shrink to CAGR 1.3e-3 / H2 1.9e-2 |
| G3 credit identity (no cash at g=1.00 ⇒ credit moves nothing) | **0.000e+00** PASS |
| G4 CAGR non-decreasing in the credit | **160/160** PASS |
| G5 determinism | no RNG in this script; grid recomputed identically PASS |
| G6 comparands printed first | SPY U56 15.13%/0.8845/−33.72%, B136 15.16%/0.8861/−33.72% (SPY holds no cash — the 4b bars are credit-invariant by construction) |

**Gate correction, stated not hidden:** the 5e-4 level bar was mis-set for a *cross-vintage*
comparison — idea 670 ran on the 2026-09-11 tape (its B136 cache ended 09-04) and this run's tape
carries four more sessions. G2b is the diagnostic: the one differing 4b verdict is a tape artefact
(it disappears at every rolled-back tape), so the reproduction is sound at the verdict level while
the pre-registered level bar was wrong. The residual H2 deviation of ~2e-2 is the same
vintage-sensitivity idea 670 itself reported (8e-3 → 1.9e-2 across its own truncations).

## The answer — 4b and its five legs as the credit rises
CONV-A is the record's own convention (`engine.metrics`, Sharpe at rf=0). CONV-B takes **every**
Sharpe against rf = the credit, for arm, baseline and SPY alike; the CAGR floor and DD cap are
identical by construction, so the gap between the tables is the rf=0 convention, not the cash leg.

| credit | 4b (A) | 4a (A) | 4b (B) | 4a (B) | L1 H1 (A/B) | L2 H2 (A/B) | L3 OOS (A/B) | **L4 DD** | **L5 CAGR floor** |
|---|---|---|---|---|---|---|---|---|---|
| 0% | **17**/160 | 4/160 | **17**/160 | 4/160 | .800/.800 | .700/.700 | .713/.713 | **.706** | **.425** |
| 1% | 20 | 24 | 20 | 4 | .919/.800 | .825/.700 | .856/.731 | .706 | .463 |
| 2% | 28 | 32 | 25 | 4 | .931/.800 | .850/.700 | .875/.750 | .706 | .500 |
| 3% | 36 | 37 | 29 | 4 | .944/.800 | .869/.700 | .894/.750 | .706 | .525 |
| 4% | 46 | 41 | 34 | 4 | .944/.800 | .881/.713 | .912/.775 | .706 | .588 |
| **5%** | **51**/160 | **42**/160 | **38**/160 | **4**/160 | .950/.800 | .900/.694 | .912/.800 | **.706** | **.613** |
| 6% | 63 | 43 | 41 | 7 | .956/.700 | .900/.650 | .912/.800 | .706 | .681 |

Two findings sit in that table:
1. **The CAGR floor is bought by cash.** Its pass share rises 0.425 → 0.613 by 5%, and at the live
   gross 0.75 it goes **0.550 → 0.900**. The floor is the only 4b leg that moves with the cash rate
   at all (L4 is **exactly constant at 0.706 across every credit** — a drawdown verdict cannot be
   bought).
2. **The 4a explosion is a convention artefact, not a cash fact.** Under the record's rf=0 Sharpe,
   4a goes 4 → 42/160; under CONV-B it stays **4/160 at every credit ≤5%**. Crediting cash and then
   counting that riskless return in the numerator of an rf=0 Sharpe pays cash-heavy books twice.
   Any future run that adds a cash leg must move `rf` with it or its Sharpe legs are meaningless.

## The invariance census (the queue's deliverable)
- **4b verdicts unchanged across 0–5%: 126 of 160 (78.8%)** under CONV-A, **132 of 160 (82.5%)**
  under CONV-B. Across 0–6%: 114 of 160.
- **All 34 flips are FALSE → TRUE.** No committed 4b pass is destroyed by any credit up to 6% on
  either panel. Idea 642's T-bill path can only *add* passes to the record, never retract one.
- The flips concentrate exactly where the queue predicted — the arms that need the floor least, i.e.
  the cash-heavy de-grossed ones: the whole BAND03/BAND03_M/BAND08 family at g ∈ {0.75, 0.85, 0.95}
  (cash share 33–47%) flips at 1–5%, and the ranked books at g ∈ {0.35, 0.50, 0.60} follow.
- **L5 alone: 30 of the 92 points failing the floor at 0% clear it by 5%.** Idea 670's committed
  closed form predicts **27** (Spearman with the realised flip credit **+0.9712**, median \|error\|
  **0.37%**, grid-rung exact 20/30) — **H_CF PASSES**, and the queue's "27 of 90" is confirmed as a
  genuine flip count once the 56 rows whose `need` is *negative* (they already clear the floor) are
  removed from the closed form's own `need ≤ 5%` reading of 83/160.

## The zero-signal control — where the floor stops being an edge test
| credit | SPYBH 4b passes | L5 share | L4 share | gross window width (both panels) |
|---|---|---|---|---|
| 0–3% | **0/16** | .500 | .375 | **−0.25** (closed) |
| 4–5% | **0/16** | .625 | .375 | −0.10 (closed) |
| 6% | **2/16** (g=0.50) | .750 | .375 | **0.00 (opens)** |

**H_SPYBH PASSES at the queue's 5% bar and fails at 6%**: a book with no signal whatsoever — `g ×
SPY` — cannot buy a 4b pass with cash up to 5%/yr, but at 6% it can, on both panels, at g=0.50.
Idea 670's "the gross window width is the edge test" therefore carries an unstated cash condition:
the zero-signal window is closed only while cash pays less than ~6%.

## The record's two matched-gross survivors are credit-proof
| point | 0% | 5% | 6% |
|---|---|---|---|
| **U56/CAND20 g=0.75** (the 2026-09-04 KEEP 4b book) | 12.73% / 1.0596 / −18.31% PASS | 14.15% / 1.1637 / −18.24% PASS | PASS |
| B136/EWELIG g=0.75 | 10.66% / 1.0211 / −17.69% PASS | 12.05% / 1.1406 / −17.57% PASS | PASS |

**H_SURV PASSES.** The live KEEP candidate's 4b status does not depend on the cash assumption in
either direction — the one conclusion in this area that 642 cannot touch.

## Rule 8 walk-forward — chosen on 2009–2016 alone, 2017–2026 read once, at every credit
**H_WF FAILS on all 6 (panel, chooser) pairs**: neither the pick nor the OOS 4b verdict is
credit-invariant under either convention.

| panel | credit | chooser | pick | OOS CAGR / Sharpe / MaxDD | OOS 4b | OOS 4a |
|---|---|---|---|---|---|---|
| U56 | 0% | C1 | BAND08 g=1.00 | 12.02% / 1.1636 / −19.05% | PASS | FAIL |
| U56 | 5% | C1 (rf=0) | **BAND03 g=0.20** | 6.98% / **3.4853** / −3.02% | FAIL (L5) | PASS |
| U56 | 5% | C1 (CONV-B) | CAND20_NOCAP g=1.00 | 20.90% / 1.1145 / −27.75% | FAIL (L4) | FAIL |
| U56 | 5% | C2 | CAND20_NOCAP g=0.50 | 13.20% / 1.3828 / −14.45% | PASS | FAIL |
| B136 | 0% | C1 | BAND08 g=1.00 | 11.05% / 1.0974 / −19.50% | PASS | FAIL |
| B136 | 5% | C1 (rf=0) | **BAND03 g=0.20** | 6.57% / **3.3840** / −3.07% | FAIL (L5) | PASS |
| B136 | 5% | C2 | CAND10 g=0.35 | 9.53% / 1.1687 / −10.19% | FAIL (L5) | FAIL |

Comparands: SPY OOS **15.27% / 0.8740 / −33.72%** (U56) and **15.33% / 0.8767 / −33.72%** (B136);
RULES v2 OOS **9.46% / 1.2772 / −12.05%** at 0% and **12.03% / 1.5949 / −11.93%** at 5% (U56),
**7.88% / 1.1059 / −12.24%** and **10.46% / 1.4384 / −12.11%** (B136).

The `C1 → g=0.20` collapse is the rf=0 convention in its purest form: a 20%-gross band book with
80% cash earns a 3.49 Sharpe on a 6.98% CAGR. CONV-B removes it entirely (C1 holds BAND08 g=1.00
to 3%), which is the strongest single argument in this run for fixing the convention before any
T-bill path is committed.

## What 642 can and cannot overturn
| conclusion | credit-invariant? |
|---|---|
| any committed 4b **PASS** (including the 2026-09-04 KEEP book) | **YES** to 6% — passes are never destroyed |
| any DD-cap (L4) verdict | **YES, exactly** — 0.706 at every credit |
| 4a counts under the consistent rf convention | **YES** (4/160 at every credit ≤5%) |
| 4a counts as the record computes them (rf=0) | **NO** — 4 → 42/160 |
| 4b **FAILURES** whose only failing leg is L5 on a cash-heavy arm | **NO** — 34 of 160 flip by 5% |
| "the zero-signal window is closed" (idea 670 §3) | **YES to 5%, NO at 6%** |
| any rule-8 walk-forward pick on this grid | **NO** — 0 of 6 invariant |

**Proposed (rule 6 — NOT applied):** PROTOCOL should state the cash convention beside every 4b
count, and any run that credits cash must take Sharpe against the same rf. No RULES change, no
PROTOCOL edit made by this run.

**SURVIVORSHIP (PROTOCOL rule 9):** U56 and B136 are CURRENT constituents of `universe.json` and
`universe_broad.json` — every CAGR is optimistic and every MaxDD understated, which makes the CAGR
floor *easier* to clear here than on a point-in-time panel. The invariant findings above are
therefore conservative; the flip counts would, if anything, be larger without the survivor bias.
