# idea 200 — back-fill-the-swapped-coefficient-audit (lane B, 2026-09-05)

**ANSWER: ZERO of idea 168's published verdicts move. The exposure is real, strictly permissive, and
worth 41 of 352 books (-35.7%) on the corpus-wide OOS-window read — but at the site the defect
actually touched it changes the failing-bar SET in 5 of 16 arm-cells and the PASS/FAIL VERDICT in
0 of 16, because every arm already failed on a bar the swap does not move. Idea 168's headline
sentence survives verbatim. No RULES change, no new book, no KEEP candidate.**

Script `research/backtests/2026-09-05_back-fill-the-swapped-coefficient-audit_B.py` (365 s).

## The defect, stated exactly

`C.margins_at(r, b, phi, delta, which)` computes `DD = delta·|SPY MaxDD| − |book MaxDD|` and
`CAGR = book CAGR − phi·SPY CAGR`. PROTOCOL 4b says MaxDD ≤ **60%** of SPY's and CAGR ≥ **70%** of
SPY's, i.e. `phi=0.70, delta=0.60`. Idea 168 line 515 passes `(0.60, 0.70)` — **both coefficients
loosened**. On the OOS window that is a DD cap of 23.60% instead of 20.23% (looser by 3.37pp) and a
CAGR floor of 9.27% instead of 10.82% (looser by 1.55pp).

## Reproduction, asserted before any new number

- Idea 168's committed `.grid.csv`: **352 of 352 rows matched**, worst numeric gap **3.55e-15**
  across all 11 numeric columns; `pass4a`, `pass4b` and `failing` identical **352/352**.
- The site itself: all **16/16** published `OOS_4b_fail` strings reproduced **exactly** under the
  swapped pair, OOS Sharpe gap **1.11e-16**. The line-515 read is reconstructed, not inferred.
- **The full-sample `pass4b` column is NOT exposed.** It goes through `H.margins`, which hard-codes
  0.60/0.70 in the correct roles; the 47/352 full-sample 4b count is unchanged and was never at risk.
  Only the OOS-window read is.

## (1) The site — 0 of 16 verdicts move

| arm | clears PUBLISHED | clears CORRECT | bar-set moves |
|---|---|---|---|
| A_LIVE (k=−0.50) | 0/4 | 0/4 | 0 |
| A_ZERO (k=0) | 0/4 | 0/4 | 2 |
| A_ISK | 0/4 | 0/4 | 1 |
| A_ISKS | 0/4 | 0/4 | 2 |

All five bar-set moves are on **broad** and all five add **DD** (one also adds CAGR:
broad@25bps A_ZERO, `H1|H2` → `H1|H2|DD|CAGR`). Every arm was already failing on H1, H2 or CAGR,
bars the swap leaves untouched — so the defect bought idea 168 nothing it published.
Idea 168's headline sentence re-read at PROTOCOL's bars: *"IS-chosen k beats k=0 on OOS Sharpe 4/4
(+0.084)"* → **4/4, +0.0839, UNCHANGED**; *"k=−0.5 loses 0/4 (−0.299)"* → **0/4, −0.2986,
UNCHANGED**; *"but fails the OOS-window 4b bars 4/4"* → **fails 4/4 at PROTOCOL's bars, UNCHANGED**.

## (2) The corpus — 41 of 352 verdicts move, all in one direction

OOS-window 4b passes **115/352 (32.7%) → 74/352 (21.0%)**, a **−35.7%** change; the failing-bar set
moves in 130/352, the verdict in **41/352 (11.6%)**. By cell: u56@10 49→33, u56@25 31→22,
broad@10 29→19, broad@25 **6→0**. Newly-binding bar among the 41: **DD 27 (65.9%), CAGR 14 (34.1%),
H1/H2 0**.

**Monotonicity asserted, not assumed:** 0/352 books have a larger DD margin under the correction,
0/352 a larger CAGR margin, and **0/352 flip FAIL→PASS**. The defect is *strictly permissive* —
every verdict it can move, it moved toward admitting a book PROTOCOL's bars reject. This is the
opposite sign to idea 178's finding on idea 165, where the defect **cost** the idea.

**The inflation is concentrated where idea 168 already warned:** by exponent, passes fall 17→6 at
k=+1.00, 17→9 at k=+0.75, 14→8 at k=+0.50, against 2→0 at k=−1.00 and 4→1 at k=−0.50. The defect
flatters the **positive-k half**, which idea 168 itself labelled survivorship-inflated and an upper
bound. Correcting it makes idea 168's own caveat stronger, not weaker.

## (3) The two tuned parameters — all 25 (φ, δ) points

OOS-window 4b passes / 352 (rows φ = CAGR floor, cols δ = DD cap):

| φ \ δ | 0.40 | 0.50 | 0.60 | 0.70 | 0.80 |
|---|---|---|---|---|---|
| 0.50 | 0 | 7 | 88 | 115 | 123 |
| 0.60 | 0 | 7 | 88 | **115** *(defect)* | 123 |
| 0.70 | 0 | 4 | **74** *(PROTOCOL)* | 101 | 109 |
| 0.80 | 0 | 2 | 52 | 79 | 87 |
| 0.90 | 0 | 2 | 32 | 57 | 65 |

Displacement **+41 books** against a full-surface span of **123**, so the swap is a third of the
whole dial's reach — not a rounding error. On the **16 site cells** the surface is **0 everywhere
except δ=0.80 (3 passes), for every φ**: at the site the CAGR half of the swap never binds at all,
and the DD half only binds beyond the swap's own magnitude. That is the mechanism behind the 0/16.

## (4) Both KEEP paths and rule 8

4a **129/352**; full-sample 4b **47/352** (unexposed, unchanged). Books clearing full-sample 4b AND
the corrected OOS-window 4b: **46** — and **46** under the defect too, so **+0 books were admitted
into the joint set by the defect**. Rule 8 (chosen ≤2016-12-31, 2017–2026 read once, 4 cells):
mean OOS A_ISK 17.92%/**0.9144**/−25.32%, A_ZERO 14.75%/0.8305/−23.16%, A_ISKS 16.10%/0.8453/−23.94%,
A_LIVE 5.34%/0.5319/−17.31%; A_ISK−A_ZERO **+0.0839, 4/4**. Benchmarks OOS: RULES v1 u56@10
7.73%/0.7471/−13.83%, broad@10 5.94%/0.5763/−21.19%; SPY 15.45%/0.8820/−33.72%. **No arm clears the
OOS-window 4b under either coefficient order (0/16 → 0/16).**

## (5) Exposure re-swept today

62 `margins_at` call sites across 22 scripts: **59 swept/non-literal, 3 SWAPPED** — the same three
idea 178 named (`required-gross-as-a-leaderboard-column_cloud.py` lines 626/641; `the-sign-is-the-
parameter-not-the-share_cloud.py` line 515). No new exposure has appeared. **With idea 178 having
priced lines 626/641 and this run pricing line 515, all three exposed sites are now priced and the
exposure idea 176 opened is closed: no published verdict in the record moves.**

Predictions **P1–P6 all HIT** (P4 scored on the 16 site cells as pre-registered; the same clause
read on the 352-book corpus is FALSE — 27 of 41 movers bind on DD, 14 on CAGR — reported unscored).

**No KEEP candidate. RULES v1 untouched. `RULES.md`, `scan.py`, `bot.py`, `baseline.py` unmodified.**
