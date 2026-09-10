# Idea 660 — is the KEY-UNIQUE join STABLE under float reformatting?

**cloud, 2026-09-10 · KILL for capital, ANSWERED for the record · premise CONFIRMED, and the answer is worse than the queue guessed**

Script: `2026-09-10_is-the-KEY-UNIQUE-join-STABLE-under-float-reformatting_cloud.py` (305 s, deterministic, no network).
Artefacts: `.grid.csv` (15) `.transition.csv` (5) `.instances.csv` (251) `.books.csv` (264) `.walkforward.csv` (12) `.keeppaths.csv` `.console.txt`.
**No RULES change, no book promoted, no KEEP claimed, no memo.** RULES.md, PROTOCOL.md, scan.py, bot.py, baseline.py untouched.

## Gates (all PASS, run before any new number was read)

| gate | result |
|---|---|
| G1 `fast_backtest` == `engine.backtest` (RULES v2, 0 bps, from warm-up) | **1.388e-17** |
| G2 cost-rung identity `r(25) = r(0) − turn·25/1e4` vs a live `engine.backtest(25)` | **1.388e-17** |
| G3 the ranking machinery reproduces `baseline.rules_v1_weights` | **0.000e+00** |
| G4 pointer-form ladder nested (STRICT ⊆ LOOSE ⊆ VALUE) | PASS (198/233/251 instances, 963,128/1,085,626/1,089,479 rows) |
| G5 dp-invariant outcomes (NOKEY/SINGLE/NONROW/UNRES) identical at all 5 rungs | PASS |
| G6 every row classified at every rung (row totals equal) | PASS (1,089,479 rows) |

**Provenance / drift note (reported, not hidden):** the corpus now carries idea 655's own committed
outputs, so the population is **251 instances / 1,089,479 pointer rows** against 655's published
246 / 1,088,554, and the dp=10 KEY-UNIQUE count is **198,267** against its published **198,353**
(−86, i.e. 655's count folded in the 88 `SINGLE`-source rows this run reports in their own column).
Every share below is computed inside this run; the two are not mixed. A census whose corpus contains
its own artefacts is not re-runnable to the digit — that is a property of this whole census family,
not of this run.

## (1) The ladder — the record's rounding is not a tie-breaker, it is a TOLERANCE

All 15 grid points are in `.grid.csv`. FORM = VALUE (the full population):

| dp | KEY-UNIQUE | share | AMBIG | MISS |
|---|---|---|---|---|
| 6 | 198,018 | 0.1818 | 287,787 | 146,047 |
| 8 | 198,245 | 0.1820 | 287,560 | 146,047 |
| **10 (the record's own)** | **198,267** | **0.1820** | 287,538 | 146,047 |
| 12 | 198,165 | 0.1819 | 287,530 | 146,157 |
| **FULL (no rounding)** | **33,960** | **0.0312** | 261,406 | **336,486** |

Same shape at STRICT (0.1214/0.1216/0.1216/0.1216 → **0.0351**) and LOOSE. **Between 6 and 12 decimal
places the answer does not move — and then it falls by 5.8×.** The record's readability is not
sitting on a plateau that happens to include 10; it is sitting on the *only* plateau there is, and
the plateau is the rounding itself.

## (2) The answer — 83% of idea 655's addressable rows are a formatting accident

Population = the **198,267** rows KEY-UNIQUE at the record's own rung (dp=10, VALUE), tracked row by row:

| rung | still UNIQUE | became AMBIG | became MISS | kept |
|---|---|---|---|---|
| dp6 | 198,018 | 249 | 0 | 0.9987 |
| dp8 | 198,245 | 22 | 0 | 0.9999 |
| dp10 | 198,267 | — | — | 1.0000 |
| dp12 | 198,157 | 0 | 110 | 0.9994 |
| **FULL** | **33,830** | **0** | **164,437** | **0.1706** |

**UNIQUE at all five rungs: 33,636 — 16.97% of the population.** The failure is one-sided and that is
the diagnosis: coarsening loses rows to **AMBIG** (249 at dp6 — over-merging, the expected failure
mode), but refining loses them to **MISS**, 164,437 of them, with **zero** going ambiguous. A key that
misses at full precision and hits at 10 dp is not a key; it is a *fuzzy match*. The child and the
source do not hold the same number — they hold numbers that agree to about ten decimals — and
`round(float(x), 10)` is the tolerance that hides the disagreement.

So idea 655's headline survives only in the weak form: **18.22% of pointer rows are row-addressable
if you accept a 1e-10 tolerance, and 3.12% are addressable on the numbers as written.** Of the
959,393 at-risk rows (source CSV has many rows), the genuinely dark count at full precision is
261,406 AMBIG + 336,486 MISS + 327,541 NOKEY = **925,433 rows, 84.94% of the pointer population** —
against the 760,321 (69.8%) idea 655 counted at dp=10.

## (3) The live leg — does a BOOK survive reformatting its own ranking key?

The same question priced: round the composite score (no vol scaler) to `dp` decimals, hold the top `n`
equal-weight at gross 1.00, weekly. Two tuned dials (dp, n); panel, tie handler and cost rung reported
at every one of **252** points (`.books.csv`).

**The book is precision-sensitive, and far more so than the join.** Sharpe spread across the dp ladder
at 10 bps: U56 0.0162 (SPREAD n=20) to 0.1158 (SPREAD n=5); B136 0.0424–0.1075; **SMALL439 0.1978 to
0.6561** (ALPHA n=5 spans Sharpe 0.0704–0.7264 and CAGR −2.53%..+24.60%). Rounding a percentile-rank
composite to 1 decimal is a *different book*, not a rounded one — and on the thin panel it is the
difference between a 24.6%/yr book and a losing one.

Rule 8 — (dp, n) chosen on 2009–2016 by IS Sharpe, 2017+ read once (all 12 in `.walkforward.csv`):

| panel | rung | tie | pick | OOS CAGR | OOS Sharpe | OOS MaxDD | beats SPY OOS | beats v2 OOS |
|---|---|---|---|---|---|---|---|---|
| U56 | 10 | ALPHA | dp2, n=5 | 29.67% | **1.014** | −36.53% | yes | no |
| U56 | 10 | SPREAD | **FULL**, n=5 | 30.87% | **1.051** | −36.53% | yes | no |
| U56 | 25 | ALPHA | dp4, n=5 | 26.79% | 0.939 | −36.55% | yes | no |
| U56 | 25 | SPREAD | **FULL**, n=5 | 26.71% | 0.943 | −36.55% | yes | no |
| B136 | 10 | ALPHA | dp1, n=5 | 26.42% | 0.878 | −37.81% | no | no |
| B136 | 10 | SPREAD | **FULL**, n=10 | 20.93% | 0.847 | −33.52% | no | no |
| B136 | 25 | ALPHA | dp1, n=5 | 21.07% | 0.746 | −40.53% | no | no |
| B136 | 25 | SPREAD | **FULL**, n=10 | 17.06% | 0.725 | −34.67% | no | no |
| SMALL439 | 10 | ALPHA | dp1, n=20 | 17.29% | 0.691 | −40.41% | no | yes |
| SMALL439 | 10 | SPREAD | dp2, n=10 | 18.71% | 0.657 | −44.86% | no | yes |
| SMALL439 | 25 | ALPHA | dp1, n=20 | 12.90% | 0.561 | −47.50% | no | yes |
| SMALL439 | 25 | SPREAD | dp2, n=10 | 13.78% | 0.539 | −52.36% | no | yes |

References @10 bps — U56: SPY 15.15% / 0.8855 / −33.72% (H 0.9587/0.8257, OOS Sharpe 0.8758),
RULES v2 8.63% / 1.2021 / −12.05% (OOS 1.2788). B136: SPY 15.23% / 0.8890 / −33.72% (OOS 0.8820),
v2 8.03% / 1.1058 / −12.24% (OOS 1.1185). SMALL439: SPY 14.13% / 0.8615 / −33.72% (OOS 0.8820),
v2 3.81% / 0.5725 / −14.68% (OOS 0.5680).

**KEEP paths over all 252 points: 4a 0/252, 4b 0/252, BOTH 0/252** (0/84 on each panel).
Nothing is close: 4a dies on the MaxDD leg (every top-n book runs −27% to −52% against the live
book's −12%), and 4b dies on the same leg (cap = 60% of SPY's −33.72% = **−20.23%**) *before* the
Sharpe legs are read. The two U56 rule-8 picks that beat SPY's OOS Sharpe (1.014 and 1.051 vs 0.876)
both draw down −36.5%. The best full-sample point on the whole grid — U56 ALPHA dp0 n=20, Sharpe
1.2294 (H1 1.285 / H2 1.199), CAGR 21.9%, MaxDD −27.84% — still misses the cap by 7.6 pp.

## Verdict

**KILL for capital, ANSWERED for the record.** The queue's suspicion is confirmed and then some:
**only 16.97% of the record's key-unique pointer rows stay unique when the rounding is removed**, and
the 83% that do not are lost to MISS, not to ambiguity — meaning `round(float(x), 10)` was never
disambiguating a key, it was tolerating a mismatch. Any published claim that quotes a re-read row
through a shared-column value key is quoting a 1e-10 fuzzy match. The live twin of the question is a
cleaner KILL: the precision dial moves a book's Sharpe by up to 0.66, so a rounded ranking key is a
different book — but every one of the 252 books it produces fails both KEEP paths on drawdown.
