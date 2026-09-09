# Idea 527 — is the rule-8 OOS leg of 4b a REDUNDANT TEST across the record?

**Verdict: ANSWERED / the premise is REFUTED corpus-wide. No KEEP, no rules change, PROTOCOL.md untouched.**
Script: `2026-09-09_price-the-OOS-LEG-of-4b-as-a-REDUNDANT-TEST-across-the-record_C.py`
Artefacts: `.census.csv` `.subsets.csv` `.live.csv` `.console.txt`

## 1. The answer

Idea 285 reported "the OOS bar is the SOLE binding bar in 0 of 1,520 failures". That reproduces
**exactly** on its own corpus (gate G1: 1,680 arm-rows, 1,520 failures, sole-OOS 0, |delta| 0 on
all three) and **does not generalise**. Over 235 runs / 469,469 committed 4b decisions that can
still be re-read bar by bar:

| | decisions | failures | sole H1 | sole H2 | **sole OOS** | sole DD | sole CAGR |
|---|---|---|---|---|---|---|---|
| record, run-pooled | 469,469 | 399,086 | 3,146 | 1,710 | **46** | 45,439 | 77,425 |

**46 of 399,086 (0.00012), in 6 of 235 runs.** Plus **1** more recovered from the ambiguous tier
(below) = **47 corpus-wide**. The queue's conditional ("if the answer is zero corpus-wide") is
**not met**, so nothing should be written into PROTOCOL that says the leg never cuts alone.

The six runs where it did: `the-IS-chosen-substitute-arm-for-every-named-asset-set_C` (31),
`is-the-conditional-sleeve-anything-at-all_B` (8), `is-the-null-key-result-one-draw-or-a-distribution_cloud` (3),
`the-on-share-column_cloud` (2), `pre-register-K_CAGR-as-the-rule-8-default_cloud` (1),
`is-the-sharpe-cagr-reversal-a-PANEL-property_C` (1).

## 2. The trap this run had to fix first (method finding)

The record's `fail4b`/`f4b` column carries **two incompatible semantics** and no artefact says which:
a **SET** of every failing bar, or the **FIRST** failing bar from a short-circuit `elif` chain
H1→H2→OOS→DD→CAGR (e.g. `2026-09-07_back-fill-the-mean-name-count-column..._B.py:249`). A
single-token value is ambiguous between the two — and single-token values are exactly what a
sole-binding count is made of. 29 artefacts / 25 runs never emit ≥2 tokens and are therefore
unreadable as sets; they are excluded from the headline. Reconstructing their 25 single-token
"OOS" rows from their own numbers against this run's measured per-panel SPY gives the true sets
`DD,OOS` ×22, `DD` ×2, `OOS` ×1 — i.e. **reading the FIRSTFAIL column as a set would have
overstated sole-OOS by 25×**. Cross-tier gates on files publishing two readings agree at 1.0000
(G2 27,096 rows; G3 208 rows; G4 715 rows).

## 3. Is the leg redundant, or merely rarely decisive?

Not redundant — rarely decisive, and asymmetrically so. The OOS bar **fails in 53.6% of all
failures**, the same order as H1 (54.3%) and H2 (58.5%); it is just almost never the *last bar
standing*, because DD and CAGR cut 45,439 + 77,425 rows on their own. P(OOS fails | H1 and H2 both
pass) = 0.0020 (380 of 194,529): the leg does carry information the halves do not.

The **bar-subset ladder** (parameter 2, all 16 grid points in `.subsets.csv`) shows soleness is a
property of the *conjunction*, not of the leg: sole-OOS 46 (FULL) → 126 (drop CAGR) → 299 (drop DD)
→ 380 (Sharpe-only). Remove the two aggressive bars and the OOS leg decides 8× more often.

## 4. Live leg (PROTOCOL rule 8, both KEEP paths)

39 pre-registered books, 3 panels × (top-n momentum n∈{5,10,20,30,40} × gross {0.75,1.00}, EWall ×2,
RULES v2 band), 10 bps, weekly, next-day. **4a 0/39, 4b 0/39. Sole binding bar: DD 22, CAGR 2,
OOS 0.** DD fails on 36 of 39. Rule 8 (n chosen on IS ≤2016-12-31, read once on 2017-01-01..):
picks top5/top5/top10/top10/top30/top30, OOS Sharpe 1.0584 / 1.0615 / 0.8493 / 0.8548 / 0.6696 /
0.6706 vs RULES v2 OOS 1.2817 (U56) / 1.1185 (B136) / 0.6629 (SMALL) and SPY OOS 0.8786 / 0.8820 /
0.8820 — beats the baseline 2/6, beats SPY 2/6, mean regret −0.1574, 4b 0/6.

## 5. Recommended PROTOCOL wording — DRAFTED, NOT APPLIED

PROTOCOL.md is untouched (rule 6: rules change only via Sunday review). Proposed amendment to
rule 4b, for the Sunday reviewer to accept or reject:

> The five 4b bars are **not independent tests**. Over the committed record the OOS leg is the sole
> binding bar in 47 of 399,086 re-readable failures (0.00012, 7 of 236 runs) while the drawdown cap
> and CAGR floor cut 11.4% and 19.4% on their own. Report the **failing-bar SET**, never the first
> failing bar, and never claim a 4b verdict was "confirmed out of sample" when the OOS leg was not
> the binding one.

And a companion clause for artefacts:

> Any committed artefact publishing a `fail4b`/`f4b` column MUST publish the complete failing-bar
> SET (a short-circuit `elif` first-fail is not a set and is not re-readable), or publish the five
> signed margins `m_H1..m_CAGR` instead.

## 6. Caveats

* The LEADERBOARD tier can only bound: rows publish no OOS number, so at most 611 of 1,811
  numerically-parseable headline rows could have been decided by the OOS leg alone (the other 1,200
  were already cut by H1/H2/DD/CAGR before rule 8 ran). It is an upper bound, not a reading, and it
  uses the record's own U56 SPY (0.957/0.834/15.23%/−33.72%) for rows priced on other panels.
* Census tiers re-read committed numbers; they inherit whatever panel vintage each run used
  (idea 514) and are not re-priced here.
* SURVIVORSHIP: BROAD136 and SMALL439 are current-constituent lists, so live-leg LEVELS are
  optimistic; only contrasts are claimed.
