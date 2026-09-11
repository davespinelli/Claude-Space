# Idea 731 — is the 4a DRAWDOWN leg reachable at all on a POST-2020 corpus?

**ANSWERED / KILL of 4a as a reachable bar at the live comparand. No KEEP, no memo, no
RULES / PROTOCOL / scan / bot / baseline edit.**

Script `2026-09-11_is-the-4a-DRAWDOWN-LEG-reachable-at-all-on-a-POST-2020-corpus_cloud.py`;
tables `.grid.csv` (60 rows), `.walkforward.csv` (12), `.floors.csv` (8), console `.console.txt`.

## Gates (pre-registered, printed before any corpus number was read)
| gate | result |
|---|---|
| G1 `fast_backtest` == `engine.backtest`, read window (index[260]+), EWALL/W | **5.204e-18** (engine carries 2 NaN rows before its first rebalance, last at position 3 — outside the read window; `fast_backtest` carries 0.0 there) |
| G2 same, ranked book / monthly cadence | **1.041e-17** (2 NaN rows, last at position 21) |
| G3 `EWALL(g=0.75)` == `baseline.rules_v2_weights` | **0.000e+00** |
| G4 SPY OOS 2017+ CAGR / Sharpe / MaxDD | 15.24% / 0.8721 / −33.72% |

G1/G2 are **not** the 0.000e+00 the record usually quotes: the two implementations differ at
float rounding (5e-18 on a daily return of order 1e-2, i.e. ~1e-16 relative). Reported as
measured rather than rounded to zero.

## Design
162 price-only books = 3 panels × 54. Families `CAND n` (top-n by the `baseline.score`
composite inside the 200d ±3% band), `IVOL n` (n lowest 20d-vol names inside the same band),
`EWALL` (every in-band name, == RULES v2); n ∈ {10,20,30,40}, gross ∈ {0.50,0.75,1.00},
cadence ∈ {W,M}. All books **de-gross** (gated-out weight → cash), matching v2. 10 bps,
weights decided at t applied at t+1.

**Comparand ladder (the x-axis, not a tuned parameter):** RULES v2 at gross
0.10/0.25/0.40/0.50/0.60/0.75/0.90/1.00, weekly, same panel and calendar. De-grossing moves
the comparand's **MaxDD** (−1.6% → −17.1%) while leaving its **Sharpe flat** (U56 1.1996 →
1.1996; B136 1.1054 → 1.1057; SMALL 0.5724 → 0.5724). RULES v1 and SPY carried off-ladder.

**Two tuned parameters, every grid point published:** P1 window ∈ {FULL, POST2020},
P2 panel ∈ {U56, B136, SMALL439}.

## The answer — two parts, and the queue's premise is half right

**(1) The DD leg is what makes the 4a rate MOVE with the comparand; it is the whole of the
ladder's variation.** Pooled over the three panels, FULL window:

| comparand gross | comparand MaxDD | Sharpe leg | DD leg | 4a |
|---|---|---|---|---|
| 0.10 | −1.80% | 6/162 | **0/162** | 0/162 |
| 0.25 | −4.45% | 6/162 | **0/162** | 0/162 |
| 0.40 | −7.06% | 6/162 | 1/162 | 0/162 |
| 0.50 | −8.78% | 6/162 | 4/162 | 0/162 |
| 0.60 | −10.48% | 6/162 | 16/162 | 1/162 |
| **0.75 (live)** | **−12.99%** | **6/162** | **30/162** | **2/162** |
| 0.90 | −15.46% | 6/162 | 51/162 | 3/162 |
| 1.00 | −17.09% | 6/162 | 64/162 | 4/162 |

The Sharpe leg is **constant at 6/162 across all eight rungs**; the DD leg runs 0 → 64.
corr(comparand MaxDD, 4a rate) = **−0.7077** (FULL), −0.4241 (POST2020).

**(2) But at the LIVE gross the DD leg is NOT the binding leg — the Sharpe-in-both-halves leg
is, by 5×.** Pooled at `v2@g0.75`: Sharpe leg **6/162 (3.7%)**, DD leg **30/162 (18.5%)**,
joint 4a **2/162 (1.23%)**. The queue filed this idea as a drawdown question; the drawdown leg
is five times looser than the leg beside it. Both readings are published.

**(3) On the POST2020 window 4a is unreachable outright.** Pooled `v2@g0.75`: **0/162**, and
the Sharpe leg is **0/162** at every ladder rung up to 0.75 — RULES v2's post-2020 Sharpe
(1.2830 U56 / 1.0488 B136 / 0.6951 SMALL) is not beaten in both halves by any book in the
corpus. Per-panel feasibility floors `m* = ceil(ln 0.05 / ln(1 − p̄))` at the live gross:

| window | panel | k/m | p̄ | FEAS floor |
|---|---|---|---|---|
| FULL | U56 | 1/54 | 0.0185 | 161 |
| FULL | B136 | 0/54 | 0.0000 | **INFINITE** |
| FULL | SMALL439 | 1/54 | 0.0185 | 161 |
| FULL | POOLED | 2/162 | 0.0123 | **242** |
| POST2020 | U56 / B136 / SMALL439 / POOLED | 0/54, 0/54, 0/54, 0/162 | 0.0000 | **INFINITE** ×4 |

**(4) It is the COMPARAND SWAP, not the books, that killed 4a.** The identical 162 books read
against **RULES v1** pass 4a at **74/162 (45.7%)** on FULL and **74/162** on POST2020 — a 37×
higher rate against a comparand whose MaxDD is only 1.8× deeper (−23.71% vs −12.99%) but whose
Sharpe is half (U56 0.6554 vs 1.1998). RULES v2 going live on 2026-09-06 raised the comparand's
Sharpe **and** cut its drawdown at the same time, tightening both legs at once. 4a is not
measuring the candidate books any more; it is measuring the live book's own quality.

## Rule 8 walk-forward (required; 4 IS-only selectors × 3 panels, each pick read ONCE on 2017+)
Selectors read 2009–2016 only (SMALL: 2010–2016): S1 max IS Sharpe, S2 max IS Sharpe among
IS-4a passers, S3 min IS MaxDD, S4 max IS Calmar.

| panel | selector | pick | OOS CAGR | OOS Sharpe | OOS MaxDD | v2 OOS Sharpe | SPY OOS Sharpe |
|---|---|---|---|---|---|---|---|
| U56 | S1 | CAND40\|g1.00\|M | 16.77% | 1.2226 | −24.37% | 1.2747 | 0.8721 |
| U56 | S2 | CAND40\|g0.50\|M | 8.26% | 1.2211 | −12.81% | 1.2747 | 0.8721 |
| U56 | S3 | IVOL10\|g0.50\|M | 3.51% | 0.8738 | −6.09% | 1.2747 | 0.8721 |
| U56 | S4 | CAND30\|g1.00\|M | 18.05% | 1.1913 | −25.99% | 1.2747 | 0.8721 |
| B136 | S1/S2 | IVOL20\|g1.00\|M | 7.57% | 0.7261 | −20.03% | 1.1185 | 0.8820 |
| B136 | S3 | IVOL20\|g0.50\|W | 3.74% | 0.7265 | −8.91% | 1.1185 | 0.8820 |
| B136 | S4 | IVOL30\|g1.00\|M | 9.51% | 0.8304 | −23.98% | 1.1185 | 0.8820 |
| SMALL439 | S1/S4 | IVOL10\|g1.00\|M | 4.22% | 0.3379 | −40.47% | 0.5680 | 0.8820 |
| SMALL439 | S2 | IVOL10\|g0.50\|M | 2.47% | 0.3503 | −21.13% | 0.5680 | 0.8820 |
| SMALL439 | S3 | **EWALL\|g0.50\|M** | 2.95% | **0.6191** | −11.40% | 0.5680 | 0.8820 |

SPY OOS: 15.24% CAGR / 0.8721 Sharpe / −33.72% MaxDD (U56 calendar), 15.45% / 0.8820 / −33.72%
(B136 / SMALL calendar).

**OOS 4a 1/12, OOS 4b 0/12; beats RULES v2 OOS Sharpe 1/12; beats SPY OOS Sharpe 4/12.** The
single OOS-4a pass (`SMALL439 / S3 / EWALL|g0.50|M`, 0.6191 vs v2 0.5680) is the *lowest-gross*
book on the panel where v2 itself is weakest, and it fails 4b on both remaining legs — OOS
Sharpe 0.6191 < SPY 0.8820 and OOS CAGR 2.95% = 19% of SPY's, against the 70% floor. **One
selector of twelve landing on a 4a pass, on the panel with the worst comparand, is not a
signal.**

## Both KEEP paths
- **4a:** 2/162 FULL, **0/162 POST2020** at the live comparand. No KEEP.
- **4b (record reading, in-sample legs only):** 13/162 FULL, 12/162 POST2020 — and the OOS leg
  that rule 8 requires is **0/12**. No KEEP.

## Caveats
- **Survivorship (idea 54):** all three panels are current-constituent lists. A
  delisting-complete corpus would have *lower* book pass rates and therefore *higher* floors —
  the bias runs against 4a's reachability, not for it. SMALL439 is the sub-$2B screen with the
  44 tickers carrying `max_1d_move >= 1.0` dropped first (440 columns incl. the SPY benchmark
  column, which is a benchmark and not a constituent).
- POST2020 halves are halves of the post-2020 window (≈2020-01→2023-05 / 2023-05→2026-09), so
  its Sharpe-leg collapse is partly a 3.5-year half-length effect, not only a regime effect.
- 162 books is one corpus; the rate levels carry the usual family-composition dependence. The
  *flatness* of the Sharpe leg across the gross ladder is the structural result and does not.

## Proposed (NOT applied — rule 6, Sunday review only)
PROTOCOL rule 4a currently reads "MaxDD no worse than the live rules". Two clauses are worth
considering at review, and neither is applied here: (i) quote the **two legs separately** beside
every 4a verdict, since at the live gross they differ 5× and a joint 0/162 says nothing about
which one bound; (ii) since 4a's rate is a function of the comparand and the comparand now
changes when RULES changes, state the comparand's **own MaxDD and Sharpe** in the row, so a
falling 4a rate can be read as a comparand improvement rather than a corpus failure.
