# Idea 1509 (lane C, 2026-09-19) — should the record's DEVICE-vs-ANCHOR contrasts ALL be re-cut against a TWO-RUNG CAPITAL BLEND?

**KILL as a record-wide re-cut — with ONE carve-out that IS worth adopting.**
Pre-registered bar (written before any number was read): material only if, at 10 bps on U56 AND
B136, >= 10% of biting contrasts FLIP THE SIGN of dSharpe or CHANGE their |t| > 2 decision between
R_NEAR and R_BLEND. **Observed: 5.9% sign flips and 0.4% decision changes on 238 bracketed
contrasts. NOT MET.** Capital arm bar: a blend-keyed rule-8 chooser must beat both the R_NEAR-keyed
chooser and the do-nothing frozen incumbent on OOS Sharpe at every panel. **NOT MET — the four
choosers pick the IDENTICAL cell on all three panels, so the ruler is rule-8 unreachable.**

## What was run
- **CENSUS (mechanical, gate G13):** every sentence in `LEADERBOARD.md`, `CHANGELOG.md`, every
  committed memo/result and every committed script docstring matching a matched-X pattern, each
  classified by anchor form with a published regex, **as committed before this run's own rows were
  appended** (a census of a growing record is not idempotent; the vintage is part of the number). **1,215 matched-X sentences; 8 (0.7%) name a
  BLEND; 1,207 (99.3%) name a single rung, an interpolated statistic, or nothing.**
- **THE RE-CUT (real books):** 45 device books per panel (STOP trailing-equity stop x MAGATE SPY
  200d gate x VOLTGT vol target; DIAL 1 STRENGTH FRAC {1.00..0.00}, DIAL 2 THRESHOLD, 3 rungs each)
  on U56 / B136 / SMALL = **135 books, every cell published**, each re-cut against four rulers
  (R_NEAR nearest rung, R_STAT interpolated statistic, R_BLEND two-rung capital blend, R_BLENDC the
  blend charged its own cross-sleeve turnover at 10 bps) on two anchor ladders (L_G gross = a SCALE
  ladder; L_H min-hold = a COMPOSITION ladder) and three matching statistics (exposure, CAGR,
  turnover). **432 contrasts, 337 bracketed, 95 unbracketed and published (gate G7).**
- Frozen: N = 20, G = 0.75, H = 126, weekly, 10 bps. All 11 gates pass; G1 replays the committed
  2026-09-04 U56 anchor to 3.7e-05.

## The mechanism, measured rather than asserted (gate G9)
A capital blend differs from a single rung **only if the two rungs hold different things.**
- **L_G is a SCALE ladder** — every rung holds the same names at the same relative weights. Measured
  on 27 real blends: a two-rung gross blend and the single gross rung at the **same realised
  exposure** differ by at most **|dSharpe| 2.8e-05 and |dCAGR| 6.1e-06**. The blend *is* the rung.
  Result: **0 of 198 sign flips and 0 of 198 decision changes** on both L_G combos.
- **L_H is a COMPOSITION ladder** — rungs hold different names on the same day, which is why 1484's
  blend mattered. Here it moves things: **11.1%** sign flips on X_TURN and **17.5%** on X_CAGR — but
  **0 and 1** |t| > 2 decision changes respectively, and the flips sit on contrasts whose dSharpe is
  ~0 under both rulers (only 4 of 18 flips exceed |dSharpe| 0.05 on either side).

## THE CARVE-OUT WORTH ADOPTING — the blend is immaterial for RANK claims and NOT for LEVEL claims
Sharpe is scale-invariant, so rounding a matched-X anchor to the nearest rung costs nothing on
Sharpe (max |R_NEAR - R_BLEND| dSharpe **0.0004** on L_G). **CAGR is not.** The same rounding moves
the *level* by up to **1.06 pp/yr on L_G and 2.01 pp/yr on L_H** — larger than the 4b CAGR-floor
margins this record routinely publishes (1498's razor-thin U56/INC G = 0.50 cell at +0.07 pp; the
standing candidate's +1.35 pp). **Recommendation: any committed CAGR- or MaxDD-LEVEL claim cut
against a NEAREST RUNG should be re-cut against the blend (or an exact continuous rung); Sharpe and
other rank claims need not be.** This is a reporting rule, not a rules change, and no rules change
is proposed here.

## The other finding: no ruler rescues any device
Of 337 bracketed contrasts, **0 are significantly POSITIVE (|t| > 2, dSharpe > 0) under the blend
and 25 are significantly NEGATIVE.** Ten previous runs found every drawdown-buying device beaten at
matched exposure by a plain de-gross; re-cutting against a fairer, implementable anchor does not
change that on a single cell. The best cell any chooser reaches (U56 VOLTGT target 0.20, FRAC 0.50:
full 14.94% / 1.1956 / -16.05%, OOS 15.76% / 1.2103 / -16.05%) sits at **dSharpe +0.042, t = +1.20**
against its own matched-exposure blend — unresolved, not a win, and it gives up 1.57 pp of OOS CAGR
to the frozen anchor it beats on Sharpe.

## Both KEEP paths, all 135 cells
**4a: 0 of 135** (the eleventh consecutive run to return 0 — a de-gross cannot beat the book it
scales). **4b: 50 full, 59 OOS, 50 BOTH**, all on U56 (35) and B136 (15), none on SMALL. Every one
inherits the frozen incumbent's standing 4b pass; none is a new candidate, because none beats its
own matched-exposure anchor.

## Rule 8 (dials fit on warm-up..2016-12-31 only; 2017-2026 read ONCE)
`C_RAW`, `C_NEAR`, `C_BLEND` and `C_STAT` pick the **same cell on all 3 panels** (U56/B136
VOLTGT 0.20/0.50; SMALL MAGATE 0.03/0.00). OOS: U56 15.76% / 1.2103 / -16.05% (frozen anchor
17.32% / 1.1857 / -19.13%; SPY 0.8738); B136 13.81% / 1.0167 / -15.22% (anchor 1.0180); SMALL
3.82% / 0.3129 / -35.10% (anchor 0.4398). **C_BLEND beats the do-nothing anchor on OOS Sharpe at
1 of 3 panels and never beats C_NEAR, because it never disagrees with it.**

SURVIVORSHIP (rule 9): U56 / B136 are current-constituent lists and SMALL a current sub-$2B screen
carried back to 2010; every absolute level above is an upper bound. What this run reads is a
contrast between two RULERS on the same books on the same days, which the bias cannot manufacture.

Script: `research/backtests/2026-09-19_two-rung-capital-blend-as-the-matched-X-anchor_C.py`
(+ `.log.txt`, `.census.csv`, `.census_pivot.csv`, `.grid.csv`, `.recut.csv`, `.algebra.csv`,
`.walkforward.csv`, `.gates.csv`).
