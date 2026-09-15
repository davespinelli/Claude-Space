# Idea 870 — is the CORR-LO excess a VOL TARGET in disguise? (lane B, 2026-09-15)

**ANSWERED: NO — AND THE QUEUE'S HYPOTHESIS IS INVERTED ON BOTH LEGS THAT COULD HAVE CARRIED IT.
It is the SAME GATE (Jaccard 0.533 at matched rate and matched gross) and it is NOT the same
effect: the excess is a MEAN leg, not a vol leg; a vol-regime-preserving null does not erase it
but nearly TRIPLES it; and the vol target is CHEAPER AND WORSE, not cheaper and equal.
KILL for capital.**

Script `2026-09-15_is-the-CORR-LO-excess-a-VOL-TARGET-in-disguise_B.py`; 3,456 real arms
(3 panels × 8 families × 3 q × 4 w × 3 depths × 2 cadences × 2 grosses) and **77,760 placebo
evaluations** (7,776 cells × 10 md5 seeds), weekly/daily gates, 10 bps, t+1, all grid points
reported. Two tuned parameters, the queue's own: **target form** and **cost rung**.

## The question and why it had a mechanical basis

Idea 815 left exactly one survivor on its eight-family sweep: **CORR-LO is the only family whose
placebo excess walks forward** (ρ +0.392 BLOCK / +0.468 YEARBLOCK) and **the only one with zero
4b passes in 432 books** — a persistent Sharpe edge that buys no capital. The queue's reading:
de-grossing on low average pairwise correlation is a realised-vol target priced at a worse cost.

That is not a loose analogy. The record's `state_corr` is built from the equal-weight variance
identity, so average pairwise correlation *is* portfolio variance divided by average name
variance. Firing on low corr is firing on a low ratio, which at roughly constant name vol is
firing on low portfolio vol. The test is therefore to split the identity and price both halves:

| family | state | role |
|---|---|---|
| CORR-LO / CORR-HI | the record's `state_corr` | the subject |
| **PORTVOL**-LO / -HI | 20d vol of the **equal-weight book** | the numerator — what a vol target targets |
| **NAMEVOL**-LO / -HI | 20d **average name** vol (= the record's VOL20) | the denominator |
| **VTCONT**-LO / -HI | continuous `m = clip(σ_target/σ_t, 1−depth, 1)` | the textbook vol target |

## Gates (printed before any new number)

G1 never-firing multiplier ≡ ungated book **0.000e+00** · G2 every placebo's mean effective
multiplier ≡ the real arm's **0.000e+00** (so the matched-gross twin cancels exactly and
excess = Sharpe(real) − Sharpe(placebo)) · G4 determinism, every placebo re-seeded
**0.000e+00** · G5 fast Sharpe ≡ `engine.metrics()['Sharpe']` **0.000e+00** · G6 the
decomposition is exact, `MEANLEG + VOLLEG − excess` **2.220e-16** over all 7,776 cells ·
**G3 PASS 4/4**: idea 815's committed CORR table rebuilt here, median |Δ| **0.0038** —
CORR-HI/BLOCK +0.0554→+0.0517, CORR-HI/YEARBLOCK +0.0249→+0.0210, CORR-LO/BLOCK
+0.0341→+0.0298, CORR-LO/YEARBLOCK +0.0568→+0.0541.

## [1] H_LEG **FAIL, and inverted** — CORR-LO is the one family that is *not* a denominator effect

Exact split, no residual: `excess = (μr−μp)/σr + μp(σp−σr)/(σr σp)`. Median over 432 arms, BLOCK.

| family | excess | MEAN leg | VOL leg | VOL share | share of arms \|VOL\|>\|MEAN\| |
|---|---|---|---|---|---|
| CORR-HI | +0.0517 | +0.0177 | +0.0349 | 0.675 | 0.613 |
| **CORR-LO** | **+0.0298** | **+0.0491** | **−0.0168** | **−0.563** | **0.153** |
| NAMEVOL-HI | +0.0189 | −0.0066 | +0.0301 | 1.595 | 0.583 |
| NAMEVOL-LO | −0.0219 | −0.0036 | −0.0151 | 0.688 | 0.347 |
| PORTVOL-HI | +0.0328 | −0.0004 | +0.0346 | 1.057 | 0.660 |
| PORTVOL-LO | +0.0128 | +0.0294 | −0.0170 | −1.332 | 0.299 |

A vol target is, by construction, a denominator effect. Every HI-side family is one (VOL share
0.675 / 1.057 / 1.595). **CORR-LO's vol leg is NEGATIVE** — the gate makes the book's realised
vol *worse* than the placebo's and earns its entire excess, and then some, on the numerator.
Only 15.3% of its arms are vol-dominated, the lowest of the eight. The sign is not a CORR fact
but a **SIDE** fact: both LO families run a negative vol leg, both HI families a positive one.

## [2] H_SPAN **PASS** — and this is what makes the rest decisive

Matched on panel/q/w/depth/cadence, median over 216 matched grid points:

| comparand | Jaccard of de-grossed days | ρ(multiplier paths) | Δ rate | Δ gbar |
|---|---|---|---|---|
| **PORTVOL-LO** | **0.533** | **+0.640** | −0.001 | **+0.0002** |
| VTCONT-LO | 0.533 | +0.625 | −0.001 | +0.055 |
| NAMEVOL-LO | 0.217 | +0.217 | +0.010 | −0.005 |
| PORTVOL-HI / NAMEVOL-HI / VTCONT-HI | 0.000 / 0.018 / 0.000 | −0.157 / −0.102 / −0.120 | | |

ρ(CORR, PORTVOL) on the raw daily states is **+0.868 / +0.896 / +0.930** (U56 / B136 / SMALL)
against ρ(CORR, NAMEVOL) +0.579 / +0.563 / +0.651 — the identity behaves as advertised. So the
low-correlation gate really is *mostly the same gate* as a low-portfolio-vol gate: over half the
same days, the same firing rate to 0.001, the same realised gross to 0.0002. **Same days,
different money** — which is the whole finding.

## [3] H_NULL **FAIL, and inverted by a factor of 2.7** — the excess is orthogonal to the vol regime

VOLBLOCK is BLOCK with the realised-vol regime put back: a circular shift applied independently
*within each realised portfolio-vol tercile*, so every placebo firing day sits in the same vol
regime as a real one. It is the exact analogue of what EPISODEFIX did to the calendar in 815.

| family | BLOCK | YEARBLOCK | **VOLBLOCK** | Δ | cut | share>0 |
|---|---|---|---|---|---|---|
| CORR-HI | +0.0517 | +0.0210 | +0.0496 | −0.0021 | 0.041 | 0.905 |
| **CORR-LO** | +0.0298 | +0.0541 | **+0.0792** | **+0.0494** | **−1.657** | **0.995** |
| NAMEVOL-HI | +0.0189 | −0.0121 | +0.0133 | −0.0055 | 0.294 | 0.634 |
| NAMEVOL-LO | −0.0219 | +0.0065 | +0.0229 | +0.0448 | 2.044 | 0.840 |
| PORTVOL-HI | +0.0328 | −0.0009 | +0.0298 | −0.0030 | 0.090 | 0.775 |
| PORTVOL-LO | +0.0128 | +0.0402 | +0.0637 | +0.0510 | −3.990 | 0.998 |

Holding the vol regime fixed was supposed to erase the excess. It **raises** it, on every panel
(U56 +0.0113→+0.0765, B136 +0.0298→+0.1188, SMALL +0.0506→+0.0631) and on 99.5% of arms. The
BLOCK null was *masking* part of the low-tail edge by being free to roll firing days into high-vol
days where de-grossing pays for free. The HI side barely moves (cut 0.041 / 0.090), so this is
not a null that flatters everything — it discriminates, and it discriminates the wrong way for
the queue's hypothesis.

## [4] H_COST **FAIL, and the ranking reverses** — the vol target is cheaper *and worse*

Matched on panel/q/w/depth/cadence/gross (Δgbar printed so the match is auditable), median over
432 matched pairs:

| comparand | Δ gbar | Δ Sharpe @0 | @10 | @25 | Δ gate turnover |
|---|---|---|---|---|---|
| **PORTVOL-LO** | **+0.0002** | **−0.0173** | **−0.0134** | **−0.0085** | **−0.4206** |
| NAMEVOL-LO | −0.0048 | −0.0448 | −0.0384 | −0.0283 | −0.8649 |
| VTCONT-LO | +0.0549 | −0.0110 | +0.0042 | +0.0205 | −2.4135 |

The queue's reading was "same effect, worse price". At a gross match of 0.0002 the vol target
trades **less** (3.11/yr against CORR-LO's 3.47) and earns **less at every rung**. CORR-LO's
extra turnover is bought, not wasted: the gap is +0.0173 of Sharpe gross of costs and still
+0.0085 at 25 bps, i.e. costs eat about half of it over the full ladder and none of the
conclusion. The only forms that beat CORR-LO are the **HI-side** ones (PORTVOL-HI +0.0271 @10,
VTCONT-HI +0.0382 @10) — which are not a disguise for it, they are its opposite tail
(Jaccard 0.000).

## [5] H_WF **FAIL on the second conjunct — which strengthens the headline**

ρ(IS excess 2009-2016, OOS excess 2017+) per family:

| family | BLOCK | YEARBLOCK | VOLBLOCK |
|---|---|---|---|
| **CORR-LO** | **+0.413** | **+0.467** | **+0.503** |
| PORTVOL-LO | +0.238 | +0.363 | +0.404 |
| CORR-HI | +0.281 | +0.227 | +0.190 |
| NAMEVOL-LO | +0.320 | +0.164 | −0.131 |
| NAMEVOL-HI | −0.232 | −0.379 | −0.194 |
| PORTVOL-HI | +0.146 | −0.029 | +0.049 |

Idea 815's committed CORR-LO BLOCK ρ was **+0.392**; here **+0.413** (YEARBLOCK 815 +0.468, here
+0.467) — an independent reproduction of the one persistent result in the record. The bar asked
whether the *vol target inherits it*. Under the record's own null it does not: PORTVOL-LO reads
+0.238, below the +0.30 bar, and CORR-LO beats it under all three nulls. **The persistence
belongs to correlation, not to the vol state it is 53% the same gate as.**

## [6] The books — and the real structural finding

Comparands @10 bps, weekly, t+1. U56: SPY 15.13%/0.885/−33.72% (OOS 15.27%/0.874), RULES v2
8.64%/1.208/−11.90% (OOS 9.49%/1.286). B136: SPY 15.16%/0.886/−33.72%, RULES v2
7.98%/1.101/−12.18% (OOS 7.88%/1.108). SMALL: SPY 14.06%/0.858/−33.72%, RULES v2
4.30%/0.663/−13.89% (OOS 3.75%/0.559).

Full-sample census over all 3,456 grid points, nothing selected:

| family | arms | 4a | 4b | med Sharpe | med CAGR | best OOS Sharpe |
|---|---|---|---|---|---|---|
| CORR-HI | 432 | 1 | **131** | 1.061 | 10.27% | 1.469 |
| PORTVOL-HI | 432 | 0 | **97** | 1.039 | 10.09% | 1.403 |
| VTCONT-HI | 432 | 0 | **90** | 1.054 | 10.38% | 1.225 |
| NAMEVOL-HI | 432 | 0 | **65** | 1.010 | 9.84% | 1.471 |
| CORR-LO | 432 | 0 | **0** | 0.972 | 9.80% | 1.127 |
| VTCONT-LO | 432 | 0 | **0** | 1.010 | 10.22% | 1.106 |
| PORTVOL-LO | 432 | 0 | **0** | 0.949 | 9.67% | 1.100 |
| NAMEVOL-LO | 432 | 0 | **0** | 0.871 | 9.00% | 1.106 |
| **TOTAL** | 3,456 | **1** | **383** | | | |

CORR-LO's 4a 0/432 and 4b 0/432 reproduce idea 815 exactly. But **"a persistent edge that buys
no capital" is not a CORR-LO fact — it is a LO-SIDE fact.** All four low-tail gates are 0 of 432,
whichever state you read the tail from; all four high-tail gates pass in bulk. 4b does not reward
the information a low-tail gate carries, because de-grossing in calm markets forfeits CAGR
against a floor of 70% of SPY's while shallowing a drawdown the cap already grants. Cost ladder
over all arms: median Sharpe 1.016 (0 bps) → 0.995 (10) → 0.961 (25).

**Rule 8 on the books.** IS-only selector (highest 2009-2016 Sharpe per panel × family), OOS read
once: 24 picks, **OOS 4a 0 of 24**, OOS 4b 3 of 24, and **CORR-LO 0 of 3** — all three passes are
HI-side. The CORR-LO picks land at U56 12.88%/0.993/−20.84%, B136 13.53%/1.004/−23.08%, SMALL
6.33%/0.451/−45.59%: below SPY's OOS Sharpe on two panels and below its OOS CAGR on all three.

**By-product, NOT proposed** (memo `2026-09-15_VTCONT-HI-U56-BYPRODUCT_MEMO.md`): the continuous
vol target had never been priced in this record, and its U56 rule-8 pick is the cheapest 4b
candidate on the shelf — **VTCONT-HI q=0.17 w=252 depth=0.50 weekly g=1.00: 13.66%/1.098/−18.79%,
halves 1.107/1.089, OOS 14.73%/1.178/−18.79%, 4b at 0/10/25 bps, 4a FAILS**, on gate turnover of
**0.71/yr** against CORR-HI's 2.16. It is robust in its own neighbourhood (10 of 12 (q,w) cells at
depth 0.50/W/g1.00 pass 4b both full-sample and OOS; 67 of 144 U56 arms). It is **not promoted**:
352 of 3,456 arms clear 4b both ways, all HI-side, so this is the best of a large field read off
a grid, and it is the *opposite tail* from the idea this run was asked to price.

## Caveats

SURVIVORSHIP: all three panels are current-constituent lists (the small panel additionally drops
the 52 tickers with `max_1d_move` ≥ 1.0 per `data/small_meta.csv`), so CAGR and drawdown *levels*
are optimistic throughout; the placebo differencing and the real-minus-null contrasts are the
durable part. VOLBLOCK's terciles are full-sample cuts of a state the null never trades — a
measurement device exactly as idea 815's declared episodes were, stated rather than hidden.

## Verdict

**KILL for capital.** The queue's hypothesis is refuted: CORR-LO is the same *gate* as a
realised-vol target and not the same *effect*, and where the two differ the correlation version
is the better one, not the worse one. No RULES change, no book promoted, no PROTOCOL edit
applied. `RULES.md`, `PROTOCOL.md`, `scan.py`, `bot.py` and `baseline.py` untouched (rule 6).

Follow-ups filed: 900, 901, 902.
