# Idea 529 — audit every fail-set column in the record for SET vs FIRSTFAIL (lane B, 2026-09-12)

**ANSWERED = THE RECORD HAS EXACTLY ONE FIRSTFAIL PRODUCER, AND IDEA 527'S DETECTOR FOUND IT —
BUT AT A PRECISION OF 0.04. KILL as a capital idea. 527's headline SURVIVES the correction;
527's *25x* side-claim could NOT be reproduced on priced books and is NOT confirmed here.**

No RULES change, no KEEP claimed, no memo with RULES wording, no book proposed or promoted, no
PROTOCOL edit applied (rule 6). `RULES.md`, `PROTOCOL.md`, `scan.py`, `bot.py` and `baseline.py`
untouched.

Script: `2026-09-12_audit-every-fail-set-column-in-the-record-for-SET-vs-FIRSTFAIL_B.py`
(deterministic, seed 529; 10 bps, t+1 via the engine, weekly, no shorting/leverage).
Params (exactly 2, all 4 grid points reported): **P1 parser ∈ {strict, loose}**,
**P2 sample ∈ {all, singleton}**.

Four previous lane runs SKIPped this idea for having no price leg. This run gives it one by
**rebuilding the object instead of re-reading it**: the mislabel 527 can make is the event
"a real book fails two 4b bars at once", so 1,200 real books were priced to measure its rate.

---

## 1. The AST stamp (P1)

586 committed artefacts carry a fail-set column (`fail4b`/`f4b`/`fail_4b`/`binding`/…);
563 have a committed producing script. The stamper reads each script's keep-paths expression:
**SET** = enumerates every failing bar (comprehension, or a list with ≥2 independent bar-token
appends, joined); **FIRSTFAIL** = an `if`/`elif` chain or a per-bar early `return`.

| stamp | strict | loose |
|---|---|---|
| SET | 415 | 432 |
| **FIRSTFAIL** | **1** | **1** |
| UNKNOWN | 69 | 45 |
| EXTERNAL (helper imported from another module) | 37 | 48 |
| INHERITED (column copied from an upstream frame) | 29 | 25 |
| NO_SCRIPT / NO_COL_EXPR | 23 / 12 | 23 / 12 |

**The record's one FIRSTFAIL producer is
`2026-09-07_back-fill-the-mean-name-count-column-over-every-quoted-price_B.py`**, whose
`keep_paths()` is a literal `if/elif` chain over H1→H2→OOS→DD→CAGR and whose own docstring says
*"first failing 4b bar"*. Its `grid.csv` has 1,098 rows, all failing, 25 of them single-`OOS`.

## 2. What idea 527's detector actually did (P1 × P2 — all 4 grid points)

| parser | sample | files | resolved | resolved_frac | SET | FIRSTFAIL | UNKNOWN | mislabelled files | mislabelled rows | recovered sole-OOS |
|---|---|---|---|---|---|---|---|---|---|---|
| strict | all | 586 | 416 | 0.7099 | 415 | 1 | 170 | 24 | 1488 | 1 |
| strict | singleton | 63 | 25 | 0.3968 | 24 | 1 | 38 | 24 | 1488 | 1 |
| loose | all | 586 | 433 | 0.7389 | 432 | 1 | 153 | 27 | 1524 | 1 |
| loose | singleton | 63 | 28 | 0.4444 | 27 | 1 | 35 | 27 | 1524 | 1 |

527's data-driven tiering (*does ANY row emit ≥2 tokens?*) put 523 files in T1_DECLARED and 63 in
the ambiguous T1_SINGLETON tier, which it then excluded from every headline.

- **It is sound in one direction: 0 of 523 DECLARED files are FIRSTFAIL.** Nothing 527 counted was
  a short-circuit column read as a set.
- **It is nearly worthless in the other: of the 25 SINGLETON files the AST can resolve, 24 are
  genuine SET and 1 is the real FIRSTFAIL — precision 0.0400 (strict), 0.0357 (loose).**
  The queue's hypothesis is **CONFIRMED**: the detector mislabels genuine SET files wholesale.

## 3. Re-running 527's headline on the corrected partition

| partition | sole-OOS | failures | rate |
|---|---|---|---|
| 527's (T1_DECLARED only) | 85 | 769,618 | 0.000110 |
| AST-corrected, parser=strict (every file the AST calls SET) | 79 | 480,825 | 0.000164 |
| AST-corrected, parser=loose | 79 | 482,908 | 0.000164 |

**527's conclusion survives its own method error.** The corrected rate is 1.5x higher and still
~1.6 × 10⁻⁴: the OOS leg is rarely — not never — the sole binding bar, which is exactly what 527
published. CAVEAT, stated plainly: this reader is **not byte-identical** to 527's (it admits more
column spellings), so the absolute counts here do not reproduce 527's published 46 / 399,086. The
comparison that matters is *within this run* — both partitions are read by the same reader.

## 4. The price leg — 1,200 real books (80 draws × 5 gross rungs × 3 panels)

Full grid, all 15 (panel, gross) cells reported (mean over 80 draws):

| panel | gross | CAGR | Sharpe | MaxDD | mean nfail | 4b | 4a | multi-fail share | sole-OOS |
|---|---|---|---|---|---|---|---|---|---|
| B136 | 0.375 | 7.08% | 1.0828 | −13.25% | 1.175 | 0 | 8 | 0.1125 | 0 |
| B136 | 0.500 | 9.45% | 1.0832 | −17.37% | 1.075 | 9 | 0 | 0.1250 | 0 |
| B136 | 0.625 | 11.83% | 1.0835 | −21.35% | 1.125 | 18 | 0 | 0.2000 | 0 |
| B136 | 0.750 | 14.21% | 1.0838 | −25.20% | 1.163 | 3 | 0 | 0.1125 | 0 |
| B136 | 1.000 | 18.97% | 1.0840 | −32.50% | 1.188 | 0 | 0 | 0.1250 | 0 |
| SMALL716 | 0.375 | 6.28% | 0.6516 | −20.86% | 4.263 | 0 | 0 | 0.9875 | 0 |
| SMALL716 | 0.500 | 8.18% | 0.6520 | −27.00% | 4.588 | 0 | 0 | 0.9875 | 0 |
| SMALL716 | 0.625 | 10.01% | 0.6523 | −32.78% | 4.313 | 0 | 0 | 0.9875 | 0 |
| SMALL716 | 0.750 | 11.76% | 0.6524 | −38.20% | 4.025 | 0 | 0 | 0.9875 | 0 |
| SMALL716 | 1.000 | 15.00% | 0.6526 | −48.05% | 3.813 | 0 | 0 | 0.9875 | 0 |
| U56 | 0.375 | 6.45% | 1.0766 | −11.87% | 1.163 | 0 | 0 | 0.1375 | 0 |
| U56 | 0.500 | 8.62% | 1.0771 | −15.60% | 1.125 | 3 | 0 | 0.1375 | 0 |
| U56 | 0.625 | 10.78% | 1.0775 | −19.23% | 0.875 | 29 | 0 | 0.1500 | 0 |
| U56 | 0.750 | 12.95% | 1.0779 | −22.74% | 1.100 | 8 | 0 | 0.1625 | 0 |
| U56 | 1.000 | 17.29% | 1.0784 | −29.45% | 1.150 | 0 | 0 | 0.1250 | 0 |

**The measured multi-fail rate p = P(a failing book fails ≥ 2 bars):**
U56 **0.1583** (n=360), B136 **0.1459** (n=370), SMALL716 **0.9875** (n=400), pooled 0.4478 —
a mixture, not one number. On the panels the record actually uses, p ≈ 0.15.

**How many of the record's files are genuinely at risk.** The exponent must be *failing* rows, not
total rows: a row that passes 4b emits no token and can never reveal the semantics. At the low-p
reading the SINGLETON tier is expected to hide **15.78** SET files (8.79 at pooled p); the AST finds
**24**. The gap is explained by the tier's composition, not by p: of the 24 mislabelled files, **6
have ZERO failing rows** (undetectable at any p) and the median has **7**. Median failing rows in
the SINGLETON tier is 16, against 276 in the DECLARED tier.

**527's "25x overstatement" side-claim is NOT confirmed here.** Across all 1,200 books, **0** fail
the OOS bar alone and **0** have OOS as their *first* failing bar — the OOS Sharpe bar is never
reached before H1 or H2 has already failed. The ratio is therefore not measurable on this corpus.
That is an honest non-reproduction, not a refutation: 527 measured it on the record's *tuned*
books, and this run shows it is not a property of books in general.

## 5. Rule 8 — walk-forward (required leg)

Reading chosen on **2009–2016 only**, evaluated on **2017–2026 untouched**. The IS-chosen reading is
*"a single-token fail column is not diagnostic; stamp it from the script"*; it holds OOS iff p stays
far from 1.

| panel | p IS (≤2016) | p OOS (2017+) | \|Δ\| | reading holds OOS? |
|---|---|---|---|---|
| U56 | 0.3977 (n=347) | 0.1376 (n=356) | 0.2601 | YES |
| B136 | 0.1642 (n=341) | 0.2546 (n=377) | 0.0904 | YES |
| SMALL716 | 0.8706 (n=394) | 0.9875 (n=400) | 0.1169 | YES |

**3 of 3 panels: the direction is window-stable, the magnitude is not** (U56 moves 0.26). So the
stamp-from-the-script prescription survives rule 8; any *numeric* claim about detectability does not.

Books OOS vs baseline and SPY (OOS CAGR / OOS Sharpe / OOS MaxDD):

| panel | RULES v2 (live) | RULES v1 | SPY | books MEAN (400) | books BEST OOS Sharpe | 4b passers |
|---|---|---|---|---|---|---|
| U56 | 9.47% / 1.2782 / −12.05% | 7.60% / 0.7361 / −13.83% | 15.33% / 0.8767 / −33.72% | 11.63% / 1.0848 / −19.78% | 22.99% / 1.2487 / −30.21% | 12.37% / 1.1329 / −18.65% (n=40) |
| B136 | 7.88% / 1.1059 / −12.24% | 5.87% / 0.5702 / −21.19% | 15.33% / 0.8767 / −33.72% | 12.01% / 1.0577 / −21.93% | 23.65% / 1.3060 / −30.36% | 11.90% / 1.1491 / −18.49% (n=30) |
| SMALL716 | 4.47% / 0.6516 / −12.18% | 33.02% / 0.7149 / −25.48% | 15.33% / 0.8767 / −33.72% | 9.41% / 0.6101 / −33.30% | 9.60% / 0.9624 / −19.72% | none |

## 6. KEEP paths — both evaluated on all 1,200 books

- **4a** (Sharpe > RULES v2 in BOTH halves AND MaxDD no worse): **8 of 1,200** — all B136 at
  gross 0.375 (e.g. CAGR 7.84%, Sharpe 1.2088, MaxDD −11.10%, H1 1.4021 / H2 1.0515).
- **4b** (Sharpe > SPY both halves AND OOS, MaxDD ≤ 60% SPY, CAGR ≥ 70% SPY): **70 of 1,200**
  (U56 40, B136 30, SMALL716 0).

**Nothing is claimed or promoted.** These are *random* equal-weight draws built to exercise the bar
vector, not to be traded; picking the 8 or the 70 after the fact is selection on the answer, and the
panels carry current-constituent survivorship bias (`universe_broad.json`, `prices_small.csv.gz` —
see `data/SMALL_PANEL_README.md`). The deliverable of this idea is the semantics stamp, not a book.

## 7. PROPOSED (not applied — rule 6)

> **PROTOCOL 5 addendum.** Any run that publishes a fail-set column (`fail4b`/`f4b`/`binding`/…)
> MUST state its semantics in the header comment as `SET` or `FIRSTFAIL`. A later reader may not
> infer it from the data: on this corpus that inference has precision 0.04.

Committed beside this file: `.stamps.csv` (per-file semantics stamp, both parsers), `.grid.csv`
(the 4 grid points), `.books.csv` (1,200 priced books with full bar vectors), `.walkforward.csv`,
`.console.txt`.
