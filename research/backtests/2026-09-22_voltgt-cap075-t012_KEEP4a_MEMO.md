# KEEP-candidate memo (path 4a) — VOL-TARGETED GROSS ON THE LIVE BAND BOOK, CAP AT THE LIVE GROSS
# (idea 2260, lane C, 2026-09-22; evidence `research/backtests/2026-09-22_voltgt-gross-vs-constant-gross-at-matched-CAGR_C.py` / `.result.md`, gates 12/12)

1. **The book.** RULES v2 unchanged in every respect except sizing: hold every instrument inside
   the 200-day ±3% band, weekly, t+1, gated-out weight to CASH and never re-spread. Size the book
   at `g_t/N_t` with `g_t = min(0.75, 0.12 / sigma_20)`, `sigma_20` being the annualised 20-day
   realised vol of that same band book held at **unit** gross, read through the previous close.
   **Never levered** (the cap IS the live gross 0.75), so no financing is assumed anywhere.
   TWO tuned parameters and no more: TARGET (0.12) and CAP (0.75).
2. **Path 4a, FULL, U56 @10 bps:** 8.56% / **1.2150** / **−10.59%**, halves **1.2369 / 1.1974**,
   against the live RULES v2 book's 8.62% / 1.2010 / −12.05% (halves 1.2276 / 1.1806). Sharpe
   higher in BOTH halves, MaxDD **1.46 pp shallower**, for **0.06 pp** of CAGR and **0.05**
   turns/yr (1.824 vs 1.770). PASS.
3. **Path 4a, OOS (rule 8, 2017–2026 read once), U56 @10 bps:** 9.35% / **1.2958** / **−10.59%**
   against the live book's 9.46% / 1.2767 / −12.05%. PASS. SPY OOS 15.29% / 0.8751 / −33.72%.
4. **Replicates on the second panel and across the whole cost ladder.** B136 @10 bps FULL 7.87% /
   1.1079 / −10.70% (halves 1.2333 / 0.9826 vs live 1.2296 / 0.9669), OOS 7.78% / 1.1208 /
   −10.70% vs live 7.85% / 1.1017 / −12.24%. **4a passes 10 of 10 panel × cost cells on the FULL
   sample and 10 of 10 on the OOS window, at 0 / 5 / 10 / 25 / 50 bps.** No cost rung breaks it.
5. **Rule-8 reachable by the record's DEFAULT chooser, not a bespoke one.** `C_SHARPE` — the
   habitual IS-only chooser that idea 2264 showed blows the drawdown cap on the constant-gross
   ladder — picks exactly (0.12, 0.75) on U56 at **every one of the five cost rungs**, choosing on
   2009–2016 alone. 120 chooser rows published.
6. **Plateau, narrow but identically bounded on two panels.** On the CAP = 0.75 target ladder,
   4a passes at t = 0.12 **and** t = 0.15 on both panels and nowhere else: t = 0.10 fails on the
   H2 Sharpe leg, t = 0.20 fails because the scaler stops biting (mean scaler 0.7496; MaxDD equal
   to the live book's to the basis point).
7. **It does NOT clear path 4b** and is not offered as a growth rule: full CAGR 8.56% against the
   4b floor of 10.60%, a **−2.04 pp** miss. This is a risk-efficiency improvement to the live
   book, not a replacement for the 4b search. 24 of 720 cells clear 4a; 192 clear 4b on both
   windows, and none of those 192 clears 4a.
8. **THE CAVEAT THAT MUST BE WEIGHED (one convention wide).** The whole 4a gain lives at
   `sigma_20`. At **L = 63 and L = 126 the cell's MaxDD is exactly the live book's** (−12.05% /
   −12.24%) and 4a fails on every panel and cost rung, because at a slow σ the scaler is still
   pinned at the cap through the worst episode and the book simply *is* the live book through the
   drawdown. `sigma_20` is the convention the committed 2026-09-20 `voltgt` memo already uses and
   was written into this script's header before the run, so it is not selected on this run's
   numbers — but a Sunday review should read point 8 as the binding risk. SURVIVORSHIP: U56 and
   B136 are CURRENT constituents held from 2008, so every CAGR level above is optimistic.
9. **Proposed RULES wording** (rule 6 — Sunday review only; `RULES.md`, `PROTOCOL.md`, `scan.py`,
   `bot.py` and `baseline.py` are NOT modified by idea 2260):

   > **2. Sizing.** Hold every instrument that is inside the 200-day ±3% band that day (the band
   > clause is unchanged) at `g/N` of NAV, `N` being the count of instruments priced that day. At
   > each weekly rebalance set `g = min(0.75, 0.12 / sigma_20)`, where `sigma_20 = sqrt(252) ×`
   > the standard deviation of the last 20 daily returns of the band book held at unit gross,
   > computed through the previous close; between rebalances `g` is not re-read. Weight not
   > deployed sits in CASH, is never re-spread across the held names, and `g` never exceeds 0.75.
   > No ranking, no momentum screen, no per-name volatility filter.

10. **Status: KEEP-candidate, path 4a, awaiting Sunday review — with point 8 attached.** It is
    NOT proposed as a live rules change by this run. It does not compete with the standing 4b
    candidates (idea 2264's g = 1.00 book, the 2026-09-20 `voltgt` memos): it is on the other
    KEEP path and answers a different question — whether the live book can be made strictly safer
    at the same return rather than more profitable at more risk.
