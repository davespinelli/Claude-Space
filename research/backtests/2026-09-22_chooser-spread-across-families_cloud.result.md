# Idea 2109 — is the CHOOSER SPREAD a GENERAL property of the record's GRIDS? (cloud, 2026-09-22)

**ANSWERED: YES, and the record's default chooser is one of the worse ones.** Six families, six
fresh 2-D grids (BAND / MOM / MADIST / VOLTGT / DRIFT / STOP), 107 cells per (panel x cadence),
U56 + B136, weekly + monthly, costs 0/10/25/50 bps derived exactly from the cost-0 run
(gate G3, max |diff| 0.000e+00) = **1,712 published grid rows**; 96 grid instances x the seven
legal IS-only choosers of idea 2087 = **672 published picks**. Rule 8 throughout: 2009–2016
chooses, 2017–2026 read exactly once. Gates G1 (no leverage, max gross 1.0000), G2 (IS/OOS
disjoint), G3 all PASS.

## What the run found

1. **V1 YES — the spread is a property of GRIDS, not of the turnover-budget family.** Per-family
   best/worst 4b FULL+OOS reach ratio (Laplace-smoothed): MADIST **23x**, VOLTGT **23x**,
   MOM **15x**, DRIFT **15x**, BAND **9x**, STOP **1x** (degenerate: 0 of 16 for all seven
   choosers). **Median 15.00x** against the pre-stated bar of 10 and against 2087's committed
   157x on one family.
2. **V2 YES — 43 of 96 instances (44.8%) have the seven legal rules DISAGREEING on the 4b
   verdict.** Median OOS-Sharpe spread across the seven picks on one and the same grid: **0.1246**
   (mean 0.1550, max 0.5120). MOM is the widest family (median 0.2783), DRIFT the narrowest
   (0.0760). A single-chooser 4b verdict in this record is a coin-flip away from its opposite on
   nearly half the grids.
3. **V3 YES — but the ranking it exposes is not the record's default.** Mean pairwise Spearman
   rho of the per-chooser reach vectors across the six families **+0.684** (min +0.337, max
   +0.957): a dominant chooser does exist. Pooled over all 96 instances it is **IS_MINMARG
   0.385 / IS_LEGS 0.323 / IS_SHARPE 0.146 / IS_CAGRSLACK 0.073 / IS_CALMAR 0.052 / IS_DD 0.000
   / CELL_ALPHA 0.000.** The record's habitual chooser, **IS_SHARPE, reaches 2.6x fewer 4b cells
   than IS_MINMARG** — it systematically buys the gross-1.00 corner and dies on the DD leg.
4. **V4 YES — 29 of 168 protocol-rung picks clear 4b FULL+OOS**, against a whole-grid base rate
   of 0.1682 at 10 bps (0.2009 / 0.1682 / 0.1145 / 0.0537 at 0 / 10 / 25 / 50 bps). Only **1 of
   168** clears 4a FULL. Binding leg over all failing cells at 10 bps: **L5_CAGR 183, L4_DD 129**,
   every Sharpe-leg combination far behind — the same two level legs that bind everywhere else in
   this record.
5. **The one KEEP-candidate worth capital** (memo beside this file): **U56/B136 MONTHLY MADIST
   top-5 at gross 0.50**, reached under rule 8 by the two best choosers (IS_LEGS, IS_MINMARG) and
   clearing 4b FULL+OOS on **both panels at all four cost rungs**. Idea 921's independent run the
   same day prices its five-leg cost closing price at **76.9 bps (U56) / 68.7 bps (B136)**.
6. **A by-product that is the thesis in miniature:** on the U56 weekly BAND ladder the three
   choosers that reach 4b pick three DIFFERENT band rungs — IS_LEGS 0.12, IS_MINMARG 0.08, and
   idea 2101 (this morning, same lane) 0.10 — all clearing 4b OOS. The band rung the record keeps
   re-deriving is not resolvable by the choice of legal chooser.

## What it does NOT show

- It does not say which chooser is RIGHT. IS_MINMARG's pooled lead is measured on the same
  grids it is being ranked on; a fresh family could reorder it (the min pairwise rho is +0.337).
- STOP contributes a 1x ratio because the family reaches 4b nowhere — a degenerate, not a
  counter-example, and it pulls the median DOWN, not up.
- Survivorship (rule 9): U56/B136 are current-constituent lists. The chooser CONTRAST is
  same-grid/same-tape and first-order immune; the 4b pass COUNTS are optimistic.

## Consequence for the record

Every committed "N of M arms clear 4b under a legal IS-only chooser" in this record was computed
with ONE chooser and published with no spread beside it. On 44.8% of grids a different legal rule
would have published the opposite verdict. **A rule-8 verdict should carry its chooser's name and,
where the grid allows it, the reach spread across the legal set** — proposed for a Sunday review
under rule 6; nothing in RULES.md, PROTOCOL.md, scan.py, bot.py or baseline.py was modified here.
