# Idea 400 — census the record's ABSOLUTE thresholds for the firing-RATE artefact

**INDEPENDENT CONCURRENT RUN, filed as such and NOT as a claim.** Lane B claimed idea 400 on the same day (`[CLAIMED 2026-09-10, lane B]` in QUEUE.md's In-progress section); this cloud run was written and executed without sight of it and its claim line is left standing. Filed under `_cloud` per the record's convention for concurrent runs (ideas 320R, 457). A concordance check against lane B's numbers is owed once both are committed.

**Cloud lane, 2026-09-10.  Verdict: SPLIT — the census is DELIVERED, idea 336's DIAGNOSIS
generalises (pooled RATE SHARE 0.619 full / 0.572 OOS over 96 panel-dependent cells), and the
queue's proposed BAR is REFUTED as stated on two counts: (i) it is not a majority verdict — only
7 of 16 non-degenerate panel-dependent instruments exceed idea 336's median published spread
(0.413), and the count swings to 11/16 at its loosest (0.193) and 2/16 at its tightest (0.686),
so "idea 336's ABS spread" names three different bars; (ii) an ABSOLUTE-spread bar is itself
scale-dependent and systematically clears the rarely-firing instruments — the record's single
most-cited absolute cut, `vol20 < 0.60` (81 of 92 AST threshold hits), has a spread of 0.036 and
a firing-rate RATIO of 7.5x.  No RULES change; no book promoted; ONE 4b passer PARKed with a memo.
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py untouched.**

## Gates (all PASS, run before anything was measured)

| gate | what it checks | result |
|---|---|---|
| G1 | vectorised Runner vs `engine.backtest`, 2 books | max abs return diff **1.39e-17** |
| G2 | the sd-weighted CORR identity vs a BRUTE-FORCE pairwise correlation matrix, 3 panels × 6 dates | **3.00e-15 / 7.66e-15 / 5.00e-16** |
| G3 | SPYTR panel-invariance (the H_INVAR premise, measured not assumed) | max abs diff **6.77e-05** over 4194 common days |
| G4 | census machinery: provenance disjoint, no malformed hits | AST 100 hits / 59 scripts, TEXT 141 / 124 rows, **PASS** |
| G5 | the decomposition identity dTOTAL ≡ dRATE + dFORM on all 450 rows | full **1.11e-16**, OOS **1.11e-16** |

**G2 is the gate that makes CORR a measurement.**  Mean pairwise correlation on a 439-name panel
is not computable day by day, so CORR is the sd-weighted average correlation via
`rho_w = (Var(Σr) − Σvar) / ((Σsd)² − Σvar)`, computed on the names with complete history and only
on windows with no missing cell — under which the identity is exact, as the brute force confirms.
(The *unweighted* mean differs by 0.028–0.117; that difference is reported, not hidden.)

**G3 is a small correction to the record.**  SPYTR is panel-invariant by definition but is *not*
bit-identical across the record's panels: U56 reads SPY from `data/prices.csv`, B136 from the
separately cached `data/prices_broad.csv`, and SMALL439 from `prices.csv` REINDEXED onto the small
panel's own calendar, so its 200d mean is taken over a different day set.  Max abs difference in
the SPY LEVEL itself is 5.10e-03.  It is far too small to move a firing rate, which is what
H_INVAR needs, and it is the same cache-vintage exposure idea 353 flagged for `prices_broad.csv`.

## PART 1 — the census, in three tiers

Two readings (tuned parameter 1).  **AST**: walk every one of the 538 committed scripts and record
every `Compare` whose left operand names a census statistic and whose right operand is a numeric
literal.  **TEXT**: the queue's literal instruction, a scan of the committed LEADERBOARD rows.

| reading | THRESHOLD-kind hits | TIER 0 (word) | TIER 1 (token-exact) | TIER 2 (+ in range) |
|---|---|---|---|---|
| AST | 92 | 92 | **88** | **88** |
| TEXT | 131 | 131 | 131 | **62** |

Per statistic, AST TIER 2: **VOL20 81** (thresholds 0.40, 0.60), **CORR 2** (0.20, 0.50),
**BREADTH 4** (0.48, 0.50, 0.68), **DISP 1** (0.50), **SPYTR 0**.

Two things the tiers buy:

1. **TIER 0 → TIER 1 removes 4 AST hits, all the same false positive**: `d.t_correct.abs() > 2.0`,
   `d.p_correct < 0.05` and two more in one file — the word "corr" inside "correct".  A census done
   by eye makes exactly this mistake, and it makes it on the loosest of the four vocabularies.
2. **TIER 1 → TIER 2 removes 69 of the TEXT reading's 131 hits (53%)** because the literal is
   outside the statistic's own range — a text scan cannot tell a threshold from a reported value,
   and it picked up correlations of 0.999988, −0.1601 and 1.0 as if they were cuts.

**Honest upper bound, stated as the record has forced on earlier censuses (ideas 276/286/523):
even TIER 2 counts a NAME, not an INSTRUMENT.**  A comparison is an instrument only if its result
gates a weight, which no name match can establish.  88 is an upper bound on the number of
committed absolute-cut comparisons on a panel-dependent statistic, not a count of gates.

**The record's absolute-threshold habit is one number, not four.**  81 of the 92 AST threshold hits
are `vol20 < 0.60` (RULES v1's `max_vol`) or `< 0.40`.  The queue names four statistics; the record
has cut three of them absolutely a total of **7** times.

## PART 2 — realised firing rates and their cross-panel spread

Priced ladder = TIER-2 census thresholds ∪ a pre-registered default ladder, provenance printed per
value.  Risk-off direction pre-registered, never tuned: BREADTH low, DISP high, VOL20 high, CORR
high, SPYTR low.  RATECONV (tuned parameter 2) changes nothing material — every spread below moves
by less than 0.007 between `daily` and `rebal`.

| statistic | thr | U56 | B136 | SMALL439 | SPREAD | RATIO | > 0.193 / 0.413 / 0.686 |
|---|---|---|---|---|---|---|---|
| BREADTH | 0.30 | 0.065 | 0.060 | 0.120 | 0.060 | 2.0 | . . . |
| BREADTH | 0.48 | 0.150 | 0.135 | 0.431 | 0.296 | 3.2 | X . . |
| BREADTH | 0.50 | 0.157 | 0.144 | 0.478 | 0.334 | 3.3 | X . . |
| BREADTH | 0.60 | 0.213 | 0.209 | 0.754 | **0.545** | 3.6 | X X . |
| BREADTH | 0.68 | 0.309 | 0.312 | 0.834 | **0.524** | 2.7 | X X . |
| VOL20 | 0.20 | 0.382 | 0.513 | 1.000 | **0.618** | 2.6 | X X . |
| VOL20 | 0.25 | 0.175 | 0.255 | 0.995 | **0.821** | 5.7 | X X X |
| VOL20 | 0.30 | 0.099 | 0.133 | 0.883 | **0.784** | 8.9 | X X X |
| VOL20 | 0.40 | 0.030 | 0.034 | 0.401 | 0.371 | 13.3 | X . . |
| **VOL20** | **0.60** | 0.006 | 0.007 | 0.042 | **0.036** | **7.5** | . . . |
| CORR | 0.20 | 0.854 | 0.811 | 0.232 | **0.622** | 3.7 | X X . |
| CORR | 0.30 | 0.503 | 0.556 | 0.068 | **0.488** | 8.1 | X X . |
| CORR | 0.40 | 0.227 | 0.243 | 0.027 | 0.215 | 8.9 | X . . |
| CORR | 0.50 | 0.116 | 0.126 | 0.000 | 0.126 | ∞ | . . . |
| SPYTR (invariant) | −0.05 … 0.10 | — | — | — | **0.010–0.018** | 1.02–1.11 | . . . |
| DISP (all 5 rungs) | — | 0/1 | 0/1 | 0/1 | 0.000–0.005 | — | DEGENERATE |

Counts, non-degenerate panel-dependent instruments (16 of 21; the 5 DISP rungs fire at the same
extreme on every panel and carry no cross-panel contrast to price):
**> 0.193: 11/16.  > 0.413: 7/16.  > 0.686: 2/16.**  Panel-invariant: **0/4 at every bar.**

Three findings the table forces:

1. **H_SPREAD FAILS as pre-registered, and the queue's bar is three bars.**  "Exceeds idea 336's
   ABS spread" is a majority verdict at 0.193, a minority verdict at 0.413 and a rarity at 0.686 —
   and idea 336 published all three.  The flag is not well defined until the record picks one; this
   run reports all three rather than picking.
2. **An ABSOLUTE-spread bar is scale-dependent, and the RATIO column is why.**  `vol20 < 0.60`, the
   record's most-cited absolute cut, has a spread of **0.036** — clearing every one of idea 336's
   bars — and a **7.5× ratio**: the small-cap panel's book is de-grossed seven times as often as
   the mega-cap panel's.  An absolute-spread bar systematically clears the rarely-firing
   instruments, which are exactly the ones whose cross-panel *counts* are most fragile.  Both
   columns are reported; neither is proposed as THE bar.
3. **H_INVAR PASSES: a word-level census over-counts.**  The four SPYTR rungs have spreads
   0.010–0.018 against a non-degenerate panel-dependent median of 0.352, and G3 shows the series
   itself differs by at most 6.8e-05 across panels.  4 of the 25 priced rungs here are not
   artefacts and never could be; a census that counts the word counts them.
4. **The record has no usable absolute DISP threshold at all.**  Its only committed one (0.50) fires
   on 0% of days on every panel, and the pre-registered default ladder (0.010–0.030) fires on
   ~100% — the cross-sectional sd of 20-day returns simply does not live there.  Reported as
   degenerate, not re-tuned (that would be a third parameter).

## PART 3 — re-pricing: does the flag matter?

ABS = the EW panel de-grossed to cash on risk-off days.  QUANT = the record's causal
rolling-quantile form at nominal q = the ABS instrument's cross-panel MEAN rate.  ABSMATCH = a
full-sample absolute threshold hitting QUANT's realised rate — it carries look-ahead in the rate
BY CONSTRUCTION and is a **control only, never a candidate**, exactly as idea 336 filed it.
dRATE = ABSMATCH − ABS, dFORM = QUANT − ABSMATCH, and G5 asserts dTOTAL = dRATE + dFORM.

The twin does equalise the rate: **median ABS spread 0.126 → median QUANT spread 0.026** (idea 336:
0.193/0.413/0.686 → 0.002/0.015/0.007).

| Sharpe | panel | n | mean dTOTAL | mean dRATE | mean dFORM | **RATE SHARE** |
|---|---|---|---|---|---|---|
| full | U56 | 32 | +0.0515 | −0.0096 | +0.0611 | 0.527 |
| full | B136 | 32 | +0.0297 | +0.0143 | +0.0154 | 0.605 |
| full | SMALL439 | 32 | +0.0686 | +0.0275 | +0.0227 | **0.696** |
| OOS | U56 | 32 | +0.0525 | −0.0145 | +0.0670 | 0.415 |
| OOS | B136 | 32 | +0.0530 | +0.0315 | +0.0216 | 0.580 |
| OOS | SMALL439 | 32 | −0.0070 | −0.0344 | +0.0170 | **0.669** |

**Pooled: 0.619 full / 0.572 OOS over 96 panel-dependent cells.  H_RATE PASSES, but weaker and
better-bounded than idea 336's single cell.**  Idea 336's 0.835 / 0.857 was one statistic
(BREADTH) on one panel (SMALL484); generalised over four statistics and three panels the rate term
still carries the majority, and it carries it most on the small-cap panel (0.70 / 0.67) and least
on U56 (0.53 / 0.42).  **The artefact is real and it is a SMALL-CAP-PANEL problem first.**

## PART 4 — both KEEP paths (PROTOCOL rule 4) and rule 8

The ungated parent is reported first, because idea 336 found 42 of its own 50 4b passes were
inherited from it.  **Here it fails 4b on every panel and both gross levels** (U56 g=1.00
17.69% / 1.1221 / −29.18%; the DD cap is −20.23%), so **0 of the 52 gate 4b passes are inherited** —
every one is bought by the gate cutting drawdown.

| arm | grid books | 4a | 4b | BOTH | inherited 4b |
|---|---|---|---|---|---|
| ABS | 150 | **2** | 19 | 0 | 0 |
| QUANT | 150 | 0 | 33 | 0 | 0 |
| ABSMATCH (look-ahead control) | 150 | 0 | 13 | 0 | 0 |

**The two 4a passes are the artefact itself, caught in the act.**  Both are SMALL439 BREADTH at
0.68, firing on **83.4% of days** — CAGR 3.4% / 4.5%, Sharpe 0.696, MaxDD −6.8% / −9.1%.  They clear
4a only because SMALL439's live RULES v2 is weak (0.5725), and they are a panel held five-sixths in
cash.  This is idea 336's "a panel held 84% in cash, not the gate disagreeing with the panel",
reproduced independently on a different statistic ladder.  **Neither is proposed for anything.**

Rule 8 ((threshold, gross) chosen on 2009–2016 Sharpe alone, 2017–2026 read once), 30 picks:
**4a 0/30, 4b 4/30.**  With the episode count beside the rate — the number of independent risk-off
runs the drawdown leg actually rests on:

| pick | rate (episodes) | full CAGR / Sharpe / MaxDD | H1 / H2 | OOS CAGR / Sharpe / MaxDD |
|---|---|---|---|---|
| U56 VOL20 ABS 0.30 g=1.00 | 0.099 (**25**) | 14.92% / 1.1787 / −17.91% | 1.298 / 1.074 | 15.03% / 1.1686 / −17.91% |
| **B136 BREADTH QUANT 0.40 g=1.00** | 0.124 (**37**) | 15.79% / 1.1630 / −20.02% | 1.210 / 1.128 | 14.17% / **1.2583** / −14.80% |
| B136 VOL20 QUANT 0.60 g=1.00 | 0.015 (**5**) | 18.28% / 1.1722 / −20.02% | 1.233 / 1.108 | 17.42% / 1.2023 / −19.44% |
| B136 CORR QUANT 0.60 g=1.00 | 0.019 (**11**) | 18.52% / 1.1945 / −20.02% | 1.216 / 1.172 | 18.58% / 1.2621 / −19.44% |

against **RULES v2** (U56 8.63% / 1.2021 / −12.05%, OOS Sharpe 1.2788; B136 8.03% / 1.1058 /
−12.24%, OOS 1.1185; SMALL439 3.81% / 0.5725, OOS 0.5680) and **SPY** (U56 15.15% / 0.8855 /
−33.72%, OOS 0.8758; B136 15.23% / 0.8890, OOS 0.8820).

Only one of the four survives its own episode count: **B136 BREADTH-QUANT q≈0.124 at g=1.00, 37
episodes, OOS Sharpe 1.2583 against RULES v2's 1.1185 and SPY's 0.8820.**  It is **PARKED, not
promoted** — see `..._cloud.memo.md` — for three reasons stated in full there: it clears the 4b
drawdown cap by **0.21 pp**, B136 is a current-constituent panel whose survivorship bias inflates
the CAGR leg it also passes, and idea 336 already priced this exact family and found the quantile
form *worse* than the absolute form under the identical chooser on both large panels.  The other
three fire on 5–25 episodes and are reported for the record, not proposed.

## Reference levels (survivorship: B136 and SMALL439 are CURRENT constituents; LEVELS biased up)

| panel | SPY CAGR / Sharpe / MaxDD | RULES v2 CAGR / Sharpe / MaxDD | SPY OOS Sharpe | v2 OOS Sharpe |
|---|---|---|---|---|
| U56 | 15.15% / 0.886 / −33.72% | 8.63% / 1.202 / −12.05% | 0.876 | 1.279 |
| B136 | 15.23% / 0.889 / −33.72% | 8.03% / 1.106 / −12.24% | 0.882 | 1.119 |
| SMALL439 | 14.13% / 0.862 / −33.72% | 3.81% / 0.572 / −14.68% | 0.882 | 0.568 |

## What this is worth to the record

1. **The census exists, and it is small.**  88 TIER-2 AST hits, of which **81 are one number**
   (`vol20 < 0.60/0.40`).  Across the four statistics the queue names, the record has cut a
   panel-dependent statistic absolutely **7** times outside the vol filter.  The rate-artefact
   exposure is narrow, not endemic.
2. **The queue's flag needs a unit and a denominator before it can be used.**  Idea 336 published
   three ABS spreads; "exceeds idea 336's ABS spread" is a different rule at each, and the answer
   swings 11/16 → 7/16 → 2/16.  Per idea 520's ask, a bar needs its unit stated.  This run does
   not adopt one.
3. **Publish the RATIO beside the SPREAD.**  An absolute-spread bar clears every rarely-firing
   instrument by construction, including the record's most-cited one at a 7.5× ratio.  The two
   columns disagree in rank order and the record should carry both.
4. **A word-level instrument census over-counts twice over.**  The naive word match catches
   `t_correct`; the text reading admits 53% out-of-range literals; and the panel-INVARIANT SPY
   family (0/4 above any bar) is counted as an artefact by any census that matches on the word.
5. **Idea 336's diagnosis generalises, with a location.**  RATE SHARE 0.619 full / 0.572 OOS
   pooled, but 0.70 / 0.67 on SMALL439 against 0.53 / 0.42 on U56.  Any future cross-panel claim
   whose instrument is an absolute cut should be re-priced **on the small-cap panel first**.

Outputs: `.console.txt` `.census.csv` `.rates.csv` `.decomp.csv` `.grid.csv` `.walkforward.csv`
`.keeppaths.csv` `.memo.md`
