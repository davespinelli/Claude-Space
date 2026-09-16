# Idea 1073 — is the CAP AXIS a STRENGTH dial rather than a SIGN dial? (lane C, 2026-09-16)

**ANSWER: the cap axis is a STRENGTH dial (H_SIGN PASS, rho > 0 in all 12 cells) — and the
attenuation is NOT a volatility object.  KILL the vol explanation.**

Vol matching was given three tolerances and a second, independent route, and it never took the
ordering away.  On the basis the run DECLARED (the gap), matching closes 18.8% / 50.5% / 28.3% at
tau = 0.45 / 0.30 / 0.20 — non-monotone, and never the 50% H_MATCH asked for at the tight rung.
On the basis the QUEUE's wording implies (the ratio), it closes 34.1% / 69.6% / 51.0%.  Both are
published; neither stands in for the other.  The crossing arm settles it: at matched name vol,
moving CAP shifts rho by **0.4063** while at matched cap, moving VOL shifts it by **0.1110** —
cap moves the dial **3.7x harder than vol does**.

## The published grid (2 dials, all 12 cells, none selected on)

| tau | q=0.00 | q=0.50 | q=1.00 | gap | ratio |
|---|---|---|---|---|---|
| UNMATCHED | +0.6886 | +0.5483 | +0.1182 | +0.5704 | 5.82x |
| 0.45 | +0.6745 | +0.5078 | +0.2113 | +0.4632 | 3.19x |
| 0.30 | +0.6816 | +0.5282 | +0.3992 | +0.2825 | 1.71x |
| 0.20 | +0.7077 | +0.5752 | +0.2986 | +0.4091 | 2.37x |

rho = partial Spearman(n/k, OOS Sharpe | k), 96 book rows per cell (8 draws x k in {20,30,40} x
n/k in {0.10, 0.20, 0.35, 0.50}).  V* = 0.25 by a declared feasibility rule (max min(nS,nB) at
tau=0.45 on a 0.01 grid), never by an outcome; the full 23-point grid is committed in
`.vstar.csv`.  G7: the dial binds — the q=1.00 / q=0.00 mean name-vol ratio falls
1.583 -> 1.239 -> 1.136 -> **1.055**, and panel-vol SD falls 0.0674 -> 0.0065.

## The crossing arm — the decisive cut

| cell | cap | mean IS name vol | rho |
|---|---|---|---|
| BSTK-LO | LARGE | 0.194 | **+0.8759** |
| BSTK-HI | LARGE | 0.325 | **+0.7649** |
| SMALL-LO | SMALL | 0.297 | **+0.3586** |
| SMALL-HI | SMALL | 0.549 | **+0.1769** |

BSTK-HI and SMALL-LO sit 0.028 apart in vol on opposite sides of the cap axis and read 0.41
apart in rho.  BSTK-HI and BSTK-LO sit 0.131 apart in vol on the same side and read 0.11 apart.
Vol is a real second-order dial (rho falls with vol *within* both pools) but it is not the
carrier of the cap ordering.

## The noise channel, priced

The queue's mechanism is real and measured: small-cap books ARE noisier — cross-draw SD of OOS
Sharpe **0.2193 (q=1.00) vs 0.1181 (q=0.00)**, reliability of a single book's OOS Sharpe
**0.0915 vs 0.5126**.  Disattenuating by that reliability moves the gap from +0.5704 to +0.5711
(closes **-0.1%**) and the ratio from 5.82x to 2.46x (closes 48.9% of the log-ratio).
Disattenuation multiplies, so it shrinks a ratio and leaves a difference alone — that is why the
two bases disagree, and it is why the "8x" wording is load-bearing in the original claim.
2 of 12 cells carry reliability < 0.05, all at q=1.00; their disattenuated rho (up to 4.47) is a
division by ~0 and carries no weight.  **That near-zero reliability is itself the finding: in
small caps the concentration dial barely moves OOS Sharpe more than the draw does.**

## Gates — 8 of 8 PASS, printed before any result

G1 fast runner == `engine.backtest` on returns (1.04e-17) and turnover (0.00e+00), cached-rank
CAND-20 == idea 286's committed `cand_weights(20)` (0.00e+00) · G2 envelope over all 473 panels,
0 violations, every name inside its declared vol window (not just the panel mean) ·
G3 no look-ahead (IS vol ranks +0.8424 against the full-sample vol it was not allowed to see) ·
G4 determinism · **G5 CROSS-RUN: idea 706's committed rho reproduces to max|d| 0.0000
(+0.7988 / +0.6520 / +0.1481)** · **G6 CROSS-RUN at the BOOK level: 356 of 356 REPRO rows join
706's committed `books.csv` on (q,k,draw,n), max|d OOS Sharpe| 2.22e-16** · G7 the tau dial binds
· G8 the V* grid published in full.

## Rule 8 and both KEEP paths

n/k chosen on 2009-2016 IS Sharpe ONLY inside each (cell, k, draw) choice set, 2017- read once.
Best matched cell: tau=0.30 q=0.00 RATIO-MAX **OOS 11.03% / 0.9503 / -19.04%**; the same selector
at q=1.00 reads **0.07% / 0.0621 / -29.87%**.  Comparands on the same panels: **SPY OOS 15.33% /
0.8767 / -33.72%**, **RULES v2 (live) OOS 4.57% / 0.6240 / -13.54%**.  **4a 0 of 1,892; 4b 81 of
1,892**, every 4b pass at q=0.00.  **NOTHING IS PROMOTED** — these are the record's committed
CAND-n books on random sub-panels of a survivor screen, so a 4b pass is a statement about the
draw, not about a rule.

## Limits and survivorship

The crossing arm's large-cap halves hold 45 names each, so its k=40 panels overlap heavily and
its 8 draws are not independent; the MATCH arm is the arm to weigh.  Matching only exists where
the pools overlap, so the matched small panels run at vol 0.260 against their pool's 0.415 —
nothing here extends to a high-vol small-cap book.  No interval is published for any rho, so
only the cell ORDERING and the SIGN are claimed (idea 1044's rule); a 0.28 and a 0.41 in this
table are not shown to differ.  Realised vol is one proxy for "small caps are noisier" — a
liquidity or factor-loading match is a different control and is not run.  SURVIVORSHIP (rule 9):
SMALL and BSTK are current constituents, so every CAGR level is optimistic and every 4b count an
upper bound; worse for this question, the vol used to match is measured on survivors, so both
arms inherit it.

Follow-ups filed: 1078, 1079, 1080 (renumbered from 1075-1077 on push: lane B took those numbers in the same hour — idea 932's numbering defect again).
