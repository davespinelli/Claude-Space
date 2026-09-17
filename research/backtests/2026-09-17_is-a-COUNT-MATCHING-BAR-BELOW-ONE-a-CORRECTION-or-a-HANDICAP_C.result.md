# Idea 1214 (lane C, 2026-09-17) — is a COUNT-MATCHING BAR BELOW ONE a CORRECTION or a HANDICAP?

**VERDICT: KILL (capital). ANSWERED = NEITHER — it is a NO-OP, and the point bar it belongs to
is MISCALIBRATED in both directions.** 17 of 17 gates pass. Runtime 29s, offline, deterministic.

Script: `2026-09-17_is-a-COUNT-MATCHING-BAR-BELOW-ONE-a-CORRECTION-or-a-HANDICAP_C.py`
Dials (2, PROTOCOL rule 4): **BAR FORM** {B_RAW, B_POINT, B_MED, B_IID90, B_IID95, B_BOOT95} x
**LADDER SET** {ALL4, NG}. 12 cells, every one published in `.grid.csv`. Nothing selected on.

---

## 1. The queue's premise has the wrong sign, and it is arithmetic, not a measurement

A pair is written in its realised direction, so `M = R_wide / R_narrow >= 1` **by construction**.
`I = d2(k_wide)/d2(k_narrow) < 1` happens exactly when the wider-spread ladder is the SHORTER one.
`M > 1 > I` then holds for every such pair: **the bar cannot bind, ever.**

- On 1207's committed pairs table, **134 of 252 pairs (0.5317) carry a bar below 1 and 134 of 134
  of them SURVIVE it (1.0000)** — gate G2.
- So the below-one bar does not penalise the shorter ladder. It hands it a **free pass**. The
  exposure the record carries is **false confirmation**, not a handicap. 1207's own line — "the
  count difference runs AGAINST the conclusion more often than for it" — is the same fact read
  from the other side, and it is the half of the census where 1155's repair does nothing at all.
- `R_k/d2(k)` is unbiased for sigma at every rung count (max |E[R_k/d2(k)] - 1| = 8.6e-04, G1), so
  1155's point correction is correctly CENTRED **in expectation**. The defect is not bias.

## 2. What the correct two-sided bar is (derived, then walked)

The record's habit ORIENTS the pair on the data — it calls the raw-wider ladder the wider dial —
so the null that governs the call is the distribution of `V = M/I` **conditional on that
orientation**. Conditioned, `V` is not centred at 1 at all: at (k_w=2, k_n=10) its null median is
**3.2685**, so a 3x raw multiple is the *typical* outcome under equal dispersion. Where
`k_w < k_n`, `V > 1` with probability one and the point bar **can never reverse**, however thin
the margin. The correct bar is the conditional two-sided band `[L, U]` (`.bands.csv`): outside
`U` the wider dial is real, outside `L` the call REVERSES onto the longer ladder, in between
there is **no call at all**. False-call rates under H0, by construction of each bar:

| bar form | P(names a widest dial) | P(names the WRONG one) |
|---|---|---|
| B_RAW | 1.0000 | 0.0000 (it has no wrong — it never corrects) |
| B_POINT | 1.0000 | **0.2573** |
| B_MED | 1.0000 | **0.5000** (a coin flip by construction) |
| B_IID90 | 0.1000 | 0.0500 |
| B_IID95 | 0.0500 | 0.0250 |

(Pooled over the 12 ordered (k_w, k_n) cells, weighted by how often each orientation is realised
under the null.) A point bar names a dial at **every** pair — 0.2573 to 0.5000 of them wrongly.
Only a band delivers the error rate the author chose. That is the whole of the repair.

## 3. The 252 pairs, re-read (ALL GRID POINTS)

| ladder set | bar form | pairs | W | N (reversed) | TIE | reversal | tie |
|---|---|---|---|---|---|---|---|
| ALL4 | B_RAW | 252 | 252 | 0 | 0 | 0.0000 | 0.0000 |
| ALL4 | B_POINT | 252 | 225 | 27 | 0 | 0.1071 | 0.0000 |
| ALL4 | B_MED | 252 | 197 | 55 | 0 | 0.2183 | 0.0000 |
| ALL4 | B_IID90 | 252 | 127 | 5 | 120 | 0.0198 | 0.4762 |
| ALL4 | B_IID95 | 252 | 126 | 5 | 121 | 0.0198 | 0.4802 |
| ALL4 | B_BOOT95 | 252 | 108 | 0 | 144 | 0.0000 | 0.5714 |
| NG | B_RAW | 126 | 126 | 0 | 0 | 0.0000 | 0.0000 |
| NG | B_POINT | 126 | 99 | 27 | 0 | 0.2143 | 0.0000 |
| NG | B_MED | 126 | 71 | 55 | 0 | 0.4365 | 0.0000 |
| NG | B_IID90 | 126 | 1 | 5 | 120 | 0.0397 | 0.9524 |
| NG | B_IID95 | 126 | 0 | 5 | 121 | 0.0397 | 0.9603 |
| NG | B_BOOT95 | 126 | 3 | 0 | 123 | 0.0000 | 0.9762 |

**Every decisive call at ALL4 is a GROSS pair.** 126 of the 252 pairs put a real dial against
GROSS, whose Sharpe spread is degenerate (1189, reproduced by 1206 and again here: IS GROSS
spread 0.0011 / 0.0034 / 0.0023 against N's 0.0465 / 0.1777 / 0.2552), and all 126 clear the band
trivially. Strike GROSS and **the calibrated bar names the raw-wider ladder at 0 of 126 pairs**;
its only 5 calls are REVERSALS, all at `M` between 1.004 and 1.052 — knife-edge ties — and
B_BOOT95, which carries the real cross-ladder dependence, declines all 5. The record's
widest-dial habit among its non-degenerate dials is **unresolved, not merely uncorrected**.

Pre-declared outcomes were (A) CORRECTION if decisive at >= 0.80, (B) HANDICAP if reversals
>= 0.10, (C) UNRESOLVED if TIE >= 0.50. The headline cell (ALL4 x B_IID95) lands at TIE 0.4802,
**five pairs short of (C)**, and only because the degenerate GROSS pairs are counted. Reported as
(A) by the pre-declared rule; read honestly it is (C) everywhere the answer could matter.

## 4. Committed widest-dial calls in the record's own text

352 committed units make a widest/narrower call and adjudicate on it. **17 are checkable** (quote
a multiple AND two counts); **6 are in d2's domain** (0.3529) — 1207's domain split again. Those
6 are the units 1207 hand-read as genuine range-vs-range pairs, re-read here under the band
(counts assigned by the record's own `I = d2(k_max)/d2(k_min)` convention):

| uid | k_w/k_n | M | I | V | null med | band95 | B_POINT | B_IID95 |
|---|---|---|---|---|---|---|---|---|
| d1e45a7a60 | 9/7 | 39.0000 | 1.0982 | 35.5114 | 1.2605 | [0.925, 2.715] | W | **W** |
| ca229253f8 | 9/2 | 2.3900 | 2.6321 | 0.9080 | 1.2596 | [0.419, 27.377] | N | TIE |
| 05d6fd1eb4 | 12/3 | 0.4100 | 1.9252 | 0.2130 | 1.1373 | [0.551, 6.042] | N | **N** |
| a5001741b0 | 12/4 | 1.4426 | 1.5827 | 0.9115 | 1.1361 | [0.657, 3.858] | N | TIE |
| b374f7d5cf | 9/4 | 1.5000 | 1.4426 | 1.0398 | 1.1904 | [0.715, 4.026] | W | TIE |
| 97f64224ae | 9/2 | 1.0800 | 2.6321 | 0.4103 | 1.2596 | [0.419, 27.377] | N | **N** |

**The two-sided bar REVERSES 2 of 6 committed widest-dial calls and declines to adjudicate 3.**
Both reversals (05d6fd1eb4, 97f64224ae) STRENGTHEN their committed verdicts — 1207 hand-read both
as already running against the author — so **no committed verdict changes**, consistent with
1207's ANSWERED = NONE. Only d1e45a7a60's "39x" survives a calibrated reading. One of six.

## 5. Price leg — rule 8, both KEEP paths, nothing promoted

Each bar form made deployable: name a dial on the IS window, or hold the anchor.
588 pick-cells = 3 panels x 14 folds x 14 choosers (42 picks each). **ALL4 and NG produce
identical picks at every cell** — GROSS is always the narrowest ladder, so dropping it never
moves an argmax. The ladder-set dial is inert on the price leg and is reported, not relied on.

Move rates: RAW 1.000, POINT 0.905, MED 0.881, IID90/IID95 0.048, **BOOT95 0.000**. The bootstrap
band never separates the winner from the runner-up on any of the 42 IS windows, so **CH_BOOT95 is
CH_ANCHOR, exactly**. Mean OOS Sharpe over 42 picks, paired delta vs CH_RAW, SE clustered on the
14 folds:

| chooser | mean OOS Sharpe | delta vs CH_RAW | SE | t |
|---|---|---|---|---|
| CH_RAW | 0.9677 | — | — | — |
| CH_POINT | 0.9959 | +0.0281 | 0.0494 | +0.57 |
| CH_MED | 0.9875 | +0.0198 | 0.0461 | +0.43 |
| CH_IID90 / CH_IID95 | 1.0179 | +0.0501 | 0.0541 | +0.93 |
| CH_BOOT95 / CH_ANCHOR | 1.0362 | +0.0685 | 0.0514 | +1.33 |

Calibrating the bar orders the choosers correctly — the more honest the bar, the better the OOS
Sharpe — and the ordering terminates at **doing nothing**. The gain is +0.0685 at **t = +1.33**:
not resolved on 14 folds, and reported as unresolved.

**RULE 8** (dials on warm-up..2016-12-31, 2017-2026 read once). At all three panels the band
returns TIE, so every band chooser holds the anchor:

| panel | chooser | full CAGR / Sharpe / MaxDD | halves | OOS CAGR / Sharpe / MaxDD | 4a | 4b | 4b OOS |
|---|---|---|---|---|---|---|---|
| U56 | CH_RAW (N=40) | 13.40% / 1.1311 / -22.46% | 1.2663/1.0361 | 14.08% / 1.1150 / -22.46% | F | F | F |
| U56 | CH_POINT, CH_MED (N=40) | 13.40% / 1.1311 / -22.46% | 1.2663/1.0361 | 14.08% / 1.1150 / -22.46% | F | F | F |
| U56 | CH_IID90/95, CH_BOOT95, CH_ANCHOR | 15.71% / 1.1480 / -19.13% | 1.2127/1.1050 | **17.16% / 1.1759 / -19.13%** | F | **T** | **T** |
| B136 | CH_RAW/POINT/MED (N=5) | 18.73% / 0.9690 / -28.12% | 1.3074/0.7109 | 14.71% / 0.7546 / -28.12% | F | F | F |
| B136 | band choosers, CH_ANCHOR | 16.18% / 1.0715 / -20.74% | 1.2902/0.8995 | 16.29% / 1.0240 / -20.74% | F | F | F |
| SMALL | CH_RAW/POINT/MED (H=252) | 13.36% / 0.7845 / -37.41% | 0.9555/0.6419 | 11.16% / 0.6677 / -37.41% | F | F | F |
| SMALL | band choosers, CH_ANCHOR | 7.84% / 0.5055 / -35.81% | 0.6594/0.3942 | 7.09% / 0.4534 / -35.81% | F | F | F |

Benchmarks: U56 SPY 15.06% / 0.8815 / -33.72% (halves 0.9600/0.8171), OOS 15.15% / 0.8686;
U56 LIVE (RULES v2) 8.60% / 1.1982 / -12.05%, OOS 9.42% / 1.2717. B136 SPY 15.16% / 0.8862,
OOS 15.33% / 0.8769; B136 LIVE 7.98% / 1.0994, OOS 7.88% / 1.1061. SMALL SPY 14.06% / 0.8582,
OOS 15.33% / 0.8769; SMALL LIVE 4.64% / 0.7130, OOS 4.47% / 0.6518.

**BOTH KEEP PATHS.** 66 rung books: **4a 0 of 66**, 4b full 17 (U56 10, B136 7, SMALL 0), 4b OOS
16, BOTH 15. 42 stitched chooser curves: 4a 0, 4b full 12, 4b OOS 8, BOTH 8. 42 rule-8 picks:
4a 0, 4b full 8, 4b OOS 8, BOTH 8.

**NOT PROMOTED, NO MEMO, NO RULES CHANGE.** Every one of the 8 passing rule-8 rows and 8 passing
stitched rows is the **anchor book** (U56, N=20/H=126/gross 0.75, weekly) reached by a chooser
that declined to move — the already-committed U56 CAND20 weekly g=0.75 book the record confirmed
on 2026-09-15 and 1206/1207 declined to promote. Counted under 1194's gross-free key it is one
book, not eight. This run produces **no new book**.

## 6. Survivorship (rule 9)

B136 and SMALL are CURRENT constituents. SMALL is the sub-$2B screen, 664 investable of 715 after
dropping every ticker with max_1d_move >= 1.0, and starts 2010. U56 is the committed cache.

## 7. Gates (17 of 17)

G0 MC d2(k) == published Hartley constants 9.66e-04 · G1 R_k/d2(k) unbiased 8.56e-04 ·
G2 every below-one bar is a NO-OP on 1207's committed pairs 1.0000 (134/134) ·
G3 bands nest L95<=L90<=median<=U90<=U95 at all 12 (k_w,k_n) · G4 fast runner == engine.backtest
2.78e-17 · G5 gross-scaling identity 0.0 · G6 live U56 MaxDD -12.0549% == committed -12.05% ·
G7 block-sum bootstrap == direct Sharpe on the identity tiling 4.44e-15 · G8 folds tile all three
panels with no overlap and no gap · G9 the 252 pairs replay 1207's committed table bit for bit
(max |dMULTIPLE| 4.55e-13 over 252 matched rows) · G10 B_RAW names the raw-wider ladder at every
pair · G11 CH_ANCHOR move rate 0 · G12 stitched lengths == sums of folds ·
G13 1207's 6 hand-read A_PAIR units all still in the live corpus · G14 null bands deterministic
across two independent constructions (0.0).

## 8. What this leaves for the queue

The bar is not the object worth repairing; the **habit** is. On the record's non-degenerate
dials a widest-dial call is unresolvable on this tape at any honest error rate, and the
deployable form of the honest bar is the anchor. Three follow-ups are filed, all price-only.
