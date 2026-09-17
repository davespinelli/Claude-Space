# Idea 1229 (cloud lane, 2026-09-17) — at what IS WINDOW LENGTH does a HEADLINE FORM separate from its own NL_PERM band?

**ANSWERED = AT NO WINDOW, AT NO CADENCE, AND THE SIGN IS THE WRONG WAY ROUND.**
`L* = NONE` for all three headline forms and both controls. 0 of 18 (form, window) cells
separate at the primary cadence; **1 of 108** across all three cadences, against **5.4**
expected at alpha 0.05 by chance (gate G12) — so the one separating cell (YEAR / NG / L1260 /
H_NARROWEST, p 0.0185, **2 moves**) is at or below the false-positive rate and is evidence of
nothing.

**THE AGGREGATE SIGN IS THE RESULT.** Over the 104 (cadence, set, window, form) cells with a
defined band, the observed delta sits **ABOVE** its own NL_PERM mean at **19**; a coin gives 52.
Two-sided binomial **p = 3.8e-11**. Mean gap **-0.0298** of Sharpe, median -0.0147, mean
p_NL_PERM **0.6678**. **Re-dealing a form's own destination multiset to random folds beats the
form's actual timing**, systematically, at every cadence and every window. 1227 read its grid as
"no form beats holding"; the sharper reading is that the forms' *timing* is worse than random,
and the destinations are doing whatever work there is.

**THE REQUIRED PRECISION, FOR THE MINORITY ON THE POSITIVE SIDE.** 4 of 54 ALL4 form cells even
have a positive gap. The cheapest is **H_RUNNERUP at L504 / QUARTER: 38 years of tape** (gap
+0.0107 against half-width 0.0242, fitted shrink exponent b 0.935), then L252 at 73 years and
L1260 at 943. Under the pre-declared 50-year attainability bar that triggers outcome **(B)
SEPARABLE ON AN ATTAINABLE TAPE** — but the number **rests on 3 moves in 193 folds**, so it is a
LOWER BOUND on the tape this question needs, not a forecast that 38 years would settle it.
H_NARROWEST, H_ANY and CH_RAW need **infinite** tape at every window: their gaps are negative.

**MORE FOLDS ON THE SAME TAPE BUY ESSENTIALLY NOTHING — THE RUN'S MOST USEFUL BYCATCH.** MONTH
(573 folds), QUARTER (193) and YEAR (46) read the **same 17.7 years**. If extra folds were
information the band would shrink by sqrt(F_month/F_year) = 0.283 from YEAR to MONTH. Measured
over 24 (window, form) cells the ratio is **0.934** (Q/Y **0.832** against a predicted 0.488) —
an implied cross-cadence exponent of **b = 0.027** against the 0.5 iid would give. The
within-cadence subsample ladder (fractions 0.25 / 0.50 / 1.00, 40 draws each) fits **b = 0.545
mean / 0.494 median** over 52 cells, i.e. dropping folds from a fixed span does scale near-iid.
The two readings together say the extrapolation basis is sound and **the F in F\* must come from
new calendar years, never from slicing the existing tape finer**. Any committed claim in the
record that bought resolution by going to a finer fold cadence bought ~7%, not 3.5x.

**BOTH KEEP PATHS AND RULE 8.** 66 rung books: **4a 0**, 4b full 17, 4b OOS 16, BOTH **16** —
all U56 and B136 rungs of the anchor family the record has already committed (U56 N=15, the
N=20/H=126/GROSS=0.75/CADENCE=W anchor, H=21, GROSS 0.50-0.75; B136 GROSS 0.50-0.70). 540
stitched chooser curves: 4a 0, 4b full 128, 4b OOS 126, **all U56**. Rule 8 with BOTH dials plus
the form chosen on the pre-2017 folds only and 2017-2026 read once: **4a 0 of 270, 4b 50 of
270**, all U56. Mean OOS Sharpe of the IS-chosen cell **0.8558** against **doing nothing
0.8845** (**-0.0286**). The IS-chosen cell is MONTH/L504/CH_RAW on U56 (OOS 17.55% / 1.1572 /
-20.51% against the anchor's 17.16% / 1.1759 / -19.13%), MONTH/L252/H_RUNNERUP on B136 (16.04% /
1.0129 against 16.29% / 1.0240), MONTH/L504/CH_RAW on SMALL (6.19% / 0.3974 against 7.09% /
0.4534). U56 SPY OOS 15.15% / 0.8686 / -33.72%; live RULES v2 OOS 9.42% / 1.2717 / -12.05%.

**VERDICT: KILL (capital).** No new book, no memo, no RULES change. Nothing clears 4a anywhere
and every 4b pass is a book already in the record.

**SURVIVORSHIP (rule 9).** B136 and SMALL are current constituents; SMALL is the sub-$2B screen
with 51 of 715 tickers dropped for max_1d_move >= 1.0 (664 investable), SPY benchmark only. The
bias does not cancel out of the OOS levels or the 4b legs, so any pass there is an upper bound.
It largely does cancel out of a gap-to-band ratio and out of the same-tape band ratio, which are
this run's two headlines.

**GATES 20 of 20.** G8 reproduces 1227's committed (window, form) deltas to 4.9e-04; G3 puts
live RULES v2 U56 MaxDD at the committed -12.05%; G10 confirms 1227's value-based move
definition (the anchor is one book under four names). Runtime 36s, offline, deterministic.
