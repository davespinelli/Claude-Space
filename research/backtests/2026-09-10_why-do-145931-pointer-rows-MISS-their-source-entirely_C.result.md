# Idea 661 — why do 145,931 pointer rows MISS their source entirely?

**lane C, 2026-09-10 · KILL for capital, ANSWERED for the record · the queue's dichotomy is REAL but LOPSIDED: 99.25% transformation, 0.74% vintage drift**

Script: `2026-09-10_why-do-145931-pointer-rows-MISS-their-source-entirely_C.py` (400.6 s, deterministic, no network).
Artefacts: `.pointers.csv` (250) `.miss.csv` (250) `.misspairs.csv` (3,940) `.missgrid.csv` (72) `.claims.csv` (102) `.grid.csv` (90) `.walkforward.csv` (6) `.keeppaths.csv` (6) `.console.txt`.
**No RULES change, no book promoted, no KEEP claimed, no memo.** RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py untouched.

## Gates (all PASS, run before any new number was read)

| gate | result |
|---|---|
| G1 FRESH book == `baseline.rules_v2_weights`, and both channels meet there | max&#124;dW&#124; **0.000e+00**, max&#124;dR&#124; **0.000e+00**, DRIFT@L=0 **0.000e+00**, TRANS@b=0.03 **0.000e+00** |
| G2 cost-rung identity `r(25) = r(0) − turn·25/1e4` vs a live `engine.backtest(25)` | max&#124;d&#124; **0.000e+00** |
| G3 idea 655's miss population re-derived on its OWN 246 instances | **246/246 exact**, max&#124;d&#124; **0**; queue block **105,504 rows / 29,127 misses (0.2761)**, exact; 655's artefact self-consistent with QUEUE 661's quoted 145,931 / 0.1341 |
| G4 class partition exact at every tolerance rung | PASS (RECOVERED + T + V + X == misses at all 6 rungs) |

The corpus is append-only and has grown since 655 ran (655's own artefacts among them), so today's totals are a **superset**: **250 instances / 1,089,229 pointer rows / 146,008 misses (0.1340)** vs 655's 246 / 1,088,554 / 145,931 (0.1341). The gate is exact reproduction on the instances 655 scanned, not equality of totals.

## (1) The answer — it is not vintage drift, and it is not rounding

146,008 miss rows over **3,940 (child, col, source) pairs**. Classified at the exact rung:

| class | rows | share |
|---|---|---|
| **TRANSFORM** (≥1 shared key column whose miss values NEVER appear in the source's column) | **144,918** | **0.9925** |
| VINTAGE (not transform, source provably younger than the child) | 1,076 | 0.0074 |
| PHANTOM (not transform, no vintage evidence — every key value exists, the tuple does not) | 14 | 0.0001 |

`min_col_overlap` is **exactly 0.0 on 144,918 of 146,008 rows**: the mismatch is total, not marginal. Only 1,090 rows show any partial overlap.

**Tolerance recovers almost nothing.** Snapping numeric key cells to 1e-6 / 1e-4 / 1e-2 / 5e-2 recovers 0 / 23 / 2,016 / 3,443 rows; recovered at **ANY** rung, **3,455 (2.37%)**. The raw ladder is monotone here, but monotonicity is reported, not gated — a wider quantum can split a child and its source into different bins.

**The vintage leg is an upper bound and still explains nothing.** Git coverage is 3,940/3,940 pairs on both sides, and the test is permissive (`source_commit >= child_commit`, i.e. same-commit counts as younger) on a **shallow 50-commit clone** spanning 2026-09-10 11:42–19:58Z. The filename-date channel — every artefact is `YYYY-MM-DD_slug_lane.suffix.csv` — finds **0** forward-dated reads. Even at its most permissive the vintage hypothesis carries 0.74%.

## (2) The mechanism, named: the record joins on LABELS whose vocabularies differ

Zero-overlap key columns, weighted by miss rows:

| key column | rows | share | kind |
|---|---|---|---|
| `family` | 39,092 | 0.2677 | label |
| `dial` | 36,467 | 0.2498 | label |
| `panel` | 30,702 | 0.2103 | label |
| `OOS_MaxDD` | 9,954 | 0.0682 | re-derived metric |
| `OOS_CAGR` | 8,658 | 0.0593 | re-derived metric |
| `n`, `regret`, `pass4b`, `cell`, `oos_best`, `m_*` | ≤4,972 each | — | mixed |

Three **label** columns carry **58.8%** of the whole miss population, and **79,707 misses (54.6%) join on a SINGLE key column**. The child is not reading a moved source; it is reading a source that never used its words — `family`/`dial`/`panel` taxonomies are re-coined per run. The second block is re-derived floats (`OOS_MaxDD`, `OOS_CAGR`, `m_*`): the child **recomputed** the metric instead of copying it, so the cell is a transform by construction, which is why tolerance cannot rescue it.

## (3) How many published claims read a source that no longer says what they quote

| | count |
|---|---|
| child files carrying at least one miss | 102 |
| still unmatched under the most generous reading (recovered at ANY rung) | **101** (142,553 rows) |
| …with a committed `.result.md` memo | 98 |
| …cited by LEADERBOARD.md / CHANGELOG.md / QUEUE.md | 101 |
| **published claims resting on an unmatched read** | **101** (142,553 rows) |

Every affected file but one is published. The largest single unmatched read is 25,153 rows (`…STEP-NORMALISED-argmin_cloud.cells.csv` → `2026-09-09_does-a-random-sub-panel-pass-4b…`, zero-overlap column `family`).

## (4) The two miss classes, priced (PROTOCOL 4 both paths, rule 8)

The census question has an exact book analogue. **DRIFT** = the vintage failure: the 200d band state is read L trading days stale. **TRANSFORM** = the key-is-not-a-copy failure: the same rows keyed through a band b ≠ the source's 0.03. Both meet the live book at (L=0, b=0.03) = RULES v2 (G1). 90 grid points, all reported.

At matched gross 0.75, worst point of each channel vs FRESH:

| panel | channel | worst Sharpe | ΔSharpe | ΔMaxDD |
|---|---|---|---|---|
| U56 | DRIFT (L=42) | 0.984 | **−0.218** | **−9.06 pp** |
| U56 | TRANS (b=0.20) | 1.114 | −0.088 | −0.02 pp |
| B136 | DRIFT (L=42) | 0.978 | **−0.128** | **−11.00 pp** |
| B136 | TRANS (b=0.20) | 1.038 | −0.068 | −3.63 pp |

**Staleness is the expensive failure and it is paid in drawdown**; the transform failure is 1.9× (B136) to 2.5× (U56) cheaper in Sharpe, and on U56 essentially free in MaxDD (−0.02 pp against DRIFT's −9.06 pp). The record fails 99.25% of the time in the way that costs least when priced — and 0.74% of the time in the way that costs most.

Rule-8 picks ((level, gross) fitted on 2009–2016, scored 2017–2026 untouched):

| panel | mode | pick | OOS CAGR | OOS Sharpe | OOS MaxDD | 4b @ 0/10/25 bps |
|---|---|---|---|---|---|---|
| U56 | FRESH | L=0 g=1.00 | 12.71% | 1.278 | −15.91% | 1/1/1 |
| U56 | DRIFT | L=2 g=1.00 | 12.47% | 1.225 | −16.42% | 1/1/1 |
| U56 | TRANS | b=0.10 g=1.00 | 12.19% | 1.197 | −16.30% | 1/1/1 |
| B136 | FRESH | L=0 g=1.00 | 10.66% | 1.117 | −16.16% | 1/1/0 |
| B136 | DRIFT | L=0 g=1.00 | 10.66% | 1.117 | −16.16% | 1/1/0 |
| B136 | TRANS | b=0.10 g=1.00 | 11.22% | 1.104 | −19.20% | 1/1/1 |

References — U56: SPY OOS Sharpe 0.876 / CAGR 15.32% / MaxDD −33.72%, RULES v2 1.279 / 9.48% / −12.05%. B136: SPY 0.882 / 15.45% / −33.72%, v2 1.119 / 7.98% / −12.24%.

**6/6 picks beat SPY's OOS Sharpe, 0/6 beat the live book, 0/6 clear 4a.** No pick improves on FRESH on any panel: every degradation of the read is a loss, and rule 8 picks the least-degraded point available to it.

## (5) Why nothing here is promotable

Full-sample **4a 0/90, 4b 19/90, BOTH 0/90** — and **all 19 4b passes sit at g=1.00, 0 at g=0.75, 0 at g=0.50**, while Sharpe is flat in gross to 3 dp (U56 1.2022 / 1.2021 / 1.2020; B136 1.1057 / 1.1058 / 1.1057 at g = 0.50 / 0.75 / 1.00). The entire 4b footprint is the **CAGR floor moving with gross**, not a book: idea 311's gross-band loophole and open idea 657's exact question, reproduced a third time. FRESH@g=1.00 *is* the live book with one dial moved.

## Verdict

**KILL for capital. ANSWERED for the record.** Nothing is promoted. The queue's dichotomy is settled and lopsided: 99.25% of the record's 146,008 unjoinable pointer rows are **transformation** — three re-coined label vocabularies (`family`, `dial`, `panel`) plus recomputed rather than copied metric floats — 0.74% vintage drift under a deliberately permissive test, 0.01% phantom, and 2.37% recoverable by any tolerance. 101 published files rest on 142,553 unmatched reads. Priced live, the record's dominant failure mode is the cheap one (−0.068..−0.088 Sharpe) and its rare one is the expensive one (−0.128..−0.218 Sharpe, −9.1..−11.0 pp MaxDD).

Recommended follow-ups are filed to QUEUE as ideas 663–665.
