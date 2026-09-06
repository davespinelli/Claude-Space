# Idea 274 — is RULES v2 only a de-grossing effect? (lane C, 2026-09-06)

Script: `research/backtests/2026-09-06_is-RULES-v2-only-a-de-grossing-effect_C.py`
Grids: `_grid.csv` (400 rows), `_headline.csv`, `_nullbands.csv`, `_walkforward.csv`.
Panels u56 + broad (survivorship: current constituents only), rungs 0 and 10 bps, weekly, t+1.
One tuned parameter: the CG control's constant gross (17-rung ladder, every rung reported).

## Verdict: **ANSWERED / SPLIT.** The CAGR ceiling is structural (confirmed). The Sharpe
edge is real on u56 but absent in-sample and absent on broad. The only thing the gate
buys on every panel, every rung and against both nulls is **drawdown**.
**No KEEP-candidate, no RULES change** (4a 0 of 396 rows).

## Reproduction
`rules_v2_weights` on u56 @10bps re-runs the CHANGELOG's published digits exactly:
CAGR 8.66% (pub 8.66), Sharpe 1.20562 (1.2056), MaxDD -12.055% (-12.05), halves
1.22593/1.19084 (1.2259/1.1908), turnover 1.774x (1.77).

## The exposure fact
Nominal gross 0.75, **realised mean gross 0.5328** (IS 0.5278 / OOS 0.5369, sd 0.1505,
range 0.067..0.737); gate on-share 0.6864; corr(gross_t, SPY next-60d return) **-0.230**.
So every un-matched comparison against a 0.75 book is 29% an exposure comparison.

## Controls
- **CG(g)** — no gate, constant nominal gross g, equal weight over priced names.
- **RGT** — each name's gate series circularly rotated by an independent random shift
  (preserves on-share, persistence and turnover; destroys timing). 60 draws u56 / 20 broad.
- **RGP** — the same gate with its column labels permuted (preserves the daily in-band
  count exactly, so the gross path and its timing are identical; destroys only *which*
  names). Both nulls are turnover-matched by construction (1.774 / 1.795 vs v2's 1.774),
  so this is an information test, not idea 262's turnover test.

## 1. Gross is not a Sharpe dial, so the CAGR ceiling is structural
The CG ladder's Sharpe is **flat**: 1.1221 -> 1.1245 across gross 0.20 -> 1.00 on u56
(span **0.0023**; broad span 0.0013), while CAGR runs 3.50% -> 17.74% and MaxDD
-6.40% -> -29.18%. For an un-gated book gross is a pure CAGR/MaxDD scaler. Hence v2's
8.66% is a *choice of exposure*, not a limit imposed by the gate — and at matched
realised gross the gate is CAGR-**negative**: v2 8.66% vs CG(g*=0.55) 9.70% on u56
(**-1.04 pp/yr**) and 8.03% vs 10.35% on broad (**-2.32 pp/yr**). The queue's second
clause is confirmed.

## 2. Sharpe: not a de-grossing effect on u56, but not in-sample either
u56 @10bps: v2 1.2056 vs CG(g*) 1.1235 (**+0.0821**, and +0.081 against *every* rung of
the ladder), 96.7th percentile of RGT (2 of 60 draws beat it) and 95.0th of RGP (3 of 60),
z +1.88 / +1.30. Breakeven **56.5 bps**, so it is not a turnover artefact.
**But rule 8 kills the reading:** on 2009-2016 alone v2's Sharpe is **1.1043 against CG's
1.1116** — a chooser with no OOS information does *not* pick the live book at 10 bps
(it picks CG g=1.00: OOS 1.1353/-29.2% vs v2's 1.2851/-12.1%). v2's entire Sharpe
advantage lives in 2017-2026. Another idea-229 selection-loses instance, and by idea
111's standard an OOS-window statistic.

## 3. Broad: here it *is* only a de-grossing effect, and a losing one
broad @10bps: v2 Sharpe 1.1058 sits at the **40th percentile of RGT** (12 of 20 draws
beat it, z +0.07) and the **0th of RGP** (20 of 20 beat it, z -1.88); its CAGR is 0th
percentile of RGT (z -4.17). CG(g*) beats it on Sharpe (1.1217) *and* CAGR (10.35%).
Breakeven **2.30 bps** — the residual edge is gone at PROTOCOL's own rung.

## 4. What the gate actually buys: drawdown, unanimously
v2's MaxDD is the **best of every draw of both nulls on both panels at both rungs** —
0 of 60 (u56) and 0 of 20 (broad) rotated or permuted gates are shallower; z +1.90 /
+2.85 (u56) and +5.36 / +3.81 (broad), and -12.05% against CG(g*)'s -16.90% at the same
average exposure. This is the one claim in the book that survives matched gross, both
nulls, both panels and rule 8.

## 5. KEEP paths
**4a 0 of 396** — nothing in the grid beats the live book on both halves with no
drawdown regression. **4b 3 of 396**, all of them un-gated CG rungs on u56
(g=0.60 and 0.65 @0bps, **g=0.65 @10bps**: 11.48% / 1.1238 / -19.75%, halves
1.1895/1.0720, OOS 1.1358). It is a **one-rung knife edge and is PARKed, not KEPT**:
g=0.60 fails the CAGR bar by 0.07 pp and g=0.70 fails the drawdown bar by 0.9 pp, so the
whole 4b window is 0.05 of nominal gross wide — inside idea 154's +/-0.03 realised-gross
grid band — and neither walk-forward selector lands on it (IS-argmax picks g=1.00,
IS-gross-match picks g=0.55; both fail 4b OOS on DD and CAGR respectively).

## Reportable
Any future claim about the band gate must publish **realised** mean gross beside it, and
must be read on drawdown rather than Sharpe: the Sharpe number is u56-only and
out-of-sample-window-only, while the drawdown number is outside every null everywhere.
