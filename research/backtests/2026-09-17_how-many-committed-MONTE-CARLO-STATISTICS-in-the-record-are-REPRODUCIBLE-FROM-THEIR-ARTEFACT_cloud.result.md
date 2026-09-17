# Idea 1191 — how many committed MONTE-CARLO STATISTICS in the record are REPRODUCIBLE FROM THEIR ARTEFACT?

**Lane:** cloud, 2026-09-17, idea 2 of 2 (LAST eligible open idea).
**Verdict: ANSWERED = 39 OF 32,785, AND IRREPRODUCIBILITY IS A KERNEL PROPERTY, NOT A COMPUTE TRADE-OFF. KILL as a capital finding.**

## Construction
Two dials and no more (rule 4): **CLAIM SET** {C_STRICT, C_PROX, C_ALL} × **STATISTIC FORM** {F_MC (K sampled pairs), F_EXACT (all K×K pairs), F_POOLED} = 9 cells, all published. Not dials, reported at every value: PANEL {U56, B136, SMALL}; ANCHOR (N, cadence) ∈ {(20,W),(12,W),(20,M),(10,M)}; the K ladder {10,20,50,100,200,400}; 20 seeds at every K; the three pair kernels {DIFF, RATIO, IND}; the 4a/4b legs; three rule-8 choosers.

Price arm: **Pool B = 400 gross-matched null books per (panel, anchor)** — at every rebalance date N names drawn uniformly from those priced that day, weight 0.75/N, 10 bps, next-day execution; **Pool A = 400 63-day moving-block bootstrap resamples** of the real book's own daily net returns. **12 real books, 4,800 null backtests, 3,600 resamples.** Census vintage: commit `15f6eec` (this run's own idea-1 rows included).

## (A) The census — 39 of 32,785
Corpus = **32,785 committed text units** (6,995 LEADERBOARD rows, 576 CHANGELOG paragraphs, 1,133 markdown artefacts).

| claim set | n | states SEED | states COUNT | states PAIR FORM | **all three** |
|---|---|---|---|---|---|
| C_STRICT | 3,016 | 0.2218 | 0.3558 | 0.0869 | **0.0129 (39)** |
| C_PROX | 6,339 | 0.1065 | 0.1756 | 0.0669 | 0.0062 (39) |
| C_ALL | 25,308 | 0.0273 | 0.0505 | 0.0401 | 0.0015 (39) |

**The count is 39 at every claim set, because the three sets nest and a unit stating all three necessarily carries a generator token.** The dial moves the denominator, never the numerator: **there are exactly 39 committed units in the whole record from which a Monte-Carlo figure could be re-run, and the binding leg is the PAIR FORM (0.0869 even under C_STRICT), not the seed.** Of 5,904 committed CSV artefacts under `research/backtests`, **442 (0.0749) carry a seed / draw / rep column** at all.

## (B) The three forms — irreproducibility is a KERNEL property
Median cross-seed SD over the 12 (panel, anchor) cells, 20 seeds at each K:

| kernel | K=10 F_MC → K=400 | \|F_MC − F_EXACT\| K=10 → 400 | \|F_EXACT − F_POOLED\| max | F_MC replay @5e-3 |
|---|---|---|---|---|
| **DIFF** (linear) | 0.0698 → 0.0000 | **0.000000 at every K** | **4.44e-16** | 0.05 → 1.00 |
| **IND** | 0.0756 → 0.0060 | 0.0275 → 0.0048 | 0.500 | 0.68 → 0.15 → 0.38 |
| **RATIO** | 0.1309 → 0.0024 | 0.0116 → 0.0020 | **43.29** | 0.05 → 0.13 |

**The clean result: for a LINEAR kernel the pairing is not information.** mean over sampled pairs of (a−b) equals mean(a) − mean(b) equals the all-pairs mean, identically — `|F_MC − F_EXACT| = 0.000000` at every K and every cell, and G2 confirms F_EXACT ≡ F_POOLED at 4.44e-16. **A linear pair statistic never needed its draw order and is always recoverable from its pooled artefact.** Everything the record has lost is lost to NONLINEARITY: the indicator form's pooled substitute is wrong by up to **0.500** (it collapses to a constant 0/1 — F_POOLED cross-seed SD is exactly 0), and the ratio form's by up to **43.29**. **1148's R_MATCHED, the statistic 1188 could not replay, is a RATIO — the worst of the three.**

**An MC statistic published without its seed replays, at the draw counts the record uses, between 0.05 and 0.68 of the time to 5e-3.** The DIFF row's apparent recovery at K=400 is not reproducibility, it is the pool being exhausted (K = NDRAW leaves nothing to sample).

**AND THE EXACT-PAIR FORM COSTS NOTHING.** At K=400 on the SMALL/N=20/W cell: F_MC **4.0 µs**, F_EXACT **227.0 µs** (57.3×) — against the **33.8 s of backtests both forms share**, i.e. the exact pairing is **1.49e5×** cheaper than the pools it is computed from. **The record's irreproducibility was not bought with compute.**

**THE ONE PLACE THE EXACT FORM DOES NOT HELP, PUBLISHED NOT ABSORBED (G4b).** This run's first cut gated "F_EXACT is less seed-dependent than F_MC" over all kernels and **FAILED at 0.8936**. Every failure is a RATIO cell — **23 of 72** — and it is a finding: all-pairs enumeration gives the near-zero-Sharpe null draws in the denominator *more* weight than random pairing does, so the exact form of a ratio is **more** seed-dependent, not less. The gate was restated to what is true (G4: 1.000 over DIFF+IND) and the RATIO share published beside it.

## (C) Rule 8 walk-forward — the record's own null statistic is SATURATED
Benchmarks: U56 SPY 15.06%/0.8815/−33.72%, OOS 0.8686; U56 RULES v2 live @10 bps 8.60%/1.1982/−12.05%, OOS 1.2717. B136 SPY 15.16%/0.8862/−33.72%, OOS 0.8769; live 7.98%/1.0994/−12.24%, OOS 1.1061. SMALL SPY 14.06%/0.8582/−33.72%, OOS 0.8769; live 4.30%/0.6637/−13.89%, OOS 0.5601.

**CH_PCT — the record's form, the book's IS Sharpe percentile inside its own null — cannot rank anchors at all on the large-cap panels.** Mean anchors tied at the maximum (of 4): U56 **3.80 → 2.00** over K = 10 → 400, B136 **3.90 → 3.00**, and the tie is saturation at 1.000 in every case. **The seed provably cannot move that pick, because the statistic has nothing to move: 1 distinct pick over 20 seeds at 6 of 6 K rungs on U56 and B136.** Only SMALL de-saturates (1.80 → 0.00 tied), and there the seed *does* move it once (2 distinct picks at K=50).

**CH_Z — the same comparison standardised by the pool's own mean and sd, which does not saturate — moves with the seed at exactly the draw counts the record publishes.** U56: **3 distinct picks over 20 seeds at K=10 (modal share 0.85), OOS Sharpe spread 0.1637**; B136: 3 distinct at K=10 and K=20 (modal share 0.65), **OOS spread 0.1097**; SMALL: 2 distinct at K=10/20, spread 0.0081. The instability dies at K ≥ 50 (U56), K ≥ 200 (B136), K ≥ 50 (SMALL). **So an unpublished seed is worth up to 0.164 of OOS Sharpe on a K=10 null and nothing on a K=200 one.** (The `saturated` column is defined for CH_PCT; for a z-score "≥ 1.0" is trivially true and the column is not informative there.)

Ties are broken **first-wins and deterministically**, and the tied count is published: a random tie-break would have manufactured the very instability being measured.

**1 of 12 books clears 4b full and OOS at 10 bps; 0 of 12 clear 4a.** The one passer is **U56 / N=20 / W — 14.18% / 1.1411 / −19.39%, halves 1.223/1.088, OOS 15.55% / 1.1598, null percentile 100.0** — the standing 2026-09-04 incumbent, so **CONFIRMATORY, not generative. No new candidate, no memo, nothing enacted.** CH_ISSHARPE (no null at all) picks N=10/M on U56 (OOS 1.0031), N=20/M on B136 (0.9735) and N=20/W on SMALL (0.7360): **the null-based choosers and the plain IS-Sharpe chooser disagree at 3 of 3 panels, and the null-based ones pick the better OOS book at 3 of 3** — which is an argument for the null, not against it, provided its draw count is large enough to resolve.

## Gates — 8 of 8 pass, including one defect this run found in the engine
- **G1** starts-runner == `engine.backtest`, post-warm-up: **2.08e-17**
- **G1b — REPORTED, NOT ABSORBED.** `engine.backtest` does `weights.shift(1)` **without filling**, so row 0's target is NaN; turnover is NaN at row 0 and again at the first rebalance-application row, and the NaN propagates into `returns` at exactly those two rows (**2008-01-02 and 2008-01-07** on U56). **Every committed "fast runner == engine.backtest" gate in the record compared pandas Series, whose `.max()` is skipna, so those two rows have never been checked by any of them.** Both sit inside the 260-day warm-up every metric discards (warm-up ends 2009-01-13), so **no committed figure moves** — but the gate that was supposed to catch it could not. Filed as 1198.
- **G2** DIFF kernel F_EXACT ≡ F_POOLED: **4.44e-16**
- **G3** RATIO/IND kernels F_EXACT ≠ F_POOLED: **43.29** (> 0 expected)
- **G4** F_EXACT cross-seed SD ≤ F_MC's on DIFF+IND: **1.000 of 144 cells**
- **G4b** same on RATIO: **0.681 of 72** (< 1 expected, see above)
- **G5** live RULES v2 U56 MaxDD **−12.0549%** against the record's −12.05%
- **G6** determinism given the pools: **0**

## Recommendation (not enacted — rule 6)
A committed Monte-Carlo figure should state its **pair form** before its seed: the seed is recoverable-by-convention, the kernel is not. The cheap, checkable form: **publish the EXACT-PAIR value for any nonlinear kernel** — it costs 1.49e5× less than the pools it summarises and is seed-free by construction — **and publish a LINEAR kernel's pooled means instead of its pairs**, since they are the same number. RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py untouched.

## Survivorship (rule 9)
U56 and B136 are CURRENT-CONSTITUENT lists; SMALL is the current output of a sub-$2B screen less the documented `max_1d_move >= 1.0` exclusion (52 of 715 dropped, 663 investable names plus SPY as benchmark only). Every LEVEL is optimistic and every 4a/4b count is an UPPER bound. The census arm is a scan of committed text and carries no market bias at all. The reproducibility statistics rank one construction against itself on one tape and the bias largely cancels; it does **not** cancel out of the rule-8 OOS levels.

## Artefacts
`..._cloud.py`, `.census.csv` (32,785 units), `.censusgrid.csv` (3 claim sets), `.books.csv` (12 books), `.forms.csv` (216 form cells), `.picks.csv` (36 chooser cells), `.gates.csv`, `.console.log`.
