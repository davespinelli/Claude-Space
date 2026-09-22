# Idea 907 — bound RAND's 4b PASS RATE with a REAL DRAW BUDGET, not one seed (lane B, 2026-09-22)

**VERDICT: ANSWERED. The base rate exists and it is `0.0360 +/- 0.0022` (12.30 of 342) at 10 bps.
887's single draw was TYPICAL, not a lucky tail — but the number it published is unusable as a
rate, and the same construction now reads 11 rather than 12 on four extra days of tape. Plus a
KILL, out of sample: an IS-only chooser handed nothing but noise clears 4b `0 of 120` times.**
No KEEP candidate. RAND is a control; nothing here is proposed for capital.

## What was run
Idea 887's 342-cell zero-signal grid, re-drawn on **S = 20 seeds** (param 1) at **cost rungs
{0, 10, 25} bps** (param 2, headline 10). 342 cells = 3 panels {U56 56 names, B136 136, SMALL 666}
x q {0.05 ... 1.00, 10 rungs} x construction {RESPREAD, DEGROSS} x gross {0.75, 0.95, 1.00}
x cadence {W, M}, less the 18 q=1.00 DEGROSS duplicates. **20,520 book-rows, all committed**
(`.books.csv`). Book construction, eligibility, leg definitions and cost/fill semantics are
copied verbatim from 887's script; `research/baseline.py`, `scan.py`, `bot.py` and `RULES.md`
are untouched.

## Gates (7 of 7 PASS, printed before any hypothesis was read)
G0/G1 `fast_run` == `engine.backtest` on a RAND book, returns 4.0e-16 and turnover 6.7e-16.
G2 q=1.00 RESPREAD == DEGROSS exactly (0.0). G3 cell count == 342. G4 RESPREAD gross exact 8.9e-16.
G5 cost rungs derivable from the 0 bps path (0.0).
**G7 REPRODUCTION: seed 887 at 10 bps on 887's OWN tape end (2026-09-14) = 12 of 342, == 887's
published 12.** On the current cache (2026-09-18) the same seed reads **11**. The construction
therefore reproduces 887 exactly; the one-cell gap is four extra trading sessions.

## 1. The base rate, every rung (out of 342, over 20 seeds)
| rung | mean | rate | SD | min | max | median | SE(rate) | seed 887 |
|---|---|---|---|---|---|---|---|---|
| 0 bps | 25.40 | 0.0743 | 4.42 | 15 | 35 | 25.0 | 0.0029 | 28 |
| **10 bps** | **12.30** | **0.0360** | **3.31** | **7** | **20** | **12.0** | **0.0022** | **11** |
| 25 bps | 3.50 | 0.0102 | 1.88 | 2 | 9 | 3.0 | 0.0012 | 4 |

887's published 12 sits at the **42.1st percentile** (z = −0.11) of the other 19 draws; its count
on today's tape (11) at the 31.6th (z = −0.40). **The single draw was not misleading in level.**
What it could not say is the spread: across seeds the count runs **7 to 20** — a 2.9x range — so
any claim of the form "RAND cleared 4b N times" is quoted to a precision the draw does not carry.
4a is rarer still: **0.30 of 342 on average at 10 bps (0.0009), and 0 of 342 at every seed at 25 bps.**

## 2. Which leg binds a coin flip (share of 6,840 draws each leg passes)
| rung | leg_DD | leg_CAGR | leg_SHARPE | all three |
|---|---|---|---|---|
| 0 bps | 0.4370 | 0.4860 | 0.4887 | 0.0743 |
| 10 bps | 0.4197 | 0.2788 | 0.2466 | 0.0360 |
| 25 bps | 0.3379 | 0.1468 | 0.1152 | 0.0102 |
Each leg alone is near a coin flip at 0 bps. **Cost is what makes 4b a bar**: from 0 to 25 bps the
CAGR leg falls 0.486 -> 0.147 and the Sharpe leg 0.489 -> 0.115, while the DD cap barely moves
(0.437 -> 0.338) — a de-grossed noise book keeps its shallow drawdown and loses its return.

## 3. Where a coin flip passes (all 31 cells with rate > 0 are in `.cells.csv`)
**5 cells pass on 20 of 20 seeds** — U56 q=1.00/RESPREAD/g0.75 (W and M), U56 q=0.90/RESPREAD/g0.75 M,
U56 q=0.90/DEGROSS/g0.75 M, B136 q=1.00/RESPREAD/g0.75 W. These are not "random books that got
lucky": at q >= 0.90 the RAND rank picks nearly the whole eligible set, so the book degenerates to
**equal-weight-everything-above-its-200d-MA at 75% gross** and the draw stops mattering. That is a
real (and already-known) exposure effect, not signal. Pass rate by axis at 10 bps:
`gross 0.75 0.0842 / 0.95 0.0110 / 1.00 0.0127`; `cadence M 0.0550 / W 0.0170`;
`constr RESPREAD 0.0447 / DEGROSS 0.0262`; `q 0.05 0.0014 -> 0.90 0.1069 -> 1.00 0.1667`.
By panel: **U56 0.0732, B136 0.0346, SMALL 0.0000** (0 of 2,280 — the small panel's own SPY-relative
bars are unreachable by noise at any width). Per-cell SE at n=20 is at most 0.1118, and the
rule-of-three bound on a 0-of-20 cell is 0.1500, so 20 seeds resolve *which* cells pass but not a
cell's rate to better than ~+/-0.11.

## 4. PROTOCOL rule 8 — params on 2009-2016 only, 2017-2026 read ONCE (60 picks per chooser)
Two pre-declared IS-only choosers pick one cell per (panel, seed) from IS Sharpe / IS Calmar alone.
| chooser | panel | OOS CAGR | OOS Sharpe | OOS MaxDD | OOS 4b |
|---|---|---|---|---|---|
| IS_SHARPE | U56 | 14.81% [1.46..18.67] | 1.011 [0.406..1.231] | −26.35% [−53.87..−5.17] | **0/20** |
| IS_SHARPE | B136 | 14.76% [1.18..20.91] | 0.993 [0.597..1.092] | −26.49% [−35.94..−3.51] | **0/20** |
| IS_SHARPE | SMALL | 9.25% [0.60..12.08] | 0.554 [0.208..0.664] | −47.23% [−52.91..−3.71] | **0/20** |
| IS_CALMAR | U56 | 17.19% [6.32..21.28] | 1.092 [0.406..1.238] | −26.68% [−53.87..−21.28] | **0/20** |
| IS_CALMAR | B136 | 15.52% [9.07..17.01] | 0.986 [0.597..1.095] | −29.59% [−43.60..−24.74] | **0/20** |
| IS_CALMAR | SMALL | 8.87% [2.00..10.67] | 0.521 [0.207..0.611] | −50.18% [−64.96..−42.74] | **0/20** |
Comparands, same tape: **SPY OOS 15.26% / 0.874 / −33.72%**; **RULES v2 OOS** 9.46% / 1.277 / −12.05%
(U56), 7.85% / 1.102 / −12.24% (B136), 3.64% / 0.546 / −14.16% (SMALL). OOS bars: CAGR floor 10.68%,
DD cap −20.23%, Sharpe > 0.874.
**POOLED OOS 4b pass rate 0.0000 (0 of 120) under both choosers, and full-sample 4b 0 of 120, 4a 0 of 120.**
The binding leg is always the **DD cap**: across the 120 picks it holds 5 times, while the CAGR leg
holds 72 and the Sharpe leg 63. An IS-only chooser fed pure noise reliably finds a book that beats
SPY's OOS *return* and roughly matches its OOS Sharpe — and then takes −26% to −50% to get it.

## 5. Both KEEP paths
- **4a (beat the live book):** 6 of 6,840 draws at 10 bps = **0.0009**; 0 of 6,840 at 25 bps. **No pass.**
- **4b (capital-worthy):** 246 of 6,840 = **0.0360**; under rule 8, **0.0000**. **No pass.**
- **VERDICT: neither. This is a CONTROL, not a candidate. Nothing here goes near capital.**

## What this means for the record
1. **`0.0360 +/- 0.0022` at 10 bps is the number a committed 4b pass must beat**, not 12/342 and
   not zero. A grid of 342 cells should expect ~12 noise passes before any signal is involved.
2. **Quote the rung.** The base rate moves 0.0743 / 0.0360 / 0.0102 across 0 / 10 / 25 bps — a 7.3x
   swing. A 4b count quoted without its cost rung is uninterpretable.
3. **A full-sample 4b pass is cheap; an IS-chosen OOS 4b pass is not.** 0 of 120 is the useful
   half of this result: rule 8 is doing real work, and the 4b DD cap is the leg doing it.
4. **Committed pass counts are tape-sensitive**: 8.3% of 887's count (1 of 12) moved on four
   trading days. Any census that differences two committed counts is differencing this noise too.

## Caveats
Survivorship: `universe.json` / `universe_broad.json` are CURRENT constituents and `prices_small.csv`
is a current screen, so every CAGR level is optimistic and both 4b bars are easier than on a
point-in-time panel; the base rate is therefore an *upper* bound on how often noise would clear a
point-in-time 4b. 20 seeds resolve the pooled rate to +/-0.0022 but a single cell only to +/-0.11.
2020 and 2022 are the only stress episodes in the window.
