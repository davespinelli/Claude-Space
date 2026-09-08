# Idea 442 — does the 4b gross-1.00 family survive a CASH CREDIT and a BORROW CHARGE?

**Lane C, 2026-09-08.** Script `2026-09-08_does-the-4b-gross-100-family-survive-a-CASH-CREDIT-and-a-BORROW-charge_C.py`.
Costs 10 bps, weights at t applied at t+1, warm-up 260 days.

## Verdict — **KILL (the carve-out hypothesis)**

The premise is falsified. Crediting cash at 150 or 300 bps and charging borrow at the same
rate does **not** dissolve the gross-1.00 family's 4b margin. Under the record's own
rf = 0 Sharpe convention the 4b pass count goes **28 → 29 → 30 of 210** books (rate
0 / 150 / 300); under the honest excess-return convention it is **28 → 28 → 28**. Not one
of idea 439's 19 passes is lost at any rate under any reading; two books are gained. The
live gross-0.75 family clears 4b in **0, 0 and 1 of 42** books.

The reason is a bar mismatch: a cash credit is a **Sharpe** instrument and 4b's binding bar
on the low-gross family is the **CAGR floor** (fails 42/42 at rate 0, still 41/42 at 300 bps).

## Grid — 2 tuned parameters, all points reported

| | |
|---|---|
| **P1 gross** | 0.50, 0.75, **1.00**, 1.25, 1.50 (idea 439's three rungs + two levered rungs so the borrow leg bites) |
| **P2 rate** | 0, 150, 300 bps/yr, symmetric: `dr_t = rate/252 · (1 − G_t)`, `G_t` = realised gross |
| reported axes (idea 439's, unchanged) | panel {U56, B136, SMALL439} × cadence {W, M} × band {0, .02, .03, .05, .08, .12, .20} |
| size | 210 books × 3 rates × 2 readings = **1 260 published points** (`.grid.csv`, `.keeppaths.csv`) |
| extra conventions (reported, never selected on) | ASYM credit 0 / borrow 300; REAL credit 150 / borrow 300 |

**Two Sharpe readings, both declared before any number was read.** `RAW` = the record's
convention (rf = 0): the credit is free return for the book, and SPY — whose realised gross
is identically 1.0 (gate G4, 0.000e+00) — receives exactly 0 from the same formula.
`EXCESS` = the same rate is the risk-free rate for everyone, subtracted from every series
including SPY and both baselines; algebraically the book's excess return collapses to
`r_t − rate·G_t/252`.

### Gates
| gate | result |
|---|---|
| G1 `fast_backtest` vs `engine.backtest` (RULES v2 / U56) | **0.000e+00** |
| G2 rate-0 grid reproduces idea 439's committed 126 books (CAGR, Sharpe, MaxDD, H1, H2, OOS) | 126/126 rows, **2.220e-16** |
| G3 rate 0 is an exact no-op on the credit path | **0.000e+00** |
| G4 SPY realised gross ≡ 1.0 | **0.000e+00** |

Live U56 band-3 g=0.75 realised gross: mean **0.5328**, p05 0.1884, max 0.7373. At nominal
1.25 the book is above 1.0 on **43.2%** of days, at 1.50 on **73.8%** — the borrow charge is
genuinely exercised.

## 1. The carve-out does not explain the family

4b passes, each cell out of 42 books:

| reading | rate | g0.50 | g0.75 | **g1.00** | g1.25 | g1.50 | total |
|---|---|---|---|---|---|---|---|
| RAW | 0 | 0 | 0 | **19** | 9 | 0 | 28 |
| RAW | 150 | 0 | 0 | **20** | 9 | 0 | 29 |
| RAW | 300 | 0 | 1 | **20** | 9 | 0 | 30 |
| EXCESS | 0 | 0 | 0 | **19** | 9 | 0 | 28 |
| EXCESS | 150 | 0 | 0 | **19** | 9 | 0 | 28 |
| EXCESS | 300 | 0 | 0 | **19** | 9 | 0 | 28 |

Set identity: **nothing is lost** going from rate 0 to 300 under RAW; the two gains are
`B136 W band0.00` and the one gross-0.75 book, `U56 M band0.12` (CAGR 10.68%, Sharpe 1.330,
OOS 1.339). By panel at every rate: U56 18–19/70, B136 10–11/70, **SMALL439 0/70** — idea
136's small-panel result reproduces a nineteenth time and is untouched by the convention.

**Binding bar on the gross-0.75 family** (why each of its 42 books fails 4b):

| reading | rate | fails | H1 | H2 | OOS | DD | **CAGR** |
|---|---|---|---|---|---|---|---|
| RAW | 0 | 42/42 | 14 | 14 | 14 | 1 | **42** |
| RAW | 300 | 41/42 | 4 | 0 | 0 | 1 | **41** |
| EXCESS | 300 | 42/42 | 14 | 14 | 14 | 3 | **42** |

At 300 bps the credit clears every Sharpe bar the 0.75 family had been failing (H2 fails
14 → 0, OOS 14 → 0) and still leaves the CAGR floor failing 41 of 42 times. A 300 bps
credit on ~47% average cash is worth **+1.4 pp/yr** against a gross gap of **+2.93 pp/yr**;
the differential is ~0.5 pp against a 2.0 pp CAGR shortfall.

## 2. What the 4b bars actually are on this dial: a gross window

Sharpe is a **pure scalar invariant** in gross — span across the five rungs within a cell,
median **0.0015**, max 0.0093 at rate 0 (and 0.0013–0.0014 under EXCESS at *every* rate).
So 4b on the gross dial is not a Sharpe test at all; it is two scale bars, a CAGR **floor**
and a MaxDD **ceiling**, solved by interpolation between the reported rungs:

**Live U56 cell (weekly, band 0.03) — admissible gross:**

| reading | rate 0 | rate 150 | rate 300 |
|---|---|---|---|
| RAW | **[0.921, 1.287]** | [0.867, 1.287] | [0.799, 1.287] |
| EXCESS | **[0.921, 1.287]** | [0.909, 1.286] | [0.896, 1.284] |

The live book sits at **0.75**, outside the window under every one of the six conventions.
A 300 bps credit moves the floor 0.12 of gross under RAW and 0.025 under EXCESS; it needs
to move 0.17. Panel medians: U56 [0.913, 1.222] → [0.780, 1.224]; B136 [0.944, 1.040] →
[0.821, 1.041]; SMALL439's floor (1.49) is **above** its ceiling (0.97) at every rate, which
is the exact shape of "0 of 70".

## 3. The convention itself is the finding — a caution for open idea 406

Under `RAW`, crediting cash manufactures a Sharpe ordering along a dial that has none:

| reading | rate | mean Sharpe span across the 5 gross rungs |
|---|---|---|
| RAW / EXCESS | 0 | **0.0015** |
| RAW | 150 | **0.2001** |
| RAW | 300 | **0.4041** |
| EXCESS | 150 / 300 | 0.0013 / 0.0014 |

The margin (gross 1.00 − gross 0.75, 42 paired cells) tells the same story: RAW **+0.0004
→ −0.0502 → −0.1008** mean dSharpe (positive in 43% → 0% → 0% of cells), EXCESS **+0.0004
→ +0.0006 → +0.0008** (min −0.0008, max +0.0024 across all rates). The whole apparent
reversal is the numeraire, not the books.

**4a is worse.** Passes against the live RULES v2 go RAW **4 → 29 → 38** of 210, of which
28 and 36 are at gross **0.50** — a credit priced this way would mint 25–34 new "4a passes"
that are nothing but de-grossed copies of the live book (idea 311's gross-scalar flag).
Under EXCESS: 4 → 7 → 9. **Recommendation for idea 406: if the record adopts a cash credit
it must adopt the excess-return reading with it, or every de-grossed arm in the record gets
a free 0.20–0.40 Sharpe and 4a becomes unreadable.**

## 4. The borrow charge

Symmetric charging costs the levered rungs almost nothing, because realised gross is far
below nominal. On the live cell under ASYM (credit 0 / borrow 300 — idea 406's description
of what idea 402 did): U56 g1.25 Sharpe 1.2052 → **1.1969** (−0.0084), CAGR 14.53% →
14.42%; g1.50 1.2047 → **1.1706** (−0.0341), 17.48% → 16.91%. B136 −0.0087 / −0.0324;
SMALL439 −0.0003 / −0.0044. Gross 1.50 fails 4b **0/42 at every rate** on the drawdown cap,
with or without the charge — the charge is not what kills it.

## 5. Rule 8 walk-forward (PROTOCOL 8)

(gross, band) chosen on IS ≤ 2016 by IS Sharpe, 2017–2026 read once; 36 cells
(panel × cadence × rate × reading), comparands under the same convention.

- Chooser beats SPY OOS **28/36**, RULES v2 OOS **18/36**, the pre-registered live
  g0.75/b0.03 **22/36**; mean oracle regret **+0.0588**.
- **The convention decides the pick.** The chooser takes gross ≥ 1.00 in **18/18** EXCESS
  cells and **6/18** RAW cells — under RAW at 150/300 bps it picks gross **0.50 in every
  one of the 12 cells**, i.e. the credit alone flips the walk-forward from "lever up" to
  "hold cash".
- Best OOS cells: U56 M RAW 0 → g1.50/b0.00, OOS **19.30% / 1.2778 / −22.41%** (SPY
  15.45% / 0.8822 / −33.72%; RULES v2 OOS 1.2853) — it still **loses** to the live book on
  Sharpe. U56 W RAW 300 → g0.50/b0.08, OOS 8.15% / 1.5654 / −9.66%, which is the credit,
  not the book.

## 6. KEEP paths — no new candidate

**0 of 1 260 points pass both paths.** Every 4b passer is the RULES v2 band book on U56 or
B136 at a gross the live book does not run, i.e. idea 311's dial placement. The best is
`U56 M band 0.00 g=1.25`: 15.03% / **1.2144** (1.2516 / 1.1809) / −19.01%, OOS 1.2766 — but
its Sharpe is **1.2144 vs the live book's 1.2058**, a gap of 0.009 on a dial whose Sharpe
span is 0.0015. It buys +6.4 pp/yr of CAGR with +6.9 pp of drawdown and a drawdown margin
of **1.22 pp** against the cap (the gross-1.25 family's median DD margin is 0.54 pp; the
gross-1.00 family's median CAGR margin is 0.80 pp). Both edges of the window are within one
bad episode of the bar — idea 321's flag. **PARK, no memo, no RULES change.**

SURVIVORSHIP: B136 and SMALL439 are current constituents only — levels overstated. Read the
within-panel gross × rate contrasts, which share the panel.

Artefacts: `.console.txt`, `.grid.csv`, `.keeppaths.csv`, `.margin.csv`, `.grossband.csv`,
`.breakeven.csv`, `.walkforward.csv`, `.extraconv.csv`.
