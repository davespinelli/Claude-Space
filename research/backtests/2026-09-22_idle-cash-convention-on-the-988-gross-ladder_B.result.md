# Idea 2286 (lane B, 2026-09-22) — does the IDLE-CASH CONVENTION change any committed GROSS-LADDER verdict?

**Verdict: ANSWERED = NO on the question that matters, and YES on one nobody had asked.
KILL of the "close the gap from the low side" premise.**

## The question

Idea 988 walked the live `BAND03` shape over gross 0.25–1.50 x cadence {D,W,M} x 3 panels and found
BOTH KEEP paths clear at **0 of 234**, with a measured mechanism: 4a's drawdown leg CAPS gross while
4b's CAGR floor FLOORS it, the two windows DISJOINT on 9 of 9 cells. Every one of those 234 books pays
**exactly 0%** on its uninvested residual, which on the live band book averages **46.7% of NAV** (U56)
— 58.8% on SMALL. The queue line's hypothesis: a carry sleeve lifts CAGR at every rung *below* g = 1.00
while leaving drawdown alone, so it is the one device that could close the gap **from the low side**.

## Design

988's ladder verbatim. **Two tuned parameters and no more**: gross g = 0.25..1.50 in 0.05 steps
(26 rungs) x carry {OFF, ON}. Published-not-tuned: panel {U56, B136, SMALL} x cadence {D, W, M} x
window {FULL, H1, H2, IS, OOS}; band c = the live 0.03; cost 10 bps; t+1. Two published control arms,
never selected over: **ON_SPREAD** (borrowing above g = 1.00 charged at proxy + 150 bps/yr) and
**FLAT2** (a flat 2.0%/yr both sides, to separate the RATE from SHY's own path). **945 published rows.**

Carry is applied **inside the drift** — the cash leg grows at (1+c) and the book renormalises through
the grown total — not added to the return afterwards. Proxy = **SHY** from the committed
`data/prices_broad.csv` (+1.31%/yr over the sample; IS +0.81%, OOS +1.72%). No network.

**Gates, all realised:** G0 SMALL blow-ups dropped = **54**. G1 the local runner reproduces
`engine.backtest` at c = 0 to **2.8e-16 / 3.2e-16** of return on all three panels, and G1b its live cell
IS `baseline.rules_v2_weights` to the same tolerance — so arm OFF is 988's numbers, not a re-derivation.
G2 `rules_v2_weights` is exactly linear in gross, max|d| **0.0**. G3 arm ON with the rate zeroed
collapses onto OFF at **0.0e+00**. G4 the credit is positive at the live cell on all three panels
(+0.56 / +0.58 / +0.80 pp/yr). G5 no unlevered rung ever runs a negative residual (min idle **+28.9%**).
G5b only **13.3%** of levered rungs run a *mean* negative residual — the band gates names out, so above
g = 1.00 the convention is a MIXTURE of credit and charge, not a pure financing cost; stated, not repaired.
G6 turnover is not identical across arms (max spread **1.6e-03 x/yr**) because carry changes the drift.
**External gate:** the credit regresses on idle NAV at **+0.01357 pp of CAGR per idle pp, rho 0.9917**,
reproducing idea 2213's independently-measured +0.0139–0.0184 / rho 0.9933–0.9992.

## A. The answer to the queue's question: NO, at 0 of 234, under every arm

| arm | keep4a | keep4a **matched** | keep4b | keep_BOTH | keep_BOTH **matched** | n |
|---|---|---|---|---|---|---|
| OFF (988's convention) | 9 | 8 | 35 | **0** | **0** | 234 |
| ON | 98 | 78 | 38 | **0** | **0** | 234 |
| ON_SPREAD | 98 | 78 | 38 | **0** | **0** | 234 |
| FLAT2 | 96 | 79 | 44 | **0** | **0** | 234 |

Unlevered subset (g <= 1.00, the only rungs PROTOCOL rule 2 permits): **0 of 144 on BOTH, every arm.**
Rule-8 picks clearing BOTH: **0 of 108**. 988's headline survives the fix intact.

**Why it cannot close the gap.** The gap `g_min(4b CAGR floor) − g_max(4a DD leg)` narrows by
**0.05–0.10 of gross and never to zero**: U56/W 0.20 → 0.15, U56/D 0.15 → 0.15, U56/M 0.30 → 0.25,
B136/D 0.25 → 0.15, B136/W 0.30 → 0.25, B136/M 0.45 → 0.35. On SMALL the 4b floor is unreachable at
any rung under any arm. The credit is proportional to idle NAV, so it lifts the LOW-gross end hardest
(+0.7997 pp mean CAGR unlevered vs **+0.2084 pp levered**, and −0.2277 pp at worst where the residual
is negative) — it moves **both** window edges up by about one rung and leaves the distance between them.

## B. And the thing nobody had asked: 4a on this ladder is convention-dependent

Arm OFF → ON flips **89 of 234** 4a verdicts, and **70 of 234 even when the yardstick is re-run under
the same convention** (`keep4a_matched`: the live RULES v2 g = 0.75 book has 46.7% idle NAV of its own,
so crediting the candidate while leaving the yardstick at 0% hands every candidate the same free
+0.8 pp; the matched leg removes that). 4b moves only **+3 of 234**. The flips are spread evenly:
8–10 per (panel, cadence) cell on all 9. **The record's committed 4a counts on a gross ladder are a
statement about the 0% cash convention, not only about the book.**

At the live cell (g = 0.75, W) the convention is worth, FULL / OOS:
U56 8.62% → **9.23%** CAGR, 1.2010 → **1.2818** Sharpe, −12.05% → **−11.47%** MaxDD (OOS 9.46% → 10.25%,
1.2767 → 1.3692); B136 7.96% → 8.59% / 1.0972 → 1.1811 / −12.24% → −11.63%; SMALL 4.26% → 5.10% /
0.6596 → 0.7787 / −14.16% → −13.30%. **Every one of those "4a passes" is zero once the yardstick is the
same book under the same convention** — `keep4a_matched` is False at the live cell on all three panels.
This is idea 2221/2213's KILL of the T-bill sweep as a rules change, reproduced at 3 cadences.

## C. Rule 8 — the fix INVERTS the chooser, and costs 7–8 pp of OOS CAGR

g chosen on 2009–2016 IS Sharpe only, unlevered ruler, 2017–2026 read once. Under **OFF** the chooser
picks **g = 1.00 on 9 of 9 cells**; under **ON, ON_SPREAD and FLAT2 it collapses to the ladder floor
g = 0.25 on 9 of 9**, because crediting idle NAV rewards de-grossing in Sharpe while CAGR is left behind.
OOS CAGR of the pick: U56/W **12.67% → 4.55%**, B136/W 10.47% → 4.05%, SMALL/W 4.76% → 2.78%.
OOS Sharpe rises (1.2760 → 1.6281 on U56/W) and every one of those picks **fails 4b on the CAGR leg
alone**. This reproduces idea 2213(D)'s inversion on a ladder that 2213 never ran.

## D. OOS vs baseline and SPY (2017–2026, read once)

U56: SPY **15.29% / 0.8751 / −33.72%**; RULES v2 live 9.46% / 1.2767 / −12.05%; the best unlevered
4b-passing ON cell (g = 1.00, W) **11.88% FULL / 1.2347 / −15.62%, halves 1.2554 / 1.2203, OOS 13.12% /
1.3148** — 4b PASS, **4a matched FAIL**, so BOTH still 0. B136: SPY 15.26% / 0.8737; best ON 4b cell
(g = 1.00, W) 11.00% / 1.1335 / −15.83%, OOS 10.98% / 1.1472, 4a matched FAIL. SMALL: **no rung clears
the 4b CAGR floor under any arm.**

## Verdict

**KILL** of the premise (the cash convention is not the device that closes 988's disjoint KEEP windows —
0 of 234, 0 of 144 unlevered, 0 of 108 rule-8 picks, under four conventions including two that are
deliberately generous), **plus a documented CONVENTION-DEPENDENCE finding**: 70 of 234 committed 4a
verdicts on this ladder are an artefact of the 0% cash convention even after the yardstick is matched,
and the record has never published a gross-ladder 4a count with its cash convention named.
**No KEEP-candidate; no memo.**
