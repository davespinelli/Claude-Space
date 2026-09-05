# Memo — idea 145: publish 4b's bars as bands (proposal for Sunday review)

1. **No coefficient changes.** All five published values sit inside their own bands; 4b passes
   stay at 29 of 306 at every band edge. This is a reporting proposal only.
2. Proposed PROTOCOL rule 4b addition, verbatim: *"Each 4b bar is published as an indifference
   band — the interval of its coefficient over which the admitted set and the ladder leakage are
   unchanged — beside the adopted point, together with the number of arms the bar excludes alone.
   Measured on the 306-row / 342-ladder corpus of ideas 129/131: H1 1.00 in [0.997, 1.045]
   (1 sole victim); H2 1.00 in [0.983, 1.021] (2); OOS 1.00 in (−inf, 1.052] (0); MaxDD cap 0.60
   in [0.5979, 0.6012] (47); CAGR floor 0.70 in [0.6965, 0.7020] (27)."*
3. **Width alone is not robustness.** A bar that binds on nothing has an infinite band (Q3: every
   band blows up once the joint screen empties). The sole-victim count must be quoted with it,
   which is why clause 2 carries both numbers.
4. **State that the OOS bar is currently free.** It excludes 0 of 306 rows and 0 of 342 ladder
   points that the other four do not already exclude. Report it; do not delete it on one corpus.
5. **Correct the record on which bar excludes most.** The drawdown cap is the sole cause of KILL
   for 47 rows (61.8% of arms clearing its other four bars), against the CAGR floor's 27 (48.2%).
   Ideas 129/131/135 are framed on the floor; the cap is the larger instrument.
6. **Rule 8 clause:** *"A coefficient may be moved within its published band without re-running
   the walk-forward: on the 18-cell corpus every in-band value moves 0 picks and leaves OOS
   Sharpe unchanged at 1.022. A move outside any band requires a fresh rule-8 run."*
7. **Idea 145's own premise is killed.** Idea 131's `gamma in [0.57, 0.61]` band came from
   swapping the statistic, not from re-calibrating a coefficient: phi has **no** strictly
   dominating value in its own units. Bands are usually indifference intervals, not dominance
   intervals, and PROTOCOL should say "band" meaning the former.
8. **The dominance test is only valid where its criteria are co-monotone** — the CAGR floor and
   the DD cap. On the Sharpe bars the ladder control excludes nothing, so H2 comes out
   "dominated in both directions", i.e. undetermined. Do not adopt the test for Sharpe bars.
9. The two strict-dominance findings (OOS ≥ 1.0522, delta ≤ 0.5978) are each worth exactly one
   ladder point and zero admissions. Not recommended as changes; recorded so nobody re-derives them.
10. **Nothing here is a KEEP for capital.** No book is proposed, RULES is untouched, and the
    standing 4b candidate is unaffected (4a 97/306, 4b 29/306, both 6/306 at every band edge).
