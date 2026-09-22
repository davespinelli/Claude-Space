# Idea 917 (lane cloud, 2026-09-22) — is the 20-day DDWIN definition floor a CRASH-LENGTH CONVENTION?

**Script:** `research/backtests/2026-09-22_ddwin-floor-convention_cloud.py`
**Artifacts:** `.population.csv` (144 rows), `.agree.csv` (3,168 rows — every proxy x population x
floor x excision x window), `.invariance.csv`, `.capital.csv` (27 rule-8 cells), `.ddwin_len.csv`,
`.ladder.csv`, `.gates.csv`, `.log.txt`.

## VERDICT — **ANSWERED: YES, AND THE ANSWER IS A KILL. NO committed DDSUB statistic is floor-invariant (0 of 11), the DDSUB population IS a crash-length artefact, and the floor is not even capital-neutral.**

## 1. THE FLOOR IS LITERALLY A CRASH-LENGTH CONVENTION (V1 YES)

Median DDWIN window length at the committed floor, excision NONE, window FULL:
**U56 24 days, B136 24 days** (SMALL 240 days). SPY's 2020 decline is 24 days. The books'
deepest declines *are* the crash, so a 20-day minimum sits one rung under the modal length and
a 40-day minimum sits above it. `|DDSUB|` of 112 real books, excision NONE / window FULL:

| panel | floor 10 | floor 20 (committed) | floor 40 | floor 60 |
|---|---|---|---|---|
| U56 | 112 (1.000) | **64 (0.571)** | 8 (0.071) | 4 (0.036) |
| B136 | 112 (1.000) | **60 (0.536)** | 12 (0.107) | 12 (0.107) |
| SMALL | 112 (1.000) | 112 (1.000) | 100 (0.893) | 72 (0.643) |

The share of 112 moves by more than 0.10 across the floor ladder on **23 of 36**
(panel x excision x window) cells — median spread 0.295, max **0.964**. Idea 912's committed
counts reproduce exactly (gate G3: 48 undefined on U56, 52 on B136). Excising 2020 by any of
SPYDD / CRASH / CAL20 restores all 112 at floor 20 (gate G4), so 912's "0 of 112 with it out"
reproduces as well. **DDSUB is a convention, not a population.**

## 2. NOT ONE COMMITTED DDSUB STATISTIC IS FLOOR-INVARIANT (V2 **NO**)

Spread of the DDSUB agreement across floors {10,20,40,60}; INVARIANT means spread ≤ 0.02
(867's own `MATCH_TOL`) on every cell where the statistic is defined at all four floors:

| proxy | invariant cells | worst spread | where |
|---|---|---|---|
| SEMI | 18 / 34 | 0.1000 | B136/NONE/FULL |
| EWMA | 17 / 34 | 0.1015 | B136/CAL20/IS |
| FULL, DOWN, TAIL10, HIVOL, SPYDD, SPYDD10 | 16 / 34 | 0.100–0.150 | B136 |
| ROLL | 15 / 34 | 0.1030 | B136/CAL20/IS |
| MAXROLL | 13 / 34 | **0.2667** | B136/NONE/FULL |
| DDWIN (the ceiling itself) | 19 / 34 | 0.0926 | B136/CAL20/IS |

**0 of 11 clear.** The best-behaved proxy still moves its agreement by 10 pp on some cell —
five times the record's own tolerance for "the same number". Ideas 867's K1/K2 and 910's K3/K4
headlines (agree 0.9531–1.0000 against a 0.95 bar) are quoted at a margin of 0.003–0.050, i.e.
**smaller than the floor effect on the same statistic**, so none of them is quotable without
naming its floor.

**IDENTIFICATION CONTROL.** On the ALL population the ten ex-ante proxies' agreement is exactly
floor-invariant (max spread **0.0e+00**) — the floor cannot reach them there. Every movement in
the DDSUB column is therefore the *population* moving, not the statistic. DDWIN itself moves even
on ALL (max spread 0.3281), because the floor edits its own definedness. This is the whole
mechanism, isolated.

## 3. THE FLOOR IS NOT CAPITAL-NEUTRAL EITHER (V3 YES)

Rule 8 throughout: the screen sees 2009–2016 only; 2017–2026 read once. Screen = books whose
**IS** own-drawdown window is ≥ FLOOR days (IS-DDSUB, legal) and whose IS DDWIN beta ≤ 0.60,
then max IS Sharpe. U56:

| floor | pool | pick | FULL | OOS | 4b |
|---|---|---|---|---|---|
| 10 | 86 | TREND/AGG/0.20/0.50 | 8.10% / 1.103 / −15.46% | 8.17% / 1.074 / −15.46% | 0 |
| 20 | 74 | TREND/AGG/0.20/0.50 | 8.10% / 1.103 / −15.46% | 8.17% / 1.074 / −15.46% | 0 |
| 40 | 64 | TREND/AGG/0.20/0.50 | 8.10% / 1.103 / −15.46% | 8.17% / 1.074 / −15.46% | 0 |
| **60** | 44 | **TREND/ROW/—/1.00** | **11.53% / 1.201 / −15.91%** | **12.67% / 1.276 / −15.91%** | **1** |

SPY FULL 15.14% / 0.885 / −33.72% (H1 0.957 / H2 0.826), OOS 15.29% / 0.875 / −33.72%; live
RULES v2 FULL 8.62% / 1.201 / −12.05%, OOS Sharpe 1.277. **A purely definitional dial — how many
days a decline must last before its beta counts — is the difference between a 4b candidate and
nothing.** The floor-60 pick is the live RULES v2 book's own TREND gate run at gross 1.00
instead of 0.75; it fails 4a (MaxDD −15.91% against the live book's −12.05%).

Honest denominator: **1 of 27** capital-arm cells clears 4b, against a U56 shelf base rate of
**9 of 112 (8.0%)** and B136 9 of 112, SMALL 0 of 112. The screen's hit rate is its shelf's hit
rate. The floor did not *find* anything; it walked the pick into a clearer. Cost ladder at that
cell: 4b holds at 0 / 10 / 25 bps and **fails at 50 bps** (3 of 4).

## 4. GATES

G0 sample ≥ 10y; G1 112 real books per panel on all three; **G2 at floor 20 this script's DDWIN
reproduces idea 912's committed `proxies_all` exactly over 4,032 readings (max|diff| = 0)**;
G3 912's 48 (U56) / 52 (B136) undefined counts reproduce exactly; G4 an excision exists making
DDWIN defined on all 112 at floor 20 (SPYDD / CRASH / CAL20 on every panel); G5 no leverage
(max gross 1.0000); G6 all 144 population rows, 3,168 agreement rows and 27 capital rows
published; G7 |DDSUB| non-increasing in the floor.

## 5. WHAT THE RECORD SHOULD DO

Every committed DDSUB reading in ideas 867, 910 and 912 should carry its floor, and the floor
should be stated as **a fraction of the binding episode's length**, not as a raw day count —
20 days is 0.83 of SPY's 24-day 2020 decline, which is why it bisects the population. A useful
follow-up is whether a length-relative floor (e.g. ≥ 0.5 x the market's own decline length)
restores invariance; this run does not test it.

## 6. SURVIVORSHIP (rule 9)

U56 / B136 are CURRENT-constituent lists; SMALL is a CURRENT sub-$2B screen (665 names after
dropping `max_1d_move >= 1.0`). Every CAGR and MaxDD LEVEL is optimistic and both 4b bars are
easier than on a point-in-time panel. The FLOOR CONTRAST is same-shelf / same-tape with only the
definedness rule moved, so it is first-order immune; the 4b pass counts and the 8.0% base rate
are not.
