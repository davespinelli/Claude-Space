# Idea 622 — census the record's PARKs for the DATA SEARCH ERROR  (cloud, 2026-09-10)

**Verdict: ANSWERED (the census) + KILL (the back-fill).  The search error was real, SINGULAR,
and worthless.**  Of the four distinct objects the record's data-PARKs are waiting on, the
whole-repo scope recovers **one** — the one already lifted on 2026-09-10 — and it is a terminal
snapshot that reaches no panel but SMALL439.  Script:
`2026-09-10_census-the-record-s-PARKs-for-the-DATA-SEARCH-ERROR_cloud.py`.

Params: **P1 park set** (STRICT / WIDE), **P2 search scope** (`data/`-only / whole repo).  PART C
carries one tuned parameter (the sector cap m, chosen by rule 8 alone); granularity, cadence and
the cost rungs are reported axes.  All 28 cap grid points are in `.capgrid.csv`.

## GATES
| gate | result |
|---|---|
| G1 segment runner vs `engine.backtest`, D and W | max\|dr\| **6.1e-16**, max\|dto\| **2.8e-16** |
| G2 cost-rung identity vs live `engine.backtest(25)` | **6.1e-16** |
| **G3 REPRODUCTION** of the queue's own claim | `universe_under2b.csv` covers **430 of the 439** SMALL names — counted, not restated |
| G4a cap m = 20 vs an un-capped top-20 on the same tie-break | **0.000e+00** |
| G4b the same book on pandas `rank()` instead | differs on **3 026 of 3 934 days**, max\|dr\| 5.2e-04 — *reported, not gated*: the composite ties and the two tie-breaks hold different names |
| **G5** the recovered provider's own vintage | **TERMINAL-DATED: 3 distinct as-of periods across all names** |

## PART A — the PARK census

| park set | distinct PARKs | stated reason is a DATA shortage | matches the record's own phrase | names a recoverable series |
|---|---|---|---|---|
| STRICT (verdict cell / QUEUE `## Done`) | 253 | **13 (5.1 %)** | 6 | 6 |
| WIDE (any committed line) | 752 | **29 (3.9 %)** | 18 | 18 |

813 PARK sentences harvested across QUEUE.md, LEADERBOARD.md, CHANGELOG.md and every
`backtests/*.result.md`.  The 10 de-duplicated DATA-PARKs that name a series collapse to **four
distinct parked objects**: idea 193/195's MCAP leg (shares outstanding, 4 occurrences), the
point-in-time **megacap** panel (shares + delisted prices, 3), idea 37's index-deletion-reversal
(index membership, 2), and the delisting-aware small panel (delisted prices, 2).

## PART B — resolution under both scopes, with the DATING test

| series | PARKs | raw match in `data/` | **audited** in `data/` | outside `data/` | provider | dating | search error |
|---|---|---|---|---|---|---|---|
| shares_outstanding | 6 | 2 | **0** | 3 | deepvalue | **SNAPSHOT** | yes |
| market_cap_PIT | 3 | 0 | 0 | 3 | deepvalue | **SNAPSHOT** | yes |
| delisted_prices | 4 | 0 | 0 | **0** | — | — | **no — genuinely absent** |
| index_membership | 2 | 0 | 0 | **0** | — | — | **no — genuinely absent** |
| *sector* (used by PART C; **no PARK names it**) | 0 | 1 | 0 | 3 | deepvalue | SNAPSHOT | — |

**The provider audit is itself a finding.** A bare column-name search accepts
`data/form4_purchases.csv:shares` as "shares outstanding" — it is an insider *transaction* size —
and `data/spinoffs.csv:sic` / `research/tenders/history.csv:sic` as a sector map for the panel.
Requiring a one-row-per-ticker table rejects all four.  **A wider search reproduces the same class
of error in the other direction**, so "re-check against the whole repo" needs a semantic gate, not
just a wider glob.

**Three further facts that decide the answer:**
1. `shares_outstanding` and `market_cap_PIT` are **the same object** — mktcap is price × shares
   out of one snapshot — so the recovered set is **one** parked object, not two.
2. That object is **SNAPSHOT-dated (3 as-of periods across all names)**, i.e. claimable only into
   the lookahead idea 623 is in the queue about, and idea 195's 2026-09-10 lift already killed it
   as a leak (|IC| 0.6959, OOS 1.584).
3. **Panel reach:** the provider covers **0 of 55** u56 names, **0 of 135** broad136 names and
   **430 of 439** SMALL439 names.  It is a sub-$2B screen, so it **cannot** lift the
   point-in-time-**megacap**-panel PARK even in principle.

**How many are claimable today: ZERO NEW ONES.**  One of four objects was a `data/`-scope search
error; it was found and spent on 2026-09-10; the other three (megacap PIT panel, index membership,
delisted prices) survive the whole-repo re-check as genuine data absences.

## PART C — pay the census off: the one time-safe thing the wider scope adds

The wider scope's only addition is a terminal snapshot of name-level attributes.  Its most
time-stable member is the SIC code, which no PARK ever named and the record has never used.  Run
as a **sector cap** on the SMALL439 top-20 equal-weight book (the 2026-09-04 KEEP 4b family), at
10 bps, weekly, with idea 621's NO-DIAL control on every row:

| grain | cap m=1 | 2 | 3 | 4 | 5 | 8 | **20 (NO CAP)** |
|---|---|---|---|---|---|---|---|
| SIC2 (53 groups) Sharpe | 0.657 | 0.689 | 0.725 | 0.762 | 0.771 | 0.768 | **0.768** |
| SIC2 CAGR | 11.3 % | 12.6 % | 13.5 % | 14.5 % | 14.8 % | 14.7 % | **14.7 %** |
| SIC2 MaxDD | −35.0 % | −31.5 % | −30.8 % | −31.5 % | −30.9 % | −30.9 % | **−30.9 %** |
| DIV (9 divisions) Sharpe | 0.490 | 0.561 | 0.739 | 0.725 | 0.699 | 0.720 | **0.768** |

**Rule 8 (cap chosen on 2010–2016 IS Sharpe, 2017–2026 read once), 16 cells (2 grains × 2 cadences
× 4 rungs): the chooser beats the NO-DIAL control in 1 of 16, median −0.0317.**  The two headline
cells: SIC2/W picks m = 4 and gets OOS **0.7791** against no-cap's **0.8095**; DIV/W picks m = 5
and gets **0.6253** against **0.8095** — the cap costs **0.18 of Sharpe** out of sample.  The OOS
oracle is m = 20 (no cap) in 5 of 16 cells.

Comparands, same window — full sample: SPY **14.13 % / 0.8615 / −33.72 %** (H 0.891/0.858),
RULES v2 **3.81 % / 0.5725 / −14.68 %** (H 0.570/0.577); the un-capped book 14.67 % / 0.7678 /
−30.85 % (H 0.870/0.722).  OOS 2017–2026: SPY 15.45 % / 0.8820 / −33.72 %, RULES v2
3.85 % / 0.5680 / −14.68 %, un-capped book 17.11 % / 0.8095 / −30.85 %.

**KEEP paths (PROTOCOL 4, both priced on every arm, 10 bps): 4a 0/28, 4b 0/28 — chooser arms
0 and 0, no-dial arms 0 and 0.**  The DD leg fails everywhere (−30.9 % against 4b's cap of
0.60 × SPY = −20.2 %) and no sector cap moves it; the binding constraint is the 20-name book's
concentration, not its sector mix (ideas 527/531 again).

## The answer to the queue's question
**One PARK in the record was a search error, and it has already been spent.**  The queue's
generalisation — that the record is sitting on claimable PARKs it never looked for — does not
survive its own census: of four distinct data-PARK objects, three are genuinely absent from every
directory, and the fourth reaches only the panel it was already spent on and only through a
terminal-dated snapshot.  The transferable lesson is narrower and better: **a PARK justified by
missing data should name the SCOPE it searched and the DATING the series would have**, because
scope alone turns one PARK into a leak (idea 623) and a wider scope without a semantic gate turns
an insider-transaction column into a shares-outstanding series.

## Caveats carried
* SURVIVORSHIP twice: SMALL439 is current constituents (idea 54) with 44 tickers dropped for
  `max_1d_move >= 1.0`, **and** the sector labels come from a screen of names that are under $2B
  *today*, so the sector map is itself a terminal snapshot.  A SIC code is far more time-stable
  than a share count; "far more" is not "invariant", and PART C's numbers carry that.
* Idea 623: a terminal-dated key beats rule 8 by construction, so no SNAPSHOT-backed PARK is
  called "claimable" here without the qualifier.
* The census classifies FILES AND SENTENCES, not claims (idea 534); WIDE is an upper bound.
  Both park sets are reported and never merged.
* Idea 321 (MaxDD is one path), idea 126 (t+1, 10 bps).
* G4b: the composite ties often enough that the tie-break rule moves the book on 77 % of days at
  max\|dr\| 5.2e-04 — small, but it means "top-20 of the composite" is not one book in this repo.
