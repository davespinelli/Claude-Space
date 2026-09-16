# Memo — the CHOOSER POOL STAMP clause (idea 1033, cloud lane, 2026-09-16)
Proposed as a PROTOCOL rule 8 reporting clause. **NOT applied** (rule 6: rules change only at
Sunday review). Nothing in `RULES.md`, `PROTOCOL.md`, `scan.py`, `bot.py` or `baseline.py` was
touched by this run, and no book was promoted.

**Exact wording, to be added to PROTOCOL.md rule 8 if the Sunday review adopts it:**

> *A rule-8 chooser percentile is a statement about the MENU the chooser was offered, not about
> the chooser, and is published with the full book list of its pool. Percentiles computed on
> different pools are never compared, differenced or pooled, even when one pool contains the
> other: on this tape `IS_CAGR` sits at the **0.801** percentile of the record's 18-book GRID
> pool and at **0.014** of the 80-book ladder that CONTAINS those 18 books unchanged, because a
> wider menu offers it books that look better in 2009–2016 and do worse in 2017–2026. Where a
> percentile is used to certify a chooser, the count that gives it power is the number of SPLIT
> ENDS it is averaged over, not the number of books in the pool: the percentile's RESOLUTION is
> 1/N at a single end and is already finer than a 5% bar at N ≥ 10, so no pool size makes a
> single-split percentile decisive, while moving from one end to 32 moves the same chooser's
> one-sided p by 0.255 against 0.055 for a 4× to 8× change of pool size.*

**Why.** Idea 1033 was filed on the premise that 1031's percentiles are too COARSE — quantised
to 1/18 — and that a bigger pool would resolve `IS_CAGR`'s 0.800 away from a coin flip. The
arithmetic half of that is right and the conclusion is wrong. Quantisation is exactly 1/N
(**H_QUANT PASS**, max |step − 1/N| = 0.00e+00), but 0.5/N ≤ 0.05 needs only **N ≥ 10**, so the
record's own 18-book pool already resolves to **0.0278**, finer than the bar it is being asked to
clear. **No pool on the ladder separates `IS_CAGR` from a coin flip at PROTOCOL's declared split**
(**H_RESOLVE FAIL**: p = 0.396 / 0.571 / 0.955 / 0.928 / 0.596 / 0.603 at N = 18 / 24 / 10 / 20 /
40 / 80), while every N ≥ 20 pool could have (**H_NOTRES PASS**). 0.800 means "one draw in five
beats it" at any N; that is a RANK, and no amount of resolution fixes a rank.

**What the run found instead.** The percentile is not size-sensitive — along the NESTED ladder it
barely moves (**H_MOVE FAIL**, WIDE10 0.000 → WIDE80 0.014) and the coin flip's own level does
not decay (**H_FLOOR FAIL**, 1.2133 → 1.2097 → 1.1988 → 1.2095, total **−0.0038**, so 1030's
floor mechanism is absent on a composition-matched ladder). It is MENU-sensitive: across the six
named pools `IS_CAGR` spans **0.000–0.801** (range 0.801) against 0.083 and 0.111 for the other
two choosers, the chooser ordering is not stable (**H_ORDER FAIL**, three distinct orderings), and
the mechanism is visible in the picks — GRID18 buys `U56-qroll-q0.17-w1008-d0.50` (OOS Sharpe
1.293) and the widened menus buy the depth-0.25 variants of the same family (1.160 / 1.157 /
1.205). Adding legal books made the chooser WORSE, which is the opposite of the queue's premise
and the reason the clause forbids cross-pool comparison rather than prescribing a pool size.

**Evidence.** `2026-09-16_is-a-CHOOSER-PERCENTILE-a-POOL-SIZE-artefact_cloud.py`, a 16,128-row
ladder (168 books × 3 rungs × 32 ends) × 2,000 random sequences per (panel, cost, pool, end
grid), **24 dial points (6 pools × 4 end grids) all reported at every panel × cost and none
selected**. Gates **9 of 11**: G1 fast runner vs `engine.backtest` (6.9e-18 / 1.7e-16), G3 SPY's
committed OOS triple (15.21% / 0.8711 / −33.72%, 1.7e-04), G4 1013's four published picks (4 of
4, 4.6e-04), G5 bit-level determinism (0.0), G6 IS purity (96 of 96), G7 the sampler against the
EXACT closed-form pool mean (144 of 144), G9 nesting. The one failure, G8 (126 of 144), is the
quantisation itself and is diagnosed to the digit: it is **108 of 108 on the K > 1 cells (G8b)**
and fails only where the random distribution is N point masses, with median atom mass
**0.0095–0.1080** (G8c). Hypotheses **4 of 8**; the four failures are the findings and are
reported as loudly as the passes.

**Rule 8.** 108 picks made on 2009–2016 alone, 2017–2026 read once: **OOS 4b 99 of 108, OOS 4a 0
of 108**. Best pick `U56 / GRID18 / IS_CAGR → U56-qroll-q0.17-w1008-d0.50` at 10 bps: full
14.05% / 1.170 / −15.59% (H1 1.132 / H2 1.206), **OOS 15.60% / 1.293 / −15.59%**, against SPY OOS
15.21% / 0.8711 / −33.72% (H1 0.959 / H2 0.821) and RULES v2 live 8.62% / 1.2007 / −12.05% (H1
1.232 / H2 1.176). The SAME chooser on the 80-book menu takes `-d0.25` at OOS 15.34% / 1.205 /
−18.23%, and on WIDE10/WIDE20 takes books that FAIL 4b on the drawdown cap. **No book KEEP is
claimed**: these are 1013's and 1023's already-committed objects, every pick fails 4a on
drawdown, and the 4b pass rate is a property of the menu (1.000 on GRID18/GRIDSHELF, 0.778 on
WIDE10) rather than of the chooser.

**Survivorship (rule 9).** U56 and B136 are current-constituent panels, so every CAGR and
drawdown LEVEL above is optimistic and every 4b count an upper bound. The measured object is a
RANK inside a distribution drawn from the same pool over the same tape, where the bias is common
to the chooser and to every control draw; where it does not cancel it flatters the coin flip, so
each chooser percentile here is a LOWER bound and the clause's headline collapse (0.801 → 0.014)
is, if anything, understated.
