# Idea 255 — does ddctl really own the deep budgets?

**Script:** `research/backtests/2026-09-09_does-ddctl-really-own-the-deep-budgets_cloud.py`
**Verdict: KILL / REFUTED — and the ordering is REVERSED.** At the deep budgets the claim is
about (T = 8–10 pp of MaxDD bought), the book-level drawdown control costs **0.5997** pp of CAGR
per pp of MaxDD against the de-gross lever's **0.3831** — ddctl is the *expensive* lever there, not
the cheap one, under both measurement conventions. It survives neither gross matching nor rule 8.

Two tuned parameters: **D** (trigger depth, 12 rungs 0.02 → 0.40 — the ladder idea 251 says the
claim needs) × **k** (armed multiplier, 4 rungs). Reset fixed at `high`. Panel, book and cost rung
reported at every level, not tuned. **1,323 ddctl/control points + 171 static-gross ladder points,
all reported** in `.grid.csv` / `.ladder.csv`.

## (0) Panels and comparands (weekly, next-day execution, 10 bps)

| panel | SPY CAGR/Sharpe/MaxDD | RULES v2 (live) | RULES v1 (superseded) |
|---|---|---|---|
| u56 | 15.19% / 0.887 / −33.72% | 8.64% / 1.204 / −12.05% | 6.42% / 0.661 / −13.83% |
| broad136 | 15.23% / 0.889 / −33.72% | 8.03% / 1.106 / −12.24% | 6.39% / 0.635 / −21.19% |
| small439 | 14.13% / 0.862 / −33.72% | 3.81% / 0.572 / −14.68% | 7.41% / 0.565 / −36.12% |

SMALL484 is run as **SMALL439**: the 44 tickers with `max_1d_move ≥ 1.0` in `data/small_meta.csv`
are dropped first, per the standing convention.

## (1) The claim, measured — exchange rate by drawdown budget T

`rate = (control CAGR − arm CAGR) / (|control MaxDD| − |arm MaxDD|)`, in pp per pp. Lower is
cheaper. De-gross is priced two ways: at the **matched DD budget** (the ladder rung that buys the
same T) and by **idea 40's fitted slope** over the whole ladder.

| bin (T, pp) | panel | n | **ddctl** | de-gross @T | Δ | ddctl cheaper | de-gross slope | cheaper vs slope |
|---|---|---|---|---|---|---|---|---|
| [0,2) | ALL | 173 | 2.5530 | 0.4515 | +2.1016 | 1 | 0.6100 | 1 |
| [2,4) | ALL | 41 | 0.7204 | 0.6401 | +0.0803 | 5 | 0.6100 | 3 |
| [4,6) | ALL | 56 | 0.7182 | 0.3816 | +0.3366 | 7 | 0.3828 | 8 |
| [6,8) | ALL | 38 | 0.5436 | 0.3056 | +0.2381 | 8 | 0.3022 | 8 |
| **[8,10)** | **ALL** | **22** | **0.5997** | **0.3831** | **+0.2166** | **3** | **0.3828** | **3** |
| [10,∞) | ALL | 101 | 0.2602 | 0.2155 | +0.0447 | 10 | 0.2374 | 10 |

Per panel in the 8–10 pp cell: u56 0.8691 vs 0.6673 (0/6 cheaper), broad136 0.5676 vs 0.4647
(3/10), small439 0.3309 vs 0.2108 (0/6). Full table for all six bins × three panels in
`.budget.csv`.

**THE 8–10 pp CELL: n = 22. ddctl median 0.5997 (range 0.1277–1.1954), de-gross 0.3831. Paired mean
delta +0.1494, t +4.27, ddctl cheaper in 3 of 22.** Against idea 40's fitted-slope convention:
de-gross 0.3828, paired delta +0.1512, cheaper in 3 of 22 — **the answer is not a measurement-
convention artefact**. Idea 251's "0.43–0.51 vs 0.58–0.61" has the two levers the wrong way round on
this ladder: nowhere in the 22-point cell does the ddctl median fall below the de-gross median.

There is exactly one bin where ddctl's median is cheaper — small439 at T ∈ [6,8), 0.1680 vs 0.2038,
6/17 — and it does not repeat on either large-cap panel or in the adjacent bins on the same panel.

### (1b) The D = 2% rung, which the claim specifically requires

| panel | book | D | n | median T | **ddctl** | de-gross | episodes | vs matched-gross Sharpe |
|---|---|---|---|---|---|---|---|---|
| u56 | CAND20 | 0.02 | 4 | 9.79 | 0.7787 | 0.7103 | 22.5 | −0.2660 |
| u56 | EWall | 0.02 | 4 | 5.04 | 1.0738 | 0.6736 | 17.0 | −0.1685 |
| u56 | V1 | 0.02 | 4 | 4.69 | 1.5956 | 0.4561 | 14.0 | −0.3591 |
| broad136 | CAND20 | 0.02 | 4 | 10.36 | 0.7128 | 0.6690 | 24.0 | −0.2298 |
| broad136 | EWall | 0.02 | 4 | 10.16 | 0.6014 | **0.6221** | 18.5 | −0.0481 |
| broad136 | V1 | 0.02 | 4 | 11.50 | 0.3806 | 0.3044 | 12.0 | −0.2400 |
| small439 | CAND20 | 0.02 | 4 | 15.35 | 0.2915 | 0.2236 | 12.0 | −0.1712 |
| small439 | EWall | 0.02 | 4 | 21.10 | 0.1205 | 0.0912 | 8.0 | −0.1141 |
| small439 | V1 | 0.02 | 4 | 19.78 | 0.2147 | 0.2083 | 11.5 | −0.0534 |

(D = 0.03 rows in the console output; same sign everywhere.) Running the ladder down to 2% is what
idea 251 said the claim needs, and it is where ddctl looks **worst**: 1 of 9 cells is cheaper than
de-gross, **8 of 72** D ≤ 3% arms are cheaper at matched budget, **2 of 72** beat the matched-gross
static book on Sharpe, and the median vs-matched-gross Sharpe is negative in **all 18** cells.

## (2) Does it survive gross matching? (idea 244's channel)

Every ddctl arm against the static-gross rung at its **own realised average gross** — the control
that removes "a drawdown rule that works by holding less".

| panel | n | beats matched-gross on Sharpe | on Sharpe AND MaxDD |
|---|---|---|---|
| u56 | 144 | **1 (0.7%)** | 1 |
| broad136 | 144 | **0 (0.0%)** | 0 |
| small439 | 144 | **6 (4.2%)** | 5 |
| **ALL** | **432** | **7 (1.6%)** | **6** |
| **deep, T ≥ 8pp** | 123 | **3 (2.4%)**, median ΔSharpe **−0.2716** | — |

Median ΔSharpe vs matched gross by budget bin (ALL): [0,2) 0.0000, [2,4) −0.0548, [4,6) −0.1168,
[6,8) −0.1370, **[8,10) −0.1708**, [10,∞) −0.3235. It gets monotonically worse with depth: the
deeper the budget, the more of ddctl's effect is just de-grossing, and the worse it does it. **No,
the deep-budget win does not survive gross matching.**

## (3) Rule 8 — (D, k) chosen on 2009–2016, evaluated untouched on 2017–2026

| panel | book | selector | pick | OOS Sharpe | control | matched-gross | RULES v2 | SPY |
|---|---|---|---|---|---|---|---|---|
| u56 | V1 | S1 max IS Sharpe | D15%/k0.00 | 0.7408 | 0.7408 | 0.7408 | 1.2817 | 0.8786 |
| u56 | CAND20 | S1 | D12%/k0.00 | **0.4956** | 1.1672 | 1.1666 | 1.2817 | 0.8786 |
| u56 | EWall | S1 | D12%/k0.00 | **0.3722** | 1.1091 | 1.1090 | 1.2817 | 0.8786 |
| broad136 | V1 | S1 | D10%/k0.00 | 0.4858 | 0.5763 | 0.5768 | 1.1185 | 0.8820 |
| broad136 | CAND20 | S1 | D15%/k0.00 | **0.3941** | 0.8919 | 0.8898 | 1.1185 | 0.8820 |
| broad136 | EWall | S1 / S2 | D12%/k0.00 | 0.4177 | 1.0185 | 1.0196 | 1.1185 | 0.8820 |
| small439 | V1 | S1 | D15%/k0.50 | 0.3118 | 0.4923 | 0.4945 | 0.5680 | 0.8820 |
| small439 | CAND20 | S1 | D4%/k0.50 | 0.4510 | 0.4873 | 0.4859 | 0.5680 | 0.8820 |
| small439 | EWall | S1 | D3%/k0.25 | **0.3167** | 0.2930 | 0.2935 | 0.5680 | 0.8820 |

**S2 (the IS-4b-aware selector) picks NOTHING in 9 of 10 cells** — no arm clears the in-sample 4b
bars — which is itself the honest answer.

- beating their own control OOS: **1/10** (small439 EWall, the panel's weakest book)
- beating the matched-gross static book OOS: **1/10**
- beating the live RULES v2 book OOS on Sharpe: **0/10**
- beating SPY OOS on Sharpe: **0/10**
- mean OOS Sharpe: pick **0.4404**, control 0.7795, matched-gross 0.7796
- mean OOS CAGR: pick **3.30%**, control 8.96%, matched-gross 6.08%; mean OOS MaxDD −16.7%

Choosing a ddctl setting in-sample costs **−0.34 of OOS Sharpe and −5.7 pp of OOS CAGR** against
simply not using one. The in-sample optimum is D ≈ 10–15% with k = 0 (full de-risk) on five of six
large-cap cells; out of sample that is the worst thing to have done.

## (3b) Degeneracy census — how many "ddctl arms" are the control wearing a label?

| panel | book | arms | never armed | numerically identical to control |
|---|---|---|---|---|
| u56 | CAND20 / EWall / V1 | 144 each | 56 / 52 / 56 | 56 / 52 / 56 |
| broad136 | CAND20 / EWall / V1 | 144 each | 48 / 48 / 36 | 48 / 48 / 36 |
| small439 | CAND20 / EWall / V1 | 144 each | 24 / 12 / 8 | 24 / 12 / 8 |
| **ALL** | | **1,296** | **340 (26.2%)** | **340 (26.2%)** |

A quarter of the ddctl grid is idea 458's constant-arm problem: at D ≥ 15–20% the trigger never
fires on these books and the "treated" arm *is* the control, to the last decimal. Any menu that
counts those as ddctl wins is counting the control several dozen times.

## (4) Both KEEP paths — all 1,323 grid points

| panel | book | n | 4a vs **LIVE RULES v2** | 4a vs superseded v1 | 4b |
|---|---|---|---|---|---|
| u56 | CAND20 / EWall / V1 | 147 each | 0 / 0 / 0 | 17 / 33 / 0 | 68 / 21 / 0 |
| broad136 | CAND20 / EWall / V1 | 147 each | 0 / 0 / 0 | 87 / 110 / 0 | 17 / 34 / 0 |
| small439 | CAND20 / EWall / V1 | 147 each | 0 / 0 / 0 | 11 / 0 / 5 | 0 / 0 / 0 |
| **TOTAL** | | **1,323** | **0** | **263** | **140** |

**4a: 0 of 1,323 against the live book, 263 against the superseded one.** A fresh grid reproducing
idea 482 (committed the same day) on new data: 4a counts written against RULES v1 do not transfer.

**4b: 140 — but 124 of them are relabelled controls.** Of the 140, 7 are the plain control and 133
carry a ddctl label; **124 of those 133 are numerically identical to their own control**
(never-armed duplicates). Only **9** are genuinely distinct ddctl books, all u56/CAND20, and all
nine are **shallow**-budget arms (T ≤ 2.05 pp — not deep ones), all nine **fail 4a against RULES
v2**, and all nine **lose or tie to their matched-gross static comparand on Sharpe** (ΔSharpe
−0.094 … 0.000). **Nothing here is a KEEP candidate and no memo is written.**

## Answer to the queue, in its own words

> *"report whether the deep-budget win survives gross matching and rule 8."*

**It does not survive either — and there was no deep-budget win to survive.** Measured directly on
the ladder idea 251 asks for (D down to 2%), ddctl costs **0.5997** pp CAGR per pp MaxDD at
T = 8–10 pp against de-gross's **0.3831** (t +4.27 paired, cheaper in 3/22), the same under idea
40's own fitted-slope convention. Gross-matched, it beats its comparand on Sharpe in 3 of 123 deep
arms with a median ΔSharpe of −0.2716. Chosen by rule 8 it loses 0.34 of OOS Sharpe to doing
nothing, 10/10 times against the live book and against SPY. Idea 251's flip of 4 of 40 menu picks
was a 4-cell median over a ladder region where **26.2% of the arms are the control in disguise**;
read on the full ladder with a matched-gross comparand, the sign is the other way.

## Caveats
- **SURVIVORSHIP:** `universe.json`, `universe_broad.json` and the small screen are all current-
  constituent lists, so every absolute CAGR is optimistic. Every number that answers the queue is a
  same-panel, same-days difference between arms and is far less exposed.
- `reset` is fixed at `high`; idea 40 also ran `recover`. Holding it fixed is what keeps the tuned
  count at two, but a `recover` ladder is not measured here.
- The exchange rate is undefined when an arm buys no drawdown (T ≈ 0); those 173 points sit in the
  [0,2) bin where the ratio explodes (ddctl median 2.55) and should not be read as an exchange rate.
- The 8–10 pp cell is 22 points. It is a small cell — but it is the cell the claim was made in, and
  the sign is consistent across all six budget bins and all three panels.
