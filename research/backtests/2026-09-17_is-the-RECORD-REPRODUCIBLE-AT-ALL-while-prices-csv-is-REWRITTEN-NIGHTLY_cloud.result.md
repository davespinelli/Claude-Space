# Idea 1163 (cloud lane, 2026-09-17) — is the RECORD REPRODUCIBLE AT ALL while data/prices.csv is REWRITTEN NIGHTLY?

**ANSWERED = THE BOOKKEEPING IS NOT, THE SCIENCE IS. `data/prices.csv` has NEVER been
append-only — 11 of 11 transitions restate, 9.1%–12.4% of shared cells every night, back to
2008-01-02 every time — and 6 of the record's 10 committed cross-run anchors no longer
reproduce. But only 10 of 1,584 (0.0063) 4a/4b verdict cells flip across the ten
trading-day vintages, 4a flips 0 of 528, and all 12 rule-8 picks are vintage-INVARIANT.**

The cheapest repair is a **committed tape fingerprint, 8–64 bytes per constant, and it works
only GOING FORWARD**: the record's existing constants are not recoverable, because only
**3 of 10** resolve to a single vintage from their value alone.

## The vintage population is not sampled — it is the whole thing

`data/prices.csv` has **12** recoverable vintages in git (2026-09-03 .. 2026-09-16) and
`data/prices_broad.csv` has **4**; the research record itself begins 2026-09-03. Every price
vintage any committed constant could have been computed on is in this run.

**Two of the twelve carry a since-fixed defect and are flagged rather than dropped:**
`fb208174` and `0ede2282` are **CALENDAR-INDEXED** (6,059 / 6,060 rows, 1,248 weekend bars
each), fixed by `c006b439` "Fix calendar-day index bug". Every headline below is reported
over all 12 **and** over the 10 trading-day vintages, because letting those two dominate a
spread would be as dishonest as quietly dropping them.

## Construction

Two tuned parameters and no more (PROTOCOL rule 4, the two the queue names):
`REPAIR {R_NONE, R_TOLERANCE, R_APPENDONLY, R_FINGERPRINT}` x
`GATE SET {G_ANCHOR, G_BENCH, G_VERDICT, G_ALL}` = **16 cells, every one published**.
VINTAGE is not a dial — it is the population under census. LADDER {GROSS 33, N 11} is not a
dial (1154/1159's construction): all 44 rungs built on every vintage, **704 books**.
PANEL {U56, B136} is not a dial.

## Gates — 7 of 7 PASS

| gate | what | value |
|---|---|---|
| G1 | fast runner == `engine.backtest` | 1.39e-17 |
| G2 | vintage reader at HEAD == `baseline.load_universe()` on disk | 0.00e+00 |
| G3 | determinism | 0.00e+00 |
| G4 | 1098/1102's n=12 triple on the CURRENT vintage — *reported, and its FAILING is the subject* | 3.37e-03 |
| **G5** | **CROSS-RUN 1159's 6f1fcb1 restatement census, on 1159's own RAW construction** | **5.11e-05** |
| G6 | `rebalance_mask` stable | 0.00e+00 |
| G11 | both universes BYTE-IDENTICAL from their first price vintage to HEAD | 0 changed |

G5 replays 1159's bycatch exactly — **31,505 of 258,733 cells, 48 of 58 columns, max
relative move 0.008384** — after the first attempt missed by 4.17e-02. The cause was this
run's construction, not 1159's: the 56-name universe census drops the two crypto columns
`baseline.EXCLUDE` removes, giving 31,503 of 253,495 across 46 of 56 columns. **The gate was
matched to 1159's object rather than the tolerance widened**; both censuses are published.

## (A) The census — it is not that `prices.csv` was rewritten once, it is rewritten every night

| panel | transitions | append-only | restated share (range) | median \|rel move\| | earliest cell touched |
|---|---|---|---|---|---|
| U56 | 11 | **0 of 11** | 0.0906 .. 0.1243 | ~1.1e-06 | 2008-01-02 at all 11 |
| B136 | 3 | **0 of 3** | 0.0010 .. 0.0423 | 8.4e-05 .. 5.1e-03 | 2008-01-02/04/07 |

Max relative move per transition runs 5.09e-05 .. 7.71e-02 (U56) and 4.42e-03 .. 7.14e-02
(B136). **1159's commit `6f1fcb1` was not exceptional — at 0.1243 it is merely the largest
of eleven, and the median nightly restatement is 0.0918.** Every single nightly commit
rewrites roughly a tenth of a tape going back eighteen years.

## (B) The anchors — which vintage does each committed constant actually live on?

| anchor | committed | tol | current dev | within tol | best vintage |
|---|---|---|---|---|---|
| A936_CAGR | 0.155787 | 5e-5 | 2.67e-04 **FAIL** | 1 of 12 | 868b5c36 (3.18e-07) |
| A936_SHARPE | 1.139701 | 5e-5 | 1.62e-03 **FAIL** | 1 of 12 | 868b5c36 (2.63e-08) |
| A936_MAXDD | -0.191276 | 5e-5 | 3.82e-07 PASS | **10 of 12** | f138ee9a |
| A1098_CAGR | 0.1771 | 5e-4 | 6.40e-04 **FAIL** | 8 of 12 | 868b5c36 |
| A1098_SHARPE | 1.1692 | 5e-4 | 3.37e-03 **FAIL** | 5 of 12 | 868b5c36 |
| A1098_MAXDD | -0.2017 | 5e-4 | 7.69e-06 PASS | **10 of 12** | f138ee9a |
| SPY_OOS_CAGR | 0.1521 | 5e-4 | 5.91e-04 **FAIL** | 2 of 12 | 868b5c36 |
| SPY_OOS_SHARPE | 0.8713 | 5e-4 | 2.89e-03 **FAIL** | 1 of 12 | 868b5c36 |
| SPY_OOS_MAXDD | -0.3372 | 5e-4 | 2.76e-05 PASS | **12 of 12** | f138ee9a |
| LIVE_MAXDD | -0.1205 | 5e-4 | 4.95e-05 PASS | **10 of 12** | c006b439 |

**Two facts fall straight out and neither was expected.**

**(i) Every anchor that still reproduces is a MaxDD, and every anchor that fails is a CAGR or
a Sharpe — 4 of 4 against 6 of 6.** This is 1159's own result arriving from the other side:
a maximum is flat between jumps, so it survives a restatement that moves every mean. The
same property makes it **useless as a vintage fingerprint** — SPY_OOS_MaxDD matches 12 of 12
vintages, A936_MaxDD 10 of 12. A drawdown anchor tells you the number is right and nothing
about which tape produced it.

**(ii) `868b5c36` (2026-09-15) is the best vintage for 6 of 10 anchors**, which independently
confirms the pin 1154 and 1161 chose on other grounds.

## (C) The verdict-stability arm — the part that reaches capital

**48 flips of 1,848 (vintage, ladder, rung, path) cells = 0.0260 overall; 10 of 1,584 =
0.0063 over the ten trading-day vintages.**

| path | all 12 vintages | trading-day only |
|---|---|---|
| 4b full | 13 of 616 = 0.0211 | **3 of 528 = 0.0057** |
| 4b OOS | 17 of 616 = 0.0276 | **7 of 528 = 0.0133** |
| 4a | 18 of 616 = 0.0292 | **0 of 528 = 0.0000** |

The five worst cells are all on the two calendar-indexed vintages. **The nightly rewriting
wrecks the record's bookkeeping and barely touches its science.**

## The repairs, priced

| repair | G_ANCHOR | G_BENCH | G_ALL | G_VERDICT | cost in its own currency |
|---|---|---|---|---|---|
| R_NONE | 0.3333 | 0.5000 | 0.4000 | 0.9740 | 0 |
| R_TOLERANCE | 1.0000 | 1.0000 | **1.0000** | 0.9740 | **resolution: see below** |
| R_APPENDONLY | 0.3333 | 0.5000 | **0.4000** | 0.9937 | rebuild + a frozen bug |
| R_FINGERPRINT | 1.0000 | 1.0000 | **1.0000** | 1.0000 | **8–64 bytes/constant** |

**R_APPENDONLY is not a repair — it is exactly R_NONE (0.4000 on G_ALL).** 1159 attributed
97.3% of the deviation to the extra BAR, and an append-only cache does not remove a bar.
**And it has a cost nobody has priced: started from the first vintage it carries 6,067 rows
and inherits the calendar-day index bug permanently, because a cache that may never be
restated may never be REPAIRED either.** Both tapes are published; the repair was scored on
the favourable one.

**R_TOLERANCE reaches 1.000 and the bill is entirely on one statistic:**

| statistic | trading-day vintage spread | adjacent-rung pairs blinded | all-12 spread | blinded |
|---|---|---|---|---|
| CAGR | 1.08e-03 | **0 of 42 = 0.0000** | 3.83e-02 | 42 of 42 |
| Sharpe | 6.37e-03 | **33 of 42 = 0.7857** | 1.45e-01 | 42 of 42 |
| MaxDD | 8.22e-07 | **0 of 42 = 0.0000** | 1.77e-02 | 38 of 42 |

Widening the Sharpe gate to its own vintage spread makes **78.6% of adjacent rungs on the
record's own ladders indistinguishable** — it would erase, among other things, the entire
gross-dial Sharpe ladder 1150/1154/1161 reason about. CAGR and MaxDD cost **nothing**.

**R_FINGERPRINT splits, and the halves disagree.** PROSPECTIVE: a constant committed with
its tape hash re-runs on that tape by construction — 1.000 at 64 bytes (sha256 hex) or 8
(crc32). RETROACTIVE: recovering the vintage of an **already-committed** constant from its
value alone resolves to exactly one vintage for **3 of 10** anchors. **The repair cannot be
applied backwards.**

## Hypotheses — 5 of 6 SUPPORTED

| hypothesis | bar | value | verdict |
|---|---|---|---|
| H_NOTAPPEND | >= 6 of 11 U56 transitions restate | **11** | SUPPORTED |
| H_SMALLMOVES | median \|relative move\| < 1e-4 | ~1.1e-06 | SUPPORTED |
| H_GATEFAIL | R_NONE G_ALL pass rate < 0.50 | 0.4000 | SUPPORTED |
| H_VERDICTSTABLE | verdict flip rate < 0.05 | 0.0260 | SUPPORTED |
| H_APPENDNOFIX | R_APPENDONLY G_ALL < 0.90 | 0.4000 | SUPPORTED |
| H_FPWINS | prospective >= 0.90 **and** identifiable >= 0.90 | 0.3000 | **REFUTED** |

H_FPWINS is refuted as declared because it demanded both halves. The prospective half clears
at 1.000; the retroactive half is 0.300. Reported as measured, not re-cut to pass.

## The narrow proposal (PROPOSED, NOT ENACTED — rule 6)

Under the decision rule declared before any number, **R_FINGERPRINT is the only enact-worthy
repair** (pass rate 1.000 >= 0.90; cost 8–64 bytes, far inside the 64-byte bar), and it is
enact-worthy **prospectively only**. R_TOLERANCE reaches the same pass rate but its mean
resolution lost is 0.262, above the 0.10 bar, and all of it is on Sharpe. So the cheapest
thing the record could actually do is a **compound** of the two:

> *Draft PROTOCOL rule 12, "no constant without a vintage": any figure a later run may gate
> against must be published beside the crc32 (8 chars) of the price tape it was computed on,
> and any cross-run gate on a CAGR or a MaxDD may declare a tolerance no wider than 1.1e-03
> / 8.3e-07 respectively — the observed trading-day vintage spread, which blinds 0 of 42
> adjacent rungs. No cross-run gate on a SHARPE may be widened at all; it must be
> fingerprinted, because the tolerance that would pass it blinds 78.6% of the record's own
> ladder.*

**The record's existing constants are not repairable by any of the three.** That is the
honest bottom line: 6 of 10 do not reproduce, 7 of 10 cannot even be traced to a vintage,
and the correct disposition is to re-derive them with fingerprints rather than to widen a
gate until they pass.

## Rule 8 + both KEEP paths — and the strongest result in the run

**All 12 (panel, ladder, chooser) rule-8 picks are vintage-INVARIANT: 1 distinct pick each
across all 12 (U56) / 4 (B136) vintages.** C_ISSHARPE and C_ISCAGR pick gross 1.000 on both
panels (1150's endpoints); **C_IS4B picks gross 0.625 (U56) / 0.575 (B136) on EVERY vintage
and clears 4b OOS at 12 of 12 and 4 of 4** — an independent, cross-vintage confirmation of
1154's tent pick and of today's idea 1161.

Current-vintage base rates and benchmarks:

| | U56 (88 rungs) | B136 (44 rungs) |
|---|---|---|
| 4b full / 4b OOS / 4a | 26 / 30 / **0** | 11 / 11 / **0** |
| SPY | 15.06% / 0.8814 / -33.72% (0.9598/0.8170), OOS 15.15% / 0.8684 | 15.16% / 0.8861 / -33.72%, OOS 15.33% / 0.8767 |
| RULES v2 (live) | 8.60% / 1.1980 / -12.05%, OOS 9.42% / 1.2714 | 7.98% / 1.0993 / -12.24%, OOS 7.88% / 1.1059 |
| best cell clearing 4b full AND OOS | N=12: 17.75% / 1.1718 / -20.17%, OOS 18.98% / 1.1804 | N=15: 16.78% / 1.0682 / -19.66%, OOS 17.49% / 1.0458 |

**NOTHING NEW IS PROPOSED and no memo is written here.** U56 N=12 is not a discovery —
1098/1102 committed the same cell — and the only rule-8-reachable 4b passer is 1154/1161's
gross selector, which already has today's memo under idea 1161 recommending PARK.
**4a is 0 of 132 cells on the current vintage and 0 of 528 trading-day verdict cells.**

## Survivorship (rule 9)

U56 and B136 are CURRENT-CONSTITUENT panels, so every CAGR and drawdown LEVEL is optimistic
and the 4b bars are measured against an inflated book; the bias does not cancel out of the
4b legs. It **entirely** cancels out of this run's headline claims — the census, the anchor
deviations, the verdict flips and the repair pass rates all contrast the same construction
against itself across vintages of the same panel.

Script `2026-09-17_is-the-RECORD-REPRODUCIBLE-AT-ALL-while-prices-csv-is-REWRITTEN-NIGHTLY_cloud.py`,
7 CSVs, console log. RULES.md, PROTOCOL.md, engine.py, scan.py, bot.py and baseline.py
untouched.
