# Idea 1237 (lane C, 2026-09-17) — does the RECORD's TUNING COST CHANGE SIGN once the ANCHOR ITSELF is WALKED?

**VERDICT: KILL (capital). ANSWERED = YES, IT CHANGES SIGN — at 4 of the 19 distinct
stand-in anchors the record's own four ladders supply, over a range of [−0.3292, +0.1105]
that is 16x the headline it contains. The incumbent anchor's rank is 5 of 19 (p 0.263) on
ALL THREE pick sets, and 5 of 10 (p 0.500) once the 9 near-clones are removed — i.e. the
+0.0204 is a property of a MEDIAN book, and the decomposition the queue asks for is not
identified: mean-over-candidates says 106.3% of it is THIS anchor, median says 13.2%.**
15 of 15 gates pass. Runtime 15s, offline, deterministic (every CSV bit-identical across two
independent runs). No new book.

Script: `2026-09-17_does-the-RECORD-s-TUNING-COST-CHANGE-SIGN-once-the-ANCHOR-ITSELF-is-WALKED_C.py`
Dials (2, PROTOCOL rule 4): **ANCHOR RUNG** {all 22 candidate books} x **PICK SET**
{P_1214, P_AXIS, P_TEXT}. 66 cells, every one published in `.grid.csv`. Nothing selected on.
The substitution rule is FROZEN at S_ALL, not dialled: 1224 established S_SE1/S_SE2/S_ANC95
are decision-identical to it at 0 of 620 cells, so a resolution qualifier is a no-op here.
`DELTA(A) = OOS Sharpe(stand-in anchor A) − OOS Sharpe(the book the record picked)`, so
POSITIVE = the record's tuning cost it that much *against that anchor*.

---

## 1. What was walked, and what the candidate set actually contains

The incumbent anchor is ONE book wearing four ladder names — gate G4 re-establishes bit for
bit, on all three panels, that N=20 / H=126 / GROSS=0.75 / CADENCE=W are the same return
stream. So a stand-in anchor is also one book, and the record's four ladders supply **22
candidate keys per panel, collapsing to 19 DISTINCT books** (G5, verified on realised
returns).

**But the 19 are not 19 comparable books, and that is measured rather than assumed (G12).**
Of the 18 non-incumbent keys, **9 are GROSS rungs whose full-sample Sharpe differs from the
incumbent's by at most 0.0040** across three panels — 1189's degeneracy (at a 0% cash rate
Sharpe is invariant to gross; only a monotone cost drag survives), so they are the anchor
re-levered, not alternatives to it. The smallest gap among the 9 non-GROSS candidates is
**0.0171, 4.3x larger**. Every figure below is published on both partitions.

P_TEXT is **frozen at 1224's own 62 committed (panel, ladder, rung) triples**, read from its
committed `picks.csv.gz` rather than re-harvested, so this run prices the same 620 cells that
produced the +0.0204. Gate G10 replays 1224's three committed deltas, SEs and both mean
columns to **4.90e-05**. A live re-harvest is run alongside as a drift diagnostic only (1230):
the tree has grown 33,861 → 33,907 units over 1,160 → 1,161 `.md` files, and today reads **62
triples, 62 shared, 0 new, 0 lost** — stable this time, still not a fixed point, still not used.

## 2. The answer to the question as asked — all 22 anchors, P_TEXT

| anchor | mean OOS Sharpe(A) | DELTA | SE | t |
|---|---|---|---|---|
| N=5 | 0.6866 | **−0.3292** | 0.1526 | **−2.16** |
| N=10 | 0.9275 | −0.0883 | 0.0821 | −1.08 |
| N=15 | 1.0453 | +0.0295 | 0.0453 | +0.65 |
| **N=20 \*** | **1.0361** | **+0.0204** | **0.0105** | **+1.94** |
| N=30 | 1.1007 | +0.0850 | 0.0493 | +1.72 |
| N=40 | 1.1080 | +0.0923 | 0.0579 | +1.59 |
| H=21 | 0.9563 | −0.0595 | 0.0719 | −0.83 |
| H=63 | 1.0207 | +0.0049 | 0.0569 | +0.09 |
| H=126 \* | 1.0361 | +0.0204 | 0.0105 | +1.94 |
| H=252 | 1.1262 | **+0.1105** | 0.0671 | +1.65 |
| CADENCE=W \* | 1.0361 | +0.0204 | 0.0105 | +1.94 |
| CADENCE=M | 0.9669 | −0.0488 | 0.0562 | −0.87 |
| GROSS=0.30 … 0.70 | 1.0311 … 1.0356 | +0.0154 … +0.0198 | 0.0100 … 0.0104 | +1.54 … +1.91 |
| GROSS=0.75 \* | 1.0361 | +0.0204 | 0.0105 | +1.94 |

`*` = a key that IS the incumbent anchor book. P_AXIS and P_1214 are in `.grid.csv` in full.

**THE SIGN CHANGES, AND NOT MARGINALLY.** 4 of 19 distinct stand-in anchors give a NEGATIVE
tuning cost on P_TEXT (3 of 19 on P_AXIS, 1 of 19 on P_1214). The range **[−0.3292, +0.1105]**
is 16x the +0.0204 it contains. **Exactly one candidate is separable from zero at |t| ≥ 2 —
N=5, at −2.16, i.e. the only resolved reading in the whole ladder says tuning PAYS.** The
incumbent's own t is +1.94.

## 3. The decomposition the queue asks for — and why it is not identified

| pick set | D_INC | SUBSTITUTION (mean over 19) | ANCHOR (= D_INC − mean) | share | SUBSTITUTION (median) | ANCHOR (vs median) | share |
|---|---|---|---|---|---|---|---|
| P_1214 | +0.0685 | +0.0655 | +0.0030 | 4.4% | +0.0661 | +0.0024 | 3.5% |
| P_AXIS | +0.0211 | +0.0181 | +0.0030 | 14.2% | +0.0187 | +0.0024 | 11.4% |
| **P_TEXT** | **+0.0204** | **−0.0013** | **+0.0217** | **106.3%** | **+0.0177** | **+0.0027** | **13.2%** |

**The headline decomposition is a choice of summary statistic, not a measurement.** On the
pick set the queue names, "almost all of the +0.0204 is THIS anchor" (106.3%) and "almost
none of it is" (13.2%) are the same data read through a mean and a median, and the whole
difference is one outlier book (N=5, −0.3292). Both are published; neither is the answer.

Restricted to the **9 genuinely different stand-ins** (G12's REAL partition): mean −0.0226,
median +0.0049, **incumbent rank 5 of 10, p = 0.500 — exactly the median book**, 4 of 9
negative. On the **9 near-clones**: mean +0.0176, rank 1 of 10 — the incumbent beats its own
re-leverings by construction (a monotone cost drag), which is the only place it ranks high.

**The incumbent's rank is 5 of 19 (p 0.263) on ALL THREE pick sets, identically.** That is
structural, not a coincidence: gate G9 establishes `DELTA(A) ≡ meanOOS(A) − meanOOS(picks)`
to 3.3e-16, so the picks enter only as an additive constant and **the anchor RANKING carries
no pick information at all** (G13: the anchor column is bit-identical between P_1214 and
P_AXIS, dev 3.3e-16). Once the anchor is walked, "what does the record's tuning cost" is
revealed to be one question — *which book do you name* — wearing three pick sets' clothes.

## 4. No rule-8-legal procedure in this tree recovers the incumbent

Two reference anchor-choosers, reported and not tuned on. **A_IS** picks the anchor by IS
Sharpe over all 22 candidates on warm-up..2016-12-31 only and holds it: it names **N=40 (U56),
N=5 (B136), H=252 (SMALL)** — not the incumbent on any panel — and reads **+0.0028 (t +0.06)**
on P_TEXT. **A_ISFOLD**, re-picking inside each fold's own IS window, reads **−0.0705
(t −1.14)**. On P_AXIS the same arms read +0.1337 (t +2.41) and +0.0236 (t +0.53).

This does not prove the incumbent was fitted to the OOS tape; it establishes the narrower and
checkable thing: **the record's own IS-argmax rule does not name the anchor on any panel, and
an anchor chosen that way is worth nothing (t +0.06) or less than nothing (t −1.14) on the
pick set that produced the +0.0204.** 151's do-nothing finding arriving from the anchor side.

## 5. Where it cuts (`.bycut.csv`, S_ALL, P_TEXT then P_AXIS)

| cut | value | picks | D_INC | t | mean over 19 | ANCHOR | negatives | rank |
|---|---|---|---|---|---|---|---|---|
| P_TEXT panel | U56 / B136 / SMALL | 220/220/180 | +0.0232 / +0.0062 / +0.0342 | +1.25 / +0.27 / +1.07 | −0.0037 / −0.0010 / +0.0012 | +0.0269 / +0.0072 / +0.0330 | 5 / 4 / 3 of 19 | 5 / 7 / 2 |
| P_TEXT ladder | N / H / GROSS / CADENCE | 180/120/260/60 | +0.0532 / −0.0007 / +0.0024 / +0.0419 | +1.83 / −0.01 / +2.01 / +1.32 | +0.0308 / −0.0230 / −0.0183 / +0.0196 | +0.0223 / +0.0223 / +0.0207 / +0.0223 | 4 / 15 / 10 / 4 of 19 | 5 / 5 / 5 / 5 |
| P_AXIS panel | U56 / B136 / SMALL | 56 each | +0.0330 / +0.0639 / −0.0336 | +0.93 / +1.74 / −0.48 | +0.0084 / +0.0664 / −0.0205 | +0.0246 / −0.0025 / −0.0131 | 5 / 1 / 16 of 19 | 5 / 7 / 7 |
| P_AXIS ladder | N / H / GROSS / CADENCE | 42 each | +0.1067 / −0.0594 / +0.0010 / +0.0361 | +3.07 / −0.80 / +2.45 / +1.20 | +0.1037 / −0.0624 / −0.0020 / +0.0331 | +0.0030 at all four | 1 / 17 / 12 / 2 of 19 | 5 at all four |

1224's two strongest cuts survive the walk and are shown to be anchor-free: **N +0.1067 at
t +3.07 sits on a 19-book mean of +0.1037, so only +0.0030 of it is the anchor; H −0.0594
sits on −0.0624.** The axes disagree in sign at nearly every stand-in, not just at this one.
**On SMALL the substitution loses at 16 of 19 anchors** (P_AXIS), so "stop tuning" is not even
sign-stable across panels. GROSS's t +2.45 / +2.01 is again a t-statistic on a tenth of a
basis point of Sharpe (1189/1214/1224) and should never be read as economic.

## 6. Rule 8 and both KEEP paths — nothing promoted, and it reproduces 1224 exactly

Every rung chosen on warm-up..2016-12-31 ONLY; 2017-2026 read once. **288 rule-8 rows**
(3 panels x 4 ladders x 22 anchors, plus the A_IS and S_NONE reference arms), **66 candidate
books**, **207 stitched rolling curves** — all published.

| object | n | 4a | 4b full | 4b OOS | BOTH | distinct books |
|---|---|---|---|---|---|---|
| candidate books | 66 | **0** | 17 | 16 | 15 | 12 |
| rule-8 rows | 288 | **0** | 70 | 66 | 62 | 12 |
| stitched curves | 207 | 8 | 55 | 54 | 54 | — |

The 66 candidate books reproduce 1224's committed `.books.csv` **bit for bit (max OOS Sharpe
deviation 0.0)** and the 15 both-paths books are the **identical set** — 0 new, 0 lost. The 12
distinct passing books are the frozen U56 anchor (**15.71% / 1.1480 / −19.13% full, halves
1.2127/1.1050; OOS 17.16% / 1.1759 / −19.13%**), U56 N=15 (17.07% / 1.1675 / −20.14%; OOS
18.87% / 1.1894), U56 H=21, and eight GROSS re-leverings of the U56 and B136 anchors.
**CONFIRMATORY, NOT GENERATIVE — every pass is a book the record already committed on
2026-09-04 and re-confirmed on 2026-09-15. NOT PROMOTED, NO MEMO, NO RULES CHANGE.**

**The 8 stitched 4a passes are published and are not a candidate.** They are 4 distinct
curves (U56 GROSS 0.30/0.35/0.40/0.45, counted twice because P_1214 and P_AXIS share a fold
set), and **all 4 fail 4b on the CAGR floor** — 6.65–10.04% against SPY's 0.70 x 15.06% =
10.54%. A de-levered anchor clears the low-return live book on both halves and buys nothing
for capital: PROTOCOL rule 4b's own stated reason for existing, arriving as a measurement.

Benchmarks: U56 SPY 15.06% / 0.8815 / −33.72% (halves 0.9600/0.8171), OOS 15.15% / 0.8686 /
−33.72%; U56 LIVE (RULES v2) 8.60% / 1.1982 / −12.05% (1.2332/1.1705), OOS 9.42% / 1.2717.
B136 SPY 15.16% / 0.8862, OOS 15.33% / 0.8769; B136 LIVE 7.98% / 1.0994, OOS 7.88% / 1.1061.
SMALL SPY 14.06% / 0.8582, OOS 15.33% / 0.8769; SMALL LIVE 4.64% / 0.7130, OOS 4.47% / 0.6518.

## 7. Survivorship (rule 9)

U56 (55 names) and B136 (135) are CURRENT constituents; SMALL is the sub-$2B screen, 664
investable of 715 after dropping every ticker with max_1d_move >= 1.0, and starts 2010. SPY is
excluded from every eligible set and used as benchmark only. The bias does not cancel out of
the OOS levels or the 4b legs, so any pass above is an upper bound.

## 8. Gates (15 of 15)

G1 fast runner == engine.backtest 2.78e-17 · G2 the GROSS ladder is the anchor frame scaled
0.0 · G3 live RULES v2 U56 MaxDD −12.0549% == committed −12.05% · G4 the anchor rung of all
four ladders is ONE book bit for bit on all 3 panels 0.0 · G5 the 22 keys collapse to 19
distinct books on every panel · G6 folds tile all three panels with no overlap and no gap ·
G7 every frozen triple is a committed ladder rung (0 bad) · G8 a pick that IS the stand-in
anchor's book has delta 0 at every cell 0.0 · G9 DELTA(A) == meanOOS(A) − meanOOS(picks)
exactly, 3.33e-16 · G10 the incumbent column replays 1224's committed DELTA/SE/means on all
three pick sets, 4.90e-05 · G11 stitched lengths == the sum of their folds · G12 the 9
non-incumbent GROSS rungs are Sharpe-degenerate against the incumbent (0.0040) and every
non-GROSS candidate is not (0.0171) · G13 the anchor column is identical across pick sets
sharing a fold set, 3.33e-16.

## 9. Pre-declared outcome, reported as the arithmetic gives it

(A) fires — median-over-19 +0.0177 > 0 and rank p 0.263 > 0.25 — and **is not a resolution**.
It clears its own p bar by 0.013, its median has a MEAN counterpart of the opposite sign
(−0.0013), 1 of 19 candidates is separable at |t| ≥ 2 and that one is NEGATIVE, and the
incumbent's own t is +1.94. The pre-declared rule was written before the degeneracy census
and weights 9 near-clones equally with 9 real alternatives; on the 9 real ones the incumbent
is the median book at p = 0.500. Reported, not rewritten.

## 10. What this leaves for the queue

Three sentences are worth a future run's header. **(i) THE RECORD'S TUNING COST IS NOT A
NUMBER, IT IS A CHOICE OF ANCHOR** — it spans [−0.3292, +0.1105] over the record's own 19
rung books and changes sign at 4 of them, so any committed figure of the form "tuning costs
X" is a claim about one book that must name it. **(ii) THE SUBSTITUTION / ANCHOR SPLIT IS NOT
IDENTIFIED ON THIS CANDIDATE SET** — mean says 106.3%, median says 13.2%, and half the
candidates are the incumbent re-levered, so the decomposition needs a stated candidate set
and a stated summary statistic before it means anything. **(iii) THE INCUMBENT ANCHOR IS THE
MEDIAN BOOK AMONG THE RECORD'S NON-DEGENERATE ALTERNATIVES (5 of 10, p 0.500), AND NO
RULE-8-LEGAL PROCEDURE IN THIS TREE NAMES IT** — which is a fact about how the anchor was
chosen, not about whether it is good. Three follow-ups filed, all price-only.
