# 4b memo — U56 MA-RESPREAD, gross 0.75 (lane C, 2026-09-11, idea 773) — **NOT PROPOSED FOR PROMOTION**

1. **What it is.** RULES wording: *"Hold, equal-weight, every U56 name trading above its own
   200-day simple moving average; spread `gross = 0.75` of NAV across exactly those names
   (RESPREAD — the gated-out weight is re-spread over the survivors, never held as cash); the
   remaining 0.25 of NAV is idle at 0%; rebalance weekly (W) or monthly (M); 10 bps per unit
   turnover, next-day execution, no shorting, no leverage."* No ranking, no vol filter, no band.
2. **How it got here.** It is **not this idea's deliverable.** Idea 773 is a measurement run about
   panel-ordering claims; this book is one of the 36 REAL-parent books rebuilt only to satisfy
   PROTOCOL rules 4 and 8. Nothing about it was tuned here.
3. **Full sample (2009-01-13 →), W / M:** CAGR **11.55% / 12.60%**, Sharpe **1.0914 / 1.1594**,
   MaxDD **−18.62% / −18.21%**, halves 1.1807/1.0260 and 1.2207/1.1151. Turnover 7.60x / 3.26x/yr.
4. **OOS (2017-01-01 →, read once):** W **12.37% / 1.1078 / −18.62%**; M **13.60% / 1.1930 / −18.21%**.
5. **vs SPY (the 4b comparand):** SPY 15.11% / 0.8835 / −33.72%, halves 0.9595/0.8211, OOS 0.8721.
   All five 4b legs pass on both cadences: H1 ✓, H2 ✓, OOS Sharpe ✓, MaxDD ≤ 60%·33.72% = 20.23% ✓,
   CAGR ≥ 70%·15.11% = 10.58% ✓. **4b PASS (W and M). 4a FAIL** — 0 of the 36 real-parent books
   clear 4a; RULES v2 beats it on OOS Sharpe (1.2747 vs 1.1078 / 1.1930).
6. **Why it is NOT proposed.** (a) It is a **byte-identical reproduction** of lane B's same-day
   committed `.keeppaths.csv` rows — 0 mismatches over all 900 books — not a new finding.
   (b) It is a **single-rung gross pass**: at g=0.50 the CAGR floor binds (7.69% W / 8.34% M against
   the 10.58% floor) and at g=1.00 the DD cap binds (−24.29% / −23.73% against the −20.23% cap);
   only g=0.75 is clean, which is the knife-edge idea 675 already flagged
   and idea 677 proposes to replace with a gross-window width.
7. **Sibling.** `B136 MA-RS g0.75 W` passes 4b on the same rung (11.66% / 1.0586 / −20.12%,
   OOS 11.97% / 1.0660); its M twin fails on DD. The pass is not panel-specific, it is gross-specific.
8. **Against the incumbent.** The standing 2026-09-04 KEEP 4b (top-20 equal weight, no vol scaler)
   and the live RULES v2 both beat this book on OOS Sharpe; its only advantage is OOS CAGR
   (13.60% vs 9.45%), bought with 6.2 pp more drawdown.
9. **Survivorship.** U56 is a current-constituent list; the level statistics carry that premium.
10. **Status.** Recorded for the census, **no RULES change requested**, no Sunday-review proposal.
