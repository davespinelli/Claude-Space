# Idea 92 — sharpe-bound-books-need-a-book-change — **ANSWERED: only dropping the ranking is a dial** (cloud, 2026-09-04)

Script `2026-09-04_sharpe-bound-book-change_cloud.py`, console `…_cloud.console.txt`,
all 96 grid points in `…_cloud.grid.csv`.

## Setup

Test cell inherited unchanged from ideas 46 and 84: `C2/CAND20` on `universe_broad.json` —
top-20 eligible by the v1 composite without `/sqrt(vol20)`, equal weight `0.75/20`, cash when
`E_t < 20`, gate = 200d MA and `vol20 < 0.60`, weekly, 10 bps. Idea 84 showed **no exposure or
turnover lever moves it**: over 20 gross × entry-budget arms the H2 margin spanned
−0.119…−0.020 and the best improving move was **+0.0027**. The queue asks what a *book* change
does. `universe.json` (56) is run identically as the control universe, where the same book
**passes** 4b, so an instrument that "works" only there is exposed as a broad-only artefact.

Harness verified against the published rows before anything else:

- `SECTOR cap=1.00` ≡ `NORANK CAND n=20` (both are the test cell) — Sharpe identical to 6dp.
- `WCAP-RANKW` at `wmax = 0.75/20` collapses onto CAND20 weight-for-weight, max|diff| 2.4e−16
  off tie days.
- Test cell, broad, 10 bps: **13.1% / 0.958 / −20.1%, H1/H2 1.125 / 0.814, OOS 0.894** — H2
  margin **−0.023**, 4b fails on H2 *alone*. Reproduces idea 46's 0.814-vs-0.837 exactly.
- Test cell, u56: 12.7% / 1.093 / −18.3%, halves 1.088 / 1.103 — reproduces idea 2's KEEP row.

Four instrument families, each sweeping exactly one dial. "Moves H2" uses **idea 84's own
threshold, |ΔH2| > 0.05**, fixed before the numbers were read.

## The answer (broad, 10 bps, ΔH2 vs the test cell)

| family | ΔH2 range | best upward | verdict | converts cell to 4b |
|---|---|---|---|---|
| **NORANK** (drop the ranking) | +0.000 … **+0.158** | **+0.158** | **DIAL** | **4 of 4** |
| SECTOR cap | −0.105 … +0.025 | +0.025 | moves H2 **down only** | 1 of 3 (fragile, below) |
| GATE (eligibility instrument) | −0.017 … +0.042 | +0.042 | **not a dial** | 1 of 5 (at the bar) |
| WCAP on the rank-weighted book | −0.033 … +0.001 | +0.001 | **not a dial** | 0 of 4 |
| WCAP on the equal-weight book | +0.000 … +0.000 | **+0.000** | **not an instrument at all** | 0 of 4 |

### 1. The per-name weight cap is definitionally inert (Q1 confirmed, exactly)

On CAND20 the cap never binds — bind rate 0 — and every arm reproduces the control **to
machine precision at every cap level on both universes**: ΔH2 = +0.000, ΔSharpe = +0.000.
An equal-weight book already sits at its own cap. On the genuinely concentrated `RANKW` book
(same 20 names weighted ∝ 1/rank) the cap does bite, and it is **monotone in one direction
only**: uncapped H2 = 0.780, and tightening the cap walks it back up to 0.815 — i.e. exactly
the equal-weight book. **The cap's entire content is "become equal-weight", and its ceiling is
the control it is supposed to beat.** It has direction but no headroom.

### 2. The sector cap moves H2 down, not up

−0.105 at a 15% cap, −0.059 at 25%, +0.025 at 40%. The 40% arm does technically convert the
cell (H2 margin **+0.002**), but it is not usable: it dies at 25 bps (ΔH2 = 0.000, 4b fails on
four bars), and **rule 8 picks the 15% cap on the in-sample window and takes the worst regret
in the whole run, −0.187** (OOS Sharpe 0.727 against the family's best 0.914). Tightening the
cap costs turnover monotonically (13.8 → 18.4×/yr) and gross (0.740 → 0.655). On u56 the
family is not a dial at all (ΔH2 ≤ +0.022).

### 3. The eligibility gate is **not** the answer here — Q4 refuted on the primary universe

Best upward move +0.042 (no gate at all), below the 0.05 threshold; the four-way decomposition
reads none +0.042 / 200d-only +0.025 / vol20-only −0.017 / band3 +0.009, and abs momentum
+0.023. The abs arm converts the cell but with an H2 margin of **+0.000** — literally at the
bar — and fails at 25 bps. This is a genuine surprise against the pre-registered prediction,
which took ideas 49/57/61 to imply the gate carries the book: the gate carries the *drawdown*
(no-gate MaxDD −26.0% vs the control's −20.1%) but not H2.

### 4. Dropping the ranking is the dial, and it is monotone (Q3 confirmed, idea 82)

H2 rises monotonically as the ranking is diluted, on the panel where the ranking was supposed
to be earning its keep:

| broad, 10 bps | turn/yr | CAGR | Sharpe | MaxDD | H1 | **H2** | OOS Sh | 4b |
|---|---|---|---|---|---|---|---|---|
| CAND n=20 (test cell) | 13.8× | 13.1% | 0.958 | −20.1% | 1.125 | **0.814** | 0.894 | fail (H2) |
| CAND n=40 | 10.3× | 11.9% | 1.004 | −19.1% | 1.133 | **0.887** | 0.980 | **PASS** |
| CAND n=60 | 8.1× | 10.9% | 1.014 | −19.0% | 1.111 | **0.927** | 1.027 | **PASS** |
| EWall (no ranking) | 8.3× | 10.7% | 1.027 | −17.7% | 1.146 | **0.917** | 1.021 | **PASS** |
| ew-band3 (no ranking) | 5.2× | 11.1% | 1.064 | −16.8% | 1.163 | **0.971** | 1.074 | **PASS** |
| SPY | — | 15.3% | 0.890 | −33.7% | 0.957 | 0.837 | 0.884 | — |

**All four convert the cell.** Rule 8 selects `ew-band3` in this family and it is
simultaneously the family's **best** OOS arm — regret exactly 0.000, the only family in the run
where the in-sample pick is also the out-of-sample winner (SECTOR −0.187, WCAP-RANKW −0.024,
GATE −0.014). OOS 2017-26: 11.2% / **1.074** / −16.8% against RULES v1 6.0% / 0.581 / −21.2%
and SPY 15.5% / 0.884 / −33.7%.

At **25 bps** the ordering not only survives but widens — ΔH2 grows to **+0.225** for ew-band3
— because the no-ranking books turn over a third as much (5.2× vs 13.8×). At that cost
ew-band3 is the *only* arm in all 24 whose sole remaining 4b failure is the CAGR floor, which
idea 84 already showed is the gross axis and already closed at `g = 0.85`.

The control universe agrees on the mechanism without the cell being broken there: NORANK is
again the only family that is a dial in both directions on u56 (ΔH2 −0.067…+0.071), rule 8
again picks ew-band3, and it again posts the best OOS Sharpe of the five picks (1.234).

## Deliverable: the list of instruments that are NOT dials on a Sharpe-bound book

1. **Gross exposure** — idea 84, ΔH2 ≤ +0.003 over 20 arms (g-invariant by construction).
2. **Turnover budget (entry-only or total)** — idea 84, same census.
3. **Per-name weight cap** — this run, ΔH2 = +0.000 exactly on any equal-weight book; on a
   concentrated book its ceiling is the equal-weight book itself.
4. **Sector cap** — this run, ΔH2 upward ≤ +0.025 and negative at every usable tightness;
   worst walk-forward regret in the run.
5. **The eligibility gate** — this run, ΔH2 upward ≤ +0.042 on the primary universe. It is a
   drawdown instrument (ideas 22/57/74), not a Sharpe instrument.

**The one thing that is a dial: the selection itself.** Diluting or removing the composite
ranking is the only change that moves a Sharpe-bound book's binding bar, and on the broad
panel it moves it by 6–58× more than anything else tested. Consistent with idea 73's
gross-matched finding that the ranking premium is negative in 16 of 21 (panel, n) cells and
idea 82's proposal to drop ranking from the candidate book entirely.

## By-product worth recording

`rank <= n` selects **21** names on 22 of 4698 broad days (45 of 4698 on u56) because the
composite ties, so idea 2's literal `g/n` construction runs at up to **0.7875 gross rather
than 0.75** on those days. Immaterial to any published verdict (it is 0.5% of days) but it
means the book is not exactly gross-constant, and a `nlargest`-style tie-break would remove it.

## Verdict

**KILL for the sector cap and the per-name weight cap as instruments** (the cap is not an
instrument at all on an equal-weight book, and the sector cap is a Sharpe cost). **KILL for
the eligibility gate as a Sharpe instrument** on this cell, against the pre-registered
prediction. **The queue's fourth candidate — dropping the ranking — is the answer**, and it
converts the cell on both KEEP-relevant measures at 10 bps and dominates at 25 bps. No new
book is proposed: the winner is `ew-band3`, already the standing candidate from idea 84, and
this run is an independent, pre-registered mechanism test that it is on the right axis. Memo:
`2026-09-04_sharpe-bound-book-change_cloud.memo.md`.

## Caveats

- **Sector labels are a price proxy, not GICS.** Each name is assigned annually, using only
  the prior 756 trading days, to the SPDR sector ETF its returns correlate with most (11.0%
  mean year-over-year label churn on broad, 12.5% on u56, 1 of 136 names ever UNK). This will
  put a "consumer" name that trades like tech into XLK. That is arguably the right object for
  a *risk* cap, but the sector-cap result should be read as "a correlation-cluster cap does
  not move H2", not as a refutation of GICS sector caps specifically.
- **Survivorship.** Both panels are current-constituent lists, so all CAGR/Sharpe levels are
  optimistic and the sector labels inherit the bias. The instrument *deltas* — the result — are
  measured on the same panel and the same days and are far less exposed.
- One cell. The census of binding bars (idea 84) found only one Sharpe-bound (book, universe)
  cell to test on, so "instruments that are not dials" is demonstrated on that cell plus a
  passing control, not on a population of Sharpe-bound cells.
