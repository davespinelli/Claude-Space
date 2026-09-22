# Idea 911 — does the DD-RESIDUAL's IS-to-OOS persistence survive an EPISODE-PRESERVING null?

**Lane cloud, 2026-09-22.**  **ANSWERED — YES, IT SURVIVES, AND THE RECORD HAD THE MECHANISM
BACKWARDS** (the persistence lives OUTSIDE the crash, not inside it) **+ a KILL of the residual as
a capital chooser** (0 of 3 arms reach 4b).  Script:
`2026-09-22_dd-residual-episode-null_cloud.py`.  Persistence grid `.persistence.csv` (36 rows, all
published), shelf `.shelf.csv`, capital picks `.walkforward.csv`, gates `.gates.csv`.

Shelf: 80 books per panel (MOM/MOMVS/MADIST/LOWVOL × k∈{5,10,20,40,ALL} × gross∈{0.25,0.50,0.75,
1.00}), monthly, fills t+1, 10 bps, gate close>200dMA & vol20<0.60 — 867's own construction.
Panels U56 / B136 / SMALL665 (54 dropped for max_1d_move ≥ 1.0), 18.7 / 18.7 / 16.7y.
Gates G0 (sample), G2 (a 100% SPY book reads beta 1.0000 on every estimator), G3 (no leverage) all
PASS.  IS deepest listed SPY episode = 2011 EU crisis on all three panels; OOS deepest = 2020 COVID.

## Arm 1 — the persistence reproduces, and EXCISION RAISES IT
Full-window persistence of the MaxDD-on-beta residual, corr(res_IS, res_OOS) across the shelf,
against a 400-draw label-shuffle null:

| panel | OLSD | OLSM | DOWN |
|---|---|---|---|
| U56 | **+0.837** | **+0.742** | **+0.920** |
| B136 | **+0.343** | **+0.361** | **+0.559** |
| SMALL665 | **+0.365** | +0.041 (n.s.) | **+0.506** |

8 of 9 blocks are outside the shuffle null's ±2σ band, so 867's +0.343 to +0.590 reading
**reproduces** (B136/SMALL sit in that range; U56 reads higher).  **V1 NOT TRIGGERED**: excising
each window's dominant episode drops persistence below half its full value on **0 of 9** positive
blocks — it *raises* it on 8 of 9 (B136 OLSD +0.343 → **+0.853**; SMALL OLSM +0.041 → **+0.571**;
U56 OLSD +0.837 → +0.844).  Excising *every* listed crash raises it too (U56 OLSD → +0.932).
So the persistence is **not** a read of which books sit on the crash.

## Arm 2 — the SPLIT: the crash is where the residual does NOT persist
Non-episode residual persistence is significant on **9 of 9** blocks (+0.328 to +0.954), while
EPISODE-ONLY persistence is weak or **negative** (−0.385 to +0.449, negative on 4 of 9: B136 OLSD
−0.292, B136 OLSM −0.148, B136 DOWN −0.031, SMALL OLSM −0.385).  **V2 NOT TRIGGERED**, and the
direction is the finding: the DD residual is a **quiet-tape** book property.  Inside the crash the
cross-book ordering of drawdown-at-matched-beta does not carry from one window to the next at all.
The record's framing — "the residual may be a crash-seat read" — is exactly inverted.

## Arm 3 — CAPITAL: a KILL (rule 8, 2017–2026 read once)
A legal IS-only DD-residual chooser (pick the shelf book with the shallowest IS drawdown at
matched IS beta) reaches **0 of 3** arms clearing 4b FULL+OOS; so does the IS-Sharpe control.
**V3 NOT TRIGGERED.**

| panel | chooser | pick | OOS CAGR / Sharpe / MaxDD | SPY OOS | 4b |
|---|---|---|---|---|---|
| U56 | IS_RESID | MADIST/ALL/g1.00 | 17.45% / 1.217 / **−22.18%** | 15.29% / 0.875 / −33.72% | fail (DD bar −20.23%) |
| U56 | IS_SHARPE | MOM/5/g1.00 | 20.92% / 0.845 / −34.61% | — | fail |
| B136 | IS_RESID | MADIST/40/g1.00 | 18.28% / 1.054 / −29.35% | 15.26% / 0.874 / −33.72% | fail |
| B136 | IS_SHARPE | MOM/20/g1.00 | 20.81% / 1.002 / −33.68% | — | fail |
| SMALL665 | IS_RESID | MADIST/40/g1.00 | 7.33% / 0.438 / −48.02% | 15.29% / 0.875 / −33.72% | fail |
| SMALL665 | IS_SHARPE | LOWVOL/10/g1.00 | 4.71% / 0.444 / −35.26% | — | fail |

The residual chooser does beat the Sharpe chooser on OOS Sharpe on all three panels (1.217 vs
0.845; 1.054 vs 1.002; 0.438 vs 0.444 — two of three) and on OOS MaxDD on all three, so it is not
noise; it simply does not reach the 4b bar.  U56's pick misses the DD leg by 1.95 pp.  No
KEEP-candidate, no 4a pass, no memo.

## Honest limits
1. **Splicing changes the statistic.** The drawdown of an episode-excised series is not a drawdown
   any investor experienced; it measures "how deep did this book get outside the listed crashes".
   That is the right object for the question asked, and it is not a tradeable quantity.
2. **The residual may be a FAMILY label, not a continuous book property.** The across-shelf OLS
   residual separates MADIST/LOWVOL from MOM, and both capital picks landed on MADIST. Within-family
   persistence was not measured here — filed as idea 2079.
3. **Survivorship (rule 9).** U56/B136 are current-constituent lists, SMALL a current sub-$2B
   screen. Every MaxDD LEVEL is optimistic. The persistence CONTRAST (full vs excised vs
   non-episode) is same-shelf / same-tape with only the return window carved, so it is first-order
   immune; the capital arm's LEVELS are not.
