# Idea 1114 — is the FLOOR CLAUSE's own CONFIDENCE q a FREE PARAMETER the RECORD never PRICED?
lane cloud, 2026-09-18. **ANSWERED: YES — AND IT HAS A PRICE. The record's de facto q = 0.50
("adopt anything that looks better") is the ONLY value in the tested set that ever LOSES money,
and it loses on both large-cap panels. KILL (capital) — no q produces a book that beats the
standing incumbent by a resolvable margin — plus a PUBLISHING clause recommended to the Sunday
review: the floor clause must DECLARE a q, and any q ≥ 0.80 removes the loss.**
Script: `research/backtests/2026-09-18_is-the-FLOOR-CLAUSE-s-own-CONFIDENCE-q-a-FREE-PARAMETER-the-RECORD-never-PRICED_cloud.py`

## What was run (house pattern: a record question run with a CAPITAL ARM)
The floor clause is read as what it operationally is — a bar a candidate must clear before a
chooser may MOVE THE BOOK off its incumbent rung. A chooser sees warm-up..2016 ONLY. For each rung
r it computes the IS Sharpe margin `m(r) = S_IS(r) − S_IS(INC)` and that margin's own sampling SD
from a **PAIRED moving-block bootstrap** (block 21 days, B = 400, shared draws across rungs, fixed
seed). It adopts the highest-IS-Sharpe rung with `m(r) > z_q · SD`, else STAYS. 2017–2026 read ONCE.

* **DIAL 1 — q ∈ {0.50, 0.80, 0.90, 0.95, 0.99}** (0.50 ⇒ z = 0, no bar: the record's habit).
* **DIAL 2 — claim set D ∈ {N, GROSS, HOLD, ALL}**: N ∈ {10,15,20,30,40}, gross ∈
  {0.50,0.60,0.75,0.85,1.00}, H ∈ {21,63,126,252}; ALL = the union.

Incumbent = the record's single confirmed 4b candidate (U56, N=20, H=126, gross 0.60, weekly).
**Gate G2: it reproduces idea 1286's committed 10 bps / t+1 row to 3.6e-07.** G1: fast runner ==
`engine.backtest` to 2.08e-17. G3: a decision at all 360 cells. G4: the bootstrap SD is positive at
198/198 non-incumbent rows. **4/4 gates pass.** 360 chooser cells = 3 panels × 4 claim sets × 5 q ×
costs {10,25,50} bps × fills {t+1,t+2}; 10 bps / t+1 is the only rung any verdict is taken on.
Reference: **SPY** 15.13% / 0.8849 / −33.72%, OOS 15.28% / 0.8747 / −33.72%; **RULES v2 live**
8.62% / 1.2018 / −12.05%, OOS 9.47% / 1.2781 / −12.05%; **incumbent** 12.59% / 1.1517 / −15.51%,
halves 1.2123 / 1.1121, OOS 13.78% / 1.1826 / −15.51%.

## Result 1 — q is NOT inert: it changes what gets adopted at 72 of 72 cells
The adopted rung differs across the five q at **every one of the 72 (panel, claim set, cost, fill)
cells** — there is no cell where the number the record never justified fails to matter. Pre-declared
outcome (C) is refuted.

## Result 2 — on U56, no rung clears even a 0.6-SD bar, so q ≥ 0.80 freezes the book
U56, 10 bps / t+1. Every IS margin is deep inside its own sampling SD:

| rung | IS Sharpe | margin | SD | t | full CAGR / Sharpe / MaxDD | OOS S | 4b |
|---|---|---|---|---|---|---|---|
| **INC (N=20,H=126,G=0.60)** | 1.1155 | — | — | — | 12.59% / 1.1517 / −15.51% | **1.1826** | PASS |
| N=40 | 1.1617 | +0.0462 | 0.0939 | **+0.49** | 10.73% / 1.1345 / −18.28% | 1.1212 | PASS |
| N=15 | 1.1482 | +0.0327 | 0.0649 | +0.50 | 13.66% / 1.1706 / −16.38% | 1.1947 | PASS |
| H=252 | 1.1320 | +0.0165 | 0.0926 | +0.18 | 12.73% / 1.1666 / −17.79% | 1.1962 | PASS |
| G=1.00 | 1.1159 | +0.0004 | 0.0021 | +0.21 | 21.11% / 1.1527 / −24.93% | 1.1840 | FAIL (DD) |
| H=63 | 1.1188 | +0.0033 | 0.0838 | +0.04 | 12.18% / 1.1201 / −20.84% | 1.1302 | FAIL (DD) |

Max |t| over all 12 U56 rungs at this cell is **0.50**; over all costs and fills, 1.43. So at
q = 0.80 the chooser adopts **nothing** on U56 — on all four claim sets. That is the finding: the
record's dial ladders contain no move that is distinguishable from noise on its own capital panel.

## Result 3 — the price of leaving q at 0.50 (the capital arm's number)
Mean Δ(OOS Sharpe), chooser − frozen incumbent, over 72 cells per q:

| q | MOVED | mean Δ(OOS S) vs FROZEN | SE | t | pos/neg | vs q=0.50 |
|---|---|---|---|---|---|---|
| **0.50** | 72/72 | +0.0122 | 0.0116 | +1.05 | 40/32 | — |
| 0.80 | 36/72 | +0.0178 | 0.0109 | +1.64 | 24/12 | +0.0056 |
| 0.90 | 33/72 | +0.0177 | 0.0109 | +1.63 | 21/12 | +0.0055 |
| 0.95 | 8/72 | +0.0070 | 0.0047 | +1.48 | 8/0 | −0.0052 |
| 0.99 | 2/72 | +0.0001 | 0.0000 | +1.42 | 2/0 | −0.0122 |

**None of these is resolvable (t ≤ 1.64), and the positive pooled means are carried entirely by
SMALL663, where the adopted book fails every 4b leg anyway.** By panel:

| panel | q=0.50 | 0.80 | 0.90 | 0.95 | 0.99 |
|---|---|---|---|---|---|
| **U56** (capital panel) | **−0.0156** | +0.0003 | +0.0002 | 0.0000 | 0.0000 |
| **B135** | **−0.0517** | −0.0490 | −0.0492 | +0.0008 | +0.0002 |
| SMALL663 (no 4b leg passes) | +0.1040 | +0.1022 | +0.1021 | +0.0201 | 0.0000 |

On U56 the damage is concentrated exactly where the theory says it should be: with no bar the
chooser adopts **N=40** on the N and ALL ladders (IS margin +0.046, i.e. +0.49 SD) and pays
**−0.0613 OOS Sharpe**; on GROSS it adopts **G=1.00** for +0.0014 OOS Sharpe and a book that then
**fails 4b on the DD leg** (−24.93%); on HOLD it adopts H=252 for +0.0136. One declared q = 0.80
turns the ALL-ladder cell from **−0.0583 into +0.0006**.

## Result 4 — the census arm (crude, lexical, reporting only, moves no gate)
Over 358 committed `.md` files: **1,697 lines quote a confidence level** (0.80/0.90/0.95/0.99);
**213 of them (0.126) also carry any justification token at all**. Concentrated in LEADERBOARD.md
(564 / 92), QUEUE.md (123 / 54), CHANGELOG.md (93 / 29). **NOT CLAIMED:** that the remaining lines
are unjustified — a lexical test cannot read an argument, only show that the number and its reason
are rarely in the same sentence. The capital arm above is what prices q.

## Verdict
**KILL (capital).** No q, on any claim set, produces a book that beats the standing incumbent by a
margin this tape can resolve: the best pooled gain is +0.0178 at t = +1.64, and on the only panel
carrying a 4b-passing book the honest answer at every q ≥ 0.80 is "adopt nothing". 4a: **0 of 360**.
4b: 128 of 360 adopted books pass, and the passing ones are overwhelmingly the incumbent itself.

**RECOMMENDED TO THE SUNDAY REVIEW — PUBLISHING ONLY (changes no book).** The floor clause must
DECLARE its q, and the declared value must be ≥ 0.80. The evidence does not separate 0.80 from
0.99 — on the capital panel nothing clears any of them, so they are the same clause there — but it
does separate all of them from the record's de facto **0.50**, which is the only value that loses
(−0.0156 on U56, −0.0517 on B135) and the only one that would have adopted a 4b-failing book
(G = 1.00, DD −24.93%). The clause's own wording should be: *"A dial move is adopted only if its
in-sample margin exceeds z(q) × the margin's own paired-block-bootstrap SD, with q declared in
advance and q ≥ 0.80; otherwise the incumbent rung stands."* Cost is nil — every run already
produces the return series the bootstrap needs.

**NOT CLAIMED:** that q = 0.95 is better than q = 0.80 (the difference is −0.0052 pooled and 0.0000
on U56); that any committed verdict in the record flips (this run re-adjudicates none of them,
whose return series are not all in the repo); or that the SMALL663 gains mean anything — that panel
fails every 4b leg at every rung and is reported, not banked.

## Survivorship (rule 9)
U56 (55 investables) and B135 are CURRENT-constituent lists; SMALL663 is a current sub-$2B screen
with the house `max_1d_move >= 1.0` filter applied FIRST (52 names dropped, 663 kept). Every
absolute level is an **UPPER bound**. The quoted result is a WITHIN-grid difference — chooser minus
frozen incumbent, and q minus q = 0.50, on the SAME panel, same names, same dates — which is
first-order immune to that bias. The bootstrap SDs are sampling SDs of a margin on THIS tape and do
not price the tape's own selection; only 2020 and 2022 are real stress in it.
