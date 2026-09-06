# Idea 280 — is-the-m=999-u56-buffer-book-a-4b-candidate-in-its-own-right (cloud, 2026-09-06)

**ANSWERED / KILL as a candidate. The arm is not a book: it is `top20-200d` at 0.957 daily return
correlation, it is 4a 0 of 45 against the live RULES v2, and at MATCHED TURNOVER the plain parent
on a slower cadence beats it by +0.093 Sharpe / +3.69pp CAGR / +0.189 OOS Sharpe. Its one real
property is drawdown, and that is the one thing the cadence dial cannot buy. No RULES change.**

Script `2026-09-06_is-the-m999-u56-buffer-book-a-4b-candidate_cloud.py`; console `.console.txt`;
all 180 grid points (45 cells x 2 rungs x literal/gross-matched) in `.grid.csv`; the TEST B ladder
in `.cadence.csv`; rule 8 in `.walkforward.csv`. u56, 2009-01-13..2026-09-03, weekly, t+1.

## Four gates, all passed before any new number was read

1. **Idea 273's u56 parent, 3/3 EXACT**: 12.67% / 1.0931 / -18.31%. Idea 72's earlier cite of the
   same book (idea 2's standing KEEP, 12.660% / 1.0921 / -18.308%) differs by +0.00098 Sharpe —
   a last-eval-day difference, not a construction one, so the gate is set on idea 273's END.
   **The standing u56 candidate and the parent are one series**, so this test has three comparands.
2. **Idea 273's u56 m=999 arm, 7/7 EXACT**: 11.90% / 1.1417 / -12.79%, H1 1.198 / H2 1.098,
   OOS 1.2102, 3.4935x/yr.
3. **The state machine nests the parent** at (m=0, j=inf): max|weight diff| and max|daily return
   diff| both **0.0e+00**.
4. **The local mask backtester is `engine.backtest`** on the weekly schedule: max|return diff|
   **0.0e+00**, so the k-week rungs of TEST B are priced under the same execution model.

## TEST A — matched realised gross: a NULL, and that is the useful part

The whole 45-cell gross span is **0.7168-0.7191** (parent 0.7168), i.e. 0.3%. Rescaling every cell
by `c = gross_parent / gross_cell` moves mean |dSharpe| by **0.0000** and changes **no** verdict:
4b stays 45/45 @10bps and 43/45 @25bps, 4a stays 0/45 at both. The candidate goes 11.90% / 1.142 /
-12.79% -> 11.87% / 1.142 / -12.75%. So its 4b pass is **not** an exposure artefact — but it is
also not the cell's: **every** cell passes, the un-budgeted parent included, which is exactly the
objection the queue raised.

## TEST B — matched turnover: the buffer LOSES, and this is the finding

Comparand chosen by |turnover - 3.49x| alone, fixed in the source before any Sharpe on the ladder
was printed. The parent at **6W (3.64x/yr)** is the match.

| @10bps | CAGR | Sharpe | MaxDD | H1 | H2 | OOS Sharpe | turn/yr |
|---|---|---|---|---|---|---|---|
| buffer m=999 (the candidate) | 11.90% | 1.142 | **-12.79%** | 1.198 | 1.098 | 1.210 | 3.49 |
| parent @6W (turnover-matched) | **15.60%** | **1.234** | -21.20% | 1.113 | **1.345** | **1.400** | 3.64 |
| parent @M (4.33x, also near) | 14.73% | 1.204 | -19.51% | 1.211 | 1.206 | 1.286 | 4.33 |
| RULES v2 (live) | 8.68% | **1.208** | -12.05% | **1.226** | **1.194** | **1.288** | **1.77** |
| parent @W (the standing candidate) | 12.67% | 1.093 | -18.31% | 1.088 | 1.103 | 1.170 | 9.63 |
| SPY | 15.26% | 0.890 | -33.72% | 0.957 | 0.837 | 0.884 | 0 |

dSharpe (buffer - matched parent) **-0.0928**, dCAGR **-3.69pp**, dOOS Sharpe **-0.1894**,
dMaxDD **+8.41pp**. Spending the same turnover budget through the CADENCE dial buys strictly more
return and risk-adjusted return; spending it through the RANK BUFFER buys drawdown. The two are
not substitutes, and the buffer is not the Sharpe-maximising way to spend the cut — which
qualifies idea 273's `corr(turnover, Sharpe) = -0.668` on this panel: turnover is not the only
axis, the instrument that removes it matters. Every cadence arm at 2W-8W and Q **fails 4b on the
drawdown cap** (-20.85% to -27.12% against the -20.23% bar); only W, M and the buffer clear it.

## TEST C — it is not a different book

Buffer vs parent (weekly): mean Jaccard **0.611**, identical held set on **19.0%** of rebalance
dates, **corr(daily returns) 0.9570**. Mean held count 18.13 vs 18.07; the buffer holds MORE on
5.6% of dates and fewer on 0.0%. Against the 6W arm: Jaccard 0.565, corr 0.9159. Against RULES v2:
Jaccard 0.512, corr 0.9278.

## Against the live book — 4a 0 of 45, at both rungs, literal and gross-matched

RULES v2 posts 8.68% / **1.208** / **-12.05%** at **1.77x/yr**. The candidate is -0.066 Sharpe,
-0.74pp of drawdown and **2.0x the turnover**, and loses H1 (1.198 vs 1.226) and H2 (1.098 vs
1.194). Out of sample it is **-0.078** against the live book (1.210 vs 1.288). It is a 4b pass on
a board where 4b passes 45/45.

## Rule 8 — the selector still carries no information at the protocol rung

Fitted on 2009-2016 alone, the IS pick is **m=30, j=1** at every rung and both scalings (IS Sharpe
1.0569 vs the parent's 0.9929) — **never the candidate**. Its OOS: 13.26% / 1.199 / -14.78%,
i.e. +0.029 vs the parent, **-0.090 vs the live book**, +0.314 vs SPY. Spearman(IS, OOS) over the
45 cells is **+0.010 @10bps** (+0.625 @25bps), IS-best is never OOS-best. The honest chooser does
not land on the arm the queue asked about, and cannot tell the 45 cells apart at 10 bps.

Pre-registered caveat (idea 111), restated: 2017-2026 is very nearly H2 here, so the rule-8 OOS
bar and 4b's H2 bar overlap almost completely — that weakens every OOS number above.
SURVIVORSHIP: u56 is current constituents, so absolute CAGR/Sharpe are optimistic for every arm;
all comparisons are between arms on the same panel and the same days.

## Answer to the queued question

**A re-labelling, on every axis the queue named.** Matched gross: null (0.3% span, no verdict
moves). Matched turnover: dominated by the plain parent on a slower cadence in CAGR, Sharpe and
OOS Sharpe. Overlap: 0.957 return correlation with the parent, same book size. Against the live
book: loses all three 4a clauses at 2x the turnover. The single thing it owns is the **-12.79%
drawdown**, the only 4b-legal drawdown in the ~3.5x/yr family — the cadence dial at the same
turnover runs -21.20%. That is a finding about the instrument, not a candidate for capital.

## Follow-ups worth queueing

* Is the rank buffer a DRAWDOWN instrument in general — does attaching it to already-4b-passing
  books cut MaxDD by ~8pp at matched turnover on the broad and small panels too?
* Cadence and buffer are not substitutes at matched turnover (-0.093 Sharpe, +8.41pp DD). Price
  the two dials TOGETHER (buffer on a 6W schedule) on one panel, 2 params, and see whether the
  drawdown cut survives at the cadence dial's return.
