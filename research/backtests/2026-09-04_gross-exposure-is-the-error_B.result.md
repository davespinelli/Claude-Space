# Idea 66 — gross-exposure-is-the-error — **KILL** (lane B, 2026-09-04)

Script: `research/backtests/2026-09-04_gross-exposure-is-the-error_B.py`
Console: `research/backtests/2026-09-04_gross-exposure-is-the-error_B.console.txt`

## The question

Idea 63 diagnosed the standing 4b failure as **75%-gross cash drag** (the books beat SPY
only in 2018 and 2022; the concentration factor explained R² 0.011–0.018 of H2 excess),
and repaired it by bolting a 25% passive core onto the book. If the disease is cash drag,
the direct cure is to stop holding cash. The queue asked: *"If 100% gross does what the
25% core does, the sleeve is a detour."*

## Design

- Books, pre-chosen from prior ideas and not tuned here: `ew-band3` (idea 57's candidate —
  equal-weight every eligible name, eligible = `vol20 < 0.60` and a 3% hysteresis band
  around the 200d MA), `top20-200d` (idea 2/55's candidate), `top20-band3` (the same
  ranked book on the band gate, so the gross effect can be read independently of gate).
- **2 tuned parameters:** gross `g ∈ {0.75, 0.80, 0.85, 0.90, 0.95, 1.00}` and core
  fraction `b ∈ {0.00, 0.25}` (`b` is a fraction *of gross*, so `g=0.75, b=0.25`
  reproduces idea 63 exactly). **All 36 arms × 6 cost levels reported**, both universes.
- Costs 5/10/15/20/25/50 bps (10 bps is the verdict cost); weekly, t+1, long-only, no
  leverage — `g=1.00` means fully invested, never margined. Analytic cost identity asserted
  against a real `cost_bps=10` engine run (max |diff| ~1e-17).
- Rule 8 walk-forward with two selection rules fixed before any OOS number was read, plus
  the OOS metrics of **every** grid point reported separately.
- Trading-day index confirmed (251 rows in 2018, 252 in 2024) — idea 38's fix is in.

## Result 1 — gross is an *exact* lever, not an edge

Against the same book at `g=1.00`, every arm has **corr 1.0000, beta = g to three
decimals, and dSharpe = 0.000**. CAGR and MaxDD scale linearly and turnover with them:

| universe.json, `ew-band3`, 10 bps | g=0.75 | g=0.85 | g=0.95 | g=1.00 |
|---|---|---|---|---|
| CAGR | 11.3% | 12.8% | 14.3% | 15.1% |
| **Sharpe** | **1.136** | **1.136** | **1.136** | **1.136** |
| MaxDD | −15.1% | −17.1% | −19.0% | −19.9% |
| turnover | 4.9x | 5.6x | 6.1x | 6.4x |

Sharpe slope d(Sharpe)/d(gross) is −0.000 / +0.000 / +0.001 for the three books on
universe.json and −0.001 / +0.008 / +0.007 on the broad list — indistinguishable from zero
everywhere. This was mechanically expected but had never been verified; it now is.

## Result 2 — gross cannot move any Sharpe bar, so it cannot fix the H2 shortfall

The bar idea 63 set out to repair is `top20`'s **broad H2 Sharpe of 0.814 against SPY's
0.837**. Across the whole gross sweep on universe_broad.json at 10 bps:

| `top20-200d`, core=0 | g=0.75 | g=0.80 | g=0.85 | g=0.90 | g=0.95 | g=1.00 |
|---|---|---|---|---|---|---|
| **H2 Sharpe** | 0.814 | 0.814 | 0.814 | 0.815 | 0.815 | 0.815 |
| MaxDD | −20.1% | −21.3% | −22.5% | −23.8% | −25.0% | −26.2% |
| 4b verdict | KILL (H2) | KILL (H2,DD) | KILL (H2,DD) | KILL (H2,DD) | KILL (H2,DD) | KILL (H2,DD) |

**Raising gross moves H2 by 0.001 and the drawdown by 6.1pp.** The same arm with the 25%
SPY core reads H2 = 0.861–0.862 at *every* gross. So the sleeve is **not** a detour: it is
the only one of the two interventions that changes anything a Sharpe bar can see, because
it changes the *composition* of the return stream, not its scale. "75% gross is the error"
is arithmetically true about CAGR and simply cannot be the explanation of an H2 *Sharpe*
shortfall.

## Result 3 — at matched investment the core is worse, and the difference is noise

Head-to-head at `g=1.00` (both fully invested; one holds a quarter in SPY), 10 bps:

| | with 25% SPY core | all-active | |
|---|---|---|---|
| universe.json `ew-band3` | 15.2% / 1.106 / −21.7% | 15.1% / **1.136** / **−19.9%** | core is worse on both axes |
| broad `ew-band3` | 15.0% / 1.040 / −23.3% | 14.8% / **1.064** / **−22.1%** | core is worse on both axes |
| broad `top20-200d` | 17.0% / **0.986** / −26.3% | 17.4% / 0.960 / **−26.2%** | core buys +0.026 Sharpe |

Paired daily differences (core minus all-active, same days) at 10 bps: **+0.23%/yr t +0.44**
(`ew-band3`), **−0.53%/yr t −0.70** (`top20-200d`), **−0.50%/yr t −0.66** (`top20-band3`)
on universe.json. Statistically zero in both directions. The core helps only the one book
and universe where the ranked book's H2 was already the binding failure, and there it
still fails 4b on drawdown.

## Result 4 — rule 8: both pre-registered rules overshoot on gross and fail OOS

IS bars (2009–2016): Sharpe > 0.899, MaxDD ≥ −13.2%, CAGR ≥ 10.5%. OOS bars (2017–2026):
Sharpe > 0.884, MaxDD ≥ −20.2%, CAGR ≥ 10.9%. SPY OOS 15.5% / 0.884 / −33.7%; RULES v1 OOS
7.8% / 0.751 / −13.8% (primary) and 6.0% / 0.581 / −21.2% (broad).

| rule | universe.json pick | OOS | broad pick | OOS |
|---|---|---|---|---|
| R1 max IS Sharpe | `ew-band3 g=1.00 b=0.25` | 16.7% / 1.174 / **−21.7%** FAIL (MaxDD) | `ew-band3 g=1.00 b=0.00` | 14.9% / 1.073 / **−22.1%** FAIL (MaxDD) |
| R2 4b-aware, max IS CAGR | `ew-band3 g=0.95 b=0.25` | 15.8% / 1.174 / **−20.6%** FAIL (MaxDD) | `ew-band3 g=0.95 b=0.00` | 14.2% / 1.073 / **−21.1%** FAIL (MaxDD) |

**All four picks fail OOS on drawdown, by 0.4–1.9pp.** The mechanism is worth recording:
because Sharpe is exactly flat in `g`, no Sharpe-based rule can select gross at all — R1's
choice is decided in the 4th decimal — and R2, which *is* drawdown-aware, still overshoots
because the 2009–2016 window contains no 2020 or 2022, so its −13.2% in-sample cap is loose
relative to the −20.2% the out-of-sample period actually enforces. **Gross is not a
selectable parameter; it is a risk-budget decision, and in-sample drawdown is not a safe
way to set it.**

## Result 5 — the one arm worth parking (PARK, not KEEP)

`ew-band3, g=0.90, core=0.00` clears all five 4b tests on **both** universes at **5, 10, 15,
20 and 25 bps**, and clears the OOS 4b bars on both (universe.json 15.2% / 1.234 / −18.0%;
broad 13.4% / 1.073 / −20.0%):

| 10 bps | full | halves | OOS | turn |
|---|---|---|---|---|
| universe.json | 13.5% / 1.136 / −18.0% | 1.113 / 1.160 | 1.234 | 5.8x |
| broad | 13.4% / 1.064 / −20.0% | 1.164 / 0.971 | 1.073 | 6.2x |

(Its full-sample MaxDD and its OOS MaxDD are the same number on both lists — the deepest
episode is in 2020/2022, inside the OOS window, so the drawdown figure is not an artefact
of the pre-2017 sample.)

That is a wider cost survival than idea 63's core arm (which needed QQQ and died above 25
bps) with one fewer moving part. It is **PARK, not KEEP**, for the reason in Result 4:
rule 8 does not and cannot select it — `g=0.90` is simply the largest gross whose linearly
scaled drawdown still fits under the broad list's −20.2% cap, which is a statement about
where the cap sits, not evidence of an edge. Its Sharpe is identical to `g=0.75`'s.

## Verdict

**KILL.** Gross exposure is not the error. It is a pure lever: it buys CAGR and sells
drawdown in fixed proportion, moves no Sharpe bar on either universe, and cannot be chosen
by any in-sample rule. Idea 63's cash-drag diagnosis explains a CAGR gap, not the H2
Sharpe gap it was invoked for; the 25% core survives this test as the only intervention of
the two that touches a Sharpe bar, but only on the broad ranked book and not enough to pass
4b there. **Rules unchanged.**

## Caveats

- **SURVIVORSHIP:** both lists are current constituents, so absolute CAGR/Sharpe are
  optimistic. The gross-vs-gross comparisons that answer this question are far less
  exposed — every arm holds the same names on the same days and differs only in scale.
- No leverage was tested. `g=1.00` is fully invested; the linearity result should not be
  extrapolated above 1.00, where financing cost and margin mechanics enter.
- Turnover scales with gross too (4.9x → 6.4x on `ew-band3`), so the cost sensitivity in
  the grid already includes the extra trading the higher gross causes.

## Queued follow-ups

- **69. risk-budget-as-an-explicit-rule** — since gross is an exact lever with zero Sharpe
  content, RULES should state gross as a drawdown budget, not a number. Test a rule that
  sets `g` from a target MaxDD (e.g. scale so trailing 3-year MaxDD ≈ 60% of SPY's) and
  check whether it beats a fixed `g` out-of-sample, given Result 4's finding that IS
  drawdown underestimates OOS.
- **70. what-actually-moves-H2** — Results 2 and 3 leave the broad H2 shortfall of the
  ranked book unexplained: gross does nothing and the SPY core does +0.047 with t < 1.
  Decompose broad H2 excess return by sector and by the top-10 mega-caps' weight, and test
  whether the shortfall is a small number of names or a regime.
