# PARK memo — idea 2077 (lane C, 2026-09-22): the UN-DE-GROSSED band book

1. **The cell.** U56, band 0.03, weekly, 10 bps, **gross 1.00** — the live RULES v2 book with
   the de-gross removed and nothing else changed. FULL 11.53% / Sharpe 1.201 / MaxDD −15.91%;
   OOS 12.67% / 1.101-1.28 class; SPY 15.14% / 0.885 / −33.72%.
2. **It clears 4b on FULL and OOS** (Sharpe > SPY both halves, MaxDD −15.91% vs a −20.23% cap,
   CAGR 11.53% vs a 10.60% floor), on the one panel, at all six financing models.
3. **It is the only weekday-robust cell in the run.** DD margin +4.32 pp against a 2.40 pp
   5-offset spread, CAGR margin +0.93 pp against 0.54 pp, 4b holds at **5 of 5** offsets —
   it passes idea 914's clause outright, which the levered rung does not.
4. **Financing cannot touch it**: borrowed NAV is identically zero at gross <= 1.00 (gate G2).
5. **But rule 8 cannot reach it.** IS (2009–2016) CAGR **10.16%** against the IS 4b floor of
   **10.47%** — illegal for a 2016 chooser by **31 bps**. It is an out-of-sample fact, not a
   choosable rule, so it is PARK and not KEEP.
6. **It is also not 4a**: MaxDD −15.91% is worse than the live book's −12.05%, so it cannot
   replace RULES v2 on the beat-the-book path. Both paths were evaluated; neither is met.
7. **On B136 it fails** (OOS CAGR 10.47% vs a 10.68% floor), so it is single-panel.
8. **What would make it a KEEP:** a legal IS-only chooser that reaches gross 1.00 without
   hindsight, verified on BOTH panels, with the DD margin still exceeding its offset spread.
   No such chooser is claimed here.
9. **Exact RULES wording IF it ever clears those bars** (not proposed for adoption now):
   *"Hold every name inside the 200d +/-3% band at 1.00/N of NAV, N = instruments priced that
   day; gated-out weight goes to CASH. Rebalance weekly."* — i.e. RULES v2 clause 2 with
   `gross = 1.00` in place of `0.75`, no other clause touched.
10. **Standing caveat:** survivorship (current constituents), single panel, and the record's
    0%-on-idle-NAV convention — which B7 shows is load-bearing for the de-grossed book's own
    4b standing at high rates. No rules change is requested this run.
