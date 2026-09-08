# Idea 244 — how-many-published-count-dials-are-gross-dials (lane B, 2026-09-08)

**SPLIT. The census is ANSWERED — 95 of 271 decidable published count cells (35.1%; bounds
17.4%–43.6%) move ≥ 5 pp of realised gross across their own quoted grid, and every one of
them is on idea 73's FIXED convention, 0 of 121 NORM cells. But the queue's own reading of
the mechanism is CORRECTED: `GROSS/n` is not a static gross ladder. It is exactly the
equal-weighted width book times a BREADTH-TIMED exposure overlay, and matching the mean
realised gross — the re-quote the queue asked for — removes the overlay's LEVEL while
leaving its TIMING, which is the part that pays. The count dial itself is a KILL under rule
8 (0/126 on 4a; pooled OOS Sharpe 0.983 against RULES v2's 1.050). One PARK by-product.
No RULES change. Nothing in RULES.md, scan.py, bot.py or baseline.py touched.**

Script `research/backtests/2026-09-08_how-many-published-count-dials-are-gross-dials_B.py`,
console `..._B.console.txt`, artifacts `.census.csv` `.census_rejects.csv` `.grid.csv`
`.gross.csv` `.argmax.csv` `.premium.csv` `.leveltiming.csv` `.walkforward.csv`.

## 0. Harness first

`engine.backtest` at `cost_bps=10` is reproduced from the cost-free path at **0.000e+00**.
Idea 240's published `mean_gross` on U56/FIXED is reproduced to **0.001 at n=5 (0.741 vs
0.741)** with the residual widening to 0.007 at n=60 (0.467 vs 0.474); idea 240 evaluates
all seven panels on one common window from 2011-01-13 while this run uses each panel's own
`index[260]`, and that window difference, not the construction, is the gap. Idea 240's two
headline numbers replicate: U56 FIXED gross **0.717 at n=20, 0.467 at n=60**.

## 1. The identity, which is the real finding

For a top-n book, with `n_held(t)` the number of names actually held:

> **FIXEDTOT(n) ≡ NORM(n) × φ_t,  φ_t = n_held(t) / n** — max |weight difference| **≤ 2.8e-17**
> at every n on the live grid.

So idea 73's convention is not "a gross ladder wearing an n label" (the queue's phrasing)
but the width book multiplied by a **market-timing overlay**: it cuts exposure exactly when
few names pass the trend gate. On U56 φ has mean 0.989 → 0.624 and **standard deviation
0.048 → 0.187** as n goes 5 → 60; a dial the record reports as a static level is a
time-varying one. This run therefore separates the overlay's LEVEL (removed by MATCHED)
from its TIMING (not removed), which no earlier run did.

The census's own measure had to be fixed to get this: `n_held ≤ min(n, n_elig)`, because a
name can pass the eligibility gate and still be unrankable (no 252-day history). Using
`n_elig` — the intuitive choice, and this run's first — breaks the identity by up to a full
position weight (3.75e-02). Every number here uses `n_held`.

## 2. Q1, the census — how many published count findings are gross-ladder points

Mechanical scan of **1,969 committed CSVs** with idea 242's published filter verbatim, so
the two censuses are comparable: **694 qualifying count-sweep cells over 69 files**, with
**328 rejections logged with their reason** in `.census_rejects.csv` (113 no Sharpe column,
141 fewer than 3 distinct integer values, 14 parent never ranks on a count, 12 no parent
script, 12 out of range, 1 empty) so the denominator is auditable rather than asserted.

Convention labels, with UNKNOWN counted and never assigned: **FIXEDTOT 222, NORM 135, MIXED
260, UNKNOWN 77.**

| | cells | ladder (span ≥ 0.05 NAV) |
|---|---|---|
| FIXEDTOT, panel mappable | 150 | **95** |
| NORM, panel mappable | 121 | **0** |
| MIXED / UNKNOWN label | 337 | undecidable |
| unmappable panel | 86 | not re-priceable |

- **Point estimate: 95 of 271 decidable cells = 35.1%.** Relative criterion (span/mean ≥ 0.10): 85 of 271 = 31.4%.
- **Deduplicated** to one row per file × count-column × panel × convention *sweep* rather than per Sharpe column: **37 of 102 = 36.3%** — the rate is not an artefact of counting the same sweep three times.
- **Bounds, carrying the undecidables explicitly**: 275 label-UNKNOWN/MIXED cells sit on a mappable panel; under a FIXEDTOT reading 143 of them would be ladders, under NORM 0. **Lower 95/546 = 17.4%, point 35.1%, upper 238/546 = 43.6%.**
- **Coverage limit, published:** only **39.0%** of the census is decidable. 337 cells cannot be labelled from source or column, 86 sit on a panel this run cannot map.
- Span distribution over decidable cells: min 0.000, p25 0.000, median 0.017, p75 0.078, **max 0.555**. 14 of 23 decidable files carry at least one ladder cell.
- **The leverage worry does not materialise:** 0 of 271 cells imply gross > 1.00; max implied gross 0.75. The FIXEDW (`w=0.15`) construction, which would put n=60 at 900% of NAV, is barred by PROTOCOL rule 2 and was declared analytic-only *before* the census was read — and in the event no published count sweep uses it past n=5.
- `Spearman(gross span, published n argmax) = −0.080 (N=271)`: the channel does **not** explain where the record's argmaxes landed. It is a confound in what a cell *means*, not a predictor of what it *chose*.

Size of the channel on the live grid (mean held gross, n = 5 → 60): STK20 **0.719 → 0.164**,
ETF24 0.694 → 0.214, ETF36 0.738 → 0.304, U56 0.741 → 0.467, BSTK100 0.737 → 0.685, B136
0.745 → 0.709, SMALL 0.747 → 0.731. NORM: **0.000 span on all seven**. So "n=60" is a
44%-invested book on U56 and a 16%-invested one on STK20, and the ladder is essentially a
narrow-panel phenomenon.

## 3. Q2, the re-quote at matched realised gross

MATCHED = the NORM book scaled by one scalar per (panel, n) so its mean realised gross
equals that cell's FIXED book's (`mean gross gap −0.0001` over the 42 cells, by construction).

**Width premium** (Sharpe at n=60 minus n=5), mean over the 7 panels:
**FIXEDTOT 0.1966 → MATCHED 0.1371 → NORM 0.1360 — the convention carries 30% of it.** Idea
240's "closing the channel halves the width premium" is directionally right and quantitatively
too strong at record scale: −26% on U56 (0.1730 → 0.1278), −61% on ETF36 (0.2643 → 0.1028),
−7% on B136, and on SMALL the premium *rises* (0.0829 → 0.0985).

**Argmax moves on 2 of 7 panels** (U56 40 → 20, STK20 20 → 60) under MATCHED and 1 of 7
under plain NORM. The STK20 MATCHED argmax at n=60 should not be quoted as a width finding:
idea 242 showed n=30/40/60 are saturated duplicates there.

**KEEP paths, all 126 live points at 10 bps: 4a 0/126.** 4b by convention:

| arm | 4b passes / 42 |
|---|---|
| FIXEDTOT | **10** |
| NORM | 5 |
| MATCHED | **3** |

**7 of the 10 4b passes a FIXED count sweep produces do not survive holding its own realised
gross fixed.** At 25 bps the whole grid gives 4b 2/126. The binding bar on failures is
overwhelmingly drawdown and CAGR (DD alone 14, CAGR alone 12, everything 38).

## 4. Level versus timing — what the re-quote does *not* remove

At the **same n and the same mean realised gross**, FIXEDTOT minus MATCHED over 42 cells:

| statistic | mean | sign |
|---|---|---|
| ΔSharpe | **+0.0480** | positive 37/42 |
| ΔOOS Sharpe | **+0.0587** | positive 36/42 |
| ΔMaxDD | **+0.0413** (FIXED draws down *less*) | — |
| ΔCAGR | +0.09% | — |

The overlay pays in **drawdown, not return** — it is a de-grossing instrument in idea 74's
sense, priced here at roughly 4 pp of MaxDD for nothing in CAGR, and it is inseparable from
the count dial under the record's dominant convention. This is why "re-quote at matched
gross" is a necessary correction but not a sufficient one: it prices the level away and
leaves a market-timing rule inside a dial the record calls "position count".

## 5. Q3, rule 8 — n chosen on 2009-2016 only, 2017-2026 read once

Pooled equal-weight over the 7 panels, **10 bps**:

| arm | OOS CAGR | OOS Sharpe | OOS MaxDD |
|---|---|---|---|
| **NOTHING (RULES v2)** | 8.5% | **1.050** | −13.2% |
| ISARGMAX-FIXEDTOT | 11.7% | 0.983 | −18.7% |
| EWALL (no count dial) | 10.5% | 0.894 | −24.3% |
| **SPY** | **15.5%** | 0.882 | −33.7% |
| ISARGMAX-MATCHED | 8.6% | 0.851 | −20.4% |
| ISARGMAX-NORM | 12.1% | 0.847 | −24.8% |
| RULES v1 | 7.8% | 0.636 | −21.6% |

At **25 bps**: v2 1.009 > FIXEDTOT 0.887 > SPY 0.882 > EWALL 0.770 > NORM 0.754 > MATCHED 0.753.

**The count dial loses to doing nothing on 5 of 7 panels (FIXEDTOT), 7 of 7 (NORM and
MATCHED) at 10 bps — and on 7 of 7 for all three arms at 25 bps.** Against SPY the FIXEDTOT
chooser wins 6/7 at 10 bps and 3/7 at 25. That is another instance of the record's recurring result that a fitted dial
loses to the incumbent. The IS pick is identical under FIXEDTOT and MATCHED on only **3 of
7** panels, so the convention also changes *what an IS chooser selects*, not merely how the
selection scores. FIXEDTOT minus MATCHED on the chooser's own OOS Sharpe is **+0.1324, sign
positive on 6/7** — but that number conflates the pick with the construction; the clean
same-n version above (+0.0587) is the one to quote.

## 6. Verdicts

- **Q1 ANSWERED, with published bounds:** 35.1% of decidable published count cells (17.4%–43.6% over the undecidables) are gross-ladder points; all of them FIXEDTOT, none NORM.
- **Queue premise CORRECTED:** the construction is a breadth-timed overlay, not a static ladder, and matching mean gross does not undo it.
- **Count dial KILLED as a selector** (4a 0/126, rule 8 below do-nothing on 5/7 panels at 10 bps and 7/7 at 25).
- **No KEEP, no memo, no RULES change.** The grid's best 4b point, STK20 n=20 FIXEDTOT (12.0% / 1.337 / −12.1%, OOS 1.446), is a **0.492-gross book on the 20-mega-cap panel idea 10 already flagged as selection** — i.e. the purest gross-ladder point in the run, and disqualified for exactly the reason this run exists.
- **PARK by-product:** φ_t = n_held/n as a standalone de-grossing instrument, priced at +0.048 Sharpe / +4.1 pp MaxDD for ~0 CAGR at matched mean gross on 37 of 42 cells. It has never been tested on its own, only smuggled inside count sweeps. Queued as a new idea rather than promoted.

## 7. Recommendations for the record

1. **Any published count/position finding on a FIXED `GROSS/n` book must carry its realised-gross span.** On narrow panels (STK20, ETF24, ETF36) the span reaches 0.48–0.56 of NAV and the "count" reading is not recoverable without it.
2. **A matched-mean-gross control is necessary but not sufficient.** State that it leaves the overlay's timing, and quote the same-n ΔSharpe beside it.
3. **Never quote a 4b pass count off a FIXED count grid without its MATCHED twin** — this run's own grid loses 7 of 10.

## Survivorship

Every panel is CURRENT constituents, one-directional, hardest on STK20 / BSTK100 / SMALL;
the SMALL panel additionally drops the 44 tickers with `max_1d_move ≥ 1.0`. Widening n on a
survivor list adds names known ex post to have survived, so any "wider is better" reading is
partly manufactured — which is why this run's headline is a convention statistic (gross
span) and not a width verdict. The census inherits the bias of every parent script it reads.

## 8. CONCORDANCE with the concurrent cloud run of the same idea

The cloud lane ran idea 244 independently the same day
(`2026-09-08_how-many-published-count-dials-are-gross-dials_cloud.py`) and pushed first;
this run was written and executed without sight of it. Filing the comparison rather than a
second copy of the claim.

**The two runs agree on every shared claim, and on none of them by construction — the
designs differ.**

| | cloud lane | lane B (this run) |
|---|---|---|
| census unit | 424 committed **scripts**, regex over source | 1,969 committed **CSVs** → 694 cells / 232 sweeps over 69 files |
| what is counted | 127 scripts carry a count dial; **53 (42%) contain the exposed `g/n` construction**; 62 of 127 (48.8%) publish no gross column | **95 of 271 decidable cells (35.1%)** move ≥ 5 pp of realised gross across their own grid; bounds 17.4–43.6% |
| unlabelable share | UNKNOWN 47 of 127 = **37%** | UNKNOWN/MIXED 337 of 694; decidable coverage **39.0%** |
| the identity | NORM ≡ FIXED on every day with `k_t = n`, **2.776e-17** | the general form: FIXEDTOT ≡ NORM × φ_t, φ_t = n_held/n, **≤ 2.8e-17** at every n |
| the tie/held-count trap | found it: "`rank <= n` drops TIED names, so k_t < n on 265 days at n=5" | found it independently: n_held ≤ min(n, n_elig); using n_elig breaks the identity by a full position weight |
| control | gross **PINNED** at nominal (NORM) | gross **MATCHED** to the FIXED cell's own realised mean (the queue's literal ask), NORM also reported |
| width-premium shrink | −38% u56, −13% broad136, −19% small439 | −26% U56, −7% B136, +19% SMALL; **mean −30%** over 7 panels |
| verdict flips | **4 of 108** 4b verdicts; 18 of 270 pairwise width comparisons | 4b **10/42 → 3/42** under MATCHED |
| rule 8 | convention changes the IS-chosen n on **2 of 3** panels; neither convention beats RULES v2 OOS on any panel (0/6) | changes the pick on **4 of 7**; FIXEDTOT beats v2 on 2/7, NORM and MATCHED 0/7 |
| 4a | 0 of 216 | 0 of 126 |

**Agreements that matter:** the channel is real and undisclosed; its size is a
panel-breadth fact, largest on the narrowest panels; idea 240's "halves the width premium"
is a u56-magnitude statement and too strong as a record-wide one (−38%/−30% by two
different measures); the count dial does not beat the incumbent out of sample under either
convention; and both runs independently arrive at the same recommendation — publish
realised gross beside every count/width arm.

**Differences, all traceable to design, none contradictory:** the ~42% (scripts containing
the construction) and 35.1% (cells whose realised gross actually moves) are different
questions with the same answer to one significant figure — a script can carry `g/n` on a
panel broad enough that gross barely moves, which is exactly the SMALL panel here (span
0.017). The premium magnitudes differ because the grids do (their n ≤ 90 at g=1.00, mine
n ≤ 60 at g=0.75) and because the premium endpoints differ (|Sharpe(90) − Sharpe(20)| vs
Sharpe(60) − Sharpe(5)).

**What this run adds that a pinned-gross design cannot see:** pinning gross removes the
overlay's level *and* its timing together. Matching the mean removes only the level, and
the residual — +0.0480 Sharpe, +0.0587 OOS Sharpe, +4.1 pp MaxDD at the same n and the same
mean gross, on 37 and 36 of 42 cells — is the timing. So the cloud lane's proposed
Sunday clause ("quote realised gross beside Sharpe, or state that the construction pins
gross") is **necessary but not sufficient**, and this run's section 4 is the reason.

**The cloud run's cross-link corroborates section 3 of this one:** it found idea 459's
single 4b-clearing ranked point (u56 TOP40 g=1.00, 12.68%/1.1242/−18.16%) is itself a
gross-ladder point whose pass disappears when gross is pinned (MaxDD −21.68%, outside the
−20.23% bar). That is the same result as "7 of the 10 4b passes a FIXED count sweep
produces do not survive holding its own realised gross fixed", reached on a different
grid.
