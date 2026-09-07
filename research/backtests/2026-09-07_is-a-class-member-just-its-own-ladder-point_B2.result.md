# Idea 135 — is a `4b-defensive` class member just its own book's static-gross ladder point?

**Lane B, 2026-09-07 — INDEPENDENT SECOND RUN.** A cloud lane published its own idea 135 run the
same day (`…_cloud.py`), and a third session claimed the idea concurrently under the `_B` stem;
this run is filed as `_B2` so none of the three overwrites another. **The reconciliation against
the cloud run is exact — see the last section.**

**Lane B, 2026-09-07.** Script `2026-09-07_is-a-class-member-just-its-own-ladder-point_B2.py`,
console `…console.txt`, grid `…grid.csv` (1,632 rows), walk-forward `…walkforward.csv` (72 rows).

## Verdict — **ANSWERED, and it is a KILL of the `4b-defensive` class as it is currently recorded.**
**Mostly YES: a class member IS its own ladder point.** Priced against its OWN book, ungated, held
at a static gross solved to the row's own achieved mean gross — same panel, same cost rung, same
window — only **65 of idea 133's 531 members (12.2%)** beat that point on Sharpe at no worse
drawdown. Mean dSharpe **−0.0440** (median −0.0297): the average member is *worse* than simply
holding less of its own book. And the control is already in the class: the matched ladder point is
itself floor-only for **438 of 531 (82.5%)**, and **passes 4b outright for 80 (15.1%)** — for one
member in seven, holding less of the same book is *capital-worthy* where the instrument is not.

## Reproduction (nothing new was read until these passed)
- idea 133's grid re-run: **1,632 of 1,632 rows matched**, max|diff| **4.44e-16** across CAGR,
  Sharpe, MaxDD, H1, H2, OOS_Sharpe, IS_Sharpe, gross and m; 0 mismatches on `floor_only`,
  `pass4b`, `pass4a`.
- idea 94's published anchor `EWall+vol60-dg u56@10bps`: 11.587% / **1.133** / −16.884% (published
  11.6% / 1.133 / −16.9%).
- **Self-identity gate:** the ungated `control` arm must price at zero against itself — max
  |dSharpe| **1.12e-14**, |dCAGR| 1.24e-13, |dMaxDD| 1.77e-13. Achieved gross-match error over all
  1,632 rows **8.5e-09**.
- Small panel **excluded, as a finding**: idea 133's own grid has **0 floor-only rows of 612**
  there, and idea 136 confirms 0/180. There is no member on that panel to price.

## What the queue got right, and what it got wrong
- **Right (H_ladder):** the class does not survive its own control — 87.8% of it is delisted.
- **WRONG, its stated mechanism:** the queue blamed de-grossing ("forcing 0.53 mean gross moves
  TOP20 from 1 member to 34"). Survival by gross mode is **m53 13.3%, native 11.5%, m75 10.5%** —
  the forced-down mode is the **best**, not the worst, and `spearman(mean gross, dSharpe) = −0.042`
  over members. Membership is manufactured at *every* exposure, not by de-grossing specifically.
  Idea 131's gross axis and this run's per-row axis are close to orthogonal.
- **The bar is convention-dependent, and PROTOCOL must say which one.** At matched mean gross
  (the queue's convention) 12.2% survive; at matched **drawdown** (idea 94's convention, D4)
  **58.9%** do. Same rows, same control family, a 4.8x difference in the answer.
- **A bare `>` is not well posed.** The ungated control IS its own ladder point, and floating point
  lets it beat itself by 2.2e-16: **17 of 206** raw admissions in this run are that artefact. The
  reported D1 carries a 1e-9 tolerance. Materiality: 42/531 (7.9%) survive by >0.01 of Sharpe,
  9/531 (1.7%) by >0.05, **0/531 by >0.10**.

## The two clauses, separately (members, n=531)
| | count | rate |
|---|---|---|
| Sharpe > ladder (D2) | 105 | 19.8% |
| \|MaxDD\| ≤ ladder | 411 | 77.4% |
| both (**D1**, the proposal) | **65** | **12.2%** |
| neither | 76 | 14.3% |
| CAGR > ladder at matched drawdown (D4) | 313 | 58.9% |

Mean dMaxDD **+2.08 pp** (members are shallower) against mean dCAGR **−1.03 pp** — the instruments
do buy drawdown at matched exposure, they just do not buy risk-adjusted return. By arm kind the
survival is `gate` 18.0% (58 of 323), `dd` 7.9%, `bud` 3.5%, **`stop` 0.0% (0 of 59)** and `ctl`
**0.0% by construction** (a ladder point cannot beat itself — this is what the tolerance restores).
By book: TOP40 23.4%, SLV25 17.3%, EWall 11.5%, TOP20 11.4%, SLV50 3.8%, TOP10 0.0% (0 of 11).

## Rule 8 walk-forward (params chosen on 2009–2016, 2017–2026 read once; 12 cells)
| selector | cells with a pick | mean OOS Sharpe | mean OOS CAGR | mean OOS MaxDD | beats SPY | beats RULES v2 |
|---|---|---|---|---|---|---|
| S0 no screen | 12 | 1.109 | 14.4% | −20.8% | 12 | 6 |
| S1 IS-4b-admissible | 11 | 1.069 | 13.0% | −20.9% | 9 | 4 |
| S3 IS floor-only (idea 133) | 12 | **1.233** | 9.1% | −14.3% | 12 | 8 |
| **S5 = S3 + the proposal** | **9** | **1.260** | 8.0% | −12.4% | 9 | 8 |
| S6 ladder screen alone | 12 | 1.115 | 13.4% | −19.5% | 11 | 6 |
| S7 IS-4a vs the live book | 3 | 1.282 | 8.6% | −13.0% | 3 | 3 |

SPY OOS 15.45% / **0.882** / −33.72%; RULES v2 OOS u56 9.53% / **1.285** / −12.05%, broad 7.98% /
1.119 / −12.24%.

**The proposal is inert as a selector.** Paired against S3 on the 9 cells where both pick: **2 of 9
picks move**, mean OOS Sharpe **+0.0009** (1 better, 1 worse, 7 tied), and it **abstains in 3 of 12
cells** where S3 has a pick. The class selector itself is what earns anything (S3 − S0 **+0.1237**,
8/12 wins); the ladder screen alone buys **+0.0065** (3/12). So the bar is worth adopting as a
*reporting* rule, not as a *selector*: it removes 87.8% of the class's rows and changes almost no
decision.

## Both KEEP paths on all 1,632 rows
- **4a vs the LIVE book (RULES v2): 23 of 1,632 (1.4%)** — all on `broad`, all sleeve books, all
  failing 4b on the CAGR floor alone. (Against RULES v1, for continuity with the pre-v2 record:
  784 of 1,632.)
- **4b vs SPY: 144 of 1,632 (8.8%)** — the same rows idea 133 published (u56 75 / broad 26 at
  10 bps, u56 30 / broad 13 at 25 bps); of them only **28 (19.4%) beat their own ladder point**,
  and **0 of the 19 at m53 do**. **0 rows pass both 4a and 4b.**
- **No new KEEP from idea 135's own question.** The standing candidate is untouched.
- **By-product (memo):** the best 4a row is `broad / SLV50 + vol60-dg` — 7.6% / **1.277** / −10.6%,
  halves 1.262 / 1.293, OOS **1.338** — which beats RULES v2 in both halves and on drawdown on
  broad *and* against the live u56 book's published halves (1.226/1.191, −12.05%). Its weakness is
  stated first in the memo: **the same book with no instrument at all (`SLV50/control`) also passes
  4a**, so the content is the sleeve plus de-gross, not the overlay. Blocked on ideas 105/106
  (sleeve RULES wording) and idea 134 (broad admits nothing at 25 bps).

## Proposed PROTOCOL clause
See `…memo.md` §1: adopt the bar **with a stated matching convention and an explicit tolerance**,
as a recording rule for the `4b-defensive` class only. Do not adopt it as a selector.

## Caveats carried
Survivorship (idea 54) inflates the fully invested ladder control most, so the control is if
anything a *hard* test — which runs against this run's own finding, not for it. Idea 128: the IS
window cannot express deep drawdowns, so every IS-window drawdown clause, D1's included, is
measured on a short ruler. MaxDD is one number off one path. Matched-gross rows are not the same
instrument as their m=1 originals and are never quoted as such.


## Reconciliation with the same-day cloud run (`…_cloud.py`) — EXACT, on a disjoint implementation
The cloud lane priced idea 133's **139 native-gross** members with its own harness (a re-run
LADDER convention plus a closed-form SCALAR one). This run's corpus is 3.8x larger (531 members
over three gross modes), but restricted to its `native` subset every published number agrees to
the digit:

| | cloud | this run (native subset) |
|---|---|---|
| members | 139 | 139 |
| beat the ladder point (Sharpe **and** MaxDD) | **16 (11.5%)** | **16 (11.5%)** |
| beat on Sharpe alone | 25 | 25 |
| mean dSharpe / dCAGR / dMaxDD | −0.0531 / −1.28 pp / +2.56 pp | −0.0531 / −1.28 pp / +2.56 pp |
| ladder point itself floor-only | 105 (75.5%) | 105 (75.5%) |
| ladder point clears full 4b | 30 (21.6%) | 30 (21.6%) |
| by kind (bud / gate / dd / stop / ctl) | 0/10, 15/89, 1/23, 0/12, 0 | 0/10, 15/89, 1/23, 0/12, 0/5 |
| by book (SLV25 / EWall / SLV50 / TOP40 / TOP20) | 9/50, 3/26, 2/52, 2/10, 0/1 | 9/50, 3/26, 2/52, 2/10, 0/1 |
| best member `u56/EWall/band3-dg@10` | 1.2056 vs 1.1234, −12.05% vs −16.40%, OOS 1.2851 vs 1.1359 | identical |

Two independent implementations, the same 16 survivors. **What this run adds beyond the cloud
run:** the two matched-gross modes (531 members rather than 139, and with them the finding that
the queue's de-grossing mechanism is *falsified* — m53 survives best, not worst); the
matched-**drawdown** convention (D4: 58.9% vs 12.2%, the 4.8x convention gap); the tolerance
artefact (17 of 206 raw admissions are the control beating itself by 2.2e-16); and the 4a re-score
against the live RULES v2 book. **What the cloud run has and this one does not:** a closed-form
scalar ladder convention with a measured Sharpe-invariance gate, and the sub-$2B panel read.
Both runs reach the same verdict on the selector question — **adopt as a reporting rule, never as
a chooser** (cloud: 0 of 4 picks move; this run: 2 of 9, paired +0.0009).
