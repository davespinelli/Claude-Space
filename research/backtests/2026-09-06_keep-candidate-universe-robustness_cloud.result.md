# Idea 53 — keep-candidate-universe-robustness — **ANSWERED: composition-ROBUST, list-SPECIFIC → PARK/SCOPE**

2026-09-06, cloud lane. Script `2026-09-06_keep-candidate-universe-robustness_cloud.py`; outputs
`.grid.csv`, `.loo.csv` (55 leave-one-out panels), `.draws.csv` (800 panels), `.walkforward.csv`,
`.console.txt`.

## Setup

Idea 2's KEEP candidate held fixed: RULES v1's two-clause gate (`px > 200d MA` AND `vol20 < 0.60`),
composite score with **no** vol scaler, top-n equal weight at `gross/n` (de-gross to cash), weekly,
10 bps, decided at close t and applied at t+1, first 260 rows dropped. Tuned parameters (≤2):
`n ∈ {10,20,30}` and `d` = names dropped `∈ {0,1,5,10}`; all points reported. Gross held at 0.75
because today's idea 287 showed it is a Sharpe-neutral level dial.

SPY is the same never-tradable series on every draw, so the 4b level bars are constants:
**MaxDD ≥ −20.23%, CAGR ≥ 10.66%** (SPY 15.23% / 0.8890 / −33.72%, H1 0.9566, H2 0.8340, OOS 0.8820).

**The control that makes the headline readable.** Dropping names shrinks the pool, and idea 287
(same day, sibling book) established that the 4b drawdown cap is a monotone readout of pool size at
fixed n. So a high pass rate at d=10 could be a size artefact. Every U56 draw is therefore paired
with a **size-matched random panel of the same k drawn from universe_broad.json's 135 names**
(200 each at k=50 and k=45).

## 0. The fitted panel

| n | CAGR | Sharpe | MaxDD | H1 / H2 | OOS Sharpe | 4a | 4b |
|---|---|---|---|---|---|---|---|
| 10 | 13.01% | 0.9385 | −17.54% | 0.930 / 0.952 | 0.9895 | no | fail (H1) |
| **20** | **12.74%** | **1.0976** | **−18.15%** | **1.097 / 1.104** | **1.1684** | no | **PASS** |
| 30 | 11.18% | 1.1214 | −16.51% | 1.063 / 1.177 | 1.2512 | no | PASS |

Anchor margins against the five 4b bars: H1 **+0.140**, H2 **+0.270**, OOS **+0.286**, DD **+2.08pp**,
CAGR **+2.08pp** — not a knife-edge pass on any bar. RULES v2 (live) on U56 is 8.68% / 1.2127 /
−11.90%, OOS 1.2937: **4a fails everywhere in this run (0 of 800+ panels)**, and the live book beats
the candidate out-of-sample on the fitted panel too.

## 1. Composition — the candidate is NOT a knife edge on U56's membership

| perturbation | panels | 4b pass rate | median Sharpe | median MaxDD | first-failing bar among failures |
|---|---|---|---|---|---|
| d=1 leave-one-out (exhaustive) | 55 | **100%** (55/55) | 1.0636–1.1306 (range) | −19.03%..−17.77% | – |
| d=5 dropped at random | 200 | **96.5%** | 1.0947 | −18.14% | H1 6, CAGR 1 |
| d=10 dropped at random | 200 | **87.0%** | 1.0801 | −17.93% | H1 20, CAGR 6 |

No single name is load-bearing: removing any one of the 55 leaves 4b intact, with the whole
leave-one-out Sharpe range (1.064–1.131) straddling the full panel's 1.0976. The most costly single
removals are NFLX (−0.034 Sharpe), NVDA, LLY, UNG, AAPL; the most helpful are XBI, SMH, XLI, GOOGL,
MSFT (+0.033) — i.e. the ETF sleeves are a *drag* on this book, not its support. When 4b does break
at d=10 it breaks on **H1** (10.0% of draws) and CAGR (5.5%); the drawdown cap and the OOS bar never
fail in 400 U56 draws. **The queue's premise — "a KEEP that survives only one composition" — is
refuted for composition WITHIN the list.**

## 2. Size control — but the candidate IS specific to the U56 list

| panel source (n=20) | k | 4b pass rate | median Sharpe | median H2 | median OOS Sharpe | median MaxDD |
|---|---|---|---|---|---|---|
| U56 minus 5 | 50 | **96.5%** | 1.0947 | 1.1187 | 1.1769 | −18.14% |
| random from B136 | 50 | **46.0%** | 0.9779 | 0.8835 | 0.9797 | −18.83% |
| U56 minus 10 | 45 | **87.0%** | 1.0801 | 1.1233 | 1.1874 | −17.93% |
| random from B136 | 45 | **45.0%** | 0.9783 | 0.9015 | 0.9976 | −18.54% |

At **matched pool size** the gap is 96.5% vs 46.0% and 87.0% vs 45.0%. The drawdown distributions
are nearly identical (median −18.1% vs −18.8%), so size is not doing the work here: the difference
is the return axis — median H2 Sharpe 1.12 vs 0.88, median OOS 1.18 vs 0.98. Random large-cap panels
fail on **H2 (30.5% / 21.5%) and the CAGR floor (39.5% / 46.5%)**, bars the U56 draws essentially
never fail.

Two things follow. First, **a ~45–46% 4b pass rate for an arbitrary same-size large-cap panel is the
base rate of the bar itself** (it lands on idea 253's 46%), so 4b passes should be read against it —
U56's 87–96.5% is genuinely above base rate, and today's sibling result (idea 287's MA200-only book,
61.3% at k=55) is much closer to it. Second, the surviving explanation for the U56 pass is the
**identity of the curated 55-name list**, which is a hand-picked list of names that are large and
liquid *today* — exactly the kind of thing that will look good in a 2009-start backtest.

## 3. Rule 8 per draw (n chosen on ≤2016 by IS Sharpe inside each draw, 2017–2026 read once)

| d | k | IS picks | median OOS CAGR | median OOS Sharpe | median OOS MaxDD | median regret | beats SPY OOS | beats RULES v2 OOS | 4b rate of the pick |
|---|---|---|---|---|---|---|---|---|---|
| 5 | 50 | n=20 in 165/200, n=30 in 30, n=10 in 5 | 14.00% | 1.1869 | −18.05% | −0.069 | **100.0%** | **0.0%** | 91.5% |
| 10 | 45 | n=20 in 86/200, n=30 in 79, n=10 in 35 | 12.92% | 1.1975 | −17.38% | −0.057 | **99.5%** | **4.5%** | 55.5% |

The walk-forward is stable in the sense that matters least and unimpressive in the sense that
matters most: the IS chooser lands on the anchor n=20 most of the time and beats SPY out-of-sample
in ~100% of draws, but it **adds nothing over just fixing n=20** (median ΔOOS Sharpe +0.0000; better
than the anchor in only 15.0% / 39.0% of draws; mean +0.007 / −0.010) and it **loses to the live
RULES v2 book out-of-sample in 100% / 95.5% of draws**. Note the pick's own 4b rate (91.5% / 55.5%)
is *below* the anchor's (96.5% / 87.0%) — in-sample selection makes the candidate worse on the KEEP
path, not better.

## Verdict — **PARK, scoped to U56; not a new KEEP; 4a 0/800+**

The idea's own decision rule was "a KEEP that survives only one composition should be scoped or
shelved". The measurement splits that in two:

- **Scoped, not shelved, on composition.** The candidate survives every single-name removal and 87%
  of 10-name removals with wide margins on four of the five bars, so it is not fitted to particular
  members of universe.json.
- **Shelved as a general large-cap rule.** At matched pool size it passes 4b on 45–46% of random
  large-cap panels versus 87–97% of U56 subsets, and that residual is a property of the curated list
  rather than of the book. Any RULES wording for this candidate must name universe.json explicitly;
  it may not be described as a large-cap momentum rule.

It remains behind the live book on both paths (4a 0/800+, and it loses to RULES v2 OOS in ≥95.5% of
draws), so nothing here changes RULES. Recommended follow-ups for the queue: (i) publish the ~46%
4b base rate for random same-size large-cap panels as a REPORT-ONLY comparand, since a bar that an
arbitrary panel clears half the time is weak evidence; (ii) test whether U56's advantage survives
replacing its ETF sleeve, given that XBI/SMH/XLI are the most *helpful* removals.

**Survivorship caveat:** `universe.json` is a hand-curated list of names that are large and liquid
today and `universe_broad.json` is a list of current constituents; every panel here is a subset of
one of those, so all absolute levels are optimistic. Dropping names at random re-samples a survivor
list — it does **not** simulate delisting, so this run measures composition sensitivity, not
survivorship. The U56-vs-random contrast is measured on one common pool, which controls composition
but not the pool's own survivorship.
