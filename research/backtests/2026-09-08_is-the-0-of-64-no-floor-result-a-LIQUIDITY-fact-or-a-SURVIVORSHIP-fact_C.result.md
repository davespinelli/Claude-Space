# Idea 435 — is-the-0-of-64-no-floor-result-a-LIQUIDITY-fact-or-a-SURVIVORSHIP-fact

lane C, 2026-09-08 · `2026-09-08_is-the-0-of-64-no-floor-result-a-LIQUIDITY-fact-or-a-SURVIVORSHIP-fact_C.py`
· 10,080 grid points + 96 seed-replication cells · runtime 1,181 s

## Answer

**LIQUIDITY FACT. Idea 428's 0/64 survives, and the queue's own survivorship diagnosis of
SMALL439 is FALSIFIED.** It takes a **20.1 %/yr** haircut on the thinnest decile of U56 to flip the
sign (median h\*, all 48 cells cross, range 16.70–24.60 %), against a plausibility band of 5 %/yr
declared before any number was read: **0 of 48 U56 cells flip inside the band.** On SMALL439 —
the panel the queue says survivorship should explain — h\* is **larger, not smaller**: 26.95 % and
only for the `PXL`/d=3 arms; the `DV` and `VOLSH` arms do not cross by 30 %/yr at all
(**0 of 144 inside the 10 % band**).

## The measurand, and why a flip is not a finding

h\* — the haircut on the thin cohort at which the rule-8 floor chooser starts beating the no-floor
control OOS — **always exists** (as h grows the no-floor arm holds a progressively poisoned cohort
that the floor arm avoids), so the deliverable is never "it flips" but the **SIZE** of h\*. That
asymmetry, and the plausibility band, were both written into the script header before Q3–Q7 ran.

## Reproduction gate (binds before any new number)

| gate | result |
|---|---|
| `fast_bt_r(h=0)` vs `engine.backtest` | max\|diff\| **6.9e-18** |
| `fast_bt_r(h=0)` vs idea 428's `fast_bt` | **0.000e+00** |
| h=0 walk-forward vs 428's committed `walkforward.csv`, 64 shared cells | max\|diff\| **2.220e-16**, identical picks **64/64** |
| 428's headline re-read here | chooser beats no-floor **0/64** (published 0/64); mean edge **−0.1651** Sharpe, **−2.338 pp** CAGR |
| LIVE RULES v2 on U56 @10 bps | 8.66 % / 1.2056 / −12.05 % (published identically) |

## The two tuned parameters, and the two readings

Exactly two: the **haircut h** ∈ {0, 1, 2, 3, 5, 8, 12, 20, 30} %/yr and the exposed **decile
breadth d** ∈ {1, 2, 3}. Everything else is idea 428 verbatim (panels, keys, matched-admission
ladder, EWALL/MA200 × rw/dg, 0/5/10/25 bps, IS 2010–2016 / OOS 2017–2026). The floor **level** is
not free — it is chosen inside the rule-8 block on the IS window only, exactly as 428 chose it.

* **Reading A (DRAG, primary).** Exposed name-days' gross return × (1−h)^(1/252). Masks, keys,
  gates and floor levels come from the OBSERVED prices and are identical at every h, so each
  (h, d) is a *paired* re-pricing of the same books on the same days.
* **Reading B (EVENT, secondary).** Shumway-style −30 % terminal shock at hazard λ = h/0.30, name
  dead thereafter (price NaN, mask False, proceeds in cash). λ is **solved from h**, so reading B
  introduces no third parameter: its expected annual drag equals reading A's h by construction.

Exposed cohort = bottom d deciles of the daily 20d-median-price cross-section — the same key a PXL
floor cuts on. Lever arm at d=1 (share of the poisoned cohort the floor actually gates): U56
0.79 → 1.00 along the ladder; SMALL439 1.00 at every rung.

## Reading A — the primary answer

Cells where the IS floor chooser beats the no-floor control OOS (64 per (h, d); U56 is 16 of them):

| h | d=1 | d=2 | d=3 | U56 d=1 | U56 d=2 | U56 d=3 |
|---|---|---|---|---|---|---|
| 0 % | 0/64 | 0/64 | 0/64 | 0/16 | 0/16 | 0/16 |
| 3 % | 0/64 | 0/64 | 0/64 | 0/16 | 0/16 | 0/16 |
| 5 % | 0/64 | 0/64 | 0/64 | 0/16 | 0/16 | 0/16 |
| 8 % | 0/64 | 0/64 | 0/64 | 0/16 | 0/16 | 0/16 |
| 12 % | 0/64 | 0/64 | 0/64 | 0/16 | 0/16 | 0/16 |
| 20 % | 6/64 | 8/64 | 6/64 | 6/16 | 8/16 | 6/16 |
| 30 % | 16/64 | 16/64 | 32/64 | 16/16 | 16/16 | 16/16 |

**Nothing moves anywhere below 20 %/yr.** Mean OOS Sharpe edge on U56 walks −0.0730 (h=0) →
−0.0576 (5 %) → −0.0480 (8 %) → −0.0063 (20 %) → +0.0336 (30 %); on SMALL439 it is still
−0.1234 at 30 %.

h\* by cell (linear interpolation in h, all cost rungs and book-forms reported):

| panel | inst | d | crossed ≤30 % | median h\* | min | max | band | inside |
|---|---|---|---|---|---|---|---|---|
| U56 | PXL | 1 | 16/16 | **21.84 %** | 19.11 % | 24.60 % | 5 % | **0/16** |
| U56 | PXL | 2 | 16/16 | **18.83 %** | 16.70 % | 20.86 % | 5 % | **0/16** |
| U56 | PXL | 3 | 16/16 | **20.27 %** | 19.25 % | 23.51 % | 5 % | **0/16** |
| SMALL439 | PXL | 3 | 16/16 | 26.95 % | 26.35 % | 28.23 % | 10 % | 0/16 |
| SMALL439 | PXL 1–2, DV 1–3, VOLSH 1–3 | | **0/16 each** | n/a | | | 10 % | 0/16 |

## Pre-registered predictions: 1 of 4 holds

* **P1 (h\* decreasing in d) — FAILS on U56.** Median h\* is non-monotone: 21.84 → 18.83 → 20.27.
  Widening the poisoned cohort past the second decile stops helping, because the extra names are
  ones the *floor also holds* (gated-is-exposed rises 0.38 → 0.83 while exposed-is-gated falls
  0.79 → 0.55). The channel saturates.
* **P2 (h\* smaller on SMALL439) — FAILS.** U56 20.11 % vs SMALL439 26.95 %, the wrong way round.
  The queue's diagnosis — "on SMALL439 that is exactly what a current-constituents panel would
  produce" — does not survive being priced: SMALL439's floor penalty is 2.7× U56's
  (−0.1957 vs −0.0730 Sharpe), so it needs *more* correction, not less.
* **P3 (plausibility) — HOLDS, and decides the verdict.** 0/48 U56 and 0/144 SMALL439 cells inside
  their bands under reading A.
* **P4 (4b passes weakly decreasing in h) — HOLDS, 432/432 book-tracks monotone.**

## Reading B — the removal channel is real, and dies on the seed test

At matched expected drag the EVENT reading flips cells 2–3× earlier (U56 median h\* 8.33 % / 9.64 %
/ 2.43 % by d; 4/16, 8/16, 8/16 cells inside the 5 % band on seed 435). So the **removal**
channel — the panel shrinking, the path breaking — and not the return correction, is what actually
moves the sign. But reading B is stochastic, and over 8 seeds at h = 3 % (the only rung inside both
bands) it does not hold:

| panel | h | d | 435 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | mean win rate |
|---|---|---|---|---|---|---|---|---|---|---|---|
| U56 | 3 % | 1 | 1/4 | 1/4 | 0/4 | 0/4 | 0/4 | 1/4 | 0/4 | 0/4 | **0.094** |
| U56 | 3 % | 2 | 2/4 | 1/4 | 0/4 | 0/4 | 0/4 | 2/4 | 0/4 | 0/4 | 0.156 |
| U56 | 3 % | 3 | 2/4 | 2/4 | 0/4 | 0/4 | 0/4 | 2/4 | 0/4 | 0/4 | 0.188 |
| U56 | 8 % | 1–3 | | | | | | | | | 0.312 / 0.438 / 0.438 |
| U56 | 20 % | 1–3 | | | | | | | | | 0.719 / 0.500 / 0.344 |
| SMALL439 | 3 % | 1–3 | 0/12 | 0/12 | 0/12 | 0/12 | 0/12 | 0/12 | 0/12 | 0/12 | **0.000, 0/8 seeds** |

**5 of 8 seeds give 0/4 at h = 3 % on U56**, and SMALL439 is flat 0/96. The seed-435 flip is a
draw, not a mechanism. Seed is a replication axis here — nothing is selected on it, all seeds
report.

## Both KEEP paths (10 bps, every grid point)

**4a 0/2520. 4b 15/2520 — and every one of the 15 is the NO-FLOOR control** (`U56/NONE/MA200/rw`,
the already-committed no-screen candidate), never a floor arm. It degrades monotonically with the
haircut and dies between 12 % and 20 %: 11.55 %/1.091/−18.6 % at h=0 → 11.34 %/1.073 at 3 % →
10.97 %/1.042 at 8 % → 10.67 %/1.016 at 12 % → gone at 20 %. That is a free robustness reading of
the standing candidate: it tolerates a 12 pp/yr survivorship correction on the thinnest decile.
The 4b bars are constant across h by construction because SPY is never haircut.
**No book is proposed. No RULES change. PROTOCOL / RULES.md / scan.py / bot.py / baseline.py
untouched.**

## Caveats

* Both panels are CURRENT constituents; this run measures the sensitivity of a *published sign* to
  that fact, it does not repair the cache. A real delisted cohort would also change the eligible
  set and the ranking, which no synthetic haircut reproduces.
* The plausibility band (5 %/yr U56, 10 %/yr SMALL439 on the thinnest decile) is a **declared
  judgement**, not a measurement, and not derived from anything in the cache. Every h\* is
  published so the band can be re-drawn by anyone who disagrees; the verdict flips only if someone
  argues a US large-cap thinnest decile is overstated by **>16.7 %/yr**.
* Reading A holds masks, gates and floor levels at their observed-price values; re-solving them on
  haircut prices is not tested here.
