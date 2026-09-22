# 4b CELL RECORDED, NOT RECOMMENDED — gross 1.00 + full SHY sweep at the LIVE band (idea 2304, lane B, 2026-09-22)
# The idea's premise is KILLED: GROSS clears the 4b CAGR floor on its own and the SWEEP clears nothing on its own,
# so this is not a joint-channel find.  The cell it lands on is the family idea 2213 already recorded at band 0.08,
# and at the LIVE band 0.03 it is STRICTLY WEAKER (4b_FULL at 3 of 4 cost rungs on U56, 2 of 4 on B136, vs 2213's 4 of 4).
1. Universe: the live panel (U56 = research/universe.json, 56 names). Replicates on B136 (research/universe_broad.json).
2. Trend band: UNCHANGED from live RULES v2 — IN above the 200d MA x 1.03, OUT below x 0.97, previous state in between,
   OUT until 200 closes exist.  Weekly cadence, executed at the next close, 10 bps per unit turnover.
3. The two dials priced, and nothing else: GROSS {0.75, 0.85, 1.00} x SWEEP FRACTION phi {0.00, 0.50, 1.00} of the
   residual `1 - sum(w)` into SHY.  Instrument fixed to SHY a priori by idea 2294's duration finding.  72 cells published.
4. THE PREMISE FAILS.  At 10 bps the shipped book's floor gap is +1.9783 pp (U56) / +2.6270 pp (B136).  GROSS alone buys
   +2.9130 / +2.6683 pp and CLEARS it; SWEEP alone buys +0.5012 / +0.5161 pp and clears nothing.  The joint cell buys
   +3.1093 / +2.8838 pp against a sum-of-parts of +3.4142 / +3.1844: INTERACTION -0.3049 / -0.3006 pp.  The mechanism is
   exact and was the point worth learning — raising gross CONSUMES the idle cash the sweep is funded from (realised mean
   gross 0.5327 -> 0.7102 on U56, idle NAV 0.4673 -> 0.2898), so the two channels are competing for one pool of capital.
5. FULL (U56, 10 bps, gross 1.00 / phi 1.00): 11.7282% / 1.2203 / -15.6411%, halves 1.2404 / 1.2063.
   B136: 10.8428% / 1.1190 / -15.8616%, halves 1.2409 / 1.0000.  SPY FULL 15.1388% / 0.8851 / -33.7173% (U56 tape).
6. RULE 8, both dials chosen on 2009-2016 ONLY and 2017-2026 read ONCE: the ZERO-PARAMETER default (gross 1.00, phi 1.00,
   nothing fitted) gives U56 OOS 12.9685% / 1.3013 / -15.6411% and B136 OOS 10.8251% / 1.1327 / -15.8616%, 4b_OOS PASS on
   both.  `C_ISSHARPE` does NOT reach it — it picks gross 0.75 / phi 1.00 (the 4a book) and fails 4b_OOS on both panels;
   `C_IS4b` is UNDEFINED on U56.  Fitting IS Sharpe buys the 4a book and loses the 4b one, as it has on every prior dial.
7. 4a: FAIL at this cell on both panels in every window.  Every 4a pass on the grid (12 of 72) is gross 0.75 WITH a sweep,
   i.e. idea 2294 reproduced; the two KEEP paths are DISJOINT here because 4a is judged against the live book's -12.24%
   drawdown and every 4b passer runs -15.6% to -16.2%.  The 4b DD cap binds in 0 of 72 cells; CAGR binds in 56 of 57 fails.
8. BLOCKING OBJECTIONS, three.  (a) Cost fragility at the LIVE band: 4b_FULL dies at 25 bps on B136 (-0.4162 pp) and at
   50 bps on both (U56 -0.5166 pp), against RULES v2's own 5/10/25/50 acceptance standard.  (b) B136's margins are inside
   the noise: FULL +0.2567 pp and OOS +0.1451 pp, while idea 2213 measured a 1.13-1.86 pp weekday-offset spread on this
   very leg.  (c) It is not a new book: idea 2119 found every committed 4b pass sits at gross 1.00, and lane C's idea 1476
   published these exact gross-1.00 figures today (reproduced here to 4 dp, which is the run's one clean corroboration).
9. NO RULES WORDING IS PROPOSED.  Raising the live book's gross from 0.75 to 1.00 is a sizing change, not a cash-management
   clause, and it is the one change this record has shown is cost-fragile and panel-thin; idea 2294's clause-7 cash sweep
   remains the standing 4a proposal and is unaffected by this run.  The Sunday review should read this as evidence AGAINST
   treating "gross 1.00 + sweep" as a joint device, not as a new candidate to ship.
10. Caveats.  One band (0.03), one cadence (W), one phase (Friday), t+1 execution, two panels, SHY as the sweep proxy (a
   ~1.9y-duration ETF, not cash).  RULE 9 SURVIVORSHIP: U56 and B136 are current-constituent lists held from 2008, so every
   absolute CAGR is optimistic and BOTH 4b bars are easier than they should be; the channel decomposition and the -0.30 pp
   interaction are same-tape, same-names and first-order immune, the pass counts are not.
