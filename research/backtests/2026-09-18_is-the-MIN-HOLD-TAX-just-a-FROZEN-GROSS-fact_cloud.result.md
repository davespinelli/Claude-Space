# Idea 1066 (lane cloud, 2026-09-18) — is the MIN-HOLD TAX just a FROZEN-GROSS fact?

**VERDICT: KILL (capital), NO NEW BOOK / ANSWERED: YES — THE TAX IS FROZEN SHARE, NOT SELECTION.**
228 cells (18 REAL min-hold rungs, 210 RANDOM-freeze seeds), 3 panels, 11 of 11 gates PASS.

## The answer
At MATCHED frozen share, a random-freeze book — a fraction f of the current holdings retained
by a coin, **no score and no age input at all** — reproduces the real min hold's drawdown tax:
**113% of it on U56, 132% on B135, 73% on SMALL663** (tax = MaxDD deepening vs the H=0 book,
averaged over the five matched rungs: REAL +2.85 / +3.77 / +4.67pp vs RANDOM +3.22 / +4.97 /
+3.39pp). The selection channel (REAL minus its own matched-share RANDOM, 8 seeds per rung,
15 rungs) is **d_MaxDD +0.10pp (REAL worse at 7 of 15), d_CAGR -0.87pp (REAL better at 5 of 15),
d_Sharpe -0.0212 (>0 at 6 of 15), d_OOS_Sharpe -0.0386 (>0 at 7 of 15)** — no reliable sign on
any leg. Freezing *by age* is not better than freezing *by coin*: the constraint's whole cost,
and its whole CAGR gain, is bought with FROZEN WEIGHT. Pre-declared outcome (A).

## Two things the ladder says that the tax story did not
1. **The tax is NOT monotone in H, the control's is (nearly) monotone in f.** U56 MaxDD runs
   -18.18 / -18.46 / -20.19 / **-25.53** / -19.13 / -21.84% at H = 0 / 5 / 21 / 63 / 126 / 252,
   so the worst rung is H=63 (the "7 pp" 1065 reported, replayed here to 0.16pp — gate G8) and
   the incumbent H=126 pays only 0.95pp. RANDOM at the matched shares runs +0.59 / +3.35 /
   +3.42 / +3.14 / +5.60pp — smooth. H=63 is a bad draw of the freeze, not a rung of a ladder.
2. **The committed anchor's DD leg is a favourable draw.** U56 H=126 posts MaxDD -19.13% while
   its own matched-share random control posts **-21.32% +- 0.66pp (z +3.34)**, i.e. 2.19pp
   better than freezing the same weight at random names — and the control's mean would FAIL
   4b's DD cap (-20.23%), which the anchor clears by 1.10pp. Only **3 of 8** share-matched seeds
   pass 4b at s=0.962. The binding leg of the 2026-09-04 pass survives a re-draw of *which*
   names the min hold happens to freeze about a third of the time.

## Capital
**4a 0 of 228. 4b 40 of 228, every one on U56**, and none is reachable: rule 8 (IS Sharpe on
warm-up..2016, OOS read once) picks REAL H=252 (4b FAIL on DD, -21.84%) on U56 and SMALL663 and
REAL H=63 (4b FAIL) on B135 once the artefact below is removed. Chooser-minus-anchor mean
+0.0880 over 12 choosers and +0.1432 vs H=0, but IS/OOS rank correlation is +0.280 with three
of twelve negative, and no pick clears 4b. Nothing is proposed for capital; nothing enacted.

## The artefact, flagged rather than banked
**RANDOM f=1.00 on U56 reads 12.45% / 1.3231 / -16.91%, OOS 1.2445, 0.91 turns per year and
passes 4b at 5 of 5 seeds — and the pooled IS chooser lands on it at 2 of 3 panels.** It is a
buy-and-hold of the twenty names the score picked in the first warm-up week of 2009, held for
seventeen years on a CURRENT-CONSTITUENT panel: the rule-9 bias in its purest form, and not
implementable at any date. It is published (it is the f dial's endpoint) and excluded from every
KEEP reading via the C_ALLx chooser, which was declared after the first pass and said so in the
script. The bare fact that an honest IS chooser walks into it is the finding, not the number.

## Survivorship (rule 9)
U56/B135 are current-constituent lists, SMALL663 a current sub-$2B screen (52 of 715 dropped for
max_1d_move >= 1.0). Levels are optimistic and every 4b pass is an UPPER bound. The headline is a
DIFFERENCE between two retention rules on the same panel, same gate, same cadence, same sizing —
first-order immune to a level bias moving both arms together. Not neutral, and stated: a current
panel cannot hold the names a min hold would have ridden to delisting, so the REAL arm's tax here
is a LOWER bound on the live one, and outcome (A) is the reading this bias flatters least.

Script: `2026-09-18_is-the-MIN-HOLD-TAX-just-a-FROZEN-GROSS-fact_cloud.py`
