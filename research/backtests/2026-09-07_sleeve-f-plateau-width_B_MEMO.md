# MEMO — the f = 0.25 constant survives, but idea 139's memo point 6 is wrong (idea 138, lane B, 2026-09-07)

1. **Status.** No new book and no new KEEP: the book is idea 139's standing 4b KEEP-candidate,
   independently reproduced here to every published digit (u56 **11.22% / 1.2331 / −16.67%**,
   halves 1.327/1.160, OOS **1.221**; broad **11.93% / 1.2370 / −18.50%**, OOS **1.196**, 10 bps).
   This memo replaces the JUSTIFICATION of its only tuned constant, not the constant.
2. **What idea 139 point 6 says.** "It is not knife-edged in f … the window is an interior
   plateau, not a grid edge." The window claim is right; the word **plateau** is wrong.
3. **The dial is a ramp, not a plateau.** Over the published sweep Sharpe rises monotonically in f
   in **16 of 16** cells; the no-sleeve control is the WORST point in 13 of 16 and above the sweep
   in **0**; `plateau_frac` **0.17** against idea 128's 0.71 median. Nothing here is flat.
4. **f = 0.25 is not the Sharpe argmax.** With the dial bounded at f = 1.00 (pure sleeve) the
   Sharpe argmax is **f = 0.60** (9/16 cells) and the shallowest drawdown is at **f = 0.75**
   (16/16). f ≥ 0.50 fails 4b in **16/16** on the CAGR floor.
5. **What f = 0.25 IS the argmax of.** The worst-of-five 4b margin — the bar the constant is
   adopted for (idea 128's finding 3). Its interior argmax is 0.15–0.30 in **14/16** cells, and the
   cell-mean worst margin is positive **only** at f = 0.25 (+0.0001).
6. **Rule 8 backs the value, not the axis.** f dialled on 2009–2016 alone: the 4b-screened selector
   picks **0.25 in 13 of 15** cells (0.20 in 2, abstains in 1) and clears all three OOS 4b bars in
   **14 of 15**; the plain IS-Sharpe selector picks **0.50 in 15 of 16** and clears them in **2**.
7. **The margin is thin even where the window is wide.** At f = 0.25 the binding bar clears by
   > 0.005 in 12/16 cells and > 0.01 in **4/16**; u56/EWall @25 bps clears by **+0.0018** (0.18
   pp/yr). One grid step of f moves that margin by 0.004–0.011 — more than the margin itself.
8. **Exact RULES wording — UNCHANGED from idea 139's memo point 7** (reproduced so the Sunday
   review reads one text, not two):
   > **Universe.** Every instrument priced that day in `research/universe.json`.
   > **Sleeve.** S = {TLT, GLD, UUP}. For each s in S on day t: `vote(s)` = the fraction of
   > {12-1m, 6m, 3m} total returns that are > 0; `rp(s)` = (1/60d stdev of daily returns)
   > normalised to sum to 1 over S. Sleeve weight `sl(s) = vote(s) * rp(s)`.
   > **Equity leg.** `eq(i) = 0.75 / N` for each of the N priced names.
   > **Book.** `raw = 0.75 * eq + 0.25 * sl`, then scale every weight by `0.75 / sum(raw)`.
   > **Cadence.** Rebalance weekly to those weights; orders decided at Friday's close execute at
   > the next session's close. No shorting, no leverage, no daily override.
9. **The sentence that must go beside it.** "f = 0.25 is the argmax of the 4b margin, not of
   Sharpe; the Sharpe-optimal f is 0.60 and it fails the CAGR floor. The 4b window (f = 0.10–0.40)
   is the interval where two monotone curves cross, and the binding margin inside it is under
   0.01 in 12 of 16 cells."
10. **Still blocked on** ideas 105/106 (how any sleeve is written into RULES) and 395 (does the
    sleeve earn anything over its own de-grossed control). Not proposed for RULES this week.
    Survivorship (idea 54) biases every number here toward the control, so the dominance of the
    sleeve over its control is understated, and the CAGR floor margins are flattered.
