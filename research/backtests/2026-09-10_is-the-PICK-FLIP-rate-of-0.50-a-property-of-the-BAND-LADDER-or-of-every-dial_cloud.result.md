# Idea 668 — is the 0.50 PICK-FLIP rate a property of the BAND ladder, or of every dial?

**Run:** 2026-09-10, cloud. **Script:** `2026-09-10_is-the-PICK-FLIP-rate-of-0.50-a-property-of-the-BAND-LADDER-or-of-every-dial_cloud.py`
**Verdict: ANSWERED — the queue's COUNT is CONFIRMED on every dial and its MECHANISM is FALSIFIED. KILL for capital: 4a 0/150, 4b 32/150, BOTH 0/150, nothing promoted, no RULES/PROTOCOL edit.**

## Gates (pre-registered, printed before any new number was read)

| Gate | Result |
|---|---|
| G1 `fast_backtest` == `engine.backtest` @10 bps | **6.939e-18** PASS |
| G2 `band_book(0.03, 0.75)` == `baseline.rules_v2_weights` | **0.000e+00** PASS |
| G3 BAND dial at g=0.75 reproduces idea 664's committed grid row (pick, IS read, Sharpe, OOS, SPY OOS, live-book OOS) | **U56 3.725e-06, B136 8.045e-07** PASS |
| G4 every ladder contains its live constant (0.03 / 0.75 / W / 20) | PASS |
| G5 all three channels agree at their level-0 point on every (panel, dial) | PASS |

**G3 is itself a datum.** On *today's* U56 tape the same gate reads **4.170e-03**, not 3.7e-06. The
gate passes only against a tape truncated to **2026-09-09** — `data/prices.csv` gained one trading
day since idea 664 ran *the same calendar day*, worth **dSharpe 2.2e-03, dOOS 3.9e-03**. This is
664's own two-day channel (dSharpe 0.0035) measured again at one day, and it is the third
consecutive run to hit it. B136 is unaffected (Friday cache, last date 2026-09-04, identical at
every truncation). Bears directly on open idea 517.

## Design

Five dials, each a ladder of books differing in exactly one parameter; a chooser reads each rung's
**in-sample** Sharpe (2009–2016 only, PROTOCOL 8) and takes the argmax, ties to the smallest rung.

| Dial | Ladder | Book |
|---|---|---|
| BAND (664's) | 0.00 … 0.20, 8 rungs | RULES v2 band book, g=0.75, W |
| N | 3 … 50, 8 rungs | top-n composite-ranked EW, g=0.75, W |
| GROSS | 0.20 … 1.00, 8 rungs | RULES v2 band book, band=0.03, W |
| VOLCAP | 0.20 … OFF, 8 rungs | top-20 ranked with a vol20 eligibility cap |
| CADENCE | D, W, M, Q, 4 rungs | RULES v2 band book, band=0.03, g=0.75 |

Three misread channels, identical in form to 664's, each with a level-0 honest control: **ROUND**
(dp ∈ 10\*,3,2,1,0), **WINDOW** (IS\*, IS_H2, TRAIL5Y, TRAIL3Y, FULL=look-ahead, flagged and
excluded from every headline), **BOOK** (read rung *i* off rung clip(*i*+k), k ∈ 0\*,+1,+2,+3,−1).
664's BOOK channel used band-*value* offsets, which have no meaning on a ladder of cadences; the
rung-index form is the only one that ports to all five dials and reduces to 664's on an evenly
spaced ladder. Stated, not hidden. **Tuned: 2 (dial, channel level).** Cost 10 bps, cadence W,
gross 0.75, band 0.03, n=20, warm-up 260, IS/OOS 2016-12-31 / 2017-01-01 — all the record's own
live constants, none chosen by looking at an outcome. Panels U56 and B136. **SURVIVORSHIP
(PROTOCOL 9): B136 is today's constituents only; every B136 level below is biased up.**

## (1) THE COUNT — confirmed, on every dial

Restated in **idea 664's own denominator** (controls counted, look-ahead excluded) so the numbers
are the same statistic as its published 42/84 = 0.5000:

| Dial | 664-convention | controls-excluded |
|---|---|---|
| BAND | **18/28 = 0.6429** | 18/22 = 0.8182 |
| CADENCE | 17/28 = 0.6071 | 17/22 = 0.7727 |
| N | 15/28 = 0.5357 | 15/22 = 0.6818 |
| GROSS | 14/28 = 0.5000 | 14/22 = 0.6364 |
| VOLCAP | 14/28 = 0.5000 | 14/22 = 0.6364 |
| **POOLED** | **78/140 = 0.5571** | 78/110 = 0.7091 |

**No dial sits below 0.500.** The band ladder is not special; it is the *most* flip-prone of the
five, and the least flip-prone two sit exactly at 664's headline. By channel: **BOOK 0.900 >
WINDOW 0.733 > ROUND 0.500** (controls excluded).

## (2) THE MECHANISM — falsified

The queue reads the flip rate as a *flatness* result ("the argmax is nearly flat, i.e. the pick is
close to arbitrary"). Measured directly on each dial's own honest IS ladder, that reading does not
survive: over the 10 (panel, dial) cells the flip rate is **uncorrelated with, if anything mildly
opposed to, every flatness statistic** —

    rho(flip rate, margin)  Spearman -0.1515  Pearson -0.4740   n=10
    rho(flip rate, spread)  Spearman -0.1137  Pearson -0.2717   n=10
    rho(flip rate, curv)    Spearman -0.1010  Pearson -0.1637   n=10
    rho(flip rate, is_sd)   Spearman -0.1137  Pearson -0.2593   n=10

(margin = best − 2nd-best IS Sharpe; spread = max − min; curv = mean |2nd difference|; is_sd = sd
across rungs. Statistic and n named beside every rho, per idea 564.)

**What flatness predicts is not whether the pick moves — it is what the move COSTS:**

    rho(max |dOOS Sharpe|, curv)    Spearman +0.9636  Pearson +0.9290   n=10
    rho(max |dOOS Sharpe|, is_sd)   Spearman +0.8788  Pearson +0.8396   n=10
    rho(max |dOOS Sharpe|, spread)  Spearman +0.8303  Pearson +0.8229   n=10
    rho(mean|dOOS Sharpe|, curv)    Spearman +0.7333  Pearson +0.6339   n=10

The cleanest pair in the run: **GROSS flips 14/22 and its worst flip costs 0.0018 (U56) / 0.0030
(B136) OOS Sharpe — 100% of its flips land under 0.01**, because Sharpe is flat in gross to three
decimals (idea 311/657 again). **CADENCE flips 17/22 and 100% of U56's flips cost more than
0.05**, worst −0.2476 Sharpe and −9.60 pp OOS MaxDD. Same flip rate band, three orders of
magnitude apart in price. The single worst flip in the run is on **N**: reading the IS Sharpe to
**0 decimals** moves U56's pick from n=50 to n=3 and costs **−0.4617 OOS Sharpe** (1.1041 → 0.6424).

So 664's free-rounding finding replicates — **ROUND's median cost is +0.0000 on all five dials** —
but "free on the median" is not "free": the same channel carries the run's largest single loss.

## (3) RULE 8 AND THE KEEP PATHS

Every point chooses on 2009–2016 and is scored on 2017–2026 untouched; look-ahead (FULL) excluded.

| panel | dial | OOS Sharpe (mean / best / worst) | OOS CAGR | OOS MaxDD | SPY | live v2 | beat SPY |
|---|---|---|---|---|---|---|---|
| U56 | BAND | 1.1866 / 1.2769 / 1.1227 | 9.01% | −12.94% | 0.8721 | 1.2747 | 14/14 |
| U56 | CADENCE | 1.1733 / 1.2847 / 0.9750 | 9.15% | −14.89% | 0.8721 | 1.2747 | 14/14 |
| U56 | GROSS | 1.2744 / 1.2757 / 1.2740 | 10.02% | −12.66% | 0.8721 | 1.2747 | 14/14 |
| U56 | N | 1.0666 / 1.1126 / 0.6424 | 12.05% | −18.48% | 0.8721 | 1.2747 | 13/14 |
| U56 | VOLCAP | 0.9529 / 1.0221 / 0.6611 | 10.22% | −17.23% | 0.8721 | 1.2747 | 13/14 |
| B136 | BAND | 1.1025 / 1.1388 / 1.0120 | 8.22% | −14.09% | 0.8820 | 1.1185 | 14/14 |
| B136 | CADENCE | 1.0941 / 1.1452 / 0.8920 | 7.96% | −13.49% | 0.8820 | 1.1185 | 14/14 |
| B136 | GROSS | 1.1183 / 1.1204 / 1.1174 | 8.37% | −12.74% | 0.8820 | 1.1185 | 14/14 |
| B136 | N | 0.7854 / 0.8966 / 0.4667 | 8.66% | −20.16% | 0.8820 | 1.1185 | 4/14 |
| B136 | VOLCAP | 0.6779 / 0.7471 / 0.6284 | 6.14% | −16.96% | 0.8820 | 1.1185 | 0/14 |

**114/140 honest points beat SPY's OOS Sharpe; 19/140 beat the live book** (all of them U56 GROSS
or the two best BAND/CADENCE picks, by ≤0.010).

**KEEP paths: 4a 0/150, 4b 32/150, BOTH 0/150.** The 4b footprint is 16 GROSS points (**every one
at g ≥ 0.95, none at g = 0.75, none at g ≤ 0.60**), 14 U56 N points and 2 VOLCAP points (both at
cap OFF). That is idea 311's gross loophole and open idea 657's question for the **fifth**
consecutive run: the whole GROSS 4b footprint is the CAGR floor moving with exposure while Sharpe
is flat to three decimals across the ladder. And **every 4b-passing dial is PICK-dependent** — no
dial passes 4b at all of its own picks (GROSS 7/15 and 9/15, U56 N 14/15, VOLCAP 2/15) — so on
every one of them the KEEP verdict inherits the arbitrariness of the argmax it was read off.
**Nothing is promoted. No memo, no RULES change, no PROTOCOL edit.**

## (4) WHAT THE RECORD SHOULD DO WITH THIS

The pick-flip rate is not a diagnostic: it is ~0.5–0.8 everywhere, on flat dials and steep ones
alike, so a run that reports one has reported a constant. The quantity that carries the
information is the dial's **OOS spread**, which is knowable before the pick is made and predicts
the worst-case cost of misreading it at Spearman +0.83. Proposed (not applied — PROTOCOL edits are
a Sunday-review matter): **rule 8 should publish the chosen dial's rung-to-rung OOS spread beside
the pick**, so a reader can tell a decision from a coin flip. Filed as a follow-up idea rather
than written into PROTOCOL.md by this run.

## Follow-ups filed

669 (does the OOS-spread screen retire the flip-rate statistic on the record's committed rule-8
picks), 670 (is the GROSS dial's 4b footprint the CAGR floor alone at a matched gross — 657's
question posed as a single test), 671 (does the ROUND channel's fat left tail sit only on ladders
whose rungs differ in book width).
