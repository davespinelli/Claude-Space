# Idea 152 — price-the-broad-POS-near-miss (cloud, 2026-09-05)

**ANSWERED. The near-miss is real, is priced exactly, and is NOT capital-worthy. `broad @10bps,
POS, n=20` has a genuine unlevered 4b interval at `m ∈ [0.55, 0.70]` (4 of 25 ladder points;
the true continuous interval is ≈ [0.50, 0.74]) — but it is broad-only, 10-bps-only, and buys
its 1.14pp of drawdown with 1.07pp of CAGR. Cross-universe 4b is 0 of 25 m-points. 25 bps kills
it outright. VERDICT: PARK as a broad-only book, KILL as a cross-universe KEEP-candidate.**

The run's transferable result is a *classification*, not a book: **which 4b bar a near-miss
fails determines whether gross can fix it.** POS's DD failure closed on the ladder; NONE's H2
failure did not move at all across a 7x gross range (H2 = 0.807 → 0.815 against a 0.834 bar).

Script `2026-09-05_price-the-broad-POS-near-miss_cloud.py`; outputs `.console.txt`, `.grid.csv`,
`.intervals.csv`, `.lever.csv`, `.walkforward.csv`, `.transfer.csv`.

## Reproduction, before any new number was read

| check | target | this run |
|---|---|---|
| [a] `INV / n=5 / w=0.15` vs `baseline.rules_v1_weights`, all 3 panels | 0 | **0.000e+00 (EXACT)** |
| [b] idea 81's POS/broad/n=20/m=0.75 @10bps | 16.0% / 1.052 / -21.4%, halves 1.197/0.927, OOS 1.005 | **16.0% / 1.052 / -21.4%, halves 1.197 / 0.927, OOS 1.005 — REPRODUCED to published precision** |
| [b] premise: POS fails 4b on the DD cap ALONE, by ~1.2pp | DD only | **DD only; margin -1.14%** |
| [c] premise: NONE fails 4b on H2 ALONE | H2 only | **H2 only; margin -0.023** |

Both halves of idea 152's premise reproduce exactly. Nothing below rests on a re-derivation.

## Corpus and grid

3 panels (broad / u56 / small) x 2 cost rungs (10, 25 bps) x **exactly two tuned parameters** —
the vol scaler in {INV = `/sqrt(v)`, NONE = `x1`, POS = `x sqrt(v)`} and the target gross
`m` in 25 points from 0.20 to 1.40 — = **450 books, every one in `.grid.csv`**. `n` is held at
20 (idea 81's published cell), not tuned. Weekly, t+1, `m/n` per name. Points at `m > 1.00` are
run so the ladder brackets the DD cap from both sides, and are flagged LEVERED and excluded
from every KEEP claim per PROTOCOL rule 2.

## (1) Idea 66's lever is near-exact under this engine — so the interval reading is valid

The engine drifts weights between rebalances and renormalises by portfolio value *including*
the cash residual, so `m` scaling the targets is not algebraically guaranteed to scale the
return series. Measured rather than assumed, over all 18 (panel, cost, scaler) cells:

| statistic | value |
|---|---|
| max Sharpe spread across the 25-point ladder, any cell | **0.0112** (broad/NONE @25bps) |
| median Sharpe spread | 0.0043 |
| max relative deviation of `r(m)` from `(m/0.75)·r(0.75)` | 0.14 (tail days only) |

Sharpe moves by at most ~1% of its level over a **7x** change in gross. Idea 66's "exact
Sharpe-neutral lever" survives; the H1/H2/OOS bars are effectively gross-invariant and the
DD/CAGR bars are not. That asymmetry is the whole mechanism below.

## (2) The interval test (idea 90) — POS has one on broad, NONE has none anywhere

Unlevered 4b-passing `m` per (panel, cost, scaler); the interval is a **descriptor**, never a
bar (idea 90's standing verdict):

| panel | cost | INV | NONE | POS |
|---|---|---|---|---|
| broad | 10 bps | empty (H2, OOS, CAGR) | **empty (H2 at every m)** | **[0.55, 0.70]**, 4/25 |
| broad | 25 bps | empty | empty | **empty** |
| u56 | 10 bps | [0.85, 0.85], 1/25 | [0.65, 0.80], 4/25 | [0.65, 0.80], 4/25 |
| u56 | 25 bps | empty | empty | empty |
| small | 10 bps | empty | empty | **empty** |
| small | 25 bps | empty | empty | empty |

`m = 0.75` is **outside** the broad POS interval — it sits one grid step above the DD ceiling.
The two ends are the two gross-sensitive bars, exactly as predicted: the CAGR floor binds below
(m=0.50 misses it by 0.02pp) and the DD cap binds above (m=0.75 misses it by 1.14pp).

**The NONE result is the decisive control.** Over the whole ladder — a 7x range of gross —
NONE's H2 Sharpe moves from 0.8067 to 0.8154 against a bar of 0.8340. No gross level reaches
it, and none ever could. A book failing a Sharpe bar cannot be re-grossed into a pass; a book
failing DD or CAGR can. That is the reusable finding.

## (3) The price of the pass: 1.07pp of CAGR for 1.14pp of drawdown

broad @10bps, POS, n=20, along the interval:

| m | CAGR | Sharpe | MaxDD | H1 | H2 | OOS Sharpe | turnover | 4b |
|---|---|---|---|---|---|---|---|---|
| 0.50 | 10.64% | 1.050 | -14.58% | 1.195 | 0.924 | 1.002 | 10.2x | FAIL (CAGR by 0.02pp) |
| 0.55 | 11.71% | 1.050 | -15.97% | 1.195 | 0.925 | 1.003 | 11.2x | **PASS** |
| 0.60 | 12.77% | 1.051 | -17.34% | 1.196 | 0.925 | 1.003 | 12.2x | **PASS** |
| 0.65 | 13.84% | 1.051 | -18.69% | 1.196 | 0.926 | 1.004 | 13.2x | **PASS** |
| 0.70 | **14.91%** | 1.051 | **-20.04%** | 1.196 | 0.926 | 1.004 | 14.3x | **PASS** (DD margin +0.02pp) |
| 0.75 | 15.98% | 1.052 | -21.36% | 1.197 | 0.927 | 1.005 | 15.3x | FAIL (DD by 1.14pp) |

SPY: 15.23% / 0.889 / -33.72%, halves 0.957 / 0.834, OOS 0.882. RULES v1 on broad @10bps:
6.39% / 0.635 / -21.19%. The m=0.70 book is the best point in the interval: it gives up
1.07pp of CAGR against m=0.75 and lands the drawdown cap with 0.02pp to spare.

## (4) It does not transfer — the precondition idea 152 itself set

Read at the same `m` on the other two panels @10bps:

| m | broad/POS | u56/POS | small/POS | cross-universe |
|---|---|---|---|---|
| 0.55 | **PASS** | FAIL (CAGR) | FAIL (H1,H2,OOS,DD,CAGR) | 1/3 |
| 0.60 | **PASS** | FAIL (CAGR) | FAIL (all five) | 1/3 |
| 0.65 | **PASS** | **PASS** | FAIL (all five) | 2/3 |
| 0.70 | **PASS** | **PASS** | FAIL (all five) | 2/3 |

**Cross-universe 4b is 0 of 25 m-points.** The small panel fails every bar at every gross with
the POS tilt — which is exactly idea 81's finding that the tilt's winning sign is panel-signed
(the sub-$2B panel's own vol premium runs the other way). De-grossing cannot fix a signal
that is pointed the wrong way.

## (5) Rule 8 walk-forward — chosen on 2009-2016, read once on 2017-2026

| panel | cost | selector | pick | OOS CAGR / Sharpe / MaxDD | vs RULES v1 OOS | vs SPY OOS | OOS-window 4b |
|---|---|---|---|---|---|---|---|
| broad | 10 | S1 IS-Sharpe | POS / m=1.00 | 20.86% / 1.007 / **-27.80%** | +0.431 | +0.125 | **False** |
| broad | 10 | S2 4b-aware (6 adm.) | **POS / m=0.60** | **12.56% / 1.003 / -17.34%** | +0.427 | +0.121 | **True** |
| broad | 25 | S1 = S2 (0 adm.) | POS / m=1.00 | 17.16% / 0.858 / -29.59% | +0.703 | **-0.024** | False |
| u56 | 10 | S1 = S2 (0 adm.) | NONE / m=0.80 | 15.33% / 1.168 / -19.46% | +0.421 | +0.286 | True |
| u56 | 25 | S1 = S2 | NONE / m=0.85 | 14.43% / 1.050 / -20.75% | +0.651 | +0.168 | False |
| small | 10 | S1 = S2 | INV / m=1.00 | 4.00% / 0.312 / -37.50% | **-0.269** | **-0.570** | False |
| small | 25 | S1 = S2 | INV / m=0.95 | -1.02% / 0.022 / -45.59% | -0.229 | -0.860 | False |

SPY OOS 15.45% / 0.882 / -33.72%. RULES v1 OOS: broad 5.94%/0.576/-21.19%, u56
7.73%/0.747/-13.83%, small 7.92%/0.581/-32.84%.

The 4b-aware screen (S2) is what keeps the broad pick inside the drawdown cap: plain IS-Sharpe
(S1) picks the top of the ladder and fails the OOS-window 4b on drawdown. That is a second,
independent datum for the standing question of whether rule 8's IS screen earns its complexity
— **here it does**, and it does so through the DD bar specifically. Note also that the *best*
OOS cell in the whole run is **u56/NONE/m=0.80** (1.168 Sharpe, 15.33% CAGR), i.e. the book
with **no** vol tilt on the panel where the tilt is not signed — consistent with idea 81's KILL.

## (6) Census over all 450 grid points

4a passes 140/450. 4b passes **13/450**, all of them unlevered, all of them @10 bps, none on
the small panel: broad/POS 4, u56/POS 4, u56/NONE 4, u56/INV 1. Failing-bar counts over the 306
unlevered points: CAGR 237, H2 204, OOS 187, H1 170, DD 121. **At 25 bps: 0 of 150 unlevered
points pass 4b on any panel with any scaler** — idea 82's proposed 25-bps breakeven bar kills
the whole family, POS included.

## Predictions, scored honestly

| | prediction | outcome |
|---|---|---|
| P1 | [a],[b],[c] hold | **HIT** — all three exact |
| P2 | Sharpe spread < 0.05 across the ladder in every cell | **HIT** — max 0.0112 |
| P3 | POS/broad has a non-empty interval, DD above / CAGR below, m=0.75 above the top | **HIT** — [0.55, 0.70], exactly those two bars, 0.75 above |
| P4 | NONE/broad interval empty at every m | **HIT** — H2 immovable over 7x gross |
| P5 | The interval does not transfer; cross-universe 4b 0/25 | **HIT** — 0/25; small fails all five bars everywhere |
| P6 | Nothing survives 25 bps | **HIT** — 0 of 150 unlevered points |

Six of six pre-registered predictions hit. That is a well-specified question, not a discovery.

## Verdict

**PARK the broad-only book; KILL the cross-universe KEEP claim.** Per idea 144 a de-grossed
book is the same book, so `POS/broad/n=20/m=0.70` is not a new signal — it is idea 81's
already-killed tilt run at a smaller risk budget. It passes 4b on one panel at one cost rung
and its rule-8 S2 pick passes the OOS-window 4b, which is why it is parked rather than killed
outright; it fails on both other panels and at 25 bps, which is why it is not a KEEP.

## Two reporting clauses proposed to the Sunday review (no RULES change requested)

1. **Classify every 4b near-miss by which bar it fails.** A DD or CAGR failure is a *risk-budget*
   failure and is closable on the gross ladder; an H1/H2/OOS failure is a *signal* failure and
   is not closable at any gross. This run measures both cases side by side on one harness
   (POS: DD closed at m ≤ 0.70; NONE: H2 moved 0.0087 over a 7x gross range against a 0.027 gap).
   The leaderboard should record the failing bar, not just "misses 4b by Xpp".
2. **A 4b pass reached only by de-grossing should be recorded with its interval and its
   cross-universe count in the same row.** Here: `[0.55, 0.70], 1 of 3 panels, 0 of 3 at 25 bps`.

## Caveats carried

Survivorship on all three current-constituent panels (idea 54); the small panel drops the 44
tickers with `max_1d_move >= 1.0` and uses SPY as a held-out benchmark, not a constituent, and
its bias runs *against* POS being real (the high-vol cohort POS tilts into is where delisted
names would sit, so every POS number here is an upper bound). Idea 128 (the IS window's SPY
drawdown is shallower than the OOS window's). Idea 38 (calendar-day price index) and idea 126
(t+1 execution only). Idea 49/39 (the eligibility gate is inverted on the small panel). No IWM
in the cache, so the small panel is judged against SPY.
