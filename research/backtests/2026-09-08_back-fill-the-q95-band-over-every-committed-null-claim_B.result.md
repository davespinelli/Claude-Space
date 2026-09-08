# Idea 215 — back-fill-the-q95-band-over-every-committed-null-claim (lane B, 2026-09-08)

**Verdict: ANSWERED, and the idea's PREMISE IS WRONG.** The record's exposure to "the statistic it
happened to pick" is **smaller than its exposure to the rotation seed it happened to draw**, and the
single largest lever in the whole clause is neither: it is the MAX band's **depth**.

Script: `2026-09-08_back-fill-the-q95-band-over-every-committed-null-claim_B.py` (914 s, deterministic).
No RULES change. `RULES.md`, `PROTOCOL.md`, `scan.py`, `bot.py`, `baseline.py` untouched.

---

## Corpus, and what the record could not supply

468 published `clears` verdicts were re-read:

| parent | corpus | per-draw nulls committed? | published clears |
|---|---|---|---|
| 186 the-null-column-for-instruments-that-are-not-keyed-tilts | 108 rows | YES, `grid.csv`, 20 draws | 17/108 |
| 191 the-on-share-column | 180 rows | YES, `grid.csv`, 20 draws | 27/180 |
| 192 does-a-harmful-instrument-clear-more-often… (corpus O) | 108 rows | YES, `repro_O.csv`, 20 draws | 17/108 |
| 201 the-margin-column-instead-of-two | 180 rows | **NO** — band summaries only | 34/180 |
| 181 does-a-null-column-change-any-published-verdict | 180 rows | n/a — **not a rotation null** | — |

**181 is out of scope on structure, not convenience.** Its null is a KEY SUBSTITUTION
(`kind == "nullkey"`, 4 substituted ranking keys per real row). The null population has exactly four
members, so `K=100` does not exist for it and a 95th percentile of four numbers interpolates between
the 3rd and 4th. Reported, not run.

**201 committed 10,800 null rows' worth of summaries and none of the rows**, so its verdicts are
carried as published and re-priced against this run's fresh draws rather than re-read from its own.

186 / 191 / 192's configurations are all subsets of 191's 90 configs × 2 cost rungs (186's 3
thresholds per family are a strict subset of 191's widened 5; 192's corpus O is 186's grid verbatim),
so **one fresh rotation grid re-prices every rotation-null claim in the record at once**.

## Reproduction gates (all before any new number)

- `[a][b][c]` fast_backtest vs `engine.backtest` 1.4e-17 … 2.8e-17; cost identity; base weights 0.0 — 3 panels.
- `[e]` **idea 186's bands re-read from its own 2,160 committed null rows: max|d| = 0.000e+00 over 108 configs.**
- `[f]` **idea 191's bands re-read from its own 3,600 committed null rows: max|d| = 0.000e+00 over 180 configs.**
- `[g]` idea 192's corpus O vs idea 186's draws (both fixed seed 186_400): **2.082e-16**. Against
  idea 191's draws the same 12 configs differ by **7.361e-02** — because 191's seed was
  `SEED + hash(...) % 10000` and Python salts `hash()` per process. The seed leg is visible inside
  the reproduction gate itself.
- `[d]/[j]` **Price-revision drift, disclosed not hidden:** `data/prices.csv` has the same last bar
  (2026-09-04) the parents saw but has been rewritten by the daily Actions job since, so RULES v1's
  u56 Sharpe reads 0.66471 against the published 0.66418 (+5.3e-04) and the fresh real rows sit
  5.0e-03 from 191's published `dSharpe`. Rather than pick a threshold that passes, this is turned
  into a verdict count of its own:
- **LEG 2b, PRICE leg isolated: 0/180 published verdicts move on the price revision alone.**
  Idea 216 priced the same re-commit independently and found all 360 of its KEEP verdicts unchanged.
  Every movement count below is therefore seed/statistic/depth, not price noise.

## The decomposition

The idea asks about one leg. There are four, and they are not the same size.

| leg | what varies | movement |
|---|---|---|
| **PRICE** | revised `prices.csv`, all else published | **0/180 (0.0%)** |
| **SEED** | same statistic (MAX), same depth (K=20), different draws | **25/180 (13.9%)** — 191 vs 201 |
| **STAT** | MAX → Q95 on the *same* committed draws, K=20 | 13/108 (186), 24/180 (191), **all F→T** |
| **DEPTH** | K=20 → 100 at fixed statistic | MAX clear rate 16.7% → **3.9%** |
| **TOTAL** | published MAX@K=20 → Q95@K=100 | **39/468 (8.3%)**, 34 F→T, 5 T→F |

**Ideas 191 and 201 read the same 180 configurations with the same statistic at the same depth and
disagree on 25 of them (13.9%), 16 False→True and 9 True→False.** Measured from inside this run, five
disjoint 20-draw blocks disagree on 43/180 (23.9%), block clear counts 30/36/31/39/20 — the published
13.9% sits inside that. 186 (fixed seed) vs 191 (salted seed) disagree on 5/108 (4.6%).

**So the answer to idea 215 as posed is 8.3%, and that number is smaller than the 13.9% the record
already carries from a choice nobody records.**

## The (stat, K) grid — all six points

| stat | K | nominal size | mean band | median band | mean margin | clears | clear rate | clearsDD | clears_IS |
|---|---|---|---|---|---|---|---|---|---|
| MAX | 20 | 0.0476 | 0.1636 | 0.1176 | −0.0644 | 30 | 16.7% | 23 | 39 |
| MAX | 50 | 0.0196 | 0.1781 | 0.1298 | −0.0789 | 25 | 13.9% | 17 | 10 |
| MAX | 100 | 0.0099 | 0.2466 | 0.1948 | −0.1475 | **7** | **3.9%** | 4 | 9 |
| Q95 | 20 | 0.05 | 0.1416 | 0.1026 | −0.0424 | 46 | 25.6% | 35 | 52 |
| Q95 | 50 | 0.05 | 0.1436 | 0.1082 | −0.0444 | 39 | 21.7% | 37 | 27 |
| Q95 | 100 | 0.05 | 0.1449 | 0.1116 | −0.0458 | **41** | 22.8% | 31 | 18 |

MAX band K=20→100: **+50.8%**, clear rate 16.7% → 3.9%. Q95 band: **+2.4%**, 25.6% → 22.8%.
This corroborates idea 207 from an independent draw set: its published Q95@100 count of **41/180
reproduces exactly**; its MAX@20 count of 28/180 reads 30/180 here, and that 2-verdict gap is the
seed leg again.

**The destructive point is MAX@K=100, and it is destructive in one direction.** Read against it,
201's 34 published clears collapse to 7 — **27/180 verdicts move and every single one is True→False**
(186: 12 of 13 T→F; 191: 20 of 20 T→F). A statistic whose size falls as 1/(K+1) does not become more
reliable with more draws; it becomes strictly harder to clear. Q95 at the same depth moves 39/468
in the *opposite* direction (34 F→T).

## Rule 8 (PROTOCOL clause 8) — 18 cells, picks on ≤2016-12-31, read once on 2017→

| selector | mean OOS Sharpe | mean OOS CAGR | mean OOS MaxDD | dOOS | t | wins | losses | abstains |
|---|---|---|---|---|---|---|---|---|
| ORACLE-OOS | +0.8197 | +11.04% | −23.16% | **+0.0431** | **+3.86** | 12 | 0 | 0 |
| S0 do-nothing | +0.7766 | +10.22% | −23.53% | 0 | — | — | — | 0 |
| S-gated MAX@K=20 | +0.7590 | +9.92% | −24.20% | −0.0176 | −1.62 | 3 | 7 | 8 |
| S-gated Q95@K=100 | +0.7471 | +9.73% | −24.32% | −0.0295 | −2.35 | 0 | 6 | 12 |
| S1 IS-argmax, ungated | +0.7405 | +9.55% | −25.52% | −0.0361 | −1.68 | 5 | 9 | 0 |
| S-gated MAX@K=100 | +0.7383 | +9.75% | −23.98% | −0.0383 | −1.50 | 0 | 5 | 13 |
| S-gated Q95@K=20 | +0.7275 | +9.45% | −25.54% | −0.0491 | −3.49 | 0 | 10 | 8 |

**All four clause-gated arms lose to doing nothing, and so does the ungated IS argmax — while
ORACLE-OOS is +0.0431 (t +3.86, 12/18 wins).** Headroom exists in this family and no band finds any
of it. This is the fifteenth such instance by the record's running count. Swapping the gate
MAX@20 → Q95@100 changes **10/18** picks for a mean dOOS of **−0.0119**: the statistic is decision-
relevant and decision-useless at the same time. `S0 = 0.7766` reproduces idea 216's published S0 exactly.

Benchmarks over the same OOS window: **SPY 15.45% / 0.8820 / −33.72%**; RULES v1 @10bps on u56
7.73% / 0.7471 / −13.83%. S0 loses to SPY by −0.105 of Sharpe.

Full sample and halves: U56 base book @10bps **12.86% / 1.1075 / −18.21%, H1 1.1097 / H2 1.1117**;
SPY 15.23% / 0.8890 / −33.72% (H1 0.9566 / H2 0.8340); RULES v1 6.46% / 0.6647 / −13.83%.

## KEEP paths (both evaluated, on all 180 real rows)

**4a 37/180, 4b 28/180, BOTH PATHS 2/180 — identical to idea 216's independently published counts.**
4b passes are 27 U56 and 1 BROAD136; SMALL439 is **0/60**, the fourteenth reproduction of idea 136.

The two BOTH rows are the same pair idea 216 found and are **not candidates**:

| panel | arm | CAGR | Sharpe | MaxDD | H1 / H2 | OOS Sharpe | OOS CAGR | OOS MaxDD |
|---|---|---|---|---|---|---|---|---|
| U56 | SLEEVE ma200 / depth 1.0 @10bps | 11.83% | 1.0663 | −13.49% | 0.9752 / 1.1507 | 1.2192 | 14.20% | −11.95% |
| BROAD136 | SLEEVE ma200 / depth 0.5 @10bps | 12.13% | 0.9684 | −16.01% | 1.1157 / 0.8415 | 0.9284 | 12.04% | −16.01% |

Idea 216 showed both fail their own exact permutation null (824/974 and 697/974 rotations at least
as extreme). Nothing is promoted here; this run proposes no book. **A verdict about a band is not a
trading rule.**

## Pre-registered predictions — 4 of 6 hit

- **HIT** P1 — T→F is 0 in LEG 1 over 288 rows (arithmetic: Q95 ≤ MAX at fixed draws).
- **HIT** P2 — MAX +50.8%, Q95 +2.4% across K.
- **MISS** P3 — published→Q95@100 movement **8.2%** vs seed floor 13.9%. *This miss is the finding.*
- **HIT** P4 — price 0/180 (0.0%) vs seed 25/180 (13.9%).
- **HIT** P5 — best gated dOOS −0.0176.
- **MISS** P6 — 10/18 picks changed, not ≤6.

## Recommendation (proposed only; PROTOCOL untouched)

1. **The clause's biggest exposure is not its statistic — it is its unrecorded seed.** Any clause-11b
   rewrite that fixes the statistic and leaves the seed unpublished buys 8.3% of stability while
   leaving 13.9% on the table. **Publish the seed and the draw set with every band**, as idea 186 did
   and idea 191 did not.
2. **Drop MAX outright, and not because Q95 clears more.** MAX@K=100 moves 27/180 of 201's published
   verdicts and *all 27* are True→False: its size shrinks as 1/(K+1), so more draws make a published
   clear less likely rather than better founded. Idea 216 reached the same conclusion from the
   size side.
3. **Q95's K is a floor, not an optimum** — bands move 2.4% across 20→100, so 100 is a cost point,
   not an argmax. Consistent with idea 216's memo.
4. **Do not read `clears` as a decision rule.** All four gated arms lose to doing nothing OOS while
   ORACLE-OOS is +0.0431 (t +3.86). Whatever the band is for, it is not selection.
5. **Idea 181's key-substitution null needs its own clause**, or an explicit exemption: with a
   4-member null population, no draw-count clause applies to it at all.

## Known limits (stated, not worked around)

- Only J−1 distinct rotations exist and neighbouring offsets are correlated, so 100 draws are not 100
  independent samples. The Q95 of a correlated sample has no guaranteed nominal size — that is
  idea 214's open question. This run measures **realised verdict movement** and claims nothing
  about size.
- A rotation moves an overlay's episodes but cannot move the sample's crises; the whole family is a
  weak null and widening or narrowing the band does not fix that.
- SMALL439 is current constituents only (survivorship). Real and rotated draws inherit the bias
  identically, so the clause reading is comparative and the level is not.
- 201's per-draw nulls are not committed, so its 34 clears are re-priced against this run's draws,
  not re-read from its own.

Artifacts: `.console.txt`, `.real.csv` (180), `.draws.csv` (18,000), `.grid.csv` (6 points),
`.moves.csv` (12 rows), `.walkforward.csv`, `.keeppaths.csv`, `.benchmarks.csv`.
