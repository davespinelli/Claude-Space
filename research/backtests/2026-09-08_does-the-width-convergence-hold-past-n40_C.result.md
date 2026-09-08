# Idea 461 — does-the-width-convergence-hold-past-n=40? (lane C, 2026-09-08)

**VERDICT: KILL of the premise. The convergence does NOT hold past n=40 — it stops at
n≈20–40 and REVERSES, and on the two panels QUEUE 461 named (B136, SMALL439) the excess
never reaches zero at any width up to n=180, at any cost rung, under either gross
convention.**  4a 0/153, 4b 28/153 (0 bps 18, 10 bps 10, **25 bps 0**), no KEEP, no memo.

Script `2026-09-08_does-the-width-convergence-hold-past-n40_C.py`; outputs `.grid.csv`
(153 points), `.zero.csv`, `.walkforward.csv`, `.console.txt` (full stdout, every point).

## What was run

Two tuned parameters, all points reported:

| dial | values |
|---|---|
| p1 `n` — the ranked book's width | 5, 10, 20, 40, **60, 90, 120, 180** |
| p2 gross convention | **FIXED** (`w = G/n`, the record's) and **NORM** (`w = G/n_held`, "at pinned gross") |

Fixed and pre-registered before any number was read: G = 0.75 on every arm; weekly cadence;
plain 200d MA gate, no hysteresis; vol cap 0.60; de-gross to cash; cost rungs {0, 10, 25}
derived exactly from one 0-bps run per arm; **10 bps is the verdict rung**; next-day
execution. Control = **EW_ALL** (every priced name at G/N_priced, no gate, no ranking) —
the same book under both conventions, so it is run once. Panels are a pre-registered list
(B136 and SMALL439, which the queue names, plus U56 so idea 239's published n=5..40 ladder
can be reproduced on all three of its named panels), not a dial.

GATE: the fast path reproduces `engine.backtest` to max |Δ| **6.9e-18 / 6.9e-18 / 1.4e-17**
on U56 / B136 / SMALL439.

**Why the second dial had to be a dial.** The record builds the ranked book FIXED, so when
fewer than `n` names are eligible the shortfall sits in cash and *realised gross falls as n
rises*. On a 135-name panel an `n = 180` FIXED book is a **de-grossed** book, not a wide one
(U56 FIXED at n=180: realised gross **0.156**, CAGR **2.20%**). Reading "excess reaches
zero at large n" off a FIXED ladder alone is therefore uninterpretable. Realised gross is
published beside every arm (the 2026-09-08 cloud run's proposal), and every reading below is
quoted under both conventions.

SURVIVORSHIP: SMALL439 and B136 are current constituents (PROTOCOL 9,
`data/SMALL_PANEL_README.md`); every panel-level number here is relative, never achievable.

## 1. The ladder turns around — mean excess over EW_ALL @10bps, 3 named panels

| n | 5 | 10 | 20 | 40 | 60 | 90 | 120 | 180 |
|---|---|---|---|---|---|---|---|---|
| FIXED, full | −0.2590 | −0.2091 | −0.1376 | **−0.1270** | −0.1293 | −0.1167 | −0.1289 | −0.1368 |
| FIXED, OOS | −0.2165 | −0.1897 | −0.1094 | **−0.0527** | −0.0560 | −0.0470 | −0.0728 | −0.0952 |
| NORM, full | −0.2690 | −0.2075 | **−0.1560** | −0.1585 | −0.1526 | −0.1565 | −0.1694 | −0.1703 |
| NORM, OOS | −0.2243 | −0.1850 | **−0.1318** | −0.1040 | −0.1049 | −0.1219 | −0.1436 | −0.1498 |
| realised gross (FIXED) | 0.745 | 0.743 | 0.734 | 0.706 | 0.636 | 0.563 | 0.494 | **0.369** |
| overlap with EW_ALL (NORM) | 0.048 | 0.096 | 0.188 | 0.351 | 0.432 | 0.518 | 0.569 | **0.597** |

The n=5..40 leg reproduces idea 239's published −0.289 / −0.220 / −0.161 / −0.131 in sign,
size and slope (that ladder was 23 panels including sub-panels; this is its 3 named panels).
**Past n=40 the monotone improvement stops.** Per panel, at 10 bps NORM, excess from n=5 to
the grid edge and the best point on the whole dial:

| panel | excess n=5 | excess n=180 | best n | best excess | mean held at n=180 | mean eligible/day | of |
|---|---|---|---|---|---|---|---|
| U56 | −0.2027 | −0.0749 | **20** | −0.0605 | 37.4 | 37.5 | 55 |
| B136 | −0.2460 | −0.0967 | **120** | −0.0958 | 91.3 | 91.5 | 135 |
| SMALL439 | −0.3582 | −0.3393 | **10** | −0.2014 | 136.6 | 142.1 | 439 |

## 2. The answer to the queue's question

Smallest n with excess ≥ 0, at the 10-bps verdict rung, over (panel × convention × window):
**3 of 24 cells reach zero — and all three are U56**, the 55-name panel where "n = 180" has
no meaning. **B136: 0 of 8. SMALL439: 0 of 8.** At 25 bps, 0 of 24. The zero-crossings:

- U56 FIXED, H2 and OOS, at n=20 (realised gross 0.717 — not a de-gross artefact).
- U56 NORM, OOS only, at n=40, by **+0.0001**.
- At 0 bps only, B136 FIXED crosses at n=90 — with realised gross **0.669**, i.e. a book
  that has quietly moved a third of NAV to cash. Under NORM at pinned gross the same panel
  never crosses at any rung. **That crossing is the de-gross channel, not convergence.**

## 3. Why it never gets there — the limit is the GATE, not the control

The ranked book is gated (200d MA) and vol-capped (<0.60); EW_ALL is neither. So widening
`n` saturates on the **eligible set**, not the panel: mean eligible/day is 37.5 of 55 (U56),
91.5 of 135 (B136), 142.1 of 439 (SMALL439). Overlap with EW_ALL therefore tops out at
**0.691 / 0.695 / 0.405** and never reaches 1.0. On U56 NORM the arms at n = 60, 90, 120 and
180 are *byte-identical* — the book has held every eligible name since n=60.

That splits idea 239's "the ranking is the cost" into two terms. Excess at n=5 is the
ranking cost **plus** the gate cost; excess at saturation is the gate cost alone (10 bps,
NORM):

| panel | total (n=5) | ranking (n=5 → saturation) | **gate + vol cap (residual)** | gate's share |
|---|---|---|---|---|
| U56 | −0.2027 | −0.1278 | **−0.0749** | 37% |
| B136 | −0.2460 | −0.1493 | **−0.0967** | 39% |
| SMALL439 | −0.3582 | −0.0189 | **−0.3393** | **95%** |

**On the small panel essentially the whole −0.34 deficit is the 200d gate and the vol cap,
not the ranking** — which is not what idea 239's width reading implies. (Caveat: SMALL439
holds 136.6 of 142.1 eligible names at n=180, so it is 96% saturated, not fully; its excess
is already reversing, so more width will not close it.)

Turnover says the same thing. At pinned gross, widening does **not** buy a cheap book: U56
falls only 18.5 → 8.2 turns/yr and floors there, because at saturation the remaining
turnover is the *gate's* churn, not the ranking's. The FIXED ladder's apparent collapse to
1.0 turns/yr at n=180 is again just the shrinking gross.

## 4. What is left of the book at the wide end (10 bps)

| panel | conv | n | realised gross | CAGR | Sharpe | MaxDD | turn/yr | overlap |
|---|---|---|---|---|---|---|---|---|
| U56 | NORM | ≥60 | 0.750 | 10.40% | 1.0492 | −15.87% | 8.21 | 0.691 |
| U56 | FIXED | 180 | **0.156** | **2.20%** | 1.1232 | −3.40% | 1.00 | 0.208 |
| B136 | NORM | 120 | 0.750 | 10.72% | 1.0262 | −17.69% | 8.27 | 0.695 |
| B136 | FIXED | 180 | **0.381** | **5.25%** | 1.0585 | −9.06% | 2.51 | 0.508 |
| SMALL439 | NORM | 180 | 0.750 | 3.73% | 0.3394 | −40.02% | 13.31 | 0.405 |
| SMALL439 | FIXED | 180 | **0.569** | **2.80%** | 0.3325 | −22.23% | 7.67 | 0.405 |

The FIXED rows are the warning: their Sharpe is flat or *higher* and their drawdown a third
of the NORM book's, purely because they are 44–84% cash. A width claim quoted without
realised gross beside it cannot be told apart from a cash claim.

## 5. Rule 8 walk-forward (PROTOCOL 8) — n chosen on 2009–2016 IS Sharpe only

18 (panel × convention × rung) cells; 2017–2026 read once.

- The IS pick is **n = 10 or 20 at 0 and 10 bps and n = 60–180 at 25 bps** (cost buys width).
- **The chooser beats its own do-nothing EW_ALL control OOS in 4 of 18**, beats RULES v2 in
  **0 of 18**, beats SPY in 10 of 18 — and the control already beats SPY on every panel but
  SMALL439, so the 10 is not the chooser's.
- **The un-ranked control has the higher IS Sharpe in 16 of 18 cells.** This run's rule-8
  menu is the n-ladder only, so a ranked arm can be "selectable" here that idea 460's
  control-inclusive menu would never pick. That is a menu artefact and is reported as one.
- Named picks at 10 bps: U56 FIXED n=20 → OOS **1.1680 / 14.36% / −18.31%**; B136 FIXED
  n=10 → OOS 0.7831 / 12.75% / −21.44%; SMALL439 FIXED n=180 → OOS 0.2477 / 2.04% /
  −22.23%. Controls OOS: 1.1357 / 1.1022 / 0.6374. RULES v2 OOS 1.2851 / 9.53% / −12.05%.
  SPY OOS **0.8820 / 15.45% / −33.72%**.

## 6. Both KEEP paths, all 153 grid points

**4a: 0/153.** Nothing beats RULES v2's Sharpe in both halves without a worse drawdown.

**4b: 28/153 — 18 at 0 bps, 10 at 10 bps, 0 at 25 bps.** Every one of the 10 passers at the
verdict rung has **NEGATIVE excess over its own control** (−0.0319 to −0.1333; the best is
U56 FIXED n=20). They clear 4b on the **drawdown cap** — MaxDD −16.7% to −19.1% against
SPY's 60% bar of −20.2% — while their own EW_ALL controls fail 4b on DD (U56 −22.5%, B136
−25.4%, SMALL439 on four bars). This is exactly the pattern ideas 239, 459 and 460 record:
**4b is passed by holding fewer names, not by ranking them better.**

The only rule-8-selectable 4b passers at the verdict rung are U56 n=20 under both
conventions — **the same book idea 460 already filed as PARK**, and it is selectable here
only because the control is off this run's menu (IS 0.9929 vs the control's 1.1100). It is
**not** re-filed as a KEEP. **PARK stands; no memo, no RULES change.**

## 7. What this changes in the record

1. Idea 239's "excess is a WIDTH function, monotone in n" is **true only on 5 ≤ n ≤ 40**.
   Extended to n=180 the curve turns: the record should quote it as *stops at n≈20–40*, not
   as an open-ended convergence, and QUEUE 243's "unbounded width curve" reading is
   contradicted at pinned gross.
2. A ranked book converges to the **gated** equal-weight book, never to EW_ALL, so a
   residual excess of −0.07 to −0.34 is structural and is the **gate's**, not the ranking's.
   On SMALL439 that residual is 95% of the whole deficit.
3. Every published FIXED count sweep with n above a panel's eligible breadth is partly a
   cash sweep. Realised gross belongs beside every count-dial arm (cloud 2026-09-08's
   proposal), and this run's B136 zero-crossing at n=90 is a live example of a reading that
   exists only in the FIXED column.
