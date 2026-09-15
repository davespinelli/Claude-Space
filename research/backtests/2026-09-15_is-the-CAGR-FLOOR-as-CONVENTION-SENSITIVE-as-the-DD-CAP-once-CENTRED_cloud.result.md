# Idea 879 (cloud lane, idea 2 of 2, 2026-09-15) — is the CAGR FLOOR as CONVENTION-SENSITIVE as the DD CAP once its MARGINS are CENTRED?

**ANSWERED: YES — AT MATCHED MARGIN THE TWO LEGS ARE INDISTINGUISHABLE (7.46 vs 7.18 flips per
book, ratio 0.96). 808's "3 vs 52" measured WHERE ITS BOOKS SAT, not how sensitive the leg is.
KILL for capital.** Nothing promoted, no rule changed; `RULES.md`, `PROTOCOL.md`, `scan.py`,
`bot.py`, `baseline.py` untouched (rule 6). Script
`research/backtests/2026-09-15_is-the-CAGR-FLOOR-as-CONVENTION-SENSITIVE-as-the-DD-CAP-once-CENTRED_cloud.py`,
wall 248s, deterministic, no network.

SELECTION: the LAST open entry in QUEUE.md, per the cloud lane's rule.

## Design
Gross is the one dial that slides a book's CAGR smoothly through the 4b floor with its
construction otherwise untouched, so a gross ladder (0.30…1.50, step 0.10) over 5 book forms ×
2 panels sweeps every form's CAGR margin through zero. **Every form crosses the floor inside the
ladder** (U56: MADG 0.80→0.90, TOP20 0.50→0.60, TOP40 0.70→0.80, EWELIG 0.60→0.70, BAND3
0.80→0.90; B136 similar), which is what makes a centred population possible at all. 71 books
(28 CAGR-centred, 15 DD-centred, 29 FAR control at |margin| > 4pp) × 26 calendars (21 monthly +
5 weekly) × 2 lags × 2 costs. Two tuned parameters, the queue's own: **margin band {0.5, 1.0,
2.0} pp × offset grid {MONTHLY, WEEKLY}**; every grid point is printed.

**G1 engine gate:** max |fast_run − engine.backtest| = **2.082e-17**, bar 1e-9 — **PASS**.
**G3 direction check on 808's own books present here (2 of 12):** DD flips 19 vs CAGR 2,
DD ratio 0.498 vs CAGR 0.708 — **ORDERING REPRODUCED** (a direction check, not an equality bar:
this is a subset of 808's population, not that population).

## H_CONVERGE — CONFIRMED
MONTHLY, 10 bps, lag 1, flips per book:

| band | CAGR n | CAGR flips/book | DD n | DD flips/book | DD ÷ CAGR |
|---|---|---|---|---|---|
| 0.5 pp | 5 | 14.40 | 6 | 7.00 | 0.49 |
| **1.0 pp** (the queue's own) | **13** | **7.46** | **11** | **7.18** | **0.96** |
| 2.0 pp | 28 | 3.64 | 20 | 7.25 | 1.99 |
| **uncentred, \|margin\| > 4 pp** | **36** | **0.00** | — | — | — |

Every band lands inside the pre-registered bar (ratio in [0.5, 2.0]). The uncentred CAGR leg
flips **0.00 times per book over 36 books** — that is exactly the quantity 808 read as "3 flips",
and it is a fact about where those books sat. Restricted to **unleveraged books only**
(gross ≤ 1.00, PROTOCOL rule 2): 1.0 pp band gives CAGR 7.46 (n=13) vs DD 7.40 (n=5),
ratio **0.99**; the answer does not rest on the leveraged rungs. At 25 bps and lag 2 the ratios
run 0.49–5.54 across all 24 (band × grid × lag × cost) cells, all printed.

## H_SPREAD — CONFIRMED, and it is the reason the raw counts differ
Median 21-calendar spread over the 71 books: **CAGR 1.413 pp, DD 8.201 pp — DD is 5.80× wider**.
So at any given distance from its bar, a far larger share of books sits *inside* the DD leg's
spread. That, not a difference in the legs' nature, is what produced 808's 17× flip gap.

Total flips over 71 books, MONTHLY: **DD 221, H2 152, CAGR 102, OOS 42, H1 0**. The Sharpe legs
are not immune either — **H2 flips 152 times**, more than CAGR.

## H_RATIO — CONFIRMED at the boundary, REFUTED as a single curve
Both legs are monotone in |margin|/spread (Spearman **−0.585 CAGR, −0.629 DD**) and, decisively,
**both flip 0.00 times per book once the ratio reaches 1.00** (CAGR 55 books, DD 22 books, zero
flips in every one). That is the part a PROTOCOL clause could use. But the curves do **not**
coincide in level below the boundary — at ratio [0, 0.25) CAGR flips **15.00**/book against DD's
**6.41** — so "leg identity adds nothing once the ratio is known" is refuted as stated, and is
reported as such.

## What this costs the shelf, on this run's own population
Of the **18 books that pass 4b at k=0** (MONTHLY, 10 bps, lag 1), **18 of 18 have at least one
leg with margin/spread < 1, and 18 of 18 flip at least one leg on at least one calendar.** Not
one 4b pass in this population is calendar-robust. The record's own U56 MADG100 book is the
concrete case: its **DD leg passes at only 13 of 21 calendars (8 flips)** and its CAGR margin is
**1.31 pp against a 1.51 pp calendar spread (ratio 0.869)** — it clears the floor on all 21
offsets, but by less than the calendar can move it.

## PROPOSED, NOT APPLIED (rule 6)
808 proposed a convention floor for the **DD leg**. This run says that is the wrong shape: the
floor belongs to **every 4b leg**, stated scale-free — *no 4b leg may be reported as passing
unless its margin exceeds its own rebalance-calendar spread (margin/spread ≥ 1), and the spread
must be published beside the margin.* `PROTOCOL.md` is untouched.

## RULE 8 on the books (IS-only selector on 2009–2016, OOS 2017–2026 read once, 10 bps, next-day)
PROTOCOL rule 2 forbids leverage and idea 879 does not ask for it, so the pick is taken over
**unleveraged** books; the leveraged argmax is printed only to show what the ladder reached.

| panel | IS pick (gross ≤ 1.00) | FULL CAGR / Sharpe / MaxDD | halves | OOS CAGR / Sharpe / MaxDD | 4a | 4b |
|---|---|---|---|---|---|---|
| U56 | MADG-g1.00 | 11.90% / 1.208 / −15.49% | 1.255 / 1.165 | 12.61% / 1.267 / −15.49% | ✗ | **PASS** |
| B136 | TOP20-g0.90 | 19.55% / 1.097 / −30.71% | 1.336 / 0.910 | 18.70% / 1.003 / −30.71% | ✗ | ✗ |

Leveraged argmaxes, **not candidates**: U56 MADG-g1.50 18.05% / 1.211 / −22.41% (OOS 19.14% /
1.269) 4b fail; B136 TOP20-g1.50 33.11% / 1.107 / −47.36% (OOS 31.34% / 1.014) 4b fail.
SPY U56 **15.13% / 0.885 / −33.72%** (OOS Sharpe 0.874), B136 15.16% / 0.886 (OOS 0.877);
RULES v2 live baseline U56 Sharpe **1.201** (H 1.232/1.177, MaxDD −12.05%), B136 1.099.
Unselected base rate: **4a 1 (1.4%), 4b 18 (25.4%)** over 71 points; **4a 1 (2.3%), 4b 13
(29.5%)** over the 44 unleveraged points.

**The U56 MADG-g1.00 4b pass is NOT proposed.** It is the record's existing MADG100 book, its
population was built by sweeping gross onto the 4b bars so the pass rate is a property of the
construction, and this run's own headline shows its DD leg failing at 8 of 21 rebalance
calendars.

## Honest limits
The gross ladder's 0.10 step sets how finely a book can be centred, so the n in each band is
small (5–28 books per leg at 10 bps, lag 1) and flips/book is a noisy statistic; the ratio
bar [0.5, 2.0] was pre-registered for that reason. The centred population is built from 5 book
forms on 2 panels, not from the record's committed books, so this is a statement about the
LEGS, not a re-adjudication of any particular committed claim. Gross above 1.00 is leverage and
is admitted only as a ladder point. SURVIVORSHIP: U56 and B136 are current-constituent lists, so
CAGR and drawdown **levels** are optimistic; the reported quantity is a within-book margin
against its own calendar spread and is far less exposed. Binding drawdown 2020.

## Follow-ups queued
891 (does the margin/spread ≥ 1 clause empty the shelf on the record's committed 4b passes, or
only on this run's synthetic population), 892 (is the 5.80× DD/CAGR spread ratio a 2020 fact —
re-measure with the 2020 episode stripped), 893 (do the H2 leg's 152 flips mean the Sharpe legs
need the same clause, and at what cost to the record's committed half-sample claims).
