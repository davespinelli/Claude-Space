# Idea 170 — is-0.75-the-argmax-on-every-corpus (cloud, 2026-09-05)

**VERDICT: KILL of the promotion.** `g = 0.75` cannot be written into PROTOCOL as a measured
constant. It reproduces as a *large-cap* peak — the OOS-4b pass-rate curve peaks at 0.75 on U56
(0.941, tied with 0.80) and at 0.70 on B136 (0.294) — but it has **no argmax at all on the small
panel** (0 books pass 4b at any of the ten gross points), and per-book the OOS argmax is spread
across **eight of the ten ladder points**, with only **30 of 51 books (60.8%)** landing inside
the claimed 0.70–0.80 band. No new book, no KEEP-candidate, no RULES change.

The run also produces the *mechanism*, which is the part worth keeping: on this construction the
three Sharpe bars are gross-invariant, so 4b's argmax in gross is nothing but the crossing of a
rising CAGR-floor margin and a falling DD-cap margin. 0.75 is where those two SPY-referenced
coefficients (0.70×CAGR, 0.60×MaxDD) cross **for a book with roughly SPY-like vol** — a property
of the bars and of the book's vol, not of any corpus.

## What was run

Idea 166's ladder, **imported from its committed script rather than retyped** (`LADDER`,
`rel_margins`, `bars_win`, `win`, and through it idea 78's `eligible_mask` / `weights_cand` /
`weights_ewall` / `half_sharpes` / `fail_4a` / `fail_4b`), on three panels:

| panel | names | eval window | SPY (full) | RULES v1 (full) |
|---|---|---|---|---|
| U56 (universe.json) | 56 | 2009-01-13 → 2026-09-04 | 15.23% / 0.889 / −33.7% | 6.45% / 0.664 / −13.8% |
| B136 (universe_broad.json) | 136 | 2009-01-13 → 2026-09-04 | 15.23% / 0.889 / −33.7% | 6.39% / 0.635 / −21.2% |
| SMALL (sub-$2B, filtered) | 439 | 2011-01-13 → 2026-09-04 | 14.13% / 0.862 / −33.7% | 7.08% / 0.550 / −36.7% |

51 books × 10 gross points = **510 engine runs**, 10 bps, weekly, t+1, no shorting, no leverage.
Books: per panel, RANKED n ∈ {5, 10, 20, 40} and EWALL on the whole panel, plus 12 fixed k = 40
sub-panel draws (seeded per panel) at RANKED n = 20. Two tuned parameters: the ladder point g
(10) and the ranked book size n (4). Panel, construction and draw are corpus axes.
SMALL drops the 44 of 483 tickers with `max_1d_move ≥ 1.0` in `data/small_meta.csv` first.

## 1. Where the OOS argmax sits

Per-book OOS-margin argmax, counts by ladder point:

| panel | 0.20 | 0.30 | 0.40 | 0.50 | 0.60 | 0.70 | 0.75 | 0.80 | 0.90 | 1.00 |
|---|---|---|---|---|---|---|---|---|---|---|
| U56 | 0 | 0 | 0 | 0 | 1 | 3 | **8** | 4 | 1 | 0 |
| B136 | 0 | 0 | 0 | 0 | 0 | 2 | 4 | **8** | 2 | 1 |
| SMALL | 3 | 1 | 1 | 0 | **4** | 1 | 0 | 1 | 3 | 3 |
| pooled | 3 | 1 | 1 | 0 | 5 | 6 | 12 | 13 | 6 | 4 |

Share of books whose OOS argmax lies in 0.70–0.80: **U56 15/17, B136 14/17, SMALL 1/17 → 30/51
(60.8%)**. On the sub-panel draws alone the median OOS argmax is 0.750 (U56), 0.800 (B136) and
0.600 (SMALL), with the 0.70–0.80 share at 1.00 / 0.75 / 0.00 respectively.

Idea 166's own statistic — the OOS-window 4b **pass rate** at each ladder point — reproduces in
shape on the large-cap panels and is degenerate on the small one:

| corpus | 0.20 | 0.50 | 0.60 | 0.70 | 0.75 | 0.80 | 0.90 | 1.00 | argmax | peak |
|---|---|---|---|---|---|---|---|---|---|---|
| U56 (17 books) | 0 | 0.059 | 0.294 | 0.824 | **0.941** | **0.941** | 0.529 | 0.235 | 0.75 (tie 0.80) | 0.941 |
| B136 (17) | 0 | 0 | 0.059 | **0.294** | 0.235 | 0.235 | 0.059 | 0 | 0.70 | 0.294 |
| SMALL (17) | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **none** | 0.000 |
| ALL (51) | 0 | 0.020 | 0.118 | 0.373 | **0.392** | **0.392** | 0.196 | 0.078 | 0.75 (tie 0.80) | 0.392 |

For reference, idea 166's B136 sub-panel corpus gave 0.110 at 0.75, 0.103 at 0.70, 0.027 at 1.00
on 300 books. The *level* is not comparable (different draws, different n), the *shape* is.

## 2. Why — the argmax is a property of 4b's own coefficients, not of a corpus

Mean spread of each 4b bar across the whole ladder (P1's test):

| panel | H1 | H2 | OOS-Sharpe | DD | CAGR |
|---|---|---|---|---|---|
| U56 | 0.0055 | 0.0058 | 0.0021 | 0.8609 | 1.3263 |
| B136 | 0.0099 | 0.0067 | 0.0056 | 0.9673 | 1.1203 |
| SMALL | 0.0060 | 0.0044 | 0.0046 | 1.3775 | 0.3290 |

**P1 held exactly.** The three Sharpe bars move by 0.002–0.010 across a 5× change in gross — the
return stream and the 10 bps cost drag scale together, so Sharpe is a gross-invariant of this
construction (idea 66's "gross is an exact lever with zero Sharpe content", re-confirmed on 51
books). Only the CAGR floor (rising in g) and the DD cap (falling in g) move. Which bar binds on
the OOS window, by ladder point (share of the 51 books):

| g | CAGR | DD | H1 | H2 |
|---|---|---|---|---|
| 0.20 | 0.824 | 0.000 | 0.000 | 0.176 |
| 0.50 | 0.667 | 0.000 | 0.078 | 0.255 |
| 0.70 | 0.431 | 0.137 | 0.118 | 0.314 |
| **0.75** | **0.314** | **0.275** | 0.118 | 0.294 |
| 0.80 | 0.137 | 0.431 | 0.118 | 0.314 |
| 1.00 | 0.000 | 0.745 | 0.039 | 0.216 |

The CAGR/DD hand-over happens **at 0.75–0.80**, which is exactly where the argmax sits whenever a
Sharpe bar is not already the binding one. That is the whole of idea 166's peak. On SMALL the
binding OOS bar at g = 0.75 is **H2 in 13 of 17 books** — a gross-invariant bar — so the margin
curve is flat or dominated by an unreachable Sharpe bar and its argmax is uninformative (4 of 12
sub-panel books are flat to 1e-3 across the entire ladder).

So the constant is not corpus-general; it is *bar*-general, conditional on the book's vol being
near SPY's. A book with half SPY's vol needs more gross to clear a 0.70×SPY CAGR floor and its
crossing moves right (U56 RANKED40 → 0.90, EWALL → 0.80); a book with far more vol never gets
there at all (SMALL).

## 3. Rule 8 walk-forward (g chosen on ≤ 2016-12-31, read once on 2017 →)

| panel | arm | mean g | OOS CAGR | OOS Sharpe | OOS MaxDD | OOS-4b passes | vs RULES v1 | vs SPY |
|---|---|---|---|---|---|---|---|---|
| U56 | STATIC 0.75 | 0.750 | 13.4% | **1.175** | −16.8% | **16/17** | +0.428 | +0.293 |
| U56 | ISMARG | 0.738 | 13.0% | 1.175 | −16.4% | 16/17 | +0.427 | +0.293 |
| U56 | ISSHARPE | 0.782 | 14.0% | 1.175 | −17.4% | 8/17 | +0.428 | +0.293 |
| B136 | STATIC 0.75 | 0.750 | 11.4% | 0.980 | −19.0% | 4/17 | +0.404 | +0.098 |
| B136 | ISMARG | 0.779 | 11.6% | 0.979 | −19.4% | 4/17 | +0.402 | +0.097 |
| B136 | ISSHARPE | 0.988 | 15.0% | 0.980 | −24.6% | 1/17 | +0.404 | +0.098 |
| SMALL | STATIC 0.75 | 0.750 | 3.3% | 0.283 | −27.7% | 0/17 | −0.178 | −0.599 |
| SMALL | ISMARG | 0.812 | 2.9% | 0.282 | −28.8% | 0/17 | −0.179 | −0.600 |
| SMALL | ISSHARPE | 0.953 | 3.6% | 0.282 | −33.4% | 0/17 | −0.179 | −0.600 |

Paired per book against the STATIC 0.75 control: **ISMARG mean −0.0009 OOS Sharpe (wins 8/51)**,
**ISSHARPE −0.0003 (wins 13/51)**. Neither IS-fitted chooser beats doing nothing — a fifth
independent instance after ideas 110, 151, 132 and 166, now on three fresh corpora. The choosers
do move the *4b verdict* (ISSHARPE drops U56 from 16 to 8 OOS passes by pushing gross to the cap
and breaking the DD bar), which is a drawdown effect, not a Sharpe effect.

## 4. Both KEEP paths, all 510 book-gross points

* **4a**: 205 of 510 pass (Sharpe > RULES v1 in both halves, MaxDD no worse). All are low-gross
  points of large-cap books whose CAGR floor then fails 4b — the live book is easy to beat on
  risk-adjusted terms and impossible to beat on return at 0.20–0.50 gross.
* **4b (full sample)**: 48 of 510, **0 of them on SMALL**. Every passer is an already-published
  book at a different gross (idea 144: a re-grossed book is the same book) — U56 RANKED20 at
  0.70/0.75/0.80 is the standing KEEP 4b candidate itself (12.7% / 1.092 / −18.3%, halves
  1.088/1.102, OOS 1.168 at g = 0.75), U56 RANKED40, U56 EWALL, B136 RANKED40 and B136 EWALL are
  ideas 10/72's books. **Nothing new is proposed.**
* The best single passing point in the run, B136 EWALL at 0.75 (10.7% / 1.026 / −17.7%, halves
  1.146/0.914, OOS 1.019), is idea 72's `B136/EWall` verbatim.

## 5. Predictions

| | prediction | outcome |
|---|---|---|
| P1 | Sharpe bars near gross-invariant; many books' argmax decided by the tie-break | **HELD** (spreads 0.002–0.010 vs 0.33–1.38) |
| P2 | where CAGR/DD bind, the argmax is an interior crossing that moves with the book's vol | **HELD** (0.60→1.00 across books within one panel) |
| P3 | 0.70–0.80 will *not* be the OOS argmax everywhere | **HELD** (60.8% of books; SMALL has no argmax at all) |
| P4 | no 4b KEEP on the small panel | **HELD** (0 of 170 small-panel book-gross points) |
| P5 | ISMARG/ISSHARPE do not beat STATIC on OOS Sharpe | **HELD** (−0.0009 / −0.0003 paired) |

5 of 5 held, which is itself a warning: the run confirms a mechanism it could have derived, and
its only surprise is the size of the small-panel failure.

## Caveats (carried, not buried)

* **Survivorship.** All three panels are current-constituent lists (idea 54); SMALL is the
  sub-$2B screen's *survivors* since 2010. Levels are biased upward — most sharply on SMALL,
  where the bias falls hardest on the beaten-down cohort the gate excludes (ideas 39/49). The
  ladder compares gross points *within* a panel, where the bias is common to every point, so the
  argmax results are less exposed than the pass rates are.
* The 200d/vol20 eligibility gate is **inverted** on the small panel (ideas 39/49): SMALL's books
  are known-broken, and their 0 pass rate is partly that, not only gross.
* SMALL starts 2011-01-13 after warm-up, so its halves and IS window are shorter than the
  large-cap panels'. Reported, not adjusted.
* Idea 38 (calendar-day price index) and idea 126 (t+1 execution only) carry over.
* The IS-window reading of `rel_margins` uses the window's own Sharpe as the OOS bar (idea 166's
  convention), kept identical so the two runs' ladders are comparable.
* 17 books per panel is a thin corpus for a pass-*rate* curve; the per-book argmax distribution
  (51 points) is the more robust of the two readings and is the one the verdict rests on.

## What PROTOCOL may and may not say

May: *"On large-cap panels the 4b-passing gross interval is 0.70–0.80 because that is where 4b's
CAGR floor and DD cap hand over; the Sharpe bars are gross-invariant, so no gross level can fix a
book that fails a Sharpe bar."*

May **not**: *"0.75 is the measured out-of-sample argmax."* It is not one on the small panel, and
it is the argmax for only 60.8% of books.

Script `research/backtests/2026-09-05_is-075-the-argmax-on-every-corpus_cloud.py`; console,
`.ladder.csv` (510 rows), `.argmax.csv` (51), `.corpus.csv`, `.walkforward.csv` (153) alongside.
