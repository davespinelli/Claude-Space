# Idea 1112 (cloud lane, 2026-09-16) — what COMPOSITION difference carries the U56-vs-B136 GATE ORDERING?

**ANSWERED = NONE OF THE THREE THE IDEA NAMES. It is carried by WHICH NAMES, at matched pool
size and matched ETF share.** Swapping U56's 20 megacaps for 20 other B136 large caps — holding
K at 56 and the ETF share at 36/56 — moves GATE by **+0.943 pp on average (mean share of the gap
+0.467, biggest of the four steps at 6 of 12 coords)**, more than doubling the pool from 56 to
136 names does (+0.724 pp, 4 of 12). **OVERLAP is refuted by construction** (U56 is a strict
SUBSET of B136, so its overlap statistic is 1.000 and has no variation to carry an ordering), and
**the queue's "cap mix" — the ETF-vs-single-name share, the only cap-like axis these two
committed panels differ on — is the smallest live step (0.284 pp) and points the WRONG WAY
(mean share −0.456)**. Gate-pass rate orders GATE worse than pool size or ETF share does
(mean rho −0.1260, same sign at only 8 of 12 coords). **CORRECTION to 1106's D1: the ordering is
not a per-cell fact** — it inverts at H=126 N=10 (−0.347 vs −0.307). And a **confound the record
has never named is measured and cleared**: U56 and B136 are served off *two different price
files* that disagree on 51 of the 56 tickers they share, but that VINTAGE step is only 0.069 pp,
so the committed ordering is composition and not data vintage. No RULES change, no book promoted,
no PROTOCOL edit (rule 6); RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py untouched.
SELECTION: this lane takes the FIRST eligible open idea (idea 1 of 2).

## The two dials and no more (PROTOCOL rule 4)

`MATCH` {NONE, SIZE, ETFSHARE, GATEPASS} — the matching variable that defines each 56-name family
drawn out of B136 — × `PANEL PAIR` {COMMITTED (U56@A, B136@B), VINTAGE (U56@A, U56@B)}.
**Six independent draws per random family, every draw published: 21 analysis instances × 12
coords = 252 cells, each with 2 nulls × 40 seeds.** `N` {5, 10, 20, 40} and `H` {5, 21, 126} are
1082/1086/1097/1106's committed coordinates, **not** dials; all 12 coords are published for every
instance. Everything else frozen at 1085/1097/1106's construction: cap INF, REBUILT DD-match, 40
seeds, 34 bisection steps, max_vol 0.60, gross 0.75, W cadence, 10 bps, LAG 1, CAND20 legs,
warm-up 260. **The null seed recipe keys on the TICKER SET, not the vintage**, so U56@A and U56@B
replay the same 40 orderings and the vintage step is the prices moving and nothing else.

## The confound found before any GATE was run, and why it had to be priced

`load_universe()` serves U56 out of `data/prices.csv`. `load_universe(broad=True)` **cannot**: 80
of the 136 broad tickers are absent from that file, so `load_prices` raises and `load_universe`
falls back to the separate weekly cache `data/prices_broad.csv`. The two files **disagree on the
56 tickers they share**: 51 of 56 columns differ, max relative price difference **3.63%** (NVDA),
max single-day return difference **723 bps**, mean |return difference| **1.94 bps/day**, and they
end on different days (2026-09-15 vs 2026-09-11). Every committed "U56 vs B136" comparison in the
record is therefore a comparison across two price vintages as well as two compositions. This run
puts all panels on the **common tape** (4,703 rows, 2008-01-02 .. 2026-09-11) so K and T match
across the vintage pair, and carries `U56@A_NATIVE` (U56 on `prices.csv`'s own 4,705-row index,
exactly as 1106 ran it) **only** as a reproduction gate.

## The four-step decomposition

U56@A → B136@B in four additive steps, each a GATE difference between two panels differing in one
axis, summing to the committed gap by construction (identity checked at 2.22e-16):

| step | what moves | mean step | mean \|step\| | mean share of gap | biggest at | resolved (>2 SE) |
|---|---|---|---|---|---|---|
| VINTAGE | same 56 tickers, other price file | −0.067 pp | 0.069 pp | +0.353 | 0/12 | 7/12 |
| IDENTITY | megacaps → 20 other large caps, K and ETF share matched | **+0.819 pp** | **0.943 pp** | **+0.467** | **6/12** | 6/12 |
| ETFSHARE | ETF share 0.643 → B136's 0.265, K matched | −0.085 pp | 0.284 pp | −0.456 | 2/12 | 4/12 |
| POOLSIZE | K 56 → 136, composition matched | +0.697 pp | 0.724 pp | +0.636 | 4/12 | 6/12 |

`GATEPASS` is not nested in the chain and is read as its own matched family and as a rank
correlation. Across the 21 instances at each coord: **ETF share** mean rho +0.2654 (same sign
10/12, mean |rho| 0.2856), **pool size K** −0.1908 (11/12, 0.2031), **gate-pass rate** −0.1260
(8/12, 0.1994), **mean pairwise return correlation** −0.1098 (8/12, 0.1629). No single-statistic
correlation reaches 0.30 in absolute value; the ordering is not a one-statistic fact.

## What each declared hypothesis did

HYPOTHESES **3 of 8** SUPPORTED. `H_IDENT` SUPPORTED (share ≥ 0.5 at 7/12). `H_VINTAGE`
SUPPORTED (|step| under 10% of the gap at 9/12; mean 0.069 pp against a mean |gap| of 1.370 pp) —
so the vintage confound is real in the data and **immaterial to GATE**. `H_RESOLVED` SUPPORTED
(the biggest step clears 2× its own seed SE at 10/12; the VINTAGE step's SE is paired over the 40
shared seeds, the other three are independent hypots). `H_ORDER` **REFUTED**: ordered at 11 of 12
coords, mean gap +1.363 pp, but **H=126 N=10 inverts** — 1106's D1 is a statement about rung
means, not about cells. `H_OVERLAP` **REFUTED BY CONSTRUCTION**, as pre-registered: U56 ⊂ B136 at
56 of 56, so overlap is 1.000 for the U56 arms and fixed for every drawn family.
`H_ETFSHARE` **REFUTED** (share ≥ 0.5 at 1/12, mean share −0.456 — the step is small *and*
opposes the gap). `H_POOLSIZE` **REFUTED** (5/12, one short of a majority; it is the runner-up,
not the carrier). `H_GATEPASS` **REFUTED** (mean |rho| 0.1994, below both K's and ETF share's).

## Gates: 10 of 10 PASS, printed before any result number

G0 U56 ⊂ B136 (so overlap has no variation) exact; G1 fast runner == `engine.backtest` 1.39e-17;
G1b `gross_rescaler(1.0)` == `nrun` 1.39e-17; G2 committed 936/1071/1082 W/H126 N=20 triple
3.18e-07; **G3 reproduces 1106's 12 committed U56 EDGE_OPEN/ELIG figures on its native tape** and
**G4 its 12 book CAGR/MaxDD/turnover triples** (0.00e+00); **G5 reproduces 1106's 12 B136 EDGE
figures** (0.00e+00, its tape *is* the common one); G6 gross 0.75 on every date a book holds
anything; G7 the vintage pair shares K and the tape; G8 every instance carries all 12 coords.

**Two gate-specification errors in this run's first pass, recorded rather than removed.** (i) G3
failed at 1.03 pp because the native twin was keyed `"U56NAT"` in the null seed recipe instead of
`"U56"`: with a different key it draws different orderings, so it was a fresh measurement wearing
a reproduction gate's label. The book triples (G4) passed at 0.00e+00 throughout, which is what
identified the cause. (ii) G6 failed at 5.69e-03 because it gated on *mean* gross being exactly
0.75, which a 56-name subpanel cannot satisfy: unlike B136 it can go **fully to cash** when no
name passes the 200d/vol gate. The corrected gate tests gross on the dates the book is invested
and the all-cash share is now published per cell as a MEASURED quantity — **0.0000% to 0.7592% of
post-warm-up rebalance dates (max on B56SZ2@B) against 0.0000% on B136**. After both fixes the
run was repeated end to end: **10 of 10 gates PASS and all 252 analysis cells are bit-identical
to the first pass** (max absolute difference 0.0 over 39 numeric columns; the decomposition,
ordering, correlation and hypothesis tables are byte-identical), so the two errors were in the
gates alone and no reported number moved.

## Rule 8 and both KEEP paths — nothing proposed

The PANEL is a real dial a book would have to choose, so it is walked: instance × N × H chosen on
2009–2016 alone, OOS read once, two declared choosers, each over all 21 instances and over the
committed pair alone. `C_SHARPE` picks badly both ways — B56SZ0@B N=10 H=5 (OOS 10.23% / 0.7643 /
−23.47%, all three OOS 4b legs FAIL, regret +0.4174) and B136@B N=5 H=126 (15.03% / 0.7687 /
−28.12%, FAIL, regret +0.4020) — both below SPY's OOS Sharpe of 0.8767. `C_GATE` picks better:
B56SZ0@B N=40 H=5 (11.01% / 1.0222 / −18.08%, OOS 4b PASS, regret +0.1596) and, on the committed
pair, U56@A N=40 H=5 (**12.37% / 1.1630 / −16.67%, OOS 4b PASS, full-sample 4b PASS, regret
+0.0077**) against SPY OOS 15.33% / 0.8767 / −33.72% and RULES v2-on-panel OOS 9.47% / 1.2782 /
−12.05%. **4a: 0 of 252** (A_DD 0/252 — no panel variant drew down less than the live book).
**4b full 26 of 252, 4b OOS 32, full AND OOS 26**; binding leg L_DD (fails 203 of 226 failures,
sole failure at 88), then L_CAGR (56, sole 4). By family: REF_U56 6/12, VINTAGE 7/12, B136 1/12,
SIZE 5/72, ETFSHARE 2/72, GATEPASS 5/72 — **the drawn 56-name subpanels pass 4b less often than
U56 itself does**, which is the same finding as the decomposition read through the KEEP paths.
The 26 passes carry drawdown headroom of +0.00 to +3.57 pp (median +1.24) and CAGR headroom
+0.29 to +6.02 pp (median +2.37); idea 1083 measured the 90% width of the drawdown-margin
quantity itself at **4.1–7.2 pp**, wider than every drawdown headroom here. **Nothing is proposed
as capital.**

GATE's own stability, for completeness: full-sample GATE ≤ 0 at 200 of 252 cells, OOS GATE ≤ 0 at
181 of 252, sign agrees full vs OOS at 217 of 252.

## What the record should take from this

1. **A "U56 vs B136" claim is a claim about which 80 single stocks B136 adds**, not about breadth
   and not about cap. The two panels are nested, so every committed contrast between them is
   confounded across three axes at once, and identity is the one that carries it.
2. **`load_universe()` and `load_universe(broad=True)` do not serve the same prices for the same
   ticker.** 51 of 56 shared columns differ, up to 3.63% in price and 723 bps in a single day's
   return. It costs GATE only 0.069 pp, but no committed cross-panel claim has ever stated it, and
   a level-valued statistic (rather than a within-pool contrast) could be moved much more.
3. **1106's D1 should be re-worded** from an "at all 5 rungs" ordering to an ordering of rung
   means: at cell resolution it fails at 1 of the 12 coords tested here.

## Survivorship (PROTOCOL rule 9)

U56 and B136 are current-constituent lists and so is every 56-name subset drawn from B136. Every
level here is optimistic and every 4a/4b count is an UPPER bound. GATE and the four steps are
within-pool contrasts over one tape and the bias very largely cancels out of them; it does NOT
cancel out of the 4b legs, measured against SPY, a real index.

Script: `2026-09-16_what-COMPOSITION-difference-carries-the-U56-vs-B136-GATE-ORDERING_cloud.py`
