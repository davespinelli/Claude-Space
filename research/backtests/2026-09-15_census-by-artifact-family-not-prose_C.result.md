# Idea 889 — census the record by ARTIFACT FAMILY, not by PROSE (lane C, 2026-09-15)

**ANSWERED: ALL THREE HEADLINE DENOMINATORS MOVE, BUT ONLY ONE OF THEM MOVES FOR THE REASON THE
QUEUE GAVE. 880's "92.9% of the record's placebo mass can never be re-priced" restates to
**65.4%** — its share rises **7.14% → 34.62%, a factor of 4.85** — and there the prose matcher IS
the defect (matcher leg ×4.24 against a rollup leg of ×1.65). For the other two the matcher is
not the culprit: 871's count moves mostly because files are not runs (×1.29 matcher, ×0.63
rollup), and 514's denominator does not move at all (×1.0000 exactly, as pre-registered), because
it never used prose to build one. A fourth number falls out that no census in the record
publishes: **871's own denominator is +22.9% six commits later** — a census denominator is a
property of a DATE, not of "the record". KILL for capital.**

Nothing promoted, no rule changed; `RULES.md`, `PROTOCOL.md`, `scan.py`, `bot.py`, `baseline.py`
untouched (rule 6). Script
`research/backtests/2026-09-15_census-by-artifact-family-not-prose_C.py`, wall 126s,
deterministic, no network. Artefacts: `.grid.csv` `.legs.csv` `.vintage.csv` `.hypotheses.csv`
`.books.csv` `.walkforward.csv` `.keep.csv` `.console.txt`.

SELECTION: the SECOND open entry in QUEUE.md, per lane C's rule.

## Gates — every published number this run restates is reproduced first, at its own VINTAGE

A census is a statement about a TREE, so each is re-run against the tree its run actually saw:
PARENT(adding commit) + that run's own script blob. Blobs are read with `git cat-file`; the
working tree is never touched.

| gate | quantity | bar | got |
|---|---|---|---|
| G1 | 871's placebo-bearing committed files | 70 | **70 PASS** |
| G2 | 880's RE-PRICEABLE files | 5 | **5 PASS** |
| G3 | 514's 3,784 artefacts / 75 token carriers | — | **BLOCKED** (see below) |
| G4a | 886: 70 files → run stems | 44 | **44 PASS** |
| G4b | 886: stems with a surviving script | 34 | **34 PASS** |
| G4c | 886: runs carrying seed-bearing per-arm cells | 9 | **9 PASS** |
| G4d | 886: per-arm cells recovered by READING | 432,709 | **432,709 PASS** |
| G5 | determinism (871's census recomputed) | same | **same PASS** |
| G6 | this run's LIVE book vs `baseline.rules_v2_weights` | 0 | **0.000e+00 PASS** |

**G3 is BLOCKED and is reported as blocked, not worked around.** 514's adding commit is this
shallow clone's boundary (50 commits, all 2026-09-14 onward) and has **no parent here**, so its
tree cannot be rebuilt and its 3,784 / 75 is **quoted, never reproduced**. 514 published the same
limit about itself. Its method is re-run at HEAD instead; its **legs** are still exact (they are
ratios inside one tree), its "vs committed" column is a cross-vintage comparison and is labelled
as one.

## The grid — census set (tuned 1) × artifact matcher (tuned 2), both LEVELS always reported

| census | headline as committed | FILE×PROSE | FILE×FAMILY | RUN×PROSE | RUN×FAMILY |
|---|---|---|---|---|---|
| **871** placebo-bearing units | 70 files | 70 | **90** | 44 | **48** |
| **880** re-priceable share | 5/70 = 7.14% | 5/79 = 6.33% | 29/108 = 26.85% | 5/48 = 10.42% | **18/52 = 34.62%** |
| **514** vintage-token share | 75/3,784 = 1.98% | 494/6,962 = 7.10% | 494/6,962 = 7.10% | 209/954 = 21.91% | **209/954 = 21.91%** |

PROSE = the census's own text predicate on text-readable blobs. FAMILY = idea 886's `cell_table`
detector verbatim (a `seed` column plus one of dsharpe/gap/excess/…), widened by a `kind`-column
table carrying ≥2 of 880's null-vocabulary values — applied to **every** committed sibling blob,
`.csv` and `.csv.gz` included. All 12 cells in `.grid.csv`; nothing is selected on the answer.

## The two legs — and the queue's premise is right in one case of three

| census | rollup leg (FILE→RUN) | matcher leg (PROSE→FAMILY) | net | moves ≥20%? | matcher dominates? |
|---|---|---|---|---|---|
| 871 | ×0.629 | ×1.286 | ×0.686 | yes | **no** |
| 880 | ×1.646 | **×4.243** | ×5.469 | yes | **yes** |
| 514 | ×3.088 | **×1.0000** | ×3.088 | yes | **no** |

- **H_MOVE CONFIRMED** (3 of 3 move past the pre-registered 0.20 bar).
- **H_MATCHER REFUTED** (dominates in 1 of 3, bar was ≥2). The prose matcher is decisive exactly
  where a census mixes its units — 880 divided a STRUCTURAL numerator by a PROSE denominator, and
  that single mismatch is worth 4.24× on its own. Where the census counts files consistently
  (871), the file→run rollup moves the number more than the matcher does.
- **H_CTRL CONFIRMED at exactly 1.0000**: 514's denominator cannot move, because it was built
  artifact-first. The defect is a property of prose-built denominators, not of censuses.
- **H_NUM CONFIRMED (×3.09)**: the same defect hits published NUMERATORS. 514's 1.98% is a
  per-file share of a per-run fact — a run whose memo stamps its panel vintage has stamped its
  CSVs too — and at run level 21.91% of the record's runs carry the token.
- 871's unit-clean readings, stated so no ratio is taken for more than it is: at FILE level the
  family matcher adds **20 blobs (×1.286)**; at RUN level it adds **4 runs (×1.091)**.

## 886's "5×" is a FILE ratio, and in cells it is 2× — H_CELLS REFUTED

At 880's own vintage: its 5 re-priceable files carry **293,760** per-arm excess cells; the family
matcher finds **29 blobs / 585,858 per-arm rows** (440,349 seed-bearing).

**In files 5.80×. In cells 1.99×.** The bar was ≥5× in cells, and it fails. The record's placebo
mass is far more *findable* than 880 reported, but only about twice as *re-priceable* — the extra
files are small ones. Any future run quoting 886's 5× should say which currency it means.

## H_VINTAGE CONFIRMED — the number 70 is a date

871's census, byte-for-byte unchanged, re-run at four committed trees:

| tree | prose files | run stems | vs published 70 |
|---|---|---|---|
| 871 vintage | **70** | 44 | 0.0% |
| 880 vintage | 79 | 48 | +12.9% |
| 886 vintage | 85 | 51 | +21.4% |
| HEAD | **86** | 51 | **+22.9%** |

880 divided by 70 a denominator that was already 79 when 880 ran. Six commits inside one day move
it 23%. No census in the record publishes the tree it counted.

## RULE 8 on the census statistic — UNDERPOWERED, and printed as such

Corpus runs split at their own median date (2026-09-08, declared before the yields were read):
the IS half holds **4** placebo-bearing runs against **39** OOS, uplift 1.0000 vs 1.1026. The
record's placebo work is almost entirely a late-corpus activity, so this statistic has no usable
in-sample side. **No transfer claim is made from it.**

## RULE 8 on the books (mandatory; 10 bps, next-day, weekly, IS 2009–2016 / OOS 2017–2026 read once)

| panel | IS pick | FULL CAGR / Sharpe / MaxDD | halves | OOS CAGR / Sharpe / MaxDD | 4a | 4b |
|---|---|---|---|---|---|---|
| U56 | EWALL075 | 13.21% / 1.120 / −22.53% | 1.196 / 1.059 | 13.70% / 1.128 / −22.53% | ✗ | ✗ |
| B136 | EWALL075 | 14.08% / 1.117 / −25.37% | 1.236 / 1.010 | 13.79% / 1.092 / −25.37% | ✗ | ✗ |
| STK20 | EWALL075 | 22.68% / 1.357 / −24.15% | 1.520 / 1.233 | 22.98% / 1.311 / −24.15% | ✗ | ✗ |

LIVE baseline RULES v2 (U56) **8.62% / 1.201 / −12.05%**, halves 1.232/1.177, OOS Sharpe 1.277.
SPY **15.13% / 0.885 / −33.72%**, halves 0.959/0.824, OOS 0.874 (B136 SPY 15.16% / 0.886 / OOS
0.877). Over all 21 grid points: **4a 0 (0.0%), 4b 8 (38.1%)**. The IS-only selector picks the
**signal-free equal-weight control on every panel**, and that pick fails 4b on the drawdown cap
(−22.53% against a −20.23% cap) on all three. Every 4b pass belongs to book families the record
has already declined (BAND100, CAND20/CAND10, EWELIG075) or to the STK20 sub-panel built here for
breadth. **Nothing is proposed.**

SURVIVORSHIP: U56/B136 are current-constituent lists and STK20 is a current-constituent megacap
subset, so CAGR and drawdown **levels** are optimistic on all three. The headline quantity of this
run — how a census denominator moves between matchers, levels and vintages — is a property of
committed files and is not exposed to that bias.

## Honest limits

1. G3 is blocked by the clone depth; 514's legs are exact, its cross-vintage column is not a
   reproduction.
2. The FAMILY matcher is 886's detector plus one widening; a different detector would give a
   different numerator. Both components are printed per blob in `.grid.csv`'s inputs.
3. The census walk-forward has 4 IS runs and is reported as underpowered, not as a transfer.
4. 880's ratio is restated **at 880's own vintage**, so its 4.85× is free of the vintage drift
   measured separately in section [3]; the two effects are not stacked.

## Follow-ups queued

894 (require a TREE STAMP — commit sha + file count — beside every published census denominator,
priced against the record's committed censuses), 895 (re-price the record's other MIXED-UNIT
shares: numerator and denominator built by different matchers), 896 (does the FAMILY matcher's
file/cell gap — 5.8× vs 1.99× — hold on the record's non-placebo artifact families).
