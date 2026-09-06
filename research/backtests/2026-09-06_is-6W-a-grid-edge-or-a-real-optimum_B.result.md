# Idea 187 — is-6W-a-grid-edge-or-a-real-optimum (lane B, 2026-09-06)

**VERDICT: KILL — for the question as posed, and for cadence as a RULES parameter.
No KEEP claimed on either path. The idea's own dichotomy is false: 6W is neither a grid edge
nor a real optimum, because CADENCE LENGTH IS NOT THE VARIABLE. Block PHASE is.**

Script: `2026-09-06_is-6W-a-grid-edge-or-a-real-optimum_B.py`
Corpus: idea 175's 115 books verbatim (SMALL439/U56/ETF36 + 112 seeded sub-panels), same book
(top-20 EW on the scan.py composite, g=0.75, bare 200d+vol20 gate), 10 bps, t+1,
IS ≤ 2016-12-31, OOS ≥ 2017-01-01. 13 ladder points × 115 books = 1495 runs.

## Reproduction, asserted before any new number was read

* **[a]** `cad_mask` == `engine.rebalance_mask` at D/W/M/Q; rebalances/yr monotone over all 13
  points (252.0 → 126.0 → 52.3 → 26.2 → 12.1 → 8.7 → 7.5 → 6.5 → 6.1 → 5.3 → 4.0 → 3.3 → 2.0).
* **[b]** `fast_backtest` == `engine.backtest` to 1.4e-16 on returns, 1.1e-15 on turnover.
* **[c] the decisive one** — on the 7 points idea 175 ran, all **805 shared rows match its
  committed `.ladder.csv` to 7.105e-15**, with **0 verdict-string mismatches and 0 worst-bar
  mismatches**. The six new points are therefore comparable to the old ones bar for bar, and
  every number below sits on idea 175's exact corpus rather than a look-alike.

## 1. The argmax moves — and the ladder is not a curve

Pooled mean OOS Sharpe over the 13 points (`*` = new):

| D | 2D | W | 2W | M | 6W | 7W* | 8W* | 2M* | 10W* | Q | 16W* | 2Q* |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|0.621|0.662|0.680|0.689|0.756|**0.780**|0.606|0.651|**0.826**|0.693|0.539|0.630|0.646|

The pooled argmax moves 6W → **2M** (P2 HIT) and is interior on the extended ladder in all four
family rows (P3 HIT), so plain truncation is refuted: **0 of 7 slower-than-6W points beat 6W**
on ALL, U56 and ETF at sign p<0.05. But the curve between them is **jagged, not humped**:
7W (0.606) is worse than every point from W onward, 2M (6.1 reb/yr) beats 8W (6.5 reb/yr) by
+0.175, and **Q (4.0/yr) is the worst point on the whole ladder while 2Q — half Q's frequency —
beats it.** On U56 the 6W-minus-7W gap is **−0.3108 (t −29.65)**, 1.9× the entire 6W-minus-W gap
idea 175 published (+0.1640). No signal-decay mechanism produces that. P5 MISSed in the
informative direction: the spread inside the {6W,7W,8W,2M,10W} zone is **9.23× the 6W-minus-M
gap**, i.e. these points are wildly different from each other, not a plateau.

## 2. The post-hoc phase control (labelled as post-hoc; added after the table above was read)

Holding cadence fixed and sweeping the block phase — which weeks the book lands on, fixed by an
arbitrary sample-start date and not a tradable choice:

| family | phase spread 6W (6 phases) | phase spread 2M | phase spread 8W | ZONE cadence spread | 6W−W (idea 175) |
|---|---|---|---|---|---|
| ALL | 0.1518 (t 5.41) | 0.2130 (t 19.29) | 0.1499 | 0.2198 | +0.0999 |
| SMALL | 0.2618 (t 11.32) | 0.2344 | 0.1604 | 0.2259 | +0.0163 |
| U56 | **0.3957 (t 34.12)** | 0.2161 | 0.2309 | 0.3108 | +0.1640 |
| ETF | **0.3862 (t 34.89)** | 0.1780 | 0.2998 | 0.2859 | +0.1600 |

**Q is the negative control and returns exactly 0.0000 spread on all four families**: Q is a
k=1 calendar-period point with exactly one phase by construction, so zero is the right answer
and the non-zero spreads elsewhere are phase, not sweep noise.

**The phase spread at one fixed cadence is 2.1–2.4× the published 6W-minus-W cadence effect
(16.1× on SMALL), and on U56/ETF it exceeds the spread across the entire slow zone.** The
ladder's 6W is **phase 0 of 6, and phase 0 ranks 1/6 on ALL, U56 and ETF** — the luckiest of six
arbitrary alignments. Stated as a count: **6W beats the weekly incumbent at only 2 of its own 6
phases** on ALL/U56/ETF, and the pooled argmax 2M beats it at **1 of 2**. Idea 175's headline is
an alignment draw.

## 3. Cadence selection is dead on a dense grid (PROTOCOL rule 8)

Paired vs the incumbent constant W, OOS Sharpe, 115 books:

| arm | ALL | SMALL | U56 | ETF |
|---|---|---|---|---|
| SEL-SHARPE | **−0.0124 (t −0.68)** | +0.1014 (t +3.40) | **−0.1377 (t −6.57)** | −0.0561 (t −2.30) |
| SEL-4B | −0.0198 (t −1.07) | +0.0969 (t +3.22) | −0.1346 (t −6.21) | −0.0784 (t −3.18) |
| RANDOM (control) | +0.0082 (t +0.56) | +0.0833 | −0.0243 | −0.0710 |
| ORACLE (bound) | +0.2218 | +0.2972 | +0.1684 | +0.1631 |

Idea 175's residual cadence skill (**+0.0388, t +3.26, capture 67.1% → 23.8%**) does not survive
the denser grid: pooled **capture is −5.6%**, SEL-SHARPE now sits **behind RANDOM** on ALL, and
loses outright on U56 (0.00455) and on ETF for SEL-4B. `SEL == ORACLE` agreement is **5.2%
pooled and 0.0% on U56**. The IS pick scatters (M 22.6%, 8W 22.6%, 16W 19.1%, 2Q 13.9%) — the IS
argmax chases the same phase noise the OOS argmax does, from a different draw. **Idea 107's
evidence base is gone: the one dial of five with apparent selector skill was a 4-point grid.**

## 4. Both KEEP paths, all 1495 rows

4a 272/1495, 4b 90/1495 — **every 4b pass is on U56** (SMALL 0/637, ETF 0/429), 31 of 90 on new
points, most-violated bar CAGR:1287. Fixed-panel 4b passes: U56 @ **2M** (15.35% / 1.2117 /
−20.11%, halves 1.176/1.249, OOS 18.03% / 1.3337 / −20.11%, 3.1×/yr), and U56 @ M / W / 2D —
idea 175's rows unchanged. **P8 holds: all four are the same book re-cadenced (idea 144), so
none is a new signal, and U56@2M is a 1-of-13 grid selection on the one panel where 4b ever
passes, at phase 0 of 2 — by section 2 it loses to W at its other phase. Not a KEEP-candidate.**
Rule 8: CONST-6W's OOS win (ALL 0.780 vs W 0.680) is a constant, not a selector, and section 2
prices it as alignment; the S1 pick under SEL-SHARPE (U56k20d05 @ 7W, OOS 1.186) is *worse* than
under CONST-6W (same book @ 6W, 1.473).

## 5. What this costs the record

Idea 188's three-way family split survives as a *sign* (SMALL wants slow, U56/ETF want 6W) but
**not as a constant** (P6 MISS): SMALL's argmax moves M → 2M and 5 of 7 slower-than-6W points
beat 6W there (2M +0.2199, t +10.56). Idea 175's "60.9% modal at 6W" reads 50.4% here, but that
number was never the right statistic — the ZONE share is 80.0% (P4 HIT), and the modal fall is
grid dilution. **Every cadence claim in the record that compares two week-block points is
confounded with phase and should be re-read.**

### Proposed for Sunday review — a PROTOCOL clause, NOT a RULES change

> **Clause 12 (block phase).** Any result comparing two rebalance cadences whose blocks are
> multi-unit (2W, 6W, 7W, 8W, 10W, 16W, 2M, 2Q — i.e. every point except D, W, M, Q, which have
> exactly one phase) must report the effect against the spread across that cadence's own phases.
> A cadence advantage smaller than its phase spread is an alignment draw, not an edge, and may
> not be written into RULES.

No change is proposed to RULES.md, scan.py, bot.py or baseline.py; none was touched. The
incumbent weekly cadence stays, and it stays because nothing here identifies a replacement —
not because W won.

**Caveats carried:** SMALL439/U56/ETF36 are current-constituent lists (idea 54) — the paired
comparisons are unaffected, no level here is an attainable return. Idea 38's calendar-day index
applies to U56/ETF36 after 2014-09-17. 10 bps only; idea 188 established the cadence split is
not a cost effect, so no cost ladder was re-run.
