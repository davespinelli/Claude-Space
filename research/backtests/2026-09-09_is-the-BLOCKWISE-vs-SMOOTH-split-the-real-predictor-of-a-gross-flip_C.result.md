# Idea 584 — is the BLOCKWISE-vs-SMOOTH split the real predictor of a GROSS FLIP?

**Lane C, 2026-09-09.  Verdict: KILL of the proposed predictor, and the sign is REVERSED.
Gross-path autocorrelation does not order the record's flips — it orders them BACKWARDS
(Spearman −0.8804 over the 6 de-gross forms; cell-level AUC 0.141), because the SMOOTH
cross-sectional clauses have the HIGHER lag-1 autocorrelation, not the blockwise gates.  The
gross gap fails too (−0.3339), reconfirming idea 581.  What the "blockwise vs smooth" label is
actually naming is the AMPLITUDE of the gross path (SD, AUC 0.9075 over 216 de-gross cells), and
what a flip actually measures is the ORDER of that path against returns, metric by metric.
No RULES change; no book promoted; no memo.  RULES.md, scan.py, bot.py, baseline.py, PROTOCOL.md
untouched.**

## Gates (all PASS, run before anything was measured)

| gate | what it checks | result |
|---|---|---|
| G1 | the vectorised runner vs `engine.backtest`, 4 books | max abs return diff **2.08e-17** |
| G2 | matched gross, asserted cell by cell on all 324 cells | **< 1e-12** |
| G3 | **PROVENANCE:** idea 581's committed 324 cells reproduced | max abs Δ(delta) **2.84e-16**, flip-flag disagreements **0** |
| G4 | a block permutation preserves the fire count and mean target gross | fire count **exact**, max abs Δtg **8.88e-16** |
| G5 | λ=1 is the clause, λ=0 is the control, mean target gross affine in λ | **0.000e+00 / 0.000e+00 / 2.22e-16** |

G3 is the one that lets this run speak about idea 581's claim at all: the same 0 Sharpe / 7 CAGR
/ 28 MaxDD flips, cell for cell.  G4 is the one that makes PART B a clean experiment — a block
permutation cannot change the gap because it does not change the multiset.

## PART A — the question as asked (36 comparisons per form: 4 dials × 3 gross × 3 panels)

| form | level | flips | flip rate | GAP | **SD** | **RHO1** | RHO5 | RUN (d) | TIMING | DDTIME |
|---|---|---|---|---|---|---|---|---|---|---|
| DD-DG | market | 14/36 | 38.9% | 0.2366 | 0.3990 | **0.9515** | 0.7620 | 29.8 | +0.1137 | −0.0656 |
| BREADTH-DG | market | 12/36 | 33.3% | 0.2316 | 0.3926 | **0.9583** | 0.7949 | 33.0 | +0.0738 | −0.0552 |
| SPYTR-DG | market | 9/36 | 25.0% | 0.2400 | 0.3981 | **0.9552** | 0.7813 | 30.5 | +0.1111 | −0.0546 |
| MA-DG | name | 0/36 | 0.0% | 0.3661 | 0.1903 | **0.9856** | 0.9267 | 32.1 | +0.1281 | −0.0469 |
| VOL-DG | name | 0/36 | 0.0% | 0.1581 | 0.1132 | **0.9835** | 0.9168 | 28.7 | +0.0902 | −0.0327 |
| BAND-DG | name | 0/36 | 0.0% | 0.3627 | 0.1894 | **0.9947** | 0.9722 | 62.7 | +0.1233 | −0.0460 |
| MA/VOL/BAND-RS | name | 0/108 | 0.0% | 0.0000 | 0.0016 | degenerate | — | — | — | — |

The three RS forms are **degenerate by construction** (k = 1 to machine precision, u_t ≡ 1), so a
flip is impossible and the ranking question is only askable over the six de-gross forms.

**The premise is false.**  "Blockwise on/off" was assumed to mean high autocorrelation.  It does
not.  A whole-book gate that switches between full gross and zero has lag-1 autocorrelation
0.9515–0.9583; a cross-sectional clause that thins gross smoothly has **0.9835–0.9947**, because
its path is a slow-moving continuous process with no jumps at all.  Ranked descending, RHO1 puts
BAND-DG > MA-DG > VOL-DG > BREADTH-DG > SPYTR-DG > DD-DG — the exact reverse of the flip order.

| predictor | Spearman(·, flip rate), n = 6 | separates the 3 flippers | AUC, 216 DG cells | AUC, within 108 market-DG |
|---|---|---|---|---|
| GAP | −0.3339 | no | 0.6385 | **0.7706** |
| **SD** | **+0.8804** | **YES** | **0.9075** | 0.7706 |
| RHO1 | **−0.8804** | no | **0.1408** | 0.3456 |
| RHO5 | −0.8804 | no | 0.1436 | 0.3526 |
| DRHO1 | −0.8317 | no | 0.2597 | 0.5205 |
| RUN | −0.1518 | no | 0.5337 | 0.6305 |
| TIMING | −0.3947 | no | 0.4960 | 0.5417 |
| DDTIME | −0.9411 | no | 0.5471 | 0.6888 |

Statistics named, per idea 564: Spearman is Pearson on average ranks, n = 6; AUC is Mann-Whitney,
ties 0.5.  **Chance floor: with 3 flipping and 3 non-flipping forms a coin puts the flippers on
top with probability 1/C(6,3) = 5.0%**, so the one "YES" is a shortlist entry, not a mechanism —
which is why PARTS B and C exist.

Two things the cell-level columns add.  (i) **Idea 581's "at the SAME mean gross gap" is a
between-group statement that does not survive within-group**: inside the 108 market-DG cells the
gap is the joint-best discriminator at AUC 0.771 (SD is identical there, because for a binary
gross path both are monotone in the fire rate).  (ii) RHO1 is below 0.5 in **both** columns —
worse than a coin in the same direction each time.

## PART B — the decisive ladder: order scrambled, gap frozen EXACTLY

The gate's fired/not-fired sequence over the scored rebalance days is cut into blocks of L weeks
and the blocks are permuted (seeds 0, 1, 2).  A permutation preserves the multiset, so the gap,
the amplitude, the fire rate and the whole marginal distribution are invariant; only the order
moves.  108 market-DG cells × 4 L × 3 seeds = **1,296 draws**.

| L | n | GAP | SD | RHO1 | RUN (d) | TIMING | flip CAGR | flip MaxDD | **flip any** |
|---|---|---|---|---|---|---|---|---|---|
| **ACTUAL** | 108 | 0.2361 | 0.3966 | **0.9550** | 31.1 | +0.0995 | 6.5% | 25.9% | **32.4%** |
| 1w | 324 | 0.2355 | 0.3964 | 0.7905 | 6.4 | +0.0200 | 7.7% | 54.6% | 58.6% |
| 4w | 324 | 0.2358 | 0.3967 | 0.9167 | 16.2 | −0.0468 | 46.9% | 54.9% | **76.9%** |
| 13w | 324 | 0.2361 | 0.3967 | 0.9421 | 23.8 | −0.0071 | 32.4% | 49.4% | 65.7% |
| 52w | 324 | 0.2358 | 0.3965 | 0.9521 | 29.0 | −0.0329 | 45.7% | 42.0% | 70.1% |

Target gross across every (L, seed): max |tg − tg(ACTUAL)| = **8.88e-16**.  The ~1e-3 wobble in
the GAP/SD columns is the realised held path drifting between rebalances, not the target.

- **Autocorrelation is worth nothing on its own ladder.**  Draw-level AUC(RHO1) = **0.5270** over
  1,296 draws; by RHO1 tertile the flip rate is 61.3% / 73.2% / 68.9% — not monotone.  The
  ladder moves RHO1 from 0.79 to 0.95 and the flip rate does not follow (Spearman −0.30 over the
  five rungs), and the **real gates carry the highest RHO1 and the lowest flip rate of all**.
- **Scrambling the order alone doubles the flip rate, 32.4% → 67.8%.**  The mean deltas say why:
  the real gates keep a drawdown edge over the matched control (dMaxDD +0.0877 unmatched →
  **+0.0267** matched), while the scrambled ones lose it entirely (+0.0238 → **−0.0371**).
- **A flip is not one phenomenon.**  Per metric, over the shuffled draws:

  | | rate | AUC(RHO1) | AUC(TIMING) | AUC(DDTIME) | AUC(GAP) |
  |---|---|---|---|---|---|
  | flip CAGR | 33.2% | 0.640 | **0.111** | 0.403 | 0.432 |
  | flip MaxDD | 50.2% | 0.433 | 0.492 | 0.525 | **0.640** |

  The **CAGR flip is a timing statistic**, and near-tautologically so: dU_CAGR = −(exposure cost)
  + (timing gain), so a draw whose timing gain happens to exceed the exposure cost crosses zero
  unmatched while dM_CAGR, which nets exposure out, does not.  By TIMING tertile the CAGR flip
  rate runs **73.7% / 24.5% / 0.9%**.  The **MaxDD flip is captured by no scalar summary of the
  path at all** — the best of the eight is GAP at 0.640 — which is what idea 321 would predict:
  a drawdown verdict turns on one episode, and no mean, sd or autocorrelation of the exposure
  path knows which episode it landed in.

## PART C — the mirror ladder: gap dialled 4×, autocorrelation frozen

W(λ) = λ·W_clause + (1−λ)·W_control, all 9 forms × 4 dials × 3 panels at g = 0.75.

| λ | GAP | SD | RHO1 | flip CAGR | flip MaxDD | flip any | market-DG | name-DG |
|---|---|---|---|---|---|---|---|---|
| 0.25 | 0.0664 | 0.0701 | 0.9718 | 6.9% | 0.0% | 6.9% | 13.9% | 0.0% |
| 0.50 | 0.1329 | 0.1402 | 0.9717 | 4.2% | 0.0% | 4.2% | 8.3% | 0.0% |
| 0.75 | 0.1994 | 0.2103 | 0.9716 | 2.8% | 0.0% | 2.8% | 5.6% | 0.0% |
| 1.00 | 0.2659 | 0.2805 | 0.9715 | 2.8% | 12.5% | 15.3% | 30.6% | 0.0% |

RHO1 range across the ladder: **3.03e-04**.  Spearman(GAP, flip rate) over the four rungs = +0.20
— **the flip rate is not monotone in the gap**.  The one sharp feature is that **every drawdown
flip on this ladder needs the full blockwise cut**: 0 of the 216 partial-amplitude cells flip on
MaxDD, and 9 of 72 do at λ = 1.  This ladder cannot separate gap from amplitude — both are affine
in λ — and it is reported as such, not as evidence for either.

## PART D — rule 8 walk-forward (27 picks: 9 arms × 3 panels)

(dial, g) chosen on 2009–2016 only by IS dSharpe against the unmatched control (the record's own
selection rule); 2017–2026 read once.

- IS sign holds OOS on **16/27** picks (59.3%) — idea 581's 59.3% under the same convention.
- **KEEP paths on the picks: 4a 1/27, 4b 3/27.**  Over all 324 grid points with no selection:
  **4a 6, 4b 50, BOTH 0** — identical to idea 581's counts, as G3 requires.
- The three 4b picks are the three books idea 581 already PARKed, re-derived, **not new**:

| pick | full CAGR / Sharpe / MaxDD | H1 / H2 | OOS CAGR / Sharpe / MaxDD | flips? |
|---|---|---|---|---|
| U56 BREADTH-DG q=0.20 g=1.00 | 16.01% / 1.2580 / −16.48% | 1.187 / 1.357 | 16.39% / **1.4563** / −14.16% | yes |
| U56 DD-DG q=0.10 g=0.75 | 11.81% / 1.2028 / −14.94% | 1.185 / 1.241 | 11.42% / 1.3436 / −14.94% | no |
| B136 BREADTH-DG q=0.20 g=1.00 | 15.17% / 1.1356 / −20.02% | 1.248 / 1.014 | 12.58% / 1.1553 / −15.32% | no |

against **RULES v2** (U56 8.64% / 1.2037 / −12.05%, OOS Sharpe 1.2817; B136 8.03% / 1.1058, OOS
1.1185) and **SPY** (15.19% / 0.8871 / −33.72%, OOS Sharpe 0.8786).  All three fail 4a; the one
4a pass (B136 VOL-DG cap 0.45 g=0.50, OOS Sharpe 1.1606) fails 4b on CAGR.  **Nothing is
promoted and no memo is filed** — these are re-derivations of already-published, already-declined
rows, and this run's grid was built for the mechanism question, not for capital.

## Reference levels (survivorship: B136 and SMALL439 are CURRENT constituents; LEVELS biased up)

| panel | SPY CAGR / Sharpe / MaxDD | RULES v2 CAGR / Sharpe / MaxDD | SPY OOS Sharpe | v2 OOS Sharpe |
|---|---|---|---|---|
| U56 | 15.19% / 0.887 / −33.72% | 8.64% / 1.204 / −12.05% | 0.879 | 1.282 |
| B136 | 15.23% / 0.889 / −33.72% | 8.03% / 1.106 / −12.24% | 0.882 | 1.119 |
| SMALL439 | 14.13% / 0.862 / −33.72% | 3.81% / 0.573 / −14.68% | 0.882 | 0.568 |

## What this is worth to the record

1. **Retire "blockwise" as a shorthand for autocorrelation.**  It is an AMPLITUDE word.  On this
   corpus the smooth cross-sectional clauses are the more autocorrelated ones by 0.03–0.04, and
   any future claim that reads "the gate is blockwise, hence persistent" is backwards.
2. **Idea 581's "at the SAME mean gross gap" does not survive within-group.**  Between forms the
   gap is uninformative (AUC 0.639); inside the market gates it is the joint-best predictor
   (0.771).  A between-group null is not a within-group null.
3. **A flip is metric-specific and mostly an order statistic.**  Freezing the gap, the amplitude
   and the marginal distribution and scrambling only the order doubles the flip rate.  The CAGR
   flip is a timing statistic (AUC 0.111); the MaxDD flip — the one that carries 28 of idea 581's
   35 flips — is predicted by nothing measured here, and is the leg the record should stop
   summarising with path statistics at all.

Outputs: `.console.txt` `.cells.csv` `.forms.csv` `.rank.csv` `.auc.csv` `.shuffle.csv`
`.lambda.csv` `.walkforward.csv` `.keeppaths.csv`
