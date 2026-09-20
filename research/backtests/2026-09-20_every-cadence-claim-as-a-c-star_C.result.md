# Idea 1613 (lane C, 2026-09-20) — is EVERY committed CADENCE claim a c* claim quoted at ONE rung?

**ANSWERED, BOTH WAYS — and the split is the finding. YES for the ORDERING (88.4% of the
record's cadence claims are quoted at a single rung, and 23.9% of re-priced cadence verdicts
flip sign inside 5–50 bps); NO for the KEEP VERDICT (0 of 24 books have a rung-conditional 4b).
KILL for a rules change; the flip risk is fully predictable from the margin already published.**

Script: `2026-09-20_every-cadence-claim-as-a-c-star_C.py` · 77 s · **19 of 19 gates pass** ·
outputs `.census.csv` (86) `.grid.csv` (120) `.cstar.csv` (180) `.verdict_interval.csv` (24)
`.walkforward.csv` (72) `.gates.csv` `.log.txt`.

## 1. The census (Q1)

Mechanical extraction over `research/LEADERBOARD.md` + `research/CHANGELOG.md` under a rule fixed
before the run (≥2 distinct cadence tokens + a comparative token; STRICT additionally requires an
explicit ordered pair such as `W→M`). Every extracted sentence is published.

| denominator | n | POINT_IMPLICIT | POINT_EXPLICIT | INTERVAL | CSTAR | **one rung** | spans 5–50 |
|---|---|---|---|---|---|---|---|
| BROAD  | 86 | 52 | 24 | 8 | 2 | **76 (88.4%)** | 1 (1.2%) |
| STRICT | 30 | 17 |  8 | 5 | 0 | **25 (83.3%)** | 1 (3.3%) |

Source split: LEADERBOARD 76, CHANGELOG 10. NOISE IS STATED, NOT HIDDEN: the BROAD rule cannot
tell a rebalance cadence from rule 9's weekly cache refresh, which is why the STRICT denominator
is carried alongside and the full CSV is committed for re-classification.

## 2. The re-pricing (Q2) — 180 pairwise verdicts, the whole cost axis exact

`r(c) = r_gross − turnover·c/1e4` reproduces a fresh engine run at **0.000e+00** at 10, 25 and
50 bps (G1/G2), and the closed-form `Sharpe(c)` matches the direct reduction at 6.7e-16 (G11), so
every c* below is arithmetic on one tape, not a re-search.

* **43 of 180 (23.9%) cadence verdicts flip sign inside 5–50 bps.** 47 of 180 cross somewhere in
  0–50; **0 of 180 cross more than once** — the verdict is MONOTONE in cost, so a c* is a complete
  description of it. Median c* among the in-band crossers **27.5 bps** (IQR 17.3–33.7).
* By frame: **LIVE 34.4%** (31/90) vs **INC 13.3%** (12/90). By window: FULL 27.8%, H1 16.7%,
  H2 27.8%, IS 19.4%, **OOS 27.8%**. By pair: DvM 33.3%, DvQ / WvM 30.0%, DvW / WvQ 23.3%,
  **MvQ 3.3%** — the two slow cadences are the one pair a point quote is safe for.
* **G9:** the solver re-derives idea 1586's committed headline (U56 / INC / FULL, W vs Q)
  at **c\* = 12.42 bps** against the committed 12.4.

**The flip is predictable from the margin the record already publishes.** Readings with
`|ΔSharpe@10| < 0.05` flip **50.7%** of the time (n=69); readings at `≥ 0.05` flip **7.2%**
(n=111). Median |Δ@10| is 0.0221 among flippers and 0.0843 among non-flippers.

## 3. The verdict as an interval (Q3) — and this is where the alarm stops

Scanning c ∈ [0, 50] at 0.25 bps for all 24 books, with the live RULES v2 comparator itself
re-priced at the same rung:

* 4b (FULL **and** OOS) is **empty over the whole band for 22 of 24** books and **holds over the
  entire band for 2**. **0 of 24 are rung-conditional.**
* Both passers are on U56 / INC: the frozen anchor **W** (15.80% / 1.1537 / −19.13% full;
  17.32% / 1.1857 OOS; 2.87 turns/yr) and its quarterly twin **Q** (15.49% / 1.1515 / −19.89%;
  17.43% / 1.1885 OOS; **1.64 turns/yr**), each passing on `[0,50]`.
* 4a: 2 of 24 books clear it at any rung. SPY U56: 15.12% / 0.8844 / −33.72% (H1 0.9573,
  H2 0.8251); live RULES v2 @10 bps: 8.62% / 1.2011 / −12.05% (H1 1.2279, H2 1.1808).

So the rung moves the *ordering* of cadences often, and the *KEEP decision* never — because the
4b legs are dominated by the DD cap and the CAGR floor, which a 40 bps cost swing moves far less
than the Sharpe ranking of two adjacent cadences.

## 4. Rule 8 (2017–2026 read ONCE), with the rung itself as dial 2

Choosing a cadence is negative-value at every rung a chooser is allowed to quote:

| chooser | mean OOS Sharpe | mean ΔS vs anchor | beats live v2 | beats SPY | 4b OOS | 4a OOS |
|---|---|---|---|---|---|---|
| C_SHARPE | 0.8815 | **−0.0464** | 0 / 24 | 16 / 24 | 4 | 0 |
| C_MEMO   | 0.9198 | −0.0080 | 0 / 24 | 16 / 24 | 2 | 0 |
| C_ANCHOR (choose nothing, stay weekly) | **0.9278** | +0.0000 | 0 / 24 | 16 / 24 | 4 | 0 |

**4 of 12 (panel × frame × chooser) groups change their IS pick with the rung they quote** — e.g.
U56/INC/C_SHARPE picks W at 5 and 10 bps and Q at 25 and 50, which is the c* = 12.42 bps crossing
showing up as a tuning artefact. The rung is therefore a real free parameter of a cadence search,
and at the protocol's binding 10 bps the incumbent's weekly cadence stands.

## 5. The constructive half — should PROTOCOL rule 2 quote a cadence verdict as an interval?

**No, not in general — and yes for one narrow, mechanically testable class.** A blanket interval
requirement buys nothing: the KEEP verdicts this protocol actually commits to are rung-invariant
(0 of 24). What is not rung-invariant is the *comparative* sentence — "weekly beats monthly" —
and the record is 88.4% made of those, quoted at one rung. The cheap fix is a margin trigger,
since c* is free once a book is run:

> **Proposed PROTOCOL rule 2 addendum (for Sunday review; not adopted by this run).** A claim that
> one rebalance cadence beats another must publish the cost `c*` at which the comparison reverses
> whenever the quoted Sharpe margin at 10 bps is under **0.05**; above that margin the point quote
> stands. `c*` costs no extra backtest: `r(c) = r_gross − turnover·c/1e4` is exact, and the
> comparison is monotone in cost (0 of 180 readings crossed twice).

That trigger fires on 38.3% of readings and catches the half that actually flips.

## Survivorship (rule 9)

U56 / B136 are CURRENT-constituent lists and SMALL a CURRENT sub-$2B screen carried back to 2010,
so every CAGR and drawdown LEVEL is an upper bound. What survives the bias is the CONTRAST between
cadences on the same names and the same days — and above all the SHAPE of that contrast in cost,
which is arithmetic on one tape.
