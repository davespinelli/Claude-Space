# Idea 131 — gross-as-the-missing-third-bar (lane B, 2026-09-05)

**Verdict: ANSWERED — KILL of the swap.** A minimum-mean-gross bar **cannot replace 4b's CAGR
floor**, because **no value of γ does both jobs**. To admit all 11 Pareto-best defensive books
the floor throws away you need γ ≤ 0.51, and there the bar admits **23** static-gross ladder
points (the CAGR floor admits 10). To empty the ladder you need γ ≥ 0.68, and there the bar
admits **0 of the 11**. The two families **overlap on the gross axis** — the floor's victims run
from 0.519 to 0.750 mean gross, the core-admissible ladder points from 0.075 to 0.673 — and the
axis is **actively perverse in the overlap**: raising γ from 0.53 to 0.54 discards **6 of the 11
Pareto-best books and 0 ladder points**. Gross ranks the lever *above* the books it was
introduced to save.

Idea 129's closing diagnosis — "the floor's real content is a gross-level filter" — is
**false as stated**. The floor's content is not reducible to a gross level.

## Harness and reproduction

Idea 94's script is **imported**; idea 129's corpus is reproduced **exactly** before any new
number is read. Corpus = 3 panels (u56, broad, small) × 3 books (V1u, TOP20, EWall) × 17 arms ×
2 cost rungs = **306 arm-rows**, plus the 19-point static-gross ladder per cell (**342 rows**)
carried separately as the pure de-risking control. Weekly, t+1, 75% target gross,
IS ≤ 2016-12-31, OOS ≥ 2017-01-01.

| check | result |
|---|---|
| (a) `H.run` vs `engine.backtest`, ungated EWall u56 | max abs diff **0.00e+00** — PASS |
| (b) idea 94's published `EWall+vol60-dg` u56 @10bps (11.6% / 1.133 / −16.9%) | **11.587% / 1.133 / −16.884%** — PASS |
| (c) idea 129's census: 306 rows / 82 Pareto / 29 pass 4b / 27 floor-only / 11 of 23 on the frontier / 97 of 342 ladder floor-only, all at m ≤ 0.80 | **all eight exact** — PASS |
| (d) idea 129's IS-screen groups A / B / C | **45 / 9 / 252** — PASS |

Two tuned parameters, both bar coefficients: γ (mean-gross floor) ∈ {0.00 … 0.75} on the coarse
grid and 0.45→0.78 step 0.01 on the fine sweep; φ (CAGR floor) ∈ {0.00 … 1.00}. δ (the MaxDD
cap) is **held** at its published 0.60 — not a third dial. **All grid points reported.**

## Q1 — the swap does admit the defensive books, at zero cost

At the QUEUE's own γ = 0.50: **27 of 27** floor-only victims admitted, **11 of 11** Pareto-best
among them, and **0** rows that currently pass 4b are lost. 4b passes rise 29 → 56; rows passing
*both* KEEP paths rise 6 → 25.

But the same table says why that is not a result: at γ = 0.50 the gross bar admits **exactly the
56 rows the core four bars admit** — it is **identical to deleting the floor and adding nothing**.
On the arm corpus the bar does no work at all until γ > 0.51.

## Q2 / Q2b — the decisive table: no γ does both jobs

Floor-only victims: n = 27 (11 Pareto), mean gross **0.519 / 0.551 / 0.750** (min/median/max).
Core-admissible ladder points: n = 107, mean gross **0.075 / 0.338 / 0.673**. **Not separable.**

| γ | corpus admits | of the floor's 29, lost | victims saved (of 27) | **Pareto victims saved (of 11)** | **ladder admitted** |
|---|---|---|---|---|---|
| 0.50 | 56 | 0 | 27 | **11** | **23** |
| 0.51 | 56 | 0 | 27 | **11** | 23 |
| 0.53 | 52 | 0 | 23 | 7 | 16 |
| **0.54** | 44 | 0 | 15 | **1** | 16 |
| 0.61 | 35 | 0 | 6 | 1 | 5 |
| 0.65 | 32 | 1 | 4 | 1 | 1 |
| 0.68 | 30 | 1 | 2 | **0** | **0** |
| φ = 0.70 (published floor) | 29 | — | 0 | 0 | 10 |

**γ achieving both (all 27 victims AND 0 ladder points): 0 of 34 grid points.** The one-step
collapse at 0.53 → 0.54 (−6 Pareto books, −0 ladder points) is the mechanism: on the gross axis
a 52.5%-gross *lever* outranks a 53.3%-gross *gated book*. The overlap region [0.519, 0.673]
contains **25 of the 27 victims and 23 ladder points**.

**Why the level fails, and what does not.** The ladder holds gross *constant* by construction;
a de-grossing gate makes it *time-varying*. On the coefficient of variation of daily gross the
two families come apart almost completely — victims **cv 0.268** mean (max 0.335), ladder
**cv 0.014** mean (max 0.022) — and **25 of 27 victims, including all 11 Pareto-best, sit above
every ladder point**. The two exceptions are `v1gate-rw` and `g200-rw`, which are full-gross
*rebuilds* that never de-gross and therefore hold gross constant exactly as the ladder does — a
mechanism, not noise. **No threshold is fitted and no verdict here rests on this**; it is
reported so the next queue idea can pre-register it.

**The one thing that does survive.** γ ∈ [0.57, 0.61] **weakly dominates the published CAGR
floor on the floor's own three criteria**: it loses none of the floor's 29 admissions, saves 6–8
of its victims, and admits 5–9 ladder points against the floor's 10. At γ = 0.61: **35 admitted,
0 lost, 6 victims saved, 5 ladder points** vs the floor's **29 / — / 0 / 10**. So gross is a
*better* one-number exposure-adequacy bar than CAGR — it is simply not a *good* one, since it
still discards 10 of the 11 books the exercise existed to save.

## Q3 — the two bars are not substitutes

| family | n | Spearman(mean gross, CAGR) |
|---|---|---|
| arm corpus | 306 | **+0.245** |
| static-gross ladder | 342 | **+0.691** |

The association the swap depends on holds **only on the ladder**, where gross and CAGR are the
same dial by construction. On real books it is weak. Verdict agreement: corpus 91.2%, ladder
96.2%; the disagreements are one-sided in both (27 and 13 rows the gross bar admits and the
floor does not; **0 rows in the other direction**).

Admitted-set OOS quality (full-sample bars, read on 2017–2026): 4b-FLOOR n=29, Sharpe **1.114**,
MaxDD **−18.5%**, CAGR **13.2%**, 6 also pass 4a. 4b-GROSS γ=0.50 n=56, Sharpe **1.112**, MaxDD
**−16.6%**, CAGR **11.2%**, 25 also pass 4a. The swap buys 1.9 pp of shallower drawdown and 27
more admissions for −0.002 Sharpe and −2.0 pp CAGR — arithmetically idea 129's φ=0 point, as it
must be.

## Rule 8 walk-forward (screens read 2009–2016 only; picks read once on 2017–2026)

S0 no screen · S1 IS-4b + CAGR floor (φ=0.70) · S2 IS-4b, no adequacy bar · S3 IS-4b + gross bar.

| selector | cells picking | OOS CAGR | OOS Sharpe | OOS MaxDD | beat SPY | beat v1 | picks moved vs S0 |
|---|---|---|---|---|---|---|---|
| S0 (all 18) | 18 | 9.1% | 0.695 | −23.1% | 6/18 | 12/18 | — |
| S1 (floor) | 7 | 12.7% | 1.022 | −21.1% | 5/7 | 7/7 | **0** |
| S2 (neither) | 7 | 12.7% | 1.022 | −21.1% | 5/7 | 7/7 | **0** |
| S3 (γ ≤ 0.65) | 7 | 12.7% | 1.022 | −21.1% | 5/7 | 7/7 | **0** |
| S3 (γ = 0.70) | 6 | 13.4% | 1.077 | −21.0% | 6/6 | 6/6 | 1 |

Reference OOS: **SPY 15.5% / 0.882 / −33.7%**; RULES v1 Sharpe 0.747 (u56 row; per-cell values in
the walk-forward csv). **Paired on the cells S3 enters**, S0 = S1 = S2 = S3 = **1.022 / −21.1% /
12.7%** at every γ ≤ 0.65. The gross bar is **exactly as inert in selection as the CAGR floor** —
0 picks moved in 7 of 7 cells — which reproduces idea 132's finding on a third bar. The single
γ=0.70 move (+0.010 Sharpe on 6 cells) is one pick and is not claimed as a result.

## Both KEEP paths, all 306 rows

4a: **97 of 306**. 4b published: **29**. 4b with the gross bar at γ=0.50: **56** (27 new, of which
19 also pass 4a). Both paths: 6 → 25. **No new book is proposed** — this script re-scores an
existing corpus under an alternative bar, which is the thing being adjudicated. Nothing is
promoted to a KEEP candidate on the strength of a bar this run recommends against adopting.

## Caveats, stated not buried

- **Survivorship** (idea 54): all three panels are current-constituent lists. Absent delistings
  inflate CAGR most for the *ungated, high-gross* books, which flatters the CAGR floor and not
  the gross bar. The dominance band in Q2b is therefore, if anything, understated — and the
  non-separation result is unaffected, since it is a statement about mean gross, not returns.
- **Idea 128**: the IS window's SPY MaxDD is 65% (u56/broad) and 55% (small) of the full sample's,
  so every IS drawdown cap here admits too much. This biases S1, S2 and S3 identically and
  cannot explain a 0-vs-0 difference in moved picks.
- **n is small where it matters**: 11 Pareto-best victims in 4 cells, all EWall, overlapping
  return series. The frontier table is a census of this corpus, not an estimate for a population.
- **Idea 38** (u56/broad calendar-day index) and **idea 126** (t+1 only, no lag band) carry over.
- The ladder is the *only* control used for "is this bar doing its job". It is a narrow control:
  it catches de-grossing, not other ways of gaming a drawdown cap.

## What this leaves for PROTOCOL

The memo proposes the negative clause — **4b's exposure-adequacy bar must not be restated as a
gross level** — plus the one usable positive (γ ∈ [0.57, 0.61] as a strictly better-calibrated
version of the same idea, if a single number is wanted). The constructive direction is that the
ladder's exclusion is a **construction** question, not a metric one: a static rescaling of an
existing book is the same book. Idea 129's `4b-defensive` reporting class remains the live
proposal for the 27 rows. The dispersion result above is filed as a new queue idea rather than
adopted here — it was found *after* the pre-registered question was answered, and adopting it in
the same run would be exactly the tuning rule 7 forbids.

**Determinism:** the script was run twice; the Q1/Q2/Q3/grid/walk-forward sections are
byte-identical between runs.

Script: `research/backtests/2026-09-05_gross-as-the-missing-third-bar_B.py`
Console: `.console.txt` · Corpus: `.grid.csv` · Ladder: `.ladder.csv` ·
Calibration: `.calibration.csv` · Ladder calibration: `.ladder_calibration.csv` ·
Separation: `.separation.csv` · Walk-forward: `.walkforward.csv` · Paired: `.paired.csv` ·
Memo: `.memo.md`
