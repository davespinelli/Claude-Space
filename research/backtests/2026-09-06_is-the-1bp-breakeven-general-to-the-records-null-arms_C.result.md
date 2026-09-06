# Idea 262 — is-the-1bp-breakeven-general-to-the-records-null-arms (lane C, 2026-09-06)

**ANSWERED / KILL of the queue's premise, twice over.** (1) The record does **not** build every
null "either held or re-drawn": of 194 committed scripts, 59 call an RNG and only **9 build a
null that TRADES**, and 3 of those 9 use a **random-walk key** whose churn is emergent —
neither held nor re-drawn. (2) The 1-bp breakeven is **not general**. It is a monotone
function of the turnover ratio and lands at ~1 bp only for the two full-churn arms
(3.7–3.8x FWD's turnover). Median breakeven vs FWD runs **RANDW 0.99 → ROTW 0.75 → RANDM
6.45 → RWK 11.36 → RANDH 16.89 → RANDQ 21.72 → RANDA 24.88 bps**, and the held draw — the
record's majority construction — **never flips at all in 50 of 72 draws**. The usable
output is a **law**: `c* = dSharpe(0)·1e4 / (T_x/vol_x − T_y/vol_y)` reproduces the measured
breakeven at **R² 0.9989, median error 0.028 bps over 337 flipping points**, so idea 263's
proposed column is *provably sufficient* to reconstruct any turnover-mismatched verdict's
breakeven **without re-running it**. No RULES change, no new KEEP-candidate, no memo.
Nothing in `RULES.md`, `scan.py`, `bot.py` or `baseline.py` touched.

Script: `2026-09-06_is-the-1bp-breakeven-general-to-the-records-null-arms_C.py` ·
console `…_C.console.txt` · grids `…_C.{census,audit,grid,breakeven,walkforward,keep}.csv`

## Design

Ideas 82 and 260's construction, imported so their verdicts **reproduce inside this run
rather than being quoted**: panels U56 / B136 / BSTK100, weekly, next-day execution, gate =
above-200d AND vol20 < 0.60, key = the composite without the vol scaler, gross matched at
0.75 on every arm including EWall, n ∈ {20,30,40,60}, 8 seeds, every seed written out.
Comparands `FWD` (top-n by the composite) and `EWall`; baseline `v1`.

The null arms are a **persistence ladder** — the same uniform key, differing in nothing but
the re-draw period — plus the two constructions the ladder does not contain:

| arm | pick | turnover x/yr (seed-mean) | ratio to FWD |
|---|---|---|---|
| `RANDH` | uniform drawn **once**, held — idea 82's RAND, byte-for-byte (rng 1000+seed) | 9.03 | 0.79 |
| `RANDA` | fresh uniform each **year** (rng 3000+seed) | 9.67 | 0.85 |
| `RANDQ` | fresh uniform each **quarter** (rng 4000+seed) | 11.56 | 1.01 |
| `RWK` | a per-name gaussian **random walk** keyed by its own 126d momentum (rng 6000+seed) — the census's third shape, imported from `does-a-harmful-instrument-…_B` ll. 262-265 | 14.11 | 1.22 |
| `RANDM` | fresh uniform each **month** (rng 5000+seed) | 16.75 | 1.45 |
| `RANDW` | fresh uniform at **every weekly rebalance** — idea 260's RANDW, byte-for-byte (rng 2000+seed) | 42.89 | 3.66 |
| `ROTW` | **deterministic** weekly rotation, `(k·n + j) mod n_elig` in fixed alphabetical order | 44.70 | 3.81 |
| `FWD` | top-n by the composite | 8.2–14.3 | 1.00 |

Cadence is held at weekly for every arm; only the **pick's** persistence moves. `ROTW`
carries `RANDW`'s churn with zero randomness, which separates the draw from the churn.

Cost rungs **0 / 1 / 2 / 5 / 10 / 25 bps** on every book. `engine.backtest` computes
`port = (held·rets).sum − turnover·bps/1e4` and neither term depends on the rung, so each
book is run once at 0 bps and every rung derived exactly. **Harness identity asserted
before any result was read: `max|live − derived| = 0.000e+00`** on three checks
(U56/FWD20@10, B136/RANDW20 seed 0 @25, BSTK100/ROTW40@5); the run aborts otherwise.
Breakevens are solved by a 0.05-bps scan to 60 bps (so a non-monotonic difference cannot be
missed) then bisected to 1e-4 bps — exact, not the 3-point interpolation of idea 260 §5.

Two tuned parameters: **panel** and **n**. The arm is the hypothesis axis, the seed is
averaged over with every draw reported, the rung is the reported axis. Grid = 3 panels ×
202 books × 6 rungs = **3636 points, all in `.grid.csv`**. Cells with `sat_share > 0.25`
(a panel that cannot supply n names) are excluded from headline counts, leaving **9 of 12**.

**Reproduction gate.** `U56/FIXED20` **12.7% / 1.092 / −18.3%**, halves 1.088/1.102 vs
published 12.7%/1.093/−18.3%; `U56/RULES v1` **6.5% / 0.664 / −13.8%** vs 6.5%/0.666/−13.8%.
On idea 260's **exact 8-cell set** the two published isolates come back to the digit:

| | published (idea 82 / 260) | this run |
|---|---|---|
| `FWD − RANDH` @10 bps | −0.0213, t −2.72, 21/64 | **−0.0213, t −2.72, 21/64** |
| `FWD − RANDW` @0 bps | −0.0236, t −3.60, 20/64 | **−0.0236, t −3.60, 20/64** |
| `FWD − RANDW` @10 bps | +0.2883 | **+0.2883, t +28.24, 64/64** |
| B136 n=20 RANDW breakeven | ~1.3 bps | **1.295 bps** |

This run's own headline uses **9** unsaturated cells: U56 n=30 has `sat_share` 0.243 and
falls inside the same 0.25 cap. On 9 cells `FWD − RANDH` @10 is −0.0159 (t −2.19, 27/72).

## 1. THE CENSUS: the queue's premise is false about what the record contains

Every rng **call site** in `research/backtests/*.py`, classified by the shape of the draw
(the thing that sets an arm's turnover). Docstring prose is stripped and a call is only
counted when its receiver is bound to an RNG — this corpus discusses `rng.permutation(...)`
in design notes and binds the name `rng` to a DataFrame in one script.

| class | sites | scripts | can a cost rung move it? |
|---|---|---|---|
| `SEED_DECL` | 83 | 57 | — |
| `SUBSET_PANEL` | 33 | 31 | **no** — a random set of NAMES/CELLS held for the sample (ideas 78/83's k-of-136 sub-panels); membership does not churn |
| `OTHER` | 23 | 19 | no |
| `PERM` | 11 | 11 | **no** — every one is a STATISTIC |
| **`HELD_KEY`** | **7** | **4** | yes (barely — see §3) |
| **`REDRAWN_KEY`** | **3** | **2** | **yes** |
| **`NOISE`** | **3** | **3** | **yes** |

**Hand audit — all 11 PERM sites and all 33 SUBSET_PANEL sites were read, not sampled.**
**0 of 11** PERM sites is a time-varying name pick: they are permutation tests
(`rng.permutation(ry)` against a correlation, a failing-bar matrix, an abstention count),
corpus half-splits, or random draws of **mode indices** (`rng.permutation(np.arange(1, J))`).
No cost rung can move any of them.

So the record's exposure is **9 scripts, not 59**, and inside those 9 the dichotomy the
queue names is incomplete:

* **HELD_KEY (4)** — `the-share-at-which-ranking-stops-paying_cloud`,
  `back-fill-the-zero-bps-rung-…_cloud`, `is-RAND-beating-FWD-persistence-or-pick_C`,
  `ranking-subtracts-value_B`. All are idea 82's construction.
* **REDRAWN_KEY (2)** — `is-RAND-beating-FWD-persistence-or-pick_C` (idea 260's RANDW,
  already priced) and **`is-the-book-size-floor-a-corpus-wide-clause_C`**, whose `RND` key is
  `rng.random(px.shape)` — a fresh uniform for **every name on every day**. Never priced.
* **NOISE (3)** — `does-a-harmful-instrument-clear-more-often-than-a-helpful-one_B`,
  `does-share-price-any-key-or-only-vol_B`,
  `is-the-null-key-result-one-draw-or-a-distribution_cloud`. These trade
  `cumsum(rng.normal(0, sd, px.shape))` keyed by the walk's own 126d momentum:
  **neither held nor re-drawn — the rank order drifts.** Never priced.

## 2. THE PRICE: the breakeven is a monotone function of the turnover ratio

Sharpe difference `X − FWD` at matched n and matched gross, over the 9 unsaturated cells ×
8 seeds (72 draws per arm; ROTW is deterministic, 9 draws):

| arm | turn ratio | d @0 bps | d @10 bps | median breakeven | draws ≤10 bps | draws that never flip |
|---|---|---|---|---|---|---|
| `RANDH` | 0.79 | +0.0069 (t +0.98) | **+0.0159 (t +2.19)** | **16.89** | 8/72 | **50/72** |
| `RANDA` | 0.85 | +0.0183 (t +2.60) | +0.0209 (t +2.86) | **24.88** | 2/72 | 65/72 |
| `RANDQ` | 1.01 | −0.0026 (t −0.46) | −0.0172 (t −2.99) | **21.72** | 11/72 | 39/72 |
| `RWK` | 1.22 | +0.0217 (t +3.86) | −0.0156 (t −2.73) | **11.36** | 20/72 | 24/72 |
| `RANDM` | 1.45 | −0.0076 (t −1.00) | −0.0684 (t −8.49) | **6.45** | 32/72 | 35/72 |
| `RANDW` | 3.66 | +0.0195 (t +3.18) | **−0.2748 (t −26.88, 0/72)** | **0.99** | **48/72** | 24/72 |
| `ROTW` | 3.81 | +0.0113 (t +0.82) | **−0.2996 (t −8.42, 0/9)** | **0.75** | 6/9 | 3/9 |

**Pre-registered branch (b) holds and (a) fails.** Idea 260's 1.0–1.3 bps is reproduced
exactly for `RANDW`, and it is a property of that arm's **3.66x turnover ratio**, not of
nulls. Move the ratio to 1.45 and the breakeven is 6.5 bps; to 1.22 and it is 11.4;
to 0.79 — the record's majority construction — and the difference **usually never flips at
all**, because the held draw trades *less* than the composite and cost helps it.

`ROTW` matters: it is `RANDW`'s churn with **no randomness**, and it prices identically
(0.75 vs 0.99 bps, −0.300 vs −0.275 at 10 bps). Whatever the sub-1-bp breakeven measures,
it is **not about drawing at random** — it is about churning the book.

Against `EWall` the same ordering holds with lower breakevens throughout (RANDW 1.08,
ROTW 0.52, RANDM 2.56, RWK 6.45, RANDA 12.34, RANDQ 13.70, RANDH 36.98), because EWall
trades least of all.

## 3. Which published null verdicts actually flip

| construction | scripts | median breakeven vs FWD | verdict at PROTOCOL's 10 bps |
|---|---|---|---|
| HELD_KEY | 4 | 16.9 bps (8 of 72 draws ≤10) | **stands** |
| REDRAWN_KEY | 2 | 0.99 bps (48 of 72 draws ≤10) | **flips below ~1 bp** — one is idea 260, already priced; **`is-the-book-size-floor-a-corpus-wide-clause_C` is not** |
| NOISE / `RWK` | 3 | 11.4 bps (20 of 72 draws ≤10) | **rung-dependent — straddles 10 bps** |

So **4 of the 9 trading-arm null scripts carry an unpriced null whose comparison sits at or
below the protocol's own rung**, and the three that are worst-exposed are the ones the
queue's held/re-drawn dichotomy does not describe at all. The `RWK` finding is the sharper
one: at 0 bps `RWK − FWD` is **+0.0217, t +3.86, 48/72** — a random walk beats the composite
— and at 10 bps it is **−0.0156, t −2.73, 28/72**. The sign of that published shape reverses
*inside* the range of rungs the record uses.

## 4. THE LAW: idea 263's column is sufficient, and this proves it

To first order `dSharpe(c) = dSharpe(0) − c·(T_x/vol_x − T_y/vol_y)/1e4`, so
`c* = dSharpe(0)·1e4 / (T_x/vol_x − T_y/vol_y)`. Over the **337** flipping
(cell, arm, seed, comparand) points:

**R² = 0.9989 · correlation 0.9995 · median |error| 0.028 bps** (median measured 6.41 bps)

| arm | n | measured median | predicted median | median abs error |
|---|---|---|---|---|
| `RANDH` | 33 | 25.79 | 25.58 | 0.208 |
| `RANDA` | 33 | 14.77 | 14.77 | 0.133 |
| `RANDQ` | 50 | 14.76 | 14.82 | 0.182 |
| `RANDM` | 57 | 4.99 | 5.02 | 0.032 |
| `RWK` | 81 | 8.58 | 8.60 | 0.028 |
| `RANDW` | 74 | 1.01 | 1.02 | 0.001 |
| `ROTW` | 9 | 0.70 | 0.70 | 0.002 |

Pre-registered branch **(c) holds** (bar was R² > 0.90). **Any turnover-mismatched
comparison in the record can have its breakeven recovered to ~0.03 bps from four published
numbers — both turnovers, both vols, and the 0-bps difference — with no re-run.** That is
the deliverable idea 263 should be built on, and it means the back-fill it proposes is a
spreadsheet exercise, not 96 re-runs.

## 5. Rule 8 walk-forward (IS 2009–2016 chooses, OOS 2017–2026 read once)

Pooled equal-weight over the 3 panels. `ALL_ISARGMAX` picked `('RANDH',20,7)` on U56 and
`('RANDA',40,·)` on B136 and BSTK100 at 10 bps — i.e. **in-sample argmax over every arm
picks a low-churn random book**, which is idea 78/83's noise-admission finding again.

| OOS Sharpe | 0 bps | 1 | 2 | 5 | **10** | 25 |
|---|---|---|---|---|---|---|
| ALL_ISARGMAX | 1.225 | 1.189 | 1.144 | 1.116 | **1.069** | 0.929 |
| EWALL | 1.154 | 1.146 | 1.138 | 1.114 | **1.073** | 0.952 |
| RANDH20 | 1.152 | 1.143 | 1.135 | 1.108 | **1.064** | 0.932 |
| RWK20 | 1.169 | 1.154 | 1.139 | 1.093 | **1.017** | 0.788 |
| RANDM20 | 1.138 | 1.120 | 1.102 | 1.047 | **0.957** | 0.684 |
| **RANDW20** | 1.159 | 1.109 | 1.060 | 0.912 | **0.666** | **−0.068** |
| **ROTW20** | 1.149 | 1.098 | 1.048 | 0.896 | **0.644** | **−0.107** |
| FWD20 | 1.084 | 1.074 | 1.065 | 1.036 | **0.987** | 0.842 |
| RULES v1 | 0.924 | 0.897 | 0.871 | 0.791 | **0.658** | 0.258 |
| SPY | 0.882 | 0.882 | 0.882 | 0.882 | **0.882** | 0.882 |

The out-of-sample ordering **is the turnover ordering**, at every rung: the two full-churn
arms are the best nulls at 0 bps and the only selectors that go negative by 25 bps
(OOS CAGR −1.3% and −1.7%), while the held draw tracks EWall to within 0.01 of Sharpe
everywhere. OOS MaxDD is flat at −0.19 for every null and −0.34 for SPY.

## 6. KEEP paths

**4a 1121/3636 · 4b 1345/3636.** By arm at PROTOCOL's 10 bps:

| | EWall | FWD | v1 | RANDH | RANDA | RANDQ | RWK | RANDM | RANDW | ROTW |
|---|---|---|---|---|---|---|---|---|---|---|
| 4b @10 bps | 1/3 | 5/12 | 0/3 | **19/96** | **24/96** | 7/96 | 5/96 | 0/96 | **0/96** | 0/12 |
| 4b @0 bps | 2/3 | 8/12 | 0/3 | 57/96 | 59/96 | 59/96 | 62/96 | 52/96 | **63/96** | 7/12 |

**No new KEEP-candidate and no memo**: every 4b pass at 10 bps is either a *random* book
(a seeded null is not a rule) or ideas 2 and 10's published books reproduced —
`U56/FWD20` 12.8% / 1.064 / −18.3%, halves 1.068/1.066, OOS 1.131. The one thing worth
recording for idea 253 is that **a held random 20-name pick clears the capital-worthy bar in
19 of 96 draws at the protocol's own rung**, and the binding bar across the 10-bps grid is
CAGR (214) then DD (128). Turnover is the entire difference between a null that passes 4b
20% of the time and one that passes 0%.

## Verdict

**ANSWERED — KILL of the premise, on both halves.** The record does not have a
held-vs-re-drawn null problem: it has **nine** scripts with a trading null, four of which
carry an unpriced comparison at or below the protocol's rung, and three of those four use a
construction the dichotomy does not name. And the 1-bp breakeven is not a property of nulls
at all — it is `dSharpe(0)` divided by a turnover gap, reproducible at R² 0.9989, which
happens to equal ~1 bp when the gap is 3.7x and equals *never* when the gap is 0.79x.
**The correct standing quotation is: a null arm's verdict is priced by its turnover RATIO to
its comparand, not by whether it was held or re-drawn; below ~1.2x the verdict is
cost-insensitive over the whole 0–25 bps range, and above ~1.4x it is a frictionless-market
statement.**

**SURVIVORSHIP.** B136 and BSTK100 are current constituents, one-directional. The bias runs
**toward the long-hold arms** (a subset held for the sample collects the full survivorship
premium of whatever it drew) and **against the churny ones** (which keep re-entering it).
So the finding that RANDH's breakeven is high and RANDW's is ~1 bp is measured *with* the
bias, and the gap between them should be treated as an **upper bound**; the `RWK` straddle
at 11.4 bps — the one finding that changes a published reading — is the conservative
direction and is the one to trust most. U56 is survivorship-free and shows the same ordering.

**Follow-ups queued:** 268 (price `is-the-book-size-floor-a-corpus-wide-clause_C`'s daily
re-draw and the three NOISE scripts on their own panels and n, the four unpriced verdicts
§3 names), 269 (back-fill the law's four columns over the leaderboard rather than re-running,
since §4 shows a spreadsheet suffices), 267 (the turnover-ratio band 1.2x–1.4x as the
record's rung-sensitivity boundary — pre-register it and test it on non-null arm pairs).
