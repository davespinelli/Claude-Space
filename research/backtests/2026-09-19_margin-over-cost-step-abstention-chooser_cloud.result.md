# Idea 1578 — is a MARGIN-OVER-COST-STEP ABSTENTION RULE a better rule-8 chooser than ARGMAX IS SHARPE?

**2026-09-19, lane cloud (idea 2 of 2).  VERDICT: ANSWERED — ALL THREE PRE-REGISTERED TESTS PASS,
AND KILL FOR CAPITAL.**  9/9 gates PASS, 67 s.
Script `2026-09-19_margin-over-cost-step-abstention-chooser_cloud.py`.

## The defect this attacks

Nine 2026-09-19 runs have had their rule-8 chooser lose to doing nothing.  Idea 1562, this lane's
own first idea, showed the arithmetic: its chosen U56 cell's whole OOS margin over the anchor is
+0.0041 of Sharpe while the *same book* loses −0.0415 of Sharpe moving from 10 to 25 bps.

## The rule

**C_ABSTAIN.**  Take the family's IS argmax exactly as rule 8 does.  Then, **on IS rows only**,
accept it if its IS Sharpe margin over its own **IS-CAGR-matched constant de-gross twin** exceeds
`k` times its own IS cost-step sensitivity |Sharpe@10bps − Sharpe@STEP|; otherwise **abstain and
hold the frozen anchor** (constant gross 0.75).  Two tuned parameters, `k` ∈ {0.5, 1, 2} and
STEP ∈ {25, 50} bps; all six cells published.  Five device families over the same frozen incumbent
frame, 34 rungs per panel, three panels = **102 rungs, every one published**.

## THE DEFECT IS REAL AND IT IS ENORMOUS

Median IS margin over its own twin against median IS cost-step sensitivity, per (panel, family):
**the margin exceeds one 10→25 bps cost step at 6 of 102 rungs and exceeds TWO steps at 0 of 102.**
On U56 the medians run F_TWOSTATE −0.0017 / F_DEGROSS +0.0000 / F_VOLTGT +0.0322 /
F_STOP −0.3213 / F_BREADTH −0.0031 against sens25 of 0.0428 / 0.0340 / 0.0368 / 0.0176 / 0.0500.
Ten further rungs have **no constant de-gross twin at all** (their CAGR is outside what the
constant ladder can reach); the rule abstains on those by construction.

## The race (rule 8: params on warm-up..2016-12-31 ONLY; 2017-01-01..2026-09-18 read ONCE)

| k | STEP | C_ISSHARPE | **C_ABSTAIN** | ANCHOR (do nothing) | ex-post best rung | accepts | regret SEL | regret ABS |
|---|---|---|---|---|---|---|---|---|
| 0.5 | 25 | 0.7443 | **0.8729** | 0.8812 | 0.8634 | 5/15 | +0.1192 | −0.0094 |
| 0.5 | 50 | 0.7443 | **0.8812** | 0.8812 | 0.8634 | 0/15 | +0.1192 | −0.0177 |
| 1.0 | 25 | 0.7443 | **0.8715** | 0.8812 | 0.8634 | 3/15 | +0.1192 | −0.0080 |
| 1.0 | 50 | 0.7443 | **0.8812** | 0.8812 | 0.8634 | 0/15 | +0.1192 | −0.0177 |
| 2.0 | 25 | 0.7443 | **0.8812** | 0.8812 | 0.8634 | 0/15 | +0.1192 | −0.0177 |
| 2.0 | 50 | 0.7443 | **0.8812** | 0.8812 | 0.8634 | 0/15 | +0.1192 | −0.0177 |

(mean OOS Sharpe over the 15 (panel, family) cells; LIVE RULES v2 1.0087, SPY 0.8738)

**T1 PASS 6/6** — abstention beats argmax IS Sharpe by **+0.127 to +0.137 of OOS Sharpe**.
**T3 PASS 6/6** — mean regret against the ex-post best rung falls from **+0.1192 to −0.0080/−0.0177**;
it goes *negative* because on three of five families the anchor beats the family's own ex-post best
rung, so declining to choose is better than the best available choice.
**T2 PASS 4/6** — and this is the finding, not a win: **C_ABSTAIN never once beats doing nothing.**
It reaches the anchor's 0.8812 at exactly the four (k, STEP) cells where it **accepts nothing at
all**, and every cell where it accepts something (5 accepts → 0.8729, 3 accepts → 0.8715) lands
*below* the anchor.  The rule's entire value is the abstaining.

Per-panel do-nothing anchors (full / halves / OOS @10 bps): **U56 15.80% / 1.1537 / −19.13%,
H1 1.2067 H2 1.1203, OOS 17.32% / 1.1857 / −19.13%**; B136 16.06% / 1.0654 / −20.74%, H1 1.2815
H2 0.8968, OOS 16.19% / 1.0180 / −20.74%; SMALL 7.81% / 0.5092 / −36.51%, H1 0.6791 H2 0.3826,
OOS 6.70% / 0.4398 / −36.51%.  SPY 15.12% / 0.8844 / −33.72% (H1 0.957 / H2 0.825), OOS 15.26% /
0.8738 / −33.72%.  LIVE RULES v2 on U56 8.62% / 1.2011 / −12.05%, OOS 9.46% / 1.2769 / −12.05%.

## KEEP paths

**4a: 0 of 102 rungs, FULL and OOS.**  **4b: 51 of 102 FULL, 54 OOS, 51 BOTH** — U56 28 of 34,
B136 23 of 34, **SMALL 0 of 34** (H1, H2 and CAGR fail 34 of 34 there; DD fails 29).  On U56 the
only binding legs are H1 (3), H2 (4) and CAGR (6); the 4b drawdown cap never binds on that panel.
**Chooser picks that clear 4b FULL and OOS *and* beat the anchor out of sample: 0 of 15.**  No memo:
this run produces no KEEP candidate.

## A BUG THIS RUN FOUND IN ITSELF AND LOGGED RATHER THAN HID

The first pass matched every twin on a constant-gross ladder running to g = 1.00, but the device
engine clamps gross at the incumbent's 0.75, so CAGR(g) is **flat above 0.75** and the inverse is
multivalued: `np.interp` returned g\* = 0.99 for the anchor itself and for four other rungs, and
G3 failed at a 2.14e-02 CAGR gap.  Corrected by restricting the ladder to [0.05, 0.75] — where
CAGR(g) is strictly increasing, now asserted by **G8 (0 non-increasing steps at every cost rung)** —
and by returning **no twin** rather than a clamped one when a device's CAGR is out of range.  The
corrected run moves T2 from 1 of 6 to 4 of 6; T1 and T3 were 6 of 6 either way.  Both readings
stand in this file and in the script's history.

## Gates

G0 16.7 y.  **G1 cross-script replay of the committed 2026-09-04 U56 frozen anchor to 3.7e-05.**
G2 exactly two tuned parameters.  G3 every existing twin within **6.4e-07** of its target CAGR.
**G4 no chooser reads a row on or after 2017-01-01 — every IS Sharpe re-derived on a tape
TRUNCATED at IS_END and compared bit-for-bit, 0 of 102 differ.**  G5 max gross 0.7769 ≤ 1.
G6 all 102 rungs published.  G7 F_DEGROSS's 0.75 rung reproduces the anchor at 0.00e+00.
G8 monotonicity, 0 violations.

## Survivorship (rule 9)

U56 and B136 are CURRENT-constituent lists, SMALL a CURRENT sub-$2B screen (665 names after the
protocol-mandated drop of 54 tickers with max_1d_move ≥ 1.0) carried back to 2010, so every
absolute level is an **upper bound**.  The headline is a contrast between two SELECTION RULES
reading the same rungs on the same tape; the bias cannot manufacture that.  The 4a / 4b counts are
not immune.

## What the record should say instead

*The protocol's rule-8 chooser is not merely weak, it is expensive: argmax IS Sharpe costs −0.137
of mean OOS Sharpe against holding the frozen anchor, across 15 (panel, device-family) cells.  A
cost-aware gate recovers essentially all of that — and it recovers it by refusing to select.  At
every dial where C_ABSTAIN accepts even one book it lands below doing nothing; at every dial where
it accepts none it equals doing nothing exactly.  The reason is measurable and one-sided: a
device's in-sample margin over its own CAGR-matched de-gross twin exceeds one 10→25 bps cost step
at 6 of 102 rungs and two steps at 0 of 102.  Rule 8 should carry an explicit abstention clause —
"return the incumbent unless the pick's IS margin exceeds its own cost-step sensitivity" — not
because abstention finds better books, but because the record has nine runs of evidence that
selection at this resolution destroys capital.*

**PROTOCOL clause PROPOSED, NOT ENACTED** (rule 6 — changes go through a Sunday review).
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py untouched.
