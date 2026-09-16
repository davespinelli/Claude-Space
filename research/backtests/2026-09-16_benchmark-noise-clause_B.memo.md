# Memo — the BENCHMARK-NOISE clause (idea 1001, lane B, 2026-09-16)
Proposed as a PROTOCOL rule 4 / rule 8 reporting clause. **NOT applied** (rule 6: rules change only
at Sunday review). Nothing in `RULES.md`, `PROTOCOL.md`, `scan.py`, `bot.py` or `baseline.py` was
touched by this run.

**Exact wording, to be added to PROTOCOL.md rule 4 if the Sunday review adopts it:**

> *A 4b Sharpe leg (`book half Sharpe > SPY half Sharpe`) is published with (a) the MARGIN in
> Sharpe units, not just the two levels, (b) the comparand's own sampling SE in that half window
> (stationary block bootstrap of SPY's returns on the same days, ≥ 1,000 draws, expected block
> 21d, seed stated), and (c) the margin expressed in that SE. A pass whose weaker leg (HALFMIN)
> is under 1 SE is reported as **not certified by the leg**: over the record's 9 committed
> memo-backed 4b passes and a 36-book never-selected control ladder, **0 of 45 books clear 1 SE on
> both legs at any of five legal window starts, and 0 of 45 at 2 SE**, against SEs of 0.2877 (H1)
> and 0.3350 (H2) and a median SHELF HALFMIN of 0.2102. Any 4b claim read inside a window that
> does not run to the end of the tape — every rule-8 IS-only chooser — additionally states SPY's
> own half Sharpe in THAT window: inside `[w, 2016-12-31]` the bar moves 0.8052 → 1.8768 over the
> legal starts (ptp 1.0717) against 0.1975 on the full tape, 5.43×, and at w=2012 it costs 7 of
> those same 9 committed passes their `L_H1`.*

**Why.** Idea 971 found the `L_H1` pass rate collapsing 0.599 → 0.134 as the window start slid and
read it as the benchmark's luck. Asked of the REAL shelf it does not reproduce: 0 of 9 committed
passes flip under a window-invariant comparand at 0 or 10 bps (1 of 9 at 25 bps), the two-leg pass
rate moves 1.000 → 0.889 over five starts, Pearson is −0.6878 against a −0.70 bar, and the moving
side is the BOOK (sd 0.0659) not the comparand (0.0523) — on H2 the comparand is nearly frozen
(0.0118) and carries 0 of 9. What 971 actually dialled is the window **END**: its number reproduces
exactly (0.8052 → 1.8768) on the IS-only frame, which is the frame rule 8 mandates. So the leg is
not luck where the record reads it, and is unstable where rule 8 reads it — and in neither place is
it certified, which is what the clause says out loud.

**Evidence.** `2026-09-16_is-every-committed-4b-SHARPE-LEG-just-the-BENCHMARK-S-OWN-LUCK-in-that-window_B.py`,
45 books × 9 windows × 3 cost rungs = 1,215 census rows, 810 leg rows in SE units, gates **6 of 6**
(all 9 SHELF memo triples reproduced; fast runner ≡ `engine.backtest` at 6.94e-18; SPY 0.1510 /
0.8829 / −0.3372 vs committed 0.1513 / 0.886 / −0.3372; COUNT halves ≡ `baseline._row` at 0.00e+00;
bootstrap determinism 0.00e+00; 971's table re-read and printed on both sets). Rule 8: 24 picks,
OOS read once; GRIDONLY (uncontaminated) **OOS 4b 9 of 12, OOS 4a 0 of 12**; best clean pick
`U56-band0.03-g1.00` **OOS 12.67% / 1.2755 / −15.91%** vs SPY **15.21% / 0.8711 / −33.72%** and
RULES v2 **9.45% / 1.2762 / −12.05%** — the book ideas 971/972/997 already published, **PARK**, and
it fails 4a on drawdown. The clause's own screen is free: it shrinks the U56 pool 7 → 3 and moves
OOS Sharpe 1.1615 → 1.2755, so it is a REPORTING requirement, not an alpha filter.
**Survivorship:** current-constituent panels inflate the book side of every margin, so the
0-of-45 noise result is a LOWER bound on how uncertifiable the legs are — it works against this
memo's own hypothesis, not for it.
