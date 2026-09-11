# Idea 517 (lane B, 2026-09-11) — do-the-THREE-LIVE-PANELS-EVER-AGREE-on-a-vintage

**ANSWERED / NO — and the queue's own proposed remedy is INSUFFICIENT (partial KILL).
No KEEP: 4a 0/36, 4b 0/36. No RULES change; RULES.md, PROTOCOL.md, scan.py, bot.py,
baseline.py untouched.**

Script: `2026-09-11_do-the-THREE-LIVE-PANELS-EVER-AGREE-on-a-vintage_B.py`
Two tuned parameters, exactly the ones the queue names: **PARAM 1 truncation rule**
(NATIVE / LASTDATE / COMMONSTART / COMMONWIN) x **PARAM 2 panel set** (UB / US / BS / ALL).
All 16 cells reported; the rule-8 band ladder is *selected* by PROTOCOL 8 on IS only,
not tuned here. 10 bps, weekly, next-day execution. Deterministic, no RNG, no network.

## GATES (five, pre-registered, all PASS — read before any result)

| gate | value |
|---|---|
| G1 `fast_bt` vs `engine.backtest`, 3 panels x 2 books | returns **2.429e-17** / turnover **0.000e+00** |
| G2 live RULES v2 U56 @10bps (idea 523 G3b: 8.61%/1.1998/−12.05%) | **8.61% / 1.1998 / −12.05%** |
| G3 cost-rung identity `net(25) = net(0) − turn*25/1e4` | **0.000e+00** |
| G4 STRUCTURAL: SMALL ⊂ B136 ⊂ U56, zero interior holes | nested=True, **0** interior mismatches |
| G5 `INTERSECT(indices)` == `COMMONWIN` window, all 4 panel sets | max symmetric difference **0 days** |

G4/G5 matter to the reading: because the three live panels are **perfectly nested with no
interior holes**, the queue's "intersect the three indices" is *exactly* a window truncation,
and the vintage problem decomposes cleanly into an END channel and a START channel.

## PART A — the census, and the geometry the queue did not measure

**87.6% of the record is multi-panel.** Of 663 committed backtest scripts (this run excluded),
596 load prices: one-panel **74**, two-panel **197**, three-panel **325** → **522 of 596 (87.6%)**
compare books built on panels of different vintages.

| panel | rows | start | end | cols |
|---|---|---|---|---|
| U56 | 4702 | 2008-01-02 | **2026-09-10** | 56 |
| B136 | 4699 | 2008-01-02 | 2026-09-04 | 136 |
| SMALL | 4194 | **2010-01-04** | 2026-09-04 | 484 |

- **END gap** (U56's tail beyond the weekly caches): **3 trading days = 0.064%** of U56.
  The queue says "up to 5 trading days"; measured today it is 3.
- **START gap** (U56/B136 head before SMALL): **505 trading days = 10.740%** of U56 —
  **168x larger**, permanent (it is a panel property, not a refresh-schedule artefact),
  and **a common-last-date truncation does not touch it**.

**A2 — a THIRD channel, in the BAR and not in the book.** 4b scores every book against SPY,
and the panels do not share one: `SPY` in `data/prices_broad.csv` (B136) differs from `SPY` in
`data/prices.csv` (U56, SMALL) on **4,097 of 4,194 common days (97.7%)**, max |d| 0.0051,
max relative **6.326e-05**. U56 and SMALL are bit-identical (0.0). Neither truncation removes
this — it is present on days both panels quote. **Priced honestly: it is real but immaterial**,
moving Sharpe by < 1e-4, below the record's own publishing resolution.

## PART B — cross-panel ORDERING flips (the queue's question), 360 claims

Unit = one published cross-panel ordering (panel set x statistic x book). **18 of 360 = 5.00%** flip.

| rule | flips | rate |
|---|---|---|
| LASTDATE (the queue's proposed fix) | 4 / 120 | **3.33%** |
| COMMONSTART | 7 / 120 | 5.83% |
| COMMONWIN (= INTERSECT, G5) | 7 / 120 | 5.83% |

**Where the risk lives — the half-split statistics carry 14 of 18 flips (77.8%); MaxDD carries 0.**

| stat | CAGR | H1 | H2 | MaxDD | Sharpe |
|---|---|---|---|---|---|
| flips / 72 | 2 | **9** | 5 | **0** | 2 |
| rate | 2.78% | **12.50%** | 6.94% | **0.00%** | 2.78% |

Mechanism: `baseline._row` splits at `len(r)//2`, an **index-length** function, so any truncation
moves the half boundary — by up to **365 calendar days** (PART C). "Sharpe > X in BOTH halves"
is the leg PROTOCOL 4a and 4b are built on.

**The sharpest form — 13 of the 18 flipped orderings are `SPYBH`, the zero-signal control.**
SPYBH is the *same instrument* on all three panels, so every ordering it produces has **zero panel
content and is 100% vintage artefact**. The other 5 are the live book `BAND03`, and **all five are H1**.

**The publishable noise floor.** Cross-panel spread of SPY-buy-and-hold's own Sharpe — one asset,
three panels, so the true value is 0:

| rule | U56 | B136 | SMALL | spread (Sharpe) | spread (CAGR) |
|---|---|---|---|---|---|
| NATIVE | 0.8835 | 0.8890 | 0.8615 | **0.0275** | 0.0110 |
| **LASTDATE** | 0.8890 | 0.8890 | 0.8615 | **0.0275** | 0.0110 |
| COMMONSTART | 0.8550 | 0.8616 | 0.8615 | 0.0065 | 0.0013 |
| **COMMONWIN** | 0.8615 | 0.8616 | 0.8615 | **0.0000** | 0.0000 |

**This is the run's headline: the queue's fix removes 0.0000 of the 0.0275.** A common-last-date
truncation moves U56's own number (+0.0055) but leaves the cross-panel spread *exactly* where it
was, because the spread is set by the START gap. Only the full window intersection clears it.
And the fix is not free: LASTDATE flips 4 of 120 published orderings on its own.

## PART C — what each channel costs a single panel's published numbers (live book BAND03 = RULES v2)

| panel | channel | days dropped | dCAGR | dSharpe | dMaxDD | dH1 | dH2 | half boundary | shift |
|---|---|---|---|---|---|---|---|---|---|
| U56 | END-only | 3 | +0.0005 | **+0.0058** | 0.0000 | −0.0089 | +0.0190 | 2017-11-03 | 4 d |
| U56 | START-only | 505 | −0.0049 | **−0.0393** | −0.0002 | **−0.1793** | +0.0848 | 2018-11-07 | **365 d** |
| U56 | BOTH | 508 | −0.0043 | −0.0326 | −0.0002 | **−0.1808** | +0.0986 | 2018-11-06 | 364 d |
| B136 | START-only | 505 | −0.0042 | −0.0244 | −0.0001 | −0.1035 | +0.0548 | 2018-11-06 | 368 d |
| SMALL | any | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 2018-11-06 | 0 |

The START channel is **6.8x** the END channel on Sharpe and **20x** on H1. SMALL is the floor:
it is already the intersection, so it never moves — which is why the record's SMALL numbers are
the only cross-panel-safe ones it publishes.

## PART D — PROTOCOL 8 walk-forward, band chosen on 2008–2016 only, 2017–2026 read once

**The book footprint of the whole vintage question is ZERO.**

- **The rule-8 pick never moves: 0 of 9** (panel set x panel) under any truncation rule.
  U56 and B136 pick band = 0.08; SMALL picks 0.12, at every rule.
- **4a 0 of 36. 4b 0 of 36.** No KEEP-candidate, no memo, no book promoted.

| panel | rule | OOS CAGR | OOS Sharpe | OOS MaxDD | RULES v2 OOS | SPY OOS |
|---|---|---|---|---|---|---|
| U56 | NATIVE | 8.97% | 1.1627 | −14.47% | 1.2747 | 0.8721 / 15.24% / −33.72% |
| U56 | LASTDATE | 9.06% | 1.1726 | −14.47% | 1.2851 | 0.8820 / 15.45% / −33.72% |
| B136 | any | 8.36% | 1.1095 | −14.81% | 1.1185 | 0.8820 / 15.45% / −33.72% |
| SMALL | any | 4.92% | 0.6888 | −15.59% | 0.6629 | 0.8820 / 15.45% / −33.72% |

No pick beats RULES v2 OOS on U56 or B136; SMALL's pick beats RULES v2 (0.6888 vs 0.6629) and
loses to SPY. Nothing here is tradeable.

**AND THE BAR ITSELF MOVES WITH THE VINTAGE.** SPY's *own* OOS Sharpe reads **0.8721 on U56 and
0.8820 on B136/SMALL** under NATIVE — a spread of **0.0099** in a quantity that is by definition
one number. It carries into PROTOCOL 4b's constants: the CAGR floor is **0.1067 on U56 vs 0.1082**
elsewhere (0.15 pp) purely from vintage. LASTDATE *does* fix this one (spread → 0.0000), because
in the 2017+ OOS window the START gap is irrelevant and only the END gap is left.

## What this run concludes

1. **The three live panels never agree on a vintage.** Today the end gap is 3 trading days; the
   start gap is 505 and is permanent. There is no day on which a naive three-panel comparison is
   clean.
2. **The queue's proposed remedy is the wrong one.** A common-last-date truncation removes
   **0.0000** of the 0.0275 zero-signal cross-panel Sharpe spread, and costs 4 of 120 orderings
   to apply. The window **intersection** (== COMMONWIN, G5) is what clears it.
3. **But the exposure is small and the book footprint is zero.** 5.00% of orderings flip;
   the rule-8 pick moves 0 of 9; 4a and 4b are 0 of 36. This is a *reporting-hygiene* defect,
   not a capital defect.
4. **Publish the noise floor.** Any cross-panel ordering claim whose margin is inside
   **0.0275 of Sharpe / 0.0110 of CAGR** (NATIVE) is inside the pure-calendar noise floor,
   measured on a single asset held three ways.

**PROPOSED for Sunday review (proposed only; no PROTOCOL edit taken here).** Amend PROTOCOL 9
with one line: *a cross-panel claim must be computed on the intersection of the panels' indices,
and must state the common window (start, end) beside it; a common-last-date truncation is not
sufficient.* A cheaper partial alternative, if the full intersection is judged too costly: split
at a **fixed calendar date** rather than `len(r)//2`, which removes the mechanism behind 14 of the
18 flips without discarding 505 days of U56/B136 history.

## Caveats, stated

- **SURVIVORSHIP** (PROTOCOL 9 / idea 54): all three panels are current constituents; no level
  here is tradeable, and PART D is reported for the rule-8 obligation, not as a candidate.
- The 4a zero is **low power** — 0 of 36 books pass 4a unperturbed, so "no 4a flip" only says
  no fail→pass occurred. The 4b zero is equally low-powered on this book family.
- The ordering census is 6 pre-registered books x 5 statistics x 4 panel sets, not the record's
  actual published claims; it measures the *mechanism's* flip rate, not the record's realised one.
  Re-reading the record's committed cross-panel claims against the 0.0275 floor is filed as 696.
- The A2 SPY-series channel is measured but not swept; at < 1e-4 of Sharpe it is below the
  resolution at which the record publishes, and is reported as a finding, not a correction.
