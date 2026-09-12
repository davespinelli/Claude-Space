# Idea 835 — does any DE-GROSSING FAMILY beat its TWIN on a leg that contains NO 2020 DRAWDOWN?
**cloud lane, 2026-09-12, idea 1 of 2. VERDICT: ANSWERED = YES, but barely, and KILL for capital.**

Script `2026-09-12_does-any-DE-GROSSING-FAMILY-beat-its-TWIN-with-NO-2020-DRAWDOWN_cloud.py`,
runtime 70 s. 2 tuned params (excluded episode × leg set), 7 × 3 = **21 points, all reported**
in `.grid.csv` (8,568 rows). No RULES/PROTOCOL/scan/bot/baseline change.

## Gates — 6 of 6 PASS
G1 `fast_run` == `engine.backtest` **1.041e-17**. G2 fast metrics == `engine.metrics` **0.000e+00**.
G3 0.01-grid twin interpolation vs an exact run **2.010e-08**. G4 idea 825's **committed**
1,944-row corpus rebuilt: max|dSharpe| **0.000e+00**, max|d twin Sharpe| **0.000e+00**, **0**
win-flag mismatches. G5 deletion arithmetic exact: empty deletion bit-identical (0.000e+00), arm
stack and twin stack vs a direct numpy masked Sharpe **0.000e+00** and **0.000e+00**. G6 a
deletion that misses a leg moves it by **exactly 0** on all 3,672 such cells.

## The answer (ENDYEAR legs, COVID_TIGHT 2020-02-19..2020-04-07, 10 bps, FULLMATCH, POOLED; mean over the 6 legs that contain the episode)
| family | with 2020 | without | delta |
|---|---|---|---|
| ABS | 0.5880 | 0.3704 | −0.2176 |
| QEXP | 0.6590 | 0.3920 | −0.2670 |
| QROLL | **0.9460** | **0.5818** | **−0.3642** |
| adv = QROLL − max(ABS,QEXP) | +0.2870 | **+0.1682** | −0.1188 |

**YES, narrowly:** QROLL still beats its matched-gross twin on 58.18% of arms and still leads the
other two families by +0.1682 with the crash deleted. **But 35 of 4,443 days (0.79%) carry 36.4
points of the win rate**, and the survival is not robust: it fails at **25 bps** (0.4850), on
**SMALL663** (0.9329 → 0.1968), and on the one leg that isolates the era — the disjoint block
**2019–2021, where QROLL goes 0.9167 → 0.0324**. It holds on U56 (0.9734 → 0.9259), B136
(0.9317 → 0.6227), 0 bps (0.6400), POSTYEAR (0.6769) and WINMATCH.

**The placebos settle what is being measured.** Deleting a same-length non-crash block moves
QROLL by **+0.0026** (PLACEBO_2017) and **−0.0046** (the 34 days immediately before the crash).
Deleting **DD_2015** moves it **−0.1197** and COVID_WIDE/COVID_DD **−0.2608 / −0.2392**. So the
clause is paid in *drawdowns*, not in day count and not only in COVID — but 2020 is 3× the 2015
episode.

## Capital leg — PROTOCOL 4, both paths, 648 arms at 10 bps
**4a: 0 → 0** (no arm ever beats RULES v2 in both halves at no worse MaxDD). **4b: 141 → 16.**
Of the 125 passes lost, **110 fail on the DD cap alone**, 12 on the CAGR floor: they cleared 4b's
"MaxDD ≤ 60% of SPY's" only because SPY's own MaxDD was −33.72% (the 2020 crash). Delete it and
SPY reads −24.50%, the cap tightens to −14.70%, and the de-grossed books no longer fit. 16
survivors, all U56/B136 (**0 on SMALL663**), 15 of 16 QROLL, e.g. `U56 QROLL L0.12 w252 d1.00 D
g1.00`: 13.16% / 1.2045 / −14.00% full, 14.02% / 1.2802 / −14.00% ex-2020.

## Rule 8 — dial chosen on ≤2016-12-31, OOS 2017-01-01.. read ONCE
Best IS pick `B136 QROLL L0.17 w504 d0.5 W g1.00` (IS Sharpe 1.0962), **unchanged** when 2020 is
deleted from the IS window (0 of 108 picks move):

| | OOS CAGR | OOS Sharpe | OOS MaxDD |
|---|---|---|---|
| pick | 12.86% | 1.107 | −17.20% |
| RULES v2 | 7.88% | 1.106 | −12.24% |
| SPY | 15.33% | 0.877 | −33.72% |
| pick ex-2020 | 15.16% | 1.321 | −15.47% |
| RULES v2 ex-2020 | 9.18% | 1.342 | −9.28% |
| SPY ex-2020 | 18.44% | 1.147 | −24.50% |

72 of 108 rule-8 picks beat SPY's OOS Sharpe with 2020 and **the same 72 without it** — the
Sharpe leg is not a 2020 artefact. The **4b** leg is: 18 of 108 picks pass with it, **4** without.

## Hypotheses — 7 of 11 PASS
H_MAIN PASS · H_ADV PASS · H_DROP PASS · H_PLACEBO PASS · **H_CLEAN FAIL** (825's clean-leg legs
run 0.4167–0.7361, not ≤0.60: `..2013` 0.6991 and `..2018` 0.7361 exceed it) · **H_COSTINV FAIL**
(25 bps) · H_MATCH PASS · **H_PANEL FAIL** (SMALL663) · **H_LEGSET FAIL** (BLOCK3) · H_4B PASS ·
H_R8 PASS.

## Verdict
**KILL for capital, ANSWERED for the record.** The queue's rationale — "a de-grossing clause that
only pays in one crash is a bet on the next crash" — is *substantially* right and *strictly* wrong:
the clause pays in every drawdown it sees (2015 as well as 2020), not only in one, but 0.79% of
the sample carries 36 points of its win rate and **89% of its 4b passes**, and the passes it
loses fail on a drawdown cap that only looked generous because SPY itself crashed. Nothing here
is capital-worthy: 4a is 0 at every rung, and a 4b pass that evaporates when one seven-week
episode is removed is an exposure bet on crash timing, not an edge.

**SURVIVORSHIP:** all three panels are current-constituent lists (SMALL663 = 663 sub-$2B names
after dropping 52 with max_1d_move ≥ 1.0 per `data/small_meta.csv`); every level is optimistic,
SMALL663 worst. Win rates are within-panel agreement rates and move far less than levels, but no
CAGR or MaxDD here is a capital claim — and under a deletion, CAGR/MaxDD are read on the chained
equity of the kept days, a counterfactual path, not a tradable one.
