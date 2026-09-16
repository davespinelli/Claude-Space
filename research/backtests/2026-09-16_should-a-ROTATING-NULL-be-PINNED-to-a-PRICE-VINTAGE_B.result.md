# Idea 1002 — should a ROTATING NULL be PINNED to a PRICE VINTAGE?

**Lane B, 2026-09-16.** Script `2026-09-16_should-a-ROTATING-NULL-be-PINNED-to-a-PRICE-VINTAGE_B.py`.
Gates **10 of 10 PASS**. Hypotheses **7 of 9**. 2 tuned params (vintage source × panel), every grid
point reported. Rule 8 walk-forward run on all 13 vintages; both KEEP paths evaluated.

## ANSWER — NO. The nightly tape does not RESAMPLE a null, it RE-PRICES it; what needs pinning is the INDEX CONVENTION, not the sha.

**KILL** the queue line's own proposal · **KILL** idea 971's "RESAMPLES" reading of the nightly
ladder · **KEEP** as a PROTOCOL rule-1/rule-4 reporting clause (proposed, **not applied** — rule 6).

### The ladder is real, not simulated
The 11 committed `data/prices.csv` shas and 4 `data/prices_broad.csv` shas were replayed out of git.
Restatement is large in *cells* — **8.91% → 13.68%** of the 4,698 × 56 historical U56 grid is
rewritten between 2026-09-04 and 2026-09-15, max relative move **6.13e-03** — and the panel grows
one row per trading day.

### 1. The tape is 0.5% of a committed null's variance, not a redraw
| panel | arm | σ_seed (coin) | σ_vint (tape) | median ratio | **TAPE SHARE of variance** |
|---|---|---|---|---|---|
| U56 | LIVE | 0.0649 | 4.78e-03 | 0.0696 | **0.0048** |
| U56 | LIVE_CP | 0.0649 | **7.47e-07** | **0.0000** | **0.000000** |
| U56 | PINKEY | 0.0645 | 4.81e-03 | 0.0647 | 0.0042 |
| U56 | PINSET | 0.0649 | 4.92e-03 | 0.0725 | 0.0052 |
| B136 | LIVE | 0.0603 | 6.19e-03 | 0.1236 | 0.0151 |
| B136 | LIVE_CP | 0.0604 | 1.86e-04 | 0.0005 | 0.000000 |

`H_RESAMPLE` **FAILS at 0.0696 against its 0.70 bar**. A committed null OOS Sharpe is **99.5%
coin, 0.5% tape** on U56 (98.5% / 1.5% on B136).

### 2. The mechanism: the coin flip holds the SAME NAMES, only their returns move
Across **42,531** shared decision rows, the U56 pool differs on **0**, the holding count on **0**,
and the drawn **NAME SET on 0 (0.0000%)**. B136 moves on 0.00–0.48%, entirely at weekly cadence.
`LIVE_CP` — the record's own convention with the index truncated to the shared prefix — collapses
σ_vint to **7.47e-07**, so the whole tape term is the APPEND channel (extra days in the OOS window),
not restatement. `H_APPEND` PASS at **6,394x**.

### 3. Pinning buys ~nothing, because there is nothing to pin
`PINSET` (draw the pool and the ranking from a committed sha) is **identical to LIVE** on U56 and
removes only **12.6%** of binding-leg flips — `H_FLIP` **FAILS** against its 0.75 bar. `H_TAPE`
passes at 0.0725, but **vacuously**: every arm carries the same ~7%-of-a-sampling-SD term, so what
it certifies is that the term is small, not that the pin removed it. `H_STALE` 0.0000, `H_BASE`
**18 of 18** published base rates inside 2×MCSE, `H_REAL` worst real-book OOS-Sharpe range
**1.38e-02**, **0 of 18** real 4a or 4b verdicts flip.

### 4. Where 971's 0.254 actually came from — the calendar-day index fix
| channel | max \|dOOS Sharpe\| @ identical seeds | binding-leg flips | 4b verdict flips |
|---|---|---|---|
| whole 9-vintage post-fix ladder | **0.0245** | 0.0167 | 0.0167 |
| SCHEMA BREAK `0ede2282` (calendar index) | **0.3843** | **0.3178** | **0.0800** |
| SCHEMA BREAK `fb208174` | **0.3901** | 0.3156 | 0.0800 |

**15.9x.** 971's reported max \|dSharpe\| **0.254** and **7.4%** REC-4b flips sit inside the schema
band and an order of magnitude above the nightly one. Commit `c006b439` ("Fix calendar-day index
bug") is a **one-off index-convention change**, not a restatement — the thing to pin is the index
convention.

### 5. A committed artifact's own numbers already name its tape
Idea 975-B's committed `.real.csv` CANON rows reproduce at machine epsilon (2.22e-16) on exactly
one vintage per panel — U56 `868b5c36`, B136 `56e08b10` — and are off by **1.80e-03 to 2.05e-02**
on all 11 others. No committed artifact in this record names its price sha; every one of them
could.

### 6. Rule 8 (PROTOCOL rule 8) — OOS 4b **9 of 39**, OOS 4a **0 of 39**
All 6 (panel, chooser) picks are vintage-invariant (`H_RULE8` PASS). The only 4b pass is U56
`C_ISCAGR` → **TOP20/M**, on all 9 vintages:

> OOS **16.68% / 1.2833 / −19.51%** (binds nothing) vs SPY OOS **15.21% / 0.8713 / −33.72%** and
> RULES v2 OOS **9.45% / 1.2757 / −12.05%**; 0.99 percentile of its own gross-matched null.

This is the record's **existing** TOP20/M object reached from a different direction, not a new
candidate, and it **fails 4a** (MaxDD −19.51% against the live book's −12.05%). 4a is 0 of 39 at
10 bps and 13 of 117 only at 0–5 bps. Not a KEEP from this run.

### PROPOSED CLAUSE (rule 6 — proposed, NOT applied)
> *Every committed null states the sha of the price file it was drawn on and the INDEX CONVENTION
> of that file (trading-day or calendar-day). A null is re-priced against a new vintage without
> re-drawing; a change of index convention invalidates the draw and the null is rebuilt. Any claim
> that a tape moved a null reports the move beside the null's own cross-seed SD, and calls it a
> RESAMPLE only when the drawn name set changed.*

### Survivorship (PROTOCOL rule 9)
U56 and B136 are current-constituent lists, so every CAGR and drawdown LEVEL is optimistic. The
measured object is a VARIANCE RATIO between two readings of the same panel on the same tape, so the
bias largely cancels; where it does not it works **against** this run — a survivor panel's
eligibility gate is more stable than a real-time one's, so the tape term reported here is a LOWER
bound and `H_TAPE` was the easier hypothesis to pass.

### Provenance note
`H_SCHEMA` was added after a 3-vintage smoke run showed the post-fix ladder nearly inert, and was
registered with its 10.0x bar **before** either schema-break vintage was priced. It is a
POST-SMOKE hypothesis and is labelled as one in the script header and everywhere it appears.
