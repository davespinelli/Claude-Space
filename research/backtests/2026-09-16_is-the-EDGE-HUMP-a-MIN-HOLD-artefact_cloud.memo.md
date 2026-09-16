# Memo — the U56 `n = 12, H = 21` 4b candidate, in tradable wording (idea 1086, cloud lane, 2026-09-16)

1. **Status.** A PROTOCOL **4b** pass on U56, full sample **and** out of sample, and the **first in
   this family that an honest IS-only procedure reaches**: U56's IS(2009-2016) Sharpe chooser picks
   exactly (n = 12, H = 21) out of the 27-cell grid. Idea 1082 found three 4b passes on the same
   construction and reached **none** of them. **This lane does NOT recommend promotion.** Rule 6
   permits one rules change per week via Sunday review; this memo puts the candidate on file in
   exact form so the decision is made on the wording rather than on a description of it.
2. **Exact RULES wording, if it were ever promoted:**
   *"On the last trading day of each week, score every instrument priced that day by the mean of
   its percentile ranks on three momentum legs — return from 252 to 21 trading days ago, return
   over the last 126 days, return over the last 63 days — multiplied by 1.0 if its close is above
   its 200-day moving average and by 0.5 otherwise. An instrument is ELIGIBLE if its close is above
   its 200-day moving average and its 20-day realised volatility is below 60% annualised. RETAIN,
   regardless of eligibility, every currently-held name entered fewer than 21 trading days ago that
   is still priced. Then fill the remaining slots, up to 12 held names in total, with the
   highest-scoring ELIGIBLE instruments that are not among those retained — a name held 21 trading
   days or longer competes for its own slot on equal terms with every other eligible instrument,
   and its holding clock restarts if it is re-selected. Weight every held name equally at 0.75 of
   NAV divided by the number held, whatever that number is; the remaining 0.25 of NAV is cash.
   Weights are decided at that close and applied the next trading day. Costs 10 bps per unit
   turnover."*
3. **What it delivers, rule 8, OOS 2017-2026 read once:** CAGR **17.57%**, Sharpe **1.1426**,
   MaxDD **−19.48%**, against SPY OOS 15.21% / 0.8711 / −33.72% and the live RULES v2 book (OOS
   9.45% / 1.2762 / −12.05%). Full sample **16.80% / 1.1625 / −19.48%**, H1 **1.248** / H2
   **1.102** against SPY's 0.9588 / 0.8207. Mean 11.3 names held; turnover **7.19x/yr**, i.e.
   **72 bp/yr** of drag already charged at the binding 10 bps.
4. **Reason 1 not to promote — the binding leg is not decidable at this sample length.** All five
   legs pass, but drawdown binds with a margin of **+0.753 pp** (|−19.48%| against the 60%-of-SPY
   cap of 20.23%). Idea 1083 measured the 90% width of exactly this quantity on exactly this tape
   at **4.1 to 7.2 pp**. The margin is a fifth of the ruler's smallest division.
5. **Reason 2 — it does not survive the panel change.** The identical construction on B136 reads
   **16.41% / 0.9840 / −26.84%** and fails 4b outright; B136's own four IS choosers all pick
   (n = 5, H = 63), which also fails. A rule that clears on one current-constituent panel and not
   the other is a cell, not a rule.
6. **Reason 3 — the hold is not stably choosable.** `H_ISHOLD` FAILS: U56's four IS-only choosers
   split **21 / 21 / 63 / 63** and B136's all pick 63. Half of U56's own choosers would have
   selected a hold whose cells fail 4b on drawdown at every n.
7. **Reason 4 — it clears no 4a, and neither does anything else here.** **0 of 54 cells** pass 4a.
   Promoting this would trade the live book's 1.2007 / −12.05% for 1.1625 / −19.48% in exchange for
   CAGR — the same trade the record has refused on `BAND03@g1.00` four times over.
8. **Reason 5 — it is the most cost-exposed member of its family.** At H = 21 the book turns over
   **7.19x/yr** against **3.04x/yr** at 1082's H = 126 for the same n = 12. Every basis point added
   to the cost assumption costs this candidate 2.4× what it costs the incumbent hold, and this run
   priced it at 10 bps only (filed as idea 1094).
9. **Evidence.** Gates **10 of 10**, printed before any result number: the fast runner and the
   bisection kernel agree with `engine.backtest` to 1.39e-17; 936/1071/1082's committed W/H126
   N = 20 triple reproduces to 3.18e-07; **all 18 of 1082's committed H = 126 EDGE rungs reproduce
   to 4.80e-03 pp**; SPY OOS to 1.70e-04; live RULES v2 MaxDD to 4.95e-05. Script
   `2026-09-16_is-the-EDGE-HUMP-a-MIN-HOLD-artefact_cloud.py`, grid and rule-8 CSVs committed.
10. **Survivorship (rule 9).** U56 is a CURRENT-CONSTITUENT list, so every level in §3 is optimistic
    and the 4b pass is an **UPPER** bound; the 4b legs are measured against SPY, a real index, so
    the bias does not cancel out of them. `RULES.md`, `PROTOCOL.md`, `scan.py`, `bot.py` and
    `baseline.py` are untouched by this run.
