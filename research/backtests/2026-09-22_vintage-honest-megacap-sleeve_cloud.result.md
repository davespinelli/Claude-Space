# Idea 934 — does the SINGLE20 LOOK-AHEAD survive a VINTAGE-HONEST mega-cap list?
lane cloud, 2026-09-22, run 11. Script: `2026-09-22_vintage-honest-megacap-sleeve_cloud.py`

**ANSWERED = THERE WAS LESS TO SURVIVE THAN 924 THOUGHT. In the leg window 924's "+0.2958 of
NAME SELECTION" sits +1.24 sd above a FIXED RANDOM 20-name basket drawn from the same
2026-vintage pool, and 71.5% of it is delivered by holding ALL 100 pool names with no selection
at all. It is a SURVIVORSHIP-POOL fact, not a selection fact. The look-ahead is real — but it
pays LATER (FULL z +5.05, OOS z +3.85), i.e. exactly where the hindsight was formed. No
vintage-honest ranking beats the fixed-random null in the leg window, and nothing here is
promotable: 0 of 48 honest cells clear 4a or 4b at any cost rung.**

## Cross-run gates — 11 of 11, reproducing idea 924 to four decimals
G6 `SINGLE20/EW - SPY` in 924's leg window (2009-01-13 … 2013-01-07, **1,003 days**, G9) reads
**+0.3705** against 924's published +0.3708; G7 `RSP - SPY` **+0.0748** against +0.0750; G8 the
selection residual `SINGLE20 - RSP` **+0.2957** against **+0.2958**. G1 the panel partitions
136 = 100 singles + 36 ETFs; G2 the answer key is `universe.json:megacap`, 20 names; G3 max
gross 0.7500, never levered; G4 the top-k rule selects exactly k once warm; G5 the ranking
carries no same-day price (corr −0.0176); G10/G11 the eligible pool runs 87 names at the leg
window start and 99 at the last date.

## The decomposition 924 did not run: POOL, then PICK
`POOL100EW` — equal-weight **every** eligible name in the 100-name single-name pool, no
selection whatever — already delivers most of what 924 attributed to picking 20 names:

| window | answer key vs RSP | POOL, no selection | share that is POOL | share that is the PICK |
|---|---|---|---|---|
| LEG (2009-13) | **+0.2957** | +0.2114 | **71.5%** | +0.0843 (28.5%) |
| FULL | +0.5785 | +0.3802 | 65.7% | +0.1983 (34.3%) |
| OOS (2017-26) | +0.6387 | +0.4431 | 69.4% | +0.1956 (30.6%) |

## The placebo that settles it: a FIXED random basket from the same pool
Two nulls, because they are not the same null. **RANDFIX** draws k names once from the pool
eligible at the warm-up date and holds them — the like-for-like null for a fixed list held from
2008. **RANDROT** redraws every rebalance; its turnover runs **46–70x/yr** against RANDFIX's
0.87x, so its handicap is churn, not selection (idea 1050's finding, reproduced).

RANDFIX, 10 md5 seeds, 10 bps, selection contrast vs RSP:

| k | LEG | FULL | OOS | turnover/yr |
|---|---|---|---|---|
| 10 | +0.2525 ± 0.1611 | +0.3054 ± 0.0807 | +0.2811 ± 0.0698 | 0.87 |
| **20** | **+0.2041 ± 0.0737** | +0.3249 ± 0.0502 | +0.3568 ± 0.0733 | 0.87 |
| 30 | +0.1538 ± 0.0998 | +0.3208 ± 0.0590 | +0.3933 ± 0.0890 | 0.89 |
| 40 | +0.2527 ± 0.0540 | +0.3310 ± 0.0404 | +0.3737 ± 0.0575 | 0.90 |

Scored at its own list size (k=20): **LEG z = +1.24, FULL z = +5.05, OOS z = +3.85.** The
hand-picked 2026 top-20 is, in the 2009–2013 window 924 read it in, **indistinguishable from
twenty names drawn at random from the same survivorship-selected pool and held**. It separates
decisively only in the period in which those names actually became the largest.

## The vintage-honest arms (2 tuned parameters, 4 x 4, every level reported)
Retention of the +0.2957 in the leg window swings from **−107% (GROWTH3Y k=40) to +117%
(IVOL60 k=10)** across the 16 honest cells — the retention is not a property of the sleeve, it
is a property of which ranking variable you pick. Against the RANDFIX null at matched k, **no
arm is resolvable in the leg window**: best is IVOL60 k=10 at z +0.57, MOM12_1 k=10 at z +0.15;
GROWTH3Y — the "has become one of the biggest" proxy, the closest price-only stand-in for the
answer key's own construction — runs z −2.55 to −10.55, i.e. **significantly WORSE than random**.
Out of sample the best honest arm is MOM12_1 k=10 at z +1.81, which 10 seeds cannot resolve.

## Rule 8 walk-forward (ranking variable and k chosen on IS only, OOS untouched)
The IS chooser picks **MOM12_1, k=10** in all 6 (pool, cost) cells. Honest pool, 10 bps:
**OOS CAGR 24.15% / Sharpe 1.0896 / MaxDD −28.16%** against live RULES v2 OOS 7.82% / 1.0982 /
−12.24% and SPY OOS 15.17% / 0.8696 / −33.72%. It triples the live book's OOS CAGR at a Sharpe
that is 0.009 BELOW it, for 2.3x the drawdown — and it is a cost-rung object: turnover 11.4x/yr
(the answer key's is 1.09x) drops it to **0.8844 at 50 bps**, 0.015 above SPY.

## KEEP paths — 0 of 48 honest cells, at every cost rung
**4a: 0 of 48.** Mega-cap sleeves draw −21% to −35% against the live book's −12.2%; the DD leg
is unreachable by construction. **4b: 0 of 48 on POOL100**, binding on the DD cap for every cell
with enough CAGR (best honest DD ratio 0.639 against the 0.60 allowance) and on the CAGR floor
for every cell inside the cap (IVOL60 k=10: 0.638 x SPY against the 0.70 floor). **Exactly one
4b pass exists in the whole run and it is inside the answer key**: POOL20 `IVOL60 k=10` — the
ten lowest-vol names of the 2026 top-20 — FULL 17.28% / 1.2862 / −19.54%, H1 1.2836, H2 1.2931,
OOS 19.33% / 1.3894 / −19.54%, DD margin over the cap 0.7 pp. Its honest twin fails the CAGR
floor. **The run's only 4b pass is precisely the cell where the look-ahead does the work**, so
it is a diagnostic, not a candidate. Nothing promoted.

## By-product, and the mirror of this run's idea 1
**Even the pure answer key fails 4b.** A 2026 top-20 list held from 2008 with perfect hindsight
reads FULL 23.29% / 1.3723 / −24.46%, clears every Sharpe leg and the CAGR floor by 2.2x — and
**fails on the drawdown cap** (0.725 of SPY's −33.72% against the 0.60 allowance). Idea 2223,
run the same day, killed the band book on the **CAGR floor** with the DD cap slack. The two 4b
legs bracket the record's two families exactly: the band book has the drawdown and not the
return, the mega-cap book has the return and not the drawdown, and neither crosses.

## Verdict
**KILL.** The look-ahead does not survive, and in the leg window there was nothing to survive:
924's +0.2958 is a survivorship-pool fact at +1.24 sd from a fixed random basket. No honest
ranking variable is resolvable against that null, the rule-8 pick loses to the live book on
Sharpe OOS at 2.3x its drawdown, and 0 of 48 honest cells clear either KEEP path.

## Honest limits
**Survivorship is the whole point and is not removed:** the 100-name pool is a 2026
constituent list, so every honest arm here is an UPPER BOUND on what was reachable in 2009 —
whatever it fails to retain it could not have retained. Names enter only on 252 prior closes,
which is point-in-time for LISTING but not for MEMBERSHIP. RSP and SPY are traded and carry no
survivorship, which is why every headline contrast is taken against RSP. Share volume is not in
the sandbox (`data/` carries `volume_small.csv.gz` only), so the queue's own "trailing dollar
volume" ranking could not be run; four price-only rankings stand in for it and all are reported.
10 placebo seeds, one gross (0.75), one cadence (W), one split point.
