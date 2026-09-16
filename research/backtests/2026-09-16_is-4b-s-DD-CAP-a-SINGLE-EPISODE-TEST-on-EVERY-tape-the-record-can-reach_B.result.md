# Idea 1024 (lane B, 2026-09-16) — is 4b's DD CAP a SINGLE-EPISODE TEST on EVERY tape the record can reach?

**ANSWER: YES — ON EVERY TAPE THE RECORD CAN REACH, AND BY A MARGIN WITH ZERO VARIANCE.**
A two-episode **cap** exists **nowhere** on the rule-8-legal grid; the only two-episode
comparand cell there is the **4a** comparand, not 4b's cap, and it is a knife-edge.

Script `2026-09-16_is-4b-s-DD-CAP-a-SINGLE-EPISODE-TEST-on-EVERY-tape-the-record-can-reach_B.py`.
Gates **8 of 8 PASS**; pre-registered hypotheses **3 of 8 PASS**. Deterministic, no network.

## Setup
2 tuned dials, all 6 points reported and none selected: **PANEL SET** {PAIR = [U56, B136],
TRIO = [U56, B136, **SMALL**]} × **EPISODE DEFINITION** {DD10, DD05, CAL_Q}. Episodes are
SPY's **own** drawdown episodes (peak → recovery to a new high) cut at 10% / 5% depth, plus a
calendar-quarter control — **no episode window is hand-typed anywhere in the file.**
Controls at every point: END GRID {LEGAL = 16 quarter-ends 2015Q1–2018Q4 (rule-8-legal, 1013's
grid); POST = 16 quarter-ends 2019Q1–2022Q4 (**rule-8-ILLEGAL**, 1022's grid, carried only as a
control}, BAR {REC_FULL, WIN}, COST {0, 10, 25} bps, CLAIM SET {SHELF 9, GRID 54} = **63 books**,
ANCHOR E = 2016-12-31. Start pinned at each panel's own `px.index[260]`.

## (A) The census — distinct episodes that ever set an OOS MaxDD
Bar **WIN** (the only bar whose cap can move with E; REC_FULL is E-invariant, so its count is
**1 by construction** and is reported as a floor, not as evidence).

| END GRID | series | U56 | B136 | SMALL | (identical under DD10 / DD05 / CAL_Q) |
|---|---|---|---|---|---|
| LEGAL | **SPY — 4b's DD cap** | **1** | **1** | **1** | the 2020 crash, 9 of 9 cells |
| LEGAL | RULES v2 — 4a comparand | 1 | 1 | **2** | `DD_2020-03-23 \| DD_2022-10-12`, 0 and 10 bps |
| LEGAL | books (median of 63) | 1 | 1 | 1 | distribution **1:50, 2:13**, mean 1.206 |
| POST (ILLEGAL) | **SPY** | **3** | **3** | **3** | `2020-03-23 \| 2022-10-12 \| 2025-04-08` |
| POST (ILLEGAL) | books (median) | 2 | 3 | 2 | distribution 1:5, 2:35, 3:23 |

So the queue's question in one line: **no cell of the legal grid has a two-episode DD cap.**
Three-episode caps exist on the POST grid on every panel — i.e. only where rule 8 forbids the
record to go. Adding a third panel does not help: SMALL's SPY column is **bit-identical** to
U56's on all 4,198 common days (gate G7), so the panel dial cannot move the comparand at all;
it can only move books. That is a structural fact, not a measurement — it is stated, not hidden.

## (B) The margin — the cap is single-episode by a *distance*, not by a tie
Deepest drawdown attributable to each episode inside the **same** OOS window, binding minus
runner-up, over the 48 (panel × legal end) cells at DD10:

| series | grid | median margin | min | max | ends under 0.05 |
|---|---|---|---|---|---|
| **SPY (the cap)** | LEGAL | **0.0922** | 0.0922 | 0.0922 | **0 / 48** |
| RULES v2 | LEGAL | 0.0296 | **0.0004** | 0.0483 | **48 / 48** |
| SPY | POST | 0.0574 | 0.0207 | 0.0922 | 6 / 48 |

SPY's binding episode is `DD_2020-03-23` at **16 of 16** legal ends on all three panels, with
`DD_2022-10-12` the runner-up at **16 of 16**, and the gap is **constant to the fourth decimal**.
The 4a comparand is one-episode only by a hair — on SMALL it actually flips (`DD_2020-03-23`
×14, `DD_2022-10-12` ×2), which is the entire source of H_ONE's FAIL.

## (C) Rule 8 (mandatory) — 3 IS-only choosers × 3 panels × the LEGAL end grid, 432 rows
At PROTOCOL's own split **E = 2016-12-31, 10 bps**, IS window read ALONE, OOS read once:

| panel | chooser | pick | OOS CAGR / Sharpe / MaxDD | 4b (WIN) | 4a |
|---|---|---|---|---|---|
| U56 | IS_SHARPE / IS_LEGS | `U56-band0.08-g1.00` | 11.99% / 1.162 / −19.05% | PASS | FAIL |
| U56 | IS_CAGR | `U56-qroll-q0.17-w1008-d0.50` | **15.60% / 1.293 / −15.59%** | PASS | FAIL |
| B136 | IS_SHARPE / IS_LEGS | `B136-band0.08-g1.00` | 11.05% / 1.097 / −19.50% | PASS | FAIL |
| B136 | IS_CAGR | `B136-qroll-q0.12-w1008-d0.50` | 14.30% / 1.157 / −17.31% | PASS | FAIL |
| SMALL | IS_SHARPE / IS_LEGS | `SMALL-band0.08-g1.00` | 6.16% / 0.666 / −18.62% | FAIL L2+L3+L5 | FAIL |
| SMALL | IS_CAGR | `SMALL-qroll-q0.12-w1008-d1.00` | 4.71% / 0.377 / −34.46% | FAIL all 5 | FAIL |

Comparands at the same split — **SPY** 15.21% / 0.871 / −33.72% (U56 calendar; full sample
15.10% / 0.883 / −33.72%, halves 0.959 / 0.821); **RULES v2 (live)** OOS 9.45% / 1.276 / −12.05%
(full 8.62% / 1.201 / −12.05%, halves 1.232 / 1.176). The best pick's full sample is
14.05% / 1.170 / −15.59%, halves **1.132 / 1.206**.
Across the whole legal walk-forward ladder: **OOS 4b 243 of 432, OOS 4b (REC_FULL) 234 of 432,
OOS 4a 0 of 432.** Every rule-8 pick's own OOS trough: `DD_2020-03-23` ×395, `DD_2022-10-12` ×37.

## (D) Both KEEP paths over the whole ladder (10 bps)
| grid | panel | rows | 4a | 4b (WIN) | 4b (REC_FULL) |
|---|---|---|---|---|---|
| LEGAL | U56 | 400 | 0 | 240 | 240 |
| LEGAL | B136 | 320 | 16 | 199 | 197 |
| LEGAL | SMALL | 288 | **0** | **0** | **0** |
| POST | U56 | 400 | 0 | 242 | 292 |
| POST | B136 | 320 | 16 | 140 | 192 |
| POST | SMALL | 288 | 0 | 0 | 0 |

SMALL passes **neither** path at any point — a 716-name sub-$2B panel cannot clear SPY's Sharpe
on this tape even with survivorship working for it.

## Gates (all printed before any hypothesis number was read)
G1 fast runner ≡ `engine.backtest` 6.94e-18 / 1.67e-16 · G2 `rules_v2_weights` 0.0 ·
G3 SPY OOS triple at the anchor 15.2102% / 0.8711 / −33.7173% vs committed, max|d| 1.70e-04 ·
G4 SHELF memo triples 9/9 · G5 determinism over the 6,048-row ladder 0.0 ·
G6 cross-run vs 1013/1022: legal-grid SPY |OOS MaxDD| range **6.66e-16** and the 2020 crash at
every legal end · G7 SMALL's SPY ≡ U56's SPY, 0.0 over 4,198 days ·
G8 episode labelling is a total partition and DD05 refines DD10 **on episode days**. G8's naive
whole-tape refinement reading is **False** and is published as such: the `CALM_` filler is a
fixed quarterly grid under both thresholds, so a 5%-only episode straddling a quarter boundary
necessarily touches two filler labels. The gate is the episode-restricted claim, which is the
one that has content; the failing reading is printed beside it rather than dropped.

## Hypotheses — 3 of 8 PASS
| id | bar | value | verdict |
|---|---|---|---|
| H_ONE | every panel × def cell == 1 (WIN, LEGAL) | max 2; the three >1 cells are all **SMALL / RULES v2**, i.e. the **4a** comparand | **FAIL** |
| H_TWO | ≥1 comparand cell ≥ 2 | 6 of 72 — all SMALL / RULES v2 / WIN; **zero** for SPY | **PASS** |
| H_BOOK | median book count ≥ 2 | median 1.00, mean 1.206, share ≥2 = 0.2063 | **FAIL** |
| H_MARGIN | median SPY margin ≥ 0.05 | **0.0922**, 0/48 ends under the bar | **PASS** |
| H_PANEL | panels disagree on the comparand | 1/1/1 in every def — SPY is SPY | **FAIL** |
| H_DEF | the definition moves ≥1 series | **0 of 213** series-cells move | **FAIL** |
| H_POST | POST comparand reaches ≥2 | 36 of 72 cells; WIN-only **36/36** | **PASS** |
| H_SMALL | \|mean book count SMALL − U56\| ≥ 0.50 | 1.444 vs 1.080, \|d\| 0.364 | **FAIL** |

H_ONE's FAIL is **not** a two-episode cap and must not be read as one: it is the 4a comparand on
one panel, moving by 0.0004 of drawdown. H_DEF's FAIL is the strongest number in the run — the
census is **completely definition-insensitive**, so the finding cannot be an artefact of how an
episode was drawn. H_BOOK's FAIL says the degeneracy is **not** a property of the tape: 13 of 63
books do move between episodes on the very same legal grid where the cap never does.

## Verdict
* **CONFIRM** the queue's claim, now on three panels and three mechanical episode definitions:
  4b's DD cap is a **single-episode test** — one month of 2020 — on every tape the record can
  reach, by a constant 0.0922 margin.
* **KILL** "a two-episode cap exists somewhere on the legal grid": 0 of 36 SPY comparand cells.
* **KILL** the panel dial as a remedy: SMALL's SPY is bit-identical to U56's (G7), so no panel
  the record can add moves the cap.
* **KEEP a PROTOCOL rule 4 DD-CAP EPISODE COUNT clause (proposed, not applied — rule 6 reserves
  rule changes to the Sunday review)** — `2026-09-16_dd-cap-episode-count-clause_B.memo.md`.

## Survivorship (PROTOCOL rule 9)
U56, B136 and SMALL are **current-constituent** lists; every CAGR level above is optimistic and
every 4b count is an upper bound. SMALL's bias is the worst of the three
(`data/SMALL_PANEL_README.md`). The measured object is **which calendar date** sets a drawdown;
survivorship reaches it only through a book's composition and not at all through SPY's, so the
comparand census is bias-free. Where it does bite — the book census — it makes books look
steadier, pushing counts **down**, so H_BOOK was the harder call and its FAIL is a lower bound.

## Not modified (PROTOCOL rule 6)
`RULES.md`, `PROTOCOL.md`, `research/scan.py`, `products/bot/bot.py`, `research/baseline.py`.
