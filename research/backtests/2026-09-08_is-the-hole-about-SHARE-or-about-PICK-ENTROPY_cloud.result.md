# Idea 438 — is-the-hole-about-SHARE-or-about-PICK-ENTROPY (cloud, 2026-09-08)

**ANSWERED. The record's x-axis is the right one. MODAL SHARE separates the +0.0076 region from
the zero region most cleanly of the three (cross-validated R²_LOO +0.1121 vs entropy +0.0803 vs
distinct-count +0.0625, and it is the argmax in 9 of 12 (h, m_min) cells) — but the margin is NOT
resolvable (SHARE − ENT +0.0318, 90% CI [−0.0390, +0.0996]). The queue's premise is TRUE as a
measurement and INERT as a mechanism: conditional on share, entropy adds +0.0014 of R² with 0
inside its CI. The one place entropy appears to win — the book — is a DIAL-EXPOSURE artefact,
which is idea 226's own lesson firing on the idea that came after it.**

Script: `2026-09-08_is-the-hole-about-SHARE-or-about-PICK-ENTROPY_cloud.py`.
Substrate: idea 219's committed `ladder.csv.gz` (36,120 rows) and `cells.csv` (560 cells), READ,
never re-simulated. Outputs: `.console.txt .cells.csv .curves.csv .loo.csv .params.csv
.conditional.csv .regions.csv .bydial.csv .book.csv .walkforward.csv .boot.csv`.

## The chain

**Q1 reproduction — the strongest gate the record has had.** All 560 cells were rebuilt *from the
ladder alone* — the seeded split-half design, the picks, the modal shares, the d's — and match the
committed `cells.csv` to **1.5e-16** across 11 columns with 0 modal-point mismatches; 219's 33
published curve rows come back with 0 cell-count errors and max |Δ mean_d| 5.0e-05. **P1 HIT.**
This matters more than a usual reproduction: entropy and the distinct count are computed on the
*same 80 half-samples* that produced `d`, so the three statistics are strictly comparable and no
part of the contrast can be a re-simulation artefact.

**Q2 the queue's premise, measured — TRUE.** Of 560 cells, 108 sit at modal share 0.30–0.42; there
the distinct-pick count spans **3.74 → 7.08** (rounded levels 4, 5, 6, 7) and entropy 1.76 → 2.52
bits. **P2 HIT** — share really does hide the shape. Inside that band the raw orderings are
positive (Spearman ENT–d +0.197, DIST–d +0.319 over 108 cells), which is exactly why the question
was worth asking. Note the six statistics are near-collinear by construction (|ρ(SHARE, ENT)| =
0.992), so this is a resolution question, not a new-variable question.

**Q4 separation, cross-validated — SHARE wins, un-separably.** R²_LOO = 1 − MSE(leave-one-cell-out
local mean) / MSE(leave-one-cell-out grand mean); a statistic that only wiggles scores ≤ 0.

| statistic | R²_LOO (h .075) | dial-FE | 90% CI on the gap vs SHARE | P(gap ≤ 0) |
|---|---|---|---|---|
| **SHARE** | **+0.1121** | **+0.1082** | — | — |
| ENTn | +0.0877 | +0.0761 | [−0.0609, +0.1054] | 0.344 |
| ENT_MM | +0.0831 | +0.0888 | [−0.0436, +0.0910] | 0.303 |
| ENT | +0.0803 | +0.0727 | [−0.0390, +0.0996] | 0.242 |
| DIST | +0.0625 | +0.0423 | [−0.0402, +0.1420] | 0.175 |
| DISTn | +0.0394 | +0.0188 | [−0.0502, +0.1879] | 0.162 |

Every statistic carries real signal (all six levels have P(R² ≤ 0) ≤ 0.009 over 112-block, 2000-draw
bootstrap), and every pairwise gap has 0 inside its CI. **P3 HIT** on the point estimate; the
honest statement is *SHARE ranks first in 9 of 12 (h, m_min) cells and no gap is resolvable*.

**Q6 the conditional test — the queue's mechanism is NULL.** Residualise d on SHARE's own
leave-one-out local curve, then ask whether the shape still orders the residual: entropy adds
**+0.0014** of R²_LOO (90% CI [−0.0183, +0.0517], P(≤0) = 0.280). **P4 HIT.** So "at share ~0.35,
does the mass sit on 2 arms or 9" is a real distinction that does not pay. The one direction worth
recording rather than claiming: `DISTn` on the share residual is +0.0243 with ρ +0.126 at every
half-window tested — reported as a direction, not a finding, because it was not bootstrapped and
it is not one of the three the queue named.

**Q7 the two regions under rule 8 — the readings disagree.** Refitting the best contiguous
interval on one corpus over 680 pre-stated (lo, hi) pairs and reading it once on the other:

| statistic | mean IS contrast | **mean held-out contrast** | transfer |
|---|---|---|---|
| ENT | +0.0117 | **+0.0042** | 0.42 |
| DIST | +0.0089 | +0.0041 | 0.49 |
| SHARE | +0.0111 | +0.0021 | 0.32 |

SHARE's A→B interval [0.875, 1.000] transfers (+0.0053) and its B→A interval [0.300, 0.400] does
not (−0.0012); entropy transfers in both directions. Two intervals per statistic is a sample of
two, so this reverses the Q4 ranking on evidence far thinner than the Q4 bootstrap.

**Q8/Q9 the book — and why its ranking is not a statistic result.** Each statistic run as a gate on
the committed ladder (threshold for each corpus chosen on the *other*; ladder IS = 2009–2016, OOS =
2017–2026 read once), paired against the do-nothing control SEL-SHARPE on OOS Sharpe:

| corpus | GATE-SHARE | GATE-ENT | GATE-DIST | MODE (always) |
|---|---|---|---|---|
| A | −0.0058 (t −6.68) | **+0.0037 (t +4.62)** | +0.0031 (t +4.00) | −0.0020 (t −1.62) |
| B | −0.0082 (t −11.20) | **+0.0023 (t +2.73)** | −0.0020 (t −2.18) | −0.0054 (t −5.69) |

**P5 MISS** — the entropy gate beats the control on both corpora. Q9 takes that apart. The
per-dial deltas are the *same for every gate*: writing the mode down is worth **+0.024 to +0.028 on
CADENCE** and **+0.018 on N** and costs **−0.028 to −0.069 on SLEEVE**, whatever statistic opened
the gate. The gates differ only in how much SLEEVE they admit. GATE-ENT on corpus A fires on 16 of
175 cells, 14 of them N — leave-one-dial-out on N takes its advantage to **exactly +0.00000**.
GATE-SHARE fires on 128 of 175 including 25 SLEEVE cells, and holding SLEEVE out flips it from
−0.0058 to **+0.0084**. So the book-level ranking of the six statistics is a ranking of dial
exposure wearing a statistic's name; Q4/Q5, which hold the cell set fixed and change only the
x-axis, are the reading that answers the queue. This is idea 226's finding (a pooled curve over
heterogeneous cells can be read wrong by composition) reappearing one idea later in a different
disguise.

**KEEP paths and references (PROTOCOL 3/4).** 4b passes by parent and rung, SEL-SHARPE vs the
gates: U56 180/162/144/126/114 → GATE-SHARE 190/167/147/114/97, GATE-ENT 208/183/162/119/106;
B136 129/102/60/46/40 → 144/106/54/42/36 and 129/99/63/49/39; **SMALL 0 at all five rungs for
every arm — P6 HIT** (idea 136, n+1). References at 10 bps: U56 window SPY 15.23%/0.889/−33.7%
(OOS 15.45%/0.882/−33.7%), RULES v2 8.66%/1.206/−12.1% (OOS 9.53%/1.285/−12.1%); SMALL window SPY
14.13%/0.862/−33.7%, RULES v2 3.80%/0.571/−14.7% (OOS 3.84%/0.566/−14.7%). **No book is
proposed and no KEEP is claimed** — every arm here is a re-selection over idea 219's committed
points (idea 144: a re-dialled book is the same book), and the 4b counts are that parent's own
rows, not new evidence.

## Verdict

**ANSWERED, and a KILL of the re-parameterisation.** Modal share stays the record's x-axis: it
separates best of the three, it is the argmax at 9 of 12 grid points, and the shape it discards is
measurably real but pays +0.0014 of R² with 0 in its CI. Nothing here licenses a PROTOCOL change,
a RULES change, or a book.

## Caveats

* **SURVIVORSHIP (idea 54):** U56, B136 and the small panel are current-constituent lists with no
  delistings. Every arm inherits it equally so the paired contrasts are unaffected; every LEVEL is
  biased upward and none is a tradable estimate.
* Cells are **not independent** — they share books (a k-group is a subset of ALL), share one 0-bps
  simulation across the five cost rungs, and 48 of corpus A's 53 books are B136 sub-panels. Every
  t is over correlated units; the bootstrap resamples whole (corpus, dial, group) blocks and no
  p-value here is a p-value on a fresh sample.
* **Entropy is biased downward** at 4–57 books per half and the bias grows with K (4 for CADENCE,
  11 for SLEEVE+). That confound is why the grid carries both a /log2(K) normalisation and a
  Miller–Madow correction; the ranking is unchanged by either (ENT_MM +0.0831, ENTn +0.0877).
* The distinct-pick count is an integer on 4–11 levels, so its local windows are coarse by
  construction; R²_LOO is the measure built to price that fairly, and it is what is reported.
* Corpora A and B are near-disjoint in books but not in parent panels (A carries 200 SMALL and 400
  U56 arm-rows), so Q7's "held out" is held out in books, not in panels.
