# MEMO — the per-leg null percentile clause (idea 975-TRANCHE, lane B, 2026-09-16)

1. **Proposing NO RULES change and NO promotion.** RULES v2 stays live; `RULES.md`, `PROTOCOL.md`,
   `scan.py`, `bot.py`, `baseline.py` untouched (rule 6). This memo records one PROTOCOL rule 4
   reporting line for the Sunday review, and the evidence that makes the weaker existing clause
   insufficient.
2. **The finding.** Idea 964's only rule-8 OOS 4b pass — the 63-phase tranched `EWELIG` book on
   U56 at gross 0.75, quarterly, OOS **12.29% / 1.120 / −20.14%** — has a gross-matched tranched
   coin-flip 4b base rate of **0.000 of 200** under both null conventions, so it clears ideas
   926/942's existing base-rate clause outright. **It still is not a book with an edge.** Against
   that same null it sits at the **0.090 percentile on OOS Sharpe** (91% of coin flips earn a
   higher one), the **0.000 percentile on OOS CAGR** (all 200 earn more; median 13.56% vs 12.29%)
   and the 1.000 percentile on |OOS MaxDD|.
3. **Why the base rate alone cannot see this.** Per-leg, the null passes `L1_H1` / `L2_H2` /
   `L3_OOS` / `L5_CAGR` at 1.000 and `L4_DD` at **0.000**. A base rate of zero here means only
   that *one* leg is unpassable in that cell, not that the book beat anything. The whole verdict is
   a **0.09 pp** margin under the 4b cap of −20.23%.
4. **The mirror case proves the same point from the other side.** Idea 980's headline pick, U56/M
   `TOP20` @ 0.75 (OOS **16.68% / 1.283 / −19.51%**), is at the **0.995** Sharpe percentile and
   **1.000** CAGR percentile of its own null — genuinely strong — yet its cell's null base rate is
   **0.815**, and its tranched null's is **1.000**. Base rate and percentile disagree about which
   of these two books did something, and **the percentile is right both times**.
5. **The tranche is a passability device where phase-books differ.** On U56/`TOP20`/Q, tranching
   moves the NULL's median |OOS MaxDD| **22.20% → 20.13%** across the fixed cap and its 4b base
   rate **0.110 → 0.680**, while the real tranche there still fails. On `EWELIG`, whose 63
   phase-books are 0.951 correlated, it moves nothing (+0.000).
6. **Null convention is not a live axis, and this retires a standing caveat.** 926's independent
   per-phase RANDROT and a phase-coherent variant give phase-book correlations that differ by at
   most **0.0012** over 12 cells. The market factor dominates; no tranche null is over-diversified.
7. **Proposed PROTOCOL rule 4 reporting line, for the Sunday review to accept or reject — exact
   wording:** *"A 4b PASS is published with its own gross-matched null's **per-leg** pass rates and
   the book's **percentile within that null on OOS Sharpe, OOS CAGR and |OOS MaxDD|**, not the
   aggregate base rate alone. A pass whose base rate is low only because one leg is unpassable in
   its cell, and which sits below the null's median on OOS Sharpe, is reported as PARK."*
8. **What the clause costs, measured on this run.** It re-labels **1 of the 5** full-sample 4b
   passes here (the subject) that ideas 926/942's base-rate clause alone would let stand, and
   leaves the two it already catches (U56/`TOP20`/M at 0.815 and 1.000) caught. It changes no 4a
   verdict, because 4a is **0 of 24** at gross 0.75 on both panels.
9. **Scope, stated plainly.** 24 REAL cells and 36,000 null rows on two current-constituent
   panels at one gross, not the record's committed 4b corpus. Idea 998 is filed to re-score the
   record's committed passes against this clause. Gates 7 of 9: G3/G4 fail on the letter because
   the panel gained one trading day since idea 964 ran (in-sample columns reproduce at 1e-7, SPY's
   own OOS CAGR moved 15.27% → 15.21%), which is idea 890's defect, not a disagreement.
10. **Survivorship.** Current-constituent panels, so every null base rate is an **upper** bound and
    every percentile a **lower** one — the bias runs against this run's own suspicion, not for it.
    Turnover is reported but not matched; the null pays ~6 bp/yr more at 10 bps, also against the
    null. Nothing here justifies real capital beyond the live paper record.
