# Idea 896 — does the FILE-vs-CELL gap hold on NON-PLACEBO artifact families?

**Lane B, 2026-09-20.** Script `2026-09-20_file-vs-cell-gap-on-non-placebo-families_B.py`,
console `…_B.console.txt`, artifacts `…_B.{census,census_blobs,claims,claim_moves,grid,walkforward,gross_flatness}.csv`.
Deterministic, offline, 100 s. RULES.md / PROTOCOL.md / scan.py / bot.py / baseline.py untouched (rule 6).

## ANSWER: NO — and it does not merely fail to generalise, **it inverts, on the placebo family too**

Idea 889 published that swapping a PROSE matcher for a structural FAMILY matcher widens the
record's placebo corpus **×5.80 in FILES but only ×1.99 in CELLS** — "findable" and
"re-priceable" differing by a factor of 2.91. 896 asked whether that holds on the record's other
artifact families. Re-run with a **unit-clean currency** (both legs counted the same way, on the
same blobs, under two cell definitions), at HEAD:

| family | PROSE files | FAMILY files | ×files | ×rows | ×nums | **gap (ROW)** | **gap (NUM)** |
|---|---|---|---|---|---|---|---|
| BOOKS | 4,046 | 6,699 | 1.656 | 5.120 | 13.564 | **0.323** | **0.122** |
| ARMS | 2,560 | 4,288 | 1.675 | 7.067 | 18.847 | **0.237** | **0.089** |
| GRIDS | 3,383 | 4,668 | 1.380 | 5.003 | 13.185 | **0.276** | **0.105** |
| PLACEBO (889's own family) | 586 | 600 | 1.024 | 3.939 | 8.392 | **0.260** | **0.122** |

- **H_GAP REFUTED** — gap ≥ 2.00 in **0 of 3** non-placebo families under both cell definitions.
- **H_DIR REFUTED** — gap ≥ 1.0 in **0 of 3**. The blobs a family matcher adds are not smaller
  than average, they are **3–4× bigger** (mean added-blob rows: BOOKS 1,248, ARMS 2,034,
  GRIDS 2,311, PLACEBO 31,465, against prose-blob means of 199–256).

## The mechanism, and why the number was never a corpus fact (G_ID, gated at 5.551e-17)

    gap = (F_f/P_f) / (F_r/P_r) = (P_r/P_f) / (F_r/F_f) = mean PROSE blob size / mean FAMILY blob size

The FILE-vs-CELL gap is **identically** the ratio of mean blob size between the two matched sets.
It is not an empirical property of a corpus and never was. 889's "2.91" reads, restated, as
*"the blobs 889's prose leg selected were 2.91× larger on average than the blobs its family leg
selected."*

## H_CTRL REFUTED — and the refutation is the result (G_REPRO, at 889's OWN vintage tree)

889's own family, re-read on **the tree 889 ran on** (`b0504dba`, parent of `9797f2ac`), with both
legs counted the same way: **PROSE 358 files / 88,051 rows; FAMILY 371 files / 528,400 rows →
×1.04 files, ×6.00 rows, gap 0.17.** Same tree, same family, **opposite direction**.

889's ×5.80 / ×1.99 is a **structural numerator over a prose-selected denominator whose cells were
counted structurally** — i.e. exactly the mixed-unit defect 889 itself diagnosed in idea 880's
4.85× move, reappearing one level up, in 889's own headline. The caveat is stated both ways: this
run's PROSE leg is the family's name-vocabulary over every text blob (what a general prose matcher
*is*), not 889's bespoke predicate, so this is **not** a bit reproduction of 5.80/1.99 — it is the
same family measured in a currency that is not mixed, and in that currency the gap inverts.

## H_CLAIM REFUTED — the gap does not change committed claims the way the queue supposed

158 committed FILE-denominated shares in 49 memos (UNTYPED 117, ARMS 15, BOOKS 13, GRIDS 7,
PLACEBO 6). Applying each family's own multiplier at the 0.20 MOVE bar: **35 shares move under
the FILE multiplier, 41 under the CELL_ROW multiplier.** The cell currency moves *more* committed
claims than the file currency, not fewer. (Coarse by construction: the multiplier is family-wide,
so the leg is all-or-nothing per family — stated, not hidden. 117 of 158 shares name no family in
160 characters of context and are untyped.)

## CAPITAL ARM — the currency is **Sharpe-neutral and 4b-DECISIVE**

Grid: BAND c ∈ {0.01,0.03,0.05,0.08,0.10} × GROSS G ∈ {0.50,0.75,1.00} on U56 / B136 / SMALL.
Exactly two dials, **all 45 cells published** (`.grid.csv`), both KEEP paths at every cell.
10 bps, weekly, next-day execution, 260-day warm-up skip.

4a FULL **1/45** · 4b FULL **9/45** · 4b OOS **7/45**. (The one 4a pass is SMALL c=0.05 G=0.50.)

**Rule 8 — parameters fixed on 2009–2016 only, 2017–2026 read ONCE** (G3: argmax identical on a
hard-truncated IS frame):

| panel | chooser | c | G | IS Sharpe | OOS CAGR | OOS Sharpe | OOS MaxDD | RULES v2 OOS | SPY OOS | 4b OOS |
|---|---|---|---|---|---|---|---|---|---|---|
| U56 | C_CELL | 0.10 | 1.00 | 1.1457 | **12.14%** | **1.1938** | −16.30% | 9.46% / 1.2766 / −12.05% | 15.26% / 0.8737 / −33.72% | **PASS** |
| U56 | C_FILE | 0.10 | 0.75 | 1.1453 | 9.08% | 1.1944 | −12.35% | ″ | ″ | FAIL |
| B136 | C_CELL | 0.10 | 1.00 | 1.1470 | **11.02%** | 1.0873 | −19.20% | 7.85% / 1.1017 / −12.24% | ″ | **PASS** |
| B136 | C_FILE | 0.10 | 0.75 | 1.1459 | 8.25% | 1.0887 | −14.58% | ″ | ″ | FAIL |
| SMALL | C_CELL | 0.08 | 1.00 | 0.9658 | 6.07% | 0.6600 | −19.00% | 4.41% / 0.6472 / −12.48% | ″ | FAIL |
| SMALL | C_FILE | 0.08 | 0.75 | 0.9652 | 4.61% | 0.6603 | −14.51% | ″ | ″ | FAIL |

**H_CAP REFUTED (0/3 same book)** — but read the decomposition before reading the refutation:
the two currencies **agree on the band dial c on 3 of 3 panels** and disagree only on gross G,
which is Sharpe-flat by construction (largest IS Sharpe spread across the three G rungs inside a
single (panel, c) is **0.0026**, median 0.0017, over 15 families). C_CELL's argmax over a flat
dial always lands on G = 1.00; C_FILE takes the pre-declared central rung G = 0.75. **OOS Sharpe
differs by at most 0.0014 — and the 4b verdict still flips, 2/3 panels to 0/3**, because 4b's
binding legs (the CAGR floor and the DD cap) are gross-dial objects and Sharpe is not.

> *The record's choice of counting currency cannot move a Sharpe ranking and can decide a 4b pass.*

Neither chooser beats RULES v2 OOS on U56 or B136 (1.19 / 1.09 vs 1.28 / 1.10); both beat it on
SMALL (0.660 / 0.660 vs 0.647), where neither clears 4b.

## Gates (8/8)

| gate | result |
|---|---|
| G0 | U56 17.65 y · B136 17.65 y · SMALL 15.65 y; IS 7.96/7.96/5.96 y, OOS 9.69 y each |
| G1 | `fast_run` vs `engine.backtest`: returns **0.000e+00**, turnover **0.000e+00** (warm-up-skipped window; the engine leaves NaN in its first rows because `w_target.shift(1)` is NaN at i==0) |
| G2 | (U56, c=0.03, G=0.75) replays `baseline.rules_v2_weights` at **0.000e+00** — that cell **is** the live book |
| G3 | no chooser reads a 2017+ row; argmax identical on a hard-truncated IS frame — **PASS** |
| G4 | determinism: whole census recomputed, counts **identical** |
| G5 | two dials (band c, gross G) |
| G6 | **45 of 45** grid cells published |
| G_ID | gap ≡ mean-blob-size ratio, max \|diff\| **5.551e-17** |
| G_REPRO | 889's family re-read at 889's own vintage tree `b0504dba` (8,412 blobs) |
| G7 | independent replication of LEADERBOARD 2026-09-20 (idea 1719): U56 c=0.10 G=1.00 OOS **12.14% / 1.1938 / −16.30%** — **matches to the published precision** |

## No new book

Every 4b pass here is a cell the record already holds; G7 reproduces idea 1719's published U56
triple to the digit. **No KEEP is proposed, no memo is written, RULES.md is untouched.**

## Survivorship (rule 9)

U56 and B136 are current-constituent lists and SMALL a current sub-$2B screen carried back to 2010,
so every **absolute** level above — including the 4b passes — is an **upper bound**. The
chooser-vs-chooser contrast that carries the capital result is inside one frame over the same names
on the same days and is first-order immune; the pass counts are not.

## What the record should say

*The FILE-vs-CELL gap is not a finding about a corpus. It is, identically, the ratio of mean blob
size between two matched sets, and its sign depends entirely on whether the two legs are counted in
the same unit. Idea 889's ×2.91 measured a mixed-unit denominator, not a property of the placebo
corpus: on 889's own tree, in a unit-clean currency, the same family gives 0.17. Any future run
quoting 886's "5×" or 889's "factor of 3" should state the currency of **both** legs, or not quote
it.* **PROPOSED, NOT ENACTED** (rule 6: Sunday review only).
