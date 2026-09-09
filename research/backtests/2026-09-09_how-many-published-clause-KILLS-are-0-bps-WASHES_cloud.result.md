# Idea 505 — how many published clause KILLs are 0-bps washes like idea 275? (cloud, 2026-09-09)

**ANSWERED / PREMISE LARGELY REFUTED. 12 of 109 (11.0%).** Idea 275's daily-exit clause is the
exception in the record, not the type. Re-running the record's own clause corpus (idea 94's
price-list harness: 25 arms across the gate / stop / dd / bud families x 3 base books x U56+B136,
each arm against its own no-clause control on the same days) at 0 / 10 / 25 bps gives 109 arms
that lose at 10 bps. Of those, **86 (79%) already lose gross of costs** (SIGNAL, median dSharpe at
0 bps -0.046), 11 are marginal, and only **12 are cost verdicts** — 7 gross-neutral washes (|d0| <=
0.005) and 5 that are gross-POSITIVE and still killed by their own bill.

**The cost-verdict shape is a property of the BOOK, not of the clause family.** 11 of the 12 sit on
EWall, whose base turnover is 0.83–0.87x/yr; 1 on TOP20 (9.1x); **0 on V1u (23–29x)**. Per family
the COST share of losers is gate 17.9%, stop 18.2%, dd 2.9%, bud 0.0% — but those shares are just
the family's exposure to the wide book. This is idea 275's own mechanism read forwards: a clause
can only be killed by its bill on a book that does not already churn, and the record's clause
corpus is dominated by books that do.

**Idea 275's ordering statistic replicates where the mechanism applies.** corr(dSharpe, dTurnover)
goes 0 bps -> 10 bps: **stop -0.179 -> -0.813** (275 measured -0.14 -> -0.75 on the daily-exit
family, which is a stop in all but name) and **gate +0.171 -> -0.395**. It does NOT appear on dd
(+0.514 -> +0.468) or bud (+0.954 -> +0.926), where the clause's dominant effect is de-grossing,
so both deltas are dominated by lost return and the rung barely moves them.

**Out-of-corpus replication (SMALL439, 439 names after dropping the 44 with max_1d_move >= 1.0):
0 cost verdicts of 57 losers.** Its EWall base turnover is double U56's (1.74x/yr) and its signal
effects are larger, so every loser is a signal loser.

**Rule 8 (arm chosen on IS 2009-2016 Sharpe at 10 bps, 2017-2026 read once): the class label does
not walk forward — IS class == OOS class in 2 of 9 cells (22%).** Every IS argmax is a non-KILL by
construction; 7 of 9 turn into OOS SIGNAL losses (e.g. U56/TOP20 dd12-recover OOS d10 -0.2204;
B136/TOP20 ebud0.05 IS d10 +0.1809 -> OOS -0.1086). "This KILL was only a cost verdict" is
therefore not a re-openable finding: it is not stable enough to bet on.

**KEEP paths (U56, 10 bps): 4a 0 of 76 arms; 4b 17 of 76**, all of them top-20-plus-a-gate or
EWall-plus-a-gate books already in the record (the 2026-09-04 KEEP 4b family). The TOP20 control
itself fails 4b on drawdown (-22.21% vs the -20.23% floor) and its gated variants pass, which is
the same finding, not a new candidate. **No new KEEP candidate; nothing here changes RULES.**

**PROTOCOL implication (proposed, not adopted):** a clause KILL should be published with its
0-bps delta AND its base book's turnover beside it. 11% of KILLs would read differently at
0 bps, and which 11% is predictable from one number that is already computed.

SURVIVORSHIP: universe.json / universe_broad.json are current-constituent lists; SMALL439 is a
current screen. All levels are optimistic; every number quoted above is an arm-minus-own-control
delta on matched days, which is far less exposed.

Files: `..._cloud.py`, `.console.txt`, `.grid.csv` (675 rows), `.census.csv` (225 arms),
`.walkforward.csv` (9 cells).
