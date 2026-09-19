# Idea 1362 (lane B, 2026-09-19) — the incumbent's 4b pass is not an execution bet, and N is not the turnover dial

**VERDICT: KILL for the N dial; the incumbent's cost robustness is CONFIRMED at 15x PROTOCOL's assumption.
No new book, no RULES change.** 168 cells published; 11/11 gates; outcome (E) COST-ROBUST fired as pre-declared.

1. **The pass does not die anywhere near a real cost.** U56, N=20, gross 0.75, weekly: 4b PASSES at all
   eight declared rungs — 15.82% / 1.1543 / -19.13% at 10 bps, **15.34% / 1.1235 / -19.21% at 25 bps**,
   14.54% / 1.0721 / -19.34% at 50 bps. Extending the same dial: it first fails at **150 bps**, fifteen
   times PROTOCOL's assumption. The idea's premise — "a book that needs 10 bps to pass is an execution
   bet" — is simply false for this book.
2. **Because cost does not attack the leg that binds.** 4b's binding margin is the drawdown cap
   (0.60 x SPY = -20.23%). Over the entire 0 -> 150 bps sweep MaxDD moves only -19.08% -> -19.92%: a
   turnover charge is a slow leak from the return stream, not a new source of loss. The first leg to
   break at 150 bps is **H1 Sharpe**, not the DD cap and not the CAGR floor.
3. **N is not the turnover dial the idea assumed.** An 8x widening of the book (N=5 -> N=40) cuts
   annualised turnover only 2.991 -> 2.257 on U56 (ratio **0.755**), 0.904 on B136, 0.850 on SMALL. The
   whole 25 bps drag spans 0.75% -> 0.56%/yr. The wider-N repair has at most ~19 bps/yr to give back, so
   it cannot work through cost — any gain it shows is a different mechanism wearing cost's clothes.
4. **So it buys nothing back, at either rung that matters.** At 25 bps nothing needs rescuing on U56.
   The only other passer, N=15, is **+0.0185 Sharpe over N=20, SE 0.0541, t +0.34** — inside its own
   paired circular-block interval (400 reps x 63-row blocks, seed 20260919, identical blocks both sides).
   At the 150 bps death rung, **0 of 7 N values pass 4b**.
5. **Rule 8 says the dial is worse than inert — it is costly.** N chosen on warm-up..2016 only by argmax
   IS net Sharpe at each rung, 2017-2026 read once: the chooser **loses at 24 of 24 (panel, rung) pairs**,
   mean -0.0628 (U56) / -0.2195 (B136) / -0.0436 (SMALL). U56's chooser takes N=40 at every rung and reads
   OOS 14.18% / 1.1221 against the frozen incumbent's 17.34% / 1.1862. H_HINDSIGHT, again.
6. **A panel fact the cost ladder exposes and should not be mistaken for a cost fact.** B136's N=20 fails
   4b at **every** rung including 0 bps (b_dd binds), while B136 N=15 passes at every rung. That flip is
   drawdown geometry on a wider panel, not execution. SMALL passes nowhere, at any N, at any rung.
7. **4a is 0 of 168** with the live book charged the same rung: a_dd is never true, because RULES v2's
   -12.1% MaxDD is unreachable for a 20-name momentum book. This is PROTOCOL rule 4's own stated reason
   for adding path 4b, reproduced here at every cost rung rather than at one.
8. **Honesty on the comparands.** At every rung the live RULES v2 baseline is charged that rung on its own
   turnover; SPY is buy-and-hold with its single entry trade charged too, so SPY's levels barely move and
   4b gets **harder**, not easier, as cost rises. Cost is a pure post-hoc charge on a fixed gross series
   (G3: exact to 2.95e-18) — the book never re-optimises against it, which is the conservative direction
   for the wider-N question.
9. **Replay.** The anchor (U56, N=20, 10 bps) reads 15.82% / 1.1543 / -19.13%, OOS 17.34% / 1.1862, worst
   |diff| **2.51e-03** against the committed 2026-09-04 figures — inside the 5e-3 tape-vintage floor, not
   exact, because commit 4e19a80 rewrote data/prices*.csv (idea 1350's finding). Stated, not rounded away.
10. **SURVIVORSHIP (rule 9).** U56/B136 are current constituents of hand-kept lists; SMALL is a current
    sub-$2B screen (54 tickers with max_1d_move >= 1.0 dropped). Every absolute level above is optimistic
    and none is an estimate of live expectancy. The cost ladder is a difference across rungs on the same
    books, so it is first-order immune; the pass/fail counts are not.

**What this licenses and what it does not.** It removes one objection to the standing 2026-09-04 4b
candidate — that its pass is bought with an optimistic 10 bps — with a 15x margin. It licenses **no**
change to N, and PROTOCOL rule 6 confines any rules change to the Sunday review in any case.
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are untouched by this run.
