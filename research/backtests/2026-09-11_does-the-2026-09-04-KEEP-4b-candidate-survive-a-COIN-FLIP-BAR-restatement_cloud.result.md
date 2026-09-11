# Idea 502 — does the 2026-09-04 KEEP-4b candidate survive a coin-flip-bar restatement?

**Run:** 2026-09-11 UTC, cloud. **Script:** `2026-09-11_does-the-2026-09-04-KEEP-4b-candidate-survive-a-COIN-FLIP-BAR-restatement_cloud.py`

**Verdict: ANSWERED — the candidate SURVIVES the coin-flip bar at the binding cost rung, and the
queue's premise is CORRECTED. It does not need a base-rate clause; it needs a COST clause.**
On its own panel at 10 bps the coin-flip 4b base rate is **0/1000 for a fixed random 20-name list
and 0/1000 for a weekly re-drawn random 20** — not the "quarter of random lists" the queue's
reading of idea 486 implies. But the two nulls fail for two different **non-signal** reasons —
RANDFIX is under-exposed (median gross **0.4996** vs the candidate's **0.7167**), RANDROT is
over-traded (**36.48x/yr** vs **9.64x/yr**) — and at **0 bps the gross-matched null passes 4b
78.1% of the time with the candidate sitting at its 78.2nd percentile**, i.e. *inside its own
null*. What separates this book from a gross-matched coin flip at 10 bps is **turnover, not
selection**: the same exposure held with four times less trading. Nothing is promoted; RULES.md,
PROTOCOL.md, scan.py, bot.py and baseline.py are untouched.

## Gates (pre-registered, printed before any new number was read)

| Gate | Result |
|---|---|
| G1 `ctx_backtest` == `engine.backtest` @10 bps | **6.939e-18** PASS |
| G2 `band_book(0.03,0.75)` == `baseline.rules_v2_weights` | **0.000e+00** PASS |
| G3 the 2026-09-04 KEEP-4b incumbent re-derived on full U56 | **12.63% / 1.0903 / −18.31%** vs published 12.66% / 1.0921 / −18.31%, max\|d\| **1.777e-03** PASS |
| G4 every null book holds ≤ 20 names at exactly 0.75/20, gross ≡ 0.75 × held/20 | dev **0.000e+00**, gross **1.110e-16** PASS |
| G5 the three cost rungs are one gross stream minus turnover × c/1e4 | **2.060e-18** PASS |
| G6 draws reproducible on re-run of seed 502 | **0.000e+00** PASS |
| G7 SMALL439 drops all 44 tickers with `max_1d_move >= 1.0` (483 → 439) | PASS |
| G8 RANDROT built on rebalance rows == the same book written densely and ffilled | **0.000e+00** PASS |

## The two nulls (structural comparands, not tuned parameters)

| Null | Definition | U56 median gross | U56 median turnover |
|---|---|---|---|
| **RANDFIX** | one **fixed** random list of 20 names, held through the same gate at 0.75/20 | 0.4996 | 3.20x/yr |
| **RANDROT** | 20 names drawn at random **from the eligible set every weekly rebalance** | 0.7195 | 36.48x/yr |
| *candidate* | *top 20 by composite, same gate, same 0.75/20* | *0.7167* | *9.64x/yr* |

RANDFIX is the "random 20-name list" of the queue's language; it differs from the candidate in two
ways at once (which names, and how often the list turns over) and, critically, in **exposure**.
RANDROT is **gross-matched by construction** (0.7195 vs 0.7167) and differs from the candidate only
in whether the 20 names are chosen by the composite or by a coin flip — but it pays 3.8x the
candidate's turnover. **Neither null is turnover-matched, and the record contains no null that
is** — that is the gap this run identifies and hands back to the queue.

## The binding result — U56, 10 bps, 1,000 draws (`.percentiles.csv`)

| Null | 4a share | 4b share | cand pctile Sharpe | CAGR | MaxDD | OOS Sharpe |
|---|---|---|---|---|---|---|
| RANDFIX | 2.4% | **0.0%** (0/1000) | **67.4%** | 100.0% | **0.0%** | **50.8%** |
| RANDROT | 0.0% | **0.0%** (0/1000) | 100.0% | 100.0% | 0.1% | 100.0% |

Candidate @10 bps: **12.63% / 1.090 / −18.31%**, H1 1.096, H2 1.092, OOS **14.31% / 1.165 /
−18.31%**, **4b PASS, 4a fail**. SPY 15.11% / 0.883 / −33.72% (4b floors: CAGR ≥ 10.58%,
\|MaxDD\| ≤ 20.23%).

**Read the percentiles honestly.** The candidate is at the **100th percentile of CAGR** and the
**0th percentile of drawdown** — it earns more than every coin flip and draws down deeper than
every coin flip — while its **Sharpe sits at the 67th percentile of fixed random lists and its OOS
Sharpe at the 51st, a coin flip away from the median**. That is the same mechanism ideas 504 and
672 found at draw and full-panel resolution: **the ranking clause earns return, not risk-adjusted
return**, and 4b sees it only through the CAGR floor.

## Cost is the whole separation (tuned axis 2, 1,000 draws, U56)

| Rung | RANDFIX 4b share (cand pctile) | RANDROT 4b share (cand pctile) | cand 4b |
|---|---|---|---|
| 0 bps | 0.1% (78.0%) | **78.1% (78.2%)** | PASS |
| **10 bps (binding)** | 0.0% (67.4%) | 0.0% (100.0%) | PASS |
| 25 bps | 0.0% (47.8%) | 0.0% (100.0%) | PASS |

**At zero cost the queue's suspicion is exactly right**: 781 of 1,000 gross-matched coin flips
clear 4b and the candidate is at their 78th percentile — the bar certifies the *family* (20 gated
U56 names at 0.75 gross), not the rule. The candidate's separation appears only once turnover is
priced, and it is a **persistence** property of the composite score, not a selection property.

## Draw-count stability (tuned axis 1, U56 @10 bps)

| Null | 250 draws | 500 draws | 1,000 draws |
|---|---|---|---|
| RANDFIX | 0.0% (pctile 67.2%) | 0.0% (67.6%) | 0.0% (67.4%) |
| RANDROT | 0.0% (100.0%) | 0.0% (100.0%) | 0.0% (100.0%) |

The share and the percentile are flat in the draw count; 250 draws would have given the same
answer. The nested design means the 250-draw grid is the first 250 seeds of the 1,000.

## Replication panels (no verdict taken from these)

| Panel | Null | 4b share @10 bps | cand pctile Sharpe | cand 4b |
|---|---|---|---|---|
| B136 | RANDFIX | 0.1% | 43.6% | fail (H2) |
| B136 | RANDROT | 0.0% | 100.0% | fail (H2) |
| SMALL439 | RANDFIX | 0.0% | 91.8% | fail (all five legs) |
| SMALL439 | RANDROT | 0.0% | 100.0% | fail (all five legs) |

On B136 — idea 486's own panel — the candidate's Sharpe is **below the median random fixed list
(43.6th percentile)** and it does not pass 4b at all. On SMALL439 RANDFIX's median gross is only
**0.2411**, so its levels are an exposure artefact and nothing else.

## PROTOCOL rule 8 — chooser on 2009–2016 only, scored 2017–2026 untouched (`.walkforward.csv`)

| Panel | Null | IS-best draw (IS Sharpe vs cand) | that draw's OOS | candidate OOS | cand OOS pctile |
|---|---|---|---|---|---|
| U56 | RANDFIX | #410 (1.359 vs 0.993) | 8.85% / **1.211** / −10.93% | 14.31% / 1.165 / −18.31% | 50.8% |
| U56 | RANDROT | #212 (0.930 vs 0.993) | 7.34% / 0.772 / −15.31% | 14.31% / 1.165 / −18.31% | 100.0% |
| B136 | RANDFIX | #868 (1.390 vs 1.044) | 5.91% / 0.924 / −11.60% | 12.49% / 0.892 / −20.05% | 22.6% |
| B136 | RANDROT | #179 (0.893 vs 1.044) | 3.87% / 0.405 / −20.92% | 12.49% / 0.892 / −20.05% | 100.0% |
| SMALL439 | RANDFIX | #234 (1.116 vs 0.420) | 0.75% / 0.160 / −15.46% | 7.23% / 0.487 / −27.43% | 93.5% |
| SMALL439 | RANDROT | #564 (0.399 vs 0.420) | −0.98% / 0.006 / −40.99% | 7.23% / 0.487 / −27.43% | 100.0% |

Two things worth stating plainly. **The luckiest in-sample coin flip beats the candidate's OOS
Sharpe on U56** (1.211 vs 1.165) — and loses 5.5 pp of OOS CAGR doing it, because it is a
half-exposed book. And the IS chooser is worthless on its own terms: the best IS Sharpe among
1,000 fixed lists (1.359) collapses to 1.211 OOS, and on B136 from 1.390 to 0.924.

## Record cross-check — what is idea 486's "24.9%" actually a rate for? (`.crosscheck.csv`)

The queue's sentence — *"4b alone passes on 747 of 3,000 random B136 CAND-20 draw books (24.9%),
i.e. the 4b bar is cleared by a quarter of random 20-name lists"* — **conflates two different
nulls**. A "CAND-20 draw book" is the **ranked rule run on a random sub-panel**: it still ranks.
A random 20-name list does not. Re-reading the record's own committed draw grid (idea 504's
1,000-draw artefact, the nearest committed relative) at 10 bps:

| Panel | CAND-20-on-a-random-sub-panel 4b share (committed) | this run's random-**LIST** 4b share |
|---|---|---|
| U56 | **72.3%** | **0.0%** |
| B136 | **44.4%** | **0.1%** |
| SMALL439 | 0.0% | 0.0% |

So the tens-of-percent base rate the record quotes is a rate for a **book that still ranks**, and
the true coin-flip rate is ~0. Note the level gap against 486's published 24.9% (44.4% here on
B136): idea 504 stated that 486's artefact could not be located and that its draw family was
re-derived, so the levels are not expected to match bit-for-bit and **no claim here rests on
486's rows**. The qualitative correction does not depend on the level.

## Survivorship (PROTOCOL 9)

B136 is today's constituents, SMALL439 the current sub-$2B screen only
(`data/SMALL_PANEL_README.md`); U56 carries a milder form of the same bias. The direction matters
here and favours the queue's suspicion, not the incumbent: **a random list drawn from a survivor
panel is a better book than a random list drawn in real time would have been**, so the null's 4b
pass share is an **upper** bound on the true coin-flip base rate and the candidate's percentile
inside it is a **lower** bound. Stated, not buried.

## Memo — 10 lines

1. **The KEEP does not need a base-rate clause.** At 10 bps the coin-flip 4b rate on U56 is
   **0/1000** on both nulls; the candidate's 4b pass is not something a coin flip reproduces.
2. **It does need a cost clause.** At 0 bps a gross-matched coin flip passes 4b **78.1%** of the
   time and the candidate sits at its **78.2nd** percentile — inside its own null.
3. The separation at 10 bps is **turnover**: 9.64x/yr against the matched null's 36.48x/yr.
4. What the composite buys over a coin flip at equal gross is therefore **persistence**, and the
   record has never priced that separately from selection.
5. On risk-adjusted return the candidate is **ordinary**: 67th percentile of Sharpe and 51st of
   OOS Sharpe against fixed random lists; 100th of CAGR and 0th of drawdown.
6. Exact RULES wording, unchanged from the 2026-09-04 candidate and pinned in code by G3:
   > *Each Monday, score every instrument by the average of its percentile ranks on 12-1 momentum,
   > 6-month and 3-month return (no volatility scaler). An instrument is **eligible** if its close
   > is above its 200-day moving average and its 20-day annualised volatility is below 0.60. Hold
   > the **top 20 eligible** names at a fixed **3.75% of NAV each** (0.75 gross ÷ 20). If fewer
   > than 20 are eligible, hold only those and leave the remainder in **cash** — never re-spread.
   > Trade at the next day's close; assume 10 bps per unit turnover.*
7. Attach to any promotion: *"clears a bar that a zero-cost coin flip clears 78% of the time; its
   margin is turnover, and its Sharpe is at the 67th percentile of random 20-name lists."*
8. **Correct the record's prose:** idea 486's 24.9% is the pass rate of the **ranked** rule on
   random sub-panels (44.4% on B136 and 72.3% on U56 in the committed 504 grid), not of random lists.
9. On B136 the candidate is **below the median** coin flip on Sharpe (43.6th pctile) and fails 4b.
10. **Recommended action: no RULES change this week.** The missing experiment is a
    **turnover-matched** coin flip; queued as a follow-up.
