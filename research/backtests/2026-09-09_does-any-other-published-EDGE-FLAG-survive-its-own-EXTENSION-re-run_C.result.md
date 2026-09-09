# Idea 509 — does any other published EDGE FLAG survive its own EXTENSION re-run?

**Verdict: ANSWERED — the queue's premise is CONFIRMED, and sharpened. Of the flagged
units that can be extension-tested at all and whose curve is not flat, **78.8% MIGRATE_EDGE**:
the flag simply re-fires at the new grid top. It is a reporting habit. But the bigger
finding is that **most of the record's edge-flag mass cannot be tested at all** — 61.9% of
flagged units sit on a STRUCTURALLY CLOSED endpoint and another 44.6% of the record's edge
cells sit on a pure SCALE dial whose Sharpe is analytically invariant.**
No KEEP-candidate, no memo, no RULES change. RULES.md, PROTOCOL.md, scan.py, bot.py and
baseline.py untouched.

Lane C, 2026-09-09. Script
`2026-09-09_does-any-other-published-EDGE-FLAG-survive-its-own-EXTENSION-re-run_C.py`;
raw output `.console.txt`, `.arms.csv` (every grid point at every depth), `.extension.csv`
(every verdict), `.walkforward.csv`, `.census.csv`, `.textcensus.csv`.

## Design
Two tuned parameters, exactly the queue's: **FLAG (the flagged dial family) x EXTENSION
DEPTH (0/1/2/3 steps past the published stop)**. 7 flags (n, band, gross, m, volcap,
quantile, cadence) x 3 panels (U56 / B136 / SMALL439) x 2 cost rungs (10 bps headline, 25
bps a second reading of the *same* books) = **448 flag arm-rows, 352 on published grids and
96 EXTENSION arms**, all reported. Weekly except on the cadence dial; weights at close t
applied at t+1; no shorting, no leverage; no network.

Everything pre-registered before a number was read:
- **Extension geometry.** HIGH end -> arithmetic, step = the grid's own last step. LOW end
  -> geometric, ratio = the grid's own first ratio (every low end here is a positive scale
  bounded below by 0). Depth k = k such steps. Depth 0 = the published grid untouched.
- **Endpoint status.** STRUCTURAL when the instrument cannot be widened: n high = the
  panel's own name count, low = 1; band low = 0.00 (no hysteresis is the plain 200d MA
  rule); gross high = 1.00 and m high = 4/3 (PROTOCOL 2, no leverage — m multiplies a 0.75
  target gross); volcap high = 9.99 and quantile high = 1.00 (no filter); **cadence BOTH**
  (D is the engine's fastest schedule, Q its slowest) — the CONTROL flag, a dial whose edge
  flags cannot be extension-tested at all. A step crossing a bound, or emptying the book
  (mean held names < 1), is recorded **CLOSED** and no arm is run past it.
- **Verdicts** per (flag, panel, cost, outcome, depth): **SURVIVES** (argmax still the
  published endpoint the flag named) / **MIGRATE_EDGE** (argmax at the NEW extended
  endpoint — the flag re-fires one grid wider) / **MIGRATE_INTERIOR** (argmax strictly
  interior — the flag was a stopping-point artefact and a real optimum exists, idea 500's
  band = 0.16 shape) / **CLOSED**. Argmax read on 5 outcomes: full Sharpe, binding-half
  Sharpe min(H1,H2), CAGR, MaxDD, OOS Sharpe.

## Reproduction gates, run before any new number
- **idea 256's census reproduces from its own committed cells file**: 22,443 cells (published
  22,443), argmax at a grid END **87.368%** (published 87.4%), edge_mono **66.876%**
  (published 66.9%).
- **RULES v2 U56 @10bps**: 8.64% / 1.2037 / -12.05%, halves 1.2309 / 1.1828 — matches idea
  500's same-day read to the digit.
- **idea 270R SMALL439 band=0.05 @10bps**: 4.18% / 0.6183 / -14.59%, halves 0.6385 / 0.6031
  (published 4.18% / 0.6183 / -14.6% / 0.6385 / 0.6031). **Exact.**
- **idea 500's own extension point reproduces**: SMALL439 band=0.16 halves 0.7245 / 0.6195,
  MaxDD -16.86% (idea 500 published 0.7245 / 0.6195 / -16.9%). The predecessor's extension
  is inside this run's grid, so this is a nested re-run, not a new sample.
- Cost decomposition (one gross backtest, both rungs derived) vs `engine.backtest(cost_bps=10)`:
  **0.000e+00**.
- Unplanned gate: **scale invariance**. max|r(gross 0.50)/2 - r(gross 0.25)| = **1.691e-04**,
  dSharpe **+0.00009** — see (2).

## (0) The flag population — two censuses
**TEXTUAL (the claims).** 544 committed `.md` files scanned; **52 carry edge-flag language,
216 phrases in all** (grid-edge 190, monotone-to-widest 22, argmax-at-end 4). The register
files carry most of it (LEADERBOARD 52, QUEUE 41, CHANGELOG 28); the heaviest result files
are idea 256's own (6), idea 500's (6), then cadence/band/n files at 3-4 each.

**NUMERIC (the shapes).** idea 256's 22,443 cells, 61 files, 21 dials, 81 (file,dial) grids;
**19,608 cells at an edge**, of which 76.5% monotone. By dial: **m 6,866 · cost 2,529 ·
cost_bps 2,069 · g 1,870 · floor_musd 1,486 · fin 1,341 · phi 1,230 · n 889**. Flags point
LOW 14,270 times and HIGH 5,338, so the extension has to run in both directions — it does.

## (1) THE ANSWER — the flag re-fires; it does not survive
**126 of 210 (flag, panel, cost, outcome) units are flagged** (84 argmaxes are already
interior and carry no flag). At depth 3:

| | CLOSED | MIGRATE_EDGE | MIGRATE_INTERIOR | SURVIVES |
|---|---|---|---|---|
| depth 1 | 72 | 45 | 0 | 9 |
| depth 2 | 76 | 39 | 6 | 5 |
| depth 3 | 78 | 39 | 5 | 4 |

**Extension-testable at depth 3: 48 of 126 — SURVIVES 4 (8.3%), MIGRATE_EDGE 39 (81.2%),
MIGRATE_INTERIOR 5 (10.4%).** The other **78 (61.9%) are CLOSED**: the endpoint is
structural (gross 1.00, quantile 1.00, volcap 9.99, cadence D and Q, n = the panel's name
count) or the book empties before three steps (n = 1; quantile 0.016 and 0.0064 hold under
one name). Cadence — the pre-registered control — is CLOSED in 11 of 11 units, as designed.

Depth matters barely: the SURVIVES count falls 9 -> 5 -> 4 as the grid widens and
MIGRATE_INTERIOR only appears at depth 2. **One step past the stop is already enough to
break most flags, and two more steps buy almost nothing.**

## (2) THE UNPLANNED LEG — 44.6% of the record's edge mass is arithmetic, not evidence
The gross and m columns came back **flat to the 4th decimal** on every Sharpe outcome:
grid spread of full Sharpe is **0.0003 / 0.0004 / 0.0001** (gross, U56 / B136 / SMALL439)
and **0.0007 / 0.0010 / 0.0020** (m), against 0.41-0.57 for n, 0.43-0.47 for quantile and
0.56-0.59 for volcap on the same panels. That is not a finding about those books, it is
arithmetic: **both are pure SCALE dials** — multiplying every weight by k multiplies the net
return by k exactly, because costs are proportional to turnover and turnover scales too, so
Sharpe is analytically invariant and only the NAV-rebalancing residual moves it. The gate
confirms it: max|r(gross .50)/2 - r(gross .25)| = **1.691e-04**, dSharpe **+0.00009**.

A tolerance was fixed once, after that was seen, and applied to every flag equally
(Sharpe-family 0.01, CAGR/MaxDD 0.1 pp): **21 of the 126 flagged units are VACUOUS, every
one of them a gross-or-m Sharpe leg.** Restated on the **33 units that are both testable
and material**: **SURVIVES 4 (12.1%), MIGRATE_EDGE 26 (78.8%), MIGRATE_INTERIOR 3 (9.1%)**.
The verdict does not depend on the tolerance — it is 81.2% before it and 78.8% after.

**Record-wide, 8,736 of 19,608 edge cells (44.6%) sit on dial `m` or dial `g`.** Every
Sharpe-outcome edge flag in that 44.6% is decided in the 4th decimal. What those two dials
*do* move monotonically is CAGR (10-14 pp across the grid) and MaxDD (15-39 pp) — and both
of those flags are true by construction for a scale dial, at a structurally capped top.

## (3) The four SURVIVORS, quoted
Only four material units survive to depth 3, and three are the same dial on the same panel:
**n = 60 on SMALL439** (binding-half Sharpe at 10 bps; full Sharpe, binding-half and CAGR at
25 bps), plus **volcap = 0.30 on B136 at 25 bps** on MaxDD. Idea 240's n flag is therefore
the record's only edge flag that holds anywhere under extension — and it holds on exactly
one of three panels: on B136 the same flag MIGRATE_EDGEs to n = 120 on all four material
outcomes at both rungs, and on U56 it is CLOSED because 60 already exceeds the panel's 55
names. Idea 240's own reading ("n tracks the panel's eligible count, ceiling unlocated
above 60") is what this reproduces; "take the widest n" stays killed.

Idea 500's band flag behaves as it published: at 10 bps the B136 binding-half argmax leaves
the endpoint, and at 25 bps it lands **MIGRATE_INTERIOR at band 0.45** on a 13-point grid.

## (4) Rule 8 — widening moves the answer, not the outcome (idea 256 replicated)
Arm chosen on 2009-2016 IS Sharpe alone, 2017-2026 read once. **168 cells (7 flags x 3
panels x 2 rungs x 4 depths), all reported.**

| depth | cells | pick at a grid edge | OOS Sharpe (median) | vs live book | wins | vs SPY | wins |
|---|---|---|---|---|---|---|---|
| 0 | 42 | 20 | 0.9775 | -0.1243 | 5/42 | +0.0972 | 23/42 |
| 1 | 42 | 24 | 0.9434 | -0.1385 | 6/42 | +0.0614 | 23/42 |
| 2 | 42 | 19 | 0.9547 | -0.1272 | 6/42 | +0.0727 | 23/42 |
| 3 | 42 | 20 | 0.9781 | -0.1159 | 6/42 | +0.0977 | 24/42 |

**Widening MOVES the rule-8 pick in 7 of 42 cells (16.7%)** and the moved picks are worth
**-0.0523 median OOS Sharpe against the live book**. Depth-3 pick minus depth-0 pick:
**median +0.0000, mean +0.0106, sd 0.0799, wins 6/42, t +0.86** — indistinguishable from
zero, and a close independent replication of idea 256's own +0.0178 at t +0.91 on a
different flag set, panel set and depth ladder. The rule-8 pick sits at a grid edge in
19-24 of 42 cells at every depth, i.e. **the walk-forward chooser re-creates the edge flag
as fast as the extension removes it.** No depth beats the live book: the median pick is
0.116-0.139 of OOS Sharpe behind RULES v2 everywhere.

## (5) KEEP paths — nothing promoted
**4a: 4 of 448 arm-rows** (published grids 2/352, extension arms 2/96).
**4b: 16 of 448** (published 15/352, extension 1/96).

- The two published 4a passes are idea 270R's SMALL439 band=0.05 at both rungs, exactly as
  idea 500 found them.
- The two **new** 4a passes from the extension are one arm at two rungs, **B136 band=0.45**
  (10 bps: 4.63% / 1.1436 / -7.17%, halves 1.3260 / 1.1454). It clears by **de-grossing**,
  not by skill: mean held names fall 88.2 -> 31.7 and turnover 3.32 -> 0.35 x/yr against the
  live book, so exposure is not matched — idea 135/244's warning, and it fails 4b outright
  (CAGR 4.63% against a 4b floor of 10.66% = 70% of SPY's 15.23%).
- The one **new** 4b from the extension, **B136 n=120**, is not new: it holds 87.9 of the
  panel's 135 names, which is the same book as volcap=9.99 (87.9 held, 11.64% / 1.0566 /
  -20.12%) and quantile=1.00 — both of which already pass 4b **on the published grid**. The
  extension re-labelled a book the record already had.
- No arm at any depth beats the live RULES v2 book on the rule-8 OOS window. **Nothing is
  promoted and no memo is written.**

## What this does and does not say
It says the record's edge flag, where it can be tested at all, is a habit: the argmax moves
to whatever the new widest point is 4 times in 5, and widening buys +0.011 of OOS Sharpe at
t +0.86. It says that most of the flag mass is not testable — structurally closed endpoints
and pure scale dials together account for the large majority of it — so the honest fix is
not "always sweep wider" but **"state the endpoint's status beside the flag"**: STRUCTURAL,
VACUOUS (flat curve), or OPEN-and-untested. It does not say the underlying arms are wrong;
idea 270R's band=0.05 4a pass survived idea 500's extension and survives this one.

**SURVIVORSHIP:** B136 is the current constituents of `research/universe_broad.json`;
SMALL439 is the sub-$2B screen with the 44 tickers whose `max_1d_move >= 1.0` dropped first.
Neither is free of survivorship bias and no number above is quoted as a live expectation.
