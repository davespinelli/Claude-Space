# Idea 372 — price the sleeve fraction against the gross numeraire on an UNGATED core

**Verdict: ANSWERED — the sleeve BEATS its matched-gross ladder point, so it is NOT "a
de-grossing device with extra moving parts". The BOOK is PARK, not KEEP: c=0.40 ungated is
4b-clean at 0/10/25 bps on both panels but rule 8's chooser never reaches it.**
Script: `2026-09-07_price-the-sleeve-fraction-against-the-gross-numeraire_cloud.py`.
1 tuned parameter (c, 10 values, all reported). The ladder multiplier m is SOLVED to match
realised mean gross, not tuned. Panel / cost rung / core gate are reported axes: 240 cells.

## Gates
- **G0** cost identity `net = gross − turnover·c/1e4` vs `engine.backtest(cost_bps=k)`: **0.00e+00**.
- **G1** idea 30's published 4b passer reproduces to the decimal: U56 @10 bps, c=0.50, ungated =
  **13.0% / 1.041 / −20.1%** (published 13.0% / 1.041 / −20.1%).
- **G2** gross-match residual |realised − target| ≤ **1.04e-06** over all 40 solved ladder points.
- **G3** panel axis degeneracy re-measured, not assumed: max |U56−B136| Sharpe **3.95e-04**,
  CAGR 2.80e-05, MaxDD 2.20e-04. B136 is not an independent confirmation for this ETF-only book.

## 1. The ruler — the sleeve wins, and it wins where it matters
Control = 100% QQQ ungated (c=1.00): 20.88% CAGR, Sharpe 1.011, MaxDD −35.12%.
`ratio` = pp of MaxDD bought per pp of CAGR paid (idea 351's sign); `numeraire` = |MaxDD|/CAGR = **1.6816**.

| gate | rung | median sleeve ratio | median matched-gross ladder ratio | median edge | sleeve ΔSharpe | ladder ΔSharpe |
|---|---|---|---|---|---|---|
| OFF | 0 | **1.984** | 1.505 | **+0.489** | +0.026 | −0.001 |
| OFF | 10 | **1.883** | 1.493 | **+0.402** | +0.017 | −0.002 |
| OFF | 25 | **1.748** | 1.475 | **+0.288** | +0.001 | −0.003 |
| ON | 0 | 1.685 | 1.522 | +0.165 | −0.040 | −0.002 |
| ON | 10 | 1.612 | 1.511 | +0.103 | −0.065 | −0.004 |
| ON | 25 | 1.475 | 1.495 | −0.030 | −0.105 | −0.005 |

- **Sleeve ratio > matched-gross ladder ratio in 96/114 priced points**; on the ungated core (the
  4b form) it is **27/27 at 0 and 10 bps** and 24/27 at 25 bps (min edge −0.013 at c=0.00).
- The sleeve also buys that drawdown at **positive** Sharpe on the ungated core (+0.026 / +0.017 /
  +0.001 median) where the ladder is Sharpe-neutral-to-negative — the ladder is a pure exposure cut,
  exactly as idea 351 predicted.
- **The 200d gate destroys the edge**: with GATE=ON the median edge falls 0.165 → 0.103 → −0.030
  across the rungs and ΔSharpe is negative at every rung. Idea 30's "the gate is the whole H1 problem"
  survives on this axis too.

**Correction to idea 351's closed form.** The realised gross-dial ratio is **1.47–1.52 at every point,
never once above the closed-form numeraire (0/114)**. |MaxDD|/CAGR = 1.6816 **overstates what the gross
dial actually delivers by 10–13%** on this book, because MaxDD is not linear in m. Scored against the
closed form the sleeve wins only 58/114; scored against the ladder point you can actually buy it wins
96/114. The record should quote the *achievable* ladder point, not the closed form, as the bar.

## 2. The sleeve moves the 4b frontier; the gross dial cannot
**4a 0/240. 4b 10/240** — every one a BLEND, every one **ungated**, at c ∈ {0.40, 0.50}:

| | BLEND ungated | BLEND gated | matched-gross LADDER |
|---|---|---|---|
| 4b passes | **10 / 60** | 0 / 60 | **0 / 120** |

No static-gross ladder point clears 4b at any gross on either panel at any rung, while the blend does.
First failing 4b bar over the 230 failures: **DD 158, H1 66, CAGR 6**.

The admissible window is bounded on both sides and is 2 of 10 grid points wide (U56 @10 bps):

| c | CAGR | Sharpe | MaxDD | H1 / H2 | OOS | turnover | 4b |
|---|---|---|---|---|---|---|---|
| 0.25 | 9.05% | 1.037 | −14.4% | 1.078 / 1.009 | 1.104 | 3.53x | fails **CAGR** (floor 10.66%) |
| **0.40** | **11.45%** | **1.044** | **−17.38%** | **1.144 / 0.975** | **1.063** | 2.87x | **PASS** (DD slack 2.85pp, CAGR slack 0.79pp) |
| **0.50** | **13.04%** | **1.041** | **−20.08%** | **1.166 / 0.955** | **1.038** | 2.42x | **PASS** (DD slack 0.15pp) |
| 0.60 | 14.62% | 1.035 | −23.21% | 1.178 / 0.938 | 1.017 | 1.96x | fails **DD** (cap 20.23%) |

c=0.40 is the better of the two on every margin and is the only cell that also clears **25 bps**
(10.97% / 1.005 / −17.45%, H1 1.098 / H2 0.940, OOS 1.027 — CAGR slack 0.31pp). It was **not in idea
30's grid** (which started at c=0.50); its 2.85pp DD slack is 19x idea 30's 0.15pp.

## 3. Rule 8 — why the book is PARK and not KEEP
c chosen on IS Sharpe ≤2016, read once on 2017–2026:

| panel/gate | rung | IS pick | OOS Sharpe | OOS MaxDD | anchor c=0.50 OOS | OOS-best c | regret |
|---|---|---|---|---|---|---|---|
| ungated | 0 | **c=1.00** | 0.963 | **−35.1%** | 1.056 | 0.00 (1.166) | 0.203 |
| ungated | 10 | **c=1.00** | 0.963 | **−35.1%** | 1.038 | 0.25 (1.104) | 0.141 |
| ungated | 25 | **c=1.00** | 0.963 | **−35.1%** | 1.012 | 0.25 (1.048) | 0.086 |
| gated | 0/10/25 | 0.25 / 0.40 / 0.80 | 1.224 / 1.173 / 1.112 | −13.1/−15.6/−22.1% | 1.191 / 1.163 / 1.123 | — | 0.000 / 0.006 / 0.011 |

IS Sharpe is **monotone increasing in c** on the ungated core, so the chooser picks c=1.00 — 100% QQQ,
a −35.1% drawdown, and a 4b failure on the DD cap — in **6/6 ungated cells**. It picks the anchor
c=0.50 in **0/12** cells. The queue's premise ("rule 8 never reaches them") is confirmed exactly.
The ungated chooser's pick ties its own matched-gross ladder point (c=1.00 ⇒ m=1.00, the same book);
the gated chooser beats its ladder point by +0.155 to +0.266 of OOS Sharpe in 6/6.

So the c=0.40 book clears every 4b bar as a **pre-registered point** but is not **selectable** from
in-sample data by the record's own chooser. Per PROTOCOL rule 8 that is **PARK**, not KEEP.

## 4. What the record should carry
1. **The sleeve is a genuine instrument, not a gross dial.** 96/114 on the ruler, 27/27 on the ungated
   core at ≤10 bps, and 10 4b passes against the ladder's 0/120. This closes the queue's conditional
   in the sleeve's favour and reproduces idea 139's "sleeve moves the frontier" on a second book.
2. **Quote the achievable ladder point, not |MaxDD|/CAGR.** The closed form overstates the gross dial
   by 10–13% here (1.68 vs 1.47–1.52 realised, 0/114). Which bar you use flips this verdict.
3. **The 200d gate is a ruler-negative clause**, not just an H1 problem: it costs the sleeve its whole
   edge over the numeraire by 25 bps and turns ΔSharpe negative at every rung.
4. The 4b window on this book is **two grid points wide**, walled by the CAGR floor below and the DD
   cap above — an admissibility band, not an optimum. Nothing here is a plateau.

**Survivorship:** U56/B136 are current-constituent lists; levels are flattered, c-differences far less.
**Conditioning:** QQQ's 2009–2017 run is the best large-cap equity decade in the sample.
