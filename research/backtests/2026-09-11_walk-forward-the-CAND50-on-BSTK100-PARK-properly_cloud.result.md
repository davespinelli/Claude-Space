# Idea 702 — walk-forward the CAND50-on-BSTK100 PARK properly

**Run:** 2026-09-11 UTC, cloud. **Script:** `2026-09-11_walk-forward-the-CAND50-on-BSTK100-PARK-properly_cloud.py`

**Verdict: PARK RESOLVED — SPLIT, NO KEEP. The 4b row IS reachable by an IS-honest rule, but by
exactly one of six, on one of two equally defensible calendars, at one of three cost rungs, and a
ZERO-SIGNAL book reaches the same bar MORE often.** Idea 694's headline cell (n=50, g=0.75) is
**not** reachable by any honest selector; the one cell that is reachable is **n=60, g=0.75**.
No book is promoted, no memo is written; RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py
are untouched.

## Gates (pre-registered, printed before any new number was read)

| Gate | Result |
|---|---|
| G0 idea 694's published cell + its IS-picker claim | CAND50 @0.75 = **0.1166 / 1.0634 / −0.1871**, halves **1.1481 / 0.9856**, OOS **0.1210 / 1.0778 / −0.1871**; SPY **0.1413 / 0.8616 / −0.3372**; IS n-picker **n=15, OOS S 0.9318**. worst \|d\| **4.43e-05** (bar 5e-04) **PASS** |
| G1 envelope (SPY never held, w ≥ 0, gross ≤ g·(1+3/n)) | **PASS**, 33/33. 171 tie cell-days of 33×817 (pandas' average tie rank lets the inherited book hold n+1 lots); worst overshoot 0.20·g at n=5 |
| G2 de-grossing identity, realised gross == g·mean(held)/n | worst **1.44e-15** (bar 1e-12) **PASS**; the capacity reading g·mean(min(n_elig,n))/n differs by ≤ **8.32e-03**, i.e. the tie days and nothing else |
| G3 zero-signal control (same envelope, random names) | ran, reported below |

**RECORD CORRECTION.** The queue describes CAND50 as "n = 50 against mean eligibility ~31". On
the whole BSTK100 pool eligibility averages **Ē = 68.44** of 100 on a rebalance day (native
calendar 67.14), and the record's own committed artefact agrees: idea 525's `.named.csv` carries
**BSTK100 Ē = 66.17, breadth 0.6617**. The ~31 is not BSTK100's eligible count under any reading
this run can reproduce. The consequence is that **only n ∈ {75, 100} is capacity-bound** here,
not n = 50: CAND50's realised fill is **0.9516**, i.e. the book runs at 0.714 of NAV against a
nominal 0.75. The de-grossing the PARK is named for is real but **5%, not 40%** — and at n = 100
it is 0.6838, which is where it starts to matter.

## The grid (33 cells, all reported; 10 bps, weekly, t+1)

| | 4a-REC | 4b-REC | 4a-OOS | 4b-OOS | 4b-IS |
|---|---|---|---|---|---|
| 33 cells | **0** | **6** | **0** | **4** | 7 |

4b-REC passers: n = 30/40/50/60/75 **all at g = 0.75**, plus n=100 @ g=1.00.
4b-OOS passers: n = 30/40/50/60 at g = 0.75. Comparands on the same panel and calendar:
RULES v2 **8.67% / 1.1292 / −12.76%** (OOS 8.80% / 1.1404 / −12.76%), SPY **14.13% / 0.8616 /
−33.72%** (OOS 15.45% / 0.8820 / −33.72%).

## Rule 8 — six IS-only selectors, read once on 2017-01-01..

| selector | pick | OOS CAGR / Sharpe / MaxDD | > SPY OOS S | > v2 OOS S | 4b-REC | 4b-OOS |
|---|---|---|---|---|---|---|
| S1 PICK-n @0.75 by IS Sharpe | n=15, g=0.75 | 13.98% / 0.9318 / −21.15% | yes | no | no | no |
| S2 PICK-n @0.75 by IS Calmar | n=15, g=0.75 | 13.98% / 0.9318 / −21.15% | yes | no | no | no |
| S3 PICK-(n,g) by IS Sharpe | n=15, g=1.00 | 18.52% / 0.9337 / −27.59% | yes | no | no | no |
| S4 PICK-(n,g) by IS Calmar | n=15, g=1.00 | 18.52% / 0.9337 / −27.59% | yes | no | no | no |
| **S5 PICK-4b-IS then IS Sharpe** | **n=60, g=0.75** | **11.80% / 1.1305 / −17.07%** | yes | no | **YES** | **YES** |
| S6 PICK-(n,g) by IS MaxDD | n=100, g=0.50 | 5.20% / 1.1022 / −8.51% | yes | no | no | no |
| ORACLE (not honest) | n=60, g=0.50 | 7.84% / 1.1315 / −11.57% | yes | no | no | no |
| RECORD (idea 694, not honest) | n=50, g=0.75 | 12.10% / 1.0778 / −18.71% | yes | no | yes | yes |

**Reaching 4b: 1 of 6 honest selectors.** Every honest selector beats SPY's OOS Sharpe; **none**
beats RULES v2's (0/6). The record's own n=50 is not among the four cells the honest selectors
land on — {(15, 0.75), (15, 1.00), (60, 0.75), (100, 0.50)}.

## Why this is a SPLIT and not a KEEP

1. **Zero-signal control.** Random names inside the identical de-grossing envelope give 4b-REC
   2/33 and 4b-OOS 1/33, and **3 of its 6 honest selectors reach 4b-REC** against the signal
   book's 1. Reaching 4b-REC is therefore not evidence of signal at all. Only on the strict
   OOS-window reading does the control fail where the book passes (control 0/6, signal 1/6),
   and one cell is one cell.
2. **Cost.** At **25 bps**: 4b-REC 2/33, 4b-OOS 1/33, honest selectors reaching either **0/6**.
   At **50 bps**: 4b 0/33 on both readings. The single pass survives only at PROTOCOL's 10 bps.
3. **Calendar.** Idea 694's calendar (broad ∩ small panel, from 2010-01-04) is a by-product of a
   run that needed the small panel. On BSTK100's **native** calendar (2008-01-02, +2 years, the
   same data) 4b-REC falls to 4/33 and **0 of 6** honest selectors reach it — S1 moves from n=15
   to n=75 and S5 from n=60 to n=75 @ g=1.00, which does not pass. The one pass is contingent on
   a convention nobody chose for this question.
4. **Survivorship.** BSTK100 is the current constituent list of `universe_broad.json` minus ETFs;
   names that left the large-cap universe over 2010–2026 are absent, so every level is optimistic
   and the gated book's more so.

## What the PARK actually was

The grid's 4b passes are **a gross window, not an n window**: five of six sit at exactly
g = 0.75 and the sixth at g = 1.00 with n = 100. At g = 0.50 the CAGR floor (0.70 × 14.13% =
9.89%) bites — every g=0.50 cell tops out at 9.51% — and at g = 1.00 the DD cap
(0.60 × −33.72% = −20.23%) bites for every n ≤ 60. That reproduces idea 677's gross-window
reading on a fresh family: what looked like "CAND50 is special" is "0.75 is the gross at which
both bars are clear at once", and n only has to be large enough (≥ 30) to hold the drawdown down.

## Survivorship & scope

Levels here are optimistic (current constituents). The object adjudicated is whether an IS-only
rule can REACH a published 4b row, which is a within-grid statement and not a level claim. No
arm here is a capital candidate.
