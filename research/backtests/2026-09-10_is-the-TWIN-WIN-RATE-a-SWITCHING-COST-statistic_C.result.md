# Idea 605 — is-the-TWIN-WIN-RATE-a-SWITCHING-COST-statistic (lane C, 2026-09-10)

**Verdict: SPLIT — CONFIRMED in LEVEL, REFUTED in ORDER.** The matched-gross twin win rate *is* a
switching-cost statistic: it falls monotonically at every one of 15 cost rungs (per-family Spearman
**−0.99 to −1.00**, pooled **−1.000**), the decay is carried by the switch tax, and — unlike idea
602's firing-rate relation, which flipped sign between halves — **it walks forward** (pooled OOS rho
**−1.0000**). But the queue's actual worry is **refuted**: the family ordering QROLL > QEXP > ABS is
**already fully present at ZERO cost** (spread **0.4167**) and **never inverts** — rho against the
0-bps order is **+1.000 at all 15 rungs, 0 → 100 bps**. Cost moves the *level* of the twin win rate,
never its *order*, so "a gate that fires is not merely a gross dial" is **not** a 10-bps-specific
claim. **No book promoted, no RULES change, no PARK.** `RULES.md`, `PROTOCOL.md`, `scan.py`,
`bot.py`, `baseline.py` untouched.

Script `2026-09-10_is-the-TWIN-WIN-RATE-a-SWITCHING-COST-statistic_C.py`; console `.console.txt`;
artefacts `.cells.csv.gz` (9 720 gated + 315 reference rows), `.drag.csv` (648 twin pairs),
`.walkforward.csv` (270 picks), `.ladder.csv`, `.ordering.csv`, `.stability.csv`, `.cadence.csv`,
`.claim.csv`, `.g3.csv.gz` (1 944 joined rows).

---

## 0. Gates — five, all pre-registered, all printed before any new number was read

| Gate | Result |
|---|---|
| **G1** derived ladder `r_gate(c) = m·r0 − (c/1e4)(m·t0 + g·\|dm\|)` vs a live `engine.backtest(c)` through idea 399's own `apply_gate`, **all 15 rungs** | **3.469e-18** (bar 1e-12) → PASS |
| **G2** fast numpy CAGR/Sharpe/MaxDD vs `engine.metrics`, 200 real series | **0.000e+00** → PASS |
| **G3** idea 602's committed `.cells.csv`, **all 1 944 gated rows** joined at rungs 0/10/25 | **4.857e-16** across dSharpe / Sharpe / twin_Sharpe / on_share / g_eff / dOOS / dMaxDD (U56 3.331e-16, B136 4.441e-16, SMALL439 4.857e-16) → PASS |
| **G4** idea 84's ungated EWALL U56 g=0.85 @10bps | 11.755% / 1.046 / −17.894% / H 1.073 / 1.025 vs published 11.8% / 1.05 / −17.9% / 1.07 / 1.04 → PASS |
| **G5** drag identity `DRAG == SWITCH_TAX + TIMING` on all 648 arms | **2.168e-17** (bar 1e-15) → PASS |

G1 is what makes the whole run cheap and exact: idea 399's overlay convention is *linear in cost*,
so a 15-rung ladder is derivable from one zero-cost pass with no approximation at all. G3 means
every number below is a re-reading of idea 602's own population, not a different vintage.

**CORRECTION to idea 602's memo.** It quotes ABS's twin win rate as **0.278** at 25 bps; its own
committed `.cells.csv` gives **0.287** — 31 wins of 108, in idea 602's own file and in this run's
recomputation alike (both 0.28703703…), so 0.278 is a transcription slip, not a data difference. Its
QEXP ladder, which the memo gave only at 10 bps, is **0.630 / 0.574 / 0.463** at 0/10/25. The
0.991 → 0.963 → 0.833 QROLL ladder is exact as published.

## 1. Population — idea 602's, with cost as the swept axis

648 twin pairs (3 panels × 18 level-arms [ABS 3 / QEXP 3 / QROLL 12] × 3 depths × 2 cadences × 2
gross) × **15 cost rungs** (0 / 1 / 2 / 3 / 5 / 7.5 / 10 / 15 / 20 / 25 / 30 / 40 / 50 / 75 / 100
bps) = **9 720 gated cells**, every point reported. Tuned parameters, both named by the queue:
**cost** and **cadence**. Depth, level, w, panel and gross are reported axes, never selected on.
Tie bar |dSharpe| ≤ 1e-12 (ideas 594/595): a tie is not a win.

## 2. Q1 — the ladder. CONFIRMED, and it is steep

| rung (bps) | 0 | 1 | 2 | 3 | 5 | 7.5 | **10** | 15 | 20 | **25** | 30 | 40 | 50 | 75 | 100 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **ABS** | .574 | .574 | .574 | .556 | .537 | .500 | **.481** | .444 | .398 | .287 | .222 | .185 | .111 | .074 | .056 |
| **QEXP** | .630 | .630 | .630 | .630 | .602 | .574 | **.574** | .519 | .481 | .463 | .444 | .426 | .370 | .204 | .148 |
| **QROLL** | .991 | .988 | .984 | .981 | .977 | .972 | **.963** | .917 | .889 | .833 | .741 | .634 | .477 | .278 | .213 |
| **POOLED** | .861 | .860 | .856 | .852 | .841 | .827 | **.818** | .772 | .739 | .681 | .605 | .525 | .398 | .231 | .176 |

Pre-registered bar (every adjacent step non-increasing **and** per-family Spearman ≤ −0.80): **0 up
steps in any family**, rho **−0.9964 / −0.9901 / −1.0000** (ABS / QEXP / QROLL), pooled **−1.0000**.
**Q1 CONFIRMED.** The 0 → 100 bps span is 0.519 / 0.482 / 0.778, pooled 0.685 — bigger than any
other dial the record has put beside a twin claim, idea 602's rate included.

The **crossing cost** is the number the record should be quoting, because two of the three families
cross inside the range a real book pays:

| family | win @ 0 | win @ **10 (PROTOCOL)** | first rung < 0.50 |
|---|---|---|---|
| ABS | 0.574 | **0.481** | **10 bps** |
| QEXP | 0.630 | 0.574 | 20 bps |
| QROLL | 0.991 | 0.963 | 50 bps |

**At PROTOCOL's own cost rung, idea 42's ABS family no longer beats its matched-gross twin at all
(0.481 — a coin flip).** Any ABS twin claim in the record is a zero-to-five-bps claim.

## 3. Q2 — the deciding test: the ORDERING is not a cost artefact

| rung | 0 | 1 | 2 | 3 | 5 | 7.5 | 10 | 15 | 20 | 25 | 30 | 40 | 50 | 75 | 100 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| top family | QROLL | QROLL | QROLL | QROLL | QROLL | QROLL | QROLL | QROLL | QROLL | QROLL | QROLL | QROLL | QROLL | QROLL | QROLL |
| bottom | ABS | ABS | ABS | ABS | ABS | ABS | ABS | ABS | ABS | ABS | ABS | ABS | ABS | ABS | ABS |
| **rho vs the 0-bps order** | **+1.000** at every single rung |

- **leg (a)** — spread at c = 0 ≤ 0.10? **FALSE**: the spread is **0.4167** *before a basis point is
  charged*, and it *widens* to 0.546 at 25 bps before narrowing as every family collapses.
- **leg (b)** — does the ordering invert anywhere on 0–100 bps? **FALSE**: min rho **+1.000**.
- **=> the family ordering is NOT a switching-cost ranking.** The queue's inference — that the
  record's "a gate is only a gross dial" claims are 10-bps-specific — **does not follow**. They are
  cost-specific in *magnitude* and cost-invariant in *sign and order*.

Arm-level, not just family-level: Spearman of the 648 arms' dSharpe against their 0-bps ranking is
**0.9643 at 10 bps** and 0.7934 at 25 (sign agreement 0.957 / 0.819). Inside the tradable band the
ladder re-scales the comparison; it does not re-order it. Only past ~40 bps does the ranking
dissolve (rho 0.565 at 40, 0.414 at 50, 0.029 at 100).

## 4. Q3 — mechanism: the tax carries the DECAY, and explains none of the ORDER

The drag splits exactly (G5, 2.2e-17) into `SWITCH_TAX = g·mean|dm|` and
`TIMING = mean(m·t0) − mean(t0(g_eff))`, the base turnover the gate avoids by being de-grossed:

| family | n | switches/yr | tax | timing | drag | tax/\|drag\| | median c\* |
|---|---|---|---|---|---|---|---|
| ABS | 108 | 4.13 | +0.00716 | −0.00272 | +0.00353 | 1.647 | 8.2 bps |
| QEXP | 108 | 0.96 | +0.00137 | −0.00077 | +0.00053 | 1.578 | 18.3 bps |
| QROLL | 432 | 3.37 | +0.00542 | −0.00240 | +0.00292 | 1.759 | 50.0 bps |

TIMING is real and always the right sign (de-grossing *does* save the base's own turnover cost) but
it is ~40% of the tax and almost never decisive: it carries the sign of the drag in **9.3%** of arms
and exceeds the tax in **5.6%**. So the **decay is a switching-cost effect** — the queue is right
about the mechanism.

It is not, however, a *sufficient* statistic. At **matched switch tax** (equal-count quintiles, 10
bps) the family label survives with a **median within-bucket gap of 0.576, max 0.812** — in the
highest-tax bucket ABS wins 0.188 while QROLL wins 0.894 *paying the same tax*. And pooled
AUC(switch_tax → win) at 10 bps is **0.5103**, i.e. nothing (drag 0.5292, on_share 0.5592, g_eff
0.5374 — none of them orders it). The tax orders the crossover cost only moderately: rho(tax, c\*)
**−0.51** pooled (−0.60 / −0.41 / −0.56 by family). **Switching cost sets how fast a gate's twin
edge dies; it does not set which gate has one.**

## 5. Q4 — cadence, the experimental handle on the switch count

Weekly cadence caps the dial at the rebalance grid while the *signal is unchanged*, so it is a
direct manipulation of the switch count:

| family | switches/yr D : W | ratio | decay 0→100 D : W | ratio | median c\* D : W |
|---|---|---|---|---|---|
| ABS | 6.24 : 3.18 | 1.96× | +0.593 : +0.444 | 1.33× | 5.7 : 16.8 bps |
| QEXP | 1.41 : 0.77 | 1.83× | +0.593 : +0.370 | 1.60× | 17.1 : 40.3 bps |
| QROLL | 4.88 : 1.87 | 2.61× | +0.972 : +0.583 | 1.67× | 36.8 : 97.7 bps |

The direction is the switching-cost story's (more switches → faster decay, ~3× the crossover cost
for W), but the decay ratio is consistently *smaller* than the switch ratio, so the tax is a partial
explanation here too. The practical reading: **QROLL on weekly cadence still wins 0.398 of its twin
comparisons at 100 bps, where daily QROLL is at 0.028.** Cadence is the cheapest available defence
of a twin claim, and the record does not quote it beside one.

## 6. Q5 — PROTOCOL KEEP paths and rule 8

**4a: 14 of 9 720, and every one of them is below 7.5 bps.** All 14 are B136 QROLL q=0.17 g=0.75 at
rungs 0/1/2/3/5 — the same shape idea 602 found at rung 0 alone, now resolved to a cut-off. **At
PROTOCOL's 10 bps and above, 4a is ZERO on every panel, family, depth, cadence and gross.**

**4b: 1 958 of 9 720**, and it is a cost-and-inheritance artefact: 306 / 141 / 45 / 0 at 0 / 10 / 25
/ 50 bps, while B136 g=0.75's *ungated parent* passes 4b on its own through 10 bps and U56 g=0.75's
through 5 bps. Dominant failure mode is the whole bar at once (4 360 rows fail H1,H2,OOS,DD,CAGR),
then CAGR alone (1 077) and DD alone (870).

**Rule 8** (chooser over level × w × depth on IS ≤ 2016-12-31 Sharpe, OOS 2017+ read once, g=0.75),
270 picks = 3 panels × 3 families × 2 cadences × 15 rungs:

| rung | 0 | 5 | **10** | 25 | 50 | 100 |
|---|---|---|---|---|---|---|
| beats its own ungated parent OOS | 12/18 | 11/18 | 11/18 | 10/18 | 6/18 | 4/18 |
| mean OOS Sharpe vs parent | +0.037 | +0.025 | +0.016 | +0.004 | −0.017 | −0.017 |
| beats its own twin OOS | 0.667 | 0.611 | 0.611 | 0.556 | 0.333 | 0.222 |
| 4b passes | 11 | 7 | **2** | 0 | 0 | 0 |
| 4a passes | 1 | 1 | **0** | 0 | 0 | 0 |

Over all 270 picks: beats SPY OOS **133**, beats **RULES v2 OOS 23**, mean regret **−0.1123**. The
**2 picks clearing 4b at the protocol rung are both B136 QEXP q=0.07 d=0.25 with `vs_nogate` and
`OOS_dSharpe` EXACTLY 0.0000** — idea 602's degenerate never-fires case, bit-identical to a parent
that passes 4b on its own. **Uninherited, non-degenerate protocol-rung rule-8 4b passes: 0.
Nothing to promote.** The chooser's *pick* is cost-stable in only half the cells: unchanged across
the whole ladder in **9 of 18** choosers (median 1.5 distinct picks, max 5).

**Rule 8 on the claim itself** is the sharpest result in the run, and it is the exact opposite of
idea 602's:

| | ABS | QEXP | QROLL | POOLED |
|---|---|---|---|---|
| IS rho(cost, win rate) | −0.9865 | +0.4330 | −0.9213 | −0.8418 |
| **OOS rho** | **−0.9964** | **−0.9901** | **−0.9874** | **−1.0000** |
| IS span 0→100 | +0.259 | −0.148 | +0.296 | +0.216 |
| **OOS span** | **+0.435** | **+0.407** | **+0.653** | **+0.576** |

Idea 602 found the *rate* relation flipped sign between windows in every family. The **cost**
relation does not: it is monotone in both windows, stronger out of sample than in, and pooled OOS
rho is a perfect −1.000. This is a stable relation and can be used to re-price the record.

One honest caveat in the other direction: the *ordering* is cost-invariant but **not
window-invariant.** Ranked on the IS window alone the families read ABS < QROLL < QEXP; on OOS they
read QEXP < ABS < QROLL (rho −0.500). The full-sample ordering QROLL > QEXP > ABS holds at all 15
rungs; the half-window orderings disagree with each other. A twin claim quoted on one window is
weaker than the cost ladder that prices it.

## 7. What the record should do with this

1. **Publish the crossing cost beside every twin claim, not just the 10-bps win rate.** ABS crosses
   0.50 at **10 bps**, QEXP at **20**, QROLL at **50**. A claim whose crossing cost sits at the rung
   it was measured on is a claim about execution, not about timing.
2. **Do not re-read the record's "a gate is only a gross dial" verdicts as cost artefacts.** The
   family ordering is present at zero cost (spread 0.4167) and invariant across 0–100 bps
   (rho +1.000 at all 15 rungs); arm-level rank stability is 0.964 at 10 bps.
3. **Quote cadence.** Weekly cadence roughly triples a gate's crossover cost at an unchanged signal.
4. Idea 602's memo's ABS-at-25-bps figure is **0.287**, not 0.278 (§0).

Follow-ups filed: **607** (crossing-cost column across the record's committed twin claims),
**608** (does the tax→c\* rho of −0.51 close under a per-panel turnover normalisation), **609**
(is the twin ordering window-invariant on a rolling-window census, given the IS/OOS rho of −0.500).

_Survivorship: all three panels are current-constituent lists, so CAGR and drawdown LEVELS are
optimistic; the gate-minus-twin contrast and its cost slope are the durable part. SMALL439 starts
2010-01-04, so its halves are not U56/B136's calendar halves, and w=2016 spends half its sample
unarmed. Research, not investment advice._
