# Idea 624 — is the SELECTION-vs-TRADING dial split a record-wide law?  (lane C, 2026-09-10)

**VERDICT: KILL as a law, SPLIT as a magnitude reading. No RULES change, no book promoted, no KEEP
claimed. RULES.md, scan.py, bot.py, baseline.py and PROTOCOL.md untouched.**

## What the queue asked, and why its literal form is not executable
Idea 621 read its SELECTION/TRADING split off the same six dials that produced it. Each dial sits in
exactly one class, so on that evidence "the class predicts" and "the dial predicts" are the same
sentence, and no re-reading of 621's cells can separate them. The census leg confirms the record
cannot supply the separation either: of the **576 committed rule-8 stems** in idea 621's own census,
**534 (92.7%)** carry dial tokens of *both* classes, 40 are TRADING-only, 1 SELECTION-only. The cut
can assign **7.1%** of the record. So the answer was built rather than mined.

## Design (PROTOCOL 4: two params, both named by the queue)
* **P1 dial class** — the a-priori binary class, plus its *measured* continuous form (mean membership
  distance JAC, computed from target weights alone, before any return is read).
* **P2 control form** — DEFAULT (the record's own default rung) and MEDIAN (the ladder midpoint),
  both reported everywhere.
* **Four HELD-OUT dials** 621 never ran, two per class, classified before the grid was built:
  `look` (single-lookback ranker) and `skip` (uniform signal skip) move membership; `wscheme`
  (within-set weighting) moves weights with membership held *exactly* fixed; `phase` (rebalance
  weekday) moves neither — it is a pure timing dial.
* Four anchors from 621 (`n`, `volcap`, `gross`, `lambda`) re-run for transfer.
* 3 panels x 8 dials x 2 cost rungs x 2 control forms = 96 rule-8 cells on the FULL leg;
  396 grid arms in all (FULL / SET-only / WGT-only legs), every one reported.
* Gates: G1 fast runner vs `engine.backtest` on returns and turnover, D and W, all 3 panels
  (max|dr| 7.0e-16, max|dto| 4.4e-16); G2 cost-rung identity 6.6e-16; G3 default rung in every
  ladder; G4 IS/OOS disjoint and exhaustive (1967 + 2434 = 4401 bars); G5 wscheme's membership
  distance and phase's target distance are **exactly 0**, by construction not by assertion.

## Results
1. **The frequency law does not transfer.** Held out: SELECTION 14/24, TRADING 9/24,
   Fisher exact **p = 0.2476**; the SELECTION side is a coin flip against its own null (sign p 0.541).
2. **Class is not the special cut.** All 35 balanced 4-4 partitions of the eight dials were scored:
   the a-priori cut ranks **31 of 35** on win-rate gap, exact **p = 0.886**. Over all eight dials
   SELECTION 31/48 vs TRADING 30/48, Fisher **p = 1.000**. On 621's own anchors the ordering
   *reverses* once the cell axes change (SELECTION 17/24 vs TRADING **21/24**, `gross` **12/12**).
3. **What does survive is a magnitude statement.** Excluding exact ties, SELECTION wins at a median
   **+0.0744** OOS Sharpe and TRADING at **+0.0021** — a 35x gap in size with no gap in frequency.
   Spearman(JAC, per-dial median dSharpe) = **+0.884**; on win rate only +0.284.
4. **The mechanism is confirmed even as the law fails.** The SET-ONLY leg reproduces the FULL leg
   rung for rung on all four selection dials and is **0/48** on all four trading dials; the
   WGT-ONLY leg is 0/48 everywhere except `wscheme` (5/48).
5. **A pure timing dial harvests as much as any selection dial.** `phase` moves no target at all
   (JAC = WGT = EXP = 0), yet its rule-8 pick beats its default by **+0.108** OOS Sharpe on u56 and
   **+0.188** on small439 — idea 412's phase nuisance, and indistinguishable from content in a
   win-rate table. This is why (2) reads the way it does.
6. **PROTOCOL 4:** 4a **0/396**; 4b **25/132** FULL-leg arms. Chooser arms 4b 12/48 against no-dial
   arms 15/48 — spending the parameter still loses KEEPs (621 Q4 replicates). 24 arms clear 4b on
   the full sample *and* on the OOS window read separately; they are the u56 TOP20 no-dial book and
   its neighbours, already in the record.

## What the record should carry forward
Idea 621's split should be restated as **"membership distance predicts how big a chooser's surviving
edge is, not whether it survives"**, with the crossing evidence attached: a dial can win 12/12 at
+0.0017 (gross) and a dial that moves nothing can win +0.19 (phase). Any future claim of the form
"class X of dial survives its own default" needs the effect size beside the count.

## Caveats
Survivorship (idea 54): all three panels are current constituents; SMALL439 additionally drops 44
tickers with max_1d_move >= 1.0 and its levels are not investable history — only within-panel
arm-minus-arm contrasts are read from it. Warm-up is index[300], not the record's [260], because the
longest ladder rung needs 273 closes; the anchors' levels therefore differ slightly from 621's.
Eight dials is a small denominator for a partition test and it is stated as one: p = 0.886 rules the
cut out as *special*, it does not prove the two classes identical. MaxDD is one number off one path
(idea 321). t+1 execution, 10 bps rung (idea 126).

Artefacts: `.console.txt`, `.census.csv`, `.grid.csv` (396 arms), `.wf.csv` (288 rule-8 cells),
`.taxonomy.csv`, `.partition.csv` (all 35 partitions).
