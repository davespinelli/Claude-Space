# Idea 988 — does ANY GROSS RUNG clear 4a AND 4b at once on the FAST CADENCES?
*(2026-09-22, lane cloud, run 17.  Script: `research/backtests/2026-09-22_any-gross-rung-clears-4a-and-4b-on-fast-cadences_cloud.py`)*

## ANSWER = NO, AT 0 OF 234 — AND THE TWO PATHS ASK THE GROSS DIAL FOR OPPOSITE THINGS

234 books published: the live `BAND03` shape (`rules_v2_weights`, band 0.03, the LIVE
constant, untuned) over **gross g = 0.25..1.50 in 0.05 steps x cadence {D, W, M} x panels
{U56, B136, SMALL}**, 10 bps, next-day execution.  Exactly two tuned parameters, the ones
the queue line names: the gross ladder and the cadence.  M is published as a control so the
verdict cannot be a fast-cadence artefact.  24 of 24 gates pass, including
**G3: W at g = 0.75 reproduces the live RULES v2 book to 0.00e+00 of Sharpe.**

| | count |
|---|---|
| clear 4a | **8 of 234** (all SMALL / M, g = 0.25..0.60) |
| clear 4b | **35 of 234** |
| clear 4b FULL and OOS | 26 of 234 |
| **clear BOTH AT ONCE** | **0 of 234** |
| unlevered subset (g <= 1.00, all PROTOCOL rule 2 permits) | 4a 8 / 4b 8 / **BOTH 0** of 144 |
| rule-8 picks clearing both | **0 of 33** |

## The mechanism, in three measured statements

**1. The two KEEP windows on the gross dial are DISJOINT on every cell where both exist.**
4a's drawdown leg (MaxDD no worse than the live book) caps gross; 4b's CAGR floor (>= 70%
of SPY) floors it.  They never meet:

| panel x cadence | 4a's DD leg allows | 4b's CAGR floor needs | gap (of gross) |
|---|---|---|---|
| U56 D | g <= 0.80 | g >= 0.95 | **0.15** |
| U56 W | g <= 0.75 | g >= 0.95 | 0.20 |
| U56 M | g <= 0.60 | g >= 0.90 | 0.30 |
| B136 D | g <= 0.80 | g >= 1.05 | 0.25 |
| B136 W | g <= 0.75 | g >= 1.00 | 0.25 |
| B136 M | g <= 0.55 | g >= 1.00 | **0.45** |
| SMALL D / W / M | g <= 0.80 / 0.75 / 0.60 | **unreachable at any rung** | — |

**Overlap: 0 of 9 cells.**  The fast cadences NARROW the gap (D is the narrowest everywhere,
0.15 on U56) but never close it — which is exactly why idea 984's four OOS passes were all
D/W and all still refused on 4a.

**2. Gross is a DRAWDOWN dial, not a SHARPE dial, and 4a needs Sharpe.**  Over the entire
0.25..1.50 ladder the book's Sharpe moves by **0.0007 to 0.0097**, while MaxDD moves by
**0.176 to 0.261** and CAGR by 0.064 to 0.151.  MaxDD travels **39x as far as first-half
Sharpe** over the same ladder.  Consequence: on **8 of 9 panel x cadence cells NO rung
anywhere on the ladder passes both of 4a's Sharpe legs** — not the levered ones either.  The
one exception is SMALL / M, where all 26 rungs pass them (the live book is weak on SMALL:
Sharpe 0.6596, halves 0.8057 / 0.5480), and there 4b's CAGR floor of 9.82% is unreachable at
every rung.  The refusal is therefore structural on both panels where the live book is
strong, and inverted on the panel where it is weak.

**3. The binding-leg census says the same thing from the other side.**  Over all 234 books:
`4b_CAGR_floor` fails 70.5% of the time and is the SOLE 4b binder 87 times; `4a_H1_gt_v2`
fails 69.7% and is the SOLE 4a binder 54 times; `4a_DD_no_worse` fails 60.7% (sole 18).  The
CAGR floor and the drawdown cap are the record's two standing binders and they pull the same
dial in opposite directions.

## The 984 rung, re-priced
U56 / D / g = 1.00: 11.20% / 1.1900 / **-14.77%**, halves 1.1940 / 1.1886, OOS 12.45% /
1.2874 / -14.77%, turnover 3.26x/yr (0.33 pp/yr of cost at 10 bps).
U56 / W / g = 1.00: 11.53% / 1.2009 / **-15.91%**, halves 1.2282 / 1.1799, OOS 12.67% /
1.2760 / -15.91%, turnover 2.35x/yr.
Both clear 4b (full and OOS).  Both fail 4a, and now with the number attached: the shallowest
rung that still clears 4b on U56/D is g = 0.95 at **-14.07%**, still **2.01 pp deeper** than
the live book's -12.05%.  That 2.01 pp is the whole of 984's refusal, and no rung on the
ladder pays it off.

## RULE 8 (g and cadence chosen on 2009-2016 ONLY, 2017-2026 read ONCE)
Three published IS-only rulers x three pools x three panels = 33 picks, **0 clearing both
paths**.  IS Sharpe and IS Calmar both run to the **levered grid edge g = 1.50** on 6 of 6
unrestricted families (the record's standing "the chooser is declining to act" flag); the
DD-budget ruler — the one dial idea 2266 found the budget does not break on — picks the
**shipped g = 0.75** on 4 of 6, i.e. reproduces the live book and buys nothing.  Excluding
leverage, IS Sharpe picks **W g = 1.00** on all three panels: on U56 that is 984's book
(OOS 12.67% / 1.2760 / -15.91%, 4b yes, 4a no), on SMALL it clears neither.

## Verdict: **KILL**
No gross rung clears both KEEP paths at any cadence on any panel, levered or not, and the
reason is not a near miss but a **disjoint window with a 0.15-0.45 gap in gross**.  The
queue's question is answered and closed.  Corollary worth carrying: **4a and 4b cannot both
be reached by moving gross alone** — a book that clears both has to come from a shape change
that raises Sharpe, since gross moves drawdown 39x harder than it moves Sharpe.
