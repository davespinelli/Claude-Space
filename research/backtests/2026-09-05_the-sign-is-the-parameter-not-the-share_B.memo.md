# Memo to the Sunday review — idea 168, the tilt exponent (lane B, 2026-09-05)

1. **Not a new book.** Every 4b passer here is idea 153's existing candidate (n ≈ 0.53 × mean
   eligible, no vol scaler) re-read at a different exponent. Nothing new is proposed for capital.
2. **What is new** is that the exponent k in `composite · vol20^k` is on a **monotone** curve, not
   a humped one: CAGR rises across the whole ladder and the beneficial band is open at the top
   edge in 12 of 12 large-cap cells at 10 bps.
3. So the project should stop saying "k = 0 is the optimum". It is not an argmax; it is the
   point where the *Sharpe* curve goes flat (±0.02 over k ∈ [−0.25, +1.00] on u56 m = 0.53)
   while CAGR keeps buying vol at par.
4. **The live k = −0.5 is the one implementable point on the wrong side of 4b.** At u56 lit
   m = 0.53, 10 bps it fails 4b on the CAGR floor (9.90%/0.996); one rung up at k = −0.25 it
   passes full-sample and OOS; at k = 0, 12.66%/1.092/−18.3%, OOS 14.36%/1.168.
5. In 12 of 12 large-cap cells at 10 bps the lowest k passing 4b is ≥ −0.25; k = −0.5 passes in
   **1 of 12**. RULES v1 on the same panel at 10 bps: 6.45%/0.664, OOS 7.73%/0.747.
6. Rule 8: an IS-fitted chooser of k beats the do-nothing constant in **18 of 36** cells — the
   fifth coin flip after ideas 110/151/132/166. Do not fit k.
7. What *does* transfer OOS is the sign, not the level: S_INV (k = −0.5) is last of four
   selectors in every large-cap cell, by 0.16 Sharpe and 4.0 pp/yr.
8. Nothing survives 25 bps: zero 4b passers full-sample at any k, on any panel. The H1 bar binds.
9. **Exact RULES wording, if and only if the Sunday review adopts idea 153's candidate** — this
   clause replaces the `/ sqrt(vol20)` in the v1 score and is a deletion, not a new dial:
   > **Scoring.** Rank eligible names by the momentum composite alone. Do **not** divide or
   > multiply the composite by any power of `vol20`; the vol scaler is deleted, not tuned.
   > `vol20` remains in the eligibility test (rule 2) only.
10. **Do not** adopt the positive exponent the CAGR curve points at. It is a grid-edge argmax,
    it is Sharpe-neutral, it reverses sign on the small panel (Spearman −0.80…−0.98, 18 of 18
    cells), and PROTOCOL rule 7 does not let a monotone slope's endpoint become a parameter.
