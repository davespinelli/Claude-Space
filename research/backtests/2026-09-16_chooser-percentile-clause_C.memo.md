# Memo — the CHOOSER PERCENTILE clause (idea 1031, lane C, 2026-09-16)
Proposed as a PROTOCOL rule 8 reporting clause. **NOT applied** (rule 6: rules change only at
Sunday review). Nothing in `RULES.md`, `PROTOCOL.md`, `scan.py`, `bot.py` or `baseline.py` was
touched by this run, and no book was promoted.

**Exact wording, to be added to PROTOCOL.md rule 8 if the Sunday review adopts it:**

> *A claim that a rule-8 chooser beats, or loses to, a random draw from its own pool is published
> as the chooser's PERCENTILE in the random control's sequence distribution, together with that
> distribution's standard deviation and the POOL SIZE — never as a gap between two means. A mean
> gap carries no yardstick: over the record's three choosers on the 18-book GRID pool, gaps of
> 0.02–0.11 in OOS Sharpe correspond to percentiles of 0.000 and 0.800, i.e. "beaten by 2,000 of
> 2,000 draws" and "beaten by one draw in five", and the mean alone distinguishes neither. The
> pool size is stated because an N-book pool quantises every percentile to 1/N: at PROTOCOL's own
> single declared split no chooser percentile on this pool is resolved finer than 1/18 = 0.0556,
> whatever the draw count, and a percentile quoted from a discrete score (a 4b pass rate) states
> the atom mass at its own median. The MEAN-versus-MEDIAN choice of bar need not be stated: over
> 18 (chooser, cell) pairs the two agree 18 times, because a sequence score averaged over 16 or
> more split points is symmetric to within |median − mean| ≤ 0.043 of one sd with the sign
> positive in 2 of 6 cells.*

**Why.** Idea 1031 was filed on the premise that a chooser avoiding the pool's worst books beats
the pool mean without beating its median. Both halves fail. The scored object is a 16-fold
average and the CLT leaves it symmetric (headline median − mean **+0.000280** on a sd of
**0.0212**, 1.3% of one sd and a coin flip in sign), so the bars never disagree — **0 flips of
18**. And the skew the premise reasoned from exists one level down with the OPPOSITE sign: the
per-end 18-book distribution has median − mean **−0.0142** at the headline and is negative in 4
of 6 cells, i.e. the pool is RIGHT-skewed and the MEAN is the harder bar. What the percentile
adds is not a verdict but a magnitude, and that is worth a clause on its own.

**Evidence.** `2026-09-16_does-IS_CAGR-s-EDGE-survive-a-MEDIAN-rather-than-MEAN-coin-flip_C.py`,
a 3,456-row ladder × 2,000 random sequences per (panel, cost, end grid), 9 dial points
(statistic × end grid) all reported and none selected. Gates 8 of 11, including a bit-level
cross-run of 1023's committed chooser means (**3.75e-07**), SPY's committed OOS triple
(15.21% / 0.8711 / −33.72%), 1013's four published picks (4 of 4, 4.59e-04), and G7 — the
sampler's MC mean against the EXACT closed-form pool mean, 6 of 6. The two gate failures (G8,
G8b) are diagnosed to the digit by G8c/G8d as atom mass from the 18-book quantisation and the
discrete 4b score, and are the reason the clause names the pool size. Hypotheses 6 of 8;
H_CAGRALL (5 of 6) and H_DIAL fail and are reported.

**Rule 8.** 18 picks made on 2009–2016 alone, 2017–2026 read once: **OOS 4b 18 of 18, OOS 4a 0 of
18**; best `U56 IS_CAGR → U56-qroll-q0.17-w1008-d0.50` at OOS **15.60% / 1.293 / −15.59%** (10
bps) against SPY OOS 15.21% / 0.8711 / −33.72% and RULES v2 live 8.62% / 1.2007 / −12.05%. No
book KEEP is claimed: these are 1013's and 1023's already-committed objects, a uniform draw from
the same pool clears 4b at these cells **0.333–0.604** of the time (0.444 at the headline), the
best pick sits at the **58.3rd** percentile of its own pool, and all 18 fail 4a on drawdown.

**Survivorship (rule 9).** Current-constituent panels inflate every level here. The measured
object is a RANK inside a distribution drawn from the same pool, where the bias is common to
chooser and control; where it does not cancel it flatters the coin flip, so every chooser
percentile in this memo is a LOWER bound — the bias works against the clause's own headline, not
for it.
