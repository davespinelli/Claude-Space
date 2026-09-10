# Idea 623 — does a TERMINAL-DATING certificate belong BEFORE rule 8? (lane B, 2026-09-10)

**Verdict: ANSWERED / SPLIT — YES a certificate belongs before rule 8, and NO the T1 family is not
it.** T1 is a perfect SCALE detector and misses 7 of 10 terminal-dated keys, the pure oracle
included; the DATING certificate written here catches 10 of 10 with zero false positives; and
neither one alone cleans the rule-8 pick — only the conjunction does. **No KEEP, no book promoted,
no RULES change.** `RULES.md`, `PROTOCOL.md`, `scan.py`, `bot.py` and `baseline.py` untouched.

## 1. Gates (four, pre-registered, all PASS)
| gate | result |
|---|---|
| G1 `fast_backtest` == `engine.backtest`, control book, evaluation window | returns **1.388e-17**, turnover **3.331e-16** (tol 1e-12) |
| G2 rung identity `r(c) = r(0) − turnover·c/1e4` vs a live 25 bps engine run | **1.388e-17** |
| G3 idea 195's committed headline MCAP/NEG/m=1.00 @10bps re-derived | **5.551e-17** — 20.29% / 1.374 / −24.87%, digit for digit (tol 5e-3) |
| G4 both certificates clear a causal scale-free control key at tol 0 | T1 med **0.000**, T2 med **0.000** |

G1/G2 are read on the evaluation window: the engine emits NaN on the two pre-first-rebalance rows
of this panel, which no published metric reads. Shares come from idea 195's **pinned** snapshot
artefact, not the nightly file (idea 565).

## 2. The instrument — the two certificates are exactly complementary, not substitutes
20 keys, ground truth hand-derived from the algebra on two independent axes. T1 = idea 433's
recommended value certificate under `px → px·diag(c)`. **T2 = truncation invariance (new here):
`key(inputs)[t]` must equal `key(inputs truncated to ≤ t)[t]`, and truncation applies to EVERY
input — an exogenous series passes through only if its own as-of date is ≤ t.**

| instrument | vs SCALE leak | vs TERMINAL dating |
|---|---|---|
| **T1** (scale) | TP 7 · FP 0 · FN 0 · TN 13 — **perfect** | TP 3 · FP 4 · **FN 7** · TN 6 |
| **T2** (dating) | TP 3 · FP 7 · FN 4 · TN 6 | TP 10 · **FP 0 · FN 0** · TN 10 — **perfect** |

**T1's seven false negatives are the whole point: FWDRET, TERMREB, MCAPREB, SHARES, FULLVOL,
FULLSHRP, MAXMOVE.** Every one is terminal-dated and scale-invariant, so the rescale operator has
nothing to bite on. `FWDRET` and `TERMREB` are pure oracles — |IC| with the realised forward return
is **1.0000** — and T1 clears both at 0.0 rank steps. T1 coincides with dating only on MCAP-shaped
keys (a price panel times a terminal constant), and that coincidence is what made the queue's
proposal look right.

**A statistic had to be named before either instrument worked, and the record has never named one
(ideas 520 / 564).** On this 430 × 4,194 panel the GLOBAL-MAX displacement — idea 433's literal
reading — flags every causal key too, at 2–4 rank steps out of 430, purely from float re-ordering
of near-ties: 6 false positives it does not have on a small corpus. The **median over days of the
per-day max** separates cleanly (causal keys 0.0, leaking keys 179–368). Both readings are
published for all 20 keys in `.certs.csv` and `.confusion.csv`. The choice is a statistic, not a
tuned dial.

## 3. The census — the record's one real record-wide terminal-dated input is its PANEL FILTER
566 committed scripts, **560 (98.9%) run a rule-8 leg**. Automatic tokens first, then the
refinement that a token is not a key:

| reading | count | share of rule-8 files |
|---|---|---|
| TIER 1 — any sharp terminal token | 511 | 91.2% |
| TIER 2 — the token sits in a key/selection function | 390 | 69.6% |
| `index_last` non-reporting hits | 55 hits / 41 files | **90.5% of that token count is printing** |
| `iloc_last` non-reporting hits | 101 hits / 62 files | mostly `eq.iloc[-1]` for CAGR — a legitimate terminal read of an equity curve |
| **reads `data/small_meta.csv`** | **298** | **53.2%** |
| reads `deepvalue/universe_under2b.csv` | 9 | 1.6% |
| reads a pinned shares snapshot | 3 | 0.5% |

**Tier 1 and tier 2 are not the answer — they are 90% printing, and any run that quotes them as a
leak count is quoting a grep.** The defensible number is the file class that cannot be printing:
**`data/small_meta.csv`'s `max_1d_move` is a FULL-SAMPLE max of |daily return|, and the SMALL panel
is defined by dropping the 44 names with `max_1d_move ≥ 1.0` — a statistic dated at the end of the
sample, applied from day one, in 298 of the record's 560 rule-8 files.** That is the `MAXMOVE` key
in §2: **T1 clears it at 1.0 rank steps; T2 flags it at 330.** The record's most widely shared
terminal-dated input is invisible to the certificate the queue proposed.

The effect is a survivorship screen, not an oracle tilt, and it is small next to the SMALL panel's
existing survivorship (§6) — but it is undeclared, and it is exactly the object a pre-rule-8 gate
exists to name.

## 4. PROTOCOL 4 and PROTOCOL 8 — the consequence book
SMALL430, top-20 equal weight, gross 0.75, weekly, t+1, 0/10/25 bps. Two tuned parameters —
**CERTIFICATE** (the gate) and **TILT STRENGTH m ∈ {0.20, 0.50, 1.00}** — and **all 363 grid points
are in `.arms.csv`**. Comparands @10 bps: SPY 14.13% / 0.862 / −33.72% (H 0.891 / 0.858, OOS 0.882);
RULES v2 (live) 3.77% / 0.565 / −14.58% (OOS 0.558); RULES v1 7.41% / 0.554 / −34.92% (OOS 0.499);
untilted control 6.12% / 0.438 / −25.90% (OOS 0.434).

**4a 0/363 and 4b 0/363, at 0, 10 and 25 bps.** The binding leg is the drawdown cap alone: MaxDD
fails **360 of 363** against H1 335, H2 289, OOS 288, CAGR 270. Idea 195's result on the same panel,
unchanged by the whole key corpus: on a 20-name small-cap book 4b is a verdict on concentration.

**Rule 8 (PROTOCOL 8), (KEY, m) chosen on 2010–2016 IS Sharpe alone, 2017–2026 read once, gate
applied BEFORE the choice — @10 bps:**

| gate | admits | pick | IS Sharpe | OOS CAGR | OOS Sharpe | OOS MaxDD | vs SPY | vs v2 |
|---|---|---|---|---|---|---|---|---|
| NONE | 20 | **FWDRET**/POS/1.00 | 0.974 | 39.03% | **2.198** | −26.70% | +1.316 | +1.640 |
| **T1** | 13 | **FWDRET**/POS/1.00 | 0.974 | 39.03% | **2.198** | −26.70% | +1.316 | +1.640 |
| T2 | 10 | PXDVOL/NEG/1.00 | 0.838 | 24.41% | 1.588 | −24.38% | +0.706 | +1.030 |
| **T1&T2** | 6 | VOL20/NEG/0.50 | 0.796 | 5.79% | **0.467** | −26.88% | **−0.415** | **−0.091** |

All 12 gate × rung cells are in `.walkforward.csv`. Read it in one line: **the T1 gate changes the
admitted set from 20 keys to 13 and does not change the pick at any of the three rungs — it still
hands rule 8 the pure oracle.** T2 removes the oracle but keeps a price-LEVEL key, which is leaky
in idea 185's other channel (PXDVOL |IC| 0.5996), so its pick still beats SPY OOS by +0.706. Only
the conjunction admits a set (MOM, R6, DDTR, REBASED, VOL20, VOLSH) whose rule-8 pick behaves like
an honest book: **OOS 5.79% / 0.467 / −26.88%, losing to SPY at all three rungs and to RULES v2 at
two of three.** That is what a walk-forward is supposed to look like on a panel with no edge.

## 5. Pre-registered predictions, scored
P1 HIT (4/4 gates) · P2 HIT (T1's dating false negatives, FWDRET named in advance) ·
P3 HIT (T2 false positives on causal keys: **none**) · P4 HIT (disjoint: T1-only DVOL, FROZEN,
PRICE, PXDVOL; T2-only the seven above) · **P5 MISS** — the dating half is right (NONE and T1 both
pick a terminal-dated key and both beat SPY OOS; T2 picks a causal-dated key) but the **T2 pick
still beats SPY OOS by +0.706**, because dating is not the only leak channel. The miss is reported
as the finding in §4 · P6 HIT (4a 0/363, 4b 0/363).

## 6. Survivorship, stated as PROTOCOL 9 requires
PART C runs on idea 195's SMALL430: current constituents of a sub-$2B screen
(`data/SMALL_PANEL_README.md`) intersected with the names that still file today — a survivor of a
survivor — and, per §3, further filtered by a full-sample `max_1d_move` statistic. Every PART C
number is biased in the tilt's favour. PARTS A and B do not depend on the panel.

## 7. Proposed PROTOCOL wording (10 lines, for the Sunday review — NOT applied here)
> **10. Dating certificate (runs BEFORE rule 8).** Every ranking or eligibility key must be
> declared as a function of dated inputs, each input carrying an as-of date. A key passes the
> DATING certificate iff, at five probe dates spanning the sample, its cross-sectional ranks
> computed on the full panel equal its ranks computed on the panel truncated at that date, with
> every input withheld whose as-of date is later than the probe — median over probe dates of the
> per-day max rank displacement equal to zero. A key that cannot be computed on truncated inputs
> FAILS. The SCALE certificate (idea 433's value form, same statistic) runs beside it, not instead
> of it: the two have disjoint content, 7 and 4 misses respectively on a 20-key corpus. A key that
> fails either certificate may still be reported, but its rule-8 result may not be quoted as
> out-of-sample evidence. Every published certificate result must name its statistic and its bar.

## 8. What the record should take from this
1. **Rule 8 is a date split, not a leak detector, and the T1 family does not repair it.** T1 is the
   right instrument for the axis it was built for and structurally blind to this one.
2. **The certificate must date the INPUTS, not just perturb the panel.** MCAPREB and SHARES read
   inf here only because the shares snapshot was made to carry an as-of date; without that they are
   invisible to both certificates.
3. **`data/small_meta.csv` is a terminal-dated panel filter in 53.2% of the record's rule-8 files.**
   Whatever else PROTOCOL adopts, that one should be declared.
4. **A grep is not a census.** The 91.2% tier-1 number is 90% print statements.

Follow-ups filed: 627 (re-cut the record's SMALL-panel results without the `max_1d_move` filter),
628 (does the SCALE channel need its own pre-rule-8 gate, given PXDVOL survives T2), 629 (as-of
dates as a required field on every input the record reads).

Script: `research/backtests/2026-09-10_does-a-TERMINAL-DATING-certificate-belong-BEFORE-rule-8_B.py`
Artefacts: `.console.txt`, `.certs.csv` (20 keys, both readings), `.confusion.csv`, `.census.csv`
(566 files), `.hits.csv`, `.tier2.csv`, `.audit.csv`, `.arms.csv` (363 rows), `.walkforward.csv`
(12 cells), `.repro.csv`.
