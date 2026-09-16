# Idea 1001 (lane B, 2026-09-16) — is every committed 4b SHARPE LEG just the BENCHMARK'S OWN LUCK in that window?

**ANSWERED = NO ON THE RECORD'S OWN READING FRAME, AND YES ON RULE 8's. 971's DIAL IS THE WINDOW
*END*, NOT THE WINDOW *START*: ON THE FULL TAPE SLIDING THE START MOVES SPY'S `L_H1` BAR BY 0.1975
AND FLIPS 0 OF 9 COMMITTED PASSES; INSIDE THE IS-ONLY WINDOW THE SAME STARTS MOVE IT BY 1.0717 AND
COST 7 OF THOSE 9 THEIR `L_H1`.**

**But the leg is not certifiable either way, and that is the durable result: 0 of 9 committed
passes — and 0 of 36 control books, at every window — clear the benchmark's OWN sampling noise on
BOTH Sharpe legs.**

Gates **6 of 6 PASS** (G1 all 9 SHELF memo triples; G2 fast runner ≡ `engine.backtest` 6.94e-18;
G3 SPY 0.1510 / 0.8829 / −0.3372 vs committed 0.1513 / 0.886 / −0.3372; G4 971's table re-read on
both sets and printed, not assumed; G5 COUNT halves ≡ `baseline._row` at 0.00e+00; G6 bootstrap
determinism 0.00e+00).

Two tuned dials, **all points reported**: CLAIM SET {SHELF (9 committed memo-backed 4b passes),
GRID (36 never-selected ladder books)} × WINDOW GRID {START5 = 971's own five starts, START9 =
the mid-years added}. The comparand convention {LIVE, FULL, POOL, MAX} is the **measured axis**,
not a dial; cost rung {0, 10, 25} bps is a reported control and 10 bps is PROTOCOL's headline.

## KILL 1 — the queue's hypothesis fails on the record's own convention (`H_LUCK` FAIL at 0 of 9)

BENCHLUCK = a book that clears BOTH Sharpe legs against the record's own comparand (SPY's realised
Sharpe in that exact half) and fails at least one once the comparand is made **window-invariant**.

| comparand | SHELF 0 bps | SHELF 10 bps | SHELF 25 bps | GRID 10 bps |
|---|---|---|---|---|
| LIVE (the record's) — passes | 9 of 9 | 9 of 9 | 9 of 9 | 34 of 36 |
| FULL (SPY's full-sample Sharpe, both halves) — BENCHLUCK | **0** | **0** | 1 (`b136-r620`, `m2_FULL` −0.0522) | **0** |
| POOL (median SPY half bar over the grid) — BENCHLUCK | 0 | 0 | 1 | 0 |
| MAX (max SPY half bar over the grid) — BENCHLUCK | 0 | 1 (`u56-top20-band-m20`) | 5 | 6 |

The bar was ≥ 1/3. At PROTOCOL's own 10 bps the answer is **zero**: every committed pass clears a
comparand that has no window in it at all. The MAX column is the only one that bites, and MAX is
a deliberately unfair bar (SPY's best half over five windows, 1.1012 / 0.8486 on U56).

## KILL 2 — and the moving side is the BOOK, not the benchmark (`H_COMP` FAIL)

`d margin = d(book half Sharpe) − d(SPY half Sharpe)` exactly, so each window step attributes.
Median over the SHELF of the across-window sd, START5, 10 bps:

| half | sd(book) | sd(SPY) | comparand carries |
|---|---|---|---|
| H1 | 0.0873 | 0.0941 | **7 of 9** books |
| H2 | 0.0436 | **0.0118** | **0 of 9** books |
| pooled | **0.0659** | 0.0523 | — |

971's reading transfers to H1 and **inverts on H2**, where SPY's bar is nearly frozen (0.8207 →
0.8486 over five starts) while the books' second halves move four times as much. `H_CORR` also
fails, at **−0.6878** against a −0.70 bar (971 got −0.957 on its synthetic grid); `r_leg2_spyH2`
is undefined because the H2 leg passes at **every** window on both sets — zero variance to
correlate. On the wider START9 grid the correlation decays further, to −0.4847.

## THE MECHANISM — 971's number is a WINDOW-*END* object, and it is real where rule 8 reads

971 read its halves inside the IS-only window `[w, 2016-12-31]`. The record reads them on the full
tape `[w, 2026-09-15]`. Same starts, same books, same COUNT half rule:

| reading frame | SPY `L_H1` bar range | ptp | SHELF two-leg pass rate |
|---|---|---|---|
| FULLTAPE (the record's) | 0.9037 … 1.1012 | **0.1975** | 1.0000 … **0.8889** |
| ISEND2016 (971's, = rule 8's IS window) | 0.8052 … **1.8768** | **1.0717** | 1.0000 … **0.2222** |

**5.43×** on the bar. 971's published 0.838 → 1.877 reproduces here at 0.8052 → 1.8768 — on the
IS-end frame only. At `w=2012` inside that frame the committed shelf's median `L_H1` margin is
**−0.1349** and **7 of the 9 committed passes lose the leg**; on the full tape the same start
costs one book. The window start is not the free parameter 971 named it; the pair (start, **end**)
is, and the end is exactly what PROTOCOL rule 8 fixes at 2016-12-31 for every IS-only chooser.

## KEEP (clause, proposed — NOT applied, rule 6) — the benchmark-noise disclosure (`H_NOISE` PASS)

Even at a frozen window, SPY's half Sharpe is **one draw**. Stationary block bootstrap of SPY's own
half-window returns (1,000 draws, expected block 21d, seed 1001) gives SE **0.2877** (H1) and
**0.3350** (H2) on the U56 tape. Against that:

- SHELF HALFMIN (the weaker of a book's two legs) median **0.2102** Sharpe units, min 0.1299, max
  0.3264 — **below** the comparand's own SE of 0.3008. Bar was "below 1 SE": **PASS**.
- **13 of 18** passing SHELF legs sit inside 1 SE, at the record window and at every other
  (12–14 of 18 across all nine windows).
- **0 of 9 SHELF books and 0 of 36 GRID books clear 1 SE on BOTH legs — at every one of the five
  windows. 0 of 45 at 2 SE.** Median min-leg, in SE units: SHELF 0.68 / 0.55 / 0.59 / 0.39 / 0.64.

So the two Sharpe legs, as PROTOCOL writes them, are a **point comparison against a noisy
comparand**, and no book in the record — committed or control — has ever cleared them by more than
the comparand's own sampling error. That is not an argument for dropping the legs (they are
directionally right, 9 of 9 and window-stable on the full tape); it is an argument that a 4b pass
**must not be quoted as though the legs were certified**. Exact wording in the memo.

## Rule 8 (required) — 24 picks, OOS read once, and the contamination stated

Dial chosen on 2009-2016 **alone**; OOS 2017-2026 read once per (panel × chooser {CH_SHARPE,
CH_CAGR, CH_MARGIN} × screen {PLAIN, FULLCOMP} × pool {ALL, GRIDONLY}).

- **ALL pool: OOS 4b 12 of 12 — and it is worthless.** The ALL pool contains the memo-selected
  SHELF, chosen with full-sample information; every one of those 12 picks is `u56-quantile50-
  respread-M` or `b136-r620-gross065-W`, books that were 4b passes before the chooser saw them.
  Reported, and discarded as evidence.
- **GRIDONLY (the clean read): OOS 4b 9 of 12, OOS 4a 0 of 12**, eight distinct picks.
- Best clean pick — U56 / `CH_SHARPE` / **FULLCOMP** → `U56-band0.03-g1.00`:
  **OOS 12.67% / 1.2755 / −15.91%** vs **SPY OOS 15.21% / 0.8711 / −33.72%** and **RULES v2 OOS
  9.45% / 1.2762 / −12.05%**. Passes 4b out of sample; **fails 4a** on drawdown (−15.91% against
  the live book's −12.05%).
  This is **not a new candidate** — it is the same U56/`BAND03` book ideas 971, 972 and 997 already
  published, reached from a fourth direction. **PARK.**
- The FULLCOMP screen (require the legs to clear SPY's window-invariant full-sample Sharpe in
  sample too) shrinks the U56 pool 7 → 3 and does **not** cost OOS Sharpe: 1.1615 → 1.2755 on
  `CH_SHARPE`. `H_WF` **PASS** (11 of 12 FULLCOMP picks clear 4b OOS; 5 of 6 on GRIDONLY).
  A reporting requirement that is free, not an alpha filter — which is what the clause claims.

## Hypotheses as pre-registered

| name | bar | got | verdict |
|---|---|---|---|
| `H_LUCK` | ≥ 1/3 of SHELF two-leg LIVE passes fail under FULL | 0 of 9 = 0.0000 | **FAIL** |
| `H_CORR` | Pearson(SHELF two-leg rate, SPY mean bar) ≤ −0.70 | −0.6878 | **FAIL** |
| `H_COMP` | median sd(SPY half) > median sd(book half) | 0.0523 vs 0.0659 | **FAIL** |
| `H_NOISE` | median SHELF HALFMIN < 1 bootstrap SE of SPY's half Sharpe | 0.2102 vs 0.3008 | **PASS** |
| `H_WF` | a FULLCOMP-screened IS-only chooser picks a 4b OOS pass | 11 of 12 | **PASS** |

Three of five pre-registered bars fail. They are reported here as loudly as the two that pass.

## Survivorship

U56 and B136 are **current-constituent** panels, so the BOOK side of every margin is optimistic:
names that went to zero are absent. The measured objects are (i) a margin against SPY and (ii) that
margin's movement across windows, both computed on the same biased panel. Survivorship inflates
the book side, which pushes margins **up** — i.e. it works AGAINST `H_LUCK`, `H_CORR` and
`H_NOISE`, the three this run tested. The 0-of-45 noise result is therefore a **lower** bound on
how uncertifiable the legs are, not an upper one. SPY itself is a real index series and is not
subject to the panel's bias.

## Artifacts

`2026-09-16_is-every-committed-4b-SHARPE-LEG-just-the-BENCHMARK-S-OWN-LUCK-in-that-window_B.py`
(deterministic, seed 1001, 21s, committed caches only — no network, never yfinance), with
`.console.txt`, `.census.csv` (1,215 book × window × rung rows), `.benchluck.csv` (108),
`.reconcile.csv` (20), `.decomp.csv` (180), `.noise.csv` (810 leg rows in SE units),
`.outsidenoise.csv` (10), `.walkforward.csv` (24),
`.hypotheses.csv`, `.gates.csv`. Nothing in `RULES.md`, `PROTOCOL.md`, `scan.py`, `bot.py` or
`baseline.py` was modified; the clause below is **proposed, not applied** (rule 6).
