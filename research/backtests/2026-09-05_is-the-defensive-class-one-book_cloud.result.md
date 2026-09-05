# Idea 133 — is-the-defensive-class-one-book-in-disguise (cloud, 2026-09-05)

**ANSWERED — the class is NOT one book, and it is not an exposure band either. PROTOCOL should
name the CLASS, not the book.** Widening idea 129's corpus along the two axes the leaderboard
actually publishes — position count and the multi-asset sleeve, both at **matched gross 0.75** —
turns the `4b-defensive` class from 27 rows / 1 book into **138 rows / 6 books / 61 distinct
(book, arm) constructions**, of which **112 are not EWall** and **51 sit at full gross (≥ 0.74)**.

Corpus: 3 panels × {EWall, V1u, R5, R10, R20, R40, S3-25, S3-50, S4-50} × idea 94's 17 overlays ×
{10, 25} bps = **816 arm-rows**, plus a **240-row static-gross ladder control**. All reported.
Exactly two tuned parameters (n ∈ {5,10,20,40}, sleeve fraction f ∈ {0.25,0.50}).

## Harness (all checks before any new number was read)
* Idea 94's simulator and idea 129's census functions (`bars_win`, `margins_at`, `fails`,
  `pareto_front`) are **imported, not re-implemented** — literally the same census.
* Engine-equivalence on all 24 ungated (panel, book) controls: **max|diff| = 0.000e+00**.
* All **306** of idea 129's rows reproduce arm-for-arm: max|diff| CAGR 9.7e-17, Sharpe 2.2e-16,
  MaxDD 9.7e-17, OOS Sharpe 2.2e-16. Idea 94's published `EWall+vol60-dg` u56 @10bps re-derives
  at 11.6% / 1.133 / −16.9%.

## 0. The premise, audited against idea 129's own file
Of the 11 Pareto-best floor-only KILLs, **10** are EWall + trend gate + `dg`; the 11th is
`broad / EWall / 25bps / ddctl-8/.5/recover` at 0.661 gross — a book drawdown control, not a gate.
In the full floor-only set: **26 of 27 EWall**, but only **16 `dg`** (2 `rw`, 9 non-gate overlays)
and one `TOP20`. The queue's "all EWall + a slow trend gate de-grossed to ~53%" was already an
approximation of its own source.

## 1. The class on the widened corpus
| | rows |
|---|---|
| 4b-defensive (fails ONLY the CAGR floor) | **138 of 816 (16.9%)** |
| by book | S3-50 45, S4-50 44, EWall 26, S3-25 12, R40 10, R20 1 |
| not EWall | **112 of 138** |
| not "EWall + gate + dg" | **122 of 138** |
| distinct (book, arm) constructions | **61** |
| by convention | dg 55, none (no gate) 55, **rw 28** |
| gross: min / median / max | 0.519 / 0.717 / **0.750** |

**The decisive members are six sleeve books with no overlay at all.** `S3-50 / control` and
`S4-50 / control` — a 50/50 blend of the ranked top-20 book and a momentum × risk-parity sleeve of
(TLT, GLD, UUP[, DBC]), at full matched gross — are 4b-defensive on both large-cap panels:

| panel | book | cost | CAGR | Sharpe | MaxDD | OOS Sharpe | gross | CAGR shortfall |
|---|---|---|---|---|---|---|---|---|
| u56 | S3-50 control | 10 bps | 10.1% | **1.276** | −12.2% | 1.241 | 0.750 | **−0.6 pp** |
| u56 | S4-50 control | 10 bps | 10.4% | 1.259 | −13.1% | 1.267 | 0.750 | −0.3 pp |
| broad | S3-50 control | 10 bps | 9.9% | 1.108 | −13.1% | 1.024 | 0.750 | −0.8 pp |

(SPY 15.2% / 0.889 / −33.7%, OOS 0.882.) A book with no gate, no stop and no de-grossing, at the
same gross as everything else, is killed by 4b for missing the CAGR floor by 0.3–0.8 pp/yr while
holding a third of SPY's drawdown. That is the class's existence proof.

## 2. Pareto-best members: the sleeve, not EWall
Of the 17 class members on the (Sharpe, MaxDD) Pareto frontier of their own (panel, cost) cell:
**S3-50 10, EWall 4, S4-50 3**. Best of them: `u56 / S3-50 / ebud-0.10 / 10bps` at 9.9% / **1.291**
/ −11.1% (OOS 1.277), missing the floor by 0.7 pp. Idea 129's 11 EWall rows survive as a subset —
they were the frontier of a corpus that contained no diversified book but EWall.

## 3. The ladder control kills the "~53% gross" reading
Pure de-grossing (static multiplier, no rule at all) puts **88 of 240** ladder rows into the class,
spanning **all 8 books** — R5, R10, R20, R40, S3-25, S3-50, S4-50 and EWall — at gross 0.297–0.750.
So low gross is *sufficient* to enter the class but not *necessary*: 51 of 138 real members are at
full gross. **The class is defined by the floor, not by a construction and not by an exposure band.**

## 4. Rule 8 walk-forward — the floor is no longer inert in selection
(panel, cost) cells, argmax IS Sharpe over the widened corpus, OOS 2017-2026 read once:

| selector | picks | mean OOS CAGR | mean OOS Sharpe | mean OOS MaxDD | defensive picks |
|---|---|---|---|---|---|
| S0 no screen | 6 | 11.6% | 0.939 | −21.8% | 2/6 |
| S1 IS 4b screen **with** the floor | 4 | 12.4% | 1.111 | −17.3% | 0/4 |
| S2 the same, **floor deleted** | 4 | 10.1% | **1.124** | **−13.5%** | 3/4 |

**S1 ≠ S2 in 3 of 6 cells**, breaking idea 129's 0-of-18 on the narrow corpus: with a diversified
book in the corpus the floor starts changing picks, and it changes them for the worse — deleting it
buys +0.013 of OOS Sharpe and **3.8 pp of OOS drawdown** for 2.3 pp of OOS CAGR. Both screens admit
**nothing at all** on the small panel in either cost rung.

## 5. No new KEEP
88 of 816 rows pass 4b, but only **2 constructions pass in all four (u56/broad × 10/25 bps) cells**:
`EWall + vol60-dg` (the standing incumbent, 11.6-12.4% / 1.113-1.138 / −16.9..−18.7%) and
`EWall + band3-rw` (10.9-12.2% / 1.002-1.161 / −17.7..−18.7%). Widening the corpus by six books
produced **no new cross-cell 4b passer** — which is itself a result about how tight 4b is.

## 6. Predictions, scored (written before the main grid)
P1 the class has a non-EWall member → **HELD** (112). P2 every member is de-grossed (< 0.70) →
**FAILED** — 51 members sit at 0.75, so the class is not an exposure band. P3 EWall is the majority
of Pareto-best members → **FAILED** (S3-50 10, EWall 4, S4-50 3). P4 < 25% of members are `rw` →
**HELD** (20%). P5 S1 ≠ S2 in ≥ 1 cell → **HELD** (3 of 6).

## Caveats
Survivorship: three current-constituent panels (idea 54); the small panel drops the 44 names with
`max_1d_move ≥ 1.0` (439 names) and holds SPY out entirely, per idea 129. Absent delistings inflate
every arm's CAGR and inflate the ungated books most, so the floor's exclusion of defensive arms is
if anything understated. Idea 128: the IS window is shallower than OOS (−22.1% vs −33.7%), biasing
the S1/S2 screens toward admitting too much. Idea 126: t+1 execution only. Idea 127: mean gross is
reported on every row and the dg/rw split is never collapsed. The sleeve books exist only on
u56/broad, so every sleeve statement here is a two-panel statement. No level is an achievable return.

## Proposed wording (for Sunday review; RULES.md untouched)
> Idea 129's `4b-defensive` record should name the **class**, not a book: an arm that clears 4b's
> halves, OOS-Sharpe and drawdown bars and fails only the CAGR floor is recorded `4b-defensive`
> whatever its construction, and must state its CAGR shortfall in pp **and its mean realised
> gross** — because the class contains full-gross diversified books (sleeve controls at 0.750) as
> well as de-grossed trend books (EWall gates at 0.52), and the two are different objects.
