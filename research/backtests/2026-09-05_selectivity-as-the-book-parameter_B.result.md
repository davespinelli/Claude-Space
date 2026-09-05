# Idea 160 — selectivity-as-the-book-parameter (lane B, 2026-09-05)

**Verdict: KILL of the proposal.** Fixing the SHARE q of the eligible set instead of the
name count n is a real, correctly-implemented instrument that does exactly what it claims
mechanically and buys **nothing**: at matched mean book size it is worse on Sharpe in
23 of 32 primary comparisons, deeper in drawdown in 24 of 32, more expensive by 1.9 turns
per year, and it is the **worst of five rule-8 selectors, below a random pick**. RULES
keeps its fixed n. No rule change, no promotion.

Script `2026-09-05_selectivity-as-the-book-parameter_B.py`; console
`.console.txt`; grids `.grid.csv`, `.paired.csv`, `.walkforward.csv`; memo `.memo.md`.

---

## Design

Both arms share the composite key (no `/sqrt(vol20)`, per ideas 1/2/80/81), the
200d / `vol20 < 0.60` gate, 75% gross, weekly rebalance, t+1 execution, and the
**full-gross-rebuild (rw)** convention. The *only* difference is how the weekly count is set:

| arm | count rule |
|---|---|
| **FIXQ** | `n_t = max(1, round(q · E_t))` — the top q share of that week's eligible set |
| **FIXN** | `n_t = n`, with `n = round(q · mean E_t)` taken over the **IS window 2009–2016 only** |

so the two arms hold the same number of names *on average* and differ only in whether that
number tracks `E_t`. The rw convention is pre-registered, not chosen: `gross/n` (idea 81's
"dg") silently de-grosses whenever `E_t < n`, which would confound count-tracking with
exposure-tracking. Realised mean gross is 0.7488–0.7500 on every one of the 96 books.

**Exactly two tuned parameters** (PROTOCOL rule 4): q ∈ {0.10, 0.20, 0.30, 0.40, 0.53,
0.65, 0.80, 1.00} (0.53 carried in from idea 153, not fitted; 1.00 is the EWall control)
× the count rule ∈ {FIXQ, FIXN} = **16 grid points per cell, every one printed**.
Panels and cost rungs are the queue's own pre-registered axes: u56 × broad × {10, 25} bps
= 4 primary cells; the 484-name sub-$2B panel is run identically and reported **separately
as secondary** (ideas 39/49/136: the gate is inverted there). **96 backtests in total.**

## Pre-checks, run before any new number was read

**[d] Trading-day index (idea 38): CLEAN.** All three panels max 253 rows/yr 2015–24.

**[a] Harness reproduces the published incumbent exactly.**

| row | result | published |
|---|---|---|
| U56/CAND20 **dg** @10bps | **12.65974% / 1.09214 / −18.30835%**, halves 1.08828 / 1.10155 | idea 2 KEEP 12.7% / 1.093 / −18.3%, 1.088/1.103 — matches the CHANGELOG's re-derivable value to all printed digits |
| U56/RULES v1 @10bps | 6.45305% / 0.66418 / −13.82780%, halves 0.64091 / 0.68779 | live book 6.5% / 0.666 / −13.8% |
| U56/CAND20 **rw** (this run's convention) | 12.78846% / 1.06354 / −18.30835%, halves 1.06817 / 1.06639 | — |

The dg→rw switch costs the incumbent book 0.029 of Sharpe on u56 and is applied to **both**
arms, so it cannot favour either.

**[b] Premise 1 — PARTLY NOT REPRODUCED, and the correction matters.** The queue states
"B136: n_elig 3 to 127, so q swings 16x week to week". The eligible-count range is right
(3 → 127, a 42× range), but a *top-20 book's* q is capped at 1.0, so its realised
selectivity swings **6.35×**, not 16×:

| panel | weeks | E min / mean / max | q(n=20) min / mean / max | swing |
|---|---|---|---|---|
| u56 | 921 | 3 / 37.5 / 55 | 0.364 / 0.569 / 1.000 | 2.75× |
| broad (B136) | 921 | 3 / 91.4 / 127 | 0.157 / 0.258 / 1.000 | **6.35×** |
| small (secondary) | 817 | 1 / 148.3 / 289 | 0.069 / 0.169 / 1.000 | 14.45× |

A ~16× q swing exists on the **small** panel, not on B136. The premise survives in kind
(q does float a lot) but its headline number belongs to a different panel.

**[c] Premise 2 — FAILS, and it predicts the answer.** Idea 78's Spearman(q, spread) = −0.975
is a **cross-cell** statistic measured across matched-q designs. The time-series version —
the one a share-tracking rule would have to exploit — is absent:

> **Spearman(realised weekly q, weekly gross cost-free top-20 selection spread) = −0.069 (u56, 919 weeks) and −0.013 (broad, 920 weeks).**

By q-quintile the annualised gross spread is non-monotone on both panels (u56:
+4.3%, +6.8%, +5.7%, +1.5%, −0.7% at q̄ = 0.42→0.93, t = 1.41/2.24/2.36/0.69/−0.77; broad:
−1.8%, +9.8%, +4.6%, +3.7%, +4.7%). There is a weak decline at the very top on u56 and
nothing at all on broad. **Idea 78's mechanism does not exist week-to-week inside a panel**,
so there was never anything for FIXQ to harvest — and this was known before any book was run.

## Q1 — the answer: FIXQ − FIXN at matched mean book size

32 primary comparisons (2 panels × 2 costs × 8 q), paired on daily returns:

| statistic | mean | FIXQ wins |
|---|---|---|
| ΔSharpe | **−0.0257** (median −0.0138) | **9 / 32** |
| ΔCAGR | −0.048 pp | 11 / 32 |
| ΔMaxDD (positive = FIXQ shallower) | **−4.40 pp** | 8 / 32 |
| ΔOOS Sharpe | **−0.0394** | 9 / 32 |
| Δturnover | **+1.86 ×/yr** (FIXQ more expensive) | — |
| paired daily t | mean **−0.315**; \|t\| ≥ 2 in **2 / 32**, both **negative** | — |

The effect is a small, consistently negative nothing: not one of the 32 cells shows FIXQ
significantly ahead, two show it significantly behind, and it pays 1.9 extra turns a year
for the privilege. On the secondary small panel it is worse still (mean ΔSharpe −0.055,
FIXQ wins 2/16, ΔCAGR −0.89 pp).

**The one thing FIXQ does buy is a slow-bear tilt, and it pays for it in the fast crash.**
2022: mean **+2.35 pp**, FIXQ better in **26 / 32**. 2020: mean **−3.69 pp**, FIXQ better in
**5 / 32**. This is idea 46's adaptive-count finding recovered on a different instrument, and
with the sign of its cost now visible: holding a *share* means holding more names into a
grinding decline (good) and cutting the book hard into a V-shaped crash (bad). The two
roughly cancel; on drawdown FIXQ is worse, because 2020 is where the drawdown is.

## Q2 — mechanism: the instrument works, it just does not pay

Realised selectivity sd across weeks, per arm (10 bps; identical at 25 bps by construction):

| panel | FIXQ sd(q) | FIXN sd(q) | ratio |
|---|---|---|---|
| u56 | 0.0068 – 0.0169 | 0.1015 – 0.2005 | ~12× |
| broad | 0.0032 – 0.0094 | 0.0916 – 0.1890 | ~22× |
| small | 0.0099 – 0.0441 | 0.1030 – 0.2026 | ~7× |

FIXQ stabilises selectivity by **one to two orders of magnitude** and moves full-sample
Sharpe by −0.026 on average. This is a null with a working instrument behind it, not a null
from a broken one.

## Q3 — both KEEP paths, all 96 books

| path | passes | FIXQ | FIXN |
|---|---|---|---|
| **4a** (beat the live rules) | 22 / 96 | 7 | 15 |
| **4b** (capital-worthy, full sample) | **15 / 96** | **5** | **10** |
| 4b on the OOS window alone | 23 / 96 | 7 | 16 |

(counts by arm are over the 64 primary large-cap books; every 4b pass is at **10 bps** and
**large-cap** — 0 of 32 small-panel books passes anything, a sixth independent reproduction
of idea 136.) First-failing-bar census on 4b: DD 62, H2 59, H1 58, OOS 52, CAGR 52.

**One FIXQ book passes 4b outright and is recorded rather than promoted:**
`u56 @10bps, FIXQ q = 0.53` — **13.17% / 1.0572 / −19.36%**, halves **0.9822 / 1.1270**,
**OOS 15.54% / 1.1813 / −19.36%**, turnover 13.0×/yr. Its OOS Sharpe is the **highest of all
96 books**. It is nevertheless not proposed, for four reasons stated together: its matched
control `FIXN n = 19` also passes 4b (1.0390, OOS 1.1072) so the *instrument* is not what
earns the pass; the same book fails 4b on **broad** (DD) and at **25 bps** (H1, DD), so it
clears neither idea 82's proposed 25 bps cross-universe bar nor a second panel; its H1
margin over SPY is **0.025**; and it is one cell of 32 in a family whose mean is negative.
See `.memo.md`.

## Q4 — rule 8 walk-forward (IS 2009–2016 chosen, OOS 2017–2026 read once)

Mean OOS over the **4 primary cells** (SPY OOS Sharpe **0.882**; RULES v1 0.662):

| selector | OOS CAGR | OOS Sharpe | OOS MaxDD | vs S0 |
|---|---|---|---|---|
| **S0 do-nothing (published n = 20)** | 12.36% | **0.9356** | −19.2% | — |
| S1 IS-Sharpe over all 16 arms | 15.02% | 0.8000 | −27.0% | −0.136 |
| **S2 IS-Sharpe over FIXQ only** | 13.02% | **0.7019** | **−32.9%** | **−0.234** |
| S3 IS-Sharpe over FIXN only | 14.20% | 0.9322 | −21.7% | −0.003 |
| S4 **random** arm | 12.67% | **0.9580** | −23.1% | **+0.022** |

Over all 6 cells: S0 0.7540, S1 0.6855, **S2 0.5567**, S3 0.7736, S4 0.7444.

**S2 — this idea's own selector — is last of five on both readings and loses to a random
pick by 0.256 of OOS Sharpe on the primary cells, at 13.7 pp more drawdown.** The IS window
sends every informed selector to the most concentrated arm it can find (q = 0.10 in 5 of
6 S1 picks and 6 of 6 S2 picks) and that concentration does not survive; S3 escapes on broad
only because the FIXN family's IS argmax happens to sit at q = 1.00. The do-nothing control
beats SPY and beats three of the four selectors — the project's standing result (ideas 132,
141, 149, 151) reproduced on a seventh bar.

## Q5 — the real dial is the LEVEL of q, not whether it is pinned

Sharpe is near-monotone **increasing** in q on both large-cap panels and both arms:

| cell | FIXQ argmax q (Sharpe) | FIXN argmax q (Sharpe) | Spearman(q, Sharpe) FIXQ / FIXN |
|---|---|---|---|
| u56 @10 | 0.53 (1.0572) | 0.80 (1.0644) | +0.571 / +0.905 |
| u56 @25 | 1.00 (0.9240) | 0.80 (0.9353) | +0.833 / +0.905 |
| broad @10 | 1.00 (1.0253) | 1.00 (1.0243) | +0.857 / +0.976 |
| broad @25 | 1.00 (0.9060) | 1.00 (0.9060) | +0.857 / +0.976 |

The Sharpe **range across q** is 0.117–0.230 per cell; the FIXQ-vs-FIXN gap is 0.026. **The
level of selectivity is 5–9× more consequential than whether it is held fixed**, and the
level that wins is q → 1, i.e. hold everything eligible. That is a fourth independent
derivation of "the ranking subtracts value" (ideas 72, 82, 141) arriving from the selectivity
axis, and it is the transferable part of this run. On the secondary small panel the ordering
inverts (FIXN argmax q = 0.10 at both costs, Spearman −0.524 / −0.143), which is ideas
39/49's universe clause again.

## Caveats carried

Survivorship on all three current-constituent panels (idea 54) — and it runs **against** the
arm this run rejects, since FIXQ holds *more* names in bad weeks, exactly the cohort delisted
names would occupy, so a delisting-aware panel would make FIXQ look worse, not better.
Idea 128's shallow IS drawdown window biases every rule-8 selector identically. Idea 126:
t+1 execution only, no spread or impact model. No IWM in the cache, so the small panel is
judged against SPY (stated, not adjusted). The 4 primary walk-forward cells are few; the
6-cell reading is reported beside them and agrees. `q = 0.53` is imported from idea 153 and
is therefore not free, but it is also not independent of that run's own fitting.
