# Idea 416 — pre-register K_CAGR as the rule-8 default (cloud, 2026-09-08)

**VERDICT: KILL of the proposal. The K_CAGR-over-K_Sharpe gap DOES NOT REPLICATE out of corpus.
Per the pre-registered decision rule, PROTOCOL rule 8 gets the DO-NOTHING control, not a named
selector.** Script `2026-09-08_pre-register-K_CAGR-as-the-rule-8-default_cloud.py`.

## The corpus, and why it is a real test
Ideas 142 and 151 read the **same nine books on the same three panels**; 151 only widened the
cost rung. `+0.0342` could not have been disconfirmed by 151 on any cell 142 had already read.
This run reads a corpus with **zero (panel, book) overlap and zero (panel, book, cost, arm) row
overlap with either parent** — asserted in gate (b), printed in the console, not asserted by eye:

* **A fourth panel, `bstk100`** — the broad panel with all 36 ETFs deleted, SPY held out as the
  benchmark return only. 100 US large-cap stocks. Carries the six old equity books.
* **Six new books** — `R3` (top-3), `R60`, `R80`, `S3-75`, `S4-25`, and `IVOL`
  (inverse-60d-vol over every priced name at gross 0.75, the only new *construction*).

24 (panel, book) cells x 3 rungs {0, 10, 25 bps} x idea 94's 17 arms = **72 paired cells,
1,224 arm-rows, all reported** in `.grid.csv`; 6 defaults x 2 pools x 72 = **864 picks** in
`.picks.csv`. Gate (a): `H.run` reproduces `engine.backtest` on every ungated book to
**0.000e+00** on all four panels.

Two tuned parameters, identical to idea 151's so the pre-registration is literal: the **default**
(D_NONE / K_Sharpe / K_CAGR / K_Calmar / K_MaxDD / K_Random) and the **pool** (P_ALL / P_S1).

## The pre-registered readings, reported once

| # | pair (OOS Sharpe, P_ALL) | this corpus | idea 142 | idea 151 | verdict |
|---|---|---|---|---|---|
| **P1** | **K_CAGR − K_Sharpe** | **−0.0006, t −0.22, 12W/18L/42T, sign p 0.36** | +0.0415 (t 3.34) | +0.0342 (t 3.96) | **FAILS** |
| P2 | K_CAGR − D_NONE | −0.0036, t −1.00, 21W/26L/25T, p 0.56 | — | +0.0100 (t 3.17) | **FAILS** |
| P3 | K_Sharpe − D_NONE | −0.0029, t −0.65, 32W/30L/10T, p 0.90 | — | −0.0241 (t −3.34) | holds in sign, **not in size** |
| P4 | K_CAGR − K_Sharpe, OOS CAGR / MaxDD | **+0.82 pp (29W/1L, p 0.0000) / −1.24 pp (5W/23L, p 0.0009)** | — | +1.36 / −1.61 pp | **HOLDS** |
| P5 | K_CAGR − K_Random | +0.0498, t +4.42, 47W/20L, p 0.0013 | — | — | HOLDS |

**Decision rule (fixed before the run): rule 8 may name K_CAGR only if P1 AND P2 hold. P1 fails.
==> rule 8 gets the DO-NOTHING control.**

## What actually replicated, and what did not

1. **The headline is gone, and it is not a tie-rate artefact.** K_Sharpe and K_CAGR pick the same
   arm in 42 of 72 cells here vs 29/72 (151) and 18/48 (142). But conditioning on the cells where
   they *disagree* does not rescue it: **−0.0014 per disagreeing cell here vs +0.0572 (151) and
   +0.111 (142)**. The gap is absent where the selectors differ, not merely diluted.
2. **The exchange rate is the durable part.** K_CAGR buys OOS CAGR and pays OOS drawdown against
   K_Sharpe with near-perfect consistency (29W/1L on CAGR, 5W/23L on MaxDD). What ideas 142/151
   read as *selector skill on Sharpe* is, out of corpus, **a risk-preference dial with a
   ~0.66 pp-of-drawdown-per-pp-of-CAGR price and no Sharpe content**.
3. **No default beats doing nothing on OOS Sharpe on this corpus.** K_Sharpe −0.0029 (p 0.90),
   K_CAGR −0.0036 (p 0.56), K_Calmar −0.0003 (p 0.81), K_MaxDD −0.0417 (p 0.076), K_Random
   −0.0534 (p 0.0000). Idea 151's *sign* survives; its *significance* does not. The honest
   statement is weaker and cleaner than either parent's: **selection is not separable from
   abstention here, in either direction.**
4. **Idea 418's de-risking finding reproduces hard.** *Every* default including RANDOM loses OOS
   CAGR to do-nothing (K_Sharpe −0.97 pp, K_Random −2.81 pp, K_MaxDD −4.50 pp, all p<0.0001) and
   wins OOS MaxDD (+1.37 / +3.48 / +9.24 pp, all p<0.005). The **menu** is the de-risking
   instrument; the chooser is not. Third independent corpus to say so.
5. **Selection still beats chance.** Against a 400-draw random-selection distribution
   (mean −0.0438, sd 0.0085), both K_Sharpe (−0.0029) and K_CAGR (−0.0036) sit at the
   **100th percentile**. Same shape as idea 151's SPLIT: selection beats a coin and loses to
   inaction.
6. **Idea 417's mechanism does NOT replicate.** rho(d, IS_argmax_margin) = **−0.012** (K_Sharpe)
   and **−0.166** (K_CAGR), against idea 151's −0.383. Idea 417 should be read as a property of
   idea 151's corpus until something else carries it.
7. **One positive reading, reported because it exists, not promoted.** On the *screened* pool
   P_S1, K_CAGR − D_NONE = **+0.0036 (t +1.96, 23W/9L, sign p 0.020)** — the only
   selector-beats-abstention reading in the file, on a pool where 40 of 72 cells tie because the
   screen admits nothing. That is idea 132/140's abstention finding again, not a selector result,
   and it is one of 42 paired readings printed here.

## Walk-forward (PROTOCOL rule 8) — every pick read ONCE on 2017-2026

Means over all 72 cells (P_ALL): D_NONE **14.18% / 0.9426 / −26.45%**; K_CAGR 14.03% / 0.9390 /
−26.32%; K_Sharpe 13.21% / 0.9397 / −25.08%; K_Calmar 12.85% / 0.9422 / −24.43%; K_Random
11.37% / 0.8892 / −22.97%; K_MaxDD 9.68% / 0.9008 / −17.21%.
Reference OOS: **SPY 15.45% / 0.8820 / −33.72%**, live **RULES v2 1.0582** Sharpe (per panel
1.1136 broad / 1.1354 bstk100 / 1.2810 u56 / 0.5597 small), RULES v1 well below.
Per panel (D_NONE): u56 13.20%/1.0980/−18.52%, broad 12.68%/0.9938/−22.32%,
bstk100 16.57%/0.9895/−26.97%, **small 11.44%/0.5932/−39.25%**.

## Both KEEP paths, on all 1,224 rows

4a vs live RULES v2 **22**; 4a vs v1 538; 4b (full sample) **186**; 4b (OOS window) 194;
**BOTH PATHS 0**. All 22 4a passes are at 0 bps (broad 13, u56 8) plus one broad row at 10 bps;
**0 of 408 at 25 bps** — the 18th reproduction of idea 136. The **small panel admits 0 of 204 on
4b at every rung**, reproducing the record's small-panel wall. The binding 4b bar is DD (285 rows)
then CAGR (226). No memo, no RULES change, no candidate.

## Caveats

* **SURVIVORSHIP (idea 54).** All four panels are current constituents; the small panel is the
  sub-$2B screen's survivors since 2010 with `max_1d_move >= 1.0` names dropped. Every CAGR here
  is inflated and every 4b CAGR-floor margin is optimistic — and a *CAGR-argmax* selector is the
  one most exposed to that bias, which if anything biases this test **in K_CAGR's favour**. It
  still failed. Paired signs are unaffected (both sides share the panel); the 4b counts are not.
* Idea 128: the IS window's SPY drawdown is shallower than the OOS window's, so P_S1's IS
  drawdown bar is measured on a window that cannot express a deep drawdown.
* Idea 126: t+1 execution only.
* 72 cells are not 72 independent observations — the six bstk100 books share 100 names and arms
  overlap heavily inside a panel. Per-panel, per-rung and per-stratum splits are printed so the
  clustering is visible rather than hidden.

## What this changes

PROTOCOL rule 8 should keep saying nothing about a selector, and where a run needs a default it
should be **the do-nothing control** — the cell's own ungated book — with the argmax reported
beside it, not instead of it. Ideas **415** (is K_CAGR the CAGR floor in disguise) and **417**
(is IS-argmax confidence an inverse signal) are both weakened: the effect 415 is trying to
decompose does not exist off its own corpus, and 417's rho does not carry. Idea **418** (price
the defensive menu, not the chooser) is strengthened on a third corpus and is now the live thread.
