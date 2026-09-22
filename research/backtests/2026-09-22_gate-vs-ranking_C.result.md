# Idea 2094 (lane C, 2026-09-22) — RESULT: **ANSWERED / THE 2083 PASS IS THE GATE, NOT THE RANKING**

**Question.** Idea 2083 left a KEEP-4b candidate (U56, MADIST top-40, gross 1.00, monthly, t+1,
10 bps; OOS 16.24% / 1.3099 / −17.67%, a +2.56 pp margin over the −20.23% cap). Its own memo
warned the book is "top 40 of 56", so the pass might be the 200d-MA gate. Hold every dial and
replace ONLY the ranking with orderings carrying no return information.

**Setup.** U56, gate `close > 200dMA & vol20 < 0.60`, monthly month-end decision, fills t+1,
10 bps, gross 1.00 at `gross/k` per name (shortfall stays in CASH). Two tuned dials: RANKING
{MADIST, ALPHA (alphabetical), REVMADIST (deliberately reversed), RAND (per-month redraw, 5
seeds), RANDSTATIC (one permutation, 5 seeds)} × WIDTH k {20, 30, 40, 50, ALL}. 65 grid points,
all published in `.grid.csv`. Replication gates G1/G2 reproduce 2083's 1.3099 / −17.67% exactly.

## 1. The gate census is the whole story
At the 213 month-end decision closes, the gate admits a mean of **37.5 of 56 names** (median 41,
min 4, max 52). **43.2% of months admit fewer than 40 names**, so "top 40" IS "every gated name"
in nearly half the sample; at k = 50 that is **93.0%** of months. Mean holding overlap (Jaccard)
with the MADIST book of the same width: k=40 → ALPHA 0.889, RAND 0.894, REVMADIST 0.878;
k=50 → 0.998 for all; k=ALL → 1.000 (mechanical, gate G4).

## 2. Every information-free ranking clears 4b at 2083's width (V1 TRIGGERED)
| ranking (k=40) | OOS CAGR | OOS Sharpe | OOS MaxDD | OOS DD margin | 4b FULL+OOS |
|---|---|---|---|---|---|
| MADIST (2083) | 16.24% | 1.3099 | −17.67% | **+2.56 pp** | 1/1 seed |
| ALPHA | 15.92% | **1.3266** | −16.60% | **+3.63 pp** | 1/1 |
| RAND (mean of 5 seeds) | 14.98% | 1.2732 | −17.39% | +2.84 pp | **5/5** |
| RANDSTATIC (mean of 5) | 15.10% | 1.2758 | −16.84% | +3.39 pp | **5/5** |
| REVMADIST (wrong direction) | 13.23% | 1.1974 | −15.65% | **+4.58 pp** | 1/1 |
SPY OOS 15.29% / 0.8751 / −33.72%; live RULES v2 OOS Sharpe 1.2767; FULL SPY 15.14% / 0.8851 /
−33.72% (H1 0.9570 / H2 0.8264). All five rankings clear 4b at **8 of 8** cost {0,10,25,50} bps ×
lag {0,+1d} cells. **4a fails everywhere** (every FULL MaxDD is worse than v2's −12.05%).

## 3. The ranking does not earn the drawdown margin (V2 NOT triggered)
MADIST's +2.56 pp is the **SMALLEST** margin of the five at k=40; the info-free mean is +3.16 pp,
a **−0.61 pp** difference against a paired circular-block bootstrap SE of 0.78 pp. Every one of
the 12 paired OOS Sharpe differences has a 95% interval spanning zero (MADIST − ALPHA is
**−0.0166**, i.e. the alphabet wins); dMaxDD is negative (deeper) in all 12.

## 4. The direction does not matter either (V3 NOT triggered)
REVMADIST — rank by *worst* trend first — also clears 4b FULL+OOS at k=40, with a **larger** DD
margin (+4.58 pp) than MADIST. It gives up 3.01 pp of OOS CAGR, so the trend signal buys return,
but it buys **no part of the 4b verdict**.

## 5. What actually moves the verdict is the WIDTH / CASH BUFFER (V4 TRIGGERED)
4b pass rate by k: **20 → 0.00, 30 → 0.92, 40 → 1.00, 50 → 1.00, ALL → 0.00** (sd 0.535); by
ranking: 0.40–0.60 (sd 0.089). k=ALL re-spreads to full gross and FAILS (−1.95 pp); k=50 holds the
same names at a FIXED 1/50 denominator, leaving ~25% in cash, and passes with +4.75 pp at every
ranking (−15.48% MaxDD, identical to 4dp). The device is the **fixed denominator's cash buffer**
on top of the gate, not the ordering.

## 6. Rule 8 walk-forward (IS 2009–2016 chooses, 2017–2026 read once)
IS-Sharpe chooser over the 25 (ranking, k) cells picks **ALPHA k=30** → OOS 17.59% / 1.2996 /
−18.56%, DD margin +1.67 pp, **4b FULL+OOS PASS**. MADIST k=40 sits at IS-Sharpe rank **13 of 25**
— a legal chooser does not reach 2083's book at all, and the book it does reach uses no return
information. Full ladder in `.walkforward.csv`.

**Verdict: ANSWERED — KILL of the MADIST ranking as the earner of 2083's pass; the surviving
4b candidate is the gate + fixed-denominator cash buffer, reachable with an alphabetical sort.**
Survivorship (rule 9): U56 is a current-constituent list, so all LEVELS are optimistic; the
ranking contrast is same-panel/same-tape/same-width and first-order immune.
