# Idea 773 — does the OOS SPAN COLLAPSE hold for the other four statistics?

**Lane C, 2026-09-11.** Script `2026-09-11_does-the-OOS-SPAN-COLLAPSE-hold-for-the-OTHER-FOUR-STATISTICS_C.py`.
Artefacts: `.grid.csv` (900 books), `.floors.csv` (60), `.spans.csv` (90), `.verdicts.csv` (40),
`.walkforward.csv`, `.keeppaths.csv` (900), `.console.txt`.

**VERDICT: ANSWERED / KILL for capital. The queue's premise is REFUTED in the general case and
REPLACED by a sharper one.** The IS→OOS span collapse idea 567 found for `PREM_SHARPE` is a
**PREMIUM** property, not a property of panel claims. Both premium statistics collapse and land
*below* their own OOS floor; all three level statistics (SHARPE, CAGR, MAXDD) do the opposite —
their OOS span/floor ratio is **larger** than their IS ratio. But the statistic a three-panel
ordering actually has to clear is not the span (the two extremes) — it is the **smallest adjacent
gap**, and that gap is inside its own floor in **88 of 90 cells** (86 of 90 at D=24). Only one of
five currencies, **SHARPE**, keeps out-of-sample content by the pre-registered definition, and what
it holds up is a **two-panel** fact (large caps ≫ small caps), not the three-panel ordering the
record quotes.

No RULES change, no new book, no PROTOCOL edit. RULES.md, PROTOCOL.md, scan.py, bot.py and
baseline.py untouched.

## Gates (5, pre-registered, printed before any new number was read — ALL PASS)

| Gate | Result | Bar |
|---|---|---|
| G0 determinism — crc32 draw scheme rebuilt twice | **0 of 72 draws differ** | 0 |
| G1 identity — `fast_backtest` vs `engine.backtest`, one book per parent | **0.000e+00** | 1e-12 |
| G2 **cross-lane reproduction** — idea 567's committed `.floors.csv`, all **60 rows × 7 cols** rebuilt from prices here | **8.882e-16** | 1e-12 |
| G3 **cross-lane reproduction** — idea 567's committed `.walkforward.csv` ORDER spans, all 6 cells | **8.327e-17** | 1e-12 |
| G4 reproduction — live RULES v2 on U56 vs the committed `0.0861 / 1.1998 / -0.1205` | **4.945e-05** | 1e-4 |

G2/G3 make this an independent same-day rebuild of lane B's numbers from source, not a re-quote.
The `.keeppaths.csv` written here is also **byte-identical to lane B's on all 900 rows** (4a, 4b and
the binding-failure leg all match, 0 mismatches).

## Design

Idea 567's panels, draws and books verbatim, so the two runs are directly comparable.
Parents U56 (55 names), B136 (135), SMALL439 (439); k=36 draws, 24 crc32 seeds per parent;
arms `EWall` (control) and `MA-RS` (gross respread over names above their 200d MA);
10 bps, next-day fills, warm-up `idx[260]`, IS ≤ 2016-12-31, OOS ≥ 2017-01-01 read once.

**Exactly two tuned parameters: STATISTIC × SPLIT (5 × 3 = 15), every point reported.**
Reported-never-selected axes: gross {0.50, 0.75, 1.00}, cadence {W, M}, draw count D {3, 6, 12, 24},
floor form {POOLED, RSS}. The headline is quoted at D=6 (567's D) and D=24 (best-resolved floor)
and the full 8-way (D × form) robustness table is committed.

*Definitions.* **span** = max − min of the statistic across the three real parents at one
(gross, cadence). **margin** = the smallest *adjacent* gap in the three-parent ordering — the bar a
3-panel ordering claim has to clear, since the span only bounds the two extremes. **floor** =
within-parent sd of the statistic across k-matched draws (567's estimator). POOLED = mean of the
three parents' floors; RSS = √(fₐ² + f_b²) of the two parents the gap is actually between
(idea 774's parent-specific bar).

*OOS content* was defined before any number was read: span/floor > 1 in ≥ 4 of 6 cells **AND** the
IS ordering survives into OOS in ≥ 4 of 6 cells. Span above the floor with a scrambled ordering is
dispersion, not content; a stable ordering inside the floor is a coin that keeps landing the same
way at this draw count.

## Result 1 — the collapse is a PREMIUM property (D=6, POOLED, median over the 6 cells)

| statistic | span/floor IS | span/floor OOS | collapse? | OOS cells span>floor | ordering survives | verdict |
|---|---|---|---|---|---|---|
| PREM_SHARPE | **1.58x** | **0.75x** | YES | 0/6 | 3/6 | NO OOS CONTENT |
| PREM_CAGR | 1.03x | 0.65x | YES | 1/6 | 6/6 | NO OOS CONTENT |
| SHARPE | 2.79x | **5.49x** | no | 6/6 | 6/6 | **OOS CONTENT** |
| CAGR | 1.75x | 2.16x | no | 6/6 | **0/6** | NO OOS CONTENT |
| MAXDD | 2.75x | **6.69x** | no | 6/6 | 3/6 | NO OOS CONTENT |

`H_REPRO` **HOLDS**: 567's 1.58x IS / 0.75x OOS reproduce here at **1.5809 / 0.7466** (|d| 0.0009
and 0.0034) from an independently rebuilt grid.
`H_COLLAPSE` (OOS ratio below IS ratio for ≥ 3 of 5) is **FALSIFIED — 2 of 5**, and the two are
exactly the two premium statistics. The split is stable across all 8 (D × form) combinations:
PREM_SHARPE and PREM_CAGR collapse in **8/8**, SHARPE and MAXDD in **0/8**, CAGR in **2/8**
(RSS bar only, at D=3 and D=24).
`H_LEVEL` **HOLDS**: level span/floor IS [1.75, 2.79] vs premium [1.03, 1.58]; OOS level
[2.16, 6.69] vs premium [0.65, 0.75] — disjoint in both windows.
`H_NONE` **HOLDS**, but barely: **1 of 5** statistics keeps OOS content, and the same one in
**8 of 8** (D × form) combinations.

Read plainly: a premium is an arm-minus-arm object measured inside one panel, so the parents'
return differences cancel out of it and what is left out of sample is smaller than one panel's own
composition luck. A level inherits those differences whole — which is why its span grows, and why
its span is the *least* informative thing about it (see below).

## Result 2 — the ordering bar, not the span bar: 88 of 90 cells are inside the floor

The span is a two-extreme object. A three-panel ordering claim has to clear its **adjacent** gap,
and that gap is below its own floor in almost every cell:

| D | cells with margin > floor | cells with span > floor |
|---|---|---|
| 3 | **4 / 90** | 66 / 90 |
| 6 | **4 / 90** | 66 / 90 |
| 12 | **2 / 90** | 66 / 90 |
| 24 | **2 / 90** | 70 / 90 |

Median margin/floor at D=6, OOS: PREM_SHARPE 0.18, PREM_CAGR 0.23, CAGR 0.24, SHARPE 0.64,
MAXDD 0.72. Not one of the five reaches 1.0. The two cells that do clear are MAXDD at cadence M.

## Result 3 — where the instability lives: the nested pair

`U56 ⊆ B136` **exactly** (all 55 U56 names are in B136's 135), so "U56 > B136" is not a comparison
of two panels; it is the marginal contribution of B136's other 80 names. That nested pair is the
binding adjacent gap in **21 of 30** OOS cells (SHARPE 6/6, CAGR 6/6, MAXDD 6/6, PREM_CAGR 3/6),
and it is where every ordering flip happens:

- **CAGR** flips 0/6 → the IS order is `B136>U56>SMALL439` in all six cells, OOS is
  `U56>B136>SMALL439` in all six. The whole flip is the nested pair swapping across a gap of
  **0.0036–0.0097** against a floor of **0.024–0.029**. The SMALL439 leg never moves.
- **MAXDD** survives 3/6 → the three failures are the same nested-pair swap at cadence M
  (gap 0.0036–0.0057 vs floor 0.031).
- **SHARPE** survives 6/6 and is the only "OOS content" verdict — but its adjacent gap is the
  nested U56|B136 pair at **0.041–0.092** against an OOS floor of **0.103**, i.e. **0.64x**. What
  its span is actually measuring is `U56/B136 ≈ 1.11 vs SMALL439 ≈ 0.54`: a **large-cap-vs-small-cap**
  fact worth 0.57 of Sharpe against a 0.10 floor, stated three-panel for no reason.

So the one surviving currency supports a two-panel claim, and the three-panel version of it is
inside the floor. Stability across the two windows is also not independent evidence here: the same
overlapping names are in both.

## Rule 8 walk-forward — WF-B, the ordering as a trading instruction

Selector: (parent, gross, cadence) picked on the IS window alone by each statistic in turn; OOS
2017+ read **once**, against RULES v2 on the same panel and against SPY.

| selector | picks | OOS CAGR / Sharpe / MaxDD | RULES v2 (same panel) | SPY |
|---|---|---|---|---|
| PREM_SHARPE | U56 g0.50 M | 9.00% / 1.1924 / −12.42% | 9.45% / 1.2747 / −12.05% | 15.24% / 0.8721 / −33.72% |
| PREM_CAGR | U56 g0.50 M | 9.00% / 1.1924 / −12.42% | 9.45% / 1.2747 / −12.05% | 15.24% / 0.8721 / −33.72% |
| SHARPE | U56 g1.00 M | 18.26% / 1.1936 / −23.73% | 9.45% / 1.2747 / −12.05% | 15.24% / 0.8721 / −33.72% |
| CAGR | B136 g1.00 M | 17.25% / 1.1016 / −28.35% | 7.98% / 1.1185 / −12.24% | 15.45% / 0.8820 / −33.72% |
| MAXDD | U56 g0.50 W | 8.23% / 1.1079 / −12.69% | 9.45% / 1.2747 / −12.05% | 15.24% / 0.8721 / −33.72% |

**All five selectors lose to RULES v2 on OOS Sharpe; all five beat SPY on OOS Sharpe.** Across all
18 REAL MA-RS books: beat RULES v2 OOS Sharpe **3/18**, beat SPY OOS Sharpe **12/18**. The choice
of ranking currency moves the book you end up holding — CAGR picks a different *parent* (B136) and
SHARPE picks a different *gross* (1.00 vs 0.50) — which costs **9.3 pp of OOS CAGR and 11.3 pp of
OOS drawdown** between the extremes of a table whose orderings are inside their own floor.

## KEEP paths (evaluated on every one of the 900 books)

4a **2**, 4b **52**, BOTH **0**. By parent: 4a U56 2 / B136 0 / SMALL439 0; 4b U56 39 / B136 13 /
SMALL439 0. Both 4a passes are DRAW panels, not tradable rules.
Binding 4b failure legs: DD 313, CAGR 191, the full-fail set 206, H1,H2,OOS,DD 88, clean 52.

On the **REAL** parents, 4b passes in exactly **3 of 36** books: `U56 MA-RS g0.75 W`,
`U56 MA-RS g0.75 M`, `B136 MA-RS g0.75 W`. These are **not a new candidate**: they are identical to
lane B's same-day committed rows (0 mismatches over 900), and they are the **single-rung gross**
pass idea 675 already flagged — at g=0.50 the CAGR floor binds, at g=1.00 the DD cap binds, and
only g=0.75 is clean. Memo `2026-09-11_u56-marsrespread-gross075_4b_C_MEMO.md` records the wording
and the reason it is **not proposed for promotion**. 4a is 0 of 36 on the real parents.

## Caveats

- **Survivorship.** `universe_broad.json` and the small panel are current constituents. A premium
  is arm-minus-arm on one panel so the bias largely cancels; the LEVEL spans do not cancel, so every
  level span here is an upper bound and every level floor a lower bound — which biases `H_LEVEL`
  *toward* holding. The conclusion that survives that bias is the negative one (Result 2).
- **U56 draws overlap ~64% by construction** (36 of 55), so its floor is structurally smallest.
  Reported, never corrected; idea 775 is the open question about exactly that.
- **A stable ordering across IS and OOS is not independent evidence** when the panels are nested.
- Two windows and one draw scheme; the margin/floor ratios are point estimates at D ≤ 24, and
  idea 780's open question (how many draws resolve a cross-parent statistic at all) applies here
  with the same force.

## What this retires

Any claim of the form "characteristic X orders U56 > B136 > SMALL439" is an ordering claim, and its
adjacent gap clears the draw floor in **2–4 of 90** cells measured here. The one reading with OOS
content is `{U56, B136} ≫ SMALL439` on SHARPE. A companion follow-up worth pre-registering: report
the **adjacent-gap/floor ratio**, not the span/floor ratio, beside every published panel ordering —
the span passed 66–70 of 90 cells and the ordering bar passed 2–4, so the record has been quoting
the permissive one.
