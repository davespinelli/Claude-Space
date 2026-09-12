# Idea 609 — is the TWIN ORDERING window-invariant on a ROLLING census?
**cloud lane, 2026-09-12. ANSWERED = NO, AND BY A WIDER MARGIN THAN 605's TWO-HALF CAVEAT SUGGESTED. The published order QROLL > QEXP > ABS is what a reader would have seen in 32.2% of rolling 3-year windows — and it is "modal" only by a 19–19 tie. KILL for capital on the claim; one post-hoc 4b KEEP-CANDIDATE falls out as a by-product, memo filed, NOT proposed (rule 6). No RULES/PROTOCOL edit.**

Script `2026-09-12_is-the-TWIN-ORDERING-window-invariant-on-a-ROLLING-census_cloud.py`.
RULES.md, PROTOCOL.md, research/scan.py, products/bot/bot.py and research/baseline.py untouched.

## 0. A reproduction finding this run had to make first, and publishes
The gate is per-panel and **it does not all pass**, which is itself the first result:

| gate | result |
|---|---|
| G1 vectorised runner ≡ `engine.backtest` | 0.000e+00 → PASS |
| G2 fast CAGR/Sharpe/MaxDD ≡ `engine.metrics` | 0.000e+00 → PASS |
| G3 0.01-grid twin interpolation vs an EXACT run at g = 0.6237 | \|ΔSharpe\| < 1e-6 → PASS |
| **G4a U56 win rates ≡ idea 605's committed cells** | **exact at all 3 rungs, 0 verdict flips in 216 arms** → PASS |
| G4b B136 win rates | 0 flips at 0 bps, **2/216 at 10, 3/216 at 25**, every flipped arm inside \|dSharpe\| ≤ 2.5e-03 → reported, not tolerated |
| **G4c SMALL439** | **FAIL — THE PANEL NO LONGER EXISTS** |
| G4d the ORDER reproduces on today's panels | PASS on POOLED3 at 0/10/25 bps |
| G5 a window covering the whole sample ≡ the full-sample win rates | exact → PASS |

**Idea 605 ran SMALL439** (440 columns, 439 names after dropping 44 with `max_1d_move ≥ 1.0`). The
committed small panel today is **716 columns / 715 names / 52 dropped / 663 left** — it GREW
between 2026-09-10 and today. No tolerance can join those rows: it is a different panel. **So idea
605's POOLED win-rate LEVELS are not reproducible today**, and this run says so rather than quietly
re-deriving them. U56's are, exactly; B136's to 2–3 knife-edge arms inside the weekly
`prices_broad.csv` refresh (idea 406's known drift).

**A second reproduction finding, and the sharper one:** on **REPRO2** — the two panels that DO
reproduce — **ABS and QEXP are EXACTLY TIED** at 0 bps (0.6389 / 0.6389) and at 10 bps (0.6111 /
0.6111). 605's published THREE-WAY order is carried by the panel that no longer exists: drop SMALL
and the bottom two families are not ordered at all at PROTOCOL's own rung. Only at 25 bps does ABS
separate downward. Reported here, not broken by a tie-break rule.
The headline pooled scope is therefore **POOLED3**, fixed by a rule stated before any rolling number
is read — the pooled scope on which the published order is both **well-defined (no tie)** and
**reproduced** at 10 bps — with REPRO2 printed beside it at every grid point and every hypothesis
re-read on it.

## 1. The answer the queue asked for
Rolling **756-day (3-year)** windows stepped **63 days**, 10 bps, FULLMATCH, POOLED3, **59 windows
2009-01-13 → 2026-07-27**:

| order | windows | share |
|---|---|---|
| **QROLL > QEXP > ABS** (the published order) | **19** | **32.2%** |
| QROLL > ABS > QEXP | **19** | **32.2%** |
| QEXP > QROLL > ABS | 18 | 30.5% |
| TIED | 2 | 3.4% |
| ABS > QROLL > QEXP | 1 | 1.7% |

**So the published order is the one a reader would have seen in under a third of windows, and it is
"modal" only by a 19–19 tie with QROLL > ABS > QEXP.** H_MAJORITY's PASS is a coin flip and is
reported as one. The strong leg alone (QROLL on top) holds in **64.4%**; the exact inversion in
**0.0%**; the median Spearman against the published order is **+0.500**, not +1.000. Per-family win
rate over the census: ABS median 0.407 [0.000, 1.000], QEXP 0.556 [0.056, 0.833], QROLL 0.731
[0.287, 1.000] — against full-sample 0.5926 / 0.6296 / 0.9491. **QROLL's window win rate is below
its own full-sample value in 53 of 59 windows**: the published level is not a typical window's, it
is close to the census maximum.

## 2. The tuned grid — all 20 points × 2 scopes printed
share_exact at step 63, POOLED3: **L=252 0.284 · 504 0.238 · 756 0.322 · 1008 0.273 · 1260 0.235**,
Spearman vs L **−0.500** (REPRO2 +0.800). **Longer windows do NOT converge on the full-sample
reading** — H_LMONO FAILS, and with it the idea that the full-sample order is a limit of the window
orders. share_exact never exceeds **0.312** at any of the 20 grid points on POOLED3 (max 0.257 on
REPRO2), so no choice of (L, step) rescues the claim. Step range by L: 252 **0.114**, 504 0.051,
756 0.055, 1008 0.013, 1260 0.006 — H_STEPFREE fails on the 1-year rung alone.

## 3. The reported axes
**Cost:** share_exact 0.271 / 0.322 / 0.305 at 0 / 10 / 25 bps — H_COSTINV PASSES, so 605's
cost-invariance of the order survives the rolling census as well as the full sample.
**Twin matching: this is the biggest single effect in the run.** Under **WINMATCH** — the twin's
gross re-matched on the window itself, which is what a reader holding only that window would build —
share_exact collapses to **0.102** (0.051 at 0 bps, 0.119 at 25), and share_bottom with it (0.627 →
0.102). H_MATCH FAILS by 0.220. **The published order is substantially an artefact of matching the
twin's gross on a sample the reader does not have.**
**Panels:** U56 0.254, B136 0.254, SMALL 0.264 — H_PANEL passes; the weakness is not one panel's.

## 4. PROTOCOL rule 8 on the claim
(L, step) chosen on the first half of the census by share_exact alone, read once on the second.
IS pick **L = 252, step = 21** (IS 0.262) → **OOS 0.310, \|Δ\| 0.048** — H_R8CLAIM passes *at the
level of the share*. **But the share-level pass hides an order-level flip that is total:** the IS
modal order is **QEXP > QROLL > ABS at all 20 of 20 grid points**, and the OOS modal order has
QROLL on top at **all 20 of 20**. `share_top` runs **0.056–0.250 in sample** against **0.550–0.950
out of sample**. 605's IS/OOS caveat (rho −0.500) reproduces and strengthens: **the published order
is the modal order in ZERO in-sample grid points, and the whole "QROLL on top" fact lives in the
post-2017 window.**

## 5. PROTOCOL rule 8 on the books + both KEEP paths (mandatory), 648 arms × 3 rungs
Dial chosen on IS by IS Sharpe alone, OOS read once. **4a: 3 of 648 at 0 bps, 0 of 648 at 10 bps,
0 of 648 at 25 bps** (rule-8 picks 4a 3 / 0 / 0 of 108). 4b: 305 / 141 / 44, of which **earned**
(own matched-gross twin FAILS 4b) 97 / 83 / 44; rule-8 picks passing 4b 42 / 18 / 8.
**SMALL gives 0 4b passes at every rung.** Median OOS CAGR / Sharpe / MaxDD at 10 bps by panel and
family are in §E of the console; U56 QROLL 12.89% / 1.216 / −15.76%, B136 QROLL 11.19% / 1.100 /
−16.78%, SMALL QROLL 4.38% / 0.375 / −31.86% — against **SPY OOS 15.33% / 0.877 / −33.72%** and
**RULES v2 OOS 9.47%/1.278/−12.05% (U56), 7.88%/1.106/−12.24% (B136), 3.75%/0.560/−13.89% (SMALL)**.
**Disclosure:** the single best earned 4b passer by OOS Sharpe (U56 QROLL q0.07 w252 d1.00 D g0.75,
OOS 1.447) clears the 4b CAGR floor by **0.015 pp** and was **not** the rule-8 IS pick for its cell.
It is a knife edge and is **not** promoted; 16 of the 83 earned passers sit inside 0.25 pp of the
floor and are flagged as a group.

## 6. Pre-registered hypotheses — 6 of 11 pass (POOLED3; REPRO2 re-reading printed beside)
PASS: H_REPRO, H_MAJORITY (*by a 19–19 tie*), H_NOINV, H_COSTINV, H_PANEL, H_R8CLAIM (*share level
only; the modal order flips IS→OOS at 20 of 20 points*).
**FAIL: H_HALF (0.322 vs the 0.50 bar — the queue's literal question), H_TOP (0.644 vs 0.80),
H_LMONO (Spearman −0.500), H_STEPFREE (0.114 at L=252), H_MATCH (0.322 vs WINMATCH's 0.102).**
On REPRO2, H_MAJORITY, H_HALF and H_TOP all FAIL as well.

## 7. What the record should do with this
1. **Stop quoting the three-way twin order at all.** It survives 32.2% of 3-year windows, is modal
   only by a tie, and on the two panels that still reproduce its bottom two families are exactly
   tied at PROTOCOL's own rung.
2. **Quote `QROLL on top` instead if anything is quoted** — 64.4% of windows, 0.0% inversions — and
   quote it with its window, because in sample it holds in 5.6–25.0% and out of sample in 55–95%.
3. **Every matched-gross twin claim in the record should state its matching sample.** FULLMATCH
   0.322 vs WINMATCH 0.102 is the largest axis in this run and it is not a cost or a window choice.
4. **`data/prices_small.csv` grew from 483 to 715 names between 2026-09-10 and 2026-09-12**, so no
   committed SMALL439 number in the record is reproducible today. This needs a panel-vintage stamp
   beside every small-panel claim.

## 8. By-product: one post-hoc 4b KEEP-CANDIDATE (memo filed, NOT proposed)
`2026-09-12_609_BYPRODUCT_MEMO.md`. **B136, QROLL q0.17 w252, depth 0.50, daily gate, g = 1.00**:
13.29% / **1.134** / **−15.19%**, halves 1.210 / 1.054, **OOS 13.33% / 1.190 / −15.19%** at 10 bps
against SPY 15.16%/0.886/−33.72% (OOS 15.33%/0.877/−33.72%) and RULES v2 OOS 7.88%/1.106/−12.24%.
**4b at 0, 10 AND 25 bps** (CAGR margin +4.20 / +2.67 / +0.41 pp; DD margin +5.17 / +5.04 / +3.90
pp). **Earned** — its own matched-gross twin (12.65%/1.021/−20.76%) fails 4b at every rung. It WAS
the rule-8 IS pick for its cell. Transports to U56 (13.43%/1.179/−15.42%, OOS Sharpe 1.329, 4b
passes); **fails on SMALL** (6.51%/0.514/−29.94%). **Fails 4a.** It is post-hoc with respect to
idea 609's question and is not proposed for any Sunday review.

## Caveats
SURVIVORSHIP: all three panels are current-constituent lists, so every LEVEL is optimistic and the
SMALL panel worst (`data/SMALL_PANEL_README.md`); 52 tickers with `max_1d_move ≥ 1.0` dropped, 663
left. The win rate is a within-panel agreement rate, which survivorship moves far less than levels.
Rolling windows overlap heavily — that is what a step ladder is for, and the step's own effect is
published (§2). A 1-year window is 252 days of one regime; no Sharpe or CAGR read off one is a
capital claim. The census is anchored on U56's calendar; a panel joins a window only with ≥ 80% of
L days in it, which is why SMALL carries 53 windows where the others carry 59.

## 9. Reconciliation with lane B's independent run of the same idea
Lane B ran idea 609 concurrently; this run was launched before its commit was visible. **The two
reconcile exactly once the convention is named, and the apparent gap between the headlines is that
axis and nothing else.** Lane B headlines the WINDOW-matched twin (**0.0847**) and reports the
FULL-matched reading at **0.3390**; this run headlines the FULL-matched twin (**0.322** on POOLED3)
and reports WINMATCH at **0.102**. Those are the same measurement under the same two conventions.
Both runs independently find 4a **0 of 648** at 10 bps, 4b **141–142 of 648** (this run reads
exactly 605's committed 141), and that `data/prices_small.csv` went **439 → 663** tradable names in
two days. New here: the per-panel reproduction gate localising the failure to SMALL439 (U56 is
exact); the **ABS ≡ QEXP exact tie on the two reproducing panels**; the 19–19 modal tie; the
**IS modal order QEXP > QROLL > ABS at 20 of 20 grid points**; and the by-product memo.

## Follow-ups filed
823 (stamp every committed small-panel claim with its panel vintage — 483 → 715 names in two days),
824 (re-price the record's matched-gross twin claims under WINMATCH, where this run's largest axis
lives), 825 (is `QROLL on top` an entirely post-2017 fact? — it holds in ≤ 25% of in-sample grid
points and ≥ 55% of out-of-sample ones at all 20).
