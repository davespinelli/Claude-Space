# AMENDMENT MEMO (not a new candidate, not a rules change) — idea 2412, lane B, 2026-09-23

**What this memo is.** Idea 2391 filed `CAP2 + symmetric damper lam = 0.40` as a 4b KEEP-candidate,
FILED NOT ADOPTED, because its B136 drawdown margin was only 0.71 pp. This run prices the asymmetric
form and finds the exit damping is PURE COST: at EVERY matched `lam_in`, on BOTH panels and BOTH books,
un-damping the sell side improves Sharpe, OOS Sharpe and MaxDD and restores held-set fidelity to exactly
100% (gate G13) and the post-trade stub to zero (G12). It is a strict dominance, 56 of 56 matched pairs.

**It does NOT replace idea 2391's candidate and is NOT filed as one.** It is a KILL as the turnover
device it was proposed as: `FASTEXIT` gives back 40–60% of the cut (U56 CAP2 3.51 -> 2.81x/yr vs SYM's
2.34x) and loses the joint both-panel 50 bps 4b that was idea 2391's entire case. Rule 8 does not reach
it either: over 32 IS-only picks the exit rule lands SYM 24 / FASTEXIT 8 / FASTDOWN 0, and `lam_in` 0.40
gets ZERO picks. 4a is 0 of 672 rows.

**EXACT RULES WORDING, to be attached to idea 2391's clause 4 IF and ONLY IF that damper is ever adopted:**

> 4. Each week, move every risk name a fraction `lam = 0.40` of the distance from its held weight to its
>    target `min(0.75 / N_in, 0.02)` of NAV, and hold the residual in SHY. **A name the 200d +/-3% band
>    gates OUT is EXEMPT from the damper and is sold in FULL at that week's rebalance.** The damper
>    applies to purchases and to re-sizings of names the band still holds; it never delays an exit.

**Why the exemption and not the whole device.** The damper's only published bill was on the sell side
(post-trade stub 1.84% / 2.52% of NAV, held-set fidelity 76.1%, mean names held 37.6 -> 50.7). The
exemption removes that bill exactly and costs 0.43 pp of CAGR on U56 at 10 bps, buying +0.0354 Sharpe,
+2.96 pp of drawdown and +0.0706 OOS Sharpe. It is a SAFETY clause, not a return claim.
