# Idea 1476 (lane C, 2026-09-22) — how many committed BEST-RUNG claims sit on a ladder whose NEIGHBOURS are a FACTOR 2 APART

**VERDICT: ANSWERED (census) + KILL of the refinement premise. No new capital book, no KEEP memo.**

Script: `research/backtests/2026-09-22_best-rung-ladder-spacing_C.py` (deterministic, seed 1476, no network).
Panels U56 (`universe.json`, 56 names) and B136 (`universe_broad.json`, 136 names), weekly cadence, 10 bps,
t+1 execution. Tuned parameters: **2** (the refined rung; the bootstrap block length) — all grid points reported.

---

## (A) CENSUS — the record's best-rung claims sit on ladders it cannot resolve

Scanned `LEADERBOARD.md`, `CHANGELOG.md` and every `research/backtests/*.md` memo for rows carrying a
best/argmax/optimal/steepest/peaks-at claim **and** at least two values of the same dial (the ladder).

| | |
|---|---|
| claim sites with a recoverable ladder | **291** across 39 files (242 of them in LEADERBOARD.md) |
| worst adjacent spacing **>= 2.0x** | **196 (67.4%)** |
| meeting 1461's **<= 15%** spacing bar | **15 (5.2%)** |
| quoting ANY SE / bootstrap / CI | **27 (9.3%)** |
| worst-spacing quartiles (25/50/75/95) | **1.50x / 2.00x / 4.00x / 12.60x** |
| ladders containing a ZERO rung (spacing undefined) | 7 (2.4%) |

By dial (sites / median worst spacing / share >= 2x / share quoting an SE):
`n` 113 / 2.00x / 0.770 / 0.106 · `g` 66 / 1.33x / 0.212 / 0.015 · `H` 40 / 3.14x / 0.900 / 0.175 ·
`k` 32 / 2.00x / 0.844 / 0.031 · `L` 20 / 2.00x / 0.800 / 0.250 · `w` 6 / 2.75x / 0.833 / 0.167 ·
`c` 6 / 2.00x / 0.667 / 0.000 · `phi` 4 / 2.00x / 1.000 / 0.000.

**Census limits, stated not repaired.** The ladder is recovered from the PROSE of the same row, so (i) a claim
whose ladder lives only in its script or CSV is missed, and (ii) **200 of the 291 sites expose only 2 rungs**,
which is a lower bound on their true spacing, not a measurement of it. `H` is the worst-served dial and `g`
the best. Full site list: `.census.csv`.

## (B) CAPITAL ARM — refining the three SHIPPED best-rung claims to <= 15% spacing

F1 `n = 5` (RULES v1 top-n, gross held at 0.75 so n is not a sizing dial), F2 `gross = 0.75` (RULES v2
clause 3), F3 `band = 0.03` (RULES v2 clause 2). Coarse ladders as the record quotes them; refined ladders
`n` = every integer 3..20, `gross` = 0.25·4^(k/10) k=0..10 (1.149x), `band` = 0.01·10^(k/17) k=0..17 (1.145x).
Paired **stationary block bootstrap** (identical resampled dates for every rung, 400 draws, block 21 and 63).

### 1. Refinement RELOCATES the argmax in 3 of 6 cells — and every relocation is noise

| panel | family | coarse argmax | refined argmax | Sharpe gained | paired SE (21/63) | gap/SE | P(gap<=0) |
|---|---|---|---|---|---|---|---|
| U56 | n | 20 | **19** | +0.0140 | 0.1343 / 0.1312 | 0.10 | — |
| U56 | gross | 0.50 | **0.5743** | +0.0000 | 0.0005 / 0.0005 | 0.06 | 0.535 |
| U56 | band | 0.03 | **0.0258** | +0.0035 | 0.0090 / 0.0101 | 0.39 | 0.350 |
| B136 | n | 20 | 20 | 0.0000 | 0.1256 | — | — |
| B136 | gross | 0.75 | 0.75 | 0.0000 | 0.0000 | — | — |
| B136 | band | 0.08 | 0.08 | 0.0000 | 0.0450 | — | — |

The refined argmax is never worth more than **+0.0140 of Sharpe** and never more than **0.39 SE**. The
bootstrap cannot locate the argmax at any spacing: its 5–95 spread on the `n` ladder is **11 of 18 rungs**
(U56) and **15 of 18** (B136), and P(the shipped rung is the argmax) runs 0.000–0.138.
**Refining the ladder does not repair a best-rung claim; it relabels an unresolvable maximum.**

### 2. What IS resolvable is the LEVEL, not the location

The shipped `n = 5` is beaten by the refined argmax by **+0.3468 of Sharpe at 2.58 SE, P(gap<=0) = 0.0025**
(U56; +0.2097 at 1.67 SE on B136) — ideas 953 / 2244 reproduced on an integer-spaced ladder. Sharpe climbs
monotonically in trend from 0.6553 (n=5) to 1.0020 (n=19) on U56.

### 3. The gross ladder is Sharpe-FLAT, so its best-rung claim is empty at ANY spacing

Sharpe across the whole 0.25 -> 1.00 refined ladder spans **0.000205** (U56: 1.2009–1.2011) and **0.000223**
(B136) while CAGR runs 2.85% -> 11.53%. A "best gross rung" scored on Sharpe is an arithmetic artefact.
Gross decides 4b only through the LEVEL bars: **`gross = 1.00` is the sole 4b passer on both panels** (U56
full 11.53% / 1.2009 / -15.91%, OOS 12.67% / 1.2760 / -15.91%; B136 10.63% / 1.0971 / -16.16%, OOS 10.47% /
1.1006 / -16.16%), margin over SPY 2.33 / 1.70 SE. **This is not new** — it is the family already recorded in
`2026-09-22_u56-b136-band008-gross100-tbill-sweep_4b_cloud_MEMO.md`, and on B136 the CAGR floor holds by
0.003 of the 0.70 ratio. No memo is filed on it here.

### 4. A resolution limit the refinement standard cannot meet: `n` is INTEGER-QUANTIZED

The finest legal `n` ladder is step-1, and 3->4 is 33%, 6->7 is 17%: **the <= 15% bar is unattainable below
n = 7**, which is exactly where the shipped claim (`n = 5`) and 113 of the record's 291 census sites live.
1461's refinement standard is inapplicable to a count dial in the region the record argues about.

### 5. Refinement's ONE genuine find, and why it is not a book

Two **off-coarse** band rungs on B136 — `c = 0.02254` and `c = 0.02581` — pass **4a** (Sharpe 1.1106 / 1.1070
vs the live book's 1.0972; H1 1.2357 / 1.2301 vs 1.2296; H2 0.9872 / 0.9856 vs 0.9669; MaxDD -12.21% /
-12.20% vs -12.24%) and are invisible at coarse spacing. But the margin is **+0.0134 / +0.0098 of Sharpe at
1.58 / 1.65 SE (P(margin<=0) = 0.045 / 0.063)**, it is **one panel of two** (no U56 twin), and 4a is not the
path that matters for capital. PARK-worthy as a question, not adoptable.

### 6. PROTOCOL rule 8 — dials chosen on 2009-2016 only, 2017-2026 read once

| panel | family | refined pick -> OOS CAGR / Sharpe / MaxDD | coarse pick -> OOS | shipped -> OOS Sharpe |
|---|---|---|---|---|
| U56 | n | **12** -> 9.27% / 0.8997 / -13.92% | 15 -> 8.59% / 0.8360 / -15.88% | 5 -> 0.7283 |
| U56 | gross | **1.00** -> 12.67% / 1.2760 / -15.91% | 1.00 -> same | 0.75 -> 1.2767 |
| U56 | band | **0.10** -> 9.08% / 1.1945 / -12.35% | 0.08 -> 8.97% / 1.1635 / -14.47% | 0.03 -> 1.2767 |
| B136 | n | **20** -> 7.52% / 0.7292 / -17.40% | 20 -> same | 5 -> 0.5465 |
| B136 | gross | **1.00** -> 10.47% / 1.1006 / -16.16% | 1.00 -> same | 0.75 -> 1.1017 |
| B136 | band | **0.10** -> 8.25% / 1.0887 / -14.58% | 0.08 -> 8.22% / 1.0934 / -14.81% | 0.03 -> 1.1017 |

Comparands OOS: RULES v2 live book **9.46% / 1.2767 / -12.05%** (U56) and **7.85% / 1.1017 / -12.24%** (B136);
SPY **15.29% / 0.8751 / -33.72%** (U56 dates) and **15.26% / 0.8737 / -33.72%** (B136 dates).
Refinement moves the rule-8 pick in **3 of 6** cells — U56 n 15->12 (**+0.0637** of OOS Sharpe), U56 band
0.08->0.10 (**+0.0310**), B136 band 0.08->0.10 (**-0.0047**, i.e. refinement made the chooser WORSE). In none
of the three does the refined chooser reach the live book's OOS Sharpe, and on all 6 cells the chosen rung is
beaten by the live book on Sharpe. **No chooser on any of
these three refined ladders reaches a capital book.**

---

## KEEP paths, both evaluated

- **4a (beat the book):** 2 of 104 refined rungs pass, both B136 band rungs in §5, both held by < 2 SE, neither
  replicating on U56. **FAIL as a candidate.**
- **4b (capital-worthy):** 2 of 104 pass, both `gross = 1.00` (§3) — an already-recorded family, not this
  idea's find. **No new candidate.**

## What this run cannot do (stated, not repaired)

One cadence (weekly, the live book's), one cost rung (10 bps), one rebalance phase (Friday), one execution
delay (t+1), two panels, three dials — the three the live books ship. The census reads PROSE only (see the
limits above). The paired SE is a stationary block bootstrap at two block lengths, not a full re-draw of the
tape. **SURVIVORSHIP (rule 9):** U56 and B136 are current-constituent lists held from 2008, so every absolute
CAGR/Sharpe level is optimistic and both 4b bars are easier than on a point-in-time panel; the WITHIN-LADDER
contrasts this idea turns on are same-tape, same-names and first-order immune, the pass counts are not.

## Residue (rule 6; RULES.md, PROTOCOL.md, scan.py, bot.py, baseline.py untouched)

A publishing note is earned and stated, not enacted: **only 9.3% of the record's 291 best-rung claim sites
quote any SE, and 67.4% sit on a ladder spaced >= 2x — yet this run finds the argmax unresolvable even at
1.15x.** The corrective is not a finer ladder; it is that a best-rung claim should publish the paired SE of
its winner-minus-runner-up gap, because on this tape that gap is between 0.06 and 0.39 SE on 3 of 3 shipped
dials.
