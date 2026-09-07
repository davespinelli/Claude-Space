# Idea 129 — is the sign test worth anything on the small panel?  KILL, with a repair

**Answer to the queue's question: NO.** On the 439-name small panel, an IS-admissible price
denominator stays positive out of sample **exactly as often as a rejected one — 100.0% vs
100.0%, a discrimination of +0.0 pp at all 12 (q, tau) grid points, Fisher p 1.000.** The
screen changes **0 of 6** walk-forward picks and its OOS Sharpe equals the unscreened
selector's to four decimals (0.5572 vs 0.5572). Idea 122's clause is cosmetic here too, so it
is cosmetic on every panel the record has, and PROTOCOL should say so.

**But the run also found why, and the why is a repair, not a shrug.** The clause is applied to
rows that have already been filtered by idea 94's absolute floor on the *full-sample*
denominator — and on this sample the full-sample denominator is the OOS denominator
(**corr +0.9996**; the full-sample MaxDD trough falls inside the OOS window for **50 of 51**
book-arm legs). The floor has therefore already removed the negative-OOS rows before the sign
test is consulted: of the 33 rows it excludes, **28 are OOS-negative**. Applied to the
unrestricted population instead, the identical IS-only screen discriminates **+35.8 pp
(0.880 vs 0.522), Fisher p 1.0e-04, significant at 12 of 12 grid points**.

Script `2026-09-07_is-the-sign-test-worth-anything-on-the-small-panel_cloud.py`, console
`.console.txt`, data `.signtest.csv` (96 rows) / `.bootstrap.csv` (5,760) / `.d3.csv` /
`.discrim.csv` / `.discrim_allrows.csv` / `.troughs.csv` / `.grid.csv` / `.walkforward.csv` /
`.selector.csv`.

## Setup

Idea 122's screen, unchanged in every respect, moved to the panel idea 119 said the sign moves
on. Books (V1u top-5 @15%, TOP20, EWall @75% gross), 16 treated arms, cost rungs {0, 5, 10, 25}
bps, the IS/OOS split, NDRAW = 40, the seed and the (q, tau) grid are idea 122's verbatim, so
this run cannot pick its own bar. Two tuned parameters, both of the test: q in {0.05, 0.10,
0.20}, tau in {0.80, 0.90, 0.95, 1.00}; headline (0.10, 0.90). Panel: `prices_small.csv.gz`
minus the 44 tickers with `max_1d_move >= 1.0`, leaving **439 names**, 2010-01-04 to 2026-09-04,
evaluated from 2011-01-13.

**Gates, asserted before any new number was read.** Premise gate: idea 122's committed
`.signtest.csv` re-read — 138 published rates, 90 admissible, **OOS denominator positive in
138/138** — asserted, not assumed. G1 cached targets vs idea 94's `targets()`: **0.000e+00**.
G2 `H.run` with every instrument off vs `engine.backtest` at 10 bps: **0.000e+00**. The
bootstrap was re-run end to end on a second, independently scheduled parallel pass and
reproduced **bit-for-bit (max|diff| 0.0 over 5,760 rows)**; draws come off one seeded rng in
idea 122's order, only their evaluation is parallel.

## The screen on this panel

| axis | published rows passing |
|---|---|
| D1 cost {0,5,10,25} bps | 61/63 (96.8%) |
| D2 window IS and OOS | 50/63 (79.4%) |
| D3 panel q=0.10 tau=0.90 | 48/63 (76.2%) |
| **ALL THREE (admissible)** | **39/63 (61.9%)** |

Comparable to u56/broad's 90/138 (65.2%) — the screen bites about as hard here. Across the 12
grid points the admissible share runs 47.6% to 71.4%.

## The one question (the queue's own wording)

| | n | P(dMaxDD_OOS > 0) |
|---|---|---|
| IS-admissible | 43 | **1.0000** |
| IS-rejected | 20 | **1.0000** |

Discrimination **+0.0 pp**, Fisher p **1.000** — and identically 0.0 pp at all 12 grid points,
with p < 0.05 at **none** of them. **P1 was REFUTED**: the queue's premise that "the small panel
is where the sign actually moves" does not hold for the rows that carry a published rate. Their
OOS denominator is positive **63 of 63**, the same 100% degeneracy idea 122 hit on u56/broad.
The sign does move on the panel as a whole — over all 96 rows it is positive 70.8% full,
**60.4% IS**, 70.8% OOS — just never in the published subset.

## Why (the mechanism, [4c])

* The full-sample MaxDD trough falls in the **OOS window for 50 of 51** book-arm legs at 10 bps
  (controls 3/3): V1u 2025-04-08, TOP20/EWall mostly 2020-03, one EWall leg 2011-10-03.
* Therefore **corr(dMaxDD_full, dMaxDD_OOS) = +0.9996**, against corr(full, IS) = +0.8730;
  sign(full) = sign(OOS) in 89/96 rows but sign(full) = sign(IS) in only 66/96.
* Idea 94's absolute floor selects on `dMaxDD_full > 0.10 pp` — i.e. on very nearly the OOS
  quantity itself. Of the **33 rows it excludes, 28 are OOS-negative**.

**The floor, not the sign test, is what removes the negative-OOS rows.** By the time the clause
is consulted there is nothing left for it to reject. That single fact explains the degeneracy on
both panel families with one mechanism, and it is a property of the 2017-2026 OOS window holding
the sample's deepest drawdowns — not of the small panel.

## The answerable version ([4b])

Run on all 96 rows instead of the 63 pre-filtered ones, the identical IS-only screen predicts
the OOS sign:

| | n | P(dMaxDD_OOS > 0) |
|---|---|---|
| IS-admissible | 50 | 0.880 |
| IS-rejected | 46 | 0.522 |

**+35.8 pp, Fisher p 1.0e-04**; mean +36.0 pp across the 12 grid points, **p < 0.05 at 12/12**.
The 96 rows contain each configuration twice (10 and 25 bps), so the honest de-duplicated
reading is the 48 rows of one rung: identical **+35.8 pp** with Fisher p **0.0103** at either
rung alone. By book at 10 bps the direction is consistent (V1u 8/8 vs 3/8, TOP20 5/5 vs 7/11,
EWall 9/12 vs 2/4).

**Proposed amendment to idea 122's REPORT-ONLY clause:** apply the sign test *instead of* the
absolute floor, not after it. As currently written the clause is evaluated on a set the floor
has already conditioned on the answer, which is exactly why two runs on two panel families have
now measured its power as zero.

## Rule 8 walk-forward and KEEP paths

The screen is computed on 2010-2016 only (D1 on IS returns at all four rungs, D3 on IS-window
draws); 2017-2026 untouched. S1 = idea 94's selector, S2 = S1 after the screen.

| book/cost | S1 pick | OOS Sharpe | control OOS | RULES v2 OOS | SPY OOS |
|---|---|---|---|---|---|
| EWall 10 | band3-dg | 0.568 | 0.637 | 0.568 | 0.882 |
| EWall 25 | ddctl-8/.5/recover | 0.684 | 0.621 | 0.507 | 0.882 |
| TOP20 10 | ddctl-8/.5/high | 0.669 | 0.807 | 0.568 | 0.882 |
| TOP20 25 | ddctl-8/.5/high | 0.654 | 0.694 | 0.507 | 0.882 |
| V1u 10 | g200-rw | 0.545 | 0.448 | 0.568 | 0.882 |
| V1u 25 | g200-rw | 0.224 | 0.117 | 0.507 | 0.882 |

**S1 mean OOS Sharpe 0.5572; S2 at the headline 0.5572 (0 of 6 picks changed, d +0.0000).**
Every cell loses to SPY's OOS 0.882. **P3 confirmed: 4a 0/96 against the live RULES v2 and
4b 0/96**, with H1, H2 and OOS binding in 96/96 (DD 81, CAGR 75) — the small panel has no
defensive book here either, consistent with the record. (For continuity only, 4a against the
superseded RULES v1 passes 42/96, because v1 draws a -36.12% drawdown on this panel; that is a
statement about v1, not a candidate.)

## Verdict

**KILL of the clause as written, with a stated repair.** The sign test has no out-of-sample
discriminating power where the record applies it — 0.0 pp on u56/broad (138/138) and 0.0 pp on
the small panel (63/63) — because idea 94's absolute floor already selects on a full-sample
denominator that is the OOS denominator at corr +0.9996. Applied to the unfiltered population
it discriminates at +35.8 pp (p 1.0e-04, 12/12 grid points). No KEEP, no rule change proposed:
the deliverable is a correction to a REPORT-ONLY clause.

**SURVIVORSHIP:** `prices_small.csv.gz` is a current-constituent screen of sub-$2B names (see
`data/SMALL_PANEL_README.md`), the most flattered panel in this record; every absolute level
above is optimistic. This run reports sign stability and within-cell differences, which are far
less exposed — but a survivorship-free small panel could move which rows pass. The panel starts
2010-01-04, so its IS window is effectively 2011-2016, six years, not eight.
