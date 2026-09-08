# Idea 457 — publish-ROOM-beside-every-abstention-and-chooser-result (cloud lane, 2026-09-08)

**Verdict: ANSWERED / SPLIT. The back-fill is done and the clause is drafted; the queue's
premise is CONFIRMED as a contamination claim and CORRECTED as a directional one.
No RULES change, no KEEP, no memo; `RULES.md`, `PROTOCOL.md`, `scan.py`, `bot.py` and
`baseline.py` untouched.**

Script: `2026-09-08_publish-ROOM-beside-every-abstention-and-chooser-result_cloud.py`
(deterministic, no network, ~4 min). Two tuned parameters, all **22 grid points reported**:
**P1** abstention threshold as a quantile `q ∈ {0.0, 0.1, … 1.0}` of the corpus's own top-2
gap distribution (11), **P2** neutral comparand `∈ {MENU-MEAN, IS-MEDIAN-ARM}` (2). The
margin scale is PINNED at `raw` (idea 241's pre-registered scale) and the absolute anchor
τ = 0.013 is reported beside the grid as a pre-registered point, not fitted. Metric pinned at
Sharpe by the queue's wording; CAGR/MaxDD are a labelled sensitivity, not a third dial.

---

## 0. Gates — idea 241's decomposition reproduces from its own committed census, exactly

| term | this run | idea 241 published |
|---|---|---|
| `ROOM_241 = OOS_ctl − OOS_mean` | **+0.0258** (t +22.21, n **1834**) | +0.0258 (t +22.2) |
| `LIFT = OOS_star − OOS_mean` | +0.0201 (t +11.76) | +0.0201 (t +11.8) |
| `MARGIN = OOS_star − OOS_ctl` | −0.0058 (t −3.19) | −0.0058 (t −3.2) |
| `REGRET = OOS_best − OOS_star` | +0.0478 (t +26.94) | +0.0478 (t +26.9) |

Cell count **1,834** matches the queue's own number exactly. Two identities checked to machine
precision: `MARGIN = ROOM_445 − REGRET` (max|err| **0.000e+00**) and
`GAIN = ROOM_241 − LIFT` (max|err| **5.55e-17**).

## 1. A naming correction the record needs first

**The record already uses "ROOM" for two different quantities**, exactly as idea 445 found for
`regret`:

* `ROOM_445 = OOS_best − OOS_ctl` — headroom **above** the fallback (idea 445's clause);
* `ROOM_241 = OOS_ctl − OOS_neutral` — the fallback's free **premium over a random menu draw**
  (idea 241's +0.0258, and the one idea 457 asks to net out).

They are different numbers on the same cells (Sharpe: +0.0420 vs +0.0258) and they enter
different identities. Any clause PROTOCOL adopts must name which one it means.

## 2. PART A — the back-fill (`.cells.csv`, 5,422 rows; 1,834 Sharpe)

Nothing is recomputed from prices: every input column is already published by idea 241, so the
back-fill is **exact and lossless — 0 unaudited cells**, unlike idea 445's ladder recovery.

| metric | cells | files | ROOM_241 | LIFT | ROOM_445 | REGRET | GAIN |
|---|---|---|---|---|---|---|---|
| **Sharpe** | 1834 | 45 | **+0.0258** (t +22.2) | +0.0201 | +0.0420 | +0.0478 | +0.0058 |
| CAGR | 1805 | 42 | +0.0204 (t +27.4) | +0.0308 | +0.0134 | +0.0030 | −0.0104 |
| MaxDD | 1777 | 40 | −0.0335 (t −23.4) | +0.0404 | +0.0889 | +0.0149 | −0.0740 |

The control beats a random menu draw in **75.5%** of the 1,834 cells but beats the IS-argmax in
only 34.5% of them. Leave-one-out check: excluding the compared arm from the neutral multiplies
each term by exactly `n/(n−1)` (ROOM_241 +0.0258 → +0.0279, LIFT +0.0201 → +0.0241), so **no
sign and no verdict in this run depends on that convention.**

## 3. PART B — the τ grid: every positive pooled verdict flips

`D_raw(τ) = mean 1{margin<τ}(OOS_ctl − OOS_star)` vs `D_net(τ) = mean 1{margin<τ}(OOS_neutral − OOS_star)`.

| | grid points | POSITIVE raw | POSITIVE net | **FLIP** | reverse flip |
|---|---|---|---|---|---|
| pooled over the record (22 grid pts + 2 anchors) | 24 | 18 | **0** | **18** | 0 |

The anchor τ = 0.013: `D_raw` **+0.0030 (t +2.84)** → `D_net` **−0.0127 (t −11.79)** under
MENU-MEAN, **−0.0095 (t −6.38)** under IS-MEDIAN-ARM. The free term `FREE = +0.0157` is larger
than the whole published gain. **The headline is not merely inflated by ROOM — it is ROOM,
minus a negative selector term.**

**File-level verdicts** (one parent file × one grid point = one published-shaped abstention
verdict; 44 files × 10 τ × 2 neutrals = 880):

| neutral | verdicts | POS raw | POS net | **FLIP** | reverse flip |
|---|---|---|---|---|---|
| MENU-MEAN | 440 | 254 | 62 | **208 (81.9% of the positive ones)** | 16 |
| IS-MEDIAN-ARM | 440 | 254 | 141 | **140 (55.1%)** | 27 |

The flip share under MENU-MEAN is high at **every** rung of the abstention rate and is not a
property of one corner of the grid — 5/6 at q=0.1, 21/22 at q=0.3, 29/32 at q=0.6, 23/35 at
q=1.0 (66%–95%). It is not monotone: the netting bites everywhere, not only where the rule
leans hardest on the fallback.

## 4. PART C — the record's own published abstention verdicts, re-quoted

Mechanical population: every committed `research/backtests/*.csv` carrying an abstain-family
column. **19 files over 10 parent stems.**

| status | files | published rows |
|---|---|---|
| **AUDITED** (a neutral comparand is published or recoverable) | 5 | 1,077 |
| ROOM445-ONLY (headroom back-fillable, no neutral published) | 2 | 279 |
| **UNAUDITED** (counted as unaudited, never as a pass) | 12 | — |

Of the audited rows: **362 POSITIVE raw → 310 POSITIVE net, and 150 flip (41.4% of the positive
ones).** By stem: `the-013-margin-rule_B` taugrid **26 of 26** positive rows flip and
sensitivity **6 of 6** flip (its `incumbent ∈ {ctl, mean}` rows are a free within-file re-quote);
`is-K_MEDIAN-a-real-abstention-rule` **59 of 165** flip against its own published `pool_OOS`.

**12 of 19 files cannot be re-quoted at all** — including
`2026-09-05_abstention-is-the-only-thing-that-ever-helps_cloud`, the most abstention-shaped
result in the record, which publishes `gain` and `mean_OOS_Sharpe` but no neutral arm. That
is the clause's case: the column has to be written at run time; it cannot be recovered later.

## 5. PART D — rule 8 on the corpus

Split by **publication** date (every parent file is dated 2026-09-xx; the market-time
walk-forward is PART E), IS 957 cells / 29 files, OOS 877 cells / 16 files. `q*` chosen on the
first half is **1.0 — a grid edge, "always abstain"** (IS D +0.0283). Read once on the second
half: **D_raw −0.0189 (t −7.87)**, D_net −0.0333 (t −16.38). The tuned threshold does not
transfer even within the corpus, and no verdict flips because none is positive to begin with.

## 6. PART E — rule 8 on LIVE PRICES, out of corpus (idea 241's pre-registered 31-arm menu)

3 panels × 2 cost rungs × 200 seeded sub-menus = **1,200 live cells**, reproducing idea 241's
committed count exactly. Arms chosen 2010–2013, τ chosen 2014–2016, **2017-01-01 onwards read
once**, t+1 execution, 10 bps anchor + 25 bps rung.

**The premise's direction does not survive the move to fresh prices.**

| corpus | ROOM_241 | star_is_ctl | GAIN |
|---|---|---|---|
| committed record (1,834 Sharpe cells) | **+0.0258** (t +22.2) | 34.4% | +0.0058 |
| live, all panels (1,200) | **−0.0133** (t −8.3) | 74.3% | −0.0329 |
| live, broad136 | +0.0008 | **100.0%** | +0.0000 |
| live, small439 | +0.0442 | **100.0%** | +0.0000 |
| live, u56 | **−0.0849** | 23.0% | −0.0986 |

On two of three live panels the ungated control **is** the IS argmax in every sub-menu, so the
abstention rule is a strict no-op there and the ABSTAIN, ARGMAX and INCUMBENT books are
literally the same book (this is the degeneracy open idea 458 asks about; it is confirmed
here). On u56 — the one panel where the rule acts — the control's room is **negative**, so
netting ROOM out makes the abstention delta *less* bad, not more. **0 of 22 live grid points
are positive raw; 0 are positive net.**

Realised books (τ frozen at the calibration q*, which is again the "always abstain" edge):

| panel | cost | book | OOS CAGR | OOS Sharpe | OOS MaxDD | SPY OOS | v2 OOS |
|---|---|---|---|---|---|---|---|
| u56 | 10 | **ARGMAX** | 11.79% | **1.274** | −15.5% | 0.882 | 1.285 |
| u56 | 10 | NET-ABSTAIN | 10.55% | 1.261 | −14.9% | ″ | ″ |
| u56 | 10 | ABSTAIN | 18.47% | 1.135 | −29.2% | ″ | ″ |
| broad136 | 10 | ABSTAIN = ARGMAX | 18.59% | 1.101 | −32.7% | 0.882 | 1.119 |
| broad136 | 10 | NET-ABSTAIN | 9.47% | 1.150 | −15.8% | ″ | ″ |
| small439 | 10 | ABSTAIN = ARGMAX | 12.88% | 0.635 | −46.0% | 0.882 | 0.568 |

SPY OOS: CAGR 15.45%, Sharpe 0.882, MaxDD −33.7%.
`ABSTAIN − ARGMAX` OOS Sharpe **−0.0414, wins 0/6**; `NET-ABSTAIN − ARGMAX` **+0.0062,
wins 3/6** — abstaining to the *neutral* arm is a coin flip, abstaining to the *control* is a
loss. **BOTH KEEP PATHS over the 24 live books: 4a 0/24, 4b 2/24, 4a(OOS) 0/24, 4b(OOS) 2/24**,
and both 4b passes are the ARGMAX book on u56, whose picks are idea 241's already-committed
`b0-g1.00-{W,M}` arms — nothing new is promoted. NET-ABSTAIN on u56 misses 4b only on the CAGR
floor (10.55% vs the 10.82% required).

## 7. The clause, as drafted (report-only; PROTOCOL is NOT edited by this run)

> **Clause (abstention results).** Any result reporting that an abstention rule beats its own
> unabstained selector must publish, in the same table: (i) `ROOM = OOS_fallback − OOS_neutral`,
> the free premium the fallback carries over a random draw from the same menu, and (ii) the
> **net** delta with that room removed. The identity
> `GAIN = ROOM − LIFT` is exact, so a verdict is reportable as an *abstention* effect only if
> the net delta carries the same sign as the headline. The neutral arm must be named
> (`MENU-MEAN` is the default; `IS-MEDIAN-ARM` is admissible and reported separately, since the
> two disagree on 68 of 254 file-level verdicts here). Where the fallback is the IS argmax in
> ≥ 95% of a corpus's cells, the rule is a no-op on that corpus and must be labelled one rather
> than scored.

## 8. What the queue asked, answered

* *Back-fill ROOM over the 1,834 control-carrying census cells* — **done, exactly, 0 unaudited**
  (`.cells.csv`).
* *How many published abstention verdicts flip?* — **18 of 18 positive pooled grid points; 208
  of 254 file-level verdicts (81.9%) under MENU-MEAN and 140 of 254 (55.1%) under
  IS-MEDIAN-ARM; 150 of 362 positive rows (41.4%) in the record's own published abstention
  files, with 12 of 19 such files not re-quotable at all.**
* *The premise* — **CONFIRMED as contamination** (the free term exceeds the whole published
  gain at the anchor) and **CORRECTED as direction**: ROOM_241 is **+0.026 on the committed
  corpus and −0.013 on fresh live prices**, so netting it out moves published verdicts both
  ways. The clause is needed because the term is large and unsigned, not because it is always
  positive.

---

## 9. CONCORDANCE — this is an independent concurrent SECOND RUN

Lane C claimed and pushed idea 457 the same day (`..._C.py`, commit `76c73a5`). This run was
written and executed without sight of it and is filed as a second reading, not a fresh claim.
The two runs use different designs — lane C's second dial is the margin **norm** {raw, z, rng}
and it carries an exact within-file permutation null; this run's second dial is the **neutral
comparand** and it carries the record's own abstain-column files as a third corpus.

| claim | lane C (`_C`) | this run (`_cloud`) | agree? |
|---|---|---|---|
| idea 241's four decomposition numbers reproduce | max \|Δmean\| 4.98e-05 | 4 dp on all four | **yes** |
| control-carrying Sharpe cells | 1,834 / 45 files | 1,834 / 45 files | **yes** |
| argmax **is** the control | 631 (34.4%) | 631 (34.4%) | **yes** |
| ROOM > 0 share | 75.5% | 75.5% | **yes** |
| positive abstention verdicts that flip | **277 of 425 (65.2%)** | **208 of 254 (81.9%)** MENU-MEAN, 140 of 254 (55.1%) IS-MEDIAN-ARM | **yes, in direction and rough size** (different verdict units) |
| ROOM is not a constant | per-file −0.0206 … +0.1487, negative in 7 of 45 | sign INVERTS corpus (+0.0258) vs live (−0.0133) | **yes** |
| live ROOM by panel | u56 −0.0837, broad136 +0.0013, small439 +0.0442 | u56 −0.0849, broad136 +0.0008, small439 +0.0442 | **yes** |
| KEEP paths | prose says "4b 0 of 24"; **its own `_C.keeppaths.csv` carries `pass4b` True on 2 rows** | 4a 0/24, **4b 2/24** | **the artefacts agree; lane C's prose does not** |

**One correction to lane C's filing.** Both runs find the same two 4b passes — the u56 ARGMAX
book at 10 and 25 bps (`_C`: OOS 11.66% / 1.2731 / −15.46%; `_cloud`: 11.79% / 1.2743 /
−15.53%). Lane C's memo sentence "4b 0 of 24 books for every book under test" is contradicted
by its own committed `.keeppaths.csv`. Neither pass is new: both are idea 241's already-filed
`b0-g1.00-{W,M}` arms, so **no book is promoted by either run** and the verdict is unchanged.

**What this run adds beyond lane C:** (i) the record's own 19 abstain-column CSVs re-quoted,
with 12 of 19 shown to be **unauditable after the fact** — the strongest argument for making
the column mandatory at run time; (ii) the **ROOM naming collision** between ideas 241 and 445,
which any PROTOCOL clause must resolve; (iii) the `star_is_ctl` = **100%** no-op degeneracy on
broad136 and small439, an independent confirmation of open idea 458.
