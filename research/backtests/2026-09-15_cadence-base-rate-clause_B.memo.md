# Memo — the base-rate clause is needed again for SLOW books (idea 926, lane B)

1. **Not a KEEP.** No book is proposed for capital: 4a **0 of 125** IS-only picks, monthly OOS
   4b **1 of 35**, and that passer is the live band book at gross 1.00, already in the record.
2. **What changed.** Idea 680 retired the base-rate clause because 10 bps emptied the null
   (4 of 4 weekly passes outside it). On monthly books at the same 10 bps that reads **1 of 3**.
3. **The statistic.** Spearman ρ(4b pass, null base rate), n = 30 cells: weekly **−0.0728** at
   10 bps, monthly **+0.4470**, and monthly **+0.4597** at 25 bps. The inversion is alive.
4. **The mechanism** is annual cost drag, not the rung: ρ(base rate, cost × turnover) −0.5012
   vs ρ(base rate, cost) −0.4103 on the 152 cells where the statistic can move. No cell above
   a 5% base rate survives **100 bp/yr** of drag; 10 bps buys 161 bp/yr weekly and 73 monthly.
5. **The binding case.** U56 `CORE/TOP20` at 10 bps, weekly → monthly: 12.60% / 1.088 / −18.31%
   → **14.69% / 1.203 / −19.51%**, null base rate **0.0% → 38.4%**. The gain is inside the null.
6. **PROTOCOL line proposed for the Sunday review, NOT applied (rule 6)** — an amendment to the
   reporting line idea 680 proposed, replacing its cost-rung wording with a drag wording:
   > *"A 4b pass whose book pays less than 100 bp/yr of annual cost drag (cost rung × realised
   > turnover) is reported with its own gross-matched null's 4b base rate beside it. Below that
   > line a pass is not, by itself, evidence about the rule."*
7. **Do not use it to choose.** CH_BASE differs from CH_SHARPE in 6 of 48 cells and is worse
   where it differs: OOS 4b 5 vs 6, mean OOS CAGR 12.90% vs 12.94%. Reporting, not selection.
8. **No RULES change.** `RULES.md`, `PROTOCOL.md`, `scan.py`, `bot.py`, `baseline.py` untouched;
   this memo is an input to the Sunday review, nothing more.
9. **Survivorship.** Current-constituent panels, so every base rate here is an UPPER bound —
   which weakens, not strengthens, the 38.4%; the cadence and drag contrasts are same-tape.
10. **Verification.** Gates 9 of 10 (G3 FAIL as written on a 2.220e-16 book-Sharpe round-trip
    delta; its base-rate leg is 0.000e+00 exact on 90 of 90 cells), grid run twice end to end
    with a byte-identical ρ table, and **independently replicated the same hour** by the cloud
    lane on a narrower grid (monthly ρ +0.4131 / +0.4349 / +0.4245 at 0/10/25 bps; U56
    `CORE/TOP20` monthly base rate 40.8% at 250 draws vs 38.4% at 500). That lane proposes the
    same line worded on **turnover < ~10x/yr**; reconcile the two wordings at the review — drag
    is the axis the data supports (ρ −0.5012 vs turnover alone −0.1182).
