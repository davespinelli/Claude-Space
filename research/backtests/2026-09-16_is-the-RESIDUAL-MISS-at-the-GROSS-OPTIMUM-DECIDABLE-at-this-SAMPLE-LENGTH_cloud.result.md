# Idea 1083 (cloud lane, 2026-09-16) — is the 1.0–1.3pp RESIDUAL MISS at the GROSS OPTIMUM DECIDABLE at this SAMPLE LENGTH?

**ANSWERED = NO. "The window is empty" is NOT a claim this tape can carry. KILL of 1064's and
1071's empty-window verdict as an ESTABLISHED fact — it is reported here as UNRESOLVED, with
P(open) running 7.6%–16.5% across every cell. CONFIRM of the realised numbers themselves, which
reproduce exactly. A PARK is flagged (U56 / g=0.50) that misses full 4b by 0.23 pp of CAGR and
passes 4b OUT OF SAMPLE. No book promoted, no KEEP claimed; RULES.md, PROTOCOL.md, scan.py,
bot.py and baseline.py untouched.**

## What was asked
Idea 1071 reproduced 1064's empty joint window at a best miss of 1.270 pp (U56) and 1.012 pp
(B136). Bootstrap the MISS at the gross optimum on both panels, report its 90% interval, and say
whether "the window is empty" is a claim this tape can carry. Max 2 params (block length, draws).

## The two dials, and what was declared before any number
`BLOCK LENGTH L ∈ {21, 63, 126, 252}` × `DRAWS D ∈ {200, 1000}` — 8 cells per panel, all reported,
on a **10-rung** gross ladder (0.30…0.75) that is fully published. One circular block index per
replicate is applied to **every series at once** — SPY, the live RULES v2 book and all ten rungs —
because every term of MISS is measured on the same tape and a book-only resample would hold the
two bars fixed and understate the interval.

Declared in advance: **MaxDD is a path functional**, so the DD leg is the one this method
distorts, and (declared direction) reshuffling should **break** long declines and bias
bootstrapped |MaxDD| *small*. **Decidability rule, fixed before the run:** the empty-window claim
is decidable at 90% iff the 5th percentile of MISS is > 0; a straddle means UNRESOLVED.

## Gates (printed before any result number) — 6 of 7
| gate | value | |
|---|---|---|
| G1 CROSS-RUN vs 936's committed W/H126 triple | 3.18e-07 | PASS |
| G2 fast runner ≡ `engine.backtest` | 1.39e-17 | PASS |
| G3 CROSS-RUN SPY OOS triple | 1.70e-04 | PASS |
| **G4 bootstrapped \|MaxDD\| biased SMALL as declared** | **L=21 +1.54, L=63 +0.87, L=126 +0.05, L=252 +0.00 pp** | **FAIL** |
| G5 CROSS-RUN 1071's committed optimum MISS — B136 2.76e-05, U56 2.68e-01 | | PASS |
| G6 live RULES v2 MaxDD ≡ committed −12.05% | 4.95e-05 | PASS |

**G4 failed and the declared direction was backwards.** Block resampling does not break this
tape's long declines — at short blocks it *concatenates* bad ones, so bootstrapped |MaxDD| comes
back **larger** by up to 1.54 pp, and the bias vanishes monotonically as L grows (+0.00 pp at
L=252, where the worst episode fits inside one block and is reproduced exactly). The direction
matters for reading the result: the bias **inflates** MISS, i.e. it pushes the verdict *toward*
"empty" — and the window still cannot be shown empty. **The failure is conservative for the
conclusion below, and is published rather than repaired.**

G5's U56 gap of 0.268 pp is not an error: 1071 read a 5-rung ladder and this run reads 10, so the
U56 optimum moves from g=0.45 (1.270 pp) to **g=0.50 (1.002 pp)**. B136's optimum is unchanged at
g=0.45 and reproduces to 2.8e-05.

## A correction to the queue text's own premise
The queue says both optima bind "on the 4b CAGR floor rather than the DD cap". On the finer ladder
that is true only for B136. At U56's true optimum g=0.50 the **DD leg binds** (|−13.06%| −
|−12.05%| = **1.01 pp** against the CAGR leg's 0.23 pp), and across the draws **DD binds on 0.718**
of replicates pooled (0.841 U56, 0.583 B136) — **H_CAGRLEG FAILS**. 1071's reading was a property
of its rung spacing, not of the book.

## The realised ladder (U56, all 10 rungs)
| g | CAGR | Sharpe | MaxDD | MISS | MISS_is | MISS_oos | 4b | 4a | 4b OOS |
|---|---|---|---|---|---|---|---|---|---|
| 0.40 | 8.26% | 1.1384 | −10.55% | 2.312 | 3.083 | 1.673 | ✗ | ✗ | ✗ |
| 0.45 | 9.30% | 1.1386 | −11.81% | 1.270 | 2.153 | **0.537** | ✗ | ✗ | ✗ |
| **0.50** | 10.34% | 1.1388 | −13.06% | **1.002** | **1.511** | 1.002 | ✗ | ✗ | **✓** |
| 0.55 | 11.39% | 1.1390 | −14.29% | 2.236 | 2.429 | 2.236 | ✓ | ✗ | ✓ |
| 0.75 | 15.58% | 1.1397 | −19.13% | 7.073 | 6.065 | 7.073 | ✓ | ✗ | ✓ |

**Window open at 0 of 10 rungs on both panels** — the realised verdict is 1064's and 1071's, on a
finer ladder. Sharpe is flat to 3 decimals along the whole ladder, as the arithmetic requires.

## The bootstrap — the answer
**At g\*** (the single rung), the empty-window verdict is decidable in **9 of 16 cells** and the
verdict **moves with the block length** (U56/D=1000 reads F,F,T,T over L=21,63,126,252;
B136/D=200 reads F,T,T,F) — **H_DECIDE and H_STABLE both FAIL**, and **H_DRAWS fails too**: going
from 200 to 1000 draws flips 4 of 8 (panel, L) verdicts.

**On the statistic 1064 and 1071 actually published** — MISS\*, the *minimum over the ladder* —
the verdict is **NOT DECIDABLE IN ANY OF THE 16 CELLS**:

| U56 | L=21 | L=63 | L=126 | L=252 |
|---|---|---|---|---|
| MISS\* median (D=1000) | 1.465 | 1.335 | 1.335 | 1.170 |
| 90% interval | [−0.97, 3.80] | [−0.75, 3.64] | [−0.26, 3.41] | [−0.25, 3.51] |
| P(some rung opens the window) | 0.165 | 0.131 | 0.089 | 0.083 |

B136 is the same shape: intervals [−0.89, 4.44] → [−0.32, 3.21], **P(open) 0.076–0.150**. Every
interval straddles zero at every block length and both draw counts, **16 of 16**.

**H_WIDTH PASSES and is the cleanest way to say it:** the 90% width of MISS at g\* runs **4.1 to
7.2 pp** against a realised MISS of **1.00 pp**. The record has been adjudicating a one-point
quantity with a five-point ruler.

## Rule 8 — gross chosen on IS (2009–2016) MISS alone, OOS (2017–2026) read once
| panel | pick | full | halves | OOS | 4b | 4b OOS | 4a |
|---|---|---|---|---|---|---|---|
| U56 | g=0.50 | 10.34% / 1.1388 / −13.06% | 1.2030 / 1.0960 | **11.25% / 1.1633 / −13.06%** | ✗ | **✓** | ✗ |
| B136 | g=0.45 | 9.60% / 1.0609 / −12.82% | 1.2873 / 0.8816 | 9.62% / 1.0071 / −12.82% | ✗ | ✗ | ✗ |

Benchmarks: **SPY** full 15.10% / 0.8829 / −33.72%, OOS **15.21% / 0.8711 / −33.72%** (U56
calendar); 15.16% / 0.8861 / −33.72%, OOS 15.33% / 0.8767 / −33.72% (B136). **RULES v2 live** full
8.62% / 1.2007 / −12.05%, OOS **9.45% / 1.2762 / −12.05%** (U56); 7.98% / 1.0993 / −12.24%, OOS
7.88% / 1.1059 / −12.24% (B136). **H_WF PASSES, 1 of 2.**

**The PARK, stated plainly and NOT proposed.** The IS-only pick on U56 — the same W/H126 top-20
book at **gross 0.50** — clears **four of 4b's five legs full-sample** (H1 1.2030 and H2 1.0960 vs
SPY's 0.9588 / 0.8207; MaxDD −13.06% against the −20.23% cap) and **fails only the CAGR floor, by
0.23 pp** (10.34% against 10.57%). It clears **4b outright out of sample**. It fails 4a on
drawdown by 1.01 pp. It is **PARK, not KEEP**: PROTOCOL rule 4's 4b bar is full-sample and it does
not clear it, and this run's own headline is that a margin of that size is not decidable on this
tape — which cuts against promoting it exactly as hard as it cuts against declaring it dead.

## Hypotheses (declared before the run, scored as written) — 2 of 6
- **FAIL H_DECIDE** — 9 of 16 cells at g\*, **0 of 16** on the published MISS\*.
- **FAIL H_STABLE** — the verdict moves with L in 3 of 4 (panel, D) groups.
- **PASS H_WIDTH** — max 90% width 7.244 pp against a realised MISS of 1.002–1.012 pp.
- **FAIL H_CAGRLEG** — the DD leg binds on 0.718 of draws, not the CAGR leg.
- **FAIL H_DRAWS** — 200 → 1000 draws flips 4 of 8 (panel, L) verdicts.
- **PASS H_WF** — 1 of 2 IS-only picks clears 4b out of sample.

## Verdict — **KILL** (of the claim, not of the arithmetic)
The realised numbers are right and reproduce to 2.8e-05. What cannot survive is the **verdict**
built on them: at this sample length a 1.0 pp miss sits inside a 4–7 pp sampling interval, the
bootstrap puts 8–17% probability on the window being open, and the verdict flips on the block
length and on the draw count — the two things a reader is least able to check. **1064's and
1071's empty-window results should be read as UNRESOLVED, not as established**, and any future
run proposing to close that window must publish the interval beside the point.

## Survivorship (PROTOCOL rule 9)
U56 and B136 are **current-constituent** panels. Every level is optimistic and the CAGR floor and
DD cap are read against SPY, a real index, so every MISS here is a **lower** bound on the true one
and every 4b count an upper bound. The bootstrap resamples the same inflated tape and **prices
sampling error only** — it cannot and does not correct the bias.

Script: `2026-09-16_is-the-RESIDUAL-MISS-at-the-GROSS-OPTIMUM-DECIDABLE-at-this-SAMPLE-LENGTH_cloud.py`.
6 CSVs (`ladder`, `bootstrap`, `rule8`, `benchmarks`, `gates`, `hypotheses`), console log.
