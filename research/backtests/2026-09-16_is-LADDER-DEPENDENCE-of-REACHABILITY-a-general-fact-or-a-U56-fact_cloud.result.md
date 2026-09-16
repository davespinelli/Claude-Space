# Idea 1101 (cloud, 2026-09-16) — is LADDER-DEPENDENCE of REACHABILITY a general fact or a U56 fact?

**ANSWER = A U56-AND-B136-AND-ANCHOR-A FACT. PREMISE REFUTED.** 1096's "2 of 4" reproduces
exactly on its own two panels (gate G7, set `{GROSS, CADENCE}` on both) and then dies everywhere
else: **SMALL/A = 1 of 4, U56/B = 0, B136/B = 1, SMALL/B = 0** under the headline chooser
`C_ISSHARPE`. The count is 2 in 2 of the 6 (panel, anchor) cells and the reaching SET is the same
in only those 2. Mean headline reach count **1.0000** against a uniform-argmax expectation of
**0.7111** (1/9 + 1/4 + 1/10 + 1/4) — above chance, but by 1.4x, not by a level.

**THE MECHANISM, WHICH IS THE PART WORTH KEEPING.** The GROSS ladder is a **boundary attractor
under every chooser**: its IS-Sharpe and IS-CAGR argmax is **0.75 (the top rung) in all 6 cells**
and its IS-DD argmax is **0.30 (the bottom rung) in all 6**. "GROSS reaches the anchor" therefore
says nothing about the anchor — it says the anchor's gross happens to equal the chooser's
boundary. Anchor A sits at 0.75 and is reached from GROSS on all three panels; anchor B sits at
0.55 and is reached from GROSS on none. And the reach is bought at a **Sharpe margin of 1.09e-04
to 9.92e-04** — below the resolution of anything this record can measure. Across all 72
decisions, reach == endpoint-ness on **62 of 72 (86.1%)**: endpoint cells reach **6 of 9**,
interior cells **7 of 63**. H_BOUNDARY is REFUTED as a *perfect* predictor (the 10 discordant
cells are named in the console) but is by far the strongest one available.

**PER LADDER, ALL PANELS / ANCHORS / CHOOSERS:** GROSS 6/18, CADENCE 5/18, H 2/18, **N 0/18**.
1096's "N and H never reach" survives as a fact about N (0 of 18, mean P_boot 0.050) and does
**not** survive for H (2 of 18, both on B136 anchor B).

**IS THE 2-OF-4 EVEN MEASURED? MOSTLY NOT.** Bootstrap P(anchor is the IS argmax), 1000 joint
moving-block redraws (L=63, same block index on every rung so cross-rung correlation survives):
**11 of 24 headline decisions are resolved** at the 0.90/0.10 bar; P_boot range 0.000-0.949. The
two U56 reaches 1096 published sit at P_boot **0.716** (GROSS) and **0.278** (CADENCE) — the
CADENCE reach is a coin flip that landed. H_RESOLVED REFUTED.

**RULE 8 AND BOTH KEEP PATHS — NOTHING PROPOSED.** The 162 rung books are byte-identical across
both dials; only which rung gets *called* reached moves, so 4a and 4b are invariant by
construction, and are scored because rule 4 says so. Rung chosen on IS 2009-2016 alone, 3
choosers, OOS read ONCE: **6 of 72 picks clear 4b full, 7 of 72 clear 4b OOS, 0 of 72 clear 4a.**
Whole grid, 162 rungs: 4b full 26, 4b OOS 30, 4a 0 (U56 20/54, B136 6/54, **SMALL 0/54**). Every
passing pick is the standing anchor U56 / W / H=126 / N=20 / gross 0.75 — full **15.58% / 1.1397
/ −19.13%**, halves 1.2037 / 1.0971, OOS **16.97% / 1.1643 / −19.13%** against SPY OOS 15.21% /
0.8711 / −33.72% and live RULES v2 OOS 9.45% / 1.2762 / −12.05% — or a U56 anchor-B H rung. No
new book.

**SMALL IS NOT A NARROWER VERSION OF THE LARGE PANELS, IT IS A DIFFERENT TAPE.** 0 of 54 SMALL
rungs clear 4b on any leg pattern: L_H1 1/54, L_H2 0/54, L_OOS 0/54. SMALL's own RULES v2 reads
4.30% / 0.6637 / −13.89%. Any reach result on SMALL is a statement about a book nobody would run.

**GATES 7 of 7.** G1 fast runner == `engine.backtest` 1.39e-17; G2 CROSS-RUN the committed U56
anchor-A triple 3.18e-07; G3 SPY OOS 1.70e-04; G4 live RULES v2 MaxDD == −12.05% 4.95e-05; G5
determinism 0.00e+00; G6 fast runner == engine at anchor B (M cadence) 2.78e-17; **G7 CROSS-RUN
1096's D3 reproduces `{GROSS, CADENCE}` on both panels, exactly.**

**THE DECLARED APPROXIMATION.** P_boot resamples ONE tape, so it is sampling error around this
regime, not regime uncertainty: every P_boot is closer to 0 or 1 than the truth, and H_RESOLVED
is scored in the direction that favours SUPPORTED. A decision called resolved here may still be
a coin flip across regimes; one called unresolved is unresolved a fortiori.

**SURVIVORSHIP (rule 9).** U56 and B136 are current-constituent lists; the SMALL pool is the
current constituents of a sub-$2B screen (663 names after dropping 52 with `max_1d_move >= 1.0`
from data/small_meta.csv, tape 2010-01-04 → 2026-09-11), so it is missing every name that fell
below the screen, delisted or went to zero. A reach decision contrasts two rungs over the same
inflated tape and the bias very largely cancels; it does not cancel out of the 4b legs, so the 26
full-sample 4b passes are an UPPER bound.

**WHAT THE RECORD SHOULD DO WITH IT (proposed, NOT enacted — rule 6).** A published statement
that a book is "rule-8 reachable" should name the LADDER it was reached from and the anchor's
POSITION on that ladder, because a reach from a boundary rung is a property of the ladder's
endpoints and not of the book. Filed as follow-up ideas below.
