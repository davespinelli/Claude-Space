# Idea 2256 — does the both-paths cell's turnover floor move if the two legs run on different clocks?

**2026-09-22, lane cloud, run 12.** Script `2026-09-22_split-clock-legs_cloud.py`.
128 cells published (2 panels x 4 equity clocks x 4 sleeve clocks x 4 cost rungs). 6 of 6 gates exact.

## ANSWERED = NO, and the grid closes the question rather than sampling it

**0 of 96 split-clock cells trade less than their own (panel, cost) cell's best same-clock rung.**
Annual turnover is **monotone non-increasing in each clock separately at every one of the 8
(panel, cost) cells**, so the minimum of the 4x4 grid is always the slow/slow corner, which is a
SAME-clock rung. The best split pair (Q/M) costs **+0.30x/yr on u56 and +0.31x/yr on broad**
against the best same-clock rung (Q/Q). A split clock is the union of two rebalance schedules: it
removes no trading dates and adds the trades needed to pull a freshly-refreshed leg back against
a stale one. **KILL of the device.**

| panel | committed (W,W) | best same-clock | best split | floor moved | live RULES v2 |
|---|---|---|---|---|---|
| u56   | 8.18x/yr | **2.40x (Q,Q)** | 2.70x (Q/M) | **+0.30x** | 1.77x |
| broad | 10.88x/yr | **2.94x (Q,Q)** | 3.25x (Q/M) | **+0.31x** | 2.01x |

The floor also does not reach the live book: the lowest turnover ANY of the 16 clock pairs
attains is **1.35x the live book's** (u56) and **1.46x** (broad), and the pre-registered
turnover-constrained chooser **C_TO abstains at 8 of 8 cells** — no clock pair gets its IS
turnover under the live book's own.

## The result worth capital came off the DIAGONAL, not off the device

G6 proves the diagonal IS the committed cadence ladder (`(f,f)` reproduces
`engine.backtest(freq=f)` to <1e-12 on returns and turnover), so the run's own comparand arm
prices something the record had not: **the committed `S3-50 + band3-rw` book run MONTHLY — both
legs, gate included.** Idea 2250's cadence work slowed only the RANK refresh and kept the gate and
sleeve weekly, reaching 5.81x/yr at its M rung; refreshing the whole book monthly reaches
**3.87x/yr with a HIGHER Sharpe and a SHALLOWER drawdown** (1.3171 / −10.35% against 2250's M rung
1.2978 / −11.09% and the committed weekly cell's 1.2634 / −11.63%).

u56, both legs monthly, t+1, gross 0.75, band 3%, blend 0.50, n=20:

| cost | CAGR | Sharpe | MaxDD | H1 / H2 | OOS CAGR/Sharpe/MaxDD | TO | 4a | 4b |
|---|---|---|---|---|---|---|---|---|
| 5 bps  | 12.28% | 1.3386 | −10.34% | 1.3489 / 1.3307 | 12.91% / 1.3790 / −10.34% | 3.87x | YES | YES |
| 10 bps | **12.06%** | **1.3171** | **−10.35%** | **1.3256 / 1.3109** | **12.71% / 1.3591 / −10.35%** | 3.87x | YES | YES |
| 25 bps | 11.41% | 1.2524 | −10.38% | 1.2555 / 1.2511 | 12.09% / 1.2990 / −10.38% | 3.87x | YES | YES |
| 50 bps | 10.34% | 1.1435 | −10.43% | 1.1374 / 1.1504 | 11.06% / 1.1978 / −10.43% | 3.87x | YES | no (4b OOS still YES) |

broad reads 13.19% / 1.2615 / −11.13% at 10 bps (halves 1.4733 / 1.0735, OOS 12.20% / 1.1432 /
−11.13%, 4.97x/yr) and clears BOTH paths at 5/10/25/50 bps.
Comparands at 10 bps: live RULES v2 u56 8.62% / 1.2010 / −12.05% (halves 1.2276/1.1806, OOS
1.2767), SPY 15.14% / 0.8851 / −33.72% (halves 0.9570/0.8264; OOS 15.29% / 0.8751 / −33.72%), so the 4b bars are CAGR ≥ 10.60%
and MaxDD ≥ −20.23%.

**Rule 8 reaches it.** C_DIAG — the same IS-Sharpe argmax restricted to the 4 same-clock rungs,
i.e. ONE parameter instead of two — picks **(M,M) at 8 of 8 panel x cost cells** on 2009–2016
alone and clears 4a at 8/8, 4b FULL at 7/8 and 4b OOS at 7/8 out of sample.
**DISCLOSURE: C_DIAG is POST-HOC.** It was added after the first run showed every split cell
dominated; the pre-registered chooser C_SHARPE (argmax over all 16 pairs) picks the SPLIT pair
M/W at 6 of 8 cells — which itself clears 4a+4b on u56 at 5/10/25 bps but trades 4.74x/yr and is
dominated by (M,M) on turnover, Sharpe and drawdown, and fails 4a on broad.

## Counts and caveats

- KEEP paths over all 128 cells: **4a 40, 4b 71, BOTH 39** (27 of the 39 are split cells, all of
  them dominated on turnover by a same-clock rung in the same (panel, cost) cell).
- At 25/50 bps: **8 of 64** cells clear BOTH paths; 6 of those 8 are (M,M) or (M,Q).
- Gates: G1 book identity 1.1e-16 · G2 degenerate limit 6.9e-18 / 4.2e-16 · G3 idea-142 re-run
  max d 3.7e-04 · G4 leg additivity 3.6e-15 · G5 128/128 published · G6 diagonal = engine ≤2e-15.
- **Survivorship (PROTOCOL rule 9 / idea 54):** u56 and broad are 2026 constituents held from
  2008, so every CAGR level is optimistic and both 4b level legs are easier than on a
  point-in-time panel. Turnover contrasts are same-tape / same-names and first-order immune; the
  pass counts are not.
- Costs are flat per unit turnover: no spread, impact or borrow. One execution delay (t+1), one
  blend, one band, one gross, one sleeve. The mean realised gross of the (M,M) cell is 0.7513, so
  the monthly rung is not buying its numbers with extra exposure.
- This run proposes no rules change; PROTOCOL rule 6 gives that to the Sunday review.
