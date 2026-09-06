# Idea 228 — does-any-dial-argmax-move-with-cost (lane C, 2026-09-06)

**Verdict: KILL of idea 155's stated mechanism; the queue's conditional is a qualified HIT.**
The cost rung *can* re-rank a dial — it does so in **3 of 12** panel × dial cells — but never
above the protocol's own 10 bps rung: **0 of 12 argmaxes move anywhere in 10→30 bps**, and all
3 moves happen in the 0→10 bps stretch. Between 10 and 30 bps the ladder is a level check, not
a chooser, on every dial tested.

**What idea 155 got wrong.** Its explanation — Spearman(q, turnover) = −1.000, therefore a rung
shifts the level and not the argmax — does not generalise, and is not even the right sign of
association. Monotone turnover holds in **8 of 12** cells here, and **all 3 re-ranking cells sit
inside that monotone group** (3/8), while the 4 non-monotone cells re-rank **0/4**. Perfect
turnover monotonicity is neither necessary nor sufficient for an immovable argmax; it was a
coincidence of the q dial. The parent's own q rows re-read from its committed grid reproduce
exactly (ρ = −1.000 on all three panels; 1/1/2 distinct argmaxes), so this is a reinterpretation
of idea 155's numbers, not a contradiction of them.

**The census** (665 points = 3 panels × 4 dials × 7 cost rungs; every point in `.grid.csv`).
Construction held fixed across dials: top-n equal weight, no vol scaler, gross 1.00, over the
band-gated 200d ∧ vol20 eligible set; defaults n=20, g=0, max_vol=0.60, k=1 week.

| panel | dial | ρ(dial, turnover) | turnover range /yr | argmax 0→30 bps | re-rank? |
|---|---|---|---|---|---|
| U56 | N (count) | −1.000 | 6.7–27.6 | 40 at all 7 rungs | no |
| U56 | G (200d band) | −1.000 | 10.6–12.8 | 0.12 at all 7 | no |
| U56 | V (vol cap) | −0.976 | 12.2–14.3 | off (5.00) at all 7 | no |
| U56 | K (cadence) | −1.000 | 3.3–12.8 | **1w → 6w at 5 bps** | **yes** |
| B136 | N | −1.000 | 11.4–32.1 | **40 → 56 at 10 bps** | **yes** |
| B136 | G | −0.964 | 17.7–18.4 | 0.12 at all 7 | no |
| B136 | V | −1.000 | 17.5–25.7 | 0.80 at all 7 | no |
| B136 | K | −1.000 | 4.7–18.4 | 4w at all 7 | no |
| SMALL484 | N | −1.000 | 21.3–48.3 | 15 at all 7 | no |
| SMALL484 | G | −0.964 | 27.8–27.9 | 0.02 at all 7 | no |
| SMALL484 | V | −0.762 | 21.8–34.7 | off (5.00) at all 7 | no |
| SMALL484 | K | −1.000 | 6.1–27.9 | **1w → 6w at 5 bps** | **yes** |

**Cadence is the one dial the ladder actually chooses** (2 of 3 panels), and it is also the only
dial where ignoring cost is expensive: picking the 0-bps argmax and then paying 30 bps costs
**0.155 Sharpe (U56/K)** and **0.230 (SMALL484/K)**, against **0.018** for B136/N and **0.000 in
the remaining 9 of 12 cells**. That number, not the argmax table, is what a cost rung is worth as
a chooser.

**Mechanism, and it is not turnover monotonicity.** A rung re-ranks a dial iff the 0-bps top-two
gap is smaller than the tilt the ladder applies across that pair. Comparing gap against the
maximum 30-bp Sharpe-slope spread predicts **9 of 12** cells and catches **3 of 3** actual
re-ranks with no false negatives (3 false positives: B136/K gap 0.0199 vs tilt 0.0702,
SMALL484/N 0.0348 vs 0.0402, SMALL484/G 0.0011 vs 0.0050 — near-ties where the tilt is spread
over the losers rather than concentrated on the runner-up). It is a necessary condition, not a
sufficient one. `.mechanism.csv` carries both columns for every cell.

**Rule 8 (dial chosen on 2009–2016 at each rung, 2017–2026 read once; 84 cells).** Overall the
IS chooser beats do-nothing by **+0.0177** mean OOS Sharpe, winning 59.5% of cells, against a
random dial's **−0.0306** — so this is *not* an eleventh clean selection-loses instance. But the
whole premium is one dial: **V +0.1049** (85.7% wins, +0.213…+0.376 on SMALL484), which is the
chooser discovering the corner "switch the vol20 gate off" — the same finding ideas 38/49 made
directly. **Excluding V, the chooser is −0.0113 over 63 cells and wins 50.8%**, i.e. a coin flip,
which is the record's usual reading. The rung changes the IS pick in only **4 of 12** cells, and
where it does the OOS consequence can be large: U56/N picks n=3 at 0–25 bps (−0.10 to −0.13 vs
do-nothing) and n=40 at 30 bps (+0.137).

**OOS levels at 10 bps** (2017-01-01→2026-09-04): do-nothing book **U56 1.1683 / 19.22% /
−23.98%**, B136 0.8937 / 16.51% / −26.20%, SMALL484 0.5116 / 9.71% / −35.22%; RULES v1 baseline
0.7471 / 0.5763 / 0.5540; SPY 0.8820 / 15.45% / −33.72%. Full sample at 10 bps, do-nothing
(n=20): U56 CAGR 16.89%, Sharpe 1.0922, MaxDD −23.98%, H1 1.088 / H2 1.102; RULES v1 6.45% /
0.6642 / −13.83% (0.641/0.688); SPY 15.23% / 0.8890 / −33.72% (0.957/0.834).

**KEEP paths, all 665 points.** 4a **50/665** — B136 44 (G 14, N 13, V 12, K 5), SMALL484 6 (all
V), **U56 0 of 217, always on drawdown against the live low-vol book** (idea 136's standing
diagnosis, reproduced again). 4b **12/665, all on U56**: n=40 clears at **all 7 rungs** (10 bps:
CAGR 12.95%, Sharpe 1.1236, MaxDD −18.38%, H1 1.073 / H2 1.172, OOS 1.2656, 6.7x/yr turnover)
and max_vol=0.30 clears at 0–20 bps. **B136 and SMALL484 pass 4b 0 of 448** — the sixteenth
reproduction of idea 136 on the small panel.

**The U56 n=40 pass is PARKed, not proposed,** for three reasons in this run's own output: it
runs at **86.3% mean invested against n=20's 95.5%**, so part of the pass is idea 157's cash
channel and not selectivity; n=40 is a full-sample argmax that the IS chooser picks at exactly
one of seven rungs; and it fails 4b on B136 (drawdown, −25.06% vs a −20.23% cap), so it is a
one-panel book. Per idea 144 a re-dialled book is the same book. No RULES change, no memo.

**Reproduction.** The cost identity `net(c) = gross − turnover·c/1e4` matches
`engine.backtest(cost_bps=10)` at **6.9e-18 / 6.9e-18 / 1.4e-17** on the three panels, which is
what makes the seven rungs exact rather than re-simulated. `simulate()` is engine's loop with an
arbitrary k-week mask; k=1 is engine's own `freq="W"`.

**Caveats.** Current-constituent survivorship on `universe_broad.json` and the small panel (idea
54) — every arm inherits it equally, so the census's argmax comparisons are unaffected but no
*level* here is tradable. Four dials on one construction is not the whole record; a dial swept
on a different book could behave differently, and the three cells the mechanism test
over-predicts show the margins are thin. The 0-bps rung is a counterfactual, not a tradable
point. Daily cadence is excluded (idea 38's index caveat); the K dial starts at 1 week.

**Follow-ups queued:** 230, 231, 232.
