# Idea 1179 (lane B, 2026-09-17) — what does a ONE-SIDED agreement between a FREE bar and a PAID one buy the record?

**ANSWERED = NOTHING, BECAUSE THE ONE-SIDEDNESS IS NOT A PROPERTY OF THE MACHINERY AND DOES
NOT GENERALISE. WHAT THE RECORD CAN ACTUALLY BUY IS A DIFFERENT PROPERTY — BOUNDARY
CONCENTRATION — AND THAT ONE IS PRESENT AT ALL FOUR PAIRS AND IS CHEAP.**

Three findings, in the order they bind.

1. **The direction does not replicate; it REVERSES.** Of the three fresh paid-vs-free pairs
   the queue names, **0 of 3 are one-sided in 1170's direction**. Two are one-sided the
   OTHER way (the free bar *refuses* what the paid bar admits) and one is two-sided.
2. **1170's own one-sidedness is a CONSTANT artefact, not a machinery fact.** Its free bar
   (2 × median SE) sits far below its paid bar; matching the two on the number of cells
   admitted needs a free constant of **6.532, not 2.000 — 3.27x** — and at that constant
   the +16 / −0 becomes **+1 / −1, TWO-SIDED**. The "sound lower bound on refusals" is what
   any looser bar gives you by construction.
3. **The SCREEN works anyway, and it does not need one-sidedness.** All four pairs reach
   **zero screened error** — verdicts identical to paying the full null everywhere — while
   paying at only **0.023 to 0.299** of cells, because disagreements concentrate near the
   free bar's critical value. That, not the sign of the minority count, is what the free
   bar buys.

**And it buys nothing in capital.** Swapping an IS chooser's admitted pool between the free
bar, the paid bar and the screen moves the pick at **0 of 36** (panel, pair, chooser) cells
and |ΔOOS Sharpe| is **0.0000** everywhere. 4a is **0 of 72** books and **0 of 108** picks.

Gates **12 of 12 PASS**, including 1170's committed pair replayed bit for bit (0 of 132
verdicts differing on each of its two rules, agreement 0.8788 / +16 / −0 reproduced to
0.000e+00). Hypotheses **1 of 6 SUPPORTED**.

## The four pairs

| pair | paid bar | free bar | cost of the free bar |
|---|---|---|---|
| `B_MEANP` | moving-block bootstrap p on the mean (L=63, 1,000 draws) | normal p on the t | 0 draws |
| `B_SHARPE` | moving-block bootstrap band [q025,q975] on the Sharpe | Lo (2002) analytic SE | 0 draws |
| `B_PERMT` | moving-block sign-flip permutation p on r − r_SPY | paired t | 0 draws |
| `B_TSTAT` | 1170's `R_1164` (5 seeds × 2 nulls × 1,000 draws) | 1170's `R_TSTAT` (1 seed) | 0 extra draws |

## ARM A — the census: the record CANNOT audit this retrospectively

**5,747 committed CSVs scanned**; 816 carry at least one bar column.

| class | files | rows | share of bar-bearing files |
|---|---|---|---|
| **BOTH** a paid and a free bar | **35** | 14,573 | **0.0429** |
| PAID only | 94 | 21,929 | 0.1152 |
| FREE only | 687 | 432,101 | 0.8419 |

In a resampling context (247 files) BOTH rises to **0.1377**. Prose is worse: of **59,872
committed sentences** in 1,060 files, **843 quote a paid bar and only 23 (0.0273) also quote
its free counterpart**. **H_AUDITABLE REFUTED at 0.0429.** A screen cannot be back-tested on
the record's own committed files; it has to be adopted forward, one extra column at a time.

## ARM C — agreement and one-sidedness (87 POP+ANCHOR cells; the 45 GROSS rungs are near-duplicates for scale-invariant statistics and are published separately)

| pair | free admits | paid admits | agree | +extra / −lost | verdict | **matched z\*** | matched agree | matched +/− | **matched verdict** |
|---|---|---|---|---|---|---|---|---|---|
| `B_MEANP` | 79 | 80 | 0.9655 | +1 / −2 | TWO-SIDED | 1.935 (vs 1.960) | 0.9770 | +1 / −1 | TWO-SIDED |
| `B_SHARPE` | 79 | 81 | 0.9770 | +0 / −2 | **ONE-SIDED −** | 1.813 (vs 1.960) | **1.0000** | +0 / −0 | **IDENTICAL** |
| `B_PERMT` | 11 | 20 | 0.8966 | +0 / −9 | **ONE-SIDED −** | 1.389 (vs 1.960) | 0.9540 | +2 / −2 | TWO-SIDED |
| `B_TSTAT` | 78 | 62 | 0.8161 | **+16 / −0** | **ONE-SIDED +** | **6.532 (vs 2.000)** | 0.9770 | +1 / −1 | **TWO-SIDED** |

Over all 132 cells the same pattern holds (B_TSTAT 0.8788 / +16 / −0, which is 1170's
committed number; all 16 of its disagreements sit in the 87 non-GROSS cells).

**H_ONESIDED REFUTED** (0 of 3 fresh pairs in the same direction). **H_UNIVERSAL REFUTED**
(3 of 4 one-sided, and in two directions). **H_CONSTANT REFUTED** (1 of 3 survives matching,
and the one that survives — `B_SHARPE` — survives by becoming *identical*, i.e. its
disagreement was purely a level offset too).

**The mechanism is arithmetic and it explains both signs.** Where the paid bar is a
resample that *widens* the null for serial dependence (`B_SHARPE`, `B_PERMT`), the paid bar
is the stricter one and the free bar over-admits or under-admits according only to which
constant is larger; here the block band came out *narrower* than Lo's iid SE at the margin,
so the free bar refused 2 and 9 cells the paid bar admitted. Where the two bars differ by an
arbitrary multiplier (`B_TSTAT`: 2 × SE against 3 × cross-seed spread with a 0.25 pp floor),
the looser one admits a strict superset **by construction**, and a superset is one-sided by
construction. **One-sidedness is a statement about two constants, not about two methods.**

## ARM D — the screen, all 24 dial points published (`.dialgrid.csv`)

Flag a cell when |z_free − z\*| ≤ k and pay the full null only there; take the free verdict
everywhere else. k = ∞ is the status quo (cost 1.000, error 0.000 by construction);
k = 0 is the free bar alone.

| pair | free-only error | **exact k\* for zero error** | **cost at k\*** | ladder k for zero error | cost |
|---|---|---|---|---|---|
| `B_MEANP` | 0.0345 | 0.045 | **0.0575** | 0.25 | 0.1149 |
| `B_SHARPE` | 0.0230 | 0.043 | **0.0230** | 0.25 | 0.1149 |
| `B_PERMT` | 0.1034 | 0.671 | **0.2529** | 1.00 | 0.3678 |
| `B_TSTAT` | 0.1839 | 4.786 | **0.2989** | ∞ | 1.0000 |

**H_SCREEN SUPPORTED, 4 of 4.** Every pair reproduces paying-everywhere exactly while paying
at under 30% of cells, and two of them at under 6%. The screen does **not** require
one-sidedness: `B_MEANP` is two-sided and still gets to zero error at 0.0575 cost, because
its one wrong-way disagreement also sits within 0.045 of the bar. **The property worth
publishing is that disagreements are boundary-concentrated, and it is a strictly weaker and
strictly more useful property than the one 1170 reported.**

Gate G12 checks both screen identities and monotonicity in k (0.000e+00).

## ARM F — rule 8 walk-forward and both KEEP paths: ZERO capital content

72 population books (3 panels × 4 N × 3 H × 2 cadences), every one published. Bars for the
choosers are rebuilt on the **IS window (2009–2016) only**; picks are scored on the untouched
2017–2026 window. 3 panels × 3 choosers × 4 pairs × 3 regimes (`G_FREE` / `G_PAID` /
`G_SCREEN` at k = 1.00) = **108 picks, all published**.

* Base rates: **4b full 2 of 72, 4b OOS 3 of 72, 4a 0 of 72** (U56 2/2/0, B136 0/1/0,
  SMALL 0/0/0).
* Picks: **4b full AND OOS 0 of 108, 4a 0 of 108.**
* **The bar regime moves the pick at 0 of 36 (panel, pair, chooser) cells**, for free-vs-paid
  and for screen-vs-paid alike; mean and max |ΔOOS Sharpe| = **0.0000**. **H_CAPITAL
  REFUTED.**
* Best 4b book (full AND OOS): **U56 / N20/H126/W**, full **15.55% / 1.1381 / −19.13%**
  (H1 1.2049 / H2 1.0932), OOS **16.92% / 1.1615 / −19.13%**. Against SPY full
  15.06% / 0.8814 / −33.72%, OOS 15.15% / 0.8684 / −33.72%; live RULES v2 full
  8.60% / 1.1980 / −12.05%, OOS 9.42% / 1.2714 / −12.05%. It is **PRIOR ART** — the same
  incumbent cell 1170 reached — **IS-chooser-reachable NO (0 of 108 picks land on it)**, and
  it **fails 4a**. No memo; nothing here is a KEEP candidate.
* **Published honestly:** `B_PERMT`'s IS-window pool is nearly empty (mean 0.33 books) and
  the chooser falls back to the unrestricted 24-book set at **6 of 9** (panel, chooser) cells
  under every regime. That is *why* its regimes cannot differ, and it is a limitation of the
  arm, not a result.

## Verdict

**KILL as a capital finding.** Nothing is enacted; no memo, no rules change. The finding is a
DISCLOSURE one — the fifth in this family after 1151, 1165 and 1170 — and it *corrects* 1170
rather than extending it.

**CLAUSE PROPOSED, NOT ENACTED (PROTOCOL rule 6 — Sunday review only):** *a run reporting that
a cheap bar agrees one-sidedly with an expensive one must also report the agreement at a
LEVEL-MATCHED cheap constant — the one admitting the same number of cells — because a looser
bar admits a superset by construction and a superset is one-sided by construction; and a run
publishing a resampled bar should publish its closed-form counterpart in the same row, which
costs no draws and is the only way the screen above can ever be audited from the record
(BOTH is 0.0429 of committed bar-bearing CSVs today).*

**A correction this run makes to the record.** 1170's committed sentence — *"every
disagreement is one-sided: +16 admitted, −0 refused. The cheap rule never refuses a cell the
expensive rule admits, so it is a sound lower bound on refusals"* — is **arithmetically
correct and inferentially void**. Its free bar is 3.27x looser than its paid bar at matched
level; at matched level the same 132 cells give +1 / −1. Any future citation should quote the
boundary-concentration number (k\* = 4.786, cost 0.2989) instead, which is what actually
licenses the screen.

**SURVIVORSHIP (PROTOCOL rule 9).** U56 and B136 are current-constituent lists; SMALL is the
current constituents of a sub-$2B screen (**664 columns after dropping 52 tickers with
`max_1d_move >= 1.0` from `data/small_meta.csv`**, tape 2010-01-04 → 2026-09-11). Every
delisted, zeroed or screened-out name is absent, so every CAGR, drawdown and 4b base rate
above is the most flattering the period could have produced. It largely cancels out of the
headline — an agreement count between two bars read on the same cell — and does **not** cancel
out of the 4a / 4b legs in ARM F.
