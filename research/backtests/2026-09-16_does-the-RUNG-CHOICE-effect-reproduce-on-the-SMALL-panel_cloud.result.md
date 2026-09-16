# Idea 1141 (cloud lane, 2026-09-16) — does the RUNG-CHOICE effect reproduce on the SMALL panel?

**ANSWERED = NOT AS 1131 STATED IT, AND THE QUEUE'S OWN PREMISE IS REFUTED IN THE OPPOSITE
DIRECTION.** The queue predicted that a noisier panel would fire **far MORE often** at every
rung set (1073: reliability 0.0915 on small caps against 0.5126 on large). It fires **far
LESS**: the matched-k share runs **SMALL H 0.2778 against U56 0.5079 and B136 0.7143, and
SMALL CADENCE 0.0794 against 0.0952 and 0.1825** — lower than both large panels on both
movable ladders. 1131's literal claim does not reproduce either, but for a reason its own
framing could not see: **CORE does not fire at all four statistics on SMALL in the first
place** (5 of 8 blocks, against 8 of 8 on both large panels), so there is no "fires where
most subsets do not" left to be an outlier about. **The direction-free re-cut (D1) is the
real answer and it goes 1131's way harder: CORE's firing state is the MINORITY state on 6 of
8 SMALL blocks, against 2 of 8 on U56 and 3 of 8 on B136.** The rung-CHOICE dependence is
**stronger** on the small panel; only its sign flips. Two **CORRECTIONS** to the committed
record fall out (below). No RULES change, no book promoted, no PROTOCOL edit (rule 6);
RULES.md, PROTOCOL.md, engine.py, scan.py, bot.py and baseline.py untouched.

**SELECTION:** this lane takes the LAST eligible open idea (idea 2 of 2); 1141 ended
'## Open' and names no EDGAR / Form 4 / 8-K / options / spin-off / live-data source. It has a
price leg — 111 books over 4 ladders x 3 panels x 2 rung sets, 72 rule-8 picks — so it
carries this run's mandatory rule-8 walk-forward and both KEEP paths.

## THE TWO DIALS AND NO MORE (PROTOCOL rule 4)

`PANEL` {U56, B136, SMALL} x `RUNG SET` {CORE, EXT} = **6 combinations, ALL published**
(`.dialpoints.csv`, at three q each = 18 rows). LADDER is **not** a dial: all four are
rebuilt and reported, and the headline is restricted to **H and CADENCE**, the only two whose
rung set actually changes — N (9) and GROSS (10) carry **identical** rung lists at both
levels (1131/1134's structural fact) and are rung-inescapable BY CONSTRUCTION. STATISTIC is
not a dial (all 4 everywhere). **CONFIDENCE q is NOT a dial**: 0.90 headline, 0.80 and 0.95
reported beside it, nothing selected on them. **SEED BASE is not a dial**: 1131's own three
bases, so U56 and B136 reproduce bit for bit. Frozen at
1082/1094/1098/1102/1108/1110/1116/1117/1118/1122/1131's construction: CAND20 legs, cap INF,
max_vol 0.60, gross 0.75, min hold 126, N=20, W, 10 bps, LAG 1, warm-up 260, IS end
2016-12-31, block L=63, 1000 draws, `zlib.crc32` seeds.

## THE SMALL PANEL'S STAMP (idea 1074's recommendation, 1119's practice)

`data/small_meta.csv` lists **715 tickers; 52 dropped for `max_1d_move` >= 1.0**; the pool
served is **664 columns = 663 constituents + SPY as benchmark only**, tape **2010-01-04 ..
2026-09-11, 4,198 rows** (warm 3,938, IS 1,502, OOS 2,436). This idea's own text says
"483 sub-$2B names"; the loader serves 663 today — idea 706's rebuild and idea 1072's finding
that committed SMALL headlines move on it. **The stamp, not the label, is what every SMALL
number here refers to.** SPY is the 4b benchmark and not a constituent, so it is removed from
the selectable set and from the live-RULES-v2 comparand on that panel; **G_SPY prices that
choice rather than asserting it — had SPY been left selectable it would have been held on 0
of 871 rebalance dates, so the exclusion changes nothing measurable.**

**THE TAPE IS NOT MATCHED AND CANNOT BE, and the direction is stated before any number.**
SMALL starts 2010 against U56's 2008, so its bootstrap sees ~500 fewer rows and its floors
are **wider** for that reason alone — a bias **toward firing**, i.e. toward the queue's
premise and **against** this run's answer. The premise is refuted anyway.

## GATES 10 of 10 PASS, printed before any result number

G1 fast runner == `engine.backtest` 1.39e-17; G2 committed U56 W/H126/N=20 triple 3.18e-07
(15.5787% / 1.1397 / −19.1276%); G3 SPY OOS 1.70e-04; G4 live RULES v2 MaxDD 4.95e-05;
G5 determinism 0.00e+00; G6 `cadence_mask` == `engine.rebalance_mask` on D/W/M/Q, **0
differing bars on all three panels** (engine.py not modified); G9 every ladder live on every
panel (min Sharpe spread 1.79e-03); G_SPY reported above. **The two that matter: G7
reproduces 1131's committed `ksubsets_joint` on all four large-panel blocks at 2.78e-17, and
G8 reproduces its committed per-statistic counts on all 16 rows at 0.00e+00.** The two-panel
result this run extends is reproduced exactly before the third panel is read.
**HYPOTHESES 1 of 5** — and four of the five failures are the finding.

## THE MATCHED-k CENSUS — 126 four-rung subsets per block, on all three panels

| panel | ladder | S_FULL | S_OOS | CAGR | DD | **all four at once** | CORE fires all 4 |
|---|---|---|---|---|---|---|---|
| U56 | H | 1.0000 | 0.8810 | 0.5873 | 1.0000 | **0.5079** | yes |
| U56 | CADENCE | 0.1587 | 0.5635 | 0.1270 | 1.0000 | **0.0952** | yes |
| B136 | H | 1.0000 | 0.8333 | 0.7143 | 1.0000 | **0.7143** | yes |
| B136 | CADENCE | 0.3889 | 0.4841 | 0.3413 | 1.0000 | **0.1825** | yes |
| **SMALL** | **H** | 0.5556 | 0.3651 | 0.5556 | 1.0000 | **0.2778** | **no** |
| **SMALL** | **CADENCE** | 0.1587 | 0.3730 | 0.4762 | **0.4365** | **0.0794** | **no** |

Pooled over all 24 (panel, ladder, stat) blocks: **1,890 of 3,024 (0.6250)** four-rung
subsets fire, and **CORE fires in 21 of 24**. On the two large panels CORE fires in 16 of 16;
**every one of the three blocks where CORE is silent is on SMALL**.

## D1 — THE DIRECTION-FREE RE-CUT (POST-HOC AND LABELLED AS SUCH)

Declared hypothesis (c) asks whether CORE fires **where most subsets do not**. That
presupposes CORE fires. D1 drops the direction and asks the question the presupposition hides
— what share of matched-k subsets **agree with CORE's own firing state**, whichever it is?
It is a re-cut of two columns already in `.ksubsets.csv`, not a new measurement and not a
third dial.

| panel | CORE is the MINORITY state on | median agree share |
|---|---|---|
| U56 | 2 of 8 blocks | 0.7341 |
| B136 | 3 of 8 blocks | 0.7738 |
| **SMALL** | **6 of 8 blocks** | **0.4444** |

**The rung-CHOICE dependence 1131 discovered is not merely present on the small panel, it is
stronger there.** What does not transfer is the *direction*: on the large panels CORE is
atypical by firing where most subsets stay silent; on SMALL it is atypical in both directions
at once, silent on two blocks where a majority of subsets fire and firing on four where a
majority stay silent.

## THE SIX DIAL POINTS, at q = 0.90

| panel | rung set | blocks firing (of 8) | share |
|---|---|---|---|
| U56 | CORE | 8 | 1.0000 |
| U56 | EXT | 4 | 0.5000 |
| B136 | CORE | 8 | 1.0000 |
| B136 | EXT | 3 | 0.3750 |
| **SMALL** | **CORE** | **5** | **0.6250** |
| **SMALL** | **EXT** | **1** | **0.1250** |

q sensitivity, reported and never selected on — CORE share at q ∈ {0.80, 0.90, 0.95}: U56
0.5000 / 1.0000 / 1.0000; B136 0.6250 / 1.0000 / 1.0000; SMALL 0.2500 / 0.6250 / 0.7500. The
*level* moves with q on every panel; the *ordering* (SMALL below both large panels) does not.

## CORRECTION 1 — 1131's "DD is the only statistic un-resolvable everywhere" is a LARGE-PANEL fact

1131 published: *"DD is un-resolvable at every rung set on every block and is the only
statistic that is. A committed floor-keyed claim on DD ... is worth quoting."* On both large
panels DD fires on **126 of 126** subsets in all four blocks, exactly as committed. **On
SMALL CADENCE it fires on 55 of 126 (0.4365)**, and the block is silenceable by adding **4Q**
alone. So the one statistic the record was told it could safely quote a floor on is
un-resolvable **on large-cap tapes**, not on this tape in general.

## CORRECTION 2 — the non-monotonicity headline rests on ONE block of 24

1131's fatal detail — *"U56 H / S_OOS still fires on the FULL 9-rung EXT ladder yet falls
silent once H=210 alone is added"* — **reproduces exactly** (escape cost 1, cheapest rung
`210`, `fires_full_ext` True). It is also **the only such block across all three panels and
all 24 (panel, ladder, statistic) cells**, and **0 of the 8 SMALL blocks are non-monotone**.
The phenomenon is real and was correctly identified; quoted as a general property of the
trigger it is one observation. **What does generalise is the escape itself**: of the 21
blocks that fire at CORE, **14 can be silenced by adding rungs and 7 cannot be silenced by
any of the 31 supersets**, median cost **1 rung**, max 2 — and on the two large panels alone
this reproduces 1131's committed 10-of-16 / 6-un-silenceable / median-1 / max-2 figures
exactly.

## HYPOTHESES — 1 of 5, and the four failures carry the run

- **(a) H_REPRO SUPPORTED.** G7 2.78e-17 on 4 blocks, G8 0 mismatches on 16 rows.
- **(b) H_SMALL_FIRES_MORE REFUTED, in the opposite direction on both ladders.** The queue's
  inference from 1073's reliability gap — noisier panel, more un-resolvable ladders — is
  simply wrong here. A plausible reading, stated as a reading and not a result: firing
  requires the *largest* gap in a subset to be un-resolved, and the small panel's rung-to-rung
  gaps are **wider** as well as noisier, so the two effects cut against each other and the
  gap wins. This run does not decompose that and does not claim to.
- **(c) H_CORE_OUTLIER_SMALL REFUTED, on its precondition rather than its bar.** CORE fires
  at all four statistics on neither SMALL ladder, so the declared statistic is undefined in
  spirit. The STRICT (< 0.50) reading is also refuted. **D1 is the re-cut that answers the
  question actually being asked.**
- **(d) H_DEGENERATE REFUTED.** Neither SMALL ladder is degenerate, so SMALL **can** carry the
  test — the answer is a real negative, not an inconclusive one.
- **(e) H_NONMONO REFUTED.** 0 non-monotone blocks on SMALL; see Correction 2.

**THE DECISION RULE, applied as declared -> DOES NOT REPRODUCE on SMALL.** Reported as
declared. D1 is reported beside it, labelled post-hoc, and neither is hidden behind the other.

## RULE 8 AND BOTH KEEP PATHS — nothing proposed

Rungs chosen on IS alone per (panel, ladder, rung set, chooser), OOS read once. **72 rule-8
picks: 4b full 6, 4b OOS 6, 4a 0. Whole grid, 111 rungs: 4b full 17, 4b OOS 18, 4a 0 — U56
11 of 37, B136 6 of 37, SMALL 0 of 37.** Benchmarks: U56 SPY full 15.10% / 0.8829 / −33.72%
(halves 0.9588 / 0.8207), OOS 15.21% / 0.8711 / −33.72%; B136 SPY 15.16% / 0.8861 / −33.72%,
OOS 15.33% / 0.8767 / −33.72%; **SMALL SPY 14.06% / 0.8581 / −33.72% (halves 0.9138 / 0.8344),
OOS 15.33% / 0.8767 / −33.72%**; live RULES v2 U56 8.62% / 1.2007 / −12.05% (OOS 9.45% /
1.2762), B136 7.98% / 1.0993 / −12.24% (OOS 7.88% / 1.1059), **SMALL 4.30% / 0.6629 / −13.89%
(OOS 3.75% / 0.5590)**. Best pick clearing 4b full AND OOS: U56 / GROSS / CORE / C_ISSHARPE /
gross 0.75 — the standing anchor, full 15.58% / 1.1397 / −19.13% (halves 1.2037 / 1.0971),
OOS 16.97% / 1.1643 / −19.13%, 2.90x/yr. **All six passing picks are U56; SMALL passes 0 of
37 rungs on either KEEP path.**

**NOTHING PROPOSED.** The book at every rung is identical across both dials — only which
subsets get *called* fired changes — so 4a and 4b are invariant to this run's dials by
construction, and every passing pick is the standing top-20 / W / H126 family the record
already holds and has already PARKED. 4a is empty at every rung on every panel.

## WHAT THE RECORD SHOULD DO WITH IT, STATED NARROWLY (proposed, NOT enacted — rule 6)

1131's recommendation — *any committed floor-keyed claim should quote its rung LIST, not its
rung count* — survives this panel and is **strengthened**: the rung choice matters **more**
on the noisier tape, not less. Two of 1131's supporting statements should be re-quoted with a
panel stamp rather than as tape facts: **the DD survivorship claim** (Correction 1) and **the
non-monotonicity headline** (Correction 2). And the queue's own heuristic — *a noisier panel
fires more* — should not be used again without being measured; it is wrong on both movable
ladders here.

## SURVIVORSHIP (PROTOCOL rule 9)

U56 and B136 are CURRENT-CONSTITUENT lists; **the SMALL pool is worse** — a screen run on
names that exist today, so anything delisted, acquired or dropped out of the screen is absent,
and a small-cap pool loses names that way far more often than a large-cap one. Every CAGR and
drawdown **level** on SMALL is optimistic by an unknown and probably large amount. Firing
shares, rung-to-rung gaps and agreements contrast rungs over the same inflated tape and the
bias very largely cancels out of them; it does **not** cancel out of the 4b legs, measured
against SPY, a real index — so SMALL's 0 of 37 is if anything an **over**statement of how
close that panel comes.

## Files

`.grid.csv` (111 books), `.ksubsets.csv` / `.ksubsets_joint.csv` (the 3,024-subset census),
`.d1.csv`, `.dialpoints.csv` (the 6 dial points x 3 q), `.escapecost.csv` (exhaustive over
all 31 supersets x 24 blocks), `.walkforward.csv` (72 picks), `.gates.csv`,
`.hypotheses.csv`, `.console.txt`. Script
`research/backtests/2026-09-16_does-the-RUNG-CHOICE-effect-reproduce-on-the-SMALL-panel_cloud.py`.
