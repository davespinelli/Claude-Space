# MEMO — the zero-cost base-rate clause (idea 680, lane B, 2026-09-15)

1. **Proposing NO RULES change and NO promotion.** RULES v2 stays live; `RULES.md`,
   `PROTOCOL.md`, `scan.py`, `bot.py`, `baseline.py` untouched (rule 6). This memo exists to
   record one PROTOCOL reporting line for the Sunday review and the evidence that kills the
   stronger version of it.
2. **The finding.** At 0 bps only **1 of 7** committed-key 4b passes sits outside its own
   gross-matched coin-flip null (survivors' base rates 0.2%, 9.3%, 53.4%, 74.8%, 81.4%, 98.0%,
   100.0%). At 10 bps **4 of 4** sit outside; at 25 bps **2 of 2**.
3. **The mechanism.** At 0 bps passing 4b *predicts a higher* base rate — Spearman **+0.6387**
   over 30 cells, mean 0.5959 (passers) vs 0.0733 (failers). At 10 bps the sign flips to
   **−0.1048** and every base rate collapses (mean 0.1953 → 0.0004, max 1.000 → 0.010, cells
   above 0.05: 12 → 0).
4. **So the clause is KILL as a new bar.** PROTOCOL rule 2's own 10 bps rung already empties
   the null. A base-rate clause added on top changes no verdict PROTOCOL reaches.
5. **And it is harmful as a rule-8 chooser.** CH_BASE picks identically to CH_SHARPE at 10 and
   25 bps on all three panels; at 0 bps it steers U56 from `EXT/BAND03` (OOS 12.95% / 1.301 /
   −15.88%, 4b PASS) to `CORE/BAND03` (OOS 9.66% / 1.302 / −12.03%, 4b fail) — **−3.29 pp of
   OOS CAGR for nothing**. Rule 8 totals: 4b 7 of 21 live picks, 4a **0 of 21**.
6. **The standing candidate is unaffected and reproduces.** `U56/TOP20` at 0.75 / weekly /
   10 bps: 12.60% / 1.088 / −18.31%, halves 1.09/1.09, 4b PASS, null base rate **0.0%**. Its
   zero-cost base rate of 74.8% independently reproduces idea 502's 78.1% on a different,
   exactly gross-matched null (G5 = 0.0000), so 502's number stands — its implication for the
   live book does not survive the cost rung.
7. **Caveat that must travel with any base-rate number.** The null's rotation convention moves
   it more than cost does: `U56/TOP20` at 0 bps reads **74.8% (RANDROT) vs 0.2% (RANDFIX)**.
   There is no such thing as *the* coin-flip base rate; a number is meaningless without its null.
8. **Proposed PROTOCOL line, for the Sunday review to accept or reject — exact wording:**
   *"10. **Zero-cost rows are not evidence.** A 4b pass quoted at any cost below PROTOCOL rule
   2's 10 bps must be published with its own gross-matched coin-flip base rate and the null's
   rotation convention named, or not published as a pass at all. At 10 bps and above no such
   clause applies."*
9. **Scope, stated plainly.** 30 (panel × claim set × book) cells were re-priced, not the
   record's 153,020 committed 4b PASS rows; 50.9% of those rows do not name their own book and
   4.3% already belong to null-construction books. The census is the denominator, not the claim.
10. **Survivorship.** Current-constituent panels, so every base rate above is an **upper** bound
    and every percentile a **lower** bound — the bias runs against the incumbents, not for them.
    Nothing here justifies real capital beyond the live paper record.
