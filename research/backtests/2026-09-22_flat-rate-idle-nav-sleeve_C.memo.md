# QUALIFICATION memo on the standing KEEP-4a candidate — idea 2227, lane C, 2026-09-22

1. **What this is.** Not a new book. Idea 2231's lazy idle-NAV sweep (RULES v2 band book, idle NAV
   into SHY at `phi = 0`, no-trade tolerance `h = 0.10`) stays the deployable object and keeps its
   own memo. This run re-prices that same sweep against a **FLAT-RATE counterfactual sleeve**
   (idle NAV earns a constant `y` per year instead of SHY's realised path), `y` on a 9-rung
   ladder, and it changes what the candidate's margin may be claimed to rest on.
2. **The level is NOT a rate-regime artefact.** The gain is exactly mechanical and linear in `y`:
   `d(dCAGR)/dy = +0.4770` (U56) / `+0.4747` (B136), **R2 = 0.99998**, intercept -0.07 pp, ratio to
   the mean sleeve share (0.445) of 1.06-1.08. SHY's whole 2009-2026 path is worth a flat
   **1.216% (U56 FULL) / 1.290% (B136 FULL)** — the LOW end of any plausible cash rate, so the
   record's +0.50 pp is understated against normal short rates, not inflated.
3. **The window asymmetry 2227 named is real but small.** SHY's gain is `+0.30 pp IS` vs
   `+0.70 pp OOS` (U56) and `+0.28` vs `+0.76` (B136); a flat rate shows `+0.00 / +0.02 pp` of
   OOS-minus-IS. So essentially **all** of that 0.40-0.47 pp surplus is the rate path — but the
   surplus itself is under half a point of CAGR, not the whole credit.
4. **What IS an artefact, and it binds: the 4a pass at 25 and 50 bps.** The 4a frontier in `y` is
   exactly linear in cost — **`y >= 0.081% per bp` (U56) / `0.089% per bp` (B136)**, by bisection
   with each `y` a fresh pricing: `0.81% / 0.89%` at 10 bps, `2.03% / 2.23%` at 25, `4.10% / 4.50%`
   at 50, **identical in FULL and OOS**. A flat sleeve at SHY's own equivalent rate therefore
   **FAILS 4a at 25 bps on both panels**, and it fails on the **DD leg** (`dMaxDD -0.02 / -0.03 pp`)
   while both Sharpe legs stay positive (`dH1 +0.042 / +0.038`, `dH2 +0.037 / +0.038`).
5. **Where 2231's 25/50 bps pass comes from.** SHY at 25 bps reads `dH1 +0.0368`, `dH2 +0.0709`,
   `dMaxDD +0.50 pp` — the pass is bought by **bond duration handing back drawdown**, not by the
   cash yield. Duration contributes almost nothing to Sharpe (`+0.0015 FULL`, `-0.0064 OOS` against
   the CAGR-matched flat arm) and the entire benefit is that `+0.51 / +0.55 pp` of MaxDD.
6. **Rule 8, 2017-2026 read ONCE.** Argmax IS Sharpe and argmax IS Sharpe among IS-4a passers both
   pick the ladder top `y = 5.0%` on both panels (IS Sharpe is monotone in `y`), which is a
   **sensitivity, not a strategy** — nobody picks next decade's cash rate. The rate-assumption-free
   arm TRAIL (sleeve credited the trailing 252-day realised SHY return, lagged one day) reads OOS
   **U56 9.99% / 1.3425 / -11.96%** and **B136 8.48% / 1.1834 / -12.14%** against live
   9.46% / 1.2767 / -12.05% and 7.85% / 1.1017 / -12.24%; **4a TRUE at 0/5/10/25/50 bps on U56 and
   at 0/5/10 bps on B136**. SPY OOS 15.29% / 0.8751 / -33.72%.
7. **4b is a KILL, as before and for the same reason.** 61 of 1020 rows pass, all at high `y`; the
   **CAGR floor binds in every single fail** and the DD cap in none. The flat rate required to
   clear the floor is `y* = 2.76%` (U56 OOS) to `6.11%` (U56 IS) and `5.21-6.06%` (B136).
8. **Exact RULES wording — an AMENDMENT to clause 5 of idea 2231's memo, not a replacement for it.**
   If a Sunday review adopts 2231's sweep, append to its proposed clause: *"The idle-NAV sleeve is
   held in a short-duration Treasury instrument. The sweep's acceptance is conditional on that
   instrument yielding at least 0.081% per basis point of round-trip cost (0.81% per annum at the
   10 bps book cost); below that yield the sleeve's turnover exceeds its credit and the sweep is
   not to be run. Above 25 bps of cost the sweep is accepted only with a duration-bearing
   instrument, since a zero-duration cash sleeve at the same yield fails the drawdown leg."*
9. **Honest limits.** FLAT and TRAIL are synthetic accounting lines — no duration, no credit, no
   bid-ask, and TRAIL is a *lagged rate forecast*, not a tradeable instrument (the sandbox carries
   no bill-yield series, so SHY is the only real cash proxy priced here). One band (0.03), one gross
   (0.75), one cadence (W), one weekday offset (d = 0); the 5-offset spread of ideas 914/2111 was
   not measured. Sleeve legs are charged separately from core SPY/SHY, so SHY-arm turnover is an
   upper bound — section H quantifies it at 1.23% / 0.50% of core weight, i.e. negligible.
10. **Recommendation.** Keep 2231's candidate at 0-10 bps; **do not carry its 25/50 bps 4a pass into
    a rules change without the duration clause in line 8.** Gates **18 of 18 PASS**, 1020 published
    rows. Survivorship (rule 9): U56/B136 are current-constituent panels, so levels are optimistic.
