# Memo — idea 198, for Sunday review. NOT a rules change; evidence only.

1. **Nothing here is a KEEP candidate.** No new book is proposed; every book belongs to ideas
   159/165/168 and is already priced. What is on trial is a SELECTION RULE and the null it
   should be judged against.
2. **Idea 178's IS-window 4b screen should be struck from the record as a selector.** Its
   published +0.0287 paired OOS Sharpe sits at the **54.5th percentile** (z +0.11) of a null
   that admits a uniformly random subset of the screen's own admitted size in each cell — dead
   centre. Under the alternative coefficient convention (PUB) it sits at the 34.0th.
3. The null's own mean is **+0.0272**. Restricting the IS-argmax pool at random buys 95% of the
   screen's entire published edge; the screen contributes **+0.0015**.
4. **The screen fails on its own claimed mechanism too.** Idea 178 diagnosed it as
   de-concentration. Its mean picked book size is 9.73 against the null's 10.49 — the **35th
   percentile**. It de-concentrates less than chance. Idea 199's floor `n >= 25` reaches 27.82,
   the 100th.
5. **Idea 199's floor survives this null**: +0.1297 at the **100.0th percentile**, z +4.57, and
   every floor k in {10,15,20,25} sits at or above the 95th. So the two results together say
   restriction per se is not the mechanism and **de-concentration is**. Nothing in idea 199's
   own caveats (k is a grid edge; ρ(n, OOS Sharpe) reverses on the sub-$2B panel; OOS CAGR
   13.53% → 10.96%) is relaxed by this run.
6. **Proposed PROTOCOL clause, exact wording** (for the Sunday review to accept or reject; this
   run does not modify PROTOCOL.md, RULES.md, scan.py, bot.py or baseline.py):
   > **10. Size-matched null for pool restrictions.** Any selector that narrows a candidate
   > pool before an in-sample argmax must be reported against a null that admits a uniformly
   > random subset of the SAME SIZE in each cell (≥200 draws, seeded, with the same fallback
   > behaviour when the selector admits none). Publish the selector's percentile in that null
   > beside its paired edge. Comparing such a selector against do-nothing alone is not
   > sufficient evidence.
7. **Why the clause is needed, in one number:** on this corpus a random 3-book subset in every
   cell returns **+0.0756** mean paired OOS Sharpe — 263% of the screen's published edge, with
   no parameters at all. Restricting an overfit argmax is nearly free money against
   do-nothing, so "beats do-nothing" is close to uninformative for this class of instrument.
8. **The mechanism, stated once:** ρ(n, OOS Sharpe) is +0.489 (t +3.67) within cells while
   ρ(n, IS Sharpe) is only +0.195, and the IS-Sharpe argmax's mean picked size falls
   monotonically from 27.4 (a random single book) to 8.55 (the full-pool argmax) as the pool
   widens. The IS argmax is a concentration machine; every instrument that helps here helps by
   blocking it from its own small-book tail.
9. **Power caveat, not buried:** the screen fires in only 4 of 11 cells, so its null has four
   live cells. The honest reading is that the screen **cannot be distinguished** from a
   same-size random restriction, not that it has been proven equal to one.
10. **Survivorship (idea 54)** applies to all three panels — current constituents, no
    delistings on the small panel, levels biased upward. Every arm reads the same panel, so the
    comparison stands; no level in this run is a tradable estimate.
