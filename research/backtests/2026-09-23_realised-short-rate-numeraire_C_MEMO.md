# Memo — idea 2484 (lane C, 2026-09-23): the standing 4b candidate under the tape's own short rate

1. **The finding.** The committed CAP2 candidate keeps its 4b pass when Sharpe and CAGR are
   measured in EXCESS of the tape's own realised short rate (SHY), on BOTH panels, at 0 and
   10 bps — the rungs PROTOCOL actually binds. **No RULES change is proposed by this run.**
2. **Headline (U56, cap 2%, gross 0.75, weekly, 10 bps, EXCESS numeraire):** CAGR 10.15%,
   Sharpe 1.1046, MaxDD -16.19%, halves 1.1757 / 1.0463, OOS 10.83% / 1.1386.
   SPY EXCESS: 13.68% / 0.8053 / -35.17%, OOS 13.45% / 0.7820. Live RULES v2 EXCESS: 0.9853.
   B136: 10.34% / 0.9766 / -18.02%, halves 1.1505 / 0.8162, OOS 9.74% / 0.9231. 4b on both.
3. **The haircut is real and it is mechanical.** The convention costs the candidate -0.1640 of
   Sharpe and SPY only -0.0844 (net -0.0797), because the hit is `rf / sigma` and the candidate
   runs a 34.4% SHY sleeve at sigma 8.99% against SPY's fully-invested 17.5%. Predicted-vs-
   realised correlation +0.9956; the book is hit harder than the benchmark in 32 of 32 cells.
4. **The leg that breaks is `L_OOS`** (64/64 -> 56/64 record-wide), because SHY paid 0.81%/yr
   across the whole rule-8 IS window and 1.73%/yr out of sample — the free carry sits in the one
   sample rule 8 treats as honest.
5. **One committed claim dies:** the U56 headline's "survives 25 bps" stamp. Under EXCESS its
   CAGR floor misses by 0.0038 pp. Treat 10 bps as the candidate's true cost ceiling on U56.
6. **Rule 8 is not numeraire-stable:** TOTAL and EXCESS choosers agree on 4 of 16 triples; under
   EXCESS the picks defect from gross 0.75 to gross 1.00 in 11 of 16 and their full-sample 4b
   rate falls 12/16 -> 3/16. Any future rule-8 pick should state its numeraire.
7. **RULES wording, if a Sunday review ever adopts this candidate, is UNCHANGED from idea 2322's
   memo** — this run alters no clause. The only addition proposed is a REPORTING stamp:
   *"Every Sharpe and CAGR quoted for a book holding a cash or T-bill sleeve shall be reported in
   excess of the sweep instrument's own realised return, alongside the total-return figure."*
8. **Why this is a CONFIRM and not a KEEP:** the book is the standing candidate, already filed
   and already not recommended; this run adds a robustness stamp it did not hold and removes one
   it should not have held. 4a remains 0 of 64 under both numeraires (the live book's -12.05%
   MaxDD is unreachable by this family), so 4b is still the only live path.
9. **Caveat (rule 9):** U56/B136 are CURRENT constituents held from 2008, so every absolute CAGR
   is flattered and `L_CAGR` is the contaminated leg. The TOTAL-vs-EXCESS contrast is same-tape,
   same-weights and first-order immune to that bias; the absolute 4b verdicts are not.
10. **Reproduction:** `python research/backtests/2026-09-23_realised-short-rate-numeraire_C.py`,
    offline, 6s, 128 published rows, 12 of 12 gates, committed CAP2/CAND headlines to 4.98e-05.
