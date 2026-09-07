# Idea 355 — why does the grid ORDERING invert on B136 at 0 bps only?

**Verdict: ANSWERED. The queue's premise is half right and half wrong, and the wrong half is
the expensive one.** Script: `2026-09-07_why-does-the-grid-ORDERING-invert-on-B136-at-0-bps-only_cloud.py`
(2 tuned params: n ∈ {3,5,10,20}, g ∈ {0.75,0.85,1.00}; all 12 points × 5 arms × 2 panels ×
3 rungs = 360 reported, plus RULES v1/v2/SPY controls).

## Gates
- **G0** — the 3-term identity `S(c) = (G − c·T)/V(c)` reproduces `engine.backtest(cost_bps=c)`
  to **2.2e-16** over 9 checks. The ordering of the 12 books is therefore a function of exactly
  three numbers per book, each substitutable one at a time.
- **G1a** — every one of the **360 cells shared with idea 39's committed grid CSV** matches to
  ≤2.2e-16 (turnover ≤7.1e-15). This is a bit-for-bit reproduction, not a re-estimate.
- **G1** — idea 39's published rank correlations reproduce exactly: B136 CALENDAR **−0.538** @0 bps
  → **+0.972** @10 bps; SANDBOX **−0.322** → **+0.434**.

## 1. Which term carries the inversion — the substitution test
Replace one term at a time with the corrected tape's value and re-rank (B136, 0 bps):

| arm | ρ | ρ with G corrected | ρ with T corrected | ρ with V corrected |
|---|---|---|---|---|
| CALENDAR | **−0.538** | **+0.972** | −0.538 | −0.699 |
| SANDBOX | **−0.322** | **+0.972** | −0.322 | −0.699 |
| SHRUNK | **+0.056** | **+0.895** | +0.056 | +0.056 |

**The gross-return term G carries all of it.** Substituting G restores ρ to +0.97 in one move;
substituting V makes it *worse*; substituting T is algebraically a no-op at 0 bps — which is the
whole shape of the puzzle. The queue named three candidates (turnover, breadth, vol) and the
answer is none of them: it is the return term.

**Breadth is not the channel either.** Mean eligible count moves 91.5 → 87.9 (B136) and 37.5 → 36.3
(U56) between corrected and calendar, and the eligible set binds the book (E_t < n) on at most
**2.4%** of B136 days. A 4% breadth shift cannot re-order a top-20 book that is never breadth-constrained.

## 2. The mechanism: lookback compression, not the tape
`SHRUNK` is the **corrected** tape with every `score()` window multiplied by 252/365 — the number
of trading days a calendar-day window actually spans. No index change, no truncation, no cost change.
It collapses ρ on B136 from **1.000 → 0.056** at 0 bps, with ρ_sub_G = +0.895. The calendar index
did not corrupt prices; it silently ran a 200d MA over 138 trading days, a 252d momentum leg over 174,
and a 20d vol window over 14. The n-ordering by gross return follows:

| arm (B136, g=0.75, 0 bps) | G at n=3 / 5 / 10 / 20 | Sharpe order |
|---|---|---|
| CORRECTED | 0.0997 / 0.0968 / 0.0935 / **0.1058** | 20 > 10 > 5 > 3 |
| TRUNC (start only) | 0.0892 / 0.0893 / 0.0885 / **0.0983** | 20 > 10 > 5 > 3 |
| CALENDAR | 0.0723 / 0.0673 / 0.0613 / 0.0656 | 5 > 3 > 20 > 10 |
| SANDBOX | 0.0740 / 0.0668 / 0.0580 / 0.0645 | 3 > 20 > 5 > 10 |
| SHRUNK | 0.1161 / 0.1018 / 0.1071 / 0.1032 | 10 > 3 > 20 > 5 |

Truncating the start (TRUNC) preserves the ordering at every rung on both panels (ρ ≥ 0.965). Only the
index does damage, and only through the windows it shortens.

## 3. Why 0 bps only, and why B136 only — a signal-to-perturbation ratio
The tape perturbation is the **same size on both panels**: mean |ΔSharpe| = 0.180 (B136) vs 0.184 (U56).
What differs is the spread the ordering has to work with:

| panel | rung | cross-book sd of Sharpe | between-n range | within-n range (the g dial) | cost share of the key | ρ vs CALENDAR | R² |
|---|---|---|---|---|---|---|---|
| B136 | 0 | 0.047 | 0.116 | 0.0005 | 0.000 | **−0.538** | **0.022** |
| B136 | 10 | 0.097 | 0.247 | 0.0004 | 0.544 | +0.972 | 0.981 |
| B136 | 25 | 0.174 | 0.442 | 0.0003 | 0.948 | +0.951 | 1.000 |
| U56 | 0 | 0.095 | 0.189 | 0.0008 | 0.000 | +1.000 | 0.916 |
| U56 | 10 | 0.154 | 0.340 | 0.0007 | 0.374 | +0.993 | 0.961 |

Two facts do the work. (a) **g is not a dial at all**: within one n the three gross levels differ by
0.0003–0.0008 of Sharpe, so 12 grid points are really 4 books plus 8 near-ties resolved at the 4th
decimal. (b) At 10 bps the **cost drag supplies 54% (B136) / 37% (U56) of the cross-book spread** of the
ordering key, and turnover is monotone in n and tape-stable (T falls ~17% uniformly). Switch costs off and
that stabiliser is gone; what remains on B136 is a 0.116 between-n spread against a 0.180 perturbation.
Mean |rank change| is **6.00 at 0 bps and 0.33 at 10 bps**. On U56 the same perturbation meets a 0.189
spread and moves **0.00** ranks.

## 4. The correction the record needs — this is NOT "no economic content"
The queue's reading ("decided by something with no economic content") is right about the *g* triplets and
wrong about the *n* dial. The inversion is a real, signed, reproducible chooser error. Rule 8, (n,g) chosen
on IS ≤2016 on each chooser tape, **scored on the corrected tape** either way:

| panel | rung | corrected pick → OOS | calendar pick → OOS | sandbox pick → OOS |
|---|---|---|---|---|
| B136 | 0 | TOP20_g1.00 → **0.907** | TOP3_g1.00 → 0.767 (**−0.140**, −1.37pp CAGR) | TOP3_g1.00 → 0.767 (−0.140) |
| B136 | 10 | TOP20_g1.00 → **0.735** | TOP20_g1.00 → 0.735 (0.000) | TOP3_g1.00 → 0.465 (**−0.270**, −3.77pp) |
| B136 | 25 | TOP20_g1.00 → **0.476** | TOP20_g1.00 → 0.476 (0.000) | TOP3_g1.00 → 0.014 (**−0.462**, −7.06pp) |
| U56 | 0 | TOP10_g1.00 → 1.058 | TOP20_g1.00 → 1.104 (+0.046) | TOP20_g0.75 → 1.104 (+0.047) |
| U56 | 10/25 | TOP20_g1.00 | identical | identical |

So the broken tape's ordering is not harmless noise — it costs **−0.14 to −0.46 of OOS Sharpe** and up to
**−7.1pp of OOS CAGR** on B136 whenever cost is not there to mask it. It happens to be harmless at exactly
PROTOCOL's own 10 bps rung on the CALENDAR arm, and *not* on the SANDBOX arm (the actual pre-fix cache),
which is wrong at all three rungs. Idea 39's "verdicts survive at 10 bps" is a rung coincidence, not a
property of the cache.

## 5. KEEP paths (corrected tape, 78 cells)
**4a 0/78. 4b 7/78** — all U56, all reproductions of idea 39's committed cells, none new:
5 at 0 bps (TOP10 ×3, TOP20 g0.75/g0.85) and 2 at 10 bps (TOP10_g1.00 11.96%/0.906/−17.9%/H 0.980/0.847/
OOS 0.897; TOP20_g0.85 11.44%/0.969/−19.6%/H 1.038/0.916/OOS 0.992) against SPY 15.23%/0.889/−33.72%,
halves 0.957/0.834, OOS 0.882, and RULES v2 U56 8.66%/1.206/−12.05% (H 1.226/1.191, OOS 1.285).
**B136 0/39.** First failing 4b bar over the 71 failures: H1 50, H2 16, CAGR 3, DD 2.
The family is not walk-forward-KEEPable: the rule-8 chooser at 10 bps on U56 lands on **TOP20_g1.00**,
whose −22.8% MaxDD **fails** the 20.23% DD cap; the two 4b passers are not what IS Sharpe selects.

## 6. What the record should carry
1. `rho_sub_G / rho_sub_T / rho_sub_V` is a cheap three-line attribution for any published ordering
   disagreement, and it is exact (gate G0), not a regression.
2. **Report the cost share of the ordering key beside any published argmax.** An argmax whose key is
   ≥50% cost drag is ordering turnover, not returns; at 0 bps that ordering has no stabiliser.
3. **A gross dial `g` applied multiplicatively to a fully-invested book is not a dial for Sharpe**
   (within-n range 0.0003–0.0008 here). Grids that sweep it inflate their point count 3× and pollute
   every rank statistic with near-ties. This is idea 311's "dial placement, not an edge" in rank form.
4. Any cached tape must be checked for **window compression**, not just for weekend rows — the SHRUNK
   arm shows the damage is fully reproducible on a correct index by shortening lookbacks alone.

**Survivorship:** none of the three panels used here is point-in-time; U56/B136 are current constituents
of `research/universe.json` / `universe_broad.json`. No small-cap panel was used.
