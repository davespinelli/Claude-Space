# Idea 1197 — is the BOOK's NULL PERCENTILE SATURATED at every cell the record quotes it?

**Lane C, 2026-09-17. ANSWERED = YES ON BOTH LARGE-CAP PANELS, AND 23 COMMITTED CLAIMS
WERE ADJUDICATED AGAINST A STATISTIC PINNED AT ITS CEILING.** KILL as a capital finding:
no new book, no RULES change, no PROTOCOL edit (rule 6). RULES.md, PROTOCOL.md, engine.py,
scan.py, bot.py and baseline.py untouched.

SELECTION: lane C takes the SECOND open idea; 1197 was second in `## Open` and is not
EDGAR / Form 4 / 8-K / options / live-data.

## The two dials and no more (rule 4; the queue names both)

`CLAIM SET` {C_STRICT, C_PROX, C_ALL} x `DRAW COUNT K` {10, 20, 50, 100, 200, 400}
= **18 cells, every one published**. NOT dials, reported at every value: PANEL
{U56, B136, SMALL}; ANCHOR (N, cadence) {(20,W), (12,W), (20,M), (10,M)}; 20 seeds at
every K; the statistics {CH_PCT, CH_Z, CH_ISSHARPE}; the 4a/4b legs; three rule-8
choosers. 12 real books, **4,800 gross-matched null backtests**, 54 chooser cells.

## (A) The census — 103 claims, 26 at the ceiling, 23 of them load-bearing

Corpus = **32,819 committed text units** (6,999 LEADERBOARD rows, 584 CHANGELOG
paragraphs, 1,134 markdown artefacts) at commit 9e641f3.

| claim set | n | ceiling-quoted | states draw count | adjudicated | **adjudicated AT the ceiling** | adjudicated with NO draw count |
|---|---|---|---|---|---|---|
| C_STRICT (numeric percentile + null token) | 103 | 26 (0.2524) | 40 (0.3883) | 85 | **23 (0.2233)** | 49 |
| C_PROX (percentile token + null token) | 248 | 26 (0.1048) | 77 (0.3105) | 185 | 23 (0.0927) | 121 |
| C_ALL (file-level, any number) | 1,718 | 36 (0.0210) | 394 (0.2293) | 1,100 | 29 (0.0169) | 840 |

The 26 ceiling-quoted C_STRICT units are 13 memo/result notes, 12 LEADERBOARD rows and
1 CHANGELOG paragraph — the ceiling is not a artefact of one file's house style.
**22 of 103 are OVERQUOTED**: they write more decimal places than their own stated draw
count can carry (a K-draw percentile resolves to 100/(K+1) pp and no finer). And **49 of
the 85 adjudicated claims state no draw count at all**, so their resolution is not
recoverable from the committed text in either direction — that is the larger half of the
problem and it is reported as such, not merged into the 23.

## (B) The re-pricing — the statistic is a CONSTANT on B136 at the record's own K

Share of the 80 (anchor, seed) cells where CH_PCT is pinned at exactly 1.000:

| panel | K=10 | K=20 | K=50 | K=100 | K=200 | K=400 |
|---|---|---|---|---|---|---|
| U56 | 0.963 | 0.938 | 0.838 | 0.825 | 0.613 | 0.500 |
| B136 | **1.000** | 0.963 | 0.950 | 0.900 | 0.762 | 0.750 |
| SMALL | 0.425 | 0.412 | 0.163 | 0.125 | 0.037 | 0.000 |

**DISTINCT VALUES TAKEN over all 80 cells is the blunter statement: CH_PCT takes 1 value
on B136 at K=10, 2 on U56, and never more than 6 at any K <= 200 on either large-cap
panel — against CH_Z's 80 of 80 at every rung.** Anchors tied at the maximum, of 4
(1191's statistic, mean over 20 seeds): U56 3.85 -> 2.00 and B136 4.00 -> 3.00 over
K = 10 -> 400, every tie being saturation at the ceiling; CH_Z reads **1.00 at 18 of 18
(panel, K) cells**, i.e. it never ties at all. **SMALL de-saturates and is the control
that makes the point a STATISTIC property and not a machinery one** — same code, same
pool size, 0.000 saturation at K=400.

So idea 1191's reading is confirmed and extended: the saturation is not a K=10 artefact.
At **K=400 — forty times the draw count 1191 flagged — B136 is still pinned at 0.750.**

## (C) Rule 8 and both KEEP paths — the saturated statistic misses the only 4b book

Parameters chosen on 2009-2016 ONLY; 2017-2026 read ONCE. Benchmarks: **U56 SPY 15.06% /
0.8815 / -33.72% (halves 0.9600/0.8171), OOS 15.15% / 0.8686; U56 RULES v2 (live) @10 bps
8.60% / 1.1982 / -12.05%, OOS 9.42% / 1.2717; B136 SPY 15.16% / 0.8862 / -33.72%, OOS
15.33% / 0.8769; B136 LIVE 7.98% / 1.0994 / -12.24%, OOS 7.88% / 1.1061; SMALL SPY 14.06%
/ 0.8582 / -33.72%, OOS 15.33% / 0.8769; SMALL LIVE 4.64% / 0.7130 / -12.18%, OOS 4.47% /
0.6518.**

**Mean OOS Sharpe over the 18 (panel, K) picks: CH_Z 0.9324, CH_ISSHARPE 0.9065,
CH_PCT 0.8931 — the saturated statistic costs 0.0393 against the same comparison
standardised.** CH_PCT lands on N=10/M on both large-cap panels at K <= 100 (U56 OOS
1.0115, B136 OOS 0.9468) purely because first-wins breaks a 4-way tie; CH_Z lands on
U56 N=20/W at 5 of 6 K rungs. **CH_PCT never reaches the only 4b book at any K on any
panel; CH_Z reaches it at 5 of 6.** Ties are broken FIRST-WINS, deterministically, and
the tied count published — a random tie-break would have manufactured the instability
being measured.

**1 of 12 books clears 4b full AND OOS at 10 bps; 0 of 12 clear 4a.** The passer is
**U56 / N=20 / W: 14.31% / 1.1520 / -19.09%, halves 1.229/1.103, OOS 15.66% / 1.1705** —
the standing 2026-09-04 incumbent, so this grid reproducing it is **CONFIRMATORY, NOT
GENERATIVE. NO NEW CANDIDATE, NO MEMO, NOTHING ENACTED.** 5 of 54 rule-8 picks clear 4b
(all CH_Z on U56); 0 of 54 clear 4a.

## Gates — 7 of 7 pass

| gate | value | target |
|---|---|---|
| G1 fast runner == `engine.backtest` (post-warm-up) | 2.08e-17 | 0 |
| G2 determinism | 0.00e+00 | 0 |
| G3 live RULES v2 U56 MaxDD vs the record's -12.05% | -0.120549 | -0.1205 |
| G4 CH_PCT distinct values <= K+1 at every rung | 0 violations | 0 |
| G5 CH_Z mean anchors tied at its max (no ceiling) | 1.000 | 1.000 |
| G6 census sets nest C_STRICT <= C_PROX <= C_ALL | 0 violations | 0 |
| G7 null target gross == 0.75 at every rebalance row | 1.11e-16 | 0 |

## Recommendation, proposed not enacted (rule 6)

**A committed percentile-of-its-own-null figure should state its DRAW COUNT, and a value
of 1.000 (or 0.000) should be published as a BOUND — "> 1 - 1/(K+1)" — never as a point.**
On this grid alone that would restate 26 of 103 committed claims and would have stopped
23 of them being used to adjudicate anything. Where a ranking is wanted, publish the
null-standardised z beside it: it costs nothing extra to compute and it does not tie.

## Survivorship (rule 9)

U56 and B136 are CURRENT-CONSTITUENT lists; SMALL is the current output of a sub-$2B
screen less the documented `max_1d_move >= 1.0` exclusion. Every CAGR and drawdown LEVEL
is optimistic and the 4b count is an UPPER bound. The census arm is a scan of committed
text and carries no market bias at all; the saturation shares rank one construction
against its own null on one tape and the bias very largely cancels, but it does NOT
cancel out of the rule-8 OOS levels.

Script `2026-09-17_is-the-BOOK-s-NULL-PERCENTILE-SATURATED-at-every-cell-the-record-quotes-it_C.py`,
6 CSVs, console log. Follow-ups filed 1199, 1200, 1201.
