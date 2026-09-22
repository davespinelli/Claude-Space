# Idea 1775 (lane C, 2026-09-22) — does the NAME-SET CHOOSER LIFT replicate on B136 and SMALL, or is it a U56 fact?

**VERDICT: ANSWERED, answer (c) — the LIFT replicates on a second panel, the REACHED BOOK does not,
and the whole object is an N=20 fact. KILL for a rules change; no new KEEP candidate.**

Script: `research/backtests/2026-09-22_name-set-chooser-lift-replication_C.py` (89.6 s, offline,
deterministic, **9/9 gates**). 1749's construction unchanged: band c=0.03, gross 0.75, weekly,
t+1, 10 bps binding, seed stream `default_rng(16320000 + 1009*N + d)`, decile = ceil(D/10), the
same four IS-only statistics, IS ≤ 2016-12-31 / OOS ≥ 2017-01-01. Two tuned dials and no more:
**PANEL** {U56, B136, SMALL665} × **N** {20, 40}. Reported, not tuned: D ∈ {24, 96, 240, 480}
(nested) and cost ∈ {0, 10, 25, 50} bps. 11,520 cells published.

## 1. The replication of 1749 (U56, N=20) — holds, with one draw lost to a cache refresh

| | 1749 (2026-09-20) | this run (2026-09-22) |
|---|---|---|
| 4b BOTH base rate | 43/480 = 8.96% | **42/480 = 8.75%** |
| top decile (IS_CAGRSLACK / IS_MINMARG) | 25/48 = 52.08% | **25/48 = 52.08%** |
| lift, exact hypergeometric p | +43.1 pp, p < 1e-4 | **+43.33 pp, p = 9.09e-18** |
| statistics with p < 0.05 | — | **4 of 4** |

The single draw that fell out is **1632's own draw 3**, which now misses the FULL 4b CAGR floor by
**−3.28e-06** (0.0003 pp of CAGR). Between the two runs the committed `data/prices.csv` was
refreshed and SPY's FULL CAGR moved 15.12% → 15.1388% (OOS 15.26% → 15.2870%), lifting both CAGR
floors. **A verdict the record has carried for three runs is quoted at a precision finer than a
two-day price-cache refresh.** G3a confirms draws 3 and 18 still reproduce 1632's published cells
to max |d| = 2.745e-04 (1632 quotes 4 dp), so this is a bar move, not a construction difference.

## 2. The lift is NOT a 56-name artefact — but it decays hard, and dies at N=40

4b BOTH (FULL *and* OOS), D = 480, 10 bps, best statistic per cell:

| panel | pool | N | base rate | top decile | lift | p | stats p<0.05 |
|---|---|---|---|---|---|---|---|
| U56 | 56 | 20 | 42/480 = 8.75% | 25/48 = 52.08% | **+43.33 pp** | 9.1e-18 | 4/4 |
| U56 | 56 | 40 | **0/480 = 0.00%** | 0/48 | — | 1.0000 | 0/4 |
| B136 | 136 | 20 | 12/480 = 2.50% | 10/48 = 20.83% | **+18.33 pp** | 2.3e-09 | 3/4 |
| B136 | 136 | 40 | **0/480 = 0.00%** | 0/48 | — | 1.0000 | 0/4 |
| SMALL665 | 665 | 20 | **0/480 = 0.00%** | 0/48 | — | 1.0000 | 0/4 |
| SMALL665 | 665 | 40 | **0/480 = 0.00%** | 0/48 | — | 1.0000 | 0/4 |

* **B136 at N=20 replicates the lift** at p = 2.3e-09 with the same argmax statistic
  (IS_CAGRSLACK), so the chooser is carrying name-set information on a 136-name pool too. 1749's
  headline is **not** a 56-column artefact.
* The base rate collapses 3.5× from U56 to B136 (8.75% → 2.50%) and the reachable top-decile rate
  2.5× (52.08% → 20.83%), so what replicates is the *sign and significance*, not the magnitude.
* **At N=40 the 4b-BOTH target is empty on all three panels** (0/480 at 10 bps; 1/480 on B136 at
  0 bps only). The object exists at exactly **one of six (panel, N) cells** with a non-trivial
  count, and at 4 of 6 the question is unanswerable for want of a single passing draw.
* On the easier 4b-OOS-only target the lift survives at 4 of 6 cells (U56 N=40 +9.17 pp p=0.0097;
  B136 N=40 +3.75 pp p=0.0098), so N=40 is not a *statistical* death — it is a **bar** death: the
  4b FULL legs are what empties.

## 3. SMALL665 — the chooser's information does not merely vanish, it reverses sign

SMALL665 carries **0 of 480** 4b passes at either N, on 4b OOS as well as 4b BOTH, so no lift is
measurable in either direction. The reason is a level gap, not noise: the full-pool small-cap band
book runs FULL 4.26% / 0.6588 / −14.16% and OOS 3.63% / 0.5447 against a 4b OOS CAGR floor of
0.70 × 15.29% = **10.70%**. Independently of the empty target, the *continuous* rank correlation
between the IS statistic and the OOS 4b margin — the mechanism the lift rides on — is
**NEGATIVE on SMALL665 at all 8 (N, statistic) pairs** (ρ(S, OOS CAGR margin) −0.047 … −0.116)
against **+0.19 … +0.59 on U56 and B136**. On the small panel the chooser is slightly
*anti*-informative.

## 4. Rule 8 (2009–2016 chooses, 2017–2026 read ONCE) — the reached book is confined to U56

| panel | N | 4b BOTH | 4b OOS | 4b FULL | 4a FULL | 4a OOS | n |
|---|---|---|---|---|---|---|---|
| U56 | 20 | **13** | 13 | 13 | 2 | 2 | 16 |
| U56 | 40 | 0 | 2 | 0 | 1 | 1 | 16 |
| B136 | 20 | 0 | 0 | 2 | 0 | 0 | 16 |
| B136 | 40 | 0 | 3 | 0 | 0 | 0 | 16 |
| SMALL665 | 20/40 | 0 | 0 | 0 | 0 | 0 | 32 |

**13 of 13 rule-8 picks that clear 4b FULL and OOS are U56 N=20 cells; 0 of 80 elsewhere.** They
are reproductions of 1749's already-standing candidate, not a new one — the D=240/480 argmax on
IS_CAGRSLACK/IS_MINMARG is **draw 166** again: FULL 11.75% / 1.3343 / −13.16%, halves
1.4722/1.2104, OOS 11.74% / 1.3112 / −13.16%, against SPY OOS 15.29% / 0.8751 / −33.72% and live
RULES v2 OOS 9.46% / 1.2767 / −12.05%.

On B136 the chooser moves toward the right region and lands short: at D=480 IS_CAGRSLACK /
IS_MINMARG pick **draw 297**, which clears **4b FULL** (11.14% / 1.2664 / −10.96%) and fails 4b
OOS on the **CAGR floor** (OOS 9.64% vs the 10.70% floor, −1.06 pp).

Binding leg across all 96 picks: **O5_CAGR 78**, O3_OOS 32, O4_DD 16 — the 4b CAGR floor again,
drawdown least of all. **4a is reached at 3 of 96** picks (U56 N=20 draw 76 at D=96/240: FULL
10.23% / 1.3264 / −11.75%, halves 1.4792/1.1962, OOS 10.28% / 1.2846 — it clears 4a FULL and OOS
and **fails 4b** on the CAGR floor; U56 N=40 draw 68 similarly).

## 5. Dual-path cells exist off U56 — and no legal chooser reaches any of them

**5 of 2,880 draws clear 4a FULL *and* 4b FULL *and* 4b OOS** at 10 bps: U56 N=20 draws 187, 238,
250, 384 and — the first such cell off U56 in the record — **B136 N=20 draw 261** (FULL 11.40% /
1.3406 / −11.98%, halves 1.3720/1.3128; OOS 11.29% / 1.3224 / −11.98%; 4a OOS also True).
**0 of 96 rule-8 picks reach any of the five.** They are hindsight and are recorded as such.

## 6. Cost ladder (reported, not tuned) — 4b BOTH counts per cell over 480 draws

| panel | N | 0 bps | 10 bps | 25 bps | 50 bps |
|---|---|---|---|---|---|
| U56 | 20 | 55 | 42 | 28 | 13 |
| B136 | 20 | 14 | 12 | 7 | 2 |
| U56/B136 | 40 | 0 / 1 | 0 | 0 | 0 |
| SMALL665 | 20/40 | 0 | 0 | 0 | 0 |

## 7. Gates — 9/9

G1 runner == `engine.backtest` on returns AND turnover, all three panels (worst |d| 1.80e-16);
G2 cost identity (6.59e-17); G3a 1632's draws 3/18 reproduce (2.745e-04); G3b 1749's counts, 42 vs
43 with the single moved draw's binding margin 3.28e-06 (< 1e-4, the pre-stated tolerance for a
refreshed cache) and the top-decile count 25/48 exact; G4 no statistic reads a row ≥ 2017-01-01;
G5 exactly two tuned dials; G6 11,520 of 11,520 cells published; G7 seed stream unchanged from
1632/1749; G8 max realised target gross 0.750000; G9 SMALL's 4,203 trading days are a subset of
U56's, so the live RULES v2 4a anchor is read on each panel's own calendar without interpolation.

## 8. What the record should now say

1749's wording — "the NAME SET is a REACHABLE axis" — must be **narrowed twice**: the *lift* is
real on B136 as well as U56 at N=20 (so it is not a 56-name artefact), but (a) the *reached 4b
book* exists on U56 N=20 only, 13 of 13 versus 0 of 80, and (b) the whole object is an **N=20**
construction — at N=40 the 4b-BOTH population is empty on every panel, so there is nothing for any
chooser to reach. Nothing here is capital-worthy that was not already standing: no new KEEP
candidate, and no memo is written.

**SURVIVORSHIP (rule 9), first-order.** All three panels are CURRENT-constituent lists. The draw
is a 35.7% cut of U56, a 14.7% cut of B136 and a 3.0% cut of SMALL665 at N=20, and that difference
in cut depth is itself a live candidate explanation for the panel dependence found above — it is
reported, not controlled away. The U56 N=20 cells remain the record's most survivorship-exposed
construction and their absolute pass counts are upper bounds.
