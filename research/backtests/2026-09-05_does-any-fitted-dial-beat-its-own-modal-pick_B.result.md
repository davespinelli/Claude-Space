# Idea 189 — does-any-fitted-dial-beat-its-own-modal-pick (lane B, 2026-09-05)

**VERDICT: KILL of the generalisation as the QUEUE stated it — the constant does NOT win on all
five dials. It wins significantly on ONE (CADENCE). But the run's usable finding is the other
half of the same table: the mode arm never materially LOSES either (worst dial −0.0001 OOS
Sharpe), so "read the mode once and write it down" weakly dominates "fit the dial" across all
five, and strictly dominates on the only dial whose ladder has an interior optimum.
No RULES change, no new book, no KEEP-candidate. RULES.md, scan.py, bot.py, baseline.py untouched.**

Script `2026-09-05_does-any-fitted-dial-beat-its-own-modal-pick_B.py`, 99s, 1908 ladder rows,
53 books, 10 bps, t+1, IS ≤ 2016-12-31, OOS 2017-01-01→2026 read once.
Two tuned parameters: SELECTOR (2) × LADDER POINT (36), all reported.

## Reproduction, asserted before any new number was read
* **[a]** `fast_backtest` == `products/backtester/engine.backtest`: max|dret| 6.2e-17, max|dturn|
  1.2e-15 at D/W/M/Q. PASS.
* **[b]** CAND-20 weights == idea 78's `weights_cand` on U56/B136/BSTK100: max|dw| **0.000e+00**. PASS.
* **[c]** the 1908-row ladder reproduces idea 171's **committed** `.ladder.csv`: max|Δ| over 12
  numeric columns **3.553e-15** (worst column: turnover), `fail4b` string identical in **100.0%**.
  PASS. This run is idea 171's experiment with one arm added, not a look-alike.

## The mode arms
Every pick is IS-only; the mode is a count over picks, not a new fit. MODE-LOO for book *b*
excludes *b*'s own pick. **The LOO mode differed from the in-corpus mode in 0 of 53 books in all
10 dial×selector cells** — the mode is corpus-stable, and the in-corpus version's hindsight is
worth 0.0000 Sharpe (P6 HIT).

| dial | SEL-SHARPE modal pick | share | incumbent | what the mode IS |
|---|---|---|---|---|
| GROSS | **1.00** | 94.3% | 0.75 | ladder ENDPOINT |
| N | **20** | 22.6% | 20 | the INCUMBENT (mode arm ≡ do-nothing, 0/53 changes) |
| BAND | **0.08** | 81.1% | 0.00 | ladder ENDPOINT |
| CADENCE | **M** | 83.0% | W | **INTERIOR point** |
| SLEEVE | **0.30** | 100.0% | 0.00 | ladder ENDPOINT |

That table is the run's structural finding: of five modes, three are grid edges, one is the
incumbent already, and **exactly one — cadence — is an interior point that says something a
human did not already know.** "Read the mode and write it down" is a *different* instruction from
"do nothing" or "run to the edge of the grid" on one dial in five.

## Headline — MODE-SHARPE-LOO minus SEL-SHARPE, paired over 53 books, OOS Sharpe

| dial | mean d | t | W/L/tie | sign p | verdict |
|---|---|---|---|---|---|
| GROSS | −0.0001 | −1.06 | 1/2/50 | 1.0000 | mode behind (n.s.) |
| N | +0.0215 | +1.47 | 21/20/12 | 1.0000 | mode ahead (n.s.) |
| BAND | +0.0005 | +0.16 | 8/2/43 | 0.1094 | mode ahead (n.s.) |
| **CADENCE** | **+0.0261** | **+2.89** | **9/0/44** | **0.0039** | **MODE WINS** |
| SLEEVE | +0.0000 | — | 0/0/53 | 1.0000 | identical (selector never deviates) |

**THE COUNT: mode ahead 3/5, significant 1/5, tied 1/5, selector ahead 1/5 (by 0.0001).**
The idea's conditional ("if the constant wins on all five") is **not met** — P2 MISS, reported as
a failure. On the 4b-margin score the count is the same: CADENCE only.

## Why the count is 1 and not 5 — the deviation decomposition
On books where the selector agrees with its own LOO mode the paired difference is **exactly 0.0**
(verified, P4 HIT), so the whole gap is the deviations. Sign convention: d = mode − selector, so
d > 0 means the off-mode pick lost.

| dial | deviations | mean d given deviating | paid off | hurt |
|---|---|---|---|---|
| GROSS | 3/53 | −0.0010 | 2 | 1 |
| N | 41/53 | +0.0278 | 20 | 21 |
| BAND | 10/53 | +0.0027 | 2 | 8 |
| **CADENCE** | **9/53** | **+0.1536** | **0** | **9** |
| SLEEVE | 0/53 | — | 0 | 0 |

Idea 175's "rare off-modal picks are catastrophic" is therefore **cadence-specific, not a general
property of argmax noise**. On N the deviations are a coin flip (20 paid off, 21 hurt) with a fat
tail on both sides (−0.2397 … +0.3176); on cadence **all nine deviations hurt**, every one of them
the selector picking **Q** where the mode says M — idea 175's Q-tail, reproduced on a different
corpus and a shorter ladder. A dial whose off-mode picks are one-directionally bad is a dial where
writing the mode down is genuinely worth something; a dial whose off-mode picks are symmetric noise
is a dial where it makes no difference which of the two you use.

Per-family (the pooled t overstates — 48 of 53 books are correlated B136 draws): the CADENCE
result is the B136 family (+0.0276, n50, t +2.90); U56's two books and SMALL's one never deviate,
so they contribute exactly 0.0000 and cannot corroborate it. **One family, not three.**

## Context — every arm minus the INCUMBENT (idea 171's table, mode arms added), OOS Sharpe
| dial | SEL-SHARPE | MODE-LOO | RANDOM | ORACLE |
|---|---|---|---|---|
| GROSS | −0.0006 (LOSES) | **−0.0006 (LOSES)** | +0.0002 | +0.0014 |
| N | −0.0215 (n.s.) | **+0.0000 (≡ const)** | −0.0593 | +0.0900 |
| BAND | +0.0085 (n.s.) | **+0.0090 (n.s.)** | +0.0022 | +0.0325 |
| CADENCE | +0.0642 (BEATS) | **+0.0903 (BEATS, t+10.1)** | −0.0215 | +0.0956 |
| SLEEVE | +0.1801 (BEATS) | **+0.1801 (BEATS)** | +0.0762 (BEATS) | +0.1801 |

The mode beats the incumbent on 3/5 and loses on GROSS (P5 HIT). SLEEVE is disqualified by its own
control exactly as in idea 171 — RANDOM banks 42% of the same gain on a monotone truncated ladder.
**CADENCE is the only dial where the mode beats the incumbent, beats the selector, and beats RANDOM
(which is negative there): +0.0903 of the oracle's +0.0956, i.e. 94.5% capture with no fitting.**

## Rule 8 walk-forward — pooled over the five dials (mean over 53 books, OOS window read once)
| arm | OOS CAGR | OOS Sharpe | OOS MaxDD |
|---|---|---|---|
| CONST (do nothing) | 9.96% | 0.9638 | −17.18% |
| SEL-SHARPE (fit it) | 10.90% | 1.0100 | −18.18% |
| **MODE-SHARPE-LOO (write the mode down)** | **10.81%** | **1.0196** | **−17.85%** |
| SEL-4B | 10.57% | 0.9806 | −18.16% |
| RANDOM | 9.63% | 0.9634 | −16.80% |
| ORACLE (not implementable) | 9.49% | 1.0438 | −15.04% |
| SPY (OOS) | 15.45% | 0.8820 | −33.72% |
| RULES v1 (OOS, U56 / B136 / SMALL) | 7.73% / 5.94% / 19.31% | 0.7471 / 0.5763 / 0.6046 | −13.83% / −21.19% / −35.01% |

Writing the mode down buys **+0.0558 of OOS Sharpe over doing nothing and +0.0096 over fitting**,
with 0.33pp less drawdown than fitting and 0.09pp less CAGR. Every arm loses to SPY on CAGR by a
wide margin and beats it on Sharpe and drawdown — the corpus is 53 mostly-sub-panel books, not a
tradable proposal.

## Both KEEP paths (PROTOCOL rule 4), all 1908 ladder rows
* **4a: 1507/1908.  4b: 250/1908** — identical to idea 171 by construction of control [c].
* 214 of the 250 are sub-panels (a corpus device, not tradable). The **36 fixed-panel passes are
  all on U56/BSTK100 and all re-parameterisations of idea 2's existing book (idea 144)**; none is
  proposed. 4b binding bars over failing rows: CAGR 1223, H2 689, DD 447, OOS 405, H1 312.
* Arm-level on fixed panels: CONST 5/25, SEL-SHARPE 6/25, **MODE-LOO 5/25**, SEL-4B 8/25,
  MODE-4B-LOO 4/25, RANDOM 5/25, ORACLE 6/25. **The mode arm produces no 4b pass the constant did
  not already produce.** P7: no new KEEP.

## Predictions: 5 of 7 hit, 1 miss, 1 "see note" — the miss is the headline
P1 HIT · **P2 MISS (mode ahead on 3/5, not ≥4 — the generalisation fails)** · P3 HIT · P4 HIT ·
P5 HIT · P6 HIT · P7 see note (36 fixed-panel 4b rows, all re-parameterisations, as idea 171).

## Caveats carried, not buried
Survivorship on U56/B136/SMALL484 (idea 54) — paired comparisons unaffected, levels are not.
Idea 144 (a re-dialled book is the same book). Idea 38's calendar-day index (D and Q rebalance on
some non-trading days after 2014-09-17). Idea 126 (t+1 only). Idea 183 (GROSS/BAND/SLEEVE ladders
are truncated at the end the mode runs to). The mode is read from THIS corpus; only CADENCE=M has
been replicated on a second, disjoint corpus (idea 175, 115 books) — one replication, not a
guarantee. 48 of 53 books are correlated draws of one panel, so pooled t-statistics overstate.
