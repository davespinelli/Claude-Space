# Idea 155 — where-selectivity-and-cost-cross (cloud, 2026-09-06)

**SPLIT. The queue's "if" FIRES and comes with a number — the argmax selectivity is q = 0.90 at
0–20 bps on both primary panels and 1.00 by 25 bps, a THIRD independent derivation of "drop the
ranking". But the crossing the queue went looking for DOES NOT EXIST on the large-cap panels,
because idea 78's two curves are not in the same units: gross CAGR premium is monotone in
selectivity and survives past 30 bps, while gross SHARPE premium is already negative at zero
cost and Spearman(q, gross premium) is POSITIVE (+0.615 U56, +0.853 B136). Nothing crosses;
selectivity buys return and buys more risk than return. One 4b by-product goes to Sunday review
as a SCOPING clause, not a book. No RULES change; RULES.md, scan.py, bot.py and baseline.py
untouched.**

Script `2026-09-06_where-selectivity-and-cost-cross_cloud.py`; artefacts `.console.txt`,
`.grid.csv`, `.breakeven.csv`, `.subpanels.csv`, `.walkforward.csv`, `.keep.csv`, `.memo.md`.
283 s.

## Reproduction, before any new number was read

Idea 78's `build_panels`, `eligible_mask`, `weights_ewall`, `weights_cand`, `fail_4a`,
`fail_4b`, `spearman`, `tstat` and its composite key imported verbatim; idea 171's
`fast_backtest` used for speed and asserted against `engine.backtest` first.

* **idea 78's published control ordering re-derives**: B136 @10 bps EWall **1.0261** > CAND20
  **0.9569** > CAND5 **0.8802** against its published 1.026 / 0.957 / 0.880 — **max |d| 0.0002**.
* `fast_backtest` == `engine.backtest` on this run's own weight matrices, max |dret| **2.1e-17**.
* cost additivity `net(c) = gross − turnover·c/1e4` direct vs derived, **0.000e+00** over 2 q ×
  7 rungs (so the 7 rungs cost one simulation each, not seven).
* cached-`Panel` weights == uncached `weights_q`, **0.000e+00**.

**A construction defect in the parent, found by the reproduction gate and fixed rather than
absorbed.** The first attempt asserted `q = 1.00 == weights_ewall` and FAILED at max |dw| 0.25.
The cause: a name can clear the 200d / vol20 < 0.60 gate while its composite is NaN (200 days of
history but not the 252 the 12-1 leg needs). **Idea 78's `weights_ewall` holds those names on
426 of 4699 B136 days (last 2021-09-28, up to 11 names at once); no ranked book can.** Comparing
any ranked book to that EWall mixes a ranking effect with a *coverage* effect. Every arm here
uses the rankable set, so q = 1.00 is EWall on exactly the names the key can order and the
premium is pure ranking. The size of the change is small and is printed, not assumed away:
B136 @10 bps EWall 1.0261 vs EWall-rankable **1.0253**.

## Q2 — the gross curve: the queue's premise is true in CAGR and FALSE in Sharpe

At **zero cost**, per panel, against the same panel's q = 1.00 book:

| panel | q=0.05 CAGR prem | q=0.20 | q=0.50 | q=0.90 | Spearman(q, gross CAGR prem) | Spearman(q, gross **Sharpe** prem) |
|---|---|---|---|---|---|---|
| U56 | **+14.03 pp** | +7.64 | +3.32 | +1.04 | −1.00 (monotone) | **+0.615** |
| B136 | **+9.07 pp** | +2.74 | +1.50 | +0.55 | −1.00 (monotone) | **+0.853** |
| ETF36 | +0.05 | +0.62 | +1.31 | +0.41 | non-monotone | +0.853 |
| BSTK100 | +10.15 | +4.75 | +1.56 | +0.64 | −1.00 | +0.643 |
| SMALL439 | +2.66 | +3.38 | +2.36 | +0.60 | non-monotone | −0.238 |

The key **does** carry information: the most selective book earns +14.03 pp/yr of CAGR over
holding the eligible set on U56. It carries none in risk-adjusted terms, at any cost, because it
buys the return with more than proportional risk:

| panel | | CAGR | Sharpe | MaxDD | mean names held |
|---|---|---|---|---|---|
| U56 | q=0.05 | 25.34% | **0.9912** | **−34.76%** | 1.8 |
| U56 | q=1.00 | 11.31% | **1.1324** | −15.77% | 37.4 |
| B136 | q=0.05 | 20.69% | **0.9892** | **−30.00%** | 4.6 |
| B136 | q=1.00 | 11.62% | **1.1046** | −17.34% | 91.4 |

**So there is nothing to cross.** Idea 78's "gross spread rises in selectivity" (a return
statement) and "net premium falls" (a Sharpe statement) are not two ends of one curve. On the
Sharpe axis the gross curve already slopes the way the net curve does; adding cost only steepens
it. **P2 is a MISS and it is the run's most transferable finding**: any future quote of idea 78's
gross-spread result must name its unit.

## Q3 — the answer the queue asked for: argmax q by cost rung

Net Sharpe premium against the same panel's q = 1.00 book. Every one of the 12 × 7 × 5 grid
points is in `.grid.csv` and the console.

| panel | 0 bps | 5 | 10 | 15 | 20 | 25 | 30 |
|---|---|---|---|---|---|---|---|
| **U56** | **0.90** | 0.90 | **0.90** | 0.90 | 0.90 | 0.90 | 0.90 |
| **B136** | **0.90** | 0.90 | **0.90** | 0.90 | 0.90 | **1.00** | **1.00** |
| ETF36 | 0.70 | 0.70 | 0.70 | 0.70 | 0.70 | 0.70 | 0.70 |
| BSTK100 | 0.80 | 0.80 | 0.90 | 0.90 | 0.90 | 0.90 | 0.90 |
| SMALL439 (secondary) | **0.30** | 0.30 | 0.30 | 0.30 | 0.30 | 0.30 | 0.30 |

**At 10 bps the argmax is 0.90 on both primary panels — "at or near 1.0", so the queue's
condition fires: a third independent derivation of idea 82's "drop the ranking", now with a
number.** The number is not 1.00 but 0.90: trimming the worst-ranked *decile* of the eligible set
is worth +0.0316 (U56) and +0.0072 (B136) of Sharpe at 10 bps; every selectivity below 0.80 is
worse than not ranking at all, at every rung including zero. On U56 the whole q ≤ 0.20 region
costs 0.14–0.16 of Sharpe gross and 0.11–0.19 at 30 bps.

**The dual reading — breakeven cost c\*(q), the rung at which each selectivity stops beating
q = 1.00** (`.breakeven.csv`; "<0" = already behind with zero costs):

| panel | 0.05 | 0.10 | 0.20 | 0.30 | 0.50 | 0.70 | 0.80 | 0.90 | Spearman(q, c\*) |
|---|---|---|---|---|---|---|---|---|---|
| U56 | <0 | <0 | <0 | 11.4 | 3.2 | <0 | 16.2 | **>30** | **+0.464** |
| B136 | <0 | <0 | <0 | <0 | <0 | <0 | <0 | **20.7** | **+0.500** |
| ETF36 | <0 | <0 | <0 | <0 | <0 | >30 | 24.6 | 6.4 | +0.768 |
| BSTK100 | <0 | <0 | 0.5 | <0 | <0 | <0 | 29.2 | **>30** | +0.500 |
| SMALL439 | 0.4 | 13.8 | >30 | >30 | >30 | >30 | >30 | >30 | +1.000 |

**P5 HIT on all five panels: the more selective the book, the lower the cost that kills it.** The
gradient is brutal — on U56 the breakeven falls from >30 bps at q = 0.90 to below zero at
q ≤ 0.20. The one panel where selectivity survives real costs is the small panel, and that is
ideas 39/49/136's inverted-gate panel, not evidence about the large-cap rule.

## Q4 — is the argmax a draw or a result? 72 seeded sub-panels of B136

k = 20/40/80 × 24 draws, idea 78's own construction, 864 books × 7 rungs:

| rung | mean argmax q | median | sd | argmax = 1.00 | argmax ≥ 0.80 | mean best premium | draws with ANY q<1 ahead |
|---|---|---|---|---|---|---|---|
| 0 | 0.840 | 0.90 | 0.152 | 20.8% | 77.8% | +0.0218 | 57/72 |
| 5 | 0.878 | 0.90 | 0.124 | 31.9% | 83.3% | +0.0161 | 49/72 |
| **10** | **0.886** | **0.90** | 0.126 | **37.5%** | 83.3% | +0.0115 | 45/72 |
| 15 | 0.921 | 1.00 | 0.110 | 52.8% | 91.7% | +0.0080 | 34/72 |
| 20 | 0.946 | 1.00 | 0.078 | 61.1% | 97.2% | +0.0054 | 28/72 |
| 25 | 0.948 | 1.00 | 0.126 | 69.4% | 97.2% | +0.0036 | 22/72 |
| 30 | 0.955 | 1.00 | 0.126 | 76.4% | 97.2% | +0.0022 | 17/72 |

**P4 HIT, and here it is monotone rather than nearly so: the argmax q rises with every rung**
(0.840 → 0.955), the fraction of draws whose best answer is "do not rank at all" rises 20.8% →
76.4%, and the value of the best q < 1 decays 10× (+0.0218 → +0.0022). Mean argmax rises with k
too (0.829/0.846/0.846 at 0 bps → 0.952/0.954/0.958 at 30). The mean premium is negative at every
q ≤ 0.80 and every rung, with the q = 0.20 row at t = **−14.2** (0 bps) to **−22.1** (30 bps).

## Q5 — rule 8: nobody could have picked 0.90 from the IS window

Picks made on IS ≤ 2016-12-31, OOS ≥ 2017-01-01 read once. Mean over the 2 primary panels:

| rung | S3 ORACLE | **S0 q=1.00 (no ranking)** | S1 IS-Sharpe fit | S2 random q | *const q=0.90* |
|---|---|---|---|---|---|
| 0 | 1.1795 | **1.1486** | 0.9619 | 1.1484 | *1.1647* |
| **10** | 1.0830 | **1.0662** | **0.8502** | 0.8555 | *1.0765* |
| 25 | 0.9444 | **0.9422** | 0.6822 | 0.9338 | *0.9438* |
| 30 | 0.9016 | **0.9008** | 0.6262 | 0.7419 | *0.8994* |

**P6 HIT, emphatically. The IS-window argmax picks q = 0.15 (U56) and q = 0.10 (B136) at every
rung and gives up 0.216 of OOS Sharpe against doing nothing, at 14.5 pp more drawdown**
(−31.3% vs −16.8% at 10 bps). This is the project's standing result (ideas 132/141/151/160/189)
on a ninth bar, and it is the honest boundary on this run's own answer: **q = 0.90 is a
full-sample statement.** A pre-registered constant q = 0.90 would have beaten the no-ranking
control OOS at 6 of 7 rungs (+0.0161 at 0 bps, +0.0103 at 10, −0.0014 at 30) and beats it on
56.9% of the 72 sub-panels at 10 bps, falling to 43.1% at 25 bps — the same "write the constant
down, do not fit it" pattern ideas 189/219 found on the dials.

Benchmarks OOS: **SPY 15.45% / 0.8820 / −33.72%**; RULES v1 @10 bps 0.7471 (U56), 0.5763 (B136),
0.4425 (ETF36), 0.5440 (BSTK100), 0.4923 (SMALL439).

## Q6 — both KEEP paths

924 books × 7 rungs. Panels: 4a 2/3/5/5/9/10/17 and 4b **8/8/7/2/0/0/0** at 0/5/10/15/20/25/30
bps. Sub-panels: 4a 70→267, 4b **157/120/91/58/27/6/0**. First-failing bar on 4b over all rows:
**H1 3615, H2 1584, DD 665, CAGR 110, OOS 10**. **SMALL439: 0 of 84 passes at any rung** —
ideas 39/49/136 again. Sub-panel 4b pass count by q at 10 bps is monotone in q up to 0.90:
0/0/0/0/0/0/4/9/17/18/**24**/19 for q = 0.05…1.00, i.e. **q = 0.90 produces more 4b passes than
any other selectivity, including not ranking at all.**

**The 4b by-product, recorded and NOT proposed as a book.** `q = 0.90` (equal-weight the top 90%
of the eligible set, 75% gross, weekly) passes 4b on **U56 at 0/5/10/15 bps** — 11.30% / **1.0808**
/ −16.79%, halves 1.114/1.054, **OOS 1.1263**, turnover 9.4×/yr at 10 bps — **and on B136 at
0/5/10 bps** — 11.14% / 1.0325 / −18.37%, halves 1.148/0.925, OOS 1.0267, 9.3×/yr. It is
cross-universe at PROTOCOL's own 10 bps, and it survives one rung further than q = 1.00 on U56
(where the no-ranking book already fails 4b's CAGR floor at 10 bps). It dies at 20–25 bps on the
CAGR floor, so it does **not** clear idea 82's proposed 25 bps cross-universe bar. Per **idea
144 a re-dialled book is the same book**: this is idea 72's `EWall` with its worst decile
trimmed, so it goes to Sunday review as a SCOPING clause, not a new book. Exact wording in
`.memo.md`.

## Predictions

5 of 6 hit. **P1** HIT (idea 78's ordering to 0.0002). **P2 MISS, and it is the headline**: the
gross premium is negative at most q and Spearman(q, gross Sharpe premium) is +0.615 / +0.853,
i.e. the queue's premise holds in CAGR and inverts in Sharpe — there is no crossing to locate.
**P3** HIT (argmax 0.90 / 0.90 at 10 bps). **P4** HIT (non-decreasing in cost on both panels, and
monotone over the 72 sub-panels: 0.840 → 0.955). **P5** HIT on all five panels (+0.46 to +1.00).
**P6** HIT (IS-fit 0.8502 vs no-ranking 1.0662 at 10 bps).

## Caveats carried

Current-constituent survivorship (idea 54) on all five panels. It runs **against** the arm this
run favours — q = 1.00 and q = 0.90 hold the whole eligible set including exactly the beaten-down
cohort a delisting-aware panel would kill — so a survivorship-free panel would move the argmax q
DOWN, not up, and the "drop the ranking" conclusion is the one this bias does not manufacture.
No LEVEL here is a tradable estimate. The small panel is secondary throughout (ideas 39/49/136:
the gate is inverted there), so its argmax q = 0.30 is not evidence about the large-cap rule; it
is also the only panel where selectivity survives 30 bps, which is why it is reported and not
pooled. Costs are a flat linear bps charge on turnover; real cost is spread plus impact and is
convex in size, so a 30 bps rung is not "trading 30 bps wide" (idea 126). The 72 sub-panels share
one parent and overlap heavily, so their spread is a sampling band, not 72 independent
experiments. At q = 1.00 the premium is 0 by construction, so the sweep tests whether ANY q < 1
beats holding the eligible set, not a horse race between two free arms. The rankable-set change
documented above makes this run's q = 1.00 differ from idea 78's `EWall` by 0.0008 of Sharpe on
B136 @10 bps; every number here is on the rankable convention. Ideas 38, 126 and 144 carry over.

## Follow-ups queued

227 (the coverage-vs-ranking split: how many published EWall claims hold eligible-but-unrankable
names, and does any verdict move), 228 (does the q = 0.90 trim survive as a constant on a third
corpus and on the cadence/gross dials), 229 (report idea 78's gross-spread family in BOTH units,
since the sign depends on which one is quoted).
