# Idea 867 (lane B, 2026-09-15) — is the 4b DD CAP just a BETA CAP?

**ANSWERED = NO. The DD leg is a high-R² read of beta and still not a beta cap, and the gap is
exactly the size that decides the 4b shelf. KILL for capital (rule 8: 4a 0 of 12, 4b 0 of 12).**

No RULES change, no book promoted, no PROTOCOL edit applied (rule 6). `RULES.md`, `PROTOCOL.md`,
`scan.py`, `bot.py` and `baseline.py` untouched.

**SELECTION.** Taken as the last Open idea carrying a book to price. 904 / 903 / 896 / 895 / 894 /
877 / 876 sit below it with standing SKIP notes (prose or null-contrast censuses with no book, so
none can carry this run's mandatory rule-8 walk-forward); 869 is the same class and was given the
same note by this lane.

## What was asked

Ideas 662, 866 and 676 each found de-grossing buys drawdown and pays CAGR. If that is *all* the
DD leg sees, then `MaxDD(book) ≥ 0.60 · MaxDD(SPY)` is the constraint `beta ≤ 0.60` in a costume.
The equivalence is **exact on one ray and that is what makes the question sharp**: gate G4 shows
the zero-signal book `g × SPY` has FULL beta = g to 1.7e-03 and MaxDD ratio = g to 3.6e-02, so on
the cash/SPY ray the two caps *are* the same constraint. The question is only whether real books
depart from that ray by enough to flip the leg.

## Scale, dials, gates

336 real books + 48 controls (ZEROSIG, RANDGATE×3) on 3 panels × 4 families × 3 modes × 3 thetas
× 4 gross rungs, each scored on 3 windows with 4 beta estimators = 1,152 book-windows, 10 bps,
t+1, weekly. **TUNED 1** beta estimator {FULL, DOWN, ROLL, DDWIN}; **TUNED 2** panel {U56, B136,
SMALL}. Every one of the 12 grid points is reported below and in `.agree.csv` / `.matched.csv` /
`.residual.csv` / `.margin.csv`.

**GATES 5 of 5 PASS.** G1 TREND/ROW at g=0.75 ≡ `baseline.rules_v2_weights`, max|dw| **0.000e+00**.
G2 fast `Book.at` ≡ `engine.backtest`, max|dr| **1.041e-17**, max|dturn| **2.429e-16**. G3 U56
committed triples reproduced — SPY 15.13%/0.8845/−33.72% (committed 15.16%/0.8861/−33.72%),
RULES v2 8.62%/1.2013/−12.05% (committed 8.63%/1.2018/−12.05%). G4 the analytic ray, above.
G5 determinism, max|dSharpe| and max|dbeta| **0.000e+00**.

## H1 HOLDS — beta explains most of the variance

Spearman(beta, MaxDD), FULL window: U56 **−0.947 / −0.949 / −0.959 / −0.968**, B136 **−0.950 /
−0.957 / −0.941 / −0.949**, SMALL **−0.857 / −0.813 / −0.842 / −0.688** (FULL/DOWN/ROLL/DDWIN).
8 of 12 clear |ρ| ≥ 0.90 — **and all four misses are SMALL**, where R² falls to 0.54–0.77 against
0.85–0.92 on the two large-cap panels. The queue's premise is right about the *variance*: linear
R² 0.862–0.918 on U56/B136.

## H2, H2b, H3 FAIL — and the variance is not what decides a bar

Substituting `beta ≤ 0.60` for the DD leg agrees on **0.679 to 0.983** of books (H2: 2 of 12 cells
clear 95%). Even with **beta\* chosen to maximise agreement** — the most favourable beta cap that
exists, fitted on the answer — agreement tops out at 0.857–1.000, median **0.911** (H2b: 3 of 12).
Beta-matched pairs (|Δbeta| ≤ 0.02, same panel) land on **opposite sides of the DD leg 0.0%–19.4%**
of the time, with MaxDD differing by up to **34.1 pp inside a matched pair** (H3: 2 of 12).
Agreement is flat across cost rungs (0.818 / 0.812 / 0.798 at 0 / 10 / 25 bps).

**The mechanism, and it is arithmetic.** A bar is flipped by the residual, not by the R². Residual
SD is **2.19–7.16 pp of drawdown**; the median distance from the 0.60·MaxDD(SPY) bar is 6.79–8.81
pp; **10.7%–46.4% of books sit within one residual SD of the bar**. An R² of 0.87 is simply not
fine enough to reproduce a threshold at that resolution.

## The one place the two caps do coincide is circular

On B136 the **DDWIN** estimator — beta measured *inside the book's own peak-to-trough drawdown
window* — reads agreement **0.983**, best-case **1.000**, and matched-pair disagreement **0 of 109**.
That is the honest form of the queue's hypothesis: the DD leg *is* a beta cap when beta is measured
on the drawdown you are trying to predict. It is unusable for selection for the same reason it is
exact. On the three estimators anyone can compute ex ante, the equivalence does not hold.

## It reaches 4b, which is the leg that matters

Books where the swap would flip the **whole 4b verdict** (the DD leg differs *and* the other three
legs all pass): U56 **9 of 112** against **9 actual 4b passes**; B136 **6 of 112** (ROLL 8) against
**10 actual passes**. Swapping a beta cap in for the DD leg would rewrite most of the 4b shelf on
both large-cap panels. SMALL flips 0, because SMALL passes 4b 0 of 112 to begin with.

## H4 FAILS — the residual is not noise, it walks forward

MaxDD ~ beta fitted on **2009–2016 only**, the same coefficients read on 2017–2026 (rule 8):
ρ(resid_IS, resid_OOS) = **+0.343 to +0.590 on 9 of 12 cells** (U56 FULL +0.437, B136 FULL +0.536,
SMALL FULL +0.343); only ROLL on U56/B136 and DDWIN on B136 fall under the +0.30 bar. For scale,
ρ(MaxDD_IS, MaxDD_OOS) is +0.902–+0.974 and ρ(beta_IS, beta_OOS) +0.745–+0.987, so the panel is
stable and the residual is a persistent book property, not sampling noise.

## RULE 8 ON THE BOOKS — 4a 0 of 12, 4b 0 of 12

IS-only choosers on 2009–2016, OOS 2017–2026 read once, 10 bps, t+1, weekly:

| panel | chooser | book | OOS CAGR | Sharpe | MaxDD | H1/H2 | 4a | 4b |
|---|---|---|---|---|---|---|---|---|
| U56 | IS_SHARPE | TREND/AGG/th=0.2/g=1.00 | 16.41% | 1.075 | −29.18% | 1.184/0.955 | n | n |
| U56 | IS_DDRESID | TREND/AGG/th=0.4/g=1.00 | 15.69% | 1.200 | −23.59% | 1.306/1.083 | n | n |
| U56 | IS_LOWBETA | DISP/HYB/th=0.6/g=0.25 | 1.03% | 0.555 | −3.91% | 0.655/0.449 | n | n |
| U56 | IS_MAXDD | TREND/HYB/th=0.6/g=0.25 | 2.61% | 1.125 | −4.10% | 1.361/0.853 | n | n |
| B136 | IS_SHARPE | TREND/AGG/th=0.2/g=1.00 | 15.85% | 1.058 | −25.59% | 1.231/0.873 | n | n |
| B136 | IS_DDRESID | TREND/AGG/th=0.4/g=1.00 | 13.55% | 1.015 | −25.59% | 1.124/0.892 | n | n |
| SMALL | IS_SHARPE | VOL/AGG/th=0.2/g=1.00 | 12.52% | 0.673 | −37.13% | 0.932/0.447 | n | n |
| SMALL | IS_DDRESID | MOM/AGG/th=0.6/g=1.00 | 4.14% | 0.472 | −15.68% | 0.575/0.367 | n | n |

Comparands, same OOS window: **SPY 15.27% / 0.874 / −33.72%** (halves 0.980/0.759); **RULES v2
(live) U56 9.46% / 1.277 / −12.05%** (1.410/1.132), B136 7.88% / 1.106, SMALL 4.47% / 0.652.
Full 18 rows in `.walkforward.csv`.

**H5 FAILS, and it fails in the direction that corroborates H4.** The DD-residual chooser — which
the queue's hypothesis says should be picking from noise — beats the low-beta chooser on OOS Sharpe
at **2 of 3 panels**, and on U56 by 1.200 against 0.555 at 15.69% CAGR against 1.03%. A chooser
reading a quantity that does not exist cannot do that.

**And the near-miss is on theme.** U56 IS_DDRESID clears **three of the four 4b legs** — H1 1.306 >
0.980, H2 1.083 > 0.759, CAGR 15.69% ≥ 0.70·15.27% = 10.69% — and is rejected by **the DD cap
alone** (−23.59% against the −20.23% bar). It also fails 4a on Sharpe (1.200 < RULES v2's 1.277).
Not a KEEP-candidate, no memo, **not proposed**: the leg this run was sent to investigate is the
one that kills the run's own best book, which is the cleanest available demonstration that it is
not decoration.

## Verdict

**The 4b DD cap is not a beta cap.** It is 0.86–0.92 R² of one on large caps and 0.54–0.77 on
small caps, and the 8–14% of verdict it does not share with beta is concentrated exactly where the
shelf is decided: 9 of 112 U56 books and 6 of 112 B136 books would change their 4b verdict under
the substitution, against 9 and 10 actual passes. The residual is persistent out of sample
(ρ +0.34 to +0.59) and picks better books than beta does. **KILL for capital** — nothing on this
grid reaches either KEEP path out of sample — but the DD leg survives the audit and should not be
replaced by a beta constraint.

## Survivorship

U56 / B136 / SMALL are current-constituent lists (SMALL additionally drops the 52 tickers with
`max_1d_move` ≥ 1.0 per `data/small_meta.csv`), so every CAGR and drawdown **level** above is
optimistic — the books' and the comparands' alike. The agreement rates, matched-pair contrasts and
IS→OOS residual correlations are same-tape comparisons between books on one panel and are
unaffected.

## Follow-ups filed

909 (what is in the DD residual — is it left-tail shape, gate timing, or breadth), 910 (does the
DDWIN circularity have a non-circular ex-ante proxy), 911 (does the DD residual's IS→OOS
persistence survive an episode-preserving null).

Artifacts: `.console.txt` `.books.csv` (1,152 rows) `.agree.csv` `.matched.csv` `.residual.csv`
`.margin.csv` `.walkforward.csv`.
