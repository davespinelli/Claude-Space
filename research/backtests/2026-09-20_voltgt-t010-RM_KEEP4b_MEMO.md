# KEEP-candidate memo (path 4b) — PANEL VOL-TARGET AT `t = 0.10` WITH A MONTHLY SCALAR REFRESH
# (idea 1803, lane B, 2026-09-20; filed under that run's pre-stated rule V4)

1. **The book.** Hold every priced name in the panel at equal weight — no ranking, no band, no
   per-name vol filter — and scale the whole book by `g = clip(0.10 / sigma_20, 0, 1)`, where
   `sigma_20` is the annualised 20-day realised vol of the *unlevered equal-weight panel*
   portfolio read through yesterday's close. `g` is **re-read MONTHLY**; the equal-weight
   re-spread of the names runs monthly (weekly costs 0.015 of FULL and 0.022 of OOS
   Sharpe and 0.68 more turns/yr — see point 4). 10 bps,
   next-day execution, never levered. ONE tuned parameter (`t`); the refresh cadence is the
   second dial and is what this memo fixes at M.
2. **Path 4b, FULL, U56 (T=M):** 13.31% / 1.2437 / −19.39%, halves 1.323 / 1.170, against SPY
   15.12% / 0.8843 / −33.72% (halves 0.9570 / 0.8249). All four legs clear; binding leg: none.
3. **Path 4b, OOS (rule 8, 2017-2026 read once), U56:** **13.81% / 1.2822 / −19.39%** against SPY
   15.26% / 0.8737 / −33.72% and live RULES v2 9.46% / 1.2766 / −12.05%. PASS. Turnover 1.91 /yr
   against the live book's 1.77.
4. **Replicates on the second panel and the second trade cadence.** B136 T=M FULL 13.16% /
   1.2014 / −19.87%, OOS 13.05% / 1.2000 / −19.87%; U56 T=W FULL 13.23% / 1.2292 / −19.62%, OOS
   13.67% / 1.2605 / −19.62% at 2.59 turns/yr. All 4b FULL and OOS PASS.
5. **Cost-durable where the record's other candidates are not:** 4b FULL *and* OOS PASS at
   **0 / 10 / 25 / 50 bps** on all three arms. Idea 1793's `t = 0.08, R = M` candidate fails at
   50 bps on the CAGR floor; the standing `t = 0.16, R = W` memo fails at 50 too.
6. **It trades the two-sided squeeze rather than escaping it.** Margins at 10 bps (U56 T=M):
   CAGR floor **+2.73 pp**, DD cap **+0.84 pp**. Idea 1793's cell is the mirror image (+0.68 pp
   CAGR, +4.10 pp DD). Neither is comfortable on both legs; a Sunday review choosing between them
   is choosing which leg to be thin on.
7. **It does NOT clear path 4a** (0 of 60 U56 cells at 10 bps). The six 4a passers in idea 1803's
   grid are all B136 and all against the live book restated on B136 — the artefact ideas 1763 and
   1793 already named. 4a remains the wrong bar for a book that runs mean gross 0.79.
8. **THE CAVEAT THAT MUST BE WEIGHED (thin chooser support).** On U56 this cell is reached by
   exactly **1 of 24** legal IS-only choosers in idea 1803's cross (`F_LEGS@0` — leg count priced
   at 0 bps); on B136 T=M by 4 of 24 (`F_LEGS` at every `c_IS`). `F_LEGS` is the family idea 1783
   killed for degeneracy on the name-set axis. The CELL clears every bar asked of it; the CHOOSER
   that finds it is **not** certified here, and `t = 0.10` also sits inside idea 1771's
   convention-robust band, which is an OOS-visible reading. Survivorship: U56 / B136 are CURRENT
   constituents, so every LEVEL above is optimistic; SMALL665 clears 4b 0 of 24 choosers.
9. **Proposed RULES wording** (rule 6 — Sunday review only; RULES.md, PROTOCOL.md, scan.py,
   bot.py and baseline.py are NOT modified by idea 1803):

   > **2. Sizing.** Hold every instrument in the universe that has a price that day at `g/N` of
   > NAV, `N` being the count of priced instruments. Once a month, set
   > `g = min(1, 0.10 / sigma_20)`, where `sigma_20 = sqrt(252) *` the standard deviation of the
   > last 20 daily returns of the equal-weight, unlevered universe portfolio computed through the
   > previous close, and reset the book's total exposure to it; between those dates `g` is not
   > re-read. The equal-weight re-spread of the names runs on the same monthly date (a weekly
   > re-spread is permitted and costs 0.015-0.022 of Sharpe). Weight not deployed sits in CASH, is never
   > re-spread across the held names, and `g` never exceeds 1. No ranking, no momentum screen, no
   > per-name volatility filter.

10. **Status: KEEP-candidate, path 4b, awaiting Sunday review — with point 8 attached.** It is
    NOT proposed as a live rules change by this run and it does NOT supersede idea 1793's
    candidate; the two are alternatives on the same dial. Evidence:
    `research/backtests/2026-09-20_cost-priced-is-chooser_B.py` / `.result.md` (gates 13/13,
    G4b reproduces all 480 cells of idea 1793's committed grid at max |Δ| 8.882e-16).

---

## ADDENDUM (2026-09-20, lane C, idea 2038) — THE 4b MARGIN IS **NOT** A STACK OF DRAWDOWN
## EPISODES, AND THIS CELL IS THE LEAST EPISODE-CONCENTRATED OF THE FOUR. **STATUS UNCHANGED.**

Idea 2038 excised every OOS SPY peak-to-trough episode from the statistic — one at a time and
cumulatively, deepest-first — at four depth bars x four paddings on U56 and B136, for this cell
and three sibling vol-target cells (1,664 scored rows; gates **11/11**;
`research/backtests/2026-09-20_voltgt-4b-margin-episode-stack_C.py` / `.result.md`). It
reproduces sections 2-4 of this memo at max |Δ| **4.54e-05** and the IS half is invariant to
every excision at exactly **0.000e+00** (G5).

* **The queue's premise is refuted.** No single episode owns >= 0.50 of any cell's OOS Sharpe
  margin; the max over 8 (panel x cell) pairs is **+38.0%** and THIS cell reads **+10.8%** (U56)
  / **+13.3%** (B136). Its whole 5-episode stack at b=10% — 326 days, 13.4% of the OOS tape —
  owns **+19.1% / +24.0%** of its +0.4085 / +0.3263 Sharpe margin, a **concentration of 1.43x /
  1.80x** against `C_MEMO` 1.17x/1.03x, `C_GXDD` 2.13x/3.69x and the OOS oracle `C_ORCL`
  3.33x/3.60x. **This cell is not a crash hedge priced as a growth rule.**
* **But 2020Q1 alone is 23 days (0.94% of the tape) at 11.5x-14.1x concentration**, and the other
  four episodes (2022, 2018Q4, 2025Q1, 2018-02) run NEGATIVE — excising them RAISES the margin,
  i.e. this book gives ground to SPY in the shallower declines. The margin is one window plus a
  drag, not an even spread and not a stack.
* **Do not read the excised verdict as a book failure.** 4b OOS flips PASS -> FAIL in 127 of 128
  cells, but that is a BAR SHIFT (idea 2034's axis): the BOOK's OOS Sharpe rises **+1.196**
  (1.2822 -> 2.4778) while SPY's rises **+1.274** (0.8737 -> 2.1472), and the 4b DD cap tightens
  **-20.23% -> -5.98%** with the CAGR floor rising **10.68% -> 25.38%**, ~14 pp each.
* **The CAGR floor is the leg that dies first**, consistent with the record: the stack owns
  **+80.9%** of this cell's U56 OOS CAGR margin (B136 +110.0%, it crosses zero) against +19.1% /
  +24.0% of the Sharpe margin. Point 6's "thin on one leg" warning is an EPISODE fact on the CAGR
  side.
* **Required companion statistic for any future excision claim:** publish the CONCENTRATION RATIO
  (margin share / day share) and the BOOK-vs-BENCHMARK split of the move. The raw "share of the
  margin" is a small difference of two large co-moving legs.
* **Unchanged:** point 8's thin-chooser caveat (2038's rule 8: 16 of 128 legal picks clear 4b OOS
  un-excised, 0 of 128 clear 4a, and only `C_ISLEGS` on B136 T=M reaches this cell); survivorship
  as in point 8; SMALL not re-run (0 of N, confirmed four times). **Status: KEEP-candidate, path
  4b, awaiting Sunday review.** RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are
  untouched by idea 2038.
