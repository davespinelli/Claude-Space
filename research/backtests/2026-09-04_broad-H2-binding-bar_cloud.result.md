# Idea 63 — broad-H2-binding-bar (cloud lane, 2026-09-04)

**Verdict: the concentration hypothesis is REJECTED — the broad-universe H2 shortfall is
not a mega-cap/equal-weight effect and is not one year — plus one 4b KEEP-candidate that
falls out of the diagnosis: a 25% passive core sleeve.** The books do not fail H2 because
they cannot hold mega caps; they fail it because they are 75%-invested in a half where SPY
compounded at 15.0%/yr. Restoring the missing beta fixes the bar, and a control shows the
fix is **not** QQQ-specific.

Script: `research/backtests/2026-09-04_broad-H2-binding-bar_cloud.py`
Console: `2026-09-04_broad-H2-binding-bar_cloud.console.txt`
Memo: `2026-09-04_broad-H2-binding-bar_cloud.memo.md`

## Setup

H2 is the protocol's own split: **2017-11-03 → 2026-09-03** (H1 2009-01-13 → 2017-11-02).
SPY H1 0.957 / H2 0.837 — those are the 4b bars. Books: `v1`, `top20` (idea 2's KEEP),
`ew-all`, `ew-band3` (idea 57's KEEP-candidate), weekly, t+1, 10 bps, both universes.
Harness reproduces the published broad rows exactly (top20 13.1%/0.958/-20.1%, ew-all
10.7%/1.027/-17.7%, ew-band3 11.1%/1.064/-16.8%).

## Correction to the queue's premise

On the broad list at 10 bps the equal-weight books **already clear** the H2 bar: `ew-all`
0.917 and `ew-band3` 0.971 vs 0.837. Only the ranked, concentrated `top20` fails it
(0.814, -0.023) — and `v1` (0.537). Idea 4's "H2 or MaxDD binds for 9 of 10 arms" mixes two
different failures: **H2 binds for the ranked book; MaxDD/CAGR bind for the equal-weight
books.** So the question "can an equal-weight book hold this half?" was already answered
yes; the question is why the *concentrated* book cannot.

## Finding 1 — it is not the concentration factor (hypothesis rejected)

RSP (equal-weight S&P 500) is in both universes, so `RSP - SPY` is a tradable concentration
factor: negative when mega-caps lead. Regressing each book's daily excess over SPY on it:

| book | half | alpha/yr | beta | t(beta) | R² |
|---|---|---|---|---|---|
| top20 | H1 | -1.9% | **-1.20** | -24.1 | 0.207 |
| top20 | **H2** | -4.5% | **-0.20** | -5.0 | **0.011** |
| ew-all | H1 | -2.2% | -0.97 | -24.6 | 0.214 |
| ew-all | **H2** | -5.3% | +0.22 | +6.3 | **0.018** |
| ew-band3 | H2 | -4.8% | +0.20 | +5.8 | 0.015 |
| QQQ (reference) | H2 | +2.6% | -0.92 | -46.6 | 0.495 |

(broad list; universe.json is the same story with betas +0.04.) In **H1** these books load
*negatively* on equal-weight — they behaved like a mega-cap tilt, not an equal-weight one.
In **H2** the loading collapses to ~0 and explains **1-2% of the variance**; the entire
shortfall sits in alpha. A momentum book already holds the mega-caps. "An equal-weight book
structurally cannot hold the 2023-24 leadership" is not what the data says.

## Finding 2 — it is not one year, it is every strong up-year

H2 excess vs SPY (annualised daily mean, t) on the broad list, `ew-band3`: 2017 stub -10.0
(t -1.53), 2018 **+3.6**, 2019 **-11.6 (t -2.22)**, 2020 -9.2, 2021 -6.7, 2022 **+9.1**,
2023 -9.9 (t -2.04), 2024 -9.5, 2025 -8.2, 2026 -5.1. The two years the book *wins* are the
two down years. The worst drag (2019) had `RSP-SPY` at only -2.3pp, while 2024's -12.1pp of
concentration produced a smaller drag than 2019 did — the timing does not line up with
concentration at all.

Leave-one-year-out on broad `top20` (H2 0.814 vs bar 0.837): dropping **2019**, **2021** or
**2023** — any one of the three, individually — flips it to a pass. No single year owns the
failure. H2 CAGR: books 9.7-11.5%, SPY 15.0%. A 75%-gross book with a cash sleeve lags a
15%/yr benchmark in every year the benchmark runs; that is the whole mechanism.

## Finding 3 — the remedy, and the control that keeps it honest

Replace a fraction *b* of the book with a passive core at **matched 75% gross** (so
drawdown stays comparable), b ∈ {0, 0.25, 0.50}, all points at 5/10/25/50 bps on both lists.
At b = 0.25 with QQQ, at 10 bps:

| arm | universe.json | broad | cross-universe 4b |
|---|---|---|---|
| top20 b=0 | 12.7%/1.093/-18.3% | 13.1%/0.958/-20.1% (H2 0.814) | no |
| **top20 b=0.25** | 13.5%/1.120/-18.5% | 13.8%/1.016/-19.9% (H2 **0.880**) | **YES** |
| ew-all b=0.25 | 11.8%/1.083/-17.3% | 12.0%/1.061/-18.8% | **YES** |
| ew-band3 b=0 (idea 57) | 11.3%/1.136/-15.1% | 11.1%/1.064/-16.8% | YES |
| **ew-band3 b=0.25** | 12.4%/1.142/-16.2% | 12.3%/1.086/-18.5% | **YES, and at 25 bps too** |

Cross-universe 4b passes go from **1 of 4 books at b=0 to 3 of 4 at b=0.25**; b=0.50 breaks
the drawdown cap everywhere on broad.

**The control that matters:** QQQ is the best-performing liquid US index *of this exact
sample*, so a QQQ sleeve is a hindsight tilt 4b cannot detect. Re-running b=0.25 with a
**SPY** or **VTI** core instead: broad `top20` H2 goes 0.814 → **0.861 (SPY)** / 0.853
(VTI), and `ew-band3` → 0.960 / 0.949 — the H2 bar is fixed by *plain beta*, not by mega
caps. The QQQ version's only real advantage appears at 25 bps, where it still passes on
broad and the SPY/VTI versions fail on CAGR — i.e. the extra is the hindsight premium,
exactly where you would expect it.

## Rule 8

Both selection rules, on both universes, pick `top20 / b=0.50` on 2009-2016. OOS
(2017-2026): **universe.json 15.4%/1.106/-18.8% clears** every OOS 4b bar; **broad
14.4%/0.991/-22.0% FAILS** on drawdown (cap -20.2%). Neither walk-forward picks the b=0.25
arm this run recommends — it is the *sample-wide* 4b test that selects b=0.25, and the IS
rule over-reaches to b=0.50. That is the candidate's main weakness and is stated as such in
the memo.

## Honest limits

- **Survivorship, and it cuts the wrong way here:** both lists are current constituents, so
  the mega-caps the books are accused of missing are in the list *because* they won. Any
  concentration effect is therefore an upper bound — and it still came out at R² 0.01.
- The core sleeve is a return-and-beta fix, not an edge: it moves the book toward the
  benchmark it is being measured against. It should be judged on whether 75% gross was ever
  the right exposure, not on the Sharpe it buys.
- b=0.25 was chosen by the sample-wide cross-universe 4b test, not by the walk-forward,
  which prefers b=0.50 (and fails OOS on broad). One tuned parameter, three points, all
  reported.
- 2026 is a partial year (through 2026-09-03).
