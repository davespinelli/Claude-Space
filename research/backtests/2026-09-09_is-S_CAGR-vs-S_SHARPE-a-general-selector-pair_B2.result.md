# Idea 270 — is-S_CAGR-vs-S_SHARPE-a-general-selector-pair (lane B2, 2026-09-09)

**SECOND INDEPENDENT REPLICATION.** Idea 270 was answered by lane B (`..._B.py`, 5 dials x 12
panels, 348 arms) and replicated by cloud (`..._cloud.py`, 6 dials x 3 panels x 2 cost rungs,
174 arms) in the same session. This run was designed, executed and written before either was
visible on `main` (it was claimed from the same queue line and lost the push race), on a third
design: **5 dials x 4 panels x 2 cost rungs = 288 arms, plus a 40,774-cell census of the
record** — six times the census corpus lane B read. It is filed as a replication, not a new
answer. It **agrees with both on the verdict** and, because its census is an order of magnitude
larger and it measures the *mechanism* the other two only assert, it **adjudicates the one
structural point they disagreed about**. See the reconciliation section at the end.

**ANSWERED. The +2.53 pp / −0.0254 headline is NOT a general exchange rate. Two findings, in
the pre-registered order: (1) NOT-A-PRICE — on 4 of 5 dials the two selectors pick the SAME
arm, and where they differ the CAGR pick is more often FREE than paid for; (2) conditional
on a price existing at all, the rate is DIAL-SPECIFIC, spanning −4.3 to +297.8 pp of CAGR
per unit of Sharpe across the record's dial families (permutation p 0.031 / 0.0002).**
No RULES change, no KEEP-candidate, no memo. `RULES.md`, `scan.py`, `bot.py`, `baseline.py`
untouched.

Script `2026-09-09_is-S_CAGR-vs-S_SHARPE-a-general-selector-pair_B2.py`; outputs `.grid.csv`
(304 rows), `.walkforward.csv`, `.exchange.csv`, `.geometry.csv`, `.census.csv.gz` (40,774
cells), `.console.txt` (every number below).

## Reproduction gates (run before any new number was read)

The price caches are refreshed weekly: `data/prices.csv` now ends **2026-09-08**, two trading
days past idea 259's sample, **and carries restated adjusted closes for days it did see**.
Bit-identical reproduction is therefore impossible and claiming it would be false. The gate
is run at the parent's own sample end (`2026-09-04`) with a pre-declared tolerance of 1e-3:

* **[a]** `U56/EWall` max abs diff **1.267e-05** over 12 metric columns (its **closed**
  2009–2016 IS window alone moves **1.95e-06** — that is the size of the restatement);
  `U56/FWD20` **5.60e-07**. Live `RULES v1` from `engine.backtest`: 6.4194% / 0.66110 / −13.8278%.
* **[b]** the whole SIZE dial re-run at that date vs idea 259's committed `grid.csv`:
  28 cells × 12 columns + `sat_share`, max abs diff **1.533e-05** — and **exactly 0.00000000
  on B136, BSTK100 and SMALL439**; the residual is U56's restated cache alone. `sat_share`
  reproduces at 0.0 on all four panels.
* **[c]** idea 259's headline recomputes from its own committed `walkforward.csv`: pair
  disagrees **3 of 4** panels, mean dOOS_CAGR **+2.5348 pp**, mean dOOS_Sharpe **−0.025389**
  (published +2.53 / −0.0254).

**Gate [c] already decomposes the headline** and this is the first thing the run reports:
per panel dCAGR_pp {B136 +3.626, BSTK100 +3.010, SMALL439 0.000, U56 +3.503} and dSharpe
{B136 **+0.0437**, BSTK100 **+0.0306**, SMALL439 0.0000, U56 −0.1758}. The published
"−0.0254 of Sharpe" is **one priced panel, two panels where S_CAGR wins on BOTH metrics,
and one null**, averaged. It was never four panels paying a price.

## Tuned parameters (PROTOCOL rule 4)

Two: **(1)** the dial's own arm value, **(2)** the panel. All rungs and all four panels
reported. The DIAL FAMILY is the axis of the question, not a tuned parameter. Cost is
reported at both rungs (10 bps primary, 0 bps diagnostic), never chosen. `SAT_CAP`, `GROSS`,
`MAX_VOL`, `NS`, the composite key, the IS/OOS split and the panels are idea 259's constants,
imported verbatim; the no-cap sensitivity is reported too.

## Leg B — controlled 5-dial grid (288 arms × 2 cost rungs, one construction throughout)

| dial | cells | pair disagrees | priced (dSharpe<0) | free (dSharpe≥0) | mean dCAGR_pp | mean dSharpe | median rate |
|---|---|---|---|---|---|---|---|
| CADENCE | 4 | **0** | 0 | 0 | 0.0000 | 0.0000 | n/a |
| VOLGATE | 4 | **0** | 0 | 0 | 0.0000 | 0.0000 | n/a |
| GROSS | 4 | 1 | 0 | 1 | +1.2150 | +0.0001 | n/a |
| TRIM | 4 | 1 | 0 | 1 | +0.8244 | +0.0402 | n/a |
| SIZE | 4 | 3 | **1** | 2 | +2.5604 | −0.0242 | **21.07** |

**The selector pair is nearly degenerate off the SIZE dial.** On CADENCE both selectors pick
`CAD-M` on all four panels; on VOLGATE both pick `V-off` on all four; on GROSS and TRIM they
differ on one panel each and in both cases S_CAGR wins on *both* metrics. **The whole grid
contains exactly ONE priced cell — U56/SIZE — and its rate is 21.07, not the published 99.9.**
Pooled over 20 cells: dCAGR_pp **+0.9200, t +2.469, positive 5/20**; dSharpe **+0.00323,
t +0.262, positive 4/20** — i.e. across dials, selecting on CAGR costs *no* Sharpe on average.
Dropping `SAT_CAP` changes nothing (SIZE still the only priced cell). At 0 bps the picture is
the same shape with TRIM acquiring a priced cell at rate 0.54, so **the exchange is not a cost
artefact and not a cost-stable number either**.

## Leg B — the dial's own trade-off geometry (all arms, not just the two picks)

Regressing each dial's OOS CAGR (pp) on its OOS Sharpe *within* a panel gives the local
exchange the dial actually offers, independent of any selection:

| dial | median OOS slope (pp/Sharpe) | median Spearman(OOS Sharpe, OOS CAGR) | cells with ρ<0 |
|---|---|---|---|
| GROSS | **+1784.1** | +1.000 | 1 of 4 |
| VOLGATE | +23.8 | +0.893 | 0 of 4 |
| CADENCE | +18.8 | +0.800 | 0 of 4 |
| TRIM | **−5.1** | −0.218 | 3 of 4 |
| SIZE | **−9.4** | −0.321 | 3 of 4 |

Between-dial permutation on the slopes: spread of medians **1793.5 pp/Sharpe, p 0.0062**
(5 dials, 20 cells, 5,000 permutations, seed 270). **Sharpe and CAGR are not even ordered the
same way on different dials** — on GROSS, VOLGATE and CADENCE they move together (a "trade"
between them is a category error), and only on SIZE and TRIM do they oppose. The exchange
rate is a property of the dial's geometry, not of the selector pair.

## Leg A — census over the record (the queue's own instruction)

189 committed CSVs carry `IS_CAGR` + `IS_Sharpe` + `OOS_CAGR` + `OOS_Sharpe`. Scanning them
for swept dials (a non-metric column with ≥3 values inside a cell fixed by every other
non-metric key) yields **40,774 cells across 170 files and 61 distinct dial columns**, 0 files
skipped.

| family | cells | files | disagree | disagree % | priced | free | median rate | IQR |
|---|---|---|---|---|---|---|---|---|
| SIZE | 5,164 | 30 | 1,811 | 35.1% | 1,064 | 747 | **+297.8** | [12.6, 1732.5] |
| GROSS | 1,701 | 21 | 940 | 55.3% | 852 | 88 | **+45.3** | [19.4, 99.4] |
| COST | 4,203 | 29 | 72 | 1.7% | 54 | 18 | +20.5 | [1.7, 38.8] |
| OTHER | 29,090 | 156 | 8,459 | 29.1% | 5,575 | 2,884 | +4.6 | [−3.0, 22.0] |
| VOLGATE | 223 | 6 | 37 | 16.6% | 21 | 16 | +1.7 | [0.1, 3.1] |
| CADENCE | 393 | 5 | 28 | 7.1% | 20 | 8 | **−4.3** | [−8.6, 2.1] |

* Pooled disagreement **11,347 / 40,774 = 27.8%**; of those, priced 66.9%, free 33.1%.
* Conditional on disagreeing: dCAGR **+1.736 pp**, dSharpe **−0.0482**, aggregate rate
  **36.0** — a third of the published 99.9.
* S_CAGR wins OOS Sharpe in **32.3%** of disagreements, OOS CAGR in 77.1%. Full shape
  decomposition: **45.5% the queue's +CAGR/−Sharpe, 31.6% a free lunch (better on both),
  21.3% worse on both, 1.6% other** — **54.5% of disagreements are not a trade in either
  direction**.
* Rate over the 7,586 priced cells: median **9.94**, IQR **[−1.72, +39.58]**, deciles
  [−7.26, +241.38]. File-clustered (145 files with a rate): median **13.17**, IQR [3.44, 34.70],
  range −17.1 to +5950.7, **29 of 145 files negative**. Idea 259's **99.92 sits at the 84.6th
  percentile of cells and the 89.7th of files** and is OUTSIDE the pooled IQR; only 11.2% of
  cells land within a factor of two of it.
* Between-family permutation on the rates: spread of medians **302.2, p 0.0310** (named
  families) and **p 0.0002** including OTHER. Sign-split: CADENCE negative, the rest positive.

## Rule 8 — walk-forward (IS 2009–2016 chooses, OOS 2017–2026 read once)

Means over 5 dials × 4 panels at 10 bps:

| selector | OOS CAGR | OOS Sharpe | OOS MaxDD | beats RULES v2 | beats SPY |
|---|---|---|---|---|---|
| S_CAGR | **14.64%** | **0.8528** | −28.87% | 2/20 | 10/20 |
| S_SHARPE | 13.72% | 0.8496 | −28.20% | 2/20 | 10/20 |
| DEFAULT (do nothing) | 11.24% | 0.8455 | −24.82% | 0/20 | **15/20** |
| S_RAND | 11.91% | 0.7966 | −26.96% | 2/20 | 8/20 |
| RULES v2 (live) | 7.55% | **1.0268** | — | — | — |
| RULES v1 | 6.81% | 0.5957 | — | — | — |
| SPY | 15.43% | 0.8812 | — | — | — |

**S_CAGR weakly DOMINATES S_SHARPE out of sample** — +0.92 pp of CAGR *and* +0.0032 of Sharpe
— so on this grid the "price" is negative. What the CAGR selector actually pays is
**drawdown**: −28.87% vs −28.20% vs −24.82% for doing nothing. Both selectors beat a random
rung of the same pool (+0.05 of Sharpe) but **neither beats the live RULES v2 book** (2 of 20),
and **doing nothing beats SPY more often (15/20) than either selector does (10/20)** — a
further instance for idea 229's selection-loses pool.

## KEEP paths (PROTOCOL rule 4)

* **4a vs RULES v2 (the live book): 0 of 144 arms.** 4a vs the superseded v1: 30 of 144.
* **4b vs SPY: 22 of 144** (16 on U56, 6 on B136; SMALL439 and BSTK100 0 of 72 — the 16th and
  further reproductions of idea 136).
* **4a-v2 ∩ 4b = 0 arms. Nothing is promotable and no memo is written.**
* At 0 bps: 4a-v2 0/144, 4b 34/144. The 4b fail-bar census is led by `H1,H2,OOS,DD,CAGR` (34)
  and `DD` alone (30).
* Every 4b passer is an already-known row (U56 `FWD20/30/40`, `CAD-W/M`, `G0.625/0.750`,
  `V0.40–1.00`, `Q0.60–0.90`; B136 `EWall`, `FWD40/60`, `Q0.80–1.00`).

## What this changes

Nothing in RULES. The reportable consequence is a **reporting habit**, in the same register as
idea 259's own: **the +2.53 pp / −0.0254 exchange must not be quoted as a general conversion
between the two selectors.** It is (i) undefined on most dials, because the two selectors pick
the same arm; (ii) not a price in half the cases where they do differ; and (iii) where a price
exists, a dial-specific number spanning −4.3 to +297.8. A run that wants to claim a CAGR-vs-
Sharpe selection cost must measure it **on its own dial**.

## Caveats

* **Survivorship (rule 9):** `universe_broad.json` and the small panel are current
  constituents. Both selectors read the same panels, so the bias is common to the pair and
  cannot manufacture a *difference* between them; it does inflate the level of every OOS
  number above. No book here is proposed for capital.
* The census inherits 170 runs' construction choices and its `OTHER` family (29,090 cells,
  71%) is heterogeneous by definition; that is why leg B holds construction fixed, and the
  two legs agree on the direction of the answer.
* The grid's between-dial permutation could not be computed (only SIZE has a priced cell), so
  the DIAL-SPECIFIC leg rests on the census permutation and on leg B's independent geometry
  test (p 0.0062), not on the grid's rates.
* A cell rate is a ratio with a small denominator; it is heavy-tailed by construction, which
  is why medians, IQRs, file-clustering and a permutation test are reported instead of a mean.

---

## Reconciliation with the two sibling runs of idea 270 (same day, independent designs)

Three designs, three panel sets, three dial menus. What all three agree on:

* **The queue's premise is refuted.** The exchange rate is not a constant.
* **Disagreement is a minority event:** lane B 12/60 (20.0%), cloud 11/36 (30.6%), here
  **5/20 (25.0%)** on the controlled grid and **11,347/40,774 (27.8%)** on the record census.
* **Neither selector earns its keep.** Lane B: S_SHARPE −DONOTHING +0.0038 (t +0.31). Cloud:
  do-nothing 0.8956 beats both. Here: both beat a *random* rung of the same pool but neither
  beats the live RULES v2 book (2/20), and do-nothing beats SPY more often (15/20) than either
  selector (10/20).
* **The CAGR leg replicates in sign everywhere** (idea 259 +2.53 pp; lane B census +0.63 pp;
  cloud +1.49 pp; here, conditional on disagreement, **+1.736 pp** on 11,347 census cells).

**The point the siblings disagreed on, and what this run says about it.**

1. *Is it an "n-dial phenomenon"?* Lane B said yes (n 7/12 vs cadence 1/12); cloud said no
   (cadence 4/6, volcap 3/6, n 2/6). **This run's controlled grid sides with lane B** (SIZE 3/4,
   TRIM 1/4, GROSS 1/4, CADENCE 0/4, VOLGATE 0/4) and **so does the record census on 40,774
   cells** (disagreement rate GROSS 55.3%, SIZE 35.1%, OTHER 29.1%, VOLGATE 16.6%, CADENCE 7.1%,
   COST 1.7%) — but with GROSS, not SIZE, disagreeing most often in the record. So the *ranking*
   of dials is design-specific, exactly as cloud found; what is stable is that **CADENCE and
   COST sit at the bottom on every reading**.
2. *Is the Sharpe denominator an invariant?* Lane B reported it homogeneous at ≈−0.014
   (permutation p 0.31); cloud found it **positive** on its disagreeing cells (median +0.0073)
   and called the invariant unreproduced. **This run's census settles it in cloud's favour, at
   scale:** across 11,347 disagreements S_CAGR **wins** OOS Sharpe in **32.3%**, and the
   decomposition is **45.5% the queue's +CAGR/−Sharpe shape, 31.6% free lunch (better on both),
   21.3% worse on both, 1.6% other** — i.e. **a majority of disagreements is not a trade in
   either direction**.
   A denominator that is negative in only two-thirds of cases is not an invariant.
3. *Why does the dial identity matter at all?* Neither sibling measured this; cloud asserted
   that `gross` and `quantile` never disagree "mechanically, because Sharpe and CAGR are
   monotone in the same direction along both". **This run measures that claim and confirms it as
   the mechanism**: median Spearman(OOS Sharpe, OOS CAGR) along the dial is **+1.000 (GROSS),
   +0.893 (VOLGATE), +0.800 (CADENCE)** versus **−0.218 (TRIM), −0.321 (SIZE)**, and the per-dial
   OOS CAGR-on-Sharpe slope spans **+1784 to −9.4 pp per Sharpe point, permutation p 0.0062**.
   On three of five dials the two metrics move *together*, so a "trade" between them is a
   category error there; that, and not the selector pair, is what makes the rate dial-specific.

**Corpus note.** The census read the 189 qualifying CSVs present in `research/backtests` at the
time this run started; the two sibling idea-270 runs had not yet landed on `main` and are
therefore not in it. Re-running today would add at most their files and cannot move a 40,774-cell
distribution materially.

**Nothing here changes any of the three verdicts:** no KEEP, no memo, no RULES change, and
`RULES.md`, `PROTOCOL.md`, `scan.py`, `bot.py`, `baseline.py` untouched by all three.
