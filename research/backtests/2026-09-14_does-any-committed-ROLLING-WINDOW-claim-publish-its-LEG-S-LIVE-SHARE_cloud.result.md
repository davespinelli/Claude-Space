# Idea 845 (cloud, 2026-09-14) — does any committed ROLLING-WINDOW claim in the record PUBLISH its leg's LIVE SHARE?

**ANSWERED: NO — 0 of 46 committed rolling-window claim files outside idea 843's own lineage print a live-share column, and the missing column is not cosmetic: it makes the record's two standing w1008 4b candidates look WORSE than they are.** Re-read on the leg where their own threshold exists, K8 goes 1.2223 → **1.3562** Sharpe and −14.79% → **−12.72%** MaxDD, and the B136 sibling 1.1121 → **1.2043**. Both keep 4b at 0, 10 and 25 bps on every leg. No RULES change, nothing promoted; RULES.md, scan.py, bot.py, baseline.py and PROTOCOL.md untouched (the proposed protocol line is a *proposal*, rule 6).

Script `2026-09-14_does-any-committed-ROLLING-WINDOW-claim-publish-its-LEG-S-LIVE-SHARE_cloud.py`; 810 book rows, 10 tuned census cells, all committed to `.books.csv` / `.cells.csv` / `.census.csv` / `.liveness.csv` / `.walkforward.csv` / `.console.txt`.

## Gates (printed before any number; all pass)
`fast_run` == `engine.backtest` on a real *gated* B136 book over 4,701 finite rows (the engine's 2 NaN warm-up rows named, both before the 260-day skip): max|dr| **1.388e-17**, max|dturn| **7.910e-16**. The committed B136 QROLL candidate reproduces its memo **EXACTLY** (14.3007% / 1.1121 / −17.3144% vs 14.30% / 1.1121 / −17.31%, max|d| 4.36e-05); **K8 reproduces NEAR, not exact** — 14.1541% / 1.2223 / −14.7912% against the memo's 14.16% / 1.2226 / −14.79%, max|d| **2.89e-04**, residual unexplained and stated (it is smaller than every verdict margin read below, and the MaxDD matches to the digit). G3 re-proves 843's inertness identity on 30 (panel, w, arm) dead regions: **max|d| 0.000e+00**. SPY reproduces the 4b comparand 15.1631% / 0.8861 / −33.7172%.

## (a) The column the record never prints
| panel | w252 | w504 | w756 | w1008 | w2016 |
|---|---|---|---|---|---|
| U56 / B136 FULL leg | 0.9998 | 0.9451 | 0.8884 | **0.8316** | **0.6048** |
| U56 / B136 PRE leg (≤2016) | 0.9995 | 0.8784 | 0.7529 | 0.6273 | **0.1251** |
| SMALL FULL / PRE | 0.9997 / 0.9993 | 0.9380 / 0.8375 | 0.8740 / 0.6698 | 0.8101 / **0.5020** | 0.5541 / **0.0000** |

First live day is 2011-12-30 for w1008 and 2016-01-05 for w2016 on the 2009-start panels. 843's 87.5%-dead PRE leg reproduces (1 − 0.1251).

## (b) The census: 4 of 50, all one lineage
50 files make a rolling-window claim under **LOOSE** (file-level co-occurrence of a rolling token, a named window length and a verdict word), 7 under **TIGHT** (one line carries all three). **4 of 50 LOOSE (0.0800) and 2 of 7 TIGHT publish a live-share token — and they are idea 843's script, its result memo, and the LEADERBOARD/CHANGELOG rows that quote it. Outside that lineage the count is 0 of 46.** So H_NONE is literally falsified by the run that found the problem and holds everywhere else. 27 of the 50 mention "warm-up" or `min_periods` *somewhere* without ever turning it into a share. All ten (reading × bar) cells are in `.cells.csv`; at the 0.90 bar **4 of 7 TIGHT (0.5714)** and 21 of 50 LOOSE claim files name a window whose FULL-leg live share is below it (H_ATRISK PASS). **Rule 8 on the claim** (reading chosen on the earlier dated half, later 23 files read once): publish-share 0.0000 → 0.0000, gap **0.0000** against a 0.10 bar — PASS, because the record is uniformly silent, not because it is stable.

## (c) The book leg — the dilution is real and it runs the RIGHT way
Every arm (3 q × 5 w × 2 depth × 3 panels × 3 rungs) priced on RAW (the record's convention), LIVE (starts the day its own threshold exists) and OOS legs. **4b passes 32/90 RAW, 32/90 LIVE, 35/90 OOS at 10 bps; 4a 0/90 everywhere** (the breadth gate never beats the live band book on drawdown). Across all 90 arms LIVE − RAW Sharpe is **+0.0176 mean / 54 of 90 positive**, and it is monotone in how dead the window is: +0.0007 (w252) → +0.0396 (w1008), falling back to +0.0026 at w2016 where the live leg is short. The two standing candidates at 10 bps:

| book | leg | from | days | CAGR | Sharpe | MaxDD | halves | ungated control | 4b |
|---|---|---|---|---|---|---|---|---|---|
| U56 K8 q0.17 w1008 d1.00 | RAW | 2009-01-13 | 4,443 | 14.15% | 1.2223 | −14.79% | 1.141/1.303 | 13.82% / 1.0462 / −20.88% | PASS |
| U56 K8 | **LIVE** | 2011-12-30 | 3,695 | **14.82%** | **1.3562** | **−12.72%** | 1.317/1.399 | 14.42% / 1.1066 / −20.88% | PASS |
| U56 K8 | OOS | 2017-01-03 | 2,436 | 16.03% | 1.3932 | −12.72% | 1.559/1.224 | 15.04% / 1.1065 / −20.88% | PASS |
| B136 q0.12 w1008 d0.50 | RAW | 2009-01-13 | 4,443 | 14.30% | 1.1121 | −17.31% | 1.186/1.036 | 14.20% / 1.0211 / −23.09% | PASS |
| B136 | **LIVE** | 2011-12-30 | 3,695 | **14.52%** | **1.2043** | −17.31% | 1.303/1.118 | 14.40% / 1.0724 / −23.09% | PASS |
| B136 | OOS | 2017-01-03 | 2,436 | 14.30% | 1.1572 | −17.31% | 1.300/1.002 | 13.96% / 1.0094 / −23.09% | PASS |

SPY on the LIVE leg is 15.04% / 0.9307 / −33.72% (halves 1.1167/0.8419), so K8's LIVE 4b legs clear by 1.3168 > 1.1167, 1.3992 > 0.8419, −12.72% inside −20.23%, 14.82% ≥ 10.53%. **H_CANDLIVE PASS at 0, 10 and 25 bps on both books.** The gated arm beats its own ungated equal-weight control on the same leg by +0.25 (K8) and +0.13 (B136) Sharpe with 8 pp and 6 pp less drawdown, so the edge is the gate's, not the warm-up's — the record's RAW convention was *understating* it by averaging in days on which the gate does not exist.

## (d) The chooser: liveness does not move it, the LIVE-LEG reading does
Rule 8 on the books, (q, w, depth) on 2009–2016 IS Sharpe alone, 2017–2026 read once, three pre-declared choosers. **H_PICKMOVE FAILS** — BLIND and LIVE50 pick identically on all three panels (U56 and B136 q0.12/0.17 w504 d0.50, SMALL q0.07 w504 d1.00), which is good news about 843's warm-up-blind concern at a 50% bar. But **LIVELEG** (same candidate set, IS Sharpe read on each arm's *own* live segment — no OOS information) moves the pick on **3 of 3** panels and on U56 moves it from a 4b **FAIL (DDCAP, OOS 14.69% / 1.1942 / −20.88%)** to a 4b **PASS** — it picks K8 itself, OOS 16.03% / 1.3932 / −12.72%. B136 moves from OOS 12.95%/1.1157 to 14.39%/1.2181, SMALL from 6.75%/0.4974 to 5.17%/0.3960 (worse, and 4b-failing either way). One selector convention that helps on 2 of 3 panels and hurts on the third is **PARK, not KEEP**: it is a candidate protocol convention, not a book.

## (e) By-product the run had to name
The B136 QROLL memo's RULES wording says "SPY excluded from holdings", but its published numbers reproduce **only with SPY in the panel** (14.3007% / 1.1121 / −17.3144%); excluding SPY gives 14.32% / 1.1140. The wording and the number disagree; the number is the one the record carries.

## Proposed PROTOCOL line (PROPOSAL ONLY — rule 6, Sunday review; PROTOCOL.md not edited)
> **10. Live share (rolling windows):** any verdict that turns on a rolling-window LENGTH must print, beside it, the LIVE SHARE of each leg it is read on — the fraction of scored days on which that window's statistic actually exists. A rolling statistic with `min_periods = w` is NaN for its first w−1 days and every gate built on it is inert there, so the arm IS its own ungated control on those days. A leg with live share below 0.90 may not carry a window-length verdict on its own; report the LIVE-leg reading beside the RAW one.

## Survivorship and limits
All three panels are **current-constituent** lists, so every CAGR and drawdown LEVEL above is optimistic, SMALL worst (52 tickers with `max_1d_move ≥ 1.0` dropped from `data/small_meta.csv`; 663 names left, sub-$2B screen read today). The RAW↔LIVE *difference* is a within-book contrast on one panel and survives survivorship far better than any level. Nothing here is a capital claim on its own, nothing was promoted, and the 4b shelf is unchanged in membership — only in what its two w1008 members are worth.
