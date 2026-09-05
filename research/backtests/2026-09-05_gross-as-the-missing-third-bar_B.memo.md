# Memo — idea 131: do not restate 4b's adequacy bar as a gross level

**Verdict: KILL of the swap.** Not a KEEP-candidate; no rules change is requested.

1. Idea 129 closed with "the floor's real content is a gross-level filter". Tested directly, it
   is **false**: on the 306-row corpus Spearman(mean gross, CAGR) is only **+0.245**, against
   **+0.691** on the static-gross ladder where the two are one dial by construction.
2. **No γ does both jobs.** All 27 floor-only victims (11 Pareto-best) need γ ≤ 0.51, where the
   bar admits **23** ladder points; emptying the ladder needs γ ≥ 0.68, where it admits **0 of
   the 11**. 0 of 34 fine-grid γ achieve both.
3. The axis is **perverse in the overlap**: γ 0.53 → 0.54 discards **6 Pareto-best books and 0
   ladder points**. A 52.5%-gross lever outranks a 53.3%-gross gated book.
4. At the QUEUE's own γ = 0.50 the bar is **vacuous on real books** — it admits exactly the 56
   rows the core four bars admit, i.e. it is "delete the floor" wearing a bar's name.
5. **The one usable positive:** γ ∈ [0.57, 0.61] **weakly dominates φ = 0.70 on the floor's own
   three criteria** — loses none of its 29 admissions, saves 6–8 victims, admits 5–9 ladder
   points against 10. Gross is a better one-number adequacy bar than CAGR; it is not a good one.
6. **Rule 8:** paired on the cells it enters, S3 = S1 = S2 = S0 = **1.022 OOS Sharpe / −21.1% /
   12.7%** at every γ ≤ 0.65, with **0 of 7 picks moved**. A third bar, equally inert in
   selection — idea 132's result on new ground.

**Proposed PROTOCOL clause (negative, for the Sunday review — reporting only, no bar changes):**

> 4b's return-adequacy bar may not be restated as a minimum mean gross. On the project's arm
> corpus the two are weakly related (ρ = +0.25) and the families they must separate — defensive
> gated books and static-gross ladder points — overlap in mean gross, so no threshold both
> admits the former and excludes the latter. Where a run reports a gross bar, it must also
> report how many ladder points that bar admits.

**Lead for the queue, found after the question was answered and therefore NOT adopted here:**
the ladder holds gross constant by construction while a de-grossing gate makes it time-varying.
On cv(gross) the families nearly separate — victims mean **0.268**, ladder mean **0.014**, and
**25 of 27 victims including all 11 Pareto-best sit above every ladder point**. The two
exceptions are `rw` full-gross rebuilds, which never de-gross. Adopting this in the same run
would be the tuning rule 7 forbids; it is queued for pre-registration instead.

**Constructive direction (not adopted here):** the ladder is excluded correctly by a
*construction* rule, not a metric — a static rescaling of an existing book is the same book, and
should never enter a corpus as a separate candidate. That removes the ladder's claim on the
adequacy bar entirely and leaves idea 129's `4b-defensive` reporting class as the live proposal
for the 27 rows.

**No RULES wording is proposed.** The exercise adjudicated a bar and rejected it; RULES.md,
scan.py, bot.py and baseline.py are untouched.
