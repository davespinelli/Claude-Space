# Idea 885 — what makes a RESHAPED length multiset cost +0.0012 in UNIFORM gaps and nothing in REAL ones?
Lane C, 2026-09-15. Script `2026-09-15_conditional-gap-null-closes-the-INTERACTION_C.py`.

**ANSWERED — NOTHING DOES. THE QUANTITY THE IDEA WAS COMMISSIONED TO EXPLAIN IS NOT THERE AT 200
SEEDS.** At 20 seeds the interaction's own cross-arm SE is ±0.0011, which is the size of the
residual itself; at 200 seeds all three LEGAL cap rules read inside the calibration band
(SPLIT8 **+0.00006**, FILL **−0.00015**, LONE **−0.00058**, SE 0.00039, band ±0.0010) and only
DOM — the null whose longest run is **13.7×** the real arm's cap — survives, at −0.00318 and with
the opposite sign. The conditional gap draw this run built works exactly as designed and moves
nothing, so the queue's nominated carrier is refuted too. **KILL for capital**; nothing promoted,
`RULES.md`, `PROTOCOL.md`, `scan.py`, `bot.py` and `baseline.py` untouched (rule 6). One
correction to the record is proposed as a finding, not applied.

SELECTION: taken as the second Open idea **with a price leg**. 888 sits above it and carries a
standing lane-C SKIP (a re-read of nine committed runs' published placebo VERDICTS: prose, no book
to price, so it cannot carry this run's mandatory rule-8 walk-forward or either KEEP path).

## Setup
2 tuned params, the queue's own: **PARAM 1 conditioning statistic {PRE, ADJ} × PARAM 2 cap rule
{REAL, DOM, SPLIT8, LONE, FILL}**. Reported axes, never selected over: panel {U56 56, B136 136,
SMALL 664}, family {BREADTH, VOL20, DISP, CORR} × {HI, LO}, q {0.07, 0.12, 0.17}, w {252, 1008},
depth {0.50, 1.00}, cadence {D, W}, gross {0.75, 1.00}, cost rung {0, 10, 25}. 10 bps, next-day
fills. **1,152 arms × 21 nulls × 200 seeds = 4,838,400 placebo paths, each priced at three rungs
= 14,515,200 placebo books.** Every grid point is in `.gap.csv` / `.excess.csv` / `.closure.csv`.

**THE NEW OBJECT — CG.** 871's gap draw, the *identical multiset*, re-ORDERED so that the
association between a run's length and the gaps beside it reproduces the REAL arm's own. `CG*_X`
is handed `SM_X`'s md5 stream, so the two share the gap multiset AND the reshaped length multiset
and differ in ONE thing: which gap sits next to which run. Coupling strength is not a parameter —
it is the arm's own ρ through the Gaussian copula identity ρ_S = (6/π)·asin(ρ_P/2), with ADJ
pre-divided by the averaging constant 0.8165 = (2/4)/√(6/16), derived, not fitted.

Gates. **G7** BLOCK2 **−0.00000** (SE 0.00026, sign z +0.00) → the band. **G2** rate match
**0.000e+00**. **G8** OP_REAL ≡ BLOCK bit-for-bit **0.000e+00**. **G_MARG** CG carries SM's gap
AND length multisets element-for-element, **0 violations in 3,000**. **G_JOINT** on synthetic
COUPLED arms (half the gate corpus is built with a real association, because a gate that only ever
sees ρ = 0 cannot tell a working coupling from a broken one): |CG achieved − real| **0.003 / 0.012**
against a 0.10 bar, while 871's own draw reads |ρ| ≤ **0.011**. **G_ARMS** the 1,152-row real-arm
table reproduces 882's committed `arms.csv` at **0.000e+00** on CAGR, Sharpe and OOS Sharpe, and
picks the same three rule-8 books. **G5a/G5b** inherit 882's named defect (1.058% of matched draws,
871's gap draw can zero BOTH boundary gaps and circularly merge two runs); every headline is
re-read on the 1,110 clean arms and moves by ≤ 0.0001.

## 1. The residual is a 20-seed artefact — the decisive table
Same 1,152 arms, same formula `I = s(SM_X) − s(OP_X) − s(UG_REAL)`, 882's committed `gap.csv`
read at its 20 seeds against this run at 200:

| cap rule | I @20 seeds (882) | I @200 seeds | SE @200 | mean/SE @200 | legal cap? |
|---|---|---|---|---|---|
| SPLIT8 | +0.00048 | **+0.00006** | 0.00039 | +0.33 | yes |
| FILL | +0.00057 | **−0.00015** | 0.00040 | −0.14 | yes |
| LONE | +0.00155 | **−0.00058** | 0.00039 | −2.49 | yes |
| DOM | −0.00263 | **−0.00318** | 0.00037 | −10.04 | **no — max run 13.7 × L\*** |

The arithmetic that settles it, and it is checkable against the run's own output: the per-arm seed
SD of the excess at 10 bps is **0.0668**, so a per-arm median has SE 1.2533·σ/√S = **0.0187** at 20
seeds and **0.0059** at 200; the interaction is a four-null contrast, so its cross-arm SE is
**±0.0011** at 20 seeds and **±0.00038** at 200 — and the *observed* SEs at 200 seeds are
0.00037–0.00040, matching the prediction. **882's residual was between 0.4 and 1.7 SE of zero at
the seed count it was read at.** Idea 881 called it "an open quantity, not a finding"; that caution
was right and the queue's framing of it as +0.0012 to +0.0023 "with the same sign at all three cap
rules" over-read it. At 200 seeds the three legal rules do not even share a sign.

## 2. What IS there: the PLACEMENT channel, and 882 published it as zero
`UG_REAL` — 871's uniform gap draw applied to the real arm's OWN fire-run length multiset, which
reshapes no run at all — reads **+0.00154** at 200 seeds (mean/SE **+6.95**, sign z **−5.30**,
clean arms +0.00153). 882 published **−0.00003** on clean arms and concluded the placement channel
was zero. It is not: uniform placement alone costs **+0.0015** of Sharpe against BLOCK, which is
larger than every legal cap rule's interaction term and is a **main effect**, not an interaction.
The reshaping "cost" 885 was sent to locate is mostly this, already inside UG_REAL.

## 3. Why the numbers moved — a pattern the record should not ignore
Between 20 and 200 seeds, **9 of 9** switch-matched nulls shift in the SAME direction (+0.00020 to
+0.00184, mean **+0.00099**), while **BLOCK2 — the only contrast whose two sides share BLOCK's own
construction — does not move (−0.00015 → −0.00000)**. Nine same-signed shifts is p ≈ 0.004 against
sampling noise. The signature is that of a small-sample bias in the per-arm *median* estimator that
cancels only between same-construction nulls, and every headline in this line of the record is a
`null − BLOCK` contrast, i.e. exactly the case where it does not cancel. Filed as idea 903, with
the test named; not asserted as established here.

## 4. The queue's nominated carrier is refuted on its own terms
| reading | result |
|---|---|
| H_RHO (real arms carry the joint association, |median ρ| > 0.10) | **REFUTED** at +0.086 (PRE) / +0.086 (ADJ) / +0.075 (POST) |
| H_JOINT (CG reproduces it, 871's draw destroys it) | **CONFIRMED** — BLOCK 0.086 = the real arms' 0.086, UG/SM 0.002–0.011, CGPRE 0.081–0.091 |
| H_CLOSE (conditional gaps close the interaction) | **REFUTED** — and its pre-condition fails first: only 1 of 4 I_UNIF is outside the band |
| H_GAP (CG sits closer to OP than SM does) | **CONFIRMED on the medians, and it does not survive the stricter per-arm test** |
| H_COSTINV | **CONFIRMED** — worst signed range over 0/10/25 bps 0.00055 |

H_GAP is the one place this run's pre-registered bar flatters the result and it is reported as
such: on medians-of-medians CGADJ is closer to OP than SM on 4 of 4 cap rules, but the per-arm
paired test — the same claim, read on each arm — improves on only **0.45–0.53** of arms, and on the
452 arms where the misspecification is largest (|ρ_ADJ| > 0.20) on **0.37–0.51**. The same-draw
contrast `dCOUPLE = CG − SM`, which removes marginal noise by construction, is at most **0.0010**
and its sign flips between the two conditioning statistics (ADJ: DOM +0.00082, LONE −0.00101).
**Restoring the joint (length, gap) distribution does not move the price of the null.**

The association is real but half the size the hypothesis needed, and it is a family fact, not a
book fact: VOL20-HI **+0.271**, CORR-HI **+0.212**, DISP-HI +0.149 against BREADTH-HI **−0.035**,
BREADTH-LO −0.012. Median |ρ| is 0.14–0.15 with 35–39% of arms above 0.20 — which is why the
pooled signed median lands at +0.086 and why conditioning on it changes nothing pooled.

## 5. RULE 8
**(a) THE STATISTIC.** The interaction does not walk forward at any cap rule: I_UNIF DOM IS
**−0.00035** → OOS **−0.00684**, SPLIT8 +0.00145 → +0.00033, FILL +0.00144 → +0.00004, LONE
−0.00109 → −0.00026; every CG version flips sign across the split (CGPRE SPLIT8 +0.00333 →
−0.00145). ρ(IS gap, OOS gap) ≥ +0.30 reaches 8 of 8 families for **SM_DOM only** — 881's
max-run-length effect is again the one persistent object here — 4 of 8 for OP_DOM, 3 of 8 for
CGPRE_DOM and **0 of 8 for all 16 other nulls**, BLOCK2 included.

**(b) THE BOOKS.** IS-only selector (highest 2009–2016 Sharpe per panel), OOS read once, 10 bps,
t+1. All three picks and all three metrics reproduce 882's committed `books.csv` at **0.000e+00**.

| panel | IS-pick | FULL CAGR / Sharpe / MaxDD | halves | OOS CAGR / Sharpe / MaxDD | 4a | 4b |
|---|---|---|---|---|---|---|
| U56 | CORR-HI q0.07 w1008 d1.0 W g1.0 | 12.73% / 1.034 / −22.93% | 1.160 / 0.915 | 12.41% / 1.016 / −22.93% | fail | fail |
| B136 | CORR-HI q0.12 w252 d1.0 W g1.0 | 13.91% / 1.166 / −16.63% | 1.289 / 1.037 | 12.97% / 1.154 / −16.63% | fail | **PASS** |
| SMALL | VOL20-LO q0.17 w252 d1.0 D g1.0 | 5.04% / 0.404 / −48.52% | 0.736 / 0.201 | 2.00% / 0.203 / −48.52% | fail | fail |

Comparands (U56 window): SPY **15.13% / 0.885 / −33.72%** (OOS 15.27% / 0.874), RULES v2 (live)
**8.64% / 1.208 / −11.90%** (OOS 9.49% / 1.286). 4b bars DD ≥ −20.23%, CAGR ≥ 10.59%, OOS Sharpe >
0.874. Unselected base rates: 4a **0 / 1,152**; 4b U56 61 (15.9%), B136 44 (11.5%), SMALL 0.
The B136 pass is an already-committed book reproduced inside a gate, so **no memo is written and
nothing is proposed for promotion**.

## 6. Survivorship
U56 / B136 / SMALL are current-constituent lists (SMALL additionally drops the 52 tickers with
`max_1d_move` ≥ 1.0 per `data/small_meta.csv`), so every CAGR and drawdown LEVEL above is
optimistic — the books' and the comparands' alike. This run's headline is a difference between two
nulls **on the same arm and the same draw**, which is a same-tape contrast and unaffected.

## 7. Limits, stated rather than left to be found
- The 200-seed reading is better than the 20-seed one by construction (a median estimator improves
  monotonically in S, and BLOCK2 reads 0.000 at both), but this run does not *prove* the bias
  mechanism of §3; it reports the pattern and files the test.
- CGADJ over-couples on reshaped lengths (achieved ρ 0.158 against the real arms' 0.086 at DOM)
  because the attenuation constant is derived for the real length multiset. CGPRE does not
  (0.081–0.091). The conclusion is the same under both, and CGPRE is the clean one.
- ρ is measured on the LINEAR decomposition, the geometry 871's draw actually produces; the
  leading and trailing gaps are included. Interior-only medians are +0.093 / +0.110 / +0.093,
  slightly larger, and change nothing.
- One conditioning statistic (POST) is reported as a diagnostic only; no null was built on it, so
  the parameter count stays at two.
