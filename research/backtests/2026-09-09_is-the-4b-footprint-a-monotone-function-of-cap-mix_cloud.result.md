# Idea 285 — is the 4b footprint a monotone function of cap mix? (cloud, 2026-09-09)

**ANSWERED / KILL of the question as posed. The footprint FALLS steeply and reliably in q but is
NOT a monotone function of it, and — the substantive finding — THERE IS NO SINGLE ADMISSIBILITY
CURVE, because which 4b bar binds is a function of the BOOK SIZE n, not of the cap mix. No RULES
change, no book promoted, no KEEP claimed; RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py
untouched.**

Script: `research/backtests/2026-09-09_is-the-4b-footprint-a-monotone-function-of-cap-mix_cloud.py`
(1,321 s panel loop, deterministic, seed 20260909, no network; `--reuse` re-reads the committed
`.arms.csv` for the analysis). Artefacts: `.console.txt`, `.arms.csv` (1,680 rows), `.curves.csv`,
`.firstbind.csv`, `.binding.csv`, `.walkforward.csv`.

## Design

Idea 276's MIX construction, rebuilt as idea 286 rebuilt it: **k = 40 names per panel**, a share
**q** drawn from the sub-$2B panel and 1−q from the large-cap **stock** pool (ETFs excluded), every
panel run on ONE common window (the small panel's 4,194 trading days, 2010-01-04 → 2026-09-04) so
the rungs are comparable; SPY joined as a benchmark column only.

Two tuned parameters, both reporting axes with every point published:
**q ∈ {0.00, 0.05, …, 1.00}** (21 rungs; idea 276 used 5) × **n ∈ {10, 20, 30}** (idea 276 used 10
and 20), **20 draws per rung** (idea 276/286 used 8) = **420 panels, 1,680 arm-rows**, plus `EWall`
as the un-ranked control and the live `RULES v2` book as the 4a comparand on each panel.
10 bps, weekly, next-day execution, 260-day warm-up skip, 75% gross.
All five 4b bars evaluated separately, the OOS bar by PROTOCOL rule 8 (IS ≤ 2016-12-31, 2017→end
read once).

**SURVIVORSHIP:** both ends of the ladder are current-constituent sets — the sub-$2B screen
(`data/SMALL_PANEL_README.md`, 44 `max_1d_move ≥ 1.0` names dropped first, 439 usable) and
`universe_broad.json` (100 non-ETF names). Every level here is optimistic; only the **contrast
across q** is claimed.

## 1. The ladder does what idea 276 said

Mean gate breadth falls **0.6810 → 0.3236** monotonically over the 21 rungs;
**Spearman(q, breadth) = −1.0000 exactly** (idea 286 measured −0.9801 on the 5-rung ladder).
SPY is identical on every rung by construction (0.8615 full, 0.8820 OOS), so nothing below is a
benchmark artefact.

## 2. Is the footprint monotone? NO — but it is steep

Joint 4b pass rate, q=0 → q=1, over 20 draws per rung:

| arm | q=0 | q=1 | Spearman(q, rate) | up-steps of 20 | monotone? |
|---|---|---|---|---|---|
| EWall | 0.35 | 0.00 | −0.920 | 2 | **no** |
| top10 | 0.10 | 0.00 | −0.709 | 4 | **no** |
| top20 | **0.70** | 0.00 | −0.941 | 3 | **no** |
| top30 | 0.50 | 0.00 | −0.794 | 1 | **no** |

**160 of 1,680 arm-rows (9.5%) clear 4b; 5 of 1,680 (0.30%) clear 4a.** The direction is not in
doubt — every bar on every arm has Spearman ≤ −0.71 and 20 of 24 are ≤ −0.85 — but at the 0.05
resolution the queue asked for, **no curve is monotone**: 1 to 7 of the 20 q→q+0.05 transitions go
the wrong way on every bar. At 8 draws per rung and 5 rungs (idea 276's grid) that noise is invisible;
at 21 rungs it is not. **"Monotone" is a 5-rung statement, not a property of the footprint.**

One published boundary moves: idea 276's "every 4b pass at q ≤ 0.5" becomes **q ≤ 0.60** here
(top20 and EWall each still pass on 1 of 20 draws at q=0.60). The 0.5 edge was a grid point.

## 3. The admissibility curve — where each bar first binds

First q whose pass rate falls below 50% (full 21-rung curves in `.curves.csv`, `.firstbind.csv`):

| arm | H1 | H2 | OOS | DD cap | CAGR floor | **binding order (earliest first)** |
|---|---|---|---|---|---|---|
| EWall | 0.50 | 0.05 | 0.25 | **0.00** | 0.50 | DDcap → H2 → OOS → H1/CAGR |
| top10 | 0.40 | **0.00** | 0.05 | **0.00** | 0.50 | H2/DDcap → OOS → H1 → CAGR |
| top20 | 0.55 | **0.30** | 0.35 | 0.85 | 0.35 | H2 → OOS/CAGR → H1 → DDcap |
| top30 | 0.55 | 0.20 | 0.35 | never | **0.05** | CAGR → H2 → OOS → H1 → (DDcap never) |

**This is the answer the queue was looking for and it is not the answer the queue expected.** The
five bars do not bind at one q; they bind in an order that **reverses across n**. At n=30 the CAGR
floor is gone by q=0.05 and the DD cap never binds at all (pass rate ≥ 0.60 at every rung, because a
30-name equal-weight book of a 40-name panel is barely concentrated); at n=10 and at EWall it is the
DD cap that is already binding at q=0, while the CAGR floor survives to q=0.50. **A published
"admissibility q" is therefore not a property of the cap mix — it is a property of (cap mix, book
size) jointly, and the record's per-panel verdicts have been reading one off the other.**

## 4. Which bar actually cuts — and one bar that never does

Among all 4b failures, the share failing on each bar / the share where it is the **SOLE** failure:

| arm | n_fail | H1 | H2 | OOS | DD cap | CAGR floor |
|---|---|---|---|---|---|---|
| EWall | 384 | 0.539 / 0.005 | 0.893 / 0.003 | 0.815 / **0.000** | **0.961** / 0.091 | 0.641 / 0.000 |
| top10 | 407 | 0.595 / 0.002 | 0.897 / 0.010 | 0.845 / **0.000** | 0.885 / 0.081 | 0.577 / 0.000 |
| top20 | 329 | 0.635 / 0.003 | **0.942** / 0.082 | 0.815 / **0.000** | 0.322 / 0.006 | 0.888 / 0.018 |
| top30 | 400 | 0.505 / 0.000 | 0.787 / 0.003 | 0.695 / **0.000** | 0.050 / 0.000 | **0.998** / 0.193 |

**The OOS bar is the sole binding bar in 0 of 1,520 failures — it never cuts anything H1 and H2 have
not already cut.** On this corpus PROTOCOL 4b's rule-8 leg is redundant given its two half-sample
legs (it is not redundant as a *discipline*, and this run does not propose deleting it — but it
should stop being counted as an independent test). The bar that does the cutting is the DD cap on
diffuse books (EWall, top10) and the CAGR floor on wide ranked books (top30), with H2 the most
frequently-failed bar everywhere.

## 5. Rule 8 and both KEEP paths

n chosen per draw on IS Sharpe (≤ 2016-12-31), read once on 2017 → 2026-09-04, all 21 rungs in
`.walkforward.csv`. Median across the 20 draws of each rung:

| q | pick 10/20/30 | OOS CAGR | OOS Sharpe | OOS MaxDD | EWall OOS | RULES v2 OOS | SPY OOS | beats v2 | beats SPY |
|---|---|---|---|---|---|---|---|---|---|
| 0.00 | .25/.15/.60 | 10.9% | **1.032** | −16.1% | 1.005 | 1.112 | 0.882 | 15% | **90%** |
| 0.25 | .40/.35/.25 | 10.5% | 0.903 | −18.8% | 0.851 | 0.994 | 0.882 | 20% | 60% |
| 0.50 | .20/.50/.30 | 7.4% | 0.719 | −15.7% | 0.760 | 0.847 | 0.882 | 25% | 15% |
| 0.75 | .30/.55/.15 | 5.0% | 0.504 | −20.6% | 0.494 | 0.673 | 0.882 | 20% | 0% |
| 1.00 | .20/.75/.05 | 1.7% | 0.215 | −28.0% | 0.147 | 0.520 | 0.882 | 0% | 0% |

Pooled over all 420 draws the rule-8 chooser **beats the live RULES v2 book OOS on 16.7% of draws
and SPY OOS on 32.4%; its picks clear 4b on 10.2% and 4a on 0.5%.** The median OOS Sharpe crosses
SPY's 0.882 between q=0.30 and q=0.35, and the *share* of draws beating SPY crosses 50% between
q=0.40 and q=0.45 — two different "where it stops working" answers from the same grid, which is the
same level-vs-rate distinction section 3 makes.

**No KEEP.** The top20 book's 70% 4b pass rate at q=0 is a 40-name large-cap random draw, i.e. idea
486's random-draw base rate restated on a different construction, not a new book; and 4a passes on
5 of 1,680 rows.

## Honest limits

- 20 draws per rung is 2.5× idea 276 but still gives a pass-rate standard error of ~0.11 at 50%;
  that is exactly why the up-steps in §2 exist, and the non-monotonicity claim is a claim about
  **what the record can resolve**, not a claim that the true curve wiggles.
- k=40 is held fixed at idea 276's value; the interaction found in §3 is (q × n), and (q × k) is
  untested.
- Both ends of the ladder are survivor sets, so the *level* of every pass rate is optimistic; the
  q-contrast is the claim.
- The 4a comparand is the live RULES v2 book **run on the same 40-name mixed panel**, not the live
  book on its own universe; 4a passes are 0.30% and the leg is barely exercised.
