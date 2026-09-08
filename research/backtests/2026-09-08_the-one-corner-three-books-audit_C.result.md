# idea 451 — the one-corner-three-books audit (lane C, 2026-09-08)

**ANSWERED, and the queue's framing is RE-SCOPED. The census exists (91 / 301 / 492 cells
quoted by two or more scripts under the three match rules) and the under-specification is
real and large — but it is overwhelmingly a WITHIN-script fact, not a cross-script one
(the same cell name spans a wider Sharpe range inside ONE script than between scripts in
93.5–97.8% of cells), and of the four fingerprint axes only the RANKING KEY carries Sharpe:
+0.1354 at 10 bps over 96 paired flips against +0.0039 (gross channel), +0.0003 (gross
level) and −0.0000 (drop_spy). No KEEP claimed; 4a 0 of 576, 4b 37 of 576 and every 10-bps
passer is an already-published record object. RULES.md, scan.py, bot.py and baseline.py
untouched.**

## Control — the parent reproduces on the object it was measured on
Idea 232 [b2]'s four builds at `U56 n=20 max_vol=off g=0.75`, SPY investable, 10 bps:

| build | this run CAGR / Sharpe / MaxDD / OOS | idea 232 published Sharpe |
|---|---|---|
| V1KEY, NORM (idea 256's) | 9.96% / **0.9560** / −19.49% / 1.0356 | 0.9947 |
| V1KEY, RAW | 9.69% / 0.9787 / −17.89% / 1.0855 | 1.0270 |
| COMP, NORM | 13.41% / 1.0762 / −21.37% / 1.1199 | 1.1084 |
| COMP, RAW (idea 228's) | 13.27% / **1.1075** / −19.39% / 1.1707 | 1.1469 |

**The construction spread reproduces at +0.1516 against the published +0.1522 (|d| 6.0e-4)**,
and MaxDD reproduces to 4 dp on all four builds. The Sharpe LEVELS sit 0.032–0.048 low and
uniformly so: this run starts at `px.index[260]` (2009-01-13) and rebalances through
`engine.backtest`; idea 232's [b1] already priced that same first-bar difference against idea
228's hand-rolled loop. The offset is common to all four builds, so the audited quantity —
the gap between builds — is unaffected. Stated, not swept.

## Leg A — the census (committed artefacts, not prose)
1 874 committed CSVs (this run's own 10 artefacts skipped by the harvester — a harvest is not a quotation); **89 carry (panel, n, level Sharpe)** — 88 files, **68 scripts, 98 395
quotations**. Both tuned parameters, all 12 grid points reported:

| rule (cell key) | cells ≥2 scripts | median cross-script spread | median WITHIN-script spread | disagree @0.02 / 0.05 / 0.10 / 0.20 |
|---|---|---|---|---|
| M1 (panel, n) | 91 | 0.1355 | **0.6602** | 0.945 / 0.846 / 0.681 / 0.308 |
| M2 (+ cost rung) | 301 | 0.0706 | **0.3994** | 0.748 / 0.605 / 0.389 / 0.226 |
| M3 (+ gross level) | 492 | 0.0322 | **0.1221** | 0.571 / 0.372 / 0.222 / 0.120 |

**The control is decisive and it points away from the queue's framing.** In **97.8% (M1),
97.3% (M2) and 93.5% (M3)** of census cells the cell's spread INSIDE a single script already
covers the whole cross-script gap. Two scripts quoting `U56 n=5` 0.72 of Sharpe apart is not
two books mislabelled as one; it is a cell name that never named the axes, and each script
walks that range on its own. Conditioning on cost then gross shrinks the median cross-script
gap 0.1355 → 0.0706 → 0.0322 — cost rung and gross level are the two cheapest specificity
wins available, and neither is a construction discrepancy.

**The fingerprint mostly cannot be recovered from source, which is itself the finding.** Text
rules (published in the script) resolve, over the 68 quoting scripts: key V1KEY 27 / COMP 2 /
**MIXED 34** / UNSTATED 2 / no source 3; channel NORM 29 / RAW 4 / MIXED 6 / UNSTATED 26;
drop_spy DROPPED 26 / UNSTATED 39. **84 of 91 M1 cells contain at least one script whose key
is undecidable from its source, and only 7 cells carry two determinate and different keys**
(0 of 301 at M2, 0 of 492 at M3). Half the record's quoting scripts are MIXED because they
legitimately run both keys in one file — so **a fingerprint is a property of the ROW, not of
the file**, and inferring it from source is the wrong instrument. Every cell's per-script
fingerprint is published in `.census.csv`; the per-script reading in `.fingerprints.csv`.

## Leg B — what the fingerprint is worth (12 corners × 16 builds = 192 books, all reported)
Construction spread (max−min Sharpe over the 16 builds) per cell at 10 bps: **0.0461
(SMALL n=20, cap 0.60) … 0.2453 (B136 n=10, cap off)**, median 0.1604; over all rungs median
0.1420, max 0.4562. Per-axis paired flips, other three axes and the cell held fixed:

| axis | mean dSharpe @10 bps (n=96) | frac > 0 | @0 / @25 bps | mean dCAGR | mean dMaxDD |
|---|---|---|---|---|---|
| **key V1KEY → COMP** | **+0.1354** (sd 0.0720, −0.0090 … +0.2447) | **95.8%** | +0.0679 / **+0.2368** | +5.82 pp | −4.52 pp |
| channel NORM → RAW | +0.0039 (sd 0.0111) | 50.0% | +0.0025 / +0.0060 | −0.09 pp | +0.48 pp |
| gross 0.75 → 1.00 | +0.0003 (sd 0.0016) | 58.3% | +0.0006 / −0.0000 | **+3.21 pp** | **−7.27 pp** |
| drop_spy OUT → IN | −0.0000 (sd 0.0087) | 25.0% | +0.0004 / −0.0007 | −0.00 pp | −0.02 pp |

Holding the key fixed collapses the 16-build spread to a mean 0.0196 at 10 bps: **the key owns
a mean 80.2% of the construction spread (76.1% at 0 bps, 86.5% at 25 bps)**, ≥0.72 in 11 of 12
corners at 10 bps. The one exception is `SMALL n=20 cap 0.60`, where the key owns 0.0% and the
whole 0.0461 sits inside one key. The key's premium **grows with cost** because the un-tilted
composite trades less (8.70 vs 10.97 turns/yr at the audited corner) — it is partly a turnover
fact, not purely a signal fact. Sharpe is gross-invariant (span 0.0016) while CAGR and MaxDD
are not, so **a gross level must be named for any CAGR or drawdown claim and cannot rescue a
Sharpe one**; `drop_spy` is inert on every panel including SMALL, where idea 232 already
priced the same correction at nothing.

## Rule 8 — walk-forward (params picked on ≤2016-12-31, read on 2017-01-01..)
The IS chooser over the 16 fingerprints beats the PRE-REGISTERED live construction
(V1KEY/NORM/0.75/SPY-out) by **mean +0.1375 OOS Sharpe, positive in 31 of 36 cells** (min
−0.0323, max +0.4263); mean OOS Sharpe 0.8182 vs 0.6806, mean regret 0.0279 vs 0.1655. This
is not selection skill: the chooser picks COMP in 8 of 12 corners and the whole gap is the key
axis. It is bought with drawdown — B136 n=10 cap off OOS MaxDD **−33.5% vs −17.3%**; U56 n=20
cap off −27.2% vs −19.4%. Against the comparands the chooser beats SPY OOS in 16 of 36 and
**RULES v2 in 5 of 36**; the pre-registered arm 10 of 36 and **0 of 36**. OOS references at
10 bps: SPY 15.45% / 0.8820 / −33.72%; RULES v2 U56 9.52% / **1.2834** / −12.07%, B136 7.98% /
1.1178 / −12.25%, SMALL 4.55% / 0.6629 / −12.09%.

## KEEP paths (all 576 points = 192 books × 3 rungs)
**4a 0 of 576** against the live RULES v2 on every panel. **4b 37 of 576** — 27 at 0 bps, **8 at
10 bps, 2 at 25 bps** — U56 33, B136 4, **SMALL 0** (idea 136's reproduction again). Binding 4b
bars at 10 bps (of 192): DD 138, H2 128, OOS 116, H1 84, CAGR 80. Every 10-bps passer is a
known record object: 6 of 8 are the COMP-key top-20 g=0.75 books idea 228/232 already
published (best `U56 n=20 cap off COMP/RAW/0.75/SPY-out`: 13.47% / **1.1223** / −19.39%,
halves 1.160/1.118, OOS 1.1833), and the other 2 are V1KEY n=10 g=1.00 books clearing the H2
bar by 0.005 on 20.7 turns/yr. **No KEEP claimed.** The two 25-bps survivors are the same
COMP/RAW corner.

## What this run proposes (Sunday review, report-only — no RULES change)
1. A cell name is a claim about a book only when it carries **(panel, n, max_vol, cost rung,
   gross level, ranking key)**. Cost and gross are the two cheapest wins (median cross-script
   gap 0.1355 → 0.0322); **the ranking key is the one that is worth Sharpe** (+0.1354 at
   10 bps, 80% of the whole construction spread).
2. The fingerprint belongs in the **CSV row**, emitted by the script, not inferred from its
   source: 34 of 68 quoting scripts are legitimately MIXED on the key, and 84 of 91 M1 cells
   contain a script whose key no text rule can resolve.
3. `drop_spy` should be dropped from the fingerprint (inert everywhere, 25% frac-positive at
   a −0.0000 mean); the gross **channel** likewise for Sharpe claims (+0.0039, 50/50), but
   both gross channel and level must be quoted beside any CAGR or MaxDD claim, where a level
   flip alone moves +3.21 pp and −7.27 pp.

Artefacts: `.quotes.csv.gz` (98 395 harvested quotations), `.census.csv`, `.censusgrid.csv`,
`.fingerprints.csv`, `.grid.csv` (192 books × 3 rungs), `.spread.csv`, `.keyshare.csv`,
`.axes.csv`, `.keep.csv`, `.walkforward.csv`, `.refs.csv`, `.console.txt`.
