# PARK memo — `SINGLE20/VT` (idea 924, lane C, 2026-09-15). **BLOCKED, NOT A KEEP.**

1. **The book.** U56's 20 `megacap` single names only, equal weight, weekly, gross scaled so the
   book's trailing-60d vol matches SPY's and never levered: `w_i = min(1, σ60(SPY)/σ60(EW)) · g/20`.
2. **What it does.** g=0.75: FULL 18.84% / 1.391 / −19.13% (halves 1.493 / 1.303), OOS 18.54% /
   1.357 / −19.13%, against SPY FULL 15.13% / 0.885 / −33.72% and OOS 15.27% / 0.874 / −33.72%.
3. It clears **PROTOCOL 4b on FULL, IS and OOS**; at g=0.45 it also clears **4a** on FULL and OOS.
4. **Exact RULES wording it would need** (recorded for the audit trail, **not proposed**):
   *"Hold the 20 names of `universe.json:megacap` at equal weight, rebalanced weekly, at gross
   min(1, σ60(SPY)/σ60(book)) × 0.75 of NAV; the ungrossed remainder is CASH."*
5. **Why it is blocked (1).** The name list is the 2026 mega-cap ranking applied from 2009. It is an
   answer key, not a rule; idea 924 measures 80% of the sleeve's edge as name selection (+0.2958 of
   Sharpe in the leg window, +0.5750 on FULL) against RSP, the survivorship-free comparand.
6. **Why it is blocked (2).** **Rule 8 reaches it 0 of 10 times.** Every IS-only chooser takes
   `SINGLE20/EW` at the top of the gross ladder instead and fails the OOS DD cap (−31.82% vs −20.23%).
7. **Why it is blocked (3).** On the same 480-cell grid, the survivorship-free sleeves (`EQETF24`,
   `ETF36`, `NONEQ12`, `SPYONLY`) clear 4b **0 times in any window at any gross**.
8. **What would unblock it.** A vintage-honest constituent rule that picks the 20 names from data
   available at each rebalance (filed as 934). Until that exists this book has no ex-ante form.
9. **Cost.** Leg-window edge moves +0.2072 → +0.1744 across 0 → 50 bps; the book is not fragile to
   the rung, which is exactly why the rung is not what is wrong with it.
10. **Status: PARK.** No RULES change, no PROTOCOL change, no version bump, nothing for Sunday
    beyond the reporting question in 933.
