# Idea 1211 (lane B, 2026-09-17) — is the RECORD's COUNT CUE the CLAIM's OWN COUNT?

**VERDICT: KILL (capital) / ANSWERED = NO, THE SCRIPT CANNOT CONVICT THE TEXT — and the one
direction that IS measurable clears it. Of 147 committed claims whose script is on disk with
artefacts, exactly 2 (0.0136) quote MORE units than their script's LARGEST table has rows: the
record essentially never INFLATES a count. Every mis-count the recovery finds points the other
way (R_NOUN 20 of 25 UNDER, 0 OVER), and a 16-line hand audit shows that undercount is the
RULE's error, not the record's — the script's artefact is the FULL grid where the claim
averages over a named sub-grid. Consequence: substituting K_SCRIPT for K_TEXT never removes a
resolution and only adds them (12→18, 70→75, 70→115), so 1210's 80 of 165 is a FLOOR.**

Script: `2026-09-17_is-the-RECORD-s-COUNT-CUE-the-CLAIM-s-OWN-COUNT_B.py`
(23 s, offline, deterministic). Gates **13 of 13 PASS**.

## The object, frozen

1210 recovered a pick count for 85.4% of committed OOS-Sharpe gap claims by taking the count
cue NEAREST the gap on the same line, and wrote the limit down itself: *"Where a line quotes
several counts, the nearest one may not be the claim's own."* This run takes **1210's own
committed adjudication artefact, all 165 rows, verbatim** — not a re-harvest — and re-recovers
K from the SCRIPT behind each row.

* The record **PREPENDS** rows, so 1210's stored line numbers are stale: **17 of 165 still
  match**. All **165 of 165 relocate** by exact text match (0 ambiguous), and **165 of 165**
  reproduce 1210's K from the relocated text (G2 = 0.000).
* Mapping (fixed rule): LEADERBOARD row → the last `*.py` token on the row; CHANGELOG line →
  the nearest `*.py` at or above it inside the same `##` section; memo/result → its own stem.
  **163 of 165 map; 148 have the script on disk**, over **107 distinct scripts**; **147** of
  those scripts emitted at least one `<stem>.<suffix>.csv`. The other **18 are UNMEASURABLE and
  are reported as such, never as mis-counts.**
* Today's re-harvest of C_STRICT gives 165 and of C_BROAD 196 — 1210's committed numbers
  exactly — so nothing in the headline turns on freezing the frame.

## THE FIRST FINDING IS ABOUT THE TEXT, NOT THE SCRIPTS

**94 of 165 committed count cues (0.5697) NAME NO UNIT AT ALL.** The record writes "N of M"
and moves on. The nouns that do appear: cells 27, picks 20, books 10, rungs 5, panels 4, arms
3, draws 1, claims 1. A count whose unit is unstated cannot be checked against anything — not
by this run, and not by a reader.

## The two dials, all 9 cells published

| rule | claim set | n | mapped | measurable | recovered | exact | OVER | UNDER | med K_t/K_s | p10 | p90 | in-supply |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **R_NOUN** | **C_STRICT** | **165** | **148** | **147** | **25** | **5** | **0** | **20** | **0.048** | 0.007 | 1.000 | **0.3333** |
| R_NEAREST | C_STRICT | 165 | 148 | 147 | 147 | 55 | 19 | 73 | 1.000 | 0.167 | 1.219 | 0.3333 |
| R_MAXART | C_STRICT | 165 | 148 | 147 | 147 | 7 | **2** | 138 | 0.026 | 0.001 | 0.421 | 0.3333 |
| R_NOUN | C_ADJ | 107 | 91 | 91 | 12 | 3 | 0 | 9 | 0.072 | 0.008 | 1.000 | 0.3271 |
| R_NEAREST | C_ADJ | 107 | 91 | 91 | 91 | 35 | 15 | 41 | 1.000 | 0.167 | 1.500 | 0.3271 |
| R_MAXART | C_ADJ | 107 | 91 | 91 | 91 | 4 | 2 | 85 | 0.029 | 0.000 | 0.500 | 0.3271 |
| R_NOUN | C_BROAD | 196 | 179 | 178 | 32 | 5 | 0 | 27 | 0.057 | 0.006 | 1.000 | 0.3316 |
| R_NEAREST | C_BROAD | 196 | 179 | 178 | 178 | 65 | 20 | 93 | 0.900 | 0.164 | 1.147 | 0.3316 |
| R_MAXART | C_BROAD | 196 | 179 | 178 | 178 | 9 | 2 | 167 | 0.028 | 0.001 | 0.408 | 0.3316 |

Headline cell (`R_NOUN` × `C_STRICT`) was declared before any artefact was read, as was the
trap: resolution is monotone in K and K enters as a SQUARE ROOT, so a count wrong by 12x moves
the bar by only 3.46x. **A small flip count is not evidence the counts are right**, which is
why the headline is the mis-count rate and its direction.

Rule-free containment, no referent assumed: **55 of 147 (0.3741)** quoted counts equal SOME
artefact row count of their own script; 92 do not.

## THE HAND AUDIT, AND WHY IT OVERTURNS THE 0.80 UNDERCOUNT SHARE

20 headline rows drawn at `random_state=1211` (16 distinct lines; 4 lines carry two gaps each)
were read against their source line AND their script's artefacts:

| reading | distinct lines |
|---|---|
| the TEXT's count is the claim's own; the script artefact is a SUPERSET (**rule** error) | 9 |
| both right (`…is-n_elig-the-variable…`, 195 books = `books.csv` 195 rows) | 1 |
| both wrong — the nearest cue is not the claim's own AND the artefact is not either | 3 |
| unverifiable from 1210's stored ±90-character snippet | 3 |

Worked example, checked end to end: `2026-09-06_monthly-drawdown-cost_cloud.py` claims *"plain
monthly is the IS pick in **14 of 16 cells**, worth +0.0000 OOS Sharpe."* Its `grid.csv` has
**96** rows = 2 panels × 4 books × 6 arms × 2 bps, and 2 panels × 4 books × 2 bps = **16** —
the claim's 16 cells are exactly a marginal of the 96-row table. The text is right; the
6x "undercount" is the recovery rule reading the wrong axis of the same table.

**So R_NOUN identifies the claim's own referent in 1 of 16 audited lines.** Read the 0.8000
undercount share as an UPPER BOUND on text error that is mostly rule error; read the **0 of 25
overcount** and **2 of 147 under R_MAXART** as the statistic that survives, because it needs no
referent: a claim that quotes more units than the script's biggest table has rows is wrong
whatever axis it meant. Two do. Neither is a KEEP-path claim.

On the 13 verifiable lines the TEXT's count is the claim's own in **10** — loosely consistent
with 1210's own "~0.90 precise" hand audit, a little below it, and never in the inflating
direction.

## The consequence (ARM D): substituting K_SCRIPT only ever ADDS resolutions

σ_d re-measured on this tape with 1210's construction inherited whole: **σ_CELL = 0.1176**
(216 paired picks, gated against 1210's committed 0.1176 at 1.4e-05), σ_FOLD = 0.3707.
1210's headline reproduces **exactly**: 80 of 165 resolved on K_TEXT, and row-for-row
identical to its own `resolved` column (G12 = 0.000).

| rule | n | resolved on K_TEXT | on K_SCRIPT | lost | gained |
|---|---|---|---|---|---|
| R_NOUN | 25 | 12 | **18** | **0** | 6 |
| R_NEAREST | 147 | 70 | 75 | 1 | 6 |
| R_MAXART | 147 | 70 | 115 | **0** | 45 |

At σ_FOLD: 7→13, 24→28, 24→91; lost 0 / 2 / 0. **Not one resolved claim becomes unresolved
under R_NOUN or R_MAXART.** The count cue never makes a claim look BETTER resolved than its
script supports, so 1210's 80 of 165 is a floor on that axis — while its three OTHER
generosities (iid picks, clustered/iid ratio 1.39, σ_CELL over σ_FOLD) all still push the
other way and are untouched here.

## PROTOCOL rule 8 (the dial chosen on the pre-split claims, the rest read ONCE)

The census has no tradable parameter, so the dial is walked forward on the record's own dates:
claims dated ≤ 2026-09-10 choose the recovery rule, claims after are read once. 150 of 165
rows carry a date; IS 114, OOS 36.

| rule | window | n | exact | share | over | under |
|---|---|---|---|---|---|---|
| R_NOUN | IS | 21 | 2 | 0.0952 | 0 | 19 |
| R_NOUN | OOS | 4 | 3 | 0.7500 | 0 | 1 |
| R_NEAREST | IS | 111 | 36 | 0.3243 | 16 | 59 |
| **R_NEAREST** | **OOS** | **36** | **19** | **0.5278** | **3** | **14** |
| R_MAXART | IS | 111 | 6 | 0.0541 | 2 | 103 |
| R_MAXART | OOS | 36 | 1 | 0.0278 | 0 | 35 |

IS picks R_NEAREST (0.3243); read once out of sample it agrees on **19 of 36 (0.5278)**, over 3,
under 14 — the direction holds out of sample and the level rises, because newer rows quote
counts closer to a table the script actually wrote. R_NOUN's OOS cell is 4 rows and is
reported, not relied on.

The tape-side rule 8 (1210's choosers, picks on 2009–2016 alone, 2017–2026 read once):

| who | n picks | OOS CAGR | OOS Sharpe | OOS MaxDD |
|---|---|---|---|---|
| CH_ISCAGR | 24 | 11.81% | 0.7866 | −26.21% |
| CH_ISSHARPE | 24 | 11.61% | 0.7963 | −25.59% |
| CH_ISDD | 24 | 9.56% | 0.8157 | −21.85% |
| RULES v2 (live) U56 / B136 / SMALL | — | 9.42% / 7.88% / 3.75% | 1.2714 / 1.1059 / 0.5600 | −12.05% / −12.24% / −13.89% |
| SPY (U56 / B136 / SMALL days) | — | 15.15% / 15.33% / 15.33% | 0.8684 / 0.8767 / 0.8767 | −33.72% |

Every chooser loses to the live book on OOS Sharpe and to SPY on OOS CAGR — unchanged from
1210, reproduced here as a cross-run check.

## Both KEEP paths (rule 4) on the 144 distinct books this run built

4a **0 of 144**. 4b FULL 20, 4b OOS 24, **4b FULL and OOS 19 of 144** (U56 14/48, B136 5/48,
SMALL 0/48). These are 1101's rung books, **PRIOR ART** — recorded, not promoted, no memo, no
RULES change. A count census cannot pass a KEEP path on its own.

## Gates, 13 of 13

G0 frame is 165 · G1 all 165 relocate · G2 1210's K reproduces (0.000) · G3 record is
append-only · G4 fast runner ≡ `engine.backtest` 1.39e-17 · G5 1101's U56 anchor-A triple
1.62e-03 · G6 live RULES v2 MaxDD 4.95e-05 · G7 SPY OOS triple 2.89e-03 · G8 harvest
deterministic 0.000 · G9 σ_CELL ≡ 1210's 0.1176 at 1.43e-05 · G10 chooser-vs-itself EXACTLY 0 ·
G11 80-of-165 reproduces · G12 row-level agreement with 1210's `resolved` column 0.000.

## Limits, stated

1. **The recovery rule is the weak leg, and the audit says so.** A script's artefact is a table
   at the granularity the script chose to dump, not at the granularity a sentence averages
   over; R_NOUN hits the claim's own referent in 1 of 16 audited lines. Every UNDER count here
   is therefore contaminated. Only the OVER direction (2 of 147 under R_MAXART) and the
   containment rate (55 of 147) are referent-free.
2. **57% of the cues name no unit**, so for most committed counts there is nothing to match
   against by any rule, and this run imputes nothing.
3. 18 of 165 claims belong to scripts that dumped no CSV — UNMEASURABLE, excluded, not counted
   as mis-counts.
4. σ_d is 1210's, measured between its three honest choosers on 1101's four ladders; a more
   heterogeneous pair carries a larger SD, which would resolve FEWER claims, not more.
5. Rule 9 survivorship: U56, B136 and SMALL are current-constituent lists; SMALL drops the 52
   of 715 names with max_1d_move ≥ 1.0 (663 names, starts 2010). Every level is optimistic.
