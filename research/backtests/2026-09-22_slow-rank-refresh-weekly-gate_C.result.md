# Idea 2250 — does a SLOWER RANK REFRESH at an unchanged WEEKLY band gate keep the BOTH-PATHS pass?

**Lane C, 2026-09-22.** Script `2026-09-22_slow-rank-refresh-weekly-gate_C.py`; grid
`.grid.csv` (64 cells), walk-forward `.walkforward.csv` (32 picks), console `.console.txt`.

## Verdict — **KILL** of the cost-robustness hypothesis; **PARK** of the by-product

Slowing the top-20 composite refresh to 2W / M / Q while the band3 gate, the de-risking and the
TLT/GLD/UUP sleeve keep running WEEKLY does **not** rescue the both-paths cell on the cost ladder
that disqualified it. **1 of 64 cells clears the Sunday promotion bar at 25 bps** (u56 / M /
backfill / 25 bps), its CAGR-floor margin is **+0.22 pp**, and **rule 8's IS chooser does not
reach it** — at u56 @25 bps S0 picks Q/backfill, whose OOS Sharpe 1.2369 sits *below* the live
book's 1.2399, so the bar fails. At 50 bps **0 of 16**. On `broad`, **0 of 32** cells clear the
bar at any cost rung, because the book never beats the live book out of sample there.

## The mechanical result that decides it: there is a TURNOVER FLOOR at ~5x/yr

| panel | R = W (committed) | 2W | M | Q |
|---|---|---|---|---|
| u56   | **8.18x** | 6.67x | 5.81x | 5.23x |
| broad | **10.88x** | 8.54x | 6.90x | 5.85x |

Quarterly refresh — a 13x slower ranking — removes only **36%** of u56's turnover and **46%** of
broad's. The rank refresh is a minority of this book's trading: the weekly band gate, the weekly
`rw` re-spread and the weekly sleeve re-solve are the majority, and none of them is touched here.
The live book trades **1.77x/yr**. The pre-declared cost-aware chooser S2 (IS turnover ≤ 4.0x/yr)
**abstains in all 8 (panel, cost) cells** — no rung on this ladder is even admissible to it. Any
device that wants this candidate cost-robust has to attack the other two legs, not the ranking.

## What the slowdown DOES buy (the by-product, at ≤ 10 bps only)

On u56 @10 bps the device is a strict improvement on every axis at once. Committed cell
(R = W): 11.27% / 1.2634 / −11.63%, halves 1.2822 / 1.2476, OOS 1.2885, **8.18x**. Monthly with
backfill: **11.78% / 1.3081 / −11.05%**, halves 1.3179 / 1.3008, OOS **1.3512**, **5.76x** — more
CAGR, more Sharpe, shallower drawdown and 30% less trading. 1767's staleness mechanism does **not**
bite here: slowing the ranking costs nothing on this book, which is itself a finding about the
composite rank's weekly churn (it is trading, not information).

**Rule 8 reaches a passing cell at 10 bps.** S0 and S1 both pick R = 2W / backfill on u56 @5 and
@10 bps: OOS 11.75% / **1.2819** / −11.09% at 6.64x, against live RULES v2 OOS 9.46% / 1.2767 /
−12.05% and SPY OOS 15.29% / 0.8751 / −33.72%. Both KEEP paths pass. Pooled over the 8
(panel, cost) cells the IS chooser beats the shipped R = W default by **+0.0600** of mean OOS
Sharpe (S0, 6 of 8 cells; S1 +0.0405, 4 of 6 non-abstaining) while cutting turnover ~20-35%.

## Why that is still not a promotion

It inherits the parent's disqualification verbatim: **everything above 10 bps dies** (u56 @25 bps
the chooser's own pick fails the bar; @50 bps 4b fails on the CAGR floor in every one of the 16
cells) and **`broad` never beats the live book out of sample** at any refresh rung or cost rung
(0 of 32). The 2026-09-20 Sunday review refused the R = W cell for exactly this shape. A cheaper
version of a book whose whole edge still lives at ≤10 bps is a better book, not a capital-worthy
one. Memo written, PARK.

## Gates (all four exact, printed before any hypothesis was read)

* **G1** `H.run` == `engine.backtest` on RULES v2 @10 bps: `0.000e+00` on both panels.
* **G2** (R = W, backfill = False) reproduces the committed cell: frame diff `0.000e+00` on every
  row the simulator reads, **net-return diff `0.000e+00`** on both panels. (Off-schedule rows
  differ by construction — the slowed frame is held between refreshes — and are never read.)
* **G3** backfill is a no-op at R = W: `0.000e+00` on both panels.
* **G4** 64 of 64 cells published, pass and fail alike.

## Caveats

* **Survivorship (PROTOCOL rule 9 / idea 54):** u56 and broad are CURRENT-constituent lists, so
  every CAGR level is optimistic and both 4b bars are easier than on a point-in-time panel. The
  cadence contrast is within-tape (same names, same dates, only the refresh schedule moves) and
  is first-order immune; the pass counts are not.
* Flat bps-on-turnover cost model: a slower book trading the same notional at worse prices is
  invisible here. That is the record's own convention, and the one every 4b verdict uses.
* t+1 execution throughout; the Sunday review already showed latency non-binding for this cell.
* `2W` is every second weekly date anchored on the first — one phase, not a phase average.
