# Idea 268 — do-the-18-majority-reversing-files-have-reversing-HEADLINES (cloud, 2026-09-06)

**Verdict: ANSWERED / the queue's worry is almost entirely unfounded, with exactly one real hit.
Of 48 HEADLINE sentences across the 11 parents of idea 259's 18 majority-reversing files, **0**
change once the CAGR column is beside them. One published sentence in the record does change,
and it is a **LEADERBOARD row**, not a headline: idea 262's rule-8 ordering `EWALL 1.073 >
FWD20 0.987` on OOS Sharpe reverses to `FWD20 13.4% > EWALL 11.4%` on OOS CAGR. The reason the
files are 62% reversing while the sentences are not is structural and is confirmed by a clean
re-run: the reversal lives **only in the between-book carrier axis** (25/40 pairs reverse,
62.5%) and **never in the within-book dial delta** (0/64, including 0/28 where the dial has real
Sharpe content) — and the dial delta is the statistic every one of those 11 headlines asserts.
No RULES change, no KEEP-candidate, no new book.**

Script: `research/backtests/2026-09-06_do-the-18-majority-reversing-files-have-reversing-HEADLINES_cloud.py`
Outputs: `.audit.csv`, `.sentences.csv`, `.files.csv`, `.grid.csv` (80 points), `.carrier.csv`,
`.overlay.csv`, `.walkforward.csv`, `.console.txt`. 10 bps, weekly, next-day execution; 0 bps
carried as a diagnostic column only.

---

## Leg A — the sentence audit (the queue's literal ask)

Idea 259's committed census re-derives cleanly: **91** files carry RANKED EWall pairs, **18**
have a majority reversing (share 0.55–1.00). Those 18 files map to **11 distinct PARENT
scripts** — every one of ideas 91, 99, 102, 109, 112, 113, 114, 115, 116, 133, 262 — because a
parent commits several CSVs (`.grid`, `.picks`, `.walkforward`) off the same run.

Pre-registered before any prose was read: HEADLINE = title line + everything before the first
`##`; a sentence is a *comparative EWall-vs-ranked claim* iff it carries an EWall token AND a
ranked-book token AND a comparative verb/operator; a claim CHANGES iff it is stated on Sharpe (or
unqualified) and its backing pairs reverse in a majority of cells.

| block | sentences | EWall-mentioning | comparative claims | **adjudicated to change** |
|---|---|---|---|---|
| HEADLINE | 48 | 5 | 1 (mechanical) | **0** |
| BODY | 439 | 22 | 1 (mechanical) | **0** |
| LEADERBOARD rows | 156 | 9 | 2 (mechanical) | **1** |

The two mechanical hits that do **not** survive adjudication, stated so the regex's failure is
visible rather than hidden:
* idea 91 HEADLINE — *"…the band-parameterised weight builder equals idea 84's three fixed books
  at 0 differing cells (band 3% → C57/ew-band3; band 0 → C72/EWall and C2/CAND20); `run` vs
  `engine.backtest` max|diff| = 0.0…"*. This is a **reproduction check**, not a comparison; the
  `vs` belongs to `run` vs `engine.backtest`. Not a claim about which book wins. **Stands.**
* idea 262 BODY — *"…gross matched at 0.75 on every arm including EWall, n ∈ {20,30,40,60}…"*.
  A construction description. **Stands.**

The one that **does** change, found in the LEADERBOARD block and confirmed against the parent's
own committed `.walkforward.csv` rather than re-derived:

> idea 262, 2026-09-06: *"OOS Sharpe at 10 bps: EWALL **1.073** > ALL_ISARGMAX 1.069 > … >
> FWD20 0.987 > … > SPY 0.882"*

On OOS **CAGR** at the same 10 bps rung the order between those two arms inverts: FWD20 **13.38%**
> EWALL **11.40%** (SPY 15.45%). The sentence is true as written and false in ordering the moment
the CAGR column is beside it — exactly idea 259's one-directional pattern (EWall buys Sharpe by
giving up CAGR). It is a *reporting* defect in one row, not a wrong verdict: idea 262's actual
verdict was about breakeven costs and does not rest on this ordering.

**Why 62% of rows and 0% of headlines.** In 10 of the 11 parents `ewall` is a **carrier** — a
second base book dragged through an overlay study (sleeve, band, breadth, stop, crypto, gross)
so the overlay's effect can be measured on two constructions. The census pairs the carrier
against `top20` at every value of the dial, which is 64 of 104 rows in the shared harness; the
headline is always about the **dial**. Nobody published the carrier comparison.

## Leg B — controlled re-run (two 2-parameter grids, 80 points, all reported)

One construction (weekly, t+1, 10 bps, gate = above-200d AND vol20 < 0.60, key = composite
without the vol scaler), arms `EWall` (every eligible name, equal weight) and `TOP20`, on
4 panels × 2 dials swept separately: **grid G** gross ∈ {0.55,0.65,0.75,0.85,1.00} at band 0;
**grid B** 200d re-entry band ∈ {0,2,3,5,8}% at gross 0.75. Nothing is picked across the grids.

*Harness reproduction:* `B136 / EWall / g0.75 / 10 bps` returns **10.7% / 1.026 / −17.7%,
OOS 1.019**, identical to ideas 10, 82 and 259's published row. `U56 / TOP20 / g0.75` returns
12.8% / 1.064 / −18.3%, the standing 4b candidate's construction.

| test @10 bps | reversing | note |
|---|---|---|
| **CARRIER** — EWall − TOP20 at fixed (panel, dial, rung) | **25 / 40 = 62.5%** | EWall wins Sharpe in 25/40, CAGR in **0/40**; conditional on winning Sharpe it loses CAGR **25/25** |
| **DIAL delta** — metric(v) − metric(v_ref) *within* a book | **0 / 64 = 0.0%** | grid G 0/32, grid B 0/32 |

Paired over grid B (the non-degenerate dial): dSharpe **+0.0403, t +2.53** (15/20 positive),
dCAGR **−0.0166, t −13.04** (0/20 positive). The carrier reversal is not marginal — it is the
same one-directional effect idea 259 measured, at 100% conditional rate on this clean grid.

The dial result needs one honest caveat: on **grid G** the reversal count is 0/32 *by
construction* — gross is a pure lever with no Sharpe content (|dSharpe| ≤ 0.0006 in all 32
cells, so no sign test is possible), which is why grid B was added. On **grid B** the dial moves
Sharpe genuinely (|dSharpe| > 0.005 in 28 of 32 cells, up to 0.052) and the reversal count is
still **0/32**. That is the load-bearing number: a within-book dial delta that really does move
Sharpe still never disagrees with CAGR.

## Rule 8 walk-forward (IS 2009-01-01..2016-12-31 chooses, OOS 2017-01-01+ read once)

| grid | selector | OOS Sharpe (4 panels) | OOS CAGR | vs SPY 0.882 / 15.5% | vs RULES v1 |
|---|---|---|---|---|---|
| G | S_SHARPE | 1.017 / 1.006 / 0.467 / 1.131 | 14.1 / 16.1 / 8.6 / 16.4% | beats SPY on Sharpe 3/4 | beats v1 (0.58/0.54/0.49/0.75) 3/4 |
| G | S_CAGR | 0.885 / 0.890 / 0.467 / 1.131 | 16.5 / 17.2 / 8.6 / 19.3% | beats SPY 1/4 | 3/4 |
| B | S_SHARPE | 1.058 / 1.058 / 0.369 / 1.158 | 11.5 / 12.7 / 4.4 / 12.7% | beats SPY 3/4 | 3/4 |
| B | S_CAGR | 0.884 / 0.891 / 0.369 / 1.171 | 12.5 / 13.0 / 4.4 / 15.2% | beats SPY 1/4 | 3/4 |

S_CAGR − S_SHARPE, OOS: **−0.062 Sharpe / +1.59 pp CAGR** (grid G) and **−0.082 Sharpe /
+0.96 pp CAGR** (grid B); the two selectors pick a different point in **3 of 4** panels on each
grid. So the metric a study quotes *is* a decision, not just a label — the same conclusion idea
259 reached, and the price runs the same way (CAGR bought with Sharpe) but is **smaller here**
than idea 259's +2.53 pp / −0.025 on the n dial. SMALL is the outlier in both grids: every arm
loses to SPY and to RULES v1 out of sample.

## KEEP paths

4a passes **21/80**, 4b passes **19/80** at 10 bps across both grids. Every 4b pass is a re-run
of an already-published book — `U56/EWall+band3` (11.3% / 1.135 / −15.1%, halves 1.113/1.158,
OOS 1.232) is idea 57's `ew-band3`, and `U56/TOP20@g0.75` (12.8% / 1.064 / −18.3%, OOS 1.131) is
the standing 2026-09-04 4b candidate. Nothing here is a new construction and nothing displaces
the incumbent, so: **no KEEP-candidate, no memo, no RULES change.** SMALL contributes 0 of the
19 passes at any dial value.

## Caveats

**SURVIVORSHIP.** `universe_broad.json`, the BSTK100 megacap cut and the sub-$2B panel are
CURRENT constituents; dead names are absent. On a survivor list the un-ranked book that holds
everything inherits the full survivorship premium while a ranking rule can only redistribute it,
so the bias runs **toward** the pro-EWall side of every carrier comparison counted here — i.e.
against this run's own finding on the CAGR leg, and in favour of it on the Sharpe leg. 44 names
with `max_1d_move >= 1.0` were dropped from the small panel before any number was computed.

**Scope.** Leg A reads only the 11 parents idea 259 flagged. It says nothing about the other 73
files with a minority of reversing pairs, nor about EWall claims in parents that committed no
grid CSV. The regex classifier produced 2 false positives out of 4 mechanical hits (50%), which
is why every hit is quoted verbatim above rather than only counted.

## Proposed reporting habit (not a RULES change; for Sunday review to accept or drop)

Idea 259 proposed a CAGR column beside every EWall-vs-ranked comparison. This run narrows it:
the column is only load-bearing where a **between-book** comparison is the published claim.
Within-book dial deltas — the great majority of what the record publishes — never reversed in
64 controlled cells, so requiring the column there is cost without benefit. Suggested wording:
*"any published sentence ordering two DIFFERENT book constructions on Sharpe must quote CAGR
beside it; dial-delta claims within one construction need not."* One existing LEADERBOARD row
(idea 262's rule-8 ordering) should carry a CAGR note under that habit.
