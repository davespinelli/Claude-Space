# Idea 1023 (cloud lane, 2026-09-16) — should a RULE-8 CHOOSER be scored on PICK STABILITY rather than IS FIT?

**ANSWERED = NO, AND THE QUEUE'S AXIS IS THE WRONG ONE. KILL the "score choosers on pick
stability" proposal: the sign of the stability-return trade is a property of the STABILITY
STATISTIC, not of the choosers (the three definitions agree on the sign in 8 of 12 cells and
disagree in all 3 U56 cells), and a concrete stabiliser is a near-no-op (mean ΔSharpe −0.0018).
KILL "stability costs return" as the mechanism: what costs return is WHICH IS statistic a
chooser reads — a UNIFORM COIN FLIP from the same pool beats `IS_SHARPE` in 5 of 6 cells and
`IS_LEGS` in 5 of 6, and beats `IS_CAGR` in 1 of 6. KEEP a PROTOCOL rule 8 CHOOSER FLOOR clause
(proposed, not applied — rule 6). Nothing promoted, no RULES change; `RULES.md`, `PROTOCOL.md`,
`scan.py`, `bot.py` and `baseline.py` untouched.**

Script: `2026-09-16_should-a-RULE-8-CHOOSER-be-scored-on-PICK-STABILITY-rather-than-IS-FIT_cloud.py`

## The grid

The 36 never-memo-selected GRID ladder books (18 U56 / 18 B136) re-read at 1013's own **16**
quarter-ends 2015-03-31..2018-12-31 x **3** cost rungs = **2,160 ladder rows**; **7** choosers
(the record's three, their BANDMODE-stabilised twins, and RANDOM) x 2 panels x 3 rungs x 16 ends
= **576 chooser rows**, plus **400** independent RANDOM chooser SEQUENCES per (panel, cost).
Two tuned axes only, the queue line's own — CHOOSER SET {REC3, STAB3, NULL1} x STABILITY
STATISTIC {NUNIQ, MODE_SHARE, OOS_BAND} — all points reported, none selected. Every headline
number is a **band mean**, not the value at any one end; reporting the best end would be
selection on the OOS window.

Two controls 1013 did not carry:

- **RANDOM** — a chooser picking uniformly from the same pool at every end. Maximally unstable,
  reads no IS data. If instability *per se* bought return, it would beat everything.
- **BANDMODE** — a rule-8-legal stabiliser: at end E, run the raw chooser at E and the three
  preceding quarter-ends and take the modal pick. It is the concrete thing PROTOCOL would adopt
  if it scored choosers on stability, and its cost is measured directly.

## The trade is not a fact about the choosers — it is a fact about the statistic

**H_COST PASS, and the pass is the least interesting thing in the run.** With 1013's own NUNIQ
at U56 / 10 bps, ρ(instability, mean OOS Sharpe) = **+1.0000** — stability costs return. With
`OOS_BAND` in the same cell it is **−1.0000** — stability pays. The three stability statistics
agree on the SIGN of the trade in **8 of 12** (set x cell) combinations and disagree in **all
three** U56 cells for the record's own chooser set:

| set | panel | cost | NUNIQ / MODE_SHARE / OOS_BAND | unanimous |
|---|---|---|---|---|
| REC3 | U56 | 0 | +1 / −1 / −1 | **False** |
| REC3 | U56 | **10** | **+1 / +1 / −1** | **False** |
| REC3 | U56 | 25 | +1 / +1 / −1 | **False** |
| REC3 | B136 | 0 | 0 / 0 / −1 | True |

A ranking whose sign flips with the definition of the ranking variable cannot be the basis of a
PROTOCOL clause. (It is also a rank correlation over **three** points, two of which are the same
book in most cells — the statistic is barely defined.)

## The decisive control: a coin flip beats both STABLE choosers

**H_RANDOM FAIL (1 of 6 cells), H_RAND2 FAIL (11 of 18 pairs).** Mean OOS Sharpe over the band,
RANDOM minus the chooser — positive means the coin flip wins:

| chooser | RANDOM wins | mean margin | chooser 4b rate | RANDOM 4b rate | **4b gap** |
|---|---|---|---|---|---|
| `IS_SHARPE` (stable) | **5 of 6** | **+0.0418** | 0.729 | 0.469 | +0.260 |
| `IS_LEGS` (stable) | **5 of 6** | **+0.0545** | 0.729 | 0.469 | +0.260 |
| `IS_CAGR` (unstable) | **1 of 6** | **−0.0222** | **0.979** | 0.469 | **+0.510** |

At U56 / 10 bps: RANDOM **1.2433** against `IS_SHARPE`/`IS_LEGS` **1.1557** and `IS_CAGR`
**1.2618**. At U56 / 25 bps RANDOM (1.1479) beats **all three**, including the best.

This is the run's answer and it is not the queue's framing. Instability *per se* buys nothing —
RANDOM is the most unstable chooser there is and it loses to `IS_CAGR` in 5 of 6 cells. What
separates the choosers is **which IS statistic they read**: `IS_CAGR` dominates a coin flip on
both axes everywhere, while the two stable choosers are beaten by one on OOS Sharpe in 5 of 6
cells and on 4b pass rate in **3 of 6** (all three B136 cells: −0.0498, −0.0822, −0.0227). Their
stability is not the cause of their weakness; it is a symptom of the same thing — they converge
on `band0.08@1.00`, a low-return book, and stay there.

## What IS fit actually buys: verdict reliability, not Sharpe

Over the band, `IS_CAGR`'s 4b pass rate is **0.979** against RANDOM's **0.469** — a **+0.510**
gap — while its OOS Sharpe edge over RANDOM is **+0.0222**. IS fit is worth about half a verdict
and about two hundredths of a Sharpe. Any clause scoring choosers should be scored on the first,
not the second.

## The concrete stabiliser is a no-op in both directions

**H_STAB PASS.** BANDMODE costs a mean **−0.0018** of OOS Sharpe (worst **−0.0173**, at
U56/0bps/`IS_SHARPE`) — free. It also buys almost nothing: mean ΔNUNIQ **−0.11**, strictly more
stable in **4 of 18** cells, and **exactly zero** effect in all 6 B136 cells at 10 and 25 bps.
Per chooser: `IS_CAGR` −0.0024 Sharpe for −0.50 NUNIQ, `IS_SHARPE` −0.0031 for 0.00,
`IS_LEGS` +0.0002 for **+0.17** (it makes `IS_LEGS` *less* stable in one cell). Stabilising
`IS_CAGR` is the one case that both works and is free — which is the opposite of "stability
costs return".

## 1013's ordering is not cost-invariant

**H_SIGN FAIL.** `IS_CAGR` beats `IS_SHARPE` on mean OOS Sharpe in **5 of 6** cells but loses at
B136 / 25 bps (**0.9944** vs **1.0216**). 1013's 1.162-vs-1.293 gap is a U56 / 10 bps reading,
not a property of the choosers.

## Rule 8 and both KEEP paths

The whole experiment is a rule-8 walk-forward. At PROTOCOL's own split, picks made on
2009-01-13..2016-12-31 **alone** from the never-memo-selected GRID pool, 2017–2026 read once,
at 10 bps:

- U56 `band0.08@1.00` (`IS_SHARPE`, `IS_LEGS`, and both their BANDMODE twins) **11.99% / 1.162 / −19.05%**
- U56 `qroll-q0.17-w1008-d0.50` (`IS_CAGR`, `BM_IS_CAGR`) **15.60% / 1.293 / −15.59%**
- B136 `band0.08@1.00` **11.05% / 1.097 / −19.50%**; B136 `qroll-q0.12-w1008-d0.50` **14.30% / 1.157 / −17.31%**
- RANDOM at the declared split: U56 **13.21% / 1.278 / −15.38%**, B136 **11.53% / 1.138 / −15.99%**

Comparands: **SPY OOS 15.21% / 0.871 / −33.72%** (U56) and **15.33% / 0.877 / −33.72%** (B136);
**RULES v2 (live, 10 bps) full 8.62% / 1.201 / −12.05%** (H1 1.232 / H2 1.176) on U56 and
**7.98% / 1.099 / −12.24%** (H1 1.235 / H2 0.966) on B136. SPY's own OOS Sharpe moves
0.7946..0.9209 across the 16 ends.

**OOS 4b is 36 of 36** for the deterministic choosers at the declared split and **0.8142** over
the whole 576-row band grid; RANDOM's band 4b rate is **0.338..0.612**. **OOS 4a is 0 of 36**,
and **0.0000** over the whole grid — no chooser's pick beats the live book's −12.05% drawdown at
any end, on either panel, at any rung. **Nothing is promoted.**

## Gates 7 of 7 PASS, printed before any result number

G1 `fast_run` == `engine.backtest` on returns AND turnover **6.939e-18 / 1.665e-16**. G2 band
book == `baseline.rules_v2_weights` **0.000e+00**. G3 CROSS-RUN SPY OOS at 2016-12-31 reads
**15.2102% / 0.8711 / −33.7173%**, max|d| **1.702e-04**. **G4 CROSS-RUN: all four of 1013's
published declared-split picks reproduce their OOS triples, 4 of 4, max|d| 4.588e-04**
(**H_REPRO PASS**: `IS_SHARPE` == `IS_LEGS`, `IS_CAGR` differs, 1.1615 and 1.2933 against 1013's
1.162 and 1.293). G5 determinism over the 2,160-row ladder **0.000e+00**. **G6 IS PURITY**: every
chooser's pick invariant under a permutation of the OOS returns, **0 moved of 60**. **G7 BANDMODE
LEGALITY**: its pick at E is a function of raw picks at ends ≤ E only, **0** disagreeing cells.

## Limits, stated

The end grid is QUARTERLY and spans 2015–2018, both inherited from 1013; a daily grid would find
more pick changes, so every NUNIQ here is a LOWER bound and every MODE_SHARE an UPPER bound. The
pool is 18 books per panel, so a uniform draw is a 1-in-18 lottery and RANDOM's band statistics
(NUNIQ ≈ 11, MODE_SHARE ≈ 0.18) are sample means over 400 sequences, not exact. The Spearman
statistics rest on **three** chooser points each and two of the three choosers coincide in most
cells; they are reported because the queue asked for a ranking, and their instability across
statistics is the finding, not a defect to be smoothed. BANDMODE's look-back is fixed at 4
quarters and is not tuned.

## Survivorship (rule 9)

U56 and B136 are CURRENT-CONSTITUENT lists, so every CAGR and drawdown LEVEL is optimistic and
every 4b count an UPPER bound. The measured object is a DIFFERENCE between choosers reading the
SAME pool over the SAME tape, and the bias is a common factor to all of them. Where it does not
cancel it flatters RANDOM — a uniform draw from a survivor panel is a BETTER book than a
real-time one — so RANDOM's numbers are an UPPER bound and **H_RANDOM / H_RAND2 were the HARDER
calls, and they failed anyway**. SPY is a real index series and is not inflated.

## Proposed, not applied (rule 6)

`2026-09-16_chooser-floor-clause_cloud.memo.md` proposes a PROTOCOL rule 8 clause: *every rule-8
result is published beside a UNIFORM RANDOM pick from the same selection pool, drawn over the
same end grid, reporting both mean OOS Sharpe and 4b pass rate; a chooser the coin flip beats on
OOS Sharpe is named as such in the result, and a chooser it beats on BOTH is not used to select a
book for promotion.* On the record as it stands this names `IS_SHARPE` and `IS_LEGS` in 5 of 6
cells on Sharpe and disqualifies both in the 3 B136 cells where the coin flip beats them on both
axes; `IS_CAGR` clears it in 6 of 6.

Follow-ups filed: 1030, 1031, 1032.
