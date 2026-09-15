# Idea 905 — does the PLACEMENT channel (+0.0015) survive a gap draw that is not 871's?
Lane B, 2026-09-15. Script `2026-09-15_does-the-PLACEMENT-channel-survive-a-gap-draw-that-is-not-871s_B.py`.

**ANSWERED — NO. IT IS A PROPERTY OF THE GAP MARGINAL, NOT OF REDRAWING PLACEMENT.** 885's
`signed(UG_REAL) = +0.00154` reproduces here **bit-for-bit** (arm by arm, 1.94e-16 over six
committed columns × 1,152 arms), so the number is real. But it does not survive a draw that
respects the arm's own gap distribution: the two draws that CHANGE the marginal are outside
the ±0.0010 band in **2 of 2** (UNIF **+0.00154**, LNFIT **+0.00125**) and the three that
PRESERVE it are inside in **3 of 3** (EBOOT **+0.00009**, GBLOCK **−0.00051**, GPERM
**+0.00059**). The decisive level is GPERM — the arm's own reduced-gap multiset, permuted,
so the marginal distance is exactly zero and only the ORDER and the length↔gap coupling are
destroyed: it reads **inside the band**. **KILL for the "placement channel" reading**;
nothing promoted, `RULES.md`, `PROTOCOL.md`, `scan.py`, `bot.py`, `baseline.py` untouched
(rule 6). Two corrections to the record are proposed as findings, not applied.

SELECTION: lane B claims the LAST open idea — 905, which carries a price leg (every arm is a
de-grossing book), so it can and does carry the mandatory rule-8 walk-forward.

## Setup
2 tuned params, the queue's own: **PARAM 1 gap draw {UNIF, LNFIT, EBOOT, GBLOCK, GPERM} ×
PARAM 2 cap rule {REAL, DOM, LONE}**. Reported axes, never selected over: panel {U56 56,
B136 136, SMALL 664}, family {BREADTH, VOL20, DISP, CORR} × {HI, LO}, q {0.07, 0.12, 0.17},
w {252, 1008}, depth {0.50, 1.00}, cadence {D, W}, gross {0.75, 1.00}, cost rung {0, 10, 25}.
10 bps, next-day fills, no shorting, no leverage. **1,152 arms × 19 nulls × 200 seeds =
4,377,600 placebo paths, each priced at three rungs = 13,132,800 placebo books.** Every grid
point is in `.gap.csv` / `.excess.csv` / `.draws.csv` / `.grid.csv`. GBLOCK's block length
`b = round(sqrt(m+1))` is DERIVED from the sample size, not fitted — it is not a third param.

**THE NEW OBJECTS.** All five draws lay `m+1` gaps summing to `n−k` in 871's own REDUCED
space (interior gaps carry a mandatory +1 so no two runs can merge). UNIF is
`_gaps_like_switchmatch`, verbatim. LNFIT fits a log-normal to the arm's own reduced gaps by
moments on `log(g+1)`. EBOOT iid-bootstraps the arm's own reduced-gap multiset. GBLOCK
circular-block-bootstraps the arm's own reduced-gap SEQUENCE, so local serial structure partly
survives. GPERM freely permutes the arm's own reduced-gap multiset — marginal preserved
**element for element**, order destroyed. Every draw except UNIF is projected onto the exact
total by the same largest-remainder step, so the four alternatives differ only in what they draw.

## Gates (printed before any hypothesis was read)
| gate | reading | bar |
|---|---|---|
| G2 rate match | `max|mean(placebo) − mean(real)|` **0.000e+00** | 1e-12 |
| G3 medians vs 885's 14 committed numbers | worst |Δ| **4.91e-06** | 1e-05 (5 d.p.) |
| **G3b arm by arm vs 885's `.gap.csv`** | **1.94e-16** over 6 columns × 1,152 arms | 1e-12 |
| G4a exact total / G4b interior ≥ 1 / G4c k,m preserved / G4d GPERM multiset exact | **0 / 0 / 0 / 0** violations | 0 |
| G7 BLOCK2 calibration | **−0.00000** (SE 0.00026, z +0.00) | ≤0.0010, |z|<2 |
| G8 OP_REAL ≡ BLOCK | **0.000e+00** | 0 |

G5 circular counts (2.654% of matched-null construction checks, 67 LONE max-run) inherit
882/885's named cause — a draw may put both the leading AND trailing gap at 0, circularly
merging the first and last runs. Every headline is re-read on the violation-free arms
(`clean` column in `[4]`), which moves no verdict.

## The headline (cap REAL, 10 bps, 1,152 arms, 200 seeds, band ±0.0010)
| draw | what it preserves | W1/mean | gap CV | longest gap ÷ real | signed | mean/SE | verdict |
|---|---|---|---|---|---|---|---|
| UNIF (871) | nothing | 0.416 | 0.973 | 0.635 | **+0.00154** | +6.95 | OUTSIDE |
| LNFIT | nothing | 0.406 | 2.086 | 1.619 | **+0.00125** | +5.75 | OUTSIDE |
| EBOOT | marginal in law | 0.210 | 1.484 | 0.915 | +0.00009 | +0.71 | inside |
| GBLOCK | marginal + serial | 0.194 | 1.478 | 0.918 | −0.00051 | +0.39 | inside |
| GPERM | marginal **exactly** | **0.000** | 1.529 | 1.000 | +0.00059 | +2.98 | inside |

Real arms' own reduced-gap CV: median **1.529**, IQR [1.246, 1.813], mean gap 86.8 days.
871's uniform composition is far too FLAT (CV 0.973) and cannot produce a long quiet stretch
(longest gap 0.635× the real one); the log-normal overshoots the other way (CV 2.086, 1.619×).
**Both directions of misfit cost the same sign**, so the carrier is misfit MAGNITUDE, not
flatness — "uniformity" is one instance of a gap-marginal misspecification, not the mechanism.

## Pre-registered hypotheses
| H | bar | result |
|---|---|---|
| H_UNIF | only UNIF outside the band | **REFUTED** — LNFIT is outside too (it is also a wrong marginal) |
| H_PLACE | all five outside, same sign, spread ≤0.0010 | **REFUTED** — spread 0.00205, signs differ |
| H_ORDER | GPERM outside the band | **REFUTED** — +0.00059, inside; order alone costs nothing resolvable |
| H_SERIAL | \|GBLOCK\| < \|GPERM\| | CONFIRMED (0.00051 < 0.00059) — but **both inside the band**, so this ordering is within resolution and carries no weight |
| H_MONO | ρ(W1, \|channel\|) ≥ +0.50 over 15 cells | **REFUTED** — +0.258 |
| H_CAPINV | same sign at all three cap rules | **REFUTED** — 2 of 5 draws |
| H_COSTINV | every signed gap moves <0.005 across 0/10/25 bps | CONFIRMED — worst range 0.00051 |

H_MONO's refutation is a property of the DOM/LONE cells, which each subtract their own OP
anchor (itself outside the band at DOM, −0.00130) and so carry a second noisy term. On the
five cap-REAL cells alone — the object of the idea — ρ(W1, SIGNED channel) = **+0.700** and
ρ(W1, |channel|) = +0.600. **This is a diagnostic, not the pre-registered bar**, and it is
reported as such: the pre-registered reading is REFUTED.

**RESTRICTION (H_CAPINV).** The +0.0015 is a **cap-REAL object**. With the length channel
removed by differencing against OP, the isolated channel at DOM and LONE is at or below zero
for four of five draws (UNIF DOM −0.00139 / LONE +0.00097; EBOOT −0.00089 / −0.00111; GBLOCK
−0.00106 / −0.00153; GPERM −0.00076 / −0.00088). Reshaping the lengths and redrawing the gaps
do not compose additively, so no reading here transports to a reshaping null.

## Rule 8 — walk-forward (IS ..2016-12-31 fitted, OOS 2017-01-01.. read once)
**(a) The channel does not walk forward at cap REAL.** ρ(IS gap, OOS gap) ≥ +0.30 in **1 of 8**
families for UNIF and **0 of 8** for the other four. Per window the four marginal-preserving
draws flip sign (LNFIT −0.00353→+0.00094, EBOOT −0.00285→+0.00186, GBLOCK −0.00198→+0.00161,
GPERM −0.00215→+0.00200) while UNIF keeps its sign and shrinks (+0.00330→+0.00155). The pooled
median is the only stable quantity; the per-arm number is not. The DOM cells — the LENGTH
channel, a different object — do walk forward (7–8 of 8 families), which is the contrast.

**(b) The books.** The arm grid is 885's, so the IS-only selector returns 885's own books and
reproduces them exactly — a gate on this run's plumbing, not a new capital finding.

| panel | IS-pick | FULL CAGR / Sharpe / MaxDD | halves | OOS CAGR / Sharpe / MaxDD | 4a | 4b |
|---|---|---|---|---|---|---|
| B136 | CORR-HI q0.12 w252 d1.0 W g1.0 | 13.91% / 1.166 / −16.63% | 1.289 / 1.037 | 12.97% / 1.154 / −16.63% | fail | **PASS** |
| U56 | CORR-HI q0.07 w1008 d1.0 W g1.0 | 12.73% / 1.034 / −22.93% | 1.160 / 0.915 | 12.41% / 1.016 / −22.93% | fail | fail |
| SMALL | VOL20-LO q0.17 w252 d1.0 D g1.0 | 5.04% / 0.404 / −48.52% | 0.736 / 0.201 | 2.00% / 0.203 / −48.52% | fail | fail |

Comparands: **SPY** U56 15.13% / 0.885 / −33.72% (OOS 15.27% / 0.874), B136 15.16% / 0.886 /
−33.72% (OOS 15.33% / 0.877), SMALL 14.06% / 0.858 / −33.72% (OOS 15.33% / 0.877). **RULES v2
(live)** U56 8.64% / 1.208 / −11.90% (OOS 9.49% / 1.286), B136 7.98% / 1.101 / −12.18% (OOS
7.88% / 1.108), SMALL 4.30% / 0.663 / −13.89% (OOS 3.75% / 0.559). Unselected base rates: 4a
**0 of 384 on all three panels**; 4b 44/384 (B136, 11.5%), 61/384 (U56, 15.9%), 0/384 (SMALL).
The one 4b PASS (B136 CORR-HI, OOS 12.97% / 1.154 / −16.63%) was already committed by ideas
883 and 885 and was not proposed for adoption then; it is not proposed now. **No memo, nothing
promoted** — this run is not a KEEP-candidate.

SURVIVORSHIP: U56 and B136 are current-constituent lists; SMALL is current constituents of the
sub-$2B screen with every `max_1d_move ≥ 1.0` ticker dropped first, so its CAGRs are the most
optimistic numbers here and any 4b reading on it is an upper bound. The headline is a
DIFFERENCE BETWEEN TWO NULLS ON THE SAME ARM and is far less exposed to that bias than a level.

## Two corrections proposed to the record (findings, not applied)
1. **A run-length-matched null should be gap-MARGINAL-matched by name.** 871's uniform
   composition buys a systematic **+0.0015 of Sharpe** against BLOCK on de-grossing arms at
   cap REAL, purely from a gap distribution the arm never had. The fix is free and is a
   one-line change to the draw: permute the arm's own reduced gaps (GPERM, +0.00059, inside
   the band) or bootstrap them (EBOOT, +0.00009). Neither costs a parameter, neither changes
   k, m, the switch count or the rate, and either removes the bias. This bears directly on
   the open queue item asking whether PROTOCOL should require a run-length-matched null by
   name: **matching run lengths is not sufficient — the gaps need matching too.**
2. **"Clean-arm" numbers in the record are not reproducible across runs and should be quoted
   with their null set attached.** `clean` means "no matched null IN THIS RUN violated the
   circular k/m match on this arm", so it is a property of the ARM × NULL SET, not of the arm.
   885 published UG_REAL on clean arms as +0.00153 over **1,110** clean arms; this run's own
   flag admits only **561** (the four new draws put a zero on a boundary gap ~4.5× as often as
   871's composition does: share-0 ≈0.05 vs 0.011) and the same object reads **+0.00166**.
   Re-read on 885's OWN committed clean flag it is **+0.00153**, reproducing to 3e-06 — the
   arm-level numbers are identical (G3b 1.94e-16); only the SUBSET moved.

## Verdict
**KILL** for the premise. The +0.0015 is real, reproduces bit-for-bit, and is a
GAP-MARGINAL MISSPECIFICATION — not evidence that redrawing placement costs anything. Nothing
proposed for `RULES.md`.
