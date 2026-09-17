# Idea 1189 — is the GROSS-RUNG DEGENERACY of SHARPE a UNIVERSAL property of the de-GROSSED book?

**Lane:** cloud, 2026-09-17, idea 1 of 2 (FIRST eligible open idea).
**Verdict: ANSWERED = YES, UNIVERSAL — and 6 of this run's 14 4b passes are the same anchor re-read. KILL as a capital finding.**

## Construction
Two dials and no more (rule 4): **GROSS RUNG** g ∈ {0.30, 0.40, 0.50, 0.60, 0.70, 0.75, 0.85, 1.00} × **ANCHOR** (N, cadence) ∈ {(20,W), (12,W), (30,W), (10,M), (20,M)}. Not dials, reported at every value: PANEL {U56, B136, SMALL}; the four statistics; the 4a/4b legs; the three rule-8 choosers. **3 × 5 × 8 = 120 books, every one published in `.grid.csv`.**

Book = the 2026-09-04 KEEP-4b family: composite (12-1 + 6m + 3m percentile ranks), **no vol scaler**, eligibility = above own 200d MA, top-N equal weight at g/N of NAV, gated-out weight to CASH at 0%. 10 bps per unit turnover, weights at close t applied t+1.

## (A) The rung-spread distribution — the degeneracy is universal
15 (panel, anchor) cells, 8 gross rungs each. Relative rung spread (max − min over the ladder, as a share of the cell's mean):

| statistic | median | min | max |
|---|---|---|---|
| **Sharpe** | **0.561%** | 0.026% | 4.027% |
| CAGR | 109.52% | 98.34% | 112.03% |
| MaxDD | 100.81% | 90.33% | 105.32% |
| turnover | 109.09% | 108.58% | 109.53% |

**CAGR/Sharpe spread ratio: median 199.7x (min 24.6x, max 4,277x).** Absolute Sharpe rung spread is **< 0.01 at 10 of 15 cells and < 0.05 at 15 of 15**; the worst cell in the whole grid is SMALL / N=10 / M at **0.02741** over a 3.33x change in gross. **Not one cell contradicts 1158's 8e-04 reading; it is the median case, not the exception.** Meanwhile the gross dial moves CAGR by ~100% of its own mean at every one of the 15 cells (G5) and |MaxDD| is non-decreasing in gross at 15 of 15 (G6).

Mechanism, and it is not an assumption: with a 0%-return cash sleeve the weight identity W(g) = g·W(1) holds by construction, so mean, vol and cost drag all scale by ≈ g and Sharpe cancels. **The residual is the sleeve's compounding, which G3 measures rather than assumes: max |r(0.30) − 0.30·r(1.00)| = 2.087e-03** (1177's finding, independently reproduced). That residual is the entire 0.026%–4.03% Sharpe spread.

## (B) What a 4b pass at a new gross rung actually is
**14 of 120 books clear 4b full and OOS at 10 bps; 1 of 120 clears 4a.** Those 14 sit on only **8 distinct (panel, anchor) cells — 6 of the 14 (0.43) are an anchor already counted, re-read at a different gross rung.** Within an anchor the Sharpe of the "different" books agrees to 1e-3 while the CAGR does not:

- U56 / N=20 / W at g = 0.60, 0.70, 0.75 → **Sharpe 1.14080 … 1.14099** (spread 1.9e-04), CAGR 11.32% … 14.18%, MaxDD −15.73% … −19.39%.
- U56 / N=20 / M at g = 0.60, 0.70 → Sharpe 1.19784 / 1.19880, CAGR 12.49% / 14.62%.
- U56 / N=30 / W at g = 0.70, 0.75 → Sharpe 1.14822 / 1.14822 (spread 4e-06).

**Per-leg failures over all 120 books: L_DD 70, L_H2 56, L_OOS 48, L_CAGR 41, L_H1 24.** The two legs the gross dial actually moves — L_DD and L_CAGR — are 111 of the 239 leg failures, and they move in OPPOSITE directions, which is the whole of what walking the ladder does: it slides a book along a CAGR-vs-drawdown line whose Sharpe is fixed. **A 4b pass found by lowering gross is not a new rule; it is the same rule with less of it.**

## (C) Rule 8 walk-forward — the gross dial is not a chooser dial
Chosen on < 2017, read 2017–2026 once. Benchmarks: U56 SPY 15.06%/0.8814/−33.72%, OOS 15.15%/0.8684; U56 RULES v2 live @10 bps 8.60%/1.1980/−12.05%, OOS 1.2714. B136 SPY 15.16%/0.8861/−33.72%, OOS 0.8767; B136 live 7.98%/1.0993/−12.24%, OOS 1.1059. SMALL SPY 14.06%/0.8581/−33.72%, OOS 0.8767; SMALL live 4.30%/0.6637/−13.89%, OOS 0.5600.

**Freeing the gross dial moves the chosen ANCHOR at 0 of 3 panels**, and changes OOS Sharpe by +0.0040 (U56), +0.0048 (B136), −0.0000 (SMALL). **But it is not free.** Because IS Sharpe is flat in gross, the IS-Sharpe argmax lands on the ladder's TOP rung g = 1.00 at 2 of 3 panels on noise of order 1e-3, and takes the drawdown with it: U56 picks N=10/M/g=1.00 → OOS 23.11% / 1.0069 / **−32.11%** against the frozen-gross pick's −25.03%. **CH_ISCALMAR is the control that proves the point: on SMALL it picks the SAME anchor at the BOTTOM rung g=0.30 → OOS 6.48% / 0.7354 / −13.15%, an OOS Sharpe identical to the g=1.00 pick's 0.7358 at a third of the drawdown.** Two "different" picks, one book.

**0 of 9 picks clear 4b; 1 of 9 clears 4a** (SMALL / CH_ISCALMAR, on the DD leg alone). 6 of 9 beat SPY OOS on Sharpe.

**The 14 passers are not rule-8 reachable.** Their IS-Sharpe ranks are 6, 12, 13, 17, 18, 19, 28, 29, 34, 35 of 40 on U56 and 6, 14, 36, 37 of 40 on B136 — none is the IS argmax. **No new KEEP candidate and no memo.** U56 / N=20 / W / g=0.75 is the standing 2026-09-04 incumbent, so its appearance here is CONFIRMATORY, not generative.

## Gates — 6 of 6 pass
- **G1** fast segment runner == `engine.backtest`: **2.08e-17**
- **G2** determinism: **0**
- **G3** cash sleeve breaks r(g) = g·r(1): **2.087e-03** (> 0 expected; 1177 reproduced)
- **G4** live RULES v2 U56 MaxDD **−12.0549%** against the record's −12.05%
- **G5** gross dial moves CAGR at every cell: min relative spread **0.9834**
- **G6** |MaxDD| non-decreasing in gross: **15 of 15 cells**

## Recommendation (not enacted — rule 6)
A future run should not count two books that differ only in gross as two 4b passes. The cheap, checkable form: **report a 4b pass keyed on (panel, N, cadence, H), with gross quoted as an attribute rather than as part of the key** — on this grid that alone collapses 14 claimed passes to 8. No RULES.md, PROTOCOL.md, scan.py, bot.py or baseline.py edit was made.

## Survivorship (rule 9)
U56 and B136 are CURRENT-CONSTITUENT lists; SMALL is the current output of a sub-$2B screen less the documented `max_1d_move >= 1.0` exclusion (52 of 715 dropped, 663 investable names plus SPY as benchmark only). Every CAGR and drawdown LEVEL is optimistic and every 4a/4b count is an UPPER bound, the 14 included. The bias largely cancels out of a RUNG SPREAD, which ranks one construction against itself on one tape; it does **not** cancel out of the rule-8 OOS levels.

## Artefacts
`..._cloud.py`, `.grid.csv` (120 books), `.spreads.csv` (15 cells), `.picks.csv` (9 rule-8 picks), `.gates.csv`, `.console.log`.
