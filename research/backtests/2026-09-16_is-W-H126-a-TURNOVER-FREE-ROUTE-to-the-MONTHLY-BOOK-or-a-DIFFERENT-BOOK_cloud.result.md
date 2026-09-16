# Idea 1064 — is W/H126 a TURNOVER-FREE ROUTE to the MONTHLY BOOK, or a DIFFERENT BOOK?

**cloud lane, 2026-09-16.** Script
`2026-09-16_is-W-H126-a-TURNOVER-FREE-ROUTE-to-the-MONTHLY-BOOK-or-a-DIFFERENT-BOOK_cloud.py`.
Two tuned dials: **gross rung {0.75, 0.65, 0.55, 0.45, 0.35} × overlap statistic {JACCARD,
OVERLAP_COEF, WEIGHT_L1}** — all points reported. Fixed (not dials): NTOP 20, max_vol 0.60,
10 bps, LAG 1, the CAND20 mechanism and canonical period-end dates (936's construction verbatim);
the books W/H126, M/H0, W/H0 are the objects, fixed by the queue text. R3_84 / MOMONLY are a
replication of the overlap reading, not a dial. 184 overlap rows, 920 ladder rows, 54 walk-forward
rows. **Gates 7 of 7 pass**, including G2 (936's three committed U56/CAND20 books reproduced to
1.4e-04 in CAGR/Sharpe/MaxDD/turnover), G4 (the live RULES v2 book's committed −12.05% MaxDD, to
5e-05), G5 (the two books 936 reports identical overlap at 1.000 every day) and G6 (every overlap
statistic identical at all five rungs, 2.2e-16 — **the two dials are orthogonal by construction**).

## (1) THE OVERLAP: NEITHER. W/H126 is a THIRD book, about 42% of the way from chance to identity

Median day-by-day overlap, U56 / CAND20 (B136 in brackets):

| pair | JACCARD | OVERLAP_COEF | WEIGHT_L1 | net-return ρ |
|---|---|---|---|---|
| **W/H126 vs M/H0** | **0.5455** [0.3333] | 0.7500 [0.5000] | 0.7000 [0.5000] | **0.9363** [0.8860] |
| W/H0 vs M/H0 (cadence-only anchor) | 0.7391 [0.6667] | 0.9000 [0.8000] | 0.8500 [0.8000] | 0.9516 [0.9443] |
| W/H126 vs W/H0 | 0.5385 [0.3333] | 0.7000 [0.5000] | 0.7000 [0.5000] | 0.8988 [0.8668] |
| M/H0 vs M/H5 (identity ceiling, G5) | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| i.i.d.-ranking NULL, W/H126 vs M/H0 (floor) | 0.2121 [0.0811] | 0.3500 [0.1500] | 0.3500 [0.1500] | 0.9252 [0.9120] |

Closed-form floor for two independent uniform 20-of-K subsets, E[∩]/E[∪]: **U56 0.2174, B136
0.0794** — the empirical null lands on it.

- **H_SAME FAIL** (0.5455 < 0.80; ρ 0.9363 < 0.95). **H_DIFF FAIL** (0.5455 > floor + 0.10 =
  0.3121). The reading rule was fixed before any number and the answer is **PARTIAL**: W/H126 sits
  **(0.5455 − 0.2121)/(1 − 0.2121) = 0.423** of the way from chance to identity on U56, and
  **0.274** on B136. It is not the monthly book by another route, and it is not a fresh draw.
- **H_MINHOLD_MOVES PASS** and it is the useful half: the ordinary weekly book already overlaps M
  at **0.7391**, and adding the min hold moves W *away* from M, to 0.5455. W/H126 is **equidistant
  from both parents** (0.5455 vs M, 0.5385 vs W/H0) — a third portfolio, sharing about half its
  names with each, not an interpolation between them.
- The return correlation is the trap: the null's two routes correlate at **0.9252** while holding
  only 21% of the same names, because a 20-name equal-weight basket of the same panel is mostly
  market. **A high return ρ is not evidence of the same book** — 0.9363 vs 0.9252 is almost the
  whole distance from the null, and this is worth carrying to any future "same book?" claim.

## (2) THE GROSS RUNG: NO. The window is EMPTY in 18 of 18 cells

The ladder is arithmetic (**H_ARITH PASS**: full-sample Sharpe span **0.0016** across the five
rungs — 1.1382 to 1.1397), so gross buys drawdown and sells CAGR, one for one:

| gross | CAGR | Sharpe | MaxDD | H1 / H2 | OOS CAGR / Sh / DD | 4b | 4a |
|---|---|---|---|---|---|---|---|
| 0.75 | 15.58% | 1.1397 | −19.13% | 1.204 / 1.097 | 16.97% / 1.164 / −19.13% | **PASS** | FAIL |
| 0.65 | 13.48% | 1.1394 | −16.73% | 1.203 / 1.097 | 14.68% / 1.164 / −16.73% | **PASS** | FAIL |
| 0.55 | 11.39% | 1.1390 | −14.29% | 1.203 / 1.096 | 12.39% / 1.163 / −14.29% | **PASS** | FAIL |
| 0.45 | 9.30% | 1.1386 | −11.81% | 1.203 / 1.096 | 10.11% / 1.163 / −11.81% | FAIL L_CAGR | FAIL |
| 0.35 | 7.22% | 1.1382 | −9.28% | 1.202 / 1.095 | 7.84% / 1.162 / −9.28% | FAIL L_CAGR | FAIL |

**H_RUNG FAIL.** The drawdown comes inside the live book's −12.05% only at g ≤ 0.473; 4b's CAGR
floor (0.70 × SPY's 15.10% = 10.57%) holds only at g ≥ 0.511. The two windows **do not meet**, on
**18 of 18** (2 panels × 3 mechanisms × 3 books) cells. At the lowest 4b-legal rung W/H126's
drawdown is **−13.03%, a 0.97 pp miss** — the smallest gap of the nine U56 cells (M/H0 misses by
1.56 pp, W/H0 by 3.15; B136 1.51 / 4.57 / 4.18).

**H_4A_LEG FAIL — the queue's premise is wrong.** W/H126 does not fail 4a on drawdown alone: at
gross 0.75 it fails **all three** legs (A_H1 1.204 vs the live 1.232, A_H2 1.097 vs 1.176, A_DD).
Because Sharpe is invariant along the ladder, **no gross rung can ever fix the two Sharpe legs** —
de-grossing was never going to deliver 4a for this book, and the 0.97 pp drawdown gap is the
second reason, not the first.

## (3) WHAT DE-GROSSING DOES DO: it moves 4b's COIN FLIP by 0.55

**H_NULL4A FAIL** (the honest direction): the gross-matched null's 4a pass rate is **0.000 at every
rung on U56**, because 4a is judged against a live book whose Sharpe is 1.20 — a random 20-name
basket never gets there. De-grossing does not hand 4a to a coin flip.

**H_NULL4B PASS, and it is the finding with teeth.** The same null's **4b** pass rate along the
identical ladder is **0.100 / 0.550 / 0.050 / 0.000 / 0.000** (U56, W/H126 construction, 20 seeds),
a span of **0.550**. 4b's base rate is a *gross-rung object*: at g = 0.65 a random book passes 4b
more often than not (the DD cap has eased while the CAGR floor has not yet bitten). W/H126's own
4b pass at g = 0.65 therefore sits in a cell where the coin flip passes **55%** of the time. This
extends the record's per-leg-null line (942/969/998) onto a dial nobody had walked.

## (4) RULE 8 (walk-forward, 2009–2016 → 2017–2026)

`C_ISSHARPE` hits the OOS-best rung in **0.889** of 54 cells and `C_ISDD` in **0.000** — but the
first number is an artefact and is reported as one: Sharpe is invariant along the ladder, so the
chooser is decided entirely by its declared tie-break (highest gross), which is the default. The
4a-targeting chooser `C_ISDD` picks g = 0.35–0.45 everywhere and **loses 4b in every cell**
(OOS 4b 0 of 18). OOS at the default rung, U56/CAND20: **W/H126 16.97% / 1.164 / −19.13%**,
M/H0 17.50% / 1.306 / −19.51%, against **SPY 15.21% / 0.8711 / −33.72%** and the **live RULES v2
9.45% / 1.2762 / −12.05%**.

## VERDICT — **KILL** the de-grossing route; **PARK** W/H126 where 936 left it

**ANSWERED: NEITHER.** W/H126 is not the monthly book reached by a cheaper route (median Jaccard
0.5455, not ≈1) and not a genuinely different portfolio (floor 0.2121) — it is a third book 42% of
the way from chance to identity, and further from M than the ordinary weekly book already was.
**KILL** the gross rung as a way to bring it inside the live book's drawdown: the window is empty
in 18 of 18 cells, the best miss is 0.97 pp, and 4a fails on both Sharpe legs where no rung can
help. **CONFIRM** that the ladder is pure arithmetic (Sharpe span 0.0016). **NEW:** 4b's own coin
flip moves 0.100 → 0.550 → 0.050 across three adjacent rungs, so a 4b pass quoted at one gross is
quoted at a base rate the gross chose. **Nothing promoted; no KEEP candidate; RULES.md untouched.**
Gates 7 of 7, hypotheses 3 of 8.

**Survivorship:** U56 and B136 are current-constituent panels. The bias is common to the books and
to the null and flatters both the CAGR floor and the DD cap against SPY, which is a real index.
**Resolution caveat:** 20 seeds per null cell put the base-rate grain at 0.05, so the null 4b
differences read here (span 0.550) are resolvable but their individual levels are ±0.11 at 2 SE.
