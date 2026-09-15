# Idea 943 (lane C, 2026-09-15) — should every published CADENCE or TURNOVER claim carry its NULL'S GAIN?

**ANSWERED = YES, AND ~89% OF THE RECORD'S CLAIMS DO NOT. KILL** for the record's un-null'd cadence
and turnover claims as evidence about a rule; **PARK unchanged** for U56/TOP20 (this run is its
third independent strike this week); nothing promoted; rule 6 untouched. `RULES.md`, `PROTOCOL.md`,
`scan.py`, `bot.py` and `baseline.py` are not modified.

Script `research/backtests/2026-09-15_should-every-published-CADENCE-or-TURNOVER-claim-carry-its-NULL-GAIN_C.py`
with `.census.csv` (2,750), `.census_headline.csv` (8), `.books.csv` (64), `.null.csv` (19,200),
`.gain.csv` (64), `.rescore.csv` (8), `.walkforward.csv` (16), `.hypotheses.csv`, `.gates.csv`,
`.console.txt`. Runtime 133.3 s, deterministic, offline (`load_prices` fell back to the committed
`data/prices.csv` cache — no network call was made or attempted successfully).

---

## 1. What was asked, and what the right subtrahend is

Idea 931 found the W→M improvement on the standing candidate is a **turnover rebate every book
collects**: on U56/TOP20 the null's own median gain runs +0.0466 / +0.3334 / +0.7624 / +1.4501 at
0 / 10 / 25 / 50 bps while the book's runs +0.0994 / +0.1525 / +0.2321 / +0.3645. Slowing a book
down cuts turnover, and at a fixed cost rung *every* book — including a coin flip — is paid for
that. So a published "monthly beats weekly by X of Sharpe" is evidence about the **rule** only in
the part of X that exceeds what a gross-matched random book collects for free on the same panel
over the same cadence step. The queue asked for the record-wide form: census the committed
cadence and turnover claims for whether any priced that null gain, and re-score those that did not.

**Two tuned dials, all 8 points reported and never merged:** CLAIM SET {STRICT, WIDE} × COST RUNG
{0, 10, 25, 50} bps. Reported axes, nothing fitted on them: PANEL {U56, B136} × BOOK TEMPLATE
{TOP20 = idea 670's `CAND20`, TOP05 = RULES v1's own width} × CADENCE STEP {D→W, W→M, M→Q, W→Q} ×
WINDOW {FULL, IS, OOS, H1, H2}, 300 draws per (panel, template, cadence) with the 150-draw
half-sample beside it.

## 2. GATES — 8 of 8 PASS, printed before any result number

| gate | stat | bar |
|---|---|---|
| G1 fast runner == `engine.backtest` (TOP20, U56, W and M) | dret 2.08e-17 / 4.16e-17, dturn 4.44e-16 / 6.66e-16 | 1e-9 |
| G2 null TARGET gross / count / per-name weight == the book's, all 16 cells | 2.220e-16 / 0 / 0.000e+00 | 1e-12 / 0 / 1e-12 |
| G3 **CROSS-RUN** vs idea 931's published U56/TOP20 W→M book **and NULL MEDIAN** gains, 4 rungs | book d **0.0000 / 0.0000 / 0.0000 / 0.0000**; null d 0.0057 / 0.0049 / 0.0024 / 0.0015 | 0.060 |
| G4 draw legality \|P(t)\| ≥ k(t) on every decision row | 0 rows short | 0 |
| G5 determinism, same seed → same null series | 0.000e+00 | 0 |
| G6 the null is INVESTED on every cell | min median realised gross 0.7500, min vol 0.1002 | > 0.50 / > 0.01 |
| G7 census corpus is the committed tree | 908 md files, 7,362,982 bytes, 2,750 claim units | > 700 / > 0 |
| G8 the draw is UNIFORM and NON-DEGENERATE | max \|observed − hypergeometric E\| **0.0164**, max E 0.5693 | \|d\| < 0.02 / E < 0.95 |

**G3 is the strong one and it is an independent reproduction:** at a different seed and a different
draw budget (300 vs 500) this tree reproduces idea 931's book gains to four decimals and its null
medians to ≤ 0.0057 of Sharpe. The mechanism is not a one-run artefact.

**G8 was RE-SPECIFIED after its first cut, stated not hidden.** The first formulation was a flat
"mean null-vs-book name overlap < 0.50" and **FAILED at 0.5749** — but that is not degeneracy: on
U56 a TOP20 book holds 20 of a ~28-name eligible pool, so a *uniform* draw is supposed to overlap
~0.57. A flat bar would have condemned idea 931's own accepted construction. The object the gate
needs is (a) uniformity — observed overlap == the hypergeometric expectation E[k/|P|] — and (b)
non-degeneracy — that expectation itself below 1, which is exactly what rules out an
equal-weight-everything template, where the gross-matched draw must take the whole pool and the
"null" *is* the book. The re-specified gate passes at 0.0164.

## 3. PART A — THE CENSUS

Corpus: **908 committed `.result.md` / `.memo.md` files (7,362,982 bytes) + 499 CHANGELOG entries +
6,312 LEADERBOARD lines.** Claim unit = one paragraph (or one leaderboard row) carrying a
cadence-or-turnover AXIS token; STRICT additionally requires a COMPARATIVE token, a METRIC word and
≥ 2 numerals.

| claim set | claims | priced the null's GAIN (UPPER) | own paragraph states it (LOWER) | null LEVEL only | no null at all |
|---|---|---|---|---|---|
| **STRICT** | **1,487** | 165 = **11.10 %** | 131 = **8.81 %** | 688 = 46.27 % | 634 = 42.64 % |
| **WIDE** | **2,750** | 301 = **10.95 %** | 164 = **5.96 %** | 1,355 = 49.27 % | 1,094 = 39.78 % |

Axis split (WIDE): CADENCE 1,233, TURNOVER 1,190, BOTH 327. By source, STRICT `share_gain_priced`:
MEMO 12.58 %, LEADERBOARD 10.76 %, CHANGELOG 8.60 %. Across distinct runs: **45 of the 481 runs
carrying a STRICT claim** price a null gain anywhere in their family (9.4 %).

**The upper bound is deliberately generous and still damning.** `share_gain_priced` credits the
whole run family — a run that priced a null delta on *some other* axis counts — so the true share
sits inside **[5.96 %, 11.10 %]** and **1,322 of 1,487 STRICT claims (88.90 %) never subtracted the
rebate**, 658 of them on the turnover axis, 441 on cadence, 223 on both. **H_CENSUS PASSES**: the
record is not uniformly guilty — roughly one claim in nine already does this. **H_CLAIM PASSES** at
0.15 pp: the headline is not a claim-set artefact.

## 4. PART B — THE RE-SCORE: what the un-priced claims did not subtract

**H_EXCESS FAILS at 0 of 16.** At PROTOCOL's own 10 bps, on **every** (panel, template, step) cell
the book's cadence gain is **below** its own gross-matched null's median gain.

| panel | template | step | book gain | null median gain | **excess** | book pctile | ann. turnover drop |
|---|---|---|---|---|---|---|---|
| U56 | TOP20 | D→W | +0.1090 | +1.3414 | **−1.2324** | 0.0 | 16.07 |
| U56 | TOP20 | W→M | +0.1525 | +0.3285 | **−0.1760** | 0.0 | 6.20 |
| U56 | TOP20 | M→Q | −0.1561 | −0.0086 | **−0.1476** | 2.7 | 2.11 |
| U56 | TOP20 | W→Q | −0.0037 | +0.3212 | **−0.3249** | 0.0 | 8.30 |
| U56 | TOP05 | D→W | +0.1135 | +2.1555 | **−2.0420** | 0.0 | 27.53 |
| U56 | TOP05 | W→M | +0.0924 | +0.4775 | **−0.3851** | 2.0 | 10.75 |
| U56 | TOP05 | M→Q | −0.1563 | +0.0147 | **−0.1710** | 17.3 | 3.83 |
| U56 | TOP05 | W→Q | −0.0639 | +0.4957 | **−0.5596** | 0.0 | 14.58 |
| B136 | TOP20 | D→W | +0.1960 | +2.0784 | **−1.8824** | 0.0 | 19.51 |
| B136 | TOP20 | W→M | +0.1603 | +0.4271 | **−0.2668** | 0.3 | 7.78 |
| B136 | TOP20 | M→Q | −0.1765 | +0.0430 | **−0.2195** | 0.3 | 2.90 |
| B136 | TOP20 | W→Q | −0.0162 | +0.4641 | **−0.4803** | 0.0 | 10.67 |
| B136 | TOP05 | D→W | +0.2475 | +2.2293 | **−1.9818** | 0.0 | 33.16 |
| B136 | TOP05 | W→M | +0.2921 | +0.4479 | **−0.1558** | 20.0 | 12.33 |
| B136 | TOP05 | M→Q | −0.0842 | +0.0375 | **−0.1217** | 25.3 | 4.98 |
| B136 | TOP05 | W→Q | +0.2079 | +0.4912 | **−0.2833** | 7.3 | 17.31 |

The book sits at the **0.0th percentile of its own null's improvement distribution on 8 of 16
cells** and never above the 25.3rd. The largest single un-subtracted rebate on the grid is
**+11.2642 of Sharpe** (B136/TOP05, D→W, 50 bps) — a number no committed book gain in this record
comes within an order of magnitude of.

**H_RUNG FAILS at 0.625, and the failure is the finding.** At **0 bps the null's median cadence
gain is NEGATIVE** (median across cells −0.0279; positive on only 2 of 16) and the book beats it on
**6 of 16** cells; at 10 bps the null's median is positive on 15 of 16 and the book beats it on
**0 of 16**. Who wins the cadence contest is decided by the cost rung, not by the rule. **A cadence
claim quoted without its rung is not a claim**, exactly as idea 933 concluded for a Shapley share.

**H_REBATE FAILS at 15 of 16**, and narrowly: U56/TOP20 M→Q reads −0.0086 at 10 bps. The rebate is
a property of *how much turnover the step removes*, not of slowing down as such — the M→Q step
removes only ~2.1x of annual turnover against D→W's ~16–33x. The rebate is universal at 25 and 50
bps (16 of 16) and universal in direction, not in level.

**All 64 (panel × template × step × rung) grid points are published in `.gain.csv` and printed in
full in `.console.txt`.** Nothing is withheld.

## 5. PART C — RULE 8 WALK-FORWARD (cadence chosen on 2009–2016 alone, 2017–2026 read ONCE)

Both KEEP paths evaluated on all 16 (panel × template × rung) cells. **OOS 4b 3 of 16, 4a 0 of 16.**

OOS bars: **SPY 15.27 % / 0.874 / −33.72 %**; **RULES v2 (live) 9.46 % / 1.277 / −12.05 %**.

The cadence CHOICE transfers cleanly — every IS-only chooser picks M or Q, never W or D — and all
three 4b passes are U56/TOP20, at 0 / 10 / 25 bps. The 10 bps pick reads **OOS 17.53 % / 1.305 /
−19.51 %** on a FULL-sample 15.28 % / 1.212 / −19.51 %, halves 1.204 / 1.226. **4a fails
everywhere**: v2's OOS Sharpe 1.277 is not beaten in both halves at any rung.

**And the walk-forward carries the same defect it was built to test.** Handed the *same* IS-only
chooser, the null picks the same slow cadence (mode Q, 87.3 % of 300 draws at 10 bps) and collects
an OOS median gain over weekly of **+0.2518 against the book's +0.1821 — OOS excess −0.0697**.
Across all 16 cells the OOS excess is positive on **2 of 16**, both at 0 bps. **The 4b pass is a
statement about the book's LEVEL; the cadence decision that produced it is worth less than a coin
flip's.** This is a third independent strike on the same standing candidate, after idea 933's
answer-key mega-cap sleeve (margin-kill 1.23) and idea 938's rebalance-offset artefact.

## 6. PRE-REGISTERED BARS

| bar | stat | verdict |
|---|---|---|
| H_CENSUS ≥ 1 committed claim prices its null's GAIN | 165 of 1,487 STRICT; 301 of 2,750 WIDE | **PASS** |
| H_REBATE null median gain > 0 on EVERY cell at 10 bps | 15 of 16; min −0.0086 | **FAIL** |
| H_EXCESS book gain > null median on ≥ 50 % of cells at 10 bps | **0 of 16 = 0.0000** | **FAIL** |
| H_RUNG 0 bps and 10 bps verdicts agree on ≥ 90 % of cells | 0.6250 | **FAIL** |
| H_CLAIM census headline moves ≤ 5 pp between claim sets | 11.10 % vs 10.95 % = 0.15 pp | **PASS** |
| H_WF rule 8: any IS-only cadence pick clears 4a or 4b OOS | 4b 3 of 16, 4a 0 of 16 | **PASS** |

## 7. THE GUARD THIS PROPOSES (for Sunday review — PROTOCOL.md is NOT edited here, rule 6)

> **PROTOCOL 10 (proposed).** Any published claim that a change of REBALANCE CADENCE or of
> TURNOVER improved a book must quote, beside the book's gain, (a) the **cost rung** the gain is
> read at and (b) the **median gain of the book's own gross-matched null over the same step at the
> same rung**, with the book's percentile in that null's improvement distribution. A cadence or
> turnover gain smaller than its null's median is a **turnover rebate, not a result**, and may not
> be cited as evidence about the rule.

Cost of adopting it as measured here: **1,322 of 1,487 committed STRICT claims (88.9 %) would need
the second number**, and on the 16 cells this run rebuilt, **0 of 16 would survive it at 10 bps**.

## 8. SURVIVORSHIP, and which way it cuts

U56 and B136 are **current-constituent lists**, so every CAGR and drawdown LEVEL above is
optimistic. The direction for this run's headline is specific and works **against** the books: a
coin flip drawn from a survivor panel is a *better* book than one drawn in real time, so every null
gain here is an **upper bound** on the honest null and every book's excess over it is a **lower
bound** — a cell where the book fails to out-gain its null fails a fortiori. The 4b bar is SPY,
which is not survivorship-inflated. The 663-name SMALL panel was **not** run here and this file
makes no claim about it; idea 931 read it and found the same direction (0.0 percentile). Stated,
not hidden.

## 9. VERDICT

**KILL** for the record's un-null'd cadence and turnover claims as evidence about a rule — on the
generous upper-bound reading **88.9 % of committed STRICT claims (1,322 of 1,487) quote a gain they
never differenced against the free rebate**, and on the 16 cells this run rebuilt the book loses to
its own null at **0 of 16** at 10 bps. **PARK unchanged** for U56/TOP20 — its 3 OOS 4b passes are a
level fact on a book that now carries three independent strikes, and its OOS cadence excess is
−0.0697. **Nothing promoted, no RULES change, no PROTOCOL edit, rule 6 untouched.**
