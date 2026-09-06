# Idea 74 — drawdown-instrument-exchange-rate (cloud, 2026-09-06)

**Verdict: ANSWERED. The menu the queue asked for is delivered and its ORDERING is stable —
and the published pairwise numbers it replaces were wrong in ordering, not just in level.
As a per-cell SELECTOR the same menu is a KILL (rule 8: IS-cheapest stays cheapest OOS in
3/25 cells). No RULES change, no new KEEP; one PARK by-product (below). RULES.md, scan.py,
bot.py and baseline.py untouched.**

Script `research/backtests/2026-09-06_drawdown-instrument-exchange-rate_cloud.py`, importing
idea 245's module (base books, simulator, instruments) and through it idea 94's `run_stop`.
2 panels x 2 instrument-free base books x 6 families x 6 strength levels x 2 cost rungs =
**296 backtests, all reported**; exactly TWO tuned dimensions (family, strength). The budget
grid T ∈ {2,4,6,8,10} pp is a reporting axis — all five printed, reachable or not.

Harness: **[A]** no-instrument == `engine.backtest`, max|diff| **0.000e+00**; **[C]** stop ==
idea 94's published `run_stop`, **0.000e+00** at every depth; **[D]** every published rate
recomputed from the committed grid CSV, max|diff| **0.000e+00**.

## 1. The menu (median exchange rate over the 4 panel x book cells, 10 bps)

pp of CAGR surrendered per pp of MaxDD bought. **Lower = cheaper. De-gross is the reference:
an instrument above it is dominated by simply holding less.** "—" = the family's whole ladder
cannot buy that much drawdown.

| instrument | T=2 pp | T=4 | T=6 | T=8 | T=10 | reach (max pp) |
|---|---|---|---|---|---|---|
| MA re-entry band | **−0.06** | **0.23** | **0.36** | — | — | 0.02–6.87 |
| book DD control (idea 40) | 0.29 | 0.40 | 0.53 | **0.56** | — | 7.49–9.42 |
| absolute momentum | 0.41 | 0.53 | — | — | — | −0.11–5.05 |
| 200d-type MA gate | 0.44 | 0.42 | 0.46 | — | — | 1.21–7.02 |
| **de-gross (reference)** | 0.63 | 0.62 | 0.62 | 0.61 | **0.61** | 12.74–14.86 |
| per-name trailing stop | **0.89** | — | — | — | — | 1.85–2.73 |

Two structural facts the pairwise literature could not see:

**(a) The published ordering is REVERSED.** Idea 9 priced the stop at 0.17–0.53 and idea 57
priced the 200d gate at 4.45, i.e. the stop looked ~10x cheaper than the gate. On one matched
book at one cost the stop is **the dearest instrument the project owns (0.89)** and the gate is
**cheap (0.44)** — and the stop is the ONLY family that loses to de-gross (beats it in 1/3
comparable cells, median gap **+0.28**). Every other family beats de-gross where comparable:
200d **7/7**, band **5/5**, abs **4/4**, ddctl **13/15** (median gaps −0.20, −0.47, −0.17,
−0.17). Those three published numbers were not comparable and should not be quoted again.

**(b) Rate is not the whole menu — REACH is.** The stop cannot buy 4 pp of drawdown at any
depth in any cell; abs stops at ~5 pp, the gates at ~7 pp, ddctl at ~9.4 pp. **De-gross is the
only instrument that reaches an arbitrary budget**, and its rate is flat in the budget
(0.63 → 0.61 from T=2 to T=10) because it is an exact lever. So the correct reading is a
two-column menu: for budgets ≤ 6 pp use the cheap gates; above that there is no alternative to
holding less. At 25 bps every rate rises and every reach shrinks (band 0.00/0.37/0.46, ddctl
0.30/0.45/0.58/0.56, dg 0.62/0.61/0.61/0.60/0.60, stop 1.63 and unreachable beyond T=2).

## 2. Rule 8 — walk-forwarding the menu itself

Family AND level chosen on the 2009–2016 exchange rate only; 2017–2026 read once.

- **IS-cheapest family stays cheapest OOS in 3/25 cells.** Mean rate regret **+0.291**,
  median +0.226.
- The IS window picks **de-gross 21/25 times**; OOS the cheapest is **ddctl 12, band 9**,
  de-gross only 2.
- The mechanism is idea 117's, restated on this axis: the IS window's controls draw down only
  −11.3% to −15.3% while OOS they draw −19.2% to −25.7%. **A window with little drawdown to buy
  makes every instrument look dear** (dg's own rate is 0.97–1.33 IS vs 0.59–0.82 OOS), and
  de-gross wins IS only because it is the one family that can still reach the budget there.
- OOS book metrics of the rule-8 picks are sound but unremarkable: e.g. u56/CAND20/T=2 picks
  dg/0.8 → 13.3% / 1.175 / −17.8% vs RULES v1 7.7% / 0.747 / −13.8% and SPY 15.5% / 0.882 /
  −33.7%; broad/EWALL0/T=2 picks band/0.12 → 13.8% / 1.165 / −21.7%.

**Conclusion: the exchange rate is a valid REPORTING column and an invalid SELECTOR.** RULES may
quote the menu's ordering when a drawdown budget is set; it must not fit family or level per
window.

## 3. Both KEEP paths (all 144 arms at 10 bps)

4a 35/144, 4b 33/144; all four no-instrument controls fail BOTH paths on DD. Benchmarks: SPY
15.2% / 0.889 / −33.7% (halves 0.957/0.834, OOS 0.882); RULES v1 6.5% / 0.664 / −13.8% (u56).

**PARK by-product — `EWALL0 + 12% MA re-entry band` on u56.** 14.1% / **1.233** / −19.4%,
halves 1.268/1.211, OOS **1.272**, turnover **1.9x/yr**, and its exchange rate is **negative
(−0.26)**: it buys 3.1 pp of drawdown while *adding* 0.8 pp of CAGR. It survives 25 bps
(13.8% / 1.207 / −19.5%, OOS 1.245). It is the best 4b arm in the run. It is **PARK, not KEEP**,
for two stated reasons: (i) 12% is the **widest point of the ladder** and Sharpe is monotone
increasing across the whole width sweep while turnover falls 6.4x → 1.9x, so this is a grid edge,
not a located optimum (idea 240's exact lesson); (ii) it **fails 4b on `broad`** at both cost
rungs, on DRAWDOWN (−21.7% vs the −20.2% cap), so it is not cross-universe. Queue idea added.

Proposed RULES wording IF and only if the ceiling is located and the broad failure closes:

> Hold every name in the universe at equal weight, sized to 75% gross. A name is eligible once
> its close exceeds its own 200-day moving average by 12%, and stays eligible until its close
> falls 12% below that average; names between the two thresholds keep whatever state they last
> had. Re-evaluate weekly at the close and trade at the next close.

## 4. What this settles

1. The queue's deliverable exists: one ranked insurance menu, matched book and matched cost,
   with reach published beside rate.
2. Three published exchange rates (ideas 9, 57, 66) are re-quoted on one axis and their
   **ordering reverses**; the stop is the project's dearest drawdown instrument, not its cheapest.
3. The menu must be read as an ordering, never fitted per window — rule 8 rejects it as a
   selector at 3/25.

SURVIVORSHIP: both panels are current constituents; a survivor panel has shallower crashes, so
every instrument here is priced in a world with less drawdown to buy. The rate is a ratio of two
within-cell differences against the same control, which cancels most but not all of that bias.
