# 1260 (lane B, 2026-09-18) — is the record's DECISIVENESS BAR on the WRONG SIDE of the OBSERVED/BAR line?

**ANSWERED YES ON THE STATISTIC AND NO ON THE MONEY. VERDICT: KILL (capital), NO NEW BOOK, NO RULES
OR PROTOCOL CHANGE.** 14 of 16 gates (the two failures are findings about the record, below), 64s,
offline, deterministic.

## The question, and the two dials
1252 priced the incumbent decisiveness bar (P_boot >= 0.90) on 72 real book choices and found it
licenses the *worse* half of them (mean OOS Sharpe delta -0.0061 given fire vs +0.0133 given
refusal). 1242 separately showed every OBSERVED-side output is exactly L-free. So the record has
been publishing decisiveness on the draw side and never priced the observed side at all.

Dial 1 = SCORE {**S_OBS_RATIO** = IS margin / rung spread (the queue's own statistic),
**S_OBS_MARGIN** = IS margin scaled by the anchor's own stat | **S_PBOOT_TOP**,
**S_PBOOT_MARGIN**}. Dial 2 = BAR QUANTILE {0.50, 0.60, 0.70, 0.80, 0.90, 0.95}. **24 cells, every
one published.** Not dials: panel (3), anchor (2, 1101's), ladder (4), chooser (3) = the same 72
decisions at every cell; block length frozen at the record's L = 63 with its sensitivity reported
as a control. 10 bps, t+1, warm-up 260, picks on warm-up..2016-12-31, **2017-2026 read once**.

## The answer on the statistic (outcome (B), not (A))
`d` = OOS Sharpe(pick) − OOS Sharpe(anchor), paired per decision; mean over all 72 **+0.0095**
(1252 committed +0.0090). The incumbent's own absolute bar replays: n_fire 17, **d|fire -0.0060 vs
d|refuse +0.0142, diff -0.0202** (1252: -0.0061 / +0.0133 / -0.0194).

- **Licensed-minus-refused > 0 at 8 of 12 OBSERVED-side cells against 1 of 12 BAR-side cells.**
- **Mean licensed-minus-refused: OBS +0.0401 vs BAR -0.0142.** H_CLASS SUPPORTED.
- Best cell **S_OBS_MARGIN @ q0.95 +0.1839** (welch +8.34); **S_OBS_RATIO @ q0.90 +0.1404**
  (welch +5.08). Rank corr of each score against `d`: +0.0942 / -0.1526 / +0.0079 / -0.0472.

## Why that is not money (H_CAPITAL_R8 REFUTED — the reading that governs)
- **The positive cells are two to five distinct book choices, not four to eight.** Two choosers
  landing on the same rung is ONE choice: `n_distinct_fire` is published beside `n_fire` at every
  cell. S_OBS_MARGIN@q0.95 fires 4 times = **2 distinct choices, both the H ladder on SMALL663** —
  the panel that fails all five 4b legs at 54 of 54. S_OBS_RATIO@q0.90 fires 8 = 5 distinct, and
  is the only positive cell spanning all three panels and more than one ladder.
- **RULE 8 ON THE DIAL ITSELF KILLS IT.** (score, quantile) chosen on an inner IS split
  (pick on warm-up..2012, scored 2013-2016), outer read once: **inner/outer licensed-minus-refused
  rank corr -0.4292** — choosing the bar in sample ANTI-selects. The inner argmax is
  **S_OBS_MARGIN @ q0.90**, whose outer licensed-minus-refused is **+0.0297** (not +0.1839) and
  whose capital value is **d_sel +0.0040** of mean OOS Sharpe while **costing a 4b pass (23 vs the
  do-nothing 24)**. 0 of the 2 cells that beat do-nothing without costing a 4b pass are reachable
  forward. Mean d_sel over all 24 cells +0.0026.
- **Gating remains a destruction operator.** Realised 4b BOTH over the 72: do-nothing **24**,
  always-act **6**, incumbent P_boot>=0.90 **19**, best matched observed-side selector **20**.
  Mean OOS Sharpe: do-nothing 0.7922, always-act 0.8017, SEL_PBOOT_0.90 0.7908 (-0.0014),
  SEL_S_OBS_RATIO matched 0.8044 (+0.0121).

## Bycatch 1 — the OBSERVED/BAR line is NOT the mechanism, against this run's own framing
At a QUANTILE bar the draw side is L-stable too: licensed-minus-refused at q0.90 moves
**0.0000** across L = 21/63/252 on both bar-side scores (the bar re-floats to 1.0000 at every L and
the fire set barely moves). 1242's L-fragility is a property of an ABSOLUTE bar on a draw
statistic, not of the class. The observed side's advantage has to stand on its delta alone.

## Bycatch 2 — two committed runs disagree on the level of the SAME 72 decisions (G9 FAIL / G9b PASS)
1252 publishes do-nothing mean OOS Sharpe **0.8268**; 1246 publishes **0.7922** over the same 72.
This run reads **0.7922 / 0.8017**, i.e. reproduces 1246 to 1e-4 and 1252's licensed-minus-refused
pair to 1e-3. **The deltas agree across all three runs; the level does not.** G7 also fails: 1252's
rank corr(P_pick, d) -0.1423 reads +0.0079 here — both inside an n=72 rank correlation's own noise,
which is why this run adjudicates on the difference and not on the correlation. Published, not
toleranced.

## Capital (the 162 rung books, the same construction)
**4a 0 of 162** (live RULES v2's -12.05% MaxDD against growth books — rule 4's own reason for 4b).
**4b full 26, 4b OOS 30, BOTH 25** collapsing to **19 distinct books, U56 20 / B136 5 / SMALL663 0**,
and every one is prior art: the 2026-09-04 anchor (15.62% / 1.1423 / -19.13%, OOS 17.04% / 1.1688),
its gross/H/ladder clones, U56 A N=12 (17.69% / 1.1686 / -20.17%, OOS 1.1748 — still the 0.06pp
DD-cap margin 1259 has open) and U56 B N=20 (11.07% / 1.1387 / -18.01%, OOS 1.1827). Binding 4b leg
remains the DD cap (fails at 106 of 162). Benchmarks: U56 SPY 15.13% / 0.8848 / -33.72%
(halves 0.9598/0.8234), OOS 15.28% / 0.8745; U56 live v2 @10 bps 8.62% / 1.2017 / -12.05%, OOS 1.2778.

## Hypotheses and gates
H_SIGN SUPPORTED, H_CLASS SUPPORTED, H_LFREE SUPPORTED, H_CAPITAL SUPPORTED (best of 24),
**H_CAPITAL_R8 REFUTED**, **H_R8_TRANSFERS REFUTED**. Gates 14 of 16: G1 incumbent triple 2.60e-03
(tape restated daily), G2 live DD 4.95e-05, G3 SPY OOS 3.22e-03, G4/G4b window partitions exact,
G5 fast runner == engine.backtest 1.39e-17, G6 mean d vs 1252 4.52e-04, **G7 FAIL** (above),
G8 incumbent bar's negative sign reproduced, **G9 FAIL / G9b PASS 9.98e-05** (above), G10 rule-8
choice made on the inner split only, G11 observed-side L-swing exactly 0, G12/G13 determinism 0,
G14 SPY eligible on SMALL 0 days.

## What the record should take from it
A decisiveness bar belongs on the OBSERVED side — the direction is consistent and the sign flips
against the incumbent — but **no bar in either class is worth capital on this tape**, because the
bar's own dial does not transfer (inner/outer rank corr -0.4292) and gating still destroys 4b
passes. Recommended for the Sunday review as a PUBLISHING note only, not enacted here (rule 6):
report a pick's observed margin/rung-spread ratio *beside* any P_boot, and quote both with their
`n_distinct` rather than their `n_fire`.

## Survivorship (rule 9)
U56 and B136 are current-constituent lists; SMALL663 is a current sub-$2B screen (52 of 715 dropped
on max_1d_move >= 1.0). Every 4b count above is an upper bound. The headline is a comparison of two
bar classes over the SAME 72 decisions on the SAME panels, so a level bias moves both sides
together; it does bear on one number — the best observed-side cell is 2 SMALL663/H choices, and
SMALL663 is the most survivorship-flattered of the three panels, which makes that cell weaker than
it reads, not stronger.

## Files
`2026-09-18_is-the-record-s-DECISIVENESS-BAR-ON-THE-WRONG-SIDE-of-the-OBSERVED-BAR-line_B.py`
plus `.grid.csv` (24), `.decisions.csv` (72), `.books.csv` (162), `.walkforward.csv` (24),
`.selectors.csv` (7), `.control.csv` (12), `.gates.csv` (16), `.console.txt`.
