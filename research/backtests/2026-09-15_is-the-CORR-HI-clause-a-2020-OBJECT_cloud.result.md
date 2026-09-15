# Idea 864 (cloud lane, 2026-09-15) — is-the-CORR-HI-clause-a-2020-OBJECT

**ANSWERED: NO at the grid level (there is no non-crash evidence worth the name), YES at the
attribution level (2020 is the single biggest payer), and the clause's own memo cell survives the
crash-free corpus but cannot clear 4b there. VERDICT: KILL for capital.**
No book promoted. RULES.md, PROTOCOL.md, scan.py, bot.py, baseline.py untouched.

Script `research/backtests/2026-09-15_is-the-CORR-HI-clause-a-2020-OBJECT_cloud.py`;
console `..._cloud.console.txt`; data `..._cloud.{grid,corpora,comparands,walkforward,ladders,controls,years,hypotheses}.csv`.

## Gates (all printed before any verdict)
| gate | result |
|---|---|
| G1 runner identity (depth 0 == `engine.backtest`) | max\|d\| **0.000e+00** PASS |
| G2 causality (`min_periods=w`, t+1; no-threshold days rise with w) | 0/0/11/263/515/767/1271/1775 PASS |
| G3 reproduction of idea 814/863's FULL cell | **14.02% / 1.1538 / -15.11%** exactly — H_REPRO PASS |
| G4 determinism (grid recomputed, no RNG outside the seeded shuffle) | \|dSharpe\| **0.000e+00** PASS |
| G5 splice integrity | \|FULL\| 4443 = 4381+62 (tight) = 4190+253 (year); NOCRASH 3939 = 4443-504 PASS |
| G6 cross-run vs idea 863's committed `corpora.csv` | EX2020 WORKS **25 vs 863's 25** PASS; NOCRASH 17 vs 863's EXBOTH 12 — expected, 863's EXBOTH strips the TIGHT 2020 window, NOCRASH strips the calendar year |

## The answer — the deciding test FAILS
`WORKS(cell, corpus)` = gated Sharpe > its own matched-gross twin's AND \|gated MaxDD\| < twin's,
both legs, 40 cells (w × depth) at every corpus.

| corpus | days | WORKS/40 | Sharpe leg | DD leg | 4b | 4a | med dSharpe | med dMaxDD | med dCAGR |
|---|---|---|---|---|---|---|---|---|---|
| FULL | 4443 | 33 | 34 | 38 | 26 | 0 | +0.0488 | +3.38pp | +0.21pp |
| EX2020T (tight 2020 removed) | 4381 | **25** | 25 | 36 | 2 | 0 | +0.0055 | +2.63pp | -0.03pp |
| ONLY2020T (tight 2020 alone) | 62 | **15** | 36 | 15 | 1 | 1 | +0.1189 | -0.02pp | +3.99pp |
| EX2020Y (calendar 2020 removed) | 4190 | 28 | 28 | 35 | 2 | 0 | +0.0139 | +2.61pp | +0.05pp |
| ONLY2020Y (calendar 2020 alone) | 253 | **40** | 40 | 40 | 3 | 2 | +0.3344 | +5.00pp | +5.12pp |
| ONLY2022 | 251 | **26** | 26 | 30 | 14 | 0 | +0.0306 | +1.46pp | +0.42pp |
| **NOCRASH (both calendar episodes removed)** | 3939 | **17** | 18 | 30 | 2 | 0 | **-0.0031** | +0.64pp | -0.19pp |

- **H_NONCRASH FAIL** (17/40 < the pre-stated 20/40 bar), and the median dSharpe on that corpus is
  **negative (-0.0031)**. Below a coin flip. **No non-crash evidence for the clause exists at the
  grid level** — the queue's premise is confirmed.
- **H_2020 FAIL** (ONLY2020T 15/40 < 30/40), and the reason is instructive: inside the 62-day tight
  window the **Sharpe leg passes 36/40** but the **DD leg only 15/40** — in the fastest part of the
  crash the clause de-grosses *late enough* that its own drawdown is no better than a twin that
  simply held that much less all along. On the **calendar** year the clause is perfect
  (**ONLY2020Y 40/40**, median dSharpe +0.3344, median dCAGR +5.12pp). The 2020 payoff is a
  calendar-2020 fact, not a crash-window fact.
- H_EX2020 PASS (25/40), reproducing 863's EX2020 count exactly — 2020's *removal* alone does not
  break the clause; it is the removal of **both** episodes that does.
- The DD leg weakens as the crashes come out (38 → 36/35 → **30** on NOCRASH) and the Sharpe leg
  collapses with it (34 → **18**). Both legs are episode-carried.
- **4a is 0/40 on every non-episode corpus** (and 0/40 on FULL): against the live RULES v2 book the
  clause never clears the drawdown leg at gross 1.00, on any corpus of any length.

## The memo cell, corpus by corpus (w=252, depth=0.50, q=0.17)
| corpus | on% | gross | gated CAGR/Sharpe/MaxDD | twin CAGR/Sharpe/MaxDD | WORKS | 4b |
|---|---|---|---|---|---|---|
| FULL | 16.6% | 0.9172 | 14.02% / 1.1538 / -15.11% | 13.03% / 1.0211 / -21.33% | WORKS | PASS |
| EX2020T | 15.8% | 0.9211 | 14.73% / 1.2171 / -15.11% | 14.33% / 1.1456 / -20.06% | WORKS | FAIL(DD) |
| ONLY2020T | 72.6% | 0.6371 | -26.40% / -1.5268 / -13.83% | -35.76% / -1.9071 / -15.17% | WORKS | FAIL(H2,CAGR,OOS) |
| ONLY2022 | 51.4% | 0.7430 | -7.27% / -0.5507 / -14.85% | -8.32% / -0.6341 / -16.25% | WORKS | FAIL(H1,DD) |
| **NOCRASH** | 14.0% | 0.9298 | **15.32% / 1.2849 / -13.25%** | 15.19% / 1.2281 / -15.55% | **WORKS** | **FAIL(DD)** |

Inside the NOCRASH **OOS** window (1,932 days): **17.02% / 1.5242 / -12.71%** vs SPY
20.21% / 1.3929 / -19.35% → **4b FAIL(DD)**, because stripping the crashes shrinks the comparand's
own drawdown: SPY's MaxDD falls from -33.72% to -22.06% and the 60% bar tightens from -20.23% to
-13.24%, which the book's -13.25% misses by **one basis point**. H_CELL PASS, **H_4B_NC FAIL**.
That knife-edge is the honest headline: the clause's 4b pass is a statement about SPY's crash
drawdown, not about the book's.

## Rule 8 walk-forward — dials fitted on 2009–2016 alone (a window containing NEITHER episode)
Both pre-stated choosers pick the same interior cell **(w=252, depth=0.75)**; C2's eligible pool is
2/40. Each OOS window read once.

| OOS corpus | days | arm CAGR/Sharpe/MaxDD | twin (matched gross) | SPY | RULES v2 | WORKS | 4b | 4a |
|---|---|---|---|---|---|---|---|---|
| FULL | 2436 | **14.37% / 1.2792 / -12.12%** | 12.17% / 1.0100 / -20.33% | 15.33% / 0.8767 / -33.72% | 7.88% / 1.1059 / -12.24% | YES | PASS | PASS |
| EX2020T | 2374 | 15.11% / 1.3408 / -12.12% | 14.51% / 1.2492 / -19.26% | 16.95% / 1.0751 / -24.50% | 8.76% / 1.2830 / -9.28% | YES | PASS | FAIL |
| EX2020Y | 2183 | 13.60% / 1.2749 / -12.12% | 12.65% / 1.1377 / -19.11% | 15.00% / 0.9811 / -24.50% | 7.82% / 1.1876 / -9.28% | YES | PASS | FAIL |
| **NOCRASH** | 1932 | **16.32% / 1.5114 / -10.69%** | 16.61% / 1.4731 / -15.21% | 20.21% / 1.3929 / -19.35% | 9.90% / 1.4485 / -7.23% | YES | **PASS** | FAIL |

**H_WF PASS** — and this is the one place the clause looks alive: a chooser that never saw either
crash still lands on a cell that beats its matched-gross twin and clears 4b on the crash-free OOS
corpus, 8/8 across the four corpora and both choosers. It does **not** rescue the verdict, because
the grid it was picked from is 17/40 on that same corpus: the pick is a good draw from a pool with
no edge, not evidence of one.

## Controls
- **PLACEBO (+252 trading days, same firing rate and depth, wrong dates): WORKS NO on all four
  corpora** — FULL, ONLY2020T, ONLY2022 and NOCRASH. The clause's dates do carry information.
- **SHUFFLE null on NOCRASH** (20 draws, seed 864; ON-blocks permuted in time, count and length
  preserved): null dSharpe min -0.1527 / median -0.0528 / max +0.1332, WORKS on **2 of 20** draws.
  The real cell's +0.0567 sits at the **95th percentile** — real but one-tailed-marginal, and the
  null is not inert (2 draws clear both legs by chance).

## Where the value actually sits — exact attribution
Cumulative **log** excess of the memo cell over its own full-sample matched twin: **+0.1547
(+16.74% simple)**, partitioned exactly (residual zero by construction):

| partition | days | log excess | share |
|---|---|---|---|
| 2020 episode (calendar) | 253 | **+0.0756** | **48.9%** |
| 2022 episode (calendar) | 251 | +0.0339 | 21.9% |
| everything else | 3939 | +0.0452 | 29.2% |
| *2020 TIGHT window alone* | *62* | ***+0.0846*** | ***54.7%*** |

**54.7% of the clause's entire lifetime excess is earned in 62 trading days.** The tight window
earns more than the whole calendar year containing it, i.e. 2020-outside-Feb-Apr costs the clause
money. Two crashes = **70.8%** of the total on 504 of 4,443 days (11.3% of the sample).
Calendar table: the cell loses to its twin in **7 of 18 years**.

## Ladders (reported, never selected on)
NOCRASH WORKS **YES at 0 / 5 / 10 / 25 bps** and **NO at 50 bps**; **YES at lag 1 and 2, NO at
lag 3**. **H_LADDER FAIL.** The crash-free edge does not survive either a 50 bps rung or a
three-day execution delay.

## Hypothesis table
| H_REPRO | H_2020 | H_EX2020 | H_NONCRASH | H_CELL | H_4B_NC | H_WF | H_LADDER |
|---|---|---|---|---|---|---|---|
| PASS | FAIL | PASS | **FAIL** | PASS | FAIL | PASS | FAIL |

**VERDICT: KILL** (the pre-stated rule: KILL if H_NONCRASH fails). The CORR-HI clause is not a
2020 object in the sense of dying without 2020 — it survives either episode's removal singly — but
it is a **crash-shape bet**: it needs at least one of the two episodes, earns 70.8% of its lifetime
excess in 11.3% of its days, and on a crash-free corpus its grid-level evidence is 17/40, its 4b
pass dies on the drawdown leg by one basis point, and its edge dies at 50 bps or lag 3. Nothing
here justifies sizing it as a market-state clause.

**SURVIVORSHIP (PROTOCOL rule 9):** B136 is `universe_broad.json`'s CURRENT constituents. Every
CAGR and MaxDD LEVEL above is optimistic and the crash-free corpus is, if anything, generous to the
clause — the names that died are exactly the ones that would have co-moved hardest in 2020 and
2022. The arm-minus-twin DIFFERENCE is the durable part.
