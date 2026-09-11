# Idea 698 — does-the-B136-SPY-SERIES-gap-ever-reach-a-published-verdict (cloud, 2026-09-11)

**ANSWERED / NO — AND THE TEST THAT SAYS "YES" IS THE WRONG TEST. 0 of 1,836 committed
BROAD-panel 4b passes are decidable by the two-cache SPY gap; the tightest sits at 20.22×
its own bar's shift. Fresh price leg: 0/24 verdict flips on either channel. KILL of the
premise — idea 517's caveat can be retired. No KEEP, no memo, no RULES change.**

## The bar shift (what the cache is actually worth)

Swapping `SPY` from `data/prices_broad.csv` for `SPY` from `data/prices.csv`, over the 4,699
common days, moves each 4b bar by:

| bar | prices_broad | prices.csv | shift |
|---|---|---|---|
| H1 Sharpe | 0.95663840 | 0.95661920 | 1.920e-05 |
| H2 Sharpe | 0.83403269 | 0.83401566 | 1.703e-05 |
| OOS Sharpe | 0.88202392 | 0.88201069 | 1.324e-05 |
| DD cap (0.60×) | 0.20229572 | 0.20230354 | 7.821e-06 |
| CAGR floor (0.70×) | 0.10659834 | 0.10659631 | 2.022e-06 |
| OOS CAGR floor (0.70×) | 0.10815311 | 0.10815507 | 1.958e-06 |
| OOS DD cap (0.60×) | 0.20229572 | 0.20230354 | 7.821e-06 |

The seven bars differ by **an order of magnitude among themselves** (1.958e-06 … 1.920e-05),
and that is the whole methodological point below.

## The census — and the test that gets it wrong

**6,885 committed 4b passes** were harvested from the 181 artefact CSVs (of 792 publishing a
4b column) that also publish a `SPY*` bar column, and each pass's every available 4b leg was
restated with a **margin** — its signed distance from its bar, i.e. exactly how far the bar
would have to move to flip it. Tightest-margin distribution: min **1.699e-06**, p1 1.36e-04,
median **0.0104**, max 0.5200. The binding leg is the CAGR floor (33.7% full-sample + 27.1%
OOS = **60.8%**), then the DD cap (33.4%), then the OOS Sharpe bar (5.9%).

* **Loose test** (margin vs the *largest* of the seven shifts, 1.920e-05 — the reading idea
  517's one-number framing invites): **9 of 6,885 passes look decidable**, 3 of them on BROAD.
* **Leg-matched test** (each margin against **its own bar's** shift — the correct test):
  **2 of 6,885**, and **0 of the 1,836 BROAD passes**. The tightest BROAD margin is
  **20.22×** its own leg's shift.

The 9 hits are an artefact of comparing an **OOS-CAGR-floor** margin (shift 1.958e-06) against
the **H1-Sharpe** bar's shift (1.920e-05) — a factor of ten. The two hits that survive
leg-matching are on non-BROAD panels, where the gap **does not exist at all**: U56 reads its
SPY from `data/prices.csv`, and `baseline.load_universe(small=True)` *joins that same
prices.csv SPY* onto the small panel, so on both panels the two readings are the identical
series and the shift is exactly zero. **The honest count of committed 4b verdicts this cache
could have decided is 0.**

## The fresh price leg — two channels, separated

On B136, `SPY` is not only the comparand: `load_universe(broad=True)` returns it as a
**column** the books rank and can hold. Three arms over one common calendar (G4: the panels
differ in **no** column but `SPY`, 0.000e+00; G5: identical index):
**A NATIVE** (broad bar, broad column) · **B BAR-SWAP** (prices.csv bar, broad column —
comparand channel alone) · **C BOTH**.

24 pre-registered books (CAND-n, n ∈ {5,10,15,20,30,40,50} × gross ∈ {0.50,0.75,1.00}, plus
the live band book at the same three grosses), weekly, 10 bps, t+1, all reported:

* **4b verdict flips A→B: 0/24. A→C: 0/24.** 4b passes 3/24 in all three arms; 4a **0/24** in
  all three.
* Smallest tightest-margin over the 24 books is **6.475e-04 = 34×** the largest bar shift.
* **BOOK channel** (SPY as a panel column): max |Sharpe(A) − Sharpe(C)| over 24 books =
  **7.651e-07** — smaller than the comparand channel and never near a bar.
* **Rule 8** (pick by IS Sharpe on IS rows only, 2017–2026 read once): all three arms pick
  **the same book** (BAND@g1.00, IS Sharpe 1.0922), OOS CAGR **10.66%**, OOS Sharpe **1.1174**,
  OOS MaxDD **−16.16%** against SPY OOS Sharpe 0.8820; 4b PASS, 4a FAIL, in every arm.
* Cost appendix (**labelled robustness, no verdict taken from it**): 0 bps → 6/24 pass, 0
  flips; 25 bps → 0/24 pass, 0 flips. The gap is invisible at every rung.

## Gates (all PASS, printed before any new number was read)

G1 fast_backtest == engine.backtest 1.041e-17 · G2 band_book == rules_v2_weights 0.000e+00 ·
**G3 idea 517 reproduction**: the two series differ on **97.7868%** of 4,699 common days, max
abs **$0.0051**, max rel **9.059e-05** (517 published 97.7% and 6.326e-05 on an earlier
prices.csv vintage; the gate pins direction and order of magnitude, not the digits) ·
G4 arms differ only in `SPY` 0.000e+00 · G5 one common calendar, 4,699 rows ·
G6 causality, `w(px[:d])` an exact prefix of `w(px)` 0.000e+00.

## Caveats

* The census reads only artefacts that publish **both** a 4b verdict column and a `SPY*` bar
  column: 181 of 792 files. Passes whose file published no SPY comparand cannot be given a
  margin and are not counted.
* Panel attribution is by a `panel`/`uni` column where one exists, else by filename token:
  BROAD 1,836 (26.7%) / OTHER 3,364 (48.9%) / UNKNOWN 1,685 (24.5%). The BROAD-restricted
  result is the one that carries the verdict; the UNKNOWN bucket is reported, not assumed
  away, and the tightest margin anywhere in it (5.659e-06, leg `mCAGR`) is **2.8×** its own
  leg's shift — still outside, so the conclusion does not turn on that bucket's labels.
* **SURVIVORSHIP (PROTOCOL 9):** B136 is today's constituents (research/universe_broad.json);
  names acquired, delisted or dropped from the index are absent, so every LEVEL here is biased
  upward and none is a tradeable estimate. The headline is a **difference between two readings
  of the same 24 books on the same days**, to which the bias applies identically on both sides.

## What should change

Nothing in the code. `data/prices_broad.csv` keeping its own SPY column is **not** a live
risk to any published 4b verdict, and future runs need not carry idea 517's caveat. The
transferable lesson is the other one: **a margin must be compared against its own bar's
shift.** The loose reading turns 0 decidable passes into 9.
