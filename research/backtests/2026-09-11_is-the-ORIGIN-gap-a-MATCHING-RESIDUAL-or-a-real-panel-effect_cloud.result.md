# Idea 570 (cloud, 2026-09-11) — is-the-ORIGIN-gap-a-MATCHING-RESIDUAL-or-a-real-panel-effect

**ANSWERED: it is a REAL PANEL EFFECT, not a matching residual — idea 568's premise CONFIRMED,
and this is the most OOS-stable cross-panel result in the record.** An exact one-to-one
name-level match drives the B/S characteristic residual from idea 568's **0.1290 to 0.0003–0.0052**
(name-level 0.0003–0.0024), a 25–400× reduction, and the origin gap **does not shrink — it holds at
+0.165 to +0.302 (t +8.9 to +29.6), inside its own seed sd on 0 of 8 tight points**, and it holds
sign IS vs OOS at **18 of 18** grid points. **KILL for capital all the same:** the single 4b passer
is the record's existing whole-B136 MA-RS gate at ρ = **0.9987**, strictly worse than it on every
metric. No new KEEP, no memo, no rule change; RULES.md, PROTOCOL.md, scan.py, bot.py and
baseline.py untouched (rule 6).

SELECTION: taken as the LAST eligible open idea in QUEUE.md (the tail of the Open list is annotated
SKIP/PARK/LOCAL-ONLY by earlier lanes); 570 mentions no EDGAR / Form 4 / 8-K / options / spin-offs /
live data.

Script `2026-09-11_is-the-ORIGIN-gap-a-MATCHING-RESIDUAL-or-a-real-panel-effect_cloud.py` · 5,184-book
matched grid + 288 matched panel-pairs · 10 bps · next-day fills · IS ≤ 2016-12-31, OOS ≥ 2017-01-01
read once · 219s.

## Gates (pre-registered, printed before any exactly-matched number was read) — ALL PASS

| gate | object | result | bar |
|---|---|---|---|
| G2 real panels | the three real panels' 36 REAL rows (13 columns) rebuilt from prices vs idea 312/568's committed grid | B136 **2.22e-16**, SMALL439 **2.22e-16**, U56 2.12e-06; published premia re-read U56 −0.0045 / B136 −0.0465 / SMALL439 −0.1023, **gap +0.0978 exactly** | 1e-9 (U56 1e-4) |
| G3 identity | `fast_backtest` vs `engine.backtest` | **1.388e-17** | 1e-12 |
| G4 pool | the pooled frame vs idea 568's committed console | **2010-01-04…2026-09-04, 4194 bars, B 134 + SMALL 439 = 573 names — exact** | exact |
| G1 kernel repro | idea 568's committed `.origin.csv` (achieved_B, achieved_S, prem_B, prem_S, gap, sd_pair, t) rebuilt here from its own seeding scheme and price source | **1.776e-15** over 3 rows × 7 columns — an independent cross-lane reproduction; its 0.1290 residual re-read exactly | 1e-9 |

**Minor defect found in the record (numbers unaffected):** idea 568's committed docstring states
*"Pool = 135 B136 tradables + 439 SMALL tradables = 574 names"*. Its own console — and this
reproduction — say **134 + 439 = 573**: one B136 name carries no characteristic and is dropped by
`name_chars`. The prose was never reconciled with the run. Every published rung used the 573-name
pool, so no committed number moves.

## The exact match (the thing idea 568 could not do)

For each seed the B names are visited in a seeded random order and each takes its **nearest unused**
S partner on the characteristic, accepted only if |x_b − x_s| ≤ τ; the first k pairs are kept. No
name is reused on either side, so the two panels are equally wide and carry the same characteristic
distribution up to τ.

Dials (PROTOCOL rule 4, exactly two, as the queue specifies): **τ ∈ {0.01, 0.02, 0.05, ∞}** ×
**k ∈ {18, 36, 72}** — all 12 points reported, for both characteristics. Reported never selected:
characteristic {cvol, breadth}, gross {0.50, 0.75, 1.00}, cadence {W, M}, 12 seeds, period.

Match quality, against idea 568's 0.1290:

| char | τ | k | achieved B | achieved S | **panel residual** | name residual |
|---|---|---|---|---|---|---|
| cvol | 0.01 | 36 | — | — | **0.00034** | 0.00034 |
| cvol | 0.02 | 36 | — | — | **0.00141** | 0.00141 |
| breadth | 0.02 | 36 | 0.6057 | 0.6080 | **0.00322** | 0.00242 |
| breadth | 0.01 | 36 | 0.6016 | 0.6060 | **0.00522** | 0.00050 |
| (loosest) any | ∞ | 72 | — | — | 0.0835–0.0856 | 0.0835–0.0876 |

**H_EXACT HOLDS.** k = 72 is infeasible at every finite τ (at most 52 pairs exist within 0.02 and 62
within 0.05 on cvol) — reported, not dropped.

## The answer: origin survives an exact match

| char | τ | k | residual | prem B | prem S | **gap** | sd_pair | **t** | inside sd | × GAP_PUB | × KERNEL |
|---|---|---|---|---|---|---|---|---|---|---|---|
| cvol | 0.01 | 18 | 0.0006 | −0.0683 | −0.2332 | **+0.1649** | 0.0640 | +8.92 | No | 1.69 | 0.65 |
| cvol | 0.01 | 36 | 0.0003 | −0.0140 | −0.2687 | **+0.2547** | 0.0312 | +28.27 | No | 2.60 | 1.00 |
| cvol | 0.02 | 36 | 0.0014 | −0.0145 | −0.2767 | **+0.2622** | 0.0405 | +22.45 | No | 2.68 | 1.03 |
| breadth | 0.01 | 36 | 0.0052 | +0.0226 | −0.2528 | **+0.2753** | 0.0323 | +29.57 | No | 2.82 | 1.09 |
| breadth | 0.01 | 18 | 0.0049 | −0.0428 | −0.3450 | **+0.3021** | 0.0819 | +12.79 | No | 3.09 | 1.19 |
| … all 18 points | | | | | | **+0.165 … +0.302** | | **+7.6 … +48.6** | **0 of 18** | 1.69–3.09 | 0.65–1.19 |

**H_RESID FALSIFIED.** At τ ≤ 0.02 the gap is inside its own seed sd on **0 of 8** points. The
residual is gone and the gap is not.

**H_MONO FALSIFIED** (2 of 6 ladders). Tightening τ does not shrink the gap — it usually **grows** it:
cvol k=36 runs +0.2199 (τ=∞) → **+0.2547** (τ=0.01); breadth k=36 runs +0.2327 → **+0.2753**. The
residual was working *against* the finding, exactly as idea 568 argued from a slope it also called
noise — this run establishes it by construction instead of by inference.

## Rule 8 walk-forward

**WF-A** — the exactly-matched gap re-read on IS-only and OOS-only returns at all 18 points: **sign
holds 18 of 18**; mean gap **FULL +0.2396 / IS +0.2551 / OOS +0.2357**. That is the flattest IS→OOS
cross-panel statistic anywhere in this record's cross-panel line (compare idea 567's three-panel span,
which collapsed 0.2017 IS → 0.0645 OOS). The two characteristics disagree on *which* half is larger —
breadth IS +0.30…+0.45 vs OOS +0.14…+0.28, cvol IS +0.03…+0.25 vs OOS +0.22…+0.36 — so the *level* is
a characteristic statement even though the sign is not.

**WF-B** — priced as a book: pick (char, τ, k) by IS Sharpe of the seed-pooled B-side MA-RS book at
g = 0.75/W, OOS read once. The IS surface picks **breadth, τ = ∞, k = 72** — the **loosest-matched**
point on the grid, which is itself the answer to whether the match helps a book.

| book | CAGR | Sharpe | MaxDD | OOS CAGR | OOS Sharpe | OOS MaxDD | 4a | 4b |
|---|---|---|---|---|---|---|---|---|
| B-side (IS pick) | 10.67% | 1.0171 | −19.92% | 11.28% | 1.0258 | −19.92% | False | **PASS** |
| S-side twin | 7.19% | 0.6146 | −30.07% | 6.80% | 0.5586 | −30.07% | False | H1,H2,OOS,DD,CAGR |
| ORIGIN-BLIND control | 9.32% | 0.8832 | −22.28% | 9.63% | 0.8719 | −22.28% | False | H2,OOS,DD,CAGR |
| **INCUMBENT B136 MA-RS g0.75 W** | **11.20%** | **1.0450** | **−20.12%** | **11.97%** | **1.0660** | −20.12% | False | **PASS** |
| SMALL439 MA-RS g0.75 W | 6.48% | 0.5034 | −38.24% | 7.38% | 0.5355 | −38.24% | False | H1,H2,OOS,DD,CAGR |
| **RULES v2 U56 (live book)** | 8.66% | **1.2056** | **−12.05%** | 9.53% | **1.2851** | −12.05% | — | CAGR |
| SPY | 15.23% | 0.8890 | −33.72% | 15.45% | 0.8820 | −33.72% | — | H1,H2,OOS,DD |

**Books beating RULES v2 OOS Sharpe: 0 of 3. Beating SPY: 1 of 3.**

## KEEP paths — and why the one 4b pass is not a candidate

Full matched grid **5,184 books**: **4a 21/5184, 4b 244/5184, BOTH 1/5184.** By side: B 4a 6 / 4b 225,
S 4a 15 / 4b 19 — the origin asymmetry again. Binding legs: DD 1728, CAGR 460.

The WF-B B-side book clears 4b. It is **not a new candidate**: its daily returns correlate **0.9987**
with the whole-B136 MA-RS gate at the same gross and cadence — a book the record already holds and
which idea 778 re-found the same day as a REAL 4b passer — and it is **strictly worse** than that
incumbent on CAGR (10.67% vs 11.20%), Sharpe (1.0171 vs 1.0450) and OOS Sharpe (1.0258 vs 1.0660). It
is the incumbent with 62 of its 134 names deleted by a seeded matcher. Against the live book it gives
up **0.26 of OOS Sharpe for 7.9 pp more drawdown** and fails 4a.

**NO KEEP-CANDIDATE, NO MEMO, NO RULES CHANGE.**

## What this does and does not establish

It establishes that at an exact characteristic match, on two characteristics, at every tolerance and
every k, and in both halves, **B136-sourced names carry a larger MA-gate selection premium than
SMALL439-sourced names by 1.7–3.1× the published U56−SMALL439 gap**. It does **not** establish *why*.
The design controls the characteristic; it does not control **differential survivorship** — the small
panel is a current-constituent screen and carries more survivorship premium than the large-cap panel,
and a differential survivorship effect would produce exactly this sign. That alternative cannot be
excluded from committed data and is the first thing a KEEP would have to answer.

## Survivorship

`universe_broad.json` and the small panel are **current constituents**. The premium is an arm-minus-arm
difference on the *same* panel, so the level bias largely cancels *within* a panel — but the B-minus-S
**origin** gap does **not** cancel it, and that is the live alternative explanation stated above. The
small panel drops every ticker with `max_1d_move ≥ 1.0` (439 of 483 kept). Pooled window
2010-01-04…2026-09-04, read from 2011-01 after the 260-bar warm-up — 15.7 years, PROTOCOL rule 1
satisfied.

## Follow-ups proposed

782. **price the ORIGIN gap against a SURVIVORSHIP-MATCHED small panel** — idea 570 shows origin
survives an exact characteristic match at 1.7–3.1× the published gap, but the only uncontrolled
channel left is that SMALL439 is a current-constituent screen with more survivorship premium than
B136. Match on listing-history length or first-bar date as well as the characteristic and report
whether the gap survives. Max 2 params (history bucket, k).

783. **is the ORIGIN gap a LIQUIDITY gap** — the B/S contrast at matched cvol and matched breadth is
still a contrast in dollar volume by two orders of magnitude, and the MA gate trades on it. Re-run
idea 570's exact match on `volume_small` where available and report the gap at matched turnover. Max
2 params (volume statistic, k). NOTE: needs a broad/u56 volume cache (see parked idea 429) — local or
Actions, not cloud.

784. **does the ORIGIN asymmetry show up in 4b PASS RATES, not just the premium** — this run's matched
grid passes 4b on 225 of 2,592 B-side books against 19 of 2,592 S-side books at identical
characteristic and identical width, an 11.8× asymmetry nobody has priced. Ask whether that pass-rate
gap is the premium gap re-expressed or an independent drawdown fact. Max 2 params (bar, k).
