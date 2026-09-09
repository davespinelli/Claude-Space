# Idea 308 — why does the CORR ordering die at q=0.75? (cloud, 2026-09-09)

**VERDICT: ANSWERED — NEITHER of the queue's two candidate causes survives its own statistic,
and the premise itself is a mixture. (1) RANGE RESTRICTION is refuted: pooled sd(corr_IS) is
0.0270 → 0.0289 → 0.0269 across q=0.25/0.50/0.75 — FLAT (0.999×) — it shrinks only at k=20 and
GROWS at k=40 and k=80, and the Thorndike correction that restores the q=0.25 predictor spread
moves mean |rho| at q=0.75 the WRONG WAY (0.1603 → 0.1439 against a 0.3062 target).
(2) A RISING NOISE FLOOR is refuted in the direction stated but replaced by something worse:
the noise does not rise with q, it is at the floor at EVERY q. A panel's OOS Sharpe has no
test–retest reliability anywhere — split-half r_AB = +0.049 / −0.049 / +0.065 (Spearman–Brown
R = +0.088 / −0.152 / +0.064) — so every rho in this family, including the "7/9 significant"
at q=0.25, is a correlation against an outcome that does not replicate against itself.
(3) The exact identity (residual 4.44e-16) puts the change in the SLOPE, not either spread —
and only at k=20 and k=40: at k=80 |rho| GROWS with q (−0.105 → −0.310), so idea 293's q-dial
is a k=20/40 fact averaged over a sign flip, not a law. (4) The one thing that does NOT die at
q=0.75 is the tradable edge: the rule-8 walk-forward edge is +0.105 (9/9) at q=0.25, +0.034
(7/9) at q=0.50 and **+0.099 (9/9) at q=0.75**. KILL for capital anyway — picks lose to SPY at
every q on CAGR and to RULES v2 on Sharpe. RULES v2 unchanged; no new KEEP.**

Script: `research/backtests/2026-09-09_why-does-the-CORR-ordering-die-at-q-0.75_cloud.py`
Artefacts: `.panels.csv` (545), `.strata.csv` (27 cells), `.decomp.csv`, `.walkforward.csv`,
`.keeppaths.csv`, `.console.txt`.

## What was priced

Idea 284/293's construction verbatim: 540 constructed panels = 3 q × 3 k × 60 seeds, seed key
`crc32("STRAT|{q:.3f}|{sd}")`, drawn from BSTK100 large-cap stocks and the sub-$2B panel; books
EWall / CAND10 / CAND20 plus v2 as the 4a comparand; weekly, 10 bps, next-day, gross 0.75,
IS ≤ 2016-12-31 / OOS ≥ 2017-01-01. Two tuned parameters — **q** and **k**, the same two idea
293 tuned. All 27 (q, k, book) cells reported; nothing selected on the outcome.

### Gates (all passed before any verdict was read)

- **G1** the rebuild reproduces idea 293's committed `.panels.csv` on all 540 constructed
  panels to **2.220e-16** (max over `corr_IS`, `disp_IS`, `evol_IS`, `breadth_IS` and the three
  books' full and OOS Sharpe). Same objects, not a re-specification.
- **G2** (q=0.500, k=40) reproduces idea 284's published rho: EWall **−0.4708** (|diff| 0.00000),
  CAND10 **−0.3648** (0.00002), CAND20 **−0.4815** (0.00002).
- **G3** idea 293's q-gradient reproduces to 4e-5: **−0.3426 / −0.3152 / −0.1462**, significant
  7/9, 7/9, **1/9**, seed halves agree 9/9, 9/9, **4/9**.

## The two statistics the queue asked for

| q | mean rho | **sd(corr_IS)** | **sd(OOS Sharpe)** | beta | Lo SE(Sharpe) | R analytic | R split-half | sig |
|---|---|---|---|---|---|---|---|---|
| 0.25 | −0.3426 | 0.0270 | 0.1370 | −1.589 | 0.3741 | −7.26 | +0.088 | 7/9 |
| 0.50 | −0.3152 | 0.0289 | 0.1620 | −2.053 | 0.3601 | −4.61 | −0.152 | 7/9 |
| 0.75 | −0.1462 | 0.0269 | 0.1844 | −1.254 | 0.3442 | −2.79 | +0.064 | 1/9 |

**q 0.25 → 0.75: sd(corr_IS) ×0.999, sd(OOS Sharpe) ×1.346, |rho| ×0.427.**

## Cause A — range restriction: refuted

The predictor spread is flat pooled and non-monotone within k: **k=20 0.0396 → 0.0346**
(shrinks, u=1.146), **k=40 0.0263 → 0.0279** (grows), **k=80 0.0150 → 0.0183** (grows). The
sd_x term of the decomposition is negative in only **3 of 9** (k, book) pairs — the three at
k=20. Applying the Thorndike case-2 correction that rescales each q=0.75 cell to the q=0.25
predictor spread takes mean |rho| from **0.1603 to 0.1439** — further from the 0.3062 target,
because at k=40 and k=80 the correction *shrinks* rho (u < 1). Range restriction cannot be the
mechanism of something it moves in the wrong direction on two of three widths.

## Cause B — the noise floor: not rising, already at the floor everywhere

The outcome spread does rise (sd_y term negative in **9/9** pairs, the only consistently signed
term). But that is not a rising noise floor:

- **Analytic.** Lo (2002) SE of a panel's ~9.7-year OOS Sharpe is 0.3741 / 0.3601 / 0.3442 — it
  *falls slightly* with q, and is **2.0–2.7× larger than the entire cross-panel sd** it must sit
  inside. Implied reliability is negative at every q (−7.26 / −4.61 / −2.79).
- **Empirical.** Each panel's Sharpe on 2017-01-03..2021-11-01 correlated across the 60 seeds
  against its Sharpe on 2021-11-01..2026-09-04: **r_AB = +0.049 / −0.049 / +0.065**,
  Spearman–Brown **R = +0.088 / −0.152 / +0.064**. A panel's OOS Sharpe does not predict its own
  OOS Sharpe in the other half of the same window, at any cap mix.

Disattenuation is therefore inadmissible, and its failure mode is the diagnosis: dividing by
√R gives |rho| = 1.043 at q=0.25 and 1.195 at q=0.50 — out of range. **The noise floor is not
what changed at q=0.75; it is what the whole family has been standing on all along.**

*Honest limit on the analytic leg:* the 540 panels share one market factor, so their OOS Sharpes
are strongly cross-correlated and the between-panel variance is legitimately far below the
independent sampling variance — a negative `R_analytic` is expected in this design and is not by
itself proof of unreliability. The **split-half** estimate is the defensible one, and it says
zero too, which is why the conclusion rests on it.

## What actually carries the change — and where the premise breaks

`rho = beta × sd_x / sd_y` holds to **4.44e-16**, so the q=0.25 → 0.75 change splits exactly:

| k | book | rho q0.25 | rho q0.75 | dlog\|rho\| | beta term | sd_x term | sd_y term |
|---|---|---|---|---|---|---|---|
| 20 | EWall | −0.4108 | −0.0541 | −2.028 | **−1.785 (88%)** | −0.136 | −0.107 |
| 20 | CAND10 | −0.3864 | −0.0590 | −1.880 | **−1.620 (86%)** | −0.136 | −0.124 |
| 20 | CAND20 | −0.4063 | −0.0460 | −2.179 | **−1.940 (89%)** | −0.136 | −0.103 |
| 40 | EWall | −0.3018 | −0.1342 | −0.810 | **−0.456 (56%)** | +0.058 | −0.413 |
| 40 | CAND10 | −0.3976 | −0.1565 | −0.932 | **−0.538 (58%)** | +0.058 | −0.452 |
| 40 | CAND20 | −0.2830 | −0.1400 | −0.704 | −0.305 (43%) | +0.058 | **−0.457 (65%)** |
| 80 | EWall | −0.1053 | **−0.3104** | **+1.081** | +1.078 | +0.202 | −0.199 |
| 80 | CAND10 | −0.2441 | −0.2586 | +0.057 | +0.408 | +0.202 | −0.552 |
| 80 | CAND20 | −0.2203 | −0.2840 | +0.254 | +0.372 | +0.202 | −0.321 |

Two things follow. First, at k=20 and k=40 the **slope collapses** — a term the queue named
neither, and one that means the relationship weakened rather than the measurement. Second, and
larger: **dlog|rho| is negative in only 6 of 9 pairs. At k=80 the ordering STRENGTHENS at
q=0.75.** Idea 293 saw the edge of this ("k=80 is the one width where q=0.75 survives") but
reported the pooled q-gradient as the dial. Pooling over a sign flip is not a gradient. The
correct statement is that the q-decay is a **narrow-panel** phenomenon and reverses at k=80.

## Rule 8 — the statistic dies, the edge does not

Direction fitted on **seeds 0–29 with IS-window statistics only**, applied once to the untouched
seeds 30–59, picking the 5 panels the fitted direction favours. The fitted direction is negative
in **27/27** cells.

| q | mean edge vs anchor | positive | picks OOS CAGR | anchor / SPY / v2 | picks OOS Sharpe | SPY / v2 | picks OOS MaxDD | SPY / v2 |
|---|---|---|---|---|---|---|---|---|
| 0.25 | **+0.1051** | **9/9** | 12.60% | 10.83 / 15.45 / 7.77% | 0.9245 | 0.8820 / 0.9885 | −25.62% | −33.72 / −12.32% |
| 0.50 | +0.0339 | 7/9 | 9.61% | 9.12 / 15.45 / 6.66% | 0.7148 | 0.8820 / 0.8556 | −27.40% | −33.72 / −13.00% |
| 0.75 | **+0.0994** | **9/9** | 8.72% | 6.94 / 15.45 / 5.14% | 0.6135 | 0.8820 / 0.6674 | −29.87% | −33.72 / −14.78% |

The walk-forward edge at q=0.75 (+0.099, 9/9) is essentially the q=0.25 edge (+0.105, 9/9) and
larger than q=0.50's. **Whatever dies at q=0.75, it is the rho statistic, not the selector.**
That is a correction to how idea 293's result has been read.

It is still a KILL for capital: picks lose to SPY on CAGR at every q (12.60 / 9.61 / 8.72% vs
15.45%) and to the live RULES v2 book on Sharpe at q=0.25 and q=0.50, clearing SPY's Sharpe only
at q=0.25 — where they carry more than twice v2's drawdown.

## Both KEEP paths — all 1,620 panel-books, no selection

| q | pass 4a | pass 4b | both |
|---|---|---|---|
| 0.25 | 0 / 540 | **33 / 540** | 0 |
| 0.50 | 0 / 540 | 6 / 540 | 0 |
| 0.75 | 2 / 540 | **0 / 540** | 0 |

**0 of 1,620 clear both paths.** The DD bar appears in every failing set at every q, and 4b
passage falls monotonically in q (33 → 6 → 0) exactly as the cap-mix gradient of ideas 284/293
and the open question of idea 548 predicts — while 4a moves the other way (0 → 0 → 2), the same
near-exclusivity idea 404 and idea 544 measured on the gross dial.

## Survivorship

Every panel is drawn from current constituents of `universe_broad.json` and of the sub-$2B screen
(`prices_small.csv.gz` less the 44 tickers with `max_1d_move ≥ 1.0`). No delistings. Small-cap
survivorship is the worse of the two and **rises with q — the very dial under test** — so the
q=0.75 levels are the most inflated of the three, and the CAGR and 4b columns inherit that whole.
The cross-stratum contrasts and the reliability coefficients are the defensible objects here; the
levels are not.

## What this changes

Nothing in RULES v2. It closes idea 308 with a negative answer to both offered causes and hands
the queue three corrections: the q-gradient reverses at k=80 and should not be quoted pooled; the
rho's denominator has no test–retest reliability at any q, so the whole `corr_IS → OOS Sharpe`
literature in the record is measured against an unreliable outcome; and the walk-forward edge
does not decay in q even though the correlation does.
