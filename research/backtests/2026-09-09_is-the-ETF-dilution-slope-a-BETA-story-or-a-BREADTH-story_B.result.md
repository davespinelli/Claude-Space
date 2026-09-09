# Idea 291 — is-the-ETF-dilution-slope-a-BETA-story-or-a-BREADTH-story (lane B, 2026-09-09)

**ANSWERED / SPLIT: the BREADTH half is REFUTED and the BETA half is only HALF true. The slope
is a MEAN-RETURN slope.** No RULES change, no book promoted, no KEEP claimed; RULES.md,
PROTOCOL.md, products/scan.py, products/bot/bot.py and research/baseline.py untouched.

## Gates first, all PASS

| gate | result |
|---|---|
| **Reproduction** — idea 277's committed `...is-ETF36-a-third-cluster..._C.sweepbooks.csv` EWall block rebuilt from source, 9 rungs x 7 columns | max abs diff **2.220e-16**; the published slope re-reads **OOS Sharpe 1.0597 -> 0.6656, monotone 8/8** |
| **Identity** — `Sharpe == sqrt(252)*mu/(sbar*sqrt(D))` over 54 pooled decompositions | **2.220e-16** |
| **Identity, per panel** — the same over 294 per-panel decompositions | **2.220e-16** |
| **Scale invariance** — `Sharpe(book x lambda) == Sharpe(book)`, all 18 arms rescaled to the s=0 gross | **6.661e-16** |
| **Weight-pool vs return-pool** — the decomposition runs on the weight-pooled book, idea 277 pools net returns | **1.336e-04** of Sharpe = **0.03%** of the move being decomposed |
| every panel k == 36 at every rung | asserted at run time; width is not confounded with composition |

## The identity (exact, not a fit)

For any book with realised drifted weights `held`, gross `G_t`, `y_t = (sum_i held_i r_i)/mean(G)`:

    mu = mean(y)                          MEAN-RETURN channel
    sbar = mean_t sum_i u_it sigma_i      VOL channel (average vol of what is HELD)
    D = var(y)/sbar^2                     CO-MOVEMENT channel (diversification)
    Sharpe = sqrt(252) * mu / (sbar * sqrt(D))
    log Sharpe = 0.5 log 252 + log mu - log sbar - 0.5 log D

so the s = 0 -> 1 move splits into three exactly additive numbers (residual < 1e-15).

## "At matched realised gross" — executed AND proved inert

Realised gross runs 0.7445 -> 0.7501 across the sweep (GATED; UNGATED is flat at 0.7501).
Rescaling every rung to the s=0 gross changes Sharpe by **4.441e-16**. A gross difference can
reach a Sharpe only through the cost bill, and that bill's spread across s is **0.0277 of
Sharpe on GATED (7.0% of the 0.394 OOS move) and 0.0003 on UNGATED (0.1%)**. The gross-matching
instruction is carried out literally in `.grossmatched_arms.csv` and it moves nothing.

## The answer — pooled book, all rungs, both conventions, three windows

| conv / window | Sharpe 0 -> 1 | dlogS | **MEAN** | **VOL** | **CO-MOVEMENT** |
|---|---|---|---|---|---|
| GATED / FULL | 1.1467 -> 0.7285 | -0.4536 | **-0.8201 (+180.8%)** | +0.4240 (-93.5%) | -0.0575 (+12.7%) |
| GATED / IS | 1.1620 -> 0.6829 | -0.5316 | **-0.9622 (+181.0%)** | +0.4409 (-82.9%) | -0.0102 (+1.9%) |
| GATED / OOS | 1.1342 -> 0.7646 | -0.3943 | **-0.7083 (+179.6%)** | +0.3994 (-101.3%) | -0.0855 (+21.7%) |
| UNGATED / FULL | 1.1727 -> 0.8301 | -0.3455 | **-0.6799 (+196.8%)** | +0.3675 (-106.4%) | -0.0331 (+9.6%) |
| UNGATED / IS | 1.1990 -> 0.7689 | -0.4444 | **-0.7923 (+178.3%)** | +0.3636 (-81.8%) | -0.0157 (+3.5%) |
| UNGATED / OOS | 1.1507 -> 0.8798 | -0.2684 | **-0.5918 (+220.5%)** | +0.3626 (-135.1%) | -0.0393 (+14.6%) |

Step by step, all 8 rung-to-rung steps in every conv x window: **MEAN is negative 8/8, VOL is
positive 8/8** (falling constituent vol is a Sharpe TAILWIND the whole way), and CO-MOVEMENT is
positive in only 2-5 of 8.

## Pooling-artefact control (this run's own correction to itself)

`k_eff` on the pooled book falls 76 -> 34, but that is **seed pooling, not composition**: at s=0
the six seed panels hold six different 36-name draws from BSTK100, at s=1 all six ARE ETF36. Re-run
per panel (k = 36 at both ends, k_eff ~ 35 at both ends) and the co-movement channel collapses:

| conv / window | MEAN | VOL | CO-MOVEMENT |
|---|---|---|---|
| GATED / FULL | **+203.9%** | -104.0% | **+0.1%** |
| GATED / OOS | **+201.9%** | -113.3% | **+11.3%** |
| UNGATED / FULL | **+205.0%** | -110.8% | +5.8% |
| UNGATED / OOS | **+231.8%** | -142.1% | +10.2% |

## Channel freeze (exact counterfactual from the identity)

| conv / window | actual move | MEAN frozen at s=0 | VOL frozen | CO-MOVEMENT frozen |
|---|---|---|---|---|
| GATED / FULL | -0.4182 | **+0.5076 (SIGN REVERSES)** | -0.6699 | -0.3750 |
| GATED / OOS | -0.3696 | **+0.4183 (SIGN REVERSES)** | -0.6214 | -0.3013 |
| UNGATED / FULL | -0.3426 | **+0.4657** | -0.5979 | -0.3147 |
| UNGATED / OOS | -0.2709 | **+0.4393** | -0.5385 | -0.2356 |

Hold the mean channel fixed and an all-ETF panel out-Sharpes an all-stock one. Hold the
co-movement channel fixed and 81-92% of the slope is still there.

## BETA or BREADTH

**BETA: half of it.** Inside the mean channel, `mu = beta*mu_spy + alpha`, and `beta*mu_spy`
carries **56.1% of d(mu) OOS / 57.9% FULL** on GATED (42-51% on UNGATED). Beta itself falls
**0.823 -> 0.438** (GATED, full) and **1.024 -> 0.707** (UNGATED). So the ETF end is lower-beta
AND lower-alpha, roughly half and half; "beta story" is a true half, not the whole.

**BREADTH: refuted as the carrier.** The co-movement channel is worth +0.1% to +21.7% of the
move and the queue's named sub-term is the smallest piece of it: decomposing dD (+0.0378, GATED
full) gives **rho +0.0680, cross-sectional vol dispersion +0.0013 (3.4%), k_eff +0.0112**.

**Correction to the parent's characteristic reading.** Idea 277 reported dispersion HALVING
(0.0964 -> 0.0620) and correlation FLAT (0.3626 -> 0.3436). Measured as the quantities that
actually enter a Sharpe, both go the other way: the vol-weighted pairwise correlation of the
HELD set **rises 0.355 -> 0.426** and the cross-sectional CV of constituent vols **rises 0.252 ->
0.468**. Idea 277's `disp` is 63-day return dispersion over the eligible set and its `corr` is the
unweighted whole-panel matrix mean; neither is the term that multiplies into `D`. "Dispersion"
is two different quantities in this record and they move in opposite directions.

## Rule 8 walk-forward (s chosen on 2009-2016 IS Sharpe, 2017-2026 read once)

| book | pick | CAGR | Sharpe | MaxDD | H1/H2 | OOS CAGR | OOS Sharpe | OOS MaxDD |
|---|---|---|---|---|---|---|---|---|
| IS-Sharpe pick (GATED) | s=0.000 | 13.13% | 1.0745 | -22.01% | 1.1994/0.9517 | 12.60% | 1.0597 | -22.01% |
| IS-Sharpe pick (UNGATED) | s=0.125 | 15.67% | 1.1792 | -25.22% | 1.3145/1.0624 | 15.39% | **1.1442** | -25.22% |
| RULES v2 (live, pooled) | — | 7.39% | 1.0628 | -12.03% | 1.1460/0.9822 | 7.60% | 1.1030 | -12.03% |
| RULES v1 (pooled) | — | 7.35% | 0.7967 | -15.67% | 1.0154/0.6041 | 6.50% | 0.6956 | -15.67% |
| SPY | — | 15.23% | 0.8890 | -33.72% | 0.9566/0.8340 | 15.45% | 0.8820 | -33.72% |
| s=1.000 EWall (GATED) | — | 5.11% | 0.6287 | -21.79% | 0.6624/0.6015 | 5.58% | 0.6656 | -21.79% |

The chooser beats SPY OOS 2/2 and RULES v2 OOS 1/2. **Rule 8 on the ANSWER itself**: the
attribution is stable across the split — share_MEAN 181.0% (IS) vs 179.6% (OOS) on GATED,
178.3% vs 220.5% on UNGATED; the sign and the ordering of the three channels is identical in
every window. The conclusion is not an in-sample artefact.

## Both KEEP paths — 116 arms (18 pooled + 98 per-panel), 10 bps

**4a: 0 / 116.** **4b: 7 / 116** — pooled GATED s=0.125 (11.74%/1.0435/-18.52%) and s=0.250
(11.22%/1.0466/-18.21%), plus 5 single-seed panels. The dominant binding leg is the DD cap
(46 arms fail on DD alone). **These are NOT a KEEP candidate**: a MIX panel is a seeded random
draw of 36 names, not a rule anyone can trade, and the pass is idea 277's already-published
EWall-on-a-large-cap-panel shape restricted to a lucky composition. No memo is filed.

## Survivorship, stated

universe_broad.json is current constituents and every MIX panel is a subset of it, so the STOCK
end carries a survivorship premium the ETF end structurally cannot. That bias runs **toward**
a steep slope and **toward** attributing it to the mean channel, so the mean channel's 180-232%
is an UPPER bound and the co-movement channel's ~0-22% is the conservative half — which is the
half that gets refuted.

## Grid

9 ETF shares x 2 gate conventions x 6 seeds (s=1.000 is ETF36 for every seed, so one panel there)
= 49 panels, 196 grid rows at 10 and 0 bps, 348 decompositions, 18 pooled arms, all reported in
`.grid.csv`, `.channels.csv`, `.panelchannels.csv`, `.steps.csv`, `.freeze.csv`,
`.grossmatch.csv`, `.grossmatched_arms.csv`, `.attribution.csv`, `.panelattribution.csv`,
`.walkforward.csv`, `.keeppaths.csv` and `.console.txt`.

Tuned parameters (PROTOCOL rule 4, exactly two): **ETF share s** (9 rungs) and **gate convention**
(GATED / UNGATED). Seed is replication, window and cost rung are reporting axes.

## For the queue

The un-ranked book's Sharpe on these panels is a **mean-return** statistic wearing a
diversification statistic's name: the three channels move -0.82 / +0.42 / -0.06, i.e. the two
large ones are the numerator and the denominator's LEVEL, and they partly cancel. Worth asking
whether the record's other published "panel property explains the Sharpe" claims survive the same
three-way split, since a characteristic that only moves `sbar` is buying Sharpe from the wrong
end.
