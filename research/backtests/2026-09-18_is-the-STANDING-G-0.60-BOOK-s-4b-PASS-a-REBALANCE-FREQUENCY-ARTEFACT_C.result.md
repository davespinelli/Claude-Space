# Idea 1285 (lane C, 2026-09-18) — is the STANDING G = 0.60 BOOK's 4b PASS a REBALANCE FREQUENCY ARTEFACT?

**ANSWERED: NO — (A) NOT AN ARTEFACT, WITH A NARROWING. On U56 the standing rung clears 4b at W, M and Q at every costed rung and at D up to 25 bps; the cadence gain is NOT idea 943's turnover rebate (the book's W→other gain is negative where the null's is positive); and letting a rule-8 chooser move the cadence COSTS OOS Sharpe (t −3.55). BUT the book's separation from a turnover-matched twin is a WEEKLY fact: +0.1244 (z +2.30, above all 12 seeds) at W against +0.041 / +0.042 / +0.059 (z +0.60 / +1.29 / +1.18) at D / M / Q. KEEP-4b candidate CONFIRMED and narrowed to (U56, weekly). No new book, no RULES change (rule 6).** 8 of 9 gate items passing, 1 pre-declared gate REFUTED and kept as a result; 68s, offline, deterministic.

## Construction
3,360 published cells = 3 panels (U56 / B135 / SMALL663) × 14 arms (RANK, RAND×12, SPYONLY) × **DIAL 1 cadence {D, W, M, Q}** × 5 gross rungs (published, never tuned) × **DIAL 2 cost {0, 10, 25, 50} bps** (0 = reference). 336 chooser rows. Fill t+1 throughout (PROTOCOL rule 2). Frozen: N = 20, H = 126, the 21/252 + 0/126 + 0/63 composite, eligibility (above 200d MA, vol20 < 0.60), equal slots, 260-row warm-up.

**The turnover-matched control** is RAND: identical N, H, cadence, gross and eligibility set, ranking replaced by a uniform draw, 12 seeds. Matched by construction, and the match is published rather than assumed — realised turnover/yr at U56 G = 0.60 is RANK **2.32 / 3.28 / 1.74 / 1.32** against RAND **2.78 / 3.60 / 2.02 / 1.56** at W / D / M / Q — and every difference is *also* published in a TURNOVER-NEUTRAL form charging the control `c × (turnover_RANK / turnover_RAND)` so the two pay identical annual drag.

## ARM A — the standing rung re-priced (U56, G = 0.60, 10 bps, t+1)
| cadence | CAGR | Sharpe | MaxDD | H1 / H2 | OOS CAGR / Sharpe / MaxDD | turn/yr | 4b |
|---|---|---|---|---|---|---|---|
| D | 11.89% | 1.0610 | −18.77% | 1.15 / 1.01 | 13.24% / 1.0871 / −18.77% | 3.28 | **PASS** |
| **W (standing)** | **12.59%** | **1.1517** | **−15.51%** | **1.21 / 1.11** | **13.78% / 1.1826 / −15.51%** | 2.32 | **PASS** |
| M | 11.51% | 1.0671 | −18.77% | 1.22 / 0.97 | 12.39% / 1.0562 / −18.77% | 1.74 | **PASS** |
| Q | 12.37% | 1.1513 | −16.11% | 1.23 / 1.11 | 13.91% / 1.1884 / −16.11% | 1.32 | **PASS** |

SPY 15.13% / 0.8849 / −33.72% (OOS 0.8747); live RULES v2 8.62% / 1.2018 / −12.05% (OOS 1.2781).
4b pass count at G = 0.60 over the three costed rungs {10, 25, 50}: **U56 D 2/3, W 3/3, M 3/3, Q 3/3** — D's only failure is the CAGR floor at 50 bps. **B135 D 0/3, W 2/3, M 0/3, Q 2/3** (D and M fail on DD). **SMALL663 0/3 at every cadence.**

## ARM B — selection above the turnover-matched twin (G = 0.60, 10 bps)
| panel | D | W | M | Q |
|---|---|---|---|---|
| U56 diff (z, pct) | +0.0412 (+0.60, 0.75) | **+0.1244 (+2.30, 1.00)** | +0.0421 (+1.29, 0.83) | +0.0587 (+1.18, 0.92) |
| U56 turnover-neutral diff | +0.0373 | **+0.1193** | +0.0388 | +0.0558 |
| B135 diff (z) | −0.0143 (−0.24) | +0.0136 (+0.22) | +0.0670 (+0.76) | +0.0213 (+0.34) |
| SMALL663 diff (z) | −0.0728 (−1.04) | −0.0319 (−0.29) | −0.1730 (−2.06) | −0.0593 (−0.46) |

The twin passes 4b at **0 or 1 of 12 seeds at every U56 cadence**, so no cadence makes the pass reproducible without the ranking. But only at W does RANK sit above all 12 seeds and clear 2 SD, and the turnover-neutral re-charge moves the U56 W figure by 0.005.

## ARM C — it is not idea 943's rebate (U56, 10 bps, gain relative to W)
| cadence | RANK gain | NULL(median) gain | excess | RANK OOS gain | NULL OOS gain |
|---|---|---|---|---|---|
| D | −0.0908 | **+0.0177** | −0.1084 | −0.0955 | −0.0285 |
| M | −0.0847 | **+0.0057** | −0.0904 | −0.1264 | −0.0568 |
| Q | −0.0004 | **+0.0612** | −0.0616 | +0.0058 | +0.0987 |

943's rebate is visibly present **in the null** (slowing to Q buys a random book +0.0612 at 10 bps, rising to +0.1117 at 50) and the book does not collect it: its excess over the same-cadence null is negative at all 12 U56 cells. W is where the ranking pays and the null does not.

## ARM D — rule 8, parameters chosen on warm-up..2016-12-31, 2017-2026 read ONCE
FREE picks (cadence, gross) in sample; FROZEN_W pins the standing weekly cadence and picks gross only.
**d(OOS Sharpe) = FREE − FROZEN_W = −0.0369 (SE 0.0104, t −3.55) over 168 cells; positive 53, negative 67, identical picks 48.** By arm: **RANK −0.0611** (n = 12; 1 positive, 4 negative, 7 identical), RAND −0.0381 (n = 144), SPYONLY +0.0025. The IS chooser picks W for RANK at 7 of 12 cells. **Cadence freedom is a negative-value dial.**
U56 RANK chooser, FREE = FROZEN at 0 / 10 / 25 bps → **W / 0.60**, OOS Sharpe 1.2034 / 1.1826 / 1.1512, 4b PASS. At 50 bps IS drifts to Q/1.00 → OOS 1.1389 and fails the DD leg; FROZEN_W's W/1.00 fails it too. Rule-8 4b passes: **RANK 12/24, RAND 13/288, SPYONLY 0/24.**
**4a: 0 of 3,360 published cells and 0 of 336 chooser rows** — rule 4's own stated reason for path 4b.

## Gates — 8 of 9 passing, and the one failure is a finding
G1 fast runner == `engine.backtest` on the standing book, **2.08e-17**. G2 SPYONLY at gross 1.00 / 0 bps reproduces each panel's own SPY Sharpe, **0.00e+00**. G3 CAGR non-increasing in the cost rung, **0** violations across 3,360 cells. **G4 (pre-declared) FAILS** — SPYONLY is *not* cadence-invariant at every gross, because below gross 1.00 the arm carries a cash sleeve and rebalancing back to gross **is a trade**: its own Sharpe spread across D/W/M/Q at G = 0.60 runs **0.0080 / 0.0099 / 0.0153 / 0.0243** at 0 / 10 / 25 / 50 bps on U56. A book with no stock selection whatsoever is still a cadence object; the gate is kept in the table as a refuted premise (rule 7) rather than edited away. **G4b** the invariant that does hold — gross 1.00, no cash sleeve — is exact: 1 distinct Sharpe, 0 turnover. G5 SPY never a constituent. G6 every chooser decided on IS rows only. G7 RANK turnover/yr non-increasing as the cadence slows, 0 of 9 violations. **G8 reproduces the record's committed standing-rung triple (idea 1281: 12.59% / 1.1517 / −15.51%, OOS 1.1826) to max|dSharpe| 0.0000.**

## Failing-4b-leg census (continuity with the record's standing diagnosis)
RANK (n = 203 failing cells): **DD 0.8670**, CAGR 0.5074, H2 0.4926, OOS 0.4187, H1 0.3941. RAND (n = 2,815): DD 0.7542, CAGR 0.6188. SPYONLY (n = 240): H1 0.8958, DD 0.8000. The DD leg still binds for 0.867 of the book's failures, as the CHANGELOG says — and it is now clear that the cadence dial moves that leg (U56 MaxDD −15.51% at W against −18.77% at D and M) without changing the verdict on this panel.

## Survivorship (rule 9)
U56 and B135 are CURRENT-constituent lists; SMALL663 is a current sub-$2B screen with the house `max_1d_move >= 1.0` filter applied FIRST (52 of 715 names dropped). A current-constituent list is a list of SURVIVORS, so a random draw from it is a draw from winners and the RAND control is **flattered** — which biases the run against ARM B's positive separations, making the weekly +0.1244 conservative. Every absolute 4b verdict and OOS triple above is an **upper bound**. The cadence contrast is read on identical windows of one tape and is first-order immune to a bias that moves all four cadences together.

Script: `research/backtests/2026-09-18_is-the-STANDING-G-0.60-BOOK-s-4b-PASS-a-REBALANCE-FREQUENCY-ARTEFACT_C.py`
Memo: `research/backtests/2026-09-18_is-the-STANDING-G-0.60-BOOK-s-4b-PASS-a-REBALANCE-FREQUENCY-ARTEFACT_C.memo.md`
