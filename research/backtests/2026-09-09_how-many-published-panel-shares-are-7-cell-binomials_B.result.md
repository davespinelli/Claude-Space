# Idea 290 (lane B) — how many published panel shares are 7-cell binomials?

**ANSWERED / KILL.** The census answers the queue's question with a number; the rule the
census implies is then tested with real money on the line and **kills itself** — the
noise bar collapses to "do nothing", which is exactly what it should do and exactly why
it is not a new book. No KEEP candidate, no memo, no RULES change. `RULES.md`,
`PROTOCOL.md`, `scan.py`, `bot.py` and `baseline.py` untouched.

Script: `2026-09-09_how-many-published-panel-shares-are-7-cell-binomials_B.py`
Artefacts: `.console.txt`, `.shares.csv.gz`, `.orderings.csv`, `.census_grid.csv`,
`.arms.csv`, `.walkforward.csv`.

Two tuned parameters and only two, shared by both halves: the **cell cap / cell count**
(`nmax` in the census, `m` in the live test) and the **noise bar `alpha`**. All 36
census grid points and all 72 selector grid points are reported.

---

## Reproduction gate (4/4 PASS, before any new number)

Recomputed from idea 277's own committed `panelshare.csv`:

| quantity | recomputed | published | |
|---|---|---|---|
| within-rung seed sd | 0.2641 | 0.2641 | OK |
| between-rung sd | 0.1419 | 0.1419 | OK |
| ETF36 share | 0.2857 = **2/7** | 2/7 | OK |
| 7-cell binomial floor 0.5/√7 | 0.1890 | 0.1890 | OK |

By-product worth stating: idea 277's seed sd is **1.397×** the mechanical 7-cell floor,
i.e. the seed noise is *larger* than the most a 7-cell binomial can be — the reversal
share carries panel-construction variance on top of cell noise, not instead of it.

## A. The census — the queue's question, answered

Sources: 866 published files (`research/backtests/*.result.md`, `*.console.txt`,
`CHANGELOG.md`, `LEADERBOARD.md`, `QUEUE.md`). **10,518** `k/n` share tokens at n ≤ 15,
**7,788** at n ≤ 10, **749** at exactly 7 cells (9.6% of all n ≤ 10 tokens).

A **panel ordering** = two shares with *different* values inside one published sentence
that names ≥ 2 distinct panels. (Sentence, not physical line: a CHANGELOG entry is one
multi-kilobyte line, and pairing every share on it would invent contrasts nobody made.)
That yields **471 occurrences → 332 DISTINCT claims** — the record restates the same
claim in `console.txt`, `result.md` and `CHANGELOG.md`, and every count below is on
distinct claims. Each is tested with a **two-sided Fisher exact** test (exact, not a
normal approximation — that is the whole point at n ≤ 10).

### HEADLINE, at the queue's own cap (n ≤ 10) and the conventional bar (α = 0.05)

> **40 of 244 distinct published panel orderings survive their own sampling noise
> (16.4%). 204 (83.6%) do not.** Median Fisher p **0.444**; median published gap **0.387**.

The reason is mechanical, not rhetorical. The **minimum detectable share gap** between
two n-cell shares under a two-sided Fisher exact:

| n | α=0.01 | α=0.05 | α=0.10 | α=0.20 | α=0.32 | α=0.50 |
|---|---|---|---|---|---|---|
| 5 | 1.000 | 0.800 | 0.800 | 0.600 | 0.600 | 0.400 |
| 7 | 0.857 | **0.714** | 0.571 | 0.429 | 0.429 | 0.286 |
| 8 | 0.750 | 0.625 | 0.500 | 0.500 | 0.375 | 0.250 |
| 10 | 0.700 | **0.500** | 0.400 | 0.400 | 0.300 | 0.200 |
| 12 | 0.583 | 0.417 | 0.333 | 0.333 | 0.250 | 0.167 |
| 15 | 0.467 | 0.333 | 0.267 | 0.267 | 0.200 | 0.133 |

A 7-cell ordering needs a gap of **0.714 (5 of 7 cells)** to be callable at α=0.05. The
record's median 7-cell gap is **0.286 (2 of 7)** — a factor of 2.5 below the floor. 7 is
also the record's *modal* cell count for panel orderings (186 of 488 share-slots at
n ≤ 10; then 6:97, 8:52, 9:32, 5:30, 3:25, 2:22, 4:22, 10:22).

### The full 6 × 6 grid (all points; distinct claims)

| nmax | orderings | survive @0.01 | @0.05 | @0.10 | @0.20 | @0.32 | @0.50 | median p |
|---|---|---|---|---|---|---|---|---|
| 5 | 30 | 0 (0.0%) | 1 (3.3%) | 1 (3.3%) | 7 (23.3%) | 8 (26.7%) | 17 (56.7%) | 0.456 |
| 7 | 174 | 17 (9.8%) | 25 (14.4%) | 49 (28.2%) | 82 (47.1%) | 83 (47.7%) | 114 (65.5%) | 0.437 |
| 8 | 214 | 22 (10.3%) | 31 (14.5%) | 58 (27.1%) | 97 (45.3%) | 101 (47.2%) | 137 (64.0%) | 0.444 |
| **10** | **244** | 28 (11.5%) | **40 (16.4%)** | 68 (27.9%) | 109 (44.7%) | 116 (47.5%) | 153 (62.7%) | **0.444** |
| 12 | 295 | 41 (13.9%) | 64 (21.7%) | 96 (32.5%) | 138 (46.8%) | 148 (50.2%) | 191 (64.8%) | 0.315 |
| 15 | 332 | 49 (14.8%) | 73 (22.0%) | 110 (33.1%) | 154 (46.4%) | 169 (50.9%) | 213 (64.2%) | 0.304 |

**The verdict is not "it is all noise."** Survival at α=0.05 (16.4%) is *above* the 5% a
pure null would deliver — excess **+0.114** — and the excess is positive at 32 of the
36 grid points; the four negatives all sit at nmax=5, where the denominator is 30 and
no gap below 0.800 is callable at α=0.05 at all. Some published panel
orderings are real. But (a) the survival rate is itself flattered, because the record
preferentially *writes down* the wide gaps, and (b) at the record's own modal cell count
the typical claim sits below the detectability floor, so **the ordering is unfalsifiable
on its own cells regardless of which way it points.** The monotone rise in survival with
`nmax` (16.4% → 22.0% from 10 to 15 cells) is the same statement from the other side:
what the record can defend is a function of how many cells it happened to run.

Widest published gaps that **still** fail at α=0.05 (verbatim from the record):

- `3/3 vs 0/3` gap +1.000, p 0.100 — *"The 1-week fill kills F085 on B136 only … 3/3 passing cells → 0/3"* (CHANGELOG:73)
- `6/7 vs 0/2` gap +0.857, p 0.083 — *"at g=1.00 the informative cells widen 0/3 (U56) and 0/2 (B136)"* (CHANGELOG:292, LEADERBOARD:3428, QUEUE:242)
- `2/2 vs 2/7` gap +0.714, p 0.167 — *"only 2 of 7 broad bars failing at 25 bps already fail at 0 bps (u56 2/2, small 6/8)"* (CHANGELOG:42)

These are honest claims that happen to be uncallable, not sloppy ones. That is the point.

**Method limits, stated:** the extractor is a regex heuristic over prose. It cannot tell
a share from a ratio, it treats a sentence as a claim, and it can pair two shares that a
human reader would not have contrasted. It over- rather than under-counts orderings, so
the 83.6% failure rate is an estimate, not an audit.

## B. Does the noise bar pay? (rule 8 — chosen on 2009–2016, judged on 2017–2026 untouched)

A census earns a PROTOCOL line only if acting on it beats not acting. Three panels
(U56 56 names, B136 136, SMALL 440 sub-$2B), 10 arms each (band dial 0.00–0.12 on the
RULES v2 form, rank dial n=3/5/8/12 on the v1 form), weekly, 10 bps, t+1. Each arm is
scored by **the share of m in-sample sub-windows in which it beats the live baseline** —
a k/m share with m ≤ 10, exactly the published statistic under audit. Three selectors:

- **S_NAIVE** — argmax share.
- **S_NOISE** — argmax *only if* its Fisher-exact lead over the runner-up clears α, else the live constant.
- **S_CONST** — always the live constant (band 0.03), the do-nothing control.

72 cells = 3 panels × 4 m × 6 α, **all reported** in `.walkforward.csv`. OOS mean:

| | OOS Sharpe | OOS CAGR | OOS MaxDD |
|---|---|---|---|
| S_NAIVE | 0.9697 | 7.26% | −14.38% |
| S_NOISE | **0.9903** | 7.12% | −13.01% |
| S_CONST | 0.9894 | 7.11% | −12.99% |
| SPY | 0.8809 | 15.43% | −33.72% |

- **NAIVE − CONST: −0.0197** Sharpe (pooled t −2.33, wins 30/72) — the raw small-cell share
  selector is *worse than doing nothing*, and buys +0.15 pp of CAGR for +1.4 pp of drawdown.
- **NOISE − CONST: +0.0009** (t +1.00) — the bar **fired in 1 of 72 cells**. It is a
  do-nothing rule with one exception.
- **NOISE − NAIVE: +0.0207** (t +2.46, wins 42/72).

**Those pooled t's are overstated and I am not leaning on them.** The 72 cells are 3
panels × near-duplicate m/α, so the effective sample is **3**:

| panel | NAIVE − CONST | NOISE − CONST | S_NAIVE picked | fired |
|---|---|---|---|---|
| U56 | **−0.1099** | +0.0000 | band0.08, band0.12 | 0/24 |
| B136 | **−0.0110** | +0.0000 | band0.02, band0.08, band0.12 | 0/24 |
| SMALL | +0.0617 | +0.0028 | band0.05, band0.12 | 1/24 |

2 of 3 panels negative for the naive share, 1 positive. **The correct reading is that the
small-cell share is not a usable selector in either direction, and the binomial bar's
whole contribution is to notice that and abstain.** This is the record's recurring
do-nothing-wins result reached by a new route, not a new edge.

## Both KEEP paths (PROTOCOL rule 4, full sample; 4b's OOS leg = rule 8)

| | count |
|---|---|
| 4a vs a **per-panel** restatement of RULES v2 | 1 / 30 |
| 4a vs **the actual live book** (RULES v2 on U56) — the binding comparand | **0 / 30** |
| 4b vs SPY (Sharpe both halves **and** OOS, MaxDD ≤ 60% SPY, CAGR ≥ 70% SPY) | **0 / 30** |
| both | **0 / 30** |

Selector books: S_NAIVE 4a(live) **0/72**, 4b **0/72**; S_NOISE 4a(live) **0/72**, 4b **0/72**.

The one per-panel 4a passer is `SMALL band0.05` (4.2% / 0.618 / −14.6%, halves
0.638/0.603, OOS 4.2%/0.613/−14.6% against SMALL's own band-0.03 baseline
0.570/0.577/−14.7%). Against the *live* book (U56 RULES v2, 8.6% / 1.204 / −12.1%,
halves 1.231/1.183) it fails both Sharpe legs by a wide margin, so it is **not** a 4a
pass under PROTOCOL rule 4 as written. Reported both ways rather than quietly picking
the flattering comparand. 4b is 0/30 because every band book earns ~4–9% CAGR against
SPY's 15.2% — the CAGR floor binds before anything else.

SURVIVORSHIP: B136 and the sub-$2B panel are current constituents only (PROTOCOL rule 9).

## What the record should take from this

1. **40 of 244 (16.4%).** That is the answer to the queue's question, at its own cap and
   the conventional bar.
2. A 7-cell ordering is **uncallable below a 5-of-7 gap**; the record's median 7-cell gap
   is 2-of-7. Publishing `(k, n, Fisher p)` instead of a bare share costs one column and
   makes the difference visible.
3. Acting on the finding is worth **nothing** — the bar abstains 71 times in 72 and gains
   +0.0009 OOS Sharpe. It is a reporting discipline, not a book.
