# Idea 923 — which committed SINGLE-RUNG BANDS are GENUINE KNIFE EDGES?

**Lane cloud, run 8, 2026-09-22.** Script:
`research/backtests/2026-09-22_single-rung-bands-true-widths_cloud.py`
(deterministic, offline, 6 of 6 gates PASS). Panels U56 (56) / B136 (136) / SMALL (665 names
after dropping 54 with `max_1d_move >= 1.0`), weekly, costs 0/10/25/50 bps, criteria
{4b FULL, 4b OOS, 4a FULL}, IS ..2016-12-31, OOS 2017-01-01.. .

## Verdict: ANSWERED — and "one rung" is mostly neither of the two facts 919 named.

**Idea 919 framed the choice as knife edge (0.0036) vs wide interval (0.2096). On the
re-buildable ladder the dominant answer is a THIRD thing: a single rung is usually a HALF-LINE
running into the no-leverage ceiling.**

### Scope of the denominator (stated, not assumed)
This run rebuilds the band × gross ladder family exhaustively — 2 dials × 3 panels × 4 cost
rungs × 3 criteria = **360 re-buildable families**, each re-solved on a fine grid (gross 0.20–1.00
step 0.01; band 0.000–0.200 step 0.0025). It is **not** a textual census of every committed
single-rung claim in the corpus; claims on families this sandbox cannot rebuild (live data,
share volume) are out of scope and are in no denominator here.

1. **W1 — THE DISTRIBUTION (the deliverable).** Of the 360 families, the record's own coarse
   grid would publish **59 as single-rung** (GROSS 49, BAND 10).
   - **GROSS dial, n = 49:** true width min **0.0000**, p25 0.0200, **median 0.0500**, p75 0.0800,
     max 0.1800. A reader infers **0.1500** from "one rung" — the coarse grid's widest local step.
   - **BAND dial, n = 10:** min 0.0000, p25 0.0088, **median 0.0225**, p75 0.0825, max 0.1200,
     against an inferred 0.0300.
   The spread is a factor of **∞ to 1** at the bottom (exact zero-width rungs exist) and
   **9× between p25 and max** on gross. 919's two anchor facts are both real and both common.

2. **W2 — GENUINE KNIFE EDGES are a minority.** Below 919's own knife bar: **10 of 49 (20%)**
   on gross, **2 of 10 (20%)** on band. Below the coarse grid's own local step —
   i.e. the claim "one rung" is at least not an over-statement of narrowness —
   **48 of 49 (98%)** on gross, **6 of 10 (60%)** on band.

3. **W3 — THE REAL ANSWER: 98% of gross single-rungs are BOUNDARY-CLIPPED.** **48 of 49**
   run into the **HIGH** edge of the legal dial (gross 1.00, no leverage) and **0** into the low
   edge. Such a band is not a knife edge and not an interval: it is **"everything above g\*"**,
   and its published width is an artefact of where the ladder is allowed to stop. The
   multi-rung contrast is the same shape but longer: **14 of 14 (100%)** clipped, median width
   **0.5150**. On this dial the record has never measured a two-sided band at all.

4. **W4 — On the BAND dial, "the width" is often not one number.** **7 of 10 (70%)** single-rung
   band-dial claims have a **discontiguous** fine pass set (11 of 22 multi-rung ones likewise),
   and **0 of 10** are clipped. Here the failure mode is the opposite of the gross dial: the
   region is genuinely interior but genuinely broken.

5. **Both tuned dials checked.** The classification is not an artefact of either.
   Claim set RECORD / ALT and resolution FINE / HALF give SINGLE n = 59 / 59 / 62 / 62, gross
   median width 0.0500 / 0.0400 / 0.0600 / 0.0600, clipped share 81% / 81% / 74% / 74%.

6. **W6 — RULE 8, OOS read once.** 26 of 120 (panel, cost, dial, fixed) families have a
   non-empty **IS** 4b band. The IS band's **midpoint lands inside the OOS band in only
   8 of 26 (31%)**, and **ρ(IS width, OOS width) = −0.1825** — an in-sample band's width carries
   no information about, and if anything points against, its own out-of-sample width. The
   IS-chosen point clears **4b OOS in 9 of 26** and **4a OOS in 0 of 26**. At 10 bps the widest
   case is U56 / band dial at gross 1.00: IS band [0.077, 0.130] → pick 0.104 → OOS
   **12.20% / 1.193 / −16.64%** (4b-OOS PASS, 4a-OOS FAIL) against **SPY OOS 15.29% / 0.875 /
   −33.72%** and the **live book OOS 9.46% / 1.277 / −12.05%**. Three of the four B136 gross-dial
   IS bands map to an **EMPTY** OOS band.

7. **W7 — BOTH KEEP PATHS, every fine grid point, 10 bps.** U56 4b FULL 112/810, 4b OOS 151,
   FULL&OOS 112, 4a FULL **0**; B136 77 / 52 / 52 / 5; SMALL **0 / 0 / 0** (4a FULL 233).
   **BOTH PATHS = 0 on all three panels.** Nothing here is a KEEP candidate.

## What the record should take from this
"Single rung" on the gross dial should be **retired as a width claim**. In 98% of re-buildable
cases it denotes `[g*, 1.00]` — a half-line whose right edge is the leverage constraint, not
the data — so the informative statistic is **g\*, the left edge**, not the width. On the band
dial the informative statistic is **the number of disjoint regions**, which is >1 in 70% of
single-rung cases. Publishing either one alongside the rung count would make 919's two anchor
facts distinguishable at a glance.

## Survivorship (PROTOCOL rule 9)
All three panels are current-constituent lists. SMALL screens names sub-$2B **and still listed
today**, so every sub-$2B company delisted, acquired or taken to zero between 2010 and 2026 is
absent; its CAGR is severely optimistic and its drawdown severely understated. SMALL enters
here only as a third tape for a within-tape geometric statistic (band widths), never as a
return. Note SMALL carries **0 of 810** 4b passes at every cost rung.
