# Idea 257 — window-stamp every reach and every depth denominator  (cloud, 2026-09-09)

**Verdict: ANSWERED / SPLIT — the fix WORKS in aggregate and FAILS exactly where a drawdown
instrument is bought.** Re-quoting reach per crisis episode at matched SPY depth (idea 117's
denominator) turns idea 251's **47-of-48 "OOS reach beats IS reach"** into **21 of 48
(sign-test p = 0.47)** and cuts median |log10(IS/OOS)| from **0.366 to 0.117**, clearing idea
117's 0.227 bar. But the DEEP bin — episodes ≥ 20 pp, the only ones a drawdown instrument
exists for — **does not improve at all** (median |log10| stays 0.366), for a structural reason:
at every theta the sample contains **one** in-sample deep episode against **two** out-of-sample
ones, so "matched depth" is not available there, it is merely asserted. And as a **selector**
the episode statistic is a wash (14 better / 14 worse / 20 ties over 48 cells), reproducing
idea 117's own P4. **Report-only, do not adopt as a chooser. No RULES change, no KEEP, no
memo; RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py untouched.**

## 0. Harness

The object under test is idea 251's 48 cells exactly: 2 panels (u56, broad) × 2
instrument-free base books (EWALL0, CAND20) × 2 cost rungs × 6 instrument families on idea
251's EXTENDED ladder — **504 arms + 8 controls = 512 backtests, all reported**, plus 14,616
arm-episode rows. Idea 245's module (books, simulator, instruments) and idea 117's episode
classifier are IMPORTED, not re-implemented. Panels truncated to idea 251's last bar
(2026-09-04). The small panel is deliberately out of scope: the 47/48 claim is about these
cells.

| gate | result |
|---|---|
| G1 `run(no instrument)` vs `engine.backtest` | max\|dret\| **0.000e+00**, max\|dturn\| **0.000e+00** |
| G1 `run(stop=S)` vs idea 94's `run_stop` | **0.000e+00** over 4 depths |
| G2 vs idea 251's **committed** grid.csv | bought_pp max 8.8e-3 (q99 5.0e-5), paid_pp 1.3e-2 (q99 1.1e-2), IS_bought 7.4e-2 (q99 1.1e-4), CAGR 1.5e-4, MaxDD 8.8e-5; **304/512 rows agree to 1e-6** |
| G3 vs idea 251's **committed** reach.csv | max_bought 1.3e-5, IS_max_bought 3.7e-5, OOS_max_bought 1.3e-5 |
| G3 headline recount | **OOS reach > IS reach in 47 of 48 cells** (published: 47 of 48), p = 3.5e-13 |

G2/G3 are **tolerance** gates, not bit-for-bit ones, and the reason is in the data: on the
4,699 × 58 cells the two `data/prices.csv` versions share, adjusted closes have been restated
by up to **3e-4** (DIA, COST, LLY, META, UNH). The two largest arm disagreements (0.074 and
0.068 pp of IS reach) are the 200d gate at a 20-day MA, the shortest lookback on the extended
ladder; the largest full-sample one (0.0088 pp) is the path-dependent stop. All of it is 2–3
orders of magnitude below the gaps under test, and idea 251's headline recounts unchanged.

## 1. The episodes (idea 62/117's classifier, θ = 0.10)

| eid | peak | trough | depth | days p→t | speed | bin | window |
|---|---|---|---|---|---|---|---|
| E1 | 2009-01-28 | 2009-03-09 | 22.06 | 27 | FAST | **DEEP** | IS |
| E2 | 2010-04-23 | 2010-07-02 | 15.70 | 49 | FAST | SHALLOW | IS |
| E3 | 2011-04-29 | 2011-10-03 | 18.61 | 108 | SLOW | SHALLOW | IS |
| E4 | 2015-07-20 | 2016-02-11 | 13.02 | 143 | SLOW | SHALLOW | IS |
| E5 | 2018-01-26 | 2018-02-08 | 10.10 | 9 | FAST | SHALLOW | OOS |
| E6 | 2018-09-20 | 2018-12-24 | 19.35 | 65 | SLOW | SHALLOW | OOS |
| E7 | 2020-02-19 | 2020-03-23 | 33.72 | 23 | FAST | **DEEP** | OOS |
| E8 | 2022-01-03 | 2022-10-12 | 24.50 | 195 | SLOW | **DEEP** | OOS |
| E9 | 2025-02-19 | 2025-04-08 | 18.76 | 34 | FAST | SHALLOW | OOS |

θ = 0.08 gives 13 episodes (5 IS / 8 OOS), θ = 0.15 gives 7 (3 / 4). **The DEEP bin is 1 IS
episode against 2 OOS at every theta** — and the one IS deep episode is E1, the 27-day GFC
fragment the 2009-01-13 slice merely clips, which idea 117 already flagged.

## 2. The test (both bars pre-registered from idea 117)

θ = 0.10, the pre-registered point:

| statistic | bin | OOS>IS, whole-window | → episode-stamped | med \|log10(IS/OOS)\| | B1 | B2 |
|---|---|---|---|---|---|---|
| reach | ALL | 47/48 (p 3.5e-13) | **21/48 (p 0.471)** | **0.366 → 0.117** | PASS | PASS |
| reach | SHALLOW | 47/48 | 27/48 (p 0.471) | 0.366 → **0.101** | PASS | PASS |
| reach | **DEEP** | 47/48 | 18/48 (p 0.111) | **0.366 → 0.366** | PASS | **FAIL** |
| price | ALL | 6/41 (p 4.9e-06) | 21/48 (p 0.471) | 0.247 → **0.226** | PASS | PASS |
| price | SHALLOW | 6/41 | 27/47 (p 0.382) | 0.247 → 0.200 | PASS | PASS |
| price | **DEEP** | 6/41 | 11/48 (p **0.0002**) | 0.247 → 0.204 | **FAIL** | PASS |

B1 = the one-sided asymmetry must become insignificant at 5%; B2 = median |log10(IS/OOS)|
must fall and clear idea 117's published 0.227. Note the whole-window PRICE asymmetry runs
the OTHER way (35 of 41 cells price CHEAPER out of sample), which is the same depth effect
seen from the denominator's side.

**Robust across theta, and so is the failure.** Reach-ALL clears both bars at every theta
(med 0.181 / 0.117 / 0.195 at 0.08 / 0.10 / 0.15; sign p 0.19 / 0.47 / 0.89). Reach-DEEP
fails B2 at **all three** with an identical 0.366 — because the DEEP composition does not
change with theta. Price-DEEP fails B1 at all three (p 0.0000 / 0.0002 / 0.0002).

## 3. Per family (θ = 0.10, mean over the 8 cells)

| family | whole-window reach IS → OOS (pp) | OOS>IS | episode-normalised IS → OOS | OOS>IS |
|---|---|---|---|---|
| 200d MA gate | 1.26 → 3.94 | 8/8 | 0.0702 → 0.0697 | 3/8 |
| MA re-entry band | 1.79 → 3.19 | 8/8 | 0.0624 → 0.0122 | 0/8 |
| absolute momentum | 2.04 → 3.51 | 7/8 | 0.2802 → 0.0743 | 0/8 |
| de-gross (reference) | 13.16 → 23.90 | 8/8 | 0.6795 → 0.7116 | 5/8 |
| book DD control (idea 40) | 4.05 → 9.89 | 8/8 | 0.2446 → 0.2753 | 6/8 |
| **per-name trailing stop** | **0.80 → 5.14** | 8/8 | 0.0822 → 0.1530 | **7/8** |

The gates and the band are fully explained by depth — normalised, three of them reverse. The
**stop is the family the fix helps least** (still 7/8), consistent with idea 117's P3 finding
that the stop's protection is the one that does not respond to crisis depth (t +1.46).

## 4. Rule 8 — two selectors on IS only, 2017–2026 read once

| selector | mean OOS reach at pick | forfeit vs OOS-optimal (mean / median) | picks OOS-optimal | OOS Sharpe | 4a | 4b |
|---|---|---|---|---|---|---|
| S_WINDOW (idea 251's) | 7.163 pp | 1.099 / 0.335 pp | 20/48 | **0.9996** | 8/48 | **9/48** |
| S_EPISODE (candidate) | **7.271 pp** | **0.990 / 0.217 pp** | **23/48** | 0.9764 | 8/48 | 6/48 |

Head-to-head the candidate forfeits less OOS reach in **14 of 48 cells, more in 14, ties in
20** — a wash, and it buys the marginally better reach with marginally worse OOS Sharpe. This
is idea 117's P4 result reproduced on a different statistic: **the depth denominator is a
reporting convention, not a chooser.**

## 5. Both KEEP paths
Across the whole 504-arm grid: **4a 18/504, 4b 57/504, 4a ∧ 4b 0/504.** Of the 96 rule-8
picks, **15 clear 4b** — all on u56/broad EWALL0 (plus one CAND20 stop), best being the u56
EWALL0 2% re-entry band at 10 bps: full sample 12.09% / 1.1431 / −17.71%, OOS 13.05% /
1.1722 / −17.71% against SPY OOS 0.8820. **Every one of them has a LOWER OOS Sharpe than the
live RULES v2 book** (1.2851 on u56 at 10 bps, 1.1185 on broad) and every one fails 4a on the
drawdown bar. The full-sample best arm in the grid (u56 EWALL0 band 12%, 14.09% / 1.2330 /
−19.36%, OOS 15.22% / 1.2723) is **not** what the pre-registered selector picked, so quoting
it as a candidate would be selecting on the full sample. **No memo: nothing here is a
capital-worthy object the record does not already hold.**

## Caveats
SURVIVORSHIP (idea 54): `broad` is a current-constituent list, so its crashes are shallower
than the real world's; reach is an ABSOLUTE quantity so the bias is not cancelled and every
reach here understates the instrument. The episode-normalised statistic divides by SPY's
depth, which is survivorship-free — an argument for the convention that is independent of
whether it closes the gap. The DEEP-bin result rests on **one** in-sample episode and is a
statement about the sample, not about the instruments. Idea 38: calendar-day index. Idea 126:
t+1 execution only.

Files: `.arms.csv` (512), `.episodes.csv`, `.epreach.csv.gz` (14,616), `.gap.csv`,
`.walkforward.csv`, `.console.txt`.
