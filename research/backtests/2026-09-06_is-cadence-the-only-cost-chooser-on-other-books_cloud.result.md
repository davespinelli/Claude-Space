# Idea 230 — is-cadence-the-only-cost-chooser-on-other-books (cloud lane, 2026-09-06)

**Verdict: KILL of the queue's conditional. Cadence is NOT the only dial a cost rung can
choose — it is only the dial that was cheapest to notice on idea 228's one book.** Across
**33 panel × book × dial cells** (3 panels × {TOPN control, V1C, EWALL} × their dials,
1792 grid points, every one in `.grid.csv`) the rung re-ranks **11 of 33 cells (33%)**, and
the re-ranks are spread over **three** dials: **K 5 of 9, N 3 of 6, V 3 of 9, G 0 of 9**.
Idea 228's stronger secondary claim — *"0 of 12 argmaxes move anywhere in 10→30 bps"* — also
**fails**: here **5 of 33 move above 10 bps** (B136/EWALL/V and B136/V1C/V at 20 bps,
SMALL439/V1C/N at 20, SMALL439/V1C/K and SMALL439/EWALL/K at 15). Between 10 and 30 bps the
ladder is a chooser on some books, not a level check on all of them.

**What survives of idea 228.** Two things. (1) **Cadence is still the dial the rung chooses
most often and most expensively**: K re-ranks in 5 of 9 cells and carries the largest cost of
ignoring the rung — taking the 0-bps pick and paying 30 bps gives up a mean **0.0717** and a
max **0.2913** Sharpe on K, against **0.0419 / 0.1488** on N, **0.0175 / 0.1408** on V, and
**exactly 0.0000 in all 9 G cells**. (2) **The mechanism predictor holds.** Idea 228's rule —
a rung re-ranks iff the 0-bps top-two Sharpe gap is smaller than the ladder's maximum 30-bp
tilt — is right in **26 of 33** cells, catches **11 of 11** actual re-ranks with **no false
negatives**, and over-fires 7 times. Pooled with 228 that is **14 of 14 actual re-ranks
caught, 10 false positives**: a necessary condition, never a sufficient one.

**The variable idea 228 could not see is the BOOK, not the dial.** Re-rankable cells by book:
**V1C 7 of 12, TOPN 2 of 12, EWALL 2 of 9**; cost of ignoring the rung by book: **V1C 0.0721
mean / 0.2913 max, TOPN 0.0144 / 0.1551, EWALL 0.0018 / 0.0118**. The live RULES v1 composite
book — the one that actually trades — is **an order of magnitude more cost-sensitive in its
dial choices than either alternative**, because the vol scaler pushes it into low-vol names it
then churns (23.7×/yr at B136 defaults vs EWALL's 10.9×). An equal-weight-all book is almost
immune: its argmax barely moves and, when it does, the cost of getting it wrong is ≤0.012
Sharpe. **"How much does the cost rung matter as a chooser" is a property of the construction,
and it is worst for the book in production.**

| panel | book | ρ(dial,turn) K | argmax K 0→30 bps | argmax N 0→30 | argmax V 0→30 | argmax G |
|---|---|---|---|---|---|---|
| U56 | TOPN (control) | −1.000 | **1w → 6w @5bps** | 40 all | off all | 0.12 all |
| U56 | V1C | −1.000 | **2w → 6w @10bps** | 40 all | off all | 0.12 all |
| U56 | EWALL | −1.000 | 4w all | — | off all | 0.12 all |
| B136 | TOPN | −1.000 | 4w all | **40 → 56 @10bps** | 0.80 all | 0.12 all |
| B136 | V1C | −1.000 | **2w → 4w @5bps** | **25→40→56 @5/10** | **0.20→0.80→off @10/20** | 0.12 all |
| B136 | EWALL | −1.000 | 4w all | — | **0.80 → off @20bps** | 0.12 all |
| SMALL439 | TOPN | −1.000 | 6w all | 15 all | off all | 0.02 all |
| SMALL439 | V1C | −1.000 | **1w→3w→8w @10/15** | **3 → 40 @20bps** | **0.60 → off @10bps** | 0.08 all |
| SMALL439 | EWALL | −1.000 | **8w → 13w @15bps** | — | off all | 0.12 all |

**The control reproduces idea 228 exactly on the two panels it shares** (U56 all four dials,
B136 all four, including B136/N's 40→56 at 10 bps and U56/K's 1w→6w at 5 bps), so this is a
widening of 228's census, not a contradiction of its arithmetic. The one control row that
differs is **SMALL439/K, where 228's third re-rank disappears**: 228 read the *unscreened*
SMALL484 panel, this run drops the 44 tickers with `max_1d_move ≥ 1.0` per `data/small_meta.csv`
and the K argmax is then 6 weeks at all seven rungs. **One of idea 228's three re-ranks was a
data artefact of unscreened split/error bars.**

**Why G is the dial no rung can ever choose, on any book or panel.** Its argmax is 0.12 (the
grid edge) in 8 of 9 cells and is *also* its lowest-turnover point (ρ(G, turnover) = −1.000 to
−0.643, 3.5×/yr at g=0.12 vs 10.9× at g=0.00), so the ladder tilts the leader in the direction
it is already winning. That is exactly the structure idea 155 described for its q dial —
which makes it a property of *some* dials, as 228 argued, and G is a second clean instance.
The 0.12 argmax sits on the grid edge and is **not** a recommendation: it is untested beyond
12%.

**Rule 8 (dial chosen on 2009–2016 at each rung, 2017–2026 read once; 231 cells).** Headline
mean d(pick − do-nothing) is **+0.0329**, winning 62.3%, against a random dial's −0.0099 — but
**that number is a cost artefact and should not be quoted without the rung breakdown**:

| rung | 0 | 5 | **10** | 15 | 20 | 25 | 30 |
|---|---|---|---|---|---|---|---|
| mean d(pick − do-nothing) | −0.0161 | −0.0075 | **−0.0049** | +0.0357 | +0.0482 | +0.0694 | +0.1055 |
| win rate | 36.4% | 42.4% | **51.5%** | 69.7% | 75.8% | 75.8% | 84.8% |

**At PROTOCOL's own 10 bps the IS chooser is −0.0049 and wins 51.5% of cells — a coin flip,
the eleventh reproduction of ideas 132/141/151/160/189.** The positive full-ladder mean is
entirely 15–30 bps, where the do-nothing default (weekly, n=20) is bleeding turnover and *any*
selector that notices cost beats it — the random dial improves monotonically over the same
rungs (−0.0275 → +0.0076). Excluding the V dial (228's "switch the gate off" corner) the mean
is +0.0422; excluding V *and* G (whose chooser also runs to a grid corner) it is +0.0308 —
i.e. this run's premium is not one corner, it is the cost ladder itself. By dial:
G +0.0613 (74.6% wins), K +0.0325 (60.3%), N +0.0283 (61.9%), V +0.0079 (52.4%). The IS pick
moves with the rung in **17 of 33** cells, up from 4 of 12 in 228.

**OOS levels at 10 bps** (2017-01-01 → 2026-09-04), do-nothing book of each cell: U56 TOPN
**1.1683 / 19.22% / −23.98%**, U56 V1C 1.0286 / 14.18% / −22.79%, U56 EWALL 1.1119 / 15.14% /
−20.88%; B136 TOPN 0.8937 / 16.51% / −26.20%, B136 V1C 0.7470 / 10.17% / −22.88%, B136 EWALL
**1.0175 / 14.09% / −23.09%**; SMALL439 TOPN 0.4881 / 9.04% / −36.39%, V1C 0.3617 / 4.87% /
−36.99%, EWALL 0.2929 / 3.79% / −50.02%. RULES v1 baseline OOS 0.7471 (U56) / 0.5763 (B136) /
0.4923 (SMALL439); **SPY 0.8820 / 15.45% / −33.72%**. Full sample at 10 bps the literal live
book (n=5, w=0.15) is U56 6.45% / 0.6642 / −13.83%, B136 6.39% / 0.6350 / −21.19%, SMALL439
7.41% / 0.5647 / −36.12%; SPY 15.23% / 0.8890 / −33.72% (H1 0.957 / H2 0.834).

**KEEP paths, all 1792 points.** 4a **245/1792**, all on B136 (156) and SMALL439 (89); **U56
0 of 595**, always on drawdown against the live low-vol book — idea 136's standing diagnosis,
reproduced a seventeenth time. 4b **49/1792**: **48 on U56** (EWALL 24, TOPN 12, V1C 12) and
**1 on B136** (EWALL, max_vol=0.30, 0 bps only). **SMALL439 passes 4b 0 of 595.** The best
point in the run is `U56 / EWALL / g = 0.03`, which clears 4b at **all seven rungs**
(10 bps: CAGR **15.05%**, Sharpe **1.1348**, MaxDD **−19.95%**, H1 1.1131 / H2 1.1576,
OOS **1.2314**, 6.4×/yr turnover, 100% invested) — better than idea 228's U56/n=40 on every
bar. **It is recorded, not promoted**, for the reason 228's was: on B136 the identical
construction fails 4b on drawdown (**−22.12% against the −20.23% cap**) at every rung, so it
is a one-panel book; and per idea 144 a re-dialled book is the same book — this is idea 57's
`ew-band3` at gross 1.00, already in the record. No RULES change, no memo, no promotion.

**Caveats.** Current-constituent survivorship on B136 and SMALL439 (idea 54) flatters every
long book quoted here; SMALL439 additionally drops 44 names on `max_1d_move ≥ 1.0`, which is a
data screen and not a tradable rule. Costs are flat linear bps on turnover, not spread-and-
impact (idea 126). Two tuned parameters only (dial value, cost rung); the three books are
pre-registered — two named by QUEUE 230, one the parent's own construction as a control. The
G and V argmaxes sit on grid edges and are reported as grid edges. EWALL has no count dial and
contributes 3 dials rather than 4; that is stated rather than invented.

**Reproduction.** `python research/backtests/2026-09-06_is-cadence-the-only-cost-chooser-on-other-books_cloud.py`
(94 s). The cost identity `net(c) = gross − turnover·c/1e4` matches `engine.backtest` at
10 bps to 1.4e-17 on all three panels. Console in `.console.txt`; census in `.census.csv`;
predictor in `.mechanism.csv`; rule 8 in `.walkforward.csv`; pass counts in `.keep.csv`.

**Follow-ups for the queue:** (233) does the cost rung's chooser-power track a book's turnover
level directly — regress `cost_of_0bps_pick_at_30` on default turnover across these 33 cells
plus 228's 12; (234) re-read every published dial argmax whose parent quoted only one rung, and
flag the ones whose book is V1C-shaped (high turnover, vol-scaled ranking); (235) the rule-8
premium is monotone in the cost rung on both the chooser AND a random dial — test whether the
"selection beats do-nothing" claim in any published run is just the run's rung being above the
book's own turnover break-even.
