# Idea 1570 (lane cloud, idea 1 of 2) — how LONG a tape would resolve the record's typical device margin, and does POOLING resolve it?

**VERDICT: KILL for capital (pre-registered H_WALL fired).** The device family is real, it passes
4b, and it cannot be distinguished from a constant de-gross on any tape this century.

## ARM A — the census of the record's own 2026-09-19 output
287 committed CSVs scanned. A column trio `(d, se, t)` is admitted only if `se` is *named* like a
standard error, `t` like a t statistic, and `d/se` reproduces `t` to 1e-6 on >= 98% of finite rows
with >= 3 distinct `t` values (G9 — constant and boolean columns cannot match by accident).
**50 internally validated triples, 4,371 contrast rows.**

| statistic | value |
|---|---|
| \|t\| distribution | min 0.000, q25 0.299, **median 0.712**, q75 1.237, q90 2.110, q95 2.885, max 7.648 |
| already resolved (\|t\| > 2) today | **481 of 4,371 = 11.00%** |
| required multiple of its own window (unresolved rows, n = 3,890) | q25 3.82x, **median 10.98x**, q75 57.22x, q90 624.81x |
| extra tape required, years (unresolved rows) | q25 43.8y, **median 147.1y**, q75 919.2y, q90 9,984.9y |
| reachable with tape available before 2050 (<= 24 more years) | **24.57% of all rows; 15.24% of unresolved rows** |

By window: FULL 12.22% resolved (median extra 162.0y), OOS **2.41%** resolved (median extra
108.4y). By panel: U56 13.10%, B136 11.54%, SMALL 8.16%.

**The answer to the question as asked: the median unresolved contrast the record produced on
2026-09-19 needs about ELEVEN TIMES its own tape, i.e. ~147 more years. Three quarters of the
unresolved mass is not reachable before 2050.**

## ARM B — the pooled ruler (the constructive half)
Device family = idea 1562's two-state gross (frozen incumbent frame, N=20, H=126, MAXVOL 0.60,
weekly; gross 0.75 when SPY is above its own MA, `g_low` when below), each cell against the
**constant gross whose FULL-sample CAGR it matches** (G4: worst match 0.01 bp). 12 cells
(4 MA x 3 `g_low`) x 2 large-cap panels = **the 24 large-cap cells**. One circular-block index set
per replicate is applied to all 24 cells *and* their 24 twins simultaneously.

| L | per-cell \|t\| > 2 | pooled EQ \|t\| | pooled PREC \|t\| | paired SE / independence SE | extra tape needed (EQ / PREC) |
|---|---|---|---|---|---|
| 21 | 0 of 24 (max 1.2817) | 0.5937 | 0.9103 | 3.78x / 3.69x | 182.7y / 67.6y |
| 63 | 0 of 24 (max 1.5224) | 0.7137 | 1.0794 | 3.66x / 3.60x | 121.0y / 43.0y |
| 126 | 0 of 24 (max 1.7379) | 0.7944 | 1.2138 | 3.56x / 3.52x | 94.2y / 30.3y |

**Pooling resolves 0 of 6 (L, scheme) combinations.** Pooled margin +0.0191 (EQ) / +0.0125-0.0128
(PREC) of Sharpe.

**THE METHOD FINDING, and it is the reusable one.** Had the 24 cells been pooled as if they were
independent — the arithmetic anyone reaching for a pooled ruler would write down — the pooled SE
would have been **3.5x to 3.8x too small**, and 5 of the 6 combinations would have read
\|t\| = 2.24 / 2.61 / 2.83 / 3.36 / 3.89 / 4.28, i.e. **"RESOLVED"**. They are not. The cells share
one tape and one holdings frame; the paired pooled bootstrap carries that and the independence
arithmetic manufactures it. **Any future pooled claim in this record must publish the ratio of its
paired pooled SE to its independence-assuming SE.**

## ARM C — the capital arm (rule 8, 2017-2026 read once)
Cell chosen by argmax IS Sharpe on warm-up..2016-12-31 only.

| panel | pick | FULL | OOS | 4a | 4b | vs own CAGR-matched twin, OOS |
|---|---|---|---|---|---|---|
| U56 | MA 100, g_low 0.5625 | 14.65% / 1.1817 / -16.54% (H1/H2 1.2289/1.1508) | **16.15% / 1.2247 / -16.54%** | False | **TRUE full and OOS** | +0.0393, SE 0.0418, \|t\| 0.94 — UNRESOLVED |
| B136 | MA 200, g_low 0.3750 | 14.23% / 1.0799 / -16.69% (1.3272/0.8827) | **14.29% / 1.0254 / -16.69%** | False | **TRUE full and OOS** | +0.0082, SE 0.0697, \|t\| 0.12 — UNRESOLVED |
| SMALL | MA 200, g_low 0.3750 | 6.87% / 0.5104 / -31.21% (0.7238/0.3362) | 5.33% / 0.4057 / -31.21% | False | False (all four legs fail) | **-0.0336** — loses to the twin, UNRESOLVED |

Comparands: SPY 15.12% / 0.8844 / -33.72% (OOS 15.26% / 0.8738 / -33.72%); live RULES v2 @10bps
U56 8.62% / 1.2011 / -12.05% (OOS 9.46% / 1.2769), B136 1.0973 (OOS 1.1019), SMALL 0.7185
(OOS 0.6473). Frozen 2026-09-04 anchor U56 15.80% / 1.1537 / -19.13%, OOS 1.1857 (G1 replayed to
3.7e-05); idea 1562's headline cell replayed to 3.3e-04 (G2).

**Why this is not a rules proposal.** Both large-cap picks clear 4b on FULL *and* OOS, and both beat
their own de-gross twin — by a margin the tape cannot separate from zero (\|t\| 0.94 and 0.12). The
twin is a *simpler* book: one constant number (g* = 0.6958 on U56, 0.6649 on B136) against a device
with an MA length, a threshold and a second gross. On the evidence available the record cannot say
the device is better, so the simpler book wins by default and no RULES change is proposed.

## Gates, cost ladder, survivorship
13 gates, **0 FAIL**: G0 min 15.6y; G1 / G2 cross-script replays; G3 exactly two tuned parameters
(block length, pooling scheme — the MA, `g_low` and cost ladders are the family's inherited
coordinates, published in full, never selected on); G4 twin CAGR match 0.01 bp; G5 no chooser reads
a row on or after 2017-01-01; G6 max realised gross 0.7769 <= 1.0; G7 cost ladder an exact identity
on one turnover path (dev 0.00e+00); G8 all 144 cells published (3 panels x 4 MA x 3 g_low x 4 cost
rungs 0/10/25/50 bps); G9 census matcher admits no constant/boolean column. Deterministic, offline,
44.9s.

**SURVIVORSHIP (rule 9):** U56 and B136 are current-constituent lists and SMALL a current sub-$2B
screen carried back to 2010 (483-name screen, names with `max_1d_move >= 1.0` in
`data/small_meta.csv` dropped first), so every ABSOLUTE level is an UPPER BOUND. ARM A is a
statement about the record's own published \|t\| values and is bias-free. ARM B is a contrast
between two books over the SAME names on the SAME days. The 4a/4b pass counts in ARM C are NOT
immune and are upper bounds.
