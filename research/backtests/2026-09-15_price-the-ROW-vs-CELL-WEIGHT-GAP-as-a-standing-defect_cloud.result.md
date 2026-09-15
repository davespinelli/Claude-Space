# Idea 973 (cloud lane, 2026-09-15) — price the ROW-vs-CELL WEIGHT GAP as a standing defect

**ANSWERED = PARTLY, AND NOT IN THE FORM ASKED. KILL for "the row-vs-cell gap is a standing
defect"; the defect that IS standing is a POOLING gap across artifacts, not a weighting gap
inside one.** Nothing promoted, no rule change, rule 6 untouched. `RULES.md`, `PROTOCOL.md`,
`scan.py`, `bot.py`, `baseline.py` untouched.
SELECTION: the LAST Open idea in QUEUE.md, per the lane rule; it carries a price leg and names
no EDGAR / Form 4 / 8-K / options / spin-off / live-data object.

Script `2026-09-15_price-the-ROW-vs-CELL-WEIGHT-GAP-as-a-standing-defect_cloud.py`.
Artifacts: `.claims.csv` (1,819), `.pooled.csv` (30), `.corpus.csv` (909), `.grid.csv` (1,200),
`.balanced.csv`, `.walkforward.csv` (180), `.hypotheses.csv`, `.gapsummary.csv`, `.console.txt`.

## What was asked
Idea 970's WIDE census read **67.6% destruction row-weighted and 25.0% cell-weighted**, because
ONE cell (`U56/TOP20/g0.75/W`) carried **4,094 of its 4,335 rows** — a row-weighted share that
measures citation count rather than the object. Idea 951 found the same shape on the 4b leg
alphabet. The queue asked for the census: how many of the record's committed SHARE claims move
by more than 10 pp between row, cell and file weighting, and what clause follows.

## What was measured
**4,759 committed csv artifacts scanned; 909 (413 MB) carry a pre-registered SHARE column AND a
nameable cell key**, of which 74 are the record's own null / coin-flip generators and are named
in `.corpus.csv`. That is **1,819 (file, statistic) share claims over 2,564,269 committed rows
and 574,110 (file, cell) pairs**; 1,677 claims across 835 files after excluding the null
generators. Plus a **1,200-row control grid** (5 books × 3 panels × 4 gross × 4 cadences × 5 cost
rungs) which has exactly one row per cell and is therefore balanced by construction, and 180
rule-8 picks.
TUNED 2: CLAIM SET (ALL / NONNULL / GRID) and WEIGHTING (ROW / CELL / CELLANY / FILE /
FILECELL) — every level printed, none chosen. Statistic, file and panel are reported, never
fitted. **GATES 6 of 6.**

## The answer — inside an artifact there is essentially no gap
| claim set | claims | rows | >10 pp on ROW−CELL | >10 pp on the widest pair | median gap | max gap |
|---|---|---|---|---|---|---|
| ALL | 1,819 | 2,564,269 | 0.011 | 0.328 | **0.00 pp** | 30.30 pp |
| NONNULL | 1,677 | 2,331,090 | **0.010** | 0.316 | **0.00 pp** | 30.30 pp |

`H_GAP` **PASSES at 0.316** against its 0.25 bar — **and that headline is misleading, so it is
reported with its own correction.** The widest pair includes `CELLANY` (does a cell EVER pass),
which answers a different question from `ROW` and `CELL` (what share passes). **On ROW versus
CELL alone the figure is 0.010 — 17 claims of 1,677 — and the median gap is exactly 0.00 pp.**

## 970's one-cell case is an OUTLIER, not the record's normal
`H_CONC` **FAIL** — Spearman(largest-cell row share, |ROW−CELL| gap) = **+0.0117** (bar 0.50);
Spearman(Herfindahl, gap) = −0.0634. `H_ONE` **FAIL** — the **median largest-cell row share over
1,677 NONNULL claims is 0.051** (90th percentile 0.333, 99th 0.616) against a 0.50 bar. **Only
1.2% of committed share claims have any cell carrying more than half their rows, and 0.7% more
than 90%.** Median claim: 25 cells, 225 rows. The concentration that produced 970's 67.6% is a
roughly 1-in-83 event in this corpus, not a standing property of it.

G3 confirms the case itself rather than explaining it away: **970's committed `mapped_WIDE.csv`
is 27,143 rows (as published) over 31 distinct panel/book/gross/cadence cells, its largest cell
`U56|TOP20|0.75|W` carries 10,265 rows = 37.8% of the corpus and its top three carry 80.5%.**
970's concentration is real. It is just not typical.

## The defect that IS standing is a POOLING gap
Pooled over the whole corpus, statistic by statistic, the five weightings separate — and the two
that separate most do so between **ROW and FILE**, i.e. between counting rows and counting
artifacts, not between counting rows and counting cells:

| statistic | files | rows | ROW | CELL | CELLANY | FILE | FILECELL | spread (5) | spread (4) |
|---|---|---|---|---|---|---|---|---|---|
| `keep4b` | 148 | 306,214 | **0.073** | 0.033 | 0.051 | **0.192** | 0.191 | 15.93 pp | **15.93 pp** |
| `pass4a` | 498 | 583,318 | **0.123** | **0.248** | 0.268 | 0.124 | 0.126 | 14.53 pp | **12.51 pp** |
| `pass4b_OOSPURE` | 6 | 43,140 | 0.048 | 0.082 | 0.278 | 0.060 | 0.069 | 22.95 pp | 3.39 pp |
| `pass4b_REC` | 6 | 43,140 | 0.049 | 0.080 | 0.276 | 0.060 | 0.068 | 22.64 pp | 3.07 pp |
| `pass4b` | 556 | 870,865 | 0.134 | 0.140 | 0.165 | 0.185 | 0.185 | 5.02 pp | 5.02 pp |

`H_POOLED` **PASSES at 0.267** over all five weightings (4 of 15 statistics) — but two of those
four move only because of `CELLANY`. **Over the four weightings that estimate the same quantity
the figure is 0.133, two of fifteen: `keep4b` (7.3% row-weighted against 19.2% file-weighted,
15.93 pp) and `pass4a` (12.3% row-weighted against 24.8% cell-weighted, 12.51 pp).** Both are
statistics the record pools across hundreds of artifacts of wildly different sizes. Inside one
artifact the design is usually near-balanced; it is the POOLING that creates the concentration.

`H_BALANCED` **PASS**: on this run's own 1,200-row grid the ROW and CELL shares are identical to
machine precision at every cell-key coarseness (1,200 cells × 1 row, 240 × 5, 15 × 80; `pass4b`
0.0567, `pass4a` 0.0167 throughout). A design with equal rows per cell has no gap at all, which
is what makes the gap a defect rather than a definition (G4 proves the same identity in closed
form).

## Rule 8
Book × gross chosen on **2009–2016 alone** by 3 IS-only choosers × 3 panels × 4 cadences,
2017–2026 read **once** (G6: picks invariant to permuted OOS columns).
**OOS 4b 4 of 36; OOS 4a 0 of 36. Full-sample grid at 10 bps: 4b 10 of 240, 4a 3 of 240.**
All four OOS passes are the same object — `U56 / BAND03 @ gross 1.00`, picked daily and weekly:
best `U56/W/C_ISLEGS → BAND03 @ g1.00` OOS **12.68% / 1.277 / −15.91%** against **SPY OOS 15.27%
/ 0.874 / −33.72%** and **RULES v2 OOS 9.46% / 1.277 / −12.05%**; the daily twin reads 12.46% /
1.288 / −14.77%. **This independently reproduces idea 970's committed best rule-8 pick (12.68% /
1.276 / −15.91%) on a different grid built by a different script.** It is the live book levered
to 100% gross — it clears 4b, **fails 4a on drawdown**, and buys its CAGR with gross rather than
skill. Nothing here is a KEEP on either path.

## Capital
**No.** This run prices a bookkeeping convention, not a rule; its only price leg reproduces a
book the record has already declined twice. The weighting census carries no capital consequence
directly — but it does bound how much of the record's falsification machinery is mis-calibrated:
**two of fifteen pooled share statistics, and one committed claim in a hundred, and no more.**

## What this proposes (a POOLING clause, for Sunday review, NOT written into PROTOCOL.md)
> *"A share claim states its unit. Inside one artifact the default is ROW weighting and no
> restatement is required, because the record's designs are near-balanced (median largest-cell
> row share 0.051). A share POOLED ACROSS ARTIFACTS is published BOTH row-weighted and
> file-weighted, and where the two differ by more than 10 pp the file-weighted figure is the
> headline, because a row-weighted pooled share measures how often a cell was written down.
> Any claim whose largest cell carries more than 25% of its rows names that cell and publishes
> the cell-weighted figure beside the row-weighted one."*

Cost of adoption as measured here: **17 of 1,677 committed claims (1.0%) gain a second figure;
2 of 15 pooled statistics change headline — `keep4b` 7.3% → 19.2% and `pass4a` 12.3% → 24.8%;
no committed verdict changes and nothing is withdrawn.** The clause is cheap because the defect
is narrow — which is itself the finding, and the opposite of what the queue assumed.

## Survivorship (rule 9)
U56, B136 and SMALL are CURRENT-CONSTITUENT lists; SMALL additionally drops the 52 tickers with
`max_1d_move` ≥ 1.0 per `data/small_meta.csv`. The weighting census is a contrast between two
ways of AVERAGING THE RECORD'S OWN NUMBERS and carries no price exposure at all. The rule-8
triples are levels read against SPY, which is not survivorship-inflated, so the four 4b passes
reported are UPPER bounds and every FAIL is understated.

Follow-ups filed: 977 (is `keep4b`'s 7.3%-vs-19.2% pooling gap a size effect or a vintage
effect), 978 (do the record's committed cross-artifact shares change any verdict under
file-weighting), 979 (should a share claim's unit be a required column in every committed csv).
