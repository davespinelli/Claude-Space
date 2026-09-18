# Idea 1286 (lane cloud, 2026-09-18) — is the standing G = 0.60 book's 4b pass PAID FOR BY SELECTION, or BOUGHT BY EXPOSURE?

**ANSWERED: (A) PAID FOR — ON U56, AND ONLY ON U56.** With N, H, cadence, gross, costs and
execution held identical and **only the ranking removed**, the standing book beats its
random-selection twin by **+0.081 to +0.162 of full Sharpe on U56, sitting above all 12 seeds at
7 of 8 grid points**, and under rule 8 (gross chosen in sample, 2017-2026 read once) by
**+0.0678 mean OOS Sharpe, SE 0.0186, t +3.66, positive at 21 of 24 cells**. It survives the
stress it had never been given: **4b PASS at every one of the 8 (cost, delay) grid points on
U56, including 25 bps with a t+2 fill** — full 12.04% / 1.0976 / −17.06%, OOS 13.21% / 1.1266 /
−17.06%, against SPY 15.13% / 0.8849 / −33.72%. **On B135 the separation is ~zero (z −0.26 to
+0.78) and the book loses 4b's DD leg at every t+2 cell; on SMALL663 the ranking is WORSE than
random at 6 of 8 grid points.** 6 of 6 gates, 35 s, offline, deterministic.
**Verdict: the standing 4b candidate is CONFIRMED and NARROWED to U56. No RULES change proposed
(rule 6 reserves that for a Sunday review); memo written.**

## Why this idea
The queue's tail (943, 905, 825) is three stale Open duplicates of items already claimed by
other lanes, and everything above them through 1139 is record-bookkeeping. The sprint's
documented fallback was used: **three new price-only ideas (1284 / 1285 / 1286) stress-testing
the standing KEEP-4b candidate were filed, and the LAST was claimed.** Price-only; no EDGAR /
Form 4 / 8-K / options / spin-offs / live data.

Idea 1282 and idea 1281 (this lane, earlier today) both land on the same book: the U56 gross
rung **G = 0.60** is the one book on the record's four ladders that passes 4b under *every*
drawdown key tried. The CHANGELOG's standing diagnosis is that "the DD cap is the only binding
4b leg and every exposure mechanism is reproduced by a flat gross cut". Put together: if the
binding leg is drawdown and drawdown is bought by cutting gross, **what is the three-leg
composite selection contributing?** Nobody had run the control that answers it.

## The construction
Four arms, identical in everything but selection, on three panels:

| arm | what it is |
|---|---|
| **RANK** | the standing book — top N=20 by the frozen 21/252 + 0/126 + 0/63 composite among eligible names, min-hold H=126, equal weight |
| **RAND** | **identical mechanics**, N=20 slots, min-hold H=126, equal weight, drawn uniformly at random from the **same eligible set**. 12 seeds. Matches breadth, holding period, turnover shape and exposure; removes **only** the ranking |
| **BREADTH** | equal weight over every eligible name, no N, no ranking |
| **SPYONLY** | g of NAV in SPY, rest cash — exposure with no stock selection at all |

DIAL 1 = cost {0, 10, 25, 50} bps. DIAL 2 = fill delay {t+1, t+2}. **Gross is not a dial**: all
five rungs {0.50, 0.60, 0.75, 0.85, 1.00} are reported at every grid point and the rule-8 arm
chooses it in sample. 1,800 published cells; 360 rule-8 chooser rows.

## The standing rung under defence, G = 0.60, all 8 grid points

**U56 — passes 4b at every one of the 8, and the twin never does:**

| | RANK | RAND (median of 12) | 4b passes among 12 seeds | BREADTH | SPY@0.60 |
|---|---|---|---|---|---|
| t+1, 0 bps | 12.85% / **1.173** / −15.47% **4b PASS** | 9.56% / 1.058 / −16.49% | **0 / 12** | 1.135 fail | 0.884 fail |
| t+1, 10 bps | 12.59% / **1.152** / −15.51% **PASS** | 9.26% / 1.027 / −16.52% | **0 / 12** | 1.052 fail | 0.882 fail |
| t+1, 25 bps | 12.20% / **1.119** / −15.59% **PASS** | 8.80% / 0.981 / −16.57% | **0 / 12** | 0.926 fail | 0.879 fail |
| t+1, 50 bps | 11.55% / **1.065** / −15.72% **PASS** | 8.05% / 0.904 / −16.65% | **0 / 12** | 0.716 fail | 0.874 fail |
| t+2, 0 bps | 12.69% / **1.151** / −17.04% **PASS** | 9.66% / 1.070 / −17.11% | **0 / 12** | 1.133 fail | 0.884 fail |
| t+2, 10 bps | 12.43% / **1.129** / −17.05% **PASS** | 9.36% / 1.039 / −17.13% | **0 / 12** | 1.053 fail | 0.882 fail |
| **t+2, 25 bps** | **12.04% / 1.098 / −17.06% PASS** | 8.91% / 0.993 / −17.17% | **0 / 12** | 0.931 fail | 0.879 fail |
| t+2, 50 bps | 11.39% / **1.044** / −17.08% **PASS** | 8.16% / 0.916 / −17.24% | **0 / 12** | 0.728 fail | 0.874 fail |

**B135 — passes only at t+1 and only to 25 bps.** t+1: PASS at 0/10/25 bps, fails H2 at 50.
**t+2: fails the DD leg at all four cost rungs** (−20.37% to −20.76% against the cap's −20.23%).
An extra day of slippage costs this panel 3.6 pp of MaxDD and the verdict with it.

**SMALL663 — fails every leg at every grid point** (H1, H2, OOS, DD, CAGR all named), 0.530
down to 0.414 full Sharpe against SPY's 0.858.

## RANK − RAND: is the ranking paid for?
Full-sample Sharpe at G = 0.60; `z` is against the 12-seed spread; `pctile` is the share of
seeds RANK beats.

| panel | delay | 0 bps | 10 bps | 25 bps | 50 bps |
|---|---|---|---|---|---|
| **U56** | t+1 | +0.115 (z **+2.05**, 12/12) | +0.124 (z **+2.23**, 12/12) | +0.138 (z **+2.50**, 12/12) | +0.162 (z **+2.95**, 12/12) |
| **U56** | t+2 | +0.081 (z +1.63, 11/12) | +0.090 (z +1.79, 12/12) | +0.105 (z **+2.04**, 12/12) | +0.129 (z **+2.45**, 12/12) |
| B135 | t+1 | +0.004 (z −0.00) | +0.014 (z +0.15) | +0.028 (z +0.38) | +0.051 (z +0.78) |
| B135 | t+2 | −0.014 (z −0.26) | −0.004 (z −0.12) | +0.011 (z +0.09) | +0.035 (z +0.45) |
| SMALL663 | t+1 | **−0.035** (z −0.69) | **−0.032** | **−0.028** | **−0.020** |
| SMALL663 | t+2 | **−0.016** | **−0.013** | **−0.008** | +0.000 |

**The separation is a U56 fact.** It also *widens* with cost, on all three panels — RANK turns
over 2.32/yr against RAND's 2.77 and BREADTH's 6.60, so the ranked book is the cheapest of the
three to run and gains relative ground at every cost rung. That is the opposite of the usual
"the edge dies at realistic costs" failure mode, and it is the most robust thing in this run.

## Rule 8 — gross chosen on warm-up..2016 only, 2017–2026 read ONCE
Differences in OOS Sharpe over all 24 (panel, cost, delay) cells:

| contrast | mean | SE | t | positive |
|---|---|---|---|---|
| **RANK − RAND** | **+0.0678** | 0.0186 | **+3.66** | **21 of 24** |
| **RANK − BREADTH** | **+0.1384** | 0.0274 | **+5.04** | **21 of 24** |
| RANK − SPYONLY | −0.0277 | 0.0652 | −0.42 | 16 of 24 |

Rule-8 4b passes: **RANK 9/24, BREADTH 5/24, RAND 11/288, SPYONLY 0/24.** 4a: **0 of 360** —
and 0 of all 1,800 published cells, which is rule 4's own stated reason for path 4b.

**The RANK − SPYONLY mean is negative and it is entirely SMALL663.** By panel it runs **U56
+0.202 to +0.329 and B135 +0.018 to +0.167 at every cell**, against **SMALL663 −0.400 to
−0.526 at every cell**. On large caps the whole apparatus beats plain de-grossed SPY by a wide
margin; on small caps it is beaten by it, badly, and the pooled mean hides both.

## An honest caveat on the SPYONLY arm
**SPYONLY's 0-of-120 4b record is mechanical, not evidence.** A constant-gross SPY-plus-cash
book has *exactly* SPY's Sharpe (gate G2: 0.00e+00 at gross 1.00), and 4b's three Sharpe legs
are strict `>`, so it cannot pass at any gross. Its failing-leg profile confirms this — H1 and
H2 named in **1.000** of its failures. The informative SPYONLY comparison is the OOS Sharpe
difference above, not the pass count, and it is reported as such.

## The binding leg, which confirms the CHANGELOG's standing diagnosis
Share of each arm's *failing* cells naming each leg:

| arm | n fail | H1 | H2 | OOS | **DD** | CAGR |
|---|---|---|---|---|---|---|
| RANK | 101 | 0.396 | 0.505 | 0.396 | **0.871** | 0.475 |
| RAND | 1410 | 0.277 | 0.539 | 0.468 | **0.749** | 0.596 |
| BREADTH | 109 | 0.642 | 0.688 | 0.596 | 0.624 | 0.853 |
| SPYONLY | 120 | 1.000 | 1.000 | 0.800 | 0.800 | 0.400 |

DD is the binding leg for 0.871 of RANK's failures. The diagnosis holds — **and this run shows
it is not the whole story: holding gross fixed at 0.60, removing only the ranking still costs
0/12 seeds their pass on U56.** Exposure sets the level; selection decides who clears it.

## Gates, all 6 passing
G1 fast runner == `engine.backtest` on the standing book, **2.08e-17**. G2 SPYONLY at gross 1.00
and 0 bps reproduces each panel's own SPY Sharpe, **0.00e+00** — so the exposure control is
provably the benchmark it claims to be. G3 CAGR non-increasing in the cost rung, **0**
violations across all 1,800 cells. G4 SPYONLY's Sharpe invariant to the fill delay (it never
trades intra-week), max distinct value **1**. G5 SPY never a panel constituent (asserted in
`Panel.__init__`). G6 gross chosen on IS rows only (structural).

## Survivorship (rule 9) — it cuts against this run's own headline, and that is the point
U56 and B135 are CURRENT-constituent lists; SMALL663 is a current sub-$2B screen with the house
`max_1d_move >= 1.0` filter applied FIRST (52 of 715 names dropped). This matters more than
usual here and in a **known direction: a current-constituent list is a list of survivors, so a
random draw from it is a draw from winners, and RAND is FLATTERED.** That biases the run
*against* the (A) it reports — the true RANK − RAND separation on a vintage-honest panel is at
least the +0.068 measured here. The reverse also holds and is stated: SMALL663's negative
separation is *not* evidence the composite is worthless on small caps, only that it is not
visible above a survivor-flattered control. All absolute 4b / 4a verdicts and OOS triples are
upper bounds.

Script: `research/backtests/2026-09-18_is-the-STANDING-G-0.60-BOOK-s-4b-PASS-PAID-FOR-BY-SELECTION-or-BOUGHT-BY-EXPOSURE_cloud.py`
