# MEMO — KEEP-4b candidates BY THE LETTER, recorded and NOT recommended (idea 2098, 2026-09-22, lane cloud)

1. CANDIDATES: U56 panel, **top-40 equal-weight at gross 1.00 (2.5% of NAV per name), monthly
   trade, fills t+1, 10 bps** — reached this run at three (definition, q) settings under three
   different ranking families: MOM/40/1.00 (q=0.30, both near-high definitions), MADIST/40/1.00
   (q=0.40 — idea 2083's candidate, reproduced exactly) and MOMVS/40/1.00 (VOL60, q=0.80).
2. PATH: 4b only. **4a FAILS on all three and on 0 of 165 grid points**: FULL MaxDD −17.7% to
   −18.2% is worse than live RULES v2's −12.05%. Nothing here challenges the live book on 4a.
3. NUMBERS (FULL / OOS, 10 bps, t+1): MOM/40 14.56%/1.195/−17.96% and 16.17%/1.297/−17.96%;
   MADIST/40 14.57%/1.197/−17.67% and 16.24%/1.310/−17.67%; MOMVS/40 14.29%/1.195/−18.17% and
   15.51%/1.276/−18.17%. Halves clear SPY on all three.
4. SPY: FULL 15.14%/0.885/−33.72% (halves 0.957/0.826), OOS 15.29%/0.875/−33.72% → 4b bars
   DD −20.23%, CAGR 10.60% FULL / 10.70% OOS. All seven legs clear on all three books.
5. LEGAL IS-only chooser (rule 8, 2009–2016 only, 2017–2026 read once): over the 80-book shelf,
   regress each book's drawdown ON QUIET DAYS ONLY on its IS SPY beta and take the largest
   positive residual; quiet = SPY within the q-th IS percentile of its distance from the running
   high. This run's own ARM 4 shows that chooser is **worth less than a uniform draw from the
   same shelf** (5 of 27 U56 picks clear against a 20-of-80 = 25.0% base rate).
6. ROBUST: 4b holds at **24 of 24** cost {0,10,25,50} bps x signal-lag {0,+1d} cells on all three
   books. A +1-day lag spends ~1.9 pp of the 2.3–2.6 pp drawdown margin.
7. WHY NOT RECOMMENDED: at U56 / k=40 / gross 1.00 **all four shelf families clear 4b** (LOWVOL
   too, OOS 1.2304). The pass is a CELL fact — top-40 of a 56-name current-constituent list at
   full gross — not a family, chooser or quiet-tape fact. The binding margins are 2.27–2.56 pp of
   drawdown, and idea 2090 (this lane, earlier today) found that margin unresolvable at 95% on
   the MADIST/40 twin. Three books with a common cell and one shared binding leg are ONE
   candidate, not three.
8. EXACT RULES WORDING (were any of these proposed at a Sunday review — NOT proposed here):
     "On the last trading day of each month, rank every U56 name whose close is above its 200-day
      moving average and whose 20-day annualised realised vol is below 0.60 by RANKER, descending.
      Hold the top 40 at 2.5% of NAV each; if fewer than 40 names qualify, hold only those that do
      and leave the remainder in CASH (never re-spread, never lever). Hold the positions unchanged
      between month-ends. Weights decided at close t apply at t+1. Costs 10 bps per unit turnover."
     RANKER = (close / 200-day moving average − 1) [MADIST]; or the scan.py composite without the
     vol scaler [MOM]; or the scan.py composite with it [MOMVS].
9. SURVIVORSHIP (rule 9): U56 is a CURRENT-constituent 56-name list. LEVELS are optimistic and
   the 4b bar is easier here than on a point-in-time panel — the 25% shelf base rate is itself a
   survivorship number. Treat every CAGR and MaxDD above as an upper bound.
10. RELATION TO RECORD: this run reproduces idea 2083's candidate to 4 dp (gate G1b) and answers
    its open threshold question — q = 0.40 is a true interior argmax, not a boundary pick — while
    removing the reason to credit the quiet-tape statistic for the pass. Against the standing 1795
    candidate (OOS 15.40%/1.357/−15.90%) these carry more OOS CAGR, less OOS Sharpe and a deeper
    drawdown. The live question the record should price next is the **top-40 / gross-1.00 U56
    cell itself**, stripped of every chooser — which ideas 2079 (gross 0.75) and 2083 (gross 1.00)
    already bracket.
