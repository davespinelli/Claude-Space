# Idea 4 — abs-momentum-filter (lane C, 2026-09-04)

**Verdict: KILL** for absolute (12-1) momentum as a replacement for, or an addition to, the
200d-MA eligibility gate. Two of the four idea-4 arms nominally pass 4b on both large-cap
universes, but they pass by **+0.0002 Sharpe** and **+0.12pp of drawdown** — ties, not
margins — and **neither pre-registered walk-forward rule picks an idea-4 arm on either
universe**. They are documented below and explicitly recommended against.

Script: `research/backtests/2026-09-04_abs-momentum-filter_C.py`
Console: `research/backtests/2026-09-04_abs-momentum-filter_C.console.txt`
Grid: 2 books x 5 gates x 4 cost levels x 2 universes = 80 points, **all reported**.
1 tuned dimension (the gate instrument). n=20, 75% gross, `vol20<0.60`, weekly rebalance
and the no-vol-scaler composite are all pre-chosen from ideas 2/55/57 and not swept here.

## Harness checks (all exact)
| check | this run | published |
|---|---|---|
| analytic cost model vs `engine.backtest(cost_bps=10)` | max abs daily diff **0.00e+00** | identity |
| idea 2 KEEP row (top20, 200d, universe.json) | 12.7%/1.093/-18.3% | 12.7%/1.093/-18.3% |
| idea 57 KEEP-candidate (ew-all, band3) | 11.3%/1.136/-15.1% | 11.3%/1.136/-15.1% |

## The mechanism prediction was confirmed; the payoff was not
Idea 57 priced the 200d gate as insurance that never pays because it flips 7.55x/ticker/yr.
12-1 momentum **is** the slower signal, exactly as predicted:

| gate | flips/tkr/yr (uni / broad) | ew-all turnover (uni / broad) | mean names passing (uni) |
|---|---|---|---|
| none | 0.00 / 0.00 | 1.9x / 1.8x | 56.0 |
| band3 (idea 57) | **1.77 / 2.03** | 4.9x / 5.2x | 38.4 |
| **abs 12-1** | **5.75 / 5.98** | 6.4x / 6.4x | 39.4 |
| 200d (incumbent) | 7.55 / 7.73 | 8.2x / 8.3x | 38.5 |
| **200d AND abs** | **8.06 / 8.34** | 9.7x / 9.6x | 33.0 |

Slower did not translate into a decisive win. Paired daily differences at 10 bps, **abs
minus the 200d incumbent**:

| book | universe.json | universe_broad.json |
|---|---|---|
| ew-all (gate-only) | +0.94pp CAGR, +0.021 Sharpe, **t +0.92** | +1.05pp CAGR, +0.040 Sharpe, **t +1.19** |
| top20 (ranked) | -0.30pp CAGR, -0.035 Sharpe, t -0.30 | -0.30pp CAGR, -0.014 Sharpe, t -0.44 |

Same sign on both lists in each book, opposite signs *between* books, and nothing beyond
t +1.2. Against the **ungated** control the abs gate is negative on Sharpe in 3 of 4 cells
(-0.065, -0.055, -0.054; only broad/top20 is +0.015) — it is the same insurance contract as
the 200d gate, slightly cheaper, still not paying.

**The AND arm is the clear loser.** Requiring both signals makes the gate stricter *and*
faster (8.06 flips, 9.7x turnover, 33 names): vs the incumbent it is -1.36pp CAGR / -0.067
Sharpe on universe.json top20 (**t -1.99**, the only near-significant paired result in the
run) and -0.41pp / -0.053 on ew-all; vs the ungated control -2.41pp / -0.096 (t -2.50) and
-2.22pp / -0.130 (t -1.54). Idea 4's "also try both" is answered: no.

## Whipsaw ordering holds only where the gate is the only thing happening
Sharpe at 10 bps, gates ordered by flip rate (fewest first):

| book / universe | band3 | abs | 200d | both | monotone? |
|---|---|---|---|---|---|
| ew-all / universe.json | **1.136** | 1.072 | 1.050 | 0.997 | **yes** |
| ew-all / broad | 1.064 | **1.068** | 1.027 | 0.988 | near (top two within 0.004) |
| top20 / universe.json | **1.118** | 1.058 | 1.093 | 1.026 | no |
| top20 / broad | 0.952 | 0.944 | 0.958 | **0.963** | no (inverted) |

Idea 57's whipsaw mechanism survives in the gate-only book on both lists and is drowned by
the momentum ranking in the top20 book. Useful refinement: gate choice is a real decision
for `ew-all`, and noise for a ranked book.

## The two nominal cross-universe 4b passes are ties
4b margins on the binding bar, 10 bps:

| arm | universe.json binding | broad binding | honest read |
|---|---|---|---|
| top20 + 200d AND abs | H1 +0.050 | **H2 +0.0002** | a tie at the 4th decimal |
| ew-all + abs | H1 +0.160 | **DD +0.12pp** (-20.05% vs -20.20% cap) | 0.12pp of drawdown slack |
| ew-all + band3 (idea 57 ref) | H1 +0.156 | H2 +0.134 | the only arm with real margin |

Neither survives cost: at 25 bps `ew-all/abs` fails on both lists (CAGR on universe.json,
DD on broad) and `top20/both` fails on both (H1/CAGR, H2/OOS/CAGR).

## Rule 8 walk-forward (gate and book chosen on 2009-2016, 2017-2026 untouched, 10 bps)
| universe | Rule A (max IS Sharpe) | Rule B (4b-aware IS filter) |
|---|---|---|
| universe.json | top20/**none** — OOS 14.9%/1.164/-18.5%, clears | top20/**none** — same, clears |
| universe_broad | ew-all/**none** — OOS 12.5%/1.104/-20.8%, **fails OOS DD** | ew-all/**band3** — OOS 11.2%/1.074/-16.8%, clears |

OOS references: RULES v1 baseline 7.8%/0.751/-13.8% (universe.json), 6.0%/0.581/-21.2%
(broad); SPY 15.5%/0.884/-33.7%. **No idea-4 arm is selected by any rule on any universe** —
four independent selections, four rejections. Idea-4 arms' own OOS numbers are worse than
the arm each rule did pick: universe.json ew-all/abs 12.2%/1.113/-17.1% vs band3's
12.6%/1.234/-15.1%; broad ew-all/abs 12.1%/1.083/-20.1% vs band3's 11.2%/1.074/-16.8%
(abs wins CAGR and Sharpe there but gives back 3.3pp of drawdown).

## Full-sample, 10 bps, for the record
universe.json (SPY 15.3%/0.890/-33.7%, halves 0.957/0.837, OOS 0.884; RULES v1 6.5%/0.666/-13.8%):
ew-all abs **11.4%/1.072/-17.1%** (halves 1.116/1.038, OOS 1.113) vs 200d 10.4%/1.050/-15.9%
vs none 12.2%/1.127/-18.4% vs band3 11.3%/1.136/-15.1%.
broad (RULES v1 6.4%/0.640/-21.2%): ew-all abs **11.8%/1.068/-20.1%** (halves 1.158/0.988,
OOS 1.083) vs 200d 10.7%/1.027/-17.7% vs none 12.9%/1.121/-20.8% vs band3 11.1%/1.064/-16.8%.
2022 is where abs earns its keep in the ranked book (top20: abs -6.7% vs 200d -9.0% on
universe.json, -9.0% vs -10.9% on broad) and 2020 is where it gives it back (14.1% vs 15.4%;
8.6% vs 12.2%).

Leaderboard note: broad-universe rows carry the broad-universe RULES v1 baseline
(0.640, halves 0.762/0.537) in the baseline column, since that is the run their 4a verdict
was read against — not the universe.json 0.67 used by earlier rows.

**SURVIVORSHIP:** both lists are current constituents, so absolute CAGR/Sharpe are
optimistic in one direction. The gate-vs-gate comparisons that carry the KILL are far less
exposed — every arm draws from the same names on the same days.
