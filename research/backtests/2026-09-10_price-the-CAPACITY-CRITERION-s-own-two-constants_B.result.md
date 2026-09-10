# Idea 647 — price-the-CAPACITY-CRITERION-s-own-two-constants (lane B, 2026-09-10)

**ANSWERED / no KEEP. The criterion does not have two constants — it has one.**
Idea 121's/427's `participation = per_trade_frac x ticket / p25` is *exactly* linear in the
ticket and the bar enters only as a threshold on it, so only the ratio **R = ticket / bar**
is identified. Over 64 (ticket, bar) pairs x 2 instruments, spanning 40 distinct ratios of
which 17 are hit by more than one pair, **the selected floor disagreed within a ratio 0 times**,
and the linearity check is exact to 1.7e-18. `($10M, 10%)`, `($1M, 1%)` and `($250M, 250%)`
are the same clause: **R = $100M**. A PROTOCOL clause that publishes both numbers publishes one.

## The surface (P2 HOLDS — R is load-bearing)

Sweeping tickets `{$1M .. $250M}` x bars `{2% .. 33.3%}` on idea 427's own 8-rung ladder:

| | 2.0% | 5.0% | 7.5% | **10.0%** | 15.0% | 20.0% | 25.0% | 33.3% |
|---|---|---|---|---|---|---|---|---|
| $1M | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| $5M | 5M | 0.5M | 0.25M | 0 | 0 | 0 | 0 | 0 |
| **$10M** | 10M | 5M | 1M | **0.5M** | 0.25M | 0 | 0 | 0 |
| $50M | -- | 20M | 10M | 10M | 5M | 5M | 5M | 2M |
| $250M | -- | -- | -- | -- | -- | -- | 20M | 10M |

(DV instrument; `--` = no rung on the ladder meets the bar. Full 64x2 table in `.surface.csv`.)

**All 8 of 8 rungs are selected by some pair on DV** (7 of 8 on VOLSH), and **11/64 DV pairs
(17/64 VOLSH) have no admissible rung at all**. As one dial, the whole criterion is a step
function of R: DV picks `$0` below R=$57M, `$0.25M` to $90M, `$0.5M` to $108M, `$1M` to $140M,
`$2M` to $202M, `$5M` to $404M, `$10M` to $754M, `$20M` to $1,090M, nothing above.

## The published default (P3 HOLDS)

idea 121's **$1M is the answer on 3/64 coarse pairs (4.7%) and 0/64 refined ones.** On a
33-rung log ladder ($25k..$20M) the published pair R=$100M solves at **$0.412M**, not the
$0.50M idea 427 read off its own 8 rungs and not the $1M idea 121 read off its 4. Coarse ==
refined on only 23/53 DV pairs; median overshoot ratio 1.29x (DV) / 1.58x (VOLSH), max
overshoot $4.52M. This replicates idea 646's defect on the very clause 427 proposed.

## Three further defects the sweep exposes

1. **The passing set is not always an up-set.** `kappa` is monotone non-increasing in the floor
   on DV but **NOT on VOLSH** (one up-step at $20M, where the book falls to 11.9 held names and
   turnover rises back to 19.6x/yr). "The smallest passing rung" is therefore not a solution
   concept on the share instrument without a stated monotonicity check.
2. **The criterion's own answer moves between windows.** Solved on the IS half alone it matches
   the full-sample answer on **110/128 (85.9%)** of (pair, instrument) points — it agrees at the
   published pair, but 1 in 7 elsewhere it does not.
3. **There is an unswept THIRD constant.** The criterion fixes the p25 quantile. Re-solving at
   p50 changes the selected rung on **29/64 (DV) and 30/64 (VOLSH)** pairs. Reported as a
   diagnostic only; it selects nothing here (2 tuned params: ticket, bar).

## Instruments (P4 HOLDS)

DV and admission-matched VOLSH select the identical rung on **54/64 pairs (84.4%)**, so idea
427's shares-vs-dollars recommendation is not disturbed by the constants — but the DV ladder
spans a far wider performance range (EWALL CAGR 15.10 pp vs 4.68 pp; Sharpe 0.841 vs 0.312).

## Books, both KEEP paths, rule 8 (P5 HOLDS)

Grid = 3 books x 2 instruments x 8 levels x 4 cost rungs = 192 points, all reported in
`.grid.csv`. **4a 0/192, 4b 0/192.** Binding 4b bars: H2 192, OOS 192, DD 192, H1 187, CAGR 184.
Best full-sample point is the NO-FLOOR control (EWALL, 10 bps): CAGR 10.18%, Sharpe 0.678,
MaxDD -36.2%, H1/H2 0.797/0.614 — against RULES v2 0.572 (0.570/0.577, MaxDD -14.7%) and SPY
0.862 (0.891/0.858, MaxDD -33.7%). Every floor moves it down.

Rule 8 (IS 2010-2016 -> OOS 2017-2026, mean over 24 book x instrument x cost cells):

| arm | OOS CAGR | OOS Sharpe | OOS MaxDD |
|---|---|---|---|
| IS-Sharpe pick over the ladder | 5.12% | 0.382 | -37.6% |
| criterion floor at R=$100M | 4.13% | 0.318 | -39.6% |
| criterion floor solved on IS only | 4.13% | 0.318 | -39.6% |
| **NO-FLOOR control** | **5.43%** | **0.405** | **-37.2%** |
| idea 121's $1M | 2.76% | 0.229 | -41.6% |
| RULES v2 (live) | 3.85% | 0.568 | -14.7% |
| SPY | 15.45% | 0.882 | -33.7% |

The IS-chosen floor beats the no-floor control **0/24** and SPY **0/24** (it beats the published
$1M 24/24 — the only thing a floor reliably beats is a worse floor). The criterion's own floor
beats no-floor 3/24. This re-confirms idea 427's finding at every point of the constant surface:
**a liquidity floor is a capacity clause and never a performance clause.**

## Gates

G1 `fast_bt` == `engine.backtest`, max|dgross| 1.39e-17, max|dturnover| 9.02e-17.
G2 idea 121's published EWall g=0.75 CAGR ladder (10.18 / 5.92 / 1.64 / -4.92%) reproduced to
0.003 pp. Unscreened RANK20 participation reproduces idea 121's published 17.6% at 17.62%, and
the published pair reproduces idea 427's $0.50M exactly.

## Coverage and survivorship

SMALL439 only — `load_volume` raises for U56 and broad136, which is queue idea 429 and needs
network. SMALL439 is **current constituents** of a sub-$2B screen, so every dollar-volume
statistic here is measured on names still listed today and the thin cohort a floor argues about
is the cohort that is missing. Only floor-minus-floor and pair-minus-pair contrasts on the same
days are read; no book is proposed.

## Proposed wording (Sunday review; PROTOCOL.md NOT edited by this run)

Amendment to idea 427's proposed clause 10, replacing its two constants:

> ... Choose `s` by solving the capacity criterion on the run's own narrowest book: the smallest
> `s` at which one rebalance moves <= 10% of the p25 held-name 20d median DOLLAR volume **per
> $100M of stated capital**. State that ratio (capital / participation bar), not the two numbers
> separately — they are not separately identified — and solve on a ladder refined until the next
> rung down fails, publishing the solving ladder. A floor selected from a coarse ladder is a
> resolution artefact, not a solution. State the quantile, and check that the passing set is an
> up-set before quoting a "smallest passing" rung.

Script: `research/backtests/2026-09-10_price-the-CAPACITY-CRITERION-s-own-two-constants_B.py`
(83s, deterministic). Artefacts: `.console.txt` `.capacity.csv` `.surface.csv` `.refined.csv`
`.grid.csv` `.walkforward.csv`.
