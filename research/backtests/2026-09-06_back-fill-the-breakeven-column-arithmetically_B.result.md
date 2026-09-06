# Idea 269 — back-fill-the-breakeven-column-arithmetically-not-by-re-running (lane B, 2026-09-06)

**ANSWERED, and a SPLIT verdict.** The *arithmetic* works better than idea 269 assumed: the
law needs **three** committed numbers per arm, not four (vol is recoverable from CAGR and
Sharpe to **4.0e-4 median relative error**, 98.6% within 1% on 10 061 committed triples),
and it reproduces measured breakevens on the record's **non-null** dials at **R² 0.9990 IS /
0.9994 OOS**, median error **0.015 / 0.017 bps**, over 1 191 / 1 257 flipping pairs spanning
turnover ratios **0.06x–34x**. Both pre-registered bars are cleared.

**But the back-fill's REACH is the binding constraint, and it is small.** Only **315 of 2 238
distinct** leaderboard rows (14.1%) can be back-filled, because the leaderboard publishes no
turnover and **74% of its rows have a parent that committed none either**. Of the 305 distinct
non-degenerate rows that can be priced, **13 (4.3%)** have a breakeven inside PROTOCOL's own
(0, 25] bps range — i.e. 4.3% of the priceable published verdicts are cost-created or
cost-destroyed rather than robust. Idea 269's premise that the column "can be back-filled over
the leaderboard" is therefore **half right**: the formula is sufficient, the *record* is not.

No RULES change, no new KEEP-candidate, no PROTOCOL change (that is a Sunday-review matter).
Nothing in `RULES.md`, `scan.py`, `bot.py` or `baseline.py` touched.

Script `2026-09-06_back-fill-the-breakeven-column-arithmetically_B.py` · console `…_B.console.txt` ·
grids `…_B.{schema,rows,baselines,backfill,sensitivity,validation,volrecovery,grid,keep,walkforward}.csv[.gz]`

---

## 0. Identities asserted before any result was read

| check | result |
|---|---|
| derived rung vs a live `backtest(cost_bps=c)` (3 books × 3 rungs) | `max|live − derived| = 0.000e+00` |
| closed-form `Sharpe(c)` from 5 moments vs the re-summed series (3 books × 5 rungs) | `4.441e-16` |
| reproduction `U56/RULES v1` weekly @10 bps | **6.45% / 0.664 / −13.83%**, halves 0.641/0.688 (published 6.5%/0.666/−13.8%) |
| reproduction `U56/FIXED20` (idea 73's literal `GROSS/n`) | **12.66% / 1.092 / −18.31%**, halves 1.088/1.102 (published 12.7%/1.093/−18.3%) |

The moment identity is what makes the run affordable: `mean(c) = m0 − k·mt` and
`var(c) = Sxx − 2k·Sxt + k²·Stt` with `k = c/1e4`, so a 1 200-point cost ladder costs five
scalars per book instead of 1 200 re-summations of a 4 400-day series.

## 1. THE CENSUS — what the record actually commits

`LEADERBOARD.md` holds **3 753** data rows across 190 script cells. **1 515 of them are
byte-identical duplicates of another row** (2 238 distinct) — a pre-existing rebase artefact,
not created here; every count below is given on both.

| tier (by the parent script's committed schema) | rows | share |
|---|---|---|
| **A** turnover + Vol + Sharpe in one file | 387 | 10.3% |
| **B** turnover + Sharpe + CAGR (Vol recoverable — see §2) | 749 | 20.0% |
| **C** turnover only | 114 | 3.0% |
| **D** a CSV, but no turnover column anywhere | 847 | 22.6% |
| **E** no committed CSV at all | 1 656 | 44.1% |

The tier is necessary but not sufficient: the leaderboard row must also be *joined* to a grid
row. The join is a numeric fingerprint — (CAGR, Sharpe, MaxDD) at the leaderboard's own printed
precision, searched only inside the parent script's own CSVs:

* 2 917 rows print all three numbers;
* **704** match ≥1 committed grid row; **684** of those pin an unambiguous turnover
  (369 with Vol committed outright, 315 needing recovery); 20 remain ambiguous.

**So the arithmetic is never the bottleneck — the missing turnover column is.**

## 2. THE VOL RECOVERY — the law needs three numbers, not four

`engine.metrics` defines `Sharpe = mean_ann/vol` and `CAGR` from compounded daily returns, so
`ln(1+CAGR) = mean_ann − vol²/2 + O(m₃)` and vol is the **positive root** of
`vol²/2 − Sharpe·vol + ln(1+CAGR) = 0` (discriminant `(Sharpe−vol)² ≥ 0`; for `Sharpe < 0` the
admissible root is the upper one — the naive smaller root is what makes the identity look
broken on losing books).

Tested against **every** committed (CAGR, Sharpe, Vol) triple in the corpus — 10 061 rows from
16 CSVs, this run's own outputs excluded:

| statistic | value |
|---|---|
| median \|relative error\| | **3.96e-04** |
| p90 / p99 / max | 8.45e-04 / 2.59e-02 / 9.80e-01 |
| median \|absolute error\| | 4.6e-05 vol points |
| within 1% relative | **98.63%** (pre-registered bar: ≥95% → **USABLE**) |
| within 0.1% relative | 92.59% |

All **138** failures sit at *positive* Sharpe in 8 files — they are the third-moment term the
lognormal step drops, not the sign ambiguity. This is the run's most portable single result:
**the record's Vol column is redundant**, so tier B joins tier A and the reachable set doubles.

## 3. THE COMPARAND

Each row's own published baseline (the "Baseline Sharpe (H1/H2)" column) is identified
mechanically by fingerprinting that triple against RULES v1 and SPY computed live here on
3 panels × 2 cadences × 4 start conventions. The record's earliest rows were run on an earlier
price vintage, so the tolerance is **one printed unit (0.011)** on each of Sharpe/H1/H2, and a
string resolves only if every candidate inside that ball agrees on the same (panel, cadence).

**9 of 566 distinct baseline strings resolve, covering 2 346 of 3 753 rows** — the two dominant
strings are `0.67 (0.64/0.69)` → `v1/U56/W` (resid 0.0051, 1 490 rows) and `0.64 (0.76/0.54)` →
`v1/B136/W` (resid 0.0050, 672 rows). The start-convention spread in the numbers the law
actually consumes is small and is carried through as a sensitivity, not hidden: e.g.
`v1/U56/W` turnover 22.32–23.79x/yr, vol 0.0992–0.1026.

## 4. THE BACK-FILL — the headline

`c* = 10 + dSharpe(10)·1e4 / (T_x/vol_x − T_y/vol_y)`, no row re-run.

| | rows |
|---|---|
| back-filled | **315 distinct** (624 raw) — 14.1% of the distinct record |
| of those, idea 263's >2x turnover-mismatched | 194 |
| degenerate denominator (`|T_x/vol_x − T_y/vol_y| < 1`, arm turnover-matched to its baseline) | 10 |
| **breakeven inside (0, 25] bps** | **13 of 305** non-degenerate (**4.3%**) |
| … of the 194 >2x-mismatched rows | 6 (3.1%) |

`c*` distribution over the 315: median **−16.0 bps**, IQR −23.5 to −10.0, p95 +18.4. A negative
`c*` means the row's sign versus its own baseline **never** flips at a positive cost, i.e. the
published verdict is cost-robust; **that is the overwhelming majority of the record.**

The 13 at-risk rows are concentrated: **9 of them are idea 10's `sector-only-universe` panel
sweep** and 2 are idea 13's `52w-high-proximity`. All 13 are published **KILL 4b** verdicts
whose arm is *lower*-turnover than its baseline, so their (negative) Sharpe gap against v1
closes as costs rise — the cheapest is `ETF24/CAND-n20` at **3.77 bps** and the dearest
`ETF36/CAND-n5` at **20.79 bps**. None is a KEEP that a higher rung would overturn; the exposure
runs the other way, and it is small.

Sensitivity: the in-band count moves 26→28 raw across all four start conventions and is
identical (26 raw) when the recovered vol is forced onto every row instead of the committed one.

## 5. VALIDATION — the law off the nulls (idea 262 fitted it on nulls only)

150 books (3 panels × {`v1`, `EWall`, `FWD`, `FWDVS`, `FIXED`} × cadence D/W/M/Q × n ∈ {5,10,20,40}
× gross ∈ {0.50,0.75,1.00}), all pairs within a panel, exact breakevens by 0.05-bps scan + bisection.

| window | pairs | flip <60 bps | R² committed vol | R² **recovered** vol | median \|err\| |
|---|---|---|---|---|---|
| FULL | 3 675 | 1 258 | 0.9994 | 0.9811 | 0.012 / 0.011 bps |
| **IS** 2009–2016 | 3 675 | 1 191 | 0.9889 | **0.9990** | 0.015 bps |
| **OOS** 2017–2026 | 3 675 | 1 257 | 0.9998 | **0.9994** | 0.017 bps |

Pre-registered bar (b) was R² > 0.90 with recovered vol, IS **and** OOS → **HOLDS**. The law is
not a null-arm artefact; it is an identity of the cost model, and idea 262's R² 0.9989 was if
anything pessimistic.

## 6. RULE 8 WALK-FORWARD (books)

(panel, n) chosen on IS 2009-01-01..2016-12-31 alone — IS-argmax `B136 / FWD n=10 / W / g0.75`
(IS Sharpe 1.056, ahead of BSTK100 n=10 at 1.050 and B136 n=20 at 1.023). OOS read once:

| book | CAGR | Sharpe | MaxDD | H1 / H2 | OOS CAGR | OOS Sharpe | OOS MaxDD |
|---|---|---|---|---|---|---|---|
| **IS-argmax B136/FWD10/W** | 14.25% | 0.895 | −21.4% | 1.118 / 0.710 | 12.77% | 0.781 | −21.4% |
| RULES v1 (B136) | 6.39% | 0.635 | −21.2% | 0.756 / 0.532 | 5.94% | 0.576 | −21.2% |
| SPY | 15.23% | 0.889 | −33.7% | 0.957 / 0.834 | 15.45% | **0.882** | −33.7% |

**KILL** — fails 4b on `H2, OOS, DD` (0.710 < 0.834; 0.781 < 0.882; 21.4% > 60%·33.7% = 20.2%)
and fails 4a on both halves. It beats v1 comfortably and SPY not at all.

## 7. BOTH KEEP PATHS

900 grid points (150 books × 6 rungs) in `.grid.csv`; 169 pass 4a, 148 pass 4b, 284 either.
**14 books pass 4b at PROTOCOL's own 10 bps** — and every one is a book the record already
holds (U56 `FWD20/M` 15.3%/1.213/−19.5% OOS 1.307, `FIXED20/W` = idea 73's, `EWall/M`,
B136/BSTK100 `FIXED40/W`), reached here as controls rather than as findings. **None of them is
the rule-8 pick**, so this run produces **no KEEP-candidate**: the only book selected without
hindsight fails 4b, and the books that pass 4b were not selected.

## 8. What this leaves for the queue

1. The back-fill is cheap and correct but reaches 14% of the record. The lever that would
   matter is **prospective**: a committed turnover column costs one number per grid row and
   moves a row from tier D/E to tier A. Retroactively, 1 656 rows have no CSV at all and are
   unreachable by any arithmetic.
2. `LEADERBOARD.md` carries **1 515 duplicate rows**. Any count ever quoted off that file —
   including several in the record — is inflated unless it de-duplicates.
3. The 13 at-risk rows are all KILLs that soften with cost, and 9 share one parent
   (`2026-09-04_sector-only-universe_C.py`). Re-quoting that one script's panel sweep at
   25 bps would settle most of the record's cost-fragility in a single run.
