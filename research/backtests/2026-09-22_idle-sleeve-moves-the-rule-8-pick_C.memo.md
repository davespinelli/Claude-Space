# PARK memo — idea 2217, lane C, 2026-09-22 (KEEP-**4a** candidate, RECORDED NOT RECOMMENDED)

1. **What it is.** The RULES v2 band book at band 0.08 and gross 0.50, with its idle NAV
   (`1 − Σw`, here ~60% of NAV) swept into **SHY** instead of held at 0% cash. Long-only, total
   weight exactly 1.00, no leverage, weekly, t+1, 10 bps. Two tuned dials (band, gross); the sweep
   fraction phi = 0.00 is a published arm, not a fitted parameter; all 25 grid points reported.
2. **What rule 8 reaches** (argmax IS Sharpe, 2009–2016 only, both panels agree): **c 0.08 / g 0.50**.
   U56 FULL 6.51% / **1.3084** / **−8.92%** (halves 1.3619/1.2719), OOS 7.12% / 1.3576 / −8.92%.
   B136 FULL 6.49% / 1.2761 / −9.17% (1.3908/1.1708), OOS 6.60% / 1.2912 / −9.17%.
3. **Why it passes 4a where 15 months of ladder work passed 0 of 25:** it beats the live book's
   Sharpe in both halves on both panels with 3.1–3.3 pp *less* drawdown, at 15/15 (U56, ≤25 bps)
   and 20/20 (B136, incl. 50 bps) offset x cost cells.
4. **Why it is NOT recommended.** Re-scored against the live cell *of its own arm* (same sweep on
   both sides, so only band x gross is priced) it holds 17/20 on U56 FULL but **0 of 20 on U56
   OOS**, while B136 keeps 16/20 — one panel passes, one fails. Its 4a edge over the *unswept*
   incumbent is therefore largely the cash credit the comparand is denied, not a book fact.
5. **It fails 4b outright** (OOS CAGR 7.12% against a 10.70% floor), so it is not capital-worthy
   under the path PROTOCOL says matters; it is a lower-return, lower-risk book than the live one.
6. **Exact RULES wording if a Sunday review ever adopts it** — clause 2's band constant
   `1.03 / 0.97` becomes `1.08 / 0.92`, and clause 4 is replaced by:
   > 4. **Sizing:** each IN name is held at `0.50 / N` of current NAV. Names that are OUT are not
   > held. The NAV not held in IN names — `idle = 1 − 0.50 * (IN / N)` — is **swept into SHY, not
   > left in cash**, and reset on the same weekly schedule as clause 5. The book is therefore
   > always 100% invested and never levered.
7. **The cheaper, separable half of this result**, and the one worth testing next: applying the
   SHY sweep to the **live cell as it stands** (band 0.03, gross 0.75) is worth +0.50 pp CAGR and
   +0.067 Sharpe on U56 FULL, **passes 4a at d = 0 but flickers across weekday offsets at 10 bps
   and dies at 25 bps on both panels** — inside its own scheduling noise, so not adoptable either.
8. **Do not adopt without**: an idle-NAV-matched 4a that holds on BOTH panels OOS, a 25 bps pass at
   the live cell, a real brokerage sweep rate (SHY total return at adjusted closes is an upper
   bound on what a cash sweep actually pays), and ≥ 8 weeks of live tracking (PLAN Tier 3).
9. **Survivorship (rule 9):** U56/B136 are current-constituent panels; all levels are optimistic.
10. RULES.md / PROTOCOL.md / scan.py / bot.py / baseline.py were not touched by this run.
