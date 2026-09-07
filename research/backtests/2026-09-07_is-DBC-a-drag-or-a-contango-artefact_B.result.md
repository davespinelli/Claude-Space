# Idea 106 — is-DBC-a-drag-or-a-contango-artefact (lane B, 2026-09-07)

**Verdict: SPLIT. The queue's CONCLUSION is confirmed and the queue's stated MECHANISM is
falsified. Idea 104's "drop DBC" arm is contango-conditioned and is mis-specified in exactly
the gross convention it was booked in. No new KEEP; rules unchanged.**

Script `2026-09-07_is-DBC-a-drag-or-a-contango-artefact_B.py`, 120 grid points at 10 bps (all
reported, `.grid.csv`), 600 cost-ladder points (`.ladder.csv`), 32 matched S4-vs-noDBC gaps
(`.gaps.csv`), 10 boundary-sensitivity points (`.boundary.csv`), 8 attribution rows
(`.attrib.csv`), 8 rule-8 cells (`.walkforward.csv`), console in `.console.txt`.

Tuned (2): sleeve in {S4, noDBC, DBConly} x f in {0, 0.25, 0.50, 0.75, 1.00}. Controls
(reported, never selected on): universe {u56, broad}, book {top20, ewall}, gross convention
{natural, g=1.00}, cost {5,10,15,20,25} bps. Sleeve construction is idea 18 variant B copied
verbatim from idea 102's script. Sub-period boundary **pre-registered at 2014-01-01** from the
queue's own wording; four alternatives swept as a reported robustness check.
Cost-linearity gate vs `engine.backtest` at 10 bps: **max |derived - direct| = 0.00e+00**.

---

## 1. The queue's premise is wrong on the return side

DBC's contribution inside the S4 sleeve (sum of lagged weight x return, pp of the sleeve's
cumulative simple return), identical to 3 s.f. on both panels:

| asset | total pp | 2009-2013 | 2014-2026 | share | mean weight |
|---|---|---|---|---|---|
| TLT | +5.63 | +1.00 | +4.63 | 9.1% | 0.119 |
| GLD | +33.22 | +12.22 | +21.01 | 53.5% | 0.125 |
| **DBC** | **+10.39** | **+1.66** | **+8.72** | 16.7% | 0.090 |
| UUP | +12.87 | -2.94 | +15.82 | 20.7% | 0.247 |

The **+10.4pp reproduces idea 102 exactly**, but the queue's "its dead years are 2009-2013" is
false as stated: DBC's 2009-2013 contribution is **+1.66pp, positive**, and **84% of its total
arrives after 2014**. Its actually-negative years are 2012-2015 and 2023-2025. What *is* true
is the standalone reading the queue was reaching for — DBC held alone (f=1, DBConly) earns
**CAGR +0.2% / Sharpe 0.075 in 2009-2013** vs **+4.6% / 0.440 after** — the trend vote simply
kept the sleeve out of the worst of the contango bleed, so the era shows up as a *risk* cost,
not a return cost.

## 2. The drag is nonetheless entirely front-loaded — the conclusion holds

gap = Sharpe(noDBC) - Sharpe(S4) at matched (universe, book, convention, f), 32 cells, f>0:

| window | cells positive | mean gap | min | max |
|---|---|---|---|---|
| full sample | 22/32 | **+0.0055** | -0.0996 | +0.0628 |
| contango era (-2013) | **32/32** | **+0.0658** | +0.0052 | +0.1351 |
| post-2014 | 17/32 | **-0.0201** | -0.1917 | +0.0542 |
| OOS 2017+ | 12/32 | **-0.0458** | -0.3092 | +0.0625 |

Unanimous in the contango era, a coin flip after it, negative on average out of sample. noDBC
does trade lower: turnover falls in **32/32** cells (mean -0.196 /yr), so idea 102's turnover
claim survives intact — it is the Sharpe claim that does not.

**Boundary sensitivity (reported, never selected on):** the mean post-boundary gap decays
monotonically as the start date is pushed out — u56 -0.0057 / -0.0120 / -0.0168 / -0.0482 /
-0.0491 and broad -0.0107 / -0.0178 / -0.0233 / -0.0534 / -0.0560 for boundaries 2012 / 2013 /
2014 / 2015 / 2016. The verdict does not hinge on the pre-registered 2014 cut; every
alternative is worse for the prune.

## 3. The convention split lands exactly on idea 104's arm

| convention | gap_full | gap_contango | gap_post | gap_oos |
|---|---|---|---|---|
| natural | +0.0246 (12/16) | +0.0490 (16/16) | +0.0188 (12/16) | **+0.0135 (12/16)** |
| g=1.00 | -0.0137 (10/16) | +0.0826 (16/16) | -0.0589 (5/16) | **-0.1052 (0/16)** |

Idea 101/104's candidate is stated at **g=1.00**, and that is the convention in which deleting
DBC loses out of sample in **16/16** cells. In its own cell (top20, g1.00, f=0.50):

| universe | sleeve | CAGR | Sharpe | MaxDD | H1/H2 | CON | POST | OOS Sharpe | turn/yr | 4a | 4b |
|---|---|---|---|---|---|---|---|---|---|---|---|
| u56 | S4 | 11.8% | 1.149 | -14.2% | 1.099/1.197 | 1.065 | 1.184 | **1.236** | 12.50 | no | **yes** |
| u56 | noDBC | 11.5% | 1.167 | -13.3% | 1.169/1.167 | 1.135 | 1.180 | **1.215** | 12.42 | no | **yes** |
| broad | S4 | 12.2% | 1.063 | -15.6% | 1.173/0.961 | 1.297 | 0.968 | **1.020** | 15.32 | no | **yes** |
| broad | noDBC | 12.0% | 1.073 | -14.6% | 1.245/0.917 | 1.379 | 0.951 | **0.985** | 15.23 | no | **yes** |

Both arms pass 4b in the same four cells; noDBC's entire full-sample edge is ~1pp of MaxDD
and ~0.01-0.02 of Sharpe bought in 2009-2013, and it is **behind on OOS Sharpe in all four**.
Idea 104's "S3 beats S4 on 4a in 2/2 universes at all 5 cost rungs" was judged against
**RULES v1**; against the live **RULES v2** baseline the whole grid yields **4a 2/120** and both
passers are noDBC at natural gross on the **broad** panel only (top20 f=0.50: 8.0%/1.124/-10.8%,
H1 1.257/H2 1.014; ewall f=0.50: 6.8%/1.252/-10.3%, H1 1.316/H2 1.195). They fail on u56, die
by 15 bps (4a passes by rung 6/2/1/0/0 at 5/10/15/20/25 bps), and earn less than half of SPY's
CAGR — **PARK-grade at best, not a KEEP**, and this run is the reason to distrust them.

## 4. Rule 8 walk-forward ((sleeve, f) on 2009-2016 IS Sharpe, 2017-2026 read once)

The chooser **mis-picks exactly as predicted** — its IS window is 62% contango era, and it
picks noDBC in **8/8** cells at f=0.50 in 8/8. Out of sample the pick beats **SPY 8/8** but
**RULES v2 only 4/8**, and gives up 5-9pp of SPY's 15.5% OOS CAGR (7.0-12.3%).

| universe | book | conv | pick | OOS CAGR | OOS Sharpe | OOS MaxDD | RULES v2 OOS | SPY OOS | gap noDBC-S4 |
|---|---|---|---|---|---|---|---|---|---|
| u56 | top20 | natural | noDBC f=.50 | 8.8% | 1.345 | -9.8% | 1.285 | 0.882 | +0.037 |
| u56 | top20 | g1.00 | noDBC f=.50 | 12.3% | 1.215 | -13.3% | 1.285 | 0.882 | **-0.021** |
| u56 | ewall | natural | noDBC f=.50 | 7.3% | 1.330 | -8.7% | 1.285 | 0.882 | +0.050 |
| u56 | ewall | g1.00 | noDBC f=.50 | 10.2% | 1.233 | -11.8% | 1.285 | 0.882 | **-0.014** |
| broad | top20 | natural | noDBC f=.50 | 8.0% | 1.070 | -10.8% | 1.119 | 0.882 | +0.017 |
| broad | top20 | g1.00 | noDBC f=.50 | 11.1% | 0.985 | -14.6% | 1.119 | 0.882 | **-0.035** |
| broad | ewall | natural | noDBC f=.50 | 7.0% | 1.266 | -10.3% | 1.119 | 0.882 | +0.035 |
| broad | ewall | g1.00 | noDBC f=.50 | 9.8% | 1.184 | -13.1% | 1.119 | 0.882 | **-0.016** |

OOS gap noDBC-S4 with each sleeve at its own IS-best f: mean **+0.0066, positive 4/8** — a coin
flip, split perfectly 4/4 natural-positive vs 4/4 g1.00-negative. Rule-8 picks: 4a 2/8, 4b 2/8.

## 5. KEEP paths (both, whole grid, 10 bps)

**4a (vs RULES v2, live): 2/120. 4b (vs SPY): 17/120.** 4b passers split 7 S4 / 7 noDBC /
3 DBConly, and every DBConly pass is at f=0 or f=0.25 where the book dominates. Cost ladder,
pooled passes at 5/10/15/20/25 bps: 4a **6/2/1/0/0**, 4b **31/17/13/9/3**. By sleeve at 10 bps:
4a S4 0, noDBC 2, DBConly 0; 4b S4 7, noDBC 7, DBConly 3. **The two arms are indistinguishable
on the path that matters for capital.**

## 6. What this changes

- **Do not prune DBC on idea 102/104's evidence.** The deletion gain is unanimous only in
  2009-2013, is a coin flip after, and is negative OOS in the g=1.00 convention idea 101/104's
  candidate is written in. Idea 104's "second arm" verdict is **mis-specified**, as the queue
  suspected — for the right reason (front-loading) but not the stated one (dead years).
- **Idea 102's turnover finding stands** (noDBC lower in 32/32, -0.196 /yr) and is the only
  defensible reason left to prefer the prune; it is worth ~0.02 of Sharpe at 10 bps and is
  swamped by the -0.105 OOS Sharpe cost at g=1.00.
- **The standing candidate is unchanged:** `top20 + 50% (TLT,GLD,DBC,UUP)` at g=1.00 keeps its
  4b pass on both panels; nothing here beats it and nothing here promotes S3 over it.

## Stated limits

- SURVIVORSHIP: both panels are current constituents; equity levels biased up. Sleeve assets
  are ETFs and are not exposed.
- Queue idea 38: `data/prices*.csv` is calendar-day-indexed after 2014-09-17, so the two
  sub-periods are indexed differently and **absolute cross-era Sharpe levels are not
  comparable**. Every statistic this run judges on is a within-sub-period difference between
  two arms on identical days, which is immune to it.
- "Contango era" is a label taken from the queue, not an independently measured roll-yield
  series; the run tests a date split, not a curve-shape regime. A roll-yield-conditioned
  version is a natural follow-up.
