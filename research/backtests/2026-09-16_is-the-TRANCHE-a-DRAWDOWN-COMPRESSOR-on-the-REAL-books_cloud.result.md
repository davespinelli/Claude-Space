# Idea 1006 — is the TRANCHE a DRAWDOWN COMPRESSOR on the REAL books at the same +0.84 pp it gives the NULL?

**cloud lane, 2026-09-16.** Script `2026-09-16_is-the-TRANCHE-a-DRAWDOWN-COMPRESSOR-on-the-REAL-books_cloud.py`.
**GATES 9 of 9. HYPOTHESES 10 of 10.** Runtime 375 s.

## ANSWER = YES, AND THE RULE COLLECTS SLIGHTLY MORE THAN THE COIN FLIP DOES

Idea 999 measured `DDC = |OOS MaxDD(CANON)| − |OOS MaxDD(FPORT)|` only on coin flips and
published **+0.84 pp mean / +0.91 pp median, positive in 23 of 30 W/M/Q cells**. Read on the
**REAL books** over the same grid widened from 5 books to 9:

| statistic | REAL books | 999's NULL |
|---|---|---|
| median DDC, 54 pooled W/M/Q cells | **+1.36 pp** | +0.91 pp (its own 30) |
| median DDC, 999's own 30 cells | **+0.94 pp** | +0.91 pp |
| mean DDC, pooled | +1.40 pp | +0.84 pp |
| cells with DDC > 0 | 45 of 54 | 23 of 30 |
| paired median (REAL − NULL), per cell | **+0.10 pp** (REC5's 30: +0.12) | — |
| sign agreement, REAL vs NULL, per cell | **88.9%** (REC5's 30: 83.3%) | — |
| Spearman(NULL DDC, REAL DDC) | **+0.5382** (REC5's 30: +0.3971) | — |

Every pre-registered bar clears. `H_SIGN` (>0) **PASS**, `H_SIZE` (≥ +0.50 pp) **PASS**,
`H_MATCH` (≥70%) **PASS at 88.9%**, `H_PAIRED` (|median gap| ≤ 0.30 pp) **PASS at +0.10 pp**,
`H_RANK` (≥ +0.50) **PASS at +0.5382**. The compression is **not an estimator artefact of the
null**: it is a property of averaging P phase-books, and the rule collects it cell for cell,
with a paired gap of one tenth of a percentage point.

`H_D` **PASS exactly**: at D the family has one phase, so FPORT ≡ CANON and DDC is
`0.000e+00` on all 18 D cells. `H_COST` **PASS**: +1.37 / +1.36 / +1.34 pp at 0 / 10 / 25 bps
— not a cost artefact. `H_CAD` **PASS**: W +0.68, M +0.29, Q +1.76 pp, one sign.

## WHERE IT IS BIG, AND THE ONE PLACE IT INVERTS

The two tuned axes, all 12 points, none selected (10 bps):

| bookset | D | W | M | Q |
|---|---|---|---|---|
| REC5 (999's five) | +0.00 (0/10) | +0.55 (9/10) | +0.08 (5/10) | **+1.73 (10/10)** |
| WIDE4 (new rungs) | +0.00 (0/8) | +1.04 (8/8) | +0.29 (5/8) | **+1.97 (8/8)** |
| POOLED9 | +0.00 (0/18) | +0.68 (17/18) | +0.29 (10/18) | **+1.76 (18/18)** |

**Quarterly is where the tranche pays and it pays on every single cell — 18 of 18.** Monthly
is the weak band on both panels and in both booksets (10 of 18 positive, median +0.29 pp),
and it is monthly that carries every large NEGATIVE cell: U56/TOP40/M **−3.62 pp**,
U56/TOP60/M −2.83, U56/TOP30/M −2.65, B136/TOP60/M −2.34. The null does the same thing in the
same cells (−3.41, −2.83, −2.68, −2.28), which is why `H_MATCH` and `H_PAIRED` clear: **where
the tranche hurts, it hurts the coin flip by the same amount.** The M band is not a property
of the rules; it is a property of averaging 21 monthly phases on this tape.

Widening the book set moved the answer in the direction the null predicted: the four new
rungs (TOP5, TOP30, TOP60, BAND06) give a LARGER median compression than 999's five
(+1.97 vs +1.73 pp at Q), and the largest single real compression in the grid is
**B136/TOP5/M +5.66 pp** (−31.25% → −25.59%) and **U56/TOP5/M +5.53 pp** (−27.24% → −21.71%).
Narrow books have the most phase dispersion to average away.

## IS IT 4b-CONVERTIBLE? TWICE OUT OF 54 — AND THE MARGIN IS THE WHOLE STORY

`H_4bCONV` **PASS**. At 10 bps the REAL 4b count goes **CANON 11 of 54 → FPORT 13 of 54**, 4a
**0 → 1**, and `L4_DD` flips fail→pass in exactly 2 cells:

- `U56 / EWELIG / Q` **−22.21% → −20.14%** against the cap −20.23%; 4b `L4_DD` → PASS, binds nothing.
- `B136 / TOP30 / W` **−20.30% → −18.85%** against the same cap; 4b `L2_H2,L4_DD` → PASS.

This is 999's **double crossing** reproduced on real books: the compression converts only where
it carries the cell across a cap fixed outside it while the CAGR floor is already clearable.
Both flips clear by **0.09 pp and 1.38 pp** respectively. 41 of the 54 cells move their
drawdown in the right direction and collect nothing at all, because they were never near
−20.23%.

## THE CANDIDATE, AND WHY IT SHOULD NOT BE PROMOTED ON THESE NUMBERS

`U56 / EWELIG / Q / gross 0.75`, FPORT (the 63-phase quarterly tranche), is a **4b
KEEP-candidate that survives rule 8** — and it is a knife edge.

| | full | OOS 2017–2026 | halves |
|---|---|---|---|
| tranche (FPORT) @10 bps | 11.59% / 1.1067 / **−20.14%** | 12.29% / 1.1201 / −20.14% | 1.2030 / 1.0333 |
| phase-0 book (CANON) | 11.55% / 1.0751 / −22.21% | 11.52% / 1.0328 / −22.21% | 1.2280 / 0.9518 |
| SPY | 15.10% / 0.8830 / −33.72% | 15.21% / 0.8713 / −33.72% | 0.9591 / 0.8208 |
| RULES v2 (live), U56 | 8.62% / 1.2009 / −12.05% | 9.45% / 1.2765 / −12.05% | — |

It passes 4b at **0, 10 and 25 bps** (DD −20.12% / −20.14% / −20.18% against the cap −20.23%),
turnover 1.79×/yr, and rule 8 selects it: chosen on 2009–2016 alone by `C_IS4B`, read once on
2017–2026, it is 1 of the 2 OOS 4b passes in the walk-forward. **It is not KEEP-worthy:**

1. The binding margin is **0.09 pp of drawdown (0.05 pp at 25 bps)**. The record's own
   rebalance-offset work puts the calendar noise on a statistic like this at ~1 pp — the pass
   is an order of magnitude inside it.
2. It **does not replicate on the second panel**. `B136 / EWELIG / Q` FPORT is −23.10%, **2.9 pp
   outside the same cap**, and fails `L4_DD` at every rung.
3. Its whole drawdown is the OOS episode (full MaxDD = OOS MaxDD), so 4b's cap is being tested
   on one crash, not on two.

Memo with exact RULES wording: `2026-09-16_quarterly-tranche-candidate_cloud.memo.md`. The
recommendation there is **do not promote at Sunday review**.

## RULE 8 (PROTOCOL rule 8) — the tranche is the better estimator, and still only 2 of 24

(book, cadence) chosen inside each panel on **2009–2016 ALONE** by four IS-only choosers,
2017–2026 read **once**, 3 cost rungs, both KEEP paths:

- **OOS 4b: FPORT 2 of 24, CANON 0 of 24. OOS 4a: FPORT 4 of 24, CANON 0 of 24.**
- Median OOS across all 24 picks: FPORT **14.18% / 1.0517 / −23.82%** vs CANON 13.68% /
  0.9104 / −23.84%. **The tranche buys +0.14 of median OOS Sharpe for free** — same books,
  same schedule, same gross, only the estimator differs.
- Comparands, same OOS window: SPY **15.21% / 0.8713 / −33.72%** (U56), **15.33% / 0.8769 /
  −33.72%** (B136); RULES v2 (live) **9.45% / 1.2765 / −12.05%** (U56), **7.88% / 1.1061 /
  −12.24%** (B136).
- The one 4a pass at 10 bps is `B136 / BAND03 / W` FPORT, i.e. **the live book itself,
  tranched across its five weekly phases**: OOS 7.97% / 1.1199 / **−11.43%** against RULES v2
  on the same panel 7.88% / 1.1061 / −12.24%. The same object on U56 does *not* pass 4a (OOS
  H2 1.1089 vs the live book's 1.1173). One panel, and the Sharpe gap is +0.0138 — reported,
  not proposed.

## GATES, 9 of 9

G0 masks ≡ `engine.rebalance_mask` (0 rows). G1 fast `Ctx` ≡ `engine.backtest` on returns and
turnover (2.08e-17 / 4.44e-16). G2 `band_book(0.03,0.75)` ≡ `baseline.rules_v2_weights`
(0.0). G3 tranche identity at D (0.0). G4 determinism (0.0). G5 null gross/count match
(0 / 1.11e-16). **G6 CROSS-RUN: idea 999's committed `.real.csv` reproduced on all 240 shared
rows at 2.22e-16.** **G7 CROSS-RUN: 999's own null draws replayed on 3 pre-declared cells,
30 rows at 2.22e-16.** **G8: 999's published headline recomputed from its own committed
nulls — mean +0.84 pp, median +0.91 pp, positive 23 of 30, to the digit.** G8 also records
that 999's estimator is the **difference of the cell's medians**; the median of the paired
per-draw differences on the same cells reads +0.86 / +0.94 pp, so the published number is
convention-stable to 0.03 pp.

## SURVIVORSHIP (PROTOCOL rule 9)

U56 and B136 are current-constituent lists: every CAGR and drawdown LEVEL and every 4b verdict
above is optimistic. The measured object, DDC, is a difference between two estimators of the
SAME book on the SAME tape, so the level bias largely cancels. What does not cancel: a survivor
panel compresses cross-name dispersion, which raises phase-book correlation and **shrinks** the
CANON→FPORT gap — the bias pushes DDC toward zero and therefore works AGAINST `H_SIGN` and
`H_SIZE`, not for them. The 4b comparands are read against SPY, which is not
survivorship-inflated.

**NOT MODIFIED (rule 6):** RULES.md, PROTOCOL.md, scan.py, bot.py, baseline.py.
