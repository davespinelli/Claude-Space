# Idea 259 — does-the-sharpe-cagr-reversal-sit-under-every-EWall-claim (lane C, 2026-09-06)

**Verdict: ANSWERED. The reversal is GENERAL, not an idea-82 quirk — 47.5% of the record's
published "EWall beats the ranked book on Sharpe" cells LOSE on CAGR. KILL of Sharpe-only
reporting for un-ranked-vs-ranked comparisons; a CAGR column is proposed as a required
reporting habit, not a RULES change. No new KEEP-candidate, no book promoted.**

Script: `research/backtests/2026-09-06_does-the-sharpe-cagr-reversal-sit-under-every-EWall-claim_C.py`
Outputs: `.census.csv.gz` (44,358 pairs), `.grid.csv` (64 points), `.paired.csv`, `.predictor.csv`,
`.walkforward.csv`, `.console.txt`. 10 bps, weekly, next-day execution; 0 bps carried as a
diagnostic column only.

---

## Leg A — the census (the queue's literal ask)

771 committed CSVs scanned (`.csv` and `.csv.gz`; this run's own outputs excluded), 0 unreadable. 97 files carry an
EWall-type arm beside at least one other arm with both a `Sharpe` and a `CAGR` column →
**44,358 comparison pairs**, of which **37,044 are against a RANKED comparand** (CAND/FWD/top-n/
v1/REV/band/frac) across **91 files**. A cell is the label column's fully-crossed co-columns, so
the EWall row is paired against every value of a dial it does not itself have.

| RANKED pairs (37,044) | count |
|---|---|
| EWall wins on **Sharpe** | 25,878 |
| EWall wins on **CAGR** | 13,317 |
| **Reversals** (`sign dSharpe ≠ sign dCAGR`, eps 0.005 / 5 bps) | **12,475 = 33.7%** (eps=0: 13,358 = 36.1%) |
| — of which EWall-wins-Sharpe-loses-CAGR (the queue's direction) | **12,280 (98.4% of reversals)** |
| — of which EWall-loses-Sharpe-wins-CAGR | 195 |
| **Conditional on EWall winning on Sharpe, it loses on CAGR** | **12,280 / 25,878 = 47.5%** |
| OOS reversals (35,343 pairs with OOS columns) | 10,829 = 30.6% |
| Files with ≥1 reversal | **87 of 91** |
| Files where a MAJORITY of pairs reverse | **18 of 91** |

Sign table (EWall minus ranked, 0 = inside eps):

```
dC     -1.0   0.0    1.0
dS
-1.0   9757    22    195
 0.0    881   208    103
 1.0  12280   579  13019
```

The reversal is **one-directional**: EWall buys Sharpe by giving up CAGR, essentially never the
other way round (12,280 vs 195). Against non-ranked comparands (RAND draws, sleeves, overlays;
7,314 pairs, 24 files) the same conditional rate is only **25.0%**, so this is specifically a
property of comparing an un-ranked book to a *ranked* one, not of EWall in general.

## Leg B — controlled re-read (one construction, idea 82's, imported verbatim)

4 panels × 6 n, gross matched at 0.75 everywhere; saturated cells (`sat_share > 0.25`) excluded
from headline counts.

**Harness reproduction (rows the record published verbatim), exact:**
- `B136/EWall` here **10.7% / 1.026 / −17.7%, OOS 1.019** vs idea 82 and idea 10's published
  10.7% / 1.026 / −17.7%, OOS 1.019.
- `U56/EWall` here 10.4% / 1.049 / −15.9%, 4b fails on **`CAGR` alone** — idea 82's exact wording.

**Reproduction gate** (idea 82's 3 panels × n ∈ {20,30,40,60}, 9 unsaturated cells here vs the 8
idea 82 counted — `BSTK100/n=60` sits at sat_share 0.265, just over the cap either way):
- `EWall − FWD` Sharpe **+0.0410** (published +0.0467), t **+3.52** (+4.03), 7/9 positive (7/8).
- `FWD − EWall` CAGR **+1.26 pp/yr** (published +1.28), t **+5.49** (+4.93), **9/9** positive (8/8).

**Widened to all 4 panels (21 unsaturated cells) the two headlines separate sharply:**

| rung | `EWall − FWD` Sharpe | `EWall − FWD` CAGR | reversals |
|---|---|---|---|
| **10 bps** | **+0.0359, t +1.79, 14/21** | **−2.26 pp/yr, t −6.65, 0/21** | **14/21** (OOS 13/21) |
| 0 bps (diagnostic) | +0.0171, t +0.90, 13/21 | −3.02 pp/yr, t −7.10, 0/21 | 13/21 (OOS 13/21) |

The Sharpe claim is **panel-fragile** — adding SMALL439 drops it from t +3.52 to t +1.79 and it
loses 7 of 21 cells — while the CAGR claim is **unanimous, 0/21, at both rungs**. And the reversal
count barely moves between 10 bps and 0 bps (14 vs 13 of 21), so per idea 260's channel this is
**not** the turnover bill: the ranked book's CAGR advantage is **3.02 pp/yr before costs and 2.26
after**, i.e. EWall's lower turnover (8.2x/yr against FWD5's 18–30x/yr) buys back 0.76 pp/yr and
the sign survives at either rung.

## Leg C — the predictor (can a reversal be flagged before re-running?)

Pre-registered rule: a reversal requires the vol ratio `V_ew/V_cmp` to lie outside the interval
between the CAGR ratio and 1.0.

- Fresh grid (48 cells): **accuracy 0.896**, TP 27 / FP 5 / **FN 0**.
- Census (2,098 RANKED pairs carrying a `Vol` column): accuracy 0.722, precision 0.501,
  **recall 1.000**, FN 0.

**Zero false negatives in both.** The rule is a clean **necessary** condition and a poor sufficient
one — the false positives are where CAGR (geometric) and the arithmetic mean inside Sharpe
disagree. Usable as a cheap screen: if the vol ratio is inside the band, the comparison *cannot*
reverse and one metric is enough; if it is outside, both metrics must be published.

## Rule 8 — does the metric you quote change the book you run?

IS 2009-01-01..2016-12-31 chooses, OOS 2017+ read once. Pooled equal-weight over 4 panels, 10 bps:

| selector | picks | OOS CAGR | OOS Sharpe | OOS MaxDD |
|---|---|---|---|---|
| **EWALL** (do nothing) | EWall ×4 | 9.30% | **0.8577** | −24.9% |
| FWD20 (incumbent) | FWD20 ×4 | 11.73% | 0.8428 | −24.8% |
| S_SHARPE (argmax IS Sharpe) | FWD10, FWD10, FWD20, FWD20 | 11.63% | 0.7815 | −25.6% |
| S_CAGR (argmax IS CAGR) | FWD5, FWD5, FWD20, FWD5 | **14.16%** | 0.7561 | −26.9% |
| RULES v1 OOS Sharpe | — | — | 0.576 / 0.503 / 0.571 / 0.747 | — |
| SPY OOS | — | 15.45% | 0.882 | −33.7% |

**The metric is a decision, not a label:** S_SHARPE and S_CAGR pick a **different arm in 3 of 4
panels**, and switching from Sharpe to CAGR as the selection metric buys **+2.53 pp/yr of OOS CAGR
for −0.0254 of OOS Sharpe** (per panel +0.044 / +0.031 / 0.000 / −0.176). Same picks and the same
sign at 0 bps (+3.03 pp/yr for −0.0230).

**Both IS choosers lose to doing nothing on Sharpe** (EWALL 0.8577 > FWD20 0.8428 > S_SHARPE
0.7815 > S_CAGR 0.7561) — a further instance for idea 229's selection-loses pool — and **all four
lose to SPY OOS (0.882)** on Sharpe and on CAGR.

## KEEP paths (all 64 leg-B points reported)

- **10 bps: 4a 5/32, 4b 6/32.** 4b passes: `U56/FWD20` (12.8%/1.064/−18.3%), `U56/FWD30`,
  `U56/FWD40`, `B136/EWall` (10.7%/1.026/−17.7%), `B136/FWD40`, `B136/FWD60`.
- 0 bps: 4a 1/32, 4b 11/32.
- **Nothing new.** `U56/FWD20` is idea 2's `CAND-n20` construction and `B136/EWall` is idea 10's
  known row; `SMALL439` is **0 of 16** at both rungs, a further reproduction of idea 136.

## Survivorship

`universe_broad.json`, the megacap cut and the small panel are current constituents. On a list of
known survivors the book that holds *everything* inherits the full survivorship premium while any
selection rule can only redistribute it, so the bias runs **toward** the pro-EWall side of every
comparison counted here — i.e. against the finding, which is that EWall's Sharpe win is bought
with CAGR.

## Recommended reporting habit (no RULES change; PROTOCOL habit, for Sunday review)

> Any comparison between an un-ranked book (`EWall` and its variants) and a ranked book must
> publish **CAGR beside Sharpe**, both signed the same way, plus each arm's realised volatility.
> Where the vol ratio lies outside the interval between the two arms' CAGR ratio and 1.0, the
> comparison is reversal-prone and a single-metric verdict is not reportable.

`RULES.md`, `scan.py`, `bot.py` and `baseline.py` untouched.

## Queued follow-ups

- **268** — back-fill the reversal column over the 18 majority-reversing files and report how many
  of their *headline sentences* (not grid rows) change.
- **269** — is the 47.5% conditional rate a property of the ranked arm's `n`? The fresh grid says
  the reversal dies as n → the eligible count; test whether reversal share is a monotone function
  of the concentration ratio `n / n_elig` across the census.
- **270** — S_CAGR vs S_SHARPE as a pre-registered selector pair on the record's other dials.
