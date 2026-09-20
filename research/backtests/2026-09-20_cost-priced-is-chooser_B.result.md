# Idea 1803 (lane B, 2026-09-20) — CAN A COST-PRICED IS-ONLY CHOOSER REACH THE DAILY-REFRESH CELLS IDEA 1793 LEFT UNREACHABLE?

**ANSWERED / KILL OF THE COST-ACCOUNTING EXPLANATION — and the same axis turns out to be
DECISIVE on the OTHER half of the dial, which is the constructive half of this run.**

Script `research/backtests/2026-09-20_cost-priced-is-chooser_B.py`, **gates 13 of 13**, every one
of 120 cells x 4 book-cost rungs (`.grid.csv`), 480 chooser-statistic rows (`.isstats.csv`), 144
legal picks (`.choosers.csv`), 60 decomposition rows (`.decomp.csv`) published.

## What was asked, and the pre-stated rules

Idea 1793 left one named residue: `R = D` clears 4b FULL *and* OOS at 4 of 4 large-panel arms for
every `t >= 0.10`, the OOS oracle takes `t = 0.12, R = D`, and **no legal IS-only chooser ever
picks it**. A daily refresh trades ~2.1-2.5 turns/yr more than a monthly one, i.e. ~21-25 bps/yr
of charged cost at 10 bps, on the order of the IS-Sharpe gaps the chooser reads. So the refusal
might be COST ACCOUNTING rather than information — and a cost artefact is removable.

The test moved ONE thing in 1793's grid and runner: the cost rung the chooser's statistic is
priced at, `c_IS in {0, 10, 25, 50}` bps, crossed with six statistic families. **The book is
always charged the real rung** (0/10/25/50, 10 bps headline), so `c_IS` moves the RANKING only.
Verdict rules V1-V5 were fixed before the run and are reproduced verbatim in the script header.

## (1) V1 — NOT TRIGGERED. **THE REFRESH HALF IS COST-INERT. KILL.**

| `c_IS` | picks with `R in {D,W}` | picks with `R = D` | by R | mean picked `t` |
|---|---|---|---|---|
| 0 bps | **4 of 36** | **0** | D=0, W=4, M=32, Q=0 | 0.1211 |
| 10 bps | **4 of 36** | **0** | D=0, W=4, M=32, Q=0 | 0.1378 |
| 25 bps | **4 of 36** | **0** | D=0, W=4, M=32, Q=0 | 0.1489 |
| 50 bps | 2 of 36 | **0** | D=0, W=2, M=34, Q=0 | 0.1489 |

The R-distribution is **identical** at 0, 10 and 25 bps and `R = D` is picked **0 of 144** times
at every rung, by every one of the six families, on every one of the six arms. Handing the
chooser a statistic that ignores costs entirely does not buy one single daily-refresh pick.

## (2) V3 — NOT TRIGGERED, and this is the mechanism. **ONLY ~19% OF THE STALE PREFERENCE IS COST.**

Of 60 (arm x target x stale-R) comparisons, the stale cell out-Sharpes the daily one **in sample
at 10 bps in 36**. Decomposing each gap into `gap(10) - gap(0)` (the cost part) and `gap(0)`:

* median cost share **0.187**, mean 0.333, IQR 0.120-0.289;
* **2 of 60** gaps flip sign when the statistic is priced at 0 bps — both on SMALL665, none on
  U56 or B136;
* per panel: U56 stale-wins 10/20, median cost share 0.191, **0 flips**, R=D's extra turnover
  **+2.11/yr**; B136 10/20, 0.261, **0 flips**, +2.26/yr; SMALL665 16/20, 0.161, 2 flips, +2.45/yr.

The extra cost of a daily refresh is real and charged — it is simply **not what the chooser is
reading**. Roughly four fifths of the in-sample preference for a stale scalar is GROSS RETURN:
on 2009-2016 the stale, more-exposed book genuinely earns more before costs. This is the priced
version of idea 1789's crash-presence finding (freshness is worth ~0.0003 of Sharpe inside a
crash-free window) and it **KILLS the remaining half of 1789's own sentence** — "the argmax falls
to the stale cell on noise *and saved turnover*". The saved turnover is a fifth of it at most.

## (3) THE CONSTRUCTIVE HALF — the chooser's cost rung is decisive on the **TARGET**, not the refresh

V2 as pre-stated (best single family) did **NOT** trigger: 4 arms at `c_IS = 0` against 4 at
`c_IS = 10` (both `F_GXDD`). Pooled over all 36 (family x arm) cells, however, the axis is far
from inert:

| `c_IS` | legal picks clearing 4b FULL+OOS | picks in the convention-robust band `t in {0.10,0.12}` | mean OOS MaxDD | mean turnover |
|---|---|---|---|---|
| 0 bps | **13 of 36** | **14 of 36** | −25.58% | 2.30 /yr |
| 10 bps | 7 of 36 | 13 of 36 | −27.21% | 2.11 /yr |
| 25 bps | 7 of 36 | 8 of 36 | −28.06% | 2.03 /yr |
| 50 bps | 8 of 36 | 8 of 36 | −28.38% | 1.96 /yr |

`F_CALMAR` goes from **0 of 6 arms at 10/25/50 bps to 4 of 6 at 0 bps**; `F_LEGS` from 1 to 3.
Mechanism, read directly off the grid (U56, T=M, R=M): turnover falls monotonically in the
target — 2.19 / 1.91 / 1.47 / 1.05 / 0.90 /yr at `t` = 0.08 / 0.10 / 0.12 / 0.16 / 0.20 — while
mean gross rises 0.69 -> 0.97 and OOS MaxDD deepens **−16.1% -> −27.5%**. A cost-charged IS
statistic therefore walks the chooser UP the target ladder to the lazy, most-exposed end, which
is the end that blows the 4b drawdown cap out of sample: `F_CALMAR@10` picks `t = 0.20` on all
four large arms (OOS MaxDD −27.5% to −30.0% against the −20.23% cap) and `F_CALMAR@0` picks
`t = 0.08` on all four (OOS −16.1% to −16.5%, 4b PASS).

**Stated against our own reading:** the flip is a knife edge at the headline rung. U56 T=M IS
Calmar reads t=0.08 **1.2313** vs t=0.20 **1.2334** at `c_IS = 10` — a margin of **0.0021** — and
1.2698 vs 1.2413 at `c_IS = 0`. So "charging the chooser costs breaks it" is a statement about a
statistic that is nearly flat across the target ladder, not a large effect, and it is a
POST-HOC family selection (1 of 6) unless a future run pre-registers `F_CALMAR@0`.

## (4) V4 / V5 — CAPITAL: 35 of 144 legal picks clear 4b FULL *and* OOS at 10 bps; 1 is cost-fragile

Reach per arm (of 24 choosers): U56 T=W **10**, U56 T=M **10**, B136 T=M **10**, B136 T=W 5,
**SMALL665 0 of 24 on both arms** (fourth independent confirmation of addendum A2). Of the 35
passing picks only **1** fails 4b at 25 bps (V5), so the cost-fragility counterweight is not what
kills anything here.

The cells reached are `t = 0.08, R = M` (idea 1793's standing candidate, reproduced exactly) and
`t = 0.10, R = W/M`. The one the record does not already carry is **`t = 0.10, R = M`**:

| cell | FULL (10 bps) | halves | OOS (10 bps) | turnover | 4b at 0/10/25/50 bps |
|---|---|---|---|---|---|
| U56 T=M | 13.31% / 1.2437 / −19.39% | 1.323 / 1.170 | **13.81% / 1.2822 / −19.39%** | 1.91 /yr | PASS / PASS / PASS / **PASS** |
| U56 T=W | 13.23% / 1.2292 / −19.62% | 1.318 / 1.147 | 13.67% / 1.2605 / −19.62% | 2.59 /yr | PASS / PASS / PASS / PASS |
| B136 T=M | 13.16% / 1.2014 / −19.87% | 1.352 / 1.058 | 13.05% / 1.2000 / −19.87% | 2.00 /yr | PASS / PASS / PASS / PASS |

against SPY 15.12% / 0.8843 / −33.72% (OOS 15.26% / 0.8737) and live RULES v2 8.62% / 1.2010 /
−12.05% (OOS 9.46% / 1.2766). It **trades the squeeze rather than escaping it** — against idea
1793's `t = 0.08` pick it buys **+1.94 pp of OOS CAGR** and a CAGR-floor margin of **2.73 pp**
(1793: 0.68 pp) at the price of a DD-cap margin of **0.84 pp** (1793: 4.10 pp) — and it is the
only one of the two that survives 50 bps, where `t = 0.08` fails on the CAGR floor.

**Multiplicity, stated plainly:** on U56 this cell is reached by exactly ONE of 24 choosers
(`F_LEGS@0`); on B136 T=M by four (`F_LEGS` at every `c_IS`). `F_LEGS` is also the family idea
1783 killed for degeneracy on the NAME-SET axis. The cell is filed as a KEEP-candidate under
pre-stated rule V4 (`2026-09-20_voltgt-t010-RM_KEEP4b_MEMO.md`) with that thin support written
into the memo; the CHOOSER is not certified by this run.

## (5) PATH 4a — KILL, same restatement artefact the record already named

6 of 120 grid cells clear 4a FULL at 10 bps and 7 of 144 legal picks; **every one is on B136**,
at `t in {0.08, 0.10}` with `R in {D, W}`, and only against the live book **restated on B136**
(Sharpe 1.0972, halves 1.2298/0.9671). Against the real live U56 comparand (1.2010, −12.05%)
**0 of 60 U56 cells** clear 4a. Ideas 1763 and 1793 recorded the same artefact; this is its third
appearance and it is not a passer.

## (6) GATES 13 of 13

G0 18.7y; **G1** two-schedule runner == `engine.backtest` on returns AND turnover **0.000e+00**;
**G2** cost identity == fresh engine runs at 10/25 bps **0.000e+00**; **G3** the standing KEEP-4b
memo's points 2-4 at max |Δ| **4.605e-05**; **G4a** idea 1767's (T=M, R=W) U56 OOS row at
**5.027e-05**; **G4b CROSS-RUN** — all **480** shared cells of idea 1793's committed grid at max
|Δ| **8.882e-16** with **480/480** identical 4b verdicts; **G4c** our `c_IS = 10` statistics ==
1793's `is_Sharpe` / `gx_MaxDD` columns at **2.220e-16 / 9.975e-17**; **G5** a refresh row moves
every held name by ONE common factor (8.882e-16 over 133,070 rows); **G7** 480 book rows + 480
statistic rows, all published; **G8** twin IS-gross match 2.887e-11; **G9** max realised gross
1.0000; **G10** all 144 chooser picks unchanged on panels PHYSICALLY truncated at 2016-12-31 —
rule 8 tested, not asserted.

## (7) Survivorship

U56 / B136 are CURRENT-constituent lists and SMALL665 a CURRENT sub-$2B screen (54 tickers with
`max_1d_move >= 1.0` dropped). Every CAGR and drawdown LEVEL above is optimistic and both 4b bars
are easier here than on a point-in-time panel. The chooser contrast is same-tape / same-names /
same-grid with only the statistic's cost rung moved, so it is first-order immune; the pass COUNTS
are not.

## (8) What this changes in the record

* **KILL** — "the stale-refresh preference is saved turnover": at most a fifth of it is, and the
  refresh pick does not move at all when the chooser is handed a cost-free statistic.
* **CONFIRMS and sharpens** idea 1789: the preference is a gross-return fact of a crash-free IS
  window, not an accounting fact.
* **NEW, and it is the residue worth a pre-registered run:** the same axis that is inert on the
  refresh half is decisive on the TARGET half, in the WRONG direction — charging the chooser the
  costs the book pays walks it toward the lazy, high-exposure rung that fails the 4b drawdown cap.
  Filed as idea 1795's neighbour; this run does NOT promote `F_CALMAR@0`, whose margin at the
  headline rung is 0.0021 of IS Calmar.
* RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are untouched (rule 6).
