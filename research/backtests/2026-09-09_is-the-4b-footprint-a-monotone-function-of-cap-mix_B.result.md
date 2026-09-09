# Idea 285 — is the 4b footprint a monotone function of cap mix? (lane B, 2026-09-09)

**VERDICT: ANSWERED / KILL as a book, and the queue's word is upheld as a TREND but not as a
THRESHOLD. Yes, the 4b footprint is monotone in cap mix: 11 of the 12 (leg × book size)
pass-rate curves are statistically consistent with a monotone non-increasing truth once
12-draw binomial noise is priced, and every leg's slack falls in q (Spearman −0.33 to −0.91
over 252 cells). But the LEVEL curve wiggles at every rung — 3 to 7 of its 20 steps go the
wrong way — because the binomial sd of a rate at 12 draws is 0.144, larger than most steps of
the fitted curve. So an admissibility CURVE is publishable; an admissibility CUTOFF is not.
The binding order at n=20 is H2 ≈ CAGR (q=0.20) → OOS (0.40) → H1 (0.50) → DD cap (0.90):
the drawdown cap is the LAST leg to bind along the cap axis, not the first — and it is the one
leg whose curve does NOT replicate out of sample (Spearman +0.16), because the cap itself is
11.16% inside 2010–2016 and 20.23% inside 2017–2026.** No RULES change, no book promoted, no
memo. 4a passes **0 of 504** mix cells. `RULES.md`, `PROTOCOL.md`, `scan.py`, `bot.py`,
`baseline.py` untouched.

Script `2026-09-09_is-the-4b-footprint-a-monotone-function-of-cap-mix_B.py`.
Tuned parameters (PROTOCOL rule 4, max 2): **q** (21 rungs) and **n** (book size, 2 values).
All 504 mix cells + 10 named cells are reported (`.grid.csv`); aggregates in `.curve.csv`,
`.binding.csv`, `.monotone.csv`, `.walkforward.csv`, `.console.txt`.
10 bps, weekly, next-day execution. k=40 names per panel, 12 draws per rung, seed 285.

## Gates

- **G0** `fast_backtest` (vectorised twin) vs `engine.backtest`: max |dret| **1.39e-17**
  (CAND20) / **1.04e-17** (v2), max |dturnover| **2.50e-16** / **2.22e-16**, over 4192 of 4194
  rows. The 2 excluded rows precede the first rebalance, where `engine.backtest`'s `w_target`
  is `shift(1)`-ed to all-NaN so its turnover — and therefore its return — is undefined; they
  sit 258 rows before any evaluation window starts.
- **G1** idea 276 replayed at **its own** settings (seed 2026, q step 0.1, 6 draws, k=40):
  4b **3/66 at n=10** and **16/66 at n=20**, both digit-exact against its published footprint,
  max q of a pass 0.3 / 0.5 against its published "every pass at q ≤ 0.5". The parent
  reproduces exactly, so the finer sweep below is an extension of it, not a re-derivation.

## PART A — the admissibility curve

Per-q pass rate of each 4b leg, 12 draws per rung, **CAND20** (full table for both book sizes
in `.curve.csv`; the n=10 table is in the console):

| q | H1 | H2 | OOS | DD | CAGR | joint 4b | 4a |
|---|---|---|---|---|---|---|---|
| 0.00 | 0.917 | 0.667 | 0.833 | **1.000** | 0.667 | 0.667 | 0 |
| 0.05 | 1.000 | 0.917 | 0.917 | **1.000** | 0.917 | 0.917 | 0 |
| 0.10 | 1.000 | 0.667 | 0.917 | **1.000** | 0.833 | 0.667 | 0 |
| 0.15 | 0.917 | 0.667 | 0.750 | **1.000** | 0.833 | 0.583 | 0 |
| 0.20 | 0.833 | 0.333 | 0.583 | **1.000** | 0.333 | 0.250 | 0 |
| 0.25 | 1.000 | 0.333 | 0.667 | **1.000** | 0.500 | 0.333 | 0 |
| 0.30 | 0.917 | 0.583 | 0.583 | **1.000** | 0.333 | 0.333 | 0 |
| 0.35 | 0.917 | 0.250 | 0.500 | **1.000** | 0.500 | 0.250 | 0 |
| 0.40 | 0.583 | 0.083 | 0.083 | 0.833 | 0.083 | 0.083 | 0 |
| 0.50 | 0.250 | 0.250 | 0.250 | 0.750 | 0.000 | 0.000 | 0 |
| 0.60 | 0.333 | 0.000 | 0.000 | 0.750 | 0.000 | 0.000 | 0 |
| 0.75 | 0.167 | 0.000 | 0.000 | 0.500 | 0.000 | 0.000 | 0 |
| 0.90 | 0.000 | 0.000 | 0.000 | 0.167 | 0.000 | 0.000 | 0 |
| 1.00 | 0.000 | 0.000 | 0.000 | 0.167 | 0.000 | 0.000 | 0 |

**Where each leg first binds**, with a bootstrap p10–p90 (resampling the 12 draws inside each
rung, 1000 reps) on the q at which the rate first falls below 0.5:

| leg | CAND20 q\* | bootstrap p10–p90 | CAND10 q\* | bootstrap p10–p90 |
|---|---|---|---|---|
| H2 | **0.20** | [0.10, 0.25] | 0.00 | [0.00, 0.05] |
| CAGR floor | **0.20** | [0.20, 0.30] | 0.40 | [0.20, 0.45] |
| OOS | **0.40** | [0.20, 0.40] | 0.00 | [0.00, 0.10] |
| H1 | **0.50** | [0.40, 0.50] | 0.40 | [0.20, 0.45] |
| DD cap | **0.90** | [0.75, 0.90] | 0.00 | [0.00, 0.00] |
| joint 4b | **0.20** | [0.10, 0.20] | 0.00 | [0.00, 0.00] |

Two things to read off this. First, **the DD cap is the last leg to bind, by a wide margin**:
at n=20 it is the only leg with a perfect 12/12 pass rate from q=0.00 all the way to q=0.35,
and it does not fall below half until q=0.90. The joint 4b path along the cap axis is decided
by the half-Sharpe legs and the CAGR floor, not by drawdown. Second, **there is no curve at
all at n=10**: every leg is already below a perfect rate at q=0.00, three of the five are
already below half there, and joint 4b never exceeds 0.25 at any rung (9 passes in 252 cells).
The admissibility curve is a property of the (book size, cap mix) pair, not of cap mix alone.

Slack in each leg's own cross-draw sd, n=20 (positive = passing): the DD leg is the only one
still positive at q=0.85 (+0.15) while H2/CAGR/OOS are at −1.5 or worse.

## PART B — monotone?

| | CAND10 | CAND20 |
|---|---|---|
| joint-4b up-steps (of 20) | 4 | 3 |
| Spearman(q, joint 4b) | −0.1766 | −0.5790 |
| Spearman(q, slack) H1 / H2 / OOS / DD / CAGR | −0.78 / −0.63 / −0.71 / −0.66 / −0.78 | −0.84 / −0.80 / −0.86 / **−0.33** / **−0.91** |

The level curve is not literally monotone anywhere. **PART B3 asks whether it could be**:
PAVA fits the best monotone non-increasing curve, then 2000 binomial re-draws from that fit
(12 per rung) give the up-step count a truly monotone curve would show at this sample size.

**11 of 12 curves are consistent with monotone** (p = 0.121 to 0.872). The single rejection is
CAND20's H2 leg at **p = 0.042** — which is one rejection in twelve tests at the 5% level,
i.e. exactly the false-positive rate, so it is not evidence of a real non-monotonicity. Max
|observed − monotone fit| is 0.083 to 0.250. The binomial sd of a rate at 12 draws is **0.144**,
larger than most single steps of the fitted curve: that, and not a real reversal, is what the
wiggle is. **A publishable admissibility curve needs many more than 12 draws per rung to
resolve a threshold; at 12 it resolves only a gradient.**

**Which leg is closest to binding, raw units vs noise units** (idea 253's question, now along
the cap axis rather than the k axis): at n=20 the raw-unit argmin is H2 130 / H1 40 / CAGR 34 /
OOS 30 / DD 18, the noise-unit argmin is H2 127 / CAGR 74 / H1 24 / DD 17 / OOS 10, and the two
units **agree on only 60.3%** of 252 cells (76.2% at n=10). Idea 253's conclusion — "which bar
was closest is a fact about the units, not about the record" — reproduces on a completely
different axis.

## PART C — rule 8 walk-forward

**C1, does the curve replicate?** The four window-computable legs, re-derived inside IS
2010–2016 and inside OOS 2017–2026 (the OOS leg is undefined inside a window):

| leg | CAND20 IS q\* | OOS q\* | Spearman(IS curve, OOS curve) |
|---|---|---|---|
| H1 | 0.70 | 0.45 | **+0.8925** |
| H2 | 0.20 | 0.20 | **+0.9097** |
| CAGR | 0.45 | 0.20 | **+0.8172** |
| DD | 0.00 | 0.90 | **+0.1573** |
| joint 4-leg | 0.00 | 0.20 | +0.7583 |

**The shape of the curve replicates for every leg except the drawdown cap.** The reason is
mechanical and worth recording: SPY's own MaxDD is **−18.61% inside 2010–2016** and **−33.72%
inside 2017–2026**, so 4b's cap (0.60 × SPY) is **11.16% in-sample and 20.23% out-of-sample** —
1.8× looser — and the leg that looks hardest in-sample is nearly free out of sample. Every mix
book's full-sample MaxDD equals its OOS MaxDD to four decimals (e.g. −0.1785 at n=20, q=0.15),
i.e. **every one of these books takes its worst drawdown inside the OOS window**. This is
independent corroboration of open queue idea 518 (the DD leg of both KEEP paths is decided by
two crash episodes, not by the book) on a corpus it was not built from.

**C2, the book test.** q chosen on IS 2010–2016 by argmax mean IS Sharpe; OOS read once.

| | CAND10 | CAND20 |
|---|---|---|
| IS argmax q\* | 0.05 | 0.15 |
| OOS CAGR | 13.04% | 11.18% |
| OOS Sharpe | 0.9125 | 0.9891 |
| OOS MaxDD | −21.81% | −17.85% |
| anchor (mean OOS Sharpe over all 21 rungs) | 0.6525 | 0.7072 |
| RULES v2 OOS, same panels | 1.1334 | 1.0606 |
| SPY OOS | 0.8820 | 0.8820 |
| draws beating RULES v2 OOS | 0/12 | 2/12 |
| draws beating SPY OOS | 9/12 | 9/12 |
| 4b / 4a at q\* | 1/12 · 0/12 | 7/12 · 0/12 |
| Spearman(IS q-curve, OOS q-curve) | +0.9377 | +0.9325 |

Full sample at the chosen cell (CAND20, q=0.15, mean of 12 draws): CAGR 11.12%, Sharpe 1.0034,
MaxDD −17.85%, halves **1.1328 / 0.8846**, against RULES v2 on the same panels 1.0707
(1.1849 / 0.9575, MaxDD −12.11%) and SPY 0.8616 (CAGR 14.13%, MaxDD −33.72%).

**Choosing q generalises; the book it chooses does not clear the bar.** The IS q-curve ranks
the rungs almost perfectly for OOS (+0.93 at both book sizes) and beats the do-nothing anchor
by 0.26–0.28 of Sharpe, so cap mix is a genuinely selectable panel property. But the selected
book still loses to the live RULES v2 on the same panels out of sample (0.989 vs 1.061; 2 of 12
draws win) and its full-sample MaxDD is 47% worse than v2's, so **4a fails on 504 of 504 mix
cells** and 4b at the chosen rung passes only 7 of 12 draws. There is nothing here to promote.

## Named reference panels (not part of the sweep)

| panel | n | CAGR | Sharpe | MaxDD | H1 | H2 | OOS Sharpe | v2 Sharpe | 4a | 4b |
|---|---|---|---|---|---|---|---|---|---|---|
| U56 | 20 | 12.7% | 1.097 | −18.1% | 1.102 | 1.098 | 1.167 | 1.211 | no | **yes** |
| B136 | 20 | 13.1% | 0.959 | −20.1% | 1.125 | 0.815 | 0.895 | 1.108 | no | no |
| BSTK100 | 20 | 13.9% | 1.003 | −20.4% | 1.181 | 0.843 | 0.941 | 1.156 | no | no |
| ETF36 | 20 | 6.6% | 0.805 | −15.2% | 0.766 | 0.841 | 0.915 | 0.813 | no | no |
| SMALL | 20 | 6.7% | 0.472 | −27.4% | 0.604 | 0.364 | 0.501 | 0.571 | no | no |

The one 4b pass (U56 CAND20) is the cell ideas 276 and 286 already publish; it is reproduced
here, not discovered, and it still loses to RULES v2 on its own panel on every leg of 4a.

## Caveats

- **SURVIVORSHIP** (PROTOCOL rule 9): the small panel and broad136 are CURRENT constituents of
  their screens, so every small-cap number is biased upward by an unknown amount. Since the
  small-cap end is where 4b *fails*, the true curve is if anything steeper than the one above,
  not flatter — but no level here should be read as tradable.
- 12 draws per rung is enough for the gradient and not for a cutoff; the bootstrap intervals
  above are the honest width of each published binding point.
- SPY is identical across all 504 mix cells (one common calendar, 2010-01-04 to 2026-09-04),
  so the 4b bars themselves do not move along the sweep — only the books do.

## Cross-lane check (added at merge)

The cloud lane answered idea 285 the same day from an independent design
(`2026-09-09_is-the-4b-footprint-a-monotone-function-of-cap-mix_cloud.py`: 21 rungs × **20**
draws × 4 arms, ETFs excluded from the large pool). Its `top20` arm is the closest analogue to
this run's CAND20. Comparing the two lanes' published binding points (q at which each leg's
pass rate first falls below 0.5):

| leg | lane B (12 draws) | bootstrap p10–p90 | cloud `top20` (20 draws) |
|---|---|---|---|
| H2 | 0.20 | [0.10, 0.25] | 0.30 |
| CAGR floor | 0.20 | [0.20, 0.30] | 0.35 |
| OOS | 0.40 | [0.20, 0.40] | 0.35 |
| H1 | 0.50 | [0.40, 0.50] | 0.55 |
| DD cap | **0.90** | [0.75, 0.90] | **0.85** |
| joint 4b | 0.20 | [0.10, 0.20] | 0.20 |

Every cloud value is inside or one rung outside this run's bootstrap interval, and the two
lanes agree on the two structural claims: **the DD cap binds last at n=20 and first at n=10**
(the cloud lane's `top10` DD cap binds at q=0.00, as this run's CAND10 does), and the binding
ORDER therefore reverses with book size, so there is no single admissibility curve. The lanes
also agree that wrong-way steps appear on every leg of every arm. They differ only in what to
conclude from that: at 20 draws the cloud lane reads the wrong-way steps as evidence that
"monotone" is a coarse-rung statement; the PAVA + binomial test here shows that at 12 draws
those same wrong-way steps are what a genuinely monotone curve produces, so the finding is that
the level curve is under-resolved, not that the trend reverses. Both readings kill the same
thing — an admissibility CUTOFF — and neither promotes a book.
