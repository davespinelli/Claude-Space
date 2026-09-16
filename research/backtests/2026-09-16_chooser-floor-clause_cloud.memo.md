# MEMO — PROTOCOL rule 8 CHOOSER FLOOR clause (PROPOSED, NOT APPLIED — rule 6)

Source: idea 1023 (cloud lane, 2026-09-16),
`2026-09-16_should-a-RULE-8-CHOOSER-be-scored-on-PICK-STABILITY-rather-than-IS-FIT_cloud.py`.
This is a REPORTING clause. It changes no bar, promotes no book, and does not touch `RULES.md`,
`PROTOCOL.md`, `scan.py`, `bot.py` or `baseline.py`.

## Exact RULES wording (to be added to PROTOCOL.md rule 8 at a Sunday review, not before)

> **8b (chooser floor, added 2026-09-16).** Every rule-8 result is published beside a **UNIFORM
> RANDOM** pick from the same selection pool, drawn over the same end grid with at least 200
> independent sequences, reporting the random control's **mean OOS Sharpe** and its **4b pass
> rate** against the chooser's own. A chooser the random control beats on OOS Sharpe is named as
> such in the result. A chooser the random control beats on **both** OOS Sharpe and 4b pass rate
> is not used to select a book for promotion. Pick stability is reported but is **not** a
> scoring criterion: where a stability statistic is quoted, all of {distinct picks, modal share,
> published-OOS-Sharpe band} are quoted, because they do not agree on the sign of the
> stability-return trade.

## Why

The queue asked whether a rule-8 chooser should be scored on pick stability rather than IS fit.
Both halves of that question fail on measurement.

**Stability is not a scoreable axis.** Over the record's own three choosers, ρ(instability, mean
OOS Sharpe) is **+1.0000** with `NUNIQ` (1013's statistic) and **−1.0000** with `OOS_BAND` in the
same U56 / 10 bps cell. The three statistics agree on the SIGN of the trade in only **8 of 12**
cells and disagree in **all three** U56 cells. A concrete, rule-8-legal stabiliser (BANDMODE:
modal pick over E and the three preceding quarter-ends) costs a mean **−0.0018** of OOS Sharpe
and buys a mean **−0.11** distinct picks — free and useless in roughly equal measure.

**IS fit has never been floored.** The record has run IS-only choosers since rule 8 was written
and has never compared one to a coin flip. It should have: a uniform draw from the same pool
beats `IS_SHARPE` in **5 of 6** panel x cost cells (mean margin +0.0418) and `IS_LEGS` in **5 of
6** (+0.0545), and beats **all three** at U56 / 25 bps. It beats `IS_CAGR` in **1 of 6** (mean
margin −0.0222). On the broad panel the coin flip beats the two stable choosers on 4b pass rate
as well (−0.0498 / −0.0822 / −0.0227).

**What IS fit is worth is a verdict, not a Sharpe.** `IS_CAGR`'s band 4b pass rate is **0.979**
against the random control's **0.469** — a **+0.510** gap — while its OOS Sharpe edge is
**+0.0222**. That is the axis the clause scores on.

## What it re-labels on the record as it stands

It names `IS_SHARPE` and `IS_LEGS` in the 5 of 6 cells where the coin flip beats them on OOS
Sharpe, and disqualifies both from selecting a book for promotion in the 3 B136 cells where it
beats them on both axes. `IS_CAGR` clears the floor in 6 of 6. No published verdict changes: no
rule-8 pick in this record was promoted, and OOS 4a remains 0 of 36.
