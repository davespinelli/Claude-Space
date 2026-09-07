# Idea 373 — does the IS-SPREAD screen retire the record's rho-based chooser verdicts?

**cloud, 2026-09-07.** Script `2026-09-07_does-the-IS-SPREAD-screen-retire-the-record-s-rho-based-chooser-verdicts_cloud.py`.
Outputs `.corpus_stratified.csv` (6307 menus), `.corpus_filelevel.csv` (255), `.live.csv` (225 points),
`.rule8.csv` (54 menus), console `.console.txt`.

## Verdict: **the screen does NOT work as a screen — KILL as proposed. It IS a drawdown abstention rule.**

`S1 = IS_Sharpe(top1) - IS_Sharpe(top2)`, computed beside every chooser menu in the record's
committed evidence. 0 tuned parameters; the threshold is a reported ladder.

**Corpus:** every committed `research/backtests/*.csv` carrying the canonical triple
`IS_Sharpe`/`OOS_Sharpe`/`OOS_MaxDD` — **225 files, 6307 stratified menus, 168,713 arms** (a menu =
rows sharing every pre-registered stratifier present: panel, universe, book, form, cost, bps,
cost_bps, rung, freq, cadence, kind; SPY rows dropped). File-level menus (one per file, median 168
arms) reported alongside. **Live arm:** 6 dials x 3 panels x 3 rungs = 225 points / 54 menus, rebuilt
from source, IS <= 2016-12-31 chooses, 2017- read once.

### 1. The queue's count

| menu definition | median S1 | **S1 < 0.01** | S1 < 0.005 | S1 < 0.05 |
|---|---|---|---|---|
| stratified (6307) | 0.0221 | **2229 = 35.3%** | 1746 = 27.7% | 4615 = 73.2% |
| file-level (255) | 0.0071 | **140 = 54.9%** | 116 = 45.5% | 227 = 89.0% |
| live (54) | — | **15 = 27.8%** | 13 | 37 |

So a third of the record's chooser menus — over half at file level — are decided on an IS margin
under 0.01 of Sharpe. The queue's premise about *prevalence* is confirmed.

### 2. …but the spread does not identify the bad picks. It gets the sign backwards.

| S1 bucket (stratified) | menus | mean OOS-Sharpe regret | argmax flip | verdict flip | med dd_ratio |
|---|---|---|---|---|---|
| < 0.005 | 1746 | **0.0746** | 88.9% | 32.2% | 1.53 |
| 0.005–0.01 | 483 | 0.1069 | 85.9% | 27.1% | 1.42 |
| 0.01–0.02 | 778 | 0.0923 | 87.0% | 27.4% | 1.59 |
| 0.02–0.05 | 1608 | 0.1206 | 85.5% | 23.6% | 1.74 |
| 0.05–0.10 | 931 | 0.1427 | 80.8% | 31.6% | 1.30 |
| > 0.10 | 761 | **0.1312** | 64.9% | 27.9% | 1.20 |

**Spearman(S1, regret) = +0.155** (stratified), **+0.093** (file-level), **-0.013** (live). Regret
*rises* with the spread. A screen that abstains on small S1 abstains from the choices that cost
least. Mean regret in the live arm: 0.0404 at S1<0.01 against 0.0456 at S1>=0.01. On its stated job
— retiring chooser verdicts that rest on noise — **the screen has no discriminating power.**

Part of why: Spearman(S1, the menu's own OOS Sharpe spread) = +0.237. A tight IS menu is largely
just a tight menu, so there is less to lose by picking wrong in it.

### 3. The flip the queue asked to count is real — and it is universal, not a small-spread effect

| | all menus | S1 < 0.01 |
|---|---|---|
| **ARGMAX FLIP** (IS pick is not the menu's best arm by OOS MaxDD) | 83.5% (5265/6307) | **88.2%** |
| **VERDICT FLIP** (pick beats its menu median on one OOS column, loses on the other) | 28.4% (1791/6307) | **31.1%** |
| median dd_ratio (pick's OOS MaxDD / menu-best OOS MaxDD) | 1.49 | **1.52** |
| median OOS drawdown regret | 5.87 pp | **6.08 pp** |

File-level: 96.1% / 31.8% overall against 97.1% / 37.1% at S1 < 0.01. Live: 74.1% / 61.1%.
The answer to "how many of those flip when the pick is judged by OOS MaxDD instead" is **88.2% of
the argmaxes and 31.1% of the verdicts** — but the same is true of essentially every menu in the
record regardless of spread. **The flip is a property of scoring a Sharpe chooser on drawdown, not
a property of a thin IS margin.** Idea 371's 4.8x is the tail of that distribution, not its centre
(median 1.5x, file-level median 2.1x).

### 4. Where the screen DOES pay: as an abstention rule scored on drawdown

Live paths, taking the menu's median-IS arm instead of its argmax when S1 < t (the only place the
abstention arm can be scored, since committed grids do not carry the median arm's identity):

| threshold | menus abstained | mean OOS Sharpe | d vs argmax | **mean OOS MaxDD improvement** |
|---|---|---|---|---|
| 0 (raw argmax) | 0 | 0.8474 | — | — |
| 0.005 | 13 | 0.8577 | +0.0103 | **+1.38 pp** |
| 0.01 | 15 | 0.8540 | +0.0066 | **+1.30 pp** |
| 0.02 | 20 | 0.8589 | +0.0116 | **+1.29 pp** |
| 0.05 | 37 | 0.8529 | +0.0056 | **+1.45 pp** |
| 0.10 | 50 | 0.8397 | -0.0076 | **+2.26 pp** |

Free on Sharpe up to t=0.05 and worth 1.3–1.5 pp of OOS drawdown. And the one statistic where the
spread genuinely separates: mean dd_ratio **1.79 at S1<0.01 vs 1.195 at S1>=0.01** in the live arm —
driven by the GROSS dial, whose S1 is 0.0000–0.0001 (Sharpe is gross-invariant, ideas 311/326) while
its OOS MaxDD range is 2.0–2.5x. **The tie the spread detects is a tie in Sharpe *because the dial
is an exposure dial*, and an exposure dial's whole effect is drawdown.**

### 5. What this means for PROTOCOL (proposal, not a rules change)

Not "abstain when S1 < 0.01". The supportable clause is: **when a rule-8 menu's IS Sharpe spread is
below ~0.01, the dial is not a Sharpe dial — score the pick on OOS MaxDD and report the menu's
drawdown range beside the rho.** That is a reporting requirement, which costs nothing, rather than a
selection rule, which the corpus does not support.

### 6. KEEP paths over the live grid (225 points, all reported)

**4a 9/225, 4b 33/225** (22/10/1 at 0/10/25 bps). By panel: U56 22, B136 11, SMALL439 0.
Best: U56 TOP20 monthly @0 bps 15.2%/1.239/-19.4% (OOS 1.318) and U56 TOP20+VOLTGT t=0.12 @0 bps
12.4%/1.175/-12.7% (OOS 1.253) — both reproductions of standing record objects (ideas 329/374), not
new candidates. First failing 4b bar: H1 106, CAGR 36, H2 33, DD 17.

## Reproduction gates
- GATE 1 idea 40/41 published U56 books @10 bps: TOP3 21.9%/1.04/-25.8% **PASS**, TOP5 16.5%/0.95/-21.6% **PASS**.
- GATE 2 live RULES v2 U56 @10 bps 8.66%/1.2056/-12.05% **PASS**.
- GATE 3 idea 371's object, partial by construction: its G1 dial ran on the QQQ core-plus-sleeve
  family; this file's GROSS dial is TOP20 with g in {0.40..1.00}. What replicates is the shape —
  **S1 = 0.0000/0.0000/0.0001** at 0/10/25 bps (tighter than idea 371's reported 0.001–0.005) and an
  OOS MaxDD range of **2.4x** across the dial (idea 371: 4.8x on its own, deeper-floored grid).
  rho(IS, OOS) is **+0.400** here, not -1.00 — the perfect inversion is idea 371's book, not the
  dial's property, which is consistent with idea 371's own finding that C1 was the outlier.

## Caveats
The corpus is the record's committed CSVs — a superset of the leaderboard's prose verdicts,
including menus no chooser was ever run on, so §1's counts describe the record's *evidence*, not
exactly its published verdicts. Benchmark rows dropped. Live arm on current-constituent panels
(survivorship). Menus with fewer than 3 arms excluded.
