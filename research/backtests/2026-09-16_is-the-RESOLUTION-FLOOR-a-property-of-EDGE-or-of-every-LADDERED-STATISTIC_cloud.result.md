# Idea 1103 (cloud lane, 2026-09-16) — is the RESOLUTION FLOOR a property of EDGE or of every LADDERED STATISTIC?

**ANSWERED = OF EVERY LADDERED STATISTIC, AND THE IDEA'S PREMISE RUNS BACKWARDS. KILL of the
premise.** EDGE — the one statistic with a null attached — is the **best**-resolving of the six
on both panels at all three block lengths, and CAGR, the same book statistic with the null
removed, is the **worst**. No RULES change, no book promoted, no PROTOCOL edit (rule 6);
RULES.md, PROTOCOL.md, engine.py, scan.py, bot.py and baseline.py untouched.

## What was run
Two dials and no more: `STATISTIC` {EDGE, EDGE_FIXNULL, CAGR, S_FULL, S_OOS, DD} x `BLOCK
LENGTH` {21, 63, 126} = 18 points, all published, on **both** panels (36 rows). PANEL is not a
dial (1098's own two, reported everywhere); the LADDER is not a dial (1082/1098's nine rungs
`[5,8,10,12,15,20,25,30,40]` verbatim); q is not a dial (0.90 headline, 0.95 beside). Frozen at
1082/1094/1098/1102/1104's construction: CAND20 legs, cap INF, max_vol 0.60, gross 0.75, W, min
hold 126, 10 bps, LAG 1, warm-up 260, IS end 2016-12-31, S=40 nulls, 1000 draws, 34-step
bisection.

**GATES 16 of 16 PASS, printed before any result number.** G1/G1b fast runner ==
`engine.backtest` and == `gross_rescaler(1.0)` at 1.39e-17 on both panels; G2 committed U56
W/H126/N=20 triple 3.18e-07; G3 SPY OOS 1.70e-04; G4/G4b committed U56 n=12 / B136 n=15 triples
4.98e-05 / 2.13e-05; G5 live RULES v2 MaxDD 4.95e-05; G6 null-seed determinism 0.00e+00;
**G7 reproduces all nine of 1082/1098's committed U56 EDGE figures at 4.80e-03**; **G8
reproduces 1098's committed U56 EDGE floor@90 (3.2528 vs 3.25), peak n=12 and collapse at
7.78e-03**, G8b its B136 collapse at 9.41e-05; G9 EDGE_FIXNULL is a variance-only control
(identical point gaps, 0.00e+00); G10 every ladder live; G11 all three resamplers exact on the
identity draw (7.91e-16).

## The answer (headline L=63, q=0.90; REL_FLOOR = floor / ladder spread, 36 rung pairs)

| panel | statistic | spread | floor@90 | REL_FLOOR | unres/36 | W90 | tie set |
|---|---|---|---|---|---|---|---|
| U56 | **EDGE** | 6.407 pp | 3.253 | **0.5077** | 15 | 4 | 5;8;10;12 |
| U56 | EDGE_FIXNULL | 6.407 pp | 3.253 | 0.5077 | 15 | 4 | 5;8;10;12 |
| U56 | CAGR | 4.370 pp | INF | **1.0000** | 20 | 5 | whole ladder |
| U56 | S_FULL | 0.183 | 0.176 | 0.9614 | 33 | 7 | 7 rungs |
| U56 | S_OOS | 0.290 | 0.264 | 0.9096 | 31 | 7 | 8 rungs |
| U56 | DD | 6.726 pp | 5.684 | 0.8451 | 34 | 8 | 8 rungs |
| B136 | **EDGE** | 6.471 pp | 3.079 | **0.4759** | 15 | 4 | 5;10;15 |
| B136 | EDGE_FIXNULL | 6.471 pp | 3.079 | 0.4759 | 13 | 3 | **{10} — DECIDED** |
| B136 | CAGR | 3.594 pp | INF | **1.0000** | 32 | 5 | whole ladder |
| B136 | S_FULL | 0.121 | INF | 1.0000 | 35 | 7 | whole ladder |
| B136 | S_OOS | 0.301 | 0.172 | 0.5707 | 19 | 5 | 6 rungs |
| B136 | DD | 8.464 pp | 6.509 | 0.7690 | 23 | 6 | 7 rungs |

Cross-statistic comparison is made ONLY on three unit-free readings (REL_FLOOR, unresolved
share of 36, W90 = rungs carrying >= 0.90 of the bootstrap argmax mass), by the pre-registered
"wins >= 2 of 3" rule. Raw floors across statistics compare nothing and are never used that way.

## Hypotheses: 1 of 6 supported
- **(a) H_NULL_COSTS REFUTED, and by 6-0.** CAGR (no null) beats EDGE at **0 of 6** (panel, L)
  points; **EDGE beats CAGR at 6 of 6**. The idea's own premise is the wrong way round.
- **(b) H_FIXNULL_MID SUPPORTED 6 of 6** — but the effect is second-order and in one place it
  runs the wrong way: holding the null median fixed leaves REL_FLOOR **identical** at 5 of 6
  points and makes it **worse** at U56 L=126 (0.5077 -> 0.7273). Its one real gain is at the
  peak on B136, where it is the only cell in the whole run that **DECIDES** the ladder
  (tie set {10} at all three L).
- **(c) H_SOME_DECIDES REFUTED: 0 of 8** null-free (panel, statistic) cells decide at L=63.
- **(d) H_DD_WORST REFUTED** — **CAGR** is worst (median REL_FLOOR 1.0000), not DD (0.7690).
- **(e) H_OOS_WORSE REFUTED 0 of 6**: S_OOS resolves **better** than S_FULL at 5 of 6, on ~40%
  fewer days, because the OOS ladder spread (0.290 / 0.301) is more than double the full-sample
  spread (0.183 / 0.121). Resolution is spread-over-noise, not sample length.
- **(f) H_L_RISES REFUTED 2 of 12**: block length barely moves it (EDGE's U56 REL_FLOOR is
  0.5077 at L = 21, 63 and 126 alike).

## The mechanism, measured
`Var(dEDGE) = Var(dBOOK) + Var(dNULLMED) - 2Cov`. The null median's share of the EDGE pair-gap
variance is **+0.0615 / +0.0681 / +0.0724** on U56 and **+0.1220 / +0.1200 / +0.1283** on B136
at L = 21 / 63 / 126 — real but small, and the whole of it is the term the idea named. Its cost
in noise is tiny: median `sd(dEDGE)` 1.6486 pp against `sd(dBOOK)` 1.5910 pp on U56 (+3.6%) and
1.6322 vs 1.5659 on B136 (+4.2%). Its gain in signal is large: subtracting the DD-matched null
**widens the ladder** from 4.370 to 6.407 pp on U56 (1.47x) and from 3.594 to 6.471 pp on B136
(1.80x), because the null's own CAGR runs the OTHER way across the ladder (U56 11.88 -> 10.88 at
n=12 -> 13.04 pp at n=40; B136 13.19 -> 9.77 -> 13.46) while the book's falls monotonically.
Net signal-to-noise: **1.42x on U56, 1.73x on B136 in EDGE's favour**. That is the whole result.

## Rule 8 and both KEEP paths — nothing proposed as capital
Rung chosen on IS 2009-2016 alone, four choosers (C_ISSHARPE, C_ISDD, C_ISCAGR, C_ISEDGE), OOS
2017-2026 read once. **8 IS picks: 4b full 0, 4b OOS 0, 4a 0, median OOS Sharpe 0.9003, median
regret +0.2866.** Whole grid, 18 rungs: 4b full 3, 4b OOS 4, 4a 0 — and **no chooser reaches
any of them**: the three full-sample 4b passes are U56 n=12 (OOS 18.89% / 1.1758 / -20.17%),
U56 n=20 (16.97% / 1.1643 / -19.13%) and B136 n=15 (17.49% / 1.0458 / -19.66%), while every
chooser lands on n=5, n=8, n=30 or n=40. Benchmarks: **U56 SPY 15.10% / 0.8829 / -33.72% full
and 15.21% / 0.8711 / -33.72% OOS; B136 SPY 15.16% / 0.8861 / -33.72% and 15.33% / 0.8767 /
-33.72%; live RULES v2 U56 8.62% / 1.2007 / -12.05% and 9.45% / 1.2762 / -12.05%, B136 7.98% /
1.0993 / -12.24% and 7.88% / 1.1059 / -12.24%.** **NOTHING PROPOSED AS CAPITAL.**

## What the record should carry from here
1. **The floor is a property of the STATISTIC, not of EDGE.** All six differ, by a factor of
   more than two in REL_FLOOR (0.4759 to 1.0000) on the same nine books.
2. **A null-referenced statistic resolves BETTER, not worse.** 1098's floor is not inflated by
   its null; the null is what makes the ladder readable at all. Any future run that swaps EDGE
   for a "cleaner" raw statistic to avoid the null's sampling error will resolve strictly worse.
3. **Sample length is not the axis.** S_OOS beats S_FULL on 40% fewer days at 5 of 6 points.
4. **1102/1110's practice of quoting a floor without its statistic's spread is unreadable.** A
   floor of 3.25 pp and one of 0.176 Sharpe are the same object only after division by spread.

## Survivorship (PROTOCOL rule 9)
U56 and B136 are CURRENT-CONSTITUENT panels, so every level above is optimistic. Rung-pair gaps
and their bootstrap sign agreement contrast two books over the same inflated tape and the bias
very largely cancels out of them — which is why this run's headline is a resolvability claim and
not a capital claim. It does NOT cancel out of the 4b legs, which are measured against SPY.
