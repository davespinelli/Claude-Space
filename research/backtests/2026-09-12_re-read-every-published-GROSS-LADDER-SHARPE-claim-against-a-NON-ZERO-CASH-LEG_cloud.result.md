# Idea 799 — re-read every published GROSS-LADDER SHARPE claim against a NON-ZERO CASH LEG

**Run:** cloud, 2026-09-12.
**Script:** `2026-09-12_re-read-every-published-GROSS-LADDER-SHARPE-claim-against-a-NON-ZERO-CASH-LEG_cloud.py`
**Verdict: ANSWERED — the record's Sharpe-across-gross prose is a ZERO-CASH artefact almost in
full: 2 of 507 committed claims survive a 150 bps credit, and on manual read BOTH survivors are
parsing artefacts, so the honest count is 0. KILL for capital; no KEEP claimed, and every 4b pass
the credit buys is named an artefact of an uncredited comparand.**

## The headline number

| claim set | n claims | survive @ 0 bps (the record's own convention) | @ 150 bps | @ 300 bps |
|---|---|---|---|---|
| **STRICT** (comparison/invariance marker required) | **507** | **0.941** | **0.004** | **0.004** |
| STRICT, directional only (INVARIANT + SIGNED + PAIR) | 147 | 0.959 | 0.014 | 0.014 |
| STRICT, **INVARIANT** ("Sharpe is g-invariant/flat") | **118** | **0.992** | **0.000** | **0.000** |
| STRICT, PAIR (two named grosses compared) | 17 | 0.824 | 0.000 | 0.000 |
| WIDE (any Sharpe + gross sentence) | 1030 | 0.941 | 0.002 | 0.002 |

The 0 bps column is the scorer's own control: at the convention the claims were measured under,
94.1% of them reproduce, and **99.2% of the explicit invariance claims** do. Change nothing but
what the idle money earns and the same claims read **0.4%**.

**The two "survivors" are not survivors.** Both are SIGNED claims whose extracted sign happens to
match the credited slope: `LEADERBOARD.md:4840` is a *prescription* sentence about
rho(cost-statistic, c\*) whose −0.755 is a correlation, not a slope, and `CHANGELOG.md:306` quotes
a **range** ("−0.001 to +0.008") whose first signed number is negative. Neither is a claim that
Sharpe *falls* in gross. **0 of 507 committed claims survive on a manual read.**

## The census

- Corpus fixed before any claim was read: **803 committed files** — `research/backtests/*.md`
  (the published memos) + `LEADERBOARD.md` + `CHANGELOG.md`. `QUEUE.md` is excluded: proposals are
  not claims. Scripts and consoles are excluded: a claim is something the record *published*.
- **1,030 distinct claims** across **226 files** (507 STRICT / 523 WIDE-only), classified
  INVARIANT 118 / SIGNED 13 / PAIR 25 / OTHER 874.
- Cell recovery: a panel is named in **232** of 1,030 claims (U56 162, B136 42, small 28), a form
  in 45, a cadence in 55. The rest are scored against the **pooled median** cell — reported, not
  hidden, and the pooled and panel-specific verdicts agree because 0 of 36 cells is positive at
  150 bps.

## The mechanism: it is the idle weight, exactly

**H_IDLE PASS.** Over all 612 books, the credited-minus-uncredited CAGR gap equals
`rate × mean idle weight` to a **median ratio of 1.084** at 150 bps (p05 1.017, p95 1.177) and
1.080 at 300; `rho(idle weight, |ΔSharpe|) = +0.976` at both rates. Idle weight is mechanical in
g (0.80 at g=0.20 → 0.00 at g=1.00), and **MA-DG** — the de-grossing form, median idle **0.610** —
is the form the record most often quotes a gross ladder for. The most idle-heavy failures are
quoted verbatim in the console with their idle weights beside them, per the queue's request.

Slope in g, over the 36 (panel × form × cadence) cells, FULL window:

| cash | min | median | max | cells with slope > 0 |
|---|---|---|---|---|
| 0 bps | −0.0088 | **+0.0060** | +0.0400 | 32/36 |
| 150 bps | −0.6884 | **−0.3414** | −0.1341 | **0/36** |
| 300 bps | −1.3677 | **−0.6832** | −0.3058 | **0/36** |

## Rule 8 walk-forward

**WF-A (claim level).** Survival verdicts recomputed on IS (≤2016) and OOS (≥2017) alone.
At 150 bps IS survival 0.002, OOS 0.010, **agreement 0.992** — the kill is not a window artefact
(**H_WINDOW PASS**). The informative side-result is at **0 bps**: IS survival **0.166** vs OOS
**0.945**, agreement only 0.219. The record's own g-invariance is an **OOS-window fact even at its
own convention**: on the pre-2017 window alone, 83.4% of the same claims already fail idea 311's
own bar with the idle fraction earning nothing.

**WF-B (a book).** Form and g chosen by IS Sharpe on B136/W at each rate; OOS read once.

| cash | IS pick | idle | OOS CAGR | OOS Sharpe | OOS MaxDD | RULES v2 (credited) OOS | SPY OOS | 4a | 4b |
|---|---|---|---|---|---|---|---|---|---|
| 0 bps | TOP10 g=1.00 | 0.000 | 20.93% | 0.846 | −33.52% | 7.98% / 1.119 / −12.24% | 15.45% / 0.882 / −33.72% | False | False (H2,OOS,DD) |
| 150 bps | MA-DG g=0.20 | 0.858 | 3.40% | 1.821 | −3.37% | 8.74% / 1.218 / −12.20% | 15.45% / 0.882 / −33.72% | True | **False (CAGR)** |
| 300 bps | MA-DG g=0.20 | 0.858 | 4.72% | 2.503 | −3.29% | 9.50% / 1.315 / −12.16% | 15.45% / 0.882 / −33.72% | True | **False (CAGR)** |

The credited IS selector walks straight into the **most idle book on the ladder** (86% cash) and
its 4a passes are bought by exactly that: high Sharpe on a 3–5% CAGR. **4b fails on CAGR at every
rate.** No KEEP.

## KEEP paths — every book, every rate

| cash | books | 4a | 4b | BOTH | binding 4b legs |
|---|---|---|---|---|---|
| 0 bps | 612 | 34 | 50 | 0 | CAGR 336, DD 273, H2 221, OOS 221, H1 130 |
| 150 bps | 612 | 124 | 69 | 0 | CAGR 307, DD 268, H2 204, OOS 198, H1 76 |
| 300 bps | 612 | 142 | 95 | **1** | CAGR 277, DD 266, H2 165, OOS 155, H1 51 |

150 bps buys **19** new 4b passes and loses 0; 300 bps buys **45**. **H_NOFREE:** every one of them
is a pass against SPY, which is fully invested and receives **no** credit. None is a capital
candidate and none is claimed as one.

## Gates

| gate | reading | bar | verdict |
|---|---|---|---|
| G1 identity (fast vs `engine.backtest`) | 2.776e-17 | 1e-12 | PASS |
| G2 cash-0 (credited runner at rate 0 vs plain) | 2.290e-16 | 1e-12 | PASS |
| G3 repro (idea 576's committed grid, 1,836 rows) | max \|ΔSharpe\| 4.441e-16, max \|Δidle\| 9.714e-17 | 1e-9 | PASS |
| G4 census (idempotent harvest, STRICT ⊂ WIDE) | 1,030 distinct claims | — | PASS |

## Hypotheses

H_HARVEST **PASS** (507 STRICT ≥ 50) · H_FAIL **PASS** (INVARIANT survival 0.000 < 0.50) ·
H_SIGN **PASS** (0 of 5 positive-slope claims survive) · H_IDLE **PASS** · H_WINDOW **PASS** ·
H_NOFREE **PASS**.

## Caveats, stated plainly

- A **flat** 150/300 bps over 2009–2026 is not the cash rate that existed (~10 bps to 2015, ~500
  after 2022). This prices the **convention**, not a forecast; idea 642 holds the real-instrument
  (SHY) version. A claim that fails here is a claim whose truth depends on an **undeclared dial** —
  that is the finding — not one proven false at the rate that actually obtained.
- Claims are matched to cells by keyword. 798 of 1,030 name no panel and are scored against the
  pooled median; with 0 of 36 cells positive at either credit, no plausible re-mapping changes the
  verdict, but the mapping is a stated approximation.
- **Survivorship:** B136 and the small panel are current constituents; dead names are absent, so
  every panel return here is biased upward.

## What the record should do

Every published Sharpe comparison across gross should state the **cash convention and the book's
idle weight** beside it, exactly as PROTOCOL already requires costs and cadence. A gross ladder run
at 0% cash is a ladder in *how much of the book is switched off*, and its Sharpe is not comparable
across rungs. This is a candidate PROTOCOL line for Sunday review — **not** a rules change, and
**no** KEEP is claimed from this run.
