# Idea 787 — does ANY standing 4b candidate clear an EQUAL-WEIGHT bar?

**lane B, 2026-09-11.** Script `2026-09-11_does-ANY-standing-4b-candidate-clear-an-EQUAL-WEIGHT-bar_B.py`.
Two tuned parameters, **every grid point reported**: dial (6–7 rungs) × panel (2). The FAMILY axis is a
structural enumeration of the record's committed memos, not a tuned dimension. 10 bps, next-day
execution, no shorting, gross ≤ 1.00, 260-row warm-up skip, SPY-free frame, rule 8 throughout.

## ANSWER — NO. **0 of 82.** The record's entire standing 4b shelf is a comparand artefact, not one book.

Idea 742 showed the standing candidate (RULES v2 band at gross 1.00) fails 4b against an equal-weight
basket of its own panel, and that the binding leg is the **CAGR floor**. That was the weakest possible
test of the shelf: a de-grossing book whose Sharpe is flat in gross and whose CAGR is pure cash weight.
This run re-prices the **whole shelf as six families** — including the RETURN books (QUANT-RESP runs
15.5–19.6% CAGR) whose whole case is the leg the band book failed.

| bar | 4a | 4b pass | of 82 cells |
|---|---|---|---|
| RULES v2 live (4a comparand) | — | **0** | 0.0% |
| **B_SPY** (the PROTOCOL 4b comparand) | — | **26** | 31.7% |
| **B_EW742** (idea 742's bar: equal-weight panel, daily, 0 bps) | — | **0** | 0.0% |
| **B_EWW10** (same basket, weekly, 10 bps — the *weaker* bar) | — | **0** | 0.0% |

Under rule 8 (dial picked on IS ≤ 2016 alone, 2017–2026 read once): **4 of 12** family×panel picks pass
4b-vs-SPY; **0 of 12** pass against either equal-weight bar.

## Gates (pre-registered, all PASS)

| gate | value | bar |
|---|---|---|
| G1 `fast_backtest` vs `engine.backtest`, returns AND turnover, 3 books × 2 panels | max **2.08e-17** | 1e-12 |
| G2 `b_band_dg(0.75)` == `baseline.rules_v2_weights` (full frame) | **0.000e+00** | exact |
| G3 U56 SPY b&h == idea 742 (15.11% / 0.8835 / −33.72%) | 2.743e-05 | 5e-4 |
| G4 U56 `B_EW742` == idea 742's own bar (17.94% / 1.1357 / −28.87% / 1.2129 / 1.0743 / OOS 18.64% / 1.1448) | **4.536e-05** | 5e-4 |
| G4b `Sharpe(B_EW742) > Sharpe(B_EWW10)` — the cost-matched bar is the weaker one | +0.01199 | > 0 |
| G5 U56 BAND-DG g1.00 == standing memo line 3 (11.55% / 1.2067 / −15.70% / 1.2405 / 1.1798) | 4.954e-05 | 5e-4 |
| G6 cost-rung identity `r(25) = r(0) − turnover·25/1e4`, both panels | **0.000e+00** | 1e-12 |

**G4 failed on the first pass and the specification was corrected, not the bar.** Idea 742's `B_EW` is
**daily-rebalanced at 0 bps**; the first version of this run scored a weekly/10 bps basket and read
1.446e-02 against the memo's digits. Both bars are now run and both are reported. `B_EWW10` is the
weaker of the two on both panels (G4b), so the 0-of-82 KILL is stated against the *easier* bar.

## The three bars and the live book

| panel | series | CAGR | Sharpe | MaxDD | H1 | H2 | OOS CAGR | OOS Sharpe |
|---|---|---|---|---|---|---|---|---|
| U56 | B_SPY | 15.11% | 0.8835 | −33.72% | 0.9595 | 0.8211 | 15.24% | 0.8721 |
| U56 | **B_EW742** | 17.94% | 1.1357 | −28.87% | 1.2129 | 1.0743 | 18.64% | 1.1448 |
| U56 | **B_EWW10** | 17.69% | 1.1237 | −29.09% | 1.2036 | 1.0598 | 18.35% | 1.1308 |
| U56 | RULES v2 live (g 0.75) | 8.63% | 1.2069 | −11.90% | 1.2400 | 1.1806 | 9.48% | 1.2834 |
| B136 | B_SPY | 15.23% | 0.8890 | −33.72% | 0.9566 | 0.8340 | 15.45% | 0.8820 |
| B136 | **B_EW742** | 19.22% | 1.1361 | −32.52% | 1.2469 | 1.0373 | 18.90% | 1.1148 |
| B136 | **B_EWW10** | 18.95% | 1.1238 | −32.71% | 1.2354 | 1.0240 | 18.62% | 1.1022 |
| B136 | RULES v2 live (g 0.75) | 8.03% | 1.1078 | −12.18% | 1.2312 | 0.9861 | 7.98% | 1.1206 |

Swapping SPY for the panel's own equal-weight basket moves the 4b bars by **+0.24 Sharpe, +2.8 pp of
CAGR floor and −4.6 pp of drawdown budget on U56** (+0.23 / +3.7 pp / −1.0 pp on B136). That swap, and
nothing about the books, is what turns 26 passes into 0.

## The finding underneath the KILL: the shelf HAS risk-adjusted edge; it cannot spend it

The shelf does not lose the Sharpe contest on U56. **21 of 41 U56 cells beat `B_EWW10` on all three
Sharpe legs at once** (H1, H2 and OOS) — the gates and rules are doing real work against naive equal
weight. What no cell does, on either panel, is clear the **CAGR floor and the DD cap together**:

* **The tight-drawdown books miss the return floor.** BAND-DG at every gross clears H1/H2/OOS/DD and
  misses CAGR: at the live g 0.75 by **−3.75 pp/yr**, at the standing candidate's g 1.00 by **−0.83 pp**
  (−1.00 pp against `B_EW742`; OOS **−0.14 pp** / −0.35 pp).
* **The high-return books blow the drawdown cap.** QUANT-RESP q0.20 clears the U56 CAGR floor by
  **+7.25 pp/yr** and breaches the DD cap by **−4.42 pp**; on B136 it is the only cell clearing all
  three Sharpe legs and it misses DD by −2.73 pp.
* Max legs cleared against `B_EWW10`: **4 of 5**, reached by 20 U56 cells and 1 B136 cell. Never 5.

## Appendix — the one dial that could close the U56 gap is the one PROTOCOL 2 forbids

On a de-grossing book at a zero cash rate, gross is a pure scale on both level legs, so the committed
BAND-DG ladder pins the answer without any new tuning (linear fit through the 7 rungs, r² 0.99999 CAGR
/ 0.99996 MaxDD):

| panel | gross needed to clear the EW CAGR floor | gross that breaches the EW DD cap | window | feasible at gross ≤ 1.00? |
|---|---|---|---|---|
| U56 | **1.0716** | 1.1122 | non-empty, [1.072, 1.112] | **NO — the whole window is leverage** |
| B136 | 1.2356 | 1.2239 | **EMPTY** | NO — no gross clears both legs at all |

So on U56 the standing candidate's 4b pass is not merely a comparand fact: it is **0.072 of gross away
from being true against the honest bar, and every point of that gap is on the far side of PROTOCOL rule
2's no-leverage constraint.** On B136 no amount of gross, leveraged or not, closes it.

## Verdict — **KILL for capital, across the whole standing shelf.** No KEEP, no memo, no book promoted.

RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are untouched (rule 6).

## Caveats

1. **SURVIVORSHIP cuts toward the bar, not the books.** U56 and the broad panel are current
   constituents. The equal-weight bar is the maximally survivorship-exposed object in this run — it
   holds every survivor at full weight — so its CAGR floor is inflated by an unmeasured amount and the
   CAGR-floor misses above are upper bounds on the real gap. The **Sharpe and DD legs**, where the
   shelf's failures on B136 and the high-return cells sit, are far less exposed. A delisting-complete
   panel would move the U56 CAGR verdict and is the one test that could revive this shelf.
2. **The equal-weight bar is investable but not free.** `B_EWW10` is charged the books' own 10 bps and
   rebalances weekly; `B_EW742` is the 0-bps daily bar. The two differ by 0.012 of Sharpe, so the
   "equal weight at zero cost flatters the bar" objection is quantitatively dead here, as idea 742 found.
3. **Two panels, not three.** SMALL439 is not run; idea 742 reports the shelf's candidate failing there
   on H1/H2/OOS/CAGR against B_SPY already, so adding it cannot produce a passer.
4. **One window.** Both 4b level bars are comparand-relative and move with the sample; idea 522 showed
   staleness alone flips the full-sample 4b verdict on 4 of 201 U56 month-ends at today's lag.
