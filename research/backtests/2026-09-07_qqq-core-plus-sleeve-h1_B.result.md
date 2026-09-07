# Idea 30 — qqq-core-plus-sleeve-h1 — **KILL** (lane B, 2026-09-07)

Script: `research/backtests/2026-09-07_qqq-core-plus-sleeve-h1_B.py`
Artifacts: `.grid.csv` (192 rows), `.walkforward.csv` (40 rows), `.console.txt` (full log)

## The question
Idea 24 published `60% QQQ>200d + 40% macro sleeve` at 10.8% / 0.95 / -18.9% with halves
0.84 / 1.04 — a KILL whose H2 clears SPY and whose H1 does not. The queue asked *why* the
first half fails, and whether `50% QQQ + 10% SPY + 40% sleeve` fixes it.

## Harness gate (a MATCH, not a reproduction — read the provenance)
Variant B, rebuilt from idea 24's source, **matches the published decimals** on the tape truncated
to idea 24's own last bar (2026-09-02): 10.8% / 0.95 / -18.9% / 0.84 / 1.04. On today's tape (two
extra bars) the same code reads 10.9% / 0.95 / -18.9% / 0.84 / 1.05.

Provenance matters here and the record should not overstate it: `data/prices.csv` is now on the
**corrected trading-day index** (4699 rows, **0 weekend rows**, asserted in the script), while idea
24 computed its row on the pre-fix calendar-day tape, which is no longer in the repo. So this is a
match to two decimals *across* that correction, not a byte-level rerun of idea 24's numbers — the
agreement bounds how much the index fix moved this particular book, and nothing more. Per idea 39
the calendar-day cache was conservative rather than generous, which is the tolerable direction, but
the label stays "match".

Leg additivity `corr(core + sleeve, blend) = 0.999988`, mean |diff| 1.15e-05/day.

## The answer: it is a RETURN shortfall, and the 200d gate on the core is all of it
Algebraic split of the Sharpe gap against SPY, `dS = (mu_B - mu_S)/sig_B + mu_S(1/sig_B - 1/sig_S)`:

| period | mu_B | mu_SPY | sig_B | sig_SPY | dSharpe | return term | vol term |
|---|---|---|---|---|---|---|---|
| H1 (2009-01 -> 2017-11) | 8.69% | 15.74% | 10.30% | 16.45% | **-0.113** | **-0.684** | +0.571 |
| H2 (2017-11 -> 2026-09) | 13.25% | 15.76% | 12.58% | 18.90% | +0.219 | -0.200 | +0.419 |

The sleeve does exactly what it was built to do — it takes 6.2pp of volatility out in H1, worth
+0.571 of Sharpe, its **largest** contribution of any period. What fails is the numerator: the
book earns 8.7%/yr against SPY's 15.7%.

That 7.0pp is not the sleeve's opportunity cost and not QQQ-vs-SPY. It is the **200d gate on the
core**, which in the first half is a whipsaw tax and in the second half is insurance that pays:

| period | gated core CAGR | ungated core CAGR | d CAGR | gated Sharpe | ungated Sharpe | d Sharpe |
|---|---|---|---|---|---|---|
| H1 | 6.78% | 12.88% | **-6.11pp** | 0.822 | 1.189 | **-0.367** |
| H2 | 10.91% | 12.20% | -1.28pp | 1.018 | 0.884 | **+0.134** |

The gate sits in cash 15.2% of 2009-2016 days and 16.7% of 2017-2026 days — the *frequency* is
stable; only the *value* flips sign. Calendar years make the same point: the blend beats SPY in
**1 of 8 years to 2016** (mean gap -8.01%) and 4 of 10 from 2017 (mean -1.76%), with the worst
gaps in 2011 (-13.4pp), 2016 (-12.9pp), 2012 (-11.5pp) — the 200d-MA whipsaw years. The sleeve
is only 20.3% of the H1 mean and 19.2% of H1 variance (corr to core 0.753); it cannot be the
explanation either way.

This is a second, independent confirmation of idea 55's finding on a different book family:
the 200d gate is not the edge, and where it costs, it costs return.

## The queue's proposed repair: KILL
`50% QQQ + 10% SPY + 40% sleeve` moves H1 by **+0.007** against a bar that needs **+0.113**
(U56 @10 bps: H1 0.851 vs anchor 0.844; Sharpe 0.957 vs 0.954; CAGR -0.50pp). At 25 bps,
dH1 +0.006 and dSharpe -0.000. The entire q dial at c=0.60 spans H1 0.804 (all SPY) to 0.853
(q=0.75) — its **ceiling** is 0.104 short of the bar. There is no mix of QQQ and SPY inside a
gated core that clears H1.

## The grid (2 tuned parameters, all 192 points reported)
`c` (equity core fraction) x `q` (QQQ share of that core), x panel x cost rung x core gate.

- **4b 14/192, 4a 0/192.**
- GATE=ON: H1 spans [0.792, 0.853]; **0 of 24 (c,q) points clear the H1 bar** at either rung.
  H1 is a failing bar in 24/24 gated cells (alone 4, with CAGR 16, with DD 4).
- GATE=OFF: H1 spans [0.967, 1.189]; **24/24 clear it at 10 bps**, 20/24 at 25 bps.
- All 14 4b passes are GATE=OFF and `c=0.50`. Best cell (U56 @10 bps, c=0.50 q=1.00, i.e.
  50% QQQ + 50% sleeve, no filter): 13.0% / 1.041 / -20.1%, halves 1.166 / 0.955, OOS 1.038,
  turnover 2.4x/yr. DD slack is **0.2pp** against the -20.23% cap and q=1.00 breaks between
  10 and 25 bps.

## Rule 8 walk-forward — this is what makes it a KILL rather than a PARK
(c,q) chosen on 2009-2016, 2017-2026 read once, U56 @10 bps:

- **GATE=ON (pre-registered):** IS-Sharpe picks 30/30/40 -> OOS 11.80% / **1.134** / -14.9%.
  The anchor it was meant to improve reads OOS 1.153, so the chooser lands **-0.019 below
  doing nothing**; regret vs the OOS-best cell -0.029. The IS 4b screen is empty, so it changes
  no pick.
- **GATE=OFF (diagnostic):** IS-Sharpe picks c=0.80 -> OOS 18.44% / 0.985 / **-29.3%**, nine
  points past the 4b drawdown cap; the 4b-aware screen picks c=0.70 (-26.3%). **Neither ever
  reaches the c=0.50 cells that pass 4b**; regret -0.053 / -0.038.
- Every arm on both settings loses to the live RULES v2 book out of sample (OOS Sharpe 1.285).

So the only 4b-passing family here requires (i) flipping a third dial and (ii) a level of `c`
that no pre-registered in-sample rule selects. Recorded as a diagnostic; not proposed.

## Reporting note the record should carry
The panel axis is **degenerate** for this book: it holds only QQQ, SPY and the 9 sleeve ETFs,
all present in both universes. Max |U56 - B136| across all 96 cells is Sharpe 1.09e-04,
CAGR 8.60e-06, MaxDD 1.72e-04 — price-file rounding. B136 is not an independent confirmation
for any ETF-only book; only the 4a comparand differs. Any future ETF-only idea should state this
rather than presenting two panels as two tests.

## Caveats
Current-constituent universes (survivorship flatters every level; the c/q differences much less).
The tape is the corrected trading-day index (see the harness gate above); idea 24's published row
is not, so the two are compared across that fix rather than on identical data. QQQ's 2009-2017 run is the best
large-cap equity stretch in the sample, so "the gate cost the core 6.11pp in H1" is conditioned
on that regime.

## Verdict
**KILL** for the queue's repair and for (c,q) as the instrument. The H1 failure is diagnosed and
attributed. Rules unchanged; nothing proposed for Sunday review.
