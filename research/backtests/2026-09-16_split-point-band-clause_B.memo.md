# PROPOSED PROTOCOL rule 8 clause — the SPLIT-POINT BAND (idea 1013, lane B, 2026-09-16)

**Status: PROPOSED, NOT APPLIED.** Rule 6 — PROTOCOL changes go through the Sunday review.
`RULES.md`, `PROTOCOL.md`, `scan.py`, `bot.py`, `baseline.py` untouched by this run.

**Why.** Rule 8 fixes the IS/OOS split at 2016-12-31 by fiat. Idea 1013 measured the price of
that fiat over the 16 legal quarter-end splits 2015-03-31..2018-12-31, start pinned: the
*verdict* is nearly safe (**0 of 9 committed 4b passes change**; 41 of 45 books constant at
10 bps, but **38 of 45 at 25 bps**), while the *pick* and the *published number* are not
(**3 of 6 chooser cells change pick**; OOS Sharpe moves **0.1747–0.2666** even where the pick
does not, against the **0.2102** median leg margin the record certifies passes on). The split
point moves exactly one leg of five — `L5_CAGR` — because `L1_H1`/`L2_H2` are count halves of
the full path, `L3_OOS` moves on both sides at once, and SPY's `|OOS MaxDD|` range across all
16 ends is **0.0000**.

**Exact wording proposed for PROTOCOL rule 8:**

> A rule-8 result is published with its **SPLIT-POINT BAND**: the same IS-only chooser is
> re-run at the quarter-ends one year either side of the declared split, and the MIN and MAX of
> the pick's OOS Sharpe, OOS CAGR and OOS MaxDD across that band are reported beside the
> declared-split numbers. A pick whose OOS Sharpe band is **wider than the narrower of its two
> 4b Sharpe margins** is reported as PARK, not KEEP, whatever it reads at 2016-12-31. Where the
> chooser's PICK ITSELF changes inside the band, the result names every book chosen and the
> ends that choose it, and may not be quoted as "the rule-8 pick" without them.

**Reading rule for already-committed rule-8 results:** read as scoped to the 2016-12-31 split
and carrying an unreported band; a committed 4b pass whose only E-sensitive leg is `L5_CAGR`
and whose OOS CAGR sits within 5% of the floor is re-read as PARK until its band is published.

**What it would re-label on this run:** 3 of 6 GRID picks (both B136 Sharpe-family cells and
U56/IS_CAGR) and 4 of 45 books; it changes **no** 4a verdict, because path 4a never reads the
split point at all. It re-labels **none** of the record's 9 committed memo-backed passes, all
of which hold at 16 of 16 ends.
