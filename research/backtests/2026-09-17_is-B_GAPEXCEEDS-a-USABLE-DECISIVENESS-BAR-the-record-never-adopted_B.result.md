# Idea 1252 (lane B, 2026-09-17) — is B_GAPEXCEEDS a USABLE DECISIVENESS BAR the record never adopted?

**VERDICT: KILL (capital). NO NEW BOOK, NO MEMO, NO RULES CHANGE.** 4a 0 of 1026 rule-8 rows;
the 274 4b-BOTH rows collapse to 19 distinct realised books and NOT ONE is produced by either
bar — every one is a plain rung book or the anchor itself. Gates 9/10 (the one FAIL is a
reachability gate and is the finding, below).

Script: `2026-09-17_is-B_GAPEXCEEDS-a-USABLE-DECISIVENESS-BAR-the-record-never-adopted_B.py`
Dials (rule 4, exactly 2): BAR PERCENTILE {50, 75, 90, 95, 97.5, 99} x CLAIM SET {CS_ALL,
CS_SHARPE, CS_LARGE, CS_NODEG} = **24 cells, every one published** in `.dialgrid.csv`.
Frozen: 1208/1242's same 72 decisions (3 panels x 2 anchors x 4 ladders x 3 choosers), L = 63,
B = 1000, incumbent bar q = 0.90, 10 bps, LAG 1, IS end 2016-12-31.

## 1. The queue's premise is arithmetically right and materially misleading (premise audit)

The queue reads 1242 as "B_GAPEXCEEDS moves on only 12 of 72 decisions, the most stable
bar-side output measured". Reading 1242's committed `.outputs.csv` row by row (this run replays
it to **0.000e+00** on both P_boot and B_GAPEXCEEDS, gates G3/G4):

| L | 1 | 2 | 5 | 10 | 21 | 42 | **63** | 126 | 252 | 504 | 1008 | T |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| B_GAPEXCEEDS fires | 0 | 0 | 0 | 0 | 0 | 0 | **0** | 0 | 0 | 0 | 2 | 10 |
| P_boot >= 0.90 fires | 11 | 12 | 12 | 13 | 14 | 16 | **16** | 17 | 20 | 23 | 34 | 72 |

The "12" is the bar's **entire lifetime output over all 864 committed rows**, and **12 of 12 sit
at L = 1008 or L = T** — the two rungs where the moving-block resample is at or near the
IDENTITY and the draws stop being a null at all. At the record's own frozen L = 63, and at
every one of the ten rungs from L = 1 to L = 504, **B_GAPEXCEEDS FIRES ZERO TIMES**.

## 2. Why: the bar is structurally near-unreachable, before any tape is read (ARM 0)

It asks whether the OBSERVED top-minus-second margin of a k-rung ladder exceeds the 95th
percentile of the DRAWS' OWN top-minus-second gap. A resample of k correlated books produces a
max-minus-second spread dominated by sampling noise, systematically WIDER than the real ladder's
separation — so the bar requires a real ladder to be more separated than 95 of 100 pure-noise
ones. On **400 synthetic ladders it fires 0 times** (G0b FAIL, declared as a gate before
measuring): mean observed margin / draw-gap q95 = **0.2980**, and the observed margin sits at the
**41.6th percentile** of the draw-gap distribution on average. This is a property of the
statistic, not of this tape.

## 3. Its "perfect stability" is degeneracy, and inverts at any usable move rate (job 2)

9 rng streams, L = 63, same 72 decisions. GAPEX at 90/95/97.5/99 flips on **0 of 72** — it is
CONSTANT, which is why 1242 measured exactly zero seed swing. The only percentile at which it
licenses anything comparable to the incumbent is **p = 50** (18 of 72 vs the incumbent's 16 —
the MOVE-MATCHED rung), and there it flips on **10 of 72 decisions against the incumbent's 2**,
fire-count swing 3 vs 2. **The stability advantage is entirely an artefact of never firing.**

Fire counts across dial 1 on CS_ALL: **18 / 1 / 0 / 0 / 0 / 0** at p = 50 / 75 / 90 / 95 / 97.5 / 99.
Agreement with the incumbent 0.6944 at p = 50 (kappa **0.1538**), 0.7778 at p >= 90 (kappa 0.0000
— agreement by mutual silence, not by judgement).

## 4. Job 3 — INFORM: the only capital claim, and NEITHER bar has it (rule 8)

d = OOS Sharpe(pick book) − OOS Sharpe(anchor book), paired per decision, picks made on
warm-up..2016-12-31 only, 2017-2026 read ONCE. CS_ALL:

| bar | n_fire | mean d given FIRE | mean d given NO fire | difference | t |
|---|---|---|---|---|---|
| P_boot >= 0.90 (incumbent) | 16 | **−0.0061** | +0.0133 | **−0.0194** | −1.28 |
| GAPEX p=50 (move-matched) | 18 | +0.0111 | +0.0082 | +0.0029 | +0.33 |
| GAPEX p=95 (the record's) | **0** | n/a | +0.0090 | n/a | n/a |

**THE INCUMBENT BAR IS MILDLY ANTI-INFORMATIVE**: the decisions it licenses do WORSE out of
sample than the ones it refuses. Rank correlation between each bar's continuous score and the
OOS delta is NEGATIVE on both: −0.1423 (P_pick), −0.1201 (the observed margin's gap percentile
rank). Mean d over all 72 decisions is +0.0090, i.e. acting on the IS argmax is worth a little on
this tape and the bars do not find the decisions where it pays.

## 5. The money, all 12 selectors (CS_ALL, mean OOS Sharpe of each selector's realised book)

| selector | moved | mean OOS Sharpe | vs anchor | t | 4a | 4b BOTH |
|---|---|---|---|---|---|---|
| SEL_NEVER_anchor (do nothing) | 0 | 0.8268 | — | — | 0 | **24 of 72** |
| SEL_ALWAYS_pick | 58 | **0.8357** | +0.0090 | +0.66 | 0 | 6 |
| SEL_PBOOT090 (incumbent) | 13 | 0.8254 | **−0.0014** | −1.26 | 0 | 19 |
| SEL_GAPEX_50 = MATCHED | 16 | 0.8296 | +0.0028 | +0.34 | 0 | 19 |
| SEL_GAPEX_75 | 1 | 0.8276 | +0.0009 | +1.00 | 0 | 23 |
| SEL_GAPEX_90 / 95 / 97.5 / 99 | 0 | 0.8268 | +0.0000 | n/a | 0 | 24 |
| SEL_AND_both | 0 | 0.8268 | +0.0000 | n/a | 0 | 24 |
| SEL_OR_either | 13 | 0.8254 | −0.0014 | −1.26 | 0 | 19 |

H_BETTER is SUPPORTED but trivially: at the move-matched rung GAPEX buys **+0.0042** of mean OOS
Sharpe over the incumbent (0.8296 vs 0.8254), t +0.34 against the anchor, and on **CS_LARGE its
sign flips to −0.0068 (t −1.16)**. Both bars lose to simply ALWAYS acting (0.8357), and every
bar-gated selector converts passing anchor books into failing ones: 4b BOTH falls 24 -> 19 under
either bar and 24 -> 6 under always-acting. **GATING IS A DESTRUCTION OPERATOR HERE, NOT A FILTER.**

## 6. KEEP paths, both evaluated on every row (1026 rule-8 rows in `.walkforward.csv`)

- **4a: 0 of 1026.** Leg pass counts A_H1 532, A_H2 10, A_DD 21 — live RULES v2's -12.05% MaxDD
  is out of reach for every book in this family, as in every run since 2026-09-04.
- **4b: 274 of 1026 pass BOTH the full-sample and OOS legs, collapsing to 19 DISTINCT realised
  books** (269 of 274 on U56, 5 on B136). The best is U56 anchor B, N = 20, a **plain rung book**:
  full 11.03% / 1.1354 / -18.01%, OOS 12.42% / **1.1771** / -18.01% vs U56 SPY OOS 15.15% /
  0.8684 / -33.72%. The incumbent 2026-09-04 anchor replays at full 15.55% / 1.1381 / -19.13%
  (G1: 1.6e-03 from the committed 1.139701), OOS 16.92% / 1.1615 / -19.13%. **No bar produces a
  book that is not already in the record.**

## 7. Hypotheses (all declared in the script header before any tape was read)

- H_STINGY **SUPPORTED** — 0 of 72 vs 16 of 72.
- H_USABLE **REFUTED** — the bar licenses nothing at all at its own rung.
- H_STABLE **SUPPORTED but vacuous** — 0 flips because 0 fires; at p = 50 it is 5x LESS stable.
- H_INFORM **REFUTED** — no bar's licensed set has a positive OOS delta with t > 1; the
  incumbent's is negative.
- H_BETTER **SUPPORTED, inside noise** — +0.0042 of mean OOS Sharpe, sign-flipping by claim set.

## 8. What the record should take, in one sentence

**A DECISIVENESS BAR SHOULD BE PUBLISHED WITH ITS FIRE COUNT AT THE BLOCK LENGTH IT WILL BE USED
AT, AND WITH THE OOS DELTA OF THE DECISIONS IT LICENSES AGAINST THE ONES IT REFUSES — BECAUSE
B_GAPEXCEEDS' HEADLINE STABILITY IS A CONSTANT-ZERO FIRE COUNT AT EVERY HONEST L, AND THE
INCUMBENT P_boot >= 0.90, WHICH DOES FIRE, LICENSES THE WORSE HALF OF THE DECISIONS.** PROPOSED
for the Sunday review (rule 6) as a PROTOCOL reporting line only — never as a chooser: rule 8
shows every gating policy in this family is worth between −0.0014 and +0.0028 of mean OOS Sharpe
against doing nothing. RULES.md, scan.py, bot.py and baseline.py are untouched.

## 9. Survivorship (rule 9)

U56 and B136 are CURRENT-constituent lists; SMALL is the current constituents of a sub-$2B screen
(`data/SMALL_PANEL_README.md`). Every LEVEL here — CAGR, MaxDD, Sharpe, and every bootstrap built
on them — is optimistic, so the 4b counts are upper bounds. The headline is a CONTRAST between two
bars over the same 72 decisions on the same tape, first-order immune to a common level bias; the
4b legs are not.
