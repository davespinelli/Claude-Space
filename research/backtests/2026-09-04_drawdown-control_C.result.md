# Idea 22 — `drawdown-control` (lane C, 2026-09-04) — **KILL**

**Question, verbatim from QUEUE:** *"v1 with book-level rule: if book drawdown > 8%, halve
exposure until new high."*

**Verdict: KILL, on all three books and both universes, and the mechanism is now priced.**
0 of 288 treated arms passes 4b on both universes; 269 of 288 lose Sharpe against their own
control; 252 of 288 are dominated by a *static* gross cut that buys the same drawdown more
cheaply. Idea 40 reported this mechanism as a KILL on a different book; this run does the idea
as literally worded on the live book, adds the control idea 66 made mandatory, and prices the
instrument on idea 74's axis.

Script: `research/backtests/2026-09-04_drawdown-control_C.py` ·
console `…_C.console.txt` · grid `…_C.grid.csv` (882 points) · ladder `…_C.ladder.csv` ·
rates `…_C.rates.csv`.

## Design

* **Books** (pre-chosen, never selected): `V1` = RULES v1 exactly as live (idea 22's literal
  subject); `CAND20` = idea 2's standing 4b KEEP-candidate; `EWall` = idea 72/10's
  `B136/EWall`. **Universes:** `universe.json` (56) and `universe_broad.json` (136), both
  always reported.
* **Two tuned parameters only:** trigger `D ∈ {4,6,8,10,12,15}%` and exposure multiplier while
  triggered `k ∈ {0.00,0.25,0.50,0.75}` (0.50 = "halve"). **RESET is an arm, not a dial** —
  `high` (idea 22 as worded: cut until a new equity high) and `recover` (release at
  drawdown shallower than `D/2`) are both fully reported, and every walk-forward selection runs
  *within* one reset arm so no selection ever spans three dials.
* 6 cells × (1 control + 48 treated) × 3 cost levels (5/10/25 bps) = **882 points, all reported.**
* Weekly, t+1 execution, long-only, no leverage. The drawdown state machine reads the book's own
  **net** equity through close *t−1* only.
* **Harness sanity:** the control reproduces `engine.backtest` with `max|diff| = 0.0` in every
  cell, and reproduces idea 2's published KEEP row (12.7% / 1.093 / −18.3%, halves 1.088/1.103)
  and idea 10's `B136/EWall` (10.7% / 1.027 / −17.7%) to the decimal before any new number is read.

## 1. The literal rule (D = 8%, k = 0.50, new-high reset), 10 bps

| universe | book | rule | control | dSharpe | dCAGR | dMaxDD bought | days cut | episodes | 4b |
|---|---|---|---|---|---|---|---|---|---|
| u56 | V1 | 3.7% / 0.485 / −12.1% | 6.5% / 0.666 / −13.8% | **−0.182** | −2.81pp | +1.73pp | 52.2% | 5 | fail H1,H2,OOS,CAGR |
| u56 | CAND20 | 8.4% / 0.917 / −14.2% | 12.7% / 1.093 / −18.3% | **−0.176** | −4.26pp | +4.08pp | 47.8% | 7 | fail H1,CAGR |
| u56 | EWall | 6.7% / 0.833 / −12.5% | 10.4% / 1.050 / −15.9% | **−0.217** | −3.76pp | +3.39pp | 47.5% | 6 | fail H1,CAGR |
| broad | V1 | 3.2% / 0.440 / −15.3% | 6.4% / 0.640 / −21.2% | **−0.200** | −3.28pp | +5.90pp | 65.4% | 6 | fail H1,H2,OOS,CAGR |
| broad | CAND20 | 7.5% / 0.749 / −15.3% | 13.1% / 0.958 / −20.1% | **−0.209** | −5.62pp | +4.77pp | 59.9% | 9 | fail H1,H2,OOS,CAGR |
| broad | EWall | 7.2% / 0.882 / −14.3% | 10.7% / 1.027 / −17.7% | **−0.146** | −3.53pp | +3.36pp | 42.0% | 5 | fail H2,OOS,CAGR |

Six cells, six negative Sharpe deltas, and in every one the rule **converts a 4b-passing or
near-passing book into a 4b failure on the CAGR floor**. It does exactly what it says on the
tin — drawdown improves in 6/6 — and pays more than the drawdown is worth.

## 2. P1–P4, all four pre-registered predictions hold

* **P1 (Sharpe-negative): HOLDS.** 269 / 288 treated arms lose Sharpe against their own cell
  control at 10 bps; median dSharpe −0.072 to −0.202 by cell. The best arm in the whole run is
  `EWall broad D4%/k0.75/recover` at **+0.003**.
* **P2 (the de-levering ratchet): HOLDS.** Median share of days spent cut is **50.5%** under the
  `high` reset and **37.5%** under `recover` — reproducing idea 40's 52–79% on a different book
  and confirming its diagnosis: cutting exposure slows the recovery that is required to un-cut,
  so a "tail control" spends half its life as a permanent de-levering. The `recover` reset
  removes ~13pp of that and is better in most arms, but does not save the instrument.
  **The extreme case is structural, not a parameter choice:** at `k = 0.00` the book earns
  nothing, so it can never make a new high *and* can never recover to `−D/2` — **both reset
  rules are absorbing.** `u56 CAND20 D4%/k0.00` exits in 2011 and never returns: 97.3% of days
  cut, 0.0% in 2020 and 0.0% in 2022, full-sample −0.1% / Sharpe −0.049, and its second-half
  Sharpe is undefined because the return stream is exactly zero. One quarter of the k-grid is
  degenerate by construction, and that is a property of the rule family, not of the grid.
* **P3 (dominated by a static gross cut): HOLDS.** Median exchange rate **1.018 pp of CAGR
  surrendered per pp of MaxDD bought**, against the static-gross lever's **0.305–0.697** in the
  same cells (mean 0.566) — the drawdown rule pays roughly **1.8× the going price**. 252 / 288
  arms are dominated. Held against a *static* book at the arm's own realised average gross,
  the mean deltas are negative on all three axes in 5 of 6 cells, and only **3 of 288 arms beat
  their matched static book on both Sharpe and MaxDD** — by +0.001 to +0.003 of Sharpe.
* **P4 (no conversion): HOLDS.** 0 treated arms pass 4b on both universes; **no arm converts a
  cell its control failed.** 18 arms pass 4b on `u56` — all in `CAND20`, where the *control*
  already passes and every one of the 18 is either the mildest corner of the grid (D=15%, which
  never triggers, i.e. literally the control) or a strictly worse version of it.
* **4a census, the pathology 4b exists to catch:** 4a passes *rise* with cost — 10 / 62 at
  10 bps and 30 / 74 at 25 bps across the two universes — while 4b passes fall to **0 of 294 at
  25 bps**. Cutting exposure beats RULES v1 on 4a precisely because RULES v1 is weak.

## 3. Walk-forward (PROTOCOL rule 8) — the rule is not selectable

Parameters chosen on 2009–2016 alone, 2017–2026 untouched, 10 bps, two selection rules fixed
before any OOS number was read.

* **S1 (argmax IS Sharpe) picks the do-nothing corner `D=15% / k=0.75` in 12 of 12 cells.** In
  the 4 cells where that arm never triggers it is bit-identical to the control; in the 8 where
  it does bind it **loses OOS Sharpe in 8 of 8** (−0.013 to −0.066). Mean OOS Sharpe: control
  **0.922**, S1 **0.900**.
* **S2 (4b-aware) PICKS NOTHING in 10 of 12 cells** — no in-sample point cleared the IS 4b bars —
  and in the 2 where it picks (`broad/EWall`) it picks the same do-nothing arm and gives up
  0.066 of OOS Sharpe. This is the same structural outcome as ideas 39, 40, 46 and 49.
* OOS references: SPY 15.5% / 0.884 / −33.7%; RULES v1 7.8% / 0.751 / −13.8%.

## 4. Where the instrument is *not* dominated, and why it still fails

36 of 288 arms beat the static gross lever on the CAGR-per-drawdown axis, and **24 of them are
in one cell: `broad / V1`** — the worst book in the run (0.640 Sharpe, −21.2% MaxDD, failing all
five 4b bars including the drawdown cap). There the control's drawdown is deep and its static
gross slope is shallow (0.305), so a state-dependent cut is comparatively cheap. That is a
statement about how bad the book is, not about the instrument: 47 of its 48 arms still lose
Sharpe, and no arm gets it within reach of any 4b bar. **A drawdown rule is cheapest exactly
where the book is not worth running.**

One honest positive, recorded because it runs against the KILL: the rule *reduces* turnover
(u56 `CAND20` 9.63× → median 7.81×/yr), so none of the cost is a trading-cost story — the loss
is entirely the exposure that is missing during recoveries.

## 5. Bear-market shape — the rule does not even buy the bear

2022 is where a drawdown control should earn its keep. It does not: `u56 CAND20` returns −9.0%
un-cut and −8.2% with the literal rule (SPY −18.2%), and `broad EWall` is actually **worse**
(−10.1% vs −8.4%). 2020 is where it is paid for: `u56 CAND20` +15.4% → +2.6%, `broad CAND20`
+12.2% → +0.9%. The only arms that materially improve 2022 are the absorbing `k=0.00` ones,
which return +0.0% in every year because they are in permanent cash. The instrument is late to
a fast crash and still invested through the slow one — consistent with idea 62's framing.

## Recommended RULES wording

**None.** Do not add a book-level drawdown trigger to RULES. If the Sunday review wants
drawdown reduced, the supported instrument is the exposure number itself (idea 66: gross is an
exact, Sharpe-neutral lever), priced at 0.31–0.70 pp of CAGR per pp of MaxDD, against this
rule's 1.02. Idea 22 is now answered twice — idea 40 on the growth book, this run on the live
book — and should be closed rather than re-parameterised.

## Caveats

* **Survivorship:** both lists are current-constituent, so all absolute CAGRs are optimistic.
  The result is a set of treatment deltas on shared panels and shared days, which is far less
  exposed; and survivorship runs *against* a drawdown control (a list of survivors has shallower
  drawdowns than the live universe did), so the KILL is conservative.
* The exchange-rate comparison uses the arm's realised *average* gross to pick the matched
  static point; matching on average gross is not matching on the whole exposure path, and the
  ladder step is 0.05 in multiplier. Both are stated in the script.
* The `high` reset re-arms on a new all-time high of the *net* equity of that arm, so trigger
  paths differ slightly between cost levels; each cost level is simulated separately rather than
  re-priced, so the 5 and 25 bps rows are internally consistent.
