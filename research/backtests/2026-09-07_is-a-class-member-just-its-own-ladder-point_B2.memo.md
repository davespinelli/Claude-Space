# Memo — idea 135 (lane B, 2026-09-07): the ladder control, and the one 4a candidate it left standing

## 1. PROTOCOL amendment proposed (the queue's own proposal, priced and then narrowed)

The queue proposed: *"a `4b-defensive` row must beat its OWN book's static-gross ladder point at
matched mean gross to be recorded at all."* Priced on all 531 members of idea 133's u56/broad
corpus, the bar **removes 466 of them (87.8%)**. It is therefore a real bar and not a formality —
but it must be written with two qualifications the run found, or it is not well posed:

> **PROTOCOL 4c (proposed, for the Sunday review — not applied here).** A row may be recorded as
> `4b-defensive` only if it beats its own book's ungated static-gross ladder point, solved to the
> row's own achieved mean gross on the same panel, cost rung and window, by **more than 1e-9** of
> Sharpe at no worse MaxDD. **The matching convention must be stated with the claim**: at matched
> mean gross 12.2% of the existing class survives, at matched *drawdown* (idea 94's convention)
> 58.9% does. The tolerance is not pedantry: with a bare `>`, the ungated control beats **itself**
> by 2.2e-16 and 17 of 206 admissions in this run are that artefact.

## 2. The 4a by-product (a KEEP-candidate for the Sunday review, with its weakness stated first)

**Its weakness:** the same book with **no instrument at all** (`SLV50 / control`, de-grossed to
0.53) also clears 4a. So the adoptable content is the *sleeve plus de-gross*, not the overlay, and
the row below is quoted only because it is the best of the 23. It is a `broad`-panel book
(survivorship: current constituents, idea 54) and it **fails 4b's CAGR floor by 3.1 pp**.

| Book (broad, 10 bps, weekly, t+1) | CAGR | Sharpe | MaxDD | H1 / H2 | OOS 2017– |
|---|---|---|---|---|---|
| `SLV50 + vol60-dg`, native gross 0.735 | 7.6% | **1.277** | **−10.6%** | 1.262 / 1.293 | **1.338** |
| RULES v2 re-run on broad | 8.0% | 1.106 | −12.24% | — | 1.119 |
| RULES v2 as live on u56 (RULES.md) | 8.66% | 1.206 | −12.05% | 1.226 / 1.191 | 1.285 |
| SPY | 15.2% | 0.889 | −33.7% | 0.957 / 0.834 | 0.882 |

Rule 8: choosing by IS Sharpe among IS-4a passers gives a pick in 3 of 12 cells (all `broad` @10
bps) and **beats RULES v2 and SPY out-of-sample in 3 of 3** (mean OOS Sharpe 1.282 vs 1.119/0.882).

**Exact RULES wording, if the Sunday review adopts it** (v3 clause 4, replacing clause 4 only):

> 4. **Sizing.** Hold two legs. *Equity leg (50% of gross):* every IN name at `0.375 / N` of NAV,
>    N = instruments in `research/universe_broad.json` priced that day; a name whose 20-day
>    realised vol exceeds 60% annualised is OUT and its weight stays in **cash** (de-gross; never
>    re-spread). *Macro sleeve (50% of gross):* TLT, GLD, DBC, UUP, weighted by a three-signal
>    momentum vote (12m ex-1m, 6m, 3m, each scored +1 if positive) times inverse 60-day realised
>    volatility, normalised to 0.375 of NAV; the sleeve is **not gated** (idea 18 variant B, as
>    implemented in `2026-09-05_which-asset-carries-S4_C.py: sleeve_weights`).
>    Rebalance both legs on the weekly schedule of clause 5.

**Blockers, all pre-existing:** ideas 105/106 (sleeve RULES wording), idea 134 (`broad` admits
nothing at 25 bps), and the fact that RULES trades `universe.json`, not `universe_broad.json`.
