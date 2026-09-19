# Idea 1373 (lane C, 2026-09-19) — INVERSE-VOL SLOT WEIGHTING on the frozen 2026-09-04 incumbent
## VERDICT: **rule-8 KILL for the DIAL on all three panels. PARK for the B136 HALF-RISK SUBSTITUTION. KILL on U56, the live panel.**
## The one-line finding: **inverse-vol slot weighting is a DRAWDOWN instrument, not a Sharpe instrument — and on the incumbent's own panel the drawdown is not for sale at a price worth paying.**

All 36 grid cells, 30 bootstrap rows, 6 shuffle-null rows and 3 rule-8 rows published:
`*.grid.csv` `*.bootstrap.csv` `*.shuffle.csv` `*.exchange.csv` `*.rule8.csv` `*.gates.csv` `*.log`.
Offline, deterministic, 63 s, gates **8 of 8**. Selection is byte-identical to the incumbent at every
rung (gate G3); only the 20 slot weights move (w ∝ vol^−p, normalised, gross held at 0.75).

## 1. What the dial does, and what it costs (U56, volwin 20, 10 bps, t+1)
| p | CAGR | Sharpe | MaxDD | OOS CAGR / Sharpe | turnover/yr | Calmar | pp DD bought per pp CAGR paid |
|---|---|---|---|---|---|---|---|
| **0.00 (incumbent)** | **15.80%** | **1.1537** | **−19.13%** | **17.32% / 1.1857** | 2.75 | **0.826** | — |
| 0.25 | 14.89% | 1.1442 | −18.36% | 16.58% / 1.1974 | 3.17 | 0.811 | 0.85 |
| 0.50 | 14.00% | 1.1311 | −17.68% | 15.80% / 1.2038 | 3.93 | 0.792 | 0.80 |
| 0.75 | 13.16% | 1.1168 | −17.06% | 15.03% / 1.2067 | 4.74 | 0.772 | 0.78 |
| 1.00 | 12.40% | 1.1017 | −16.49% | 14.31% / 1.2066 | 5.56 | 0.752 | 0.78 |
| 1.50 | 11.10% | 1.0710 | −15.47% | 13.07% / 1.2005 | 7.15 | **0.718** | 0.78 |

SPY on this panel: 15.12% / 0.8844 / −33.72%, OOS Sharpe 0.8738. Live RULES v2: Sharpe 1.2011, MaxDD −12.05%.

**H_DD CONFIRMED and irrelevant.** p=1 shallows U56 MaxDD by **+2.64 pp** (−19.13% → −16.49%), widening the
4b DD margin from **+1.10 pp to +3.74 pp**. But U56 already PASSES that leg, and the CAGR-floor margin falls
**5.22 pp → 1.81 pp** (0.52 pp at p=1.5). The dial does not buy a binder; it **swaps a 5 pp margin for a
1 pp one at an exchange rate of 0.78 pp of drawdown per pp of CAGR**, and Calmar falls monotonically at
every rung on both volwins, full sample and OOS. Turnover doubles (2.75 → 5.56/yr).

**H_SHARPE FAILED, with the sign reversed.** Paired circular-block bootstrap (400 reps × 63-row blocks,
seed 20260919, identical blocks both sides): the daily return difference against the incumbent is
**negative and resolvable at 20 of 30 cells** (U56 p=1 FULL **t −4.49**, OOS **t −2.51**; B136 FULL t −4.19;
all 20 resolvable cells are negative). The small OOS Sharpe rise on U56 (+0.021 at p=1) is pure
denominator — the numerator is resolvably worse.

## 2. The one place the leg actually binds — B136 (volwin 20)
At equal weight B136 **fails 4b on the DD cap alone**, margin **−0.51 pp** (−20.74% against the −20.23% cap).
Every rung p = 0.25 … 1.00 flips it to a **full 4b PASS, full sample AND OOS** (vw 60: 0.25 … 1.50 too);
p = 1.5 then fails H2. At the two lowest rungs the drawdown is bought **cheaper than 1:1** — **1.69 / 1.65 pp
of MaxDD per pp of CAGR** — and Calmar **rises** (0.7743 → 0.7845 → 0.7942 full; 0.7805 → 0.7960 → 0.8101 OOS).
That is the only genuinely favourable trade in the whole 36-cell grid, and it is on a panel the live book
does not trade. 4b by panel: **U56 12 of 12, B136 9 of 12, SMALL 0 of 12. 4a 0 of 36** (live RULES v2's
−12.05% MaxDD is out of reach for a growth book, as in every run of this family).

## 3. The effect is VOL INFORMATION in the drawdown and DISPERSION in the Sharpe
Dispersion-matched SHUFFLE null (200 seeds, the identical weight vector dealt to the held names in permuted
order — weight dispersion held exactly, vol information destroyed):
**MaxDD percentile 1.000 / 1.000 / 1.000 / 1.000 / 0.875 / 0.955** across the six (panel, p) cells — the
drawdown gain is real vol information. **Sharpe percentile 1.000 / 0.995 on U56 and 1.000 / 1.000 on SMALL,
but only 0.910 / 0.890 on B136** — so **H_INFO fails on B136 for Sharpe**: what carries B136's Sharpe is
unequal weights, not which name is which.

## 4. Rule 8 (p chosen on warm-up..2016-12-31 by argmax IS net Sharpe, ties to the lower p; 2017–2026 read ONCE)
| panel | IS pick | OOS Sharpe pick | OOS Sharpe anchor p=0 | Δ | ex-post best OOS p |
|---|---|---|---|---|---|
| U56 | **p = 0** | 1.1857 | 1.1857 | **+0.0000** | 0.75 |
| B136 | **p = 0** | 1.0180 | 1.0180 | **+0.0000** | 0.00 |
| SMALL | p = 1.5 | 0.5340 | 0.4398 | +0.0942 | 1.5 |

**H_PICK CONFIRMED.** The chooser picks the incumbent on both panels that clear 4b, so the dial is
**un-choosable but harmless** there — it cannot be tuned into the book by any legal IS rule. Where it does
get picked (SMALL) the panel fails 4b at 0 of 12 with or without it, so the +0.0942 buys nothing. B136's 4b
flip is therefore **not reachable by rule 8**: the IS chooser leaves the DD fail standing.

## 5. Why this is a PARK and not a KEEP, and why no memo
No cell dominates the incumbent on U56: every p > 0 lowers CAGR (−3.40 pp at p=1), full Sharpe (−0.052,
resolvably) and Calmar, while widening a margin that already passes. The B136 half-risk rung (p = 0.25–0.5,
either volwin) is a real 4b KEEP-candidate *shape* — 4b PASS full and OOS, Calmar up full and OOS, DD gain
beyond its own dispersion-matched null — but it is on a non-live panel and is not IS-choosable, so it is
PARKED for a run that can justify a fixed convention without hindsight. **No RULES change is proposed and no
memo is written** (PROTOCOL rule 6 reserves enactment for the Sunday review; nothing here reaches a KEEP).

## 6. Gates (8/8) and caveats
G1 the p=0 U56 cell replays idea 1350's committed head-vintage anchor 15.80% / 1.1537 / −19.13% to
**max|dev| 3.7e-5**, inside that run's own 5e-3 tape floor. G2 weights sum to gross, worst |dev| 3.3e-16.
G3 p=0 bit-identical across both volwins. G4 all 36 cells published. G5 exactly two tuned parameters
(p, panel). G6 the chooser's last IS row is 2016-12-30. G7 determinism exact. G8 effective N is
non-increasing in p at every panel (19.8 → 13.6 on U56).
**Survivorship (rule 9):** U56 / B136 are current-constituent lists and SMALL a current sub-$2B screen, so
every level is an upper bound. The headline is a difference between two weightings of the SAME names on the
SAME days, first-order immune to a common level bias; the 4b pass count is not.
**Estimator caveat:** the vol used is the book's own vol20 read at the decision row (t−1), clipped to
[0.08, 2.00] — the 0.08 floor is the live rules' own clip. The 60-day control moves every number in the same
direction and never changes a verdict, so no result here rests on the window choice.
