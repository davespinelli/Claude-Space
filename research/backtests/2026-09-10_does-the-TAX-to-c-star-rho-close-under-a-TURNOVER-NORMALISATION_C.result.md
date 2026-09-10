# Idea 608 — does-the-TAX-to-c-star-rho-close-under-a-TURNOVER-NORMALISATION (lane C, 2026-09-10)

**Verdict: KILL — the queue's hypothesis is REFUTED, and refuted in the strongest available way:
every turnover normalisation makes the relation WORSE, not better.** Idea 605's
`rho(switch_tax, c*) = −0.5131` pooled becomes **−0.4102 … −0.4198** under all five base-turnover
normalisers (best **N6 = −0.4198**, a **gain of −0.0933**), against a pre-registered bar of +0.15 to
be called PARTIAL and 0.80 to be called CLOSED. The missing part is **not** the base book's turnover
level. It is the **zero-cost EDGE**: the analytic control `SLOPE / dSharpe_0` lands at
**rho = −0.9999** on the same 494 arms and **−0.9998 out of sample**. **Nothing promoted, no RULES
change, no PARK.** `RULES.md`, `PROTOCOL.md`, `scan.py`, `bot.py`, `baseline.py` untouched.

Script `2026-09-10_does-the-TAX-to-c-star-rho-close-under-a-TURNOVER-NORMALISATION_C.py`; console
`.console.txt`; artefacts `.arms.csv.gz` (648 arms × 60 columns), `.norms.csv` (the 10 normaliser
columns), `.rho.csv` (the full 16 × 10 rho table), `.censor.csv`, `.walkforward.csv`, `.picks.csv`
(54 rule-8 picks), `.cells.csv.gz` (1 944 arm × rung cells), `.refs.csv`. Runtime 3m45s, deterministic
(re-run bit-identical).

---

## 0. Gates — seven, all pre-registered, all printed before any new number was read

| Gate | Result |
|---|---|
| **G1** derived ladder `r_gate(c) = m·r0 − (c/1e4)(m·t0 + g·\|dm\|)` vs a live `engine.backtest(c)` through idea 399's own `apply_gate`, 7 rungs | **3.469e-18** (bar 1e-12) → PASS |
| **G2** fast numpy CAGR/Sharpe/MaxDD vs `engine.metrics`, 200 real series | **2.220e-16** → PASS |
| **G3** idea 605's committed `.drag.csv`, **all 648 arms** joined on switch_tax / timing / drag / dSharpe_0 / g_eff / on_share / switch_per_yr / c* | **max 5.684e-14**, +inf set identical, 648 of 648 matched → PASS |
| **G4** idea 605's **published** rho(tax, c\*) reproduced on its own censoring rule | POOLED **−0.5131** (n 494), ABS **−0.5950** (60), QEXP **−0.4117** (60), QROLL **−0.5614** (374) — all four exact to 4dp and to the row count → PASS |
| **G5** drag identity `DRAG == SWITCH_TAX + TIMING`, 648 arms | **2.168e-17** → PASS |
| **G6** the invariance (§2): group-constant normalisers leave the within-group rho unchanged | **0.000e+00** → PASS |
| **G7** `tax(g=1.00)/tax(g=0.75) == 4/3` exactly, while c\* is gross-stable | **2.220e-16** → PASS |

G4 is the one that matters: this run is a re-reading of idea 605's own 648 arms, not a different
vintage, and its headline is reproduced to the digit before anything new is computed.

**One thing idea 605 did not state, and should have.** Its −0.5131 is **censored**: it keeps only
arms with `0 < c* < ∞`, dropping **154 of 648** (90 that already lose at zero cost, 64 that still win
at 500 bps). The number is highly sensitive to that choice — see §3's censoring table, where the raw
tax reads −0.5131 / −0.2902 / −0.2443 / −0.3499 on four defensible rules. Any crossing-cost rank
statistic in the record must publish its censoring rule beside it.

## 1. Q1 — the queue's test. Every turnover normaliser LOSES

648 twin-pair arms (3 panels × 18 level-arms × 3 depths × 2 cadences × 2 gross), idea 605's exactly.
Tuned parameters, both named by the queue: **normaliser** (10 rungs, all reported) and **panel** (4,
all reported). Family, level, w, depth, gross, cadence, cost rung and censoring rule are reported
axes, never selected on.

Pooled (n = 494, idea 605's censoring):

| | N0 tax | N1 tax/g | **N2 tax/T_panel** | **N3 tax/T_panel,gross** | **N4 tax/mean(m·t0)** | **N5 tax/mean(Cs)** | **N6 tax/T_v2** | N7 drag | N8 drag/T | **N9 SLOPE/dSharpe_0** |
|---|---|---|---|---|---|---|---|---|---|---|
| **rho** | **−0.5131** | −0.5224 | −0.4102 | −0.4167 | −0.4100 | −0.4169 | −0.4198 | −0.5521 | −0.4950 | **−0.9999** |
| Δ\|rho\| vs N0 | — | +0.0094 | −0.1028 | −0.0964 | −0.1031 | −0.0962 | −0.0933 | +0.0391 | −0.0181 | **+0.4868** |

The five bold columns N2–N6 **are** the queue's proposal, on five different readings of "the base's
mean turnover per panel" (panel EWALL at g=1, the arm's own base book, the gate's realised base
turnover, the twin's realised turnover, and the live RULES v2 book's turnover). **All five move the
relation the wrong way, by about a tenth of a rho, and none comes near the 0.80 bar.**
**Pre-registered verdict: REFUTED.**

The reason is visible in the levels themselves: the three panels' base books churn **10.86% / 10.91%
/ 17.63% a year** (U56 / B136 / SMALL439). The widest ratio across panels is **1.62×**. There is
simply not enough cross-panel dispersion in the base's turnover for a per-panel divisor to be doing
useful work — and what little it does do, it does in the wrong direction, because it pulls the three
panels' tax distributions into more overlap precisely where their rho disagrees most (§2).

Per-family, pooled across panels, the same story: ABS −0.5950 → −0.4565…−0.4767, QEXP −0.4117 →
−0.2439…−0.2526, QROLL −0.5614 → −0.4534…−0.4704. Not one family improves.

## 2. Q2 — the invariance, and where the pooled −0.51 actually comes from

**A normaliser that is constant inside a group cannot change that group's Spearman at all.** A
per-panel divisor is by construction constant inside a panel. G6 measures it and gets **exactly
zero**: across N1 (per-gross), N2 (per-panel), N3 (per panel × gross) and N6 (RULES v2 per panel),
the largest change to any within-panel-×-gross rho is **0.000e+00**. Only the arm-level
normalisers — N4, N5, N7, N8, N9 — can move a within-panel number at all, and N4/N5 move it by
≤ 0.021.

So the queue's instrument is a **pooled-only instrument by construction.** And the pooled number is
where the −0.51 comes from — not the units:

| panel × gross | n | rho(tax, c\*) | rho(drag, c\*) | rho(SLOPE/dSharpe_0, c\*) |
|---|---|---|---|---|
| U56 g0.75 / g1.00 | 81 / 81 | **−0.7553 / −0.7558** | −0.8049 / −0.8054 | −0.9995 / −0.9993 |
| B136 g0.75 / g1.00 | 82 / 82 | **−0.7242 / −0.7285** | −0.7604 / −0.7640 | −0.9997 / −0.9999 |
| SMALL439 g0.75 / g1.00 | 84 / 84 | **−0.2967 / −0.2907** | −0.3162 / −0.3084 | −0.9999 / −1.0000 |
| **POOLED** | 494 | **−0.5131** | −0.5521 | −0.9999 |

**Two of the three panels already sit at −0.72 to −0.76 — far stronger than the published −0.51 —
and the pooled number is dragged down by SMALL439 at −0.30 and by the act of pooling itself.** The
record's "the tax orders c\* only moderately" is a statement about a pooled population, and the fix
for it is to quote the per-panel rho, which is the one number a per-panel normalisation provably
cannot touch.

G7 does clear the one units artefact that was really there: the tax scales **exactly** 4/3 with
gross (max |ratio − 4/3| = 2.2e-16) while c\* barely moves with it (median |Δc\*| **0.216 bps** over
292 finite pairs, max 4.33; max |ΔdSharpe_0| 1.0e-3, the weekly-drift residual). Stripping that axis
alone — N1, `tax/g` — is the **only** normalisation in the ladder that helps, and it helps by
**+0.0094**. The artefact was real and it was negligible.

## 3. Q3 — what the normalisation cannot reach: the EDGE

The ladder is linear in cost and the denominator vol nearly so, which makes the crossover an
explicit ratio:

    dSharpe(c) ≈ dSharpe_0 − (c/1e4)·252·[ mean(Cg)/vol_g − mean(Cs)/vol_s ]
    ⇒  c* ≈ dSharpe_0 / SLOPE ,   SLOPE = (252/1e4)·[ mean(Cg)/vol_g − mean(Cs)/vol_s ]

Accuracy of that approximation on the 494 arms: **rho(ĉ\*, c\*) = +0.99986**, median
|ĉ\*/c\* − 1| = **0.55%**. So c\* is, to within half a percent, *the zero-cost edge divided by a
vol-normalised drag* — and any tax-only statistic is missing the **numerator**:

| statistic | rho vs c\* |
|---|---|
| switch_tax | −0.5131 |
| drag | −0.5521 |
| SLOPE (vol-normalised drag) | −0.5240 |
| dSharpe_0 (the EDGE) | **+0.3620** |
| **SLOPE / dSharpe_0** | **−0.9999** |

Conditioning on the edge does what dividing by turnover does not. Inside equal-count dSharpe_0
quintiles:

| edge quintile | 1 (.0008–.018) | 2 (.018–.033) | 3 (.033–.049) | 4 (.049–.079) | 5 (.079–.236) | mean |
|---|---|---|---|---|---|---|
| rho(tax, c\*) | −0.6334 | −0.8635 | −0.9507 | −0.9442 | −0.8146 | **−0.8413** |
| rho(tax/T, c\*) | −0.5508 | −0.7970 | −0.9347 | −0.9292 | −0.8452 | −0.8114 |

**Mean within-edge-quintile rho(tax, c\*) is −0.8413 against a pooled −0.5131** — the tax *does*
order the crossover cost, once you stop comparing arms with different edges. The normalised tax is
worse inside every quintile but the last. The edge is the confounder; the turnover level is not.

**Censoring, reported on four rules and never tuned:**

| rule | n | N0 tax | N3 tax/T | N5 tax/mean(Cs) | N7 drag | N9 SLOPE/edge |
|---|---|---|---|---|---|---|
| idea 605's (0 < c\* < ∞) | 494 | −0.5131 | −0.4167 | −0.4169 | −0.5521 | **−0.9999** |
| finite only (c\* ≥ 0) | 584 | −0.2902 | −0.2221 | −0.2368 | −0.3276 | −0.3324 |
| all arms, +inf ranked top | 648 | −0.2443 | −0.1751 | −0.1827 | −0.3755 | −0.3460 |
| strictly inside 0–100 bps | 421 | −0.3499 | −0.2509 | −0.2543 | −0.3509 | −0.9998 |

The refutation is unanimous across all four: **the turnover normalisation is worse than the raw tax
on every censoring rule.** The identity N9 is near-perfect wherever c\* is an interior crossing and
degrades where it is not — which is the honest statement that a ratio identity says nothing about
arms that never cross.

## 4. Q4 — rule 8 on the claim itself

Every quantity (tax, drag, slope, edge, c\*) rebuilt **inside the IS window (≤ 2016-12-31) only**;
the normaliser is picked on IS by |rho| and read **once** on OOS (2017+).

| window | n | N0 | N1 | N2 | N3 | N4 | N5 | N6 | N7 | N8 | **N9** |
|---|---|---|---|---|---|---|---|---|---|---|---|
| IS | 186 | −0.4631 | −0.4671 | −0.4615 | −0.4684 | −0.4340 | −0.4485 | −0.4463 | −0.5686 | −0.5556 | **−0.9999** |
| **OOS** | 482 | **−0.4478** | −0.4581 | −0.2942 | **−0.2988** | −0.2805 | −0.2942 | −0.3279 | −0.5009 | −0.4401 | **−0.9998** |

- IS pick restricted to the queue's turnover set: **N3** (|rho_IS| 0.4684) → OOS **−0.2988**, against
  the raw tax's OOS **−0.4478**. **The chosen normalisation loses 0.1490 of rho out of sample.** The
  refutation walks forward.
- IS pick over all ten: **N9** (|rho_IS| 0.9999) → OOS **−0.9998**. **The analytic relation is the
  one thing here that is genuinely stable across windows**, and it needs no cost sweep to compute —
  every input is a zero-cost quantity.

## 5. Q5 — PROTOCOL: both KEEP paths and the book chooser

Both paths evaluated on all 648 arms at rungs 0 / 10 / 25 bps (1 944 cells, all reported in
`.cells.csv.gz`), against RULES v2 (live baseline) and SPY.

- **4a: 3 / 0 / 0 of 648** at 0 / 10 / 25 bps. **Zero at PROTOCOL's own rung**, consistent with idea
  605's ladder resolving 4a to a sub-7.5-bps phenomenon.
- **4b: 306 / 141 / 45 of 648.** Dominant failure legs at 10 bps: the whole bar at once (216), then
  CAGR alone (185), then DD alone (92).
- **Rule-8 book chooser** (IS Sharpe pick over level × w × depth, OOS read once, gross 0.75), 54
  picks = 3 panels × 3 families × 2 cadences × 3 rungs:

| rung | beats RULES v2 OOS | beats SPY OOS | 4a | 4b | mean OOS Sharpe | mean OOS CAGR | mean OOS MaxDD | mean regret |
|---|---|---|---|---|---|---|---|---|
| 0 | 3/18 | 12/18 | 1 | 11 | +0.9322 | +8.96% | −18.57% | −0.1193 |
| **10** | **1/18** | **12/18** | **0** | **2** | +0.8224 | +7.81% | −19.76% | −0.1218 |
| 25 | 1/18 | 12/18 | 0 | 0 | +0.6758 | +6.29% | −21.84% | −0.1135 |

The best pick at 10 bps (U56 QROLL q=0.17 w=504 d=1.00 D) reads **9.49% / 1.1535 / −13.64%** full
sample, halves **1.1789 / 1.1285**, OOS **10.05% / 1.2316 / −13.64%** — against RULES v2 U56 **8.63%
/ 1.2021 / −12.05%**, halves **1.2309 / 1.1798**, OOS **9.48% / 1.2788 / −12.05%**, and SPY **15.15%
/ 0.8855 / −33.72%**, halves **0.9587 / 0.8257**, OOS **15.32% / 0.8758 / −33.72%**. It loses to the
live book in both halves and out of sample; it beats SPY on Sharpe and drawdown and loses badly on
CAGR. **4a 0 of 18.**

**The 2 picks clearing 4b at the protocol rung are both B136 QEXP q=0.07 d=0.25 (D and W), and both
are bit-identical to the ungated parent** — `+0.1072 / +1.0261 / −0.1769`, halves
`+1.1456 / +0.9144`, OOS `+0.1058 / +1.0185 / −0.1769`, the same numbers as `NOGATE g0.75` on B136 to
4dp. The gate never fires. **Uninherited, non-degenerate protocol-rung 4b passes: 0.** This is the
same degenerate case idea 605 flagged, reproduced here independently.

_Survivorship: all three panels are current-constituent lists, so CAGR and drawdown LEVELS are
optimistic. The rank statistics this run is about are unaffected by a level shift common to an arm
and its twin. SMALL439 starts 2010-01-04, so its halves are not U56/B136's calendar halves._

## 6. What the record should do with this

1. **Do not add a turnover-normalised tax column.** It is worse than the raw tax on every panel,
   every family, all four censoring rules, and out of sample. The queue's premise — that the base
   book's churn level is the missing variable — is wrong, and the reason is measurable: the three
   panels' base books churn within a 1.62× band, which is not enough dispersion to matter.
2. **Quote c\* against `dSharpe_0 / SLOPE`, not against the tax.** The identity is exact to 0.55% in
   level, −0.9999 in rank, and −0.9998 out of sample, and every input is a **zero-cost** quantity —
   a crossing cost can be published without sweeping a cost ladder at all.
3. **Quote the per-panel rho, not the pooled one.** U56 −0.755 and B136 −0.724 against a pooled
   −0.513: idea 605's "moderate" ordering is largely a pooling artefact, and G6 proves no per-panel
   normalisation can ever change the per-panel numbers it would be defended with.
4. **Publish the censoring rule beside every crossing-cost rank statistic.** Idea 605's −0.5131 is
   −0.2443 with nothing dropped; 154 of 648 arms are excluded to get it.

Follow-ups filed: **610** (is SMALL439's −0.30 an edge-dispersion effect — the quintile conditioning
per panel), **611** (put a `ĉ* = dSharpe_0/SLOPE` column on every published crossing-cost claim and
census how many needed a cost sweep at all), **612** (census the record's censored rank statistics,
given −0.5131 → −0.2443).
