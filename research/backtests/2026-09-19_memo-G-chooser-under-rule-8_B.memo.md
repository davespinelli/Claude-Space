# KEEP-4b CANDIDATE memo for the Sunday review — the live book is UNDER-GROSSED, and the memo's own G rule says so
(idea 1454, lane B, 2026-09-19. PROTOCOL rule 6 reserves enactment for the Sunday review; NOTHING is
enacted here and RULES.md / bot.py / scan.py / baseline.py are untouched. Script:
`research/backtests/2026-09-19_memo-G-chooser-under-rule-8_B.py`.)

1. **What was tested.** The LIVE RULES v2 book, shape unchanged (`baseline.rules_v2_weights`: 200d
   ±3% hysteresis band, hold every IN name, de-gross to cash, never re-spread), with its ONE sizing
   number walked over G ∈ {0.25, 0.375, 0.50, 0.625, 0.75, 0.875, 1.00} × cadence {W, M} — 14 cells
   per panel on U56 / B136 / SMALL485, 42 in all, every one reported. Two tuned parameters exactly.
   No leverage: the ladder stops at G = 1.00 (PROTOCOL rule 2).
2. **The finding.** On U56, at the live weekly cadence, G = 1.00 clears ALL FIVE 4b legs full-sample
   AND out-of-sample: **CAGR 11.53% (floor 10.59%, +0.94 pp), Sharpe 1.201, MaxDD −15.91% (cap
   −20.23%, +4.32 pp), halves 1.228 / 1.180 vs SPY 0.957 / 0.825; OOS CAGR 12.67% / Sharpe 1.276 /
   MaxDD −15.91%** vs SPY OOS 15.26% / 0.874 / −33.72%. Turnover 2.35x/yr. The live G = 0.75 fails
   4b on the CAGR floor alone — the single bar RULES.md itself names — by **−1.97 pp full-sample and
   −1.22 pp OOS**, with all four other legs already passing.
3. **Rule 8 is clean and the choice is not a fit.** Both IS-only choosers, fit on 2009–2016 and read
   once on 2017–2026, pick G = 1.00. The licensable G set is **{0.875, 1.00}** at a 2017 split,
   **{0.875, 1.00}** at 2015 and **{1.00}** at 2019 — stable across all three splits, and the
   recommendation keeps the live cadence W rather than switching to the joint chooser's M pick.
4. **The memo that set 0.75 got its own rule backwards.** 2026-09-03_RECOMMENDATION.md pre-stated
   "smallest G whose MaxDD ≤ 60% of SPY's and CAGR ≥ 70% of SPY's; if none, keep 75%". On IS at
   weekly, NO rung clears the IS CAGR floor (best 10.16% at G = 1.00 vs 10.47%), so the FALLBACK
   fires and 0.75 is kept — which is how the live book came to sit below its own bar. On the full
   sample that same rule picks **G = 1.00**, not 0.75.
5. **This is a risk-budget finding, not an alpha finding — state it that way.** Sharpe is **1.201 at
   all seven weekly rungs** on U56 (invariant to 3 dp). G buys nothing risk-adjusted; it only moves
   the book along its own ray. The book has simply been run at three quarters of the exposure its own
   drawdown budget permits, and the 4b CAGR floor is exactly what that costs.
6. **Cost-robust to 25 bps, not to 50.** 4b passes FULL and OOS at 0, 5, 10 and 25 bps. At 50 bps the
   full-sample CAGR leg fails by 0.10 pp (10.49% vs 10.59%) while OOS still passes. The live 0.75
   fails the CAGR leg at **every** rung including 0 bps, so its failure is exposure, not friction.
   Caveat (idea 1063): the ladder is one-sided — SPY pays no turnover cost, so the bar never moves.
7. **Replication FAILS off U56 — the honest limit of this result.** 0 of 14 cells clear the two level
   legs on B136 and 0 of 14 on SMALL485, at all three splits. B136's G = 1.00 W passes 4b full-sample
   but misses the OOS CAGR floor by 0.21 pp (10.47% vs 10.68%); B136 at G = 1.00 M **breaches** the
   OOS DD cap (−20.50% vs −20.23%). U56 is a current-constituent list (idea 54), so the absolute CAGR
   this pass is built on is survivorship-optimistic and a full-gross book is the most exposed to that.
8. **4a fails everywhere: 0 of 42 cells.** Raising gross strictly deepens MaxDD against the live rules
   at an unchanged Sharpe, so this book never beats the book. It is a 4b-only candidate.
9. **Two further caveats the Sunday review must carry.** (i) C_BUDGET is DEGENERATE here — the IS DD
   cap binds at 0 of 7 rungs on all three panels, so "spend the budget" reduces to "take the ladder's
   ceiling", and the ceiling is 1.00 only because PROTOCOL forbids leverage. (ii) The 4b DD cap moved
   −13.24% (IS) → −20.23% (OOS) as SPY's own MaxDD went −22.06% → −33.72%: budgeting against the cap
   was conservative by luck in this window, and a shallower SPY decline would tighten it.
10. **EXACT RULES WORDING if the review adopts it** — a one-number change to clause 4, nothing else:
   > **4. Sizing:** each IN name is held at `1.00 / N` of current NAV (1.7857% at N = 56). Round
   > shares down to whole units. Names that are OUT are not held and **their weight stays in cash —
   > the book de-grosses.** Do NOT re-spread the gross over the IN names: a re-grossed book is a
   > different, unpriced book (idea 81).
   Clause 5's reset line becomes `1.00 / N` of NAV. Clauses 1, 2, 3, 6, 7, 8 unchanged; cadence stays
   weekly; version bumps to v3 with the acceptance table replaced by §2 above and the §7 limit stated.
   If the review declines the survivorship exposure in §7, the correct fallback is **G = 0.875**,
   which clears 4b OOS at both cadences and at the 2015 and 2017 splits but misses the full-sample
   CAGR floor by 0.52 pp — i.e. a partial, not a pass.
