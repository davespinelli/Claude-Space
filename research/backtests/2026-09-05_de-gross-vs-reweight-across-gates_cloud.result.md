# Idea 130 — de-gross-vs-reweight-is-not-one-convention — **ANSWERED: the MECHANISM generalises perfectly, the CROSSOVER THRESHOLD does not**

Script: `research/backtests/2026-09-05_de-gross-vs-reweight-across-gates_cloud.py`
Console: `…_cloud.console.txt` · Grid: `…_cloud.grid.csv` (900 arm-rows + 24 controls) ·
Convention axis: `…_cloud.convention.csv` (450 dg/rw pairs) · Crossover: `…_cloud.crossover.csv`
(90 cells) · Walk-forward: `…_cloud.walkforward.csv`

## What was run
Idea 95 measured the `dg` vs `rw` convention on ONE book with ONE gate. This run puts it on
5 gates × 5 strictness points × 2 conventions × 3 books × 3 panels × 2 cost rungs = **900
arm-rows**, every one reported. Two tuned parameters (gate strictness dial, convention);
gate identity, book, panel and cost are reported axes, never selected on. Idea 94's simulator
is imported, not re-implemented; the dial-parameterised gate masks reproduce idea 94's own
masks **exactly** at all five default dials, and idea 95's published `EWall+vol60-dg` u56
@10 bps row reproduces to the printed digit (**11.6% / 1.133 / −16.9%**).

## Answer 1 — the mechanism is universal: **48 of 48**
Across every gate, book and panel, in every row where the convention ALONE decides the 4b
verdict:

| convention that passes | rows | the bar the OTHER convention breaks |
|---|---|---|
| `rw` passes, `dg` fails | 39 | **CAGR floor — 39 of 39** |
| `dg` passes, `rw` fails | 9 | **drawdown cap — 9 of 9** |

Not one row breaks on any other bar, and not one breaks in the other direction. Idea 95's
"the convention swaps which bar binds" is confirmed as a general property, with a clean
one-line statement of the sign: **de-grossing risks the CAGR floor; re-weighting risks the
drawdown cap.** The mechanism is analytic for `EWall`, where `rw_t = dg_t / f_t` exactly
(f = admitted fraction), so the convention there is a pure time-varying gross scaler and moves
CAGR and MaxDD together along precisely the axis on which 4b's two absolute bars sit. The bind
swaps in **79%** of EWall rows, **30%** of TOP20 rows and **3%** of V1u rows — V1u holds 5
names at a fixed 15% and has almost nothing for the convention to move.

## Answer 2 — the crossover threshold is **NOT stable**
Located on the one axis the five gates share (`adm`, the mean fraction of the panel admitted):

- A Sharpe sign change exists in only **54 of 90 cells (60%)**. In the other 36, one convention
  wins across the whole dial (rw throughout 21, dg throughout 15).
- Where it exists: **adm\* mean 0.611, sd 0.180, range 0.228–0.953** — a spread covering most
  of the usable range of the axis.
- It is **not a gate property**: vol60 0.786 vs v1gate 0.418 (means).
- It is **not a book property** either: EWall 0.636, TOP20 0.602, V1u 0.595 — nearly identical
  means with sds of 0.13–0.22.
- What it mostly tracks is the **panel**: u56 0.704, broad 0.734, **small 0.427**.

There is no single number PROTOCOL can quote. Note also that idea 95's claim was framed on the
*4b* axis while a crossover is naturally measured on the *Sharpe* axis, and these are different
objects: for `EWall+vol60` the Sharpe crossover sits at adm\* ≈ 0.95 on both large-cap panels
(dial 0.60→0.80), i.e. `dg` wins on Sharpe over essentially the entire usable range and `rw`
only overtakes once the gate has stopped gating.

## Answer 3 — the convention is small on Sharpe and decisive on 4b
Mean |rw − dg| Sharpe is **0.030** (EWall 0.044, V1u 0.028, TOP20 0.018; max 0.179), against a
mean **0.134** Sharpe spread across the five gates at their default dials — the convention is
~4.5× smaller than the gate choice it is usually reported inside. But because 4b is a set of
*absolute* bars, that small move still flips the verdict in **48 of 450 pairs (11%)**. A row
published without its convention named is therefore not reproducible: 110 of 900 arms pass 4b,
and a ninth of the pass/fail decisions turn on a convention that most write-ups treat as
presentational.

## Answer 4 — rule 8 cannot pick the convention
(dial, convention) chosen on IS Sharpe alone, evaluated untouched on 2017–2026, 90 cells:
- The selector picks `rw` in **59 of 90** cells — but `rw` picks average **0.691** OOS Sharpe
  against `dg` picks' **0.802**. The walk-forward systematically prefers the convention that
  does worse out of sample.
- The pick is the OOS-best arm in **18 of 90** cells; it beats the ungated control in **32 of
  90** and SPY in **35 of 90**.
- Spearman(IS, OOS) across the arms of a cell averages −0.08 (u56/EWall) to +0.58
  (broad/EWall) — no consistent sign.

## Verdict
**ANSWERED — KILL of the "stable crossover threshold" hypothesis; KEEP of the sign rule as a
reporting requirement.** The convention is a real, signed, universal instrument with an
unstable location. Proposed PROTOCOL wording (a reporting clause, not a rules change — nothing
here promotes or demotes a book):

> Any published result that applies a gate to a book must name its convention (`dg` =
> gated-out names to cash; `rw` = book rebuilt at full gross among the admitted names) and
> report the other one alongside it. The two are not readings of one instrument: `dg` risks
> 4b's CAGR floor and `rw` risks 4b's drawdown cap (48/48 decisive rows, idea 130). There is
> no stable crossover point at which one becomes correct — it exists in only 60% of cells and
> ranges over an admitted fraction of 0.23–0.95 — so the convention may not be chosen by
> walk-forward (rule 8 picks the OOS-worse convention in 59/90 cells) and must be declared in
> advance.

**The standing candidate is unaffected**: `EWall + vol60` passes 4b on both large-cap panels
under **both** conventions (u56 5 dg / 5 rw, broad 4 dg / 4 rw across the dial and cost rungs),
so its adoption case does not rest on the convention. No RULES change proposed this week.

## Caveats, carried
- Survivorship: all three panels are current-constituent lists (idea 54). The small panel is
  the sub-$2B screen minus the 44 tickers with `max_1d_move ≥ 1.0` in `data/small_meta.csv`
  (439 names), and SPY there is a joined benchmark excluded from every book; on u56/broad SPY
  is a genuine universe.json constituent and is left in, exactly as ideas 94/95 had it. The
  small panel is also the one whose adm\* (0.427) sits furthest from the large-cap panels, so
  the instability of the crossover is partly an instability *of the panel*, and survivorship
  is a live candidate for the difference.
- Idea 38's calendar-day-index warning was checked, not assumed: all three caches are
  trading-day clean (0 weekend rows, 0 rows with >70% flat prices).
- 0 of 300 small-panel arms pass 4b under either convention, so every 4b statement above is a
  large-cap statement.
