# MEMO — idea 1358 (lane cloud, 2026-09-19): pay the residual a coupon, not zero

1. **FINDING.** Routing the incumbent's uninvested gross into **SHY** instead of 0% cash adds
   **+0.0466 full / +0.0535 OOS Sharpe, +0.57 pp CAGR and 0.38 pp of drawdown room** on U56 at the
   frozen gross 0.60 — the only effect in this run that is RESOLVABLE (paired 63-row block
   bootstrap, 400 reps: |t| > 2 on **9 of 9** SHY cells full AND OOS; IEF 0 of 9, TLT 0 of 9).
2. **IT IS NOT ALPHA, IT IS A MEASUREMENT CORRECTION.** Every de-grossed book in the record
   (1296, 1346, 794, 1297) pays its residual 0%/yr. SHY is what idle cash actually earns. The gain
   is therefore an understatement the record has been carrying, not a new edge, and it scales with
   (1 − gross): +0.069 / +0.047 / +0.023 of Sharpe at g 0.50 / 0.60 / 0.75, on all three panels.
3. **AS A TUNED DIAL THE AXIS IS A KILL (rule 8).** The (SLEEVE, GROSS) pair chosen on 2009–2016 IS
   Sharpe picks IEF@0.50 / IEF@0.50 / TLT@0.50 and delivers **mean −0.0082 OOS Sharpe against doing
   nothing** (worst −0.0541, better on 2 of 3). The chooser never finds SHY, which is the ex-post
   best OOS cell on **3 of 3** panels. Duration is an IS mirage: TLT's OOS dSharpe is negative at
   **9 of 9** cells and its 2022 costs the U56 book −14.9% against cash's −1.6%.
4. **4b, SCORED WITHOUT A CHOOSER.** U56 SHY@g0.60 full **14.24% / 1.2182 / −16.00%**, halves
   **1.290 / 1.177** (SPY 0.957 / 0.825), OOS **15.91% / 1.2500 / −16.00%** (SPY OOS 0.8738; bars
   DD −20.23%, CAGR floor 10.59%). **All four 4b legs pass full AND OOS**, and it dominates the
   frozen (CASH, 0.60) incumbent on Sharpe, CAGR and MaxDD at once. B136 SHY@g0.60 does the same
   (1.1063 / 1.0888 OOS). **4a KILL** — H2 1.177 vs the live book's 1.1808, short by 0.004.
5. **VERDICT: 4b KEEP-CANDIDATE for the SUBSTITUTION, KILL for the DIAL.** Enact only as realism,
   with gross left exactly where it is; do not let the sleeve become a tuned knob.
6. **EXACT RULES WORDING (proposed, Sunday review only — rule 6):**
   > *Residual.* Gross not invested in the selected names is held in **SHY** (1–3y US Treasury
   > ETF), rebalanced on the same weekly grid as the book and charged the same 10 bps per unit of
   > turnover. It is never shorted and never levered: invested weight plus residual weight equals
   > 1.0. SHY remains separately selectable by the score; a name may be held both ways.
7. **CAVEATS.** (a) 2009–2026 holds the largest bond bull market on record; SHY's own standalone
   CAGR is only **1.31%** and its edge here is carry, not duration — that is precisely why SHY
   survives and IEF/TLT do not. (b) The gain shrinks to +0.023 Sharpe by gross 0.75 and vanishes at
   gross 1.00, so it is worth exactly as much as the book is de-grossed. (c) Turnover rises
   2.46 → 2.71/yr (drag 24.6 → 27.1 bp/yr), already netted out of every number above.
   (d) Survivorship: U56/B136/SMALL are current-constituent lists (rule 9); the SLEEVE tickers are
   not survivorship-affected. (e) SMALL fails 4b at **0 of 12** cells with or without a sleeve —
   the sleeve fixes nothing there.
8. **NOT RECOMMENDED FOR ENACTMENT THIS WEEK** on its own: it changes no selection and no exposure,
   so it can ride the next RULES change. What it DOES require is a PROTOCOL note that every
   published de-grossed book in the record understates itself by (1 − gross) × the T-bill return.
9. **GATES 7/7**, including a cross-script replay of ideas 1296/1346's committed anchor to
   **4.4e-16 / 1.1e-16 / 8.3e-17** on U56 / B136 / SMALL — the sleeve runner collapses exactly onto
   the cash runner when the sleeve is CASH.
10. Script `research/backtests/2026-09-19_does-routing-the-incumbent-s-UNINVESTED-GROSS-into-a-BOND-SLEEVE-buy-the-BINDING-4b-DD-LEG_cloud.py`; 36 cells + 42 controls + 27 bootstrap rows all published.
