# Idea 82 — the cost breakeven as a numeric KEEP bar

**Verdict: ANSWERED. Idea 11 reproduces to the decimal, the bar is proposable at 25 bps, and the
standing KEEP fails PROTOCOL's own 10 bps assumption cross-universe.** No new book, no RULES change.

1. **Idea 11 reproduces exactly.** Idea 2's candidate, in the `rw` (full-gross rebuild) convention,
   has a cross-universe breakeven of **7.5 bps** — idea 11's published number — and
   `EWall + v1gate-rw` breaks even on `broad` at **10.5 bps**, idea 11's "EWall 10.5". The harness
   identity holds (`H.run` vs `engine.backtest` max|diff| **0.000e+00**) and idea 94's published
   `EWall+vol60-dg` u56@10bps row is exact (11.587% / 1.133 / -16.884%).
2. **The de-gross convention decides the answer, not the gate.** `EWall + band3` holds
   cross-universe 4b to the top of the 30 bps grid under **rw** (the published form, per idea 91)
   and **never passes at any cost, on either universe**, under **dg**. Same book, same band, same
   gross: opposite verdict. Any bar RULES states must name the convention.
3. **The four standing candidates, ranked by cross-universe breakeven** (bps, 0.5 bp grid, both
   universes, published bars): idea 57 `EWall+band3-rw` **>= 30** (grid-limited) = incumbent
   `EWall+vol60-dg` **>= 30** > idea 46 fraction f=0.85 **14.0** > idea 2 `CAND-n20` **7.5 (rw)** /
   **4.0 (dg)** > idea 72 `EWall` **never passes** under either reading tried.
4. **The passing cost set is a genuine interval**: contiguous in **27 of 27** measurable
   (book, arm, panel) triples, zero interior holes. A single breakeven number is well defined.
5. **What sets it**: over the 64 triples the first-failing bar is the CAGR floor **31**, the DD cap
   **22**, H2 **12**, H1 **10**, OOS Sharpe **9**. The DD-cap entries are mostly books that already
   fail at 0 bps, so they are not cost-driven — stated rather than counted as breakeven causes.
6. **Rule 8 (choose on 2009-2016, evaluate 2017-2026 untouched)**: over the 6 books measurable in
   both windows the IS->OOS breakeven spread is mean **+3.2 bps**, median +4.5, range **-8.0 to
   +12.0**, Spearman(IS, OOS) **+0.580**. The IS breakeven *understates* the OOS one in 5 of 6 —
   the opposite of idea 128's prediction. Per-panel the spread is far wider (u56/TOP20 arms
   +12.5 to +29.5), which is the register idea 11's "+26 / -13.5" belongs to; at the
   cross-universe level it is narrower.
7. **Proposed bar.** At the published bars, books holding cross-universe 4b to at least C* are
   **10** (0 bps), 9 (5), 7 (7.5), **6 (10)**, 4 (15), **3 (20, 25, 30)**. RULES should state:
   > A KEEP must hold cross-universe 4b (both large-cap universes) to at least **25 bps**, not the
   > 10 bps PROTOCOL assumes — 10 bps plus the +12 bps upper walk-forward spread, rounded to the
   > published 25 bps rung. Quote the breakeven itself, and the convention (`dg` / `rw`), with it.
   Choosing 25 over 15 is a judgement about how much walk-forward spread to carry; the whole
   0.5 bp curve and the full 420-point (phi x delta x C*) grid are published so the Sunday review
   can pick a different rung from the same evidence.
8. **Consequence for the book on the table**: idea 2's standing 4b KEEP **fails a 10 bps bar**
   (7.5 rw / 4.0 dg) and fails 4b on `broad` at 10 bps outright (OOS 12.5% / 0.892 / -20.1% vs
   SPY 15.45% / 0.882 / -33.7%). Idea 57's `band3-rw` and the incumbent `vol60-dg` clear 4b on
   **both** universes at **both** published cost rungs; idea 46's fraction book clears at 10 bps
   and fails at 25.

**Caveats.** Survivorship: u56 and broad are current-constituent lists (idea 54). The small panel
is excluded by design — no book has passed 4b there. ">= 30 bps" means the grid ran out, not that
the book is costless. Idea 38: u56/broad are on a calendar-day index. Costs are charged per unit of
turnover with no spread or impact model, so a bar stated in bps is a modelling convention, not a
market quote. The mapping from leaderboard prose to construction is stated in the script header;
idea 72's book could not be pinned and is reported under two readings, neither claimed to be it.
