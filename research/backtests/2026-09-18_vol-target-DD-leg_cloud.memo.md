# PARK memo — portfolio vol targeting on the M12_1 book (idea 1263, lane cloud, 2026-09-18)

**Status: PARK, and this memo recommends AGAINST enactment.** One cell of 126 buys the binding 4b
drawdown leg by TIMING rather than by EXPOSURE and dominates the standing 2026-09-04 book on three
of four legs, but rule 8 does not reach it and its OOS Sharpe is BELOW the incumbent's. It is filed
so a Sunday review can see it, not because the record should take it.

**The cell.** U56, signal M12_1 (21/252 momentum alone), TARGET 0.15 annualised, VOL_LOOK 21 days.
Full 18.42% / 1.2368 / -18.50%; halves 1.4299 / 1.0640; IS 1.3248; **OOS 17.76% / 1.1700 / -18.50%**;
turnover 4.34/yr; mean gross 0.8745, min 0.2085, cap (1.00) binding on 52.3% of weeks. SPY: full
15.13% / 0.8849 / -33.72%, OOS 0.8747. Committed incumbent: 15.78% / 1.1522 / -19.13%, OOS 1.1832.

**Exact RULES wording, if it were ever enacted.** *"Each week, after selecting the book, compute the
trailing 21-day realised annualised volatility of the book's own daily return path as of the
decision close, v. Hold the book at gross = min(1.00, 0.75 x 0.15 / v) of NAV, the remainder in
cash. No leverage; no floor."*

**Why it is a PARK and not a KEEP.** (i) Rule 8 — TARGET and VOL_LOOK chosen on warm-up..2016-12-31
by IS Sharpe — picks TARGET 0.20 / LOOK 21, not this cell, and that pick FAILS 4b; chooser-minus-
do-nothing is +0.0021 on this arm and **-0.0590 across the six (panel, signal) arms**. (ii) Its OOS
Sharpe 1.1700 is below the incumbent's 1.1832 and far below the live RULES v2 book's 1.2781.
(iii) 4a fails (H2, DD) as it does at 126 of 126 cells. (iv) It costs +1.59/yr of turnover over the
incumbent, and 10 bps is this record's assumption, not a measurement.

**What is real in it.** Against a constant-gross control held at this cell's OWN mean gross of
0.8745 — the control that separates timing from simply running more exposure — the mechanism buys
**+5.17pp of MaxDD (-23.66% -> -18.50%) and +0.0424 of full Sharpe for -1.21pp of CAGR and
+1.42/yr of turnover**, and that control FAILS 4b where this cell passes. 7 of the run's 14 4b
conversions survive their gross-matched control this way; the other 7 are exposure alone.

**Survivorship (rule 9).** U56 is a current-constituent list, so the anchor's drawdown is flattered
and this mechanism's DD gain is a LOWER bound while the CAGR it gives up is measured against a
flattered comparand. Every level here is optimistic; the contrast against the gross-matched control
is first-order immune to that, the 4b legs are not.
