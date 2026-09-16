# Idea 1013 (lane B, 2026-09-16) — does RULE 8's IS END DATE need PINNING the way its START does?

**ANSWERED = NO, NOT THE WAY ITS START DOES — THE VERDICT IS SAFE, THE PICK AND THE PUBLISHED
NUMBER ARE NOT.** KILL the premise that rule 8's IS END carries a defect of the same order as
its START: **0 of the record's 9 committed memo-backed 4b passes change verdict at ANY of the
16 legal split points**, and the comparand bar moves **8.47x less** than 1001's start dial moved
its. KILL, separately, the assumption the queue line inherits — that a stable verdict means a
stable rule-8 result: **the PICK moves in 3 of 6 (panel x chooser) cells**, and the pick's
**published OOS Sharpe moves up to 0.2666 purely from the split date, which is LARGER than the
0.2102 median leg margin the record certifies its passes on**. KEEP as a PROTOCOL rule 8
reporting clause (proposed, not applied — rule 6). Nothing promoted, no RULES change;
`RULES.md`, `PROTOCOL.md`, `scan.py`, `bot.py` and `baseline.py` untouched.

## THE GRID

**45 books** (the record's **9** committed memo-backed 4b passes, rebuilt from lane C's own
`shelf_books`, plus the **36**-book never-memo-selected band x gross x QROLL ladder) x **16
quarter-end split points** 2015-03-31 .. 2018-12-31 x **3 cost rungs** x **2 bar conventions**
= **2,160 ladder rows**, plus **192 rule-8 picks** (2 pools x 2 panels x 16 ends x 3 IS-only
choosers). Two tuned axes only — **IS END GRID** {END_Q 16 quarter-ends, END_Y 4 year-ends} x
**CHOOSER** {IS_SHARPE, IS_LEGS, IS_CAGR} — all points reported, none selected. The window
START is PINNED at the record's own `px.index[260]` (2009-01-13) throughout, so the only thing
that moves is the split point PROTOCOL rule 8 sets by fiat. Runtime 7.3 s.

## THE ANSWER, AND IT IS AN INTEGER

The queue's literal question — *how many committed passes change* — is **ZERO**. All nine
SHELF books pass 4b at **16 of 16** ends, each with **one** distinct binding-leg set. 1001's
analogue on the START dial lost `L_H1` on **seven of nine** at w=2012. Across all 45 books the
verdict is constant on **41 (0.9111)**, so **H_PIN PASSES its 0.90 bar — but only just, and
only at this rung.** The cost-rung control says so plainly and is reported as loudly as the
pass: **0.9556 at 0 bps, 0.9111 at 10 bps, 0.8444 at 25 bps.** *The headline hypothesis fails
its own bar at 25 bps.* PROTOCOL's 10 bps is the rung that makes the fiat look safe.

**H_BAR PASSES, and the margin is the point.** SPY's OOS Sharpe bar moves **0.1263** (U56) /
**0.1266** (B136) across the 16 legal ends, against 1001's published **1.0717** over the legal
starts — **8.47x tamer** — and below 1001's own full-tape **0.1975**. The end is the calm half
of the window, which is exactly why the fiat has survived unexamined.

## THE MECHANISM — THE SPLIT POINT MOVES EXACTLY ONE LEG OF FIVE

| leg | constant across the 16 ends | why |
|---|---|---|
| `L1_H1` | **45/45** | E-INVARIANT BY CONSTRUCTION — the record's halves are a COUNT split of the FULL post-warm-up path (`baseline._row`, `h = len(r)//2`), which the split point never touches |
| `L2_H2` | **45/45** | same |
| `L3_OOS` | **45/45** | both sides move together; the book's OOS Sharpe and SPY's move in step and the comparison survives |
| `L4_DD` | **45/45** | **SPY's `|OOS MaxDD|` range across all 16 ends is 0.0000** — the 2020 crash sits inside EVERY legal OOS window, on the book side too (3 of 6 pick cells show OOS MaxDD spread 0.0000) |
| `L5_CAGR` | **40/45 (0.889)** | the only E-sensitive leg |

**PROTOCOL rule 8's split point is a dial on the CAGR floor and on nothing else.** All four
verdict-flippers are **B136** and all four flip on `L5_CAGR` alone:

```
GRID  B136-band0.03-g1.00          ....P...........   1/16 ends
GRID  B136-band0.08-g1.00          ..PPPPPPP......P   8/16 ends
GRID  B136-qroll-q0.17-w252-d1.00  ..PPPPPPPPPPPPPP  14/16 ends
GRID  B136-qroll-q0.17-w504-d1.00  PPPPPPPPPP..PPPP  14/16 ends
```

`B136-band0.08-g1.00` clears 4b at **exactly 8 of the 16 legal split points**. Its
certification is a coin flip on a date nobody chose on evidence. **H_LEG FAILS at 0.8889**
against its 0.90 bar — the same five books, read as binding-leg sets.

## THE PART THAT IS NOT SAFE — H_PICK FAILS 3 of 6

| panel | chooser | distinct picks / 16 | OOS Sharpe spread | OOS CAGR spread | OOS 4b |
|---|---|---|---|---|---|
| U56 | IS_SHARPE | **2** | **0.2666** | 0.0245 | 16/16 |
| U56 | IS_LEGS | **2** | **0.2666** | 0.0245 | 16/16 |
| U56 | IS_CAGR | **4** | 0.2285 | 0.0238 | 15/16 |
| B136 | IS_SHARPE | 1 | 0.1955 | 0.0177 | 8/16 |
| B136 | IS_LEGS | 1 | 0.1955 | 0.0177 | 8/16 |
| B136 | IS_CAGR | 1 | 0.1747 | 0.0234 | 16/16 |

**The stronger finding is in the last three rows, where the pick NEVER changes.** Holding the
chosen book fixed, the number the record would PUBLISH for it still moves **0.1747 to 0.1955**
of Sharpe, purely from where the split was put. For scale: idea 1001's median SHELF HALFMIN leg
margin — the weaker of the two Sharpe legs on the committed shelf — is **0.2102**, against
comparand bootstrap SEs of 0.2877 / 0.3350. **The split-point swing is the same order as, and
in the worst cell larger than, the margin the record certifies its passes on.** A stable
verdict is not a stable result.

## ATTRIBUTION — A BENCHMARK DIAL, NOT A POWER DIAL

**H_COMP PASSES.** Pearson of the 4b pass count against SPY's own OOS Sharpe is **+0.7595**;
against the OOS window's LENGTH it is **+0.0806**. Sliding the split point does not change the
answer by giving the test more or less data — it changes it by moving the benchmark's bar.
That is the same attribution 1001 found for the START, arriving at one tenth the amplitude.
**H_MONO FAILS**: the pass count runs 26 26 28 28 **29** 28 28 28 28 27 26 26 27 27 27 28 over
the 16 ends — non-monotone, one sign change, peak at 2016-03-31 and PROTOCOL's own 2016-12-31
sitting one below it. A regime dial, not a length dial, so "use more data" is not the fix.

## RULE 8 AND BOTH KEEP PATHS

The whole experiment is a rule-8 walk-forward; at PROTOCOL's own E = 2016-12-31, picks made on
2009-01-13..2016-12-31 ALONE from the never-memo-selected GRID pool, 2017-2026 read once:

| panel | chooser | pick | OOS CAGR | OOS Sharpe | OOS MaxDD | 4b | 4a |
|---|---|---|---|---|---|---|---|
| U56 | IS_SHARPE / IS_LEGS | `U56-band0.08-g1.00` | 11.99% | 1.162 | −19.05% | **Y** | n |
| U56 | IS_CAGR | `U56-qroll-q0.17-w1008-d0.50` | 15.60% | 1.293 | −15.59% | **Y** | n |
| B136 | IS_SHARPE / IS_LEGS | `B136-band0.08-g1.00` | 11.05% | 1.097 | −19.50% | **Y** | n |
| B136 | IS_CAGR | `B136-qroll-q0.12-w1008-d0.50` | 14.30% | 1.157 | −17.31% | **Y** | n |
| U56 | *SPY* | comparand | **15.21%** | **0.871** | **−33.72%** | full 0.883 / −33.72% | |
| U56 | *RULES v2* | live baseline | 9.45% | 1.276 | −12.05% | full **1.201** / **−12.05%** | |
| B136 | *SPY* | comparand | **15.33%** | **0.877** | **−33.72%** | full 0.886 / −33.72% | |
| B136 | *RULES v2* | live baseline | 7.88% | 1.106 | −12.24% | full **1.099** / **−12.24%** | |

**KEEP path 4a: 0 of 96 GRID picks and 1 of 45 books** (`B136-band0.08-g0.50`, CAGR 5.67% /
Sharpe 1.118 / MaxDD −10.00%, halves 1.275 / 0.967). It beats the live book in both halves with
a shallower drawdown and is **not promotable**: at 5.67% CAGR it misses 4b's floor
(0.70 x 15.33% = 10.73%) by 5.1 pp — the low-return shape PROTOCOL 4b was written to stop
promoting. **Note that 4a is entirely immune to this run's dial**: it reads full-sample halves
and full-sample MaxDD and never looks at the split at all. **KEEP path 4b: 79 of 96 GRID picks;
437 of 720 ladder rows at 10 bps (439 under the WIN bar).** Nothing is promoted — none of these
is a new book, and every 4b count above is an upper bound under the standing base-rate,
per-leg-percentile and declined-slot clauses (926/942, 975-B, 993).

## GATES 7 of 7 PASS, printed before any result number

G1 fast runner == `engine.backtest` on returns AND turnover **6.939e-18 / 1.665e-16**. G2
`rules_v2_weights(U,0.03,0.75)` == `baseline.rules_v2_weights(U)` **0.000e+00**. **G3
CROSS-RUN: SPY's OOS triple at E=2016-12-31 reads 15.2102% / 0.8711 / −33.7173% against the
record's committed 15.21% / 0.8713 / −33.72%, max|d| 1.702e-04.** **G4 all 9 SHELF books
reproduce their committed memo triples 9/9.** G5 determinism over the whole 2,160-row ladder
**0.000e+00**. G6 IS purity — every chooser's pick invariant under a permutation of the OOS
columns, **0 disagreements**. G7 leg identity at E=REC against an independent recomputation,
**0 disagreeing rows**.

## LIMITS, STATED

The split-point grid is quarterly; a daily grid would find more flips, so every instability
number here is a LOWER bound and every stability number an UPPER bound. The 2015-2018 span is
the queue line's own and is bounded below by needing an IS window long enough to choose on and
above by needing an OOS window long enough to read — it is not a claim about ends outside it.
The SHELF's 9-of-9 invariance is measured on books selected on the FULL tape, so their passes
were never at risk from an OOS-window dial in the first place; that is a reason the result is
unsurprising, not a reason it is wrong, and it is why the GRID carries the headline. `L4_DD`'s
total inertia is a property of THIS tape — 2020 is inside every legal OOS window here — and
would not survive a split point after 2020.

## SURVIVORSHIP (PROTOCOL rule 9)

U56 and B136 are CURRENT-CONSTITUENT lists, so every CAGR and drawdown LEVEL above is
optimistic and every 4b count is an UPPER bound. The measured object is the MOVEMENT of a
verdict as one date slides on the SAME books over the SAME tape, and the bias is a common
factor to every end. Where it does not cancel it works AGAINST this run's own suspicion: a
survivor panel's books are steadier than real-time ones, so the instability measured here is a
LOWER bound and **H_PIN was the EASIER hypothesis to pass**. SPY is a real index series and is
not inflated, so the comparand movement in H_BAR is clean.

## PROPOSED, NOT APPLIED (rule 6)

`2026-09-16_split-point-band-clause_B.memo.md` — a PROTOCOL rule 8 reporting clause requiring a
rule-8 result to publish its split-point band, with a reading rule for the record's existing
picks. It contradicts nothing: 1001's start-dial numbers and the record's committed SPY and
SHELF triples are all reproduced here.

## FOLLOW-UPS FILED

1021, 1022, 1023.
