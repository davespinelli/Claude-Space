# Idea 462 — is the gate-vs-ranked ORDERING SPLIT a GROSS fact?  **KILL (of the gross hypothesis)**

**Answer: no, and the Sharpe leg of the split is provably untouchable by exposure.**
Idea 460's split survives matching the two families on gross in BOTH directions; what moves
is the CAGR leg only, and that is the leg a gross change must move by construction.

## Reproduction (G4, asserted in code)
The NATIVE arm returns idea 460's published counts number for number: gate **16/16**,
ranked **6/28**, all **22/44**, pairwise flips **34/132**, IS→OOS ordering stability raw
1/11 / excess 5/11. Gates G1–G3b also pass (engine twin 1.4e-17 returns / 2.0e-16 turnover;
`dg_weights(BAND3,0.75)` is `baseline.rules_v2_weights` exactly; EW_ALL gross 0.75; the
re-spread construction is gross-0.75 on every day with an admitted name).

## The confound is real and both matchings close it
Realised gross, native: gate **0.381–0.544**, ranked **0.726–0.750** (gap 0.19–0.37).
RESPREAD (gate books re-spread to g/n_admitted) closes it to **≤0.024**; SCALARLO (ranked
books and EW_ALL times a constant k = 0.553–0.808 fitted on IS ≤2016 only) closes it to
**≤0.033**. Neither variant levers: the remainder sits in cash.

## Headline: full-ordering survival (44 per variant)

| variant | GATE | RANKED | gap |
|---|---|---|---|
| NATIVE (= idea 460) | 16/16 (100.0%) | 6/28 (21.4%) | 78.6 pp |
| RESPREAD (matched UP) | 12/16 (75.0%) | 6/28 (21.4%) | 53.6 pp |
| SCALARLO (matched DOWN) | 11/16 (68.8%) | 2/28 (7.1%) | 61.6 pp |

Split by metric, which is where the whole result sits:

| variant | Sharpe gate | Sharpe ranked | CAGR gate | CAGR ranked |
|---|---|---|---|---|
| NATIVE | 8/8 | 2/14 | 8/8 | 4/14 |
| RESPREAD | 8/8 | 2/14 | 4/8 | 4/14 |
| SCALARLO | 8/8 | 2/14 | 3/8 | 0/14 |

**Under Sharpe the split is invariant to gross — identically 8/8 vs 2/14 in all three
variants, at both 10 and 25 bps.** Every point of movement is CAGR.

## Why, mechanically (measured, not asserted)
A scalar gross match scales the return stream, so with cash at 0% it is Sharpe-neutral up to
the cost term and compounding drift: over 48 rescaled arms, **max |ΔSharpe| = 0.0036**
(mean −0.0006) against **max |ΔCAGR| = 0.0637** and **max |ΔMaxDD| = 0.1717**. Exposure
LEVEL therefore cannot carry a Sharpe ordering at all. The gate family's low gross is not a
level — it is a time-varying cash allocation, and that timing property is what survives the
restatement. Re-spreading, the only leverage-free way to match a gate book upward, is not an
exposure change but a different book: over 24 paired points it buys **+3.42% of CAGR**
(OOS +3.76%) and pays **−11.96 pp of MaxDD** (OOS −12.08 pp, worse on **24/24**), losing
Sharpe on average (−0.024 full, −0.042 OOS, wins 7/24).

## KEEP paths and rule 8
**4a 0/216** (drawdown, every point). 4b 29/216 (NATIVE 7, RESPREAD 16, SCALARLO 6); 4b'
(also beats its own variant's EW_ALL) 12/216. Rule 8, book chosen on IS ≤2016-12-31 inside
each variant under two selectors, 2017–2026 read once: **0/36 picks beat their own EW_ALL
out of sample**, 2/36 clear 4b OOS, 0/18 cells show the excess restatement changing the pick
(idea 460's 0/6, three times over). **No KEEP.**

## Lead logged, not a KEEP
RESPREAD RULES v2 on U56 clears 4b at **both** rungs, beats its own EW_ALL at both, and
holds both out of sample (OOS 13.41%/1.2025/−17.71% at 10 bps, 12.68%/1.1427/−17.89% at 25,
vs SPY OOS 15.45%/0.8820/−33.72%). It still **loses to the live native RULES v2 book OOS**
(Sharpe 1.2851/1.2483) and pays 5.7 pp more drawdown, no rule-8 selector picks it, and the
paired evidence above says re-spreading costs Sharpe on 17 of 24 points. Not a rules change.

## Prescription proposed (Sunday-review business, NOT applied)
Any claim that two book families are "matched on gross" must state WHICH match: a scalar
exposure match is Sharpe-neutral by construction (ceiling measured here at 0.0036) and can
only move CAGR and MaxDD claims, while a re-spread match changes the book. The record's
"matched-gross" prescription (idea 471) does not currently distinguish them.

**SURVIVORSHIP:** B136 and SMALL439 are current-constituent lists, so their levels are
biased upward and unequally; only the within-panel book-minus-EW_ALL contrast is load-bearing.
SMALL439 drops the 44 names with max_1d_move ≥ 1.0 and its levels are not investable history.
