# Idea 541 — is the 4b DD CAP the CADENCE DIAL in disguise?

**2026-09-11, cloud.  ANSWERED: idea 299's claim GENERALISES IN MAGNITUDE and FAILS IN MECHANISM.
Cadence moves MaxDD by a median 9–11 pp on a gated book — ~8x idea 299's one-book 1.13 pp — but by
only 0.7–0.9 pp on the signal-free control, so the dial is not an accounting artefact of the cap:
it is the GATE'S LATENCY.  The cap is measuring something real.  Operationally the claim still
bites: 5 of the 5 cells that clear 4b anywhere are CADENCE-DECIDED, and no cell clears it at all
four cadences.  KILL of the "in disguise" reading; PROTOCOL wording PROPOSED, not applied.**

Script: `2026-09-11_is-the-4b-DD-CAP-the-CADENCE-DIAL-in-disguise_cloud.py`
Artefacts: `.grid.csv` (288 cells) · `.cadence.csv` (72 cells) · `.walkforward.csv` · `.gates.csv` · `.console.txt`

## Setup
Two tuned parameters, published in full: **cadence** ∈ {D, W, M, Q} × **gross** g ∈ {0.50, 0.75,
0.90, 1.00}.  Reported axes: panel ∈ {U56 (55 tradables), B136 (135), SMALL439 (439)}, book ∈
{**BAND** = the live signal, every priced name at g/N_priced while inside its 200d ±3% hysteresis
band and 0.0 outside, gated-out weight to CASH; **ALLIN** = the signal-free control, the same
envelope with the gate always ON}, cost ∈ {10, 25, 50} bps.  t+1 execution, 260-day warm-up skip,
IS/OOS boundary 2016-12-31.

*Deviation from the QUEUE entry's suggested params (cadence, panel), stated plainly:* panel is a
reported axis over all three panels and **gross** takes the second tuned slot, because idea 733
(same lane, today) established gross is the only dial that moves 4b's binding bar — a cadence
sweep at one gross would have had nothing to flip.

*Idea 298's own QUANTILE-family book is quoted, not rebuilt:* idea 299 re-affirmed it as PARK with
0 of 27 books clearing 4b at weekly cadence, so its cadence sensitivity cannot be read off a 4b
pass it does not have.  The sweep instead runs the family that carries the record's committed 4b
passes (the de-grossing band book at high gross, per idea 733).

**SMALL439 survivorship caveat:** `data/prices_small.csv` is 483 sub-$2B names since 2010; the 44
tickers with `max_1d_move >= 1.0` in `data/small_meta.csv` were dropped first, leaving 439.  The
panel is **current constituents of the screen only** (`data/SMALL_PANEL_README.md`), so every
small-cap number below is biased upward and is reported, never promoted.

## Gates — all pass
| gate | result |
|---|---|
| G1 cost linearity, r(c) = r(0) − turnover·c/1e4 | **0.000e+00** on 6 probe cells (2 books × 3 panels) |
| G2 the live book restates idea 733's committed row (U56, BAND, W, g0.75, 10 bps) | CAGR **−3.7e-07**, Sharpe **−1.3e-07**, MaxDD **+3.2e-07**, OOS Sharpe **−4.9e-07** — bar 5e-6 |
| G3 ALLIN is really signal-free (realised gross flat at g) | max\|dev\| **8.9e-16 / 1.9e-15 / 7.3e-15** |
| G3b ALLIN turnover < BAND turnover at matched cadence/gross | **0 violations of 48** |

## 1. The magnitude generalises — and then some
`DD_SPREAD` = max MaxDD − min MaxDD over the four cadences, in pp, per (panel, book, gross, cost):

| | median | min | max |
|---|---|---|---|
| all 72 cells | **4.13 pp** | 0.59 | **14.00 pp** |
| U56 BAND | **9.25** | 5.68 | 11.25 |
| B136 BAND | **11.49** | 6.98 | 14.00 |
| SMALL439 BAND | **7.90** | 4.34 | 10.56 |
| U56 ALLIN | **0.70** | 0.63 | 0.79 |
| B136 ALLIN | **0.86** | 0.59 | 0.98 |
| SMALL439 ALLIN | **2.61** | 0.75 | 3.92 |

**47 of 72 cells (65.3%) reach or exceed idea 299's 1.13 pp**, so the one-book claim was if anything
an understatement — but every cell that does is a **BAND** cell.  Worked example, U56 BAND at 10 bps:

| gross | D | W | M | Q | spread |
|---|---|---|---|---|---|
| 0.50 | −7.56% | −8.01% | −9.65% | −13.44% | 5.88 pp |
| 0.75 (live) | −11.18% | **−11.90%** | −14.19% | −19.80% | 8.62 pp |
| 0.90 | −13.30% | −14.19% | −16.83% | −23.51% | 10.21 pp |
| 1.00 | −14.69% | **−15.70%** | −18.56% | **−25.94%** | **11.25 pp** |

The DD cap is −20.23% on this panel.  **The same book, same signal, same gross, crosses the cap
purely by changing the rebalance schedule.** Even the live g0.75 book sits only 0.43 pp inside the
cap at quarterly cadence.

## 2. But the mechanism is the gate's latency, not the cap's bookkeeping
Two facts kill the "in disguise" reading:

1. **The spread is ~10x larger on the gated book than on the identical ungated envelope**
   (9.25 / 11.49 / 7.90 pp vs 0.70 / 0.86 / 2.61 pp).  If the cap were merely sensitive to how
   drawdown is accounted across a rebalance schedule, ALLIN would move too.  It does not.
2. **The sign flips with the gate.** Quarterly gives the **shallowest** drawdown on **all 36 ALLIN
   cells** (less turnover, less cost, more drift) and daily gives it on **32 of 36 BAND cells**.
   Slow rebalancing helps a book with no signal and badly hurts one whose entire protective value
   is how fast it can de-gross.

So cadence is a first-order, economically real determinant of a gated book's drawdown: it is the
speed limit on the signal.  What the cap is "in disguise" is not a dial but a **gate-speed test**.

**The uncomfortable corollary, which is the finding worth carrying:** cadence and the signal itself
are the **same order of magnitude** on the drawdown leg.  MaxDD gap (BAND − ALLIN) at the live
weekly cadence, against the cadence spread on the signal book:

| panel | cadence spread (median) | signal effect @W | ratio |
|---|---|---|---|
| U56 | 9.25 pp | **+10.89 pp** | 1.2x |
| B136 | 11.49 pp | **+13.57 pp** | 1.2x |
| SMALL439 | 7.90 pp | **+21.68 pp** | 2.7x |

An unreported cadence choice is worth nearly as much drawdown as the entire gate on the two large-cap
panels.  Note also that the gate's own value decays with cadence — the BAND−ALLIN gap falls from
+14.41 pp (D) to +2.75 pp (Q) on B136 and +11.41 → +2.01 pp on U56.

## 3. The verdict census the idea asked for
- **4b passes: 9 of 288 cells.**
- (panel, book, gross, cost) cells with **any** 4b pass: **5 of 72**.  Cells passing at **all four
  cadences: 0**.
- **CADENCE-DECIDED (verdict not constant over D/W/M/Q): 5 of 5 — every single one.**
- **DD-CADENCE-DECIDED (the DD leg alone flips across cadence): 23 of 72 cells.**
- **SIGNAL-DECIDED: 9 of 144** (panel, cadence, gross, cost) cells flip between BAND and ALLIN —
  BAND passes where ALLIN fails in **9**, the reverse in **0**.  So every 4b pass in this grid needs
  the gate *and* a fast cadence; neither alone suffices.

| panel | book | gross | cost | 4b at D / W / M / Q | DD leg at D / W / M / Q | spread |
|---|---|---|---|---|---|---|
| B136 | BAND | 1.00 | 10 | ✗ / **✓** / ✗ / ✗ | ✓ / ✓ / ✗ / ✗ | 14.00 pp |
| U56 | BAND | 0.90 | 10 | ✗ / ✗ / **✓** / ✗ | ✓ / ✓ / ✓ / ✗ | 10.21 pp |
| U56 | BAND | 1.00 | 10 | **✓ / ✓ / ✓** / ✗ | ✓ / ✓ / ✓ / ✗ | 11.25 pp |
| U56 | BAND | 1.00 | 25 | **✓ / ✓ / ✓** / ✗ | ✓ / ✓ / ✓ / ✗ | 11.11 pp |
| U56 | BAND | 1.00 | 50 | ✗ / ✗ / **✓** / ✗ | ✓ / ✓ / ✓ / ✗ | 10.89 pp |

**Which bar actually binds.** Of the 279 failing cells, the DD cap fails in 154 and the CAGR floor in
173, but as the **sole** failing leg: **DD cap 75, CAGR floor 90, halves 0, OOS Sharpe 0**.  In
practice 4b is a two-bar test and the halves/OOS-Sharpe legs never bind alone on this family.

## 4. Rule-8 walk-forward ((cadence, gross) chosen on IS ≤ 2016 only; 2017–2026 untouched)
| panel · book | selector | pick | OOS Sharpe | OOS CAGR | OOS MaxDD | live RULES v2 OOS | SPY OOS | 4b |
|---|---|---|---|---|---|---|---|---|
| U56 BAND | S1 max IS Sharpe | **M, g1.00** | 1.2325 | **12.86%** | −18.56% | 1.2834 / 9.48% / −11.90% | 0.8721 / 15.24% | **PASS** |
| U56 BAND | S2 memo's bars | **M, g1.00** | 1.2325 | 12.86% | −18.56% | same | same | **PASS** |
| B136 BAND | S1 max IS Sharpe | **W, g1.00** | 1.1195 | 10.66% | −16.08% | 1.1206 / 7.98% / −12.18% | 0.8820 / 15.45% | **PASS** |
| B136 BAND | S2 memo's bars | M, g1.00 | 1.0993 | 11.18% | **−20.40%** | same | same | **FAIL** (DD by 0.17 pp) |
| U56 ALLIN | S1 / S2 | Q g1.00 / D g0.75 | 1.1689 / 1.1293 | 18.93% / 13.75% | −28.46% / −22.25% | — | — | FAIL / FAIL |
| B136 ALLIN | S1 / S2 | Q g1.00 / D g0.75 | 1.1254 / 1.0995 | 18.88% / 13.95% | −32.12% / −25.17% | — | — | FAIL / FAIL |
| SMALL439 BAND | S1 | M, g1.00 | **0.6209** | 5.75% | −21.87% | 0.5665 / 3.84% / −14.70% | 0.8820 / 15.45% | FAIL |
| SMALL439 BAND | S2 | — | — | — | — | — | — | **INFEASIBLE** |
| SMALL439 ALLIN | S1 | D, g0.90 | 0.6503 | 12.19% | −42.28% | — | — | FAIL |

An honest IS-only choice of **both** dials lands on a 4b passer on U56 under **both** selectors
(monthly, gross 1.00).  It does **not** on B136 under the memo's pre-stated rule — that selector
picks monthly and then misses the DD cap by 0.17 pp.  **SMALL439 fails everywhere** (best OOS Sharpe
0.6209 against SPY's 0.8820): the small-cap panel carries no 4b candidate at any cadence or gross,
consistent with the rest of the record.

## 5. Consequence for today's other result (idea 733's KEEP-candidate), stated against it
Idea 733 proposed the live band book at **gross 1.00**.  This grid prices its cadence exposure:

| cell @10 bps | D | W (proposed) | M | Q |
|---|---|---|---|---|
| **U56** MaxDD / 4b | −14.69% **✓** | **−15.70% ✓** | −18.56% **✓** | −25.94% ✗ |
| **B136** MaxDD / 4b | −14.69% ✗ (CAGR 10.51% vs floor 10.66%) | **−16.08% ✓** | −20.40% ✗ (DD) | −28.69% ✗ |

So the candidate is **cadence-robust on U56 (3 of 4 cadences) and weekly-only on B136 (1 of 4)** —
its single B136 pass is a knife edge between a daily cell that fails the CAGR floor on cost drag and
a monthly cell that fails the DD cap by 0.17 pp.  The idea-733 memo has been amended to carry this.

## Verdict
**ANSWERED / KILL of the "DD cap is the cadence dial in disguise" reading** (the dial moves ~10x
more on gated than ungated books and flips sign with the gate, so it is the gate's latency, not the
cap's bookkeeping) **+ CONFIRMED as an operational defect in how the record reports 4b** (5 of 5
passing cells are cadence-decided; 0 pass at all four cadences).  No new book, no KEEP.

**PROTOCOL wording PROPOSED (not applied — rule 6, Sunday review only):** add to rule 4b —
*"A 4b verdict must state the rebalance cadence it was computed at, and a candidate whose DD-cap leg
is not stable across at least the neighbouring cadences (W and M) is PARK, not KEEP."*
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are untouched by this run.

## Caveats
Current-constituent survivorship in all three panels (worst on SMALL439, whose numbers are reported
only).  The scored windows start 2009-01-13 (U56/B136) and 2011-01-13 (SMALL439), so **2008 is
excluded everywhere**.  Only 2020 and 2022 are real stress tests.  Cadence here is the engine's
period-end schedule (`rebalance_mask`), so "monthly" means one fixed calendar grid, not an average
over start dates — a phase sweep would be the natural next test and is **not** run here, which means
the per-cadence MaxDDs above each carry an unmeasured phase component.  Quarterly has only ~67
rebalances in the sample, so its drawdown is the least well estimated of the four.
