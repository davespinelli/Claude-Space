# Idea 1192 (lane B, 2026-09-17) — does the COARSE END of a FRACTION LADDER move MORE than the FINE END on EVERY FAMILY?

**ANSWERED = YES ON MOST BUT NOT ON EVERY FAMILY (B), AND THE CARRIER IS THE ENDPOINT — THROUGH A
DEGENERACY, NOT THROUGH LENGTH AND NOT THROUGH THE LOG-LINEAR CHANNEL ANYONE WOULD HAVE MODELLED.**

Script `2026-09-17_does-the-COARSE-END-of-a-FRACTION-LADDER-MOVE-MORE-THAN-THE-FINE-END-ON-EVERY-FAMILY_B.py`.
Two tuned dials, 12 cells, all published: LADDER END {E_FINE, E_COARSE, E_SLIDE} x BETWEEN TERM
{B_ENDPOINT, B_MATCHED, B_SD, B_SPAN}. 486 families = (panel, dial ladder, rung, statistic).
Gates **17 of 17 PASS**. Hypotheses 3 SUPPORTED / 3 REFUTED / 1 KNIFE-EDGE. Runtime 44s.

## THE IDENTIFICATION, WHICH IS THE POINT OF THE RUN
The record has only ever walked its fraction ladder in ONE direction — 1188's
L2/L3/L4/L6/L8 grow the rung COUNT and the ENDPOINT together, so the two channels are
confounded in every committed figure. This run separates them by construction, not by a fit:

- **E_COARSE** holds the fine anchor f=8 and adds rungs at the coarse end
  ({1,8} / {1,6,8} / {1,5,6,8} / {1,4,5,6,8} / L8), so **fmax = 8 at every rung count and the
  B_ENDPOINT between term is IDENTICAL across the whole walk** (gate G8, dev 0; `.walks.csv`
  med_B = 0.4527 at all five rungs). Everything that moves inside E_COARSE is LENGTH.
- **E_SLIDE** freezes the rung count at 2 — the published L3's own count — and slides the window
  ({1,2,3} / {1,3,4} / {1,4,5} / {1,5,6} / {1,6,8}), so **length cannot move** (gate G8b).
  Everything that moves inside E_SLIDE is the ENDPOINT.
- The two walks meet at L8 and agree there to **0.000e+00** (gate G9, 288 coordinates).
- `dlog v = dlog W - dlog B` is an **identity** (v = W/B exactly), so ATTRIB_B is an attribution
  and not a regression.

## THE ANSWER
| | median over the 486 families |
|---|---|
| **share(coarse move > fine move)**, headline cell | **0.6173** -> **(B) YES ON MOST** |
| median excursion, COARSE (L3 -> {1,2}) | **0.9822** |
| median excursion, FINE (L3 -> L8) | **0.6036** |
| **LSENS_COARSE** (fmax frozen -> LENGTH only) | **1.2847** |
| **LSENS_SLIDE** (k frozen -> ENDPOINT only) | **4.8344** |
| mechanism ratio LENGTH / ENDPOINT | **0.2657** -> **(M_END) BETWEEN ENDPOINT** |
| median ATTRIB_B at the coarse move | **0.8431** |

The mechanism reads **(M_END) at 4 of 4 between forms** and the share sits in a narrow
**0.5679 .. 0.6420** across all 12 dial cells: neither dial changes the answer. Length is not
zero — LSENS_COARSE 1.2847 clears the 1.10 live bar, so **H3 SUPPORTED**: with the between term
frozen by construction the figure still moves 1.28x, purely through the within median's
composition. But the endpoint channel is **3.8x larger**, and it carries **84%** of the coarse
move's magnitude (H4, which predicted the within term would carry it, is **REFUTED**).

## WHY THE COARSE END MOVES MORE — AND WHY THE OBVIOUS ENDPOINT MODEL GETS IT BACKWARDS
Printed **before any tape was read** (`.analytic.csv`): on a perfectly log-linear
`m[f] = log f` with a frozen within term, the pure-endpoint world gives
**MOVE_COARSE 0.4606 against MOVE_FINE 0.6381** — the **FINE** end moves more, by construction
(gate G7c). So a high observed share **refutes** that model: **H2 LOGLIN REFUTED at 0.6173**.

The real carrier is a **near-degeneracy at f=2** (`.degeneracy.csv`):

| step | median | share < 0.5 | share < 0.25 | log-linear prediction |
|---|---|---|---|---|
| B(fmax=2) / B(fmax=3) **coarsen** | **0.4343** | 0.5514 | 0.3292 | 0.6309 |
| B(fmax=8) / B(fmax=3) **refine** | 1.7116 | 0.1296 | 0.0700 | 1.8928 |

A half-tape contrast of MAXDD medians is a contrast over **two** segments of a running minimum
and very nearly vanishes: med_B runs **0.0610** at fmax=2 against **0.2246** at fmax=3 and
**0.4527** at fmax=8. The ratio divides by it and explodes — **median ratio 14.3466 at L2
against 3.9105 at L3**. Refining is well-behaved (1.71 observed vs 1.89 predicted); coarsening
is not (0.43 vs 0.63). **The excursion is an endpoint fact about the SMALLEST between term the
ladder can be given, not about how many rungs it has.**

**B_SPAN does not save it.** Lane B's 1158 run proved the span-normalised between term is
*exactly* ladder-invariant on a log-linear `m[f]` (gate G7 reproduces it at dev 0.000e+00 on all
three walks). On this tape it buys **nothing at the coarse end**: observed LSENS 5.1208 /
1.2847 / 6.1053 against the analytic 1.0000, and the share only falls 0.6173 -> 0.5679. A
normalisation of the log-linear channel cannot fix a degeneracy that is not log-linear.

## NOT ON EVERY FAMILY — AND THE HEADLINE STATISTIC IS THE COUNTEREXAMPLE
**H5 UNIVERSAL REFUTED: 3 distinct outcome bands** across the 3 panels and 6 statistics
(`.universality.csv`).

- by panel: U56 **0.7160** (B), SMALL 0.6667 (B), **B136 0.4691 (C)**.
- by statistic: CAGR 0.7901, VOL 0.7654, ULCER 0.7284 (all B); CALMAR 0.5802, SHARPE 0.4568 (C);
  **MAXDD 0.3827 — band (D), THE FINE END MOVES MORE** (med coarse 0.4428 vs fine 0.5805).

**MAXDD is the lineage's headline statistic** (1140/1148/1157/1158/1188 all publish it), and it
is the single statistic whose direction is the *opposite* of 1188's pooled premise. 1188's
0.5435-at-L2 is a six-statistic pool; the statistic the record actually quotes does not have the
effect. Any clause written from the pooled number would be written for the wrong statistic.

## THE C_PERM CONTROL, DECLARED UP FRONT, AND IT LANDS HARD
On a **21-day block-shuffled tape** — structure destroyed, marginal and short-run dependence
kept — the asymmetry **survives almost intact**: coarse>fine at **0.6049** of 81 books against
0.6173 on the real tape, median excursion 0.7262 / 0.6041, LSENS_SLIDE 2.2260 vs LSENS_COARSE
1.2346. **The coarse-end excursion is a property of the LADDER'S GEOMETRY and not of the
market.** A figure whose ladder sensitivity a permuted tape reproduces is not measuring a regime.

## GATES 17 OF 17, INCLUDING THREE BIT-FOR-BIT REPLAYS
G1 1188's committed premise from its own artefact (L2 0.543460 > L6 0.203326, L8 0.234815; dev
4.26e-07). G2 936's U56 anchor triple (6.04e-06). G3 the record's committed full-tape MAXDD on
all three panels (7.17e-06). **G4 1158's committed L8 R_COUNT reading of SMALL/MAXDD 1.173714 ->
1.173714 (2.59e-08). G5 1148's committed SMALL/MAXDD/R_MATCHED/F_1140 0.794259 -> 0.794259
(1.89e-07), replayed through 1188's recovered Monte-Carlo draw order.** G6 SPY OOS triple
(1.70e-04). G7/G7b/G7c the three analytic identities (0 / 0 / 1.78e-01). G8-G8e five structural
gates on the dial (all 0). G9 the L8 pivot (0). G10 the vintage pin. G11 determinism from
PARTVALS with no cache (0).

**H6 is a KNIFE EDGE, reported as one.** The median Spearman rho of the E_SLIDE excursion against
log(fmax) is **0.49999999999999994** against a declared bar of 0.50 — one float ulp below it. The
median of 486 discrete five-point rank correlations can only straddle that bar, never resolve it,
so it is scored KNIFE-EDGE and the raw double printed rather than called a refutation.

**A NON-REPRODUCTION, stated as one.** Lane B's 1158 run found ONE extra trading day moves a
committed ratio by up to 0.776 relative. On **this** object it does not: max **4.70e-14** over the
27 books whose tape differs at all (U56 only; the B136 and SMALL caches both end 2026-09-11). A
sub-tape MAXDD median is a running minimum and one bar appended at the end does not move it. Not
folded into the headline as agreement.

## CAPITAL — RULE 8 AND BOTH KEEP PATHS, 81 BOOKS AND 12 PICKS ALL PUBLISHED
Parameters on 2009-2016 only, 2017-2026 read once, 10 bps, next-day, weekly.

- **4a: 0 of 81 books and 0 of 12 picks.**
- 4b full AND OOS **15 of 81** (U56 10/27, B136 5/27, **SMALL 0/27**) — but those 15 rows are
  about **5 distinct selections**. U56/CADENCE=W, U56/GROSS=0.75, U56/H=126 and U56/N=20 return
  the **identical** series 15.58% / 1.139742 / -19.13% (they *are* 936's anchor book, reached four
  ways), and **U56 GROSS 0.55->0.75 is that one book de-grossed: Sharpe 1.139051 -> 1.139742, a
  spread of 6.9e-04 over a 1.36x change in gross.** B136's four GROSS passers are likewise one
  book. This independently reproduces **idea 1189's premise** (still open) from a third direction.
- **The direction the ladder is walked MOVES THE PICK at 3 of 3 panels**, and **H7 CAPITAL is
  SUPPORTED in the COARSE reading's favour**: mean OOS Sharpe CH_COARSE **0.8692** vs CH_FINE
  **0.6871** (gap 0.1821), CH_PUB 0.7373, CH_IS 0.8509. The two-rung "unresolved" reading picks
  *better* books than the seven-rung one — on SMALL, CH_FINE picks N=5 at OOS Sharpe 0.1972
  against CH_COARSE's 0.4387. **Resolution is not free and on this evidence it is not even
  positive**, which is the same direction 1174 found on the H axis (-0.0559).
- CH_COARSE's only 4b-OOS pass is U56/GROSS=0.50 — **the de-grossed incumbent**, Sharpe 1.1389,
  fails 4b full and fails 4a. Not a new candidate, per 1189's warning.

**VERDICT: KILL as a capital finding.** No memo (PROTOCOL rule 4: a KEEP needs 4a or 4b, and the
picks clear neither).

## WHAT THE RECORD SHOULD CARRY (PROPOSED, NOT ENACTED — rule 6)
A sub-tape claim must state **the coarsest rung its between term is taken over**, not only its
rung count: the endpoint carries 84% of the move and a half-tape contrast is near-degenerate. And
**a pooled-over-statistics ladder-sensitivity number must not be quoted for MAXDD**, which is the
one statistic here whose direction reverses.

## SURVIVORSHIP (rule 9)
U56 and B136 are current-constituent lists; SMALL is the current output of a sub-$2B screen
(715 listed, 52 dropped for `max_1d_move >= 1.0`, 663 + SPY served). Every LEVEL is optimistic
and every 4a/4b count is an UPPER bound. The run's object is a ratio of two spreads in the
statistic's own units and is far less exposed, but MAXDD is the lineage's headline and a
survivorship-flattered panel has a shallower drawdown path, so the levels are published beside
every ratio in `.walks.csv` and `.surface.csv`.
