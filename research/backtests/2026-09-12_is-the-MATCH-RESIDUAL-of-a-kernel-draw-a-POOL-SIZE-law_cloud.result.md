# Idea 800 — is-the-MATCH-RESIDUAL-of-a-kernel-draw-a-POOL-SIZE-law (cloud, 2026-09-12)

**ANSWERED = NO. There is no pool-size law. All six pre-registered hypotheses FAIL, the queue's
premise is KILLED, and idea 796's 430→663 observation is re-measured here at 0.83x (its own
convention) and 0.48x (frozen rungs) against its published 4.90x — inside this machinery's own
re-draw noise, and in the opposite direction. No KEEP: 4a 0 / 4b 51 / BOTH 0 of 2,496 books
(0 / 26 / 0 of 1,560 distinct), and no book here is a tradable rule.**

Script: `2026-09-12_is-the-MATCH-RESIDUAL-of-a-kernel-draw-a-POOL-SIZE-law_cloud.py`
Artefacts: `.grid.csv .rungs.csv .law.csv .ladder.csv .dispersion.csv .overlap.csv .heldout.csv
.vintage.csv .walkforward.csv .keeppaths.csv .gates.csv .console.txt`

## What was run

Idea 569/571's kernel draw (k names, weights ∝ exp(−½((x−L)/h)²), h = BW·sd(char), BW held at
0.500) re-run inside **sub-sampled arms**, with the rung levels frozen once at the full pool's own
Q5 quantiles in raw characteristic units so a rung means the same thing in every cell.

* **Tuned (2, the queue's own):** pool size s ∈ {40, 60, 90, 136, 200, 330} × k ∈ {12, 24, 36, 48}.
  Pool size is applied three ways — SYM (both arms at s), THIN (only the thin arm moves), THICK
  (only the thick arm moves) — which is the discriminating test for the queue's min(n) reading.
  All 144 (pair, shape, s, k) points reported; 30 are unavailable (an arm cannot reach s, or
  s ≤ k leaves the kernel no freedom).
* **Reported, never selected:** arm pair (BS = the record's B-vs-SMALL arms; **SS = two disjoint
  random halves of the small panel, a same-distribution null** reaching min(n) = 330),
  characteristic (momac, tpers), CHARBASIS (FULL = chars and bandwidth frozen at the full pool;
  SUB = both recomputed inside the sub-sample), replicate 0–5, rung, seed 0–5, window, gross,
  cadence, book form. 9,471 (cell, char, rung) residual rows over 1,343 feasible cells.
* **Panel:** B136 (135 tradable) ∪ sub-$2B screen (663 tradable after dropping the 52 tickers with
  `max_1d_move ≥ 1.0` per PROTOCOL), 2010-01-04 … 2026-09-04, 4,194 bars, 797 names after G1.

**Gates.** G1 contiguity: 1 of 798 names (MMC) carries an interior gap and was **dropped**, which
makes the vectorised lag-21 autocorrelation exact by construction for every remaining name (rungs
re-frozen afterwards). G2 estimator: vectorised vs idea 571's pandas momac, max |Δ| **3.7e-15**
(bar 1e-12) PASS. G0 determinism PASS. G3 engine: `fast_backtest` vs `engine.backtest`
**1.4e-17** (bar 1e-9) PASS. G4 anchor (measured, not gated — the small panel has been appended to
since idea 796 ran): this run's full-pool BW=0.500/Q5/k=36 |resid| momac **0.0056** vs idea 796's
committed 0.0050 (its Q19 set), tpers **0.0014** vs 0.0013.

## The six pre-registered hypotheses: 0 of 6

| | claim | reading | verdict |
|---|---|---|---|
| H_MONO | Spearman(min_n, \|resid\|) ≤ −0.90 on the SYM ladder | BS/tpers −0.500, SS/momac −0.429, SS/tpers −0.371 | **FAIL** |
| H_MIN | the THIN arm governs | THICK-only moves are NOT inert (BS/momac max \|Δlog10\| 0.277 vs bar 0.10); THIN/SYM worst ratio 2.10x vs bar 1.25 | **FAIL** |
| H_POWER | log-log R² ≥ 0.80, slope ∈ [−1.00, −0.25] | pooled R² 0.005–0.046, slopes −0.167 … **+0.086** | **FAIL** |
| H_FILL | K/min_n beats min_n | residual sd 0.192/0.221/0.217/0.233 vs 0.203/0.221/0.219/0.227 — wins 1 of 4 | **FAIL** |
| H_NEFF | kernel n_eff beats both | R² 0.016/0.010/0.009/0.050, never beats both | **FAIL** |
| H_VINT | a min(n) law reproduces idea 796's 430→663 move | momac MOVES (ratio 0.483), tpers inert (1.026) | **FAIL** |

**The clean SYM ladder** (rung- and replicate-averaged, one fit per pair × char × k × basis) is the
law in isolation: 13 fits at CHARBASIS=FULL, **median slope −0.208, median R² 0.399, 1 of 13 with
Spearman ≤ −0.90, and 3 with a POSITIVE slope**. On the SS pair, where min(n) spans 40 → 330 (a
factor of 8), momac at k=36 reads 0.01086 / 0.00185 / 0.00340 / 0.00327 / 0.00301 / 0.00296 and
tpers 0.00064 / 0.00078 / 0.00088 / 0.00074 / 0.00068 / 0.00054 — flat from s = 60 upward.
Growing the pool eightfold buys essentially nothing.

## What the residual is actually entitled to

The deliverable the queue asked for exists, but it is a **noise band, not a formula**.

Across 216 cells of six replicates that differ only in which names were sub-sampled — identical
shape, size, k and rungs — the **within-cell max/min of |resid| has median 2.56x, p90 5.49x, max
48.18x**. Pooling the (nearly inert) shape and size axes gives median p90/p10 3.18x.

So **a matched-level residual quoted from one cell of this machinery carries a factor of about 2.6x
from re-drawing alone**, before any panel content is involved. Idea 796's cited 0.0133 → 0.0027
(4.90x; FROZEN vs LIVE, BW=0.500/Q5, 4 rungs each, read from its own `.summary.csv`) sits inside
that band. Re-measured here with the arms held fixed and only the thick arm's size changed, the same
contrast reads **0.826x** under idea 796's own per-vintage-rung convention and **0.483x** with the
rungs frozen — the **opposite direction** in both. tpers is inert on the same move (1.026 / 0.975).
The remaining differences from idea 796 are its seed key (flavour label) and its exact FROZEN B
arm; those are named rather than resolved, because a 4.90x reading on one 4-rung cell is not
separable from 2.6x re-draw noise either way.

## Post-hoc (labelled as post-hoc; not pre-registered, and it fails its own held-out test)

In **bandwidth units** the picture is much tidier. |resid| / sd(char) collapses momac and tpers from
**4.95x apart in raw units to 1.14x** (BS) and 4.89x → 1.15x (SS): BS momac 0.0881, BS tpers 0.1001,
SS momac 0.0473, SS tpers 0.0546. The cross-panel arms sit **1.85x above** the same-distribution SS
null, which is the composition bias on top of the matching floor.

That reading was then tested on a **held-out third characteristic never used in the grid** (`avol`,
annualised realised daily vol, sd 0.2003 against momac's 0.0724), with the predicted band stated
before the number was computed. It lands **OUTSIDE on both arms**: BS 0.4104 (predicted
[0.0881, 0.1001]) and SS 0.0347 (predicted [0.0473, 0.0546]). The sd-collapse is therefore a
two-characteristic coincidence, not a law.

What survives the held-out test is the **separation** of the two arms in the characteristic, not the
size of either pool. Over the six (pair, char) points:

| pair | char | SMD | OVL | \|resid\|/sd |
|---|---|---|---|---|
| BS | momac | 0.328 | 0.817 | 0.0881 |
| BS | tpers | 0.369 | 0.759 | 0.1001 |
| BS | avol | 1.146 | 0.385 | 0.4104 |
| SS | momac | 0.048 | 0.889 | 0.0473 |
| SS | tpers | 0.127 | 0.890 | 0.0546 |
| SS | avol | 0.009 | 0.859 | 0.0347 |

Spearman(SMD, |resid|/sd) = **+1.000**, Spearman(OVL, |resid|/sd) = −0.771 over six points. Six
points is not a law; it is queued (idea 802) for a pre-registered test.

## Rule 8

**WF-A (the answer).** Characteristics re-estimated on IS prices alone and on OOS prices alone and
the whole law refit in each. The predictor was chosen on IS by pooled R² — `neff_min`, IS pooled
mean R² **0.088** — and its OOS reading taken once: OOS mean R² **0.115**, and it is still the OOS
winner (neff_min 0.115 > min_n 0.100 > tot_n 0.100 > fill 0.019). The ranking walks forward; the
*magnitude* does not, because at R² ≈ 0.1 there is almost nothing to walk. Every window-specific
slope is in the CSV; on the BS arms the OOS min_n slope is **+0.009** (momac) and **+0.194** (tpers),
i.e. the wrong sign.

**WF-B (a book).** 2,496 books (1,560 distinct name-set × form × gross), 10 bps, next-day fills,
weekly, over 2011-01-13 … 2026-09-04. Pick by IS Sharpe alone, OOS read once:

| | CAGR | Sharpe | MaxDD | halves | OOS CAGR | OOS Sharpe | OOS MaxDD |
|---|---|---|---|---|---|---|---|
| WF-B pick (momac, arm B, s=90, k=12, L=0.8748, EWall, g=1.00) | 19.81% | 1.264 | −29.01% | 1.478 / 1.122 | **19.95%** | **1.203** | **−29.01%** |
| RULES v2 (U56, live) | 8.19% | 1.169 | −12.05% | 1.056 / 1.272 | 9.53% | 1.285 | −12.05% |
| SPY | 14.13% | 0.862 | −33.72% | 0.891 / 0.858 | 15.45% | 0.882 | −33.72% |

The pick beats SPY on OOS CAGR and Sharpe and loses to the live book on OOS Sharpe. **4a False**
(second-half Sharpe 1.122 < RULES v2's 1.272, and MaxDD −29.01% vs −12.05%). **4b FAIL on DD**
(−29.01% against the −20.23% cap = 60% of SPY's).

**KEEP paths over all books: 4a 0 / 4b 51 / BOTH 0** of 2,496 (0 / 26 / 0 of 1,560 distinct). Every
4b passer is a `MA-RS` book at g=0.75 drawn from the B arm at s ∈ {40, 60, 90}, i.e. a
kernel-weighted seeded draw of 12–48 large caps. **None is a capital candidate and none is claimed
as one** — there is no rule here anyone could trade, because the "rule" is "draw 36 names with these
seeds". Fail-leg census: DD alone 524, CAGR alone 287, everything 736.

## Caveats

* **Survivorship.** Both arms are current constituents; names that died are absent. The object of
  the law is a difference of *achieved characteristic levels* between two draws from the same
  screened universe, so the bias is second-order there. The return legs (WF-B, the KEEP counts)
  carry the usual upward bias and are read as diagnostics only.
* min(n) spans only 40 → 136 on the record's own BS arms (B136 is the binding ceiling). The 8x
  span, and therefore the strongest evidence for H_MONO/H_POWER failing, comes from the SS pair.
* The post-hoc SMD reading rests on six points and is not claimed.

## Consequence for the record

Any committed matched-level claim that quotes a single |resid| is quoting a number with a **~2.6x
re-draw band** around it, and **cannot** buy precision by growing the pool. The two things that do
move it are the characteristic's own scale (trivially, the kernel is scale-equivariant) and how far
apart the two arms sit in that characteristic. No RULES, PROTOCOL, scan.py, bot.py or baseline.py
edit; nothing outside this run's own outputs was touched.
