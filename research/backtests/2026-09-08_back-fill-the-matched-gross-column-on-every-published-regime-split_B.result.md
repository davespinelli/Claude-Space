# Idea 471 — back-fill-the-matched-gross-column-on-every-published-d_on/d_off-regime-split (lane B, 2026-09-08)

**Verdict: ANSWERED / SPLIT. No KEEP, no RULES change.** The queue's premise holds for the
shape the record's headline actually is — an **ALWAYS-ON** instrument's delta split by regime —
and the collapse is near-total: of the 61 positive published claims only **42.6%** stay positive
against a gross-matched static, and for the `gross` family the pooled d_on goes **+4.25 → +0.14
pp/yr** with the sign becoming an exact coin flip (13/27 positive, sign p **1.0000**). On idea
246's own headline cell (u56 / EWall / spy200 / 10 bps) the published **+6.4062 pp/yr becomes
+0.0051 (full-sample match) and −0.0082 (within-regime match)** — the arm holds 0.3745 of NAV
where its control holds 0.7496, and that is the entire claim. The **CONDITIONAL** shape behaves
differently, and the comparand decides which way: it survives a full-sample match (75.0%) but
**not a within-regime one (64.8%; of its 30 positive claims only 26.7% stay positive)**.
**Census: the record cannot adjudicate itself** — only **14 of 85** regime-split files and
**2,812 of 39,136** rows (7.2%) publish realised gross for both arm and comparand.

Script `research/backtests/2026-09-08_back-fill-the-matched-gross-column-on-every-published-regime-split_B.py`,
log `…_B.log.txt`, artefacts `…census.csv` / `…censusgap.csv` / `…grid.csv` (4,536 rows) /
`…match.csv` (648 matches) / `…restated.csv` (648 claims × 2 shapes) / `…signtests.csv` /
`…walkforward.csv` / `…livebase.csv`.

---

## Construction

3 panels (u56 56 names, broad 136, small 439 after idea 130's bad-split drop) × 3 ungated base
books (V1u, TOP20, EWall) × 3 cost rungs (0 / 10 / 25 bps) × 8 instruments × 3 regimes ×
{conditional arm, always-on sibling, do-nothing control, 4 gross-matched statics} =
**4,536 runs, every one printed and written to the `.grid.csv`**. Exactly TWO tuned dimensions:
**INSTRUMENT** (idea 246's g200-dg, band3-dg, abs12-dg, vol60-dg, stop15, stop25, ddctl8,
gross50) and **REGIME** (spy200, breadth20, hivol80). Panels, books and cost rungs are reported,
never selected on. Idea 94's harness and idea 246's `run_cond` are imported, not re-implemented.

**Two matched statics, because a regime split needs one idea 249 did not.** Idea 249 matched on
FULL-SAMPLE mean realised gross. For a regime-conditional arm the gross deficit is concentrated
in the armed regime by construction, so a full-sample match spreads the arm's deficit over days
on which it never de-grossed and leaves an ON-regime gap in exactly the quantity a d_on claim is
measured in. Both are therefore solved and reported:

- **MF** — static at the arm's full-sample mean realised gross (idea 249's convention);
- **MON** — static at the arm's **ON-regime** mean realised gross (**primary**).

Checks, asserted before any number was read. **(a)** `run_cond` with no instrument equals
`engine.backtest` at max |diff| **0.000e+00**. **(b)** each of the **648** matched statics is
solved to its arm's own realised mean gross in its own cell and rung: max |achieved − target|
**6.08e-05** (full) / **9.53e-05** (ON) against a 1e-4 tolerance. **(c)** the OFF-regime gross of
a conditional arm is close to but not identical to the control's — the instrument does not ACT
off the regime but the arm carries the holdings its armed days left it; the residue is
**1.26e-02** max, reported rather than assumed.

## 1. The census — the record cannot adjudicate its own regime claims

2,013 committed CSVs (1,661,726 rows) scanned. Detector is deliberately conservative: a bare
`on`/`off` column counts only when its opposite number is present in the same file, because in
this record a lone `off` beside `shift` is a rebalance-PHASE offset, not a regime (the cadence
corpus alone would otherwise have added 7,894 spurious rows). Miscounts therefore run toward
UNDER-counting, the safe direction for a coverage bound. Both lanes' idea-471 outputs are
excluded — they are censuses OF the record, not claims IN it.

| decidability | files | rows | % of regime rows |
|---|---|---|---|
| UNDECIDABLE — no gross column at all | 63 | 31,608 | 80.8% |
| UNDECIDABLE — one gross column, no control level | 7 | 4,230 | 10.8% |
| UNDECIDABLE — one gross column, no arm label | 1 | 486 | 1.2% |
| DECIDABLE — within-file arm/control label | 4 | 1,920 | 4.9% |
| DECIDABLE — paired gross columns | 10 | 892 | 2.3% |

**85 files / 39,136 rows (2.36% of the record's rows) carry a regime split; 14 files / 2,812 rows
(16.5% / 7.2%) are gross-decidable from the committed file.** Of the 892 pairwise-decidable
cells, **685 (76.8%) carry a realised-gross gap ≥ 0.05 NAV** between arm and comparand — i.e.
where the column exists, it usually shows the confound. Record-wide the share of regime-split
rows carrying it is therefore **bounded at 1.8% – 94.6%** and is **not reported as a point**:
the undecidable 92.8% cannot be adjudicated without a re-run, which is the census's real finding.

## 2. The confound, measured (mean realised gross gap vs the published control, NAV)

| family | gap ON-regime, always-on | gap ON-regime, conditional | cells ≥ 0.05 |
|---|---|---|---|
| gross | **0.375** | 0.320–0.333 | 100% |
| dd | 0.284–0.294 | 0.243–0.254 | 100% |
| gate | 0.165–0.200 | 0.152–0.181 | 61–78% |
| stop | 0.015–0.019 | 0.019–0.020 | 5.6–11.1% |

## 3. H2 — how many published claims survive? (10 bps; survive = sign preserved AND |restated| ≥ 0.5 |published|)

| shape | n | mean d_on vs control | vs MF | vs MON | survive MF | survive MON | of the POSITIVE claims, still positive vs MON |
|---|---|---|---|---|---|---|---|
| **A — always-on split (the record's headline)** | 216 | −0.572 | −1.678 | **−2.651** | 51.9% | **46.8%** | **42.6%** (61 cells) |
| **C — regime-conditional split** | 216 | −3.161 | −3.133 | **−4.992** | 75.0% | **64.8%** | **26.7%** (30 cells) |

Restricted to publishable magnitudes (|d_on| ≥ 1.0 pp/yr): A 48.1%, C 71.5%. Cost rungs move
nothing (A survives 47.7 / 46.8 / 46.8% at 0 / 10 / 25 bps; C 62.0 / 64.8 / 65.3%), so **this is
not a cost story.**

**The `gross` family is the queue's own object and it is where the collapse is total:** shape A
pooled d_on **+4.2524 → +0.1580 (MF) → +0.1426 (MON)**, median **+6.4062 → +0.0203 → −0.0047**,
positive 19/27 → 19/27 → **13/27, sign p 1.0000**. Restated, the claim is a coin flip.

## 4. H3 — the claim SHAPE "d_on > d_off" (the armed regime is the one it pays in)

| shape | holds vs control | vs MF | vs MON | ordering FLIPS |
|---|---|---|---|---|
| A | 38.4% | 46.3% | **26.4%** | **36.1%** |
| C | 18.5% | 31.5% | **16.2%** | 27.3% |

By family (shape A, vs control → vs MON): gross **74.1% → 51.9%**, dd **70.4% → 25.9%**,
gate 35.2% → 15.7%, stop 11.1% → 35.2%. The families whose gross gap is large are the families
whose ordering does not survive; `stop`, whose gap is 0.015–0.019 NAV, is the only one that moves
the other way — a clean internal control on the mechanism.

## 5. H4 — is anything left? (exact two-sided sign test, 10 bps)

| shape | statistic | n | positive | mean | median | p |
|---|---|---|---|---|---|---|
| A | d_on vs control | 204 | 29.9% | −0.572 | −1.002 | 0.0000 |
| A | d_on vs MON | 216 | 21.8% | −2.651 | −1.822 | 0.0000 |
| A | **gross family, d_on vs MON** | 27 | **48.1%** | **+0.143** | **−0.005** | **1.0000** |
| C | d_on vs control | 204 | 14.7% | −3.161 | −1.976 | 0.0000 |
| C | d_on vs MON | 216 | 13.0% | −4.992 | −2.754 | 0.0000 |

Restated, regime conditioning is **negative** almost everywhere and a **coin flip** exactly where
the record's headline lives. Nothing is left that is both positive and distinguishable from zero.

## 6. Rule 8 — walk-forward (INSTRUMENT, REGIME) chosen on 2009–2016 IS alone, 2017–2026 read once

| shape | chooser | OOS statistic > 0 | median OOS statistic | median regret vs OOS oracle | picks whose OOS **restated** d_on > 0 |
|---|---|---|---|---|---|
| A | published (IS d_on vs control) | **26/27** | +9.5439 | 0.8130 | **13/27 — a coin flip** |
| A | restated (IS d_on vs MON) | 7/27 | −3.4436 | 4.6340 | 7/27 |
| C | published | 4/27 | −2.3737 | 3.3628 | **0/27** |
| C | restated | 3/27 | −4.1219 | 4.6270 | 3/27 |

The published statistic transfers on **its own terms** (26/27) and on the restated terms not at
all (13/27) — precisely the signature of a statistic that is measuring gross, which is stable
out of sample, rather than timing, which is not.

**OOS levels of the rule-8 picks vs the comparands PROTOCOL step 3 requires** (10 bps; SPY OOS
CAGR 15.45% / Sharpe 0.882). Shape A published picks: broad/EWall 7.98% / 1.119, u56/EWall 6.86%
/ 1.136, small/TOP20 10.11% / 0.729 — against their own matched statics 4.64% / 1.104, 6.85% /
1.136, 9.52% / 0.807 and the do-nothing controls 13.93% / 1.102, 13.82% / 1.136, 17.10% / 0.809.
**Every pick gives up 3–7 pp/yr of OOS CAGR to its own control for ≈ 0.02 of OOS Sharpe.** Live
RULES v2 OOS is 7.98% / 1.119 (broad), 9.53% / 1.285 (u56), 3.84% / 0.566 (small).

## 7. KEEP paths, on every row

4a **49 / 4,536** — and every one of them is a **matched static** (33 matchedONA, 16 matchedON);
**no conditional or always-on arm passes 4a on any panel, book or rung.** 4b **279 / 4,536**;
among conditional arms at 10 bps, **46**. Those 46 are u56 (28) and broad (18), EWall (29) and
TOP20 (17); their Sharpe excess over their own matched static is **+0.0268** (39/46 positive) and
their OOS excess **+0.0563** (42/46), **but their CAGR is below the do-nothing control in 46 of
46** and 9 of 46 are passes the matched static already has. Best row: broad / EWall / gross50 /
spy200 — CAGR 11.79%, Sharpe **1.2112** (H1 1.2757 / H2 1.1489), MaxDD −17.33%, OOS Sharpe 1.2579,
OOS CAGR 12.09%, realised gross 0.685.

**This is idea 249's already-recorded residual, not a new object** (idea 249, lane B, 2026-09-08:
57/216 arms passed 4b where their matched twin did not, best fails 4a, no KEEP). It is a
de-grossed gate/de-gross book on EWall — an object ideas 94, 244, 249 and 468 already carry — it
fails 4a against the live RULES v2 everywhere, and no procedure tested here selects it: this
idea's own rule-8 chooser lands on arms whose OOS restated statistic is ≤ 0 in 27/27 cells.
**No memo, no RULES change. RULES.md, scan.py, bot.py and baseline.py untouched.**

## 8. Concordance with the concurrent cloud run

The cloud lane ran idea 471 the same day (`…_regime-split_cloud.py`, committed as `bb646c6`
while this grid was still running) with a different construction: 864 claims on 2 rungs against a
full-sample-matched static only, and a much stricter census admission rule (a matched ON/OFF
column PAIR plus a regime witness, admitting 4 delta claims over 3 files / 1,890 rows, against
this run's 85 files / 39,136 rows for any regime-split column). **Same verdict, same direction,
and one shared number is exact:** idea 246's headline cell u56 / EWall / spy200 / 10 bps,
published d_on **+6.4062 pp/yr**, appears identically in both runs, and both find it collapses to
≈ 0. Both find the always-on shape's premise CONFIRMED (cloud: pooled gap +2.308 → −0.694, sign
inverts, 69.9% of the magnitude is gross arithmetic; here: positive claims 61 → 42.6% surviving,
gross family to a coin flip) and both find **0 of the record's published d_on/d_off delta claims
publish both an arm and a control gross**.

**Where the two part company is the CONDITIONAL shape, and the reason is the comparand.** The
cloud run reports it survives (published gap −2.690 → restated −2.608, only 3.0% of the magnitude
gross arithmetic) using a full-sample match; this run reproduces that under **MF** (survival
75.0%, mean −3.161 → −3.133 — the same near-null shift) and then shows it **does not hold under
the within-regime match MON** (64.8%, mean → −4.992, and of the 30 positive conditional claims
only 26.7% stay positive). Neither result contradicts the other: they are two different controls,
and the stricter one is the one a d_on claim is actually measured against. The conditional shape's
survival is therefore **conditional on the matching convention**, which is itself worth publishing.

## 9. Limits

**SURVIVORSHIP:** all three panels are current-constituent lists (idea 54), so every absolute
CAGR is optimistic. Sections 3–5 are paired differences inside one cell on the same days and are
far less exposed; the section 6–7 LEVELS are fully exposed and are upper bounds.
**Census coverage:** the detector is column-name-based, so a regime split published only in prose
or in a `.result.md` table is invisible to it; the 92.8% undecidable share is a floor on what
cannot be adjudicated, not a ceiling. **The record's regime splits are concentrated:** 4 of the
14 decidable files come from two parent scripts (idea 246-C and idea 249-B), so file-clustering
means the decidable sample is not 14 independent claims.

## 10. Recommended clause (nothing modified)

Any result splitting a delta by regime must publish **mean realised gross for the arm and for the
comparand, separately within each regime state** — not a full-sample average, which is what a
regime-conditional arm's gross deficit hides behind. Where the two differ by ≥ 0.05 NAV the
headline must be quoted as an excess over a static matched **within that regime**, with the
full-gross number kept beside it.
