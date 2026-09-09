# Idea 515 (lane C) — restate the record's 158 REPRODUCTION GATES as TOLERANCES in record units

**Verdict: ANSWERED / the restatement DOES NOT RESCUE THE RECORD.** No KEEP, no memo, no rule
change. `RULES.md`, `PROTOCOL.md`, `scan.py`, `bot.py`, `baseline.py` untouched.

Script: `2026-09-09_restate-the-record-s-158-REPRODUCTION-GATES-as-TOLERANCES-in-record-units_C.py`
Artefacts: `.census.csv` (520 clauses), `.gates.csv` (171 recorded), `.status.csv`, `.ladder.csv`
(21 grid points), `.keeppaths.csv` (30 arms), `.walkforward.csv`, `.console.txt`.

## Parameters (two, as the queue allows; every grid point reported)

* **P1 tolerance bar**, 7 levels: the gate's own declared bar (`native`), then 1e-12, 1e-9, 1e-6,
  **1e-4**, **1e-3**, 1e-2 applied to the observed |delta|. The two bold rungs are the queue's own.
* **P2 sample**, 3 nested levels: S12 ⊂ S24 ⊂ S48 of the 158, ordered by `md5(filename)` so the
  sample spans dates instead of following them.

Nothing is tuned on an outcome. Deterministic: two independent runs agree on every number.

## Method — why the gates could be measured at all

A reproduction gate is an `assert`; when it fails it raises, so the record has never seen **how
far off** it is, and one failing gate hides every gate behind it. Each target is parsed and every
`assert` is AST-rewritten into a recording call that evaluates the same expression, writes
`(observed, declared bar, pass)` to a JSONL file and **never raises**. `A and B` is split into
separately-recorded clauses; a chained compare into one record per link. Writes under
`research/backtests/` are redirected to a scratch mirror (idea 513's machinery) — **no committed
artefact was touched**. Prices, code and interpreter unchanged. A script killed by the 150 s
timeout still reports every gate it reached, which is why 14 timeouts still contribute data.

## Reproduction gate (recorded, non-raising, before any new number)

Idea 513's own regexes re-run on the 158 scripts it named: **158 / 136 / 22 / 27** against its
published 158 / 136 / 22 / 26. **Three of four legs are exact.** The fourth is off by exactly one
and the whole gap is **idea 513's own script counting itself** — excluding it gives 26. Confirmed
against git: the reader count is 26 at `4f974a2` (the tree without that file) and 27 at `e5125ca`
(with it). A census carrying no vintage stamp cannot tell those two trees apart, which is
precisely idea 514.

## [A] What the record's gates actually are (all 158 scripts, 520 clauses, no sampling)

| clause form | n | share |
|---|---|---|
| tolerance (`x < tol`) | 345 | 66.3% |
| exact numeric (`==`) | 87 | 16.7% |
| structural (`.equals`, `not bad`, set/index tests) | 46 | 8.8% |
| count (`len(...) == k`) | 40 | 7.7% |
| floor (`x >= k`) | 2 | 0.4% |

Declared bars: median **1e-12**, mode 1e-12 (233 clauses), **85.8% at ≤ 1e-9**. Only 38 of 345
declare anything looser than 1e-6 (5e-4 ×15, 5e-3 ×9, 1e-4 ×8, 1e-3 ×2, 2e-3 ×2, 2e-2 ×1, 260 ×1).

**The record almost never writes the unit into the gate: 412 of 520 clauses (79.2%) carry no
recoverable unit** in their source or message. Establishable: count 36, dd 19, sharpe 14, cagr 12,
turnover 10, weight 8, price 4, share 4, return 1. This is the finding that limits every bar
proposal below — a bar in "record units" cannot be applied to a gate that does not say what unit
it is in.

## [B] Re-execution (S48)

48 scripts: rc=0 **31**, rc=124 (timeout, gates still recorded) **14**, other rc **3**. **171 of the
sample's 199 static clauses were reached (85.9%)**; the remaining 28 sit behind an early exit, a
timeout or an untaken branch and are reported as UNREACHED, never as passing. Of the reached
clauses, 156 are numeric (tol 118, count 24, exact 13, floor 1) in 41 scripts; 15 are structural.

## [C] The ladder — all 21 grid points

`gate` = share of numeric gates surviving; `claim` = share of scripts **all** of whose numeric
gates survive (the queue's "published claims").

| bar | S12 gate | S12 claim | S24 gate | S24 claim | S48 gate | S48 claim |
|---|---|---|---|---|---|---|
| native | 0.8333 | 0.6364 | 0.8421 | 0.7143 | **0.8718** | **0.6585 (27/41)** |
| 1e-12 | 0.7500 | 0.3636 | 0.7500 | 0.5714 | 0.8205 | 0.5854 (24/41) |
| 1e-9 | 0.7500 | 0.3636 | 0.7500 | 0.5714 | 0.8269 | 0.5854 (24/41) |
| 1e-6 | 0.7500 | 0.3636 | 0.7500 | 0.5714 | 0.8269 | 0.5854 (24/41) |
| **1e-4** | 0.7917 | 0.3636 | 0.7895 | 0.5714 | 0.8462 | 0.5854 (24/41) |
| **1e-3** | 0.8958 | 0.6364 | 0.8816 | 0.7619 | **0.9038** | **0.7317 (30/41)** |
| 1e-2 | 0.9583 | 0.8182 | 0.9737 | 0.9048 | 0.9808 | 0.9268 (38/41) |

**HEADLINE. Restating the gates at the queue's |dSharpe| < 1e-3 recovers 3 of the 14 failing
claims and no more: 27/41 published claims survive their own gate today, 30/41 survive at 1e-3,
and 11 of 41 still fail.** Only at 1e-2 — a bar that is nearly toothless in Sharpe units — do 38
of 41 survive.

**The tight end is NOT monotone against native (58.5% vs 65.9%): a uniform machine-precision bar
is STRICTER than the record's own**, because 38 tolerance clauses declare a bar looser than 1e-6.
Any adopted bar must be `min(native, proposed)`, not a flat replacement.

### The queue's two bars, applied only where the unit is establishable

| unit | n | native pass | at the queue's bar | median \|d\| | max \|d\| |
|---|---|---|---|---|---|
| sharpe | 5 | 40.0% | **60.0%** at 1e-3 | 7.85e-4 | 4.71e-3 |
| cagr | 3 | 0.0% | **0.0%** at 1e-4 | 1.25e-3 | 8.09e-3 |

**|dSharpe| < 1e-3 is right-sized; |dCAGR| < 1e-4 is one to two orders too tight** — the observed
CAGR restatement is 1.25e-3 to 8.09e-3 (0.12 to 0.81 pp) and clears the proposed bar 0 times out
of 3. Sample sizes are 5 and 3; this is a direction, not an estimate.

### Where the failures are

20 of 156 numeric gates fail natively, in 14 scripts. **18 of the 20 sit below 1e-2**; failing
|d| quantiles: min 1.8e-5, p25 7.85e-4, **median 3.83e-3**, p75 8.23e-3, max 0.3898. The maximum
is a `c*` compared against idea 335's committed `grid.csv` under `d < 1e-9` — **0.39 bps**, well
inside the 2-bps integer step idea 513 measured on the same dial, i.e. one restatement step, not
a code failure.

The single most instructive case: `abs(m['Sharpe'] - 1.133) < 5e-4` appears in **three different
scripts** (`defensive-class-census_B`, `is-a-class-member-just-its-own-ladder-point_B` and `_B2`)
and reads **7.85e-4 in all three** — one published constant, three claims, all three failing at
5e-4 and all three recovered at 1e-3. Against that, `abs(m['CAGR'] - 0.2185) < 5e-4` reads
1.25e-3 and is recovered by neither.

**Structural gates cannot be restated as a tolerance at all.** 15 reached, 3 fail. One is
`2026-09-04_crypto-sleeve_C.py`'s `px.index.equals(pxb.index)` — the primary and broad panels no
longer share an index because `data/prices.csv` gained 2026-09-08 while `data/prices_broad.csv`
is cached Fridays. That is a **vintage stamp problem (idea 514), not a tolerance problem**, and
it is 8.8% of the record's gates.

**Attribution.** Reading each script's panel statically (following one level of sibling-module
import, because several scripts get `px` from an imported helper): **all 14 natively-failing
scripts read the moving file `data/prices.csv`; the 2 sample scripts that read only the static
panels fail 0 of 6 gates.** Consistent with idea 513's attribution — but the static-only cell is
2 scripts, so this corroborates rather than establishes.

## [D] What the bars are WORTH in PROTOCOL units — U56, 30 arms, 10 bps, weekly, t+1

Live RULES v2 (band 0.03, gross 0.75): CAGR 8.64%, Sharpe 1.204, MaxDD -12.05%, H1/H2
1.231/1.183, OOS Sharpe 1.282. SPY: CAGR 15.19%, Sharpe 0.887, MaxDD -33.72%, H1/H2 0.959/0.829,
OOS Sharpe 0.879, OOS CAGR 15.38%.

**4a 0/30. 4b 6/30** — the entire gross-1.00 column at every band (margins +0.0031 … +0.0094).
That is **not a new candidate**: it sits inside idea 442's published admissible-gross window
[0.921, 1.287] for this exact cell, and idea 406 flags the whole family as priced with cash
credited at zero. No memo is written for it.

Margins: |4a| min 0.0000, p10 0.0140, **median 0.0385**; |4b| min 0.0031, p10 0.0066, **median
0.0222**.

**Worst-case verdict flips when every Sharpe leg moves by ±1e-3 and every CAGR leg by ±1e-4:
4a 3/30, 4b 0/30 — and all three 4a near-flips are band 0.03, i.e. the live book compared against
itself at a different gross (margins 0.0000 / -0.00025 / -0.00052), which is structurally ~0 and
not a knife-edge. On every arm that is not a self-comparison, both bars flip nothing.**

### Rule 8 walk-forward (band chosen on 2009-2016 alone, 2017-2026 read once)

| gross | IS pick | IS Sharpe | OOS CAGR | OOS Sharpe | OOS MaxDD | beats base | beats SPY |
|---|---|---|---|---|---|---|---|
| 0.55 | 0.03 | 1.1038 | 6.94% | 1.2821 | -8.91% | yes | yes |
| 0.65 | 0.03 | 1.1040 | 8.22% | 1.2819 | -10.49% | yes | yes |
| 0.75 | 0.03 | 1.1043 | 9.51% | 1.2817 | -12.05% | no (tie) | yes |
| 0.85 | 0.03 | 1.1045 | 10.80% | 1.2814 | -13.61% | no | yes |
| 1.00 | 0.03 | 1.1047 | 12.74% | 1.2810 | -15.91% | no | yes |

Base OOS Sharpe 1.2817 (CAGR 9.51%, MaxDD -12.05%); SPY OOS Sharpe 0.8786 (CAGR 15.38%, MaxDD
-33.72%). Beats base 2/5, beats SPY 5/5. The IS pick is **band 0.03 — the live constant — at all
five gross levels**, and the IS Sharpe gap to the runner-up is 0.0197–0.0198, about **20× the
1e-3 bar**: no tolerance rung in this study changes a single rule-8 choice.

## What this says about PROTOCOL (proposed, NOT adopted — rule 6)

1. **A gate must name its unit.** 79.2% of the record's 520 clauses do not, so most of them cannot
   be restated in record units at all. This is the binding constraint, not the bar.
2. **Size the bar to the metric, and take `min(native, proposed)`.** |dSharpe| < 1e-3 is the right
   order (it recovers 3/3 of the Sharpe-constant claims); |dCAGR| < 1e-4 recovers 0/3 and should
   be ≥ 1e-2 to clear the observed restatement, at which point it barely tests anything.
3. **The restatement is a reporting fix, not a verdict fix.** It rescues 3 of 41 claims and flips
   0 non-self-comparison verdicts against 4a/4b margins whose medians are 0.0385 and 0.0222.
4. **Prefer a recomputed reference to a hand-copied constant.** Every gate that failed at a
   looser-than-1e-6 bar compares against a 3–4 decimal number typed into the source.
5. **8.8% of gates are structural and no tolerance reaches them** — those need idea 514's vintage
   stamp instead.

## Honest limits

The sample is 48 of 158 scripts (30%); 14 hit the 150 s timeout, so 28 of 199 static clauses in
the sample were never reached and are reported as UNREACHED. Unit classification is a regex over
the clause source and assert message, so the 79.2% "unknown" is an upper bound on ignorance, not
a proof that no unit exists — the 0.3898 outlier is a `c*` in bps that the classifier could not
see. The unit-specific bar results rest on n = 5 (Sharpe) and n = 3 (CAGR). Vintage is deliberately
**not** a third parameter (PROTOCOL caps at two), so the causal attribution is borrowed from idea
513 rather than re-established here. Part [D] uses the U56 panel only.
