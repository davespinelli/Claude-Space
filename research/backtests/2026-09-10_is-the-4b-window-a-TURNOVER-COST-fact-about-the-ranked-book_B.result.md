# Idea 403 — is the 4b window a TURNOVER-COST fact about the ranked book?  (lane B, 2026-09-10)

**VERDICT: SPLIT — CONFIRMED IN THE SLOPE, REFUTED IN THE LEVEL.  No KEEP, no book promoted, no
RULES change.  RULES.md / PROTOCOL.md / scan.py / bot.py / baseline.py untouched.**

Script `2026-09-10_is-the-4b-window-a-TURNOVER-COST-fact-about-the-ranked-book_B.py`; console,
`.grid.csv` (4 224 arm-rows), `.windows.csv` (384 window measurements), `.matched.csv`,
`.walkforward.csv`, `.keeppaths.csv` committed beside it.

## Corpus and tuned parameters
11 f-points (0.00–0.50, uniform, step 0.05) x 8 lambdas x 2 panels x 2 base books x 2 sleeve sets
= 704 simulations, read at 6 cost rungs off the exact rung identity = **4 224 arm-rows**.
Exactly two tuned parameters, both swept in full and every point reported: **f** (the sleeve
fraction, the dial whose window is measured) and **lambda** (partial rebalancing applied to the
BASE leg only — the sleeve's own trading is untouched, which is the queue's "rather than of the
sleeve" clause made operational).  Panels, base books, sleeve sets, cost rungs, both selectors and
both KEEP paths are reported axes and are never selected on.

## Gates (all pass, before any new number was read)
* **G1** `H.run` with every instrument off vs `engine.backtest`: max|d| **0.000e+00** on both panels.
* **G2** the rung identity `r(c) = r(0) − turnover·c/1e4` vs a live 25 bps run: **0.000e+00** on
  both panels.  This is what licenses reading six rungs off one simulation, and it is also the
  reason the question is answerable at all (see below).
* **G3** reproduction of idea 138's committed `.grid.csv` at lambda = 1 on the 160 shared rows,
  with per-panel tolerances stated in advance: **broad 2.220e-16** (its cache is written weekly on
  Fridays and is untouched since idea 138 ran), **u56 3.743e-03** (`data/prices.csv` is rewritten
  daily and now carries three trading days idea 138 could not see — idea 137's drift allowance).
  **4b verdict agreement 160/160.**
* **G4** base turnover strictly monotone in lambda in every (panel, book).

## Premise check — half of the queue's own description is wrong
Read back off idea 138's committed grid: "EMPTY in exactly the two broad/TOP20 @25bps cells" is
**EXACT** (2 of 16).  "**4–7 grid points wide on every EWall cell**" is **NOT**: EWall cells run
**2–5** points, and the widest window in the record (7 points) belongs to **u56/TOP20 @10bps — the
ranked book itself**, not to EWall.  The queue's sentence attributes the wide windows to the book
that does not have them.

## The mechanism the question turns on
No instrument here reads equity, so turnover reaches a return series **only** through cost:
`r(c) = r(0) − turnover·c/1e4`, exact (G2).  A genuine turnover-cost fact must therefore be a
single function of the **drag** `D = base_turnover · c/1e4`, whichever route produced D.  Two routes
are available: the **cost route** (vary the rung at lambda = 1 — changes drag and nothing else) and
the **lambda route** (vary lambda at a fixed rung — changes drag *and* the base book's path).

## CONFIRMED — the slope.  Width is a clean function of drag, and both routes agree.
* Within every one of the 8 (panel, book, sleeve) cells, **rho(width, drag) = −0.854 … −0.960**.
* **238 matched-drag pairs** within 25 % on drag: the two routes give **exactly equal width in
  181/238**, median residual **0.0000**, mean **+0.0055**, and disagree by more than one grid step
  in only **23/238**.
* The queue's headline case is confirmed outright: cutting broad/TOP20's base turnover from
  **13.18 → 7.62 x/yr** (lambda 1 → 0.15) **OPENS both empty @25bps windows** to 3–4 grid points;
  at lambda = 0.06 (5.24 x/yr) they are 5 points wide, and the worst-of-five margin moves monotonically
  from **−0.0430 to +0.0190**.  The binding bar on the empty side is **H2**, not the CAGR floor.
* The dial's signature is exactly the cost signature: over the lambda ladder the median within-cell
  rho(width, base_to) is **+0.577 at 0 bps** (and width never moves — range 0.000) but
  **−0.826 at 25 bps** and **−0.923 at 50 bps**.  A dial that does nothing at zero cost and
  everything at high cost is a cost dial.

## REFUTED — the level, and the sign.  The cross-cell ordering is not turnover.
* Pooled over idea 138's 16 native cells, **rho(width, base_to) = −0.127** — nothing.
* **The base book with 11–16x the turnover has the WIDER window**: native mean width TOP20
  **0.156** vs EWall **0.125**; at 0 bps TOP20 **0.325** vs EWall **0.200**; at matched turnover
  @10bps TOP20 **0.288** vs EWall **0.150**.  The intercept runs *opposite* to turnover.
* **The spread does not vanish at zero cost**: width sd across the 8 native cells is **0.0835 at
  0 bps** — *larger* than the **0.0641 at 25 bps** — and 0 of 8 cells is empty there.  The two
  cells idea 138 found empty are the **widest in the corpus at 0 bps** (7 and 6 points).
* The **panel** gap survives matching (@25bps matched-turnover u56 **0.188** vs broad **0.138**),
  which is idea 137's regime residual showing up on a second statistic.
* So the correct model is **width ≈ intercept(panel, book, sleeve) − slope · drag**, with the two
  terms carrying **opposite signs in turnover**.  A screen that ranked candidate cells by base
  turnover alone would rank them **backwards**.

## Honest limitation on A3 (matched turnover)
lambda can only *lower* turnover, and it bottoms out at 3.78 (u56) / 5.24 (broad) x/yr against
EWall's 0.83 / 0.87 — smoothing a top-20 basket spreads its trades but does not remove the
entries and exits.  **T\* was bracketed in only 12 of 48 cells**; the rest are clamped at the low
end and flagged in `.matched.csv`.  A3 is therefore *not* a clean match, and the arbiter of the
turnover-cost question is **A4**, where the cost rung supplies the range lambda cannot reach.

## Rule 8 (PROTOCOL 8) — (f, lambda) chosen on 2009–2016 alone, 2017–2026 read once
| selector | picks | OOS Sharpe | OOS CAGR | OOS MaxDD | beats SPY | beats RULES v2 | clears OOS 4b bars |
|---|---|---|---|---|---|---|---|
| S0 (IS Sharpe) | f = 0.50 in 34/48, lambda = 0.06 in 33/48 | **1.2065** | 10.35 % | −14.10 % | 46/48 | 27/48 | 17/48 |
| S1 (IS-4b screened) | f 0.20–0.50, lambda = 0.06 in 32/48 | **1.1814** | 11.17 % | −15.59 % | 46/48 | 18/48 | **29/48** |
| SPY (OOS) | — | 0.8789 | 15.38 % | −33.72 % | — | — | — |
| RULES v2 (OOS, cost-matched) | — | 1.1783 | 8.57 % | −12.17 % | — | — | — |

The chooser buys the turnover instrument: **lambda < 1 in 20/24 TOP20 cells** and, less expectedly,
in **12/24 EWall cells** too (prediction P5 was half wrong — even a 0.83x/yr book pays to smooth).

**Window transfer:** the IS window's width *ordering* transfers (Spearman(IS width, full width)
**+0.794**) but its *location* does not — over the 346 cells where both windows are non-empty they
**overlap in 346/346**, the full-sample window is **nested inside the IS window in 215/346**, and the
IS window's lower edge sits at or below the full window's in **344/346** (mean 0.045 vs 0.173).
The IS window is a **superset, not a forecast**: idea 128/138's caveat — an IS drawdown cap is
measured on a window that cannot express a deep drawdown — showing up as window *location*.

## KEEP paths (PROTOCOL 4, both evaluated on every arm-row)
**4a** vs the LIVE RULES v2 book, cost-matched: **55 / 4 224** — and **0 at 25 and 50 bps**.
**4b** vs SPY on all five bars: **1 770 / 4 224** (402/383/346/318/217/104 at 0/5/10/15/25/50 bps).
**BOTH: 12 / 4 224, and all twelve sit at 0 and 5 bps — below PROTOCOL's own 10 bps rung.
At 10 bps and above, BOTH = 0.**  Nothing is promoted and no memo is filed.

## Predictions, scored
P1 **WRONG** (I predicted the empty windows survive at 0 bps; they are the corpus's widest there).
P2 **WRONG** (I predicted the 0 bps and 25 bps lambda curves move together; they diverge, which is
the cost signature).  P3 **RIGHT** (the panel gap survives matching).  P4 **RIGHT** (the queue's
"4–7 on every EWall cell" is wrong; the 7-point window is the ranked book's).  P5 **HALF RIGHT**
(lambda < 1 on TOP20 as predicted, but also on half the EWall cells).

## Caveats carried
* **SURVIVORSHIP (idea 54):** current constituents on both panels; the equity leg is flattered
  relative to the ETF sleeve, so every window here is biased narrow and toward low f — the negative
  half of this result is understated, not overstated.
* lambda changes the base book's **path** as well as its trading; a heavily smoothed TOP20 is
  compositionally closer to EWall.  This is why A4's cost route, which changes drag and nothing
  else, is the arbiter and the lambda route is only corroboration.
* lambda can only lower turnover, so the falsification is one-sided (it can open a window, never
  close one).
* MaxDD is one number off one path and the 4b DD cap turns on exactly that number (idea 321).
* Idea 126: t+1 execution, no lag band.  Idea 38: u56/broad carry the calendar-day index.

## What the record should do with this
Publish **drag (base turnover x rung)** beside any window-width claim, not turnover — the two are
not interchangeable, and turnover alone gets the cross-cell ordering backwards.  A base book's
turnover is a statement about how fast its window *closes as the rung rises*, never about how wide
that window is at any given rung.
