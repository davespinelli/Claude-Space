# Idea 201 — the-margin-column-instead-of-two (cloud, 2026-09-05)

**VERDICT: SPLIT, and the queue's proposal is a KILL. MARGIN is a sufficient statistic for the
clause VERDICT — trivially, because `clears` is *defined* as `|dSharpe| > band` and margin is
`|dSharpe| − band`, so a margin-only reader reproduces all 180 published verdicts on both bars
and on-share changes none of them. It is NOT a sufficient statistic for anything a reader
actually does with the clause: on-share carries real incremental information about the OOS
outcome after the IS margin (partial ρ −0.24 to −0.42; ΔR² +0.240 on DDCTL, +0.217 on SLEEVE),
and adding it to a margin-only selector changes 8 of 18 rule-8 picks worth +0.0717 OOS Sharpe.
PROTOCOL should keep idea 191's PAIR, not collapse it to one column.** Rules unchanged; no new
book; no KEEP candidate. Two by-products below are larger than the answer.

Script: `2026-09-05_the-margin-column-instead-of-two_cloud.py` (754 s, 5490 backtests). Idea
191's script is **imported, never re-typed**. Outputs: `.console.txt`, `.clause.csv`,
`.stability.csv`, `.walkforward.csv`, `.keep.csv`.

---

## 0. Reproduction — asserted before any new number was read

| gate | what | result |
|---|---|---|
| [a] | `fast_backtest` vs `engine.backtest`, all three panels | max \|dret\| 1.39e-17 / 2.08e-17 / 2.78e-17 |
| [b] | cost identity, 10 bps derived from the 0 bps run | 1.39e-17 / 2.08e-17 / 2.78e-17 |
| [c] | base CAND-20 weights vs idea 78/171 `weights_cand` | **0.000e+00** on all three panels |
| [d] | RULES v1 on u56 @10 bps | **6.45305% / 0.66418 / −13.82780%**, every published digit |
| [f] | idea 191's committed `clause.csv`, **all 180 real rows**, 7 quantities | max abs diff **2.220e-16** |

## 1. BY-PRODUCT (larger than the answer): idea 191's published BANDS are not reproducible

Idea 191 seeds its rotations with `SEED + hash((panel, family, thr)) % 10_000`. Python salts
`hash()` on `str` and `PYTHONHASHSEED` is unset, so **that seed is a different number in every
process** — this run printed 9868 for `('U56','DDCTL',0.03)`; the parent's own run used
something else and no record of it survives. Its **real rows reproduce exactly** (2.2e-16
above, gate [f]) and its **bands cannot be reproduced at all**, only re-drawn. PROTOCOL 5 asks
for deterministic scripts; this one is not, and nothing in the committed output says so. This
run uses `zlib.crc32` seeds, which are stable across processes.

## 2. BY-PRODUCT: the clause verdict is 17.8% draw-dependent

60 rotations per configuration = **3 disjoint blocks of 20**, so the band can be measured
against its own sampling noise for the first time.

| quantity | value |
|---|---|
| mean band (block 0, idea 186's construction) | 0.1540 |
| mean sd of the band across the 3 blocks | 0.0435 |
| mean range across the 3 blocks | 0.0819 |
| **mean(range / band)** | **63.3%** |
| verdict flips, block 0 vs block 1 / block 2 / **any** | 17/180, 29/180, **32/180 = 17.8%** |
| mean \|margin\| of flipping rows vs stable rows | **0.0476 vs 0.0775** |
| Spearman(on-share, band sd) | +0.204 |

**About one clause verdict in six is a property of which 20 rotations were drawn, not of the
overlay.** The flip zone is exactly where |margin| is small, which is where the corpus's
near-misses live. Any published `clears` with |margin| below ~0.05 should be read as
undetermined, and the honest fix is more draws or a margin with a stated error bar — not a
second column.

## 3. Q1 — the queue's literal question: NO verdict changes, and that is nearly vacuous

| bar | sign(margin) == published verdict |
|---|---|
| Sharpe | **180/180** |
| drawdown | **180/180** |

Clear rate 34/180 on Sharpe, 28/180 on drawdown. By family at 10 bps (n = 30 each):

| family | clears | mean margin | mean band | mean \|dSharpe\| | mean on-share |
|---|---|---|---|---|---|
| BUDGET | 8 | −0.0254 | 0.0897 | 0.0643 | 54.1% |
| DDCTL | 11 | −0.0066 | 0.1589 | 0.1523 | 17.0% |
| SLEEVE | 0 | −0.1160 | 0.1759 | 0.0599 | 17.5% |

This is an identity, not evidence. It answers the queue as asked and settles nothing, because
the pair was never proposed to *decide* the clause — it was proposed to *interpret* it.

## 4. Q2 — on-share is NOT redundant to margin: it predicts the OOS outcome after it

| rows | target | n used | ρ(margin_IS) | ρ(on-share) | **partial ρ(on-share \| margin_IS)** | R² margin | R² margin+on-share | **ΔR²** | t(on-share) |
|---|---|---|---|---|---|---|---|---|---|
| all 180 | margin_OOS | 178 | +0.434 | −0.248 | **−0.307** | 0.0587 | 0.0750 | +0.016 | −1.76 |
| all 180 | dSharpe_OOS | 178 | −0.181 | −0.191 | **−0.211** | 0.0181 | 0.0347 | +0.017 | −1.73 |
| 90 @10 bps | margin_OOS | 89 | +0.426 | −0.183 | **−0.236** | 0.0650 | 0.0730 | +0.008 | −0.86 |
| 90 @10 bps | dSharpe_OOS | 89 | −0.247 | −0.320 | **−0.361** | 0.0195 | 0.0796 | **+0.060** | **−2.37** |

Within family, at 10 bps (n = 30 each), on OOS margin:

| family | ρ(margin_IS) | **partial ρ(on-share)** | **ΔR²** |
|---|---|---|---|
| BUDGET | +0.275 | −0.049 | +0.001 |
| DDCTL | −0.316 | **−0.376** | **+0.240** |
| SLEEVE | +0.174 | **−0.416** | **+0.217** |

On two of the three families on-share explains **more of the OOS outcome than the IS margin
does**, with the sign idea 191 predicted: higher on-share, worse out-of-sample. Margin cannot
carry that, because the band it subtracts is estimated on the *same* window whose effect it is
netting out. (Two SMALL439 BUDGET τ=0.05/skip cells have an undefined IS Sharpe — the overlay
suppresses 93.7% of rebalances, so the book is flat through the IS window — and are dropped
from these regressions; `n used` states it, nothing is imputed.)

## 5. Q3/Q5 — rule 8, and the decision test the queue actually needed

Overlay point chosen on ≤ 2016-12-31 only, 2017-2026 read once, 18 cells (3 panels × 3
families × 2 cost rungs), pool = 10 points (5 thr × 2 depth). On-share median gate 19.7%.

| selector | mean OOS Sharpe | mean OOS CAGR | mean OOS MaxDD | dOOS | t | W/L | abstains |
|---|---|---|---|---|---|---|---|
| ORACLE-OOS (ceiling) | 0.8197 | 11.04% | −23.16% | +0.0431 | +3.86 | 12/0 | 0 |
| S6 ON-SHARE-only (lowest) | 0.7819 | 10.26% | −23.52% | +0.0053 | +0.74 | 8/4 | 0 |
| **S0 do-nothing** | **0.7766** | **10.22%** | **−23.53%** | — | — | — | — |
| S3 PAIR: margin argmax \| low on-share | 0.7438 | 9.65% | −25.12% | −0.0328 | −1.77 | 7/9 | 0 |
| S1 IS-Sharpe argmax | 0.7405 | 9.55% | −25.52% | −0.0361 | −1.68 | 5/9 | 0 |
| S5 PAIR: clause-gated \| low on-share | 0.7368 | 9.64% | −24.83% | −0.0399 | −2.38 | 0/6 | 12 |
| S4 MARGIN-only, clause-gated | 0.6813 | 8.73% | −24.99% | −0.0953 | −2.66 | 0/8 | 10 |
| **S2 MARGIN-only argmax** | **0.6721** | 8.46% | −25.50% | **−0.1045** | **−2.73** | 5/11 | 0 |

OOS-window benchmarks: **SPY 15.45% / 0.8820 / −33.72%**; RULES v1 @10 bps 7.73% / 0.7471 /
−13.83% (U56), 5.94% / 0.5762 / −21.19% (BROAD136), 7.88% / 0.6617 / −32.37% (SMALL439).

**The decision test:**

| margin-only | + on-share | picks changed | mean dOOS Sharpe from adding on-share |
|---|---|---|---|
| S2 margin argmax | S3 pair | **8 of 18** | **+0.0717** |
| S4 margin clause-gated | S5 pair | 4 of 18 | +0.0554 |

Two things follow. **(a) The pair is not decision-equivalent to margin alone** — the second
column changes 44% of the rule-8 picks and every change is an improvement on average, so the
queue's "one column, not two" is a KILL. **(b) The roles are inverted from idea 191's
framing:** margin, which idea 191 offered as "the single summary", is the **worst selector in
the run** (−0.1045, t −2.73), and on-share, which idea 191 killed as a standalone column, is
the only arm not below the do-nothing control (+0.0053, t +0.74, 8W/4L — inside noise, so this
is not a claim that it works). Margin is the right summary of a *verdict* and the wrong basis
for a *choice*.

**S0 do-nothing still wins.** Every implementable selector except S6 loses to it, and S6's
edge is a third of its own standard error. That is the eleventh consecutive instance in this
project of an IS-fitted selector failing to earn its complexity.

## 6. BOTH KEEP PATHS, on every real row

4a: **37/180**. 4b: **28/180**, all but one on U56 (BROAD136 SLEEVE ma=200 f=0.5 @10 bps is the
single non-U56 pass; SMALL439 passes **0 of 60**). Failing-bar census: 70 rows fail all five,
28 pass, 25 fail `H2,OOS,DD`, 13 fail `H1,CAGR`. The best 4b passes at 10 bps:

| panel | family | thr / depth | on-share | margin | clears | CAGR | Sharpe | MaxDD | H1 / H2 | OOS Sharpe |
|---|---|---|---|---|---|---|---|---|---|---|
| U56 | SLEEVE | 200 / 0.5 | 17.7% | −0.1223 | no | 12.38% | 1.1246 | −14.07% | 1.083 / 1.166 | 1.2333 |
| U56 | BUDGET | 0.05 / half | 88.2% | −0.0271 | no | 13.25% | 1.1208 | −18.17% | 1.115 / 1.132 | 1.2058 |
| U56 | SLEEVE | 400 / 0.5 | 9.1% | −0.0505 | no | 12.74% | 1.1159 | −18.21% | 1.091 / 1.144 | 1.2088 |
| U56 | *(control, no overlay)* | — | 0.0% | 0.0000 | — | 12.86% | 1.1075 | −18.21% | 1.110 / 1.112 | 1.1775 |

**Not one of the 4b passes clears its own null.** Every overlay that passes 4b on this book is
inside its rotation band — i.e. an equally-frequent randomly-timed overlay does the same thing
— which is idea 186/190's finding reproduced here from the other direction. Nothing is
promoted. Several DDCTL rows sit at on-share 0.0% and margin exactly 0.0000: those are idea
202's inert cells, the untilted control published under an overlay's name, and they are
labelled as such rather than counted as passes on their own merit.

## 7. Predictions — 2 of 5 hit

| | prediction | outcome |
|---|---|---|
| P1 | sign(margin) == clears on 180/180, both bars | **HIT** |
| P2 | on-share adds nothing given the IS margin | **MISS** — partial ρ −0.236, ΔR² up to +0.240 |
| P3 | no rule-8 pick differs, margin-only vs pair | **MISS** — 8 of 18 changed |
| P4 | real rows reproduce, bands do not | **HIT** |
| P5 | no selector beats do-nothing OOS | **MISS on the letter** — S6 is +0.0053 at t +0.74, 8W/4L; inside noise, so the substantive claim survives while the literal prediction does not |

Three misses is the run's honest headline: the hypothesis this idea was written to confirm is
wrong on both of its non-trivial legs.

## 8. Caveats, carried not buried

* **SURVIVORSHIP (idea 54):** all three panels are current constituents; SMALL439 has no
  delistings. Real and rotated draws inherit the bias identically so the *clause* reading is
  unaffected; every level (CAGR, Sharpe, 4a/4b counts) is biased upward and is not a tradable
  estimate.
* Only J−1 distinct rotations exist and neighbouring offsets are correlated, so the three
  blocks are disjoint in offset but not independent; §2's flip rate is therefore a *lower*
  bound on the band's true instability, not an upper one.
* Q2 has 180 rows over 90 configurations × 2 near-duplicate cost rungs; every pooled statistic
  is also reported on the 90 unique configurations at 10 bps, and the two disagree in strength
  (t −1.76 vs −0.86 on margin_OOS, −1.73 vs −2.37 on dSharpe_OOS). Neither reading is strong;
  what is robust is the *within-family* ΔR² of +0.24 / +0.22.
* BUDGET-skip's rotation null is not turnover-matched (idea 191 measured 1782.7% mean on this
  grid). That is idea 203's subject; it is inherited and stated here, not fixed.
* Idea 38: calendar-day index after 2014-09-17 on U56/BROAD136. Idea 126: t+1 only.

## 9. Proposed PROTOCOL amendment, report-only, for Sunday review (evidence, not a rule change)

> **Clause 11c stands as idea 191 wrote it — publish the PAIR.** A margin-only reading
> reproduces every clause verdict by construction but loses information: conditional on the
> in-sample margin, on-share still predicts the out-of-sample outcome (partial ρ −0.24 to
> −0.42; ΔR² +0.240 on DDCTL, +0.217 on SLEEVE), and adding it to a margin-only rule-8
> selector changes 8 of 18 picks worth +0.0717 OOS Sharpe. Quote the margin as the summary of
> the *verdict*; never use it as a selector — the margin argmax is the worst arm of eighteen
> cells at −0.1045 OOS Sharpe against the do-nothing control.
>
> **New: the band needs an error bar.** Measured on three disjoint 20-draw blocks, the
> 20-rotation band's own range is **63.3% of its value** and **17.8% of clause verdicts flip**
> between blocks, concentrated where \|margin\| < 0.05. Publish the band as a mean over blocks
> with its spread, or raise the draw count, and read any `clears` with \|margin\| below 0.05 as
> undetermined. Seed every null with a process-stable function (`zlib.crc32`, not `hash()`) —
> idea 191's committed bands cannot be reproduced because Python salts `hash()` on `str`.
