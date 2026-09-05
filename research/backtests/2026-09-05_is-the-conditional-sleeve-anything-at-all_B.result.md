# idea 190 — is-the-conditional-sleeve-anything-at-all (lane B, 2026-09-05)

**ANSWERED, and it splits three ways. (i) The published two-sided clause of ideas 181/186 is the
wrong statistic and this run has the exact counter-example. (ii) Under the right statistic the
STATIC sleeve DOES separate from its substitution null — it is the strict argmax of the whole
enumerated population in 72 of 72 points. (iii) That separation is HINDSIGHT and is not available
to an out-of-sample chooser: on the IS window it is the argmax in only 8 of 72, and the triple an
IS rule would actually have picked loses to doing nothing by −0.2509 OOS Sharpe, 0 wins in 12.
KILL of the static sleeve as an asset choice. No new book, no KEEP candidate, RULES untouched.**

**5232 genuine backtests in 538 s.** 2 panels (U56, BROAD136) × base n {10,20,40} × cost {10,25}
× f {0.10,0.20,0.50} × set {S3=TLT/GLD/UUP, S4=+DBC} = 72 real rows, 12 R20 controls, 36 CASH
controls, and **10,344 null rows**. Exactly 2 tuned parameters (f, asset set); panel, n and cost
rung are carried axes on which nothing is ever selected. Base book, sleeve construction (idea
100/104's momentum-vote × risk-parity) and gross rescale are **imported from** the committed
`2026-09-05_sleeve-f-that-clears-the-floor_cloud.py`, not re-typed.

## Why rotation was replaced, and by what

Idea 186's matched null for an overlay rotates its ON indicator. A static sleeve has `s_t ≡ 1`,
so every rotation returns the identical book: the null is the point mass at the real value. The
free parameter a static sleeve actually has is **which assets**, so its matched null is a random
**substitution** — same construction, same f, same cadence, same gross rescale, same name count k,
different tickers.

Two pools, both reported. **DIV** = the 12 non-crypto `bonds_fx_commod` members minus the real
sleeve's own names, so the population is **C(9,3)=84 (S3) / C(8,4)=70 (S4) and is ENUMERATED
WHOLE** — an exact percentile, no seed, no draw band. That is idea 208's proposal 11b applied at
the first opportunity after it was written. **ALL** = every panel column except SPY and the real
names (n=20 only), 200 draws from the **int-literal seed 1902026** (idea 208's proposal 5).

## Reproduction, asserted before any new number was read — 5 of 5

| check | result |
|---|---|
| [a] `fast_backtest` vs `engine.backtest` | max\|dret\| **1.39e-17**, max\|dturn\| 3.3e-16, both panels |
| [b] cost identity (10 bps derived from one 0 bps run) | **1.39e-17** vs a genuine 10 bps engine run |
| [c] this run's blend vs idea 134's `book_weights`, 6 points × 2 panels | **0.000e+00** |
| [d] the 24 committed control-arm rows of idea 134's `.grid.csv` | **24 of 24 matched, max\|d\| 5.0e-16** |
| [e] null matched by construction (name count, disjoint from the real set, realised gross identical on every rebalance date) | **PASS**, 10 draws × 2 panels |

Where the null is **not** exact it is measured, not assumed (idea 186's turnover caveat, the same
discipline): sleeve on-share real 0.9395 vs null [0.9036, 0.9456] — the momentum vote can zero the
sleeve leg, so "always-on" is 94%, not 100%; sleeve share of gross real 0.1633 vs null
[0.1868, 0.2019]; realised turnover ratio null/real [0.937, 0.969].

## (1) The clause as published clears 29.2%. The clause read correctly clears 100%.

| pool | points | two-sided clear (≥95th pct of \|dSharpe\|) | dMaxDD clear | mean signed percentile | strict signed argmax |
|---|---|---|---|---|---|
| DIV (enumerated 84/70) | 72 | **21/72 = 29.2%** | 21/72 = 29.2% | **1.000** | **72/72 full sample** |
| ALL (200 draws) | 24 | 2/24 = 8.3% | 16/24 = 66.7% | 0.897 | 0/24 |

Mean real dSharpe **+0.0493** against a DIV null mean of **−0.0549**: the null draws are
overwhelmingly *harmful*, and the ideas 181/186 statistic — |dSharpe(real)| above every draw —
credits a substitute that **destroys** 0.27 of Sharpe with a larger |dSharpe| than the real
sleeve's +0.10, and blocks it. The DIV null mean is negative in **100.0%** of the 72 points. A
two-sided clause is right for a tilt whose null is symmetric and wrong here.

## (2) …and the signed reading is exactly what hindsight produces

| window | real sleeve is the strict argmax of its own enumerated DIV population |
|---|---|
| full sample 2009–2026 | **72 / 72** |
| IS window ≤ 2016-12-31 | **8 / 72** (mean percentile 0.921) |
| OOS window 2017–2026 | 48 / 72 (mean percentile 0.993) |

TLT/GLD/UUP is the best of 84 diversifier triples over the whole sample and the best of 84 over
2017–2026, but the best over 2009–2016 only 11% of the time. A chooser standing in 2016 with the
project's own IS-Sharpe rule would not have picked it.

## (3) The drawdown half of the sleeve is a cash carve-out with three tickers on it

| vs R20, mean over 72 points | sleeve | cash at the same f |
|---|---|---|
| dSharpe | **+0.0493** | −0.0017 (sleeve better 72/72) |
| dMaxDD | +0.0610 | **+0.0608 — cash captures 98.4% (median)** |
| dCAGR | −2.54 pp | −3.84 pp |

Stable across f (cash captures 93.7% / 94.8% / 104.6% at f = 0.10 / 0.20 / 0.50). The sleeve's
**drawdown** improvement is de-grossing (ideas 66/184); its **Sharpe** improvement is the assets —
and (2) says that part is not selectable.

## (4) Rule 8, 12 cells, 2017–2026 read once — the do-nothing streak survives, but only just, and only because of (2)

| arm | mean OOS Sharpe | paired vs S0 | wins | OOS CAGR | OOS MaxDD | OOS 4a | OOS 4b |
|---|---|---|---|---|---|---|---|
| **S0 do nothing (R20)** | **0.9805** | — | — | **14.75%** | −24.28% | 3/12 | 0/12 |
| S1 IS-argmax sleeve (assets **given**) | 1.0504 | **+0.0699 (t +6.85)** | **12/12** | 9.21% | −12.72% | 11/12 | 1/12 |
| S2 clause-gated argmax | 0.9917 | +0.0112 (t +1.83) | 3/12 | 14.26% | −22.98% | 5/12 | 2/12 |
| S3 mean substitute | 0.8111 | −0.1694 (t −12.21) | 0/12 | 7.83% | −17.54% | — | 0.0% |
| S4 cash at S1's f | 0.9769 | −0.0036 (t −4.03) | 0/12 | 7.41% | −12.73% | 12/12 | 0/12 |
| **S5 IS-argmax substitute (assets CHOSEN)** | **0.7296** | **−0.2509 (t −17.29)** | **0/12** | 7.08% | −17.70% | — | — |

Benchmarks on the same window: **SPY 0.8820 / 15.45% / −33.72%; RULES v1 @10bps u56 0.7471,
broad 0.5763 (mean 0.4695 / 4.64% / −18.98% across both rungs).**

**S5 − S1 = −0.3208 (t −19.09), 0 of 12** — the whole asset-identity question in one number. The
IS rule picks `IEF+LQD+UNG` or `IEF+LQD+SLV` in 12 of 12 cells; UNG is a catastrophe out of
sample. S1's +0.0699 is therefore not a selector beating do-nothing; it is **the answer to "how
much is a free correct answer worth"**, and it is bought with **5.5 pp of CAGR** — which is why
S1 fails 4b's CAGR floor in 11 of 12 cells while S0's failures are the drawdown cap (12 of 12,
with H1 in 6). On the bars that
decide capital nothing here passes: OOS 4b is 0/12, 1/12, 2/12, 0/12 for S0/S1/S2/S4 and **0.0%**
over the substitutes. S2, the clause used as a gate, abstains in 9 of 12 cells — the fourth run
(after ideas 181/186/194) in which the null clause fails as a selection gate.

## (5) Both KEEP paths, all 10,464 rows

| rows | 4a | 4b |
|---|---|---|
| real sleeve (72) | 41/72 | **23/72** |
| R20 controls (12) | 3/12 | 0/12 |
| CASH controls (36) | 19/36 | 8/36 |
| null draws (10,344) | 32.6% | **12.3%** |

The real sleeve reaches 4b **more** often than a substituted one (31.9% vs 12.3%) — the opposite
direction to idea 186's rotation result for the conditional sleeve, and the honest reason is (2),
not skill. Of the 23 full-sample 4b passes, **7 clear the two-sided DIV null on Sharpe and 2 on
drawdown**; 19 of the 23 are u56 and 9 are at 25 bps. Rule 8 says
these are IS artefacts: the same construction passes OOS 4b once in twelve.

## Verdict — KILL

The static sleeve of ideas 101/134 is **not an asset-selection effect that can be traded**. Its
drawdown benefit is 98.4% reproduced by holding cash at the same f; its Sharpe benefit exists only
if the three tickers are handed over for free, and the enumerated population shows an IS chooser
would have taken a different, much worse triple. No book is proposed and no RULES change follows
(rule 6). The transferable products are two proposed PROTOCOL amendments in the memo: **11c**
(publish the SIGNED percentile, and enumerate the null population where it is enumerable) and
**11d** (an instrument whose asset identities were chosen by a human must publish an
IS-chosen-substitute arm, or its separation is undated hindsight).

## Predictions, scored as they fell — 5 of 6 pre-registered, plus 1 post-hoc

P1 HIT ([a]–[e]) · P2 HIT (DIV clear 29.2% < 40%) · P3 HIT (ALL separates better than DIV:
|dSharpe| percentile 0.551 vs 0.337, dMaxDD 0.964 vs 0.725) · P4 HIT (cash captures 98.4% ≥ 50%)
· **P5 MISS** (S1 beats S0 by +0.0699, 12/12 — and (2)/(4) explain why that is not what it looks
like) · P6 HIT (23 4b passes, 7/23 clear) · **P7 HIT, post-hoc and labelled as such** (S5 0.7296 <
S1 1.0504). S5 and the signed-percentile reading were added after the first pass in response to
P5; the docstring says so and the pre-registered six are reported unchanged.

## Caveats carried, not buried

* **Survivorship.** U56 and BROAD136 are current-constituent lists (idea 54). Real and null draws
  inherit it identically so the comparison is unaffected; every level is optimistic.
* The DIV pool is itself a survivor list of instruments that existed and stayed liquid 2008–2026.
  An enumeration is exact **for that pool** and says nothing about assets outside it.
* SMALL439 is out of scope and the reason is stated rather than buried: joining diversifier ETFs
  to the small panel would put them in the composite's ranking pool and change the base book.
  Ideas 136/186 found the small panel contributes 0 of 36 on both KEEP paths.
* 12 rule-8 cells share 2 price panels, so every t-stat above is optimistic; the enumerated
  percentile, not the t-stat, is the inference this run leans on.
* Idea 38 (calendar-day index after 2014-09-17) and idea 126 (t+1 execution only) carry over.
* Idea 144: an overlaid book is the same book with an instrument on it, not a new book.

Script `2026-09-05_is-the-conditional-sleeve-anything-at-all_B.py`; artefacts `.console.txt`,
`.grid.csv`, `.null.csv`, `.clause.csv`, `.walkforward.csv`, `.keep.csv`, `.memo.md`.
**RULES.md, scan.py, bot.py and baseline.py untouched.**
