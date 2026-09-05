# Memo — proposed PROTOCOL clause on fitted dials (idea 189, cloud, 2026-09-05)

Not a RULES change and not a KEEP candidate: nothing is proposed as a book, and `RULES.md`,
`scan.py`, `bot.py` and `baseline.py` are untouched. This is the clause idea 189 was queued to
produce, for a Sunday review to adopt or reject.

**Proposed clause.** A dial may be FITTED PER BOOK only where the fit has been shown to beat a
constant fixed at the fitting rule's OWN MODAL PICK, measured across books and out of sample.
Otherwise publish the mode once and hold it fixed. Every dial claim must publish (i) the modal
pick, (ii) its share of books, and (iii) whether the mode sits at a LADDER ENDPOINT.

**Why the third item.** On idea 171's own five dials, three — GROSS, BAND, SLEEVE — put the IS
argmax on the ladder's last point in **69–100%** of books. There the selector already IS a
constant, the modal arm agrees with it in 69–100% of pairs, and the paired difference is bounded
by **0.0001** of OOS Sharpe. A "fitted dial" whose mode is an endpoint is a truncated ladder,
not a choice, and a claim either way about fitting on it is uninformative.

**Why the clause bites where the dial is real.** On the two dials with a genuinely spread pick
distribution — N (modal share 23%) and CADENCE (83–89%) — the modal constant beats the fit in
**4 of 4 corpus × dial cells**: N +0.0215 (53 books) and +0.0256 (115 books), CADENCE +0.0261 and
+0.0255 of OOS Sharpe. Pooled over the five dials it banks **69.8% / 63.1%** of the ORACLE's gap
over the inherited constant where the fit banks **57.8% / 49.6%**. Fitting's best case anywhere
in the 3 × 2 × 2 × 5 grid is **+0.0001** OOS Sharpe.

**The mechanism, and the limit that must travel with the clause.** The constant wins through
tail picks: when the CADENCE selector leaves M it loses **0.15–0.23** of OOS Sharpe (worst books
−0.28 and −0.43). But a mode is only writable if it is concentrated — split-half validation
reproduces the mode in **9 of 10** corpus × dial cells, and the one failure (N on 53 books, modal
share 22.6%) is also the one cell where the held-out mode LOSES, at **−0.0229**. So the clause
needs a modal-share floor, which idea 219 is queued to measure; until it exists, read "the mode"
as unwritable below roughly a 50% share.
