# Idea 1119 (cloud lane, 2026-09-16) — does the LADDER axis answer hold on the SMALL panel?

**ANSWERED = YES, the ladder axis holds — and the idea's own premise does not.** The LADDER
answer survives on the 664-name sub-$2B panel (LAD beats STAT at 8 of 8 independent seed
redraws, on the binary reading *and* on both continuous ones), so 1116's conclusion transfers to
the panel where 1073 measured reliability 0.0915. But the *gradient* this idea is built on — "the
margin is 17.0x on U56 but 11.7x on B136, i.e. it weakens as the panel widens" — **is one draw
of each panel**: on 8 redraws U56's margin runs 3.18x–17.00x (median 7.00x) against B136's
11.00x–11.67x (median 11.00x), so the two large panels order the *other way* at the median and
1116's committed 17.0x is U56's redraw **maximum**. KILL of the breadth gradient, KILL of the
"small caps will degenerate the table" expectation, CONFIRM of the ladder answer. No RULES
change, no book promoted, no PROTOCOL edit (rule 6); RULES.md, PROTOCOL.md, scan.py, bot.py and
baseline.py untouched. SELECTION: this lane takes the LAST eligible open idea (idea 2 of 2).

## The two dials and no more (PROTOCOL rule 4)

`PANEL` {U56, B136, SMALL} × `CONFIDENCE q` {0.80, 0.90, 0.95} — **all 9 combinations
published**, plus the two side definitions beside them (45 decomposition rows in all). LADDER and
STATISTIC are **not** dials: they are the two candidate answers, and all 3 × 4 × 4 = **48 CORE
cells** are reported at every q. The un-resolvability DEFINITION is **frozen** at `INF_FLOOR`
(1116's headline) and the decision rule never reads the other two. BLOCK LENGTH is frozen the
same way (L=63 headline, L ∈ {21, 126} beside, never selected on). Everything else frozen at
1082/1094/1098/1102/1108/1110/1116's construction: CAND20 legs, cap INF, max_vol 0.60, gross
0.75 (except on the GROSS ladder), W (except on CADENCE), min hold 126 (except on H), N=20
(except on N), 10 bps, LAG 1, warm-up 260, IS end 2016-12-31, 1000 draws, `zlib.crc32` seeds.

## The SMALL panel's stamp (idea 1074's recommendation, applied)

`data/small_meta.csv` lists 715 tickers; **52 dropped for `max_1d_move` >= 1.0**; the pool served
is **664 names** (663 + SPY as benchmark only), tape **2010-01-04 .. 2026-09-11, 4,198 rows**,
mean 524.3 names priced per day. This idea's own text says "485-name"; the loader serves 664
today — idea 706's 439→663 rebuild and idea 1072's finding that committed SMALL headlines move on
it. **The stamp, not the label, is what these numbers refer to.** SPY is the 4b benchmark on this
panel and not a constituent, so it is removed from the selectable set; gate `G_SPY` prices that
choice rather than asserting it — **had SPY been left in it would have been held at 0 of 871
rebalance dates**, so the exclusion changes nothing measurable.

## A gate failed, and the failure is the second finding

The first pass FAILED its own reproduction gates against 1116 (U56 ETA2 0.7333/0.0667 against
1116's committed 0.8095/0.0476). Before reading that as a code discrepancy it had to be separated
from a seed redraw, because this lane's bootstrap base is 11191119 and 1116's is 11161116.
**Re-running the identical code at 11161116 reproduces 1116's committed ETA2 pair, concordance
pair and all four per-ladder INF_FLOOR counts on both panels, bit for bit** (G7/G8/G9, max
deviation 4.4e-07). So the code is 1116's; everything the two bases disagree about is the DRAW.
The **seed redraw arm** (post-hoc and labelled as such — 1116 itself ran 6 redraws for the axis
question) then measures how much that is, at 8 bases across all three panels.

## The answer

The 4 × 4 tables at the headline cell (INF_FLOOR, q=0.90; 1 = un-resolvable):

```
U56        S_FULL  S_OOS  CAGR   DD   row      B136     S_FULL S_OOS CAGR  DD  row      SMALL   S_FULL S_OOS CAGR  DD  row
N            0      0      0     0    0/4      N          1     0    1    0   2/4      N         0     0    0    0   0/4
H            1      1      1     1    4/4      H          1     1    1    1   4/4      H         0     1    0    1   2/4
GROSS        1      1      0     0    2/4      GROSS      0     0    0    0   0/4      GROSS     1     1    0    0   2/4
CADENCE      1      1      1     1    4/4      CADENCE    1     1    1    1   4/4      CADENCE   1     0    1    1   3/4
col        3/4    3/4    2/4   2/4             col      3/4   2/4  3/4  2/4             col     2/4   2/4  1/4  2/4
```

Rows vary, columns barely do — on **all three** panels. At the headline cell SMALL reads
ETA2_LAD **0.3016** against ETA2_STAT **0.0476** (6.33x), and on the two readings that need no
threshold: REL_FLOOR eta2 LAD 0.3055 vs STAT 0.2029, LOG_M eta2 LAD 0.4767 vs STAT 0.1997,
concordance within-ladder 0.5417 vs within-statistic 0.3750. **LAD wins on SMALL at 8 of 8 seed
redraws on the binary reading, 8 of 8 on REL_FLOOR and 8 of 8 on concordance** — and SMALL is the
*most* stable panel of the three under redraw (7/16 un-resolvable and 0.3016/0.0476 at every one
of the 8 bases, margin 6.33x with zero spread).

**H_MARGIN_MONO REFUTED, and this is the keeper.** The redraw distribution of the margin:

| panel | n_unres/16 | ETA2_LAD | ETA2_STAT | margin | LAD wins |
|---|---|---|---|---|---|
| U56 | 8–10 (med 9.0) | 0.4286–0.8095 (med 0.6250) | 0.0476–0.1746 (med 0.0958) | 3.18x–17.00x (med **7.00x**) | 8/8 |
| B136 | 9–10 (med 10.0) | 0.5556–0.7333 (med 0.7333) | 0.0476–0.0667 (med 0.0667) | 11.00x–11.67x (med **11.00x**) | 8/8 |
| SMALL | 7–7 (med 7.0) | 0.3016 | 0.0476 | 6.33x (no spread) | 8/8 |

1116's committed 17.0x is U56's redraw maximum and its 11.7x is B136's; at the median the
ordering is **B136 > U56**, i.e. the reverse of the gradient this idea infers from them. ETA2 on a
4 × 4 *binary* table takes very few distinct values, so a single draw of it cannot support a
"weakens as the panel widens" reading in the first place. What is robust is only the *sign*: the
ladder axis wins, on every panel and every redraw.

**H_DEGENERATE REFUTED.** The expected failure mode did not happen: SMALL's binary table is not
constant (SST 3.9375, 7 of 16 un-resolvable), *fewer* than either large panel's 10 of 16, because
SMALL's ladder spreads are far larger (median 1.3944 against 0.5984 and 0.6058) and its gaps sit
further from the q boundary. The draw dominating one book's OOS Sharpe (1073's 0.0915) does not
make the ladder's rung-to-rung *contrasts* less decidable here.

**H_HCAD and H_NGROSS both REFUTED at the cell level.** 1116's sharpest per-cell result — H and
CADENCE un-resolvable at all 4 statistics, N and GROSS at almost none — is 5 of 8 and 2 of 8 on
SMALL, not 8 of 8 and ≤1 of 8. Per-ladder medians over the redraws: SMALL N 0/4, H 2/4, GROSS
2/4, CADENCE 3/4 — the *ordering* of the ladders survives (CADENCE worst, N best) but the
saturation does not. The marginals say why: on SMALL, GROSS carries mean REL_FLOOR 0.5503 and
mean log10 M 0.279 (resolvable, as on both large panels) while CADENCE carries 1.0000 and 1.720.

**The matched-tape arm** (all three panels truncated to SMALL's 2010 start, so the comparison is
not a tape-length comparison) leaves the answer intact: U56 0.8095/0.0476 on 4,200 rows, B136
0.7333/0.0667 on 4,198, SMALL 0.3016/0.0476 on 3,938; LAD wins all three.

## Gates: 15 of 15 PASS, printed before any result number

G1 fast runner == `engine.backtest` 1.39e-17; G2 committed U56 W/H126/N=20 triple 3.18e-07;
G3 SPY OOS triple 1.70e-04; G4 live RULES v2 MaxDD 4.95e-05; G5 SMALL pipeline determinism 0.0;
G6 + per-panel: every ladder live (Sharpe spread 0.896 overall, 0.183 / 0.121 / 0.511 per panel);
**G7/G8/G9 × 2 panels: the SEED-MATCHED bit-level reproduction of 1116's ETA2, concordance and
per-ladder counts** (max 4.4e-07, counts exact). HYPOTHESES **5 of 9** SUPPORTED (H_REPRO,
H_LADDER, H_SURVIVES, H_CONCORD, H_REDRAW; REFUTED: H_MARGIN_MONO, H_DEGENERATE, H_HCAD,
H_NGROSS).

## Rule 8 and both KEEP paths — nothing proposed, and SMALL is a clean KILL as capital

Rung chosen on IS 2009–2016 alone, per ladder, three choosers, OOS read once. **All 36 picks: 4b
full 4, 4b OOS 4, 4a 0**; the IS chooser picks the OOS-best rung 11 of 36 times. Per panel:
U56 4/12 and 4/12 with median OOS Sharpe 1.1633 (median regret +0.0083); B136 0/12 and 0/12 at
1.0011 (+0.0515); **SMALL 0/12 and 0/12 at median OOS Sharpe 0.4317 against SPY's 0.8767 and
RULES v2-on-panel's 0.5600 (median regret +0.0832)**. Whole grid, 81 rungs: 4b full 16, 4b OOS
17, **4a 0**. By panel: U56 10/27 and 11/27, B136 6/27 and 6/27, **SMALL 0 of 27 on both**, and
SMALL fails nearly every leg individually — L_H1 1/27, L_H2 0/27, L_OOS 0/27, L_DD 2/27,
L_CAGR 1/27. Binding leg across the 65 failures: L_DD (fails 53, sole failure 26), then L_CAGR
(35, sole 9). **Nothing on the SMALL panel comes close to either KEEP path at any of the 27
rungs, and nothing here is proposed as capital.**

## Survivorship (PROTOCOL rule 9)

U56 and B136 are current-constituent lists. The SMALL pool is worse: it is the *current*
constituents of a sub-$2B screen, so every name that fell below the screen, delisted or went to
zero is absent, and a small-cap pool loses names that way far more often than a large-cap one.
Every CAGR and drawdown LEVEL on SMALL is optimistic by an amount this run cannot measure and
every 4a/4b count on it is an UPPER bound — which makes the 0-of-27 above stronger, not weaker.
A rung-to-rung GAP and a rung-to-rung AGREEMENT both contrast two books over the same inflated
tape, so the bias very largely cancels out of the floor, the ETA2 and every quantity decomposed
here; it does NOT cancel out of the 4b legs, measured against SPY, a real index.

## The declared approximation, and its direction

`NO_TAPE_500` rests on 1110's projection A' = Φ(√M Φ⁻¹(A)): a fixed population gap and an SE
falling as 1/√T. Both assumptions run TOWARD resolution, so every `M_needed` here is a LOWER
bound and every `NO_TAPE_500` count a LOWER bound on un-resolvability. The exponent is
INHERITED from 1110 and is NOT re-measured here, still less on the SMALL tape, so the DD column's
`M_needed` is this run's least trustworthy quantity and is reported apart.

Script: `2026-09-16_does-the-LADDER-axis-answer-hold-on-the-SMALL-panel_cloud.py`
