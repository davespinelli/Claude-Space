# Idea 248 — is-LEAK-a-general-tax-on-every-published-per-armed-day-number (cloud, 2026-09-08)

**Verdict: ANSWERED / SPLIT. The queue's CONCLUSION generalises and hardens — the per-armed-day
verdict flips on 88.5% of the record's published claims and on 86.9% of 720 fresh arms — but
the queue's own MECHANISM is CORRECTED: LEAK is NOT the dominant term arm by arm. No RULES
change; one 4b KEEP-candidate by-product, PARK-recommended, memo written and not adopted.
`RULES.md`, `PROTOCOL.md`, `scan.py`, `bot.py` and `baseline.py` untouched.**

Script `2026-09-08_is-LEAK-a-general-tax-on-every-published-per-armed-day-number_cloud.py`
(deterministic, no network, ~7 min). Two tuned parameters, **all 48 grid points × 18 rungs
reported**: **P1** the arming rate `q ∈ {0.05, 0.10, 0.20, 0.35, 0.50, 0.65}` (6), **P2** the
instrument family, idea 246's published eight (8). Panels {u56, broad, small439}, books
{V1u, TOP20, EWall}, cost rungs {10, 25} bps and every setting inside an instrument (band 3%,
stops 15/25%, D=8%/k=0.5, vol 60%, m=0.50) are the project's published ones, held fixed and
never selected on. Idea 246's simulator is **imported, not re-implemented**.

---

## 1. The identity

    L(cond)   = c_on + ((1−f)/f)·c_off            per-armed-day loss of the CONDITIONAL arm
    L(always) = f·d_on + (1−f)·d_off              the always-on arm's unnormalised annual delta
    total = L(cond) − L(always) = CONC + ACT + LEAK
      CONC = (1−f)(d_on − d_off)     the instrument being dearer in its own regime  [idea 75]
      ACT  = c_on − d_on             the conditional arm acting differently ON armed days
      LEAK = ((1−f)/f)·c_off         its delta on days it is SUPPOSED to be inert, ×(1−f)/f

Checked to machine precision on both corpora: **max|residual| 7.02e-14** on the record's own
432 published claims, **2.84e-14** on the 720 fresh arms.

## 2. PART A — the census: the class is a SINGLETON FAMILY

| tier | files |
|---|---|
| **PUBLISHED-COLUMN** — a per-armed / per-active normalised column | 5, of which **2 are real** |
| NORMALISABLE — publishes an arming fraction AND a delta, so the statistic *could* have been quoted | **32** |
| DECOMPOSABLE — also publishes the ON/OFF split CONC/ACT/LEAK needs | **2** |
| PROSE claims ("per armed day" and variants) in committed `.md` / LEADERBOARD / CHANGELOG | 3 files, 7 mentions |

The 3 other PUBLISHED-COLUMN hits are lexicon false positives (`per_day_pct` is an event-study
day return; `col_perturb` is a column name), named and excluded rather than counted. **Every
per-armed-day number the record has ever published is idea 246's own** — 432 claims in two
CSVs, three prose mentions, three LEADERBOARD rows. The queue's "every published claim in the
record" is therefore a set of one family, and the interesting question is not the census but
whether the effect generalises off it, which is PART C.

Note the asymmetry: **32 files could have quoted the statistic and 2 can be decomposed.** The
column that makes a per-armed-day number auditable (the ON/OFF split of both the conditional
arm and its always-on sibling) is almost never published, which is the same
write-it-at-run-time-or-lose-it problem idea 445 and idea 457 found for ROOM/REGRET.

## 3. PART B — re-quoting idea 246's 432 published claims

Gate: recomputing CONC/ACT/LEAK from idea 246's own published columns reproduces its committed
values at **max|ΔCONC| 7.1e-15, max|ΔACT| 3.6e-15, max|ΔLEAK| 1.4e-14, max|Δtotal| 7.0e-14**,
and the regime medians match its memo exactly (spy200 −2.343 / 0.000 / −0.782 / −1.543).

| | claims | published verdict ("loses MORE per armed day") | survives dropping the normalisation | **FLIP** | survives netting LEAK out | **FLIP** |
|---|---|---|---|---|---|---|
| all | 432 | 374 (86.6%) | 43 | **331 (88.5%)** | 282 | **92 (24.6%)** |
| spy200 | 144 | 122 | | 104 | | 33 |
| breadth20 | 144 | 123 | | 110 | | 53 |
| hivol80 | 144 | 129 | | 117 | | 6 |

Flips by instrument run 36–46 of ~50 for the unnormalised restatement and 3–28 for the
LEAK-netted one; `gross50` is the extreme (46 of 46 and 28 of 46), `stop15` the mildest on the
LEAK netting (3 of 52) because its damage really is concentrated in its own regime.

**The two restatements are not interchangeable.** Dropping the normalisation flips 88.5% of
the published verdicts; netting LEAK out flips only 24.6%. LEAK is a large part of the number
but it is not the part that decides the sign — the `1/f` amplification of *all three* terms is.

## 4. PART C — the generalisation: make the ARMING RATE the dial

The regime is replaced by a breadth quantile whose level *is* the nominal arming rate, swept
over six levels × 8 instruments × 18 rungs = 864 arms.

**First, a coverage caution that is a result in its own right.** Nominal `q` and realised `f`
are not the same number: an expanding bottom-`q` breadth quantile with a 3-year warm-up fires
far below its nominal rate — `q=0.05` never fires at all on any panel (**144 of 864 arms are
DEGENERATE and are reported, never scored**), and `q=0.10` realises f = 0.014–0.025. Any
result that quotes a nominal threshold as if it were an arming rate is overstating coverage.

720 scoreable arms. Pooled medians:

| q | f (realised) | (1−f)/f | total | CONC | ACT | LEAK | unnormalised |
|---|---|---|---|---|---|---|---|
| 0.10 | 0.025 | 38.6 | **−9.172** | +13.757 | −10.238 | −11.240 | **+1.296** |
| 0.20 | 0.087 | 10.6 | **−3.358** | +0.806 | −1.124 | −2.919 | **+0.986** |
| 0.35 | 0.234 | 3.28 | **−1.243** | +0.283 | −0.527 | −1.205 | **+0.582** |
| 0.50 | 0.420 | 1.38 | **−0.589** | +0.337 | −0.205 | −0.464 | **+0.408** |
| 0.65 | 0.604 | 0.66 | **−0.188** | +0.300 | −0.053 | −0.238 | **+0.403** |

**The sign reversal is a property of the statistic at EVERY arming rate**, not of idea 246's
three regimes: `total` is negative at all six q levels and the unnormalised delta is positive
at all six. Sign tests over the 720 arms: **579/720 negative normalised (p 7.98e-64)** against
**81/720 negative unnormalised (p 1.85e-108)** — the same comparison, opposite answers, both
overwhelming.

| | of 720 arms |
|---|---|
| published-style verdict true | 579 (80.4%) |
| **FLIPS when the normalisation is dropped** | **503 (86.9%)** |
| **FLIPS when LEAK is netted out** | **270 (46.6%)** |

Flip rates are stable across the whole arming range (86/103 to 110/123 for the unnormalised
restatement), so this is not a small-f corner effect.

### The correction to idea 246's headline

Idea 246 reported LEAK as **52%** of the median total against CONC's **13%**. That is a
*ratio of medians*. Per arm it does not hold:

| q | median share of \|CONC\| | \|ACT\| | \|LEAK\| | arms where \|LEAK\| is the largest term |
|---|---|---|---|---|
| 0.10 | 0.427 | 0.336 | 0.203 | 32/144 |
| 0.20 | 0.416 | 0.280 | 0.302 | 50/144 |
| 0.35 | 0.411 | 0.266 | 0.326 | 53/144 |
| 0.50 | 0.472 | 0.255 | 0.270 | 35/144 |
| 0.65 | 0.501 | 0.139 | 0.285 | 39/144 |

**Median per-arm shares: CONC 44.4%, LEAK 26.9%, ACT 25.1%. `|LEAK|` is the largest of the
three terms in only 209 of 720 arms (29.0%).** And LEAK is not uniquely a function of the
arming lever — Spearman((1−f)/f, |term|) is **+0.439 for LEAK, +0.494 for CONC, +0.408 for
ACT, +0.554 for the total**. Every term inflates as f shrinks, because they all carry a
(1−f) or (1−f)/f factor.

**So: is LEAK a general tax? Yes as an amplified residue — it is present, it grows as arming
gets rarer, and on the record's own published claims it flips a quarter of the verdicts. No as
the queue frames it — it is not the dominant term arm by arm, and it is not what reverses the
sign. The per-armed-day statistic is unsafe because of the `1/f` normalisation itself, of which
LEAK is one of three amplified parts.** PROTOCOL's remedy should be to require the
unnormalised delta beside any per-armed-day number, not merely a LEAK column.

## 5. PART D — rule 8 and both KEEP paths

`(instrument, q)` chosen on IS ≤ 2016-12-31 by IS Sharpe alone, 2017-2026 read once, t+1
execution, 10 bps anchor and 25 bps rung.

| | of 18 (panel × book × cost) cells |
|---|---|
| IS pick beats its own control OOS | **5/18** |
| IS pick beats SPY OOS | 7/18 |
| IS pick beats RULES v2 OOS | 5/18 |
| mean OOS regret vs the in-cell oracle | **+0.1075** |

Median OOS Sharpe of the pick **0.627** against its own do-nothing control's **0.760** — the
chooser is a net destroyer of Sharpe. **As a selectable rule this is a KILL.**

**BOTH KEEP PATHS over all 882 rows: 4a vs the live RULES v2 book 0/882; 4a vs RULES v1
(idea 246's own comparand, kept for continuity) 275/882; 4b 94/882** — 65 on u56, 29 on broad,
**0 on small439**, and **0 of the 18 do-nothing controls passes 4b**, so the overlay is doing
the work where it passes.

## 6. The by-product: one 4b KEEP-candidate, PARK-recommended

The rule-8 pick on u56/EWall is `vol60-dg` armed at `q=0.20`, and it clears 4b at both cost
rungs — a candidate chosen in-sample and read once out of sample, so it is rule-8 clean.

| book | CAGR | Sharpe | MaxDD | H1 / H2 | OOS CAGR | OOS Sharpe | OOS MaxDD |
|---|---|---|---|---|---|---|---|
| **pick, u56/EWall/vol60-dg@q0.20, 10 bps** | **12.85%** | **1.158** | **−18.1%** | 1.199 / 1.119 | 13.00% | **1.193** | −18.1% |
| same, 25 bps | 12.67% | 1.144 | −18.1% | 1.187 / 1.102 | 12.79% | 1.176 | −18.1% |
| its own un-overlaid control | 13.27% | 1.124 | −22.5% | 1.190 / 1.072 | 13.82% | 1.136 | −22.5% |
| SPY | 15.23% | 0.889 | −33.7% | — | 15.45% | 0.882 | −33.7% |
| RULES v2 (live) | — | — | — | — | — | 1.285 | — |

4b bars on u56: DD cap 20.23%, CAGR floor 10.66% — the control **fails on drawdown** (−22.5%)
and the overlay buys the pass by cutting MaxDD 4.4 pp for 0.4 pp of CAGR.

**Recommended PARK, not KEEP, for three stated reasons:** (i) the arming coverage is
asymmetric — f is **0.031 in-sample against 0.132 out-of-sample**, the same defect that PARKed
idea 247's arm; (ii) it fails 4a against the live RULES v2 book *and* against v1, and loses to
RULES v2 on OOS Sharpe (1.193 vs 1.285); (iii) the selector that found it is a net Sharpe
destroyer over the other 17 cells, so this cell is the good draw from a bad chooser.
Memo: `..._cloud.memo.md`.
