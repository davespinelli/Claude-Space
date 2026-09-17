# Idea 1213 — do the RECORD's OTHER COUNT-CORRECTIONS STATE THEIR OWN DOMAIN?

**Answer: NO — 40 of 2,994 committed correction invocations (0.0134) state their own domain,
and the one place on price where a count correction is actually LOAD-BEARING is exactly the
place where it is OUT of its domain.** Verdict **KILL (capital)**: no new book, no new
candidate, no RULES change. Run 2026-09-17, cloud lane, idea 1 of 2.

Script: `2026-09-17_do-the-RECORD-s-OTHER-COUNT-CORRECTIONS-STATE-THEIR-OWN-DOMAIN_cloud.py`.
RULES.md, PROTOCOL.md, engine.py, scan.py, bot.py and baseline.py untouched.

## The two dials and no more (PROTOCOL rule 4; the queue names both)

`CORRECTION SET` {C_D2, C_COUNT, C_ALL} × `DOMAIN RULE` {R_TABULATED, R_STATED, R_LOOSE}
= **9 cells, every one published** (`.census.csv`, `.cells.csv`).
NOT dials, reported at every value: PANEL {U56, B136, SMALL}; the four ladders
LAD_N6 (k=6) / LAD_N14 (k=14) / LAD_G8 (k=8) / LAD_G16 (k=16); the six correction families;
the 4a and 4b legs; the rule-8 split. 10 bps, t+1 execution, weekly, 260-row warm-up.

## (0) The arithmetic, printed before any text or any price was read

d2(k) is tabulated for k = 2..12. The record's habit above 12 is to **clip at d2(12) = 3.258**.
Clipping makes the correction **constant in k**, so for two ladders both longer than 12 rungs the
count correction contributes **exactly 1.000000** to their ratio and cannot order them. Gate G0
returns True and `d2(14)/d2(16)` clipped = 1.000000. This is arithmetic, not a finding.

## (A) The census — six correction families, 104,556 units, 2,994 invocations

Corpus: 7,203 LEADERBOARD rows + every committed markdown paragraph under `research/`
(2,630 distinct files). Unit definition and the count-cue harvest are **inherited whole from
1155/1207** so the numbers are like-for-like, including the harvest's own noise (max harvested
k = 272,832 — a leaderboard row quoting several counts, 1211's open complaint, not repaired here).

| family | domain (from its own definition) | n | states domain | share | in-domain (tabulated) | out-of-domain carrying a verdict |
|---|---|---|---|---|---|---|
| D2 | k ∈ [2,12] Hartley table | 279 | 17 | **0.0609** | 0.1720 | 67 |
| SUBSAMPLE | matched m ≥ 1, both sizes stated | 452 | 4 | **0.0088** | 0.5066 | 101 |
| SE_SQRTN | n ≥ 2 exchangeable draws | 13 | 2 | 0.1538 | 0.4615 | 2 |
| BLOCK_L | 1 ≤ L ≤ T/2 (→ L ≤ 2099 here) | 446 | 5 | **0.0112** | 0.5000 | 90 |
| MULTTEST | m ≥ 2 tests, m stated | 13 | 2 | 0.1538 | 0.9231 | 0 |
| ANNUAL | p periods/yr stated | 1,791 | 10 | **0.0056** | 0.3412 | 323 |

**The 9 cells** (`.census.csv`): the share stating its own domain runs 0.0609 (C_D2) /
0.0309 (C_COUNT) / **0.0134 (C_ALL)** — it *falls* as the correction set widens, i.e. d2 is the
record's **best-documented** correction and it still states its domain 6% of the time.
Out-of-domain share under R_TABULATED runs 0.8280 / 0.6196 / 0.6229; under R_STATED
0.9391 / 0.9691 / 0.9866; under R_LOOSE 0.5233 / 0.5054 / 0.5919. Between 0.21 and 0.43 of
out-of-domain units carry a verdict token (583 units under C_ALL / R_TABULATED).

**1207's 0.8125 generalises.** Its finding was about 1155's 96 checkable units; across the whole
record d2's out-of-domain share reads **0.8280**, and the same pathology is present in every other
family at 0.49–0.66.

## (B) The price leg — rule 8, both KEEP paths, 108 decisions

Book construction frozen at the 2026-09-04 KEEP-4b candidate's (composite 12-1 + 6m + 3m
percentile ranks, **no vol scaler**, above-own-200d-MA eligibility, top-N equal weight at g/N,
gated-out weight to CASH). Chooser: if the ladder's IS-Sharpe **range** clears the bar the
correction set builds from the per-rung block-bootstrap SE (**L = 63, stated**, B = 400, seed 1213),
take the IS argmax rung; otherwise stay at the anchor (N = 20, g = 0.75). Chosen on 2009–2016,
2017–2026 read **once**.

Benchmarks (`.benchmarks.csv`): U56 SPY 15.06% / 0.8814 / −33.72% (halves 0.9598/0.8170),
OOS 15.15% / 0.8684; U56 RULES v2 LIVE 8.60% / 1.1980 / −12.05%, OOS 1.2714.
B136 SPY 15.16% / 0.8861 / −33.72%, OOS 0.8767; B136 LIVE 7.98% / 1.0993, OOS 1.1059.
SMALL SPY 14.06% / 0.8581 / −33.72%, OOS 0.8767; SMALL LIVE 4.30% / 0.6637 / −13.89%, OOS 0.5600.

**Every one of the 108 decisions stays at the anchor.** All nine cells are identical:
mean OOS Sharpe 0.9339, mean OOS CAGR 14.96%, worst OOS MaxDD −30.49%, **0 clear 4a, 4 of 12
clear 4b per cell (36 of 108)** — and all 36 are the **U56 anchor**, i.e. the standing
2026-09-04 incumbent (14.18% / 1.1410 / −19.39%, halves 1.2223/1.0883, **OOS 15.55% / 1.1595**).
**CONFIRMATORY, NOT GENERATIVE. No new candidate, no memo, nothing enacted.**

### The control that makes the 9 cells readable

Running the same gate with **no correction at all** (`.control_nocorrection.csv`) is what turns a
null result into an answer:

| panel | ladder | k | range/SE | bare gate | clipped-d2 gate | tabulated-d2 gate | load-bearing |
|---|---|---|---|---|---|---|---|
| U56 | LAD_N6 | 6 | 0.7856 | False | False | False | no |
| **U56** | **LAD_N14** | **14** | **1.0520** | **True** | **False** | **undefined** | **YES** |
| U56 | LAD_G8 | 8 | 0.0012 | False | False | False | no |
| U56 | LAD_G16 | 16 | 0.0014 | False | False | undefined | no |
| B136 | LAD_N6 | 6 | 0.5229 | False | False | False | no |
| B136 | LAD_N14 | 14 | 0.5693 | False | False | undefined | no |
| B136 | LAD_G8 | 8 | 0.0278 | False | False | False | no |
| B136 | LAD_G16 | 16 | 0.0300 | False | False | undefined | no |
| SMALL | LAD_N6 | 6 | 0.9712 | False | False | False | no |
| **SMALL** | **LAD_N14** | **14** | **2.0122** | **True** | **False** | **undefined** | **YES** |
| SMALL | LAD_G8 | 8 | 0.0148 | False | False | False | no |
| SMALL | LAD_G16 | 16 | 0.0161 | False | False | undefined | no |

**The correction is load-bearing at 2 of 12 (panel, ladder) families, and BOTH of them are the
k = 14 ladders — exactly where d2 has no tabulated value.** At both, the bare range clears its own
SE (1.0520 and 2.0122) and the clipped constant 3.258 switches the gate **off**. So the only two
places on this tape where a count correction decides anything, it decides it with **a number that
is not d2(14)** — it is d2(12) wearing d2(14)'s name. Under R_TABULATED the same two cells are
`applied = False` and the chooser declines for the opposite reason, and lands on the same book.

The gross ladders are not adjudicable at all: range/SE runs 0.0012–0.0300 because IS Sharpe is
flat in gross (1189's finding, reproduced here at four decimals). Eight of twelve families sit
below half their bare SE, so on those the domain question **cannot be settled on price** — the
ladder fails with or without any correction.

## Caveats

Survivorship: `universe.json` / `universe_broad.json` are current constituents; the small panel is
the current output of a sub-$2B screen. The committed `small_meta.csv` carries **715** rows here,
of which 52 are dropped for `max_1d_move ≥ 1.0`, leaving **663** tradable — the label `SMALL439`
does not denote this pool (idea 1074 is still open on the rename). The census's count harvest is
1155/1207's and inherits its noise; the in-domain/out-of-domain shares are therefore an upper bound
on how well the record documents itself, not a lower one. `states_domain` is scored at the UNIT
level, so a domain token anywhere in a long paragraph counts — again generous to the record.

## What this closes and what it opens

Closes 1213: **no correction family in this record states its own domain at a rate above 0.16,
and the two ladders where a correction changes a gate are both out of the domain it is quoted
from.** Opens: the fix is cheap and mechanical — a correction should refuse rather than clip, which
is `R_TABULATED`, and on this tape it costs nothing (same 108 books, same 36 4b passes) because
the anchor was already the answer.
