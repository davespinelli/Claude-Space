# Idea 1140 (lane B, 2026-09-16) — is DD's RUNG-ROBUST UN-RESOLVABILITY a PATH-FUNCTIONAL fact or a TAPE fact?

**ANSWERED = NEITHER. THE IDEA'S BINARY IS REFUTED ON BOTH HORNS, AND A THIRD, NARROWER
CARRIER IS NAMED AND MEASURED: it is MAX-ness, not path-functionality.** DD's two matched
PATH partners do **not** share its robustness (MAXDD 12 of 12 mover cells ROBUST, ULCER 7 of
12, CALMAR 9 of 12), which **KILLS the PATH-FUNCTIONAL reading as stated**; and MAXDD is
resolvable on **13 of 60** shortened-sub-tape cells against **0 of 12** on the full tape, so
it is not absolutely un-resolvable either — but it is still the most robust of all six
statistics at **every** tape fraction, which **KILLS the pure TAPE reading too**. The one
mechanism that survives: **MAXDD is the ONLY statistic of six whose realised rung GAP and
whose bootstrap SD BOTH GROW with tape length** (b(gap) +0.1419 / b(SD) +0.1654 pooled;
+0.2606 / +0.1654 on the mover ladders), the extreme-value signature. ULCER (a root-mean-
square of the *same* drawdown path) and CALMAR (a ratio *divided by* that same maximum) both
have **negative** SD exponents like the moment statistics. **BYCATCH, and it may matter more
than the headline: on the H and CADENCE ladders the NON-PATH statistics' realised rung gaps
shrink FASTER than their sampling SD (b(gap) −0.58 vs b(SD) −0.44), so their resolution gets
WORSE with a longer tape — those rung effects are ~0 and more data will never resolve them.**
No RULES change, no book promoted, no PROTOCOL edit (rule 6); RULES.md, PROTOCOL.md,
engine.py, scan.py, bot.py and baseline.py untouched.

**SELECTION:** lane B takes the LAST open idea; 1140 ended '## Open' and names no EDGAR /
Form 4 / 8-K / options / live-data source. It has a PRICE LEG — 74 rebuilt books over 4
ladders x 2 panels, block-bootstrapped at 6 sub-tapes x 3 seed bases — so it carries this
run's mandatory rule-8 walk-forward and both KEEP paths.

## THE TWO DIALS AND NO MORE (PROTOCOL rule 4)
`STAT SET` {S_NONPATH, S_PATH, S_ALL} x `SUB-TAPE FRACTION` {1/1, 1/2, 1/3} = **9
combinations, ALL published** (`.grid.csv`, and again at q=0.80 and q=0.95). **PANEL (U56,
B136), LADDER (N, H, GROSS, CADENCE) and RUNG SET (CORE, EXT) are NOT dials** — all 2 x 4 x 2
x 6 x 3 = 5,184 cells are published in `.cells.csv`. **CONFIDENCE q is NOT a dial**: 0.90 is
the headline, 0.80 and 0.95 are reported beside it at every point and nothing is selected on
them. **BLOCK LENGTH is NOT a dial**: L=63 frozen from 1098/1102/1110/1131. Frozen at
1082/1094/1098/1102/1108/1110/1116/1117/1118/1122/1131's construction: CAND20 legs, cap INF,
max_vol 0.60, gross 0.75, min hold 126, N=20, W, 10 bps, LAG 1, warm-up 260, IS end
2016-12-31, 1000 draws, crc32 seeds, seed bases [11311131, 11171117, 11161116].

## THE DESIGN — THREE MATCHED PAIRS, ONE DIFFERENCE INSIDE EACH
The idea's word is "path functional", so the test is a matched one: three pairs in which the
*only* thing that differs is whether the statistic reads the ORDER of the same return stream
or only its MOMENTS.

| role | NON-PATH (moments) | PATH (order-dependent) |
|---|---|---|
| level | CAGR | **MAXDD** |
| dispersion | VOL | ULCER |
| ratio | SHARPE | CALMAR |

x six **disjoint** sub-tapes of the warm record (1 whole, 2 halves, 3 thirds), so 1131's own
16 blocks are re-run at three tape lengths.

## GATES 11 of 11 PASS, printed before any result number
G1 fast runner == `engine.backtest` 1.39e-17; G2 committed U56 W/H126/N=20 triple 3.18e-07
(15.5787% / 1.1397 / −19.1276%); G3 SPY OOS 1.70e-04; G4 / G4b committed U56 n=12 and B136
n=15 triples 4.97e-05 / 2.13e-05; G5 live RULES v2 MaxDD −12.05% at 4.95e-05; G6 determinism
0.00e+00; G7 `cadence_mask` == `engine.rebalance_mask` on D/W/M/Q (engine.py not modified);
G8 reproduces all 54 rows of 1110's committed CORE grid at 0.00e+00; **G9 reproduces 1131's
committed 16-block table on all 12 shared blocks at 0.00e+00** (1131's S_FULL == this run's
SHARPE, its CAGR == CAGR, its DD == MAXDD, same seeds, same draws); G10 every statistic live
(min median |gap| 6.09e-04). **HYPOTHESES 2 of 5 SUPPORTED.**

## RESULT 1 — 1131's 16 blocks, re-run with all six statistics (full tape, q=0.90)
ROBUST counts over the 12 mover cells per statistic (2 panels x {H, CADENCE} x 3 seed bases):

| pair | NON-PATH | ROBUST | PATH | ROBUST |
|---|---|---|---|---|
| level | CAGR | **0 / 12** | **MAXDD** | **12 / 12** |
| dispersion | VOL | 0 / 12 | ULCER | 7 / 12 |
| ratio | SHARPE | 6 / 12 | CALMAR | 9 / 12 |

The pair ordering runs the PATH way in **all three** pairs, so path-functionality is *a*
contributor. But **H_PATH_FIRES is REFUTED**: if it were *the* carrier the PATH arm would be
12/12/12, and it is 12/7/9. ULCER and CALMAR both ESCAPE on the U56 blocks. **MAXDD is the
only statistic of the six that never escapes anywhere.** N and GROSS carry identical rung
lists at both levels (1134's defect) and are excluded from every mover count; they are
published anyway.

## RESULT 2 — the 9 dial cells (INF share at EXT on the mover ladders, q=0.90)

| stat set | 1/1 | 1/2 | 1/3 |
|---|---|---|---|
| S_NONPATH | 0.2500 | 0.1250 | 0.0648 |
| S_PATH | 0.7778 | 0.6111 | 0.5926 |
| S_ALL | 0.5139 | 0.3681 | 0.3287 |

Per statistic at 1/1 → 1/3: CAGR 0.00 → 0.00, VOL 0.25 → 0.03, SHARPE 0.50 → 0.17, **MAXDD
1.00 → 0.83**, ULCER 0.58 → 0.58, CALMAR 0.75 → 0.36. At q=0.80 the non-path arm is 0.000 at
every fraction and the path arm 0.417 / 0.375 / 0.250; at q=0.95, 0.444 / 0.361 / 0.241
against 0.917 / 0.750 / 0.759. **This is NOT the test and was declared as not-the-test before
it was computed** — a sub-tape changes length *and* regime at once (see the LIMIT below).

## RESULT 3 / 6 — the exponents, pre-registered and post-hoc, both published
Fit log(y) = a + b·log(n) over the six sub-tapes, per (panel, ladder, rung set, statistic),
medians pooled over the 3 seed bases first.

| statistic | arm | b(ratio) all 16 | b(gap) all 16 | b(SD) all 16 | b(ratio) movers | b(gap) movers | b(SD) movers |
|---|---|---|---|---|---|---|---|
| CAGR | NON-PATH | +0.1029 | −0.3495 | −0.4675 | −0.1671 | −0.7110 | −0.4592 |
| VOL | NON-PATH | +0.2586 | +0.0004 | −0.3181 | −0.0819 | −0.4424 | −0.3181 |
| SHARPE | NON-PATH | +0.0625 | −0.4231 | −0.4482 | −0.1046 | −0.6086 | −0.4482 |
| **MAXDD** | PATH | +0.1142 | **+0.1419** | **+0.1654** | +0.0543 | **+0.2606** | **+0.1654** |
| ULCER | PATH | +0.0978 | −0.1221 | −0.1916 | +0.0158 | −0.1560 | −0.1916 |
| CALMAR | PATH | +0.3581 | −0.1699 | −0.5543 | +0.0103 | −0.4864 | −0.5543 |

**H_EXPONENT is REFUTED** (arm medians +0.1107 non-path vs +0.1293 path, against bars of
+0.35 and +0.20) and so is **H_GAP_GROWS** (path b(gap) −0.0295 against a +0.10 bar, non-path
−0.3120 against a ±0.10 bar). Both were refuted for the *same* reason and it is the useful
one: the realised rung gap is not a stable quantity plus noise, it is **mostly noise**, so it
shrinks with tape length instead of standing still.

**A DEFECT IN THIS RUN'S OWN PRE-REGISTRATION, reported and NOT fixed (RESULT 6, labelled
POST-HOC):** H_EXPONENT's arm medians pool all 16 cells per statistic including the N and
GROSS ladders, whose rung sets cannot move and on which 1131's claim does not live. Restricted
to the 8 mover cells — a re-cut of already-published columns, not a third dial — the
comparison moves: **NON-PATH −0.1251, PATH +0.0327, separation −0.1578**. The pre-registered
verdict below is **not** rewritten on the strength of it.

**The robust part of this table is the SIGN STRUCTURE, which is identical in both cuts:
MAXDD is the only statistic with BOTH b(gap) and b(SD) positive.** Its gap and its dispersion
both grow with the tape; the other five all have their SD *fall*, including the two path
functionals. That is the extreme-value signature, and it re-derives 1110's +0.2093 vs −0.4540
in a second currency.

## RESULT 4 / 8 — where MAXDD DOES resolve
13 of 60 shortened-sub-tape mover cells at EXT are resolvable, against **0 of 12** on the full
tape, over 5 distinct (panel, ladder, sub-tape) combinations of 20 — B136 CADENCE F2_2, B136
H F2_2, B136 H F3_3, U56 H F3_1 (all 3 seed bases each) and U56 H F2_1 (1 of 3). **So
H_TAPE_ESCAPE is SUPPORTED**: there are stretches of this record on which DD's rung gaps do
resolve. Against that: MAXDD is still 13/60 where CAGR is 57/60, VOL 57/60, SHARPE 50/60,
ULCER 24/60 and CALMAR 35/60, so the tape reading does not carry it either.

## RESULT 5 — the level leg 1110 flagged
Median |level| over rungs by fraction, with its own exponent: CAGR 15.58 / 15.09 / 14.81
(+0.046), VOL 13.84 / 13.62 / 14.03 (−0.008), SHARPE 1.084 / 1.102 / 1.099 (−0.014), **MAXDD
21.52 / 16.67 / 16.32 (+0.265)**, ULCER 4.79 / 4.26 / 4.58 (+0.056), CALMAR 0.735 / 0.850 /
0.910 (−0.196). Only MAXDD's own level grows materially with the tape it is measured on —
again the maximum, not the path.

## THE LIMIT, NAMED AND MEASURED (RESULT 7) — this is why the exponents are bounded, not sharp
A sub-tape differs from the full tape in **length AND regime**. Measured on the same published
column, the WITHIN-fraction spread (same length, different stretch — pure regime) against the
BETWEEN-fraction move (length plus regime): CAGR 3.50x, VOL 5.52x, SHARPE 1.66x, MAXDD 5.19x,
ULCER 61.5x, CALMAR 9.07x. **The regime noise is 1.7 to 61 times the length effect being
fitted through it.** Every exponent magnitude in this file must be read as an upper bound on
precision, not as a measurement; only the SIGN structure, which reproduces across both cuts,
all three seed bases and both panels, is asserted.

## VERDICT AGAINST THE PRE-REGISTERED DECISION RULE
Declared before any number: PATH-FUNCTIONAL iff H_PATH_FIRES and H_NONPATH_ESC and
H_EXPONENT; TAPE iff H_TAPE_ESCAPE and PATH b(ratio) not below NON-PATH's; MIXED otherwise.
H_PATH_FIRES **False**, H_NONPATH_ESC **True**, H_EXPONENT **False**, H_TAPE_ESCAPE **True**,
PATH +0.1293 ≥ NON-PATH +0.1107 → **the rule outputs TAPE**. It is reported as the rule's
output and no further. The rule was written to arbitrate two readings that both turned out to
be wrong, and its TAPE clause fires on an arm median (+0.1293 vs +0.1107) that is inside the
regime noise measured above and that reverses on the mover-only re-cut. **The finding this
run stands behind is the narrower one: the carrier is MAX-ness — a strict subset of
path-functionality — and it is partly, not wholly, tape-dependent.**

## RULE 8 AND BOTH KEEP PATHS — 74 books, 48 IS picks, NOTHING PROPOSED
The books are byte-identical to 1131's by construction, so this leg is invariant to both
dials; it is run because rule 4 requires it. Rung chosen on IS 2009–2016 alone, OOS 2017–2026
read once.

- U56 SPY full 15.10% / 0.8829 / −33.72%, halves 0.9588 / 0.8207, OOS 15.21% / 0.8711 / −33.72%
- U56 RULES v2 (live) full 8.62% / 1.2007 / −12.05%, halves 1.2322 / 1.1760, OOS 9.45% / 1.2762 / −12.05%
- B136 SPY full 15.16% / 0.8861 / −33.72%; B136 RULES v2 full 7.98% / 1.0993 / −12.24%
- 48 IS picks: **4b full 6, 4b OOS 6, 4a 0**, median OOS Sharpe 1.0244, median regret +0.0228
- whole 74-rung grid: 4b full 17, 4b OOS 18, **4a 0**
- every 4b pass among the IS picks is the **frozen default rung** (U56 GROSS 0.75 and U56
  CADENCE W): full 15.58% / 1.1397 / −19.13%, halves 1.2037 / 1.0971, OOS 16.97% / 1.1643 /
  −19.13% vs SPY OOS 15.21% / 0.8711 / −33.72%
- best IS pick by OOS Sharpe: U56 H/CORE C_ISSHARPE pick 252 — full 15.88% / 1.1648 / −21.84%,
  halves 1.2236 / 1.1266, OOS 17.31% / 1.1931 / −21.84%

**4a is 0 of 74 at every rung** (the live book's −12.05% MaxDD is unreachable for these
books). The 4b passes are the incumbent default, already in the record; **nothing is
proposed, no memo, no RULES change.**

## SURVIVORSHIP (rule 9)
U56 and B136 are CURRENT-CONSTITUENT panels. Every level here is optimistic and every
exponent is fitted on that inflated tape; the bootstrap prices SAMPLING error only and cannot
correct the bias. **Cross-read, not recomputed: 1141 (cloud, same day) found DD's
"un-resolvable everywhere" is a LARGE-PANEL fact — it fires less on the SMALL panel.** That
is independent evidence on the same side as RESULT 4, and this run does not rebuild SMALL.

## WHAT A LATER RUN SHOULD DO (filed as 1146–1148)
The extreme-value reading makes a testable prediction this run did not test: a *truncated*
maximum (worst k-day drawdown, or the 95th percentile of the drawdown distribution rather
than its max) should behave like ULCER, not like MAXDD. And the bycatch — non-path rung gaps
converging to ~0 on the H and CADENCE ladders — bears directly on every committed argmax on
those ladders.

Script `research/backtests/2026-09-16_is-DD-s-RUNG-ROBUST-UN-RESOLVABILITY-a-PATH-FUNCTIONAL-fact-or-a-TAPE-fact_B.py`,
11 CSVs, console log, 5 LEADERBOARD rows.
