# Idea 1346 (lane cloud, 2026-09-19) — does DE-GROSSING buy back the 4b DD LEG on the ONE PANEL WHOSE CADENCE ARGMAX IS MONTHLY?

**VERDICT: ANSWERED YES, MECHANICALLY — and PARK, NOT KEEP.** Gross 0.50 does buy back B136
monthly's drawdown leg exactly as the idea predicted, producing a cell that clears 4b on every leg
full-sample AND out-of-sample and beats the frozen incumbent's Sharpe by +0.0304. Rule 8 never
reaches it: the in-sample chooser picks (0.75, W) on B136, because **B136's monthly advantage is
wholly a post-2017 fact** (IS M−W = **−0.0307**, OOS M−W = **+0.0808**).

## 1. The DD leg is bought back, and the CAGR floor survives it

B136, 4b bars: DD cap −20.23%, CAGR floor 10.59% (SPY 15.12% / 0.8845 / −33.72%).

| gross | cad | CAGR | Sharpe | MaxDD | DD margin | CAGR margin | H1/H2 | OOS Sharpe | 4b full+OOS |
|---|---|---|---|---|---|---|---|---|---|
| 0.40 | M | 9.54% | 1.0917 | −15.57% | +4.66 pp | **−1.04 pp** | 1.232/1.004 | 1.1153 | no (CAGR) |
| **0.50** | **M** | **11.97%** | **1.0934** | **−19.21%** | **+1.02 pp** | **+1.39 pp** | **1.233/1.007** | **1.1175** | **YES** |
| 0.60 | M | 14.42% | 1.0950 | −22.76% | **−2.53 pp** | +3.83 pp | 1.234/1.009 | 1.1196 | no (DD) |
| 0.75 | M | 18.11% | 1.0973 | −27.90% | −7.67 pp | +7.53 pp | 1.235/1.013 | 1.1226 | no (DD) |
| 0.60 | W | 13.43% | 1.0630 | −15.97% | +4.26 pp | +2.85 pp | 1.232/0.941 | 1.0387 | yes (anchor) |

The window is exactly one rung wide: **0.50 is the only monthly gross on which both margins are
non-negative**, because the two margins move in opposite directions in gross and cross between
0.40 and 0.60. Idea 1335's −22.76% / 2.53 pp shortfall at gross 0.60 is reproduced exactly.
On U56 the monthly window is also one rung wide (0.60 only); on SMALL there is no rung at all.

## 2. Why de-grossing is the DD dial and not a Sharpe dial

Uninvested gross sits in cash at 0%, so mean and vol scale together and only the 10 bps turnover
drag — which does NOT scale — breaks the invariance. Measured, per (panel, cadence), over the four
gross rungs: **Sharpe spread 0.0014–0.0055, MaxDD spread 8.79–18.01 pp, CAGR spread 2.61–8.57 pp.**
De-grossing is a pure DD/CAGR exchange (B136 M: +3.54 pp of MaxDD for −2.45 pp of CAGR at
0.60→0.50) and buys ~nothing in Sharpe. That is precisely what makes it a legitimate way to pay a
DD cap — and also why it cannot create a 4b pass where the CAGR floor is the binder.

## 3. M vs W is gross-invariant, and it is a post-2017 fact

| panel | M − W full Sharpe (g0.40→0.75) | M − W OOS Sharpe | M − W IS Sharpe at g0.60 |
|---|---|---|---|
| U56 | −0.1078 → −0.1049 | −0.1079 → −0.1050 | −0.1078 |
| **B136** | **+0.0309 → +0.0327** | **+0.0791 → +0.0821** | **−0.0307** |
| SMALL | −0.1439 → −0.1415 | −0.2218 → −0.2186 | −0.1418 |

B136 is still the only monthly panel and the sign is stable across the whole gross ladder, so
1335's headline replicates. But the *in-sample* sign is the opposite one: on warm-up..2016-12-31
B136's monthly book is **worse** than its weekly book by 0.0307 of Sharpe, and the entire +0.0808
of OOS advantage arrives after 2017. A chooser standing in 2016 would have rejected it.

## 4. Rule 8

(GROSS, CADENCE) chosen on warm-up..2016-12-31 by argmax IS Sharpe, 2017-2026 read ONCE.

| panel | IS pick | IS margin over anchor | OOS pick / anchor Sharpe | d OOS Sharpe | d OOS MaxDD | ex-post best OOS |
|---|---|---|---|---|---|---|
| U56 | (0.75, W) | +0.00034 | 1.1971 / 1.1965 | +0.0006 | −3.76 pp | (0.75, W) |
| B136 | (0.75, W) | +0.00121 | 1.0405 / 1.0387 | +0.0018 | −3.69 pp | (0.75, **M**) 1.1226 |
| SMALL | (0.75, M) | +0.05235 | 0.3460→0.2548 / 0.4728 | **−0.2180** | −7.31 pp | (0.75, W) |

Mean d OOS Sharpe **−0.0718**; beats the incumbent 2 of 3 but by +0.0006 and +0.0018 on margins of
+0.00034 and +0.00121 of IS Sharpe — i.e. the chooser is indifferent to three decimal places and
is buying a **deeper** drawdown (−3.7 pp) for a Sharpe gain in the fourth. On SMALL the same
chooser, facing its one large IS margin (+0.052), loses 0.218 of OOS Sharpe. **The (0.50, M) cell
that answers the idea's question is never selected on any panel.**

**A caution on the rule-8 pick itself:** U56 (0.75, W) clears the 4b DD cap by **+0.09 pp**
(−20.14% against −20.23%). Idea 1253 measured that one weekday of execution slippage costs this
family up to 2.18 pp of MaxDD. That pass is inside its own execution noise and should not be read
as a book.

## 5. Keep paths and gates

**4a 0 of 24** (unreachable: RULES v2's −12.05% MaxDD). 4b full 8 of 24, 4b full+OOS **8 of 24**
(U56 4/8, B136 4/8, **SMALL 0 of 8**). By cadence: W 6/12, M 2/12. By gross: 0/3/3/2 at
0.40/0.50/0.60/0.75. Binding legs over all 24 cells: **CAGR 13 > DD 11 > H1 8 = H2 8**.

4/4 asserted gates pass. **G1 is a cross-script within-day replay: the (0.60, W) cell reproduces
the anchor committed earlier today by this lane's idea-1296 script on ALL THREE panels to
max deviation 8.3e-17 / 2.2e-16 / 8.3e-17** across CAGR, Sharpe, MaxDD, H1, H2 and turnover — and
that U56 row is itself bit-identical to idea 1335's committed number. G0 sample ≥ 10y on all three.

SURVIVORSHIP (rule 9): U56 / B136 / SMALL are current-constituent lists; SMALL is a sub-$2B screen
carried back to 2010 (`data/small_meta.csv` drops the `max_1d_move >= 1.0` names), so its LEVELS
are an upper bound and only its CONTRASTS across gross and cadence are read here. B136's
current-constituent bias is the obvious alternative explanation for a monthly edge that exists only
after 2017 and is NOT priced here.

Deterministic, offline, 13.5s.
