# Idea 1271 — does a PER-NAME TRAILING STOP buy the DD LEG more cheaply than PORTFOLIO DE-GROSSING?

## Verdict: **ANSWERED NO** on U56/B135 · **KILL (capital)**, no new book · **PARK** on the small-cap panel.

360 cells (6 stop depths x 4 cooldowns x 3 arms x 3 panels) + an 18-point de-grossing frontier. 16/19 gates. 76s.

## The mechanism is not an exposure cut (G4's mean-gross clause)
Mean realised gross stays within **0.0048 / 0.0008 / 0.0017** of the anchor's on U56 / B135 / SMALL663: the stop
removes the losing name and the slot is refilled. This is the first mechanism in the record to move the DD leg
without moving exposure.

## It fires, and it buys drawdown
| panel | depth 5% | 10% | 15% | 20% | 30% |
|---|---|---|---|---|---|
| U56 expulsions/yr | 82.4 | 36.5 | 18.7 | 9.9 | 3.6 |
| SMALL663 expulsions/yr | 228.1 | 116.4 | 71.5 | 45.9 | 21.3 |

Idea 9's "0.4 firings/yr on v1" does **not** transfer to this book. Best DD cells: U56 -19.13% -> **-12.98%**
(+6.14pp, costing -9.12pp CAGR); B135 -20.74% -> -16.43% (+4.31pp, -5.44pp); SMALL663 -35.81% -> -26.16%
(+9.65pp, **+0.67pp** CAGR).

## But de-grossing buys the same drawdown ~20x cheaper (the title's question)
Frontier = the same book at gross 0.75/0.65/0.55/0.45/0.35/0.25 (U56: 15.78/13.65/11.53/9.41/7.30/5.20% CAGR at
-19.13/-16.73/-14.29/-11.81/-9.28/-6.69% MaxDD, Sharpe flat at ~1.151). Read at **matched MaxDD**:

| panel | d_CAGR vs frontier | d_Sharpe | d_OOS | stop wins |
|---|---|---|---|---|
| U56 | **-3.55pp** | -0.1291 | -0.1494 | 0 of 7 |
| B135 | **-3.90pp** | -0.1522 | -0.2258 | 0 of 7 |
| SMALL663 | **+2.80pp** | +0.1086 | +0.0739 | **18 of 20** |

U56 exchange rate: the stop pays **17.34pp CAGR per pp of MaxDD**; de-grossing pays **0.87**. (B135's ratio reads
3282 on a near-zero denominator — unstable, published, read the matched-MaxDD differences instead.)

## The drawdown signal is real — this is a price verdict
vs a dose-matched RANDOM-expulsion placebo (same count, same weeks, 3 seeds): d_MaxDD **+2.21pp (>0 at 49/60)**,
d_CAGR -1.86pp, d_Sharpe -0.0616 (12/60), d_OOS -0.0823 (8/60). vs WORSTRANK expulsion: d_MaxDD +1.75pp (42/60).

## Rule 8 (chosen on IS Sharpe to 2016-12-31, 2017-2026 read once)
U56 picks 0.20/21 -> OOS 1.1363 vs do-nothing 1.1832 (**-0.0469**); B135 0.20/126 -> 0.9673 vs 1.0240 (-0.0567);
SMALL663 0.20/21 -> 0.5464 vs 0.4534 (**+0.0929**). STOP arm mean -0.0036, positive at 1 of 3; all 15 choosers
mean -0.0173, positive at 5 of 15. **4a 0 of 360. 4b 56 of 360. 0 of 60 braked cells convert a 4b FAIL.**

## Gates: 16 of 19, failures published not re-specified away
G1 anchor replay err 5.97e-05 · G2/G5/G7/G8 exact zeros (G5 = counts rebuilt from truncated prices, 488
rebalances) · G6 monotone dose. **G4 fails on all three panels**: its drift clause demands no cell drift above the
anchor's own intra-week gross, and braked cells reach 0.7821 vs the anchor's 0.7674 because an expelled book is
briefly more concentrated. G4 and G7 were **corrected mid-run** and both original wordings are on the record: G4
first demanded drifted gross <= 0.75, which the committed anchor itself fails at 0.7674; G7 first demanded exact
dose, failing at |d|=2 in the legal shortfall case its own prose named.

## Survivorship (rule 9), and it cuts toward the stop
U56/B135 current constituents; SMALL663 = 715 sub-$2B names less 52 with max_1d_move >= 1.0. A current-constituent
panel has had its permanent losers removed in advance, so an instrument whose job is to cut names that keep falling
is measured on a tape where the worst a name can do is fall and recover. This KILL is therefore conservative, and
the SMALL663 PARK needs a delisting-complete panel before it is read as an edge.

Artefacts: `.console.txt`, `.grid.csv` (360), `.frontier.csv` (18), `.walkforward.csv` (15), `.dose.csv`, `.gates.csv`.
