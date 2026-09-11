# Idea 694 — is-the-WIDTH-to-OOS-slope-a-SELECTION-POOL-effect-or-a-SMALL-CAP-effect (cloud, 2026-09-11)

**ANSWERED / SPLIT — IT IS BOTH, AND THE CAP-MIX HALF IS 20× THE WIDTH HALF. The published
slope's SIGN is a cap-mix fact (positive only in the pure-small pool, NEGATIVE at q ≤ 0.50)
and 68% of its MAGNITUDE is the fixed-n confound (selectivity + de-grossing). A residual
pool-depth slope survives at q = 1.00 only: ρ +0.5269 → +0.2387, span +0.2333 → +0.0745.
KILL for capital: 4a 0 of 1,130 rows, 4b 0 of 480 rows in the pool where the slope lives,
no pick beats SPY's OOS CAGR. No KEEP, no memo, no RULES change.**

## What was confounded

Both published ladders (ideas 685 and 688) hold the **book size n** fixed and widen the panel.
Three things move with k at fixed n, not one:

1. **pool depth** — more names to choose from (the claimed channel);
2. **selectivity** — n/k falls 10× across k = 40..400 (CAND-30: 0.7500 → 0.0750);
3. **fill / gross** — CAND-n weights each pick at GROSS/n, so when the eligible count
   `n_elig = breadth·k` is below n the book runs **de-grossed**. Measured: CAND-30's realised
   gross is **0.4324** of nominal at k = 40 and **0.9905** at k = 400. *At fixed n, width buys
   exposure.* ρ(k, fill) = **+0.6572** on the published arm.

and across the two ladders **cap mix q** moves as well. Holding n/k fixed kills (2) by
construction and (3) empirically — on the fixed-ratio grid fill is k-flat (r = 0.50:
0.6394 → 0.6346; r = 0.05: 0.9737 → 0.9931) — leaving pool depth alone.

## Construction

Tuned (2, PROTOCOL 4): **ratio r = n/k ∈ {0.05, 0.10, 0.25, 0.50} × k ∈ {40, 60, 80, 100,
200, 400}**, n = max(2, round(r·k)); all 24 cells reported at every support. Reported, never
chosen on: **q ∈ {0.00 (pure BSTK100), 0.50, 1.00 (pure SMALL439)}**, the record's fixed-n
ladder {5,10,15,20,30} + EWall, 8 seeded draws. **113 panels, 1,130 book rows, 288 picks.**
Everything else inherited: RULES v1 eligibility, v1 composite with the vol scaler off,
GROSS 0.75, weekly, 10 bps, next-day execution, 260-day warm-up, IS ≤ 2016 / OOS 2017–.

**Gates, all pre-registered, all pass.** G1 `fast_bt` vs `engine.backtest` **1.388e-17**
returns / **0.000e+00** turnover. G2 cached-rank CAND-20 vs idea 286's `cand_weights(20)`
**0.000e+00**. G3 envelope: exact width, exact cap mix, no duplicate columns, inside pools.
G4 **the reproduction**: the fixed-n arm on the replayed q = 1.00 panels matches idea 688's
committed `.books.csv` on **288 of 288 rows × 9 statistics, max |Δ| 2.054e-15**, and its
headline recomputes to **ρ(k, OOS Sharpe) = +0.5269** with means
**0.2516 → 0.2729 → 0.3232 → 0.3725 → 0.4257 → 0.4849**.

## The answer

| support | grid | ρ(k, OOS S) | mean OOS S, k = min → max | span | per-draw series positive | t |
|---|---|---|---|---|---|---|
| q = 1.00 | fixed **n** (published) | **+0.5269** | 0.2516 → 0.4849 | +0.2333 | **44/48** | 11.14 |
| q = 1.00 | fixed **n/k** (this run) | **+0.2387** | 0.3097 → 0.3842 | **+0.0745** | 23/32 | 4.10 |
| q = 0.50 | fixed n | −0.2216 | 0.7544 → 0.7085 | −0.0459 | 15/48 | −3.55 |
| q = 0.50 | fixed n/k | +0.0981 | 0.6404 → 0.7689 | +0.1285 | 19/32 | 1.93 |
| q = 0.00 | fixed n | −0.3011 | 0.9752 → 0.9075 | −0.0677 | 13/48 | −4.16 |
| q = 0.00 | fixed n/k | +0.0018 | 0.8489 → 0.8998 | +0.0509 | 16/32 | −0.16 |

1. **The slope survives at q = 1.00, at about a third of its published size.** Pinning n/k
   removes **68.1%** of the span (+0.2333 → +0.0745) and 55% of ρ. The residue is not noise —
   23 of 32 independent (ratio, draw) k-series are positive, t 4.10 — so *pool depth is real
   and small*. Partials on the published arm say the same: ρ(k, OOS S) +0.5269 falls to
   **+0.4339** controlling for fill and **+0.2553** controlling for the ratio.
2. **Its sign is a cap-mix fact.** The same published construction gives **−0.2216** at
   q = 0.50 and **−0.3011** at q = 0.00. Idea 685's "wide end loses" and idea 688's "width is
   good" are *the same measurement on different cap mixes*, exactly as the queue suspected.
3. **Cap mix dwarfs width.** On the k ≤ 100 block where all three q levels exist,
   ρ(q, OOS Sharpe | k) = **−0.7627** against ρ(k, OOS Sharpe | q) = **+0.0370** — a factor of
   **20.6**. Levels (fixed-ratio grid): OOS Sharpe **0.8782 / 0.6899 / 0.3385** and OOS CAGR
   **13.33% / 9.49% / 4.50%** at q = 0.00 / 0.50 / 1.00, MaxDD −23.2% / −25.2% / −32.0%.
4. **The selection ratio is the dial that actually pays, and it changes sign with cap mix.**
   ρ(ratio, OOS S | k) = **+0.72 / +0.80** (q = 0.00), **+0.38 / +0.68** (q = 0.50),
   **−0.37 / −0.50** (q = 1.00) on the fixed-n / fixed-ratio grids. Concentrate in small caps,
   spread in large caps — and note this is the axis the record's width ladders vary *by
   accident*.
5. **EWall, the record's own naturally fixed-ratio book, agrees**: ρ(k, OOS S) **+0.1920**
   (q = 1.00), −0.0674 (q = 0.50), −0.2582 (q = 0.00).

## Rule 8 (PROTOCOL 8) and the KEEP paths

Dial chosen on 2009–2016 IS Sharpe inside one draw's own choice set, 2017– read once; six
selectors including idea 688's width-pinner and a seeded RANDOM control; 288 picks.

**The width-pinner's gain is the confound, and it reverses when the ratio is pinned.** K-MAX's
edge over the do-nothing anchor at q = 1.00 is **+0.1613** on the published fixed-n grid
(reproducing idea 688's "width-pinning gains") and **−0.1119** on the fixed-ratio grid. At
q = 0.00 it is +0.0091 / +0.0123, i.e. nothing. Pooled, the picks reach OOS CAGR **9.11%**
against **SPY's 15.45%**, OOS Sharpe 0.6995 (fixn) / 0.6551 (ratio) against SPY 0.8820 and
RULES v2 0.8673 on the same panels; they beat SPY OOS Sharpe in **29%** of picks and RULES v2
in **10%**. RANDOM beats the anchor as often as K-MAX does on the fixed-ratio grid.

**KEEP paths, every book row: 4a 0 of 1,130.** 4b **77 of 1,130**, and the footprint is the
cap-mix result restated: **q = 0.00 67, q = 0.50 10, q = 1.00 0 of 480**, monotone in width
(32/240 at k = 40 → **0/80 at k = 400**). Every passer is the record's committed CAND-n /
EWall book on a *random sub-panel of BSTK100*, i.e. a statement about the draw, not a rule
anyone can trade; none passes 4a; the rule-8 picks that pass 4b (N-MAX 8/24, RATIO-MAX 9/24)
lose to RULES v2 OOS in ~90% of cases. **No new KEEP-candidate, no memo** — consistent with
ideas 685/688's convention that a pass on a drawn panel is not a capital candidate.

**SURVIVORSHIP.** SMALL439 and BSTK100 are current constituents of their screens, so every
CAGR level is optimistic; the q axis is precisely the axis survivorship contaminates most,
which means result (3) is an upper bound on how *badly* the small pool does, not a floor.

**What this licenses for the record (recorded, not applied):** any published k-ladder claim
should state its **n/k and its realised fill beside k**, since at fixed n those two move 10×
and 2.3× respectively across the record's own width range, and a width claim that quotes
neither is not decidable. Follow-ups proposed in QUEUE.
