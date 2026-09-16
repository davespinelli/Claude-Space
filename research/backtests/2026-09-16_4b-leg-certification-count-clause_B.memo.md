# Memo — the 4b leg-certification clause needs a COUNT, not a DISJUNCTION (idea 969, lane B)

Source: `2026-09-16_re-score-EVERY-committed-4b-PASS-against-its-OWN-CELL-s-PER-LEG-NULL-under-BOTH-KINDS_B.py`.
36,000 gross-matched coin flips (200 draws × 3 kinds × 30 (panel, book, cadence) families, rescaled
across 3 gross rungs), 90 ladder cells, 10 bps, next-day execution. Gates 8 of 8. PROPOSED, NOT
APPLIED (rule 6): `RULES.md`, `PROTOCOL.md`, `scan.py`, `bot.py` and `baseline.py` are untouched.

1. **Not a KEEP for capital.** No book is proposed. Rule-8 OOS 4a is **0 of 18** picks and OOS 4b
   **5 of 18**, every passer already in the record (the live band book, and TOP10/TOP20 at 0.50).
2. **The clause as written strips nothing.** Idea 942's clause (ii) calls a 4b PASS UNADJUDICATED
   when *every* leg is non-certifying. On the record's own claimed cells that fires on **1 of 18**
   STRICT resolvable passes (survival **0.944**), **2 of 88** WIDE (0.977) and **2 of 10** structural
   passes (0.800). On the **72 non-degenerate ladder cells it fires 0 times**.
3. **The 2 cells it does strip are its own null's defect, not bad books.** Both are `EWELIG` —
   U56@0.75/M and B136@0.75/W — the cells idea 998 found DEGENERATE: a holding-count-matched draw
   from the eligible pool when the book already holds that whole pool *is* the book, 1 distinct
   draw of 200. The disjunction is a null-construction detector, not a book filter.
4. **Why it is vacuous: one leg carries it.** Of the 32 ladder cells with exactly one certifying
   leg, the sole certifier is `L_CAGR` in **20** and `L_DD` in **12**, and **never** `L_H1`,
   `L_H2` or `L_OOS`. A coin flip essentially never clears 70% of SPY's CAGR (median RANDROT base
   rate **0.000**), so `L_CAGR` alone keeps almost every pass adjudicable.
5. **942's per-leg reading reproduces on the record's OWN claimed cells.** Share of STRICT cells
   where the leg is non-certifying under BOTH kinds: `L_OOS` **0.722**, `L_H1` 0.667, `L_H2` 0.667,
   `L_DD` 0.556, `L_CAGR` 0.278. Four legs of five are cleared by a coin flip more than 90% of the
   time in the majority of the cells the record quotes.
6. **The kind does not move the verdict; it moves the leg.** Survival is **identical** under
   RANDROT and RANDFIX (0.944 / 0.977 / 0.800), but leg-by-leg the two kinds disagree on
   **12.2%** of (cell, leg) pairs and RANDFIX is uniformly the harsher null (median `L_OOS` base
   rate 0.995 vs RANDROT's 0.950). Quoting one kind understates leg deadness.
7. **PROPOSED CLAUSE, exact wording, replacing 942's clause (ii) final sentence:**
   > *"Any published 4b PASS carries the per-leg base rate of its own cell's gross-matched null
   > under BOTH null kinds (rotating and fixed), together with the number of DISTINCT draws the
   > null produced. A leg whose base rate exceeds 0.90 under EITHER kind is reported as NOT
   > CERTIFYING. A pass is reported as its CERTIFYING-LEG COUNT out of five, and a pass with
   > FEWER THAN TWO certifying legs is reported as UNADJUDICATED, not as a KEEP. A null with
   > fewer than 50% distinct draws is reported as DEGENERATE and certifies nothing."*
8. **Scored on this grid**, the count bar has the teeth the disjunction lacks: of the 10 structural
   4b passes it leaves **4** at ≥2 legs and **1** at ≥3, against 8 at ≥1. Over the 72 non-degenerate
   cells: ≥1 **72**, ≥2 **56**, ≥3 **45**, ≥4 **33**. Mean certifying legs are 2.11 (STRICT), 2.61
   (WIDE), **1.40** (structural) — the price-harvested passes are the weakest of the three.
9. **Do not use it to choose.** `C_ISCERT` — pick the cell with the most certifying IS legs — is
   the worst of three IS-only rule-8 choosers: OOS 4b **0 of 6** against `C_ISSHARPE`'s 2 and
   `C_IS4B`'s 3, mean OOS Sharpe 0.857 vs 0.943 / 0.984. `H_RULE8` FAIL. Reporting, not selection.
10. **SURVIVORSHIP (rule 9).** U56 and B136 are current-constituent lists, so a coin flip drawn
    here is a better book than one drawn in real time and **every base rate above is an UPPER
    bound**. That cuts *against* this memo: legs measured live could certify more often than
    printed, which would make the ≥1 disjunction even more vacuous, not less.
