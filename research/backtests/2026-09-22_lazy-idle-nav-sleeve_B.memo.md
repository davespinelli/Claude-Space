# KEEP-4a candidate memo — idea 2231, lane B, 2026-09-22 (lazy idle-NAV sweep)

1. **What it is.** RULES v2's band book, unchanged, with its idle NAV swept into SHY instead of
   held at 0% cash — but the sweep is rebalanced **lazily**: the sleeve is left alone unless its
   weight differs from the target idle share by more than `h = 0.10`, or unless leaving it would
   push total weight above 1.00. Two tuned params (tolerance h, sleeve mix phi); all 21 cells x
   5 cost rungs x 3 windows x 2 panels published in `.grid.csv`.
2. **KEEP path: 4a** (Sharpe > live rules in both halves, MaxDD no worse). FULL, 10 bps:
   U56 **9.13% / 1.2692 / -11.53%** vs live **8.62% / 1.2010 / -12.05%**; B136 **8.50% / 1.1704 /
   -11.68%** vs live **7.96% / 1.0972 / -12.24%**. 4a passes on BOTH panels at 0/5/10/25 bps and
   on U56 also at 50 bps. It is 4b FAIL everywhere on the CAGR floor alone (OOS -0.55 pp U56).
3. **Rule 8 (2017-2026 read once).** Argmax IS Sharpe and argmax IS Sharpe among IS-4a passers
   BOTH pick phi = 0.00 / h = 0.10 on BOTH panels. OOS: U56 **10.15% / 1.3577 / -11.53%** and
   B136 **8.61% / 1.1955 / -11.68%**, each beating the live book on CAGR, Sharpe AND MaxDD
   (9.46% / 1.2767 / -12.05%; 7.85% / 1.1017 / -12.24%). SPY OOS 15.29% / 0.8751 / -33.72%.
4. **Why lazily and not eagerly.** The eager sweep (h = 0) is idea 2213's; it fails 4a at 50 bps
   on both panels. h = 0.10 retains **102.8% / 105.0%** of its Sharpe gain for **63.7% / 65.3%**
   of its turnover lift (2.43x / 2.68x per year against the eager 2.80x / 3.04x and the live
   1.77x / 2.01x), and the skipped trades cost tracking error worth less than their own cost.
5. **Exact RULES wording if a Sunday review adopts it** — replace clause 4's last sentence:
   > 4. **Sizing:** each IN name is held at `0.75 / N` of current NAV. Names that are OUT are not
   > held. The NAV not held in IN names — call it `idle = 1 - 0.75 * (IN / N)` — is **swept into
   > SHY**, with a **no-trade tolerance**: on the weekly rebalance the SHY sleeve is traded only
   > if the difference between its current weight and `idle` exceeds **0.10** of NAV, or if
   > leaving it would take total weight above 1.00. The book is never levered and never short.
6. **Do not adopt without**: the 5-offset weekday spread this run did not measure (ideas
   914 / 2111 make it binding), a 50 bps pass on B136 (it needs h = 0.50 there), and >= 8 weeks of
   live tracking (PLAN Tier 3). Note the sleeve is a REAL bond allocation: SHY 2022 **-3.88%**,
   IS CAGR 0.81% vs OOS 1.72%, so the measured gain is partly a rate-regime fact (idea 2227).
7. RULES.md / PROTOCOL.md / scan.py / bot.py / baseline.py were NOT touched by this run.
