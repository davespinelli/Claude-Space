# Idea 810 — price the U56 / MA-BAND / g=1.00 VOL-gated book against its GROSS-MATCHED CONTROL

**ANSWERED. The drawdown effect idea 596 flagged is REAL and survives every dial the queue named —
and it is still NOT capital-worthy. The −5.54 pp MaxDD advantage over the book's own gross-matched
control is a ONE-EPISODE statistic: in-sample it is +0.71 pp, out-of-sample +5.54 pp, because U56's
binding drawdown is the single 2020 episode, which sits entirely inside the OOS window. It is bought
with out-of-sample Sharpe (−0.039 against the same control), it is the same order as the rebalance
convention floor of its own two books (5.54 pp vs a 5.53 pp floor), and the arm fails 4a against
RULES v2 at 0 of 40 grid points while sharing its 4b pass with its own control at 23 of 24.
KILL for capital; the effect is worth recording, the book is not.**

Script `2026-09-12_price-the-U56-MA-BAND-g1.00-LIGHT-OVERLAY-against-its-GROSS-MATCHED-CONTROL_cloud.py`
(6.4 s, deterministic, no network). **Pre-registered before any number was read**: the cell (U56,
`baseline.rules_v2_weights` 200d ±3% band, g/N to CASH, g = 1.00, VOL gate = SPY 20d realised vol ≤
dial, weekly, t+1, gate OFF ⇒ whole book to cash), the comparand (**CONTROL-M** = the same book × a
constant matching the arm's mean realised gross), the statistic (**dMaxDD_M = MaxDD(arm) −
MaxDD(CONTROL-M)**, positive = arm shallower), and the deciding test (rule 8 on that statistic).
**Tuned: dial (8) × cost (5) = 40 points, all reported.** Reported-never-selected: execution lag
(t+1, t+2), window, and the 5 phases of the rebalance schedule.

## The pre-registered cell (U56 / band ±3% / g 1.00 / VOL 0.25 / weekly / t+1 / 10 bps)

| | CAGR | Sharpe | MaxDD | halves | OOS CAGR / Sharpe / MaxDD |
|---|---|---|---|---|---|
| **arm** | 11.08% | 1.210 | **−9.57%** | 1.305 / 1.125 | 11.58% / 1.239 / −9.57% |
| **its own CONTROL-M** | 10.93% | 1.202 | **−15.11%** | — | 12.02% / **1.278** / −15.11% |
| CONTROL-U (g 1.00, ungated) | — | — | −15.91% | — | — |
| RULES v2 baseline (live) | 8.63% | 1.202 | −12.05% | — | 9.47% / 1.278 / −12.05% |
| SPY buy-and-hold | 15.16% | 0.886 | −33.72% | — | 15.33% / 0.877 / −33.72% |

Gate OFF 10.94% of days; mean realised gross 0.6730 (arm) vs 0.7102 (CONTROL-U); turnover 2.60/yr
vs the control's 2.23.

## The seven pre-registered hypotheses

| test | bar | measured | verdict |
|---|---|---|---|
| **H_REPRO** reproduces idea 596's committed cell | Sharpe 1e-4, levels 5e-4 | CAGR 1.6e-5, MaxDD 1.0e-5 and 7.8e-6 **pass**; arm Sharpe 1.49e-4, ctlM Sharpe 2.85e-4 **exceed the bar** | **FAIL at the stated bar** |
| **H_SIGN** dMaxDD_M > 0 at the cell | > 0 | **+5.54 pp** | **PASS** |
| **H_DIAL** majority of dials, contiguous | > 4 of 8, contiguous | **5 of 8** ({0.15,0.20,0.25,0.30,0.35}), contiguous | **PASS** |
| **H_COST** DD effect cost-insensitive, Sharpe edge decays | < 1.00 pp; monotone | **0.983 pp** over 0→50 bps; dSharpe_M +0.012 → −0.008, monotone | **PASS** |
| **H_FLOOR** Sharpe gap inside its floor, DD gap outside | both | floor: Sharpe **0.0942**, MaxDD **5.53 pp**; measured \|dSharpe_M\| **0.0084** (inside), \|dMaxDD_M\| **5.54 pp** (outside **by 0.01 pp**) | **PASS, by a hair** |
| **H_WF** rule 8: OOS dMaxDD_M > 0 | > 0 | **+5.54 pp**, and positive in **20 of 20** (lag × cost × selector) picks | **PASS** |
| **H_4b** 4b does not separate arm from CONTROL-M | both pass | both pass at the cell; over 40 points arm 4b 24, ctlM 4b 23, arm-passes-where-control-fails **1** | **PASS** |

**On H_REPRO:** the two failures are Sharpe only, at 1.5e-4 and 2.9e-4 against a 1e-4 bar — and idea
596 published those Sharpes as `1.210` and `1.202`, i.e. to a half-ulp of **5e-4**. The bar I
pre-registered is tighter than the precision at which the parent number exists, so this reads as a
**bar-setting fault, not a reproduction failure**: every quantity reproduces to the precision at which
it was published. The pre-registered verdict stands as FAIL and the reading is stated rather than the
bar relaxed. The general lesson is the record's own: **publish the precision beside the number, or no
later run can test reproduction of it.**

## Why the effect is real and still does not earn capital

1. **It is one episode.** IS (…2016-12-31) dMaxDD_M is **+0.71 pp**; OOS (2017-01-01…) is **+5.54 pp**,
   and the full sample equals the OOS number exactly — U56's binding drawdown is the 2020 episode
   (idea 596's own finding), which lies wholly inside the OOS window. The "20 of 20 walk-forward picks
   positive" is therefore **20 readings of one drawdown**, not 20 confirmations. Nothing here
   establishes the gate would cover the *next* one.
2. **It is paid for in Sharpe, out of sample.** OOS dSharpe_M = **−0.039**: the arm's OOS Sharpe
   (1.239) is below its own gross-matched control's (1.278) and below RULES v2's (1.278). The full-
   sample "+0.008 at equal Sharpe" that made the cell look free is **inside the 0.0942 convention
   floor** of the same two books — idea 596's "equal Sharpe" was a floor statement, now measured.
3. **The DD gap is the size of the convention.** Re-run on the 5 phases of the same 5-day rebalance
   schedule, the same comparison reads **+1.66 to +4.84 pp** — every phase positive (the sign is
   robust), but every phase *smaller* than the calendar-weekly +5.54 pp. The published cell sits above
   the whole phase range: the calendar-week convention is the most flattering one available to it.
4. **KEEP paths.** 4a **0 of 40** grid points against RULES v2 (and 0 on the OOS window). 4b 24 of 40,
   but CONTROL-M — which holds uniformly less with no timing at all — passes at 23 of those, so the
   4b pass is exposure, not clause, exactly as idea 596 found. The single cell where 4b does see the
   clause (dial 0.25, **25 bps**, control fails on CAGR) is a cost artefact, not a candidate.
5. **Delayed execution.** At t+2 the cell still reads +5.20 pp, and the IS-dMaxDD selector then picks
   dial 0.15 at three of five cost rungs — a dial whose OOS dSharpe_M is **−0.22**. The selector this
   run pre-registered is itself unstable in the execution lag.

## Gates
G1 never-firing gate ≡ CONTROL-U **0.000e+00** on returns and turnover (bar 1e-12) · G2 fast runner ≡
`engine.backtest` **8.674e-18** (bar 1e-9) · G3 CONTROL-M's mean realised gross ≡ the arm's, max over
the whole grid **1.562e-04** (bar 1e-3) · G4 determinism, whole grid recomputed **0.000e+00**.

## Verdict
**6 of 7 pre-registered hypotheses pass, and the cell is still NOT a KEEP.** The pre-registered KEEP
condition (the DD effect survives rule 8 **and** clears its own convention floor **and** is contiguous
in the dial **and** the arm passes 4b where its gross-matched control does not) fails on its last
clause. No RULES change, no book promoted, no memo of candidacy, no PROTOCOL edit (rule 6).
`RULES.md`, `PROTOCOL.md`, `scan.py`, `bot.py`, `baseline.py` untouched.

**What is worth keeping is the measurement, not the book:** a de-gross clause can cut a real 5.5 pp of
drawdown against a gross-matched control at no full-sample Sharpe cost, and PROTOCOL 4b cannot see it
(its DD leg is a floor against SPY, its Sharpe legs are against SPY). That is the record's standing
complaint about the DD cap, now with a within-panel, floor-calibrated, walk-forward number attached —
and with the size of the claim cut by the two things the parent could not see: the effect is one
episode, and it is the size of its own rebalance convention.

## Caveats
- **SURVIVORSHIP.** U56 is a current-constituent list (`research/universe.json`); every level is
  optimistic. The headline is a within-panel difference between two books on the same names, which
  the bias moves far less than it moves levels — but the walk-forward levels carry it in full.
- One panel, one gate family, one gross. Nothing here speaks to B136 or the small panel, and idea
  596's grid is the only evidence that this cell was the best of 144 — which is why it was
  pre-registered rather than claimed.
- The convention floor is measured on a 5-day-block schedule, not on calendar weekdays; it is a
  phase spread of the same schedule length, which is the comparable object, and is stated as such.
