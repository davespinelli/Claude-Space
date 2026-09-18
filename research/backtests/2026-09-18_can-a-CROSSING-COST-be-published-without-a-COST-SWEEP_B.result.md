# Idea 611 (lane B, 2026-09-18) — can a CROSSING COST be published without a COST SWEEP?

**ANSWERED: YES, EXACTLY — AND 608's PUBLISHED FORM IS THE WRONG ONE.  KILL (capital), no new book.**
Script `2026-09-18_can-a-CROSSING-COST-be-published-without-a-COST-SWEEP_B.py`; gates **12 of 12**.
Grid: N {10,15,20,25,30} x GROSS {0.55..0.85 by 0.05} = 35 cells x 3 panels = 105 books, each
swept at 21 real rungs (0..100 bps by 5) — 2,205 honest backtests — and scored under both KEEP
paths at the record's rungs {0,10,25,50}.  Exactly two tuned parameters (N, GROSS); H=126,
weekly, RAW three-leg composite, vol20<0.60, t+1, warm-up 260 all frozen.

1. **A cost rung is an EXACT affine shift, so a sweep re-computes nothing** (gate G3):
   `max |r(c) − (r_0 − c·u)| = 0.000e+00` over 105 books x 21 rungs.  `held` and `turn` are
   functions of the price path alone; cost never feeds back into a weight.
2. **For the Sharpe family the whole ladder collapses to FIVE NUMBERS** read off one 0 bps run:
   `S(c) = (m_r − c·m_u)·√252 / √(v_r − 2c·cov + c²·v_u)` — gate G4, max error **7.77e-16**.
3. **C_EXACT reproduces a real fine sweep at rho +1.00000**, median relative error **2.53e-05**,
   p90 2.49e-04; **0.9980 of the 494 crossing pairs within 0.5%** (1.0000 on the 70 pairs whose
   books both clear 4b).  Its single worst pair (2.28e-02) is a near-tie — dSharpe_0 = 5.1e-06,
   c* = 0.31 bps, absolute gap 0.007 bps — i.e. the SWEEP's own bracket interpolation, not the
   closed form's.
4. **608's linear form should be retired.** C_LIN's median relative error is **1.01e-02**, ~400x
   C_EXACT's, only **0.2409** of pairs within 0.5%, worst **29.9%**.  The term it drops is the
   cost's effect on the DENOMINATOR; H_LINBREAK fires only weakly — rho(|err_lin|, turnover-
   dispersion gap) **+0.2740**, rho with |Δturnover| **−0.1589**.
5. **What breaks is the QUESTION, not the estimator.**  **1,291 of 1,785 pairs (0.7232) never
   cross inside [0,100] bps** — a published c* outside the swept range is not a measurement —
   and **171 of the 494 real crossings (0.3462) are INVISIBLE on the record's own 0/10/25/50
   ladder**.  Where that coarse ladder does see a crossing it is fine (median gap 0.0065 bps).
6. **The record's own bill** (`.record_sweeps.csv`): 1,425 committed csv artefacts carry a cost
   column; **729 (0.5116) are sweeps of >= 3 rungs, with 2,741 redundant rungs** that gate G3
   proves are exact recomputations of their own 0 bps row.
7. **RULE 8 (parameters on warm-up..2016 only, 2017-2026 read ONCE).**  **K_EXACT and K_LIN reach
   the SAME BOOK as the real sweep at 12 of 12 (panel x deployment rung)** — H_REACH fires for
   the closed form and, contrary to the pre-declaration, for the linear form too: c* accuracy and
   argmax agreement are different bars.
8. **CAPITAL VERDICT: KILL.**  All three cost-aware choosers score **−0.0426 of mean OOS Sharpe
   against doing nothing** (beat the anchor 4 of 12).  On U56 at the 10 bps bar they land on
   N=15/g=0.85 (full 19.44% / 1.1713 / **−22.58%**, OOS 21.56% / 1.1957) which **FAILS 4b on the
   drawdown cap alone**, while the do-nothing anchor N=20/g=0.75 (15.78% / 1.1522 / −19.13%, OOS
   17.28% / 1.1832) **PASSES**.  Buying return with gross and paying for it in drawdown is what a
   cost-adjusted Sharpe argmax does here.
9. **PROTOCOL grid:** 4a **0 of 420**; 4b **136 of 420** (U56 20/35 and B135 19/35 at 10 bps,
   **SMALL663 0 of 140 on every rung**).  Every 10-bps 4b failure on U56 and B135 binds on
   **MaxDD ALONE** (15 and 16 sole-DD; CAGR/OOS/H1/H2 sole-binder counts all zero) — the
   CHANGELOG diagnosis reproduces once more, now across the cost axis.
10. **PROPOSED PROTOCOL LINE (a proposal; PROTOCOL.md is NOT modified by this run).** *"A
    published crossing cost must state the swept range and the estimator.  Because cost enters
    the engine affinely, the estimator of record is the five-moment exact form (m_r, m_u, v_r,
    v_u, cov) from a single 0 bps run; a multi-rung sweep is a control, not evidence.  A c*
    outside the swept range is reported as NO CROSSING, never as a number."*

SURVIVORSHIP (rule 9): U56 and B135 are current-constituent lists, SMALL663 a current sub-$2B
screen (max_1d_move >= 1.0 dropped).  Every absolute level is optimistic and every 4b pass is an
upper bound.  ARM A is survivorship-neutral — it compares estimators of the same object on the
same books, so a level bias common to a panel cancels exactly.
