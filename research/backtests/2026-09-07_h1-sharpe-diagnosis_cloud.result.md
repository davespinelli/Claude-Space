# Idea 43 — h1-sharpe-diagnosis (2026-09-07, cloud)

**ANSWERED, and the queue's premise is FALSIFIED on the panels it was written about. Neither of the
two offered explanations is right: it is not a 2009-10 beta miss and it is not a regime failure —
the book's whole first-half Sharpe edge is a VOLATILITY term sitting on top of a NEGATIVE return
term, uniformly across every year of H1. 4a 0/45, 4b 7/45 at 10 bps, 0/45 at 25 bps. No RULES
change, no KEEP claimed; RULES.md, scan.py, bot.py and baseline.py untouched.**

Script `research/backtests/2026-09-07_h1-sharpe-diagnosis_cloud.py`, console
`…_cloud.console.txt`, artefacts `.grid.csv` (45 cells x 3 rungs, every point printed),
`.yearly.csv` (108 book-years), `.loyo.csv`, `.walkforward.csv`.

## Gates (passed before any new number was read)
- `fast_backtest` vs `engine.backtest`: max|dr| **0.000e+00**, max|dturnover| **0.000e+00**.
- Derived rung `r(c) = r(0) − turnover·c/1e4` vs a live `backtest(cost_bps=25)`: **0.000e+00**.
- Gross-invariance of Sharpe, measured not assumed: top-20 at g=0.75 vs g=1.00 @10 bps reads
  **1.0635 vs 1.0638** (span 0.0002). This is load-bearing: **no gross setting can close a Sharpe
  gap**, so "the book misses 2009-10 beta" cannot be a position-size statement.

## [P] Is H1 still "the single binding 4b constraint"? No — DRAWDOWN is.
Census over 45 cells (n ∈ {5,10,20,40,ALL} × gross ∈ {0.75,0.85,1.00} × 3 panels):

| rung | 4b | 4a | failing bars (count of 45) | H1 the SOLE failing bar |
|---|---|---|---|---|
| 0 bps | 11/45 | 0/45 | **DD 34**, H2 18, H1 15, OOS 15, CAGR 11 | **0/45** |
| 10 bps | 7/45 | 0/45 | **DD 34**, H2 24, H1 21, OOS 21, CAGR 16 | **2/45** |
| 25 bps | 0/45 | 0/45 | H1 39, H2 36, DD 35, OOS 33, CAGR 24 | 1/45 |

On **B136 the H1 bar is cleared by 15/15 cells** (best 1.144 vs SPY's 0.957, +0.188); on U56 by
9/15 (best 1.068, +0.112). The premise survives only on **SMALL439: 0/15, best 0.608 vs 0.891
(−0.283)**. Ideas 24/25/28/40 are pre-index-fix rows (QUEUE 38/39); on the corrected index the
binding bar for this family moved to drawdown, and any future work aimed at "the H1 problem"
should be aimed at the small panel instead.

## [Y] The decomposition — the answer is a VOL term, not a 2009-10 term
`S_book − S_SPY = (mu_b − mu_s)/sig_b + mu_s·(1/sig_b − 1/sig_s)` over H1, at 10 bps, g=0.75:

| panel / book | H1 gap | RETURN term | VOL term | vol-matched counterfactual Sharpe | SPY H1 |
|---|---|---|---|---|---|
| U56 / EWALL | +0.111 | **−0.621** | **+0.731** | 0.605 | 0.957 |
| B136 / EWALL | +0.187 | **−0.410** | **+0.597** | 0.704 | 0.957 |
| SMALL439 / EWALL | −0.456 | −0.646 | +0.189 | 0.358 | 0.891 |

The book never out-returns SPY in H1 on any panel; it wins on Sharpe purely by running at half
SPY's volatility (U56 EWALL beta by year **0.24–0.71**, mean invested gross a flat 0.750). Carried
at SPY's volatility the same book would score **0.605 / 0.704 / 0.358** against SPY's 0.957/0.957/
0.891 — it would lose outright. Combined with the gross-invariance gate, that is the structural
reason 4b is a narrow corridor here: the vol advantage cannot be converted into return, and the
dial that would try (gross) moves CAGR and MaxDD together, which is why **DD is the bar that fails
34 of 45 cells**.

## Leave-one-year-out on H1: no year is the story
No single deleted year flips the sign of the H1 gap on any panel or book (9 years × 6 book-panels).
U56 EWALL: gap ranges +0.069…+0.154 across deletions; **2009+2010 alone is +0.101** and dropping
both leaves **+0.098** — the exact opposite of a 2009-10 miss. B136 EWALL: **+0.066** in 2009-10,
+0.220 without it. The one place the queue's intuition has any support is the **ranked top-20 book
on U56**, where 2009+2010 alone is **−0.111** (vs +0.179 for H1 without it) — a real but
non-decisive drag that never flips a verdict. SMALL439 stays −0.35…−0.60 under every deletion:
a homogeneous failure, not an episode.

## [R] Is 4b reachable on this universe? Yes on the large-cap panels, never on the small one
At 10 bps: **U56 4/15** (best n=20 g=0.75, 12.79% / 1.064 / −18.31%, H1/H2 1.068/1.066, OOS 1.131),
**B136 3/15** (best EWALL g=0.75, 10.70% / 1.025 / −17.69%, H1/H2 1.143/0.915, OOS 1.019),
**SMALL439 0/15** (closest cell's worst bar margin −0.42, failing all five). At 25 bps: **0/45** —
consistent with idea 323's finding that this family's passes are ≤10-bps objects.

## Rule 8 walk-forward ((n, gross) chosen on IS ≤ 2016 by Sharpe, OOS 2017+ read once, 10 bps)

| panel | IS-chosen | OOS CAGR | OOS Sharpe | OOS MaxDD | anchor (EWALL g=0.75) | OOS-best | regret |
|---|---|---|---|---|---|---|---|
| U56 | n=20 g=0.85 | 16.40% | 1.131 | −20.60% | 1.113 | 1.136 | **−0.005** |
| B136 | n=10 g=1.00 | 16.72% | 0.785 | −27.95% | 1.019 | 1.019 | **−0.234** |
| SMALL439 | n=20 g=1.00 | 8.64% | 0.467 | −42.96% | 0.288 | 0.553 | −0.086 |

RULES v2 (live) OOS Sharpe 1.285 / 1.119 / 0.568; SPY OOS 0.882 (CAGR 15.45%, MaxDD −33.72%).
The IS chooser beats the anchor on 2 of 3 panels but loses to the OOS-best everywhere — the
record's recurring "IS chooser is not free" result, and on B136 it costs 0.23 of Sharpe by
choosing gross 1.00.

## Verdict
**KILL of the premise as stated** (H1 is not the binding bar on U56/B136 and is not decided by
2009-10 anywhere), **CONFIRM of the constraint on SMALL439**, and one durable structural fact for
the record: on these panels the eligible-equal-weight family is a de-risked market, not an alpha
book — its Sharpe edge is entirely the vol term, so 4b lives or dies on the DD and CAGR bars.
No new book, no KEEP-candidate, nothing promoted.

## Caveats
All three panels are current-constituent lists (**survivorship**), which flatters every momentum
book; the sub-$2B panel is the worst offender and the 44 tickers with `max_1d_move ≥ 1.0` in
`data/small_meta.csv` were dropped before anything was run (439 names + SPY, from 2010-01-04, so
it has no 2009 and cannot speak to the 2009-10 question — it is carried as a regime control only).
Per-year betas are OLS on daily returns within the calendar year, no lag adjustment.
