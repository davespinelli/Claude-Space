# Idea 359 (lane C, 2026-09-07) — retire-the-linear-blend-normalisation-record-wide

**Script:** `2026-09-07_retire-the-linear-blend-normalisation-record-wide_C.py`
**Artefacts:** `.console.txt`, `.grid.csv` (1,260 rows), `.statistics.csv` (756 interior),
`.pathology.csv`, `.disagreement.csv`, `.headlines.csv`, `.restated.csv`, `.keeppaths.csv`,
`.walkforward.csv`
**Params (2):** `statistic` ∈ {conv_per_pp, raw_per_pp, dSharpe_raw} × `f` ∈ {0, .25, .50, .75, 1.00}.
The sleeve is **not** a third parameter — it is whatever the statistic under test selects, which is
the only way to ask whether the normalisation changes what the record would have chosen.

**VERDICT: SPLIT.** The census is answered and yields **three corrections to the record**; the
queue's proposal — retire conv_per_pp and make `raw_per_pp` the reportable statistic — is
**KILLED as written**, on its own two grounds (raw_per_pp is *not* defined more often as the
record implements it, and it is the **worst** of four selectors out of sample). Rules unchanged.
**No new KEEP** (4a 1/1260 vs RULES v2; 4b 49/990 distinct, all previously known; every rule-8
pick loses to the no-sleeve control in 8 of 12 cells).

## Reproduction gates (nothing below was read until these passed)

- Matched cash sleeve is algebraically the book: max Sharpe spread across f = **4.441e-16**.
- Against idea 357's committed `grid.csv`, all **1,260** rows: max |diff| = **0.000e+00**.
- Idea 100's published headline reproduces to 3 dp: conv mean **+0.2646 (36/36)** for S4 and
  **+0.0524 (36/36)** for S9 (published +0.265 / +0.052); conv_per_pp medians **0.0902 / 0.0309**
  (published 0.090 / 0.031). Idea 103's ladder rho reproduces at **−0.6246** (published −0.624)
  and raw at **−0.2482** (published −0.240). Idea 357's pathology reproduces at **23/756** points
  with worst |conv_per_pp| **5.433e7**.

## The census

10 LEADERBOARD rows and 4 parent scripts carry a linear-blend dSharpe (file list derived by grep
at runtime, in `.console.txt`): ideas **26, 100, 100b, 103 (both lanes), 357**.

| published claim | as published (linear blend) | re-stated benchmark-free | changes? |
|---|---|---|---|
| **26** "dSharpe > 0 in 36/36, mean +0.052" | 36/36, +0.0524 | dSharpe_raw **23/36**, +0.0380 | **YES** |
| **100** S4 arm "36/36, +0.265" | 36/36, +0.2646 | dSharpe_raw **36/36**, +0.0905 | no (magnitude −66%) |
| **100** exchange rate "0.090 vs 0.031" | 0.0902 / 0.0309 | raw_per_pp **0.0366 / 0.0053** | no (ordering holds) |
| **100b** "S4 convexity higher in 36/36" | 36/36, +0.2122 | **25/36**, +0.0525 | **YES** |
| **100b** "S4 exchange rate higher in 32/36" | 32/36, **+0.0500** | **24/36, −0.1036** | **YES — mean flips sign** |
| **103** "conv_per_pp falls with correlation" (11-rung ladder) | rho −0.6246, R² 0.221, 33/36 cells neg | raw rho −0.2482 but **OLS slope +0.147 (t +2.43)**; dSharpe_raw rho −0.324 | **YES — rank and slope disagree** |
| same, on idea 357's wider 21-sleeve plane | conv rho **−0.111**, R² 0.0033 (n.s.) | raw **+0.3307**, dSharpe_raw **+0.3012**, negative in only **3/36** and **5/36** cells | **YES — sign reverses** |
| **357** "conv_per_pp explodes to 5.4e7" | reproduced exactly | **guard artefact** — see below | **YES** |

**CORRECTION 1 — the queue's premise "raw_per_pp is defined everywhere" is false as the record
implements it.** Over the 756 interior points, the record's own code NaNs `raw_per_pp` on
**80/756** and `conv_per_pp` on only **36/756**. The 80 are not a numerator problem: **64 of them
are points where the blend GAINED CAGR**, silently discarded by the one-sided guard
`give_pp > 1e-6`. raw_per_pp is defined more often only in its *numerator*, never in the record's
implementation.

**CORRECTION 2 — idea 357's "conv_per_pp explodes (5.4e7)" is a guard artefact, not a property of
the statistic.** The two statistics are guarded *differently* in every committed script:
conv_per_pp as `dSharpe / max(give, 1e-9)` (never NaN, explodes) and raw_per_pp as NaN unless
`give > 1e-6`. Applying **one common guard** (|give_pp| ≥ 0.05) to both:

| statistic | record's guard: NaN / |·|>10 / worst | common guard: NaN / |·|>10 / worst |
|---|---|---|
| conv_per_pp | 36 / **62** / **1.892e+08** | 41 / **0** / 0.873 |
| raw_per_pp | **80** / 0 / 4.58 | 23 / 0 / 2.143 |
| dSharpe_raw | **0** / 0 / 1.191 | 0 / 0 / 1.191 |

Under a common guard neither ratio explodes, and conv_per_pp's excess of undefined points is
**exactly 41 − 23 = 18**, the cash null's interior points — i.e. the *only* thing the linear-blend
yardstick actually costs in definedness is the cash null, not the "far beyond" of idea 357's row.
Both ratios share the same denominator, so a denominator pathology never separated them.

**CORRECTION 3 — the premise "it gives a different ordering" is confirmed, and far more strongly
than idea 103 stated.** Within each of the 36 (panel, book, conv, f) cells, mean spearman between
conv_per_pp and raw_per_pp is only **+0.3044**, and the two pick the **same argmax sleeve in 8 of
36 cells**. conv vs dSharpe_raw: +0.2917, 5/36. raw vs dSharpe_raw: +0.8133, 12/36. The
normalisation is not cosmetic — it changes the selection two times out of three.

## Rule 8 walk-forward — the decider (params on 2009–2016, 2017–2026 read once)

Four pre-registered choosers pick the (sleeve, f) pair maximising their own **in-sample** statistic;
C_SHARPE is the record's existing default; CTRL is the pure book. 12 cells (2 panels × 3 books ×
2 conventions).

| chooser | OOS Sharpe | OOS CAGR | OOS MaxDD | beats CTRL | beats SPY | beats v1 | beats v2 | 4b |
|---|---|---|---|---|---|---|---|---|
| **CTRL (no sleeve)** | **0.9193** | **10.41%** | −17.82% | — | **8/12** | 8/12 | 0/12 | **4/12** |
| C_CONV | 0.9250 | 9.36% | −17.23% | 4/12 | 7/12 | 11/12 | 0/12 | 1/12 |
| C_DELTA (dSharpe_raw) | 0.9222 | 8.34% | −16.21% | 4/12 | 7/12 | 12/12 | 0/12 | 1/12 |
| C_SHARPE (record default) | 0.9202 | 8.73% | −17.12% | 4/12 | 7/12 | 12/12 | 0/12 | 0/12 |
| **C_RAW (the proposal)** | **0.9050** | 8.27% | −15.08% | 4/12 | **6/12** | 12/12 | 0/12 | **0/12** |

References OOS: SPY **0.8820 / 15.45% / −33.72%**; RULES v2 **1.2851 (u56) / 1.1185 (broad)**;
RULES v1 0.7471 / 0.5763.

Head-to-head: **C_RAW beats C_CONV in 3/12 (mean −0.0200)**, C_DELTA in 2/12 (−0.0172), C_SHARPE
in 2/12 (−0.0151). **The proposed statistic is the worst selector of the four**, and every
statistic-driven chooser beats the no-sleeve control in only 4 of 12 cells while surrendering
1–2 pp of OOS CAGR to it. No chooser beats RULES v2 in any cell.

## KEEP paths (all 1,260 points reported, none selected on)

4b **137/1260** raw, **49/990** distinct books; 4a vs RULES v2 **1/1260**; 4a vs RULES v1 586/1260.
The best 4b pass is `u56 X_GLD top20 natural f=0.25` — 11.56% / **1.1539** / −14.58%, H1 1.0733 /
H2 1.2296, OOS **1.2844** — which is **idea 357's already-PARKed by-product reproduced to 4 dp**,
not a new candidate. It is selected by **none** of the four choosers, in any cell.

## What to report instead

The queue asked for `raw_per_pp` as the reportable statistic. The evidence does not support it: it
is neither better defined (as implemented, 80 NaN vs 36) nor a better selector (worst of four).
What the evidence *does* support is narrower and denominator-free:

1. **Report `dSharpe_raw = Sharpe(f) − Sharpe(0)`** — the only one of the three defined on all 756
   points (0 NaN, 0 absurd), including the cash null, and mid-pack rather than worst as a selector.
2. **Publish the CAGR give-up as its own column, never as a denominator.** Both ratios are
   uninterpretable near give_pp = 0 and *invert in sign* where give_pp < 0 (64 of 756 points) — a
   region the record currently hides behind a one-sided guard rather than reporting.
3. **Any per-pp figure already published must carry its guard**, because 62 of the record's
   "absurd" conv_per_pp readings and all 80 of its missing raw_per_pp readings are guard choices,
   not data.

Nothing here is a rules change; PROTOCOL rule 5's leaderboard row is the natural place, and that is
a Sunday-review question, not this run's.

## Limits

Both panels are current constituents (levels biased up); the sleeve ETFs are survivors by
construction. 10 bps, weekly, next-day execution through the shared engine. The 32-sleeve
population of idea 103 lane B is not rebuilt here — its 11-rung ladder is, and idea 357's 21-sleeve
plane is the superset used for the wider reading; the lane-B row is re-stated on the ladder it
shares, not on its own subset enumeration.
