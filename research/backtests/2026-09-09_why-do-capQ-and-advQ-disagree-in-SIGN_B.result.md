# Idea 313 — why do capQ and advQ disagree in SIGN? (2026-09-09, lane B)

**ANSWERED. The sign gap is the 2026 LOOK-AHEAD STAMP and DECILE 1 — it is not "cap disagrees
with liquidity". Stamping the same market-cap key EARLY or DYNAMICALLY instead of in 2026 flips
its decile slope from negative to positive in 4 of 4 cells (paired bootstrap P(gap>0) 0.947-0.993),
while swapping the KEY at a fixed stamp moves it much less. Dropping decile 1 removes 81% (MA-RS)
and 77% (MA-DG) of the whole gap, and a no-late-entrants panel does NOT shrink it, so the residue
is the thin corner rather than late-entry survivorship. Two by-products: the record's published
"rho" is a PEARSON correlation on 10 points, not the Spearman its prose names — and on the rank
statistic idea 51's headline +0.335 is +0.030 — and idea 51's capQ slope is not reproducible today
at all, because the metadata file it reads is rewritten nightly. KEEP 4a 6/360, 4b 2/360, BOTH 0.
No book promoted, no memo, RULES untouched.**

Script `2026-09-09_why-do-capQ-and-advQ-disagree-in-SIGN_B.py`; artefacts `.console.txt`
`.deciles.csv` `.slopes.csv` `.bootstrap.csv` `.walkforward.csv` `.surv.csv`.

## What was run

SMALL panel (483 names, 44 dropped for `max_1d_move >= 1.0` → **439 tradable**, 2010-01-04 ..
2026-09-04). Idea 51 lane B's pre-registered decile point held fixed: g = 0.75, weekly, 10 bps,
NDEC = 10, key window 60d median, MA 200d, arms {EWall, MA-RS, MA-DG}.

Exactly **two parameters, fully crossed, all 6 grid points reported**:

- **p1 key** — `CAP` = `px_t * shares_eff_i` with `shares_eff_i = mktcap_2026 / px_i(last)`
  (the causal price-times-fixed-shares proxy idea 313 asks for); `ADV` = `(px*vol).rolling(60).median()`
  (idea 51's column, verbatim).
- **p2 stamp** — `LATE` rank once on each name's last valid key value; `EARLY` rank once on its
  first valid value; `DYN` re-rank cross-sectionally every day.

Idea 51 compared **(CAP, LATE)** against **(ADV, DYN)** — opposite corners, moving key content and
stamp timing at once. All six cells are run here, on two panels (MAIN 439 names, FULLHIST 239),
6 × 10 × 3 × 2 = **360 books**.

**Honest bound on what "causal" buys.** `shares_eff` is a 2026 share count. CAP/EARLY and CAP/DYN
remove the *price* look-ahead inside the cap stamp — the component that actually moves over 16
years — not the share-count look-ahead. A fully causal cap needs a shares history, which `data/`
does not carry (QUEUE 195 is PARKed on exactly that). No cell here is a clean market-cap decile
and none is tradable.

## Gates

| gate | result |
|---|---|
| **G1a** `rank(CAP at LATE stamp)` vs `rank(mktcap_2026)` | **0.00e+00** — CAP/LATE *is* idea 51's capQ |
| **G1b** ADV/DYN vs idea 424's committed `advQ-DYNAMIC`, 30 rows | max\|dSharpe\| **8.33e-17**, max\|dCAGR\| **9.93e-17** |
| **G1c** idea 51's published headline slopes | ADV/DYN MA-RS **+0.3351** vs published **+0.335** — exact under PEARSON |
| **G1a2** CAP/LATE vs idea 424's `capQ-STATIC`, 30 rows | max\|dSharpe\| **0.2329**, max\|dCAGR\| **0.0328** — see vintage note |
| **G2** `shares_eff` vs the file's own `shares` column, n=430 | median ratio **0.9883**, IQR [0.9715, 1.0041] (the price adjustment) |

**Two gate results are themselves findings.**

1. **The record's "rho" is Pearson, not Spearman.** Idea 51 and idea 424 both compute
   `np.corrcoef(decile, dSharpe)` while their prose calls the statistic Spearman. Under Pearson
   this run reproduces idea 51's `+0.335` to four decimals; under the rank statistic the same
   committed ladder reads **+0.030**.
2. **Idea 51's capQ slope is not reproducible today.** `research/deepvalue/universe_under2b.csv`
   was rewritten by the nightly filings job on **2026-09-09** and now covers **430** of the 439
   tradable names, against **434** one day earlier (idea 424) and **435** when idea 51 ran. The
   decile edges are `qcut` over the covered set, so five names moving re-cuts every boundary:
   `capQ MA-DG` reads **-0.199** here against **-0.335** yesterday and **-0.336** as published,
   and the book-level drift is **max \|dSharpe\| 0.233** — nine times idea 424's 0.0257 bound a
   day earlier. The published number is inside its own noise band (SE ≈ 0.354) but it is not a
   number the repo can hand back.

## Q1 — the answer, in one table

`rho_P` = Pearson (the record's statistic), `rho_S` = Spearman, `dSharpe vs EWall`, n = 10,
SE ≈ 0.354.

| key | stamp | arm | rho_P | t | rho_S | IS_P | t | OOS_P | t |
|---|---|---|---|---|---|---|---|---|---|
| CAP | **LATE** | MA-RS | **-0.125** | -0.36 | -0.152 | +0.372 | +1.13 | -0.515 | -1.70 |
| CAP | **LATE** | MA-DG | **-0.199** | -0.57 | -0.236 | +0.382 | +1.17 | -0.586 | -2.05 |
| CAP | EARLY | MA-RS | **+0.480** | +1.55 | +0.406 | +0.526 | +1.75 | +0.288 | +0.85 |
| CAP | EARLY | MA-DG | **+0.656** | +2.46 | +0.576 | +0.652 | +2.43 | +0.420 | +1.31 |
| CAP | DYN | MA-RS | **+0.677** | +2.60 | +0.733 | +0.636 | +2.33 | +0.167 | +0.48 |
| CAP | DYN | MA-DG | **+0.376** | +1.15 | +0.309 | +0.660 | +2.49 | -0.181 | -0.52 |
| ADV | LATE | MA-RS | +0.159 | +0.46 | +0.152 | +0.538 | +1.81 | -0.117 | -0.33 |
| ADV | LATE | MA-DG | -0.074 | -0.21 | -0.127 | +0.448 | +1.42 | -0.356 | -1.08 |
| ADV | EARLY | MA-RS | +0.266 | +0.78 | +0.236 | +0.637 | +2.34 | -0.085 | -0.24 |
| ADV | EARLY | MA-DG | +0.436 | +1.37 | +0.455 | +0.731 | +3.03 | -0.182 | -0.52 |
| ADV | DYN | MA-RS | **+0.335** | +1.01 | **+0.030** | +0.462 | +1.48 | +0.120 | +0.34 |
| ADV | DYN | MA-DG | +0.113 | +0.32 | +0.079 | +0.396 | +1.22 | -0.463 | -1.48 |

**The cap key's SIGN is the stamp.** Holding the key at CAP and moving only the stamp:
-0.125 → +0.480 → +0.677 (MA-RS) and -0.199 → +0.656 → +0.376 (MA-DG). The negative slope idea 51
attributed to *market cap* belongs to the *2026 price stamp*: sorting names by what they were
worth at the end of the sample puts the winners in the top deciles by construction, and that is
what reverses the ladder. Take the price look-ahead out — either stamp at entry or re-rank daily —
and the cap slope agrees with the liquidity key instead of opposing it, in **4 of 4** cells.

## Q2 — the decomposition, both paths

`gap = rho_P(ADV,DYN) - rho_P(CAP,LATE)`:

| arm | gap | path A: stamp (CAP) | + key (at DYN) | path B: key (at LATE) | + stamp (ADV) |
|---|---|---|---|---|---|
| MA-RS | **+0.460** | **+0.802** | -0.342 | +0.284 | +0.176 |
| MA-DG | **+0.311** | **+0.574** | -0.263 | +0.125 | +0.186 |

The two paths differ by a large interaction, so neither is privileged and both are printed. What
survives either reading: the **stamp leg is the big one on the cap key** (+0.802 / +0.574), the
**key leg at a fixed stamp is small** (+0.284 / +0.125 at LATE), and the key leg at DYN is
*negative* — i.e. once both keys are stamped causally they over-correct past each other rather
than agreeing. Idea 313's framing ("cap and liquidity disagree about size") is not what the grid
shows; the two stamps of the *same* key disagree more than the two keys at the same stamp.

## Q3 — paired calendar-year block bootstrap (1,000 draws, seed 313)

One year-resample per draw applied to every book, so gaps are paired.

| arm | contrast | gap | 5% | 95% | P(gap>0) | P(signs differ) |
|---|---|---|---|---|---|---|
| MA-RS | **CAP/EARLY − CAP/LATE** | **+0.531** | +0.056 | +1.003 | **0.971** | 0.627 |
| MA-RS | **CAP/DYN − CAP/LATE** | **+0.629** | +0.227 | +1.051 | **0.988** | 0.627 |
| MA-RS | ADV/LATE − CAP/LATE | +0.242 | -0.019 | +0.539 | 0.922 | 0.377 |
| MA-RS | ADV/DYN − CAP/LATE | +0.381 | -0.016 | +0.728 | 0.942 | 0.579 |
| MA-DG | **CAP/EARLY − CAP/LATE** | **+0.708** | +0.278 | +1.118 | **0.993** | 0.682 |
| MA-DG | **CAP/DYN − CAP/LATE** | +0.447 | -0.004 | +0.930 | 0.947 | 0.542 |
| MA-DG | ADV/LATE − CAP/LATE | +0.112 | -0.145 | +0.401 | 0.741 | 0.188 |
| MA-DG | ADV/DYN − CAP/LATE | +0.247 | -0.181 | +0.695 | 0.820 | 0.400 |

**The stamp contrasts are the ones whose intervals exclude zero**; the pure key contrast at a
fixed LATE stamp is the weakest row in both arms (P 0.922 / 0.741). Individually, only the
causally-stamped cap slopes are distinguishable from zero (CAP/EARLY P 0.964 / 0.981, CAP/DYN
P 0.972 / 0.829); every LATE-stamped slope, idea 51's two headline numbers included, has a 90%
interval straddling zero.

## Q4 — survivorship, the third named cause

| arm | gap MAIN | gap deciles 2-10 | gap FULLHIST (no late entrants) |
|---|---|---|---|
| MA-RS | +0.460 | **+0.088** | +0.737 |
| MA-DG | +0.311 | **+0.073** | +0.405 |

**Decile 1 carries 81% (MA-RS) and 77% (MA-DG) of the whole sign gap.** Removing it leaves a
residue smaller than a quarter of one standard error. Rebuilding every scheme on the 239 names
priced on the panel's first bar does **not** shrink the gap (it widens), so the mechanism is the
*thin corner* — the smallest/least-traded tenth of a current-constituent screen, where the
survivorship bias is largest and where the Pearson statistic puts most of its weight — and not
late-entry composition. This is also why the Pearson/Spearman split matters in exactly one cell:
mean \|P − S\| over the 12 schemes is only **0.066** with **0/12** sign disagreements, but idea
51's published `advQ-D MA-RS` reads **+0.335 Pearson / +0.030 Spearman**, a gap of +0.305 —
4.6× the mean — because decile 1's dSharpe is -0.707 against a -0.06..-0.29 body.

## Q5 — RULE 8

**W1 (the slope claim).** Over 24 (panel, key, stamp, arm) cells: `rho_IS > 0` in **24/24**,
`rho_OOS < 0` in **18/24**, and only **6/24** keep their sign across the boundary. Idea 424 found
14/14 and 10/14 on one panel and one stamp scheme; this extends the same result to two panels and
three stamps, including the causal ones. **The decile-slope statistic does not walk forward under
any stamp**, so no clause should be built on it — that verdict is independent of which key or
statistic is used.

**W2 (a pick).** Decile chosen by best IS (2010-2016) EWall Sharpe, 2017-2026 read once. OOS
references: SPY 0.882 / 15.45% / -33.72%; RULES v2 0.568 / 3.85% / -14.68%; whole-panel EWall
control 0.637 / 10.09% / -36.17%.

| panel | scheme | pick | IS Sh | OOS CAGR | OOS Sh | OOS DD | vs SPY | vs v2 | vs ctrl |
|---|---|---|---|---|---|---|---|---|---|
| MAIN | CAP/LATE | d2 | 1.029 | 6.78% | 0.440 | -44.32% | -0.442 | -0.128 | -0.196 |
| MAIN | CAP/EARLY | d1 | 1.748 | 17.25% | 1.150 | -25.57% | +0.268 | +0.582 | +0.513 |
| MAIN | CAP/DYN | d1 | 2.366 | 50.58% | 2.348 | -32.40% | +1.466 | +1.779 | +1.711 |
| MAIN | ADV/LATE | d1 | 0.871 | 8.35% | 0.550 | -35.23% | -0.332 | -0.018 | -0.087 |
| MAIN | ADV/EARLY | d1 | 1.438 | 19.87% | 1.143 | -31.21% | +0.261 | +0.575 | +0.506 |
| MAIN | ADV/DYN | d1 | 1.695 | 37.42% | 2.213 | -24.54% | +1.331 | +1.645 | +1.576 |
| FULLHIST | CAP/LATE | d2 | 1.079 | 5.95% | 0.423 | -37.24% | -0.459 | -0.145 | -0.214 |
| FULLHIST | CAP/EARLY | d1 | 1.912 | 17.28% | 1.176 | -26.05% | +0.294 | +0.608 | +0.540 |
| FULLHIST | CAP/DYN | d1 | 2.164 | 43.18% | 2.148 | -27.64% | +1.266 | +1.580 | +1.512 |
| FULLHIST | ADV/LATE | d10 | 1.006 | 12.63% | 0.737 | -32.55% | -0.145 | +0.168 | +0.100 |
| FULLHIST | ADV/EARLY | d1 | 1.435 | 22.24% | 1.272 | -27.79% | +0.390 | +0.704 | +0.635 |
| FULLHIST | ADV/DYN | d1 | 1.626 | 36.55% | 2.077 | -26.43% | +1.195 | +1.509 | +1.441 |

**Read that table only with this attached:** every causally-stamped scheme picks **decile 1** —
the thinnest, least-liquid tenth of a current-constituents small-cap screen — and an OOS CAGR of
50.58% there is a **bias measurement, not an edge**. The only schemes that do *not* pick the thin
corner are the two LATE-stamped ones, and they are the two that lose to SPY. That is the same
corner idea 51's cloud replication and idea 424 both rejected.

## Q6 — KEEP paths over all 360 books

**4a 6/360** (all MA-DG: CAP/EARLY d1, CAP/DYN d2, ADV/DYN d2, on both panels).
**4b 2/360** — `MAIN CAP/DYN d1 MA-DG` (CAGR 14.50%, Sharpe 1.861, MaxDD -16.82%, halves
1.25/2.39, OOS 18.61% / 2.242) and its FULLHIST twin (12.05%, 1.422, -19.23%, 0.91/1.84,
OOS 15.58% / 1.694). **BOTH 0/360.**

**Neither 4b passer is promoted, and this is a judgement stated rather than buried.** It is
decile 1 by *daily-re-ranked* market cap on a current-constituent sub-$2B screen — the corner
where this panel's survivorship bias is largest — its "cap" still carries a 2026 share count, and
a key that re-ranks on price daily buys whatever has just fallen, which is a mechanical
mean-reversion overlay rather than a size clause. Under PROTOCOL 4 it is **PARK, not KEEP**: it
would need a delisting-inclusive panel and a real shares history before the number means anything.
No memo, no RULES change.

## Caveats carried, not buried

- **SURVIVORSHIP.** `data/prices_small.csv.gz` is current constituents of the sub-$2B screen only
  — no delisted names — so every LEVEL is biased up, decile 1 most. This run's claims are
  scheme-vs-scheme DIFFERENCES; the Q5 table is a level table and is labelled as such.
- **`shares_eff` is a 2026 share count** (see the honest bound above). CAP/EARLY and CAP/DYN are
  price-causal, not fully causal.
- **CAP covers 430/439 names, ADV covers 439**, so the two keys' ladders are cut over slightly
  different sets — inherited from idea 51's design, and the same in idea 424.
- **n = 10 deciles throughout**; every rho carries SE ≈ 0.354, a t, and a paired bootstrap.
- **The capQ leg cannot be reproduced against yesterday's artefact** (G1a2), for a documented
  data-vintage reason that is outside this script.
