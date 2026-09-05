# Idea 166 — does-the-ceiling-beat-a-chosen-gross (lane C, 2026-09-05)

**ANSWERED, and it kills the clause it was sent to confirm. `g = min(g_req, 1.00)` is not
load-bearing: on the untouched 2017–2026 window it is the WORST of the four gross-choice
rules tested, worse than doing nothing. It passes the OOS-window 4b in 9 of 300 books
against 33 for the fixed `g = 0.75` the project already uses, 28 for the IS 4b-margin
argmax and 32 for idea 152's interval midpoint. Idea 156's headline `0.00 -> 0.12 -> 0.00`
reproduces exactly — and is a statement about ONE of six cells. In the other five the
ceiling is last. No RULES change, no new book, no KEEP-candidate.**

Script `2026-09-05_does-the-ceiling-beat-a-chosen-gross_C.py`; outputs `.console.txt`,
`.grid.csv` (1200 book-arm rows), `.ladder.csv` (3000 rows = 300 books x 10 gross points),
`.choices.csv`, `.cells.csv`, `.walkforward.csv`.

## Reproduction, asserted before any new number was read

| check | result |
|---|---|
| [a] STATIC arm vs idea 78's committed `gridB.csv`, 300 books | **EXACT** — max abs diff 2.2e-16 on CAGR/Sharpe/MaxDD/H1/H2/Sharpe_OOS; 4b failing-bar string identical in **100.0%** |
| [b] idea 156: fraction of books needing `g_req > 1.00` | **55.0%** (idea 156: 55.0%), median `g_req` 1.032 |
| [b] idea 156: k=20/n=20 full-sample 4b pass, STATIC -> CEILING | **0.00 -> 0.12** (idea 156: 0.00 -> 0.12) |

This is idea 78's corpus, idea 156's lever and 4b's own bars. The weights are built as
`mask * (g / n)`, bit-for-bit idea 78's `weights_cand(..., gross=g)`.

## The four rules, all IS-only and all capped at 1.00 (PROTOCOL rule 2)

| rule | g mean | g median | at the 1.00 cap | Spearman(g, g_req) |
|---|---|---|---|---|
| STATIC (the incumbent constant) | 0.750 | 0.750 | 0% | — |
| CEILING `min(g_req, 1.00)` (idea 148/156) | 0.930 | **1.000** | **55.0%** | +0.913 |
| MAXMARG (IS 4b-margin argmax over the ladder) | 0.739 | 0.750 | 21.7% | +0.797 |
| MIDPOINT (idea 152's IS-passing interval midpoint) | 0.741 | 0.750 | 21.0% | +0.800 |

The first line of the answer is in that table. For 55% of the books CEILING is not choosing a
gross at all — it is spending every unit of gross rule 2 permits, because the vol match asks
for more than 1.00 and the cap truncates. The two rules that actually read the book's own
in-sample 4b geometry both land, on average, within 0.01 of the constant 0.75 the project
already had.

## The horse race — 300 books, paired, verdict read once on 2017–2026

| rule | IS-4b pass | **OOS-4b pass** | mean OOS margin | full-sample 4b | 4a pass | OOS CAGR | OOS Sharpe | OOS MaxDD |
|---|---|---|---|---|---|---|---|---|
| STATIC 0.75 | 24 | **33** | -0.2240 | 42 | 178 | 10.94% | 0.8752 | -19.91% |
| CEILING | 8 | **9** | -0.2943 | 10 | 57 | 13.32% | 0.8752 | -23.99% |
| MAXMARG | 62 | **28** | -0.2128 | 41 | 206 | 10.37% | 0.8741 | -18.88% |
| MIDPOINT | 62 | **32** | -0.2096 | 42 | 205 | 10.39% | 0.8741 | -18.91% |

Paired, book by book:

| vs CEILING | OOS-4b win | lose | d OOS margin | t | vs STATIC | win | lose | d OOS margin |
|---|---|---|---|---|---|---|---|---|
| STATIC | 32 | 8 | +0.0703 | 7.57 | CEILING | 8 | 32 | -0.0703 |
| MAXMARG | 20 | 1 | +0.0815 | 10.70 | MAXMARG | 12 | 17 | +0.0112 |
| MIDPOINT | 24 | 1 | +0.0847 | 10.90 | MIDPOINT | 13 | 14 | +0.0145 |

(The sub-panels overlap, so the t is a magnitude cue, not an independence claim.)

**Both halves of idea 166's question answer the same way.** The ceiling loses to a chosen
gross, 24–1 on the midpoint rule. And a chosen gross does not beat doing nothing: MIDPOINT
is 13–14 against the fixed 0.75 on OOS passes and buys +0.0145 of mean OOS margin for the
cost of an extra fitted quantity. Read together with ideas 151 and 110, that is the same
answer this project keeps getting: the selection step is not where the money is.

### Why the ceiling loses, in one row

4b failing-bar census on the OOS window (a book can fail several bars):

| rule | OOS pass | H1 | H2 | OOS | **DD** | **CAGR** |
|---|---|---|---|---|---|---|
| STATIC | 33 | 159 | 145 | 142 | 144 | 145 |
| CEILING | 9 | 159 | 145 | 143 | **245** | **71** |
| MAXMARG | 28 | 160 | 147 | 144 | **104** | **181** |
| MIDPOINT | 32 | 160 | 147 | 144 | 104 | 174 |

The ceiling buys CAGR with drawdown exactly as idea 156 said it would (CAGR failures
145 -> 71) and pays 101 extra drawdown failures for it. 4b asks for 100% of SPY's Sharpe in
both halves and out of sample but only 60% of its drawdown, so pushing gross to the legal
maximum is the wrong direction on the bar that is actually scarce. The three Sharpe bars
barely move across the four rules (H1 159/159/160/160) — gross is the exact lever idea 66
described, and it cannot buy a Sharpe bar.

### Idea 156's `0.00 -> 0.12 -> 0.00` was one cell

Per-cell OOS-window 4b pass rate:

| k | n | STATIC | CEILING | MAXMARG | MIDPOINT |
|---|---|---|---|---|---|
| 20 | 5 | 0.02 | 0.00 | 0.04 | 0.04 |
| 20 | 20 | 0.00 | **0.12** | 0.10 | 0.10 |
| 40 | 5 | 0.00 | 0.00 | 0.02 | 0.02 |
| 40 | 20 | **0.30** | 0.04 | 0.24 | 0.24 |
| 80 | 5 | 0.02 | 0.02 | 0.02 | 0.02 |
| 80 | 20 | **0.32** | 0.00 | 0.14 | 0.22 |

The one cell idea 156 reported (k=20/n=20) is the one cell where the ceiling wins, and it
wins there by 0.02 over the chosen rules. It is the cell whose books run 6.94% volatility and
need a median 1.82x to match SPY — i.e. the cell where the cap is furthest from binding on
anything. In the two cells with the most 4b passes in the corpus the ceiling is last by a
factor of 7 and by 0.32 to 0.00.

## The ladder itself — the incumbent constant is at the argmax

All 10 gross points, all 300 books:

| g | IS-4b pass | **OOS-4b pass** | full 4b | mean OOS margin | mean CAGR | mean MaxDD |
|---|---|---|---|---|---|---|
| 0.20 | 0.000 | 0.000 | 0.000 | -0.725 | 3.01% | -5.62% |
| 0.40 | 0.023 | 0.003 | 0.000 | -0.459 | 6.00% | -11.04% |
| 0.60 | 0.083 | 0.040 | 0.063 | -0.270 | 8.96% | -16.25% |
| 0.70 | 0.100 | 0.103 | 0.147 | -0.226 | 10.42% | -18.78% |
| **0.75** | 0.080 | **0.110** | 0.140 | **-0.224** | 11.14% | -20.03% |
| 0.80 | 0.053 | 0.063 | 0.083 | -0.236 | 11.87% | -21.26% |
| 0.90 | 0.020 | 0.017 | 0.030 | -0.289 | 13.30% | -23.70% |
| 1.00 | 0.023 | 0.027 | 0.027 | -0.368 | 14.72% | -26.08% |

`g = 0.75` is the OOS argmax of the ladder and `g = 1.00` — where the ceiling parks 55% of
the books — passes **4.1x less often**. The curve is single-peaked with a 0.70–0.75 plateau,
which is why an IS-fitted chooser cannot improve on the constant: there is nothing to choose.

**Oracle control:** 60 of 300 books (20.0%) have SOME ladder point that passes the OOS-window
4b; the best implementable rule reaches 33. Even a perfect chooser of g would leave 240 of
300 books outside 4b. The choice of gross is not the binding problem on this corpus.

## Rule 8 walk-forward (PROTOCOL rule 8) — chosen on ≤2016-12-31, read once on 2017→

Everything — each arm's gross AND the sub-panel — is fixed on the IS window.
S0 = do-nothing full-B136 control at the same gross rule; S1 = IS-Sharpe argmax over the 150
books; S2 = 4b-aware IS screen then IS-Sharpe argmax (S1 fallback).

| rule | mean OOS Sharpe | mean OOS CAGR | mean OOS MaxDD | picks passing 4b | picks passing 4a | mean g |
|---|---|---|---|---|---|---|
| STATIC | **0.9620** | 13.01% | -19.29% | 1 / 6 | 5 / 6 | 0.750 |
| CEILING | 0.9372 | 14.14% | -21.81% | 2 / 6 | 2 / 6 | 0.896 |
| MAXMARG | 0.9519 | 9.23% | -12.93% | 2 / 6 | 6 / 6 | 0.600 |
| MIDPOINT | 0.9521 | 9.70% | -13.61% | **4 / 6** | 6 / 6 | 0.625 |
| **SPY OOS** | 0.882 | 15.45% | -33.72% | — | — | — |
| **RULES v1 OOS on B136** | 0.576 | 5.94% | -21.19% | — | — | — |

The ceiling is last on OOS Sharpe here too, and last-equal on 4a. The best individual picks:

* `STATIC n=20 S2` (k=40): OOS **12.30% / 1.068 / -19.63%**, full-sample 4b **passes**
* `CEILING n=20 S1=S2` (k=20, g=1.00): OOS **11.16% / 1.103 / -13.93%**, full-sample 4b passes
  — this is idea 156's own headline pick, reproduced
* `MAXMARG = MIDPOINT n=20 S1=S2` (k=20, g=0.90): OOS **10.04% / 1.104 / -12.58%**, 4b passes
  — the same book at 0.90 rather than 1.00, with 1.35pp less drawdown for 1.12pp of CAGR

Every one of the 24 picks beats RULES v1's OOS Sharpe of 0.576. **None is proposed as a
KEEP.** Under idea 144's standing convention a re-grossed book is the same book, and idea
164's leaderboard rows already record 4b passes reached by re-grossing as *not proposed*.
This run produced no new signal, no new construction and no new universe — only four ways of
picking one number.

## Both KEEP paths, as PROTOCOL rule 4 requires

* **4a (beat the book):** 646 of 1200 book-arm rows pass — MAXMARG 206, MIDPOINT 205,
  STATIC 178, CEILING 57. The ceiling more than triples the 4a failure rate of every other
  rule, because 4a's drawdown clause is measured against RULES v1's own shallow book.
* **4b (capital-worthy):** 135 of 1200 on the full sample, 102 of 1200 on the OOS window.
  All are re-grossings of books already in the record; none is a new candidate.

## Pre-registered predictions, scored

| | prediction | result |
|---|---|---|
| P1 | [a] and [b] both hold | **HIT** — exact to 2.2e-16 and 55.0% / 0.00 -> 0.12 |
| P2 | CEILING sits at exactly 1.00 for a majority | **HIT** — 55.0% |
| P3 | MAXMARG picks well below 1.00 for most books | **HIT** — median 0.75, only 21.7% at the cap |
| P4 | MAXMARG ≥ CEILING on OOS 4b pass count | **HIT** — 28 vs 9, paired 20 win / 1 lose |
| P5 | MIDPOINT ≥ MAXMARG on OOS | **HIT** — 32 vs 28, margin -0.2096 vs -0.2128 |
| P6 | no arm produces a KEEP PROTOCOL would accept | **HIT** — every 4b pass is a re-grossing |

6 of 6. **The corpus's strongest result was not among them:** nothing predicted that the
CEILING would lose to the do-nothing constant 0.75 (9 vs 33, paired 8–32), nor that no
IS-fitted chooser would beat that constant either. Both are recorded as unpredicted.

## What this says about the record

1. **Idea 148's clause should not be written into RULES or PROTOCOL as a gross-CHOICE rule.**
   It was proposed on the strength of one cell of one corpus. Across all six cells of that
   same corpus it is the worst of four rules on the untouched window, and its mechanism —
   spend all the gross rule 2 allows — is the wrong direction against 4b's binding bar.
2. **What survives of idea 148/156 is the DIAGNOSTIC, not the rule.** `g_req = 0.75 x
   vol_SPY / vol_book` remains exactly what idea 156 showed it to be: a free number that says
   whether a book's CAGR shortfall is reachable under rule 2. Idea 165 (open) can still
   back-fill it as a leaderboard column. This run only denies that the same number should be
   used to SET the gross.
3. **The 0.75 in RULES is at the ladder's out-of-sample argmax, with a 0.70–0.75 plateau.**
   That is a stronger defence of the incumbent constant than the project had, and it is a
   by-product, not a fitted claim.

## Caveats carried

* **Survivorship:** B136 is a current-constituent list (idea 54). All four rules inherit it
  equally, so the comparison is fair, but every absolute pass rate here is flattered.
* The sub-panels overlap heavily by construction, so the 300 books are not independent; the
  t-statistics are magnitude cues.
* The ladder is 10 points from 0.20 to 1.00. A finer ladder would move MIDPOINT slightly; it
  cannot move CEILING, whose g is computed off-ladder and exactly.
* Idea 38 (calendar-day price index) and idea 126 (t+1 execution only) carry over unchanged.
* The k=20/n=20 cell holds every eligible name by construction (idea 78's own flag), so its
  numbers are a weighting result, not a selection result.
