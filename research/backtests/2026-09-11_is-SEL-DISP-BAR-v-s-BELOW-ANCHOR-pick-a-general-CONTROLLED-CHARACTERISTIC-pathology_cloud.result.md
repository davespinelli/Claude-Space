# Idea 715 — is SEL-DISP|v's below-anchor pick a general CONTROLLED-CHARACTERISTIC pathology?

**cloud, 2026-09-11 — ANSWERED / KILL of the "general pathology" reading. No RULES change, no book
promoted, no KEEP claimed; RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py untouched.**

## Answer in one line
**No.** Across all four characteristics the controlled selector out-picks its own anchor in
**8 of 24** cells — below the exact uniform-pick expectation of 13.0 (p = 0.042) but *not*
distinguishable from a within-stratum-permuted version of the same variable (expected 10.3,
p = 0.41), and **21 of the 24 controlled cells sit inside their own permutation band**. The
pathology is **disp-specific**, not general — and where it is real, most of it is the
**within-stratum de-meaning** the control is bundled with, not log(book vol).

## Gates (asserted before any new number was read)
- **G1** — idea 540's 12 published selector rows re-derive from idea 533's `.arms.csv` under this
  run's own fitters: max |Δ| over (q, draw, OOS CAGR/Sharpe/MaxDD, anchor) = **0.000e+00**. The two
  cells the queue names reproduce exactly: top10 SEL-DISP|v **0.3494** vs anchor **0.6451**, top20
  **0.2852** vs **0.6860**.
- **G2** — committed KEEP counts re-derive (4a **0/504**, 4b **41/504**); SPY is one series and is
  constant to 3.3e-16. **CORRECTION TO IDEA 540 (drift recorded, non-raising):** RULES v2 in this
  artefact is *not* a constant — it is re-run on **each panel's own 40 names**, so `base_*` varies
  across the 504 rows (sd 0.2205; OOS Sharpe mean 0.8175, range [0.3116, 1.2253]). Idea 540's
  console printed `RULES v2 OOS +0.0792/1.0616/-0.1141` as *the* comparand; that is row 0's panel
  (q=0.00, draw=0) alone and sits at the **85.1st percentile** of the 504. Its per-row `beats_v2`
  flags are unaffected (they used each row's own base); only the header line is. This run quotes
  RULES v2 per row and as a distribution, never as a scalar.
- **G3** — **fresh rebuild**: six of the 168 panels were re-drawn from today's price files (seed
  20260909 replayed; 44 `max_1d_move >= 1.0` names dropped first, 439 usable small caps, 100
  large-cap stocks) and re-backtested. Max |Δ| on the IS window over 18 rebuilt books =
  **2.220e-16** — the committed ladder reproduces bit-for-bit on today's vintage.

## Design (2 tuned parameters, all 96 grid points published)
4 characteristics {breadth, disp, corr, evol} × 4 transforms {none, dm, residx, ratio} × 2
directions {argmax, argmin} × 3 arms {EWall, top10, top20}, each an **IS-only selector**
(≤ 2016-12-31) over idea 295's 168-panel MIX ladder, read **once** on the untouched OOS window.
`dm` = within-stratum de-mean only; `residx` = idea 540's control verbatim (FWL residue on
log IS book vol); `ratio` = x / bookvol_IS. Arm, direction and the 21-stratum resolution are
inherited reported axes, not tuned.

## The two nulls (this is what decides it)
| null | what it is | beat-anchor rate |
|---|---|---|
| EXACT | the arm's own 168 OOS Sharpes — the complete uniform-pick distribution, no sampling | EWall 0.5417 / top10 0.5357 / top20 0.5536 (mean **0.5436**) |
| PERM | characteristic permuted **within stratum** 200× (seed 715), every selector re-run | none 0.5133 / dm 0.4383 / residx 0.4294 / ratio 0.4933 |

Note the permutation means (0.60 overall) sit **below** the mean anchor (0.6628): argmax/argmin of
*any* variable, structureless or not, lands in the extreme-q strata, which carry the low OOS
Sharpes. Within-stratum permutation preserves that stratum location and therefore cannot see it —
so the **exact uniform-pick null is the demanding comparand**, and "below anchor" is by itself a
stratum-location statement, not evidence about the characteristic.

## Results
| transform | cells | beat anchor | mean pct | mean OOS Sharpe | in own band | beat v2 | beat SPY | 4b |
|---|---|---|---|---|---|---|---|---|
| none   | 24 | 14 | 0.4268 | 0.5437 | 24/24 | 4 | 5 | 1 |
| dm     | 24 |  9 | 0.3378 | 0.4830 | 24/24 | 0 | 2 | 0 |
| residx | 24 |  **8** | 0.3130 | 0.4611 | **21/24** | 0 | 2 | 0 |
| ratio  | 24 | 14 | 0.4549 | 0.5797 | 20/24 | 2 | 7 | 3 |

By characteristic (24 cells each): breadth 13, disp 13, corr 12, **evol 7** beat the anchor.

**Only 6 of 96 cells separate from their own permutation null at p<0.05 (4.8 expected at chance).**
Two of them are the queue's own cells and they are extreme: top10 disp|residx+ **0.3494** vs band
[0.6096, 0.9925] and top20 disp|residx+ **0.2852** vs [0.8378, 1.0812], both p = 0.0000 (0 of 200
draws) — the only cells in the file that clear Bonferroni over 96 (5.2e-4). **The one controlled
cell that separates *upward* is top20 breadth|residx+ (0.9338 vs [0.2118, 0.8842], p = 0.02)**,
which does not clear Bonferroni. So: a controlled characteristic *does* occasionally out-pick its
anchor, but never more often than chance across the family.

**Where the damage actually comes from** (24 paired cells, same char/direction/arm):
- control vs raw: mean Δ OOS Sharpe **−0.0826**, median −0.0496, helps in 7 of 24
- control vs de-meaning: mean Δ **−0.0219**, median **+0.0000**, helps in 4 of 24

i.e. roughly **three quarters of "the control inverts the ranking" is the within-stratum
de-meaning**, not log(book vol). Idea 540's single `residx` rung could not separate the two.

## Rule 8 walk-forward and both KEEP paths
Every selector is IS-built and OOS-read once. SPY OOS **+15.45% / 0.8820 / −33.72%**; RULES v2 is
per-panel (OOS Sharpe mean 0.8175, CAGR +6.33%, MaxDD −13.50%) and each pick is judged against
RULES v2 **on its own panel**.

- over the 96 selectors: beat the anchor **45 (46.9%)** vs exact null 54.4% (p = 0.15); mean
  percentile **0.383**; **55 of 96 picks land below their arm's median**; beat RULES v2 **6**,
  beat SPY **16**
- **KEEP 4a 0/96. KEEP 4b 4/96 (4.2%) — BELOW the corpus base rate 41/504 (8.1%).**
- the ANCHOR rows themselves beat RULES v2 0/3 and SPY 0/3; the record's own SEL-S beats the anchor
  3/3 but RULES v2 0/3, SPY 1/3, 4b 1/3
- best single cell: top10 evol|ratio− → OOS **+14.84% / 1.0539 / −18.99%** (4b pass), against SPY
  +15.45% / 0.8820 / −33.72% — one cell of 96, lower CAGR than SPY, and not proposed as anything.

**VERDICT: KILL** of the general-pathology reading. The controlled-selector family under-picks its
anchor, but inside its own null; no controlled characteristic reliably out-picks its anchor; 4a is
0 and 4b is below the corpus base rate. Nothing here is a capital candidate.

## Caveats
SURVIVORSHIP (idea 54, `data/SMALL_PANEL_README.md`): the small-cap end of the q ladder is the
**current-constituent** sub-$2B screen (44 `max_1d_move >= 1.0` names dropped first) and the
large-cap end the **current** 136-name broad list, so every level inherited here is optimistic. The
claims above are within-ladder rankings against an anchor and a permutation band, not level claims.
The permutation is within-stratum and therefore blind to stratum location (see above). The 168
panels share names across draws, so the cells are not independent — the Bonferroni bar quoted is
conservative on the family size and anti-conservative on the dependence.

Artefacts: `.selectors.csv` (96+6 rows) `.permutation.csv` (96) `.pairs.csv` (24) `.walkforward.csv`
`.keeppaths.csv` `.gate3.csv` `.console.txt`
