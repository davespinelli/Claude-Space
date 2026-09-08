# Idea 249 — do-de-grossing-instruments-belong-armed-only-in-crashes-after-all (lane B, 2026-09-08)

**Verdict: NO — KILL of the queue's premise, and the KILL is not a cost story.** Once realised
mean gross is matched, arming `gross50` or `ddctl8` only in the SPY<200d crash regime costs
**−0.97 pp/yr of CAGR** at 10 bps (5/36 and 2/36 cells positive, sign p 0.0000 both families),
is **Sharpe-neutral** (−0.0059 / −0.0051 median, 17/36 and 14/36 positive — coin flips), and
loses **just as much at 0 bps** (−0.98 / −0.91). The explicit switching bill against the arm's
own matched control is **+0.049 / −0.024 pp/yr** — a rounding error — so `switch_mult` is not
the mechanism the queue suspected. Idea 246's "+12.6 and +5.8 pp/yr ON crash days" is a
**pure gross-arithmetic artefact**: it is holding 0.375 of a book while the market falls,
which the matched static control also does. What survives matching is a genuine but paid-for
**drawdown purchase** (MaxDD 4.5–5.9 pp shallower than the matched static), already the record's
known idea-94 result. **No KEEP. RULES.md, scan.py, bot.py and baseline.py untouched.**

Script `research/backtests/2026-09-08_do-de-grossing-instruments-belong-armed-only-in-crashes-after-all_B.py`.
3 panels (u56 56 names, broad 136, small 439 after idea 130's bad-split drop) x 3 ungated base
books (V1u, TOP20, EWall) x 3 cost rungs (0 / 10 / 25 bps) x {control, 8 always-on arms, 8
spy200 arms, 8 breadth20 arms, 16 gross-matched static controls} = **1,107 runs, every one
printed and written to the `.grid.csv`**. Exactly TWO tuned dimensions: FAMILY (gross, ddctl)
and STRENGTH (m ∈ {0.00, 0.25, 0.50, 0.75}; D ∈ {0.04, 0.08, 0.12, 0.16}, k = 0.5 fixed at its
published value). Panels, books, cost rungs and the regime are reported, never selected on.
Idea 94's harness and idea 246's `run_cond` are imported, not re-implemented.

Harness gates, asserted before any number was read: **CHECK (a)** `run_cond` with no instrument
equals `engine.backtest` at **max|diff| = 0.000e+00** on returns at all three cost rungs.
**GROSS MATCH:** each of the 432 matched static controls is solved to its arm's own realised
mean gross in its own cell and rung — max |achieved − target| **8.63e-05**, mu range
0.8262–1.0571. Every arm is re-run at each rung; nothing is derived from a turnover identity,
because the ddctl state machine reads NET equity and so its book is cost-dependent.

## 1. H1 — the decisive table: conditional arm minus its OWN matched-gross static control

Raw whole-sample differences. Nothing is divided by the armed fraction, so idea 246's LEAK
amplifier ((1−f)/f = 4.9) is not in play anywhere below.

| regime | rung | family | n | d_CAGR (pp/yr) | positive | sign p | d_Sharpe | positive | d_MaxDD |
|---|---|---|---|---|---|---|---|---|---|
| spy200 | 0 bps | gross | 36 | **−0.958** | 5/36 | 0.0000 | +0.0026 | 20/36 | +0.0598 |
| spy200 | 0 bps | ddctl | 36 | **−0.867** | 1/36 | 0.0000 | −0.0031 | 15/36 | +0.0455 |
| spy200 | **10 bps** | gross | 36 | **−0.937** | 6/36 | 0.0000 | −0.0059 | 17/36 | **+0.0586** |
| spy200 | **10 bps** | ddctl | 36 | **−0.966** | 2/36 | 0.0000 | −0.0051 | 14/36 | **+0.0450** |
| spy200 | 25 bps | gross | 36 | −0.933 | 4/36 | 0.0000 | −0.0095 | 13/36 | +0.0493 |
| spy200 | 25 bps | ddctl | 36 | −1.034 | 4/36 | 0.0000 | −0.0063 | 11/36 | +0.0459 |

Robustness never selected on — `breadth20` instead of `spy200` gives the same answer with the
same signs: d_CAGR −0.64 (gross) / −0.64 (ddctl) at 10 bps, 1/36 and 0/36 positive, and the
same Sharpe coin flip (15/36, 14/36).

Per (family, strength) at 10 bps, medians over the 9 panel x book cells — the loss is present at
every one of the 8 grid points and does not have an interior escape:

| arm | d_CAGR vs matched | pos | d_Sharpe vs matched | pos | d_ann vs CONTROL | d_ann vs ALWAYS | switch_mult | mean gross |
|---|---|---|---|---|---|---|---|---|
| gross00 | −1.278 | 2/9 | −0.0591 | 1/9 | −3.230 | +8.975 | n/a (TO_always ≈ 0) | 0.619 |
| gross25 | −1.182 | 2/9 | −0.0129 | 3/9 | −2.424 | +6.734 | 24.36 | 0.652 |
| **gross50** | **−0.956** | 1/9 | +0.0114 | 6/9 | −1.617 | +4.493 | 12.47 | 0.685 |
| gross75 | −0.483 | 0/9 | +0.0139 | 7/9 | −0.807 | +2.250 | 8.50 | 0.718 |
| ddctl04 | −0.986 | 1/9 | +0.0055 | 5/9 | −1.730 | +3.564 | 9.15 | 0.692 |
| **ddctl08** | **−1.188** | 1/9 | +0.0109 | 5/9 | −1.626 | +2.456 | 7.43 | 0.701 |
| ddctl12 | −0.664 | 0/9 | −0.0093 | 3/9 | −1.075 | +1.546 | 6.72 | 0.726 |
| ddctl16 | −0.950 | 0/9 | −0.0095 | 1/9 | −0.893 | +1.283 | 6.46 | 0.738 |

## 2. H2/H3 — where idea 246's crash-day surplus actually came from, and what the cost bill is

The three comparands disagree by construction, and the gross column is why (spy200, 10 bps,
medians over 36 cells): mean realised gross is **0.750 (control) / 0.671 (gross-family arm) /
0.281 (always-on)** and **0.750 / 0.712 / 0.590** for ddctl. Against the always-on sibling the
conditional arm gains **+4.49 / +2.46 pp/yr** — that is idea 246's finding, and it is the arm
holding twice as much of a rising book. Against the unmatched control it loses −1.47 / −1.19.
Against the **matched** control, which holds the identical mean gross, it loses −0.97 / −0.97.
Only the last of the three has the exposure confound removed, and it is the one that answers
the queue.

The switching cost is real but tiny where it matters. `switch_mult = (TO_cond/TO_always)/f` is
**12.47 (gross) and 7.49 (ddctl)** at the median — inside and above the queue's quoted 5.9–11.6x
band, > 1 in 27/36 and 36/36 cells — but it is large mostly because the always-on gross lever
barely trades (1.81x/yr). Against the arm's own matched control the turnovers are **12.70x vs
12.42x** (gross) and **12.89x vs 13.14x** (ddctl), i.e. the base book's own weekly rebalancing
dominates both, and the explicit bill is **+0.049 and −0.024 pp/yr**. The 0-bps rung settles it:
the loss is **−0.98 / −0.91 at zero cost** against **−0.97 / −0.97 at 10 bps**. Charging the
switching cost explicitly, as the queue asked, changes the answer by less than 0.1 pp/yr.

## 3. H4 — both KEEP paths, all 1,107 rows

| row class | n | 4a | 4b |
|---|---|---|---|
| CONTROL (do nothing) | 27 | 5 | **0** |
| ALWAYS-ON | 216 | 71 | 15 |
| **COND spy200** | 216 | 79 | **59** |
| COND breadth20 | 216 | 53 | 33 |
| MATCHED (spy200 gross) | 216 | 43 | 9 |
| MATCHED (breadth20 gross) | 216 | 39 | 0 |

**57 of 216** spy200 arms pass 4b where their own matched-gross twin does not (4a: 38/216), and
that is the honest residual: the arm buys drawdown a static de-gross cannot. Best at 10 bps —
`broad/EWall/ddctl04` 11.93% / **1.2225** / −17.33%, halves 1.3054/1.1423, OOS 1.2516; and
`u56/EWall/gross50` 11.21% / **1.2052** / −15.59%, halves 1.1989/1.2132, OOS 1.2991 (SPY over
the same window 15.23% / 0.889 / −33.72%, OOS 0.882).

**None of it is a KEEP.** 4a here is judged against RULES v1 (idea 246's imported `keep_paths`,
the pre-2026-09-06 convention). Against the LIVE **RULES v2** — u56 @10 bps 8.66% / **1.2056** /
**−12.05%**, halves 1.2259/1.1909, OOS 1.2851 — the best conditional arm loses H1 (1.1989 vs
1.2259) and carries a 3.5 pp deeper drawdown, so it fails 4a on the live book. The 4b passes are
the drawdown-cap passes idea 94 already priced, on the same EWall shape idea 246 already PARKed.

## 4. Rule 8 — walk-forward, (FAMILY, STRENGTH) chosen on 2009–2016 IS Sharpe alone

Menu = 8 spy200 arms + the do-nothing control + all 8 matched static controls; 2017–2026 read
once, 27 (panel, book, cost) cells.

* chooser picks a **conditional arm in 13/27**, a **matched static in 14/27**, do-nothing 0/27 —
  in more than half the cells the in-sample evidence says *hold less all the time*, not *time it*.
* OOS regret vs do-nothing: mean **+0.0140**, **median +0.0001**, wins 19/27.
* OOS regret vs the best matched static: mean +0.0136, **median +0.0000**, wins 12/27.
* IS pick == OOS oracle among the conditional arms in **1/27**; median Spearman(IS, OOS) **0.118**.
* Every pick gives up OOS CAGR: at 10 bps the pick's median OOS CAGR is **12.55% vs 13.82%** for
  do-nothing (0 bps 12.22% vs 13.91%; 25 bps 12.35% vs 12.57%). Best cell +0.157 Sharpe
  (broad/EWall @0 bps), worst −0.019 (small/V1u @10 bps).

A median regret of one ten-thousandth of Sharpe bought with 1.3 pp/yr of OOS CAGR is the
record's do-nothing result again — the **17th** entry in the selection-loses census.

## 5. What this settles

1. **The queue's question is answered NO.** Idea 6's breadth sleeve and idea 40 were killed on
   the full-period number, and matching realised gross does not rescue either: the crash-armed
   version loses ~1 pp/yr of CAGR to a constant de-gross holding the same average exposure.
2. **The mechanism is not switching cost.** The queue named `switch_mult` 5.9–11.6x; it is real
   (7.5–12.5x here) and it costs < 0.05 pp/yr, because the base book's weekly rebalance already
   dominates turnover. The loss survives at 0 bps intact.
3. **Idea 246's d_on/d_off table needs a gross column.** "+12.6 / +5.8 pp/yr ON crash days" is
   measured against a control at 0.75 gross while the arm sits at 0.375. Against a control at
   the arm's own realised gross the surplus disappears and the sign of the whole-sample answer
   with it. Any future "instrument X pays in regime R" claim should carry the matched-gross row.
4. **What is left is a drawdown purchase at a known price**, not an edge: 4.5–5.9 pp of MaxDD
   for ~1 pp/yr of CAGR and no Sharpe. That is idea 94's price list, re-derived.

## Caveats carried, not buried

* SURVIVORSHIP: all three panels are current-constituent lists (idea 54), so every absolute CAGR
  in sections 3–4 is optimistic and should be read as an upper bound. Sections 1–2 are paired
  differences inside one cell on the same days and are far less exposed.
* The small panel drops the 44 bad-split tickers of `data/small_meta.csv` (439 names) and holds
  SPY as a benchmark only, never as a constituent.
* `spy200` and `breadth20` are two regimes, not the space of regimes; `hivol80` is not re-run
  here because idea 246 showed both de-grossing families reverse sign under it (d_on −7.86 /
  −7.33) — that arm is idea 247's, not this one's.
* The matched control is a CONSTANT multiplier. A different gross-neutral comparand (e.g. a
  vol-targeted book at the same mean gross) could give a different number; the constant one is
  chosen because it is the parameter-free default and adds no third tuned dimension.
* 4a counts in the `.grid.csv` are against RULES v1 (idea 246's imported helper). The live-book
  comparison is section 3 and `.livebase.csv`; no 4a count here is a claim against RULES v2.
