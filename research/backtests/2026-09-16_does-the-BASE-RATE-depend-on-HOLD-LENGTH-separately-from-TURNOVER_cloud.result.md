# Idea 936 — does the BASE RATE depend on HOLD LENGTH separately from TURNOVER?

**cloud lane, 2026-09-16.** Script `2026-09-16_does-the-BASE-RATE-depend-on-HOLD-LENGTH-separately-from-TURNOVER_cloud.py`.
Two tuned dials: **rebalance grid {D, W, M, Q} × min hold {0, 5, 21, 63, 126} trading days** = 20
points, all reported. Fixed (not dials): gross 0.75, 10 bps, NTOP 20, 3 top-N mechanisms × 2 panels,
canonical period-end dates; a 0 bps re-pricing is a diagnostic on the comparand (968's C2 precedent).
240 book rows + 1,600 null rows. **Gates 6 of 6 pass**, including G3 (H=0 reproduces idea 1059's
committed U56/CAND20/W book to 3.5e-04), G5 (the constraint binds: mean realised holding span
39.6 → 44.1 → 73.1 → 126.6 → 188.8 days) and G6 (the H=0 null's turnover reproduces 1059's
committed 239.0 / 49.8 / 11.5 / 3.9 per year to within 1.8%).

## THE CONSTRUCTION DOES SPLIT THE AXIS

Null realised turnover per year, U56 (rows = rebalance grid, cols = min hold):

| f \ H | 0 | 5 | 21 | 63 | 126 |
|---|---|---|---|---|---|
| D | 239.1 | 49.1 | 13.0 | 5.5 | 3.6 |
| W | 49.7 | 41.7 | 10.7 | 4.5 | 2.6 |
| M | 11.5 | 11.5 | 8.5 | 3.8 | 2.1 |
| Q | 3.9 | 3.9 | 3.9 | 2.9 | 1.6 |

The min-hold dial spans the **entire** cadence range at fixed f: (D, H=5) has the turnover of
(W, H=0) to 1.1%, (D, H=21) that of (M, H=0), (D, H=126) that of (Q, H=0). That is the contrast
926's drag-matching could not make — same drag, opposite reaction speed.

## THE ANSWER: the null's upper tail is a TURNOVER object; frequency carries nothing beyond it

Null p90 Sharpe, U56, 10 bps:

| f \ H | 0 | 5 | 21 | 63 | 126 |
|---|---|---|---|---|---|
| D | **−0.825** | 0.794 | 1.031 | 1.131 | 1.141 |
| W | 0.738 | 0.814 | 1.038 | 1.137 | 1.108 |
| M | 1.077 | 1.077 | 1.095 | 1.112 | 1.117 |
| Q | 1.166 | 1.166 | 1.166 | 1.143 | 1.165 |

- **H_FREQ PASS.** Across **39 matched pairs** (different f, realised turnover within 20%), the
  null's p90 Sharpe agrees to a **median |Δ| of 0.032 and a max of 0.059**; |Δ base rate| median
  0.000. Once drag is charged, the rebalance frequency is worth about 0.03 of Sharpe.
- **H_TAIL PASS.** η² of the null's p90 Sharpe over the 20 cells: **log-turnover 0.383** > hold
  0.271 > frequency 0.205 (U56, 10 bps); B136 0.396 / 0.300 / 0.192. The tail is ordered by drag.
- **H_HOLD FAIL as stated, and the FAIL is the answer.** The f-span at H=0 (1.990) is dominated by
  one cell: the daily null at H=0 turns over 239x/yr and pays **2,390 bp/yr**, which is 1059's and
  1060's "the D/W redrawn null is not a comparand" measured again. Drop that single cell and the
  two dials are interchangeable: **W→Q at H=0 spans 0.428, H 0→126 at f=W spans 0.399.** Hold
  length and rebalance frequency are the same axis wearing two labels.

## THE REFUTED HALF: min hold does NOT move the null's drawdown, but it DOES move a book's

Declared before any number: *H moves L_DD, f moves nothing once drag is charged.* The second half
holds; **the first is refuted for the null and confirmed for the books.**

- **H_LDD FAIL.** The null's L_DD failure share at f=W runs 0.95 / 1.00 / 0.90 / 0.95 / 1.00 over
  H (span 0.10 — two draws in twenty, inside the grain), and its **median MaxDD is flat at −0.22
  to −0.24 in 19 of the 20 cells** (the exception is D/H=0 at −0.88, pure cost).
- The books move: U56 mean book MaxDD at f=W runs **−18.70% → −18.76% → −20.32% → −25.91% →
  −19.81%** over H, and at f=D **−18.78% → −25.81%** by H=63. Mechanism: a random book has no
  loser to be stuck with — every name it retains is as good as the one it would have drawn —
  whereas a *selecting* book's retained name is precisely the one its own score wanted to drop.
  **Min hold is a drawdown tax that only a book with selection pays.** That is a real asymmetry
  between the book and its own null, and it runs in the direction that penalises the book.

## THE BOOKS: min hold buys back the turnover rebate, and pays for it in drawdown

U56 mean book Sharpe (3 mechanisms):

| f \ H | 0 | 5 | 21 | 63 | 126 |
|---|---|---|---|---|---|
| D | 0.960 | 1.066 | 1.127 | 1.093 | 1.072 |
| W | 1.051 | 1.064 | 1.114 | 1.111 | **1.156** |
| M | **1.183** | 1.183 | 1.086 | 1.122 | 1.074 |
| Q | 1.031 | 1.031 | 1.031 | 1.123 | 1.142 |

U56/CAND20 walking H at f=W: CAGR **12.73 → 13.11 → 14.35 → 14.95 → 15.58%**, turnover
**10.79 → 9.85 → 6.14 → 3.87 → 2.90**/yr, MaxDD −18.31 → −18.48 → −20.24 → −25.69 → −19.13%.
At H=126 the weekly book reaches the monthly book's return on **a quarter of the turnover** — and
still does not clear 4a.

## RULE 8 (2009–2016 chooses the (f, H) point, 2017–2026 read once)

| panel | mech | chooser | pick | OOS best | OOS CAGR | OOS Sharpe | OOS MaxDD | OOS 4b |
|---|---|---|---|---|---|---|---|---|
| U56 | CAND20 | C_ISSHARPE | D/H21 | M/H0 | 15.00% | 1.1024 | −20.19% | yes |
| U56 | CAND20 | default W/H0 | W/H0 | M/H0 | 14.34% | 1.1252 | −18.31% | yes |
| U56 | MOMONLY | C_ISSHARPE | W/H126 | W/H126 ✓ | **17.37%** | 1.1575 | −20.58% | no |
| B136 | CAND20 | C_ISSHARPE | M/H21 | M/H126 | 15.92% | 0.9998 | −27.14% | no |

Comparands: **RULES v2 (live)** U56 OOS 9.45% / 1.2762 / −12.05% (full 8.62% / 1.2007 / −12.05%,
halves 1.232 / 1.176); B136 OOS 7.88% / 1.1059 / −12.24%. **SPY** OOS 15.21% / 0.8711 / −33.72%
(full 15.10% / 0.8829 / −33.72%).

**H_RULE8 PASS on the stated bar but the reading is negative**: the IS-chosen cell's mean OOS
Sharpe is 1.0421 against the default W/H=0's 1.0006 (+0.0415), while its **hit rate on the OOS-best
cell is 1 of 6 (0.167)** and its **OOS 4b pass rate FALLS, 0.167 against the default's 0.500**. The
free parameter buys 0.04 of Sharpe and sells a verdict — idea 953's finding, on a new dial.

## KEEP paths

**4b 25 of 120, 4a 0 of 120, BOTH 0** at 10 bps. Every 4b passer carries 19–27% of drawdown against
the live book's 12.05%. Best OOS 4b passers on U56: M/H0 and M/H5 CAND20 (identical: full 15.26% /
1.2121 / −19.51%, halves 1.204 / 1.227, OOS 17.50% / 1.3057 / −19.51%) — already-committed cells —
and **W/H126 CAND20 (full 15.58% / 1.1397 / −19.13%, halves 1.204 / 1.097, OOS 16.97% / 1.1643 /
−19.13%, turnover 2.90/yr)**, which is new and is **PARK, not KEEP**: it fails 4a, no IS-only
chooser picks it for CAND20, and its Sharpe sits below the monthly incumbent's.

## VERDICT

**ANSWERED: the base rate does NOT depend on hold length separately from turnover.** At matched
drag the rebalance frequency is worth a median 0.032 of the null's p90 Sharpe over 39 pairs, and
the two dials span the same range (0.428 vs 0.399) once the 2,390 bp/yr daily null cell is removed.
**KILL** the reading that 926's residual 2.31x gap is a reaction-speed effect — it is the daily
null's own churn. **KILL** the declared prediction that min hold raises the *null's* L_DD (span
0.10, median MaxDD flat at −0.22 in 19 of 20 cells) and **CONFIRM** it for *books* (up to 7 pp of
MaxDD), which is a book-versus-null asymmetry the record has not priced. **PARK** W/H126 as a
low-turnover 4b passer. Gates 6 of 6, hypotheses 3 of 6, nothing promoted.

**Resolution caveat, stated:** 20 draws per null cell put the base rate's grain at 0.05, so
base-rate differences below ~0.15 are not resolvable (the record's own ideas 1011/1041 point). The
η² of the *base rate* on frequency (0.803 on U56, but 0.177 on B136) sits on that grain and is not
read as a result here; the p90 Sharpe, a continuous statistic, is.

Survivorship: U56/B136 are current-constituent panels; the bias is common to books and null and
flatters both the CAGR floor and the DD cap against SPY, which is a real index series.
