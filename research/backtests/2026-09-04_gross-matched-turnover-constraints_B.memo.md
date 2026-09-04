# Memo — rank hysteresis on the ranked book (idea 79, surfaced by idea 86)

1. **What:** `CAND20/hyst2` — idea 2's standing 4b KEEP, plus one change: a held name is kept while its
   composite rank stays inside the top **40** (2×n) instead of the top 20. Freed slots refill from the best
   unheld names. No signal, gate, gross or cadence change.
2. **4b PASS on universe.json (56):** 12.7% CAGR / **1.145** Sharpe / **−17.2%** MaxDD, halves 1.169 / 1.133,
   OOS 1.231 — vs SPY 15.3% / 0.890 / −33.7%, halves 0.957/0.837, OOS 0.884. 4b bars all cleared.
3. **Strictly dominates the standing candidate** on u56: Sharpe 1.145 vs 1.093, MaxDD −17.2% vs −18.3%,
   OOS Sharpe 1.231 vs 1.170, turnover **3.91x/yr vs 9.63x** — same CAGR (12.7%).
4. **Rule 8:** `k = 2` is what the pre-registered IS rule (best 2009–2016 Sharpe) picks on **both** universes,
   and it beats its own control OOS on both (u56 1.231 vs 1.170; broad 0.939 vs 0.894), and SPY on both.
5. **Gross-matched:** `gm=on` moves every hysteresis number by ≤0.001 (dGross 0.000), so this is a holding-
   period effect, not the exposure artefact that killed `budget-top`. It is the only instrument in idea 86
   that improved CAGR *and* MaxDD *and* turnover at once.
6. **Not significant on Sharpe:** t(dSharpe vs control) = 0.00…+1.70 across the six (universe, k) cells.
   The claim that survives testing is *40–60% less turnover at no measured cost*, not *higher Sharpe*.
7. **Fails 4b on universe_broad (136)** on H2 (0.831 vs SPY 0.837) — the same bar its control fails, by a
   smaller margin (control 0.814). So this is a u56-scoped candidate, exactly like idea 2's.
8. **Cost/survivorship:** breakeven not re-measured here; at 25 bps `hyst2` keeps a 5.7x/yr turnover edge over
   the control, so it should be *more* cost-tolerant, but idea 45's protocol has not been run on it. The
   survivor panel understates turnover, which flatters the control more than the candidate.
9. **Recommended to Sunday review:** adopt only as a turnover clause on the existing candidate, not as a new
   book, and only after idea 45's cost/lag sweep. Not a RULES change this week.
10. **Exact RULES wording if adopted** (replaces the position-count sentence, no other clause changes):

> Hold the top 20 eligible names by the composite score, equally weighted at 3.75% each (75% gross).
> **A name already held is retained until its composite rank falls outside the top 40; vacated slots are
> filled by the highest-ranked eligible names not currently held.** Rebalance weekly.
