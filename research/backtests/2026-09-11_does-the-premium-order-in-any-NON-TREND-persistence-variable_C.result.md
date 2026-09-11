# Idea 798 — does-the-MA-gate-premium-order-in-ANY-persistence-variable-that-is-NOT-a-TREND-statistic (lane C, 2026-09-11)

**Script:** `2026-09-11_does-the-premium-order-in-any-NON-TREND-persistence-variable_C.py`
**Verdict: ANSWERED — NO. The ladder is a TREND-STATISTIC fact, not a persistence fact.
KILL for capital (4a 12 / 4b 42 / BOTH 0 of 3,888 books).**

## Selection

Lane C's rule is "claim the SECOND open idea". That is **797**
(*which-committed-LADDER-claims-in-the-record-pass-a-REQUIRED-SIGN-test-they-never-took*), a
prose/AST census of the record's committed ladder claims with **no price leg**, so it cannot
carry this run's mandatory rule-8 walk-forward in a sandbox with no network. It is annotated
**SKIP** in QUEUE.md and stays OPEN for a LOCAL/Actions run, exactly as ideas 780/781/777/713
were handled. Lane C took the next eligible idea, **798**, which is price-only and runs here.

## The question

Idea 569 found `tpers` (1 − daily flip rate of the name's own above-200d-MA state) orders the
MA-gate SELECTION premium monotonically on kernel-matched k=36 draws (POOL slope +33.381187,
R2 0.847210, slope·span +0.707607 = 7.24x the published GAP). Idea 571 (lane B, yesterday)
showed the R2 **survives off-gate** on three non-gate persistence variables (mompers 0.7105,
momsgn 0.7943, momac 0.7765 = 0.84–0.94x tpers's) and read that as *"the premium rising with
persistence is a property of persistence in general"*. But all four of those variables are
**trend statistics** — persistence of a 200d-MA state or of a 12-1 momentum state. The queue
asked: run the same draws on persistence variables with **no trend content** and report whether
the slope survives.

| variable | what it is | trend content? |
|---|---|---|
| `tpers` | 1 − flip rate of `px > 200d MA` | **YES** (REFERENCE, idea 569's winner) |
| `retsgn` | 1 − flip rate of `daily return > 0` — sign persistence of daily returns | none |
| `volpers` | 1 − flip rate of `vol20 > its own trailing 252d median` — vol-regime state persistence | none (second moment) |
| `retac` | lag-1 autocorrelation of **daily** returns (continuous form) | none |

**Volume-rank persistence** (the queue's third named variable) is **NOT RUNNABLE here and is
reported as such, not silently dropped:** `baseline.load_volume` serves the SMALL panel only, so
the B136 half of the pool has no volume cache and the characteristic cannot be defined on the
pooled name set the draws are built from. Parked idea 429 (LOCAL/Actions) builds that cache.

Machinery is idea 569/571's, verbatim: pool = 134 B136 + 439 SMALL tradables on the common
index (573 names, 2010-01-04..2026-09-04), k=36 kernel draws (h = 0.5·sd, 6 seeds), pre-registered
10/30/50/70/90th-percentile rungs, flavours POOL/BONLY/SONLY, gross {0.50,0.75,1.00} × cadence
{W,M} reported and averaged, 10 bps, t+1 fills. Tuned parameters: exactly two — the **SIGNAL**
and the **LEVEL**. 324 draws × 2 arms × 3 gross × 2 cadence = **3,888 books, every grid point in
`.grid.csv`**.

## Gates

- **G1 PASS** — idea 569's committed `tpers` ladder reproduces **bit-for-bit**: 13/13 rungs, max
  |Δ| over (achieved, premium, sd, slope, R2, span, effect) = **1.11e-16**; POOL slope
  +33.381187, R2 0.847210, effect +0.707607 to <1e-6 of the pre-registered values.
- **G2 PASS** — `fast_backtest` == `engine.backtest`, max |Δreturn| **1.39e-17**.
- **G3 PASS** — idea 569's committed tpers matched-level B−S origin gaps, 3/3, max |Δ| **8.33e-17**.
- **G4 PASS** — the three new variables really are trend-free: |Spearman vs `mompers`| ≤ **0.1709**
  (retsgn +0.1122, volpers +0.0901, retac +0.1709), and independent of tpers as well
  (+0.2110 / +0.1916 / +0.1635, bar 0.50). **They fail below, and not because they are copies of
  anything — that is what makes the failure informative.**

## Result — the slope does NOT survive. R2 falls by 13x–235x.

POOL fits (premium vs the draw's achieved characteristic; required sign fixed in advance by the
three real panels' own values of each characteristic, computed before any premium is read):

| char | trend? | slope | R2 | R2 / tpers | slope·span | /GAP | monotone | signOK | H_INFO |
|---|---|---|---|---|---|---|---|---|---|
| tpers | **TREND** | +33.3812 | **0.8472** | 1.000 | +0.7076 | 7.24 | up | True | **True** |
| retsgn | free | +0.7334 | **0.0036** | 0.004 | +0.0191 | 0.19 | — | False | False |
| volpers | free | +6.9269 | **0.0638** | 0.075 | +0.0852 | 0.87 | — | True | False |
| retac | free | −0.2784 | **0.0046** | 0.005 | −0.0270 | 0.28 | — | True | False |

Put beside idea 571's trend-persistence variables, the separation is the whole result:

- trend persistence (idea 571): R2 **0.7105 / 0.7943 / 0.7765** = 0.84–0.94x tpers's;
- trend-free persistence (here): R2 **0.0036 / 0.0638 / 0.0046** = **0.4%–7.5%** of tpers's.

Not one trend-free variable is monotone on POOL, not one clears the effect bar (0.5·GAP =
0.0489 — volpers comes closest at 0.0852, but its |effect| 0.0852 is **below** its own
within-rung seed sd 0.1091, so H_NOISE fails too), and `retsgn` gets the required sign wrong.
**H_TRENDFREE FAILS. H_TREND PASSES.**

So idea 571's Result 1 has to be narrowed: the ladder is not "persistence in general". Everything
that orders the MA-gate premium on this machinery is a **trend statistic** — the gate's own 200d
state or a 12-1 momentum state. Persistence of the daily return sign, of the vol regime, and the
lag-1 return autocorrelation are all genuinely persistent, genuinely independent of tpers, and
carry **no ordering at all**.

## H_CARRIER — still False for everything, but one number is a lead

| char | rungs inside seed sd | mean B−S | mean \|B−S\| | mean \|match resid\| |
|---|---|---|---|---|
| tpers | 0/3 | +0.1204 (0.61x idea 568) | 0.1204 | 0.0017 |
| retsgn | 2/3 | +0.0823 (0.42x) | 0.0823 | 0.0022 |
| volpers | 3/4 | +0.0655 (0.33x) | **0.0655** | **0.0007** |
| retac | 1/4 | +0.0961 (0.49x) | 0.0961 | 0.0077 |

No variable passes (every rung must be inside the floor). `volpers` is the **tightest-matched**
reading on this machinery to date — match residual **0.0007**, 2.4x tighter than tpers's and 22x
tighter than idea 571's `momac` (0.0152) — and its mean |B−S| is 0.0655 = 0.33x idea 568 against
momac's 0.0549 at a far looser match. That bears directly on **idea 796** (is momac's 0.0549 real
or a matching residual): a variable that matches 22x tighter lands at a *larger* gap, which is
evidence for the residual reading. Reported as a lead, not a result.

## RULE 8 walk-forward (required)

**WF-A** — every slope refit inside 2010-2016 and again in 2017-2026, read once. Sign holds
**9/12** (char, flavour) cells; all three failures are trend-free variables (retsgn POOL, retac
BONLY, retac SONLY); tpers holds 3/3. POOL R2:

| window | tpers | retsgn | volpers | retac |
|---|---|---|---|---|
| IS 2010-2016 | **0.518** | 0.169 | 0.124 | 0.001 |
| OOS 2017-2026 | **0.758** | 0.025 | 0.009 | 0.002 |

The trend variable has the highest POOL R2 in **both** windows, and the trend-free ones decay
toward zero out of sample instead of strengthening.

**WF-B** — (char, level) picked by **IS Sharpe alone** at g=0.75/W POOL, OOS read once. The pick
is `tpers L=0.9780` (IS +0.9447) — the trend variable wins the selection too, and it was also the
OOS winner (+1.0517). It is the same book idea 571's WF-B selected, so the numbers below
reproduce that row exactly:

| book | CAGR | Sharpe | MaxDD | H1 / H2 | OOS CAGR | OOS Sharpe | OOS MaxDD |
|---|---|---|---|---|---|---|---|
| WF-B pick (seed-pooled) | 14.53% | 1.134 | −23.56% | 1.260 / 1.058 | 16.51% | 1.194 | −23.56% |
| RULES v2 (B136) baseline | 7.62% | 1.082 | −12.24% | 1.126 / 1.040 | 7.98% | 1.119 | −12.24% |
| SPY | 14.13% | 0.862 | −33.72% | 0.891 / 0.858 | 15.45% | 0.882 | −33.72% |

- **4a FALSE** — out-Sharpes RULES v2 in both halves (1.260>1.126, 1.058>1.040) but MaxDD
  −23.56% vs −12.24%: the MaxDD leg binds.
- **4b FAILS on DD only** — H1, H2, OOS and CAGR all clear SPY; MaxDD −23.56% vs the cap
  0.60 × −33.72% = **−20.23%**, missed by 3.3pp.
- Over all 3,888 books: **4a 12, 4b 42, BOTH 0**. Binding 4b legs: DD 3383, H2 2884, OOS 2813,
  H1 2325, CAGR 2180. 4b passers by char: retac 20, volpers 14, tpers 6, retsgn 2 — and 38 of 42
  are MA-RS, 20 of 42 are `retac`-BONLY draws, i.e. the 4b passers track **which names got drawn**
  (B-sourced, large-cap) rather than the characteristic. A kernel draw is not a tradable rule.

**No KEEP candidate, so no RULES wording is proposed.** RULES.md, PROTOCOL.md, scan.py, bot.py
and baseline.py untouched.

## Caveats

Survivorship: B136 and the small panel are CURRENT constituents; every number is a statement
about surviving names, not a tradable 2010 universe. The pool is ffilled, so a stale name has runs
of exact-zero returns that would read as persistence on `retsgn`/`retac` — measured and reported:
|Spearman(char, zero-return share)| ≤ **0.1035** across all four variables (mean zero share 2.93%),
so the contamination is not driving the null. `volpers` uses a trailing 252d median (causal), not
a full-sample level. 2010-01-04..2026-09-04, one common index; only 2020 and 2022 are real stress
tests in it. One negative result on one machinery: this says trend-free persistence does not order
**this** premium on **these** draws, not that no trend-free variable ever could.
