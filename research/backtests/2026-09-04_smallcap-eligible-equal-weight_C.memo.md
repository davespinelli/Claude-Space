# Idea 39 — small-cap-eligible-equal-weight — **KILL** (lane C, 2026-09-04)

Not a KEEP memo. This records a portability failure that bears directly on the two
live 4b KEEP-candidates, so the Sunday review should read it before promoting either.

**Question.** Ideas 2 (top-20 EQW @75% gross) and 46 (f=0.85) pass PROTOCOL 4b on
universe.json and universe_broad.json — two current-constituent lists of ETFs and
large caps. Idea 39 asks whether the book they are built on (equal-weight everything
above its 200d MA with vol20 < 0.60) survives on a structurally different universe:
the 439-name sub-$2B small-cap panel (483 names less the 44 with max_1d_move ≥ 1.0).

**Answer: 0 of 10 grid points pass 4a or 4b, and none is close.** Sample 2011-01-13
to 2026-09-03, weekly, 10 bps, t+1 execution. SPY 14.2%/0.863/-33.7% (halves
0.886/0.864); RULES v1 on the same panel 8.1%/0.602/-32.8%. 4b bars: Sharpe > 0.886
(H1) and > 0.864 (H2), MaxDD ≥ -20.2%, CAGR ≥ 9.9%.

| point | CAGR | Sharpe | MaxDD | H1/H2 | OOS Sharpe |
|---|---|---|---|---|---|
| **F f=1.00 g=0.75** (idea 39's primary arm) | 3.5% | 0.329 | -40.2% | 0.433/0.250 | 0.280 |
| F f=1.00 g=1.00 | 4.4% | 0.329 | -50.4% | 0.436/0.250 | 0.280 |
| F f=0.85 g=0.75 / g=1.00 (idea 46's rule) | 4.3% / 5.3% | 0.371 / 0.372 | -40.9% / -51.2% | 0.466/0.302 | 0.318 |
| F f=0.45 g=0.75 / g=1.00 | 5.7% / 7.2% | 0.448 | -40.7% / -51.4% | 0.51/0.41 | 0.447 |
| N n=20 g=0.75 / g=1.00 (idea 2's rule) | 6.7% / 8.3% | 0.469 / 0.470 | -27.4% / -36.4% | 0.61/0.35 | 0.496 |
| N n=40 g=0.75 / g=1.00 | 5.2% / 6.4% | 0.415 | -24.1% / -31.9% | 0.44/0.40 | 0.467 |

Every point fails all five 4b tests (H1, H2, OOS, MaxDD, CAGR) and 4a on both halves.
Rule-8 walk-forward (params chosen on 2011-2016 only, two selection rules fixed in
advance): the plain-Sharpe rule picks f=0.85 g=1.00 → OOS 4.4%/0.318/-51.2% against
SPY 15.5%/0.884/-33.7%; the 4b-aware rule picks **nothing** — no in-sample point met
the in-sample drawdown or CAGR bar. Both KEEP-candidate rules are among the worst
points on this panel, not merely weaker ones.

**Mechanism: the eligibility gate is inverted on small caps, not just weak.**
Equal-weighting all 439 names with no filter at all gives 8.1%/0.640/-30.7% at 1.5x
turnover — better than every filtered arm on Sharpe, CAGR *and* drawdown. Decomposed
at matched 75% gross: 200d gate only 6.4%/0.500/-38.2%; vol20 gate only 5.4%/0.441;
both 3.6%/0.332/-40.0%. Each gate subtracts, and they compound. Costs explain only
part of it — the same f=1.00 book at 0 bps still reads 5.0%/0.432 against the
unfiltered 8.1%, so ~1.4pp of the 4.5pp CAGR gap is the 13.4x turnover and ~3.1pp is
selection. The complement book (hold every name the filter *rejects*) returns
11.9%/0.731; eligible minus complement is **-8.41%/yr, t -3.77**.

**Caveat that limits how far the complement result may be pushed.** The panel is
current constituents of a sub-$2B screen: names that crashed and then delisted are
absent. That bias falls hardest on exactly the beaten-down, high-vol names the
complement holds, so "buy the rejects" is *not* a tradeable finding — read it only as
evidence on the gate's sign. The KILL itself does not depend on it: the unfiltered
control and the filtered arms hold overlapping survivor sets, and the filtered arms
still lose.

**Where it bleeds.** Not exposure — the f=1.00 book is 74.4% invested on average and
spends exactly one day in cash (2020-03-19, when the eligible set hit 0 of 439). The
loss is cross-sectional: 2020 f=1.00 +3.2% vs unfiltered +28.3% and SPY +18.3%; 2019
+2.8% vs +12.8%; 2023 +5.4% vs +12.8%; 2024 +2.4% vs +9.1%. The trend gate holds the
names that never fell and misses the rebound cohort, in every V-shaped year.

**What the Sunday review should take from this.** The two 4b candidates have now been
tested on three universes. Both pass on the 56-name and (f=0.85) 136-name large-cap
lists and both fail decisively here. Two large-cap current-constituent lists that
overlap heavily are one replication, not two — this is the first genuinely
out-of-universe test and it fails. Promote either rule as a **large-cap rule with a
stated universe condition**, not as a general one, and do not size it on the
assumption that the mechanism is universal.

**Independent replication.** Lane B ran QUEUE idea 49 on the same panel from a
separately-written script during the same sprint and reached the same KILL: its
f=1.00 arm reads CAGR 3.5%, identical to this one, and its unfiltered control
(10.2%/0.677/-36.2% at 100% gross vs 8.1%/0.640/-30.7% here at 75%) is the same
result at a different gross. Two independent implementations agreeing to the decimal
is the strongest confirmation the project has for any result to date.

**Ideas queued:** lane B's 51 (trend-filter-by-market-cap) already covers the
gate-sign-across-universes follow-up. Added here: 54 (delisting-aware small panel,
INFRASTRUCTURE — the bias falls hardest on the cohort this run found excluded) and
55 (trend-gate lookback on the primary universe, where the gate is supposedly the
edge and nobody has varied it).
