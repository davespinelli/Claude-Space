# Idea 60 — band-gate-on-small-panel (lane B, 2026-09-06)

**ANSWERED, and idea 52's whipsaw hypothesis is a KILL. The band does NOT recover a large part
of the 5.4 pp: it recovers 7.0% of it. The shape of the recovery curve says why — it never
saturates. Widening the band keeps buying CAGR back monotonically to b = 20%, and it is still
rising there, having recovered 100.8% of the trend half's damage. Whipsaw damage would be bought
out by a band and then stop; this does not stop, which is the NO-SIGNAL shape. The same
non-saturation is on the large caps too (U56 band20 recovers 284% of its trend-half gap), so the
sub-$2B inversion is not a different mechanism — it is the same drag at 2.9× the magnitude
landing on a panel with no return to absorb it. Rules unchanged; no new book; no KEEP-candidate;
no memo. `RULES.md`, `scan.py`, `bot.py` and `baseline.py` untouched.**

Script: `2026-09-06_band-gate-on-small-panel_B.py`. **432 grid points** — 2 panels × floors
{$0, $1M} × 2 conventions {rw, dg} × 2 compositions {TREND, FULL} × 9 arms × 4 cost rungs
{0, 5, 10, 25} bps — **every one printed** and written to `.grid.csv`, plus 48 decomposition
rows, 48 × 3 recovery-curve readings, 48 walk-forward cells and 108 verdict rows. Exactly two
tuned parameters (instrument family BAND/STALE × its dial); panel, floor, convention,
composition and cost rung are reported at every value with **no selection over them**. Weekly,
next-day execution, gross 0.75, long only.

## 0. Reproduction gates (all five bind; nothing below was read until they passed)
| gate | this run | published | |
|---|---|---|---|
| [a] `fast_bt` vs `engine.backtest` | max abs diff **8.674e-18** | — | pass |
| [b] SPY, SMALL439 window 2011-01-13..2026-09-04 | 14.13%/0.862/−33.7%, halves 0.891/0.858 | idea 121 identical | pass |
| [c] LIVE RULES v1 on SMALL439 @10bps | **8.15%/0.603/−32.8%** | idea 121 8.15%/0.603/−32.8% | pass |
| [d] LIVE RULES v2 on U56 @10bps | **8.66%/1.2056/−12.05%**, halves 1.2259/1.1908 | idea 61 identical | pass |
| [e] idea 61's SMALL439 × ew-all × BAND × TREND × floor-$0 rows, 28 cells | max abs Sharpe diff **5.551e-17** | idea 61 `.grid.csv` | pass |

Gate [c] costs one convention to state: v1's cross-sectional ranks must be computed on the 439
**selectable** names only. SPY is a benchmark column joined by `load_universe(small=True)`, not a
constituent, and ranking it in moves the book to 7.41%/0.565/−36.1% — 0.74 pp of CAGR. Any
small-panel run that passes the SPY-bearing frame to a **ranking** book is reading a different
book from the record's. (Equal-weight books are unaffected: `weights_ewall` never selects a
non-tradable column, which is why gate [e] is exact.)

Flip rates are convention-sensitive in the same way. Idea 4/57/61 measure them over the whole
index and every column; this run's headline table measures them over the **evaluation** window
and tradable columns only. Under idea 61's convention U56 re-derives at **7.443 / 1.746**
(published 7.44 / 1.75; idea 4/57 7.55 / 1.77). Both panels are measured identically throughout,
so the small-vs-large ratio is convention-free.

## 1. P1 — the published damage reproduces at both anchors
SMALL439, floor $0, g = 0.75, gross-matched (`rw`), full eligibility gate, EWgate minus EWall:

| rung | dCAGR pp | dSharpe | dMaxDD pp | names all / gated |
|---|---|---|---|---|
| **10 bps** | **−6.5155** | **−0.3420** | **−3.8143** | 347.91 / 141.23 |
| idea 121 published | −6.5155 | −0.3420 | −3.8143 | 347.91 / 141.26 |
| **0 bps** (idea 49's headline) | **−5.3121** | −0.2527 | −2.6288 | 347.91 / 141.23 |
| idea 49 published | ≈ −5.4 | — | — | — |

**P1 HOLDS**, to four decimals against idea 121 and to 0.09 pp against idea 49.

## 2. The four-way decomposition — the trend half is the SMALLER destroyer
CAGR by half of the filter, SMALL439, floor $0, `rw`, **0 bps** (the queue's rung):

| EWall | 200d only | vol20 only | both | published gap |
|---|---|---|---|---|
| 10.37% | 7.59% | 6.11% | 5.06% | **−5.31 pp** |

The trend half alone costs **2.79 pp**; the vol20 < 0.60 half alone costs **4.26 pp**. The gate's
damage is majority *volatility filter*, and a band is an instrument on the trend half only — so
even a perfect trend instrument leaves most of the 5.4 pp on the table by construction. This is
idea 38/56's ordering (no-gate > 200d > vol20 > both), recovered on the equal-weight book and
now with the arithmetic attached.

## 3. P2 — the band recovers 7.0%, not "a large part"
Three readings of "the damage", all printed for all 48 cells (`.curve.csv`); P2 is judged on the
**largest** of them, which can only help the hypothesis:

| reading | the gap | band3 recovers |
|---|---|---|
| **PUB** — the published EWall-vs-full-gate gap | 5.31 pp | **7.0%** |
| TRND(FULL) — trend half's own gap inside the full gate | 1.05 pp | 35.5% |
| TRND(TREND) — trend half's gap with no vol filter at all | 2.79 pp | 20.1% |

**P2 FAILS** on every reading (best 35.5% against a 50% bar). Idea 52's prediction — that the
band should recover a large part of the 5.4 pp — is refuted at zero cost, and costs do not
rescue it: band3's PUB recovery rises only 7.0% → 8.7% → 10.0% → 12.8% across 0/5/10/25 bps (the
band's 10.6× turnover against the gate's 13.4× is worth something, just not much), so even at
25 bps the band repairs an eighth of the damage.

## 4. P4 — the discriminator, and it is the whole answer
Whipsaw damage is caused by crossings that are noise, so a band wide enough to swallow the noise
should remove most of the damage **and then stop helping**. It does not stop:

| reading | 0.00 → 0.03 | 0.03 → 0.20 | ratio | total at b = 0.20 |
|---|---|---|---|---|
| PUB | 7.0% | **32.3%** | **4.60** | 39.4% |
| TRND(FULL) | 35.5% | **163.4%** | **4.60** | **198.9%** |
| TRND(TREND) | 20.1% | **80.7%** | **4.02** | **100.8%** |

Recovery is still **rising at the widest band on all three readings**. At b = 0.20 the arm still
gates out nearly half the panel — 185.8 of 347.9 priced names held, 0.76 flips/tkr/yr — and yet
delivers **10.40% against the un-gated book's 10.37%**: it has recovered **100.8%** of the trend
half's damage without becoming the un-gated book. **P4 FAILS**: the curve has the NO-SIGNAL
shape. The gate does not lose money on the noisy crossings; it loses money on *every* crossing,
and the only band that stops the loss is the one wide enough to stop acting on the signal.

The same shape is on the large caps: U56 at 0 bps has a trend-half gap of 0.96 pp, band3 recovers
34.6% of it and **band20 recovers 284%**. So non-saturation is not a small-panel pathology — the
200d gate's damage is never noise-crossing damage. What is special about the sub-$2B panel is the
*size* of the drag (2.79 pp vs 0.96 pp at 0 bps, 2.9×) landing on a panel with no offsetting
return to absorb it. The inversion is the same mechanism at a magnitude the returns cannot carry,
not a different one.

## 5. P3 — whipsaw is present, and it is not the differentiator
| arm | SMALL439 | U56 | ratio |
|---|---|---|---|
| 200d | **8.91** | 7.81 | 1.14× |
| band3 | 3.27 | 1.83 | 1.79× |
| band20 | 0.76 | 0.27 | 2.79× |

**P3 HOLDS but does not carry the hypothesis.** The small panel flips only **1.14×** more than
the large caps on the bare gate. That is nowhere near enough to explain a sign reversal, and the
band's effect on the flip count is if anything *stronger* where it helps least: band3 cuts flips
**4.3×** on U56 (7.81 → 1.83) and only **2.7×** on SMALL439 (8.91 → 3.27), while recovering
34.6% of the trend-half gap on U56 against 20.1% on SMALL439. A 1.14× difference in flip rate
cannot produce a 2.9× difference in damage, and the instrument that removes flips fastest is not
the one that recovers the most. Flip count is not the variable the inversion lives on.

## 6. Rule 8 walk-forward (dial chosen on 2010..2016 only, 2017..2026 read once)
| panel | IS-Sharpe pick | band3 (pre-registered constant) | 200d (incumbent) | NOGATE (do nothing) | SPY |
|---|---|---|---|---|---|
| SMALL439 (32 cells) OOS Sharpe | 0.399 | 0.281 | 0.264 | 0.366 | **0.882** |
| SMALL439 OOS CAGR | 4.12% | 2.58% | 2.36% | 4.93% | **15.45%** |
| SMALL439 OOS MaxDD | −26.8% | −28.3% | −28.1% | −34.0% | −33.7% |
| U56 (16 cells) OOS Sharpe | 1.191 | **1.249** | 1.185 | 1.159 | 0.882 |
| U56 OOS CAGR | 11.27% | 11.07% | 10.29% | **13.17%** | 15.45% |

On SMALL439 the IS chooser beats do-nothing on Sharpe in 24/32 cells but **loses to it on CAGR**
(4.12% vs 4.93%) and beats SPY in **0/32** — the panel has no arm worth choosing between. On U56
the pre-registered constant b = 0.03 beats the IS chooser in **12/16 cells** (1.249 vs 1.191):
the record's 14th instance of an in-sample selector losing to a constant it could have inherited.

## 7. Both KEEP paths at PROTOCOL's 10 bps
4b bars on the SMALL439 window: H1 > 0.891, H2 > 0.858, OOS Sharpe > 0.882, MaxDD ≥ −20.2%,
CAGR ≥ 9.89%. 4a bars (live RULES v2 on its own universe, aligned): H1 > 1.056, H2 > 1.272.

**4a 0/108. 4b 15/108, every one of them on U56, 0 on SMALL439** (binding bars over the 93
failures: CAGR 86, H1 72, H2 72, OOS 72, DD 50). **P5 HOLDS**, consistent with idea 121's 0/192
and idea 61's 0 small-panel 4b passes. Nothing here is promotable.

The 15 U56 passes reproduce idea 61's territory rather than extending it — `EWall + band12-rw`
reads **14.02%/1.2264/−19.4%, halves 1.2611/1.2048**, matching its PARK to 3 dp — with one
by-product worth recording: **adding the vol20 < 0.60 half subtracts Sharpe from 8 of 9 gated
arms on U56** (mean −0.041; band12 1.2264 → 1.1773, band3 1.1609 → 1.1348) and is neutral only
when there is no trend gate at all (+0.001). The volatility filter is a net negative on large
caps too, not only on the sub-$2B panel.

## 8. What this closes and what it opens
Idea 52 is answered and closed: **whipsaw is not the mechanism**. Anyone reaching for a
hysteresis band, a stale gate or a slower re-evaluation to rescue trend-following on this panel
is treating a symptom the data says is not the disease — and idea 61's flip-rate floor already
says the same thing from the other direction (below ~0.5 flips/tkr/yr the gate is strictly
worse, so there is no "slow enough" arm to escape to either).

Two caveats on the level, neither of which touches the contrasts. **Survivorship:** the panel is
current constituents, and its missing cohort is concentrated in exactly the thin, noisy names the
gate arms disagree about — every number here is an arm-minus-arm difference on the same names and
the same days for that reason. **Capacity:** at idea 121's proposed $1M ADV floor the published
damage shrinks from −6.52 pp to −4.87 pp at 10 bps but never changes sign, and band3's recovery
does not improve; the floor rows are in `.grid.csv` and `.curve.csv` at every cost rung.

## Queued follow-ups
- **282** is-the-vol20-half-the-whole-small-panel-inversion — this run attributes 4.26 of the
  5.31 pp to `vol20 < 0.60` and only 2.79 pp to the trend half. Sweep the vol ceiling
  {0.30, 0.45, 0.60, 0.90, ∞} × {gate on, gate off} on SMALL439 and U56 and report whether the
  inversion is a *volatility* filter result that the record has been attributing to trend.
- **283** does-the-no-signal-shape-appear-on-any-panel-that-passes — the saturation test in §4 is
  a two-number diagnostic computable from any published band ladder. Back-fill it over idea 61's
  408 cells and idea 57's 40, and report whether the arms that clear 4b are exactly the ones
  whose recovery curve *does* saturate.
