# Idea 807 — is-the-21-OFFSET-ENSEMBLE-of-the-805-book-a-4b-PASS-in-its-own-right

**Lane C, 2026-09-15.** Script `2026-09-15_is-the-21-OFFSET-ENSEMBLE-of-the-805-book-a-4b-PASS_C.py`.
Outputs: `.grid.csv` (714 cells), `.sleeves.csv` (21 offsets), `.walkforward.csv`, `.keeppaths.csv`, `.console.txt`.

## ANSWER

**YES ON THE LETTER, NO ON THE POINT. The ensemble IS a 4b pass in its own right — and it does NOT
recover the drawdown margin; it reproduces the mean offset. PARK, NOT KEEP. KILL for capital.**

Idea 805 killed the U56 / MA-DG / MONTHLY / g=1.00 book on H_CAL: 4b held at only 13 of 21
month-end offsets, all 8 failures on the DD leg alone, because the book's DD-cap margin (4.74pp)
was smaller than the 21-offset MaxDD spread (8.37pp). The queue's objection was that no real
portfolio has to pick one of those dates. This run prices the book that does not pick one: capital
split once into 21 equal sleeves, one per offset, each compounding and paying its own costs, never
re-equalised (ENS-NAV) — the implementable construction, with an unpriced daily-re-equalised
variant (ENS-EW) reported beside it and selecting nothing.

That ensemble passes 4b at the pre-declared cell. It passes on all five legs, at every cost rung
through 50 bps, and at execution lags 1, 2 and 3. **But the margin it clears the DD cap by falls to
1.16pp — smaller than the 4.74pp of the single calendar it replaced, and one seventh of the 8.37pp
spread it was supposed to average away.** The reason is in the diagnostic: the 21 sleeves' daily
returns correlate 0.968 on average and **all 21 trough inside March 2020**, on 5 distinct dates
between 2020-03-12 and 2020-03-23. There is only one drawdown here, seen 21 times; the offset moves
only where inside that episode each sleeve last re-set its weights. Averaging 21 views of one crash
buys **+0.31pp** of drawdown out of an 8.37pp spread.

And the number the record published was the best of the 21: **offset 0 ranks 1 of 21 on MaxDD**
(−15.49%, shallowest; mean −19.38%, worst −23.85%). Idea 805's 4.74pp margin is the margin of that
rank, not of that book. The calendar-free version of the same rule clears the cap by 1.16pp.

## GATES (all pass on the book)

| gate | reading | bar | verdict |
|---|---|---|---|
| G1 engine | `fast_run` vs `engine.backtest`, sleeve k=0 | 1e-9 | **PASS** 2.082e-17 |
| G2a repro of 804/805's triple | full 11.90% / 1.21 / −15.5%, OOS 12.61% / 1.27 / −15.5% | half a unit in the last published digit | **OVER on CAGR only** (1.6e-4 / 3.5e-4) |
| G2a' same book on 805's panel end | **full 11.9212% / 1.2095 / −15.486%, OOS 12.6457% / 1.2693 / −15.486%** vs published 11.92% / 1.21 / −15.5% and 12.65% / 1.27 / −15.5% | same | **PASS**, max 0.867 tol units |
| G2b repro of H_CAL | **13 of 21** offsets pass 4b (published 13); all 8 failures on DD alone | exact | **PASS** |
| G2c repro of the quoted pp | offset-0 margin **4.74pp**, 21-offset spread **8.37pp** | 0.05pp | **PASS** |
| G4 ensemble identity | rebuilt return path vs mean-of-sleeve-NAVs | 1e-12 | **PASS** 2.787e-14 |

G2a's CAGR miss is disclosed and explained, not waived: `data/prices.csv` gained one trading day
(2026-09-14) between 805's run and this one. Truncating the panel at 805's own last bar
(2026-09-11, read off git, not searched for) reproduces every published field inside the bar. One
extra bar over 17.7 years moves CAGR by ~1.7e-4, which is the whole discrepancy. **Every CAGR in
this file is measured on the longer window and is not comparable to a published CAGR to better than
~2e-4.**

## COMPARANDS AND BARS (window 2009-01-13 .. 2026-09-14, U56 = 56 names; SPY is a constituent *and* the comparand, 804/805's construction)

| | CAGR | Sharpe | MaxDD | halves | OOS (2017+) |
|---|---|---|---|---|---|
| SPY | 15.13% | 0.886 | −33.72% | 0.959 / 0.824 | 15.27% / 0.874 / −33.72% |
| RULES v2 (live) | 8.62% | 1.202 | −12.05% | 1.232 / 1.177 | 9.46% / 1.277 / −12.05% |

4b bars: H1 Sharpe > 0.9588 · H2 > 0.8236 · OOS > 0.8740 · MaxDD ≥ −20.2304% · CAGR ≥ 10.5912%.
4a bars: H1 > 1.2322 · H2 > 1.1770 · MaxDD ≥ −12.0549%.

## PRE-REGISTERED HYPOTHESES — 2 of 6 PASS

| | statement | reading | verdict |
|---|---|---|---|
| **H_ENS** | ENS-NAV passes 4b at g=1.00 / 10 bps / lag 1 | **11.68% / 1.177 / −19.07%**, halves **1.230 / 1.135**, OOS **12.70% / 1.230 / −19.07%**; all five legs true | **PASS** |
| **H_DDGAIN** | ensemble MaxDD better than the MEAN of the 21 sleeves by ≥ 1.00pp | −19.07% vs mean −19.38% → **+0.31pp** | **FAIL** |
| **H_MARGIN** | ensemble DD-cap margin exceeds the 21-offset MaxDD spread | **1.16pp vs 8.37pp** | **FAIL** |
| **H_COST** | 4b at g=1.00 at every rung through 25 bps | passes at 0, 5, 10, 15, 20, 25 **and 50** bps | **PASS** |
| **H_BAND** | the ensemble's 4b gross band contains 805's {0.90, 0.95, 1.00} | **{0.95, 1.00}** at 10 bps (0.90 fails the **CAGR** leg by 0.09pp, not DD); {0.90, 0.95, 1.00} at 0 and 5 bps; {1.00} at 50 bps | **FAIL** |
| **H_WF** | both IS-only selectors land at a g that passes 4b OOS | IS-SHARPE → g = 1.00 → OOS **12.70% / 1.230 / −19.07%, 4b PASS**; IS-BAND-MIDPOINT → **NO PICK, the IS 4b band is EMPTY** (all 17 rungs fail the IS CAGR leg) | **FAIL** |

## RULE 8 WALK-FORWARD (parameters on 2009–2016 only; OOS read once)

| selector | g | OOS CAGR | OOS Sharpe | OOS MaxDD | 4b | 4a |
|---|---|---|---|---|---|---|
| IS-SHARPE | 1.00 | 12.70% | 1.230 | −19.07% | **PASS** | FAIL |
| IS-BAND-MIDPOINT | — | — | — | — | **no pick (IS band empty)** | — |
| pre-declared g=1.00 | 1.00 | 12.70% | 1.230 | −19.07% | **PASS** | FAIL |
| SPY | — | 15.27% | 0.874 | −33.72% | | |
| RULES v2 (live) | — | 9.46% | 1.277 | −12.05% | | |

The ensemble beats SPY's OOS Sharpe by 0.356 and loses to SPY's OOS CAGR by 2.57pp/yr; it loses to
RULES v2's OOS Sharpe by 0.047 and to its MaxDD by 7.02pp. The empty IS band is idea 809's pattern
again: the 4b band this book lives in is an **ex-post object** — it does not exist on 2009–2016.

## THE 21 SLEEVES (g=1.00, 10 bps, lag 1) — 805's H_CAL table, re-measured

MaxDD mean **−19.38%**, min **−23.85%** (offset 15), max **−15.49%** (offsets 0 and 19), spread **8.37pp**.
Sharpe mean 1.161 (1.072 … 1.242). CAGR mean 11.68% (11.03% … 12.54%).
4b passes at offsets 0–8 and 17–20 (**13 of 21**); fails at 9–16, **DD leg alone, every time**.
4a: **0 of 21**.

## KEEP-PATH CENSUS

* ENS-NAV + ENS-EW, 17 gross × 7 cost × 3 lags: **4b 90 / 714**, **4a 0 / 714**.
* Per cell: 3/17 rungs at 0–5 bps, 2/17 at 10–25 bps, 1/17 at 50 bps — identical under both
  conventions and all three lags.
* Sleeves at the pre-declared cell: 4b **13/21**, 4a **0/21**.
* Lag sensitivity at g=1.00 / 10 bps (reported, never selected): lag 1 margin **1.16pp**, lag 2
  **0.78pp**, lag 3 **0.17pp** — all three still 4b passes, the last by a sixth of a point.
* Turnover 1.96×/yr, realised gross 0.710 at g=1.00. ENS-NAV costs exactly the 21 sleeves' own
  turnover: there is no cross-sleeve transfer, so the ensemble is not more expensive than the book
  it replaces. **That is the one thing averaging does buy.**

## WHY THIS IS NOT CAPITAL-WORTHY

1. The DD leg clears by **1.16pp** on a cap (−20.23%) computed from a **survivorship-biased** SPY
   comparand on a survivorship-biased panel. The margin is smaller than the measurement error the
   record has already documented in panel vintage (idea 823: median |ΔMaxDD| 1.10pp on a re-cut
   panel alone).
2. The pass dies on ordinary conventions the run reports but never selects: at lag 3 the margin is
   **0.17pp**; at 10 bps the pass exists at 2 of 17 gross rungs, a run flush against the ladder's
   top endpoint (g = 1.00) with **no interior**, while the Sharpe argmax sits at the opposite
   endpoint (g = 0.20, Sharpe 1.181 against 1.177 at g = 1.00).
3. Rule 8 is half-satisfied at best: one of two pre-declared selectors has **no pick at all**
   because the IS window's own 4b band is empty.
4. The ensemble does not out-earn SPY (12.70% vs 15.27% OOS CAGR) and does not out-Sharpe the live
   book (1.230 vs 1.277) — it is a lower-return, lower-drawdown object that clears 4b's floors
   rather than beating anything.

**Nothing is promoted. No RULES change, no PROTOCOL edit applied. `RULES.md`, `PROTOCOL.md`,
`scan.py`, `bot.py` and `baseline.py` untouched (rule 6).**

## ONE LINE FOR THE RECORD

A monthly book's 4b drawdown pass should be quoted **with the offset ensemble's margin, not the
chosen calendar's** — here 1.16pp against 4.74pp — because averaging 21 calendars removes the
choice without removing the risk: the drawdowns are the same March 2020, 21 times.

## SURVIVORSHIP

U56 is the **current** constituent list of `research/universe.json`. Dead names are absent, so every
CAGR here is biased upward and the 4b CAGR floor (0.70 × SPY's CAGR on the same survivor-free
benchmark) is easier to clear than on a point-in-time panel; the DD cap is biased the same way. No
result above is corrected for this.
