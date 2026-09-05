# idea 119 — `V1u-small-negative-price` (cloud, 2026-09-05) — **KILL the citation as worded**

> **Note on duplication.** Lane B ran this same queue idea in parallel and pushed first (`2026-09-05_v1u-small-negative-price_B.result.md`). This script was written and run without sight of that one. The two agree to the decimal on every shared number — the premise count, the rule-8 pick and its OOS row, the concentration direction and the zero KEEP passes — and reach the same verdict by different attacks, which is the strongest form of confirmation this project has. What is additive here is flagged in sections 2, 3 and 4 and in the review note; the vol-scaler attribution and the investability bound are lane B's and are not re-derived here.

**What was on trial.** A *number*, not a book: idea 97's price list reports, in the cell
`panel=small, book=V1u`, gate arms whose price (pp of CAGR surrendered per pp of MaxDD bought) is
**negative** — the gate adds CAGR and cuts drawdown, +0.02..+0.10 Sharpe. The queue asked for an
audit before anyone cites it. Four attacks were pre-registered; the number fails two of them
outright, and what survives is not the claim that was made.

**Reproduction (S0): EXACT.** All 32 committed `small/V1u` pricelist rows re-derived through idea
94's own simulator and idea 97's own panel loader; max |diff| `1.8e-15`. The cached-signal path used
in the bootstrap reproduces `H.targets()` to `<1e-12` over all 11 arms.

Panel: `prices_small.csv.gz`, SPY held out, the 44 names with `max_1d_move >= 1.0` dropped → **439
names**, trading-day indexed, eval from 2011-01-13, IS ..2016-12-31. Two tuned parameters: the gate
instrument family and the position count `n`.

## (1) The queue's own wording does not survive (S1)

| rung | priceable gate arms (dMaxDD > 0.10 pp) | of those, negative |
|---|---|---|
| 10 bps | 6 of 10 | **5** (−1.414 .. −0.339) |
| 25 bps | 7 of 10 | **6** (−1.488 .. −0.391) |

`band3-dg` prices **positive** at both rungs (+0.604, +0.299), and both `vol60` arms buy *exactly
zero* drawdown on this book. Pooled: **11 negative of 13 priceable of 20 gate rows** — not "6/6",
and not "every gate". The −0.34..−1.41 range quoted in the queue is right for the arms it covers.

## (2) The decisive objection: every negative price is a ratio of noise (S2)

The control book's own drawdown is **−34.02 pp**. The drawdown each negative-priced arm actually
buys is:

| arm (10 bps) | dCAGR (pp) | dMaxDD (pp) | as % of control MaxDD | price |
|---|---|---|---|---|
| g200-dg | −0.19 | 0.57 | 1.7% | −0.339 |
| g200-rw | −1.68 | 1.19 | 3.5% | −1.414 |
| abs12-rw | −1.31 | 3.28 | 9.7% | −0.399 |
| v1gate-dg | −0.30 | 0.57 | 1.7% | −0.537 |
| v1gate-rw | −1.10 | 1.19 | 3.5% | −0.927 |

Pre-registered materiality bar (dMaxDD ≥ 10% of the control's |MaxDD| = 3.40 pp): **0 of 11 negative
rows are material.** Raising idea 94's 0.10 pp priceability floor to 3 pp leaves **one** gate row in
the whole cell. The headline "−1.41" is 1.19 pp of drawdown on a book that draws down 34 pp — the
denominator, not the instrument, is doing the work.

## (3) What the bootstrap says: the CAGR gain is real for one convention only (S3)

100 seeded draws dropping 10% of names, and 100 dropping 25%; control and each arm rebuilt inside
each subsample. Pre-registered: ARTEFACT iff the free-lunch sign fails to hold in ≥90% of draws OR
the price IQR spans zero.

| arm | free-lunch sign, drop 10% | drop 25% | verdict |
|---|---|---|---|
| g200-**rw** | 100% | 93% | **survives (both)** |
| abs12-**rw** | 99% | 93% | **survives (both)** |
| v1gate-**rw** | 93% | 77% | survives at 10%, artefact at 25% |
| g200-**dg** | 82% | 69% | artefact |
| v1gate-**dg** | 78% | 55% | artefact |
| abs12-**dg** | 64% | 52% | artefact |

**ARTEFACT in 7 of 12 audits.** The split is not random: every surviving arm is a `-rw` arm, and
`-rw` is by idea 94's own definition **not insurance at all** — it rebuilds the book at full gross
among the gated-in names, i.e. it is a **selection change**. The `-dg` (de-gross) arms, which are the
honest insurance form, are exactly the ones whose sign does not survive resampling the panel.

## (4) It is not one year, and it is not costs (S4, S6)

Deleting any single calendar year leaves the CAGR gain intact in **0 of 96** arm-year combinations
(no sign flips). 2020 is the largest single year (`abs12-rw` +10.9 pp, `g200-rw` +10.3 pp of that
year's return) and deleting it still leaves dCAGR negative. Costs are not the mechanism either: the
gain is already there at **0 bps** (`g200-rw` −1.76 pp, `abs12-rw` −1.34 pp) and *shrinks* as costs
rise, and every gated arm turns over 32.8–33.5×/yr against the control's 33.3× — the gate saves no
trading at all.

## (5) It is largely a top-5 concentration property (S5)

Negative-priced arms by position count: **n=5 → 5 of 6 priceable; n=10 → 4/8; n=20 → 4/9; n=40 →
2/9.** For the de-gross arms the CAGR sign flips to the normal one (the gate costs CAGR) by n=20
(`g200-dg` −0.02 pp at n=5 → +0.40 at n=20 → +0.64 at n=40), and dMaxDD rises from 0.57 pp at n=5 to
7.69 pp at n=40 — only at larger n does a gate buy *material* drawdown on this panel, and there it
is paid for in the ordinary way. The free lunch lives where the book holds 5 of 439 names.

## (6) Walk-forward, and the fact that settles the practical question (S7)

Idea 94's selector S1 on the IS window picks `g200-rw` at both rungs; OOS price −1.501 / −1.589 with
**regret 0.000** (it does land on the OOS-cheapest arm — of a ratio that section 2 shows is
uninterpretable). The *book* it picks: **8.7% / 0.634 / −32.8%** full sample, halves 0.689 / 0.587,
**OOS 8.9% / 0.631 / −32.8%**, against RULES v1 on the same panel 7.9% / 0.581 / −32.8% and **SPY
15.5% / 0.882 / −33.7%** (full-sample SPY 14.1% / 0.862 / −33.7%).

**0 of 14 audited books pass 4a; 0 of 14 pass 4b**, at either cost rung. Nothing in this cell is
capital-worthy however the price is read.

## Survivorship, stated because it runs against the artefact hypothesis

The panel is current constituents of a sub-$2B screen, so names that fell and delisted are absent.
That bias flatters the **ungated** book — it holds beaten-down names that all, in fact, survived —
and therefore makes a gate that excludes them look *worse* here than on a delisting-aware panel. So
survivorship cannot be the explanation for a gate looking good, and the artefact case has to rest on
the denominator, the concentration and the resampling instability measured above — which it does.
Absolute CAGR/Sharpe levels on this panel remain unquotable (idea 54 open).

## For the Sunday review

1. **Do not cite `small/V1u` as evidence that gates are free insurance on small caps.** The
   supportable sentence is: *"On the 439-name sub-$2B panel, a 5-name book's gate arms show a small
   CAGR gain (~1–2 pp/yr, present at 0 bps) that is a selection effect of the reweight convention,
   buys under 10% of the book's own drawdown in every case, weakens monotonically as the book widens
   past 5 names, and produces books that fail both KEEP paths."*
2. **PROTOCOL/price-list proposal (does not touch RULES):** replace idea 94's absolute priceability
   floor (`dMaxDD > 0.10 pp`) with a **relative** one — an instrument is priceable only when it buys
   at least **10% of the control book's own |MaxDD|**. Under the absolute floor this cell publishes
   11 negative prices; under the relative floor it publishes none, which is the correct answer.
   Every price already published elsewhere should be re-tabulated under the relative floor before it
   is quoted (queued as idea 120).
3. Idea 117 (crisis-depth as the price denominator) and this run are the same finding from two
   directions: **a price is not interpretable without the depth of the drawdown it is divided by.**
