# Idea 1116 (lane B, 2026-09-16) — is UN-RESOLVABILITY a LADDER property or a STATISTIC property?

**ANSWERED = LADDER.** Un-resolvability is a property of *which dial is being laddered*, not of
*which statistic is read off it*. KILL of the statistic reading, and KILL of the two most
tempting explanations of the ladder reading. No RULES change, no book promoted, no PROTOCOL
edit (rule 6); RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py untouched.
SELECTION: lane B takes the LAST eligible open idea.

## The two dials and no more (PROTOCOL rule 4)

UNRESOLVABILITY DEFINITION {INF_FLOOR, ZERO_CONTENT, NO_TAPE_500} × CONFIDENCE q {0.80, 0.90,
0.95} = **9 combinations, all published**. LADDER and STATISTIC are **not** dials — they are the
two candidate answers, and all 2 × 4 × 4 = 32 CORE cells are reported under every combination.
PANEL is not a dial. BLOCK LENGTH is not a dial (L=63 headline, L ∈ {21, 126} reported beside and
never selected on). Everything else frozen at 1082/1094/1098/1102/1108/1110's construction; seeds
are `zlib.crc32`, 1108's repair.

## The answer

The headline definition (INF_FLOOR at q=0.90) reproduces 1110's count exactly: **18 of 32 cells
carry an infinite floor**. Laid out as a 4 × 4 table per panel, the rows are near-constant and
the columns carry almost nothing:

```
U56        S_FULL  S_OOS   CAGR    DD    row        B136     S_FULL  S_OOS  CAGR   DD   row
N            0       0      0      0     0/4        N          1      0     1     0    2/4
H            1       1      1      1     4/4        H          1      1     1     1    4/4
GROSS        0       1      0      0     1/4        GROSS      0      0     0     0    0/4
CADENCE      1       1      1      1     4/4        CADENCE    1      1     0     1    3/4
col        2/4     3/4    2/4    2/4                col      3/4    2/4   2/4   2/4
```

**H and CADENCE are un-resolvable at every statistic on both panels; N and GROSS at almost none.
Every column reads 2 or 3 of 4.** A main-effects two-way decomposition puts **ETA2_LAD 0.8095
against ETA2_STAT 0.0476 on U56 (17.0×)** and **0.5556 against 0.0476 on B136 (11.7×)**. Both
threshold-free continuous readings agree and are stronger: REL_FLOOR 0.5752/0.1177 and
0.9738/0.0066; log10(M_needed) 0.8127/0.0379 and 0.6727/0.0684. The second, independent reading —
CONCORDANCE, whose two sides share the marginal base rate by construction — gives within-ladder
agreement **0.8750 / 0.7083** against within-statistic **0.3750 / 0.3750** (**H_CONCORD PASS**).
**LADDER wins both panels in 8 of the 9 dial combinations and STATISTIC in 0 of 9**; the lone
exception is NO_TAPE_500 at q=0.80 on U56, the sparsest table in the run (2 of 16 cells set).

## Both tempting explanations, killed on their own terms

**H_GROSS_CARRIES FAILS.** The ladder answer is not one ladder in disguise. GROSS is fully
resolvable on B136 but 1 of 4 un-resolvable on U56, and only 2 (U56) and 1 (B136) of the three
non-GROSS ladders are un-resolvable at all four statistics. Re-scored on 1110's **own** committed
flags it still fails, on the B136 leg — so the FAIL is not a seed artefact, though the U56 leg of
it is (U56 GROSS/S_OOS flips with the seed) and is named as such.

**H_DD_WORST FAILS and runs backwards.** DD is among the *more* resolvable statistics (mean
REL_FLOOR 0.7381 on U56, 0.7189 on B136). The least resolvable statistic is **S_OOS on U56
(0.9873)** and **CAGR on B136 (0.7777)** — not the same statistic on the two panels, which is the
statistic reading failing on its own terms rather than merely losing to the other axis.

## D1 and D2 — post-hoc and labelled

This run draws its **own** bootstrap (SEED_BOOT 11161116 against 1110's 11101110), so the
cross-run is an independent redraw, not a reproduction attempt. **G9: committed argmax gaps 32 of
32 exact; infinite-floor flags 30 of 32.** The two that flip are U56 N/CAGR and U56 GROSS/S_OOS,
and two more flip on NO_TAPE_500 at M = 359 and 255 against a 500 cap, so NO_TAPE_500 reads **10
of 32 here against 1110's committed 8**. That is **1108's seed finding reproduced independently**,
and it is a CORRECTION to the precision at which 1110's NO_TAPE_500 count should be quoted.

**Stated because it is easy to misread:** the U56 INF_FLOOR decomposition matches 1110's to the
digit while the underlying tables differ in 2 of 16 cells. The two flips are mirror-symmetric in
*both* margins, leaving SS_row, SS_col and SS_total each unchanged. That is an accident of this
pair of flips, not evidence that the decomposition is seed-insensitive. **D2 is the actual
evidence: three further independent seed draws, LADDER wins in 6 of 6 (seed, panel) redraws**,
ETA2_LAD 0.5556–0.8095 against ETA2_STAT 0.0476–0.0667. The cell-level flag is seed-fragile; the
axis answer is not.

## What the record should do with this

The honest reading is narrow and worth stating narrowly: **which axis the record should stop
laddering is H and CADENCE, not any statistic.** Those two ladders decide nothing at any of the
four statistics on either panel, so a published argmax on a min-hold or a cadence ladder is
contentless whichever number is read off it — while an argmax on an N or a GROSS ladder is
resolvable at almost every statistic. Re-reading such a claim under a different statistic cannot
rescue it, because the statistic is not where the un-resolvability lives. This is a **proposal for
the Sunday review, not an enacted change** (rule 6), and it is filed as such.

## Gates, rule 8, and both KEEP paths

**GATES 10 of 10, printed before any result number.** G1 fast runner == `engine.backtest`
1.39e-17; G2 CROSS-RUN 936/1071/1082/1094/1102/1108/1110's U56 W/H126/N=20 triple 3.18e-07; G3 SPY
OOS 1.70e-04; G4 1098/1102's U56 n=12 4.97e-05 and G4b its B136 n=15 2.13e-05; G5 live RULES v2
MaxDD 4.95e-05; G6 determinism 0.00e+00; G7 the ladders are live (Sharpe spread 0.1916); G8
CROSS-RUN 1102's committed tie-set verdicts 32 of 32; G9 CROSS-RUN 1110's committed gaps 32 of 32.

**Rule 8 and both KEEP paths — NOTHING PROPOSED.** No definition and no q can move a book: the
BOOK at all 54 rungs is byte-identical across both dials, only which cells get *called*
un-resolvable changes, so 4a and 4b are invariant to dial 1 and dial 2 by construction. Scored
anyway because rule 4 requires it. Rung chosen on IS 2009–2016 ALONE, per ladder, three choosers,
OOS read ONCE: **4 of 24 picks clear 4b full AND OOS; 0 of 24 clear 4a.** Whole grid, 54 cells:
**4b full 16, 4b OOS 17, 4a 0** — independently reproducing 1108's and 1110's counts. Every
passing pick is the standing anchor U56 / W / H=126 / N=20 / gross 0.75 (full 15.58% / 1.1397 /
-19.13%, halves 1.2037/1.0971, OOS 16.97% / 1.1643 / -19.13%), a cell the record already holds and
has already PARKED. Benchmarks: U56 SPY full 15.10% / 0.8829 / -33.72% (halves 0.9588/0.8207), OOS
15.21% / 0.8711 / -33.72%; U56 RULES v2 live 8.62% / 1.2007 / -12.05%, OOS 9.45% / 1.2762 /
-12.05%; B136 SPY full 15.16% / 0.8861 / -33.72%, OOS 15.33% / 0.8767 / -33.72%; B136 RULES v2
7.98% / 1.0993 / -12.24%, OOS 7.88% / 1.1059 / -12.24%.

## The declared approximation, and its direction

NO_TAPE_500 rests on 1110's **projection** A' = Φ(√M Φ⁻¹(A)) — a fixed population gap and an SE
falling as 1/√T. Both assumptions run **toward** resolution, so every M_needed here is a LOWER
bound and every NO_TAPE_500 count a LOWER bound on un-resolvability. The exponent is **inherited**
from 1110's sub-tape measurement (median β −0.4540 over the 24 non-DD cells, DD +0.2093) and is
not re-measured here, so DD's M_needed is the least trustworthy quantity in this run and is named
as such. The M_needed solver is exact rather than a grid sweep: with z = Φ⁻¹(A) and z_q = Φ⁻¹(q) a
pair is unresolved at M iff M < (z_q/z)², so the un-resolved set changes only at those critical
multiples — identical to the sweep by construction, and cross-checked against 1110's committed
column in G9.

## Survivorship (PROTOCOL rule 9)

U56 and B136 are CURRENT-CONSTITUENT panels, so every level is optimistic. A rung-to-rung gap and a
rung-to-rung agreement both contrast two books over the same inflated tape, and the bias very
largely cancels out of them, out of the floor and out of every quantity decomposed here; it does
NOT cancel out of the 4b legs, which are measured against SPY, a real index, so the 16 full-sample
4b passes are an UPPER bound.

Script `research/backtests/2026-09-16_is-UN-RESOLVABILITY-a-LADDER-property-or-a-STATISTIC-property_B.py`,
10 CSVs, console log, 5 LEADERBOARD rows.
