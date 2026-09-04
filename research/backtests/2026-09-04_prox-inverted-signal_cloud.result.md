# Idea 80 — is-52w-proximity-a-short-signal — **KILL**

Script: `research/backtests/2026-09-04_prox-inverted-signal_cloud.py` ·
console: `2026-09-04_prox-inverted-signal_cloud.console.txt` ·
36 points reported (2 universes × [live v1 + EWall control + 4 ranking keys × n ∈ {5,10,20,30}]).
Two tuned parameters (ranking key, n), exactly idea 13's grid. Harness reproduces idea 2's
published KEEP row to the decimal (12.7% / 1.093 / −18.3%, halves 1.088/1.103) and idea 13's
live-v1 and EWall rows.

## The question
Idea 13 found the weekly rank IC of `PROX = P_t / max(P_{t−251..t})` **negative** among
eligible names (−0.021 t −2.13 on universe.json, −0.025 t −3.34 on broad). Two readings:
(A) genuine reversal inside the trend gate, so inverting the key should win; (B) a volatility
artefact, since low-vol names sit near their highs mechanically, so "far from the high" is
just "high vol". This run inverts the key (**IPROX** = −PROX), vol-neutralises it
(**IPROXn**: PROX rank residualised on vol20 rank cross-sectionally each day, then inverted),
and runs the rival explanation as its own book (**LOWVOL** = −vol20), against the incumbent
composite (**COMP**).

## Answer: reading (B). The signal is a volatility proxy, and inverting it does not pay.

**The mechanism is measured directly.** Mean cross-sectional Spearman(PROX, vol20) over
eligible names = **−0.487** (u56) and **−0.406** (broad): the gate's high-PROX names *are* the
low-vol names. Weekly Fama-MacBeth slopes on next week's return (percentile ranks, eligible
names only):

| | u56 slope (t) | broad slope (t) |
|---|---|---|
| PROX alone | −0.00298 (**−3.03**) | −0.00282 (**−3.43**) |
| vol20 alone | +0.00498 (+4.63) | +0.00367 (+3.88) |
| **PROX with vol20** | **−0.00065 (−0.65)** | **−0.00161 (−2.26)** |
| **vol20 with PROX** | **+0.00451 (+3.90)** | **+0.00294 (+3.19)** |

On universe.json PROX's t collapses from −3.03 to −0.65 once vol20 is in the regression while
vol20 keeps its own; on broad it drops from −3.43 to −2.26 (slope down 43%). Same picture in
IC space: IPROX IC +0.0208 / +0.0252 → **IPROXn IC +0.0021 (t +0.25) / +0.0134 (t +2.21)**.
Idea 13's negative IC was mostly, and on the primary list entirely, the short-horizon
**high-vol** premium inside the gate wearing a 52-week-high costume.

**Even the vol tilt is not tradeable, and its sign is against the low-vol prior.** LOWVOL —
buying the *least* volatile eligible names — has IC **−0.0426 (t −3.94)** / −0.0329 (t −3.75)
and loses to COMP in **0 of 8** matched-n pairs across both lists (mean −8.4% / −9.9% per year,
t −3.0 to −3.8). So inside this gate high vol wins the next week, which is exactly the exposure
IPROX buys (held-name vol20 0.304 vs COMP 0.296 at n=5) — and it still does not beat COMP.

**As a book, inverting the key fails.** IPROX beats COMP in **3 of 8** matched-n pairs across
both lists, but every difference is either negative and significant (u56: dSharpe −0.075 to
−0.135, paired t −0.53 to −2.46, mean −1.69%/yr) or statistically nothing (broad: dSharpe
−0.012 to +0.024, **paired t −0.09 to +0.13**, mean −0.04%/yr). The three "wins" are coin flips
on one list, not a signal. Stripping the vol content makes it strictly worse: **IPROX beats
IPROXn in 8 of 8** (t +1.84 to +3.11, +0.69% to +9.87%/yr) and IPROXn beats COMP in **0 of 8**.
Against the no-ranking control, IPROX adds nothing COMP does not (dSharpe vs EWall −0.223 to
−0.046 at every n on both lists) and IPROXn is negative at 7 of 8 points.

**Cross-universe 4b: 0 of 18 points pass on both lists.** IPROX-n20 and IPROX-n30 do pass 4b on
broad alone (13.4% / 0.98 / −19.7% and 12.1% / 0.97 / −19.8%, where COMP-n20 fails H2) — the
run's only interesting number for the idea — but both fail on universe.json's CAGR floor
(10.6% and 9.5% vs the 10.68% bar), and their paired t vs COMP on broad is +0.13. That is a
one-list, one-parameter pass with no separation from the control, i.e. the pattern the
protocol's cross-universe bar exists to reject.

**Rule 8 rejects it.** Parameters chosen on 2009–2016 only, 2017–2026 read once. On
universe.json S1 and S2 both select **LOWVOL-n20** (IS Sharpe 1.005, the highest of the 16) →
OOS 6.2% / 0.853 / −12.8%, fails the OOS bars; on broad both select **LOWVOL-n30** → OOS 5.4% /
0.692 / −15.0%, fails. Audited within each n, the in-sample rule picks **COMP at 6 of the 8
(universe, n) cells** and never picks IPROX or IPROXn anywhere. Spearman(IS, OOS Sharpe) over the
16 CAND points = +0.621 (u56) and +0.185 (broad).

**Cost makes it worse, which idea 11 (run today) prices exactly.** Inverting the key roughly
doubles to triples turnover — IPROX 20.0–37.6×/yr and IPROXn 21.6–44.0×/yr vs COMP's 9.6–21.3×
— because a level statistic bounded near 1.0 reshuffles on tiny moves (idea 13's finding,
reproduced: flips/ticker/yr 9.3 for IPROX-n20 vs 4.4 for COMP-n20). At idea 11's measured
−0.08 to −0.10 Sharpe per 10 bps for a 10×/yr book, IPROX's extra 10–20×/yr of turnover is
another 0.08–0.20 of Sharpe the reported numbers already charge at 10 bps and would charge
again at any realistic higher cost.

## Transferable finding
Any cross-sectional key measured *inside* an eligibility gate must be regressed against vol20
before its IC is believed. The gate itself is a vol filter (`vol20 < 0.60`) applied to a
trend-selected set, so a level statistic bounded by a running maximum inherits a −0.4 to −0.5
rank correlation with vol by construction. Idea 13's negative IC was real and reproducible and
still carried no independent information.

## Caveats
Survivorship: current constituents of both lists, one-directional, and it points against the
KILL being an artefact of the panel — IPROX deliberately buys the names furthest below their own
highs, exactly the cohort where delisted names would have lived, so its numbers here are biased
*upward* and it still loses.

**Verdict: KILL.** 0 of 18 points pass 4b on both lists; the inverted key beats the incumbent in
0 of 4 matched-n pairs on universe.json and is indistinguishable from it on broad; the IC it
inherits is a volatility proxy that vanishes (t −0.65) once vol20 is controlled; rule 8 never
selects it. No new book proposed, no RULES change.
