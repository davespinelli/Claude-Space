# Idea 825 — is QROLL-ON-TOP an entirely POST-2017 fact?
cloud lane, 2026-09-12, idea 1 of 2 · script `2026-09-12_is-QROLL-ON-TOP-an-entirely-POST-2017-fact_cloud.py`

**ANSWER: YES at the record's own split — and the PRE-leg statistic is not sign-stable on any
reported axis, so "QROLL's advantage before 2017" is not a quantity the record can quote at all.**
No KEEP claimed, no book promoted, no memo. `RULES.md`, `PROTOCOL.md`, `research/scan.py`,
`products/bot/bot.py`, `research/baseline.py` untouched.

## The headline (split 2016-12-31, famset FULL = idea 605's corpus, 10 bps, FULLMATCH, POOLED)

| leg | window | ABS | QEXP | QROLL | adv = QROLL − max(ABS,QEXP) | order |
|---|---|---|---|---|---|---|
| PRE  | ..2016-12-31 | 0.3333 | 0.5833 | 0.5231 | **−0.0602** | QEXP > QROLL > ABS |
| POST | 2017-01-01.. | 0.7407 | 0.6481 | 0.9722 | **+0.2315** | QROLL > ABS > QEXP |

The PRE order is exactly idea 609's IS modal (QEXP > QROLL > ABS); the POST leg is the published
one with QROLL at 0.9722. So the *ordering* claim is a second-window fact.

The *advantage over the gross-matched control* is a different and weaker claim, and it does
survive: QROLL beats its own static-gross twin on **0.5231** of pre-2017 arms — more often than
not, just not more often than QEXP. H_PRE and H_PREPOS were pre-registered separately for exactly
this reason; the first FAILS, the second PASSES.

## 2 of 9 pre-registered hypotheses PASS

| | verdict | evidence |
|---|---|---|
| H_PRE QROLL strictly on top on the PRE leg | **FAIL** | adv_PRE −0.0602 |
| H_PREPOS win[QROLL] > 0.50 on the PRE leg | **PASS** | 0.5231 |
| H_GAP \|adv_PRE − adv_POST\| ≤ 0.20 | **FAIL** | 0.2917 |
| H_SPLITFREE sign(adv_PRE) constant over 5 splits | **FAIL** | 2012 +0.0926, 2014 −0.3426, 2016 −0.0602, 2018 +0.1343, 2020 +0.3079 |
| H_FAMSET sign constant over 4 family sets | **FAIL** | FULL −0.0602, SHORT −0.2130, LONG +0.0926, BAL −0.1204 |
| H_COSTINV sign constant over 0/10/25 bps | **FAIL** | +0.1528 / −0.0602 / −0.1366 |
| H_MATCH \|FULLMATCH − WINMATCH\| ≤ 0.10 | **PASS** | −0.0602 vs −0.0046, \|d\| 0.0556 |
| H_PANEL sign agrees across panels | **FAIL** | U56 +0.0417, B136 −0.0694, SMALL663 −0.2917 |
| H_R8CLAIM rule 8 on the claim | **FAIL** | famset picked on the PRE leg = LONG (+0.0926); read ONCE on POST +0.2222, gap 0.1296 |

## Why it is a window fact and not a corpus fact

`adv_PRE` rises monotonically as the PRE leg absorbs more post-2017 data — Spearman(split date,
adv_PRE) **+0.70** over the five splits (+0.5152 over all 20 tuned points), while
Spearman(split date, adv_POST) is **−0.70** (−0.6486 over 20): every day of post-2017 data moved
from POST to PRE takes the advantage with it. `win[QROLL]` on the PRE leg tracks the same way,
0.4907–0.5926 at splits ≤ 2016 against 0.7361–0.9005 at splits ≥ 2018.

Across **all 960 cells** (20 tuned points × 3 rungs × 2 matchings × 4 scopes): QROLL is on top in
290 of 480 PRE cells (0.604) against 368 of 480 POST cells (0.767), and the PRE leg's modal order
is QROLL > QEXP > ABS only 151/480 times with 92 TIED, against 238/480 for QROLL > ABS > QEXP on
the POST leg. At the headline rung 13 of 20 tuned points have adv_PRE > 0 and **20 of 20** have
adv_POST > 0 — the POST leg never once fails to put QROLL on top, the PRE leg fails 7 times and
flips sign on split, famset, cost and panel alike.

## Gates

G1 `fast_run` == `engine.backtest` max|d| 1.0e-17 PASS · G2 fast metrics == `engine.metrics` 0.0e+00
PASS · G3 0.01-grid twin interpolation |dSharpe| 2.0e-08 PASS · G5 whole-sample leg == full-sample
win rates max|d| 0.0 PASS.

G4 (full-sample order = idea 605's QROLL > QEXP > ABS) **PASSES POOLED at 0/10/25 bps** (QROLL
0.9769 / 0.9491 / 0.8727) and on B136 and SMALL663 at all three rungs, but **FAILS on U56 alone**:
there the order is QROLL > ABS > QEXP at 0 and 10 bps and TIED at 25 (ABS 0.6667 = QEXP 0.6667).
Reported, not tolerated: the published order is a pooled fact, and one of the record's three
panels does not carry its weak leg.

## PROTOCOL rule 8 on the books, and both KEEP paths (10 bps, 108 rule-8 picks)

Dial (level, w) chosen on IS ≤2016-12-31 by IS Sharpe; OOS 2017-01-01.. read once.

| panel | family | OOS CAGR | OOS Sharpe | OOS MaxDD | 4b passes |
|---|---|---|---|---|---|
| U56 | ABS / QEXP / QROLL | 12.83% / 12.57% / 12.51% | 1.163 / 1.066 / **1.194** | −17.7% / −19.1% / −17.3% | 3/12, 0/12, 3/12 |
| B136 | ABS / QEXP / QROLL | 11.58% / 12.22% / 11.31% | 1.019 / 1.010 / **1.099** | −20.2% / −20.4% / −15.6% | 0/12, 6/12, 6/12 |
| SMALL663 | ABS / QEXP / QROLL | 3.49% / 3.91% / 4.77% | 0.330 / 0.328 / **0.405** | −32.2% / −41.8% / −32.0% | 0/12 each |

Comparands on the same OOS window: SPY 15.33% / 0.877 / −33.72%; RULES v2 (live) 9.47% / 1.278 /
−12.05% on U56. Full sample: SPY 15.16% / 0.886 / −33.72%.

Full-sample KEEP tallies over all 1,944 (panel, arm, rung) rows: **4a 3/1944** (all B136 at 0 bps),
**4b 490/1944** — 162/67/24 on U56 and 143/74/20 on B136 at 0/10/25 bps, and **0/216 on SMALL663 at
every rung**. Rule-8 picks: 4a 3/324, 4b 68/324. At 10 bps 114 of the 141 full-sample 4b passers
are QROLL, but the best of them (U56 `QROLL q0.07 w252 d1.00 D g1.00`, OOS 16.49% / 1.449 /
−13.90%) has a **matched-gross twin that also passes 4b** — an exposure pass, not a clause pass.
45/216 U56 and 13/216 B136 4b passers at 10 bps share that defect; at 25 bps none do.

## Caveats

SURVIVORSHIP: all three panels are current-constituent lists, so every level is optimistic and
SMALL663 worst — a sub-$2B screen read today cannot see the names that fell out of it
(`data/SMALL_PANEL_README.md`); 52 tickers with `max_1d_move ≥ 1.0` were dropped before anything was
computed. A win rate is a within-panel agreement rate, which survivorship moves far less than a
level, but no Sharpe or CAGR here is a capital claim on its own. Idea 609 already established that
605's POOLED win-rate *levels* are not reproducible today (the small panel grew from 439 to 663
names), so this run gates on the ORDER and says so.

## Follow-ups filed
834 (is the same PRE/POST asymmetry present in the ABS family, i.e. is it QROLL's or the window's),
835 (does any de-grossing family beat its twin on a leg that contains no 2020 drawdown).
