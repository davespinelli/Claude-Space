# Idea 1771 (lane B, 2026-09-20) — IS THE STANDING VOLTGT016 4b OOS PASS DECIDABLE ACROSS THE SIGMA-CONVENTION SURFACE?

**ANSWERED — NO. IT IS A KNIFE-EDGE, AND THE KNIFE IS THE TARGET RUNG, NOT THE CONVENTION.
DOWNGRADE THE STANDING KEEP-4b CANDIDATE TO PARK AND KILL THE `t = 0.16` CERTIFICATION.
THE DIAL SURVIVES: VOL-TARGETING IS THE FIRST DEVICE IN THIS RECORD TO BEAT ITS OWN
REALISED-GROSS-MATCHED CONSTANT-GROSS TWIN AT SCALE. NO NEW BOOK; NO RULES CHANGE (rule 6).**

Script: `research/backtests/2026-09-20_voltgt-sigma-convention-surface_B.py`
Artifacts: `.grid.csv` (2,400 scored rows) · `.pass_share.csv` · `.twin.csv` · `.walkforward.csv` · `.gates.csv` · `.log.txt`

## The defect this closes

The record has exactly one standing KEEP-4b candidate (`2026-09-20_voltgt-panel_KEEP4b_MEMO.md`,
idea 1730). Its U56 4b OOS pass clears the drawdown cap by **0.37 pp** and addendum A1 (idea 1715)
already flipped it to FAIL by reading `sigma` one day staler — **one** alternative convention,
tested **once**. `sigma_t` is not a primitive: it is a convention with a LOOKBACK `L` and a
STALENESS `d`, and the memo's RULES wording fixes neither. The surface those choices span had
never been mapped.

## Construction

Tuned (2, the protocol maximum, all 20 grid points reported): `L ∈ {5,10,20,40,60}`,
`d ∈ {0,1,2,5}`. Published, not tuned: target `t ∈ {0.08,0.10,0.12,0.16,0.20}`, panel
{U56, B136, SMALL665}, cost {0,10,25,50} bps. Control: every VOLTGT book paired with its OWN
constant-gross twin carrying the SAME REALISED MEAN GROSS on the SAME window (bisection to
< 1e-10). **300 VOLTGT books + 600 matched twins × 4 cost rungs = 2,400 scored rows, all published.**
Verdict rules V1–V4 were fixed in the script header before the run.

## Replication first

Idea 1730's memo reproduces to **max |Δ| 2.8e-04** across its 12 published numbers (U56 FULL
15.61% / 1.2028 / −19.86%, OOS 15.94% / 1.2196 / −19.86%; B136 FULL 15.94% / 1.2050 / −18.76%,
OOS 15.36% / 1.1839 / −18.76%), and idea 1715's A1 reproduces **exactly**: `d = 1` gives U56 OOS
MaxDD **−20.7709%** against the published −20.77%, 4b OOS FAIL. Gates **10/10**; the run's fast
path equals `engine.backtest` at **≤ 3.5e-17** on all three panels at two cost rungs.

## The answer — V1 TRIGGERED

At the candidate's own target `t = 0.16`, the **CONVENTION PASS-SHARE** is **0.250 on U56
(5 of 20 cells) and 0.400 on B136 (8 of 20)**. The memo's cell `(L=20, d=0)` is one of the five.
A 4b pass holding at a quarter of the conventions its own rule wording leaves open is a property
of the cell, not of the book. V2 (≥ 0.75 on both panels) is not met. **PARK, not KEEP.**

## But the carrier is the TARGET RUNG, and it is a two-sided squeeze

The 4b failure is almost entirely the **DD cap `L4_DD`**, and its OOS fail-share is monotone in `t`:

| panel | t=0.08 | 0.10 | 0.12 | 0.16 | 0.20 |
|---|---|---|---|---|---|
| U56 DD fail | 0.00 | 0.10 | 0.20 | **0.75** | **0.95** |
| U56 CAGR fail | **0.45** | 0.00 | 0.00 | 0.00 | 0.00 |
| U56 4b OOS pass-share | 0.55 | **0.90** | **0.80** | 0.25 | 0.05 |
| B136 DD fail | 0.00 | 0.10 | 0.25 | 0.60 | 0.80 |
| B136 CAGR fail | **0.85** | 0.00 | 0.00 | 0.00 | 0.00 |
| B136 4b OOS pass-share | 0.15 | **0.85** | **0.75** | 0.40 | 0.20 |

4b on this family is a **two-sided squeeze**: the CAGR floor binds below `t ≈ 0.10`, the DD cap
binds above `t ≈ 0.12`, and the convention-robust band is `t ∈ {0.10, 0.12}` on BOTH panels. **The
memo's `t = 0.16` sits on the wrong side of the squeeze.** (This is also a counter-example to the
record's standing "the CAGR floor is the binding leg almost every time": here DD binds 0.40 of the
whole U56 surface against CAGR's 0.09.)

## Why the chooser walks INTO the fragile rung

IS Sharpe (2011–2016) **peaks at `t = 0.16` on both panels** (U56 1.1822 at L20/d0 vs 1.1339 at
t=0.12; B136 1.2301 vs 1.1572) — exactly where the DD cap is knife-edge out of sample. Worse, the
IS argmax over the whole surface is `t0.16 L20 **d1**` on both panels (U56 1.1897 > d0's 1.1822),
i.e. the in-sample objective prefers the **staler** convention, and that is the cell A1 showed
fails 4b OOS.

## Rule 8 (2011/2009–2016 chooses; 2017–2026 read ONCE)

Three legal IS-only choosers × 3 panels × 2 arms (t fixed at 0.16 / t free), plus `C_MEMO` (the
memo's own cell — no choice at all, the hindsight control).

* **At the candidate's own rung on U56, 0 of 3 legal choosers reach a 4b-OOS-passing cell.**
  `C_ISSHARPE` and `C_ISLEGS` both pick `L20 d1` → OOS 15.76% / 1.2012 / **−20.77% FAIL**;
  `C_ISDD` picks `L40 d1` → **−20.83% FAIL**. Only `C_MEMO` passes, and `C_MEMO` is hindsight.
* On B136 the same rung survives all three (OOS 1.1621 / −19.30%, 1.1621, 1.1697 / −19.68%) —
  so **whether the candidate passes depends on the panel AND on which of three equally defensible
  IS-only choosers you use.**
* With `t` free, `C_ISLEGS` lands on **`t = 0.12`** on BOTH panels and passes 4b OOS on both
  (U56 `t0.12 L40 d0` 14.48% / 1.2392 / −18.06%; B136 `t0.12 L20 d0` 13.86% / 1.2220 / −16.01%) —
  a legal, IS-only route to a passing cell, and it does not go through `t = 0.16`.
* **Totals: 4b OOS 7 of 18 legal picks; 4a OOS 0 of 24.** SMALL665: 0 of 8 picks, every one below
  SPY (best OOS 0.4901 against SPY 0.8738).

## Control — V4 NOT triggered: the vol-target dial beats its matched twin

At **identical realised mean gross**, pooled over all 100 cells per panel at 10 bps:

| panel | mean dSharpe | mean dMaxDD | win share | OOS dSharpe | OOS dMaxDD | OOS win | 4b OOS VOLTGT | twin |
|---|---|---|---|---|---|---|---|---|
| U56 | +0.0263 | +6.05 pp | 0.770 | **+0.0587** | **+6.16 pp** | 0.810 | **51/100** | 4 |
| B136 | +0.0204 | +8.96 pp | 0.720 | **+0.0503** | **+9.44 pp** | 0.790 | **47/100** | 0 |
| SMALL665 | −0.1540 | +3.58 pp | 0.000 | −0.2516 | +1.80 pp | 0.000 | 0/100 | 0 |

At the memo's own cell the twin (constant gross `k = 0.9338`, matched to 1e-10) posts OOS
17.06% / **1.1266** / **−27.46%** against the VOLTGT book's 15.94% / 1.2196 / −19.86%: +0.093 of
Sharpe and **+7.6 pp of drawdown** bought by the time-variation alone. The twin's only four 4b OOS
passes in the whole run are `t=0.08, L=60` cells where it is simply a low constant gross (k ≈ 0.662).
**This is the first device in this record to survive its own realised-gross-matched twin at scale**
(against BAND, MAXVOL, SPYFILT, STOP, MADIST and the eight sleeves, all of which lost). It does not
survive on SMALL, where the plain twin wins 100 of 100 — the same panel-dependence idea 1632 found
for the band.

## Cost ladder and small caps

4b OOS passes over the 100 cells per panel: U56 58 / **51** / 38 / 29 and B136 57 / **47** / 40 / 31
at 0 / 10 / 25 / 50 bps. **SMALL665: 0 / 100 at every cost rung and every convention**, confirming
addendum A2 on a 5× wider surface (L1_H1 fails 1.000 of OOS cells there).

## What this run does and does not establish

* It **does not** certify `t = 0.10` or `t = 0.12`. The pass-share table is an OOS-visible
  statistic and cannot select a rung. What is legal is the rule-8 result: `C_ISLEGS` with `t` free
  reaches `t = 0.12` on both panels from in-sample information alone, and that pick clears 4b OOS.
  A re-specified candidate at `t = 0.12` needs its own run with the chooser pre-registered.
* It **does not** close idea 1537 (which asks for a block bootstrap of the VOLTGT-vs-twin dMaxDD on
  a finer target ladder); this run's twin contrast is unbootstrapped.
* **SURVIVORSHIP:** U56 and B136 are CURRENT constituents; SMALL665 is a current sub-$2B screen
  (54 names with `max_1d_move >= 1.0` dropped, 665 remain). Every pass count above is the
  optimistic read.

## Residue for the Sunday review (rule 6 — nothing enacted here)

1. **The standing KEEP-4b candidate should be read as PARK.** Its rung is the least
   convention-robust on its own published grid and is unreachable on U56 by every legal IS-only
   chooser tested.
2. **Publish the CONVENTION PASS-SHARE beside any 4b verdict whose signal has a lookback**, the way
   idea 956 proposed the phase pass-share for the rebalance date. It is free, it is a statement
   about the book rather than an estimator, and on this corpus it separates a 0.90 book from a
   0.25 book that read identically at their canonical cell.
3. **Any RULES wording that names a volatility must also name its lookback and its staleness.**
   The memo's clause names neither and is therefore not implementable without a second, uncertified
   choice.

`RULES.md`, `PROTOCOL.md`, `scan.py`, `bot.py` and `baseline.py` are UNTOUCHED by this run.
