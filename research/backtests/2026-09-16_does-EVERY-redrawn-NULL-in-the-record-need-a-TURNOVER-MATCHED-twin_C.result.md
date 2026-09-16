# Idea 1060 (lane C, 2026-09-16) — does EVERY redrawn NULL in the record need a TURNOVER-MATCHED twin?

Script: `research/backtests/2026-09-16_does-EVERY-redrawn-NULL-in-the-record-need-a-TURNOVER-MATCHED-twin_C.py`
Log: `…_C.log.txt` · data: `.census.csv .claims.csv .claimsets.csv .handicap.csv .match.csv .nulls.csv .profile.csv .moves.csv .rule8.csv`
Corpus stamp: git `015b74a813db`, 969 committed `.py` + 2,203 `.md` under `research/`. Runtime 155.7s.
**GATES 10 of 10 PASS** — including G5/G6, which rebuild idea 968's published redrawn-null turnover
(max |d| 4.6e-7 x/yr) and its 40 published leg failure shares (max |d| 0.0) **bit-for-bit**.

## ANSWER: NO — not every one. Only the ones read at DAILY or WEEKLY cadence, where it changes everything.

**Two tuned dials, all points reported:** CLAIM SET (CS_ALL / CS_MD / CS_WORST) × MATCHING RULE
(UNIF / SWAP / HOLD / FIXED). 0 bps is a diagnostic on the comparand (968's C2 precedent), not a dial.

### (A) The census — what the record states
| claim set | claims | files | states null turnover ±1 line | on the claim line |
|---|---|---|---|---|
| CS_ALL (every committed file) | 2,538 | 434 | **20.7%** | 11.9% |
| CS_MD (the committed prose record) | 2,082 | 286 | 23.4% | 13.4% |
| CS_WORST (own script rotates AND prices at D/W) | **116** | 32 | **14.7%** | 9.5% |

340 scripts carry a random draw; 199 also use null / coin-flip language. By AST (not grep):
**ROTATING 25, FIXED 35, AMBIG 139** — and all 25 rotating ones price at a D or W cadence.
The ±1-line test is an **upper bound on stating** (it counts any nearby turnover token, including the
book's), so at least **79%** of the record's null-citing claims do not price their null's churn.
H_CENSUS's bar was <10% and is **FAILED** at 20.7%: the record states it more often than predicted,
mostly in the recent 931/943/968/969/1050 line of runs.

### (B) The handicap, measured (gross 0.75, 20 seeds, CAND20 as the book the null prices)
| panel | cadence | null x/yr | book x/yr | ratio | excess drag |
|---|---|---|---|---|---|
| U56 | D | 239.00 | 27.07 | **8.8x** | **2,119 bp/yr** |
| U56 | W | 49.80 | 11.00 | 4.5x | 388 bp/yr |
| U56 | M | 11.50 | 4.81 | 2.4x | 67 bp/yr |
| U56 | Q | 3.89 | 2.70 | 1.4x | 12 bp/yr |
| B136 | D | 320.78 | 33.82 | **9.5x** | **2,870 bp/yr** |
| B136 | W | 66.62 | 14.30 | 4.7x | 523 bp/yr |
| B136 | M | 15.34 | 6.53 | 2.4x | 88 bp/yr |
| B136 | Q | 5.13 | 3.63 | 1.4x | 15 bp/yr |

H_GAP (>=5x at D and W) **FAILS** on the W cells (4.53x / 4.66x). The live RULES v2 book turns over
0.84–2.73x/yr, i.e. the redrawn null churns **28x to 88x** the live book.

### (C) The matched twins — what matching does to the verdicts (10 bps, failure shares H1/H2/OOS/DD/CAGR)
| panel | cad | UNIF | → MATCHED (SWAP) | f | HOLD k |
|---|---|---|---|---|---|
| U56 | D | 1.00/1.00/1.00/1.00/1.00 | 0.60/0.45/0.35/1.00/0.65 | 0.0717 | 10 |
| U56 | **W** | 1.00/1.00/1.00/1.00/1.00 | **0.15/0.25/0.25/0.95/0.15** | 0.1458 | 5 |
| U56 | M | 0.15/0.10/0.05/0.95/0.10 | 0.00/0.10/0.05/0.80/0.10 | 0.2991 | 3 |
| U56 | Q | 0.00/0.05/0.00/0.85/0.00 | 0.05/0.00/0.00/0.65/0.00 | 0.5943 | 2 |
| B136 | D | 1.00/1.00/1.00/1.00/1.00 | 0.65/0.70/0.65/1.00/0.50 | 0.0871 | 10 |
| B136 | **W** | 1.00/1.00/1.00/1.00/1.00 | **0.05/0.25/0.15/1.00/0.00** | 0.1836 | 5 |
| B136 | M | 0.05/0.60/0.50/1.00/0.05 | 0.10/0.10/0.00/0.95/0.00 | 0.3754 | 3 |
| B136 | Q | 0.00/0.10/0.10/1.00/0.00 | 0.00/0.15/0.10/1.00/0.00 | 0.6538 | 2 |

Matching moves a leg's base rate by >=0.25 in **18 of 40** (leg × cadence × panel) cells — **45%**,
so the decisive H_MOVE **FAILS its 50% bar**. But the failure is a *location* result, not a null
result: **17 of those 18 cells are D or W**, where the move runs −0.30 to **−1.00**, and M/Q move
+0.05 to −0.20. At W the L_CAGR leg goes from 1.00 (free) to 0.15 / 0.00.

### (D) Mechanism and robustness
- **H_ZERO PASS (93.8%, bar 75%)** — at 0 bps the UNIF→SWAP move on the four return-scaled legs is
  <0.10 in 30 of 32 cells. The whole effect is the 10 bps **tax on churn**, not selection.
- **H_TWIN PASS (80.0%, bar 80%)** — SWAP (per-name probability f) and HOLD (full redraw every k-th
  decision day) agree within 0.15 in 32 of 40 cells, max gap 0.250. The result is not an artifact of
  how the match is made. 5 of 16 matched cells are **CLIPPED** (HOLD cannot reach the target at
  k=2/3/10, err −6% to −27%) and are flagged in `.match.csv`; SWAP matches to within ±5.2%.
- **H_DD FAIL** — the DD leg does **not** stay saturated under matching: 0.650..1.000 (U56 Q 0.650,
  U56 M 0.800). 968's C2 / idea 1061's "saturated comparand" reading holds at D/W, not at M/Q.

### (E) RULE 8 (PROTOCOL rule 8) — matching solved on IS 2009–2016 alone, OOS 2017– read ONCE
Book = CAND20 top-20 equal weight (the record's standing 4b construction), gross 0.75, 10 bps:

| panel | cad | full CAGR/Sharpe/MaxDD | H1/H2 | **OOS** CAGR/Sharpe/MaxDD | RULES v2 OOS Sharpe | SPY OOS Sharpe | 4a | 4b |
|---|---|---|---|---|---|---|---|---|
| U56 | W | 12.74% / 1.0603 / −18.31% | 1.073 / 1.056 | **14.35% / 1.1246 / −18.31%** | 1.2762 | 0.8711 | no | **yes** |
| U56 | M | 15.28% / 1.2125 / −19.51% | 1.205 / 1.227 | **17.53% / 1.3061 / −19.51%** | 1.2762 | 0.8711 | no | **yes** |
| U56 | D | 11.08% / 0.9514 / −18.38% | 0.931 / 0.974 | 12.83% / 1.0412 / −18.38% | 1.2762 | 0.8711 | no | no |
| U56 | Q | 14.31% / 1.0549 / −27.12% | 1.140 / 1.003 | 16.14% / 1.0911 / −27.12% | 1.2762 | 0.8711 | no | no |
| B136 | D/W/M/Q | 9.78–16.51% / 0.747–1.104 | — | 9.04–16.28% / 0.684–1.035 | 1.1059 | 0.8767 | no | no |

4a fails everywhere (v2's OOS Sharpe 1.2762 / 1.1059 is higher); 4b passes at U56 W and U56 M only —
both already committed. **The adjudication the null choice moves** (book's OOS percentile vs its null):

| panel | cad | UNIF | SWAP | HOLD | FIXED |
|---|---|---|---|---|---|
| U56 | W | 1.000 | 0.950 | 0.800 | 0.900 |
| U56 | M | 1.000 | 1.000 | 1.000 | 1.000 |
| B136 | **D** | **1.000** | **0.050** | 0.150 | 0.000 |
| B136 | **W** | **1.000** | **0.300** | 0.350 | 0.150 |
| B136 | M | 0.900 | 0.450 | 0.700 | 0.700 |

H_RULE8 **FAILS** (3 of 8 cells move >=0.25), but the three that move are B136 D/W/M, where a
percentile of 1.000 ("the book beats every coin flip") becomes **0.050 / 0.300 / 0.450** — no
evidence at all. The standing U56 candidate **survives** its matched twin (0.950 at W, 1.000 at M).

## VERDICT
**KILL** the D/W-cadence redrawn null as a comparand: at those cadences it pays 388–2,870 bp/yr the
book never pays, its five 4b legs fail at 1.000 for that reason alone, and 116 committed claims
(CS_WORST) sit on it — any "the book beats the coin flip" read there is bought, not earned.
**ANSWERED NO** to the queue's "EVERY": at M and Q the handicap is 1.4–2.4x and matching moves the
base rates by <=0.20, so those nulls stand as published.
**CONFIRM** the mechanism (H_ZERO: pure cost) and its mechanism-independence (H_TWIN).
**KILL** the universal-saturation reading of L_DD (0.650 at U56 Q).
**KEEP (proposed, not applied — PROTOCOL changes need the Sunday review, rule 6)** a PROTOCOL rule 4
clause: *"A claim adjudicated against a redrawn null must state the null's realised annual turnover
and the book's. Where the ratio exceeds 3x — in practice any null redrawn on a daily or weekly
decision grid — the claim must also be read against a turnover-matched twin (a per-name swap
probability f or a redraw period k solved so the null's realised turnover matches the book's to
within 5%), and both readings published."* The 3x bar is where this run's grid separates: the
verdict-moving cells are D (8.8–9.5x) and W (4.5–4.7x); M (2.4x) and Q (1.4x) move nothing.

**SURVIVORSHIP (PROTOCOL rule 9).** U56 and B136 are current-constituent lists, so all CAGR and
drawdown levels are optimistic. The object measured here is the difference between two nulls drawn
from the same panel on the same days, so the bias is common to both sides; where it does not cancel
it inflates CAGR and therefore flatters the **matched** null, making H_MOVE easier to pass — and it
still failed its bar. RULES.md / PROTOCOL.md / scan.py / bot.py / baseline.py unmodified (rule 6).
