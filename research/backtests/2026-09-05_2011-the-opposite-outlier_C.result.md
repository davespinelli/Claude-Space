# Idea 116 — 2011-the-opposite-outlier — **KILL as posed** (2026-09-05, lane C)

Script `2026-09-05_2011-the-opposite-outlier_C.py`; console `…_C.console.txt`;
CSVs `.grid .picks .swaps .l2o .yearsplit .recut .peryear .walkforward`.

## Question
Idea 112 acquitted 2013 and left 2011 as the open suspect on the other tail. Are rule 8's
parameter picks *effectively chosen by 2011*? What do the 16 ex-2011 swaps cost OOS, and does an
IS window that keeps 2011 but is otherwise re-cut pick the same points?

## Harness
Idea 112's construction imported verbatim: 6 overlay grids (sleeve, band, breadth, stop, crypto,
gross) × 2 books (top20, ewall) × 2 universes (u56, broad) × 2 cost rungs (10/25 bps) = **44
cells**, weekly, next-day execution. Second tuned axis: **46 distinct IS year-sets** — FULL (1),
LOYO (8), leave-two-out (28, all 6 years long), contiguous re-cuts of length 4–8 (15). The OOS
window 2017-01-01 → 2026-09-04 is never touched by any window. All 2 024 window×cell picks are
reported; nothing is selected on the window axis.

## S1 — reproduction (idea 112's committed CSVs read back, not transcribed)
**Exact.** 0 mismatches over 44 cells × 9 windows = **396 pick comparisons**. LOYO change counts
identical year-for-year (2009 11, 2010 6, **2011 16**, 2012 5, 2013 8, 2014 8, 2015 9, 2016 9;
median 8.5). G-leverage table identical to 4 dp (full-IS control −0.058, ex-2011 −0.101). Per-year
pooled overlay d identical (2011 **+0.215**, the sample best; 2013 −0.386, the worst).

**One clause of the premise is FALSE.** QUEUE idea 116 says 2011 is "the only year whose deletion
makes G MORE negative". In idea 112's own `deltas.csv` **four** years do: 2011 (−0.0437), 2014
(−0.0095), 2016 (−0.0092), 2010 (−0.0054). 2011's shift is 4.6× the next largest, so the ranking
survives; the word "only" does not. Withdraw it.

## S2 — the 16 swaps, priced OOS
Mean **dOOS Sharpe −0.033** (idea 112's own swaps.csv: −0.0331), worse in **11/16**, mean dOOS
CAGR **+1.6pp** for **−3.1pp** of OOS drawdown, net **4b −2**, **4b-OOS −3**. Pre-registered sign
test: deleting 2011 *hurts* OOS ⇒ 2011 is a **FEATURE** of rule 8's selector, not a defect. The
mechanism is visible in the swap table: **11 of the 16 swaps turn the defensive dial down** — all
8 sleeve arms (f 0.50→0.25 or 0.25→0.00), both stop arms (0.25→no stop) and gross 0.75→1.00.
Without 2011 in the window the defensive arms stop looking good. The 4 breadth arms move the other
way and the single band arm drops its hysteresis (0.08→0.00), which is not signed either way.
Context: 2016 is joint-worst on the same statistic (−0.033 over 9 swaps).

## S3 — is 2011 the selector? (matched length, 28 L2O windows, per-year null) — **NOT SUPPORTED**
All 28 windows are 6 years long, so only *which* years vary. Agreement of pick(W) with pick(FULL),
split on whether the window keeps year y, pooled over the 44 cells:

| y | A_keep | A_drop | premium | ΔOOS Sharpe | Δregret |
|---|---|---|---|---|---|
| **2011** | **0.756** | **0.588** | **+0.169** | **+0.010** | **−0.010** |
| 2009 | 0.725 | 0.682 | +0.043 | +0.001 | −0.001 |
| 2015 | 0.718 | 0.705 | +0.013 | −0.002 | +0.002 |
| 2016 | 0.715 | 0.711 | +0.004 | +0.006 | −0.006 |
| 2010 | 0.708 | 0.734 | −0.026 | −0.002 | +0.002 |
| 2013 | 0.703 | 0.747 | −0.043 | −0.005 | +0.005 |
| 2014 | 0.696 | 0.769 | −0.074 | −0.002 | +0.002 |
| 2012 | 0.693 | 0.779 | −0.087 | −0.005 | +0.005 |

premium(2011) = **+0.169**, largest of the eight (3.9× the next) but **below the pre-registered
0.20 bar** ⇒ the claim as worded is NOT SUPPORTED. Supplementary, post-hoc: the seven windows that
drop 2011 hold agreement ranks averaging 5.79 of 28 — the five lowest-agreement windows in the
family all drop 2011 (one keep-2011 window ties the fifth at 0.568). Structurally-matched null (which of 8 years is marked) p = 0.125, its floor;
unstructured null (any 7 of 28, 200k draws, seed 0) p = **0.00018**. So 2011's uniqueness is real;
what it misses is the *size* bar.

## S4 — the price of that dependence
Keeping 2011 is worth **+0.010** of mean OOS Sharpe and **−0.010** of mean OOS regret. Mean regret
across the whole design is 0.018–0.028 — there is almost nothing for a selector to get wrong here,
which independently reproduces idea 114's finding (mean OOS regret 0.015, rule 8 already OOS-best
in 16/44 cells). A dependence this strong and this cheap is a curiosity, not a defect.

## S5 — contiguous re-cuts (the queue's second clause) — **explained by length, not by 2011**
Re-cuts containing 2011 agree 0.682 vs 0.568 without — but agreement is monotone in window length
(4y 0.577, 5y 0.608, 6y 0.674, 7y 0.773, 8y 1.000) and the 2011-containing spans average 5.6 years
against 4.3. The three spans that omit 2011 are all short by construction. The controlled answer is
S3's +0.169.

## Rule-8 walk-forward (mandatory), 44 cells × 46 windows, OOS 2017–2026
| window set | n | OOS Sharpe | OOS CAGR | OOS MaxDD | 4a /44 | 4b /44 | 4b-OOS /44 |
|---|---|---|---|---|---|---|---|
| **FULL (rule 8 as written)** | 44 | **1.048** | 13.3% | −19.7% | 17 | **20** | **22** |
| LOYO ex2011 | 44 | 1.036 | 13.9% | −20.8% | 16 | 18 | 19 |
| L2O keeps 2011 | 924 | 1.045 | 12.9% | −19.2% | 19.4 | 17.6 | 20.6 |
| L2O drops 2011 | 308 | 1.035 | 13.8% | −20.7% | 16.1 | 18.3 | 20.0 |
| RECUT keeps 2011 | 528 | 1.036 | 13.1% | −19.5% | 18.4 | 18.3 | 21.6 |
| RECUT omits 2011 | 132 | 1.027 | 14.2% | −21.3% | 15.3 | 16.7 | 18.7 |

SPY (both panels): full 15.2% / 0.889 / −33.7%; OOS 15.5% / 0.882 / −33.7%. RULES v1 (u56, 10 bps)
is the baseline in `.walkforward.csv` per cell. **Rule 8's own window is the best of all 46** on
OOS Sharpe and on both 4b counts — no re-cut improves on it.

Headline cell (u56 / top20 / sleeve / 10 bps — the standing KEEP-4b candidate). Windows picking
each f, of 46: f=0.00 → 6, f=0.25 → 8, **f=0.50 → 28**, f=0.75 → 4, f=1.00 → 0.
f=0.50 reads 12.3% / **1.180** / −14.3% (H1 1.161, H2 1.200), OOS 13.6% / **1.261** / −14.3%.
**Standing KEEP-4b candidate untouched** — it is the modal pick under a 46-window sweep of the IS
definition, and the one window that most reliably unseats it (drop 2011) is also the one that costs
the most OOS.

## Verdict
**KILL as posed.** 2011 is uniquely the pick-moving year (16/44, p = 0.00018 on the unstructured
null) — but it is not "choosing" rule 8's picks in any sense that matters: the premium misses its
pre-registered bar, its influence is worth **+0.010** OOS Sharpe *in the right direction*, and
rule 8's full window beats every one of the 45 alternatives. One premise clause ("the only year")
is withdrawn as false. No RULES change, no new KEEP, no PROTOCOL change proposed.

## Caveats
Survivorship (both panels are current constituents; identical across every window compared).
2009 is a partial year (~11.5 months after the 260-row warm-up). Crypto arms are near-inert on
windows ending before 2014-09-17 (BTC's first row) and are shown in and out of every pooled stat.
Calendar-day index (queue idea 38) hits every window identically. Sharpe on a spliced series is
idea 89's convention; MaxDD is never taken on one.
