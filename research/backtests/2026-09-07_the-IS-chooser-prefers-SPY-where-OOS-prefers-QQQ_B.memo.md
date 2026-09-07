# Memo — 4b cell surfaced by idea 371: RULES v2 at gross 1.00 (Sunday review, 2026-09-07, lane B)

1. **Cell.** `rules_v2_weights(px, band=0.03, gross=1.00)`, weekly, 10 bps, U56: CAGR **11.59%**, Sharpe **1.205**, MaxDD **−15.91%**, halves **1.227 / 1.190**, OOS (2017-26) CAGR 12.78% / Sharpe 1.284 / MaxDD −15.91%, turnover 2.35x/yr.
2. **4b bars cleared with slack** (SPY 15.23%/0.889/−33.72%, H1 0.957 H2 0.834 OOS 0.882): H1 +0.270, H2 +0.356, OOS +0.402, DD slack **4.32pp**, CAGR slack **0.93pp**. Clears at 0/10/**25** bps on U56; on B136 at 0/10 bps only (**fails CAGR at 25 bps**).
3. **4a: fails** (H2 and DD vs the live 0.75-gross book) — this is a path-4b item only.
4. **Rule 8 selects it** 6/6 panel×rung cells — but the whole G1 IS Sharpe spread is **0.001–0.005**, so the selection is a numerical tie, not a preference. Treat it as unselected.
5. **The only bar the gross dial moves is CAGR.** Sharpe is flat to ≤0.001 across gross 0.20→1.00; DD scales linearly (−3.3% → −15.9%). This is idea 351's numeraire result, upward.
6. **Not new.** Idea 66 (2026-09-04) already recorded `universe.json ew-band3 g=1.00` as a 4b KEEP (15.1%/1.14/−19.9%, 6.4x/yr). This cell is its RULES-v2 sibling: same band gate, **no `vol20 < 0.60` filter**, corrected tape, 2.35x/yr.
7. **Exact RULES wording if the review takes it** — clause 3 of RULES v2, replace verbatim: "Hold every instrument inside the 200d ±3% band at **1.00**/N of NAV, N = instruments priced that day; gated-out weight goes to CASH (de-gross, never re-spread)." No other clause changes; version bump RULES.md and `products/bot/bot.py` per PROTOCOL 6.
8. **What it actually buys.** +2.9pp CAGR and +3.9pp MaxDD against the live book; Sharpe unchanged (1.205 vs 1.206). It is a position-sizing decision, not an edge, and PROTOCOL 6 allows one change per week.
9. **Risks.** Current-constituent survivorship; the CAGR slack is 0.93pp on U56 and **0.13pp on B136**, so the 4b pass is cost- and panel-fragile at the top rung; no cash buffer remains for the band's re-entry turnover.
10. **Recommendation: do not promote on this run's evidence.** It arrived as a control arm of a chooser study, not as its question; ideas 311/351/372 all class an unlevered gross move as a dial placement. Un-park it with a dedicated gross-placement run that prices the DD against the numeraire clause.
