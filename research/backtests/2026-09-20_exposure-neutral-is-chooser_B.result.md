# KEEP-candidate memo (path 4b) — THE EXPOSURE-NEUTRAL DRAWDOWN CHOOSER `C_GXDD`
Idea 1793 (lane B, 2026-09-20). Evidence: `2026-09-20_exposure-neutral-is-chooser_B.py` /
`.grid.csv` (480 rows, every cell) / `.choosers.csv` / `.twins.csv` / `.truncated.csv` /
`.gates.csv`. **Gates 11 of 11.** RULES.md, PROTOCOL.md, scan.py, bot.py, baseline.py untouched.

1. **The book.** The standing panel vol-target (memo `2026-09-20_voltgt-panel_KEEP4b_MEMO.md`):
   hold EVERY priced name equal-weight, scale the whole book by `g = clip(t / sigma20, 0, 1)`,
   `sigma20` = annualised 20-day realised vol of the *unlevered equal-weight panel*, read through
   yesterday's close (`L = 20`, `d = 0`). Two nested schedules (idea 1767): TRADE cadence `T`
   re-spreads the names, REFRESH cadence `R` re-reads `g`. 10 bps, next-day, never levered.
2. **The chooser is the finding.** `C_GXDD` ranks each `(t, R)` cell by
   `IS MaxDD(book) - IS MaxDD(its OWN constant-gross twin matched to the book's IS realised mean
   gross)` — 100% in-sample, so rule-8 legal. It is the drawdown the TIMING buys, net of the
   drawdown that merely buying less does.
3. **Rule 8 (dials `t` and `R` fitted on 2009-2016 ONLY; 2017-2026 read ONCE): `C_GXDD` reaches a
   cell clearing 4b FULL *and* OOS on 4 of 4 large-panel arms**, against `C_ISDD` 2 of 4 and
   `C_ISSHARPE` / `C_ISCALMAR` / `C_GXS` **0 of 4**. G10 re-derives all 36 picks on a panel
   physically truncated at 2016-12-31: 36 of 36 identical.
4. **U56 (the live universe), pick `t = 0.08, R = M`:** FULL 11.26% / 1.2285 / -16.13% (halves
   1.3198 / 1.1442), **OOS 11.87% / 1.2780 / -16.13%**, 2.19 turns/yr, mean gross 0.690, vs SPY
   15.12% / 0.8843 / -33.72% (OOS 15.26% / 0.8737). All five legs clear; DD margin **4.10 pp**
   against the parked memo's 0.37 pp.
5. **B136, pick `t = 0.10, R = W`:** FULL 12.17% / 1.1817 / -13.46% (halves 1.2755 / 1.0904),
   **OOS 12.69% / 1.2417 / -13.46%**, 3.05 turns/yr. Clears 4b FULL *and* OOS at **0 / 10 / 25 /
   50 bps** — the parked memo's own cell fails at 50.
6. **`C_GXS` is a provable NO-OP and it kills a standing explanation.** A long-only constant-gross
   twin's Sharpe is invariant in its gross: across a twin range `k = 0.62 -> 0.98` the twin's IS
   Sharpe spans **0.0007-0.0057** against the book's **0.2283-0.3347** (0.2%-2.4%), spearman
   0.9985-1.0000, argmax identical 6 of 6. **KILL "IS Sharpe rewards the lazier, HIGHER-GROSS
   book"** (ideas 1767 / 1771 / 1763): exposure carries ~1% of the IS Sharpe variation here. What
   IS Sharpe buys is LESS TIMING. On the DRAWDOWN leg the twin carries 55-75% of the variation,
   which is why the same correction is decisive there and vacuous on Sharpe.
7. **The squeeze is MOVED, not escaped.** U56's pick trades a thin DD cap for a thin CAGR floor:
   L5_CAGR margin **0.68 pp** (11.26% vs 10.58%) and the cell FAILS at 50 bps on that floor. B136's
   pick sits in the middle (DD 6.77 pp, CAGR 1.58 pp) and survives all four rungs.
8. **Still unreachable, and still failing.** The refresh half of the dial is not choosable: `R = D`
   clears 4b FULL+OOS at 4 of 4 arms for every `t >= 0.10` and **no legal IS-only chooser ever picks
   it** (the OOS oracle does: `t=0.12, R=D`, U56 OOS 15.28% / 1.3485 / -15.79%). **SMALL665: 0 of 40
   cells clear 4b at any of the four cost rungs.** **Path 4a: 0 of 36 legal picks; 6 of 120 grid
   cells, all B136, and only against the live book RESTATED on B136 (Sharpe 1.0972 against the real
   live U56 comparand's 1.2010) — recorded as a KILL for 4a, not a passer.**
9. **Proposed RULES wording** (rule 6 — Sunday review only; nothing is shipped by this run). It
   names the lookback and the staleness, which idea 1771 point (3) requires, and fixes the REFRESH
   cadence rather than the trade date, which idea 1767 requires:

   > **2. Sizing.** Hold every instrument in the universe priced that day at `g/N` of NAV, `N` the
   > count of priced instruments. `g = min(1, t / sigma_20)`, where `sigma_20` is the annualised
   > 20-day realised volatility of the equal-weight, unlevered universe portfolio computed through
   > **yesterday's close** (`sqrt(252) x` the standard deviation of its last 20 daily returns, no
   > extra staleness). `g` is re-read and the book's total exposure reset to it **at least monthly**;
   > the equal-weight re-spread of the names may run on any cadence from weekly to monthly. Weight
   > not deployed sits in CASH and is never re-spread. No ranking, no momentum screen, no per-name
   > volatility filter. **`t` is fixed once, before any out-of-sample data exists, as the rung of
   > {0.08, 0.10, 0.12, 0.16, 0.20} maximising `MaxDD(book) - MaxDD(twin)` over the fitting window,
   > where `twin` holds the same names at a CONSTANT gross equal to the book's realised mean gross
   > on that window.** On the live universe that rung is **`t = 0.08`**.
10. **Status: KEEP-candidate, path 4b, awaiting Sunday review — NOT a rules change by this run.**
    It is the first VOLTGT wording in the record that is fully implementable (target, lookback,
    staleness, refresh and trade cadence all named) AND reached by a pre-registered legal IS-only
    chooser. **Survivorship:** U56 / B136 are CURRENT constituents and SMALL665 a CURRENT sub-$2B
    screen (54 `max_1d_move >= 1.0` tickers dropped); every CAGR and drawdown LEVEL above is
    optimistic and both 4b bars are easier here than on a point-in-time panel. The CHOOSER contrast
    is same-tape / same-names / same-grid and is first-order immune; the pass COUNTS are not.
