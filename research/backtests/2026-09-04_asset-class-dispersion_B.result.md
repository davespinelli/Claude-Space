# Idea 73 — asset-class-dispersion: **KILL** for dispersion as a universe clause

Run: `research/backtests/2026-09-04_asset-class-dispersion_B.py` (lane B, 2026-09-04).
35 points (7 panels × {EWall, v1, CAND-5/10/20}), all reported, 10 bps, weekly, t+1, 75% gross,
common window 2011-01-13 → 2026-09-03 so every panel is judged on identical days.
Harness reproduces idea 2's KEEP row (U56/CAND20 12.7% / 1.093 / -18.3%, halves 1.088/1.103) and
the live v1 row (6.5% / 0.666 / -13.8%) to the decimal on universe.json's own window.

1. **The premise is true as a fact about the panels.** Mean cross-sectional sd of 12-1 momentum over
   the eligible set: ETF24 0.129 < ETF36 0.145 < B136 0.257 < BSTK100 0.278 < U56 0.281 < STK20 0.378
   < SMALL484 0.682. The ETF panels really do have 2.6× less to sort than the mega-cap stock panel and
   4.7× less than small caps, and the ordering is stable across halves.
2. **The inference from it is false.** Across panels the *net* ranking premium (CAND-n Sharpe minus the
   same panel's equal-weight-all-eligible Sharpe, same days/gate/gross) has Spearman **-0.107 / -0.071 /
   -0.071** with dispersion at n = 5/10/20 — nil to slightly negative. The single largest premium in the
   whole run is **ETF36/CAND20 at +0.228 Sharpe (t +2.41)**, on the *second-lowest* dispersion panel;
   the highest-dispersion panel (SMALL484) has the worst net Sharpe of all 21 CAND points (0.493).
3. **The gross selection spread tracks candidate count, not dispersion.** Spearman(sd, gross spread) is
   +0.429/+0.679/+0.357, but Spearman(n_elig, gross spread) is **+0.571/+0.857/+0.964** — and the two are
   confounded across panels (SMALL484 is both widest and largest). "More names to choose from" explains
   the cross-panel pattern better than "more spread between them".
4. **Within a panel, over time, dispersion pays nothing.** Terciles cut on an expanding quantile of each
   panel's own dispersion history (no look-ahead): high-dispersion weeks beat low-dispersion weeks in
   only **2 / 2 / 3 of 7 panels** at n = 5/10/20. Pooled with panel fixed effects (4,877 panel-weeks),
   corr(dispersion percentile, weekly selection spread) = **-0.006 / -0.015 / +0.001, |t| ≤ 1.01**. This
   is the test with power, and it is flat.
5. **Rule 8 rejects it outright.** S3, the pre-registered dispersion rule (highest 2009-16 mean dispersion
   at n=20), picks **SMALL484 → OOS 7.6% / 0.506 / -26.3%, FAILING every OOS 4b bar** and finishing last
   of the seven panels. S1 (IS Sharpe) picks STK20/CAND10 → OOS 21.2%/1.366/-17.3% **PASS**; S2 (4b-aware)
   picks STK20/CAND20 → OOS 14.0%/1.449/-12.1% **PASS**. Spearman(IS dispersion, OOS Sharpe) = **+0.134**
   over the 21 points (+0.143 over the 7 panels at n=20) against Spearman(IS Sharpe, OOS Sharpe) = **+0.710**.
   The panel choice *is* predictable out of sample — dispersion is simply not what predicts it.
6. **Idea 10's ETF KILL is re-explained.** The ETF book fails on the *level* of return, not on the ranking:
   ETF36/CAND20 6.6% CAGR against the window's 9.91% 4b floor, while its ranking premium is the best in the
   run. Ranking is not what breaks on ETFs; expected return is.
7. **Nothing is upgraded.** The only 4b passes are already-known books: U56/EWall, U56/CAND10, U56/CAND20
   (idea 2's candidate) and all four STK20 books (idea 10's PARK, and idea 71 says that panel is selection).
   No new KEEP-candidate; no rule change proposed.
8. **Survivorship** is one-directional on all three lists and falls hardest on STK20/BSTK100/SMALL484 — the
   high-dispersion panels — so the run is biased *toward* finding that dispersion pays, and it still does not.
9. **Exact RULES wording recommended: none.** Do not add a dispersion clause. If a universe clause is ever
   wanted, the supported wording is about return level and candidate count, not spread: *"The ranked book may
   be run on any panel of at least 20 eligible names; a panel is disqualified by its own realised CAGR
   against the 4b floor, not by its cross-sectional dispersion."*
10. Follow-ups queued: 77 (what *does* predict a panel — decompose the +0.710 IS→OOS Sharpe rank correlation),
    78 (candidate-count vs dispersion, disentangled by subsampling one panel to fixed n_elig).
