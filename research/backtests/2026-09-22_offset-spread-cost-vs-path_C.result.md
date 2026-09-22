# Idea 2115 (lane C, 2026-09-22) — is the REBALANCE-OFFSET SPREAD a COST ARTEFACT or a PATH ARTEFACT?

**ANSWERED, DECISIVELY: it is a PATH artefact. 162 of 162 cells. KILL the cost-artefact reading —
and with it the hope that better execution retires idea 914's clause.**

Script `research/backtests/2026-09-22_offset-spread-cost-vs-path_C.py`; artefacts `.console.txt`,
`.grid.csv.gz` (1,440 scored books), `.spreads.csv`, `.split.csv`, `.clause.csv`,
`.walkforward.csv`, `.gates.csv`. Deterministic, offline, 17 s.

## The question and why it mattered
Idea 914 killed a KEEP-4b candidate because its DD margin was smaller than the same book's spread
across five weekly rebalance offsets; idea 2119 (lane B, today) turned that clause on a 25-cell
ladder and found only 7 of 16 passes survive 5 of 5 offsets. Both runs treat the spread as given.
If the spread were a turnover-TIMING BILL it must collapse toward zero at 0 bps, and 914's clause
would be a statement about the broker that better execution retires. If it is PATH SAMPLING it
survives at zero cost, and the clause is a statement about the RULE that nothing retires.

## The answer
**Every single cell is a path artefact.** Over 162 (panel × book × cadence × window × leg) cells
— cadence D excluded as the structural-zero control (G4) — the pre-registered buckets read
**PATH 1.000 / MIXED 0.000 / COST 0.000**, on all three legs separately (CAGR 54/54,
Sharpe 54/54, MaxDD 54/54).

- **Median S(0)/S(10) = 1.0003** (min 0.889, max 1.100). *The whole* of PROTOCOL's own 10 bps
  offset spread is already present at ZERO cost. Median S(0)/S(50) = 1.0013 (min 0.645).
- **The slope is nil.** |d S / d c| median 1.16e-05 per bp, max 4.05e-04 per bp, against spread
  LEVELS of 0.001–0.19 in the leg's own unit. Fifty basis points of cost move the spread by less
  than its own rounding.
- **The exact arithmetic split agrees** (B3 — not a fit). Because costs never touch the held path
  in this engine (gate G5, 0.000e+00), `net_d(c) − net_0(c) = [gross_d − gross_0] − (c/1e4)·
  [turn_d − turn_0]` exactly. At PROTOCOL's 10 bps the ratio |COST_d|/|PATH_d| has median
  **0.0072** — the weekday cost bill is seven tenths of one percent of the weekday path
  difference — and cost dominates in **0.0069** of 144 offset pairs. At 50 bps still only 0.0358
  (cost dominates 0.0139). Per book: BAND03_G075 0.0036, TOP20 0.0065, EWELIG 0.0126. Per cadence:
  Q 0.0031, M 0.0067, W 0.0185. Median |PATH_d| is 0.168–0.775 pp/yr of CAGR against a median
  |COST_d| of 0.0006–0.0050 pp/yr.
- **B1c** on the clip-free offsets {0,1,2} only (G6: W d3 clips 2 weeks, d4 clips 175): PATH 0.988,
  MIXED 0.012, median S0/S10 1.000. The verdict is not a holiday-week artefact.

## What this does to idea 914's clause (B4)
It **hardens** it. The cost rung does move how many books pass 4b — 9 → 6 → 5 → 2 d=0 passes at
0/10/25/50 bps — but that is the book's LEVEL dying of costs, not the spread shrinking. The share
of d=0 4b passes whose every leg margin exceeds its own offset spread runs **0.111 → 0.000 →
0.000 → 0.000**. At PROTOCOL's own 10 bps, **zero of six** 4b passes clear their own weekday
spread on every leg, and **two of six** are 5-of-5-offset stable. The binding leg is drawdown at
every rung (clr_DD 0.111 / 0.167 / 0.000 / 0.000, against clr_CAGR 0.889 / 0.833 / 0.800 / 1.000).
Since the spread is cost-invariant and the margins shrink with cost, **the clause can only get
harder as execution assumptions get more honest, never easier.**

## Capital arm (B5 rule 8, B6 path 4a) — NO NEW KEEP
Dials chosen on IS 2009–2016 only at d=0 by IS Sharpe; 2017–2026 read once. The cost rung is not a
real choice (PROTOCOL rung 2 fixes it at 10 bps), so the headline pick selects CADENCE at 10 bps
and the both-dials-free pick is reported as a sensitivity only.

| panel | book | pick | OOS book | RULES v2 OOS | SPY OOS | 4b | 4a | 5/5 |
|---|---|---|---|---|---|---|---|---|
| U56 | BAND03_G075 | M@10 | 9.55% / 1.224 / −14.38% | 9.46% / 1.277 / −12.05% | 15.29% / 0.875 / −33.72% | FAIL | FAIL | N |
| U56 | TOP20 | M@10 | **16.68% / 1.284 / −19.51%** | 9.46% / 1.277 / −12.05% | 15.29% / 0.875 / −33.72% | **PASS** | FAIL | **N** |
| U56 | EWELIG | M@10 | 8.88% / 1.290 / −10.82% | 9.46% / 1.277 / −12.05% | 15.29% / 0.875 / −33.72% | FAIL | PASS | N |
| B136 | BAND03_G075 | W@10 | 7.85% / 1.102 / −12.24% | 7.85% / 1.102 / −12.24% | 15.26% / 0.874 / −33.72% | FAIL | FAIL | N |
| B136 | TOP20 | M@10 | 15.48% / 0.997 / −26.11% | 7.85% / 1.102 / −12.24% | 15.26% / 0.874 / −33.72% | FAIL | FAIL | N |
| B136 | EWELIG | M@10 | 7.82% / 1.135 / −11.94% | 7.85% / 1.102 / −12.24% | 15.26% / 0.874 / −33.72% | FAIL | PASS | N |

Path 4a: **10 of 216** d=0 cells (EWELIG 9/72, BAND03_G075 1/72, TOP20 0/72). Path 4b: 22 of 216,
all TOP20.

**The one OOS 4b pass is NOT a new candidate and is not proposed.** U56/TOP20/monthly at 10 bps
reads FULL 14.70% / 1.203 / −19.51% (H1 1.211, H2 1.204 vs SPY 0.957 / 0.826) and OOS 16.68% /
1.284 / −19.51%, so it clears 4b on FULL and OOS by the letter. It is the record's **own
2026-09-04 first KEEP-4b shape** (top 20 by the v1 composite, no vol scaler, gross 0.75/20) read
at its month-end phase — already published, and already de-certified twice: idea 879 found this
shelf passes **7 of 21** monthly offsets at gross 0.75, and idea 956 found U56/DOM21/TOP20 fails
**16 of 21** DOM phases (phase pass-share 0.238), the single fragile certification in its corpus.
This run reproduces that fragility from a third direction and adds the reason it cannot be fixed:
the pick's **OOS DD margin is +0.723 pp against its own OOS DD spread of 2.258 pp**, and that
spread is 100% path. No execution improvement, no cost rung, removes it. The other 4b passer,
U56/TOP20/weekly, is 5-of-5 offset stable on FULL and OOS but its DD margin (+1.922 pp) is still
under half its own DD spread (3.989 pp). **No memo is filed and no RULES change is proposed;
RULES.md, scan.py, bot.py and baseline.py are untouched.**

## Gates — 7/7 PASS
G1 local `run()+net()` ≡ `engine.backtest(W, 10 bps)` **0.000e+00**; G2 `offset_mask(·,0,R)` ≡
`rebalance_mask(·,R)` **4/4 cadences, 0 diffs**; G3 BAND03_G075 ≡ `baseline.rules_v2_weights`
**0.000e+00**; G4 cadence D offset masks identical, the structural zero, **0 diffs**; G5 cost
linearity `net(path,25)` ≡ full re-run at 25 bps **0.000e+00** (this is what makes B3 exact);
G6 clipping census published (clip-free offsets {0,1,2}; W: d3 = 2, d4 = 175) and B1 re-read on
them as B1c rather than the bar being widened; G7 SPY buy-and-hold offset-invariant by
construction.

## Limits, stated
**SURVIVORSHIP (PROTOCOL rule 9):** U56 and B136 are current-constituent lists, so every absolute
CAGR and drawdown here is optimistic. This run is a WITHIN-TAPE contrast — same names, same dates,
only the rebalance weekday and the cost rung move — which is what the idea asks; it does not
repair the level. The cost model is a flat bps-on-turnover bill, so a spread driven by
SLIPPAGE that varies by weekday (not by turnover volume) would be invisible here; the claim is
about the record's own cost convention, which is the convention every 4b verdict was scored under.
Cadence D is a structural zero by construction and is excluded from every share above.
