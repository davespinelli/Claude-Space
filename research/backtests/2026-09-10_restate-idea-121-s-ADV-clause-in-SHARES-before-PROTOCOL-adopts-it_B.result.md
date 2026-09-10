# idea 427 — restate idea 121's ADV clause in SHARES before PROTOCOL adopts it (lane B, 2026-09-10)

**ANSWERED. The clause should be written in SHARES, at a level solved from the dollar capacity
criterion — and its proposed $1M default should not be adopted at all, because it is an artefact
of idea 121's own 4-rung ladder. No book, no KEEP (4a 0/192, 4b 0/192). PROTOCOL.md is NOT edited
by this run; the wording is proposed for Sunday review.**

Script `2026-09-10_restate-idea-121-s-ADV-clause-in-SHARES-before-PROTOCOL-adopts-it_B.py`.
Panel SMALL439, 3 books x 2 instruments x 8 levels x 4 cost rungs = 192 points, all reported.
Tuned parameters: exactly two — the floor INSTRUMENT and its LEVEL.

## Coverage limit (stated first, it bounds everything below)

The queue says "every panel that has volume cached". That is **1 of 3 panels**: `load_volume`
raises for anything but `small=True`, and `data/` holds `volume_small.csv.gz` and no other volume
file. U56 and broad136 volume is queue idea 429 and needs network. SMALL439 is **current
constituents** of a sub-$2B screen, and the missing delisted cohort is exactly the thin, cheap
cohort a liquidity floor argues about — so only floor-minus-floor contrasts on the same days and
book are read here, and the recommendation is built so that it does not rest on any return series.

## Gates

- **G1** `fast_bt` vs `engine.backtest`: max|Δgross| **1.39e-17**, max|Δturnover| **9.02e-17**.
- **G2** idea 121's published EWall g=0.75 CAGR ladder (none/$1M/$5M/$20M) = 10.18 / 5.92 / 1.64 /
  −4.92%; reproduced here as **10.18 / 5.92 / 1.64 / −4.92%** (max |diff| 0.003 pp).
- Capacity criterion reproduces idea 121 exactly: unscreened R20 participation **17.62%** against
  its published 17.6%; held-name ADV p25 $1.35M / p50 $4.59M (idea 119 published $0.87M / $4.33M
  on its own book convention).
- Admission matching: all 8 rungs matched to **≤ 0.5 names/day** by bisection on an admission
  identity, no return input. DV $1M → **252.10** names/day (idea 425 published 252.1).

## The four legs

**(1) Capacity — the share form does the clause's job (P1 and P2 both FALSIFIED).**
At the matched $1M pair the R20 book's participation is **7.27% (DV) vs 6.34% (VOLSH)** — the
share form is *better*, not worse. And the smallest rung meeting idea 121's own 10% bar is
**$0.50M under DV and its 39,125 sh/day twin under VOLSH — the same 281.1 names/day (80.8% of the
panel)**. There is no capacity price for writing the clause in shares.

**(2) The $1M default is a ladder-resolution artefact.**
Idea 121 searched {$0, $1M, $5M, $20M} and reported the smallest *passing* rung as $1M. With rungs
between $0 and $1M the same criterion, same book, same panel, solves at **$0.50M**. Idea 121's
default therefore discards a further **29 names/day** for nothing its own criterion asks for. A
PROTOCOL clause whose default cannot be re-derived from its own criterion should not carry that
default.

**(3) Invariance — the one leg that needs no returns.**
Under idea 197's T1 rescale `px -> px @ diag(c)`, the dollar mask's admitted set moves on
**1.15% / 2.82%** of live ticker-days at σ = 0.10 / 0.25; the share mask moves on **exactly 0** at
both. At matched admission the two masks are genuinely different objects: Jaccard **0.8445**,
**15.55%** disagreement over the union of admitted ticker-days.

**(4) Consequence — the choice is not free (P4 FALSIFIED).**
At matched admission, level for level and cost for cost, the instrument changes **15/96 4a
verdicts** and **1/96 4b verdicts**. "Either wording" is not an available answer.

## The return gap: reported, and deliberately NOT used

VOLSH−DV over the 84 non-identity matched pairs is **+2.74 pp CAGR (median +1.82, positive in
72/84)** and **+0.1551 Sharpe (72/84)** — same sign as idea 425's +1.23 pp / 144-of-144, larger on
these books (EWALL +4.58 pp 28/28, EWGATE +2.02 pp 28/28, RANK20 +1.60 pp 16/28).

**P3 (the gap is a price-composition artefact) is FALSIFIED.** The two swapped sets separate by
**+2.70 price quintiles** (DV-only mean price $53.48, VOLSH-only $4.13), but with a per-stratum
`s*_k` solved so that admission is matched *inside* each quintile the gap survives in **5 of 5**:
+6.60 / +2.30 / +1.77 / +1.76 / +2.00 pp, name-weighted **+2.89 pp** against a pooled +2.57 pp.

A post-hoc diagnostic (not pre-registered) names a mechanism: `px*vol` moves with price, so the
dollar floor ejects a name after it falls and re-admits it after it rises. The DV-only set has run
**+11.01%** over the prior 126d and returns **+0.29%** over the next 126d; the VOLSH-only set has
run **+2.53%** and returns **+28.91%**.

**But that 28.6 pp forward gap is precisely the shape survivorship produces on this panel**: a
name that is cheap and thin today and still a constituent is by construction one that fell and
then survived. The gap is real on SMALL439 and uninterpretable off it. The recommendation below
therefore rests only on legs (1) and (3), which need no return series at all.

## Rule 8 (PROTOCOL rule 8) — the floor never pays for itself

Floor LEVEL chosen on 2010–2016 IS Sharpe, 2017–2026 read once, per book per instrument per cost
(24 cells, all reported in `.walkforward.csv`):

| | OOS CAGR | OOS Sharpe | OOS MaxDD |
|---|---|---|---|
| IS-chosen floor | 5.12% | 0.382 | −37.6% |
| NO-FLOOR control | 5.43% | 0.405 | −37.2% |
| constant $1M | 2.76% | 0.229 | −41.6% |
| live RULES v2 | 3.85% | 0.568 | −14.7% |
| SPY | 15.45% | 0.882 | −33.7% |

The chooser beats the no-floor control in **0/24**, beats the constant $1M in 24/24, beats RULES
v2 in 8/24 and beats SPY in **0/24**. **P5 HOLDS.** DV picks $0 in 12/12; VOLSH picks $0 or
$0.25M. A liquidity floor is a capacity clause; on this panel it is pure cost, and no result may
cite it as a source of return.

## KEEP paths (both, 10 bps, every grid point)

**4a 0/192, 4b 0/192, BOTH 0/192.** 4b binding bars: H2 192, OOS 192, DD 192, H1 187, CAGR 184.
Bars on this window: H1 > 0.891, H2 > 0.858, OOS Sharpe > 0.882, MaxDD ≥ −20.2%, CAGR ≥ 9.89%.

## Recommended wording — proposed PROTOCOL clause 10 (for Sunday review; PROTOCOL.md untouched)

> **10. Liquidity floor (reporting requirement; no default panel change).** Any run that screens
> its panel for liquidity must state the floor's INSTRUMENT, its LEVEL, and the mean admitted
> names/day it produces, and must run the unscreened panel beside it. Write the floor in SHARES —
> `vol.rolling(20).median() >= s` — not dollars: a floor on `(px*vol)` is built on the adjusted
> close and is not invariant under re-adjustment, and the two instruments do not agree (they
> disagree on 15.6% of admitted ticker-days at matched admission and change 4a verdicts on 16% of
> a matched grid). Choose `s` by solving the capacity criterion on the run's own narrowest book —
> the smallest `s` at which one rebalance of the stated capital moves ≤ 10% of the p25 held-name
> 20d median DOLLAR volume — and publish the solving ladder; do not carry a fixed default across
> panels, because a share level is not comparable across panels or across time. A floor is a
> CAPACITY statement: no KEEP may cite a floor as a source of return, and no floor-conditional
> return comparison may be quoted from a current-constituent panel.

**Cost of adopting it, measured:** 0 published verdicts move (4a 0/192 and 4b 0/192 at every rung
of both ladders), one extra ladder per screened run, and the loss of the $1M default.

**What would change the recommendation:** a volume cache for U56 or broad136 (queue idea 429).
Legs (1) and (3) are panel-independent in form but their magnitudes are not, and leg (4)'s 15/96
is a SMALL439 count.

Outputs: `.console.txt` `.ladder.csv` `.capacity.csv` `.maskdiff.csv` `.price.csv` `.pathdiag.csv`
`.grid.csv` `.verdicts.csv` `.walkforward.csv`.
