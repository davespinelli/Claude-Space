# KEEP-candidate memo (path 4b) — NF20 + VOLCAP, 75% gross, weekly

1. **Object.** Idea 335's standing parent (top-k = min(20, E_t) of the eligible set, equal
   weight, no vol scaler, weekly, t+1, 75% gross) with a **book-level volatility cap**: scale the
   whole book by `m_t = min(1, target / vol20_ann(book)_{t-1})`. Two dials only, gross and target.
   Offered for comparison at Sunday review, **not** proposed as a rules change this week.
2. **Rule 8 first.** The target is chosen on **2008–2016 IS Sharpe @10 bps alone** and 2017–2026
   is read once: the chooser picks **0.18 on U56** and **0.20 on B136**, both at g = 0.75.
   Chooser regret against the OOS oracle **−0.0069**; the rival IS c*_4b chooser is worse
   (**−0.0626**, 3/6 vs the parent) and is rejected.
3. **Numbers, U56 (2009-01-13..2026-09-04, weekly, t+1, 10 bps):** CAGR **12.7%**, Sharpe
   **1.084**, MaxDD **−15.3%**, halves **1.091 / 1.083**, OOS Sharpe **1.150**, turnover
   **10.9×/yr**, mean gross 0.740, capped on **6.5%** of days.
4. **4b bars on U56, all five cleared:** H1 1.091 > SPY 0.957; H2 1.083 > 0.834; OOS 1.150 >
   0.882; MaxDD −15.3% ≥ −20.23% (60% of SPY's −33.72%); CAGR 12.7% ≥ 10.66% (70% of 15.23%).
5. **It clears 4b on B136 too** (13.1% / 0.982 / −18.1%, halves 1.126 / 0.853, OOS 0.934) — the
   first VOLCAP arm in the record to clear the path on both panels — but the H2 margin there is
   only **+0.019**, one bad half from failing.
6. **Against the un-capped parent it is SMALL:** +0.014 OOS Sharpe on U56 (+0.051 on B136) and
   −0.1 pp of CAGR; what it actually buys is **3.0 pp of drawdown** (−15.3% vs −18.3%). Judge it
   as drawdown insurance bought with a second dial, not as a return improvement.
7. **4a: FAILS, 0 of 54 cells at every rung.** Against live RULES v2 (1.2056, −12.05%) it loses
   both halves and 3.2 pp of drawdown. 4b-only, like every candidate in this family.
8. **Cost.** Breakeven **23.9 bps** on U56, 11.8 on B136; the family clears 4b in **21/54** cells
   at 10 bps and **0/54 at 25 bps**. At ~11×/yr turnover this is a cost-fragile book and idea 58's
   cost wall is unclosed.
9. **Survivorship.** U56 and B136 are current-constituent lists and B136 contains U56, so the
   CAGR figures are optimistic, the two panels are not independent, and the CAGR floor is the bar
   this flatters most.
10. **Exact RULES wording if ever adopted** (not proposed this week; PROTOCOL rule 6 allows one
    change per week and this run proposes none) — inserted as a new clause after v2's clause 4:

    > **4b. Book-level volatility cap.** After clause 4 has sized the book, compute the trailing
    > 20-trading-day annualised standard deviation of the book's own daily returns as of the
    > **previous** close, `v`. Multiply every position weight by `m = min(1, 0.18 / v)`; the
    > withheld weight stays in **cash** and is never re-spread. `m` is recomputed **every
    > trading day** from the previous close and the book is re-scaled to it the next day — this
    > is what was backtested, and it is a **daily** clause on an otherwise weekly book, so it
    > re-introduces the intra-week trading v2's clause 6 removed. Before 20 book returns exist,
    > `m = 1`.
