# Idea 380 — the SCORED vs PRICED denominator is a 5-point sign-stability gap

**Lane B, 2026-09-07.** Script `2026-09-07_the-SCORED-vs-PRICED-denominator_B.py` (2076 s,
deterministic, 8 seeds × 2 panels × 40 draws × 2 conventions × 16 arms = 20,480 priced draws).

## VERDICT: **ANSWERED — the premise is CONFIRMED (98.3% denominator, 1.7% seed), but the
## defect is made entirely of UNPRICEABLE draws, and idea 382's already-filed floor closes it
## EXACTLY. No rules change; no KEEP (4a 14/96 and 4b 10/96, all artefacts — see §5).**

---

## Gates (7/8; the one miss is itself the finding)

| gate | value | tol | |
|---|---|---|---|
| G1a `H.run` == `engine.backtest` RETURNS @0/25 bps, both books, both panels | 0.000e+00 | 1e-12 | PASS |
| G1b same, TURNOVER | 0.000e+00 | 1e-12 | PASS |
| G2 PRICED book == idea 94 `H.targets(px,"EWall")` | 0.000e+00 | 1e-15 | PASS |
| G3a idea 380's filed `max\|dw\| = 0.0150` | 0.000e+00 | 1e-4 | PASS |
| G3b idea 380's filed 1530 of 4439 disagreeing u56 eval days | 0.000e+00 | 0 | PASS |
| G4 reproduce `_B2`'s committed d3 (SCORED ALL) at ITS seed 20260905 | **2.500e-02** | 1e-12 | **FAIL** |
| G5 reproduce `_B`'s committed d3 (PRICED ALL) at ITS seed 20260907 | 0.000e+00 | 1e-12 | PASS |
| G_CLS audit classifier vs 6 hand-established files | 0 misses | 0 | PASS |

**G4's miss is not a pipeline difference.** It is *one* cell of 64 — `(B136, ebud-0.20)` — and
one net draw of 40. The two implementations' SCORED weight matrices are **bit-identical** on
both full panels (max |dw| 0.000e+00 vs `_B2`'s own `_topw`), and on that cell all 40 draws
agree on dMaxDD to **5.55e-14**. What differs is the *sign* of five draws whose |dMaxDD| is
≈ 1.1e-14 — i.e. an arm with no drawdown effect at all. **All 40 draws of that cell are
sub-floor** (|dMaxDD| ≤ 0.10 pp). This is idea 382's priceability failure reproduced
independently, on a statistic that does not exist.

---

## 1. THE AUDIT (the deliverable the queue asked for)

327 committed python files scanned; **69 build an all-names book** (96 construction sites),
classified site-level by a pre-registered source classifier gated 6/6 against hand-established
files.

| convention | files | sites |
|---|---|---|
| **PRICED** (`px.notna()`, weight `gross/#priced`) | **52** | 72 |
| SCORED (`composite.notna()`, weight `gross/#scored`) | 3 | 3 |
| BOTH (one file carries each) | 1 | 3 |
| UNRESOLVED (reported, not guessed) | 13 | 18 |

**Of the 56 files the classifier resolves, 52 (92.9%) are PRICED.** The entire SCORED
population is four files: `2026-09-06_can-a-panel-property-choose-the-cadence_cloud.py`,
`2026-09-07_book-size-floor-INSTRUMENT-CLASS-replication_cloud.py`,
`2026-09-07_breadth-adaptive-count-2022_B.py`, and idea 124's `_B2` run (BOTH).

Mapped onto the 3,116 parsed LEADERBOARD rows: **396 rows sit on a PRICED all-names book, 48
on a SCORED or mixed one**, 184 on an unresolved script, 2,459 on scripts that build no
all-names book. **`research/baseline.py: rules_v2_weights` — the LIVE book — is PRICED**, and
this run reproduces it to the last digit from the PRICED construction (§4).

So the record does not have two competing conventions in any balanced sense. It has one
convention used by 92.9% of files and 89% of attributable rows, and a four-file minority — one
of which produced the disputed number.

## 2. THE CAUSAL TEST — the archive's contrast was confounded; the finding survives anyway

Idea 382 established that the two archived runs do **not** share a seed (`_B` 20260907,
`_B2` 20260905), so the queue's "on IDENTICAL bootstrap draws" is false and seed and
convention moved together in the archive. Broken here with a 2×2 plus a seed panel: one
pipeline, one arm set, both conventions on the **same draw index** at each of 8 seeds.

**mean D3 `frac_pos_full`, as the record computes it**

| panel | matched-seed gap (SCORED − PRICED) |
|---|---|
| u56, 8 seeds | +0.0312 … +0.0687 |
| B136, 8 seeds | +0.0500 … +0.0625 |
| **pooled** | **+0.0507 ± 0.0046, t = +31.0, 8/8 positive** |

Across-seed SD *within* a convention: PRICED 0.0024, SCORED 0.0040. The archived confounded
contrast (SCORED@20260905 − PRICED@20260907) is **+0.0516**, of which the **denominator
explains +0.0507 (98.3%)** and the seed +0.0009 (1.7%).

- **H1 (denominator effect): RETAINED.**
- **H0 (seed artefact): NOT RETAINED** — +0.0516 is far outside ±3 within-convention seed SD
  (±0.0120).

**The queue's premise is confirmed.** Its stated mechanism ("identical draws") was wrong; its
conclusion was right.

## 3. WHAT THE GAP IS ACTUALLY MADE OF — and why the record already voted for the fix

Recomputing D3 under **idea 382's committed amendment** (count only draws clearing idea 94's
0.10 pp floor):

| | matched-seed gap |
|---|---|
| as the record computes it | +0.0507 ± 0.0046 |
| **floored (idea 382's amendment)** | **exactly 0.0000 at all 16 (panel, seed) cells** |

On the 10,240 matched draw-pairs:

- median between-convention |ΔdMaxDD| = **4.44e-14** — the two conventions price every
  instrument identically to machine epsilon;
- **519 pairs (5.07%) disagree in sign**;
- **0 of the 8,849 pairs where both conventions clear the floor disagree in sign** (13.6% of
  pairs are sub-floor).

**Every sign disagreement between the two conventions lives in a draw where |dMaxDD| is
numerically zero.** The 5-point gap is real and is caused by the denominator, but it is not a
disagreement about drawdown — it is 519 coin-flips on undefined statistics. The record does
not need to pick a convention to close this gap; it needs the floor it already amended in.

## 4. THE PRICE — what the convention is worth in return space

Every one of 96 cells reported (2 conventions × 2 gate forms × 4 gross × 3 cost rungs × 2
panels).

| panel | median \|ΔSharpe\| | max | median \|ΔCAGR\| | sign |
|---|---|---|---|---|
| u56 | 0.00369 | 0.00426 | 0.053 pp | 12+ / 12− |
| B136 | 0.00215 | 0.00267 | 0.036 pp | 12+ / 12− |

**The sign is form-dependent, not universal:** SCORED helps the band3-gated (live) form
(+0.0032 u56 / +0.0017 B136) and hurts the ungated form (−0.0042 / −0.0026), at every gross and
every cost rung.

**The live book, exactly** (PRICED band3-dg at gross 0.75 == `rules_v2_weights`, reproduced to
the last digit):

| panel | book | CAGR | Sharpe | MaxDD | H1/H2 | OOS Sharpe |
|---|---|---|---|---|---|---|
| u56 | PRICED (= live v2) | 8.66% | 1.2056 | −12.05% | 1.2259/1.1908 | 1.2851 |
| u56 | SCORED | 8.72% | 1.2088 | −12.05% | 1.2306/1.1924 | 1.2863 |
| B136 | PRICED (= live v2) | 8.03% | 1.1058 | −12.24% | 1.2291/0.9844 | 1.1185 |
| B136 | SCORED | 8.08% | 1.1075 | −12.33% | 1.2325/0.9839 | **1.1177** |

Switching the live book's denominator buys +0.0032 Sharpe on u56 and **loses** OOS Sharpe and
MaxDD on B136. Not a rules change.

## 5. KEEP PATHS — 4a 14/96, 4b 10/96, and both are artefacts

| cost | 4a | 4b |
|---|---|---|
| 0 bps | 4/32 | 4/32 |
| 10 bps | 5/32 | 4/32 |
| 25 bps | 5/32 | 2/32 |

- **4a: 14 of 48 SCORED cells pass; 0 of 48 PRICED cells do.** Every passer is the band3 live
  form at gross ≤ 0.75, on both panels. The margin that carries them over the line is the
  +0.0032/+0.0017 of §4 — i.e. **an unnamed convention worth ~0.003 Sharpe moves 14 cells
  across the 4a bar**, which is the strongest argument in this run for naming one. But the
  passes themselves are the gross dial plus PROTOCOL 4a's MaxDD clause: the g=0.375 cell is the
  live book at half gross (CAGR 4.33% vs 8.66%, MaxDD −6.12% vs −12.05%, Sharpe unchanged to
  three decimals). This is exactly the failure mode PROTOCOL rule 4b was added on Sep 4 to
  correct — all 14 miss 4b's CAGR floor (0.70 × SPY = 10.66%) by more than half.
- **4b: 10 passers, 5 PRICED / 5 SCORED**, all at gross 1.00 on the band3 live form, all
  re-measurements of filed objects. The denominator does not separate them.

**No KEEP-candidate is proposed.** A memo is filed (`.memo.md`) with exact RULES wording for
the 4a by-product and an explicit recommendation **against** adoption.

## 6. RULE 8 — (convention, gross) chosen on IS ≤ 2016, evaluated 2017–2026

12 picks (2 panels × 2 forms × 3 cost rungs). The IS chooser picks **SCORED 9/12, PRICED 3/12**
— it does not stably prefer either. Gross goes to 1.00 at every point (a grid edge, flagged).

| | OOS Sharpe | OOS CAGR | OOS MaxDD |
|---|---|---|---|
| picks (u56 band3 @10 bps) | 1.2856 | 12.82% | −15.91% |
| picks (B136 band3 @10 bps) | 1.1165 | 10.68% | −16.27% |
| RULES v2 OOS (u56 / B136 @10 bps) | 1.2851 / 1.1185 | 9.53% / 7.98% | −12.05% / −12.24% |
| SPY OOS | 0.8820 | 15.45% | −33.72% |

**Picks above SPY OOS Sharpe 12/12; above RULES v2 OOS Sharpe 4/12.** The OOS cost of choosing
the wrong convention is **median 0.0018 Sharpe, max 0.0094** — the walk-forward says the choice
is nearly free out of sample, which is the other half of the case for simply naming one.

## 7. THE PROPOSAL

1. **Name PRICED the record's single all-names denominator.** `indicator = px.notna()`,
   `weight = gross / #priced`. It is already what 92.9% of resolvable files, 396 of 444
   attributable LEADERBOARD rows, and the LIVE `rules_v2_weights` use. Naming SCORED instead
   would require re-pricing 396 rows to buy ≤0.004 of Sharpe whose sign flips with the gate
   form.
2. **Keep idea 382's floor amendment — it, not the convention, is what closes the D3 gap**
   (exactly 0.0000 at 16/16 cells; 0 of 8,849 priceable pairs disagree). Naming a convention
   alone would hide the gap by removing the comparison; the floor removes the *cause*.
3. **Add a `denom` column** naming the convention (`priced` / `scored`) on any LEADERBOARD row
   quoting an all-names book, and re-tag the 48 SCORED-or-mixed rows in place.
4. The four SCORED files are listed by name in §1 and in `.audit.csv` for whoever re-prices
   them.

## Files

`.py` `.console.txt` `.bootstrap.csv` (20,480 draws) `.d3.csv` (512 cells) `.grid.csv`
(96 cells) `.walkforward.csv` `.live.csv` `.audit.csv` `.audit_rows.csv` `.gates.csv` `.memo.md`
