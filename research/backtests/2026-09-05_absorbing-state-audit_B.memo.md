# Memo — idea 93, absorbing-state audit (lane B, 2026-09-05). NOT a KEEP; a negative design clause.

This is not a KEEP-candidate memo: nothing in this run passes both KEEP paths (0 of 1824 arms) and
no book is proposed. It is filed because idea 93 asked for a *general fix* and the honest answer is
a prohibition plus a test, not a replacement instrument. Proposed for the Sunday review as a
PROTOCOL clause, not a RULES change.

**Proposed PROTOCOL clause (exact wording).** *"10. **High-water-mark re-entry is prohibited.** No
exposure rule may condition RE-ENTRY on a state variable regaining a running maximum — the book's
equity high, a name's pre-stop peak, or any other. Such a rule is near-absorbing (release rate 0.86–0.95,
mean block 251–285 trading days) and, where the rule's own action freezes that variable — a full cut
to cash, k=0 — it is exactly absorbing: 140 of 140 armed arms in idea 93 never released, mean capture
724 rebalances. Release must be conditioned on a bounded, action-independent event: a calendar
timeout, or an exogenous series such as SPY's own 200d. Every state-dependent arm must report
armings, releases, escape rate and terminal state beside its Sharpe."*

**Second clause (the correction the fix does NOT earn).** *"Removing absorption is a correctness fix,
not an improvement, and may not be quoted as one. In idea 93 the exogenous release is Sharpe-identical
to the pathology it cures (mean ΔSharpe -0.2633 vs -0.2636 over 288 arms each), makes MaxDD deeper in
140 of 288 arms (mean gain -0.0325), raises turnover from 9.3× to 19.8× a year, and is dominated by
the static-gross lever in 67% of arms on idea 74's axis (0.683 vs 0.537 pp CAGR per pp MaxDD)."*

**The audit test, one line.** For a proposed rule, write down the variable its release condition
reads and ask two questions: *(i) is the condition a running maximum?* → near-absorbing; *(ii) does
the rule's own action stop that variable moving?* → exactly absorbing. Endogeneity is **not** the
test: idea 93 falsified that reading — `nhigh` (release on the NAME's own price, which keeps trading
whether or not we hold it) is the second most absorbing rule the project owns, at release rate 0.951
and 8.4 names permanently out, while the endogenous-but-not-HWM `free` releases at 0.999.

**Standing rules affected.** RULES v1 as live contains no state-dependent exposure rule, so nothing
in the live book is exposed. Idea 40's book-level DD control and idea 22's `high`/`recover` resets
are both prohibited by clause 10 as worded. Idea 9's per-name trailing stop is prohibited only if
its re-entry is a high-water mark; its published numbers should be re-read against §4 of the result
before being quoted as a stop's numbers rather than a partial-cash book's. Idea 75's conditional
arming is not prohibited — arming is not release — and it is mildly positive here (+0.0328 mean
Sharpe over 192 paired arms, positive in 133), but the gain is concentrated on the absorbing arms
(`bookhigh` +0.073, `nhigh` +0.045) and near zero on the non-absorbing ones (`free`/`spy200` +0.007
each), i.e. it helps by firing the broken rule less often, not by timing anything. It does not make
the stop worth owning: the STOP family is still Sharpe-negative against its own control in 277 of 384.

Costs 10 bps, next-day execution, both KEEP paths evaluated, rule-8 walk-forward run (78 selections,
mean OOS Sharpe vs control -0.171 among the 65 material moves). SURVIVORSHIP: current-constituent
panels; all claims are within-cell deltas on shared days.
