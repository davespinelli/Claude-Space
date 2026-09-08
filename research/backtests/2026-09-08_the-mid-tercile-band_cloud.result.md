# Idea 456 — is the MID-TERCILE peak a real shape or a menu-size artefact? (cloud, 2026-09-08)

**SPLIT. The queue's suspected culprit is EXONERATED and a different one is convicted; the
rule the peak was supposed to license is KILLED.** No RULES change, no KEEP, no memo;
`RULES.md`, `scan.py`, `bot.py`, `baseline.py` and `PROTOCOL.md` untouched.

- The mid-tercile peak is **NOT a menu-size artefact.** It survives conditioning on |A| and on
  the ladder's own IS spread (within-|A| demeaned: mid **+0.0142**, t +3.4).
- It **IS a between-FILE composition artefact.** Demean the payoff inside each parent file and
  the peak is gone: narrow +0.0050, mid **−0.0025**, wide −0.0026, every |t| < 1.4.
- The **BAND rule is KILLED by rule 8**, exactly where the threshold rule was: it wins in
  sample (+0.0173 vs +0.0152) and transfers worse (date split OOS **−0.0155** vs −0.0014;
  it beats the threshold family in **3 of 20** seeded file splits, and always-abstain in 2/20).

## Gates (passed before any new number was read)

| gate | result |
|---|---|
| G1 exact reproduction of the parent's tercile table off its committed `.census.csv` | raw +0.0093 / **+0.0242** / −0.0072, ρ −0.0236, n **1,203** over 43 files — max abs diff vs `_B.sorting.csv` **7.6e-17** (z and rng likewise) |
| G2 cost-rung identity `net(c) = gross − TO·c/1e4` | max abs diff **0.000e+00** |
| G3 fresh re-harvest of the whole committed record (1,916 CSVs) | 93 admitted, 11,560 census rows, **1,207** MOVED Sharpe cells over 44 files — every table below is quoted on BOTH corpora and they agree to the third decimal |

t-STAT CAVEAT, stated once: cells inside one file share an arm ladder, so instance-pooled t's
are inflated. Every headline is given instance-pooled **and** file-clustered.

## A. The conditioning the queue asked for

The confound is real but points the wrong way. Spearman(|A|, margin) **−0.281**,
Spearman(|A|, gain) **+0.287** — bigger menus have thinner top-2 gaps *and* pay more to
abstain, which is exactly the machinery that would manufacture a spurious narrow-tercile
result. It does not manufacture the *mid* peak.

Within each menu-size stratum the shape is a **different shape in every stratum**, and only
the widest one is a mid peak:

| \|A\| | n | narrow | mid | wide | ρ | shape |
|---|---|---|---|---|---|---|
| 3–4 | 323 | −0.0178 | −0.0401 | **−0.1172** | −0.644 | monotone-down |
| 5–6 | 96 | +0.0140 | +0.0083 | +0.0291 | +0.066 | mid-trough |
| 7–10 | 164 | +0.0210 | +0.0329 | +0.0378 | +0.167 | monotone-up |
| 11–16 | 168 | +0.0715 | +0.0292 | +0.0982 | +0.369 | mid-trough |
| 17+ | 452 | −0.0210 | **+0.0624** | +0.0365 | +0.370 | MID-PEAK |

The IS-spread strata do the same thing (mid-trough / mid-peak / monotone-down as sd rises).
**The pooled curve is a mixture of five shapes whose ρ ranges from −0.64 to +0.37**, which is
the honest reason the pooled ρ is ~0: it is not a weak signal, it is cancellation.

The decisive test — demean `gain` inside a stratum and re-rank the margin inside it:

| demeaned within | narrow | mid | wide | shape |
|---|---|---|---|---|
| \|A\| bin | −0.0085 (t −2.0) | **+0.0142 (t +3.4)** | −0.0054 (t −1.3) | MID-PEAK survives |
| IS-sd tercile | +0.0033 (t +0.7) | **+0.0092 (t +2.4)** | −0.0125 (t −2.2) | MID-PEAK survives |
| **FILE** | +0.0050 (t +1.3) | **−0.0025 (t −0.8)** | −0.0026 (t −0.6) | **peak GONE** |
| FILE × \|A\| | +0.0036 (t +1.0) | +0.0017 (t +0.5) | −0.0053 (t −1.4) | **peak GONE** |

So the peak is neither menu size nor ladder spread: it is **which experiment the cell came
from**. Within one grid's own ladder the margin buys nothing at any part of its range.

## B. The band rule, all 55 grid points (norm = raw; z and rng reported as labelled sensitivity)

D = mean[OOS Sharpe(rule) − OOS Sharpe(argmax)]; abstain iff `qlo < F(margin) ≤ qhi`.

| family | best edges | D (pooled) | D (file-clustered) | abstains |
|---|---|---|---|---|
| THRESHOLD (qlo = 0, the parent's killed rule) | (0.0, 0.8) | +0.0152 (t +6.7) | +0.0334 (t +2.8) | 80.0% |
| **BAND** | **(0.2, 0.8)** | **+0.0173 (t +8.7)** | **+0.0411 (t +4.7)** | 60.0% |
| ALWAYS-ABSTAIN | (0.0, 1.0) | +0.0088 (t +3.2) | +0.0354 (t +2.9) | 100% |

The band does buy the parent's shape in sample, on both corpora and all three margin scales —
which is what one extra degree of freedom is for. Note the fitted band's own edges: it abstains
on 60% of cells and the winning *threshold* abstains on 80%, i.e. **both families converge on
"mostly do not select"** rather than on any property of the gap.

## C. Rule 8 on the corpus — the band transfers WORSE, not better

| split | family | fitted edges | IS D | **OOS D** | OOS file-clustered |
|---|---|---|---|---|---|
| by parent-file date (cut 2026-09-07) | THRESHOLD | (0.0, 0.9) | +0.0410 | **−0.0014** (t −0.50) | +0.0083 |
| by parent-file date | **BAND** | (0.1, 1.0) | +0.0434 | **−0.0155** (t −5.08) | +0.0038 |
| by parent-file date | ALWAYS-ABSTAIN | — | — | −0.0147 (t −4.52) | +0.0062 |

20 seeded random FILE splits (fit on half the files, read the other half once):

| family | mean OOS D | median | D > 0 | beats always-abstain | beats the other family |
|---|---|---|---|---|---|
| THRESHOLD | +0.0109 | +0.0103 | 19/20 | 12/20 | 17/20 |
| **BAND** | **+0.0012** | **−0.0048** | **8/20** | **2/20** | **3/20** |
| ALWAYS-ABSTAIN | +0.0099 | +0.0015 | 12/20 | — | — |

Read that table honestly in both directions. The band is dead: it is a coin flip out of
sample and loses to the simpler family it nests. And the threshold family's apparent +0.0109
is **not** a rehabilitation of idea 241's rule: the edges it selects are (0.0, 0.9) in 12 of
20 seeds and it abstains on 83.4% of cells on average, so it beats always-abstain in only
12/20 — a coin flip too. Both families are collecting the ROOM the control carries
(idea 241: `OOS_ctl − OOS_mean` +0.0258, t +22.2), not margin information, and the file-
clustered means make that explicit: THRESHOLD +0.0270, BAND +0.0265, ALWAYS-ABSTAIN +0.0326 —
**doing nothing but holding the control is the best of the three.**

## D. Rule 8 on live prices, out of corpus (31 arms × 3 panels × 2 rungs, 200 seeded sub-menus)

Coverage first, because it bounds everything after it: the ungated control is the IS argmax in
**400/400** sub-menus on broad136 and **400/400** on small439, so every abstention rule is a
**strict no-op on two of three panels** (idea 458's open question, confirmed here). On u56 it
moves 308 of 400 cells.

Edges chosen without touching 2017+ — on the live calibration frame (arms ≤2013, payoff
2014–16) → THRESHOLD (0.0, 0.9), BAND (0.1, 1.0); the record-fitted edges from part C are
identical. D on the headline frame (arms ≤2016, payoff 2017+):

| panel | cost | ALWAYS-ABSTAIN | CAL/BAND | CAL/THRESHOLD |
|---|---|---|---|---|
| broad136 / small439 | 10, 25 | +0.0000 | +0.0000 | +0.0000 |
| u56 | 10 bps | −0.1161 | **−0.1078** | −0.1014 |
| u56 | 25 bps | −0.0811 | **−0.0649** | −0.0811 |

Live terciles on u56 MOVED cells are **monotone-down** (ρ −0.345 @10bps, −0.706 @25bps) — the
margin does sort there, in the direction *opposite* to the queue's rule, reproducing the
parent's live reading. The record's mid peak does not appear on fresh prices at all.

### Books and both KEEP paths (equal weight over each cell's chosen arm)

| panel | cost | book | CAGR | Sharpe | MaxDD | OOS CAGR | OOS Sharpe | OOS MaxDD | 4a | 4b |
|---|---|---|---|---|---|---|---|---|---|---|
| u56 | 10 | ARGMAX | 11.13% | **1.2255** | −15.53% | 11.79% | **1.2743** | −15.53% | ✗ | **✓** |
| u56 | 10 | CAL/THRESHOLD | 17.17% | 1.1422 | −27.75% | 17.91% | 1.1556 | −27.75% | ✗ | ✗ |
| u56 | 10 | CAL/BAND | 17.18% | 1.1322 | −28.16% | 17.92% | 1.1442 | −28.16% | ✗ | ✗ |
| u56 | 10 | INCUMBENT = ALWAYS-ABSTAIN | 17.74% | 1.1245 | −29.18% | 18.47% | 1.1353 | −29.18% | ✗ | ✗ |
| u56 | 10 | RULES v2 (live) | 8.66% | 1.2056 | −12.05% | 9.53% | 1.2851 | −12.05% | — | — |
| u56 | 10 | SPY | 15.23% | 0.8890 | −33.72% | 15.45% | 0.8820 | −33.72% | — | — |
| broad136 | 10 | every book (no-op) | 18.92% | 1.1220 | −32.72% | 18.59% | 1.1006 | −32.72% | ✗ | ✗ |
| small439 | 10 | every book (no-op) | 13.12% | 0.6770 | −46.03% | 12.88% | 0.6351 | −46.03% | ✗ | ✗ |

**42 rule books: 4a 0/42, 4b 2/42, 4b(OOS) 2/42, BOTH 0/42.** The two 4b passes are the
ARGMAX book on u56 at 10 and 25 bps — idea 241's already-published object, not this run's
band, which fails 4b at both rungs. **No KEEP-candidate, no memo.**

## Pre-registered predictions vs outcome

| | prediction | outcome |
|---|---|---|
| R1 | the mid peak is a menu-size composition artefact | **REFUTED** — it survives within-\|A\| demeaning at t +3.4; the artefact is between-FILE |
| R2 | only the "wide tercile is negative" half survives | **PARTLY** — wide is the only tercile negative in 3 of 4 demeaning schemes, but it is not significant within FILE either |
| R3 | the band wins in sample and fails rule 8 | **CONFIRMED** — +0.0173 IS, −0.0155 OOS on the date split, 3/20 vs the threshold family |
| R4 | live: loses on u56, strict no-op elsewhere | **CONFIRMED** — −0.065/−0.108 on u56, 800/800 no-op cells on broad136 and small439 |

## Survivorship

The small panel is current constituents of a sub-$2B screen (483 names, tickers with
`max_1d_move >= 1.0` in `data/small_meta.csv` dropped first, 439 remaining) and broad136 is
current constituents (PROTOCOL 9). Levels are upward-biased; only same-cell contrasts (rule
minus argmax, same ladder, same days) are read. The record corpus inherits whatever bias each
source run carried — this is a re-reading of committed results, not new evidence about returns.

## What the queue should take from this

1. `456` is answered: **not menu size, not IS spread — FILE.** The correct control for any
   record-wide tercile/decile shape is a parent-file fixed effect, not a size stratum.
2. The mid peak's within-|A| survival is itself a warning: **the shape differs qualitatively
   in every menu-size stratum** (ρ from −0.64 to +0.37), so any pooled margin curve in the
   record is a mixture statistic and should be published stratified or not at all.
3. `458` gets a free confirmation: the ungated control is the IS argmax in 800/800 broad136 and
   small439 sub-menus here, which silently reduces every chooser experiment on those panels to
   a constant.
