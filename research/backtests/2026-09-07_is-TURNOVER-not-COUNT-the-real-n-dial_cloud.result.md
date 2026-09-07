# Idea 325 — is-TURNOVER-not-COUNT-the-real-n-dial (2026-09-07, cloud)

**SPLIT. The queue's premise is FALSIFIED — "wider is better on B136" is NOT just "cheaper is
better" (73.1% of the gap survives at zero cost, and the n-ordering is Spearman +1.000 at 0 bps).
But the by-product is bigger than the question: the NO-TRADE BAND is a far stronger dial than the
name count, and it produces the record's first FAMILY of 4b passes that survive 25 bps —
breakevens 25–47 bps against idea 323's finding that nine of the record's ten standing 4b cells
break between 6.9 and 24.7 bps. 4b 37/108 @10 bps, 9/108 @25 bps; 4a 0/108. PARK, not KEEP
(one panel, monotone to the grid edge, not chooser-reachable). RULES.md, scan.py, bot.py and
baseline.py untouched.**

Script `research/backtests/2026-09-07_is-TURNOVER-not-COUNT-the-real-n-dial_cloud.py`, console
`…_cloud.console.txt`, artefacts `.grid.csv` (108 cells × 3 rungs, every point printed),
`.match.csv`, `.breakeven.csv`, `.walkforward.csv`, `.ctx.csv`.

## Gates (passed before any new number was read)
- `fast_backtest` vs `engine.backtest`: max|dr| **0.000e+00**, max|dturnover| **0.000e+00**.
- Derived rung `r(c) = r(0) − turnover·c/1e4` vs a live `backtest(cost_bps=25)`: **0.000e+00**.
- The band state machine **NESTS** the record's hard rank cut: `sel_band(n=20, m=0)` vs
  `sel_hard(n=20)` — **0 disagreements of 54,600** rebalance-day × ticker cells (this required
  carrying the parent's own rank-tie quirk: slots per day are `|{rank ≤ n}|`, not a flat n).
- Idea 44's published U56 anchor reproduces **to the digit**: FIXED `g/n`, n=20, 10 bps →
  **12.66% / 1.092 / −18.31%** against its published 12.66% / 1.092 / −18.31%.

## [A] The premise: is the n-ordering a cost artefact? No.
Books run once at 0 bps, rungs derived exactly. m=0 (the record's own hard-cut book):

| panel | Spearman(n, Sharpe) @0 / 10 / 25 bps | wide(n=80) − narrow(n=20) dSharpe @0 bps | @10 bps | cost channel | turnover 20 vs 80 |
|---|---|---|---|---|---|
| U56 | +0.306 / +0.306 / +0.414 | **−0.0227** | −0.0144 | +0.0083 | 11.00x vs 8.21x |
| B136 | **+1.000 / +1.000 / +1.000** | **+0.0594** | +0.0814 | +0.0219 (**26.9%**) | 14.31x vs 8.77x |
| SMALL439 | +0.000 / +0.071 / +0.107 | −0.0470 | −0.0324 | +0.0147 | 20.45x vs 14.82x |

B136's width ordering is **perfectly monotone at ZERO cost**; cost amplifies it by a quarter and
does not create it. On U56 and SMALL439 the wide book is *worse* than top-20 gross of cost, so
there is no ordering for cost to explain. This also re-confirms the U56 / B136 / SMALL439 split
ideas 320 and 51 keep finding, now with the cost channel removed.

## [B] Turnover matching — the queue's own instrument
Matching the wide book's turnover with a band on a narrower book (10 bps): the band-matched narrow
book **beats** the wide book in **5 of 9** comparisons, and the two largest margins are narrow's
(SMALL439 n=10 m=10 **+0.179**, U56 n=20 m=5 **+0.038**). At matched turnover, width buys nothing
that a band cannot buy more cheaply — the width channel and the churn channel are separable and
the churn channel is the bigger one.

## [B2] The band is the real dial (dSharpe vs the same n at m=0, 10 bps)

| panel | n=10 | n=20 | n=40 |
|---|---|---|---|
| U56 | +0.092 / +0.153 / +0.155 / **+0.169** | +0.024 / +0.025 / +0.048 / **+0.063** | +0.008 / +0.005 / +0.007 / +0.007 |
| B136 | +0.103 / +0.146 / **+0.168** / +0.155 | +0.036 / +0.033 / **+0.065** / +0.034 | +0.001 / +0.017 / +0.017 / +0.010 |
| SMALL439 | +0.047 / +0.119 / **+0.160** / +0.081 | +0.041 / +0.041 / +0.055 / **+0.112** | +0.004 / +0.050 / +0.043 / +0.066 |

(m = 5 / 10 / 20 / 40.) Turnover falls 2.5–3.2x over the same range. The effect is largest exactly
where churn is largest (small n) and decays to nothing by n=40, which is the mechanism idea 47
guessed at, measured on its own dial.

## [C]/[E] Cost robustness — the result that matters
4b at 10 bps: **37/108**; at 25 bps: **9/108** (4a **0/108** at every rung — RULES v2's −12.05%
MaxDD is unreachable). Breakevens for the nine 25-bps survivors:

| cell | turnover | @25 bps CAGR / Sharpe / MaxDD | breakeven c* | first bar to fail |
|---|---|---|---|---|
| **U56 n=20 m=20** | 5.26x | 11.98% / 1.043 / −17.32% | **47 bps** | CAGR |
| U56 n=10 m=40 | 4.57x | 13.82% / 1.047 / −19.06% | 47 bps | H1 |
| U56 n=20 m=40 | 5.07x | 11.88% / 1.059 / −16.16% | 46 bps | CAGR |
| U56 n=20 m=10 | 6.13x | 11.95% / 1.011 / −17.57% | 38 bps | H1 |
| U56 n=20 m=5 | 7.22x | 11.78% / 0.996 / −17.57% | 30 bps | H1 |
| U56 n=30 m=40 / m=20 / m=10 | 5.85–6.15x | 10.7–10.8% / 0.996–1.027 | 27 / 26 / 25 bps | CAGR |
| B136 n=60 m=10 | 6.91x | 10.69% / 0.943 / −18.95% | 25 bps | CAGR |

Idea 323's census found exactly **one** cell in the whole record clearing 25 bps. The band
produces **nine**, eight of them on U56, at a third of the hard-cut book's turnover.

## KEEP-candidate (4b path), and why it is filed as PARK
**U56 / top-20 by the v1 composite / no-trade band m=20 / NORM 75% gross / weekly / 10 bps:
12.87% CAGR, Sharpe 1.112, MaxDD −17.22%, H1/H2 1.144/1.093, OOS 1.187, turnover 5.26x/yr**
(SPY 15.23% / 0.889 / −33.72%, H1/H2 0.957/0.834, OOS 0.882; RULES v2 8.66% / 1.206 / −12.05%).
All five 4b bars clear with room: H1 +0.187, H2 +0.259, OOS +0.305, DD +3.01 pp, CAGR +2.21 pp,
and it holds to **47 bps**. It is nonetheless **PARK, not KEEP**:
1. **One panel.** The same cell fails 4b on B136 (H2 0.817 vs SPY's 0.834) and everything fails on
   SMALL439. The record's cross-universe bar (idea 72) is not met.
2. **Grid edge.** U56 Sharpe is monotone in m out to the widest point tested (m=40) — idea 240/256's
   flag. The breakeven peaks at the interior m=20, which is the only reason a cell is nominated
   at all rather than the edge.
3. **Not chooser-reachable.** Rule 8's IS window picks n=5 m=10 on U56 (OOS Sharpe 1.076), with
   regret **−0.122** against the OOS-best n=10 m=20 and **−0.055** against the n=20 m=0 anchor.
   The record's ~12th "the IS chooser is not free" instance.

## Rule 8 walk-forward ((n, m) chosen on IS ≤ 2016 by Sharpe, OOS 2017+ read once, 10 bps)

| panel | IS-chosen | OOS CAGR | OOS Sharpe | OOS MaxDD | anchor n=20 m=0 | OOS-best | regret |
|---|---|---|---|---|---|---|---|
| U56 | n=5 m=10 | 20.45% | 1.076 | −22.35% | 1.131 | 1.197 (n=10 m=20) | −0.122 |
| B136 | n=10 m=20 | 15.63% | 0.922 | −22.24% | 0.884 | 1.053 (n=80 m=40) | −0.132 |
| SMALL439 | n=10 m=40 | 8.05% | 0.480 | −30.74% | 0.466 | 0.639 (n=10 m=10) | −0.160 |

RULES v2 (live) OOS Sharpe 1.285 / 1.119 / 0.568; SPY OOS 0.882, CAGR 15.45%, MaxDD −33.72%.

## Verdict
Premise **KILLED** (the width ordering is 73% gross-of-cost on B136 and has the wrong sign on the
other two panels); the **band, not the count, is the turnover dial**, and it is worth more Sharpe
than width at every n ≤ 20 on all three panels; one **4b PARK candidate** with the best cost
robustness in the record to date. No RULES change.

## Caveats
All three panels are current-constituent lists (**survivorship**); the sub-$2B panel is the worst
offender and the 44 tickers with `max_1d_move ≥ 1.0` in `data/small_meta.csv` were dropped first
(439 names + SPY, from 2010-01-04, so its halves are not the same calendar halves as U56/B136).
On U56 only ~37 names are eligible on an average day, so n=60, n=80 and n=ALL are the same book
there — the U56 "wide" column is EWALL, not a distinct width. Weights are NORM (`g/k_t`) at
g=0.75 throughout, so the n and m dials cannot smuggle in a gross change.
