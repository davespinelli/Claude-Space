# Idea 399 — does a ROLLING breadth quantile fire at its own nominal rate?

**Cloud lane, 2026-09-10. Verdict: SPLIT — the QUEUE'S SUSPICION IS CONFIRMED (idea 336 measured its Q3 KILL on a crippled instrument) and the KILL SURVIVES ANYWAY at PROTOCOL's cost rung.** A trailing-w quantile fixes the level: median realised/nominal **0.884 vs QEXP's 0.207**, and at **w = 1008** on armed days it is **0.85–1.03 on every panel** against idea 336's 0.00–0.31. It keeps what the quantile form bought — cross-panel rate spread **0.003–0.034 vs ABS's 0.193/0.413/0.686**. The chooser stops picking dead arms: **0 of 54 QROLL cells pick an arm firing < 1% of days, against 15 of 18 for QEXP**, and the picks beat doing nothing on OOS Sharpe **50/54 (mean +0.102)** vs QEXP's 3/18. But it still earns no KEEP: **4a 3 of 1296, all three at ZERO cost**; at PROTOCOL's 10 bps rung, **4a 0** and every rule-8-chosen 4b pass (2 of 18) sits on a **parent that already passes 4b**. No RULES change, no book promoted; RULES.md, PROTOCOL.md, scan.py, bot.py, baseline.py untouched.

Script: `research/backtests/2026-09-10_does-a-ROLLING-breadth-quantile-fire-at-its-own-nominal-rate_cloud.py` (+ `_addendum.py` for the G3 diagnosis)
Data: `.grid.csv` (1 989 rows), `.rates.csv`, `.matched.csv` (216), `.walkforward.csv` (90), `.picks.csv`, `.console.txt`.

## Design

Base book fixed and never tuned, idea 28/42/336's: **EWALL(G)** = equal-weight every name above its own 200d MA with `vol20 < 0.60`, at `G/E_t`, weekly, next-day execution; the overlay carries the book at `(1 − depth)` when panel breadth is low and pays the rung on `|Δmult|·G` at t+1. Families: **ABS(B)** (idea 42, B ∈ {0.30, 0.40, 0.50}), **QEXP(q)** (idea 336's causal expanding quantile), **QROLL(q, w)** (this idea: trailing-w-day q-quantile through t only), plus **NOGATE** and a **matched-mean-gross static twin**. **Two tuned parameters, exactly as the queue names them: w ∈ {252, 504, 1008, 2016} × depth ∈ {0.25, 0.50, 1.00}**, 12 points, all reported. Reported and never selected on: q ∈ {0.07, 0.12, 0.17} (idea 336's own nominal levels, inherited verbatim), panel {U56, B136, SMALL439}, gross {0.75, 1.00}, cadence {D, W}, cost {0, 10, 25} bps.

**Gates.** G1 derived cost rung vs live `engine.backtest(25)` **0.000e+00 PASS**. G2 idea 84's ungated EWALL U56 g=0.85 @10 bps 11.755% / 1.046 / −17.894% / H 1.07 / 1.03 vs committed 11.8% / 1.05 / −17.9% / 1.07 / 1.04 **PASS**. G4a the estimator on an **IID** control fires at its nominal q to **3.1e-03 PASS**; G4b the same estimator on an **AR(1) ρ=0.98** control (breadth-like persistence) fires at 0.1569 / 0.1394 / 0.1262 / 0.1228 for w = 252 / 504 / 1008 / 2016 against q = 0.12 — **measured, not a bar**, and it is the reference against which the panel numbers below should be read: short windows over-fire *because breadth is persistent*, not because the panel is odd. **G3 FAILS its 1e-9 bar and the addendum locates why**: joined to idea 336's committed grid on all 432 re-run ABS/QEXP arms, max abs diff **1.139e-02**; but **B136, whose cache did not move, is bit-identical at 2.220e-16**, and truncating U56 to idea 336's own vintage (2026-09-04) cuts the residual to **1.606e-05, a 709× reduction**. What truncation cannot remove (1.6e-05, with a vintage-invariant MaxDD floor of 1.11e-06) is a **price restatement in `data/prices.csv`** — the same U56 channel idea 592 filed at 1.9e-06 and idea 519 named. **G3 fails for a DATA reason, not a code one**, and it is reported as a failure regardless.

## Q1 — level fidelity: FIXED, and `w` is the dial

realised / nominal q, **armed days only** (all-days figures in `.rates.csv`; unarmed days are gate OFF):

| family | w | B136 .07/.12/.17 | SMALL439 .07/.12/.17 | U56 .07/.12/.17 |
|---|---|---|---|---|
| QEXP (idea 336) | — | 0.000 / 0.207 / 0.277 | 0.004 / 0.165 / 0.284 | 0.032 / 0.270 / 0.306 |
| QROLL | 252 | 1.747 / 1.462 / 1.284 | 1.768 / 1.394 / 1.265 | 1.586 / 1.344 / 1.156 |
| QROLL | 504 | 1.549 / 1.323 / 1.178 | 1.227 / 1.059 / 0.975 | 1.606 / 1.241 / 1.083 |
| **QROLL** | **1008** | **1.025 / 0.946 / 0.854** | **0.901 / 0.894 / 0.867** | **1.025 / 0.968 / 0.865** |
| QROLL | 2016 | 1.017 / 0.972 / 0.901 | 0.800 / 0.727 / 0.732 | 1.058 / 0.934 / 0.891 |

**w = 1008 (4 years) is the fidelity point** — within 15% of nominal on all nine panel×q cells and within 3% at q = 0.07. w = 252 over-fires by 1.16–1.77×, which G4b predicts from persistence alone; w = 2016 is fine on armed days but costs 39–45% of the eval sample to warm-up, so its **all-days** ratio falls to 0.40–0.64. Idea 336's "q = 0.07 is inert (0.000–0.002 of days)" is **fully repaired**: QROLL's q = 0.07 fires on 3.1–12.4% of days depending on w.

## Q2 — cross-panel equalisation: KEPT

Cross-panel spread of the realised rate: **QROLL 0.0028–0.0337 (median 0.0180)**, QEXP 0.0023–0.0126 (median 0.0049), **ABS 0.193 / 0.413 / 0.686 (median 0.383)**. The rolling form is ~20× looser than the expanding one and ~20× tighter than the absolute one — it buys nearly all of the equalisation while giving back none of the level. Fidelity and equalisation are different claims and both are reported.

## Q3 — what the fixed instrument EARNS (the part idea 336 could not measure)

- **Against the matched-mean-gross static twin** (same average exposure, no timing), 10 bps, g = 0.75: **QROLL beats it in 208 of 216 cells** (median ΔSharpe +0.023 to +0.063, ΔOOS +0.036 to +0.109) against **QEXP's 31 of 54**. This is the substantive correction to idea 336: a gate that actually fires is *not* just a gross dial in a timing costume.
- **Against PROTOCOL's KEEP paths it still fails.** 4a: **3 of 1296, every one at rung 0** (B136, QROLL q=0.17/0.12, w=252/504) — at 10 and 25 bps, **zero**. 4b: 385 of 1296 overall but the passes are a **cost and gross artefact**: rung 0 / 10 / 25 = 228 / 113 / 44, and at gross 0.75 with 10 bps only **14 of 216**.
- **Rule 8 is the only 4b claim PROTOCOL allows**, and it is decisive: of the 18 QROLL chooser cells at 10 bps, **2 pass 4b — both on B136, both w = 1008** (q=0.07 d=0.25 D, OOS Sharpe 1.081; q=0.12 d=0.50 W, OOS 1.161) — and **both sit on a B136 parent that already passes 4b on its own**. Uninherited passes at the protocol rung: **0 of 30** across all three families. At 25 bps nothing passes anywhere.
- **Q4, the chooser:** QROLL picks an arm firing < 1% of days in **0 of 54** cells (QEXP: 15 of 18, median picked rate 0.0003), beats doing nothing OOS in **50 of 54** (mean +0.102; QEXP 3/18, mean −0.000; ABS 12/18, mean −0.047), beats SPY OOS in 36/54, and beats **RULES v2 OOS in 17/54** against **0/18 for both comparands**. Mean regret −0.135.

## Verdict and what the record should do

**SPLIT.** Idea 336's Q3 KILL was measured on an instrument that barely fired, and the queue was right to flag it — the diagnosis it drew ("the quantile family earns nothing") does not survive contact with a rate-faithful version, which beats both do-nothing and its own matched-gross twin almost everywhere. But the KILL's *conclusion* stands where PROTOCOL puts the bar: **no 4a at 10 or 25 bps, and no uninherited rule-8 4b pass at the protocol rung**. Nothing is promoted and nothing is PARKed as a book.

Filed for the queue: (1) **w = 1008 is the rate-faithful default** for any future breadth-quantile arm, and any published quantile-gate result run on an expanding window should be re-read at w = 1008 before it is quoted; (2) idea 336's committed **q = 0.07 arms are inert and their verdicts are uninformative**, not negative; (3) the U56 `data/prices.csv` **restatement channel is live at 1.6e-05** after the append is removed — G3-style gates on U56 should quote a truncated-vintage number beside the raw one.

SURVIVORSHIP: all three panels are current-constituent lists (SMALL439 = the sub-$2B panel less the 44 names with `max_1d_move ≥ 1.0`), so CAGR and drawdown *levels* are optimistic; the gated-vs-parent and gated-vs-twin contrasts are the durable part. SMALL439 starts 2010-01-04, so its halves are not the same calendar halves as U56/B136's, and w = 2016 costs it 45% of its eval sample in warm-up.
