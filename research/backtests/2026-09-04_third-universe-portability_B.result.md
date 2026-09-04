# Idea 49 — third-universe-portability (lane B, 2026-09-04) — **KILL, both candidates, 0 of 28 grid points**

Script: `research/backtests/2026-09-04_third-universe-portability_B.py`
Console: `research/backtests/2026-09-04_third-universe-portability_B.console.txt`

## The question
The project's two 4b KEEP-candidates — idea 2's `N n=20` (top 20 eligible, equal weight, 75%
gross, no `/sqrt(vol20)`) and idea 46's `F f=0.85` (top 85% of whatever is eligible) — were
validated on `universe.json` (56 names) and `universe_broad.json` (136 names). Those are two
overlapping current-constituent lists of US large caps in the same 2009-2026 mega-cap regime;
`broad` is close to a superset of the other. Idea 46 argued f=0.85 was the better rule *because
it ported* across both. This run tests both on the first structurally different universe in the
cache: the 439-name sub-$2B panel (483 names less the 44 with `max_1d_move >= 1.0`), 2011-01-13
to 2026-09-03, trading-day indexed, same construction and same fixed parameters — nothing tuned
to this panel.

## Result — both candidates collapse
| rule | universe.json | universe_broad | **small panel** | small-panel OOS |
|---|---|---|---|---|
| `N n=20` | 12.7% / 1.093 / -18.3% (PASS 4b) | 0.958 / -20.1%, H2 0.814 (FAIL by 0.02) | **6.7% / 0.469 / -27.4%**, halves 0.613/0.352 | 7.4% / 0.496 / -27.4% |
| `F f=0.85` | 11.3% / 1.072 / -16.7% (PASS 4b) | 11.2% / 1.024 / -18.6% (PASS 4b) | **4.3% / 0.371 / -40.9%**, halves 0.466/0.302 | 3.6% / 0.318 / -40.9% |

Same window: SPY 14.2% / 0.863 / -33.7% (halves 0.886/0.864, OOS 15.5%/0.884); RULES v1 (live,
`universe.json`) 6.3% / 0.650 / -13.8%. **0 of 24 selection-pool points pass 4a or 4b** (0 of 28
including the four matched-size diagnostics); every point fails all five 4b tests — H1, H2, OOS,
drawdown and CAGR. This is not a near miss.

## The decisive control: the rule subtracts value from its own asset class
Holding all 439 names equal-weight at 75% gross with **no filter and no ranking** returns
**10.2% / 0.677 / -36.2%** — a higher CAGR and a higher Sharpe than *every one of the 28 filtered
books*. (Consistent with idea 50's 100%-gross 2012+ control, 14.3%/0.74.) So the small-cap
failure is not "small caps did badly": the panel's own beta earned 10.2%, and RULES v1's
machinery turned it into 3.5-9.4%.

**Where it goes:** `F f=1.00` *is* "equal-weight all eligible", i.e. the control plus the
eligibility filter alone. It returns 3.5%/0.329 against the control's 10.2%/0.677 — the 200d-MA
+ vol20<0.60 filter costs **6.6pp/yr of CAGR**, of which only **1.2pp is turnover** (13.3x/yr vs
1.7x/yr at 10 bps); **5.4pp is the filter's own timing**, at 0 bps. On noisy sub-$2B names the
trend filter buys after run-ups and sells after drops. The momentum ranking on top of it is
close to irrelevant: the whole f-sweep sits in a 3.5-6.2% band.

## Other findings
1. **The portability argument for f=0.85 does not survive.** At matched average book size the
   fraction arm beats the count arm on Sharpe at 6/8 pairs here (mean +0.017) against 3/8
   (mean -0.002) on `universe.json` — the sign flips, and both magnitudes are noise. The
   fraction-vs-count choice has no stable answer across universes; it was never the load-bearing
   part of either candidate.
2. **The N-vs-NF decomposition is confirmed.** `E_t < 20` on only 0.89% of days here (E_t means
   141 of 439), so the cash clause almost never fires and N ≈ NF at every n (max gap 0.014
   Sharpe). That is direct evidence for idea 46's finding (5): on `universe.json` the whole
   N-NF difference *was* the cash sleeve, not the position count.
3. **Walk-forward (rule 8) picks nothing under the 4b-aware rule in all three arms** — no
   in-sample point met the in-sample drawdown cap (-11.2%; best in-sample MaxDD -19.6%). The
   plain-Sharpe rule picks `N n=15` (OOS 8.3%/0.524/-27.7%) and `F f=0.70` (OOS 4.0%/0.345/-38.6%),
   both far below SPY's OOS 15.5%/0.884 and below RULES v1's OOS 7.8%/0.751.
4. **Costs bite where they should.** Turnover runs 13-30x/yr on this panel vs 9.6x/yr for the
   candidate on `universe.json`. At 25 bps `N n=20` falls to 3.5%/0.288 and `f=0.85` to
   2.0%/0.215; at 50 bps both are **negative** (-1.6% CAGR). 10 bps is already optimistic for
   sub-$2B names, so the real-money version of these books is worse than the headline.
   A one-week execution lag changes nothing (0.476 and 0.425 Sharpe) — there is no fast signal
   here to decay.

## Caveats
- **Survivorship runs the wrong way for a KILL, which strengthens it.** All 483 panel names
  trade through 2026-09-03: no delistings, no bankruptcies. This panel is *more*
  survivorship-flattered than the two large-cap lists, and the books still fail every test.
- **Benchmark mismatch is stated, not adjusted for.** The cache has no IWM column, so 4b here
  asks "does this small-cap book beat SPY", which is harder than beating its own asset class.
  The control comparison above is the version that does not depend on the benchmark, and the
  rule loses that one too.
- The eval window starts 2011-01-13 (260-day warm-up on a 2010 panel), so the in-sample leg is
  six years, not eight as on `prices.csv`.

## What this means for the Sunday review
The 4b passes on `universe.json` and `universe_broad.json` are a property of **that universe**,
not of the rule. The trend-eligibility filter that ideas 2, 25, 28 and 46 all rest on is
value-destroying on small caps, and 4b's SPY benchmark plus a mega-cap current-constituent list
is exactly the setting where it looks best. Neither candidate should be adopted as a general
rule; if idea 2's `n=20` is adopted at all it should be scoped explicitly to the large-cap list
it was fitted on, with this run recorded as the failed replication. Follow-ups queued as ideas
51-53.
