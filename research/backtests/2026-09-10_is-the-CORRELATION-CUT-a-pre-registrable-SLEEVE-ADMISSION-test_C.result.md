# Idea 650 — is the CORRELATION CUT a pre-registrable SLEEVE-ADMISSION test?  (lane C, 2026-09-10)

**VERDICT: KILL.** The ORDERING transfers; the THRESHOLD is not recoverable from the IS window;
applying the cut costs OOS Sharpe on 192 of 192 paired cells. Nothing promoted.

**Setup.** 618's ten sleeves (TRAIN) + **30 sleeves the record has never run** (TEST: 14 sector
ETFs, 3 credit, 4 commodity singles, 5 two-asset and 4 three-asset mixes, pre-registered by rule;
XLRE and XLC excluded and named for short history) x 2 panels x 2 books x 8 lambdas x 11 f, read at
6 rungs = **84,480 arm-rows / 160 cells**. The queue's two parameters are both swept in full: sleeve
set and a 41-point threshold ladder, every point reported. Weekly, t+1, gross 0.75, IS <= 2016-12-31.
INERT = no (lambda, f, rung) point in a cell's 48-point grid passes 4b.

**Gates.** All pass. G3 reproduces **all 40 of 618's cells** off its committed `.fits.csv` —
max|da0| **0.000e+00**, |dmean_w| 4.4e-16, |dn_empty| 0, |dsl_corr| 6.9e-17 — because the machinery
is imported from 618's file, not re-typed.

**H1 — the cut is NOT fittable on the IS window.** 618's 40/40 separation is a **full-sample** fact:
on 2009-2016 alone the classes OVERLAP (max `sl_corr_IS` among LIVE train cells **+0.8488**, min
among INERT **+0.6505**; AUC 0.895 IS vs **1.000 full**). The ladder's accuracy maximiser is
therefore tau in **[+0.85, +1.00]** (acc 0.950) — the **majority-class no-op**, not 0.50. It is not a
degenerate-label artefact: the IS label carries both classes at **6 of 6 rungs**, and the maximiser
is the no-op at all six.

**H2 / H3 (the ask) — it admits out of sample and NEVER rejects.** Carrying tau* = +0.925:
**TPR 0.000, TNR 1.000, balanced accuracy 0.500 in all six sleeve x window panels**; raw accuracy
falls 0.950 (TRAIN/IS) -> **0.283 (TEST/OOS)** purely on the base rate, which flips from 22.5% inert
to **71.7%** on the never-run sleeves. The predictor itself is stable (rho(corr_IS, corr_OOS)
**+0.934**, **0 of 80** pairs change side of tau*), so the failure is in the label, not the input.

**What DOES survive is the ordering.** AUC(`sl_corr_IS` -> inert_OOS) on the 120 never-run test
cells is **0.832**, against 618's own foil `sl_MaxDD_IS` at **0.274** (inverted). 618's published
0.50 cut — the number the IS window cannot produce — does admit and reject out of sample:
acc **0.750**, balanced **0.808**, TPR 0.674, TNR 0.941 (58/2/28/32). Its **28 false admits are one
named family**: every COMMOD cell (16/16 inert OOS at corr -0.02..0.43), plus LQD/TIP/HYG,
CRED2/CRED3, GDX. Out of sample a low correlation no longer buys a window (SECTOR 98% inert,
COMMOD 100%).

**KEEP paths.** 4a **55/84,480**, 4b **10,670/84,480**, **BOTH 12/84,480 — all at 0 and 5 bps; at
PROTOCOL's own 10 bps rung BOTH = 0**, the same shape as 403/613/618. At 10 bps COMMOD takes
**0 of 1,408** 4b passes and SECTOR **14 of 4,928**.

**Rule 8.** (sleeve, f) chosen on 2009-2016, 2017-2026 read once, 192 picks per selector.
tau* is a **no-op** (S_ADMIT identical to S_ALL, delta 0.0000 on 192/192). At the 0.50 cut ADMIT
**loses to REJECT on 192 of 192** paired cells (mean dSharpe **-0.1087**; test sleeves only
**-0.2417**), and loses to CASH by -0.1917. Best OOS at 10 bps is **S_CASH** — u56 **14.76% /
1.161 / -21.2%**, broad 13.95% / 1.026 / -24.4% — against SPY OOS 15.32% / 0.876 / -33.7% (u56) and
15.45% / 0.882 / -33.7% (broad), and RULES v2 OOS 9.48% / 1.279 / -12.1% (u56), 7.98% / 1.119 /
-12.2% (broad). **OOS 4a 0/192 for every selector**; OOS 4b 0/192 except S_IS4b 7 and S_REJECT50 28.

**PROTOCOL 3 reference arm** (u56 TOP20 + LQD f=0.25, lambda 1.00, 10 bps, pre-registered as the
modal test-admit pick, NOT chosen): 11.87% / 1.119 / -19.4%, H1/H2 1.374/0.957, OOS Sharpe 1.031 —
4b PASS full and OOS, **4a KILL** vs RULES v2 (8.63% / 1.202 / -12.1%). It is not promoted: rule 8's
own IS selector picks f=0.50 on this sleeve, not f=0.25, and that pick reads OOS Sharpe 0.819.

**What the record should say instead.** `sl_corr` ranks inertness on sleeves it has never seen
(AUC 0.832) and the sleeve's standalone drawdown does not (0.274) — 618's H2 conclusion stands. But
"`sl_corr > 0.5` classifies inert-vs-not 40/40" must be quoted as a **full-sample, ten-sleeve,
in-sample-fitted** statement: the IS window puts the maximiser at the no-op, the base rate moves 3x
between sleeve sets, and the cut is worth **negative** OOS Sharpe wherever it binds.

**Caveats carried.** Survivorship (idea 54) on both panels. SMALL439 excluded (prices no ETF).
Sleeve assets are also investable names in both panels (403/613/618's convention). Inertness is a 4b
label and inherits 4b's SPY comparand and its one-path MaxDD (idea 321). lambda can only lower
turnover. Idea 126: t+1, no lag band.

**Nothing promoted.** RULES.md, PROTOCOL.md, scan.py, bot.py, baseline.py untouched.
