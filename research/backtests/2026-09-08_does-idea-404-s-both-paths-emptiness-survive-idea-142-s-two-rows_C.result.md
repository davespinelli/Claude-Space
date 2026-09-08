# Idea 413 — does idea 404's both-paths emptiness survive idea 142's two rows?

**Lane C, 2026-09-08. Verdict: ANSWERED / SPLIT.  The emptiness is NOT a comparand artefact
(it reproduces exactly) but IS a corpus-coverage artefact.  PROTOCOL 4 must NOT be told the
paths are exclusive — but the joint pass is one coordinate wide and dies under rule 8.**

Script: `2026-09-08_does-idea-404-s-both-paths-emptiness-survive-idea-142-s-two-rows_C.py`
Files: `.console.txt` `.rescore.csv` `.coverage.csv` `.grid.csv` (288 rows) `.bothpaths.csv`
`.walkforward.csv` `.bothpaths_oos.csv`

## The question
Idea 142 reports 2 of 816 rows clearing 4a-vs-RULES-v2 **and** 4b together; ideas 135 / 138 /
402 report 0 of 1,632 / 0 of 208 / 0 of 1,728.  Idea 404 read the zeros as a **structural
exclusion** (4a's DD bar caps gross from above, 4b's CAGR floor from below) and the queue
proposed writing "the paths are exclusive" into PROTOCOL 4.  Three candidate explanations —
comparand, corpus, or a real exclusion — separated below.

## A — the comparand is exonerated (no new simulation; published columns)
| corpus | rows | both-paths, 4a vs **cost-matched RULES v2** (idea 142's) | both-paths, 4a vs V1 @ fixed 10 bps (idea 398's defect) |
|---|---|---|---|
| 135 | 1,632 | **0** | 39 |
| 138 | 208 | **0** | 20 |
| 402 | 1,728 | **0** | 76 |
| 142 | 816 | **2** | 31 |

Re-scored under idea 142's own comparand the three corpora reproduce their published zeros
**exactly**.  The older comparand is the *looser* one, so the defect idea 398 named can only
make 4a harder on re-score — it can never open an empty corpus.  Comparand ruled out.

## B — the coordinate is not in any of the three corpora
Read out of the committed constructors, not asserted:
* idea 142/133 `S3-50` = 0.50 x **R20** + 0.50 x **S3**, gate on **both** legs, blend
  **rescaled back to gross 0.75** after the gate (family **C133**).
* idea 135 `SLV50` = 0.50 x **EWall** + 0.50 x **S4**, gate on the **equity leg only**, sleeve
  normalised to gross and **never gated**, **no rescale** (family **C135**).
* ideas 138/402 carry **no gate arm at all** — `band3-rw` is not expressible there.

## C — the decisive grid (288 fresh rows; 2 tuned dials: leg, f)
Crossing the ingredients that differ, at every reported convention (family x arm x sleeve x
panel x cost).  Gates all EXACT (0.000e+00): `H.run` == `engine.backtest`; this run's
constructor == idea 133's `S3-50` **and** idea 135's `SLV50` on both conventions; f=0 == the
plain base book.

* 4a(v2) 22 / 288 · 4b 84 / 288 · **BOTH 2 / 288 (0.7%)**
* Both live at **one** coordinate: `C133 · band3-rw · leg R20 · f 0.50 · sleeve S3 · 10 bps`,
  on u56 (11.27%/1.2624/-11.63%) and broad (11.50%/1.1350/-11.82%) — idea 142's two rows,
  reproduced from prices.
* Zero at `f` 0 or 0.25, zero on the EWall leg, zero on S4, zero at 25 bps, zero under `dg`,
  **zero under family C135** — idea 135's construction cannot reach it.
* Idea 404's mechanism survives as a tendency: of the 22 rows clearing 4a, **20 fail 4b on the
  CAGR floor alone**.

## D — rule 8 walk-forward (dials on 2009–2016, 2017–2026 read once)
48 cells: OOS 4a 9, OOS 4b 11, **OOS BOTH 0**.  Following the two full-sample both-paths rows
into the untouched window:

| | OOS CAGR | OOS Sharpe | OOS MaxDD | OOS halves | RULES v2 OOS halves | 4a | 4b |
|---|---|---|---|---|---|---|---|
| u56 | 11.73% | 1.2886 | -11.63% | 1.268 / 1.317 | 1.398 / 1.162 | **fail (H1)** | pass |
| broad | 10.82% | 1.0473 | -11.82% | 1.019 / 1.081 | 1.268 / 0.947 | **fail (H1)** | pass |
| SPY OOS | 15.45% | 0.8820 | -33.72% | 0.975 / 0.782 | — | — | — |

Both lose the **first OOS half** to the live book, and broad clears 4b's OOS CAGR floor by
**+0.0048 pp/yr** (10.8201% vs a floor of 10.8153%) — a knife-edge, not a margin.

## What the record should say
1. **Not** "the paths are exclusive."  A joint pass exists and reproduces from prices.
2. **Not** "the emptiness was a comparand bug" either — the zeros are exact under idea 142's
   own comparand.  They are **coverage** statements: three corpora that cannot express the
   coordinate reported its absence as a property of the bars.
3. The honest wording is a rate with a corpus attached: *joint 4a+4b passes exist at ~0.7% of
   grid points, at a single (leg, f, sleeve, convention, cost) coordinate, and 0 of 48
   walk-forward cells hold both paths out of sample.*
4. **KILL** for the book itself as a KEEP candidate: full-sample only, dies on 4a's H1 out of
   sample, and its 4b OOS floor margin is 5 bps/yr wide.

SURVIVORSHIP: `broad` is current constituents of `universe_broad.json` (PROTOCOL 9).
