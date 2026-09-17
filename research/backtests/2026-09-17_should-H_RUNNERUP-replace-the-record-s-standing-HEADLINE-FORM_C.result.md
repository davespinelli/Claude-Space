# Idea 1227 (lane C, 2026-09-17) — should H_RUNNERUP replace the record's standing HEADLINE FORM?

**VERDICT: KILL (capital). ANSWERED = NOT ON PRICE — NO HEADLINE FORM BEATS HOLDING.** Given
dozens of picks instead of 1223's handful (193 per grid point against 42), **0 of 18** (form,
window) cells at the record's own comparison set beat CH_ANCHOR with a fold-clustered |t| ≥ 2 and
both matched nulls; pooled over both sets and both cadences, **36 of 96 cells post a naive
positive gain, 0 survive |t| ≥ 2, and exactly 1 clears both nulls against the 4.8 chance
predicts.** H_RUNNERUP's own best window is +0.0126 at t +1.86, p_PERM 0.207. 17 of 17 gates
pass. Runtime 16s, offline, deterministic, **no new book.**

Script: `2026-09-17_should-H_RUNNERUP-replace-the-record-s-standing-HEADLINE-FORM_C.py`
Dials (2, PROTOCOL rule 4): **HEADLINE FORM** {H_RUNNERUP, H_NARROWEST, H_ANY} + controls
{CH_RAW, CH_ANCHOR} × **IS WINDOW** L ∈ {252, 504, 756, 1260, 2520, EXPANDING}. 30 cells, each
published at 2 comparison sets × 2 fold cadences = **120 rows, every one in `.deltas.csv`.**
Not dials, reported at every value, never selected on: PANEL {U56, B136, SMALL}; SET {ALL4, NG}
(verdict read off **ALL4**, the record's own); CADENCE {QUARTER primary, YEAR for continuity).

---

## 1. What 1223 left open, and what this run does about it

1223 found H_RUNNERUP is the only reading of "the widest dial" a degenerate comparison-set member
cannot manufacture (CREATED 0 headline calls at every δ ≤ 0.30, against 40 of 42 for H_NARROWEST
and 37 of 42 for H_ANY) — a robustness argument for adopting it as the standing form. It also
priced it at **−0.0183 of mean OOS Sharpe on 42 picks, |t| 1.16**, which decides nothing: a
chooser that moves at 0.048 makes **two** real decisions in 42 folds.

This run makes the folds QUARTERLY (67/67/59 per panel, 2010Q1-2026Q3, 193 (panel, fold) cells per grid point)
and makes the IS window a dial, so each form is walked against the anchor dozens of times. The
bar is frozen at B_IID95, the record's calibrated conditional two-sided band, seed 12141214, so
the bands are literally 1214's and 1223's numbers (G8 replicates 1223's committed move rates and
mean OOS Sharpes at (YEAR, EXPAND) to **3.8e-04**).

## 2. A BOOKKEEPING ERROR IN THE MOVE RATE, FOUND AND FIXED HERE (G9, G10, G11)

**The anchor is one book under four names.** N=20, H=126, GROSS=0.75 and CADENCE=W are the
*same return series*, bit for bit, in all three panels (G9 = 0.0). 1223 — and this run's first
pass — counted a pick landing on any of them as a MOVE. It is not one. Re-defining a move **by
value** rather than by key drops the pooled move rate from **0.3817 to 0.3537** (G11):
CH_RAW at ALL4/QUARTER/L252 reads 0.860, not 0.969; H_NARROWEST 0.751, not 0.808. **No delta and
no Sharpe changes** (the books are identical), but the null's destination pool does: 4 of 22
draws were no-ops. Both definitions are carried in `.picks.csv` (`moved`, `moved_key`); every
number below uses the value definition, and G8 checks 1223's numbers on 1223's own definition.

## 3. ALL 18 GRID POINTS AT THE RECORD'S OWN SET (ALL4, QUARTER, 193 picks each)

| window | H_RUNNERUP Δ (t) | H_NARROWEST Δ (t) | H_ANY Δ (t) | CH_RAW Δ (t) |
|---|---|---|---|---|
| L252 | **+0.0126 (+1.86)** | −0.0383 (−0.62) | −0.0383 (−0.62) | −0.0211 (−0.33) |
| L504 | +0.0101 (+1.16) | −0.0087 (−0.14) | −0.0087 (−0.14) | +0.0195 (+0.32) |
| L756 | −0.0082 (−0.80) | +0.0406 (+0.64) | +0.0406 (+0.64) | +0.0137 (+0.22) |
| L1260 | +0.0012 (+0.70) | +0.0116 (+0.20) | +0.0116 (+0.20) | −0.0121 (−0.20) |
| L2520 | −0.0074 (−1.04) | −0.0290 (−0.49) | −0.0290 (−0.49) | −0.0631 (−1.11) |
| EXPAND | −0.0115 (−1.31) | −0.0602 (−1.02) | −0.0602 (−1.02) | −0.0746 (−1.36) |
| **mean over the 6** | **−0.0005** | −0.0140 | −0.0140 | −0.0229 |
| **move rate** | **0.022** | 0.770 | 0.770 | 0.897 |
| **worst cell** | **−0.0115** | −0.0602 | −0.0602 | −0.0746 |

CH_ANCHOR (do nothing) mean OOS Sharpe **1.2875** over the same 193 picks. Δ is paired per
(panel, fold); SE clusters on folds, which tile the tape without overlap. **The sign of every
form flips with the window**, which is the whole finding: nothing here is a property of the form.

## 4. THE NULLS — 2,000 reps each, pre-declared, and they are what settles it

NL_COUNT (move on m random folds, destinations drawn from the 18 non-anchor books) and NL_PERM
(the chooser's OWN destinations, re-dealt at random times) are reported at every cell in
`.deltas.csv`. Pooled over both sets and both cadences, **96 non-anchor cells**:

| leg | cells passing |
|---|---|
| naive Δ > 0 | **36 of 96** |
| Δ > 0 and |t| ≥ 2 | **0** |
| Δ > 0 and p_NL_COUNT ≤ 0.05 | **1** |
| Δ > 0 and p_NL_PERM ≤ 0.05 | **1** |
| all three | **0** |

The single cell clearing both nulls is **YEAR / NG / L1260 / H_NARROWEST**: Δ +0.0196, t +1.49,
p_COUNT 0.006, p_PERM 0.015 — on the non-record set, the non-primary cadence, 49 picks, failing
the t leg, and **1 of 96 against the 4.8 that 0.05 predicts by chance.** It is named here rather
than promoted. 1210/1221/1227-cloud's finding arrives again: *naive "gain > 0" is worth nothing
at this sample size, and a count-matched bar removes almost all of it.*

## 5. THE CAPITAL LEG — rule 8, both KEEP paths, nothing promoted

**Rung books (66 = 22 × 3 panels, QUARTER fold span):** 4a **0**; 4b full 17; 4b OOS 16; BOTH
**16**, and all 16 are the U56 anchor family plus B136's GROSS rungs — under 1194's gross-free
key, **two** books, both already in the record. **Stitched chooser curves (360):** 4a **0**; 4b
full 84, 4b OOS 82, BOTH 82, **every one of them on U56**, collapsing to 28 distinct
(CAGR, Sharpe, MaxDD) triples that are near-anchor by construction.

**RULE 8** (the two dials chosen on the pre-2017 folds ONLY, 2017-2026 read once, set frozen at
ALL4):

| panel | IS-chosen (window, form) | OOS CAGR / Sharpe / MaxDD | anchor OOS | 4a | 4b |
|---|---|---|---|---|---|
| U56 | L504 / **H_RUNNERUP** | 17.46% / **1.1885** / −19.13% | 17.16% / 1.1759 / −19.13% | F | **T** |
| B136 | L252 / **H_RUNNERUP** | 16.89% / **1.0518** / −20.74% | 16.29% / 1.0240 / −20.74% | F | F |
| SMALL | L504 / CH_RAW | 5.25% / 0.3564 / −37.41% | 7.09% / 0.4534 / −35.81% | F | F |

Benchmarks over the same OOS span: U56 SPY 15.15% / 0.8686 / −33.72%, LIVE (RULES v2) 9.42% /
1.2717 / −12.05%; B136 SPY 15.33% / 0.8769, LIVE 7.88% / 1.1061; SMALL SPY 15.33% / 0.8769,
LIVE 4.47% / 0.6518. At YEAR folds the IS choice lands on H_RUNNERUP/L252 for U56 — which makes
**zero** OOS moves, i.e. it *is* the anchor — and on CH_RAW for the other two, both of which lose
to the anchor.

**The two panels where the rule-8 pick beats holding are the two where it makes 1 and 3 moves in
its 39 OOS quarters.** That is the same two-decision problem 1223 had, arriving through a different
door: H_RUNNERUP is so reluctant that a walk-forward gain on it is a statement about one or three
quarters, not about a rule. **NOT PROMOTED, NO MEMO, NO RULES CHANGE. This run produces no new
book.**

## 6. What the answer actually is

**On price: no — nothing should replace holding, H_RUNNERUP included.** But the question the
queue asked was whether H_RUNNERUP should be the record's standing *headline form*, and the two
legs now point the same way for the first time: 1223 showed it is the only form a degenerate
comparison-set member cannot manufacture, and this run shows that **adopting it costs
essentially nothing** — mean **−0.0005** of OOS Sharpe over 6 windows against −0.0140 for
H_NARROWEST/H_ANY and −0.0229 for the record's raw habit, and a worst case of −0.0115 against
−0.0746. It is the cheapest form *because* it is the most reluctant (move rate 0.022 against
0.770 and 0.897), and reluctance is exactly what every chooser result in this record has been
paying for. **That is a reporting recommendation for the Sunday review, not a capital one, and
it is filed as such: no RULES wording is proposed here.**

## 7. Survivorship (rule 9)

B136 and SMALL are CURRENT constituents. SMALL is the sub-$2B screen, 664 investable of 715 after
dropping every ticker with `max_1d_move >= 1.0`, and starts 2010 (59 quarterly folds against 67).
U56 is the committed cache. SPY is a benchmark column in every panel, never an eligible name.

## 8. Gates (17 of 17)

G0 MC d2(k) == Hartley 9.66e-04 · G1 R_k/d2(k) unbiased 8.56e-04 · G2 fast runner ==
engine.backtest 2.78e-17 · G3 live U56 MaxDD −12.05% == committed · **G9 the anchor is one book
under four names 0.0** · **G10 the anchor-equivalent key set is exactly {N=20, H=126, GROSS=0.75,
CADENCE=W}** · G4 QUARTER and YEAR folds tile all three panels with no overlap and no gap (6
gates, 0) · G5 CH_ANCHOR move rate 0 · **G11 the value-based move rate never exceeds the
key-based one (0.0280 of cells differ)** · G8 (YEAR, EXPAND) replicates 1223's 8 committed
numbers to 3.81e-04 · G7 stitched Sharpe from per-fold aggregates == direct 2.22e-16 · G6 each
stitched curve's length == the sum of its folds' 0.

## 9. What this leaves for the queue

Three follow-ups, all price-only: (a) the stitched listing shows U56 / NG / L252 / H_ANY at OOS
Sharpe 1.2377 against the anchor's 1.1759 — a *curve* nobody chose, on the non-record set, whose
own pooled fold delta is −0.0197; ask whether the record's chooser results are being read off
listings like this one. (b) Every form's sign flips with the IS window on 193 picks; measure the
window length at which a form's own delta separates from its NL_PERM band, if any does. (c)
Census how many committed move rates in the record count a pick onto an anchor-equivalent key as
a move (§2 says 1223 does; it is unlikely to be alone).
