# Idea 1150 (lane C, 2026-09-16) — is-the-CAGR-FLOOR-a-DE-GROSSING-DETECTOR-rather-than-a-COST-LEG

**ANSWERED = YES, IT IS A DE-GROSSING DETECTOR AND NOT A COST LEG — and the queue's own
wording of the hand-over is REFUTED: it is not SHARPE -> CAGR, it is L_DD -> L_CAGR, two
EXPOSURE legs, with no Sharpe leg binding anywhere on U56 at PROTOCOL's cost rung.**
No RULES change, no book promoted, no PROTOCOL edit (rule 6); RULES.md, PROTOCOL.md,
scan.py, bot.py, engine.py and baseline.py untouched. SELECTION: lane C takes the SECOND
open idea; 1150 was second in `## Open` and is not EDGAR / Form 4 / 8-K / options /
live-data. It is a pure price run — 66 books, 528 scored cells, 48 rule-8 picks — so it
carries this run's mandatory rule-8 walk-forward and both KEEP paths.

**THE TWO DIALS AND NO MORE (PROTOCOL rule 4, and the queue names both):** `GROSS RUNG`
{0.200 .. 1.000 step 0.025, 33 rungs} x `COST RUNG` {0, 2, 5, 7.5, 10, 15, 25, 50 bps} =
**264 per panel, 528 in all, EVERY ONE PUBLISHED** in `.grid.csv` (59 columns). PANEL
{U56, B136} is not a dial (both reported everywhere). **BENCHMARK VARIANT is not a dial
either:** `B_SPY` is the PROTOCOL floor and the headline; `B_SPYCOST` (SPY charged the same
rate on its own turnover) and `B_SPYGROSS` (SPY held at the SAME gross, rest in cash) are
CONTROLS computed at all 528 cells and never selected on. The fine ladder **NESTS** the
record's committed 0.30..0.75 step-0.05 rungs (G10), so every committed gross-ladder number
is re-derivable from this file. Frozen at 1082/1094/1098/1102/1108/1110/1116/1117/1118's
construction: CAND20 legs, cap INF, max_vol 0.60, min hold 126, N=20, W, LAG 1, warm-up
260, IS end 2016-12-31, zero cash, block L=63, 1000 draws, crc32 seeds, q=0.90.

**THE BINDING-LEG RULE, DECLARED BEFORE ANY NUMBER.** Each 4b leg is re-expressed as the
signed fraction of its OWN bar still in hand — Sharpe legs `(book-SPY)/|SPY|`, `L_DD`
`(0.60|SPY_dd|-|dd|)/(0.60|SPY_dd|)`, `L_CAGR` `(CAGR-0.70*SPY_CAGR)/|0.70*SPY_CAGR|` — so
the five sit on one scale and **BINDING = argmin of the five**, negative meaning that leg
fails. `g*` (the hand-over) = the highest gross rung whose binding leg is `L_CAGR`;
MONOTONE means `L_CAGR` binds at every rung at or below `g*` and none above.

**GATES 10 of 10 PASS, printed before any result number.** G1 fast runner ==
`engine.backtest` 1.39e-17; G2 committed U56 W/H126/N=20 triple 3.18e-07 (15.5787% /
1.1397 / -19.1276%); G3 SPY OOS 1.70e-04; G4 1098/1102's committed U56 n=12 triple
4.97e-05; G5 live RULES v2 MaxDD 4.95e-05; G6 determinism 0.00e+00; G7 `cadence_mask` ==
`engine.rebalance_mask` on D/W/M/Q, 0 differing bars; **G9 the post-hoc cost transform
`net = gross - turnover*c/1e4` == `engine.backtest(cost_bps=25)` at 6.94e-18**, which is
what licenses pricing 8 cost rungs off one book per gross rung; G10 the fine ladder nests
the committed rungs. **G8 is the one that matters: the committed GROSS-ladder grid
reproduces on all 20 rows x 6 statistics at 2.22e-16 with 0 of 100 leg-flag
disagreements** — the object under test is reproduced exactly before anything new is read.
**HYPOTHESES 5 of 5 SUPPORTED.**

**A CORRECTION TO THE QUEUE'S OWN PREMISE, STATED FIRST.** The idea text says "all four
CAGR-killed cells sit on the GROSS ladder (U56 g 0.55/0.60/0.65, B136 g 0.50)". Those rungs
are the record's own **first PASSING** rungs, not its killed ones. Every committed grid
this tree can read — 40+ files carrying the gross ladder, G8's comparand among them — puts
the L_CAGR failures at **U56 g <= 0.50 (5 rungs of 10) and B136 g <= 0.45 (4 of 10)** at 10
bps. The count "four" is B136's. The direction of the finding is unaffected and the
run tests the boundary it can reproduce, not the one the queue wrote down.

**THE ANSWER. The hand-over EXISTS, is MONOTONE at 16 of 16 (panel, cost) points, and sits
at g* = 0.600 on U56 and 0.525 on B136.** Below it `L_CAGR` binds; above it `L_DD` does.

**IT IS NOT A COST OBJECT.** Moving cost from 0 to 50 bps — **five times PROTOCOL's rung**,
the full width of the record's own ladder — moves `g*` by **exactly one rung of 0.025 on
U56 (0.600 -> 0.625, and only past 15 bps) and by ZERO rungs on B136**. On the paired block
bootstrap (idea 1012's basis: the same 1,000 draws on both arms, so the tape cancels) the
median `g*(50bps) - g*(0bps)` is **+0.0250 on U56 [90% -0.000, +0.050] and +0.0000 on B136
[-0.025, +0.029]**, with `|delta| <= 1 rung` in **89.8% / 92.9%** of draws and exactly zero
in 35.2% / 44.1%.

**THE MECHANISM, MEASURED.** At `g*` the book's CAGR sits 8.60 pp/yr (U56) and 10.44 pp/yr
(B136) below the same book at gross 1.00 with no costs, while 0 -> 10 bps of cost accounts
for 0.263 pp and 0.257 pp of it: **cost is 3.0% and 2.4% of the drop that puts the book
through the floor.** The other ~97% is de-grossing. And Sharpe does not notice: across the
WHOLE 0.20..1.00 ladder the full-sample Sharpe spread is **0.0016 (U56, 0 bps) to 0.0116
(B136, 50 bps)** while the CAGR spread is **15.2 to 17.6 percentage points**. The queue's
"1.1390 vs 1.1397" is not a near-miss, it is the shape of the whole ladder.

**THE CONTROL THAT DECIDES IT. Under a GROSS-MATCHED floor — SPY held at the same gross as
the book, remainder in cash — `L_CAGR` binds at 0 of 528 cells and FAILS at 0 of 528.** The
entire CAGR leg on the gross ladder is an artefact of scoring a de-grossed book against a
fully-invested benchmark. Charging the benchmark instead (`B_SPYCOST`) changes `g*` at **0
of 16** points, because buy-and-hold SPY has no turnover to charge: **the floor's asymmetry
is an EXPOSURE asymmetry, not a cost-rate asymmetry.** 1063's one-sided-handicap reading is
the right object but the wrong currency.

**THE QUEUE'S "SHARPE -> CAGR" WORDING IS REFUTED.** Over all 528 cells a Sharpe-family leg
(`L_H1`/`L_H2`/`L_OOS`) is the binding leg at **47 (0.089)**; `L_DD` binds at 231 and
`L_CAGR` at 250. On **U56 at every cost rung from 0 to 25 bps a Sharpe leg binds at 0 of 33
gross rungs**; one appears only at 50 bps. `L_OOS` never binds anywhere. The gross ladder's
4b verdict is decided end to end by two EXPOSURE legs pulling opposite ways, which is also
why **the 4b pass set at 10 bps is a CONTIGUOUS WINDOW and not a peak: U56 gross
0.525..0.775 (11 rungs), B136 0.500..0.725 (10).** 4b on this ladder selects an exposure
band, and every rung inside it is the same book scaled.

**THE LIMIT, MEASURED NOT ASSERTED.** `g*` as a NUMBER is barely resolvable: its unpaired
90% block-bootstrap interval spans **8 rungs on both panels** (U56 [0.450, 0.625], B136
[0.400, 0.575]), so "the hand-over is at 0.600" is not a publishable figure at this tape
length. What IS resolvable is its INVARIANCE, because that comparison is paired and the
tape cancels. Every claim above is made in the paired currency. `L_OOS` is undefined on a
resampled tape and is excluded from the bootstrap arm only (4 legs there, 5 in the point
arm); stated, not hidden.

**RULE 8 AND BOTH KEEP PATHS — 66 books, 528 cells, 48 IS-only picks, NOTHING PROPOSED.**
Only the 10 bps rung is a PROTOCOL-legal book (rule 2) — a book cannot choose its cost
rate — so the KEEP question is asked there and nowhere else: **66 cells, 4b full 21, 4b OOS
22, 4a 0.** Benchmarks: **U56 SPY full 15.10% / 0.8829 / -33.72% (halves 0.9588/0.8207),
OOS 15.21% / 0.8711 / -33.72%; B136 SPY 15.16% / 0.8861 / -33.72%, OOS 15.33% / 0.8767 /
-33.72%; live RULES v2 U56 8.62% / 1.2007 / -12.05% (halves 1.2322/1.1760, OOS 9.45% /
1.2762), B136 7.98% / 1.0993 / -12.24% (OOS 7.88% / 1.1059).** Best 10 bps cell passing 4b
on BOTH the full sample and OOS is **U56 gross 0.775: full 16.10% / 1.1398 / -19.72%
(halves 1.2038 / 1.0972), OOS 17.54% / 1.1644 / -19.72%, 2.99x/yr** against the incumbent
gross 0.75's full 15.58% / 1.1397 / -19.13%, OOS 16.97% / 1.1643 / -19.13% — **one rung
away, +0.0001 of full Sharpe, inside every resolution floor the record has measured, and
the whole 11-rung passing window spans 0.1566 of OOS Sharpe end to end.** **4a is 0 of 528
at every rung and every cost rung.** And rule 8 is emphatic: **0 of 48 IS-only picks pass
4b full, 4b OOS or 4a.** `C_ISSHARPE` and `C_ISCAGR` both pick **gross 1.00** on both
panels (which fails `L_DD`) and `C_ISDD` picks **gross 0.20** (which fails `L_CAGR`) — the
three honest choosers land on the two ENDPOINTS, i.e. on the two binding legs, and the
passing band in the middle is unreachable by any of them. Nothing is proposed; every
passing rung is the standing top-20 / W / H126 family the record already holds and has
already PARKED.

**SURVIVORSHIP (rule 9).** U56 and B136 are CURRENT-CONSTITUENT panels, so every CAGR and
drawdown LEVEL here is optimistic and the `L_CAGR` and `L_DD` bars are both measured against
an inflated book. The bias does NOT cancel out of the 4b legs. It very largely DOES cancel
out of this run's headline, which contrasts the SAME book against ITSELF across cost rungs
and against a de-grossed version of the same benchmark; the invariance claims are ratios
over one tape, not levels.

**WHAT THE RECORD SHOULD DO WITH IT, STATED NARROWLY (proposed, NOT enacted — rule 6).**
Three things. (1) A 4b verdict on a GROSS ladder should not be read as a cost verdict: at
PROTOCOL's rung cost moves the boundary by 0 to 1 rung of 0.025 and accounts for ~3% of the
CAGR drop that causes the failure. (2) Any committed claim of the form "this book dies on
the CAGR floor" that lives on the gross ladder should carry the **gross-matched control**,
which zeroes the leg at 528 of 528 cells. (3) The queue's "the binding leg hands over from
Sharpe to CAGR" should be re-quoted as **L_DD -> L_CAGR**; no Sharpe leg binds on U56 at
PROTOCOL's cost rung at any gross.

Script `research/backtests/2026-09-16_is-the-CAGR-FLOOR-a-DE-GROSSING-DETECTOR-rather-than-a-COST-LEG_C.py`,
9 CSVs, console log, 6 LEADERBOARD rows. Follow-ups filed 1152 (is the 4b gross WINDOW's
width a panel object or a tape object), 1153 (does any committed CAGR-floor death survive a
gross-matched benchmark), 1154 (why do all three honest choosers land on a gross ENDPOINT).
