# Idea 135 — is a `4b-defensive` class member just its own ladder point?

**2026-09-07, cloud.  Verdict: SPLIT — the queue's suspicion is CONFIRMED on the corpus and
its proposed rule is INERT in selection.  Only 16 of 139 class members (11.5%) beat their
own book's static-gross ladder point at matched mean gross; the ladder point is itself in
the class in 105 of 139 (75.5%) and clears FULL 4b — beating the member outright on the
record's own KEEP path — in 30 of 139 (21.6%).  The mean class member has a LOWER Sharpe
(−0.0531) and a LOWER CAGR (−1.28 pp) than a dumb static cut at the same average exposure,
buying 2.56 pp of drawdown it did not need an overlay to buy.  But the proposed rule
changes 0 of 4 rule-8 picks.  Rules unchanged; no new KEEP (4a 294/748, 4b 59/748, nothing
the record did not already hold).**

Script `2026-09-07_is-a-class-member-just-its-own-ladder-point_cloud.py`; artefacts
`.grid.csv` (748 arm-rows), `.ladders.csv` (153 solves), `.test.csv` (139 members),
`.walkforward.csv` (18 rows), `.console.txt`.

## Design

**The class** (idea 129's, verbatim, via idea 133's own committed code): a `4b-defensive`
arm clears 4b's halves bars, its OOS-Sharpe bar and its drawdown cap, and fails **only**
the CAGR floor — `fails(margins) == ["CAGR"]`.

**The comparand** is what the queue asked for: *the arm's own book's static-gross ladder
point at matched mean gross.*  Two conventions, both priced, neither assumed:

| | what | Sharpe invariance (G4, **measured**) |
|---|---|---|
| **LADDER** | the record's own: the book's `control` arm **re-run** at the multiplier m matching the member's realised mean gross (idea 133's `run_at_gross`, two Newton steps) | **1.088e-03** — the engine's cash leg drifts, so only NEARLY invariant |
| **SCALAR** | the closed form r = a·r₀, turn = a·turn₀ | **6.661e-16** — exactly invariant |

That distinction is why the question has content.  A static cut can only buy drawdown by
surrendering CAGR along a **fixed** Sharpe; a de-grossing overlay also moves Sharpe.  So
"does the overlay earn its name" is exactly "does it beat its own ladder point".  The two
conventions agree to three decimals on every headline below, so G4's 1.1e-03 gap changes
no verdict — which is the point of measuring it rather than assuming it.

**Corpus**: idea 133's, restricted to **native gross** — each arm at its own exposure,
which is idea 129's reading and the one the class was defined on.  Idea 133's m53/m75
rescalings answer a different question and would have confounded the comparand with the
treatment.  3 panels × 8 books × 17 arms × 2 cost rungs = **748 rows** (the small panel
carries no TLT/GLD/DBC/UUP, so its 2 sleeve books are skipped — exactly idea 133's own
748-not-816).

**Tuned parameters (max 2, PROTOCOL rule 4)**: ranked book size n ∈ {5,10,20,40} and sleeve
fraction f ∈ {0.25,0.50} — idea 133's own two.  Panel, arm, cost rung and window are census
axes: every level reported, nothing selected on outcome.

## Gates (printed in [0] before any new number)

| gate | what | result |
|---|---|---|
| G1 | this run's native-gross corpus reproduces idea 133's committed `.grid.csv` | **748/748 rows, 13 numeric columns, max abs diff 3.553e-15; `floor_only` mismatches 0; `pass4b` mismatches 0** |
| G2 | the ladder point at m = 1 **is** the book's control arm | `0.000e+00` |
| G3 | matched-gross solve over 153 members | max abs(achieved − member) `2.500e-10` |
| G4 | Sharpe invariance of the static gross dial, measured | LADDER `1.088e-03`, SCALAR `6.661e-16` |
| G5 | the standing 2026-09-04 KEEP-4b row (`46 N n=20`; published 12.7% / 1.09 / -18.3%, halves 1.09/1.10) at fixed n=20 | **12.66% / 1.092 / -18.31% (1.09/1.10) — EXACT** |

G1 is load-bearing: the 139 members priced here **are** idea 133's members, not
look-alikes, so the verdict attaches to the record's own class.

## [A] The class at native gross

748 arm-rows | 4a **294/748** | 4b **59/748** | class **139/748**.

| panel | EWall | SLV25 | SLV50 | TOP20 | TOP40 |
|---|---|---|---|---|---|
| u56 | 14 | 28 | 25 | 1 | 10 |
| broad | 12 | 22 | 27 | 0 | 0 |
| small | **0 — the class is empty on the sub-$2B panel at both cost rungs** | | | | |

## [B] The test

| comparand | beats on Sharpe **AND** drawdown | beats on Sharpe alone | mean dSharpe | mean dMaxDD (pp, + = member shallower) | mean dCAGR (pp) |
|---|---|---|---|---|---|
| LADDER | **16/139 (11.5%)** | 25/139 (18.0%) | **−0.0531** | **+2.56** | **−1.28** |
| SCALAR | **16/139 (11.5%)** | 25/139 (18.0%) | −0.0532 | +2.55 | −1.29 |

Read the three columns together.  The average class member **is** 2.56 pp shallower than
its ladder point — but it gets there with 0.053 **less** Sharpe and 1.28 pp **less** CAGR.
A static cut deep enough to match its drawdown would have kept more of both.  The overlay
is not buying insurance the gross dial cannot sell; it is buying the same insurance at a
worse price.

**The ladder point is itself a class member in 105 of 139 cases (75.5%), and clears FULL
4b in 30 of 139 (21.6%).**  Idea 133 inferred "de-grossing manufactures membership" by
moving a dial across the corpus; here it is measured directly, one member at a time, and it
is the majority case.

### The instrument that survives is a drawdown instrument, and it is a minority everywhere

| arm kind | n | beats | beats on Sharpe alone | mean dSharpe | mean dMaxDD | mean dCAGR |
|---|---|---|---|---|---|---|
| gate (5 trend gates × 2 conventions) | 89 | **15** | 15 | −0.0569 | **+0.0359** | −0.0160 |
| dd (book drawdown control) | 23 | **1** | 1 | −0.0889 | +0.0200 | −0.0136 |
| bud (entry turnover budget) | 10 | **0** | **9** | **+0.0146** | −0.0005 | +0.0012 |
| stop (per-name trailing stop) | 12 | **0** | 0 | −0.0347 | −0.0082 | −0.0053 |
| ctl (no overlay — the identity check) | 5 | **0** | 0 | 0.0000 | 0.0000 | 0.0000 |

`ctl` at 0.0000 across the board is the identity check: an arm with no overlay **is** its
own ladder point, and the machinery says so exactly.

**The two kinds split on which bar they move, and neither moves both.**  The 9 `ebud` arms
beat their ladder point on **Sharpe** (+0.0146 mean) but are drawdown-neutral (−0.0005, five
basis points the wrong way), so they fail the AND test — the entry budget is a turnover
instrument, not an exposure one, which is why a gross-matched control nearly reproduces it.
The 15 surviving `gate` arms are the mirror image: they win the AND test on **drawdown**
(+3.6 pp mean over the whole gate family) while the family's mean Sharpe is 0.057 *below*
its ladder points.  Fifteen of 89 gates clear the bar; 74 do not.

The largest single margin is `u56 / EWall / band3-dg @10 bps`: Sharpe 1.2056 vs the
ladder's 1.1234 (**+0.0822**) at MaxDD −12.05% vs −16.40% (**+4.34 pp shallower**), OOS
Sharpe 1.2851 vs 1.1359.  That arm is doing real work.  It is 1 of 139.

### by book, by panel × cost

| book | n | beats | mean dSharpe | mean dMaxDD | ladder point in class |
|---|---|---|---|---|---|
| SLV25 | 50 | 9 | −0.0560 | +2.95 pp | 34/50 |
| EWall | 26 | 3 | −0.0637 | +4.24 pp | 18/26 |
| SLV50 | 52 | 2 | −0.0435 | +1.27 pp | **52/52** |
| TOP40 | 10 | 2 | −0.0490 | +3.13 pp | 1/10 |
| TOP20 | 1 | 0 | −0.1733 | +0.31 pp | 0/1 |

SLV50's 52/52 is the sharpest single number in the run: **every** SLV50 class member has a
ladder point that is also in the class.  Its membership is entirely reproducible by scaling.

| panel | cost | n | beats | mean dSharpe | mean dOOS Sharpe |
|---|---|---|---|---|---|
| u56 | 10 | 40 | 7 | −0.0429 | **+0.0011** |
| u56 | 25 | 38 | 4 | −0.0439 | −0.0056 |
| broad | 10 | 34 | 3 | −0.0579 | −0.0187 |
| broad | 25 | 27 | 2 | −0.0751 | −0.0470 |

The deficit holds on both panels at both rungs and **widens with cost**: a member that
spends turnover to hold an exposure path pays for it, while a ladder point's turnover
scales down with its gross.  The OOS column is the same story one window later — the
members are OOS-neutral at best (+0.0011 on u56 @10 bps) and lose by 0.047 at the worst
corner.

## [C] The proposed recording rule

Applying the queue's proposal — *a `4b-defensive` row must beat its own ladder point to be
recorded at all* — the class goes **139 → 16 rows (11.5% survive)**, across **4 of 5 books**
(EWall, SLV25, SLV50, TOP40) and **2 of 5 arm kinds** (`gate`, `dd`).  Both conventions give
the same 16.  **`ebud` and `stop` are eliminated entirely**, and 74 of 89 gates with them.

## [D] Rule 8 — the rule is right about the corpus and inert about selection

Selectors fixed in writing before any OOS number was read; chosen on 2009-2016 alone,
2017-2026 read once, pooled over all books inside a (panel, cost) cell.

| selector | mean OOS Sharpe | mean OOS CAGR | mean OOS MaxDD | cells |
|---|---|---|---|---|
| S0 no screen | 0.9625 | 13.53% | −24.94% | 6/6 |
| S3 class (idea 133) | **1.2582** | 9.27% | **−14.37%** | 4/6 |
| **S5 class + beats own IS ladder** | **1.2582** | 9.27% | −14.37% | 4/6 |
| SPY (OOS) | 0.8820 | 15.45% | −33.72% | — |

**S5 changes S3's pick in 0 of 4 cells; paired OOS Sharpe delta +0.0000.**  The rule cuts
88.5% of the class on the full sample and yet removes nothing an IS chooser would have
picked, because the IS chooser lands on `SLV50/ebud-0.10` and `SLV25/ebud-0.10` — arms
that pass S5's *IS-window Sharpe* test even though they fail the full-sample AND test.
This is idea 129's CAGR-floor shape exactly: **a bar that is right about the corpus and
inert about selection.**  It should be adopted as a **reporting** requirement, and must not
be sold as a selector.

The small panel's two cells are `(empty)` for S3 and S5 — the class has no members there,
so S0's ungated picks (OOS Sharpe 0.6367 and 0.6831) are the only reading available, and
both lose to SPY.

## Caveats

1. **SURVIVORSHIP**: all three panels are current-constituent lists.  It runs against the
   members here: absent delistings inflate the ungated, fully-invested control most, so the
   ladder point the member must beat is if anything flattered, and 11.5% may be an
   under-count.  `broad` **contains** `u56`, so they are not two independent samples.
2. The IS window's SPY MaxDD (−22.1%) is shallower than the OOS window's (−33.7%), so any
   IS drawdown cap sits on a window that cannot express deep drawdowns; this biases every
   IS screen toward over-admission, **S5 included** — and S5 is an IS-window Sharpe test,
   which is why it does not reproduce the full-sample cut.
3. MaxDD is one number off one path; "beats on drawdown" inherits that fragility, and the
   whole `bud` family sits five basis points the wrong side of the line.
4. QUEUE idea 387 independently flags the entry budget as possibly unpriceable under its own
   denominator convention.  `ebud` is the family this test eliminates and the family the IS
   chooser keeps picking; that tension is stated, not resolved here, and no `ebud` result
   should be leaned on until 387 reports.
5. A matched-gross ladder point is **not** the same instrument as the member and is never
   quoted as one.
