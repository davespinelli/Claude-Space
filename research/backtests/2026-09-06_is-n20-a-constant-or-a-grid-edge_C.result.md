# Idea 240 — is-n20-a-constant-or-a-grid-edge (lane C, 2026-09-06)

**Verdict: KILL for "take the widest n", and a CORRECTION to idea 77's 7-of-7 claim. n=20 was
a grid edge. On {20,30,40,60} the OOS argmax splits 3 at 20 / 1 interior / 3 at 60 — but it is
neither a constant nor an edge: it tracks the panel's own eligible count, Spearman +0.926 on
both weighting conventions. Half the apparent width premium is the gross ladder. The
do-nothing incumbent still beats every rule tested.**

Script: `research/backtests/2026-09-06_is-n20-a-constant-or-a-grid-edge_C.py`
Console: `…_C.console.txt` · CSVs: `.grid` (98 pts) `.argmax` `.walkforward`

## Reproduction gate (read before anything new)

Idea 73/77's panels, gate (200d + vol20<0.60), ranking key (no vol scaler), 75% gross, weekly
cadence, 10 bps and next-day execution were imported verbatim. Idea 77's published n=20 IS/OOS
column reproduces on all 7 panels, max abs difference **0.0004**:

| panel | IS (pub) | OOS (pub) | | panel | IS (pub) | OOS (pub) |
|---|---|---|---|---|---|---|
| STK20 | 1.0392 (1.039) | 1.4458 (1.446) | | BSTK100 | 1.0520 (1.052) | 0.9383 (0.938) |
| B136 | 1.0251 (1.025) | 0.8919 (0.892) | | U56 | 0.9556 (0.956) | 1.1680 (1.168) |
| SMALL484 | 0.4709 (0.471) | 0.5104 (0.510) | | ETF24 | 0.5304 (0.530) | 0.8886 (0.889) |
| ETF36 | 0.5771 (0.577) | 0.9419 (0.942) | | | | |

Harness rows: U56/CAND20 12.7% / 1.092 / -18.3% (idea 2 KEEP 12.7% / 1.093 / -18.3%); U56/v1
6.5% / 0.664 / -13.8%. Common window 2011-01-13 → 2026-09-04 (3,934 days), identical days for
all seven panels. SPY on it 14.1% / 0.862 / -33.7%, halves 0.891/0.858, OOS 0.882.
4b bars: MaxDD ≤ 20.2%, CAGR ≥ 9.89%, OOS Sharpe > 0.8820.

## The de-grossing control (declared in the script header, before any result)

Idea 73's book is `rank ≤ n` at a **fixed** weight GROSS/n, so on a panel that cannot supply n
eligible names, widening n *is a gross ladder wearing an n label*. Both conventions are run and
both are reported everywhere:

- **FIXED** — w = 0.75/n (idea 73's, verbatim; pre-registered as primary).
- **NORM** — w = 0.75/min(n, n_elig), i.e. always 75% invested (the width dial with the gross
  channel closed).

The confound is large: U56 at n=60 holds mean gross **0.474** under FIXED against 0.750 under
NORM; STK20 at n=20 is 99.3% saturated and n=30/40/60 are byte-identical books there (max abs
return difference 0.00e+00).

## 1. The answer: n=20 was the edge, and "widest" is not the rule either

Tuned parameters: panel (7) and n (6 values). All 84 CAND points + 14 references are in `.grid.csv`.

| | n=20 | interior (30/40) | n=60 |
|---|---|---|---|
| OOS argmax, FIXED | 3/7 | 1/7 | 3/7 |
| OOS argmax, NORM | 3/7 | 1/7 | 3/7 |

Idea 77's **7 of 7 at n=20 does not survive the grid being widened** — 4 of 7 panels move the
moment 30/40/60 exist. Outcome (A) of the three the script pre-registered is dead.

But outcome (B) — "take the widest n" — is dead too. Pooled OOS Sharpe (equal weight over the
7 panels), WIDEST60 minus WIDEST20: **+0.0609 (FIXED) / +0.0335 (NORM)**, on **4/7** and **3/7**
panels respectively. A rule that wins on three or four panels of seven is a coin flip, and the
RANDOM control (mean over the four n values) sits *between* the two edges at 0.994 (FIXED),
i.e. the pooled premium is a mean effect, not a decision rule.

## 2. What the argmax actually is: the panel's own size

| panel | tradable | mean elig | share of weeks that cannot fill n=20 | OOS argmax (FIXED / NORM) |
|---|---|---|---|---|
| STK20 | 20 | 13.5 | **99.3%** | 20 / 20 |
| ETF24 | 24 | 17.4 | 47.6% | 20 / 20 |
| ETF36 | 36 | 24.4 | 20.6% | 20 / 20 |
| U56 | 56 | 37.9 | 9.5% | **40 / 30** |
| BSTK100 | 100 | 68.4 | 1.6% | 60 / 60 |
| B136 | 136 | 92.9 | 1.2% | 60 / 60 |
| SMALL484 | 483 | 148.3 | 0.9% | 60 / 60 |

**Spearman(mean eligible count, OOS argmax n) = +0.926 on BOTH conventions** (N=7, descriptive —
7 draws, nothing here is strongly evidenced). The three panels that "stay at 20" are exactly the
three that cannot supply more than that; the three that go to 60 are the three largest, where 60
is *again* the top of the grid. **The ceiling is still not located for any panel with ≥60 eligible
names** — this run moved the edge, it did not remove it. `argmax/mean_elig` ranges 0.40 to 1.48
and is not a constant either.

## 3. Rule 8 walk-forward — rules and directions fixed before any OOS read

IS 2009-2016, OOS 2017-2026 read once. Pooled = equal weight over the 7 panels; NOTHING is the
project's incumbent U56/n=20 alone.

| rule | pre-registered as | OOS Sharpe (FIXED) | OOS CAGR | OOS MaxDD | OOS Sharpe (NORM) |
|---|---|---|---|---|---|
| **NOTHING** | incumbent U56/n=20, no dial read | **1.168** | **14.4%** | -18.3% | **1.131** |
| WIDEST60 | widest n on THIS grid | 1.030 | 6.9% | -12.5% | 0.933 |
| RANDOM | mean over the 4 n values | 0.994 | 8.8% | -15.3% | 0.908 |
| ISARGMAX | argmax IS Sharpe within panel | 0.976 | 10.8% | -18.1% | 0.907 |
| WIDEST20 / NARROWEST | widest on idea 73's grid = narrowest on this one | 0.969 | 11.1% | -18.2% | 0.900 |

References OOS: SPY 15.5% / 0.882 / -33.7%; RULES v1 (U56) 7.7% / 0.747 / -13.8%.

Three readings:

1. **Doing nothing beats every dial rule on the table**, by +0.138 over the best of them. This is
   a **12th instance for idea 229's pool** of an IS-informed or constant dial rule losing to the
   incumbent out of sample.
2. **The IS reading of the dial is worse than a coin flip**: ISARGMAX − WIDEST20 = **+0.0070**
   against RANDOM's **+0.0244** (identical +0.0070 vs +0.0086 under NORM). ISARGMAX moves only
   2 of 7 panels (B136 and BSTK100, both 20→30) and both of those under-shoot the OOS argmax of 60.
3. **WIDEST60's Sharpe is bought with return**: OOS CAGR 6.9% against WIDEST20's 11.1% and SPY's
   15.5% — under FIXED it is de-grossing (mean gross 0.72 → 0.47 on U56), not width.

## 4. Closing the gross channel halves the effect and reverses two cells

| | FIXED | NORM |
|---|---|---|
| pooled WIDEST60 − WIDEST20 | +0.0609 (4/7 wins) | +0.0335 (3/7 wins) |
| U56 n=30 vs n=20, full Sharpe | 1.102 vs 1.092 (**wider wins**) | 1.055 vs 1.068 (**incumbent wins**) |
| BSTK100 n=60, MaxDD | -17.1% at gross 0.697 (4b **PASS**) | -26.4% at gross 0.748 (4b **FAIL on DD**) |

Idea 135's control, confirmed on this dial: the two most attractive-looking new cells are gross
ladder points, not width findings. U56/n=30's apparent Sharpe edge over the standing candidate
disappears the moment the book is held at constant gross.

## 5. KEEP paths — both, every point

**4a:** FIXED 23/42, NORM 4/42. **4b:** FIXED 11/42, NORM 13/42.

4b passers new relative to idea 77 (which published U56/n10, U56/n20, STK20/n5, STK20/n10,
STK20/n20): **U56/n30, B136/n40, B136/n60, BSTK100/n30, BSTK100/n40, BSTK100/n60** under FIXED;
**U56/n40, U56/n60, STK20/n30-60 (duplicates of n=20), B136/n40, B136/n60** under NORM.

Best new row, BSTK100/n=60 FIXED: 11.4% / **1.108** / -17.1%, halves 1.178/1.040, OOS 1.129,
turnover 6.3x/yr — clears 4b *and* 4a. **Nothing is promoted.** It fails 4b under NORM on the
drawdown bar (-26.4% vs the -20.2% cap), i.e. the whole margin is the de-grossing the FIXED
convention performs silently; and BSTK100 is 100 current-constituent broad-list stocks, the
survivorship exposure idea 77 already flagged. Widening n on a survivorship-selected list adds
names known ex post to have survived, so "wider is better" is partly manufactured here.

**RULES wording recommended: none.** RULES.md, scan.py, bot.py and baseline.py untouched.

## 6. Limits, and what to report next

N=7 panels, all current constituents, one-directional. The +0.926 is descriptive over 7 draws.
Both grid edges (20 and 60) are still argmaxes on 3 panels each, so this run relocated the edge
problem rather than solving it — a fair reading is that *no* published n argmax in the record
should be quoted without its panel's eligible count and its saturation share beside it, since
n=20 on STK20 (99.3% saturated) and n=20 on SMALL484 (0.9%) are not the same dial setting.
Ideas 242-244 queued.
