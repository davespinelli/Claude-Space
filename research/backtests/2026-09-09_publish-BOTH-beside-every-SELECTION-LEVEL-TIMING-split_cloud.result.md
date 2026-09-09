# Idea 558 — publish BOTH beside every SELECTION/LEVEL/TIMING split (cloud, 2026-09-09)

**Answer: 103 of the record's 162 distinct published SELECTION numbers (63.6%) are majority-BOTH.
Over the 378 committed rows, 250 (66.1%). None of the committed files publishes BOTH.**

## What was audited

A mechanical scan of all 2,429 committed CSVs in `research/backtests` for a header carrying
`sel_pp` AND `level_pp` AND `timing_pp` finds the record's SELECTION/LEVEL/TIMING split in
exactly **2 files**:

| file | rows | distinct cells |
|---|---|---|
| `2026-09-09_does-the-uncompensated-residual-finding-replicate-off-SMALL439_B.pairs.csv` (idea 305) | 324 | 162 |
| `2026-09-06_does-a-pure-exposure-gate-exist-on-the-small-panel_C.matched.csv` (idea 51R) | 54 | 27 |

The 54 rows of the second file are an **exact subset** of the first file's SMALL439 / QUANTILE-M
rows (max |d| 8.9e-16), and the `con` dial duplicates every SELECTION number by construction, so
378 committed rows carry **162 distinct** numbers.

## The finding

`SELECTION = ADD + DROP + BOTH + Jensen`, where BOTH is the shared-names weight gap that the
MEAN-based depth match leaves open. Majority-BOTH is pre-registered as `|BOTH| > |SELECTION|`.

- **103/162 = 63.6%** majority-BOTH; mean |BOTH|/|SEL| **3.819**, median **1.222**; BOTH is
  **32.0%** of |ADD|+|DROP|+|BOTH|.
- Dominant-BOTH (BOTH the largest of the three legs) is only **35/162 = 21.6%** — the leg is
  usually not the biggest, it is just bigger than the *net* number published.
- By panel: U56 51.9%, B136 55.6%, **SMALL439 83.3%**.

## The mechanism — a depth fact, not a panel fact

`rank rho(|BOTH|/|SEL|, x) = -0.4573` over 162 cells, and panel dummies cut the residual SD of
`log(|BOTH|/|SEL|) ~ x` by **0.6%** (bar 25%). **H_DEPTH holds on both legs.** By theta:

| theta | x | overlap | majority-BOTH |
|---|---|---|---|
| +0.12 | 0.257 | 0.791 | 18/18 = 100% |
| +0.06 | 0.433 | 0.838 | 18/18 = 100% |
| -0.12 | 0.856 | 0.955 | 6/18 = 33% |
| -0.25 | 0.936 | 0.983 | 6/18 = 33% |

The mismatch channel closes as the two slices converge. **H_CAD fails** (Q 75.9% / W 59.3% /
M 55.6%, worst |rate − pooled| 0.123 > 0.10).

## Gates — all six pass

G1 zero-cost identity 9.7e-17 (486 books) · G2 three-leg identity 1.4e-16 (486 cells) ·
G3 the record's own `SEL+LEVEL+TIMING = dCAGR0_dg` 2.7e-15 (324 rows) ·
R1 idea 305's 324 rows × 9 cols worst 3.6e-15 · R2 idea 51R's 54 rows worst 8.9e-16 ·
R3 idea 556's 162 cadence-W leg rows worst 1.8e-15.

## Rule 8

The per-cell majority-BOTH **label is not stable**: chosen on IS it agrees OOS only 96/162
(59.3%); the dominant leg agrees 67.3%, the SELECTION sign 72.2%, and the rate itself moves
43.2% IS → 65.4% OOS. So the reportable finding is the **pooled rate and the depth ordering**,
not any one cell's label. WF-B (best IS Sharpe per panel, OOS read once) beats SPY OOS 3/3 but
**RULES v2 0/3**. WF-C's IS-fitted depth model beats neither the IS mean nor zero on 0/4 panels.

## KEEP paths

4a **1/486**, 4b **20/486**, BOTH **0/486**. The lone 4a passer (U56 QUANTILE-M/DEGROSS
theta +0.06 M, CAGR 7.02%, Sharpe 1.2364, MaxDD −9.20%) fails 4b on CAGR; every 4b passer is a
U56/B136 book already in the record. DD is the modal blocker (203/486 fail on DD alone).
**No book promoted.**

**SURVIVORSHIP:** B136 and SMALL439 are current constituents of their screens only; every CAGR
level is biased up and the 4a/4b columns are not immune. The legs are same-panel arm-minus-arm
differences, so the bias very largely cancels there, but ADD is exactly the side survivorship
flatters most.

## What this means for the record

Every SELECTION number the record has published is a "which names" claim that is, in ~2 cases
out of 3, smaller than a leg that is not about which names are held at all.

**Cross-reference (idea 559, lane C, same day):** the obvious repair — pin `k_q` to `k_ma`
*daily* so BOTH is zero by construction — does not rescue the split, it collapses it. Because
`MA-THRESH` admits exactly `{dist > theta}` and idea 305's quantile control ranks on that same
`dist`, a daily match returns the identical gate and the contrast vanishes. Read together, the
two results say the same thing from opposite ends: **the depth mismatch was the contrast.** The
`|BOTH|/|SEL|` ordering measured here — 100% majority-BOTH at overlap 0.79-0.84, 33% at overlap
0.95-0.98 — is the continuous version of 559's discrete collapse, and it is why the ratio rises
as the match loosens rather than falling.
