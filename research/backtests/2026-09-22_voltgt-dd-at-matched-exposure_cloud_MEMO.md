# KEEP-4b CANDIDATE — idea 1537 (2026-09-22, lane cloud). Recorded, NOT recommended.

1. **BOOK.** U56. Top-20 by 126-day momentum among names above their 200-day MA with 20-day
   annualised vol < 0.60, equal weight at 0.75/20 of NAV, weekly, t+1 — the record's frozen
   2026-09-04 anchor shape — with every weight multiplied by `min(1, 0.20 / rv_t)`, `rv_t` the
   20-day annualised realised vol of the book's own returns through close t.
2. **EXACT RULES WORDING if ever promoted.** *"Clause 4 (exposure scalar). After clause 3 has set
   target weights, multiply every weight by `min(1, v / rv_t)`, where `rv_t` is the 20-day
   annualised realised volatility of this book's own daily returns through the decision close t
   and `v = 0.20`. `v` is chosen once on the trailing history available at the time as the
   in-sample Sharpe argmax over the ladder 0.06…0.30 step 0.02; on the 2009-2016 history that
   rule returns `v = 0.20`."*
3. **NUMBERS @10 bps, U56.** FULL 12.25% / 1.0741 / −16.70% (halves 1.0937 / 1.0609),
   OOS 13.39% / 1.1238 / −16.70%. Turnover **10.02×/yr**, realised mean gross 0.7174.
4. **COMPARANDS.** Live RULES v2 FULL 8.62% / 1.2010 / −12.05%, OOS 9.46% / 1.2767 / −12.05%.
   SPY FULL 15.14% / 0.8851 / −33.72%, OOS 15.29% / 0.8751 / −33.72%.
5. **4b.** PASS FULL *and* OOS at 0 and 10 bps. **Dies at 25 bps** (FULL CAGR 10.57% against the
   10.60% floor — a 0.03 pp miss) and again at 50. OOS margins at 10 bps: DD **+3.53 pp**
   (−16.70% vs cap −20.23%), CAGR **+2.69 pp** (13.39% vs floor 10.70%).
6. **4a: FAIL, 0 of 156 cells** on every panel and cost rung. Sharpe is below live RULES v2 in
   both halves and the drawdown is 4.65 pp deeper. This is a 4b-only candidate.
7. **RULE 8.** `v` is chosen on 2009-2016 alone by IS Sharpe and 2017-2026 was read once. The
   chooser picks v = 0.20, the second-loosest rung on the ladder — it turns the device most of
   the way OFF, which is the honest reading of the pick.
8. **WHY NOT RECOMMENDED — its own zero-parameter twin does the same job.** The matched-exposure
   constant de-gross anchor (same book, no scalar, gross scaled to the same realised 0.7174)
   reads FULL 12.20% / 1.0644 / −17.94%, OOS 1.1133, and **also clears 4b at 10 bps**. Over the
   whole ladder, **0 of 156 cells clear 4b-OOS where the anchor does not**, and 4 do the reverse.
   The device's whole edge over that twin here is +1.24 pp of drawdown (t = 2.22) and +0.0097 of
   full-sample Sharpe (se 0.0094) — and this rung is the one where the scalar barely binds; where
   it does bind (v = 0.06–0.12) the t on dMaxDD is 1.18–1.57 and the Sharpe difference turns
   NEGATIVE on U56 at every rung (−0.007 at v = 0.06, −0.025 at 0.08, −0.041 at 0.10, −0.024 at 0.12).
9. **AND IT IS A TURNOVER MONSTER.** 10.02×/yr against live RULES v2's 1.77× and against idea
   2264's standing candidate at 2.35×. A pass that dies at 25 bps is not a capital result.
10. **CAVEATS.** Survivorship (PROTOCOL rule 9): U56 is 2026 constituents held from 2008, so the
   CAGR level is optimistic and both 4b level legs are easier than on a point-in-time panel.
   Flat costs, no spread/impact/borrow. One cadence (W), one delay (t+1), one base shape
   (N = 20, H = 126). RULES.md / scan.py / bot.py / baseline.py untouched.
