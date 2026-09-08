# Idea 243 — locate the n ceiling above 60 (cloud, 2026-09-08)

**Verdict: ANSWERED, and the queue's own framing is corrected. The ceiling is MECHANICAL —
it is the day the ranked book runs out of eligible names — and an interior optimum does exist
in 15 of 15 (panel, rung) cells but is worth <= 0.011 Sharpe on the large-cap panels, loses to
the UN-RANKED EW_ALL book in 14 of 15, and does not survive rule 8. No KEEP, no RULES change.**

Script: `research/backtests/2026-09-08_locate-the-n-ceiling-above-60_cloud.py`
(5 panels x 15 arms x 3 cost rungs = 225 arm-rows; ONE tuned dial, n, at 13 levels, all
reported. Artefacts `.ladder.csv`, `.walkforward.csv`, `.keep.csv`, `.console.txt`.)

## 0. The premise is false as written: the NORM ladder does not converge to EWall
Under NORM, `RANKED(n)` with `n >= n_elig(t)` **is** the equal-weight book over the ELIGIBLE
set. Gate G3 asserts the identity at **max |dw| 0.000e+00** on 4 panels. EWall also holds the
gated-out names, so it is a different book and the ladder can never reach it: overlap with
EW_ALL SATURATES at 0.657 (B136), 0.658 (BSTK100), 0.653 (U56), 0.391 (SMALL439), while
overlap with EW_ELIG goes to 0.944-0.947. **What the width dial converges to is the 200d-gated
equal-weight book, not EWall** — so any "the ranked book just becomes EWall at large n" reading
in the record is measuring the GATE, not the ranking (the same conclusion lane C reached from
the excess side on 2026-09-08).

## 1. The ceiling, located (this is idea 243's deliverable)
The ladder becomes numerically IDENTICAL to EW_ELIG — every column, every day — at

| panel | eligible names/day (mean, p95, max) | ladder is EW_ELIG from |
|---|---|---|
| U56 | 37.4 / 52 / 55 | **n = 60** |
| BSTK100 | 67.1 / 91 / 96 | **n = 120** (0.0002 Sharpe from it already at n=90) |
| B136 | 91.4 / 121 / 128 | **n = 150** |
| SMALL439 | 140.2 / 233 / 279 | **n = 240+** (still 0.939 overlap at 240) |

So the "unbounded width curve" idea 240 reported is a panel-breadth fact with a hard stop, and
"3 of 7 panels went straight to the new top (n=60)" reads, on U56, as *the chooser picked the
gated equal-weight book* — at n=60 there is nothing else to pick.

## 2. Does an interior OOS optimum exist? Yes — and it is worth almost nothing
Argmax over the 13-point ladder is INTERIOR (neither n=5 nor n=240) in **15 of 15 (panel, rung)
cells full-sample and 15 of 15 OOS**. Full-sample argmax: B136 **n=120**, BSTK100 **n=75**,
U56 **n=20** (n=50 at 25 bps), SMALL439 **n=10**. OOS argmax: B136 **75**, BSTK100 **75**
(60 at 25 bps), U56 **30**, SMALL439 **10**.

But the oracle best beats EW_ELIG — the ladder's own limit, chosen with the answer in hand — by
only **+0.0009 (B136)** and **+0.0105 (BSTK100)** of Sharpe at 10 bps; the visible margins are
on SMALL439 (+0.147) and U56 (+0.014). And against the un-ranked **EW_ALL** control the same
oracle wins **1 of 15** full-sample and **5 of 15** OOS: at 10 bps EW_ALL is 1.1220 (B136),
1.1853 (BSTK100), 1.1240 (U56), 0.6781 (SMALL439) against the best ranked point's 1.0262 /
1.0322 / 1.0635 / 0.4816. **The interior optimum is an optimum only inside the gated family.**

## 3. Rule 8 — the interior optimum does not survive being chosen ex ante
n chosen on <= 2016 by IS Sharpe, 2017-2026 read once, 15 cells:
IS pick == OOS oracle in **0 of 15**; mean OOS Sharpe regret vs the oracle **+0.1486**. The
IS-chosen n beats EW_ELIG OOS in 9 of 15, **EW_ALL in 1 of 15**, RULES v2 (live) in 2 of 15,
SPY in 6 of 15. The IS chooser lands at n=10 on both large-cap panels at 0 and 10 bps —
the narrowest interior arm — and delivers OOS 0.7806 (B136) / 0.7452 (BSTK100) against EW_ALL's
1.1022 / 1.1487. The one place ranking survives ex ante is U56 (n=20, OOS 1.1307 vs EW_ALL
1.1357, RULES v2 1.2851).

## 4. KEEP paths
**4a 0 of 225. 4b 38 of 225**, every one on B136 (22) or U56 (16), none on BSTK100 or SMALL439,
none at 25 bps. Two of the B136 passers ARE EW_ELIG itself and the rest are n >= 40, i.e. arms
that have largely converged to it — the passes belong to the 200d gate's equal-weight book, not
to the ranking. **No new KEEP.**

## 5. By-product: a joined BENCHMARK inside the small-panel book (cross-lane note)
`baseline.load_universe(small=True)` joins SPY as a benchmark, never a constituent, but lane C's
committed ladder ranks and holds every column, SPY included. Re-run with SPY excluded from the
investable set and everything else identical: max |d Sharpe| **0.0093** and max |d OOS Sharpe|
**0.0134**, both at n=20 (a single benchmark holding is worth 1/n of a narrow book); EW_ALL moves
0.0006. **Lane C's conclusions are unaffected** — recorded so the convention is explicit next time.

## Gates
G1 `simulate(EW_ALL)` vs `engine.backtest` on B136: max |dret| **4.2e-17**.
G2 RE-EXECUTION of lane C's committed NORM grid, 72 shared (panel, n, rung) cells: max |dSharpe|
**2.2e-16**. This is a determinism / data-stability check, **NOT independent corroboration** —
lane C's module is imported and its `simulate` / `ranked_weights` / `ew_weights` are used verbatim.
G3 identity `NORM(n -> inf) == EW_ELIG`: max |dw| **0.000e+00** on 4 panels.

SURVIVORSHIP: B136 and BSTK100 are current constituents of `research/universe_broad.json`;
SMALL439 is the sub-$2B screen's survivors since 2010 with the 44 tickers whose
`data/small_meta.csv` `max_1d_move >= 1.0` dropped (PROTOCOL 9). Levels are upward-biased and not
achievable; every reading here is a within-panel contrast between books on the same days.
