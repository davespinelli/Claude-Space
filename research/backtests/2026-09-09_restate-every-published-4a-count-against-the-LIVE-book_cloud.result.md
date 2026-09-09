# Idea 482 — restate every published 4a count against the LIVE book (RULES v2)

**Script:** `research/backtests/2026-09-09_restate-every-published-4a-count-against-the-LIVE-book_cloud.py`
**Verdict: ANSWERED / REFUTED.** 94.1% of the record's published 4a passes are artefacts of the
superseded RULES v1 comparand. **57,165 published 4a passes → 3,353 survive the live book.**
Two tuned parameters, as the queue allows: **baseline version** ∈ {v1, v2} and **panel** ∈
{u56, broad136, small439}. All grid points reported.

## (0) The baselines, recomputed from scratch (weekly, next-day, `compare()` convention)

| panel | book | 10 bps CAGR / Sharpe / MaxDD | H1 / H2 | OOS 2017– CAGR / Sharpe / MaxDD |
|---|---|---|---|---|
| u56 | **v2 (live)** | 8.64% / **1.2037** / −12.05% | 1.2309 / 1.1828 | 9.51% / **1.2817** / −12.05% |
| u56 | v1 (superseded) | 6.42% / 0.6611 / −13.83% | 0.6429 / 0.6804 | 7.66% / 0.7408 / −13.83% |
| u56 | SPY | 15.19% / 0.8871 / −33.72% | 0.9587 / 0.8287 | 15.38% / 0.8786 / −33.72% |
| broad136 | **v2 (live)** | 8.03% / **1.1058** / −12.24% | 1.2291 / 0.9844 | 7.98% / **1.1185** / −12.24% |
| broad136 | v1 | 6.39% / 0.6350 / −21.19% | 0.7562 / 0.5320 | 5.94% / 0.5763 / −21.19% |
| broad136 | SPY | 15.23% / 0.8890 / −33.72% | 0.9566 / 0.8340 | 15.45% / 0.8820 / −33.72% |
| small439 | **v2 (live)** | 3.81% / **0.5725** / −14.68% | 0.5699 / 0.5770 | 3.85% / 0.5680 / −14.68% |
| small439 | v1 | 7.41% / 0.5647 / −36.12% | 0.7434 / 0.4044 | 6.35% / 0.4923 / −36.12% |
| small439 | SPY | 14.13% / 0.8615 / −33.72% | 0.8907 / 0.8577 | 15.45% / 0.8820 / −33.72% |

These reproduce the record: u56 v2 matches RULES.md's acceptance table (8.66%/1.2056/−12.05%,
1.2259/1.1908, OOS 1.2851) to rounding, and broad136 v1/v2 match idea 252's quoted
6.39%/0.635/−21.19% and 8.03%/1.106/−12.24% exactly. Nothing here is new — it is the bar.

## (1) Reproduction control (the honesty gate)

Harvested **240** committed grid CSVs carrying `H1`, `H2`, `MaxDD`, a published 4a column and a
mappable panel label — **208,030 rows**. Before restating anything, the recomputed **4a-vs-v1**
must reproduce the file's own published 4a column:

| agreement | exact | [0.95,1) | [0.80,0.95) | [0.50,0.80) | <0.50 |
|---|---|---|---|---|---|
| files | 53 | 49 | 38 | 65 | 35 |

**102 of 240 files reproduce at ≥95%** (median over all 240: 0.913). The other 138 used a different
window, cost rung or half-split than `compare()`; they are **excluded outright** rather than
restated on a mismatched bar. Everything below is the trusted subset: **137,642 rows, 102 files**.
Rows priced at cost rungs other than 10/25 bps are dropped for the same reason.

## (2) The restatement — ALL grid points

| panel | rows | published 4a | recomputed 4a-v1 | **4a-v2 (live)** | survive | survive rate |
|---|---|---|---|---|---|---|
| broad136 | 51,641 | 33,028 | 33,030 | **1,167** | 1,167 | **3.5%** |
| small439 | 30,011 | 9,795 | 10,491 | **2,236** | 2,140 | **21.8%** |
| u56 | 55,990 | 14,342 | 14,324 | **46** | 46 | **0.3%** |
| **ALL** | **137,642** | **57,165** | 57,845 | **3,449** | **3,353** | **5.9%** |

Idea 252's 178/300 → 3/300 on one corpus was not a local accident. It is the record-wide rate.

**Which bar kills them** (census over the 53,812 published passes that die):

| panel | lost | fails H1 | fails H2 | fails DD |
|---|---|---|---|---|
| broad136 | 31,861 | 27,687 | 27,250 | 25,627 |
| small439 | 7,655 | 993 | 2,884 | **6,577** |
| u56 | 14,296 | 12,499 | 12,880 | 4,663 |
| **ALL** | **53,812** | **41,179** | **43,014** | **36,867** |

On the two large-cap panels both Sharpe halves are what cut (v2 roughly doubles v1's Sharpe there).
On small439 the **drawdown cap** is what cuts (86% of losses): v1 drew −36.12% on that panel, so
almost anything cleared its DD bar; v2 draws −14.68%. small439 is also the only panel where v2 is
*not* obviously the better book — Sharpe 0.5725 vs 0.5647, i.e. v2 buys a 21pp shallower drawdown
for no Sharpe — which is exactly why 21.8% of its published passes survive.

**Cost rung — why the old bar was so easy to clear:**

| cost | rows | published 4a | pass rate | 4a-v2 | rate |
|---|---|---|---|---|---|
| 10 bps | 74,016 | 24,614 | 33.3% | 1,617 | 2.2% |
| 25 bps | 63,626 | 32,551 | **51.2%** | 1,832 | 2.9% |

The published pass rate *rises* with costs, because v1 is a turnover-heavy top-5 book that decays
−0.33 to −0.42 Sharpe from 10 to 25 bps while v2 decays −0.04 to −0.06. Under v1, "beat the book at
25 bps" was close to a free pass. Under v2 the bar barely moves with the cost rung.

## (3) Do any 4a-based verdicts flip?

| | files |
|---|---|
| files with ≥1 published 4a pass | 102 |
| **files where every published 4a pass dies against the live book** | **76** |
| files retaining ≥1 4a pass against the live book | 26 |

Largest counts that go to zero: `is-the-null-key-result-one-draw-or-a-distribution` (2,604→0),
`scale-free-as-a-corpus-eligibility-rule_C.grid.u56` (1,797→0), `absorbing-state-audit_B.ddctl`
(432→0), the three copies of the `does-a-random-screen-de-concentrate` corpus (302→0 each),
`which-4b-bar-binds` (208→0), `is-075-the-argmax-on-every-corpus` (205→0),
`does-every-regime-conditional-dial-lose-its-own-regime` (204→0), `drawdown-control_C.grid`
(176→0). Full list in `.perfile.csv`.

The 26 survivors are concentrated in the gross/leverage family (`no-leverage-ceiling-is-load-bearing`,
the four `gross-interval` / `is-the-ladder-even-a-candidate` / `pin-m-or-let-the-screen-choose`
copies — 353/7,650 each), `scale-free-as-a-corpus-eligibility-rule` on broad (217/4,800) and
`ew-band3-at-085-does-not-hold-on-broad` (193/2,904 — a v2-family book, so unsurprising). Note
`the-IS-chosen-substitute-arm-for-every-named-asset-set` falls **10,743 → 1**.

## (4) Rule 8 — walk-forward. Is "passes 4a vs the live book" a better SELECTOR?

The restatement is a filter over each committed menu. On every menu publishing an IS column and OOS
columns (**232 menus over 91 files**), pick the max-**IS_Sharpe** arm inside (a) the whole menu,
(b) the 4a-v1 survivors, (c) the 4a-v2 survivors — choice made on the first half only — and read the
untouched OOS leg:

| panel | menus | all: OOS Sh / CAGR / DD | 4a-v1: OOS Sh / CAGR / DD | **4a-v2: OOS Sh / CAGR / DD** |
|---|---|---|---|---|
| broad136 | 89 | 1.0338 / 13.08% / −20.26% | 1.0434 / 11.06% / −17.49% | **1.1582 / 6.22% / −9.65%** (n=20) |
| small439 | 53 | 0.5370 / 6.87% / −30.48% | 0.5727 / 8.16% / −29.88% | **0.6338 / 3.55% / −12.76%** (n=11) |
| u56 | 90 | 1.1229 / 15.43% / −20.65% | 1.1787 / 9.75% / −12.70% | **1.2892 / 10.33% / −11.47%** (n=7) |
| **ALL** | **232** | 0.9549 / 12.57% / −22.75% | 0.9895 / 9.95% / −18.47% | **1.0305 / 6.20% / −10.89%** |

Paired, on the 38 menus where both filters still leave a pick:
- 4a-v2 vs 4a-v1: **+0.0164 mean OOS Sharpe, t +1.52, 19/38 wins — not significant.**
- 4a-v2 vs the unfiltered menu: **+0.0512 mean OOS Sharpe, t +2.66, 21/38 wins — significant.**

So the live-book filter *does* pick better risk-adjusted books out of sample than picking freely —
but it is a **Sharpe filter that destroys CAGR**: OOS CAGR falls 12.57% → 6.20% and OOS drawdown
halves. That is PROTOCOL 4's own warning, measured: 4a judged against a low-return live book kills
growth. On 194 of 232 menus the 4a-v2 filter leaves **no arm at all**.

Against the references: the ALL-panel 4a-v2 pick averages OOS Sharpe 1.0305 vs the live v2 baseline's
own OOS 1.2817 (u56) / 1.1185 (broad136) / 0.5680 (small439) and SPY's 0.8786. It beats SPY on Sharpe
and loses to it on CAGR (6.20% vs 15.38%), i.e. the selector does not produce a 4b book.

## (5) Both KEEP paths

**No new book is introduced** — idea 482 restates the committed record, so there is nothing to
promote and no memo. Reported as counts:

- **4a against the live RULES v2: 3,449 / 137,642** committed grid points (2.5%).
- 4a against the superseded v1: 57,845 / 137,642 (42.0%).
- **4b is not restated.** 4b is judged against SPY, which did not change on 2026-09-06, so no
  published 4b count moves. Ideas 481/253 own the 4b re-scoring.

## (6) Answer to the queue, in its own words

> *"report how many published 4a passes survive the live baseline, and whether any 4a-based verdict
> in the record flips."*

**3,353 of 57,165 survive (5.9%), and 76 of the 102 reproducible files lose their 4a support
entirely.** Any sentence in the record of the form "N of M arms clear 4a", written before
2026-09-06, should be read as "clear the *superseded* 4a"; the live-book number is ~6% of it, and on
u56 it is 0.3%. The record's 4a counts were never wrong — they were measured against a book that is
no longer live.

## Caveats
- **SURVIVORSHIP:** broad136 and small439 are current-constituent screens (PROTOCOL 9,
  `data/SMALL_PANEL_README.md`). small439 = the 483-name sub-$2B panel with the 44 tickers whose
  `max_1d_move ≥ 1.0` dropped. Absolute levels are optimistic; the v1-vs-v2 margin is a same-names,
  same-days difference and is much less exposed.
- **138 of 240 harvested files could not be reproduced** and are excluded. They are not counted as
  surviving or as dying — they are unrestated. A file whose harness used a different warm-up or
  half-split may carry 4a counts that this census cannot speak to.
- Rows are grid points, not independent books: several files are near-duplicates of each other (the
  four `gross-interval`/`ladder` copies), so the row counts are weighted toward large sweeps.
- The restatement assumes each row's H1/H2/MaxDD were computed on the same window as `compare()`.
  The ≥95% reproduction gate is what enforces that; it is a necessary, not a sufficient, check.
