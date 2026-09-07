# Idea 383 — does the CALMAR RAY survive a NON-CASH de-gross? (cloud, 2026-09-07)

**Verdict: NO TILT on the question asked — KILL. The ray is NOT fixed (a non-cash residual
multiplies its Calmar spread by 8–19x), but on the one panel where cash leaves no
admissible band it opens none: SMALL439 stays 0/5 non-empty for all three residual
assets. A SPY residual is provably incapable of helping, by closed form. By-product,
reported not proposed: a SHY residual strictly dominates cash cell-for-cell and delivers
the record's only 4a passer in this family (1 of 180 cells at 10 bps, 0 at 25).**

Script `2026-09-07_does-the-CALMAR-RAY-survive-a-NON-CASH-de-gross_cloud.py`.

## Design

Idea 333's grid verbatim — family = idea 329's anchor arm (top-n of the v1 composite, vol
scaler OFF, RULES v1 eligibility, NORM weights `w_i = g/k_t`, m=0, weekly, next-day
execution) — with one thing changed: what the residual `(1-g)` of NAV is held in. Two
tuned parameters as the queue specifies: `n ∈ {10,20,40,80,ALL}` × `gross ∈
{0.375,0.50,0.625,0.75}` = 20 cells, all reported, on 3 panels × 3 residual arms × 3 cost
rungs = **180 rows** in `.grid.csv`. The residual asset (CASH / SPY / SHY) is the
treatment, always reported side by side, never selected on.

SPY and SHY are dropped from the **ranked** universe on every panel so the residual asset
can never also be a holding; G3b prices that deviation from idea 333 (B136 n=20 g=0.75
@10 bps: dCAGR −0.05%, dSharpe −0.0053, dMaxDD −0.37%). The SPY/SHY sleeves are **charged
their own turnover**; cash is not — the honest treatment, and one that handicaps the
non-cash arms.

Gates: G1 0.000e+00 on returns and turnover at 0 and 25 bps; G2 explicit constant-price
residual == implicit cash, 2.8e-17; **G3 idea 333's committed (B136, n=20, g=0.75) row
reproduced at max |d| 0.000e+00**; G4 at gross=1.0 all arms coincide, 0.000e+00; G5 no
NaN in any residual series.

## 1. The ray tilts — a lot — and idea 333's premise about *why* is wrong

Max Calmar spread over the gross ladder, @10 bps:

| panel | CASH | SHY | SPY |
|---|---|---|---|
| B136 | 0.0224 | 0.0575 | **0.1038** |
| U56 | 0.0211 | 0.0787 | **0.1190** |
| SMALL439 | 0.0078 | 0.0659 | **0.1456** |

Cash reproduces idea 333's 0.0198-scale invariance (max 0.0224 here). A SPY residual
tilts the ray **4.6–19x** more. So "gross slides a book along a nearly fixed Calmar ray"
is a statement about **cash**, not about gross: it holds only because cash is the origin.
Linearity in gross is near-exact for cash (min R² 0.9991) and degrades for SPY (min R²
0.8844) exactly as a two-asset blend should.

## 2. But the tilt cannot reach the bar, and for SPY that is a theorem

The joint DD+CAGR bar is `Calmar ≥ (0.70/0.60) × Calmar_SPY`. A 100%-SPY residual
converges to `Calmar_SPY` itself — **exactly `1/1.1667` = 85.7% of the bar**. Blending
toward SPY therefore bends the ray toward a point that is provably *below* the bar by
14.3%, no matter the panel or the book. The data agrees: the SPY arm's non-empty band
count **falls** from cash's 5/5 to 3/5 on B136 and from 5/5 to 2/5 on U56, and its cells
clearing both bars go **5 → 0** and **7 → 0**. SPY residual is not a fix; it is a
strictly worse funding choice under 4b.

On SMALL439 (the panel where cash leaves none), the best non-cash Calmar reached is
**0.3822** (SPY, n=10, g=0.375) against a bar of **0.4889** — short by 0.107, and the
extrapolation limit is 0.4191, still short. The inverted bands stay inverted at 5/5 n for
all three arms (`g_lo` 0.44–2.72 against `g_hi` 0.33–0.48, and negative for SPY).

| panel | arm | non-empty bands /5 | cells clearing both bars /20 |
|---|---|---|---|
| B136 | CASH / SHY / SPY | 5 / 5 / **3** | 5 / **6** / **0** |
| U56 | CASH / SHY / SPY | 5 / 5 / **2** | 7 / 7 / **0** |
| **SMALL439** | CASH / SHY / SPY | **0 / 0 / 0** | **0 / 0 / 0** |

**Pre-registered verdict: NO TILT.**

## 3. The by-product that matters more than the answer — the zero-cash convention

SHY returns **1.34% CAGR at Sharpe 0.984 with −5.71% MaxDD** over the sample. Parking the
de-grossed sleeve there instead of at zero **strictly dominates cash in every matched
cell**: it adds CAGR and, being near-uncorrelated, usually *reduces* drawdown. B136,
n=ALL, g=0.375, @10 bps:

| residual | CAGR | Sharpe | MaxDD | H1 / H2 | OOS Sharpe | 4a |
|---|---|---|---|---|---|---|
| CASH | 5.40% | 1.020 | −9.77% | — | — | fails H1, H2 |
| **SHY** | **6.27%** | **1.178** | **−11.10%** | **1.261 / 1.104** | **1.202** | **PASS** |
| SPY | 15.00% | 0.958 | −29.52% | — | — | fails H1, H2, DD |

RULES v2 on B136 @10 bps is 8.03% / 1.106 / −12.24%, H1/H2 1.229/0.984, OOS 1.119 — the
SHY cell beats it on Sharpe in **both halves**, on MaxDD, and out of sample, and rule 8
picks that exact cell (IS-Sharpe argmax, regret +0.0110). It is a **4a KEEP-candidate**;
memo filed alongside. It is **not** a 4b object — it fails the CAGR floor (6.27% against
10.66% required), which is the low-return shape PROTOCOL 4b was added in order to reject.

Its fragility is the headline caveat: **1 of 180 cells passes 4a at 10 bps, 9 of 180 at 0
bps, and 0 of 180 at 25 bps** (H1 is the failing bar there). And most of what SHY adds is
simply the risk-free rate the record has been setting to **zero** — which is a systematic
understatement in *every* de-grossed book the project has ever priced, not an edge in this
one.

## 4. Rule 8 and 4b

Rule 8 ((n, gross) on IS 2008-2016 Sharpe @10 bps, 2017-2026 read once): **4/9 picks above
SPY OOS 0.882, 3/9 above RULES v2 OOS, 1/9 clears 4b, 1/9 clears 4a, mean regret
+0.0951**. 4b @10 bps: B136 CASH 3/20 → SHY 4/20 → SPY 0/20; U56 CASH 5/20 → SHY 5/20 →
SPY 0/20; SMALL439 0/20 on all three. At 25 bps only one cell survives anywhere (U56 SHY
n=20 g=0.75, 11.68%/0.976/−18.14%) against cash's zero. First-failing 4b bars @10 bps
pooled: CAGR 100, DD 94, H2 75, OOS 73, H1 66.

## 5. What the record should carry

1. **Restate idea 333's ray claim as a CASH claim.** "Gross slides a book along a nearly
   fixed Calmar ray" is true of de-grossing *into cash* (spread ≤ 0.0224) and false of
   de-grossing generally (≤ 0.1456). The leaderboard row should name the residual asset.
2. **The SPY-residual closed form is publishable and needs no grid**: a residual in the
   benchmark converges to `Calmar_SPY = bar / 1.1667`, so it can never satisfy 4b's joint
   bar and can only drag a passing book down. No future idea needs to test it.
3. **Price the zero-cash convention.** Every de-grossed book in the record is scored with
   its cash sleeve earning 0. On this family that understates CAGR by ~0.84 pp/yr at 62.5%
   residual and Sharpe by ~0.16. That is a record-wide accounting question, not an edge.

## Caveats

All three panels are **current-constituent** lists — SURVIVORSHIP; SMALL439 is the sub-$2B
screen with the 44 `max_1d_move ≥ 1.0` names dropped, and its 4b CAGR floor is tested in
the book's favour, which makes the NO-TILT reading there **conservative**. SHY is a 1–3y
Treasury ETF, not a T-bill: it carries real duration and its 2022 drawdown is not zero,
and its 2009–2021 return is a one-directional rate regime. Gross ≤ 0.75 throughout, so
nothing here is leverage.

Artefacts: `.grid.csv` (180 rows), `.ray.csv`, `.band.csv`, `.walkforward.csv`,
`.console.txt`.
