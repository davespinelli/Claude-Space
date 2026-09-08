# Idea 225 — back-fill-the-split-half-distribution-over-every-single-draw-claim (cloud, 2026-09-08)

**ANSWERED, and the back-fill is COMPLETE rather than sampled. The record contains exactly ONE
published family resting on a single seeded corpus split — idea 189's Q5, 10 verdicts — and of
those 10, exactly ONE moves: the A/N cell the queue already named. Its published −0.0229 sits at
the 6th percentile of its own 200-draw distribution, whose mean is +0.0064. The other 9 verdicts
are immovable, 8 of them with a split-to-split sd of 0.0000. So the practice the queue feared is
rare, not endemic — but where it bites it is worth +0.0149 of book-level OOS Sharpe (t +4.80),
because the single draw wrote down the wrong dial point (N=10 instead of N=20).**

Script: `2026-09-08_back-fill-the-split-half-distribution-over-every-single-draw-claim_cloud.py`.
Substrate: idea 189's committed `ladder.csv` (6,048 rows) and idea 219's `ladder.csv.gz` (36,120
rows), READ, never re-simulated. Outputs: `.console.txt .census.csv .backfill.csv .params.csv
.calibration.csv .book.csv .walkforward.csv`.

## The chain

**Q1 census — the practice is rare.** All 389 committed backtest scripts parsed (0 failures);
**109 seeded partition calls in 74 scripts**, 29 repeated at their call site and 80 single-draw.
Adjudicated into families, the single-draw hits are overwhelmingly *not* corpus splits: 36
sub-panel draws (corpus construction), 13 dropout resamples, 7 rotation/offset nulls, 4 null
instruments, 1 label permutation, 16 printed individually as unadjudicated — and **3 with the
corpus split-half signature**, of which two partition *blocks of a return series* inside a
flip-rate estimator and publish no split-half verdict. That leaves **one published family**: idea
189's Q5, 2 corpora × 5 dials at seed 189500. **P2 HIT.** The classifier is a stated syntactic
heuristic and every hit is printed with its family, so both error directions are auditable rather
than asserted.

**Q2 reproduction.** All 10 published verdicts rebuilt from idea 189's committed ladder alone —
modes, agreement flags, and d — with **max |Δ| 4.3e-05** against the printed 4-dp console and **0**
mode or agreement mismatches. **P1 HIT.**

**Q3 the back-fill — 1 of 10 moves.** At S = 200 (seed 189500, stream re-drawn):

| corpus/dial | published | S-mean | S-sd | pctile | sign moves |
|---|---|---|---|---|---|
| **A / N** | **−0.0229** | **+0.0064** | **0.0187** | **0.06** | **YES** |
| B / N | +0.0256 | +0.0201 | 0.0202 | 0.25 | no |
| A/GROSS, A/BAND, A/CADENCE, A/SLEEVE, B/GROSS, B/BAND, B/CADENCE, B/SLEEVE | — | = published | **0.0000** | — | no |

**P3 MISS** (2 predicted, 1 delivered) and **P4 MISS** (mode-agreement moved in 0 of 10, so it is
*more* stable than sign, not less). Eight of ten cells are completely insensitive to the split —
the mode is the same on every one of 400 half-samples. The one that moves, moves decisively:
idea 219's finding, reproduced here from a different substrate and a different estimator.
Note the housekeeping that matters: signs are compared on the full-precision reproduced value,
never on the printed `−0.0000`, and a cell where every draw agrees to 1e-6 (A/SLEEVE) is marked
DEGENERATE so a zero-vs-zero flip is never counted as a moved verdict.

**Q4 the general number PROTOCOL should quote.** Idea 219's 560 cells × 80 seeded splits = 44,800
single draws, re-derived exactly: **a single seeded split disagrees in sign with its own settled
many-draw answer 20.5% of the time** (median 18.8% of cells above 0.40 — a near coin flip in 105
of 560 cells), and **mean |single draw − many-draw mean| = 0.0130, which is 1.15× the mean size of
the effect itself (0.0113)**. **P5 HIT.** The rate is a clean function of how far the effect sits
from zero:

| \|mean\| / sd of draws | cells | P(sign disagree) |
|---|---|---|
| < 0.25 | 168 | 0.178 |
| 0.25–0.5 | 61 | 0.335 |
| 0.5–1 | 161 | 0.291 |
| 1–2 | 115 | 0.148 |
| > 2 | 55 | **0.009** |

So a single split is safe exactly where it is not needed (|mean|/sd > 2) and unreliable in the
band the record actually publishes in.

**Q5 the two tuned parameters (S × verdict rule, 9 points).** The count is **1 / 1 / 0** at S = 40,
200 and 1000 alike; mean sd 0.0045 → 0.0039 → 0.0038. The distribution is settled by S = 40, so
the answer is not an artefact of how many splits were run.

**Q6 consequence — the sampling fix is worth something, once.** The S-draw mode differs from the
published single-draw mode in 1 of 10 cells (A/N: 10 → 20), and **S-MODE is identical to FULL-MODE
in all 10** — reading the mode off many splits converges on reading it off the whole corpus, which
is the cheaper instruction. Priced per book on the committed ladder with rule-8 picks (IS ≤
2016-12-31, OOS 2017–2026 read once, 10 bps), paired against the do-nothing control SEL-SHARPE:

| corpus | SINGLE-MODE | S-MODE | **S-MODE − SINGLE-MODE** |
|---|---|---|---|
| A | −0.0053 (t −1.31) | +0.0096 (t +2.72) | **+0.0149 (t +4.80), 53 rows differ** |
| B | +0.0124 (t +4.49) | +0.0124 (t +4.49) | **+0.0000, 0 rows differ** |

The whole A-side gap is the N dial, where the single draw's N=10 is worth −0.0530 and the settled
N=20 is worth +0.0215 — a **+0.0745** swing on that dial. Per idea 226/438's standing check, the
S-MODE advantage over the control survives leave-one-dial-out on corpus A (LODO range +0.0055 to
+0.0120, no dial's removal kills or flips it), so unlike idea 438's gate this is not a
dial-exposure artefact. **P6 MISS** — but the miss is about idea 189's own mode-vs-selector
question, which S-MODE ≡ FULL-MODE simply reproduces; this idea's own quantity is the
SINGLE-vs-S contrast above.

Arm levels (means over book × dial rows) and references at 10 bps: corpus A S-MODE 10.60%/1.020/
−17.8% (OOS 10.81%/1.020/−17.8%) vs SEL-SHARPE 10.80%/1.019/−18.2% (OOS 10.90%/1.010/−18.2%) vs
SINGLE-MODE 10.96%/1.008/−18.4% (OOS 11.15%/1.005/−18.4%); corpus B all three modes
5.64%/0.708/−17.9% (OOS 6.06%/0.738/−17.8%) vs SEL-SHARPE 5.54%/0.706/−18.2% (OOS
5.80%/0.725/−18.1%). U56 window SPY 15.23%/0.889/−33.7% (OOS 15.45%/0.882/−33.7%), RULES v2
8.66%/1.206/−12.1% (OOS 9.53%/1.285/−12.1%); SMALL window SPY 14.13%/0.862/−33.7%, RULES v2
3.80%/0.571/−14.7% (OOS 3.84%/0.566/−14.7%). **KEEP paths** (point-level verdicts inherited from
the parent's committed ladder, zero new evidence): B136 4a 176→192, 4b 36→37; U56 4a 179→164, 4b
58→65; **SMALL 4b 0 for every arm**. No book is proposed and no KEEP is claimed (idea 144).

## Verdict

**ANSWERED. The queue's worry is real, localised and now fully back-filled.** One published family,
one moved verdict, and a general calibration number — 20.5%, rising to ~33% where |mean|/sd sits
between 0.25 and 0.5 — that any future single-draw split claim can be read against. The natural
follow-on is a PROTOCOL footnote, not a clause: where a verdict is read off a seeded corpus split,
quote it off the whole corpus (which S-MODE ≡ FULL-MODE shows is the same answer for free), or
report the split-to-split sd beside it. **Nothing here licenses a RULES change or a book.**

## Caveats

* The census **classifier is a syntactic heuristic**, not a proof: a loop counts as a repetition
  loop iff none of its targets is referenced in its body, and a partition inherits repetition from
  an enclosing repetition loop or a function called inside one. It therefore misses a repetition
  expressed as a `while`, as a seed list consumed by an outer driver, or behind a helper module,
  and over-counts a per-unit draw that legitimately happens once per unit. Every hit is printed
  with its source line and adjudicated family so both directions are visible.
* The census covers **committed `research/backtests/*.py` only**. A claim published in a memo whose
  script was never committed cannot be found by any parser; so is anything in the local
  (options / EDGAR / Form 4) lane.
* Idea 189's two corpora **share one RNG stream** (A's permutation is drawn first), so the published
  draw is one point in a 2-dimensional seed space. The back-fill re-draws both, which is the right
  distribution but not the marginal of the published procedure conditioned on A.
* **SURVIVORSHIP (idea 54):** U56, B136 and the small panel are current-constituent lists with no
  delistings. Every arm inherits it equally so the paired contrasts are unaffected; every LEVEL is
  biased upward and none is a tradable estimate.
* Cells and books are not independent (books are shared across dials and groups); no t here is a
  t on a fresh sample.
* Idea 144: a re-dialled book is the same book. Nothing here is a new signal.
