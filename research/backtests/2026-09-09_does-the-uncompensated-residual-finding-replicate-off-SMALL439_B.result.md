# Idea 305 — does-the-uncompensated-residual-finding-replicate-off-SMALL439 (lane B, 2026-09-09)

**Verdict: ANSWERED / KILL of the unqualified claim. H_REPLICATES FAILS, H_PANEL_SPECIFIC HOLDS.**
Idea 300's "the MA gate's extra timing residual is uncompensated" survives off SMALL439 only as a
**pooled sign**, not as the rung-by-rung fact it was published as. No KEEP: 4a 1/486, 4b 20/486,
BOTH 0/486, and the one 4a passer is a reproduction of a book idea 306 already published.

Script: `research/backtests/2026-09-09_does-the-uncompensated-residual-finding-replicate-off-SMALL439_B.py`
Outputs: `.grid.csv .decomp.csv .matched.csv .pairs.csv .bmatch.csv .walkforward.csv .console.txt`

## Design
Idea 300's matched experiment verbatim, with the panel loop added. Same ranking (dist = px/ma200 − 1)
for both arms; the constant-depth arm's x is set to the MA arm's OWN mean mask fraction at that theta
on that panel, so only the gate's **depth movement** differs. Gross 0.75, 10 bps, next-day, no
shorting/leverage; the 0-bps rung is derived exactly (r0 = r10 + turnover·bps/1e4).
Tuned dials (2): theta (9, idea 298/300's grid verbatim) × cadence (W/M/Q). Reported contrasts:
panel {U56, B136, SMALL439} × family {MA-THRESH, QUANTILE-M, QUANTILE-F} × construction
{RESPREAD, DEGROSS} = **486 books**, 81 decomposition cells × 3 windows.

## Reproduction gates (both PASS, read before anything else)
* **R1** — SMALL439 carried as the anchor reproduces idea 300's published headline on all nine
  quoted numbers to 4 dp: DEGROSS dSharpe **−0.0092**, OOS **−0.0256**, RESPREAD **+0.0476**,
  resid0 MA **−0.3817** / QUANTILE-M **−0.0124** pp/yr, attribution **−0.2917 = +1.2436 sel
  −1.1660 lev −0.3693 tim**.
* **R2** — every one of **162/162** (panel, theta, cadence ∈ W/M/Q, construction) cells matches
  idea 306's `pairs.csv` at gross 0.75 to **9.7e-17** on dSharpe (4.4e-16 on dCAGR).
* Identity r_dg,t = c_t·r_rs,t closes to 5.6e-17; the attribution identity closes to 2.7e-15 pp
  over 81 cells.

## The design fails its own matching gate off SMALL439 — and that is a finding
`ceil(x·n_t)` rounds the constant-depth arm **up** by up to 1/n_t of exposure per day: 0.23% at
n = 439 but **1.8% at n = 56**. Worst |Δ mask fraction| is 0.00166 on SMALL439 and **0.01396 on
U56** (bar 0.01); worst |Δ realised c_bar| 0.00643 vs **0.03469** (bar 0.02). The mismatch is
signed **in favour of the constant-depth arm** and correlates **−0.687 (U56) / −0.736 (B136)**
with the measured dSharpe at c_bar ≥ 0.5 — i.e. it pushes the answer toward "MA loses".
So a **QUANTILE-F** arm was added (identical ranking, identical x, marginal name carries the
fractional weight x·n_t − floor(x·n_t)): mask-fraction error falls to 0.00225 (U56) / 0.00103
(B136), and every conclusion below is quoted on both arms. **The verdict is unchanged**, so the
rounding was not driving it — but any future run of this design on a thin panel must use the
fractional form.

## The queue's exact test: does dSharpe stay ≤ 0 at c_bar ≥ 0.5?

| panel | n | dSharpe (full) | positive | OOS dSharpe | rungs > 0 | verdict |
|---|---|---|---|---|---|---|
| U56 | 15 | **−0.0059** | 8/15 | **+0.0039** | 2/5 | clauses 2, 3 FAIL |
| B136 | 15 | **−0.0087** | 10/15 | −0.0182 | 2/5 | clause 3 FAILS |
| SMALL439 (anchor) | 15 | **−0.0338** | 2/15 | **−0.0605** | 0/5 | all PASS |

Exactly-matched restatement (QUANTILE-F): U56 −0.0078 full / +0.0039 OOS, B136 −0.0090 / −0.0182 —
same clause pattern, so **H_REPLICATES FAILS on the exact arm too**.

Rung by rung (mean over cadences), the two shallow rungs **reverse sign** off SMALL439:
θ −0.40 → U56 **+0.0063**, B136 **+0.0028**, SMALL439 −0.0212; θ −0.25 → **+0.0223 / +0.0088 /
−0.0451**. On SMALL439 idea 300's band was −0.012..−0.047 at every one of these rungs. Off it,
the effect is a coin flip whose mean is a fifth the size.

## What DOES replicate — the residual itself, not its price
The timing residual is the most panel-stable object in the run: MA-THRESH resid0 **−0.3375 (U56)
/ −0.4231 (B136) / −0.3817 (SMALL439)** pp/yr — a spread of 0.086 pp/yr across panels that differ
8× in width and 100× in market cap, and all three inside idea 298's [−0.70, −0.20] band. The
constant-depth control is zero everywhere: **−0.0310 / −0.0321 / −0.0124** (QUANTILE-F: −0.0300 /
−0.0328 / −0.0122). So *what* the MA form costs replicates; *whether Sharpe notices* does not.

## The mechanism differs by panel (exact attribution, 0 bps, DEGROSS, pp/yr)

| panel | dCAGR0 | SELECTION | LEVEL | TIMING |
|---|---|---|---|---|
| U56 | −0.8503 | **−0.5779** | +0.0340 | −0.3064 |
| B136 | −0.8390 | **−0.4058** | −0.0422 | −0.3910 |
| SMALL439 | −0.2917 | **+1.2436** | −1.1660 | −0.3693 |

On SMALL439 the MA threshold's deeper slice is a genuinely *better* slice (+1.24 pp/yr) that
de-grossing gives back; on U56/B136 the same slice is a *worse* slice (−0.58 / −0.41) — the
DEGROSS reading of idea 306's already-published RESPREAD sign reversal (here: RESPREAD dSharpe
+0.0476 SMALL439 vs −0.0617 U56 / −0.0444 B136). Pooled over all 27 cells the MA form is far worse
off SMALL439 (**−0.1231 U56 / −0.1164 B136** vs −0.0092), but that whole gap lives at θ ≥ +0.06
(c_bar ≤ 0.47), where MA runs −0.17..−0.45 on the large-cap panels and **positive** (+0.02..+0.04)
on SMALL439. The panel ordering therefore **reverses with strictness**, which is why a single
pooled mean cannot be quoted for this pair without its c_bar rung.

## Rule 8 walk-forward (IS ≤ 2016-12-31 chooses; 2017-01-01..2026 read once)
* **WF-A** — no arm's IS pick beats RULES v2 OOS on any panel (best U56 pick 1.0736 vs live
  1.2817; best B136 1.1384 vs 1.2851). MA/DEGROSS is the worst pick on both target panels
  (U56 0.5677, B136 1.1384) against its constant-depth twin (1.0736 / 1.0070).
* **WF-B** — family choice is barely learnable: IS prefers MA in 6/27 (U56), 11/27 (B136),
  15/27 (SMALL439); IS→OOS sign agreement 0.70 / 0.59 / 0.59. Always-QUANTILE-M beats always-MA
  OOS on all three (1.1208 vs 1.0174; 1.0804 vs 0.9822; 0.6268 vs 0.6011).
* **WF-C** — **idea 300's OOS KILL of idea 298's constant-residual discount does not generalise.**
  On SMALL439 the IS constant is useless (IS −0.0201 → OOS −0.5918; MAE 0.5789 vs zero's 0.5975).
  On U56 it walks forward cleanly (IS −0.3162 → OOS −0.3377; MAE **0.2348** vs zero's 0.3382) and
  on B136 it drifts but still beats zero (IS −0.2864 → OOS −0.5287; 0.3562 vs 0.5352). The
  constant-depth arm's ZERO walks forward on all three (OOS MAE 0.021–0.036).

## KEEP paths — nothing new
4a **1/486**, 4b **20/486**, BOTH **0/486** (by panel: U56 1 / 18, B136 0 / 2, SMALL439 0 / 0).
The single 4a passer — U56 QUANTILE-M/DEGROSS θ +0.06, monthly, 7.02%/1.2364/−9.20%, halves
1.3010/1.1905 — is the **constant-depth twin, not the MA form**, is the *same cell* idea 306
already published as its 4a passer, and its OOS Sharpe (1.2603) is below live RULES v2's (1.2817)
while it fails 4b on CAGR. Recorded as a reproduction, **not** a new KEEP-candidate; no RULES
wording proposed. The 4b list is idea 298/306's known U56-heavy footprint restated (18 of 20 on
U56), and 12 of the 20 are constant-depth books.

## Honest limits
* Two dials only (theta × cadence); x is a deterministic function of theta; QUANTILE-F is a
  matching repair, not a dial, and nothing is selected on it.
* B136 and SMALL439 are current constituents (no delistings): every CAGR **level** and the whole
  4a/4b column is optimistic. The arm-minus-arm contrasts share names, ranking and days, so the
  bias very largely cancels there.
* n = 15 cells per panel at c_bar ≥ 0.5, drawn from 9 correlated thetas × 3 correlated cadences —
  the ±0.006..0.009 means quoted above are not distinguishable from zero at this resolution, which
  is exactly the claim: off SMALL439 this effect is **not resolvable**, not "confirmed smaller".
* Even QUANTILE-F leaves |Δ c_bar| up to 0.0237 on U56 — that residue is rebalance **drift**, not
  rounding, and is irreducible without a daily-rebalanced arm (out of scope at 2 dials).
* Follow-ups filed as 555–557.
