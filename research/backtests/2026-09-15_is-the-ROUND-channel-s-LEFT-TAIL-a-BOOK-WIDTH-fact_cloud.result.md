# Idea 671 — is the ROUND channel's LEFT TAIL a BOOK-WIDTH fact?

**cloud lane, 2026-09-15 · ANSWERED = YES, DECISIVELY · KILL for capital.**
No RULES change, nothing promoted, no PROTOCOL edit; `RULES.md`, `PROTOCOL.md`, `scan.py`,
`bot.py` and `baseline.py` untouched.

## What was run
The ROUND channel is idea 668's: a rule-8 chooser reads each rung's **in-sample** Sharpe, rounds it
to `dp` decimals, then takes the argmax with ties broken to the smallest rung index. Coarse
rounding manufactures ties, so the tie-break — not the evidence — picks the book. `dp=10` is the
honest control.

57 sites = 3 panels (U56 55 names, B136 135, SMALL 663 after the `max_1d_move >= 1.0` cut) × 6 dials
× 3 committed context rungs, **plus 3 U56-only SLEEVECAP sites**; × 5 decimal levels = **285
cells**, 420 rung-rows, all published.

Exactly two tuned parameters, both the queue's own, all points reported:
1. **DIAL CLASS** ∈ {WIDTH: `N`, `COVERAGE`, `VOLBREADTH` (+ `SLEEVECAP`); NONWIDTH: `BAND`,
   `GROSS`, `CADENCE`} — the queue's own partition, declared before any number.
2. **DECIMALS** `dp` ∈ {10 (control), 3, 2, 1, 0} — 668's own ladder.

The queue's third width dial, **sector cap**, exists only as `research/universe.json`'s four sleeves
and therefore runs on **U56 alone**: `universe_broad.json` is a flat list and the small panel has no
group map. Nothing was fabricated to fill the gap.

**Gates, all PASS before any new number:** `fast_backtest` == `engine.backtest` @10 bps 8.674e-18;
`band_book(0.03,0.75)` == `rules_v2_weights` 0.000e+00; determinism 0.000e+00; control identity
(dp=10 argmax == unrounded argmax) at **every** site. **G3 reproduces idea 668's headline
observation on all four tape vintages**: U56 / N dial / gross 0.75 / dp=0 moves the pick **50 → 3**
with dOOS Sharpe **−0.4651 (today), −0.4594, −0.4602, −0.4560** against 668's committed **−0.4617**
(best residual 1.451e-03) — the first clean cross-vintage replication of that number.

## The answer: YES
dOOS Sharpe of the rounded pick against the dp=10 control, 216 non-control cells (SLEEVECAP apart):

| class | cells | median | mean | **min** | p05 | frac moved | **P(d ≤ −0.10)** | mean of negatives |
|---|---|---|---|---|---|---|---|---|
| **WIDTH** | 108 | 0.0000 | −0.0492 | **−0.5097** | −0.4910 | 0.231 | **0.139** | −0.3589 |
| **NONWIDTH** | 108 | +0.0007 | +0.0082 | **−0.0546** | −0.0260 | 0.630 | **0.000** | −0.0479 |

**The entire left tail below −0.055 is width dials.** NONWIDTH dials move the pick *more often*
(63% vs 23% of cells) and it costs essentially nothing; WIDTH dials move rarely and, when they do,
catastrophically. Per dial, min dOOS Sharpe: COVERAGE −0.5097, VOLBREADTH −0.5060, N −0.4671,
SLEEVECAP −0.0741 | BAND −0.0546, CADENCE −0.0428, GROSS 0.0000 (exactly — it cannot move width).

- **H_WIDTH CONFIRMED.**
- **H_TIE CONFIRMED, 93 of 93.** Every moved cell has ≥2 rungs tied at the rounded maximum
  (minimum 2). The channel has exactly one mechanism.
- **H_MEDIAN0 half-replicates.** 668's "median +0.0000" holds exactly for WIDTH; NONWIDTH's median
  is +0.0007, not 0. Stated as measured.
- **H_MEASURE FALSIFIED — the queue's classification was right and my doubt was wrong.** Measured
  mean *relative* width spread within a site: COVERAGE 2.056, N 2.049, SLEEVECAP 1.074,
  VOLBREADTH 0.721 || **BAND 0.092**, CADENCE 0.018, GROSS 0.000. The band gate does not
  materially move how many names you hold.
- **H_SCALE CONFIRMED.** |Spearman(width jump, −|d|)| **0.857** vs |Spearman(IS-Sharpe spread,
  −|d|)| **0.256**. Damage tracks how far the *book* moved, not how flat the *evidence* was.
  (Statistics named per open idea 564: raw Spearman(width_jump, dOOS) is +0.0217 while
  Pearson is −0.7575 — the pair that disagrees most in the run, and a live example of 564's point.)
- **It is a dp=0 phenomenon.** By decimals, P(d ≤ −0.10) is 0.278 at dp=0, **0.000 at dp=1, 2 and 3**;
  min dOOS is −0.5097 / −0.0414 / 0.0000 / 0.0000.

## Rule 8 and the KEEP paths (every cell is a rule-8 pick; OOS read once per site × dp)
| dp | mean OOS CAGR | mean OOS Sharpe | mean OOS MaxDD | 4b OOS | 4a OOS |
|---|---|---|---|---|---|
| 10 (control) | 8.13% | 0.8744 | −19.36% | 9 | **0** |
| 3 | 7.99% | 0.8745 | −19.14% | 7 | 0 |
| 2 | 7.07% | 0.8747 | −17.44% | 6 | 1 |
| 1 | 6.83% | 0.8824 | −16.60% | 5 | 5 |
| 0 | 5.64% | 0.7848 | −15.41% | 2 | 4 |

Comparands on the same OOS window: **SPY** 15.27% / 0.8740 / −33.72% (U56 calendar), 15.33% /
0.8767 / −33.72% (B136, SMALL); **RULES v2** 9.46% / 1.2772 / −12.05% (U56), 7.88% / 1.1059 /
−12.24% (B136), 3.75% / 0.5600 / −13.89% (SMALL). Totals: 4a 10 of 285, 4b OOS 29 of 285 (25 at
25 bps), 4b FULL 35 of 285 (18 at 25 bps). **Rounding flips a 4b verdict in 16 of 228 non-control
cells (7.0%), always from pass to fail.**

**A second, unasked-for finding, reported because it is a PROTOCOL fact.** The control cells pass
4a **0 times in 57**; coarse rounding *manufactures* **10** 4a passes — every one of them by
de-grossing (picks: gross 0.20, band 0.00, cadence D, all at context gross 0.50, OOS CAGR 1.1% to
7.9%). 4a's MaxDD leg is judged against the low-return live book, so a rounding artefact that
shrinks the book buys the verdict. This is ideas 679/771's de-grossing result arriving through a
channel that has nothing to do with the strategy.

## Why nothing is promoted
All nine control-cell 4b passes are U56 (eight) or B136 (one) band/breadth books at gross 0.75–1.00 —
the standing exposure family, and today's idea 862 run showed on an overlapping corpus that a
matched-gross twin reproduces their OOS Sharpe to **+0.0010** and fails 4b on the drawdown leg
alone. Nothing here is a new candidate.

## Caveats
**SURVIVORSHIP:** all three panels are current-constituent lists, so every CAGR and drawdown LEVEL
is optimistic; this run measures a DIFFERENCE between two readings of the *same* books, which is
survivorship-neutral. SLEEVECAP is U56-only (12 cells) and its sleeves are asset-class sleeves, not
GICS sectors — it is corroborating, not load-bearing. Idea 835's 2020-dependence caveat applies to
every MaxDD comparison.

## What the record should take from this
A published rule-8 pick on a **width** dial needs its IS read quoted at enough precision to break
its own ties: at dp=0 the tie-break silently swaps a 38-name book for a 3-name book and costs half a
unit of OOS Sharpe, while the same coarseness on band, gross or cadence costs nothing measurable.
The cheap protection is the tie count, which this run shows is *necessary and sufficient* for the
channel to bite (93 of 93): **publish the number of rungs tied at the chooser's maximum beside every
rule-8 pick, and state the read's precision.**
