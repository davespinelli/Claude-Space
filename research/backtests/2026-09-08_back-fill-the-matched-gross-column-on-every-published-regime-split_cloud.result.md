# Idea 471 — back-fill-the-matched-gross-column-on-every-published-d_on/d_off-regime-split (cloud lane, 2026-09-08)

Script `2026-09-08_back-fill-the-matched-gross-column-on-every-published-regime-split_cloud.py`,
console `…_cloud.console.txt`, artefacts `…census.csv` / `…census_rejects.csv` /
`…restated.csv` (864 claims) / `…books.csv` (1,764 books) / `…walkforward.csv`.
10 and 25 bps rungs, weekly cadence, next-day execution.

**VERDICT: SPLIT — the queue's premise is CONFIRMED for the ALWAYS-ON regime splits and
REFUTED for the CONDITIONAL ones. No KEEP, no RULES change.**

---

## Q1 — the census: how many published regime splits are there?

Every committed CSV (2,015) scanned for a matched ON/OFF column pair reporting the same
statistic for two complementary states of time, plus a regime witness column. Three-way,
nothing hidden:

- **ADMITTED: 4 regime-split *delta* claims, over 3 files, 1,890 published rows — and all
  three files come from ONE parent script** (idea 246-C
  `does-every-regime-conditional-dial-lose-its-own-regime`): `.mechanism.csv` (d_on/d_off,
  432 rows), `.decomp.csv` (d_on/d_off and d_cond_on/d_cond_off, 432), `.grid.csv`
  (d_cond_on/d_cond_off, 594).
- **1 of the 4 publishes any gross column at all, and 0 of 4 publish BOTH an arm and a
  control gross** — so the confound idea 249 found is **not checkable from any committed
  artefact in the record**. That is the census's real finding: the missing column is
  missing everywhere it matters.
- **REJECTED: 92 pairs, each logged with its reason** — 64 have no regime witness, so the
  on/off names a DIAL state, not a time state (`CAGR_on`/`CAGR_off` for "the vol scaler on
  vs off", `dGross_on`/`dGross_off` for a turnover constraint); 28 are genuine time-state
  splits that are not arm-minus-control deltas (`vol_in`/`vol_out`, `closer_hi`/`closer_lo`),
  so there is no control whose gross could be matched.

Idea 249's own `.mech.csv` is excluded by construction: it already carries
`d_*_vs_matched` beside `d_*_vs_control` and never uses an on/off column pair. It is the
one place in the record where the column already exists.

## CHECKS

- **(a)** All 432 `.mechanism.csv` rows reproduce from idea 246-C's own committed code;
  max |d_on − reproduced| **6.6e-05**, max |d_off| **3.1e-03** pp/yr. The `.grid.csv` join
  covers 432 of 576 because 144 of its conditional rows are the `regime='always'` arm,
  which is not a regime split.
- **(a2)** Not bit-exact, and the cause is located rather than asserted: the same residual
  is already in the **CONTROL** rows — no instrument, no regime, no code of this run —
  max |dSharpe| **5.4e-04**, exactly equal in 9 of 18 cells, gross max |d| 2.6e-08. The
  residual is upstream: the cached price panel moved under the record, the same cause idea
  468 recorded at max |dCAGR| 2.9e-05. **Every number below is this run's own
  re-computation of both sides**, never a published number differenced against a fresh
  one, so the residual cannot leak into the restatement.
- **(b)** The gross-matched static is solved to the arm's own realised mean gross in every
  one of **864** cells: worst |achieved − target| **9.913e-05** against a 1e-4 tolerance.

## THE MISSING COLUMN, BACK-FILLED

Mean realised gross, arm vs its published full-gross control (0.7495), pooled over 54
cells each:

| instrument | always-on arm | conditional arm | control |
|---|---|---|---|
| gross50 | **0.3750** | 0.7003 | 0.7495 |
| ddctl8 | 0.5505 | 0.7112 | 0.7495 |
| band3-dg / g200-dg / abs12-dg | 0.648 | 0.720–0.725 | 0.7495 |
| vol60-dg | 0.6873 | 0.7344 | 0.7495 |
| stop15 / stop25 | 0.738 / 0.746 | 0.745 / 0.748 | 0.7495 |

**538 of 864 claims (62.3%) compare an arm and a control whose mean realised gross differs
by more than 0.01 NAV**; median |gap| 0.0206, max **0.3749**.

## HOW MANY PUBLISHED REGIME CLAIMS SURVIVE?

Sign survival of the individual deltas is high — that is not where the damage is:

| | d_on sign | d_off sign | both | ordering (d_on vs d_off) |
|---|---|---|---|---|
| always-on (432) | 82.9% | 85.0% | 74.8% | 73.8% |
| conditional (432) | 85.0% | 66.7% | 59.7% | 72.9% |

**The claim these files actually make is the GAP — "the instrument is dearer/cheaper in
its own regime" — and that is where the two modes part company:**

- **ALWAYS-ON: gap published mean +2.308 pp/yr → restated −0.694. The pooled sign
  INVERTS, and 69.9% of the published magnitude is gross arithmetic.** Positive cells go
  165/432 → 204/432.
- **CONDITIONAL: gap published mean −2.690 → restated −2.608. Only 3.0% of the magnitude
  is gross arithmetic — the conditional splits survive.**

The mechanism is exactly the gross gap. `gross50` always-on holds 0.375 against the
control's 0.750, and its published d_on collapses from **+4.7223 to +0.1855 pp/yr** pooled;
on idea 246's own headline cell (u56 / EWall / 10 bps / spy200) it goes **+6.4062 →
+0.0051**, i.e. **99.9% of the published crash-day surplus was holding half a book while
the market fell**, which the matched static also does, for free. `ddctl8` always-on goes
+1.3986 → −0.9038. The conditional arms sit at a 0.002–0.049 gross gap and barely move
(`gross50` cond: d_on −1.8833 → −2.9791 on the same cell).

By regime, the always-on ordering claim survives **91.0% on hivol80, 72.9% on breadth20
and only 57.6% on spy200** — spy200 is the regime whose ON days are precisely the days a
de-grossed book wins by construction.

## L2 — rule 8 (instrument × regime chosen on 2009-2016 IS Sharpe, 2017-2026 read once)

Menu includes do-nothing and every gross-matched static. Over 18 (panel × book × rung)
cells: the IS pick is a **live conditional instrument in 16, a matched static in 2, and
do-nothing in 0**. OOS against do-nothing: **mean +0.0188 but median −0.0004, wins 8/18.**
Against the best matched static: **mean +0.0145, median −0.0025, wins 8/18** — a coin
flip. Mean OOS regret vs the oracle +0.0500. The pick beats RULES v2 OOS in **7/18** and
SPY in **7/18**.

## L3 — both KEEP paths on every arm AND every matched control (1,746 books)

**4a 0/1746.** 4b **137/1746**: always-on 33, conditional 88, matched statics 16, control
0. Binding bars DD 1193 / H2 1087 / OOS 1075 / H1 980 / CAGR 963.

**118 of the 121 arm 4b passes are NOT shared with the arm's own gross-matched twin** —
those are the only passes a regime instrument can claim credit for, and they are
concentrated in `vol60-dg` (always-on) and the de-gross gates (conditional).

Best of them: **u56 / EWall / 10 bps `cond:band3-dg@hivol80` — CAGR 12.22%, Sharpe 1.2116
(H1 1.2333 / H2 1.1919), OOS Sharpe 1.2831, MaxDD −15.50%**, failing 4a on drawdown only.
This is an independent reproduction of the arm **idea 247 already has PARKed** (queue: u56
@10 bps 12.2% / 1.21 / −15.5%, halves 1.23/1.19, OOS 1.2831). This run adds one fact to
that PARK — the arm survives its own gross-matched control — and changes nothing else:
idea 247's reason to park it stands (the expanding 80th-percentile vol regime arms 3.3% of
IS days against 17.1% of OOS days, so rule 8 selected it on ~66 armed IS days). **Not
promoted, no memo.**

## Caveats

SURVIVORSHIP: current constituents only, hardest on the small panel; the 44 small-cap
tickers with `max_1d_move >= 1.0` are dropped first and SPY is a benchmark there, never
held. The census can only see what was committed as CSV: a regime split published only in
a console file or a memo is invisible to it, and the rejection log is the honest account
of the boundary. The restatement covers the record's regime-split population exactly
because that population is one parent script's output — a fact about the record, not a
choice of scope.
