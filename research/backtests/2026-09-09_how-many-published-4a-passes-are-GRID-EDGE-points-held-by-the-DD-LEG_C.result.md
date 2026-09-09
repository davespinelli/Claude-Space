# Idea 500 — how many published 4a passes are GRID-EDGE points held by the DD LEG?

**Verdict: SPLIT — the DD-LEG half is CONFIRMED and generalises; the GRID-EDGE half is
REFUTED. No KEEP-candidate, no memo, no RULES change.** RULES.md, PROTOCOL.md, scan.py,
bot.py and baseline.py untouched.

Lane C, 2026-09-09. Script `2026-09-09_how-many-published-4a-passes-are-GRID-EDGE-points-held-by-the-DD-LEG_C.py`;
raw output `.console.txt`, `.arms.csv` (every grid point), `.legs.csv`, `.census.csv`,
`.extension.csv`, `.walkforward.csv`.

## Design
Two tuned parameters, exactly as the queue allows: **dial x panel**. 6 dials (n, band,
gross, volcap, quantile, cadence — book forms lifted verbatim from idea 270R) x 3 panels
(U56 / B136 / SMALL439) x 2 cost rungs (10 bps headline, 25 bps rung — a second reading of
the *same* books, not a third parameter) = **174 published arm-rows**, plus **70 EXTENSION
arm-rows** past every OPEN grid endpoint = 244 rows, all reported. Weekly except on the
cadence dial; weights at t applied at t+1; no network.

Pre-registered before any number was read:
- **4a** — PROTOCOL 4a against the LIVE RULES v2 book at the arm's own rung: H1 Sharpe >
  base H1 AND H2 Sharpe > base H2 AND full MaxDD >= base MaxDD.
- **dominator** — another arm on the same sweep with strictly higher Sharpe in BOTH halves.
- **DD_HELD** — >= 1 dominator and EVERY dominator fails 4a on the MaxDD leg ALONE.
- **EDGE** — the sweep's Sharpe argmax (binding half = min(H1,H2)) sits at a grid endpoint
  the passer does not occupy. **MONOTONE** — min(H1,H2) moves monotonically from passer to
  that endpoint. **GRID_EDGE_DD_HELD = DD_HELD & EDGE & MONOTONE** (idea 270R's shape).
- **OPEN vs STRUCTURAL endpoint** — an endpoint is STRUCTURAL when the instrument cannot be
  widened (gross 1.00 = no leverage per PROTOCOL 2; volcap 9.99 and quantile 1.00 = no
  filter; cadence D and Q = the engine's fastest and slowest schedules). Only an OPEN
  endpoint can be a stopping-point artefact, so **every OPEN-edge sweep is re-run with the
  grid extended past it** — the direct test the queue's premise implies.

## Reproduction gates, run before any new number
- **idea 270R's SMALL439 band=0.05 arm reproduces EXACTLY**: 4.18% / 0.6183 / -14.59%,
  halves 0.6385 / 0.6031 at 10 bps (published 4.18% / 0.6183 / -14.6% / 0.6385 / 0.6031).
- RULES v2 on U56 @10bps: 8.64% / 1.2037 / -12.05%, halves 1.2309 / 1.1828 against the
  published 8.66% / 1.2056 / -12.05% / 1.2259 / 1.1908. **Not exact** — the committed price
  cache now runs to 2026-09-08, four trading days past the publication, which moves the
  half boundary. Drift is 0.02 pp CAGR / 0.0019 Sharpe / 0.008 on the halves.
- Cost decomposition (one gross run, both rungs derived) matches
  `engine.backtest(cost_bps=10)` at **0.000e+00**, so the 2 rungs cost one backtest, not two.
- Unplanned third gate: this run's **4b count is 14 of 174 with exactly 1 surviving 25 bps**
  — idea 270R's published 4b tally, arm for arm, on a different IS/OOS convention.

## (1) The census — the "how many" cannot be answered at this scale
**2 published 4a passes in 174 arm-rows (1.1%)**, and they are the *same arm at two rungs*:
SMALL439 / band=0.05. Both are **DD_HELD = 1, EDGE = 1, MONOTONE = 1, GRID_EDGE_DD_HELD = 1**.
So on the reconstructible corpus the shape is 2/2 — but the denominator is **one distinct
arm**, which is not a record-wide count. 0 of the 2 EDGE endpoints are STRUCTURAL.

The dominators, quoted (10 bps): passer band 0.05 H1 0.6385 H2 0.6031 MaxDD -14.59% against
base 0.5699 / 0.5770 / -14.68%; dominator band 0.08 (0.6546 / 0.6076 / **-14.91%**) and band
0.12 (0.6877 / 0.6215 / **-16.00%**) — both clear BOTH Sharpe legs and are cut by MaxDD alone.
The 25 bps rung is the same picture.

## (1b) The generalisable number — 4a is a drawdown test wearing a Sharpe test's name
Across all 244 arm-rows, **both Sharpe legs clear the live book only 15 times (6.1%)**, and
**the MaxDD leg then cuts 13 of those 15 (86.7%)**, admitting 2. On the 174 published rows
alone: 9 clear both Sharpe legs, MaxDD cuts 7 (77.8%). **The 4a bar is decided by its
drawdown leg in ~4 of every 5 arms that get that far**, which is the queue's real finding
and does not depend on the thin 4a denominator.

## (2) The EXTENSION test — the grid-edge premise is REFUTED
The band grid was extended from its published stop at 0.12 to 0.16 / 0.20 / 0.25 / 0.35.
Full extended sweep at 10 bps (arm: H1/H2/MaxDD/4a):

`0 0.5251/0.5555/-14.3%/0 · 0.01 0.5537/0.5706/-14.2%/0 · 0.03 0.5699/0.5770/-14.7%/0 ·
0.05 0.6385/0.6031/-14.6%/1 · 0.08 0.6546/0.6076/-14.9%/0 · 0.12 0.6877/0.6215/-16.0%/0 ·
0.16 0.7245/0.6195/-16.9%/0 · 0.20 0.7109/0.5958/-17.1%/0 · 0.25 0.6695/0.5748/-17.7%/0 ·
0.35 0.6422/0.4808/-19.0%/0`

Three things follow. **(a) The pass SURVIVES the wider grid, 2 of 2** — band 0.05 is still
the sweep's only 4a passer at both rungs, and the 70 extension rows add **0** new 4a passes
and **0** new 4b passes. **(b) The extension adds dominators, not an escape**: 2 -> 3 at
10 bps and 2 -> 4 at 25 bps, and **every added dominator is again cut by the MaxDD leg
alone** (DD_HELD_ext = 1). **(c) The published curve's "monotone to the widest point tested"
was itself a stopping-point reading**: H1 Sharpe peaks at band **0.16**, one step past where
the record stopped, and falls away to 0.35, while MaxDD deteriorates monotonically -14.2% ->
-19.0% across the whole range. EDGE flips 1 -> 0 for both passers once the grid is widened.

So idea 270R's flag was right to fire and right about the mechanism, but the arm is **not**
an artefact of where the sweep stopped: it is a genuine consequence of a drawdown cap on a
book whose Sharpe and drawdown rise together in the band.

## (3) Rule 8 (PROTOCOL 8) — params on 2009-2016, 2017-2026 read once
36 cells on the published grids. IS-Sharpe chooser: **OOS Sharpe 0.8548, CAGR 8.05%, MaxDD
-20.06%**, against **RULES v2 0.9657 / 6.93% / -13.10%**, **SPY 0.8809 / 15.43% / -33.72%**,
EWALL do-nothing 0.9515, RULES v1 0.4206. The chooser beats RULES v2 in **5/36** cells and
SPY in 22/36 — a further instance of the record's selection-loses result.

The IS-4a chooser (best IS Sharpe among arms whose 4a legs clear *in sample only*) exists in
4 cells and beats RULES v2 OOS in **4/4** — but at **OOS Sharpe 0.6105 and CAGR 4.32%**
against SPY's 0.8809 / 15.43%: the 4a bar transfers against the low-return live book and
nowhere near the index. On the **extended** grids the same chooser exists in 6 cells and
beats RULES v2 in only **4/6**, and the widened grid moves the rule-8 pick in **6 of 36**
cells for mean OOS Sharpe 0.8548 -> 0.8349. **Widening the grid never helps the chooser.**

## (4) Both KEEP paths
Published grids: **4a 2/174, 4b 14/174.** With extensions: **4a 2/244, 4b 14/244.**
The 14 4b passers are U56 (9) and B136 (5), all the open-eligibility high-gross equal-weight
book the record already published (gross 1.00, volcap 9.99/0.90/0.60, quantile 1.00/0.75,
n 20/30/50); only **U56 gross=1.00** survives 25 bps (11.17% / 1.1662 / -15.96%, halves
1.1938 / 1.1448, OOS 1.2443, turnover 2.35x/yr). **This is not a new book and is not filed
as a candidate** — it is idea 270R's set reproduced, i.e. the path that selects *exposure*
rather than a rule. The 4a passer (SMALL439 band 0.05) fails 4b on every leg that matters:
CAGR 4.18% against SPY's 15.4%.

## Honest caveats
- The census denominator is the reconstructible dial x panel corpus only — 174 published
  arm-rows, 1 distinct 4a-passing arm. Record-wide 4a counts sit in files whose books cannot
  all be rebuilt from committed caches; this run does not claim to have re-read them.
- `EDGE`/`MONOTONE` are grid-relative by construction: they measure where a sweep stopped,
  which is exactly why the extension re-run, not the flag, carries the verdict.
- SURVIVORSHIP: B136 is current constituents of `universe_broad.json`; SMALL439 is the
  sub-$2B screen with the 44 tickers whose `max_1d_move >= 1.0` dropped first. SMALL439's
  panel starts 2010-01-04, so its halves are shorter than U56's and B136's.
- The 25 bps rung re-reads the same books rather than re-optimising at that rung.

## Follow-ups queued
508 (is the DD leg's 86.7% cut rate a panel constant or a SMALL439 fact),
509 (does any published EDGE flag in the record survive its own extension re-run),
510 (price the 4a MaxDD leg against a volatility-matched cap instead of the live book's).
