# Idea 1031 (lane C, 2026-09-16) — does IS_CAGR's EDGE survive a MEDIAN rather than a MEAN coin flip?

**ANSWERED = YES, IT SURVIVES — AND THE QUEUE'S MECHANISM IS BACKWARDS. KILL the mean-vs-median
distinction: the two bars return the SAME verdict in **0 of 18** (chooser, cell) pairs, because
a sequence mean over 16 ends is symmetric to within Monte-Carlo noise (|median − mean| ≤ 0.043
of one sd, sign positive in 2 of 6 cells). KILL the queue's stated MECHANISM: the underlying
book distribution is skewed the OTHER way — median − mean = **−0.0142** at the headline and
negative in 4 of 6 cells — so a chooser that merely avoids the pool's worst books lands BELOW
the mean, and the MEAN is the harder bar, not the easier one. KEEP a PROTOCOL rule 8 CHOOSER
PERCENTILE clause (proposed, not applied — rule 6), because what the percentile adds is not a
different verdict but the MAGNITUDE 1023 could not report: `IS_CAGR` sits at the **80.0th**
percentile of its own coin flip — **1 draw in 5 beats the record's best rule-8 chooser** — while
`IS_SHARPE` and `IS_LEGS` sit at **0.000**, beaten by 2,000 of 2,000. Gates 8 of 11 and both
failures are diagnosed to the digit; hypotheses 6 of 8 and every failure is reported as loudly
as a pass. Nothing promoted, no RULES change; `RULES.md`, `PROTOCOL.md`, `scan.py`, `bot.py` and
`baseline.py` untouched.**

Script: `2026-09-16_does-IS_CAGR-s-EDGE-survive-a-MEDIAN-rather-than-MEAN-coin-flip_C.py`

## What was asked

Idea 1023 scored RANDOM by the mean of 400 sequences, which is the pool MEAN. The queue's worry:
a chooser that avoids the pool's worst books beats that mean without beating the median, so
1023's "`IS_CAGR` beats the coin flip in 5 of 6 cells" may be an artefact of the bar. Re-score
all three choosers as PERCENTILES of the random control's own sequence distribution and report
which clear the 50th. Max 2 params (percentile statistic, end grid).

## The grid

1023's own pool and cells, re-read: the **36** never-memo-selected GRID ladder books (18 U56 /
18 B136) × 3 cost rungs × the **32**-end union of the three end grids = a **3,456**-row ladder;
**2,000** random chooser SEQUENCES per (panel, cost, end grid) — 5× 1023's 400, so a percentile
resolves to 0.0005 and its binomial SE at p = 0.5 is 0.0112. Two tuned axes only, the queue
line's own — PERCENTILE STATISTIC {`MEAN_SH`, `MED_SH`, `RATE4B`} × END GRID {`Q16`, `Q32`,
`REC1`} — **all 9 points reported at every panel × cost, none selected.** Cost (0/10/25 bps) and
panel are reported CONTROLS, not dials. Headline = 1023's own cell: U56 / 10 bps / `MEAN_SH` /
`Q16`.

`Q32`'s caveat was declared before the numbers: its earliest ends leave an IS window of barely
two years. Legal under rule 8's letter, thin in substance, a sensitivity axis and never a
headline.

## The run reproduces 1023 bit-for-bit before re-scoring it

**H_1023 PASS.** In 1023's headline cell this run reads `IS_SHARPE` and `IS_LEGS` at
**1.155696** and `IS_CAGR` at **1.261757** — 1023's committed values to **3.75e-07** and
**2.69e-07**. RANDOM is not re-sampled but solved: the exact pool mean is a closed form (the mean
of the end × book OOS-Sharpe matrix) and reads **1.243265** against 1023's Monte-Carlo
**1.243317**, |d| **5.21e-05** against 3 MC SE of 3.13e-03. Every number below is a re-reading
of the same ladder, not a different experiment.

Getting there cost one construction correction, stated because it moves published numbers: an
initial pass truncated the two panels to a common calendar (the B136 weekly cache runs 2 sessions
behind U56) and that alone moved SPY's OOS CAGR from the record's 15.21% to 15.33% and broke
G3/G4. 1023 and 1013 let each panel keep its own calendar and nothing here splices them, so this
run does the same. On that construction **G3 reads SPY OOS 15.2102% / 0.8711 / −33.7173%** —
the record's committed comparand — and **G4 reproduces all four of 1013's published declared-split
picks** at max |d| 4.59e-04.

## The answer: the two bars never disagree

**H_FLIP PASS — 0 flips of 18.** 1023's bar (chooser mean > RANDOM's pool mean) and this run's
bar (chooser score above the MEDIAN of the random sequence distribution) return the identical
verdict in every one of the 18 (chooser, panel × cost) pairs on the headline grid.

| panel / cost | `IS_SHARPE` pct | `IS_LEGS` pct | `IS_CAGR` pct |
|---|---|---|---|
| U56 / 0 | 0.000 | 0.000 | **0.947** |
| U56 / **10** | **0.000** | **0.000** | **0.800** |
| U56 / 25 | 0.059 | 0.042 | 0.317 |
| B136 / 0 | 0.051 | 0.000 | **0.990** |
| B136 / 10 | 0.003 | 0.003 | **0.979** |
| B136 / 25 | **0.996** | **0.996** | **0.678** |
| **mean** | **0.185** | **0.173** | **0.785** |

**H_CAGR50 PASS** at the 80.0th percentile. **H_CAGRALL FAILS at 5 of 6** — the same count, and
the same failing cell (U56 / 25 bps), that 1023 reported against the mean. **H_STAB50 PASS at 10
of 12**, again matching 1023's 5-of-6 per chooser.

## Why the queue's worry is empty — and where its mechanism points the wrong way

**The scored distribution has no skew to exploit.** A sequence score is a 16-fold average, and
the CLT flattens the pool's shape out of it. Across the six Q16/`MEAN_SH` cells, median − mean
runs **−0.00069 / +0.00028 / −0.00003 / −0.00022 / −0.00050 / +0.00055** against sds of
0.0129–0.0257: in units of one sd that is **−0.035 to +0.043, mean −0.0031**, and the SIGN is
positive in only 2 of 6. **H_PREMISE's headline PASS (+0.000280) is a noise pass and is reported
as one** — it is 1.3% of one standard deviation and would change sign on a different seed. On
`Q32` (32-fold averages) the range tightens further to −0.018..+0.030 sd.

**And the skew the queue reasoned from exists at the BOOK level with the opposite sign.** The
per-end 18-book distribution — what a single draw actually sees — has median − mean **−0.014349
/ −0.014246 / +0.004054 / −0.005992 / +0.008565 / +0.005328** across the six Q16 cells and is
negative in 4 of 6, negative in 4 of 6 on `Q32` too. The pool is RIGHT-skewed: a few
high-Sharpe books pull the mean ABOVE the median. So the chooser the queue describes — one that
dodges the worst books and lands near the median — clears the median bar and **fails the mean
bar**, the reverse of the premise. Where the two bars could differ at all, 1023's was the
stricter one.

## What the percentile DOES add: the magnitude, which a point estimate cannot carry

1023 published "+0.0418 of Sharpe" and "−0.0418" with no yardstick, although it had committed
one (`sd_over_seq`) and never used it. Re-expressed as a share of coin flips beaten:

- `IS_CAGR` at the headline scores 1.2618 against a random mean of 1.2441, z **+0.83**,
  percentile **0.800**. The record's best legal rule-8 chooser is beaten by **one coin flip in
  five** drawn from the same 18 books.
- `IS_SHARPE` and `IS_LEGS` score 1.1557, z **−4.16**, percentile **0.000** — **0 of 2,000**
  uniform draws do worse. 1023's "RANDOM wins 5 of 6" understates this badly: these two are not
  merely below average, they are outside the null's entire realised support in the headline cell.
- Averaged over the six cells the ordering is `IS_CAGR` 0.785, `IS_SHARPE` 0.185, `IS_LEGS`
  0.173 — a gap of ~60 percentile points between the record's three choosers, from gaps of
  0.02–0.11 in Sharpe.

## The statistic dial moves the answer; the end grid mostly does not

**H_DIAL FAIL.** The set of choosers clearing the 50th is `{IS_CAGR}` at all three end grids on
`MEAN_SH` and on `MED_SH`, and **`{IS_CAGR, IS_SHARPE, IS_LEGS}` at all three on `RATE4B`.**
Which choosers beat a coin flip therefore depends on what they are scored FOR, not on how wide
the band is.

**H_VERDICT PASS, and it is the sharpest form of 1023's own conclusion.** In the headline cell
`IS_CAGR`'s 4b pass rate is 0.938 against the pool's 0.446, at percentile **1.000** — it beats
**2,000 of 2,000** coin flips on verdict reliability while beating 1,600 of 2,000 on Sharpe. IS
fit buys the verdict, not the return, and the percentile separates the two cleanly where a
Sharpe gap could not.

The end grid matters in one place only: the 25 bps rung, where widening `Q16` → `Q32` moves
`IS_CAGR` from 0.317 to **0.002** on U56 and `IS_SHARPE` from 0.059 to **0.968**. At 0 and 10
bps the two grids agree on every one of the 12 verdicts.

## Gates 8 of 11 — and the two failures are a resolution fact worth a clause

G1 PASS (6.94e-18 / 1.67e-16), G2 PASS (0.0), **G3 PASS — SPY OOS ≡ the record's committed
15.21% / 0.8711 / −33.72%**, **G4 PASS — 1013's four published picks, 4 of 4 at max |d|
4.59e-04**, G5 PASS (ladder determinism 0.0 over 3,456 rows), G6 PASS (IS purity, 0 moved picks
of 96), **G7 PASS — the sampler's MC mean equals the EXACT closed-form pool mean in 6 of 6 cells
at max |d| 1.11e-03, which is what licenses reading a percentile off the draws at all.**

**G8 FAILS at 0.2482 and G8b at 0.0255; G8d PASSES at 0.00075 and G8c diagnoses the gap
exactly.** A mid-rank percentile returns 0.5 at a distribution's own median only where there is
no ATOM there, and exactly two things put one there. (i) `REC1` is ONE end, so the score
distribution IS the 18-book pool: **every percentile at PROTOCOL's own declared split is
quantised to 1/18 = 0.0556** and cannot be resolved finer, whatever the draw count. (ii)
`RATE4B` averages 0/1 indicators and takes 2 distinct values at `REC1`, with an atom up to
**0.679**. On the 24 multi-end continuous cells the bar is met by more than an order of
magnitude (worst |d| 7.5e-04). The failures are properties of the STATISTIC and the POOL SIZE,
not of the percentile function — and the first of them is a finding: **the record's own single
split point is the least resolvable place to percentile a chooser.**

## Rule 8 walk-forward — PROTOCOL's own split, both KEEP paths

Picks made on **2009–2016 alone**, 2017–2026 read ONCE, 3 choosers × 2 panels × 3 rungs = 18.

**OOS 4b: 18 of 18. OOS 4a: 0 of 18.** Best pick `U56 IS_CAGR → U56-qroll-q0.17-w1008-d0.50`,
OOS **15.60% / 1.293 / −15.59%** at 10 bps (16.68% / 1.372 / −15.52% at 0 bps) against SPY OOS
**15.21% / 0.8711 / −33.72%** (4b cap −20.23%, floor 10.57%) and RULES v2 live @10 bps
**8.62% / 1.2007 / −12.05%** (H1 1.2322 / H2 1.1760). The Sharpe-family picks read 11.99% /
1.162 / −19.05%; B136 reads 11.05% / 1.097 / −19.50% and 14.30% / 1.157 / −17.31% against its own
SPY 15.33% / 0.8767 / −33.72% and RULES v2 7.98% / 1.0993 / −12.24%.

**No book is promoted and no book KEEP is claimed, for two stated reasons.** First, these are
not new objects: they are 1013's and 1023's already-committed picks, reproduced here to 4.59e-04
as gate G4 and already carried in LEADERBOARD.md without promotion. Second — and this is this
run's own contribution to reading them — **a uniform draw from the same 18-book pool clears 4b
at these very cells 0.333 to 0.604 of the time** (0.444 at the headline), so an 18-of-18 4b
sweep is close to what the null delivers, and the best pick sits at the **58.3rd percentile** of
its own pool's OOS Sharpe. Every pick fails 4a on drawdown against the live book's −12.05%, for
the fifth time in the record. A 4b pass a coin flip reaches 44% of the time is not capital-worthy
evidence, which is the whole argument for the clause below.

## Survivorship (rule 9)

U56 and B136 are CURRENT-CONSTITUENT lists, so every CAGR and drawdown LEVEL above is optimistic
and every 4b count an upper bound. The measured object is a chooser's RANK inside a distribution
built from the SAME pool over the SAME tape, and the bias is a common factor to the chooser and
to every draw it is ranked against. Where it does not cancel it flatters the coin flip — a
uniform draw from a survivor panel is a better book than a real-time one — so **every chooser
percentile here is a LOWER bound and H_CAGR50 was the harder call.** SPY is a real index series
and is not inflated.

## The clause this proposes, for Sunday review and NOT written into PROTOCOL.md (rule 6)

See `2026-09-16_chooser-percentile-clause_C.memo.md`. In short: a rule-8 chooser claim states the
chooser's PERCENTILE in its own pool's random-sequence distribution and that distribution's sd,
not a mean gap; and it states the pool size, because an N-book pool quantises every percentile to
1/N and PROTOCOL's own single split point is the coarsest reading available.

## What 1023 may still say, and what 1031 adds

**MAY STILL SAY** — that `IS_CAGR` beats a uniform draw from its pool on OOS Sharpe in 5 of 6
cells and that the two stable choosers lose to one; both survive the median bar unchanged, in
the same cells. **MAY NO LONGER SAY** — that the mean-versus-median choice is open (it changes
nothing, 0 of 18), or that the RANDOM control is summarised by its mean (it has a sd of
0.013–0.026 that turns 1023's "+0.0418" into "beaten by 1 draw in 5" and its "−0.0418" into
"beaten by 2,000 of 2,000"). **1031's own premise, that the pool's skew makes the mean the softer
bar, is refuted with its own sign reversed.** Follow-ups filed: 1033, 1034, 1035.
