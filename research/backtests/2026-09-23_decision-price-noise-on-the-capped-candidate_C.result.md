# Idea 2495 (lane C, run 60, 2026-09-23) — decision-price noise on the standing 4b candidate

**VERDICT: CONFIRM of the standing capped candidate — a robustness stamp, NOT a new candidate and
NOT a RULES change.** No change to RULES.md, PROTOCOL.md, scan.py, bot.py or baseline.py (rule 6).

**THE QUESTION.** The candidate is a threshold rule on one number: today's close against its own
200d MA. The record has moved that THRESHOLD every deterministic way it can be moved (band width,
MA length, Donchian, MA slope, asymmetric entry/exit edges) and has perturbed the panel's
COMPOSITION, but it has never perturbed THE PRICE THE THRESHOLD IS READ FROM. Closes are not exact:
the auction print, a second vendor's adjusted close and a different back-adjustment convention
disagree by a few bps, and `band_state` is HYSTERETIC, so a spurious close ratchets a name into the
book rather than washing out on the next bar.

**THE DESIGN.** `p~ = p * exp(sigma_k z)`, i.i.d. per name-day, seeded; k in {0, 10, 25, 50, 100,
200, 400} bps with 8 seeds at every k > 0. The perturbed frame drives the band state, the eligible
set, `N_in` and every weight. **P&L, SPY and the live RULES v2 baseline are earned on the TRUE tape
at every k** (G7: comparand spread 0.000e+00 over all 3,136 rows), so anything that moves is a
decision movement and nothing else. Two tuned dials and no more: per-name cap {0.015, 0.020, 0.030,
INF} and gross {0.75, 1.00}. k, seed, panels {U56, B136}, rungs {0, 10, 25, 50} bps, weekly
cadence, band 0.03, MA 200d and the SHY sweep are reported, never selected on.

**THE ANSWER — THE VERDICT IS INVARIANT AT EVERY PLAUSIBLE k.** The committed U56 CAP2 cell (cap
2%, g 0.75, weekly, 10 bps) passes 4b on **8 of 8 seeds at every k out to 200 bps and 7 of 8 at 400
bps**; B136's passes 8 of 8 at every k including 400. Across the 25 of 64 cells that pass 4b at
k = 0, 4b survives in **100.0% of (cell x seed) draws at 10 and 25 bps, 99.5% at 50, 96.0% at 100,
86.5% at 200, 63.5% at 400**; 15 of 25 never flip on any seed, and the median first-flip k is
**300 bps — an order of magnitude beyond any plausible vendor disagreement, and larger than the 3%
band itself.**

**THE FRAGILITY MARGIN, PUBLISHED.** U56 committed cell across k = 0/10/25/50/100/200/400 bps:
CAGR 11.62 / 11.56 / 11.59 / 11.56 / 11.50 / 11.09 / 10.78%; Sharpe 1.2687 / 1.2631 / 1.2665 /
1.2643 / 1.2579 / 1.2172 / 1.1899; MaxDD -14.81 / -14.81 / -14.80 / -14.75 / -14.75 / -14.62 /
-14.36%; OOS Sharpe 1.3318 / 1.3263 / 1.3327 / 1.3358 / 1.3217 / 1.2872 / 1.2563. Out to 100 bps
the entire eight-seed RANGE of Sharpe (1.2517..1.2760) lies within 0.02 of the committed value.

**WHAT DOES BREAK IS TURNOVER.** The same cell trades 3.51 / 3.52 / 3.55 / 3.64 / 4.00 / 5.50 /
9.34x per year across k: **+14% at 100 bps, +166% at 400 bps**, while CAGR gives up 0.84 pp. The
gate-state disagreement share is 0.25 / 0.70 / 1.48 / 3.25 / 5.67 / 9.38% and the mean length of a
disagreement is **4.8 / 5.7 / 6.6 / 8.0 / 6.2 / 3.0 trading days** (G12): the hysteresis ratchet is
real, worth about a week, and self-limiting once the noise exceeds the band. Realised risk gross
moves by under 0.002 of NAV across the whole ladder, so this is a pure decision effect.

**THE CAVEAT THE RECORD SHOULD CARRY: THE RULE-8 PICK IS FAR MORE FRAGILE THAN THE VERDICT.** Over
784 picks, the (cap, gross) chosen on warm-up..2016-12-31 matches its k = 0 pick in only **91.4% of
draws at 10 bps**, 85.2% at 25, 82.0% at 50, 80.5% at 100, 46.9% at 200 and 35.9% at 400. Roughly
one committed rule-8 triple in twelve would have been a different triple under a 10 bps decision
error, at a noise level at which not one 4b verdict flips. Every published rule-8 pick in this
record should be read as one draw from that distribution, not as a determinate choice.

**4a: 4 of 3,136 rows, and all four appear ONLY at k = 400 bps on the cap-1.5% U56 arm** — noise
artefacts, not candidates. The live book's -12.05% MaxDD remains unreachable by this family.

**GATES: 14 of 14.** G3 reproduces the committed CAP2 (11.62% / 1.2687 / -14.81%, OOS 12.77% /
1.3318) and CAND (12.59% / 1.1934 / -17.39%, OOS 13.85% / 1.2397) U56 headlines to 4.98e-05; G1
replica == `engine.backtest` at 0.000e+00; G2 the k = 0 eligible set is bit-identical to
`baseline.band_state` & priced; G5 cost exactly linear (3.47e-18); G7 comparands bit-identical
across k; G8 the noise bites monotonically; G10 realised sd matches nominal k; G11 k = 0 is the
identity; G4 no leverage (peak gross 1.000000).

**SURVIVORSHIP (rule 9).** U56 / B136 are CURRENT constituents of their screens held from 2008, so
every absolute CAGR is optimistic and `L_CAGR` is the contaminated leg. The k-vs-k contrast is
same-tape, same-days, same-names and first-order immune to that bias; the absolute 4b verdicts are
not. SMALL is not priced (0 of 128 4b cells, idea 2383) — noise cannot mend three failing legs.
