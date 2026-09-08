# Idea 241 — the 0.013 margin rule (cloud, 2026-09-08)

Script: `2026-09-08_the-013-margin-rule_cloud.py`
Console: `.console.txt` · CSVs: `.corpus .instances .tau .holdout .livegrid .walkforward .keeppaths`

**Verdict: KILL.** A minimum-margin abstention rule does not beat the raw IS argmax anywhere —
not on the record's 8,748 published argmaxes, not out of sample when its own threshold is
chosen honestly, and not on fresh prices. Idea 77's 0.013 is the 46th percentile of the
record's own margins, i.e. an ordinary margin; "0.013 was too thin to act on" is a post-hoc
reading of one instance. No new candidate, no memo.

## Reproduction gates (binding, before any new number)
| gate | published | here |
|---|---|---|
| idea 114's margin distribution, its own 44 committed cells | mean 0.019 / median 0.006 / max 0.120 | 0.0190 / 0.0060 / 0.1195 — MATCH |
| idea 114's null, Spearman(margin, OOS regret) | +0.119, wrong sign | +0.104 — MATCH |
| `fast_backtest` vs `engine.backtest`, RULES v2 / u56 | — | max abs diff 0.000e+00 |

## A. The corpus — 8,748 published argmaxes over 92 committed files
Mechanical, not by prose: 1,909 committed CSVs scanned; rejected 1,238 (no `OOS_Sharpe`),
254 (no `IS_Sharpe`), 175 (no numeric design dial with 3–25 levels), 149 (no clean ≥3-rung
ladder), 1 empty. Replication/reporting axes (draw, seed, rung, phase, shift, fold, cost_bps…)
are barred from being the dial. Ladders 3–21 arms, median 4. Top dials: `off` 2277, `f` 1502,
`q` 1158, `gross` 945, `g` 617, `share` 427.
One file carries 1,210 instances, so **every pooled number is reported both instance-pooled and
file-clustered (equal weight per file), and every bootstrap is blocked on file.**

## B. The margin, and where 0.013 sits (R4)
Mean 0.0339, median 0.0167, sd 0.0510, max 0.751; p10 0.0005, p25 0.0028, p75 0.0447, p90 0.0837.
**Idea 77's 0.013 is the 45.8th percentile — R4 CONFIRMED, an ordinary margin.**
The pick is already the OOS-best arm in 37.4% of instances (file-clustered 39.7%); mean regret
0.0413. Spearman(margin, regret) +0.151 pooled / −0.122 within-file — no usable signal in
either direction, consistent with idea 114's null.

## C. The rule (P1 = tau, P2 = fallback) — every rung reported
| tau | abstain | d vs argmax (LADDER-MEAN) | file-clustered | d vs argmax (LADDER-MEDIAN) | file-clustered |
|---|---|---|---|---|---|
| 0 (raw argmax) | 0.0% | +0.0000 | +0.0000 | +0.0000 | +0.0000 |
| 0.001 | 16.2% | −0.0000 | −0.0001 | +0.0002 | +0.0000 |
| 0.005 | 31.1% | −0.0012 | −0.0015 | −0.0001 | −0.0010 |
| **0.013 (idea 77)** | 45.8% | **−0.0026** | **−0.0028** | **+0.0006** | **+0.0002** |
| 0.020 | 53.6% | −0.0041 | −0.0045 | +0.0004 | −0.0009 |
| 0.030 | 63.4% | −0.0058 | −0.0064 | +0.0003 | −0.0012 |
| 0.050 | 78.1% | −0.0084 | −0.0099 | +0.0004 | −0.0025 |
| 0.100 | 92.7% | −0.0136 | −0.0169 | −0.0024 | −0.0066 |
| 0.250 | 99.0% | −0.0196 | −0.0257 | −0.0074 | −0.0144 |
| ∞ (always abstain) | 100.0% | **−0.0237** | **−0.0387** | −0.0124 | −0.0308 |

**Under LADDER-MEAN, 0 of 9 tau > 0 rungs beat the raw argmax; the curve is monotone DOWN in
tau and ∞ is the worst point.** Under LADDER-MEDIAN two rungs (0.001, 0.013) are nominally
ahead by +0.0000/+0.0002 file-clustered — three decimal places below the +0.0387 the raw
argmax already earns over the ladder mean, i.e. noise-scale.
R1 CONFIRMED (no interior optimum worth the name). **R2 REFUTED**: abstaining always is not
the winner here, it is the worst point on both fallbacks. R3 partly held — the curve is
close to linear in the abstention rate (max deviation 0.020/0.022 over the 9 finite rungs).

## D. Rule 8 on the corpus — tau chosen on half the FILES, read once on the other half (20 seeds)
| fallback | tau* chosen | held-out gain of tau* | seeds positive | held-out gain of tau=∞ |
|---|---|---|---|---|
| LADDER-MEAN | 0.001 in 20/20 | **−0.0001** | 7/20 | −0.0405 (0/20) |
| LADDER-MEDIAN | 0.001 / 0.013 / 0.030 | **−0.0009** | 4/20 | −0.0339 (0/20) |

**The rule does not survive its own walk-forward.** Its LADDER-MEDIAN in-sample edge of
+0.0002 becomes −0.0009 held out, positive in 4 of 20 seeds — a coin flip on the wrong side.

## E. Rule 8 on live prices, out of corpus — idea 229's pre-registered 36 cells
6 dials × 3 panels × 2 cost rungs, each dial carrying its **declared incumbent**; choice on
IS (≤2016-12-31) only, 2017–2026 read once. Live margin median 0.0036; **69.4% of live cells
sit at or below idea 77's 0.013**, so the rule bites hard here.

| tau | abstain | mean OOS Sharpe (incumbent fallback) | d vs argmax | (ladder-mean fallback) | d |
|---|---|---|---|---|---|
| 0 | 0.0% | 0.8042 | +0.0000 | 0.8042 | +0.0000 |
| 0.001 | 27.8% | 0.8028 | −0.0013 | 0.8014 | −0.0028 |
| 0.005 | 55.6% | 0.7835 | −0.0206 | 0.7778 | −0.0264 |
| **0.013** | 69.4% | 0.7684 | **−0.0358** | 0.7690 | −0.0351 |
| 0.050 | 88.9% | 0.7317 | −0.0724 | 0.7447 | −0.0595 |
| ∞ | 100.0% | 0.7328 | −0.0714 | 0.7478 | −0.0564 |

Pooled equal-weight books (6 panel×cost books): **CHOOSER OOS Sharpe 0.8214, ABSTAIN@0.013
0.7668 (−0.0546), INCUMBENT 0.7138 (−0.1077), LADDER-MEAN 0.7666, ORACLE 0.8520.**
The abstention rule gives back 51% of the gap between the chooser and the (non-investable)
oracle, and gets nothing for it.

Benchmarks (full / OOS): SPY 15.23% / 0.889 / −33.72%, OOS 15.45% / 0.882. RULES v2 @10 bps
u56 8.66% / 1.206 / −12.05%, broad 8.03% / 1.106, small 3.80% / 0.571. RULES v1 @10 bps
u56 6.46% / 0.665, broad 6.39% / 0.635, small 8.15% / 0.603.

## A side finding, with its caveat
On this corpus the **raw argmax beats the ladder mean by +0.0387 file-clustered**
(pooled +0.0237, 95% file-blocked CI [+0.0207, +0.0585], P(≤0) 0.000), and on the live 36
cells by +0.0714. That runs against the record's standing "selection loses to a control"
result (ideas 229/232/446). It is **not** a refutation of those, and this run does not claim
one: admission here requires only that a source file published both columns, so the corpus
mixes IS/OOS conventions, ladder kinds and comparands, whereas 229/446 matched the control to
the same ladder and found ≈0. Even on the live frame the +0.0714 mean is **positive in only
17 of 36 cells** — it is a fat right tail on the `share` and `kexp` dials (+0.24 to +0.43 on
u56/broad), not a broad win. Read it as a reason to re-run the controlled comparison on a
wider dial set, not as evidence that selection pays.

## Both KEEP paths — 30 pooled books
**4a vs live RULES v2: 0/30. 4a vs the retired RULES v1: 24/30. 4b vs SPY: 1/30.**
The single 4b pass is `CHOOSER, u56, 10 bps`: CAGR 10.85%, Sharpe 1.111, MaxDD −15.13%,
H1/H2 1.145/1.087, OOS 11.75% / 1.151. **Reported as a by-product, NOT a candidate and no
memo**: it is an equal-weight composite of six free dial choices (far over the 2-parameter
budget), it clears the CAGR floor by 0.19 pp (10.85% vs 10.66%), and its own OOS Sharpe 1.151
is below the live RULES v2 book's 1.285 on the same panel. Its ABSTAIN and INCUMBENT
counterparts fail 4b outright. Binding 4b bars over all 30: CAGR 29, H2 17, H1 14, OOS 14, DD 10.

## SURVIVORSHIP
The small panel is current constituents of a sub-$2B screen; the broad panel is current
constituents (PROTOCOL 9). Levels are upward-biased and only same-cell contrasts (pick minus
fallback, same ladder, same days) are read. The record corpus is a re-reading of committed
artefacts and inherits whatever bias each source run carried.

## Recommendation
Do not adopt a minimum-margin abstention clause. The margin remains what idea 114 found it to
be — a selector-STABILITY statistic — and this run adds that it is not a decision rule at any
threshold, under either fallback, in or out of sample.
