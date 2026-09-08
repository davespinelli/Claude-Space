# Idea 414 — price the BOTH-PATHS row on the cost rung it dies on (lane C, 2026-09-08)

**Row:** idea 142's only two both-paths rows — book `S3-50` (0.50 x composite TOP20 + 0.50 x
TLT/GLD/UUP momentum-vote x risk-parity sleeve, gross 0.75), arm `band3-rw`, weekly, t+1, panels
u56 and broad. Construction imported from ideas 133/94/129; idea 142's committed row reproduces
to max|diff| **2.8e-17** at both 10 and 25 bps, turnover **8.17x / 10.86x** (queue: 8.2x/10.9x).
Cost enters the return series affinely (`r(c) = r(0) - turnover*c/1e4`, asserted EXACT, 0.0e+00
over 7 rungs), so every fine-grid point is exact rather than interpolated.

**ANSWER — the binary hides a knife edge on one panel and 6.7 bps of slack on the other.**

| panel | c*(4b) | c*(4a, matched) | candidate dies at | binding bar | slack over 10 bps |
|---|---|---|---|---|---|
| u56 | 16.70 | 17.01 | **16.70 bps** | 4b CAGR floor | +6.70 bps |
| broad | 16.95 | **10.24** | **10.24 bps** | **4a H2 Sharpe** | **+0.24 bps** |

Named grid (window=full), all reported: u56 passes both paths at 10/12/15 and fails from 18 on
(CAGR floor); broad passes both paths at **10 only** — at 12 bps it still passes 4b but has
already lost 4a, and from 18 bps it loses 4b too. Per-bar c* for all six bars x three windows x
both 4a comparand conventions is in `.crossings.csv`.

Three things the Sunday review could not see in idea 142's binary:

1. **The two panels die on different bars.** u56 dies on 4b's CAGR floor (margin +0.61 pp at 10
   bps, the number the queue quotes); broad dies on **4a's H2 Sharpe leg**, whose margin at 10
   bps is **+0.0017 of Sharpe**. Broad's both-paths status is not a 10-vs-25 fact — it is a
   0.24-bps fact, inside any plausible execution error.
2. **4a's drawdown bar is not what gives way** (P3 held). Its margin is +0.0042 at 10 bps and
   c* is 41.4 bps on broad and past 60 on u56: a proportional cost drag barely moves a drawdown
   ratio. 4a dies on its Sharpe legs.
3. **The comparand convention (idea 398's open defect) is worth <2 bps here**: pricing RULES v2
   at the arm's own rung vs a fixed 10 bps moves c*(4a) from 17.01 to 15.26 (u56) and 10.24 to
   10.17 (broad). It cannot rescue or condemn the row.

**Rule 8 (walk-forward run on the rung, since the book has no fitted parameter): c* itself does
not walk forward.** IS (2009-2016) alone vs the OOS window read once, 4b path:
u56 **12.48 -> 20.54** (IS *understates* slack by 8.1 bps), broad **25.11 -> 10.04** (IS
*overstates* it by 15.1 bps) — mis-stated by 8-15 bps in **opposite directions** on the two
panels. OOS-window 4b at the record's rung: u56 CAGR 11.73% / Sharpe 1.2886 / MaxDD -11.63%
(SPY 15.45% / 0.8820 / -33.72%; live RULES v2 1.2851; RULES v1 0.7471) passing to 20 bps; broad
10.82% / 1.0473 / -11.82% passing at 10 bps with a CAGR-floor margin of **+0.0000** and failing
from 12 bps.

**VERDICT: ANSWERED — c* published; the candidate is DOWNGRADED to PARK.** It is not a
both-paths book at any rung the record could defend on broad, and on u56 its 6.7 bps of slack
is an in-sample number the OOS window revises by +8 bps and the IS window by -8. Costs: at 10
bps the arm already pays 82 (u56) / 109 (broad) bps/yr of drag, and each extra 10 bps of rung
costs it 0.82 / 1.09 pp of CAGR — a book whose verdict is decided in the second decimal of the
spread assumption. **Survivorship (idea 54) makes every CAGR here optimistic, so every
CAGR-driven c* above is an UPPER bound on the real slack.**

Artefacts: `.grid.csv` (42 rows: 2 panels x 7 rungs x 3 windows), `.crossings.csv` (66 rows:
6 bars x 3 windows x 2 panels x conventions), `.walkforward.csv`, `.headline.csv`,
`.console.txt`. Predictions P1-P4 all HELD (stated before any number was read).
