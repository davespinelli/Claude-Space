# RESULT — idea 899, does-crediting-IDLE-CASH-at-the-SHY-PATH-move-the-4b-verdict (cloud, 2026-09-15)

**ANSWERED: YES, MATERIALLY — the record's "one rung wide" robustness claim is a CASH-CONVENTION
artefact.** All three pre-declared hypotheses PASS. Under the standing ZERO-cash convention
exactly **one** gross rung (0.65) passes 4b on ≥ 20 of 21 monthly offsets; under a realistic cash
credit **three** do, and the passing band **moves down** the ladder. No new book is proposed and no
rules change is made — this is an accounting finding about books the record already owns. A
PROTOCOL clause is **PROPOSED and NOT APPLIED** (rule 6); RULES.md, PROTOCOL.md, scan.py, bot.py
and baseline.py untouched.

## Gates, printed before any hypothesis was read
| Gate | Result |
|---|---|
| G1 cash simulator at cash_ret = 0 vs `engine.backtest`, g ∈ {0.50, 0.65, 1.00} | **PASS**, max&#124;dr&#124; = max&#124;dturnover&#124; = **0.000e+00** |
| G2 (k=0, g=0.65, ZERO) vs idea 879's memo triple 12.69% / 1.201 / −17.11% | **PASS**, exact to the printed digits |
| G3 full-sample CAGR non-decreasing in the flat cash rate at all 11 gross rungs | **PASS** |

## What is actually being handed out
SHY's realised return over the priced sample: **1.318%/yr** full, **0.785%** H1, **1.854%** H2,
**1.737%** OOS 2017+. The book's own idle-cash share at g = 0.65 averages **0.377 of NAV**, so the
credit is worth roughly 50 bps/yr of book CAGR — which is the whole story below, because the leg
this book fails is a level bar, not a risk bar.

**SHY is not a bill path.** Effective duration ~1.9y, so it overstates a cash sleeve through
2009–2021 and understates it in 2022, and the book holds SHY itself on **10.2%** of days (credited
once as a holding and once as the numeraire). Every SHY number here is an **upper bound** on a
real cash credit over this sample. FLAT150 / FLAT300 are idea 406's own rungs and bracket it.

## H_MOVE — PASS. The convention moves published verdicts
Over the 11 gross rungs × 21 monthly offsets (231 cells, 10 bps), cells whose 4b verdict flips
against ZERO: **FLAT150 20 (8.7%), SHY 26 (11.3%), FLAT300 40 (17.3%)**. Bar was ≥ 5%.

## H_WIDEN — PASS. "One rung wide" is a convention, not a property of the book
4b passes out of 21 monthly offsets, by gross rung:

| gross | ZERO | FLAT150 | FLAT300 | SHY |
|---|---|---|---|---|
| 0.50 | 0 | 1 | **15** | 0 |
| 0.55 | 2 | **15** | **21** | **14** |
| 0.60 | 16 | **21** | **21** | **21** |
| 0.65 | **21** | **21** | **21** | **21** |
| 0.70 | 16 | 17 | 17 | **20** |
| 0.75 | 7 | 7 | 7 | 11 |
| 0.80–1.00 | 1–3 | 1–3 | 1–3 | 1–4 |

Rungs passing on ≥ 20 of 21 offsets: **ZERO 1, FLAT150 2, FLAT300 3, SHY 3.** The band widens and
**slides down**: paying the idle sleeve lets a *less* exposed book clear the CAGR floor, while the
DD cap — which is what closes the band from above — barely moves (it is an exposure bar, and the
credit adds return without adding exposure). Idea 879's knife-edge at g = 0.65 is therefore a
statement about the ZERO convention, not about the book.

## H_ORDER — PASS. It is a level shift, not a re-ranking
Spearman between the ZERO and SHY 4b CAGR margins over the 11 rungs at k = 0: **+1.0000**. The
credit does not reorder the ladder; it slides the whole margin vector up by ~0.5 pp and lets more
of it clear a fixed floor. That is why the effect is entirely predictable and entirely material.

## The ladder at k = 0, 10 bps (full sample 2009-01-13 → 2026-09-14)
Against SPY **15.13% / 0.885 / −33.72%** (4b bars: CAGR floor 10.59%, DD cap −20.23%; SPY is
**not** credited — it is fully invested, so the bars themselves do not move):

| cash | g = 0.60 | g = 0.65 | g = 0.75 |
|---|---|---|---|
| ZERO | 11.7% / 1.201 / −15.9% | 12.7% / 1.201 / −17.1% | 14.7% / 1.202 / −19.5% |
| SHY | 12.3% / 1.260 / −15.2% | 13.2% / 1.249 / −16.5% | 15.1% / 1.232 / −19.1% |
| FLAT300 | 13.1% / 1.332 / −15.8% | 13.9% / 1.309 / −17.0% | 15.6% / 1.272 / −19.5% |

And the live book, which de-grosses and therefore pays this tax too:

| RULES v2 (live) | full sample | OOS 2017+ |
|---|---|---|
| cash = ZERO | 8.62% / 1.201 / −12.05% | 9.46% / 1.277 / −12.05% |
| cash = SHY | 9.24% / 1.283 / −11.47% | 10.27% / 1.371 / −11.47% |
| cash = FLAT300 | 10.13% / 1.396 / −11.98% | **10.97%** / 1.465 / −11.98% |

RULES.md records v2 failing 4b **on the CAGR floor alone**. That failure narrows from −1.97 pp to
−1.35 pp (SHY) and −0.46 pp (FLAT300) full sample, and **reverses out of sample at FLAT300**
(10.97% against the 10.69% OOS floor). The live book still fails 4b full sample under every
convention tested — but the size of the miss the record quotes is convention-dependent, and the
record does not say so.

## PROTOCOL rule 8 — idea 879's own IS-only selector, run under each convention, OOS read once
Selector (declared before the run, imported from idea 879): the gross rung minimising |IS CAGR
margin over the 4b floor| on 2009-01-13 → 2016-12-31. OOS 2017-01-01 → 2026-09-14 read **once**.

| cash | IS pick | IS margin | OOS CAGR | OOS Sharpe | OOS MaxDD | OOS H1 / H2 | OOS 4b | OOS 4a |
|---|---|---|---|---|---|---|---|---|
| ZERO | g = 0.65 | +0.19 pp | 14.38% | 1.2814 | −17.11% | 1.4469 / 1.1039 | **PASS** | FAIL |
| FLAT150 | g = 0.60 | +0.05 pp | 13.96% | 1.3433 | −15.85% | 1.5049 / 1.1703 | **PASS** | FAIL |
| **SHY** | **g = 0.60** | −0.27 pp | **14.02%** | **1.3479** | **−15.24%** | 1.5234 / 1.1623 | **PASS** | FAIL |
| FLAT300 | g = 0.55 | +0.06 pp | 13.68% | 1.4309 | −14.56% | 1.5875 / 1.2634 | **PASS** | FAIL |

SPY OOS 15.27% / 0.874 / −33.72% (OOS 4b bars: CAGR floor 10.69%, DD cap −20.23%).

**The rule-8 content: the convention changes the PICK** — 0.65 under ZERO, 0.60 under SHY, 0.55
under FLAT300 — and every pick clears 4b out of sample. The credited picks give up ~0.4 pp of OOS
CAGR and buy **+0.067 OOS Sharpe and 1.9 pp of OOS drawdown**. A selector calibrated under a
convention the book will not actually trade under is picking the wrong rung, by one to two rungs.

## Verdict
**PARK, with a PROTOCOL clause PROPOSED (not applied — rule 6).** Nothing here is a new book: it
is the record's existing TOP20 candidate priced under a cash convention the record does not
currently state. Proposed clause, for a Sunday review to accept or reject:

> *Any book that holds cash must publish its CASH CONVENTION beside its 4b verdict, and any claim
> about the WIDTH of a gross band must be published under at least two conventions.*

The g = 0.60 / SHY cell passes 4b full sample and OOS on 21 of 21 offsets, but it is **not** a
KEEP-candidate under PROTOCOL as written, because PROTOCOL as written prices cash at zero and
under that convention the cell passes only 16 of 21. Promoting it would require changing the
convention first. No memo proposing adoption is written.

## Caveats
- **SURVIVORSHIP**: `research/universe.json` is the CURRENT constituent list (idea 54); levels are
  optimistic and both 4b level bars are easier here than on a point-in-time panel.
- SHY is a ~1.9y-duration ETF, not a 3M bill, and is itself a panel constituent: an upper bound on
  a real cash credit, bracketed here by the FLAT150 / FLAT300 rungs.
- The credit is **not** applied to SPY (fully invested), so the 4b bars are unchanged; it **is**
  applied to RULES v2, which de-grosses.
- 2020 and 2022 are the only real stress episodes in the window.
- Rule 6: a rules or PROTOCOL change is a Sunday-review decision. This is not a proposal to apply.
