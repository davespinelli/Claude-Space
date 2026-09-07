# Idea 318 — does-WIDENING-into-narrow-markets-beat-the-broad-leg (cloud, 2026-09-07)

**KILL. The U56 edge is a grid artefact — and worse, it is not a widening effect at all.**

Idea 316 reported DILUTE (narrow → `min(2*n0, E_t)` names at constant 75% gross) beating the
clause-free NF20 on U56 at 1.073/-18.0% vs 1.070/-18.3%, on one unswept control point. This run
swept `q ∈ {0.10,0.20,0.30,0.40} × m ∈ {1.5,2,3,5}` = 16 points on each of U56 / B136 / SMALL439
(48 points, all reported), against three references: NF20 (never widen), DIL-ALW *m* (widen every
day — the second unconditional parent), and EWALL. Gross is 0.75 in both regimes by construction,
so `d = r(DILUTE) − r(NF20)` is width and nothing else.

## 1. The narrow-day effect is negative on 48 of 48 points

`ann_eff_on_narrow_pp` (annualised d over armed days only) is **> 0 in 0/48**: mean **−0.56 pp/yr on
U56, −2.47 on B136, −5.17 on SMALL439** (ex-2022 −0.13 / −2.98 / −5.94, positive in 9/48). Whatever
the U56 book gain was, it did **not** come from the narrow days — widening into narrow markets loses
money on every panel at every setting. This is the exact mirror of idea 316's concentration census
(which found the concentration effect +5.17 on U56 and negative on the other two): both signs of the
same clause lose on the two nominated panels, so the flag is not pricing width in either direction.

## 2. Where the +0.003 came from, and why it does not move in *m*

On U56 the four *m* values give **bit-identical books at q=0.10 and q=0.20** and identical from m=2
upward at q=0.30/0.40. The reason is mechanical: `k_narrow = min(round(m*20), E_t)` and the narrow
regime is *defined* as the days when E_t is small (mean E on narrow days: 11.2 at q=0.10, 17.1 at
q=0.20 vs 39-41 off-narrow). The broad leg `min(20, E_t)` is already holding **every eligible name**
on those days, so there is nothing to widen into. At q=0.10 the clause is a literal no-op — d ≡ 0.000
on all 283 armed days, and all four "4b passes" there are NF20 with a different label. The whole U56
result is the q=0.20 column: **−0.054 pp/yr of book return bought +0.314 pp of drawdown**, +0.003 of
Sharpe, from a single drawdown path (dMaxDD is +0.314 pp identically at q=0.20/0.30/0.40 — one
episode). That is a rounding artefact, not an edge.

## 3. The parents test (idea 317's bar) fails 40/48

The conditional clause beats **both** NF20 and DIL-ALW(m) in **8/48 full-sample and 9/48 OOS** — all
eight on U56, none on B136 (0/16) or SMALL439 (0/16). It loses to always-widening in 26/48. The
conditional flag is not adding information to "hold more names".

## 4. Rule 8 walk-forward: the chooser never beats the do-nothing control

(q,m) picked on ≤2016 IS Sharpe, 2017– read once. Both choosers (IS-Sharpe and 4b-aware) pick the
same point on all three panels.

| panel | pick | OOS CAGR / Sharpe / MaxDD | NF20 control OOS | SPY OOS | RULES v2 OOS |
|---|---|---|---|---|---|
| U56 | DILUTE q0.20 m1.5 | 14.4% / **1.142** / −18.0% (4b PASS) | 14.5% / 1.137 / −18.3% (4b PASS) | 15.5% / 0.882 / −33.7% | 9.5% / 1.285 / −12.1% |
| B136 | DILUTE q0.10 m1.5 | 12.1% / **0.866** / −20.2% (4b FAIL H2,OOS) | 12.4% / 0.883 / −20.1% (4b FAIL H2) | 15.5% / 0.882 / −33.7% | 8.0% / 1.119 / −12.2% |
| SMALL439 | DILUTE q0.40 m3.0 | 6.3% / **0.447** / −32.8% (4b FAIL, all five) | 6.9% / 0.464 / −33.5% | 15.5% / 0.882 / −33.7% | 3.8% / 0.568 / −14.7% |

The chooser **loses OOS CAGR on 3/3 panels** and loses OOS Sharpe on 2/3; on U56 it wins by +0.005
of Sharpe for −0.1 pp of CAGR, i.e. the same non-result as the full sample. 4a: **0/78 rows**.

## 5. Full-sample headline at idea 316's own point (q=0.20, m=2.0)

| panel | DILUTE | NF20 (clause deleted) | SPY |
|---|---|---|---|
| U56 | 12.78% / 1.073 / −18.0% (H1 1.077 / H2 1.076), 4b PASS | 12.83% / 1.070 / −18.3% (1.076/1.072), 4b PASS | 15.2% / 0.889 / −33.7% |
| B136 | 12.8% / 0.945 / −19.8% (1.093/0.813), 4b FAIL H2 | 13.0% / 0.943 / −20.1% (1.105/0.802), 4b FAIL H2 | 15.2% / 0.889 / −33.7% |
| SMALL439 | 5.1% / 0.380 / −34.1% (0.537/0.255), 4b FAIL ×5 | 6.4% / 0.449 / −33.5% (0.606/0.324), 4b FAIL ×5 | 14.1% / 0.862 / −33.7% |

Replicates idea 316's numbers exactly. **16/48 DILUTE points pass 4b; all 16 are U56 and every one
either is bit-identical to its NF20 parent (the eight q≤0.20 cells) or has LOWER CAGR than it.**
Nothing here is capital-worthy that NF20 was not already.

## 6. The live by-product (not proposed, queued as idea 320)

The **unconditional** wider book clears 4b on B136 where NF20 does not: DIL-ALW m2.0 / m3.0 / m5.0 →
OOS 0.971 / 1.003 / 1.030 vs NF20's 0.883, all 4b PASS, and EWALL (k = E_t) OOS 1.019 PASS. On U56
the same dial is flat-to-down (1.155 / 1.134 / 1.114 vs 1.137) and on SMALL439 it is monotonically
worse (0.454 → 0.361 vs 0.464). That is the n-dial, already the record's most-tested knob, with the
familiar panel ordering — it is not this idea's finding and is not being proposed off this run.

**Survivorship:** universe.json (56) and universe_broad.json (136) are current-constituent lists;
SMALL439 is the current constituents of a sub-$2B screen with the README's `max_1d_move ≥ 1.0`
names dropped (1 of 440). Absolute CAGRs are optimistic on all three panels; the DILUTE-vs-NF20
contrast, which is what the idea asks about, is a within-panel difference and is the durable part.

**Rules unchanged. No KEEP.** Script: `2026-09-07_does-WIDENING-into-narrow-markets-beat-the-broad-leg_cloud.py`
