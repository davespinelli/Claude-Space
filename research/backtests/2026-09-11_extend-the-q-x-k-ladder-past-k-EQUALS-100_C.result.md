# Idea 685 — extend-the-q-x-k-ladder-past-k=100 (lane C, 2026-09-11)

**ANSWERED / THE CLASSIFICATION DOES NOT TRANSFER — KILL. No KEEP (4a 0/306, 4b 0/306).**

Idea 525 (lane B) classified the record's five published "panel property explains the
result" statistics on a ladder whose **k arm spans 2.5x** (40..100, capped because BSTK100
has exactly 100 names). The record publishes panel claims across **12.5x** of width
(ETF36 k=35 -> SMALL439 k=439). Idea 685 asked whether that classification survives at the
widths the record actually uses.

It does not. **Extending k to 400 on matched q support flips 3 of 5 pre-registered verdicts
and 4 of 5 beta readings.**

## Construction

No internet in this sandbox, so the large-cap pool cannot be widened; this run takes the
queue's own second option — restrict to `q >= 0.5` and extend `k`. A cell exists iff
`q*k <= 439` and `(1-q)*k <= 100`, giving 17 feasible cells, 3 seeded draws each:

| q | k |
|---|---|
| 0.50 | 40, 60, 80, 100, 200 |
| 0.75 | 40, 60, 80, 100, 200, 400 |
| 1.00 | 40, 60, 80, 100, 200, 400 |

**51 panels, k span 40..400 = 10.0x** (lane B 2.5x; the record's own 35..439 = 12.5x). This
is the widest k arm the committed caches support at all. Two tuned parameters (q, k);
everything else — the RULES v1 gate, GROSS 0.75, weekly cadence, 10 bps, next-day execution,
260-day warm-up skip, NS_LAD {5,10,15,20,30}, 3 draws — is lane B's / idea 286's published
convention, imported and not re-typed.

Because the k extension and the q restriction are two different changes, every statistic is
classified on **three supports** so they can be told apart:

* **(B)** lane B, `q in [0,1], k <= 100`, 58 panels — read from its committed `.decomp.csv`
* **(N)** NARROW, `q >= 0.5, k <= 100`, 36 panels — **lane B's own panels, reproduced**
* **(W)** WIDE, `q >= 0.5, k <= 400`, 51 panels — N plus the 15 new wide panels

`W - N` is the **k extension** on matched q; `N - B` is the **q restriction** at matched k.

## Gates (asserted before any new number was read)

* **G0 REPRODUCTION — PASS.** Lane B's rng draw sequence (seed 2026, its full loop in its own
  order, including the q=0.00/0.25 cells that advance the generator) is replayed, and the
  q>=0.5 subset re-measured from scratch. **36 panels x 14 quantities** — Ebar, breadth,
  Emed, Ebar_IS, breadth_IS, S1..S5, EW_Sharpe, EW_OOS_Sharpe, ADAPT_Sharpe, best_prem —
  reproduce its committed CSVs at **machine precision, worst 7.105e-15**, 0/36 moving above
  1e-9 on every column. The WIDE reading is therefore a strict extension of lane B's, not a
  re-implementation of it.
* **G1 k-IDENTITY — PASS.** `max |k*breadth - Ebar|` over all 51 panels = **1.421e-14**.
* **G2 ENVELOPE — PASS.** All 51 panels: exact width, exact cap mix, no duplicate columns,
  inside the pool bounds.

## The extended ladder decouples far better than the narrow one

|  | Ebar span | Spearman(breadth, Ebar) |
|---|---|---|
| idea 286 (fixed k=40) | — | **+0.99999** |
| lane B published (q in [0,1], k<=100) | — | +0.5166 |
| NARROW (q>=0.5, k<=100) | 10.87..53.11 = **4.89x** | +0.3719 |
| **WIDE (q>=0.5, k<=400)** | 10.87..164.98 = **15.18x** | **+0.0963** |

Breadth stays flat in k out to 400 (within-q sd 0.010–0.024 against 0.089 across q), so the
design's identifying assumption holds at the new widths — the extra span is pure n_elig.

## The classification, three supports

| statistic | (B) lane B | (N) narrow | (W) **wide** | beta_log breadth / beta_log k (N -> W) |
|---|---|---|---|---|
| S1 rho(n, OOS Sharpe) [209/199] | breadth | breadth | **JOINT** | +0.660/+0.127 -> +0.629/**+0.297** |
| S2 INV-vs-NONE top-20 overlap [153] | JOINT | JOINT | **n_elig** | −0.419/−0.904 -> **−0.245/−0.993** |
| S3 Sharpe-vs-CAGR reversal [271/269C] | breadth | breadth | breadth | +0.581/−0.140 -> +0.520/−0.189 |
| S4 argmax_n premium vs EWall [155] | breadth | NULL | **breadth** | +0.500/+0.138 -> +0.533/+0.201 |
| S5 fixed n=20 − adaptive n_t [157] | NULL | NULL | NULL | +0.083/−0.202 -> +0.089/**+0.062** |

* **k extension (N -> W): 3 of 5 verdicts flip, 4 of 5 beta readings flip.**
* **q restriction (B -> N): 2 of 5 verdicts flip** (S4, S5) — reported separately, so it is
  not charged to the k arm.
* **Only S3 is stable on all three supports.** Every other published statistic reads
  differently depending on how much width you are allowed to see.
* The count the queue tracks: **2 of 5 n_elig at k<=400** (1 of them JOINT) against lane B's
  published **1 of 5** at k<=100.
* The 2-of-3 sign-consistency sensitivity returns the **same five verdicts** as the
  pre-registered 3-of-3 bar, so the result is not a discreteness artefact of the 3-level
  q grid (that grid's bar is the stricter one, and it did not bite).

### S2 — lane B's one raw-width claim, at 10x of width

Lane B read S2 as "mixed" (beta_log k −0.919 vs beta_log breadth −0.421) and its
pre-registered verdict as JOINT. At k<=400 the breadth loading **halves** and the reading
goes cleanly to **k**:

| support | beta_log breadth | beta_log k | reading | R² |
|---|---|---|---|---|
| lane B (k<=100, all q) | −0.421 | −0.919 | mixed | 0.945 |
| NARROW (k<=100, q>=.5) | −0.419 | −0.904 | mixed | 0.954 |
| **WIDE (k<=400, q>=.5)** | **−0.245** | **−0.993** | **k** | **0.972** |

The raw level is monotone in width across the whole 10x, which is the extrapolation lane B
could not see: **k=40 0.9564, 60 0.8873, 80 0.8150, 100 0.7567, 200 0.5566, 400 0.3631.**
Lane B's *direction* on S2 was right and is now stronger; its *JOINT* verdict was an
artefact of the truncated k arm.

## PROTOCOL 4a / 4b (10 bps, every arm row)

**4a 0/306. 4b 0/306.** Zero at every k (40, 60, 80, 100, 200, 400) and every q
(0.50, 0.75, 1.00).

This is an **out-of-sample confirmation of lane B's own headline**: it found 21/348 4b
passes with *every* pass at q <= 0.25. This run adds 15 new panels at q >= 0.5 and widths
up to 400 and finds **no pass anywhere** — the q <= 0.25 boundary holds where lane B could
not look. No arm here is a new BOOK: CAND-n and EWall are the record's existing books
re-run on re-drawn panels, so a pass would have been a statement about the panel, not a
capital candidate.

## Rule 8 walk-forward (properties on 2010–2016, 2017–2026 read once)

Five selectors x five book sizes, run on **both** choice sets so the arm answers idea 685
directly: does giving the selector 10x of width instead of 2.5x change what it picks?

| selector | same panel (N vs W) | k picked N -> W | OOS Sharpe N -> W | delta |
|---|---|---|---|---|
| **EBAR-MAX** | **0/5** | **100 -> 400** | 0.6771 -> **0.5085** | **−0.1685** |
| | | | OOS MaxDD −26.79% -> **−30.03%** | |
| EBAR-MIN | 5/5 | 40 -> 40 | 0.4945 -> 0.4945 | 0.0000 |
| BREADTH-MAX | 5/5 | 60 -> 60 | 0.7421 -> 0.7421 | 0.0000 |
| BREADTH-MIN | 5/5 | 40 -> 40 | 0.4945 -> 0.4945 | 0.0000 |
| IS-SHARPE-MAX | 5/5 | 40/80 -> 40/80 | 0.8064 -> 0.8064 | 0.0000 |

**EBAR-MAX is the only selector the extension moves, and it moves it for the worse.** Given
a 400-name panel it takes it on 5 of 5 book sizes — n_elig is mechanically maximal at
maximal width — and pays **0.169 of OOS Sharpe** for it. BREADTH-MAX is untouched, because
breadth is flat in k and the wider panels offer it nothing.

That is the rule-8 form of the same finding. Lane B concluded EBAR-MAX and BREADTH-MAX were
"the same selector", differing by **0.0047** of OOS Sharpe. **Once k is a free axis to 400
they are not: the gap is +0.2336 in BREADTH-MAX's favour** (0.7421 vs 0.5085). Choosing a
panel on n_elig and choosing it on breadth agree only while width is held nearly fixed.

The same asymmetry shows up in raw predictive power, and the extension widens it. Within
book size, Spearman(IS property, OOS Sharpe):

| support | breadth_IS | Ebar_IS | gap |
|---|---|---|---|
| lane B published | +0.806 | +0.460 | 0.346 |
| NARROW (k<=100) | +0.694 | +0.357 | 0.337 |
| **WIDE (k<=400)** | **+0.589** | **+0.162** | **0.427** |

Giving the ladder 10x of width does not make n_elig a better forward predictor — it makes it
a worse one, and leaves breadth ahead by more than before.

Benchmarks on the WIDE ladder: **SPY OOS Sharpe 0.8820** (CAGR 15.45%, MaxDD −33.72%);
**RULES v2 OOS Sharpe 0.7272** (CAGR 5.19%, MaxDD −13.26%). **No selector beats SPY OOS on
any of its 5 book sizes (0/5 on all five selectors)**; RULES v2 is beaten 1/5 by BREADTH-MAX
and 1/5 by IS-SHARPE-MAX, 0/5 by the rest. Nothing here is capital-worthy.

## What this does and does not say

* It does **not** overturn idea 525's mechanical core: the k-identity holds (1.421e-14), and
  at fixed k breadth and n_elig remain the same variable up to a constant.
* It **does** say that lane B's published *classification* — and any classification fitted on
  2.5x of width — cannot be read onto the record's 12.5x. The record states panel claims
  across ETF36 (35) to SMALL439 (439); a verdict fitted at 40..100 flips on 3 of 5 of them by
  k=400.
* The practical consequence is narrow and cheap, and is **proposed, not taken**: any published
  panel-property claim should carry **the k range it was fitted on**, and no claim should be
  read outside it. This run changes no rule and promotes no book.

## Caveats, stated

* 3 draws per cell; the q grid has only 3 levels, so the q-side sign bar is 3-of-3 (stricter
  than lane B's 4-of-5 purely from discreteness). The 2-of-3 sensitivity is reported and
  returns identical verdicts.
* `q >= 0.5` is forced by the pool bounds, not chosen; it is why the three-support
  decomposition exists, and its own cost (2 of 5 verdicts) is reported separately.
* q=0.50 cannot reach k=400 ((1-q)*k would need 200 large caps), so the k=400 row is
  q in {0.75, 1.00} only.
* **SURVIVORSHIP** (idea 54, data/SMALL_PANEL_README.md): SMALL439 and BSTK100 are CURRENT
  constituents. The q >= 0.5 envelope makes this ladder *more* small-cap than lane B's, so
  every level is more optimistic than lane B's, and the widest panels are the most exposed —
  which cuts against, not for, the wide-k readings above.

RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py untouched. No KEEP, no memo, no rule
change. Follow-ups filed as 687–689.

Outputs: `.panels.csv` `.stats.csv` `.books.csv` `.decomp.csv` `.walkforward.csv`
`.console.txt`
