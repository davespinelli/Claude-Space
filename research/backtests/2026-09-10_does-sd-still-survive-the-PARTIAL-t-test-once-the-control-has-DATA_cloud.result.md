# Idea 485 (cloud, 2026-09-10) — does `sd` still survive the PARTIAL t-test once the control has DATA?

**Verdict: ANSWERED and SPLIT. KILL for capital.** The queue's hypothesis is **CONFIRMED on effect
size and REFUTED on the published verdict**, and the reason is that idea 83's pre-registered bar
pairs an *effect-size* leg with a *significance* leg that move in **opposite directions in N**. On
B136, `kill` falls **0.675 → 0.171** (a factor of 3.94) as the control gains power and crosses idea
252's own 1/3 threshold between D=100 and D=150 — while |t| **rises monotonically +6.19 → +9.62**,
because t scales with √N. So idea 252's sentence "sd survives" is literally unchanged at every
B136 draw count (0 of 7), and it is preserved **entirely by the leg that is an N statistic**. On
SMALL484 the full bar does fire: sd is **KILLED** from D=300 at λ=2 and from D=100 at λ*.
No RULES change, no book promoted, no KEEP claimed, no PROTOCOL edit; RULES.md, PROTOCOL.md,
scan.py, bot.py and baseline.py untouched.

Script `2026-09-10_does-sd-still-survive-the-PARTIAL-t-test-once-the-control-has-DATA_cloud.py`
(deterministic, standalone, no network, 564s); console `.console.txt`; CSVs `.power.csv` (84),
`.regressions.csv` (4,032), `.ladder.csv` (14), `.grid.csv` (120), `.walkforward.csv` (20),
`.keeppaths.csv` (120).

---

## GATES (pre-registered, run before any new number was read)

| | |
|---|---|
| G1 | `fast_backtest` == `engine.backtest` at 10 bps on a drawn book: max\|d\| **1.388e-17** |
| G2 | cost-rung identity `r(25) = r(0) − turn·25/1e4`: max\|d\| **1.388e-17** |
| G3 | **MEMBERSHIP** — the regenerated name sets reproduce idea 484's committed `sd`, `sd_IS`, `n_elig`, `n_elig_IS` on **all 3,000 rows × 4 columns** at max\|d\| **7.105e-15** (0.0000 in every one of the 6 (panel, k) cells). The design matrix is provably idea 484's own, not a re-draw. |
| G4 | **IDEA 252's OWN NUMBER** at D=50 (its 150 pooled B136 rows), n=20, CAND Sharpe — all 9 published values reproduced: R²(sd) 0.3062 (\|d\| 3.5e-05), t(sd) +8.08 (2.6e-03), OOF λ=2 pR² 0.2067 (4.5e-05), t +6.19 (2.9e-04), kill 0.675 (1.2e-04), IS λ=0.5 kill 0.000 (2.3e-04) and t −0.10 (1.2e-03), idea 83's scalar kill_W 0.620 (9.5e-06) and t_W +5.87 (4.2e-04) |
| G5 | the D ladder is **NESTED**: the first 50 name sets at D=500 are byte-identical to the D=50 sets, in every (panel, k) cell |

Because G3 and G4 both pass, every number below is idea 252's test, on idea 484's rows, with the
draw count as the only thing that moved.

---

## (1) THE POWER AUDIT — the control did not have data, and now it does

B136, pooled cell, out of fold (`.power.csv` carries all 84 points):

| D | N | R²(target) at λ=2 | R²(`sd` ~ M) at λ=2 | edf |
|---|---|---|---|---|
| 50 | 150 | +0.2100 | **+0.2680** | 109.9 |
| 100 | 300 | +0.5139 | +0.6440 | 130.0 |
| 200 | 600 | +0.6611 | +0.7548 | 135.0 |
| 500 | 1500 | **+0.7213** | **+0.7959** | 137.0 |

Idea 252's own power audit reported out-of-fold R²(sd ~ M) of **−0.04 … +0.41** at D=50 and
concluded "out of fold the same model genuinely carries only −0.04 to +0.41 of `sd`". At D=500 it
carries **0.796**. The control that idea 252 tested against genuinely did not span `sd`; the
control at D=500 very nearly does.

## (2) THE TEST — the ladder, idea 252's headline cell, out of fold at λ=2

n=20, CAND Sharpe, pooled over the three k cells — idea 252's own cell, at every D:

| panel | D | N | R²(sd) | t(sd) | R²(F) | pR²(sd\|F) | **t(sd\|F)** | **kill** | kill_W (scalar) | KILLED? |
|---|---|---|---|---|---|---|---|---|---|---|
| B136 | 50 | 150 | 0.3062 | +8.08 | 0.2100 | 0.2067 | **+6.19** | **0.675** | 0.620 | no |
| B136 | 100 | 300 | 0.3187 | +11.81 | 0.5139 | 0.1195 | +6.35 | **0.375** | 0.612 | no |
| B136 | 150 | 450 | 0.3116 | +14.24 | 0.6040 | 0.0999 | +7.04 | **0.320** | 0.551 | no |
| B136 | 200 | 600 | 0.3260 | +17.01 | 0.6611 | 0.0832 | +7.36 | **0.255** | 0.581 | no |
| B136 | 300 | 900 | 0.3377 | +21.40 | 0.7021 | 0.0672 | +8.04 | **0.199** | 0.566 | no |
| B136 | 400 | 1200 | 0.3517 | +25.49 | 0.7184 | 0.0648 | +9.11 | **0.184** | 0.584 | no |
| B136 | 500 | 1500 | 0.3401 | +27.78 | 0.7213 | 0.0583 | **+9.62** | **0.171** | 0.581 | no |
| SMALL484 | 50 | 150 | 0.0032 | +0.69 | 0.1469 | 0.0043 | +0.80 | 1.337 | 5.818 | no |
| SMALL484 | 300 | 900 | 0.0050 | +2.12 | 0.5752 | 0.0010 | +0.96 | **0.205** | 1.749 | **YES** |
| SMALL484 | 400 | 1200 | 0.0053 | +2.53 | 0.6704 | 0.0010 | +1.12 | **0.197** | 1.734 | **YES** |
| SMALL484 | 500 | 1500 | 0.0049 | +2.72 | 0.7035 | 0.0009 | +1.19 | **0.192** | 1.823 | **YES** |

Three things are in that table.

**(a) The queue is right about the effect size.** `kill` — the share of `sd`'s univariate R² that
survives the control — collapses from 0.675 to 0.171 on B136. The name-additive control absorbs
**32.5% of `sd` at D=50 and 82.9% at D=500**. Idea 252's headline number is a **D=50 statement**,
exactly as idea 484 found for the fit comparison, and it crosses idea 252's own 1/3 bar by D=150.

**(b) The published verdict nevertheless survives, and only because of the t leg.** idea 83's bar
is a conjunction: KILLED iff kill < 1/3 **AND** |t| < 2. The kill leg is met from D=150 onward;
the t leg is missed by a wider margin at every step, because t(sd|F) grows with √N even as the
effect shrinks (+6.19 at N=150, +9.62 at N=1500). **A bar built from an effect size and a
significance test cannot be read as one number when N is the thing being varied**, and the
record's sentence "idea 83's 62% is STRUCTURAL, not a power result" is only true of the *scalar*.

**(c) idea 83's ONE-SCALAR control is flat, and that is the cleanest evidence.** `kill_W` on B136
reads 0.620 / 0.612 / 0.551 / 0.581 / 0.566 / 0.584 / 0.581 across the same seven D — a
1-parameter control is at its asymptote by N=150, so its kill does not move. The 136-column
control's kill moves by 3.94x on the identical rows. **The difference between the two controls'
kills is therefore a power difference, not a structural one, and idea 252 read it the other way.**

Whole-grid, out-of-fold scheme, book-Sharpe targets (CAND + EWall Sharpe, both n, all 4 scopes,
all 6 penalties = 96 points per cell; `.regressions.csv` has all 4,032):

| panel | D | survives \|t\|>2 | kill median [min, max] | **KILLED by the full bar** |
|---|---|---|---|---|
| B136 | 50 | 92 / 96 | 0.851 [0.563, 1.094] | **0 / 96** |
| B136 | 150 | 96 / 96 | 0.390 [0.177, 0.850] | 0 / 96 |
| B136 | 300 | 89 / 96 | 0.167 [0.026, 0.531] | 7 / 96 |
| B136 | 500 | **78 / 96** | **0.092** [0.008, 0.396] | **18 / 96** |
| SMALL484 | 50 | 2 / 96 | 1.001 | 10 / 96 |
| SMALL484 | 500 | 4 / 96 | 0.291 | **52 / 96** |

B136's kill median falls **9.2x** (0.851 → 0.092) and the full bar fires 18 times where it never
fired at idea 252's N. **On SMALL484 `sd` has essentially no univariate R² to begin with**
(0.0032–0.0122, t +0.69 to +2.72) and the bar kills it in 52 of 96 points at D=500 — so the
record's dispersion result is a **B136 fact**, not a panel-general one. On the PREMIUM target the
bar fires **9/48 → 40/48** on B136 between D=50 and D=500.

## (3) LIVE LEG — the surviving coefficient made a chooser, rule 8, 10 and 25 bps

If the part of `sd` orthogonal to name composition is informative, then choosing a sub-panel on
`sd_perp = resid(sd_IS | F_oof)` should beat choosing on raw `sd`. Every selector input is
computed on 2009–2016 only; 2017-01-01.. is read once. Median over the six (k, n) cells:

| panel | cost | S0 do-nothing | S1 IS Sharpe | S2 IS sd | **S3 IS sd_perp** | S4 pred M+sd | RULES v2 | SPY |
|---|---|---|---|---|---|---|---|---|
| B136 | 10 | 0.8529 | 1.0456 | 0.9361 | **0.8876** | 1.0547 | **1.1185** | 0.8820 |
| B136 | 25 | 0.7004 | 0.9149 | 0.7970 | **0.7597** | 0.9233 | — | 0.8820 |
| SMALL484 | 10 | 0.4324 | 0.3049 | 0.0284 | **0.1000** | 0.5359 | **0.6629** | 0.8820 |
| SMALL484 | 25 | 0.2414 | 0.1808 | −0.0981 | **−0.0459** | 0.4127 | — | 0.8820 |

(OOS Sharpe; OOS CAGR and MaxDD for every one of the 120 books are in `.grid.csv`.)

**S3 is WORSE than S2 at every (panel, cost) point** — 0.8876 vs 0.9361 and 0.7597 vs 0.7970 on
B136; 0.1000 vs 0.0284 and −0.0459 vs −0.0981 on SMALL484 is the one place it helps, and both
numbers are ~0. Residualising `sd` on name composition, which is exactly what "the partial
coefficient is real and usable" would license, **does not improve the chooser and mostly degrades
it**; the residualisation changes the pick in only 4 of 12 cells, and in the B136 k=40/n=20 cell
S2 and S3 select the identical draw (224) and are therefore the same book. **No selector's median
beats the live book's OOS Sharpe on either panel** (best is S4 at 1.0547 against RULES v2's
1.1185), and per-cell only 2 of 6 (S1, S2) beat it on B136 at 10 bps.

## KEEP paths — nothing to promote

120 books (2 panels × 3 k × 2 n × 5 selectors × 2 rungs), both paths on every one.

* **4a: 0 / 120 — 4b: 10 / 120 — BOTH: 0 / 120.** B136 4b 10/60; SMALL484 4b **0/60**.
* 4a is 0 everywhere because RULES v2 on B136 draws down only −12.24% against the picks' −17.6%
  to −19.6%.
* All 10 4b passers are individual B136 draws (k=20 n=5 draw 253; k=40 n=20 draws 337/224/214),
  and idea 486 already showed that **~25% of random 20-name B136 lists clear 4b on their own**. So
  the passers are a property of the draw generator, not of a rule — and this run's own result is
  that the statistic used to pick them carries no usable orthogonal information. **No memo and no
  RULES wording is proposed.**

## WHAT SHOULD CHANGE

1. **Idea 252's headline needs its N, and its bar needs splitting.** "The name-level control
   leaves kill 0.675 at t +6.19" is a D=50 fact; at D=500 it is kill 0.171 at t +9.62 on the same
   rows. A bar of the form `effect < c AND |t| < 2` should never be quoted as a single verdict
   across changing N, because its two legs are monotone in opposite directions. **Report kill and
   |t| separately with N beside them.**
2. **Retract the "62% is STRUCTURAL, not a power result" reading.** It is structural for idea 83's
   one-scalar control (kill_W flat at 0.55–0.62 over a 10x range of N) and a pure power number for
   the 136-column one (kill 0.675 → 0.171 over the same range).
3. **Dispersion claims on the small panel should be dropped, not restated.** `sd`'s univariate R²
   there is 0.003–0.012 and the full kill bar fires in 52 of 96 points at D=500.
4. **Nothing here is capital-relevant.** 0 of 120 books clear both KEEP paths, no selector beats
   the live book, and the one selector this idea exists to test (S3) is the second-worst of the four.

## SURVIVORSHIP AND LIMITATIONS (stated, not hidden)

* **`sd` and the book metrics at 10 bps are READ from idea 484's committed `.grid.csv.gz`**, not
  re-derived from prices for all 3,000 rows. What *is* re-derived from prices, for every one of
  those rows, is the name **membership** the design matrix is built from — G3, at 7.105e-15. A
  wrong membership would give a wrong design matrix and G3 would fail.
* **SURVIVORSHIP:** B136 and the small panel are CURRENT-constituent lists
  (research/universe_broad.json, data/SMALL_PANEL_README.md), so their **levels** are biased upward;
  only within-panel contrasts (draw vs draw, D vs D on the same rows, model vs model) are
  load-bearing. **SMALL484 is idea 484's panel and still contains the 44 names with
  `max_1d_move >= 1.0` that this lane normally drops** — it is used because the queue names idea
  484's grid and the grid is SMALL484. SMALL439 is built and its reference rows printed (SPY
  14.13% / 0.862 / −33.72%, identical to SMALL484's because SPY is the benchmark either way), but
  the live leg was not re-run on it: 3,000 filtered book builds do not fit one run's budget, and
  idea 487 (same day, same generator, same seeds) priced SMALL439 selector books directly.
* The small panel starts 2011-01-13 after warm-up, so its IS window is shorter than B136's
  (2009-01-13), which is one reason its `sd` has less to work with.
* Costs 10 and 25 bps per unit turnover; weights decided at close *t*, applied at *t+1*; weekly
  cadence; gross 0.75; no shorting, no leverage.
