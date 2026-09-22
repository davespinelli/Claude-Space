# Caveat for the Sunday review — the standing 4b candidate's drawdown margin is not decidable (idea 1542, lane C, 2026-09-22)

1. Not a KEEP memo: this run produced **no new candidate** (4a 0 of 60 cells, 4b OOS 10 of 60, all of them plain gross rungs of the live band book). It files a caveat against the candidate the record already carries.
2. PROTOCOL 4b convicts on `margin = MaxDD(book) − 0.60 x MaxDD(SPY)`. This run bootstrapped **that same quantity** (paired circular block, B = 1,000, SPY resampled on the same index) at every grid point — `.dd_leg.csv`, 396 rows.
3. **Only 57.5% of the 120 (panel x window x L x device) cells @10 bps are decidable at |t| > 2**; 67.6% among the cells whose leg passes.
4. The **live book is safe**: u56 FULL margin **+8.18 pp, SE 2.56, t +3.19**; b136 **+7.99 pp, t +3.27**.
5. The **candidate is not**: u56 `GROSS_g1.00` (idea 2264's book, gross 1.00 instead of 0.75) OOS margin **+4.32 pp, SE 2.36, t +1.83 — PASS but UNDECIDABLE**. `GROSS_g1.25` reads **+0.54 pp, t +0.24**.
6. On b136 the same g = 1.00 leg **is** decidable (t +2.01), but that cell misses 4b OOS on the CAGR floor from 10 bps on — the two panels do not both give a decidable pass.
7. This is not resolvable by waiting: the MaxDD contrast SE is **1.35x larger on the full 17.7y window than on the 2.21x shorter 8y window** (MaxDD is a maximum; its dispersion grows with horizon).
8. Nor by changing statistic: of six drawdown-path statistics, **MaxDD is the best resolver** (R 0.405 vs Ulcer 0.343, MeanDD 0.355, CVaR 0.155, TUW 0.146, Calmar 0.058) and **none reaches R = 1** at any of 324 grid points.
9. **Recommended wording if the review wants a clause** (PROTOCOL change, Sunday only, not applied here): *"A 4b drawdown-cap pass shall be published with the SE of its own leg margin, from a paired circular-block bootstrap on the book and SPY together; a margin inside 2 SE is reported as UNDECIDABLE, not as a pass."*
10. **No RULES change is proposed.** The live book stays as it is; the gross-1.00 candidate should carry this caveat into any capital decision rather than be promoted on the drawdown leg.
