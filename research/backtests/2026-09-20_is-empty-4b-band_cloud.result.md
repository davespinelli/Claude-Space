# Idea 809 (lane cloud, 2026-09-20) — DOES ANY COMMITTED WIDTH-OR-GROSS 4b BAND HAVE AN **EMPTY IN-SAMPLE COUNTERPART**?

**ANSWERED — DOUBLE KILL. (1) 806's empty IS band is NOT general: 2 of 23 ladders, 8.7%, below the
pre-stated 10% bar, so "the IS band must be non-empty" is COSMETIC as a rule-8 clause and must not
be adopted. (2) The obvious replacement — "the published cell must itself be inside its own IS 4b
band" — looks strong (+0.5305 OOS Sharpe, +41.9 pp OOS-4b rate) and is CONFOUNDED BY PANEL: 24 of
its 30 suppressions are SMALL, and on the large panels the cells it would suppress cleared OOS 4b
at 6 of 6. KILLED too. (3) But EMPTINESS was the wrong diagnostic all along — the IS band is a
DIFFERENT SET, not a missing one: mean Jaccard 0.471, 9.33 rungs against the FULL band's 20.05,
and it contains the FULL band at only 6 of 21 ladders.**

## The question
Idea 806 retired both of 589's doubts about a width candidate and still killed it, because the IS
window's own 4b band was EMPTY — no width cleared 4b on 2009-2016, so 0 of 4 IS-only selectors
could reach a band that exists only on the full sample. If that is general, rule 8 needs "the IS
band is non-empty" as a precondition before any band is published, and much of the record's 4b band
prose is an ex-post-only object no live chooser could have traded. Idea 809 was SKIPPED on
2026-09-15 as having "no single book to price"; that reading is overturned here — it asks for every
RUNG of two committed ladders, each a real weights function.

## The construction
Both committed band families, every rung, three panels, scored **twice** — once on the FULL sample
against full-sample SPY bars, once **inside the IS window alone against SPY's own IS-window bars**,
reading nothing after the split date:

* **BAND** (the live RULES v2 ladder): `c` in {0.00 .. 0.12} x `G` in {0.50, 0.75, 0.85, 1.00} = 28
  rungs. Gate G4: the (c = 0.03, G = 0.75) rung **is** `baseline.rules_v2_weights`, max |dw| = 0.
* **VOLTGT** (the standing KEEP-candidate's ladder): `t` in {0.08 .. 0.20} x `h` in 10 rungs = 50.

3 panels x 78 rungs = **234 books**, x COST {10, 25, 50} bps x SPLIT {2016-12-31, 2018-12-31} =
**1,404 scored cells**. **TUNED: 2, and they are the idea's own — the band set and the split.** Every
rung, cost and panel is reported. Execution t+1 throughout. Gates **7 of 7**.

The IS band's third leg is a **stand-in** (SPY's IS second-half Sharpe in place of an OOS Sharpe a
chooser cannot see). Stated, not buried: V1 is reported both with it and with it dropped, and the
four-leg read gives the identical 2 of 23, so the substitution carries nothing.

## V1 — THE PRECONDITION IS COSMETIC (2 of 23 = 8.7%)
23 of 36 ladders have a non-empty FULL band. Exactly **2** are ex-post-only, and both are
**U56 / BAND at 25 and 50 bps on the 2016 split** — i.e. 806's own panel and own family, at costs
above the headline. By family: BAND 2/11, **VOLTGT 0/12**. By split: 2016 2/12, **2018 0/11**. So
806's diagnosis was right about its own candidate and wrong as a law. **KILL on the general clause.**

## V2 — EMPTINESS WAS THE WRONG DIAGNOSTIC: THE IS BAND IS A *DIFFERENT SET*
Over the 21 ladders where both bands are non-empty: mean **Jaccard 0.471** (median 0.421, min
0.111, max 1.000). The IS band averages **9.33 rungs against the FULL band's 20.05**. The IS band
contains the FULL band at only **6 of 21**; the FULL band contains the IS band at 11 of 21. Worst
case, `B136 / BAND / 25 bps / 2018 split`, has 1 FULL rung and 9 IS rungs with Jaccard **0.111** —
a chooser standing at the split date would have had nine candidates and one of them right.
**This, not emptiness, is the real hazard, and it is the part the record has never published.**

## V3 — THE PRE-STATED TEST WAS MIS-SPECIFIED, AND IS REPORTED RATHER THAN REWRITTEN
Pre-stated V3: adopt only if the restricted chooser does not lose OOS Sharpe AND removes OOS 4b
failures. Applied as written it reads **REJECT** on a paired mean of **-0.0012** Sharpe (1 win, 1
loss). That number is meaningless: on **42 of the 44** paired decisions both arms pick the **same
rung**, so the paired channel is a no-op by construction and the pre-stated rule never scored the
precondition's only real effect, which is suppression. The rule is named as mis-specified rather
than quietly replaced, and everything below is **POST-HOC** and weaker evidence accordingly.

Unconditional arm: 72/72 published, OOS 4b 32, mean OOS Sharpe 0.9505. Restricted arm: 44/72
published, OOS 4b 27, mean OOS Sharpe 1.1721. Suppressed (n = 28): the unconditional pick would
have cleared OOS 4b at **4 of 28**, mean OOS Sharpe 0.6003 against SPY's 0.8975.

## V3b — AND THE SHARPER PRECONDITION DIES ON THE PANEL CONFOUND (the second KILL)
**30 of 72 (41.7%) unconditional IS-argmax picks sit OUTSIDE their own IS 4b band** — the record's
standard rule-8 chooser routinely publishes a cell its own IS window says fails 4b. The headline
split looks decisive: INSIDE (n = 42) mean OOS Sharpe **1.1715**, OOS 4b **61.9%**; OUTSIDE (n = 30)
**0.6410** and **20.0%** — a +0.5305 / +41.9 pp gap.

**It does not survive holding panel fixed.** 24 of the 30 OUTSIDE picks are SMALL665, which clears
4b at **0 of 468** cells no matter what. On the large panels: B136 IN n=22 / OUT n=2 with dSharpe
**-0.0920**; U56 IN n=20 / OUT n=4 with dSharpe +0.1033 — and the OUT picks on the large panels
cleared OOS 4b at **6 of 6**. The whole apparent lift is SMALL-panel selection. **KILL: the sharper
precondition is not a replacement clause either.**

## V4 — THE STANDING KEEP-CANDIDATE IS NOT AN EX-POST-ONLY OBJECT
`B136 VOLTGT t = 0.10, h = 0.08` is inside its own ladder's IS 4b band at **5 of 6** (cost, split)
cells, binding leg `none`. It fails only at **(50 bps, 2016 split)**, on H2 / third leg / CAGR — the
same three legs that bind it elsewhere. OOS at the headline: **13.01% / 1.2928 / -11.81%**.

## SMALL665
**0 of 468 cells inside the FULL band and 0 inside the IS band, on both families, at every cost and
both splits — an eighth independent confirmation that neither family works on small caps.**

## What it changes
1. **No PROTOCOL change is proposed.** 806's "the IS band is non-empty" clause is killed as a
   general precondition (8.7%), and so is the sharper cell-membership version (panel confound).
2. **A reporting requirement is proposed instead, because V2 is the finding that survives:** any
   published band should state its **IS-band Jaccard** alongside it. The record has been publishing
   FULL bands roughly twice the size of the band a chooser could actually see, overlapping them
   about half the time, and has never said so.
3. The standing 4b KEEP-candidate is unaffected and slightly strengthened (V4: 5 of 6, and the one
   failure is at 50 bps, off the headline cost).

## Survivorship
U56 / B136 are CURRENT-constituent lists and SMALL665 a CURRENT sub-$2B screen (54 tickers with
`max_1d_move >= 1.0` in `data/small_meta.csv` dropped first). Every CAGR and drawdown LEVEL is
optimistic and every 4b bar is easier here than on a point-in-time panel. The IS-vs-FULL band
CONTRAST is same-tape / same-names / same-ladder and first-order immune; the BAND MEMBERSHIP COUNTS
are not. RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are untouched.

## Evidence
`research/backtests/2026-09-20_is-empty-4b-band_cloud.py` / `.log.txt` / `.console.txt` /
`.grid.csv.gz` (1,404 cells) / `.ladders.csv` (36) / `.walkforward.csv` (144 = 72 decisions x 2
arms) / `.candidate.csv` (6) / `.gates.csv` (7/7).
