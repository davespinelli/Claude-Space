# Idea 2260 (2026-09-22, lane C) — result

**Script:** `research/backtests/2026-09-22_voltgt-gross-vs-constant-gross-at-matched-CAGR_C.py`
**Artefacts:** `.console.txt`, `.grid.csv` (720 book rows), `.ladder.csv` (110 constant-gross
rows), `.matched.csv`, `.choosers.csv` (120 rule-8 rows), `.gates.csv`.
**Gates: 12 of 12 PASS**, including G3 (committed cells of ideas 2233 / 2237 / 2264 reproduce
at max |Δ| **5.0e-05**), G2 (the degenerate limit TARGET = 10 pins the scaler to CAP and the
book equals the constant-gross book at g = CAP at max |Δw| **0.000e+00**), G4 (no lookahead in
`sigma_t`, 0.000e+00 over 15 truncation checks), G5 (derived cost ladder = re-simulation at
25 bps, 0.000e+00), G7 (ladder CAGR strictly increasing in g, min step +1.43 pp / +1.33 pp).

## ANSWERED = YES on the literal question, and the honest answer is that the win is real, small, and lookback-bound.

### 1. The 4b question as the idea worded it: **YES — 35 of 720 cells.**
35 cells clear 4b on the FULL sample **and** on the rule-8 OOS window while carrying **CAGR ≥
the constant g = 1.00 rung's** and a **strictly larger 4b drawdown margin** than g = 1.00.
The cleanest — and the only **unlevered** one (PROTOCOL rule 2) — is

    u56, L = 20, TARGET = 0.20, CAP = 1.00, band 0.03, weekly, t+1

which **strictly dominates the record's only reliable 4b passer on every reported statistic at
every cost rung 0 / 5 / 10 / 25 / 50 bps at the same turnover**:

| @10 bps, u56 | CAGR | Sharpe | MaxDD | H1 / H2 | OOS CAGR | OOS Sharpe | OOS MaxDD | TO/yr |
|---|---|---|---|---|---|---|---|---|
| voltgt t=0.20 cap=1.00 | **11.56%** | **1.2102** | **−15.16%** | 1.2309 / 1.1945 | **12.71%** | **1.2908** | **−15.16%** | 2.363 |
| constant g = 1.00 (2233/2264) | 11.53% | 1.2009 | −15.91% | 1.2282 / 1.1799 | 12.67% | 1.2760 | −15.91% | 2.352 |
| live RULES v2 (g = 0.75) | 8.62% | 1.2010 | −12.05% | 1.2276 / 1.1806 | 9.46% | 1.2767 | −12.05% | 1.770 |
| SPY | 15.14% | 0.8851 | −33.72% | — | 15.29% | 0.8751 | −33.72% | — |

**But the margin is +0.75 pp of MaxDD and +0.009 / +0.015 of Sharpe**, which sits *inside* the
record's own paired block-bootstrap MaxDD SE of **2.93 pp** (idea 1511). And it inherits idea
2264's panel dependence exactly: on **b136 it clears 4b FULL at every rung but fails 4b OOS from
5 bps on**, on the OOS CAGR floor. **This is not proposed as a new 4b candidate** — it is a
strictly-better restatement of the one the record already has, not a different result.

### 2. The mechanism claim behind the idea is **FALSIFIED as a general fact: it is a LOOKBACK fact, not a vol-targeting fact.**
`dDD_vs_matched` = MaxDD(vol target) − MaxDD(constant gross interpolated to the *same* full-sample
CAGR); positive = the vol target buys the drawdown leg more cheaply. All 720 cells lie inside the
ladder's CAGR range, so every cell is matched and published.

| lookback | share dDD > 0 (u56 / b136, 0–10 bps) | median dDD @10 bps (u56 / b136) |
|---|---|---|
| **L = 20** | **1.000 / 1.000** | **+2.14 pp / +1.39 pp** |
| L = 63 | 0.542 / 0.833 | +0.12 pp / +0.70 pp |
| L = 126 | **0.000 / 0.000** | **−0.87 pp / −0.28 pp** |

Pooled over all 720 cells the effect is a coin flip: **366 of 720 positive (0.508)**, median
**+0.007 pp**. So "a trailing-vol target spends the drawdown budget where it is cheap" is true at
a **20-day** window and **false at 126 days on both panels at every cost rung**. Lookback is a
REPORTED axis in this run, never tuned — which is precisely why this reading is available.
Any future claim that vol targeting dominates constant gross on the drawdown axis must state
its σ window.

### 3. The unexpected result, and the one worth capital: **a second PROTOCOL-4a passer.**
4a is the path the record has failed 0-for-hundreds on (2264: 0 of 110 book + 0 of 170 chooser
cells; idea 2213(B)'s idle-NAV accounting fix was the only passer on file). **24 of 720 cells
clear 4a here**, all of them at **CAP = 0.75** (the live gross, so nothing is levered and no
financing is assumed), all at TARGET ∈ {0.12, 0.15}, on **both panels at all five cost rungs**:

| @10 bps | CAGR | Sharpe | MaxDD | H1 / H2 | OOS CAGR | OOS Sharpe | OOS MaxDD | TO/yr |
|---|---|---|---|---|---|---|---|---|
| **u56 voltgt t=0.12 cap=0.75** | 8.56% | **1.2150** | **−10.59%** | **1.2369 / 1.1974** | 9.35% | **1.2958** | **−10.59%** | 1.824 |
| u56 live RULES v2 | 8.62% | 1.2010 | −12.05% | 1.2276 / 1.1806 | 9.46% | 1.2767 | −12.05% | 1.770 |
| **b136 voltgt t=0.12 cap=0.75** | 7.87% | **1.1079** | **−10.70%** | **1.2333 / 0.9826** | 7.78% | **1.1208** | **−10.70%** | 2.054 |
| b136 live RULES v2 | 7.96% | 1.0972 | −12.24% | 1.2296 / 0.9669 | 7.85% | 1.1017 | −12.24% | 2.011 |

It beats the live book's Sharpe **in both halves** with MaxDD **1.46 pp shallower**, gives up
**0.06 pp of CAGR**, and adds **0.05 turns/yr**. The same holds on the rule-8 OOS window read
once: **OOS 4a passes 10 of 10 panel × cost cells** (OOS Sharpe higher and OOS MaxDD shallower
at 0 / 5 / 10 / 25 / 50 bps on both panels).

### 4. RULE 8 — 2009–2016 chooses, 2017–2026 read once (120 published chooser rows).
`C_SHARPE`, the record's *habitual* IS-only chooser and the one idea 2264 showed blows the DD cap
on the gross ladder, **picks exactly (0.12, 0.75) on u56 at L = 20 at every one of the five cost
rungs** — so the 4a candidate is rule-8 reachable by the record's default chooser, with no
new chooser invented for it. Scoreboard on the 4b leg (30 panel × lookback × cost cells each):
`C_DDB060` **20 / 30**, `C_CALMAR` 15 / 30, `C_SHARPE` 14 / 30, `C_LIVE` (fixed t = 0.10,
cap = 1.00, no-information control) 10 / 30.

### 5. Plateau, not a spike — but a narrow one.
On the CAP = 0.75 target ladder at L = 20, 4a passes at **t = 0.12 and t = 0.15 on BOTH panels
and nowhere else**: t = 0.10 fails (H2 Sharpe below live), t = 0.20 fails because the scaler
stops biting (mean scaler 0.7496, MaxDD identical to the live book's). Two adjacent rungs of six,
bounded identically on two independent panels.

### 6. THE CAVEAT THAT DECIDES THE STATUS — the 4a pass is a **20-day** fact.
At **L = 63 and L = 126 the same cell's MaxDD is exactly the live book's** (−12.05% / −12.24%,
to the basis point) and **4a fails on every panel and cost rung**. The mechanism is visible: at a
slow σ the scaler is still pinned at CAP through the worst episode, so the book *is* the live book
through the drawdown; only the 20-day window de-grosses into it. `sigma_20` is the convention the
committed 2026-09-20 `voltgt` memo already uses and was declared in this script's header before
the run, so it is not chosen by this run's numbers — but the result is one convention wide.

### 7. Other counts, all published.
4b FULL 206 / 720, 4b OOS 227 / 720, 4b BOTH 192 / 720; unlevered sub-grid (CAP ≤ 1.00) 4b BOTH
40 / 360, 4a 24 / 360. First failing 4b leg over all 720: FULL — CAGR floor 458, DD 51; OOS —
CAGR 443, DD 51, Sharpe 13. **The CAGR floor is what kills this family, not drawdown**, matching
the record.

### 8. Caveats carried.
SURVIVORSHIP (PROTOCOL rule 9 / idea 54): u56 and b136 are CURRENT constituents held from 2008,
so every CAGR level is optimistic and both 4b level legs are easier than on a point-in-time panel.
CAP rungs above 1.00 are levered and the engine charges **no** financing, borrow or margin cost —
hence every headline above is also given on the unlevered sub-grid. Costs are flat per unit
turnover: no spread, impact or borrow. One cadence (W), one delay (t+1), one band (3%).
`RULES.md`, `PROTOCOL.md`, `scan.py`, `bot.py` and `baseline.py` are untouched by this run.

## Verdict
**KEEP-candidate, PROTOCOL path 4a** (`voltgt t = 0.12, cap = 0.75, σ₂₀`) — memo:
`research/backtests/2026-09-22_voltgt-cap075-t012_KEEP4a_MEMO.md`, with point 6 attached.
**PARK on path 4b**: the 4b answer is YES but the winning cell beats the incumbent g = 1.00 by
less than the record's own MaxDD standard error and fails on the second panel out of sample.
