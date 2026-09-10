# Idea 619 — re-read every published CADENCE verdict against its own PHASE SPREAD (cloud, 2026-09-10)

**Verdict: the queue's premise is CONFIRMED record-wide, and it is worse than idea 220 measured.
83.5% of the record's 158,471 machine-readable cadence effects are smaller than their own phase
band, 92.0% of the 100 STRICT claim files are majority-fragile, and only 6 of 199 cadence-claim
files (3.0%) carry a phase column of their own. KILL of cadence as a tuned parameter: under
PROTOCOL rule 8 no chooser beats the un-dialled weekly incumbent out of sample (REC −0.0197,
2/9 wins; SEL-CP −0.0595; PH-AVG −0.0221). No RULES change, no book promoted, no KEEP claimed;
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py untouched. 4a 7/1188, 4b 0/1188.**

Script `research/backtests/2026-09-10_re-read-every-published-CADENCE-verdict-against-its-own-PHASE-SPREAD_cloud.py`.
Artefacts: `.console.txt`, `.grid.csv` (1,188 arm-rows), `.bands.csv` (7,128 measured phase
bands), `.census.csv` (2,794 files), `.claims.csv` (189,649 claims), `.reread.csv`,
`.summary.csv`, `.wf.csv`.

## What this run is, and how it differs from its parent

Idea 220 (2026-09-06) audited **240** pairwise claims from the **four** corpora whose grid CSV it
could re-run. This run asks the queue's question of the **whole committed record** as it stands
today — every committed CSV under `research/` (2,794 files, 0 unreadable, this run's own
artefacts excluded) — and does not re-run the parents: it extracts each file's **own published
gap** and compares it to a phase band measured here on a pre-registered grid.

**LIMITATION, stated rather than buried.** A claim's phase spread is a property of *its* book on
*its* panel; re-running 199 files' books is not possible in one run. The band each claim is judged
against is measured on this run's 9 (panel × book) cells and matched by cadence pair, metric and
panel where the file names one. It is a **reference** band, not the claim's own. Every headline is
therefore reported at the 25th / 50th / 75th percentile of the band distribution, and the whole
distribution is published in `.bands.csv`.

## Gates (run before any new number was read) — ALL PASS

| gate | result |
|---|---|
| G1 `fast_bt` vs `engine.backtest` at D/W/M/Q, returns **and** turnover, 3 panels | max **6.41e-16** / **1.55e-15** |
| G2 cost-rung identity vs a live 25 bps `engine.backtest` | max **6.41e-16** |
| G3 k=1 phase 0 == `freq='D'`; calendar off=0 == `engine.rebalance_mask` | **0.000e+00**, **0** disagreements at all four cadences |
| G4 idea 412's committed `.phase.csv` rebuilt from source at its raw vintage | u56 **2.220e-16**, broad **2.220e-16**, small **0.000e+00** on the mean; ≤9.71e-17 on the range (bar 1e-9 for broad/small, u56 reported not barred) |

G4 is the load-bearing one: the phase machinery this run judges the record with is the *same*
machinery that produced the number the queue cites, to machine precision, on all three panels.
(Unlike ideas 328/601, u56 reproduces exactly here — the statistic is a within-run spread across
phases, not a half split, so the one extra trading day does not move it.)

## A. The measured phase bands (this run's grid, 10 bps, n_phase = 5)

Sharpe range across phases, mean / max over the 9 (panel × book) cells:

| k (trading days) | ~ | mean SD | mean RANGE | max RANGE |
|---|---|---|---|---|
| 1 | D | 0.0000 | 0.0000 | 0.0000 |
| 2 | 2D | 0.0188 | 0.0265 | 0.0863 |
| 5 | W | 0.0153 | 0.0399 | 0.0896 |
| 10 | 2W | 0.0222 | 0.0564 | 0.1521 |
| 21 | M | 0.0210 | 0.0521 | 0.1192 |
| 30 | 6W | 0.0323 | 0.0785 | 0.2010 |
| 63 | Q | 0.0556 | **0.1481** | **0.3796** |

The **calendar** ladder with a within-block day offset — the record's own convention, where the
phase is "rebalance on the (last − off)-th bar" — reads the same order of magnitude: W 0.0405,
M 0.0490, Q 0.0544 mean range (max 0.1139 / 0.0922 / 0.1261). D has exactly one phase and a range
of exactly zero, which is the whole reason D-pairs survive below.

Phase count is monotone by construction (the sets are nested): mean Sharpe range over the
non-degenerate ladder is **0.0341** at n_phase 2, **0.0524** at 3, **0.0669** at 5.

## B. The census

| | |
|---|---|
| committed CSVs scanned | **2,794** (0 unreadable) |
| STRICT cadence-claim files (cadence-**named** column, cadence vocabulary, plus a metric column) | **157** |
| MED (any column whose **values** are a cadence vocabulary) | **199** |
| of the 199, files carrying a phase / offset column of their own | **6 (3.0%)** |
| pairwise claims extracted from CSVs | **189,627** (STRICT 162,235) |
| LEADERBOARD prose lines quoting a cadence pair and a number (LOOSE rung) | 22 |

**97.0% of the record's cadence-claim files are phase-0 numbers by construction** — they contain
no column that would let a reader check the thing this idea is about.

## C. The re-read — the queue's question, answered

Pre-registered before any number was read: `BAND_UNION = rng(A) + rng(B)` (a phase chooser can
push A up and B down), `BAND_MAX = max(rng(A), rng(B))` (the conservative reading). A claim is
PHASE-FRAGILE if `|gap| < band`.

| n_phase | claim set | n | frag @ p25 | **frag @ p50** | frag @ p75 | frag (BAND_MAX) | median \|gap\| | median band | median ratio |
|---|---|---|---|---|---|---|---|---|---|
| 2 | STRICT | 158,471 | 44.4% | **59.0%** | 72.4% | 53.2% | 0.0112 | 0.0171 | 0.706 |
| 3 | STRICT | 158,471 | 62.5% | **73.6%** | 83.0% | 67.9% | 0.0112 | 0.0333 | 0.385 |
| **5** | **STRICT** | **158,471** | **71.6%** | **83.5%** | **89.7%** | **76.4%** | **0.0112** | **0.0468** | **0.264** |
| 5 | MED | 183,213 | 68.9% | 81.4% | 88.9% | 74.3% | 0.0120 | 0.0433 | 0.294 |
| 5 | LOOSE | 183,235 | 68.9% | 81.4% | 88.9% | 74.3% | 0.0120 | 0.0433 | 0.294 |

**File-weighted (one vote per file, so the handful of 4,000-row grids cannot carry the headline):
median file fragile share 85.7%, and 92 of the 100 STRICT files are majority-fragile.**

**Degeneracy control.** 2.7% of STRICT claims have a gap of *exactly* zero — an inert cadence dial,
trivially fragile. On the 154,152 non-zero claims the fragile share is **83.0%** (median ratio
0.278). The finding is not a zero-gap artefact.

**Every reading of the claim set and of the band agrees**: the smallest number anywhere in the
table — 2 phases, the p25 band, STRICT — is 44.4%, and the queue's own configuration (5 phases,
idea 412's count) is 83.5%.

### Which claims survive: the same split idea 220 found, now over 800× more claims

| pair | ~ | n | fragile | median \|gap\| | median band | ratio |
|---|---|---|---|---|---|---|
| 1–2 | D–2D | 6,375 | **45.9%** | 0.0054 | 0.0021 | 1.226 |
| 1–21 | D–M | 9,768 | **48.0%** | 0.0253 | 0.0252 | 1.086 |
| 1–10 | D–2W | 910 | **50.8%** | 0.0244 | 0.0161 | 0.967 |
| 1–5 | D–W | 21,272 | 69.6% | 0.0092 | 0.0160 | 0.446 |
| 5–10 | W–2W | 2,351 | 79.7% | 0.0096 | 0.0307 | 0.213 |
| 5–63 | W–Q | 21,136 | 87.5% | 0.0166 | 0.0633 | 0.246 |
| **5–21** | **W–M** | **72,494** | **87.5%** | 0.0102 | 0.0468 | 0.230 |
| 5–30 | W–6W | 715 | **93.0%** | 0.0156 | 0.0622 | 0.301 |
| **21–63** | **M–Q** | **24,558** | **94.0%** | 0.0123 | 0.0683 | 0.184 |

Every pair containing **D** — the one cadence point with no phase freedom and a ~10× turnover
difference — sits at 46–70%. Every pair the project has actually argued about (W vs M, W vs 6W,
M vs Q) sits at 87–94%. This is idea 220's conclusion reproduced on the whole record by an
independent route: *the record is right where the answer was never in doubt and fragile
everywhere a cadence constant was being chosen.*

### By metric — the fragility is worst exactly where PROTOCOL rule 4 looks

| metric | n | fragile | median ratio |
|---|---|---|---|
| H2 (second-half Sharpe) | 21,820 | **90.6%** | 0.178 |
| OOS Sharpe | 17,504 | **86.9%** | 0.168 |
| Sharpe | 25,963 | 84.5% | 0.272 |
| MaxDD | 22,842 | 83.1% | 0.302 |
| H1 | 21,855 | 78.2% | 0.330 |
| CAGR | 42,267 | 76.8% | 0.372 |
| OOS CAGR / OOS MaxDD | 30,962 | 76.8% / 76.3% | 0.322 / 0.387 |

The two legs the 4a and 4b predicates turn on — H2 and OOS Sharpe — are the record's **most**
phase-fragile quantities, not its least.

## D. PROTOCOL rule 8 — cadence chosen on 2009–2016, 2017–2026 read exactly once (10 bps)

Four arms on each of the 9 (panel × book) cells. NODIAL spends no parameter.

| arm | mean OOS CAGR | mean OOS Sharpe | mean OOS MaxDD | vs NODIAL | wins |
|---|---|---|---|---|---|
| **NODIAL** (weekly, phase 0 — the incumbent) | **11.90%** | **0.9745** | −22.49% | — | — |
| REC (cadence by IS Sharpe at phase 0 — what the record does) | 11.79% | 0.9549 | −24.00% | **−0.0197** | 2/9 |
| SEL-CP (cadence **and** phase by IS Sharpe) | 11.89% | 0.9150 | −25.04% | **−0.0595** | 4/9 |
| PH-AVG (cadence by IS Sharpe of the phase-averaged blend) | 11.99% | 0.9524 | −24.05% | **−0.0221** | 5/9 (median +0.0062) |

Full-sample means over the same 36 picks: NODIAL CAGR 11.45% / Sharpe 0.9718 / MaxDD −22.49% /
halves 1.064 / 0.906; REC 11.67% / 0.9729 / −24.00% / 1.105 / 0.880; SEL-CP 12.05% / 0.9722 /
−25.04% / 1.152 / 0.842. **Every chooser buys its in-sample H1 with H2 and with drawdown.**

References over the same OOS window: SPY 15.45% / 0.8820 / −33.72%. RULES v2 (live) OOS
u56 9.53% / 1.2851 / −12.05%, broad 7.98% / 1.1185 / −12.24%, small 3.85% / 0.5680 / −14.68%.

**No cadence dial earns its parameter.** The record's cadence "skill" is measured at one arbitrary
phase; let the selector see the phase too and it gets *worse*, not better.

## E. Both KEEP paths, every arm-row

**4a 7 / 1,188 · 4b 0 / 1,188 · BOTH 0 / 1,188** (0 bps 3/396, 10 bps 2/396, 25 bps 2/396).
All 7 4a passers are RULESv2 re-cadencings at **phase 1 or phase 38** — none at phase 0. A phase
is fixed by the sample start date and is **not a tradable choice**, so they are unreachable.
**No KEEP-candidate; nothing promoted.**

## Reading, and what should follow

The queue asked "how many have an effect size below their own phase spread". The answer, on the
strictest claim set and the queue's own phase count, is **83.5% of 158,471 effects, in 92 of 100
files** — and it survives every weakening of the band (44.4% at the harshest), the file-weighted
recount (85.7%), and the removal of inert cells (83.0%). The record's cadence literature is
almost entirely an argument about a quantity smaller than the nuisance parameter nobody priced.

Idea 220 already proposed, report-only, that any future cadence claim quote its phase-averaged
gap and sign share. This run says the cheaper rule is enough and should be the one adopted:
**a cadence claim must quote the number of phases its cadence point admits, or state that the
point has one** (D and any k=1 schedule). That single column would have flagged 97.0% of the
record's cadence-claim files as unaudited at the moment they were filed. **Proposed for Sunday
review, report-only, no RULES change applied here.**

### Caveats
* **Survivorship** (idea 54): u56/B136/SMALL439 are current-constituent lists; SMALL439 drops the
  44 `max_1d_move >= 1.0` tickers before anything runs. No level here is an attainable return; the
  paired comparisons that carry the conclusion are within-panel.
* **The reference-band substitution** (above) is this run's main methodological limitation.
* Idea 38: `data/prices*.csv` are calendar-day indexed after 2014-09-17, so a 1-bar offset on the
  large-cap panels can land on a weekend (a no-op in weights). The large-cap phase ranges are a
  **lower** bound, which biases the fragile share **down** — against this run's own finding.
* All three panels truncated to their common last date 2026-09-04 (idea 328). MaxDD is one number
  off one path (idea 321). 10 bps and t+1 execution throughout.
* The claim extractor reads a file's own committed numbers; it cannot know which rows a file's
  prose actually *argued*. It therefore over-counts (every extractable pair is a "claim"), which
  is why the file-weighted recount is published beside the claim-weighted one.
