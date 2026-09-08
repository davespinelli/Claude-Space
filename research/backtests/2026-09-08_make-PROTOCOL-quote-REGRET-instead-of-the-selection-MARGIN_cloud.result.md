# Idea 445 — make-PROTOCOL-quote-REGRET-instead-of-the-selection-MARGIN (cloud lane, 2026-09-08)

**Verdict: ANSWERED / clause DRAFTED — with the queue's own premise corrected in two places.
The proposal is CONFIRMED (publish ROOM and REGRET separately); the implicit sub-claim that
REGRET is a single quotable constant is KILLED.  No KEEP (4b 0 of 4, 4a-vs-v2 0 of 4).**

Script: `2026-09-08_make-PROTOCOL-quote-REGRET-instead-of-the-selection-MARGIN_cloud.py`
(deterministic, seed 445000, no network, 43 s).  Two tuned parameters, all 4 grid points
reported: **P1** ladder recovery in {SHARED-KEYS, DROP-ARM} (idea 446's semantics, imported),
**P2** control vocabulary in {STRICT, BROAD} (idea 229's, imported), each read at three
reproduction-certificate thresholds (0 / 0.5 / 1.0) = 12 published rows.

---

## A. The `32` audit — the queue's count is wrong, and the word is undefined

306 committed `*.walkforward.csv` files scanned (this run's own artefact excluded so the census
is idempotent on a re-run).

| | files |
|---|---|
| literal `regret` column | **65** (21.2%), 3,093 rows |
| regret derivable from a best-in-pool column | 19 |
| neither | 222 |

The queue's "32 instances that already publish a regret column" does not reproduce: it is **65
files**. The number 32 does appear — it is the count of files publishing **at least one
NEGATIVE** regret, which is impossible if regret means *best-minus-pick*. **15.6% of all 3,093
published regret values in the record are negative**, and several files (e.g.
`does-CONDITIONAL-correlation-beat-unconditional`, `breadth-gate-on-v2_B`,
`earnings-season-avoidance_cloud`) publish regret columns that are negative in *every* row —
i.e. a signed margin wearing the name `regret`. **`regret` is not currently a defined term in
this record.** That is an argument for the clause, not against it.

## B. The back-fill — ROOM and REGRET recomputed from the recovered ladders

For every SHAPE-W instance, the arm ladder was rebuilt from the committed `<stem>.grid.csv` and

```
REGRET = OOS_best(ladder) - OOS_pick        ROOM = OOS_best(ladder) - OOS_control
MARGIN = OOS_pick - OOS_control  ==  ROOM - REGRET
```

**Identity check: max |MARGIN − (ROOM − REGRET)| = 1.11e-16 over all 28,775 back-filled cells.**

| P2 | P1 | files attempted | recovered | cells on a ≥2-arm ladder | median ladder | certificate |
|---|---|---|---|---|---|---|
| STRICT | SHARED-KEYS | 65 | 44 (67.7%) | 2,634 | 17 | 94.8% of cells, 41/44 files at 100% |
| STRICT | DROP-ARM | 65 | 52 (80.0%) | 3,949 | 18 | 95.6%, 49/52 at 100% |
| BROAD | SHARED-KEYS | 115 | 64 (55.7%) | 8,763 | 16 | 96.4%, 61/64 at 100% |
| BROAD | DROP-ARM | 115 | 75 (65.2%) | 13,429 | 17 | 96.9%, 72/75 at 100% |

Rejections are published by reason (no committed grid CSV 5–19, grid without `OOS_Sharpe` 6–12,
no ≥2-arm group 2–18, no axis outside the cell key 0–2). **34–44% of the class cannot be
back-filled and is counted as unaudited, never as a pass.**

**Recovered regret does NOT reproduce the record's published regret column**: on the 6,372 cells
carrying both, mean |diff| 0.137, only 18.4% agree to 1e-6. Given part A, the disagreement is at
least partly the record's own inconsistent definition; the rest is that a recovered ladder is an
inference about the pool a run selected over. Either way it is a defect the clause fixes, and it
is reported, not smoothed over.

## C. The attribution — MARGIN moves, REGRET does not

Instance-weighted, bootstrap (2,000 draws) blocked on the instance:

| P2 | P1 | inst | cells | MARGIN | 95% CI | ROOM | REGRET | 95% CI | ROOM-dominated |
|---|---|---|---|---|---|---|---|---|---|
| STRICT | SHARED-KEYS | 46 | 2,634 | **−0.00892** | [−0.041, +0.020] | +0.12546 | **+0.13438** | [+0.102, +0.170] | 43.5% |
| STRICT | DROP-ARM | 54 | 3,949 | **−0.00376** | [−0.032, +0.023] | +0.12807 | **+0.13184** | [+0.101, +0.167] | 44.4% |
| BROAD | SHARED-KEYS | 119 | 8,763 | **+0.08371** | [+0.034, +0.136] | +0.21520 | **+0.13148** | [+0.109, +0.160] | 61.3% |
| BROAD | DROP-ARM | 145 | 13,429 | **+0.08412** | [+0.039, +0.128] | +0.21013 | **+0.12602** | [+0.104, +0.149] | 64.8% |

(cert ≥ 0.5 and ≥ 1.0 rows are in `.boot.csv`; they move every number by < 0.01 and change no
sign.)

Across the four grid points: **MARGIN spans −0.00892 … +0.08412 (swing 0.093, and it CHANGES
SIGN). ROOM spans +0.1255 … +0.2152 (swing 0.090). REGRET spans +0.1260 … +0.1344 (swing
0.008 — an order of magnitude smaller, and always positive.)** Relative dispersion across
instances (sd / |mean|): MARGIN **11.21**, REGRET **1.01**.

## D. The invariance test — this is the clause, as an identity

48 files publish ≥2 admitted control columns (92 file × grid-point blocks). Same pick, same
ladder, different comparand:

| quantity | blocks | mean within-file sd | mean within-file range | blocks with sd = 0 |
|---|---|---|---|---|
| margin | 92 | 0.166556953 | 0.360345682 | **2 / 92** |
| room | 92 | 0.166556953 | 0.360345682 | 2 / 92 |
| regret | 92 | **0.000000000** | **0.000000000** | **92 / 92** |

**REGRET is invariant to the comparand in 92 of 92 blocks; MARGIN in 2 of 92**, and MARGIN's
within-file variation is *exactly* ROOM's, to nine decimals. A published margin is therefore a
joint statement about the selector and the comparand the author happened to name; the regret is
a statement about the selector alone.

## E. Rule 8 on live prices, out of corpus

Idea 229's pre-registered ladder imported unchanged: 6 dials × 3 panels (u56 56, broad 136,
SMALL439) × 2 costs (10/25 bps), 234 books, choice on IS ≤ 2016-12-31, 2017–2026 read once,
t+1 execution, 260-bar warm-up skip.

Same 36 choices, four comparands:

| control | beats ctl | ROOM | REGRET | MARGIN | 95% CI on MARGIN |
|---|---|---|---|---|---|
| INCUMBENT arm | 17/36 | +0.11009 | **0.03871** | +0.07138 | [+0.021, +0.122] |
| LADDER-MEAN | 25/36 | +0.09508 | **0.03871** | +0.05637 | [+0.026, +0.093] |
| BOOK v2 (live) | 5/36 | −0.12346 | **0.03871** | −0.16217 | [−0.231, −0.103] |
| BOOK v1 | 29/36 | +0.39143 | **0.03871** | +0.35272 | [+0.238, +0.469] |

**REGRET is identical under all four (sd across controls 0.00e+00); MARGIN swings 0.515 of
Sharpe and changes sign.** Mean REGRET 0.03871, 95% CI [0.02046, 0.05789] — idea 229's
0.03871 [0.02078, 0.05805] reproduced exactly. By dial, ROOM concentrates in `kexp` (+0.308) and
`share` (+0.268), the two dials whose declared incumbent the record already knew was wrong,
while their REGRET (0.061, 0.096) is the same order as everywhere else — the margin's "win" is
the incumbent being bad, not the chooser being good.

### Both KEEP paths (pooled equal-weight books over the 36 cells, 10/25 bps pooled)

| book | CAGR | Sharpe | MaxDD | H1 / H2 | OOS CAGR | OOS Sharpe | OOS MaxDD | 4a v2 | 4a v1 | 4b | failing |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S1 IS-Sharpe chooser | 8.53% | 0.922 | −17.12% | 1.044 / 0.811 | 8.13% | 0.879 | −17.12% | False | True | **False** | H2\|OOS\|CAGR |
| S0 do nothing (incumbent) | 6.50% | 0.806 | −15.28% | 0.938 / 0.687 | 6.12% | 0.756 | −15.28% | False | True | False | H1\|H2\|OOS\|CAGR |
| LADDER-MEAN | 7.13% | 0.840 | −16.18% | 0.948 / 0.743 | 6.91% | 0.810 | −16.18% | False | True | False | H1\|H2\|OOS\|CAGR |
| ORACLE (not a rule) | 7.84% | 0.909 | −15.72% | 0.990 / 0.837 | 7.84% | 0.904 | −15.72% | False | True | False | CAGR |
| SPY | 15.23% | 0.889 | −33.72% | 0.959 / 0.834 | 15.45% | 0.882 | −33.72% | — | — | — | — |
| RULES v2 (live) pooled | 6.96% | 1.021 | −10.92% | 1.084 / 0.961 | 6.95% | 1.038 | −10.92% | — | — | — | — |
| RULES v1 pooled | 4.90% | 0.539 | −18.54% | 0.616 / 0.474 | 5.12% | 0.546 | −18.54% | — | — | — | — |

**KEEP: 4a-vs-v2 0 of 4, 4b 0 of 4** (4a-vs-v1 4 of 4, including the do-nothing book — which is
the paper's own point restated: v1 is not a bar).

## Predictions vs outcomes

| | prediction | outcome |
|---|---|---|
| R1 | "32" will not reproduce | **CONFIRMED** — 65 files; 32 is the negative-regret file count |
| R2 | ROOM large relative to REGRET | **PARTLY** — record-wide ROOM 0.125–0.215 vs REGRET 0.126–0.134, so ROOM dominates 43.5–64.8% of instances, not "most" under STRICT |
| R3 | REGRET tighter than MARGIN | **CONFIRMED** — sd/|mean| 1.01 vs 11.21; swing 0.008 vs 0.093 |
| R4 | within-file sd(REGRET) = 0 exactly | **CONFIRMED** — 92/92 blocks at 0.000000000 |
| R5 | live REGRET ≈ 0.04, no 4b KEEP | **CONFIRMED** — 0.03871 [0.020, 0.058], 4b 0 of 4 |

## The correction the queue needs

The queue asks PROTOCOL to **quote** the regret ("the real number is REGRET ~0.04"). That does
not survive this run: the live 36-cell corpus gives **0.0387 [0.020, 0.058]** and the
back-filled record gives **0.118–0.134 [0.094, 0.170]** — a 3.4× difference between two honest
measurements of the same quantity on different ladders. **REGRET is not a constant either; it
scales with the ladder** (longer/wider ladders leave more to lose). So PROTOCOL should require
regret to be **published per result**, not fixed at a number. The clause below is written that
way.

## F. The drafted PROTOCOL clause (for the Sunday review — this run does NOT edit PROTOCOL.md)

```
10. Selection results publish ROOM and REGRET, not the margin alone (proposed, idea 445).
    Any result that reports an in-sample chooser beating (or losing to) a comparand must
    publish, beside the margin, the two terms it decomposes into:

        MARGIN = OOS(pick) - OOS(control)  =  ROOM - REGRET
        ROOM   = OOS(best arm on the ladder) - OOS(control)   [a verdict on the CONTROL]
        REGRET = OOS(best arm on the ladder) - OOS(pick)      [>= 0; the SELECTOR's shortfall]

    ROOM is a property of the comparand and the dial; it changes when the comparand changes and
    says nothing about the selector.  REGRET is invariant to the comparand and is the only term
    selection controls.  A run may therefore not claim "selection helps" or "selection loses"
    from the margin alone: it must quote its own REGRET (there is no global constant -- the
    record's back-filled regret is 0.118-0.134 and the live 6-dial corpus's is 0.0387, because
    regret scales with the ladder), it must name the control's FAMILY (an unselected ARM of the
    same ladder, or a BOOK), and it must state the ladder length.  A column named `regret` means
    OOS(best arm) - OOS(pick) and nothing else; it is never negative.  The ladder and its
    per-arm OOS metrics are committed with the result so both terms are reconstructable.
```

The last two sentences are not decoration: 15.6% of the record's published regret values are
negative today, and 34–44% of SHAPE-W instances cannot be re-read at all because no per-arm grid
was committed.

## Caveats

* A re-reading of committed artefacts. Files with no grid CSV cannot be back-filled; the
  coverage fraction is published and those verdicts stand unaudited.
* A recovered ladder is an inference about the pool a run selected over; the reproduction
  certificate is the check, and results are reported at three thresholds.
* `OOS_best` is an oracle quantity, so ROOM is an upper bound on what any chooser could have
  won, not an achievable return.
* Instances are not independent (shared panels, prices, dials, books) — the bootstrap blocks on
  the instance and the file count is published beside it.
* SMALL439 is a **current-constituents** panel (`data/SMALL_PANEL_README.md`) with
  `max_1d_move >= 1.0` tickers dropped: **survivorship bias**, used as a shape check only, never
  as a tradable return.
* 10 bps is the protocol rung; 25 bps is carried as a robustness axis.
