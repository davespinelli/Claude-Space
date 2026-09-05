# Memo — idea 123, a report-only PROTOCOL clause (lane C, 2026-09-05)

**Not a RULES change.** RULES.md, scan.py, bot.py and baseline.py are untouched; this is a
proposal for the Sunday review to add ONE reporting clause to PROTOCOL.md. Evidence:
`2026-09-05_relative-priceability-floor_C.result.md`.

**Proposed PROTOCOL clause (exact wording):**

> **N. Priceability of a drawdown price.** (numbering for the Sunday review: idea 121 has
> also proposed a clause 10, the $1M ADV floor) Any quoted rate of the form
> `(CAGR_ctl − CAGR_arm) / (|MaxDD_ctl| − |MaxDD_arm|)` must be reported next to its
> denominator expressed as a percentage of the control's own `|MaxDD|` in the same window.
> A rate whose denominator is below **10% of the control's `|MaxDD|`** is marked
> **not interpretable** and may not be cited as a price, an ordering, or a tier. This floor
> is REPORT-ONLY: it must not be used to select instruments or parameters (rule 8), and it
> does not license calling a deep negative price an artefact.

**Why 10%:** on idea 94/97's 202 published full-window prices, the 149 rows clearing the bar
keep their price sign from 2009–2016 to 2017–2026 in **88.4%** of cases (median |Δrate| 0.891);
the 53 rows below it agree **49.1%** of the time (median |Δrate| 2.701) — a coin flip. The
number is idea 119's own materiality bar, adopted unchanged, and the census is flat over
φ ∈ {0.02, 0.05, 0.10, 0.20} (8.9% / 15.3% / 26.2% / 50.5% of prices removed).

**Why report-only:** as a walk-forward selector the floor loses **0.019 of mean OOS Sharpe**
(0.710 vs 0.729 over 18 cells) and raises mean regret 0.441 → 0.602; at φ = 0.20 four cells
have no eligible arm. Same conclusion as idea 122's sign test, by an independent screen.

**What it costs the existing record:** 26.2% of published prices (V1u 42.7%, TOP20 30.1%,
EWall 18.2%; the stop tier loses 21 of 23 rows), and idea 97's tier sentence weakens rather
than firms up (C1 33/54 → 24/54 clause-rows true, C3 true only because the stop becomes
unmeasurable). Any future memo quoting a tier ordering must quote it under this clause.
