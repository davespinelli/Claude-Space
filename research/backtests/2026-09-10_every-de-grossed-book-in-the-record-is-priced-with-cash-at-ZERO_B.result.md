# Idea 406 — every de-grossed book in the record is priced with cash at ZERO (lane B, 2026-09-10)

**Verdict: ANSWERED / no KEEP.** The convention is real, it is material, and it taxes exactly the
books the queue said it taxes — but the queue's literal fix (credit cash, leave `rf = 0`) is
internally inconsistent, and the consistent version moves the Sharpe legs the *other* way. No book
KEEPs on either path under any credit rung, and RULES v2 still fails 4b at 300 bps.

Script `research/backtests/2026-09-10_every-de-grossed-book-in-the-record-is-priced-with-cash-at-ZERO_B.py`.
Outputs `.console.txt`, `.grid.csv` (2,880 arm-rows), `.flips.csv`, `.census.csv`,
`.walkforward.csv`, `.livebook.csv`. Nothing in RULES.md / PROTOCOL.md / scan.py / bot.py /
baseline.py touched.

## Design

Two tuned parameters, exactly as the queue specified, every point reported:

* **credit** c ∈ {0, 150, 300} bps/yr, flat, paid daily on **positive cash only**, *inside* the
  drift renormalisation (not bolted on afterwards). Negative cash (g > 1) keeps idea 402's
  financing convention at fin = 0 and is carried as a **control**, never as a candidate.
* **book** = idea 402's committed family, f ∈ {0.00, 0.25, 0.60} × g ∈ {0.40 … 2.00} (12 points),
  plus RULES v2 and RULES v1 priced at the same rungs.

Reported axes, never selected on: panel {u56, broad} × base book {EWall, TOP20} × sleeve
{S3, S4} × cost rung {10, 25} bps = **16 cells**. 576 books × 3 credit rungs, weekly, t+1.

Three **treatments**, because "credit the cash" is not one question but two:

| | cash earns | Sharpe rf | what it is |
|---|---|---|---|
| **C0** | 0 | 0 | the record's standing convention (idea 402's) |
| **C1** | c | 0 | the queue's literal ask |
| **C2** | c | c | internally consistent — excess-return Sharpe for the arm **and** SPY |

The CAGR floor and the DD cap are total-return bars and are **identical under C1 and C2**; the
three Sharpe legs (H1, H2, OOS) are where C1 and C2 part company.

### Gates

* **(a)** At c = 0 the simulator reproduces idea 402's committed `.grid.csv`: **broad 4.2e-14 on
  288/288 shared rows** (its cache is written weekly and has not moved). **u56 is 4.16e-3
  untruncated and 4.8e-6 when truncated to idea 402's last bar, 2026-09-04 — not zero.**
  `data/prices.csv` is re-downloaded daily with auto-adjusted closes, so its history is restated
  between runs: **u56 rows in this record are reproducible to ~1e-5, not bit-exact.** Reported,
  not corrected.
* **(a′)** `run_cash(c = 0)` vs `engine.backtest` on today's u56: **2.97e-16**.
* **(b)** The exact CAGR gain vs the first-order form `(1 − gross)·c`: mean +27.2 bps actual vs
  +25.0 predicted at c = 150 (error ≤ **7.9 bps**), +54.5 vs +50.0 at c = 300 (error ≤ 16.4 bps).
  Compounding makes the credit worth slightly *more* than the linear form. The record-wide census
  below inherits exactly this error, in the conservative direction.

## Q1/Q2 — how many 4b margins change sign (exact, 576 books × 16 cells)

| credit | treat | H1 | H2 | OOS | DD | CAGR | **4b verdict** | 4a verdict (v2) |
|---|---|---|---|---|---|---|---|---|
| 150 | C1 | 0 / 0 | **8** / 0 | **12** / 0 | 0 / 0 | **12** / 0 | **10 / 0** (69 → 79) | 15 / 4 (45 → 56) |
| 150 | C2 | 0 / **9** | 0 / **8** | 2 / **9** | 0 / 0 | **12** / 0 | **10 / 1** (69 → 78) | 0 / **22** (45 → 23) |
| 300 | C1 | 0 / 0 | **15** / 0 | **20** / 0 | 1 / 0 | **26** / 0 | **23 / 0** (69 → 92) | 22 / 8 (45 → 59) |
| 300 | C2 | 0 / **31** | 3 / **9** | **13** / **9** | 1 / 0 | **26** / 0 | **23 / 2** (69 → 90) | 0 / **27** (45 → 18) |

(cells are `fail→pass / pass→fail`, out of 576.)

Three facts, all pre-registered and all confirmed:

1. **The tax is exactly where the queue said it is.** Split by gross regime, the 4b verdict flips
   are **10/10 (150 bps) and 23/23 (300 bps) in the de-grossed arms (g < 1, mean cash 0.333)** and
   **0 in the levered arms (g ≥ 1, cash 0.000)**. Mean Δm_min: **+0.0070 / +0.0125** de-grossed vs
   **+0.0000** levered.
2. **The DD cap barely moves** (P2 held): mean Δm_DD **+0.0002 / +0.0004**, max +0.0015, one flip
   in 576 at 300 bps. Cash only cushions a drawdown by the credit accrued during it.
3. **C2 reverses the Sharpe legs** (P3 held, predicted ≈ −0.042 at 150 bps, measured mean
   **−0.0235 / −0.0208 / −0.0207** on H1/H2/OOS and **−0.0469 / −0.0415 / −0.0414** at 300 bps).
   A low-vol de-grossed book earns more of its `rf = 0` Sharpe from the risk-free leg than SPY
   does; taking that leg out costs it more than it costs SPY. **31 of 576 H1 margins go from pass
   to fail at 300 bps.**

The 4a path is the sharpest reversal: **C1 helps it (45 → 56 → 59) and C2 destroys it
(45 → 23 → 18)**, because RULES v2 holds **46.8% cash** — more than every arm that passes 4a
(they sit at g 0.40–0.85) — and 4a is decided by ḡ/σ, not by cash alone.

**The convention does not change the ranking.** Under C0, C1 and C2, at both credit rungs, the
best (f, g) is the same standing incumbent **(f = 0.25, g = 0.75), passing 4b in 14 of 16 cells**,
and it is the **only** pair ≥ 14/16 in all five treatments. **No pair passes 4b in all 16 cells
under any treatment.**

## Q3 — record-wide census (26,207 committed rows, 18 files)

Every committed `.csv` in `research/backtests` that publishes the full 4b margin vector *and* a
realised `gross` column, re-read under the first-order credit (`ΔCAGR = (1−gross)·c`,
`ΔSharpe = (1−gross)·c/Vol`), m_DD left unmoved (Q1 shows its true shift is ≤ 15 bp of margin).
Mean cash across the corpus **0.266**.

| credit | CAGR-floor margins flipping fail→pass | 4b verdicts flipping fail→pass |
|---|---|---|
| 150 bps | 857 / 26,207 = **3.27%** | 742 / 26,207 = **2.83%** |
| 300 bps | 1,769 / 26,207 = **6.75%** | 1,322 / 26,207 = **5.04%** |

pass→fail is 0 by construction: C1 margins are weakly increasing. The census is therefore
**C1-only and an UPPER bound** — it prices the generous horn. Concentration matters: the flips are
not spread evenly. `2026-09-10_does-any-published-COLUMN-prescription-survive-its-own-L2-ladder_C`
goes 147 → 307 → 433 passes of 2,592 (6.2% → 11.9% → 16.7%), and
`2026-09-10_why-do-4b-windows-have-width-0-on-four-of-six-dials_B` 299 → 377 → 445 of 2,156,
while `2026-09-10_is-the-BAND-the-only-clean-adopted-constant_cloud` flips **0 of 312** and both
committed `keeppaths.csv` files flip **0** — the rows the record actually *published as passes*
are not near the bar, only the failures are.

## Q4 — rule 8 (choose (f, g) on 2009–2016 by IS 4b min-margin, read 2017–2026 once)

De-grossed arms only (g < 1), 16 cells, one pick per cell per treatment.

| treat | pick unchanged | OOS CAGR | OOS Sharpe | OOS MaxDD | vs RULES v2 OOS | vs SPY OOS | OOS bars all clear |
|---|---|---|---|---|---|---|---|
| C0 @ 0 | — | 13.45% | 1.108 | −20.40% | 8.57% / 1.178 / −12.17% (**−0.070**) | 15.38% / 0.879 / −33.72% (14/16) | 8/16 |
| C1 @ 150 | 13/16 | 13.53% | 1.129 | −20.09% | 9.34% / 1.276 / −12.13% (**−0.147**) | (14/16) | 10/16 |
| C1 @ 300 | 12/16 | 13.76% | 1.152 | −20.00% | 10.11% / 1.373 / −12.09% (**−0.222**) | (14/16) | 11/16 |
| C2 @ 150 | 14/16 | 13.56% | 1.002 | −20.17% | 9.34% / 1.067 / −12.13% (**−0.065**) | 0.796 (14/16) | 10/16 |
| C2 @ 300 | 14/16 | 13.83% | 0.896 | −20.15% | 10.11% / 0.956 / −12.09% (**−0.060**) | 0.714 (14/16) | 10/16 |

P4 held: the pick is unchanged in 12–14 of 16 cells and where it moves it moves to **lower** g.
The decisive column is the fifth: **crediting cash makes the rule-8 pick worse against the live
book out-of-sample, not better** (−0.070 → −0.147 → −0.222 under C1), because RULES v2 holds
46.8% cash and collects more of the credit than any candidate does. Every pick still beats SPY on
OOS Sharpe in 14/16 cells and loses to RULES v2 in all five treatments.

## Q5/Q6 — KEEP paths, and the book that actually holds the cash

| treatment | 4a (v2) | 4a (v1) | 4b | (f,g) passing 4b in all 16 cells |
|---|---|---|---|---|
| C0 @ 0 | 45/576 | 242/576 | 69/576 | **0/18** |
| C1 @ 150 | 56/576 | 235/576 | 79/576 | **0/18** |
| C2 @ 150 | 23/576 | 235/576 | 78/576 | **0/18** |
| C1 @ 300 | 59/576 | 228/576 | 92/576 | **0/18** |
| C2 @ 300 | 18/576 | 228/576 | 90/576 | **0/18** |

**No KEEP on either path, at any credit rung, under either treatment.**

The single most capital-relevant row is RULES v2 itself. It holds **46.8% cash on average** — far
more than the 25% the queue assumed — and its binding 4b bar is the CAGR floor in **every one of
the 20 (panel × cost × credit × treatment) rows**:

| c (bps) | RULES v2 CAGR (u56) | 4b CAGR floor | m_CAGR | Sharpe C1 | Sharpe C2 | 4b |
|---|---|---|---|---|---|---|
| 0 | 8.63% | 10.61% | **−198 bps** | 1.202 | — | fail |
| 150 | 9.40% | 10.61% | **−121 bps** | 1.301 | 1.090 | fail |
| 300 | 10.16% | 10.61% | **−44 bps** | 1.400 | 0.977 | fail |

Crediting cash at 300 bps closes **78% of the live book's 4b CAGR-floor deficit and still leaves
it 44 bps short**, on both panels and both cost rungs. That is the honest size of the convention:
large enough to be worth fixing, not large enough to promote anything.

## What this says about the record

The queue's premise is **confirmed**: the convention is a one-sided tax on de-grossed books, worth
+27 bps of CAGR at 150 bps and +54 at 300 on a book at gross 0.75, zero on a levered book, and it
moves **2.8–5.0% of the record's 26,207 committed 4b verdicts** from fail to pass.

The queue's **proposed fix is not safe to apply as stated.** Crediting cash while leaving Sharpe
at `rf = 0` pays the book a risk-free return and then counts it as alpha; do it consistently and
the three Sharpe legs move down instead of up (9–31 pass→fail per leg) and the 4a path loses half
its passes. P5 held: the convention is a real tax on the CAGR floor **and** a real subsidy on the
Sharpe legs, and the two do not cancel. A PROTOCOL change here would have to pick a rate, credit
it, **and** set `rf` to the same rate in `engine.metrics` — a three-line change that re-prices
every Sharpe in the record, not a one-line generosity.

## Caveats carried, not buried

* **A flat credit over 2009–2026 is wrong in both directions.** T-bills paid ~10 bps in 2009–2015
  and ~500 in 2023–2026; 150/300 brackets the realised average, not the path. No rate series is
  cached and the sandbox has no network. This is the single largest caveat and it is why the run
  produces an ANSWER and not a PROTOCOL amendment.
* The census (Q3) is first-order and C1-only; its Sharpe leg uses full-sample `Vol` as a proxy for
  per-half vol, which the record does not publish. Upper bound, by construction.
* `data/prices.csv` is restated daily by auto-adjustment — u56 rows in this record reproduce to
  ~1e-5, not bit-exact (gate a).
* Survivorship (idea 54): both panels are current constituents.
* MaxDD is one number off one path (idea 321) and the 4b DD cap turns on exactly it.
* Idea 126: t+1 only. Idea 38: calendar-day index on both panels.
