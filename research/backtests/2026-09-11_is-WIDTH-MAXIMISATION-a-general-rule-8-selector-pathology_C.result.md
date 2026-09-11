# Idea 688 — is-WIDTH-MAXIMISATION-a-general-rule-8-selector-pathology (lane C, 2026-09-11)

**ANSWERED / SPLIT — the MECHANISM is completely general, idea 685's PRICE is not.
KILL for capital (4a 0/288, 4b 0/288; 0 of 3,400 picks beat SPY OOS). No KEEP, no memo.**

Idea 685 found EBAR-MAX takes the widest panel on 5 of 5 book sizes once k is free to 400,
and pays −0.1685 of OOS Sharpe for it. Its stated mechanism was mechanical, not empirical:
`Ebar` is a SUM over panel members, so on a choice set that varies in width, `argmax Ebar`
is `argmax k` up to a breadth factor that barely moves. Nothing in that argument is about
Ebar. Idea 688 tests every count-form selector for the same defect.

**Both halves of the answer:**

1. **The pathology is general and total.** Every count-form criterion tested pins on width at
   a rate of **1.000**, and five of them are *literally the same selector* as "take the
   widest" — pick-for-pick agreement with the K-MAX control **1.000** at every ceiling.
2. **Its price does not generalise, and idea 685's sign is refuted as a general claim.** On
   this ladder the width-pinned policy *gains* **+0.1393 to +0.2330** of OOS Sharpe going
   from a 2.5× to a 10× choice set, where idea 685 measured **−0.1685**. Same mechanism,
   opposite sign — which is what "mechanical" means: an extensive criterion is a **fixed
   policy wearing a selector's clothes**, and whether that policy wins is a fact about the
   data, not about the criterion.

## Construction

**A single-pool width ladder.** q = 1.00 (every panel an i.i.d. uniform draw of columns from
SMALL439 — FORCED, not tuned: only q ≥ 0.75 reaches k = 400 at all, and q = 1.00 is the one
case where all panels come from one pool), k ∈ {40, 60, 80, 100, 200, 400} = **10.0× of
width**, 8 draws → **48 panels, 288 book rows, 3,400 picks.**

**Matched normalisation pairs.** Five criteria are each run against their own k-normalised
twin, where the twin is *literally the same number divided by k* (GATE 2 asserts it at
**0.000e+00**): mean count / breadth, median count / median share, max count / max share,
sd of count / sd of share, names-ever-eligible / coverage share. Within a pair the two
selectors see the same information and differ **only** by the normalisation, so if one pins
on width and the other does not, the missing division is the only explanation left.

Plus, from the record's own population: IS-SHARPE-MAX (its dominant criterion), EWSHARPE-MAX,
SELECTIVITY-MAX (20/Ēbar — inverse-extensive), idea 685's own EBAR-MIN / BREADTH-MIN pair,
and two calibration controls — **K-MAX** (criterion = k; must pin at 1.000) and **RANDOM**
(seeded uniform; measures the test's own false-positive rate). **17 selectors × 5 ceilings,
all reported.**

Two tuned parameters: the **selector set** (17, listed above) and the **choice-set width**
(ceiling C ∈ {60, 80, 100, 200, 400} = 1.5×/2.0×/2.5×/5.0×/10.0×; C = 100 is lane B's
published ceiling, C = 400 idea 685's). Everything else is the record's: RULES v1 gate,
CAND-n/EWall books, GROSS 0.75, weekly, 10 bps, next-day, 260-day warm-up skip,
NS_LAD {5,10,15,20,30}, IS ≤ 2016-12-31. 8 draws instead of lane B's 3 is resolution for a
rate statistic, not a verdict knob; every per-draw pick is published.

## Gates (asserted before any new number was read)

* **G0 REPRODUCTION — PASS.** The k ≤ 100 draws replay lane B's generator and the k ∈ {200,
  400} draws replay idea 685's second generator, each in its own loop order. **30
  panel-overlaps × 14 quantities** (Ebar, breadth, Emed, Ebar_IS, breadth_IS, S1–S5,
  EW_Sharpe, EW_OOS_Sharpe, ADAPT_Sharpe, best_prem) reproduce both committed runs at
  **machine precision, worst 1.421e-14**, 0/30 moving above 1e-9 on any column.
* **G1 k-IDENTITY — PASS.** max |k·breadth − Ebar| over 48 panels = **2.842e-14**.
* **G2 PAIR IDENTITY — PASS at 0.000e+00** on all five pairs.
* **G3 ENVELOPE — PASS.** Exact width, pure SMALL pool, no duplicate columns, inside 439.

## Census — how much of the record sits in this family

**770 MAX/MIN-form selector sites in 340 committed scripts, 142 distinct criteria.** By the
declared lexicon: **rate-form 609 sites (79.1%)**, unclassified 143 (18.6%), **count-form 18
(2.3%), 6 distinct criteria** — `IS_bought` (6), `Ebar_IS` (4), `width` (3), `OOS_bought` (2),
`n_elig_IS` (2), `bought_pp` (1). `IS_Sharpe` alone is 312 sites in 210 files.

So **width-maximisation is not what the record mostly does** — it is a 2.3% corner. Stated
honestly: `bought_pp` reads as a count by the lexicon though its name suggests percentage
points, and the 18.6% unclassified bucket is not adjudicated here. The census is descriptive;
no verdict below is taken from it.

## The extensivity exponent (b = d log|C| / d log k, 48 panels)

| criterion | b | R² | measured | twin | b (twin) |
|---|---|---|---|---|---|
| C_Ebar (mean count) | **+0.9976** | 0.986 | EXTENSIVE | I_breadth | **−0.0024** |
| C_Emed (median count) | **+1.0009** | 0.983 | EXTENSIVE | I_bmed | +0.0009 |
| C_Emax (max count) | **+0.9470** | 0.985 | EXTENSIVE | I_bmax | −0.0530 |
| C_Esd (sd of count) | **+0.9485** | 0.980 | EXTENSIVE | I_bsd | −0.0515 |
| C_cover (names ever eligible) | **+1.0019** | 0.991 | EXTENSIVE | I_cover | +0.0019 |
| X_select (20/Ēbar) | **−0.9976** | 0.986 | INVERSE-EXTENSIVE | — | — |
| IS_Sharpe | −0.0510 | 0.002 | INTENSIVE | — | — |
| EW IS_Sharpe | +0.3049 | 0.079 | MIXED | — | — |
| k (positive control) | +1.0000 | 1.000 | EXTENSIVE | — | — |
| R_rand (negative control) | −0.0006 | 0.000 | INTENSIVE | — | — |

Every count-form criterion is proportional to width (b within 0.053 of 1.0); every
k-normalised twin is flat (|b| ≤ 0.053). **The declared family is confirmed by the measured
exponent on 14 of 15 non-control selectors** — the one exception is EWSHARPE-MAX (b = +0.305,
MIXED), reported as measured.

## The mechanical-argmax test (pin rate, per ceiling; controls calibrate it)

Pin rate = share of the 8 independent draws on which the selector's pick sits at the end its
form points at. Uniform reference 1/|K|; 95% exact-binomial band at C = 400 is [0.000, 0.500].

| selector | C=60 | C=80 | C=100 | C=200 | **C=400** | verdict at C=400 |
|---|---|---|---|---|---|---|
| **EBAR-MAX** | 1.000 | 1.000 | 1.000 | 1.000 | **1.000** | WIDTH-PINNED (p < 1e-4) |
| **EMED-MAX** | 1.000 | 1.000 | 0.875 | 1.000 | **1.000** | WIDTH-PINNED |
| **EMAX-MAX** | 1.000 | 1.000 | 0.875 | 1.000 | **1.000** | WIDTH-PINNED |
| **ESD-MAX** | 1.000 | 1.000 | 0.750 | 1.000 | **1.000** | WIDTH-PINNED |
| **COVER-MAX** | 1.000 | 1.000 | 1.000 | 1.000 | **1.000** | WIDTH-PINNED |
| **EBAR-MIN** (at the floor) | 1.000 | 1.000 | 1.000 | 1.000 | **1.000** | WIDTH-PINNED |
| BREADTH-MAX | 0.375 | 0.250 | 0.250 | 0.000 | 0.000 | WIDTH-NEUTRAL |
| BMED-MAX | 0.250 | 0.250 | 0.375 | 0.000 | 0.000 | WIDTH-NEUTRAL |
| BMAX-MAX | 0.375 | 0.250 | 0.125 | 0.125 | 0.000 | WIDTH-NEUTRAL |
| BSD-MAX | 0.250 | 0.250 | 0.000 | 0.000 | 0.000 | WIDTH-NEUTRAL |
| COVERSHARE-MAX | 0.500 | 0.500 | 0.125 | 0.125 | 0.000 | WIDTH-NEUTRAL |
| BREADTH-MIN | 0.375 | 0.250 | 0.125 | 0.125 | 0.125 | WIDTH-NEUTRAL |
| SELECTIVITY-MAX | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | WIDTH-NEUTRAL (pins at the FLOOR) |
| IS-SHARPE-MAX | 0.375 | 0.375 | 0.250 | 0.000 | 0.000 | WIDTH-NEUTRAL |
| EWSHARPE-MAX | 0.625 | 0.375 | **0.875** | 0.000 | 0.125 | WIDTH-NEUTRAL |
| K-MAX (control +) | 1.000 | 1.000 | 1.000 | 1.000 | **1.000** | WIDTH-PINNED ✔ by construction |
| RANDOM (control −) | 0.625 | 0.000 | 0.250 | 0.000 | 0.125 | WIDTH-NEUTRAL ✔ |

**6 of 17 selectors are EXTENSIVE IN DISGUISE** by the pre-registered bar (pinned ≥ 0.80 and
|b| ≥ 0.70, K-MAX excluded): EBAR-MAX, EMED-MAX, EMAX-MAX, ESD-MAX, COVER-MAX, EBAR-MIN.
**Every matched pair separates at a pin gap of +1.000** (EBAR-MIN/BREADTH-MIN +0.875) — the
extensive member pins, the twin that is the same number divided by k does not. Both controls
land where they should, so the test is calibrated and not measuring itself.

**The five MAX-form count criteria are one selector, not five:** pick-for-pick agreement with
K-MAX is **1.000 at every ceiling** for EBAR-MAX and COVER-MAX, and 0.750–1.000 for
EMED/EMAX/ESD (their only disagreements are at C = 100). SELECTIVITY-MAX and EBAR-MIN are
likewise the same policy in the other direction — identical OOS to 4 decimals (0.2524).

## The price (rule 8: criteria on ≤2016, 2017-01-01.. read once)

| selector | OOS Sharpe C=100 | OOS Sharpe C=400 | **ΔOOS** | ΔOOS CAGR | ΔOOS MaxDD |
|---|---|---|---|---|---|
| EBAR-MAX / COVER-MAX / K-MAX | 0.3841 | **0.5234** | **+0.1393** | +3.23pp | +1.28pp |
| EMED-MAX / EMAX-MAX | 0.3424 | 0.5234 | +0.1810 | +3.95pp | +2.98pp |
| ESD-MAX | 0.2904 | 0.5234 | +0.2330 | +4.89pp | +4.76pp |
| EBAR-MIN | 0.2524 | 0.2524 | 0.0000 | 0.00 | 0.00 |
| IS-SHARPE-MAX | 0.3144 | 0.3650 | +0.0506 | +1.17pp | +1.48pp |
| RANDOM | 0.3076 | 0.3308 | +0.0232 | +0.61pp | +0.01pp |

Mean ΔOOS Sharpe: **disguised selectors +0.1456, everything else +0.0293.**

**Idea 685's −0.1685 does not reproduce here, and that is the finding, not a discrepancy.**
On this ladder width is genuinely good for the book — Spearman(k, OOS Sharpe) over the 288
book rows is **+0.5269** (+0.40 to +0.68 within each n) and mean OOS Sharpe rises monotonically
**0.2516 → 0.2729 → 0.3232 → 0.3725 → 0.4257 → 0.4849** from k = 40 to 400, because a CAND-n
book at fixed n selects from a bigger pool. So the wide end pays here and did not in idea
685's mixed-q choice set.

The criteria cannot be taking credit for that: **mean IS Sharpe by k is not monotone at all**
(0.3324, 0.3270, 0.3039, 0.3920, 0.2672, 0.3487), so nothing an IS selector measures sees the
width→OOS relation; the count-form criteria capture it by riding the axis, not by reading it.
The evidence is EBAR-MIN, the same criterion in MIN form: it takes k = 40 on 8 of 8 draws and
returns **0.2524**, the worst of all 17 selectors, against EBAR-MAX's 0.5234 — best and worst
from one criterion, decided entirely by the direction of the argmax.

**The correct general statement, which this run supports and idea 685's does not:** a count-form
criterion on a width-varying choice set is not a selector at all — it is the constant policy
"take the widest" (or "the narrowest"), and its OOS number is whatever that constant is worth
in that sample. Reporting it as a *selected* result overstates what was measured by the whole
of the width effect.

## PROTOCOL 4a / 4b and the benchmarks (10 bps, every book row)

**4a 0/288. 4b 0/288** — zero at every width (0/48 at each of k = 40, 60, 80, 100, 200, 400).
Pooled book rows: CAGR 4.28%, Sharpe 0.3447, MaxDD −33.69%, halves **0.3809 / 0.3179**,
OOS Sharpe 0.3551 / OOS CAGR 4.79% / OOS MaxDD −32.97%. Against **SPY** (CAGR 14.13%, Sharpe
0.8616, MaxDD −33.72%, halves 0.8907/0.8577, **OOS Sharpe 0.8820**) and **RULES v2** on the
same panels (Sharpe 0.5220, halves 0.4955/0.5482, MaxDD −15.80%, **OOS Sharpe 0.5314**).

**Of 3,400 selector picks, 0 beat SPY's OOS Sharpe** and 344 (10.1%) beat RULES v2; 52.1%
beat the do-nothing choice-set mean. The best arm in the run — the k = 400 pick, OOS Sharpe
0.5234, OOS CAGR 8.56%, OOS MaxDD −29.58% — is still well under SPY on every leg. **Nothing
here is capital-worthy, and no arm is a new book:** CAND-n and EWall are the record's existing
books re-run on re-drawn panels.

## What this does and does not say

* It does **not** overturn idea 685's measurement — its −0.1685 stands on its own ladder, and
  the reproduction gate replays 18 of its panels at 1.421e-14.
* It **does** refute the generalisation. Width-maximisation is a general *mechanical* defect
  (6 of 6 count-form selectors pin at 1.000, every matched pair separates at +1.000) but its
  *cost* is data-dependent and here reverses sign. Any claim of the form "EBAR-MAX is worse"
  is a claim about one sample; "EBAR-MAX is not a selector" is the portable one.
* The practical consequence is narrow, cheap and **proposed, not taken**: a rule-8 selector
  whose criterion is a count should either be normalised by the choice-set dimension it
  varies over, or reported as the fixed policy it is — with the K-MAX agreement rate beside
  it, which costs one column. This run changes no rule and promotes no book.

## Caveats, stated

* 8 draws gives the pin-rate test a floor of 0.125 and a 95% band of [0.000, 0.500] at
  C = 400; separations of 1.000 vs 0.000 are far outside it, but a selector sitting near the
  band edge (EWSHARPE-MAX reads WIDTH-PINNED at C = 100 and 0.125 at C = 400) is not resolved
  by this sample, and is reported as measured rather than smoothed.
* Panel-level criteria return the same pick at every book size, so the independent unit is the
  draw (n = 8), not draw × n (n = 40); the tables use the draw and say so.
* q = 1.00 is forced by the pool bounds. It is what makes the draws exchangeable, and it is
  also why the wide end pays: an all-small-cap pool at k = 400 is the deepest selection pool
  in the run.
* **SURVIVORSHIP** (idea 54, `data/SMALL_PANEL_README.md`): SMALL439 is CURRENT constituents,
  so every level here is optimistic, and q = 1.00 makes this the most exposed corner of the
  record's panels. It moves every panel in a choice set together and so can neither
  manufacture nor hide an argmax concentration — but it does inflate the width→OOS slope that
  makes the wide pick look good, which cuts **against** this run's positive ΔOOS, not for it.

RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py untouched. No KEEP, no memo, no rule
change. Follow-ups filed as 693–695.

Outputs: `.census.csv` `.panels.csv` `.stats.csv` `.books.csv` `.extensivity.csv` `.picks.csv`
`.walkforward.csv` `.console.txt`
