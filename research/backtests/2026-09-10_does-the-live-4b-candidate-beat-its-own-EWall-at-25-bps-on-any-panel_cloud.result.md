# Idea 463 — does the live 4b candidate beat its own EW_ALL at 25 bps on any panel? (cloud, 2026-09-10)

**Verdict: KILL. The 2026-09-04 KEEP 4b candidate's edge over equal weight is a COST-RUNG fact, and
the queue's second clause is the answer. Its breakeven cost is c\* = 20.79 bps on the common window
and 13.62 bps on its own native window — below the rung PROTOCOL already stresses. No rule-8 screen
finds a form that survives, and 4a is 0 of 528 rows.**

## Gates (all PASS, printed before any new number)
| Gate | Result |
|---|---|
| G1 idea 460's premise, off its own imported book builders | U56 TOP20 weekly dSharpe **+0.072777** @10bps (published +0.072778), **−0.028407** @25bps (−0.028406); Sharpe 1.141921/1.029862 (1.141922/1.029863); MaxDD −0.193888 (−0.193888); mean drifted gross 0.726509 (0.726509) |
| G2 `fast_backtest` vs `engine.backtest`, returns AND turnover, at W and M | ≤ **2.8e-17** / **3.3e-16** |
| G3 cost identity r(c) = r0 − turnover·c/1e4 | **0.000e+00** — so every c\* below is exact, not interpolated |
| G4 IS/OOS disjoint and exhaustive | IS 2011-01-13..2016-12-30 (1502d) / OOS 2017-01-03..2026-09-04 (2432d), overlap 0, union = 3934 = full |

## Corpus
10 depths n × 4 cadences × 3 panels = **120 arms** + 12 cadence-matched EW_ALL controls, read at
**0/10/25/50 bps** = 528 rows, all in `.grid.csv`. Two tuned parameters and only two: **n** and
**freq**. Common window 2011-01-13 → 2026-09-04 (15.6y, idea 460's convention so G1 reproduces and
the panels compare); SPY 14.13%/0.8615/−33.72%, halves 0.8907/0.8577, OOS 15.45%/0.8820/−33.72%.

## A1 — which forms beat their own matched EW_ALL at BOTH rungs (full sample)
| panel | @10 bps | @25 bps | BOTH | which |
|---|---|---|---|---|
| U56 | 20/40 | 9/40 | **9/40** | n=3/M, 15/M, 20/M, 25/M, 30/M, 40/W, 40/M, 50/W, 50/M |
| B136 | 5/40 | 0/40 | **0/40** | — |
| SMALL439 | 9/40 | 4/40 | **4/40** | n=5/M, 10/M, 15/W, 20/M |
| pooled | 34/120 | 13/120 | **13/120** | (60/120 at 0 bps, 4/120 at 50 bps) |

**Prediction P1 confirmed and it is the structural point: the survivors are almost all MONTHLY.**
Cadence, not depth, is what carries a ranking edge through a cost rung — the loss between 10 and 25
bps is a turnover loss and cadence is the turnover dial. Note also that **60 of 120 forms do not beat
EW_ALL even at ZERO cost**; for those the question was never a cost question.

## A2 — the breakeven cost c\* (the transferable number)
| arm | c\* | zero-cost edge | turnover |
|---|---|---|---|
| **the live candidate — U56, n=20, weekly, common window** | **20.79 bps** | +0.1401 | **9.09x/yr** vs EW_ALL 0.82x/yr |
| the same on its own NATIVE window (where it was published 2026-09-04) | **13.62 bps** | — | — |
| U56, n=20, **monthly** | 46.91 bps | — | 3.93x/yr |
| U56, n=40, monthly | 64.91 bps | — | 2.17x/yr |

Over the 120 forms, 60 have a crossing inside [0, 200] bps; median c\* **13.3 bps**, and **47 of those
60 cross BELOW 25 bps**. The live candidate pays an **11x turnover ratio** (9.09x vs 0.82x) to buy
0.14 of zero-cost Sharpe, and that trade stops paying at 20.79 bps — 13.62 bps on the window it was
published on. Prediction P3 said 17–18 bps: right about the range, wrong about the window sensitivity.

## A3 — rule 8, and this is the decisive result
Form chosen on 2011–2016 ALONE (S1 = the queue's own criterion: smallest n beating EW_ALL at BOTH
rungs in sample, tie-break lowest IS turnover; S2 = max IS dSharpe at 25 bps, a robustness read),
then 2017–2026 read ONCE.

| panel | IS qualifiers | S1 pick | OOS dSharpe @10 | OOS dSharpe @25 | OOS Sharpe | vs SPY 0.8820 |
|---|---|---|---|---|---|---|
| U56 | 19/40 | n=3/Q | **−0.4383** | **−0.4573** | 0.7407 / 0.7184 | loses |
| B136 | 13/40 | n=3/Q | **−0.1780** | **−0.1997** | 0.9539 / 0.9290 | beats |
| SMALL439 | 1/40 | n=20/M | +0.0776 | +0.0354 | 0.7014 / 0.6509 | loses |

S2 picks n=5/M (U56) and n=3/Q (B136, SMALL439) and fails the same way: U56 OOS dSharpe −0.2644 /
−0.3036. Pooled: picks beating their own EW_ALL out of sample **4/12**; at the 25 bps rung
specifically **2 of 6** non-abstaining picks; **4a 0/12, 4b 0/12**. The one panel where the IS screen
transfers is SMALL439 — the panel whose survivorship bias flatters a *ranked* book most (ranking
concentrates into the survivors), and where the surviving arm still loses to SPY out of sample by
0.23 Sharpe.

## KEEP paths
**4a 0 of 528 rows** (on every panel, every rung). 4b 34/528; 4b AND beats its own EW_ALL 26/528;
**both paths 0**. At the 25 bps rung the population the queue asks for is exactly **2 rows**, both
U56 monthly:

| arm | full CAGR/Sharpe/MaxDD | halves | dSharpe | OOS CAGR/Sharpe/MaxDD | OOS dSharpe | turnover |
|---|---|---|---|---|---|---|
| U56 n=30 /M | 12.67% / 1.1381 / −18.20% | 1.107/1.172 | +0.0589 | 13.99% / 1.1837 / −18.20% | +0.0347 | 2.91x/yr |
| U56 n=40 /M | 10.98% / 1.1575 / −15.20% | 1.088/1.223 | +0.0783 | 12.34% / 1.2367 / −15.20% | +0.0877 | 2.17x/yr |

Both fail 4a on the drawdown leg, and — the point — **neither is found by either rule-8 selector**.
They are full-sample choices, which is precisely the artefact rule 8 exists to catch. Recorded as a
lead for a future idea (a *monthly-cadence deep* book, n ≥ 30), **not** as a KEEP or a PARK promotion.
The near neighbour U56 n=20/M is worth naming too: it beats EW_ALL at 0/10/25 bps (+0.127/+0.100/
+0.059), holds it out of sample (+0.038 at 25 bps) on 3.93x/yr turnover, and fails 4b only on the DD
cap (−21.52% against −20.23%).

## What PROTOCOL should say (recommended wording, NOT applied here)
PROTOCOL edits are Sunday-review business, so this run proposes rather than writes. Suggested
addition to PROTOCOL 4b:

> *Any book that beats an un-ranked equal-weight control must publish its breakeven cost c\* — the
> rung at which that Sharpe advantage crosses zero — alongside the advantage. An edge whose c\* sits
> inside the 10–25 bps range the record quotes is a cost-rung fact and cannot support a KEEP.*

The live candidate would fail that clause on both windows (c\* 20.79 / 13.62).

## Caveats
SURVIVORSHIP (idea 54): all three panels are current-constituent lists; SMALL439 is a sub-$2B screen
run today and back-filled with idea 118's `max_1d_move ≥ 1.0` filter applied first (idea 627: itself
terminal-dated). A ranked book on a survivorship-biased panel is flattered **more** than its
equal-weight control, so every SMALL439 dSharpe here is an upper bound — which matters because
SMALL439 is the only panel where the rule-8 pick transferred. U56 and B136 hold SPY as a constituent
(idea 460's convention, carried verbatim), which shrinks dSharpe. Cadence is not a pure cost dial —
D/W/M/Q change *when* the book sees its signal as well as how often it trades — which is why c\*, an
exact function of drag alone, is the arbiter and cadence is a reported axis. MaxDD is one number off
one path and the 4b DD cap turns on exactly that number (idea 321). Idea 126: t+1, no lag band.
Idea 38: U56/B136 carry the calendar-day index. Idea 460's committed 4b column was the four-bar form;
this file's is the protocol-correct five-bar one, so the two 4b counts are not comparable (the G1
gate targets the Sharpe/MaxDD/dSharpe columns, which are).
