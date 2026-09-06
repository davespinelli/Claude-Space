# idea 223 — the-trade-date-anchor-as-a-published-column (cloud, 2026-09-06)

**VERDICT: the record's "a monthly rebalance is phase-free" premise is KILLED. The trade-date
anchor is a live, unpriced dial worth 5.94pp (broad) to 8.85pp (u56) of full-sample MaxDD on the
IDENTICAL rule, and it flips 4b on 9 of 21 u56 anchors and 20 of 21 broad anchors. The standing
candidate's u56 4b pass is a 12-of-21 statement about which day of the month it trades, not a
property of the book. One by-product survives everything: the anchor-agnostic MEAN-21 book is a
KEEP-candidate (4b) on u56 at 10 AND 25 bps with no anchor chosen at all.**

## What an anchor is

`engine.rebalance_mask(freq="M")` fires on the last trading bar of the month and
`engine.backtest` fills one bar later. An ANCHOR slides that whole schedule — decision bar and
fill bar together — by `phase` bars, leaving the decision-to-fill gap at exactly 1 bar
(PROTOCOL rule 2). Both panels carry 20.88 bars/month, so phases 0..20 enumerate the choice
before the schedule wraps. Nothing about the book changes across the 21 cells.

## Controls (asserted before any new number was read)

* **[A]** `sim(lag=1, phase=0)` == `engine.backtest` to **1.4e-17** on returns and **0.0** on
  turnover, on both panels; the 0-bps-plus-turnover-netting cost shortcut equals a direct 10-bps
  engine run to **1.4e-17**.
* **[B] the decisive control.** The sweep reproduces idea 182B's committed `.phase.csv` on all
  **8** reference phases × **12** columns to **2.2e-16**. This is 182B's instrument, unmodified.

## D1 — the 21-anchor band (identical rule, only the trade date moves)

| panel @ cost | MaxDD range | Sharpe range | CAGR range | OOS Sharpe range | 4b passes | 4a passes | phase 0 (published) |
|---|---|---|---|---|---|---|---|
| u56 @10bps | −14.67% .. −23.52% (**8.85pp**) | 1.0078 .. 1.1628 (0.155) | 1.72pp | 0.242 | **12/21** | 0/21 | 4b PASS |
| u56 @25bps | −14.78% .. −23.68% (**8.89pp**) | 0.9466 .. 1.1018 (0.155) | 1.74pp | 0.240 | **12/21** | 1/21 | 4b PASS |
| broad @10bps | −19.18% .. −25.11% (**5.94pp**) | 0.9405 .. 1.1298 (0.189) | 3.21pp | 0.365 | **1/21** | 2/21 | 4b FAIL (DD) |
| broad @25bps | −19.30% .. −25.37% (**6.07pp**) | 0.8601 .. 1.0517 (0.192) | 3.18pp | 0.369 | **1/21** | 21/21 | 4b FAIL (DD) |

182B measured 8 phases and found a 2.51pp MaxDD band with 7-of-8 passing. Over the full 21 the
band is **3.5x wider** (8.85pp) and the pass rate falls to **12 of 21**. 182B's 8-phase window
was the benign end: phases 11–17 all fail the drawdown cap on u56, and phase 8 — not the
published phase 0 — is the drawdown minimum on both panels (u56 −14.67%, broad −19.18%).

The band is **not** a cost artefact (10 → 25 bps moves it by 0.04pp on u56) and **not** a
turnover artefact (turnover is 4.67–4.90x/yr across all 21 u56 anchors, a 5% spread). It is the
calendar day, and nothing else.

The broad reading is the sharper one: on broad the *published* anchor is the **worst** of the 21
on drawdown at 10 bps and only 1 of 21 anchors passes 4b at all. The parent's "fails the
universe change by 4.3pp" sentence is really "fails it at 20 of 21 possible trade dates".

## D2 — the LEADERBOARD back-fill (the count the idea asks for)

2,732 committed rows carry a parseable MaxDD. The cadence classifier (printed in full in the
console) finds **75 monthly rows**; the WIDE variant adds **0** rows, so the count is not
sensitive to classifier strictness here.

Every row is scored against the same 4b drawdown cap, 0.60 × |SPY MaxDD| = **20.23%**.

| anchor band used | monthly rows within ±band of the cap | of those, PASSING by less than the band |
|---|---|---|
| broad, 5.94pp | **53 / 75 (70.7%)** | 23 |
| u56, 8.85pp | **58 / 75 (77.3%)** | 23 |

**THE ANSWER: 58 of 75 published monthly drawdown claims (77.3%) sit closer to the 4b drawdown
cap than the phase noise of their own schedule; 23 of them PASS the cap by less than that band,
i.e. by an amount a different trade date could erase.** The three narrowest are 182B's own
fill-7 rows at +0.13pp, +0.22pp and +0.25pp of margin — against an 8.85pp band.

*Caveat, not buried:* LEADERBOARD.md does not record each row's evaluation window, so one cap
(this script's own post-warm-up SPY) is applied to every row. Rows evaluated on a different
window carry a cap error that is **not** quantified. The count is an estimate of exposure, not a
re-adjudication of any individual row.

## D3 — PROTOCOL rule 8 walk-forward on the anchor choice (phase chosen on ≤2016-12-31 only)

| panel @ cost | arm | chosen | IS Sharpe | OOS CAGR | OOS Sharpe | OOS MaxDD |
|---|---|---|---|---|---|---|
| u56 @10 | CONST-0 (published) | ph0 | 1.1418 | 14.56% | **1.1695** | −18.81% |
| u56 @10 | IS-PICK | ph0 | 1.1418 | 14.56% | 1.1695 | −18.81% |
| u56 @10 | MEAN-21 | — | 1.0812 | 13.95% | 1.1280 | −19.61% |
| u56 @10 | ORACLE (bound) | ph7 | 1.0760 | 15.63% | 1.2298 | −19.21% |
| u56 @10 | RULES v1 | — | 0.5534 | 7.73% | 0.7471 | −13.83% |
| u56 @10 | SPY | — | 0.8986 | 15.45% | 0.8820 | −33.72% |
| broad @10 | CONST-0 (published) | ph0 | 1.1844 | 16.51% | 1.0976 | −24.51% |
| broad @10 | IS-PICK | ph10 | 1.2377 | 13.66% | **0.9729** | −22.15% |
| broad @10 | MEAN-21 | — | 1.1824 | 13.82% | 0.9830 | −22.51% |
| broad @10 | ORACLE (bound) | ph19 | 1.0978 | 16.48% | 1.1039 | −24.50% |
| broad @10 | RULES v1 | — | 0.7147 | 5.94% | 0.5763 | −21.19% |
| broad @10 | SPY | — | 0.8987 | 15.45% | 0.8820 | −33.72% |

25 bps is the same picture one rung down (u56 IS-PICK = ph0, 13.72%/1.1102/−18.90%; broad
IS-PICK = ph10, **−0.1267** OOS Sharpe vs the published anchor).

**An IS chooser cannot pick the anchor.** On u56 it picks the published phase 0 and adds exactly
**0.0000** OOS Sharpe over doing nothing; on broad it picks phase 10 and *loses* **−0.1247**
(10 bps) / **−0.1267** (25 bps). On both panels IS-PICK's *in-sample* Sharpe is the highest of
the four arms and its OOS Sharpe is below the ORACLE by 0.13–0.26 — the classic in-sample-only
win. The anchor is therefore a dial that must be **removed**, not **chosen**.

## The one thing that survives — MEAN-21

Holding 1/21 of capital on each of the 21 anchor schedules chooses nothing, has no free
parameter, and is what "anchor-agnostic" means operationally:

| panel @ cost | CAGR | Sharpe | MaxDD | H1 / H2 | OOS Sharpe | turnover | 4b | 4a |
|---|---|---|---|---|---|---|---|---|
| u56 @10 | 12.84% | 1.1058 | −19.61% | 1.174 / 1.058 | 1.1280 | 4.85x/yr | **PASS** | FAIL (DD) |
| u56 @25 | 12.03% | 1.0428 | −19.68% | 1.105 / 0.999 | 1.0682 | 4.85x/yr | **PASS** | FAIL (DD) |
| broad @10 | 14.34% | 1.0646 | −22.51% | 1.270 / 0.900 | 0.9830 | 7.25x/yr | FAIL (DD) | FAIL (DD) |
| broad @25 | 13.10% | 0.9837 | −22.63% | 1.184 / 0.822 | 0.9041 | 7.25x/yr | FAIL (H2,DD) | PASS |

vs SPY 15.23% / 0.8890 / −33.72% (H1 0.9566, H2 0.8340; OOS 15.45% / 0.8820) and RULES v1
6.45% / 0.6642 / −13.83% at 10 bps.

MEAN-21 gives up 1.28pp of CAGR and 0.050 of Sharpe against the published anchor on u56 and buys
the removal of a dial whose spread is 8.85pp of drawdown. It clears 4b at **both** cost rungs.
It carries the parent's scope caveat unchanged: **it fails 4b on broad**, so it is a
universe.json-scoped candidate, exactly like its parent. Memo written.

## Caveats

* **SURVIVORSHIP.** universe.json and universe_broad.json are current-constituent lists. No level
  above is an attainable return. The anchor *spread* is a within-panel difference and is far less
  exposed to that bias than the levels are.
* The D2 window caveat above.
* 21 anchors is the phase count on a ~20.88-bar month; months with 19–23 bars make the wrap
  approximate, so phase 20 and phase 0 are not perfectly disjoint schedules.
