# Idea 1255 (lane cloud, 2026-09-17) — how much of the 2026-09-04 KEEP 4b book is the handful of names the screen already knows won?

**VERDICT: KILL (capital) — no new book. The committed 4b pass is worth about SIX NAMES, and the
damage is concentrated in names whose wins land in the OUT-OF-SAMPLE window, which is precisely
what a current-constituent panel encodes and rule 9 has never priced.**

## What was run
The frozen 2026-09-04 candidate (U56 / composite 21-252, 0-126, 0-63 / no vol scaler / above-own-200d
and vol20 < 0.60 / N=20 / H=126 / gross 0.75 / cash for gated-out weight / weekly, decide Friday and
trade Monday — idea 1253's G9 identity), 10 bps, t+1 execution, 260-row warm-up, **rebuilt from
scratch on a panel with the k ex-post best names DELETED ENTIRELY** — not un-selected: composite
ranks, eligibility, min-hold clock and every top-N slot are recomputed without them. k = 0, 1, 2, 3,
5, 8, 12 (dial 1) x deletion rule {TOTRET = highest full-sample total return, CONTRIB = highest
realised contribution to this book} (dial 2) x basis {FULL = the cheating order, **IS = the rule-8
order, chosen on warm-up..2016-12-31 only**} x 3 panels = **84 cells, all published** in `.grid.csv`;
deletion orders in `.deletions.csv`. **9 of 9 gates pass** — G3/G4: the k=0 cell reproduces the
committed anchor at 1.1480 / -19.13% exactly. 45s, offline, deterministic.

SPY is the benchmark on the same window and is never a panel constituent, so **the 4b bars do not
move with k** (MaxDD >= -20.23%, CAGR >= 10.54%, Sharpe > 0.9600/0.8171 halves and 0.8686 OOS).

## The names, and the ladder (U56)
Deletion order TOTRET/FULL: **AVGO, NVDA, TSLA, NFLX, AMD, AAPL, AMZN, SMH, LLY, V, GOOGL, MSFT.**
CONTRIB/FULL: **NVDA, NFLX, AMD, AVGO, AAPL, AMZN, XLK, GOOGL, META, TSLA, SMH, MSFT.**

| k | mean full CAGR (FULL basis) | example cell (TOTRET/FULL) | 4b |
|---|---|---|---|
| 0 | 15.71% | 15.71% / 1.1480 / -19.13%, OOS 17.16% / 1.1759 | **PASS** |
| 1 | 14.58% | 14.26% / 1.0801 / -18.79%, OOS 16.36% / 1.1570 | **PASS** |
| 2 | 13.56% | 13.32% / 1.0434 / -17.61%, OOS 14.65% / 1.0802 | **PASS** |
| 3 | 13.18% | 13.35% / 1.0674 / -17.61%, OOS 14.92% / 1.1263 | **PASS** |
| 5 | 11.69% | 11.64% / 0.9840 / -20.46%, OOS 13.53% / 1.0728 | fail (DD by 0.23 pp) |
| 8 | 10.87% | 10.58% / 0.9467 / -18.89%, OOS 12.34% / 1.0418 | fail (H1 0.9017 < SPY 0.9600) |
| 12 | 9.61% | 9.48% / 0.8632 / -21.07%, OOS 10.88% / 0.9414 | fail (H1, DD **and CAGR** — 9.48% < the 10.54% floor) |

**4b passes 14 of 28 U56 cells, 3 of 28 on B136, 0 of 28 on SMALL663; 4a passes 0 of 84.** The book
loses roughly **1.1 pp of full-sample CAGR per deleted name over the first three** and crosses 4b's
own CAGR floor between k = 8 and k = 12. The first leg to break is the **drawdown cap again** (as in
idea 1253) and it is **NON-MONOTONE in k** — CONTRIB/FULL fails at k=2 and k=3, passes again at k=5,
fails at k=8 — so the DD leg is not measuring a property that survives one name being removed. The
CAGR and Sharpe legs decay smoothly and are the honest reading of the ladder.

## Rule 8 — and this is the finding
When the deletion set is chosen **on the in-sample window only** (the k names that had already won by
2016-12-31, which is all a 2017 investor could know), U56 OOS Sharpe barely moves: **1.1759 at k=0 ->
1.1593 at k=12 (TOTRET/IS)**, and the OOS leg passes at **7 of 7 rungs on both large-cap panels**.
When the deletion set is chosen on the **full sample** — i.e. including names whose runs happened
AFTER 2017 — the same k=12 costs **1.1759 -> 0.9414, a drop of 0.2346 of OOS Sharpe**, ten times
larger. **The price of the panel is not "it holds past winners"; it is "it was allowed to hold names
that had not won yet in 2016 and went on to win by 2026".** That is exactly the information a
current-constituent list leaks and the one no walk-forward inside the panel can remove.

## What this does and does not say
It does not remove the bias — no delisted name can be added to a panel that never held one — so
these are **lower bounds** on its cost and the levels remain optimistic even at k=12. It does not
produce a new book and nothing is promoted. It does say the committed 4b pass is **not broad**: it
survives losing its three best names and does not survive losing its best eight, and its margin over
4b's CAGR floor (15.71% vs 10.54%) is about six names wide on a 55-name panel. On SMALL663 the
relationship **inverts** — deleting the ex-post winners RAISES OOS Sharpe (0.4534 -> 0.5303, rank
slope +0.99) — so concentration in known winners is a large-cap-panel property, not a property of
this book's mechanics. **PROPOSED for the Sunday review (rule 6) as wording only, never as a chooser:
rule 9's survivorship sentence should carry a NUMBER — the k at which the claim's own 4b pass dies —
whenever a memo is written on a current-constituent panel.** RULES.md, PROTOCOL.md, scan.py, bot.py
and baseline.py untouched.

## Survivorship (rule 9)
U56 and B136 are current-constituent lists; SMALL663 is a current sub-$2B screen (52 of 715 dropped
for `max_1d_move >= 1.0` before anything was computed). This run measures the bias's lower bound
rather than correcting it; every absolute level printed is optimistic and every 4b pass is an upper
bound.
