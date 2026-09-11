# Idea 684 (cloud) — does idea 153's OVERLAP ordering survive a k-MATCHED restatement?

**VERDICT: ANSWERED / NO — the ordering reproduces across the named panels and INVERTS the moment
k is held. A documented KILL of the published reading of S2 as a cap-mix property.**
No RULES change, no book promoted, no PROTOCOL edit. RULES.md, PROTOCOL.md, scan.py, bot.py and
baseline.py untouched.

Script `2026-09-11_does-idea-153-s-OVERLAP-ordering-survive-a-k-MATCHED-restatement_cloud.py`;
console + 4 CSVs (`.panels`, `.grid`, `.books`, `.walkforward`) committed.
Two parameters, both pre-declared, every grid point reported: **k ∈ {20, 40, 80, 120}** and
**q (small-cap share) ∈ {0, 0.25, 0.50, 0.75, 1.00}**, 6 seeded draws per cell (SEED 684), gross
fixed at the live 0.75, 10 bps, weekly, t+1. 120 matched panels + 3 named panels, 240 books.

## 1. Reproduction gates (recorded, non-raising)

| | k | Ebar | breadth | idea 525 published |
|---|---|---|---|---|
| U56 | 55 | 37.10 | 0.6746 | k 55, Ebar 36.14, breadth 0.6571 |
| B136 | 135 | 89.36 | 0.6619 | k 135, breadth 0.6619 **exact** |
| SMALL439 | 439 | 141.53 | 0.3224 | Ebar 141.53, breadth 0.3224 **both exact** |

44 small-panel names dropped by `max_1d_move >= 1.0` (idea 525 published 44). k matches exactly on
all three. U56's Ebar/breadth differ from 525 because this run starts **every** panel at 2010-01-01
for a matched window; SMALL439 and B136 already started there, which is why they are exact.

## 2. The published claim reproduces — on panels that differ in k by 8×

Idea 153's headline: S2 (mean |top20(INV) ∩ top20(NONE)|/20 over weekly rebalance days)
**U56 0.694 > B136 0.425 > SMALL439 0.269**, spread 0.425, read as "the vol scaler changes the
book more on low-breadth panels".

This run, named panels, matched window: **0.7956 / 0.5745 / 0.4010**, spread 0.3946 —
**ORDERING REPRODUCED** (levels higher, as in the 2026-09-09 lane-B rerun's 0.7983/0.5756/0.4010).
But those three panels differ in k by 8.0× (55 → 439), and top-N-of-k overlap falls with k by
arithmetic alone (the independence benchmark 20/k is 1.00 / 0.50 / 0.25 / 0.167 across this run's
k ladder).

## 3. The restatement: at matched k the ordering does not merely weaken, it REVERSES

S2, k in rows, q in columns (means over 6 draws; within-cell sd 0.003–0.026):

| k \ q | 0.00 | 0.25 | 0.50 | 0.75 | 1.00 |
|---|---|---|---|---|---|
| 20 | 1.0000 | 1.0000 | — | — | — |
| 40 | 0.8872 | 0.9067 | 0.9321 | 0.9460 | **0.9732** |
| 80 | 0.7312 | 0.7273 | 0.7312 | 0.7701 | **0.8701** |
| 120 | 0.6081 | 0.6039 | 0.6143 | 0.6433 | **0.7857** |

q moves breadth by the full published range inside every k row (0.68 → 0.32, i.e. it spans U56's
0.6746 to SMALL439's 0.3224), so the dial is doing what the named panels do. The published
ordering (high breadth → high overlap) holds at **0 of 4** matched widths; the **all-small** panel
has the **highest** S2 at every k where the cell is defined. Signed spread q=0 minus q=1:
**−0.0860 (k=40), −0.1389 (k=80), −0.1776 (k=120)** against the published **+0.425**.
k=20 is degenerate and is reported, not used: top-20 of 20 candidates is the whole panel (S2 ≡ 1),
and at q ≥ 0.5 fewer than 20 names are eligible on most days, so the cell is undefined.

Channel sizes: mean S2 spread **across k = 0.3192** vs **across the whole cap ladder at fixed
k = 0.1027**, a **3.11×** ratio, and the residual within-k channel has the **wrong sign**.
Log-log, pooled over the 94 defined panels: `log S2 = +0.888 − 0.3095·log k − 0.2440·log breadth`;
log k alone −0.2917, log breadth alone −0.1586; ρ(S2, k) **−0.887** vs ρ(S2, breadth) **−0.251**.
Inside each matched-k row ρ(S2, breadth) is **−0.96 / −0.81 / −0.84 (mean −0.871)** — the sign of
the published claim, **inverted**, at every width. Idea 525's direction (a width claim wearing a
breadth label) is confirmed on a third construction; its magnitudes (−0.919 / −0.421) are larger
than this run's because its k arm spanned only 40–100.

## 4. The books S2 is a proxy for (240 books, 10 bps, both KEEP paths)

**4a 0 of 240. 4b 15 of 240 (6.25%), and every pass sits at q ≤ 0.25** — 12 at q=0, 3 at q=0.25,
**0 at q = 0.50, 0.75, 1.00**. A fifth independent construction reproducing ideas 276/285/286/524:
the 4b footprint is a low-q object. By book, 4b **CAND20-NONE 10/120 vs CAND20-INV 5/120** — the
no-vol-scaler book (the 2026-09-04 KEEP 4b construction) passes twice as often, consistent with
the record's standing finding that the scaler cancels the signal.

S2 is a **weak** proxy for what it is quoted as measuring. dSharpe(NONE − INV) per panel: mean
−0.0086, median +0.0000, positive in 42 of 120. ρ(S2, |dSharpe|) = **−0.515** pooled — but that is
again the width channel: inside each matched-k row it is **−0.46 / +0.09 / −0.18 (mean −0.185)**.
Holding width, knowing S2 tells you almost nothing about how much the vol scaler costs the book.

## 5. PROTOCOL rule 8 (score variant chosen on 2009–2016, 2017–2026 read once, 20 cells)

Pooled OOS 2017–2026, equal weight over cells:

| | OOS CAGR | OOS Sharpe | OOS MaxDD |
|---|---|---|---|
| rule-8 pick | 7.49% | 0.639 | −27.93% |
| the rejected variant | — | 0.628 | — |
| RULES v2 (do-nothing) | 5.81% | **0.793** | **−13.71%** |
| SPY | **15.24%** | 0.872 | −33.72% |

The IS chooser picks **CAND20-INV in 18 of 20 cells** — i.e. rule 8 selects the vol scaler the
record has repeatedly shown to be noise — and buys **+0.0034 median OOS Sharpe** over the variant
it rejected (better in 10 of 20, a coin flip). The pick **beats RULES v2 in 0 of 20 cells**
(median −0.134) and **SPY in 4 of 20** (median −0.189). Another instance of the record's recurring
"a fitted dial loses to the incumbent".

## 6. What to carry forward

1. **Do not quote S2 as a panel property.** Any sentence of the form "the vol scaler changes the
   book more on small-cap / low-breadth panels" is reading 20/k. At matched width the effect is
   the opposite sign, at roughly a third the magnitude.
2. **Publish k beside every top-N overlap statistic**, as ideas 286/525 asked for n_elig — an
   overlap statistic without its k is uninterpretable.
3. Nothing here is a KEEP. The best 4b passer (CAND20-NONE, k=40, q=0, draw 3: CAGR 13.50%,
   Sharpe 1.1281, MaxDD −18.11%, H1 1.1957 / H2 1.0695, OOS 1.1491) is a 40-name **all-large-cap**
   draw, i.e. the standing candidate's own territory on a narrower panel, and does not beat it.

**SURVIVORSHIP (rule 9):** all pools are current constituents; the sub-$2B panel is a screen run
today, so q=1 **levels** are optimistic — which makes the direction of §3 conservative, since the
inversion says the optimistic panel has the **higher** overlap. The matched-k **contrasts** are the
part of this run that survives the caveat, not the levels.
