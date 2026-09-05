# Memo — idea 95: what RULES may and may not say about the 0.60 vol threshold

1. `EWall + vol60-dg` survives its own threshold sweep unbeaten: with theta swept over
   {0.40,0.50,0.60,0.80,1.00} × {dg,rw} on both large-cap lists at 10 and 25 bps, **0.60/dg is one
   of only two of the 40 points passing 4b in all four (universe × cost) cells** — u56 11.6%/1.133/
   -16.9% (halves 1.156/1.113, OOS 1.186), broad 12.4%/1.138/-18.7% (halves 1.255/1.027, OOS
   1.122), 1.4×/yr turnover — the other being `0.50/rw` at 2.4×/yr. No re-tuning is warranted.
2. But 0.60 is **not derived**: Sharpe moves 0.009-0.074 across the whole axis, the ungated
   control sits inside that range in 7 of 8 cells, and every one of the 40 arms *loses* CAGR to
   its own control (-0.25..-4.04 pp/yr, |t| ≥ 2 in only 13, and 1.53-2.00 at 0.60).
3. Rule 8 cannot set it: **0 of 8 pre-registered walk-forward selections pick 0.60**; u56 picks
   1.00 (OOS rank 7-8 of 10, losing to the ungated control) and broad picks 0.40 — opposite
   endpoints — and ρ(IS,OOS Sharpe) flips sign, **-0.70/-0.64 on u56 against +0.59/+0.94 on broad**.
4. The 4b window in theta is closed on the left by the CAGR floor (0.40 fails it) and on the right
   by the MaxDD cap (0.80/1.00 fail it); no Sharpe bar ever binds. The threshold is a risk-budget
   *location*, exactly as idea 84/90 found for gross.
5. What the gate does earn: at matched drawdown it beats the static-gross lever in **38 of 40**
   points, by up to +3.85 pp of CAGR, pricing at 0.257-0.318 pp/pp at 0.60 against ladder slopes
   of 0.558-0.595 — about half the cost of simply holding less.
6. Adoption is therefore **unblocked on the numbers and constrained on the wording**: RULES may
   state the constant, must not call it a threshold, an optimum, or a volatility filter.

**Exact RULES wording, if the Sunday review adopts the book:**

> **Book.** Hold every name in the universe at equal weight, 75% gross, rebalanced weekly at
> Friday's close and executed at the next session's close. There is no ranking and no
> position-count limit.
>
> **Risk gate.** A name whose 20-day realised volatility (annualised) is 0.60 or higher is not
> held; its weight goes to cash and the rest of the book is **not** rescaled, so the book
> de-grosses in high-volatility regimes.
>
> **On the 0.60 constant.** 0.60 is a *declared risk-budget setting, not a fitted or optimal
> value*. Swept over 0.40-1.00 on two large-cap universes at 10 and 25 bps it moves Sharpe by at
> most 0.074 and never significantly; it sets the book's drawdown and return level, monotonically,
> and nothing else. Values below ~0.50 breach the CAGR floor and values above ~0.60 breach the
> drawdown cap of PROTOCOL 4b. It may be re-set only as a stated change to the risk budget, never
> on backtested performance — a walk-forward chose it in 0 of 8 cells and chose opposite ends of
> the range on the two universes.
>
> **Universe clause** (ideas 39/49/55, unchanged): this book is validated on large-cap
> current-constituent lists only and fails on the sub-$2B panel; it must not be described as a
> general rule.
