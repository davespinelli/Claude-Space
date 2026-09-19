# Idea 1196 — should a committed MC FIGURE state its PAIR FORM before its SEED?

**Lane:** C, 2026-09-19 (SECOND numbered item standing in '## Open'; 1204 was first, lane A's).
**Verdict: ANSWERED = 76 OF 470 PAIR STATISTICS ARE RECOVERABLE TODAY (0.1617), AND RETIRING THE UNRECOVERABLE ONES COSTS NOTHING IN MONEY. KILL as a capital finding — no new book.**

## Construction
Two dials and no more (rule 4; the queue names both): **CLAIM SET** {C_STRICT, C_PROX, C_ALL} (1191's nesting lexicon, verbatim, so the denominators are comparable) × **KERNEL CLASS** {LINEAR, NONLINEAR, UNCLASSIFIED} = 9 cells, **all published**. Not dials, reported at every value: PANEL {U56, B136, SMALL}; the anchor grid N {10,12,20,30} × cadence {W,M} = **24 real books**; the draw ladder K {10,20,50,100,200}; 20 seeds at every K; four choosers; the 4a and 4b legs; rule-8 OOS. Books: composite momentum score, 200d MA eligibility, gross 0.75 spread equally over N names, **10 bps, next-day execution** (PROTOCOL 2), no shorting, no leverage. Null pools: 200 gross-matched draws per anchor (at each rebalance date N names drawn uniformly from those priced that day, weight 0.75/N) — **4,800 null backtests**, IS window only, so no chooser ever sees 2017-2026. Deterministic, offline, 327 s.

**RECOVERABILITY, DEFINED MECHANICALLY.** A **LINEAR** kernel is recoverable by construction: mean over pairs of (a−b) is the difference of pooled means, so the pairing is not information (1191 G2; this run's **G2 re-confirms it at 5.55e-17**). A **NONLINEAR** kernel needs the per-draw values, so it is recoverable **only** if the unit's stem still owns a CSV with a seed/draw/rep column **and** states a draw count. A unit whose text names both kinds is **UNCLASSIFIED** and is never counted as recoverable.

## (A) The harvest — 470 pair statistics, 76 recoverable
Corpus = **35,100 committed text units** (7,710 LEADERBOARD rows, 69 CHANGELOG paragraphs, 1,261 markdown artefacts); **6,950 committed CSVs, 479 (0.0689)** carry a per-draw column.

| claim set | MC-derived | PAIR | LINEAR | NONLINEAR | UNCLASSIFIED | **recoverable today** |
|---|---|---|---|---|---|---|
| C_STRICT | 3,215 | 299 (0.0930) | 39 (1.000 rec.) | 90 (0.122 rec., 11) | 170 (0 rec.) | **50 of 299 (0.1672)** |
| C_PROX | 6,695 | 470 (0.0702) | 65 (1.000) | 145 (0.076, 11) | 260 (0) | **76 of 470 (0.1617)** |
| C_ALL | 27,046 | 470 (0.0174) | 65 (1.000) | 145 (0.076, 11) | 260 (0) | **76 of 470 (0.1617)** |

**Dial 1 moves the denominator and then stops moving the numerator: C_PROX and C_ALL contain the SAME 470 pair units**, because the pair test itself requires a generator or null token, so widening the claim set past C_PROX cannot add a pair statistic. The same shape as 1191's "39 at every claim set", reached from the other side.

**The binding leg is the KERNEL, not the seed or the artefact.** Only **11 nonlinear pair statistics in the entire record** (0.076 of 145) still own the per-draw artefact they would need. Every LINEAR one is recoverable whether or not it ever stated a seed — and only 0.108 of them did. **0.553 of C_ALL pair units cannot be classified at all** from their own text (G4b, reported not absorbed): the largest single category is a paragraph that names a difference and a rate in the same breath and never says which its MC figure is.

## (B) What the exact-pair re-publication would cost
Measured on SMALL/N=20/W: pooled (linear) form **10.4 µs**, exact-pair form **101.4 µs** (9.8×), the 200-draw **pool 28.4 s — 2.8e5× the pairing**.
- the **39** C_STRICT linear units: **zero** — they are already exact.
- the **11** recoverable nonlinear units: **0.0011 s** of pairing in total; the artefacts exist.
- the **79** lost nonlinear units: their pools must be rebuilt, **≈0.62 compute-hours** — and 2.8e5× more than the pairing that would then take. **The record's irreproducibility was never bought with compute; it was bought with a missing sentence.**

## (C) Rule 8 walk-forward — the recoverable form buys THE SAME BOOK
Benchmarks (post-warm-up / OOS 2017-2026): **U56** SPY 15.12%/0.8844/−33.72%, OOS 15.26%/**0.8738**/−33.72%; live RULES v2 @10 bps 8.62%/1.2011/−12.05%, OOS 9.46%/**1.2769**/−12.05%. **B136** SPY OOS 15.26%/0.8739; live OOS 7.85%/1.1019/−12.24%. **SMALL** SPY OOS 15.26%/0.8738; live OOS 3.64%/0.5459/−14.16%.

Choosers fitted on warm-up→2016-12-31 only, 2017-2026 read **once**. All 60 (panel × chooser × K) cells published in `.picks.csv`; at the full pool (K=200, seed-free):

| chooser | class | U56 pick / OOS Sharpe | B136 | SMALL | mean tied-at-max /8 |
|---|---|---|---|---|---|
| CH_DIFF | LINEAR, recoverable | N=10/W **1.0256** | N=10/W 0.8388 | N=10/W 0.6799 | 1.00 |
| CH_Z | LINEAR, recoverable | N=20/W **1.1660** (4b PASS) | N=30/W 0.9441 | N=20/W 0.7364 | 1.00 |
| CH_PCT | NONLINEAR, record's | N=10/W **1.0256** | N=10/W 0.8388 | N=30/W 0.6802 | **5.15** |
| CH_RATIO | NONLINEAR | N=10/W **1.0256** | N=10/W 0.8388 | N=20/W 0.7364 | 1.00 |

**THE ANSWER TO "RECOVERABLE TODAY", IN MONEY: CH_DIFF (linear, recoverable) and CH_PCT (nonlinear, the record's own form) buy the SAME BOOK at 14 of 15 (panel, K) cells and their mean modal OOS Sharpe is identical to four decimals — 0.8481 both.** The single disagreement is SMALL at K=200 and is worth **0.0003** of OOS Sharpe. So the record can re-publish every unrecoverable percentile as a recoverable difference **without changing a single purchase**.

**AND THE CLASS MEAN IS NOT THE FINDING — THE STANDARDISATION IS.** Class means read LINEAR 0.8984 vs NONLINEAR 0.8511, but that gap is carried **entirely by CH_Z** (0.9488 against 0.8481 / 0.8481 / 0.8541 for the other three). CH_Z is the only chooser that divides by the pool's own SD, and it is the only one that recovers the incumbent. **Reported as a one-chooser fact, not as a kernel-class fact.**

**THE RECORD'S PERCENTILE FORM CANNOT RANK.** CH_PCT is tied at its maximum on **5.76 of 8** anchors on U56 and **6.93 of 8** on B136 — the saturation 1191 measured — so its "pick" is the deterministic first-wins tie-break, not a choice. The linear forms are tied at **1.00 of 8** everywhere. Ties are broken first-wins and the tied count is published; a random tie-break would have manufactured the instability being measured.

**4b/4a over all 24 grid points: 3 clear 4b full+OOS, 0 clear 4a.** U56 N=20/W **14.23%/1.1448/−19.39%, halves 1.217/1.100, OOS 15.65%/1.1660/−19.39%** (the standing 2026-09-04 incumbent), U56 N=30/W (12.34%/1.1524/−18.31%, OOS 1.2276), U56 N=30/M (13.46%/1.1958/−18.13%, OOS 1.2180). **The only rule-8-reachable pass is the incumbent, reached by CH_Z — CONFIRMATORY, not generative. No new candidate, no memo, nothing enacted.** No chooser's pick beats the live book's OOS Sharpe (1.2769 on U56).

## Gates — 8 of 9 pass, and the one failure IS the finding
- **G1** starts-runner == `engine.backtest`, post-warm-up: **1.73e-17**
- **G2** LINEAR kernel: mean of paired diffs == pooled-mean diff: **5.55e-17**
- **G3 — FAILED AS FIRST STATED, REPORTED NOT ABSORBED: 0.** The mirrored-pool counterexample was pre-declared at the incumbent cell U56/20/W and reads exactly 0 there, because that book beats all 200 draws: **both mirrored pools read percentile 1.000**. The gate could not fail on the mathematics; it failed on **saturation**, which is the same defect section (C) prices.
- **G3b** same construction at the **interior** cell SMALL/N=20/M (pct 0.580, chosen mechanically as argmin|pct−0.5|): **0.035** — the mirrored pool moves the percentile where the percentile is not saturated
- **G3c** synthetic, no tape: two 4-point pools with identical mean (0.000) and sd (1.154701), percentiles **0.50 vs 0.75** (difference 0.25) — a nonlinear kernel is provably not a function of the pooled sufficient statistics.
- **G4** kernel classes partition the corpus: **1.000**
- **G4b** share of C_ALL pair units the lexicon cannot classify: **0.5532** (reported, not absorbed)
- **G5** live RULES v2 U56 MaxDD **−12.055%** against the record's −12.05%
- **G6** determinism given the pools: **0**

## Recommendation (not enacted — rule 6)
**A committed MC figure should state its KERNEL CLASS before its seed, and a LINEAR one should be published as pooled means.** Exact wording, if the Sunday review wants it in PROTOCOL: *"Any figure computed from paired draws states its kernel. A kernel whose pair-mean is a function of the pooled means is published AS those pooled means (no seed, no draw order). Any other kernel publishes its per-draw artefact."* This run prices the migration at **0.62 compute-hours and 0.0003 of OOS Sharpe**. RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py untouched.

## Survivorship (rule 9)
U56 and B136 are CURRENT-CONSTITUENT lists; SMALL is the current output of a sub-$2B screen less the documented `max_1d_move >= 1.0` exclusion (54 of 719 dropped, 665 investable plus SPY as benchmark only). Every LEVEL is optimistic and every 4a/4b count is an UPPER bound. The harvest arm scans committed text and carries no market bias. The chooser comparison ranks two estimator classes against each other on one tape and the bias largely cancels; it does **not** cancel out of the rule-8 OOS levels.

## Artefacts
`..._C.py`, `.census.csv` (35,100 units), `.censusgrid.csv` (9 dial cells), `.books.csv` (24 books), `.picks.csv` (60 chooser cells), `.gates.csv`, `.console.log`.
