# MEMO — idea 1555 (lane B, 2026-09-19): where should gated-out weight go?

1. **FINDING.** Seven destinations for RULES v2's band-gated weight, raced at identical selection,
   identical cadence and identical 100% of NAV (G frozen 0.75, 210 cells, all published). **Path 4a:
   10 cells full, 8 full AND OOS — every one of the 8 is SHY on the LIVE frame, all four F rungs on
   U56 and all four on B136.** Best cell U56/LIVE SHY F = 1.00: full **9.12% / 1.2675 / -11.48%**,
   halves **1.278 / 1.264** vs live **1.228 / 1.181**, OOS **10.14% / 1.3560 / -11.48%** vs live OOS
   1.2769, turnover 1.77 -> 2.80x/yr, charged. This is idea 1498's standing candidate, replayed here
   to the committed decimal (G3) — **no new book**; what is new is that it now survives two controls.
2. **CONTROL 1 — THE FRAMING SURVIVES.** 1358's ladder was SHY/IEF/TLT, all bonds. Adding an EQUITY
   sleeve tests whether 1498's result is "cash earns something" or "the band under-deploys". **SPY
   clears 4a at 0 of 30.** On U56/LIVE it buys +8.27 pp/yr of CAGR (8.51% -> 16.78%) and pays
   **0.1516 of Sharpe and 18.24 pp of drawdown**, monotone in F at 4 of 4 rungs. The de-gross is
   buying real risk reduction; only a LOW-VOL residual keeps it.
3. **CONTROL 2 — THE COMPETING FIX IS KILLED.** Idea 1454 read the live book's 4b failure as a CAGR
   floor problem and proposed abolishing the cash leg (G = 1.00). Made conditional as RESPREAD, it
   **loses to SHY on Sharpe at 6 of 6 panel-frames (mean -0.0630 full, -0.0725 OOS) and on MaxDD at
   6 of 6 (mean -12.20 pp deeper)**, winning only CAGR (6 of 6, +5.39 pp), at turnover 1.77 -> 5.68x/yr.
   It is the de-gross ray, paid for at full price. **1454's proposed fix should not be enacted.**
4. **AS A TUNED DIAL THE AXIS IS A KILL (rule 8), REPRODUCING 1358 ON AN INDEPENDENT GRID.** Fit on
   warm-up..2016-12-31 only, 2017-2026 read once: **C_SHARPE picks IEF x3 / TLT x3 and never finds
   SHY**, mean OOS dSharpe **-0.0274** vs doing nothing, beats it **1 of 6**; C_CAGR **-0.0699**,
   **0 of 6**. The ex-post best 4b cell of all 210 (U56/LIVE GLD F = 0.50, OOS 13.26% / 1.4204 /
   -13.70%) is reached by no chooser. H_HINDSIGHT fires again. **Enact the destination as REALISM,
   never as a knob.**
5. **4b.** 40 of 210 full AND OOS, none of them a new book; U56/INC SHY inherits the 2026-09-04
   candidate's 5 passes. The live LIVE-frame book still fails 4b on the CAGR floor at every
   destination except the ones that buy it with beta, exactly as 1454 and 1498 found.
6. **EXACT RULES WORDING (proposed, Sunday review only — rule 6):**
   > *Residual.* Weight gated out by clause 2 is held in **SHY** (1–3y US Treasury ETF), rebalanced
   > on the same weekly grid as the book and charged the same 10 bps per unit of turnover. It is
   > never re-spread over the names still in the band, never shorted and never levered: invested
   > weight plus residual weight equals 1.0. The residual instrument is FIXED at SHY and is not a
   > tuned parameter. SHY remains separately selectable by the score; a name may be held both ways.
7. **WHAT THE BOOK ACTUALLY IS, STATED PLAINLY.** RULES v2's realised mean gross is **0.5328 (U56) /
   0.5322 (B136) / 0.4051 (SMALL)** — published, not asserted (G8c). At F = 1.00 the 4a candidate
   therefore holds a mean **46.7% of NAV in short Treasuries**. It is a half-bond book. Its 4a win is
   **DIVERSIFICATION, NOT ALPHA**: CAGR rises only +0.50 pp; vol falls.
8. **CAVEATS.** (a) There is **no zero-duration instrument in the committed cache** (no BIL, no SHV),
   so SHY is the cheapest proxy available and it is marked to market — own profile FULL 1.31% /
   0.958 / **-5.71%**, OOS 1.72% / -5.71%. Every "credit the cash" number in this record is optimistic
   for the ZIRP years and carries genuine duration risk afterwards. (b) The 4a pass is **LIVE frame
   only and large-cap only**: 0 of 30 on SMALL, 0 of 30 on INC. (c) GLD reaches a higher Sharpe than
   SHY at F = 0.25 (1.2770 vs 1.2675) but fails 4a on drawdown and is picked by no chooser; its 9
   4b passes are hindsight. (d) Survivorship (rule 9): U56 / B136 are current-constituent lists,
   SMALL a current sub-$2B screen — absolute levels are upper bounds; the destination CONTRAST on
   the same names and days is first-order immune.
9. **GATES 8/8**, including G1 destination invariance at F = 0 (**0.000e+00** across 6 dests x 6
   panel-frames), G2 `baseline.rules_v2_weights` replay **1.249e-16** on all three panels, G3 idea
   1498's two committed U56 SHY cells reproduced exactly, G4 no leverage (max deployed 1.000000000000),
   G6 no chooser input reads a row on or after 2017-01-01.
10. Script `research/backtests/2026-09-19_where-should-gated-out-weight-go_B.py`; 210 cells in
    `.grid.csv`, 6 head-to-head rows in `.headtohead.csv`, 18 chooser picks in `.walkforward.csv`,
    gates in `.gates.csv`, full transcript in `.log.txt`. **NOT ENACTED — rule 6 reserves enactment
    for the Sunday review.**
