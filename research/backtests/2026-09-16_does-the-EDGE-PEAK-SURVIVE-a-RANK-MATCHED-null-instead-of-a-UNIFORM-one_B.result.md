# Idea 1085 (lane B, 2026-09-16) — does the EDGE PEAK survive a RANK-MATCHED null instead of a UNIFORM one?

**ANSWERED = NO, AND IN THE OPPOSITE DIRECTION TO THE QUEUE'S CHARGE.** The 200d/vol gate is worth
**NEGATIVE** CAGR, so 1082's committed EDGE figures **UNDER-state** rank skill rather than
over-stating it — and essentially **none** of the +6.8 / +8.3 pp peak is gate (−1.0% / −3.7% of it).
But the peak's **LEFT-HAND SIDE does not survive**: U56's argmax moves 12 → **5**, and B136's holds at
10 only by 0.86 SE (it was 4.50 SE under the uniform null). **KILL** of the queue's "the peak is
partly gate" premise; **CORRECTION** to 1082's hump, which reduces to a far-side collapse.

Script: `2026-09-16_does-the-EDGE-PEAK-SURVIVE-a-RANK-MATCHED-null-instead-of-a-UNIFORM-one_B.py`
(112 s, deterministic). Console: `..._B.console.txt`. All 12 gates PASS, including **G9**: the OPEN
arm reproduces all 18 of 1082's committed EDGE figures to 4.9e-07 pp under 1082's own seed recipe,
so the two runs are the same object and the ELIG arm is the only new measurement.

## The two dials (PROTOCOL rule 4) — all 18 cells per panel reported, nothing hidden

| dial | values |
|---|---|
| **N** | 5, 8, 10, 12, 15, 20, 25, 30, 40 — 1082's ladder unchanged |
| **NULLGATE** | **OPEN** = random ranks, no eligibility gate (1082's / the record's convention, the control) · **ELIG** = random ranks drawn from the book's OWN eligible set (px > 200d MA AND 20d annualised vol < 0.60) |

Frozen, **not** dials: seeds 40 (1082's second dial, retired here), cap INF, CAND20 legs, max_vol
0.60, gross 0.75, W cadence, min hold 126, 10 bps, LAG 1, REBUILT DD-match convention.

`EDGE_g(n) = 100 · (CAGR_book(n) − median_s CAGR_null_g(n,s))`, every null path scaled to the book's
**own** realised |MaxDD| at that rung. `GATE(n) = EDGE_OPEN(n) − EDGE_ELIG(n)`.

## How much the gate binds (a tape fact both arms see)

| panel | eligible / priced at the mean rebalance | min | rebalances with <20 / <40 eligible |
|---|---|---|---|
| U56 | 37.5 of 54.1 (69.2%) | 3 | 10.5% / 43.3% |
| B136 | 91.4 of 131.4 (69.6%) | 3 | 2.4% / 6.9% |

## THE ANSWER — EDGE under each null gate (40 seeds, REBUILT)

| panel | N | book CAGR | EDGE_OPEN | EDGE_ELIG | **GATE** | ±SE | GATE as share of EDGE_OPEN |
|---|---|---|---|---|---|---|---|
| U56 | 5 | 17.83% | +5.950 | **+7.386** | −1.436 | 0.583 | −24.1% |
| U56 | 8 | 16.84% | +5.351 | +5.656 | −0.305 | 0.596 | −5.7% |
| U56 | 10 | 17.12% | +6.205 | +6.526 | −0.321 | 0.501 | −5.2% |
| U56 | **12** | 17.71% | **+6.820** | +6.889 | −0.069 | 0.404 | **−1.0%** |
| U56 | 15 | 17.00% | +5.215 | +5.839 | −0.624 | 0.335 | −12.0% |
| U56 | 20 | 15.58% | +5.118 | +5.145 | −0.027 | 0.343 | −0.5% |
| U56 | 25 | 14.89% | +2.953 | +3.499 | −0.546 | 0.296 | −18.5% |
| U56 | 30 | 14.01% | +1.546 | +1.906 | −0.360 | 0.219 | −23.3% |
| U56 | 40 | 13.46% | +0.414 | +0.910 | −0.496 | 0.106 | −120.0% |
| B136 | 5 | 18.91% | +5.717 | +8.189 | −2.471 | 0.612 | −43.2% |
| B136 | 8 | 17.82% | +5.245 | +6.754 | −1.510 | 0.536 | −28.8% |
| B136 | **10** | 18.09% | **+8.324** | **+8.631** | −0.307 | 0.477 | **−3.7%** |
| B136 | 12 | 17.60% | +6.520 | +6.585 | −0.065 | 0.459 | −1.0% |
| B136 | 15 | 16.78% | +6.834 | +6.710 | **+0.123** | 0.400 | +1.8% |
| B136 | 20 | 16.04% | +4.932 | +5.601 | −0.669 | 0.331 | −13.6% |
| B136 | 25 | 16.37% | +4.269 | +5.144 | −0.875 | 0.322 | −20.5% |
| B136 | 30 | 16.01% | +2.811 | +3.788 | −0.977 | 0.231 | −34.8% |
| B136 | 40 | 15.31% | +1.853 | +2.921 | −1.067 | 0.217 | −57.6% |

`GATE < 0` at **17 of 18** rungs (the sole exception, B136 N=15 at +0.123 pp, is 0.31 SE, i.e.
zero). Mean GATE −0.465 pp (U56) and −0.869 pp (B136).

**Reading.** The record's uniform null is a *harder* null than the eligibility-gated one, not an
easier one. Gating to eligible names and then ordering them at chance **loses** CAGR. So every
committed EDGE figure in this family is a **lower** bound on rank skill, and the queue's worry —
that EDGE(n) is inflated by the gate's own contribution — is the wrong sign.

**How much of the peak is gate rather than rank?** At the peak rungs, **−1.0%** (U56 N=12) and
**−3.7%** (B136 N=10). The peak is rank, entirely.

## The clip-free control (D5) — this is not a λ artefact

λ is capped at 1, so a null draw already drier than the book enters unmatched with its CAGR
under-stated, which *inflates* that arm's EDGE. The ELIG null is clipped more often than the OPEN
null at 14 of 18 rungs, so the matched GATE is confounded. The same contrast with **no DD match at
all** (both nulls at gross 0.75) cannot be a clip artefact:

| panel | GATE_raw range | mean | sign agrees with matched GATE | ELIG null drier |
|---|---|---|---|---|
| U56 | −1.579 .. −0.541 pp | −1.163 | **9 of 9** | 9 of 9 rungs |
| B136 | −1.889 .. −0.850 pp | −1.529 | **8 of 9** | 7 of 9 rungs |

Every GATE_raw is negative and all but two exceed 2 SE. Unmatched, a random draw from the eligible
set earns **0.54–1.89 pp/yr less** than a random draw from everything priced, while running
**0.9–3.3 pp drier**. **The 200d/vol gate is a RISK filter, not a return filter.** Under a DD match
the dryness is partly paid back as a higher λ, which is why the matched GATE (−0.03 .. −2.47 pp) is
smaller in magnitude than GATE_raw — but not enough to turn it positive.

## THE COST — the shape of the ladder does NOT survive intact

| | U56 | B136 |
|---|---|---|
| argmax EDGE_OPEN | 12 | 10 |
| argmax EDGE_ELIG | **5** | 10 |
| peak − EDGE(5), OPEN | +0.870 ± 0.507 = 1.72 SE (not decisive) | +2.607 ± 0.579 = **4.50 SE** |
| peak − EDGE(5), ELIG | n/a (5 *is* the peak) | +0.443 ± 0.516 = **0.86 SE** (not decisive) |
| peak − EDGE(20), ELIG | +2.241 ± 0.479 = 4.68 SE | +3.030 ± 0.399 = 7.59 SE |
| peak − EDGE(40), ELIG | +6.477 ± 0.442 = **14.64 SE** | +5.710 ± 0.353 = **16.17 SE** |
| Spearman(OPEN ladder, ELIG ladder) | 0.9333 | 0.8667 |

**On both panels the hump's left-hand side dissolves under the fairer null.** U56 flips outright
(n=5 now wins); B136 keeps n=10 but its margin over n=5 falls from 4.50 SE to 0.86 SE, i.e. from
decisive to undecidable. What survives on both panels, and overwhelmingly, is the **far-side
collapse**: the peak beats n=40 by 14.6 / 16.2 SE. 1082's headline should be re-read as *EDGE
collapses above ~n=15*, not as *EDGE peaks at n=12 / n=10*.

`H_GATEFLAT` FAILS on both panels (spread 1.409 pp vs 2 SE = 1.210; 2.595 pp vs 1.299), so the
queue's premise that **"the mix changes with n"** is literally **confirmed** — the gate's
contribution is not constant across the ladder. It just runs the other way and is far too small to
build the peak.

## Hypotheses, scored as declared (19; 8 PASS, 11 FAIL)

PASS: H_HUMP ×2 (peak still beats n=40 decisively under ELIG), H_SIG ×2 (ELIG peak +7.386 / +8.631
pp vs 2 SE 0.878 / 0.659), H_ARGMAX[B136], H_EDGEPICK (both EDGE choosers pick n=5 on both panels),
H_4A (0 of 18 rungs clear 4a).
FAIL: H_ARGMAX[U56] (12 → 5), H_GATEPOS ×2, H_GATEFLAT ×2, H_HALF ×2, H_SLOPE ×2, H_RANKORDER ×2,
H_WF (0 of 10 rule-8 picks clear 4b OOS).

## PROTOCOL rule 8 — N chosen on IS (2009–2016) only, OOS (2017–2026) read ONCE

| panel | chooser | N | OOS CAGR / Sharpe / MaxDD | SPY OOS | 4b OOS |
|---|---|---|---|---|---|
| U56 | C_ISSHARPE / C_ISDD | 40 | 14.00% / 1.0983 / −22.98% | 15.21% / 0.8711 / −33.72% | **fail** (O_DD) |
| U56 | C_ISCAGR / C_ISEDGE_OPEN / C_ISEDGE_ELIG | 5 | 17.06% / 0.9003 / −25.85% | 15.21% / 0.8711 / −33.72% | **fail** (O_DD) |
| B136 | C_ISSHARPE | 8 | 14.56% / 0.7866 / −24.54% | 15.33% / 0.8767 / −33.72% | **fail** (O_S, O_DD) |
| B136 | C_ISDD | 30 | 16.61% / 1.0696 / −24.35% | 15.33% / 0.8767 / −33.72% | **fail** (O_DD) |
| B136 | C_ISCAGR / C_ISEDGE_OPEN / C_ISEDGE_ELIG | 5 | 15.03% / 0.7687 / −28.12% | 15.33% / 0.8767 / −33.72% | **fail** (O_S, O_DD) |

**0 of 10 picks clear 4b out of sample**, every one on the drawdown leg (60%-of-SPY OOS cap =
20.23%). The new ELIG-based EDGE chooser picks the same rung as the OPEN one on both panels, so the
null gate does **not** rescue rule 8.

## KEEP paths

- **4a: 0 of 18 rungs.** The MaxDD leg against live RULES v2 (−12.05% / −12.24%) is unreachable by
  any rung of this book, as 1082 found.
- **4b full sample: 3 of 18** (U56 n=12, U56 n=20, B136 n=15) — byte-identical to 1082's three
  passes, since the book is unchanged. All three were already PARKed by 1082 on two grounds that
  this run does not disturb: their DD margins (+0.06 / +1.10 / +0.57 pp) sit far inside 1083's
  4.1–7.2 pp decidability width, and **no IS-only chooser reaches them** (H_WF above).
- **Nothing is proposed. No memo. No rule change.**

## Survivorship (PROTOCOL rule 9)

U56 and B136 are current-constituent lists, so every level is optimistic and every 4b count is an
upper bound. EDGE_OPEN, EDGE_ELIG and GATE are all within-pool contrasts over the same tape, so the
bias very largely cancels out of this run's headline; it does **not** cancel out of the 4b legs,
which are measured against SPY.

## What this costs the record

Two committed readings move:

1. **Every EDGE figure in the 1071 / 1082 / 1086 family is a lower bound on rank skill**, by
   0.03–2.47 pp depending on the rung. The record's null is gate-free, and a gate-free random book
   *out-earns* a gated one (D5: by 0.54–1.89 pp/yr unmatched), so it is the **harder** comparand.
   Any prose describing EDGE as "the composite's advantage over chance" is reading a quantity that
   silently charges the composite for the gate's own negative CAGR contribution.
2. **1082's argmax is not a stable object.** It is n=12 / n=10 against a uniform null, n=5 / n=10
   against a rank-matched one, and D3 shows it also moved with the seed count on U56 (5/12/12 at
   S=10/20/40). The far-side collapse is the durable fact; the peak location is not.
