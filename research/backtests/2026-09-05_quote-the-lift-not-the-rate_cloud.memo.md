# Proposed PROTOCOL reporting clause — for the Sunday review (idea 149, cloud, 2026-09-05)

Not a RULES change and not a KEEP: a reporting clause only. Evidence in
`2026-09-05_quote-the-lift-not-the-rate_cloud.result.md`.

**Proposed addition to PROTOCOL rule 4 (exact wording):**

> **Joint pass counts must state their cell set.** Any statistic of the form "N of M books pass
> in every cell" must be quoted with (a) the list of cells used, (b) each cell's own pass count,
> and (c) the same statistic re-read over ALL cells, including those that admit nothing. A joint
> pass count is multiplicative, so one empty cell zeroes it: dropping empty cells from the
> denominator is not a rounding convention, it changes the answer. Quote the raw rate, not a
> lift — a size-matched-null adjustment is only informative where a material share of the
> statistic's draws admit nothing.

**Why (three numbers).** Idea 90's operational KEEP reads **4 of 51** (book, arm) pairs over four
large-cap cells and **0 of 51** once the two small-panel cells are restored; idea 129's POINT
census read the same way goes **2 of 51 -> 0 of 51**. Under randomised bars the same convention
inflates the count **20.2x** at the tightest screen.

**Why not idea 149's own prescription.** The lift over the size-matched null is monotone in
tightness for one of the two statistic families and **non-monotone for the other**, i.e. exactly
the defect it was proposed to cure. Idea 141's fix works because its cells hold 17 arms and
P(non-empty) falls to 0.424; these statistics are defined over 51 pairs, where P(non-empty)
never falls below 0.997. Both statistics nonetheless clear their own nulls by 13.3x and 263x
(p < 0.0001), so nothing already published needs withdrawing — only re-quoting with its cell set.
