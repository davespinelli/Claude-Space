# KEEP-CANDIDATE MEMO — VOLTGT-DRIFT on B136 (idea 2034, lane cloud, 2026-09-20). **BOTH paths: 4a AND 4b.**

1. **WHAT.** Equal-weight the broad panel, scale gross by a vol target, and refresh that gross on a
   DRIFT TRIGGER rather than a calendar. Cell: panel B136, `t = 0.10`, `h = 0.08`, trade weekly,
   10 bps, t+1, gross capped at 1.00. Reached by a LEGAL IS-only chooser (argmax min IS 4b-leg
   slack on 2009-2016), not hand-picked; 2017-2026 read exactly once.
2. **FULL SAMPLE (10 bps, t+1).** CAGR **12.51%**, Sharpe **1.2286**, MaxDD **-11.81%**,
   halves **1.3171 / 1.1415**. Turnover 3.13/yr, 19.8 refreshes/yr, mean gross 0.777.
3. **VS LIVE RULES v2.** 7.96% / 1.0972 / -12.24%, halves 1.2296 / 0.9669. **PATH 4a PASSES:**
   Sharpe higher in BOTH halves (+0.0875, +0.1746) and MaxDD 0.43 pp shallower.
4. **VS SPY.** 15.12% / 0.8844 / -33.72%, halves 0.9571 / 0.8249. **PATH 4b PASSES**, all five
   legs positive: H1 +0.3600, H2 +0.3166, OOS +0.4191, MaxDD vs `0.60 x SPY` +8.42 pp, CAGR vs
   `0.70 x SPY` +1.92 pp.
5. **RULE 8 (OOS 2017-2026, read ONCE).** 13.01% / **1.2928** / -11.81%, against SPY 15.26% /
   0.8737 / -33.72% and live RULES v2 7.85% / 1.1017 / -12.24%. Clears 4b OOS and 4a OOS.
6. **COSTS.** 0 bps 1.2603 / 25 bps 1.1812 / 50 bps 1.1020. Both paths hold at 25 bps; at 50 bps
   4b still passes and 4a fails.
7. **CAVEATS.** 1 of 24 picks on one panel at one cadence — a multiple-comparison caveat applies,
   and the CAGR leg's margin is thin (+1.92 pp). SURVIVORSHIP: B136 is a CURRENT-constituent list,
   so the levels are optimistic and both 4b bars are easier than on a point-in-time panel. The
   family clears 4b 0 of N on SMALL665 (confirmed five times).
8. **EVIDENCE.** `research/backtests/2026-09-20_4b-verdict-bar-vs-book_cloud.py`, rows
   `panel=B136, book_tape=FULL, bar=FULL, target=0.10, T_trade=W, family=DRIFT, h=0.08` of
   `.grid.csv.gz`; pick row 95 of `.walkforward.csv`; gates 11/11 in `.gates.csv`.
9. **EXACT RULES WORDING, if adopted at a Sunday review (replaces clause 2-3 of RULES v2 wholesale):**

   > **2. Panel.** Hold every instrument in `research/universe_broad.json` that is priced that day.
   > **3. Weight.** Each held name gets `G_t / N_t` of NAV, where `N_t` is the number of instruments
   > priced that day and `G_t` is the GROSS SCALAR. Un-deployed weight is CASH; never re-spread.
   > **4. Gross scalar.** Let `sigma_t` be the annualised 20-day realised volatility of the
   > UNLEVERED equal-weight panel portfolio through close `t`. The TARGET gross is
   > `g_t = min(0.10 / sigma_t, 1.00)`; if `sigma_t` is unavailable, `g_t = 0`.
   > **5. Refresh trigger (DRIFT, not calendar).** Carry the gross scalar `G` forward unchanged.
   > At each close `t`, if `|g_t - (current deployed gross)| > 0.08`, set `G = g_t`; otherwise
   > leave `G` unchanged. Gross is never levered above 1.00.
   > **6. Trade.** Rebalance name weights to `G / N` on the weekly rebalance date only; on a
   > non-rebalance day on which the trigger fires, rescale the existing holdings pro rata to the
   > new `G` and trade nothing else. All weights decided at close `t` are executed at close `t+1`.
   > **7. Costs.** 10 bps per unit turnover.

10. **STATUS.** KEEP-candidate on BOTH paths, awaiting Sunday review. Not adopted; RULES.md,
    PROTOCOL.md, scan.py, bot.py and baseline.py are untouched by this run.

---

## ADDENDUM (2026-09-20, lane cloud run 2, idea 2054) — **THE 4a LEG IS DOWNGRADED. THE 4b LEG IS THE MOST STRESS-TESTED IN THE FILE.**

Idea 2054 re-priced this cell on the full cross of the sprint's four standing stress axes —
COST {10, 25, 50} bps x DELAY {t+1, t+2} x PHASE {ENGINE + five weekday/month-day rungs} — inside
a 5,040-book corpus (gates 8/8; this cell reproduced to max abs d = 8.327e-17). Result:

* **4b: 36 of 36 points, 100.0%.** The binding-leg column reads `none` at every point. At the
  WORST corner (50 bps, t+2, WED/D10) the book still reads 10.78% / 1.0618 / -13.77% against a
  `0.70 x SPY` CAGR floor of 10.59% and a `0.60 x SPY` MaxDD cap of -20.23%.
* **4a: 8 of 36 points, 22.2% — an ARTEFACT of the discovery settings.** It survives only at
  t+1, only at <= 25 bps, and only at 4 of the 6 phase rungs. One extra day of execution latency
  takes it to **0 of 18**, entirely through drawdown (MaxDD -11.81% -> -12.82%, through the live
  book's -12.24%, while both Sharpe halves still clear). At 50 bps it is 0 of 12.

**Point 3 of this memo is therefore RESTATED:** "PATH 4a PASSES" holds only at t+1 execution, at
or below 25 bps, and at 4 of 6 rebalance-phase rungs — it is not a robust 4a pass and must not be
quoted as one. Points 1, 2, 4, 5, 6, 8 and 9 stand unchanged; point 7's multiple-comparison
caveat is reinforced (8 of 864 rule-8 picks clear both paths, all on B136, all at t+1).

**STATUS after the addendum:** KEEP-candidate on path **4b only**, awaiting Sunday review, with a
36-of-36 stress record. Evidence:
`research/backtests/2026-09-20_dualpath-four-axis-stress_cloud.py` / `.result.md` /
`.candidate.csv` / `.axes.csv` / `.census.csv` / `.walkforward.csv` / `.gates.csv`.

---

## ADDENDUM 2 (2026-09-20, lane cloud run 3, idea 2046) — **THE AXIS THAT KILLS 4a IS LATENCY, NOT COST. 4b NOW 45 OF 45.**

Idea 2046 walked COST {10, 25, 50} bps and EXECUTION DELAY {t+1, **t+2, t+3**} **jointly** (t+3
had never been priced in this record), inside a 630-book / 1,890-cell corpus. Gates 8/8; this cell
reproduced to max abs d = 8.327e-17.

* **4b: 9 of 9 joint points, binding leg `none` at every one.** Worst corner (50 bps, t+3):
  10.79% / 1.0536 / -13.98% against a `0.70 x SPY` CAGR floor of 10.59% and a `0.60 x SPY` MaxDD
  cap of -20.23%. With idea 2054's 36 of 36, the 4b leg now has a **45-of-45** stress record.
* **4a: 2 of 9.** The frontier is unambiguous — **t+1 clears 4a up to 25 bps; t+2 and t+3 clear it
  at NO cost at all.** Failure modes H1 x4, MaxDD x3; t+3 rescues nothing (corpus-wide 4a falls
  21 -> 2 of 210 from t+1 to t+3 at 10 bps).
* **The two ladders are ADDITIVE:** worst Sharpe interaction +0.0036 (2.8% of the larger main
  move), MaxDD 0.67 pp. Cheaper execution therefore cannot buy latency back, which is why 4a has
  no surviving cell off t+1.
* Rule 8 here: **1 of 108** legal picks clears both paths — this cell, at the discovery corner —
  and 39 of 108 clear 4b only. SMALL665 is 0 of 630 on both paths (seventh confirmation).

**Point 3's restatement is sharpened: `t+1` execution is a LOAD-BEARING clause of point 9's rule
wording, not a convention.** Points 1, 2, 4, 5, 6, 8 and 9 stand unchanged.

**STATUS after addendum 2:** KEEP-candidate on path **4b only**, awaiting Sunday review, with a
45-of-45 joint stress record. Evidence:
`research/backtests/2026-09-20_cost-latency-joint-ladder_cloud.py` / `.result.md` /
`.candidate.csv` / `.frontier.csv` / `.interaction.csv` / `.census.csv` / `.walkforward.csv` /
`.gates.csv`.

---

## ADDENDUM 3 (2026-09-20, lane C, idea 2050) — **THE 4b LEG IS NOT A NAME-SET ACCIDENT. THE 4a LEG DIES ON A SECOND AXIS.**

Idea 2050 deleted `k` names at random from the panel's own held-name list and rebuilt the whole
book on what was left — the equal-weight basket, the realised panel volatility that drives the
gross scalar, the drift trigger and the turnover — 200 seeded draws at each of k = 5 / 10 / 20 / 40,
on B136 and on both companion panels (2,403 rebuilt books; gates 8/8; the undeleted reference
reproduced this memo's cell to max abs d = 4.441e-16).

* **4b: 800 of 800, 100.0%, at every rung** — including deleting 40 of the 136 names (29.4%).
  Over all 800 draws the WORST reading of every leg is still positive: H1 **+0.2254**, H2 +0.2064,
  OOS **+0.2997**, MaxDD vs `0.60 x SPY` **+6.40 pp**, CAGR vs `0.70 x SPY` **+0.63 pp**. Worst
  single book 11.22% / 1.1099 / -13.83% (OOS 11.73% / 1.1734 / -13.83%). Mean Sharpe falls only
  1.2286 -> 1.2078 across the whole ladder. Idea 1749 measured the name set as a reachable axis
  worth ~43 pp of 4b pass rate; **on this cell it is worth zero.** Deleting SPY itself (a held
  name here) costs nothing: 1.000 with it gone, 1.000 with it kept.
* **RULE 8 on the deleted panels** (IS 2009-2016 chooses `t` and `h`, 2017-2026 read ONCE): the
  legal IS-only chooser reaches a 4b-clearing book at **59 of 60** draws, OOS mean **13.10%** /
  **1.2752** / worst -21.06%, against live RULES v2 OOS 7.85% / 1.1017 / -12.24% and SPY OOS
  15.26% / 0.8737 / -33.72%. It keeps `t = 0.10` at 57 of 60 but lands on `h = 0.08` at only
  17 of 60 — **the target is the stable dial, the drift threshold is not** — which does not move
  the verdict, because 38.5 of the 50 ladder cells clear 4b on the average deleted panel.
* **4a: 0.760 -> 0.630 -> 0.405 -> 0.280** as k goes 5 -> 10 -> 20 -> 40, and the MATCHED bar
  (live RULES v2 rebuilt on the same deleted names) tracks the fixed bar within 0.05 at every
  rung, so it is a BOOK effect, not a comparand effect. **381 of the 385 failures fail on MaxDD**
  (371 on drawdown alone) while both Sharpe halves clear in 786 of 800 — the identical mechanism
  ideas 2054 and 2046 found on the latency axis. Deleting FIVE names of 136 breaks 4a in 24% of
  draws.

**Point 3 of this memo is RESTATED AGAIN, and more narrowly than addenda 1 and 2 left it:** the 4a
pass holds only at t+1 execution, at or below 25 bps, at 4 of 6 rebalance-phase rungs, **and only
on the exact 136-name list**. It is not a 4a pass in any usable sense and must not be quoted as
one. The downgrade in addenda 1 and 2 stands; the name set is a THIRD independent axis on which
it fails, and the second to fail through drawdown.

**Point 7's survivorship caveat is NARROWED, not lifted.** Random deletion bounds the verdict's
SENSITIVITY to the name set — it is not a point-in-time correction, because it removes survivors at
random where history removes losers. The 4b LEVELS here stay optimistic; what this addendum
establishes is that they are not held up by any small set of particular names.

**STATUS after addendum 3:** unchanged — **KEEP-candidate on path 4b only**, awaiting Sunday
review, now with a 45-of-45 cost x delay x phase stress record (addenda 1 and 2) AND an
800-of-800 name-deletion record. The
exact RULES wording in point 9 is unchanged. Evidence:
`research/backtests/2026-09-20_dualpath-name-set-deletion_C.py` / `.result.md` / `.log.txt` /
`.draws.csv.gz` / `.summary.csv` / `.walkforward.csv` / `.wf_summary.csv` / `.gates.csv`.

---

## ADDENDUM 3 (2026-09-20, lane B, idea 2064) — **THE SURVIVORSHIP CAVEAT IS REPLACED BY A MEASURED REACH, AND THE RANDOM-DELETION RECORD IS NOT THE RIGHT EVIDENCE FOR IT.**

Idea 2050's 800-of-800 record deletes names UNIFORMLY AT RANDOM and says so itself: that bounds
SENSITIVITY to the name set, not the BIAS, because history removes losers where the random draw
removes survivors. Idea 2064 ran the survivorship DIRECTION — delete the `k` highest-returning
names (`BEST`, full sample; `BEST_IS`, ranked on 2009-2016 only) — on 266 books and 90 rule-8
picks, gates 10/10, this cell reproduced to 4.441e-16.

1. **The random band never covers the adversarial rung: 0 of 8 (panel, k).** At every rung the
   BEST book reads below the MINIMUM of 30 random draws at the same `k`. **Addendum 2's and idea
   2050's name-set records must not be quoted as "survivorship-robust".**
2. **CAVEAT 7 IS REPLACED, NOT LIFTED, BY A REACH.** On B136 the cell keeps 4b after deleting its
   **10 best names of 136 (7.4%)** — BEST k=10 reads 11.14% / 1.1266 / -12.79% — and **loses it at
   the 20 best (14.7%)**, 10.38% / 1.0662 / -12.95%, `L5_CAGR` -0.21 pp. `BEST_IS` reaches k=20.
   On U56 the pass ends at **k = 5**, by **0.04 pp** of CAGR.
3. **Every break is the CAGR FLOOR; not one is drawdown.** `L4_DD` never falls below +6.70 pp and
   both Sharpe halves and the OOS leg stay positive at every rung. Caveat 7's "+1.92 pp is thin" is
   now the operative constraint, with a measured exchange rate on B136: CAGR 12.51% -> 11.62% ->
   11.14% -> 10.38% -> 9.35% at k = 0 / 5 / 10 / 20 / 40, i.e. **0.18 pp of CAGR per deleted best
   name at k = 5, falling to 0.08 pp at k = 40.**
4. **Point 3 is RESTATED a third time.** Path 4a fails 0 of 8 on the fixed bar and 0 of 8 on the
   matched bar, MaxDD implicated at 8 of 8 and H1 at 6 of 8, while the random control at the same
   `k` still passes 0.800 / 0.667 / 0.500 / 0.233.
5. **Rule 8 on adversarial panels:** reach 4 of 8 (random control 32 of 32), mean OOS 13.22% /
   1.1539 / -17.93% vs SPY OOS 15.26% / 0.8737 / -33.72% and live RULES v2 OOS 7.85% / 1.1017 /
   -12.24%; all four failures `L4_DD`. The chooser keeps `t = 0.10` at 2 of 8 and `h = 0.08` at
   **0 of 8** — adversarial deletion moves the TARGET dial random deletion left stable at 57 of 60.
6. **Bound, not correction.** Nothing offline can restore a delisted 2011 name; `BEST` is
   deliberately pessimistic (look-ahead in the stress, never in the book) and `BEST_IS` is the
   ex-ante readable version. Both published.
7. **STATUS UNCHANGED — KEEP-candidate on path 4b only**, awaiting the Sunday review, now carrying
   a 36-of-36 four-axis stress record, an 800-of-800 random-deletion record and a **bounded
   adversarial reach of 10 names of 136**. Anyone quoting the 4b pass must quote that reach with
   it. RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py untouched by idea 2064.
