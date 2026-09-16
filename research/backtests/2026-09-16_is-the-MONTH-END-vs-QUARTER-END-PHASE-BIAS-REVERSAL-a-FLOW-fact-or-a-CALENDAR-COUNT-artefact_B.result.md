# Idea 974-MEQE (lane B, 2026-09-16) — is the MONTH-END vs QUARTER-END phase-bias REVERSAL a FLOW fact or a CALENDAR-COUNT artefact?

> **Numbering note (defect 932).** Two different ideas carry the number 974. This is the QUEUE line
> `is-the-MONTH-END-vs-QUARTER-END-PHASE-BIAS-REVERSAL-a-FLOW-fact-or-a-CALENDAR-COUNT-artefact`
> (filed 2026-09-15 by idea 964), **not** the CHANGELOG's 974
> `should-every-PHASE-CHOOSING-CLAIM-carry-its-FAMILY-S-OWN-BLIND-BASE-RATE`, which the cloud lane
> answered on 2026-09-15. Cited here as **974-MEQE**.

## ANSWERED = **FLOW FACT.** The reversal survives the calendar-count control, and it is a QUARTER-END fact, not a month-end fact.
## But **KILL** for trading it: the effect is real, stable and *not in-sample learnable*. **KILL** for 4a. **PARK** the one low-turnover book it surfaces.

Nothing promoted. `RULES.md`, `PROTOCOL.md`, `scan.py`, `bot.py`, `baseline.py` untouched (rule 6).

---

## What was asked

Idea 964 published, over 60 committed families at 10 bps, that the canonical rebalance phase
(period-end, `d = 0`, the day `engine.rebalance_mask` produces and the only day the live rules trade)
sits at the **0.929** percentile of its own 21-phase family MONTHLY (**+0.600 pp** CAGR over the family
mean) and at the **0.063** percentile of its own 63-phase family QUARTERLY (**−1.112 pp**). The two
cadences' canonicals are biased in opposite directions and 964's pooled `H_BIAS` passed only by
cancellation. The queue's suspicion: a 63-phase quarterly family spans **three** month-ends and a
21-phase monthly family **one**, so the quarterly canonical might just be one of three month-end-like
days losing in a comparison set three times as wide — a **calendar-count artefact**.

## What was measured

**12,600 grid rows** rebuilt from scratch (3 panels × 5 books × 2 gross × (21 M + 63 Q) phases × 5 cost
rungs), **600 CALEND arm rows**, **150 family × rung decomposition cells**, **150 null-percentile rows**
and **900 rule-8 walk-forward rows**. TUNED 2, exactly as the queue line allows: **DECOMPOSITION**
(FULL / BLOCK0 / MPOS / CALEND) and **PANEL** (U56 / B136 / SMALL); all levels printed, neither chosen.

## Gates: 9 of 10 PASS — and the one FAIL is a finding about the record, not about this run

| gate | result |
|---|---|
| G0 `offset_mask(·,per,0)` == `engine.rebalance_mask` on M/Q/W | **PASS**, 0 rows |
| G1 fast `Ctx` == `engine.backtest` | **PASS**, returns 6.94e-18 / turnover 1.67e-16 |
| G2 BAND03@0.75 == `baseline.rules_v2_weights` | **PASS**, 0.000e+00 |
| G3 964's committed grid replayed **on today's data** | **FAIL**, max&#124;d&#124; 5.349e-02 |
| G3b the same replay **on 964's own data vintage** (`c22e4d3`) | **PASS**, 4,200 of 4,200 U56 rows × 13 cols, max&#124;d&#124; **1.776e-15** |
| G4 CALENDAR IDENTITY: `MEND_Q3` == `offset_mask(idx,"Q",0)` | **PASS**, 0 rows |
| G5 964's published headline recomputed from its own grid | **PASS**, M +0.600 pp / 0.929, Q −1.112 pp / 0.063, max&#124;d&#124; 4.9e-04 |
| G6 `MEND_Q1/Q2/Q3` pairwise disjoint, each 4.02/yr (`MEND_ALL` 12.05) | **PASS** |
| G7 MOD21 is APPROXIMATE, measured not assumed | **PASS** (below) |
| G8 determinism, subject family rebuilt from scratch | **PASS**, 0.000e+00 |

**G3's failure is DATA, not code.** `data/prices.csv` was **restated across its entire history** by the
nightly close action between 964's commit and this run — max |d| **8.96** (BTC-USD), **UNH by 3.67** — on
**4,704 shared rows**, plus one new trading day (2026-09-14 → 2026-09-15). Consequence for the record:
**no committed grid is byte-reproducible on a later calendar day**; 964's own G3 passed at 1.78e-15 only
because it ran against 962 the same day. G3b removes the vintage and the code reproduces exactly.
Nothing this run reports moves with it — the canonical's Q percentile reads **0.0635 on both vintages**.

**G7 — the queue's own arithmetic is approximate, and that is why the exact arms exist.** Of each
mod-21 phase's 71 rebalance dates, the share that are *true* month-ends: phase 0 **1.000**, phase 21
**0.366** (mean month-phase 8.44), phase 42 **0.465** (mean 4.97). `d mod 21` is a weak proxy for
"position within the month" at quarterly cadence, so the CALEND arms rebalance on the last trading day
of the 1st / 2nd / 3rd month of each quarter exactly, four times a year in every arm.

---

## (1) The reversal SURVIVES the calendar-count control — `H_COUNT` **FAIL**

Median within-family CAGR percentile of the canonical, 30 families at 10 bps:

| decomposition | competitors | median percentile of the canonical |
|---|---:|---:|
| `M_FULL` (964, monthly) | 21 | **0.9286** |
| `Q_FULL` (964, quarterly) | 63 | **0.0635** |
| **`Q_BLOCK0` (width-matched: the 21 days of the quarter's final month)** | **21** | **0.1190** |
| `Q_MPOS` (within-month profile, averaged over the 3 blocks) | 21 | 0.5476 |

Cutting the comparison set from 63 competitors to 21 moves the quarter-end from the 6th percentile to
the **12th**, not past the 50th. **`H_COUNT` FAILS at 0.1190** (bar > 0.50). Stable on every axis: all
five cost rungs give 0.1190 identically; by panel B136 0.3571 / SMALL 0.1190 / U56 0.1190; by book
0.0238 (BAND03) to 0.3571 (EWELIG) — **no cell reaches 0.50.** The width of the family is not the story.

## (2) Month-end-ness is still GOOD — but not in the quarter's last month. `H_MEND` **PASS**

Where `m = 0` (the month-end) sits inside each block of the quarter:

| block | median percentile of `m = 0` | median block mean CAGR |
|---|---:|---:|
| 0 — last month (**contains the quarter-end**) | **0.1190** | 11.70% |
| 1 — middle month | **0.6905** | 13.94% |
| 2 — first month | **0.8333** | 11.78% |

`H_MEND` **PASSES at 0.6905 / 0.8333**. Month-end is an above-median rebalance day in two of three
months of the quarter, matching the monthly family's 0.9286 in direction. It is a bottom-decile day in
exactly one: the month whose end *is* the quarter-end.

## (3) The exact arms, and `H_QEND` **PASS** / `H_TRADE` **PASS** / `H_NULL` **PASS**

30 families, 10 bps, medians. Every arm is 4 rebalances a year on a true month-end; `MEND_ALL` (12/yr)
is the cadence reference. `MEND_Q3` ≡ the canonical quarterly phase (G4).

| arm | CAGR | Sharpe | MaxDD | OOS CAGR | OOS Sharpe | OOS MaxDD | turn/yr | 4b | 4a |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `MEND_Q1` (1st month of Q) | 14.37% | 1.0480 | −30.35% | 14.44% | 1.0256 | −30.35% | 3.36 | **0/30** | 0 |
| `MEND_Q2` (2nd month of Q) | 12.98% | **1.0981** | −27.88% | 14.67% | 1.0134 | **−27.88%** | 3.48 | **3/30** | 0 |
| **`MEND_Q3` (quarter-end — what the live rules trade)** | **11.47%** | **0.9396** | **−31.70%** | **11.08%** | **0.7960** | **−31.70%** | 3.41 | **0/30** | 0 |
| `MEND_ALL` (every month-end, 12/yr) | 12.11% | 1.0783 | −28.02% | 12.89% | 1.0028 | −28.02% | 6.76 | 3/30 | 0 |

- **`H_QEND` PASS at 0.8667** — the quarter-end has the lowest full-sample CAGR of the three arms in
  **26 of 30** families against a chance rate of 0.3333. The ordering is **identical at all five cost
  rungs** (0 / 5 / 10 / 25 / 50 bps), so it is not a turnover rebate.
- **`H_TRADE` PASS at 1.0000** — best(Q1,Q2) beats Q3 on OOS Sharpe in **30 of 30** families.
- **`H_NULL` PASS at 0.9127** — and this is the gate that matters, because every one of the 63 mod-21
  quarterly phases is *also* a 4×/yr book on the same panel, book and gross, so that family **is** the
  null for "which day of the quarter do you rebalance". Median CAGR percentile inside it:
  `MEND_Q2` **0.9127** (OOS Sharpe pctile 0.9286), `MEND_Q1` 0.8413 (0.6508), `MEND_Q3` **0.0635**
  (0.1587). For scale, the family's own CAGR spread has median **4.38 pp** and the Q2 − Q3 gap is
  **1.51 pp** — real, and about a third of the dial's width.

**`H_FLOW` PASSES.** The reversal is a flow fact: month-ends are good rebalance days, the quarter-end
is not, and the family-width control does not explain it.

## (4) Rule 8 walk-forward — **and this is where it dies**

Arm chosen on **2009–2016 alone** by two IS-only choosers; **2017–2026 read once**. 60 picks at 10 bps.

| chooser | n | med OOS CAGR | med OOS Sharpe | med OOS MaxDD | 4b REC | 4b PURE | 4a |
|---|---:|---:|---:|---:|---:|---:|---:|
| `C_CAGR` (IS CAGR) | 30 | 12.99% | **0.8570** | −29.00% | **1/30** | 1/30 | **0/30** |
| `C_SHARPE` (IS Sharpe) | 30 | 12.99% | **0.8453** | −29.00% | **1/30** | 1/30 | **0/30** |
| `FIXED_MEND_Q2` | 30 | 14.67% | 1.0134 | −27.88% | 3/30 | 3/30 | 0/30 |
| `FIXED_MEND_ALL` | 30 | 12.89% | 1.0028 | −28.02% | 3/30 | 3/30 | 0/30 |
| `FIXED_MEND_Q1` | 30 | 14.44% | 1.0256 | −30.35% | 0/30 | 0/30 | 0/30 |
| `FIXED_MEND_Q3` | 30 | 11.08% | 0.7960 | −31.70% | 0/30 | 0/30 | 0/30 |
| **SPY (OOS)** | | **15.33%** | **0.8769** | **−33.72%** | | | |
| **RULES v2 (OOS)** | | | **1.1061** | **−12.24%** | | | |

**Eight years of history cannot find the arm.** The IS choosers pick `MEND_Q1` — the **0-of-30** arm —
**16 of 30** times, and `MEND_Q3` — the arm this run just showed is the worst day of the quarter —
**8–10** times; `MEND_Q2`, the 3-of-30 arm, only **4–6** times. The chooser's median OOS Sharpe
(**0.8570**) lands *below* every fixed arm except the quarter-end itself, and below a parameter-free
`MEND_ALL` (1.0028). This reproduces ideas 962 / 964-BASERATE on a dial neither touched: **choosing a
rebalance day in sample is worse than not choosing one.** 2 of 60 at 10 bps, and **2 of 60 at every
rung** (0/5/10/25/50 bps).

**4a is 0 of 600 arm rows and 0 of 60 picks.** No arm on any panel comes near the live book's −12.24%
OOS drawdown; `L4_DD` is the sole failing leg on 20 of the 60 picks and appears in 56 of the 58 failures.

## (5) The one object worth parking

`U56 / EWELIG / gross 0.75 / MEND_Q2` — equal-weight every eligible name, rebalanced **four times a
year on the middle month-end of each quarter**: full **13.00% / 1.2162 / −17.51%**, halves
**1.2514 / 1.1915**, OOS **13.96% / 1.2597 / −17.51%**, at **1.80 turns/yr**, against SPY
**15.10% / 0.8830 / −33.72%** (halves 0.9591 / 0.8208) and OOS **15.21% / 0.8713 / −33.72%**. It clears
4b on both conventions and is the **one** family the IS chooser gets right. Same book at `MEND_ALL`
(12/yr): 11.78% / 1.1382 / −17.01% at **3.64** turns/yr — half the turnover buys 1.2 pp of CAGR and
0.08 of Sharpe. **PARK, not KEEP:** 4a fails (−17.5% against −12.2%), it is one cell of thirty, its
arm is not IS-learnable (§4), and the two BAND03 passers at the same arm do not survive the switch to
`MEND_Q1` at all.

---

## The clause this proposes, for Sunday review and NOT written into `PROTOCOL.md` (rule 6)

> *"A canonical-phase statistic is quoted per cadence, never pooled across cadences. Month-end and
> quarter-end are different objects: the monthly canonical sits at the 0.93 percentile of its own
> family and the quarterly canonical at 0.06, and that gap survives a width-matched control
> (0.12 on 21 competitors). Any claim that a period-end is a good or bad rebalance day names the
> period. Separately: a cross-run gate against a committed grid must replay the data vintage that grid
> was built on — `data/prices.csv` is restated across its whole history nightly, so a same-code replay
> on a later day disagrees at 5.3e-02."*

Cost of adoption: zero re-runs; one `git show <commit>:data/prices.csv` in any cross-run gate.

## Survivorship (rule 9)

U56 / B136 / SMALL are **current-constituent** lists (SMALL additionally drops the 52 tickers with
`max_1d_move` ≥ 1.0 per `data/small_meta.csv`, leaving 663 names + SPY as benchmark). Every CAGR and
drawdown **level** above is optimistic, most severely on SMALL. The entire subject of this run is the
**same names on the same tape rebalanced on different days**, so every percentile, ordering and
arm-vs-arm contrast is very nearly immune to it. The 4b levels are read against SPY, which is not
survivorship-inflated, so the 6 full-sample and 6 OOS passes are **upper bounds** and every FAIL is
understated. 2009–2026 holds only two real stress tests (2020, 2022) in a QQQ-favourable regime, and
`MEND_Q2`'s edge over `MEND_Q3` rests on ~68 rebalance dates per arm.
