# Idea 2129 (lane B, 2026-09-22) — does a DRAWDOWN-BUDGETED GROSS convert the live book's UNSPENT DD MARGIN into CAGR?

**VERDICT: KILL, decisively, and on a strictly harder control than the last attempt.** The live
band book's ~8 pp of unspent 4b drawdown budget is **not spendable by reading the book's own
drawdown**. Of the **100** finite-budget cells published, **0 induce a 4b flip** their own static
twin does not already have; the budgeted book **loses Sharpe to its matched-mean-gross static
twin in 120 of 120 cells** (median −0.1240, mean −0.2666, best −0.0325); and rule 8's IS-Sharpe
chooser picks **D = inf — no budget at all — on both panels and both arms**. No RULES change, no
KEEP, no memo. RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py untouched (rule 6).

Script `2026-09-22_drawdown-budgeted-gross_B.py` · **3,000 published grid rows**
(`.grid.csv.gz`: 2 panels × 5 budgets × 5 ceilings × 5 offsets × 4 cost rungs × 3 windows) ·
console `.out.txt` · 274 s, deterministic, offline.

## The device and the two dials

`gross_t = g_hi · (1 − dd_t / D)` clipped to `[0, g_hi]`, with `dd_t` the book's **own** trailing
drawdown read at the decision close and applied at t+1 (gate G3 proves causality by shocking the
last day's prices and finding the gross path bit-identical). Base = RULES v2's frozen band clause
(`band_state`, band 0.03, equal weight, fixed denominator N = names priced). **Exactly two tuned
parameters, every point published:** budget `D ∈ {0.05, 0.10, 0.15, 0.20, ∞}` and ceiling
`g_hi ∈ {0.75, 0.85, 0.90, 0.95, 1.00}`. `D = ∞` is the static control column and
**(g_hi 0.75, D ∞) IS `baseline.rules_v2_weights` — gate G2, max|d| = 0.000e+00**, so the ladder
literally contains the live book. Weekly, t+1, long-only, **no leverage anywhere** (g_hi ≤ 1.00
forces the matched twin's λ ≤ 1.00, so no financing question arises). 8 of 8 gates PASS.

## What is new against idea 852, which already returned KILL here

852 (2026-09-14, lane B) throttled this same book on its own equity and killed it. Three legs are
new and the KILL is correspondingly larger: (i) the response is **continuous**, so there is no
threshold to be inert at — 852's passes were all arms whose trigger never fired, here **every**
finite-D cell fires; (ii) the **ceiling is a published dial from the live 0.75 up to 1.00**, so
the "spend the budget" half — running *larger* than the live book while nothing has gone wrong —
is priced, which 852's gross-1.00 parent structurally could not do; (iii) every cell is scored
against a **matched-mean-gross twin** (gate G4, max|d| 1.110e-16), the null the record adopted
after 852. Idea 69 measured a matched-constant-gross premium of `+0.027 / +0.030` Sharpe for a
**different** budget construction (a trailing-1y SPY-vs-book ratio, T=0.70/L=252), which is NOT
re-run here and is NOT refuted by this run. What this run establishes is narrower and its own:
for the *equity-drawdown-proportional* response, the matched-gross premium is **negative in 120
of 120 cells**. Whether 69's construction keeps its sign under this control is still open.

## (A) THE HEADLINE — the budget never flips a verdict, and the DD leg never binds

4b at d=0, 10 bps: **8 passes of 150** (panel × window × cell), and **all 8 are `D = inf`**.

| panel | window | 4b | 4a | H1 | H2 | **DD** | **CAGR** |
|---|---|---|---|---|---|---|---|
| U56 | FULL | 2/25 | 0/25 | 20 | 20 | **25/25** | **2/25** |
| U56 | IS | 0/25 | 0/25 | 6 | 20 | **25/25** | **0/25** |
| U56 | OOS | 4/25 | 0/25 | 20 | 20 | **25/25** | **4/25** |
| B136 | FULL | 1/25 | 0/25 | 20 | 14 | **25/25** | **1/25** |
| B136 | IS | 1/25 | 0/25 | 5 | 19 | **25/25** | **1/25** |
| B136 | OOS | 0/25 | 0/25 | 22 | 15 | **25/25** | **0/25** |

**The DD leg passes 150 of 150 and the CAGR leg carries every failure.** The device is an
instrument for buying the one thing the book already has a surplus of. **Budget-induced flips: 0.**

## (B) THE CAGR FLOOR IS MONOTONE IN D, AND THE BEST BUDGET IS NO BUDGET

CAGR-floor margin (pp), rows g_hi, cols D = 0.05 / 0.10 / 0.15 / 0.20 / ∞ — **U56 OOS**:

| g_hi | 0.05 | 0.10 | 0.15 | 0.20 | ∞ |
|---|---|---|---|---|---|
| 0.75 | −9.65 | −4.21 | −3.14 | −2.63 | **−1.24** |
| 0.85 | −9.47 | −3.92 | −2.43 | −1.77 | **+0.04** |
| 0.90 | −10.57 | −3.84 | −2.10 | −1.37 | **+0.68** |
| 0.95 | −10.70 | −3.83 | −1.80 | −0.97 | **+1.32** |
| 1.00 | −10.70 | −3.90 | −1.52 | −0.60 | **+1.97** |

Every row is monotone increasing in D, on **all six panel × window blocks**. B2's pre-stated test
— *can the budget dial lift the floor margin above zero at the LIVE ceiling 0.75?* — answers **NO
on every panel and window**, and the best margin reachable at g_hi = 0.75 is exactly the live
book's own (U56 −1.98 / −2.86 / −1.24 pp FULL/IS/OOS; B136 −2.63 / −2.38 / −2.83 pp).

## (C) THE MECHANISM — the budget dial is a BETTER drawdown buyer and a WORSE CAGR keeper

Per pp of **mean gross given up** (U56 FULL, against each row's own D = ∞ anchor):

| dial | DD saved | CAGR paid |
|---|---|---|
| **budget D** (0.10–0.20, all five ceilings) | **+0.320 … +0.371 pp/pp** | **−0.265 … −0.273 pp/pp** |
| **static gross** (D = ∞, against g_hi 1.00) | +0.228 … +0.230 pp/pp | **−0.174 pp/pp** |

B136 is the same picture (budget +0.270…+0.365 vs static +0.232…+0.234 on DD; −0.238…−0.267 vs
**−0.159** on CAGR). So the timing **is** real — the budget dial genuinely converts exposure into
drawdown protection ~1.5× more efficiently than the flat dial. It is simply **50–70% more
expensive in CAGR per unit of exposure**, and CAGR is the only leg that binds. MaxDD is monotone
in D at **10 of 10** (panel × ceiling) rows.

## (D) THE MATCHED-MEAN-GROSS NULL — 120 of 120, no survivors

Against its arithmetically matched static twin (same mean target gross by construction):
**DISTINCT 108/120 (90.0%), MARGINAL 12/120, INDISTINGUISHABLE 0/120** — but distinct in the
**wrong direction**. dSharpe median **−0.1240**, mean −0.2666, range [−1.1611, **−0.0325**]:
the budgeted book **beats its twin on Sharpe in 0 of 120 cells**. dCAGR median −0.845 pp (beats in
3/120); dMaxDD median +0.696 pp (beats in 70/120, the half-win that (C) explains). This is the
record's eighth consecutive finding that a DD-buying device is dominated at matched exposure —
and the first where the device wins on drawdown and still loses, because it is billed in CAGR.

## (E) RULE 8, 2017–2026 READ ONCE — the chooser refuses the dial

IS-Sharpe argmax over 2009–2016 only, per panel, then OOS read once.

| arm | panel | pick | OOS book | RULES v2 OOS | SPY OOS | 4b | 4a |
|---|---|---|---|---|---|---|---|
| free | U56 | **D ∞ / g_hi 1.00** | 12.67% / **1.2760** / −15.91% | 9.46% / 1.2767 / −12.05% | 15.29% / 0.8751 / −33.72% | **PASS** | FAIL |
| free | B136 | **D ∞ / g_hi 1.00** | 10.47% / 1.1006 / −16.16% | 7.85% / 1.1017 / −12.24% | 15.26% / 0.8737 / −33.72% | **FAIL** (CAGR −0.21 pp) | FAIL |
| live-ceiling | U56 | **D ∞ / g_hi 0.75** | 9.46% / 1.2767 / −12.05% | — (it *is* the live book) | — | FAIL (CAGR −1.24 pp) | FAIL |
| live-ceiling | B136 | **D ∞ / g_hi 0.75** | 7.85% / 1.1017 / −12.24% | — (it *is* the live book) | — | FAIL (CAGR −2.83 pp) | FAIL |

**The chooser picks D = ∞ in all four arms**: on IS Sharpe the budget is never worth having, so the
walk-forward never even reaches the device. The IS-matched twin is consequently *bit-identical*
(λ_IS = 1.0000 / 0.7500, ΔCAGR +0.00 pp, ΔSharpe +0.0000, ΔMaxDD +0.00 pp) — a self-consistency
check, not a result. **4a is 0/25 in every window on both panels** (B6).

## (F) BY-PRODUCT, reported and NOT proposed — the floor is reachable only by plain re-grossing

The free arm's pick is **the live book with the de-gross removed** (band 0.03, gross 1.00). On U56
it clears 4b on FULL and OOS (FULL 11.53% / 1.2009 / −15.91%, CAGR margin +0.93 pp; OOS +1.97 pp),
is **stable at 5 of 5 weekday offsets**, and clears idea 914's clause on both binding legs
(OOS DD +4.32 pp vs a 2.398 pp spread = 1.80×; CAGR +1.97 pp vs 0.578 pp = 3.41×). **It is still
not a KEEP candidate**, on three independent counts: it **fails 4b in the IS window** on U56
(CAGR −0.31 pp), it **fails 4b on B136 OOS** (CAGR −0.21 pp, and B136 FULL clears by +0.04 pp with
a 0.625 pp offset spread — ratio 0.07×, inside its own weekday noise by 914's clause), and the
cost ladder erodes it (U56 FULL 3/2/1/0 passes at 0/10/25/50 bps; B136 OOS 1/0/0/0). Idea 2119
reached the same cell from a different ladder this morning and killed it; this run reproduces that
on an independent family and adds the IS-window failure.

## What this run cannot do (stated, not repaired)

One band width (0.03, the live one — frozen, not a dial), one cadence (weekly), one response
*shape* (linear in the realised drawdown; a convex or hysteretic response is not priced), one
offset family (5 weekday phases; d=3 clips 2 weeks and d=4 clips 175, so the g_hi-1.00 spreads in
(F) are read on the full family and would narrow clip-free). The budgeted book's equity feeds back
into its own gross, so **cost rungs are not post-hoc subtractions here**: every rung in B7 is an
independent re-run (G5), which is why the record's usual cost-linearity gate is absent.

**SURVIVORSHIP (rule 9).** U56 and B136 are **current-constituent** lists, so every absolute CAGR
and drawdown level is optimistic and every 4b pass above is an upper bound. The (D) contrast is
within-tape — same names, same days, matched mean gross — which is the part the bias cannot
manufacture; the levels in (A), (B) and (F) are not repaired by it.

## Residue

1. **The clean statement the record can reuse:** *on the live band family the drawdown budget is a
   real instrument with the wrong price tag — it buys ~1.5× more drawdown per unit of exposure than
   a flat de-gross and pays ~1.6× more CAGR for it, and CAGR is the only leg that binds.* That
   sentence explains idea 852's KILL, idea 69's PARK and this one with a single number.
2. **The open leg this run does NOT close:** idea 69's trailing-1y SPY-vs-book budget has still
   never been scored against a matched-mean-gross twin. It is a different response shape and this
   run says nothing about it.
3. **A falsifier worth one run:** the ratio in (C) is fixed by the *shape* of the response. If any
   response shape can be found whose CAGR cost per pp of exposure is at or below the flat dial's
   −0.174, the device becomes live again. Nothing here says such a shape exists.
4. **No new KEEP, no PARK memo, no RULES change.**
