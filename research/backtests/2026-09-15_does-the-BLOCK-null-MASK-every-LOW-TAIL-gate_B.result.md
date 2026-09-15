# Idea 901 — does the BLOCK null MASK every LOW-TAIL gate in the record? (lane B, 2026-09-15)

**ANSWERED = NO. KILL for the queue's premise; the MECHANISM survives on a different axis.**

Script: `2026-09-15_does-the-BLOCK-null-MASK-every-LOW-TAIL-gate_B.py` · 10 bps, t+1, weekly
book, committed caches only, no network · 4,320 arms (10 families × 3 panels × 144 grid points),
21,600 placebo cells × 10 seeds = **216,000 placebo evaluations** · 282 s.

## The answer in one line

BLOCK does **not** mask every low-tail gate — it masks **4 of 5** — and the one it does not mask
(BREADTH-LO) is not an exception to the mechanism but a **demonstration of it**: the bias is
keyed to **where a gate's firing days sit on the volatility distribution**, not to which tail of
its own state the gate reads. `rho(fire_volpct, uplift) = −0.684` over 30 family × panel cells,
**−0.500 over all 4,320 arms**; arms firing **below** vol percentile 0.500 have median uplift
**+0.0362** (share > 0 **0.895**), arms firing **at/above** it **−0.0017** (share > 0 0.473).
0.500 is exactly where a BLOCK placebo lands by construction.

## Gates (section [0], all printed before any new number was read)

| gate | result |
|---|---|
| G1 never-firing multiplier ≡ ungated book | 0.000e+00 (bar 1e-12) **PASS** |
| G2 every placebo kind's mean effective multiplier ≡ the real arm's | 0.000e+00 **PASS** (the matched-gross twin cancels exactly) |
| G3 committed medians rebuilt from the committed CSVs, not prose | **6/6**, median \|d\| 0.0032 — 815 CORR-LO/BLOCK +0.0341→+0.0298, CORR-LO/YEARBLOCK +0.0568→+0.0541, CORR-HI/BLOCK +0.0554→+0.0517, CORR-HI/YEARBLOCK +0.0249→+0.0210; **870 CORR-LO/BLOCK +0.0298→+0.0298 and CORR-LO/VOLBLOCK +0.0792→+0.0790** |
| G4 determinism, every placebo re-seeded from its md5 | 0.000e+00 **PASS** |
| G5 fast Sharpe ≡ `engine.metrics()['Sharpe']` | 0.000e+00 **PASS** |
| G6 **VOLBLOCK at k=1 ≡ BLOCK at the same seed** | 0.000e+00 **PASS** (the stratum count is a true one-parameter family containing BLOCK) |
| G7 VOL20 ≡ idea 870's NAMEVOL | 0.000e+00 **PASS** (so NAMEVOL is not carried twice) |

## [1] Q1/Q3 — the uplift, median excess @10 bps, n=432 cells per family per kind

| family | BLOCK | YEARBLK | VB2 | VB3 | VB5 | upl2 | upl3 | upl5 | share>0 (k=3) |
|---|---|---|---|---|---|---|---|---|---|
| BREADTH-LO | +0.0683 | +0.0181 | +0.0566 | +0.0676 | +0.0529 | −0.0117 | **−0.0007** | −0.0154 | 0.424 |
| CORR-LO | +0.0298 | +0.0541 | +0.0700 | +0.0790 | +0.1015 | +0.0402 | **+0.0492** | +0.0717 | 0.882 |
| DISP-LO | −0.0361 | −0.0185 | −0.0130 | −0.0070 | +0.0149 | +0.0232 | **+0.0292** | +0.0510 | 0.898 |
| PORTVOL-LO | +0.0128 | +0.0402 | +0.0472 | +0.0612 | +0.0846 | +0.0344 | **+0.0484** | +0.0718 | 0.903 |
| VOL20-LO | −0.0192 | +0.0055 | +0.0132 | +0.0221 | +0.0434 | +0.0324 | **+0.0413** | +0.0626 | 0.917 |
| BREADTH-HI | +0.0112 | +0.0490 | +0.0272 | +0.0383 | +0.0523 | +0.0160 | **+0.0272** | +0.0412 | 0.877 |
| CORR-HI | +0.0517 | +0.0210 | +0.0400 | +0.0474 | +0.0375 | −0.0117 | **−0.0043** | −0.0142 | 0.433 |
| DISP-HI | +0.0276 | +0.0021 | +0.0234 | +0.0286 | +0.0239 | −0.0042 | **+0.0010** | −0.0036 | 0.593 |
| PORTVOL-HI | +0.0328 | −0.0009 | +0.0213 | +0.0301 | +0.0086 | −0.0114 | **−0.0027** | −0.0242 | 0.451 |
| VOL20-HI | +0.0189 | −0.0150 | +0.0081 | +0.0151 | −0.0030 | −0.0108 | **−0.0038** | −0.0219 | 0.463 |

**H_MASK FAIL, 4 of 5.** **H_STRAT PASS** — the sign of the uplift is identical at k=2/3/5 on
**0.967** of the 30 family × panel cells (only DISP-HI/B136 moves, on a median of +0.0010), so
idea 870's tercile cut is not carrying the result.

## [2] Q2 — the bias is not signed by the LO/HI label

| side | arms | med upl k=2 | k=3 | k=5 | share>0 (k=3) |
|---|---|---|---|---|---|
| LO | 2,160 | +0.0217 | **+0.0305** | +0.0479 | 0.805 |
| HI | 2,160 | −0.0030 | **+0.0044** | −0.0020 | 0.563 |

**H_SIGN FAIL** — HI's median uplift at k=3 is +0.0044, not negative. The label is the wrong
axis, which section [2b] then measures directly.

## [2b] What the uplift IS keyed to (POST-HOC, not a pre-registered bar)

Sorted by `fire_volpct`, the mean percentile-rank of realised portfolio vol on a gate's firing
days — a BLOCK placebo sits at 0.500 by construction, so it should score **too high** (excess
understated, uplift > 0) for a gate firing below 0.500 and **too low** (excess overstated,
uplift < 0) for one firing above it:

```
PORTVOL-LO  0.15–0.19   +0.0092 / +0.0683 / +0.0742      CORR-LO   0.19–0.21   +0.0767 / +0.0633 / +0.0063
VOL20-LO    0.22–0.26   +0.0079 / +0.0561 / +0.0556      DISP-LO   0.30–0.35   +0.0125 / +0.0408 / +0.0342
BREADTH-HI  0.41–0.43   +0.0383 / +0.0136 / +0.0304   ── 0.500 ──
DISP-HI     0.66–0.73   +0.0027 / −0.0081 / +0.0224      BREADTH-LO 0.73–0.80  +0.0170 / −0.0091 / −0.0139
VOL20-HI    0.78–0.84   +0.0239 / −0.0063 / −0.0192      CORR-HI   0.84–0.87   +0.0251 / −0.0176 / −0.0055
PORTVOL-HI  0.83–0.87   +0.0231 / −0.0208 / −0.0086
```

**The two families that sink H_MASK and H_SIGN are the two that cross the 0.500 line against
their own label.** BREADTH-LO is a LO gate that fires at vol percentile **0.73–0.80** (low
breadth *is* a falling market), and it is the only LO family BLOCK does not mask. BREADTH-HI is
a HI gate that fires at **0.41–0.43**, below the median, and it is the only HI family with a
clearly positive uplift. Both take the sign `fire_volpct` predicts, not the sign the tail label
predicts. That is the mechanism passing the test its own framing failed.

Consistency with the rest of the record, unprompted: idea 815 found EPISODEFIX **erases**
BREADTH-LO's excess (+0.0725 → +0.0041). A gate whose firing days are the crash days is exactly
the gate an episode-preserving null kills and a vol-preserving null leaves alone. The two nulls
agree on BREADTH-LO and disagree on CORR-LO for the same reason.

## [3] Q4 — the census of the record, re-priced

Harvested **79,920** committed LO-tail placebo-differenced numbers from **11 files** that name
their null; **28 files** carried the arm key but named no null and were skipped (a bare
`dSharpe`/`excess` column also holds matched-gross twin differences, which are not placebo
numbers). Files storing per-seed draws were collapsed to the seed **mean** first, because the
draw is an input and the mean is the published number. This run's own output is excluded from
its own census.

| claim set | k | rows | matched | understated | med uplift | restate>20% | sign flips | U56+B136 und. |
|---|---|---|---|---|---|---|---|---|
| NARROW | 2 | 13,392 | 12,960 | 0.745 | +0.0261 | 0.857 | 0.321 | 0.787 |
| NARROW | **3** | 13,392 | **12,960** | **0.806** | **+0.0357** | **0.864** | 0.369 | 0.839 |
| NARROW | 5 | 13,392 | 12,960 | 0.853 | +0.0523 | 0.925 | 0.491 | 0.836 |
| SHIFT | 2 | 27,936 | 27,072 | 0.673 | +0.0170 | 0.840 | 0.279 | 0.723 |
| SHIFT | 3 | 27,936 | 27,072 | 0.751 | +0.0261 | 0.849 | 0.310 | 0.799 |
| SHIFT | 5 | 27,936 | 27,072 | 0.835 | +0.0422 | 0.898 | 0.405 | 0.844 |
| ALL | 2 | 79,920 | 78,624 | 0.558 | +0.0078 | 0.871 | 0.263 | 0.599 |
| ALL | 3 | 79,920 | 78,624 | 0.615 | +0.0161 | 0.875 | 0.282 | 0.653 |
| ALL | 5 | 79,920 | 78,624 | 0.673 | +0.0302 | 0.915 | 0.344 | 0.675 |

**H_COUNT FAIL** — 0.806 understated at the NARROW × k=3 point, short of the 0.90 bar, and the
shortfall is BREADTH-LO's 3,024 rows, exactly as [2b] predicts.

**Two floors this must be read against, both measured here:**
- reproduction control, median \|my BLOCK − published BLOCK\| on the same keys: **0.0105**;
- **the record's own committed BLOCK numbers disagree with each other by a median of 0.0581
  on the same arm key** across 1,728 keys carried by 2+ files (max 0.6220), against idea 871's
  per-arm seed noise floor of 0.0145.

So the k=3 median uplift of +0.0357 is **0.61× the record's own key-level disagreement**. The
per-row understatement *shares* are not resolvable below that floor and should not be quoted as
precise counts. The **per-family medians** are the part that survives it:

| family | matched | pub med | VOLBLOCK3 | uplift | understated | restate>20% |
|---|---|---|---|---|---|---|
| BREADTH-LO | 3,024 | +0.0514 | +0.0742 | **+0.0077** | 0.573 | 0.707 |
| CORR-LO | 3,456 | +0.0180 | +0.0866 | **+0.0632** | 0.919 | 0.889 |
| DISP-LO | 3,024 | −0.0269 | −0.0075 | **+0.0230** | 0.789 | 0.918 |
| PORTVOL-LO | 432 | +0.0128 | +0.0612 | **+0.0475** | 0.903 | 0.889 |
| VOL20-LO | 3,024 | −0.0183 | +0.0230 | **+0.0405** | 0.912 | 0.936 |

## [4] Q5 — rule 8 and capital

Comparands @10 bps, weekly, t+1 — U56 SPY 15.13% / 0.885 / −33.72% (OOS 15.27% / 0.874 /
−33.72%), RULES v2 (live) 8.64% / 1.208 / −11.90% (OOS 9.49% / 1.286 / −11.90%); B136 SPY
15.16% / 0.886 / −33.72%, RULES v2 7.98% / 1.101 / −12.18%; SMALL SPY 14.06% / 0.858 / −33.72%,
RULES v2 4.30% / 0.663 / −13.89%.

Full-sample KEEP census over **all 4,320 arms, nothing selected**: **4a 1, 4b 475**. By side —
**LO: 4a 0, 4b 116, OOS 4a 10, OOS 4b 260**; HI: 4a 1, 4b 359, OOS 4a 29, OOS 4b 560. Every one
of the LO side's 116 full-sample 4b passes is **BREADTH-LO**; CORR-LO, DISP-LO, PORTVOL-LO and
VOL20-LO are **0 of 432 each**, reproducing idea 870's LO-side blind spot exactly.

**Rule 8** (IS-only selector: highest 2009–2016 Sharpe per panel × family, OOS 2017+ read once),
30 picks — OOS 4a **0**, OOS 4b **6**, LO-side OOS 4b **2 of 15**. Both LO passes are BREADTH-LO:
U56 (q 0.17, w 504, depth 1.00, D, g 1.00) **OOS 13.46% / 1.233 / −17.82%**, H1/H2 1.412/1.044;
B136 (q 0.17, w 504, depth 0.50, W, g 1.00) **OOS 12.87% / 1.109 / −17.20%**, H1/H2 1.284/0.914.
SMALL fails on every family (best LO pick BREADTH-LO OOS 6.67% / 0.492 / −31.92%).

**H_CAP PASS — and it is NOT a capital result.** Those two passes are *not* produced by the
re-pricing: BREADTH-LO's 4b count is already committed in the record (114 of 432 in idea 606's
2026-09-12 lane B table, rebuilt here as 116), and idea 815 already showed its excess is an
EPISODEFIX artefact. Re-pricing moved BREADTH-LO's excess by **+0.0077**, i.e. by less than the
seed noise floor. **No new book, no KEEP candidate on either path.**

Cost ladder, all arms, every rung — 0 bps median Sharpe 1.001 / CAGR 10.01% / MaxDD −20.84%;
10 bps 0.975 / 9.77% / −20.84%; 25 bps 0.930 / 9.39% / −20.84%. The uplift **grows with cost**
on both sides (LO +0.0189 → +0.0317 → +0.0550 at 0/10/25 bps; HI −0.0077 → +0.0044 → +0.0231),
because a vol-stratified placebo also has to pay for switching in the regime it switches in.

Walk-forward of the re-priced excess, `rho(IS, OOS)` per family: CORR-LO is the only family
positive under **all five** nulls (+0.413 BLOCK → +0.460 VOLBLOCK3 → +0.612 VOLBLOCK5),
reproducing idea 815's +0.392; DISP-LO and VOL20-LO go **negative** under VOLBLOCK (−0.506,
−0.183) although they are positive under BLOCK, so the re-pricing does not rescue their
persistence either.

## Pre-registered bars

| bar | result |
|---|---|
| H_MASK — uplift > 0 for ALL 5 LO families | **FAIL** (4/5; BREADTH-LO −0.0007) |
| H_SIGN — LO uplift > 0 AND HI uplift < 0 | **FAIL** (LO +0.0305, HI +0.0044) |
| H_STRAT — same sign at k=2/3/5 on ≥90% of cells | **PASS** (0.967) |
| H_COUNT — ≥90% of NARROW committed LO rows understated | **FAIL** (0.806) |
| H_CAP — ≥1 LO rule-8 pick clears OOS 4b | **PASS** (2, both BREADTH-LO, both pre-existing) |

## Verdict

**KILL for the queue's premise, with the mechanism confirmed and relocated.** "LOW-tail gate" is
not the class BLOCK mis-prices; **"gate that fires away from the middle of the vol
distribution"** is, and it mis-prices in the direction of the side the gate sits on. Four of the
record's five low-tail families are understated by BLOCK (CORR-LO most, +0.0632 on 3,456
committed rows); the fifth, BREADTH-LO, is not, because it fires in the high-vol tail. **No book
changes and nothing is proposed for RULES.md** — the re-pricing raises excesses on exactly the
families that hold 0 of 432 on 4b, so a bigger placebo-differenced number still buys no capital.

**Restrictions, stated:** the per-row understatement shares are resolved only to the record's own
0.0581 key-level disagreement and should be read as per-family medians, not counts. The census
normalises the record's SMALL439 / SMALL663 / SMALL panels to one name — the U56+B136-only
column is printed beside every pooled figure for that reason. All three panels are
current-constituent lists (SMALL additionally drops every ticker with `max_1d_move >= 1.0`), so
CAGR and drawdown **levels** are optimistic; the placebo differencing and the BLOCK-vs-VOLBLOCK
contrast are the durable part. Vol strata are full-sample quantile cuts of a state the null
never trades — a measurement device, not a tradeable path.
