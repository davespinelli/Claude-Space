# Idea 269C — is-the-reversal-share-a-function-of-n-over-n_elig (lane C, 2026-09-06)

**Verdict: ANSWERED — KILL of the queue's premise. Reversal share is NOT a monotone
function of `n / n_elig`, and the width does not replace a re-run: at MATCHED ratio the
five panels disagree 0.00 vs 1.00 in 6 of 7 rows. What survives is one-sided and much
weaker than the premise — a pre-registered `r >= 0.55` screen classifies OOS reversals at
0.743 against a 0.543 base rate. No new KEEP-candidate, no book promoted, no RULES change.**

Script: `research/backtests/2026-09-06_is-the-reversal-share-a-function-of-n-over-n_elig_C.py`
Outputs: `.grid.csv` (70 points), `.reversal.csv` / `.reversal_0bps.csv` (35 cells each),
`.census_backfill.csv.gz` (35,875 pairs), `.points.csv`, `.elig.csv`, `.walkforward.csv`,
`.threshold_grid.csv`, `.rivals.csv`, `.selectors.csv`, `.console.txt`.
10 bps headline, weekly, next-day execution, gross 0.75; 0 bps carried as a diagnostic only.

**Reproduction gate, 2/2 exact, before any new number was read** (idea 259's construction
imported verbatim): `B136/EWall` here **10.7% / 1.026 / −17.7%, OOS 1.019** vs idea 259's
published 10.7% / 1.026 / −17.7%, OOS 1.019; `U56/EWall` here **10.4% / 1.049 / −15.9%,
4b fails on `CAGR` alone** vs idea 259's identical wording.

---

## Panel widths (median eligible names on weekly rebalance days, canonical gate)

| panel | cols | n_elig | IS | OOS | p10 – p90 |
|---|---|---|---|---|---|
| U56 | 56 | 41 | 39 | 42 | 18 – 48 |
| B136 | 136 | 99 | 99.5 | 98 | 48 – 116 |
| BSTK100 | 100 | 72 | 73 | 71 | 38 – 86 |
| SMALL439 | 439 | 148 | 137.5 | 153 | 70 – 194 |
| ETF36 | 36 | 27 | 26 | 27 | 11 – 32 |

## Leg A — the census, and why it cannot answer the question

Idea 259's committed census read verbatim: 37,044 RANKED pairs, `n` parsed strictly from the
comparand label on 97.6%, panel mapped on 99.3%, **both on 35,875 (96.8%) over 84 files**.
Dropped labels are listed in the console (bare `FWD`/`CAND`/`RANKED`/`REV`, `frac085`, band
arms — never guessed).

**The census's answer is a weighting choice, not a fact:**

| weighting | Spearman(reversal, r) | t | n |
|---|---|---|---|
| pair-level (all 35,875) | **+0.351** | +70.98 | 35,875 |
| point-level (30 distinct (panel, n) widths) | **−0.342** | −1.93 | 30 |
| file-clustered (one r, one share per file) | **+0.590** | +6.62 | 84 |

The sign flips with the weighting because the census has almost no within-file width
variation and only six distinct `n` values (5 and 20 are 88% of all pairs): r moves mostly
BETWEEN panels, so "r" and "panel" are the same regressor there. Within panel the sign is
not even stable: B136 **+0.429**, BSTK100 +0.520, U56 +0.429, SMALL439 +0.165, ETF36
**−0.455**. The census is therefore reported and set aside; the matched-ratio grid decides.

## Leg B — matched-ratio grid (the design the census could not supply)

`n = round(r* · n_elig)` per panel, so all five panels are read at the same seven ratios.
35 EWall-vs-FWD cells at 10 bps (and 35 at 0 bps), every one in `.reversal.csv`.

| r* | cells | reversal share 10 bps | 0 bps | mean dSharpe | mean dCAGR | sat_share |
|---|---|---|---|---|---|---|
| 0.05 | 5 | 0.60 | 0.80 | +0.1375 | −0.0488 | 0.004 |
| 0.10 | 5 | 0.60 | 0.60 | +0.0995 | −0.0351 | 0.009 |
| 0.20 | 5 | **0.80** | 0.80 | +0.0615 | −0.0215 | 0.024 |
| 0.35 | 5 | **0.80** | 0.60 | +0.0215 | −0.0152 | 0.066 |
| 0.50 | 5 | 0.40 | 0.40 | −0.0116 | −0.0131 | 0.118 |
| 0.75 | 5 | 0.40 | 0.40 | −0.0096 | −0.0063 | 0.221 |
| 1.00 | 5 | **0.00** | 0.00 | −0.0033 | −0.0017 | 0.517 |

**Not monotone**: the share RISES from 0.60 at r = 0.05 to 0.80 at r = 0.20–0.35 before
falling. Pooled Spearman is −0.386 (t −2.40) over 35 cells — but r = 1 is the IDENTITY
cell, where FWD-n holds every eligible name and *is* EWall, so it cannot reverse by
construction. **Dropping it, the trend is −0.181, t −0.97 (0 bps: −0.299, t −1.66) — not
distinguishable from no trend.** The one clean statement about r is the trivial one.

**And the ratio is not the variable.** At matched r the panels do not agree (1 = reverses):

| r* | B136 | BSTK100 | ETF36 | SMALL439 | U56 |
|---|---|---|---|---|---|
| 0.05 | 1 | 1 | 0 | 0 | 1 |
| 0.10 | 1 | 1 | 0 | 0 | 1 |
| 0.20 | 1 | 1 | 1 | 0 | 1 |
| 0.35 | 1 | 1 | 1 | 0 | 1 |
| 0.50 | 1 | 1 | 0 | 0 | 0 |
| 0.75 | 1 | 1 | 0 | 0 | 0 |
| 1.00 | 0 | 0 | 0 | 0 | 0 |

Panel shares: B136 6/7, BSTK100 6/7, U56 4/7, ETF36 2/7, **SMALL439 0/7 at every ratio and
both cost rungs**. Six of the seven rows span the full 0–1 range. A number that is 0 and 1
at the same value of the proposed predictor is not a function of it.

Leg C, same 35 cells: Spearman(rev, r) −0.386 (t −2.40), (rev, n) −0.317 (t −1.92),
(rev, n_elig) −0.081 (t −0.47). The ratio beats raw width only marginally, and neither
beats the panel identity.

## Rule 8 (i) — the RELATIONSHIP out of sample

Reversal recomputed from IS-window (2009–2016) metrics; the threshold is chosen on IS
accuracy alone; the OOS window (2017+) is read once. All 20 threshold grid points are in
`.threshold_grid.csv` and the console.

- IS-fitted **r\* = 0.55** (IS accuracy 0.657) → **OOS accuracy 0.743 vs a 0.543
  majority-class base rate.** IS reversal share 0.486, OOS 0.457, cells agreeing 0.743.
- Rivals, all fitted IS and read once OOS: CONST 0.514 IS / **0.543** OOS; R_THRESH 0.657 /
  **0.743**; PANEL (per-panel IS majority) **0.686 IS** / 0.657 OOS.

So the width rule does carry OOS classification content and it beats the panel rule out of
sample even though the panel rule fits better in sample — but it is a one-sided screen
(`r >= 0.55` → probably safe: 8 of 10 such cells do not reverse, and 5 of those 10 are the
identity cell), not the monotone law the queue proposed, and it misclassifies all five
low-r SMALL439 cells.

## Rule 8 (ii) — the BOOK: does the width rule change what you would run?

IS 2009-01-01..2016-12-31 chooses; OOS 2017+ read once; pooled equal-weight over the five
panels, 10 bps.

| selector | picks | OOS CAGR | OOS Sharpe | OOS MaxDD |
|---|---|---|---|---|
| EWALL (do nothing) | EWall ×5 | 8.61% | 0.8574 | −20.6% |
| FWD20 (incumbent) | FWD20/25/20/15/20 | 11.12% | **0.9031** | −21.4% |
| S_SHARPE (argmax IS Sharpe) | FWD10, FWD14, FWD27, FWD15, FWD4 | 12.43% | 0.8887 | −21.6% |
| S_CAGR (argmax IS CAGR) | FWD5, FWD4, FWD1, FWD15, FWD2 | **13.99%** | 0.7973 | −23.0% |
| **RSEL** (narrowest n with r ≥ 0.55) | FWD74, FWD54, FWD20, FWD111, FWD31 | 9.64% | 0.8966 | −21.4% |
| RULES v1 | v1 ×5 | 6.43% | 0.6908 | −17.3% |
| SPY OOS | — | 15.45% | 0.8820 | −33.7% |

The width rule is a real decision — it picks a different book on 5 of 5 panels — but it
buys nothing: **RSEL 0.8966 sits below the incumbent FWD20's 0.9031 while giving up 1.48
pp/yr of CAGR**, and everything loses to SPY on CAGR. S_CAGR beating S_SHARPE by +6.0 pp/yr
of OOS CAGR for −0.091 of Sharpe reproduces idea 259's sign on a fifth panel.

## KEEP paths (all 70 leg-B points reported)

- **10 bps: 4a 6/40, 4b 8/40.** Passers: `U56/FWD14` (13.3%/1.021/−19.0%), `U56/FWD20`
  (12.8%/1.064/−18.3%), `U56/FWD31` (11.6%/1.069/−17.4%), `B136/EWall`
  (10.7%/1.026/−17.7%), `B136/FWD35`, `B136/FWD50`, `B136/FWD74`, `B136/FWD99`.
- 0 bps: 4a 3/40, 4b 12/40. Failing-bar census in the console for both rungs.
- **Nothing new.** `U56/FWD20` is idea 2's `CAND-n20`, `B136/EWall` is idea 10's row, and
  the rest are interior points of the same two ladders idea 259 already published
  (`U56/FWD30`, `B136/FWD40`, `B136/FWD60`). `SMALL439` and `ETF36` are 0 of 16 at both
  rungs — a further reproduction of idea 136.

## Survivorship

`universe_broad.json`, the megacap cut and the small panel are current constituents. The
un-ranked book holds everything and inherits the full survivorship premium while a
selection rule can only redistribute it, so the bias runs TOWARD more reversals at low r —
i.e. toward the queue's hypothesis, which still fails.

## What the record should carry instead

> The Sharpe/CAGR reversal is **not** recoverable from `n / n_elig`. It is a property of the
> PANEL: on the five panels tested it runs 6/7, 6/7, 4/7, 2/7 and 0/7 of matched-ratio cells,
> and the same ratio gives 0 and 1 on different panels in 6 of 7 rows. Only two width facts
> are safe: at `r = 1` the ranked book IS the un-ranked one and cannot reverse, and
> `r >= 0.55` is a one-sided screen worth 0.743 OOS accuracy against a 0.543 base rate.
> Idea 259's recommendation stands unchanged — publish CAGR beside Sharpe; do not replace it
> with a width column.

`RULES.md`, `scan.py`, `bot.py` and `baseline.py` untouched.

## Queued follow-ups

- **271** — the reversal is a panel property: fit it on panel characteristics (breadth,
  cross-sectional dispersion, mean pairwise correlation of the eligible set) rather than on
  the book's width, since SMALL439 never reverses and B136 almost always does.
- **272** — `sat_share` reaches 0.52 at r = 1 while n_elig moves 18 → 48 across the sample:
  re-run the matched-ratio grid with a TIME-VARYING n (n_t = r·n_elig,t) so r is held fixed
  day by day rather than at the median only.
