# Memo — idea 189: the PROTOCOL clause this run does and does not support (NOT a proposal)

This is **not** a KEEP memo: no new book, no rules change, nothing for capital. Idea 189 asked for
a PROTOCOL clause and PROTOCOL rule 6 reserves changes for Sunday review, so this is evidence.

1. **What the run supports.** Across idea 171's five dials, a constant fixed at the selector's own
   modal pick matched or beat the selector on 4 of 5 and lost on the fifth by 0.0001 OOS Sharpe.
   The mode is free, has no tuned parameter, and was corpus-stable (LOO mode = in-corpus mode in
   0/53 books, all ten dial×selector cells).
2. **What it does not support.** The mode beats the selector *significantly* on 1 of 5 dials only
   (CADENCE, +0.0261, t +2.89, 9W/0L, sign p 0.0039), and that result lives in one book family.
   Idea 175's "off-modal picks are catastrophic" is cadence-specific: on N the deviations are 20
   good / 21 bad.
3. **The discriminator, which is the clause worth writing.** The mode is informative only where
   the ladder has an INTERIOR optimum. Three of the five modes (GROSS 1.00, BAND 0.08, SLEEVE
   0.30) are grid edges and one (N=20) is the incumbent already.

**Exact PROTOCOL wording proposed for Sunday review (rule 10, new; nothing in RULES.md changes):**

> **10. Fitted dials.** Before fitting a dial in-sample, report the ladder's shape and the
> selector's modal pick. If the modal pick is a grid endpoint, the dial is not being chosen and
> the ladder must be widened or the arm dropped (idea 183). If the modal pick equals the incumbent,
> write nothing. Only where the modal pick is an INTERIOR point may a dial be fixed at it, and it
> is then written into RULES as a constant — never as a per-book selector, which cost 0.0261 of
> OOS Sharpe on the one dial where this distinction was measurable (idea 189).

