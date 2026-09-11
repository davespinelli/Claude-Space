# Idea 703 — is-the-RATIO-to-OOS-slope-steeper-at-the-WIDE-end-for-a-reason
**lane C, 2026-09-11.** Script `2026-09-11_is-the-RATIO-to-OOS-slope-steeper-at-the-WIDE-end-for-a-reason_C.py`;
artefacts `.console.txt .books.csv .profile.csv .transplant.csv .buckets.csv .walkforward.csv
.keeppaths.csv`. Runtime 501.9 s, 48 panels, 240 book rows, 192 rank-bucket blocks.

## Verdict — **SPLIT, and it is mostly artefact**

The pre-registered bars disagree, which the docstring said would be reported as SPLIT rather
than rescued by a third statistic. Both are quoted:

| bar | value | reading |
|---|---|---|
| **BAR 1** (transplant shares) | NOISE **+87.3%**, EFFECT **+26.5%**, interaction −13.8% | **RANK-STATISTIC ARTEFACT** (bar: NOISE ≥ 0.60) |
| **BAR 2** (rank-free Sharpe span) | SPANRATIO **1.524** | **profile steepens** (bar: ≥ 1.50) — but by a hair, and see §3 |

**So: the ratio really does bite ~1.5× harder on a 400-name panel than on a 40-name one, but
that is not what the record's −0.3693 → −0.9415 shows. 87% of that rank move is the
between-draw spread collapsing as the panels stop being different panels.** At k = 400 an
8-draw ladder samples 400 of 439 names, so the draws overlap **91.2%**; at k = 40 they overlap
**9.5%**. Spearman is a signal-to-noise statistic, so it must sharpen. No KEEP, no memo.

## 0. Gates (all pre-registered, all PASS, printed before any new number was read)

* **G0** all **192** of idea 694's committed ARM B book rows reproduce at max |Δ| **9.714e-17**
  across CAGR/Sharpe/MaxDD/H1/H2/OOS_CAGR/OOS_Sharpe/OOS_MaxDD/IS_Sharpe (0 of 192 over 1e-9).
* **G0b** the six published within-k ρ(r, OOS Sharpe) re-measured from this run's own books:
  −0.3693 / −0.1393 / −0.3724 / −0.4632 / −0.8325 / −0.9415, worst |Δ| **4.86e-05**.
* **G1** 48 panels, exact width, no duplicate columns, all inside SMALL439.
* **G2** see §1.
* **G3** transplant diagonal RHO(k,k) equals the observed within-k ρ at **0.000e+00**.
* **G4** the reconstructed 0 bps series equals a fresh `cost_bps=0` backtest at **< 1e-15** (3 cells).
* **G5** this run's one-score-frame fast path gives weights identical to idea 286's
  `cand_weights(n)` at **0.0** (3 cells).

## 1. Two corrections to the queue's premise, before any decomposition

**(a) The sequence is NOT monotone.** The queue says the slope goes −0.3693 → −0.9415
"monotonically over k=40..400". **4 of 5 steps are downward; the k = 40 → 60 step is +0.2301,
i.e. UP, and retraces 40.2% of the whole span.** The word should be deleted from the record.
The dip is an *effect-side* fact, not a noise one: in the transplant matrix the row e = 60 is
the flattest row in **every** column (−0.1211 / −0.1393 / −0.2543 / −0.2482 / −0.5298 / −0.6327),
and k = 60 is the only width whose r-profile is non-monotone (A(0.25) = 0.3058 > A(0.10) =
0.2641, 2/3 steps). Wherever k = 60's own profile is used, the slope is flat; wherever its noise
is used, it is not.

**(b) "More cells to order" is FALSE BY CONSTRUCTION (GATE 2, tested by counting).** Every k
carries exactly 4 r-levels × 8 draws = **32 rows**, and n = max(2, round(r·k)) is **4 distinct
values at every k** — 40:[2,4,10,20], 60:[3,6,15,30], 80:[4,8,20,40], 100:[5,10,25,50],
200:[10,20,50,100], 400:[20,40,100,200]. k = 400 orders neither more cells nor more distinct
levels than k = 40. The artefact that *is* available to a rank statistic is **attenuation**, and
that is what §2 prices.

## 2. The decomposition — an exact, non-parametric transplant

Split the ARM B grid at each width into its r-profile and its draw residual,
`A_k(r) = mean_d S_k(r,d)`, `R_k(r,d) = S_k(r,d) − A_k(r)`, then read one width's profile at
another's noise: `RHO(e, m) = Spearman(r, A_e(r) + R_m(r,d))`. The diagonal is the observed ρ
exactly (GATE 3).

|  | m=40 | m=60 | m=80 | m=100 | m=200 | m=400 |
|---|---|---|---|---|---|---|
| **e=40** | **−0.3693** | −0.4268 | −0.4147 | −0.4178 | −0.8264 | −0.8688 |
| **e=60** | −0.1211 | **−0.1393** | −0.2543 | −0.2482 | −0.5298 | −0.6327 |
| **e=80** | −0.3209 | −0.3572 | **−0.3724** | −0.3784 | −0.7810 | −0.8718 |
| **e=100** | −0.4117 | −0.4601 | −0.4329 | **−0.4632** | −0.8325 | −0.8658 |
| **e=200** | −0.3996 | −0.4723 | −0.4571 | −0.4783 | **−0.8325** | −0.8507 |
| **e=400** | −0.5207 | −0.6024 | −0.5146 | −0.5510 | −0.9051 | **−0.9415** |

*Read the table by columns, not rows.* The **m = 400 column spans −0.63 to −0.94 whatever
profile is dropped into it**; the m = 40 column spans −0.12 to −0.52. Noise source moves the
statistic further than effect source does.

    total   RHO(400,400) − RHO(40,40) = −0.5721   (published −0.5722)
    EFFECT  RHO(400, 40) − RHO(40,40) = −0.1514    share  +26.5%
    NOISE   RHO( 40,400) − RHO(40,40) = −0.4995    share  +87.3%
    INTERACTION                       = +0.0787    share  −13.8%

The mechanism is measured, not assumed. Per width: **mean pairwise panel overlap 0.0946 /
0.1399 / 0.1768 / 0.2293 / 0.4477 / 0.9117** (= k/439 to three decimals), and the cross-draw sd
of OOS Sharpe falls **0.1998 → 0.0385 (5.2×)** while the Sharpe-unit span rises only
**0.1948 → 0.2969 (1.52×)**. SNR = span/sd goes **0.97 → 7.71 (7.9×)**; the draw-blocked ρ
(within-draw Spearman over the 4 r levels, averaged over draws — noise-free by construction)
goes **−0.6750 → −1.0000** and is **−1.0000 at k = 400 because every one of the 8 draws is
essentially the same panel**. At k = 400 the ladder has one panel measured eight times.

## 3. What the real 26% is made of — the queue's two named mechanisms

| k | A(r=.05) | A(r=.10) | A(r=.25) | A(r=.50) | span | span 0 bps | sd_draw | SNR | ρ_blocked |
|---|---|---|---|---|---|---|---|---|---|
| 40 | +0.3935 | +0.3625 | +0.2842 | +0.1987 | +0.1948 | +0.2113 | 0.1998 | 0.97 | −0.6750 |
| 60 | +0.3624 | +0.2641 | +0.3058 | +0.2304 | +0.1320 | +0.1542 | 0.1378 | 0.96 | −0.2250 |
| 80 | +0.4163 | +0.3639 | +0.3100 | +0.2354 | +0.1809 | +0.2063 | 0.2606 | 0.69 | −0.5250 |
| 100 | +0.4345 | +0.4201 | +0.3062 | +0.2248 | +0.2097 | +0.2360 | 0.1772 | 1.18 | −0.7000 |
| 200 | +0.4539 | +0.4408 | +0.3490 | +0.2310 | +0.2229 | +0.2579 | 0.0573 | 3.89 | −0.9250 |
| 400 | +0.5234 | +0.4400 | +0.3467 | +0.2266 | **+0.2969** | +0.3383 | 0.0385 | 7.71 | −1.0000 |

**(ii) THE COST OF HOLDING MORE NAMES IS NOT THE MECHANISM — IT WORKS THE OTHER WAY.** Costs
are recovered exactly from the turnover identity (GATE 4), so the whole profile is re-read at
0 bps. The span growth k = 40 → 400 is **+0.1021 at 10 bps and +0.1270 at 0 bps: COSTSHARE
−24.4%.** Deleting costs makes the sharpening **bigger**. The reason is in the per-r drag,
which is *monotone decreasing in r at every width* (k=400: −0.1219 / −0.1168 / −0.0981 /
−0.0805 of Sharpe at r = .05/.10/.25/.50): a CAND-20 book on a 400-name panel turns its whole
NAV over far more often than a CAND-200 one, so **holding more names is CHEAPER, not dearer**,
and costs *compress* the r-profile rather than steepening it. The queue's channel (ii) is
**refuted with its sign**.

**(i) THE DISPERSION OF THE SCORE'S TOP TAIL IS THE MECHANISM, and it is the right size.**
Cost-free, book-free rank-bucket ladder (B1 = ranks 1..n(.05), B2 = (n05,n10], B3 = (n10,n25],
B4 = (n25,n50], each held EW between weekly rebalances), OOS Sharpe:

| k | B1 | B2 | B3 | B4 | TAIL = B1−B4 |
|---|---|---|---|---|---|
| 40 | +0.4848 | +0.2489 | +0.0931 | +0.0748 | +0.4100 |
| 60 | +0.4519 | +0.1188 | +0.2155 | +0.1152 | +0.3367 |
| 80 | +0.5232 | +0.2632 | +0.1993 | +0.0589 | +0.4643 |
| 100 | +0.5649 | +0.3744 | +0.1160 | +0.0612 | +0.5037 |
| 200 | +0.5675 | +0.4101 | +0.2048 | +0.0867 | +0.4808 |
| 400 | **+0.6447** | +0.3923 | +0.1491 | +0.0597 | **+0.5850** |

**TAIL(400)/TAIL(40) = 1.427, ρ(k, TAIL) = +0.8857** — against a SPANRATIO of **1.524**. The
cost-free top-tail measure reproduces the surviving steepening to within 7%, on a construction
that shares no book convention, no gross and no cost rung with the CAND ladder. **The real
quarter of the effect is a top-tail dispersion story and nothing else.** Note where it lives:
it is almost entirely B1 rising (+0.4848 → +0.6447) — the *top* of a deeper pool gets better —
while B4 is flat near zero at every width (+0.0748 → +0.0597). Depth does not make the tail
worse; it makes the head better.

**(iii) FILL / CAPACITY is INERT, as pre-declared.** n/Ebar at fixed r is constant to three
decimals across a 10× width change (r = .50: 1.539 / 1.565 / 1.528 / 1.512 / 1.544 / 1.555;
breadth 0.3272…0.3216, ρ(k, breadth) = −0.1356). Every scale-free quantity is fixed by
construction when r is fixed, so the record's fill channel cannot produce this sharpening.
Reported because it was pre-registered, not because it moved.

## 4. Rule 8 walk-forward (r chosen on 2009–2016 IS Sharpe, 2017– read once, 8 draws × 6 widths)

| selector | scope | cells | OOS Sharpe | OOS CAGR | OOS MaxDD | beats v2 | beats SPY |
|---|---|---|---|---|---|---|---|
| PICK-r | per k, pooled | 48 | +0.2802 | +3.10% | −27.50% | 4/48 | **0/48** |
| R-MIN (r=.05) | per k, pooled | 48 | +0.4307 | +7.41% | −40.51% | 16/48 | **1/48** |
| R-MAX (r=.50) | per k, pooled | 48 | +0.2245 | +1.71% | −22.16% | 0/48 | **0/48** |
| PICK-(k,r) | whole grid | 8 | +0.2821 | +3.34% | −34.10% | 0/8 | **0/8** |
| **SPY** | — | — | **+0.8820** | **+15.45%** | **−33.72%** | — | — |
| **RULES v2** (per panel, mean) | — | — | +0.5314 | +3.77% | −15.44% | — | — |

**Choosing r on IS is worth −0.1505 of OOS Sharpe against simply taking r = 0.05, and it is
better in 3 of 48 cells.** The IS picker takes r = 0.50 at five of the six widths (r = 0.10 at
k = 40) — the *worst* end of the very ladder this idea is about, at every width where the
published slope is steepest. At k = 400 PICK-r and R-MAX are the same book in all 8 draws.
Best arm anywhere on the grid: R-MIN at k = 400, OOS **+7.88% / 0.5234 / −26.96%** against SPY
**+15.45% / 0.8820 / −33.72%**. Nothing here is a capital candidate.

## 5. KEEP paths (PROTOCOL rule 4, 10 bps, all 240 book rows)

**4a 0/240. 4b 0/240** — 0/40 at every one of the six widths. No KEEP, no memo, no RULES
change; `RULES.md`, `PROTOCOL.md`, `scan.py`, `bot.py` and `baseline.py` untouched.

## 6. For the record

1. Delete "monotonically" from idea 703's description of idea 694's ρ ladder: 4 of 5 steps, and
   the first step goes the wrong way by 40.2% of the span.
2. **Any within-k rank correlation quoted across a k ladder drawn from a fixed pool must state
   its draw overlap k/|pool| beside it.** At k/|pool| ≥ 0.9 the draws are one panel and the
   rank statistic is guaranteed to sharpen; 87.3% of this record's published sharpening is that.
   Proposed for Sunday review (rule 6), **not applied here**.
3. Quote the rank-free span beside any ρ ladder: here it moves 1.52× where ρ moves 2.55×.
4. Idea 694's channel list needs a sign correction: at fixed panel, **cost falls with n**, so
   "the cost of holding more names" compresses a ratio profile rather than steepening it.

**SURVIVORSHIP** (idea 54, `data/SMALL_PANEL_README.md`): SMALL439 is the current constituents
of its screen and this ladder is entirely small-cap, so every LEVEL above is optimistic. The
objects under test are a within-ladder rank statistic and a within-ladder Sharpe span; a
survivor list moves every panel in a ladder in the same direction, so it can bias the level and
not the sign of the decomposition. It does, however, make the k → 439 limit *more* degenerate
than a live pool would be, which is a caveat that runs **with** conclusion (2), not against it.
No arm here is a new book — CAND-n / EWall are the record's existing books on re-drawn panels.
