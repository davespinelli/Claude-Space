# Idea 164 — is-4b-internally-consistent-at-any-vol (cloud, 2026-09-05)

**ANSWERED — KILL of the mis-pairing hypothesis, with one coefficient narrowed.**
4b's band is **NOT empty**. It is narrow, it is empty on the small panel, and the coefficient
that actually binds is **gamma (the CAGR floor)**, not delta (the DD cap).

Script: `2026-09-05_is-4b-internally-consistent-at-any-vol_cloud.py`
Artifacts: `.console.txt`, `.ladder.csv` (480 rows), `.books.csv` (24), `.coeff.csv` (289),
`.walkforward.csv` (72). Runtime 496 s. 10 bps, weekly, t+1, PROTOCOL rules 2/3/4/8.

## The algebra (written before the data was read)

With `s = Sharpe/Sharpe_SPY`, `v = Vol/Vol_SPY`, `rho = (|MaxDD|/Vol) / (|MaxDD_SPY|/Vol_SPY)`,
and the first-order identity `CAGR ~ Sharpe x Vol`, 4b's two gross-sensitive bars become

```
CAGR floor   s*v   >= gamma        ->   v >= gamma / s
DD cap       rho*v <= delta        ->   v <= delta / rho
ADMISSIBLE VOL BAND   v in [gamma/s, delta/rho],  NON-EMPTY iff  rho/s <= delta/gamma = 0.857143
```

The three Sharpe bars are gross-invariant, so they sit outside the band entirely.
**A book with SPY's Sharpe must be 14.3% less drawdown-prone per unit of vol than SPY, or no
gross level whatever puts it inside 4b.** That inequality is the whole of idea 164.

## Verification of the frame

| check | result |
|---|---|
| [a] idea 156's premise (books at v = 1 fail the DD cap) | **298 of 300** (idea 164 quotes 297) — REPRODUCED |
| [b] does `rho > delta` alone predict that failure? | **100.0%** of the 300 vol-matched books |
| [c] Sharpe flat in g over 0.10–2.00 | median range **0.0057**, max 0.0332 — gross-invariant as assumed |
| [c] vol linear in g | min R² **0.999944** |
| [c] rho drift over the ladder | median **0.128**, max 0.706 — rho is NOT constant, so every verdict below is read off the EXACT ladder, not the algebra |
| analytic test vs exact ladder | agree in **95.8%** of the 24 books |

## The premise's inference is wrong

Idea 156's 300 books fail the DD cap at v = 1 not because the band is empty but because
**v = 1 is above the band's right edge**. Their rho: median **0.801**, 5th pct 0.650, min 0.575
→ their right edge sits at `delta/rho ≈ 0.75`, and **72.3% of them have rho ≤ 0.857, i.e. a
non-empty band.** "Scaled to SPY's vol it fails DD, de-grossed it fails CAGR" is a statement
about the two grosses that were tried, not about the band between them.

## Does any panel produce a book inside it? YES — 7 of 24

Books clearing **all five** 4b bars at a **legal** gross (g ≤ 1.00, rule 2):

| panel | book | s | rho | rho/s | passing gross | Sharpe | H1 / H2 | OOS Sharpe |
|---|---|---|---|---|---|---|---|---|
| u56 | EWBAND3 | 1.284 | 0.802 | 0.624 | 0.80–1.00 | 1.142 | 1.117 / 1.167 | 1.241 |
| u56 | TOP20 | 1.246 | 0.830 | 0.666 | 0.70–0.80 | 1.108 | 1.110 / 1.112 | 1.178 |
| u56 | TOP40 | 1.271 | 0.870 | 0.684 | 0.90–1.00 | 1.130 | 1.083 / 1.175 | 1.268 |
| u56 | EWALL | 1.186 | 0.841 | 0.709 | 0.80–0.90 | 1.054 | 1.073 / 1.041 | 1.118 |
| B136 | EWBAND3 | 1.197 | 0.845 | 0.705 | 0.80–0.90 | 1.065 | 1.165 / 0.971 | 1.074 |
| B136 | TOP40 | 1.130 | 0.841 | 0.745 | 0.70 | 1.004 | 1.133 / 0.888 | 0.981 |
| B136 | EWALL | 1.156 | 0.889 | 0.769 | 0.80 | 1.028 | 1.148 / 0.915 | 1.020 |

SPY: 15.23% / 0.889 / −33.72%, halves 0.957 / 0.834, OOS 0.882.
Band widths are **1–3 ladder points of 0.10 gross** — 4b is satisfiable but tight.
Census by panel: `4b at some legal g` u56 4, B136 3, SMALL **0**;
`gross-bars OK but a SHARPE bar fails` u56 2, B136 3; `BAND EMPTY at any gross` u56 2, B136 2,
**SMALL 8 of 8**.

**The small panel has no book inside 4b at any gross.** Its rho/s runs **1.35 to 3.87**
(EWALL 3.87, TOP5 2.24, best is TOP10 at 1.35) against the 0.857 threshold — the failure is
structural, not a gross choice. Note the direction of the survivorship bias: the panel is
current constituents only, so its true rho is *worse* than measured.

## Which coefficient moves? GAMMA.

Books (of 24) with a non-empty band at legal gross, sweeping one coefficient at 4b's value for
the other:

| delta @ gamma=0.70 | 0.40 | 0.45 | 0.50 | 0.55 | **0.60** | 0.65 | 0.70 | … | 1.15 | 1.20 |
|---|---|---|---|---|---|---|---|---|---|---|
| books | 0 | 1 | 6 | 10 | **12** | 14 | 14 | 14 | 14 | 15 |

| gamma @ delta=0.60 | 0.30 | 0.40 | 0.50 | 0.60 | **0.70** | 0.80 | 0.90 | 1.00 | 1.10 |
|---|---|---|---|---|---|---|---|---|---|
| books | 20 | 15 | 15 | 13 | **12** | 10 | 2 | 0 | 0 |

Books admitted per 0.05 of relaxation: **delta up +0.70, gamma down +1.26** — gamma is 1.8x the
cheaper lever. More decisive than the slope: **delta saturates at 0.65 and never binds again**
(14/24 flat from 0.65 all the way to 1.15), while gamma keeps biting to 1.00 where it admits
nothing at all. At 4b's published pair the DD cap is *marginally* binding (12 → 14 books over
one 0.05 step) and the CAGR floor is the live constraint.

**So: the coefficients are not mis-paired, and PROTOCOL should not move delta. If a coefficient
ever moves, it is gamma, and moving it is a decision about how much return the project demands,
not about risk.** This lines up with idea 129 (the CAGR floor is not a risk bar), idea 148 (the
floor does 4b's exclusion work under the no-leverage ceiling) and idea 156.

## Rule 8 walk-forward (gross chosen on ≤2016-12-31, read once on 2017→)

Selector means over the 24 book-panel cells. `S_BAND` = midpoint of the IS-estimated band
clipped to (0, 1.00]; `S_STATIC` = 0.75 (do-nothing); `S_ISDD` = largest g clearing the IS DD cap.

| selector | mean g | OOS CAGR | OOS Sharpe | OOS MaxDD | OOS gross-bar pass |
|---|---|---|---|---|---|
| S_BAND | 0.638 | 9.36% | 0.8129 | −18.70% | **41.7%** |
| S_ISDD | 0.604 | 8.97% | 0.8128 | −17.54% | 41.7% |
| S_STATIC | 0.700 | 9.79% | 0.8138 | −22.35% | 20.8% |

SPY OOS 15.45% / 0.882 / −33.72%. RULES v1 OOS: u56 7.73% / 0.747 / −13.83%;
B136 5.94% / 0.576 / −21.19%; SMALL 6.35% / 0.492 / −36.12%.

The band selector **doubles** the OOS pass rate (41.7% vs 20.8%) and takes 3.7pp off OOS
drawdown, and buys **exactly nothing** in Sharpe (0.8129 vs 0.8138, −0.001) for −0.43pp of OOS
CAGR. That is the expected shape: gross is Sharpe-neutral (idea 66), so the band can only ever
be a drawdown instrument. It is also *not* better than the cruder cap-only control S_ISDD,
which matches its pass rate at lower gross. **Independent support for idea 163's hypothesis
that a 4b-aware IS screen pays only through drawdown.**

Transfer is the weak point: Spearman(rho/s IS, rho/s OOS) = **+0.585** over 24 cells and the
consistency verdict agrees IS-vs-OOS in only **75.0%** (IS non-empty 10/24, OOS 14/24). rho is
a one-path statistic and inherits all of that path's estimation error.

## Verdict

**KILL** of "4b's two coefficients are mis-paired / the band is empty". The band is non-empty
for 12 of 24 books and fully satisfiable for 7. **No new KEEP** — nothing here proposes a book;
this run prices a PROTOCOL bar, and idea 144 already holds that a re-grossed book is the same
book. 4a passes at some gross in 15 of 24 cells and is not the object of this run.

## By-product worth one line (bears on idea 154, still open)

`EWBAND3` (idea 57's ew-all + 3% band) clears **all five 4b bars on BOTH large-cap panels** at
g ∈ {0.80, 0.90} — u56 0.80–1.00, B136 0.80–0.90 — which is a cross-universe 4b pass at a gross
idea 84 did not test and idea 154's premise (capped at 0.7877 on broad) reads as unavailable.
The construction convention here may differ from idea 84's; **not claimed as a KEEP**, flagged
for idea 154's dedicated run.

## Caveats

Survivorship on all three panels (current constituents; worst on SMALL — see
`data/SMALL_PANEL_README.md`, idea 54) and it flatters rho in the direction that makes 4b look
*more* satisfiable than it is. rho and the band's edges are single-path statistics. The
analytic band is a first-order identity; every verdict is read off the exact ladder. Levered
ladder points are computed so the right edge is visible and excluded from every verdict
(rule 2). Ideas 38 (calendar-day index) and 126 (t+1) carry over and affect all arms equally.
