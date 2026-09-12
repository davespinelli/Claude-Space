# Idea 842 — is the NEGATIVE NEXT-WINDOW delta a BASE-RATE IDENTITY? (cloud lane, 2026-09-12)

**ANSWERED: NO — AND NOT CONTENT EITHER. The delta decomposes EXACTLY into a base-rate term plus
a within-book term, and the base-rate term's share of it is not a number the record can quote:
it is +0.41 at the head cell, +0.74 at 0 bps, +0.11 at 25 bps, and spans −10.71 to +1.63 across
the very 48 cells that all carry the same negative sign.** The queue's premise — that a
no-information generator with the same per-book base rates and halves marginals reproduces the
−0.15 — is **half right at one cost rung and wrong at the other two**. At **10 of those 48 cells**
the base-rate term has the **opposite sign** to the delta it is supposed to explain (OVERLAP21/
756/OTHER3: delta −0.0628, base-rate term **+0.0685**), and at **12 more** it is **more negative
than the whole delta** (DISJOINT/1260/NONE: −0.1276 vs **−0.1809**, share +1.42), so it is not a
bound in either direction. **KILL for the base-rate-identity reading and for the content reading
alike. No KEEP claimed, no book promoted, no memo, no RULES/PROTOCOL change (rule 6); RULES.md,
PROTOCOL.md, scan.py, bot.py and baseline.py untouched.**

Script: `2026-09-12_is-the-NEGATIVE-NEXT-WINDOW-delta-a-BASE-RATE-IDENTITY_cloud.py`
(`.txt`, `.books.csv`, `.grid.csv`, `.perbook.csv`, `.generators.csv`, `.wf.csv`). Runtime 35s.
Two tuned parameters: **P1 generator** (ANALYTIC / BERNOULLI / HYPERGEOM), **P2 base-rate
estimator** (RAW / LOO / SHRUNK) — all 9 cells reported. H {756, 1260}, scheme {OVERLAP21,
CHAIN, DISJOINT}, 12 tiling offsets, conditioning {NONE, OTHER3, DDCAGR, SHARPE}, cost
{0, 10, 25} bps and memo set {MEMO8, MEMO12} are reported at **all 144 cells**, not selected.
No book dial is tuned: every book runs at the gross, band, n and cadence its own memo published.

## The closed form the queue asked for

For a cell with books *k*, pair counts *n_k*, halves-PASS shares *s_k*, base rates *b_k*:

    w_k^P = n_k s_k / SUM_j n_j s_j      w_k^F = n_k (1-s_k) / SUM_j n_j (1-s_j)
    delta_NOINFO = SUM_k w_k^P b_k - SUM_k w_k^F b_k                                        (1)
    delta_REAL - delta_NOINFO = SUM_k [ w_k^P (1-s_k) + w_k^F s_k ] d_k                     (2)

(2) is **exact algebra**, not an approximation — it follows from *b_k = s_k p_k^P + (1−s_k) p_k^F*.
Books with *s_k* ∈ {0,1} carry weight 0 in the within term, which is correct: their *d_k* is
undefined. **GATE G5: max |delta_REAL − noinfo_RAW − within_term| = 4.233e-16 over all 144
cells** against a 1e-12 bar.

## Gates

| gate | result |
|---|---|
| G1+G2 the 12 books reproduce their own committed triples | **12 of 12 PASS**; LIVE 8.63% / 1.2018 / −12.05% |
| G3 vectorised window metrics vs `engine.metrics` | max \|diff\| **2.220e-16** vs bar 1e-10 — PASS |
| **G4 reproduce ideas 832 and 839's committed deltas from an independent census** | **6 of 6 EXACT**: 832 H_INFO 756 (n 627, 0.3182/0.3810/**−0.0628**) and 1260 (n 419, 0.7072/0.7838/**−0.0765**); 839 OVERLAP21/NONE (n 1680, **−0.1067**), SHARPE (n 1472, **−0.1269**), CHAIN (n 564, **−0.1149**), DISJOINT HEAD (n 288, **−0.1620**) — PASS |
| **G5 the decomposition (2) is an identity** | max err **4.233e-16** vs 1e-12 — PASS |
| G6 Monte-Carlo convergence to the closed form (2,000 draws) | max \|BERNOULLI − ANALYTIC\| **0.0006**, \|HYPERGEOM − ANALYTIC\| **0.0006** vs bar 0.02 — PASS |

## The answer: SHARE = delta_NOINFO / delta_REAL

Head cell MEMO12 / DISJOINT / H=756 / NONE at 10 bps, **n = 288 pairs, 12 books**:

    delta_REAL -0.1620  =  base-rate term -0.0660  +  within term -0.0960

| estimator | base-rate term | **SHARE** |
|---|---|---|
| RAW | −0.0660 | **+0.4073** |
| LOO | −0.0618 | +0.3815 |
| SHRUNK (m0 = 3.99) | −0.0566 | +0.3493 |

**H_ID (SHARE ≥ 0.80) FAIL. H_CONTENT (SHARE ≤ 0.20) FAIL.** The delta is roughly
**40% selection structure and 60% within-book**, and neither pre-registered reading survives.
**H_EST PASS**: max−min SHARE over the three estimators is **0.0580** vs a 0.10 bar, so the
answer does not turn on how *b_k* is estimated. The three generators agree to 0.006 (ANALYTIC
+0.4073 / BERNOULLI +0.4065 / HYPERGEOM +0.4112), and the real delta sits at the **edge** of the
independence band at that cell ([−0.1608, +0.0300], p **0.0500**).

*Declared degeneracy:* HYPERGEOM resamples the observed labels, so it preserves *b_k* exactly and
cannot read an estimator — its three estimator rows are identical **by construction** and are
printed rather than deduplicated.

## Why the share is not quotable: it moves with the cost rung and flips sign across cells

| cost | delta_REAL | base-rate term | within term | SHARE (RAW) |
|---|---|---|---|---|
| 0 bps | −0.1400 | **−0.1035** | −0.0365 | **+0.7391** |
| **10 bps (PROTOCOL)** | **−0.1620** | −0.0660 | −0.0960 | **+0.4073** |
| 25 bps | −0.1214 | −0.0136 | −0.1078 | **+0.1119** |

Same 288 pairs, same books, same formula: the cost rung alone takes the answer from "mostly a
base-rate identity" to "mostly within-book". Across the **48 negative 10-bps cells** (idea 839's
48 of 48 reproduces exactly):

| estimator | median SHARE | min | max | ≥0.80 | ≤0.20 |
|---|---|---|---|---|---|
| RAW | **+0.4091** | −10.7143 | +1.6343 | 18 of 48 | 16 of 48 |
| LOO | +0.3535 | −16.5333 | +1.7708 | 18 of 48 | 16 of 48 |
| SHRUNK | +0.2791 | −9.2294 | +1.2754 | 12 of 48 | 18 of 48 |

**H_UNIV FAIL** — 18 identity-like, 16 content-like, 14 in between out of 48 cells that are
*unanimous in sign*. The count of the two failure modes over those 48 cells (6 and 8 of the 24
MEMO12 cells respectively) matters more than the spread:

- **Sign reversal, 10 of 48.** At OVERLAP21/756/OTHER3 (idea 832's own published cell) the delta
  is −0.0628 while the base-rate term is **+0.0685**: the selection structure points the *other
  way*, and the entire negative sign is within-book (−0.1312). Same at CHAIN/756/OTHER3 and
  DISJOINT/756/OTHER3 — every reversal is a conditioned (OTHER3/DDCAGR) cell at H=756.
- **Overshoot, 12 of 48.** At DISJOINT/1260/NONE the base-rate term is **−0.1809** against a delta
  of −0.1276 (SHARE +1.4171) and the within term is **positive** (+0.0532) — the no-information
  generator is *more* negative than the data, which is idea 839's BOOKLAB finding restated as
  algebra rather than as a permutation. Every overshoot is an H=1260 cell.

So the two axes PROTOCOL does not name split the answer cleanly: **conditioning flips the
base-rate term's sign, horizon makes it overshoot, and cost sets its size** — at 25 bps the
median base-rate term over that rung's 32 negative cells is **−0.0276 of the delta, i.e. the
wrong sign on average**, against +0.7105 at 0 bps and +0.4091 at 10.

## The per-book anatomy (head cell) — the mechanism is three books, not a relationship

| book | n | s_k | b_k | d_k | base-rate contribution | within contribution |
|---|---|---|---|---|---|---|
| R1 | 24 | 0.2500 | 0.5417 | −0.7222 | **−0.0235** | −0.0483 |
| K5 | 24 | 0.2917 | 0.7083 | −0.3950 | **−0.0202** | −0.0291 |
| R3 | 24 | 0.5417 | 0.2917 | +0.0350 | **+0.0177** | +0.0031 |
| K3 | 24 | 0.2500 | 0.2500 | +0.3333 | −0.0108 | +0.0223 |
| K8 | 24 | 0.3333 | 0.6667 | +0.5000 | −0.0091 | +0.0397 |
| K7 | 24 | 0.8333 | 0.0000 | 0.0000 | +0.0000 | +0.0000 |

`Spearman(s_k, b_k) = −0.1241` — **the monotone relationship the queue's premise assumes is
essentially absent**. The base-rate term is a *weighted difference*, and −0.0437 of its −0.0660
is two books (R1, K5) whose halves leg fires rarely while their 4b base rate is high. K7 is the
instructive null: *s_k* = 0.833 and *b_k* = 0 give it the largest `w^P` in the cell (0.1869) and
it contributes exactly zero to both terms.

## H_POWER — the one pre-registered leg that fails on noise, not on algebra

| injected d_k | delta_REAL | base-rate term | within term (normalised) | identity error | recovery error |
|---|---|---|---|---|---|
| 0.00 | −0.0354 | −0.0621 | +0.0301 | 0.0e+00 | 0.0301 |
| **+0.20** | +0.1430 | −0.0546 | **+0.2235** | 0.0e+00 | 0.0235 |
| **−0.20** | −0.2334 | −0.0692 | **−0.1857** | 0.0e+00 | 0.0143 |

**H_POWER FAIL** as pre-registered (max recovery error 0.0235 vs a 0.01 bar). The identity leg
holds to **1.110e-16** at every injection, so the failure is entirely binomial sampling noise at
288 pairs: **the decomposition is exact but the head cell cannot resolve a within-book delta to
better than about ±0.03**, which is 19% of the −0.1620 it is being asked to explain. This is the
resolution statement the run's other numbers should be read against.

## RULE 8 (this run's own tuned axis) — H_WF PASS, and it does not rescue the finding

Pairs split by C12: IS = predictor window ends ≤ 2016-12-31 (96 pairs), OOS = predictor entry
≥ 2017-01-01 (48 pairs). No pair is scored twice.

| leg | n pairs | delta_REAL | base-rate (RAW) | SHARE | within term |
|---|---|---|---|---|---|
| IS | 96 | −0.1209 | −0.0280 | +0.2315 | −0.0929 |
| **OOS** | 48 | **−0.1667** | −0.0208 | **+0.1250** | −0.1458 |

IS pick (SHARE closest to 1.00) = (BERNOULLI, RAW) at +0.2433 → **OOS +0.1120, gap 0.1313** vs a
0.20 bar: **H_WF PASS**. But it passes by agreeing that the base-rate term explains **almost
nothing** on either leg (0.12–0.24), which contradicts the 0.74 the same corpus reads at 0 bps
and the +1.42 it reads at H=1260. On the LOO estimator the OOS base-rate term is **+0.0278**
against a delta of −0.1667 — the wrong sign again, on the untouched window.

## RULE 8 mandated book leg + BOTH KEEP paths (unchanged: this run tunes no book dial)

Fixed window from trading day 260; OOS from 2017-01-01. SPY 15.16% / 0.8861 / −33.72%
(halves 0.9595 / 0.8259); OOS SPY 15.33% / 0.8767 / −33.72% (0.9802 / 0.7650).
LIVE RULES v2 8.63% / 1.2018 / −12.05%; OOS 9.47% / 1.2782 / −12.05%.

| book | full CAGR / Sharpe / MaxDD | OOS CAGR / Sharpe / MaxDD | 4a | 4b | 4b OOS-only |
|---|---|---|---|---|---|
| K4 | 11.9% / 1.2095 / −15.5% | 12.7% / 1.2693 / −15.5% | FAIL (H2>LIVE+DD) | PASS | PASS |
| K5 *(standing candidate)* | 11.5% / 1.2017 / −15.9% | 12.7% / 1.2775 / −15.9% | FAIL (H2>LIVE+DD) | PASS | PASS |
| **K8** | 14.2% / 1.2226 / −14.8% | **16.0% / 1.3937 / −12.7%** | FAIL (H1>LIVE+DD) | PASS | PASS |
| R3 | 15.4% / 1.2260 / −20.0% | 16.0% / 1.2154 / −20.0% | FAIL (H2>LIVE+DD) | PASS | PASS |
| K7 | 6.2% / 1.1687 / −11.1% | 6.4% / 1.1871 / −11.1% | FAIL (H2>LIVE) | FAIL (CAGR) | FAIL (CAGR) |

**4a: 0 of 12** (every book's MaxDD is worse than the live book's −12.05%). **4b: 11 of 12;
OOS-only 4b: 11 of 12** — K7 alone fails, on the CAGR floor. Identical to idea 839's reading of
the same corpus, as it must be.

`baseline.compare()` at 10 bps, weekly: K5 11.5% / 1.20 / −15.9% (halves 1.24/1.17) and K8
14.2% / 1.22 / −14.8% (1.14/1.30) against RULES v2 8.6% / 1.20 / −12.1% (1.23/1.18) — both
**4a KILL** on the drawdown leg, which is PROTOCOL 4's stated reason for having path 4b at all.

## Pre-registered scorecard

| hypothesis | bar | result | verdict |
|---|---|---|---|
| H_ID | SHARE ≥ 0.80 at head | +0.4073 | **FAIL** |
| H_CONTENT | SHARE ≤ 0.20 at head | +0.4073 | **FAIL** |
| H_UNIV | same verdict at ≥80% of 48 cells | 37.5% | **FAIL** |
| H_EST | max−min SHARE ≤ 0.10 | 0.0580 | **PASS** |
| H_WF | IS→OOS SHARE gap ≤ 0.20 | 0.1313 | **PASS** |
| H_POWER | injected ±0.20 recovered to 0.01 | 0.0235 | **FAIL** |

**3 of 6 PASS**, and the two that pass are the two that say the answer is *stable* rather than
that it is *large*.

## What this leaves standing, and what it retires

**Standing.** Ideas 832 and 839's one durable statement — *the halves clause's verdict is never
positively informative*, 48 of 48 cells negative at the PROTOCOL rung — is untouched and now has
an exact algebraic reading: `delta = base-rate term + positively-weighted mean of per-book
deltas`, and BOTH terms are negative at the head cell.

**Retired.** Any future claim that the negative next-window delta *is* a base-rate or selection
artefact. It is not: the artefact term carries the wrong sign at 10 of the 48 negative cells, overshoots the
whole delta at 12 more, and moves from 0.74 to 0.11 on nothing but PROTOCOL's own cost rungs.
Equally retired is the opposite claim that the delta is a clean within-book fact — 40% of it is
selection at the rung PROTOCOL actually uses. **The quantity has no quotable decomposition, which
is the same conclusion idea 838's lane reached about its length and idea 839 reached about its
offsets: this statistic is not stable enough to publish a number for.**

**SURVIVORSHIP:** `universe.json` and `universe_broad.json` are current-constituent lists, so
every level above is optimistic. The object measured is a within-corpus conditional contrast and
its algebraic decomposition; survivorship does not cancel out of either term.
