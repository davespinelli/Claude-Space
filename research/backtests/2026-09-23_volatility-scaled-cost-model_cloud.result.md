# RESULT — idea 2395, does a volatility-scaled cost model move where the capped family dies?

**2026-09-23, lane cloud, run 44. ANSWERED = NO. KILL of the vol-scaled cost model as a
re-pricing device; CONFIRM of the record's cost conclusions. No rule changes; no new candidate.**
`RULES.md`, `scan.py`, `bot.py` and `baseline.py` are untouched.

1. **What was priced.** `cost_i,t = k x (vol20_i,t-1 / median_j vol20_j,t-1)^p x |dw_i,t|` on both
   candidate books (CAP2, the 2%-capped candidate; CAND, the uncapped `gross/N_in` candidate) on
   both panels, at p = 0.0 / 0.5 / 1.0 / 1.5, gross 0.75 and 1.00, rungs 0 / 10 / 25 / 50 bps,
   under three calibration conventions. 384 published rows, 14 of 14 gates.
2. **The level was held fixed so only the shape could move.** `k` is calibrated per book so the
   TOTAL bill equals the flat rung's total bill to machine precision (G5: max|d| 2.8e-17 over 64
   cells). The flat and scaled models therefore spend the *same money*, differently distributed.
3. **The headline.** Under the two pinned conventions, the highest 4b-passing rung is identical at
   all four exponents in **16 of 16** (panel, book, gross) cells, and **0 of 192** scaled rows flip
   their 4b verdict. Joint both-panel 4b is **9 of 24 at every exponent**, for both books.
4. **The premise was right about the mechanism and wrong about the consequence.** SHY's share of
   the bill collapses 22.87% -> 0.25% (U56 CAP2) as p goes 0 -> 1.5 while its share of turnover is
   unchanged at 22.87%. The book barely notices: max |dSharpe| over the 192 pinned rows is
   **0.0070**, max |dCAGR| 0.12 pp. The reallocation is near-orthogonal to the return path.
5. **Direction, measured.** 198 of 288 scaled rows LOSE Sharpe; only 18 gain (all U56 CAP2 at the
   live gross, by <= 0.0002). A volatility-proportional model is *harsher* on books that park a
   quarter of their turnover in SHY, because the refund on the cash sleeve is smaller than the
   extra charge on the equity rotation once the total is pinned.
6. **The one boundary move, reported not buried.** 1 of 24 (panel, book, gross, convention) cells
   moves — U56 CAP2, gross 1.00, convention CAUSAL, p=1.5, death rung 50 -> 25. CAUSAL calibrates
   `k` expanding from data through t-1 only and does NOT pin the bill: its realised total runs
   1.072x-1.325x the flat total at p=1.5. That cell fails `L_CAGR` by 0.08 pp after being charged
   up to 32% more money, so it is a LEVEL effect, not a shape effect. Pinned conventions: 0 of 16.
7. **Rule 8.** (book, gross) fitted on <= 2016-12-31 only, 2017-2026 read once, separately under
   each cost model: 192 picks, **192 of 192 beat SPY's OOS Sharpe under every exponent**, 192 of
   192 take gross 0.75. The model changes the PICK in 4 of 48 chooser cells and the VERDICT in 0.
8. **What this licenses.** Every committed "dies at 50 bps" in this record can now be read as a
   claim about HOW MUCH is charged rather than HOW it is charged. It does not license the 50 bps
   rung itself, and it says nothing about a cost model proportional to spread, ADV or trade size.
9. **Unchanged blockers.** 0 of 384 rows pass 4a. The binding leg on all 108 of 108 sub-50bps 4b
   FAILs is `L_DD` alone, and all 108 sit at gross 1.00.
10. **Survivorship (rule 9).** U56 and B136 are current constituents of their screens held from
    2008, so absolute levels are biased upward and `L_CAGR` is the contaminated leg. The
    flat-vs-scaled contrast is same-tape, same-weights and same-total-bill, so it is first-order
    immune; the absolute 4b verdicts are not.
