# Memo to the Sunday review — idea 159 (lane B, 2026-09-05). No RULES change proposed.

1. Idea 159 asked for a number: the book share above which a cross-sectional key is arithmetic
   noise. **The number does not exist.** It is not missing for want of data — it is undefined.
2. A crossing requires the tilt's gross value g(m) to decay in share faster than its cost c(m).
   Bootstrapped (block 21 d, 2000 reps, seed 159), d = slope(log g) − slope(log c) straddles zero
   in **6 of 6** (panel, tilt) cells: u56 INV +0.032 [−1.186, +1.097], broad INV +0.173
   [−0.781, +1.274]. The curves are parallel in logs.
3. Mechanism, arithmetic: both the value and the cost of a tilt scale with the number of names it
   moves, and book share is exactly what governs that count (idea 153). Share scales numerator
   and denominator alike, so g/c is flat: **1.95 / 1.83 / 2.20** at m = 0.05 / 0.53 / 1.00 on u56.
4. On the *honest* cost bar (the exact incremental cost of holding the tilted book over its
   control) the tilt is affordable by 1–3 orders of magnitude at every share: **g/c = 16–4254**
   on u56, 9–193 on broad.
5. So the live vol scaler is not too expensive to run. At the incumbent's own share (u56, m=0.53,
   n=20) it has 2.68 pp/yr of magnitude available against 0.083 pp/yr of true incremental cost —
   and it spends it as **−2.68 pp/yr**, negative at **all 10 shares on u56 and all 10 on broad**.
6. **Proposed PROTOCOL rule-9 reporting clause** (reporting only, no bar changes): *a claim that
   an instrument "stops paying" above some level must report the ratio of its realised magnitude
   to its cost across that level, not the two curves separately; a ratio whose log-slope
   difference straddles zero has no threshold and no threshold may be quoted from it.*
7. Rule 8: an m\*-gated selector returns mean OOS Sharpe **0.7212** over 12 cells against
   **0.8044** for doing nothing (wins 1 of 12) and 0.7005 for plain IS-Sharpe; RULES v1 0.4514,
   SPY 0.882. All four selectors lose to SPY.
8. No new book. 4b passes are idea 153's known set on a finer grid (17/90 literal, 24/90
   gross-normalised, at 10 bps); **0 of 90 at 25 bps**; INV passes 2 of 60, both at m ≥ 0.85
   where the tilt is degenerate. Nothing is proposed.
9. This is a fifth independent "delete the vol scaler" (after ideas 72, 82, 141, 160, 162) and the
   first that separates cost from direction and finds only direction guilty.
10. Caveats: survivorship on all three current-constituent panels; the small panel's gate is
    inverted (ideas 39/49); the block bootstrap measures sampling error around one realised path.
