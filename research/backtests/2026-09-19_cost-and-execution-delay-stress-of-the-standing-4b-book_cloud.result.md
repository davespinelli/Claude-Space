# Idea 1590 (lane cloud, idea 2 of 2) — does the standing 4b book survive 25/50 bps and extra days of execution delay?

**VERDICT: KILL for capital (pre-registered H_FRAGILE fired).** The standing book's 4b pass is
robust to COST out to 120 bps and dies to ONE extra day of EXECUTION LATENCY at every cost rung,
0 bps included. And no IS-only chooser reaches a 4b-passing rung at any of the 48 (panel, cost,
delay) cells.

624 published cells: 3 panels x 13 gross rungs (0.40..1.00 step 0.05) x cost {0, 10, 25, 50} bps
x execution delay {+0, +1, +2, +3} trading days on top of PROTOCOL rule 2's t-1 -> t (so +0 IS the
protocol convention, G7 verified bit-for-bit). The book itself is frozen: N = 20, H = 126,
MAXVOL 0.60, per-name 200d MA gate, weekly.

## 1. Cost is not what kills it. Latency is.
The frozen incumbent (U56, gross 0.75) at delay +0:

| cost | CAGR | Sharpe | MaxDD | H1/H2 | OOS | 4b full / OOS |
|---|---|---|---|---|---|---|
| 0 bps | 16.14% | 1.1750 | -19.08% | 1.2291/1.1409 | 17.67% / 1.2063 / -19.08% | **True / True** |
| 10 bps | 15.80% | 1.1537 | -19.13% | 1.2067/1.1203 | 17.32% / 1.1857 / -19.13% | **True / True** |
| 25 bps | 15.31% | 1.1217 | -19.20% | 1.1730/1.0895 | 16.81% / 1.1546 / -19.20% | **True / True** |
| 50 bps | 14.48% | 1.0682 | -19.35% | 1.1166/1.0381 | 15.95% / 1.1028 / -19.35% | **True / True** |

Bisected on its own turnover path, its 4b verdict does not flip until **c\* = 120.3 bps** (OOS
median c\* on U56 is 139.0). At 2.87x/yr turnover the standing book is simply not a high-turnover
object, so a 2.5x or 5x cost shock does not reach it.

**One extra day of execution delay does.** U56, gross 0.75, 10 bps, vs delay +0:

| | dSharpe | dCAGR | dMaxDD | dOOS Sharpe | 4b full (OOS) |
|---|---|---|---|---|---|
| +1 day | **-0.0487** | -0.54 pp | **-2.44 pp** | -0.0835 | True -> **False** (True -> False) |
| +2 days | -0.0334 | -0.31 pp | -1.37 pp | -0.0507 | True -> **False** |
| +3 days | -0.0418 | -0.34 pp | **-2.79 pp** | -0.0078 | True -> **False** |

MaxDD moves -19.13% -> -21.57%, straight through the 4b DD cap of -20.23%. At delay +1 the entire
U56 gross ladder loses the g = 0.75 rung (c\* = x, i.e. it fails 4b even at 0 bps). **The binding
4b leg is a latency object, not a cost object, and no cost convention in the record has ever
tested it.**

## 2. And the latency axis is not even monotone — it is a coin flip of the size of the margin
B136's frozen book goes the *other* way: delay +1 turns a 4b FAIL into a 4b PASS (dSharpe **+0.0907**,
dCAGR +1.81 pp, dMaxDD **+1.32 pp**, OOS 16.19%/1.0180 -> 17.98%/1.1024), and then loses it again at
+2 and +3. SMALL moves +0.0480 / +0.0050 / +0.0131 of Sharpe and never passes anything. Across the
grid the 4b BOTH-window count runs 11 / 11 / 9 / 6 (0 bps) and 10 / 10 / 4 / 3 (10 bps) as delay
goes +0 / +1 / +2 / +3. **A single trading day of execution timing moves MaxDD by 1.3 to 3.6 pp in
either direction — larger than the DD margin 4b verdicts are decided on. Every 4b verdict in this
record is quoted on one arbitrary point of an axis with that much dispersion.**

## 3. The death search, all 156 (panel, delay, gross) books
c\* FULL (bps), `x` = already fails 4b at 0 bps:

```
 [U56]  delay |  0.40  0.45  0.50  0.55  0.60  0.65  0.70  0.75  0.80 .. 1.00
           +0 |     x     x   5.3  50.5  88.1 119.6 120.0 120.3     x ..    x
           +1 |     x     x     x  34.5  71.6 102.9   8.2     x     x ..    x
           +2 |     x     x     x  41.3  78.7 110.3 111.5     x     x ..    x
           +3 |     x     x     x  40.1  76.9  88.8     x     x     x ..    x
 [B136] +0 |  .. 14.1  42.7  43.1  43.4  43.8  x ..   +1 | .. 12.7 60.8 91.1 91.6 92.0 92.4 91.0 x ..
 [SMALL] every cell x at every delay and every gross — SMALL passes 4b nowhere.
```
Pooled at delay +0: 11 books pass 4b FULL at 0 bps, **median c\* 43.8 bps** (q25 42.9, q75 103.8) —
so on the cost axis alone the pre-registered 25 bps bar is cleared. Per panel: U56 median 103.8,
B136 median 43.1, SMALL none.

## 4. The capital arm: no IS-only chooser reaches a passing rung, anywhere
Gross chosen by argmax IS Sharpe on warm-up..2016-12-31 only, separately at each (cost, delay) cell
so the chooser pays the same cost and latency the book does; 2017-2026 read once.
**0 of 48 picks clear 4b on either window, and 0 of 48 clear 4a.** The chooser lands on
g = 0.95-1.00 at every one of the 48 cells, because IS Sharpe is flat-to-increasing in gross — and
those rungs blow the DD cap. At the realistic (25 bps, +1 day) cell:

| panel | pick | FULL | OOS | 4b full/OOS |
|---|---|---|---|---|
| U56 | g 0.95 | 18.71% / 1.0739 / -26.81% (H1/H2 1.1779/1.0033) | 20.07% / 1.0731 / **-26.81%** | False / False |
| B136 | g 1.00 | 23.10% / 1.1251 / -25.52% (1.3289/0.9684) | 23.16% / 1.0719 / **-25.52%** | False / False |
| SMALL | g 1.00 | 10.20% / 0.5240 / -45.48% (0.7045/0.3886) | 9.16% / 0.4742 / **-45.48%** | False / False |

Comparands: SPY 15.12% / 0.8844 / -33.72% (OOS 15.26% / 0.8738 / -33.72%), 4b bars DD cap -20.23%
and CAGR floor 10.59%; live RULES v2 @10bps U56 8.62% / 1.2011 / -12.05% (OOS 9.46% / 1.2769),
B136 1.0973 (OOS 1.1019), SMALL 0.7185 (OOS 0.6473). Over the whole 624-cell grid **4a fires 5
times full and 0 times OOS.**

**No RULES change proposed.** The 4b passes that exist in this grid are real but unreachable: they
sit at gross 0.50-0.75, and every legal IS-only chooser walks past them to gross 1.00.

## 5. Gates and caveats
12 gates, **0 FAIL**: G0 min 16.7y; **G1 frozen 2026-09-04 U56 anchor replayed at the (10 bps, +0)
cell to 3.72e-05**; G2 exactly two tuned parameters (cost rung, execution delay — the gross ladder
is the chooser's IS-only coordinate and N/H/MAXVOL/cadence are frozen inheritances); G3 cost ladder
an exact identity on one turnover path (0.00e+00); G4 max realised gross 1.000000 <= 1.0; G5 no
chooser reads a row on or after 2017-01-01; G6 all 624 cells published; **G7 delay +0 reproduces
the protocol convention bit-for-bit against an independently rebuilt lag-1 frame (0.00e+00)**;
G8 all 38 interior c\* bracketed (PASS at c\*-0.02 bp, FAIL at c\*+0.02 bp). Deterministic, offline,
23.0s.

**SURVIVORSHIP (rule 9):** U56 (55 names) and B136 (135) are current-constituent lists and SMALL a
current sub-$2B screen carried back to 2010 — 665 investable names after dropping the 54 tickers
with `max_1d_move >= 1.0` in `data/small_meta.csv` (the cached pool has grown well past the 439 and
483 figures older memos quote; the label, not the run, is stale). Every absolute level and every
4a/4b pass count is an UPPER BOUND. The run's headline is a DEGRADATION along two axes over the
SAME names on the SAME days, which the bias cannot manufacture.

**One honest limit on the delay result:** delay is implemented as reading the signal at close
t-1-d and trading at t, which holds the rebalance calendar fixed and only ages the signal. A real
latency would also move the fill price within the day. The sign and size of the MaxDD move is a
lower bound on what an execution study would find, not an upper one.
