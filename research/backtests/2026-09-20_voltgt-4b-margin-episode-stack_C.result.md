# Idea 2038 (lane C, 2026-09-20) — does the VOL-TARGET family's 4b MARGIN decompose into a STACK OF DRAWDOWN EPISODES?

**Verdict: ANSWERED — NO, it is not a stack.  It is ONE 23-day episode (2020Q1) at 11-40x
concentration, PARTLY CANCELLED by the other four; the full 5-episode stack owns only 13.8-49.3%
of the OOS Sharpe margin while holding 13.4% of the OOS days (concentration 1.03x-3.69x).
The queue's "three quarters own the whole margin" premise is REFUTED at every (bar x pad x panel
x cell) grid point.  Plus a KILL on reading the excised verdict as a book failure: excision moves
the 4b BAR by more than it moves the book.**

Script `research/backtests/2026-09-20_voltgt-4b-margin-episode-stack_C.py`; gates **11/11**.
Published: `.grid.csv` (1,664 scored rows), `.decomp.csv` (1,536), `.walkforward.csv` (256),
`.episodes.csv`, `.ladder.csv`, `.gates.csv`, `.log.txt`.

## What was run

Four committed vol-target cells, none chosen by this run: **C_KEEP** `t=0.10, T=M, R=M` (the
standing KEEP-4b candidate, memo `2026-09-20_voltgt-t010-RM_KEEP4b_MEMO.md`), **C_MEMO**
`t=0.16, T=W, R=W` (the original panel memo, PARK), **C_GXDD** `t=0.08, T=M, R=M` (idea 1793's
chooser pick) and **C_ORCL** `t=0.12, T=M, R=D` (1793's OOS oracle), on U56 and B136 at 10 bps,
t+1, sigma `(L=20, d=0)`.

**Excision convention** (the record's, idea 1715/912/2022 lineage): an excision deletes the
episode's days from the STATISTIC, not from the tape — every book is traded and charged on the
full price history, then the excised days are dropped from the daily NET return vector for the
book, for SPY and for live RULES v2 alike.  MaxDD is therefore read on a spliced curve and CAGR
on a shortened calendar; both stated, neither hidden.  Every episode is found on OOS SPY, so the
IS half is invariant (**G5 = 0.000e+00 exactly**, both panels).

**Tuned (2, every grid point reported):** DEPTH BAR `b ∈ {0.05, 0.10, 0.15, 0.20}` and PADDING
`p ∈ {0, 5, 10, 20}` trading days each side of the decline.  Canonical `(b=0.10, p=0)`.

**Episodes at b=10%, identical on both panels** (peak → trough, depth, days):
2020-03-23 **−33.72%** (23d) · 2022-10-12 **−24.50%** (195d) · 2018-12-24 **−19.35%** (65d) ·
2025-04-08 **−18.76%** (34d) · 2018-02-08 **−10.10%** (9d).  Total 326d = **13.4%** of the
2,441-day OOS tape.

## Reproduction (gates)

| gate | value | target |
|---|---|---|
| G4 two-schedule diagonal == `engine.backtest` | 1.39e-17 / 2.78e-17 | < 1e-12 |
| G5 IS half invariant to every excision | **0.000e+00** | == 0 |
| G_PUB U56 `C_KEEP` (memo §2/§3: 13.31% / 1.2437 / −19.39%, OOS 13.81% / 1.2822) | 4.54e-05 | < 6e-4 |
| G_PUB U56 `C_MEMO` (15.61% / 1.2027 / −19.86%, OOS 15.94% / 1.2193) | 2.95e-05 | < 6e-4 |
| G_PUB B136 `C_MEMO` (15.94% / 1.2049 / −18.76%, OOS 15.36% / 1.1837) | 4.61e-05 | < 6e-4 |
| G_PUB U56 `C_GXDD` (1793: OOS 11.87% / 1.2780 / −16.13%) | 1.85e-05 | < 6e-4 |
| G8 SPY OOS (15.26% / 0.8737 / −33.72%) | exact | < 6e-4 |
| G6 NONE control excises 0 days; G7 stack exhausts the episode list | 0 / 0 | == 0 |

## The answer

**H_STACK — FALSIFIED on the aggregate, CONFIRMED for one window.**  No single episode owns
≥ 0.50 of any cell's OOS Sharpe margin: the maximum over all 8 (panel × cell) pairs is **+38.0%**
(B136 `C_ORCL`, 2020Q1) and the standing candidate reads **+10.8%** on U56 / **+13.3%** on B136.
But 2020Q1 is 23 days = **0.94%** of the OOS tape, so its **concentration ratio** (margin share ÷
day share) is **11.5x–40.3x**.  Every other episode reads NEGATIVE concentration on `C_KEEP` and
`C_MEMO` — excising 2018Q4, 2025Q1 or 2018-02 **raises** the margin, i.e. the book loses ground to
SPY through those declines.

| panel / cell | 2020Q1 alone (0.94% of days) | all 5 episodes (13.4%) | others, net | conc. (all) |
|---|---|---|---|---|
| U56 `C_KEEP` | +10.8% (11.5x) | **+19.1%** | +8.3% | **1.43x** |
| U56 `C_MEMO` | +35.6% (37.8x) | +15.6% | −20.0% | 1.17x |
| U56 `C_GXDD` | +16.4% (17.5x) | +28.5% | +12.0% | 2.13x |
| U56 `C_ORCL` | +33.7% (35.8x) | +44.5% | +10.7% | 3.33x |
| B136 `C_KEEP` | +13.3% (14.1x) | **+24.0%** | +10.7% | **1.80x** |
| B136 `C_MEMO` | +35.9% (38.1x) | +13.8% | −22.0% | 1.03x |
| B136 `C_GXDD` | +24.7% (26.2x) | +49.3% | +24.6% | 3.69x |
| B136 `C_ORCL` | +38.0% (40.3x) | +48.0% | +10.1% | 3.60x |

Against idea 2022's yardstick — **89% of the drift-vs-calendar edge in one 24-day window** — the
4b margin against SPY is a different object: at most half of it lives in 13.4% of the tape, and
for the standing candidate a fifth to a quarter does.  **The standing KEEP-4b candidate is the
LEAST episode-concentrated of the four cells on both panels.**

**H_CRASH — the verdict flips, but NOT for the reason the hypothesis states.**  With every
b=10% episode excised, 4b OOS goes PASS → FAIL in **127 of 128** (panel × cell × bar × pad) cells.
This is mostly a **BAR SHIFT**, the axis idea 2034 was filed to isolate, and it must not be read
as a book failure.  The excision moves the BOOK's OOS Sharpe **+1.196** (U56 `C_KEEP`, 1.2822 →
2.4778) and SPY's **+1.274** (0.8737 → 2.1472): both legs rise together and the margin loses only
0.078 of 0.408.  On the two non-Sharpe legs the bar moves violently — the 4b DD cap
`0.60 × SPY` tightens **−20.23% → −5.98%** and the CAGR floor `0.70 × SPY` rises
**10.68% → 25.38%**, both by ~14 pp — so a book that keeps a −8% drawdown and a 33% CAGR still
fails.  **KILL the reading that "excise the crashes and the book dies".**

**H_CAGR — CONFIRMED in 6 of 8 pairs.**  The CAGR floor, the record's largest binding leg, is the
leg that dies first: on U56 `C_KEEP` the stack owns **+80.9%** of the OOS CAGR margin against
**+19.1%** of the Sharpe margin; on B136 `C_KEEP` **+110.0%** (it crosses zero).  The two
exceptions are `C_MEMO` on both panels, where the Sharpe leg loses more.  One resolution caveat
stated: B136 `C_GXDD` carries a base OOS CAGR margin of **+0.47 pp**, so its 4-digit CAGR shares
(up to +1024%) are a thin denominator, not a measurement.  Sharpe-leg denominators run
0.3080–0.4748 and carry no such degeneracy.

**H_DIAL — FALSIFIED.**  The family's ordering on OOS Sharpe margin is **not** episode-invariant:
11 distinct orderings over 208 (bar × pad × mode) cells on U56 (modal
`C_ORCL > C_KEEP > C_GXDD > C_MEMO` at 24.0%) and 10 on B136 (modal the same at 30.3%).  Which
vol-target cell looks best depends on which quarter you delete.

**Both dials are live, and the depth bar inverts.**  At `b=5%` (13 episodes, 476d) the
all-excision Sharpe share for `C_KEEP` is **NEGATIVE** (−35.9% U56, −43.1% B136): adding the
shallow declines makes the book look *better*, because it gives ground to SPY in them.  Padding
monotonically raises the share at `b ≥ 10%` (U56 `C_KEEP` +19.1% → +35.8% from p=0 to p=20;
B136 +24.0% → +61.8%), i.e. the book's edge sits in the *recovery leg* as much as in the decline.
The full 4 × 4 ladder is in `.ladder.csv` and the log.

## Rule 8 (parameters chosen on 2009–2016 only, 2017–2026 read once)

Two legal IS-only choosers over the family's own 5 × 4 `(t, R)` grid, at both trade cadences:

| panel | T | chooser | pick | OOS CAGR / Sharpe / MaxDD | vs SPY | vs live v2 | 4b OOS | 4a OOS |
|---|---|---|---|---|---|---|---|---|
| U56 | M | `C_ISSHARPE` | t=0.16, R=M | 16.46% / 1.2018 / −24.24% | 15.26% / 0.8737 / −33.72% | 9.46% / 1.2766 / −12.05% | **FAIL** (DD) | FAIL |
| U56 | M | `C_ISLEGS` | t=0.12, R=M | 15.37% / 1.2865 / −21.01% | " | " | **FAIL** (DD) | FAIL |
| U56 | W | `C_ISSHARPE` | t=0.16, R=M | 16.30% / 1.1815 / −24.52% | " | " | FAIL | FAIL |
| U56 | W | `C_ISLEGS` | t=0.12, R=M | 15.22% / 1.2650 / −21.27% | " | " | FAIL | FAIL |
| B136 | M | `C_ISSHARPE` | t=0.20, R=M | 16.27% / 1.0824 / −29.67% | " | 7.85% / 1.1017 / −12.24% | FAIL | FAIL |
| B136 | M | `C_ISLEGS` | t=0.10, R=M | 13.05% / 1.2000 / −19.87% | " | " | **PASS** | FAIL |
| B136 | W | `C_ISSHARPE` | t=0.20, R=M | 16.29% / 1.0744 / −30.02% | " | " | FAIL | FAIL |
| B136 | W | `C_ISLEGS` | t=0.10, R=M | 13.05% / 1.1884 / −20.27% | " | " | FAIL | FAIL |

**16 of 128 rule-8 picks clear 4b OOS un-excised, 0 of 128 with every episode excised; 4a OOS
0 of 128 either way.**  Only `C_ISLEGS` on B136 T=M reaches the standing candidate's own cell.
This independently reconfirms ideas 1771 / 1803: the CELL clears, the CHOOSER does not.

## What this does and does not change

* It does **not** move the standing KEEP-4b candidate's status.  Its FULL and OOS numbers are
  reproduced here to 4.54e-05 and it remains the least episode-concentrated cell of the four.
* It **does** add a required companion statistic to every future episode-excision claim: publish
  the **CONCENTRATION RATIO** (margin share ÷ day share) and the **BOOK / BENCHMARK split** of the
  move, because the raw "share of the margin" is a small difference of two large co-moving legs,
  and because the 4b bar itself moves ~14 pp on both non-Sharpe legs under excision.
* Survivorship: U56 and B136 are CURRENT constituents, so every LEVEL above is optimistic.
  SMALL665 is not run here — the family clears 4b 0 of N there, confirmed four times
  (addendum A2 and ideas 1763 / 1793 / 1803).
* `RULES.md`, `PROTOCOL.md`, `scan.py`, `bot.py` and `baseline.py` are untouched by this run.
