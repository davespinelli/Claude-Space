# Idea 815 — is the CORR-LO POSITIVE EXCESS a DE-GROSSING artefact? (lane C, 2026-09-15)

**ANSWERED = NO, AND THE QUEUE'S DIAGNOSIS IS INVERTED.** The BLOCK circular shift is not
manufacturing CORR-LO's excess. It is manufacturing the excess of the four **prior-direction**
families — the ones idea 606 read as the generalising result — and it is *understating* CORR-LO.
**KILL for capital**: the CORR-LO book passes 4b at **0 of 1,152** cells at the protocol rung and
4a at **0**, and its 36 rule-8 picks pass neither path. No RULES change, no book promoted, no KEEP
claimed; RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py untouched (rule 6). **One PROTOCOL
line is PROPOSED, NOT APPLIED.**

Script `research/backtests/2026-09-15_is-the-CORR-LO-POSITIVE-EXCESS-a-DE-GROSSING-artefact_C.py`

## What was run

Idea 606's machinery held **completely fixed** — same book (EWALL: every name above its 200d with
`vol20 < 0.60`, equal weight at `gross/n`), same gate (de-gross to `1-depth` on the state's bad
tail, cash never re-spread, switch cost on `|dm|`), same arms, same firing rates, same
twin-cancelling differenced statistic — and **only the NULL changed**.

Tuned parameters (2), exactly the pair the queue names:

1. **state** — BREADTH / VOL20 / DISP / CORR, each in **both** directions (8 families). Direction
   is not a third parameter: both are always reported, never selected on.
2. **placebo kind** — a 2 × 3 factorial, CLUSTERING {iid, circular shift} × CALENDAR STRATA
   {none, calendar year, episode}: `RAND` / `YEARMATCH` / `EPMATCH` / `BLOCK` / **`BLOCKYEAR`** /
   **`BLOCKEP`**, of which idea 606 had only `RAND` and `BLOCK`; plus the displacement ladder
   `SHIFT5/10/21/63/126/252`, each run as a **LAG** (+s) and a **LEAD** (−s). 12 kinds.

`BLOCKYEAR` and `BLOCKEP` are the objects idea 606 did not have: a circular shift **within** each
calendar year, and within each of {COVID_TIGHT, BEAR2022, everything else}. They preserve the
arm's firing count per stratum **and** its run-length distribution, so an excess that survives them
is neither a calendar artefact nor a clustering artefact. `YEARMATCH`/`EPMATCH` are their iid
counterparts, reported so the two channels are read apart instead of confounded.

Reported axes, never tuned: level q 0.07/0.12/0.17 · w 252/504/1008/2016 · depth 0.25/0.50/1.00 ·
cadence D/W · gross 0.75/1.00 · cost 0/10/25 bps · panel U56 / B136 / SMALL663. Episodes declared
in advance and never swept: COVID_TIGHT 2020-02-19..2020-04-07, BEAR2022 2022-01-04..2022-10-12
(5.18–5.84% of each evaluation window). **10,368 gated cells; 248,832 placebo cells**, every grid
point published.

## Reproduction gates — G1, G2, G4, G5, G5b, G6, G7 PASS; G3 passes on the unchanged cache and on the published object, and its miss is MEASURED

| | gate | result |
|---|---|---|
| G1 | cost rung `r(c) = r(0) − turnover·c/1e4` vs `engine.backtest(cost_bps=10)` | **0.000e+00** all three panels |
| G2 | idea 84's ungated EWALL U56 g=0.85 @10bps (target 11.8% / 1.05 / −17.9% / H 1.07 / 1.04) | 11.74% / 1.045 / −17.89% / H 1.074 / 1.022 |
| G3a | idea 606's **committed** `.excess.csv`, per arm, on **B136 — the one panel whose cache is unchanged** | **2.671e-16** (1,152 arms) |
| G3b | firing-day-share drift vs 606's committed `on_share` | B136 **9.7e-17**, SMALL663 **9.7e-17**, U56 **8.667e-04** |
| G3c | the **published object**: 606's eight per-family medians and share>0, all panels pooled, bar 0.005 declared before the run | max **0.0046** (CORR-LO **+0.0271 / 0.8495** vs its committed **+0.0270 / 0.8449**) |
| G4 | the fast numpy CAGR / Sharpe / MaxDD used on 249k cells vs `engine.metrics()` | **0.000e+00** |
| G5 | placebo matching identity, 41,472 arm × kind checks (de-grossed day count and mean multiplier — this is what cancels the twin) | **0.000e+00**, every kind |
| G5b | the two episode-stratified kinds reproduce the arm's firing-day count **inside** the episodes | **0.000e+00** |
| G6 | comparands are the record's | U56 RULES v2 8.62% / 1.2013 / −12.05%; B136 7.98% / 1.0993 / −12.24%; SPY 15.13–15.16% / 0.8845–0.8861 / −33.72% |
| G7 | deleting an EMPTY day set is bit-identical | **0.000e+00** |

**G3's one miss is a finding, not an excuse.** Per-arm reproduction of idea 606 is exact on B136
(2.7e-16) and at float level on SMALL663 (1.7e-08, identical firing days), and misses on U56
(2.5e-02). The cause is measured, not asserted: `data/prices.csv` has been **re-adjusted** since
2026-09-12 — it now ends 2026-09-14 against the other caches' 2026-09-11, and U56's committed
firing-day share moves by up to **8.667e-04** (≈4 of 4,443 days), while B136's and SMALL663's move
by 1e-16. **The committed price caches are not frozen, so a U56 per-arm result published on one day
is not per-arm reproducible on another.** Truncating U56 back to 2026-09-11 does not recover it
(4.4e-02), which is what says the values were restated and not merely extended.

## Q4 — the queue's premise is FACTUALLY FALSE, and this is the whole answer

The queue's hypothesis (A) assumes "a calendar alignment (2020, 2022) that **both tails share**".
Measured directly — the share of an arm's de-grossed days that falls inside the two episodes:

| family | REAL | BLOCK placebo | REAL − BLOCK |
|---|---|---|---|
| BREADTH-LO | **0.2755** | 0.0497 | **+0.2258** |
| CORR-HI | **0.2335** | 0.0549 | **+0.1786** |
| VOL20-HI | 0.1659 | 0.0526 | +0.1133 |
| DISP-HI | 0.1349 | 0.0523 | +0.0826 |
| CORR-LO | **0.0000** | 0.0532 | **−0.0532** |
| BREADTH-HI / VOL20-LO / DISP-LO | **0.0000** | ~0.053 | ~−0.053 |

The two tails are **calendar-disjoint, not aligned.** CORR-HI's *least* episode-loaded arm still
spends 11.6% of its firing days in the episodes; **87.5% of CORR-LO's 432 arms spend exactly zero**
and the maximum over all of them is 1.39%. So the mechanism hypothesis (A) proposes cannot be the
one producing CORR-LO's excess — it is the one producing **CORR-HI's**, and BREADTH-LO's.

## Q1 — the answer, against a null that preserves the calendar AND the clustering

Median excess (real arm Sharpe − placebo Sharpe), 432 arms per family per kind, three panels
pooled; share of arms beating their own placebo and an exact two-sided sign-test p beside it.

| family | | BLOCK (606's) | **BLOCKYEAR** | **BLOCKEP** |
|---|---|---|---|---|
| BREADTH-LO | prior | **+0.0735** (0.981, 5e−114) | +0.0182 (0.748) | **−0.0172** (0.343, 6e−11) |
| CORR-HI | prior | **+0.0415** (0.861, 5e−56) | +0.0176 (0.664) | **−0.0207** (0.315, 1e−14) |
| DISP-HI | prior | **+0.0287** (0.792) | +0.0031 (0.556, p 0.024) | **−0.0320** (0.141, 3e−55) |
| VOL20-HI | prior | **+0.0210** (0.722) | **−0.0143** (0.343) | **−0.0427** (0.164, 8e−48) |
| **CORR-LO** | reversed | +0.0271 (0.850) | **+0.0513** (0.956) | **+0.0468** (0.965, **4e−103**) |
| BREADTH-HI | reversed | +0.0099 (0.634) | **+0.0353** (0.877) | **+0.0220** (0.764) |
| VOL20-LO | reversed | −0.0137 (0.361) | +0.0053 (0.593) | +0.0003 (0.502, **p 0.96**) |
| DISP-LO | reversed | −0.0202 (0.162) | −0.0049 (0.352) | −0.0096 (0.278) |

**Every prior-direction family collapses; three of the four go NEGATIVE.** Holding the calendar and
the run lengths fixed, a randomly re-timed VOL20-HI gate *beats* the real one by 0.0427 Sharpe at
share 0.164. **CORR-LO goes the other way: +0.0271 → +0.0468, share 0.850 → 0.965.** The direction
of the whole result reverses when the null is fixed.

## Q2 — the shape test, and the sharpest single number in the run

Excess against a circular shift of **exactly** s days. Spearman(|s|, median excess) — reading (A)
predicts strongly positive, (B) predicts ~0 or negative:

BREADTH-LO **+1.000** · VOL20-HI +0.771 · CORR-HI +0.714 · DISP-HI +0.714 ·
**CORR-LO −0.600** · BREADTH-HI −0.943 · VOL20-LO −0.771 · DISP-LO −0.771.

Split by direction, the **LEAD** leg (fire s days *earlier*) is decisive:

| family | LEAD 5 | LEAD 10 | LEAD 21 | LEAD 252 |
|---|---|---|---|---|
| BREADTH-LO | **−0.2049** | −0.1774 | −0.1429 | +0.0903 |
| VOL20-HI | −0.0862 | −0.1660 | **−0.2110** | +0.0524 |
| CORR-HI | −0.1101 | −0.1824 | −0.1846 | +0.0692 |
| **CORR-LO** | **+0.0980** | +0.1154 | **+0.1824** | +0.0427 |

Moving BREADTH-LO's gate five days earlier is worth **+0.20 Sharpe** over the gate itself. The
prior-direction gates are not carrying information about the drawdown; they are arriving late to an
episode whose *dates* are doing the work, and BLOCK scores them well only because a uniform shift
moves the null off those dates entirely.

## Q3 — episode deletion

BLOCK excess re-read with COVID_TIGHT and BEAR2022 removed from the return stream, as a share of
the full-sample excess: BREADTH-LO **0.170**, CORR-HI **−0.510**, DISP-HI **−0.318**, VOL20-HI
**−1.253** — against **CORR-LO +1.671** and BREADTH-HI +1.648. Same split, third method.

## Q5 — rule 8 on the claim

CORR-LO is the only family whose IS excess forecasts its own OOS excess: Spearman(IS, OOS) per arm
**+0.479 / +0.549** under BLOCKYEAR / BLOCKEP, against ≤ +0.238 for every other family and
**negative** in four of eight. Its OOS excess (**+0.0562 / +0.0457**) is at least its IS excess
(+0.0405 / +0.0410), whereas the prior families' BLOCKEP excess is negative in both windows. The
*claim* passes rule 8 where 606's did not. **The book does not — see below.**

## Q6 — rule 8 on the books: KILL

4b passes **1,704 of 10,368** cells (371 at the protocol rung); 4a passes **11 of 10,368** (1 at the
protocol rung). By family at 10 bps: CORR-HI 133, BREADTH-LO 113, VOL20-HI 63, BREADTH-HI 42,
DISP-HI 20, **CORR-LO 0, VOL20-LO 0, DISP-LO 0** (CORR-LO reaches 116 at 0 bps and 0 at 25).

The rule-8 chooser — (level, w) fitted on IS Sharpe 2009–2016 per panel × family × depth × cadence
× gross × rung, 864 picks, OOS read once:

| family | 4b full | 4b OOS | 4a full | OOS CAGR | OOS Sharpe | OOS MaxDD |
|---|---|---|---|---|---|---|
| CORR-HI | 0.370 | 0.370 | 0.037 | 10.18% | 1.0043 | −18.48% |
| BREADTH-LO | 0.324 | 0.352 | 0.028 | 10.30% | 1.0604 | −19.05% |
| VOL20-HI | 0.222 | 0.250 | 0.000 | 9.87% | 0.9708 | −20.45% |
| **CORR-LO** | **0.102** | **0.065** | **0.000** | **9.17%** | **0.8690** | **−21.94%** |
| DISP-LO | 0.083 | 0.074 | 0.000 | 9.22% | 0.8293 | −21.94% |

Comparands, OOS window: SPY U56 15.27% / **0.8740** / −33.72%; RULES v2 U56 9.46% / **1.2772** /
−12.05%; B136 7.88% / 1.1059 / −12.24%. Across all 864 picks, 71 beat RULES v2's OOS Sharpe and
475 beat SPY's, but only 327 clear 70% of SPY's OOS CAGR; SMALL663 contributes **0 of 288** on both
SPY legs.

**The best CORR-LO book in the grid** (U56, q0.07 w1008 depth 0.50 W g0.75, 10 bps — reported, not
selected on): **10.20% / 1.0504 / −15.87%** (H 1.0775 / 1.0288), OOS **10.93% / 1.1017 / −15.87%**.
It beats SPY's Sharpe in both halves and out of sample and clears the DD cap — and **misses 4b on
the CAGR floor by 0.39 pp** (10.20% against 10.59% required). Not a candidate; 0 of 36 CORR-LO
rule-8 picks pass either path.

**The one 4a pass at the protocol rung is reported and NOT claimed:** B136 CORR-HI q0.17 w504
depth 1.00 W g0.75 — 10.44% / **1.1947** / −10.36% (H **1.2499 / 1.1370**) against B136 RULES v2
7.98% / 1.0993 / −12.24% (H 1.2348 / 0.9658). It **fails rule 8**: the IS chooser for its own group
picks q0.12 w252, which is not a 4a pass. It is 1 of 3,456 head-rung cells, it is post-hoc from a
grid built for another question, and this run's own headline says CORR-HI's excess over a
calendar-preserving null is **negative**.

## The PROTOCOL line this proposes (rule 6 — PROPOSED, NOT APPLIED)

> Any claim differenced against a rate-matched placebo must publish the excess against a null that
> preserves **both** the firing calendar and the run-length distribution (a circular shift **within**
> declared strata), not only against an unstratified shift. An unstratified shift scores a gate for
> *when the episodes are*, which is not information the gate supplies.

Cost of adopting it, measured here: it reverses the sign of the record's generalising result on
**3 of 4** prior-direction families and leaves the one family 606 flagged as anomalous standing.

## Caveats

1. **Survivorship.** All three panels are current-constituent lists, so CAGR and drawdown levels
   are optimistic, the SPY bars included. Correlation measured on a survivor panel is itself
   optimistic. The placebo *differencing* and the null-vs-null contrast are the durable part.
2. **Two episodes.** The episode strata are two declared windows. BLOCKYEAR does not depend on that
   choice and agrees with BLOCKEP on every family, which is the check that the answer is not the
   episode definition.
3. **The claim passes rule 8; the book does not.** Nothing here makes CORR-LO tradeable. The
   surviving statement is about what the record's placebo leg measures, not about a book.
4. **G3's U56 miss** (§ gates). U56 per-arm figures published before 2026-09-15 cannot be
   reproduced from the current cache.
5. **CORR-LO's excess is measured where it never de-grosses during a crash.** Its books therefore
   carry the full episode drawdown, which is exactly why they fail the 4b DD and CAGR legs.

## Files

`.cells.csv` (10,368) · `.excess.csv.gz` (arm × kind) · `.placebo.csv.gz` (248,832) ·
`.walkforward.csv` (864 rule-8 picks) · `.ladder.csv` · `.overlap.csv` · `.claim.csv` ·
`.gates.csv` · `.g5.csv.gz` · `.console.txt`
