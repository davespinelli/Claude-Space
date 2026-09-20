# Idea 2026 (lane C, 2026-09-20) — CAN THE DRIFT THRESHOLD BE SET WITHOUT THE IS WINDOW?

**Verdict: ANSWERED — YES, and the answer carries a KEEP-4b candidate that spends ZERO in-sample
statistics.** Script `2026-09-20_ladder-free-drift-threshold_C.py`, gates **9/9**, 7,360 scored
rows (1,840 cells x 4 cost rungs) published in `.grid.csv.gz`.

## What was asked

Idea 1799's KEEP-4b candidate re-reads the exposure scalar `g_t = clip(t / sigma20_panel, 0, 1)`
only when the book's held gross has drifted from it by more than a CONSTANT `h`. Its own memo
point 7 conceded the weakness: the legal IS-only chooser walks to the LAZIEST rung of whatever `h`
ladder it is given (18 of 24 picks on the top two rungs), so the reach is ladder-length fragile.
Idea 2026 asks whether the threshold can be set with no IS statistic at all, by three LADDER-FREE
constructions: `h_t = k * SD_20(g_t)` (SDMULT), `h_t = f * g_t` (FRACG), and a two-sided
asymmetric version, tight DOWN / loose UP at a pre-stated 4:1 ratio (ASYMG). ASYMH (the incumbent
constant made asymmetric) isolates the asymmetry at a fixed base. The whole calendar ladder
`R in {D,W,M,Q}` and the incumbent FIXH ladder are the comparands.

**PRE-STATED before the run** (in the script docstring, never adjusted): `k* = 1.0`, `f* = 0.10`,
ASYMH `h* = 0.12`, ratio 4:1, and `t* = 0.16` inherited from the standing VOLTGT memo. Two tuned
dials within any one family (TARGET x the family's own scale rung); no chooser crosses families,
panels, trade cadence or cost. Both KEEP paths scored at every cell; rule 8 read once.

## Headline

**V1 TRIGGERED.** At `t*` and 10 bps, over the 6 arms (panel x trade cadence), the pre-stated
ladder-free constants clear 4b FULL *and* OOS on **FRACG 4 / ASYMG 4 / SDMULT 3 of 6 arms with no
IS statistic spent**, against the incumbent FIXH family's best legal IS-only chooser at **3 of 6**
(C_ISSHARPE; mean over the four choosers 1.75). Every pass is U56 or B136; SMALL665 clears
**0 of 6**, on four legs at once (fifth confirmation of the VOLTGT memo's A2).

**The fix is the PRE-STATED CONSTANT, not the ladder shape (V3).** Truncating a family's ladder to
its first four rungs moves the IS chooser's pick on 15-24 of 24 (arm x chooser) pairs in EVERY
family — ladder-free families included. What the ladder-free families buy is verdict stability:
the OOS 4b verdict moves on **0 of 24** for SDMULT / ASYMG / ASYMH against **5 of 24** for FIXH and
3 of 24 for FRACG. A pre-stated constant reads no ladder at all and is immune by construction.

**The strongest new fact (V5).** Idea 2022's committed caveat — that 1799's "drift beats a
turnover-matched calendar" is a 24-day 2020 episode — replicates exactly here and is **specific to
the CONSTANT threshold**. Mean OOS-Sharpe edge over each arm's own turnover-matched calendar point,
full tape -> 2020-crash-excised tape (2020-02-19..2020-03-23), pre-stated cells:

| family | full tape | crash-excised | arms positive after excision |
|---|---|---|---|
| FIXH `h=0.12` (incumbent) | **+0.0798** | **-0.0050** | 0 of 4 |
| FRACG `f=0.10` | +0.0648 | **+0.0377** | 4 of 4 |
| SDMULT `k=1.0` | +0.0142 | **+0.0320** | 3 of 3 |
| ASYMH `h=0.12` | +0.0424 | +0.0168 | 3 of 4 |
| ASYMG `f=0.10` | +0.0269 | +0.0109 | 2 of 4 |

Scaling the threshold to the scalar in force converts an episode-driven edge into one that
survives deleting the episode. (Both tapes' 4b OOS verdicts still shift on the excised tape, but
that is the SPY BAR SHIFT idea 2022 named in its point 9 — SPY OOS MaxDD -33.72% -> -24.50% — not
a book failure: the FRACG book's own OOS MaxDD is -19.12% on both tapes.)

**V4 TRIGGERED (asymmetry pays, cheaply).** At a matched base, the 4:1 tight-down/loose-up trigger
clears 4b on more cells than its symmetric twin (ASYMH 144 vs FIXH 136 of 270; ASYMG 103 vs FRACG
92 of 210), wins OOS MaxDD by +1.01 / +0.61 pp, cuts gross deeper through the crash, and pays
-0.33 / -0.16 pp of OOS CAGR and +0.26 / +0.23 turns/yr. Mean OOS Sharpe is a wash (+0.0008 /
+0.0077). Path 4a also improves (41 vs 30, 34 vs 22) but never passes at a pre-stated cell.

**V2 SPLIT — the "scale-free" story is HALF WRONG and is killed for the fraction rules.** Across
the 15 (panel x target) cells, only SDMULT's realised refresh rate is more stable than fixed
`h = 0.12`'s (CV 0.28 / 0.30 vs 0.45 / 0.46). FRACG and ASYMG are **worse** (0.51). Their virtue is
not an invariant cadence; it is pass-robustness and episode-independence. Reported as a KILL of the
invariance claim, not smoothed over.

**Ladder robustness at `t*`, 4 large-panel arms, 10 bps** (4b FULL+OOS, cell counts):
ASYMH 36/36, ASYMG 27/28, FIXH 32/36, FRACG 24/28, CAL 8/16 (`D` and `W` only; `M`/`Q` 0 of 8),
SDMULT 11/28 (it dies above `k = 1`). Along the TARGET ladder at each pre-stated rung, FRACG and
ASYMG hold 4/4 arms at `t in {0.10, 0.12, 0.16}` (ASYMG also at 0.20); SDMULT holds only to 0.12.

## The KEEP-4b candidate

`FRACG f = 0.10`, `t = 0.16`, monthly re-spread, U56, 10 bps, t+1:
**full 15.81% / 1.2470 / -19.12%, halves 1.2937 / 1.2055; OOS 16.55% / 1.2928 / -19.12%**, 1.42
turns/yr, ~10 refreshes/yr. vs SPY 15.12% / 0.8843 / -33.72% (OOS 15.26% / 0.8737 / -33.72%) and
live RULES v2 8.62% / 1.2010 / -12.05% (OOS 9.46% / 1.2766). Four 4b legs clear with margins
H1 +0.337, H2 +0.381, OOS +0.419, DD +1.11 pp, CAGR +5.23 pp. It clears **0 / 10 / 25 / 50 bps**
and repeats on B136 (16.03% / 1.2364 / -17.00%; OOS 16.10% / 1.2621 / -17.00%) and on the weekly
arm of both panels (U56 W fails 4b at 50 bps only, on the DD leg by 0.28 pp).

**Path 4a: KILL** at every pre-stated cell on every panel (0 of 6 arms for all five families) — its
drawdown is deeper than the live book's -12.05%, exactly as PROTOCOL 4b anticipates.

## Caveats, stated

1. **Survivorship.** U56 / B136 are CURRENT-constituent lists; SMALL665 is a current sub-$2B
   screen (54 tickers with `max_1d_move >= 1.0` dropped first). Every level is optimistic; the
   threshold-rule CONTRAST is same-tape / same-names and first-order immune, the PASS COUNTS
   are not.
2. **No standard errors.** This run publishes point estimates. Idea 2042 owns the 4b-leg SE
   question and idea 2022 has already shown that the drift-vs-calendar sweep is resolvable at only
   61 of 263 cells. The +0.0377 crash-excised edge above is a point estimate on 4 arms.
3. `t* = 0.16` is INHERITED, not chosen here; the run is zero-IS given that inheritance, not zero-
   parameter. The `t` ladder is published in full so the inheritance can be audited.
4. The sigma convention is FIXED at (L=20, d=0); idea 1771 owns that surface and this run does not
   re-price it.
5. SMALL665 clears nothing anywhere: 0 of its 460 cells (1,840 scored rows) on path 4b and on path 4a alike.

## Gates (9/9)

G0 18.7y; G1 calendar diagonal == `engine.backtest` 0.000e+00; G2 cost identity 0.000e+00;
G3 standing VOLTGT memo 4.605e-05; G4 every zero rung (FIXH h=0, SDMULT k=0, FRACG f=0) == CAL R=D
at 0.000e+00 on 90 of 90 cells; G5 idea 1799's KEEP cell reproduced to 4.042e-07; G6 gross never
levered (max 1.000000); G7 the ladder-free thresholds move refresh frequency 0.5..168.9/yr;
G8 the 4:1 trigger refreshes at least as often as its symmetric twin on 1080 of 1080 pairs.

Artifacts: `.grid.csv.gz` (all 7,360 rows), `.prestated.csv`, `.choosers.csv`, `.fragility.csv`,
`.invariance.csv`, `.asymmetry.csv`, `.crash.csv`, `.census.csv`, `.gates.csv`, `.log.txt`.
