# Memo to the Sunday review — idea 97, what PROTOCOL may quote about drawdown instruments

Proposal: **amend PROTOCOL, not RULES.** No trading rule changes; no file was modified by this
run. Evidence: `2026-09-05_price-list-tier-bar_B.result.md` (18 cells × 3 panels × 3 windows).

1. Idea 94's four-tier sentence is **not quotable**: its first clause (gate < gross lever) is
   true in 6/6 u56 and 6/6 broad full-sample cells but **2/6 on the 439-name small-cap panel**
   and **0/6 in u56's own in-sample window**; the second clause is 13/18 full and 9/18 OOS.
2. Its last clause survives everything: the per-name trailing stop is the dearest tier in
   **50 of 54** panel × window × cell rows.
3. But its *phrasing* is wrong: "a stop is not insurance" holds only on large caps. On the
   small panel the stop buys positive drawdown in 9/12 cells (median +1.07 pp) — dearest, not
   inert.
4. Exact wording proposed for **PROTOCOL rule 4**, appended as a new sentence:

   > *When a rule is justified as drawdown insurance, price it as pp of CAGR surrendered per pp
   > of MaxDD bought against the SAME base book on the SAME days, and quote the static-gross
   > lever's price in that cell beside it. Only one ordering may be stated as general: a
   > per-name trailing stop is the dearest drawdown instrument the project has priced
   > (dearest tier in 50 of 54 rows across three panels). Every other ordering — including
   > "per-name gates are cheaper than holding less" — is panel-specific and window-specific and
   > must be requoted on the panel in question. Any price quoted must state the MaxDD of the
   > window it was measured in.*

5. The last clause of that wording is load-bearing: the gate tier prices at **4.108** in u56's
   2009–2016 window (SPY MaxDD −22.1%) and **0.404** in 2017–2026 (SPY MaxDD −33.7%). A
   drawdown price without its window's depth is not a number, it is a regime reading.
6. Do **not** adopt a tier-based selector. Choosing the cheapest in-sample tier and a
   non-extremal member of it is worse out of sample than idea 94's plain instrument selector
   (mean OOS regret +0.489 vs +0.337; rank-1 4/18 vs 8/18) at equal OOS Sharpe (+0.007).
7. Report-only statistic worth adding next to any drawdown budget: **in 12 of 18 cells no rule
   tier was cheaper in-sample than simply de-grossing.** The honest default is the lever.
8. Rules unchanged. No KEEP: no arm passes 4b on all three panels, and none passes it on the
   small panel at all. `EWall+vol60-dg` and `EWall+band3-rw` are reproduced as cross-universe
   4b passes on the two large panels (idea 94's pair), joined at 10 bps by `EWall+g200-rw` and
   `EWall+v1gate-rw`.
9. Survivorship caveat that ships with the wording: all three panels are current constituents;
   the small panel's bias flatters gates (it excludes the beaten-down names a gate would have
   sold), so the C1 inversion reported there is a lower bound.
10. Follow-ups queued as ideas 117 (price at matched crisis depth), 118 (why the book-level DD
    control is cheap on small caps), 119 (audit `V1u/small`'s negative gate price).
