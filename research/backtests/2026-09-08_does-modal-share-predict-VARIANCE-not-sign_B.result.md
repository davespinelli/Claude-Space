# Idea 224 — does-modal-share-predict-VARIANCE-not-sign (lane B, 2026-09-08)

**SPLIT: the queue's PREMISE is CONFIRMED and its PROPOSAL is KILLED. Modal share prices the
VARIANCE of a mode's held-out value (Spearman −0.804) exactly where idea 219 showed it does not
price the SIGN (−0.046) — but calibrated honestly under rule 8, a share-scaled CONFIDENCE
interval covers no better than a FLAT constant at 15x the width, and the ranking it does deliver
is delivered better by a column the record already computes: the cell's DISTINCT pick count. No
RULES change, no book promoted, no KEEP on either path; RULES.md, scan.py, bot.py and baseline.py
untouched.**

Script `2026-09-08_does-modal-share-predict-VARIANCE-not-sign_B.py`; artefacts `.console.txt`,
`.cells.csv`, `.curve.csv`, `.decomp.csv`, `.fit.csv`, `.calib.csv`, `.kstar.csv`,
`.walkforward.csv`, `.keep.csv`. 6 s, no new simulation except the RULES v2 / SPY anchor.

## Q1 — the gate, passed before any new number was read

No re-simulation. Idea 219's committed `ladder.csv.gz` (36 120 rows = 168 books × 43 dial points
× 5 rungs) is the input, and the gate is that this run rebuilds 219's **cells.csv 560/560 rows**
and its **sweep.csv 132/132 rows** from that ladder alone, using 219's own `groups_of`, its
`SPLIT_SEED = 219500` and its crc32-of-the-cell-key seeding: **max |d| 3.553e-15 over 19 shared
columns, 0 `full_mode` mismatches.** The 560 cells reasoned over below are bit-for-bit the 560
the record published, and 219's own reproduction of ideas 189/217 is inherited, not re-paid for.

## Q2 — the curve the parent's verdict never spoke to

sd(d) over each cell's 80 seeded half-split draws, by share decile (m_min = 12, all 560 cells;
m_min 8 is identical because no group is smaller than 16, which is reported, not hidden):

| decile | share | cells | mean d | sd(d) | sd FIXED-mode | switch rate | n_books | points |
|---|---|---|---|---|---|---|---|---|
| 1 | 28.0% | 56 | +0.0049 | 0.0454 | 0.0151 | 41.9% | 57.1 | 8.23 |
| 2 | 36.4% | 56 | −0.0089 | 0.0403 | 0.0154 | 41.6% | 25.6 | 5.98 |
| 3 | 42.4% | 56 | +0.0053 | 0.0253 | 0.0113 | 31.8% | 24.4 | 5.29 |
| 4 | 51.6% | 56 | +0.0085 | 0.0131 | 0.0073 | 20.9% | 21.7 | 4.36 |
| 5 | 65.2% | 57 | +0.0250 | 0.0233 | 0.0139 | 6.2% | 25.8 | 3.54 |
| 6 | 78.3% | 56 | +0.0080 | 0.0069 | 0.0066 | 0.2% | 24.7 | 3.00 |
| 7 | 86.6% | 55 | +0.0100 | 0.0061 | 0.0061 | 0.0% | 54.6 | 3.27 |
| 8 | 93.9% | 60 | +0.0020 | 0.0030 | 0.0030 | 0.0% | 28.1 | 2.35 |
| 9 | 99.7% | 108 | +0.0003 | 0.0003 | 0.0003 | 0.0% | 21.6 | 1.08 |

**Spearman(share, sd(d)) = −0.804** against **−0.046** on the signed mean (219's KILL) and −0.641
on |mean|. It is not the n axis: −0.853 / −0.699 / −0.820 in the three n_books terciles, and the
highest-sd decile is also the LARGEST-n one (57.1 books). It is not one dial and not one rung:
negative in all 7 dial views (−0.251 BAND+ … −0.963 SLEEVE) and all 5 rungs (−0.766 … −0.839).

## Q3 — what share is actually pricing (P3 SPLIT)

A FIXED-MODE control re-scores every draw with the full-cell mode, so only the held-out **sample**
moves; `var_switch = var_total − var_fixed`.

| decile | share | sd total | sd FIXED | sd SWITCH | var from switch | switch rate |
|---|---|---|---|---|---|---|
| 1 | 28.0% | 0.0606 | 0.0176 | 0.0579 | **91.5%** | 41.9% |
| 3 | 42.4% | 0.0322 | 0.0143 | 0.0289 | 80.2% | 31.8% |
| 4 | 51.6% | 0.0164 | 0.0092 | 0.0136 | 68.8% | 20.9% |
| 6 | 78.3% | 0.0100 | 0.0095 | 0.0033 | 10.6% | 0.2% |
| 7–9 | ≥86.6% | 0.0081→0.0016 | 0.0081→0.0016 | 0.0000 | **0.0%** | 0.0% |

The mode-switch term carries the low-share end (92% of the variance in decile 1) and is **exactly
zero above share ≈ 0.78**. But the FIXED-MODE control is **not flat** (Spearman −0.711): at high
share the mode equals nearly every book's own pick, so the sample term collapses too. P3 is
therefore SPLIT — share prices a real mechanism, but the mechanism it prices has already
disappeared where the record's published cells overwhelmingly sit.

## Q4 — the fit, and the column that beats it

log(sd + 1e−6), m_min = 12, n = 560. Every model reported, none selected:

| model | R² | b_share | b_log n | b_log points |
|---|---|---|---|---|
| const | 0.000 | — | — | — |
| share | 0.550 | −10.930 | — | — |
| log n | 0.012 | — | +0.678 | — |
| **distinct** | **0.637** | — | — | +4.460 |
| share + log n | 0.550 | −10.929 | +0.002 | — |
| share + log n + distinct | 0.671 | **−0.944** | −1.157 | +4.505 |

**`distinct` — the number of ladder points receiving any book's vote — beats share on its own
(0.637 vs 0.550) and absorbs it: share's log-sd slope collapses from −10.93 to −0.94.** Out of
sample, CTRL-ONLY (no share at all) matches SHARE+CTRL on every split's log-sd R² to within 0.004.

## Q5 — rule 8 on the column itself, and where it dies

The column is a fitted object, so it is fitted on one part of the cell corpus and read on another,
and **k is chosen on the training cells** (smallest of 18 grid points reaching 90% coverage there)
and read once on the held-out cells. The published quantity is one seeded draw (idea 225: 20.5% of
single draws disagree in sign with the settled answer), so the test is whether `d₁ ± k·sd_hat`
covers the cell's settled value.

*Ranking — share wins decisively:* OOS log-sd R² **+0.517 / +0.592 / +0.539 / +0.234** on the four
splits against **−0.025 / −0.022 / −0.000 / −1.866** for a constant, with ρ(sd_hat, |error|)
**+0.70 … +0.83**.

*Interval — share loses outright:*

| split | model | k (train) | test coverage | test width | vs CONST |
|---|---|---|---|---|---|
| A → B | CONST | 40 | 89.6% | 0.0715 | 1.00x |
| A → B | **SHARE** | 25 | **88.8%** | 1.0742 | **15.01x** |
| B → A | CONST | 25 | 93.1% | 0.0804 | 1.00x |
| B → A | SHARE | 25 | 94.3% | 0.9631 | 11.98x |
| 10 bps → 5/15/20/25 | CONST | 40 | 94.6% | 0.1070 | 1.00x |
| 10 bps → 5/15/20/25 | SHARE | 25 | 89.1% | 0.9215 | 8.61x |
| published → BAND+/SLEEVE+ | CONST | 60 | 94.4% | 0.0776 | 1.00x |
| published → BAND+/SLEEVE+ | SHARE | 40 | 100.0% | 4.1354 | 53.32x |

Block bootstrap over 2000 resamples of whole (corpus, dial, group) blocks of the held-out cells,
A → B: SHARE coverage median **88.8% [84.2%, 93.2%]**, width ratio median **14.85x [9.75x,
20.65x]**. The k-free read says why: z = |draw − settled| / sd_hat has median 0.83 for SHARE vs
4.69 for CONST (share is on the right scale for the typical cell) but p90/median **38.6 vs 8.7** —
where share says "confident", sd_hat → 0 while the sample-term error does not, so buying the tail
costs everyone else an interval an order of magnitude too wide.

## Q6 — rule 8 on the books, and both KEEP paths

Picks on IS ≤ 2016-12-31, OOS ≥ 2017-01-01 read once; 112 cells × 3416 book-picks per rung.

| rung | arm | OOS Sharpe | OOS CAGR | OOS MaxDD | 4a pass | 4b pass |
|---|---|---|---|---|---|---|
| 10 | MODE | 0.8589 | 7.33% | −16.78% | 1625 | 380 |
| 10 | FIT | 0.8522 | 7.21% | −16.65% | 1639 | 360 |
| 10 | **SHRUNK** (the column as a decision) | **0.8199** | 7.55% | −17.87% | 1378 | 342 |
| 10 | INCUMBENT | 0.7649 | 7.15% | −18.17% | 1428 | 375 |
| 10 | ORACLE | 0.8966 | 6.81% | −14.61% | 1905 | 313 |

**SHRUNK − MODE = −0.0331 / −0.0390 / −0.0393 / −0.0422 / −0.0380 at 5/10/15/20/25 bps
(t −4.03 … −4.53; only 6–7% of cells improve).** Used as a decision the column destroys value at
every rung — P5 confirmed, and consistent with 219's KILL of the gate.

Anchor over the same OOS window, 10 bps weekly, on `baseline.load_universe()`:
**RULES v2 (live) 9.53% / 1.29 / −12.05%; SPY 15.45% / 0.88 / −33.72%; the MODE arm 7.33% / 0.86 /
−16.78%** (mean over 112 cells' books). Per idea 144 no arm here is a new book — every one is a
re-dial of books already in the record — so **neither KEEP path can be claimed by this run**
whatever the counts say; they are reported because PROTOCOL rule 4 asks for them.

## Verdict and what the record should do

**KILL** as a PROTOCOL clause and as a published interval. The premise survives and is worth
recording: share is informative about the SPREAD, not the sign, and that is a genuinely new
reading of 219's own data. But (i) the interval fails calibration by an order of magnitude, (ii)
the mechanism it prices is dead above share ≈ 0.78 where the published cells live, and (iii) even
the ranking belongs to `distinct`, not to share. If the record ever wants a confidence flag beside
a published mode, the cheap honest version is the DISTINCT PICK COUNT plus a FLAT width — not a
share-scaled interval.

## Honest limits

Cells are not independent (shared books, shared simulations across rungs, shared parents); every t
and CI is over correlated units and optimistic, and the block bootstrap only blunts it. sd(d) is a
resampling sd over 80 correlated half-splits of one finite corpus — it measures how far a
published number could have moved under a different split, and nothing more. At share = 1.00 the
mode cannot move, so sd there is a pure sample term. Survivorship: idea 175's SMALL panel and idea
171's U56/B136 are current constituents. A design correction is disclosed in the script header:
the first Q5 pass capped k at 10 and read k off the test cells; both were fixed (grid to 100, k
chosen on train only) and a k-free statistic added before the verdict was read. Q2/Q3/Q4 were
unaffected.
