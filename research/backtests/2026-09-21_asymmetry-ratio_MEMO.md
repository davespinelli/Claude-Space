# MEMO — idea 2075 (lane C, 2026-09-21): the asymmetric drift trigger, if the record wants one

1. **This memo does NOT propose a rules change.** The standing KEEP-4b candidate (idea 2026: U56,
   FRACG `f = 0.10`, `t = 0.16`, monthly, 10 bps — full 15.81% / 1.2470 / -19.12%, OOS 16.55% /
   1.2928 / -19.12%) is NOT displaced by any rung of the down/up ratio dial. It stands unchanged.
2. Pre-stated cells clearing 4b FULL+OOS exist at `A = 4` (8 of 12 large-panel cells, the same 8
   its symmetric twin clears), so PROTOCOL rule 5 asks for exact wording; it is given below and
   should be adopted ONLY if a Sunday review wants the drawdown credit for its own sake.
3. **The rung is 2, not 4.** Pooled over 60 (arm x base) pairs at `t*`, 10 bps: `A = 2` buys
   +0.708 pp of OOS MaxDD for -0.201 pp of OOS CAGR (3.52 pp per pp), against 2.77 at `A = 4`,
   2.98 at 8 and 2.35 at 16. 87% of the peak credit is collected at the first rung off symmetric.
4. **RULES wording, exact, if adopted** — replaces nothing in RULES v2 clause 2; it modifies the
   VOLTGT refresh clause of the standing KEEP memo only:
   > *Re-read the exposure scalar `g_t = clip(t / sigma20_panel, 0, 1)` on any day the book's held
   > gross has drifted BELOW `g_t` by more than `f * g_t`, or ABOVE `g_t` by more than
   > `f * g_t / 2`, with `f = 0.10` and `t = 0.16`. On a re-read, re-spread to `g_t`. Names are
   > re-spread on the scheduled monthly trade day at the scalar then in force. Gross is never
   > levered above 1.00.*
5. Numbers for that exact cell (U56, monthly, 10 bps, t+1): full **15.28% / 1.2260 / -19.13%**,
   halves **1.2681 / 1.1891**; OOS **15.97% / 1.2684 / -19.13%**; 1.53 turns/yr, 14.2 refreshes/yr.
   vs SPY 15.12% / 0.8843 / -33.72% (OOS 15.26% / 0.8737 / -33.72%). All five 4b legs clear.
6. **Path 4a: KILL**, at every one of the 420 large-panel cells at `t*`, 10 bps — the book's
   drawdown is deeper than live RULES v2's -12.05%, exactly as PROTOCOL 4b anticipates.
7. **Do NOT ship `A = 4`.** It costs 0.09 pp more OOS CAGR than `A = 2` for 0.10 pp of drawdown,
   and at the FIXH base it narrows the cost band: `A = 4` clears 4b at 0 and 10 bps and fails at
   25 and 50 on `L4_DD`, where the standing `A = 1` book clears all four rungs.
8. **Do NOT ship a DOWN-ONLY trigger.** With no up-side threshold the book has no re-entry channel
   and is absorbing at gross 0 on 360 of 360 cells; the repaired trade-day-re-read version weakly
   dominates its matched twin on 1 of 60 pairs and loses 0.198 pp of OOS CAGR and 3 of 58 4b passes.
9. **Do NOT use `C_ISDD` as a legal chooser** on any corpus a de-grossing dial can drive to zero:
   a book holding nothing has in-sample MaxDD exactly 0, and it picked that book on 12 of 12 cells.
10. **Caveats.** Survivorship-biased current-constituent panels (levels optimistic, contrast not);
    point estimates with no SE — idea 2060 found the 4b CAGR margin unresolvable at 95%, so the
    0.1-0.9 pp deltas above are likely inside their own noise; `t = 0.16` is inherited, not chosen.
