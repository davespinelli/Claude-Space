# Idea 1147 — are the H and CADENCE argmaxes waiting on data that cannot help? ANSWERED: YES for H. The correct reading is ZERO, and pricing it costs nothing because the argmax buys nothing.

1. **The zero reading, tested head-on.** A circular block-bootstrap null of "every rung is the
   same book" (63d blocks, 400 reps, seed 1147) is DECISIVE at **0 of 18** (panel, ladder, stat)
   cells. p runs 0.1675..0.9700, median 0.5788, and the OBSERVED rung gap sits BELOW the null's
   MEDIAN gap in 16 of 18 cells — U56/H/Sharpe observed 0.0325 against a null median of 0.0887
   (p 0.9700); SMALL663/H/CAGR 0.0154 against 0.0467 (p 0.9700). The ladders do not merely fail
   to separate: the null over-produces the gap they show.
2. **1140's bycatch replicates, and a longer tape makes it worse.** b(RATIO) <= 0 at 11 of 18
   cells, median -0.0956 (1140 read -0.1251 on the mover ladders). Median b(GAP) -0.2259 against
   median b(SD) -0.3203. Strongest on SMALL663's H ladder: b(RATIO) -0.6547 (Sharpe) / -0.7267
   (CAGR), where b(GAP) -0.9981 / -1.0824 outruns b(SD) -0.3434 / -0.3558.
3. **Nothing reaches the decisiveness bar even at the full tape.** RATIO = GAP/SD <= 2 at 18 of 18
   cells, median 0.8829. The best cell in the whole run is B136/CADENCE/CAGR at 1.9357.
4. **But the two ladders are NOT the same object — a blanket "zero" over-reads.** On the H ladder
   b(GAP) is negative at 6 of 9 cells. On the CADENCE ladder it is POSITIVE on U56 and B136
   (CAGR +0.5389 / +0.2026, Sharpe +0.1995 / +0.1018), so cadence's resolution GROWS with tape.
   H is un-resolvable; CADENCE is improving and merely not there yet (and still p 0.53 under G2).
   A committed claim that reads "under-powered" is wrong about H and defensible about CADENCE.
5. **CAPITAL ARM (rule 8, OOS read once) — "price what changes if the correct reading is zero."**
   ARGMAX chooser (best H rung and best cadence rung chosen on 2009-2016) minus ZERO chooser
   (the standing default H=1, weekly), both read once on 2017-2026:
   d(OOS Sharpe) mean **+0.0144, SE 0.0189, t +0.76, n=9** — indistinguishable from zero;
   d(OOS CAGR) +0.0154; d(OOS MaxDD) **-0.0425, negative in 8 of 9 cells**. The argmax pick
   differs from the default in 8 of 9 cells, so it is a genuinely different book — not a better one.
6. **Levels.** U56 ARGMAX(H=63, M) 22.98% / 1.1093 / -33.18% vs ZERO 21.42% / 1.1391 / -27.24%.
   B136 ARGMAX(H=63, M) 23.47% / 1.0166 / -35.27% vs ZERO 19.26% / 0.9256 / -31.03%.
   SMALL663 ARGMAX(H=21, W) 17.79% / 0.6911 / -44.08% vs ZERO 19.38% / 0.7358 / -39.01%.
   SPY OOS 15.28-15.33% / 0.8745-0.8767 / -33.72%. RULES v2 OOS Sharpe 1.2778 / 1.1059 / 0.5600.
7. **VERDICT: ANSWERED / KILL (capital).** KEEP paths over all 18 OOS grid points: 4b 0, 4a 0.
   The binding leg is the DD cap, failing at 18 of 18 (L_H2 6, L_H1 0, L_CAGR 0) — the same leg
   that binds the incumbent MOM20 book. The H overlay's only reliable effect is a deeper drawdown.
8. **RECOMMENDED TO THE SUNDAY REVIEW, PUBLISHING ONLY (changes no book):** a committed H argmax,
   tie-set or floor claim must be published as **ZERO**, not as "under-powered at this sample
   length". The measured basis is (2) and (3): the effect shrinks faster than the noise, no
   attainable tape closes the ratio, and the argmax it names is worth +0.0144 of OOS Sharpe at
   t +0.76 while costing 4.3pp of drawdown. A CADENCE argmax may still be published as
   under-powered — its gap is growing — but must quote its ratio (best in the record: 1.94).
9. **What this does NOT say.** It does not say H and cadence are interchangeable in cost: the
   daily rung is plainly worse everywhere (U56 full-tape Sharpe 1.0122 vs weekly 1.1266, SMALL663
   0.5024 vs 0.7464). The zero reading is about the argmax WITHIN the resolvable part of the
   ladder, not about the ladder's endpoints.
10. **SURVIVORSHIP (rule 9).** U56 and B136 are current-constituent lists; SMALL663 is a current
    sub-$2B screen with 52 of 715 names dropped on max_1d_move >= 1.0. Every LEVEL is an UPPER
    bound. Points 1-4 are gaps and ratios BETWEEN rungs of the same panel, so a level bias moves
    every rung together and they are first-order immune; point 5-6's OOS levels are not, and are
    quoted as upper bounds.
