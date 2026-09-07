# Idea 108 — S3-arm-cost-breakeven (lane B, 2026-09-07)

**Verdict: SPLIT.** The measurement the queue asked for is **ANSWERED** (`c* = 16.0 bps`
cross-universe, sharpening idea 101's `(15, 20]` bracket). The queue's stated **MECHANISM is
falsified** — the CAGR floor binds on u56 only; on broad it is H2, and across the record's
40 passing cells the modal binding bar is H1. And the run **downgrades the arm's capital
claim**: the out-of-sample cost budget is **3.5 bps cross-universe**, i.e. *below* PROTOCOL's
own 10 bps assumption. Rules unchanged; no new KEEP; one PROTOCOL proposal (report-only).

Script: `2026-09-07_S3-arm-cost-breakeven_B.py` · console `.console.txt` · grid `.grid.csv.gz`
(7,320 rows) · `.breakeven.csv` · `.binding.csv` / `.binding_IS.csv` / `.binding_OOS.csv` ·
`.walkforward.csv` · `.rule8.csv` · `.baselines.csv` · memo `_MEMO.md`.

## Reproduction gates (asserted before any new number was read)

| Gate | Result |
|---|---|
| G1 cost linearity (61-rung derivation vs a direct 10 bps run) | **max abs diff 0.000e+00** |
| G2 idea 101's committed S3 headline, u56, g1.00/W/10 bps | committed 11.5%/1.167/-13.3% OOS 1.215@12.3% → here **identical**, max abs diff 4.83e-04 |
| G2 idea 101's committed S3 headline, broad | committed 12.0%/1.073/-14.6% OOS 0.985@11.1% → here **identical**, max abs diff 4.82e-04 |
| identity: `be_joint == min` of the five per-bar breakevens `== D1`'s be | **0.000e+00** on all 120 cells |

Two tuned parameters (PROTOCOL rule 4): `f ∈ {0, .25, .50, .75, 1.00}` × `cost ∈ 0..30 bps by
0.5` (61 rungs). Controls, reported and never selected on: universe {u56, broad}, arm {S3
pre-registered, S4}, gross convention {g1.00 pre-registered, natural}, cadence {W
pre-registered, M, D}. 120 cells × 61 rungs = **7,320 points, all reported**.

## D1 — the 0.5 bp breakeven curve (full-sample 4b)

Candidate cell `top20 + 50% (TLT,GLD,UUP)` @ g=1.00, weekly:

| f | u56 | broad | cross-universe |
|---|---|---|---|
| 0.00 | never | never | never |
| 0.25 | 25.5 | never | never |
| **0.50** | **16.0** | **16.5** | **16.0** |
| 0.75 | never | never | never |
| 1.00 | never | never | never |

**`c* = 16.0 bps`.** Idea 101's 5-bps grid could only bracket it to `(15, 20]`; the 0.5 bp grid
puts it at 16.0. The pass region is one contiguous interval (0 holes on both panels), as a
monotone cost curve requires. Headroom over PROTOCOL's 10 bps assumption is **6.0 bps (1.60×)**.
At the arm's turnover — **12.42 units/yr (u56), 15.23 (broad)** — 16.0 bps is a cost budget of
**≈2.0%/yr of NAV**; the 10 bps assumption spends ≈1.24%/yr of it.

## D2 — which bar binds (the queue's claim, tested)

Per-bar breakeven at f=0.50, full sample:

| panel | be_H1 | be_H2 | be_OOS | be_DD | be_CAGR | joint | **binding** |
|---|---|---|---|---|---|---|---|
| u56 | 25.0 | 30.0 | 30.0 | 30.0 | **16.0** | 16.0 | **CAGR** |
| broad | 29.0 | **16.5** | 17.5 | 30.0 | 17.5 | 16.5 | **H2** |

**The queue's "CAGR floor binding first" is a one-universe result.** It holds on u56, where the
CAGR margin is razor-thin (+0.0228 at 0 bps → **+0.0006 at 16.0**, ≈0.14 pp of CAGR per bp). On
broad the second-half Sharpe bar dies first (margin +0.2102 → **+0.0001 at 16.5**) with CAGR
still alive to 17.5. Census over the **40 of 120** cells that clear 4b at 0 bps at all:
**H1 20, CAGR 15, H2 5** — the CAGR floor is not even the modal binding bar. Of the 80 cells
that never pass, the sole blocker is CAGR in 34 and the drawdown cap in 20.

## D3 — the walk-forward spread on the breakeven (the number sizing depends on)

`be_IS` / `be_OOS` = the same bar set re-measured inside 2009–2016 / 2017–2026 (4 bars inside a
single window: there is no separate OOS-Sharpe bar there — stated, not hidden).

| panel | be_full | be_IS | be_OOS | **spread (IS − OOS)** | bar setting be_OOS |
|---|---|---|---|---|---|
| u56 | 16.0 | 11.0 | 21.0 | **−10.0** | CAGR |
| broad | 16.5 | 15.0 | **3.5** | **+11.5** | **H1** |

**The spread is not a haircut — it is sign-unstable across the two universes**, and they
disagree by 21.5 bps on a quantity whose full-sample value is 16. Census over the 25 cells
where it is defined: 5 positive, 9 zero, 11 negative; the sign is *panel*-signed
(u56 mean −10.69, broad mean +4.11), not idea-signed. Idea 128's prediction that IS breakevens
are biased up holds on broad and **reverses on u56**.

**Cross-universe out-of-sample budget = 3.5 bps**, set by broad's first-half-of-OOS Sharpe:
at 10 bps that margin is already **−0.0760** (arm 0.899 vs SPY 0.975 over 2017–2021). Note the
gap this exposes in the bar set itself: PROTOCOL 4b's OOS clause is a *single aggregate* Sharpe
comparison over 2017–2026 (margin +0.1034 on broad at 10 bps — it passes), while requiring the
same four bars *inside* the OOS window is strictly stronger and the arm **fails it at PROTOCOL's
own cost** on broad. The full-sample `c* = 16.0` is therefore an in-sample-assisted number.

## 4a — a correction to the record under the live baseline

Idea 101 published "**4a on both universes to 25 bps**". Against **RULES v1** that reproduces and
is if anything understated: the arm passes to **≥30 bps** on both panels (right-censored; idea
101's grid stopped at 25). Against **RULES v2 — the live book since 2026-09-06 and the
comparand PROTOCOL rule 3/4a now names — the arm passes 4a at NO cost, not even 0 bps, on
either panel.** Over all 120 cells: 4a vs v1 78/120, 4a vs v2 **15/120**. Idea 101's 4a claim
did not survive the baseline switch and should not be quoted forward.

## Rule 8 (walk-forward, required)

`f` chosen on 2009–2016 IS Sharpe alone per (panel, arm, conv, cadence, cost); 2017–2026 read
untouched. **The selector picks f=0.50 in 122/122 rungs of the candidate cell — zero regret at
every one of the 61 costs**, confirming idea 101's selector result across the whole ladder
(72.4% over all 1,464 cells; mean regret +0.0058 Sharpe).

OOS (2017–2026) at the headline 10 bps:

| | CAGR | Sharpe | MaxDD |
|---|---|---|---|
| arm, u56 | 12.27% | **1.215** | −13.29% |
| arm, broad | 11.13% | **0.985** | −14.62% |
| RULES v2, u56 | 9.53% | **1.285** | −12.05% |
| RULES v2, broad | 7.98% | **1.119** | −12.24% |
| SPY | 15.45% | 0.882 | −33.72% |

The arm beats SPY's OOS Sharpe on both panels and loses to RULES v2's on both — the same fact
the 4a failure states, seen from the other side.

## Caveats carried

SURVIVORSHIP (idea 54): u56 and broad are current-constituent lists, so the equity legs are
biased up while the SPY bars are not — the **absolute** breakeven is biased up; the f-contrast
and the IS-vs-OOS spread are cleaner. Idea 38: calendar-day index post-2014-09-17. Flat bps per
unit turnover, both ways, no spread/impact/borrow model — `c*` is an **all-in** budget, not a
commission estimate. Right-censoring at 30 bps is labelled, never read as "30".
