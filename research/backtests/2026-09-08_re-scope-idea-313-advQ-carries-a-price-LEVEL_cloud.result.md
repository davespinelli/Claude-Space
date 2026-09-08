# Idea 424 — does the capQ/advQ decile SIGN gap survive a price-free liquidity key? (2026-09-08, cloud)

**ANSWERED, and the queue's premise is INVERTED. The sign gap SURVIVES the substitution and
WIDENS with the price-free key: removing the price level from advQ makes it disagree with capQ
MORE, not less. Separately — and this is the larger result — the decile-slope statistic that
generated idea 313's question is itself KILLED by rule 8: not one of the 14 (key x membership x
arm) slopes keeps its sign across the two halves. KEEP 4a 2/210, 4b 0/210. Rules unchanged;
no book promoted; no KEEP-candidate; no memo.**

Script `2026-09-08_re-scope-idea-313-advQ-carries-a-price-LEVEL_cloud.py`;
artefacts `.console.txt` `.deciles.csv` `.slopes.csv` `.bootstrap.csv` `.walkforward.csv` `.keys.csv`.

## What was run

SMALL panel (483 names, 44 dropped for `max_1d_move >= 1.0` -> **439 tradable**, 2010-01-04 ..
2026-09-04). Idea 51 lane B's pre-registered decile point held fixed: g = 0.75, weekly, 10 bps
(0 bps alongside), NDEC = 10, key window 60d median, MA 200d, arms {EWall, MA-RS, MA-DG}.

Exactly **two parameters, fully crossed, all grid points reported**:

- **p1 key** — `capQ` (static 2026 mktcap), `advQ` (`(px*vol)` 60d median — idea 51's column),
  `VOLSH` (share volume only, no price), `DVOLT` (`terminal_price_i * vol` — a FIXED per-name
  price scale times volume)
- **p2 membership** — STATIC (a name sits in one decile forever) or DYNAMIC (re-ranked
  cross-sectionally each day). `capQ` is constant in time so `capQ-DYNAMIC` does not exist.

7 schemes x 10 deciles x 3 arms = **210 books**, each at 10 and 0 bps.

**This decomposition is the point.** Idea 51 ran capQ only as STATIC and advQ only as DYNAMIC,
so its sign gap confounds *key content* with *membership dynamics*. Running every liquidity key
under both memberships separates them.

## Gates

**G2 — T1 invariance re-measured on THIS panel** (idea 197's operator `px -> px @ diag(c)`,
c lognormal, sigma {0.25, 0.50} x 3 seeds), reported rather than cited:

| key | fraction of key cells whose cross-sectional rank moves |
|---|---|
| capQ | **0.0000** (a file column; no price operator touches it) |
| advQ | **0.9531** [0.9359, 0.9687] |
| VOLSH | **0.0000** |
| DVOLT | **0.9594** [0.9435, 0.9718] |

The premise holds: advQ carries a price level, VOLSH does not. (Idea 197 quotes 73% for advQ;
this run reads 95.3% because the window here is idea 51's 60d **median**, not idea 197's 20d
mean — a different statistic on a different panel, reported as such, not reconciled away.)

**G1 — reproduction of idea 51 lane B.** `advQ-DYNAMIC`, the leg the queue's question is about,
**reproduces EXACTLY** (max |diff| 8.33e-17 on Sharpe, 9.93e-17 on CAGR, all 30 rows). `capQ-STATIC` does **not** reproduce
bit-exact, and the cause is a **data vintage, not this script**: `research/deepvalue/universe_under2b.csv`
was re-committed on 2026-09-07, *after* idea 51 ran. It now covers **434** of the 439 tradable
names against the **435** idea 51's console reports; since the decile edges are `qcut` over the
covered set, one name moves and the 43/44 sizes alternate differently (15 of 30 capQ rows have a
different decile size; 0 of 30 advQ rows do). The published vintage is not recoverable from the repo. **Bound on the
damage: max |dSharpe| drift 0.0257**, and idea 51's headline slopes still reproduce (capQ MA-DG
rho **-0.335** vs published -0.336/-0.335; advQ-D MA-RS **+0.335** vs published +0.335).

## Q1 — key agreement is the answer to idea 313 in one table

Spearman between the STATIC per-name key ranks (n = names):

|  | capQ | advQ | VOLSH | DVOLT |
|---|---|---|---|---|
| **capQ** | +1.000 | +0.429 | **+0.318** | **+0.709** |
| **advQ** | +0.429 | +1.000 | +0.843 | +0.844 |
| **VOLSH** | +0.318 | +0.843 | +1.000 | +0.711 |
| **DVOLT** | +0.709 | +0.844 | +0.711 | +1.000 |

capQ agrees with `DVOLT` (+0.709) more than twice as well as with `VOLSH` (+0.318), and advQ sits
between them at +0.429. **What capQ shares with a liquidity key is the PRICE LEVEL, not the
volume** — which is arithmetically unsurprising once stated (market cap = price x shares), and is
exactly what idea 313 was asking about.

## Q2 — the sign gap, FULL / IS 2010-2016 / OOS 2017-2026

rho(decile, dSharpe vs EWall), n = 10 deciles, so **SE(rho) ~ 0.354**.

| key | memb | arm | rho_full | t | rho_IS | t | rho_OOS | t |
|---|---|---|---|---|---|---|---|---|
| capQ | STATIC | MA-RS | **-0.326** | -0.98 | +0.365 | +1.11 | -0.583 | -2.03 |
| capQ | STATIC | MA-DG | **-0.335** | -1.01 | +0.349 | +1.05 | -0.709 | -2.85 |
| advQ | STATIC | MA-RS | +0.099 | +0.28 | +0.550 | +1.86 | -0.265 | -0.78 |
| advQ | STATIC | MA-DG | +0.133 | +0.38 | +0.531 | +1.77 | -0.309 | -0.92 |
| advQ | DYNAMIC | MA-RS | **+0.335** | +1.01 | +0.462 | +1.48 | +0.120 | +0.34 |
| advQ | DYNAMIC | MA-DG | +0.113 | +0.32 | +0.396 | +1.22 | -0.463 | -1.48 |
| VOLSH | STATIC | MA-RS | **+0.630** | +2.30 | +0.649 | +2.41 | +0.153 | +0.44 |
| VOLSH | STATIC | MA-DG | +0.381 | +1.16 | +0.609 | +2.17 | -0.193 | -0.56 |
| VOLSH | DYNAMIC | MA-RS | +0.467 | +1.49 | +0.522 | +1.73 | +0.272 | +0.80 |
| VOLSH | DYNAMIC | MA-DG | +0.262 | +0.77 | +0.408 | +1.26 | -0.159 | -0.46 |
| DVOLT | STATIC | MA-RS | +0.058 | +0.16 | +0.715 | +2.89 | -0.423 | -1.32 |
| DVOLT | STATIC | MA-DG | -0.113 | -0.32 | +0.652 | +2.43 | -0.513 | -1.69 |
| DVOLT | DYNAMIC | MA-RS | +0.184 | +0.53 | +0.628 | +2.28 | -0.484 | -1.57 |
| DVOLT | DYNAMIC | MA-DG | -0.264 | -0.78 | +0.419 | +1.31 | -0.682 | -2.64 |

**Two readings, and the second one is the important one.**

1. **The substitution answer.** Ordering the gap-to-capQ by how much price the key carries gives
   **DVOLT < advQ < VOLSH** — the *price-free* key disagrees with capQ *most*. Deleting the price
   level does not repair the disagreement, it enlarges it. Idea 313's framing ("advQ carries a
   price level, so the disagreement is contamination") is inverted: the contamination is the part
   that partially RECONCILES advQ with market cap.
2. **The membership decomposition.** On MA-RS the gap to capQ splits as key content
   (capQ-S vs advQ-S, both static) **+0.425** and membership dynamics (advQ-S vs advQ-D)
   **+0.236**. Both axes matter; key content is roughly two thirds. Idea 51's single comparison
   could not have separated them.

## Q3 — paired calendar-year block bootstrap (1,000 draws, seed 424)

One year-resample per draw applied to every book, so rho and the gap are PAIRED.

**No individual slope is distinguishable from zero.** P(rho > 0): capQ-S MA-RS **0.227**,
MA-DG 0.245; advQ-D MA-RS 0.892; the only 90% interval excluding zero is VOLSH-D MA-RS
[+0.110, +0.612], P 0.979. So "capQ is negative and advQ is positive" **overstates what n = 10
supports** — idea 51's -0.336 / +0.335 are each about one SE from zero.

**The GAP, however, is real** (rho_key - rho_capQ, paired per draw). MA-RS:

| contrast | gap (point) | boot mean | 5% | 95% | P(gap>0) | P(signs differ) |
|---|---|---|---|---|---|---|
| advQ-S vs capQ-S | +0.425 | +0.285 | -0.023 | +0.591 | 0.935 | 0.456 |
| advQ-D vs capQ-S | +0.662 | +0.480 | +0.090 | +0.788 | 0.977 | 0.667 |
| **VOLSH-S vs capQ-S** | **+0.957** | +0.614 | +0.167 | +1.007 | **0.993** | 0.684 |
| **VOLSH-D vs capQ-S** | **+0.793** | +0.607 | +0.209 | +0.952 | **0.994** | 0.754 |
| DVOLT-S vs capQ-S | +0.385 | +0.262 | +0.022 | +0.553 | 0.963 | 0.343 |
| DVOLT-D vs capQ-S | +0.510 | +0.325 | +0.052 | +0.630 | 0.975 | 0.479 |

MA-DG is the same ordering, weaker: VOLSH-S +0.716 (P 0.947), DVOLT-D **+0.071** (P 0.581,
signs differ only 14.0% of draws). Full table in `.bootstrap.csv`. **The two keys really do
measure different things; what is not supported is attaching a sign to either one alone.**

## Q4 — RULE 8

**W1 (the slope claim).** `rho_IS` is **positive in 14 of 14** rows — capQ included (+0.365 /
+0.349) — and `rho_OOS` is **negative in 10 of 14**, capQ most negative (-0.583 / -0.709). **Not
one key's slope keeps its sign across the halves.** capQ's negative full-sample slope is an
OOS-half artefact; advQ's positive full-sample slope is an IS-half artefact; the "sign
disagreement" idea 313 set out to explain is, on a walk-forward reading, two unstable statistics
rather than two stable opposite facts. This is the run's main result and it KILLS the decile-slope
statistic as something to build a clause on.

**W2 (a pick).** Decile chosen by best IS (2010-2016) EWall Sharpe, 2017-2026 read once:

| key | memb | pick | IS Sh | OOS CAGR | OOS Sh | OOS DD | vs SPY | vs v2 | vs ctrl |
|---|---|---|---|---|---|---|---|---|---|
| capQ | STATIC | 2 | 1.020 | 7.80% | 0.496 | -41.95% | -0.386 | -0.072 | -0.140 |
| advQ | STATIC | 1 | 0.981 | 22.54% | 1.346 | -28.31% | +0.464 | +0.778 | +0.709 |
| advQ | DYNAMIC | 1 | 1.695 | 37.42% | 2.213 | -24.54% | +1.331 | +1.645 | +1.576 |
| VOLSH | STATIC | 1 | 1.155 | 17.35% | 1.125 | -27.62% | +0.243 | +0.557 | +0.489 |
| VOLSH | DYNAMIC | 1 | 1.474 | 18.45% | 1.328 | -26.13% | +0.446 | +0.760 | +0.691 |
| DVOLT | STATIC | 1 | 1.037 | 16.52% | 0.980 | -35.93% | +0.098 | +0.412 | +0.343 |
| DVOLT | DYNAMIC | 1 | 1.194 | 17.47% | 1.142 | -26.08% | +0.260 | +0.574 | +0.506 |

OOS references: SPY 0.882 / 15.45% / -33.72%; RULES v2 0.568 / 3.85% / -14.68%; EWall whole-panel
control 0.637 / 10.09% / -36.17%. 6 of 7 picks beat SPY, the control and RULES v2 OOS.

**Read the row above only with this attached:** the IS chooser lands on **decile 1 in 6 of 7
cells** — the thinnest, least-liquid decile, precisely where current-constituent survivorship is
largest. Idea 51's cloud replication rejected the same corner ("control returns 19.71% CAGR,
least-liquid survivorship decile"). An OOS Sharpe of **2.213** on the least-traded tenth of a
current-constituents small-cap screen is a **bias measurement, not an edge**.

## Q5 — KEEP paths over all 210 books

**4a 2/210** (advQ-S d3 MA-DG, advQ-D d2 MA-DG). **4b 0/210.** Nothing here is capital-worthy,
which is the honest reading of the same survivorship fact.

## Caveats carried, not buried

- **SURVIVORSHIP.** `data/prices_small.csv.gz` is current constituents of the sub-$2B screen only
  — no delisted names — so every LEVEL on this panel is biased up, the thin deciles most of all.
  This run's claims are key-vs-key DIFFERENCES on one panel, which the bias affects far less than
  levels, but the Q4 table is a level table and is labelled as such.
- **capQ is a look-ahead CLASSIFIER** (a 2026 market-cap stamp used to sort 2010 returns). It is
  kept because idea 51 published it and the question is about reproducing that comparison, not
  because it is tradable.
- n = 10 deciles throughout; every rho carries SE ~ 0.354 and is reported with a t and a paired
  bootstrap for that reason.
- The capQ leg cannot be reproduced bit-exact (G1 above); the drift is bounded and quantified.
- `DVOLT`'s terminal price is a per-name constant taken from the end of the sample — an oracle
  diagnostic for isolating the price factor, never a tradable key.
