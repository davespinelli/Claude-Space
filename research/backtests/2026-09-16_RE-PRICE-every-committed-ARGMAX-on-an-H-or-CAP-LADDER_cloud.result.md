# Idea 1107 (cloud lane, 2026-09-16) — RE-PRICE every committed ARGMAX on an H or CAP LADDER

**ANSWERED = NONE. NOT ONE of the record's 26 committed H-axis or cap-axis EDGE argmaxes
survives both tests.** On the headline TAPE basis the answer is **0 of 26** CORE ladders and
**0.0 of 33** harvested prose claims; on the JOINT basis also **0 of 26**; on the record's **own**
bar — the seed SE of the null median, the bar 1082 / 1085 / 1097 argued their headlines against —
**9 of 26** survive. The two tests are **not** equally hard: **floor-only failures 14, gate-only
failures 0**, so the null gate never kills an argmax the floor would have spared. **The maximum
gap-to-floor ratio over all 26 ladders is exactly 1.000** — no committed argmax on either axis
clears its own floor even once, and **18 of 26 ladders have a WHOLE-LADDER floor**: no rung pair
anywhere on them is sign-resolved at q=0.90. This is a **KILL of the published H-axis and
cap-axis argmax as a claim**, and a **CORRECTION to the record's decisiveness bar**: the seed SE
prices only the *null's* sampling error and ignores the *tape's*, and the two answers differ on
**9 of 26** ladders. No RULES change, no book promoted, no PROTOCOL edit (rule 6); RULES.md,
PROTOCOL.md, scan.py, bot.py and baseline.py untouched.

## THE DIALS AND NO MORE (PROTOCOL rule 4)
CLAIM SET {CORE, WIDE} x FLOOR BASIS {SEED, TAPE, JOINT} = **6 cells, all published**. CORE = the
26 committed EDGE ladders this run rebuilds exactly — 1086's **18 H ladders** (2 panels x 9 N,
rungs H in {21, 63, 126}) and 1071's **8 cap ladders** (2 panels x 4 N, rungs cap in {1.00, 1.25,
1.50, 2.00, INF}). WIDE = the **33** VALUED H-or-cap argmax claims harvested from 1,009 corpus
files. **The cell coordinates are not dials** — (panel, N, H, cap, seeds, DD-match convention) are
taken exactly as committed. BLOCK LENGTH is not a dial: headline L=63, L in {21, 126} reported
beside it and reading **0 of 26 at all three**.

## GATES 11 of 11, printed before any result number
G1 fast runner == `engine.backtest` 1.39e-17; **G1b `gross_rescaler(1.0)` == `nrun` 1.39e-17**
(the bisection kernel is the same book, not an approximation of it); **G1c the CAPPED build ==
`engine.backtest` 1.39e-17** (1071's arm); G2 CROSS-RUN 936/1071/1082/1097's committed
W/H126/N=20 triple 3.18e-07; G3 SPY OOS triple 1.70e-04 (U56) / 4.05e-05 (B136); G4 live RULES v2
MaxDD == committed 4.95e-05 / 9.85e-06; **G5 CROSS-RUN reproduces ALL 94 of 1097's committed
EDGE_OPEN and EDGE_ELIG figures at 1.78e-15**; G6 its committed book CAGRs at 8.33e-17; **G7
CROSS-RUN reproduces 1097's committed argmax_OPEN and argmax_ELIG on all 26 H/cap ladders,
26 of 26, exactly.** The gate work is the point: every number below is measured on a tree that
first reproduced the record's own.

## TEST 1 — THE NULL GATE (1097's, reproduced)
argmax UNCHANGED between the OPEN and the rank-matched ELIG null in **14 of 26**; **MOVED in 12**
— **7 of 18** on the H axis, **5 of 8** on the cap axis. This reproduces 1097's committed counts
exactly and is the control, not a new measurement.

## TEST 2 — THE FLOOR, on three bases
| basis | what it prices | floor survives | CORE survive BOTH | WIDE (33 claims) |
|---|---|---|---|---|
| SEED | the null median's seed SE, `K=2 * sqrt(SE_i^2 + SE_j^2)` — the record's own bar | 12 of 26 (H 11/18, cap 1/8) | **9 of 26** (0.346) | 16.5 of 33 (0.500) |
| **TAPE** (headline) | 1098/1102/1108's block-bootstrap sign-resolution floor at q=0.90 | **0 of 26** | **0 of 26** (0.000) | **0.0 of 33** |
| JOINT | the two in quadrature | **0 of 26** | **0 of 26** (0.000) | **0.0 of 33** |

Median TAPE floor **1.1493 pp** against a median committed gap of **0.6758 pp**; median
gap/floor ratio **0.614**, **maximum 1.000**. Of the 134 rung pairs across all 26 ladders, only
**46 are sign-resolved** at q=0.90 (median agreement **0.833**, below the bar), and **18 of 26
ladders resolve NOTHING** — their floor is the whole ladder spread.

**H_SHORT PASSES and is the cleanest statement of why:** a 3-rung H ladder gives 3 pairs and
**0 of 18** of them clear their floor. The 5-rung cap ladders are the fairer test and read **0 of
8** as well, so this is not only a rung-count artefact.

## H_BASIS FAILS, AND THAT IS THE CORRECTION
The three bases agree on the survival verdict for only **0.654** of the 26 ladders. "Survives its
floor" is therefore a **basis statement**, not a tape statement — and the disagreement is not
symmetric. The SEED basis is the record's own and lets **9** argmaxes through (U56 H at N = 8, 20,
25, 40 and B136 H at N = 5, 8, 15, 25, 30); the TAPE basis lets **none**. The reason is
structural: the seed SE prices how much the *null median* would move if the rank draws were
redrawn, and prices **nothing at all** about how much the *book* and the *null together* would
move if the tape were redrawn. Every committed decisiveness call on these two axes was made with
the second term missing.

## THE DECLARED APPROXIMATION, AND ITS DIRECTION
Inside the bootstrap the DD-match multiplier lambda is held at its full-sample value (re-solving
it per draw would cost 26 x 1000 x k x m bisections and was not run); the resampled null CAGR is
then exact from block log-sums of the lambda-scaled series. **Declared in advance: this REMOVES a
source of draw-to-draw variation, so the TAPE floor published here is a LOWER bound and every
survival count above is an UPPER bound.** The bias runs *toward* survival and nothing survives
anyway.

## RULE 8 AND BOTH KEEP PATHS — NOTHING PROPOSED
EDGE is not a KEEP path and dial 2 cannot move one: the **book at every cell is byte-identical
across the two gates**, only the comparand changes, so 4a and 4b are invariant to it by
construction. Scored anyway because rule 4 requires it. Rung chosen on IS 2009-2016 **alone**, per
ladder, three choosers, OOS read once: **16 of 78 picks clear 4b full AND OOS; 0 of 78 clear 4a.**
Whole grid, 94 committed cells: **4b full 18, 4b OOS 19, 4a 0.** The passing picks are cells the
record already holds and has already PARKED — U56 H=21 at N = 10/12/15/30/40, U56 H=126 N=20 (the
standing anchor, full **15.58% / 1.1397 / -19.13%**, halves 1.2037/1.0971, OOS **16.97% / 1.1643
/ -19.13%**), the U56 cap ladder at N=20, and B136's cap ladder at N = 20/25. Benchmarks: U56 SPY
full 15.10% / 0.8829 / -33.72% (halves 0.9588/0.8207), OOS 15.21% / 0.8711 / -33.72%; U56 RULES v2
live 8.62% / 1.2007 / -12.05%, OOS 9.45% / 1.2762 / -12.05%; B136 SPY OOS 15.33% / 0.8767 /
-33.72%; B136 RULES v2 OOS 7.88% / 1.1059 / -12.24%. **Nothing new, nothing promoted, no memo
written.**

## A LIMIT OF THE WIDE ARM, STATED
All **33** harvested claims sit on the **H** axis; the harvester found **zero** prose argmax
claims naming a cap value inside its window, against **3,691** rejects. The record argues the cap
axis in CSVs and in prose that never puts a cap value next to the claim word, so the WIDE arm
cannot reach it and the cap verdict above rests entirely on the 8 rebuilt CORE ladders. Every
reject is published with its reason and context.

## SURVIVORSHIP (PROTOCOL rule 9)
U56 and B136 are CURRENT-CONSTITUENT panels. EDGE, the gate and the floor are all within-pool
contrasts over the same inflated tape and the bias very largely cancels out of them; it does
**not** cancel out of the 4b legs, measured against SPY, a real index, so the 18 full-sample 4b
passes are an UPPER bound.

Script `research/backtests/2026-09-16_RE-PRICE-every-committed-ARGMAX-on-an-H-or-CAP-LADDER_cloud.py`,
11 CSVs, 4 LEADERBOARD rows.
