# Idea 51 — trend-filter-by-market-cap (cloud, 2026-09-06) — INDEPENDENT REPLICATION

**Note on provenance.** This run was claimed and executed concurrently with lane B's idea 51,
which reached `## Done` first. It is therefore filed as a **second, independent replication on a
different grid**, not as a fresh claim. It confirms lane B's KILL on every shared number and
adds one leg that lane B did not run.

**KILL, and the queue's framing is wrong twice over.** At matched gross the 200d/vol20 filter
subtracts Sharpe on *all three* universes (1 of 9 panel × cadence cells positive), so there is no
cap boundary to find — and the leg that destroys small caps is the **volatility screen**, not the
trend screen.

## Design

`FILT` = equal weight across admitted names at GROSS/k (matched gross, no ranking) vs `CTRL` =
equal weight across every live name at GROSS/n. `DEGROSS` (the live RULES form, gated weight →
cash) reported alongside. Gate decomposed into its legs: **MA** (px > rolling(lb).mean()),
**VOL** (vol20 < 0.60), **MAVOL** (both = RULES v1 eligibility = idea 49's f=1.00 book). Panels
U56 / B136 / SMALL439. Tuned: cadence {W,M,Q} × lookback {100,200,300}, reported at every value.
126 sweep books + 80 decile books, each at 10 and 0 bps, 75% gross, t+1.

**H1 replication gate, asserted first — HOLDS.** SMALL439 / MAVOL / lb 200 / weekly / RESPREAD on
idea 49's own window: CTRL 10.20% / 0.6792 / −36.16% (idea 49: 10.2% / 0.677 / −36.2%); gap
**−5.33 pp/yr at 0 bps** (idea 49: −5.4) and **−6.53 pp/yr at 10 bps** (idea 49: −6.6). Lane B
independently got −5.31.

## H2 — the filter loses at matched gross on every panel (FAILS the pre-registered flip)

dSharpe (FILT − matched CTRL), MAVOL, lb 200, RESPREAD:

| panel | W | M | Q | dCAGR @0 bps (W) |
|---|---|---|---|---|
| U56 | −0.0571 | **+0.0135** | −0.0708 | −1.45 pp/yr |
| B136 | −0.0831 | −0.0319 | −0.0830 | −1.97 pp/yr |
| SMALL439 | −0.3404 | −0.1896 | −0.2466 | −5.34 pp/yr |

**1 of 9 cells positive.** The panel ordering U56 > B136 > SMALL439 is monotone and matches lane
B's independently (mean MA/RESPREAD dSharpe −0.0154 / −0.0345 / −0.0735 here against lane B's
−0.004 / −0.047 / −0.102). So idea 49's "the filter is the whole edge on universe.json" is not a
*selection* claim: at matched gross the filter subtracts on the large-cap panels too — just less.

## H5 — which leg? FAILS, and reverses (the new finding)

dCAGR at 0 bps (pp/yr, RESPREAD, mean over cadences) and dSharpe (lb 200):

| panel | MA only | VOL only | MAVOL |
|---|---|---|---|
| SMALL439 | **−1.44** (dS −0.074) | **−3.93** (dS −0.204) | −4.56 (dS −0.259) |
| U56 | −0.28 (dS −0.015) | −0.85 (dS −0.016) | −1.08 (dS −0.038) |
| B136 | −0.82 (dS −0.035) | −0.71 (dS −0.008) | −1.59 (dS −0.066) |

On the sub-$2B panel the **vol20 < 0.60 cap costs 2.7× what the trend leg costs**; on the two
large-cap panels the legs are comparable. Lane B ran MA and MAVOL but never VOL alone, so this
splits their MAVOL result: the queue's question ("where does trend-following stop working") is
aimed at the cheaper of the two legs. A vol cap set at large-cap volatility simply deletes most
of a small-cap panel.

The lookback dial says the same thing: SMALL439 damage shrinks monotonically as the MA slows
(dSharpe −0.396 → −0.340 → −0.291 for lb 100/200/300 at weekly), consistent with idea 52's
whipsaw mechanism — a slower trend leg is a *less bad* trend leg, never a good one.

## H3 / H4 — no size boundary exists (both FAIL)

Within SMALL439 (MAVOL, RESPREAD, weekly, lb 200), two size columns:

| proxy | ρ(decile, dSharpe) | t | ρ(decile, dCAGR₀) | t | deciles with dSharpe > 0 |
|---|---|---|---|---|---|
| CAP (today's mktcap, **not** point-in-time) | −0.127 | −0.36 | −0.176 | −0.51 | **0 / 10** |
| ADV (60d median $ volume, point-in-time) | −0.042 | −0.12 | **+0.430** | +1.35 | **0 / 10** |

The damage is **flat** across the small-cap cross-section, not graded by size, and the two
proxies disagree in sign on the CAGR column — reproducing lane B's capQ −0.336 / advQ +0.335
split on an independent decile grid. **H4: no decile on either proxy clears dSharpe > 0 in both
halves and out of sample; nor does either large-cap panel** (U56 weekly −0.097 / −0.046 / −0.022;
B136 −0.073 / −0.123 / −0.084). There is no boundary to write into RULES.

## Rule 8 and the KEEP paths

(cadence, lookback) chosen on IS Sharpe inside each of 18 (panel × gate × construction) arms:
**1 / 18 picks beat the matched no-filter control OOS, 6 / 18 beat SPY, 0 / 18 beat the live
RULES v2 book.** Sweep 4a 0/126, 4b 17/126 — and **12 of those 17 4b passers still lose to their
own no-filter control**; the 5 that win do so by +0.009 to +0.021 of Sharpe and 3 of the 5 are
the **VOL-only** book, not a trend book. Deciles 4a 1/80, 4b 0/80.

**The one 4a pass, rejected.** ADV decile 2 / MA / DEGROSS: 9.54% / 1.2553 / −8.28% (halves
1.3463 / 1.2317, OOS 1.2122) clears 4a against the live book. It is not a candidate: its own
no-filter control returns **19.71%** CAGR, so the filter destroys 10.3 pp/yr there and the cell
fails 4b on CAGR; and it is the second-least-liquid decile of a survivorship-screened sub-$2B
panel — precisely where the missing delistings live and where 10 bps is fiction. Reported for
completeness, not proposed.

## Caveats

SURVIVORSHIP: all three panels are current constituents. The dSharpe/dCAGR headlines are
FILT-minus-CTRL contrasts on the same names and days, so the bias largely cancels there; it does
not cancel out of the 4a/4b levels, nor out of the CAP decile labels, which are **today's** caps
and therefore peek. A KILL of the filter is *strengthened* by the bias — the missing names are
exactly the ones a trend filter would have exited.

Script `2026-09-06_trend-filter-by-market-cap_cloud.py`; console, `sweep.csv` (126 cells),
`deciles.csv` (80 cells), `walkforward.csv` committed.
