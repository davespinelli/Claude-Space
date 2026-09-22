# KEEP-candidate memo (PROTOCOL path 4b) — idea 2300, lane cloud, 2026-09-22

1. **The book.** RULES v2's band and cadence, clause 4 REPLACED by a full re-gross, plus a T-bill sweep on
   the residual NAV. Exact wording, to replace clauses 4 and 5's sizing sentence if a Sunday review adopts it:
   *"**Sizing:** each IN name is held at `0.75 / N_in` of current NAV, where `N_in` is the number of IN names
   that day (not the universe count N). Round shares down to whole units. The residual `1 - sum(w)` of NAV is
   held in **SHY** and is reset on the same weekly schedule as the equity legs."*
2. **Numbers, U56, weekly, next-day execution, 10 bps, 2009-01-13 to 2026-09-18** — CAGR **12.55%**, Sharpe
   **1.1896**, MaxDD **-17.39%**, halves **1.2378 / 1.1593**, OOS 2017- **13.77% / 1.2332 / -17.39%**, turnover
   4.40x/yr. SPY: 15.14% / 0.8851 / -33.72% (OOS 15.29% / 0.8751). Live RULES v2: 8.62% / 1.2010 / -12.05%.
3. **Why 4b and not 4a.** All five 4b legs clear (H1, H2, OOS Sharpe > SPY; MaxDD 17.39% <= 0.60 x 33.72% =
   20.23%; CAGR 12.55% >= 0.70 x 15.14% = 10.60%). It FAILS 4a: its drawdown is 5.3 pp worse than the live
   book's, which is the trade 4b was written to allow.
4. **It travels to B136**: 11.99% / 1.0930 / -18.11% (OOS 1.0994), 4b FULL and OOS, at 0 / 10 / 25 bps on both
   panels. It **fails at 50 bps** on both, and it clears **nothing on SMALL** (0 of 120 cells there).
5. **Rule 8 (walk-forward).** With both dials chosen on 2009-2016 only and 2017-2026 read once, `C_ISCALMAR`
   picks exactly this cell on U56 and it PASSES 4b out of sample; `C_ISSHARPE` picks RG50/phi=1 (OOS 11.99% /
   1.3072 / -14.21%), also a 4b OOS pass. On B136 and SMALL neither chooser reaches a 4b passer.
6. **Concentration is the risk this book adds.** Re-grossing over `N_in` means the per-name weight is
   `0.75 / N_in`: median 1.79% of NAV, but 10.1% at the 99th percentile and **15.0% on the worst day**
   (5 names IN). 1.01% of days carry a position above 10% of NAV. The live book never exceeds 1.34%.
7. **The sweep is worth +0.3 to +0.7 pp of CAGR and ~+0.03 of Sharpe on every arm**, and it is NOT what makes
   this cell pass: RG100 at phi=0 already clears 4b (12.19% / 1.1568 / -17.71% at 10 bps). Idea 2119's law
   holds — the pass lives at total gross 1.00.
8. **What the same run says about the live rule.** De-gross is still the right side of the trade: d(Sharpe) =
   DG - DEVICE widens with carry at 15 of 15 cells, no CAGR or MaxDD verdict moves, and every verdict that
   moves at 0/10/25 bps moves INTO de-gross's favour. This candidate wins on the CAGR floor alone.
9. **Not adopted here (PROTOCOL rule 6).** Rules change only via a Sunday review, one change per week, and
   this would be TWO changes to RULES.md (clause 4's de-gross ban from idea 81, plus a new cash sleeve).
   It also needs >= 8 weeks of live tracking under PLAN Tier 3 before any capital.
10. **Survivorship (rule 9).** U56 and B136 are current-constituent lists held from 2008, so the absolute
    12.55% is optimistic; the margin over the live book is same-names, same-days and much less exposed, but
    the 4b CAGR leg is an ABSOLUTE bar and is the leg most contaminated by this bias.
