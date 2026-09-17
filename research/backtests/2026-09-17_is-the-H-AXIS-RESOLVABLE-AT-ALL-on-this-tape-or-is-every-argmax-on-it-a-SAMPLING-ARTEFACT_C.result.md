# Idea 1181 (lane C, 2026-09-17) — is the H AXIS RESOLVABLE AT ALL on this tape, or is every argmax on it a SAMPLING ARTEFACT?

**ANSWERED = NO, IT IS NOT RESOLVABLE AT ANY ATTAINABLE RUNG COUNT — pre-declared outcome (B).**
Adding rungs was never going to fix 1174's disagreement, because the disagreement is not in the
ladder. It is in the tape.

Script `2026-09-17_is-the-H-AXIS-RESOLVABLE-AT-ALL-on-this-tape-or-is-every-argmax-on-it-a-SAMPLING-ARTEFACT_C.py`.
Two tuned dials — LADDER {L3, L5, L7, L10, L16} x BLOCK LENGTH {1, 5, 21, 63, 126} = **25 cells,
every one published**. Not dials, reported at every value: panel {U56, B136, SMALL} x N
{5,8,10,12,15,20,25,30,40} = 27 families, statistics {Sharpe (headline), CAGR}, the 4a/4b legs at
all 432 books, five rule-8 choosers. 2,000 paired circular-block draws per cell, seed 1181.
Ladders are STRICTLY NESTED over a FIXED range [21, 126], so rung count is never confounded with
range (G7/G7b).

## The headline: the argmax is informative but never resolved

Pre-declared, before any number: a family is RESOLVED when the modal bootstrap argmax share is
>= 0.50 AND the 90% argmax confidence set spans <= 21 days on the H axis. **LEG 2 is stated in
DAYS, not in rungs, precisely so a ladder cannot buy "stability" by deleting rungs.** A ladder
resolves the axis at >= 14 of 27 families.

| ladder | rungs | RESOLVED (block 63) | median modal share | uniform null 1/L | ratio | median 90% set span |
|---|---|---|---|---|---|---|
| L3  |  3 | **1/27** | 0.6315 | 0.3333 | 1.89x | 63 d |
| L5  |  5 | **0/27** | 0.5480 | 0.2000 | 2.74x | 84 d |
| L7  |  7 | **1/27** | 0.4720 | 0.1429 | 3.30x | 69 d |
| L10 | 10 | **2/27** | 0.4470 | 0.1000 | 4.47x | 74 d |
| L16 | 16 | **0/27** | 0.3825 | 0.0625 | 6.12x | 89 d |

**No rung count comes within a factor of seven of the bar.** The best cell in the entire 25-cell
dial grid is 2 of 27 (L10 at blocks 63 and 126); 18 of the 25 cells read 0 or 1 of 27. The block
length barely matters — going from IID (block 1) to a half-year block (126) moves the median L16
modal share from 0.3285 to 0.3790 and the median span from 100 to 84 days. The control statistic
CAGR is no better (best cell 5 of 27, on the 3-rung ladder).

The argmax is *not* uninformative: every family at every ladder sits above its uniform null
(27/27 at all five ladders, 6.12x it at L16). It is simply nowhere near precise enough to name a
rung. **The 90% argmax confidence set at L16 holds a median 7 of 16 rungs and spans 89 days of a
105-day axis — 85% of the whole axis.**

## 1174's finding, re-read with the interval attached

1174 reported the L3 and L16 point argmaxes disagree at 14 of 18 families and stopped there. With
an interval on it:

* the point argmax carries median probability **0.3825**; at 2 of 27 families it is under 0.20;
* the observed top-minus-second Sharpe gap has median **0.0247** against a paired bootstrap SE of
  **0.0955** — median **gap/SE 0.347**;
* **0 of 27 families have a top rung that beats the second by 2 SE.** Not one.

So 1174's 14-of-18 disagreement is exactly what two readings of an unresolved axis should look
like. It is not evidence that the finer ladder is better, and it was never evidence that the
coarse one is wrong.

## The detection floor — how big a real effect would have to be

CTRL_CORR is the falsification control: the family's own 16 books, affinely rescaled to a common
mean and sd so every rung has **exactly** the same full-sample Sharpe while the cross-rung
correlation (adjacent H rungs share most of their holdings) survives. CTRL_POWER lifts one rung by
delta and re-reads.

| delta (Sharpe) | 0.00 | 0.05 | 0.10 | 0.20 | 0.30 | 0.60 | 1.00 |
|---|---|---|---|---|---|---|---|
| CTRL_CORR resolved /27 | **0** | 0 | 3 | 12 | **22** | 27 | 27 |
| CTRL_INDEP resolved /27 | 0 | 0 | 0 | 0 | 0 | 3 | 21 |

**Detection floor delta\* = 0.30 Sharpe.** Against it:

* the real L16 ladder's median **best-minus-second** Sharpe gap is **0.0247** — **12x below the floor**;
* the real ladder's median **best-minus-worst** spread across all 16 rungs is **0.2025** — still
  below the floor, at a majority of families.

That is the answer in one line: **on this tape the entire end-to-end range of the H axis is
smaller than the smallest difference the tape can resolve.** Every published H argmax in the
record, this run's included, is a draw from a distribution that spans most of the axis.

CTRL_INDEP (same DGP, cross-rung correlation destroyed) needs ~1.00 Sharpe of separation for the
same verdict. The correlation between adjacent rungs is worth roughly 3x in the SE of the paired
difference (G12 median pairing gain 3.04x) and roughly 3x in the detection floor — which is why
this comparison must be made inside each draw, and why a run that resamples rungs independently
would understate resolution by a factor of three.

## Rule 8 walk-forward (PROTOCOL rule 8) — (N, H) on 2009–2016 only, 2017–2026 read ONCE

| chooser | mean OOS Sharpe | mean OOS CAGR | mean OOS MaxDD | beats SPY | 4b full | 4a |
|---|---|---|---|---|---|---|
| CH_L3_IS    | 0.8800 | 16.07% | -28.01% | 2/3 | **1** | 0 |
| CH_L16_IS   | 0.9323 | 18.79% | -30.02% | 1/3 | 0 | 0 |
| CH_BOOTMEAN | 0.9323 | 18.79% | -30.02% | 1/3 | 0 | 0 |
| CH_MODAL    | 0.8854 | 14.54% | -29.88% | 2/3 | 0 | 0 |
| CH_FREEZE63 | 0.7987 | 16.20% | -30.27% | 2/3 | 0 | 0 |

SPY OOS Sharpe 0.8684 (U56 tape) / 0.8767 (B136, SMALL tapes); live RULES v2 OOS Sharpe 1.2714 /
-12.05% MaxDD on U56.

CH_L16_IS − CH_FREEZE63 on mean OOS Sharpe is **+0.1336** — tuning the hold axis *helped* here,
the opposite sign to 1174's −0.0559. **Neither number is a measurement: both rest on three picks.**
Reported as a contradiction, not resolved. Queue idea 1183 (rolling IS window, dozens of picks per
ladder) is the only way to settle it, and this run is a second reason to run it. Note also that the
chooser with the best mean OOS Sharpe produced **no** 4b pass, while the coarse chooser's single
pick is the only one that cleared 4b — mean OOS Sharpe and the KEEP paths do not rank the choosers
the same way.

Both KEEP paths at all 432 books: **4a 0/432. 4b full AND OOS 17/432** (U56 16, B136 1, SMALL 0),
spread over 9 distinct (panel, N) families — and **G13 confirms all 17 are cells 1174 already
published today; 0 are new.** Nothing here is a candidate. **KILL as a capital finding.** No memo,
no RULES change (rule 6).

## Gates — 16 of 17 PASS

G1 fast runner ≡ `engine.backtest` 1.39e-17. G2 committed W/H126 N=20 triple 1.62e-03.
**G3 FAILS: the SPY OOS triple drifts 2.894e-03** from the committed anchor — this is bit-for-bit
the drift 1174 read on the same tape the same day, and **G3b diagnoses it**: 1174's same-day
committed benchmarks reproduce at 1.11e-16, so the drift is tape vintage (idea 1163), not
construction. G4 live MaxDD 4.95e-05. **G5 reproduces 1174's WHOLE committed 288-cell grid at
1.78e-15** (G5b: all 288 shared). G6 determinism 0. G7/G7b nesting and range. G8 the count-matrix
sampler ≡ direct block gathering **on the same drawn starts, cell for cell, 1.78e-14** — exactness,
not agreement in law. G8b bootstrap bias 1.22e-02. G9 the H dial is live (B136 turnover spread
6.47x/yr). **G10 falsification: CTRL_CORR at delta=0 reads RESOLVED at 0 of 27** (bar was 9) with
median modal share 0.1205 — the criterion does not fire on an axis whose rungs are identical by
construction. **G11 power: CTRL_CORR at delta=1.00 reads 27 of 27.** G12 pairing gain 3.04x at
100% of families. G13 new 4b cells = 0.

## What was NOT measured, and why

MaxDD is never given a bootstrap interval here. Sharpe and CAGR are additive in the resampled
blocks so their block bootstrap is exact; MaxDD is an order statistic of the path, and the
record's own same-day lane-B run ("why does an IID RESAMPLE produce DEEPER drawdowns than a BLOCK
one") shows a resampled drawdown is a *different object*, not a noisier reading of the same one.
MaxDD is reported point-wise at all 432 books and still scored in 4a/4b.

**SURVIVORSHIP (PROTOCOL rule 9).** U56, B136 and SMALL are current-constituent lists. Every CAGR
and drawdown level above is optimistic and every 4a/4b count is an upper bound. The resolution
question compares one construction against itself on one tape, and the bias very largely cancels
out of it; it does not cancel out of the rule-8 OOS levels, which are upper bounds.

## The clause this suggests (PROPOSED, NOT ENACTED — rule 6)

> An H-axis argmax may not be published as a finding without the sampling interval on it. Where the
> 90% argmax confidence set spans more than half the axis — which, at block 63, is every one of the
> 27 families measured here — the correct statement is "the axis does not resolve", not a rung.

Files: `.py`, `.console.txt`, `.grid.csv` (432 books), `.boot.csv` (1,350 = 27 x 5 x 5 x 2),
`.controls.csv` (378), `.rule8.csv` (15), `.benchmarks.csv` (6), `.gates.csv` (17),
`.leaderboard.txt`.
