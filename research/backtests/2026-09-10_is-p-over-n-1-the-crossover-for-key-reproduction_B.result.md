# Idea 498 — is p/n = 1 the crossover for key reproduction?  **KILL of the premise as posed.**

**Answer: no.** Out-of-fold key reproduction does not cross 0.5 at p/n = 1, p/n is not a
sufficient statistic for where it crosses, and the crossover cannot be quoted without also
stating the fold count and the ridge penalty. Lane B, 2026-09-10, 132 s, no network.

**Gate.** n = 200, full width, key = `sd`, medians over lam x K reproduce idea 483's published
triple exactly: **U56 0.9387 (p/n 0.275), B136 0.6676 (0.675), SMALL439 0.3151 (2.195)** vs its
0.939 / 0.668 / 0.315. The fast book path is gated against `engine.backtest` on 5 draws per
panel at **max |d daily return| 8.3e-17** over the evaluated window.

**1. The crossover is not at 1.** Sweeping n over 16 values x 14 (panel, width) pairs x 6 lam x 4 K x 3 keys
(16,128 grid points, all in `.grid.csv`), the interpolated p/n* at which honest reproduction
falls below 0.5 has pooled median **1.170 (IQR 0.884-1.469)** at lam <= 1, and only **36.8%** of
cells sit within +/-20% of 1.0. At the headline cell (lam 1.0, K 5, full width) it is
sd **1.111 / 1.583 / 1.466**, mu **1.095 / 1.417 / 1.373**, yS **1.048 / 1.518 / 1.218**
(U56 / B136 / SMALL439) — above 1 on every panel and every key.

**2. The fold count moves it 1.8x; n_train is the right denominator, at ~1.7 not 1.**
Pre-registered before the sweep: a pure width effect should cross at p/n_train = 1, i.e.
p/n* = (K-1)/K = 0.50..0.90, *below* 1. **Refuted in the opposite direction** — p/n* *rises*
with K (0.76-0.91 at K=2 to 1.19-1.78 at K=10), median spread across K **1.792x**. Rescaling to
the rows the fold actually fits on flattens that to **1.195x**, so n_train is the correct
denominator, but the level is **p/n_train* = 1.72 (IQR 1.46-1.83)**, and **76.4%** of cells land
within +/-20% of 1.8. Equivalently, in draws: honest reproduction needs **n ~ 0.7-1.1 x p**.

**3. p/n is not a sufficient statistic.** Within a *single* panel, configurations at the same
p/n differ in R2_oof by a **median 0.812 and up to 2.363** (U56, p/n ~ 1: R2_oof -1.542 at
p=25/n=30 vs +0.822 at p=55/n=60). That spread is wider than the whole meaningful range of an
R2, so a p/n number alone cannot say whether a control is still a control.

**4. The penalty dominates the location, as it dominated idea 483's inference.** Median p/n*
across panels moves **0.14 (lam=100) to 1.42 (lam=1e-3, K=5)**, a ~10x range from a dial the
record does not publish. 5.6% of cells never cross 0.5 anywhere in the swept range.

**5. The mechanism is width-vs-sample, not column space.** `mu` (mean member annualised return)
is **exactly** linear in the full-width membership matrix — ceiling R2_oof **0.9994-1.0000** at
n=1200, lam<=1 — while the record's actual key `sd` is nonlinear, ceiling **0.953-0.968**. The
two cross at essentially the same p/n* (full-width medians at lam <= 1: mu 1.230, sd 1.095). So the collapse is a
sample-size-against-width effect, not "the key was never recoverable"; the 3-5% nonlinearity
gap in `sd` is not what puts SMALL439 at 0.315.

**6. Rule 8 (fit on the first half, read the second once).** Honest folding changes the
inference, not the book — the same conclusion idea 483 reached. Median OOS Sharpe, OOF-fitted
vs IS-fitted selector: U56 **1.1458 / 1.1458**, B136 **1.0328 / 1.0358**, SMALL439 **0.4192 /
0.5823**; vs live **RULES v2 OOS 1.1798 / 0.9844 / 0.5770** (CAGR 8.93% / 7.14% / 4.08%, MaxDD
-12.05% / -12.24% / -11.74%) and **SPY OOS 0.8257 / 0.8340 / 0.8577** (CAGR 14.81% / 14.99% /
15.92%, MaxDD -33.72%). The OOF selector beats RULES v2 on Sharpe on 1 of 3 panels and SPY on
2 of 3, in both cases at 2.1-3.9x the live book's drawdown (OOS MaxDD -26.1% / -27.9% / -45.1%).
Selector agreement does **not** track p/n: 24/24 cells agree at SMALL439 p/n 4.39, 8/24 at
B136 p/n 1.35.

**7. KEEP paths.** 3,600 draw books (1,200 x 3 panels), full sample + both halves at 10 bps:
**4a 0/3600, 4b 0/3600, both 0/3600.** Nothing to promote. RULES.md, PROTOCOL.md, scan.py,
bot.py and baseline.py untouched.

**PROPOSAL for Sunday review (not applied here).** Where the record quotes a wide control's
honest reproduction, publish it as **(p, n, K, lam)**, not as p/n — and if one number is wanted,
use **p / n_train = p / (n(1-1/K))** against a **1.7** line, not p/n against 1. The p/n = 1
shorthand in the queue is wrong by the fold count in one direction and by the penalty in the
other.

**SURVIVORSHIP** (rule 9 / idea 54): B136 and the sub-$2B panel are current constituents only;
this is a within-panel statement about fitted controls, so the screens' differential affects the
cross-panel *levels* quoted above, not the crossover comparison.

Files: `.grid.csv` (16,128 sweep points), `.crossover.csv` (1,008 interpolated p/n*),
`.ceiling.csv`, `.walkforward.csv`, `.keeppaths.csv`, `.gate.csv`, `.console.txt`.
