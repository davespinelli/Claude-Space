# Idea 522 (lane B) — how many of the record's 46 STRUCTURAL gates are CROSS-PANEL VINTAGE tests?

**Verdict: ANSWERED / 16 of 46 (34.8%) are cross-file and ALL 16 sit on a file pair the CACHE
REFRESH SCHEDULE currently decides — but the queue's framing is wrong twice over. (i) The 46 is an
OVER-COUNT: 24 of them are tolerance gates hiding behind a boolean name, so only 19 are genuinely
structural. (ii) Fixing the schedule would NOT make the panels agree — 15 of the 16 also sit on a
pair whose SHARED cells disagree, and that leg is code, not calendar.** No KEEP claimed, no book
promoted, no memo of a new candidate, no rule change. `RULES.md`, `PROTOCOL.md`, `scan.py`,
`bot.py`, `baseline.py` untouched (PROTOCOL rule 6).

Script: `2026-09-11_how-many-of-the-record-s-46-STRUCTURAL-gates-are-CROSS-PANEL-VINTAGE-tests_B.py`
Artefacts: `.clauses.csv` (46 rows, one per structural clause) · `.pairs.csv` (13 pair×test
decisions) · `.grid.csv` (2,316 panel×anchor×k book cells) · `.flips.csv` · `.walkforward.csv` ·
`.keeppaths.csv` · `.console.txt`. Deterministic: `PYTHONHASHSEED=1` and `=2` give byte-identical
console and CSVs.

## Parameters (two, as the queue allows; every grid point reported)

* **P1 CLASS**, 3 nested readings of "cross-file index/shape test": **NARROW** (the clause's own
  expression is an index/shape/set predicate AND its resolved closure reads ≥2 input panel files),
  **MID** (the *resolved closure* carries the predicate AND ≥2 files), **WIDE** (≥2 files, any
  predicate form). NARROW ⊆ MID ⊆ WIDE, asserted, 0 violations.
* **P2 STALENESS k ∈ {0, 3, 9, 21}** trading days a panel's cache lags "today" (book leg). k=3 is
  the gap actually on disk today.

Reported TREATMENTS, not selected on any outcome, every cell published: PANEL {U56, B136,
SMALL483} and the file pairs the census finds. Dataflow depth (6), the over-approximating
union-every-assignment closure and the book's fixed configuration (band ±3%, gross 1.00, weekly,
10 bps, next-day execution) are FIXED and not swept. The rule-8 selector only ever picks k.

## Pre-registered reproduction gates (printed before any census number was read)

| gate | result |
|---|---|
| **G1** idea 515's published counts off its own `.clauses.csv` | **PASS** — 520 rows, tolerance 345, exact 87, structural 46, count 40, scripts 151, all as published. *Residual found and reported, not corrected:* 345+87+46+40 = **518**, not 520; idea 515's published breakdown silently omits 2 `floor` clauses. |
| **G2** the exemplar, crypto-sleeve L406 `px.index.equals(pxb.index)` | **PASS** — fails as-cached; PRICES-only days are exactly `2026-09-08, 09-09, 09-10`; BROAD-only days `[]`; truncating PRICES to BROAD's last close makes it **True**. |
| **G3** shared-CELL agreement (the "tail-only" hypothesis) | **FAIL — H0 rejected, and this is the finding.** See below. |
| **G4** truncation ≡ prefix | **PASS** — max\|Δ daily return\| **0.000e+00** at 4 cut points, so the anchor×k grid is sliced, not re-run. |
| **G5** identify the standing 4b candidate's frame convention | **PASS** — the memo's five U56 numbers (11.55% / 1.2067 / −15.70% / 1.2405 / 1.1798) reproduce **SPY-FREE** to **4.95e-05** and NOT SPY-in-frame (8.71e-03). Idea 740 said the LEADERBOARD cannot identify its own comparand; the memo's digits can, and this one is `SAMEv2_noSPY`. |

**G3 in full.** PRICES vs PRICES_BROAD share 4,699 rows × 56 columns = **253,159 cells**;
**214,065 (84.6%) disagree by more than 1e-6 relative**, max 3.627e-02. Decomposed:
`prices_broad.csv` is written at **2 decimals** against `prices.csv`'s 4, which accounts for most
of it — but **5,696 cells (2.25%) disagree BEYOND that rounding**, and they are one name:
**GOOGL 4,488**, then NFLX 114, AMZN 100. GOOGL's broad/primary ratio has median **1.000644**
(min 1.000000, max 1.001368) across the *whole* history — a back-adjustment-factor restatement
between two caches downloaded at different times, not a tail. The other two panel pairs share zero
columns, so no cell test exists for them.

## [A] The census — the 46 are not what the label says

* **46 / 46 located in source.**
* Only **7 of 46** have an index/shape/set predicate in the clause's own expression. The other
  **39 read `assert ok` / `assert g6` / `assert not bad`** and say nothing at the clause — which is
  why idea 515's clause-level classifier called them structural.
* Once the closure is resolved, **24 of 46 carry a numeric tolerance** — they are **tolerance
  gates misfiled as structural**. Example: `2026-09-05_band-width-at-g085_cloud.py:220` is
  `assert ok` where `ok = all(abs(a-b) < 6e-3 …)` against idea 84's published rows.
* **Genuinely structural once resolved: 19 of 46.** Idea 515's "8.8% of gates are structural" is
  therefore an upper bound; the resolved figure is **19/520 = 3.7%**.

| P1 class | n | share of 46 |
|---|---|---|
| NARROW | **4** | 8.7% |
| MID | **16** | 34.8% |
| WIDE | **16** | 34.8% |

MID and WIDE coincide: every clause in the record that touches ≥2 panel files also carries a
structural predicate somewhere in its closure. File pairs found: `PRICES|PRICES_BROAD` 12 clauses,
`PRICES|PRICES_BROAD|PRICES_SMALL` 3, `PRICES|PRICES_SMALL` 1. No clause pairs a price panel with
`volume_small`, `small_meta`, `earnings_dates`, `form4_purchases` or `spinoffs`.

## [B] Schedule-decided or code-decided? (re-executed on today's files)

13 (pair × test) cells: **SCHEDULE 10 · INERT 2 · CODE 1.** Every `index.equals` and `shape[0]`
test across dated panels is SCHEDULE (fails as-cached, passes on the common index); the only INERT
pair is `PRICES_SMALL|VOLUME_SMALL`, which is written by one script in one pass. The single CODE
cell is the **value** test `PRICES|PRICES_BROAD cells@1e-6`.

The answer to the queue, at all three classes:

| class | cross-file clauses | on a pair the SCHEDULE decides | also on a pair whose CELLS disagree |
|---|---|---|---|
| NARROW | 4 | **4** (8.7% of all 46) | 3 |
| MID | 16 | **16** (34.8% of all 46) | 15 |
| WIDE | 16 | **16** (34.8% of all 46) | 15 |

So the queue's premise is confirmed for the index leg and **refuted as a remedy**: re-caching
`prices_broad.csv` on the same day as `prices.csv` would silence 10 of 13 gate cells and leave the
one that compares numbers still failing, on 84.6% of the shared cells and on 2.25% of them beyond
any rounding. A clause that reads `assert px.index.equals(pxb.index)` and then *joins the two
panels* — which is exactly what crypto-sleeve L406 does — is checking the cheap half.

## [C] What the refresh schedule is worth to a BOOK (2,316 cells)

Book = the band book at gross 1.00 (the standing 4b candidate) on each panel; 4a comparand =
RULES v2 (same clause at gross 0.75) on the same panel and the same truncated window; 4b comparand
= SPY. Anchor = a month-end "today"; staleness k = the cache ends k trading days before it.
Everything here is SPY-in-frame (`baseline.compare`'s own convention) for book *and* comparand;
per G5 that is −0.0071 Sharpe / +0.21 pp MaxDD against the memo's SPY-free numbers, common to
every cell.

**Full-sample reading at each k** (anchor = the panel's own last close):

| panel | k | end | CAGR | Sharpe | MaxDD | H1/H2 | v2 Sharpe | SPY Sh | 4a | 4b |
|---|---|---|---|---|---|---|---|---|---|---|
| U56 | 0 | 2026-09-10 | 11.52% | 1.1996 | −15.91% | 1.235/1.171 | 1.1998 | 0.8835 | n | **Y** |
| U56 | 3 | 2026-09-04 | 11.59% | 1.2055 | −15.91% | 1.226/1.190 | 1.2056 | 0.8890 | n | **Y** |
| U56 | 9 | 2026-08-27 | 11.61% | 1.2068 | −15.91% | 1.225/1.194 | 1.2070 | 0.8901 | n | **Y** |
| U56 | 21 | 2026-08-11 | 11.59% | 1.2042 | −15.91% | 1.223/1.191 | 1.2043 | 0.8913 | n | **Y** |
| B136 | 0 | 2026-09-04 | 10.72% | 1.1057 | −16.16% | 1.230/0.983 | 1.1058 | 0.8890 | n | **Y** |
| B136 | 21 | 2026-08-06 | 10.75% | 1.1064 | −16.16% | 1.227/0.988 | 1.1065 | 0.8908 | n | **Y** |
| SMALL483 | 0 | 2026-09-04 | 5.35% | 0.6143 | −15.91% | 0.542/0.679 | 0.6146 | 0.8615 | n | n |
| SMALL483 | 21 | 2026-08-06 | 5.36% | 0.6154 | −15.91% | 0.549/0.676 | 0.6157 | 0.8635 | n | n |

**Decision power over books — k>0 against the fresh k=0 reading, over every anchor:**

| panel | k | anchors | med \|ΔSharpe\| | max \|ΔSharpe\| | med \|ΔCAGR\| pp | max \|ΔDD\| pp | 4a flips | **4b flips** |
|---|---|---|---|---|---|---|---|---|
| U56 | 3 | 201 | 0.0058 | 0.0989 | 0.063 | 0.351 | 0 | **4** |
| U56 | 9 | 201 | 0.0109 | 0.4674 | 0.112 | 1.575 | 0 | **11** |
| U56 | 21 | 201 | 0.0195 | 0.6464 | 0.191 | 5.459 | 0 | **15** |
| B136 | 3 | 201 | 0.0054 | 0.1324 | 0.062 | 0.711 | 0 | **2** |
| B136 | 9 | 201 | 0.0095 | 0.4699 | 0.109 | 1.731 | 0 | **7** |
| B136 | 21 | 201 | 0.0188 | 0.6565 | 0.195 | 5.699 | 0 | **12** |
| SMALL483 | 3/9/21 | 177 | 0.0072/0.0125/0.0227 | 0.0901/0.1550/0.3505 | 0.070/0.111/0.209 | 0.000/0.484/1.768 | 0 | **0** |

**The cache schedule alone decides a published 4b verdict on 4 of 201 U56 month-ends at today's
actual 3-day lag (2.0%), 15 of 201 (7.5%) at a 21-day lag**, and never decides a 4a one. The
binding leg is almost always the **CAGR floor** (U56 k=9 and k=21: 11 of 11 and 15 of 15 flips are
CAGR; k=3: 3 CAGR + 1 H2+CAGR), which is the same leg ideas 733 and 541 found binding — a
month-end SPY number moves the 70%-of-SPY floor more than it moves the book. SMALL483 never flips
because it fails 4b at every k by a wide margin.

## [D] Rule 8 walk-forward — k chosen on IS anchors (≤ 2016-12-31) alone

Pre-stated selector: highest mean Sharpe over IS anchors, ties (<1e-9) to the smallest k. The dial
is **discriminated, not degenerate** (no ties): IS picks **k=21** on U56 (1.153827 vs 1.139708 at
k=0) and B136 (1.131663 vs 1.118781), **k=0** on SMALL483 (0.343364 vs 0.325057 at k=21). 2017–2026
read once, every rung reported:

| panel | k | | oCAGR | oSharpe | oMaxDD | v2 oCAGR | v2 oSh | SPY oCAGR | SPY oSh | SPY oDD | 4a | 4b |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| U56 | 0 | | 12.66% | 1.2740 | −15.91% | 9.45% | 1.2747 | 15.24% | 0.8721 | −33.72% | n | **Y** |
| U56 | 3 | | 12.78% | 1.2844 | −15.91% | 9.53% | 1.2851 | 15.45% | 0.8820 | −33.72% | n | **Y** |
| U56 | 9 | | 12.82% | 1.2869 | −15.91% | 9.56% | 1.2877 | 15.51% | 0.8840 | −33.72% | n | **Y** |
| U56 | 21 | **\*** | 12.79% | 1.2825 | −15.91% | 9.55% | 1.2833 | 15.58% | 0.8861 | −33.72% | n | **Y** |
| B136 | 0 | | 10.66% | 1.1174 | −16.16% | 7.98% | 1.1185 | 15.45% | 0.8820 | −33.72% | n | n |
| B136 | 21 | **\*** | 10.71% | 1.1188 | −16.16% | 8.02% | 1.1199 | 15.57% | 0.8852 | −33.72% | n | n |
| SMALL483 | 0 | **\*** | 5.98% | 0.6619 | −15.91% | 4.55% | 0.6629 | 15.45% | 0.8820 | −33.72% | n | n |
| SMALL483 | 21 | | 6.01% | 0.6639 | −15.91% | 4.57% | 0.6650 | 15.57% | 0.8852 | −33.72% | n | n |

**The OOS verdict is staleness-INVARIANT everywhere** — U56 passes 4b at all four rungs, B136 and
SMALL483 fail at all four — even though the anchor-by-anchor verdict is not. The schedule moves
*which month-end you happen to publish on*, not the ten-year conclusion. That is the honest
reading: the gates are schedule-decided, the books are not.

## KEEP paths

* **4a: 0 / 2,316** anchor-cells and **0 / 12** OOS cells, on every panel and every k. The band
  book's Sharpe is gross-invariant (idea 733), so raising gross can never beat RULES v2 on the 4a
  comparand — this run adds 2,316 more cells saying so.
* **4b: 1,063 / 2,316** anchor-cells (U56 436/804, B136 627/804, SMALL483 0/708) and **4 / 12**
  OOS cells, all four of them U56.
* **No new KEEP-candidate.** The only 4b passer here is the *already-standing* U56 band-book-at-
  gross-1.00 candidate (idea 733, memo `2026-09-11_u56-v2band-gross100_4b_cloud_MEMO.md`),
  reproduced to 4.95e-05 by G5. This run adds a robustness leg to it and an identification of its
  frame convention; both are filed as an **amendment (line 9c) to that memo**, not as a new claim.

## What this run proposes (NOT applied — PROTOCOL rule 6)

1. **Infrastructure, not rules:** cache `prices.csv` and `prices_broad.csv` in the same pass, or
   make every cross-panel read go through a common-index intersection. This is the *same* defect
   idea 353 (still open, LOCAL ONLY) names for `cache_prices.py`.
2. **A gate-writing clause:** a cross-panel structural gate should state which leg it tests. An
   `index.equals` between two independently refreshed caches is a calendar assertion; if the script
   then joins the panels it also needs a **value** check, which today would fail on 84.6% of shared
   cells and on 2.25% beyond write rounding.
3. **A correction to idea 515's census:** report the 46 as "structural *at the clause*", since 24
   of them resolve to tolerance gates; the resolved count is 19.

## Caveats

`universe.json` and `universe_broad.json` are **current** constituents (survivorship favours trend
sleeves); `prices_small.csv.gz` likewise — see `data/SMALL_PANEL_README.md`. The census closure
deliberately over-approximates (it unions every assignment to a name anywhere in the file), so the
cross-file counts are upper bounds on what any single execution path reads. Only 2020 and 2022 are
real stress tests in the book leg. The staleness ladder truncates the *tail* only; a cache that is
stale in the middle of the sample is not tested here and cannot be, since every panel on disk is
contiguous.
