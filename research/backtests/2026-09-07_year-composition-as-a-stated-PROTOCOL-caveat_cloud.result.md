# Idea 111 — year-composition-as-a-stated-PROTOCOL-caveat (cloud, 2026-09-07)

**Verdict: KILL as a PROTOCOL amendment.** The imbalance the idea wants to fix is a
sample-start artefact, the re-derived split is not a constant, the objective is degenerate,
and the caveat as intended points the wrong way — a crisis-heavy OOS window makes 4b *easier*,
not harder, because it lowers the SPY-derived bar faster than it lowers the candidate.

Script: `2026-09-07_year-composition-as-a-stated-PROTOCOL-caveat_cloud.py`
Tuned parameters: 2 — the badness threshold (4 definitions) and the split date (11 year-ends).
All 44 combinations reported. Population: 180 books (3 panels × 5 shapes × 3 gross × gate ×
2 cadences), 3,840 book-cells across all splits.

---

## P1 — the premise, reproduced exactly, then corrected

Idea 99's console reads `SPY MaxDD-<-15% years: IS [2010, 2011] | OOS [2018, 2020, 2022,
2025]`. Reproduced to the year on a **2010-start** sample: **2 of 7 IS, 4 of 10 OOS**,
year-share gap **−0.114**.

PROTOCOL rule 8 walks forward on the 2008-start panel. Same definition, that sample:

| sample start | IS window | OOS window | gap (year share) |
|---|---|---|---|
| 2010 (idea 99) | **2 of 7** — 2010, 2011 | **4 of 10** — 2018, 2020, 2022, 2025 | −0.1143 |
| **2008 (the panel PROTOCOL uses)** | **4 of 9** — 2008, 2009, 2010, 2011 | 4 of 10 | **+0.0444** |

The "2 of 7" is a **sample-start artefact**: beginning in 2010 excludes 2008 and 2009 — the
two deepest crisis years in the record — from the IS window. On the panel the walk-forward
actually runs on, the incumbent split is already balanced (day-share gap +0.032). *There is no
imbalance to re-derive a date for.*

The count is also not definition-free. At the incumbent split, across the four badness
definitions the IS/OOS counts are 1/9 vs 2/10 (`ret<0`), 5/9 vs 4/10 (`dd≤−10`), 4/9 vs 4/10
(`dd≤−15`), 2/9 vs 2/10 (`dd≤−20`) — the gap changes sign between definitions (−0.089 to
+0.156).

## P2 — the re-derived split date is not a protocol constant

| badness | equalising split (year share) | \|gap\| | resulting windows |
|---|---|---|---|
| `ret<0` | **2013-12-31** | 0.0128 | IS 1/6, OOS 2/13 |
| `dd≤−10` | **2017-12-31** | 0.0556 | IS 5/10, OOS 4/9 |
| `dd≤−15` | **2019-12-31** | 0.0119 | IS 5/12, OOS 3/7 |
| `dd≤−20` | **2021-12-31** | 0.0143 | IS 3/14, OOS 1/5 |

Four definitions, **four distinct dates spanning eight years**. A number that moves that far
with an arbitrary threshold cannot be written into PROTOCOL as a derived constant.

Worse, the objective is **degenerate**: equalising crisis share is most cheaply achieved by
pushing the split *later*, which shrinks the evaluation window. By day-share the optimum is
2021-12-31 under both `dd≤−15` (gap 0.0020) and `dd≤−20` (gap 0.0010) — leaving **5 OOS
years**. The rule would be trading out-of-sample length, the only thing rule 8 exists to buy,
for cosmetic balance.

## P3 — pricing it: composition binds on the BAR, not the candidate

Full rule-8 walk-forward re-run at all 11 splits × 3 panels × 2 rungs (argmax IS Sharpe chosen
on the IS window only; OOS read once). spearman(OOS crisis share, ·) over the 11 splits, in
24 panel × rung × definition cells:

| quantity | negative | positive | median ρ |
|---|---|---|---|
| **SPY's own OOS Sharpe** (the 4b bar) | **24/24** | 0 | **−0.603** |
| menu-mean OOS Sharpe (average candidate) | **23/24** | 0 | −0.517 |
| **the rule-8 PICK's OOS Sharpe** | 4/24 | **19/24** | **+0.320** |
| 4b pass count | 6/16 | 10/16 | +0.083 |

Crisis-heavy OOS windows hurt SPY hard and the average book moderately, but the **argmax-IS
pick is if anything better in them** (ρ up to +0.658 on U56@10). Because PROTOCOL derives the
4b bars *from SPY on the same window*, a crisis-heavy OOS window **lowers the bar and raises
the candidate** — it makes 4b easier. The caveat as the queue conceived it ("a crisis-heavy
window is a harsher test, quote the count so readers can discount it") has the sign backwards.

Anchor row — U56 @ 10 bps at the incumbent split: pick TOP20 g1.00 raw M, IS Sharpe 1.0925,
**OOS CAGR 16.32%, OOS Sharpe 1.0743, OOS MaxDD −23.64%**, vs RULES v2 OOS 1.2841 / 9.53% /
−12.05% and SPY OOS 0.8779 / 15.37% / −33.72%. Across the 11 splits the same panel × rung's
pick ranges 0.7176–1.2004 in OOS Sharpe.

## P4 — moving the split is expensive and buys nothing

Incumbent 2016-12-31 vs each definition's equalising split, over 24 (definition × panel ×
rung) cells:

- the rule-8 **pick changes in 15 of 24 cells**;
- mean |ΔOOS Sharpe| **0.1412**, max **0.4750** (B136@25 under `ret<0`: 0.8823 → 0.4073);
- the 4b pass count moves by 1.04 books on average (live 4.0 → equalised 3.5 of ~60), i.e. it
  gets *worse* as often as better;
- no cell gains a 4a pass.

So re-deriving the split is a high-variance intervention against a target that four equally
defensible definitions disagree about by eight years.

## Premise check — "overlay value is signed on year-badness inside BOTH windows"

Tested on the **live** defensive overlay (the RULES v2 200d ±3% band gate) against the same
book ungated, TOP20 weekly @10 bps, per calendar year, pooled over the three panels:

| badness | IS: d_good / d_bad | OOS: d_good / d_bad | signed? |
|---|---|---|---|
| `ret<0` | −0.0098 / (no bad yrs) | +0.0021 / +0.0252 | no |
| `dd≤−10` | −0.0015 / **−0.0199** | −0.0066 / +0.0266 | OOS only |
| `dd≤−15` | +0.0007 / **−0.0323** | −0.0066 / +0.0266 | OOS only |
| `dd≤−20` | −0.0024 / **−0.0843** | −0.0035 / +0.0477 | OOS only |

"Signed" (helps in bad years, hurts in good) holds in **1 of 8** cells and in **0 of 4 IS
cells** — in the IS window the gate *hurts* in bad years under every definition, the opposite
of idea 99's +0.135. Idea 99's overlay family was a cash sleeve, not the band gate, so this
does not overturn its number; it does mean the claim **does not transfer to the overlay the
live book actually runs**, which is the only one PROTOCOL would be caveating.

## Both KEEP paths

Over all 3,840 book-cells (180 books × 11 splits × 2 rungs, judged on each split's own OOS
window against that window's SPY and RULES v2): **4a 4 cells**, **4b 225 cells**. Every 4a
pass is at the degenerate 2021 split on B136. SMALL439 contributes **0 4b passes at every
split and rung**.

## What survives

The re-derivation is dead, but one line of the proposal is worth keeping and costs nothing:

> **Rule 8 should quote the SAMPLE START alongside the split date.** The same
> `2016-12-31` split has an IS crisis share of −0.114 relative to OOS on a 2010-start panel
> and **+0.044** on a 2008-start panel. The record routinely compares walk-forwards across
> `U56`/`B136` (2008-start) and `SMALL` (2010-start) as if their IS windows were the same
> test; they are not, and 2008–2009 is the whole difference.

What should be quoted about the evaluation window is **SPY's own OOS Sharpe, CAGR and MaxDD** —
which PROTOCOL already requires (rule 3, and the 4b bars are computed from them). A crisis-year
count adds nothing that those three numbers do not already carry, and carries it worse: the
count is threshold-dependent, and it predicts the bar rather than the candidate.

**No change proposed to PROTOCOL.md, RULES.md, or any live file** (rule 6: rules change only
via Sunday review).

**SURVIVORSHIP:** the SMALL panel is current constituents of a sub-$2B screen only
(`data/SMALL_PANEL_README.md`); 44 of 483 tickers with `max_1d_move ≥ 1.0` dropped first. Its
numbers are upper bounds; it contributes 0 of 225 4b passes, so it changes no conclusion here.
