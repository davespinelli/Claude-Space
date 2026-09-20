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

---

## ADDENDUM (2026-09-20, lane cloud, idea 1767) — SECTION 1's "WEEKLY REBALANCE" IS THE WRONG
## CLAUSE. The load-bearing dial is the SCALAR REFRESH, and a cheaper book dominates this one.

Idea 1767 crossed TRADE cadence `T` (how often the NAMES are re-spread to equal weight) against
REFRESH cadence `R` (how often `g = clip(t / sigma20, 0, 1)` is re-read) on the same book — two
nested schedules, the diagonal `T == R` being this memo's construction exactly (G3 reproduces
sections 2-4 at max |Δ| **4.605e-05**; gates 9/9;
`research/backtests/2026-09-20_voltgt-trade-vs-refresh-cadence_cloud.py`, 384 cells published).

* **The monthly blowout idea 956 found is a STALENESS fact, not a rebalance-count fact.** Of the
  weekly-minus-monthly OOS drawdown gap, refreshing the SCALAR weekly while trading the names
  MONTHLY recovers **+4.57 pp of +4.38 on U56 (104%), +7.36 of +7.35 on B136 (100%) and +7.62 of
  +7.58 on SMALL665 (101%)**. Doing the opposite — re-spreading the names weekly on a MONTHLY
  scalar — recovers **−0.28 / −0.45 / −1.16 pp (−6% / −6% / −15%)**, i.e. nothing at all.
* **The 4b verdict is a function of R alone.** Pooled over panels and targets at 10 bps, `R ∈
  {D, W}` clears full 4b in 4 of 6 cells at EVERY trade cadence including quarterly, and
  `R ∈ {M, Q}` clears 0 of 6 at EVERY trade cadence including daily. `T` is inert on the verdict.
* **A strictly better and cheaper book exists: (T=M, R=W).** U56 FULL 15.71% / 1.2129 / −19.68%
  (halves 1.2864 / 1.1468), **OOS 16.11% / 1.2343 / −19.68% at 1.51 turns/yr** against this memo's
  15.94% / 1.2193 / −19.86% at 1.83 — **+0.015 of OOS Sharpe, +0.18 pp of drawdown and −17.5% of
  turnover**. B136 OOS 15.38% / 1.1886 / −18.74% at 1.61 against 15.36% / 1.1837 / −18.76% at 1.93.
  It clears 4b FULL and OOS at 0 / 10 / 25 bps and fails only at 50, on the CAGR floor.
* **Rule 8 says it is not choosable, which is why this is a PARK and not a promotion.** With `T`
  and `R` chosen jointly on 2009-2016 only, **4 of 24 legal IS-only picks clear 4b OOS and 0 of 24
  clear 4a OOS**; **23 of 24 land off-diagonal on the WRONG side**, taking a STALE scalar
  (`R = M` or `Q`) because IS Sharpe rewards the lazier, higher-gross book. On U56 all eight IS
  picks go to `(T=Q, R=M)` — OOS −20.83% / −23.96%, 4b OOS FAIL at both targets — while the
  no-choice control `(T=W, R=W)` passes at both. The gain is real and unreachable in sample.
* **What this changes in section 9.** The wording must fix the SCALAR REFRESH, not the trade date:
  a correct version reads "`g` is re-read and the book's total exposure reset to it **at least
  weekly**; the equal-weight re-spread of the names may run on any cadence from daily to monthly".
  Shipping "weekly rebalance" as written prices in a cost the book does not need and does not
  protect the drawdown it claims to.
* **Unchanged:** 0 of 384 cells clear path 4a on any panel; on SMALL665 every one of 128 cells
  fails 4-5 legs; the only binding leg on U56/B136 is the DD CAP (32-41 of 64 per panel × target,
  every other leg binding 0-2 times). Survivorship as stated in point 8 and in idea 1771's
  addendum. **The candidate's status remains PARK** (idea 1771); idea 1767 does not restore it and
  does not propose a rules change. RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are
  untouched by idea 1767.

---

## ADDENDUM (2026-09-20, lane B, idea 1763) — POINT 8's PANEL-INHERITANCE CAVEAT IS **NOT**
## LOAD-BEARING, AND A SPY-SOURCED TARGET IS NOT THE PORTABLE FIX EITHER. STATUS UNCHANGED: **PARK**.

Idea 1763 re-cut this book with `sigma_t` sourced three ways — the PANEL's own equal-weight portfolio
(this memo's construction), **SPY's own daily returns**, and a 50/50 BLEND — at five targets, four
(L,d) conventions and three panels, each against its realised-mean-gross-matched constant-gross twin
(720 scored rows, gates 18/18; `research/backtests/2026-09-20_voltgt-sigma-source_B.py` / `.result.md`).
It reproduces sections 2–4 of this memo at max |Δ| **2.76e-04**, addendum A1 exactly (d=1 → U56 OOS
MaxDD −20.7709%, 4b OOS FAIL) and addendum A2 exactly (PANEL-sourced clears 4b **0 of 20** on SMALL665).

* **Point 8's caveat is answered, and it was not carrying the pass.** At this memo's own cell
  (L=20, d=0, t=0.16) the SPY-sourced book carries the SAME 4b FULL and OOS verdicts on both panels:
  U56 OOS **15.18% / 1.2192 / −19.48%** against this memo's 15.94% / 1.2196 / −19.86% (ΔSharpe
  **−0.0004**), B136 OOS **14.93% / 1.1986 / −18.32%** against 15.36% / 1.1839 / −18.76% (ΔSharpe
  **+0.0147**). The two sigma series are near-duplicates on the large panels (`corr` 0.9910 pearson /
  0.9746–0.9803 spearman). **KILL the reading that this book's 4b pass is a survivorship-panel artefact.**
* **The scalar is genuinely panel-free.** SPY-sourced `g_t` is identical across U56 and SMALL665 at
  1.221e-15; the 2.397e-03 residual against B136 is a CACHE artefact (`prices.csv` vs `prices_broad.csv`
  disagree about SPY by $0.0051) and vanishes to 0.000e+00 on re-sourcing. The PANEL-sourced scalar
  disperses across panels by max |Δ| **0.2015 / 0.6542**.
* **But it does not rescue SMALL, and the premise of the idea dies there.** 0 of 40 non-PANEL cells
  clear 4b FULL *and* OOS on SMALL665 at any cost rung; the leg that fails is `L2_H2` in **1.000** of
  cells for every source. SMALL is a PANEL-RETURN failure, not a sigma-source failure. (SPY-sourcing
  does lift SMALL OOS Sharpe 0.4022 → 0.5862 at t=0.16 and repairs ~68% of the twin deficit — it is
  still beaten by buying less of itself.)
* **And it is not more robust.** 4b OOS convention pass-share on U56+B136: **PANEL 0.700, SPY 0.625,
  BLEND 0.650.** Turnover 3.06 /yr vs 2.93 (2.07 vs 1.83 at this memo's rung). Under **rule 8**, on U56
  `SRC=SPY` reaches a 4b-OOS passer **0 of 2** times against `SRC=PANEL`'s **2 of 2**: SPY's sigma runs
  ~9% above the U56 panel's, so IS Sharpe peaks one rung higher and argmax walks the chooser onto
  t=0.20 (OOS −20.91%, DD cap FAIL). A chooser handed the source as a free dial buys SPY **14 of 18**
  times — the source that then fails.
* **The dial survives the substitution.** Against matched constant-gross twins the SPY-sourced book
  wins OOS by **+0.0927 Sharpe / +7.66 pp MaxDD on U56 (win 1.000)** and **+0.1112 / +11.20 pp on B136**,
  clearing 4b OOS 12–13 of 20 against the twins' 3 and 0. Idea 1771's "first device to beat its matched
  twin" is a property of the vol-target DIAL, not of the panel-sourced sigma.
* **Constructive residue.** At **t ∈ {0.10, 0.12}**, 24 of 24 cells (3 sources × 2 panels × 4
  conventions) clear 4b FULL and OOS — idea 1771's convention-robust band, now shown to be
  SOURCE-INVARIANT too. Inside it the public SPY series serves as well as the panel's own, so any future
  wording can be the simpler, panel-free one. Not promoted here: the band is OOS-visible and only 1 of 3
  legal IS-only choosers (`C_ISLEGS`) lands in it.
* **Path 4a:** 6 of 180 cells clear 4a FULL and OOS, all B136 t=0.08 L=20 — but only against the live
  book **restated on B136** (halves 1.2298 / 0.9671). Against the live U56 comparand (1.2279 / 1.1808 at
  −12.05%) **0 of 60** clear 4a. Recorded as a KILL for 4a, not a passer.
* **Unchanged:** status **PARK** (ideas 1771, 1767). Survivorship as in point 8 and the addenda above.
  RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are untouched by idea 1763.

---

## ADDENDUM (2026-09-20, lane B, idea 1793) — THE TARGET RUNG IS REACHABLE AFTER ALL, BUT ONLY BY
## AN EXPOSURE-NEUTRAL STATISTIC; AND "IS SHARPE REWARDS THE HIGHER-GROSS BOOK" IS **FALSE**.

Idea 1793 re-ran this book's `t` x `R` grid on three panels at four cost rungs (480 cells, every one
published; gates 11/11; `research/backtests/2026-09-20_exposure-neutral-is-chooser_B.py` /
`.result.md`), giving every cell its OWN realised-mean-gross-matched constant-gross twin bisected on
the **IS window only**, so the twin difference is a LEGAL rule-8 chooser. It reproduces sections 2-4
of this memo at max |d| **4.605e-05** and idea 1767's `(T=M, R=W)` U56 OOS row at **5.027e-05**.

* **`C_GXDD` — rank by `IS MaxDD(book) - IS MaxDD(twin)` — clears 4b FULL *and* OOS at 4 of 4
  large-panel arms**, against `C_ISDD` 2 of 4, `C_ISLEGS` 1 of 4 and `C_ISSHARPE` / `C_ISCALMAR`
  **0 of 4**. U56 pick `t = 0.08, R = M`: OOS **11.87% / 1.2780 / -16.13%**, DD margin **4.10 pp**
  against this memo's 0.37 pp. B136 pick `t = 0.10, R = W`: OOS **12.69% / 1.2417 / -13.46%**,
  clearing at **0 / 10 / 25 / 50 bps** where this memo's cell fails at 50. All 36 picks are
  unchanged when rebuilt on a panel physically truncated at 2016-12-31 (G10).
* **KILL the explanation idea 1767 gave for its own off-diagonal picks.** The SAME correction on the
  SHARPE leg (`C_GXS`) makes the IDENTICAL pick to plain `C_ISSHARPE` in 6 of 6 arms: a long-only
  constant-gross twin's Sharpe is invariant in its gross (twin IS Sharpe spread **0.0007-0.0057**
  across `k = 0.62 -> 0.98`, against the book's **0.2283-0.3347**; spearman 0.9985-1.0000). Exposure
  carries ~1% of the IS Sharpe variation here, so IS Sharpe's preference for `t = 0.16-0.20` is a
  preference for **LESS TIMING**, not for more gross. On the drawdown leg the twin carries 55-75% of
  the variation, which is why the same correction is decisive there.
* **The two-sided squeeze is MOVED, not escaped.** The U56 pick swaps this memo's thin DD-cap margin
  for a thin CAGR-floor margin (**0.68 pp**) and fails at 50 bps on it; only B136's `t = 0.10` sits
  in the middle of the squeeze.
* **The REFRESH half is still unreachable.** `R = D` clears 4b FULL+OOS at 4 of 4 arms for every
  `t >= 0.10` and no legal IS-only chooser ever picks it; the OOS oracle takes `t = 0.12, R = D`
  (U56 OOS 15.28% / 1.3485 / -15.79%). Idea 1767's wording fix ("at least weekly") is tightened by
  1793 to "at least monthly" only because that is what its own legal chooser reaches, not because
  monthly is better.
* **Unchanged:** SMALL665 clears 4b **0 of 40** at every cost rung (A2, third confirmation); path 4a
  is 0 of 36 legal picks and its 6 grid passers are B136-restatement artefacts; survivorship as in
  point 8 and the addenda above. **Status of THIS memo (t = 0.16, R = W): still PARK.** Idea 1793
  files a SEPARATE KEEP-4b candidate for the CHOOSER (`2026-09-20_exposure-neutral-is-chooser_B.result.md`),
  awaiting the same Sunday review. RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are
  untouched by idea 1793.
