# Idea 260 — is-RAND-beating-FWD-persistence-or-pick (lane C, 2026-09-06)

**ANSWERED. The sign SURVIVES the separation — and idea 82's published magnitude does
not.** At 0 bps, `FWD − RANDW` (weekly re-draw) is **−0.0236, t −3.60, positive in 20/64
draws**, i.e. *more* negative than idea 82's held-draw isolate, so the negative sign is
about the **pick**, not about persistence. But idea 82's own `FWD − RANDH` is
**−0.0111, t −1.45 (not significant) at 0 bps** and only reaches its published −0.0213 /
t −2.72 at 10 bps: **roughly half of the record's isolate is the composite's own turnover
bill**, not a statement about ranking. And the random arm's pick advantage is worth
**1.0–1.3 bps**: at PROTOCOL's own 10 bps rung `FWD − RANDW` is **+0.2883, t +11.19, 8/8**
(OOS +0.338, 3/3). No RULES change, no new KEEP-candidate, no memo. Nothing in `RULES.md`,
`scan.py`, `bot.py` or `baseline.py` touched.

Script: `2026-09-06_is-RAND-beating-FWD-persistence-or-pick_C.py` · console `…_C.console.txt` ·
grids `…_C.{grid,comparisons,headline,seeds,breakeven,walkforward}.csv`

## Design

Idea 82's run, verbatim, plus one arm and two extra cost rungs. Panels U56 / B136 /
BSTK100, weekly, next-day execution, gate = above-200d AND vol20 < 0.60, key = the
composite without the vol scaler, **gross matched at 0.75 on every arm including EWall**,
n ∈ {20,30,40,60}, 8 seeds, every seed reported. Two tuned parameters: **panel** and **n**.

| arm | pick | persistence | turnover (x/yr, n=20) |
|---|---|---|---|
| `EWall` | every eligible name | gate only | 8.2–8.6 |
| `FWD` | top-n by the composite | gate + rank drift | 11.0–14.3 |
| `REV` | bottom-n by the composite | gate + rank drift | 16.8–29.9 |
| `RANDH` | **idea 82's RAND, byte-for-byte** — one uniform per name, drawn once (rng 1000+seed), held | gate only | 8.6–9.3 |
| `RANDW` | **new** — a fresh uniform per name at **every rebalance date** (rng 2000+seed) | none | **38.4–60.2** |

Cost rungs **0 / 10 / 30 bps**, all reported on every point. `engine.backtest` computes
`port = (held·rets).sum − turnover·bps/1e4` and neither `held` nor `turnover` depends on
the rung, so each book is run once at 0 bps and the other rungs are derived exactly.
**Harness identity asserted before any result was read: derived vs live `backtest()` =
`0.000e+00`** on FWD20@10bps and RANDW20 seed 0 @30bps; the run aborts otherwise. The
decomposition `(FWD−RANDW) = (FWD−RANDH) + (RANDH−RANDW)` holds at `0.000e+00`.

Grid = 3 panels × 74 books × 3 rungs = **666 points, all in `.grid.csv`**. Saturated cells
(`sat_share > 0.25`, a panel that cannot supply n names) are excluded from headline counts
exactly as in idea 82, leaving 8 of 12 cells.

**Reproduction gate.** `U56/CAND20 FIXED` **12.7% / 1.092 / −18.3%, halves 1.088/1.102**
vs published 12.7%/1.093/−18.3%, 1.088/1.103 (idea 81's last-digit gap). `U56/RULES v1`
6.5%/0.664/−13.8% vs 6.5%/0.666/−13.8%. Idea 82's isolate at 10 bps reproduces to the
digit: `FWD − RANDH` **−0.0213, t −2.72, 21/64** per (cell, seed); its cell-level headline
`EWall − FWD` **+0.0467, t +4.03, 7/8**. `B136/EWall` 4b pass and `U56/FWD20` 4b pass both
reproduce.

## 1. The queue's question: the sign KEEPS at 0 bps, and it is the PICK

Sharpe, over the 8 unsaturated cells (RAND arms are the 8-seed mean):

| bps | `FWD − RANDH` (held draw) | `FWD − RANDW` (weekly re-draw) | `RANDH − RANDW` (persistence alone) |
|---|---|---|---|
| **0** | **−0.0111, t −0.99, 2/8** | **−0.0236, t −2.27, 1/8** | −0.0125, t −1.82, 2/8 |
| 10 | −0.0213, t −1.73, 1/8 | **+0.2883, t +11.19, 8/8** | +0.3096, t +10.91, 8/8 |
| 30 | −0.0416, t −2.80, 1/8 | **+0.9058, t +10.82, 8/8** | +0.9474, t +10.50, 8/8 |

Per (cell, seed), 64 draws: `FWD − RANDW` at 0 bps **−0.0236, t −3.60, 20/64**;
`FWD − RANDH` at 0 bps −0.0111, **t −1.45, 29/64**.

Pre-registered branch **(a) holds**: the sign is negative at the sign rung and survives
separating persistence from the pick — it gets *more* negative, not less. Idea 82's
finding is **about the pick**, under its own label.

The one cell that goes the other way is again **U56 n=20** — the project's own universe at
the incumbent count — where `FWD − RANDW` is **+0.0394** at 0 bps and FWD never loses at
any rung (+0.328 at 10, +0.901 at 30).

## 2. What the separation costs idea 82's published number

`FWD − RANDH` moves −0.0111 → −0.0213 → −0.0416 across 0/10/30 bps, i.e. **−0.0102 per
10 bps**, which is exactly FWD's excess turnover over RANDH (12.9x vs 9.1x/yr at n=20,
≈0.38 pp/yr on ≈12% vol). So the record's isolate is **≈52% cost and ≈48% pick**, and at
0 bps its pick half does not clear t = 2. **Every published quotation of "the composite
adds nothing over a random pick" is quoting a number half of which is the composite's own
trading bill.** The queue was right that the arm was not measuring what it was named; it
was wrong about which channel was contaminating it.

## 3. The persistence leg is nothing at 0 bps and everything above it

`RANDH − RANDW`: Sharpe **−0.0125 (t −1.76)**, CAGR **−0.0001 pp/yr (t −0.07, 3/8)** at 0
bps. Holding a random subset for seventeen years earns *exactly zero* expected return over
re-drawing it weekly, and loses a little Sharpe (the weekly re-draw time-diversifies
idiosyncratic risk). At 10 bps the same leg is **+0.3096** and at 30 bps **+0.9474** —
all of it the 51.2x/yr turnover bill. Persistence, in this book, is a **cost** variable and
not a **return** variable, which is the cleanest available statement of why idea 82's
pre-registration was right to hold the draw and wrong to call the result a ranking number.

## 4. The Sharpe/CAGR reversal is NOT a persistence artefact

Idea 82's KILL rested on `FWD − RAND` being −0.021 on Sharpe and +1.25 pp/yr on CAGR. Both
halves reproduce on the fresh-draw arm:

| metric, 0 bps | `FWD − RANDH` | `FWD − RANDW` | `RANDH − RANDW` |
|---|---|---|---|
| CAGR | **+1.57 pp/yr, t +4.83, 8/8** | **+1.57 pp/yr, t +5.93, 8/8** | −0.01 pp/yr, t −0.07 |
| \|MaxDD\| | +1.25 pp, t +4.59, 8/8 | +1.38 pp, t +5.45, 8/8 | +0.13 pp, t +3.25 |

The composite buys **1.57 pp of CAGR for 1.38 pp of MaxDD** against a genuinely fresh
random pick, at zero cost — a risk-budget trade, identical to the one idea 82 measured
against the held draw. Idea 82's reversal is **confirmed and is not an artefact of the
held draw.**

## 5. The random arm's edge is worth 1 bp

Sign flip of `FWD − RANDW` on Sharpe, by linear interpolation on the measured ladder:

| panel, n | 0 bps | 10 bps | 30 bps | flip | turnover FWD / RANDW |
|---|---|---|---|---|---|
| U56 20 | +0.0394 | +0.328 | +0.901 | **no flip** | 11.0 / 38.4 |
| B136 20 | −0.0588 | +0.395 | +1.286 | **1.3 bps** | 14.3 / 60.2 |
| B136 30 / 40 / 60 | −0.045 / −0.033 / −0.022 | +0.349 / +0.301 / +0.193 | +1.125 / +0.963 / +0.623 | 1.1 / 1.0 / 1.0 bps | 12.5–9.8 / 52.2–31.5 |
| BSTK100 20 / 30 / 40 | −0.034 / −0.026 / −0.009 | +0.305 / +0.243 / +0.194 | +0.974 / +0.777 / +0.598 | 1.0 / 1.0 / 0.5 bps | 13.5–10.5 / 55.0–35.3 |

**The whole "a coin flip beats the composite" reading lives below 1.3 bps of round-trip
cost, on a protocol whose binding assumption is 10.** It is a statement about a
frictionless market.

## 6. Rule 8 walk-forward (IS 2009–2016 chooses, OOS 2017–2026 read once)

Pooled equal-weight over the 3 panels:

| selector | 0 bps CAGR/Sharpe/MaxDD | 10 bps | 30 bps |
|---|---|---|---|
| ALL_ISARGMAX | 12.9% / **1.178** / −20.1% | 11.4% / **1.048** / −19.8% | 9.0% / 0.836 / −21.0% |
| EWALL | 12.3% / 1.126 / −19.6% | 11.4% / 1.047 / −19.9% | 9.5% / **0.888** / −20.6% |
| **RANDW20** | 12.3% / 1.093 / −20.0% | **6.6% / 0.630 / −20.6%** | **−3.9% / −0.286 / −40.2%** |
| RANDH20 | 12.4% / 1.090 / −20.1% | 11.3% / 1.007 / −20.4% | 9.2% / 0.840 / −21.4% |
| FWD20 | 14.8% / 1.062 / −21.8% | 13.3% / 0.968 / −21.9% | 10.4% / 0.781 / −22.1% |
| SPY | 15.5% / 0.882 / −33.7% | 15.5% / 0.882 / −33.7% | 15.5% / 0.882 / −33.7% |
| RULES v1 | 9.6% / 0.853 / −17.6% | 6.5% / 0.609 / −18.7% | 0.7% / 0.120 / −23.2% |

`FWD20 − RANDW20` OOS Sharpe: **−0.031 (wins 1/3) at 0 bps, +0.338 (3/3) at 10 bps,
+1.066 (3/3) at 30 bps.** The in-sample sign and the out-of-sample sign agree at every
rung, including the flip. `RANDW20` is the only selector in the table whose OOS Sharpe goes
**negative** by 30 bps.

## 7. KEEP paths

4b passes, 157 of 666 points:

| rung | EWall | FWD | REV | RANDH | RANDW | v1 |
|---|---|---|---|---|---|---|
| 0 bps | 2/3 | 8/12 | 2/12 | 57/96 | **63/96** | 0/3 |
| **10 bps** | 1/3 | 5/12 | 0/12 | 19/96 | **0/96** | 0/3 |
| 30 bps | 0/3 | 0/12 | 0/12 | 0/96 | 0/96 | 0/3 |

At 0 bps the weekly re-draw is the **best** 4b arm on the board; at PROTOCOL's own rung it
passes **zero of 96**. Nothing new is claimed: `B136/EWall` (10.7%/1.026/−17.7%, halves
1.146/0.914, OOS 1.019) and `U56/FWD20` (12.8%/1.064/−18.3%, halves 1.068/1.066, OOS
1.131) are ideas 10 and 2's published books, reproduced. **No new KEEP-candidate, so no
memo.**

## Verdict

**ANSWERED — idea 82's SIGN is CONFIRMED, its MAGNITUDE is corrected, and its label needs
one more qualifier than the queue asked for.** The negative `FWD − RAND` is a pick
statement and it survives (indeed strengthens) a fresh weekly draw at 0 bps. But the
published −0.0213 is roughly half the composite's own turnover bill; the pick half alone is
−0.0111 at t −1.45, which does not clear the record's own significance habit. And the
reading the number invites — "a coin flip is as good as the ranking" — is priced: it is
true below **1.0–1.3 bps** and false, by **+0.29 of Sharpe at t +11 and 8/8**, at the 10
bps this protocol is built on. **The correct standing quotation is: at zero cost the
composite's top-n is not reliably better risk-adjusted than a random n of the same eligible
set, while earning +1.57 pp/yr more CAGR for +1.38 pp more drawdown; at any fundable cost
the composite wins outright because the ranking is persistent and a coin flip is not.**

**SURVIVORSHIP.** B136 / BSTK100 are current constituents, one-directional. The bias runs
**toward RANDH and against RANDW**: a random subset *held* for the sample collects the full
survivorship premium of whatever it drew, while a weekly re-draw keeps re-entering it at a
fresh cost. So the finding that the sign survives the re-draw (§1) is measured *against*
the panel's own headwind and is the conservative direction; the persistence leg in §3 is
measured *with* it and its 0-bps Sharpe reading (−0.0125, t −1.76) should be treated as an
upper bound on how little persistence is worth.

**Follow-ups queued:** 261 (back-fill the 0-bps rung under every published gross-matched
arm difference, since §2 shows a turnover-bill contaminant that no cost rung exposes),
262 (is the 1-bp breakeven a general property of the record's random/null arms), 263
(the persistence-vs-cost decomposition as a required column beside any turnover-mismatched
comparison).
