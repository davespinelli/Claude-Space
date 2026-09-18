# 1250 (lane cloud, 2026-09-18) — is the L NEIGHBOURHOOD of 63 WIDE ENOUGH to make every committed L-KEYED claim SAFE?

**ANSWERED (B): THE NEIGHBOURHOOD IS REAL BUT NARROWER THAN THE RECORD'S OWN PUBLISHED SPAN. At the
record's declared noise multiple the safe band around L = 63 is [16, 200] for the queue's core
outputs and [26, 126] once B_RESOLVED — the decisive bar, the most-cited bar output in the record —
is included. It covers 1242's (42, 126) with room to spare and does NOT reach (21, 252). A
neighbourhood clause written at [42, 126] resolves all 141 unstated-L units; one written at the
record's full span resolves 110 of 141 at best. VERDICT: KILL (capital), NO NEW BOOK, PUBLISHING
CLAUSE RECOMMENDED TO THE SUNDAY REVIEW ONLY.** 13 of 18 gates (the 5 failures are located below and
4 of them are findings about the record), 989s, offline, deterministic.

## The question and the two dials
1242 read the neighbourhood off two rung PAIRS — 0 of 18 outputs separate at (42, 126), 8 of 18 at
(21, 252) — which says nothing about where between 126 and 252 safety ends. This run measures the
band directly on a **21-rung numeric L ladder** (1242's 11 rungs plus 10 new ones filling the
neighbourhood: 16, 26, 32, 52, 79, 100, 160, 200, 378, 756) plus the degenerate rung L = T.
Dial 1 = NOISE MULTIPLE {1.0, 1.5, 2.0, 3.0}; dial 2 = OUTPUT SET {OS_CORE 7, OS_WIDE 14, OS_ALL 18}.
**12 cells, every one published**, and all 18 per-output bands published at all four multiples (72
rows in `.bands.csv`). Not dials: the 72 decisions, the 18 output definitions, B = 1000, the 8 seed
streams, and the **pre-declared** assertion band BAND_REC = (21, 252) — 1242's LP_REC, the span the
record has actually published at — with BAND_NEAR = (42, 126) as a descriptive control.

## The map (the queue's actual ask), at the declared multiple m = 2.0
| output | band | breaks at |
|---|---|---|
| O_REACH, O_PICK, O_MARGIN, O_LEVEL, O_GAPRATIO | **[1, 1008]** — all 21 rungs, exactly invariant | never |
| B_GAPEXCEEDS | [1, 756] | above at 1008 |
| B_MODALMATCH | [1, 378] | above at 504 |
| B_Q95, B_NULLMED, B_BOOT95, B_PCTRANK, B_MODALRUNG | [1, 252] | above at 378 |
| B_Q05 | [10, 378] | below at 5, above at 504 |
| B_RECRANGE | [16, 252] | below at 10, above at 378 |
| B_PPICK | [10, 200] | below at 5, above at 252 |
| B_PMAX | [5, 200] | below at 2, above at 252 |
| B_SD | [21, 200] | below at 16, above at 252 |
| **B_RESOLVED** (the record's decisive bar) | **[26, 126]** | below at 21, above at 160 |

Intersections: **OS_CORE [16, 200]**, **OS_WIDE = OS_ALL [26, 126]** (B_RESOLVED binds both wider
sets). At the strictest reading m = 1.0 the OS_CORE band is still 5 rungs wide, **[42, 100]** — which
is exactly why 1242's (42, 126) pair found nothing: the pair sits on the band's edge, and 126 is
inside only from m = 1.5 up.

## What a clause would buy, over the record's own 141 units
The census is inherited whole from 1242 (`.census_units.csv`, 4,031 committed text units): of the
1,272 OS_CORE units, 1,129 carry a verdict, 158 of those rest on a bar-side output and so NEED an L,
and **141 state none** (G9 replays this exactly; G10 replays the OS_WIDE 700).

| m | set | band | covers (21,252) | covers (42,126) | units | resolved vs (21,252) | resolved vs (42,126) |
|---|---|---|---|---|---|---|---|
| 1.0 | OS_CORE | [42, 100] | no | no | 141 | 0 | 110 |
| 1.5 | OS_CORE | [26, 126] | no | yes | 141 | 10 | **141** |
| **2.0** | **OS_CORE** | **[16, 200]** | no | yes | 141 | **110** | **141** |
| 3.0 | OS_CORE | [1, 252] | **yes** | yes | 141 | **141** | 141 |
| 1.0 / 1.5 / 2.0 / 3.0 | OS_WIDE = OS_ALL | [42,100] / [32,126] / [26,126] / [16,200] | no | no/yes/yes/yes | 700 | 17 / 21 / 115 / 147 | 666 / 700 / 700 / 700 |

**H_BAND SUPPORTED** (every bar output's band is wider than a point at m = 2.0), **H_COVER REFUTED**
(no cell but m = 3.0 / OS_CORE covers the record's own span), **H_RESOLVE SUPPORTED** (110 of 141 at
the declared multiple).

## Rule 8 — the band measured in sample, read once on 2017-2026 (H_TRANSFER REFUTED)
The pre-declared choice rule (most units resolved against BAND_REC; ties to the smallest multiple,
then the smallest set) reaches **m = 3.0 / OS_WIDE, IS band [16, 200]**. Read once on OOS book
returns, that cell's band is **[26, 79]** — narrower at both ends, and the IS band does NOT hold:
7 of 14 outputs keep or widen their band, 7 narrow, and the binding one, B_RESOLVED, goes
[16, 200] -> [26, 79]. **The neighbourhood still EXISTS out of sample** — 13 of 13 bar outputs have
a band wider than a point at every multiple — **but its width does not transfer**, so a clause must
be written on the narrow reading, not the in-sample one. Bands covering BAND_REC out of sample:
1 / 4 / 6 / 12 of 13 at m = 1.0 / 1.5 / 2.0 / 3.0.

## Capital, and why the clause is worth nothing to it (H_CAPITAL REFUTED)
The book PICK never moves with L — **0 of 72 decisions, at all 22 rungs (G12 exact)** — so no
weights function anywhere in this record depends on the block length. What moves is the GATE. Over
the whole ladder the P_boot >= 0.90 selector fires 11 to 32 times of 72, and:

- **inside the rule-8 band [16, 200]**: mean OOS Sharpe 0.7908 to 0.7938 (d_sel -0.0014 to +0.0016,
  0.0030 wide), realised **4b BOTH 18 to 20**;
- **over the whole ladder**: d_sel -0.0033 to +0.0027 (0.0060 wide), 4b BOTH 13 to 21;
- **do-nothing (never gate) is 24 4b passes and 0.7922** — so the gate destroys 3 to 11 passes at
  every single rung, inside the safe band as much as outside it.

So H_CAPITAL is REFUTED in the only sense that matters: the band is not tight enough to make even the
4b count invariant (18-20 inside it), and the whole L question is worth ±0.003 of mean OOS Sharpe
against a gate that costs 4 to 6 4b passes wherever it is set. **4a 0 of 162** (A_DD fails at 153 —
live RULES v2's -12.05% MaxDD). **4b full 26, 4b OOS 30, BOTH 25 rows -> 19 distinct books**
(U56 20 rows, B136 5, SMALL663 0), binding leg the DD cap (fails at 106 of 162), every one prior art:
2026-09-04 incumbent U56 N=20/H126/G0.75/W 15.62% / 1.1423 / -19.13% full, halves 1.2049/1.1009, OOS
17.04% / 1.1688; U56 N=12/H126/G0.75/W 17.69% / 1.1686 / -20.17%, OOS 18.87% / 1.1748. Benchmarks:
U56 SPY 15.13% / 0.8848 / -33.72% (halves 0.9598/0.8234), OOS 15.28% / 0.8745; U56 live RULES v2
@10 bps 8.62% / 1.2017 / -12.05% (halves 1.2329/1.1771), OOS 9.47% / 1.2778. **This run adds no book.**

## The five failing gates, located rather than excused
G6, G7 and G8 are pooled replays of 1242 and were **expected to fail**, because this lane's SMALL
panel is the 663-name max_1d_move-filtered one (mandated) and 1242's was the unfiltered 715-name
panel — 1272's finding, restated here as a measurement. The decomposition:

- **B136 is a clean replay.** Max deviation over all 18 outputs x 288 rows is **4.44e-16** against
  1242's in-memory values (G6a's literal "bit for bit" wording is what fails), and **exactly 0.0**
  when the two committed `.outputs.csv` artefacts are merged and differenced directly. B136 is the
  weekly-cached tape, so nothing moved: the machinery is identical.
- **SMALL is the panel split.** Exactly **4 of 72 decisions pick a different rung**, all four on
  SMALL (G6c PASS): A/CADENCE/CH_ISSHARPE, A/CADENCE/CH_ISDD, B/N/CH_ISCAGR, B/CADENCE/CH_ISSHARPE.
  That is the whole of G7's 1-of-72 reach gap and G8's 0.0278 resolution-rate gap.
- **U56 is the daily tape restatement, and it exposes one fragile output (G6b FAIL at 0.418, a
  FINDING).** Off the degenerate rung, a ~1e-6 restatement of the adjusted closes moves every level
  output by 1e-6 to 5e-5 (O_LEVEL 1.06e-06, B_NULLMED 2.98e-05, B_Q95 1.49e-05) and B_PPICK by one
  draw (0.001) — inert. **B_PCTRANK moves by up to 0.418 on 36 of 264 rows**, and all 18 of the
  moves above 0.05 are **CH_ISDD at L >= 126**: where the draw law is coarse, the observed level sits
  in a mass point and its percentile rank is decided on near-equality. At the degenerate rung L = T
  every draw reproduces the observed path exactly, so B_PCTRANK and B_GAPEXCEEDS are decided on exact
  equality and flip 0 <-> 1 on 4 U56 rows.
- **The implication for this idea's own answer:** B_PCTRANK's measured band [1, 252] at m = 2.0
  **overstates its reliability** — an output that a 1e-6 tape restatement can move by 0.4 is not made
  safe by any block-length clause. The honest core set is the five exactly-invariant observed
  outputs plus B_Q95 / B_NULLMED / B_BOOT95 / B_RECRANGE.
- G7a PASSES: reach is **constant across all 22 rungs** inside this run, which is the L-freeness
  claim itself; only its level (13 here vs 1208's 14) moves with the panel.

## What the record should adopt (rule 6: recommended, not enacted)
Replace the point convention with a band: **"a resample output published without an L asserts its
claim for every L in [42, 126]"**. That clause is measured-safe at m >= 1.5 in sample for all 141
unstated-L OS_CORE units and for all 700 OS_WIDE ones, it is the narrow (out-of-sample) reading
rather than the flattering one, and it costs nothing, because no book in this record depends on L.
Do NOT write the clause at the record's published span (21, 252): B_RESOLVED, B_SD, B_PPICK and
B_PMAX all break inside it. And publish B_PCTRANK with a tape-vintage stamp, or stop publishing it.

## Survivorship (rule 9)
U56 and B136 are CURRENT-CONSTITUENT lists; SMALL663 is a current sub-$2B screen with 52 of 715
names dropped on max_1d_move >= 1.0. Every level and every 4b count is an UPPER bound. The headline
is a set of swings of the SAME statistic on the SAME books measured at different block lengths, so a
level bias moves every rung together and the bands are first-order immune; the capital table's 4b
counts are not, and are quoted as upper bounds.

## Files
`2026-09-18_is-the-L-NEIGHBOURHOOD-of-63-WIDE-ENOUGH-to-make-every-committed-L-KEYED-claim-SAFE_cloud.py`
plus `.bands.csv` (72), `.grid.csv` (12), `.outputs.csv` (1,584), `.seedsweep.csv` (576),
`.walkforward.csv` (72), `.capital.csv` (21), `.census.csv` (3), `.books.csv` (162),
`.gates.csv` (18), `.console.txt`.
