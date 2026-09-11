# Idea 785 (cloud lane, 2026-09-11) — is-the-EQUAL-WEIGHT-BAR-the-right-4b-COMPARAND-for-PROTOCOL-itself

**ANSWERED — NO. DO NOT WRITE AN EQUAL-WEIGHT BASKET INTO RULE 4b. All three equal-weight
wordings are INFEASIBLE (0 of 72 books pass), including the gross-matched one drafted
specifically to answer the fairness objection; the one feasible variant is feasible only on
the panel where it is a *weaker* bar than SPY. / KILL for the wording swap — PROTOCOL
unchanged.**

## Question

PROTOCOL rule 4b names SPY and nothing else. Idea 742 killed one standing candidate against
an equal-weight basket of its own panel; idea 787 re-priced the whole shelf and got **26 of
82 cells passing against SPY, 0 against either equal-weight bar**. The queue asks the level
up: not "does this book survive the swap" but **"is the equal-weight basket the comparand
PROTOCOL should name"** — draft the wording, and report how many committed 4b verdicts it
moves.

A comparand is not chosen by which books it kills. Five candidate wordings are scored on the
three properties a bar needs before it is worth writing into PROTOCOL: **feasibility** (some
book must be able to pass it — the record's own degeneracy principle applied to PROTOCOL),
**discrimination**, and **selection** (rule 8: a book chosen on the bar from the first half
alone must be worth holding in the second — the property neither 742 nor 787 measured).

## Gates — ALL PASS (after one declared failure, below)

| gate | what | result |
|---|---|---|
| G1 identity | `fast_backtest` vs `engine.backtest`, returns **and** turnover, one book per panel | **0.000e+00** (bar 1e-12) |
| G2 band | BAND-DG g=0.75 vs `baseline.rules_v2_weights` on each panel's own frame | **0.000e+00**, exact — the live book is on the grid, not a lookalike |
| G3 787 repro | W0 and W1 vs idea 787's committed `B_SPY` / `B_EWW10` digits, 4 cells × 5 stats | max \|d\| **4.991e-05** (bar 5e-4) |
| G4 gross | W2's realised daily gross vs the book's own **target** gross | max \|d\| **4.441e-16** (bar 1e-12) |
| G5 non-degenerate | the incumbent W0 must pass strictly inside 0–100% of the grid | **9 of 72 (12.5%)** |

**G4 failed on the first version and is reported, not hidden.** That version sized W2 to the
book's *realised* gross lagged one day, which the engine then lagged again: mean \|d\| read
**1.223e-02** and max **1.000** at band transitions. W2 was rebuilt to match the book's own
**target** gross on the same decision day — the gross a manager could actually size to —
before any pass count was read. The book's realised gross drifts from its own target by
**0.0457** on average (worst book); that drift is reported, not matched, because matching it
would require tomorrow's prices.

## The five candidate wordings

* **W0 SPY** — PROTOCOL verbatim. The incumbent and the control.
* **W1 EWP_FULL** — equal-weight, fully invested (gross 1.00), weekly, 10 bps, the book's own panel. This is 787's `B_EWW10`, the weaker of its two equal-weight bars.
* **W2 EWP_GROSS** — the same basket at **the book's own target gross**, rest in cash at 0%, daily. The wording drafted to answer the objection 742, 672 and 787 all raise: a book sitting 40% in cash is being asked to out-compound a 100%-invested basket.
* **W3 EWP_BH** — equal weight across the names priced on day 0, never rebalanced, 10 bps once.
* **W4 MAX_SPY_EWP** — must clear every leg against **both** SPY and EWP_FULL.

| panel | wording | CAGR | Sharpe | MaxDD | H1 | H2 | OOS CAGR | OOS Sharpe |
|---|---|---|---|---|---|---|---|---|
| U56 | W0_SPY | 15.11% | 0.8835 | −33.72% | 0.9595 | 0.8211 | 15.24% | 0.8721 |
| U56 | W1_EWP_FULL | 17.69% | 1.1237 | −29.09% | 1.2036 | 1.0598 | 18.35% | 1.1308 |
| U56 | W3_EWP_BH | 21.41% | 1.0179 | −46.09% | 1.2569 | 0.9115 | 23.91% | 0.9934 |
| B136 | W0_SPY | 15.23% | 0.8890 | −33.72% | 0.9566 | 0.8340 | 15.45% | 0.8820 |
| B136 | W1_EWP_FULL | 18.95% | 1.1238 | −32.71% | 1.2354 | 1.0240 | 18.62% | 1.1022 |
| B136 | W3_EWP_BH | 20.07% | 1.0809 | −32.86% | 1.2666 | 0.9582 | 20.78% | 1.0401 |
| SMALL439 | W0_SPY | 14.13% | 0.8615 | −33.72% | 0.8907 | 0.8577 | 15.45% | 0.8820 |
| SMALL439 | W1_EWP_FULL | 13.12% | 0.6770 | −46.03% | 0.7969 | 0.6124 | 12.88% | 0.6351 |
| SMALL439 | W3_EWP_BH | 7.06% | 0.4343 | −45.38% | 0.6176 | 0.3009 | 5.15% | 0.3402 |

## Two dials (PROTOCOL rule 4), all 20 points reported

BAR FORM (5) × CLAIM SET {ALL, GATED, U56, SHELF} (4). Reported, never selected: panel (3),
family (4: BAND-DG, MA-RS, CAND20, EWALL), gross (3), cadence (2) = a 72-book grid, 5 legs.

| claim set | n | W0_SPY | W1_EWP_FULL | W2_EWP_GROSS | W3_EWP_BH | W4_MAX |
|---|---|---|---|---|---|---|
| ALL | 72 | **9** | 0 | 0 | 3 | 0 |
| GATED | 54 | **9** | 0 | 0 | 1 | 0 |
| U56 | 24 | **6** | 0 | 0 | 0 | 0 |
| SHELF | 9 | **9** | 0 | 0 | 0 | 0 |

**B1 — INFEASIBLE: W1_EWP_FULL, W2_EWP_GROSS, W4_MAX_SPY_EWP, at every one of the four claim
sets.** W3_EWP_BH passes 3 of 72 — **all three on SMALL439**, the one panel where buy-and-hold
equal weight is a *weaker* bar than SPY (7.06% CAGR / 0.4343 Sharpe vs SPY's 14.13% / 0.8615).
It is feasible for the wrong reason: the bar is bad, not the books good. On U56 it passes 0.

**B2 — MOVEMENT.** Every equal-weight wording moves the same 9 verdicts and they all move the
same way: **9 convicted, 0 acquitted** (W3 also acquits the 3 small-cap books). **The
standing shelf is 100% convicted and 0% acquitted by all three forms** — 787's result
replicated on an independently built grid.

## The finding underneath: the wording and the two constants are not separable

The binding leg **changes completely** when the comparand is gross-matched:

| wording | H1 | H2 | OOS | **DD** | **CAGR** |
|---|---|---|---|---|---|
| W0_SPY | 24 | 27 | 27 | 37 | 41 |
| W1_EWP_FULL | 60 | 47 | 46 | 37 | 51 |
| **W2_EWP_GROSS** | 55 | 51 | 51 | **72** | **12** |

Gross-matching does exactly what 742/672/787 said it would — it takes the CAGR floor off the
table (41 → 12 binding) — and then **the drawdown cap alone convicts all 72 books.** The
arithmetic is the point: de-grossing cuts the book's drawdown *and* the gross-matched
comparand's drawdown roughly together, so the 0.60 multiplier, written for a fully-invested
SPY, has to be earned by gate quality instead of by cash. The live book is the clean case:
**BAND-DG g0.75 clears H1, H2, OOS and CAGR against its own gross-matched basket and fails on
DD alone** (−11.90% against a cap of ≈ −9.3%).

**Appendix — the implied re-calibration (diagnostic, not a proposal).** Against W2, **14 of
72 books clear all three Sharpe legs**; the cheapest one to admit is `U56/MA-RS/g0.5/M`, and
it needs **λ_DD ≥ 0.816** where PROTOCOL says **0.60** (its CAGR leg would then be satisfied
at any λ_CAGR ≤ 0.948, so 0.70 is not the blocker). Across those 14, λ_DD needed runs
**0.816–1.013**. Against W1 the cheapest is λ_DD ≥ 0.275 but that book's CAGR leg then needs
λ_CAGR ≤ 0.324, well below PROTOCOL's 0.70. **Neither equal-weight wording is adoptable
without moving at least one of the two constants**, and the run makes no proposal about what
they should become.

## Rule 8 WF-B — each wording used as a SELECTOR, OOS read once

Among the books whose five 4b legs all clear the wording's comparand on **2009–2016 data
only**, hold the best-IS-Sharpe one through 2017–2026; if the wording admits nothing, stand
down to the live book.

| wording | admitted (ALL) | picked | OOS CAGR | OOS Sharpe | OOS MaxDD |
|---|---|---|---|---|---|
| **W0_SPY** | 12 | U56/MA-RS/g0.75/M | **13.60%** | 1.1930 | −18.21% |
| W1 / W2 / W3 / W4 | **0** | STAND-DOWN (RULES v2 U56) | 9.48% | 1.2834 | −11.90% |
| **RULES v2 U56 (live)** | — | — | **9.48%** | **1.2834** | **−11.90%** |
| **SPY** | — | — | **15.24%** | **0.8721** | **−33.72%** |

**Beating the live book OOS Sharpe: 0 of 20. Beating SPY OOS Sharpe: 20 of 20.** The
equal-weight wordings' apparent OOS "win" (mean Sharpe 1.2834 vs W0's 1.1930) is **entirely
stand-down**: they admit nothing in-sample, so they select nothing, so they score the live
book. That is not evidence a bar is better — it is the fifth independent reproduction of idea
776's stand-down reading. The incumbent wording, which does select, buys **+4.1 pp of OOS
CAGR for −0.09 of OOS Sharpe and 6.3 pp more drawdown**.

## Sizing census (not re-adjudicated)

Of **784** committed markdown files, **768 mention 4b**, with **13,256 4b sites** of which
**3,153 assert a pass or a KEEP**. The exposure of any rule-4b rewording is the whole record;
the *rebuildable* adjudication is this run's 72-book grid, where the three equal-weight
wordings move 9 verdicts each and W3 moves 12.

## KEEP paths

Book grid (72): **4a 1, 4b 9, BOTH 0** (4a comparand = each panel's own BAND-DG g0.75 W, the
live book's form). The nine 4b passes under the rule as written: `U56/BAND-DG/g1.0/{W,M}`,
`U56/MA-RS/g0.75/{W,M}`, `U56/CAND20/g0.75/{W,M}`, `B136/BAND-DG/g1.0/W`,
`B136/MA-RS/g0.75/W`, `B136/CAND20/g0.75/M` — the MA-RS / band shelf the record already
holds. WF-B selection books (20): **4a 0, 4b 4**. **No candidate, no memo, no rule change.**

## PROTOCOL proposal (Sunday, not adopted — this run changed nothing)

**Do not swap the comparand.** Instead, make the artefact visible: *rule 4b keeps SPY as the
binding comparand, and every published 4b verdict must also quote the same five legs against
an equal-weight basket of the book's own investable panel, at the book's own gross, as a
NON-BINDING column.* That costs one extra backtest per claim, keeps rule 4b feasible (the
incumbent passes 12.5% of this grid), and makes a pass that exists only because SPY is the
comparand impossible to quote without the reader seeing it. A binding swap should not be
considered until someone proposes and walks forward a re-calibration of the 0.60 and 0.70
multipliers, which this run shows are not separable from the wording.

## Survivorship

`universe_broad.json` and the small panel are **current constituents only**, and this matters
*more* here than usually: every equal-weight comparand (W1, W2, W3) is a basket of exactly
those surviving names, so the bar it sets is inflated by the full survivorship premium, while
SPY is a real index with its own delisting history already inside it. **The equal-weight
wordings are therefore measured here at their harshest**, so the 0-of-72 conviction is stated
against the construction that flatters them; a delisting-complete panel would lower those
bars and could make W1/W2 feasible. Names with `max_1d_move >= 1.0` are dropped from the
small panel per PROTOCOL (483 → 439). Panels start on different dates (U56/B136 2008, SMALL
2010).

## Artefacts

`.wordings.csv` (the 20 tuned points) `.verdicts.csv` (per book × wording, with failing legs)
`.recalibration.csv` `.bars.csv` `.books.csv` `.walkforward.csv` `.census.csv`
`.keeppaths.csv` `.console.txt`
