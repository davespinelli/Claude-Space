# Idea 827 — does PROTOCOL 4b have a BENCHMARK-REGIME DEPENDENCE the record never states?

**lane B, 2026-09-12.** Script: `2026-09-12_does-the-4b-CAGR-FLOOR-have-a-BENCHMARK-REGIME-DEPENDENCE-the-record-never-states_B.py`.
**VERDICT: KILL of the queue's hypothesis — and a NEW, larger caveat in its place. No RULES change,
no PROTOCOL edit applied, no book promoted, no KEEP claimed, no memo. RULES.md, PROTOCOL.md,
scan.py, bot.py and baseline.py untouched (rule 6).**

## The question and the answer

Idea 829's sensitivity S2 found ZERO of 4,520 entry windows has SPY CAGR ≤ 0, so every 4b verdict
in the record has been read against a benchmark compounding 9.70–22.15%/yr. The queue's hypothesis
was that some standing 4b passes are therefore **artefacts of an unstated benchmark regime**.

**ANSWERED = YES there is a dependence, NO it does not manufacture a single pass.** All three of
4b's ratio legs (`CAGR ≥ 0.70×bench`, `MaxDD ≤ 0.60×bench`, `Sharpe > bench`) tighten **monotonically**
as the benchmark's drift rises, so a weaker benchmark makes 4b strictly **easier**:

- **H_ARTEFACT FAIL — 0 of 24** (6 standing-pass books × the queue's 4 drifts {0,2,4,6}%) cells fail.
- **H_MONOTONE PASS — 0** fail→pass violations over 69 fine-grid drifts × 3 conventions × 8 books.

So the direction of the bias is the opposite of the one the queue assumed. **The record's 4b passes
were scored against the HARDEST benchmark the sample offers, not the easiest.**

## What the dependence does buy: the BREAK DRIFT, and it is thin

Under the path-preserving convention P (SPY's own daily path, vol matched exactly, drift retilted),
the benchmark CAGR at which each standing pass dies:

| book | break drift | margin over SPY's realised 15.16% | binding leg |
|---|---|---|---|
| CAND-B003-G100 (the standing candidate) | **16.50%** | **+1.34 pp** | cagr |
| B008-G100 | 16.50% | +1.34 pp | cagr |
| MARS-G075-W | 16.50% | +1.34 pp | cagr |
| EWALL-MAGATE-G100-M | 17.50% | +2.34 pp | cagr |
| B136-R6TOP20-G065-W | 18.50% | +3.34 pp | halves |
| Q50RS-G075-M | 22.00% | +6.84 pp | cagr |
| LIVE-V2-G075 (control) | 12.50% | −2.66 pp | cagr |
| RULES-V1 (control) | 9.50% | −5.66 pp | cagr+halves |

**H_BREAK PASS** (6 of 6 break at ≤ 25%/yr). **H_LEG FAIL** (5 of 6 bind on `leg_cagr`; B136-R6TOP20
binds on the halves clause). Three of the six — including the standing candidate — sit **1.34 pp/yr**
from failing. A benchmark 9% stronger in relative terms retires half the record's 4b shelf.

## The bigger finding: 4b's DD cap is a DRAW, not a bar

**H_CONV FAIL — median break drift spreads up to 9.50 pp across the three vol-matching conventions**
(Q50RS-G075-M: 22.00 under P, 13.50 under block bootstrap B, 12.50 under iid normal N).
The mechanism is in `.benchdiag.csv`: at **matched vol AND matched drift**, the synthetic benchmark's
own MaxDD is

| convention | median bench MaxDD | p10 / p90 | ⇒ 4b DD cap (60%) |
|---|---|---|---|
| P (SPY's actual path) | −33.72% | −33.72% / −33.72% | −20.23% |
| B (block bootstrap, 63d) | −33.00% | −37.76% / −27.77% | −19.80% |
| N (iid normal) | −32.61% | −43.67% / −24.17% | −19.57% |

so the 4b drawdown cap ranges from **−26.2% to −14.5%** across paths that are *identical* in drift and
vol. At the drift SPY actually delivered, the standing passes fail the **DD leg** on 4–58% of
bootstrap paths and 22–50% of normal paths, and the **halves leg** on 18–58% — while `fail_cagr` is
**0.00** for all six. Restated: **4b's `MaxDD ≤ 60% of SPY's` is not conditioning on SPY's drift, it
is conditioning on the particular crash sequence SPY happened to realise (one GFC, one COVID, one
2022).** That is the unstated regime dependence the queue was looking for, and it lives in the DD leg,
not the CAGR floor.

## Rule 8

**(a) this run's own tuned parameter.** Break drift estimated on 2009-01-13…2016-12-31 only, OOS
2017-01-01…2026-09-11 read once. **H_WF FAIL — max |OOS − IS| = 3.50 pp against a 3.00 pp bar**
(CAND-B003-G100 15.00 → 18.50). The miss is in the **generous** direction in **7 of 8** books
(OOS break ≥ IS break; the one exception is Q50RS-G075-M, 21.00 → 20.50), because SPY's IS MaxDD is
**−22.06%** against **−33.72%** OOS, so 4b's DD cap is looser out of sample. **Spearman(IS rank, OOS
rank) = +0.8590** and Pearson **+0.9528** over the 8 books: the *ordering* of break drifts is
selectable in sample even though the *level* is not.

**(b) mandated book leg, OOS 2017-01-01…2026-09-11, nothing fitted:**

| book | OOS CAGR | OOS Sharpe | OOS MaxDD |
|---|---|---|---|
| CAND-B003-G100 | 12.70% | 1.2775 | −15.91% |
| B008-G100 | 12.04% | 1.1654 | −19.05% |
| MARS-G075-W | 12.35% | 1.1061 | −18.65% |
| Q50RS-G075-M | 16.00% | 1.2154 | −19.98% |
| EWALL-MAGATE-G100-M | 12.65% | 1.2693 | −15.49% |
| B136-R6TOP20-G065-W | 14.52% | 1.0400 | −19.43% |
| **RULES v2 baseline (live), u56** | **9.47%** | **1.2782** | **−12.05%** |
| **SPY** | **15.33%** | **0.8767** | **−33.72%** |

Full sample: CAND 11.54%/1.2017/−15.91%, halves 1.2354/1.1749; live RULES v2 8.63%/1.2018/−12.05%,
halves 1.2349/1.1757; SPY 15.16%/0.8861/−33.72%.

**Both KEEP paths, every book:** all six standing passes are **4b PASS / 4a FAIL**, full sample AND
OOS — 4a fails on drawdown for every book that raises return, exactly as the record already says. The
two controls fail 4b on the CAGR floor (LIVE) and on four legs (V1). Nothing new is a KEEP candidate;
this run proposes no book.

## Hypotheses: 2 of 6 PASS · Gates: 5 of 5 PASS

`H_ARTEFACT` FAIL (0/24) · `H_MONOTONE` **PASS** (0 violations) · `H_BREAK` **PASS** (6/6) ·
`H_LEG` FAIL (5/6) · `H_CONV` FAIL (9.50 pp) · `H_WF` FAIL (3.50 pp).

Gates: **G1** fast `mets()` vs `engine.metrics` on all 8 books **0.000e+00** (bar 1e-12) · **G2**
reproduces the standing candidate memo's published 11.52%/1.1996/−15.91% and OOS 12.66%/1.2740/−15.91%
to **0.0004** · **G3** the local v2 constructor equals `baseline.rules_v2_weights` **weight-for-weight
at 0.000e+00** · **G4** `vol_match_redrift` hits target vol AND target geometric CAGR simultaneously to
**1.43e-14** (an earlier draft's multiplicative tilt moved vol by 3.7e-5 and was rejected by this gate)
· **G5** at the realised benchmark the re-scoring reproduces the record's own 4b verdicts — **6 of 8
pass, exactly the 6 standing passes, with LIVE failing on `cagr` and V1 on four legs**.

## Sensitivity, reported not tuned

At drifts ≤ 0 the literal reading of 4b (`CAGR ≥ 0.70 × bench`, floor goes negative) and the clamped
reading (`max(0, 0.70 × bench)`) **agree at every point here**, because no book in the set loses money;
the two can only diverge for a book with negative CAGR. Worth stating in PROTOCOL anyway: at drift
−4% the synthetic benchmark's MaxDD is **−64.60%**, so 4b's DD cap becomes **−38.76%** — a book could
lose 38% of NAV and clear the risk leg. The record has never read 4b anywhere near there.

## Caveats

1. **SURVIVORSHIP.** `universe.json` (56) and `universe_broad.json` (136) are current-constituent
   lists; every level is optimistic. The bias is shared by book and comparand, and no book changes here.
2. **One benchmark history.** All three conventions are built from the *same* 4,443-bar SPY return
   sample, so the B and N distributions inherit its unconditional moments. They vary the crash
   *sequence*, not the regime.
3. **The break drift is not a forecast.** It says how strong a benchmark would retire a pass, not how
   likely such a benchmark is.
4. **2 tuned parameters exactly** (drift, vol-matching convention), all 14 ladder points × 3
   conventions × 8 books reported in `.ladder.csv`, plus a 69-point fine grid in `.breaks.csv`.

## Files

`.txt` (full console) · `.books.csv` · `.benchdiag.csv` · `.ladder.csv` · `.breaks.csv` ·
`.keeppaths.csv` · `.wf.csv` · `.gates.csv`
