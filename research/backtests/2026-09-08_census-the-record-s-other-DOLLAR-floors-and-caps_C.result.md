# Idea 428 — census-the-record-s-other-DOLLAR-floors-and-caps (lane C, 2026-09-08)

**Verdict: ANSWERED — and the premise is NEGATIVE. The record has no "other" dollar floors or
caps. The damaging form exists in exactly 2 of 379 committed scripts, and both are the SAME
construction: idea 121's `$1M` ADV floor in `band-gate-on-small-panel_B` and idea 425's own re-run
of it. Re-run backlog from this class: 17 LEADERBOARD rows, 9 of which idea 425 already priced.**

## The instrument (not a regex)

Idea 197's theorem says a mask leaks the adjustment channel iff it is not invariant under
T1 `px -> px @ diag(c)`. So the detector is a **homogeneity-degree analysis over the AST**:
`deg(px)=1`, `deg(share volume, returns, ranks)=0`, `deg(a*b)=deg(a)+deg(b)`,
`deg(a/b)=deg(a)-deg(b)`, rolling/median/shift/quantile preserve degree, `pct_change`/`rank`
return 0. A comparison is flagged iff one side is provably degree ≥ 1 **and traceable to a price
symbol** (origin tracking, so `px > ma` is exempt) **and** the other side resolves to a
dimensionless constant — a literal, a module constant, a numeric loop variable, or a parameter
every call site passes a number to. Cuts at level 0 are separated out: `px > 0` is exactly
T1-invariant.

Unknown symbols default to degree 0, which makes the detector conservative, so the run reports
three buckets and **adjudicates every hit outside the safe one** rather than quoting a bare count.

## Q1 — the census (379 scripts, 293 price-bearing comparisons)

| bucket | meaning | hits | files |
|---|---|---|---|
| B1 | absolute cut, level resolved | 3 | 2 |
| B2 | threshold the analyser could not resolve | 46 | 23 |
| B3 | price vs price (scale-covariant, e.g. `px > ma`) | 234 | 144 |
| Z | absolute cut at level 0 (T1-invariant) | 10 | 5 |

All 49 B1+B2 hits adjudicated, **0 unadjudicated**: DV_FLOOR 2 **DAMAGING**; RATIO_TOL 2,
TRAIL_STOP 11, MOVING_AVG 25, BLOCK_REF 1, OPT_MODEL 4, NOT_PRICE 4 — all SAFE (price vs price,
or not a price at all). The two B1 hits in `audit-every-published-key-for-the-adjustment-leak_B`
are a `1e-9` tolerance on a price/price **ratio** — degree 0 in truth, an analyser miss, not a leak.

**DAMAGING form: 2 of 379 files (0.53%)** — `2026-09-06_band-gate-on-small-panel_B.py:265` and
`2026-09-08_the-liquidity-FLOOR-is-in-the-eligibility-mask-not-a-tilt_C.py:231`, the identical
line `return m & (dv >= floor).fillna(False)`. **No market-cap floor, no notional cap, and no
price floor is used as an eligibility mask anywhere in the record.**

## Q2 — exposure

3,349 LEADERBOARD rows parsed; 173 sit under files the detector flagged at all, **17 under the
two DAMAGING ones** (9 in `band-gate-on-small-panel_B`, 8 in the idea-425 file). Idea 425 already
established that only 2 of those 9 are reachable by the floor and that neither changes a verdict.
**The re-run backlog this idea was written to discover is empty beyond what idea 425 already did.**

## Q3–Q5 — the ranking the QUEUE asked for (measured, not asserted)

Common support = live & all three keys finite: 1,364,963 of 1,368,684 SMALL439 ticker-days
(99.73%); 240,098 of 240,212 on U56 (99.95%). Matched-admission levels are **solved** from a
pooled-quantile identity (admission agreement ≤ 1.4e-4), never fitted to a return.

| construction | panel | level | gated share of live ticker-days |
|---|---|---|---|
| `(px*vol).rolling(20).median() >= $1M` | SMALL439 | 1,000,000 | **27.54%** |
| `vol.rolling(20).median() >= s*` (price-free) | SMALL439 | 69,650 sh | 27.53% |
| `px.rolling(20).median() >= $5` | SMALL439 | 5.00 | 13.15% |
| `px.rolling(20).median() >= $5` | U56 | 5.00 | 3.07% |

**P1 CONFIRMED**: the $1M ADV floor gates more than twice what a $5 price floor would, so if
PROTOCOL adopts idea 121's clause it becomes the record's single largest price-borne mask.

**P2 CONFIRMED, with one qualification.** At matched admission (16 cells per rung: 2 books × 2
conventions × 4 cost rungs), the price-free key beats **both** price-bearing keys in **64 of 64**
cells: VOLSH − DV **+2.610 pp CAGR / +0.163 Sharpe**, VOLSH − PXL **+3.179 pp / +0.182**. Idea
425's +1.23 pp is reproduced in shape and exceeded here because this grid runs the ladder out to
$5M. The qualification: DV − PXL **changes sign along the level ladder** (+1.39 pp at $0.5M,
+0.98 at $1M, +0.11 at $2M, −0.21 at $5M; 16/16 → 8/16 cells, +0.569 pp pooled over 64), so the
two price-bearing keys are
not interchangeable and "price-borne" is not one failure mode. SURVIVORSHIP: SMALL439 is current
constituents only and the delisted cohort sits exactly in the thin names a floor argues about, so
only floor-minus-floor contrasts are read here — no level, and no book is proposed on this panel.

## Q6 — rule 8 (level chosen on 2010–2016, 2017–2026 read once), 64 cells

| panel | instrument | beats no-floor OOS | beats SPY OOS | mean OOS Sharpe | no-floor | SPY |
|---|---|---|---|---|---|---|
| SMALL439 | DV | 0/16 | 0/16 | 0.398 | 0.587 | 0.882 |
| SMALL439 | VOLSH | 0/16 | 0/16 | 0.495 | 0.587 | 0.882 |
| SMALL439 | PXL | 0/16 | 0/16 | 0.282 | 0.587 | 0.882 |
| U56 | PXL | 0/16 | 16/16 | 1.087 | 1.160 | 0.882 |

The IS chooser beats the no-floor control in **0 of 64** cells (it picks the OOS-best *level* in
48/64 — the levels are ordered, the instrument is what loses). Mean OOS CAGR: pick 6.57% vs
no-floor 8.90% vs SPY 15.45%. **Every liquidity floor tested is a cost, not an edge, out of
sample, on both panels.**

## Q7 — both KEEP paths at 10 bps (72 points)

4a bars (RULES v2 @10 bps): H1 > 1.226, H2 > 1.191, MaxDD ≥ −12.05%. **4a KEEP 0/72.**
4b bars (U56 window): H1 > 0.957, H2 > 0.834, OOS > 0.882, MaxDD ≥ −20.23%, CAGR ≥ 10.66%.
**4b KEEP 1/72** — and it is the **no-floor control**, U56 / EWALL+MA200 / rw / 0.75 gross:
11.55% / 1.091 / −18.6%, halves 1.167 / 1.037. It **is not a new candidate**: it is a weekly,
de-grossed point of the family already committed as `2026-09-08_u56-ewall-magate-fullgross`
(monthly, full gross, 11.96%/1.2126/−15.49%), it is dominated by it on all three metrics, and it
**dies on the cost ladder** (25 bps: 10.28% CAGR, below the 10.66% floor → KILL(CAGR)). No memo:
adding one would put a strictly worse dial point beside the standing candidate. **P3 holds on
SMALL439** — 0 of 56 SMALL439 points clear 4b at any instrument or level.

## Reproduction gates (all bind before any new number was read)

`fast_bt` vs `engine.backtest` 6.9e-18 · SPY/SMALL439 14.13%/0.862/−33.7%, halves 0.891/0.858
(idea 425 published identically) · RULES v2 on U56 8.66%/1.2056/−12.05% (published identically) ·
RULES v1 on SMALL439 8.15%/0.603/−32.8% (published identically) · the flagged construction rebuilt
here admits 991,742 of 1,364,963 support ticker-days (72.6571%).

## What the record should do

1. **Nothing to re-run.** The class idea 428 hypothesised does not exist beyond the one file idea
   425 already priced. Ideas that assumed a backlog of dollar floors and caps should be re-scoped.
2. **The detector is reusable.** `scan_file()` in this script is a standing certificate: it reads
   the whole corpus in ~2 s and reports 0 unadjudicated hits. It is a better instrument than idea
   193's Spearman (killed) and idea 197's regex census (7 false-positive-prone hits).
3. **If PROTOCOL adopts idea 121's ADV clause** (idea 427's question), it should be written on
   share volume, not dollars: at matched admission the dollar key costs 2.61 pp CAGR in 64/64
   cells, and it would be the record's largest price-borne mask at 27.5% of ticker-days.

Grid 288 points · walk-forward 64 cells · verdicts 72 points · census 293 comparisons · runtime 113 s.
