# Memo — idea 63: 25% passive core sleeve (4b KEEP-candidate, 2026-09-04, cloud)

1. **Candidate:** idea 57's `ew-band3` book with **25% of gross held in a passive core** (SPY; QQQ scores higher but is a hindsight tilt on this sample).
2. **Numbers, 10 bps, weekly, t+1** — universe.json 12.4%/1.142/-16.2% (QQQ core) and 11.4%/1.106/-16.5% (SPY core); broad 12.3%/1.086/-18.5% and 11.3%/1.040/-17.7%; SPY 15.3%/0.890/-33.7%.
3. **Passes 4b on BOTH universes** (halves 1.183/1.113 and 1.203/0.986 with QQQ; 1.110/1.106 and 1.127/0.960 with SPY), and the QQQ version still passes both at 25 bps — the first arm in the project to survive 25 bps cross-universe.
4. **Why it works:** the diagnosis, not a search. The books' second-half shortfall is 75%-gross cash drag in a 15%/yr half (they beat SPY only in 2018 and 2022), not mega-cap concentration — the concentration factor explains R² 0.011-0.018 of H2 excess.
5. **Control:** a plain SPY or VTI core fixes the same bar (broad top20 H2 0.814 → 0.861 / 0.853), so the effect is beta, not the NASDAQ.
6. **Weakness (state it at review):** rule 8 picks b=0.50 on both universes, whose OOS clears on universe.json (15.4%/1.106/-18.8%) but **fails broad OOS drawdown** (-22.0% vs -20.2%). b=0.25 is selected by the sample-wide 4b test, not by the walk-forward.
7. **Survivorship:** current-constituent lists; absolute numbers optimistic, and the mega-caps the book is accused of missing are in the list because they won.
8. **RULES wording, exactly:** *"Hold 25% of gross exposure in SPY at all times. Allocate the remaining 50% of gross equally across every eligible name, where eligible means vol20 < 0.60 and the price has closed more than 3% above its 200-day moving average since it last closed more than 3% below it. Rebalance weekly, execute at the next close."*
9. **Do not adopt without:** the Sunday review agreeing that 75% gross was itself the error, and a decision on QQQ vs SPY as the core (QQQ = +1.0pp CAGR and the 25 bps pass; SPY = no hindsight).
10. **Supersedes nothing yet.** It is idea 57's candidate plus a beta sleeve; if the review rejects the sleeve, idea 57's arm stands unchanged.
