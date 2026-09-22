# Idea 915 — does ANY 4b DD margin survive the 2022 bar?

**Lane cloud, run 4, 2026-09-22.** Script `2026-09-22_4b-dd-margin-vs-the-2022-bar_cloud.py`.
Artifacts: `.grid.csv.gz` (4032 rows), `.cells.csv.gz` (1008), `.bars.csv` (36), `.clause.csv`,
`.walkforward.csv` (9), `.gates.csv`, `.console.txt`.

**ANSWER: it depends entirely on a convention idea 912 never separated — and under the fair
one the answer is "almost all of them". 0 of 18 survive the reading 912 wrote down; 18 of 18
survive the matched reading. The "2020 margin" diagnosis is a WINDOW MISMATCH, not a
fragility. No new KEEP: the one candidate this run produced dies on the record's own newest
clause.**

## The two readings
Excising an episode can be done two ways and they are not the same test:

* **BARONLY** — the BAR moves and the BOOK does not. SPY's MaxDD is read on the excised tape,
  the book's on the full tape. This is 912's reading as written. It compares two tapes.
* **MATCHED** — both legs on the SAME excised tape. *Outside the 2020 episode, is the book
  still within 60% of SPY's drawdown?*

Both are published at every cell. Nothing is tuned between them.

## Gates — 6 of 6 PASS, including a direct reproduction of idea 912
`G7` reproduces 912 exactly: SPY OOS MaxDD **−33.72%** (trough 2020-03-23, 23 days) →
**−24.50%** (trough **2022-10-12, 195 days**) once COVID is excised; the 4b cap moves
**−20.23% → −14.70%**. G2 the EWELIG form ≡ `baseline.rules_v2_weights` (max|d| 0); G1 local
`run()+net()` ≡ `engine.backtest` (0.000e+00); G3 excision is a strict row drop and `NONE` is
the identity; G4 SMALL drops 54 of 719 names with `max_1d_move ≥ 1.0`; G6 realised gross
0.7373 ≤ nominal 0.75.

## The shelf
28 books/panel × 3 panels = **84 priced paths**: `EWELIG` (RULES v2's own band form),
`TOP n` (`baseline.score` composite) and `MOM n` (12-1 momentum) at n ∈ {10,20,40},
gross ∈ {0.75,1.00}, cadence ∈ {W,M}, weekly/monthly t+1, 4 cost rungs, 3 windows,
4 excisions. Exactly two tuned dials as the filed line specifies — **excision window** and
**claim-set width n**; form, gross, cadence, cost, panel, window and convention are reported
at every rung, never selected on.

## (A) THE HEADLINE — 0 of 18 under BARONLY, 18 of 18 under MATCHED

Restricted to FULL and OOS, the only windows that actually contain 2020:

| | cells | COVID | CY2020 | GFC+COVID |
|---|---|---|---|---|
| **full 4b passes** surviving, BARONLY | 18 | **0 (0.000)** | 0 | 0 |
| **full 4b passes** surviving, MATCHED | 18 | **18 (1.000)** | 18 | 18 |
| **DD leg alone**, BARONLY | 78 | 30 (0.385) | 30 | 30 |
| **DD leg alone**, MATCHED | 78 | **72 (0.923)** | 72 | 72 |

Pooled over all windows and cost rungs (158 DD-leg passes): BARONLY **0.696**, MATCHED
**0.962** for COVID/CY2020; **0.468** vs **0.772** for GFC+COVID. Per-rung at 0/10/25/50 bps
the MATCHED DD survival is 0.952 / 0.951 / 0.949 / 1.000 — **the convention, not the cost
rung, is what decides the verdict.**

## (B) THE MECHANISM (B7) — the books' own drawdown IS the same 2020 episode
**80 of 84** books have their binding decline trough in **2020** on FULL, and **80 of 84** on
OOS. SPY's does too (2020-03-23). Excising COVID from SPY alone removes the crash from the
*bar* while leaving it in the *book* — which is why every margin dies under BARONLY. Excise it
from both and the ratio barely moves. The B1 count is therefore not evidence that the record's
DD margins are fragile; it is evidence that **912's excision was applied to one side of a
ratio.**

## (C) The one excision that bites even under MATCHED
`GFC+COVID` is the only rung that moves the MATCHED count (0.923 → 0.923 on FULL/OOS but
**0.772 pooled**, and on U56 IS it takes DD-leg survivors from 9 of 9 to **6 of 9**). The
reason is visible in the bar table: the GFC sits in the **IS** window, where it moves SPY's
MaxDD −22.06% → −18.61% while the books' IS declines trough in 2011 and 2016. A 2020 excision
leaves the IS bar untouched at −22.06% by construction — a control the machinery passes.

## (D) Rule 8 — 2017–2026 read ONCE (9 arms, `.walkforward.csv`)
(excision, n) chosen on the IS window only by IS Sharpe, with the form fixed in advance.
**4a: 0 of 9. 4b under the published bar: 1 of 9.** The one pass:

| panel | form | IS pick | OOS book | OOS RULES v2 | OOS SPY | 4b | 4a |
|---|---|---|---|---|---|---|---|
| U56 | EWELIG g1.00 W | excision GFC+COVID | **12.67% / 1.2760 / −15.91%** | 9.46% / 1.2767 / −12.05% | 15.29% / 0.8751 / −33.72% | PASS (DD +4.32 pp) | FAIL |

Every whole-shelf IS-Sharpe argmax (TOP10/MOM10 monthly at gross 1.00) is a **4b FAIL on DD**
by 11–15 pp, with OOS MaxDD −31% to −35%. The chooser that reaches a 4b pass is the one whose
**form is fixed beforehand** — which the live rules do fix.

A **second** cell, priced but not picked, is stronger on paper: **U56 EWELIG band 0.03 gross
1.00 MONTHLY** passes 4b in **FULL, IS and OOS** at 0/10/25 bps (OOS 12.82% / 1.2252 /
−18.81%, DD margin +1.43 pp), and it is the **IS-Sharpe argmax within the EWELIG form**
(1.1076 of 4 cells) — i.e. legally reachable with only (gross, cadence) free.

## (E) B8 — and BOTH candidates die on the record's own newest clause
Idea 914's clause, hardened by 2115, generalised by 2119, and turned on the live book by idea
**2111 in this same run**: *a margin inside the book's own 5-offset rebalance spread is not a
pass.* Applied at each book's own cadence:

| book | win | 4b at d=0 | offsets passing | DD margin / spread | CAGR margin / spread |
|---|---|---|---|---|---|
| U56 EWELIG g1.00 **M** | FULL | PASS | **2 of 5** | +1.425 / **5.869 → unresolved** | +1.302 / 0.258 res |
| U56 EWELIG g1.00 **M** | OOS | PASS | **2 of 5** | +1.425 / **5.869 → unresolved** | +2.117 / 0.425 res |
| U56 EWELIG g1.00 **W** | FULL | PASS | 5 of 5 | +4.319 / 2.398 res | +0.935 / 0.535 res |
| U56 EWELIG g1.00 **W** | IS | **FAIL** | 0 of 5 | +2.785 / 2.913 unres | **−0.308 / 0.875 unres** |
| U56 EWELIG g1.00 **W** | OOS | PASS | 5 of 5 | +4.319 / 2.398 res | +1.969 / 0.578 res |

* The **monthly** cell's DD margin is **4.1× smaller than its own monthly offset spread**, and
  its 4b verdict holds at only **2 of 5** offsets. **KILLED by the clause.**
* The **weekly** cell clears every leg at 5 of 5 offsets on FULL and OOS but **FAILS 4b in the
  IS window** — on a CAGR margin that is itself unresolved (−0.308 pp against 0.875 pp) — so
  selecting it requires having read 2017–2026. This independently reproduces idea 2119's PARK
  of the same cell from a different grid, and adds that its IS failure is not resolvable.
* Level legs (DD + CAGR) passing at d=0 across these two books: **7 of 11 resolved (0.636)**.

**NO KEEP. RULES.md / PROTOCOL.md / scan.py / bot.py / baseline.py untouched (rule 6).** A
PARK memo is filed (`..._cloud.memo.md`) for the weekly cell with exact RULES wording; it
should NOT be adopted.

## Path 4a (B6)
4a over all 1008 cells: **10 of 252 at 0 bps (0.040) and 1 of 252 (0.004) at 10/25/50 bps.**
The live band book at gross 0.75 is very hard to beat on 4a's drawdown leg.

## What this run cannot do (stated, not repaired)
**SPLICE CAVEAT:** an excised series is a splice no investor experienced — dropping 2020 joins
2020-02-18 to 2020-07-01 as consecutive sessions. Every excised number is a counterfactual
bar, not a tradable result, and no book here is recommended on an excised reading. Three
excision windows, one shelf of 28 forms; the record's *committed* passes are not re-scored
one by one — this run prices its own population instead, so (A) bounds THIS shelf and re-scores
no previously published verdict. The 4b bars are set by a **costless** SPY at every rung (idea
1063's one-sided handicap stands). **SURVIVORSHIP (rule 9):** U56, B136 and SMALL are
current-constituent lists, so every absolute CAGR and drawdown level is optimistic; SMALL is
the sub-$2B screen's survivors since 2010 and is the most optimistic of the three. The
excision contrast is within-tape — same names, same books, only the calendar window moves —
and does not repair the level.

## Residue (not a rules change)
1. **PROTOCOL should name the convention.** Any future episode-excision reading must state
   whether the bar alone or both legs move; the two differ by **0 of 18 vs 18 of 18** on this
   shelf. A BARONLY reading should not be used to retire a pass.
2. **912's finding survives as a fact about SPY, not about the record's books.** SPY's OOS
   worst decline really does move to a 195-day 2022 episode; what does not follow is that the
   record's DD margins were 2020 margins.
3. The one excision worth keeping as a stress is **GFC+COVID**, because it is the only one
   that moves the IS bar and so the only one that bites a book chosen on IS.
