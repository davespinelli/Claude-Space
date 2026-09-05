# Memo — idea 152: the priced broad-POS book (PARK, not KEEP)

1. **Book, stated exactly.** Universe `universe_broad.json` (136 names). Weekly, decide at
   Friday close, execute next close, 10 bps per unit turnover, long-only, no leverage.
2. **Eligibility (unchanged from RULES v1).** Hold a name only if `close > 200d MA` and
   `vol20 < 0.60` annualised.
3. **Ranking key.** `composite x sqrt(vol20)`, where composite = mean of the percentile ranks of
   12-1 momentum, 6-month and 3-month return, times `0.5 + 0.5 * above200d`, and
   `vol20` is floored at 0.08 before the square root.
4. **Selection and sizing.** Hold the top **20** eligible names at **3.50% each** (target gross
   `m = 0.70`), rest in cash. Turnover runs ~14.3x/yr.
5. **Full sample (2009-01-13 → 2026-09-04, 10 bps).** CAGR **14.91%**, Sharpe **1.051**, MaxDD
   **-20.04%**, halves **1.196 / 0.926**, OOS Sharpe **1.004**. SPY: 15.23% / 0.889 / -33.72%,
   halves 0.957 / 0.834, OOS 0.882. RULES v1 on the same panel: 6.39% / 0.635 / -21.19%.
6. **4b margins at m = 0.70.** H1 +0.239, H2 +0.092, OOS +0.122, DD **+0.02pp**, CAGR +4.25pp.
   All five clear. The unlevered 4b interval is `m ∈ [0.55, 0.70]` (continuous ≈ [0.50, 0.74]);
   `m = 0.75` fails the DD cap by 1.14pp and `m = 0.50` fails the CAGR floor by 0.02pp.
7. **Rule 8.** Chosen on 2009-2016 by the 4b-aware IS screen, the family picks `POS / m = 0.60`
   and reads OOS 12.56% / **1.003** / -17.34% against SPY OOS 15.45% / 0.882 / -33.72% and
   RULES v1 OOS 5.94% / 0.576 / -21.19%. The OOS-window 4b passes. Plain IS-Sharpe picks
   `m = 1.00` and fails the OOS-window DD cap — the screen is load-bearing here.
8. **Why this is PARK and not KEEP.** Cross-universe 4b is **0 of 25** gross points: u56 passes
   only at `m >= 0.65`, and the sub-$2B panel fails **all five bars at every gross with this
   tilt**, because its own vol premium is signed the other way (idea 81). At 25 bps the whole
   family — every panel, every scaler, every gross — passes 4b **0 of 150** unlevered points.
9. **What it is not.** Per idea 144 a de-grossed book is the same book. This is idea 81's
   already-killed `x sqrt(vol20)` tilt run at a smaller risk budget, not a new signal. The
   drawdown gap was bought with 1.07pp of CAGR, not earned.
10. **If it were ever adopted, the RULES wording would be** — *"Rank eligible names by
    `composite x sqrt(vol20)`; hold the top 20 at 3.50% each (70% gross), weekly, next-close
    execution. Applies to the 136-name broad list only; not portable to the sub-$2B panel and
    not viable above ~15 bps."* **No RULES change is requested from this run.**
