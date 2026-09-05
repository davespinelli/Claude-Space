# Idea 167 — is-the-value-cost-parallelism-general (cloud, 2026-09-05)

**VERDICT: KILL of the parallelism hypothesis — and the no-threshold conclusion survives anyway,
on stronger grounds.** Idea 159's `d = slope(log g) − slope(log c) ≈ 0` does **not** generalise:
on the common cost bar d is significantly non-zero in **7 of 12** (panel, instrument) cells, and
in **5 of those 7 it is significantly POSITIVE** (+1.67 to +3.13), the opposite sign from a
"stops paying above m" threshold. What *is* general is the ratio's **level**: `g/c ≥ 2.37` at all
**120 of 120** grid points on the turnover bar and `≥ 2.23` at all 47 points where the honest
incremental bar exists — **not one point in the run has an instrument costing more than it
moves**. The empirical crossing `m*` therefore does not exist in **12 of 12** IS cells. Idea 74's
exchange-rate framing is confirmed as a ratio and not a threshold, but *because the ratio never
reaches 1*, not because the two curves are parallel. No drawdown budget may be quoted as a level.

No new book, no KEEP, no RULES change.

## Reproduction gate — 6 of 6, before any new number was read

| check | published | this run | |
|---|---|---|---|
| [a] mean weekly eligible, u56 / broad / small | 37.5 / 91.5 / 141.2 (ideas 153/159) | 37.5 / 91.5 / 141.2 | MATCH |
| [b] idea 94 `EWall + band3-rw`, u56 @10 bps | 12.2% / 1.161 / −17.7%, halves 1.210/1.129 | 12.2% / 1.161 / −17.7%, 1.210/1.129 | MATCH |
| [c] cost-derivation identity, base book | `r_c = r_0 − turnover·c/1e4` vs a fresh 10 bps run | max abs diff **0.00e+00** | MATCH |
| [c] same identity for the **stop** arm | (its state machine reads prices, not equity) | max abs diff **0.00e+00** | MATCH |

[c] is what makes every gross/net pair below the *same book* rather than two runs.

## What was run

Four instruments off idea 74/94's menu, each an **overlay on the same ungated base book** at book
share m, through idea 94's committed `run()` simulator (imported, not retyped):

* **G200** — per-name 200d MA gate, de-gross convention (gated-out weight → cash)
* **BAND3** — 200d MA with a ±3% re-entry band, de-gross (idea 57's instrument)
* **DEGROSS** — static ×0.75 gross multiplier (idea 66's exact lever)
* **STOP15** — per-name 15% trailing stop (idea 9's instrument)

Base book = idea 78/94's TOP20 ranking generalised in n (composite, no vol scaler, **ungated**,
top-n at 0.75/n); n = max(2, round(m × N)); m over idea 159's 10-point grid. Panels u56 (56),
broad (136), small (439 after dropping the 44 tickers with `max_1d_move ≥ 1.0`). 150 books, each
run once at 0 bps with the 10 and 25 bps rungs derived exactly. Two tuned parameters: instrument
(4) × share (10); panel is a corpus axis. 92 s runtime, deterministic.

**Deviation from idea 159, stated not buried:** its second bar was BAR-OVL, the weight distance
between two *target* books. Three of these four instruments are execution overlays and the stop
changes no target weight at all, so BAR-OVL is identically zero for it. BAR-TO (10 bps ×
|Δ annualised turnover|) is the same quantity read off realised trading and exists for all four.
BAR-INC (exact incremental cost in CAGR terms) is unchanged from idea 159.

## 1. The d-statistic — the hypothesis fails

Bootstrap: circular block 21 d, 2000 replicates, seed 167, g resampled on the same block index,
c held at its point estimate (idea 159's scheme exactly).

| panel | instrument | bar | slope log g | slope log c | **d** | boot 5–95 | P(d<0) | reading |
|---|---|---|---|---|---|---|---|---|
| u56 | G200 | TO | +3.199 | +3.229 | −0.030 | [−1.061, +1.445] | 0.44 | straddles 0 |
| u56 | BAND3 | TO | +3.177 | +1.506 | **+1.671** | [+0.368, +3.527] | 0.03 | **positive** |
| u56 | DEGROSS | TO | −0.649 | −2.857 | **+2.207** | [+1.827, +2.586] | 0.00 | **positive** |
| u56 | STOP15 | TO | −0.845 | +0.030 | −0.875 | [−1.733, +0.569] | 0.87 | straddles 0 |
| broad | G200 | TO | +4.160 | +3.930 | +0.230 | [−1.342, +1.541] | 0.51 | straddles 0 |
| broad | BAND3 | TO | +4.048 | +0.918 | **+3.130** | [+1.795, +4.653] | 0.00 | **positive** |
| broad | DEGROSS | TO | −0.344 | −2.807 | **+2.463** | [+2.140, +2.791] | 0.00 | **positive** |
| broad | STOP15 | TO | −0.393 | +0.471 | **−0.864** | [−1.509, −0.182] | 0.97 | **negative** |
| small | G200 | TO | +2.400 | +4.322 | **−1.921** | [−3.515, −0.150] | 0.96 | **negative** |
| small | BAND3 | TO | +2.784 | +2.366 | +0.418 | [−1.223, +2.153] | 0.30 | straddles 0 |
| small | DEGROSS | TO | −0.381 | −2.645 | **+2.263** | [+1.465, +2.971] | 0.01 | **positive** |
| small | STOP15 | TO | +0.022 | +0.423 | −0.401 | [−1.025, +0.882] | 0.78 | straddles 0 |

**BAR-TO: straddles zero 5 of 12, significantly positive 5 of 12, significantly negative 2 of
12.** On the honest BAR-INC (computable in 7 of 12 — see below) it straddles zero in only 2 of 7
and is negative in 5. Idea 159's vol-tilt reference was 6 of 6 straddling.

Two readings matter:

* A **positive** d (BAND3 on both large-cap panels; DEGROSS on all three) means the instrument's
  value decays *slower* than its cost as the book grows — it gets relatively **cheaper** at
  higher share. There is no upper threshold; if anything there is a lower one.
* The two **negative** cells (broad STOP15, small G200) are the only places a crossing is even
  admissible in principle — and section 2 shows it still does not occur, because the ratio starts
  two orders of magnitude above 1.

## 2. Why no threshold exists anyway — the ratio's level

| bar | points with c > 0 | min g/c | median | max | points with **g/c < 1** |
|---|---|---|---|---|---|
| BAR-TO | 120 of 120 | **2.37** | 21.3 | 2127.6 | **0** |
| BAR-INC | 47 of 120 | **2.23** | 7.8 | 738.8 | **0** |

Minimum g/c by cell runs 2.37 (small STOP15) to 31.8 (small G200) on BAR-TO. The cheapest
instrument in the run still moves more than twice what it costs at its worst share. Consequently
`cross_empirical` returns **no finite m\* in 12 of 12** IS cells, and the walk-forward's GATED arm
is identical to the do-nothing NEVER arm in every cell — a threshold rule that can never fire.

**DEGROSS has no honest cost at all**: `c_INC ≤ 0` at **all 30** of its points (it is a trading-
cost *saving*), which is why its BAR-INC d is undefined. That is P3, held. G200's `c_INC > 0` at
only 12 of 30 points and BAND3's at 5 of 30 — the gates are, on the exact incremental bar, free
or better across most of the share axis. STOP15 is the one instrument that always costs
something (30 of 30).

## 3. Rule 8 walk-forward (d and m\* fitted on ≤ 2016-12-31, OOS read once)

Per (panel, instrument), mean over the ten shares, ALWAYS minus the do-nothing NEVER control:

| panel | instrument | ΔOOS Sharpe | ΔOOS CAGR | ΔOOS MaxDD (pp, + = shallower) |
|---|---|---|---|---|
| u56 | G200 | **+0.040** | −1.5 pp | +3.4 |
| u56 | BAND3 | **+0.046** | −1.3 pp | +3.3 |
| u56 | DEGROSS | −0.001 | −4.3 pp | +5.5 |
| u56 | STOP15 | −0.043 | −1.6 pp | **−0.9** |
| broad | G200 | +0.017 | −1.9 pp | +5.4 |
| broad | BAND3 | +0.009 | −1.9 pp | +6.0 |
| broad | DEGROSS | −0.001 | −3.6 pp | +5.8 |
| broad | STOP15 | −0.061 | −1.8 pp | **−1.9** |
| small | G200 | −0.051 | −2.6 pp | +11.3 |
| small | BAND3 | −0.043 | −2.5 pp | +11.1 |
| small | DEGROSS | +0.000 | −2.2 pp | +7.7 |
| small | STOP15 | −0.063 | −1.8 pp | +2.5 |

ALWAYS beats NEVER on OOS Sharpe in **5 of 12** (mean −0.0125); GATED is by construction 0 of 12.
The two gates pay on the large-cap panels and lose on the small one (ideas 39/49's inverted gate,
exactly as expected), DEGROSS is Sharpe-neutral and drawdown-positive (idea 66 again), and the
**per-name stop loses Sharpe *and deepens drawdown* on both large-cap panels** — the instrument
sold as insurance is the one that does not insure. d_IS < 0 in 5 of 12 cells against d_full < 0
in 5 of 12; the sign is stable, the magnitude is not.

## 4. KEEP-candidate walk-forward — the pick made on IS only

| panel | selector | pick | IS Sharpe | OOS CAGR | OOS Sharpe | OOS MaxDD | OOS-4b | failing bar |
|---|---|---|---|---|---|---|---|---|
| u56 | IS_SHARPE | G200, m = 0.05 | 1.376 | 25.4% | 0.969 | −34.5% | **no** | DD |
| u56 | IS_4bMARGIN | OFF, m = 0.53 | 1.122 | 15.6% | 1.197 | −21.2% | **no** | DD |
| u56 | control (OFF, 0.53) | — | 1.122 | 15.6% | 1.197 | −21.2% | **no** | DD |
| broad | IS_SHARPE | OFF, m = 0.05 | 1.247 | 19.1% | 0.888 | −28.0% | **no** | H1, DD |
| broad | IS_4bMARGIN | DEGROSS, m = 0.10 | 1.147 | 11.8% | 0.893 | −20.4% | **no** | H1, DD |
| small | IS_SHARPE | OFF, m = 0.70 | 0.767 | 8.7% | 0.584 | −37.2% | **no** | all five |
| small | IS_4bMARGIN | DEGROSS, m = 1.00 | 0.767 | 6.9% | 0.638 | −23.1% | **no** | all five |

**0 of 9 IS-chosen picks pass the OOS-window 4b**, every large-cap failure on the drawdown cap
(20.2% = 0.60 × SPY's OOS MaxDD). This is the honest reading of the 18 full-sample 4b passes
below: they are hindsight picks off a 150-book grid, and no prospective selector finds one.

## 5. Both KEEP paths, all 150 grid points

* **4a**: 38 of 150 at 10 bps, **95 of 150 at 25 bps** — the count rises with cost because RULES
  v1 degrades faster than these books do (v1 falls 0.664 → 0.317 Sharpe on u56).
* **4b (full sample)**: 18 of 150 at 10 bps, 10 at 25 bps; OOS-window 4b 18 and 12. **All 18 are
  instrument arms** — the base book never passes on its own, so on this share axis the gate or
  the de-gross lever is what earns the pass.
* Best full-sample cells: `u56 BAND3 m = 0.70` (11.3% / 1.198 / −16.0%, halves 1.237/1.173, OOS
  1.257, 3.9× turnover) and `u56 BAND3 m = 0.53` (12.7% / 1.176 / −18.2%, halves 1.186/1.179,
  OOS 1.248, 5.9× turnover, **still passing at 25 bps**). `broad G200/BAND3 m = 0.40` also pass
  at 25 bps and pass 4a — a contrast with idea 137's "broad @25 bps is the wall", which was
  measured on sleeve arms, not on this book family. **None of these is proposed**: section 4
  shows no prospective selector reaches them, and they are ideas 57/94's `band3-dg` family at a
  new book share, not a new instrument.

## 6. Predictions

| | prediction | outcome |
|---|---|---|
| P1 | reproduction [a]–[c] pass | **HELD** (6 of 6, identity at 0.00e+00) |
| P2 | d straddles zero in the large majority of cells | **FAILED — the informative failure** (5 of 12 on BAR-TO, 2 of 7 on BAR-INC) |
| P3 | DEGROSS's cost may be negative/flat, d undefined rather than zero | **HELD** (c_INC ≤ 0 at all 30 points) |
| P4 | the stop is the instrument most likely to show d < 0 | **HALF-HELD** (d < 0 in 3 of 3 panels but distinguishable in only 1) |
| P5 | no new book, no KEEP | **HELD** (0 of 9 IS-chosen picks pass OOS 4b) |

## What may be said, and what may not

May: *"An instrument's value and its cost are both proportional to the names it moves, so their
ratio is roughly scale-free — and on every instrument the project has priced, that ratio is
2.2×–2100× at every book share tested. No instrument on idea 74's menu is anywhere near too
expensive to run, so 'stop using it above m' is not a statement the data can support."*

May **not**: *"value and cost decay at the same rate"* (they do not — d is significantly non-zero
in 7 of 12 cells), nor any drawdown budget quoted as a **level**. Idea 69's "set g from a target
MaxDD" survives as an exposure rule but not as a price argument.

## Caveats (carried, not buried)

* **Survivorship.** All three panels are current-constituent lists (idea 54); small is the
  sub-$2B screen's *survivors* since 2010. Levels biased up; d compares shares within a panel.
* The 200d/vol20 gate is **inverted** on the small panel (ideas 39/49) — its G200/BAND3 rows
  describe an instrument known not to work there, which is why it is the panel where the two
  gates lose OOS Sharpe.
* A block bootstrap on one realised path measures sampling error around that path, not
  uncertainty across worlds (idea 159's caveat).
* c is held at its point estimate inside the bootstrap (idea 159's scheme), so the intervals
  understate uncertainty in d. Wider true intervals would move cells *toward* "straddles zero",
  i.e. toward idea 159's result and away from this run's headline — the failure of P2 is
  therefore conservative in the wrong direction and should be re-tested with c resampled too.
* BAR-TO replaces idea 159's BAR-OVL by necessity (see above); the two coincide only when the
  instrument purely adds trades.
* Ideas 38 (calendar-day index) and 126 (t+1 execution) carry over.

Script `research/backtests/2026-09-05_is-the-value-cost-parallelism-general_cloud.py`; console,
`.grid.csv` (150), `.curve.csv` (120), `.dslope.csv` (24), `.walkforward.csv` (36),
`.keepcandidate.csv` (9) alongside.
