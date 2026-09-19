# Idea 1511 (lane cloud, 2026-09-19) — does a DOWNSIDE-ONLY VOLATILITY GATE beat the incumbent's TWO-SIDED vol20?

**ANSWERED — NO, ON EVERY ARM, AND THE IDEA'S PREMISE IS FALSE BEFORE THE GATE STATISTIC IS EVEN
CHANGED. KILL. ONE METHOD FINDING THAT INVALIDATES A WHOLE CLASS OF DRAWDOWN CLAIMS. NO RULES
CHANGE PROPOSED.**

## What was run
Four gate statistics on the frozen 2026-09-04 KEEP-4b incumbent (N = 20, H = 126, gross 0.75, 200d
MA gate, weekly Fri-decide / Mon-trade, 10 bps, t+1): **VOL** (the incumbent's own two-sided
`std * sqrt(252)`, the control), **SEMI0** (`sqrt(mean(min(r,0)^2))`), **SEMIM**
(`sqrt(mean(min(r-mu,0)^2))`) and **UPM** (`sqrt(mean(max(r-mu,0)^2))`, **the placebo**). SEMIM and
UPM are an exact decomposition of the control: gate **G10 asserts SEMIM^2 + UPM^2 = VOL^2 * (w-1)/w
pointwise to 2.8e-14** (the factor is pandas' `ddof=1` in the incumbent's own rolling std, which
VOL must keep — it is why G2 is bit-identical). Two dials: **window w {10, 20, 40, 60}** and
**target pass rate q {0.70, 0.80, 0.90, p*, 1.00}**, each cell's threshold being the q-quantile of
*its own* statistic over the **in-sample priced cells only** and applied unchanged to 2017-2026.
4 x 4 x 5 = **80 cells per panel, 240 in all on U56 / B136 / SMALL, every one published.**
All **11 gates pass**: G1 replays the committed U56 anchor to **3.7e-05**, G2 shows the
VOL / w=20 / q=p* cell recovers a threshold of **exactly 0.600000** and is **bit-identical
(0.000e+00)** to the frozen incumbent, G8 matches every pass rate to **3e-05**.

## (0) THE PREMISE IS FALSE: THE INCUMBENT'S GATE BARELY BINDS
The incumbent's own pass rate p*, measured as the in-sample share of priced name-days with
`vol20 < 0.60`, is **96.68% (U56), 96.84% (B136), 88.13% (SMALL)**. The screen the idea set out to
improve excludes **3.3% / 3.2% / 11.9%** of name-days. Removing it **entirely** (q = 1.00, same
window) costs U56 **0.0176 of Sharpe at t -0.37** while *adding* 0.08 pp/yr of CAGR, and on SMALL
it **improves** Sharpe by **+0.1075** and drawdown by **+4.51 pp**. A dial that barely turns cannot
be improved by relabelling it, and the run should be read in that light.

## (1) THE DRAWDOWN LEG DOES NOT WIDEN — PRE-REGISTERED B1 FAILS
At the matched pass rate, mean dMaxDD of SEMI0 against its VOL control at the same window:
**U56 +0.61 pp, B136 +0.74 pp**, both short of the pre-registered +1.0 pp bar on both panels
(**B1 FAIL**). SEMIM is *worse* than the control on U56 (**-0.39 pp**) and B136 (**-0.13 pp**). Only
SMALL shows a real SEMI0 drawdown gain (**+3.00 pp**) — and it buys it with **-0.0099** of Sharpe
and **-0.38 pp/yr** of CAGR, on the panel where nothing passes 4b anyway (0 of 80).

## (2) THE PLACEBO KILLS THE STORY
Screening on **UPSIDE** dispersion does what screening on downside dispersion does. Mean dMaxDD vs
the control: U56 **downside +0.11 pp vs upside +0.25 pp** (the placebo WINS), B136 **+0.31 vs
+0.12**, SMALL **+1.64 vs +0.61**. Mean dSharpe: U56 **+0.0015 vs +0.0020** (placebo wins again),
B136 **-0.0020 vs -0.0132**, SMALL **-0.0099 vs +0.0023** (placebo wins). **The word "downside" is
doing no work**: what little these gates do, they do by being a dispersion screen at a given pass
rate, not by which tail they read.

## (3) THE METHOD FINDING — THE DRAWDOWN LEG IS NOT MEASURABLE AT THIS SAMPLE LENGTH
**0 of 240 cells reach |t| > 2 on dMaxDD against the frozen incumbent** (max |t| anywhere
**1.72**). The paired circular-block bootstrap SE of the drawdown contrast averages **2.93 pp** —
**2.7x the anchor's ENTIRE 1.10 pp 4b drawdown margin** (-19.13% against a -20.23% cap). Realised
MaxDD spans **4.66 pp (U56), 8.63 pp (B136), 8.94 pp (SMALL)** across the 80 cells of each panel.
**Any claim in the record that a device moved the binding 4b drawdown leg by less than ~3 pp is
inside its own SE and is not a finding.** This is the third independent convention now shown to
swamp that leg (after idea 1409's lookback and idea 1515's single-day clip), and unlike those two
it is a statement about the leg's *resolvability*, not about a particular dial.

Of the **6 cells in all 240 that resolve at |t| > 2 on dSharpe, 5 are NEGATIVE** (U56
VOL/w10 -0.0852, VOL/w40 -0.1091, **SEMIM/w20 -0.0775 at t -2.84**, UPM/w40 -0.1132 and -0.0899);
the single positive is B136 SEMIM/w10/q0.90 (+0.0959, t +2.26) and it does not survive rule 8.

## (4) BOTH KEEP PATHS AT ALL 240 CELLS
**4a 0 of 240 full and 0 of 240 OOS** — another consecutive 4a zero. **4b 59 full / 58 OOS / 58
BOTH**: U56 43 of 80 (VOL 10, SEMI0 11, SEMIM 9, **UPM 13** — the placebo produces the MOST 4b
passes), B136 16 of 80 (SEMI0 7, VOL 3, SEMIM 3, UPM 3), **SMALL 0 of 80**. **The binding leg is
DRAWDOWN on both surviving panels** (U56 43/80, B136 17/80) while H1, H2 and the CAGR floor pass
80/80 and 80/80 on U56 — exactly the standing CHANGELOG finding. **Sorted by OOS Sharpe, the best
4b-BOTH cell in all 240 IS the frozen incumbent itself** (1.1857); the best challenger is
UPM/w60/q0.80 at 1.1832, i.e. the placebo.

## (5) RULE 8 — PRE-REGISTERED B3 FAILS ON ALL THREE PANELS
Both dials and every threshold fitted on warm-up..2016-12-31; 2017-2026 read once. The
downside-only chooser picks U56 SEMIM/w10/q0.80 -> OOS **14.88% / 1.0937 / -21.51%** vs the anchor's
**17.32% / 1.1857 / -19.13%**; B136 SEMIM/w20/q0.80 -> **13.19% / 0.8859 / -22.63%** vs
**16.19% / 1.0180 / -20.74%**; SMALL SEMI0/w10/q0.70 -> **5.24% / 0.3790 / -33.14%** vs
**6.70% / 0.4398 / -36.51%**. **It loses on OOS Sharpe on 3 of 3 panels, and on OOS CAGR on 3 of 3,
by 2.44 / 3.00 / 1.46 pp/yr.** The all-cells chooser loses too (U56 1.0937, B136 1.0459 vs 1.0180 —
one win — SMALL 0.3452 vs 0.4398). Doing nothing wins.

## Verdict
**KILL.** B1 FAIL, B2 PASS (and 5 of its 6 resolved cells run the wrong way), B3 FAIL on 3 of 3
panels. The premise is false at the outset (the incumbent's screen passes 96.7% of U56 name-days),
the upside placebo matches or beats the downside statistic on every currency, no cell in 240
resolves on the drawdown leg the idea targeted, and nothing in the grid beats the frozen incumbent
out of sample. **The useful residue is (3)** — the 4b drawdown leg carries a ~2.93 pp standard
error against a 1.10 pp margin, so it cannot adjudicate any device of this size, whatever the
device is.
