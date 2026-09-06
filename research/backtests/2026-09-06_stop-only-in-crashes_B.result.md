# Idea 75 — stop-only-in-crashes (lane B, 2026-09-06)

**Verdict: KILL, and the queue's premise is REFUTED with the sign reversed. The trailing
stop's damage is NOT whipsaw in trending markets — it is concentrated in exactly the crash
regime the conditional arming keeps. Splitting (stop minus its own control) by SPY's 200d
regime, the stop loses a median 0.66–2.00 pp/yr annualised on SPY-below-200d days against
0.00–0.93 pp/yr on SPY-above-200d days, and at the two deepest stops the trending-market
damage is essentially zero (−0.04 and −0.005 pp/yr) while the crash damage is −1.03 and
−0.66. So arming only in crashes throws away 52–66% of the firings and recovers a median
+0.0007 Sharpe out of the −0.0108 the always-on stop gives up — about 6% of the loss. No
armed arm passes a KEEP path its own no-stop control does not already pass (0 of 144), and
rule 8 picks a stop in 10 of 12 cells for a mean OOS regret of −0.0083.**

Script: `2026-09-06_stop-only-in-crashes_B.py`. 144 stop arms + 12 matched no-stop controls,
all reported. Exactly TWO tuned parameters: stop depth S ∈ {10, 15, 20, 25}% and arming
regime ARM ∈ {always, spy200, breadth20}. Panel {u56, broad}, book {v1, top20, ew-band3},
cost {10, 25 bps} and cooldown (fixed 0) are reported at every value and never selected on.
Idea 94's module is imported, not re-implemented.

## 0. Reproduction — exact
With `stop=None` this run's simulator equals `engine.backtest` at **max|diff| = 0.000e+00**.
With `ARM=always` it equals idea 94's `run_stop(cooldown=0)` at **max|diff| = 0.000e+00** on
returns and turnover at all four depths, with **identical firing counts**. The disarmed days
still track the trailing high — arming gates the *trigger*, not the state — so the always-on
arm is a strict special case, not a re-parameterisation.

## 1. Regime coverage (post-warm-up, 4,439 days)
| panel | arm | armed frac | days | IS frac | OOS frac |
|---|---|---|---|---|---|
| u56 / broad | always | 1.000 | 4439 | 1.000 | 1.000 |
| u56 / broad | spy200 | 0.171 | 757 | 0.177 | 0.165 |
| u56 | breadth20 | 0.086 | 380 | 0.031 | 0.131 |
| broad | breadth20 | 0.081 | 360 | 0.025 | 0.127 |

`breadth20` uses an **expanding** (min 3y) 20th percentile, so it has no look-ahead; the price
of that is an IS/OOS coverage asymmetry (3.1% of IS days armed vs 13.1% of OOS days). Stated,
not corrected — correcting it would require a fixed threshold chosen on the full sample.

## 2. The premise, measured (the decisive table)
Annualised return of (stop arm − its own no-stop control), split by the SPY<200d regime,
10 bps, median over the 6 (panel × book) cells at each (arm, depth):

| arm | depth | med Δ in CRASH regime | >0 | med Δ in TREND regime | >0 | med Δ2020 | med Δ2022 |
|---|---|---|---|---|---|---|---|
| always | 0.10 | **−1.234 pp/yr** | 1/6 | −0.929 pp/yr | 1/6 | −1.206 | +0.863 |
| always | 0.15 | **−1.163** | 0/6 | −0.336 | 1/6 | −1.607 | −0.738 |
| always | 0.20 | **−1.027** | 0/6 | **−0.038** | 0/6 | −1.436 | −0.400 |
| always | 0.25 | **−0.664** | 0/6 | **−0.005** | 1/6 | −1.898 | −0.226 |
| spy200 | 0.10 | −1.821 | 1/6 | −0.262 | 2/6 | −1.180 | −0.327 |
| spy200 | 0.15 | −1.478 | 0/6 | −0.111 | 0/6 | −1.549 | −1.025 |
| spy200 | 0.20 | −1.051 | 0/6 | −0.030 | 0/6 | −1.367 | −0.420 |
| spy200 | 0.25 | −0.664 | 0/6 | +0.000 | 3/6 | −1.894 | −0.226 |
| breadth20 | 0.10 | −2.001 | 1/6 | −0.132 | 1/6 | −1.103 | +0.065 |
| breadth20 | 0.15 | −1.508 | 0/6 | −0.070 | 0/6 | −1.549 | −0.868 |
| breadth20 | 0.20 | −0.941 | 0/6 | −0.017 | 0/6 | −1.340 | −0.510 |
| breadth20 | 0.25 | −0.695 | 0/6 | +0.000 | 1/6 | −1.876 | −0.226 |

The crash-regime column is negative in **69 of 72** cells (3 positives, all at S=0.10) and its
magnitude is **3.5x** the trending-regime column at S=0.15, **27x** at S=0.20 and **133x** at
S=0.25 (always-on rows; 1.3x at S=0.10, the depth that fires 53x/yr and is mostly cost).
**The stop loses money precisely where
the queue said it earns its keep.** Idea 9's own year cut said as much and was read backwards:
2020 — the deepest crash in the sample — is the stop's worst year here too (median −1.1 to
−1.9 pp in every one of the 12 rows), and 2020 is a *crash*, not a whipsaw. What the queue
read as "whipsaw damage in trending markets" is, at the depths that matter, a rounding error.

Mechanism, consistent with idea 96 section 3: a trailing stop fires into a short-term reversal,
and crashes are where reversals are largest and most frequent, so the crash regime is where the
instrument is dearest — not cheapest.

## 3. H1 — does arming recover the Sharpe the always-on stop gives up? NO
Paired against the SAME (panel, book, cost, depth) always-on arm, 48 pairs each:

| arm | beats always-on | med ΔSharpe vs always | beats its control | med ΔSharpe vs control | firings kept |
|---|---|---|---|---|---|
| always | — | 0.000 | 2/48 | −0.011 | 100% |
| spy200 | 30/48 | **+0.0007** | 2/48 | −0.010 | 47.8% |
| breadth20 | 25/48 | **+0.0006** | 3/48 | −0.009 | 34.4% |

Arming is a directionally correct but **quantitatively empty** improvement: it removes half to
two thirds of the trades and buys back ~6% of the always-on stop's Sharpe loss. Mean ΔSharpe vs
always is +0.009 with a max of +0.066 and a min of −0.004 — the mean is carried by a handful of
`v1`/25 bps cells where the control itself is near-degenerate. The armed stop still loses to
simply not stopping in **46 of 48** cells.

## 4. H2 — priceability against the static-gross lever (idea 66): NO improvement
Of 144 arms, 63 buy any drawdown at all; of those, the share priced at or below the same book's
constant-gross lever is **12/22 (always), 13/20 (spy200), 12/21 (breadth20)** — median paid
0.586 / 0.462 / 0.359 pp of CAGR per pp of MaxDD against a lever price of ~0.686–0.688. Arming
lowers the *average* price only because it also lowers the *quantity*: median ΔMaxDD vs control
is 0.000 pp for both armed regimes. There is no cell where the armed stop buys materially more
drawdown than the always-on one; the MaxDD delta between armed and always-on is 0.000 pp at the
median. **The instrument is not made cheaper by arming it, it is made smaller.**

## 5. KEEP paths — 0 of 144 arms earns a pass its control does not already have
At 10 bps, 27 of 72 arms pass 4a and 29 of 72 pass 4b — and **every one of those is inherited**:
`arms passing 4b whose own control FAILS 4b: 0`, `arms passing 4a whose own control FAILS 4a: 0`.
The passing books are idea 2's `top20` and idea 57's `ew-band3`, which are already 4b KEEPs; 3 of
the 6 controls pass 4b unaided. Controls at 10 bps:

| panel | book | CAGR | Sharpe | MaxDD | H1 / H2 | OOS Sharpe | fails 4a | fails 4b |
|---|---|---|---|---|---|---|---|---|
| u56 | v1 | 6.5% | 0.664 | −13.8% | 0.641 / 0.688 | 0.747 | H1,H2 | H1,H2,OOS,CAGR |
| u56 | top20 | 12.7% | **1.092** | −18.3% | 1.088 / 1.102 | 1.168 | DD | **passes** |
| u56 | ew-band3 | 11.3% | **1.135** | −15.1% | 1.113 / 1.158 | 1.232 | DD | **passes** |
| broad | v1 | 6.4% | 0.635 | −21.2% | 0.756 / 0.532 | 0.576 | H1,H2 | H1,H2,OOS,DD,CAGR |
| broad | top20 | 13.1% | 0.957 | −20.1% | 1.125 / 0.811 | 0.892 | passes | H2 |
| broad | ew-band3 | 11.1% | **1.062** | −16.8% | 1.163 / 0.968 | 1.071 | passes | **passes** |

The best armed arm anywhere (u56/ew-band3, S=0.10, spy200: 10.7% / 1.123 / −14.8%, OOS 1.228)
sits **below its own control** on Sharpe (1.135), CAGR (11.3%) and OOS Sharpe (1.232) — it clears
4b only because the book underneath it does.

## 6. Rule 8 walk-forward — (S, ARM) on 2009–2016, 2017–2026 read once
| panel | book | cost | pick | IS Sharpe | OOS CAGR | OOS Sharpe | OOS MaxDD | ctrl OOS | regret | best OOS |
|---|---|---|---|---|---|---|---|---|---|---|
| u56 | v1 | 10 | 0.10/breadth20 | 0.558 | 7.5% | 0.729 | −13.8% | 0.747 | **−0.018** | none |
| u56 | v1 | 25 | 0.10/breadth20 | 0.209 | 3.5% | 0.378 | −14.7% | 0.399 | −0.022 | none |
| u56 | top20 | 10 | 0.20/always | 0.995 | 14.0% | 1.160 | −17.0% | 1.168 | −0.008 | none |
| u56 | top20 | 25 | 0.25/spy200 | 0.860 | 12.5% | 1.034 | −18.5% | 1.050 | −0.015 | none |
| u56 | ew-band3 | 10 | 0.20/always | 1.023 | 12.1% | 1.211 | −14.8% | 1.232 | **−0.021** | none |
| u56 | ew-band3 | 25 | 0.25/spy200 | 0.943 | 11.5% | 1.142 | −15.4% | 1.159 | −0.017 | none |
| broad | v1 | 10 | 0.10/always | 0.723 | 6.0% | 0.586 | −20.4% | 0.576 | +0.010 | 0.10/always |
| broad | v1 | 25 | 0.10/always | 0.313 | 1.2% | 0.161 | −26.1% | 0.155 | +0.006 | 0.10/spy200 |
| broad | top20 | 10 | none | 1.044 | 12.5% | 0.892 | −20.1% | 0.892 | 0.000 | none |
| broad | top20 | 25 | none | 0.893 | 10.1% | 0.743 | −20.2% | 0.743 | 0.000 | none |
| broad | ew-band3 | 10 | 0.20/always | 1.054 | 10.8% | 1.068 | −16.7% | 1.071 | −0.003 | 0.10/breadth20 |
| broad | ew-band3 | 25 | 0.25/always | 0.980 | 10.0% | 0.984 | −17.5% | 0.994 | −0.011 | 0.10/breadth20 |

Selector takes a stop in **10/12** cells and an *armed* stop in **4/12**; mean OOS regret vs the
no-stop control **−0.0083**, median −0.0094, negative in 8/12. The best available OOS arm is the
**no-stop control in 8/12** cells. OOS benchmarks over the same window: **RULES v1 baseline
7.7% / 0.747 / −13.8% (u56), 5.9% / 0.576 / −21.2% (broad); SPY 15.5% / 0.882 / −33.7%.**
The selected arms beat the live baseline's OOS Sharpe in 5/6 cells at 10 bps and beat SPY's in
4/6 — but so do their controls, by more. This is the 15th instance in the record of a dial rule
losing to doing nothing.

## 7. What this changes
- **Idea 9 / 94 / 96's stop KILL is confirmed a third time**, now on the one axis that was left
  open, on a harness reproducing idea 94 to zero.
- **The queue's stated mechanism is wrong, and the correction is the finding worth carrying:**
  the per-name trailing stop is dearest in crashes, not in trends. Any future proposal to arm a
  fast instrument "only when it matters" inherits this result — arming it in the crash regime
  concentrates it into its own worst regime. Idea 6's KILL of a breadth-triggered sleeve and
  idea 40's KILL of book-level drawdown control now have a mechanism in common with this one.
- **No rules change.** Nothing here is a KEEP candidate under 4a or 4b.

## Caveats
Current-constituent survivorship on both panels flatters the always-invested control and so runs
*with* this conclusion — it makes the stop's measured loss an upper bound on its value, not a
lower one. MaxDD is one number off one path; section 4 does not treat sub-1-pp drawdown deltas as
real. `breadth20`'s expanding threshold gives it 4x more armed days OOS than IS (section 1), which
weakens the rule-8 evidence *for* that regime specifically — it does not weaken the full-sample
premise test in section 2, which uses `spy200` for the split in every row. The 2009–2016/2017–2026
split, the three book definitions and the depth grid are inherited from idea 94 on overlapping
data, so the walk-forward validates the ARMING comparison, not those constants. Idea 38's
calendar-day index is still unfixed for `u56`/`broad`; it applies identically to arm and control in
every comparison here. No file outside `research/` was modified.
