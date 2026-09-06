# Idea 51 — trend-filter-by-market-cap (lane B, 2026-09-06)

**Verdict: KILL of the market-cap reading. The universe boundary is REAL and survives
rule 8, but it is NOT a cap boundary — it is a panel boundary, and no RULES clause
phrased in market cap is supportable. Plus a PROTOCOL by-product: on unlevered
gross-scalar books, path 4b does not discriminate the filter from no filter at all.**

Script: `2026-09-06_trend-filter-by-market-cap_B.py` · 10 bps, t+1 fills, no leverage,
no shorting · outputs `.console.txt` `.grid.csv` `.deciles.csv` `.walkforward.csv`
`.grossband.csv` `.summary.csv` `.zerocost.csv` · runtime 734 s.

## Design

Treatment is the **eligibility filter alone**. There is no ranking in any book: every
arm is equal-weight over a set of names, so the only thing that varies is which names
are in the set and what happens to the gated-out weight.

| arm | set | gross convention |
|---|---|---|
| `EWall` | every priced tradable name | **CONTROL**, gross `g` |
| `MA-RS` | px > 200d MA | RESPREAD — gross pinned at `g` (selection only) |
| `MA-DG` | px > 200d MA | DEGROSS — weight `g/N`, `N` = ALL names, rest CASH |
| `MAVOL-RS` / `MAVOL-DG` | px > 200d MA **and** vol20 < 0.60 (the literal v1 filter) | as above |

Splitting RS from DG is the point: idea 49's number was measured under one convention,
and the record (81 / 121 / 297) keeps finding that de-grossing prices in a cash drag
with no selection content.

Panels: `U56` (universe.json), `B136` (universe_broad.json), `SMALL439`
(data/prices_small.csv, stocks only, `max_1d_move < 1.0` per the panel README, SPY
joined as benchmark only). **Tuned parameters: 2** — gross `g ∈ {0.50, 0.75, 1.00}`
and cadence `∈ {W, M}`. MA window 200, vol cap 0.60 and the cost rung are inherited
from RULES, not tuned. All 6 grid points reported for all 15 (panel, arm) cells.
Decile work runs at the single pre-registered point `g = 0.75`, weekly.

**Survivorship:** `SMALL439` is the *current* constituent list of a sub-$2B screen —
no delistings, no acquisitions. `B136` is current constituents too. Both bias returns
up; the missing cohort on the small panel is exactly the thin, failed cohort.

## Q1 — the filter alone, 90 books

Costs CAGR in **72 of 72** filter cells and Sharpe in **54 of 72**. Means over the six
(g, cadence) points, against `EWall` at the same (g, cadence):

| panel | MA-RS | MA-DG | MAVOL-RS | MAVOL-DG |
|---|---|---|---|---|
| **U56** dCAGR / dSharpe | −1.21% / **−0.004** | −4.72% / **+0.062** | −2.16% / −0.033 | −5.50% / **+0.020** |
| **B136** | −2.06% / −0.047 | −5.99% / −0.009 | −2.88% / −0.074 | −6.48% / −0.035 |
| **SMALL439** | −2.41% / −0.102 | −5.92% / −0.082 | −5.33% / **−0.269** | −7.78% / −0.259 |

The panel ordering is monotone in every one of the four arms: U56 ≥ B136 > SMALL439.

**Idea 49's −5.4 pp/yr reproduces at its own cost rung.** At 0 bps, g = 0.75, weekly:
`SMALL439/MAVOL-RS` is **−5.31 pp/yr** and `MAVOL-DG` −8.31 pp/yr — the published
figure is the RESPREAD arm of the literal v1 filter, to 0.1 pp. But **roughly 60% of
the headline CAGR damage on every panel is the de-grossing convention, not selection**:
U56 MA-RS −1.21% vs MA-DG −4.72%; SMALL439 −2.41% vs −5.92%. The filter's *selection*
cost is a third of what the record has been quoting.

Cost is not the story either: the sign is identical at 0 bps in 11 of 12 panel × arm
cells, despite the filter multiplying turnover by 4–8× (U56 EWall 0.83×/yr → MA-RS
7.62×/yr).

## Q3 — cap deciles inside the small panel: the cap reading dies here

Two size columns, because neither alone is honest. `capQ` = static 2026 mktcap from
`research/deepvalue/universe_under2b.csv` (a look-ahead **classifier** — no return
information enters it, but it is a *today* cap applied to 2010 data). `advQ` = trailing
60d median dollar volume, ranked cross-sectionally each day — fully causal, membership
time-varying. 435/439 names carry a cap; panel-median 60d dollar volume is $3.22M.

| | corr(decile, dSharpe) | corr(decile, dCAGR) | dSharpe > 0 |
|---|---|---|---|
| capQ · MA-RS | **−0.336** | −0.405 | 0/10 |
| capQ · MA-DG | −0.333 | −0.325 | 1/10 |
| advQ · MA-RS | **+0.335** | +0.185 | 0/10 |
| advQ · MA-DG | +0.113 | +0.908 | 1/10 |

**The two size columns give opposite-signed slopes.** Under static cap the filter gets
*worse* as cap rises inside the panel; under dollar volume it gets *better*. Their
per-decile dSharpe series correlate only +0.545. Meanwhile the filter is negative in
**19 of 20** decile × arm cells under each scheme, at 10 bps and at 0 bps alike.

So there is no cap boundary *inside* the sub-$2B panel: the gate is uniformly bad on
these names at every size, and the apparent slope is whatever the size proxy is. The
advQ slope is additionally confounded by survivorship — decile 1 ($0.05M ADV) has an
`EWall` CAGR of 31.7% and a Sharpe of 2.03, which is the missing-delistings cohort
speaking, not a real thin-name premium.

## Q4 — rule 8 walk-forward (g and cadence chosen on IS 2010-2016 Sharpe inside each panel × arm; the control re-selects on its own IS window; 2017-2026 read once)

| panel | arm | IS pick | OOS CAGR | OOS Sharpe | OOS MaxDD | dOOS CAGR | dOOS Sharpe |
|---|---|---|---|---|---|---|---|
| U56 | EWall (ctl) | g1.00/M | 18.63% | 1.151 | −29.00% | — | — |
| U56 | MA-RS | g1.00/M | 18.30% | 1.195 | −23.76% | −0.32% | **+0.045** |
| U56 | MA-DG | g1.00/M | 12.72% | 1.275 | −15.49% | −5.91% | **+0.124** |
| U56 | MAVOL-DG | g1.00/M | 12.00% | 1.298 | −14.17% | −6.63% | **+0.147** |
| B136 | EWall (ctl) | g1.00/W | 18.59% | 1.101 | −32.72% | — | — |
| B136 | MA-RS | g1.00/M | 17.22% | 1.100 | −28.35% | −1.37% | −0.001 |
| B136 | MA-DG | g1.00/M | 11.12% | 1.153 | −16.08% | −7.47% | +0.053 |
| SMALL439 | EWall (ctl) | g1.00/W | 12.88% | 0.635 | −46.03% | — | — |
| SMALL439 | MA-RS | g1.00/M | 11.85% | 0.630 | −50.21% | −1.02% | −0.005 |
| SMALL439 | MA-DG | g1.00/M | 5.40% | 0.590 | −21.62% | −7.47% | −0.045 |
| SMALL439 | MAVOL-RS | g1.00/M | 5.14% | 0.356 | −51.57% | −7.74% | **−0.279** |
| SMALL439 | MAVOL-DG | g1.00/M | 2.09% | 0.335 | −19.13% | −10.79% | **−0.301** |

OOS references: SPY 15.45% / 0.882 / −33.72%; RULES v2 (live) U56 9.53% / 1.285 /
−12.05%, B136 7.98% / 1.119 / −12.24%, SMALL439 3.85% / 0.568 / −14.68%.

**The panel ordering survives untouched.** OOS the gate is worth positive Sharpe on
U56, zero on B136, and clearly negative on SMALL439 — the same ordering as in-sample,
chosen without seeing 2017-2026. Caveat: the IS chooser picks `g = 1.00`, the **grid
edge**, in all 15 arms (cf. ideas 236/243).

## Q5 — the KEEP-path verdicts are gross-dial placements

None of these books is levered: `g` is a scalar on an otherwise identical position
vector with the remainder in cash at 0%. Measured over all 30 (panel, arm, cadence)
cells: **Sharpe span across g is at most 0.0050** (mean 0.0016), while CAGR scales
1.969× and MaxDD 1.902× from g = 0.50 to g = 1.00. So 4b's CAGR floor and DD cap are
two *level* tests on one dial, and a fixed 3-point ladder decides them by resolution.

Solving the band per book-form and **running its midpoint**:

- Band non-empty in **20 of 30** book-forms; 4b passes at the solved `g*` in **20 of
  20**. The fixed ladder had produced 10 of 90.
- U56 10/10, B136 10/10, **SMALL439 0/10** (`g_lo > g_hi` in every form).
- The no-filter control `EWall` passes 4b too — U56 at g\*=0.64 (11.27% / 1.124 /
  −19.41%, OOS 1.136), B136 at g\*=0.58 (10.95% / 1.122 / −20.11%, OOS 1.103).

**Path 4b therefore does not discriminate the trend filter from no filter at all.**
For a gross-scalar book it collapses to one number — Calmar ≥ (0.70·SPY CAGR) /
(0.60·|SPY MaxDD|) = **0.527** — plus the Sharpe tests. At g = 0.75 weekly:

| | EWall | MA-RS | MA-DG | MAVOL-RS | MAVOL-DG |
|---|---|---|---|---|---|
| U56 Calmar | 0.589 | 0.619 | 0.683 | 0.655 | 0.673 |
| B136 | 0.558 | 0.578 | 0.617 | 0.606 | 0.597 |
| SMALL439 | 0.282 | **0.169** | **0.249** | **0.092** | **0.139** |

That single table is the cleanest statement of the answer: the gate **raises** Calmar
in 8 of 8 large-cap arm comparisons and **lowers** it in 4 of 4 small-cap ones, and the
0.527 line falls between the panels, not inside them.

## KEEP paths

- **4a: 1 of 90** — `B136/MA-DG/g0.50/M`, Sharpe 1.132 (H1 1.242 / H2 1.020) vs RULES v2
  B136 1.106 (1.229 / 0.984), MaxDD −8.33% vs −12.24%. It "beats the book" by shrinking
  to 5.59% CAGR; per Q5 its Sharpe is 1.132/1.133/1.135 at g = 0.50/0.75/1.00, so this
  is the same dial placement in the other direction. Not a candidate.
- **4b: 10 of 90 on the fixed ladder, 20 of 20 on the solved band — including the
  no-filter control.** No candidate: nothing here beats its own control.
- Decile grid: 4a 1/60, 4b 0/60.

**No KEEP memo is written and RULES is unchanged.**

## Answers to idea 51

1. *Where does trend-following stop working?* Between `B136` and the sub-$2B panel. The
   boundary is real, monotone across all four filter arms, and survives rule 8.
2. *Is it a market-cap boundary?* **No.** Inside the small panel the two size columns
   disagree in sign (−0.336 vs +0.335) and the gate is negative in 19/20 cells at every
   size. The cross-panel ordering is a panel-composition effect (U56 and B136 are
   heavily ETF, and carry different survivorship), not a smooth function of cap.
3. *Does it belong in RULES as a universe clause?* Only as a **per-universe validation
   statement**, never as a cap threshold. Proposed wording for the Sunday review, as a
   PROTOCOL reporting clause rather than a RULES change:

   > The 200d trend gate is validated on `research/universe.json` and
   > `research/universe_broad.json` only. On the sub-$2B panel it is negative in 72/72
   > CAGR cells and 19/20 cap-decile Sharpe cells, at 0 and 10 bps, under both the
   > RESPREAD and DEGROSS conventions. Any claim that the gate generalises by market
   > cap must show a size column whose decile slope is sign-stable across at least two
   > independent size proxies.
