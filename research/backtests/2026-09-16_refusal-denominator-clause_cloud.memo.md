# Memo — proposed PROTOCOL rule 4 reporting clause (idea 995, cloud lane, 2026-09-16)

1. **Finding.** Idea 993's `ctrl_4b_in_emptied` read 0 on the M/Q half and 4 on the D/W half, and
   the record took that as a cadence asymmetry in the screen. Resolved to the four rungs it is a
   **denominator artefact**: the control holds 2 OOS 4b passes at D, 2 at W, **0 at M and 0 at Q**.
   The screen destroys 4 of 4 available on the fast half and 0 of 0 on the slow half.
2. **Second finding.** The free-refusal median is **undefined at D at every floor above 0.00** —
   the screen empties all 9 daily slots, so the incumbent convention has no rows to summarise, and
   a silent cell would be read as an absent effect rather than a total one.
3. **Proposed wording, PROTOCOL.md rule 4 (a REPORTING clause; it changes no KEEP bar):**
   *"Any published count of picks a screen, eligibility filter or decline rule REMOVES must be
   printed as a fraction of what was available to remove in the same cell — `removed / available`,
   never `removed` alone — and any cell whose surviving-pick statistic is undefined because every
   slot was refused must be printed as `undefined (n refused of n)`, never omitted."*
4. **Cells** are the (panel, cadence) pairs the claim is measured on; a claim pooled over cadences
   prints the per-cadence fractions beside the pooled one.
5. **Cost.** One extra integer and one extra string per published row. No re-run of any book.
6. **Reach.** It applies to every refusal/decline/eligibility claim in the record, 993's and 980's
   included; it would have made 993's 0-vs-4 self-refuting on the page it was published on.
7. **Status: PROPOSED, NOT APPLIED.** Rule 6 allows one rules change per week via Sunday review.
   `RULES.md`, `PROTOCOL.md`, `scan.py`, `bot.py` and `baseline.py` are untouched by this run.
8. **Not a capital claim.** This run buys no KEEP path: OOS 4a is **0 of 36**, and every OOS 4b
   passer is U56 `BAND03` @ gross 1.00 — the live book at full gross on its sixth arrival and
   sixth refusal (fails 4a everywhere).
9. **Evidence.** Gates 11 of 11, including exact cross-run reproduction of 993's 13,500-row ladder
   (7.11e-15), 993's committed MQ18/DW18 decline rows (0 / 0 / 5.0e-05) and 981's published
   `L4_DD` cadence gradient (3.33e-04). Script:
   `2026-09-16_is-REFUSAL-COST-a-CADENCE-object_cloud.py`.
10. **Survivorship (rule 9).** Current-constituent panels; SMALL drops `max_1d_move >= 1.0`. Every
    4b count above — control, screened and fallback alike — is an UPPER bound, so the *available*
    denominators this clause demands are themselves optimistic, which strengthens the case for
    printing them rather than weakening it.
