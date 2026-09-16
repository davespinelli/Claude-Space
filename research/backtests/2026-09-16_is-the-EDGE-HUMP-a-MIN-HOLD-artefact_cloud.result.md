# Idea 1086 (cloud lane, 2026-09-16) — is the EDGE HUMP a MIN-HOLD artefact?

**ANSWERED = IT SPLITS BY PANEL, AND THE HOLD IS NOT A MONOTONE DIAL.** On **B136 the queue is
right**: the EDGE peak moves LEFT as the hold shortens (argmax n = **10 → 5 → 5** at H = 126 / 63 /
21, `H_LEFT` PASS) and at **H = 63 the ladder is MONOTONE DECREASING in n** (`H_HUMP` FAIL) — the
hump collapses into exactly the slope idea 1082 killed, so **1082's CEILING verdict is partly an
artefact of its own frozen H = 126**. On **U56 the queue is wrong**: argmax reads **12 → 8 → 12**,
`H_LEFT` FAILS, the hump survives at every hold, and shortening H makes it *sharper*, not flatter —
EDGE(12) − EDGE(5) goes from **1.72 SE (NOT decisive) at H = 126 to 2.96 SE (DECISIVE) at H = 21**,
which is the staleness mechanism running backwards. The pre-named third outcome — a uniform level
lift — does not hold either (U56 mean ΔEDGE **+0.184 pp**, B136 **−1.135 pp**).

**A 4b PASS THAT IS RULE-8 REACHABLE, THE FIRST IN THIS FAMILY — AND IT IS PARKED, NOT PROPOSED.**
U56 **N = 12, H = 21** clears all five 4b legs full-sample and all three out of sample, and U56's
IS-only Sharpe chooser picks exactly that cell. It is parked on two stated grounds below. **No
RULES change, no book promoted, no PROTOCOL edit (rule 6); RULES.md, PROTOCOL.md, scan.py, bot.py
and baseline.py untouched.**

Script `research/backtests/2026-09-16_is-the-EDGE-HUMP-a-MIN-HOLD-artefact_cloud.py`, 8 CSVs,
console log committed. **Gates 10 of 10. Hypotheses 11 of 14.**

---

## SELECTION

The cloud lane takes the LAST eligible open idea. 1086 was the last line under `## Open` and names
no EDGAR / Form 4 / 8-K / options / spin-off / live-data source.

## THE TWO DIALS AND NO MORE (PROTOCOL rule 4)

**N** {5, 8, 10, 12, 15, 20, 25, 30, 40} — 1082's ladder verbatim — × **H** {21, 63, 126} = **27
cells per panel, 54 in total, ALL published** for the book and the null. **SEEDS ARE FROZEN AT 40**:
they were 1082's second dial and are not one here. Everything else stays at 936/1064/1071/1082's
construction: cap INF, CAND20 legs, max_vol 0.60, gross 0.75, W cadence, 10 bps, LAG 1.

**THE NULL DRAWS ARE PAIRED ACROSS H BY CONSTRUCTION.** The seed recipe is 1082's verbatim —
`md5(panel, N, "INF", s)`, with no H term — so the random rank matrix at a given (panel, n, s) is
the *same object* at all three holds and the min hold is then applied to it exactly as it is
applied to the book. Two consequences, both wanted: the H comparison is paired and carries less
noise than independent draws would, and the H = 126 column is **bit-identical to 1082's**, which is
what G5 checks.

## GATES — 10 of 10, printed before any result number

| gate | \|d\| |
|---|---|
| G1 fast runner ≡ `engine.backtest` (U56, N=20, H=126, cap INF) | 1.388e-17 |
| G1b `gross_rescaler(1.0)` ≡ `nrun` — the bisection kernel is the same book | 1.388e-17 |
| G2 CROSS-RUN vs 936/1071/1082's committed W/H126 N=20 triple | 3.183e-07 |
| G3 CROSS-RUN SPY OOS triple | 1.702e-04 |
| G4c \|MaxDD\| of the REBUILT null is monotone in λ (the bisection is well posed) | 0.000e+00 |
| **G5 CROSS-RUN 1082's committed H=126 EDGE ladder, BOTH panels (18 rungs)** | **4.798e-03** |
| G5b CROSS-RUN 1071/1082's committed U56 N=20 H=126 null median (CASH) | 2.202e-04 |
| G6 live RULES v2 MaxDD ≡ committed −12.05% | 4.949e-05 |
| G7 null draw is deterministic in its seed recipe | 0.000e+00 |
| G8 the H dial is LIVE (U56 turnover spread ≥ 1.0x/yr) | 5.739e+00 |

G5 is the one that matters for reading this run against 1082: all **18** committed H = 126 EDGE
rungs reproduce to **4.8e-03 pp**, the rounding of 1082's own published two decimals.

## THE ANSWER — THE EDGE LADDER AT EVERY HOLD (40 seeds, REBUILT convention)

**U56** — EDGE(n, H) in pp

| H | 5 | 8 | 10 | 12 | 15 | 20 | 25 | 30 | 40 | argmax |
|---|---|---|---|---|---|---|---|---|---|---|
| 21 | +5.967 | +6.193 | +7.353 | **+7.662** | +5.258 | +3.908 | +1.802 | +1.739 | +1.343 | **n=12** |
| 63 | +6.637 | **+8.070** | +6.799 | +5.358 | +4.630 | +2.123 | +2.271 | +2.075 | +0.147 | **n=8** |
| 126 | +5.950 | +5.351 | +6.205 | **+6.820** | +5.215 | +5.118 | +2.953 | +1.546 | +0.414 | **n=12** |

**B136** — EDGE(n, H) in pp

| H | 5 | 8 | 10 | 12 | 15 | 20 | 25 | 30 | 40 | argmax |
|---|---|---|---|---|---|---|---|---|---|---|
| 21 | **+8.074** | +4.842 | +5.544 | +4.597 | +3.072 | +4.398 | +3.370 | +1.594 | +0.799 | **n=5** |
| 63 | **+11.269** | +8.822 | +7.663 | +5.182 | +4.473 | +3.352 | +2.133 | +1.439 | +0.398 | **n=5** |
| 126 | +5.717 | +5.245 | **+8.324** | +6.520 | +6.834 | +4.932 | +4.269 | +2.811 | +1.853 | **n=10** |

Seed SE at H = 126 runs 0.09–0.48 pp per rung.

**`H_LEFT` PASSES on B136 and FAILS on U56.** **`H_HUMP` FAILS on exactly one of six (panel, H)
cells — B136 at H = 63, where the ladder is monotone decreasing from +11.269 at n = 5 to +0.398 at
n = 40.** That is the SLOPE story 1082 killed at H = 126, alive at a shorter hold on the broad
panel. **`H_E5` PASSES on both panels but means very different things**: B136 EDGE(5) runs
5.717 → 11.269 → 8.074 (a real lift), U56 5.950 → 6.637 → **5.967** — a rise of **+0.016 pp**
against a 0.383 pp seed SE, i.e. nothing.

**THE HOLD IS NOT A MONOTONE DIAL, AND THAT IS ITS OWN RESULT.** H = 63 is not between H = 21 and
H = 126 on either panel: U56's argmax reads 12 / 8 / 12 and B136's EDGE(5) is *highest* at the
middle hold. Any reading of the form "as H shortens, X" is therefore unavailable on this tape from
a three-point ladder, and the strongest version of the queue's claim — monotone in H — is supported
by neither panel.

## D1 — IS ANY PEAK MOVEMENT DECISIVE? (post-run, labelled as such)

EDGE at two cells differs only through the two null medians (the books are deterministic), so
SE(ΔEDGE) = √(SE_a² + SE_b²).

| cell | Δ | SE | σ | verdict |
|---|---|---|---|---|
| U56 H=126: EDGE(12) − EDGE(5) | +0.870 | 0.507 | 1.72 | NOT decisive *(1082's number)* |
| **U56 H=21: EDGE(12) − EDGE(5)** | **+1.696** | 0.574 | **2.96** | **DECISIVE** |
| U56 H=63: EDGE(8) − EDGE(5) | +1.433 | 0.560 | 2.56 | DECISIVE |
| U56 H=21: EDGE(12) − EDGE(20) | +3.755 | 0.397 | 9.46 | DECISIVE |
| B136 H=126: EDGE(10) − EDGE(5) | +2.607 | 0.579 | 4.50 | DECISIVE |
| B136 H=63: EDGE(5) − EDGE(20) | +7.917 | 0.460 | 17.21 | DECISIVE |

**The U56 row is the refutation of the queue's mechanism on that panel.** Under staleness,
shortening the hold should *shrink* the gap between the peak and n = 5, because a 21-day hold no
longer locks five names for half a year. It grows: 1.72 SE → 2.96 SE. The hold is doing something
real (turnover goes 3.04x → 7.19x/yr at n = 12) and what it does is make the ceiling *more*
visible, not less.

## THE LEVEL EFFECT — outcome (c), named in advance, and it does not hold either

ΔEDGE = EDGE(n, 21) − EDGE(n, 126), by n:

- **U56** +0.016 / +0.842 / +1.148 / +0.842 / +0.043 / −1.210 / −1.151 / +0.193 / +0.930 —
  7 of 9 positive, **mean +0.184 pp**, median +0.193.
- **B136** +2.357 / −0.403 / −2.780 / −1.922 / −3.762 / −0.534 / −0.900 / −1.217 / −1.054 —
  **1 of 9 positive, mean −1.135 pp**.

A shorter hold does not lift the edge uniformly. On B136 it *lowers* it everywhere except n = 5,
which is precisely why the peak moves there.

## RULE 8, BOTH KEEP PATHS, AND THE PARK

(n, H) chosen **jointly on IS 2009-2016 alone** by four choosers over the 27 cells; OOS 2017-2026
read **once**.

Benchmarks: **U56** SPY full 15.10% / 0.8829 / −33.72% (halves 0.9588/0.8207), OOS 15.21% / 0.8711
/ −33.72%; RULES v2 live full 8.62% / 1.2007 / −12.05%, OOS 9.45% / 1.2762 / −12.05%. **B136** SPY
full 15.16% / 0.8861 / −33.72%, OOS 15.33% / 0.8767 / −33.72%; RULES v2 full 7.98% / 1.0993 /
−12.24%, OOS 7.88% / 1.1059 / −12.24%.

| panel | chooser | pick | OOS CAGR / Sharpe / MaxDD | 4b full | 4b OOS | 4a |
|---|---|---|---|---|---|---|
| U56 | C_ISSHARPE | **n=12, H=21** | **17.57% / 1.1426 / −19.48%** | **Y** | **Y** | . |
| U56 | C_ISDD | n=40, H=21 | 13.01% / 1.1286 / −19.27% | Y | Y | . |
| U56 | C_ISEDGE | n=5, H=63 | 18.02% / 0.8998 / −26.26% | . | . | . |
| U56 | C_ISCAGR | n=5, H=63 | 18.02% / 0.8998 / −26.26% | . | . | . |
| B136 | C_ISSHARPE | n=5, H=63 | 20.46% / 0.9156 / −28.62% | . | . | . |
| B136 | C_ISDD | n=40, H=63 | 13.89% / 0.9641 / −28.28% | . | . | . |
| B136 | C_ISEDGE | n=5, H=63 | 20.46% / 0.9156 / −28.62% | . | . | . |
| B136 | C_ISCAGR | n=5, H=63 | 20.46% / 0.9156 / −28.62% | . | . | . |

**`H_WF` PASSES, 2 of 8 picks.** **`H_4A` PASSES — 0 of 54 cells clear 4a**, so the live book's
drawdown leg is a book fact, not an (n, H) fact, exactly as 1082 found. **`H_ISHOLD` FAILS: U56's
four choosers split 21/21/63/63 and B136's all pick 63** — the hold is not stably choosable out of
sample even when n is.

Grid totals: **U56 4b full 7 of 27, 4b OOS 7 of 27, 4a 0 of 27. B136 4b full 1 of 27, 4b OOS 2 of
27, 4a 0 of 27.** Every one of the eight full-sample passes binds on **drawdown**, by
**+0.061 to +1.103 pp** against the 20.23% cap, with CAGR margins of +1.49 to +7.14 pp.

### The candidate, and why it is PARKED

U56 **n = 12, H = 21**: full **16.80% / 1.1625 / −19.48%**, halves **1.248 / 1.102**, OOS
**17.57% / 1.1426 / −19.48%**, turnover **7.19x/yr** (72 bp/yr of drag at the binding 10 bps).
It clears all five 4b legs full-sample and all three out of sample, and U56's IS-only Sharpe
chooser picks it from 2009-2016 alone — **the first cell in this family that any honest IS-only
procedure reaches.** 1082 found three 4b passes and reached none of them.

It is **PARKED, not proposed**, on two grounds stated plainly:

1. **The binding leg is not decidable at this sample length.** Its drawdown margin is **+0.753 pp**
   against the cap, and idea 1083 measured the 90% width of exactly this quantity on exactly this
   tape at **4.1–7.2 pp**. The margin is a fifth of the ruler's smallest division.
2. **It does not survive the panel change.** The same (12, 21) construction on B136 reads
   16.41% / 0.9840 / −26.84% and fails 4b outright; B136's own IS choosers all pick (5, 63), which
   also fails. A rule that clears on one current-constituent panel and not the other is a cell, not
   a rule.

A memo with the exact RULES wording the candidate *would* take is written at
`2026-09-16_is-the-EDGE-HUMP-a-MIN-HOLD-artefact_cloud.memo.md` so Sunday review has it in hand.
**This run does not recommend it for capital.**

## D2 — THE λ ≤ 1 CLIP (post-run, carried from 1082)

A null draw already drier than the book enters unmatched at λ = 1 with its CAGR understated, which
**inflates** EDGE. Clip share by (panel, H, n) is in `…_cloud.diagnostics.csv`; it bites hardest at
the ends of the ladder, so it runs **against** every hump verdict above, and they survive it.

## SURVIVORSHIP (PROTOCOL rule 9)

U56 and B136 are **CURRENT-CONSTITUENT** lists. Every level here is optimistic and every 4b/4a
count is an **UPPER** bound. The book-vs-null contrast is drawn from the same pool over the same
tape and the bias very largely cancels out of EDGE; it does **not** cancel out of the 4b legs,
which are measured against SPY, a real index — so the parked candidate is flattered by it, which is
a third reason not to propose it.

## FOLLOW-UPS FILED

1093 (is the B136 H=63 MONOTONE ladder a genuine slope or the middle rung of a non-monotone H
dial), 1094 (does the U56 n=12/H=21 candidate survive 25 and 50 bps, given it turns over 2.4× the
H=126 book), 1095 (is the H dial non-monotone on a finer hold ladder, or is 63 simply mis-placed).
