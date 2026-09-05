# Idea 184 — is-the-gross-ladder-worth-running-at-all (lane B, 2026-09-05)

**ANSWERED — SPLIT. KILL of the QUEUE's strong form (verdicts DO change under g := 0.75), KILL
of the gross ARGMAX as a selector, and a cheaper replacement for the sweep that loses nothing.
No RULES change, no new book, no KEEP-candidate.**

Script `research/backtests/2026-09-05_is-the-gross-ladder-worth-running-at-all_B.py`;
artefacts `.grid.csv` (486 points), `.books.csv` (54), `.walkforward.csv` (54), `.bars.csv`,
`.rescale.csv`, `.console.txt`. 243 **genuine** engine runs (no rescaling anywhere, per idea
176), 578s, seed 184.

## Corpus
3 panels (u56 56 names / broad 136 / small 439 after dropping 44 tickers with
`max_1d_move >= 1.0`) × 3 signals (COMP, MOM, R6) × 3 counts (n = 10/20/40) = 27 book-cells,
each laddered on 9 gross points g ∈ {0.20 … 1.35} with the anchor 0.75 **interior at rank 5 of
9** (idea 183's caveat). 2 cost rungs (10, 25 bps) derived exactly from the zero-cost run →
54 books, 486 ladder points. GROSS is the only tuned dial; panel, signal, count, cadence (W),
max_vol (0.60), vol power (0.5) and cost are reported axes, never selected on.

## Reproduction (4 of 4)
* cost-derivation identity `port_c = port_0 − turnover·c/1e4`: max |genuine − derived| =
  **0.000e+00** on all three panels.
* RULES v1 u56 @10 bps: 6.45% / **0.6642** / −13.83% (published 0.664).
* SPY u56/broad 15.23% / **0.8890** / −33.72%; small-panel window 14.13% / 0.8615.
* idea 173's flatness reproduces on a different corpus: mean OOS Sharpe over the whole ladder
  0.7369 → 0.7383, **range 0.0014** over a 6.75× gross span (idea 173: 0.003 over 3×).

## The two halves of a gross-ladder verdict, priced separately

**SELECTION is worthless, and it is not harmless.** Rule 8 (g chosen ≤2016-12-31, read ONCE
on 2017→, 54 books):

| arm | OOS CAGR | OOS Sharpe | OOS MaxDD | 4b-OOS | 4a | mean g |
|---|---|---|---|---|---|---|
| FIX075 (do-nothing) | 8.91% | **0.7383** | −22.85% | 7/54 | 29/54 | 0.750 |
| ISSHARPE (IS argmax) | 13.29% | 0.7380 | −34.91% | 5/54 | 1/54 | 1.198 |
| IS4B (lowest IS-admissible g) | 8.70% | 0.7381 | −22.56% | 6/54 | 29/54 | 0.739 |
| ORACLE (best OOS, not implementable) | 10.02% | 0.7400 | −22.27% | 1/54 | 20/54 | 0.757 |
| RULES v1 | 4.39% | 0.4229 | −26.24% | — | — | — |
| SPY | 15.45% | 0.8820 | −33.72% | — | — | — |

Paired against FIX075: ISSHARPE **−0.0002 (t −0.58)**, IS4B −0.0001 (t −1.53), and **even
perfect foresight of gross buys +0.0017 (t +6.89)** — that is the entire risk-adjusted value
the dial can deliver, with hindsight, on 54 books. Meanwhile the IS-Sharpe selector picks
g = 1.35 in **30 of 54** books and moves **OOS MaxDD by −12.06pp (t −12.81, deeper in 50/54)**
and 4a passes from 29 to 1. **A flat ladder does not make its argmax safe: it makes the argmax
a random draw over exposure.** GROSS carries 46 of the project's 104 textual argmax claims.

**ADMISSION is NOT inert — the strong form fails.** Verdict at g = 0.75 vs "some ladder point
passes": 4a 29 → 40 (**11 books flip**), 4b full-sample 7 → 15 (**8 flip**), 4b OOS-window
7 → 12 (**5 flip**). Per point, 65 of 486 carry a 4b verdict different from their own book's
0.75 verdict. Fixing gross at 0.75 everywhere **would re-label the record**, so PROTOCOL
cannot simply retire the sweep.

## But the sweep is a bracket, not a search — and one run recovers it

* **All three Sharpe bars are gross-invariant**: same pass/fail at all 9 points in **54/54**
  books (H1), **54/54** (H2), **53/54** (OOS). The DD cap is invariant in **0/54** and the
  CAGR floor in 15/54. Of 464 full-sample 4b failures the sole binding bar is DD 62 / CAGR 78
  against H1 3, H2 1, OOS 0.
* Therefore 4b admission is an **interval in g**, bounded below by the CAGR floor (at g ≤ 0.50
  the floor fails in 161 of 162 points) and above by the DD cap (at g ≥ 1.20 it fails in 108
  of 108). The 4b pass rate is single-peaked: 0.0 / 0.0 / 1.9 / 9.3 / **13.0** / 5.6 / 11.1 /
  0.0 / 0.0 % across the ladder. The admissible set is **contiguous in 54 of 54 books**.
* The 8 flipping books are exactly that geometry: 2 broad books fail the **DD cap** at 0.75 and
  pass at 0.50–0.65; 6 u56 n=40 books fail the **CAGR floor** at 0.75 and pass at 0.90–1.05.
* **The interval is recoverable from ONE run.** Rescaling the g=0.75 return stream to every
  other rung reproduces the genuine 4b-admissible set in **54 of 54 books** and mislabels
  **0 of 432** points, at max |ΔSharpe| 0.0072, max |ΔMaxDD| **0.83pp**, max |ΔCAGR| 0.24pp.
  Idea 176's exposure is real in magnitude and did not move a verdict here — but 0.83pp is
  wider than some 4b margins, so the chosen endpoint still needs a genuine confirming run.
* All 11 4a flips pass **only below** g = 0.75 (4a's pass rate is monotone decreasing, 74.1% →
  0.0%). Those are de-grossing beating a low-return live book — PROTOCOL rule 4b's own
  preamble already discounts them.

## Pre-registered predictions: 3 hits, 3 misses
P1 selection inert (|Δ| < 0.02, |t| < 2) — **HIT** (−0.0002, t −0.58).
P2 Sharpe bars gross-invariant in ≥90% of books — **HIT** (100/100/98.1%).
P3 ≥25% of books flip 4b — **MISS**: 14.8% (4b), 20.4% (4a), 9.3% (4b-OOS). Direction right,
threshold wrong.
P4 flips carried by CAGR floor and DD cap — **HIT** (sole binding: DD 62, CAGR 78, Sharpe 4).
P5 zero 4b passes at every g ≤ 0.50 — **MISS by one point**: 1 of 54 passes at g = 0.50.
P6 rescaling mislabels ≥1 verdict — **MISS**: 0 of 432.

## Both KEEP paths (all 486 points)
4a **206/486**; 4b full-sample **22/486**; 4b OOS-window **23/486**; both 4a and 4b 7.
By panel: u56 4a 72 / 4b 15 / 4b-OOS 21; broad 99 / 7 / 2; **small 35 / 0 / 0** — a ninth
reproduction of idea 136 (the small panel has no defensive class).
Best point clearing 4b full-sample AND the OOS window: **u56 · COMP · n=40 · g=0.90 · W ·
10 bps → 11.41% / 1.1244 / −16.43%** (H1 1.0907, H2 1.1571; OOS 13.09% / 1.2494 / −16.43%;
5.9×/yr turnover). **Reported, not proposed:** it is 1 of 15 unpriced ladder selections and it
**fails the universe change** — broad @10 bps 11.70% / 0.9482 / **−22.03%** (DD cap −20.23%)
with H2 0.784 < SPY's 0.834, small 7.96% / 0.5827 / −33.39%. Same shape and same failure as
idea 173's by-product, already queued as pre-registered idea 182; nothing new to propose.

## Offered to PROTOCOL, not adopted (rule 6 — Sunday review only)
Rule 4 addendum: *a gross ladder may not be swept for an argmax. Report the book at the
pre-registered gross, plus the 4b-admissible gross INTERVAL [g_lo, g_hi] derived from the
level bars of that single run, and re-run genuinely only at the endpoint being claimed.* On
this corpus that is 1 + 1 runs where the project spends 9, it loses no verdict (54/54), and it
removes 46 of 104 argmax claims from the record. The runs saved should go to CADENCE, the one
dial ideas 173 and 175 found has interior, selectable structure.

## Caveats carried, not buried
Survivorship (idea 54) on all three panels — every CAGR here is optimistic and every MaxDD
flattering, so the 4b interval looks WIDER than it is, and "the sweep is a bracket" is the
conservative reading. Window composition (idea 111): the IS window holds fewer SPY-drawdown
years, and the small panel's IS window is only 2011–2016. This run prices what a gross ladder
CAN do on 486 fresh points; it does not re-run every committed leaderboard row (that is idea
176's audit). t+1 execution, 10/25 bps, no shorting, no leverage.
