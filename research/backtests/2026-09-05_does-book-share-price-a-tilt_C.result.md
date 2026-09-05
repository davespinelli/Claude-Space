# Idea 153 — does-book-share-of-the-panel-price-a-tilt (lane C, 2026-09-05)

**ANSWERED: YES, and it dissolves idea 81's puzzle. Book share prices a cross-sectional tilt;
the key's own t-statistic does not.** One by-product is a cross-universe 4b KEEP-candidate at
10 bps with **zero free parameters** (the standing KEEP restated as a share). Rules unchanged
this run — the by-product goes to the Sunday review, not into RULES.

Script `2026-09-05_does-book-share-price-a-tilt_C.py`; console, grid, overlap, regression,
matched, transfer and walk-forward CSVs alongside.

## Reproduction, asserted before any new number was read

| check | published | this run | |
|---|---|---|---|
| [a] u56 n=20 INV-vs-NONE name overlap (idea 81) | 69.4% | **69.4%** | MATCH |
| [a] broad n=20 INV-vs-NONE name overlap (idea 81) | 42.5% | **42.5%** | MATCH |
| [b] NONE/n=20/u56@10bps vs idea 81's committed grid row | 12.65974%/1.09214/-18.30835%, halves 1.08828/1.10155 | identical to 5 dp | IDENTICAL |
| [c] idea 80 Fama-MacBeth bivariate vol20 slope, u56 | +0.0045 (t +3.90) | **+0.00450 (t +3.90)** | MATCH |
| [c] same, broad | +0.0029 (t +3.19) | **+0.00294 (t +3.19)** | MATCH |

Small panel, never run by idea 80: slope **-0.00084 (t -0.95)** — the sign reverses and is not
significant, consistent with idea 81's finding that the winning tilt matches the panel's own
premium sign.

## The corpus

2 tuned parameters, all 21 grid points reported per (panel, cost): target book share
m ∈ {0.05, 0.10, 0.20, 0.35, 0.53, 0.75, 1.00} × tilt ∈ {INV = /√vol20 (RULES v1's live tilt),
NONE, POS = ×√vol20}. n = round(m × mean weekly eligible count): u56 Ē = 37.5, broad Ē = 91.5,
small Ē = 141.2. 3 panels × 2 cost rungs = **126 books**, plus a 63-book gross-normalised
control at 10 bps. Weekly, t+1, 10/25 bps, no shorting, no leverage.

## P2 — overlap is a function of share, not of the panel

Cross-panel spread of INV-vs-NONE name overlap **at matched n = 20: 0.425** (u56 69.4%,
broad 42.5%, small 26.9%). **At matched share: mean 0.045**, and ≤ 0.090 at every m. Overlap is
monotone increasing in m in all three panels. Matched-n comparisons across panels of different
breadth have been comparing books that express a completely different amount of ranking.

## P3/P4 — the regression the idea asked for

y = |dSharpe| or |dCAGR| of the tilt against its own no-tilt control at matched (panel, m, cost,
construction). Regressors: name overlap vs. the panel's Fama-MacBeth vol20 slope t.

| sample | y | b(overlap) | t | R² overlap | R² t_biv | joint t(t_biv) |
|---|---|---|---|---|---|---|
| all 126 rows | \|dSharpe\| | **-0.328** | **-11.50** | **0.516** | 0.010 | +2.15 |
| all 126 rows | \|dCAGR\| | -0.099 | -12.00 | **0.537** | 0.072 | +5.51 |
| literal, m ≤ 0.53 | \|dSharpe\| | **-0.428** | **-6.60** | **0.429** | 0.028 | +2.17 |
| literal, m ≤ 0.53 | \|dCAGR\| | -0.124 | -7.31 | **0.480** | 0.108 | +4.57 |
| gross-normalised, m ≤ 0.53 | \|dSharpe\| | -0.292 | -5.13 | **0.485** | 0.009 | +1.02 |

Overlap explains **15-50× more** of the tilt's realised magnitude than the key's own t does, on
the full grid and on the sub-grid that excludes the mechanically forced m → 1 endpoint, and
under both weighting constructions. Within-panel Spearman(overlap, |dSharpe|): u56 **-0.83**,
broad **-0.94**, small -0.46 (small -0.03 on m ≤ 0.53 — the panel whose premium is unsigned has
nothing for share to modulate, which is the right control).

## P5 — idea 81's puzzle dissolves

dCAGR(POS − NONE), 10 bps, literal book:

| basis | u56 | broad | ratio |
|---|---|---|---|
| matched **n = 20** (idea 81's comparison) | +0.49%/yr | +2.89%/yr | **5.9×** |
| matched **share m = 0.20** (u56 n=7, broad n=18) | **+2.83%/yr** | **+2.75%/yr** | **1.0×** |

The stronger slope on u56 (t +3.90) paying less than the weaker one on broad (t +3.19) was an
artefact of u56's n=20 book holding 53% of its eligible panel while broad's held 22%. At matched
share the two agree to 8 bps/yr. Same for INV: at m = 0.20 the tilt costs -7.12%/yr on u56 and
-4.94%/yr on broad; at n = 20 it cost -2.76% and -4.94%.

## The by-product: a zero-free-parameter 4b transfer (10 bps)

The standing KEEP (2026-09-04: top-20 equal-weight, no vol scaler, u56) holds a share of
20/37.5 = 0.533 (realised 0.509). Idea 44 killed the same **name count** on broad (4b H2 fail).
Carrying its **share** instead — no tuning, the share is read off the incumbent and multiplied by
broad's own Ē:

| panel | n | share | cost | CAGR | Sharpe | MaxDD | H1 / H2 | OOS Sharpe | 4b |
|---|---|---|---|---|---|---|---|---|---|
| broad | 20 (name count) | 0.219 | 10 | 13.1% | 0.957 | -20.1% | 1.125 / **0.811** | 0.892 | **FAIL (H2)** |
| broad | 47 (share) | 0.514 | 10 | 11.7% | 1.021 | -19.0% | 1.115 / **0.935** | 1.031 | **PASS** |
| broad | 49 (share) | 0.536 | 10 | 11.6% | 1.023 | -19.0% | 1.123 / **0.932** | 1.032 | **PASS** |
| broad | 47/49 | ~0.52 | 25 | 10.1% | 0.90 | -19.1% | 0.99 / 0.82 | 0.91 | FAIL (H2, CAGR) |
| small | 20 / 72 / 75 | any | 10, 25 | ≤ 6.7% | ≤ 0.47 | ≤ -25.6% | — | — | FAIL (all five bars) |

SPY: 15.23%/0.889/-33.72%, halves 0.957/0.834, OOS 15.45%/0.882/-33.72%. RULES v1 on broad
@10bps: 6.39%/0.635/-21.19%, OOS 5.94%/0.576/-21.19%.

## Both KEEP paths, all 126 books

**4a 38/126** (all on broad or u56 at large m, i.e. beating a live book that returns 6.4%/yr is
not the bar that matters). **4b 10/126**, every one of them at **10 bps** and on a large-cap
panel: u56 m ∈ {0.35, 0.53, 0.75} and broad m ∈ {0.35, 0.53, 0.75}, tilt NONE or POS.
**Cross-universe 4b (same (m, tilt) on both large-cap panels): m = 0.53 and m = 0.75, tilt NONE
and tilt POS — 4 points.** Zero at 25 bps (u56 fails H1, broad fails H2/CAGR — idea 137's wall).
Zero anywhere on the small panel (all five bars, at every m — idea 136 confirmed a third time).
**INV — the live rule's own tilt — passes 4b 0 of 42 times.**

## Rule 8 walk-forward (2009-2016 → 2017-2026, small panel 2011-2016)

| panel | cost | selector | pick | OOS CAGR / Sharpe / MaxDD | RULES v1 OOS | SPY OOS |
|---|---|---|---|---|---|---|
| u56 | 10 | IS Sharpe | NONE, m=0.10 (n=4) | 20.6% / 1.022 / -23.8% | 7.7% / 0.747 / -13.8% | 15.5% / 0.882 / -33.7% |
| broad | 10 | IS Sharpe | POS, m=0.05 (n=5) | 22.4% / 1.009 / -29.7% | 5.9% / 0.576 / -21.2% | same |
| broad | 10 | no-tilt control | NONE, m=1.00 (n=91) | 10.1% / **1.100** / -15.7% | | |
| small | 10 | IS Sharpe | INV, m=0.05 (n=7) | 5.0% / 0.418 / -35.0% | 7.9% / 0.581 / -32.8% | same |

Mean OOS Sharpe over the 6 (panel, cost) cells: **tilt allowed 0.753, no tilt allowed 0.781**,
RULES v1 0.451, SPY 0.882. The 4b-aware IS screen finds **nothing admissible in 4 of 6 cells**.
Two honest consequences: (i) allowing the walk-forward to choose a tilt *subtracts* 0.028 of mean
OOS Sharpe, a fourth independent KILL of the vol scaler in either direction; (ii) **an IS-Sharpe
chooser does not land on the m that passes 4b** (it picks m = 0.05-0.10, the far end of the
share axis), so the m-sweep is *not* a walk-forward-selectable rule. The transfer above survives
that objection only because its share is inherited from the incumbent, not chosen.

## Predictions

P1 HELD (all 5 reproduction checks), P2 HELD, P3 HELD, P4 HELD, P5 HELD, **P6 FAILED** — a
cross-universe 4b pass does exist, at m ∈ {0.53, 0.75} with no tilt, at 10 bps.

## Caveats carried

Survivorship on all three current-constituent panels (idea 54); the eligibility gate is inverted
on the small panel (idea 49/39) so its numbers are about a gate that does not work there; idea 38
(calendar-day index) and idea 126 (t+1 only) carry over; the m → 1.00 endpoint forces
overlap → 1 and dSharpe → 0 mechanically, so every regression is also reported on m ≤ 0.53;
the literal GROSS/n book de-grosses to 0.64-0.70 at large m (idea 73/81), which is why the whole
grid is re-run gross-normalised — the overlap result is unchanged (R² 0.485 vs 0.429). m is a
sample-average share; a time-varying n_t = round(m × E_t) is a **different, untested** rule.
