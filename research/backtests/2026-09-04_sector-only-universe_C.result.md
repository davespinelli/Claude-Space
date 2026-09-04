# Idea 10 — sector-only-universe — **KILL**, and the complement is the finding

**Script:** `research/backtests/2026-09-04_sector-only-universe_C.py` ·
**Console:** `..._C.console.txt` · **Grid:** `..._C.grid.csv` · 2026-09-04, lane C ·
10 bps, weekly, next-day execution, 75% gross.

30 grid points (6 panels × [v1 + EWall + CAND n∈{5,10,20}]), **all reported**. Harness
reproduces idea 2's published KEEP row to the decimal (12.7% / 1.093 / −18.3%, halves
1.088/1.103) and the live RULES v1 row before any new number.

## Verdict: KILL. Dropping the single stocks removes more return than risk.

**0 of 10 ETF-only points pass 4a or 4b**, and none is close. The best ETF arm is
`ETF36/CAND-n20` at **6.8% / 0.817 / −15.2%** (halves 0.754/0.878, OOS 8.1%/0.943) against
SPY's 15.3% / 0.890 / −33.7%; it fails 4b on **H1 and CAGR** — the CAGR floor is 10.68% and
it earns 6.8%. The literal queued arm (`ETF24`, broad + sector ETFs only, no bonds or
commodities) is worse still: **6.7% / 0.779 / −15.2%**, failing H1, H2 *and* CAGR.

**Half the hypothesis is right and it does not help.** Matched construction, same days,
same gross, vs the full-list control: `ETF36` has **lower vol in 10 of 10 pairs** and
`ETF24` in 6 of 10 — so the idiosyncratic-risk claim is real on volatility. But the
drawdown claim fails (shallower in only 4/10 and 2/10), and **Sharpe is worse in 20 of 20
pairs**, because the return loss is far larger than the risk saved: **−6.15%/yr mean for
ETF36 (t to −5.31) and −5.02%/yr for ETF24 (t to −4.11)**. Risk came down; return came
down more.

## The complement control is where the run earns its keep

The mirror panel — the same 56-name list stripped down to its **20 mega-cap single
stocks** — carries the entire edge, and produced the run's only 4a pass (1 of 30; prior 4a
passes exist in ideas 2, 40 and 55):

| point | CAGR | Sharpe | MaxDD | H1 / H2 | OOS | 4a | 4b |
|---|---|---|---|---|---|---|---|
| STK20/CAND-n20 | 12.1% | **1.338** | −12.1% | 1.341 / 1.344 | 14.0% / 1.449 / −12.1% | **PASS** | PASS |
| STK20/CAND-n10 | 19.0% | 1.305 | −17.3% | 1.295 / 1.321 | 21.2% / 1.366 / −17.3% | no | PASS |
| STK20/v1 (live rules, ETFs removed) | 18.1% | 1.135 | −19.3% | 1.157 / 1.122 | 19.1% / 1.140 | no | PASS |
| U56/CAND-n20 (idea 2's standing candidate) | 12.7% | 1.093 | −18.3% | 1.088 / 1.103 | 14.4% / 1.170 | no | PASS |

Both rule-8 selections pick a STK20 arm (S1 → n=10, S2 → n=20) and **both clear all three
OOS 4b bars**, with Spearman(IS, OOS Sharpe) = **+0.608** over the 18 CAND points — the
strongest in-sample/out-of-sample rank agreement the project has recorded (idea 8 got
+0.000 on this list). Running v1's *own* construction on stocks only is worth **+11.6pp
CAGR and +0.468 Sharpe (t +4.07)** over running it on the full list.

## Why STK20 is a PARK and not a KEEP — the internal control says so

Those numbers are the most survivorship-exposed in the repository. `universe.json`'s
megacap group is 20 tickers picked as 2026 constituents (NVDA, AVGO, PLTR, META, TSLA…);
they are in the file *because* they won, and a momentum book on them is close to a
look-ahead portfolio. The run contains its own measurement of that bias:

- **STK20** (20 hand-picked mega-caps) beats its control by **+5.19%/yr, t up to +4.45**,
  Sharpe better in 5 of 5 pairs.
- **BSTK100** (the same test on `universe_broad.json`'s 100 single stocks — a much wider,
  less curated stock leg) beats its control by only **+0.92%/yr, t max +2.04**, Sharpe
  better in 3 of 5, and **fails 4b on drawdown** at every n.

The "stocks beat ETFs" effect therefore shrinks by 5.6× when the stock leg goes from 20
curated names to 100, which is what selection — not a premium — looks like. The honest
reading is that **STK20 measures the survivorship bias itself**, and its 4a/4b passes
should not be treated as capital-worthy. Recommended against; memo written with the RULES
wording it *would* require, for the Sunday review to reject on the record.

## Other results worth keeping

- **The ETF book is not composition-fragile, and that buys nothing.** The 36 ETFs are
  bit-identical in `universe.json` and `universe_broad.json` (symmetric difference `[]`),
  so an ETF-only book passes idea 53's cross-universe test by construction — and still
  fails 4b outright. Universe invariance is not a substitute for return.
- **Ranking is worth more on ETFs than on stocks, in the wrong direction.** On ETF36,
  `CAND-n20` (0.817) beats `EWall` (0.631) by +0.186 Sharpe; on U56 the ranked book
  (1.093) beats EWall (1.050) by only +0.043. Ranking a low-dispersion panel harder does
  not rescue it.
- **`B136/EWall` passes 4b** (10.7% / 1.027 / −17.7%, halves 1.146/0.917, OOS 1.021) —
  equal-weighting every eligible name in the broad list, no ranking at all, at 8.3×
  turnover. It is a cheaper book than any ranked arm and belongs in the Sunday comparison.
- **ETFs were the drag in 2015 and 2023**: ETF36 −4.2% vs STK20 +12.2% in 2015, and +6.4%
  vs +24.9% in 2023.

## Caveats

Survivorship: current constituents of both lists, one-directional. It runs **against** the
ETF KILL (an ETF panel is barely flattered, so the ETF book's shortfall is if anything
understated relative to a fair stock panel) and **hard in favour** of the STK20 result,
which is why that arm is parked. The ETF-vs-control comparisons hold days, gate, gross and
construction fixed. No delisted names anywhere.

Ideas 71–73 queued.
