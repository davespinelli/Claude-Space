# Idea 801 — is-every-MATCHED-LEVEL-GAP-in-the-record-an-OOS-WINDOW-fact (lane C, 2026-09-12)

**ANSWERED = YES. PREMISE CONFIRMED / KILL for every "absorbed once matched" verdict in the
record as written. No KEEP claimed.**

Script: `2026-09-12_is-every-MATCHED-LEVEL-GAP-in-the-record-an-OOS-WINDOW-fact_C.py`
Outputs: `.census.csv .prose.csv .rebuilt.csv .rungs.csv .feas.csv .grid.csv .windows.csv
.walkforward.csv .keeppaths.csv .published_windows.csv .console.txt`

## The headline

The record's matched-level B−S gap is **not a sample fact — it is a window fact, and the verdict
it carries is a post-2017 verdict.** Rebuilt on today's pooled panel (B136 135 names + SMALL 663,
4,198 bars), over 36 overlapping kernel-matched k=36 rungs on 11 characteristics:

| window (PROTOCOL split 2016-12-31) | mean \|gap\| | "absorbed" (mean \|gap\| < CARRIER 0.09805) |
|---|---|---|
| **IS 2010–2016** | **0.1594** | **1 of 11 characteristics** |
| **OOS 2017–2026** | **0.0787** | **8 of 11 characteristics** |
| FULL sample (what the record publishes) | 0.0915 | 5 of 11 |

The verdict **flips between IS and OOS in 9 of 11 characteristics (0.818)**, and the published
FULL-window verdict **differs from at least one window's verdict in 9 of 11**. At the rung level
|gap| is larger IS than OOS in **27 of 36 rungs**; the per-characteristic IS/OOS ratio has median
**2.889** (mean 2.651, range 0.817–5.12). In-floor counts move the same way: 15/36 rungs inside
the seed floor IS vs **23/36 OOS**.

Pre-registered results, all 6 tuned points reported:

| hypothesis | STRICT | WIDE | number |
|---|---|---|---|
| H_WINDOW (flips > 50%) | **PASS** | **PASS** | 0.818 at the PROTOCOL split |
| H_FULLMISLEAD (≥ 50%) | **PASS** | **PASS** | 0.818 |
| H_OOS_SMALL (majority) | **PASS** | **PASS** | 0.818 (1.000 at the 2017 split) |
| H_SPLIT (same majority at all 3 splits) | **PASS** | — | 2015 0.818 / 2016 0.818 / 2017 0.727 |
| H_STABLE (falsifier: agreement ≥ 0.80) | **FAIL** | **FAIL** | agreement 0.182 |
| H_CENSUS (< 50% of rows carry the cut) | **FAIL** | **FAIL** | 123/165 and **144/187 = 0.770** |

## H_CENSUS fails in the informative direction

The cut is **already in the record** — 144 of 187 committed matched-level gap rows (77.0%, over 4
of 8 `*.origin.csv` files) carry `gap_IS` / `gap_OOS` columns. **No published verdict uses them.**
Read from the record's own columns: mean |IS| 0.2062 vs |OOS| 0.1672, verdict flips in 2 of 8
published (file, char) cells, FULL misleads in 2 of 8. The record's own data points the same way
as the rebuild, weakly — because the files that published the cut are dominated by `cvol` and
`breadth` cells matched on a residual/hbucket scheme, where the drift runs the *other* way
(cvol −0.1578 and −0.1136 IS−OOS in two files). So the columns exist, are ignored, and the two
matching schemes do not even agree on the sign of the window effect.

## What survives the cut

Only **`mompers` and `mrho`** give the same verdict in both windows — and both give NOT-absorbed
(|gap| 0.0997 / 0.1049 FULL, 0.1174 / 0.1329 IS, 0.1377 / 0.1317 OOS). Every characteristic the
record has ever called "absorbed once matched" — `tpers` 0.0439, `momac` 0.1143, `plevel` 0.0436,
`beta` 0.0713, `volpers` 0.0848, `momsgn` 0.0886 — is absorbed only after 2017. Idea 571's and
796's `momac` headline is the clearest case: |gap| 0.2261 IS against 0.0729 OOS. `momsgn` is the
one cell that flips the other way at the PROTOCOL split (IS 0.0944 absorbed, OOS 0.1156 not), and
it stops flipping at all at the 2017 split — the flip count is a majority at every split date but
which characteristics flip is not stable, which is itself a reason not to quote any single cell.

Match quality is not the explanation: median |achieved_B − achieved_S| is **0.0038** across the 36
rungs (max 0.1795, on `plevel`, where BONLY cannot reach the low rungs at all — 19 of 165 planned
rungs are infeasible and are reported, not dropped).

## Rule 8

**WF-A** *is* the answer above: the gap and its verdict are recomputed inside each window at every
(characteristic, split), and the IS→OOS verdict drift is the finding.

**WF-B** takes the absorption claim as a trading instruction — "at matched characteristic the panel
of origin does not matter, hold whichever arm is available" — and picks
(char, flavour, level, seed, gross, cadence) by **IS Sharpe alone** over the overlapping rungs,
reading OOS once:

| selector | IS pick | IS Sharpe | OOS CAGR | OOS Sharpe | OOS MaxDD | 4b fails |
|---|---|---|---|---|---|---|
| ANY-ARM | beta/POOL/L0.551/s5/g1.00/M | 1.6022 | 7.47% | 0.4810 | −41.15% | H2, OOS, DD |
| BONLY | mrho/BONLY/L0.176/s3/g1.00/M | 1.4633 | 23.05% | 1.2787 | −26.79% | DD |
| SONLY | beta/SONLY/L0.551/s2/g1.00/M | 1.4074 | 11.73% | 0.6909 | −40.40% | H2, OOS, DD |

Comparands: RULES v2 OOS **9.47% / 1.2782 / −12.05%** (U56) and 7.88% / 1.1059 / −12.24% (B136);
**SPY OOS 15.33% / 0.8767 / −33.72%**. The IS chooser lands on a book that loses SPY on OOS
Sharpe by 0.396 and on CAGR by 7.9pp, at 1.22x SPY's drawdown. The instruction does not transport.

And the claim is wrong in level terms even where the gap is small: over the **same** overlapping
rungs, mean OOS Sharpe is **BONLY 0.9988 vs SONLY 0.4257 (+0.5731)** — the panel of origin matters
enormously; what matches is only the MA-gate *premium*, a difference of differences.

## KEEP paths (10,512 books; 4a vs RULES v2 on each draw's own panel, 4b vs SPY)

4a **24**, 4b **147**, BOTH **2**. Binding 4b legs: DD 9,264 / H2 7,974 / OOS 7,894 / CAGR 6,037 /
H1 5,647. Every 4b passer is BONLY (141) or POOL (6); **SONLY 0**. The two BOTH books are
`mrho/BONLY/L0.176/s3/MA-RS/g0.50/W` (11.12% / 1.3633 / −13.09%) and
`volpers/BONLY/L0.951/s1/MA-RS/g0.50/W` (10.10% / 1.2249 / −13.32%).

**No KEEP is claimed.** Each is a seeded kernel-weighted draw of 36 names built to answer a
measurement question; it is not a rule anyone can hold, and the 4b pass is a diagnostic that the
BONLY arm is simply large-cap beta with an MA gate.

## Gates

G1 identity `fast_backtest` vs `engine.backtest` max |Δreturn| **2.776e-17** (bar 1e-9) — PASS.
G2 determinism **0 of 876** draws differ on rebuild — PASS. G3 census idempotent, row count
matches a direct read (diff 0) — PASS. G4 vintage is **measured, not gated**: idea 796 established
that the pooled name set and every pooled quantile have moved on re-stated closes, so a 1e-9
reproduction of idea 571's rows would fail for reasons unrelated to this question.

## Caveats

Survivorship: the pool is current constituents of `universe_broad.json` plus the current sub-$2B
screen (every `max_1d_move >= 1.0` ticker dropped per PROTOCOL). Dead SMALL names are absent, so
the S-sourced premium is biased **up** and |gap| is **shrunk in both windows** — the bias cannot
manufacture a window *difference*, which is the quantity measured here. `breadth` (22 committed
rows) is censused under CLAIMSET=WIDE but is a panel-level characteristic matched by a
residual/hbucket scheme, not the kernel draw, so it is **not** rebuilt — stated, not hidden.
Costs 10 bps per unit turnover, next-day fills, no shorting, no leverage.

## What this means for the record

Any committed statement of the form "at matched *X* the panel of origin is absorbed" is, on this
machinery, a statement about 2017–2026 only. The honest form is two numbers, not one. Nine of
eleven characteristics change verdict at the cut, the falsifier fails at 0.182 agreement, and the
record's own unused `gap_IS`/`gap_OOS` columns were sitting in 77% of its committed rows the whole
time.
