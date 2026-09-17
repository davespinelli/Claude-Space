# Idea 1161 (lane B, 2026-09-17) — why does a RESAMPLE NULL sit ABOVE the OBSERVED MAXIMUM?

**ANSWERED = IT IS THE BOOK, NOT THE RESAMPLE. All three carriers the queue named are
DEAD — block artefacts, wrap-around and marginal resampling are worth 0.003 to 0.007 of a
log gap against a total of 0.060 — and on a tape built to have NO serial structure at all
the machinery reads 0.5244 below its own median, the coin flip. But the queue's own framing
is dead too: the residual is NOT the recovery/mean-reversion story either. An MA(1) carrying
the book's OWN lag-1 autocorrelation closes 27.8% of the distance, and across the three
panels the gap runs the WRONG WAY against ac1.**

The correction a published band needs is therefore **not a bootstrap repair**: on a LEVEL
(`OBJ_MAXDD`) the machinery floor is **1.0054** — no correction is warranted and the whole
6% gap is a fact about the book. On a **max-minus-min SPREAD it is 0.9505**, a genuine ~5%
machinery bias, and it is idea 1148's count inflation showing up *inside the null* where
nobody had looked.

15 of 15 gates pass. 3 of 9 hypotheses supported. Nothing proposed, no RULES change, no
PROTOCOL edit (rule 6). `RULES.md`, `PROTOCOL.md`, `scan.py`, `bot.py` and `baseline.py`
untouched.

SELECTION: this lane takes the LAST open idea; 1161 (`why-does-a-RESAMPLE-NULL-...`) ended
`## Open` and is not EDGAR / Form 4 / 8-K / options / spin-off / live-data. Pure price run —
81 ladder books, 216 population books, 108 null cells × 5 corrections, 5,400 calibration
cells — so it carries this run's mandatory rule-8 walk-forward and both KEEP paths.

---

## The two dials and no more (PROTOCOL rule 4; the queue names both)

`NULL TYPE` {N_IID, N_BLOCK, N_STAT} × `CORRECTION` {R_NONE, R_CENTER, R_PERM, R_PIVOT,
R_MACH} = **15 cells, EVERY ONE PUBLISHED**, scored on all 36 (panel × ladder × object)
cells = **540 rows in `.corrections.csv`**.

**NOTHING IS TUNED.** The headline null is 1159's own `N_BLOCK` at L = 63, 1000 draws, on
1159's own seeds (`SEED_BASE 11591159`, crc32 of `panel|ladder|null`), and `R_NONE` is
*required* to reproduce 1159's committed file — gates **G9 (observed) and G10 (null medians)
both read 3.553e-15**. Every correction is then a strict re-processing of the record's own
draws, not a re-run of a different experiment.

PANEL is not a dial. The four LADDERS and the three OBJECTS are 1159's, inherited whole. The
TAPE FAMILY {S_REAL, S_PERM, S_MA1} in Arm C is a falsification ladder with a **known**
answer under it, every cell published, nothing ever selected on it. The CHANNEL ladder in
Arm D is a one-factor-at-a-time decomposition of the null CONSTRUCTOR. The 216-book
population in Arm F is not a dial and every book is published.

---

## Gates — 15 of 15 PASS, printed before any result number

G1 fast runner ≡ `engine.backtest` **1.388e-17**. G2 the committed U56 W/H126/N=20 triple
**1.622e-03** — 1163's price-vintage defect **CARRIED, not absorbed**: this run reads
0.155520/1.138079/−0.191276 against the committed 0.155787/1.139701/−0.191276, so the bar is
declared at 5e-3 in the script and the deviation printed. G3 SPY OOS 2.894e-03. G4 live
RULES v2 MaxDD ≡ −12.05% at 4.949e-05. G5 SMALL determinism 0.000e+00. **G6 `N_BLOCK` at
L = 1 IS `N_IID` bit for bit (1162's identity) 0.000e+00.** **G7 `perm_index` rows are exact
permutations of 0..T−1 for all three nulls, 0.000e+00 — this is what makes R_PERM a control
and not another bootstrap.** **G8 R_CENTER forces every draw's total log return onto the
observed one, 0.000e+00.** G11 `boot_maxdd` on the identity index ≡ the observed |MaxDD|
1.421e-14. **G9a/G9b replay 1159's committed 108 cells and its "89 of 108" out of its own
CSV at 0.000e+00 — the premise is VERIFIED FROM THE RECORD, never recalled.** G9c the
queue's ratio triple. **G12 the four ladders' anchor rungs ARE the same book, 0.000e+00.**

---

## TWO DEFECTS IN THE PARENT, FOUND WHILE REBUILDING IT, REPORTED NOT ABSORBED

**1. The record publishes a triple without its labels.** The queue quotes 1159's median
ratios as a bare *"0.936 / 0.851 / 0.964 by null type"*. Only 1159's own CSV says which
number belongs to which null (`N_BLOCK 0.9358`, `N_IID 0.8507`, `N_STAT 0.9641`), and the
two readings are **0.085 apart on a 0.15 effect**. The first cut of this script mapped them
in the other order and **G9c failed at 8.527e-02**. The gate is the only reason the error
did not propagate.

**2. The parent's denominator is inflated by a factor of four on its strongest object.**
Every ladder's ANCHOR rung is the SAME book — N = 20, H = 126, gross = 0.75, weekly — so
`OBJ_MAXDD`'s **36 cells are 9 distinct (panel × null) measurements replicated four times**,
differing only by the null's seed (gate G12, observed identical at 0.000e+00). `OBJ_SPREAD`
and `OBJ_ARGMAX` are genuinely 36 each. On distinct cells the parent's headline reads **62
of 81 (0.765)**, not 89 of 108 (0.824). The 4 replicates agree at **9 of 9**, and the
replicate spread of the null MEDIAN is **0.0182 (median) / 0.0256 (max)** of the median
against a headline gap of **0.0585** — so the "36 of 36" is **not** a seed artefact, but it
is **9 measurements, not 36**, and this run quotes the distinct-cell reading beside the
parent's throughout.

---

## ARM C — THE DECISIVE ARM: put a KNOWN answer under the machinery

`S_PERM` re-orders the ladder's rungs by ONE common random permutation. Every rung's marginal
is exact, the cross-rung dependence is exact, and **there is no serial structure left to
lose**, so a resample null of an S_PERM tape is correctly specified and the truth is
**ratio = 1.000, share below median = 0.500**. 25 independent pseudo-tapes per cell × 400
draws × 3 nulls × 3 objects × 12 (panel, ladder) = **5,400 published calibration cells**.

| tape | null | OBJ_MAXDD | OBJ_SPREAD | OBJ_ARGMAX |
|---|---|---|---|---|
| S_PERM | N_BLOCK | **1.0096** | 0.9453 | 0.9724 |
| S_PERM | N_IID | **0.9998** | 0.9509 | 0.9665 |
| S_PERM | N_STAT | **1.0020** | 0.9636 | 0.9902 |
| S_MA1 | N_BLOCK | 1.0065 | 0.9732 | 0.9365 |
| S_MA1 | N_IID | 0.9415 | 0.9532 | 0.8883 |
| S_MA1 | N_STAT | 1.0020 | 0.9911 | 0.9605 |

**Aggregate S_PERM: 1,416 of 2,700 below the median, 0.5244.** Against the real panels'
0.824. **H_MACHINERY REFUTED.**

---

## ARM D — THE CHANNEL LADDER: every machinery channel is worth nothing

One factor at a time off the record's own `N_BLOCK`, on `OBJ_MAXDD`, in log(observed / null
median) so the channels add:

| variant | removes | median log gap | vs the record |
|---|---|---|---|
| K0_RECORD | nothing (N_BLOCK, L = 63) | −0.0603 | +0.0000 |
| K1_NOWRAP | wrap-around only | −0.0614 | **+0.0026** |
| K2_CENTER | the DRIFT channel (Jensen) | −0.0567 | **+0.0046** |
| K3_PERM | the MARGINAL-RESAMPLING channel | −0.0861 | **−0.0066** |
| K4_IID | all block order (L = 63 → L = 1) | −0.1617 | −0.1128 |
| K5_IIDPERM | marginal resampling AND all order | −0.1589 | −0.1039 |

**H_WRAP, H_DRIFT and H_MARGINAL are all REFUTED**, and two of the three move the gap the
*wrong way*. The only variant that moves it materially is K4_IID — and that is not a repair,
it is **a different null**: it removes 63 days of the book's own order. **The gap is a
monotone function of how much of the BOOK's order the null keeps.**

---

## AND THE QUEUE'S REMAINING CARRIER IS DEAD TOO

`S_MA1` runs the S_PERM tape through a common MA(1) filter whose lag-1 autocorrelation is the
anchor book's OWN. On `OBJ_MAXDD` it closes **0.278** of the S_PERM (1.0054) → REAL (0.9415)
distance. **H_AC1 REFUTED.** The book's serial structure carries the gap, but not at lag 1:
`VR(63)` runs 0.53–0.57 while `VR(21)` runs 0.67–0.91, so the structure that shortens these
drawdowns lives at **quarter horizons**, which is exactly why K4_IID (L = 63 → 1) is the one
variant that moves anything.

**AND THE SIGN IS THE OPPOSITE OF THE MEAN-REVERSION STORY**, which is 1162's `H_MEANREV`
refutation seen from this side. Three distinct books, published as three:

| panel | ac1 | VR(21) | VR(63) | recovery drift | perm gap | seed spread |
|---|---|---|---|---|---|---|
| U56 | −0.0501 | 0.7343 | 0.5298 | −0.001476 | −0.0605 | 0.0066 |
| B136 | −0.0378 | 0.6692 | 0.5350 | −0.001690 | −0.0861 | 0.0185 |
| SMALL | −0.0301 | 0.9147 | 0.5665 | −0.000998 | −0.1062 | 0.0083 |

The **least** mean-reverting panel carries the **largest** gap. **n = 3. A DIAGNOSTIC, NOT A
TEST** — all four anchor rows per panel are the same book (G12), so a rank correlation over
the 12 rows would be three points counted four times each, and this run **does not report
one**. The seed-spread column gives the gap's own 1000-draw noise for scale.

---

## THE CORRECTION GRID — all 15 dial cells, all 108 cells each

| correction | N_BLOCK | N_IID | N_STAT | all 108 | on the 81 DISTINCT |
|---|---|---|---|---|---|
| R_NONE (the record) | 30/36, 0.9358 | 29/36, 0.8507 | 30/36, 0.9641 | 89 (0.824), 0.9304 | 62 (0.765) |
| R_CENTER | 29/36, 0.9394 | 30/36, 0.8568 | 29/36, 0.9672 | 88 (0.815), 0.9341 | 61 (0.753) |
| R_PERM | 30/36, 0.9357 | 30/36, 0.8529 | 29/36, 0.9576 | 89 (0.824), 0.9319 | 62 (0.765) |
| R_PIVOT | 6/36, 1.0605 | 7/36, 1.1541 | 6/36, 1.0249 | 19 (0.176), 1.0495 | 19 (0.235) |
| R_MACH | 27/36, 0.9237 | 30/36, 0.8501 | 25/36, 0.9657 | 82 (0.759), 0.9003 | 60 (0.741) |

**H_BOOK SUPPORTED: R_PERM — the null that preserves the observed multiset EXACTLY and
destroys only order — still sits above the observed at 36 of 36 on `OBJ_MAXDD`.**

**H_BAND REFUTED, and this is worth saying plainly.** R_MACH does not improve coverage at all
(inside-90% 0.9630 → 0.9630) because the machinery correction is ~1% and the band is ~30%
wide. **The record's bands were never failing to contain the observed value; they were
mis-centred, and a 1% recentring does not change a verdict.**

---

## WHAT A PUBLISHED BAND WOULD NEED — the deliverable the queue asked for

| object | S_PERM machinery floor | real median ratio | after R_MACH |
|---|---|---|---|
| OBJ_MAXDD (a LEVEL) | **1.0054** | 0.9415 | 0.9248 |
| OBJ_SPREAD (max−min) | **0.9505** | 0.9050 | 0.8501 |
| OBJ_ARGMAX (a margin) | **0.9796** | 0.9198 | 0.8553 |

**A LEVEL needs NO machinery correction** — the whole of its gap is a fact about the book,
and a band around it should be read as "this book's drawdown is genuinely 6% shallower than
a re-ordering of its own returns", which is a *finding*, not an artefact. **A max-minus-min
SPREAD needs one of about 5%**, and it is the **same count inflation idea 1148 corrected in
the observed statistic and nobody had checked in the null** — a max-minus-min over k rungs
of a resampled ladder grows with k on the null side too. **H_OBJECT SUPPORTED.** This is the
one place a mechanical repair is warranted, and it is the *opposite* of the object the queue
was worried about.

---

## RULE 8 AND BOTH KEEP PATHS

72 books per panel (N × H × cadence), **216 in all, every one published** in
`.walkforward.csv`; parameters chosen on 2009–2016 ONLY and read once on 2017–2026.

**4b full 12 of 216, 4b OOS 13 of 216, 4a 0 of 216** (U56 11/11, B136 1/2, SMALL 0/0).

**Best 4b book (full AND OOS): `U56 / weekly / N = 12 / H = 126`** — full **17.65% /
1.1658 / −20.17%** (H1 1.2741 / H2 1.0833), OOS **18.78% / 1.1701 / −20.17%**; against SPY
full 15.06% / 0.8814 / −33.72% and OOS 15.15% / 0.8684 / −33.72%, and live RULES v2 full
8.60% / 1.1980 / −12.05% (OOS 9.42% / 1.2714 / −12.05%). It is **NOT IS-chooser-reachable**
(no chooser on this grid picks it) and it **fails 4a 0 of 216**. Memo written with exact
RULES wording, **recommending PARK**.

**THE CAPITAL QUESTION, AT ITS TRUE WEIGHT.** `CH_NULLDD` uses the null itself as the
selector — the book whose IS |MaxDD| is shallowest relative to its own IS null median. 180
picks published. The correction moves the pick at **9 of 9 (panel, null) cells — but 3 of 9
once R_PIVOT is set aside**, and R_PIVOT is a *reflection*, not a repair: it maps the null
through the observed value, turning "the null sits above" into "the null sits below" by
construction, without pricing why. Mean OOS Sharpe of the pick: **R_NONE 0.7110, R_MACH
0.7110, R_CENTER 0.7241, R_PERM 0.7471**, R_PIVOT 0.9103. **The three honest corrections are
worth +0.000 to +0.036 of OOS Sharpe. H_CAPITAL is recorded SUPPORTED against its declared
bar and is reported here as CAPITAL-IRRELEVANT**, because the bar was written before the
R_PIVOT/repair distinction was visible and this run does not move a bar after seeing it.

Picks clearing 4b full AND OOS: 27 of 180; **4a 0 of 180**. By chooser: CH_ISCAGR 0 of 45
(mean OOS 0.9460), CH_ISSHARPE 0 of 45 (0.8770), **CH_ISDD 15 of 45 (0.8638)**, CH_NULLDD 12
of 45 (0.7607) — a plain IS drawdown chooser reaches a 4b passer more often than the
null-normalised one does.

---

## SURVIVORSHIP (PROTOCOL rule 9)

U56, B136 and SMALL are **current-constituent lists**; SMALL is the current constituents of a
sub-$2B screen, **663 columns after dropping the 52 tickers with `max_1d_move >= 1.0` from
`data/small_meta.csv`** (tape 2010-01-04 → 2026-09-11). Every delisted, zeroed or
screened-out name is absent, so every CAGR, drawdown and 4b pass rate above is the most
flattering the period could have produced.

**It bears on this run's headline DIRECTLY AND IN THE DIRECTION OF THE FINDING.** A
survivor-only panel has *shallower* observed drawdowns than the real one, which pushes the
observed value further below its own null. **The Arm C machinery floor is immune** (it is a
ratio read on the same panel, so the bias divides out). **The residual book gap is NOT**: an
unknown part of the 6% is survivorship, and this run cannot separate them without a
point-in-time panel. The conclusion that survives regardless is the *comparative* one —
machinery ≈ 1.00 on a level and 0.95 on a spread — because both are read on the same tapes.

---

## Files

`2026-09-17_why-does-a-RESAMPLE-NULL-sit-ABOVE-the-OBSERVED-MAXIMUM-at-108-of-108-cells_B.py`
plus `.objects.csv` (108), `.corrections.csv` (540), `.calibration.csv` (5,400),
`.machinery.csv` (108), `.dialgrid.csv` (15), `.channels.csv` (72), `.structure.csv` (12),
`.structure_panel.csv` (3), `.ladder.csv` (81), `.walkforward.csv` (216), `.picks.csv` (180),
`.hypotheses.csv` (9), `.gates.csv` (15), `.console.txt`, `.memo.md`.

**NOTHING ENACTED.** No RULES change, no PROTOCOL clause proposed — rule 6 reserves every
PROTOCOL edit to a Sunday review, and this run priced one null family on one book family.
