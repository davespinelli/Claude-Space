# Idea 741 — restate the 58,529 v1-EXPOSED rows of the pre-2026-09-06 record

**lane C, 2026-09-11.** 10 bps, next-day execution, weekly comparand cadence, gross 0.75 on the
book population. Script: `2026-09-11_restate-the-58529-v1-EXPOSED-rows-of-the-PRE-2026-09-06-record_C.py`
(runtime 53 s). Two tuned parameters: ROW SET (6 census tiers) × CONVENTION (6 candidates);
every grid point published.

## Verdict

**ANSWERED / KILL OF THE RESTATEMENT. The old record loses nothing and gains nothing, because
the queue's 58,529 is not the old record and the old record does not quote the convention under
audit.** No KEEP, no memo, no candidate, no RULES or PROTOCOL edit. `RULES.md`, `PROTOCOL.md`,
`scan.py`, `bot.py` and `baseline.py` untouched.

## Gates

| gate | bar (pre-registered) | result |
|---|---|---|
| **G1** REPRODUCTION | idea 737's census integers **exactly**; its 324-book grid < 1e-9 | **PASS** |
| **G2** VINTAGE | per-date match rate of all 6 candidates (no bar) | reported |
| **B1** is the 58,529 the old record? | ≥ 50% of the v1-exposed rows are pre-2026-09-06 | **FAIL — 7.13%** |
| **B2** anything to restate? | ≥ 1 v1-era block uniquely identified as CROSSv1 | **FAIL — 0 blocks** |
| **B3** which leg binds? | MaxDD explains ≥ 50% of the v1 flips | **PASS — 97.71%** |
| **B4** 4b untouched | 0 rows change 4b across all 6 candidates | **PASS — 0** |
| **B5** fresh decision | SAMEv1 ≠ CROSSv1 4a count on the 12 rule-8 picks | **PASS — 5/12 vs 1/12** |

**G1** is asserted on idea 737's **own file set** (the 375 files named in its committed
`.census.csv`), because the corpus has grown by 3 files since 737 ran. On that set every
published integer comes back exactly: `qual_files` 375, `qual_rows` 433,949, `canon_rows`
386,109, `blocks_canon` 1,018, `exposed_v1` **58,529**, `exposed_rows` 2,949, `flip_F2T` 2,944,
`flip_T2F` 5, `exposed_spy` 1,079, and the v1 flip split 58,340 / 189. The 324-book grid
rebuilds to max |d| **2.220e-16**. The queue's stated mechanism also reproduces to the published
digit: RULES v1 MaxDD **−13.83%** on U56 against **−44.83%** on SMALL484. The current corpus
(378 files / 434,321 rows / 386,481 CANON rows / 1,027 blocks) is the working population for
everything below: v1-exposed **58,563**, v2-exposed 2,964.

One bookkeeping correction to 737, filed rather than left standing: its `qual_rows` (433,949)
exceeds the sum of its own census blocks (433,445) by **504 rows**. Those 504 rows are a single
file's NA panel label, which survives `.astype(str)` as pandas NA and is dropped by `groupby`.
They are correctly outside CANON in both runs; only the file-level row count saw them.

## B1 — the 58,529 is overwhelmingly NOT the pre-2026-09-06 record

| era | blocks | rows | v1-exposed | share of 58,529 | cross-FAIL→same-PASS | reverse |
|---|---|---|---|---|---|---|
| **V1ERA** (pre-2026-09-06) | 146 | 31,571 | **4,176** | **7.13%** | 4,172 | 4 |
| V2ERA | 881 | 354,910 | 54,387 | 92.87% | 54,200 | 187 |

The v1 pair's 15.16% exposure is a **counterfactual computed across the whole corpus**: 92.87% of
it sits on rows published *after* RULES v2 went live, which quote a v2 comparand and can never
be restated onto a v1 one. The queue's title — "the 58,529 v1-EXPOSED rows of the PRE-2026-09-06
record" — mis-attributes the count. The old record's share is **4,176 rows**, 1.08% of CANON.

G2 licenses that era cut empirically rather than by assertion. Row-weighted share of published
4a cells each candidate reproduces, by filename date:

| date | rows | SAMEv2 | SAMEv2_noSPY | CROSSv2 | SAMEv1 | SAMEv1_noSPY | CROSSv1 | best |
|---|---|---|---|---|---|---|---|---|
| 2026-09-05 | 28,813 | 0.6968 | 0.6967 | 0.6959 | **0.8748** | 0.8703 | 0.7554 | SAMEv1 |
| 2026-09-06 | 24,289 | 0.7722 | 0.7666 | 0.7503 | 0.8465 | 0.8488 | **0.8687** | CROSSv1 |
| 2026-09-07 | 20,151 | 0.8807 | **0.8808** | 0.8774 | 0.7575 | 0.7515 | 0.8507 | SAMEv2_noSPY |
| 2026-09-08 | 64,725 | 0.9816 | **0.9823** | 0.9807 | 0.7739 | 0.7649 | 0.9504 | SAMEv2_noSPY |
| 2026-09-10 | 174,407 | 0.9932 | 0.9947 | **0.9966** | 0.7926 | 0.7883 | 0.9515 | CROSSv2 |

Pre-cut dates read a v1 candidate as best, post-cut dates a v2 one, with **2026-09-06 itself
transitional** — which is why `V1ERA6` is published as a second tier throughout.

Exposure is also entirely a non-U56 phenomenon: **U56 v1-exposed 0 (0.00%)** by construction
(on U56, CROSSv1 *is* SAMEv1 — same frame, same book), against B136 32.77%, SMALL484 25.12%,
SMALL439 5.78%.

## B2 — the restatement, and why it costs the old record nothing

LOST = published PASS → restated FAIL; GAINED = published FAIL → restated PASS.

| tier | blocks | rows | scorable | pub PASS | SAMEv2 | CROSSv2 | **SAMEv1** | **CROSSv1** |
|---|---|---|---|---|---|---|---|---|
| CANON737 | 1,027 | 386,481 | 361,105 | 19,842 | 17,829/2,134 | 19,142/542 | 5,952/73,145 | 12,096/23,476 |
| **V1ERA** | 146 | 31,571 | 28,823 | 8,805 | 8,737/0 | 8,763/0 | **3,327/284** | **7,029/19** |
| V1ERA6 | 329 | 71,728 | 53,112 | 15,077 | 14,232/37 | 14,815/12 | 4,655/2,684 | 9,518/718 |
| V1ERA_EXPOSED | 77 | 18,588 | 16,876 | 7,259 | 7,216/0 | 7,242/0 | 2,972/269 | 6,674/4 |
| **V1ERA_IDENT** | 26 | 2,635 | 2,635 | 586 | 583/0 | 586/0 | **3/5** | **312/5** |
| V1ERA_UNIQ_CROSSv1 | **0** | 0 | 0 | 0 | — | — | — | — |

Restricted to the rows the convention can actually move (SAMEv1 ≠ CROSSv1):

| tier | exposed rows | published PASS among them | SAMEv1 lost/gain | CROSSv1 lost/gain |
|---|---|---|---|---|
| V1ERA | 3,975 | 3,702 | **0 / 269** | **3,702 / 4** |
| V1ERA_IDENT | 317 | 309 | 0 / 4 | 309 / 4 |

**On every exposed v1-era row that was published as a PASS, the same-panel v1 bar agrees.**
Restating the old record on SAMEv1 costs it **zero** published passes and hands it 269 new ones;
restating it on CROSSv1 would destroy 3,702 of the 3,702. The old record already reads
same-panel.

Identification says the same thing directly. Of the 146 v1-era blocks, **7 are uniquely
identified** (1,108 rows) and every one of them is a SAME convention — SAMEv1 968 rows,
SAMEv1_noSPY 140 rows. **Zero blocks are uniquely CROSSv1.** No committed pre-2026-09-06 block
can be shown to have used the cross-panel v1 comparand, so **no published verdict is established
to need restating**.

At claim level (a block is one idea, a row one of its grid cells), on the clean `V1ERA_IDENT`
tier only **3 of 26 blocks** change a single cell under SAMEv1 and **1** loses a published PASS,
against 9 of 26 and 8 under CROSSv1. The raw `V1ERA` tier's 110 of 133 is not a restatement
count: it is dominated by blocks whose real comparand this sandbox cannot rebuild at all (idea
739: 133 blocks / 103,736 rows reach no knob setting of the PROTOCOL book), where a
published-vs-recomputed disagreement prices the *unidentified comparand*, not the convention.

## B3 — the queue's mechanism is right

Scoring each flip on the leg that fails on its **failing** side (a SAMEv1-PASS / CROSSv1-FAIL row
is scored on its CROSSv1 legs, and vice versa), over all 58,563 v1-exposed rows: **MaxDD binds
97.71%** (57,220), H2 18.18% (10,649), H1 2.48% (1,452); legs are not exclusive. Per panel the
MaxDD share tracks the SAMEv1−CROSSv1 drawdown spread exactly as 737 predicted: B136 −0.0736
(46,575 of 47,227), SMALL439 −0.2230 (3,117 of 3,325), SMALL484 −0.3100 (7,528 of 8,011). The
20× is the drawdown leg, confirmed.

## Both KEEP paths

4a on the 324-book audit population, and on the 12 rule-8 picks:

| convention | 4a /324 | 4a /12 |
|---|---|---|
| SAMEv2 (the live bar) | 9 | **0** |
| SAMEv2_noSPY | 9 | 0 |
| CROSSv2 | 0 | 0 |
| SAMEv1 | 72 | **5** |
| SAMEv1_noSPY | 77 | 4 |
| CROSSv1 | 48 | **1** |

**4b is 16/324 and 1/12, identical under all six candidates (B4 PASS)** — 4b's legs read SPY and
the row itself, both panel-local in every convention.

## Rule 8 walk-forward

12 arms = 3 panels × 2 gate families × 2 constructions. Each arm's (level, cadence) chosen on IS
Sharpe over **2010–2016 alone**; 2017+ read once. Picks: OOS Sharpe **0.5655 … 1.2168**, OOS CAGR
**1.04% … 24.02%**, OOS MaxDD **−35.07% … −3.38%**.

Beats OOS Sharpe: **SPY 8/12**, SAMEv2 (live baseline) 7/12, SAMEv2_noSPY 7/12, CROSSv2 0/12,
SAMEv1 11/12, SAMEv1_noSPY 11/12, CROSSv1 8/12. OOS comparand Sharpes — U56: SAMEv2 1.2747 /
SAMEv1 0.7309 / SPY 0.8721; B136: 1.1185 / 0.5763 / 0.8820; SMALL439: 0.5680 / 0.4923 / 0.8820.

4a on the 12 fresh picks splits **5/12 under SAMEv1 against 1/12 under CROSSv1** (B5 PASS) — the
v1 convention genuinely moves an out-of-sample decision. But under the **live** v2 bar the same
12 picks score **0/12 either way**, as they do under CROSSv2. The convention question is
**archival**: it is material only on a comparand the book retired on 2026-09-06.

## What this does and does not license

- **No restatement is owed.** Where the pre-2026-09-06 record is identifiable at all it already
  quotes the same-panel v1 comparand, and on its exposed published passes the two conventions
  agree 3,702 for 3,702.
- **737's 58,529 should be quoted as a corpus-wide counterfactual, not as the old record.** The
  old record's share is 4,176 rows (7.13%), and 0 of its blocks are provably CROSSv1.
- **Nothing here touches the live bar.** 4b is convention-invariant (B4), and the live v2 4a bar
  gives 0/12 on fresh picks under every reading.
- No PROTOCOL clause is proposed. Idea 737's proposed rule-3 wording already covers the live
  case; this run removes the archival motive for back-dating it, it does not add one.

## Caveats

(i) **SURVIVORSHIP** (idea 54): all four panels are current constituents, no delistings, so every
CAGR level is inflated; the convention contrast is a comparand-minus-comparand difference on the
same panel and window and is largely immune. (ii) A **row is a grid cell**, not a headline claim —
read claim-level impact off the block table, not the row counts. (iii) The classifier recognises
only a comparand it can **rebuild**; unidentified blocks are counted as such and never assigned,
which is why `V1ERA_IDENT` is published as the clean reading beside the raw one. (iv) Six
conventions over one corpus are not six independent experiments. (v) The era cut is a **filename
date**, validated empirically by G2, not a commit timestamp; 2026-09-06 is transitional and is
published both ways (`V1ERA` / `V1ERA6`).
