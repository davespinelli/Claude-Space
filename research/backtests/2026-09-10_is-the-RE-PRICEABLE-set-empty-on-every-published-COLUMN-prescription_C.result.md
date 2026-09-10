# Idea 616 — is the RE-PRICEABLE set empty on every published COLUMN prescription?  (lane C, 2026-09-10)

**VERDICT: SPLIT — 613's census finding GENERALISES to 4 of the record's 5 other column
prescriptions and is REFUTED on the 5th; and the five columns are NOT interchangeable — on a
fresh grid that carries all of them, the UN-RANKED control (239) flips 98% of Sharpe verdicts
while the crossing cost (607) flips almost nothing because 87% of the cells are already losing
at 0 bps. No KEEP claimed, no book promoted, no memo. RULES.md / PROTOCOL.md / scan.py / bot.py /
baseline.py untouched.**

Script `2026-09-10_is-the-RE-PRICEABLE-set-empty-on-every-published-COLUMN-prescription_C.py`;
`.console.txt`, `.census.csv` (2 811 files x 5 prescriptions x 2 tiers), `.presc.csv` (30 census
cells), `.grid.csv` (2 160 arm-rows), `.reread.csv`, `.cstar.csv`, `.wf.csv` committed beside it.
Runs in 149 s, deterministic.

## Axes, and what is ever selected on (PROTOCOL 4)
The queue names the two tuned parameters and both are swept in full with every point reported:
**P1 prescription set** (239 EWall / 471 matched-gross / 583 gross / 604 placebo / 607 crossing
cost, with 613 WIDTH as the already-published control) and **P2 strictness** (LOOSE = header
keyword only, the census a naive regex would make; STRICT = keyword AND the column's values in
the right physical range AND the claim's own witness column present and numeric).
**VINTAGE (PRE / AT / NOW) is a reported axis, not a tuned one** — all three are always printed.
The fresh leg's dials are **band** (6 points, 0.00–0.08) and **gross** (3 points, 0.50/0.75/1.00),
fully enumerated, never chosen. The only selection anywhere is PROTOCOL rule 8.

## Gates — all pass, before any new number was read
* **G1** the vectorised runner vs `engine.backtest` on the evaluated slice: max|dr|
  **6.409e-16 / 6.297e-16 / 6.093e-16** and max|dturnover| **3.331e-16 / 3.331e-16 / 2.776e-16**
  on u56 / broad / small.
* **G2** the rung identity `r(c) = r(0) − turnover·c/1e4` vs a live `engine.backtest(25)`:
  **6.409e-16 / 6.297e-16 / 6.093e-16**.
* **G3 VINTAGE** — 4 550 stamped artefacts; git can still see the add commit of 4 549 of them and
  a filename stamp post-dates its own add commit in **0**. The repo history is shallow
  (2026-09-09 → 2026-09-10, 50 commits), so the **filename date stamp is the only vintage that
  reaches the whole record**, and it is what this run uses.
* **G4** the census machinery reproduces idea 613's OWN published census off 613's committed
  `.census.csv`: **44 TIER-A width files (published 44), 1 re-priceable (published 1).**

## H1 — THE CENSUS.  613 generalises to 4 of 5, and dies on the 5th
2 811 committed CSVs scanned (this run's own artefacts excluded), 2 809 stamped.
STRICT tier, **PRE** = files stamped strictly before the proposal date, i.e. what the prescribing
run could actually see:

| prescription | proposed | Y-claim files at proposal | + X | **re-priceable AT PROPOSAL** | now |
|---|---|---|---|---|---|
| **239** publish EWall beside every panel claim | 2026-09-06 | 252 | 1 | **0.4 %** | 2.7 % (35/1 285) |
| **471** matched gross on every d_on/d_off split | 2026-09-08 | 36 | 3 | **8.3 %** | 10.7 % (9/84) |
| **583** both arms' gross beside every CAGR/MaxDD comparison | 2026-09-09 | 916 | 61 | **6.7 %** | 6.5 % (74/1 145) |
| **604** a placebo column beside every twin claim | 2026-09-10 | 278 | 5 | **1.8 %** | 1.7 % (5/297) |
| **607** a crossing cost beside every twin claim | 2026-09-10 | 278 | 152 | **54.7 %** | 55.6 % (165/297) |
| *613 width (published control)* | 2026-09-10 | 44 | 1 | *2.3 %* | — |

**Four of the five prescriptions were made against a corpus that is 0.4–8.3 % re-priceable — the
same regime as 613's 2.3 %.** The exception is **607**, and its exception has a reason: the thing
607 asks for is a **cost ladder**, and the record already runs almost everything at 2+ rungs, so
55 % of twin claims can be priced for a crossing cost with no new run at all. 607 is therefore
not a back-fill request; it is a request to *read a column the record already publishes.*
LOOSE and STRICT agree to within 1.6 pp on every prescription and every vintage — the header/value
gap that cost 613's census a factor of 3.5 does not bite here, because these five columns are
named after quantities rather than after statistics about them.

## H2 — VINTAGE.  The record does not back-fill, with one exception that proves the rule
PRE → NOW moves: 471 +2.4 pp, 583 **−0.2 pp**, 604 −0.1 pp, 607 +0.9 pp — nothing.
**239 is the one that moves: 0.4 % → 2.7 %, a 6.75x rise, and all 34 of the new re-priceable files
are stamped on or after the proposal date.** That is idea 460 ("back-fill-the-EWall-column-on-the-319-files-that-lack-it") doing exactly what it said it would. The record *can* back-fill a
column when it schedules a run to do it — and even then the compliant share of panel claims
finishes at **2.7 %**, because the claim population grew from 252 files to 1 285 in the same
four days. **Prescriptions do not propagate; back-fill runs do, and they lose to the record's
own growth rate.**

## H3 — WHOSE files are the re-priceable ones?
| idea | re-priceable (STRICT, now) | stamped ON/AFTER its proposal | stamped BEFORE |
|---|---|---|---|
| 239 | 35 | **34** | 1 |
| 471 | 9 | 6 | 3 |
| 583 | 74 | 13 | **61** |
| 604 | 5 | **0** | 5 |
| 607 | 165 | 13 | **152** |

613's extreme case (the only re-priceable file was the prescribing run's own) is **not** the
general shape. Two distinct regimes: 239 and 471 are **prescription-driven** (the compliant files
appeared after the ask), 583 and 607 are **incidental** (the column was already there for other
reasons, and the prescription is largely a request to read it). **604 is the pathological case:
its five compliant files all pre-date it and it has produced none since** — the placebo column
has not spread at all in the days since the prescription was published.

## H4 — WHAT THE MISSING COLUMN COSTS, on a fresh grid that carries all five
432 simulations (3 panels x 2 books x 3 grosses x 6 bands x 4 forms: ARM = 200d band gate
de-grossing to cash, CTRL = the same book ungated at the same nominal gross, TWIN = the ungated
book scaled to the arm's **realised** mean gross, PLACEBO = the arm's gate block-shuffled in time,
block 21d, seed 616) read at 5 rungs = 2 160 arm-rows.

Of the cells the record would publish as a **win against the full-gross control**, how many
survive each prescribed re-reading:

| statistic | wins vs CTRL | survive TWIN (583/471) | survive PLACEBO (604) | survive EWALL (239) |
|---|---|---|---|---|
| CAGR | 10 | 10 (100 %) | 10 (100 %) | 10 (100 %) |
| **Sharpe** | 189 | 189 (100 %) | 189 (100 %) | **3 (2 %)** |
| **MaxDD** | 540 | 525 (97 %) | **311 (58 %)** | **0 (0 %)** |

**The five columns are not substitutes and they do not bind in the order the record proposes
them.** Sharpe is exposure-blind (idea 581, reproduced exactly: 189/189 survive the gross match),
so the gross column changes the *size* of a CAGR/MaxDD claim and never the sign of a Sharpe one:
median |dCAGR vs CTRL| **0.0247** against |dCAGR vs TWIN| **0.0057**, a factor of **4.31x**
(MaxDD 1.73x) — larger than idea 581's quoted ~2x, on a grid where the twin matches the arm's
realised gross to **1.1e-15**. The placebo bites only on MaxDD (42 % of the wins are timing-free)
and the un-ranked control annihilates almost everything, because on these panels the band gate's
Sharpe edge over its own full-gross self is real and its edge over holding *everything equally*
is not.

**607's crossing cost is near-vacuous on this menu, for the reason that makes it cheap:** 95 of
108 (panel, book, gross, band) cells cross inside [0, 50] bps on CAGR, but the **median crossing
cost is 0.0 bps and 94 of the 95 are already losing to their own matched-gross twin at zero
cost.** A crossing-cost column on a claim that never wins is a column of zeros. (Sharpe: 90/108
cross, 60 already losing at 0 bps.)

## KEEP paths (PROTOCOL 4, evaluated on every arm-row)
**4a** vs the live RULES v2, cost-matched: **94 / 2 160** (20 at 10 bps).
**4b** vs SPY on all five bars: **79 / 2 160** (34/17/16/10/2 at 0/5/10/25/50 bps).
**BOTH: 0 / 2 160, at every rung.**

**NO KEEP IS CLAIMED, and the reason is the record's own.** All 16 of the 10-bps 4b passers are
band-gated books at **gross 1.00** (u56 TOP20 g0.75 x 6 bands, u56 EWALL g1.00 x 6, broad EWALL
g1.00 x 4) — the already-published **gross-1.00 family (ideas 439 / 442, and idea 411 F filed
earlier today, which found 9 of 216 at 10 bps, every one of them RULES v2 at gross 1.00, and
declined to claim it)**. At the
**live** gross of 0.75 the same book fails 4b on the **CAGR floor** by **−0.0209 to −0.0243**
across the whole band ladder, against 411 F's independently measured **−0.0200** on the live
configuration: two different constructions, the same binding leg and the same margin to within
half a point. The best passer's binding margin is **+0.0078 at 10 bps and +0.0013 at 50 bps** —
thinner than idea 619's measured W-vs-M phase band of 0.0468, which is the record's own reason
not to promote a margin this size.

This is the loop closing on itself: **the one candidate this run produced is a GROSS story**, and
whether it may be promoted turns on exactly the column ideas 583/471 say the record does not
publish. It is also a direct partial answer to the open queue idea **585** — for the *band* gate
(not the breadth gate), **the 4b pass lives only at gross 1.00**, and the leg that fails at 0.75
is the CAGR floor, not the drawdown cap.

## Rule 8 (PROTOCOL 8) — (band, gross) chosen on 2009–2016 alone, 2017–2026 read exactly once
30 picks per selector (3 panels x 2 books x 5 rungs).

| selector | median band | median gross | OOS Sharpe | OOS CAGR | OOS MaxDD | beats SPY | beats RULES v2 | OOS 4b | OOS 4a |
|---|---|---|---|---|---|---|---|---|---|
| S0 IS-Sharpe | 0.08 | 1.00 | **0.9312** | 14.28 % | −25.51 % | 18/30 | 12/30 | 9/30 | **0/30** |
| S1 IS-4b screened | 0.08 | 1.00 | 0.9309 | 13.23 % | −24.24 % | 18/30 | 12/30 | **12/30** | **0/30** |
| S2 vs FULL-GROSS control (column-blind) | 0.08 | 0.50 | 0.9303 | 9.42 % | −17.08 % | 18/30 | 12/30 | 0/30 | **0/30** |
| S3 vs MATCHED-GROSS twin (prescribed) | 0.08 | 0.50 | 0.9302 | 9.29 % | −16.87 % | 18/30 | 12/30 | 0/30 | **0/30** |

At 10 bps, by panel (SPY OOS and RULES v2 OOS are the comparands):

| panel | SPY OOS CAGR / Sharpe / MaxDD | RULES v2 OOS | S1 IS-4b | S3 vs TWIN |
|---|---|---|---|---|
| u56 | 15.32 % / 0.876 / −33.7 % | 9.48 % / 1.279 / −12.1 % | 13.93 % / **1.170** / −19.6 % | 13.58 % / 1.172 / −18.0 % |
| broad | 15.45 % / 0.882 / −33.7 % | 7.98 % / 1.119 / −12.2 % | 12.80 % / 1.019 / −21.1 % | 7.61 % / 1.019 / −12.8 % |
| small | 15.45 % / 0.882 / −33.7 % | 3.85 % / 0.568 / −14.7 % | 13.71 % / 0.716 / −28.7 % | 8.63 % / 0.714 / −20.0 % |

**No selector clears 4a out of sample on any of its 120 picks.** And the question as a selector:
**S2 (the comparand the record publishes when the gross column is absent) and S3 (the comparand
471/583 prescribe) make the identical rule-8 pick in 29 of 30 cells, 96.7 %**, and their OOS
Sharpes differ by **0.0001**. So the prescribed column changes the *published size* of a claim by
4.31x and its *pick* almost never — which is the honest limit of what a gross column buys, and it
is the mirror image of 613's finding that a drag column changes rank everywhere and predicts
nothing at the record's own rungs.

## Predictions, scored
P1 **RIGHT** — the re-priceable share at proposal would be near zero on most prescriptions (0.4 %,
1.8 %, 6.7 %, 8.3 % on four of five).
P2 **WRONG** — I predicted all five; 607 is **54.7 %** re-priceable at proposal, because a cost
ladder is something the record already runs for other reasons.
P3 **RIGHT** — no material back-fill (≤ +2.4 pp on four of five).
P4 **WRONG in shape** — I predicted 613's "the only compliant file is the prescribing run's own"
would generalise; it holds for 604 (0 files since) and inverts for 583 and 607, where 82–92 % of
the compliant files pre-date the prescription.
P5 **RIGHT** — the columns are not interchangeable: on Sharpe verdicts the EWall control overturns
**98 %** and the gross column **0 %**.

## Caveats carried
* **SURVIVORSHIP (idea 54):** all three panels are current constituents; SMALL439 additionally
  drops the 44 `max_1d_move >= 1.0` tickers from `data/small_meta.csv` before anything runs
  (439 investable names, 2010→2026).
* The census reads **committed CSVs only**; a claim made in prose and never written to a CSV is
  invisible to it, which is why LOOSE is reported beside STRICT as an upper bound.
* **VINTAGE is the filename stamp**, the record's own convention. A file re-written later under
  the same name keeps its original stamp, so the PRE counts are, if anything, generous to the
  record. Git cannot arbitrate: the history is 50 commits deep and starts on 2026-09-09.
* 604's proposal date is taken as 2026-09-10 (its parent idea 602's own date tag); 239/471/583's
  are their queue date tags. A one-day error in either direction moves no headline: the PRE and
  AT columns are both reported and differ by at most 2.2 pp on any prescription.
* The placebo is a **block** shuffle (21d): it preserves the gate's on-share and cross-section
  and destroys only its timing, so it is a timing null, not an exposure null — the twin is the
  exposure null and both are reported.
* MaxDD is one number off one path (idea 321) and the 4b DD cap turns on exactly that number.
* Idea 126: t+1 execution, no lag band. Idea 38: u56/broad carry the calendar-day index.
