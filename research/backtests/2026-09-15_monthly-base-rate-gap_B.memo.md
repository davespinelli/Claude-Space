# Memo — idea 926 — PARK, not KEEP (lane B, 2026-09-15)

1. **The book.** `U56/M/CORE/TOP20`: top-20 by the `scan.py` composite with no vol scaler, equal
   weight, gross 0.75, **monthly** rebalance, 10 bps, next-day execution.
2. **It clears 4b twice.** Full sample **14.69% / 1.203 / −19.51%** (halves 1.216 / 1.198);
   rule-8 OOS 2017–2026 **16.67% / 1.283 / −19.51%**. SPY 15.13% / 0.885 / −33.72% (OOS
   15.27% / 0.874 / −33.72%); RULES v2 live 8.62% / 1.201 / −12.05% (OOS 9.46% / 1.277 / −12.05%).
3. **4a FAILS** (−19.51% against the live book's −12.05%), as every growth book in the record does.
4. **PARK, disqualified by this run's own headline:** its gross-matched coin-flip null clears the
   identical 4b bar at the identical cost **40.5% of the time** (400 draws, gross match 0.0000).
5. Its weekly twin — same rule, same gross, same gate — has a base rate of **0.0%**. The
   difference is cadence, not selection.
6. **No IS-only chooser reaches it.** Rule 8, cadence free: CH_ANYCAD is **0 of 18** OOS-4b and
   picks `Q/EXT/TOP5` (OOS 11.94% / 0.550 / −38.48%). This book is visible only with hindsight.
7. **Wording it would need IF the base-rate leg were ever cleared** (NOT proposed for Sunday
   review): `RULES v3 clause 1 — hold the top 20 names by the v1 composite computed WITHOUT the
   volatility scaler, equal weight at 0.0375 of NAV each (gross 0.75), rebalanced on the last
   trading day of each month, orders at the next open; gated-out weight goes to CASH.`
8. **Blocking condition for any future promotion:** the cell's own monthly null base rate must
   read ≤ 0.05 at 10 bps. Today it reads 0.405, so the clause is not met and no draft is filed.
9. **Survivorship (PROTOCOL 9):** U56 is a current-constituent list, so the 14.69% is optimistic
   and the 40.5% is an **upper** bound on the null — the disqualification is the conservative leg.
10. **Nothing promoted. No RULES.md, PROTOCOL.md, scan.py, bot.py or baseline.py change.**
