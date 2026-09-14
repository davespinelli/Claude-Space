# Idea 847 — how many committed RULE-8 PICKS chose a DIAL THAT DID NOT EXIST for most of the IS WINDOW?
lane C, 2026-09-14 · `2026-09-14_how-many-committed-RULE-8-PICKS-CHOSE-a-DIAL-THAT-DID-NOT-EXIST-for-most-of-the-IS-WINDOW_C.py`

## THE ANSWER: **FEW PICKS CARRY THE DEFECT, BUT WHERE IT EXISTS IT IS NEARLY TOTAL — AND FIXING IT DOES NOT PAY.**
**236 of 6,465** committed dial values (**3.7%**, 73 of 543 files, medium detector) name a rolling
window at all; of those, **148 (62.7%)** were chosen on an IS window their threshold was dead for
more than a tenth of, **51 (21.6%)** for more than half, and the minimum live share on the record is
**0.0000** — a pick that never existed in sample. Re-choosing the record's **own committed numbers**
with the dead dials removed moves the pick in **83.9%** of the cells that still have a candidate and
moves the committed OOS Sharpe by a median **0.1330** (max **1.5926**). On the price leg the warm-up-
aware chooser moves the w pick in **66 of 72** cells (**91.7%**) at 10 bps — 843's 76% QROLL rate
reproduces and **generalises to two families it never touched** (QROLL 100%, VROLL 91.7%, MAROLL
83.3%, spread 16.7 pp) — but it buys nothing: median OOS Sharpe **1.1098 → 1.0887 (−0.0211)**, 4a
**0 of 72 under every chooser** at 10 bps, 4b 18 → 20. **KILL for capital.** The defect is a
reporting defect, not a lost edge: no book is promoted, no KEEP is claimed, no RULES change.

## GATES (printed before any verdict) — 6 of 6 PASS
| gate | what | result |
|---|---|---|
| G1 | vectorised runner == `engine.backtest` | max │d│ **1.041e-17** |
| G2 | fast CAGR/Sharpe/MaxDD == `engine.metrics` | max │d│ **0.000e+00** |
| G3 | **the inertness identity on this run's corpus**: before its threshold exists a window-dial arm is the ungated book | max │d│ **0.000e+00** on **936** arms across all three families |
| G4 | this run's QROLL cells rebuild idea 843's **committed** `.walkforward.csv` | **216** common cells, **0** w mismatches, **0** level mismatches, max │d live share│ 1.110e-16, max │d OOS Sharpe│ **2.220e-16** |
| G5 | RULES v2 and SPY vs their committed triples | 8.6282% / 1.2018 / −12.0549% and 15.16% / 0.8861 / −33.72%, max │d│ **4.561e-05** |
| G6 | the census detector against a control set written **before** the census ran | **15 of 15** |

G4 is what makes this a re-read of the record rather than a private grid: 216 of the record's own
committed picks are inside this run's corpus, bit-identically.

## LEG A — THE CENSUS (689 committed walkforward files; nothing re-run)
| pick set | files | committed dial values | warm-up-bearing | WU % | live < 0.90 | live < 0.50 | median live | min live |
|---|---|---|---|---|---|---|---|---|
| P1 narrow | 543 | 6,465 | 70 | 1.1% | 56 | 25 | 0.7489 | 0.0000 |
| **P2 medium (headline)** | 543 | 6,465 | **236** | **3.7%** | **148 (62.7%)** | **51 (21.6%)** | **0.8587** | **0.0000** |
| P3 wide | 543 | 6,465 | 1,942 | 30.0% | 352 | 117 | 0.9721 | 0.0000 |

The detector spans a 28× range in what counts as a window dial (70 → 1,942), so **the level of this
census is a detector choice and only its shape is robust**: at every detector the median flagged
pick is alive for most of its window and a fifth of them are not. Read the bar-1.00 column as a
definition: a rolling window of w ≥ 20 observations on a leg that starts at the panel's own start
**always** has live share < 1.0, so "how many sub-1.0 picks are there" is answered by construction
and the informative question is *how far* below.

## LEG B — RE-CHOOSING THE RECORD'S OWN COMMITTED NUMBERS (28 files, committed OOS reads compared)
| pick set | bar | cells | no candidate | moved | move % | med │dOOS Sharpe│ | max │dOOS│ | worse | better |
|---|---|---|---|---|---|---|---|---|---|
| P1/P2 | 0.50 | 7,750 | 18 | 4,234 | 54.8% | 0.0446 | 1.0635 | 1,357 | 2,852 |
| **P1/P2** | **0.90** | 7,750 | **7,302** | 376 | **83.9%** | **0.1330** | 1.5926 | 107 | 269 |
| P1/P2 | 1.00 | 7,750 | 7,520 | 214 | 93.0% | 0.3771 | 1.5926 | 84 | 130 |
| P3 | 0.50 | 8,164 | 18 | 4,612 | 56.6% | 0.0510 | 1.9923 | 1,486 | 3,101 |
| P3 | 0.90 | 8,164 | 7,302 | 754 | 87.5% | 0.3771 | 1.9923 | 236 | 518 |
| P3 | 1.00 | 8,164 | 7,556 | 592 | 97.4% | 0.4336 | 1.7846 | 198 | 394 |

**This is the queue's question answered on the record's own OOS numbers: the reads move, and they
move a lot.** The honest caveat is the `no candidate` column — at bar 0.90 the liveness screen
empties **94% of the record's re-choosable cells**, so the 83.9% move rate is measured on the 448
cells that retain a candidate at all, and a move is usually a move *to a short or non-rolling dial*.
Direction is 2.5:1 in favour of the re-choice (269 better / 107 worse at 0.90), which is evidence
the blind chooser is buying warm-up rather than signal — but it is an unconditioned comparison of
other people's committed cells, not a controlled experiment.

## LEG C — PROTOCOL RULE 8 ON THE BOOKS (dial chosen on IS ≤ 2016-12-31, OOS 2017-01-01…2026-09-11 read ONCE)
| chooser | cells | no candidate | 4a | 4b | med OOS CAGR | med OOS Sharpe | med OOS MaxDD |
|---|---|---|---|---|---|---|---|
| BLIND (the record's) | 216 | 0 | **3** | 80 | 11.71% | 1.107 | −17.47% |
| BAR050 (843's LIVE50) | 216 | 0 | 3 | 80 | 11.76% | 1.109 | −17.47% |
| BAR090 | 216 | 0 | 2 | **85** | 11.86% | **1.134** | −17.32% |
| BAR100 | **0** | **216** | — | — | — | — | — |
| LIVELEG (843's) | 216 | 0 | **0** | 83 | 11.53% | 1.083 | −17.35% |

Benchmarks, same OOS window: **RULES v2 (live) 8.65% / 1.188 / −12.15%; SPY 15.33% / 0.877 /
−33.72%.** At the headline 10 bps rung: **4a 0 of 72 under every chooser**, 4b 18 (BLIND) / 18
(BAR050) / **21** (BAR090) / 20 (LIVELEG). 843's direction reproduces — the warm-up-aware chooser
kills 4a passes (3 → 0 pooled over rungs) and lifts 4b (80 → 83) — and its *magnitude* is tiny:
median │ΔOOS Sharpe│ on a moved cell is **0.0491**.

**CF_EMPTY100, a construction fact and not a finding:** 216 of 216 cells have no fully-live
candidate at bar 1.00. Every rolling dial carries warm-up, so a "fully-live dials only" chooser
cannot make a pick at all. A liveness bar is only implementable below 1.0, which is why the record's
chooser cannot simply be made strict — it has to be made *leg-aware*, as 843 proposed.

**Family generality (the part 843 could not test):** move rate QROLL 100.0%, VROLL 91.7%, MAROLL
83.3%, spread 16.7 pp; median live share of the BLIND pick 0.8784 / 0.9940 / 0.7309. The
warm-up-blindness is a property of the CHOOSER, not of the breadth family.

## HYPOTHESES — 5 of 9 PASS
| | verdict | reading |
|---|---|---|
| H_CENSUS | **FAIL** | 236 of 6,465 committed dial values (3.7%) are warm-up-bearing, against a 25% bar |
| H_MOST | **FAIL** | 51 of 236 (21.6%) below 0.50 live share, against a 50% bar; 148 (62.7%) below 0.90 |
| H_MOVEB | PASS | bar-1.00 re-choice moves 214 of 230 committed cells (93.0%) |
| H_OOSB | PASS | median │Δ committed OOS Sharpe│ 0.3771 (worse 84 / better 130) |
| H_MOVEC | PASS | LIVELEG moves 66 of 72 cells (91.7%) at 10 bps over three families |
| H_GENERAL | PASS | QROLL 100.0% / VROLL 91.7% / MAROLL 83.3%, spread 16.7 pp ≤ 25 pp |
| H_BETTER | **FAIL** | median OOS Sharpe BLIND 1.1098 vs LIVELEG 1.0887 (**−0.0211**) |
| H_KEEP | PASS | 4a/4b at 10 bps: 0/18, 0/18, 0/21, —, 0/20 |
| H_EMPTY90 | **FAIL** | 0 of 216 cells lose every candidate at bar 0.90 |

**One pre-registration was restated before commit and the restatement is on the record**: H_CENSUS
first read "≥25% of the picks *whose dial is warm-up-bearing* have live share < 1.0", which is a
tautology and printed 236 of 236 (100.0%). The denominator was changed to every committed dial
value, and the tautological reading is still printed beside it. Nothing else was changed after a
number was read.

## BOOKS NAMED (so the leaderboard row is a book, not a median) — NONE CLAIMED
| chooser | pick | live share | FULL CAGR/Sharpe/MaxDD | halves | OOS CAGR/Sharpe/MaxDD | 4a | 4b |
|---|---|---|---|---|---|---|---|
| BLIND / BAR050 | B136 VROLL L0.12 w252 d1.00 D g1.00 | 0.9940 | 14.11% / 1.173 / −18.06% | 1.167 / 1.180 | 14.93% / 1.306 / −18.06% | no | yes |
| BAR090 | U56 QROLL L0.07 w252 d1.00 W g1.00 | 0.9995 | 13.34% / 1.159 / −15.81% | 0.960 / 1.358 | **16.65% / 1.445 / −13.11%** | no | yes |
| LIVELEG | U56 QROLL L0.17 w1008 d1.00 W g0.75 | 0.6273 | 10.55% / 1.220 / −11.20% | 1.139 / 1.300 | 11.90% / 1.390 / −9.65% | no | no (CAGR) |

None is claimed. They are de-grossing gate arms of the family ideas 834 and 843 already committed
and declined, this run computes **no matched-gross twin**, and 843 showed the best such arm's twin
also passes 4b (exposure, not clause). The BAR090 row's 4b pass is held by an H1 leg of **0.959625 against SPY's
0.959543 — a margin of 0.000082** — which is inside every convention this record has argued about
and is itself a reason not to promote it.

## WHAT THE RECORD SHOULD CARRY
1. **Idea 843's warm-up-blindness generalises.** It is a property of the record's chooser, not of
   QROLL: three families, 83–100% of picks move when the chooser reads the arm's own live leg.
2. **It is a reporting defect, not a lost edge.** Fixing it changes which dial is picked in ~92% of
   cells and the median OOS Sharpe by −0.02. Nobody's capital was hurt by it; the published
   *attribution* of those picks was.
3. **A liveness bar cannot be set at 1.0.** Every rolling dial has warm-up (216 of 216 cells empty),
   so the implementable fix is 843's live-leg chooser, not a strictness screen.
4. **Proposed for Sunday review, NOT applied (rule 6):** PROTOCOL 8a — *a rule-8 pick over a dial
   that is a rolling window must publish the chosen dial's IS LIVE SHARE, and choose on the arm's
   own live leg.* One column, computable before any book is built.

2 tuned parameters (pick set × liveness bar), all 9 points printed on every leg; 2,808 arm rows,
1,080 chooser picks, 2,248 census picks, 70,992 committed re-choices written. Survivorship: U56 and
B136 are current-constituent lists, every LEVEL is optimistic, and no Sharpe or CAGR here is a
capital claim. RULES.md, PROTOCOL.md, research/scan.py, products/bot/bot.py and research/baseline.py
untouched.
