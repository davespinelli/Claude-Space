# Memo — idea 2435 (lane cloud, run 46, 2026-09-23): two candidates from the ETF-exclusion ladder

1. **What was measured.** The committed candidate family is priced on panels that are 36 of 56 (U56) and
   ~35 of 136 (B136) ETFs, so the book may hold SPY itself. Removing the index funds in a nested ladder
   (NOBROAD -> NOEQETF -> STOCKS) x gross, under two conventions (RESPREAD = re-spread over survivors, the
   tradable book and the pre-stated headline; DEGROSS = survivors keep committed sizing, the attribution),
   256 rows, 12 of 12 gates, NONE bit-identical to `engine.backtest`.
2. **Headline answer, opposite in sign to the idea's premise.** The ETF sleeve is a DRAG, not the carrier:
   **dSharpe > 0 in 192 of 192 exclusion cells and dOOS_Sharpe > 0 in 192 of 192.** The committed U56 book
   parks 41.2% of NAV in ETFs (SPY alone 1.42%); B136 18.4%.
3. **CANDIDATE A (path 4a, U56 only, RECORDED — NOT RECOMMENDED).** `CAP2` + `NOEQETF`, g = 0.75, RESPREAD:
   CAGR **9.24%**, Sharpe **1.5728**, MaxDD **-8.08%**, halves 1.6271 / 1.5606, OOS 10.62% / 1.6284 / -8.08%,
   turnover **2.44x/yr**. Against live RULES v2 (8.65% / 1.2052 / -12.05%) it is better on CAGR, Sharpe, both
   halves, MaxDD and turnover, and **4a holds at 0 / 10 / 25 / 50 bps (8 of 8 cells, 32 of 32 counting the
   STOCKS rung and both conventions)**. It fails 4b on `L_CAGR` alone, by 1.42 pp.
4. **CANDIDATE B (path 4b, both panels, RECORDED — NOT RECOMMENDED).** `CAND` + `NOEQETF`, g = 0.75, RESPREAD:
   U56 **15.52% / 1.4628 / -14.92%**, halves 1.5548 / 1.4104, OOS **16.99% / 1.4743 / -14.92%**; B136
   **12.65% / 1.1558 / -17.38%**, OOS 12.82% / 1.1488. Joint both-panel 4b at **0 / 10 / 25 bps**; B136 dies
   at 50 bps on `L_CAGR` by 0.11 pp. It dominates the committed NONE book on U56 on CAGR (+2.93 pp), Sharpe
   (+0.269), MaxDD (+2.47 pp) and OOS Sharpe (+0.235).
5. **Rule 8 endorses the direction, unanimously.** Both dials fitted on <= 2016-12-31 only, 2017-2026 read
   ONCE, 64 picks: **0 of 64 land on NONE**, 64 of 64 beat their own cell's NONE anchor OOS, 64 of 64 beat
   SPY OOS, 53 of 64 beat the live RULES v2 book, 26 of 64 carry a full-sample 4b pass.
6. **WHY NEITHER IS RECOMMENDED (rule 9, and it is decisive here).** The tranche being stripped away — index
   funds — is the ONE part of the panel that is not survivorship-selected. Excluding it mechanically raises
   the NAV share of a CURRENT-CONSTITUENT stock list held from 2008, which is exactly the direction the bias
   pushes. This run cannot separate the two with the committed caches. The STOCKS rung (U56 / CAND 21.90%
   CAGR from 20 current mega-caps) is the reductio: that number is survivorship, not selection.
7. **Second blocker, Candidate B only.** Turnover **4.18x/yr** (U56) against the incumbent's 3.51x and the
   live book's re-measured 2.79x — the family's one stated adoption blocker gets WORSE, not better.
   Candidate A moves it the right way (2.44x, and 1.83x at STOCKS) and is the more interesting of the two.
8. **Third caveat, Candidate A.** It runs a **59% SHY sleeve** (72% at STOCKS), so its return is materially a
   2009-2026 T-bill path plus a thin risk book; and B136 does not confirm it (4a 0 of 8 there).
9. **EXACT RULES WORDING, if a future Sunday review adopts Candidate A (path 4a) — replaces clause 1 only:**
   *"Clause 1 (eligible instruments). The tradable set is every instrument in `research/universe.json` EXCEPT
   the broad equity index funds SPY, QQQ, VTI, RSP, DIA, IWM, EFA, EEM and the sector funds XLK, XLF, XLV,
   XLE, XLI, XLY, XLP, XLU, XLB, XLRE, XLC, SMH, XBI, KRE, ITB, GDX. SHY remains eligible and continues to
   absorb the un-invested residual. SPY continues to be priced as the benchmark and is never held. Clauses 2
   to 4 (the 200d +/-3% band, gross 0.75 spread as `gross / N_in` over the eligible names inside the band
   with a 2% per-name cap, weekly rebalance, t+1 execution) are unchanged."*
10. **Recommended action: NONE this week.** File both candidates; adopt neither. The single test that would
    settle it is a point-in-time constituent panel, which this sandbox cannot build (no network). Until one
    exists, the defensible statement is the NEGATIVE one, which needs no panel to be true: **the committed
    book's ETF sleeve does not carry its 4b pass — it costs Sharpe in 192 of 192 cells.** No change to
    RULES.md, PROTOCOL.md, scan.py, bot.py or baseline.py was made by this run (rule 6).
