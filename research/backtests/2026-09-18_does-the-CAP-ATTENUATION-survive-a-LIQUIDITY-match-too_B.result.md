# Idea 1078 (lane B, 2026-09-18) — does the CAP ATTENUATION survive a LIQUIDITY match too?

**ANSWER: YES, IT SURVIVES — and NO, liquidity does NOT close more of the gap than vol did.
KILL (capital) of the liquidity explanation, on the same terms vol was killed.** On 1073's own
cap axis a liquidity match does not close the attenuation at any tolerance; it **widens** it
(−137% / −203% / −192% of the unmatched gap, against vol's +18.8% / +50.5% / +28.3%). Gates
**8 of 8 PASS**; hypotheses 6 of 10. 998 panels, 3,992 book rows, 10 bps, weekly, next-day,
GROSS 0.75, IS ..2016 / OOS 2017.. .

Script: `research/backtests/2026-09-18_does-the-CAP-ATTENUATION-survive-a-LIQUIDITY-match-too_B.py`

## 0. The queue's LITERAL run cannot be done offline — censused, not asserted
1073's ladder spans two pools and `q = 0.00` is **pure BSTK**. A dollar-volume window needs a
volume on BOTH sides. `data/` holds exactly one volume cache (`volume_small.csv.gz`);
`load_volume(small=False)` raises. **BSTK names carrying a cached volume: 0 of 100. SMALL: 663
of 663.** (H_INFEAS PASS.) Two feasible routes were run in full instead; neither is presented as
the literal run, and the literal run is left for a session with the broad-panel volume cached.

## 1. Route B — 1073's OWN axis, a price-only liquidity match. The attenuation SURVIVES
Roll (1984) implied effective spread `2*sqrt(-cov(r_t, r_t−1))`, IS 2010..2016 only, available
on both pools. Validated first: **Spearman(Roll, −log10 median $volume) = +0.5986** over the 289
SMALL names carrying both (H_VALID PASS). Headline block k=20, the only width feasible at every
tolerance.

| tau | rho(q=0.00) | rho(q=1.00) | gap | closes | vol on this axis (1073, committed) |
|---|---|---|---|---|---|
| UNMATCHED | +0.4723 | +0.1150 | **+0.3572** | — | — |
| 0.45 | +0.7568 | −0.0908 | +0.8476 | **−137.3%** | +18.8% |
| 0.30 | +0.8325 | −0.2482 | +1.0807 | **−202.5%** | +50.5% |
| 0.20 | +0.6842 | −0.3602 | +1.0444 | **−192.4%** | +28.3% |

G7: the dial binds — SD(log10 panel Roll) falls 0.1635 → 0.0082. Holding the spread fixed makes
the cap ordering **stronger at every rung**, and the q=1.00 end goes negative. **This is the
answer to the queue: liquidity closes less than vol, not more** (H_ROLL FAIL, H_ROLLSPR PASS).
The all-k block agrees in sign and is milder: +0.6779 → −11.9% / −42.2% / −38.4%.

## 2. Route A — real dollar volume, and the attenuation ISN'T THERE to be matched away
Inside the small panel (where the queue's own variable exists), cut at the pool's own median
cap: TINY 183 names (median $399M) vs BIG 182 ($1,181M). It is a genuine liquidity axis —
median $volume **BIG / TINY = 5.72x** (H_DVGAP PASS) — but the cap ordering **reverses**:
unmatched k=20 **rho(q=0.00) +0.1998 vs rho(q=1.00) +0.4511, gap −0.2513** (H_SPREAD FAIL).
Concentration pays MORE in the tinier half of the sub-$2B screen, not less.

**The closure percentages on this axis are therefore NOT INTERPRETABLE and no claim is taken
from them.** H_LIQ's declared bar reads "closes 412.0%" at tau=0.20 and is recorded as a
**VACUOUS PASS**: it is a percentage of a *negative* base (the gap runs −0.2513 → −0.2270 →
+0.1968 → +0.7841, i.e. the ordering flips and then widens the other way). The two "True" cells
of H_MORE at tau 0.30 / 0.20 compare two such quantities and are reported as meaningless;
**H_MORE FAILS overall** (tau=0.45 DV 9.6% vs VOL 193.0%). The usable finding from route A is
the reversal itself: **the cap attenuation is a BETWEEN-POOL fact (SMALL vs BSTK), not a
within-small-cap one.** The same-axis VOL arm, run at the same tolerances for the like-for-like
comparison, is equally non-monotone (193.0% / −135.1% / −31.6%) — on this short axis neither
control is doing anything but moving draw noise.

## 3. Where liquidity DOES bite — and why it still cannot be the cap axis
CROSSQ: each cap pool cut at its own median IS $volume.

| cell | median $vol | panel vol | rho |
|---|---|---|---|
| BIG-LOQ | 431,769 | 0.3971 | −0.0936 |
| BIG-HIQ | 6,406,783 | 0.3836 | +0.0971 |
| TINY-LOQ | 64,793 | 0.4777 | **+0.5177** |
| TINY-HIQ | 2,844,709 | 0.4236 | **−0.3316** |

Within TINY, moving $volume alone shifts rho **0.8493**; within BIG it shifts it **0.1906**, and
**in the opposite direction**. Across the cut at the nearest $volume it shifts **0.2380**.
Liquidity is a strong, sign-flipping dial inside the tiny half and a weak, oppositely-signed one
inside the big half — exactly the asymmetry breadth showed in idea 1080 — so it is not a common
axis that could stand in for cap.

## 4. Rule 8 (required) and both KEEP paths
n/k chosen on 2009-2016 IS Sharpe ONLY inside each (arm, cell, k, draw) choice set; 2017- read
once. Mean OOS Sharpe / CAGR / MaxDD by selector: RATIO-MAX **0.3044 / 3.04% / −26.83%**,
IS-SHARPE-MAX 0.2893 / 3.04% / −31.06%, RANDOM 0.2732 / 2.89% / −35.12%, RATIO-MIN 0.1946 /
1.92% / −46.55%. On the SAME panels **SPY OOS Sharpe 0.8767 / CAGR 15.33% / MaxDD −33.72%** and
**RULES v2 OOS Sharpe 0.4701 / CAGR 3.56% / MaxDD −17.00%**. The best selector beats SPY on
**7.7%** of choice sets and RULES v2 on **15.0%**. By arm the only respectable OOS sits where
the panels are large caps (ROLL 0.5513, REPRO 0.5919); the small-cap arms read 0.07–0.23.

**KEEP paths, every book row: 4a 0 of 3,992; 4b 78 of 3,992 (2.0%).** By arm: ROLL 59 of 1,048
(58 of them at q=0.00, pure BSTK), REPRO 19 of 384 (all q=0.00), DV 0 of 1,024, VOL 0 of 1,152,
CROSSQ 0 of 384. Every 4b pass sits on a pure large-cap panel. These are the record's committed
CAND-n books on random sub-panels of a survivor screen, so a 4b pass is a statement about the
draw. **Nothing is promoted. No memo, no RULES change.**

## Gates — 8 of 8 PASS, printed before any result
G1 fast runner == `engine.backtest` on returns (2.08e-17) and turnover (0.00e+00), cached-rank
CAND-20 == idea 286's committed `cand_weights(20)` (0.00e+00) · G2 envelope over all 998 panels,
0 violations, every name inside its declared window · G3 no look-ahead (IS vs full-sample ranks:
vol +0.8424, $volume +0.9317, Roll +0.6780) · G4 determinism · **G5 CROSS-RUN: 1073's four
committed crossing rho reproduce at max|d| 0.00e+00 (+0.8759 / +0.7649 / +0.3586 / +0.1769) and
its 0.4063 shift at 0.4063** · **G6 BOOK level: 384 of 384 REPRO rows join 1073's committed
books.csv, max|d OOS Sharpe| 2.22e-16** · G7 all three dials bind · G8 the X* grids published in
full (251 points).

## Limits, stated before the verdict
1. The literal run was NOT executed (§0) and nothing here substitutes for it.
2. Route A's cap axis is cut on TODAY's market cap and spans only $399M vs $1,181M — a far
   shorter lever than SMALL-vs-BSTK, so its weak/reversed ordering is unsurprising on those
   grounds alone and is claimed only as a within-small statement.
3. The Roll spread is a PROXY, ranking +0.5986 against true $volume. Route B's answer is only
   as good as that number; it is a spread measure, and a depth measure could read differently.
4. Matching happens where the pools OVERLAP, so matched cells speak for neither pool's typical
   name; 7 (q, k) cells are infeasible at the tight rungs and are listed, never filled.
5. 8 draws x 4 rungs per (cell, k); no interval is published for any rho, so two closures here
   are not shown to DIFFER — only ORDERING and SIGN are claimed (idea 1044's rule).
6. SURVIVORSHIP (rule 9): a realised IS $volume is measured on names that survived to be
   screened today, so every liquidity window is doubly a survivor window. Levels are upper
   bounds; the quoted results are within-grid differences on identical dates.

## NOT claimed
That liquidity is irrelevant (§3 shows it is the dominant dial *inside* the tiny half). That
1073's numbers are wrong (they reproduce to 0.00e+00). That the literal dollar-volume ladder was
run. That route A's closure percentages mean anything. That any committed verdict flips.
