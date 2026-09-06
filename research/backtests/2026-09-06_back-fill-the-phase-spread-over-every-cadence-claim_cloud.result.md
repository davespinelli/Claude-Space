# Idea 220 — back-fill-the-phase-spread-over-every-cadence-claim (cloud, 2026-09-06)

**Verdict: KILL of the record's contested cadence verdicts. 155 of 240 published pairwise
cadence claims survive a phase audit, and the 85 that die are exactly the ones the project
argued about.** Not a KEEP-candidate; no book, no RULES change.

Script `research/backtests/2026-09-06_back-fill-the-phase-spread-over-every-cadence-claim_cloud.py`.
Artefacts: `.console.txt`, `.rows.csv` (7 750 unit × cadence × phase rows), `.claims.csv`
(240 re-priced verdicts), `.summary.csv`, `.walkforward.csv`, `.keep.csv`.

## What was done

Idea 187 showed that at a *fixed* cadence, shifting the block grid moves mean OOS Sharpe by
0.15–0.40 — 2.1–2.4× the published 6W-minus-W cadence effect. Every cadence number in the
record is a **phase-0** number. This run re-prices each published cadence verdict against its
own phase spread.

**Phase, generalised** (the one new piece of machinery, a strict superset of idea 187's):
`phase = (block shift, within-block day offset)` — the whole-sub-period shift of idea 187, plus
the trading day inside the block (rebalance on the *(last − off)*-th bar, `off ∈ {0..4}`).
Idea 187's phase is degenerate at D/W/M/Q, which is the ladder ideas 3/101/171/173 argue over;
the day offset is defined everywhere. **Phase (0,0) is the published convention bar for bar.**
Grid sizes: D 1 · 2D 2 · W 5 · 2W 10 · M 5 · 6W 30 · Q 5.

**Two tuned parameters** (PROTOCOL rule 4): CADENCE POINT (swept, all reported) × PHASE (swept,
all reported). Corpus, cell and metric are audit axes read from the committed parents.

**Corpora audited** — the four of the nine the idea names whose grid CSV survives:

| corpus | parent | shape | control [c] |
|---|---|---|---|
| A | ideas 175 + 188 | 115 books × 7 points | 805/805 rows, max\|d\| **2.220e-16** |
| B | idea 171 CADENCE dial | 53 books × D/W/M/Q | 212/212, **2.220e-16** |
| C | idea 173 CADENCE ladder | 18 cells × D/W/M/Q | 72/72, **4.441e-16** |
| D | idea 101 cadence bar | 8 cells × D/W/M | 24/24, **3.331e-16** |

**Not audited, with the reason stated rather than buried:** idea 3 (`2026-09-04_rebalance-freq_cloud`)
wrote no grid CSV — console + result.md only. Ideas 65, 107 and 182 are still OPEN in QUEUE.md:
never run, so there is no published verdict to audit. Idea 187 is this idea's parent, used as
control [d].

Controls: [a] `cad_mask(0,0) == engine.rebalance_mask` at D/W/M/Q (4/4). [b] cost linearity,
max\|d\| ≤ 1.4e-16 at four cadences. [c] above, **4/4 AUDITED**. [d] the new machinery reproduces
idea 187's committed `.phase.csv` at 6W on **690/690 rows, max\|d\| 2.220e-16**.

## The size of the correction

240 published pairwise cadence verdicts re-priced. Survival rule, pre-registered:
`sign(phase-averaged gap) == sign(phase-0 gap)` **and** `sign_share ≥ 0.95`.

| corpus | claims | SURVIVE | share | sign kept (weak) | median \|gap0\| | median phase range | median ratio |
|---|---|---|---|---|---|---|---|
| A | 84 | 39 | 46.4% | 78.6% | 0.0855 | 0.1702 | 0.486 |
| B | 24 | 18 | 75.0% | 91.7% | 0.1222 | 0.1475 | 1.018 |
| C | 108 | 78 | 72.2% | 92.6% | 0.1679 | 0.1403 | 1.179 |
| D | 24 | 20 | 83.3% | 100.0% | 0.1945 | 0.1274 | 2.151 |
| **ALL** | **240** | **155** | **64.6%** | **88.3%** | **0.1390** | **0.1465** | **0.967** |

**The median published cadence gap is the same size as its own phase range (ratio 0.967), and
128 of 240 gaps are smaller than it.** Survival is almost entirely a function of whether the
pair contains D — the one point with no phase freedom and a 10× turnover difference:

| pair family | n | survive | median ratio |
|---|---|---|---|
| involves D | 106 | 98 (**92.5%**) | 2.129 |
| involves 6W | 24 | 5 (**20.8%**) | 0.337 |
| neither | 114 | 54 (47.4%) | 0.632 |

| pair | n | survive | mean sign share | median \|gap0\| | median range |
|---|---|---|---|---|---|
| D–W | 34 | **34 (100%)** | 1.000 | 0.1729 | 0.0906 |
| W–M | 34 | 11 (32.4%) | 0.804 | 0.1284 | 0.2194 |
| W–6W | 4 | **0 (0%)** | 0.422 | 0.1300 | 0.4087 |
| M–6W | 4 | **0 (0%)** | 0.423 | 0.0842 | 0.4575 |
| W–Q / M–Q | 52 | 32 (61.5%) | 0.844 | ~0.13 | ~0.17 |

So the audit does not say "the record is 65% right". It says the record is right where the
answer was never in doubt (daily rebalancing is expensive) and wrong wherever a cadence
*constant* was being argued for.

## The headline claims, individually (corpus A)

| cell | pair | gap0 | phase-avg gap | sign share | phase range | survives |
|---|---|---|---|---|---|---|
| ALL | W–6W | −0.0999 | **+0.0153** | 32.7% | 0.2250 | no |
| ALL | M–6W | −0.0238 | **+0.0243** | 32.7% | 0.3065 | no |
| ALL | W–M | −0.0761 | −0.0090 | 52.0% | 0.1644 | no |
| U56 | W–6W | −0.1640 | **+0.0584** | 33.3% | 0.4998 | no |
| U56 | W–M | −0.0469 | **+0.0538** | 32.0% | 0.2283 | no |
| ETF | W–6W | −0.1600 | **+0.0586** | 39.3% | 0.4924 | no |
| ALL / U56 / ETF | W–Q, M–Q | +0.14 … +0.36 | same sign | **100%** | ≤0.24 | YES |

Five of the six "slower beats faster" claims that involve 6W or W-vs-M **reverse sign** under
phase averaging. Idea 175's whole geometric story is one of them.

**Idea 188's family split does not survive:** the argmax cadence per family flips on 2 of 3
families once the phase is averaged out — ETF 6W → M, U56 6W → **W** (the incumbent), SMALL M → M.

**Idea 101's cadence-insensitivity bar (idea 65) is unaffected**, because it already failed:
the D/W/M spread is 0.26–0.44 against a 0.05 bar at phase 0 in 8/8 cells, and including every
phase leaves the spread identical (D is the extreme and it has exactly one phase). The bar was
never close, phase or no phase.

## PROTOCOL rule 8 walk-forward (chose ≤ 2016-12-31; 2017-2026 read once)

| family | arm | mean OOS CAGR | mean OOS Sharpe | mean OOS MaxDD | vs CONST-W0 | t |
|---|---|---|---|---|---|---|
| ALL | CONST-W0 (incumbent) | 5.26% | 0.680 | −17.05% | — | — |
| ALL | **REC** (cadence by IS Sharpe **at phase 0** — what the record does) | 5.75% | 0.719 | −17.98% | **+0.0388** | **+3.26** |
| ALL | **SEL-CP** (cadence **and** phase by IS Sharpe) | 5.87% | 0.693 | −20.39% | +0.0134 | +0.83 |
| ALL | **PHASE-AVG** (cadence by IS Sharpe of the all-phase blend, traded as that blend) | 5.59% | 0.647 | −21.45% | **−0.0328** | **−2.11** |

References over the same OOS window: SPY 15.45% / 0.8820 / −33.72%; RULES v1 7.73% / 0.7471 /
−13.83% (U56) and 6.35% / 0.4920 / −36.12% (SMALL).

The REC row reproduces idea 175's published +0.0388 (t +3.26) exactly — and that is the finding:
**the record's cadence "skill" is worth +0.0388 only because it is measured at one arbitrary
phase.** Let the selector see the phase too and it collapses to +0.0134 (t +0.83, insignificant);
average the phase out honestly and it goes negative (−0.0328, t −2.11). By family, PHASE-AVG is
−0.1067 (t −5.30) on U56, −0.1002 (t −3.70) on ETF and +0.0623 (t +2.77) on SMALL.

## Both KEEP paths (corpus A, all 6 670 rows)

4a **1 260/6 670**, 4b **450/6 670** — every 4b pass is U56 (SMALL 0/2 842, ETF 0/1 914). Of the
450, only **59 are at phase 0** and **391 exist only off phase 0**. Best row: U56 @ 6W phase(5,4),
CAGR 14.88%, Sharpe 1.2146, MaxDD −18.16%, halves 1.116/1.306, OOS 17.88%/1.3652 — and it is
unreachable, because a phase is fixed by the sample start date and is not a tradable choice.
The phase-0 U56 @ M row (CAGR 14.76%, Sharpe 1.2081, OOS 16.71%/1.2866) is a re-cadencing of an
existing book (idea 144). **No KEEP-candidate.**

## Predictions and reading

The idea asked for "the size of the correction". It is: **85 of 240 published cadence verdicts
do not survive, and they are the contested 85.** Every verdict involving 6W (the record's most
recent cadence headline) dies at 20.8%; W-vs-M dies at 32.4%; D-vs-anything survives at 92.5%.
The one cadence statement the record can still make is *daily rebalancing is expensive and
quarterly is stale*. No cadence constant between W and Q is identified by this data.

**Proposed for Sunday review, report-only, no RULES change:** any future cadence claim must quote
the phase-averaged gap and the sign share beside the phase-0 gap, or state that the point has one
phase. Follow-ups already queued as ideas 221 and 222 are the right next steps — 222's
phase-averaged estimator is measured here and, on the large-cap families, it is *worse* than the
weekly incumbent, which 222 should be told before it starts.

### Caveats
* **Survivorship.** SMALL439/SMALL484/small, U56/u56, B136/broad and ETF36 are current-constituent
  lists (`data/SMALL_PANEL_README.md`, idea 54). No level here is an attainable return; the paired
  comparisons that carry the conclusion are unaffected.
* Corpus B reproduces idea 171 exactly, and idea 171's SMALL484 did **not** drop the
  `max_1d_move >= 1.0` tickers. Reproducing a committed parent requires its corpus; the standing
  drop rule is applied to every panel this run builds itself (A and C).
* Idea 38: `data/prices*.csv` are calendar-day indexed after 2014-09-17, so a 1-bar offset on the
  large-cap panels can land on a weekend (a no-op in weights). The large-cap phase spreads reported
  here are therefore a **lower** bound.
* 10 bps and t+1 execution throughout, except corpus C, which carries its parent's 10 and 25 bps.
