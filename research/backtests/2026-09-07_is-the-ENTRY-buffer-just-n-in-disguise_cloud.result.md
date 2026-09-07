# Idea 357 — is the ENTRY buffer just `n` in disguise?  SPLIT

**Answer: NO, and the queue's proposed retirement of `e` is REJECTED — but the record should
re-label the dial.** The entry buffer's dSharpe survives a holdings match in **45 of 54**
panel x rung x e cells (mean **+0.0546**, median +0.0498), so `enter at rank <= n-e` is not a
smaller top-n cut wearing a band's name. What it *is* is a **turnover instrument at matched
holdings**: 59% of the surviving 10-bps margin and 78% of the 25-bps margin is pure cost, and
the cost-free residual is +0.0206, positive in only 12 of 18 cells.

Script `2026-09-07_is-the-ENTRY-buffer-just-n-in-disguise_cloud.py`, console
`.console.txt`, data `.grid.csv` (78 rows) / `.match.csv` / `.decomp.csv` / `.walkforward.csv`
/ `.ctx.csv`.

## Setup

Two ladders on one frame, weekly, next-day, NORM weights g/k at g=0.75, eligibility = above the
200d MA and vol20 < 0.60, ranked by the v1 composite with the vol scaler OFF:

* **BUFFER** — idea 349's entry side, n=20 fixed, `e in {0,2,4,6,8,12,16}`, x=0, slot cap
  k_t = |{rank <= 20}|.
* **HARD** — plain top-n' cut, `n' in 2..20` (19 cells).

Two tuned parameters (n, e); panel {U56, B136, SMALL439} and cost {0, 10, 25} bps are reported
axes, every point printed. `e=0` and `n'=20` are the same book.

**Gates, asserted before any new number was read.** G1 `fast_backtest` vs
`engine.backtest`: max|dr| **0.000e+00**, max|dturn| **0.000e+00**. G2 derived 25-bps rung vs
`backtest(cost_bps=25)`: **0.000e+00**. G3 `sel_entry(e=0)` nests `sel_hard(n=20)` on 975 weekly
rebalance days: **0 disagreements** on all three panels. G4 all **21** buffer cells reproduce
idea 349's committed `.grid.csv` (e, x=0) rows on Sharpe/CAGR/MaxDD/turnover/OOS/names at
**<= 2.220e-16**.

## [B0] The two dials do not move the same things

|  | spearman(param, holdings k) | spearman(param, turnover T) |
|---|---|---|
| BUFFER `e` | **-1.000** (all panels) | **-0.964 / -0.964 / -0.893** |
| HARD `n'` | +1.000 (all panels) | **-1.000** (all panels) |

Shrinking the book by `e` **lowers** turnover; shrinking it by `n'` **raises** turnover. That
single sign difference is the whole answer, and it is why the pre-registered turnover-matched
reading came back **undefined in 54 of 54 cells**: every buffer cell's annual turnover sits
*below the entire hard ladder's range* (U56 buffer 7.57-11.00 vs hard 11.00-24.81; B136
10.15-14.31 vs 14.31-27.85; SMALL439 16.79-20.45 vs 20.45-38.55). The `n` dial cannot reach the
turnover region the entry buffer occupies, so `e` is not `n` in disguise on this data.

## [B1/B2] The match

Holdings-matched = the hard ladder's Sharpe linearly interpolated at the buffer cell's own mean
holdings (nearest-neighbour agrees: 44/54, mean +0.0544).

| reading | mean dSharpe | positive |
|---|---|---|
| vs the (e=0) anchor | +0.0363 | 44/54 |
| NAIVE (hard n'=20-e) | +0.0757 | 51/54 |
| **HOLDINGS-MATCHED** | **+0.0546** | **45/54** |
| holdings-matched, OOS | +0.0339 | 37/54 |

By rung: **12/18 (+0.0206) at 0 bps, 16/18 (+0.0497) at 10, 17/18 (+0.0935) at 25**. By panel:
U56 17/18 (+0.0657), B136 16/18 (+0.0621), SMALL439 12/18 (+0.0359).

## [B5] What the surviving margin is made of

Sharpe(c) = (mu - T*c/1e4)/s exactly, so dS_kmatch(c) = dS_kmatch(0) + (c/1e4)*(T_h/s_h -
T_b/s_b), with each book's effective vol recovered from its own rungs. The identity closes to
**max |residual| 1.1e-04** across all 18 cells.

* At matched holdings the buffer trades **-4.52x/yr less, -26.3%, in 18 of 18 cells**.
* **@10 bps: actual +0.0497 = alpha_at_0 +0.0206 + cost +0.0292 → cost is 59% of the margin.**
* **@25 bps: actual +0.0935 = +0.0206 + 0.0729 → cost is 78%.**
* The cost-free component is positive in only **12/18** cells and is negative on 3 of 6
  SMALL439 cells.

## [B4]/[C] Admission and cost tolerance

4a **0/78 at every rung** (the idea-136 pathology again). 4b **24/78 @0, 15/78 @10, 4/78 @25**;
every pass at 10 and 25 bps is U56. The entry dial opens a 4b cell the n dial does not in
**1 of 9 panel-rungs** — U56 @ 25 bps, where BUFFER passes 4/7 and HARD **0/19**. Consistent
with the decomposition, that one new cell is a cost-tolerance result, not a new source of
return: buffer best **c\* 30 bps** (U56 e=8) vs hard best **c\* 21 bps** (U56 n'=20), and the
first failing bar is `H1` for both.

## [D] Rule 8 walk-forward (chosen on 2008-2016 IS Sharpe @10 bps, 2017-2026 read once)

| menu | mean OOS Sharpe | mean regret | beats anchor | beats SPY | beats LIVE | 4b |
|---|---|---|---|---|---|---|
| BUFFER-ONLY (7) | **0.8335** | -0.0658 | 2/3 | 1/3 | 0/3 | 0/3 |
| HARD-ONLY (19) | 0.7994 | -0.0999 | 1/3 | 1/3 | 1/3 | 0/3 |
| UNION (26) | 0.7814 | -0.1179 | 1/3 | 1/3 | 0/3 | 0/3 |

BUFFER-ONLY minus HARD-ONLY: U56 **+0.156**, B136 +0.012, SMALL439 **-0.066**; mean **+0.034**,
2/3. Keeping the entry dial on the menu is worth a third of what removing it was worth in idea
349 (+0.043 for EXIT-ONLY) and it is carried by one panel. On U56 the HARD menu's IS chooser
takes n'=4 and lands at OOS 0.982 (regret -0.156) — the **14th recorded IS-chooser miss**.
All three menus lose to the LIVE book on U56 and B136.

## Verdict

**SPLIT: the idea's own hypothesis is KILLED, and a re-labelling is proposed instead of a
retirement.** `e` is a real instrument — it survives the holdings match and reaches a turnover
region `n` cannot — but at matched holdings it is a **cost dial**: 59-78% of its margin is the
turnover differential, its cost-free residual is +0.021 (12/18), and an ex-ante chooser gains
only +0.034 mean OOS Sharpe from having it. The record should stop quoting entry-buffer dSharpe
against the *nominal* comparand (n'=20-e overstates it by +0.021 on average) and quote it
holdings-matched with the cost share attached.

**PARK by-product (already inside idea 349's PARKed family, not a new proposal):** U56, top-20
frame, enter at rank <= 12, exit at rank > 20 (`e=8, x=0`), NORM g/k at 0.75, weekly — 13.77%
CAGR / 1.060 Sharpe / -19.23% MaxDD at 10 bps, halves 1.096/1.038, OOS 1.104, turnover 8.25x/yr,
**4b PASS at 0, 10 and 25 bps, c\* 30 bps**. Fails 4b on B136 and SMALL439 at every rung, fails
4a (H1/H2/DD), holds 14.8 names not 20, and is not the rule-8 pick on any menu. Memo `.memo.md`.

**SURVIVORSHIP:** all three panels are current-constituent lists, which flatters every momentum
book and a concentrated one most; the levels are optimistic, the buffer-vs-hard *differences*
much less so. SMALL439 starts 2010-01-04 (44 tickers with max_1d_move >= 1.0 dropped), so its
halves and its rule-8 IS window are not the same calendar as U56/B136.
