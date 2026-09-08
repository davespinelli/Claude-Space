# Idea 435 — is the untreated BASE BOOK the only thing passing 4b in the overlay corpus?

**Verdict: ANSWERED, premise NEGATIVE but the correction is large. No KEEP, no RULES change,
PROTOCOL untouched.** The base book is *not* the only thing passing 4b — but 40% of the
overlay corpus's 4b passes are pure carrier, and every one of the remaining 60% is a
de-grossing event on a carrier that fails 4b on the drawdown bar alone.

Script: `2026-09-08_is-the-BASE-BOOK-the-only-thing-passing-4b-in-the-overlay-corpus_cloud.py`
Costs 10 bps, next-day execution, weekly cadence, warm-up 260 days. Deterministic, no network.

## The decomposition the idea asks for

For an overlay arm carried on base book C:

| | carrier passes 4b | carrier fails 4b |
|---|---|---|
| **arm passes 4b** | CARRIED | INCREMENTAL |
| **arm fails 4b** | DESTROYED | both fail |

Only INCREMENTAL is an instrument result.

## LEG B — fresh corpus (the untreated carrier exists by construction)

3 panels (u56 / broad136 / small439) x 4 base books (EWALL, MA200, BAND3, TOP20) x 2 gross
(0.75, 1.00) = **24 carriers**; 6 overlay families (GATE, DDCTL, BUDGET, STOP, VOLTGT, LAM)
x 2 pre-registered levels = **288 overlay arms**. Two swept parameters: overlay level and
carrier gross; panel/book/family are corpus dimensions, all reported.

| | count |
|---|---|
| carriers passing 4b **untreated** | **3 / 24** (u56 MA200 g=1.00, u56 BAND3 g=1.00, broad136 BAND3 g=1.00 — all binding on CAGR, margins 0.0031 / 0.0093 / 0.0006) |
| carriers passing 4a untreated | 0 / 24 |
| overlay arms passing 4b | **50 / 288** |
| — CARRIED | 20 |
| — INCREMENTAL | 30 |
| — DESTROYED (carrier passes, arm fails) | 16 |
| **incremental share of overlay 4b passes** | **30/50 = 0.6000** |
| **net 4b passes created by the whole corpus** | **30 − 16 = +14** |
| arms passing BOTH paths | **0 / 312** |

By panel: u56 34 passes (16 carried / 18 incremental / 8 destroyed), broad136 16 (4/12/8),
**small439 0 of 96** — the thirteenth-plus reproduction of idea 136's small-panel wall.
By family: VOLTGT 14 passes (12 incremental), STOP 9 (8), GATE 8 (7), DDCTL 7 (2), LAM 7 (1),
BUDGET 5 (0 — every BUDGET pass is carried).

## The correction: the incremental passes are de-grossing, and their margins are grid dust

* **30 of 30** incremental arms hold LESS mean gross than their carrier (k in [0.695, 1.000]).
* **29 of 30** sit on carriers whose ONLY failing 4b bar is **DD** (the 30th is CAGR).
* LEG C prices a **matched-gross carrier control** for every arm — the untreated carrier
  scaled to the arm's own mean gross, no overlay:
  * the control **also passes 4b in 5 of the 30** incremental cells — those are pure gross
    placements, exactly idea 311's finding;
  * of the 25 that survive, the control fails on **DD in 24** — so what the overlay actually
    buys is *path-dependent* drawdown shaping over *constant* de-grossing, and it buys it by
    a median m_min of 0.0094 (min 0.0004, max 0.0255);
  * across all 288 arms the overlay **loses** to its own matched-gross control on Sharpe in
    203 of 288 cells (mean dSharpe **−0.0244**, mean dOOS **−0.0216**); 4b passes 50 (arms)
    vs 34 (matched-gross controls).
  * Per family, only LAM (+0.0049) and BUDGET (−0.0005) are roughly neutral; STOP is
    −0.0814 dSharpe / −0.1126 dOOS.

## Rule 8 (required) — level chosen on IS ≤ 2016-12-31, 2017-2026 read once

144 cells (panel x book x gross x family).

| | value |
|---|---|
| IS-chooser mean dOOS Sharpe vs the untreated carrier | **−0.0084** (t −1.47, wins 56/144) |
| ORACLE-OOS headroom over the carrier | **−0.0034** (positive in 64/144) |
| IS-chosen arm passes 4b | 28/144; its carrier passes in 18/144; of the 28, **15 incremental** |

Per family: GATE +0.0439 (20/24 wins) is the only positive; STOP −0.0795, DDCTL −0.0131,
LAM −0.0045, VOLTGT +0.0003, BUDGET +0.0024. Per panel: u56 +0.0102, broad136 +0.0114,
small439 −0.0469. **The ladder has negative oracle headroom overall**, so on this corpus the
selector-loses finding is again measured where there is nothing to find.

Comparands (post-warm-up, 10 bps): SPY 15.23% / 0.8890 / −33.72% on u56 and broad136,
14.13% / 0.8615 / −33.72% on small439. RULES v2 8.66% / 1.2056 / −12.05% (u56),
8.03% / 1.1058 / −12.24% (broad136), 3.80% / 0.5710 / −14.70% (small439).

Best 4b arm by margin: u56 TOP20 g=0.75 + VOLTGT(0.15) — 13.21% / 1.1018 / −16.37%,
H1 1.2090 / H2 1.0170, OOS Sharpe 1.0943, OOS CAGR 13.82%, m_min 0.0255 on CAGR. It fails 4a.

## LEG A — archival census over the committed record

1,664 CSVs scanned; 361 carry a 4b pass column; 282 of those have no dial with an explicit
OFF/none/control level, so their carrier row is not present in the same file and they cannot
be paired mechanically. **79 files qualify**, giving 31,588 paired treated rows (15,319 more
treated rows were dropped because their carrier group has no OFF row — reported, not hidden):

| | count |
|---|---|
| CARRIED | 1,679 |
| INCREMENTAL | 1,938 |
| DESTROYED | 2,461 |
| both fail | 25,510 |
| **archival incremental share of overlay 4b passes** | **1,938 / 3,617 = 0.5358** |

The archive's 53.6% and the fresh corpus's 60.0% agree, from independent constructions.
**But the archive also says the record's overlays DESTROY more 4b passes than they create
(2,461 destroyed vs 1,938 incremental, net −523)** — the fresh corpus is net +14 only because
its carriers were chosen to include three that already pass.

## What the record should take from this

1. `is-idea-2-s-BASE-BOOK-the-only-thing-passing-4b` is **false as stated**: ~55-60% of
   overlay 4b passes are not the carrier's.
2. It is nevertheless **right in spirit**: a published "N of M arms clear 4b" is
   uninterpretable without the untreated carrier's own verdict beside it, because 40-46% of
   the passes are the carrier, and the incremental remainder is a de-grossing move whose
   margin is smaller than one grid step of the gross dial.
3. Proposed (report-only, PROTOCOL untouched): any overlay run should publish, beside its
   4b count, (a) the untreated carrier's own 4b verdict and (b) the matched-gross carrier
   control's 4b verdict. On this corpus those two columns strip 20 of 50 and a further 5 of
   30, leaving 25 passes whose entire content is "path-dependent de-grossing beat constant
   de-grossing on MaxDD by ≤0.03".

**SURVIVORSHIP:** small439 is current constituents of a sub-$2B screen with `max_1d_move ≥ 1.0`
names dropped (44 of 483); broad136 is current constituents of a large-cap list. The panel
ordering u56 > broad136 > small439 inherits that bias.
