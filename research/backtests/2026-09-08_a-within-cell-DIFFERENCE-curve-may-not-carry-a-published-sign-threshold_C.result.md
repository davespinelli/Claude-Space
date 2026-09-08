# Idea 443 — a-within-cell-DIFFERENCE-curve-may-not-carry-a-published-sign-threshold (lane C, 2026-09-08)

**ANSWERED, and the back-fill retracts NOTHING. The construction idea 440 killed is real, mechanical
and detectable, but it is confined to 3 source runs and 10 columns of the record's 24 committed
curve files — and of the two curves whose reader floor is live (168c's k dial, the band-gate's
band dial), NEITHER published a crossing as its location. 168c published a sign comparison at the
control point (which idea 440 killed on separability, not on flooring) and the band-gate published
a monotonicity, whose magnitude survives here: plateau − floor +0.30112, 95% CI [+0.17318,
+0.44651], separable. So the proposed PROTOCOL clause is worth adopting as a GUARD against a
failure the record has committed once, not as a retraction notice.** The clause is drafted below
and left in the queue, not written into `PROTOCOL.md` (rule 6: a protocol clause is a Sunday-review
decision). No RULES change, no KEEP (0 of 5 arms pass 4a or 4b); `RULES.md`, `scan.py`, `bot.py`,
`baseline.py` untouched.

Script: `research/backtests/2026-09-08_a-within-cell-DIFFERENCE-curve-may-not-carry-a-published-sign-threshold_C.py`
Artefacts: `.console.txt`, `.repro.csv`, `.census.csv` (40 rows), `.sensitivity.csv` (15 grid
points), `.pinned.csv` (32 unique (file, x, y) pairs), `.bookgrid.csv` (126 fresh books),
`.walkforward.csv`, `.keeppaths.csv`.

Idea 439's committed frame (`ITEMS`, `load_item`, `local_curve`, `crossing_of`, `argmax_of`,
`make_grid`, `fast_backtest`, `band_book`, `csd`, `BANDS`/`GROSSES`/`CADENCES`, `HM_HEADLINE`) is
**imported from its script, not re-implemented**, so the census scope and the reader are the
record's own.

## Reproduction gate — before any new number was read

| check | published | this run | |
|---|---|---|---|
| idea 219's crossing at its own half-window | 0.425 (last non-positive 0.400) | 0.425 / 0.400 | MATCH |
| idea 440's EXACT per-k means on 168c's committed curve (5 published values) | −0.35419 … +0.06066 | max abs diff **3.88e-06** (published to 5 dp) | MATCH |
| idea 440's EXACT crossing / last non-positive on 168c | +0.10 / 0.00 | +0.10 / 0.00 | MATCH |
| `fast_backtest` vs `engine.backtest`, RULES v2 / U56 @10 bps | — | max abs diff **0.000e+00** | MATCH |
| all 10 registered items load and read | 10 | 10 | MATCH |

Two tuned parameters: **P1** control-detection rule ∈ {STRICT, MAJORITY, SDZERO}; **P2** tolerance
∈ {0, 1e-12, 1e-9, 1e-6, 1e-3}. All 3 × 5 = 15 grid points reported in §3.

## (1) The test needs no cell structure, which is why it can be a protocol clause

If `y = f(x) − f(x₀)` within cell, then `y = 0` at `x = x₀` in **every** row, whatever the cells
are. So the detector is one line and does not need to know the design: *is there an x level at
which every row's |y| is at or below tolerance, while y has real spread elsewhere?* That is what
makes the proposed clause mechanically enforceable rather than a matter of reading each script.

## (2) THE CENSUS — 24 committed `*curve*.csv`, headline cell (STRICT, 1e-12)

**Registered scope** (idea 439's 10 ITEMS, x and y as that run declared them): **4 of 10 pinned**,
**2 of 10 are reader floors**.

| item | x | y | pinned at x₀ | next grid pt up | exact crossing | reader floor | P(crossing = floor) |
|---|---|---|---|---|---|---|---|
| **168c** | k | dSharpe | **0.00** | +0.10 | **+0.10** | **YES** | **1.000** |
| **bandgate** | band | gap vs bare 200d | **0.00** | 0.02 | **0.02** | **YES** | **1.000** |
| 168B | k | dSharpe | 0.00 | +0.25 | none | no — the arm is never all-positive, so there is no crossing to floor | 0.000 |
| 219 | share_mean | d_mean | **1.00 (the top endpoint)** | — | — | no — nothing above it | 0.000 |
| 167, 159B, 159c, 103, 61, 277 | — | — | not pinned | — | — | — | — |

**Mechanical sweep** (every numeric (x, y) column pair in every committed curve file): **30 pinned
pairs in 8 of 24 files**, 6 of them reader floors; 32 unique (file, x, y) triples once the two
overlaps with the registered scope are de-duplicated, **7 reader floors in total, 5 with
P(crossing = floor) = 1.000**.

The sweep is deliberately over-inclusive and its false-positive class is visible by eye: of the 30
hits, **only 8 have a difference-shaped y** (`dCAGR`, `dCAGR_OOS`, `dSharpe`, `dSharpe_OOS`,
`dCAGR_pp`, `dMaxDD_pp`, `dCAGR_net_of_extra_cost_pp`, `dSharpe`), and every one of those 8 is on
the **k axis of the same two source runs** (168B and 168c). The other 22 are indicator or dispersion
columns that happen to be constant at one x — `pass4a`/`pass4b` all-False at a level, `Sharpe_sd`
and `premium_sd` undefined at a single-draw level, `switch`/`sd_d_median` zero at an empty decile.
Those are not difference curves and none of them carries a published location.

**So the record's whole within-cell-difference-against-its-own-axis construction is 3 source runs
and 10 columns: 168B (k), 168c (k) and the band-gate (band width), plus idea 219's endpoint
degeneracy.**

## (3) SENSITIVITY — all 15 grid points (P1 × P2)

| P1 \ P2 | 0 | 1e-12 | 1e-9 | 1e-6 | 1e-3 |
|---|---|---|---|---|---|
| **STRICT** (every row at x₀ within tol) | 4 / 30 / 8 | **4 / 30 / 8** | 4 / 30 / 8 | 4 / 30 / 8 | 4 / 28 / 8 |
| **MAJORITY** (≥95% of rows within tol) | 4 / 30 / 8 | 4 / 30 / 8 | 4 / 30 / 8 | 4 / 30 / 8 | 4 / 28 / 8 |
| **SDZERO** (sd at x₀ within tol) | 4 / 123 / 14 | 4 / 124 / 14 | 4 / 124 / 14 | 4 / 117 / 14 | 5 / 132 / 15 |

*(cells are: registered items pinned of 10 / sweep pairs pinned / sweep files touched)*

**The census is invariant to both parameters over the whole range that matters.** STRICT and
MAJORITY are identical in 10 of 10 cells — no committed curve has a *nearly* pinned control level,
which is what you expect if the pins are definitional rather than numerical. Tolerance does nothing
until 1e-3, where it drops 2 sweep pairs. **SDZERO is the wrong rule and the grid says so**: it
multiplies the sweep hits by 4 (30 → 124) because "sd = 0 at a level" also fires on every constant
column, including boolean flags, and its extra hits carry no published location. The headline is
therefore read at STRICT, and the reading would be identical at MAJORITY and at any tolerance below
1e-3.

## (4) THE PUBLISHED LOCATIONS — none of them is a reader floor

This is the part of the queue's question with money in it, and the answer is negative:

| pinned curve | what its source run actually PUBLISHED | is that a floored reading? |
|---|---|---|
| **168c** | "live k = −0.5 loses to k = 0 in 32 of 32 cells" — a sign comparison **at** the control point | **No.** A statement about the *negative* arm is unaffected by a floor on the positive arm. Idea 440 killed the *"k crossing"* object separately, and this run confirms its non-separability: plateau − floor **+0.01470, 95% CI [−0.01544, +0.04757]** |
| **bandgate** | "the 200d gate's damage is never noise-crossing damage (the gap rises in band width)" — a monotonicity/magnitude | **No, and the magnitude survives:** level at the floor +0.06861, plateau +0.36973, **plateau − floor +0.30112, 95% CI [+0.17318, +0.44651], separable YES**, arm slope +1.769 |
| 168B | "no interior optimum; argmax at the grid edge in 10/12" — an argmax, not a crossing | No (and its curve carries no crossing at all) |
| 219 | crossing **0.425** | No — 219's pin is at the **top endpoint** (see §5), which cannot floor a crossing |

Of the 7 reader floors found anywhere in the corpus, **4 have a plateau that is separable from the
floor level** (bandgate `gap`; 168c's `dCAGR_pp`, `dMaxDD_pp`, `dCAGR_net_of_extra_cost_pp`) and
**3 do not** (168c `dSharpe` — idea 440's kill — and 168B's `dCAGR`, `dCAGR_OOS`). That is the
clause's practical content: on a pinned curve the crossing is never a measurement, but the
magnitude usually still is, and in 4 of 7 cases here it is publishable as it stands.

## (5) A SECOND, DISTINCT FAILURE MODE: the endpoint pin

Idea 219's curve is pinned at `share_mean = 1.0` — 100 rows, every one exactly 0, because a
unanimous mode has nothing to differ from. This is **not** a control pin and it cannot floor
anything (there is no grid point above it), and indeed 219's crossing is **0.425 with the pinned
endpoint and 0.425 without it — the location is unmoved**. But it deflates every window that
reaches it: the top centre's local mean is **+0.000959 with the pin and +0.002482 without,
2.59× smaller**. A run that published 219's plateau *level* rather than its crossing would have
understated it by that factor. The proposed clause therefore has to name the control pin (a
location hazard) and the endpoint pin (a level hazard) separately.

## (6) Rule 8, live prices: what does adopting a reader floor actually cost?

The band-width dial is one of the two live reader floors **and** the record's only adopted constant
(RULES v2's 3% band), so it prices the question directly. 126 fresh books — 3 panels (U56 56,
B136 136, SMALL439 484 cols) × 3 gross × 2 cadence × 7 band widths — 10 bps, t+1. `y = IS Sharpe(band)
− IS Sharpe(band = 0)` within each (panel, gross, cadence) cell, so the curve is pinned at band 0 by
construction. **The reading is taken on IS ≤ 2016-12-31 only; 2017–2026 is read once.**

Exact per-band IS means over the 18 cells (no window):

| band | 0.00 | 0.02 | 0.03 | 0.05 | 0.08 | 0.12 | 0.20 |
|---|---|---|---|---|---|---|---|
| mean dIS Sharpe | **0.00000** | +0.02059 | +0.02142 | +0.02413 | +0.05008 | **+0.06246** | +0.03554 |
| sd | **0.00000** | 0.02541 | 0.03725 | 0.05022 | 0.05651 | 0.06178 | 0.08584 |
| > 0 in | 0/18 | 12/18 | 12/18 | 12/18 | 15/18 | 15/18 | 12/18 |

**EXACT crossing 0.02 = the next grid point above the control — a reader floor, P = 1.000 by
construction** (the mean is positive at every band > 0, so the reader cannot emit anything else).
The magnitude reading — the argmax — is **0.12**, six grid steps away.

| arm | band | CAGR | Sharpe | MaxDD | H1 / H2 | OOS CAGR | OOS Sharpe | OOS MaxDD |
|---|---|---|---|---|---|---|---|---|
| **A_FLOOR (the crossing)** | 0.02 | 7.42% | 1.0767 | −11.28% | 1.1193 / 1.0348 | 7.51% | **1.1084** | −11.28% |
| A_PLATEAU (the argmax) | 0.12 | 7.85% | 1.0630 | −14.24% | 1.1559 / 0.9732 | 7.66% | 1.0525 | −14.24% |
| A_CTRL (band = 0, the control point) | 0.00 | 7.25% | 1.0647 | −10.84% | 1.1097 / 1.0200 | 7.32% | 1.0979 | −10.84% |
| A_LIVE (RULES v2's 0.03) | 0.03 | 7.44% | 1.0712 | −11.75% | 1.1198 / 1.0238 | 7.51% | 1.0968 | −11.75% |
| A_IS (per-cell IS argmax) | 5 distinct | 7.79% | 1.0825 | −13.40% | 1.1708 / 0.9977 | 7.67% | 1.0759 | −13.40% |
| **SPY** (equal-weight of the 3 panels) | — | 15.23% | 0.8891 | −33.72% | 0.9568 / 0.8342 | 15.45% | 0.8822 | −33.72% |
| **RULES v2 (live) @10 bps** | — | 7.22% | 1.0609 | −10.88% | 1.0988 / 1.0237 | 7.37% | 1.0991 | −10.88% |

**The uncomfortable result, reported as found: on this dial the reader floor is the best arm OOS.**
Against A_FLOOR, pooled OOS: the argmax reading **−0.0559** Sharpe and **+2.96 pp** of drawdown, the
IS chooser **−0.0325** and +2.12 pp, the live 0.03 −0.0116, the control point −0.0105. That is not
an endorsement of the reader — the floor is still the only number `crossing_of` is capable of
emitting here, so it carries no information — it is the honest reason the clause is a *guard* and
not a retraction: **the whole band dial is worth +0.0105 of OOS Sharpe over doing nothing (band 0),
and selection on it loses to doing nothing by −0.0220.** A reading that cannot be wrong about a dial
that does not matter has not cost the record anything yet. **Seventh consecutive coin flip for
IS selection** after ideas 110/151/132/166/155/168/440.

## (7) KEEP paths — none

4b bars off the pooled SPY (H1 > 0.9568, H2 > 0.8342, OOS > 0.8822, |MaxDD| ≤ 20.23%, CAGR ≥ 10.66%):

| arm | 4a vs RULES v2 | 4b | failing |
|---|---|---|---|
| A_FLOOR (0.02) | False | False | CAGR |
| A_PLATEAU (0.12) | False | False | CAGR |
| A_CTRL (0.00) | False | False | CAGR |
| A_LIVE (0.03) | False | False | CAGR |
| A_IS | False | False | CAGR |

**0 of 5 on both paths.** Every arm clears 4b's Sharpe bars comfortably (OOS 1.05–1.11 against SPY's
0.882) and dies on the CAGR floor at 7.2–7.9% against a 10.66% bar — a fifth reproduction of idea
330's premise that this book form is a volatility term, not a return term. On 4a, A_FLOOR and
A_LIVE beat RULES v2 in **both** halves (1.1193/1.0348 and 1.1198/1.0238 vs 1.0988/1.0237) and fail
only on the drawdown clause, by 40 bps and 87 bps of MaxDD respectively — the band dial buys Sharpe
by taking slightly more drawdown than the live book, which is exactly the trade 4a forbids.

## Verdict

**SPLIT — the question is answered and the clause is worth adopting, but the back-fill retracts
nothing.** The construction is real and mechanically detectable (STRICT and MAJORITY agree in 10 of
10 grid cells; tolerance is irrelevant below 1e-3), it appears in 3 source runs and 10 columns of
24 committed curve files, and it produces 7 reader floors of which 5 are pinned at P = 1.000. But
no source run published a crossing on a pinned curve except the one idea 440 already killed: 168c
published a sign comparison at the control point, the band-gate published a monotonicity whose
magnitude is separable here (+0.30112, CI [+0.17318, +0.44651]), and idea 219's pin is an endpoint,
which moves no location at all (0.425 either way) though it deflates the plateau 2.59×. **Adopt the
clause as a guard, and add the endpoint pin to it as a distinct hazard.**

## PROPOSED PROTOCOL WORDING (drafted, NOT written into PROTOCOL.md — rule 6)

> **10. A within-cell difference curve may not carry a published sign threshold.** When a curve's
> `y` is defined as `f(x) − f(x₀)` within cell and `x₀` is a level of the SAME x-axis, then
> `y(x₀) = 0` identically, with zero variance, in every cell. A sign reader (`crossing_of`, and
> anything else requiring a strictly positive value) therefore cannot return `x₀` or anything below
> it, and the smallest value it is capable of emitting is the next grid point above `x₀`. Such a
> curve MAY publish a magnitude — the level at a named x, the plateau level, the slope of an arm, a
> hinge location with its knot charged as a parameter — but it MAY NOT publish the crossing as a
> location. A run that reports a crossing on such a curve must publish, in the same table: (a) the
> control level `x₀`; (b) the next grid point above it; and (c) `P(crossing = that grid point)`
> under the run's own bootstrap. Where (c) is at or near 1.0, the reading is a reader floor and is
> not a measurement.
> **10b.** A pin at an ENDPOINT of the x-axis is a different hazard: it cannot floor a location, but
> it deflates every windowed level that reaches it (idea 219: 2.59× at the top centre). A run whose
> curve is pinned at an endpoint must publish its levels with those rows excluded as well as
> included.
> Detection is mechanical and needs no knowledge of the cell structure: `y` is a within-cell
> difference against a level of its own x-axis iff there is an x level at which every row's `|y|`
> is at or below tolerance while `y` has spread elsewhere.
