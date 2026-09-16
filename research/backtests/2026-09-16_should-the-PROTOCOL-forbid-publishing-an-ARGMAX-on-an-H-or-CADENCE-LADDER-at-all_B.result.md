# Idea 1117 (lane B, 2026-09-16) — should the PROTOCOL forbid publishing an ARGMAX on an H or CADENCE ladder at all?

**ANSWERED = NO, AND THE CLAUSE FAILS ON THE ONE TEST THAT MATTERS MOST: IT CAN BE ESCAPED BY
ADDING RUNGS.** The clause as the queue words it — bar an argmax on a ladder whose floor is
whole-ladder at *every* statistic — bars **12 of the record's 32 committed argmaxes at 1110/1116's
own rungs and 0 of 32 once the same two ladders carry 9 rungs instead of 4**. It also does not do
the job it was drafted for: on this grid an honest IS-only argmax buys **nothing** out of sample on
**either** side of the clause's line, so a ban keyed on *ladder identity* aims at the wrong target.
**KILL of the clause as written.** No RULES change, no book promoted, no PROTOCOL edit (rule 6);
RULES.md, PROTOCOL.md, engine.py, scan.py, bot.py and baseline.py untouched.

**SELECTION:** lane B takes the LAST open idea; 1117 ended '## Open' and is not EDGAR / Form 4 /
8-K / options / live-data. It has a PRICE LEG — 74 books over 4 ladders x 2 panels, two rung sets —
so it carries this run's mandatory rule-8 walk-forward and both KEEP paths.

## THE TWO DIALS AND NO MORE (PROTOCOL rule 4)
`CLAIM SET` {CS_HCAD, CS_ALL32, CS_DECIDED} x `BAR` {B_ALLSTAT, B_MAJ3, B_ANY} = **9 combinations,
all published**, at 3 seed bases. PANEL, LADDER and STATISTIC are not dials. **RUNG SET
{CORE, EXT} is not a dial either and nothing is selected on it**: 1118 established that
P(INF_FLOOR) *falls* as rungs are added, so the clause's own trigger is rung-count dependent and
both levels are reported at every point. Frozen at 1082/1094/1098/1102/1108/1110/1116/1118's
construction: CAND20 legs, cap INF, max_vol 0.60, gross 0.75, min hold 126, N=20, W, 10 bps,
LAG 1, warm-up 260, IS end 2016-12-31, block L=63, 1000 draws, crc32 seeds, q=0.90.

## GATES 11 of 11 PASS, printed before any result number
G1 fast runner == `engine.backtest` 1.39e-17; G2 committed U56 W/H126/N=20 triple 3.18e-07
(15.5787% / 1.1397 / -19.1276%); G3 SPY OOS 1.70e-04; G4 / G4b committed U56 n=12 and B136 n=15
triples 4.97e-05 / 2.13e-05; G5 live RULES v2 MaxDD -12.05% at 4.95e-05; G6 determinism 0.00e+00;
G7 `cadence_mask` == `engine.rebalance_mask` on D/W/M/Q, 0 differing bars (engine.py not modified);
**G8 reproduces all 54 rows x 5 columns of 1110's committed CORE grid at 0.00e+00**; **G9
reproduces all 32 of 1110's committed argmax PEAKS with 0 mismatches**; G10 every ladder x
statistic live (min spread 1.79e-03). **HYPOTHESES 2 of 6.**

## A CORRECTION TO THE IDEA'S OWN PREMISE, MADE BEFORE ANY OTHER NUMBER
The queue says 1116 found H and CADENCE infinite "at ALL FOUR statistics on BOTH panels (8 of 8
cells)". **1110's committed census reads 15 of 16, not 16 of 16** — B136 CADENCE CAGR carries a
*finite* floor (1.8463) with a 3-rung tie set. This run's own trigger table reproduces the gap:
at the headline base B136 CADENCE is infinite at **3 of 4** statistics, and over 3 seed bases its
count runs 3 / 4 / 4. **The clause as written therefore does not even bar B136 CADENCE**, one of
the four blocks it was drafted to bar. H_PREMISE **REFUTED**; H_BARS_HCAD **REFUTED** (CORE
inf_counts U56 N 0 / H 4 / GROSS 1 / CADENCE 4, B136 N 2 / H 4 / GROSS 0 / CADENCE 3).

## THE FATAL DEFECT: THE TRIGGER VANISHES WHEN RUNGS ARE ADDED (H_STABLE REFUTED)
Per-block INFINITE-floor count, of 4 statistics, headline base:

| block | CORE (k=4) | EXT (k=9) |
|---|---|---|
| U56 H | **4** | 3 |
| U56 CADENCE | **4** | 1 |
| B136 H | **4** | 2 |
| B136 CADENCE | 3 | 1 |
| U56 N / GROSS | 0 / 1 | 0 / 1 |
| B136 N / GROSS | 2 / 0 | 2 / 0 |

Barred set at B_ALLSTAT: **{U56 H, U56 CADENCE, B136 H} on CORE rungs, and the EMPTY SET on EXT
rungs.** The census moves with it — CS_ALL32 **12 -> 0**, CS_HCAD **12 -> 0**, and at B_MAJ3 **16 -> 4**
(median over 3 bases 16 -> 0); only B_ANY is rung-stable (24 and 24). **An author who wants to
publish an H-ladder argmax need only run 9 rungs instead of 4 and the ban never fires.** That is
not a loophole this run had to hunt for: it is 1118's mechanism — an infinite floor means the
ladder's *largest* gap is un-resolved, and extra rungs add larger, more separable gaps — applied
to the clause's own trigger. **Any clause keyed on a whole-ladder floor must fix the rung set, or
it is advisory only.**

## AND THE CLAUSE AIMS AT THE WRONG TARGET (H_DISCRIMINATES REFUTED, H_WORTHLESS SUPPORTED)
Rung chosen on IS 2009-2016 alone, three choosers, OOS 2017-2026 read once, scored against that
ladder's **frozen default rung** (N=20, H=126, gross=0.75, W) on the chooser's own matched
statistic. **48 IS picks. BARRED blocks: median advantage +0.0000, 3 of 9 wins. UNBARRED blocks:
median advantage +0.0000, 10 of 39 wins.** The clause does not separate the two.

The sharper reading, reported because the zeroes are not all the same zero: **12 of 48 picks
re-pick the default rung** (advantage 0 by construction). On the **36 picks that MOVE off the
default, the median matched advantage is -0.0195 and the median OOS-Sharpe advantage -0.0502,
with 13 of 36 wins** — and it is negative on **barred and unbarred blocks alike** (B_ALLSTAT CORE:
barred -0.0111 at 3/7, unbarred -0.0361 at 3/9). **Choosing a rung by argmax is not merely
uninformative on this grid, it is negatively informative, on every ladder — N and GROSS
included.** A ban keyed on ladder identity cannot express that. H_ISOOS_RANK is SUPPORTED but
thin and should not be leaned on: mean |Spearman(IS order, OOS order)| 0.5556 barred vs 0.5868
unbarred, and the unbarred mean is carried entirely by GROSS's |rho| = 1.0000 (a near-scaling
family, 1108's result).

**CROSS-READ with idea 1107 (cloud, same day), which reaches the same KILL by a different route:**
1107 finds *no* committed H-axis or cap-axis argmax clears its own floor even once (max
gap-to-floor ratio exactly 1.000 over 26 ladders, 18 of 26 whole-ladder). The two runs agree the
claims are unsupported; this run adds that **the clause the queue proposed is not the instrument
that stops them.**

## WHAT SHOULD BE DRAFTED INSTEAD (stated, not enacted — rule 6)
A bar keyed on the *claim*, not the *dial*: every published argmax quotes (a) its gap, (b) its
ladder's resolution floor **and rung count**, and (c) its tie set at the declared q — the record
already computes all three. On this grid that clause bars **12 of 32 at CORE rungs and 4 of 32 at
EXT rungs at B_MAJ3** while remaining well-defined at any rung count, because nothing in it
depends on a whole-ladder flag.

## RULE 8 AND BOTH KEEP PATHS — nothing proposed
**48 IS picks: 4b full 6, 4b OOS 6, 4a 0, median OOS Sharpe 1.0244, median regret +0.0228.**
**All six 4b passes are the frozen DEFAULT rung** (U56 GROSS 0.75 and U56 CADENCE W are the same
incumbent book): full 15.58% / 1.1397 / -19.13% (H1 1.2037 / H2 1.0971), OOS 16.97% / 1.1643 /
-19.13%. Whole grid, 74 rungs: **4b full 17, 4b OOS 18, 4a 0**; of the 20 rungs outside 1110's
CORE only **1** clears 4b (U56 CADENCE 2Q, OOS 15.47% / 1.0660 / -17.90% — below the incumbent's
own OOS Sharpe, so it buys nothing). Benchmarks: **U56 SPY full 15.10% / 0.8829 / -33.72%, OOS
15.21% / 0.8711 / -33.72%; B136 SPY full 15.16% / 0.8861 / -33.72%, OOS 15.33% / 0.8767 /
-33.72%; live RULES v2 U56 8.62% / 1.2007 / -12.05% full and 9.45% / 1.2762 / -12.05% OOS, B136
7.98% / 1.0993 / -12.24% full and 7.88% / 1.1059 / -12.24% OOS.** **KILL of the clause; PARK
nothing; no capital proposed.**

**SURVIVORSHIP (rule 9):** U56 and B136 are current-constituent lists, so every 4b figure here is
an upper bound. The census and trigger quantities are within-panel contrasts over one tape and
the bias very largely cancels out of them; the 4b legs are measured against SPY and do not cancel.

## Files
`_B.py` (script) · `.grid.csv` (74 books) · `.trigger.csv` (48 block x rung-set x base) ·
`.census.csv` (54 dial points) · `.walkforward.csv` (48 IS picks) · `.rankinfo.csv` ·
`.committed.csv` (G9, 32 committed peaks) · `.gates.csv` · `.hypotheses.csv` · `.console.txt` ·
`.log.txt`
