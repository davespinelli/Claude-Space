# Idea 514 — stamp every committed artefact with its PANEL VINTAGE (cloud, 2026-09-09)

**ANSWERED. The premise is CONFIRMED, the proposal is drafted, and the back-fill is BOUNDED BY THE
CLONE, not by the record. No RULES change, no book promoted, no KEEP claimed; RULES.md, PROTOCOL.md,
scan.py, bot.py and baseline.py untouched.**

Script: `research/backtests/2026-09-09_stamp-every-committed-artefact-with-its-PANEL-VINTAGE_cloud.py`
(327 s, deterministic, no network). Artefacts: `.console.txt`, `.stamps.csv`, `.census.csv`,
`.vintage_sidecar.csv`, `.grid.csv`, `.flips.csv`, `.walkforward.csv`.

## A. The stamp, and why it goes on the PANEL not the FILE

`panel_stamp(px)` = `(first_date, last_date, n_rows, n_cols, panel_sha)`, where `panel_sha` is
sha256 over a canonical encoding of the object the backtest actually consumes — index as int64 ns,
columns sorted, values float64 C-order — truncated to 16 hex. It moves on an appended row, on a
restated cell and on a column-set change; it does not move on read order, dtype width or CSV
formatting.

| object | first | last | n_rows | n_cols | panel_sha |
|---|---|---|---|---|---|
| PANEL U56 | 2008-01-02 | **2026-09-08** | 4700 | 56 | `fabfd5b814808b76` |
| PANEL B136 | 2008-01-02 | **2026-09-04** | 4699 | 136 | `e660835829f4a3c3` |
| PANEL SMALL439 | 2010-01-04 | **2026-09-04** | 4194 | 440 | `e857282e3e67ec9a` |
| FILE data/prices.csv | | | | 58 | `68548b1de3629415` |
| FILE data/prices_broad.csv | | | | | `a1db76ae968c017d` |
| FILE data/prices_small.csv.gz | | | | | `bc832ada6461349b` |

Two facts fall straight out and neither is in the record:

1. **The three panels are at DIFFERENT vintages on the same day** (U56 ends 2026-09-08, B136 and
   SMALL439 end 2026-09-04 — the broad/small caches refresh weekly, only `data/prices.csv` is
   touched by the daily job). So a run date does **not** identify a vintage, and a multi-panel
   artefact has more than one.
2. **The file sha is not the panel sha.** U56 is `data/prices.csv` minus `EXCLUDE`, restricted to
   `universe.json`, ffilled; SMALL439 is the gz panel minus the 44 `max_1d_move >= 1.0` names plus a
   reindexed SPY column. Stamping the file would not identify the panel that was consumed.

## B. Census — the premise is confirmed, and it is a zero

3,784 committed artefact files under `research/backtests/` + `research/reports/` (474 `.py`,
2,249 `.csv`, 550 `.md`, 452 `.txt`, 59 other):

| test | count | share |
|---|---|---|
| any vintage-ish token (`vintage`/`last_date`/`n_rows`/`panel_sha`) | 75 | 1.98% |
| contains a **current panel last_date** string | 986 | 26.06% |
| contains a **current panel n_rows** as a standalone integer | 105 | 2.77% |
| contains a **current panel sha** | **1** | 0.03% |

The one sha hit is **this run's own `.stamps.csv`**, so the honest figure is **0 of 3,783**
pre-existing artefacts carrying a verifiable vintage. The middle two rows are upper bounds — a file
can print `2026-09-08` or `4700` for an unrelated reason — and they are the only thing the record
has today: a date somewhere in a console log, unlabelled, un-asserted, and absent from every CSV
schema.

## C. Back-fill — reconstructible in principle, not in this sandbox

- clone is **shallow: true**, **50 commits**, window `2026-09-08T23:26:54Z .. 2026-09-09T08:37:32Z`.
- 3,782 of 3,784 artefacts (99.95%) have a last-touching commit inside that window, so the
  path→commit map is complete; but **only 2 distinct `data/prices.csv` blobs are reachable**, i.e.
  the clone spans **exactly one real vintage step**. `prices_broad.csv` and `prices_small.csv.gz`
  have **one** blob each — zero steps.
- Priced exactly: newer blob `048a4741f36b` (4700 rows) vs older `031a3a69e522` (4699 rows) —
  **1 appended row, 23,055 restated cells in 46 of 58 columns, max |d| 3.000e-04**. This reproduces
  idea 513's read of the same daily-close job independently.

**So: the mechanism (artefact commit → panel blob at that commit) is correct and needs no new data,
but a shallow cloud clone can back-fill only the artefacts committed within its own window. The
sidecar `.vintage_sidecar.csv` is written for those; anything older needs a full clone, which is why
the stamp must be written AT COMPUTE TIME rather than recovered later.**

## D. What an unknown vintage costs, in PROTOCOL units

Two tuned parameters, both reporting axes, every point published: **vintage depth
d ∈ {0,1,2,3,5,10,21,63,252}** trailing trading days dropped × **book size n ∈ {5,10,20,30,40,60}**
(the 2026-09-04 KEEP-4b family: top-n of the eligible set by the v1 composite **without** the
`/sqrt(vol20)` scaler, equal weight at 75% gross), plus `EWall` and the live `RULES v2` book, on
3 panels, 10 bps, weekly, next-day execution, 260-day warm-up skip. 216 grid points in `.grid.csv`.

Full-sample read at d=0 (the reproduction anchor — the standing 2026-09-04 candidate,
U56 FWD20, rebuilds at **13.03% / 1.0818 / −18.30%, halves 1.0955/1.0769, OOS 1.1451** vs
SPY 15.19% / 0.8871 / −33.72%, OOS 0.8786):

| panel | 4a passes | 4b passes (of 8 books) |
|---|---|---|
| U56 | 0 | 3 — FWD20, FWD30, FWD40 |
| B136 | 0 | 3 — EWall, FWD40, FWD60 |
| SMALL439 | 0 | 0 |

**Verdict stability across 24 (panel, d≠0) cells × 8 books = 192 re-reads: 4a flips 0, 4b flips 3.**
The three are U56 FWD40 at d=21 (pass→fail), B136 FWD20 at d=63 (fail→pass) and B136 EWall at
d=252 (pass→fail) — i.e. **nothing flips inside a week, and the first flip needs a month of drift.**
Max |ΔSharpe| against the d=0 read: 0.0024 / 0.0017 / 0.0051 at d=1 (U56 / B136 / SMALL439), rising
to 0.0538 / 0.1091 / 0.0447 only at d=252. Max |ΔMaxDD| is 0.0000 at every depth on every panel —
the worst drawdown of every book sits in 2020/2022, so the DD leg of both KEEP paths is vintage-inert.

## E. Rule 8

n chosen on IS (≤ 2016-12-31) by IS Sharpe, read once on 2017 → panel end, repeated at each vintage:

| panel | pick at all 9 depths | OOS CAGR / Sharpe / MaxDD (d=0) | RULES v2 OOS Sharpe | SPY OOS Sharpe |
|---|---|---|---|---|
| U56 | **FWD20, stable 9/9** | 14.66% / **1.1451** / −18.30% | 1.2904 | 0.8786 |
| B136 | **FWD10, stable 9/9** | 12.77% / 0.7806 / −21.44% | 1.1206 | 0.8820 |
| SMALL439 | **FWD20, stable 9/9** | 6.95% / 0.4657 / −33.48% | 0.5665 | 0.8820 |

The rule-8 **choice** is vintage-stable on all three panels across all nine depths (IS Sharpe cannot
move at all when only the tail is truncated, which is itself the point: **the vintage risk is
entirely in the READ, not in the CHOICE**). The chosen arm beats the live book OOS on 0 of 3 panels
and beats SPY OOS on 1 of 3 (U56 only). Survivorship caveat: U56/B136 are current constituents;
SMALL439 is the current constituents of a sub-$2B screen (`data/SMALL_PANEL_README.md`), and the 44
`max_1d_move ≥ 1.0` names were dropped before use.

## The proposal (for the Sunday review; PROTOCOL, not adopted here)

> **PROTOCOL 10 — panel vintage.** Every committed artefact records the vintage of every price panel
> it consumed. `research/baseline.py` gains `panel_stamp(px) -> (first_date, last_date, n_rows,
> n_cols, panel_sha)`; each backtest writes one `<stem>.vintage.csv` row per panel used
> (`panel, first_date, last_date, n_rows, n_cols, panel_sha, file_sha`), and any CSV of results
> carries `panel_sha` as a column. A reproduction gate that fails without a matching `panel_sha`
> is reported as **DATA-DRIFT**, not as a failure, and is re-run at the artefact's own stamp before
> any conclusion is drawn. Back-fill is best-effort from git (artefact commit → panel blob at that
> commit) and only in a full clone.

Cheap, because it is measured: the stamp is 5 fields and one sha256 over ~2 M float64s (< 0.05 s per
panel), against a documented cost of **not** having it that is 3 of 192 KEEP-path verdicts and one
whole idea (513) spent attributing a gate failure to its input.

## Honest limits

- `d` truncation models *"this artefact was computed d days earlier"* through the **append** channel
  only; the **restatement** channel is measured separately in C2 (max |d| 3.000e-04 on 23,055 cells)
  and is two orders of magnitude smaller than one appended row on this panel.
- The census's two middle rows are upper bounds by construction, stated as such.
- 0 of 24 books clear 4a at any depth; the 4a leg is not exercised by this design, so "4a flips 0"
  is a weaker statement than "4b flips 3".
