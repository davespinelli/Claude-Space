# Idea 214 — does the Q95 band hold its nominal 5 percent?

**Verdict: ANSWERED. YES on the statistic and panels that matter, NO as a constant — and the
idea's own proposed remedy (a calibrated quantile) FAILS rule 8.** No RULES change, no KEEP,
PROTOCOL untouched; the recommendation is a wording change to clause 11b, proposed only.

Script: `2026-09-08_does-the-q95-band-hold-its-nominal-5-percent_cloud.py`
96 known-null arms x (1 real + 200 priced rotations) = 19,296 backtests, 10 bps, weekly,
next-day, idea 191's machinery verbatim. Deterministic (no `hash()`-seeded RNG), no network.
Runtime 1,625 s.

## Part 0 — the label already misstates the target, by arithmetic

Under exact exchangeability the real statistic's rank among {real} ∪ {K rotations} is uniform,
so a band at the r-th order statistic has size exactly `(K+1-r)/(K+1)`:

| band | K=20 | K=50 | K=100 | K=200 |
|---|---|---|---|---|
| MAX (r=K) | 0.0476 | 0.0196 | 0.0099 | 0.0050 |
| Q95 (r=⌈0.95K⌉) | **0.0952** | 0.0588 | **0.0594** | 0.0547 |

So "Q95" means 9.52% at K=20 and 5.94% at K=100 — 1.90x and 1.19x the 5% the clause names —
and the MAX band's size *collapses* with K, 4.76% → 0.50%. **The band and K cannot be chosen
independently**, which is the same fact idea 216 measured as "the MAX band walks away from
0.05", here stated as arithmetic that needs no run.

## Part 1 — realised size on a ZERO-INFORMATION overlay (all 32 grid points in `.size.csv`)

Q95/K=100, by statistic (96 arms, se across arms):

| statistic | realised | se | t vs 5% | t vs its own 5.94% |
|---|---|---|---|---|
| Sharpe (full) | **0.0531** | 0.0212 | +0.15 | −0.30 |
| MaxDD | 0.0874 | 0.0253 | +1.48 | +1.11 |
| Sharpe (IS) | 0.0677 | 0.0229 | +0.77 | +0.36 |
| Sharpe (OOS) | 0.0357 | 0.0178 | −0.80 | −1.33 |

**On the Sharpe statistic the Q95/K=100 band holds 5%.** The drawdown statistic runs
anti-conservative at 8.74% (1.75x the target) but at t +1.48 that is *not* demonstrated at
96 arms — it is a direction, not a finding.

The one deviation that IS decisive is the panel:

| panel (Q95/K=100, Sharpe) | realised | se | t vs 5% |
|---|---|---|---|
| BROAD136 | 0.0826 | 0.0468 | +0.70 |
| U56 | 0.0748 | 0.0423 | +0.59 |
| **SMALL439** | **0.0020** | 0.0020 | **−24.36** |

**On SMALL439 the clause has essentially no size at all** — a zero-information overlay clears
it twice in a thousand instead of once in twenty — so on that panel clause 11b is not a 5%
test, and a "clears" there carries far more evidence than the same word on U56 while a
"fails" carries almost none. Same story on the OOS window (0.0020, t −24.36). By target
on-share the size is 0.0443 / 0.0313 / 0.0684 / 0.0684 at 0.15 / 0.30 / 0.50 / 0.70 — no
monotone on-share effect.

*Caveat, stated rather than hidden:* at K=200 the K-subset is the whole D=200 pool, so those
four rows are deterministic given the pool and carry no subsampling variance; MAX/K=200's
0.0000 means no arm's real statistic exceeded all 200 of its own rotations.

## Part 2 — mechanism: the exchangeability worry does not bite

The idea's premise is that neighbouring circular rotations are correlated. They are —
correlation of the null statistic by circular offset distance:

| distance (rebalances) | <5 | 5–10 | 10–25 | 25–50 | 50–100 | 100–250 | ≥250 |
|---|---|---|---|---|---|---|---|
| mean ρ | **+0.3646** | +0.0611 | −0.0424 | −0.0382 | −0.0044 | −0.0022 | −0.0094 |

— but the correlation is gone beyond ~10 rebalances, and a random K-subset of ~975 rotations
almost never draws near-neighbours, so it does not damage the size. The direct check agrees:
the real arm's rank position inside its own pool is near-uniform (mean 0.4592 vs 0.500,
sd 0.2909 vs 0.289, share above 0.95 = 0.0417 vs 0.050 on the Sharpe statistic; DD is the
worst at 0.5254 / 0.0729). **The premise "correlated rotations break the nominal size" is
NOT supported; the size problem the run does find is a panel effect, not a dependence effect.**

## Rule 8 — the proposed fix does not survive

Calibrate on IS (≤2016-12-31): for each K take the smallest order statistic r* whose realised
IS size is ≤5%; apply it to 2017-2026, read once.

| K | r nominal (Q95) | IS size nominal | r* calibrated | IS size at r* | OOS size nominal | OOS size calibrated | \|err\| nominal | \|err\| calibrated |
|---|---|---|---|---|---|---|---|---|
| 20 | 19 | 0.1039 | 20 | 0.0495 | 0.0699 | 0.0324 | 0.0199 | 0.0176 |
| 50 | 48 | 0.0654 | 49 | 0.0396 | 0.0390 | 0.0259 | 0.0110 | 0.0241 |
| 100 | 95 | 0.0677 | 97 | 0.0385 | 0.0357 | 0.0275 | 0.0143 | 0.0225 |
| 200 | 190 | 0.0625 | 192 | 0.0417 | 0.0312 | 0.0312 | 0.0188 | 0.0188 |

**The IS-calibrated quantile beats the nominal Q95 out of sample in 1 of 4 rungs; mean OOS
error 0.0207 (calibrated) vs 0.0160 (nominal).** The idea's own recommendation — "clause 11b
needs a calibrated quantile, not a nominal one" — is therefore **not supported**: calibration
moves r by 1-2 order statistics and makes the OOS size *worse* on average.

## Both KEEP paths on the known-null books

A zero-information overlay clears **4a in 0/96** and **4b in 14/96 (14.6%)**; BOTH 0/96.
Thirteen of the fourteen are on U56 (8 at share 0.15, 5 at 0.30) and one on BROAD136;
**SMALL439 0/32**. The U56 untreated control clears 4b on its own (`4b -`), so those thirteen
are the carrier again — the same conclusion this run's companion idea 435 reached from a
completely different construction. The commonest binding bar on the null books is
`H1,H2,OOS,DD,CAGR` (29) followed by `CAGR` alone (17).

Comparands (10 bps, post-warm-up OOS 2017-2026): NOISE arms mean 9.14% / 0.8204 / −18.99%;
U56 control 14.49% / 1.1775 / −18.21%; BROAD136 12.40% / 0.8758 / −21.57%; SMALL439 7.46% /
0.4997 / −26.84%; SPY 15.45% / 0.8820 / −33.72%; RULES v2 9.53% / 1.2851 / −12.05% (U56),
7.98% / 1.1185 / −12.24% (BROAD136), 3.84% / 0.5710 / −14.48% (SMALL439).

## Recommendation (proposed only; PROTOCOL.md, RULES.md, scan.py, bot.py, baseline.py untouched)

1. **Do not adopt a calibrated quantile.** Rule 8 says it is worse out of sample than the
   nominal one.
2. **Quote the combinatorial size, not the label.** Clause 11b should print `(K+1-r)/(K+1)`
   beside every verdict; "Q95 at K=20" is a 9.5% test and "MAX at K=200" is a 0.5% test, and
   neither name says so.
3. **Publish the panel.** The clause's realised size is 0.0748 / 0.0826 / **0.0020** on
   U56 / BROAD136 / SMALL439. A rotation-null verdict on the small panel is not comparable to
   one on a large-cap panel and should not be pooled with it.
4. **Do not use the band on the drawdown statistic without more arms.** The point estimate is
   1.75x the target; the run cannot resolve it at 96 arms and says so rather than claiming it.

**SURVIVORSHIP:** SMALL439 is current constituents of a sub-$2B screen with `max_1d_move ≥ 1.0`
names dropped (44 of 483, leaving 439); BROAD136 is current constituents of a large-cap list.
The panel ordering above inherits that bias — and note the panel finding is about the *size of
a test*, which the survivorship bias affects only through the return process it conditions on.
