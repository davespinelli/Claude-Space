# Idea 1207 (lane C, 2026-09-17) — how many committed RANGE claims quote a MULTIPLE BELOW THEIR OWN COUNT INFLATION, and were ADJUDICATED ON IT?

**ANSWERED = NONE. ZERO committed verdicts change at any of the nine dial cells. Idea 1155's
"36 of 90 fail" is very largely an artefact of its own COUNT HARVEST, not of the record: 78 of
96 checkable C_STRICT units (0.8125) carry harvested counts OUTSIDE the d2 table's entire
domain, so their "inflation" was the clipped constant d2(12)/d2(k_min) — a number with no
relation to the claim. Of the 18 that are in domain, every one was hand-read, and the six that
really are range-vs-range comparisons all survive or are already published as the no-effect
reading.**

No RULES change, no book promoted, no PROTOCOL edit (rule 6); RULES.md, PROTOCOL.md, scan.py,
bot.py and baseline.py untouched. SELECTION: this lane takes the SECOND open idea; 1207 was
second in '## Open' and is not EDGAR / Form 4 / 8-K / options / live-data. Price leg of 66 real
rung books, 336 chooser pick-cells, 252 realised ladder pairs and 24 stitched deployable
curves, so it carries this run's mandatory rule-8 walk-forward and both KEEP paths.

## The two dials and no more (rule 4, and the queue names both)

`CLAIM SET` {C_STRICT, C_PROX, C_ALL} × `NO-EFFECT RULE` {R_MIN, R_MAX, R_BAND} = **9 cells,
EVERY ONE PUBLISHED** in `.grid.csv`. R_MIN reads the verdict as resting on the SMALLEST quoted
multiple (1155's own headline leg), R_MAX on the LARGEST (1155's second leg, 73 of 90), R_BAND
on the FLOOR of an explicit "x to y x" band where one exists (1155's own G0b treatment of
1140's "1.7x – 61x") and on the smallest otherwise.

NOT dials, reported at every value: PANEL {U56, B136, SMALL} (rule 9); the record's four
ladders N (6 rungs) / H (4) / GROSS (10) / CADENCE (2), inherited whole; the DOMAIN split; the
four choosers; the 4a and 4b legs.

## Arm 0 — the arithmetic, printed before any text or any price was read

For k iid N(0,1) draws E[max−min] = d2(k), **tabulated for k = 2..12**, and the longest ladder
this record has ever published is 10 rungs. Monte Carlo at 2e5 draws reproduces every published
constant to **2.38e-03** (gate G0).

**THE SUBSTITUTION CONVENTION IS NOT A THIRD DIAL, AND THE PROOF CARRIES NO DATA.** A verdict
resting on a multiple M rests on the comparative M/I > 1, I being the inflation
d2(k_max)/d2(k_min). Setting M to no effect gives: M′=1 → 1/I < 1, flips ALL; M′=I → I/I = 1,
flips ALL; M′=M/I → flips exactly {M ≤ I}. **Every convention is the same threshold at I.**
Gated on the actual 100 units whose counts differ: M′=1 flips 1.0000, M′=I flips 1.0000, M′=M/I
flips 0.4000 and matches {M ≤ I} with **0 mismatches** (gate G3).

Outcomes were pre-declared in the same block: (A) MANY ≥ 10 verdicts change; (B) FEW 1–9;
(C) NONE; (D) UNTRACEABLE.

## Arm A — the census replayed, the domain split, and the trace

**(A1) 1155's CENSUS REPRODUCED BIT FOR BIT on the corpus it actually ran against** (commit
`4ee8b6f~1`, the parent of 1155's own commit — its census was computed before its own artefacts
existed): **32,930 units / 1,137 markdown files / 313 C_STRICT / 90 checkable / smallest
multiple survives at 54 (0.6000) / median inflation 1.8999** — every figure 1155 committed
(gate G1). The live corpus at this run's HEAD is **33,224 units** (7,052 LEADERBOARD rows, 636
CHANGELOG paragraphs, 1,144 markdown artefacts).

**(A2) THE 9-CELL GRID, EVERY CELL PUBLISHED.**

| claim set | rule | checkable | FAILS | (share) | of which VACUOUS | IN-DOMAIN | in-dom & carries a verdict |
|---|---|---|---|---|---|---|---|
| C_STRICT | R_MIN | 96 | 39 | 0.4062 | **31** | 8 | 4 |
| C_STRICT | R_MAX | 96 | 19 | 0.1979 | 16 | 3 | 2 |
| C_STRICT | R_BAND | 96 | 38 | 0.3958 | 30 | 8 | 4 |
| C_PROX | R_MIN | 129 | 46 | 0.3566 | 36 | 10 | 5 |
| C_PROX | R_MAX | 129 | 23 | 0.1783 | 19 | 4 | 3 |
| C_PROX | R_BAND | 129 | 45 | 0.3488 | 35 | 10 | 5 |
| C_ALL | R_MIN | 129 | 46 | 0.3566 | 36 | 10 | 5 |
| C_ALL | R_MAX | 129 | 23 | 0.1783 | 19 | 4 | 3 |
| C_ALL | R_BAND | 129 | 45 | 0.3488 | 35 | 10 | 5 |

**(A3) THE DOMAIN SPLIT — WHY THE 36 IS NOT A 36.** 1155's count harvest reads ANY
"⟨n⟩ rungs / cells / points / books / rows / panels" token anywhere in the unit. **78 of the 96
checkable C_STRICT units (0.8125) have a harvested count outside k = 2..12 entirely** — the
largest is **1,087,557**, the median **126** — so their inflation was computed at the CLIPPED
value d2(12)/d2(k_min). Those units are VACUOUS, not failing, and are never merged into the
answer (gate G10 partitions the set exactly).

**(A4) THE TRACE — ALL 24 IN-DOMAIN UNITS HAND-READ, ONE LINE EACH, PUBLISHED IN `.audit.csv`**
(gate G9: 0 unaudited). Kinds: **A_PAIR 6** (a genuine range-vs-range comparison over two
different counts — the object d2 was built for), **A_OTHER 10** (a range against a point gap,
an SD or itself at equal counts — d2 does not apply), **A_NOTMULT 8** (a portfolio weight, a
protocol bar, a tolerance, a dial step — not a comparative multiple at all).

**THE TEN FAILING IN-DOMAIN UNITS UNDER R_MIN, AND WHY NONE OF THEM MOVES A VERDICT:**

- 4 are **A_NOTMULT**: `d1eff3e1a0` the 0.25x is a sleeve WEIGHT; `d5d3a4d1d0` and `b5fd35fbeb`
  are GATES / grid rows whose tokens are tolerances and carry no verdict; `f8febbcdba` 1.0x is
  a gross level and the 4a PASS rests on the halves.
- 2 are **A_OTHER**: `389bc03035` ("spread = −0.85 x GAP") and `d6206b7d66` ("within-rung sd is
  0.76 x GAP") compare a RANGE or an SD to a POINT GAP. **d2 is a range constant and does not
  apply in either direction**, and both verdicts rest on other statistics (a fitted sign; 65 of
  165 seed pairs).
- 4 are **A_PAIR — the only ones the question is really about, and all four hold:**
  - `ca229253f8` / `97f64224ae` (idea 412b, row and memo): "lambda spans a median **2.39x** of
    turnover against cadence's **6.38x**". This IS range-vs-range across two dials — but
    **lambda's ladder is the LONGER of the two** (a 13-rung coverage ladder plus a 10-rung
    absolute-n ladder against cadence's D/W/M/Q), so **count inflation runs AGAINST cadence and
    the ADOPT CADENCE verdict is if anything understated.**
  - `a5001741b0` (idea 1209's own row): the 1.4426x **IS** d2(9)/d2(4), published BY that run as
    a data-free count artefact. Its committed verdict (ANSWERED = NO, the shift changes no
    verdict) **already is the no-effect reading.**
  - `05d6fd1eb4` (idea 572): "Q5 (3 rungs) 0.0801 → Q9 (7 rungs) 0.1080" — genuinely
    count-exposed, and the growth **1.348x sits BELOW d2(7)/d2(3) = 1.598**, which STRENGTHENS
    the committed verdict that the +0.0801 is a rung-selection artefact.

**VERDICTS THAT CHANGE: 0 under R_MIN, 0 under R_MAX, 0 under R_BAND. OUTCOME (C) NONE.**

## Arm B — pricing the verdict change: rule 8 and both KEEP paths

The record's habit *"this dial's spread is X times that one's, so tune this dial"* IS a range
multiple across two ladders of different rung counts, so it is made live:

- **CH_RAW** tune the widest RAW max−min ladder (the habit; licensed by M > 1, always tunes).
- **CH_MATCHED** tune it ONLY if M > I = d2(k_wide)/d2(k_narrow); else stay at the anchor.
  **This is CH_RAW with the failing verdicts set to no effect, and the paired delta IS the
  price of the change.**
- **CH_D2** tune the argmax of spread/d2(k) (1155's M_D2 repair). **CH_ANCHOR** never move.

Folds = one calendar year of OOS, stepped one year, 2013–2026, IS expanding from the warm-up to
the day before the fold; folds tile the span with no overlap and no gap (gate G7). 10 bps, t+1,
260-row warm-up, DECIDE-AT-t selection (lag=1 — idea 1209's correction to the record's
inherited builder). **336 pick-cells = 3 panels × 14 folds × 8 choosers, 42 picks per chooser.**

**THE LARGEST FINDING IN THIS ARM, AND IT IS UN-SELECTED: over all 252 realised ordered ladder
pairs THE COUNT-INFLATION BAR SITS BELOW 1 AT 0.5317.** More than half the time the ladder with
the WIDER spread is the SHORTER one, so the count difference runs AGAINST the conclusion being
drawn rather than for it — the opposite of the direction 1155's alarm assumes.

| wider / narrower | k | n | median multiple | bar I | survives | bar < 1 |
|---|---|---|---|---|---|---|
| CADENCE / GROSS | 2/10 | 42 | 22.3651 | 0.3667 | 1.0000 | yes |
| CADENCE / H | 2/4 | 3 | 1.2285 | 0.5481 | 1.0000 | yes |
| H / CADENCE | 4/2 | 39 | 2.6945 | 1.8245 | **0.6923** | no |
| H / GROSS | 4/10 | 42 | 47.2044 | 0.6690 | 1.0000 | yes |
| H / N | 4/6 | 5 | 1.1145 | 0.8123 | 1.0000 | yes |
| N / CADENCE | 6/2 | 42 | 3.6286 | 2.2461 | **0.8810** | no |
| N / GROSS | 6/10 | 42 | 97.9919 | 0.8235 | 1.0000 | yes |
| N / H | 6/4 | 37 | 1.7268 | 1.2310 | **0.7297** | no |

**ALL4 (the record's own four ladders, the HEADLINE): the bar CANNOT BIND — 42 of 42 cells
survive and CH_MATCHED differs from CH_RAW at 0 of 42.** The reason is structural and was
predicted by the record itself: GROSS is simultaneously the LONGEST ladder (10 rungs) and the
one whose Sharpe spread is degenerate (idea 1189, reproduced by 1206 at 0 of 1,888 widest-
calls), so it is always the narrowest and the bar lands below 1.

**NG (no GROSS) is a POST-HOC control, labelled as one, added AFTER the ALL4 leg showed the bar
cannot bind. No verdict in this run rests on it.** There the bar binds: survives at 38 of 42
(0.9048), median multiple 3.8846 against a median bar 2.2461, and **CH_MATCHED differs from
CH_RAW at 4 of 42 cells.**

Mean OOS Sharpe over 42 picks per chooser, paired against that ladder set's own CH_RAW, SE
clustered on the FOLD (folds tile the tape without overlap, so fold means are the independent
units; panels inside a fold are not):

| chooser | mean OOS Sharpe | delta vs CH_RAW | SE | t |
|---|---|---|---|---|
| CH_RAW/ALL4 | 0.9677 | +0.0000 | — | — |
| CH_MATCHED/ALL4 | 0.9677 | +0.0000 | 0.0000 | +0.00 |
| CH_D2/ALL4 | 0.9959 | +0.0281 | 0.0494 | +0.57 |
| CH_ANCHOR/ALL4 | **1.0362** | +0.0685 | 0.0514 | +1.33 |
| CH_MATCHED/NG | 0.9514 | **−0.0163** | 0.0237 | −0.69 |
| CH_D2/NG | 0.9959 | +0.0281 | 0.0494 | +0.57 |
| CH_ANCHOR/NG | 1.0362 | +0.0685 | 0.0514 | +1.33 |

**NO DELTA CLEARS 2 SE AND THE LARGEST |t| IN THE RUN IS 1.33.** Changing the verdict is worth
−0.0163 of OOS Sharpe at t −0.69 — indistinguishable from zero on 42 picks. Doing nothing is
ahead of every chooser again (1155/1206's finding, reproduced from a third direction by a run
not looking for it), and again not resolvably so.

**BENCHMARKS** (10 bps, t+1, post warm-up): U56 SPY 15.06% / 0.8815 / −33.72% (halves
0.9600/0.8171), OOS 15.15% / 0.8686; U56 RULES v2 (live) 8.60% / 1.1982 / −12.05% (halves
1.2332/1.1705), OOS 9.42% / 1.2717. B136 SPY 15.16% / 0.8862 / −33.72%, OOS 15.33% / 0.8769;
B136 LIVE 7.98% / 1.0994 / −12.24%, OOS 1.1061. SMALL SPY 14.06% / 0.8582 / −33.72%, OOS
0.8769; SMALL LIVE 4.64% / 0.7130 / −12.18%, OOS 0.6518.

**BOTH KEEP PATHS.** 66 rung books: **4a 0 of 66; 4b full 17; 4b OOS 16; BOTH 15** (U56 10/22,
B136 5/22, **SMALL 0/22 on every path**). 24 rule-8 picks: **4a 0; 4b full 2; 4b OOS 2; BOTH
2.** 24 stitched deployable curves: **4a 0; 4b full 2; 4b OOS 2; BOTH 2.** Both passers are the
SAME object — **U56 CH_ANCHOR, 16.89% / 1.2199 / −19.13%, halves 1.2635/1.2043, OOS 17.16% /
1.1759** — i.e. the do-nothing control sitting on the record's standing anchor book
(U56 N=20 / H=126 / g=0.75 / W). **CONFIRMATORY, NOT GENERATIVE. RECORDED, NOT PROMOTED, NO
MEMO, NOTHING ENACTED.**

## Gates — 15 of 15 pass

G0 MC d2 == published Hartley constants **2.38e-03**; **G1 1155's census replayed BIT FOR BIT
at its own corpus (54 of 90, 0.6000, median inflation 1.8999, 32,930 units, 1,137 files)**;
G2 claim sets nest, 0 violations; **G3 the substitution convention proved to be one threshold
at I on the actual 100 units — 0 mismatches**; G4 fast runner == `engine.backtest` on the
decision-time frame **2.78e-17**; **G5 the GROSS ladder is provably the anchor frame SCALED,
0.000e+00**; G6 live RULES v2 U56 MaxDD **−12.0549%** against the record's −12.05%; G7 folds
tile all three panels with no overlap and no gap; G8 CH_ANCHOR move rate exactly 0; **G9 every
in-domain unit carries a hand read, 0 unaudited**; G10 the domain split partitions the
checkable set exactly; G11 the census is deterministic across two runs, 0 differences;
G12 each stitched curve's length == the sum of its folds'.

## Recommendation, proposed not enacted (rule 6)

**A committed re-read that corrects a statistic for its own COUNT must state the DOMAIN of the
correction and report the units outside it SEPARATELY — never as failures.** On this corpus
that restates 78 of 96 of 1155's own checkable units, and it would have stopped a headline of
"two in five committed spread multiples are not effects" standing in the record when the
traceable number is **zero**. A secondary clause follows from Arm B: **a count-matching bar
whose value falls BELOW 1 is not a correction, it is a handicap on the SHORTER ladder**, and it
does so at 0.5317 of this record's realised ladder pairs.

## Survivorship (rule 9)

U56 and B136 are CURRENT-CONSTITUENT lists; SMALL is the current output of a sub-$2B screen
less the documented `max_1d_move >= 1.0` exclusion (51 of 715 dropped, 664 investable names
plus SPY as benchmark only). Every CAGR and drawdown LEVEL is optimistic and the 4b counts are
an UPPER bound. The census and trace arms are a scan of committed text and carry no market bias
at all; the chooser deltas rank one construction against itself on one tape and the bias very
largely cancels out of the DELTAS, but it does NOT cancel out of the rule-8 OOS levels.

## KILL as a capital finding

Script `research/backtests/2026-09-17_how-many-committed-RANGE-claims-quote-a-MULTIPLE-BELOW-THEIR-OWN-COUNT-INFLATION_C.py`,
8 CSVs, console log, this result note, 4 LEADERBOARD rows. Runtime 55s, offline, deterministic.
Follow-ups filed 1213, 1214, 1215.
