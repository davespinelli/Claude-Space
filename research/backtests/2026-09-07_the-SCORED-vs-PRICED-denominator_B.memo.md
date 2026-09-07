# Memo — idea 380's 4a by-product (SCORED band3 all-names at reduced gross). ADOPTION NOT RECOMMENDED.

1. **The object.** All-names equal weight under the SCORED denominator, inside the live 200d ±3% band, de-grossed to CASH, weekly.
2. **The 4a record.** 14 of 48 SCORED cells pass 4a on both panels at 0/10/25 bps; **0 of 48 PRICED cells pass**. Every passer is gross ≤ 0.75.
3. **Best cell (u56, gross 0.375, 10 bps):** CAGR 4.33%, Sharpe 1.2088, MaxDD −6.12%, halves 1.2296/1.1933, OOS Sharpe 1.2871 vs RULES v2 1.2056 (1.2259/1.1908), OOS 1.2851.
4. **Confirms on B136** (gross 0.375, 10 bps): Sharpe 1.1074, MaxDD −6.26%, halves 1.2307/0.9853 vs v2 1.1058 (1.2291/0.9844).
5. **Exact RULES wording if ever adopted:** *"Hold every name whose 12-1/6/3 composite is DEFINED and which sits inside the 200d ±3% band, at gross/N of NAV where N = the number of names with a defined composite that day; gated-out weight goes to CASH. gross = 0.375. Rebalance weekly."*
6. **Why NOT to adopt (1): the margin is the denominator, not an edge.** The 4a pass is carried by +0.0032 of Sharpe — the whole return-space value of the convention (§4 of the result) — and its sign flips to −0.0042 the moment the band gate is removed.
7. **Why NOT to adopt (2): it fails 4b badly.** CAGR 4.33% against SPY's 15.23%; PROTOCOL's floor is 0.70 × SPY = 10.66%. All 14 passers miss it by more than half.
8. **Why NOT to adopt (3): 4a is being gamed by the gross dial.** The cell is literally the live book at half gross — same Sharpe to three decimals, half the CAGR, half the drawdown. This is the exact failure PROTOCOL 4b was added on 2026-09-04 to correct.
9. **Rule 8 does not support it either:** the IS chooser splits SCORED 9 / PRICED 3 over 12 points, and the OOS cost of the wrong convention is median 0.0018 Sharpe (max 0.0094).
10. **Recommendation: no rules change.** Adopt PRICED as the record's named all-names denominator (92.9% of resolvable files, 396 of 444 attributable rows, and the live `rules_v2_weights` already use it), keep idea 382's floor amendment, and add a `denom` column. Survivorship note: B136 is `universe_broad.json` current constituents.
