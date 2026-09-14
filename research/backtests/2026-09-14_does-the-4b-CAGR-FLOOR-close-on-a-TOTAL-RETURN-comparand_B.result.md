# Idea 850 — does the 4b CAGR FLOOR close on a TOTAL-RETURN comparand?
**2026-09-14, lane B — VERDICT: KILL (the premise is FALSE). Nothing promoted, no RULES change.**

Script: `2026-09-14_does-the-4b-CAGR-FLOOR-close-on-a-TOTAL-RETURN-comparand_B.py`
Outputs: `.console.txt`, `.convention.csv`, `.books.csv` (924 rows), `.walkforward.csv`, `.quantization.csv`
2 tuned params: comparand drag *d* (7 rungs) x candidate set {SHELF, GRID}. All 14 combinations reported, none selected.
Costs 0 / **10** / 25 bps, next-day execution. SURVIVORSHIP: U56/B136 are current-constituent lists; every LEVEL is optimistic, the CONTRASTS are the claim.

## The claim under test
> "every 4b floor in the record is priced against the **price-only** SPY column in `data/prices.csv`
> while the traded panel is adjusted closes, so the floor may be systematically mis-set in one
> direction; measure the sign and size."

The queue filed it **PARK, needs a dividend/total-return series**. It does not. The convention of
`data/prices.csv` is decidable **from the file itself**, because the same file carries six
fixed-income ETFs whose *price* return is structurally pinned and whose *total* return is not.

## GATES — 5 of 5 PASS, printed before any new number
| | gate | result |
|---|---|---|
| G1 | SPY headline reproduces the record's committed 15.1631% / 0.8861 / −33.7172% | max\|d\| **4.561e-05** |
| G2 | the committed FIXED bars ARE 60%/70% of that SPY, so a comparand move moves them mechanically | cap −20.2303% vs −20.23%, floor 10.6142% vs 10.61% |
| G3 | `fast_run` == `engine.backtest` on RULES v2 / U56 / 10 bps | max\|d\| **1.388e-17** |
| G4 | the *d*=0 comparand IS the committed column (empty counterfactual = identity) | max\|d\| **0.000e+00** |
| G5 | `prices.csv` and `prices_broad.csv` share ONE convention on the 48 of 56 shared tickers never under $5 | ratio drift **1.680e-03** vs the 0.2–0.3 a convention gap would open |

All 8 committed 4b shelf memos rebuild inside idea 851's tolerance (worst dS 0.0202, `u56-top20-band-m20`); none dropped.

## PART A — the premise is FALSE, on 3 of 3 independent internal legs
| ticker | sleeve | first → last | cumulative | CAGR/yr |
|---|---|---|---|---|
| SHY | 1-3y UST | 60.815 → 81.370 | **+33.80%** | 1.57% |
| IEF | 7-10y UST | 55.378 → 91.010 | +64.34% | 2.69% |
| TIP | TIPS | 61.917 → 105.840 | +70.94% | 2.91% |
| LQD | IG corp | 51.421 → 104.320 | +102.88% | 3.86% |
| HYG | HY corp | 31.349 → 78.600 | +150.73% | 5.04% |
| TLT | 20y+ UST | 53.382 → 80.870 | +51.49% | 2.25% |

- **LEG 1 — par pull.** A fund holding only 1-3 year Treasuries redeems its paper at par; its clean price is a bounded, mean-reverting series that cannot compound. Cached SHY compounds **+33.80% over 18.7 years** and its **minimum is its first observation** — it never once revisits its starting level in 4,703 sessions. A price-only short-Treasury series cannot do this.
- **LEG 2 — the ladder.** The six sleeves compound in exact **yield order** (SHY 1.57 < IEF 2.69 < TIP 2.91 < LQD 3.86 < HYG 5.04). That is carry. A price-only set would order by duration-weighted rate moves, not by coupon.
- **LEG 3 — the long end.** TLT runs 53.38 → peak 141.58 (2020-08-04) → 80.87, i.e. **−42.88% from its peak**, yet **+51.49% from the start**. A cumulative gain through a price collapse of that size is coupon, not price.

`data/prices.csv` is a **dividend-reinvested (total-return) panel**. SPY is a column of that same
file, written by the same `engine.load_prices` call (`auto_adjust=True`, falling back to this
cache). **Benchmark and traded panel are on ONE convention by construction: the mismatch the idea
postulates is ZERO, not small.** G5 adds that the sandbox holds no *second* convention either, so
a genuine price-only comparand would still have to come from outside.

## PART B — the size, had the premise been true (7 drags x 2 sets, ALL reported)
| d %/yr | SPY CAGR | Sharpe | MaxDD | 4b floor | 4b cap | SHELF 4b | GRID 4b | 4a |
|---|---|---|---|---|---|---|---|---|
| **0.00** | **15.1631%** | **0.8861** | **−33.7172%** | **10.61%** | **−20.23%** | **8 / 8** | **19 / 36** | 0 / 8, 1 / 36 |
| 0.50 | 14.5890% | 0.8578 | −33.7481% | 10.21% | −20.25% | 8 / 8 | 19 / 36 | unchanged |
| 1.00 | 14.0178% | 0.8296 | −33.7789% | 9.81% | −20.27% | 8 / 8 | 20 / 36 | unchanged |
| 1.50 | 13.4493% | 0.8014 | −33.8097% | 9.41% | −20.29% | 8 / 8 | 20 / 36 | unchanged |
| 1.80 | 13.1097% | 0.7844 | −33.8281% | 9.18% | −20.30% | 8 / 8 | 20 / 36 | unchanged |
| 2.00 | 12.8838% | 0.7731 | −33.8404% | 9.02% | −20.30% | 8 / 8 | 20 / 36 | unchanged |
| 2.50 | 12.3210% | 0.7449 | −33.8712% | 8.62% | −20.32% | 8 / 8 | 22 / 36 | unchanged |

**SIGN.** The floor moves **DOWN** with the drag, at **−0.798 pp per 1.00 %/yr** (the 0.70
coefficient, essentially exactly). Had the record really been using a price-only SPY, its 4b CAGR
floor would have been **too LOW** and every 4b verdict **too GENEROUS** — the convention it
actually uses is the *stricter* one. The idea's "systematically mis-set in one direction" is
wrong twice over: the direction is the safe one, and it is **not one direction** —

**SECOND-ORDER.** A drag also shallows the comparand's MaxDD (−33.72% → −33.87%), so the **cap
TIGHTENS as the floor loosens**. The two 4b level bars move in *opposite* directions under a
comparand error. They do not cancel; they trade off, and the Sharpe legs (H1 0.9595 → 0.8075,
H2 0.8259 → 0.6936) loosen alongside the floor.

**HOW MUCH SLACK IS THERE.** At *d*=0 the shelf's CAGR margins run **+0.78% .. +4.80%**; the
tightest is `u56-band008-gross100` at +0.78%. It would take **1.11 %/yr** of comparand error *in
the wrong direction* (a floor too HIGH) to cost the shelf its first CAGR pass — and a price-only
comparand errs the other way. **3 of 44 books** change their 4b verdict anywhere on the drag grid
(`U56-qroll-q0.12-w252-d1.00` first, at d=1.00); **41 are invariant to the comparand convention.**
4a never reads SPY and is invariant by construction: 1 of 44 books passes it at every d.
Rung sensitivity: SHELF 8/8/7 at 0/10/25 bps at d=0; GRID 20/19/14.

## PART C — rule 8 (dial on 2009-2016 IS Sharpe, OOS 2017-2026 read once per (d, panel))
| | pick | IS Sharpe | OOS CAGR | OOS Sharpe | OOS MaxDD | OOS H1/H2 | 4b | 4a |
|---|---|---|---|---|---|---|---|---|
| U56 | `U56-band0.08-g1.00` | 1.1226 | **12.04%** | **1.1654** | −19.05% | 1.2461 / 1.0785 | PASS | FAIL |
| B136 | `B136-band0.08-g1.00` | 1.1421 | **11.05%** | **1.0974** | −19.50% | 1.2177 / 0.9628 | PASS | FAIL |
| RULES v2 OOS | — | — | 9.47% / 7.88% | 1.2782 / 1.1059 | −12.05% / −12.24% | — | — | — |
| RULES v1 OOS | — | — | 7.60% / 5.87% | 0.7361 / 0.5702 | — | — | — | — |
| SPY OOS | — | — | 15.33% | 0.8767 | −33.72% | — | — | — |

The pick is **identical at all 7 drags on both panels** (1 distinct pick per panel) — the comparand
reaches the **bars only, never the chooser**, exactly as it should when the dial is IS Sharpe.
The OOS 4b verdict differs from the *d*=0 reading in **0 of 14** (drag, panel) cells, and
RE-PRICED vs the record's FIXED full-sample bars in **0 of 14**. 4a fails in 14 of 14: the picks
out-return RULES v2 by 2.6/3.2 pp of CAGR but lose on Sharpe and carry 7 pp more drawdown.

## BY-PRODUCT (found while gating; not the idea)
`data/prices_broad.csv` is stored at **two decimals**, `data/prices.csv` is not. On back-adjusted
low-priced history that is not a rounding nicety: **216,129 of 263,368 shared cells differ (82.1%)**,
max absolute 0.0052 (half a cent) but max **relative 3.63%** (NVDA, whose split-adjusted 2009 price
is near $0.14; then NFLX 1.59%, AVGO 0.45%, TSLA 0.37%, AMZN 0.24%). Priced end-to-end on the 56
tickers both files carry, the same book run on the full-precision vs the 2-decimal panel moves
**dSharpe ≤ 0.0009** and dMaxDD 0.00 pp — **inside** idea 851's 0.030 admission tolerance, so no
committed number is wrong. But it is a **floor under the reproducibility of every B136 result** and
**no committed file states it**. NAMED, not fixed: `cache_prices.py` is out of scope for this lane.

## What the record should take from this
1. **The idea is closed, not parked.** Its PARK tag ("needs a dividend/total-return series") was
   itself the error: the panel's own fixed-income columns answer it with no network.
2. A PROTOCOL line worth a Sunday review (**not applied here**): *a 4b verdict should name the
   return convention of its comparand, and that convention must be the one the traded panel is on.*
   Today it is, by construction — the census above is what makes that checkable rather than assumed.
3. 4a is comparand-free; only 4b is exposed to this class of error at all.
