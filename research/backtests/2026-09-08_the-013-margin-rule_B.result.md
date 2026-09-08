# Idea 241 — the 0.013 margin rule (lane B, 2026-09-08)

**Verdict: KILL.** A minimum-margin abstention rule does not beat the raw IS argmax out of
sample. Every one of the three walk-forwards flips the sign of the effect, and the effect
that exists in sample is not a margin effect at all — it is the ROOM the control arm
carries. Nothing promoted. RULES.md, scan.py, bot.py, baseline.py, PROTOCOL.md untouched.

## The headline, in one table

| where | how the rule was chosen | in-sample D | out-of-sample D |
|---|---|---|---|
| **WF1** record, split by parent-file date | (q, norm) on files < 2026-09-06 | **+0.0334** (rng/q0.8, t +10.9, n 658) | **−0.0017** (t −0.97, p 0.33, n 1,176) |
| **WF2** record → fresh live corpus | best record point (rng/q0.6) | +0.0113 | **−0.0266** (n 1,200) |
| **WF3** nested live: arms 2010–13, τ on 2014–16, read 2017+ | raw/q0.9, τ 0.0543 | +0.0749 | **−0.0329** |

`D(τ) = mean[ OOS_Sharpe(selector) − OOS_Sharpe(raw argmax) ]`, so `D(0) ≡ 0` and the raw
argmax is its own control. **Positive in sample every time, negative or nil every time it is
read out of sample.**

## Corpus

* **PART A — census.** 1,909 committed `research/backtests/*.csv` scanned → **92 ADMITTED**
  (1,413 no arm column, 315 no matched IS/OOS pair, 89 no usable cell; ledger committed).
  **11,530 (file × cell × metric) rows, 5,057 distinct cells, of which 4,925 Sharpe cells
  over 89 files.** Cells are found mechanically by idea 417's `id_columns`, reused verbatim
  so the two censuses are comparable. 1,834 Sharpe cells carry a labelled control arm; the
  argmax **is** the control in 631 of them (12.8%), where abstention is a no-op by
  construction.
* **PART B — fresh live corpus**, sharing no data with the record: 31 arms (band × gross ×
  cadence + an ungated control) × 3 panels × 2 cost rungs = 186 arm-rows, and **1,200 seeded
  sub-menus** as selection cells.

**Tuned parameters: exactly 2** — `q` (the threshold as a quantile of the calibration set's
own gap distribution, 10 values) × `norm` ∈ {raw, z, rng}. **All 30 grid points reported**,
at each of 3 incumbent definitions, in `.taugrid.csv` and `.taugrid_live.csv`. Metric pinned
at Sharpe by the queue's wording; CAGR/MaxDD/Calmar are a labelled sensitivity, not a third
dial. The queue's own τ = 0.013 raw is carried as a **pre-registered** point beside the grid.

## Gates (passed before any new number was read)

| gate | requirement | result |
|---|---|---|
| G1 | cost-rung identity `net(c) = gross − TO·c/1e4` vs a direct 25 bps backtest | **0.000e+00** |
| G2 | idea 431's degeneracy claim: its 36 dial pools all have a top-2 IS gap < 0.15 | **36/36 (100%)**, max gap 0.0786, median 0.0242 — **reproduced** |
| G3 | the queue's τ = 0.013 is carried, not fitted | idea 77's two levels are quoted from the queue, not recomputed |

G2 is why this run does not use an absolute τ ladder: on a corpus whose gaps top out at
0.079, any ladder reaching 0.10 is vacuous. Defining τ as a **quantile of the corpus's own
gaps** removes that failure mode, and the rule still loses.

## Why the in-sample effect exists (and is not the margin)

Against the **control** incumbent, D rises monotonically with τ to about **+0.011** at
rng/q0.6 on the record. Against the **IS-median** arm it is **negative at all 27 non-zero
grid points** (−0.003 → −0.029), and against the **menu mean** likewise (−0.003 → −0.031).
**The incumbent's identity, not the margin, sets the sign** — the same control-vocabulary
artefact ideas 229 and 445 named.

The decomposition says exactly why (1,834 control-carrying cells):

| term | mean | t |
|---|---|---|
| ROOM the control carries, `OOS_ctl − OOS_mean` | **+0.0258** | +22.2 |
| what the argmax buys, `OOS_star − OOS_mean` | +0.0201 | +11.8 |
| argmax vs control, `OOS_star − OOS_ctl` | **−0.0058** | −3.2 |
| oracle regret, `OOS_best − OOS_star` | +0.0478 | +26.9 |

The control is simply a better-than-average arm in these grids. Any rule that hands cells
back to it collects that room, **whether or not the margin carries information** — which is
why D grows with the abstention rate rather than with any property of the gap.

## The decisive test: does the margin *sort* the payoff?

`gain(cell) = OOS_ctl − OOS_star` — what abstaining on that cell actually pays. If the
queue's rule is real, gain must **fall** with the margin. On the record's 1,203 MOVED cells:

| norm | narrow | mid | wide | Spearman(margin, gain) |
|---|---|---|---|---|
| raw | +0.0093 | **+0.0242** | −0.0072 | **−0.024** |
| z | +0.0145 | **+0.0189** | −0.0071 | −0.037 |
| rng | +0.0138 | **+0.0292** | −0.0166 | −0.111 |

**Non-monotone, and the rank correlation is ~0.** The middle tercile pays *more* than the
narrow one, so a *minimum*-margin threshold is the wrong shape: the only ordered fact is
that the WIDE tercile is negative, i.e. the sortable statement is "do not abstain when the
gap is wide", not "abstain when it is narrow". On the live u56 cells the gain is **negative
in all three terciles** (−0.125 / −0.122 / −0.138) with Spearman **−0.536** — the margin
does sort there, in the direction opposite to the queue's rule. The sign of the sort is
corpus-dependent; the rule is not.

The pre-registered τ = 0.013 lands at the **40.6% quantile** of the record's own gaps
(it would abstain on 40.6% of cells) and gives D **+0.0030** vs the control, **−0.0049** vs
the median arm, **−0.0074** vs the menu mean — and does not survive WF1 either.

## Live books (PROTOCOL 10 bps anchor, OOS = 2017-01-01..)

τ chosen on 2014–2016 and read once on 2017+: raw/q0.9, τ = 0.0543.

| panel | book | OOS CAGR | OOS Sharpe | OOS MaxDD |
|---|---|---|---|---|
| u56 | **ARGMAX** | 11.79% | **1.2743** | −15.53% |
| u56 | ABSTAIN | 18.47% | 1.1353 | −29.18% |
| u56 | INCUMBENT | 18.47% | 1.1353 | −29.18% |
| u56 | RULES v2 (live) | 9.53% | 1.2851 | −12.05% |
| u56 | SPY | 15.45% | 0.8820 | −33.72% |
| broad136 | ARGMAX = ABSTAIN = INCUMBENT | 18.59% | 1.1006 | −32.72% |
| broad136 | RULES v2 / SPY | 7.98% / 15.45% | 1.1185 / 0.8820 | −12.24% / −33.72% |
| small439 | ARGMAX = ABSTAIN = INCUMBENT | 12.88% | 0.6351 | −46.03% |
| small439 | RULES v2 / SPY | 3.85% / 15.45% | 0.5680 / 0.8820 | −14.68% / −33.72% |

**ABSTAIN beats ARGMAX on OOS Sharpe in 0 of 6 (panel, cost) books**, mean −0.0414; where it
moves at all (u56) it costs **−0.139 of Sharpe and doubles the drawdown** (−15.5% → −29.2%)
to buy +6.7 pp of CAGR — a pure de-risking-in-reverse trade, not a selection improvement.

**COVERAGE LIMIT, reported not buried:** on broad136 and small439 the ungated control is the
IS-Sharpe argmax in **400 of 400** sub-menus, so the abstention rule is a strict no-op on
two of the three live panels. The live evidence is a **u56-only** result (400 cells, 23%
of them moved).

## KEEP paths

* **Books: 4a 0/18, 4b 2/18, 4a(OOS) 0/18, 4b(OOS) 2/18, BOTH 0/18.** The two 4b passes are
  the **ARGMAX** book on u56 at 10 and 25 bps — the object under test (ABSTAIN) is **0/6 on
  both paths**, as is the INCUMBENT.
* **Individual arms: 4a 11/186, 4b 22/186, 4b(OOS) 20/186, BOTH 0/186.**
* The u56 ARGMAX book's 4b pass is not a new candidate: it is an equal-weight blend of the
  eight **gross-1.00 band arms** that already pass 4b on u56 in this grid (`b0`…`b0.06` at
  gross 1.00, OOS Sharpe 1.21–1.28), i.e. idea 439's known gross-1.00 4b family, and it
  fails 4a. **No memo filed** — the idea under test is the abstention rule, and it is killed.

## Statistical caveat (stated in the console, once, and applying to every t below it)

Cells inside one file share an arm ladder, and 1,200 live sub-menus are drawn from 31 arms,
so the paired t treats correlated cells as independent and is **inflated** — grossly so on
the live corpus (t values in the hundreds are arithmetic, not evidence). The signs and
magnitudes of D are the honest readings; the t is a direction indicator only.

Script: `research/backtests/2026-09-08_the-013-margin-rule_B.py`
Artefacts: `.console.txt` (687 lines), `.census.csv`, `.ledger.csv`, `.taugrid.csv`,
`.taugrid_live.csv`, `.sensitivity.csv`, `.decomposition.csv`, `.sorting.csv`,
`.walkforward.csv`, `.walkforward_live.csv`, `.wf2.csv`, `.arms.csv`, `.livecells.csv`,
`.livecells_cal.csv`, `.books.csv`, `.keeppaths.csv`, `.gate431.csv`

_Survivorship: SMALL439 and `universe_broad.json` are current constituents only
(`data/SMALL_PANEL_README.md`) — the contrasts between selectors are the reading, not the
levels. Research, not investment advice._
