# Idea 878 — does EVERY committed 4b DD pass sit on a POST-2017 drawdown, and is a pre-2017-only DD cap estimable at all?

**ANSWERED: NO to both halves of the queue's premise. (1) 8 of 9 committed 4b passes trough on the
2020 crash, but one troughs in NOVEMBER 2011 — idea 808's "252 of 252" does not hold on the real
shelf (37 of 45 books here), and on the never-selected GRID it is 29 of 36. (2) A pre-2017-only DD
cap IS estimable: it is −13.24% against the published −20.23%, and 7 of the 9 committed passes clear
that tighter cap IN SAMPLE.** Cloud lane, 2026-09-15, idea 2 of 2. Gates 3/3 + G4 reported as a
count. **KILL for capital** — no new book, nothing promoted.

## Gates
| gate | result |
|---|---|
| G1 all 9 SHELF books reproduce their committed memo triple | **PASS** |
| G2 `fast_run` vs `engine.backtest` | **PASS**, max abs return diff **8.674e-18** |
| G3 SPY comparand vs the record's committed triple | **PASS** — 15.13% / 0.885 / −33.72% |
| G4 idea 808's claim, re-read on this book set (not assumed) | full MaxDD == OOS MaxDD on **37 of 45**; == IS MaxDD on **8 of 45**. 808 published 252/252 and 0/252. |

## 1. Where the binding drawdown actually troughs (10 bps, PROTOCOL split)
| book | full MaxDD | trough | peak | IS MaxDD | OOS MaxDD | post-2017 |
|---|---|---|---|---|---|---|
| u56-v2band-gross100 | −15.91% | 2020-03-12 | 2020-02-19 | −10.45% | −15.91% | yes |
| u56-band008-gross100 | −19.05% | 2020-03-12 | 2020-02-19 | −11.22% | −19.05% | yes |
| u56-top20-band-m20 | −18.31% | 2020-03-12 | 2020-02-19 | −11.65% | −18.31% | yes |
| u56-marsrespread-gross075 | −18.65% | 2020-03-18 | 2020-02-19 | −10.87% | −18.65% | yes |
| u56-quantile50-respread-M | −19.75% | 2020-03-20 | 2020-02-19 | −10.63% | −19.75% | yes |
| b136-r620-gross065-W | −19.43% | 2020-03-20 | 2020-02-19 | −10.15% | −19.43% | yes |
| b136-qroll-q012-w1008-d050-g100 | −17.31% | 2020-03-31 | 2020-02-19 | −15.07% | −17.31% | yes |
| **u56-k8-qroll-q017-w1008-d100-g100** | **−14.79%** | **2011-11-25** | **2011-04-29** | **−14.79%** | −12.72% | **no** |
| u56-top20-g065-M | −17.11% | 2020-03-16 | 2020-02-19 | −10.38% | −17.11% | yes |

`H_POST` **FAILS** at 8/9. Eight of the nine books fall from the *same peak*, 2020-02-19, and trough
within 19 days of each other: the 4b DD leg on the shelf is very nearly one number about one month.
But it is not literally universal, and the exception is not a marginal book — it is
`u56-k8-qroll-q017-w1008-d100-g100`, the shelf's **shallowest** drawdown (−14.79%) and, from this
run's sibling (idea 891, committed today), the shelf's **largest** margin-over-calendar-spread ratio
(1.925). The one book whose DD leg rule 8 could have fitted is the one book whose DD leg is most
robust to the rebalance calendar. Trough-year census: SHELF {2011: 1, 2020: 8}; GRID {2011: 3,
2016: 4, 2018: 1, 2020: 28}.

`H_SPLIT` **FAILS**: the share is 89% (8/9) at every split date in the grid — flat, but below the
90% bar at all four, so the result is not a property of PROTOCOL's own 2017 split. On the GRID the
share moves with the split (33/36 at 2015 and 2016, 29/36 at 2017 and 2018).

## 2. The pre-2017-only cap is estimable, and it is much tighter — `H_UNEST` FAILS
SPY's full-sample MaxDD is −33.72% (trough 2020-03-23), so the published cap is **−20.23%**. SPY's
**in-sample** MaxDD is −22.06% (the 2011 decline), so an IS-only analyst's cap is **−13.24%** — and
that number is identical at all four split dates, because SPY's in-sample drawdown is the 2011 one
in every case.

| set | n | clears published cap | clears IS-only cap (2015 / 2016 / 2017 / 2018) |
|---|---|---|---|
| SHELF | 9 | **9/9** | 7/9 / 7/9 / **7/9** / 7/9 |
| GRID | 36 | 29/36 | 15/36 / 14/36 / **13/36** / 13/36 |

So the queue's second clause is answered plainly: the cap is estimable pre-2017, it is 6.99 pp
tighter than the published one, and **7 of the 9 committed passes would have cleared it**. The two
that would not are `b136-qroll-q012-w1008-d050-g100` (IS −15.07%) and
`u56-k8-qroll-q017-w1008-d100-g100` (IS −14.79%) — again the 2011-trough book.

## 3. The direction of the IS-cap's error — near one-directional, but split-dependent
| rung | split | TP | FP | FN | TN | accuracy |
|---|---|---|---|---|---|---|
| 10 | 2015-01-01 | 21 | **1** | 17 | 6 | 0.600 |
| 10 | 2016-01-01 | 21 | 0 | 17 | 7 | 0.622 |
| 10 | 2017-01-01 | 20 | 0 | 18 | 7 | 0.600 |
| 10 | 2018-01-01 | 20 | 0 | 18 | 7 | 0.600 |
| 25 | 2015-01-01 | 21 | **1** | 16 | 7 | 0.622 |
| 25 | 2016-01-01 | 21 | 0 | 16 | 8 | 0.644 |
| 25 | 2017-01-01 | 19 | 0 | 18 | 8 | 0.600 |
| 25 | 2018-01-01 | 19 | 0 | 18 | 8 | 0.600 |

`H_PRED` **FAILS** (0.600 vs a 0.70 bar), but the failure is entirely on one side: **FN 16–18
against FP 0–1**. The IS-only cap almost never certifies a book that later breaks the published cap;
it rejects roughly half the books that would have cleared it. The single false positive at the 2015
split is `B136-qroll-q0.17-w252-d1.00` (GRID, not a committed pass), whose full MaxDD is −22.88% and
whose trough is **2016-02-08** — i.e. it is a false positive only because a 2015 split hides that
drawdown from the estimator. **"Zero false positives" is therefore a statement about the 2016/2017/
2018 splits, not a property of the cap**, and this run does not claim it as one.

## 4. Rule 8 (PROTOCOL rule 8) — choose on 2009–2016, evaluate 2017+ untouched
**9 of 45 books clear all four 4b legs in sample** (SHELF 5/9, GRID 4/36) — so the IS 4b band is
*not* empty on this book set, contrary to idea 809's pattern on width and gross bands. The IS-only
best-IS-Sharpe chooser picks:

| | IS 2009–2016 | OOS 2017+ |
|---|---|---|
| **SHELF pick — b136-r620-gross065-W** | 15.56% / 1.254 / −10.15% | **14.52% / 1.040 / −19.43%** |
| GRID pick — B136-band0.08-g1.00 | 11.80% / 1.142 / −11.67% | 11.05% / 1.097 / −19.50% |
| SPY | — | 15.33% / 0.877 / −33.72% |
| RULES v2 (live) | — | 7.88% / 1.106 / −12.24% |

Both picks: OOS **4b PASS**, OOS **4a FAIL**. `H_WF` **PASS**. Note the convergence with this run's
sibling (idea 891): two different IS-only choosers — one on min margin-over-spread ratio, one on IS
Sharpe — land on the same book, `b136-r620-gross065-W`, and it clears 4b out of sample both times.
It is already memo-backed (2026-09-12); nothing new is promoted here.

## 5. Cost-rung control
At 10 and 25 bps alike: post-2017 troughs 8/9, clears published cap 9/9, clears IS cap 7/9. The
window a drawdown troughs in does not move with the cost rung.

## Verdict — **KILL for capital**
No new book, no rules change proposed, nothing promoted. The run refutes both halves of the premise
it was given: the DD leg is *nearly* a post-2017 object but not universally one (8/9 shelf, 37/45
pooled, against 808's 252/252), and a pre-2017-only cap is not merely estimable but tighter and
almost purely conservative. What survives as usable: **an IS-only DD screen at 0.60 × SPY's IS
drawdown is a safe pre-filter** — at the 2016/2017/2018 splits it certified no book that later broke
the published cap — but it is a screen that discards about half of what would have passed, and its
one leak shows the guarantee belongs to the split, not to the rule.

**SURVIVORSHIP:** U56 (`research/universe.json`) and B136 (`research/universe_broad.json`) are
CURRENT-constituent lists, so every drawdown level above is optimistic — names that delisted or went
to zero are absent from both the books and the panel. The reported objects (which window a trough
falls in; the IS-vs-full cap gap) are computed on the same biased panel throughout.

Artifacts: `.py`, `.console.txt`, `.books.csv` (90 book × rung rows), `.walkforward.csv`.
Modifies nothing. RULES.md, PROTOCOL.md, scan.py, bot.py, baseline.py untouched.
