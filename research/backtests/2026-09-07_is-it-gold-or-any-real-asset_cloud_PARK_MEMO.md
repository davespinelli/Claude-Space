# PARK memo — `GLD+UUP` two-leg sleeve (idea 105, cloud 2026-09-07)

1. **Candidate.** `top20 + 50% (GLD, UUP)` at g = 1.00 — idea 100/102's sleeve with TLT *and*
   DBC deleted; 2 assets instead of 4, same idea-18 variant-B machinery, weekly, 10 bps.
2. **Numbers (10 bps, next-day).** u56 12.24% / **1.170** / −14.65%, H 1.109/1.229, OOS 13.09%
   / **1.259** / −14.65%, 12.4×/yr. broad 12.67% / 1.081 / −16.02%, H 1.175/0.989, OOS 12.05%
   / 1.042 / −16.02%, 15.1×/yr. SPY 15.23%/0.889/−33.72%, OOS 0.882.
3. **Path.** 4b on **both** panels at 10 bps. 4a: **fails** (0/640) — it does not beat RULES v2.
4. **Why it is interesting.** Highest dSharpe retention of 16 arms (99.1% of idea 102's arm
   with one fewer asset); highest OOS Sharpe of 16 arms at f=0.50 (**1.2651**); the **only**
   arm holding a cross-universe 4b pass to **20 bps**; dominates S4 and noDBC at every cost
   rung on both panels.
5. **BLOCKER — why this is PARK and not KEEP.** Rule 8's pre-registered IS selector picks it
   in **0 of 8 cells** (it takes `sub_TIP` 5/8, `noDBC` 3/8). The arm was found by reading the
   OOS table. Adopting it would be out-of-sample-informed selection.
6. **Secondary blockers.** (a) 4a-negative on RULES v2's own terms. (b) The pure-ballast null
   `UUPonly` also clears 4b, so 4b is not carrying the claim; the real margin is **+0.135 u56
   / +0.133 broad** Sharpe over that null. (c) broad H2 = 0.989 — the weak-second-half
   signature ideas 101/106 flagged. (d) Written at **g = 1.00**, the convention where lane B's
   idea-106 correction found the `noDBC` prune's sign flips; untested against that.
7. **What would clear blocker 5.** A pre-registered selector that reaches this arm on
   2009-2016 alone — e.g. select on IS *dSharpe retention per asset* rather than IS Sharpe —
   run over the same 16-arm grid, with the selector fixed before the OOS window is read.
   Failing that, a third panel (SMALL439 or a point-in-time megacap set) on which the arm's
   4b pass and 20-bps reach reproduce without any selection.
8. **What would clear blocker 6d.** Re-run the arm at natural gross and at the record's
   de-gross/gate conventions; if the 20-bps reach is g=1.00-specific it is a convention
   artefact, not a sleeve.
9. **Exact RULES wording, if and only if both blockers clear at a Sunday review** (this is
   draft text, NOT adopted; RULES.md is untouched by this run):
   > *Clause S — macro leg.* Hold 50% of NAV in a two-asset macro leg of **GLD and UUP**,
   > weighted by the trend vote (fraction of {12-1m, 6m, 3m} returns above zero, in
   > {0, 1/3, 2/3, 1}) times inverse-60-day-volatility risk parity, row-normalised. The
   > remaining 50% holds the equity book. Rebalance weekly with the book; rescale the combined
   > row to 1.00 gross. **No TLT, no DBC, no other commodity or metal** — see idea 105.
10. **Do not adopt this week.** No RULES change is proposed. The reportable finding of idea 105
    is the hypothesis test (§1-§3 of the result), which stands on its own and blocks any
    future "macro sleeve" / "precious-metals" wording regardless of what happens to this arm.
