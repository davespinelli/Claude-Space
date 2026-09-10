# Idea 644 — does-PROTOCOL-need-a-T2-DATING-clause-beside-T1 (lane C, 2026-09-10)

**ANSWERED, no KEEP. YES — PROTOCOL needs a T2 clause beside T1, and the load-bearing finding is
that it CANNOT be written as syntax.** Idea 426 named the hole and priced one exclusion, but it
implemented that exclusion as a hand-fixed regex (`shift(-k)|iloc[-1]`). On a hand-truth dating
table that regex **clears 7 of 10 genuinely forward-dated keys**. The certificate proposed here is
20/20.

Script `2026-09-10_does-PROTOCOL-need-a-T2-DATING-clause-beside-T1_C.py`.
Outputs `.console.txt .truth.csv .backfill.csv .crosstab.csv .census.csv .book.csv .walkforward.csv`.
Deterministic: two independent processes produce byte-identical `.backfill.csv` and
`.walkforward.csv`.

## The instrument

T2 mirrors T1's construction, one axis over:

| | perturbation | admissible iff |
|---|---|---|
| T1 (426/433) | across NAMES, `px -> px @ diag(c)` | the value the book consumes does not move |
| **T2 (here)** | **across TIME**, every row STRICTLY AFTER a cut date replaced | **no cell of the key dated AT OR BEFORE the cut moves** |

That is the queue's clause read literally, made executable, and sampling-error-free in the same
sense T1 is: a deterministic invariance check under a seeded operator, not an estimated correlation.

## Gates

| gate | result |
|---|---|
| `fast_bt` == `engine.backtest` | 6.939e-18 at 0 and at 10 bps |
| idea 426's 111-key census re-read from its own `.backfill.csv` | 111 keys, T1 **72 PASS / 39 FAIL** — its published split, exactly |
| the 16-key book set re-derived from 426's own mechanical rule | **kid→expr map identical** to 426's committed `.book.csv` |
| the book grid | 4a **0/420** and 4b **68/57/48/12** at 0/5/10/25 bps — 426's grid reproduced exactly |

## (1) Clause form — TRUTH20 (10 causal keys, 10 leaking keys, truth written first)

| form | false clearances | false rejections |
|---|---|---|
| **SYN** (426's regex, verbatim) | **7/10** — ZFULL, MAXNORM, MINMAX, TRANK, REVMAX, CENTERED, BFILL | 0 |
| SYN+ (regex widened by hand: `bfill`, `iloc[-k]`, `tail`) | 6/10 | 0 |
| **OP1** (certificate, 1 cut) | **0/10** | **0/10** |
| **OP3** (certificate, 3 cuts) | **0/10** | **0/10** |

A regex cannot see a full-sample `px.max()`, a `rank(axis=0)`, a centred rolling mean or a reversed
`cummax` — all of which are pure look-ahead and all of which a reader would plausibly write. **P1
HIT.**

## (2) Corpus — the back-fill, beside 426's T1 column

**On the record's own 111 reconstructible keys, SYN and OP3 agree EXACTLY: 8 FAIL each, the same 8
keys, reach 7 scripts.** Every leak this record currently carries is `iloc[-1]`- or `shift(-k)`-
shaped (5 terminal-ratio variants, 3 forward shifts of 5/21/252 days). No census key contains a
full-sample reducer, `bfill`, `center=True` or `rank(axis=0)` — checked, not assumed.

**That is a MISS on P2, reported as a miss.** The certificate's extra reach is real (TRUTH20) and
currently unexercised. It is worth adopting because it keeps adjudicating keys nobody has written
yet, not because it finds more today.

## (3) T2 is not a relabelling of T1 — the failure sets are DISJOINT

|  | T2 PASS | T2 FAIL |
|---|---|---|
| **T1 PASS** | 64 | **8** |
| **T1 FAIL** | **39** | **0** |

8 keys are T1-PASS/T2-FAIL (`px.iloc[-1]/px - 1` is degree 0, so T1 clears it); 39 are
T1-FAIL/T2-PASS (a 200d mean is degree 1 but strictly backward-looking); **none fails both.** This
falsifies the pre-registered "all four corners" reading (**P3 MISS**) with something stronger:
the two clauses never fire together, so adopting either alone leaves the other's entire failure set
admitted.

## Rule 8 — the price of each gate, and the decomposition 426 could not do

(KEY, m) chosen on 2010–2016 IS Sharpe, 2017–2026 read once, 10 bps, 4 (panel, book) cells.

| chooser | pick | mean ΔOOS Sharpe vs S_ALL | beats SPY | beats RULES v2 |
|---|---|---|---|---|
| S_ALL (no gate) | K10 / +1.00 in **4/4** | — | 4/4 | 4/4 |
| S_T1 | K10 / +1.00 in 4/4 | **+0.0000** (identical pick 4/4) | 4/4 | 4/4 |
| S_T2SYN | K02 or K08 / −1.00 | **−0.3292** (moves the pick 4/4) | 3/4 | 2/4 |
| **S_T2OP3** | same as SYN here | **−0.3292** | 3/4 | 2/4 |
| S_T1T2 | K15 / K06 | **−0.4508** | 2/4 | 2/4 |

**DECOMPOSITION.** 426 published T1 alone at +0.0000 and T1+dating at −0.4508 and could not say
which clause carried it. **T2 carries 73.0% of the joint price on its own; T1 adds the remaining
−0.1216 only CONDITIONAL on T2** — because the arm T2 leaves behind is T1-FAIL in **4 of 4** cells
(K02 the 200d mean ×3, K08 a panel handle ×1). So T1 is inert alone and *not* inert given T2: a
record that adopted T2 alone would publish a book resting on a degree-1 key. Both clauses are
needed, and the order is T1 *and* T2, not T1 *or* T2. **P4 HIT** (price −0.3292 < 0, 4a 0/420).

Read the sign the right way round: a negative price is the clause working. The Sharpe it gives up
was never earnable — the removed arm is `px.iloc[-1]/px − 1.0` at m=+1.00, best cell U56/MA200
**OOS 21.58% / 1.527 / −22.25%** against SPY 15.32%/0.876/−33.72% and RULES v2 9.48%/1.279/−12.05%.

## Book / KEEP paths

4a **0/420 at every rung**. 4b 68/57/48/12 at 0/5/10/25 bps; deduped for the shared m=0 control
55/44/35/12 of 364. Every 4b pass is the underlying book clearing, not the key (the m=0 control
passes 4b alone in the U56/MA200 cell and still loses RULES v2 OOS, 1.106 vs 1.279). No rule-8 pick
passes 4b — all fail the drawdown leg except U56/MA200 S_NONE. Gross held equal across every tilt
(grid range 0.7499–0.7504, spread 4.45e-04), so m moves the cross-section and never the exposure.
Rule 8 passed over **10 arms** that clear 4b, are T1-PASS *and* T2-PASS, and beat their own control
OOS.

## The drafted clause (report-only; PROTOCOL.md NOT edited — rule 6, Sunday review)

Full text in `.console.txt` PART 5. Clause 11 sits **beside** clause 10, not inside it: (a)
reproducibility gate; (b) the causality certificate at ≥3 cuts as the adjudicator, with the regex
allowed only as a reader's aid; (c) necessary-not-sufficient and independent of T1; (d) must run
BEFORE rule 8, because rule 8 splits by DATE and a terminal-dated key is dated at T in both halves.

## Verdict

**ANSWERED / no KEEP.** The deliverable is the T2 clause plus the 111-key T2 column beside 426's T1
column. Two things the queue's draft did not anticipate: the exclusion must be an **instrument, not
a syntax list** (7/10 on TRUTH20), and T1 and T2 fail **disjoint** sets of this record's keys, so
neither substitutes for the other.

**SURVIVORSHIP:** U56 and SMALL439 are both current constituents, SMALL doubly so. No book is
proposed on either.

**LIMITS:** the census is idea 426's reachable 19.4% of key-bearing sites (the free-variable wall is
80.6%, idea 643's question); the certificate is run on a 500d × 100-name slice, so a key whose
future-reading is confined to rows outside that slice would not be detected.

RULES.md, PROTOCOL.md, scan.py, bot.py, baseline.py untouched.

## Follow-ups filed

* the T2 column can only be as wide as the harvest — the wall (idea 643) caps T2 exactly as it caps
  T1, and both clauses are worth exactly the reach of the convention that feeds them;
* SYN and OP3 agreeing on this corpus is a fact about *today's* record; a T2 column should be
  re-run, not re-quoted, once the wall is cleared.
