# Idea 135 — is a `4b-defensive` class member just its own ladder point?  (lane B)

**2026-09-07, lane B. INDEPENDENT SECOND RUN of idea 135, written and launched before the
cloud lane's answer landed on `main`, and only cross-checked against it after both had
finished. Verdict: CONFIRM of the cloud's answer (reproduced at 0.000e+00 on all 748 rows
and all 139 ladder points), plus a KILL of the proposed recording rule at every usable
margin, plus a DEFECT: the record's own 4a bar has been priced against three different
comparands and the two runs of THIS idea disagree on 116 of 748 rows.**

Script `2026-09-07_is-a-class-member-just-its-own-ladder-point_B.py`; artefacts `.grid.csv`
(748 arm rows, each carrying a full-window AND an IS-window matched ladder point),
`.survival.csv` (the 8-point eps x stat rule grid), `.walkforward.csv` (72 rows),
`.paired.csv`, `.console.txt`.

## What was priced

The queue's control, verbatim: every arm against **its own book's static-gross ladder point
at matched mean gross** — the same book, ungated, no overlay, at the one static multiplier m
whose mean gross over the same window equals the arm's. Two matches per arm: one solved on
the full evaluation window (for the census) and one on the **IS window alone** (so the rule-8
screen uses no future information — the cloud run did not carry this second match).

Corpus inherited from idea 133 without change: 3 panels x 8 books (small panel has no
TLT/GLD/DBC/UUP, so its 2 sleeve books are skipped) x 17 arms x 2 cost rungs = **748 rows**,
native gross.

**Tuned parameters, exactly two, all points reported**: `eps` in {0.00, 0.05, 0.10, 0.15}
(the Sharpe margin the rule demands) and `stat` in {`sharpe`, `dom`} (Sharpe margin alone, or
that AND MaxDD no worse). Panels, books, arms, gates, dials, cost rungs, windows and 4b's
coefficients (phi 0.70, delta 0.60) are census axes, selected on nothing.

## Gates (printed before any new number)

| gate | what | result |
|---|---|---|
| a | idea 94's published `EWall+vol60-dg u56@10bps` | 11.587% / **1.133** / -16.884% vs published 11.6/1.133/-16.9 — PASS |
| b | `H.run` with every instrument off == `engine.backtest` | **0.000e+00** |
| c | **the ladder is not a rescaling** — `max\|r(m=0.5) - 0.5·r(m=1)\|` | **1.394e-03**; Sharpe 1.1240 (m=1) vs 1.1229 (m=0.5). The cash leg re-drifts, so Sharpe is only NEARLY gross-invariant — which is what gives the question content |
| d | matched-gross solve | worst `\|achieved - target\|` **9.36e-10** (full-window), **5.33e-10** (IS-window); 0 of 748 rows worse than 5e-3 |
| e | idea 133's committed native-gross census re-run | **748/748 rows**, max\|d Sharpe\| **2.220e-16**, `floor_only` mismatches **0**, `pass4b` mismatches **0** |
| f | **cross-run**: this run vs the cloud lane's committed `.grid.csv` and `.test.csv` | **748/748 rows and 139/139 members at max\|d\| = 0.000e+00** on CAGR, Sharpe, MaxDD, OOS_Sharpe, gross, `lad_Sharpe`, `lad_MaxDD`, `lad_CAGR`, `ladder_m`, `d_Sharpe`, `lad_floor_only` — **except `pass4a`, see the defect below** |

## The answer — H_ladder is CONFIRMED

- **139 of 748 rows (18.6%)** are `4b-defensive` class members.
- Their matched ladder point is **itself in the class in 105 of 139 (75.5%)**, and clears
  full 4b in 61 of 748 rows overall.
- The mean member has a **LOWER Sharpe (-0.0531)** and a **LOWER CAGR (-1.28 pp)** than a dumb
  static cut at the same average exposure, buying **+2.56 pp** of drawdown it needed no
  overlay to buy. Mean OOS Sharpe margin **-0.0149**.
- Beat rates — the cloud's 11.5% reproduced exactly, and located: it is the **dominance**
  convention. Under Sharpe alone it is 18.0%.

| stat | eps | all rows | class members | Pareto-best members |
|---|---|---|---|---|
| sharpe | 0.00 | 116/748 (15.5%) | **25/139 (18.0%)** | 9/16 (56.2%) |
| sharpe | 0.05 | 12/748 | **3/139 (2.2%)** | 2/16 |
| sharpe | 0.10 | 1/748 | **0/139** | 0/16 |
| sharpe | 0.15 | 0/748 | **0/139** | 0/16 |
| dom | 0.00 | 82/748 (11.0%) | **16/139 (11.5%)** | 5/16 (31.2%) |
| dom | 0.05 | 12/748 | 3/139 | 2/16 |
| dom | 0.10 | 1/748 | 0/139 | 0/16 |
| dom | 0.15 | 0/748 | 0/139 | 0/16 |

**The proposed rule is a knife-edge, not a margin.** It is not "require a margin": at any
eps >= 0.10 it deletes the class outright, and at eps = 0.05 it leaves 3 rows of 139. The
only setting that leaves a class at all is eps = 0.00, where 82-88% of members still fail.

## Three things this run adds to the cloud's

**1. The ladder margin PERSISTS out of sample and is not the gross dial.**
`rho(d_Sharpe, d_OOS_Sharpe) = +0.802` over the 139 members: an arm that beats its own ladder
point in-sample tends to keep doing so. `rho(gross, d_Sharpe) = +0.069` (vs `rho(gross,
Sharpe) = +0.245`) — the margin is a property of the overlay, not of where it sits on the
exposure axis. That makes the rule's inertness in selection (below) the more damning result:
the statistic is real, the screen built on it is not.

**2. It is one arm FAMILY, not the class, that survives the control.**

| kind | n | beat (sharpe, eps 0) | mean d_Sharpe |
|---|---|---|---|
| **bud** (entry-only turnover budget) | 10 | **9 (90.0%)** | **+0.015** |
| gate (5 trend gates x dg/rw) | 89 | 15 (16.9%) | -0.057 |
| stop (trailing stops) | 12 | **0** | -0.035 |
| dd (book drawdown control) | 23 | 1 (4.3%) | **-0.089** |
| ctl (the control arm itself) | 5 | 0 | **0.000** (self-check: an arm IS its own m=1 ladder point) |

Stops and drawdown controls are **strictly worse than de-grossing** at the same average
exposure. Entry budgets are the one family that does something a static cut cannot.

**3. The class is nearly a property of two books' de-grossed controls.** Ladder-point class
rate by book: **SLV50 68/68 (100%)**, SLV25 57.4%, EWall 17.6%, TOP40 3.9%, TOP20 2.0%,
TOP10 1.0%, TOP5 and V1u **0.0%**. Where the class is dense the ladder is already in it.

## Rule 8 walk-forward (parameters on 2009-2016, 2017-2026 read once)

Cells pool all books within a (panel, cost) pair; 6 cells. `S3L` is the proposed screen,
applied to the **IS-window** matched ladder point.

| selector | OOS CAGR | OOS Sharpe | OOS MaxDD | beats SPY | beats RULES v2 | beats ctl | mean OOS rank |
|---|---|---|---|---|---|---|---|
| S0 (no screen) | 13.5% | 0.962 | -24.9% | 4/6 | 4/6 | 3/6 | 39.8 |
| S1 (4b IS, phi 0.70) | 13.1% | 1.153 | -20.7% | 4/6 | 2/6 | 3/6 | 33.8 |
| S2 (floor deleted) | 10.6% | 1.219 | -16.9% | 4/6 | 3/6 | 3/6 | 17.8 |
| **S3 (the class selector)** | 9.3% | **1.258** | **-14.4%** | 4/6 | 3/6 | 4/6 | **9.8** |
| S3L (sharpe, eps 0) | 9.3% | 1.258 | -14.4% | 4/6 | 3/6 | 4/6 | 9.8 |
| S3L (sharpe, eps 0.05) | 8.3% | 1.225 | -13.6% | 1/6 | 1/6 | 1/6 | 3.0 |
| S3L (dom, eps 0) | 10.0% | 1.169 | -15.1% | 2/6 | 1/6 | 1/6 | 48.5 |
| S3L (eps >= 0.10, either stat) | — | — | — | 0/6 | 0/6 | 0/6 | picks nothing |

References, means over the 6 cells: **SPY OOS 15.45% / 0.882 / -33.72%**; **RULES v2 (live)
OOS 6.94% / 0.966 / -13.11%**; RULES v1 OOS Sharpe 0.451; ungated EWall control OOS 0.952.

Paired against S3, per cell:

| stat | eps | picks moved | cells emptied | mean d OOS Sharpe | min |
|---|---|---|---|---|---|
| sharpe | 0.00 | **0 of 6** | 2 | **0.0000** | 0.0000 |
| sharpe | 0.05 | 3 of 6 | 5 | 0.0000 | 0.0000 |
| dom | 0.00 | 4 of 6 | 4 | **-0.1441** | **-0.2051** |
| either | >= 0.10 | 4 of 6 | 6 | (no picks) | — |

**The rule is inert where it is harmless and harmful where it bites.** At its only
non-destructive setting it changes nothing (0 of 6 picks — the cloud's "0 of 4" on its own
cell count, reproduced); the dominance version moves 4 of 6 picks, empties 4 of 6 cells and
costs **-0.144 mean OOS Sharpe**; every eps >= 0.10 leaves the selector with nothing to pick.

## DEFECT found by the cross-run check — the 4a comparand is unstated

The two independent runs of this idea agree at 0.000e+00 on every performance number and
**disagree on `pass4a` for 116 of 748 rows** (cloud 294, this run 314):

- the cloud run prices 4a against `H.run(px, book_targets(px,"V1u"), bps=10.0)` — the **V1u
  book at a FIXED 10 bps**, used to judge 25-bps arms as well;
- this run prices it against `baseline.rules_v1_weights` at **the arm's own cost rung** (314
  of 748), and separately against the **LIVE RULES v2** (4 of 748).

Both differences are material. `book_targets(px,"V1u")` is **not** `rules_v1_weights`
(max|dW| **0.15** — V1u is ungated, the live v1 applies its eligibility filter). And the rung
alone moves the bar enormously: RULES v1 halves are **0.641 / 0.688 at 10 bps** but
**0.285 / 0.346 at 25 bps**, so a 25-bps arm judged against a 10-bps baseline faces a bar
roughly twice as high. PROTOCOL rules 3 and 4a say "the current live rules", which since
2026-09-06 is **v2** — on that reading the corpus's 4a count is **4 of 748**, not 294 or 314.
Recorded here, not fixed: PROTOCOL/`baseline.py` are out of scope for a research run.

## Both KEEP paths on all 748 rows

- **4b: 59 of 748** (identical to the cloud's count). Cross-cell survivors (4b in all four
  u56/broad x 10/25bps cells): **EWall/band3-rw and EWall/vol60-dg** — the record's standing
  pair, nothing new.
- **4a vs RULES v2 (live): 4 of 748**, all `broad` sleeve books (SLV25 1, SLV50 3).
- **4a vs RULES v1, cost-matched: 314 of 748.**
- **No new KEEP; no rules change proposed. No memo filed.**

## Caveats carried

- **Survivorship** (idea 54): three current-constituent panels. It runs one way here — absent
  delistings inflate the ungated, fully-invested ladder control most, so H_ladder is if
  anything measured against a FLATTERED comparand, which cuts against the verdict, not for it.
- **Idea 128**: the IS window (SPY MaxDD -22.1%) is shallower than the OOS window (-33.7%), so
  every IS screen over-admits; this hits S3 and S3L identically and cannot explain the gap.
- **Idea 38**: u56/broad still carry the calendar-day index; it applies identically to an arm
  and to its own ladder point and cancels in the paired comparison.
- MaxDD is one number off one path, so the `dom` statistic — the one the cloud's headline
  uses — inherits that fragility. This is why both conventions are reported.
- The small panel contributes **0 class members and 0 4b passes** at either rung, so the
  headline is a u56/broad statement.
