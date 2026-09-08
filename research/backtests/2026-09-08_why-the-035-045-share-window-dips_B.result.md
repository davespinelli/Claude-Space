# idea 226 — why-the-035-045-share-window-dips (lane B, 2026-09-08)

**ANSWERED. The queue's premise is REFUTED: the dip is NOT a dial-composition artefact —
holding the dial mix fixed makes it DEEPER, not shallower. It is a real but small hole that
the raw pooled curve cannot resolve from zero, and it is worth nothing as a rule (KILL of the
window instrument). No RULES change, no KEEP claimed; RULES.md, scan.py, bot.py and
baseline.py untouched.**

## Q1 reproduction, before any new number was read
Nothing was re-simulated. Idea 219's committed 36 120-row ladder IS the simulation (one 0 bps
run per book × dial × point, the 5 rungs derived by idea 217's exact cost identity); the cells
are a deterministic function of it plus the parent's seeds. Rebuilt 560 of 560 cells, matched
idea 219's committed `cells.csv` at **max |d| 1.457e-16** over 9 numeric columns with **0
full-mode string mismatches and 0 unmatched rows**, and reproduced its published local curve
to the digit (-0.0016 / -0.0030 / -0.0015 / -0.0011 / -0.0005 at centres 0.300–0.400) and its
crossing (**0.425**, last non-positive centre **0.400**). Split count raised 40 → 200 as a
superset of the same seeded stream, so the S=40 numbers reproduce *inside* this run.

## Q2 the queue's premise, as a checkable claim
Dip cells = share ∈ [0.225, 0.475] (the cells feeding the non-positive centres), 166 of 560.

| view | % of all | % of dip | conc | its own mean d **in the dip** | its overall mean d |
|---|---|---|---|---|---|
| GROSS | 14.3% | 3.0% | 0.21× | +0.0002 | −0.0000 |
| **N** | 14.3% | 36.7% | **2.57×** | +0.0016 | +0.0072 |
| BAND | 14.3% | 6.0% | 0.42× | +0.0099 | +0.0013 |
| **BAND+** | 14.3% | 33.7% | **2.36×** | **+0.0012** | +0.0016 |
| CADENCE | 14.3% | 0.0% | 0.00× | — | +0.0253 |
| SLEEVE | 14.3% | 0.0% | 0.00× | — | +0.0013 |
| **SLEEVE+** | 14.3% | 20.5% | 1.43× | **−0.0071** | +0.0010 |

Half right, and wrong where it matters. BAND+ and SLEEVE+ *are* over-represented (together
54.2% of dip cells vs 28.6% overall, 1.90×) — but **N is the most concentrated view of all
(2.57×) and the queue does not name it**, and **BAND+, the view the queue leads with, is
POSITIVE inside the dip (+0.0012)**: it concentrates there without dragging it down. Only
SLEEVE+ is negative there. Corpus (0.91×/1.04×) and rung (0.87×–1.08×) composition is flat.

## Q3–Q4 dial by dial, and leave one view out
4 of 7 views have a non-positive local window inside the dip range: N (4 windows, min
−0.0081), SLEEVE+ (7, min −0.0121), BAND+ (2, −0.0020), BAND (1, −0.0018). The 3 that do not
**have no support there**: GROSS spans 0.322–1.000 (3–5 cells per window), CADENCE 0.594–1.000
and SLEEVE 0.483–1.000 (**zero** cells in every window from 0.300 to 0.400). Every view that
reaches the window shows the hole.

**Leave-one-out: 0 of 7 removals clears it.** Dropping SLEEVE+ helps most (min −0.0036 →
−0.0019, mean −0.0014 → +0.0004) and still leaves 4 non-positive windows; dropping BAND+ —
the queue's own candidate — **deepens it to −0.0081**.

## Q5 hold the mix fixed — the answer
| pooled curve | min d in dip | mean d in dip | crossing |
|---|---|---|---|
| raw (idea 219's) | −0.0036 | −0.0014 | 0.425 |
| **dial fixed effects removed** | **−0.0068** | **−0.0047** | **none exists** |
| dial mix standardised to global | −0.0038 | −0.0015 | 0.400 |

Composition was **masking** the hole, not causing it. Over both tuned parameters (half-window
{0.050, 0.075, 0.100, 0.125} × m_min {8, 12, 20, 40}, all 16 reported), the **dial-demeaned
dip is negative in 16 of 16 grid points** (−0.0084 … −0.0025) while the raw dip is negative in
only 8 of 16 — it flips positive at m_min 20 and 40, where only the ALL and largest groups
survive.

## Q6 is the hole non-zero? (block bootstrap over 112 (corpus, dial, group) blocks)
| cell set | n | raw mean (t) [90% CI] | dial-demeaned (t) [90% CI] |
|---|---|---|---|
| deepest window [0.250, 0.400] | 105 | **−0.0036 (−1.67) [−0.0095, +0.0023]** | **−0.0068 (−3.08) [−0.0130, −0.0006]** |
| [0.325, 0.475] | 126 | −0.0008 (−0.46) [−0.0063, +0.0048] | −0.0039 (−2.11) [−0.0094, +0.0019] |
| [0.400, 0.550] | 91 | +0.0076 (+4.36) [+0.0026, +0.0132] | +0.0049 (+3.00) [+0.0003, +0.0102] |
| [0.475, 0.625] | 68 | +0.0116 (+4.22) [+0.0052, +0.0200] | +0.0087 (+3.61) [+0.0029, +0.0164] |
| everything outside the dip | 394 | +0.0076 (+8.17) [+0.0047, +0.0109] | — |

**The raw dip's own 90% CI covers zero; the dial-demeaned one does not.** So the honest reading
of idea 219's curve is: in this share window the modal constant's edge is **absent**, not
negative — and the only version of the hole that separates from zero is the one the queue
predicted would disappear. Raising 40 → 200 splits moves the dip by −0.00054: not split noise.

## Q7 rule 8 — the dip as a rule, and the KILL
"Fit inside the window, write the mode down outside it", window chosen on a training set over
115 pre-stated (lo, hi) pairs, applied untouched to the test set:

| trained on | window* | tested on | window | always-mode | Δ |
|---|---|---|---|---|---|
| corpus A | [0.200, 0.300] | corpus B | +0.0047 | +0.0052 | **−0.0005** |
| corpus B | [0.250, 0.400] | corpus A | +0.0050 | +0.0057 | **−0.0007** |
| 10 bps | [0.250, 0.425] | 5/15/20/25 bps | +0.0061 | +0.0059 | +0.0003 |
| published views | [0.250, 0.400] | extended views | +0.0020 | +0.0013 | +0.0007 |
| *fixed a priori* [0.225, 0.475] | — | all cells | +0.0053 | +0.0054 | −0.0000 |

Book-level, picks on ≤ 2016-12-31 and 2017–2026 read once, pooled over 7 views × 5 rungs:
corpus A ORACLE 1.0336 > **MODE-LOO 1.0109 > WINDOW-X 1.0100** > WINDOW-FIX 1.0093 >
SEL-SHARPE 1.0042 > SEL-4B 0.9643 > RANDOM 0.9531 > CONST-INC 0.9275; corpus B ORACLE 0.7744 >
SEL-4B 0.7440 > **MODE-LOO 0.7351 > WINDOW-FIX 0.7329 > WINDOW-X 0.7328** > SEL-SHARPE 0.7268 >
RANDOM 0.6806 > CONST-INC 0.6470. The window costs **−0.0009 (A) and −0.0024 (B)** of OOS
Sharpe against doing nothing about share at all — the same direction idea 219 found for its
share FLOOR, now reproduced for a share WINDOW.

## Q8 benchmarks and both KEEP paths (idea 219's ladder re-read, not new)
SPY OOS 15.45% / 0.8820 / −33.72%. RULES v1 @10 bps OOS: U56 7.73% / 0.7471 / −13.83%,
B136 5.94% / 0.5763 / −21.19%, SMALL 17.15% / 0.5540 / −44.83%.
4a: A 1511/1857/1996/2056/2106 and B 1250/1589/1906/2204/2532 at 5/10/15/20/25 bps.
4b: A 464/301/179/105/64 and B 410/307/248/178/137. By parent: B136 1004/10750, U56
1389/14620, **SMALL 0 of 10750**. These are idea 219's own committed rows re-read, not an
independent reproduction of idea 136 — counted as zero new evidence for it. Per idea 144 a
re-dialled book is the same book; nothing is proposed.

## Predictions: 4 of 7 hit
P1 HIT (1.46e-16, crossing 0.425/0.400) · P2 **MISS** (BAND+ 2.36×, SLEEVE+ **1.43×**, just
under the 1.5× bar) · P3 **MISS** — the run's headline: demeaning deepens the dip to −0.0068 ·
P4 HIT (N, BAND, BAND+, SLEEVE+) · P5 **MISS** (no single removal clears it) · P6 HIT
(A −0.0009, B −0.0024) · P7 HIT (0 passes).

## What PROTOCOL should carry
The share axis has a hole between roughly 0.25 and 0.42 where the modal constant banks
**nothing** (raw −0.0036, CI covering zero) against **+0.0076 (t +8.17)** everywhere else, and
it is a property of the share axis, not of which dials sit there. Report it as a region of
**no evidence for the constant**, never as a region where fitting wins — the gate that acts on
it loses on both corpora.

## Caveats
Survivorship (idea 54) on B136/U56/both small panels; every arm inherits it equally so the
paired comparisons are unaffected and no LEVEL is tradable. Cells are not independent (shared
books, shared simulations across rungs, shared parents); every t is over correlated units with
an optimistic nominal size, and the bootstrap resamples whole (corpus, dial, group) blocks.
The modal share is estimated on half-corpora of 4–57 books, so its sampling error is largest
exactly where the share is lowest — the region under test. S=200 removes split noise, not
corpus noise: 560 cells still come from ~112 blocks. Corpus A's SMALL484 lacks the
max_1d_move ≥ 1.0 screen that corpus B's SMALL439 applies (inherited, unchanged). Ideas 38,
126 and 144 carry over.

Script `research/backtests/2026-09-08_why-the-035-045-share-window-dips_B.py`; artefacts
`.console.txt`, `.cells.csv`, `.curves.csv`, `.lodo.csv`, `.composition.csv`,
`.walkforward.csv`, `.keep.csv`.
