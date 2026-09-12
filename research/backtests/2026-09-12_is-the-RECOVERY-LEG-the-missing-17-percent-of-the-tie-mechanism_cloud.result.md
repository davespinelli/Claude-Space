# Idea 596 — is the RECOVERY LEG the missing 17 percent of the tie mechanism?

**cloud lane, 2026-09-12.** Script `2026-09-12_is-the-RECOVERY-LEG-the-missing-17-percent-of-the-tie-mechanism_cloud.py`.
Outputs `.console.txt` / `.cells.csv` (144 arms) / `.predicates.csv` (40 points) / `.episodes.csv` /
`.walkforward.csv` / this file.

## ANSWER = YES. THE LEG SPLIT IS THE WHOLE GAP; THE SWITCH-COST TERM IS REDUNDANT.

**6 of 6 pre-registered hypotheses pass.** On a fresh 141-arm corpus with 45 MaxDD ties, the
decline-leg predicate — *the clause was not de-grossed anywhere between the control's drawdown peak
and its trough* — is an **exact identity with the tie label: P(pred|tie) = 1.0000 and
P(tie|pred) = 1.0000, 0 false negatives, 0 false positives, at every one of the five cover bars**,
pooled and with the confound family dropped.

The record's open question was a two-change gap: idea 592's predicate (window peak→**recovery**) read
0.8326, and the 2026-09-10 census's (window peak→**trough**, *plus* a switch-cost term) read 1.0000,
with nothing saying which change did the work. Decomposed here at eps = 0 over all 141 scored arms:

| predicate | window | P(pred\|tie) | P(tie\|pred) | #pred |
|---|---|---|---|---|
| EPISODE (idea 592's) | peak → recovery | **0.1333** | 1.0000 | 6 |
| **DECLINE (idea 596's)** | peak → trough | **1.0000** | **1.0000** | 45 |
| RECOVERY (the control) | trough → recovery | 0.1333 | 1.0000 | 6 |
| DECLINE+COST (2026-09-10's) | peak → trough, + no switch cost | 1.0000 | 1.0000 | 45 |

- **the LEG SPLIT moves necessity +0.8667** (0.1333 → 1.0000). This is change (a).
- **the SWITCH-COST term moves it +0.0000**, sufficiency +0.0000, and DECLINE vs DECLINE+COST
  **disagree on 0 of 141 cells**. Change (b) is redundant: the 2026-09-10 predicate's exactness is
  the leg split's doing, and its cost term can be dropped from any restatement.
- **all 39 ties the whole-episode predicate misses have cover 0.000e+00 on the decline leg** — their
  entire binding-episode cover sits in the recovery leg. The mechanism is not subtle: the decline
  legs here are 17 trading days (U56/B136, 2020-02-19 → 2020-03-12) while the recovery legs are
  100–172 days, so an episode-**average** cover is swamped by a recovery the DD leg never sees.
- **RECOVERY alone is not the predicate** (0.1333 necessity), which is the control reading that stops
  "any window works" passing as a finding.

## Why 0.1333 here and 0.8326 there — and what is comparable

This run did **not** rebuild idea 592's block shuffles. A predicate claimed to be exact is a claim
about the predicate, so it was tested on a corpus it was not discovered on; the price of that choice
is stated plainly: **0.1333 is not comparable to 0.8326 as a number.** Only the within-run ordering
of the four predicates is evidence, and that ordering is unambiguous. The level gap is itself
informative — on a corpus whose binding episode has a long recovery tail, idea 592's episode-average
column is near-useless (0.1333), so the record should not quote 0.8326 as a property of the predicate.

## Scope limit on the sufficiency direction (named, not buried)

Necessity is close to an identity **by construction**: zero decline-leg cover means the arm holds the
control's weights throughout peak→trough, so the arm/control equity *ratio* is constant there and the
arm reproduces the control's peak-to-trough decline exactly. The non-trivial half is **sufficiency** —
the arm's own MaxDD could be set on a *different* episode, which is exactly the case 2026-09-10 found
2 instances of and this corpus found **0** of. Sufficiency is therefore an empirical result here, and
it holds **only for de-gross clauses** (the arm never holds *more* than the control). A clause that
can add exposure could break it, and nothing in this run tests that.

## Corpus, gates, conventions

144 arms = 3 panels × 4 gate families × 4 dials × 3 gross, all reported; 3 degenerate (the gate never
fires) excluded and counted. Book = the live form `baseline.rules_v2_weights` (200d ±3% band, g/N,
gated-out weight to CASH), weekly, next-day fill, 10 bps. Clause = market gate OFF ⇒ book de-grossed to
cash (k=0). Controls: CONTROL-U at nominal gross, CONTROL-M = the same book × a constant so its mean
realised gross equals the arm's. Families SPYTR / BREADTH / VOL / **SPYDD** — SPYDD is the confound
(it fires on the drawdown itself) and is **named**, with every rate reported again without it
(30 ties, identical verdicts). Tuned parameters: **two**, both the predicate's — leg split (4) and
cover bar (5 rungs, because "cover == 0" is not testable in floating point). Ties: 45 of 141 (31.9%);
by family SPYTR 0, BREADTH 12, VOL 18, SPYDD 15.
Gates: G1 never-firing arm ≡ CONTROL-U (0.0e+00), G2 runner ≡ `engine.backtest` (1.4e-17), G3 the
binding episode reproduces the control's MaxDD (0.0e+00), G4 CONTROL-M's mean gross ≡ the arm's
(≤ 1.6e-04). All pass.

## Rule 8 walk-forward, and the books this corpus threw up: KILL

Dial chosen on IS (..2016-12-31) by IS Sharpe alone per (panel, family, gross); OOS (2017-01-01..) read
once. **4 of 36 rule-8 picks pass 4b OOS; 2 of 36 pass 4a OOS.** Over all 141 arms: 4a 2 / 4b 7 full
sample, 4a 12 / 4b 12 on the OOS window, **BOTH paths 0**. Dominant binding 4b leg: CAGR (74 cells).

Seven arms pass 4b on the full sample (six also OOS), all but one on U56 at gross 1.00, and three of
them *are* the rule-8 IS pick at their (panel, family, gross) — superficially a stronger candidate than
idea 806's. They die on the one test that matters:

| arm | CAGR / Sharpe / MaxDD | OOS | **its own gross-matched CONTROL-M** | ctlM 4b |
|---|---|---|---|---|
| U56 VOL 0.25 g=1.00 | 11.08% / 1.210 / **−9.57%** | 11.58% / 1.239 | 10.93% / 1.202 / −15.11% | **PASS** |
| U56 BREADTH 0.20 g=1.00 | 11.46% / 1.196 / −15.91% | 12.61% / 1.273 | 11.48% / 1.202 / −15.82% | **PASS** |
| U56 SPYDD 0.35 g=1.00 | 11.19% / 1.173 / −15.91% | 12.70% / 1.278 | 11.44% / 1.202 / −15.77% | **PASS** |

**Arms clearing 4b on both windows AND beating their own gross-matched control: 0 of 141.**
6 of the 7 passers are matched by a control that holds uniformly less with **no timing at all** — the
pass is the exposure, not the clause. (The seventh, B136 BREADTH 0.20, fails 4b OOS.) This reproduces
ideas 502 / 504 / 674 / 767 on a fourth construction: 4b's Sharpe legs are measured against SPY, so
only its CAGR floor ever sees a clause, and at gross 1.00 the floor is cleared by exposure alone.
Worth recording separately: U56 VOL 0.25 does cut drawdown hard against its matched control
(−9.57% vs −15.11%) at equal Sharpe — a real effect that **4b cannot see**, which is evidence for the
record's standing complaint about the DD cap rather than a candidate.

**No KEEP. No memo written.** Nothing here is a rules change: the panel, the family and the gross were
read off a 144-cell grid after the fact — the failure mode idea 806 documented in this same sprint —
so the most any of it could be is a pre-registration target, filed as idea 810.

## Caveats

- **SURVIVORSHIP.** All three panels are current-constituent lists, so every level is optimistic; the
  SMALL panel is the worst case (a sub-$2B screen read today cannot see the names that fell out of it —
  `data/SMALL_PANEL_README.md`). Per the standing instruction, the 52 tickers with
  `max_1d_move >= 1.0` in `data/small_meta.csv` were dropped first, leaving 663 names. The predicate
  result is a within-panel agreement rate, which survivorship moves far less than it moves levels; the
  walk-forward levels carry the full bias.
- Every panel's binding episode is **2020** (U56/B136 peak 2020-02-19, SMALL peak 2018-08-31), so the
  decline/recovery asymmetry this run exploits is measured on essentially one event. A corpus whose
  binding episode were 2022 (a long decline, fast recovery) could invert the two columns' roles, and
  that is the obvious next test — filed as part of idea 811.
- `data/prices.csv` is re-downloaded daily, so U56 rows reproduce to ~3e-3, not bit-exact (idea 406).
- The IS/OOS split is the record's standing 2016/2017 convention and was not varied.

## Filed for the queue

- **810** — pre-registered run of the U56 / MA-band / gross-1.00 light-overlay cell against a
  gross-matched control as the *primary* comparand, not a footnote.
- **811** — does the decline/recovery decomposition survive a corpus whose binding episode is 2022?
