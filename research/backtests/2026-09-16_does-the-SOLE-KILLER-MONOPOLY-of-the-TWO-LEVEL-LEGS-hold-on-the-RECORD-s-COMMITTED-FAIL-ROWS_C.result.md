# Idea 1010 (lane C, 2026-09-16) — does the SOLE-KILLER MONOPOLY of the two LEVEL legs hold on the RECORD's committed FAIL rows?

**ANSWERED = NO on the monopoly, YES on the near-monopoly. Verdict: KILL of 1007's "0 of 30" as a
claim about the record; its positive half survives at 0.9719.**

## The question
Idea 1007 found `L1_H1`, `L2_H2` and `L3_OOS` are the SOLE binding leg in **0 of 30** null cells
while `L5_CAGR` (7) and `L4_DD` (5) take all of them. This run asks the same question of the
RECORD: **883,294 committed 4b FAIL rows** across **449 committed CSVs** carrying a `fail4b`
column (995,062 rows read, ~247 MB), plus this run's own 60-cell priced grid.

## The answer
The Sharpe legs **do** decide a 4b verdict alone, **9,180 times**:

| sole binder | rows | share of all FAIL rows | share of all sole-binder rows |
|---|---|---|---|
| `L1_H1`   |   6,453 | 0.00731 | 0.01973 |
| `L2_H2`   |   2,612 | 0.00296 | 0.00798 |
| `L3_OOS`  |     115 | 0.00013 | 0.00035 |
| **SHARPE pooled** | **9,180** | **0.01039** | **0.02806** |
| `L4_DD`   | 153,477 | 0.17376 | 0.46910 |
| `L5_CAGR` | 164,467 | 0.18620 | 0.50277 |
| **LEVEL pooled**  | **317,944** | **0.35995** | **0.97194** |

(327,124 of the 883,294 FAIL rows have a sole binder at all; the other 556,170 die on two or
more legs at once.)

So 1007's **0 of 30** is a property of its 30-cell grid, not of the record. What IS a record-wide
fact is the **near**-monopoly: the two level legs take **97.19%** of every sole-binder row.
The one leg for which 1007's monopoly essentially holds is `L3_OOS` — sole on **115 of 883,294**
rows (0.013%), i.e. the OOS Sharpe leg has, in the whole committed record, decided a 4b verdict
by itself 115 times.

## The 12 cells (2 tuned axes, all reported, none selected)

| claim set | defn | n | sole_any | sole_SHARPE | sole_LEVEL | top leg |
|---|---|---|---|---|---|---|
| ALLROWS  | STRICT | 883,294 | 0.3703 | **0.0104** | 0.3599 | `L5_CAGR` |
| ALLROWS  | FAMILY | 883,294 | 0.3738 | 0.0139 | 0.3599 | `L5_CAGR` |
| ALLROWS  | RECOMP | 107,705 | 0.5668 | 0.0060 | 0.5608 | `L4_DD` |
| REALROWS | STRICT | 651,409 | 0.3355 | **0.0121** | 0.3234 | `L5_CAGR` |
| REALROWS | FAMILY | 651,409 | 0.3398 | 0.0164 | 0.3234 | `L5_CAGR` |
| REALROWS | RECOMP |   2,714 | 0.5586 | 0.0232 | 0.5354 | `L5_CAGR` |
| FILEWT   | STRICT |     436 | 0.4423 | **0.0311** | 0.4112 | `L4_DD` |
| FILEWT   | FAMILY |     436 | 0.4486 | 0.0374 | 0.4112 | `L4_DD` |
| FILEWT   | RECOMP |      13 | 0.6059 | 0.0220 | 0.5839 | `L4_DD` |
| FRESH    | STRICT |      39 | 0.7949 | **0.0513** | 0.7436 | `L4_DD` |
| FRESH    | FAMILY |      39 | 0.8205 | 0.0769 | 0.7436 | `L4_DD` |
| FRESH    | RECOMP |      39 | 0.7949 | 0.0513 | 0.7436 | `L4_DD` |

The SHARPE sole share **rises monotonically with how much the weighting resists the record's
large grid dumps**: 0.0104 row-weighted → 0.0311 file-weighted → 0.0513 on a freshly priced grid.
The row-weighted headline is the *most* favourable reading 1007's claim can get.

## Pre-registered bars: 3 of 7 PASS
| bar | observed | pre-registered | |
|---|---|---|---|
| H_MONO   | 0.0104 | < 0.010 | **FAIL** |
| H_MONO_R | 0.0121 | < 0.010 | **FAIL** |
| H_FAMILY | 0.0139 | < 0.050 | PASS |
| H_TAKE   | 0.9719 | ≥ 0.90  | PASS |
| H_STABLE | ALLROWS `L5_CAGR` / REALROWS `L5_CAGR` / FILEWT `L4_DD` / FRESH `L4_DD` | one leg | **FAIL** |
| H_FRESH  | top `L4_DD`, SHARPE 0.0513 | top `L5_CAGR`, same side of 0.01 | **FAIL** |
| H_RULE8  | 1 of 18 | ≥ 1 | PASS |

**H_STABLE's failure is a finding, not noise:** *which* level leg holds the sole-binder crown is a
weighting artefact — `L5_CAGR` row-weighted, `L4_DD` file-weighted and on fresh prices. Only the
*family* answer (LEVEL over SHARPE) is stable.

## Gates: 6 of 8 PASS — and both failures are facts about the record
* **G0 FAIL** — 235 of 995,062 rows (0.00024) carry a `fail4b` value that is not a binding set:
  a few files write an aggregate COUNTER dict (`{'DD': 44, 'CAGR': 4}`) or prose
  (`no IS-admissible point`) into the column. All 235 are **excluded** from every claim set, none
  guessed at.
* **G1 FAIL** — **83 of 310,256** rows carry a committed `pass4b` that its own `fail4b` contradicts.
  Localised: **80 rows in `2026-09-07_amihud-illiquidity-premium_cloud_grid.csv`** and **3 in
  `2026-09-11_how-much-of-the-record-s-CAND-vs-EWALL-premia-is-EXPOSURE_C.walkforward.csv`**.
* G2 PASS (0 of 121,905), G3 2.08e-17 / 4.44e-16, G4 0.0, G5 0.0, G6 0 leftover,
  G7 13 of 16 numeric files admitted at median fidelity 1.0000.

## PROTOCOL rule 8 — (book, cadence) chosen on 2009–2016 alone, OOS read once
2 panels × 3 IS-only choosers × 3 cost rungs = 18 picks. **OOS 4b 1 of 18, OOS 4a 0 of 18.**

The single 4b pass is `U56 C_ISLEGS → TOP20/M at 25 bps`: OOS **15.92% / 1.2325 / −19.60%**
against SPY OOS **15.21% / 0.8713 / −33.72%** and RULES v2 OOS **9.45% / 1.2765 / −12.05%**. It is
**the record's existing TOP20/M object reached from a fifth direction, not a new candidate**, it
appears at one cost rung only, and it **fails 4a** on drawdown (−19.60% vs the live book's
−12.05%). Every other pick binds `L4_DD`, alone, on all 17 — which is itself the run's own answer
reproduced on fresh prices.

## Survivorship (PROTOCOL rule 9)
U56 and B136 are current-constituent lists, so every CAGR and drawdown LEVEL in the price arm is
optimistic. That cuts in a known direction: survivorship lifts realised CAGR and compresses
drawdowns, making `L5_CAGR` and `L4_DD` **easier** to clear and a level-leg sole binder **harder**
to observe. The FRESH arm's SHARPE sole share of 0.0513 is therefore an **upper** bound and the
level-leg near-monopoly a **lower** bound. The record arm is a census of committed text and
inherits whatever bias its 449 source files carried.

## Verdict
**KILL** — for 1007's monopoly reading. No new book, no KEEP claimed, no memo, rule 6 untouched.
What 1007 may still say: the two level legs take 97.19% of sole-binder rows, and `L3_OOS` alone
decides a verdict 115 times in 883,294. What it may no longer say: that the Sharpe legs never
decide alone, or that the sole-binder crown belongs to a nameable one of the two level legs.
