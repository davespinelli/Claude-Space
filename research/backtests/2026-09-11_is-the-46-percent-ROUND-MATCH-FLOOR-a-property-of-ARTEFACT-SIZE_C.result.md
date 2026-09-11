# Idea 792 — is the 46% ROUND-MATCH FLOOR a property of ARTEFACT SIZE?  **ANSWERED — YES, and of an undeclared convention. No KEEP claimed (no book).**

**Lane C, 2026-09-11.** Script `2026-09-11_is-the-46-percent-ROUND-MATCH-FLOOR-a-property-of-ARTEFACT-SIZE_C.py`.
Artefacts: `.runs.csv` (713 runs), `.grid.csv` (30 cells), `.walkforward.csv`, `.headline.csv`
(21,294 published tokens), `.console.txt`.

## What was measured
Idea 790's verifier calls a token verified when it is present verbatim OR some committed value
lies within `tol = 0.5*10^-d` of `{q, q/100, q*100}`. For a token drawn uniformly on a run's own
`[p1, p99]` value range that is a covering problem with a **closed form** — the union length of
`v ± tol`, `100v ± 100tol`, `v/100 ± tol/100` clipped to the range, over the range — so the floor
is computed exactly for every run x precision, with idea 790's own verifier run as seeded Monte
Carlo only to calibrate it (G4: max |MC − exact| = **0.0010** over the ladder).

Two tuned parameters, as declared: **precision** `d ∈ {1..6}` and **artefact size**, bucketed into
quintiles of the run's committed DATA value count. All 30 cells reported. 713 of 791 run stems
carry a usable DATA artefact (73 have none, 5 hold < 50 values); 731 MB read; value count runs
50 → 817,333 (median 6,954).

## Gates (pre-registered) — ALL PASS
| gate | reading |
|---|---|
| G1 verifier sound | PLANT-TRUE at 4 dp **1.0000** of 42,780 (bar ≥ 0.95) |
| G2 790 reachable | d=4 floor by size bucket 0.0434 / 0.1288 / 0.3509 / 0.5751 / 0.7837 **brackets 790's 0.4600**; pooled 0.3764 exact, 0.3775 MC |
| G3 monotone in d | pooled 0.8689 → 0.7843 → 0.6405 → 0.3764 → 0.1179 → 0.0216 |
| G4 closed form == MC | 0.0010 / 0.0001 / 0.0008 / 0.0001 / 0.0006 / 0.0001 |
| G5 comparands real | RULES v2 full Sharpe 1.1998, MaxDD −0.1205; SPY OOS Sharpe 0.8721 — reproduce the record exactly |

## The answer
**1. The floor is a size statistic, not a constant.** At the record's own 4 dp it runs **0.0434**
(Q1, median 833 committed values) to **0.7837** (Q5, median 43,805) — an 18x span across one
corpus. Spearman(log10 value density, floor) = **+0.9565** at d=4 (+0.9367 at d=3, +0.9558 at
d=6). 790's pooled 46.0% is one point on that surface: the corpus-wide pooled value is 0.3764 and
790's 60-run calibration slice simply sat where it sat.

**2. Most of the floor is an undeclared convention, not the data.** Splitting the verifier's three
candidates: identity-only pooled floor is **0.0679** at 4 dp against **0.3764** with `q/100` and
`q*100` allowed — **82.0%** of the 4-dp floor (77.6% at 3 dp, 85.9% at 6 dp) is bought by a
leniency no published verification claim states. Under identity-only matching the median run needs
**3 dp** to clear a 5% floor; under 790's convention it needs **5 dp**, and **68 of 713 runs
cannot clear 5% at any precision on the ladder**.

**3. The publishable minimum.** Smallest precision whose own floor clears the bar (exact,
3-scaling): 5% bar → Q1 **4 dp**, Q2 **5**, Q3 **6**, Q4 **6**, Q5 **> 6**; 1% bar → Q1 5, Q2 6,
Q3 6, Q4 > 6, Q5 > 6. Separation (PLANT-TRUE − PLANT-FALSE) at 4 dp falls 0.9538 (Q1) → 0.2185
(Q5): on the largest artefacts a 4-dp match is nearly uninformative.

**4. Rule 8 walk-forward.** d* chosen on vintages ≤ 2026-09-08 (corpus median, 429 runs), later
vintages (284 runs) read once: Q1 d*=5 IS 0.0059 → OOS 0.0033 HOLDS; Q2 d*=5 0.0199 → 0.0106
HOLDS; Q3 d*=6 0.0071 → 0.0053 HOLDS; Q4 d*=6 0.0168 → 0.0138 HOLDS; Q5 no ladder point reaches
the bar in either window (infeasible, not a walk-forward failure). **4/5 buckets hold, the fifth
is unreachable at both ends.** The record's standing 4-dp convention, read once on the OOS half:
floor **0.3444** (IS 0.3976) — a 4-dp re-verification claim succeeds on noise alone about a third
of the time.

**5. What the record actually quotes.** 21,294 published headline tokens (≥ 4 significant digits)
across 629 runs: median precision **4 dp** (48.3% at 4 dp, 29.8% at 2, 19.0% at 3, 2.1% at ≥ 5).
Scored against the floor at each token's own precision and its own run's artefact size:
**59.2%** sit above a 46% floor, **71.0%** above 20%, **86.4%** above 5%; median token floor
**0.6261**. By bucket the median token floor is 0.0723 (Q1), 0.1868, 0.5578, 0.7558, **0.9822**
(Q5).

## Proposed reporting habit (not applied — PROTOCOL/RULES untouched)
A re-verification claim should carry **(n, d, floor)**: the artefact value count it was checked
against, the precision quoted, and the floor from this run's surface — and should drop the
`x100 / ÷100` candidates unless a unit conversion is actually in play, which alone buys 3 dp of
headroom. Nothing was edited: `RULES.md`, `PROTOCOL.md`, `scan.py`, `bot.py`, `baseline.py` are
untouched.

## KEEP paths
**N/A — not claimed either way.** This idea produces no book, no weights function and no return
stream, so PROTOCOL 4a (beat the book in both halves) and 4b (beat SPY in both halves and OOS)
have nothing to score. Comparands computed and reported for the row: RULES v2 full CAGR 8.61%,
Sharpe 1.1998 (H1 1.2349 / H2 1.1718), MaxDD −12.05%; SPY full CAGR 15.11%, Sharpe 0.8835, MaxDD
−33.72%; OOS 2017+ RULES v2 CAGR 9.45% / Sharpe 1.2747 / MaxDD −12.05% against SPY 15.24% /
0.8721 / −33.72%.

**Verdict: ANSWERED / KILL as a capital idea.** The 46% is real but it is not a constant of the
verifier — it is a joint reading of artefact size and an undeclared ×100 leniency, and at the
record's median artefact size the honest 5%-floor precision is 5 dp, not 4.
