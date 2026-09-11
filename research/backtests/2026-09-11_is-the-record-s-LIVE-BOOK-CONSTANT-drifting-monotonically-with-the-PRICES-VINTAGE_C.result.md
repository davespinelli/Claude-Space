# Idea 692 — is the record's LIVE BOOK CONSTANT drifting monotonically with the PRICES VINTAGE?

**2026-09-11, lane C. Verdict: ANSWERED / KILL OF THE MONOTONICITY PREMISE — but the queue's
*attribution* is CONFIRMED exactly.** No RULES change, no book promoted, no KEEP claimed, no
PROTOCOL edit applied; `RULES.md`, `PROTOCOL.md`, `scan.py`, `bot.py` and `baseline.py` untouched.

## What this run could do that the record could not

Ideas 514 and 519 both record that the sandbox clone is **shallow (50 commits)**: 514 reached
exactly ONE real vintage step and modelled the rest by truncation, and 519 priced the
restatement channel with **synthetic draws** calibrated to 514's published envelope. This run
starts with `git fetch --unshallow`, which exposes **all 8 committed vintages of
`data/prices.csv`** (2026-09-03 … 2026-09-10). Every number below is measured on the real
committed files, so the append channel and the restatement channel are separated without a
model of either.

## Gates (8, pre-registered, printed before any new number was read — ALL PASS)

| | gate | result |
|---|---|---|
| G1 | `fast_backtest` == `engine.backtest` @10 bps | 6.939e-18 |
| G2 | `band_book(0.03,0.75)` == `rules_v2_weights` | EXACT 0 |
| G3 | v8 reproduces idea 523's G3b live constant 8.61% / 1.1998 / −12.05% | max\|d\| **4.945e-05** |
| G4 | the 8 pinned commit hashes extract to the pinned (rows, cols, last date) | exact, 8/8 |
| G5 | weights are causal: `w(px[:d]) == w(px)[:d]`, both books | EXACT 0 |
| G6 | `TRUNC(v8,d)` is a value-for-value prefix of v8 | EXACT 0 |
| G7 | every universe ticker present in all 8 vintages | 56/56, 8/8 |
| G8 | weekend rows per vintage == pinned {v1:1248, v2:1248, v3..v8:0} | exact |

**G8 is load-bearing.** The panel was *rebuilt* on 2026-09-04: v1/v2 carry 1,248 weekend rows
(6,059/6,060 rows) and v3…v8 carry none (4,698…4,702 rows). A "vintage" step across that
boundary is a **construction break**, not appended days, and every table below marks it BREAK.
Reading it as drift would have produced a −0.226 Sharpe "vintage effect" that is nothing of the
kind.

## (A) The queue's attribution is confirmed, to five decimal places

| published reading | nearest rung on the real ladder | max \|d\| |
|---|---|---|
| idea 415 G2, read 2026-09-10: 8.66% / 1.2056 / −12.05% | **the 2026-09-04 vintage (v4/v5)** | 4.942e-05 |
| idea 523 G3b, read 2026-09-11: 8.61% / 1.1998 / −12.05% | **the 2026-09-10 vintage (v8)** | 4.945e-05 |

Both readings sit on the ladder exactly. The two vintages differ by **3 appended trading days**
(4,699 → 4,702 rows) and by nothing else: **every rung on the ladder starts at the same row date,
2009-01-13**, so idea 518's start-date channel is excluded by construction, not by argument. The
gap is 0.0058 Sharpe / 5 bps of CAGR with MaxDD identical — appended days, as 523 guessed.

## (B) …and the premise built on top of it is false: the drift is NOT monotone

| ladder | rungs | Spearman(end, Sharpe) | sign flips | Sharpe span |
|---|---|---|---|---|
| committed TRUNC (append only), LIVE | 8 | **−0.9386** | **0** | 0.0077 |
| committed TRUNC, CAND20 | 8 | −0.5581 | 2 | 0.0025 |
| long append ladder U56, LIVE | 355 | **+0.5222** | **178 of 354** | 0.2924 |
| long append ladder U56, CAND20 | 355 | +0.7045 | 183 | 0.2022 |
| long append ladder B136, LIVE | 355 | +0.2202 | 175 | 0.3067 |
| long append ladder B136, CAND20 | 355 | +0.1562 | 193 | 0.3396 |

On the 8 committed rungs the live book's Sharpe looks perfectly monotone-decreasing (ρ −0.9386,
zero sign flips) — which is exactly what the queue expected. **That appearance is an artefact of
a 5-trading-day window with 4 distinct end-dates.** Extend the same append channel to 355 rungs
(month-ends 2017-01…2026-08 plus every one of the last 252 trading days, v8 truncated, so
restatement is zero by construction) and the increment changes sign at **178 of 354 steps
(50.3%)** — a coin flip — *and the trend reverses*: ρ goes from −0.94 to **+0.52**. "Sharpe decays
with appended days" is the wrong generalisation of a four-point sample; over nine years of rungs
it rises, and over any given week it does whatever that week did. A (constant, vintage) pair is
the right bookkeeping; a (constant, vintage) *extrapolation* is not available.

## (C) Shelf life — param 2 (GATE BAR) × vintage, the actionable output

First appended trading day at which \|dSharpe\| from the final rung exceeds the bar:

| bar | U56 LIVE | U56 CAND20 | B136 LIVE | B136 CAND20 |
|---|---|---|---|---|
| 5e-4 | 1 | 1 | 1 | 1 |
| 1e-3 | 1 | 1 | 1 | 1 |
| **5e-3** (the record's usual gate bar) | **3** | 27 | 16 | 17 |
| 1e-2 | 67 | 67 | 86 | 40 |
| 2e-2 | 110 | 108 | 105 | 64 |
| 5e-2 | never in 252d | never in 252d | never in 252d | 243 |

**At the record's standard 5e-3 gate bar a live-book constant has a shelf life of three trading
days.** At 1e-3 it is one day. Any gate that quotes a constant to 4 decimals and does not carry
its vintage is, at these bars, unfalsifiable after a week. (Recommendation for the Sunday review
under PROTOCOL rule 6 — *not* applied here: a published constant at a bar ≤ 5e-3 should carry the
prices.csv end-date it was read at. No PROTOCOL edit is made by this run.)

## (D) The restatement channel, measured instead of modelled — 519's conclusion survives

`TRUE − TRUNC` at a shared end-date is the restatement channel alone (same days, same book, one
file restated relative to the other). Over the 12 same-construction rows:

**max \|dSharpe\| 0.0003 · max \|dCAGR\| 0.0037% · max \|dMaxDD\| 0.0000% · 4b verdict flips 0 of 16.**

Idea 519 reached "the restatement channel is verdict-inert" with synthetic draws; it is now
confirmed on the real committed files with no model in between.

**One correction to the record's envelope.** Idea 514 published max \|dreturn\| = 3.000e-04 and 519
calibrated its draws to it. Measured on same-construction pairs the envelope actually spans
**5.331e-05 … 7.713e-02** (0.18× … 257×). The wide end is v1→v2 on **PLTR**, with only **60 of
40,161** moving cells above 1e-4 — i.e. the **sparse-large corner 519 explicitly recorded as
untested is not hypothetical; it is in the record's own committed files.** Priced on the book it
is small but not zero: **+0.0034 Sharpe (LIVE), +0.0031 (CAND20)** — clears a 5e-3 bar, fails 1e-3.
519's dense-small result stands; its "DENSE-SMALL, NOT SPARSE-LARGE" caveat now has a number.

## (E) Rule 8 walk-forward (required) — the vintage treated as the dial the chooser tunes

Chooser picks the rung with the highest IS Sharpe (through 2016-12-31); the pick is read on
2017-2026 untouched.

| book | channel | pick | IS spread | IS spread ex-BREAK | OOS CAGR / Sharpe / MaxDD | OOS spread over rungs | blind-v8 cost |
|---|---|---|---|---|---|---|---|
| LIVE | TRUE | v4 | 6.40e-02 | 2.47e-06 | 9.53% / 1.2851 / −12.05% | 3.50e-01 | +0.0104 |
| LIVE | TRUNC | v1 (tie) | **0.00e+00** | 0.00e+00 | 9.53% / 1.2851 / −12.05% | 1.38e-02 | +0.0104 |
| CAND20 | TRUE | v5 | 6.06e-02 | 3.63e-06 | 14.36% / 1.1680 / −18.31% | 1.92e-01 | +0.0032 |
| CAND20 | TRUNC | v1 (tie) | **0.00e+00** | 0.00e+00 | 14.35% / 1.1675 / −18.31% | 4.39e-03 | +0.0027 |

Comparands on the live vintage (v8), OOS 2017-01-01 → 2026-09-10:
**RULES v2 baseline 9.45% / 1.2747 / −12.05% · SPY 15.24% / 0.8721 / −33.72% · CAND20 14.31% /
1.1648 / −18.31%.**

**The vintage dial is a pure coin flip in-sample and still costs OOS.** On the append channel the
IS Sharpe spread across all 8 rungs is **exactly 0.00e+00** — appending days cannot touch
2009-2016, so the chooser has *literally no information*, and the "pick" is whichever rung the
sort visited first — while the OOS spread across rungs is 1.38e-2 (LIVE). Even on the TRUE ladder
the IS spread is 2.47e-06 once the construction break is excluded; the 6.40e-02 headline spread is
the BREAK, not restatement. This is idea 669's flip-rate concern in its purest form: a dial whose
IS signal is provably zero.

## (F) Both KEEP paths at every rung (PROTOCOL rule 4)

| book | 4a | 4b | 4b fail-sets seen |
|---|---|---|---|
| LIVE (RULES v2, the incumbent) | 0/16 | 0/16 | `CAGR` **alone**, at every rung |
| CAND20 (standing 2026-09-04 KEEP-4b candidate) | 0/16 | **16/16** | — |

**The 4b verdict is vintage-invariant within every (book, channel), the construction break
included.** The standing candidate does not owe its 4b pass to which day the price cache was
pulled, and the incumbent's 4b failure is the CAGR floor alone at every rung — restating idea
691's floor result on a ladder 691 did not have.

**NOTHING PROMOTED.** LIVE *is* the incumbent and CAND20 is the standing candidate; this run adds
no book and takes no KEEP. Its output is a measurement and a correction to the record's envelope.

## Caveats that limit what this proves

1. **Eight vintages over eight calendar days.** The committed ladder cannot distinguish a trend
   from noise — that is the run's own headline, and it applies to every committed-ladder number
   above, including the −0.9386.
2. **The long ladder is truncation.** It is the append channel *alone*; it says nothing about
   restatement, which is why (D) is measured separately on the real files.
3. **Survivorship (PROTOCOL 9).** U56 and B136 are today's constituents; every LEVEL above is
   biased upward and none is a tradeable estimate. The claims made are within-panel differences
   between two vintages of the same file over the same names, where the bias applies to both
   sides.
4. **B136 has no vintage ladder** — `data/prices_broad.csv` has 3 commits and has not moved since
   2026-09-04, so it carries the append ladder only, as a non-tuned replication.
5. **One-ticker corner.** The 7.713e-02 restatement is a single name (PLTR) on a single pair; it
   bounds the sparse-large corner from below, it does not characterise it.

## Artefacts

`2026-09-11_is-the-record-s-LIVE-BOOK-CONSTANT-drifting-monotonically-with-the-PRICES-VINTAGE_C.{py,result.md,console.txt,cells.csv,grid.csv,ladder.csv,monotonicity.csv,channels.csv,shelflife.csv,walkforward.csv}`
