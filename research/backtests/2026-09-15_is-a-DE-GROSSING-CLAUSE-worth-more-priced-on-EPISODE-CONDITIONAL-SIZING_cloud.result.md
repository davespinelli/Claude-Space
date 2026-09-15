# Idea 866 (cloud lane, 2026-09-15) — is a DE-GROSSING CLAUSE worth more priced on EPISODE-CONDITIONAL SIZING than on a FULL-SAMPLE book?

**ANSWERED: NO. The ordinary-year cost and the crash payoff move together — no floor on the grid
keeps half the gate's 2020 payoff at ≤25 bps/yr of ordinary-year CAGR, and the walk-forward-chosen
sizing cell is beaten on CAGR *and* Sharpe *and* MaxDD by the very gate it was meant to improve on.
VERDICT: PARK (the pre-registered 4b conjunction fires and is reported verbatim, but the arm is a
worse spelling of idea 864's documented KILL, so no capital claim is made).**
No book promoted. RULES.md, PROTOCOL.md, scan.py, bot.py, baseline.py untouched.

Script `research/backtests/2026-09-15_is-a-DE-GROSSING-CLAUSE-worth-more-priced-on-EPISODE-CONDITIONAL-SIZING_cloud.py`;
console `..._cloud.console.txt`; data `..._cloud.{grid,years,episodes,insample,oos,walkforward,robust,efficiency,dominance,hypotheses}.csv`.

## The two forms (one state, one panel, one book — B136, EWALL g=1.00, weekly, 10 bps, t+1)
- state = 20d average pairwise correlation of the panel, ON above its rolling `w`-day 83rd
  percentile (LEVEL 0.17) — 863/864's state, verbatim.
- **GATE(d)** (the record's): `mult = 1 − d` on every ON day. Memo cell `w=252, d=0.50`.
- **SIZE(f)** (this run's): `mult = 1 − (1−f)·u`, `u = (pctrank − 0.83)/0.17` clipped to [0,1] — full
  gross at the ON boundary, the **floor f** only at the window's correlation extreme, 1.0 when OFF.
- Both decided at t, applied at t+1, switch cost on |Δmult|, both scored against the same
  matched-gross static twin (EWALL held at a constant gross = the arm's realised mean multiplier).
- Tuned: **floor** (7 levels) × **window** (6) = 42 SIZE cells, all published; the 6 GATE cells at
  the memo's inherited depth 0.50 sit beside them as the comparand.

## Gates (printed before any verdict)
| gate | result |
|---|---|
| G1 runner identity (SIZE floor 1.00 == ungated `engine.backtest`) | max\|d\| **0.000e+00** PASS |
| G2 causality (`min_periods=w`; multiplier is exactly `raw.shift(1)`) | no-threshold days 0/0/11/263/515/767 monotone in w; shift exact — PASS |
| G3 H_REPRO: GATE memo cell vs 863/864's committed triple | **14.02% / 1.1538 / −15.11%** exactly — PASS |
| G4 determinism | no RNG in this script; grid recomputed identically across three runs — PASS |
| G5 comparands printed first | SPY **15.16% / 0.8861 / −33.72%**, RULES v2 **7.98% / 1.0993 / −12.24%**, UNGATED EWALL **14.20% / 1.0211 / −23.09%** |
| G6 cost rungs 0/10/25/50 bps × execution lag t+1/t+2 on the chosen cell | reported below |

4b bars off SPY: H1 > 0.9596, H2 > 0.8259, OOS Sharpe > 0.8767, |MaxDD| ≤ 20.23%, CAGR ≥ 10.61%.
4a bars off RULES v2: H1 > 1.2348, H2 > 0.9658, MaxDD ≥ −12.24%.

## The answer — the two legs the queue asked for, at the memo window w=252
| arm | ord-year CAGR (2020+2022 removed) | Δ vs ungated | 2020 | Δ2020 | 2022 | Δ2022 | full CAGR/Sharpe/MaxDD |
|---|---|---|---|---|---|---|---|
| UNGATED g=1.00 | 16.37% | — | 9.51% | — | −11.36% | — | 14.20% / 1.0211 / −23.09% |
| **GATE d=0.50** | 15.32% | **−1.05pp** | 17.40% | **+7.89pp** | −7.27% | **+4.09pp** | **14.02% / 1.1538 / −15.11%** |
| SIZE f=0.10 | 14.51% | −1.85pp | 24.13% | +14.62pp | −9.00% | +2.36pp | 13.56% / 1.1260 / −16.59% |
| SIZE f=0.25 | 14.83% | −1.53pp | 21.74% | +12.22pp | −9.35% | +2.01pp | 13.69% / 1.1207 / −17.03% |
| SIZE f=0.50 | 15.36% | −1.01pp | 17.70% | +8.19pp | −9.97% | +1.39pp | 13.89% / 1.0987 / −18.15% |
| SIZE f=0.75 | 15.87% | −0.50pp | 13.62% | +4.11pp | −10.64% | +0.72pp | 14.06% / 1.0639 / −19.90% |
| SIZE f=0.90 | 16.17% | −0.20pp | 11.16% | +1.65pp | −11.07% | +0.29pp | 14.14% / 1.0389 / −21.66% |

- **H_ORD ∩ H_CRASH is EMPTY.** The only floor within 25 bps/yr of the ungated ordinary-year CAGR
  is f=0.90, and it keeps just **+1.65pp** of the gate's **+7.92pp** 2020 payoff. Every floor that
  keeps half the payoff costs 1.0–1.9pp/yr in ordinary years — i.e. **more** than the gate's 1.05pp.
  The clause's cost and its payoff are the same dial read at two ends.
- **H_YEARS FAILS**: against its own matched-gross twin the best SIZE cell loses in **8 of 18**
  calendar years against the GATE's **7 of 18**, and its losing-year sum is larger at every floor
  below 0.75 (−21.53pp at f=0.10 vs the gate's −13.24pp). Smoothing the gate did not remove the
  ordinary-year drag; it spread it.
- **H_CRASH PASSES in isolation** (f ≤ 0.75 all keep ≥ half the 2020 payoff) and **H_WORKS,
  H_WF, H_4B all PASS** — hence the pre-registered conjunction's KEEP label, reported verbatim.
- **2022 is where sizing breaks.** In a slow bear the state sits just above its threshold, so the
  ramp barely de-grosses: the gate buys +4.09pp, every SIZE floor buys ≤ +2.36pp. The payoff the
  floor preserves is concentrated in the one fast crash (2020), which is exactly the
  single-episode dependence idea 864 killed the clause for.

## Rule 8 walk-forward — dials fitted on 2009–2016 alone, 2017–2026 read once
C1 (argmax IS Sharpe) and C2 (highest floor clearing the IS DD bar; its pool is **0/42**, so it
falls back to C1) both pick **SIZE w=252, f=0.25** (IS Sharpe 1.0686, IS MaxDD −15.07%).

| OOS arm | CAGR | Sharpe | MaxDD | matched-gross twin | WORKS | 4b | 4a |
|---|---|---|---|---|---|---|---|
| **SIZE w=252 f=0.25 (chosen)** | **13.73%** | **1.1701** | **−17.03%** | 1.0097 / −21.40% | YES | **PASS** | FAIL |
| GATE w=252 d=0.50 (comparand) | **14.29%** | **1.2080** | **−15.11%** | 1.0098 / −21.26% | YES | PASS | FAIL |
| SPY | 15.33% | 0.8767 | −33.72% | — | — | — | — |
| RULES v2 (live baseline) | 7.88% | 1.1059 | −12.24% | — | — | — | — |
| UNGATED EWALL | 13.96% | 1.0094 | −23.09% | — | — | — | — |

The chosen sizing cell clears 4b OOS on every leg — **and the gate beats it on all three numbers**.
4a is **0 of 48 cells** on the full sample and 0 of 4 OOS: against RULES v2's −12.24% neither form
ever clears the drawdown leg at gross 1.00, consistent with idea 679's finding that 4a's DD leg is
an exposure test.

## Robustness on the chosen cell (G6)
| arm | 0 bps | 10 bps | 25 bps | 50 bps |
|---|---|---|---|---|
| SIZE (t+1) Sharpe | 1.2290 | 1.1207 | 0.9579 | 0.6863 (WORKS fails) |
| SIZE (t+2) Sharpe | 1.1917 | 1.0849 | 0.9242 | 0.6559 (WORKS fails) |
| GATE (t+1) Sharpe | 1.2582 | 1.1538 | 0.9967 | 0.7342 |
| GATE (t+2) Sharpe | 1.1866 | 1.0829 | 0.9269 | 0.6664 |

A one-day execution delay costs the sizing arm 0.036 Sharpe and the gate 0.071 — the ramp is the
less timing-sensitive of the two, the one place the sizing form is structurally better. Both die
at 50 bps.

## Descriptive addenda (computed after the pre-registered legs; no dial chosen on them)
- **Episode efficiency** (crash payoff bought per pp of ordinary-year CAGR given up): SIZE beats
  the GATE at **5 of 6 windows** — but at **f=0.90 in all five**, a floor that buys +1.65pp of a
  +7.92pp payoff. Efficiency is highest exactly where the clause does least.
- **Dominance**: only **1 of 42** SIZE cells beats its own GATE comparand on CAGR+Sharpe+MaxDD on
  the full sample (w=756, f=0.10) and **2 of 42** OOS (w=504, f=0.10/0.25) — and none at the memo
  window. Whatever survives is a window artefact, not a form advantage.

## What this means for the record
The de-grossing clause is not mispriced by being binary. Priced as a floor it buys crash protection
at the same exchange rate, loses more ordinary years, keeps less of 2022, and is dominated by the
gate at the window the memo actually named. PROTOCOL rule 6 is untouched: no RULES change is
proposed, and the mechanical 4b label is published (not claimed) beside the PARK.

**SURVIVORSHIP (PROTOCOL rule 9):** B136 is `research/universe_broad.json`'s CURRENT constituents,
so every CAGR is optimistic, every MaxDD understated, and the correlation state is optimistic too —
the names that died are the ones that would have correlated hardest in a crash. The GATE-vs-SIZE
*contrast* runs on the identical panel and is far less exposed than any level quoted above.
