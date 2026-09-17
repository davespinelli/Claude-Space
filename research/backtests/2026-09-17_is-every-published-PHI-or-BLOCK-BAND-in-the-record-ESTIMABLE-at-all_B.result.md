# Idea 1170 (lane B, 2026-09-17) — is every published PHI or BLOCK BAND in the record ESTIMABLE at all?

**ANSWERED = NO, AND THE THREE CLASSES FAIL DIFFERENTLY.** The moving-block BAND is clean
(estimable at 132 of 132 cells under all four resolution rules, observed inside its own 90%
band at 132 of 132). The interpolation weight PHI is 0.530 to 0.932 estimable depending
only on **which bar you pick**, not on the data. The ladder crossing **L\* is the real
defect: it is seed-stable at only 89 of 132 cells (0.674)** — a third of the record's
committed L\* values move rung when the bootstrap seed changes, and only 0.172 of committed
L\* rows publish their denominator at all.

**And the queue's own framing does not survive.** "Every published PHI in the record"
presumes `phi` names one object. It does not: `phi` appears on **17,255 committed rows in 52
files and only 848 (0.0491) are the interpolation weight**; `L*` appears on 1,344 rows and
only 87 (0.0647) are the ladder crossing. A census keyed on the token is 95% false positive.

Gates 12 of 12 PASS (1162's 15 anchor cells and 1164's 72 population cells both replayed bit
for bit, 4.4e-16). Hypotheses 2 of 8 SUPPORTED.

## The census (ARM A) — 5,715 committed CSVs, 73,452 committed sentences

| object | files | rows | publishes denominator | publishes resolution |
|---|---|---|---|---|
| S_PHI (interpolation weight) | 6 | 848 | **1.000** | 0.188 |
| S_PHI_OTHER (a different object, same name) | 46 | 16,407 | 0.000 | 0.000 |
| S_LSTAR (ladder crossing) | 2 | 87 | **0.172** | 0.000 |
| S_LSTAR_OTHER | 4 | 1,257 | 0.000 | 0.000 |
| S_BAND (block band, block context) | 35 | 23,178 | 1.000 | 0.722 |

Prose layer: 309 committed sentences quote one of the three objects **with a number**;
only **0.159** of the 208 phi sentences, 0.381 of the 21 L\* sentences and 0.163 of the 80
band sentences carry a denominator or resolution token. **The machine-readable layer is
already compliant; the reader-facing layer is not.**

## Estimability, measured on the 132 rebuildable cells (ARM B–E)

5 seeds x 1,000 draws x 2 nulls per cell; 9-rung L ladder x 3 seeds; bands at 0.80/0.90/0.95.

* phi over all cells runs **−4.48 .. 29.95**; **19 of 132 (0.144) publish a phi outside
  [0, 1]** before any rule is applied, and **7 of those still clear R_1164**.
* Re-measuring **1164's own 72 books with 5 seeds instead of 3 moves ESTIMABLE from its
  committed 56 to 52** — the estimability verdict is itself seed-dependent.
* L\* reaches the observed value at 127 of 132 (0.962) but is seed-stable at 89 (0.674).
* The 90% band's endpoints are resolved to ≤10% of its width at 116 of 132 (0.879);
  median width 18.620 pp against a median endpoint cross-seed spread of 1.385 pp.

**Dial grid, all 12 cells (estimable share):**

| | S_PHI | S_LSTAR | S_BAND |
|---|---|---|---|
| R_1164 (3x spread, 0.25pp) | 0.811 | 0.568 | 1.000 |
| R_STRICT (5x, 0.50) | 0.530 | 0.402 | 1.000 |
| R_LOOSE (1x, 0.10) | 0.924 | 0.644 | 1.000 |
| R_TSTAT (2 x median SE, ONE seed, FREE) | 0.932 | 0.636 | 1.000 |

## Pricing the repairs (ARM F′) — the cheapest one is free, and already half-done

| repair | extra draws | extra cols | rows kept | note |
|---|---|---|---|---|
| P_NONE | 0 | 0 | 132/132 | status quo |
| **P_DENOM** | **0** | 1 | 132/132 | **1.000 of committed interp-phi rows already do this** |
| **P_TSTAT** | **0** | 2 | 123/132 (0.932) | bar = 2 x median SE off the SAME draws |
| P_REFUSE | 1,056,000 | 3 | 107/132 (0.811) | 1164's 5-seed rule |
| P_INTERVAL | 1,056,000 | 2 | 132/132 | publish phi as its own cross-seed interval |

The free R_TSTAT agrees with the 5-seed incumbent on 0.879 (phi) / 0.932 (L\*) / 1.000
(band) — short of the pre-registered 0.90 bar for phi, so **H_CHEAP is REFUTED** — but
**every disagreement is one-sided: +16 admitted, −0 refused.** The cheap rule never refuses
a cell the expensive rule admits, so it is a sound *lower bound* on refusals and not a
substitute for them. Median |denominator| 3.520 pp against a median R_1164 bar of 2.042 pp
and a median R_TSTAT bar of 0.564 pp. Median cross-seed phi spread over estimable cells
**0.0989** — that is the resolution of every phi the record quotes.

## Rule 8 walk-forward and both KEEP paths (ARM F) — the repair has ZERO capital content

117 books (72 population + 3 x 15-rung anchor gross ladders), all published; choosers pick on
2009–2016 only and are scored on the untouched 2017–2026 window, with the pool restricted to
ESTIMABLE-phi books under each of the four rules.

* **4a 0 of 117 books and 0 of 45 picks.** 4b full 12, 4b OOS 13 (U56 7/5/0 by panel).
* Best 4b FULL+OOS book: **U56 N20/H126/W (= the anchor at gross 0.75), full 15.55% /
  1.1381 / −19.13% (H 1.2049/1.0932), OOS 16.92% / 1.1615 / −19.13%** — PRIOR ART, the
  standing incumbent cell, and **IS-chooser-reachable NO**.
* SPY: U56 full 15.06% / 0.8814 / −33.72%, OOS 15.15% / 0.8684. LIVE v2: 8.60% / 1.1980 /
  −12.05%, OOS 9.42% / 1.2714.
* **The estimability restriction leaves the pick UNCHANGED at 35 of 36 (panel, chooser,
  rule) cells (0.972); |dOOS Sharpe| ≥ 0.05 at 0 of 36; the single move is +0.0016 Sharpe**
  (SMALL / C_ISDD / R_STRICT, anchor/g0.30 → anchor/g0.65). **H_CAPITAL REFUTED.**

## Verdict

**KILL as a capital finding** — nothing is enacted, no memo, no rules change. The finding is
a DISCLOSURE one, the same reading 1151 reached for the cost-claim clause: refusing an
unresolvable ratio costs nothing and buys nothing in OOS terms.

**CLAUSE PROPOSED, NOT ENACTED (PROTOCOL rule 6 — Sunday review only):** *a published ratio
whose denominator is a difference of two estimated quantities must carry that denominator
and the bar it clears, computed as 2 x the order-statistic SE of the null median off the
run's own draws — which costs no extra bootstrap; a published ladder CROSSING must
additionally state the rung it lands on at every seed it was run with, because the crossing
is seed-stable at only 0.674 of this run's cells.*

**A correction this run made to itself:** the first cut computed the median SE as
(IQR / 1.349) / sqrt(n), understating it by the gaussian 1.2533 factor. **Gate G4 caught it
before a single R_TSTAT verdict was read**; `median_se` is now the distribution-free
order-statistic form, which matters because a bootstrap |MaxDD| distribution is right-skewed.

SURVIVORSHIP (PROTOCOL rule 9): U56 and B136 are current-constituent lists, SMALL the current
constituents of a sub-$2B screen. Every level here is optimistic. It largely cancels out of
the headline (a count of objects against their own noise) and does **not** cancel out of the
4a / 4b legs above.
