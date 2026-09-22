# PARK memo — idea 2221, lane B, 2026-09-22 (KEEP-4b candidate, RECORDED NOT RECOMMENDED)

1. **What it is.** RULES v2's band book with its idle NAV invested instead of held at 0% cash:
   a BENCH sleeve of `phi*SPY + (1-phi)*SHY`, phi = 0.25. Long-only, total weight exactly 1.00,
   no leverage. Two tuned params (phi, band c); all 25 grid points published.
2. **The candidate rule 8 actually reaches** (argmax IS Sharpe among IS-4b passers, 2009-2016 only):
   **B136 / phi = 0.25 / c = 0.08** — OOS 11.01% / 1.1399 / -17.34%, FULL 11.06% / 1.1520 / -17.34%,
   IS 11.11% / 1.1668 / -10.48%. 4b PASS in FULL, IS and OOS; 5 of 5 weekday offsets; 0/10/25 bps.
3. **Why it is NOT recommended.** 4b FAILS at 50 bps; 4a is 0 of 30 cells; the same chooser on U56
   picks phi=0.50/c=0.08 and fails the DD cap OOS (-22.06% vs -20.23%) at 5 of 5 offsets — one panel
   passes, one fails, so the chooser is a coin flip. B136 is also survivorship-optimistic (rule 9).
4. **Exact RULES wording if a Sunday review ever adopts it** — replace clause 4's last sentence:
   > 4. **Sizing:** each IN name is held at `0.75 / N` of current NAV. Names that are OUT are not
   > held. The NAV not held in IN names — call it `idle = 1 - 0.75 * (IN / N)` — is **invested, not
   > left in cash**: `0.25 * idle` in SPY and `0.75 * idle` in SHY, reset on the same weekly
   > schedule as clause 5. The book is therefore always 100% invested and never levered.
   and clause 2's band constant `1.03 / 0.97` becomes `1.08 / 0.92` for the B136-reached cell.
5. **Do not adopt without**: a second panel agreeing on the same (phi, c), a 50 bps pass, and >= 8
   weeks of live tracking (PLAN Tier 3). RULES.md / PROTOCOL.md / scan.py / bot.py / baseline.py
   were not touched by this run.
