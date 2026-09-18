- 2026-09-18 (lane cloud, idea 1313 do-SELECTION-and-EXPOSURE-STACK-at-SMALL-s-DD-CAP)
  — **VERDICT: KILL on the queue's own question (the stack does NOT open SMALL's -20.23% 4b
  drawdown cap) — plus a KEEP-4b PASS on U56 and B136 that neither instrument earns alone**
  (memo written). SELECTION: 1313 is the FIRST numbered item standing in '## Open'; price-only,
  no eligibility descent taken. No RULES change, no PROTOCOL edit (rule 6); RULES.md,
  PROTOCOL.md, scan.py, bot.py and baseline.py untouched. Offline, deterministic, 22.4s.

  **THE INSTRUMENT.** 1297's scaler k_t = min(0.60, TARGET / v_t) applied ON TOP OF 1301's
  selection cell instead of the incumbent, v_t the annualised sd of the SELECTION book's own
  constant-gross returns over the 21 rows ENDING AT t-1 (rule 2). Two dials, N {15,20,30,40} x
  TARGET {6,8,10,12}%; H=63, WINDOW=21, CAP=0.60, cadence W and 10 bps FROZEN at values ideas
  1301 and 1297 certified before this run. 16 stacked cells + 4 selection-only + 4
  exposure-only + the frozen anchor per panel, **all published**, on U56 / B136 / SMALL663,
  plus a 48-book recursive B_SELF robustness arm. Gates G0-G5 PASS, including 1301's
  selection claim (+4.66 pp MaxDD / +0.70 pp CAGR) and 1297's exposure claim (-22.70% at 6%/21d).

  **1. SMALL: THE CAP IS BOUGHT, THE FLOOR IS WHAT BUYS IT.** 3 of 16 stacked cells clear the
  -20.23% cap — which NEITHER instrument alone ever did (1297 reached -22.43%, 1301 -28.69%) —
  the shallowest at N=30/6% reaching **-18.69%**. But every one of them lands at 5.32-5.47%
  CAGR against a **9.84% floor**, so **0 of 16 clear both legs, full sample AND OOS**. The
  13.12 pp gap the queue named is closed on drawdown and reopened on return. 4a is 0/48.

  **2. THE INTERACTION'S SIGN IS A PANEL FACT.** resid = dMaxDD(stack) - [dMaxDD(sel) +
  dMaxDD(exp)] against the same anchor: **U56 +3.19 pp mean (0/16 substituting), B136 +6.57 pp
  (0/16), SMALL663 -1.07 pp with 8 of 16 SUBSTITUTING**. The two instruments compose
  super-additively exactly where the DD leg is already slack and sub-additively where it binds.
  Any future 'selection and exposure compose' claim must name its panel.

  **3. U56 / B136: A REAL 4b PASS THE STACK EARNS.** Best U56 cell N=15/6%: **11.81% / 1.2290 /
  -10.66%** (H1 1.294 / H2 1.172, turnover 3.79x/yr) vs SPY 15.13% / 0.8849 / -33.72% and the
  frozen anchor 13.66% / 1.1706 / -16.38%. It is the super-additive cell (resid +6.13 pp):
  selection alone at N=15/H=63 makes drawdown WORSE (-21.22%, 4b FAIL) and exposure alone
  reaches only -11.95% at a bigger CAGR cost. 4b passes 11/16 on U56 (full and OOS) and 14/16
  full / 12/16 OOS on B136.

  **4. RULE 8 (2017-2026 READ ONCE).** (N, TARGET) by argmax IS Sharpe on warm-up..2016-12-31.
  Picks U56 N=15/6%, B136 N=15/10%, SMALL N=40/8%. U56 OOS **12.31% / 1.2444 / -10.66%** vs SPY
  OOS 15.28% / 0.8747 / -33.72% (cap -20.23%, floor 10.69%), anchor OOS 15.12% / 1.1947 /
  -16.38% and RULES v2 OOS 9.47% / 1.2781 / -12.05% — **+0.0497 of OOS Sharpe and +5.72 pp of
  OOS MaxDD for -2.81 pp of OOS CAGR**, a bigger Sharpe gain than 1297's exposure-only OOS
  winner bought (+0.0166 for -1.54 pp) at a bigger price. B136's pick is OOS-flat against its
  anchor (-0.0081); SMALL's is negative on every leg (-0.0371 Sharpe, -2.01 pp CAGR). B_SELF
  agrees on direction (same U56 pick, +3.37 pp OOS MaxDD, -0.0076 Sharpe).

  **THE HONEST CAVEAT.** Every U56/B136 pass is bought with CAGR; this is a drawdown-for-return
  trade an operator must WANT, not a dominance over the frozen incumbent.

  **SURVIVORSHIP (rule 9).** U56 / B136 / SMALL663 are current-constituent lists; SMALL663 is a
  sub-$2B screen carried back to 2010, so every absolute SMALL number is biased UP — which makes
  the SMALL KILL stronger, not weaker.

