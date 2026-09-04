# Idea 94 — drawdown-insurance-price-list (lane B, 2026-09-04)

**Verdict: PARK on the price list as worded; two 4b KEEP-candidates and three 4a
KEEP-candidates fall out of it; the per-name trailing stop is a hard KILL.**

Script `research/backtests/2026-09-04_drawdown-insurance-price-list_B.py`, console
`…_B.console.txt`, data `…_B.pricelist.csv` (204 priced arm-cells) and `…_B.grid.csv`
(192 arm-points). Engine equivalence with `engine.backtest` is EXACT (max|diff| = 0.0)
on both universes.

## What was run

One simulator, one set of base books, one set of days, one matched-gross control.
Idea 22 priced the book-level drawdown control on the *gated* books, which makes the gate
itself invisible; this run takes the **ungated** book as the common base so every
instrument — gates included — is an overlay priced on the same axis:

    rate = (CAGR_control − CAGR_arm) / (|MaxDD_control| − |MaxDD_arm|)   pp CAGR per pp MaxDD

Books (all at 75% gross, all reported): `V1u` (v1's composite with /sqrt(vol20), top-5 at
15%, ungated), `TOP20` (composite without the vol scaler, top-20, ungated), `EWall`
(equal-weight every name, no ranking). Universes: universe.json (56) and
universe_broad.json (136). Costs 10 and 25 bps. 16 arms + a 19-point static-gross ladder
per cell; 12 cells; nothing selected.

Each gate is run in two conventions because they are different instruments: `-dg`
de-grosses (a gated-out name's weight goes to cash) and `-rw` rebuilds the book at full
gross among the gated-in names (this is how live RULES v1 and idea 57 are written).

## THE MENU (10 bps, median across the 6 book×universe cells, cheapest first)

| instrument | price (pp CAGR / pp MaxDD) | cells priced | median DD bought | median ΔSharpe | median turnover |
|---|---|---|---|---|---|
| `band3-rw`  200d ±3% band, reweighted | **0.18** | 6/6 | 3.06 pp | −0.001 | 10.8x |
| `g200-rw`  200d gate, reweighted | **0.22** | 6/6 | 2.55 pp | −0.005 | 11.2x |
| `vol60-rw`  vol20<0.60, reweighted | 0.32 | 4/6 | 3.90 pp | −0.001 | 11.7x |
| `vol60-dg`  vol20<0.60, to cash | 0.32 | 4/6 | 5.55 pp | +0.000 | 11.4x |
| `v1gate-rw`  200d AND vol20, reweighted | 0.35 | 6/6 | 4.91 pp | −0.047 | 11.7x |
| `ebud-0.10`  entry-only turnover budget | 0.40 | 4/6 | 2.40 pp | −0.004 | 9.2x |
| `band3-dg`  200d ±3% band, to cash | 0.44 | 5/6 | 3.38 pp | −0.010 | 10.8x |
| `g200-dg`  200d gate, to cash | 0.48 | 5/6 | 2.68 pp | −0.014 | 11.0x |
| `v1gate-dg`  the live gate, to cash | 0.51 | 5/6 | 6.65 pp | −0.034 | 11.2x |
| **`gross-m`  static exposure lever (REFERENCE)** | **0.57** | — | any | 0.000 | unchanged |
| `ddctl-8/.5/recover`  book DD control | 0.60 | 6/6 | 7.08 pp | −0.125 | 9.0x |
| `abs12-dg`  absolute momentum, to cash | 0.61 | 4/6 | 1.14 pp | −0.021 | 10.6x |
| `abs12-rw`  absolute momentum, reweighted | 0.66 | 4/6 | 0.59 pp | −0.028 | 10.8x |
| `ddctl-8/.5/high`  book DD control, new-high reset | 0.69 | 6/6 | 7.08 pp | −0.150 | 8.1x |
| `ebud-0.20` | 0.91 | 3/6 | 0.06 pp | −0.002 | 11.0x |
| `stop15` / `stop25`  per-name trailing stop | **not on the menu** | 0/6 | −0.69 / −1.25 pp | −0.033 / −0.006 | 12.5x / 11.3x |

At 25 bps the tiers are unchanged (gates 0.23–0.55, lever 0.52, DD control 0.54, stops
still unpriceable); only the order *within* the gate tier moves.

## Findings

**1. P1 REFUTED — the gate family is genuinely cheaper than holding less.** 48 of 68
priced arm-cells beat the static-gross lever at 10 bps. Idea 22's "the drawdown rule is
dominated by de-grossing" is specific to the **book-level** DD control, which this run
reproduces (0.60 / 0.69 vs the 0.57 lever, and it is the only instrument that costs
ΔSharpe > 0.12 in every cell). A per-name signal that turns exposure off *before* the
book has lost money is not the same object as a rule that reacts to the book's own equity.

**2. The per-name trailing stop buys NEGATIVE drawdown in 10 of 12 cells and zero in the
other 2.** It never bought a single pp of MaxDD in any cell, at either depth, on either
universe. It is not dear insurance — it is not insurance. Idea 9 measured 0.17–0.53 pp per
pp; on a matched harness with the base book held fixed, the denominator is the wrong sign.
Mechanism: the stop sells into the drawdown and re-buys at the next weekly rebalance,
which converts a paper drawdown into a realised one and adds 1.7–2.4x/yr of turnover.

**3. P3 REFUTED — the gates' drawdown benefit is mostly SELECTION, not de-grossing.**
The `-rw` forms hold full 75% gross at all times yet buy a median 2.69 pp of MaxDD against
the `-dg` forms' 3.50 pp, at roughly half the CAGR cost. The de-grossing half of a trend
gate is the *expensive* half. This is the opposite of the idea 73 / 21 artefact story,
which applies to screens that shrink the book, not to gates that reallocate inside it.

**4. The entry-only turnover budget is a de-grossing in disguise, and only where the book
is fast.** It never binds on `EWall` (0.83x/yr turnover, ΔCAGR and ΔMaxDD both exactly
0.000 in all 4 cells). On `V1u` (23–29x/yr) `ebud-0.10` buys 6.4/14.3 pp of MaxDD, but it
does so by holding the book at 69% of its target gross — it prices at 0.28–0.56, i.e.
around the lever, which is what it is.

**5. Absolute momentum is the dearest real gate** (0.61/0.66) and buys the least drawdown
(0.59–1.14 pp median). Idea 62's claim that abs momentum is the *slow-bear* instrument is
not contradicted, but on a whole-sample drawdown axis it is the worst trend instrument here.

## Rule 8 walk-forward — why this is PARK and not KEEP

Parameters (instrument family) chosen on 2009–2016 only, evaluated untouched on 2017–2026.
S1 = cheapest IS price among arms that bought ≥1 pp of IS drawdown.

| cell | S1 pick (IS) | OOS rank of that pick | OOS Sharpe | control | RULES v1 | SPY |
|---|---|---|---|---|---|---|
| u56 / EWall @10 | `band3-rw` | **1 of 12** | 1.203 | 1.136 | 0.747 | 0.882 |
| u56 / EWall @25 | `band3-rw` | **1 of 12** | 1.143 | 1.125 | 0.399 | 0.882 |
| broad / EWall @25 | `vol60-dg` | **1 of 12** | 1.102 | 1.091 | 0.155 | 0.882 |
| broad / V1u @10 | `g200-rw` | **1 of 6** | 0.590 | 0.573 | 0.576 | 0.882 |
| broad / V1u @25 | `g200-rw` | **1 of 6** | 0.169 | 0.146 | 0.155 | 0.882 |
| u56 / V1u @10 | `ebud-0.10` | 9 of 12 | 0.518 | 0.714 | 0.747 | 0.882 |
| u56 / V1u @25 | `ebud-0.10` | 10 of 12 | 0.211 | 0.359 | 0.399 | 0.882 |
| u56 / TOP20 @10 | `ddctl-recover` | 10 of 11 | 1.051 | 1.168 | 0.747 | 0.882 |
| u56 / TOP20 @25 | `ddctl-recover` | 11 of 11 | 0.925 | 1.072 | 0.399 | 0.882 |
| broad / TOP20 @10 | `ebud-0.10` | 11 of 11 | 0.854 | 0.930 | 0.576 | 0.882 |
| broad / TOP20 @25 | `ebud-0.10` | 10 of 11 | 0.751 | 0.807 | 0.155 | 0.882 |
| broad / EWall @10 | `stop25` | unpriceable OOS | 1.095 | 1.102 | 0.576 | 0.882 |

Median Spearman(IS price, OOS price) across the 12 cells = **0.442**, per-cell range
−1.00 to +0.93. S1 lands on the OOS-cheapest arm in 5 of 12 cells and in the bottom third
in 6 of 12. **The tier structure survives out of sample; the per-instrument ordering does
not.** RULES may quote "per-name gates are cheaper than de-grossing, which is cheaper than
book-level drawdown rules, and stops are not insurance" — it may not quote a number for
one instrument against another inside the gate tier.

## KEEP-candidates falling out of the run (by-products, not the subject)

Passing PROTOCOL **4b on BOTH universes at BOTH 10 and 25 bps** (SPY: 15.2% CAGR, Sharpe
0.889, halves 0.957/0.834, OOS 0.882, MaxDD −33.7%; bars are Sharpe > SPY in both halves
and OOS, MaxDD ≤ 20.2%, CAGR ≥ 10.66%):

| book | universe | cost | CAGR | Sharpe | MaxDD | H1/H2 | OOS Sh | turnover |
|---|---|---|---|---|---|---|---|---|
| `EWall + vol60-dg` | u56 | 10 | 11.6% | 1.133 | −16.9% | 1.156/1.113 | 1.186 | **1.39x** |
| `EWall + vol60-dg` | u56 | 25 | 11.4% | 1.113 | −16.9% | 1.137/1.091 | 1.164 | 1.39x |
| `EWall + vol60-dg` | broad | 10 | 12.4% | 1.138 | −18.7% | 1.255/1.027 | 1.122 | **1.36x** |
| `EWall + vol60-dg` | broad | 25 | 12.1% | 1.119 | −18.7% | 1.238/1.006 | 1.102 | 1.36x |
| `EWall + band3-rw` | u56 | 10 | 12.2% | 1.161 | −17.7% | 1.210/1.129 | 1.203 | 4.32x |
| `EWall + band3-rw` | u56 | 25 | 11.5% | 1.098 | −17.9% | 1.145/1.067 | 1.143 | 4.32x |
| `EWall + band3-rw` | broad | 10 | 11.7% | 1.069 | −18.5% | 1.172/0.979 | 1.076 | 4.80x |
| `EWall + band3-rw` | broad | 25 | 10.9% | 1.002 | −18.7% | 1.107/0.911 | 1.010 | 4.80x |

`band3-rw` is idea 57's `ew-band3` and this is an independent confirmation of it at 25 bps
on both universes (idea 58 asked whether it survives the cost/lag protocol; on cost alone
it does). **`vol60-dg` is new**: a pure short-horizon volatility gate with *no trend
component at all*, holding cash instead of the excluded names, at 1.4x/yr turnover — a
third of `band3-rw`'s and a fifth of `g200-rw`'s. It is the only instrument in the run
that is Sharpe-neutral-or-positive against its own control (+0.009/+0.000/+0.016/+0.007
across the four cells) while buying 5.6–6.7 pp of MaxDD. This is a direct partial answer to
open idea 56.

Passing **4a on BOTH universes at BOTH costs** (Sharpe > live RULES v1 in both halves,
MaxDD no worse) — the run's only 4a passes, all on `EWall`, all in the `-dg` convention:
`band3-dg` (u56 8.7% / 1.206 / −12.1%; broad 8.0% / 1.106 / −12.2%), `g200-dg`,
`v1gate-dg`. `band3-dg` dominates live RULES v1 on every axis at once: +2.2 pp CAGR,
+0.54 Sharpe, 1.7 pp *less* drawdown, and 1.8x/yr turnover against v1's 23x. It fails 4b
only on the CAGR floor (8.7% vs 10.66%), which is exactly what PROTOCOL 4b's rationale
paragraph says the live book's low return does to a drawdown-first design.

## Caveats, stated plainly

- **The two candidate parameters were not fitted in this run, but they were fitted
  historically on the same data.** The 3% band comes from idea 57 and the 0.60 vol
  threshold from live RULES v1; both were chosen on windows that overlap the "OOS" period
  here. The IS/OOS split above is therefore a validity check on the *price ordering*, which
  is what this run tuned (one parameter: the instrument family), and NOT a clean
  out-of-sample test of the 0.60 threshold. A threshold sweep is the required next step
  before `vol60-dg` can be proposed to a Sunday review.
- **SURVIVORSHIP:** both universes are current-constituent lists, so every absolute CAGR is
  optimistic. The price list is a set of within-cell deltas on matched days, which is far
  less exposed than the levels, but `EWall` on a survivorship-clean panel would be worse.
- `ebud` is reported as priced in only 4 of 6 cells because it does not bind on `EWall`;
  those two cells are exact zeroes, not missing data.
- Calendar-day index (open idea 38) is unfixed and affects every number here equally.

## Recommended follow-ups (queued)

95. `vol-threshold-sweep-on-ewall` — sweep the vol20 threshold in {0.40,0.50,0.60,0.80,1.0}
    and the de-gross/reweight convention on `EWall`, both universes, 10/25 bps. The 0.60 in
    `vol60-dg` is inherited from RULES v1 and has never been re-derived on this book.
96. `stop-as-negative-insurance` — the stop's ΔMaxDD is negative in 10/12 cells; test
    whether an *intra-week* exit (daily gate check, weekly rebalance) reverses the sign, or
    whether selling into drawdowns at a weekly grid is what does it.
97. `price-list-tier-bar` — propose the tier ordering (per-name gate < static gross <
    book-level DD rule < stop) as the statement PROTOCOL quotes, with the per-instrument
    price explicitly marked unstable (median Spearman 0.44, 5/12 rank-1).
