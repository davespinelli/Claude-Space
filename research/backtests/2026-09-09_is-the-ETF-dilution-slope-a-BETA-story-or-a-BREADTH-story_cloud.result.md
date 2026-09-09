# Idea 291 — is the ETF dilution slope a BETA story or a BREADTH story? (cloud, 2026-09-09)

**Verdict: ANSWERED — NEITHER, as posed. The slope is a MEAN-RETURN fall that name vol
only partly offsets, plus an almost equally large TIMING channel; the breadth /
diversification leg is ~zero and its sign flips out of sample. No KEEP, no RULES change.**

## The identity

For the un-ranked EWall book, with `h_it` the engine's realised holdings, `g_t = Σ h_it`,
`w_it = h_it/g_t`, `wbar_i` their time mean, and `x_t = Σ w_it r_it`:

```
log Sharpe_book = log(Σ wbar_i mu_i) − log A − 0.5 log(rho + (1−rho)H) + log√252
                  + TIMING + GROSS&COST
                  A = Σ wbar_i sig_i,  H = Σ wbar_i² sig_i² / A²,  rho defined to make it exact
```

`MEAN` and `VOL` are the beta legs; `rho`/`H` are the breadth legs (k is **fixed at 36**
across the whole sweep, so name count cannot move); `TIMING` is the weight-return
covariation the 200d/vol gate produces. Residual across all 27 grid points: **≤ 0.0064**.

## Gates

- (a) Averaging each panel's metrics does **not** reproduce idea 277's published curve
  (max |ΔSharpe| 0.0579, |ΔMaxDD| 0.0339) and the gap vanishes at s=1.000, where the rung
  is a single panel.
- (b) Idea 277 built each rung by **pooling the six seed panels' return series** into one
  portfolio. Reproduced under its own aggregation: **max abs diff 2.2e-16 on Sharpe,
  8.3e-17 on CAGR/MaxDD/OOS, 9/9 rungs.** The published fall is a seed-portfolio fall
  (+0.4458 full, +0.3941 OOS); the per-panel fall this run decomposes is +0.3879 / +0.3496.

## The answer (gmatch, 10 bps; log contributions, s = 0 → 1)

| channel | Δ log | share of the fall | Δ at 0 bps | Δ at 25 bps |
|---|---|---|---|---|
| **MEAN** (Σ wbar·mu) | **−0.5220** | **111%** | 134% | 83% |
| **VOL** (−log A) | **+0.3967** | **−84%** | −102% | −63% |
| DIVERSIFICATION | +0.0177 | −4% | −5% | −3% |
|  — of which CORR | +0.0206 | | | |
|  — of which CONCENTRATION | −0.0026 | | | |
| **TIMING** | **−0.2856** | **61%** | 73% | 45% |
| GROSS & COST | −0.0813 | 17% | 0% | 39% |
| residual | +0.0046 | 1% | | |

The two beta legs **net to −0.1253**, about **27%** of the −0.4698 log fall; TIMING alone is
−0.2856, about **61%**. Levels: mean name return **19.76% → 11.68%** annualised (−41%) while
name vol falls **28.58% → 19.21%** (−33%) — the numerator falls faster than the denominator,
which is the whole beta half of the story.

The breadth half is simply absent: `rho` is **0.342 → 0.327** and is not even monotone (it
dips to 0.294 at s=0.25), `N_eff` is **34.75 → 33.97** on a 36-name panel, and the
concentration leg is worth **−0.0026 in logs, 0.6% of the fall**. Idea 277's halving `disp`
column has no channel into an un-ranked book's Sharpe except through H, and H moves 0.0295
→ 0.0323.

Curve (gmatch, 10 bps, per panel): FULL Sharpe 1.0165 → 0.6287 (7/8 steps down), IS 1.0175
→ 0.5817 (6/8), **OOS 1.0151 → 0.6656 (8/8 monotone)**. Within-share seed sd 0.0882 against
a 0.3878 fall — the slope is **4.4× the seed noise**.

## Rule 8 (channels fitted on 2009–2016 only, 2017–2026 untouched)

- The IS-fitted channel model beats the naive IS-constant on **9/9** grid points and the
  OOS-level flat line on **9/9** (MAE 0.0962 vs 0.1224 vs 0.1467 at 10 bps).
- The channel carrying the largest IS slope is the same one carrying the largest OOS slope
  on **9/9** grid points — it is MEAN in both.
- It **overpredicts**: IS total slope −0.4858 vs OOS actual −0.4036 at 10 bps.
- The DIV leg's slope **flips sign** out of sample (IS +0.0578 → OOS −0.0251), which is what
  a noise channel does.

## KEEP paths

SPY 15.23% / 0.889 / −33.72% (halves 0.957/0.834, OOS 0.882); RULES v2 8.03% / 1.106 /
−12.24% (halves 1.229/0.984, OOS 1.119). Over the 441 rung books:
**4a 0/441, 4b 57/441, both 0/441**; binding 4b bars CAGR 298, H2 249, DD 225, H1 213,
OOS 213. Every 4b pass sits at s ≤ 0.625 and **none at s ≥ 0.750** — the ETF share is an
admissibility dial, not a book. These are diagnostic sub-panels, not a proposed rule.

**SURVIVORSHIP:** every MIX panel is drawn from today's `universe_broad.json` constituents,
so the whole sweep inherits that bias; the slope is a within-sweep contrast, which is why
the bias sits in the level and not in the answer.

Artefacts: `.grid.csv`, `.attribution.csv`, `.curve.csv`, `.pooled.csv`, `.gate.csv`,
`.walkforward.csv`, `.keeppaths.csv`, `.console.txt`. RULES.md, PROTOCOL.md, scan.py, bot.py
and baseline.py untouched.
