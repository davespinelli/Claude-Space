# Idea 1172 (lane C, 2026-09-17) — is the EDGE LADDER TRUNCATED at n=5, or does an INTERIOR PEAK exist BELOW it?

**ANSWERED = TRUNCATED. THERE IS NO INTERIOR PEAK. The B136 argmax moves from n=5 to n=1 at four
of the six holds and to n=2 at the other two, at bootstrap P(argmax = observed) = 0.946–1.000 and
P(argmax = 5) = 0.000 at EVERY hold on BOTH panels. EDGE has no interior optimum in n on this
tape: wherever the ladder is cut, the peak sits at the cut or one rung in. KILL as a capital
finding, and a CORRECTION to every argmax the record has published in this family.**

Dials: **N in {1, 2, 3, 4, 5, 8, 10} x H in {21, 42, 52, 63, 76, 90, 126}** = 49 cells per panel,
**98 in total, every one published** for the book and for its own DD-matched null. Everything else
frozen at 936/1064/1071/1082/1086/1093's construction (cap INF, CAND20 legs, max_vol 0.60, gross
0.75, W cadence, 10 bps, LAG 1, 40 seeds, null draws paired across H). n=10 is carried only so
three rungs overlap 1093's ladder and can be gated cell-for-cell.

## The pre-declared decision rule, and what it returned

Declared before any number, scored on B136 over 1093's own six left-end-argmax holds
{21,42,52,63,76,90}: **(A) INTERIOR PEAK AT n=5** = argmax 5 at >= 4 of 6. **(B) STILL TRUNCATED**
= argmax 1 at >= 4 of 6. **(C) NEW INTERIOR PEAK ELSEWHERE** = argmax in {2,3,4,8} at >= 4 of 6.
**(D) NOT RESOLVABLE** = no rung reaches 4 of 6.

| pre-declared hypothesis | verdict | reading |
|---|---|---|
| H_REP — the 3 rungs shared with 1093 reproduce its committed EDGE at all 18 cells | **PASS** | max \|d\| = **4.59e-07 pp** |
| H_INTERIOR — B136 argmax interior at >= 4 of 6 | **FAIL** | **2 of 6** (H=21 and H=90, both at n=2) |
| H_NOT_ONE — B136 argmax NOT at the new left end at >= 4 of 6 | **FAIL** | argmax = 1 at **4 of 6** |
| H_FIVE — 1093's rung survives the extension | **FAIL** | argmax = 5 at **0 of 6** |
| H_BOOT — bootstrap P(argmax = observed) >= 0.50 at >= 4 of 6 | **PASS** | **0.946–1.000 at all six** |
| H_CLIP — the lambda<=1 clip binds on MORE draws as n falls | **FAIL** | **2 of 7** holds — the artefact mechanism does not even run the right way |
| H_SYM — the symmetric match gives the same argmax at >= 4 of 6 | **PASS** | **6 of 6** on B136, **7 of 7** on U56 |
| H_4B_CONC — no cell at n <= 4 clears 4b | **PASS** | **0 of 56** |
| H_TURN — turnover falls strictly as H lengthens, every (panel, N) | **PASS** | B136 spread 7.81x/yr |
| H_WF — >= 1 rule-8 pick clears 4b OOS | **PASS** | 1 of 8 |
| H_4A — no cell clears 4a | **PASS** | **0 of 98** |

**Verdict off the pre-declared rules: OUTCOME (B), STILL TRUNCATED.**

## The correction

**EDGE is monotone in concentration, and its argmax is a property of the LADDER, not of the book.**
Mean EDGE over the seven holds falls **21.15 / 16.43 / 12.77 / 9.89 / 8.74 / 5.80 / 5.63 pp** at
n = 1 / 2 / 3 / 4 / 5 / 8 / 10 on B136 and **12.80 / 10.55 / 11.21 / 9.30 / 6.98 / 6.23 / 6.05** on
U56. 1093 read an argmax at n=5 because 5 was the left end of 1082's ladder; put four rungs below
it and the argmax walks straight down to them. **EDGE(1) − EDGE(5) on B136 is +3.17 / +14.82 /
+11.54 / +6.48 / +19.49 / +12.88 pp at the six holds, at +3.11 / +15.21 / +10.30 / +6.47 / +18.60 /
+11.75 SE** — decisive at every one. The record should read a published "peak at n = x" in this
family as "x was the smallest n on the ladder", unless a rung below x is shown.

**It is not the lambda clip.** The obvious artefact — fewer names deepens the book's drawdown, the
DD match stops binding, EDGE inflates at the left end — was pre-declared as H_CLIP and **REFUTED**:
the drier share is higher at n=1 than at n=10 at only 2 of 7 B136 holds (D2). And releasing the
clip upward to lambda <= 3.0, so a drier null is LEVERED to the book's drawdown instead of entering
understated (EDGE_SYM, published at all 98 cells), **leaves the argmax unchanged at 13 of the 14
(panel, hold) ladders** and identical at 6 of 6 on the B136 edge holds. The left-end rise is a
property of the book, not of the measurement.

## The EDGE ladder at every hold (pp, 40 seeds, REBUILT, clip at 1.0)

```
B136       n=1      2       3       4       5       8      10   argmax  1093  E(1)-E(5)   sigmas
  * H= 21 +11.245 +14.897 +11.562  +7.789  +8.074  +4.842  +5.544    2      5    + 3.171   + 3.11
  * H= 42 +25.797 +15.609 +12.223 +10.064 +10.974  +5.154  +5.639    1      5    +14.822   +15.21
  * H= 52 +19.495 +14.448 +11.041  +9.209  +7.951  +4.947  +4.574    1      5    +11.544   +10.30
  * H= 63 +17.753 +15.698 +12.470 +12.657 +11.269  +8.822  +7.663    1      5    + 6.484   + 6.47
  * H= 76 +29.432 +14.570 +14.269 +11.955  +9.945  +6.206  +4.389    1      5    +19.487   +18.60
  * H= 90 +20.097 +25.000 +16.472 +10.422  +7.217  +5.375  +3.277    2      5    +12.880   +11.75
    H=126 +24.216 +14.822 +11.329  +7.156  +5.717  +5.245  +8.324    1     10    +18.499   +17.65
U56
    H= 21 +10.547 +10.634 +11.611  +8.195  +5.930  +6.163  +7.319    3      -    + 4.617   + 4.04
    H= 42 +23.024 +12.549 +15.784 +12.229  +8.982  +7.545  +5.573    1      -    +14.042   +12.98
    H= 52  -0.060  +4.979  +9.511  +8.127  +6.780  +6.463  +5.534    3      -    - 6.840   - 6.51
    H= 63  +2.499  +8.761 +11.064 +12.102  +6.599  +8.029  +6.777    4      -    - 4.100   - 4.13
    H= 76 +26.624 +14.226 +11.982 +10.086  +7.548  +4.973  +4.327    1      -    +19.076   +17.46
    H= 90 +13.291 +13.557 +10.171  +8.141  +7.044  +5.153  +6.656    2      -    + 6.247   + 5.59
    H=126 +13.670  +9.136  +8.380  +6.210  +5.955  +5.295  +6.164    1      -    + 7.715   + 6.57
seed SE at H=63: B136 0.907/0.642/0.603/0.491/0.426/0.274/0.318   * = 1093's six EDGE HOLDS
```
`*` marks 1093's six holds. **P(argmax = 5) = 0.000 at all 14 (panel, hold) ladders.** U56 is the
control and is rougher — its argmax sits at n=3 or n=4 at three holds and EDGE(1) is NEGATIVE at
H=52 — but it too peaks at n=1 or n=2 at 4 of 7 and never at 5.

## What the peak costs in capital — the reason this is a KILL

```
B136   n=1   CAGR 31.71%  MaxDD -40.43% (worst -46.29%)  Sharpe 0.986   4b 0/7
       n=2        28.12%        -32.42%         -37.86%         1.058   4b 0/7
       n=5        21.18%        -27.80%         -28.62%         1.023   4b 0/7
       n=10       18.01%        -25.84%         -28.16%         1.018   4b 0/7
U56    n=1   CAGR 23.43%  MaxDD -60.46% (worst -69.85%)  Sharpe 0.786   4b 0/7
SPY          CAGR 15.16%  MaxDD -33.72%   4b DD cap 20.23%, CAGR floor 10.61%
```
**The EDGE argmax is a Sharpe MINIMUM, not a maximum.** n=1 earns the most CAGR and the least
risk-adjusted return on both panels; on U56 it draws down **−60.46% on average and −69.85% at
worst**, roughly twice SPY's. **0 of 56 cells at n <= 4 clear 4b; 0 of 98 clear 4a.** Rule 8's
B136 choosers (IS Sharpe, IS EDGE, IS CAGR all agree) pick **N=2 H=90 → OOS 29.88% / 1.0272 /
−30.26%** against **SPY OOS 15.33% / 0.8767 / −33.72%** and **RULES v2 OOS 7.88% / 1.1059 /
−12.24%**: it beats SPY on all three Sharpe legs and the CAGR floor and **fails 4b on L_DD alone**
(−30.26% against a 20.23% cap). Full sample that cell is 36.52% / 1.2610 / −30.26%, halves
1.5820 / 0.9887. A ladder peak and a book worth capital point opposite ways here, exactly as
pre-declared.

## The one 4b pass, and why it is PARK not KEEP

**U56 N=10 H=21** is the only cell of 98 clearing 4b full-sample, it also clears 4b OOS, and it is
IS-chooser-reachable (C_ISDD picks it): full **16.51% / 1.0878 / −20.12%**, halves **1.2067 /
0.9948**, OOS **16.89% / 1.0574 / −20.12%** vs SPY OOS 15.15% / 0.8684 / −33.72%. It fails 4a
(A_DD: RULES v2 draws down −12.05%). **Its binding leg has a margin of +0.112 pp** (|−20.12%|
against a 20.23% cap) — 1083 measured the 90% width of a quantity of this kind at 4.1–7.2 pp on
this tape, so this pass is **not decidable at this sample**, and n=10 is the right-hand boundary of
this run's own ladder. The 10-line memo required by the protocol is written and recommends
**against** enactment; see `.memo.md`.

## Gates

11 of 14 PASS, including **G5 (the premise itself): 1093's committed EDGE at the 18 shared cells
reproduces to 4.59e-07 pp**, G1/G1b (fast runner ≡ `engine.backtest`, 1.39e-17), G4c (|MaxDD|
monotone in lambda over the whole [0.1, 3.0] range EDGE_SYM bisects, 0.000e+00), G7 (null draw
deterministic). Three FAIL and are published as failures:

* **G9 / G8b** demanded the N=1 book hold exactly one name at *every* rebalance date. Mis-specified
  by this run: the book is correctly **all-cash at 0.053 of rebalance dates**, where the
  eligibility gate admits nobody. **Max names held = 1 at every (N=1, H) cell** — it never holds
  two. The null is built by the same machinery with the same all-cash dates, so the contrast is
  like for like (D5).
* **G3** (SPY OOS triple) fails at **|d| = 2.894e-03 — the identical value 1093 published today**.
  The committed anchor predates the 2026-09-16 close now in `data/prices.csv`; one extra tape day,
  not a construction difference (D6).

## Survivorship (PROTOCOL rule 9)

U56 and B136 are **current-constituent** lists. Every level here is optimistic and every 4b/4a
count is an upper bound. **A one-name book drawn from a current-constituent list is the most
survivorship-flattered object in the whole record** — n=1's 31.71% CAGR on B136 should be read as
an upper bound twice over. The book-vs-null contrast largely cancels the bias out of EDGE; it does
not cancel out of the 4b legs, which are measured against SPY, a real index.
