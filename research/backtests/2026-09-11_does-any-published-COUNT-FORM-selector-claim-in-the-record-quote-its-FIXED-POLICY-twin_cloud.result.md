# Idea 693 — does-any-published-COUNT-FORM-selector-claim-in-the-record-quote-its-FIXED-POLICY-twin (cloud, 2026-09-11)

**ANSWERED / ALMOST NONE DO, AND THE ONE TWIN THE RECORD *DOES* QUOTE IS THE WRONG ONE FOR
12 OF ITS 15 SITES. KILL for capital (4a 0/63 grid, 0/30 picks; 4b 4/30 picks, BELOW the
family's own 15/63 base rate). No KEEP, no memo, no RULES change.**

Idea 688 established that on a one-dial WIDTH ladder every count-form criterion is
pick-for-pick identical to "take the widest" (K-MAX agreement 1.000). This run re-reads the
record's own committed sites and prices the restatement. Two findings, both new:

1. **The record quotes a twin at 5 of 15 count-form sites (33.3%), and never at the four
   files where the criterion actually decides a published pick.** All 3 `width` sites and
   both `d_*_kextend` sites live in files that compute a K-MAX / widest / twin control —
   those are ideas 685/688's own generators, i.e. the record quotes the twin exactly where
   the twin *is* the subject. The other **10 sites (`IS_bought` ×6, `OOS_bought` ×2,
   `n_elig_IS` ×2) across 4 files quote nothing**.
2. **"Take the widest" is the correct twin for 1 of the 6 criteria.** On the record's real
   dial set (two dials: book width n, gate strictness) the count-form criteria split into
   two constant-policy families, and neither is K-MAX:

| criterion | its true fixed-policy twin | agreement | median ΔOOS Sharpe | 4b flips |
|---|---|---|---|---|
| `IS_bought`, `bought_pp`, `OOS_bought` | **CORNER** (widest n *and* loosest gate) | **1.000** (3/3 panels) | **0.0000** | **0** |
| `n_elig_IS`, `Ebar_IS` | **LOOSEST** (loosest gate; blind to n) | **1.000** (3/3 panels) | **0.0000** | **0** |
| `width` | K-MAX (widest n) | 1.000 | 0.0000 | 0 |
| `IS_Sharpe` (intensive reference) | best twin LOOSEST | 0.333 | +0.0005 | 0 |
| `RANDOM` (control, false-positive rate) | best twin any | 0.000 | — | — |

   Against the record's published twin (K-MAX) five of the six read agreement **0.000** —
   which would have been published as "the selector is informative". It is not; the twin was
   simply named on one dial of a two-dial grid.

**`n_elig_IS` / `Ebar_IS` are the strong form: they are blind to a whole dial.** Eligibility
does not depend on book width, so across the 7-rung n ladder the criterion is *exactly
constant* — every pick is a **7-way tie** resolved by the tie-break, not by the criterion.
Their agreement of 1.000 with LOOSEST is therefore partly an artefact of this run's declared
tie-break (smallest n, then strictest gate — declared before any number was read, and the
conservative direction here). The honest statement is not "they pick like LOOSEST" but
**"they carry zero information on one of the two dials they are published as selecting over."**

## Construction

**LEG A — census.** All 666 `research/backtests/*.py` parsed with `ast` (0 unparseable);
every `idxmax/idxmin/argmax/argmin/nlargest/nsmallest` site extracted with its criterion
token: **1,344 selection sites**. A fixed lexicon (printed before any count) classifies them
EXTENSIVE 15 (1.1%) / INTENSIVE 690 (51.3%) / MIXED 1 / **UNCLASSIFIED 638 (47.5%)**.

**LEG B — price.** CAND-n books through the record's RULES v1 gate, composite with **no vol
scaler** (the 2026-09-04 KEEP-4b construction, pinned by G7 at max|d| 1.777e-03), fixed
0.75/n per name so a thin book de-grosses to cash. Dials: n ∈ {5,10,15,20,30,40,50} ×
VOLCAP ∈ {0.40,0.60,0.90} = **21 books × 3 panels = 63, every point reported**. Two tuned
params: the **claim set** (the queue's 6 criteria) × the **twin definition** (K-MAX /
LOOSEST / CORNER) — all 3 × 6 × 3 panels reported. Fixed and not chosen by outcome: gross
0.75, weekly, **10 bps**, t+1, 260-row warm-up, IS ≤ 2016-12-31 / OOS ≥ 2017-01-01. A 0/25
bps table is printed as **labelled robustness** only (K-MAX agreement 0.250 at both rungs,
identical to 10 bps — the classification is cost-invariant).

## Gates (all PASS, printed before any new number was read)

G1 fast_backtest == engine.backtest 6.939e-18 · G2 band_book == rules_v2_weights 0.000e+00 ·
G3 SMALL dropped 44 tickers with max_1d_move ≥ 1.0 → 440 cols · G4 extensivity identity
`IS_bought == bought_pp × IS periods` 1.819e-12 · G5 causality, `w(px[:d])` an exact prefix
of `w(px)` 0.000e+00 · G6 IS statistics recomputed on a frame **truncated at IS_END**
reproduce 0.000e+00 · G7 the n=20/vc=0.60 cell reproduces the standing 2026-09-04 KEEP-4b
incumbent 12.63%/1.0903/−18.31% vs published 12.66%/1.0921/−18.31%.

## The capital leg (PROTOCOL 4 + 8) — this is a KILL

Rule 8: each selector picks one cell on IS only; 2017–2026 read once. 30 non-peeking picks
(`OOS_bought` is run but **labelled PEEKING and excluded from every verdict**).

* **4a: 0/63 grid points, 0/30 picks.** Nothing in this family beats the live book in both
  halves at no worse drawdown.
* **4b: 15/63 grid points (23.8%), but only 4/30 picks (13.3%)** — selection lands *below*
  its own family base rate. All 4 are the same B136 cell (n=50, vc=0.90).
* **1 of 30 picks beats RULES v2 OOS Sharpe** (SMALL, IS_Sharpe 0.5907 vs 0.5680) and
  15/30 beat SPY OOS Sharpe (0.8721–0.8820).
* On U56 the **RANDOM control** landed on the incumbent cell (n=20/vc=0.60, OOS Sharpe
  1.1648, 4b PASS) while every count-form selector missed it. With a 23.8% family pass rate
  that is unremarkable — and it is the cleanest statement of the result: **on this grid a
  count-form criterion is not a selector, and a coin flip is not worse than one.**

## Restatement of the queue's own numbers

The queue quotes **18 count-form sites across 6 criteria**; this census finds **15 across 6
criteria in 6 files**, scoring only `.py` files under `research/backtests/` with an AST token
extractor. The 6 criteria match. The 15-vs-18 gap is a **classifier difference, not a
contradiction** — it is not evidence that idea 688 is wrong, and no claim here rests on it.

## Caveats

* **47.5% of the record's selection sites (638 of 1,344) are UNCLASSIFIED by this lexicon** —
  the same blind spot open idea 695 names. Every rate above is over the adjudicated 706.
* Census scope is `research/backtests/*.py` only; selector claims made in markdown prose or
  in `research/*.py` helpers are not counted.
* **SURVIVORSHIP (PROTOCOL 9):** B136 is today's constituents and SMALL is the current
  sub-$2B screen only (data/SMALL_PANEL_README.md) — names acquired, delisted or grown out of
  the screen are absent, so every LEVEL on those panels is biased upward and none is a
  tradeable estimate. U56 carries the same bias in milder form. The headline quantities here
  are agreement rates and within-panel pick differences, to which the bias applies on both
  sides of every comparison.
