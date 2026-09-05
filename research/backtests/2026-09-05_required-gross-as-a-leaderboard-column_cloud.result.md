# Idea 165 — required-gross-as-a-leaderboard-column (cloud, 2026-09-05)

**Verdict: KILL of the proposed column as a re-labelling device — plus one infrastructure
finding the project needs more than the column.**

Idea 165 hoped `g_req` would "re-label a large part of the record". It does not. Over 378 books
and **2,355 genuine backtests**, at most **5 of 378** books change 4b verdict under a
PROTOCOL-legal, prospectively implementable re-grossing. The column is worth publishing as
*diagnosis* (it names why a book failed) but not as *rehabilitation*.

## The infrastructure finding, which came first and is the bigger one
The plan was to compute the whole gross ladder by rescaling one backtest per book, on the
project's standing claim (idea 66) that **gross is an exact lever with zero Sharpe content**.
Reproduction check [c] tested that claim against genuine re-runs and **it is false**.
`products/backtester/engine.py` drifts held weights between rebalances and renormalises against a
**constant-value cash sleeve**:

```
cur <- cur*(1+ret) / [ (cur*(1+ret)).sum() + (1 - cur.sum()) ]
```

so a book started at a different gross follows a different weight path, not a scaled one.
Measured:

| quantity | magnitude |
|---|---|
| max\|daily net-return error\|, 12 re-runs at g ∈ {0.40, 1.00} | 4.90e-03 |
| max \|dCAGR\| (lever-predicted vs genuine) | 0.0238 pp |
| max \|dMaxDD\| | **0.2755 pp** |
| \|dSharpe(g) − Sharpe(0.75)\|, 36 re-runs across the ladder | mean 0.0018, max **0.0097** |
| single-name control book, g = 0.75 → 1.00 | genuine CAGR 24.58% vs lever-predicted 25.21% |

For **ranking** books the lever is a fine approximation. For **verdicts near a bar** it is not:
4b's drawdown margins are routinely ~1pp, so a 0.28pp path error is a material fraction of the
bar a re-grossed book is judged against, and the Sharpe bars are not exactly gross-invariant
either. Worse for the column idea 165 wants: **CAGR is not monotone in gross** under the true
engine — **92 of the 213** CAGR-floor failures have a non-monotone CAGR curve on the ladder — so
"the gross it would need" is a scan result, never a closed form.

**This script's own pre-registered rule was honoured**: after [c] failed, nothing below is
computed by rescaling. Every off-0.75 number is a genuine backtest at that gross on a
pre-registered upward ladder (0.80 0.85 0.90 0.95 1.00 1.10 1.25 1.50 2.00).

## Corpus and reproduction
378 books = 3 panels (u56, broad, small) x 7 keys (NONE/INV/POS/MOM/R6/R3/RND) x 9 shares x
2 cost rungs, weekly, t+1, `norm` construction at gross 0.75. Two tuned parameters: the gross
convention (5 values) and the leverage ceiling (2 values); all grid points in `.grid.csv` /
`.greq.csv` / `.census.csv`.

* **[a] EXACT** — 189 cells reproduce idea 159's committed grid: max|diff| CAGR 9.7e-17,
  Sharpe 2.2e-16, MaxDD 8.3e-17, H1/H2 2.2e-16.
* **[b]** Idea 156's VM formula lands a genuine re-run's realised vol within 1.18e-3 relative of
  SPY's — accurate, but *by genuine measurement*, not by construction as the lever implied.

At the published g = 0.75: **4b 55/378, 4a 117/378.** Among the 323 4b failures the CAGR floor
appears in 213 (65.9%) — the population idea 165 asks about (u56 41, broad 46, small 126).

## The answer to idea 165's question
Each CAGR-floor failure classified into exactly one bucket, all at genuine re-runs, ceiling at
PROTOCOL rule 2's g ≤ 1.00:

| convention | CEILING (g_req > 1.00, record stands) | REACHABLE (clears all five bars, row mislabelled) | TRADED (clears CAGR, another bar fails) |
|---|---|---|---|
| VM_FULL (idea 156's formula, look-ahead) | **38.0%** | **0.0%** | 62.0% |
| VM_IS (implementable) | **38.0%** | **0.0%** | 62.0% |
| CF_FULL (the floor's own inverse, look-ahead) | 66.2% | 4.2% | 29.6% |
| CF_IS (implementable) | **65.7%** | **2.3%** | 31.9% |

n = 213 in every row. So idea 165's hoped-for re-label does not exist:

* Under **idea 156's own vol-matching formula, exactly ZERO of the 213** becomes a clean 4b pass
  at a legal gross. 38% are ceiling KILLs and the other 62% merely swap the CAGR bar for another.
* Under the **floor's own inverse** — the number a column actually wants — two thirds are ceiling
  KILLs and only **2.3% (5 books)** are genuinely mislabelled.
* **P3 was wrong in the direction that matters.** CF_* is *not* uniformly below VM_*: 97 of the
  213 books never clear the floor at ANY gross up to 2.00, so the vol-match proxy *understates*
  the ceiling problem rather than overstating it.

**In the TRADED bucket the drawdown cap is what takes over** (DD 57, H2 54, OOS 41, H1 38,
CAGR 34 under CF_IS/CAP) — idea 156's P5 confirmed on a much wider corpus.

Net 4b pass count over all 378 books (books already clearing the floor stay at g = 0.75):
STATIC **55** → VM_IS/CAP 56 → CF_IS/CAP **60** → CF_FULL/CAP 64 (look-ahead). **At most +5 of
378 under a legal, implementable convention.**

Per panel the story splits cleanly, and it is a *panel* story, not a rule story: under VM,
u56 is 95.1% CEILING and broad 91.3%, while the small panel is **0% CEILING / 100% TRADED** — its
books are low-vol enough to reach the floor and then fail on drawdown instead.

## Rule 8 walk-forward (chosen on 2009-2016, read ONCE on 2017-2026)
Mean OOS over the 6 (panel x cost) cells; SPY OOS 15.45% / 0.8820 / -33.72%:

| arm | OOS Sharpe | OOS CAGR | OOS MaxDD |
|---|---|---|---|
| W_4bIS (IS 4b screen at CF_IS, then IS-Sharpe) | **0.6715** | 10.86% | -26.93% |
| W_CFIS | 0.6528 | 10.86% | -28.25% |
| W_STATIC (do-nothing control) | 0.6527 | 10.83% | -27.52% |
| W_VMIS | 0.6525 | 11.48% | -28.34% |

**Re-grossing buys nothing risk-adjusted.** W_VMIS buys +0.65pp of OOS CAGR for +0.8pp of OOS
drawdown and −0.0002 of Sharpe — the exchange rate of a pure risk-budget lever, exactly as the
project has priced it elsewhere. The only arm that moves is W_4bIS, and it moves because the
*screen* changed the pick, not because the gross did.

One cell is worth naming: **u56 @ 10 bps, W_4bIS picks R6 @ m = 0.15 (n = 6) at g = 0.750 and
clears every OOS-window 4b bar — OOS 19.69% / 1.0823 / -18.93%** against SPY's 15.45% / 0.8820 /
-33.72% and RULES v1's 7.73% / 0.7471 / -13.83%. That is the IS 4b screen earning its keep in
1 of 6 cells (bears on idea 163); it is **not** a re-grossing result — the pick sits at the
published 0.75 — and one cell is not a KEEP.

## What PROTOCOL should take from this
1. **Do not add `g_req` as a rehabilitation column.** It re-labels ≤ 2.3% of CAGR-floor KILLs.
2. **Do add the failing-bar string** (idea 161's ask): 62% of CAGR-floor failures are really
   drawdown failures wearing a CAGR label, and that is knowable for free at g = 0.75.
3. **Stop treating the gross ladder as an exact lever.** Rescaling is acceptable for ranking and
   not for verdicts; a proposed follow-up idea is queued rather than fixed here, because
   PROTOCOL forbids touching `baseline.py` and `engine.py` is the live backtester.

## Caveats (carried, not buried)
* **SURVIVORSHIP.** All three panels are current-constituent lists (idea 54); the small panel is
  the worst case (`data/SMALL_PANEL_README.md`), which inflates every return there and therefore
  **understates** g_req on that panel. No small-panel number here is tradable.
* This is a back-fill over the project's standing book **families**, not over the literal rows of
  LEADERBOARD.md. Many committed rows are one-off constructions (sleeves, stops, breadth gates,
  overlays) whose scripts are not re-run here. It is the largest corpus the project has put the
  question to and spans every panel and both cost rungs, but the census is a statement about
  these 378 books and is labelled as such.
* VM_FULL and CF_FULL use full-sample information and are labelled LOOK-AHEAD at every use.
* Everything at g > 1.00 is levered, which PROTOCOL rule 2 forbids; it is reported only to size
  the shortfall and is never a KEEP.
* g_req rests on a modelled cost bill (turnover x cost_bps) with no slippage or impact, both of
  which are worse at higher gross — so every g_req here is a **lower bound**.
* Idea 38 (calendar-day price index) and idea 126 (t+1 execution) carry over unchanged.

Artefacts: `.console.txt`, `.grid.csv`, `.greq.csv`, `.census.csv`, `.walkforward.csv`,
`.repro.csv`. Runtime 4,285s; 2,355 genuine backtests.
