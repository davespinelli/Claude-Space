# Idea 808 — does the DD leg of PROTOCOL 4b need a declared convention floor?

**Cloud lane, 2026-09-15, idea 1 of 2. ANSWERED: YES — and the floor is not survivable by anything
on the shelf. KILL for capital on all five k=0 4b passes in the declared book set; a PROTOCOL clause
is PROPOSED, NOT APPLIED (rule 6). RULES.md, PROTOCOL.md, scan.py, bot.py, baseline.py untouched.**

Script: `2026-09-15_does-the-DD-LEG-of-4b-need-a-CONVENTION-FLOOR_cloud.py`
Outputs: `.cells.csv` (3,744 rows) `.legs.csv` (1,440) `.clause.csv` `.walkforward.csv` `.console.txt`

## What was run

12 books (6 forms × 2 panels) × 26 rebalance calendars (MONTHLY offsets k=0…20, WEEKLY k=0…4)
× 2 lags (1, 2) × 2 cost rungs (10, 25 bps) × 3 windows (FULL / IS / OOS). Every cell is written to
CSV, pass or fail. Forms: MADG100 and MADG075 (idea 805's g/N-above-200d-MA, de-grossed to cash),
TOP20 (the 2026-09-04 first KEEP 4b: top 20 by the v1 composite without the vol scaler, 0.75/20 each),
TOP40 (idea 589/806's book at g=1.00), EWELIG (2026-09-03 Finding 2, equal-weight all eligible at
0.75 gross), RULESV2 (the live rules, verbatim from `baseline.rules_v2_weights`). Panels U56
(`load_universe()`) and B136 (`load_universe(broad=True)`); SPY is a tradable constituent of both and
the 4b comparand, which is the record's own construction and is not changed here.

The five 4b legs are recorded as **margins in their own units** (Sharpe points for H1/H2/OOS,
percentage points for DD and CAGR) rather than booleans, so each leg can be compared with its own
spread across the equally arbitrary calendars. `ratio = margin(k=0) / spread`; **ratio < 1 means the
published verdict on that leg is a date, not a rule.**

Two tuned parameters, as declared: (1) the book set, (2) the floor form
(FULLSPREAD = max−min, SD1, SD2). Cadence family, cost, lag, window and both KEEP paths are reported
and never selected on.

## Gates

| Gate | Result |
|---|---|
| G1 engine | `fast_run` vs `engine.backtest` max abs diff **2.08e-17** (bar 1e-9) — PASS |
| G2a triple | Sharpe 1.2081 vs published 1.21 PASS; MaxDD −15.49% vs −15.5% PASS; **CAGR 11.90% vs 11.92% MISS by 1.6e-4** — printed, not hidden: `data/prices.csv` has gained bars since 805 ran, and lane C's G2a′ on 805's own panel end already showed the book itself reproduces |
| G2b H_CAL | **13 of 21 offsets pass 4b, all 8 failures on the DD leg alone** — exactly idea 805's census — PASS |
| G2c numbers | DD-cap margin **4.74pp**, 21-offset MaxDD spread **8.37pp** — both exact to the 0.10pp bar — PASS |
| G3 bars | U56: SPY 15.13% / 0.885 / −33.72% → DD cap −20.23%, CAGR floor 10.59%. RULES v2 8.62% / 1.201 / −12.05% |

## 1. The DD leg is the convention-sensitive leg (H_DDWORST, H_DDFLIP: both CONFIRMED)

MONTHLY family, FULL window, 10 bps, lag 1, across the 12 books:

| leg | median ratio | min ratio | books with ratio<1 | offset flips | mean spread |
|---|---|---|---|---|---|
| H1 | 2.441 | 1.376 | 0/12 | 0 | 0.119 Sharpe |
| H2 | 1.218 | 0.355 | 5/12 | 26 | 0.219 Sharpe |
| OOS | 1.554 | 0.497 | 2/12 | 7 | 0.217 Sharpe |
| **DD** | **0.466** | **−0.990** | **10/12** | **52** | **7.71 pp** |
| CAGR | 0.877 | −3.816 | 8/12 | 3 | 1.46 pp |

DD holds **52 of 88 (59.1%)** of all leg-level offset flips. **The honest qualification: CAGR is
almost as bad on the ratio (0.877, 8 of 12 below 1) and is only innocent-looking because most books'
CAGR margins sit far from zero in either direction, so few flips result.** Both *level* legs are
convention-sensitive; the two *Sharpe* legs H1 and OOS are not (0 and 7 flips), and H1 never flips
in any of the 252 monthly cells at any cost or lag. So the asymmetry idea 805 found on one book is a
property of the levels, not of that book — but it is a DD-**and**-CAGR property, not DD alone.

Per-book DD leg (margin0 / spread in pp): B136 TOP40 −10.50/10.60, B136 TOP20 −5.88/6.99,
B136 EWELIG −1.43/5.02, U56 TOP20 **0.72/7.40 (ratio 0.098)**, U56 TOP40 2.27/11.37, B136 MADG100
4.15/9.65, U56 EWELIG 3.22/6.40, U56 MADG100 4.75/8.37, B136 RULESV2 4.54/7.31, U56 RULESV2
5.85/6.01, B136 MADG075 7.96/7.21, U56 MADG075 8.40/6.25. Only the two MADG075 books clear their own
full spread, and both of them **fail 4b on the CAGR floor** — the de-grossing that buys the drawdown
margin is the same de-grossing that loses the return (ideas 662/866/676's channel, priced again here).

## 2. The DD leg is entirely a post-2017 object

**FULL-sample MaxDD equals OOS-window MaxDD in 252 of 252 monthly book-calendar cells, and equals the
IS-window MaxDD in 0 of 252.** Every book's binding drawdown is after 2017 (lane C found all 21
sleeves of the 805 book trough inside March 2020). So the 4b DD leg has no in-sample counterpart at
all: its level cannot be measured before the outcome window is read, and its calendar noise is the
noise of one crash episode seen 21 times.

## 3. The clause priced (H_BITE CONFIRMED — it is not vacuous; it is fatal)

5 of 12 books pass 4b at k=0 (U56: MADG100, TOP20, TOP40, EWELIG; B136: MADG100). Under
`margin > floor` on **every** leg:

| floor form | books surviving (of the 5) | surviving a DD-leg-only clause |
|---|---|---|
| FULLSPREAD (max−min) | **0** | **0** |
| SD1 | 3 | 3 |
| SD2 | 1 (U56 EWELIG) | 1 |

The queue's own floor form kills every 4b pass on the shelf, including the record's 2026-09-04 first
KEEP 4b (U56 TOP20: DD margin 0.72pp against a 7.40pp spread; it passes 4b on only **7 of 21**
calendars). Which leg binds is the second finding: for 4 of the 5 passers the binding leg list
contains DD, and for 3 of them it also contains CAGR.

## 4. Rule 8 walk-forward — is the floor knowable in sample? (H_WF: CONFIRMED, weakly)

Floors measured on IS (…2016-12-31) only, then read once against OOS (2017-01-01…). Spearman
rho(IS spread, OOS spread) across the 12 books: CAGR **+0.951**, H2 +0.573, OOS +0.573 (identical to
H2 by construction — inside a single window the OOS leg collapses into that window's own second half;
stated, not hidden), DD **+0.469**, H1 +0.322. So 3 of 5 legs clear +0.5 and the *DD* floor — the one
the clause is about — is the second-least predictable of the five.

Does the IS clause predict OOS calendar stability? Over book-leg pairs that pass their leg in sample:

| selector | n | OOS leg passes | OOS verdict unanimous across all 21 calendars |
|---|---|---|---|
| IS margin > 0 (naive) | 54 | 96.3% | 64.8% |
| IS margin > IS spread (clause) | 26 | 96.2% | **76.9%** |

Per leg (naive → clause, OOS-unanimity): DD **27.3% → 60.0%**, CAGR 71.4% → 100.0%, H2 91.7% → 87.5%,
H1 41.7% → 0.0% (n=2). The clause more than doubles DD's OOS calendar-stability rate and costs nothing
on the leg it is aimed at — but it halves the admitted set, and on H1 it selects the wrong two books.
**It is a real screen on the level legs and noise on the Sharpe legs.**

## 5. OOS triples at k=0 (10 bps, lag 1, monthly), required reporting

U56 — RULES v2 OOS 9.46% / 1.277 / −12.05%; SPY OOS 15.27% / 0.874 / −33.72%:
MADG100 12.61% / 1.267 / −15.49% 4b PASS · TOP20 16.67% / 1.282 / −19.51% 4b PASS ·
TOP40 16.10% / 1.292 / −17.96% 4b PASS · EWELIG 12.98% / 1.216 / −17.01% 4b PASS ·
MADG075 9.40% / 1.265 / −11.83% fails CAGR · RULESV2 9.56% / 1.224 / −14.38% fails CAGR.

B136 — RULES v2 OOS 7.88% / 1.106 / −12.24%; SPY OOS 15.33% / 0.877 / −33.72%:
MADG100 11.00% / 1.142 / −16.08% 4b PASS · TOP20 15.55% / 1.000 / −26.11% fails DD ·
TOP40 19.49% / 1.100 / −30.73% fails DD · EWELIG 12.02% / 1.074 / −21.66% fails DD ·
MADG075 8.22% / 1.142 / −12.27% fails CAGR · RULESV2 8.25% / 1.084 / −15.69% fails CAGR.

**4a: 0 of 12 books at k=0, and 0 of 1,008 cells anywhere in the run** — every book here is a growth
book against a low-return live baseline, which is exactly why PROTOCOL added 4b.

## 6. Cadence (H_CADENCE CONFIRMED) and robustness

Mean spread, WEEKLY ÷ MONTHLY: H1 0.697, H2 0.403, OOS 0.372, **DD 0.406**, CAGR 0.650; weekly spread
is smaller in **57 of 60** book-leg pairs. The live book's own weekly cadence is roughly 2.5× less
calendar-exposed on the DD leg than a monthly one — the clause bites hardest exactly where the record
has been publishing monthly candidates.

4b pass counts over all 252 monthly book-calendar cells: 61 (10 bps, lag 1), 50 (10 bps, lag 2),
54 (25 bps, lag 1), 43 (25 bps, lag 2). The DD leg is the most common failure at every rung
(107 / 124 / 107 / 126 failures) and H1 fails **0** times in all four.

## Verdict

**ANSWERED: YES, the DD leg needs a declared convention floor — but the honest form of the clause is
wider than the queue's, and its cost is that the shelf empties.** The DD leg is the most
convention-sensitive 4b leg (median ratio 0.466, 10 of 12 books under 1, 59% of flips, entirely a
post-2017 object with no in-sample counterpart), the CAGR leg is nearly as bad by ratio, and the two
Sharpe legs are stable. Under the queue's own FULLSPREAD floor, **0 of 5** k=0 4b passes survive,
including the 2026-09-04 first KEEP 4b. **KILL for capital on every book in the set.**

**PROPOSED PROTOCOL clause (rule 6: proposed, NOT applied; PROTOCOL.md untouched):** *add to rule 4b —
a 4b pass on a LEVEL leg (MaxDD cap, CAGR floor) must be published with the leg's spread across the
book's own rebalance-calendar family (21 trading-day offsets for a monthly book, 5 for a weekly one)
and must clear its bar by more than 2 standard deviations of that spread; a pass whose margin is
inside its own convention spread is reported as a date, not a rule. The Sharpe legs (H1/H2/OOS) need
no such floor — they never flipped across 1,008 calendar cells in this run.* SD2 rather than
FULLSPREAD because max−min is unbounded in the family size (a 21-offset family is 4× more likely to
hit an extreme than a 5-offset one), which would make the floor a function of the cadence rather than
of the book.

**Survivorship:** U56 and B136 are current-constituent lists; all CAGRs are optimistic and both level
bars are easier to clear than on a point-in-time panel. This run's headline quantity — the *spread* of
a leg across equally arbitrary calendars — is a within-book quantity and is far less exposed to that
bias than the levels are.

**By-product for open idea 806** (*do any committed MONTHLY 4b passes have a DD margin smaller than
their own offset spread*): on this declared book set the answer is **10 of 12 books, and 4 of the 5
that pass 4b at k=0**. 806's remaining half — the census of the record's committed monthly 4b rows —
still needs a lane that scores the record.
