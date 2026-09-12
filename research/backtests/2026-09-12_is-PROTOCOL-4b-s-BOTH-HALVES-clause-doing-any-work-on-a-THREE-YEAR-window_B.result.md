# Idea 832 (lane B, 2026-09-12) — is PROTOCOL 4b's BOTH-HALVES clause doing any work on a three-year window?

**ANSWERED = IT DOES ARITHMETIC WORK AND CARRIES NEGATIVE INFORMATION.** On a 756d window the
clause flips **14.16%** of verdicts (pooled over the record's 12 committed 4b passes), but
**98.58%** of the 18-month comparisons it is made of are inside their own two-sided 95% noise
band, and the windows it passes go on to do **worse**, not better, than the ones it fails:
P(next non-overlapping window passes 4b | halves PASS) = **0.3182** against **0.3810** for
halves FAIL, difference **−0.0628**. On the record's own FIXED window the clause changes
**nothing at all** — 11 of 12 books pass 4b with it and the same 11 without it.

Script: `2026-09-12_is-PROTOCOL-4b-s-BOTH-HALVES-clause-doing-any-work-on-a-THREE-YEAR-window_B.py`

## What was scored

Idea 831's corpus, rebuilt from its own committed constructors: the record's 12 reconstructible
4b/KEEP memo books (`K1..K8`, `R1..R4`), each at its own memo gross, band, n and cadence, with
the LIVE RULES v2 book and retired RULES v1 as comparands. **2 tuned parameters, the queue's
own:** clause reading **k** (the sub-window leg requires the book to beat SPY's Sharpe in every
one of k contiguous equal blocks — **k=1 is the clause dropped**, k=2 is the record's reading,
k=3 is the queue's THIRDS, k=4 the other side of it) and window split **H** (756d / 1260d).
Entry spacing s ∈ {21, 63}, claim set (MEMO8/MEMO12) and cost rung ∈ {0, 10, 25} bps are
reported, not selected. **18,396 (book, H, s, entry, cost) rows**, 6,132 at the PROTOCOL rung;
every cell printed and written to `.grid.csv` / `.cells.csv`.

**Gates, before any new number: 6 of 6 PASS.**
G1 every book reproduces its own memo's published triple inside the declared vintage tolerance
(12 of 12 scored; K2 and V1 publish no triple and are marked so). G2 LIVE reproduces RULES v2's
8.63% / 1.202 / −12.05%. **G3** this run's census reproduces idea 828/829/831's committed entry
share for the standing candidate (K5, H=756, s=21, k=2) at **0.3977 on 176 windows, |d| =
0.0000**. G4 the vectorised window metrics match `engine.metrics` to **2.2e-16**. **G5** the k=2
leg-failure counts reproduce idea 831's committed totals **exactly**: 1,574 failing windows,
halves 975, dd 898, cagr 550, sharpe 211. **G6** the analytic noise band (Memmel correction to
Jobson–Korkie) matches a paired stationary block bootstrap (L=21, 1,000 reps, seed 8320) on 60
sampled blocks at median ratio **1.1401** (IQR 1.0121–1.2603).

## The answer, three ways

**1. On the record's FIXED window the clause is inert.**

| clause reading | fixed-window 4b | fixed-window 4a |
|---|---|---|
| k=1 (**dropped**) | **11 of 12 PASS** | 0 of 12 |
| k=2 (the record's reading) | **11 of 12 PASS** | 0 of 12 |
| k=3 (thirds) | 9 of 12 | 0 of 12 |
| k=4 (quarters) | 6 of 12 | 0 of 12 |

Dropping PROTOCOL 4b's both-halves clause changes **not one** of the record's committed
verdicts. The only book it ever excluded, K7, fails on the CAGR floor with or without it. Cut
the window into thirds instead and K1 and R4 fall; into quarters and K1, K2, R1, R2, R4 fall.
The clause's severity is entirely a function of how finely you slice, which is a dial the
PROTOCOL does not name.

**2. On a three-year entry-date window it flips verdicts — by noise.**

At the headline cell (MEMO12, H=756, s=21, 10 bps) the **marginal bind rate** — windows that
pass the other three legs and fail *only* the halves leg — is **0.1416 pooled**, median 0.0994
per book, ranging 0.0000 (K7) to **0.3409** (R4). So the clause is not idle: it is the single
biggest reason a 3-year entrant fails, exactly as idea 831 found (975 of 1,574 failures).

But look at what those comparisons are:

| H | k | block | n blocks | **inside the 95% noise band** | median margin | leg pass share |
|---|---|---|---|---|---|---|
| 756 | 2 | 18.0 mo | 4,224 | **0.9858** | +0.0015 | 0.5384 |
| 756 | 3 | 12.0 mo | 6,336 | 0.9908 | −0.0141 | 0.2135 |
| 756 | 4 | 9.0 mo | 8,448 | 0.9821 | −0.0248 | 0.1075 |
| 1260 | 2 | 30.0 mo | 3,648 | **0.9649** | +0.0082 | 0.7741 |
| 1260 | 3 | 20.0 mo | 5,472 | 0.9845 | −0.0012 | 0.4660 |
| 1260 | 4 | 15.0 mo | 7,296 | 0.9888 | −0.0136 | 0.2116 |

**98.58% of the 4,224 eighteen-month book-vs-SPY Sharpe comparisons at the headline cell cannot
be called at all** (|z| < 1.96 on the Memmel-corrected difference of two correlated Sharpe
ratios; median |z| over the bootstrap-gated sample is 0.593). The leg passes 0.5384 of them —
a coin, demanded to land heads twice. Even at a 5-year window the 30-month blocks are
uncallable 96.49% of the time. **Making the window longer does not fix this; only k=2 at
H=1260 gets the leg above 0.77, and it is still noise underneath.**

**3. The clause's verdict is negatively informative about the next window.**

Conditioning on the other three legs passing, and comparing this window's halves verdict to the
**next, non-overlapping** window's full 4b verdict:

| H | conditioned pairs | P(next PASS \| halves PASS) | P(next PASS \| halves FAIL) | difference | Spearman(halves margin, next dSharpe) |
|---|---|---|---|---|---|
| 756 | 627 (396 / 231) | 0.3182 | **0.3810** | **−0.0628** | **−0.1922** |
| 1260 | 419 (345 / 74) | 0.7072 | **0.7838** | **−0.0765** | −0.0434 |

Per book at H=756, **9 of the 11 books with a defined difference are negative or zero** (K6
−0.6000, R1 −0.4024, K3 −0.3776, K5 −0.3459, K4 −0.2252, R4 −0.0238, R3 −0.0333, K8 −0.0052,
K1/K2 0.0000); only R2 is positive (+0.4118), and K7 has one pair. The sign is the opposite of
the one a robustness clause is supposed to have: a book that beat SPY in both halves of the
last three years is *less* likely to clear the bar over the next three.

## Pre-registered hypotheses — 1 of 6 PASS

| | verdict | reading |
|---|---|---|
| H_WORK | **FAIL** | median marginal bind 0.0994 vs bar 0.10 — short by 0.0006; **pooled 0.1416**, max 0.3409 (R4). Called FAIL on the pre-registered statistic, but this is a knife-edge and the pooled reading is the honest headline: the clause *does* bind. |
| H_MONO | **PASS** | pass share monotone non-increasing in k at **12 of 12** books (k is not nested, so this was a real test) |
| H_SURVIVE | **FAIL** | dropping the clause takes **0 of 12** to 0.80 at 3y (max K4 **0.7045**); at 5y exactly **1 of 12** (K4 0.8026) |
| H_NOISE | **FAIL** | **0.9858** of the 18-month comparisons are inside their own 95% band vs bar 0.50 — failed by 0.49, the run's largest single number |
| H_INFO | **FAIL** | −0.0628 vs bar +0.05; the sign is wrong, not just the size |
| H_WF | **FAIL** | IS-chosen (k, H) = (1, 1260) is also the OOS best, but IS share 0.2523 → OOS 0.8363, **gap 0.5840** vs bar 0.10 |

## Rule 8

**(a) On this run's own tuned axes.** Choosing (k, H) on IS entries only (windows closing
≤2016-12-31) picks (k=1, H=1260) at IS share 0.2523; read once on OOS entries (≥2017-01-01) it
reads **0.8363**, gap **0.5840**. The IS pick happens to be the OOS best, but every cell moves
the same way — k=2/H=756 runs 0.0903 → 0.4240, k=4/H=756 runs 0.0097 → 0.0531. **The entry-date
pass share is a property of the window, not of the clause reading**, which is the same
post-2017 character ideas 605/609/825/829 keep finding.

**(b) On the books.** OOS (2017-01-01..) against the live baseline and SPY: RULES v2 LIVE
**9.47% / 1.2782 / −12.05%**, SPY **15.33% / 0.8767 / −33.72%**. The 12 books run OOS CAGR
6.38%–16.04%, OOS Sharpe 1.0400–1.3937, OOS MaxDD −11.13% to −20.00%; K8 is best on Sharpe
(1.3937) and CAGR (16.04%), R4 worst on Sharpe (1.0400), K7 worst on CAGR (6.38%). **Every one
of the 12 has a lower OOS CAGR than SPY's 15.33% except K8 (16.04%) and R3 (16.00%).** Both
KEEP paths, fixed window: **4b 11 of 12 (identical with and without the halves clause), 4a 0 of
12** — not one committed book beats the LIVE RULES v2 book on the sub-window leg at no worse
drawdown, at any k.

## Verdict

**KILL for capital** — no book is promoted, no KEEP is claimed, no memo is filed. The finding is
about the bar, not the books: PROTOCOL 4b's both-halves clause is **inert where the record uses
it** (11 of 12 either way on the fixed window) and **actively misleading where idea 831 found it
binding** (98.58% uncallable comparisons, −0.0628 on the next window). It is not measuring
robustness on a three-year window; it is charging a coin toss twice.

**Proposal for Sunday review (PROTOCOL.md NOT modified by this run):** state the split k and the
minimum block length beside every 4b verdict, and do not read a sub-window Sharpe comparison
shorter than the point where it can be called — on this corpus no block under 30 months clears
its own noise band even 4% of the time. Either replace the clause with a statistic that has
power at that length, or drop it and say so; keeping it unexamined means 4b's most-cited failure
mode is noise with a name.

RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are untouched. Two follow-ups filed
(838, 839).

## Caveats

- **SURVIVORSHIP:** `universe.json` and `universe_broad.json` are current-constituent lists, so
  every *level* here is optimistic. The object is a within-window contrast, which the bias moves
  far less.
- The noise band is the Memmel (2003) correction to Jobson–Korkie, gated against a paired
  stationary block bootstrap (G6, median ratio 1.14 — the analytic band is if anything slightly
  **wide**, so the 0.9858 is a mild *under*statement of how uncallable these comparisons are).
- H_INFO's conditioning set shrinks with the window (627 pairs at 756d, 419 at 1260d) and is
  pooled over overlapping entry dates within a book, so its standard error is wider than n
  suggests; the per-book table is published for that reason and 9 of 11 carry the same sign.
- Windows are slices of one full-sample simulation (C1): the entrant joins a book already
  holding its weights. A book re-initialised at each entry date would carry its own warm-up
  cost, which this convention does not charge.
