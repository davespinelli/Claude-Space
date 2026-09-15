# Idea 951 (cloud, 2026-09-15) — normalise the record's 4b LEG ALPHABET and re-read every committed FAIL share

**ANSWERED. KILL for the queue's own "8x understatement" motivation — it is a mis-citation, the
true unification move is 1.02x–1.24x. The alphabet normalisation is still worth doing, but it
moves FILE-weighted shares (up to +8.40 pp), not ROW-weighted ones. What 944 could not see is the
SELECTOR: 19.3% of the record's leg-bearing cells sit outside its one-column `fail4b` filter, and
widening it moves 2 of 20 published claims past the 5 pp bar. The record's headline census claim —
"the modal binder is the CAGR floor, 68.8%" — SURVIVES (66.54%, −2.26 pp).**

## Gates — 8 of 8 PASS, printed before any claim was read
`G0` local cadence mask ≡ `engine.rebalance_mask` on W/M/Q, 0 differing rows · `G1` fast runner ≡
`engine.backtest` @10 bps, worst of W/M/Q **2.082e-17** · `G2` `band_book(0.03,0.75)` ≡
`rules_v2_weights`, **0.0** · **`G3` A1_944 reproduces 944-B's committed census EXACTLY: ΔFAIL +0
rows (816,550) and worst share delta 0.000e+00** · `G3b` the same for 944's file-weighted shares,
worst delta 0.000e+00 · `G5` the canonical alphabet is idempotent over 208 distinct observed cells,
0 violations · `G6` it never re-labels a spelling 944 already mapped, 0 violations · `G7`
canonical coverage 99.7972% of 1,020,178 leg-asserting cells (bar ≥ 99%).

## The pre-read (S1) — 944's selector was one column, the record uses forty-five
`research/backtests` carries **45 distinct leg-bearing column names** over 4,675 committed CSVs.
944's `"fail4b" in name` filter reached **923,851 cells**; **220,898 more (19.3%)** sit outside it
under `binding` (87,673), `f4b` (53,710), `failing` (31,949), `fail_4b` (28,439), `bind` (9,015),
`fails` (8,595), `fail_legs` (1,311), `fail` (178) and `binding_leg` (28). Published as
`.columns.csv`.

## The four arms (TUNED axis 1 — every level reported)
| arm | alphabet | selector | files | FAIL rows | unmappable |
|---|---|---|---|---|---|
| A0_RAW | none (verbatim strings) | `fail4b` | 472 | 816,821 | 0 |
| A1_944 | 944's CANON | `fail4b` | 472 | **816,550** | 181 |
| A2_CANON | this run's canonical L1_H1..L5_CAGR | `fail4b` | 472 | 816,586 | 145 |
| A3_WIDE | canonical | all 45 columns | **727** | **1,018,109** | 2,069 |

A0_RAW sees **186 distinct legsets**; A2_CANON collapses the same cells onto **31**. The per-file
mapping (8,369 rows, one per file × legset) is published as `.mapping.csv` and every unmappable
spelling as `.unmappable.csv`, so the normalisation is auditable cell by cell.

## The claim set (TUNED axis 2 — 20 claims × 4 arms, all reported in `.claims.csv`)
- **H_ALPH SUPPORTED, 5 of 20** claims move ≥ 5 pp on the alphabet alone (A0_RAW → A2_CANON), and
  **every one of the five is a FILE-weighted `among` share**: CAGR **+8.40 pp**, H2 +7.79, DD
  +7.40, OOS +6.67, H1 +6.18. No row-weighted claim moves as much as 2 pp (largest: CAGR_among
  +1.90 pp). Rare spellings are concentrated in a few files, so they are loud file-weighted and
  silent row-weighted.
- **H_SEL SUPPORTED, 2 of 20** claims move ≥ 5 pp on the selector alone (A2_CANON → A3_WIDE), and
  **both are ROW-weighted**: H2_among **−5.16 pp**, OOS_among **−5.08 pp** (H1_among −4.25 pp just
  misses). DD_alone **+2.99 pp** and CAGR_alone **+2.44 pp** move the same way. The two dials move
  *disjoint* halves of the claim set.
- **H_MODAL SURVIVES.** Under A3_WIDE the modal binder is still **CAGR at 0.6654** against the
  record's published 0.688 (−2.26 pp, inside the bar); DD reads 0.5704 against 0.583 (−1.29 pp).

## H_8X — NOT SUPPORTED. The queue's motivating number is a mis-citation (`.eightx.csv`)
The queue says 944 read "the L4_DD-alone share at 1.9% against 15.8% once all five are unified — an
8x understatement". Audited against **944-cloud's own committed console**:

| committed line | rows | share |
|---|---|---|
| raw `DD` alone (the true raw endpoint) | 16,006 | **0.1280** |
| normalised `L4_DD` alone | 19,772 | **0.1581** ← the queue's 15.8%, correctly cited |
| normalised `L2_H2+L4_DD` | 2,320 | **0.0185** ← the queue's "1.9%", **a TWO-leg set** |

The true unification move is **0.1280 → 0.1581 = 1.24x (+3.01 pp)**, not 8x. This run's independent
replay on 944-B's wider census agrees in direction and order: **0.1486 → 0.1510 = 1.02x
(+0.24 pp)**. The "8x" was produced by reading the wrong row off the right table — the record's
dominant DD spelling was already the canonical short form `DD`, so unifying spellings could never
move a row share eightfold.

**A further record defect, reported not absorbed:** the two committed 944 censuses disagree on the
denominator. 944-cloud publishes **125,090 FAIL rows over 184 files** (STRICT); 944-B publishes
**816,550 over 459** (WIDE, replayed here exactly at G3). Both are labelled "the record's committed
4b FAIL rows". Any leg-share quoted without naming which census it came from is unadjudicable.

## The price leg (PROTOCOL rules 2/3/4) — 3 panels × 4 books × 4 cadences = 48 cells, all published
U56 SPY 15.13% / 0.885 / −33.72% (H1 0.959 / H2 0.824, OOS 0.874); RULES v2 live baseline 8.62% /
1.201 / −12.05% (H1 1.232 / H2 1.177).

| cell | CAGR | Sharpe | MaxDD | H1 / H2 | OOS Sharpe | 4a | 4b |
|---|---|---|---|---|---|---|---|
| U56 TOP20_g075 / M (the standing candidate) | 14.7% | 1.202 | −19.5% | 1.216 / 1.198 | 1.283 | n | **y** |
| U56 TOP10_g075 / M | 16.7% | 1.124 | −23.2% | 1.217 / 1.055 | 1.097 | n | n (`L4_DD`) |
| U56 BAND03_g075 / W (= RULES v2) | 8.6% | 1.201 | −12.1% | 1.232 / 1.177 | 1.277 | n | n (`L5_CAGR`) |
| B136 TOP40_g075 / W | 11.9% | 1.000 | −19.1% | 1.141 / 0.872 | 0.972 | n | **y** |
| SMALL TOP20_g075 / M | 8.1% | 0.544 | −35.1% | 0.761 / 0.380 | 0.437 | n | n (all five legs) |

**4a PASS 0 of 48. 4b PASS 6 of 48** (5 on U56, 1 on B136, 0 on SMALL). Every `fail4b` cell in
`.grid.csv` is written in the canonical `L1_H1..L5_CAGR` alphabet by construction — the record's
first grid that needs no normalising.

## Rule 8 walk-forward — (book, cadence) chosen on 2009–2016 ALONE, 2017–2026 read ONCE
| panel | chooser | picked | OOS CAGR | OOS Sharpe | OOS MaxDD | SPY OOS | 4a | 4b |
|---|---|---|---|---|---|---|---|
| U56 | IS Sharpe max | TOP10/M | 17.2% | 1.097 | −23.2% | 15.1% / 0.874 / −33.7% | n | n (`L4_DD`) |
| U56 | IS 4b then Sharpe | TOP10/M | 17.2% | 1.097 | −23.2% | ″ | n | n (`L4_DD`) |
| U56 | canonical TOP20/M | TOP20/M | **16.7%** | **1.283** | **−19.5%** | ″ | n | **y** |
| B136 | IS 4b then Sharpe | TOP20/M | 15.5% | 1.000 | −26.1% | 15.2% / 0.877 / −33.7% | n | n (`L4_DD`) |
| SMALL | IS Sharpe max | BAND03/M | 4.1% | 0.593 | −16.8% | 14.1% / 0.877 / −33.7% | n | n (`L2_H2,L3_OOS,L5_CAGR`) |

**OOS 4b PASS 1 of 9, OOS 4a PASS 0 of 9.** The single pass is the *canonical* TOP20/M — i.e. the
book the record already holds, not one this run chose. Both in-sample choosers pick TOP10/M on U56
and TOP10/Q on B136 and **both fail OOS on `L4_DD`**: the IS-Sharpe chooser buys 0.5 pp of extra
OOS CAGR with 3.7 pp of extra drawdown and loses the 4b DD cap doing it. Nothing here is a new
candidate; the run adds no book.

## Survivorship (PROTOCOL rule 9)
U56 / B136 / SMALL are current-constituent lists. SMALL additionally drops the **52 tickers with
`max_1d_move` ≥ 1.0** per `data/small_meta.csv` (**663 names + SPY benchmark**, not the 483 the
sprint brief quotes — the cached panel has grown). Every CAGR, Sharpe and
drawdown **level** above is therefore optimistic. The 4b legs are read against SPY, which is not
survivorship-inflated, so a survivor panel makes books look **better** and 4b failures **rarer** —
which cuts against this run finding 42 of 48 cells failing, not for it. **The census is a census of
the record's TEXT and makes no market claim whatsoever**; it inherits whatever biases its source
runs carried.

## What this changes
1. Any published leg share must name **both** its alphabet and its **column selector**, and its
   **census denominator** — the two 944 censuses differ 6.5x on the last one.
2. File-weighted `among` shares in the record predating a unified alphabet are understated by
   **6–8 pp**; row-weighted shares are not (< 2 pp).
3. The "8x understatement" sentence should be struck from the queue and from any downstream text.
4. `L1_H1..L5_CAGR` joined by `,` is the spelling this run emits; `.mapping.csv` is the migration
   table for everything already committed.

## Follow-ups filed
(numbered 958–960; 955–957 were taken by a concurrent lane between this run's claim and its push — record defect 932 recurring.)

958 (re-read the record's leg shares under A3_WIDE's 45-column selector for EVERY published claim,
not just 944's 20) · 959 (the two 944 censuses' 6.5x denominator gap: which selector is the
record's intended definition of "a committed 4b FAIL row") · 960 (does the IS-Sharpe chooser's
`L4_DD` OOS failure on TOP10 generalise across panels and gross rungs).
