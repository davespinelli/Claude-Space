# KEEP-candidate memo (path 4b) — PANEL VOL-TARGET, found incidentally by idea 1730 (lane cloud, 2026-09-20)

1. **The book.** Hold EVERY priced name in the panel at equal weight, no ranking, no band, no vol
   filter; scale the whole book by `g_t = clip(target_vol / vol20_portfolio_t, 0, 1)` where
   `vol20_portfolio_t` is the 20-day realised annualised vol of the *unlevered equal-weight panel*.
   Weekly rebalance, 10 bps, next-day execution, never levered (gross capped at 1.00). ONE tuned
   parameter: `target_vol`.
2. **Path 4b, FULL, U56** (t=0.16): 15.61% / 1.2027 / -19.86%, halves 1.2828 / 1.1307, vs SPY
   15.12% / 0.8843 / -33.72% (halves 0.9570 / 0.8249). All four 4b legs clear.
3. **Path 4b, OOS (rule 8, 2017-2026 read once), U56:** 15.94% / 1.2193 / -19.86% vs SPY
   15.26% / 0.8737 / -33.72% and RULES v2 9.46% / 1.2766 / -12.05%. 4b OOS PASS.
4. **Replicates on the second panel, B136** (t=0.16): FULL 15.94% / 1.2049 / -18.76% (halves
   1.3439 / 1.0708); OOS 15.36% / 1.1837 / -18.76%. 4b FULL and OOS PASS.
5. **The rung is not the finding.** ALL THREE grid rungs (t = 0.08 / 0.12 / 0.16) clear 4b OOS on
   BOTH panels; t=0.12 posts U56 OOS 14.56% / 1.2726 / -16.44% and B136 OOS 13.86% / 1.2217 /
   -16.01%. The rule-8 IS-only argmax (2009-2016 IS Sharpe) lands on t=0.16 on both panels, so the
   walk-forward pick is a 4b passer and no rung in the grid is not.
6. **It does NOT clear path 4a** (0 of 6 rungs): its MaxDD is deeper than the live book's -12.05%
   because it runs mean gross 0.68-0.93 against the live book's 0.53. 4a is the wrong bar here —
   this is exactly what PROTOCOL rule 4b was added on 2026-09-04 to handle.
7. **Turnover is not the catch:** 1.83 /yr (U56, t=0.16) and 1.93 /yr (B136) against the live
   RULES v2 book's 1.77 and 2.01. Costs are already charged at 10 bps in every number above.
8. **Caveats, stated:** U56 and B136 are CURRENT constituents (survivorship). The vol target is
   calibrated on the *panel's own* realised vol, so it inherits the panel. `t=0.16` is the TOP of
   the grid and IS Sharpe is monotone in `t`, so the true argmax is outside the tested range —
   the claim is "every tested rung passes", not "0.16 is optimal". Not tested on SMALL.
9. **Proposed RULES wording** (rule 6 — Sunday review only; RULES.md, scan.py, bot.py and
   baseline.py are NOT modified by this run):

   > **2. Sizing.** Each week, hold every instrument in the universe that has a price that day at
   > `g/N` of NAV, where `N` is the count of priced instruments and
   > `g = min(1, 0.16 / sigma_20)`, `sigma_20` being the annualised 20-day realised volatility of
   > the equal-weight, unlevered universe portfolio (`sqrt(252) *` the 20-day standard deviation of
   > its daily returns, computed through yesterday's close). Weight not deployed sits in CASH; it
   > is never re-spread across the held names, and `g` never exceeds 1. No ranking, no momentum
   > screen, no per-name volatility filter.

10. **Status: KEEP-candidate, path 4b, awaiting Sunday review.** It is NOT proposed as a live rules
    change by this run. Evidence: `research/backtests/2026-09-20_4a-drawdown-clause-vs-gross_cloud.py`
    (`.books.csv` rows `VOLTGT t=*`, gates 74/74, `fast_run` == `engine.backtest` at 0.000e+00).

---

## ADDENDUM (2026-09-20, lane cloud, idea 1715) — two fragilities found while testing the dial

Idea 1715 re-ran this book on a 288-cell grid and **reproduced points 2-4 of this memo exactly**
(U56 t=0.16 FULL 15.61% / 1.2027 / -19.86%, OOS 15.94% / 1.2193 / -19.86%; B136 FULL 15.94% /
1.2049 / -18.76%, OOS 15.36% / 1.1837 / -18.76%; gates 4/4, `fast_run == engine.backtest` at
0.000e+00). Two things it also found, which this memo did not state and which a Sunday review
should weigh:

* **A1. The U56 4b OOS pass is thinner than one convention choice.** Its DD margin is **0.37 pp**
  (OOS MaxDD -19.86% against the 0.60 x SPY cap of -20.23%). Computing `sigma_20` through
  *t-1* instead of *t* — one extra day of staleness, a defensible convention, not a bug fix —
  moves OOS MaxDD to **-20.77%**, a 0.91 pp move that **flips 4b OOS from PASS to FAIL**. B136
  survives the same move (-19.30%). Point 2 of this memo should be read as "passes on U56 at the
  record's sigma convention", not "passes".
* **A2. It does not exist on small caps.** On the 483-name sub-$2B panel (54 `max_1d_move >= 1.0`
  tickers dropped; current constituents, so this is the optimistic read) **0 of 96 books clear 4b
  FULL or OOS** on either the vol-target or the constant-gross ladder, and the rule-8 IS-only pick
  reads OOS 7.40% / 0.4872 / -33.87% against SPY 15.26% / 0.8737 / -33.72%. This independently
  confirms idea 1719's incidental finding. Point 8's "Not tested on SMALL" is now tested: it fails.

What 1715 does support is the memo's **dial**, not its rung: the vol-target exposure path is ~57x
more resolvable in sample than constant gross (IS Sharpe spread 0.2077 vs 0.0031 against the same
leave-one-IS-year-out SD ~0.175) and costs less when mis-set (OOS MaxDD span 9.2 pp vs 14.9 pp).
The rung itself is still unresolvable: IS argmax equals the OOS oracle in 0 of 12 cells and beats
its runner-up by 0.07 of a deletion SD. Evidence:
`research/backtests/2026-09-20_voltgt-dial-rule8-resolvable_cloud.py` / `.result.md`.

---

## Addendum (2026-09-20, lane cloud, idea 956) — the candidate is PHASE-ROBUST and CADENCE-DEPENDENT

Idea 956 re-scored this book, plus five other committed/standing 4b objects, at all 21 DOM phases
and all 5 weekly phases on U56 / B136 / SMALL at 0 / 10 / 25 / 50 bps
(`research/backtests/2026-09-20_phase-averaged-4b-verdict_cloud.py`, gates 28/28; its G3 reproduces
sections 2–4 above to max|Δ| 0.0000).

* **Phase-robust on its own cadence.** `VOLTGT016` clears 4b FULL *and* OOS at **5 of 5** weekly
  phases on B136 and **4 of 5** on U56, and keeps its certification under every averaging rule
  tested — CANON, MEAN, MEDIAN, SHARE50 and TRANCHE (2 of 6 panel × grid cells each); only the
  worst-phase MIN rule drops it to 1 of 6. Its 4b pass is therefore **not** an artefact of the
  canonical rebalance date, which is the failure mode idea 944 found in 6 of 9 U56 books.
* **Cadence-dependent, and this is a real limit on the claim.** On a MONTHLY cadence (DOM21) the
  book fails 4b on both panels at the canonical phase and at 18 of 21 / 20 of 21 phases: its OOS
  MaxDD blows out to **−24.2 % (U56) and −26.1 % (B136)** against **−19.9 % / −18.8 %** weekly.
  The weekly rebalance in section 1 is load-bearing and must stay in any RULES wording.
* **Rule 8 on the phase dial:** the IS-chosen weekly phase gives U56 OOS 16.30 % / 1.2446 / −18.99 %
  and B136 15.41 % / 1.1888 / −19.64 %, against the canonical 15.94 % / 1.2193 / −19.86 % and
  15.36 % / 1.1837 / −18.76 % — i.e. choosing the date in sample buys ≈ +0.025 of OOS Sharpe here
  and −0.006 across the run's full 18-cell corpus. The phase is not a dial worth adding.
* **Unchanged:** the book still does not clear path 4a (its drawdown is deeper than the live
  book's), it is still not tested on SMALL as a candidate (SMALL 4b pass-share 0.000), and its
  status is still **KEEP-candidate, path 4b, awaiting Sunday review**. RULES.md, PROTOCOL.md,
  scan.py, bot.py and baseline.py are untouched by idea 956.

---

## ADDENDUM (2026-09-20, lane B, idea 1771) — the 4b OOS pass is CONVENTION-SELECTED and, on U56,
## UNREACHABLE BY EVERY LEGAL CHOOSER AT THIS RUNG. **STATUS PROPOSED: PARK, not KEEP.**

Idea 1771 mapped the surface `sigma_t` actually lives on — LOOKBACK `L` {5,10,20,40,60} x
STALENESS `d` {0,1,2,5}, 20 convention cells — at five targets on three panels with every book's
realised-mean-gross-matched constant-gross twin as a control (2,400 scored rows, gates 10/10;
`research/backtests/2026-09-20_voltgt-sigma-convention-surface_B.py` / `.result.md`). It
reproduces sections 2-4 of this memo at max |Δ| **2.8e-04** and addendum A1 exactly
(`d=1` → U56 OOS MaxDD **−20.7709%**, 4b OOS FAIL).

* **CONVENTION PASS-SHARE at this memo's own `t = 0.16`: 0.250 on U56 (5 of 20 cells) and 0.400 on
  B136 (8 of 20).** Section 2's pass is a property of the cell `(L=20, d=0)`, which this memo's
  RULES wording in section 9 does not even name. Section 5's claim that "the rung is not the
  finding" holds for the TARGET but not for the CONVENTION: three quarters of the defensible
  conventions fail on U56.
* **The carrier is this memo's rung.** The OOS DD-cap fail-share is monotone in the target —
  U56 0.00 / 0.10 / 0.20 / **0.75** / **0.95** at t = 0.08 / 0.10 / 0.12 / 0.16 / 0.20 — while the
  CAGR floor binds only below t ≈ 0.10. 4b is a TWO-SIDED SQUEEZE here and the convention-robust
  band is **t ∈ {0.10, 0.12}** on both panels (pass-share 0.90 / 0.80 on U56, 0.85 / 0.75 on B136).
  `t = 0.16` is the least convention-robust rung on this memo's own published grid.
* **And IS Sharpe walks the chooser straight into it.** IS Sharpe peaks at t = 0.16 on both panels
  and its surface argmax is `t0.16 L20 d1` — the STALER convention, the cell A1 showed fails.
* **Rule 8 (2017-2026 read once), at this memo's rung: 0 of 3 legal IS-only choosers reach a
  4b-OOS-passing cell on U56.** `C_ISSHARPE` / `C_ISLEGS` → `L20 d1`, OOS −20.77% FAIL; `C_ISDD` →
  `L40 d1`, −20.83% FAIL. Only the no-choice control `C_MEMO` passes. B136 survives all three.
  Overall 7 of 18 legal picks clear 4b OOS and **0 of 24 clear 4a OOS**; SMALL665 0 of 8.
* **What SURVIVES is the DIAL, not the rung.** Against its own realised-gross-matched constant-gross
  twin the vol target buys OOS **+0.0587 of Sharpe and +6.16 pp of MaxDD on U56** (win share 0.810)
  and **+0.0503 / +9.44 pp on B136** (0.790); the twins clear 4b OOS 4 and 0 times against this
  book's 51 and 47. At this memo's own cell the matched twin (k = 0.9338) posts OOS
  17.06% / 1.1266 / **−27.46%**. **This is the first device in the record to beat its matched
  twin at scale.** On SMALL665 the twin wins 100 of 100 (dSharpe −0.2516).

**Proposed status change for the Sunday review: KEEP-candidate (path 4b) → PARK.** Section 9's
wording must not ship as written: it names a volatility without naming its lookback or its
staleness, so it is not implementable without a second, uncertified choice, and the rung it fixes
is the one the surface says is fragile. Idea 1771 does NOT certify t = 0.12 in its place — that is
an OOS-visible reading and needs its own pre-registered run. RULES.md, PROTOCOL.md, scan.py,
bot.py and baseline.py are untouched by idea 1771.
