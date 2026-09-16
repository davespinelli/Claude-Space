# Idea 1104 (lane C, 2026-09-16) — does the FAR-SIDE COLLAPSE survive a PANEL it was not found on?

**ANSWERED = NO. THE FAR-SIDE COLLAPSE IS A LARGE-CAP FACT, NOT A BREADTH FACT — and the reason
is worse than "smaller": on the SMALL panel there is no positive EDGE anywhere on the ladder to
collapse from.** On U56 this run reproduces 1098 exactly (floor@90 **3.25 pp**, peak n=12 by
**0.61 pp**, collapse EDGE(12)−EDGE(40) = **+6.41 pp**, sign agreement **0.999**). On the
663-name SMALL_F10 panel (`max_1d_move >= 1.0` dropped, 52 names, per the idea's own
instruction) the same nine-rung ladder gives a collapse of **+1.96 pp** at sign agreement
**0.892 — below the 0.90 bar as a bare pair — and the panel's own 90% resolution floor is
INFINITE: 0 of 36 rung pairs resolve, so the floor exceeds the ladder's entire span (max |dEDGE|
5.39 pp).** Nothing on the small-cap EDGE ladder is publishable, the collapse included.
**KILL of the breadth reading; CONFIRM of 1098's U56 numbers at 4.8e-3; CONFIRM that 1098's
other half (the peak is not resolved) travels — it is worse on SMALL, P(argmax==full) 0.224 with
a 7-rung 90% set.** No RULES change, no PROTOCOL edit, no book proposed as capital; RULES.md,
PROTOCOL.md, scan.py, bot.py and baseline.py untouched.

SELECTION: lane C takes the SECOND open line in QUEUE.md. That is 1104; it names no EDGAR / Form
4 / 8-K / options / live-data object, so it is eligible.

## THE TWO DIALS AND NO MORE (PROTOCOL rule 4)

**n {5,8,10,12,15,20,25,30,40} (1082's ladder verbatim) x PANEL {U56, U56_2010, SMALL_F10,
SMALL_RAW} = 36 cells, ALL published.** Frozen at 1082/1098's construction: CAND20 legs, cap INF,
max_vol 0.60, gross 0.75, W, min hold 126, 10 bps, LAG 1, warm-up 260, IS end 2016-12-31, **seeds
40** (1098's headline count — the seed dial is not re-opened), 1,000 circular-block draws.
**BLOCK LENGTH is not a dial** (headline L=63, L in {21,126} reported beside it). **TAPE is not a
dial either**: the small panel begins 2010-01-04 and U56 begins 2008-01-02, so `U56_2010` — U56
clipped to the small panel's own span — is reported as a labelled control and never selected on.

EDGE(n) = 100 x (CAGR_book(n) − median of 40 DD-matched nulls), 1082's REBUILT convention (each
null re-run at the gross lam*0.75 equalising its realised |MaxDD| with the book's, 34-step
bisection); the bootstrap applies ONE block index JOINTLY to the book, all 40 nulls and every
rung. **LIMITATION INHERITED AND DECLARED: lam is matched once on the real tape and held fixed
inside the bootstrap, so every width is a LOWER bound** — which is the conservative direction for
this run's conclusion ("not resolved on SMALL"). SPY is a benchmark column on the small panel,
**never a constituent**: it is excluded from the investable set and from the RULES v2 baseline run
on both small panels (gate G_SPY).

## THE NINE-RUNG EDGE LADDER ON EVERY PANEL (pp of CAGR, S=40)

| panel | 5 | 8 | 10 | 12 | 15 | 20 | 25 | 30 | 40 |
|---|---|---|---|---|---|---|---|---|---|
| U56 | +5.95 | +5.35 | +6.21 | **+6.82** | +5.22 | +5.12 | +2.95 | +1.55 | +0.41 |
| U56_2010 | +6.51 | **+6.63** | +4.92 | +5.75 | +3.74 | +4.59 | +3.48 | +3.58 | +0.42 |
| SMALL_F10 | −5.32 | −0.85 | −0.66 | −0.45 | −0.40 | **+0.07** | −0.92 | −1.55 | −1.89 |
| SMALL_RAW | −5.90 | −8.11 | −5.03 | −3.08 | −0.57 | −2.24 | **−0.25** | −1.29 | −2.72 |

**The decisive row is not the collapse, it is the sign.** On U56 the book beats its DD-matched
null at **100% of 40 seeds at the median rung (min 92.5%)**; on SMALL_F10 it beats **35% at the
median rung and never more than 50%**, on SMALL_RAW **12.5%**. The small-cap momentum book is at
or below a random 20-name draw matched on drawdown, at every rung. 1098's shape has no small-cap
counterpart to have a far side.

## THE FLOOR AND THE FAR SIDE (headline L=63, 1,000 draws)

| panel | floor@90 | floor@95 | peak | peak − runner-up | collapse EDGE(peak)−EDGE(40) | collapse sign agree | collapse / boot sd | pairs resolved@90 | P(argmax==full) | 90% argmax set |
|---|---|---|---|---|---|---|---|---|---|---|
| U56 | **3.25** | 4.66 | 12 | +0.61 (BELOW) | **+6.41 (ABOVE)** | 0.999 | 3.63 | 21/36 | 0.378 | {5,8,10,12} |
| U56_2010 | 3.06 | 3.15 | 8 | +0.12 (BELOW) | **+6.21 (ABOVE)** | 0.997 | 2.50 | 15/36 | 0.344 | {5,8,10,12} |
| **SMALL_F10** | **inf** | inf | 20 | +0.47 (BELOW) | **+1.96 (BELOW)** | **0.892** | 1.34 | **0/36** | 0.224 | {5,8,10,12,15,20,25} |
| SMALL_RAW | 4.77 | 5.87 | 25 | +0.31 (BELOW) | +2.47 (BELOW) | 0.980 | 1.82 | 16/36 | 0.613 | {15,20,25} |

**IT IS NOT MERELY A POWER LOSS, AND IT IS NOT TAPE LENGTH.** The collapse's point estimate falls
**3.27x** (6.41 → 1.96 pp) while the bootstrap's median pair sd rises only **1.25x** (1.72 → 2.15
pp); in sd units the collapse goes from **3.63** to **1.34**. And `U56_2010` — the same 15.63-year
tape, the same warm-up, the same 5.96/9.67-year IS/OOS split — keeps a fully resolved collapse
(+6.21 pp at 0.997, above its own 3.06 floor). What changes is the pool, not the calendar.

**THE STEP FILTER IS A BIGGER LEVER ON THIS LADDER THAN THE COLLAPSE IS.** Dropping the 52 names
with `max_1d_move >= 1.0` moves the argmax 25 → 20, P(argmax==full) 0.613 → 0.224, the floor
4.77 pp → infinite, and rung-level EDGE by −0.66 to +7.26 pp (median +0.83). Neither reading supports the
breadth hypothesis — the collapse is below the floor on both small panels — but any future
SMALL-panel ladder claim in the record must stamp which filter it used, because the filter and
the effect are the same size here.

Block length barely moves any of it (collapse sign agreement 1.000/0.999/1.000 on U56 and
0.900/0.892/0.889 on SMALL_F10 at L = 21/63/126), so the SMALL failure is not a resampling-scale
artefact.

## HYPOTHESES (declared before any number): 5 of 6 SUPPORTED

| hypothesis | declared | observed | verdict |
|---|---|---|---|
| H_COLLAPSE_SIGN (SMALL_F10) EDGE(peak)−EDGE(40) > 0 | >0 | +1.96 pp | PASS |
| **H_COLLAPSE_RESOLVED (SMALL_F10) above the panel's own floor => BREADTH fact** | above | +1.96 vs floor **inf**, agreement 0.892 | **FAIL — the run's answer** |
| H_PEAK_UNRESOLVED (SMALL_F10) peak−runner-up below the floor | below | +0.47 vs inf | PASS |
| H_STEPS collapse sign unchanged on SMALL_RAW | same | +1.96 vs +2.47 pp | PASS |
| H_TAPE U56_2010 collapse still resolved | above floor | +6.21 vs 3.06 pp | PASS |
| H_FLOOR_SCALES SMALL_F10 floor higher than U56's | higher | inf vs 3.25 pp | PASS |

## GATES: 11 of 11 PASS (printed before any result number)

G1 fast runner == `engine.backtest` 1.39e-17 (U56) and 2.08e-17 (SMALL_F10); G1b
`gross_rescaler(1.0)` == `nrun` 1.39e-17 both; G2 936/1071/1082/1098's committed U56 W/H126 N=20
triple 3.18e-07; G3 SPY OOS triple 1.70e-04; G5 live RULES v2 MaxDD −12.05% at 4.95e-05; G7
determinism of the seed recipe 0.00e+00; **G_XRUN reproduces all nine of 1082/1098's committed
U56 EDGE figures at 4.80e-03 (1082 publishes them to 2dp, so this is the rounding limit)**;
G_FILT the filter drops exactly the 52 names `small_meta.csv` flags; G_SPY SPY is investable on
0 bars of the small panel.

## RULE 8 WALK-FORWARD AND BOTH KEEP PATHS (PROTOCOL rules 4 and 8)

Four IS-only choosers (C_ISSHARPE, C_ISDD, C_ISCAGR, C_ISEDGE) pick n on the IS window alone, per
panel; OOS untouched until scored. **16 picks: 4b full 2, 4b OOS 2, 4a 0 — and both passes are on
`U56_2010`, the control panel, at n=30.** Whole ladders: U56 4b 2/9, 4b-OOS 2/9, 4a 0/9;
U56_2010 3/9, 3/9, 0/9; **SMALL_F10 0/9, 0/9, 0/9; SMALL_RAW 0/9, 0/9, 0/9.**

| panel | chooser | pick | OOS CAGR / Sharpe / MaxDD | full CAGR / Sharpe / MaxDD | halves | 4b / 4b-OOS / 4a | regret |
|---|---|---|---|---|---|---|---|
| U56 | C_ISSHARPE, C_ISDD | 40 | 14.00% / 1.0983 / −22.98% | 13.46% / 1.1268 / −22.98% | 1.272/1.025 | F/F/F | +0.0922 |
| U56 | C_ISCAGR, C_ISEDGE | 5 | 17.06% / 0.9003 / −25.85% | 17.83% / 0.9860 / −25.85% | 1.197/0.827 | F/F/F | +0.2903 |
| U56_2010 | C_ISSHARPE, C_ISDD | 30 | 14.28% / 1.0791 / −18.28% | 13.01% / 1.0648 / −18.28% | 1.144/1.023 | **T/T**/F | +0.0613 |
| U56_2010 | C_ISCAGR, C_ISEDGE | 5 | 19.87% / 0.9998 / −22.89% | 17.46% / 0.9493 / −27.41% | 0.990/0.929 | F/F/F | +0.1407 |
| SMALL_F10 | C_ISSHARPE, C_ISCAGR, C_ISEDGE | 25 | 6.17% / 0.4164 / −35.59% | 8.06% / 0.5285 / −35.59% | 0.779/0.344 | F/F/F | +0.0891 |
| SMALL_F10 | C_ISDD | 40 | 6.13% / 0.4281 / −36.12% | 7.32% / 0.5094 / −36.12% | 0.713/0.365 | F/F/F | +0.0774 |
| SMALL_RAW | C_ISSHARPE, C_ISCAGR, C_ISEDGE | 25 | 9.57% / 0.5528 / −35.46% | 10.17% / 0.6113 / −35.46% | 0.887/0.376 | F/F/F | +0.0000 |
| SMALL_RAW | C_ISDD | 40 | 7.73% / 0.5014 / −36.06% | 8.13% / 0.5445 / −36.06% | 0.802/0.343 | F/F/F | +0.0514 |

Benchmarks: SPY full 15.10% / 0.8829 / −33.72% and OOS 15.21% / 0.8711 / −33.72% on U56, 14.06% /
0.8581 / −33.72% full and 15.33% / 0.8767 / −33.72% OOS on the small tape; live RULES v2 U56
8.62% / 1.2007 / −12.05% full and 9.45% / 1.2762 / −12.05% OOS, and on SMALL_F10 4.30% / 0.6629 /
−13.89% full and 3.75% / 0.5590 / −13.89% OOS. **Every SMALL rung fails all five 4b legs** — the
best full-sample CAGR rung on SMALL_F10 (n=12) runs 8.90% at Sharpe 0.525 with a −41.2% drawdown, and the
best-Sharpe rung (n=25) 8.06% / 0.529 / −35.6%, against
SPY's 14.06% / 0.858 / −33.72%, i.e. it loses on return, on risk and on both halves at once.
**NOTHING IS PROPOSED AS CAPITAL.**

## SURVIVORSHIP (PROTOCOL rule 9)

Every panel here is a CURRENT-CONSTITUENT list and the SMALL panel is the worst of them:
`data/SMALL_PANEL_README.md` warns it holds only names still listed, still public and still under
$2B **today**, so returns are biased upward and the bias grows with lookback. Book and null are
drawn from the SAME pool over the SAME tape, so the bias very largely cancels out of EDGE, out of
the argmax and out of the floor — the quantities this run's answer rests on. It does NOT cancel
out of the 4b legs, which are measured against SPY: every 4b figure on a SMALL panel above is
flattered and still fails, which only strengthens the KILL.

## WHAT THE RECORD SHOULD TAKE FROM THIS

1. **1098's "the floor kills the peak's location, not the shape's far side" is a U56/B136
   sentence.** Off the large-cap panels the far side is not resolved either, and the shape it is
   the far side of does not exist. Any future citation of the 6.41 / 6.47 pp collapse must carry
   the panel.
2. **An infinite floor is a reportable outcome, not a missing number.** SMALL_F10 resolves 0 of
   36 pairs at 90%; reporting its argmax (n=20) or its collapse as a figure would be publishing
   noise with two decimals.
3. **SMALL-panel claims need a `max_1d_move` filter stamp**, for the same reason 1074 wants
   `SMALL439` renamed: the filter moves this ladder by more than the effect being measured.

Files: `2026-09-16_does-the-FAR-SIDE-COLLAPSE-survive-a-PANEL-it-was-not-found-on_C.py` and its
`.console.txt`, `.edge.csv`, `.ladder.csv`, `.argmax.csv`, `.pairs.csv`, `.floor.csv`,
`.picks.csv`, `.grid.csv`, `.gates.csv`, `.hypotheses.csv`, `.benchmarks.csv`.
