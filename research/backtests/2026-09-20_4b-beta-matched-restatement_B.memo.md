# Idea 1719 result memo (lane B, 2026-09-20) — NOT a KEEP memo; no new book

1. **Question.** Idea 1705 found the 4b CAGR floor binds at 61–78 of 80 cells and binds from below
   on gross. Is a 4b pass therefore borrowed beta? Restate each published 4b pass against its own
   realised-beta-matched SPY blend (`blend_t = b·spy_t`, remainder in cash at 0%).
2. **Answer: NO.** 11 of 11 FULL passes and 13 of 13 OOS passes clear the strict alpha test
   (Sharpe > own blend in both halves / OOS **and** CAGR > own blend). Mean alpha CAGR **+4.67 pp/yr**
   (full-window beta) and **+3.21 pp/yr** (252d rolling beta); mean beta 0.505 / 0.602; OOS alpha
   range **+3.67 to +6.17 pp/yr** over betas 0.357–0.643. Zero passes fail the restated CAGR floor.
3. **But the restatement is defective, and that is the second finding.** Its three legs move in
   three directions: Sharpe is **exactly** beta-invariant (gated 2.220e-16 over b∈0.2–1.3), the CAGR
   floor loosens by ~b and the DD cap tightens by ~b. So 0 of 11 / 0 of 13 pass the *mechanical*
   restated 4b and **every failure is the DD leg alone** (margins -2.09 to -9.02 pp). The 0.60×
   cap is already a de-levering bar; on a de-levered benchmark it charges beta twice. **Do not put
   a beta-matched restatement into PROTOCOL rule 4b.** The clean bar is the alpha test in line 2.
4. **Against SPY-at-100% the floor is a GROSS bar on the cells that fail and an ALPHA bar on the
   cells that pass:** 83 of 96 FULL cells and 82 of 96 OOS cells fail it (DD cap 5 / 5), and those
   are the low-gross cells — but the 11 / 13 that clear it clear it on alpha.
5. **Capital arm (rule 8, IS = 2009-2016 only, 2017-2026 read once).** U56: both choosers pick
   BAND c=0.10 G=1.00 → OOS 12.14% / 1.1938 / -16.30%. B136: argmax-IS-Sharpe picks VOLTGT t=0.12 →
   OOS 13.86% / 1.2217 / -16.01%; **argmax-IS-alpha picks worse** (BAND c=0.10 G=1.00, OOS 11.02% /
   1.0873 / -19.20%: -0.134 Sharpe, -2.84 pp CAGR, 3.19 pp deeper). SMALL: no IS candidate at all.
   **KILL the alpha chooser as a selection rule.** Bars: SPY OOS 15.26% / 0.8737 / -33.72%;
   RULES v2 OOS 9.46% / 1.2766 / -12.05% (U56), 7.85% / 1.1017 / -12.24% (B136). 4a fails at every pick.
6. **Incidental, and it bites the standing KEEP-4b candidate.** The panel VOL-TARGET book's alpha
   does not replicate on SMALL: **-1.42 / -2.38 / -2.94 pp/yr** of beta-matched OOS alpha at
   t = 0.08 / 0.12 / 0.16 (OOS Sharpe 0.477 / 0.477 / 0.501), 0 of 3 rungs clear 4b-vs-SPY, against
   +4.68 to +6.17 pp/yr on U56 and B136. The VOLTGT memo's own "not tested on SMALL" caveat is now
   tested, negatively. This does not retract that candidate on U56/B136; it bounds it.
7. **Grid.** 96 books × 4 cost rungs × 3 panels = 384 published cells; families BAND c∈{0.00,0.03,
   0.05,0.10} × G∈{0.30,0.50,0.75,1.00}, MAXVOL m∈{0.40,0.60,0.80} × G, VOLTGT t∈{0.08,0.12,0.16},
   RULES v1. Two tuned parameters only: beta window ∈ {full, roll252} and claim set ∈ {FULL, OOS};
   both values of both are published. 10 bps is the binding rung; 0/25/50 bps reported.
8. **Cost robustness.** Published 4b passes 15 / 11 / 8 / 5 (FULL) and 15 / 13 / 11 / 6 (OOS) at
   0 / 10 / 25 / 50 bps; restated 4b 0 at every rung; strict alpha passes 15 / 11 / 8 / 5 and
   15 / 13 / 11 / 6 — the alpha result is unchanged across the whole cost axis.
9. **Gates 14/14.** fast_run == `engine.backtest` 0.000e+00 (returns and turnover) on all three
   panels; derived cost axis exact 0.000e+00; U56 BAND c=0.03 G=0.75 replays
   `baseline.rules_v2_weights` to 0.000e+00 (that cell IS the live book); blend(b=1) == SPY
   0.000e+00; IS stats and IS alpha identical on a hard-truncated tape (no chooser reads a 2017+
   row); max realised gross 1.000000, no shorting, no leverage; 384 of 384 cells published.
   Deterministic, offline, 34s.
10. **Survivorship (rule 9).** U56, B136 and the sub-$2B SMALL screen are CURRENT constituents, so
    every ABSOLUTE level here — including all 11 / 13 published 4b passes — is an **UPPER BOUND**.
    The book-minus-own-blend contrast is inside one frame on the same days and is first-order
    immune. **RULES.md / scan.py / bot.py / baseline.py are NOT modified by this run** (rule 6).
