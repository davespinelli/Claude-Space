# Idea 234 — re-read-single-rung-argmaxes-on-V1C-shaped-books (lane B, 2026-09-08)

**Verdict: SPLIT — the MECHANISM is confirmed and now has a paired test; the FLAG is killed as a
record-wide asterisk.** V1C-shaped books really are the rung-sensitive construction (10 of 15
panel x dial cells re-rank across 0/10/30 bps vs 3 of 15 for the same book un-scaled and 5 of 12
for the un-ranked one; Fisher p 0.0269, and on the 15 matched V1C-vs-TOPN pairs the asymmetry is
**7-0**, McNemar exact p 0.0156). But the queue's own shape test flags **40 of 7,980** published
single-rung argmax claims (0.5%, 11 files), and at PROTOCOL's own 10 bps the thing the asterisk
would warn about is worth **+0.0066 Sharpe** full-sample and **-0.0040 OOS** — reading a V1C
argmax at 0 bps instead of its true rung is, out of sample, very slightly *better*. No asterisk
is warranted at 10 bps. **No KEEP** (4a 0/2107; 4b 67/2107, 11 at 10 bps, none on >1 panel).

## Two tuned parameters, all grid points reported
* **p1 = turnover threshold T of the shape test** {0 (off), 10, 20, 30, 50} x/yr — the queue names 20. `.flagcurve.csv`
* **p2 = cost rung** {0, 5, 10, 15, 20, 25, 30} bps — the queue names 0/10/30; the whole ladder is free under the cost identity and all of it is in `.grid.csv` (2,107 points).
The vol-scaled leg has two pre-registered readings (LOOSE / NAMED); **both** are reported, neither selected.

## Part A — the census (exact, 1,892 committed CSVs)
1,123 carry a Sharpe-like objective; **510 are single-rung parents**; inside them sit **7,980
published dial-argmax claims** (2,585 sweep a numeric dial, 5,395 a categorical choice —
panel/book/arm/family). **157 claims name 10 bps explicitly; 7,823 inherit it implicitly**, so
"the record quotes one rung" is true of essentially the whole record.
Vol-scaled ranking: **902 claims LOOSE / 758 NAMED**. Adding the queue's turnover leg collapses
it: **T=10 → 158/108, T=20 → 40 claims in 11 files (22 numeric), T=30 → 1, T=50 → 0.**
Why it collapses: the median committed per-year turnover among vol-scaled claims is **2.57/yr**
(p90 17.9, p95 24.8), so `>20x/yr` cuts at the record's own 93rd percentile. Worse, **the live
V1C construction fails its own leg on the live panel** — V1C's median arm turnover is 13.6/yr on
U56 (23.7 on B136, 32.2 on SMALL439), and only 53.6% of V1C arms clear 20/yr at all. The turnover
leg is also read off whatever column each file committed (`Turn/yr`, `turnover`, `turn_dg`,
`turnover_yr`), whose units are not uniform across the record — a further reason not to lean on it.
The 11 flagged files are named in `.console.txt` and every claim is in `.claims.csv`.

## Part B — the live re-run at 0/10/30 (3 panels x 3 books x 5 dials, 268 sims, 2,107 points)
Cost identity `net(c) = gross - turn*c/1e4` asserted against `engine.backtest` at 10 bps:
**max|d| = 1.4e-17** on all three panels, so every rung is exact, not re-simulated.

| book | cells | re-rank 0/10/30 | mean cost of ignoring the rung @10 bps | @30 bps | mean turnover |
|---|---|---|---|---|---|
| **V1C** (vol-scaled ranking) | 15 | **10** | **0.0066** | 0.0580 | 20.2/yr |
| TOPN (same book, un-scaled) | 15 | 3 | 0.0032 | 0.0115 | 16.6/yr |
| EWALL (no ranking) | 12 | 5 | 0.0002 | 0.0029 | 9.7/yr |

Fisher two-sided **p 0.0269** (V1C 10/15 vs controls 8/27). Matched pairs (same panel, same dial,
same eligible set): V1C-only re-ranks **7**, TOPN-only **0**, both 3, neither 5 — **McNemar exact
p 0.0156**. This is the first paired evidence for idea 230's construction claim.
**But the frequency is not the cost.** The paired difference in the cost of ignoring the rung at
10 bps is **+0.0034 Sharpe**, and V1C is the larger of the pair in only **6 of 15**. 12 of the 18
re-rank cells cost **< 0.006** Sharpe at 10 bps; the whole effect lives at 20-30 bps (V1C mean
0.0580 at 30, driven by SMALL439 K 0.2913 and B136 N 0.1488).

## Rule 8 (walk-forward: dial picked on 2009-2016, 2017-2026 read once)
V1C, mean over 15 cells — OOS Sharpe of the IS pick vs comparands:

| rung | picks moved vs the 0-bps pick | OOS pick | do-nothing | random | oracle | premium vs do-nothing | cost of the 0-bps pick |
|---|---|---|---|---|---|---|---|
| 0 bps | 0/15 | 0.8622 | 0.8692 | 0.8450 | 0.9273 | **-0.0071** | 0.0000 |
| **10 bps** | 4/15 | 0.7054 | 0.7133 | 0.7000 | 0.7928 | **-0.0079** | **-0.0040** |
| 30 bps | 9/15 | 0.5183 | 0.4011 | 0.4097 | 0.5429 | +0.1171 | +0.1147 |

At PROTOCOL's own rung the rung-aware chooser is **behind** both do-nothing and its own cost-blind
twin; the ramp only turns positive at 15 bps and above (TOPN +0.0277, EWALL -0.0094 at 10). This
is idea 235's rung ramp reproduced on a fresh construction and a fifth dial, and it is what kills
the asterisk: the failure mode the flag names does not cost anything at the cost the project trades.

## KEEP paths (evaluated on every one of the 2,107 grid points)
**4a: 0 passes** — nothing in the grid beats live RULES v2 in both halves with no worse MaxDD.
**4b: 67 passes**, of which **11 at 10 bps** (U56 10, B136 1) and **0 of 11 hold on more than one
panel**, so all are PARK under the record's standing single-panel convention. The recurring names
are already-PARKed arms (U56 V1C/TOPN n=40, U56 EWALL g=0.03 and k=2, B136 EWALL gross=0.75).
**No RULES change proposed.**

## Caveats
SURVIVORSHIP: universe.json and universe_broad.json are current constituents; SMALL439 is current
constituents of a sub-$2B screen with the 44 max_1d_move>=1.0 tickers dropped (see
`data/SMALL_PANEL_README.md`). All long-book numbers are upper bounds. The Part A vol-scaled leg
is a text test on the sibling script, not on the traded weights — it can call a script V1C-shaped
because it *builds* a vol-scaled key somewhere; the NAMED reading removes cases whose own book
label says otherwise, and both readings are reported because neither is provably right.

## Reportable clause offered to the Sunday review
> A published single-rung argmax on a vol-scaled-ranking book carries a rung asterisk **only above
> 15 bps**. At PROTOCOL's own 10 bps the argmax moves in 4 of 15 cells and the move is worth
> +0.0066 Sharpe in sample and **-0.0040 out of sample**, so no re-quote is required. The queue's
> ">20x/yr turnover" leg is not a usable filter: it flags 40 of 7,980 claims and does not flag the
> live book on the live panel.
