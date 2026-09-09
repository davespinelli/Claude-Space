# Idea 588 — how many published dial STEPS in the record are NO-OPS?  (cloud, 2026-09-09)

**Verdict: ANSWERED / KILL as a record-wide problem — no promotion, no RULES change.**
No-op steps are real, but they are RARE (1.1–1.4% of the record's published count-dial steps),
entirely PREDICTABLE from a single panel statistic, and confined to the smallest panel. The one
place they still bite is pass-COUNTING.

## Gates (all asserted before any result was read — all PASS)
| gate | what | result |
|---|---|---|
| G1 | numpy replica vs `engine.backtest` (returns, turnover) | max\|dret\| **1.388e-17**, max\|dturn\| **0.000e+00** |
| G2 | idea 320's committed `grid.csv`, 5 ABS points x 6 columns x 3 panels | worst \|d\| U56 **2.22e-16**, B136 **1.11e-16**, SMALL439 **9.71e-17** |
| G3 | idea 320's committed `saturation.csv` max\|dW\|, 12 steps | worst \|d\| **7.286e-17** |
| G4 | idea 320's "the panel saturates at 37.5 eligible names" | U56 k_mean at n0=E_t **37.4999** |

**Convention found while building G4 (worth the record's attention):** idea 320 reports every
E_t/k statistic on the POST-WARM-UP window `px.index[260:]`, not on the full index. U56's
eligible-name mean is **37.50** on that window and **37.05** on the full one — a 0.45-name gap
that is pure convention. Both are right; only the first reproduces the record. Everything below
is on idea 320's window.

## Part A — the record-wide census (published numbers, 2,631 committed CSVs)
128 (file, dial-column) pairs carry an integer count dial AND a performance column; 18,473
reporting groups; **29,838 adjacent published steps**.

- **BIT-IDENTICAL on every shared performance column: 409 (1.371%).**
- NEAR-identical (all |d| < 1e-9, not exact): **0 (0.000%)** — the record has no near-misses at
  all, so a no-op is a clean binary, never a rounding artefact.
- On the subset whose dial is unambiguously a **book width** (`n`, `n0`, `width`):
  **304 / 27,023 = 1.125%**. (`k`/`K`/`N` are sometimes a draw size or a fold count, not a book
  dial: `K` 59/78, `N` 42/42, `k` 4/2,695 — reported, not claimed.)
- Only **15** (file, dial) pairs contain any identical step; the top file alone
  (`2026-09-06_audit-gross-normalisation-across-the-book_cloud.grid.csv`) holds 192 of the 409.

## Part B — re-derivation to machine precision (3 panels x 3 gates x 9 dial points = 81 books)
**THE CLOSED FORM, pre-registered and confirmed 108/108 (100%):** with k = min(n0, E_t) a step
n0_a -> n0_b is an exact no-op **iff n0_a >= max_t E_t**, the panel-gate CEILING. Every step
flagged identical has max|dW| = 0 and max|dr| = **0.000e+00**.

| panel | gate | names | E mean | E max = ceiling | ceiling / names |
|---|---|---|---|---|---|
| U56 | NONE / MA / MA+VOL | 56 | 53.85 / 38.45 / 37.50 | **56 / 55 / 55** | 1.000 / 0.982 / 0.982 |
| B136 | NONE / MA / MA+VOL | 136 | 130.83 / 93.21 / 91.46 | **135 / 128 / 128** | 0.993 / 0.941 / 0.941 |
| SMALL439 | NONE / MA / MA+VOL | 439 | 338.05 / 172.37 / 141.23 | **439 / 345 / 281** | 1.000 / 0.786 / 0.640 |

No-op rate: **9/72 (12.5%)** on this script's 9-point grid, **3/36 (8.3%)** on idea 320's own
published 5-point grid — and **every one of them is on U56**, one per gate, exactly the 1-of-4
idea 320 reported. B136 and SMALL439 contribute **0/24 and 0/24**. The gate barely matters
(U56 no-ops 3/3/3 across NONE/MA/MA+VOL): the binding fact is the PANEL's name count, not the
eligibility clause bolted on top of it.

**Partial no-ops are the bigger, quieter effect.** The share of DAYS on which an adjacent step
changes no weight at all runs to 0.478 (U56 MA+VOL, 40->60), 0.528 (B136 MA+VOL, 100->E_t) and
0.200 (SMALL439 MA+VOL, 100->E_t) — a dial can be half dead without producing a single
identical row.

## KEEP paths at all 81 grid points
**4a 0/81, 4b 14/81, BOTH 0/81.** Binding legs across the failures: DD 61, H2 33, OOS 31,
H1 27, CAGR 22.

**The one place no-ops still bite:** **4 of the 14 4b passers are the same book** — U56/MA at
n0 = 60, 80, 100 and E_t are bit-identical (CAGR 11.53%, Sharpe 1.0913, MaxDD -18.65%, OOS
Sharpe 1.1132). The honest count is **11 distinct 4b passers, not 14**; a pass rate quoted off
a grid whose top end sits above the panel ceiling is inflated by the ceiling, not by the rule.

## Rule 8 (PROTOCOL 8): n0 chosen on IS <= 2016-12-31 by IS Sharpe, 2017- read once
| panel | gate | pick | tie-set | OOS CAGR / Sharpe / MaxDD | RULES v2 OOS | SPY OOS | 4b |
|---|---|---|---|---|---|---|---|
| U56 | NONE | n0=5 | 1 | 23.22% / 1.048 / -28.45% | 9.53% / 1.285 / -12.05% | 15.45% / 0.882 / -33.72% | fail DD |
| U56 | MA | n0=5 | 1 | 23.22% / 1.048 / -28.45% | " | " | fail DD |
| U56 | MA+VOL | n0=20 | 1 | 14.49% / 1.137 / -18.31% | " | " | **pass** |
| B136 | NONE | n0=10 | 1 | 15.87% / 0.839 / -26.01% | 7.98% / 1.119 / -12.24% | " | fail H2,OOS,DD |
| B136 | MA | n0=10 | 1 | 15.87% / 0.839 / -26.01% | " | " | fail H2,OOS,DD |
| B136 | MA+VOL | n0=10 | 1 | 12.61% / 0.776 / -21.44% | " | " | fail H2,OOS,DD |
| SMALL439 | NONE | n0=E_t | 1 | 10.13% / 0.639 / -37.09% | 3.85% / 0.568 / -14.68% | " | fail H1,H2,OOS,DD |
| SMALL439 | MA | n0=30 | 1 | 11.58% / 0.635 / -30.09% | " | " | fail H2,OOS,DD |
| SMALL439 | MA+VOL | n0=20 | 1 | 6.92% / 0.464 / -33.48% | " | " | fail all five |

**0 of 9 picks has a tie-set larger than 1** — every IS argmax lands at a small n0, below the
ceiling, where the books genuinely differ. So the no-op problem never reached the chooser, and
the sort-order worry this idea was raised on does NOT materialise in the rule-8 layer.

## Why this is not a promotion
The only rule-8 pick that clears 4b (U56/MA+VOL n0=20) is idea 320's already-published PARK row,
re-derived to 2.2e-16 — not a new book. The 14 4b passers include four copies of one book and
are, on U56/MA+VOL, exactly the rows idea 320 declined to promote. `RULES.md`, `scan.py`,
`bot.py`, `baseline.py` and `PROTOCOL.md` untouched.

## Survivorship
B136 and SMALL439 are CURRENT-constituent lists; the names that died are absent, so every
realised E_t is a survivor's count and each published ceiling UNDERSTATES what a real historical
panel would have offered. A survivorship-free panel would have a HIGHER ceiling and therefore a
LOWER no-op rate — the bias runs against this finding, not for it. SMALL439 = the 483-name
sub-$2B panel with the 44 tickers whose `max_1d_move >= 1.0` dropped.

## What the record should do with this
Not a PROTOCOL amendment. A one-line reporting habit is enough and is free: **any grid whose
dial is an absolute count should publish `max_t E_t` beside it**, because that single number
predicts every no-op step in advance (108/108 here) and tells a reader which of the published
points are the same book.
