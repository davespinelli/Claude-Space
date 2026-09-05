# Idea 122 — price-denominators-need-a-sign-test (lane C, 2026-09-05)

**Verdict: ANSWERED — the queue's premise is NOT literal on the large-cap lists. The sign
test is worth adopting as a REPORT-ONLY PROTOCOL clause and is a KILL as a selector.**

Script `2026-09-05_price-denominator-sign-test_C.py`; console
`…_C.console.txt`; data `…_C.{signtest,bootstrap,d3,grid,walkforward,oossign,survival,
reproduction}.csv`. 40 draws × 3 drop fractions × 3 books × 17 arms × 2 universes
(≈ 12,400 sub-panel backtests) plus the 4-rung cost axis. Nothing was modified.

## 0. Reproduction (the audit is of the published file, not a re-derivation)

Cached-signal target path equals idea 94's `targets()` **exactly** (max|diff| 0.0e+00), and
this run's `(dCAGR, dMaxDD, rate)` equals idea 94's published `pricelist.csv` on **192 of 192
rows**: max|diff| dCAGR 8.9e-16, dMaxDD 1.8e-15, rate 1.1e-16, NaN-pattern agreement 192/192.
138 of the 192 rows carry a published rate (idea 94's `dMaxDD > 0.10 pp` floor).

## 1. The sign test (pre-registered, three nuisance axes)

A published rate is **admissible** only if its denominator `dMaxDD = |MaxDD_ctl| − |MaxDD_arm|`
is positive under all three:

| axis | perturbation | published rows passing |
|---|---|---|
| D1 cost | `> 0` at 0, 5, 10 and 25 bps | **133 / 138 (96.4%)** |
| D2 window | `> 0` in BOTH 2009–2016 and 2017–2026 | **98 / 138 (71.0%)** |
| D3 panel | `> 0` in ≥ τ of 40 draws deleting q of the names | **114 / 138 (82.6%)** |
| **all three** | | **90 / 138 (65.2%)** |

Headline (q, τ) = (0.10, 0.90), adopted unchanged from idea 119 so this run could not pick its
own bar. All 12 grid points reported (`…grid.csv`); the count is flat across them —
**80–96 of 138 (58–70%)** — so the test is insensitive to its own two tuned parameters.

## 2. The premise is not literal here, and the instability has an address

Idea 119 found the small-panel denominator a coin flip (sign held 49/80). On idea 94's
large-cap lists **two thirds of the published prices survive**, and the failures are not
spread across the list — they are concentrated in two places:

- **The book, not the panel.** Every one of the 24 D3 failures and all 5 D1 failures are in
  **V1u**, the 5-name concentrated book (admissible 16/41). `EWall` is 47/48, `TOP20` 27/49.
  A 5-name book's MaxDD is one name's bad month, so its denominator has no stable sign;
  a 56- or 136-name equal-weight book's does.
- **The window, not the cost.** 40 of the 138 rows have `dMaxDD_IS ≤ 0` and **0 of 138 have
  `dMaxDD_OOS ≤ 0`**. Median `dMaxDD` by book is IS 0.03 pp (TOP20) / 0.17 (V1u) / 3.25
  (EWall) against OOS 3.83 / 2.27 / 6.92. The 2009–2016 window (SPY MaxDD −22.1%) is too
  shallow for a drawdown instrument to buy anything measurable; 2017–2026 (−33.7%, with 2020
  and 2022) is not. This is idea 117's point arriving through the denominator's sign.

Predictions P1 (fewer than half survive) and P3 (cost is the binding axis) are **REFUTED**;
P2 (`-rw` fails more than `-dg`: 23/52 vs 30/48 admissible, median dMaxDD 3.76 vs 5.68 pp) is
CONFIRMED.

## 3. Rule 8 walk-forward — the screen must not be used to choose

Screen computed on 2009–2016 only (IS cost axis + IS-window draws); 2017–2026 untouched.
S1 = idea 94's selector (cheapest IS rate among arms buying ≥ 1 pp of IS MaxDD).
S2 = S1 restricted to arms passing the IS sign screen.

| selector | OOS CAGR | OOS Sharpe | OOS MaxDD | picks changed |
|---|---|---|---|---|
| S1 (idea 94, no screen) | 8.91% | 0.801 | −19.0% | — |
| S2 @ headline (0.10, 0.90) | 8.91% | 0.801 | −19.0% | **0 of 12** |
| S2 @ strictest (0.20, 1.00) | 8.41% | 0.768 | −16.7% | 2 of 12, **both worse** |
| cell control (no instrument) | — | 0.852 | — | — |
| live RULES v1 | — | 0.470 | — | — |
| SPY | 15.45% | 0.882 | −33.7% | — |

The two picks the strict screen changes are `broad/V1u` at 10 and 25 bps, where it replaces
`g200-rw` with `ebud-0.10` and loses **0.590 → 0.367** and **0.169 → 0.000** of OOS Sharpe.
And the screen has **no OOS discriminating power at all on these panels**: the OOS denominator
is positive in **138/138** rows, for IS-admissible and IS-rejected rows alike, at every one of
the 12 grid points. What the screen does do is retain the **dearer** half of the menu —
median full-sample rate 0.494 (admissible) vs 0.065 (rejected), median OOS rate 0.459 vs 0.283.

## 4. Both KEEP paths (PROTOCOL rule 4)

Across all 192 audited arm-points at 10 and 25 bps: **4a 54/192, 4b 29/192** (idea 94's arms,
reproduced). Of the 90 admissible published rows: 4a 38, 4b 26. The sign test moves **3** 4b
passes into "passes 4b but its price is not quotable" — `u56/TOP20/band3-rw` @10 and @25 bps
and `u56/TOP20/vol60-rw` @10, all three on D2. **No new KEEP.** The S1/S2 picks are below
their own no-instrument control in 7 of 12 cells and below SPY OOS Sharpe in 6 of 12 (mean
0.801 vs control 0.852 vs SPY 0.882): this run produces no capital-worthy book and does not
claim one.

## 5. Proposed PROTOCOL clause (report-only; for the Sunday review, nothing adopted here)

> *Denominator sign test.* No ratio may be quoted unless its denominator's sign survives a
> stated perturbation. For a drawdown price the denominator is
> `dMaxDD = |MaxDD_control| − |MaxDD_arm|`, and the stated perturbation is: positive at every
> cost rung in {0, 5, 10, 25} bps; positive in both halves of the sample; and positive in at
> least 90% of 40 draws that delete 10% of the panel's names at random with the signals
> recomputed on the sub-panel. A row that fails is reported as the pair `(dCAGR, dMaxDD)`
> with the axis it failed on, never as a rate. The test is a REPORTING bar and must not be
> used to select an instrument: on the two large-cap lists it changes 0 of 12 walk-forward
> picks at its stated setting and, when tightened until it binds, changes 2 and makes both
> worse out of sample.

Scope sentence that ships with it: **a price computed on a book of fewer than ~20 names, or in
a window whose benchmark MaxDD is shallower than about 25%, has no measurable denominator on
this data and should not be quoted at all** — that is where 100% of the D1/D3 failures and all
40 of the D2 failures live.

## 6. What moves elsewhere

- **Idea 22** (`ddctl` 1.02 vs lever 0.57): the u56/TOP20 `ddctl-8/.5/high` row (rate 0.994)
  is **admissible** on all three axes. The headline survives the sign test on that book.
- **Idea 74** (the insurance menu): quotable on `EWall` (47/48) and mostly on `TOP20`, **not
  on V1u** (16/41). The menu is a large-book statement.
- **Idea 94** (this list): 90 of 138 rows keep their rate; the memo's "the price of any one
  gate against another is not stable out of sample and must not be quoted" is unaffected and
  is if anything strengthened.
- **Idea 97 / 117**: the IS/OOS denominator asymmetry (40 vs 0 non-positive rows) is the same
  regime effect idea 97 found in the price LEVEL (4.108 IS vs 0.404 OOS), now visible in the
  sign. Idea 117's matched-crisis-depth pricing is the right repair; this run supports it.

## 7. Not claimed

Both universes are current-constituent lists (survivorship); every absolute level is
optimistic and a delisting-aware panel could move which rows pass. The calendar-day index bug
(idea 38) is unfixed. Bootstrap draws are uniform over all panel columns including SPY, idea
119's convention. 40 draws makes τ = 0.95 and τ = 1.00 coarse (≥38 and 40 of 40). The test
says nothing about whether a price is *useful* — only whether its denominator has a sign.
