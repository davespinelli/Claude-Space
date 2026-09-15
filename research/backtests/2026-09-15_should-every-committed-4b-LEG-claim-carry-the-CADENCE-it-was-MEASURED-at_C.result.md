# Idea 984 (lane C, 2026-09-15) — should every committed 4b LEG claim carry the CADENCE it was MEASURED at?

**ANSWER = YES, AND THE RECORD ALMOST NEVER DOES. 80.9% of committed leg-binding claims name no
cadence, 81.6% of those name `L4_DD`, and 84.2% of them do not survive being read on the D/W half
of the record's own ladder. KEEP as a PROTOCOL rule 4 reporting clause (proposed, not applied —
rule 6). KILL for reading any cadence-free leg-binding claim as a general fact. Nothing promoted;
`RULES.md`, `PROTOCOL.md`, `scan.py`, `bot.py`, `baseline.py` untouched.**

## The grid and the corpus

The ladder is rebuilt from scratch, not re-read: 3 panels {U56, B136, SMALL} × 5 books × 2 gross
{CORE 0.75, EXT 1.00} × D/W/M/Q at **matched gross** × every rebalance phase inside each cadence
(D 1, W 5, M 21, Q 63) = **2,700 phase-books**, each at 5 cost rungs = **13,500 rows**, plus 36
rule-8 picks. The corpus is the record's own prose: **430 committed leg-binding claims** harvested
from `LEADERBOARD.md` (172), `CHANGELOG.md` (151) and 79 committed `*.result.md` / `*.memo.md`
files (107). Two tuned axes only — claim set {STRICT, WIDE, FILES} and ladder half {FINE2 = D/W,
COARSE2 = M/Q, CORE4} — **all points reported, none selected**; the cadence-detection context
(SENTENCE vs whole ROW) is a reported axis, and both are published everywhere.

## The census

| claim set | n | states a cadence | **SILENT** | SILENT (whole-row context) | DD share of the silent |
|---|---|---|---|---|---|
| STRICT (explicit `L#_` token + binding verb, LEADERBOARD + CHANGELOG) | 47 | 9 | **0.809** | 0.617 | 0.816 |
| WIDE (+ prose leg names in a 4b row) | 323 | 21 | **0.935** | 0.675 | 0.728 |
| FILES (+ every committed result/memo file) | 430 | 26 | **0.940** | 0.742 | 0.713 |

By leg the corpus is `L4_DD` 311, `L5_CAGR` 108, `L1_H1` 8, `L3_OOS` 2, `L2_H2` 1; by statistic
type `S_ONLY` 224, `S_RATE` 171, `S_MODAL` 22, `S_DDTEST` 13. **H_SILENT PASS at 0.809** against a
0.50 bar, and it passes at all six (claim set × context) points — the most generous reading of the
record, whole-row context on the strictest claim set, still leaves **0.617** of leg-binding claims
with no cadence anywhere in the row that carries them.

## The re-score — what the silence costs

Each (leg, statistic) the silent claims assert, measured on both halves of this run's own ladder at
10 bps, cadence-balanced (D and W weighted equally against M and Q, since the ladder carries 1 / 5 /
21 / 63 phases):

| statistic | M/Q | D/W | Δ |
|---|---|---|---|
| `L4_DD` fail rate | **0.879** | **0.640** | −0.239 |
| `L4_DD` is the ONLY failed leg | **0.388** | **0.097** | −0.292 |
| `L4_DD` is the MODAL failed leg | **1.000** | **0.500** | −0.500 |
| `L1_H1` fail rate | 0.293 | 0.580 | +0.287 |
| `L1_H1` is the MODAL failed leg | 0.000 | 0.500 | +0.500 |
| `L5_CAGR` fail rate | 0.350 | 0.483 | +0.134 |
| `L3_OOS` fail rate | 0.448 | 0.560 | +0.112 |
| `L2_H2` fail rate | 0.488 | 0.533 | +0.046 |

**The two halves do not disagree about magnitudes, they disagree about WHICH LEG IS THE TEST.**
Every DD statistic falls when the book is sped up and every other leg's rises; `L1_H1` goes from
never-modal to modal on half the fast cells. **H_MOVE PASS at 0.842** (32 of the 38 STRICT silent
claims), **H_GAP PASS at 0.235** (claim-weighted mean |Δ|, bar 0.20), **H_DD PASS at 0.816**.

**The claim-level check, which is the strict one.** 9 of the 38 STRICT silent claims publish a
number this ladder can LOCATE (its published value matches the M/Q value within 0.10). Of those,
**1 of 9 (0.111)** still matches on D/W. On the FILES corpus **43 of 404** are locatable and **17
(0.395)** survive. The remaining silent claims are re-scored against the record-wide statistic for
their (leg, type) rather than their own population — stated, not hidden: that is an
under-determination measure, not a per-claim refutation.

## Rule 8

36 picks = 3 panels × 4 cadences × 3 IS-only choosers, (book, gross) chosen on **2009–2016 alone**,
2017–2026 read once, all 36 live. **`L4_DD` among the failed legs: M/Q 18 of 18 (1.000), D/W 5 of
18 (0.278), gap +0.722 — H_RULE8 PASS** against its 0.40 bar. The ONLY failed leg on **6 of 18**
M/Q picks and **0 of 18** D/W picks. **OOS 4b 4 of 36, OOS 4a 0 of 36**; full sample over the
2,700-row 10 bps grid 4b **140**, 4a **5**. Comparands: **SPY OOS 15.27% / 0.8741 / −33.72%**;
RULES v2 (live) full-sample Sharpe / MaxDD U56 1.201 / −12.05%, B136 1.099 / −12.24%, SMALL 0.664 /
−13.89%. All four OOS 4b passes are one object — **U56 / `BAND03` / gross 1.00, daily 12.46% /
1.288 / −14.77% and weekly 12.68% / 1.277 / −15.91%** — the same book ideas 973, 981 and 982 each
surfaced and each declined. **It is NOT promoted:** 4a fails on every panel, because gross 1.00
buys roughly a third more return for a third more drawdown than the live book's −12.05%. This run
records the fourth refusal, not a fourth sighting.

## Gates — 9 of 9 PASS, printed before any result number

G0 `offset_mask(.,per,0)` == `engine.rebalance_mask` on D/W/M/Q, 0 rows. G1 fast `Ctx` ==
`engine.backtest` on returns AND turnover post warm-up, D and M, max|d| **2.776e-16**. G2
`BAND03@0.75` == `baseline.rules_v2_weights` 0.000e+00. **G3 CROSS-RUN: idea 981's committed
13,500-row ladder reproduced on 13,500 of 13,500 rows, max|d| 7.105e-15 (on `turn_per_yr`) over 38
shared numeric columns, 0 4b-verdict flips.** **G4 CROSS-RUN: 981's published pooled `L4_DD` fail
rates 0.633 / 0.647 / 0.832 / 0.927 recomputed EXACTLY at D/W/M/Q (max|d| 3e-4, rounding).** G5
matched gross: target weight matrix identical across all four cadences on all 30 (panel, book,
gross) triples, 0.000e+00. G6 determinism 0.000e+00. G7 every chooser IS-only, 0 disagreements
under permuted OOS columns. **G8 harvester recall: idea 968's "89.2%" and idea 976's "36 of 36" —
the two claims the queue names by hand — are both found and both classified, 0 double-counted
rows.** The marginal one-way eta² table also reproduces 981's published 0.7435 / 0.5991 / 0.6470 /
0.4556 (H1 / H2 / OOS / CAGR on panel) and 0.0384 (DD on panel) exactly, from an independent build.

## Survivorship (rule 9)

U56 / B136 / SMALL are current-constituent lists (SMALL additionally drops the 52 tickers with
`max_1d_move` >= 1.0 per `data/small_meta.csv`), so every CAGR and drawdown LEVEL is optimistic and
every `L4_DD` fail rate is a LOWER bound. The object measured here is a **difference between two
halves of the same ladder** — same names, same tape, only the rebalance schedule moves — and is
very nearly immune. The rule-8 4b levels are read against SPY, which is not survivorship-inflated,
so every 4b PASS is an upper bound and every FAIL is understated.

## Limits, stated

The harvester is a sentence-level regex over markdown; a cell that packs three claims into one
sentence is counted once, and a claim whose cadence is stated two sentences away is counted as
silent under SENTENCE context — which is exactly why the ROW context is published beside it at
every point. The re-score is against the record-wide statistic except on the located subset. The
corpus is the record's PROSE; ideas 979 and 982 already priced the sibling defect on the record's
CSV artifacts, and the two censuses are not the same denominator.

## Proposed, not applied (rule 6)

`2026-09-15_cadence-scoped-leg-claim_C.memo.md` proposes the PROTOCOL rule 4 reporting clause, in
exact wording, together with the reading rule for the 404 claims already committed without one.
Follow-ups filed: 986, 987, 988.
