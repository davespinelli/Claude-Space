# Idea 1269 (lane cloud, 2026-09-18) — does a FASTER EXIT GATE buy the DD LEG that every EXPOSURE DIAL could not?

**VERDICT: KILL (capital), NO NEW BOOK / ANSWERED: NO on the panels the record's book lives on,
and where it DOES work the price input is a coin flip.** 51 cells (16 exit cells + the measured
anchor, x 3 panels), 144 dose-matched RANDOM runs, an 18-point de-grossing frontier, 19 of 19
gates PASS, 26s, offline, deterministic.

## The answer
On **U56**, the panel the committed 2026-09-04 book is defined on, the exit dial buys **nothing**.
The shallowest of the 16 exit cells (MA50 / band 0.02) reaches **-18.86% MaxDD against the
anchor's -19.13% — +0.27pp — and pays -3.43pp of CAGR for it** (12.35% vs 15.78%), while **11 of
16 cells draw down DEEPER than the anchor does at full gross**, i.e. off the de-grossing
frontier's range entirely. **0 of 16 U56 cells and 0 of 16 B135 cells sit ABOVE the frontier**:
the flat gross cut reaches every drawdown these exit gates reach, for more CAGR, at a third of the
turnover. The exit joins the brake, the vol target, the slot sizer, the correlation brake, the
defensive rotation, the idle sleeve and the trailing stop as the eighth mechanism to lose to
de-grossing.

**The one place it works is the small-cap panel, and it is not enough.** On SMALL663 **16 of 16
cells sit above the frontier (+2.48 to +7.24pp of CAGR at matched drawdown)** and the shallowest
cell buys **+8.69pp of MaxDD AND +2.45pp of CAGR** against the anchor (-27.13% / 10.33% vs
-35.81% / 7.87%) — a real improvement on both axes. But **every one of the 17 SMALL cells still
FAILS 4b**, the best OOS Sharpe on the panel is 0.7007 against SPY's 0.8769, and the exit beats
its own dose-matched RANDOM arm on Sharpe at only **8 of 16 cells (mean +0.0197)** — a coin flip.
On U56 and B135 the exit is *worse* than random churn at the same dose (mean **-0.0356** and
**-0.0686** of Sharpe). Pre-declared outcome **(C), bought by churn**, with **(D) whipsaw** on top
on U56, where every faster gate costs both CAGR and drawdown.

## The run's first number: the symmetric exit the record's convention implies has never been run
(EXIT_MA=200, band=0.00) is the exit the entry gate's own 200d line implies; the anchor's min hold
overrides it, so it had never been measured. Making the exit symmetric with the entry **costs**:

| panel | anchor | symmetric MA200/b0.00 | delta |
|---|---|---|---|
| U56 | 15.78% / 1.1522 / -19.13%, OOS 1.1832 | 13.42% / 1.0855 / -20.43%, OOS 1.0589 | **-2.36pp CAGR, -0.0667 Sharpe, -1.30pp MaxDD** |
| B135 | 16.18% / 1.0715 / -20.74%, OOS 1.0240 | 15.65% / 1.0688 / -22.35%, OOS 0.9790 | -0.53pp, -0.0027, -1.61pp |
| SMALL663 | 7.87% / 0.5073 / -35.81%, OOS 0.4534 | 10.50% / 0.6402 / -28.76%, OOS 0.5517 | **+2.62pp, +0.1329, +7.05pp** |

Turnover rises 2.75 -> 4.76/yr on U56 for that loss. The asymmetry the record inherited by
accident — hold through the 200d breach until the min hold expires — is **worth 1.30pp of
drawdown and 2.36pp of CAGR on the anchor panel**, and is the wrong convention on small caps.

## The grid (all 51 cells in the .grid.csv)
**4a 0 of 51.** **4b 13 of 51: U56 12 of 17, B135 1 of 17, SMALL663 0 of 17.** Of the 38 failures
the **DD leg fails at 36**, joined by H2 28, OOS 23, H1 7, CAGR 3 — the seventh dial running to
say the committed 4b pass is a statement about drawdown and nothing else.

## Rule 8 (walk-forward, IS Sharpe on warm-up..2016 over the 16 exit cells, OOS read once)
| panel | pick | OOS Sharpe | anchor OOS | chooser - do-nothing | 4b | rank corr |
|---|---|---|---|---|---|---|
| U56 | MA100 / b0.01 | 0.9705 | 1.1832 | **-0.2127** | PASS | -0.3824 |
| B135 | MA200 / b0.01 | 1.0710 | 1.0240 | +0.0469 | FAIL (DD) | +0.5382 |
| SMALL663 | MA150 / b0.01 | 0.6488 | 0.4534 | +0.1954 | FAIL (H2, OOS, DD) | -0.0324 |

On the anchor panel an honest chooser lands **0.2127 of OOS Sharpe BEHIND doing nothing** — the
largest chooser penalty this lane has recorded on any dial — with an IS/OOS rank correlation of
-0.3824 over 16 cells. B135's and SMALL's gains buy books that fail 4b. Mean across the three
panels is +0.0099: nothing.

## Benchmarks on this tape
U56 SPY 15.13% / 0.8849 / -33.72%, OOS 0.8747; LIVE v2 8.62% / 1.2018 / -12.05%, OOS 1.2781.
B135 SPY 15.16% / 0.8862, OOS 0.8769. SMALL663 SPY 14.06% / 0.8582, OOS 0.8769.
G1 replays the committed anchor triple 15.7147% / 1.1480 / -19.1276% to **5.965e-05**
(vintage-pinned to 2026-09-16; the live tape runs 1 trading day longer, published not toleranced).
G4 confirms the exit is **not** an exposure cut: realised mean gross is 0.7501-0.7504 at all 48
exit cells against the anchor's own 0.7501-0.7503, and no cell's drifted max exceeds the anchor's.

## Survivorship (rule 9)
U56 and B135 are current-constituent lists; SMALL663 is a current sub-$2B screen with the 52
tickers at max_1d_move >= 1.0 dropped first. Every absolute level is optimistic. This particular
bias runs **against** a faster exit — on names that all recovered, selling a dip is a mistake the
tape always punishes — so U56's "the exit costs 3.43pp of CAGR for 0.27pp of drawdown" is if
anything an UPPER bound on the exit's value, and SMALL's frontier win is the reading least
explained by the bias. The contrast against RANDOM and against the frontier is first-order immune;
the 4b legs are not.

## Capital
No new book. The exit dial is not the free axis the queue item hoped for: on the panel the
committed book lives on it is a whipsaw that costs on both legs and loses to random churn at the
same dose, and on the panel where it genuinely improves both CAGR and drawdown it still cannot get
a book past SPY on three 4b legs. What the run does leave the record is a measured price for the
inherited entry/exit asymmetry — 2.36pp of CAGR and 1.30pp of MaxDD on U56 — which had never been
a number before.
