# Idea 675 — is U56/CAND20's SINGLE-RUNG 4b pass a KNIFE EDGE or a REAL WINDOW? (lane B, 2026-09-15)

**ANSWERED = A REAL WINDOW. The queue's "knife edge" premise is REFUTED: idea 670's "passes at
exactly one rung of eight" is a statement about idea 670's RUNG SPACING, not about the book.**
The book's already-committed (2026-09-04) **4b KEEP-candidate** status is unchanged; this run removes
one fragility objection from it and adds two new, quantified ones. No RULES change, no new book
promoted, no PROTOCOL edit; `RULES.md`, `scan.py`, `bot.py`, `baseline.py` untouched.

> **INDEPENDENT SECOND CUT.** The cloud lane claimed and published idea 675 while this run was in
> flight, and its entry reached `origin/main` first, so **its PARK is the verdict on the record** and
> this file is corroboration, not a competing claim. Separate implementations — this one bisects the
> two monotone legs to 1e-4 on a 150-rung ladder; the cloud run scans 750 grosses and adds a SMALL
> panel and an offset axis — and they **agree to 1e-4 on every shared number**: window
> [0.6242, 0.8337] vs [0.6241, 0.8337], W **0.2094 vs 0.2095**, live 0.75 interior by +0.126/+0.084,
> IS window [0.7263, 0.8408] vs [0.7263, 0.8409], and the 25 bps break carried by `L1_H1` failing at
> **0 of 150** grosses here against **0 of 750** there. What this cut adds that the other does not:
> the two cost **closing prices** (window 34.9 bps vs five-leg 4b pass **21.8**; B136 25.0 vs
> **6.1**), the zero-parameter **PICK-LIVE** chooser, the window **midpoint** 0.7289 as the reason not
> to re-tune gross, the vintage-matched gate decomposition (G3b/G3c), and H5. This run's memo
> proposes no RULES change either, so the two lanes differ in label only.

## The headline

The 4b pass window on U56/CAND20 at 10 bps, solved by bisection on the two binding legs:

| | value |
|---|---|
| `g_min` (CAGR floor L5, binds from below) | **0.6242** |
| `g_max` (DD cap L4, binds from above) | **0.8337** |
| **W_exact** | **0.2094 of gross (20.94 gross points)** |
| live `g = 0.75` inside? | **yes**, margin **+0.126** below / **+0.084** above |
| window midpoint | **0.7289** — the live constant sits **0.021** from it |

Pre-registered bars: KNIFE EDGE if `W_exact ≤ 0.02`; REAL WINDOW if `W_exact ≥ 0.10` **and** 0.75
sits ≥ 0.03 inside both boundaries. **W_exact = 0.2094 → REAL WINDOW**, ten times the knife-edge bar.

## Why idea 670 saw one rung — reproduced, not asserted

The same 5-leg pass set read on ladders of different resolution:

| ladder | rungs | 4b-pass rungs | pass run | `W_ladder` |
|---|---|---|---|---|
| 0.25 | 6 | 1 | [0.75, 0.75] | 0.00 |
| **670's own 8 rungs** | 8 | **1** | **[0.75, 0.75]** | **0.00** |
| 0.10 | 15 | 2 | [0.70, 0.80] | 0.10 |
| 0.05 | 30 | 4 | [0.65, 0.80] | 0.15 |
| **0.01** | 150 | **21** | **[0.63, 0.83]** | **0.20** |

Idea 670's rungs bracketing the pass are 0.60, 0.75, 0.85. `g_min = 0.6242` sits 0.024 above its
0.60 rung and `g_max = 0.8337` sits 0.016 below its 0.85 rung, so a window 21 gross points wide
showed up as a single sample. The finding was a sampling artefact of a grid that was never built to
measure a width.

## The two fragilities this run adds, published beside the pass

**1. The 4b pass's cost tolerance is 21.8 bps, not 34.9.** Turnover is 11.01x/yr, so cost walks
`g_min` up against a nearly fixed `g_max` (the DD cap does not see cost). The DD-cap × CAGR-floor
**window** closes at **34.9 bps** on U56 — but the **five-leg 4b PASS** goes empty at **21.8 bps**,
because cost also drags the Sharpe legs. At 25 bps the window is still 0.0979 wide and 0.75 is still
inside it, yet 4b is FALSE at every one of 150 rungs: the H1-Sharpe leg fails (book 0.9283 vs SPY
0.9588). **Quoting the window's closing price alone would overstate the tolerance by 1.6x.**
On B136 the 4b pass closes at **6.1 bps — below PROTOCOL's own 10 bps rung**, so the pass is a
U56-only fact at the protocol cost (B136 4b at 0.75, 10 bps: FALSE).

**2. The in-sample 5-leg 4b pass set is EMPTY on U56.** At 10 bps the IS (2009–2016) legs read
`L1 0/150 · L2 150/150 · L3 150/150 · L4 84/150 · L5 78/150`. The H1-Sharpe leg fails at **every**
rung in sample, so a chooser standing in 2016 had **no in-sample 4b passer to pick**. PICK-SHARPE
has an empty feasible set on U56; PICK-MIN and PICK-MID select from the DD-cap × CAGR-floor window
alone. H3 below is CONFIRMED only under choosers that ignore the Sharpe legs in sample, because in
sample they are unpassable.

## Rule 8 (PROTOCOL 8) — window and pick on 2009–2016 alone, 2017–2026 read ONCE

U56, 10 bps. IS window **[0.7263, 0.8408]**, W +0.1146. OOS SPY **15.272% / 0.8740 / −33.717%**;
OOS RULES v2 (live) **9.464% / 1.2772 / −12.055%**; OOS 4b bars DD cap −20.230%, CAGR floor 10.690%.

| chooser | g | OOS CAGR / Sharpe / MaxDD | OOS halves | OOS 4b | OOS 4a |
|---|---|---|---|---|---|
| PICK-LIVE (fits nothing) | 0.75 | **14.335% / 1.1233 / −18.308%** | 1.235 / 1.011 | **PASS** | fail |
| PICK-MIN (2026-09-03 memo's rule) | 0.7263 | 13.950% / 1.1232 / −17.845% | 1.235 / 1.011 | **PASS** | fail |
| PICK-MID (max margin) | 0.7836 | 14.913% / 1.1234 / −19.000% | 1.235 / 1.011 | **PASS** | fail |

**3 of 3 U56 choosers at 10 bps clear 4b out of sample**, including the zero-parameter one. Across
every (panel, cost, chooser): **OOS 4b 10 of 20, OOS 4a 0 of 20**; all 10 passes are tradeable
(g ≤ 1.00). H5: the windows solved on each half against its OWN half of SPY both contain the
full-sample midpoint (U56 H1 [0.6903, 0.8408], H2 [0.5668, 0.8337]) — the window is not a
full-sample-only object.

## Path 4a: 0 of 600 on each panel

CAND20's Sharpe is ~0.14 **below** the live band book's at every rung (1.0596 vs 1.2013 at 0.75) and
gross cannot move Sharpe — it travels 0.0015 across the entire 150-rung ladder. The 4a Sharpe legs
are unreachable by exposure. **4b is the only path this book travels**, on any rung, at any cost.

## Gates — 6 of 7 with a bar PASS; the one FAIL is named and localized

`G1` fast_backtest == engine.backtest **1.388e-17** (returns), **4.441e-16** (turnover).
`G2` `weights(g) == g·weights(1.00)` **5.551e-17**. **BAR CORRECTION, stated not hidden:** this
run's first pass set G2's bar at exact 0.0 and recorded a FAIL. The bar was unreachable — the two
sides divide by the name count in a different order (`g/k` vs `g·(1/k)`) and differ in the last bit
of a double. Idea 670 hit and published the same correction; 1e-12 is the record's float bar.
`G7` the fine ladder priced from `g·W(1.00)` equals the record's `g/k` book on every metric
**6.661e-16**. `G5` monotonicity 0 violations in 149 steps × 40 blocks. `G6` determinism **0.0**.
`G4b` SPY and RULES v2 reproduce their committed U56 triples vintage-matched at **1.782e-05**.

**`G3b` FAILS at 1.006e-02 against a 5e-4 bar and the failure is reported, not explained away.**
Idea 670's committed CAND20 grid does not reproduce on today's cache (**G3a 1.868e-02**), and
matching the row count to that run's own last dates (U56 2026-09-10, B136 2026-09-04) removes only
46% of the gap. Where the residual sits, per metric, worst over 8 rungs with its sign:

| panel | CAGR | Sharpe | MaxDD | H1 | H2 | OOS Sharpe |
|---|---|---|---|---|---|---|
| U56 | 9.91e-05 (+) | 5.57e-04 (+) | **7.50e-08** (−) | 5.75e-04 (+) | 5.50e-04 (+) | 5.14e-04 (+) |
| B136 | 1.31e-03 (+) | 5.98e-03 (+) | 4.78e-06 (−) | 1.01e-02 (+) | 2.32e-03 (+) | 2.32e-03 (+) |

MaxDD reproduces to 1e-8 and CAGR to 1e-5 on U56; the whole **Sharpe family** is off by a
uniform-signed ~5e-4. MaxDD is a path extremum and CAGR an endpoint ratio, while Sharpe averages
every day — the signature of small per-name revisions in the **adjusted** price history (the
record's own PRICES-VINTAGE effect), to which a 20-name concentrated book is far more exposed than
the 56-name band book. That is why G4b passes at 1.8e-05 on the *same* frames where G3b fails.
**`G3c`**, the reproduction restricted to the two metrics this run's headline is actually measured
on (CAGR and MaxDD, the only two that cut the window), **PASSES on U56 at 9.913e-05**. The same
restriction reads 1.310e-03 on B136, so **every B136 number here is a portability reading and no
headline rests on it.** Independently, the width itself is vintage-insensitive: solved on idea 670's
own vintage it reads [0.6216, 0.8337], W **0.2121**, |ΔW| **0.0026**.

## Scale and parameters

150 gross rungs × 4 cost rungs × 2 panels × 5 windows = **6,000 ladder cells**, plus 40 bisected
window solves (tol 1e-4), 4 cost-closure bisections and 20 rule-8 reads. **2 tuned parameters**
(gross resolution, cost rung), every value of both reported in `.ladder.csv` / `.window.csv`;
panel, window and price vintage are declared audit axes.

## Survivorship (PROTOCOL 9)

U56 (`research/universe.json`) and B136 (`universe_broad.json`) are **current-constituent** lists.
Every CAGR and drawdown LEVEL above is optimistic — the book's, RULES v2's and SPY's alike — and
both 4b bars are easier here than on a point-in-time panel. The **width** headline is a same-tape,
same-names statement about one book's gross axis against its own SPY bars and is far less exposed;
the OOS triples and the 4b pass counts are levels and are **upper bounds**.

## Follow-ups filed

**921** (publish the FIVE-LEG cost closing price, not the window's, beside every committed 4b pass)
and **922** (why is the IS H1-Sharpe leg unpassable for CAND20 on U56 at every gross). This run's
draft 918 — re-read every committed gross band at 0.01 resolution — was **dropped as a duplicate**:
the cloud lane had already filed it as **919** from the same finding. The cloud lane's **918**
(which half carries the 25 bps break, across the record) and **920** (publish the margin beside every
committed `L3_OOS` verdict) also stand and are not re-filed here.
